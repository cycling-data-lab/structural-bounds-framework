# `experiments/` — numbered, reproducible scripts

Every experimental result reported in the manuscript is produced by exactly one numbered script in this directory.  The convention :

```
d{NN}_{short_name}.py
```

where :

- `NN` is a zero-padded two-digit number (`d01`, `d02`, …, `d24`, `d99`).  Numbering reflects the **order in which experiments were added**, not the order in which they appear in the paper.  This lets the project grow incrementally without renaming.
- `short_name` is a short snake_case description of what the script does (e.g. `d05_rspec_matbench`, `d18_shuffled_knn_null`).

## What every script must do

1. **Read from a known cache directory** (`outputs/` by default, override via env var or argparse).
2. **Pin `SEED = 42`** in every stochastic step.  Override only for explicit seed-stability checks (e.g. `seed_r = SEED * 1000 + r`).
3. **Write structured output** to `outputs/d{NN}_{short_name}.{json,csv,npz}` so that downstream figure-generation scripts can read it deterministically.
4. **Print a one-line per-step progress** to stdout (`flush=True` if running long), and a checkpoint JSON after each major step so the run is restartable.
5. **Document any non-trivial design decision in a header docstring**.

## Scripts in this repository

|ID|Purpose|Output|
|:---:|:---|:---|
| d01 | Spectral-projection picture: scatter of R²_spec vs ΔR²_LSO on the 8-task MatBench panel | `figures/fig1_spectral_projection.pdf` |
| d02 | Slack-rate comparison: rho/sqrt(n) vs transductive vs Berry-Esseen | `figures/fig2_slack_comparison.pdf` |

The 8-task headline data referenced in `d01` is extracted verbatim from `materials-applicability-bound/outputs/d11_predictive_multitask.json` and `d11b_expt_gap.json`. No new computation is performed in this repo's `d01` — it is purely a re-presentation of the empirical anchors from the MLST companion paper.

For full reproducibility of the empirical numbers (Spearman computations, permutation tests, partial Spearman bootstraps, CIG ratios), see the per-row reproducibility map in the SI (`paper_si.tex` §D), which names the exact script per row of Table 1.

## Recommended numbered backbone (for future extensions)

A complete paper typically has the following scripts.  Use this as a checklist :

|ID|Purpose|Notes|
|:---:|:---|:---|
| d03 | Empirical-validation re-runner (consolidates Tier 1 numbers from sibling repos) | Reads upstream `outputs/d*.json` from `materials-applicability-bound`, `mobility-applicability-bound`, `bikeshare-demand-forecasting` |
| d04 | Negative-transfer (C2) empirical anchor on QM9 → MatBench task pair | Validates Theorem 6 (spectral-disjointness lower bound) |
| d05 | Active-learning (C3) empirical anchor: leverage-score sampling vs uniform LSO | Validates Theorem 7 (parametric 1/n rate) |
| d06 | Fano multi-point lower bound tightness numerical exploration | Validates the sketch in notes/04 §4 |
| d07 | Sensitivity sweep: k-NN graph parameter, regulariser, regressor family | Robustness anchor |
| ... | (extend as the paper grows) | |

## Plot style

All figures should import `_plot_style.py` and call `apply_paper_style()` at the top.  This sets the Paul Tol bright palette (colour-blind safe), sans-serif fonts, and the standard figure-size dictionary.  See `d01_pilot.py` for the recommended pattern.

## Cache files

Caches (precomputed features, eigenvector dumps, shuffled-null realisations) live under `outputs/_*.npz` or `outputs/_*.parquet` and are `.gitignore`d.  The first run of a downstream script regenerates them deterministically.  Per-run logs go under `logs/` (also gitignored).
