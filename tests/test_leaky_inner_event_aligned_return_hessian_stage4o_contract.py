from __future__ import annotations

import ast
from copy import deepcopy
from decimal import Decimal
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

import canard_control.leaky_inner_event_aligned_return_hessian_stage4o_contract as stage4o
from canard_control.leaky_inner_event_aligned_return_hessian_stage4o_contract import (
    FALSE_FLAGS,
    MANIFEST_KEYS,
    PARENT_RESULT_SHA256,
    RESULT_RELATIVE_PATH,
    TOP_KEYS,
    TRUE_FLAGS,
    _numeric_core,
    canonical_sha256,
    validate_stage4o_result,
)
from canard_control.leaky_projected_return_hessian_stage4_contract import (
    HESSIAN_FIELD_NAMES,
)


REPOSITORY = Path(__file__).resolve().parents[1]


def _payload() -> dict[str, object]:
    return json.loads(
        (REPOSITORY / RESULT_RELATIVE_PATH).read_text(encoding="utf-8")
    )


def _refresh_digests(payload: dict[str, object]) -> None:
    contract = payload["contract"]
    payload["manifest"]["contract_sha256"] = canonical_sha256(contract)
    payload["manifest"]["numeric_core_sha256"] = canonical_sha256(
        _numeric_core(contract)
    )


def test_registered_stage4o_result_validates_and_fresh_replays() -> None:
    validate_stage4o_result(_payload(), REPOSITORY, recompute=True)


def test_all_five_parent_results_are_bound_exactly() -> None:
    payload = _payload()
    assert payload["contract"]["parent_result_sha256"] == PARENT_RESULT_SHA256
    assert payload["manifest"]["parent_result_sha256"] == PARENT_RESULT_SHA256
    assert len(PARENT_RESULT_SHA256) == 5
    assert any("stage4i" in path for path in PARENT_RESULT_SHA256)
    assert any("stage4l" in path for path in PARENT_RESULT_SHA256)
    assert any("stage4m" in path for path in PARENT_RESULT_SHA256)
    assert sum("stage4n" in path for path in PARENT_RESULT_SHA256) == 2


def test_exact_model_and_all_three_field_jets_are_registered() -> None:
    model = _payload()["contract"]["exact_model_and_phase_space"]
    assert "w'=epsilon*(v-a-w)" in model["model_equation"]
    assert "epsilon/2" in model["D1_fast"]
    assert "sum_j c_j" in model["D2_fast"]
    assert model["D2_slow_and_all_mixed_entries"] == "zero"
    assert model["D2_coefficients"]["c_0"].startswith("-2*v0")
    assert model["D2_coefficients"]["c_j"].startswith("3*epsilon")
    assert model["D3_coefficients"]["mixed_and_slow"] == "zero"
    assert model["physical_time_only"] is True


def test_fixed_time_second_variation_has_zero_initial_second_jet() -> None:
    jet = _payload()["contract"]["fixed_time_flow_jet"]
    assert "D2F" in jet["second_variation"]
    assert "V_hk,0=0" in jet["second_variation"]
    assert jet["affine_initial_history_injection"] is True
    assert jet["initial_second_jet"] == "D2[x -> x][h,k]=0"
    assert "integral_0^r" in jet["mild_second_variation"]
    assert jet["required_input_sectors"] == ["ss", "su", "uu"]
    assert jet["numeric_enclosure_supplied_here"] is False


def test_event_time_jet_has_one_common_denominator_and_all_terms() -> None:
    event = _payload()["contract"]["implicit_event_time_jet"]
    assert event["first_derivative"] == "T_h=-n_h/a"
    assert "dot U_h^T*n_k" in event["preprojection_second_core"]
    assert "ddot X_T*n_h*n_k/a^2" in event["preprojection_second_core"]
    assert event["second_derivative"] == "T_hk=-ell_0(Z_hk)/a"
    assert event["largest_explicit_inverse_power_after_phase_projection"] == "a^-3"
    assert event["same_correlated_denominator_required"] is True
    assert event["numeric_denominator_supplied_here"] is False


