# Research notes

Working notes documenting the formal mathematical content underlying the universal spectral lower bound. These are **not** the submission-ready manuscript — they are reference documents that the eventual submission (and the individual corollary papers) will draw from.

| File | Content |
|:---|:---|
| `01_universal_bound_proof.tex` | Formal statement and proof of Theorem 1 (universal lower bound) and Theorem 2 (Pesenson-ridge saturation). Includes Corollary C1 (recovery of MLST Theorem 1), sketches of C2 (negative transfer) and C3 (active learning), and a list of open questions. |

## Conventions

- Notation matches the MLST paper [`materials-applicability-bound/applicability_bound.tex`](https://github.com/cycling-data-lab/materials-applicability-bound/blob/main/applicability_bound.tex) wherever possible (`\Rspec`, `\Lsym`, `\bphi`, `\by`).
- Notes use `article` class rather than `iopjournal.cls` — they are not formatted for any specific venue.
- All theorems are stated with explicit assumptions; nothing is left implicit.
- Open questions are numbered and tagged for follow-up.

## Build

```bash
pdflatex notes/01_universal_bound_proof.tex
```
