from __future__ import annotations

from copy import deepcopy
from dataclasses import replace
from decimal import Decimal, localcontext
from hashlib import sha256
import json
from pathlib import Path

import pytest

from canard_control.leaky_inner_stable_manifold_stage2_contract import (
    AffineReturnC2InputBudget,
    QUANTITATIVE_FALSE_FLAGS,
    RESULT_RELATIVE_PATH,
    evaluate_affine_return_c2_majorant,
    validate_stage2_stable_manifold_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]
EXPECTED_RESULT_SHA256 = (
    "eafa4d07b0558d9d4ce7423969379fa51875fcabce55af89a2378261fdb1e18d"
)


def _payload() -> dict[str, object]:
    return json.loads(
        (REPOSITORY / RESULT_RELATIVE_PATH).read_text(encoding="utf-8")
    )


def _synthetic_return_budget() -> AffineReturnC2InputBudget:
    return AffineReturnC2InputBudget(
        section_history_ball_radius_lower="0.01",
        flow_history_tube_radius_lower="0.02",
        return_time_lower="1",
        return_time_upper="2",
        phase_functional_norm_upper="1",
        uniform_event_speed_lower="0.5",
        section_defining_function_c2_upper="0",
        section_chart_projection_norm_upper="2",
        vector_field_norm_upper="3",
        vector_field_d1_upper="4",
        flow_d1_upper="5",
        flow_d2_upper="6",
        validated_return_map_ball_radius_lower="0.001",
        evidence_status="synthetic_test_not_evidence",
    )


def test_registered_stage2_contract_is_source_bound() -> None:
    assert EXPECTED_RESULT_SHA256 is not None
    payload = _payload()
    validate_stage2_stable_manifold_result(payload, REPOSITORY)
    assert sha256(
        (REPOSITORY / RESULT_RELATIVE_PATH).read_bytes()
    ).hexdigest() == EXPECTED_RESULT_SHA256


def test_baseline_gap_is_retained_as_the_honest_failure_row() -> None:
    ingress = _payload()["contract"]["baseline_gamma001_spectral_ingress"]
    spectrum = Decimal(ingress["stable_spectrum_modulus_upper"])
    working = Decimal(ingress["working_stable_power_rate_upper"])
    beta = Decimal(ingress["sequence_weight_beta"])
    assert ingress["certificate_role"] == (
        "baseline_gamma_0.001_honest_failure_row"
    )
    assert not ingress["used_for_stage1_partial_adapter"]
    assert Decimal("0.9990004") < spectrum < Decimal("0.9990006")
    assert spectrum < working < beta < 1
    assert ingress["stable_power_constant_exists_qualitatively_at_working_rate"]
    assert not ingress["stable_power_constant_numeric_upper_validated"]
    assert not ingress["spectral_radius_bound_used_as_boundary_power_bound"]
    assert ingress["unstable_dichotomy_constant_upper_intrinsic"] == "1"
    assert ingress["unstable_backward_power_bound_on_eigenline_validated"]
    assert Decimal(
        ingress["near_unit_optimistic_critical_c_n_sufficient_threshold"]
    ) < Decimal("1.1")
    assert not ingress[
        "near_unit_optimistic_old_c_n_scalar_gate_closes"
    ]
    assert Decimal(
        ingress["near_unit_optimistic_old_c_n_discriminant_upper"]
    ) < Decimal("-8.15")
    assert not ingress["fixed_working_optimistic_old_c_n_window_possible"]