def test_terminal_phase_projection_occurs_exactly_once() -> None:
    terminal = _payload()["contract"][
        "terminal_history_and_phase_projection"
    ]
    assert terminal["event_projection_application_count"] == 1
    assert terminal["first_return_derivative"] == "DP(x)h=Pi_x U_h^T"
    assert terminal["second_return_derivative"] == "D2P(x)[h,k]=Pi_x Z_hk"
    assert terminal["history_coordinate_range"] == "every theta in [-tau_max,0]"
    assert "theta=0/current T" in terminal["recovery_coordinate_rule"]
    assert terminal["section_tangency_checks"] == [
        "ell_0(DP(x)h)=0",
        "ell_0(D2P(x)[h,k])=0",
    ]
    assert terminal["endpoint_only_translation_sufficient"] is False


def test_event_phase_projection_and_fixed_deflation_are_distinguished() -> None:
    blocks = _payload()["contract"]["projected_six_block_definition"]
    assert blocks["moving_event_projection_is_not_stable_deflation"] is True
    assert blocks["fixed_stable_projection_over_base_ball"] is True
    assert "Pi_x" in blocks["event_aligned_bilinear_map"]
    assert blocks["fixed_stable_projection"] == "P_s=I-q_hat*f_hat"
    assert blocks["separately_normed_rank_one_terms_forbidden"] is True


def test_all_six_projected_blocks_are_present_and_open() -> None:
    blocks = _payload()["contract"]["projected_six_block_definition"]
    assert set(blocks["stable_outputs"]) == {
        "stable_output_ss",
        "stable_output_su",
        "stable_output_uu",
    }
    assert set(blocks["unstable_outputs"]) == {
        "unstable_output_ss",
        "unstable_output_su",
        "unstable_output_uu",
    }
    assert set(blocks["numeric_blocks_supplied_here"]) == set(
        HESSIAN_FIELD_NAMES
    )
    assert all(
        value is None for value in blocks["numeric_blocks_supplied_here"].values()
    )


def test_selected_hessian_does_not_require_no_earlier_cover() -> None:
    logic = _payload()["contract"]["selected_versus_first_return_logic"]
    assert logic["no_earlier_hit_needed_for_selected_hessian"] is False
    assert "A through H" in logic["selected_hessian_minimum"]
    assert "add I" in logic["first_physical_local_return_upgrade"]
    assert logic["negative_oriented_earlier_crossings_allowed"] is True
    assert logic["global_one_sign_event_gap_required"] is False
    assert logic["no_earlier_hit_validated_here"] is False


def test_one_period_arbitrary_C_history_C2_gate_is_fail_closed() -> None:
    audit = _payload()["contract"]["regularity_audit"]
    assert "arbitrary continuous stable histories" in audit[
        "declared_stage4m_domain"
    ]
    assert "ddot v_x" in audit["second_translation_term"]
    assert "T-tau_max>0" in audit["center_support_facts"]
    assert "T<2*tau_max" in audit["center_support_facts"]
    assert "T<tau0+tau1" in audit["center_support_facts"]
    assert "T-tau1-tau0<0" in audit["unresolved_early_history_mechanism"]
    assert audit["linear_no_identity_fact_does_not_supply_C2"] is True
    assert audit["naive_eventual_smoothing_on_one_return_is_sufficient"] is False
    assert audit["full_arbitrary_C_ball_C2_conclusion_permitted"] is False
    assert audit["repair_validated_here"] is False


def test_two_period_route_uses_exact_T_greater_than_2_tau_threshold() -> None:
    route = _payload()["contract"]["near_two_period_smoothing_route"]
    assert "T_2>2*tau_max" in route["exact_smoothing_threshold"]
    assert route["one_period_center_fails_threshold"] is True
    assert route["two_period_center_passes_threshold"] is True
    assert Decimal(route["center_one_period_2tau_max_minus_T_lower"]) > 4
    assert Decimal(route["center_two_period_T2_minus_2tau_max_lower"]) > 14
    assert "T2_minus>2*tau_max" in route["nonlinear_common_T2_gate"]
    assert route["nonlinear_two_period_branch_validated_here"] is False


def test_two_period_graph_transfer_requires_composition_and_recalibration() -> None:
    route = _payload()["contract"]["near_two_period_smoothing_route"]
    assert "Q=P o P" in route["composition_identity_gate"]
    assert "nested domains D0,D1" in route["composition_identity_gate"]
    assert "no invariant full saddle neighborhood" in route[
        "composition_identity_gate"
    ]
    assert "W^s(Q)=W^s(P)" in route["same_stable_set_reason"]
    assert "Q=P^2 is not necessary" in route["same_semiflow_transfer_alternative"]
    assert route[
        "direct_second_event_requires_same_semiflow_stable_set_identification"
    ] is True
    assert route["Q_equals_P2_needed_only_for_one_period_branch_identity"] is True
    assert route["one_step_stage4m_caps_reusable_without_recalibration"] is False
    assert "DQ=A^2" in route["required_recalibration"]
    assert route["no_earlier_hit_needed_for_Q_stable_graph"] is False
    assert route["no_earlier_hit_needed_for_physical_first_return_label"] is True


