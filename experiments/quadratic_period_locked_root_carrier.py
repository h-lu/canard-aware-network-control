#!/usr/bin/env python3
"""Generate the quadratic period-lock canard-root carrier record."""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import sys


REPOSITORY = Path(__file__).resolve().parents[1]
SOURCE_ROOT = REPOSITORY / "src"
if str(SOURCE_ROOT) not in sys.path:
    sys.path.insert(0, str(SOURCE_ROOT))

from canard_control.quadratic_period_locked_root_carrier import (  # noqa: E402
    reference_quadratic_period_lock_payload,
    validate_quadratic_period_lock_payload,
)


def _digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=REPOSITORY
        / "experiments/results/quadratic_period_locked_root_carrier.json",
    )
    arguments = parser.parse_args()

    proof_source = (
        REPOSITORY
        / "src/canard_control/quadratic_period_locked_root_carrier.py"
    )
    audit = reference_quadratic_period_lock_payload()
    validate_quadratic_period_lock_payload(audit)
    payload = {
        "audit": audit,
        "manifest": {
            "generator": (
                "experiments/quadratic_period_locked_root_carrier.py"
            ),
            "proof_source": (
                "src/canard_control/quadratic_period_locked_root_carrier.py"
            ),
            "proof_source_sha256": _digest(proof_source),
            "arithmetic": (
                "exact SymPy balanced-projector, fold-chart, Gaussian, "
                "and root-coefficient identities"
            ),
        },
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