def test_strengthened_gap_opens_only_an_optimistic_gap_only_window() -> None:
    ingress = _payload()["contract"]["strengthened_gamma01_spectral_ingress"]
    spectrum = Decimal(ingress["stable_spectrum_modulus_upper"])
    working = Decimal(ingress["working_stable_power_rate_upper"])
    beta = Decimal(ingress["sequence_weight_beta"])
    assert ingress["certificate_role"] == (
        "strengthened_gamma_0.01_partial_adapter_row"
    )
    assert ingress["used_for_stage1_partial_adapter"]
    assert Decimal("0.99004") < spectrum < Decimal("0.99006")
    assert spectrum < working < beta < 1
    assert Decimal(
        ingress["midpoint_optimistic_kernel_with_all_unknown_norms_set_to_one"]
    ) > Decimal("403")
    assert Decimal(
        ingress["midpoint_optimistic_critical_c_n_sufficient_threshold"]
    ) < Decimal("6.21")
    assert Decimal(
        ingress["near_unit_optimistic_kernel_with_all_unknown_norms_set_to_one"]
    ) < Decimal("231")
    assert Decimal(
        ingress["near_unit_stable_kernel_coefficient_upper"]
    ) < Decimal("229.72")
    assert Decimal(
        ingress["near_unit_unstable_kernel_coefficient_upper"]
    ) < Decimal("1.22")
    assert Decimal(
        ingress["near_unit_optimistic_critical_c_n_sufficient_threshold"]
    ) > Decimal("10.82")
    assert Decimal(
        ingress["near_unit_optimistic_old_c_n_discriminant_lower"]
    ) > Decimal("0.076")
    assert ingress["near_unit_optimistic_old_c_n_scalar_gate_closes"]
    assert Decimal(ingress["optimistic_stationary_beta_lower"]) > 1
    assert ingress[
        "optimistic_kernel_strictly_decreasing_on_admissible_beta_interval"
    ]
    assert Decimal(
        ingress["fixed_working_beta_to_one_critical_c_n_supremum_lower"]
    ) > Decimal("12.36")
    assert ingress["fixed_working_optimistic_old_c_n_window_possible"]
    assert ingress["general_scalar_feasibility_budget_rhs"] == "2500"


def test_stage2_ingress_still_cannot_emit_a_graph_q_or_radius() -> None:
    contract = _payload()["contract"]
    strengthened = contract["strengthened_gamma01_spectral_ingress"]
    budget = contract["stage1_budget_after_stage2_ingress"]
    evaluation = contract["stage1_majorant_after_stage2_ingress"]
    assert budget["stable_spectral_radius_upper"] is not None
    assert budget["unstable_dichotomy_constant_upper"] == "1"
    assert budget["sequence_weight_beta"] is not None
    assert budget["stable_spectral_radius_upper"] == strengthened[
        "working_stable_power_rate_upper"
    ]
    assert budget["sequence_weight_beta"] == strengthened["sequence_weight_beta"]
    assert set(evaluation["missing_inputs"]) == {
        "stable_projection_norm_upper",
        "unstable_projection_norm_upper",
        "stable_dichotomy_constant_upper",
        "poincare_return_c2_upper",
        "nonlinear_derivative_remainder_coefficient_upper",
        "validated_return_map_ball_radius_lower",
    }
    assert evaluation["candidate_contraction_upper"] is None
    assert evaluation["candidate_sequence_radius_upper"] is None
    assert not evaluation["graph_majorant_closes"]


def test_phase_audit_separates_bvp_and_one_history_sections() -> None:
    phase = _payload()["contract"]["abstract_phase_section_audit"]
    assert phase["periodic_bvp_phase_condition_quantitatively_transverse"]
    assert Decimal(phase["periodic_bvp_phase_pairing_abs_lower"]) > Decimal(
        "0.0089"
    )
    assert not phase["periodic_bvp_phase_functional_is_one_history_functional"]
    assert phase[
        "existential_history_coordinate_section_pointwise_transverse_proved"
    ]
    assert Decimal(
        phase["existential_history_coordinate_event_speed_at_orbit_lower"]
    ) > Decimal("0.059")
    assert phase["existential_history_coordinate_section_c2_upper"] == "0"
    assert not phase[
        "fourier_existence_argument_alone_registers_phase_and_component"
    ]
    assert phase["uniform_event_speed_lower_on_return_tube"] is None
    assert not phase["uniform_event_speed_on_return_tube_validated"]
    assert not phase["specific_pulse_voltage_section_speed_lower_validated"]


