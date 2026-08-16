from __future__ import annotations

from pathlib import Path
from typing import List

from .utils import looks_secret_path, rel, sha256_file, walk_files


GENERATED_PREFIXES = (
    "vendor/", "node_modules/", "dist/", "build/", ".next/", "coverage/",
)


def classify_path(path: str, protected_paths: List[str]) -> str:
    normalized = path.lstrip("./")
    if any(normalized == p.rstrip("/") or normalized.startswith(p.rstrip("/") + "/") for p in protected_paths):
        return "protected"
    if any(normalized.startswith(prefix) for prefix in GENERATED_PREFIXES):
        return "generated-or-vendor"
    return "project"


def inventory(root: Path, protected_paths: List[str]) -> dict:
    items = []
    skipped_sensitive = []
    for path in walk_files(root):
        r = rel(root, path)
        if looks_secret_path(r):
            skipped_sensitive.append(r)
            continue
        try:
            stat = path.stat()
            digest = sha256_file(path)
        except Exception:
            continue
        items.append({
            "path": r,
            "sha256": digest,
            "size": stat.st_size,
            "classification": classify_path(r, protected_paths),
        })
    return {
        "schema_version": 1,
        "root": str(root.resolve()),
        "files": sorted(items, key=lambda x: x["path"]),
        "summary": {
            "files": len(items),
            "protected": sum(1 for x in items if x["classification"] == "protected"),
            "project": sum(1 for x in items if x["classification"] == "project"),
            "skipped_sensitive": len(skipped_sensitive),
        },
        "sensitive_paths_skipped": sorted(skipped_sensitive),
    }


def compare(target_root: Path, reference_root: Path, protected_paths: List[str]) -> dict:
    target = inventory(target_root, protected_paths)
    reference = inventory(reference_root, protected_paths)
    t = {x["path"]: x for x in target["files"]}
    r = {x["path"]: x for x in reference["files"]}
    changes = []
    for path in sorted(set(t) | set(r)):
        if path not in r:
            status = "added"
        elif path not in t:
            status = "missing"
        elif t[path]["sha256"] != r[path]["sha256"]:
            status = "modified"
        else:
            status = "same"
        if status == "same":
            continue
        item = {
            "path": path,
            "status": status,
            "classification": (t.get(path) or r.get(path) or {}).get("classification", "project"),
        }
        if path in t:
            item["target_sha256"] = t[path]["sha256"]
        if path in r:
            item["reference_sha256"] = r[path]["sha256"]
        changes.append(item)
    return {
        "schema_version": 1,
        "target": str(target_root.resolve()),
        "reference": str(reference_root.resolve()),
        "changes": changes,
        "summary": {
            "added": sum(1 for x in changes if x["status"] == "added"),
            "missing": sum(1 for x in changes if x["status"] == "missing"),
            "modified": sum(1 for x in changes if x["status"] == "modified"),
            "protected_changes": sum(1 for x in changes if x["classification"] == "protected"),
        },
    }


def render_baseline_md(report: dict) -> str:
    if "reference" not in report:
        summary = report["summary"]
        return (
            "# Baseline Inventory\n\n"
            "No external reference baseline is configured. This inventory classifies the current repository and records hashes without reading secret-like files into AI context.\n\n"
            f"- Files inventoried: {summary['files']}\n"
            f"- Protected files: {summary['protected']}\n"
            f"- Sensitive paths skipped: {summary['skipped_sensitive']}\n"
        )
    s = report["summary"]
    return (
        "# Baseline Diff\n\n"
        f"Reference: `{report['reference']}`\n\n"
        f"- Added: {s['added']}\n"
        f"- Missing: {s['missing']}\n"
        f"- Modified: {s['modified']}\n"
        f"- Changes in protected paths: {s['protected_changes']}\n\n"
        "A baseline diff is evidence. Review platform/version compatibility before treating the reference as authoritative.\n"
    )
