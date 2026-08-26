#!/usr/bin/env python3
"""Generate or check the direct outer-return Stage-1 contract."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from canard_control.leaky_outer_phase_fixed_return_stage1 import (
    RESULT_RELATIVE_PATH,
    build_outer_phase_fixed_return_result,
    validate_outer_phase_fixed_return_result,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    arguments = parser.parse_args()
    repository = Path(__file__).resolve().parents[1]
    result_path = repository / RESULT_RELATIVE_PATH
    if arguments.check:
        payload = json.loads(result_path.read_text())
        validate_outer_phase_fixed_return_result(payload, repository)
    else:
        payload = build_outer_phase_fixed_return_result(repository)
        result_path.write_text(
            json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=True) + "\n"
        )
        validate_outer_phase_fixed_return_result(payload, repository)
    print(result_path)


if __name__ == "__main__":
    main()
