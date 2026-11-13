#!/usr/bin/env python3
"""Create design dossiers and append auditable events without overwriting history.

Part of the design-staff-code plugin. Run it from the project root; dossiers live in <project>/design/initiatives
(override with DESIGN_INITIATIVES_DIR or DESIGN_PROJECT_DIR).
"""

from __future__ import annotations

import argparse
from datetime import datetime
import json
import os
from pathlib import Path
import re
import sys

try:
    import fcntl
except ImportError:  # Windows: sin flock; se escribe la línea completa en una sola llamada.
    fcntl = None


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = PLUGIN_ROOT / "templates" / "initiative"
TEMPLATE_KINDS = {"initiative": TEMPLATES, "discovery": PLUGIN_ROOT / "templates" / "discovery"}


def project_root() -> Path:
    """Raíz del proyecto: DESIGN_PROJECT_DIR, o el primer ancestro del cwd con .claude o .git."""
    override = os.environ.get("DESIGN_PROJECT_DIR")
    if override:
        return Path(override).resolve()
    here = Path.cwd().resolve()
    for candidate in (here, *here.parents):
        if (candidate / ".claude").is_dir() or (candidate / ".git").exists():
            return candidate
    return here


if os.environ.get("DESIGN_INITIATIVES_DIR"):
    INITIATIVES = Path(os.environ["DESIGN_INITIATIVES_DIR"]).resolve()
else:
    INITIATIVES = project_root() / "design" / "initiatives"
EVENT_TYPES = {
    "start", "research", "proposal", "critique", "revision", "discard",
    "decision", "validation", "handoff", "correction",
}
REFERENCED_EVENTS = {"research", "proposal", "critique", "revision", "discard", "decision", "validation", "correction"}
SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def check_slug(value: str) -> str:
    if not SLUG.fullmatch(value):
        raise argparse.ArgumentTypeError(
            "El slug debe usar minúsculas, números y guiones simples."
        )
    return value


def append_event(path: Path, event: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as stream:
        if fcntl is not None:
            fcntl.flock(stream, fcntl.LOCK_EX)
        stream.write(json.dumps(event, ensure_ascii=False, separators=(",", ":")) + "\n")
        stream.flush()
        if fcntl is not None:
            fcntl.flock(stream, fcntl.LOCK_UN)


def initialize(args: argparse.Namespace) -> int:
    if args.actor is None:
        args.actor = "discovery-lead" if args.kind == "discovery" else "staff-design-lead"
    folder = INITIATIVES / args.slug
    if folder.exists():
        print(f"Ya existe: {folder}", file=sys.stderr)
        return 1
    folder.mkdir(parents=True)
    today = datetime.now().astimezone().date().isoformat()
    if args.kind == "discovery":
        (folder / "fuentes").mkdir()
        (folder / "reviews").mkdir()
    for template in sorted(TEMPLATE_KINDS[args.kind].glob("*.md")):
        content = template.read_text(encoding="utf-8")
        content = (content.replace("{{TITLE}}", args.title)
                          .replace("{{SLUG}}", args.slug)
                          .replace("{{DATE}}", today))
        (folder / template.name).write_text(content, encoding="utf-8")
    append_event(folder / "events.jsonl", {
        "timestamp": now(),
        "actor": args.actor,
        "type": "start",
        "summary": f"Abrí {'el discovery' if args.kind == 'discovery' else 'la iniciativa'}: {args.title}",
        "refs": ["00-encuadre.md" if args.kind == "discovery" else "brief.md"],
        "next": "Completar el encuadre y las fuentes",
    })
    print(folder)
    return 0


def initiative_folder(slug: str) -> Path:
    """Follow a Git symlink checked out as a plain text file (core.symlinks=false on Windows)."""
    folder = INITIATIVES / slug
    try:
        if folder.is_file() and folder.stat().st_size < 1024:
            target = (folder.parent / folder.read_text(encoding="utf-8").strip()).resolve()
            if target.is_dir():
                return target
    except (OSError, UnicodeError, ValueError):
        pass
    return folder


def event(args: argparse.Namespace) -> int:
    folder = initiative_folder(args.slug)
    if not folder.is_dir():
        print(f"No existe el expediente: {folder}", file=sys.stderr)
        return 1
    if args.type in REFERENCED_EVENTS and not args.ref:
        print("Este evento requiere --ref con un ID, archivo o URL; si no hay fuente, usá --ref 'no-source:motivo'.", file=sys.stderr)
        return 2
    if args.type in {"revision", "validation"} and not args.artifact_version:
        print("Las revisiones y validaciones requieren --artifact-version para identificar la versión exacta.", file=sys.stderr)
        return 2
    entry: dict[str, object] = {
        "timestamp": now(),
        "actor": args.actor,
        "type": args.type,
        "summary": args.summary,
        "refs": args.ref,
    }
    if args.outcome:
        entry["outcome"] = args.outcome
    if args.next:
        entry["next"] = args.next
    if args.artifact_version:
        entry["artifact_version"] = args.artifact_version
    append_event(folder / "events.jsonl", entry)
    print(f"Registrado: {folder / 'events.jsonl'}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Crear un expediente sin sobrescribir otro")
    init_parser.add_argument("slug", type=check_slug)
    init_parser.add_argument("--title", required=True)
    init_parser.add_argument("--actor", default=None,
                             help="Por defecto: staff-design-lead, o discovery-lead con --kind discovery")
    init_parser.add_argument("--kind", choices=sorted(TEMPLATE_KINDS), default="initiative",
                             help="initiative (expediente de diseño) o discovery (fase previa al diseño)")
    init_parser.set_defaults(run=initialize)

    event_parser = subparsers.add_parser("event", help="Agregar un evento cronológico")
    event_parser.add_argument("slug", type=check_slug)
    event_parser.add_argument("--actor", required=True)
    event_parser.add_argument("--type", required=True, choices=sorted(EVENT_TYPES))
    event_parser.add_argument("--summary", required=True)
    event_parser.add_argument("--ref", action="append", default=[])
    event_parser.add_argument("--outcome")
    event_parser.add_argument("--next")
    event_parser.add_argument("--artifact-version")
    event_parser.set_defaults(run=event)

    args = parser.parse_args()
    return args.run(args)


if __name__ == "__main__":
    sys.exit(main())
