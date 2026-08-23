#!/usr/bin/env python3
"""Run the directed finite/tail periodic RFDE validation."""

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
from canard_control.fhn_periodic_infinite_validation import (
    validate_infinite_periodic_candidate,
)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--nodes", type=int, default=97)
    parser.add_argument("--cutoff", type=int, default=144)
    parser.add_argument("--precision", type=int, default=160)
    parser.add_argument("--maximum-radius", default="1e-7")
    parser.add_argument("--chosen-radius", default="1e-7")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "experiments/results/fhn_periodic_infinite_validation.json"
        ),
    )
    return parser.parse_args()


def main() -> None:
    arguments = parse_arguments()
    orbit = solve_fhn_periodic_orbit(node_count=arguments.nodes)
    validation = validate_infinite_periodic_candidate(
        orbit,
        cutoff=arguments.cutoff,
        precision=arguments.precision,
        maximum_radius=arguments.maximum_radius,
        chosen_radius=arguments.chosen_radius,
    )
    payload = {
        "provenance": {
            "generator": "experiments/fhn_periodic_infinite_validation.py",
            "argv": [sys.executable, *sys.argv],
            "default_command": (
                "PYTHONPATH=build/testdeps:src /usr/bin/python3 "
                "experiments/fhn_periodic_infinite_validation.py"
            ),
            "python": platform.python_version(),
            "platform": platform.platform(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "gmpy2": gmpy2.version(),
            "mpfr": gmpy2.mpfr_version(),
            "rounding": "MPFR RoundDown/RoundUp at every interval operation",
            "binary_accelerator": (
                "stored binary64 midpoint inverse with directed Higham "
                "product/matvec error bounds"
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
        },
        "validation": asdict(validation),
        "scope": {
            "center_periodic_rfde_orbit": (
                validation.periodic_rfde_orbit_validated
            ),
            "center_phase_bordered_rfde_inverse": (
                validation.bordered_rfde_inverse_validated
            ),
            "unit_multiplier_simple": (
                validation.unit_multiplier_simple_validated
            ),
            "full_floquet_hyperbolicity": (
                validation.full_floquet_hyperbolicity_validated
            ),
            "parameter_box_extrema": validation.extrema_validated,
            "frequency_amplitude_response_box": (
                validation.response_box_validated
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
