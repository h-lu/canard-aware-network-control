#!/usr/bin/env python3
"""Generate the exact C4-history Bernstein P-matrix certificate."""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import platform
import sys


REPOSITORY = Path(__file__).resolve().parents[1]
SOURCE_ROOT = REPOSITORY / "src"
if str(SOURCE_ROOT) not in sys.path:
    sys.path.insert(0, str(SOURCE_ROOT))

import sympy as sp  # noqa: E402

import canard_control.fixed_epsilon_target_c4_history_bernstein as proof  # noqa: E402


def _sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=REPOSITORY / proof.RESULT_RELATIVE_PATH,
    )
    arguments = parser.parse_args()
    parent_checks = proof.verify_parent_result(REPOSITORY)
    payload = {
        "audit": proof.json_ready_target_c4_history_bernstein(),
        "manifest": {
            "proof_source": proof.PROOF_SOURCE_RELATIVE_PATH,
            "proof_source_sha256": _sha256(Path(proof.__file__).resolve()),
            "generator": proof.GENERATOR_RELATIVE_PATH,
            "generator_sha256": _sha256(Path(__file__).resolve()),
            "note": proof.NOTE_RELATIVE_PATH,
            "note_sha256": _sha256(REPOSITORY / proof.NOTE_RELATIVE_PATH),
            "parent_result": proof.PARENT_RESULT_RELATIVE_PATH,
            "parent_result_sha256": proof.PARENT_RESULT_SHA256,
            "parent_claim_checks": parent_checks,
            "default_command": proof.DEFAULT_COMMAND,
            "python": platform.python_version(),
            "sympy": sp.__version__,
            "platform": platform.platform(),
            "arithmetic": proof.MANIFEST_ARITHMETIC,
        },
    }
    proof.validate_target_c4_history_bernstein_result(payload, REPOSITORY)
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
