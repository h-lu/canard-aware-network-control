#!/usr/bin/env python3
"""Run the directed D1/D3/D4 FHN parameter-box audit."""

from __future__ import annotations

import argparse
from dataclasses import asdict
import json
import platform
from pathlib import Path
import sys

import gmpy2
import numpy as np
import scipy

from canard_control.fhn_periodic_candidate import solve_fhn_periodic_orbit
from canard_control.fhn_periodic_parameter_box import (
    validate_periodic_parameter_box,
)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--nodes", type=int, default=129)
    parser.add_argument("--cutoff", type=int, default=144)
    parser.add_argument("--precision", type=int, default=160)
    parser.add_argument("--half-width", default="1e-12")
    parser.add_argument("--maximum-radius", default="5e-9")
    parser.add_argument("--chosen-radius", default="5e-9")
    parser.add_argument("--phase-partition", type=int, default=4096)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "experiments/results/fhn_periodic_parameter_box.json"
        ),
    )
    return parser.parse_args()


def main() -> None:
    arguments = parse_arguments()
    orbit = solve_fhn_periodic_orbit(node_count=arguments.nodes)
    validation = validate_periodic_parameter_box(
        orbit,
        half_width=arguments.half_width,
        cutoff=arguments.cutoff,
        precision=arguments.precision,
        maximum_radius=arguments.maximum_radius,
        chosen_radius=arguments.chosen_radius,
        phase_partition_count=arguments.phase_partition,
    )
    payload = {
        "provenance": {
            "generator": "experiments/fhn_periodic_parameter_box.py",
            "argv": [sys.executable, *sys.argv],
            "default_command": (
                "PYTHONPATH=build/testdeps:src /usr/bin/python3 "
                "experiments/fhn_periodic_parameter_box.py"
            ),
            "python": platform.python_version(),
            "platform": platform.platform(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "gmpy2": gmpy2.version(),
            "mpfr": gmpy2.mpfr_version(),
            "rounding": (
                "MPFR RoundDown/RoundUp at every theorem endpoint"
            ),
            "binary_accelerators": (
                "stored binary64 midpoint inverse and sensitivity "
                "candidates, each covered by directed residual/error bounds"
            ),
        },
        "candidate_input": {
            "node_count": len(orbit.state),
            "period": orbit.period,
            "binary_collocation_residual_inf": (
                orbit.collocation_residual_inf
            ),
            "binary_oversampled_residual_inf": (
                orbit.oversampled_residual_inf
            ),
            "binary_spectral_tail_l1": orbit.spectral_tail_l1,
            "claim_status": "diagnostic midpoint only",
        },
        "validation": asdict(validation),
        "scope": {
            "d1_parameter_box_continuation": validation.d1_validated,
            "d3_unique_voltage_extrema": validation.d3_validated,
            "d4_directed_response_lower_bound": (
                validation.d4_response_lower_bound_validated
            ),
            "response_derivative_lipschitz": (
                validation.response.derivative_lipschitz_bound_supplied
            ),
            "issue_15_closed": validation.issue_15_closed,
        },
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    arguments.output.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
