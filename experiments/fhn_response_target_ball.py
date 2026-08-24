#!/usr/bin/env python3
"""Derive the directed FHN target ball from the tracked response box."""

from __future__ import annotations

import argparse
from dataclasses import asdict
from hashlib import sha256
import json
from pathlib import Path
import platform
import sys

import gmpy2

import canard_control.directed_interval as directed_interval_source
import canard_control.fhn_response_target_ball as target_ball_source
from canard_control.fhn_response_target_ball import load_directed_target_ball


_TRACKED_FLOQUET_SHA256 = (
    "c2f93b6cfe6a8e0df3b341476fbe45a83f6fecc0398dbb7340a5213a55357a31"
)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--parameter-box-result",
        type=Path,
        default=Path("experiments/results/fhn_periodic_parameter_box.json"),
    )
    parser.add_argument(
        "--floquet-result",
        type=Path,
        default=Path("experiments/results/fhn_bloch_outer_validation.json"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("experiments/results/fhn_response_target_ball.json"),
    )
    parser.add_argument("--precision", type=int, default=160)
    return parser.parse_args()


def _sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _require_companion_floquet(path: Path) -> dict:
    digest = _sha256(path)
    if digest != _TRACKED_FLOQUET_SHA256:
        raise ValueError(
            "companion Floquet result SHA-256 mismatch: "
            f"expected {_TRACKED_FLOQUET_SHA256}, got {digest}"
        )
    payload = json.loads(path.read_text(encoding="utf-8"))
    scope = payload["scope"]
    if not scope["synchronous_orbital_hyperbolicity"]:
        raise ValueError("companion synchronous Floquet theorem is not validated")
    if scope["attraction"] or scope["full_network_transverse_stability"]:
        raise ValueError("companion Floquet record has an invalid scope promotion")
    return {
        "result_sha256": digest,
        "synchronous_orbital_hyperbolicity": True,
        "attraction": False,
        "full_network_transverse_stability": False,
    }


def main() -> None:
    arguments = parse_arguments()
    repository = Path(__file__).resolve().parents[1]
    certificate = load_directed_target_ball(
        arguments.parameter_box_result,
        precision=arguments.precision,
    )
    companion = _require_companion_floquet(arguments.floquet_result)
    if (
        json.loads(arguments.floquet_result.read_text(encoding="utf-8"))[
            "source_evidence"
        ]["parameter_box_result_sha256"]
        != certificate.source_result_sha256
    ):
        raise ValueError("response and Floquet certificates use different branches")

    source_paths = {
        "src/canard_control/directed_interval.py": Path(
            directed_interval_source.__file__
        ).resolve(),
        "src/canard_control/fhn_response_target_ball.py": Path(
            target_ball_source.__file__
        ).resolve(),
    }
    payload = {
        "provenance": {
            "generator": "experiments/fhn_response_target_ball.py",
            "generator_sha256": _sha256(Path(__file__).resolve()),
            "argv": [sys.executable, *sys.argv],
            "default_command": (
                "PYTHONPATH=build/testdeps:src /usr/bin/python3 "
                "experiments/fhn_response_target_ball.py"
            ),
            "python": platform.python_version(),
            "platform": platform.platform(),
            "gmpy2": gmpy2.version(),
            "mpfr": gmpy2.mpfr_version(),
            "rounding": "MPFR RoundDown/RoundUp at every theorem endpoint",
            "proof_source_manifest": {
                str(path.relative_to(repository)): _sha256(path)
                for path in source_paths.values()
            },
        },
        "source_evidence": {
            "parameter_box_result_sha256": certificate.source_result_sha256,
            "companion_floquet": companion,
        },
        "target_ball": asdict(certificate),
        "scope": {
            "base_frequency_squared_range_target_ball": (
                certificate.base_frequency_squared_range_target_ball_validated
            ),
            "base_squared_range_target_ball_requires_second_sensitivities": (
                certificate.second_sensitivity_required_for_base_target_ball
            ),
            "synchronous_orbital_hyperbolicity": companion[
                "synchronous_orbital_hyperbolicity"
            ],
            "attraction": False,
            "full_network_transverse_stability": False,
            "calibrated_reset_transfer": "conditional",
            "calibrated_three_output_target_ball": False,
            "same_model_periodic_separator_bridge": False,
            "physical_pulse_onset": False,
            "issue_15_closed": False,
        },
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    arguments.output.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
