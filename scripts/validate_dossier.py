#!/usr/bin/env python3
"""Check the mechanical integrity of one design initiative dossier.

This intentionally does not score design quality or the truth of claims.
"""

from __future__ import annotations

import argparse
from datetime import datetime
import json
from pathlib import Path
import re
import sys


REQUIRED_MARKDOWN = (
    "brief.md",
    "evidence.md",
    "exploration.md",
    "critiques.md",
    "decision.md",
    "artifacts.md",
)
EVENT_TYPES = {
    "start",
    "research",
    "proposal",
    "critique",
    "revision",
    "discard",
    "decision",
    "validation",
    "handoff",
    "correction",
}
REFERENCED_EVENTS = {"research", "proposal", "critique", "revision", "discard", "decision", "validation", "correction"}
LOCAL_SUFFIXES = {
    ".md", ".json", ".jsonl", ".png", ".jpg", ".jpeg",
    ".gif", ".svg", ".pdf", ".fig", ".html",
}
SCHEME = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")
UNRESOLVED_TEMPLATE = re.compile(r"\{\{[A-Z_]+\}\}")
CASE_STUDY_PATH = re.compile(r"((?:[A-Za-z0-9._-]+/)*CASO_[A-Za-z0-9._-]+\.md)")
REQUIRED_READY_EVENTS = {"research", "proposal", "critique", "decision"}
VISUAL_LENSES = ("critique", "clarify", "distill")
REVIEW_ACTORS = {"evidence-scout", "design-critic"}
REQUIRED_REVIEWER = "design-critic"
TEXT_ONLY = "text_only"
# Una fila de critiques.md con un hallazgo de nivel Corregir que sigue abierto bloquea el cierre.
OPEN_FIX = re.compile(r"^\|.*\bCorregir\b.*\|\s*(?:\*\*)?abierto(?:\*\*)?\s*\|", re.MULTILINE | re.IGNORECASE)
TEMPLATES = Path(__file__).resolve().parents[1] / "templates" / "initiative"
PROJECT_ROOT: Path | None = None  # Si es None, se busca desde el expediente (tests pueden fijarlo).


def project_root(dossier: Path) -> Path:
    if PROJECT_ROOT is not None:
        return PROJECT_ROOT
    start = dossier.resolve()
    for candidate in (start, *start.parents):
        if (candidate / ".claude").is_dir() or (candidate / ".git").exists():
            return candidate
    return Path.cwd().resolve()


def nonempty_string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def local_ref_path(ref: str, dossier: Path) -> Path | None:
    """Resolve explicit references inside the dossier; IDs and URLs are opaque."""
    if SCHEME.match(ref) or ref.startswith("#"):
        return None
    raw_path = ref.split("#", 1)[0]
    if not raw_path:
        return None
    relative = Path(raw_path)
    if relative.is_absolute() or raw_path.startswith("../"):
        return None  # External file: may be outside this evaluation's access.
    if not (raw_path.startswith("./") or relative.suffix.lower() in LOCAL_SUFFIXES):
        return None  # Evidence ID, Figma node ID, etc.
    resolved = (dossier / relative).resolve()
    if not resolved.is_relative_to(dossier.resolve()):
        return None
    return resolved


def section(content: str, heading: str) -> str:
    match = re.search(rf"^## {re.escape(heading)}\s*$", content, re.MULTILINE)
    if not match:
        return ""
    following = re.search(r"^## ", content[match.end():], re.MULTILINE)
    return content[match.end():match.end() + following.start()] if following else content[match.end():]


def review_report_present(event: dict, dossier: Path) -> bool:
    refs = event.get("refs")
    if not isinstance(refs, list):
        return False
    for ref in refs:
        if not isinstance(ref, str) or not ref.startswith("reviews/"):
            continue
        path = local_ref_path(ref, dossier)
        try:
            if path is not None and path.is_file() and path.read_text(encoding="utf-8").strip():
                return True
        except (OSError, UnicodeError):
            continue
    return False


