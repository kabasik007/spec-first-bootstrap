# AGENTS.md

Rules for agents working on Universal AI Development Bootstrap itself.

For bootstrapping another repository, also read `AUTONOMOUS_BOOTSTRAP.md`.

## Autonomous trigger

- If a user references this repository while working on a software project, treat that as a request to autonomously onboard the current workspace unless they say otherwise.
- Do not force the user through a setup questionnaire when stack/runtime/architecture facts can be discovered from repository evidence.
- A short user intent is optional; do not invent missing product requirements from it.

## Reading order

Before non-trivial changes to this repository:

- Read `AGENTS.md`.
- Read `AUTONOMOUS_BOOTSTRAP.md` when changing onboarding behavior.
- Read `docs/architecture.md` and `docs/context-intelligence.md` when changing engine architecture.
- Read `docs/design-research.md` when changing default workflow philosophy.
- Read relevant tests before changing a behavioral invariant.

For a bootstrapped target, generated root `AGENTS.md` is the concise entry point; detailed target truth lives in `docs/` and `.ai/`.

## Trust order

When guidance conflicts:

- explicit current user instruction
- verified project-specific fact with provenance
- exact repository evidence
- matching version-specific baseline/documentation
- existing project architecture/specification
- detected capability pack
- generic bootstrap guidance

Generic advice must never override verified target compatibility.

## Discover first, ask second

- Inspect repository evidence before asking setup questions.
- Do not ask for a PHP/Python/Node/framework version when manifests/files already provide a safe compatibility constraint.
- Do not ask for a template engine when repository evidence clearly identifies it.
- If a material compatibility fact remains unresolved, ask rather than guess.
- Batch current blockers into one concise question set when practical.
- Give likely options plus `Other / specify`; never force a false choice.
- Explain why each answer changes compatibility, architecture, packaging, file format or implementation.
- Store confirmed answers as verified project memory and regenerate context/roadmap.

## Readiness gate

Full onboarding generates `.ai/questions/blocking.json`.

- `ready_for_implementation=true` — no material setup blocker is currently known.
- `ready_for_implementation=false` — onboarding is valid, but risky implementation must wait for blockers to be resolved.
- Advisory questions must not stop safe work unnecessarily.
- A blocker may be superseded by stronger repository evidence or a verified user answer.

## Roadmap rule

Full onboarding generates:

- `docs/ROADMAP.md` — human execution plan
- `.ai/planning/roadmap.json` — machine-readable phases/gates

The roadmap must contain:

- readiness/blocking state
- phase dependencies
- deliverables
- exit gates
- compatibility/architecture checkpoints
- verification phase
- documentation/package/handoff phase
- definition of done

Do not silently skip a phase whose gate is still blocked.

## Universal compatibility

- The bootstrap runtime is not the target runtime.
- Legacy runtimes/frameworks are valid targets.
- Do not introduce syntax/APIs newer than the target without an explicit migration.
- Do not normalize brownfield code merely because a newer convention exists.
- Preserve package manager, lockfile, build, deployment and extension conventions unless the active change migrates them.

## Architecture defaults

- Preserve brownfield architecture by default.
- Greenfield default: simplest architecture with strong internal boundaries.
- Keep core small and stable.
- Put feature/business behavior in explicit modules.
- Keep UI/API/CLI/platform entry points at the edge.
- Put database/filesystem/queues/external APIs behind infrastructure adapters.
- Avoid catch-all `core`, `shared`, `common`, or `utils` growth.
- Prefer internal module boundaries over microservices until a concrete operational boundary exists.

A new service boundary needs evidence such as:

- independent deployment
- independent scaling
- useful fault isolation
- explicit data ownership
- independent team/operational ownership

## Spec-first boundary

- Product specs define observable behavior.
- Architecture docs define system/module boundaries.
- Change design defines how one non-trivial change will be implemented.
- Verification artifacts prove the contract.
- Do not mix deep implementation detail into product specs.

## Autonomous onboarding output

Full `init/onboard` should establish:

- concise root `AGENTS.md`
- `docs/ARCHITECTURE.md`
- `docs/DEVELOPMENT.md`
- `docs/ROADMAP.md`
- `docs/specs/`
- `.ai/discovery/project-facts.json`
- `.ai/discovery/architecture.json`
- `.ai/discovery/dependency-graph.json`
- `.ai/standards/index.json`
- `.ai/research/agenda.json`
- `.ai/questions/blocking.json`
- `.ai/planning/roadmap.json`
- `.ai/policy.json`
- baseline, knowledge and project memory

Preserve existing user-authored content outside bootstrap managed blocks.

Do not generate `.codex`, `.claude`, `.cursor`, or other tool-specific project files by default.

## Retrieval-friendly instructions

- One rule/fact per bullet or line.
- Include exact paths for path-specific rules.
- Use stable keywords in headings and bullets.
- Keep root instruction files concise.
- Move detailed explanations to linked/scoped docs.
- Do not hide compatibility constraints in long prose.
- Add scoped `AGENTS.md` files only when a subtree genuinely has different rules.

## Research rule

Research is selective, not ceremonial.

Use official/version-matched primary sources when:

- framework/version behavior is uncertain
- official extension architecture changes a technical decision
- a current tool/standard capability may have changed

Do not apply latest-version documentation to a legacy target without matching evidence.

Record material findings with source, version/date, claim, affected decision and confidence.

If web access is unavailable, leave material unknowns unresolved instead of guessing.

## Brownfield rule

Before invasive changes inspect:

- existing instructions/docs/specs
- code and entry points
- dependency/runtime constraints
- database/migrations
- tests/QA
- modules/plugins/extensions
- core/vendor/generated boundaries
- integrations/deployment
- baseline/reference evidence when available

Existing modifications are evidence; do not silently replace them with bootstrap defaults.

## Extension/platform rule

For modules/plugins/extensions:

- detect host platform and version
- prefer supported extension points over core edits
- preserve install/upgrade/uninstall lifecycle
- check permissions/data changes
- preserve translations/language resources
- verify packaging and host compatibility
- classify existing core edits before changing them

OpenCart and PrestaShop are capability packs, not global assumptions.

If host version or presentation technology is unclear and the answer affects implementation, ask explicitly. Typical examples:

- OpenCart generation/version
- target PHP compatibility floor
- `.tpl` versus Twig/view layer
- theme/override mechanism
- install/upgrade expectations

## Policy/security

Instructions are not a sandbox.

Use `.ai/policy.json` / `policy-check` for guarded actions.

- `allow` — proceed under normal workflow
- `confirm` — require explicit guarded approval
- `deny` — do not proceed

Never copy secret values into specs, prompts, logs, memory, baseline output, research findings or generated AI context.

Treat production writes, destructive commands, migrations and security/permission changes as high-risk.

## Project memory

- Project memory must preserve provenance.
- Never store secrets.
- Never turn guesses into durable facts.
- Manual verified facts must not be silently overwritten by auto-discovery.
- Re-verify stale environment facts when they may have changed.

## Adaptive rigor

- L0 trivial — implementation + focused verification
- L1 small fix — short plan + implementation + verification
- L2 feature — spec + roadmap phase + implementation + verification
- L3 architecture — spec + design/ADR + roadmap gates + tests + verification
- L4 migration/security/critical — impact + rollback/migration/security + staged verification

Do not create paperwork for trivial work.

## Verification

Verification must match the system capability:

- browser/UI
- API/backend
- CLI
- desktop
- unit/integration
- module install/upgrade/uninstall
- database/migration
- packaging
- security
- pipeline
- performance

Behavior changes should update verification evidence in the same task when practical.
