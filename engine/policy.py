from __future__ import annotations

import re
from typing import List


DEFAULT_SECRET_PATTERNS = [
    ".env", ".env.*", "*.pem", "*.key", "id_rsa", "id_ed25519",
    "credentials.json", "secrets.json", "**/secrets/**",
]
DEFAULT_DENY_WRITE = [
    ".git/", ".ai/discovery/", ".ai/baseline/reference/",
]
DEFAULT_CONFIRM_COMMANDS = [
    r"\brm\s+-rf\b", r"\bDROP\s+(TABLE|DATABASE)\b", r"\bTRUNCATE\s+TABLE\b",
    r"\bgit\s+reset\s+--hard\b", r"\bgit\s+clean\s+-[a-z]*f",
    r"\b(migrate|migration).*(prod|production)\b",
]


def build_policy(pack_context: dict, facts: dict) -> dict:
    protected = _unique(pack_context.get("protected_paths", []))
    deny_write = list(DEFAULT_DENY_WRITE)
    deny_read = list(DEFAULT_SECRET_PATTERNS)
    confirm_commands = list(DEFAULT_CONFIRM_COMMANDS)
    for policy in pack_context.get("policies", []):
        deny_write.extend(policy.get("deny_write", []) or [])
        deny_read.extend(policy.get("deny_read", []) or [])
        protected.extend(policy.get("confirm_write", []) or [])
        confirm_commands.extend(policy.get("confirm_commands", []) or [])
    return {
        "schema_version": 1,
        "enforcement": "advisory-with-check-command",
        "note": "External agents must call policy-check or implement equivalent host enforcement; this file alone cannot sandbox another process.",
        "deny_read": _unique(deny_read),
        "deny_write": _unique(deny_write),
        "confirm_write": _unique(protected),
        "confirm_commands": _unique(confirm_commands),
        "facts": {
            "project_types": facts.get("project_types", []),
            "frameworks": sorted(facts.get("frameworks", {}).keys()),
        },
    }


def check(policy: dict, action: str, subject: str) -> dict:
    normalized = subject.replace("\\", "/").lstrip("./")
    if action == "read" and _matches_any(normalized, policy.get("deny_read", [])):
        return {"decision": "deny", "reason": "path matches deny_read policy"}
    if action == "write":
        if _matches_any(normalized, policy.get("deny_write", [])):
            return {"decision": "deny", "reason": "path matches deny_write policy"}
        if _matches_any(normalized, policy.get("confirm_write", [])):
            return {"decision": "confirm", "reason": "path is protected and requires explicit approval"}
    if action == "execute":
        for pattern in policy.get("confirm_commands", []):
            try:
                if re.search(pattern, subject, flags=re.I):
                    return {"decision": "confirm", "reason": f"command matches guarded pattern: {pattern}"}
            except re.error:
                if pattern.lower() in subject.lower():
                    return {"decision": "confirm", "reason": f"command matches guarded text: {pattern}"}
    return {"decision": "allow", "reason": "no blocking policy matched"}


def _matches_any(path: str, patterns: List[str]) -> bool:
    for raw in patterns:
        pattern = raw.replace("\\", "/").lstrip("./")
        if pattern.endswith("/"):
            if path.startswith(pattern):
                return True
            continue
        if "**/" in pattern or "*" in pattern:
            regex = re.escape(pattern).replace(r"\*\*", ".*").replace(r"\*", "[^/]*")
            if re.fullmatch(regex, path):
                return True
        elif path == pattern or path.startswith(pattern.rstrip("/") + "/"):
            return True
    return False


def _unique(items):
    return list(dict.fromkeys(x for x in items if x))
