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

import canard_control.leaky_inner_signed_second_variation_stage4q_pilot as stage4q
from canard_control.leaky_inner_signed_second_variation_stage4q_pilot import (
    BLOCK_NAMES,
    DEFAULT_PERIOD_STEP_COUNTS,
    FORMATION_ORDER,
    PARENT_RESULT_SHA256,
    RESULT_RELATIVE_PATH,
    STATUS,
    THEOREM_FLAGS,
    _numeric_core,
    canonical_sha256,
    validate_stage4q_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]


def _payload() -> dict[str, object]:
    return json.loads(
        (REPOSITORY / RESULT_RELATIVE_PATH).read_text(encoding="utf-8")
    )


def _refresh(payload: dict[str, object]) -> None:
    pilot = payload["pilot"]
    payload["manifest"]["pilot_sha256"] = canonical_sha256(pilot)
    payload["manifest"]["numeric_core_sha256"] = canonical_sha256(
        _numeric_core(pilot)
    )


def test_registered_stage4q_result_validates() -> None:
    validate_stage4q_result(_payload(), REPOSITORY, recompute=False)


def test_status_and_all_theorem_flags_remain_false() -> None:
    pilot = _payload()["pilot"]
    assert pilot["status"] == STATUS == "DIAGNOSTIC_NONRIGOROUS_SOURCE_BOUND"
    claims = pilot["claim_status"]
    assert set(claims) == set(THEOREM_FLAGS)
    assert all(claims[name] is False for name in THEOREM_FLAGS)


def test_all_six_parent_results_are_exactly_bound() -> None:
    payload = _payload()
    assert payload["pilot"]["parent_result_sha256"] == PARENT_RESULT_SHA256
    assert payload["manifest"]["parent_result_sha256"] == PARENT_RESULT_SHA256
    assert len(PARENT_RESULT_SHA256) == 6
    assert any("stage4i" in path for path in PARENT_RESULT_SHA256)
    assert any("stage4l" in path for path in PARENT_RESULT_SHA256)
    assert any("stage4m" in path for path in PARENT_RESULT_SHA256)
    assert any("stage4n" in path for path in PARENT_RESULT_SHA256)
    assert any("stage4p" in path for path in PARENT_RESULT_SHA256)


def test_one_period_fails_and_two_period_passes_only_the_center_smoothing_gate() -> None:
    row = _payload()["pilot"]["selected_branch_and_smoothing"]
    assert Decimal(row["one_period_smoothing_margin_P_minus_2tau_max"]) < 0
    assert row["one_period_gate_passes"] is False
    assert Decimal(row["two_period_smoothing_margin_2P_minus_2tau_max"]) > 0
    assert row["two_period_center_gate_passes"] is True
    assert row["primary_branch_is_proved_selected_second_hit"] is False
    assert row["smoothing_gate_is_operator_error_bound"] is False


def test_mesh_ladder_contains_primary_two_period_and_formal_one_period_rows() -> None:
    rows = _payload()["pilot"]["mesh_rows"]
    assert [row["period_step_count"] for row in rows] == list(
        DEFAULT_PERIOD_STEP_COUNTS
    )
    for row in rows:
        one = row["one_period_formal_diagnostic"]
        two = row["two_period_primary_diagnostic"]
        assert one["full_history_c2_smoothing_gate"] is False
        assert one["eligible_for_full_history_c2_claim"] is False
        assert "FORMAL_FINITE_SECTION_ONLY" in one["evidence_status"]
        assert two["full_history_c2_smoothing_gate_at_center"] is True
        assert two["continuous_history_c2_bound"] is False
        assert two["event"]["return_periods"] == 2
        assert two["event"]["selected_event_exists_uniformly"] is False
        assert two["event"]["no_earlier_hit_validated"] is False


