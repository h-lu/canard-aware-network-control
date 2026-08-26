#!/usr/bin/env python3
"""Generate or check the Stage-5A correlated center-jet pilot."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from canard_control.leaky_pulse_parameter_jet_center_pilot import (
    RESULT_RELATIVE_PATH,
    build_center_jet_result,
    validate_center_jet_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output", type=Path, default=REPOSITORY / RESULT_RELATIVE_PATH
    )
    parser.add_argument(
        "--check", action="store_true", help="audit the registered pilot"
    )
    parser.add_argument(
        "--recompute",
        action="store_true",
        help="replay all three jet refinements and two direct endpoint flows",
    )
    arguments = parser.parse_args()

    if arguments.check:
        payload = json.loads(arguments.output.read_text(encoding="utf-8"))
        validate_center_jet_result(
            payload, REPOSITORY, recompute=arguments.recompute
        )
        print(arguments.output)
        print(payload["manifest"]["pilot_sha256"])
        return

    payload = build_center_jet_result(REPOSITORY)
    validate_center_jet_result(payload, REPOSITORY)
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    validate_center_jet_result(
        json.loads(arguments.output.read_text(encoding="utf-8")), REPOSITORY
    )
    print(arguments.output)
    print(payload["manifest"]["pilot_sha256"])


if __name__ == "__main__":
    main()
