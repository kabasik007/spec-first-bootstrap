from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Iterable, List

IGNORE_DIRS = {
    ".git", ".ai", "node_modules", "vendor", ".venv", "venv", "dist", "build",
    "__pycache__", ".idea", ".vscode", ".cache", "coverage", ".next",
}

SECRET_NAMES = {
    ".env", ".env.local", ".env.production", ".env.development",
    "id_rsa", "id_ed25519", "credentials.json", "secrets.json",
}


def walk_files(root: Path, max_files: int = 10000) -> List[Path]:
    out: List[Path] = []
    for base, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS and not d.startswith(".")]
        for name in files:
            out.append(Path(base) / name)
            if len(out) >= max_files:
                return out
    return out


def rel(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def read_text(path: Path, limit: int = 300_000) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")[:limit]
    except Exception:
        return ""


def read_json(path: Path, default=None):
    try:
        return json.loads(read_text(path))
    except Exception:
        return {} if default is None else default


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def find_by_name(files: Iterable[Path], name: str) -> List[Path]:
    return [p for p in files if p.name == name]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def looks_secret_path(path: str) -> bool:
    name = Path(path).name
    lower = path.lower()
    if name in SECRET_NAMES or name.startswith(".env"):
        return True
    return (
        lower.endswith(".pem")
        or lower.endswith(".key")
        or "/secrets/" in f"/{lower}/"
        or "/private/" in f"/{lower}/"
    )
