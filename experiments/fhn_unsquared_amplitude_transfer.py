#!/usr/bin/env python3
"""Build the source-bound FHN unsquared-amplitude transfer certificate."""

from __future__ import annotations

import argparse
from dataclasses import asdict
from hashlib import sha256
import json
from pathlib import Path
import platform
import sys

import gmpy2
import numpy as np

import canard_control.directed_interval as directed_interval_source
import canard_control.fhn_periodic_candidate as periodic_candidate_source
import canard_control.fhn_periodic_directed_validation as directed_validation_source
import canard_control.fhn_periodic_infinite_validation as infinite_validation_source
import canard_control.fhn_periodic_parameter_box as parameter_box_source
import canard_control.fhn_response_target_ball as target_ball_source
import canard_control.fhn_unsquared_amplitude_transfer as amplitude_source
from canard_control.fhn_unsquared_amplitude_transfer import (
    orbit_from_binary64_candidate_payload,
    validate_unsquared_amplitude_transfer,
)


TRACKED_CANDIDATE_SHA256 = (
    "7437514175586665b1bf10831793427e42d8a9cbd736536444be4a98064a3c28"
)
TRACKED_PARAMETER_BOX_SHA256 = (
    "ff13b5352c2b4e9898a4044be63fd490a3e7bb4217445a6a062188c2457c22a0"
)


def _sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--candidate",
        type=Path,
        default=Path("experiments/results/fhn_periodic_box_candidate.json"),
    )
    parser.add_argument(
        "--parameter-box",
        type=Path,
        default=Path("experiments/results/fhn_periodic_parameter_box.json"),
    )
    parser.add_argument(
        "--squared-target-ball",
        type=Path,
        default=Path("experiments/results/fhn_response_target_ball.json"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "experiments/results/fhn_unsquared_amplitude_transfer.json"
        ),
    )
    return parser.parse_args()


def main() -> None:
    arguments = parse_arguments()
    candidate_digest = _sha256(arguments.candidate)
    parameter_digest = _sha256(arguments.parameter_box)
    if candidate_digest != TRACKED_CANDIDATE_SHA256:
        raise ValueError("candidate Fourier record SHA-256 mismatch")
    if parameter_digest != TRACKED_PARAMETER_BOX_SHA256:
        raise ValueError("parameter-box record SHA-256 mismatch")

    candidate_payload = json.loads(
        arguments.candidate.read_text(encoding="utf-8")
    )
    orbit = orbit_from_binary64_candidate_payload(candidate_payload)
    audit = validate_unsquared_amplitude_transfer(
        orbit, candidate_source_sha256=candidate_digest
    )

    parameter_payload = json.loads(
        arguments.parameter_box.read_text(encoding="utf-8")
    )
    replayed_validation = json.loads(
        json.dumps(asdict(audit.parameter_validation), sort_keys=True)
    )
    if replayed_validation != parameter_payload["validation"]:
        raise ValueError(
            "fresh exact-candidate replay does not reproduce the tracked "
            "parameter validation"
        )
    candidate_summary = parameter_payload["candidate_input"]
    if (
        candidate_summary["node_count"] != len(orbit.state)
        or candidate_summary["period"] != orbit.period
        or candidate_summary["binary_collocation_residual_inf"]
        != orbit.collocation_residual_inf
        or candidate_summary["binary_oversampled_residual_inf"]
        != orbit.oversampled_residual_inf
        or candidate_summary["binary_spectral_tail_l1"]
        != orbit.spectral_tail_l1
        or candidate_summary["claim_status"] != "diagnostic midpoint only"
    ):
        raise ValueError("candidate summary does not match the replayed polynomial")

    squared_target_payload = json.loads(
        arguments.squared_target_ball.read_text(encoding="utf-8")
    )
    squared_target = squared_target_payload["target_ball"]
    if not squared_target["base_frequency_squared_range_target_ball_validated"]:
        raise ValueError("source squared-range target ball is not validated")
    if (
        squared_target["source_result_sha256"] != parameter_digest
        or squared_target["certified_output_ball_radius_lower"]
        != audit.certificate.squared_range_target_radius_lower
    ):
        raise ValueError("fresh replay and tracked squared target ball disagree")

    repository = Path(__file__).resolve().parents[1]
    source_paths = tuple(
        Path(module.__file__).resolve()
        for module in (
            directed_interval_source,
            periodic_candidate_source,
            directed_validation_source,
            infinite_validation_source,
            parameter_box_source,
            target_ball_source,
            amplitude_source,
        )
    )
    payload = {
        "provenance": {
            "generator": "experiments/fhn_unsquared_amplitude_transfer.py",
            "generator_sha256": _sha256(Path(__file__).resolve()),
            "argv": [sys.executable, *sys.argv],
            "default_command": (
                "PYTHONPATH=build/testdeps:src /usr/bin/python3 "
                "experiments/fhn_unsquared_amplitude_transfer.py"
            ),
            "python": platform.python_version(),
            "platform": platform.platform(),
            "numpy": np.__version__,
            "gmpy2": gmpy2.version(),
            "mpfr": gmpy2.mpfr_version(),
            "rounding": "MPFR RoundDown/RoundUp at every theorem endpoint",
            "proof_source_manifest": {
                str(path.relative_to(repository)): _sha256(path)
                for path in source_paths
            },
        },
        "source_evidence": {
            "candidate_result_sha256": candidate_digest,
            "parameter_box_result_sha256": parameter_digest,
            "squared_target_ball_result_sha256": _sha256(
                arguments.squared_target_ball
            ),
            "parameter_validation_exact_replay": True,
            "squared_target_radius_exact_match": True,
        },
        "certificate": asdict(audit.certificate),
        "scope": {
            "uniform_unsquared_amplitude_enclosure": True,
            "frequency_unsquared_amplitude_target_ball": True,
            "binary64_candidate_is_exact_orbit": False,
            "calibrated_safety_coordinate_transfer": "conditional",
            "calibrated_three_output_target_ball": False,
            "physical_pulse_onset": False,
        },
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    arguments.output.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