def test_route_c_registers_an_exact_phase_zero_voltage_section_point_speed() -> None:
    section = _payload()["contract"]["explicit_voltage_section_audit"]
    assert section["exact_phase_zero_section_formula"] == (
        "h_C(phi)=phi_v(0)-V_true(0)"
    )
    assert section["registered_pulse_section_description"] == (
        "v=v_inner(0), positive crossing"
    )
    assert section["normalized_phase"] == "0"
    assert section["state_component"] == "voltage"
    assert section["same_history_evaluation_functional_as_registered_pulse_section"]
    assert section["registered_pulse_section_level_binary64_hex"] == (
        "0x1.cf8fc825cafb6p-1"
    )
    assert section[
        "registered_pulse_section_level_inside_phase_zero_orbit_value_enclosure"
    ]
    assert not section[
        "exact_section_level_equals_registered_pulse_section_level_validated"
    ]
    candidate = Decimal(section["candidate_normalized_voltage_tangent_lower"])
    correction = Decimal(section["normalized_tangent_correction_upper"])
    validated = Decimal(section["validated_normalized_voltage_tangent_lower"])
    speed = Decimal(section["physical_voltage_event_speed_at_orbit_lower"])
    assert candidate > Decimal("4.491")
    assert Decimal("0") < correction < Decimal("0.000585")
    with localcontext() as context:
        context.prec = 100
        outward_gap = candidate - correction - validated
        assert Decimal(0) <= outward_gap < Decimal("1e-45")
    assert validated > Decimal("4.490")
    assert speed > Decimal("0.2469")
    assert section["section_functional_norm_upper"] == "1"
    assert section["section_chart_projection_norm_upper"] == "2"
    assert section["section_defining_function_c2_upper"] == "0"
    assert not section["unweighted_wiener_ball_directly_controls_derivative"]
    assert section["rfde_vector_field_identity_closes_tangent_correction"]
    assert not section[
        "additional_first_order_weighted_tail_bound_required_for_point_speed"
    ]
    assert section["pointwise_orbit_speed_validated"]
    assert Decimal(
        section["old_binary64_voltage_level_error_from_true_phase_zero_upper"]
    ) < Decimal("0.000010000000002")
    assert Decimal(section["physical_orbit_history_speed_upper"]) < Decimal(
        "0.4064"
    )
    assert Decimal(
        section["old_binary64_voltage_level_crossing_time_offset_upper"]
    ) < Decimal("0.000097")
    assert Decimal(
        section["old_binary64_voltage_level_crossing_phase_offset_upper"]
    ) < Decimal("0.0000054")
    assert Decimal(
        section["orbit_history_displacement_over_local_crossing_bracket_upper"]
    ) < Decimal("0.00004")
    assert section["local_crossing_bracket_within_declared_section_ball"]
    assert Decimal(
        section["old_binary64_voltage_level_local_orbit_crossing_speed_lower"]
    ) > Decimal("0.2067")
    assert section[
        "old_binary64_voltage_level_has_unique_local_true_orbit_crossing_validated"
    ]
    assert section["pulse_reshoot_required_before_route_c_target_can_be_used"]
    assert Decimal(section["declared_section_ball_radius"]) >= Decimal(
        "0.009999999999999999999999999999999999"
    )
    assert Decimal(
        section["vector_field_lipschitz_upper_on_declared_section_ball"]
    ) < Decimal("4.018")
    assert Decimal(
        section["event_speed_variation_upper_on_declared_section_ball"]
    ) < Decimal("0.04018")
    assert Decimal(
        section["uniform_event_speed_lower_on_declared_section_ball"]
    ) > Decimal("0.2067")
    assert section["uniform_event_speed_on_declared_section_ball_validated"]
    assert "a_tube>=a_orbit" in section["tube_uniform_speed_reduction_formula"]
    assert section["uniform_event_speed_lower_on_return_tube"] is None
    assert not section["uniform_event_speed_on_return_tube_validated"]

    claims = _payload()["contract"]["claim_status"]
    assert claims["concrete_history_phase_and_component_registered"]
    assert claims[
        "exact_phase_zero_voltage_section_pointwise_orbit_speed_validated"
    ]
    assert claims[
        "exact_phase_zero_voltage_section_uniform_speed_on_declared_ball_validated"
    ]
    assert claims[
        "old_binary64_voltage_level_has_unique_local_true_orbit_crossing_validated"
    ]
    assert not claims["specific_pulse_voltage_section_transversality_validated"]


