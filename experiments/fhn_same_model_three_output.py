#!/usr/bin/env python3
"""Generate the same-model staged three-output target-ball certificate."""

from __future__ import annotations

import argparse
from dataclasses import asdict
from hashlib import sha256
import json
from pathlib import Path
import platform
import sys

import canard_control.fhn_same_model_three_output as theorem_source
from canard_control.fhn_same_model_three_output import (
    load_same_model_three_output,
)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--target-ball-result",
        type=Path,
        default=Path("experiments/results/fhn_response_target_ball.json"),
    )
    parser.add_argument(
        "--separator-result",
        type=Path,
        default=Path("experiments/results/fhn_same_model_separator.json"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("experiments/results/fhn_same_model_three_output.json"),
    )
    return parser.parse_args()


def _sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _parent_provenance(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    provenance = payload["provenance"]
    return {
        "result_sha256": _sha256(path),
        "generator": provenance["generator"],
        "generator_sha256": provenance["generator_sha256"],
        "proof_source_manifest": provenance["proof_source_manifest"],
    }


def main() -> None:
    arguments = parse_arguments()
    repository = Path(__file__).resolve().parents[1]
    certificate = load_same_model_three_output(
        arguments.target_ball_result,
        arguments.separator_result,
        repository=repository,
    )
    proof_source = Path(theorem_source.__file__).resolve()
    payload = {
        "provenance": {
            "generator": "experiments/fhn_same_model_three_output.py",
            "generator_sha256": _sha256(Path(__file__).resolve()),
            "argv": [sys.executable, *sys.argv],
            "default_command": (
                "PYTHONPATH=build/testdeps:src /usr/bin/python3 "
                "experiments/fhn_same_model_three_output.py"
            ),
            "python": platform.python_version(),
            "platform": platform.platform(),
            "arithmetic": (
                "exact block algebra and directed Decimal composition from "
                "public parent endpoints"
            ),
            "proof_source_manifest": {
                str(proof_source.relative_to(repository)): _sha256(proof_source)
            },
        },
        "source_evidence": {
            "target_ball_result_sha256": (
                certificate.target_ball_result_sha256
            ),
            "separator_result_sha256": certificate.separator_result_sha256,
            "shared_parameter_box_result_sha256": (
                certificate.shared_parameter_box_result_sha256
            ),
            "source_synchronous_model_id": (
                certificate.source_synchronous_model_id
            ),
            "certified_full_network_instance_id": (
                certificate.certified_full_network_instance_id
            ),
            "target_parent_provenance": _parent_provenance(
                arguments.target_ball_result
            ),
            "separator_parent_provenance": _parent_provenance(
                arguments.separator_result
            ),
            "staged_protocol": {
                "baseline_stage": (
                    "compute (F,R_h) using only (kappa_1,kappa_3); reset r "
                    "is absent from the periodic RFDE"
                ),
                "decision_stage": (
                    "prepare constant synchronous history with reset r and "
                    "use the collective recovery clamp until first hit"
                ),
                "operational_margin": "S_op=-r because r_c=0 exactly",
            },
        },
        "certificate": asdict(certificate),
        "scope": {
            "frequency_squared_range_operational_first_hit_margin_target_ball": (
                certificate.frequency_squared_range_operational_margin_target_ball_validated
            ),
            "same_baseline_staged_protocol": (
                certificate.same_baseline_staged_protocol_validated
            ),
            "unsquared_amplitude": certificate.unsquared_amplitude_validated,
            "physical_finite_pulse": certificate.physical_finite_pulse_validated,
            "biological_basin_beyond_channel_faces": (
                certificate.biological_basin_beyond_channel_faces_validated
            ),
            "noise_hardware_robustness": (
                certificate.noise_hardware_robustness_validated
            ),
            "unforced_onset": certificate.unforced_onset_validated,
            "maximal_canard_onset": certificate.maximal_canard_onset_validated,
            "periodic_attraction": certificate.periodic_attraction_validated,
            "general_topology": certificate.general_topology_validated,
            "issue_15_closed": certificate.issue_15_closed,
        },
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    arguments.output.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
