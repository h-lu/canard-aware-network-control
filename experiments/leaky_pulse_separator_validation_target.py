#!/usr/bin/env python3
"""Generate the source-bound narrow pulse-separator validation target."""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import platform

import numpy as np
import scipy

from canard_control.leaky_pulse_separator_validation_target import (
    ARITHMETIC_SCOPE,
    DEFAULT_COMMAND,
    EXPECTED_TARGET_SHA256,
    GENERATOR_RELATIVE_PATH,
    NOTE_RELATIVE_PATH,
    PARENT_CANDIDATE_RESULT_RELATIVE_PATH,
    PARENT_CANDIDATE_SOURCE_RELATIVE_PATH,
    PARENT_ORBIT_RESULT_RELATIVE_PATH,
    RESULT_RELATIVE_PATH,
    SCHEMA_ID,
    SOURCE_RELATIVE_PATH,
    build_target,
    canonical_sha256,
    validate_target_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]


def _sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _manifest(target: dict[str, object]) -> dict[str, object]:
    sources = {
        "source": SOURCE_RELATIVE_PATH,
        "generator": GENERATOR_RELATIVE_PATH,
        "note": NOTE_RELATIVE_PATH,
        "parent_candidate_source": PARENT_CANDIDATE_SOURCE_RELATIVE_PATH,
        "parent_candidate_result": PARENT_CANDIDATE_RESULT_RELATIVE_PATH,
        "parent_orbit_result": PARENT_ORBIT_RESULT_RELATIVE_PATH,
    }
    manifest: dict[str, object] = {
        "schema_id": SCHEMA_ID,
        "target_sha256": canonical_sha256(target),
        "default_command": DEFAULT_COMMAND,
        "arithmetic_scope": ARITHMETIC_SCOPE,
        "python": platform.python_version(),
        "platform": platform.platform(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
    }
    for name, relative in sources.items():
        manifest[name] = relative
        manifest[f"{name}_sha256"] = _sha256(REPOSITORY / relative)
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=REPOSITORY / RESULT_RELATIVE_PATH,
    )
    parser.add_argument("--digest-only", action="store_true")
    arguments = parser.parse_args()
    parent_candidate = json.loads(
        (REPOSITORY / PARENT_CANDIDATE_RESULT_RELATIVE_PATH).read_text(
            encoding="utf-8"
        )
    )
    parent_orbit = json.loads(
        (REPOSITORY / PARENT_ORBIT_RESULT_RELATIVE_PATH).read_text(
            encoding="utf-8"
        )
    )
    target = build_target(parent_candidate, parent_orbit, REPOSITORY)
    digest = canonical_sha256(target)
    if arguments.digest_only:
        print(digest)
        print(json.dumps(target["observed_margins"], indent=2))
        for row in target["sample_rows"]:
            print(
                row["pulse_amplitude"]["decimal"],
                row["third_return_coordinate"]["decimal"],
                row["centered_difference_derivative"]["decimal"],
                row["sampled_reduced_sup_distance"]["decimal"],
            )
        return
    if EXPECTED_TARGET_SHA256 is None:
        raise RuntimeError("inspect --digest-only output and register its digest")
    if digest != EXPECTED_TARGET_SHA256:
        raise RuntimeError("generated separator target differs from registered body")
    payload = {"target": target, "manifest": _manifest(target)}
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    validate_target_result(payload, REPOSITORY)
    print(arguments.output)


if __name__ == "__main__":
    main()
