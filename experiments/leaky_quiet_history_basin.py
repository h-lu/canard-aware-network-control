#!/usr/bin/env python3
"""Generate the exact leaky quiet-history basin certificate."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from canard_control.leaky_quiet_history_basin import (
    RESULT_RELATIVE_PATH,
    build_quiet_history_basin_result,
    validate_quiet_history_basin_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--stdout", action="store_true")
    return parser.parse_args()


def main() -> None:
    arguments = parse_arguments()
    payload = build_quiet_history_basin_result(REPOSITORY)
    validate_quiet_history_basin_result(payload, REPOSITORY)
    encoded = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    output = arguments.output or REPOSITORY / RESULT_RELATIVE_PATH
    if not output.is_absolute():
        output = REPOSITORY / output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(encoded, encoding="utf-8")
    if arguments.stdout:
        print(encoded, end="")
    else:
        print(output)
        print(
            "certificate_sha256="
            + payload["manifest"]["certificate_sha256"]
        )


if __name__ == "__main__":
    main()
