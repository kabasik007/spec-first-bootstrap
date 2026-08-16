from __future__ import annotations

from pathlib import Path

from .utils import read_json


def load_selected(bootstrap_root: Path, knowledge_ids) -> dict:
    catalog_path = bootstrap_root / "knowledge" / "catalog.json"
    catalog = read_json(catalog_path, {"entries": []})
    by_id = {
        item["id"]: item for item in catalog.get("entries", [])
        if isinstance(item, dict) and item.get("id")
    }
    selected = []
    missing = []
    for knowledge_id in dict.fromkeys(knowledge_ids or []):
        item = by_id.get(knowledge_id)
        if item:
            selected.append(item)
        else:
            missing.append(knowledge_id)
    return {
        "schema_version": 1,
        "selected_ids": [x["id"] for x in selected],
        "entries": selected,
        "missing_ids": missing,
        "provenance_rule": "Knowledge entries must retain source/provenance. Project-specific evidence overrides generic bootstrap guidance.",
    }
