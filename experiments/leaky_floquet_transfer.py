#!/usr/bin/env python3
"""Generate the source-bound neutral-Floquet transfer artifact."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from canard_control.leaky_floquet_transfer import (
    EXPECTED_ARTIFACT_SHA256,
    RESULT_RELATIVE_PATH,
    build_leaky_floquet_transfer_artifact,
    validate_leaky_floquet_transfer_artifact,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="override the tracked result path",
    )
    parser.add_argument(
        "--stdout",
        action="store_true",
        help="also print the canonical payload",
    )
    args = parser.parse_args()

    repository = Path(__file__).resolve().parents[1]
    payload = build_leaky_floquet_transfer_artifact(repository)
    if EXPECTED_ARTIFACT_SHA256 is not None:
        validate_leaky_floquet_transfer_artifact(
            payload, repository, recompute=False
        )
    output = args.output or repository / RESULT_RELATIVE_PATH
    output.parent.mkdir(parents=True, exist_ok=True)
    rendered = json.dumps(
        payload,
        indent=2,
        sort_keys=True,
        ensure_ascii=False,
        allow_nan=False,
    ) + "\n"
    output.write_text(rendered, encoding="utf-8")
    if args.stdout:
        print(rendered, end="")
    else:
        print(output.relative_to(repository))


if __name__ == "__main__":
    main()
