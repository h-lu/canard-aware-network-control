"""Generate or check the local outer Grushin pole-subtraction certificate."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from canard_control.leaky_floquet_outer_grushin_stage1 import (
    RESULT_RELATIVE_PATH,
    build_leaky_outer_grushin_stage1_result,
    validate_leaky_outer_grushin_stage1_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=REPOSITORY / RESULT_RELATIVE_PATH,
    )
    parser.add_argument("--check", action="store_true")
    arguments = parser.parse_args()
    if arguments.check:
        payload = json.loads(arguments.output.read_text(encoding="utf-8"))
        validate_leaky_outer_grushin_stage1_result(payload, REPOSITORY)
        print(arguments.output)
        return
    payload = build_leaky_outer_grushin_stage1_result(REPOSITORY)
    validate_leaky_outer_grushin_stage1_result(payload, REPOSITORY)
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(arguments.output)


if __name__ == "__main__":
    main()
