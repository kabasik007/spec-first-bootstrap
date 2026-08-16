# Context Intelligence Layer

Universal Bootstrap v1.1 introduced the machine-readable context layer described below.

**v1.2 keeps this layer intact and adds autonomous architecture synthesis, standards discovery, research planning, `AGENTS.md`, and human-facing architecture/development docs on top of it.**

For the current default workflow, read:

- `AUTONOMOUS_BOOTSTRAP.md`
- `docs/architecture.md`

The Context Intelligence layer itself remains stack-agnostic:

```text
repository evidence
      ↓
discovery
      ↓
capability pack resolution
      ↓
dependency/workspace graph + baseline
      ↓
policy + knowledge + memory
      ↓
project-specific .ai/ context
```

## Baseline engine

`init` creates a local inventory under `.ai/baseline/inventory.json`.

Secret-like files are skipped. Each inventoried file has:

- relative path
- SHA-256
- size
- classification: `project`, `protected`, or `generated-or-vendor`

To compare a target with an official/upstream/local reference tree:

```bash
python bootstrap.py baseline /path/to/project --reference /path/to/reference
```

This writes `.ai/baseline/diff.json` and reports:

- added files
- missing files
- modified files
- changes inside protected paths

The engine does not download a reference automatically. This keeps ordinary bootstrap work local-first and avoids silently comparing against the wrong framework generation.

## Dependency/workspace graph

The graph is generated from local manifests and written to:

```text
.ai/discovery/dependency-graph.json
.ai/DEPENDENCIES.md
```

v1.2 scans supported manifests across the repository, not only at the root, so paths such as:

```text
services/auth/package.json
services/orders/composer.json
packages/shared/pyproject.toml
```

can become explicit workspace component evidence.

Supported direct dependency evidence includes:

- Composer
- npm/package.json
- requirements.txt
- pyproject.toml
- Cargo
- Go modules
- Maven
- NuGet `.csproj`
- Gradle manifests as build/component boundaries

The graph records ecosystem, package, constraint, scope, source manifest and nested manifest-defined components.

This is still dependency/build evidence, not a fake complete runtime call graph. Source/import/call and data-flow analysis can be layered on later.

## Executable capability packs

v1.0 selected pack IDs. v1.1 made them executable.

A pack can contribute:

- `extends`
- compatibility rules
- project/architecture rules
- protected paths
- verification requirements
- knowledge IDs
- policy fragments

Resolution is recursive and deterministic. Detailed manifests are loaded from `packs/**.json`; catalog-only packs remain usable as fallback capabilities and are surfaced as warnings by `verify`.

This keeps the system universal without a giant stack-specific switch.

## Knowledge catalog

Generic reusable guidance lives in `knowledge/catalog.json`.

Each knowledge entry has:

- stable ID
- title
- summary
- source/provenance
- confidence

Selected entries are written to `.ai/knowledge/index.json`.

Knowledge is deliberately separate from project memory:

- knowledge = reusable bootstrap guidance
- memory = facts verified about this particular project

Project-specific evidence always wins over generic guidance.

## Project memory

`.ai/memory/project-memory.json` stores durable project facts with provenance.

An automatically detected fact contains:

- value
- confidence
- discovery evidence
- `observed_at`
- `last_seen`

Add a manually verified fact:

```bash
python bootstrap.py memory-add /path/to/project runtime.production_php 7.4.33 \
  --source "production php -v" --confidence 1
```

Manual facts are not overwritten by later discovery refreshes.

Do not store secret values in project memory.

## Policy and permissions

`init` writes `.ai/policy.json`.

The generated policy can contain:

- `deny_read`
- `deny_write`
- `confirm_write`
- `confirm_commands`

Examples:

```bash
python bootstrap.py policy-check /path/to/project read .env
python bootstrap.py policy-check /path/to/project write system/library/foo.php
python bootstrap.py policy-check /path/to/project execute "git reset --hard HEAD~1"
```

Exit semantics:

- `0` = allow
- `2` = deny
- `3` = explicit confirmation required

The policy file is not itself a sandbox. A coding agent, IDE integration, CI wrapper or future skill must call `policy-check` or implement equivalent enforcement before guarded actions.

## Generated machine context

```text
.ai/
├── manifest.yaml
├── PROJECT.md
├── ARCHITECTURE.md
├── DEPENDENCIES.md
├── BASELINE.md
├── COMMANDS.md
├── RULES.md
├── VERIFICATION.md
├── policy.json
├── discovery/
│   ├── project-facts.json
│   ├── packs.json
│   ├── dependency-graph.json
│   ├── architecture.json
│   └── risks.json
├── standards/
│   └── index.json
├── research/
│   └── agenda.json
├── baseline/
├── knowledge/
├── memory/
├── decisions/
├── changes/
└── verification/
```

## Trust order

When facts conflict:

1. explicit current user instruction
2. verified project fact with provenance
3. exact project/version-specific repository evidence
4. baseline/reference evidence confirmed to match the target
5. high-confidence detection
6. capability-pack guidance
7. generic knowledge

Never let generic advice override known target compatibility.
