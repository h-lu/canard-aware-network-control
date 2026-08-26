#!/usr/bin/env python3
"""Generate or check the source-bound inner stable-manifold Stage-1 contract."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from canard_control.leaky_inner_stable_manifold_stage1_contract import (
    RESULT_RELATIVE_PATH,
    build_stage1_stable_manifold_result,
    validate_stage1_stable_manifold_result,
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
        help="validate the registered result without rewriting it",
    )
    arguments = parser.parse_args()

    if arguments.check:
        payload = json.loads(arguments.output.read_text(encoding="utf-8"))
        validate_stage1_stable_manifold_result(payload, REPOSITORY)
        print(arguments.output)
        return

    payload = build_stage1_stable_manifold_result(REPOSITORY)
    validate_stage1_stable_manifold_result(payload, REPOSITORY)
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(arguments.output)


if __name__ == "__main__":
    main()
