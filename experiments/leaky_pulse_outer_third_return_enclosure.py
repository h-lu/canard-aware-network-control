#!/usr/bin/env python3
"""Generate or check the directed ``J=8/25`` third-return enclosure."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from canard_control.leaky_pulse_outer_third_return_enclosure import (
    RESULT_RELATIVE_PATH,
    build_third_return_result,
    validate_third_return_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output", type=Path, default=REPOSITORY / RESULT_RELATIVE_PATH
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="validate the registered enclosure without replaying it",
    )
    parser.add_argument(
        "--recompute",
        action="store_true",
        help="replay every directed time and history cell during checking",
    )
    arguments = parser.parse_args()

    if arguments.check:
        payload = json.loads(arguments.output.read_text(encoding="utf-8"))
        validate_third_return_result(
            payload, REPOSITORY, recompute=arguments.recompute
        )
        print(arguments.output)
        print(payload["manifest"]["certificate_sha256"])
        return

    payload = build_third_return_result(REPOSITORY)
    validate_third_return_result(payload, REPOSITORY)
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    validate_third_return_result(
        json.loads(arguments.output.read_text(encoding="utf-8")), REPOSITORY
    )
    print(arguments.output)
    print(payload["manifest"]["certificate_sha256"])


if __name__ == "__main__":
    main()
