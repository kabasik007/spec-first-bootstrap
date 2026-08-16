# Design Research: Autonomous Bootstrap v1.2

This document records the external ideas used to improve Universal AI Development Bootstrap. It is not a dependency list and does not mean this project copies another framework's workflow.

## GitHub Spec Kit

Primary sources:

- https://github.com/github/spec-kit
- https://github.com/github/spec-kit/blob/main/templates/plan-template.md
- https://github.com/github/spec-kit/blob/main/templates/commands/constitution.md

Useful ideas adopted:

- establish project principles/architecture gates before implementation
- separate product specification from technical implementation planning
- resolve unknown technical context through a research phase
- make architecture decisions explicit rather than leaving them in chat history

Ideas intentionally not copied as defaults:

- mandatory heavyweight phase ceremony for every change
- assuming greenfield structure templates are correct for brownfield repositories

## OpenSpec

Primary sources:

- https://github.com/Fission-AI/OpenSpec
- https://github.com/Fission-AI/OpenSpec/blob/main/docs/getting-started.md

Useful ideas adopted:

- distinguish current system truth from proposed changes
- keep brownfield work first-class
- keep proposal/design/tasks together for a non-trivial change
- allow lightweight explore/research before committing to a design

Ideas intentionally not copied as defaults:

- requiring a separate command vocabulary for ordinary day-to-day use
- requiring Node installation for the bootstrap engine

## Agent OS

Primary source:

- https://github.com/buildermethods/agent-os

Useful ideas adopted:

- discover standards from the existing codebase
- inject only relevant standards instead of one giant instruction document
- keep project onboarding self-contained
- let modern coding agents implement plans instead of over-orchestrating many fake personas/subagents

## BootstrapAgent

Primary research/code references:

- https://arxiv.org/abs/2605.15815
- https://github.com/Vossera/BootstrapAgent

Useful ideas adopted:

- repository bootstrap knowledge should persist beyond one chat
- setup/repair knowledge should be evidence-backed and reusable
- deterministic verification is more valuable than a prose-only memory
- repeated agents should reuse a verified project contract rather than rediscover everything

## Codex AGENTS.md behavior

Primary source:

- https://github.com/openai/codex/blob/main/docs/agents_md.md

Useful ideas adopted:

- keep root `AGENTS.md` concise
- use scoped/hierarchical instructions only when a directory genuinely needs different rules
- write project instructions for retrieval, not as long narrative documentation
- keep detailed architecture/development knowledge in linked project docs

## Agent Skills specification

Primary source:

- https://agentskills.io/specification

Useful idea adopted:

- expose the autonomous bootstrap workflow as a standard `SKILL.md` capability without making skills a runtime requirement

## Resulting design

The combined v1.2 default is intentionally simpler than the systems above:

```text
repository + optional one-line intent
        |
        v
inspect evidence
        |
        v
research only material unknowns
        |
        v
preserve/choose simplest sufficient architecture
        |
        v
small core + explicit modules + edge adapters
        |
        v
AGENTS.md + human docs + machine-readable .ai context
        |
        v
spec/design only when the requested change actually needs them
        |
        v
implement + verify
```

The goal is not to maximize generated artifacts. The goal is to make the next coding session start with correct project context and architecture without making the user repeat setup instructions.
