"""
d01_pilot.py — Self-contained numerical verification of Theorem 1
(universal spectral lower bound) and the Theorem 2 saturation behaviour
on a synthetic graph-supervised regression problem.

WHAT THIS IS (and is not)
-------------------------
This script is a stand-alone *sanity check of the theorem itself*, not a
domain validation.  It builds a synthetic k-NN similarity graph, a
bandlimited hypothesis class H_d = span of the bottom-d Laplacian
eigenvectors, and a centred target signal, then verifies numerically
that an empirical-risk-minimising (ERM) learner restricted to H_d obeys

    E_T[ L_{T^c}(f-hat) ]  >=  (1 - R^2_spec(H_d, y)) * Var(y)         (Thm 1)

over uniform leave-node-out splits, and that the held-out error stays a
*small* (Theorem-2-style) slack above this floor rather than far above
it.  It runs A-to-Z inside this repository with no external data and no
sibling-repo dependency.

The MatBench / mobility / bikeshare numbers reported in the manuscript
come from the companion repositories (see paper Section 8); this pilot
does NOT reproduce those — it only confirms the mathematics of the floor
on a controlled synthetic instance.

Output:
  outputs/d01_pilot.json    -- floor vs. empirical held-out loss per dim
  figures/fig_d01_pilot.pdf -- Thm-1 floor and ERM held-out loss vs. d
"""
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

os.environ.setdefault("MPLBACKEND", "Agg")  # headless-safe before pyplot

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
N = 400          # nodes
K_NN = 10        # neighbours in the similarity graph
ALPHA = 0.8      # train fraction n/N (proportional regime, A3)
N_SPLITS = 300   # Monte-Carlo leave-node-out splits
D_GRID = [2, 4, 8, 16, 32, 64]  # hypothesis-class dimensions to sweep


def build_knn_laplacian(rng: np.random.Generator) -> np.ndarray:
    """Symmetric-normalised Laplacian of a Gaussian-weighted k-NN graph."""
    pos = rng.random((N, 2))
    d2 = np.sum((pos[:, None, :] - pos[None, :, :]) ** 2, axis=-1)
    np.fill_diagonal(d2, np.inf)
    sigma2 = np.median(np.sort(d2, axis=1)[:, K_NN - 1])  # local bandwidth
    W = np.zeros((N, N))
    nn = np.argsort(d2, axis=1)[:, :K_NN]
    for i in range(N):
        for j in nn[i]:
            w = float(np.exp(-d2[i, j] / sigma2))
            W[i, j] = W[j, i] = max(W[i, j], w)  # symmetrise (OR)
    deg = W.sum(axis=1)
    dinv2 = 1.0 / np.sqrt(np.maximum(deg, 1e-12))
    L = np.eye(N) - (dinv2[:, None] * W) * dinv2[None, :]
    return 0.5 * (L + L.T)  # numerically symmetric


