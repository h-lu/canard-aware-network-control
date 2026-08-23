#!/usr/bin/env python3
"""Run MPFR-directed validation gates for the synchronous FHN candidate."""

from __future__ import annotations

import argparse
import ctypes.util
from dataclasses import asdict, is_dataclass
import importlib.util
import json
import platform
from pathlib import Path
import shutil
import sys
from typing import Any

import gmpy2
import numpy as np
import scipy

from canard_control.fhn_periodic_candidate import (
    FHNPeriodicParameters,
    solve_fhn_periodic_orbit,
)
from canard_control.fhn_periodic_directed_validation import (
    directed_fhn_validation,
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
    parser.add_argument("--nodes", type=int, default=97)
    parser.add_argument("--precision", type=int, default=160)
    parser.add_argument("--weight-nu", default="1.001")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "experiments/results/fhn_periodic_directed_validation.json"
        ),
    )
    return parser.parse_args()


def _backend_audit() -> dict[str, Any]:
    """Record interval backends visible to this exact Python/PATH process."""

    modules: dict[str, bool] = {}
    for name in ("gmpy2", "flint", "sage", "sageall", "mpmath", "interval", "mpfi"):
        try:
            modules[name] = importlib.util.find_spec(name) is not None
        except (ModuleNotFoundError, ValueError):
            modules[name] = False
    return {
        "selected_backend": "gmpy2 MPFR directed rounding",
        "python_modules_visible": modules,
        "executables_visible": {
            name: shutil.which(name) for name in ("sage", "julia", "arb")
        },
        "shared_libraries_visible": {
            name: ctypes.util.find_library(name)
            for name in ("arb", "flint", "mpfi", "mpfr", "gmp")
        },
        "boundary": (
            "Backend visibility is provenance, not a proof. The certificate "
            "uses only explicitly directed MPFR operations; mpmath presence "
            "is not treated as an Arb/FLINT substitute."
        ),
    }


def main() -> None:
    arguments = parse_arguments()
    parameters = FHNPeriodicParameters()
    orbit = solve_fhn_periodic_orbit(parameters, node_count=arguments.nodes)
    validation = directed_fhn_validation(
        orbit,
        precision=arguments.precision,
        weight_nu=arguments.weight_nu,
    )
    payload = {
        "provenance": {
            "generator": "experiments/fhn_periodic_directed_validation.py",
            "argv": [sys.executable, *sys.argv],
            "default_command": (
                "PYTHONPATH=build/testdeps:src /usr/bin/python3 "
                "experiments/fhn_periodic_directed_validation.py"
            ),
            "python": platform.python_version(),
            "platform": platform.platform(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "gmpy2": gmpy2.version(),
            "mpfr": gmpy2.mpfr_version(),
            "rounding": "MPFR RoundDown/RoundUp at every interval operation",
            "precision_bits": arguments.precision,
            "node_count": arguments.nodes,
        },
        "backend_audit": _backend_audit(),
        "candidate_input": {
            "period": orbit.period,
            "binary_collocation_residual_inf": orbit.collocation_residual_inf,
            "binary_oversampled_residual_inf": orbit.oversampled_residual_inf,
            "spectral_tail_l1_diagnostic": orbit.spectral_tail_l1,
        },
        "validation": validation,
        "scope": {
            "exact_finite_collocation_proof": (
                validation.finite.exact_finite_collocation_root_validated
            ),
            "exact_finite_bordered_inverse_proof": (
                validation.finite.exact_finite_bordered_inverse_validated
            ),
            "directed_full_polynomial_residual": True,
            "infinite_dimensional_periodic_rfde_proof": False,
            "infinite_dimensional_bordered_inverse_proof": False,
            "issue_15_closed": False,
        },
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
