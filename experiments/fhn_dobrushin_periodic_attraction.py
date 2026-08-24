#!/usr/bin/env python3
"""Generate the Dobrushin periodic-attraction proof record."""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import platform
import sys

import gmpy2


REPOSITORY = Path(__file__).resolve().parents[1]
SOURCE_ROOT = REPOSITORY / "src"
if str(SOURCE_ROOT) not in sys.path:
    sys.path.insert(0, str(SOURCE_ROOT))

from canard_control.fhn_dobrushin_periodic_attraction import (  # noqa: E402
    reference_dobrushin_periodic_payload,
    validate_dobrushin_periodic_payload,
)


PROOF_SOURCES = (
    "src/canard_control/directed_interval.py",
    "src/canard_control/fhn_dobrushin_periodic_attraction.py",
    "src/canard_control/fhn_periodic_transverse_halanay.py",
    "src/canard_control/fhn_synchronous_floquet_right_half_cover.py",
    "src/canard_control/quadratic_period_lock_dobrushin_lift.py",
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=(
            REPOSITORY
            / "experiments/results/fhn_dobrushin_periodic_attraction.json"
        ),
    )
    arguments = parser.parse_args()
    payload = reference_dobrushin_periodic_payload()
    validate_dobrushin_periodic_payload(payload)
    generator = Path(__file__).resolve()
    payload["provenance"] = {
        "generator": str(generator.relative_to(REPOSITORY)),
        "generator_sha256": sha256(generator.read_bytes()).hexdigest(),
        "proof_source_manifest": {
            relative: sha256((REPOSITORY / relative).read_bytes()).hexdigest()
            for relative in PROOF_SOURCES
        },
        "arithmetic": (
            "MPFR directed recomposition of the weighted Dobrushin-Halanay "
            "margin and rate residual; exact rational non-rank-one witness"
        ),
        "python": platform.python_version(),
        "gmpy2": gmpy2.version(),
        "mpfr": gmpy2.mpfr_version(),
        "default_command": (
            "PYTHONPATH=src python3 "
            "experiments/fhn_dobrushin_periodic_attraction.py"
        ),
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
