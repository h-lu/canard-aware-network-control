#!/usr/bin/env python3
"""Generate or audit the directed Stage-5D event-history derivative."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from canard_control.leaky_pulse_event_aligned_derivative_stage5d import (
    RESULT_RELATIVE_PATH,
    build_stage5d_result,
    validate_stage5d_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output", type=Path, default=REPOSITORY / RESULT_RELATIVE_PATH
    )
    parser.add_argument("--check", action="store_true")
    parser.add_argument(
        "--recompute",
        action="store_true",
        help="replay Stage 5B and the Stage-5D first-variation tube",
    )
    arguments = parser.parse_args()

    if arguments.check:
        payload = json.loads(arguments.output.read_text(encoding="utf-8"))
        validate_stage5d_result(
            payload, REPOSITORY, recompute=arguments.recompute
        )
        print(arguments.output)
        print(payload["manifest"]["certificate_sha256"])
        return

    payload = build_stage5d_result(REPOSITORY)
    validate_stage5d_result(payload, REPOSITORY)
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    validate_stage5d_result(
        json.loads(arguments.output.read_text(encoding="utf-8")), REPOSITORY
    )
    print(arguments.output)
    print(payload["manifest"]["certificate_sha256"])


if __name__ == "__main__":
    main()
