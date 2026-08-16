# AGENTS.md

This file defines workflow rules for agents working on Universal Bootstrap itself and for agents using a generated project harness.

It is not the source of truth for detailed product behavior. Product behavior belongs in `docs/specs/`. Technical project facts and guardrails belong in generated `.ai/` artifacts.

## Reading order

Before non-trivial implementation work:

1. Read `AGENTS.md`.
2. Read `docs/architecture.md`.
3. For a bootstrapped target, read:
   - `.ai/PROJECT.md`
   - `.ai/ARCHITECTURE.md`
   - `.ai/DEPENDENCIES.md`
   - `.ai/RULES.md`
   - `.ai/VERIFICATION.md`
   - `.ai/policy.json`
4. Read relevant product specs under `docs/specs/`.
5. Read active `.ai/changes/<id>/` artifacts for risky or architectural work.
6. Read project memory only as evidence with provenance, never as an excuse to skip current repository evidence.

## Detect before assuming

Do not assume language, framework, runtime version, commands, package manager, project type, extension model or architecture when repository evidence can answer it.

Prefer:

```bash
python bootstrap.py detect <target>
python bootstrap.py init <target>
```

Treat detected facts as evidence with confidence, not infallible truth.

## Trust order

When facts conflict, prefer:

1. explicitly verified project fact with provenance
2. exact project/version-specific repository evidence
3. baseline/reference evidence confirmed to match the target
4. high-confidence detection
5. capability-pack guidance
6. generic knowledge

Never let generic guidance override a verified target constraint.

## Universal compatibility rule

The bootstrap runtime is not the target runtime.

A target may intentionally use legacy PHP, Python, Node, Java, .NET, databases, browsers, OS versions or framework generations.

- Do not introduce syntax/APIs newer than the supported target without an explicit migration.
- Do not normalize a legacy project merely because newer conventions exist.
- Preserve package manager, lockfile, build, deployment and extension conventions unless the change intentionally migrates them.

## Spec-first rule

Before implementing a non-trivial observable behavior change:

1. clarify the product goal
2. create or update the relevant product spec
3. confirm behavior, invariants, failure policy and compatibility
4. create technical design separately when architectural
5. implement against the contract
6. update verification evidence

## Separation of concerns

- `AGENTS.md` — workflow rules
- `docs/specs/` — observable product behavior
- `.ai/PROJECT.md` — detected project facts
- `.ai/ARCHITECTURE.md` — system shape/boundaries
- `.ai/DEPENDENCIES.md` — declared dependency evidence
- `.ai/BASELINE.md` — local/reference boundary evidence
- `.ai/RULES.md` — merged project/pack rules
- `.ai/policy.json` — machine-readable guarded actions
- `.ai/knowledge/` — reusable guidance with provenance
- `.ai/memory/` — project-specific facts with provenance
- `.ai/changes/` — change proposal/design/tasks/result
- tests / `qa/` / `.ai/verification/` — verification evidence

Do not collapse these layers into one file.

## Adaptive rigor

Scale process to risk:

- L0 trivial — implementation + focused verification
- L1 small fix — short plan + implementation + verification
- L2 feature — spec + plan + implementation + verification
- L3 architectural — spec + design/ADR + plan + tests + verification
- L4 migration/security/critical — impact + rollback/migration/security + staged verification

Do not create unnecessary paperwork for trivial changes.

## Brownfield rule

Existing behavior and existing modifications are evidence.

Before invasive changes inspect:

- code and entry points
- routes/APIs/state
- dependencies and runtime constraints
- database/migrations
- tests/QA
- modules/plugins/extensions
- core/vendor/generated boundaries
- integrations/deployment
- existing project-specific instructions
- baseline/reference evidence when available

Do not silently replace established conventions with bootstrap defaults.

## Baseline rule

A baseline/reference tree is only authoritative if its identity/version matches the target.

Use:

```bash
python bootstrap.py baseline <target> --reference <reference>
```

to identify added, missing and modified files.

Do not automatically assume that a framework's latest upstream release is the correct baseline for a legacy target.

## Extension/platform rule

For modules, plugins, extensions and platform customizations:

- detect host platform/version
- prefer supported extension points over core edits
- preserve install/upgrade/uninstall lifecycle
- check permissions/data changes
- preserve translations/language resources
- verify package layout and host compatibility
- classify existing core edits before changing them

OpenCart/PrestaShop are packs, not global assumptions.

## Dependency rule

Dependency manifests are compatibility contracts.

Before adding/upgrading a dependency:

- inspect current manifest and lockfile conventions
- inspect declared runtime/toolchain constraints
- understand public API or build impact
- verify target compatibility

The generated dependency graph is direct manifest evidence, not a complete runtime call graph.

## Memory rule

Project memory must preserve provenance.

Use `memory-add` for manually verified facts.

- Never store secrets.
- Never turn guesses into durable facts.
- Manual verified facts must not be silently overwritten by automated discovery.
- Re-verify stale facts when the environment may have changed.

## Knowledge rule

Generic knowledge is weaker than project-specific evidence.

Keep source/provenance on every knowledge entry. Do not silently inject unsourced “best practices” into project memory.

## Policy/security rule

Instructions are not a sandbox.

Before guarded actions use `.ai/policy.json` and:

```bash
python bootstrap.py policy-check <target> read <path>
python bootstrap.py policy-check <target> write <path>
python bootstrap.py policy-check <target> execute "<command>"
```

Interpret results:

- `allow` — policy did not block the action
- `confirm` — obtain explicit approval / use guarded workflow
- `deny` — do not proceed

Never copy secret values into specs, prompts, memory, logs, baseline output or generated AI context.

Treat production writes, destructive commands, migrations and permission/security changes as high-risk.

## Verification rule

Verification must match capabilities.

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

Avoid deep implementation detail unless it is necessary to preserve the product contract. Technical design belongs in architecture/change artifacts.