def test_fixed_grushin_pair_and_phase_are_not_silently_replaced_by_eigensplits() -> None:
    pilot = _payload()["pilot"]
    coordinate = pilot["fixed_grushin_coordinate"]
    assert coordinate["physical_phase_anchor"] == "q_w(0) is positive real"
    assert coordinate["same_pair_used_for_every_mesh_and_both_return_horizons"] is True
    assert coordinate["q_norm_candidate_is_not_certified"] is True
    for row in pilot["mesh_rows"]:
        mesh = row["fixed_grushin_discretization"]
        assert abs(Decimal(mesh["pairing_after_discrete_correction"]) - 1) < Decimal(
            "1e-15"
        )
        assert mesh["pairing_identity_enforced_in_finite_section"] is True
        assert mesh["finite_section_adapter_validated"] is False
        assert mesh["boundary_interpolation"] == "one_sided_four_node"
        assert mesh["positive_time_nodes_used"] is False


def test_discarded_adapter_and_finite_eigensplit_cannot_replace_fixed_pair() -> None:
    for row in _payload()["pilot"]["mesh_rows"]:
        discarded = row["discarded_zero_nonsection_stencil_adapter_audit"]
        assert discarded["coordinate"]["boundary_interpolation"] == (
            "discarded_zero_nonsection_stencil"
        )
        assert discarded["used_for_primary_acceptance"] is False
        finite = row["self_consistent_finite_eigensplit_oracle"]
        assert finite["used_for_primary_acceptance"] is False
        assert finite["eigensplit_is_continuous_history_grushin_pair"] is False
        comparison = finite["coordinate_difference_from_fixed_stage4l_adapter"]
        assert comparison["finite_eigensplit_replaces_stage4l_coordinate"] is False
        assert set(
            finite["two_period_kernel_and_blocks"]["projected_hessian_blocks"]
        ) == set(BLOCK_NAMES)


def test_signed_formation_order_precedes_every_norm() -> None:
    order = _payload()["pilot"]["signed_formation_order"]
    assert order["order"] == list(FORMATION_ORDER)
    assert order["norm_before_all_signed_combinations"] is False
    assert order["finite_section_norm_only"] is True
    assert "T_hk" in order["moving_event_history_formula"]


def test_each_two_period_row_has_six_blocks_kret_and_cancellation_ratios() -> None:
    for row in _payload()["pilot"]["mesh_rows"]:
        kernel = row["two_period_primary_diagnostic"]["kernel_and_blocks"]
        assert set(kernel["projected_hessian_blocks"]) == set(BLOCK_NAMES)
        assert Decimal(kernel["signed_event_aligned_ambient_kret_candidate"]) > 0
        assert set(kernel["output_deflation_cancellation"]) == {"ss", "su", "uu"}
        assert kernel["all_linear_combinations_formed_before_norm"] is True
        assert kernel["finite_section_only"] is True


def test_direct_two_period_and_composition_oracles_are_both_recorded() -> None:
    for row in _payload()["pilot"]["mesh_rows"]:
        oracle = row["direct_two_period_vs_discrete_composition"]
        assert oracle["identity"] == "H2=H1[A1*.,A1*.]+A1*H1"
        assert Decimal(
            oracle["two_period_hessian_direct_vs_composed_linf_bilinear"]
        ) >= 0
        assert set(oracle["projected_block_relative_defects"]) == set(BLOCK_NAMES)
        assert oracle["oracle_is_directed_error_bound"] is False


