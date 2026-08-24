"""Regression and refusal tests for the directed FHN target ball."""

from __future__ import annotations

from copy import deepcopy
from decimal import Decimal, localcontext
from hashlib import sha256
import json
from pathlib import Path

import numpy as np
import pytest

from canard_control.fhn_response_target_ball import (
    TRACKED_PARAMETER_BOX_SHA256,
    directed_target_ball_from_payload,
    load_directed_target_ball,
)


RESULT = (
    Path(__file__).resolve().parents[1]
    / "experiments/results/fhn_periodic_parameter_box.json"
)
TARGET_RESULT = (
    Path(__file__).resolve().parents[1]
    / "experiments/results/fhn_response_target_ball.json"
)
EXPECTED_TARGET_RESULT_SHA256 = (
    "dc17c3f845c3e317570c71af3acff670fb6955e2920ad2cea256507c1353dc05"
)


def _payload() -> dict:
    return json.loads(RESULT.read_text(encoding="utf-8"))


def _semantic_validation(payload: dict):
    encoded = (json.dumps(payload, sort_keys=True) + "\n").encode()
    return directed_target_ball_from_payload(
        payload,
        source_result_sha256=sha256(encoded).hexdigest(),
    )


def test_tracked_derivative_box_gives_a_positive_directed_target_ball() -> None:
    result = load_directed_target_ball(RESULT)

    assert result.source_result_sha256 == TRACKED_PARAMETER_BOX_SHA256
    assert result.norm_id == "euclidean-input-output-fixed-midpoint-inverse"
    assert result.control_order == ("kappa_1", "kappa_3")
    assert result.output_order == ("F", "R_h")
    assert result.parameter_center == ("0.2", "0.25")
    assert result.source_d1_branch_validated
    assert result.source_d3_extrema_validated
    assert result.source_d4_derivative_box_validated
    assert result.source_record_consistent
    assert result.centered_input_ball_contained_in_gain_box
    assert result.fixed_inverse_contraction_validated
    assert result.base_frequency_squared_range_target_ball_validated

    s0 = float(result.recomputed_midpoint_singular_value_lower)
    radius = float(result.recomputed_derivative_frobenius_radius_upper)
    beta = float(result.recomputed_response_margin_lower)
    q = float(result.fixed_inverse_contraction_upper)
    input_radius = float(result.certified_input_ball_radius)
    output_radius = float(result.certified_output_ball_radius_lower)
    assert s0 > 0.038
    assert 0.021 < radius < 0.022
    assert beta > 0.0162
    assert np.isclose(beta, s0 - radius, rtol=2e-14, atol=1e-30)
    assert 0.57 < q < 0.58
    assert q < 1.0
    assert input_radius <= 1e-12
    assert output_radius > 1.62e-14
    assert output_radius <= beta * input_radius * (1.0 + 2e-15)

    # The new theorem is deliberately narrower than the still-open physical
    # control goal.  These fields prevent accidental claim promotion.
    assert result.calibrated_reset_transfer_conditional
    assert not result.calibrated_reset_target_ball_validated
    assert not result.second_sensitivity_validated
    assert not result.second_sensitivity_required_for_base_target_ball
    assert not result.physical_pulse_onset_validated
    assert not result.issue_15_closed


def test_public_decimal_constants_compose_conservatively() -> None:
    result = load_directed_target_ball(RESULT)
    with localcontext() as context:
        context.prec = 120
        s0 = Decimal(result.recomputed_midpoint_singular_value_lower)
        radius = Decimal(
            result.recomputed_derivative_frobenius_radius_upper
        )
        beta = Decimal(result.recomputed_response_margin_lower)
        contraction = Decimal(result.fixed_inverse_contraction_upper)
        contraction_margin = Decimal(
            result.fixed_inverse_contraction_margin_lower
        )
        input_radius = Decimal(result.certified_input_ball_radius)
        output_radius = Decimal(result.certified_output_ball_radius_lower)
        assert beta <= s0 - radius
        assert contraction >= radius / s0
        assert contraction_margin <= Decimal(1) - contraction
        assert output_radius <= beta * input_radius


def test_public_parameter_center_is_not_hard_coded() -> None:
    payload = _payload()
    result = directed_target_ball_from_payload(
        payload,
        source_result_sha256=TRACKED_PARAMETER_BOX_SHA256,
        parameter_center=("0.200000", "0.250000"),
    )
    assert result.parameter_center == ("0.200000", "0.250000")
    assert result.target_ball_center.startswith(
        "exact P(0.200000,0.250000)"
    )


