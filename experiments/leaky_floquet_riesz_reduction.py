#!/usr/bin/env python3
"""Generate the finite analytic leaky Floquet Riesz reduction."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from canard_control.leaky_floquet_riesz_reduction import (
    RESULT_RELATIVE_PATH,
    build_leaky_floquet_riesz_result,
    validate_leaky_floquet_riesz_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output", type=Path, default=REPOSITORY / RESULT_RELATIVE_PATH
    )
    arguments = parser.parse_args()
    result = build_leaky_floquet_riesz_result(REPOSITORY)
    validate_leaky_floquet_riesz_result(result, REPOSITORY)
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(arguments.output)


if __name__ == "__main__":
    main()

