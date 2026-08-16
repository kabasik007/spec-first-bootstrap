import json
import tempfile
import unittest
from pathlib import Path

from engine.baseline import compare
from engine.harness import (
    add_memory_target,
    build_context,
    check_policy_target,
    init_target,
    verify_target,
)
from engine.memory import update_from_discovery


ROOT = Path(__file__).resolve().parents[1]


class ContextIntelligenceTests(unittest.TestCase):
    def test_generic_php_is_not_opencart_and_loads_real_pack(self):
        with tempfile.TemporaryDirectory() as td:
            target = Path(td)
            (target / "composer.json").write_text(
                json.dumps({"require": {"php": ">=5.6 <8.0", "psr/log": "^1.0"}}),
                encoding="utf-8",
            )
            for i in range(3):
                (target / f"file{i}.php").write_text("<?php echo 1;", encoding="utf-8")
            ctx = build_context(target, ROOT)
            self.assertIn("php", ctx["facts"]["languages"])
            self.assertNotIn("opencart", ctx["facts"]["frameworks"])
            loaded = {p["id"]: p for p in ctx["packs"]["loaded"]}
            self.assertFalse(loaded["languages/php"]["virtual"])
            self.assertIn("runtime-compatibility", ctx["knowledge"]["selected_ids"])

    def test_dependency_graph_composes_ecosystems(self):
        with tempfile.TemporaryDirectory() as td:
            target = Path(td)
            (target / "composer.json").write_text(
                json.dumps({"require": {"php": "^8.1", "guzzlehttp/guzzle": "^7"}}),
                encoding="utf-8",
            )
            (target / "package.json").write_text(
                json.dumps({"dependencies": {"react": "^18"}, "devDependencies": {"vite": "^5"}}),
                encoding="utf-8",
            )
            ctx = build_context(target, ROOT)
            names = {n["id"] for n in ctx["dependencies"]["nodes"]}
            self.assertIn("composer:guzzlehttp/guzzle", names)
            self.assertIn("npm:react", names)
            self.assertIn("npm:vite", names)

    def test_opencart_policy_requires_confirmation_and_denies_secret_read(self):
        with tempfile.TemporaryDirectory() as td:
            target = Path(td)
            for d in ["catalog/controller", "admin/controller", "system"]:
                (target / d).mkdir(parents=True)
            (target / "index.php").write_text("<?php define('VERSION', '2.3.0.2');", encoding="utf-8")
            (target / "composer.json").write_text(json.dumps({"require": {"php": ">=5.6"}}), encoding="utf-8")
            init_target(target, ROOT)
            self.assertEqual(check_policy_target(target, "write", "system/library/foo.php")["decision"], "confirm")
            self.assertEqual(check_policy_target(target, "read", ".env.production")["decision"], "deny")
            self.assertEqual(check_policy_target(target, "write", "extension/custom.php")["decision"], "allow")

    def test_baseline_diff_marks_modified_added_missing(self):
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            target, reference = Path(a), Path(b)
            (reference / "same.txt").write_text("same")
            (target / "same.txt").write_text("same")
            (reference / "changed.txt").write_text("old")
            (target / "changed.txt").write_text("new")
            (reference / "missing.txt").write_text("old")
            (target / "added.txt").write_text("new")
            report = compare(target, reference, [])
            by_path = {x["path"]: x["status"] for x in report["changes"]}
            self.assertEqual(by_path["changed.txt"], "modified")
            self.assertEqual(by_path["missing.txt"], "missing")
            self.assertEqual(by_path["added.txt"], "added")

    def test_manual_memory_survives_discovery_refresh(self):
        with tempfile.TemporaryDirectory() as td:
            target = Path(td)
            (target / "package.json").write_text(json.dumps({"engines": {"node": ">=18"}}), encoding="utf-8")
            init_target(target, ROOT)
            add_memory_target(target, "runtime.production_node", "18.20.4", "production shell", 1.0)
            memory_path = target / ".ai/memory/project-memory.json"
            first = json.loads(memory_path.read_text())
            ctx = build_context(target, ROOT)
            update_from_discovery(memory_path, ctx["facts"], ctx["packs"])
            second = json.loads(memory_path.read_text())
            self.assertEqual(second["facts"]["runtime.production_node"]["value"], "18.20.4")
            self.assertEqual(second["facts"]["runtime.production_node"]["source"]["type"], "manual")
            self.assertEqual(
                first["facts"]["runtime.production_node"]["observed_at"],
                second["facts"]["runtime.production_node"]["observed_at"],
            )

    def test_init_generates_v11_context_and_verify_passes(self):
        with tempfile.TemporaryDirectory() as td:
            target = Path(td)
            (target / "requirements.txt").write_text("fastapi==0.116.0\nuvicorn>=0.30\n")
            (target / "main.py").write_text("from fastapi import FastAPI\napp = FastAPI()\n")
            result = init_target(target, ROOT)
            self.assertEqual(result["bootstrap_version"], "1.1.0")
            for path in [
                ".ai/policy.json",
                ".ai/discovery/dependency-graph.json",
                ".ai/discovery/packs.json",
                ".ai/baseline/inventory.json",
                ".ai/knowledge/index.json",
                ".ai/memory/project-memory.json",
                ".ai/DEPENDENCIES.md",
                ".ai/VERIFICATION.md",
            ]:
                self.assertTrue((target / path).exists(), path)
            code, verification = verify_target(target, ROOT)
            self.assertEqual(code, 0)
            self.assertTrue(verification["ok"])


if __name__ == "__main__":
    unittest.main()
