#!/usr/bin/env python3
"""Generate, fresh-replay, and atomically install the Stage-4L certificate."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import tempfile

from canard_control.leaky_inner_terminal_stable_row_stage4l import (
    RESULT_RELATIVE_PATH,
    build_stage4l_result,
    validate_stage4l_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]


def _atomic_write(destination: Path, payload: dict[str, object]) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    serialized = json.dumps(
        payload,
        indent=2,
        sort_keys=True,
        ensure_ascii=True,
        allow_nan=False,
    ) + "\n"
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{destination.name}.",
        suffix=".tmp",
        dir=destination.parent,
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
        help="source-check and fresh-replay the installed Stage-4L result",
    )
    arguments = parser.parse_args()
    destination = arguments.output.resolve()
    if arguments.check:
        payload = json.loads(destination.read_text(encoding="utf-8"))
        validate_stage4l_result(payload, REPOSITORY, recompute=True)
    else:
        payload = build_stage4l_result(REPOSITORY)
        # The second calculation is deliberately an independent fresh replay.
        validate_stage4l_result(payload, REPOSITORY, recompute=True)
        _atomic_write(destination, payload)
    print(destination)
    print(payload["manifest"]["artifact_sha256"])


if __name__ == "__main__":
    main()
