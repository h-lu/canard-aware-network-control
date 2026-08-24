#!/usr/bin/env python3
"""Generate the target raw-slot tilted-phase comparison certificate."""

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

import canard_control.fixed_epsilon_target_tilted_phase as phase  # noqa: E402
from canard_control.fixed_epsilon_target_tilted_phase import (  # noqa: E402
    DEFAULT_COMMAND,
    GENERATOR_RELATIVE_PATH,
    MANIFEST_ARITHMETIC,
    NOTE_RELATIVE_PATH,
    PARENT_RESULT_RELATIVE_PATH,
    PROOF_SOURCE_RELATIVE_PATH,
    RESULT_RELATIVE_PATH,
    json_ready_target_tilted_phase_audit,
    validate_target_tilted_phase_result,
    verify_parent_evidence,
)


def _sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=REPOSITORY / RESULT_RELATIVE_PATH,
    )
    return parser.parse_args()


def main() -> None:
    arguments = parse_arguments()
    parent_checks = verify_parent_evidence(REPOSITORY)
    source_path = Path(phase.__file__).resolve()
    generator_path = Path(__file__).resolve()
    note_path = REPOSITORY / NOTE_RELATIVE_PATH
    parent_path = REPOSITORY / PARENT_RESULT_RELATIVE_PATH
    payload = {
        "audit": json_ready_target_tilted_phase_audit(),
        "manifest": {
            "generator": GENERATOR_RELATIVE_PATH,
            "generator_sha256": _sha256(generator_path),
            "proof_source": PROOF_SOURCE_RELATIVE_PATH,
            "proof_source_sha256": _sha256(source_path),
            "note": NOTE_RELATIVE_PATH,
            "note_sha256": _sha256(note_path),
            "parent_result": PARENT_RESULT_RELATIVE_PATH,
            "parent_result_sha256": _sha256(parent_path),
            "parent_claim_checks": parent_checks,
            "default_command": DEFAULT_COMMAND,
            "python": platform.python_version(),
            "platform": platform.platform(),
            "arithmetic": MANIFEST_ARITHMETIC,
        },
    }
    validate_target_tilted_phase_result(payload, REPOSITORY)
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
