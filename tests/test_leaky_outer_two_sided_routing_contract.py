from __future__ import annotations

from copy import deepcopy
from decimal import Decimal
from hashlib import sha256
import json
from pathlib import Path

import pytest

from canard_control.leaky_outer_two_sided_routing_contract import (
    OuterAttachmentInputBudget,
    OuterAttractingTubeInputBudget,
    QuietAttachmentInputBudget,
    RESULT_RELATIVE_PATH,
    SignedInnerExitInputBudget,
    evaluate_outer_attachment,
    evaluate_outer_attracting_tube,
    evaluate_quiet_attachment,
    evaluate_signed_inner_exit,
    validate_outer_two_sided_routing_contract_body,
    validate_outer_two_sided_routing_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]
EXPECTED_RESULT_SHA256 = (
    "1f9920ab25eec017c6cf06d1cd6a0ce9a3c349ef20c400b86ca0e65d56ee8cab"
)


def _payload() -> dict[str, object]:
    return json.loads(
        (REPOSITORY / RESULT_RELATIVE_PATH).read_text(encoding="utf-8")
    )


def test_registered_outer_routing_contract_is_source_bound() -> None:
    payload = _payload()
    validate_outer_two_sided_routing_result(payload, REPOSITORY)
    assert sha256(
        (REPOSITORY / RESULT_RELATIVE_PATH).read_bytes()
    ).hexdigest() == EXPECTED_RESULT_SHA256


def test_outer_local_polynomial_remainder_is_a_proved_history_bound() -> None:
    evidence = _payload()["contract"]["outer_local_vector_field_evidence"]
    assert evidence["declared_tube_remains_inside_proved_voltage_strip"]
    assert evidence["quadratic_vector_field_remainder_validated"]
    assert evidence["vector_field_second_derivative_bound_validated"]
    assert Decimal(
        evidence["quadratic_vector_field_remainder_coefficient_upper"]
    ) < Decimal("3.51")
    assert Decimal(
        evidence["vector_field_second_derivative_norm_upper"]
    ) < Decimal("7.04")
    assert not evidence[
        "outer_return_map_c2_bound_inferred_from_field_bound_alone"
    ]


def test_actual_outer_tube_keeps_every_missing_norm_null() -> None:
    contract = _payload()["contract"]
    budget = contract["outer_attracting_tube_actual_budget"]
    evaluation = contract["outer_attracting_tube_actual_evaluation"]
    assert budget["neutral_multiplier_algebraically_simple_validated"]
    assert not budget["outer_zero_index_validated"]
    assert set(evaluation["missing_inputs"]) == {
        "stable_spectral_radius_upper",
        "stable_power_constant_upper",
        "stable_riesz_projection_norm_upper",
        "phase_chart_projection_norm_upper",
        "return_iterate_count",
        "m_return_nonlinear_derivative_coefficient_upper",
        "chosen_section_radius",
        "validated_return_map_domain_radius_lower",
        "interreturn_flow_lipschitz_upper",
    }
    assert evaluation["linear_m_return_norm_upper"] is None
    assert not evaluation["outer_attracting_tube_closes"]


def test_outer_m_return_evaluator_closes_a_strict_synthetic_budget() -> None:
    evaluation = evaluate_outer_attracting_tube(
        OuterAttractingTubeInputBudget(
            outer_zero_index_validated=True,
            neutral_multiplier_algebraically_simple_validated=True,
            reduced_phase_section_and_return_map_validated=True,
            stable_spectral_radius_upper="0.8",
            stable_power_constant_upper="2",
            stable_riesz_projection_norm_upper="3",
            phase_chart_projection_norm_upper="2",
            return_iterate_count=5,
            m_return_nonlinear_derivative_coefficient_upper="100",
            chosen_section_radius="0.001",
            validated_return_map_domain_radius_lower="0.002",
            interreturn_flow_lipschitz_upper="5",
            interreturn_flow_tube_validated=True,
            evidence_status="synthetic_test_not_evidence",
        )
    )
    assert evaluation.linear_m_return_norm_upper == "0.65536"
    assert evaluation.m_return_lipschitz_upper == "0.75536"
    assert evaluation.outer_attracting_tube_closes


@pytest.mark.parametrize(
    "changes,match",
    [
        ({"stable_spectral_radius_upper": "1"}, "below one"),
        ({"stable_power_constant_upper": "0.9"}, "at least one"),
        ({"return_iterate_count": 0}, "positive integer"),
    ],
)
def test_outer_tube_evaluator_rejects_malformed_spectral_budgets(
    changes: dict[str, object], match: str
) -> None:
    values: dict[str, object] = {
        "outer_zero_index_validated": True,
        "neutral_multiplier_algebraically_simple_validated": True,
        "reduced_phase_section_and_return_map_validated": True,
        "stable_spectral_radius_upper": "0.8",
        "stable_power_constant_upper": "2",
        "stable_riesz_projection_norm_upper": "3",
        "phase_chart_projection_norm_upper": "2",
        "return_iterate_count": 5,
        "m_return_nonlinear_derivative_coefficient_upper": "100",
        "chosen_section_radius": "0.001",
        "validated_return_map_domain_radius_lower": "0.002",
        "interreturn_flow_lipschitz_upper": "5",
        "interreturn_flow_tube_validated": True,
        "evidence_status": "synthetic_test_not_evidence",
    }
    values.update(changes)
    with pytest.raises(ValueError, match=match):
        evaluate_outer_attracting_tube(OuterAttractingTubeInputBudget(**values))


