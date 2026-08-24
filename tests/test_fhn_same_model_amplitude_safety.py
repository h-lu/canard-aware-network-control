"""Regression and refusal tests for the amplitude--safety target ball."""

from __future__ import annotations

from copy import deepcopy
from decimal import Decimal
from hashlib import sha256
import json
from pathlib import Path

import pytest

from canard_control.fhn_same_model_amplitude_safety import (
    TRACKED_AMPLITUDE_SHA256,
    TRACKED_PARAMETER_BOX_SHA256,
    TRACKED_SEPARATOR_SHA256,
    TRACKED_THREE_OUTPUT_SHA256,
    _deadband_chart,
    decimal_amplitude_safety_composition,
    load_same_model_amplitude_safety,
    load_same_model_amplitude_safety_result,
    same_model_amplitude_safety_from_payloads,
    validate_same_model_amplitude_safety_result_payload,
)


REPOSITORY = Path(__file__).resolve().parents[1]
AMPLITUDE = (
    REPOSITORY
    / "experiments/results/fhn_unsquared_amplitude_transfer.json"
)
THREE_OUTPUT = (
    REPOSITORY / "experiments/results/fhn_same_model_three_output.json"
)
SEPARATOR = REPOSITORY / "experiments/results/fhn_same_model_separator.json"
PARAMETER_BOX = (
    REPOSITORY / "experiments/results/fhn_periodic_parameter_box.json"
)
RESULT = (
    REPOSITORY
    / "experiments/results/fhn_same_model_amplitude_safety.json"
)
EXPECTED_RESULT_SHA256 = (
    "b9d00edd48c4ae5e61291dfd08fa13d6bb6775acf7f2683b69d3d2838130da36"
)


def _read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _payloads() -> tuple[dict, dict, dict, dict]:
    return (
        _read(AMPLITUDE),
        _read(THREE_OUTPUT),
        _read(SEPARATOR),
        _read(PARAMETER_BOX),
    )


def _compose(
    amplitude: dict,
    three: dict,
    separator: dict,
    parameter: dict,
):
    return same_model_amplitude_safety_from_payloads(
        amplitude,
        three,
        separator,
        parameter,
        amplitude_result_sha256=TRACKED_AMPLITUDE_SHA256,
        three_output_result_sha256=TRACKED_THREE_OUTPUT_SHA256,
        separator_result_sha256=TRACKED_SEPARATOR_SHA256,
        parameter_box_result_sha256=TRACKED_PARAMETER_BOX_SHA256,
    )


def test_four_source_loader_proves_two_translated_amplitude_safety_balls() -> None:
    certificate = load_same_model_amplitude_safety(
        AMPLITUDE,
        THREE_OUTPUT,
        SEPARATOR,
        PARAMETER_BOX,
        repository=REPOSITORY,
    )
    assert certificate.amplitude_source_manifest_validated
    assert certificate.three_output_source_manifest_validated
    assert certificate.separator_source_manifest_validated
    assert certificate.shared_parameter_box_validated
    assert certificate.shared_squared_target_ball_validated
    assert certificate.three_dimensional_inverse_coordinate_validated
    assert certificate.exact_reset_translation_validated
    assert certificate.unique_input_for_each_certified_target_validated
    assert (
        certificate.frequency_amplitude_operational_safety_target_ball_validated
    )
    assert float(certificate.certified_output_ball_radius_lower) > 2.75e-15
    assert Decimal(
        certificate.norm_composition.transformed_three_norm_upper
    ) < Decimal(certificate.parent_squared_output_ball_radius_lower)
    assert float(certificate.norm_composition.squared_ball_slack_lower) > 0

    pulse = certificate.pulse_side_chart
    quiet = certificate.quiet_side_chart
    assert pulse.input_center == ("0.2", "0.25", "0.5")
    assert quiet.input_center == ("0.2", "0.25", "-0.5")
    assert float(pulse.reset_projection_lower) > 0
    assert float(pulse.reset_projection_upper) < 1
    assert float(quiet.reset_projection_lower) > -1
    assert float(quiet.reset_projection_upper) < 0
    assert pulse.detector_face == "+1"
    assert quiet.detector_face == "-1"
    assert not pulse.biological_outcome_claimed
    assert not quiet.biological_outcome_claimed


def test_directed_three_norm_composition_keeps_safety_component() -> None:
    amplitude, three, _, _ = _payloads()
    result = decimal_amplitude_safety_composition(
        amplitude["certificate"], three["certificate"]
    )
    assert result.frequency_component_unchanged
    assert result.safety_component_unchanged
    assert result.three_dimensional_euclidean_norm_transfer_validated
    assert float(result.inverse_coordinate_factor_upper) > 5.89
    assert Decimal(result.transformed_three_norm_upper) < Decimal(
        result.squared_output_radius_lower
    )
    assert float(result.target_amplitude_positive_margin_lower) > 2.94


