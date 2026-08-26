#!/usr/bin/env python3
"""Generate or check the outer-tube and two-sided routing contract."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from canard_control.leaky_outer_two_sided_routing_contract import (
    RESULT_RELATIVE_PATH,
    build_outer_two_sided_routing_result,
    validate_outer_two_sided_routing_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=REPOSITORY / RESULT_RELATIVE_PATH,
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="validate the registered contract without rewriting it",
    )
    arguments = parser.parse_args()

    if arguments.check:
        payload = json.loads(arguments.output.read_text(encoding="utf-8"))
        validate_outer_two_sided_routing_result(payload, REPOSITORY)
        print(arguments.output)
        return

    payload = build_outer_two_sided_routing_result(REPOSITORY)
    validate_outer_two_sided_routing_result(payload, REPOSITORY)
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(arguments.output)


if __name__ == "__main__":
    main()
