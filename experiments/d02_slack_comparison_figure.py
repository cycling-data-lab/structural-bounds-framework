"""
d02_slack_comparison_figure.py
==============================

Generates Figure 2 of the paper: the slack-comparison picture.

Shows, as a function of the train/test split ratio n/N, the
multiplicative gap between three slack rates that appear in
the program:

  (a) Original Theorem 2 (Mohri 3.7 + transduction identity):
        slack proportional to rho(Pi) / sqrt(n),
        where rho(Pi) = N/(N-n).
  (b) Sharp transductive Theorem 2 (El-Yaniv-Pechyony 2006):
        slack proportional to sqrt((n + u) / (n*u)) = sqrt(1/n + 1/u).
  (c) Berry-Esseen lower bound (notes/02 / paper Theorem 3):
        slack proportional to 1 / sqrt(N - n) = 1 / sqrt(u).

The (a)/(c) ratio is exactly sqrt(rho - 1), which the transductive
upgrade eliminates: (b)/(c) is bounded by a small constant.

This visualises the value-add of notes/04 (sharp transductive
constant): the rho factor in the original Theorem 2 is loose
by sqrt(rho - 1) approximately 2x at the standard 80/20 split.

Usage:
    python3.12 experiments/d02_slack_comparison_figure.py

Output:
    figures/fig2_slack_comparison.pdf
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _plot_style import (  # noqa: E402
    PALETTE,
    FIGSIZE,
    apply_paper_style,
)

SEED = 42  # noqa: F841

N = 1000  # population size; results are scale-invariant


def main() -> Path:
    apply_paper_style()

    n_over_N_grid = np.linspace(0.05, 0.95, 91)
    n_grid = (n_over_N_grid * N).astype(int)
    u_grid = N - n_grid
    rho_grid = N / u_grid.astype(float)

    # (a) Original Theorem 2: rho / sqrt(n).  Drop the constant
    # (M^2, log(2/eta) factors etc.) since the y-axis is unitless.
    slack_a = rho_grid / np.sqrt(n_grid.astype(float))

    # (b) Sharp transductive Theorem 2: sqrt(1/n + 1/u).
    slack_b = np.sqrt(1.0 / n_grid + 1.0 / u_grid)

    # (c) Berry-Esseen lower bound: 1 / sqrt(u).
    slack_c = 1.0 / np.sqrt(u_grid.astype(float))

    # Normalise so (c) = 1 at n/N = 0.8 for visual readability.
    norm_idx = int(np.argmin(np.abs(n_over_N_grid - 0.8)))
    scale = 1.0 / slack_c[norm_idx]
    slack_a *= scale
    slack_b *= scale
    slack_c *= scale

    fig, ax = plt.subplots(figsize=FIGSIZE["wide"])

    ax.plot(
        n_over_N_grid, slack_a,
        color=PALETTE[1], linestyle="-", linewidth=1.8,
        label=(r"(a) Original Thm 2 (Mohri + transduction):"
               r"$\ \rho(\Pi)/\sqrt{n}$"),
        zorder=2,
    )
    ax.plot(
        n_over_N_grid, slack_b,
        color=PALETTE[0], linestyle="-", linewidth=1.8,
        label=(r"(b) Sharp transductive Thm 2"
               r"\ (El-Yaniv-Pechyony 2006)"),
        zorder=3,
    )
    ax.plot(
        n_over_N_grid, slack_c,
        color=PALETTE[2], linestyle="--", linewidth=1.4,
        label=(r"(c) Berry-Esseen lower bound:"
               r"$\ 1/\sqrt{N-n}$"),
        zorder=2,
    )

    ax.axvline(0.8, color="#888888", linestyle=":", linewidth=0.8,
               zorder=1)
    ax.text(0.81, 4.2, "80/20 split", fontsize=8, color="#666666",
            rotation=90, va="top")

    ax.set_xlabel(r"Train fraction $n / N$")
    ax.set_ylabel(r"Slack (normalised, $N = 1000$)")
    ax.set_title(
        "Slack-rate comparison: "
        r"the $\sqrt{\rho - 1}$ inflation eliminated "
        "by transductive Rademacher",
        loc="left",
    )
    ax.legend(loc="upper left", fontsize=8, frameon=True, fancybox=False)
    ax.set_ylim(0, 6)
    ax.set_xlim(0, 1)

    # Annotate (a)/(c) ratio at 80/20 = sqrt(rho - 1) = sqrt(4) = 2.
    rho_80 = N / (N - 0.8 * N)
    sqrt_rho_minus_1 = np.sqrt(rho_80 - 1.0)
    ax.annotate(
        rf"$\sqrt{{\rho - 1}} = {sqrt_rho_minus_1:.1f}\times$ gap at 80/20",
        xy=(0.8, slack_a[norm_idx]),
        xytext=(0.55, 4.3),
        fontsize=8, color="#444444",
        arrowprops=dict(arrowstyle="->", color="#666666",
                        connectionstyle="arc3,rad=0.2", linewidth=0.6),
    )

    out_path = (
        Path(__file__).resolve().parent.parent
        / "figures" / "fig2_slack_comparison.pdf"
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)

    print(
        f"Wrote {out_path}  "
        f"(sqrt(rho - 1) gap at n/N = 0.8: {sqrt_rho_minus_1:.2f}x)"
    )
    return out_path


if __name__ == "__main__":
    main()
