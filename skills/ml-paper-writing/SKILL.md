---
name: ml-paper-writing
description: Draft or revise ML/AI research papers, verify their citations, and prepare venue submissions. Use for manuscript work, not general ML implementation.
license: MIT
metadata:
  version: "1.2.0"
  author: Orchestra Research
---

# ML Paper Writing

Produce the requested manuscript or revision from the supplied research evidence. Preserve the author's intended contribution, technical meaning, and uncertainty. Read the code, results, and context needed to support the affected claims; a paragraph edit does not require a full repository survey.

## Evidence and scope

- Tie each contribution to observed results or a stated argument. Do not invent experiments, numbers, proofs, citations, or claims of novelty.
- Verify new or materially changed citations against the paper and authoritative metadata. Bibliographic identity and support for the attributed claim are separate checks. Mark unresolved items explicitly; do not fabricate a plausible reference.
- Retain uncertainty justified by evidence. Do not make claims stronger merely to improve the narrative.
- Use the requested venue, year, track, and submission phase. Bundled templates and checklists are dated starting points, not current submission rules.
- Continue through the requested scope and resolve local drafting/build issues. Ask when missing evidence or conflicting instructions prevent a substantive decision; otherwise state a provisional framing and deliver the requested draft. Do not require approval for each section or expand a section edit into a full paper.
- Preparing a submission does not authorize uploading or submitting it.

## Read for the current task

| Task | Resource |
| --- | --- |
| Narrative, argument, or sentence-level revision | [Writing guide](references/writing-guide.md); use the relevant sections |
| Finding references or repairing bibliographic entries | [Citation workflow](references/citation-workflow.md) |
| Submission or camera-ready preparation | [Checklists](references/checklists.md), then the target's current official instructions |
| Reviewer-style assessment or rebuttal | [Reviewer guidelines](references/reviewer-guidelines.md) |
| New LaTeX project or venue conversion | [Template guide](templates/README.md) |
| Provenance of the writing advice | [Sources](references/sources.md) |

Do not load every resource for each task. No additional search service or Python package is required merely to use this skill; use available search and citation exports.

## Manuscripts and templates

For a full draft, make the contribution, evidence, and significance clear, and include the methods, limitations, and reproducibility details that the research and venue require. Section order, abstract length, figure order, and contribution counts should fit the paper rather than a fixed recipe.

For a new LaTeX project, copy the chosen template with its required style and bibliography files. For venue conversion, transfer content into the target template and reconcile macros; do not merge preambles blindly or modify venue styles to evade formatting rules. Preserve the existing engine and build configuration when editing an established project.

Inspect the affected output: for prose, check claim support and consistency; for bibliography edits, check metadata, citation keys, and attributed claims; for formatting changes, compile and inspect relevant rendered pages when tools are available. Report unresolved evidence, citation, or build gaps. Stop when the requested deliverable is complete and these checks are satisfied.
