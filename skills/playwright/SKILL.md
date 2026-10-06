---
name: playwright
description: Automate a browser from the terminal with Playwright CLI for navigation, data extraction, screenshots, and UI debugging.
---

# Playwright CLI

Use the bundled wrapper or an existing project-standard `playwright-cli` installation. This skill covers browser operations; use the project's testing conventions when the user requests test code.

```bash
PWCLI="${CODEX_HOME:-$HOME/.codex}/skills/playwright/scripts/playwright_cli.sh"
"$PWCLI" open https://example.com
"$PWCLI" snapshot
```

The wrapper requires `npx` and invokes `@playwright/cli`. Check `command -v npx` before executing it. If unavailable, use an already-installed CLI or report the missing Node.js/npm dependency; a global install is optional. Command explanations do not require installation.

## Browser interaction

- Obtain element refs from a snapshot before using them; do not invent ids such as `e12`.
- Refresh the snapshot after navigation or DOM changes that invalidate the refs, or when a ref fails.
- Prefer CLI actions for ordinary interaction. Use `eval` or `run-code` when a task needs capabilities the actions do not expose, with the same authorization boundaries as other actions.
- Use headed mode, screenshots, or traces when they help diagnose the requested behavior. Save artifacts to the requested location or the project's convention; otherwise use `output/playwright/`.
- Inspect the result of an interaction before claiming it worked. Navigation and inspection may continue within scope; submitting forms or changing remote data must be covered by the user's request.

## References

- Command syntax and session options: [CLI reference](references/cli.md).
- Forms, tabs, traces, and troubleshooting: [workflows](references/workflows.md).

Read only the relevant reference. Use the installed CLI's help when a command or flag differs from these examples.
