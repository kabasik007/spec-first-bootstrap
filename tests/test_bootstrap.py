import json
import subprocess
import sys
import tempfile
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
BOOTSTRAP = ROOT / "bootstrap.py"

class BootstrapTests(unittest.TestCase):
    def run_bootstrap(self, *args):
        return subprocess.run([sys.executable, str(BOOTSTRAP), *args], check=True, capture_output=True, text=True)

    def test_detects_generic_php_without_forcing_framework(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "composer.json").write_text('{"require":{"php":">=5.6 <8.4"}}', encoding="utf-8")
            for i in range(3):
                (root / f"file{i}.php").write_text("<?php echo 'ok';", encoding="utf-8")
            out = json.loads(self.run_bootstrap("detect", str(root)).stdout)
            self.assertIn("php", out["languages"])
            self.assertEqual(out["versions"]["php_constraint"]["value"], ">=5.6 <8.4")
            self.assertNotIn("opencart", out["frameworks"])

    def test_detects_opencart_as_composable_framework(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "catalog" / "controller").mkdir(parents=True)
            (root / "admin" / "controller").mkdir(parents=True)
            (root / "system").mkdir()
            for p in [root / "catalog" / "controller" / "a.php", root / "admin" / "controller" / "b.php", root / "system" / "c.php"]:
                p.write_text("<?php", encoding="utf-8")
            out = json.loads(self.run_bootstrap("detect", str(root)).stdout)
            self.assertIn("opencart", out["frameworks"])
            self.assertIn("frameworks/opencart", out["selected_packs"])
            self.assertIn("project-types/extension-platform", out["selected_packs"])

    def test_init_generates_harness_and_verify_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "package.json").write_text('{"scripts":{"test":"node test.js","build":"node build.js"},"dependencies":{"react":"latest"}}', encoding="utf-8")
            self.run_bootstrap("init", str(root))
            self.assertTrue((root / ".ai" / "manifest.yaml").exists())
            self.assertTrue((root / ".ai" / "discovery" / "project-facts.json").exists())
            verify = json.loads(self.run_bootstrap("verify", str(root)).stdout)
            self.assertTrue(verify["ok"])

if __name__ == "__main__":
    unittest.main()
