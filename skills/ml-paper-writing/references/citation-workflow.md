# Citation Management & Hallucination Prevention

This reference provides a complete workflow for managing citations programmatically, preventing AI-generated citation hallucinations, and maintaining clean bibliographies.

---

## Contents

- [Why Citation Verification Matters](#why-citation-verification-matters)
- [Citation APIs Overview](#citation-apis-overview)
- [Verified Citation Workflow](#verified-citation-workflow)
- [Python Implementation](#python-implementation)
- [BibTeX Management](#bibtex-management)
- [Common Citation Formats](#common-citation-formats)
- [Troubleshooting](#troubleshooting)

---

## Why Citation Verification Matters

Generated citations may contain invented titles, identifiers, authors, or publication details. Verify the bibliographic record and the claim it supports before inserting a citation. An API response or a search hit alone does not validate a claim.

## Citation APIs Overview

Use existing bibliography entries and primary sources first. For discovery or metadata retrieval, these services are optional:

| Service | Use |
|---------|-----|
| Semantic Scholar | Paper discovery and citation graphs |
| DOI content negotiation | Metadata/BibTeX for a known DOI |
| Crossref | DOI registration metadata |
| arXiv | Preprint records and source text |
| OpenAlex | Discovery and bulk metadata |

Check the service's current documentation for authentication and rate limits when using its API. A browser, publisher page, proceedings entry, or supplied paper can be sufficient; no particular API or package is required.

## Verified Citation Workflow

1. Find the intended paper, preserving any existing citation key.
2. Check title, authors, year, version, and identifier against an authoritative record. Use a second source if records conflict or the first is incomplete.
3. Obtain BibTeX from that record when available, or transcribe its verified metadata. Check the entry type and escaping; downloaded BibTeX is not guaranteed correct.
4. Read the relevant passage, result, or method to confirm support for the claim. An abstract keyword match is insufficient.
5. Add the entry without overwriting unrelated bibliography content. Mark unresolved citations explicitly instead of inventing fields.

## Python Implementation

For an already identified DOI, this optional standard-library helper retrieves candidate BibTeX. Inspect the response and compare its metadata with the source before adding it:

```python
from urllib.request import Request, urlopen

request = Request(
    "https://doi.org/10.48550/arXiv.1706.03762",
    headers={"Accept": "application/x-bibtex"},
)
with urlopen(request, timeout=20) as response:
    bibtex = response.read().decode("utf-8")
print(bibtex)
```

If content negotiation is unavailable, use the publisher or repository export, or transcribe verified fields. Do not select the first search result automatically or label unverified records as verified.

---

## BibTeX Management

### BibTeX vs BibLaTeX

| Feature | BibTeX | BibLaTeX |
|---------|--------|----------|
| Unicode support | Limited | Full |
| Entry types | Standard | Extended (@online, @dataset) |
| Customization | Limited | Highly flexible |
| Backend | bibtex | Biber (recommended) |

Preserve the venue template's bibliography system. Use BibLaTeX/Biber only when the template permits it and it fits the project.

### Optional BibLaTeX Setup

```latex
% In preamble
\usepackage[
    backend=biber,
    style=numeric,
    sorting=none
]{biblatex}
\addbibresource{references.bib}

% In document
\cite{vaswani_2017_attention}

% At end
\printbibliography
```

### Citation Commands

For natbib-based templates:

```latex
\cite{key}      % Numeric: [1]
\citep{key}     % Parenthetical: (Author, 2020)
\citet{key}     % Textual: Author (2020)
\citeauthor{key} % Just author name
\citeyear{key}  % Just year
```

For BibLaTeX, use its supported commands such as `\parencite` and `\textcite`; do not assume natbib commands are enabled.

### Consistent Citation Keys

Preserve existing keys. For new entries, `author_year_firstword` is one possible convention:

```
vaswani_2017_attention
devlin_2019_bert
brown_2020_language
```

---

## Common Citation Formats

### Conference Paper

```bibtex
@inproceedings{vaswani_2017_attention,
  title = {Attention Is All You Need},
  author = {Vaswani, Ashish and Shazeer, Noam and Parmar, Niki and
            Uszkoreit, Jakob and Jones, Llion and Gomez, Aidan N and
            Kaiser, Lukasz and Polosukhin, Illia},
  booktitle = {Advances in Neural Information Processing Systems},
  volume = {30},
  year = {2017},
  publisher = {Curran Associates, Inc.}
}
```

### Journal Article

```bibtex
@article{hochreiter_1997_long,
  title = {Long Short-Term Memory},
  author = {Hochreiter, Sepp and Schmidhuber, J{\"u}rgen},
  journal = {Neural Computation},
  volume = {9},
  number = {8},
  pages = {1735--1780},
  year = {1997},
  publisher = {MIT Press}
}
```

### arXiv Preprint

```bibtex
@misc{brown_2020_language,
  title = {Language Models are Few-Shot Learners},
  author = {Brown, Tom and Mann, Benjamin and Ryder, Nick and others},
  year = {2020},
  eprint = {2005.14165},
  archiveprefix = {arXiv},
  primaryclass = {cs.CL}
}
```

---

## Troubleshooting

### Common Issues

**Issue: Semantic Scholar returns no results**
- Try more specific keywords
- Check spelling of author names
- Use quotation marks for exact phrases

**Issue: DOI doesn't resolve to BibTeX**
- DOI may be registered but not linked to CrossRef
- Try arXiv ID instead if available
- Generate BibTeX from metadata manually

**Issue: Rate limiting errors**
- Respect the service's current rate limits and retry guidance
- Use API key if available
- Cache results to avoid repeat queries

**Issue: Encoding problems in BibTeX**
- Use proper LaTeX escaping: `{\"u}` for ü
- Ensure file is UTF-8 encoded
- Preserve the template's backend; use its supported Unicode or LaTeX escaping conventions

### Verification Checklist

Before adding a citation:

- [ ] Intended paper matched to an authoritative record; conflicts resolved
- [ ] DOI or arXiv ID verified when present; no identifier invented
- [ ] BibTeX retrieved or transcribed from verified metadata
- [ ] Entry type correct (@inproceedings vs @article)
- [ ] Author names complete and correctly formatted
- [ ] Year and venue verified
- [ ] Existing citation keys preserved; new keys consistent
- [ ] Source text supports the cited claim

---

## Additional Resources

**APIs:**
- Semantic Scholar: https://api.semanticscholar.org/api-docs/
- CrossRef: https://www.crossref.org/documentation/retrieve-metadata/rest-api/
- arXiv: https://info.arxiv.org/help/api/basics.html
- OpenAlex: https://docs.openalex.org/

**Python Libraries:**
- `semanticscholar`: https://pypi.org/project/semanticscholar/
- `arxiv`: https://pypi.org/project/arxiv/
- `habanero` (CrossRef): https://github.com/sckott/habanero

**Verification Tools:**
- Citely: https://citely.ai/citation-checker
- ReciteWorks: https://reciteworks.com/
