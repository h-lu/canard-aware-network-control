#!/usr/bin/env python3
"""Build the explicit quadratic-period-lock eta Floquet box."""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
import os
from pathlib import Path
import platform
import sys

import gmpy2
import numpy as np
import scipy


REPOSITORY = Path(__file__).resolve().parents[1]
SOURCE_ROOT = REPOSITORY / "src"
if str(SOURCE_ROOT) not in sys.path:
    sys.path.insert(0, str(SOURCE_ROOT))

from canard_control.quadratic_period_lock_eta_floquet_box import (  # noqa: E402
    build_eta_floquet_certificate,
    eta_floquet_payload,
    validate_eta_floquet_payload,
)


PROOF_SOURCES = (
    "src/canard_control/directed_interval.py",
    "src/canard_control/fhn_bloch_outer_validation.py",
    "src/canard_control/fhn_dobrushin_periodic_attraction.py",
    "src/canard_control/fhn_periodic_infinite_validation.py",
    "src/canard_control/fhn_synchronous_floquet_right_half_cover.py",
    "src/canard_control/fhn_synchronous_floquet_riesz_reduction.py",
    "src/canard_control/quadratic_period_lock_eta_floquet_box.py",
    "src/canard_control/quadratic_period_locked_root_carrier.py",
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=(
            REPOSITORY
            / "experiments/results/quadratic_period_lock_eta_floquet_box.json"
        ),
    )
    parser.add_argument("--precision", type=int, default=160)
    arguments = parser.parse_args()

    def progress(index: int, total: int) -> None:
        print(
            f"eta leaf replay: {index}/{total}",
            file=sys.stderr,
            flush=True,
        )

    certificate = build_eta_floquet_certificate(
        precision=arguments.precision,
        progress=progress,
    )
    payload = eta_floquet_payload(certificate)
    validate_eta_floquet_payload(payload)
    generator = Path(__file__).resolve()
    payload["provenance"] = {
        "generator": str(generator.relative_to(REPOSITORY)),
        "generator_sha256": sha256(generator.read_bytes()).hexdigest(),
        "proof_source_manifest": {
            relative: sha256((REPOSITORY / relative).read_bytes()).hexdigest()
            for relative in PROOF_SOURCES
        },
        "arithmetic": (
            "fresh MPFR/binary64 replay of every parent four-block leaf "
            "contraction followed by directed public-decimal eta bounds on "
            "the frozen parent partition"
        ),
        "python": platform.python_version(),
        "numpy": np.__version__,
        "numpy_blas": np.__config__.CONFIG.get("Build Dependencies", {}).get(
            "blas", {}
        ),
        "openblas_num_threads": os.environ.get("OPENBLAS_NUM_THREADS"),
        "scipy": scipy.__version__,
        "gmpy2": gmpy2.version(),
        "mpfr": gmpy2.mpfr_version(),
        "default_command": (
            "OPENBLAS_NUM_THREADS=8 PYTHONPATH=build/testdeps:src "
            "/usr/bin/python3 "
            "experiments/quadratic_period_lock_eta_floquet_box.py"
        ),
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "eta_radius": certificate.eta_radius,
                "minimum_leaf_eta_radius_lower": (
                    certificate.minimum_leaf_eta_radius_lower
                ),
                "eta_budget_digest": certificate.eta_budget_digest,
                "worst_leaf": {
                    "root_id": certificate.worst_leaf.root_id,
                    "path": certificate.worst_leaf.path,
                    "selected_eta_contraction_upper": (
                        certificate.worst_leaf.selected_eta_contraction_upper
                    ),
                },
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
