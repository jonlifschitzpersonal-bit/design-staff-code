#!/usr/bin/env python3
"""Validate a discovery dossier and, with --ready, the gate «listo para diseñar».

Part of the design-staff-code plugin. A discovery dossier is created with
`case.py init <slug> --kind discovery` and ends in 10-design-brief.md.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys

from validate_dossier import OPEN_FIX, resolve_link_file


STAGES = (
    "00-encuadre.md", "01-plan-de-research.md", "02-campo.md", "03-sintesis.md", "04-benchmark.md",
    "05-situacion-actual.md", "06-oportunidades.md", "07-situacion-futura.md", "08-historias.md",
    "09-baja-fidelidad.md",
)
BRIEF = "10-design-brief.md"
REQUIRED = (*STAGES, BRIEF, "critiques.md")
NOT_SKIPPABLE = {"00-encuadre.md"}
PENDING = "_Pendiente._"
SKIPPED = re.compile(r"^\*\*Etapa salteada:\*\*\s*\S", re.MULTILINE)
UNRESOLVED_TEMPLATE = re.compile(r"\{\{[A-Z_]+\}\}")
VALIDATION_LINE = re.compile(r"^\*\*Validación con usuarios:\*\*\s*(\w+)", re.MULTILINE | re.IGNORECASE)
VALIDATION_VALUES = {"realizada", "parcial", "pendiente"}
REFERENCED_EVENTS = {"research", "proposal", "critique", "revision", "discard", "decision", "validation", "correction"}
READY_OUTCOME = "ready_for_design"
REVIEWER = "design-critic"


def section(content: str, heading: str) -> str:
    match = re.search(rf"^## {re.escape(heading)}\s*$", content, re.MULTILINE)
    if not match:
        return ""
    rest = content[match.end():]
    following = re.search(r"^## ", rest, re.MULTILINE)
    return rest[: following.start()] if following else rest


def table_rows(text: str) -> int:
    """Data rows of Markdown tables: lines starting with '|' that are neither header separators nor headers."""
    rows = 0
    lines = [line.strip() for line in text.splitlines()]
    for index, line in enumerate(lines):
        if not line.startswith("|") or re.fullmatch(r"\|[\s:|-]+\|", line):
            continue
        is_header = index + 1 < len(lines) and re.fullmatch(r"\|[\s:|-]+\|", lines[index + 1] or "")
        if not is_header:
            rows += 1
    return rows


def validate(dossier: Path, *, ready: bool = False) -> tuple[list[str], int]:
    errors: list[str] = []
    dossier = resolve_link_file(dossier)
    if not dossier.is_dir():
        return [f"No existe el directorio: {dossier}"], 0

    texts: dict[str, str] = {}
    for name in REQUIRED:
        path = dossier / name
        if not path.is_file():
            errors.append(f"Falta {name}")
            continue
        texts[name] = path.read_text(encoding="utf-8")
        if UNRESOLVED_TEMPLATE.search(texts[name]):
            errors.append(f"{name} tiene variables de plantilla sin resolver")

    events: list[dict] = []
    event_path = dossier / "events.jsonl"
    if not event_path.is_file():
        errors.append("Falta events.jsonl")
    else:
        for number, line in enumerate(event_path.read_text(encoding="utf-8").splitlines(), start=1):
            if not line.strip():
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError as exc:
                errors.append(f"events.jsonl:{number} no es JSON válido: {exc.msg}")
                continue
            for field in ("timestamp", "actor", "type", "summary", "refs"):
                if field not in entry:
                    errors.append(f"events.jsonl:{number} no tiene '{field}'")
            if entry.get("type") in REFERENCED_EVENTS and not entry.get("refs"):
                errors.append(f"events.jsonl:{number} ({entry.get('type')}) necesita al menos una referencia")
            events.append(entry)

    if not ready:
        return errors, len(events)

    skipped = {name for name in STAGES if name in texts and SKIPPED.search(texts[name])}
    for name in STAGES:
        if name not in texts:
            continue
        if name in skipped and name in NOT_SKIPPABLE:
            errors.append(f"{name} no se puede saltear")
        elif name not in skipped and PENDING in texts[name]:
            errors.append(f"{name} tiene secciones pendientes; completalas o declarala con **Etapa salteada:**")
    if "02-campo.md" in texts and "02-campo.md" not in skipped and table_rows(texts["02-campo.md"]) == 0:
        errors.append("02-campo.md no registra ninguna sesión; si no hubo campo, declarala con **Etapa salteada:**")

    brief = texts.get(BRIEF, "")
    if brief:
        if PENDING in brief:
            errors.append(f"{BRIEF} tiene secciones pendientes")
        match = VALIDATION_LINE.search(brief)
        value = match.group(1).lower() if match else ""
        if value not in VALIDATION_VALUES:
            errors.append(f"{BRIEF} necesita **Validación con usuarios:** realizada, parcial o pendiente")
        elif "02-campo.md" in skipped and value != "pendiente":
            errors.append(f"Sin campo (02 salteada), {BRIEF} debe decir **Validación con usuarios:** pendiente")
        elif "09-baja-fidelidad.md" in skipped and value == "realizada":
            errors.append(f"Sin test (09 salteada), {BRIEF} no puede decir **Validación con usuarios:** realizada")
        if table_rows(section(brief, "Estado de la evidencia")) == 0:
            errors.append(f"{BRIEF} necesita la tabla de supuestos críticos en «Estado de la evidencia»")

    if OPEN_FIX.search(texts.get("critiques.md", "")):
        errors.append("critiques.md tiene un hallazgo «Corregir» abierto")

    reviews = [e for e in events if e.get("type") == "validation" and e.get("actor") == REVIEWER]
    if not reviews:
        errors.append("Falta la revisión del design-critic (evento validation con su informe en reviews/)")
    elif not any((dossier / ref).is_file() for ref in reviews[-1].get("refs", [])
                 if isinstance(ref, str) and ref.startswith("reviews/")):
        errors.append("La última revisión del design-critic no enlaza un informe existente en reviews/")
    if not any(e.get("type") == "decision" and e.get("outcome") == READY_OUTCOME for e in events):
        errors.append(f"Falta el evento decision con outcome={READY_OUTCOME}")
    return errors, len(events)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dossier", type=Path, help="Ruta a design/initiatives/<slug> de un discovery")
    parser.add_argument("--ready", action="store_true", help="Comprobar el gate «listo para diseñar»")
    parser.add_argument("--json", action="store_true", help="Imprimir resultado como JSON")
    args = parser.parse_args()
    errors, count = validate(args.dossier, ready=args.ready)
    if args.json:
        print(json.dumps({"ok": not errors, "events": count, "errors": errors}, ensure_ascii=False, indent=2))
    elif errors:
        print("El discovery no pasa:" if args.ready else "Estructura incompleta:")
        for error in errors:
            print(f"- {error}")
    elif args.ready:
        print(f"Listo para diseñar: {args.dossier} ({count} evento(s))")
    else:
        print(f"Estructura presente: {args.dossier} ({count} evento(s))")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
