import json
import subprocess
import sys
import tempfile
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
BOOTSTRAP = ROOT / "bootstrap.py"


class AutonomousBootstrapTests(unittest.TestCase):
    def run_bootstrap(self, *args, check=True):
        return subprocess.run(
            [sys.executable, str(BOOTSTRAP), *args],
            check=check,
            capture_output=True,
            text=True,
        )

    def test_greenfield_defaults_to_modular_monolith_and_human_docs(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            result = json.loads(self.run_bootstrap(
                "onboard", str(target), "--intent", "Build a new business application"
            ).stdout)
            self.assertEqual(result["architecture_style"], "modular-monolith")
            self.assertTrue((target / "AGENTS.md").exists())
            self.assertTrue((target / "docs" / "ARCHITECTURE.md").exists())
            self.assertTrue((target / "docs" / "DEVELOPMENT.md").exists())
            self.assertTrue((target / "docs" / "specs" / "README.md").exists())
            architecture = json.loads((target / ".ai" / "discovery" / "architecture.json").read_text(encoding="utf-8"))
            self.assertFalse(architecture["microservices"]["default"])
            self.assertEqual(architecture["microservices"]["decision"], "not-recommended-by-default")

    def test_init_is_full_onboarding_by_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            self.run_bootstrap("init", str(target))
            self.assertTrue((target / "AGENTS.md").exists())
            self.assertTrue((target / "docs" / "ARCHITECTURE.md").exists())
            verify = json.loads(self.run_bootstrap("verify", str(target)).stdout)
            self.assertTrue(verify["ok"])

    def test_existing_agents_content_is_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            agents = target / "AGENTS.md"
            agents.write_text("# Team Rules\n\n- KEEP-THIS-MANUAL-RULE\n", encoding="utf-8")
            self.run_bootstrap("onboard", str(target), "--intent", "Prepare repository")
            self.run_bootstrap("onboard", str(target), "--intent", "Prepare repository again")
            content = agents.read_text(encoding="utf-8")
            self.assertIn("KEEP-THIS-MANUAL-RULE", content)
            self.assertEqual(content.count("<!-- universal-bootstrap:start -->"), 1)
            self.assertEqual(content.count("<!-- universal-bootstrap:end -->"), 1)

    def test_opencart_like_host_uses_host_extension_architecture(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            (target / "catalog" / "controller").mkdir(parents=True)
            (target / "admin" / "controller").mkdir(parents=True)
            (target / "system").mkdir()
            for path in [
                target / "catalog" / "controller" / "a.php",
                target / "admin" / "controller" / "b.php",
                target / "system" / "c.php",
            ]:
                path.write_text("<?php", encoding="utf-8")
            result = json.loads(self.run_bootstrap(
                "onboard", str(target), "--intent", "Add a new extension module"
            ).stdout)
            self.assertEqual(result["architecture_style"], "host-extension")
            architecture = json.loads((target / ".ai" / "discovery" / "architecture.json").read_text(encoding="utf-8"))
            self.assertFalse(architecture["microservices"]["default"])
            agenda = json.loads((target / ".ai" / "research" / "agenda.json").read_text(encoding="utf-8"))
            ids = {item["id"] for item in agenda["items"]}
            self.assertIn("framework-opencart-version", ids)

    def test_detect_accepts_intent_without_writing_target(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            result = json.loads(self.run_bootstrap(
                "detect", str(target), "--intent", "Create a reusable library"
            ).stdout)
            self.assertEqual(result["architecture"]["intent"], "Create a reusable library")
            self.assertFalse((target / ".ai").exists())
            self.assertFalse((target / "AGENTS.md").exists())


if __name__ == "__main__":
    unittest.main()