def make_signal(evecs: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """Centred target with energy spread across the spectrum (R^2 in (0,1))."""
    k = np.arange(N)
    coeffs = np.exp(-k / 12.0) + 0.15 * rng.standard_normal(N) * np.exp(-k / 80.0)
    y = evecs @ coeffs
    y = y - y.mean()  # enforce 1^T y = 0 (Assumption 1)
    return y


def main() -> None:
    t0 = time.time()
    print("=" * 72)
    print("d01_pilot — numerical verification of Theorem 1 (LB) + Thm 2 slack")
    print("=" * 72)

    rng = np.random.default_rng(SEED)
    L = build_knn_laplacian(rng)
    evals, evecs = np.linalg.eigh(L)  # ascending eigenvalues
    y = make_signal(evecs, rng)
    var_y = float(y @ y / N)
    M = float(np.max(np.abs(y)))
    coeffs = evecs.T @ y                      # graph-Fourier coefficients
    energy = coeffs ** 2
    total_energy = float(energy.sum())

    n = int(round(ALPHA * N))
    rows = []
    print(f"\n  N={N}, k-NN={K_NN}, alpha={ALPHA} (n={n}), splits={N_SPLITS}")
    print(f"  Var(y)={var_y:.4f}, ||y||_inf=M={M:.3f}\n")
    print(f"  {'d':>4} {'R2_spec':>8} {'floor':>10} {'E[L_Tc]':>10} "
          f"{'slack':>9} {'Thm1 ok':>8}")

    for d in D_GRID:
        B = evecs[:, :d]                       # orthonormal basis of H_d
        r2_spec = float(energy[:d].sum() / total_energy)
        floor = (1.0 - r2_spec) * var_y

        losses = np.empty(N_SPLITS)
        for s in range(N_SPLITS):
            perm = rng.permutation(N)
            T, Tc = perm[:n], perm[n:]
            beta, *_ = np.linalg.lstsq(B[T], y[T], rcond=None)  # ERM on T
            f_hat = B @ beta
            losses[s] = float(np.mean((f_hat[Tc] - y[Tc]) ** 2))

        emp = float(losses.mean())
        emp_se = float(losses.std(ddof=1) / np.sqrt(N_SPLITS))
        slack = emp - floor
        holds = emp >= floor - 2 * emp_se      # Thm 1, within MC error
        rows.append({
            "d": d, "r2_spec": r2_spec, "floor": floor,
            "emp_mean_L_Tc": emp, "emp_se": emp_se,
            "slack": slack, "thm1_holds": holds,
        })
        print(f"  {d:>4} {r2_spec:>8.3f} {floor:>10.4f} {emp:>10.4f} "
              f"{slack:>+9.4f} {str(holds):>8}")

    all_hold = all(r["thm1_holds"] for r in rows)
    out = {
        "description": "Synthetic verification of Thm 1 lower bound + Thm 2 "
                       "saturation slack (NOT a real-domain validation).",
        "seed": SEED, "N": N, "k_nn": K_NN, "alpha": ALPHA,
        "n_splits": N_SPLITS, "var_y": var_y, "M": M,
        "rows": rows, "thm1_holds_all_dims": all_hold,
    }
    out_path = OUT / "d01_pilot.json"
    out_path.write_text(json.dumps(out, indent=2))
    print(f"\n  Theorem 1 holds at every dimension: {all_hold}")
    print(f"  ✓ saved {out_path.name}")

    # Figure: floor and ERM held-out loss vs. hypothesis-class dimension.
    ds = [r["d"] for r in rows]
    floors = [r["floor"] for r in rows]
    emps = [r["emp_mean_L_Tc"] for r in rows]
    ses = [r["emp_se"] for r in rows]

    fig, ax = plt.subplots(figsize=FIGSIZE["single"])
    ax.plot(ds, floors, "o-", color=PALETTE[0], lw=1.8,
            label=r"floor $(1-R^2_{\mathrm{spec}})\,\mathrm{Var}(y)$ (Thm 1)")
    ax.errorbar(ds, emps, yerr=[2 * s for s in ses], fmt="s--",
                color=PALETTE[1], lw=1.8, capsize=2,
                label=r"ERM held-out $\mathbb{E}_T[L_{T^c}]$ (Thm 2)")
    ax.axhline(var_y, color=PALETTE[6], lw=1.0, ls=":",
               label=r"$\mathrm{Var}(y)$")
    ax.set_xscale("log", base=2)
    ax.set_xlabel(r"hypothesis-class dimension $d$")
    ax.set_ylabel("leave-node-out MSE")
    ax.set_title("Thm 1 floor vs. ERM held-out error (synthetic graph)")
    ax.legend(loc="upper right", fontsize=7)
    plt.tight_layout()
    fig_path = FIG / "fig_d01_pilot.pdf"
    plt.savefig(fig_path)
    plt.close(fig)
    print(f"  ✓ saved {fig_path.name}")

    print(f"\n✓ d01 done in {time.time() - t0:.1f}s")
    if not all_hold:
        sys.exit("Theorem 1 violated — investigate before trusting downstream.")


if __name__ == "__main__":
    main()
