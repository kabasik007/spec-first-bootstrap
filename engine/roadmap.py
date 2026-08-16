from __future__ import annotations

from typing import List

from .questions import render_blocking_questions


def build_roadmap(context: dict) -> dict:
    facts = context["facts"]
    architecture = context["architecture"]
    questions = context["questions"]
    packs = context["packs"]
    intent = architecture.get("intent", "").strip()
    project_types = set(facts.get("project_types", []))
    extension = "extension-platform" in project_types
    blocked = bool(questions.get("blocking"))

    phases: List[dict] = []

    def add(phase_id: str, title: str, objective: str, deliverables: List[str], gates: List[str], depends_on: List[str]):
        phases.append({
            "id": phase_id,
            "title": title,
            "objective": objective,
            "status": "blocked" if blocked and phase_id not in {"phase-0"} else "planned",
            "depends_on": depends_on,
            "deliverables": deliverables,
            "gates": gates,
        })

    add(
        "phase-0",
        "Resolve compatibility and product blockers",
        "Close only the unknowns that can materially change runtime compatibility, architecture, file formats or public behavior.",
        [
            "Answer every item in `.ai/questions/blocking.json` or resolve it from stronger repository evidence.",
            "Store user-confirmed answers as verified project facts with provenance.",
            "Regenerate bootstrap context and confirm `ready_for_implementation=true`.",
        ],
        [
            "No unresolved global compatibility blocker remains.",
            "No required framework generation is being guessed.",
            "No presentation format is selected against contradictory repository evidence.",
        ],
        [],
    )

    add(
        "phase-1",
        "Confirm repository truth and architecture",
        "Establish the current system shape before designing the requested change.",
        [
            "Review detected runtime/framework/version facts and confidence.",
            "Review workspace/component and dependency boundaries.",
            "Review protected/core/vendor/generated zones and baseline evidence.",
            "Confirm the architecture style in `docs/ARCHITECTURE.md`.",
            "Record material unknowns in the research agenda instead of guessing.",
        ],
        [
            "Brownfield boundaries are preserved unless migration is explicitly justified.",
            "Core remains small; feature responsibilities have explicit module ownership.",
            "No new microservice boundary exists without deployment/scale/fault/data/team evidence.",
        ],
        ["phase-0"],
    )

    add(
        "phase-2",
        "Define the product/change contract",
        "Turn the user intent into an explicit observable contract without inventing requirements.",
        [
            "Create or update the relevant `docs/specs/` feature contract for non-trivial observable behavior.",
            "Define scope, non-goals, invariants, failure policy and compatibility expectations.",
            "Map user-visible/API/data behavior to verification evidence.",
            "Create a change design/ADR only when the change is architectural or high risk.",
        ],
        [
            "The requested behavior is explicit enough to implement without product guessing.",
            "Architecture details are not mixed into the product spec unnecessarily.",
            "Breaking changes, migrations and rollback needs are identified before implementation.",
        ],
        ["phase-1"],
    )

    foundation = [
        "Use existing project-native structure when brownfield.",
        "For greenfield, establish only the minimum core/contracts needed by the first feature modules.",
        "Define narrow module interfaces before cross-module calls.",
        "Keep filesystem/database/network/queue/provider access behind adapters.",
    ]
    if extension:
        foundation += [
            "Confirm host extension points, lifecycle hooks/events and protected core boundaries.",
            "Confirm permissions, language resources and package/install layout before host integration code.",
        ]
    add(
        "phase-3",
        "Prepare implementation boundaries",
        "Create the smallest stable foundation needed for implementation while preserving host/project conventions.",
        foundation,
        [
            "No catch-all God Core/shared/utils area is introduced.",
            "Every new module/block has one clear responsibility and owner.",
            "Infrastructure dependencies point inward through contracts rather than leaking into domain logic.",
        ],
        ["phase-2"],
    )

    module_deliverables = [
        "Implement business/use-case behavior inside explicit feature modules.",
        "Keep controllers/routes/UI/CLI handlers thin and orchestration-focused.",
        "Keep cross-module access behind explicit contracts.",
        "Add focused unit/integration verification for module behavior and failure paths.",
    ]
    if intent:
        module_deliverables.insert(0, "Implement the requested intent: {}".format(intent))
    add(
        "phase-4",
        "Implement feature modules and domain behavior",
        "Deliver the requested capability in coherent modules without unrelated modernization.",
        module_deliverables,
        [
            "Observable behavior matches the active spec.",
            "No unrelated code is reformatted or migrated as collateral work.",
            "Runtime/framework compatibility constraints are respected.",
        ],
        ["phase-3"],
    )

    interface_deliverables = [
        "Connect UI/API/CLI/host adapters to module/application contracts.",
        "Validate authorization/permissions at the appropriate boundary.",
        "Handle external service/provider failures explicitly.",
        "Keep serialization/view/template concerns out of core business logic.",
    ]
    if extension:
        interface_deliverables += [
            "Verify host install/upgrade/uninstall lifecycle when applicable.",
            "Verify admin/back-office and catalog/front-office surfaces separately when both are affected.",
            "Verify translations/language resources and extension packaging layout.",
        ]
    add(
        "phase-5",
        "Integrate interfaces, host lifecycle and external systems",
        "Attach the feature to real entry points without collapsing architectural boundaries.",
        interface_deliverables,
        [
            "Public interfaces have explicit input/output/error behavior.",
            "Host/platform core is not modified unless an explicit approved exception exists.",
            "External IO can be tested or substituted at its adapter boundary.",
        ],
        ["phase-4"],
    )

    add(
        "phase-6",
        "Data, migrations and backward compatibility",
        "Treat persistence changes as an explicit compatibility boundary rather than an incidental implementation detail.",
        [
            "Define ownership for every new table/collection/state contract.",
            "Make migrations forward-safe and document rollback/repair strategy where applicable.",
            "Preserve existing data semantics unless the spec explicitly changes them.",
            "Avoid cross-module direct table access when an owning module contract should be used.",
        ],
        [
            "Schema/data changes have verification evidence.",
            "Failure or partial-upgrade behavior is understood.",
            "Production-destructive operations remain guarded by policy/confirmation.",
        ],
        ["phase-5"],
    )

    verification = list(packs.get("verification", [])) or ["Run project-native focused verification for changed behavior."]
    add(
        "phase-7",
        "Verification and regression",
        "Prove the requested contract across the capabilities actually used by the project.",
        verification + [
            "Run project-native lint/type/test/build commands discovered in `docs/DEVELOPMENT.md`.",
            "Check logs/console/network/CLI output where relevant.",
            "Verify negative/error paths, not only the happy path.",
            "Record unresolved environment-only checks explicitly instead of marking them as passed.",
        ],
        [
            "Changed behavior has reproducible evidence.",
            "No critical compatibility or policy blocker remains.",
            "Regression scope matches the blast radius of the change.",
        ],
        ["phase-6"],
    )

    release_items = [
        "Update `docs/ARCHITECTURE.md` when boundaries changed.",
        "Update `docs/DEVELOPMENT.md` when commands/conventions changed.",
        "Update relevant product specs and change result notes.",
        "Document deployment/package/install steps that are not self-evident.",
        "Preserve verified project facts for the next agent session.",
    ]
    if extension:
        release_items.append("Build/inspect the extension package and verify target host/version compatibility before release.")
    add(
        "phase-8",
        "Documentation, packaging and handoff",
        "Leave the repository understandable and reproducible for the next human or coding agent.",
        release_items,
        [
            "A new session can understand architecture, commands and compatibility without repeating discovery.",
            "No temporary secret/debug artifact is committed.",
            "Definition of done is satisfied or remaining limitations are explicitly documented.",
        ],
        ["phase-7"],
    )

    return {
        "schema_version": 1,
        "title": "Autonomous Development Roadmap",
        "intent": intent,
        "architecture_style": architecture.get("style", {}).get("name"),
        "readiness": {
            "ready_for_implementation": not blocked,
            "blocking_questions": questions.get("blocking_count", 0),
            "state": "blocked-awaiting-answers" if blocked else "ready-to-plan-or-implement",
        },
        "principles": [
            "Discover before asking; ask before guessing.",
            "Batch blocking questions and explain why each answer changes the implementation.",
            "Preserve brownfield architecture unless migration is intentional.",
            "Prefer modular boundaries over premature microservices.",
            "Keep core small; keep business capabilities in explicit modules.",
            "Do not mark a phase complete without verification evidence appropriate to its risk.",
        ],
        "phases": phases,
        "definition_of_done": [
            "All blocking compatibility questions are resolved or superseded by stronger repository evidence.",
            "Requested behavior matches an explicit product/change contract.",
            "Architecture remains coherent and documented.",
            "Runtime/framework/host compatibility is verified for affected surfaces.",
            "Relevant automated/manual verification passes with recorded evidence.",
            "Migrations/rollback/packaging/deployment concerns are resolved where applicable.",
            "Human docs and durable project memory are current.",
        ],
    }