def test_stage4p_caps_and_kret_targets_are_kept_separate() -> None:
    row = _payload()["pilot"]["refinement_and_acceptance"]
    assert set(row["stage4p_recommended_wide_simultaneous_box"]) == set(
        BLOCK_NAMES
    )
    assert set(row["stage4m_legacy_strict_caps"]) == set(BLOCK_NAMES)
    assert set(row["strict_six_block_diagnostic_tests"]) == set(BLOCK_NAMES)
    assert Decimal(
        row["kret_target_from_stage4p_two_return_conditional_lower"]
    ) > Decimal("178.6")
    assert Decimal(row["legacy_one_return_kret_target_from_stage4n"]) > Decimal(
        "188.9"
    )
    assert row["any_diagnostic_test_is_a_theorem"] is False
    assert row["ambient_kret_is_required_for_stage4p_graph_arithmetic"] is False
    assert set(row["coordinate_oracle_mesh_trends"]) == set(BLOCK_NAMES)
    for trend in row["coordinate_oracle_mesh_trends"].values():
        assert len(trend["fixed_stage4l_adapter_mesh_series"]) == 3
        assert len(trend["self_consistent_finite_eigensplit_mesh_series"]) == 3
        assert len(trend["discarded_zero_nonsection_adapter_mesh_series"]) == 3
        assert trend["finite_eigensplit_used_for_acceptance"] is False
    design = row["stage4p_two_return_design"]
    assert design["simultaneous_box_graph_arithmetic_closes_conditionally"] is True
    assert design["box_is_a_directed_hessian_bound"] is False
    assert design["box_entered_into_strict_numeric_ingress"] is False
    assert design["kret_is_required_by_matrix_lyapunov_perron_arithmetic"] is False


@pytest.mark.parametrize(
    ("path", "replacement"),
    (
        (("pilot", "claim_status", "six_projected_hessian_blocks_are_validated"), True),
        (("pilot", "claim_status", "one_period_map_is_c2_on_the_full_history_space"), True),
        (("pilot", "claim_status", "biological_capture_is_validated"), True),
        (("pilot", "selected_branch_and_smoothing", "one_period_gate_passes"), True),
        (("pilot", "mesh_rows", 0, "one_period_formal_diagnostic", "eligible_for_full_history_c2_claim"), True),
        (("pilot", "mesh_rows", 0, "two_period_primary_diagnostic", "continuous_history_c2_bound"), True),
        (("pilot", "signed_formation_order", "norm_before_all_signed_combinations"), True),
        (("pilot", "refinement_and_acceptance", "any_diagnostic_test_is_a_theorem"), True),
        (("pilot", "mesh_rows", 0, "self_consistent_finite_eigensplit_oracle", "used_for_primary_acceptance"), True),
        (("pilot", "mesh_rows", 0, "discarded_zero_nonsection_stencil_adapter_audit", "used_for_primary_acceptance"), True),
    ),
)
def test_hostile_promotions_are_rejected(
    path: tuple[object, ...], replacement: object
) -> None:
    payload = deepcopy(_payload())
    target = payload
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = replacement
    _refresh(payload)
    with pytest.raises(ValueError):
        validate_stage4q_result(payload, REPOSITORY, recompute=False)


def test_hostile_formation_reordering_is_rejected() -> None:
    payload = deepcopy(_payload())
    order = payload["pilot"]["signed_formation_order"]["order"]
    order[-1], order[-2] = order[-2], order[-1]
    _refresh(payload)
    with pytest.raises(ValueError, match="formation order"):
        validate_stage4q_result(payload, REPOSITORY, recompute=False)


def test_generator_checks_the_registered_result() -> None:
    environment = os.environ.copy()
    environment["OPENBLAS_NUM_THREADS"] = "8"
    environment["OMP_NUM_THREADS"] = "1"
    environment["PYTHONPATH"] = "build/testdeps:src"
    completed = subprocess.run(
        [
            "/usr/bin/python3",
            "experiments/leaky_inner_signed_second_variation_stage4q_pilot.py",
            "--check",
        ],
        cwd=REPOSITORY,
        env=environment,
        check=True,
        capture_output=True,
        text=True,
    )
    assert RESULT_RELATIVE_PATH in completed.stdout


def test_source_has_no_true_theorem_flag_builder() -> None:
    source = (REPOSITORY / stage4q.SOURCE_RELATIVE_PATH).read_text(
        encoding="utf-8"
    )
    tree = ast.parse(source)
    assert "claims = {name: False for name in THEOREM_FLAGS}" in source
    assert not any(
        isinstance(node, ast.Assign)
        and any(isinstance(target, ast.Name) and target.id == "claims" for target in node.targets)
        and isinstance(node.value, ast.Dict)
        and any(isinstance(value, ast.Constant) and value.value is True for value in node.value.values)
        for node in ast.walk(tree)
    )
