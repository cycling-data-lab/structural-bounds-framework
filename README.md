# structural-bounds-framework

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/license/MIT)
[![Python 3.12+](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![Status: working draft v0.1](https://img.shields.io/badge/Status-working%20draft%20v0.1-orange.svg)](./paper.tex)
[![Target: JMLR / FoCM](https://img.shields.io/badge/Target-JMLR%20%2F%20FoCM-blue.svg)](./paper.tex)
[![DOI](https://img.shields.io/badge/DOI-pending%20Zenodo-blue.svg)](./CITATION.cff)

**Manuscript:** *A universal spectral lower bound on the leave-node-out generalisation error of graph-supervised learning.* Rohan Fossé and Gaël Pallares, CESI LINEACT, 2026. **In preparation for submission to *Journal of Machine Learning Research* (JMLR) or *Foundations of Computational Mathematics* (FoCM).**

This repository develops the foundational theoretical paper of the [cycling-data-lab](https://github.com/cycling-data-lab) structural-bounds research program: a regressor-free, universal lower bound on the expected leave-node-out generalisation error of any graph-supervised learner, together with a matching Berry–Esseen minimax tightness statement. The framework contains the [materials-applicability-bound](https://github.com/cycling-data-lab/materials-applicability-bound) (MLST, in submission) and [mobility-applicability-bound](https://github.com/cycling-data-lab/mobility-applicability-bound) (TR-B, in preparation) results as one-paragraph corollaries.

## Headline result

| Theorem | Statement | Status |
|:---|:---|:---:|
| **Universal lower bound** (Thm 1) | `E[L_{T^c}(f̂)] ≥ (1 - R²_spec(H_d, y)) · Var(y)` — exact in expectation, no concentration slack | proved (notes/01) |
| **Universal upper bound** (Thm 2) | ERM saturates the lower bound to `ρ(Π) · [2 R_n(H_d) + 3 M² √(log(2/η) / (2n))] + O(M²/√n)` | proved (notes/02) |
| **Berry–Esseen minimax tightness** (Thm 3) | No estimator can drive the slack below `Ω(M²/√(N-n))` in the worst case, even with oracle access to `y` on `V` | proved (notes/02) |
| **Cramér–Rao analog** (Cor 1) | The pair of bounds is the graph-supervised-learning analog of `Var(θ̂) ≥ 1/I(θ)` | direct corollary |

The bound is *learner-specific*: `R²_spec(H_d, y) := 1 - L_V(f*_{H_d}) / Var(y)` where `f*_{H_d} := argmin_{f ∈ H_d} L_V(f)` is the population-risk minimiser of the learner's hypothesis class. For closed linear `H_d`, this reduces to the projection-`R²` of `y` on `H_d` in the eigenbasis of the graph Laplacian.

## What's in here

```text
structural-bounds-framework/
├── paper.tex                              # Main manuscript (working draft v0.1, ~12 pages compiled)
├── paper_si.tex                           # Supplementary Information (stub)
├── notes/                                 # Research notes — formal proofs
│   ├── 01_universal_bound_proof.tex         # Theorem 1 (universal LB)
│   ├── 02_minimax_saturation.tex            # Theorem 2 (UB) + Theorem 3 (BE)
│   ├── 03_non_realisable_resolution.tex     # Closure: non-realisable regime is vacuous
│   └── README.md                            # Conventions and reading order
├── references/references.bib              # BibTeX
├── experiments/                           # d01 ... dNN reproducible scripts (stubs)
│   ├── _plot_style.py                       # Paul Tol palette plot helper
│   ├── d01_pilot.py                         # Smoke-test pilot (placeholder)
│   └── README.md                            # Script-numbering convention
├── figures/                               # Publication figures (PDF)
├── outputs/                               # Per-experiment JSON / CSV / NPZ
├── cover_letter.md                        # Cover letter draft
├── .zenodo.json                           # Zenodo deposit metadata
├── CITATION.cff                           # Citation File Format
└── README.md                              # This file
```

The `notes/` directory contains the canonical formal proofs that feed into `paper.tex`. Reading order: notes/01 → notes/02 (errata to notes/01) → notes/03 (closure, withdraws notes/02 Conjecture 1). The manuscript `paper.tex` absorbs the post-closure statements.

## Reproducing the manuscript

```bash
# Build the manuscript
pdflatex paper.tex
bibtex   paper
pdflatex paper.tex
pdflatex paper.tex

# Build the research notes (each compiles standalone)
pdflatex notes/01_universal_bound_proof.tex
pdflatex notes/02_minimax_saturation.tex
pdflatex notes/03_non_realisable_resolution.tex
```

The paper uses standard `article` class (not `iopjournal.cls`, since the target is JMLR / FoCM, not an IOP venue). A class swap at submission time is mechanical.

## Sibling repos in the cycling-data-lab structural-bounds program

- **[materials-applicability-bound](https://github.com/cycling-data-lab/materials-applicability-bound)** — Corollary C1: structural lower bound on the applicability-domain gap (MLST, in submission, [DOI 10.5281/zenodo.20355996](https://doi.org/10.5281/zenodo.20355996)). The MLST proof structure is the operational template for Theorem 2 of the present paper.
- **[mobility-applicability-bound](https://github.com/cycling-data-lab/mobility-applicability-bound)** — Empirical instantiation of Corollary C1 on the 34,858-commune French mobility panel (TR-B, in preparation).
- **[bikeshare-demand-forecasting](https://github.com/cycling-data-lab/bikeshare-demand-forecasting)** — Cross-domain anchor on 27 dock-based bike-share networks under leave-station-out.
- **[bikeshare-gsp-tools](https://github.com/cycling-data-lab/bikeshare-gsp-tools)** — Graph-signal-processing toolkit (spectral bounds, D-optimal siting).

The [organisation README](https://github.com/cycling-data-lab) presents the full program structure with mermaid diagram of corollary dependencies.

## How to cite

A machine-readable citation is provided in [`CITATION.cff`](./CITATION.cff) (rendered as a "Cite this repository" button on GitHub). Plain BibTeX:

```bibtex
@unpublished{FossePallares2026spectralBound,
  author = {Foss\'e, Rohan and Pallares, Ga\"el},
  title  = {A universal spectral lower bound on the leave-node-out
            generalisation error of graph-supervised learning},
  note   = {Manuscript in preparation, CESI LINEACT, 2026.
            \url{https://github.com/cycling-data-lab/structural-bounds-framework}},
  year   = {2026}
}
```

## License

[MIT](./LICENSE).

## Contact

Rohan Fossé — [rfosse@cesi.fr](mailto:rfosse@cesi.fr) — [ORCID](https://orcid.org/0009-0002-2195-0198)
Gaël Pallares — [ORCID](https://orcid.org/0009-0002-8680-604X)
