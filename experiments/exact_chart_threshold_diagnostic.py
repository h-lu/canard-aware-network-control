#!/usr/bin/env python3
"""Generate the exact-chart finite-section threshold diagnostic.

Run from the repository root with

    PYTHONPATH=src python experiments/exact_chart_threshold_diagnostic.py

The JSON and Markdown files are numerical evidence only.  They are not a
certificate for invariant histories or for the maximal-canard theorem.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
from pathlib import Path

import numpy as np
import scipy

from canard_control.exact_chart_threshold_diagnostic import (
    ExactChartParameters,
    alpha_value,
    threshold_coefficient_row,
)


DEFAULT_SCHEDULE = (
    (0.12, 2.50),
    (0.08, 2.75),
    (0.05, 3.00),
    (0.01, 4.00),
    (0.005, 4.50),
    (0.0025, 5.00),
)

QUICK_SCHEDULE = (
    (0.08, 2.75),
    (0.02, 3.50),
    (0.005, 4.50),
)

ARCHIVE_JSON = Path(
    "experiments/results/exact_chart_threshold_convergence.json"
)
ARCHIVE_MARKDOWN = Path("docs/exact-chart-threshold-diagnostic.md")
QUICK_JSON = Path("build/diagnostics/exact_chart_threshold_quick.json")
QUICK_MARKDOWN = Path("build/diagnostics/exact_chart_threshold_quick.md")


def sha256_file(path: Path) -> str:
    """Return a content identity for a numerical source file."""

    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_snapshot() -> dict[str, object]:
    """Record the repository state without making it the identity key."""

    try:
        head = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        dirty = bool(
            subprocess.run(
                ["git", "status", "--porcelain"],
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
        )
    except (OSError, subprocess.CalledProcessError):
        return {"head": None, "worktree_dirty_at_generation": None}
    return {"head": head, "worktree_dirty_at_generation": dirty}


def markdown_report(payload: dict[str, object]) -> str:
    """Render the machine-readable payload as a compact audit table."""

    rows = payload["rows"]
    assert isinstance(rows, list)
    lines = [
        "# Exact-chart canard-threshold diagnostic",
        "",
        "Status: **diagnostic numerical evidence; not a theorem or a proof.**",
        "",
        "The exact four-dimensional fixed-scaled-delay chart is integrated by a",
        "literal method of steps with Radau on every step interval.  The",
        "prescribed history on `[-S-theta_1,-S]` is the leading canard and",
        "its singular transverse graph.  At `+S`, `nu` is tuned until the",
        "KS Hamiltonian has zero energy (implemented with its equivalent",
        "positive normalization).",
        "",
        "The reported quotient is",
        "",
        r"\[",
        r" \frac{\nu_c(+h)-\nu_c(-h)}{2\delta h},",
        r"\qquad h=0.04,",
        r"\]",
        "",
        "and the formal target is",
        "",
        r"\[",
        r" \frac{K(\theta_0-\theta_1)}{4\alpha}",
        r" = -0.2041241452319315",
        r"\]",
        "",
        "for `K=1`, `theta_0=0.5`, `theta_1=1`, and",
        r"`alpha=sqrt(6)/4`.",
        "",
        "| delta | S | nu_c(0) | plus quotient | minus quotient | central | relative error | max root residual |",
        "|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row_object in rows:
        assert isinstance(row_object, dict)
        row = row_object
        lines.append(
            "| {delta:.4g} | {section_half_width:.3g} | {nu_zero:.9g} | "
            "{quotient_plus:.9g} | {quotient_minus:.9g} | "
            "{quotient_central:.9g} | {relative_error:.3e} | "
            "{root_residual_max:.3e} |".format(**row)
        )

    lines.extend(
        [
            "",
            "## What this checks",
            "",
            "Along the displayed diagonal sequence, `delta` decreases while",
            "the finite section `S` increases.  The central quotient moves",
            "toward the formal coefficient, and the plus/minus quotients",
            "agree closely relative to the asymptotic discrepancy.  This is a sensitive",
            "sign, scale, and implementation check of the transverse-return",
            "calculation.",
            "",
            "## What this does not check",
            "",
            "The leading-canard history is prescribed rather than obtained",
            "from the parameter-dependent invariant history graph.  The exit",
            "condition is the leading Hamiltonian zero level at a finite",
            "section, not equality of complete attracting and repelling RFDE",
            "histories.  Therefore the computed root depends on the chosen",
            "history, section, and order in which `delta -> 0` and `S ->",
            "infinity` are approached.  Large `S` also amplifies integration",
            "and interpolation errors along the repelling segment.  Neither",
            "the observed convergence nor the small scalar residual proves",
            "history/section independence, a simple geometric root, or the",
            "uniform theorem remainder.",
            "",
            "The exact settings and full-precision values are in",
            "`experiments/results/exact_chart_threshold_convergence.json`.",
            "",
        ]
    )
    refinements = payload.get("refinements")
    if isinstance(refinements, dict):
        lines.extend(
            [
                "## Numerical refinements",
                "",
                "At the smallest displayed `delta` and largest `S`, the",
                "archived tolerance and maximum-step refinements give",
                f"a tolerance spread of `{refinements['tolerance_spread']:.3e}`",
                f"and a maximum-step spread of `{refinements['max_step_spread']:.3e}`",
                "in the normalized central quotient. These discretization",
                "spreads are much smaller than the displayed asymptotic",
                "discrepancy, but they do not address history or section bias.",
                "",
            ]
        )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--quick",
        action="store_true",
        help="run a three-row smoke version instead of the archived table",
    )
    parser.add_argument(
        "--json",
        type=Path,
        default=None,
        help="output path; quick mode defaults under ignored build/",
    )
    parser.add_argument(
        "--markdown",
        type=Path,
        default=None,
        help="output path; quick mode defaults under ignored build/",
    )
    arguments = parser.parse_args()

    output_json = arguments.json or (
        QUICK_JSON if arguments.quick else ARCHIVE_JSON
    )
    output_markdown = arguments.markdown or (
        QUICK_MARKDOWN if arguments.quick else ARCHIVE_MARKDOWN
    )

    weak_gain = 1.0
    recovery_gap = 1.5
    theta_0 = 0.5
    theta_1 = 1.0
    eta_step = 0.04
    integration_rtol = 2.0e-9
    integration_atol = 2.0e-11
    root_xtol = 2.0e-10
    root_rtol = 2.0e-10
    max_step = 0.08
    schedule = QUICK_SCHEDULE if arguments.quick else DEFAULT_SCHEDULE
    rows = []
    for delta, section_half_width in schedule:
        parameters = ExactChartParameters(
            delta=delta,
            weak_gain=weak_gain,
            recovery_gap=recovery_gap,
            theta_0=theta_0,
            theta_1=theta_1,
        )
        row = threshold_coefficient_row(
            parameters,
            eta_step=eta_step,
            section_half_width=section_half_width,
            rtol=integration_rtol,
            atol=integration_atol,
            root_xtol=root_xtol,
            root_rtol=root_rtol,
            max_step=max_step,
        )
        rows.append(row.as_dict())
        print(
            f"delta={delta:.4g}, S={section_half_width:.3g}, "
            f"quotient={row.quotient_central:.12g}, "
            f"relative_error={row.relative_error:.3e}"
        )

    refinements: dict[str, object] | None = None
    if not arguments.quick:
        smallest_delta, largest_section = DEFAULT_SCHEDULE[-1]
        refinement_parameters = ExactChartParameters(
            delta=smallest_delta,
            weak_gain=weak_gain,
            recovery_gap=recovery_gap,
            theta_0=theta_0,
            theta_1=theta_1,
        )
        baseline = rows[-1]

        def refined_row(
            *, rtol: float, atol: float, step: float
        ) -> dict[str, float]:
            return threshold_coefficient_row(
                refinement_parameters,
                eta_step=eta_step,
                section_half_width=largest_section,
                rtol=rtol,
                atol=atol,
                root_xtol=root_xtol,
                root_rtol=root_rtol,
                max_step=step,
            ).as_dict()

        tolerance_rows = [
            baseline,
            refined_row(rtol=5.0e-10, atol=5.0e-12, step=max_step),
            refined_row(rtol=1.0e-10, atol=1.0e-12, step=max_step),
        ]
        max_step_rows = [
            baseline,
            refined_row(
                rtol=integration_rtol,
                atol=integration_atol,
                step=0.04,
            ),
            refined_row(
                rtol=integration_rtol,
                atol=integration_atol,
                step=0.02,
            ),
        ]
        tolerance_values = [
            row["quotient_central"] for row in tolerance_rows
        ]
        step_values = [row["quotient_central"] for row in max_step_rows]
        refinements = {
            "delta": smallest_delta,
            "section_half_width": largest_section,
            "tolerance_rows": tolerance_rows,
            "max_step_rows": max_step_rows,
            "tolerance_settings": [
                {"rtol": 2.0e-9, "atol": 2.0e-11},
                {"rtol": 5.0e-10, "atol": 5.0e-12},
                {"rtol": 1.0e-10, "atol": 1.0e-12},
            ],
            "max_step_settings": [0.08, 0.04, 0.02],
            "tolerance_spread": max(tolerance_values)
            - min(tolerance_values),
            "max_step_spread": max(step_values) - min(step_values),
        }

    predicted = weak_gain * (theta_0 - theta_1) / (4.0 * alpha_value())
    payload: dict[str, object] = {
        "status": "diagnostic numerical evidence; not a theorem or proof",
        "equation": "docs/final-model-blowup.md equation (6)",
        "integrator": {
            "algorithm": "method of steps; scipy.solve_ivp Radau per segment",
            "segment_length_upper_bound": theta_0,
            "rtol": integration_rtol,
            "atol": integration_atol,
            "max_step": max_step,
            "root_algorithm": "Brent on normalized KS zero-energy gap",
            "root_xtol": root_xtol,
            "root_rtol": root_rtol,
            "bracket_policy": (
                "zero root: center 0, initial half-width 0.25; eta roots: "
                "center at zero root, half-width max(0.02,8*delta*h); "
                "double until a sign change, maximum half-width 16"
            ),
        },
        "history": (
            "leading canard plus singular transverse graph on "
            "[-S-theta_1,-S]"
        ),
        "exit_condition": (
            "normalized leading KS Hamiltonian energy gap equals zero at +S"
        ),
        "parameters": {
            "weak_gain": weak_gain,
            "recovery_gap": recovery_gap,
            "theta_0": theta_0,
            "theta_1": theta_1,
            "eta_step": eta_step,
            "alpha": alpha_value(),
        },
        "predicted_coefficient": predicted,
        "quotient": "(nu_c(+h)-nu_c(-h))/(2*delta*h)",
        "rows": rows,
        "refinements": refinements,
        "software": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
        },
        "source": {
            "git": git_snapshot(),
            "sha256": {
                "driver": sha256_file(Path(__file__)),
                "solver": sha256_file(
                    Path("src/canard_control/exact_chart_threshold_diagnostic.py")
                ),
                "chart_algebra": sha256_file(
                    Path("src/canard_control/final_model_blowup.py")
                ),
            },
        },
        "disclaimer": (
            "The prescribed history and finite leading-energy exit section "
            "are diagnostic choices. Their roots are not complete-history "
            "intersections and cannot establish section-independent or "
            "uniform canard-threshold asymptotics."
        ),
    }

    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_markdown.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    output_markdown.write_text(markdown_report(payload), encoding="utf-8")


if __name__ == "__main__":
    main()