def test_projection_and_stable_dichotomy_norms_remain_null() -> None:
    ledger = _payload()["contract"]["riesz_projection_and_dichotomy_ledger"]
    assert ledger["stable_riesz_projection_norm_upper"] is None
    assert ledger["unstable_riesz_projection_norm_upper"] is None
    assert ledger["stable_dichotomy_constant_upper"] is None
    assert ledger["unstable_dichotomy_constant_upper_on_eigenline"] == "1"
    assert not ledger[
        "periodic_pencil_zero_free_cover_is_history_resolvent_bound"
    ]
    assert not ledger["local_unstable_grushin_border_is_history_riesz_covector"]


def test_actual_return_c2_budget_stays_incomplete() -> None:
    contract = _payload()["contract"]
    budget = contract["return_c2_actual_budget"]
    evaluation = contract["return_c2_actual_evaluation"]
    assert Decimal(budget["section_history_ball_radius_lower"]) > Decimal(
        "0.0099"
    )
    assert Decimal(budget["uniform_event_speed_lower"]) > Decimal("0.2067")
    assert budget["flow_history_tube_radius_lower"] is None
    assert set(evaluation["missing_inputs"]) == {
        "flow_history_tube_radius_lower",
        "return_time_lower",
        "return_time_upper",
        "vector_field_norm_upper",
        "vector_field_d1_upper",
        "flow_d1_upper",
        "flow_d2_upper",
        "validated_return_map_ball_radius_lower",
    }
    assert evaluation["return_time_d1_upper"] is None
    assert evaluation["return_time_d2_upper"] is None
    assert evaluation["poincare_return_c2_upper"] is None
    assert evaluation["nonlinear_derivative_remainder_coefficient_upper"] is None
    assert not evaluation["return_c2_majorant_closes"]


def test_affine_return_c2_evaluator_replays_the_disclosed_formulas() -> None:
    evaluation = evaluate_affine_return_c2_majorant(_synthetic_return_budget())
    assert evaluation.input_complete
    assert evaluation.return_time_d1_upper == "10"
    assert evaluation.return_time_d2_upper == "3212"
    assert evaluation.poincare_return_c2_upper == "22484"
    assert evaluation.nonlinear_derivative_remainder_coefficient_upper == "22484"
    assert evaluation.return_ball_within_flow_tube
    assert evaluation.return_c2_majorant_closes


@pytest.mark.parametrize(
    "changes",
    [
        {"uniform_event_speed_lower": "0"},
        {"section_defining_function_c2_upper": "0.1"},
        {"section_chart_projection_norm_upper": "0.9"},
        {"return_time_lower": "2", "return_time_upper": "1"},
        {"validated_return_map_ball_radius_lower": "0.02"},
    ],
)
def test_hostile_return_c2_budgets_reject_invalid_order_or_scope(
    changes: dict[str, str],
) -> None:
    with pytest.raises(ValueError, match="violates time"):
        evaluate_affine_return_c2_majorant(
            replace(_synthetic_return_budget(), **changes)
        )


