#!/usr/bin/env python3
"""Prepara un proyecto de Claude Code aislado para evaluar el sistema con un caso de diseño.

Los casos genéricos viven en `evals/cases/` del plugin. Un proyecto puede tener casos propios (por ejemplo, un
replay histórico con la solución oculta) y pasarlos con `--cases-dir`.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import sys


PLUGIN = Path(__file__).resolve().parents[1]
PLUGIN_CASES = Path(__file__).resolve().parent / "cases"


def list_cases(directory: Path) -> list[str]:
    if not directory.is_dir():
        return []
    return sorted(p.name for p in directory.iterdir() if (p / "brief.md").is_file())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case", help="Nombre del caso (carpeta con brief.md)")
    parser.add_argument("output", type=Path, help="Directorio nuevo, fuera de cualquier proyecto real")
    parser.add_argument("--cases-dir", type=Path,
                        help="Carpeta de casos propios del proyecto. Por defecto, los del plugin")
    parser.add_argument("--project", type=Path, default=Path.cwd(),
                        help="Proyecto real que la prueba no debe contener (por defecto, el directorio actual)")
    args = parser.parse_args()

    cases_dir = (args.cases_dir or PLUGIN_CASES).expanduser().resolve()
    available = list_cases(cases_dir)
    if args.case not in available:
        parser.error(f"No existe el caso '{args.case}' en {cases_dir}. Disponibles: {', '.join(available) or 'ninguno'}")

    output = args.output.expanduser().resolve()
    project = args.project.expanduser().resolve()
    if output.exists():
        parser.error(f"Ya existe: {output}; elegí un directorio nuevo")
    for forbidden in (project, PLUGIN):
        if output == forbidden or output.is_relative_to(forbidden):
            parser.error(f"La prueba debe quedar fuera de {forbidden}")

    output.mkdir(parents=True)
    # Agentes, skills, plantillas y scripts se cargan desde el plugin con --plugin-dir: no se copian.
    # reviewer.md nunca se copia: es la guía del revisor humano.
    shutil.copy2(cases_dir / args.case / "brief.md", output / "brief_input.md")
    (output / ".claude").mkdir(parents=True, exist_ok=True)
    # El plugin trae defaultEnabled: false. Cargado con --plugin-dir se habilita con la clave `@inline`;
    # sin ella, la corrida arranca sin los agentes del sistema.
    (output / ".claude" / "settings.json").write_text(
        '{"agent":"design-staff-code:staff-design-lead","enabledPlugins":{"design-staff-code@inline":true}}\n',
        encoding="utf-8",
    )
    source_boundary_note = (
        "\nLa consigna de fuente única prevalece sobre las instrucciones generales de los agentes "
        "y skills. Para esta evaluación no abras ejemplos ni casos de otros proyectos. Usá el método de "
        "los agentes y skills del plugin `design-staff-code`, `STAFF_STANDARD.md` y las plantillas del expediente. "
        "Si leés una fuente externa por error, declaralo y no presentes la corrida como ciega.\n"
    )
    (output / "CLAUDE.md").write_text(
        "# Prueba separada de product design\n\n"
        "Este proyecto es un fixture de evaluación, ficticio o histórico según el caso. "
        "No describe un producto vigente. La única fuente de hechos del caso es `brief_input.md`. "
        "No abras el repositorio real de ningún proyecto, Figma, FigJam ni los documentos `reviewer.md`; "
        "no uses datos de esos lugares para completar los vacíos. "
        "El `STAFF_STANDARD.md` del plugin `design-staff-code` sirve como método, no como evidencia del caso. "
        "Si una fuente o un artefacto visual falta, registrá la limitación.\n\n"
        "Trabajá con `staff-design-lead`, `evidence-scout` y `design-critic` como en una iniciativa "
        "material, con una sola ronda de crítica. Abrí el expediente en `design/initiatives/`, registrá las "
        "acciones durante el trabajo, tomá una postura provisional y corré el validador con `--ready` "
        "(o `--provisional` si la construcción queda bloqueada por una definición externa). Para un rediseño o "
        "flujo nuevo, escribí un caso de estudio narrativo y comprobalo además con `--case-study`. "
        "La salida de esta prueba no se promueve a conocimiento estable ni se publica.\n"
        + source_boundary_note,
        encoding="utf-8",
    )
    print(output)
    print("Fixture creado sin reviewer.md ni documentos de proyectos reales.")
    print(f'Abrilo con: claude --plugin-dir "{PLUGIN}" ...')
    return 0


if __name__ == "__main__":
    sys.exit(main())
