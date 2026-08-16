from __future__ import annotations

from pathlib import Path
from typing import Dict, Iterable, List, Optional

from .utils import read_json, walk_files


FRAMEWORK_PACKAGES = {
    "laravel": ("composer", "laravel/framework"),
    "symfony": ("composer", "symfony/framework-bundle"),
    "django": ("pypi", "django"),
    "fastapi": ("pypi", "fastapi"),
    "flask": ("pypi", "flask"),
    "react": ("npm", "react"),
    "vue": ("npm", "vue"),
    "nextjs": ("npm", "next"),
    "electron": ("npm", "electron"),
}


def _memory_value(memory: dict, keys: Iterable[str]) -> Optional[str]:
    facts = memory.get("facts", {})
    for key in keys:
        item = facts.get(key)
        if not item:
            continue
        value = item.get("value")
        if value is not None and str(value).strip():
            return str(value).strip()
    return None


def _dependency_constraint(dependencies: dict, ecosystem: str, package: str) -> Optional[str]:
    for node in dependencies.get("nodes", []):
        if node.get("kind") != "dependency":
            continue
        if node.get("ecosystem") == ecosystem and node.get("name", "").lower() == package.lower():
            value = str(node.get("constraint") or "").strip()
            return value or "present"
    return None


def _template_evidence(target: Path) -> dict:
    counts = {"tpl": 0, "twig": 0, "blade": 0, "jinja": 0}
    examples: Dict[str, List[str]] = {key: [] for key in counts}
    for path in walk_files(target, max_files=12000):
        name = path.name.lower()
        kind = None
        if name.endswith(".tpl"):
            kind = "tpl"
        elif name.endswith(".twig"):
            kind = "twig"
        elif name.endswith(".blade.php"):
            kind = "blade"
        elif name.endswith(".jinja") or name.endswith(".jinja2") or name.endswith(".j2"):
            kind = "jinja"
        if not kind:
            continue
        counts[kind] += 1
        if len(examples[kind]) < 3:
            try:
                examples[kind].append(path.relative_to(target).as_posix())
            except ValueError:
                examples[kind].append(str(path))
    active = [key for key, count in counts.items() if count]
    return {"counts": counts, "examples": examples, "active": active}


def _question(
    question_id: str,
    category: str,
    memory_key: str,
    text: str,
    why: str,
    options: List[dict],
    evidence: List[str],
    scope: str = "global",
) -> dict:
    return {
        "id": question_id,
        "category": category,
        "memory_key": memory_key,
        "question": text,
        "why": why,
        "options": options,
        "evidence": evidence,
        "scope": scope,
        "status": "blocking",
    }