def test_signed_factor_evaluator_produces_the_correct_exit_slab() -> None:
    evaluation = evaluate_signed_inner_exit(
        SignedInnerExitInputBudget(
            quantitative_inner_stable_graph_validated=True,
            graph_straightened_return_map_cylinder_validated=True,
            unstable_multiplier_modulus_lower="1.8",
            unstable_multiplier_modulus_upper="2.2",
            signed_gap_factor_deviation_upper="0.1",
            stable_row_contraction_upper="0.5",
            stable_row_gap_coupling_upper="0.1",
            stable_coordinate_radius="0.1",
            signed_exit_gap="0.01",
            validated_coordinate_gap_radius_lower="0.03",
            evidence_status="synthetic_test_not_evidence",
        )
    )
    assert evaluation.signed_factor_lower == "1.7"
    assert evaluation.signed_factor_upper == "2.3"
    assert evaluation.stable_row_image_radius_upper == "0.051"
    assert evaluation.exit_slab_gap_upper == "0.023"
    assert evaluation.signed_exit_closes


def test_actual_signed_exit_uses_multiplier_interval_but_not_a_graph() -> None:
    evaluation = _payload()["contract"]["signed_inner_exit_actual_evaluation"]
    assert "quantitative_inner_stable_graph" in evaluation["missing_artifacts"]
    assert evaluation["signed_factor_lower"] is None
    assert not evaluation["signed_exit_closes"]


def test_proved_J030_anchor_closes_only_the_target_inequality() -> None:
    evaluation = _payload()["contract"]["quiet_J_030_anchor_evaluation"]
    assert evaluation["quiet_target_inequality_closes"]
    assert Decimal(evaluation["quiet_target_margin_lower"]) > Decimal("0.0116")
    assert not evaluation["quiet_exit_face_attachment_closes"]


def test_quiet_evaluator_closes_for_a_complete_synthetic_exit_face() -> None:
    evaluation = evaluate_quiet_attachment(
        QuietAttachmentInputBudget(
            initial_set_is_complete_signed_inner_exit_face=True,
            directed_method_of_steps_family_tube_validated=True,
            complete_retained_history_bernstein_bound_validated=True,
            retained_guide_lyapunov_upper="0.0064",
            retained_p_norm_error_upper="0.001",
            quiet_p_norm_threshold_lower="0.09",
            evidence_status="synthetic_test_not_evidence",
        )
    )
    assert evaluation.retained_total_p_norm_upper == "0.081"
    assert evaluation.quiet_target_margin_lower == "0.009"
    assert evaluation.quiet_exit_face_attachment_closes


def test_J032_target_is_source_bound_but_never_promoted_to_capture() -> None:
    target = _payload()["contract"]["pulse_J_032_outer_attachment_target"]
    maximum = float(target["maximum_observed_dense_reduced_sup_distance"]["decimal"])
    assert maximum < 1.0e-5
    assert len(target["rows"]) == 3
    assert not target["continuous_history_distance_validated"]
    assert not target["directed_method_of_steps_error_validated"]
    assert not target["outer_attracting_tube_entry_validated"]
    assert not target["outer_basin_capture_validated"]


def test_requested_outer_error_allocation_closes_only_arithmetically() -> None:
    contract = _payload()["contract"]
    evaluation = contract[
        "outer_attachment_requested_evaluation_not_evidence"
    ]
    assert evaluation["input_complete"]
    assert evaluation["raw_event_history_error_upper"] == "0.000033"
    assert evaluation["projected_section_error_upper"] == "0.000066"
    assert Decimal(evaluation["outer_section_entry_margin_lower"]) == Decimal(
        "0.000034"
    )
    assert evaluation["outer_section_entry_inequality_closes"]
    assert not evaluation["outer_exit_face_attachment_closes"]


def test_outer_attachment_evaluator_closes_only_with_all_history_artifacts() -> None:
    evaluation = evaluate_outer_attachment(
        OuterAttachmentInputBudget(
            initial_set_is_complete_signed_inner_exit_face=True,
            directed_method_of_steps_family_tube_validated=True,
            continuous_history_bernstein_distance_validated=True,
            outer_section_event_bracket_validated=True,
            outer_section_event_speed_lower="0.5",
            continuous_guide_to_candidate_orbit_upper="0.00001",
            method_of_steps_history_error_upper="0.000005",
            exact_outer_orbit_correction_upper="0.00001",
            event_time_error_upper="0.000001",
            history_speed_upper_on_event_tube="3",
            section_reference_and_phase_error_upper="0.000005",
            section_chart_projection_norm_upper="2",
            outer_section_ball_radius_lower="0.0001",
            outer_attracting_tube_validated=True,
            evidence_status="synthetic_test_not_evidence",
        )
    )
    assert evaluation.outer_section_entry_inequality_closes
    assert evaluation.outer_exit_face_attachment_closes


def test_hostile_claim_promotion_is_rejected_without_replaying_trajectory() -> None:
    contract = deepcopy(_payload()["contract"])
    contract["claim_status"]["unique_physical_pulse_onset_validated"] = True
    with pytest.raises(ValueError, match="open routing or onset claim"):
        validate_outer_two_sided_routing_contract_body(contract)


def test_note_forbids_sampled_or_planar_basin_inference() -> None:
    note = (REPOSITORY / "docs/leaky-outer-two-sided-routing-contract.md").read_text(
        encoding="utf-8"
    )
    assert "Neither a planar phase portrait" in note
    assert "4097-point maximum is not inserted" in note
    assert "no separator, $J_c$, onset" in note
    assert "complete exit slab" in note
