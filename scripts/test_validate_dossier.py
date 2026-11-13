"""Scenario tests for the dossier closure gates (one review round)."""

from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import validate_dossier


VERSION = "decision v1 · spec v1 · CASO 1"
STAMP = "2026-10-19T12:00:00-03:00"


def event(actor: str, kind: str, summary: str, refs: list[str], **extra: str) -> dict:
    return {"timestamp": STAMP, "actor": actor, "type": kind,
            "summary": summary, "refs": refs, **extra}


class ClosureGateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.project = Path(self.tmp.name)
        self.project_patch = patch.object(validate_dossier, "PROJECT_ROOT", self.project)
        self.project_patch.start()
        self.addCleanup(self.project_patch.stop)
        self.dossier = self.project / "design" / "initiatives" / "fixture"
        (self.dossier / "reviews").mkdir(parents=True)
        case = self.project / "docs" / "briefs" / "CASO_fixture.md"
        case.parent.mkdir(parents=True)
        case.write_text("# Caso de estudio\n\nDecisión provisional y sus límites.\n", encoding="utf-8")
        (self.dossier / "brief.md").write_text(
            "# Brief · Fixture\n\n**Fecha de inicio:** 2026-10-19\n\nProblema sintético.\n", encoding="utf-8")
        for name in ("evidence.md", "exploration.md", "critiques.md"):
            (self.dossier / name).write_text(f"# {name}\n\nContenido del expediente.\n", encoding="utf-8")
        (self.dossier / "artifacts.md").write_text(
            "# Artefactos\n\nCaso: docs/briefs/CASO_fixture.md\n", encoding="utf-8")
        self.decision = (
            "# Decisión · Fixture\n\n**Estado:** provisional\n\n"
            "## Restricciones confirmadas\n\nUna regla absoluta sigue sin comprobarse.\n\n"
            "## Estado de ejecución\n\n"
            "| Trabajo o variante | Estado | Dependencia |\n"
            "| --- | --- | --- |\n"
            "| Diseño A | **Bloqueado** | Falta comprobar la política |\n\n"
            "## Cierre provisional\n\n"
            "**Estado de cierre:** pending_external\n"
            "**Construcción:** bloqueada\n\n"
            "| Dependencia externa | Responsable | Prueba de desbloqueo |\n"
            "| --- | --- | --- |\n"
            "| Política de datos | Privacidad | Respuesta escrita sobre retención |\n"
        )
        self.write_decision()
        self.events = [
            event("staff-design-lead", "research", "Leí el brief", ["brief.md"]),
            event("staff-design-lead", "proposal", "Comparé mecanismos", ["exploration.md"]),
            event("design-critic", "critique", "Critiqué las opciones", ["critiques.md"]),
            event("staff-design-lead", "decision", "Elegí provisionalmente", ["decision.md"]),
            event("staff-design-lead", "revision", "Revisé el caso", ["decision.md"], artifact_version=VERSION),
        ]

    def write_decision(self) -> None:
        (self.dossier / "decision.md").write_text(self.decision, encoding="utf-8")

    def add_review(self, actor: str, outcome: str, name: str, version: str = VERSION) -> None:
        ref = f"reviews/{name}.md"
        (self.dossier / ref).write_text(f"# {actor}\n\nResultado: {outcome}.\n", encoding="utf-8")
        self.events.append(event(actor, "validation", f"Informe {name}", [ref],
                                 outcome=outcome, artifact_version=version))

    def close_provisionally(self, version: str = VERSION) -> None:
        self.events.append(event(
            "staff-design-lead", "decision", "Cierre por política externa",
            ["decision.md", "reviews/critic.md"],
            outcome="pending_external", artifact_version=version))

    def check(self, *, ready: bool = False, provisional: bool = False) -> list[str]:
        (self.dossier / "events.jsonl").write_text(
            "".join(json.dumps(item, ensure_ascii=False) + "\n" for item in self.events),
            encoding="utf-8")
        errors, _ = validate_dossier.validate(
            self.dossier, ready=ready, provisional=provisional, case_study=True)
        return errors

    def test_one_round_with_applied_findings_closes(self) -> None:
        self.add_review("design-critic", "findings", "critic")
        self.assertEqual(self.check(ready=True), [])

    def test_critic_report_is_required_scout_is_optional(self) -> None:
        errors = self.check(ready=True)
        self.assertTrue(any("design-critic" in error for error in errors))
        self.add_review("design-critic", "clear", "critic")
        self.assertEqual(self.check(ready=True), [])

    def test_scout_counts_when_present(self) -> None:
        self.add_review("design-critic", "clear", "critic")
        self.add_review("evidence-scout", "no_clear", "scout")
        self.assertTrue(any("evidence-scout" in error for error in self.check(ready=True)))

    def test_text_only_revision_keeps_review_valid(self) -> None:
        self.add_review("design-critic", "findings", "critic")
        self.events.append(event("staff-design-lead", "revision", "Apliqué los hallazgos de texto",
                                 ["critiques.md"], artifact_version="v1.1", outcome="text_only"))
        self.assertEqual(self.check(ready=True), [])

    def test_visual_dossier_requires_the_three_visual_lenses(self) -> None:
        self.add_review("design-critic", "findings", "critic")
        (self.dossier / "capturas").mkdir()
        (self.dossier / "capturas" / "v1.png").write_bytes(b"x")
        errors = self.check(ready=True)
        self.assertTrue(any("distill" in error for error in errors))
        (self.dossier / "critiques.md").write_text(
            "# critiques" + chr(10) * 2 + "## Pasada visual final" + chr(10) * 2
            + chr(10).join(["| PV1 | critique (A) |", "| PV2 | clarify |", "| PV3 | distill |"]) + chr(10),
            encoding="utf-8")
        self.assertEqual(self.check(ready=True), [])

    def test_material_revision_requires_new_review(self) -> None:
        self.add_review("design-critic", "findings", "critic")
        self.events.append(event("staff-design-lead", "revision", "Cambió el mecanismo",
                                 ["decision.md"], artifact_version="v2"))
        self.assertTrue(any("design-critic" in error for error in self.check(ready=True)))
        self.add_review("design-critic", "clear", "critic-focal", version="v2")
        self.assertEqual(self.check(ready=True), [])

    def test_open_fix_blocks_closure(self) -> None:
        self.add_review("design-critic", "findings", "critic")
        table = "| ID | Nivel | Respuesta | Motivo |\n| --- | --- | --- | --- |\n"
        (self.dossier / "critiques.md").write_text(
            table + "| C1 | Corregir | abierto | Falta el dato |\n", encoding="utf-8")
        self.assertTrue(any("Corregir" in error for error in self.check(ready=True)))
        (self.dossier / "critiques.md").write_text(
            table + "| C1 | Corregir | aplicado | Texto corregido |\n", encoding="utf-8")
        self.assertEqual(self.check(ready=True), [])

    def test_blocked_case_closes_provisionally_not_ready(self) -> None:
        self.add_review("design-critic", "blocked_external", "critic")
        self.close_provisionally()
        self.assertEqual(self.check(provisional=True), [])
        self.assertTrue(self.check(ready=True))

    def test_provisional_rejects_buildable_claim_and_missing_owner(self) -> None:
        self.add_review("design-critic", "blocked_external", "critic")
        self.close_provisionally()
        self.decision = self.decision.replace("**Bloqueado**", "**Construible**")
        self.decision = self.decision.replace("| Política de datos | Privacidad |", "| Política de datos | |")
        self.write_decision()
        errors = self.check(provisional=True)
        self.assertTrue(any("construible" in error for error in errors))
        self.assertTrue(any("dependencia externa" in error for error in errors))

    def test_provisional_requires_closure_event_after_review(self) -> None:
        self.add_review("design-critic", "blocked_external", "critic")
        self.assertTrue(any("evento decision" in error for error in self.check(provisional=True)))
        self.close_provisionally(version="otra")
        self.assertTrue(any("evento decision" in error for error in self.check(provisional=True)))

    def test_link_file_is_followed(self) -> None:
        self.add_review("design-critic", "clear", "critic")
        self.check(ready=True)
        link = self.project / "link"
        link.write_text("design/initiatives/fixture", encoding="utf-8")
        errors, count = validate_dossier.validate(link, ready=True, case_study=True)
        self.assertEqual(errors, [])
        self.assertGreater(count, 0)

class SkillsReadTemplateTests(unittest.TestCase):
    def test_exploration_template_requires_skills_table(self) -> None:
        template = (Path(validate_dossier.__file__).resolve().parents[1] / "templates" / "initiative" / "exploration.md").read_text(encoding="utf-8")
        self.assertIn("## Skills y guías leídas", template)
        self.assertIsNotNone(validate_dossier.UNRESOLVED_TEMPLATE.search(template.split("## Skills y guías leídas", 1)[1]))


if __name__ == "__main__":
    unittest.main()
