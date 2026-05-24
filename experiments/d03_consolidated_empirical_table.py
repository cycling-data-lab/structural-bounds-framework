"""
d03_consolidated_empirical_table.py
===================================

Programmatically regenerates the consolidated cross-domain
empirical table (Table 1 of the main paper) by reading the
per-experiment JSON outputs from the sibling cycling-data-lab
repositories.

For each Tier-1 row, the script:
  - Locates the upstream JSON in the named sibling repository.
  - Extracts the relevant numeric fields (n, R^2_spec, Delta R^2_LSO).
  - Renders the row in LaTeX-table-ready format on stdout.

The output is intended to be visually inspected against the
hand-typed Table 1 in paper.tex; any drift between this script's
output and the manuscript table is a maintenance bug.

Usage (default: print to stdout):
    python3.12 experiments/d03_consolidated_empirical_table.py

Output:
    LaTeX table rows (8 MatBench + 4 cross-domain pilots).
    Also writes outputs/d03_consolidated_table.json with the
    full structured data.

Reads:
    ../materials-applicability-bound/outputs/d11_predictive_multitask.json
    ../materials-applicability-bound/outputs/d11b_expt_gap.json
    ../materials-applicability-bound/outputs/d01_movielens_pilot.json
    ../materials-applicability-bound/outputs/d04_qsar_pilot.json
    ../materials-applicability-bound/outputs/d03_aflow_pilot.json

Assumes the sibling repositories are checked out under the same
parent directory as structural-bounds-framework (default
cycling-data-lab layout).  Adjust SIBLING_ROOT if your layout differs.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

SEED = 42  # noqa: F841

REPO_ROOT = Path(__file__).resolve().parent.parent
SIBLING_ROOT = REPO_ROOT.parent  # /Users/.../cesi-research/
MLST_OUTPUTS = SIBLING_ROOT / "materials-applicability-bound" / "outputs"


def _load_json(path: Path) -> dict:
    if not path.exists():
        print(f"  [warning] missing upstream JSON: {path}", file=sys.stderr)
        return {}
    with path.open("r") as f:
        return json.load(f)


def gather_matbench_rows() -> list[dict]:
    """Read the 7-task d11 + the 8th-task d11b JSON; return 8 rows."""
    rows: list[dict] = []
    d11 = _load_json(MLST_OUTPUTS / "d11_predictive_multitask.json")
    for task, data in d11.items():
        if task.startswith("_"):
            continue
        rows.append({
            "domain": "MatBench v0.1",
            "task": task,
            "n": data.get("n"),
            "rspec": data.get("r_spec"),
            "delta": data.get("delta"),
            "source": "d11",
        })

    d11b = _load_json(MLST_OUTPUTS / "d11b_expt_gap.json")
    if d11b:
        rows.append({
            "domain": "MatBench v0.1",
            "task": d11b.get("task", "matbench_expt_gap"),
            "n": d11b.get("n_materials"),
            "rspec": d11b.get("r_spec_ols"),
            "delta": d11b.get("delta_r2_lso_mean"),
            "source": "d11b",
        })
    return rows


def gather_cross_domain_rows() -> list[dict]:
    """Cross-domain confirmation pilots (MovieLens, QSAR, AFLOW)."""
    rows: list[dict] = []

    movielens = _load_json(MLST_OUTPUTS / "d01_movielens_pilot.json")
    if movielens:
        s = movielens.get("summary", {})
        rows.append({
            "domain": "MovieLens",
            "task": "user-rating LSO",
            "n": None,
            "rspec": None,
            "delta": s.get("mean_R2_lso_comp"),
            "source": "d01",
        })

    qsar = _load_json(MLST_OUTPUTS / "d04_qsar_pilot.json")
    if qsar:
        s = qsar.get("summary", {})
        rows.append({
            "domain": "QSAR",
            "task": "molecular-activity LSO",
            "n": None,
            "rspec": None,
            "delta": s.get("mean_delta_R2_lso"),
            "source": "d04",
        })

    aflow = _load_json(MLST_OUTPUTS / "d03_aflow_pilot.json")
    if aflow:
        s = aflow.get("summary", {})
        for task in ("log10_bulk_modulus", "log10_shear_modulus"):
            task_data = s.get(task)
            if task_data:
                rows.append({
                    "domain": "AFLOW",
                    "task": task,
                    "n": None,
                    "rspec": None,
                    "delta": task_data.get("mean_delta_R2_lso"),
                    "source": "d03",
                })

    return rows


def _fmt_n(n) -> str:
    if n is None:
        return "---"
    if isinstance(n, (int, float)) and n >= 1000:
        return "{:,}".format(int(n)).replace(",", "{,}")
    return str(n)


def _fmt_num(x, fmt: str = "{:.3f}") -> str:
    if x is None:
        return "---"
    try:
        return fmt.format(float(x))
    except (TypeError, ValueError):
        return "---"


def render_latex_rows(rows: list[dict]) -> str:
    """LaTeX-table-ready row format matching paper.tex Table 1."""
    lines: list[str] = []
    for r in rows:
        task = r["task"].replace("_", "\\_")
        lines.append(
            f"  {task:<35s} & "
            f"{_fmt_n(r['n']):>10s} & "
            f"{_fmt_num(r['rspec']):>5s} & "
            f"{_fmt_num(r['delta'], '{:+.3f}'):>7s} & "
            f"{r['source']:<6s} \\\\"
        )
    return "\n".join(lines)


def main() -> None:
    matbench = gather_matbench_rows()
    cross = gather_cross_domain_rows()
    all_rows = matbench + cross

    output_data = {
        "n_matbench_tasks": len(matbench),
        "n_cross_domain_pilots": len(cross),
        "rows": all_rows,
    }

    out_json = REPO_ROOT / "outputs" / "d03_consolidated_table.json"
    out_json.parent.mkdir(parents=True, exist_ok=True)
    with out_json.open("w") as f:
        json.dump(output_data, f, indent=2)

    print("=" * 70)
    print("  Consolidated empirical Table 1 -- regenerated from sibling repos")
    print("=" * 70)
    print()
    print("MatBench v0.1 panel:")
    print(render_latex_rows(matbench))
    print()
    print("Cross-domain pilots:")
    print(render_latex_rows(cross))
    print()
    print(f"  -> Wrote structured output: {out_json}")
    print()
    print("Notes:")
    print(f"  - MatBench rows: {len(matbench)} (expected 8)")
    print(f"  - Cross-domain pilots: {len(cross)} (expected 4)")
    print("  - Hand-typed Table 1 in paper.tex should match these rows.")
    print("  - Any drift is a maintenance bug; rerun this script after")
    print("    any upstream d11/d11b/d01/d04/d03 update in materials-")
    print("    applicability-bound.")


if __name__ == "__main__":
    main()
