#!/usr/bin/env python3
"""Generate the exact leaky reduced-history factorization record."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from canard_control.leaky_reduced_history import (
    RESULT_RELATIVE_PATH,
    build_leaky_reduced_history_result,
    validate_leaky_reduced_history_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=REPOSITORY / RESULT_RELATIVE_PATH,
    )
    arguments = parser.parse_args()
    payload = build_leaky_reduced_history_result(REPOSITORY)
    validate_leaky_reduced_history_result(payload, REPOSITORY)
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(arguments.output)


if __name__ == "__main__":
    main()
