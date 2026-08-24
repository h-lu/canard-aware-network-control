#!/usr/bin/env python3
"""Generate the exact target C4 preparation-seam audit."""

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

import canard_control.fixed_epsilon_target_c4_preparation_seam as seam  # noqa: E402


def _digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=REPOSITORY / seam.RESULT_RELATIVE_PATH,
    )
    arguments = parser.parse_args()
    parent_checks = seam.verify_parent_result(REPOSITORY)
    payload = {
        "audit": seam.json_ready_target_c4_preparation_seam(),
        "manifest": {
            "proof_source": seam.PROOF_SOURCE_RELATIVE_PATH,
            "proof_source_sha256": _digest(Path(seam.__file__).resolve()),
            "generator": seam.GENERATOR_RELATIVE_PATH,
            "generator_sha256": _digest(Path(__file__).resolve()),
            "note": seam.NOTE_RELATIVE_PATH,
            "note_sha256": _digest(REPOSITORY / seam.NOTE_RELATIVE_PATH),
            "parent_result": seam.PARENT_RESULT_RELATIVE_PATH,
            "parent_result_sha256": seam.TARGET_PARENT_RESULT_SHA256,
            "parent_claim_checks": parent_checks,
            "default_command": seam.DEFAULT_COMMAND,
            "python": platform.python_version(),
            "platform": platform.platform(),
            "arithmetic": seam.MANIFEST_ARITHMETIC,
        },
    }
    seam.validate_target_c4_preparation_seam_result(payload, REPOSITORY)
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
