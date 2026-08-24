#!/usr/bin/env python3
"""Generate the fixed-epsilon BVP contract and shooting diagnostic."""

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

from canard_control.fixed_epsilon_quadratic_root_bvp import (  # noqa: E402
    reference_fixed_epsilon_quadratic_root_payload,
    validate_fixed_epsilon_quadratic_root_payload,
)


def _digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=(
            REPOSITORY
            / "experiments/results/fixed_epsilon_quadratic_root_bvp.json"
        ),
    )
    arguments = parser.parse_args()
    source = (
        REPOSITORY
        / "src/canard_control/fixed_epsilon_quadratic_root_bvp.py"
    )
    audit = reference_fixed_epsilon_quadratic_root_payload()
    validate_fixed_epsilon_quadratic_root_payload(audit)
    payload = {
        "audit": audit,
        "manifest": {
            "generator": "experiments/fixed_epsilon_quadratic_root_bvp.py",
            "proof_source": (
                "src/canard_control/fixed_epsilon_quadratic_root_bvp.py"
            ),
            "proof_source_sha256": _digest(source),
            "arithmetic": (
                "exact SymPy BVP contract plus binary64 SciPy shooting; "
                "no interval proof"
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
