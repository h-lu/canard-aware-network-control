#!/usr/bin/env python3
"""Generate the growing-network finite-section diagnostic data.

Run from the repository root with

    PYTHONPATH=src uv run --extra numeric \
      python experiments/growing_network_finite_section_diagnostic.py

The calculation uses a prescribed singular incoming history and a scalar
outgoing-section mismatch.  It checks the dimension-uniform sign and scale of
the Fredholm coefficient for an explicit growing family.  It does not compute
``D_N^{fin}``, an invariant-manifold intersection, a heteroclinic connection,
or a maximal canard, and it is not used in a proof.
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

from canard_control.growing_network_finite_section import (
    GrowingNetworkParameters,
    growing_direction,
    network_objects,
    network_size_row,
    projected_rhs_difference,
)


DEFAULT_OUTPUT = Path(
    "experiments/results/growing_network_finite_section_diagnostic.json"
)
DEFAULT_NODE_COUNTS = (3, 5, 9, 17, 33)


def sha256_file(path: Path) -> str:
    """Return a content identity for a numerical source file."""

    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_snapshot() -> dict[str, object]:
    """Record repository state without making it the data identity."""

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


def representative_projection_residual(
    parameters: GrowingNetworkParameters,
) -> float:
    """Check projection invisibility using two distinct delayed histories."""

    direction = growing_direction(parameters.node_count)
    current = np.concatenate(([0.2, -0.3], 0.03 * direction))
    delayed_0 = np.concatenate(([-0.1, 0.2], -0.02 * direction))
    delayed_1 = np.concatenate(([-0.25, 0.35], 0.01 * direction))
    return projected_rhs_difference(
        current,
        (delayed_0, delayed_1),
        parameters=parameters,
        zeta=0.04,
        nu=parameters.singular_center,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--quick",
        action="store_true",
        help="compute only N=3 and N=9 for a fast local check",
    )
    arguments = parser.parse_args()

    delta = 0.02
    section_half_width = 3.5
    zeta_step = 0.04
    rtol = 2.0e-9
    atol = 2.0e-11
    max_step = 0.08
    node_counts = DEFAULT_NODE_COUNTS if not arguments.quick else (3, 9)

    rows = [
        network_size_row(
            node_count=node_count,
            delta=delta,
            section_half_width=section_half_width,
            zeta_step=zeta_step,
            rtol=rtol,
            atol=atol,
            max_step=max_step,
        ).as_dict()
        for node_count in node_counts
    ]

    family_checks: dict[str, dict[str, float]] = {}
    projection_residuals: dict[str, float] = {}
    for node_count in node_counts:
        parameters = GrowingNetworkParameters(
            node_count=node_count, delta=delta
        )
        direction, curvature, graph_coefficient = network_objects(parameters)
        family_checks[str(node_count)] = {
            "direction_mean": float(np.mean(direction)),
            "direction_mean_square": float(np.mean(direction**2)),
            "direction_minimum_spacing": float(np.min(np.diff(direction))),
            "curvature_minimum": float(np.min(curvature)),
            "curvature_mean": float(np.mean(curvature)),
            "graph_coefficient_mean": float(np.mean(graph_coefficient)),
            "dobrushin_coefficient": parameters.dobrushin_coefficient,
            "predicted_coefficient": parameters.predicted_coefficient,
        }
        projection_residuals[str(node_count)] = (
            representative_projection_residual(parameters)
        )

    source_paths = (
        Path("src/canard_control/growing_network_finite_section.py"),
        Path("experiments/growing_network_finite_section_diagnostic.py"),
    )
    reference = GrowingNetworkParameters(node_count=3, delta=delta)
    payload = {
        "status": "numerical diagnostic; not used in any proof",
        "definition": {
            "history": (
                "singular orbit gamma_0 with h=0 on "
                "[-S-theta_1,-S]"
            ),
            "outgoing_condition": "Y(S)-X(S)^2+1/2=0",
            "root_name": "nu_hat_sec(N,delta,zeta;S)",
            "quotient": (
                "[nu_hat_sec(+zeta)-nu_hat_sec(-zeta)]/"
                "(2*zeta*delta)"
            ),
            "not_computed": [
                "D_N^fin",
                "G_N,delta^g",
                "stable/unstable manifold intersection",
                "heteroclinic connection",
                "maximal canard",
            ],
        },
        "network_family": {
            "stationary_distribution": "pi_N=(1/N)1",
            "markov_matrix": "P_N=(1-rho)I+rho*1*pi_N^T",
            "direction": (
                "q_i,N=sqrt(12/(N^2-1))*(i-(N+1)/2)"
            ),
            "direction_identities": "pi_N^T q_N=0; pi_N^T q_N^2=1",
            "curvature": "c_N=1+sigma*q_N",
            "delay_layers": (
                "B_0=P_N/2+zeta*q_N*pi_N^T; "
                "B_1=P_N/2-zeta*q_N*pi_N^T"
            ),
            "transverse_generator": (
                "A_N=D(P_N-I)=-D*rho*I on ker(pi_N^T)"
            ),
            "fredholm_coefficient": (
                "Lambda_N=-K*sigma*(theta_1-theta_0)/(2*D*rho)"
            ),
        },
        "parameters": {
            "node_counts": list(node_counts),
            "delta": delta,
            "section_half_width": section_half_width,
            "zeta_step": zeta_step,
            "rho": reference.rho,
            "sigma": reference.sigma,
            "beta": reference.beta,
            "D": reference.diffusion,
            "K": reference.coupling_gain,
            "theta_0": reference.delay_0,
            "theta_1": reference.delay_1,
            "predicted_coefficient": reference.predicted_coefficient,
            "singular_center": reference.singular_center,
        },
        "solver": {
            "method": (
                "literal two-delay method of steps with "
                "scipy.integrate.solve_ivp Radau"
            ),
            "rtol": rtol,
            "atol": atol,
            "max_step": max_step,
            "scipy": scipy.__version__,
            "numpy": np.__version__,
            "python": platform.python_version(),
        },
        "network_size_rows": rows,
        "checks": {
            "family_identities": family_checks,
            "projection_rhs_residuals": projection_residuals,
            "maximum_projection_rhs_residual": max(
                projection_residuals.values()
            ),
            "maximum_root_residual": max(
                row["root_residual_max"] for row in rows
            ),
            "maximum_transverse_mean": max(
                row["transverse_mean_max"] for row in rows
            ),
            "quotient_spread": max(row["quotient"] for row in rows)
            - min(row["quotient"] for row in rows),
        },
        "source_sha256": {
            str(path): sha256_file(path) for path in source_paths
        },
        "git": git_snapshot(),
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {arguments.output}")
    for row in rows:
        print(
            "N={node_count:2d} q={quotient:.10f} "
            "target={predicted_coefficient:.10f} "
            "residual={root_residual_max:.3e}".format(**row)
        )


if __name__ == "__main__":
    main()
