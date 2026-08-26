#!/usr/bin/env python3
"""Generate the leaky finite-network transverse Halanay certificate."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from canard_control.leaky_dobrushin_transverse_halanay import (
    RESULT_RELATIVE_PATH,
    build_leaky_dobrushin_transverse_result,
    validate_leaky_dobrushin_transverse_result,
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
    payload = build_leaky_dobrushin_transverse_result(REPOSITORY)
    validate_leaky_dobrushin_transverse_result(payload, REPOSITORY)
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(arguments.output)


if __name__ == "__main__":
    main()
