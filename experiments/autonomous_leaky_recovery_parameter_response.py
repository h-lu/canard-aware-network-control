#!/usr/bin/env python3
"""Generate the source-bound leaky ``(a,kappa_3)`` response artifact."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from canard_control.leaky_periodic_parameter_response import (
    EXPECTED_ARTIFACT_SHA256,
    RESULT_RELATIVE_PATH,
    build_artifact,
    canonical_sha256,
    manifest_for_artifact,
    validate_parameter_response_artifact,
)


REPOSITORY = Path(__file__).resolve().parents[1]


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--stdout", action="store_true")
    parser.add_argument(
        "--rebind-existing",
        action="store_true",
        help=(
            "retain a registered artifact body and rebuild only its source "
            "manifest"
        ),
    )
    return parser.parse_args()


def main() -> None:
    arguments = parse_arguments()
    output = arguments.output or (REPOSITORY / RESULT_RELATIVE_PATH)
    if not output.is_absolute():
        output = REPOSITORY / output
    if arguments.rebind_existing:
        if not isinstance(EXPECTED_ARTIFACT_SHA256, str):
            raise ValueError("cannot rebind an unregistered response body")
        existing = json.loads(output.read_text(encoding="utf-8"))
        artifact = existing.get("artifact")
        if not isinstance(artifact, dict):
            raise ValueError("existing response body is missing")
        if canonical_sha256(artifact) != EXPECTED_ARTIFACT_SHA256:
            raise ValueError("existing response body is not registered")
    else:
        artifact = build_artifact(REPOSITORY)
    payload = {
        "artifact": artifact,
        "manifest": manifest_for_artifact(artifact, REPOSITORY),
    }
    if isinstance(EXPECTED_ARTIFACT_SHA256, str):
        validate_parameter_response_artifact(payload, REPOSITORY)
    encoded = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(encoded, encoding="utf-8")
    if arguments.stdout:
        print(encoded, end="")
    else:
        print(output)
        print(f"artifact_sha256={payload['manifest']['artifact_sha256']}")


if __name__ == "__main__":
    main()
