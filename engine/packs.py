from __future__ import annotations

from pathlib import Path
from typing import Dict, List

from .utils import read_json


class PackRegistry:
    """Loads composable capability packs and catalog fallbacks."""

    def __init__(self, bootstrap_root: Path):
        self.bootstrap_root = bootstrap_root
        self.packs_root = bootstrap_root / "packs"
        self.catalog = read_json(self.packs_root / "catalog.json", {"packs": []})
        self.catalog_by_id = {
            p["id"]: p for p in self.catalog.get("packs", []) if isinstance(p, dict) and p.get("id")
        }
        self.manifests: Dict[str, dict] = {}
        for path in self.packs_root.rglob("*.json"):
            if path.name == "catalog.json":
                continue
            obj = read_json(path, {})
            if isinstance(obj, dict) and obj.get("id"):
                obj = dict(obj)
                obj["_manifest_path"] = path.relative_to(self.bootstrap_root).as_posix()
                self.manifests[obj["id"]] = obj

    def _virtual(self, pack_id: str) -> dict:
        meta = self.catalog_by_id.get(pack_id, {})
        return {
            "id": pack_id,
            "version": "catalog",
            "kind": meta.get("kind", "unknown"),
            "purpose": meta.get("purpose", ""),
            "extends": [],
            "rules": [],
            "protected_paths": [],
            "verification": [],
            "compatibility": [],
            "knowledge_ids": [],
            "policy": {},
            "_virtual": True,
        }

    def get(self, pack_id: str) -> dict:
        return self.manifests.get(pack_id) or self._virtual(pack_id)

    def resolve(self, selected_ids: List[str]) -> dict:
        ordered: List[dict] = []
        seen = set()

        def visit(pack_id: str):
            if pack_id in seen:
                return
            seen.add(pack_id)
            pack = self.get(pack_id)
            for parent in pack.get("extends", []) or []:
                visit(parent)
            ordered.append(pack)

        for pack_id in selected_ids:
            visit(pack_id)

        rules: List[str] = []
        protected: List[str] = []
        verification: List[str] = []
        compatibility: List[str] = []
        knowledge_ids: List[str] = []
        policies: List[dict] = []
        for pack in ordered:
            rules.extend(pack.get("rules", []) or [])
            protected.extend(pack.get("protected_paths", []) or [])
            verification.extend(pack.get("verification", []) or [])
            compatibility.extend(pack.get("compatibility", []) or [])
            knowledge_ids.extend(pack.get("knowledge_ids", []) or [])
            if pack.get("policy"):
                policies.append({"pack": pack["id"], **pack["policy"]})

        return {
            "resolved_ids": [p["id"] for p in ordered],
            "loaded": [
                {
                    "id": p["id"],
                    "version": p.get("version", "unknown"),
                    "kind": p.get("kind", "unknown"),
                    "manifest": p.get("_manifest_path"),
                    "virtual": bool(p.get("_virtual")),
                }
                for p in ordered
            ],
            "rules": _unique(rules),
            "protected_paths": _unique(protected),
            "verification": _unique(verification),
            "compatibility": _unique(compatibility),
            "knowledge_ids": _unique(knowledge_ids),
            "policies": policies,
        }


def _unique(items: List[str]) -> List[str]:
    return list(dict.fromkeys(x for x in items if x))
