"""
d01_spectral_projection_figure.py
=================================

Generates Figure 1 of the paper: the spectral projection picture.

Plots, for the 8-task MatBench v0.1 panel, the relationship between
the spectral R^2 of the compositional subspace on the target signal
(R²_spec, x-axis) and the observed leave-node-out gap between the
compositional and categorical encoders (ΔR²_LSO, y-axis).

The bound predicts ΔR²_LSO ≥ R²_spec - O(slack), with equality in
expectation under ERM-on-realisable-witness (Theorem 1 of the
manuscript).  Empirical data points should therefore lie on or
above the y = x reference line, with deviations of order O(M²/√(N-n)).

The figure is the visual headline of the empirical validation
(Section §sec:empirics, Table 1).

Data source: extracted from materials-applicability-bound/outputs/
  - d11_predictive_multitask.json (7 MatBench tasks)
  - d11b_expt_gap.json            (8th task, matbench_expt_gap)
The values are also reported verbatim in Table 1 of the manuscript.

Usage:
    python3.12 experiments/d01_spectral_projection_figure.py

Output:
    figures/fig1_spectral_projection.pdf
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Ensure the script directory is importable for _plot_style.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _plot_style import (  # noqa: E402
    PALETTE,
    FIGSIZE,
    apply_paper_style,
)

SEED = 42  # noqa: F841  (no stochastic step; kept for repo convention)

# ---------------------------------------------------------------------------
# Headline data: 8-task MatBench v0.1 panel, R²_spec and ΔR²_LSO.
# Extracted from materials-applicability-bound/outputs/d11* on 2026-05-24.
# ---------------------------------------------------------------------------
TASKS = [
    # (label,                       N,         R²_spec, ΔR²_LSO)
    ("mp_e_form",                132_752,  0.856,  0.950),
    ("mp_gap",                   106_113,  0.504,  0.812),
    ("perovskites",               18_928,  0.391,  0.500),
    ("log_kvrh",                  10_987,  0.727,  0.842),
    ("log_gvrh",                  10_987,  0.676,  0.830),
    ("phonons",                    1_265,  0.812,  0.940),
    ("dielectric",                 4_764,  0.196, -0.112),
    ("expt_gap",                   4_604,  0.428,  0.705),
]


def main() -> Path:
    apply_paper_style()

    labels = [t[0] for t in TASKS]
    ns = np.array([t[1] for t in TASKS], dtype=float)
    rspecs = np.array([t[2] for t in TASKS], dtype=float)
    deltas = np.array([t[3] for t in TASKS], dtype=float)

    # Spearman ρ for reporting in figure caption.
    # (We avoid scipy import here; trivial rank computation suffices.)
    rspec_ranks = rspecs.argsort().argsort().astype(float)
    delta_ranks = deltas.argsort().argsort().astype(float)
    rho_spearman = float(
        np.corrcoef(rspec_ranks, delta_ranks)[0, 1]
    )

    fig, ax = plt.subplots(figsize=FIGSIZE["single"])

    # y = x reference line: the bound's headline prediction in
    # expectation under saturating ERM.
    lim_lo, lim_hi = -0.2, 1.05
    ax.plot(
        [lim_lo, lim_hi], [lim_lo, lim_hi],
        color="#888888", linestyle="--", linewidth=1.0, zorder=1,
        label=r"$y = x$ (bound saturated)",
    )

    # Marker size proportional to log10(N) for visual cue of dataset
    # scale; capped to keep figure readable.
    sizes = 20.0 + 25.0 * (np.log10(ns) - np.log10(ns).min())

    # Colour: blue for ΔR² > 0 (positive gap), red for ΔR² < 0
    # (negative gap; the dielectric outlier).
    colours = [PALETTE[0] if d >= 0 else PALETTE[1] for d in deltas]

    ax.scatter(
        rspecs, deltas,
        s=sizes,
        c=colours,
        edgecolors="#222222",
        linewidth=0.6,
        zorder=3,
    )

    # Task labels, offset to avoid overlapping the markers.
    label_offsets = {
        "mp_e_form":  (0.02, 0.00),
        "mp_gap":     (0.02, -0.02),
        "perovskites":(0.02, 0.02),
        "log_kvrh":   (0.02, 0.00),
        "log_gvrh":   (-0.02, -0.07),
        "phonons":    (-0.10, 0.03),
        "dielectric": (0.02, -0.06),
        "expt_gap":   (0.02, 0.00),
    }
    for label, x, y in zip(labels, rspecs, deltas, strict=True):
        dx, dy = label_offsets.get(label, (0.02, 0.00))
        ax.annotate(
            label,
            xy=(x, y),
            xytext=(x + dx, y + dy),
            fontsize=7,
            color="#444444",
            zorder=4,
        )

    ax.set_xlim(lim_lo, lim_hi)
    ax.set_ylim(lim_lo, lim_hi)
    ax.set_xlabel(r"$R^2_{\mathrm{spec}}(\mathcal{H}_d, \mathbf{y})$")
    ax.set_ylabel(r"$\Delta R^2_{\mathrm{LSO}}$ (compositional $-$ categorical)")
    ax.set_title(
        rf"Spearman $\rho = {rho_spearman:+.3f}$  "
        rf"(exact $p = 4.96\times10^{{-5}}$, $n = 8$)",
        loc="left",
    )
    ax.legend(loc="lower right", frameon=True, fancybox=False)

    # Save to figures/.
    out_path = Path(__file__).resolve().parent.parent / "figures" / "fig1_spectral_projection.pdf"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)

    print(f"Wrote {out_path}  (Spearman ρ = {rho_spearman:+.3f})")
    return out_path


if __name__ == "__main__":
    main()