def provisional_blockers_present(decision: str) -> bool:
    closure = section(decision, "Cierre provisional")
    lines = closure.splitlines()
    header = "| Dependencia externa | Responsable | Prueba de desbloqueo |"
    try:
        start = next(index for index, line in enumerate(lines) if line.strip() == header)
    except StopIteration:
        return False
    if start + 1 >= len(lines) or not re.fullmatch(r"\|(?:\s*:?-+:?\s*\|){3}", lines[start + 1].strip()):
        return False
    for line in lines[start + 2:]:
        if not line.strip().startswith("|"):
            break
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        placeholders = {"pendiente", "por definir", "sin definir", "n/a", "-", "tbd"}
        if (len(cells) == 3 and all(cells)
                and not any(UNRESOLVED_TEMPLATE.search(cell) or cell.lower() in placeholders for cell in cells)):
            return True
    return False


def buildable_status_claimed(decision: str) -> bool:
    positive = r"(?:construible|list[oa] para construir|aprobad[oa] para construir|build[- ]ready|habilitad[oa] para construir)"
    for line in decision.splitlines():
        match = re.match(r"^\*\*(?:Estado|Estado de cierre|Construcción):\*\*\s*(.+)$", line)
        if match and re.match(rf"^(?:\*\*|`)?{positive}\b", match.group(1).strip(), re.IGNORECASE):
            return True
    execution = section(decision, "Estado de ejecución")
    for line in execution.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [cell.strip().replace("*", "").lower() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        status = cells[1]
        if re.match(rf"^(?:ahora[: ]+)?{positive}\b", status):
            return True
    return False


def resolve_link_file(path: Path) -> Path:
    """Follow a Git symlink checked out as a plain text file (core.symlinks=false on Windows)."""
    try:
        if path.is_file() and path.stat().st_size < 1024:
            target = (path.parent / path.read_text(encoding="utf-8").strip()).resolve()
            if target.exists() and target != path.resolve():
                return target
    except (OSError, UnicodeError, ValueError):
        pass
    return path


def validate(dossier: Path, *, ready: bool = False, case_study: bool = False,
             provisional: bool = False) -> tuple[list[str], int]:
    errors: list[str] = []
    if provisional and ready:
        errors.append("--ready y --provisional son modos de cierre excluyentes")
    if provisional and not case_study:
        errors.append("--provisional requiere --case-study")
    dossier = resolve_link_file(dossier)
    if not dossier.is_dir():
        return [f"No existe el directorio: {dossier}"], 0

    markdown: dict[str, str] = {}
    for filename in REQUIRED_MARKDOWN:
        path = dossier / filename
        if not path.is_file():
            errors.append(f"Falta {filename}")
            continue
        try:
            content = path.read_text(encoding="utf-8")
            markdown[filename] = content
            if not content.strip():
                errors.append(f"{filename} está vacío")
        except OSError as exc:
            errors.append(f"No se pudo leer {filename}: {exc}")

    event_path = dossier / "events.jsonl"
    if not event_path.is_file():
        errors.append("Falta events.jsonl")
        return errors, 0

    try:
        lines = event_path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        errors.append(f"No se pudo leer events.jsonl: {exc}")
        return errors, 0

    if not lines:
        errors.append("events.jsonl está vacío")
    valid_events = 0
    event_types: set[str] = set()
    parsed_events: list[dict] = []
    for number, line in enumerate(lines, start=1):
        label = f"events.jsonl:{number}"
        if not line.strip():
            errors.append(f"{label}: línea vacía")
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"{label}: JSON inválido ({exc.msg})")
            continue
        if not isinstance(event, dict):
            errors.append(f"{label}: se esperaba un objeto JSON")
            continue
        parsed_events.append(event)

        timestamp = event.get("timestamp")
        if not nonempty_string(timestamp):
            errors.append(f"{label}: falta timestamp")
        else:
            try:
                parsed = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
                if "T" not in timestamp or parsed.tzinfo is None:
                    raise ValueError("se requiere fecha, hora y zona horaria")
            except ValueError:
                errors.append(f"{label}: timestamp debe ser ISO 8601 con zona horaria")

        if not nonempty_string(event.get("actor")):
            errors.append(f"{label}: falta actor")
        event_type = event.get("type")
        if not isinstance(event_type, str) or event_type not in EVENT_TYPES:
            errors.append(f"{label}: type inválido ({event_type!r})")
        else:
            event_types.add(event_type)
        if not nonempty_string(event.get("summary")):
            errors.append(f"{label}: falta summary")

        refs = event.get("refs")
        if not isinstance(refs, list):
            errors.append(f"{label}: refs debe ser una lista")
        else:
            if event_type in REFERENCED_EVENTS and not refs:
                errors.append(f"{label}: {event_type} requiere al menos una referencia o 'no-source:motivo'")
            for index, ref in enumerate(refs):
                if not nonempty_string(ref):
                    errors.append(f"{label}: refs[{index}] debe ser un string no vacío")
                    continue
                local_path = local_ref_path(ref, dossier)
                if local_path is not None and not local_path.exists():
                    errors.append(f"{label}: referencia local inexistente: {ref}")
        if event_type in {"revision", "validation"} and not nonempty_string(event.get("artifact_version")):
            errors.append(f"{label}: {event_type} requiere artifact_version")
        valid_events += 1

    if ready or provisional:
        brief = markdown.get("brief.md", "")
        title_match = re.search(r"^# Brief · (.+)$", brief, re.MULTILINE)
        date_match = re.search(r"^\*\*Fecha de inicio:\*\* (\d{4}-\d{2}-\d{2})", brief, re.MULTILINE)
        if not title_match or not date_match:
            errors.append("brief.md necesita título y fecha de inicio para comprobar el borrador")
        for filename, content in markdown.items():
            if UNRESOLVED_TEMPLATE.search(content):
                errors.append(f"{filename} contiene marcadores de plantilla sin resolver")
            template_path = TEMPLATES / filename
            file_title = re.search(r"^# [^\n·]+ · (.+)$", content, re.MULTILINE)
            file_date = re.search(r"^\*\*Fecha(?: de inicio)?:\*\* (\d{4}-\d{2}-\d{2})", content, re.MULTILINE)
            effective_title = file_title or title_match
            effective_date = file_date or date_match
            if effective_title and effective_date and template_path.is_file():
                template = (template_path.read_text(encoding="utf-8")
                            .replace("{{TITLE}}", effective_title.group(1))
                            .replace("{{SLUG}}", dossier.name)
                            .replace("{{DATE}}", effective_date.group(1)))
                if content == template:
                    errors.append(f"{filename} sigue igual que la plantilla inicial")
        captures = dossier / "capturas"
        if captures.is_dir() and any(captures.iterdir()):
            visual = section(markdown.get("critiques.md", ""), "Pasada visual final").lower()
            for lens in VISUAL_LENSES:
                if lens not in visual:
                    errors.append(f"critiques.md: la pasada visual final no registra la guía {lens} (hay capturas en el expediente)")
        missing = REQUIRED_READY_EVENTS - event_types
        if missing:
            errors.append("Faltan eventos para cerrar la iniciativa: " + ", ".join(sorted(missing)))
        decision = markdown.get("decision.md", "")
        for heading in ("Restricciones confirmadas", "Estado de ejecución"):
            if not re.search(rf"^## {re.escape(heading)}\s*$", decision, re.MULTILINE):
                errors.append(f"decision.md necesita la sección '{heading}' para revisar límites y alcance de ejecución")

    if case_study:
        artifacts = markdown.get("artifacts.md", "")
        linked = CASE_STUDY_PATH.findall(artifacts)
        if not linked:
            errors.append("artifacts.md no enlaza un caso de estudio CASO_*.md")
        root = project_root(dossier)
        for filename in linked:
            path = root / filename if "/" in filename else root / "docs" / "briefs" / filename
            path = resolve_link_file(path)
            try:
                present = path.is_file() and bool(path.read_text(encoding="utf-8").strip())
            except OSError:
                present = False
            if not present:
                errors.append(f"Falta o está vacío el caso de estudio: {path}")
        if ready or provisional:
            # Una sola ronda de revisión: las revisiones text_only posteriores no invalidan el informe recibido.
            revisions = [index for index, event in enumerate(parsed_events) if event.get("type") == "revision"]
            material = [index for index in revisions if parsed_events[index].get("outcome") != TEXT_ONLY]
            last_material = material[-1] if material else (revisions[0] if revisions else -1)
            current_version = parsed_events[revisions[-1]].get("artifact_version") if revisions else None
            allowed_versions = {
                parsed_events[index].get("artifact_version") for index in revisions if index >= last_material
            }
            latest_reviews: dict[str, tuple[int, dict]] = {}
            for index, event in enumerate(parsed_events):
                if index > last_material and event.get("type") == "validation" and event.get("actor") in REVIEW_ACTORS:
                    latest_reviews[event["actor"]] = (index, event)
            accepted = {"clear", "findings", "blocked_external"} if provisional else {"clear", "findings"}
            required = {REQUIRED_REVIEWER} | set(latest_reviews)
            valid_reviews = {
                actor for actor, (_, event) in latest_reviews.items()
                if nonempty_string(current_version)
                and event.get("artifact_version") in allowed_versions
                and event.get("outcome") in accepted
                and review_report_present(event, dossier)
            }
            missing_reviews = required - valid_reviews
            if missing_reviews:
                errors.append(
                    "Falta el informe de revisión de la versión vigente (posterior a la última revisión material, "
                    "con informe en reviews/ y outcome " + "/".join(sorted(accepted)) + "): "
                    + ", ".join(sorted(missing_reviews))
                )
            if OPEN_FIX.search(markdown.get("critiques.md", "")):
                errors.append("critiques.md tiene hallazgos de nivel 'Corregir' marcados como abiertos")
            if provisional:
                closure = section(markdown.get("decision.md", ""), "Cierre provisional")
                if not re.search(r"^\*\*Estado de cierre:\*\*\s*`?pending_external`?\s*$", closure, re.MULTILINE):
                    errors.append("decision.md necesita '## Cierre provisional' y '**Estado de cierre:** pending_external'")
                if not re.search(r"^\*\*Construcción:\*\*\s*bloqueada\s*$", closure, re.MULTILINE):
                    errors.append("El cierre provisional debe declarar '**Construcción:** bloqueada'")
                if not provisional_blockers_present(markdown.get("decision.md", "")):
                    errors.append("El cierre provisional necesita una dependencia externa con responsable y prueba de desbloqueo")
                if buildable_status_claimed(markdown.get("decision.md", "")):
                    errors.append("Estado de ejecución afirma que una variante es construible durante el cierre provisional")
                last_review_index = max((index for index, _ in latest_reviews.values()), default=-1)
                closure_events = [
                    event for index, event in enumerate(parsed_events)
                    if index > last_review_index and event.get("type") == "decision"
                    and event.get("outcome") == "pending_external"
                ]
                if (not closure_events
                        or closure_events[-1].get("artifact_version") not in allowed_versions
                        or "decision.md" not in (closure_events[-1].get("refs") or [])):
                    errors.append("Falta un evento decision con outcome=pending_external, versión vigente y --ref decision.md después del informe")

    return errors, valid_events


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dossier", type=Path, help="Ruta a design/initiatives/<slug>")
    parser.add_argument("--json", action="store_true", help="Imprimir resultado como JSON")
    closure_mode = parser.add_mutually_exclusive_group()
    closure_mode.add_argument("--ready", action="store_true", help="Comprobar cierre con la ronda de revisión respondida y sin dependencias externas")
    closure_mode.add_argument("--provisional", action="store_true", help="Comprobar cierre pendiente por dependencias externas, sin permiso para construir")
    parser.add_argument("--case-study", action="store_true", help="Exigir caso de estudio Markdown enlazado y existente")
    args = parser.parse_args()

    errors, event_count = validate(args.dossier, ready=args.ready, case_study=args.case_study,
                                   provisional=args.provisional)
    result = {
        "dossier": str(args.dossier),
        "valid": not errors,
        "ready_check": args.ready,
        "provisional_check": args.provisional,
        "case_study_required": args.case_study,
        "event_count": event_count,
        "errors": errors,
    }
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif errors:
        print(f"Expediente con {len(errors)} problema(s): {args.dossier}")
        for error in errors:
            print(f"- {error}")
    else:
        label = ("Cierre provisional documentado; construcción bloqueada" if args.provisional else
                 "Preparado para revisión estructural" if args.ready else
                 "Estructura presente; puede ser un borrador")
        print(f"{label}: {args.dossier} ({event_count} evento(s))")
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
