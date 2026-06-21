---
name: technical-paper-writing
description: Revise technical and academic papers for formal scholarly style, concision, terminology consistency, and evidence-safe wording. Use when editing or reviewing manuscript prose, LaTeX paper drafts, abstracts, introductions, related work, methods, results, discussions, thesis chapters, reviewer responses, or Japanese/English academic writing where colloquial wording, redundancy, synonym cycling, unclear terms, or invented claims must be avoided. Use alongside academic-research-suite for large research workflows and latex-documents for LaTeX compilation.
---

# Technical Paper Writing

## Overview

Apply the user's local paper-writing policy: precise academic prose, minimal redundancy, one canonical name per concept, and no invented facts, results, citations, or implications. Treat `academic-research-suite` as the large research workflow engine, but apply this skill as the lightweight style and terminology overlay for manuscript edits.

## Priority Rules

1. Preserve truth before style. Do not add claims, results, citations, numbers, limitations, or causal interpretations unless the user provided them.
2. Preserve technical meaning before fluency. If a smoother sentence weakens a distinction, keep the distinction and rewrite more narrowly.
3. Prefer precise repetition over elegant variation. A technical concept should have one canonical name within a section or paper.
4. Prefer plain academic prose over grand style. Do not replace colloquial prose with inflated or vague academic-sounding prose.
5. Preserve existing manuscript structure unless the user asks for restructuring.

## Workflow

1. Identify the requested mode:
   - Edit mode: directly revise the provided text or file.
   - Review mode: report issues and suggested replacements without changing files.
   - Policy mode: help define preferred terminology, register, or journal style.
2. Determine the manuscript language and field from the text. Keep the user's language unless asked to translate.
3. Run a terminology pass before polishing prose. Do not polish variants into more variants.
4. Run a style pass for academic register and concision.
5. Run a truth-preservation pass against the original text. Ensure every strengthened claim is still supported by the input.
6. For LaTeX files, preserve commands, labels, citations, math, environments, comments with build directives, and package-dependent syntax. If compilation is requested or practical, use `latex-documents`.

For full literature review, citation verification, peer-review simulation, or research-to-paper pipelines, use `academic-research-suite` first, then apply this policy to the writing output.

## Academic Style Pass

Remove or replace wording that is too conversational for a paper. Examples:

- English: `a lot of`, `things`, `kind of`, `sort of`, `basically`, `really`, `pretty`, `big`, `get`, `nowadays`, `of course`, `it is obvious that`.
- Japanese: `いろいろ`, `たくさん`, `すごく`, `かなり` when imprecise, `〜な感じ`, `〜というもの`, `〜してしまう`, `もちろん`, `明らかに` when unsupported.

Prefer discipline-standard expressions:

- `use` / `employ` instead of business-register `leverage`, unless `leverage` is a field term.
- `examine`, `analyze`, `investigate`, or `evaluate` instead of vague `look at`.
- `indicate`, `suggest`, `show`, or `demonstrate` according to evidence strength.
- `This study investigates...` instead of `In this paper, we are going to look at...`.

Do not overstate novelty or importance. Replace unsupported `crucial`, `pivotal`, `groundbreaking`, `robust`, `comprehensive`, or `significant` with narrower terms, or remove them. Keep `significant` only when it means statistical significance or clearly justified importance.

## Concision Pass

Cut throat-clearing and redundant framing:

- `It should be noted that X` -> `X`
- `It is important to mention that X` -> `X`
- `In order to` -> `To`
- `Due to the fact that` -> `Because`
- `The purpose of this section is to discuss X` -> discuss `X` directly, unless it is a standard paper roadmap.

Remove duplicated explanations. If two sentences make the same point, keep the one with clearer evidence or more precise scope. Do not delete a repeated term merely because it repeats; delete repeated ideas, not necessary terminology.

## Terminology Consistency

Use one name for one concept.

When reviewing or editing a manuscript:

1. Extract candidate concept names, acronyms, method names, dataset names, model names, task names, variables, and Japanese/English translations.
2. Identify variants that appear to refer to the same concept.
3. Select a canonical term only when the local text makes the intended concept clear.
4. Replace variants consistently within the relevant scope.
5. If variants may indicate distinct concepts, report the ambiguity instead of merging them.

Use this compact audit format when reporting instead of editing:

```text
Term audit
- Canonical: retrieval-augmented generation
  Variants: RAG, retrieval augmented generation, retrieval-based generation
  Action: define acronym once, then use RAG after first mention.
```

Do not use synonym cycling to avoid repetition. In academic writing, technical repetition is clarity.

## Evidence-Safe Wording

Use hedging that matches the evidence:

- Direct result from the user's data: `show`, `demonstrate`, `indicate`.
- Plausible interpretation: `suggest`, `may indicate`, `is consistent with`.
- Unsupported or speculative explanation: mark as speculation or ask for evidence.

Never fabricate references, DOIs, author names, publication years, p-values, sample sizes, experimental settings, limitations, or future work. If a citation or result is missing, write a placeholder or ask for the source.

## LaTeX Manuscripts

When editing `.tex`:

- Preserve `\cite`, `\ref`, `\label`, `\autoref`, `\cref`, math commands, custom macros, and environments.
- Do not rename labels, bibliography keys, commands, variables, or theorem names as part of prose terminology cleanup.
- Keep `% !LW recipe=...` and other build comments unchanged.
- Use `latex-documents` for compile behavior and equation-numbering preferences.

## Output Expectations

For direct edits, make the smallest changes that satisfy the requested policy. For reviews, lead with the highest-impact issues: terminology conflicts, unsupported claims, then style and concision. Include examples only when they clarify the edit.

When uncertain, say what is uncertain and offer a conservative replacement rather than inventing context.