def test_tracked_target_ball_artifact_is_source_bound_and_scope_safe() -> None:
    raw = TARGET_RESULT.read_bytes()
    assert sha256(raw).hexdigest() == EXPECTED_TARGET_RESULT_SHA256
    payload = json.loads(raw)
    repository = Path(__file__).resolve().parents[1]
    provenance = payload["provenance"]
    generator = repository / provenance["generator"]
    assert sha256(generator.read_bytes()).hexdigest() == provenance[
        "generator_sha256"
    ]
    for relative, digest in provenance["proof_source_manifest"].items():
        assert sha256((repository / relative).read_bytes()).hexdigest() == digest

    target = payload["target_ball"]
    assert target["base_frequency_squared_range_target_ball_validated"]
    assert float(target["fixed_inverse_contraction_upper"]) < 0.575
    assert float(target["fixed_inverse_contraction_margin_lower"]) > 0.425
    assert float(target["certified_output_ball_radius_lower"]) > 1.62e-14
    scope = payload["scope"]
    assert scope["base_frequency_squared_range_target_ball"]
    assert not scope[
        "base_squared_range_target_ball_requires_second_sensitivities"
    ]
    assert scope["synchronous_orbital_hyperbolicity"]
    assert scope["calibrated_reset_transfer"] == "conditional"
    for field in (
        "attraction",
        "full_network_transverse_stability",
        "calibrated_three_output_target_ball",
        "same_model_periodic_separator_bridge",
        "physical_pulse_onset",
        "issue_15_closed",
    ):
        assert not scope[field]


def test_tracked_loader_refuses_a_forged_hash(tmp_path: Path) -> None:
    forged = tmp_path / "forged.json"
    forged.write_bytes(RESULT.read_bytes() + b" ")
    with pytest.raises(ValueError, match="SHA-256 mismatch"):
        load_directed_target_ball(forged)


@pytest.mark.parametrize(
    ("section", "flag"),
    (
        ("validation", "d1_validated"),
        ("validation", "d3_validated"),
        ("validation", "d4_response_lower_bound_validated"),
        ("continuation", "parameter_box_bordered_inverse_validated"),
        ("extrema", "extrema_validated"),
        ("response", "response_box_validated"),
        ("scope", "d4_directed_response_lower_bound"),
    ),
)
def test_semantic_validator_refuses_missing_proof_flags(
    section: str, flag: str
) -> None:
    payload = deepcopy(_payload())
    if section == "validation" or section == "scope":
        payload[section][flag] = False
    else:
        payload["validation"][section][flag] = False
    with pytest.raises(ValueError, match="must be true"):
        _semantic_validation(payload)


def test_semantic_validator_refuses_understated_derivative_radius() -> None:
    payload = deepcopy(_payload())
    payload["validation"]["response"][
        "response_frobenius_radius_upper"
    ] = "0.001"
    with pytest.raises(ValueError, match="radius is understated"):
        _semantic_validation(payload)


def test_semantic_validator_refuses_overstated_midpoint_lower_bound() -> None:
    payload = deepcopy(_payload())
    payload["validation"]["response"][
        "midpoint_smallest_singular_value_lower"
    ] = "0.04"
    with pytest.raises(ValueError, match="lower bound is overstated"):
        _semantic_validation(payload)


def test_semantic_validator_refuses_overstated_response_margin() -> None:
    payload = deepcopy(_payload())
    payload["validation"]["response"][
        "smallest_singular_value_lower"
    ] = "0.02"
    with pytest.raises(ValueError, match="margin is overstated"):
        _semantic_validation(payload)


def test_semantic_validator_refuses_a_box_missing_the_centered_ball() -> None:
    payload = deepcopy(_payload())
    payload["validation"]["gain_box"]["kappa_1_lower"] = "0.2"
    with pytest.raises(ValueError, match="does not contain"):
        _semantic_validation(payload)


def test_semantic_validator_refuses_an_interval_missing_its_midpoint() -> None:
    payload = deepcopy(_payload())
    payload["validation"]["response"]["response_lower"][0][0] = "0.04"
    payload["validation"]["response"]["response_upper"][0][0] = "0.05"
    with pytest.raises(ValueError, match="does not contain"):
        _semantic_validation(payload)


def test_semantic_validator_refuses_a_noncontracting_derivative_box() -> None:
    payload = deepcopy(_payload())
    response = payload["validation"]["response"]
    for row in range(2):
        for column in range(2):
            center = float(response["midpoint_binary64"][row][column])
            response["response_lower"][row][column] = str(center - 1.0)
            response["response_upper"][row][column] = str(center + 1.0)
    response["response_frobenius_radius_upper"] = "3"
    response["smallest_singular_value_lower"] = "1e-30"
    with pytest.raises(ValueError, match="does not give a contraction"):
        _semantic_validation(payload)
