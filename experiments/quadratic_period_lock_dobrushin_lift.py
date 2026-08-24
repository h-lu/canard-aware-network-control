#!/usr/bin/env python3
"""Generate the Dobrushin full-network quadratic-root lift record."""

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

from canard_control.quadratic_period_lock_dobrushin_lift import (  # noqa: E402
    reference_dobrushin_lift_payload,
    validate_dobrushin_lift_payload,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=REPOSITORY
        / "experiments/results/quadratic_period_lock_dobrushin_lift.json",
    )
    arguments = parser.parse_args()
    source = (
        REPOSITORY
        / "src/canard_control/quadratic_period_lock_dobrushin_lift.py"
    )
    audit = reference_dobrushin_lift_payload()
    validate_dobrushin_lift_payload(audit)
    payload = {
        "audit": audit,
        "manifest": {
            "generator": (
                "experiments/quadratic_period_lock_dobrushin_lift.py"
            ),
            "proof_source": (
                "src/canard_control/quadratic_period_lock_dobrushin_lift.py"
            ),
            "proof_source_sha256": sha256(source.read_bytes()).hexdigest(),
            "arithmetic": (
                "exact rational balance, Dobrushin, projector, and "
                "transverse-block identities"
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
