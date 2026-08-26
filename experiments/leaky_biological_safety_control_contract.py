#!/usr/bin/env python3
"""Generate or check the biological frequency--amplitude--safety contract."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from canard_control.leaky_biological_safety_control_contract import (
    RESULT_RELATIVE_PATH,
    make_payload,
    validate_biological_safety_control_result,
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
        validate_biological_safety_control_result(payload, REPOSITORY)
        print(arguments.output)
        print(payload["manifest"]["certificate_sha256"])
        return

    payload = make_payload(REPOSITORY)
    validate_biological_safety_control_result(payload, REPOSITORY)
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    validate_biological_safety_control_result(
        json.loads(arguments.output.read_text(encoding="utf-8")), REPOSITORY
    )
    print(arguments.output)
    print(payload["manifest"]["certificate_sha256"])


if __name__ == "__main__":
    main()