def test_hostile_partial_return_budget_rejects_malformed_nonnull_number() -> None:
    budget = AffineReturnC2InputBudget(
        section_history_ball_radius_lower="0.01",
        flow_history_tube_radius_lower=None,
        return_time_lower=None,
        return_time_upper=None,
        phase_functional_norm_upper="1",
        uniform_event_speed_lower=None,
        section_defining_function_c2_upper="0",
        section_chart_projection_norm_upper="2",
        vector_field_norm_upper=None,
        vector_field_d1_upper=None,
        flow_d1_upper=None,
        flow_d2_upper=None,
        validated_return_map_ball_radius_lower=None,
        evidence_status="synthetic_partial_test_not_evidence",
    )
    with pytest.raises(ValueError, match="not a decimal"):
        evaluate_affine_return_c2_majorant(
            replace(budget, flow_d1_upper="not-a-number")
        )


def test_every_open_quantitative_claim_stays_false() -> None:
    claims = _payload()["contract"]["claim_status"]
    assert all(not claims[name] for name in QUANTITATIVE_FALSE_FLAGS)


def test_hostile_result_rejects_projection_or_onset_promotion() -> None:
    for name in (
        "unstable_riesz_projection_norm_validated",
        "optimistic_unknown_norms_one_row_promoted_to_rfde_evidence",
        "specific_pulse_voltage_section_transversality_validated",
        "unique_physical_pulse_onset_validated",
    ):
        payload = deepcopy(_payload())
        payload["contract"]["claim_status"][name] = True
        with pytest.raises(ValueError, match="differs from source replay"):
            validate_stage2_stable_manifold_result(payload, REPOSITORY)


def test_hostile_result_rejects_pointwise_speed_as_uniform_tube_speed() -> None:
    payload = deepcopy(_payload())
    phase = payload["contract"]["abstract_phase_section_audit"]
    phase["uniform_event_speed_lower_on_return_tube"] = phase[
        "existential_history_coordinate_event_speed_at_orbit_lower"
    ]
    phase["uniform_event_speed_on_return_tube_validated"] = True
    with pytest.raises(ValueError, match="differs from source replay"):
        validate_stage2_stable_manifold_result(payload, REPOSITORY)


def test_hostile_result_rejects_route_c_point_speed_as_tube_speed() -> None:
    payload = deepcopy(_payload())
    section = payload["contract"]["explicit_voltage_section_audit"]
    section["uniform_event_speed_lower_on_return_tube"] = section[
        "physical_voltage_event_speed_at_orbit_lower"
    ]
    section["uniform_event_speed_on_return_tube_validated"] = True
    with pytest.raises(ValueError, match="differs from source replay"):
        validate_stage2_stable_manifold_result(payload, REPOSITORY)


def test_hostile_result_rejects_parent_hash_mutation() -> None:
    payload = deepcopy(_payload())
    relative = next(iter(payload["manifest"]["parent_result_sha256"]))
    payload["manifest"]["parent_result_sha256"][relative] = "0" * 64
    with pytest.raises(ValueError, match="manifest fixed data changed"):
        validate_stage2_stable_manifold_result(payload, REPOSITORY)


def test_stage2_note_discloses_every_nontransfer_seam() -> None:
    note = (
        REPOSITORY / "docs/leaky-inner-stable-manifold-stage2-contract.md"
    ).read_text(encoding="utf-8")
    assert "A spectral radius is not a power bound at its boundary" in note
    assert "not a functional on one RFDE history" in note
    assert "need not be periodic" in note
    assert "Their Neumann constants are not resolvent bounds" in note
    assert "periodic-BVP correction ball" in note
    assert "RFDE vector-field identity" in note
    assert "0.246926966042201268" in note
    assert "9.6733356288671430" in note
    assert r"pulse endpoint map \(K(J)\)" in note
    assert "10.825506993204714023" in note
    assert "strictly decreasing" in note
    assert "This is not RFDE evidence" in note
    assert "section ball" in note
    assert "full return-flow tube" in note
    assert r"emits no \(q\)" in note
