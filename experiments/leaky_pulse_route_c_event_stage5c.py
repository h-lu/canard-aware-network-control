#!/usr/bin/env python3
"""Generate or audit the directed Stage-5C Route-C event certificate."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from canard_control.leaky_pulse_route_c_event_stage5c import (
    RESULT_RELATIVE_PATH,
    build_stage5c_result,
    validate_stage5c_result,
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
        help="replay the Stage-5B cells and the Stage-5C event proof",
    )
    arguments = parser.parse_args()

    if arguments.check:
        payload = json.loads(arguments.output.read_text(encoding="utf-8"))
        validate_stage5c_result(
            payload, REPOSITORY, recompute=arguments.recompute
        )
        print(arguments.output)
        print(payload["manifest"]["certificate_sha256"])
        return

    payload = build_stage5c_result(REPOSITORY)
    validate_stage5c_result(payload, REPOSITORY)
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    validate_stage5c_result(
        json.loads(arguments.output.read_text(encoding="utf-8")), REPOSITORY
    )
    print(arguments.output)
    print(payload["manifest"]["certificate_sha256"])


if __name__ == "__main__":
    main()
