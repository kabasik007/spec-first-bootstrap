# Prompt-First Bootstrap

## Goal

Make the default onboarding path a single prompt that points an AI coding agent
at this public repository and asks it to set up spec-first development in the
current project.

The user should not need to clone this repository locally or pass a local path
before the agent can apply the workflow.

## Scope

This spec covers:

- README onboarding
- prompt-pack wording
- manual install positioning
- expectations for what the agent should copy or adapt

## Non-goals

- changing the spec-first workflow itself
- making browser QA mandatory
- defining behavior for every AI coding agent
- replacing project-specific judgment with a rigid installer

## User-visible behavior

- The first setup path should be a copy-paste prompt with the GitHub repository
  URL.
- The prompt should ask the agent to set up the current project for spec-first
  development.
- The prompt should tell the agent to read this bootstrap repository before
  editing the target project.
- For existing projects, the prompt should preserve the brownfield rule: inspect
  the project and create first-pass specs before changing implementation code.
- Manual copy instructions may exist, but they should be secondary and hidden
  behind a collapsed Markdown details block.
- Local clone plus local path instructions should not be presented as the
  normal setup path.
- Optional browser QA should remain optional and should be added only when it
  fits the target project.

## Invariants

- `docs/specs/` remains the product-contract layer.
- `AGENTS.md` remains the agent workflow layer.
- `qa/` remains a verification layer, not a product-contract layer.
- The README should stay short and direct rather than becoming landing-page
  copy.
- The bootstrap should work for web, backend, API, CLI, and other software
  projects.

## Edge cases and failure policy

- If an agent cannot fetch or inspect the GitHub repository, the user may use
  the manual copy fallback.
- If the target project already has an `AGENTS.md`, the agent should merge the
  workflow rules instead of blindly replacing project-specific instructions.
- If the target project is not a browser UI, the agent should skip the optional
  browser-QA pack.

## Route / state / data implications

- None.

## Verification mapping

- README should start with the repo-URL prompt path.
- Prompt files should not require `<BOOTSTRAP_PATH>`.
- Manual installation should be secondary and collapsed.