def render_roadmap(roadmap: dict, questions: dict) -> str:
    readiness = roadmap.get("readiness", {})
    lines = [
        "# Development Roadmap",
        "",
        "<!-- universal-bootstrap:start -->",
        "## Goal",
        "",
        "- Intent: {}.".format(roadmap.get("intent") or "Repository onboarding only; feature intent not yet supplied"),
        "- Architecture: `{}`.".format(roadmap.get("architecture_style") or "unknown"),
        "- Readiness: `{}`.".format(readiness.get("state")),
        "- Blocking questions: {}.".format(readiness.get("blocking_questions", 0)),
        "",
        "## Blocking questions",
        "",
        render_blocking_questions(questions),
        "",
        "If blockers exist, ask them together before risky implementation. Store confirmed answers as verified project memory and regenerate this roadmap.",
        "",
        "## Execution principles",
        "",
    ]
    lines += ["- " + item for item in roadmap.get("principles", [])]
    lines += [""]

    for phase in roadmap.get("phases", []):
        lines += [
            "## {} — {}".format(phase["id"].replace("phase-", "Phase "), phase["title"]),
            "",
            "- Status: `{}`.".format(phase.get("status")),
            "- Objective: {}".format(phase.get("objective")),
            "- Depends on: {}.".format(", ".join("`{}`".format(x) for x in phase.get("depends_on", [])) or "none"),
            "",
            "### Deliverables",
            "",
        ]
        lines += ["- " + item for item in phase.get("deliverables", [])]
        lines += ["", "### Exit gate", ""]
        lines += ["- " + item for item in phase.get("gates", [])]
        lines += [""]

    lines += ["## Definition of done", ""]
    lines += ["- " + item for item in roadmap.get("definition_of_done", [])]
    lines += ["<!-- universal-bootstrap:end -->", ""]
    return "\n".join(lines)
