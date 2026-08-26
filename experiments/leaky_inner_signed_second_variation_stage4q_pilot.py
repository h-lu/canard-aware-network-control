#!/usr/bin/env python3
"""Generate, validate, and atomically install the Stage-4Q pilot."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import tempfile

from canard_control.leaky_inner_signed_second_variation_stage4q_pilot import (
    RESULT_RELATIVE_PATH,
    build_stage4q_result,
    validate_stage4q_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]


def _atomic_write(destination: Path, payload: dict[str, object]) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    serialized = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{destination.name}.", suffix=".tmp", dir=destination.parent
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(serialized)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, destination)
        directory_descriptor = os.open(destination.parent, os.O_RDONLY)
        try:
            os.fsync(directory_descriptor)
        finally:
            os.close(directory_descriptor)
    finally:
        temporary.unlink(missing_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output", type=Path, default=REPOSITORY / RESULT_RELATIVE_PATH
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="validate the installed result without repeating the heavy replay",
    )
    parser.add_argument(
        "--fresh-check",
        action="store_true",
        help="validate the installed result and repeat the full numerical replay",
    )
    arguments = parser.parse_args()
    if arguments.check or arguments.fresh_check:
        payload = json.loads(arguments.output.read_text(encoding="utf-8"))
        validate_stage4q_result(
            payload, REPOSITORY, recompute=arguments.fresh_check
        )
        print(arguments.output)
        print(payload["manifest"]["numeric_core_sha256"])
        return

    payload = build_stage4q_result(REPOSITORY)
    # Validate the complete in-memory payload before the atomic replacement.
    validate_stage4q_result(payload, REPOSITORY, recompute=False)
    _atomic_write(arguments.output, payload)
    print(arguments.output)
    print(payload["manifest"]["numeric_core_sha256"])
    print(payload["manifest"]["pilot_sha256"])


if __name__ == "__main__":
    main()