def test_recentered_deadbands_do_not_cross_zero_or_detector_faces() -> None:
    pulse = _deadband_chart(
        "0.5",
        chart_id="pulse",
        detector_face="+1",
        input_radius_text="1e-12",
        precision_digits=140,
    )
    quiet = _deadband_chart(
        "-0.5",
        chart_id="quiet",
        detector_face="-1",
        input_radius_text="1e-12",
        precision_digits=140,
    )
    assert pulse.reset_projection_lower == "0.499999999999"
    assert pulse.reset_projection_upper == "0.500000000001"
    assert quiet.reset_projection_lower == "-0.500000000001"
    assert quiet.reset_projection_upper == "-0.499999999999"
    assert pulse.threshold_deadband_lower == "0.499999999999"
    assert quiet.threshold_deadband_lower == "0.499999999999"
    with pytest.raises(ValueError, match="crosses r=-1 or r=0"):
        _deadband_chart(
            "0",
            chart_id="forged",
            detector_face="-1",
            input_radius_text="1e-12",
            precision_digits=140,
        )


def test_composer_refuses_an_enlarged_amplitude_radius() -> None:
    amplitude, three, separator, parameter = _payloads()
    forged = deepcopy(amplitude)
    forged["certificate"]["unsquared_amplitude_target_radius_lower"] = "3e-15"
    with pytest.raises(ValueError, match="leaves the 3D target ball"):
        _compose(forged, three, separator, parameter)


def test_composer_refuses_a_different_squared_parent_radius() -> None:
    amplitude, three, separator, parameter = _payloads()
    forged = deepcopy(amplitude)
    forged["certificate"]["squared_range_target_radius_lower"] = "1e-15"
    with pytest.raises(ValueError, match="squared radii disagree"):
        _compose(forged, three, separator, parameter)


def test_composer_refuses_a_separator_without_operational_threshold() -> None:
    amplitude, three, separator, parameter = _payloads()
    forged = deepcopy(separator)
    forged["certificate"]["controlled_operational_onset_validated"] = False
    with pytest.raises(ValueError, match="must be true"):
        _compose(amplitude, three, forged, parameter)


def test_composer_refuses_a_parameter_box_without_d1() -> None:
    amplitude, three, separator, parameter = _payloads()
    forged = deepcopy(parameter)
    forged["validation"]["d1_validated"] = False
    with pytest.raises(ValueError, match="must be true"):
        _compose(amplitude, three, separator, forged)


def test_tracked_result_is_source_bound_and_scope_safe() -> None:
    raw = RESULT.read_bytes()
    assert sha256(raw).hexdigest() == EXPECTED_RESULT_SHA256
    payload = json.loads(raw)
    provenance = payload["provenance"]
    generator = REPOSITORY / provenance["generator"]
    assert sha256(generator.read_bytes()).hexdigest() == provenance[
        "generator_sha256"
    ]
    for relative, digest in provenance["proof_source_manifest"].items():
        assert sha256((REPOSITORY / relative).read_bytes()).hexdigest() == digest
    evidence = payload["source_evidence"]
    for path, name in (
        (AMPLITUDE, "amplitude_result_sha256"),
        (THREE_OUTPUT, "three_output_result_sha256"),
        (SEPARATOR, "separator_result_sha256"),
        (PARAMETER_BOX, "parameter_box_result_sha256"),
    ):
        assert evidence[name] == sha256(path.read_bytes()).hexdigest()
    validate_same_model_amplitude_safety_result_payload(payload)
    loaded = load_same_model_amplitude_safety_result(
        RESULT, expected_sha256=EXPECTED_RESULT_SHA256
    )
    assert loaded["scope"][
        "frequency_unsquared_amplitude_operational_safety_target_ball"
    ]
    for name in (
        "bounded_additive_finite_time_preparation",
        "biological_basin_capture",
        "physical_finite_pulse",
        "periodic_attraction",
        "unforced_onset",
        "maximal_canard_onset",
        "noise_hardware_robustness",
        "general_topology",
        "issue_15_closed",
    ):
        assert not loaded["scope"][name]


def test_result_validator_refuses_a_biological_scope_promotion() -> None:
    payload = _read(RESULT)
    forged = deepcopy(payload)
    forged["scope"]["biological_basin_capture"] = True
    with pytest.raises(ValueError, match="must be false"):
        validate_same_model_amplitude_safety_result_payload(forged)


def test_result_validator_refuses_a_forged_closed_ball_radius() -> None:
    payload = _read(RESULT)
    forged = deepcopy(payload)
    forged["certificate"]["certified_output_ball_radius_lower"] = "1e-3"
    with pytest.raises(ValueError, match="amplitude output radius is invalid"):
        validate_same_model_amplitude_safety_result_payload(forged)
