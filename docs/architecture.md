# Universal Bootstrap Architecture

The bootstrap is intentionally split into layers so it can support unrelated stacks without becoming a giant framework-specific prompt.

## Pipeline

```text
Target repository
  -> detector
  -> project facts + confidence/evidence
  -> architecture/risk discovery
  -> capability pack resolver
  -> project-specific .ai harness
  -> agent workflow
  -> verification
```

## Core principles

1. **Detect before instructing.** Never assume framework, version, runtime, or project type from a prompt alone when the repository can provide evidence.
2. **Compose, do not branch globally.** A repository may combine PHP + Node + Python + Docker + multiple frameworks.
3. **Keep product and technical truth separate.** `docs/specs/` defines observable product behavior; `.ai/ARCHITECTURE.md` and change designs define implementation structure and boundaries.
4. **Treat legacy as a supported state.** Old runtimes and modified framework cores are brownfield facts, not errors to normalize automatically.
5. **Scale process by risk.** Small changes should remain lightweight; migrations and architectural changes require stronger design and verification.
6. **Local-first by default.** Discovery and harness generation should work without network access. Network-backed knowledge or baseline comparison is an optional capability.
7. **Evidence over guesswork.** Generated facts should retain confidence and evidence so agents know what must still be verified.

## Generated target layout

```text
.ai/
  manifest.yaml
  PROJECT.md
  ARCHITECTURE.md
  COMMANDS.md
  RULES.md
  discovery/
    project-facts.json
    risks.json
  changes/
  verification/
  memory/
```

Future layers can add `baseline/`, `knowledge/`, richer dependency maps, policy enforcement, and pack-provided generators without changing the spec-first contract.
