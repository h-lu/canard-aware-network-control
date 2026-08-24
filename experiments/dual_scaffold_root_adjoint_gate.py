#!/usr/bin/env python3
"""Generate the exact period-locked selected-root adjoint gate record."""

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

from canard_control.dual_scaffold_root_adjoint_gate import (  # noqa: E402
    reference_root_adjoint_gate_payload,
    validate_root_adjoint_gate_payload,
)


def _digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=REPOSITORY
        / "experiments/results/dual_scaffold_root_adjoint_gate.json",
    )
    arguments = parser.parse_args()

    proof_source = (
        REPOSITORY / "src/canard_control/dual_scaffold_root_adjoint_gate.py"
    )
    audit = reference_root_adjoint_gate_payload()
    validate_root_adjoint_gate_payload(audit)
    payload = {
        "audit": audit,
        "manifest": {
            "generator": "experiments/dual_scaffold_root_adjoint_gate.py",
            "proof_source": (
                "src/canard_control/dual_scaffold_root_adjoint_gate.py"
            ),
            "proof_source_sha256": _digest(proof_source),
            "arithmetic": "exact SymPy residual-column and Gaussian identities",
        },
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
