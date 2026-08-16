# AGENTS.md

This file defines workflow rules for agents working in this repository and for agents using the generated bootstrap harness.

It is not the source of truth for detailed product behavior. Product behavior lives in `docs/specs/`. Technical architecture and discovered project constraints live in `.ai/` or project architecture docs.

## Reading order

Before non-trivial implementation work:

1. Read this `AGENTS.md`.
2. Read `docs/architecture.md` when changing the bootstrap itself.
3. For a bootstrapped target, read `.ai/PROJECT.md`, `.ai/ARCHITECTURE.md`, `.ai/RULES.md`, and `.ai/COMMANDS.md`.
4. Read `docs/specs/README.md` and the relevant feature spec when behavior is involved.
5. Read the active `.ai/changes/<id>/` artifacts for architectural or risky work.
6. Only then modify implementation.

## Detect before assuming

For target repositories, do not assume language, framework, version, commands, project type, or extension model when the repository can provide evidence.

Prefer:

```bash
python bootstrap.py detect <target>
python bootstrap.py init <target>
```

Treat generated facts as evidence with confidence, not infallible truth. Verify low-confidence facts before risky changes.

## Universal compatibility rule

The bootstrap runtime is not the target runtime.

- A target may intentionally use legacy PHP, Python, Node, Java, .NET, framework, database, browser, or OS versions.
- Do not introduce syntax or APIs newer than the target supports unless the active change explicitly performs a migration.
- Never normalize a legacy project merely because newer conventions exist.

## Spec-first rule

Before implementing a non-trivial behavior change:

1. Clarify the product goal.
2. Create or update the product spec under `docs/specs/`.
3. Confirm observable behavior, invariants, failure policy, and compatibility constraints.
4. Create technical design separately when the change is architectural.
5. Implement against the contract.
6. Add or update appropriate verification evidence.

## Separation of concerns

- `AGENTS.md` — agent workflow and operating rules
- `docs/specs/` — observable product behavior
- `.ai/PROJECT.md` — detected project facts
- `.ai/ARCHITECTURE.md` — technical boundaries/system shape
- `.ai/RULES.md` — project-specific compatibility and safety rules
- `.ai/changes/` — change-specific proposal/design/tasks/results
- tests / `qa/` / `.ai/verification/` — verification evidence

Do not collapse these layers into one document.

## Adaptive rigor

Scale process to risk:

- L0 trivial: implementation + focused verification
- L1 small fix: short plan + implementation + verification
- L2 feature: spec + plan + implementation + verification
- L3 architectural: spec + design/ADR + plan + tests + verification
- L4 migration/security/critical: impact + rollback/migration/security + staged verification

Do not create unnecessary paperwork for trivial changes.

## Brownfield rule

Existing behavior is evidence. Before invasive changes, inspect:

- code and entry points
- routes/APIs/state
- dependencies and runtime constraints
- database/migrations
- tests and QA
- modules/plugins/extensions
- framework core/vendor/generated boundaries
- integrations and deployment
- existing project-specific instructions

Do not silently replace existing conventions with bootstrap defaults.

## Extension/platform rule

When working on a module, plugin, extension, or platform customization:

- detect host platform and version
- prefer supported extension points over core edits
- preserve install/upgrade/uninstall lifecycle
- check permissions and database changes
- preserve language/translation resources
- verify packaging and host compatibility
- classify existing core modifications as brownfield facts rather than automatically rewriting them

## Security rule

- Never copy secrets or environment values into specs, prompts, logs, discovery output, or generated AI context.
- Treat production writes, destructive commands, migrations, and permission changes as high-risk operations.
- Prefer mechanical permission boundaries when available; instructions alone are not a security boundary.

## Verification rule

Verification must match the product type. Browser QA is optional.

Valid verification may include:

- browser/UI
- API/backend
- CLI
- desktop
- unit/integration
- module install/upgrade/uninstall
- database/migration
- packaging
- security
- data-pipeline
- performance

If behavior changes, update verification evidence in the same task when practical.

## Writing style for product specs

Specs should be:

- short
- explicit
- product-level
- behavior-oriented

Avoid deep implementation detail unless it is required to preserve the product contract. Technical design belongs in the architecture/change layer.
