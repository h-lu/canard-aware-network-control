#!/usr/bin/env python3
"""Generate or statically validate the Stage-4J source-bound pilot."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from canard_control.leaky_inner_projected_stable_flow_stage4j_pilot import (
    RESULT_RELATIVE_PATH,
    build_stage4j_pilot_result,
    validate_stage4j_pilot_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output", type=Path, default=REPOSITORY / RESULT_RELATIVE_PATH
    )
    parser.add_argument("--check", action="store_true")
    arguments = parser.parse_args()
    if arguments.check:
        payload = json.loads(arguments.output.read_text(encoding="utf-8"))
        validate_stage4j_pilot_result(payload, REPOSITORY)
        print(arguments.output)
        return
    payload = build_stage4j_pilot_result(REPOSITORY)
    validate_stage4j_pilot_result(payload, REPOSITORY)
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(arguments.output)


if __name__ == "__main__":
    main()
