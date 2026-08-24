#!/usr/bin/env python3
"""Generate the same-model frequency--amplitude--safety certificate."""

from __future__ import annotations

import argparse
from dataclasses import asdict
from hashlib import sha256
import json
from pathlib import Path
import platform
import sys

import canard_control.fhn_same_model_amplitude_safety as theorem_source
from canard_control.fhn_same_model_amplitude_safety import (
    load_same_model_amplitude_safety,
    validate_same_model_amplitude_safety_result_payload,
)


def _sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--amplitude-result",
        type=Path,
        default=Path(
            "experiments/results/fhn_unsquared_amplitude_transfer.json"
        ),
    )
    parser.add_argument(
        "--three-output-result",
        type=Path,
        default=Path("experiments/results/fhn_same_model_three_output.json"),
    )
    parser.add_argument(
        "--separator-result",
        type=Path,
        default=Path("experiments/results/fhn_same_model_separator.json"),
    )
    parser.add_argument(
        "--parameter-box-result",
        type=Path,
        default=Path("experiments/results/fhn_periodic_parameter_box.json"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "experiments/results/fhn_same_model_amplitude_safety.json"
        ),
    )
    return parser.parse_args()


def _parent_provenance(path: Path) -> dict[str, object]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    provenance = payload["provenance"]
    result: dict[str, object] = {
        "result_sha256": _sha256(path),
        "generator": provenance["generator"],
    }
    for field in ("generator_sha256", "proof_source_manifest"):
        if field in provenance:
            result[field] = provenance[field]
    return result


def main() -> None:
    arguments = parse_arguments()
    repository = Path(__file__).resolve().parents[1]
    certificate = load_same_model_amplitude_safety(
        arguments.amplitude_result,
        arguments.three_output_result,
        arguments.separator_result,
        arguments.parameter_box_result,
        repository=repository,
    )
    source = Path(theorem_source.__file__).resolve()
    payload = {
        "provenance": {
            "generator": "experiments/fhn_same_model_amplitude_safety.py",
            "generator_sha256": _sha256(Path(__file__).resolve()),
            "argv": [sys.executable, *sys.argv],
            "default_command": (
                "PYTHONPATH=build/testdeps:src /usr/bin/python3 "
                "experiments/fhn_same_model_amplitude_safety.py"
            ),
            "python": platform.python_version(),
            "platform": platform.platform(),
            "arithmetic": (
                "exact reset translation and directed Decimal upper/lower "
                "composition of the three-dimensional inverse amplitude map"
            ),
            "proof_source_manifest": {
                str(source.relative_to(repository)): _sha256(source)
            },
        },
        "source_evidence": {
            "amplitude_result_sha256": certificate.amplitude_result_sha256,
            "three_output_result_sha256": (
                certificate.three_output_result_sha256
            ),
            "separator_result_sha256": certificate.separator_result_sha256,
            "parameter_box_result_sha256": (
                certificate.parameter_box_result_sha256
            ),
            "squared_target_ball_result_sha256": (
                certificate.squared_target_ball_result_sha256
            ),
            "source_synchronous_model_id": (
                certificate.source_synchronous_model_id
            ),
            "certified_full_network_instance_id": (
                certificate.certified_full_network_instance_id
            ),
            "amplitude_parent_provenance": _parent_provenance(
                arguments.amplitude_result
            ),
            "three_output_parent_provenance": _parent_provenance(
                arguments.three_output_result
            ),
            "separator_parent_provenance": _parent_provenance(
                arguments.separator_result
            ),
            "parameter_box_parent_provenance": _parent_provenance(
                arguments.parameter_box_result
            ),
            "recenter_identity": (
                "Q_R(b,r0+u)-Q_R(b_c,r0)=(P(b)-P(b_c),-u)"
            ),
            "inverse_amplitude_map": (
                "(dF,dA,dS)->(dF,2*A_c*dA+dA^2,dS)"
            ),
        },
        "certificate": asdict(certificate),
        "scope": {
            "frequency_unsquared_amplitude_operational_safety_target_ball": (
                certificate.frequency_amplitude_operational_safety_target_ball_validated
            ),
            "same_baseline_staged_protocol": (
                certificate.same_model_staged_protocol_validated
            ),
            "controlled_operational_first_hit_safety": True,
            "pulse_side_positive_face_deadband_chart": True,
            "quiet_side_negative_face_deadband_chart": True,
            "bounded_additive_finite_time_preparation": (
                certificate.bounded_additive_finite_time_preparation_validated
            ),
            "biological_basin_capture": (
                certificate.biological_basin_capture_validated
            ),
            "physical_finite_pulse": (
                certificate.physical_finite_pulse_validated
            ),
            "periodic_attraction": certificate.periodic_attraction_validated,
            "unforced_onset": certificate.unforced_onset_validated,
            "maximal_canard_onset": certificate.maximal_canard_onset_validated,
            "noise_hardware_robustness": (
                certificate.noise_hardware_robustness_validated
            ),
            "general_topology": certificate.general_topology_validated,
            "issue_15_closed": certificate.issue_15_closed,
        },
    }
    validate_same_model_amplitude_safety_result_payload(payload)
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    arguments.output.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
