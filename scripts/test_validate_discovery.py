"""Scenario tests for the discovery gate «listo para diseñar»."""

from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

import validate_discovery as vd


STAMP = "2026-10-27T12:00:00-03:00"
FILLED = "# Etapa\n\nContenido completo.\n"
SKIP = "# Etapa\n\n**Etapa salteada:** sin acceso a usuarios. Consecuencia: lo de usuarios es hipótesis.\n"


def event(actor: str, kind: str, refs: list[str], **extra: str) -> dict:
    return {"timestamp": STAMP, "actor": actor, "type": kind, "summary": "s", "refs": refs, **extra}


class DiscoveryGateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.dossier = Path(self.tmp.name) / "disc"
        (self.dossier / "reviews").mkdir(parents=True)
        for name in vd.STAGES:
            self.write(name, FILLED)
        self.write("02-campo.md", "# Campo\n\n| ID | Perfil |\n| --- | --- |\n| P1 | Recepción |\n")
        self.write("critiques.md", "| ID | Nivel | Respuesta | Motivo |\n| --- | --- | --- | --- |\n| C1 | Corregir | aplicado | ok |\n")
        self.validation = "realizada"
        self.write_brief()
        self.write("reviews/critic-v1.md", "Resultado: hallazgos\n")
        self.events = [
            event("discovery-lead", "research", ["01-plan-de-research.md"]),
            event("design-critic", "validation", ["reviews/critic-v1.md"], outcome="findings"),
            event("discovery-lead", "decision", ["10-design-brief.md"], outcome=vd.READY_OUTCOME),
        ]
        self.write_events()

    def write(self, name: str, content: str) -> None:
        (self.dossier / name).write_text(content, encoding="utf-8")

    def write_brief(self) -> None:
        self.write(vd.BRIEF, (
            f"# Design brief\n\n**Validación con usuarios:** {self.validation}\n\n"
            "## Estado de la evidencia\n\n| Supuesto | Etiqueta | Prueba | Responsable |\n"
            "| --- | --- | --- | --- |\n| Pagan en el acto | hipótesis | 5 entrevistas | PM |\n\n"
            "## Riesgos y preguntas abiertas\n\nNinguno.\n"))

    def write_events(self) -> None:
        self.write("events.jsonl", "".join(json.dumps(e, ensure_ascii=False) + "\n" for e in self.events))

    def errors(self, ready: bool = True) -> list[str]:
        return vd.validate(self.dossier, ready=ready)[0]

    def test_complete_discovery_is_ready(self) -> None:
        self.assertEqual(self.errors(), [])

    def test_template_structure_passes_without_ready(self) -> None:
        self.write("03-sintesis.md", "# Síntesis\n\n_Pendiente._\n")
        self.assertEqual(self.errors(ready=False), [])
        self.assertTrue(any("03-sintesis.md" in e for e in self.errors()))

    def test_skipped_stage_is_accepted_when_declared(self) -> None:
        self.write("04-benchmark.md", SKIP + "\n_Pendiente._\n")
        self.assertEqual(self.errors(), [])

    def test_encuadre_cannot_be_skipped(self) -> None:
        self.write("00-encuadre.md", SKIP)
        self.assertTrue(any("no se puede saltear" in e for e in self.errors()))

    def test_no_field_work_forces_pending_validation(self) -> None:
        self.write("02-campo.md", SKIP)
        self.assertTrue(any("debe decir" in e for e in self.errors()))
        self.validation = "pendiente"
        self.write_brief()
        self.assertEqual(self.errors(), [])

    def test_no_test_cannot_claim_validated(self) -> None:
        self.write("09-baja-fidelidad.md", SKIP)
        self.assertTrue(any("no puede decir" in e for e in self.errors()))

    def test_field_stage_needs_a_session(self) -> None:
        self.write("02-campo.md", "# Campo\n\n| ID | Perfil |\n| --- | --- |\n")
        self.assertTrue(any("ninguna sesión" in e for e in self.errors()))

    def test_open_fix_blocks(self) -> None:
        self.write("critiques.md", "| ID | Nivel | Respuesta | Motivo |\n| --- | --- | --- | --- |\n| C1 | Corregir | abierto | falta |\n")
        self.assertTrue(any("Corregir" in e for e in self.errors()))

    def test_missing_critic_review_and_decision_block(self) -> None:
        self.events = self.events[:1]
        self.write_events()
        errors = self.errors()
        self.assertTrue(any("design-critic" in e for e in errors))
        self.assertTrue(any(vd.READY_OUTCOME in e for e in errors))

    def test_brief_needs_evidence_table(self) -> None:
        self.write(vd.BRIEF, "# Design brief\n\n**Validación con usuarios:** realizada\n\n## Estado de la evidencia\n\nNada.\n")
        self.assertTrue(any("Estado de la evidencia" in e for e in self.errors()))

    def test_skills_read_section_blocks_while_pending(self) -> None:
        template = (Path(vd.__file__).resolve().parents[1] / "templates" / "discovery" / "00-encuadre.md").read_text(encoding="utf-8")
        self.assertIn("## Skills y guías leídas", template)
        filled = template.replace("{{TITLE}}", "T").replace("{{SLUG}}", "s").replace("{{DATE}}", "2026-11-11")
        self.write("00-encuadre.md", filled)
        self.assertTrue(any("00-encuadre.md" in e and "pendientes" in e for e in self.errors()))


if __name__ == "__main__":
    unittest.main()
