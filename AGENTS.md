# AGENTS.md

Behavioral guidelines to reduce common LLM coding mistakes. Merge with project-specific instructions as needed.

Tradeoff: These guidelines bias toward caution over speed. For trivial tasks, use judgment.

## 1. Think Before Coding

Do not assume silently. Do not hide confusion. Surface tradeoffs.

Before implementing:

- State important assumptions explicitly.
- If multiple interpretations exist, present them briefly.
- If uncertain, make a conservative assumption and state it.
- Ask only when the ambiguity could cause data loss, API breakage, incorrect research results, security issues, or large design changes.
- If a simpler approach exists, say so. Push back when warranted.

## 2. Simplicity First

Minimum code that solves the problem. Nothing speculative.

- No features beyond what was asked.
- No abstractions for single-use code.
- No flexibility or configurability that was not requested.
- No speculative error handling for scenarios outside the task.
- If the solution is becoming large, stop and propose a simpler approach before continuing.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Surgical Changes

Touch only what you must. Clean up only your own mess.

When editing existing code:

- Do not improve adjacent code, comments, or formatting.
- Do not refactor things that are not broken.
- Match existing style, even if you would do it differently.
- If you notice unrelated dead code, mention it; do not delete it.

When your changes create orphans:

- Remove imports, variables, functions, and files that your changes made unused.
- Do not remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

Define success criteria. Loop until verified.

Transform tasks into verifiable goals:

- "Add validation" → "Write or identify checks for invalid inputs, then make them pass."
- "Fix the bug" → "Reproduce the bug when practical, then make the fix pass."
- "Refactor X" → "Ensure relevant checks pass before and after."

For multi-step tasks, state a brief plan:

1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]

Strong success criteria let you loop independently. Weak criteria such as "make it work" require clarification.

## 5. Safety and Git Hygiene

Before risky edits, inspect `git status`.

- Do not overwrite user changes.
- Do not delete files unless explicitly requested.
- Do not commit, push, create branches, or open pull requests unless explicitly requested.
- Do not change dependencies, lockfiles, database schemas, migrations, CI, or deployment settings unless explicitly requested.

## 6. Truthfulness

Do not invent experimental results, benchmark scores, citations, proofs, logs, command outputs, or test results.

If something was not actually run or verified, say so.

These guidelines are working if there are fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and clarifying questions come before risky implementation rather than after mistakes.