def test_direct_kernel_bypasses_scalars_but_not_intermediate_rows() -> None:
    audit = _payload()["contract"]["intermediate_stable_flow_audit"]
    assert audit["standalone_scalar_is_logically_necessary"] is False
    assert audit["conditional_scalar_K_ret_target_is_logically_necessary"] is False
    assert "first-variation rows" in audit["why_bypass_is_exact"]
    assert "intermediate-time first-variation row kernels" in audit[
        "what_cannot_be_avoided"
    ]
    assert audit["stage4l_terminal_row_can_replace_intermediate_rows"] is False
    assert audit["stage4i_center_words_alone_close_nonlinear_uniformity"] is False


def test_direct_kernel_keeps_event_and_output_correlations_before_norm() -> None:
    kernel = _payload()["contract"]["direct_correlated_kernel_route"]
    assert "tensor" in kernel["quadratic_source_kernel"]
    assert "before modulus" in kernel["second_variation_terminal_kernel"]
    assert "same signed atom-density-bimeasure" in kernel["event_terms"]
    assert "before total variation/operator norm" in kernel["output_terms"]
    assert "source time s" in kernel["complete_variables"]
    assert kernel["kernel_validated_here"] is False


def test_minimum_conditions_separate_selected_and_first_return_gates() -> None:
    conditions = _payload()["contract"]["minimum_sufficient_conditions"]
    assert set(conditions) == {
        "A_regular_domain",
        "B_nonlinear_base_cover",
        "C_selected_event_branch",
        "D_first_variation_kernels",
        "E_second_variation_kernels",
        "F_event_quotients",
        "G_terminal_and_output_cover",
        "H_six_cap_tests",
        "I_first_return_only",
        "finite_base_or_time_sampling_sufficient",
        "standalone_terminal_linear_row_sufficient",
    }
    assert "C2" in conditions["A_regular_domain"]
    assert "selected-event" in conditions["C_selected_event_branch"]
    assert "not required merely" in conditions["I_first_return_only"]
    assert conditions["finite_base_or_time_sampling_sufficient"] is False
    assert conditions["standalone_terminal_linear_row_sufficient"] is False


def test_next_task_is_two_period_correlated_and_explicitly_heuristic() -> None:
    task = _payload()["contract"]["next_numeric_task"]
    assert "near-two-period" in task["name"]
    assert "T2=2P" in task["domain"]
    assert "through 2P" in task["inputs"]
    assert "Pi_* once" in task["calculation"]
    assert "Q-specific strict caps" in task["outputs"]
    assert task["target_is_design_arithmetic_only"] is True
    assert task["unbound_finite_section_hint"]["evidence_status"].startswith(
        "HEURISTIC_FINITE_SECTION_ONLY"
    )
    assert task["pilot_result_exists"] is False


def test_theorem_note_states_exact_smoothing_threshold_without_broken_math() -> None:
    note = (
        REPOSITORY
        / "docs/leaky-inner-event-aligned-return-hessian-stage4o-contract.md"
    ).read_text(encoding="utf-8")
    assert "$T_2>2\\tau_{\\max}$" in note
    assert "$C^2$" in note
    assert "nested local domains" in note
    assert "Q=P^2$ on nested domains or the direct semiflow" in note
    assert "(C^2)" not in note
    assert "(\\theta=" not in note
    assert "(K_{\\rm ret}" not in note


def test_every_numeric_theorem_ingress_is_null_or_false() -> None:
    numeric = _payload()["contract"]["strict_numeric_ingress"]
    false_keys = {
        "all_delay_activation_and_history_seams_covered",
        "all_output_phase_cells_covered",
        "all_six_blocks_from_one_correlated_run",
        "all_six_strict_cap_tests_pass",
        "no_earlier_hit_cover_complete",
    }
    for key, value in numeric.items():
        if key == "directed_uniform_hessian_blocks":
            assert set(value) == set(HESSIAN_FIELD_NAMES)
            assert all(item is None for item in value.values())
        elif key in false_keys:
            assert value is False
        elif key == "evidence_status":
            assert value == "OPEN_FORMAL_ONLY"
        else:
            assert value is None


