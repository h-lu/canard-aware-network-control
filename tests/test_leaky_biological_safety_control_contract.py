from __future__ import annotations

from copy import deepcopy
from fractions import Fraction
import json
from pathlib import Path

import pytest

from canard_control.leaky_biological_safety_control_contract import (
    RESULT_RELATIVE_PATH,
    ROUTE_C_EVENT_PARENT_CERTIFICATE_SHA256,
    ROUTE_C_EVENT_PARENT_RESULT_SHA256,
    adapted_product_target_radius_lower,
    build_biological_safety_control_contract,
    canonical_sha256,
    euclidean_target_radius_holds,
    pulse_interval_containment_holds,
    rectangular_target_radius_lower,
    robust_safety_side_holds,
    threshold_shift_upper,
    validate_biological_safety_control_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]


def _payload() -> dict[str, object]:
    return json.loads((REPOSITORY / RESULT_RELATIVE_PATH).read_text())


def test_contract_replays_from_all_four_parents() -> None:
    payload = _payload()
    validate_biological_safety_control_result(payload, REPOSITORY)
    assert payload["certificate"] == json.loads(
        json.dumps(
            build_biological_safety_control_contract(REPOSITORY).__dict__
        )
    )


def test_adapted_product_radius_is_exact() -> None:
    assert adapted_product_target_radius_lower(
        Fraction(1, 100), Fraction(1, 80)
    ) == Fraction(1, 100)


def test_rectangular_target_radius_is_exact() -> None:
    assert rectangular_target_radius_lower(
        Fraction(1, 100),
        Fraction(1, 10),
        Fraction(1, 5),
        2,
        3,
    ) == Fraction(1, 100)


def test_euclidean_shear_budget_is_exact_and_can_fail() -> None:
    assert euclidean_target_radius_holds(
        Fraction(1, 100),
        Fraction(1, 10),
        Fraction(1, 10),
        2,
        1,
    )
    assert not euclidean_target_radius_holds(
        Fraction(1, 25),
        Fraction(1, 10),
        Fraction(1, 10),
        2,
        1,
    )


def test_pulse_interval_containment_uses_threshold_shear() -> None:
    assert pulse_interval_containment_holds(
        Fraction(1, 2),
        Fraction(3, 100),
        2,
        1,
        Fraction(2, 5),
        Fraction(3, 5),
    )
    assert not pulse_interval_containment_holds(
        Fraction(1, 2),
        Fraction(1, 25),
        2,
        1,
        Fraction(2, 5),
        Fraction(3, 5),
    )


def test_threshold_shift_and_strict_safety_erosion() -> None:
    shift = threshold_shift_upper(Fraction(1, 100), Fraction(1, 2))
    assert shift == Fraction(1, 50)
    assert robust_safety_side_holds(
        Fraction(1, 10),
        Fraction(1, 100),
        shift,
        Fraction(1, 100),
    )
    assert not robust_safety_side_holds(
        Fraction(1, 25),
        Fraction(1, 100),
        shift,
        Fraction(1, 100),
    )


def test_model_specific_biological_fields_remain_false_and_null() -> None:
    certificate = _payload()["certificate"]
    assert certificate["outer_frequency_amplitude_parent_validated"]
    assert certificate["fixed_time_wide_pulse_parent_validated"]
    assert certificate["network_safety_erosion_formula_proved"]
    assert not certificate["stable_coordinate_endpoint_signs_validated"]
    assert not certificate["interval_newton_onset_validated"]
    assert not certificate["unique_physical_pulse_onset_validated"]
    assert not certificate["two_sided_biological_routing_validated"]
    assert not certificate[
        "outer_or_quiet_capture_from_both_sides_validated"
    ]
    assert not certificate["event_aligned_biological_threshold_validated"]
    assert not certificate[
        "frequency_amplitude_biological_safety_controllability_validated"
    ]
    assert certificate["validated_event_aligned_threshold_Jc"] is None
    assert certificate["validated_stable_coordinate_endpoint_signs"] is None
    assert certificate["validated_interval_newton_image"] is None
    assert certificate["validated_physical_pulse_onset"] is None
    assert certificate["validated_two_sided_biological_routing"] is None
    assert (
        certificate["validated_outer_or_quiet_capture_from_both_sides"]
        is None
    )
    assert certificate["certified_three_output_biological_radius"] is None
    assert certificate["certified_network_robust_safety_radius"] is None


