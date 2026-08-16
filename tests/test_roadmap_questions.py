import json
import subprocess
import sys
import tempfile
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
BOOTSTRAP = ROOT / "bootstrap.py"


class RoadmapQuestionTests(unittest.TestCase):
    def run_bootstrap(self, *args, check=True):
        return subprocess.run(
            [sys.executable, str(BOOTSTRAP), *args],
            check=check,
            capture_output=True,
            text=True,
        )

    def test_unknown_php_runtime_blocks_implementation_and_roadmap(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            (target / "composer.json").write_text('{"require":{"psr/log":"^1.0"}}', encoding="utf-8")
            result = json.loads(self.run_bootstrap(
                "onboard", str(target), "--intent", "Add a new module"
            ).stdout)
            self.assertFalse(result["ready_for_implementation"])
            self.assertGreaterEqual(result["blocking_questions"], 1)
            questions = json.loads((target / ".ai" / "questions" / "blocking.json").read_text(encoding="utf-8"))
            by_id = {item["id"]: item for item in questions["blocking"]}
            self.assertIn("runtime-php-version", by_id)
            values = {option["value"] for option in by_id["runtime-php-version"]["options"]}
            self.assertIn("5.6", values)
            self.assertIn("7.x", values)
            self.assertIn("8.2+", values)
            roadmap = json.loads((target / ".ai" / "planning" / "roadmap.json").read_text(encoding="utf-8"))
            self.assertEqual(roadmap["readiness"]["state"], "blocked-awaiting-answers")
            self.assertEqual(roadmap["phases"][0]["status"], "planned")
            self.assertEqual(roadmap["phases"][1]["status"], "blocked")
            self.assertTrue((target / "docs" / "ROADMAP.md").exists())

    def test_opencart_known_version_php_constraint_and_tpl_are_ready(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            (target / "catalog" / "controller").mkdir(parents=True)
            (target / "admin" / "controller").mkdir(parents=True)
            (target / "system").mkdir()
            (target / "catalog" / "view" / "theme" / "default" / "template").mkdir(parents=True)
            (target / "index.php").write_text("<?php define('VERSION', '2.3.0.2');", encoding="utf-8")
            (target / "composer.json").write_text('{"require":{"php":">=5.6"}}', encoding="utf-8")
            (target / "catalog" / "controller" / "a.php").write_text("<?php", encoding="utf-8")
            (target / "admin" / "controller" / "b.php").write_text("<?php", encoding="utf-8")
            (target / "system" / "c.php").write_text("<?php", encoding="utf-8")
            (target / "catalog" / "view" / "theme" / "default" / "template" / "module.tpl").write_text("hello", encoding="utf-8")
            result = json.loads(self.run_bootstrap(
                "onboard", str(target), "--intent", "Add a module"
            ).stdout)
            self.assertTrue(result["ready_for_implementation"])
            self.assertEqual(result["blocking_questions"], 0)
            questions = json.loads((target / ".ai" / "questions" / "blocking.json").read_text(encoding="utf-8"))
            advisory_ids = {item["id"] for item in questions["advisory"]}
            self.assertIn("template-engine-detected", advisory_ids)

    def test_opencart_unknown_template_engine_offers_tpl_twig_options(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            (target / "catalog" / "controller").mkdir(parents=True)
            (target / "admin" / "controller").mkdir(parents=True)
            (target / "system").mkdir()
            (target / "composer.json").write_text('{"require":{"php":">=5.6"}}', encoding="utf-8")
            (target / "catalog" / "controller" / "a.php").write_text("<?php", encoding="utf-8")
            (target / "admin" / "controller" / "b.php").write_text("<?php", encoding="utf-8")
            (target / "system" / "c.php").write_text("<?php", encoding="utf-8")
            self.run_bootstrap("onboard", str(target), "--intent", "Add a module")
            questions = json.loads((target / ".ai" / "questions" / "blocking.json").read_text(encoding="utf-8"))
            by_id = {item["id"]: item for item in questions["blocking"]}
            self.assertIn("framework-opencart-version", by_id)
            self.assertIn("template-engine", by_id)
            template_values = {option["value"] for option in by_id["template-engine"]["options"]}
            self.assertTrue({"tpl", "twig", "mixed"}.issubset(template_values))

    def test_answer_command_persists_fact_and_regenerates_readiness(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            (target / "composer.json").write_text('{"require":{"psr/log":"^1.0"}}', encoding="utf-8")
            first = json.loads(self.run_bootstrap("onboard", str(target), "--intent", "Prepare module").stdout)
            self.assertFalse(first["ready_for_implementation"])
            answered = json.loads(self.run_bootstrap(
                "answer", str(target), "runtime-php-version", "5.6", "--source", "user confirmed PHP 5.6"
            ).stdout)
            self.assertTrue(answered["ready_for_implementation"])
            memory = json.loads((target / ".ai" / "memory" / "project-memory.json").read_text(encoding="utf-8"))
            self.assertEqual(memory["facts"]["runtime.php"]["value"], "5.6")
            self.assertEqual(memory["facts"]["runtime.php"]["source"]["type"], "manual")
            roadmap = json.loads((target / ".ai" / "planning" / "roadmap.json").read_text(encoding="utf-8"))
            self.assertTrue(roadmap["readiness"]["ready_for_implementation"])

    def test_roadmap_has_full_execution_phases_and_definition_of_done(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            result = json.loads(self.run_bootstrap(
                "onboard", str(target), "--intent", "Build a generic application"
            ).stdout)
            self.assertTrue(result["ready_for_implementation"])
            roadmap = json.loads((target / ".ai" / "planning" / "roadmap.json").read_text(encoding="utf-8"))
            self.assertEqual(len(roadmap["phases"]), 9)
            self.assertGreaterEqual(len(roadmap["definition_of_done"]), 5)
            phase_ids = {phase["id"] for phase in roadmap["phases"]}
            self.assertTrue({"phase-0", "phase-4", "phase-7", "phase-8"}.issubset(phase_ids))
            human = (target / "docs" / "ROADMAP.md").read_text(encoding="utf-8")
            self.assertIn("## Phase 0", human)
            self.assertIn("## Definition of done", human)


if __name__ == "__main__":
    unittest.main()
