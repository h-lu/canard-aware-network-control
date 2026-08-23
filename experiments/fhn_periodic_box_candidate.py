#!/usr/bin/env python3
"""Reproduce the synchronous-FHN periodic response-box candidate.

The JSON output is a floating-point diagnostic.  A positive ``candidate_beta``
does not constitute an interval proof because neither the continuum between
the nine samples nor Fourier tails and rounding errors are enclosed.
"""

from __future__ import annotations

import argparse
import json
import platform
import sys
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any

import numpy as np
import scipy

from canard_control.fhn_periodic_candidate import (
    FHNPeriodicParameters,
    convergence_table,
    ode_persistence_route_candidate,
    periodic_response_candidate,
    sampled_response_box_candidate,
    solve_fhn_periodic_orbit,
)


def _jsonable(value: Any) -> Any:
    if is_dataclass(value):
        return _jsonable(asdict(value))
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_jsonable(item) for item in value]
    if isinstance(value, np.ndarray):
        return _jsonable(value.tolist())
    if isinstance(value, np.generic):
        return value.item()
    return value


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--nodes", type=int, default=129)
    parser.add_argument(
        "--convergence-nodes",
        default="65,97,129,193",
        help="comma-separated odd Fourier node counts",
    )
    parser.add_argument("--half-width-kappa-1", type=float, default=5.0e-5)
    parser.add_argument("--half-width-kappa-3", type=float, default=5.0e-5)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("experiments/results/fhn_periodic_box_candidate.json"),
    )
    return parser.parse_args()


def main() -> None:
    arguments = parse_arguments()
    counts = tuple(
        int(item.strip())
        for item in arguments.convergence_nodes.split(",")
        if item.strip()
    )
    parameters = FHNPeriodicParameters()
    orbit = solve_fhn_periodic_orbit(parameters, node_count=arguments.nodes)
    response = periodic_response_candidate(orbit)
    response_box, _ = sampled_response_box_candidate(
        parameters,
        half_widths=(
            arguments.half_width_kappa_1,
            arguments.half_width_kappa_3,
        ),
        node_count=arguments.nodes,
    )
    persistence_route = ode_persistence_route_candidate(orbit)
    convergence = convergence_table(parameters, counts)

    payload = {
        "provenance": {
            "generator": "experiments/fhn_periodic_box_candidate.py",
            "default_command": (
                "PYTHONPATH=build/testdeps:src /usr/bin/python3 "
                "experiments/fhn_periodic_box_candidate.py"
            ),
            "argv": [sys.executable, *sys.argv],
            "arithmetic": "IEEE-754 binary64 without directed rounding",
            "python": platform.python_version(),
            "platform": platform.platform(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "center_node_count": arguments.nodes,
            "convergence_node_counts": counts,
        },
        "claim_status": {
            "directed_interval_proof": False,
            "validated_periodic_orbit": False,
            "validated_response_box": False,
            "finite_sample_floating_candidate": True,
            "positive_floating_weyl_candidate": response_box.candidate_beta > 0.0,
            "limitations": [
                "binary64 arithmetic is not outward rounded",
                "the Fourier tail and continuum between gain samples are not enclosed",
                "finite bordered singular values do not prove RFDE operator invertibility",
                "extremum scans do not prove interval derivative signs between scan points",
                "the ODE persistence polynomials have not been adapted or interval evaluated",
            ],
        },
        "method": {
            "orbit": "odd Fourier collocation in normalized phase with integral phase border",
            "delay": "exact Fourier shift at tau_j/T",
            "period_column": "analytic moving-delay derivative",
            "response": "bordered forward sensitivities and independent discrete adjoints",
            "box_sampling": "Cartesian 3x3 grid in (kappa_1,kappa_3)",
        },
        "center_orbit": orbit,
        "center_response": response,
        "sampled_box": response_box,
        "spectral_convergence": convergence,
        "ode_persistence_route": persistence_route,
    }
    output = arguments.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(_jsonable(payload), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(_jsonable(payload), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
