#!/usr/bin/env python3
"""Generate or independently check the Stage-3H signed-row size certificate."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from canard_control.leaky_outer_combined_row_stage3h_size import (
    RESULT_RELATIVE_PATH,
    build_outer_combined_row_stage3h_size_result,
    validate_outer_combined_row_stage3h_size_result,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    arguments = parser.parse_args()
    repository = Path(__file__).resolve().parents[1]
    result_path = repository / RESULT_RELATIVE_PATH
    if arguments.check:
        payload = json.loads(result_path.read_text())
        validate_outer_combined_row_stage3h_size_result(payload, repository)
    else:
        payload = build_outer_combined_row_stage3h_size_result(repository)
        validate_outer_combined_row_stage3h_size_result(payload, repository)
        temporary_path = result_path.with_suffix(".json.tmp")
        temporary_path.write_text(
            json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=True) + "\n"
        )
        temporary_path.replace(result_path)
    print(result_path)


if __name__ == "__main__":
    main()
