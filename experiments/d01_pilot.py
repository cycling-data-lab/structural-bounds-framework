"""
d01_pilot.py — Pilot / smoke-test script for {{repo-name}}.

This is the FIRST script you should write for a new paper.  It :

  1. Reads (or generates) a small toy dataset.
  2. Runs the simplest possible version of the headline analysis.
  3. Writes a JSON output to outputs/d01_pilot.json.
  4. Generates a sanity-check figure to figures/fig_d01_pilot.pdf.

The goal is end-to-end verification of the data → analysis → figure
pipeline BEFORE scaling to the full panel.  If d01 runs in under a
minute and produces a non-trivial figure, the downstream d02+ scripts
can safely be wired in.

Output :
  outputs/d01_pilot.json    -- structured per-step results
  figures/fig_d01_pilot.pdf -- sanity-check figure (gitignored under
                                figures/_*.pdf if you want)
"""
from __future__ import annotations
import json
import sys
import time
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"
FIG = ROOT / "figures"
OUT.mkdir(exist_ok=True)
FIG.mkdir(exist_ok=True)

sys.path.insert(0, str(ROOT / "experiments"))
from _plot_style import apply_paper_style, PALETTE, FIGSIZE  # noqa: E402

apply_paper_style()

SEED = 42


def synthetic_pilot(n: int = 200) -> dict:
    """Generate a tiny synthetic dataset + run a tiny analysis.

    Replace this body with the real pilot experiment for your paper.
    """
    rng = np.random.default_rng(SEED)
    x = np.linspace(0.0, 10.0, n)
    y_true = np.sin(x)
    y_obs = y_true + rng.normal(scale=0.2, size=n)
    # A meaningless toy estimate so the JSON has structure :
    rmse = float(np.sqrt(np.mean((y_obs - y_true) ** 2)))
    return {"n": int(n), "rmse_toy": rmse,
            "x": x.tolist(), "y_obs": y_obs.tolist(),
            "y_true": y_true.tolist()}


def main():
    t0 = time.time()
    print("=" * 72)
    print("d01_pilot — smoke-test of the data → analysis → figure pipeline")
    print("=" * 72)

    result = synthetic_pilot()
    print(f"  n = {result['n']}, toy RMSE = {result['rmse_toy']:.4f}",
          flush=True)

    # Save structured output (figure scripts will read this).
    out_path = OUT / "d01_pilot.json"
    out_path.write_text(json.dumps(
        {k: v for k, v in result.items() if k not in {"x", "y_obs", "y_true"}},
        indent=2))
    print(f"  ✓ saved {out_path.name}", flush=True)

    # Generate a sanity-check figure.
    fig, ax = plt.subplots(figsize=FIGSIZE["single"])
    ax.scatter(result["x"], result["y_obs"], s=6, color=PALETTE[0],
                label="observed", alpha=0.6, zorder=2)
    ax.plot(result["x"], result["y_true"], color=PALETTE[1],
             lw=1.8, label="ground truth", zorder=3)
    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$y$")
    ax.set_title("d01 pilot : synthetic sin($x$) + Gaussian noise")
    ax.legend(loc="upper right")
    plt.tight_layout()
    fig_path = FIG / "fig_d01_pilot.pdf"
    plt.savefig(fig_path)
    plt.close(fig)
    print(f"  ✓ saved {fig_path.name}", flush=True)

    print(f"\n✓ d01 done in {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
