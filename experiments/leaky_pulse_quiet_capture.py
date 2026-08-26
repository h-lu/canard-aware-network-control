#!/usr/bin/env python3
"""Generate the directed ``J=3/10`` physical-pulse quiet-capture result."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from canard_control.leaky_pulse_quiet_capture import (
    RESULT_RELATIVE_PATH,
    build_pulse_quiet_capture_result,
    validate_pulse_quiet_capture_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]
DEFAULT_RESULT = REPOSITORY / RESULT_RELATIVE_PATH


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_RESULT)
    arguments = parser.parse_args()
    payload = build_pulse_quiet_capture_result(REPOSITORY)
    validate_pulse_quiet_capture_result(payload, REPOSITORY)
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    validate_pulse_quiet_capture_result(
        json.loads(arguments.output.read_text(encoding="utf-8")),
        REPOSITORY,
    )
    print(arguments.output)
    print(payload["manifest"]["certificate_sha256"])


if __name__ == "__main__":
    main()
