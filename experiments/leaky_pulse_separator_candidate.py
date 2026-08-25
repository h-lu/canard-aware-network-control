#!/usr/bin/env python3
"""Generate the source-bound physical-pulse separator candidate."""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import platform

import numpy as np
import scipy

from canard_control.leaky_pulse_separator_candidate import (
    ARITHMETIC_SCOPE,
    DEFAULT_COMMAND,
    EXPECTED_CANDIDATE_SHA256,
    GENERATOR_RELATIVE_PATH,
    MODEL_SOURCE_RELATIVE_PATH,
    NOTE_RELATIVE_PATH,
    PARENT_ARTIFACT_RESULT_RELATIVE_PATH,
    PARENT_ARTIFACT_SOURCE_RELATIVE_PATH,
    RESULT_RELATIVE_PATH,
    SCHEMA_ID,
    SOURCE_RELATIVE_PATH,
    TERMINAL_HISTORY_SOURCE_RELATIVE_PATH,
    build_candidate,
    canonical_sha256,
    validate_separator_candidate_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]


def _sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _manifest(candidate: dict[str, object]) -> dict[str, object]:
    sources = {
        "source": SOURCE_RELATIVE_PATH,
        "generator": GENERATOR_RELATIVE_PATH,
        "note": NOTE_RELATIVE_PATH,
        "model_source": MODEL_SOURCE_RELATIVE_PATH,
        "terminal_history_source": TERMINAL_HISTORY_SOURCE_RELATIVE_PATH,
        "parent_artifact_source": PARENT_ARTIFACT_SOURCE_RELATIVE_PATH,
        "parent_artifact_result": PARENT_ARTIFACT_RESULT_RELATIVE_PATH,
    }
    manifest: dict[str, object] = {
        "schema_id": SCHEMA_ID,
        "candidate_sha256": canonical_sha256(candidate),
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
    parser.add_argument(
        "--digest-only",
        action="store_true",
        help="compute the body and print its canonical digest without writing",
    )
    arguments = parser.parse_args()
    parent = json.loads(
        (REPOSITORY / PARENT_ARTIFACT_RESULT_RELATIVE_PATH).read_text(
            encoding="utf-8"
        )
    )
    candidate = build_candidate(parent)
    digest = canonical_sha256(candidate)
    if arguments.digest_only:
        print(digest)
        print(json.dumps(candidate["convergence"], indent=2))
        for resolution in candidate["resolutions"]:
            roots = [
                row["pulse_amplitude"]["decimal"]
                for row in resolution["shooting_roots"]
            ]
            scaled = [
                row["multiplier_scaled_derivative"]["decimal"]
                for row in resolution["shooting_roots"]
            ]
            print(resolution["step_count"], roots, scaled)
        print(
            "integration_refinement",
            [
                row["pulse_amplitude"]["decimal"]
                for row in candidate["integration_refinement"]
            ],
        )
        return
    if EXPECTED_CANDIDATE_SHA256 is None:
        raise RuntimeError(
            "inspect --digest-only output and register the candidate digest first"
        )
    if digest != EXPECTED_CANDIDATE_SHA256:
        raise RuntimeError("generated separator body differs from registered digest")
    payload = {"candidate": candidate, "manifest": _manifest(candidate)}
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    validate_separator_candidate_result(payload, REPOSITORY)
    print(arguments.output)
    print(digest)


if __name__ == "__main__":
    main()
