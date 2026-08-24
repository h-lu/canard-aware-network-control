"""Regression and refusal tests for the unsquared-amplitude certificate."""

from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path

import pytest

from canard_control.directed_interval import DirectedInterval
from canard_control.fhn_unsquared_amplitude_transfer import (
    _public_inner_radius,
    orbit_from_binary64_candidate_payload,
)


REPOSITORY = Path(__file__).resolve().parents[1]
CANDIDATE = REPOSITORY / "experiments/results/fhn_periodic_box_candidate.json"
PARAMETER_BOX = (
    REPOSITORY / "experiments/results/fhn_periodic_parameter_box.json"
)
SQUARED_TARGET = (
    REPOSITORY / "experiments/results/fhn_response_target_ball.json"
)
RESULT = (
    REPOSITORY
    / "experiments/results/fhn_unsquared_amplitude_transfer.json"
)
EXPECTED_RESULT_SHA256 = (
    "28e74d2316f7e9324f03874c3294d27d83708c9dbb3f4eefaf04925f55bbba60"
)


def _payload() -> dict:
    return json.loads(CANDIDATE.read_text(encoding="utf-8"))


def test_candidate_loader_preserves_exact_binary64_polynomial_data() -> None:
    payload = _payload()
    orbit = orbit_from_binary64_candidate_payload(payload)
    assert len(orbit.state) == 129
    assert orbit.state.tolist() == payload["center_orbit"]["state"]
    assert orbit.period == payload["center_orbit"]["period"]
    assert payload["claim_status"]["validated_periodic_orbit"] is False


def test_candidate_loader_refuses_an_exact_orbit_promotion() -> None:
    payload = deepcopy(_payload())
    payload["claim_status"]["validated_periodic_orbit"] = True
    with pytest.raises(ValueError, match="must not claim a validated orbit"):
        orbit_from_binary64_candidate_payload(payload)


def test_candidate_loader_refuses_a_changed_phase_grid() -> None:
    payload = deepcopy(_payload())
    payload["center_orbit"]["phase_nodes"][1] += 1.0e-8
    with pytest.raises(ValueError, match="declared odd grid"):
        orbit_from_binary64_candidate_payload(payload)


def test_public_inner_radius_composes_inside_squared_target_ball() -> None:
    precision = 160
    amplitude_lower = (
        "2.94737622302543311589267704607213287465934506175704116"
    )
    amplitude_upper = (
        "2.94737869577245638555737941249143755810909328788192661"
    )
    squared_radius = (
        "1.62187273782174089504757331762715967009378618047942197e-14"
    )
    result = _public_inner_radius(
        amplitude_lower, amplitude_upper, squared_radius, precision
    )
    assert result == (
        "2.75138166016477172021072951467987182906462947064987861e-15"
    )
    lower = DirectedInterval.from_decimal(amplitude_lower, precision)
    upper = DirectedInterval.from_decimal(amplitude_upper, precision)
    rho = DirectedInterval.from_decimal(squared_radius, precision)
    radius = DirectedInterval.from_decimal(result, precision)
    assert radius.upper < lower.lower
    assert radius.upper <= rho.lower
    assert ((2 * upper + radius) * radius).upper <= rho.lower


def test_tracked_certificate_is_source_bound_and_scope_safe() -> None:
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
    assert evidence["candidate_result_sha256"] == sha256(
        CANDIDATE.read_bytes()
    ).hexdigest()
    assert evidence["parameter_box_result_sha256"] == sha256(
        PARAMETER_BOX.read_bytes()
    ).hexdigest()
    assert evidence["squared_target_ball_result_sha256"] == sha256(
        SQUARED_TARGET.read_bytes()
    ).hexdigest()
    assert evidence["parameter_validation_exact_replay"]
    assert evidence["squared_target_radius_exact_match"]

    certificate = payload["certificate"]
    assert certificate["candidate_binary64_is_exact_polynomial_data"]
    assert not certificate["candidate_binary64_is_exact_orbit"]
    assert certificate["exact_orbit_in_wiener_correction_ball"]
    assert certificate["unique_voltage_extrema_on_gain_box"]
    assert certificate["uniform_positive_amplitude_enclosure_validated"]
    assert certificate["frequency_amplitude_target_ball_validated"]
    assert float(certificate["amplitude_lower"]) > 2.947
    assert float(certificate["amplitude_upper"]) < 2.948
    assert float(certificate["unsquared_amplitude_target_radius_lower"]) > 0
    assert certificate["calibrated_safety_coordinate_transfer_conditional"]
    assert not certificate["calibrated_three_output_target_ball_validated"]
    assert not certificate["physical_pulse_onset_validated"]

    scope = payload["scope"]
    assert scope["uniform_unsquared_amplitude_enclosure"]
    assert scope["frequency_unsquared_amplitude_target_ball"]
    assert not scope["binary64_candidate_is_exact_orbit"]
    assert scope["calibrated_safety_coordinate_transfer"] == "conditional"
    assert not scope["calibrated_three_output_target_ball"]
    assert not scope["physical_pulse_onset"]
