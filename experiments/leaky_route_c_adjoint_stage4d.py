#!/usr/bin/env python3
"""Generate or check the source-bound Stage-4D adjoint bridge."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from canard_control.leaky_route_c_adjoint_stage4d import (
    RESULT_RELATIVE_PATH,
    build_stage4d_result,
    validate_stage4d_result,
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
        help="validate the registered Stage-4D result without rewriting it",
    )
    arguments = parser.parse_args()
    if arguments.check:
        payload = json.loads(arguments.output.read_text(encoding="utf-8"))
        validate_stage4d_result(payload, REPOSITORY)
        print(arguments.output)
        return
    payload = build_stage4d_result(REPOSITORY)
    validate_stage4d_result(payload, REPOSITORY)
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(arguments.output)


if __name__ == "__main__":
    main()
