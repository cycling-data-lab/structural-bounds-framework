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

## Recommended numbered backbone

A complete paper typically has the following scripts.  Use this as a checklist :

| ID  | Purpose | Notes |
|:---:|:---|:---|
| d01 | Pilot / smoke test on a small subset of the data | Verifies the pipeline end-to-end before scaling |
| d02 | Full predictive validation (the headline number) | Master experiment |
| d03 | Robustness check #1 (e.g. polymorphism / temporal heterogeneity decomposition) | Eve's law-style variance decomposition |
| d04 | Robustness check #2 (e.g. seed stability, regressor independence) | Confounder audit |
| d05 | Encoder discrimination / oracle test | Foundation-model comparison if applicable |
| d06 | Falsifiability test against a topology-matched null | CIG ratio + exact permutation $p$-value |
| d07 | Figure generator | Reads d02–d06 outputs, writes `figures/*.pdf` |
| ... | (extend as the paper grows) | |

## Plot style

All figures should import `_plot_style.py` and call `apply_paper_style()` at the top.  This sets the Paul Tol bright palette (colour-blind safe), sans-serif fonts, and the standard figure-size dictionary.  See `d01_pilot.py` for the recommended pattern.

## Cache files

Caches (precomputed features, eigenvector dumps, shuffled-null realisations) live under `outputs/_*.npz` or `outputs/_*.parquet` and are `.gitignore`d.  The first run of a downstream script regenerates them deterministically.  Per-run logs go under `logs/` (also gitignored).
