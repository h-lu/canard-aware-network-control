#!/usr/bin/env python3
"""Generate, validate, or independently replay the Stage-4E certificate."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from canard_control.leaky_shared_yqq_deflation_stage4e import (
    RESULT_RELATIVE_PATH,
    build_stage4e_result,
    validate_stage4e_result,
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
        help="validate the registered artifact and all source/parent hashes",
    )
    parser.add_argument(
        "--replay",
        action="store_true",
        help="recompute independently and require the registered artifact digest",
    )
    arguments = parser.parse_args()
    registered = None
    if arguments.output.exists():
        registered = json.loads(arguments.output.read_text(encoding="utf-8"))
    if arguments.check:
        if registered is None:
            raise FileNotFoundError(arguments.output)
        validate_stage4e_result(registered, REPOSITORY)
        print(arguments.output)
        return
    payload = build_stage4e_result(REPOSITORY)
    validate_stage4e_result(payload, REPOSITORY)
    if arguments.replay:
        if registered is None:
            raise FileNotFoundError(arguments.output)
        validate_stage4e_result(registered, REPOSITORY)
        if (
            payload["manifest"]["artifact_sha256"]
            != registered["manifest"]["artifact_sha256"]
        ):
            raise ArithmeticError("independent Stage-4E replay digest changed")
        print(payload["manifest"]["artifact_sha256"])
        return
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(arguments.output)


if __name__ == "__main__":
    main()
