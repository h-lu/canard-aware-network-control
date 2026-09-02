#!/usr/bin/env python3
"""Generate the numerical data used in Paper A, Figure 2.

Run from the repository root with

    PYTHONPATH=src uv run --extra numeric \
      python experiments/three_node_finite_section_diagnostic.py

The calculation is a prescribed-history finite-section diagnostic for the
current three-node exact fold RFDE.  It is not the manuscript's abstractly
constructed ``D_3^{fin}`` and is not evidence for a heteroclinic connection.
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

from canard_control.three_node_finite_section import (
    ThreeNodeParameters,
    convergence_row,
    integrate_finite_section,
    projected_rhs_difference,
    tune_section_root,
)


DEFAULT_OUTPUT = Path(
    "experiments/results/three_node_finite_section_diagnostic.json"
)
DEFAULT_SCHEDULE = (
    (0.12, 2.50),
    (0.08, 2.75),
    (0.05, 3.00),
    (0.02, 3.50),
    (0.01, 4.00),
)


def sha256_file(path: Path) -> str:
    """Return a content identity for a numerical source file."""

    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_snapshot() -> dict[str, object]:
    """Record the repository state without making it the data identity."""

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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--quick",
        action="store_true",
        help="use two convergence rows and omit refinement calculations",
    )
    arguments = parser.parse_args()

    zeta_step = 0.04
    rtol = 2.0e-9
    atol = 2.0e-11
    max_step = 0.08
    schedule = DEFAULT_SCHEDULE if not arguments.quick else DEFAULT_SCHEDULE[1:3]
    rows = [
        convergence_row(
            delta=delta,
            section_half_width=section_half_width,
            zeta_step=zeta_step,
            rtol=rtol,
            atol=atol,
            max_step=max_step,
        ).as_dict()
        for delta, section_half_width in schedule
    ]

    panel_delta = 0.05
    panel_section = 3.0
    panel_parameters = ThreeNodeParameters(delta=panel_delta)
    panel_row = next(row for row in rows if row["delta"] == panel_delta)
    panel_roots = {
        "minus": float(panel_row["nu_minus"]),
        "zero": float(panel_row["nu_zero"]),
        "plus": float(panel_row["nu_plus"]),
    }
    center = panel_roots["zero"]
    nu_values = np.linspace(center - 0.0032, center + 0.0032, 13)
    panel_curves: dict[str, list[float]] = {}
    for label, zeta in (("minus", -zeta_step), ("zero", 0.0), ("plus", zeta_step)):
        panel_curves[label] = [
            integrate_finite_section(
                panel_parameters,
                zeta=zeta,
                nu=float(nu),
                section_half_width=panel_section,
                rtol=rtol,
                atol=atol,
                max_step=max_step,
            ).exit_gap
            for nu in nu_values
        ]

    control_minus = tune_section_root(
        panel_parameters,
        zeta=-zeta_step,
        section_half_width=panel_section,
        coincident_delay_control=True,
        rtol=rtol,
        atol=atol,
        max_step=max_step,
    )
    control_plus = tune_section_root(
        panel_parameters,
        zeta=zeta_step,
        section_half_width=panel_section,
        coincident_delay_control=True,
        rtol=rtol,
        atol=atol,
        max_step=max_step,
    )
    control_quotient = (
        control_plus.nu - control_minus.nu
    ) / (2.0 * zeta_step * panel_delta)

    representative_current = np.array([0.2, -0.3, 0.10, -0.04, -0.06])
    representative_delayed_0 = np.array(
        [-0.1, 0.2, -0.02, 0.03, -0.01]
    )
    representative_delayed_1 = np.array(
        [-0.25, 0.35, 0.01, -0.02, 0.01]
    )
    projection_residual = projected_rhs_difference(
        representative_current,
        (representative_delayed_0, representative_delayed_1),
        parameters=panel_parameters,
        zeta=zeta_step,
        nu=panel_roots["zero"],
    )

    refinements: dict[str, object] = {}
    if not arguments.quick:
        refined_parameters = ThreeNodeParameters(delta=0.01)
        refined_rows = {}
        for step in (0.02, 0.04, 0.08):
            refined_rows[f"zeta_{step:.2f}"] = convergence_row(
                delta=0.01,
                section_half_width=4.0,
                zeta_step=step,
                rtol=rtol,
                atol=atol,
                max_step=max_step,
            ).quotient
        tight_minus = tune_section_root(
            refined_parameters,
            zeta=-zeta_step,
            section_half_width=4.0,
            rtol=5.0e-10,
            atol=5.0e-12,
            max_step=0.04,
        )
        tight_plus = tune_section_root(
            refined_parameters,
            zeta=zeta_step,
            section_half_width=4.0,
            rtol=5.0e-10,
            atol=5.0e-12,
            max_step=0.04,
        )
        tight_quotient = (
            tight_plus.nu - tight_minus.nu
        ) / (2.0 * zeta_step * refined_parameters.delta)
        refinements = {
            "zeta_step_quotients": refined_rows,
            "tight_solver_quotient": tight_quotient,
            "tight_solver_difference": abs(tight_quotient - rows[-1]["quotient"]),
        }

    source_paths = (
        Path("src/canard_control/three_node_finite_section.py"),
        Path("experiments/three_node_finite_section_diagnostic.py"),
    )
    payload = {
        "status": "numerical diagnostic; not used in any proof",
        "definition": {
            "history": "singular orbit gamma_0 with h=0 on [-S-2,-S]",
            "outgoing_condition": "Y(S)-X(S)^2+1/2=0",
            "root_name": "nu_hat_sec(delta,zeta;S)",
            "not_computed": [
                "D_3^fin",
                "G_3,delta^g",
                "heteroclinic connection",
                "maximal canard",
            ],
        },
        "parameters": {
            "sigma": panel_parameters.sigma,
            "beta": panel_parameters.beta,
            "D": 1.0,
            "K": panel_parameters.coupling_gain,
            "theta_0": panel_parameters.delay_0,
            "theta_1": panel_parameters.delay_1,
            "zeta_step": zeta_step,
            "predicted_coefficient": panel_parameters.predicted_coefficient,
            "singular_center": panel_parameters.singular_center,
        },
        "solver": {
            "method": "literal method of steps with scipy.integrate.solve_ivp Radau",
            "rtol": rtol,
            "atol": atol,
            "max_step": max_step,
            "scipy": scipy.__version__,
            "numpy": np.__version__,
            "python": platform.python_version(),
        },
        "convergence_rows": rows,
        "left_panel": {
            "delta": panel_delta,
            "section_half_width": panel_section,
            "nu_values": [float(value) for value in nu_values],
            "exit_gap_curves": panel_curves,
            "roots": panel_roots,
        },
        "coincident_delay_control": {
            "description": "opposite perturbation layers combined at one delay",
            "nu_minus": control_minus.nu,
            "nu_plus": control_plus.nu,
            "quotient": control_quotient,
        },
        "checks": {
            "projection_rhs_residual": projection_residual,
            "maximum_root_residual": max(row["root_residual_max"] for row in rows),
            "refinements": refinements,
        },
        "source_sha256": {
            str(path): sha256_file(path) for path in source_paths
        },
        "git": git_snapshot(),
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(f"wrote {arguments.output}")
    for row in rows:
        print(
            "delta={delta:.4g} S={section_half_width:.3g} "
            "q={quotient:.10f} relative_error={relative_error:.3e}".format(**row)
        )


if __name__ == "__main__":
    main()
