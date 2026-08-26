#!/usr/bin/env python3
"""Generate or statically audit the Stage-4V certificate."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from canard_control.leaky_inner_logarithmic_event_tube_stage4v import (
    RESULT_RELATIVE_PATH,
    build_stage4v_result,
    validate_stage4v_result,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="validate the registered artifact without recomputing its arithmetic",
    )
    args = parser.parse_args()
    repository = Path(__file__).resolve().parents[1]
    result_path = repository / RESULT_RELATIVE_PATH
    if args.check:
        payload = json.loads(result_path.read_text(encoding="utf-8"))
        validate_stage4v_result(payload, repository, recompute=False)
        print("Stage-4V static audit passed")
        return
    payload = build_stage4v_result(repository)
    result_path.parent.mkdir(parents=True, exist_ok=True)
    result_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(result_path)


if __name__ == "__main__":
    main()
