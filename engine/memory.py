from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Dict

from .utils import read_json, write_json


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def update_from_discovery(memory_path: Path, facts: dict, pack_context: dict) -> dict:
    memory = read_json(memory_path, {"schema_version": 1, "facts": {}})
    memory.setdefault("schema_version", 1)
    memory.setdefault("facts", {})
    observed = _discovery_facts(facts, pack_context)
    timestamp = now_iso()
    for key, item in observed.items():
        previous = memory["facts"].get(key)
        if previous and previous.get("source", {}).get("type") == "manual":
            continue
        memory["facts"][key] = {
            **item,
            "observed_at": previous.get("observed_at") if previous else timestamp,
            "last_seen": timestamp,
        }
    memory["updated_at"] = timestamp
    write_json(memory_path, memory)
    return memory


def add_manual(memory_path: Path, key: str, value: str, source: str, confidence: float = 1.0) -> dict:
    memory = read_json(memory_path, {"schema_version": 1, "facts": {}})
    memory.setdefault("facts", {})
    timestamp = now_iso()
    memory["facts"][key] = {
        "value": value,
        "confidence": float(confidence),
        "source": {"type": "manual", "reference": source},
        "observed_at": timestamp,
        "last_seen": timestamp,
    }
    memory["updated_at"] = timestamp
    write_json(memory_path, memory)
    return memory["facts"][key]


def _discovery_facts(facts: dict, pack_context: dict) -> Dict[str, dict]:
    out: Dict[str, dict] = {}
    for group in ["languages", "frameworks", "versions"]:
        for name, fact in facts.get(group, {}).items():
            out[f"{group}.{name}"] = {
                "value": fact.get("value"),
                "confidence": fact.get("confidence", 0.5),
                "source": {
                    "type": "discovery",
                    "evidence": fact.get("evidence", []),
                },
            }
    out["project.types"] = {
        "value": facts.get("project_types", []),
        "confidence": 0.9,
        "source": {"type": "discovery", "evidence": ["project structure"]},
    }
    out["bootstrap.packs"] = {
        "value": pack_context.get("resolved_ids", []),
        "confidence": 1.0,
        "source": {"type": "bootstrap", "evidence": ["pack resolver"]},
    }
    return out
