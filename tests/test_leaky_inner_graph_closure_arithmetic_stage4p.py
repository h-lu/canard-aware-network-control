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

import canard_control.leaky_inner_graph_closure_arithmetic_stage4p as stage4p
from canard_control.leaky_inner_graph_closure_arithmetic_stage4p import (
    FALSE_FLAGS,
    ONE_RETURN_KRET_TARGET_LOWER,
    PARENT_RESULT_SHA256,
    RESULT_RELATIVE_PATH,
    TOP_KEYS,
    TRUE_FLAGS,
    TWO_RETURN_CONSERVATIVE_PILOT_ENVELOPE,
    TWO_RETURN_RECOMMENDED_WIDE_BOX,
    _numeric_core,
    canonical_sha256,
    validate_stage4p_result,
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
    design = payload["design"]
    payload["manifest"]["design_sha256"] = canonical_sha256(design)
    payload["manifest"]["numeric_core_sha256"] = canonical_sha256(
        _numeric_core(design)
    )


def test_registered_stage4p_result_validates_and_fresh_replays() -> None:
    validate_stage4p_result(_payload(), REPOSITORY, recompute=True)


def test_six_frozen_parent_hashes_are_bound() -> None:
    payload = _payload()
    assert len(PARENT_RESULT_SHA256) == 6
    assert payload["design"]["parent_result_sha256"] == PARENT_RESULT_SHA256
    assert payload["manifest"]["parent_result_sha256"] == PARENT_RESULT_SHA256
    for relative, digest in PARENT_RESULT_SHA256.items():
        assert stage4p._sha256_path(REPOSITORY / relative) == digest


def test_stage4l_power_and_stage5gb_seed_are_real_ingress_only() -> None:
    design = _payload()["design"]
    one = design["one_return_design"]
    assert Decimal(one["stable_rate_upper"]) < Decimal("0.01")
    assert one["stable_power_constant_upper"] == "1"
    parent = design["source_bound_parent_ingress"]
    assert parent["stage5gb_seed_containment_strict"] is True
    strict = design["strict_numeric_ingress"]["one_return"]
    assert Decimal(strict["stable_seed_cone_radius_upper"]) < Decimal("0.0094")
    assert strict["selected_return_map_parent"] is None


def test_preferred_b_geometry_is_exact_but_return_domain_open() -> None:
    geometry = _payload()["design"]["preferred_b_geometry"]
    assert Decimal(geometry["stable_graph_radius_R_s"]) == Decimal("0.0097")
    assert Decimal(geometry["unit_unstable_graph_radius_R_u_hat"]) == Decimal(
        "0.00025"
    )
    assert Decimal(geometry["split_graph_box_radius_sum"]) == Decimal("0.00995")
    assert geometry["return_domain_validated"] is False


def test_exact_region_rejects_a_fictitious_componentwise_widest_box() -> None:
    region = _payload()["design"]["exact_feasible_region"]
    assert region["unique_componentwise_widest_cap_vector_exists"] is False
    assert "Q_s,Q_u" in region["reason_no_unique_widest_vector"]
    assert "det(I-M)>0" == region["contraction_gates"].split(", ")[-1]


@pytest.mark.parametrize("design_key", ("one_return_design", "two_return_design"))
def test_axis_frontiers_are_exactly_six_and_nonmixable(design_key: str) -> None:
    records = _payload()["design"][design_key][
        "axis_frontiers_other_five_zero"
    ]
    assert [record["block"] for record in records] == list(HESSIAN_FIELD_NAMES)
    for record in records:
        assert record["axis_only_other_five_blocks_zero"] is True
        assert record["axis_frontier_is_simultaneously_mixable"] is False
        assert record["strict_lower_probe_metrics"][
            "raw_graph_arithmetic_closes"
        ] is True
        assert record["rejecting_upper_probe_metrics"][
            "raw_graph_arithmetic_closes"
        ] is False
        assert record["combined_lower_passes"] is True
        assert record["combined_upper_fails"] is True


def test_two_return_axis_caps_relax_the_unstable_graph_budget() -> None:
    design = _payload()["design"]
    one = {
        record["block"]: Decimal(record["graph_boundary_decimal_lower"])
        for record in design["one_return_design"]["axis_frontiers_other_five_zero"]
    }
    two = {
        record["block"]: Decimal(record["graph_boundary_decimal_lower"])
        for record in design["two_return_design"]["axis_frontiers_other_five_zero"]
    }
    for name in (
        "unstable_output_ss_upper",
        "unstable_output_su_upper",
        "unstable_output_uu_upper",
    ):
        assert two[name] > Decimal("2.7") * one[name]
    assert two["stable_output_ss_upper"] < one["stable_output_ss_upper"]


def test_one_return_joint_row_closes_with_optional_kret_reconstruction() -> None:
    row = _payload()["design"]["one_return_design"]["joint_reference_row"]
    assert row["raw_graph_arithmetic_closes"] is True
    assert row["triangle_reconstructed_return_tube_arithmetic_closes"] is True
    assert Decimal(row["pair_sum_reconstructed_kret_upper"]) < Decimal(
        ONE_RETURN_KRET_TARGET_LOWER
    )
    metrics = row["exact_majorant_metrics"]
    assert Decimal(metrics["perron_root_upper"]) < Decimal("0.068")
    assert Decimal(metrics["self_map_slack_vector_lower"]["stable"]) > 0
    assert Decimal(metrics["self_map_slack_vector_lower"]["unstable"]) > 0
    assert row["certified_hessian_blocks_supplied"] is False


def test_two_return_conservative_pilot_envelope_replays_but_is_not_proof() -> None:
    two = _payload()["design"]["two_return_design"]
    pilot = two["independently_reported_finite_section_pilot"]
    assert pilot["truncation_N"] == 180
    assert pilot["source_bound_continuous_history_certificate"] is False
    row = two["conservative_pilot_envelope_replay"]
    assert row["blocks"] == TWO_RETURN_CONSERVATIVE_PILOT_ENVELOPE
    metrics = row["exact_majorant_metrics"]
    assert Decimal(metrics["perron_root_upper"]) < Decimal("0.024")
    assert Decimal(metrics["graph_height_upper"]) < Decimal("0.00001744")
    assert Decimal(metrics["graph_derivative_upper"]) < Decimal("0.003086")
    assert row["blocks_are_source_bound_continuous_history_bounds"] is False


def test_two_return_wide_box_is_recommended_and_closes_split_majorant() -> None:
    two = _payload()["design"]["two_return_design"]
    row = two["recommended_wide_proof_box"]
    assert row["blocks"] == TWO_RETURN_RECOMMENDED_WIDE_BOX
    metrics = row["exact_majorant_metrics"]
    assert Decimal(metrics["perron_root_upper"]) < Decimal("0.194")
    assert Decimal(metrics["self_map_slack_vector_lower"]["stable"]) > Decimal(
        "0.000196"
    )
    assert Decimal(metrics["self_map_slack_vector_lower"]["unstable"]) > Decimal(
        "0.000124"
    )
    assert Decimal(metrics["graph_derivative_upper"]) < Decimal("0.027")
    assert row["pair_sum_implies_conditional_kret_target"] is False
    assert row["stable_graph_validated"] is False
    audit = two["wide_box_stage5gb_conditional_derivative_audit"]
    assert audit["strictly_below_threshold"] is True
    assert audit["endpoint_stable_gap_signs_validated"] is False


def test_wide_box_conditional_crossing_uses_required_alpha_adapter() -> None:
    crossing = _payload()["design"]["two_return_design"][
        "wide_box_conditional_crossing_arithmetic"
    ]
    assert crossing["direct_unit_to_physical_comparison_forbidden"] is True
    assert "psi_phys=psi_hat/alpha" in crossing["normalization_adapter"]
    assert Decimal(crossing["unit_graph_height_upper"]) < Decimal("0.000126")
    assert Decimal(crossing["physical_graph_height_upper"]) < Decimal("0.001624")
    assert Decimal(crossing["physical_graph_height_upper"]) > Decimal("0.001")
    assert crossing["registered_common_height_target_met"] is False
    assert Decimal(crossing["adjusted_left_gap_margin_lower"]) > Decimal("0.01805")
    assert Decimal(crossing["adjusted_right_gap_margin_lower"]) > Decimal("0.01316")
    derivative = crossing["physical_gap_derivative_interval"]
    assert Decimal(derivative["lower"]) > Decimal("-261")
    assert Decimal(derivative["upper"]) < Decimal("-243")
    assert crossing["conditional_unique_selected_crossing_arithmetic_closes"] is True
    assert crossing["future_graph_supplied"] is False
    assert crossing["selected_crossing_validated"] is False
    assert crossing["physical_onset_validated"] is False


def test_two_return_centered_independent_frontiers_match_bottlenecks() -> None:
    records = _payload()["design"]["two_return_design"][
        "isolated_graph_frontiers_holding_conservative_pilot_envelope"
    ]
    values = {
        record["block"]: Decimal(record["graph_boundary_decimal_lower"])
        for record in records
    }
    assert Decimal("6.28") < values["stable_output_ss_upper"] < Decimal("6.30")
    assert Decimal("12.1") < values["unstable_output_ss_upper"] < Decimal("12.2")
    assert Decimal("222") < values["unstable_output_su_upper"] < Decimal("223")
    assert Decimal("9200") < values["unstable_output_uu_upper"] < Decimal("9220")
    assert all(
        record["frontiers_from_different_records_may_be_mixed"] is False
        for record in records
    )


def test_two_return_smoothing_is_center_positive_but_full_ball_open() -> None:
    smoothing = _payload()["design"]["two_return_design"]["smoothing_audit"]
    assert Decimal(smoothing["one_return_exact_orbit_margin_lower"]) < 0
    assert Decimal(smoothing["two_return_exact_orbit_margin_lower"]) > Decimal("14")
    assert smoothing["two_return_exact_orbit_center_passes"] is True
    assert smoothing["two_return_full_ball_event_window_passes"] is False
    assert smoothing["required_full_ball_condition"] == "T2_minus-tau_max>tau_max"


def test_two_return_hessian_is_not_obtained_by_squaring_one_return_caps() -> None:
    two = _payload()["design"]["two_return_design"]
    assert two["one_return_block_caps_may_be_squared_or_reused"] is False
    assert "D2P(Px)" in two["composition_hessian_formula"]
    assert two["conditional_linear_transfer"]["transfer_validated_here"] is False
    strict = _payload()["design"]["strict_numeric_ingress"]
    assert strict["one_return_blocks_may_fill_two_return_slots"] is False


def test_kret_is_sufficient_for_return_containment_not_graph_necessary() -> None:
    coupling = _payload()["design"]["kret_coupling"]
    assert coupling["kret_is_required_by_matrix_lyapunov_perron_arithmetic"] is False
    assert coupling["stage4n_target_alone_implies_any_stage4m_cap"] is False
    assert coupling[
        "two_return_wide_box_graph_arithmetic_closes_despite_pair_sum_failure"
    ] is True
    assert coupling["ambient_norm_may_replace_correlated_six_blocks"] is False
    assert Decimal(coupling["stage4m_common_13p2353_pair_sum_uu"]) > Decimal(
        ONE_RETURN_KRET_TARGET_LOWER
    )


def test_selected_map_can_precede_first_return_but_is_still_missing() -> None:
    distinction = _payload()["design"]["selected_versus_first_return"]
    assert distinction["abstract_graph_requires_first_positive_return"] is False
    assert distinction["abstract_graph_requires_no_earlier_hit"] is False
    assert distinction["first_return_identification_requires_no_earlier_hit"] is True
    assert distinction["current_selected_map_on_full_ball_validated"] is False


def test_strict_ingress_keeps_all_twelve_hessian_slots_null() -> None:
    ingress = _payload()["design"]["strict_numeric_ingress"]
    for key, block_key in (
        ("one_return", "directed_uniform_hessian_blocks"),
        ("two_return", "directed_uniform_D2P2_blocks"),
    ):
        blocks = ingress[key][block_key]
        assert set(blocks) == set(HESSIAN_FIELD_NAMES)
        assert all(blocks[name] is None for name in HESSIAN_FIELD_NAMES)
        assert ingress[key]["stable_graph"] is None


def test_go_no_go_boundary_is_explicit() -> None:
    decision = _payload()["design"]["acceptance_decision"]
    assert decision["one_return_arithmetic_design"] == "GO"
    assert decision["one_return_theorem_release"] == "NO_GO"
    assert decision["two_return_arithmetic_design"] == "GO_CONDITIONAL"
    assert decision["two_return_theorem_release"] == "NO_GO"
    assert decision["first_positive_return_can_be_deferred"] is True
    assert decision["scalar_kret_route_can_be_replaced_by_direct_return_domain_proof"] is True


def test_claim_ledger_is_fail_closed() -> None:
    claims = _payload()["design"]["claim_status"]
    assert set(claims) == set(TRUE_FLAGS) | set(FALSE_FLAGS)
    assert all(claims[name] is True for name in TRUE_FLAGS)
    assert all(claims[name] is False for name in FALSE_FLAGS)


@pytest.mark.parametrize(
    ("path", "replacement"),
    (
        (("design", "claim_status", "quantitative_inner_stable_graph_validated"), True),
        (
            (
                "design",
                "strict_numeric_ingress",
                "one_return",
                "directed_uniform_hessian_blocks",
                "stable_output_ss_upper",
            ),
            "1",
        ),
        (
            (
                "design",
                "strict_numeric_ingress",
                "two_return",
                "directed_uniform_D2P2_blocks",
                "unstable_output_uu_upper",
            ),
            "100",
        ),
        (
            (
                "design",
                "two_return_design",
                "recommended_wide_proof_box",
                "blocks_are_source_bound_continuous_history_bounds",
            ),
            True,
        ),
        (
            (
                "design",
                "two_return_design",
                "wide_box_conditional_crossing_arithmetic",
                "direct_unit_to_physical_comparison_forbidden",
            ),
            False,
        ),
        (
            (
                "design",
                "two_return_design",
                "wide_box_conditional_crossing_arithmetic",
                "normalization_adapter",
            ),
            "psi_phys=psi_hat",
        ),
        (
            (
                "design",
                "two_return_design",
                "one_return_block_caps_may_be_squared_or_reused",
            ),
            True,
        ),
        (
            (
                "design",
                "selected_versus_first_return",
                "current_selected_map_on_full_ball_validated",
            ),
            True,
        ),
    ),
)
def test_hostile_proof_promotions_are_rejected(
    path: tuple[str, ...], replacement: object
) -> None:
    payload = deepcopy(_payload())
    target = payload
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = replacement
    _refresh_digests(payload)
    with pytest.raises(ValueError):
        validate_stage4p_result(payload, REPOSITORY, recompute=True)


def test_hostile_axis_cap_change_is_rejected_after_digest_refresh() -> None:
    payload = deepcopy(_payload())
    payload["design"]["one_return_design"]["axis_frontiers_other_five_zero"][0][
        "graph_boundary_decimal_lower"
    ] = "99"
    _refresh_digests(payload)
    with pytest.raises(ValueError):
        validate_stage4p_result(payload, REPOSITORY, recompute=True)


def test_manifest_digests_and_outer_schema_are_exact() -> None:
    payload = _payload()
    assert set(payload) == TOP_KEYS
    assert payload["manifest"]["design_sha256"] == canonical_sha256(
        payload["design"]
    )
    assert payload["manifest"]["numeric_core_sha256"] == canonical_sha256(
        _numeric_core(payload["design"])
    )


def test_generator_validates_before_atomic_replace_and_fsyncs() -> None:
    source = (
        REPOSITORY / "experiments/leaky_inner_graph_closure_arithmetic_stage4p.py"
    ).read_text(encoding="utf-8")
    ast.parse(source)
    assert source.index("validate_stage4p_result(") < source.index("tempfile.mkstemp(")
    assert "os.replace" in source
    assert source.count("os.fsync") >= 2


def test_fresh_interpreter_validation() -> None:
    code = (
        "import json; from pathlib import Path; "
        "from canard_control.leaky_inner_graph_closure_arithmetic_stage4p "
        "import RESULT_RELATIVE_PATH, validate_stage4p_result; "
        "r=Path.cwd(); p=json.loads((r/RESULT_RELATIVE_PATH).read_text()); "
        "validate_stage4p_result(p,r,recompute=True); print('STAGE4P_FRESH_OK')"
    )
    completed = subprocess.run(
        [sys.executable, "-c", code],
        cwd=REPOSITORY,
        check=True,
        capture_output=True,
        text=True,
        timeout=240,
        env={
            **dict(os.environ),
            "PYTHONPATH": os.pathsep.join(
                part for part in ("src", os.environ.get("PYTHONPATH", "")) if part
            ),
            "OPENBLAS_NUM_THREADS": "8",
            "OMP_NUM_THREADS": "1",
        },
    )
    assert completed.stdout.strip() == "STAGE4P_FRESH_OK"


def test_result_builder_is_deterministic_in_one_process() -> None:
    first = stage4p.build_stage4p_result(REPOSITORY)
    second = stage4p.build_stage4p_result(REPOSITORY)
    assert first == second