def test_exactly_six_stage5c_event_side_fields_are_transcribed() -> None:
    certificate = _payload()["certificate"]
    event_fields = {
        key for key in certificate if key.startswith("validated_route_c_")
    }
    assert event_fields == {
        "validated_route_c_exact_section_level",
        "validated_route_c_parameter_interval_exact",
        "validated_route_c_unique_declared_bracket_event",
        "validated_route_c_positive_event_speed",
        "validated_route_c_order_four_event_time_graph_remainder_upper",
        "validated_route_c_common_event_Y_tube",
    }
    assert certificate["validated_route_c_exact_section_level"] == {
        "formula": "h_C(phi)=phi_v(0)-V_true(0)",
        "lower": (
            "0.905383843282120025506287674943450838327407828420353068999752401"
        ),
        "upper": (
            "0.905403843282120025506287674943450838327407845269557922000191891"
        ),
    }
    assert (
        certificate["validated_route_c_parameter_interval_exact"]
        == "[6021/20000,753/2500]"
    )
    event = certificate["validated_route_c_unique_declared_bracket_event"]
    assert event["left_time_exact"] == "555*sqrt(5)/24"
    assert event["right_time_exact"] == "1+546*sqrt(5)/24"
    assert "one and only one" in event["uniqueness_statement"]
    assert "third is not part" in event["ordinal_scope"]
    speed = certificate["validated_route_c_positive_event_speed"]
    assert Fraction(speed[0]) > 0
    assert Fraction(speed[1]) >= Fraction(speed[0])
    assert (
        certificate[
            "validated_route_c_order_four_event_time_graph_remainder_upper"
        ]
        == "1/10000"
    )
    history = certificate["validated_route_c_common_event_Y_tube"]
    assert history["phase_space"] == "Y=C([-5*sqrt(5),0],R)xR"
    assert Fraction(history["Y_max_radius_upper"]) < Fraction(1, 100)


def test_manifest_binds_stage5c_result_and_certificate_hashes() -> None:
    manifest = _payload()["manifest"]
    assert (
        manifest["route_c_event_parent_sha256"]
        == ROUTE_C_EVENT_PARENT_RESULT_SHA256
    )
    assert (
        manifest["route_c_event_parent_certificate_sha256"]
        == ROUTE_C_EVENT_PARENT_CERTIFICATE_SHA256
    )


def test_validator_rejects_biological_promotion() -> None:
    payload = deepcopy(_payload())
    payload["certificate"][
        "frequency_amplitude_biological_safety_controllability_validated"
    ] = True
    with pytest.raises(ValueError, match="certificate hash|differs from|promoted"):
        validate_biological_safety_control_result(payload, REPOSITORY)


def test_validator_rejects_inserted_target_radius() -> None:
    payload = deepcopy(_payload())
    payload["certificate"]["certified_three_output_biological_radius"] = "1/100"
    with pytest.raises(
        ValueError, match="certificate hash|differs from|unvalidated"
    ):
        validate_biological_safety_control_result(payload, REPOSITORY)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("stable_coordinate_endpoint_signs_validated", True),
        ("interval_newton_onset_validated", True),
        ("unique_physical_pulse_onset_validated", True),
        ("two_sided_biological_routing_validated", True),
        ("outer_or_quiet_capture_from_both_sides_validated", True),
    ],
)
def test_validator_rejects_stage5c_event_to_onset_promotion(
    field: str, value: bool
) -> None:
    payload = deepcopy(_payload())
    payload["certificate"][field] = value
    payload["manifest"]["certificate_sha256"] = canonical_sha256(
        payload["certificate"]
    )
    with pytest.raises(ValueError, match="promoted|differs from"):
        validate_biological_safety_control_result(payload, REPOSITORY)


def test_validator_rejects_old_fourier_candidate_section_level() -> None:
    payload = deepcopy(_payload())
    section = payload["certificate"]["validated_route_c_exact_section_level"]
    section["lower"] = (
        "0.905393843282120025506287674943450838327407828420743243"
    )
    section["upper"] = (
        "0.905393843282120025506287674943450838327407845269167748"
    )
    payload["manifest"]["certificate_sha256"] = canonical_sha256(
        payload["certificate"]
    )
    with pytest.raises(ValueError, match="differs from"):
        validate_biological_safety_control_result(payload, REPOSITORY)


def test_validator_rejects_parent_hash_mutation() -> None:
    payload = deepcopy(_payload())
    payload["manifest"]["pulse_jet_parent_sha256"] = "0" * 64
    with pytest.raises(ValueError, match="manifest hash"):
        validate_biological_safety_control_result(payload, REPOSITORY)


def test_validator_rejects_stage5c_parent_certificate_hash_mutation() -> None:
    payload = deepcopy(_payload())
    payload["manifest"]["route_c_event_parent_certificate_sha256"] = "0" * 64
    with pytest.raises(ValueError, match="certificate binding"):
        validate_biological_safety_control_result(payload, REPOSITORY)


def test_validator_rejects_source_bound_test_hash_mutation() -> None:
    payload = deepcopy(_payload())
    payload["manifest"]["test_sha256"] = "0" * 64
    with pytest.raises(ValueError, match="manifest hash"):
        validate_biological_safety_control_result(payload, REPOSITORY)


def test_note_preserves_biological_claim_boundary() -> None:
    note = (
        REPOSITORY / "docs/leaky-biological-safety-control-contract.md"
    ).read_text()
    assert "biological threshold" in note
    assert "Open and null" in note
    assert "do not define" in note
    assert "exactly six event-side outputs" in note
    assert "physical onset" in note
