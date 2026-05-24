# structural-bounds-framework

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/license/MIT)
[![Python 3.12+](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![Status: working draft v0.4](https://img.shields.io/badge/Status-working%20draft%20v0.4-orange.svg)](./paper.tex)
[![Target: JMLR / FoCM](https://img.shields.io/badge/Target-JMLR%20%2F%20FoCM-blue.svg)](./paper.tex)
[![DOI](https://img.shields.io/badge/DOI-pending%20Zenodo-blue.svg)](./CITATION.cff)

**Manuscript:** *A universal spectral lower bound on the leave-node-out generalisation error of graph-supervised learning.* Rohan Fossé and Gaël Pallares, CESI LINEACT, 2026. **In preparation for submission to *Journal of Machine Learning Research* (JMLR) or *Foundations of Computational Mathematics* (FoCM).**

This repository develops the foundational theoretical paper of the [cycling-data-lab](https://github.com/cycling-data-lab) structural-bounds research program: a regressor-free, universal lower bound on the expected leave-node-out generalisation error of any graph-supervised learner, together with a matching Berry–Esseen minimax tightness statement. The framework contains the [materials-applicability-bound](https://github.com/cycling-data-lab/materials-applicability-bound) (MLST, in submission) and [mobility-applicability-bound](https://github.com/cycling-data-lab/mobility-applicability-bound) (TR-B, in preparation) results as one-paragraph corollaries.

## Headline result

| Theorem | Statement | Status |
| :---    | :---      | :---:  |
| **Universal lower bound** (Thm 1) | `E[L_{T^c}(f̂)] ≥ (1 - R²_spec(H_d, y)) · Var(y)` — exact in expectation, no concentration slack | proved (notes/01) |
| **Universal upper bound** (Thm 2, sharp transductive form) | ERM saturates the lower bound to `2·R^trans_n(H_d) + 5.05·M²·√((n+u)·log(2/η)/(n·u))`; rho factor eliminated via El-Yaniv-Pechyony 2006 (notes/04) | proved (notes/02, 04) |
| **Berry–Esseen minimax tightness** (Thm 3) | No estimator can drive the slack below `Ω(M²/√(N-n))` in the worst case, even with oracle access to `y` on `V` | proved (notes/02) |
| **Cramér–Rao analog** (Cor 1) | The pair of bounds is the graph-supervised-learning analog of `Var(θ̂) ≥ 1/I(θ)`; rates and constants match to a factor ≤ 10 | direct corollary |
| **Negative transfer** (Thm 6, Cor 2 = C2) | Under spectral disjointness, `E[NT] ≥ (‖P_{H_d}y_src‖² + ‖P_{H_d}y_tgt‖²)/n_t`; transfer is unavoidably harmful | proved (paper §C2) |
| **Active learning** (Thm 7, Cor C3) | Importance-weighted leverage-score sampling achieves rate `O(M²·√(d·N·log(1/η))/n)` — parametric `1/n` instead of passive `1/√n` | proved (paper §C3) |

The bound is *learner-specific*: `R²_spec(H_d, y) := 1 - L_V(f*_{H_d}) / Var(y)` where `f*_{H_d} := argmin_{f ∈ H_d} L_V(f)` is the population-risk minimiser of the learner's hypothesis class. For closed linear `H_d`, this reduces to the projection-`R²` of `y` on `H_d` in the eigenbasis of the graph Laplacian.

## What's in here

```text
structural-bounds-framework/
├── paper.tex                              # Main manuscript (working draft v0.4, 20 pages, C1+C2+C3 full, 2 figures, full empirical section)
├── paper.pdf                              # Compiled manuscript (regenerable via pdflatex)
├── paper_si.tex                           # Supplementary Information (5 appendices, 5 pages compiled)
├── paper_si.pdf                           # Compiled SI
├── paper_si.tex                           # Supplementary Information (stub)
├── notes/                                 # Research notes — formal proofs
│   ├── 01_universal_bound_proof.tex         # Theorem 1 (universal LB)
│   ├── 02_minimax_saturation.tex            # Theorem 2 (UB) + Theorem 3 (BE)
│   ├── 03_non_realisable_resolution.tex     # Closure: non-realisable regime is vacuous
│   ├── 04_sharp_transductive_constant.tex   # Sharp transductive constant via El-Yaniv-Pechyony
│   └── README.md                            # Conventions and reading order
├── references/references.bib              # BibTeX
├── experiments/                           # d01 ... dNN reproducible scripts (stubs)
│   ├── _plot_style.py                       # Paul Tol palette plot helper
│   ├── d01_pilot.py                         # Smoke-test pilot (placeholder)
│   └── README.md                            # Script-numbering convention
├── figures/                               # Publication figures (PDF)
│   ├── fig1_spectral_projection.pdf         # Headline: R²_spec vs ΔR²_LSO scatter (8 MatBench tasks)
│   └── fig2_slack_comparison.pdf            # Slack-rate comparison: rho/sqrt(n) vs transductive vs Berry-Esseen
├── outputs/                               # Per-experiment JSON / CSV / NPZ
├── cover_letter.md                        # Cover letter draft
├── .zenodo.json                           # Zenodo deposit metadata
├── CITATION.cff                           # Citation File Format
└── README.md                              # This file
```

The `notes/` directory contains the canonical formal proofs that feed into `paper.tex`. Reading order: notes/01 → notes/02 (errata to notes/01) → notes/03 (closure, withdraws notes/02 Conjecture 1). The manuscript `paper.tex` absorbs the post-closure statements.

## Reproducing the manuscript

```bash
# Build the manuscript (run from repo root)
pdflatex paper.tex
bibtex   paper
pdflatex paper.tex
pdflatex paper.tex

# Build the Supplementary Information
pdflatex paper_si.tex
bibtex   paper_si
pdflatex paper_si.tex
pdflatex paper_si.tex

# Build the research notes (notes/01–03 standalone, notes/04 needs bibtex)
pdflatex notes/01_universal_bound_proof.tex
pdflatex notes/02_minimax_saturation.tex
pdflatex notes/03_non_realisable_resolution.tex
( cd notes && pdflatex 04_sharp_transductive_constant.tex \
            && bibtex 04_sharp_transductive_constant \
            && pdflatex 04_sharp_transductive_constant.tex \
            && pdflatex 04_sharp_transductive_constant.tex )

# Regenerate figures (uses matplotlib + Paul Tol palette in _plot_style.py)
python3.12 experiments/d01_spectral_projection_figure.py
python3.12 experiments/d02_slack_comparison_figure.py
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
