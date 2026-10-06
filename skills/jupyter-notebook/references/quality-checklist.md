# Quality Checklist

Before delivering a notebook:

- For executable changes, run the affected cells with their prerequisites, or run top-to-bottom when feasible and appropriate. A prose-only edit does not require rerunning expensive or externally mutating cells.
- Ensure early cells set all required state; avoid hidden state from prior runs.
- Keep outputs tidy. Avoid giant outputs when a short summary works.
- Prefer small tables, key metrics, or short printouts.
- Keep the narrative skimmable. Use headings and short bullets, and avoid long paragraphs.
- Leave helpful TODOs only when necessary, and label them clearly.
- If execution is not possible, call out the risk and how to validate locally.
