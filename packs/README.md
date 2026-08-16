# Capability Packs

Capability packs make Universal Bootstrap composable instead of framework-bound.

A target can resolve many packs at once:

```text
base/spec-first
base/architecture
base/change-lifecycle
base/security
languages/php
frameworks/opencart
project-types/extension-platform
verification/extension
verification/web
```

## v1.1 resolution

The engine loads detailed manifests from `packs/**.json`.

If a selected ID exists only in `catalog.json`, it becomes a virtual/fallback pack. Bootstrap still works, but `verify` warns that the capability has no detailed manifest yet.

`extends` is recursive. Parents are resolved before children.

Merged pack context is written to:

```text
.ai/discovery/packs.json
```

## What a detailed pack can contribute

- `compatibility` — target runtime/framework compatibility guidance
- `rules` — project/change rules
- `protected_paths` — paths that should receive additional baseline/policy attention
- `verification` — project-appropriate checks
- `knowledge_ids` — curated reusable guidance
- `policy` — machine-readable guardrail fragments
- `extends` — reusable parent capabilities

Example:

```json
{
  "id": "frameworks/example",
  "version": "1.1.0",
  "kind": "framework",
  "extends": ["languages/php"],
  "compatibility": [
    "Detect the exact framework generation before applying conventions."
  ],
  "protected_paths": ["core/"],
  "rules": [
    "Prefer extension points over core edits."
  ],
  "verification": [
    "Verify install/upgrade compatibility."
  ],
  "knowledge_ids": [
    "runtime-compatibility"
  ],
  "policy": {
    "confirm_write": ["core/"]
  }
}
```

## Universal rule

A pack describes a capability. It must not turn that capability into a global assumption.

Adding a detailed OpenCart pack does not make the bootstrap “for OpenCart.” Adding a React pack does not imply all targets have a browser UI.

## Catalog

`catalog.json` is the discoverable capability index.

Detailed manifests can be added incrementally while catalog-only fallback keeps less-modeled stacks usable.

## Schema

See:

- `../schemas/pack.schema.json`
- `../schemas/policy.schema.json`
- `../schemas/memory.schema.json`