def build_questions(
    target: Path,
    facts: dict,
    dependencies: dict,
    architecture: dict,
    memory: dict,
    intent: str = "",
) -> dict:
    blocking: List[dict] = []
    advisory: List[dict] = []
    languages = set(facts.get("languages", {}).keys())
    frameworks = set(facts.get("frameworks", {}).keys())
    versions = facts.get("versions", {})

    # Runtime compatibility questions are blockers only when the repository does not
    # expose a safe compatibility constraint and no verified manual fact exists.
    if "php" in languages and not versions.get("php_constraint") and not _memory_value(
        memory, ["runtime.php", "runtime.production_php", "versions.php_constraint"]
    ):
        blocking.append(_question(
            "runtime-php-version",
            "runtime",
            "runtime.php",
            "Which PHP runtime must this project remain compatible with?",
            "PHP syntax and standard-library availability change materially across 5.x, 7.x and 8.x.",
            [
                {"value": "5.6", "label": "PHP 5.6 / legacy 5.x"},
                {"value": "7.x", "label": "PHP 7.x"},
                {"value": "8.0-8.1", "label": "PHP 8.0-8.1"},
                {"value": "8.2+", "label": "PHP 8.2 or newer"},
                {"value": "other", "label": "Other / specify exact version"},
            ],
            ["PHP source detected", "No Composer/platform PHP constraint found"],
        ))

    if "python" in languages and not versions.get("python_constraint") and not _memory_value(
        memory, ["runtime.python", "runtime.production_python", "versions.python_constraint"]
    ):
        blocking.append(_question(
            "runtime-python-version",
            "runtime",
            "runtime.python",
            "Which Python runtime must this project support?",
            "Typing syntax, standard library features and dependency compatibility depend on the supported Python floor.",
            [
                {"value": "3.8", "label": "Python 3.8 / legacy compatible"},
                {"value": "3.9-3.10", "label": "Python 3.9-3.10"},
                {"value": "3.11-3.12", "label": "Python 3.11-3.12"},
                {"value": "3.13+", "label": "Python 3.13 or newer"},
                {"value": "other", "label": "Other / specify exact version"},
            ],
            ["Python source/package evidence detected", "No requires-python constraint found"],
        ))

    if "node" in languages and not versions.get("node_constraint") and not _memory_value(
        memory, ["runtime.node", "runtime.production_node", "versions.node_constraint"]
    ):
        blocking.append(_question(
            "runtime-node-version",
            "runtime",
            "runtime.node",
            "Which Node.js runtime must this project support?",
            "Available JavaScript APIs, package compatibility and build tooling depend on the Node runtime.",
            [
                {"value": "16-or-older", "label": "Node 16 or older legacy runtime"},
                {"value": "18", "label": "Node 18"},
                {"value": "20", "label": "Node 20"},
                {"value": "22+", "label": "Node 22 or newer"},
                {"value": "other", "label": "Other / specify exact version"},
            ],
            ["Node/JavaScript/TypeScript evidence detected", "No package.json engines.node constraint found"],
        ))

    # Host/framework versions matter most when extension APIs or project layout vary by generation.
    for framework in sorted(frameworks):
        known = versions.get(framework)
        manual = _memory_value(memory, ["framework.{}.version".format(framework), "versions.{}".format(framework)])
        package_constraint = None
        if framework in FRAMEWORK_PACKAGES:
            ecosystem, package = FRAMEWORK_PACKAGES[framework]
            package_constraint = _dependency_constraint(dependencies, ecosystem, package)
        if known or manual or package_constraint:
            continue

        if framework == "opencart":
            options = [
                {"value": "2.3.x", "label": "OpenCart 2.3.x"},
                {"value": "3.x", "label": "OpenCart 3.x"},
                {"value": "4.x", "label": "OpenCart 4.x"},
                {"value": "other", "label": "Other / specify exact version"},
            ]
        elif framework == "prestashop":
            options = [
                {"value": "1.6", "label": "PrestaShop 1.6"},
                {"value": "1.7", "label": "PrestaShop 1.7"},
                {"value": "8.x", "label": "PrestaShop 8.x"},
                {"value": "9.x-or-newer", "label": "PrestaShop 9.x or newer"},
                {"value": "other", "label": "Other / specify exact version"},
            ]
        elif framework == "wordpress":
            options = [
                {"value": "legacy", "label": "Legacy WordPress generation / specify version"},
                {"value": "current-project", "label": "Use the exact installed version from deployment"},
                {"value": "other", "label": "Other / specify exact version"},
            ]
        else:
            options = [{"value": "exact", "label": "Specify the exact/major framework version"}]

        blocking.append(_question(
            "framework-{}-version".format(framework),
            "framework",
            "framework.{}.version".format(framework),
            "Which {} version/generation is the target?".format(framework),
            "Framework extension points, layouts and compatibility rules can change between generations.",
            options,
            ["{} detected".format(framework), "No reliable version evidence found in repository manifests/files"],
        ))

    template = _template_evidence(target)
    platform_template_frameworks = frameworks.intersection({"opencart", "prestashop"})
    template_manual = _memory_value(memory, ["templates.engine", "view.template_engine"])
    if platform_template_frameworks and not template_manual:
        active = template.get("active", [])
        if len(active) == 0:
            options = [
                {"value": "tpl", "label": "TPL / .tpl templates"},
                {"value": "twig", "label": "Twig / .twig templates"},
                {"value": "mixed", "label": "Mixed/custom template layers"},
                {"value": "none", "label": "No template/UI work is required"},
            ]
            blocking.append(_question(
                "template-engine",
                "presentation",
                "templates.engine",
                "Which template/view engine applies to the part we will change?",
                "Generating the wrong view format can make an otherwise correct module incompatible with the host/theme generation.",
                options,
                ["Host extension platform detected", "No .tpl/.twig template evidence found"],
                scope="presentation-layer",
            ))
        elif len(active) > 1:
            blocking.append(_question(
                "template-engine",
                "presentation",
                "templates.engine",
                "Multiple template systems are present. Which one applies to the target component?",
                "The repository contains more than one view technology, so file extension alone cannot select the correct presentation boundary.",
                [{"value": item, "label": item.upper()} for item in active] + [
                    {"value": "mixed", "label": "The target intentionally uses more than one"}
                ],
                ["{} files: {}".format(name, template["counts"][name]) for name in active],
                scope="presentation-layer",
            ))
        else:
            advisory.append({
                "id": "template-engine-detected",
                "category": "presentation",
                "status": "resolved-by-evidence",
                "value": active[0],
                "evidence": template["examples"].get(active[0], []),
            })

    # A vague intent is not itself a blocker. Product questions become blockers only
    # when implementation would otherwise invent behavior.
    if not intent.strip():
        advisory.append({
            "id": "product-intent-not-supplied",
            "category": "product",
            "status": "defer-until-feature-work",
            "note": "Repository onboarding can continue, but do not invent feature behavior before the user supplies an actual change intent.",
        })

    status = "blocked" if blocking else "ready"
    return {
        "schema_version": 1,
        "status": status,
        "ready_for_implementation": not blocking,
        "blocking_count": len(blocking),
        "blocking": blocking,
        "advisory": advisory,
        "ask_policy": {
            "discover_first": "Do not ask for facts that repository evidence or verified memory can answer.",
            "batch": "Ask all current blocking questions together in one concise message when practical.",
            "options": "Offer concrete likely options plus an Other/specify option; never force a false choice.",
            "reason": "For each question explain why the answer changes compatibility, architecture or file format.",
            "after_answer": "Store the answer as a verified project fact, regenerate context/roadmap, then continue.",
            "non_blocking": "Do not interrupt implementation for advisory questions that can safely be deferred.",
        },
    }


def render_blocking_questions(questions: dict) -> str:
    items = questions.get("blocking", [])
    if not items:
        return "No blocking setup questions remain."
    lines = []
    for index, item in enumerate(items, 1):
        lines.append("{}. **{}** (`{}`)".format(index, item["question"], item["id"]))
        lines.append("   - Why: {}".format(item["why"]))
        lines.append("   - Evidence: {}".format("; ".join(item.get("evidence", [])) or "none"))
        option_text = "; ".join("{} — {}".format(option["value"], option["label"]) for option in item.get("options", []))
        if option_text:
            lines.append("   - Options: {}".format(option_text))
    return "\n".join(lines)