def test_claim_ledger_is_exact_and_fail_closed() -> None:
    claims = _payload()["contract"]["claim_status"]
    assert set(claims) == set(TRUE_FLAGS) | set(FALSE_FLAGS)
    assert all(claims[name] is True for name in TRUE_FLAGS)
    assert all(claims[name] is False for name in FALSE_FLAGS)


@pytest.mark.parametrize(
    ("path", "replacement"),
    (
        (("contract", "strict_numeric_ingress", "event_speed_lower_a_star"), "0.1"),
        (
            (
                "contract",
                "strict_numeric_ingress",
                "directed_uniform_hessian_blocks",
                "stable_output_ss",
            ),
            "0.1",
        ),
        (
            (
                "contract",
                "strict_numeric_ingress",
                "all_six_strict_cap_tests_pass",
            ),
            True,
        ),
        (
            (
                "contract",
                "claim_status",
                "moving_time_return_c2_on_full_arbitrary_C_ball_validated",
            ),
            True,
        ),
        (
            (
                "contract",
                "claim_status",
                "stable_output_ss_block_validated",
            ),
            True,
        ),
        (
            (
                "contract",
                "terminal_history_and_phase_projection",
                "event_projection_application_count",
            ),
            2,
        ),
        (
            (
                "contract",
                "selected_versus_first_return_logic",
                "no_earlier_hit_needed_for_selected_hessian",
            ),
            True,
        ),
        (
            (
                "contract",
                "near_two_period_smoothing_route",
                "one_step_stage4m_caps_reusable_without_recalibration",
            ),
            True,
        ),
    ),
)
def test_hostile_numeric_formula_and_claim_promotions_are_rejected(
    path: tuple[str, ...], replacement: object
) -> None:
    payload = deepcopy(_payload())
    target = payload
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = replacement
    _refresh_digests(payload)
    with pytest.raises(ValueError):
        validate_stage4o_result(payload, REPOSITORY)


def test_hostile_parent_hash_mutation_is_rejected() -> None:
    payload = deepcopy(_payload())
    parent = next(iter(PARENT_RESULT_SHA256))
    payload["contract"]["parent_result_sha256"][parent] = "0" * 64
    payload["manifest"]["parent_result_sha256"][parent] = "0" * 64
    _refresh_digests(payload)
    with pytest.raises(ValueError):
        validate_stage4o_result(payload, REPOSITORY)


def test_manifest_digests_and_outer_schema_are_exact() -> None:
    payload = _payload()
    assert set(payload) == TOP_KEYS
    assert set(payload["manifest"]) == MANIFEST_KEYS
    assert payload["manifest"]["contract_sha256"] == canonical_sha256(
        payload["contract"]
    )
    assert payload["manifest"]["numeric_core_sha256"] == canonical_sha256(
        _numeric_core(payload["contract"])
    )


def test_generator_validates_before_atomic_replace_and_fsyncs() -> None:
    source = (
        REPOSITORY
        / "experiments/"
        "leaky_inner_event_aligned_return_hessian_stage4o_contract.py"
    ).read_text(encoding="utf-8")
    ast.parse(source)
    assert source.index("validate_stage4o_result(") < source.index(
        "tempfile.mkstemp("
    )
    assert "os.replace" in source
    assert source.count("os.fsync") >= 2


def test_fresh_interpreter_validation() -> None:
    code = (
        "import json; from pathlib import Path; "
        "from canard_control.leaky_inner_event_aligned_return_hessian_stage4o_contract "
        "import RESULT_RELATIVE_PATH, validate_stage4o_result; "
        "r=Path.cwd(); p=json.loads((r/RESULT_RELATIVE_PATH).read_text()); "
        "validate_stage4o_result(p,r,recompute=True); print('STAGE4O_FRESH_OK')"
    )
    completed = subprocess.run(
        [sys.executable, "-c", code],
        cwd=REPOSITORY,
        check=True,
        capture_output=True,
        text=True,
        env={
            **os.environ,
            "PYTHONPATH": "src",
            "OPENBLAS_NUM_THREADS": "8",
            "OMP_NUM_THREADS": "1",
        },
    )
    assert completed.stdout.strip() == "STAGE4O_FRESH_OK"


def test_result_builder_is_deterministic() -> None:
    assert stage4o.build_stage4o_result(
        REPOSITORY
    ) == stage4o.build_stage4o_result(REPOSITORY)
