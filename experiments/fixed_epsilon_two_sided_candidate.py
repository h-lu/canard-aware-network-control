#!/usr/bin/env python3
"""Generate the fixed-epsilon two-sided full-history candidate."""

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

from canard_control.fixed_epsilon_two_sided_candidate import (  # noqa: E402
    BLUEPRINT_NOTE_SHA256,
    BLUEPRINT_RESULT_SHA256,
    BLUEPRINT_SOURCE_SHA256,
    reference_two_sided_candidate_payload,
    validate_two_sided_candidate_payload,
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
            / "experiments/results/fixed_epsilon_two_sided_candidate.json"
        ),
    )
    arguments = parser.parse_args()
    source = (
        REPOSITORY
        / "src/canard_control/fixed_epsilon_two_sided_candidate.py"
    )
    blueprint_source = (
        REPOSITORY / "src/canard_control/fixed_epsilon_quadratic_root_bvp.py"
    )
    blueprint_result = (
        REPOSITORY
        / "experiments/results/fixed_epsilon_quadratic_root_bvp.json"
    )
    blueprint_note = REPOSITORY / "docs/fixed-epsilon-quadratic-root-bvp.md"
    observed_bindings = {
        "blueprint_source_sha256": _digest(blueprint_source),
        "blueprint_result_sha256": _digest(blueprint_result),
        "blueprint_note_sha256": _digest(blueprint_note),
    }
    expected_bindings = {
        "blueprint_source_sha256": BLUEPRINT_SOURCE_SHA256,
        "blueprint_result_sha256": BLUEPRINT_RESULT_SHA256,
        "blueprint_note_sha256": BLUEPRINT_NOTE_SHA256,
    }
    if observed_bindings != expected_bindings:
        raise RuntimeError("the fixed-epsilon blueprint binding has drifted")
    audit = reference_two_sided_candidate_payload()
    validate_two_sided_candidate_payload(audit)
    payload = {
        "audit": audit,
        "manifest": {
            "generator": "experiments/fixed_epsilon_two_sided_candidate.py",
            "proof_source": (
                "src/canard_control/fixed_epsilon_two_sided_candidate.py"
            ),
            "proof_source_sha256": _digest(source),
            **observed_bindings,
            "arithmetic": (
                "binary64 SciPy DOP853 seed, sparse Newton, and full "
                "discrete-residual adjoint; no intervals"
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
