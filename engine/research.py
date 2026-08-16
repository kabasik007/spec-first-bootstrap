from __future__ import annotations


def build_agenda(facts: dict, architecture: dict, intent: str = "") -> dict:
    items = []
    frameworks = list(facts.get("frameworks", {}).keys())
    versions = facts.get("versions", {})

    for framework in frameworks:
        version_fact = versions.get(framework)
        if version_fact:
            version = version_fact.get("value")
            items.append({
                "id": "framework-{}-architecture".format(framework),
                "priority": "high",
                "question": "Confirm architecture, extension points and compatibility rules for {} {}.".format(framework, version),
                "source_policy": "official-primary-only",
                "status": "needed-if-changing-framework-boundaries",
            })
        else:
            items.append({
                "id": "framework-{}-version".format(framework),
                "priority": "high",
                "question": "Determine the exact {} version/generation from repository evidence before applying version-specific conventions.".format(framework),
                "source_policy": "repository-evidence-first-then-official-primary",
                "status": "unresolved",
            })

    if architecture.get("microservices", {}).get("decision") != "preserve-existing":
        items.append({
            "id": "architecture-service-boundary",
            "priority": "medium",
            "question": "Do not introduce microservices unless independent deployment, scaling, fault isolation, data ownership or team ownership is demonstrated.",
            "source_policy": "project-evidence-first",
            "status": "gate",
        })

    if intent.strip():
        items.append({
            "id": "intent-fit",
            "priority": "medium",
            "question": "Validate that the proposed architecture fits the user intent without inventing product-specific requirements: {}".format(intent.strip()),
            "source_policy": "user-intent-plus-project-evidence",
            "status": "required",
        })

    return {
        "schema_version": 1,
        "web_policy": {
            "use_web_when": [
                "framework/version behavior is uncertain",
                "official architecture or extension conventions materially affect the design",
                "a current standard/tool capability could have changed",
            ],
            "sources": "Prefer official documentation, official repositories and primary technical sources.",
            "record": "Store findings with source, version/date, claim and affected architecture decision.",
            "offline": "If web access is unavailable, leave the item unresolved rather than guessing.",
        },
        "items": items,
    }


def render_research_summary(agenda: dict) -> str:
    items = agenda.get("items", [])
    if not items:
        return "No external architecture research is currently required."
    lines = []
    for item in items:
        lines.append("- `{}` [{}] {}".format(item.get("id"), item.get("status"), item.get("question")))
    return "\n".join(lines)
