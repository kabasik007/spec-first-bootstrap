This target project has a browser UI.

Use this bootstrap repository as the reference:

https://github.com/kabasik007/spec-first-bootstrap

Assume the universal bootstrap harness is already installed and browser/UI verification was selected as an appropriate capability.

Read:

- `.ai/PROJECT.md`
- `.ai/ARCHITECTURE.md`
- `.ai/RULES.md`
- `qa/README.md`
- `qa/web/README.md`
- `qa/web/AGENTS.snippet.md`

Add or adapt:

1. the minimal QA folder structure
2. smoke vs regression vs experimental guidance
3. report and bug templates
4. rules for when a browser QA case is required
5. spec-to-QA mapping
6. the `qa/web/AGENTS.snippet.md` routing block in the target `AGENTS.md`

Keep browser QA optional. Prefer DOM-checkable behavior, real-browser verification, console-error checks and core network-failure checks.

Do not change product code while installing the QA layer, and do not apply this pack to non-browser products.
