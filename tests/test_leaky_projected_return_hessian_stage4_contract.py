from __future__ import annotations

from copy import deepcopy
from decimal import Decimal
from hashlib import sha256
import json
from pathlib import Path

import pytest

from canard_control.leaky_projected_return_hessian_stage4_contract import (
    FALSE_FLAGS,
    HESSIAN_FIELD_NAMES,
    MatrixLyapunovPerronInputBudget,
    ProjectedReturnHessianBlockBudget,
    RESULT_RELATIVE_PATH,
    TRUE_FLAGS,
    evaluate_matrix_lyapunov_perron_majorant,
    validate_stage4_projected_return_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]
EXPECTED_RESULT_SHA256: str | None = (
    "670fb21874fa26d953ee7bc2dc70f415c47ccc259690567fb20e5e00ea64fe13"
)


def _payload() -> dict[str, object]:
    return json.loads(
        (REPOSITORY / RESULT_RELATIVE_PATH).read_text(encoding="utf-8")
    )


def _synthetic_budget() -> MatrixLyapunovPerronInputBudget:
    blocks = ProjectedReturnHessianBlockBudget(
        stable_output_ss_upper="1",
        stable_output_su_upper="1",
        stable_output_uu_upper="1",
        unstable_output_ss_upper="1",
        unstable_output_su_upper="1",
        unstable_output_uu_upper="1",
        evidence_status="synthetic unit-test budget",
    )
    return MatrixLyapunovPerronInputBudget(
        stable_power_rate_upper="0.9",
        unstable_backward_rate_upper="0.5",
        stable_power_constant_upper="1",
        unstable_backward_power_constant_upper="1",
        sequence_weight_beta="0.95",
        stable_seed_radius="0.0001",
        stable_graph_radius="0.001",
        unstable_graph_radius="0.0005",
        validated_return_map_split_ball_radius_lower="0.002",
        hessian_blocks=blocks,
        evidence_status="synthetic unit-test budget",
    )


def test_registered_stage4_result_is_source_bound() -> None:
    assert EXPECTED_RESULT_SHA256 is not None
    payload = _payload()
    validate_stage4_projected_return_result(payload, REPOSITORY)
    assert sha256(
        (REPOSITORY / RESULT_RELATIVE_PATH).read_bytes()
    ).hexdigest() == EXPECTED_RESULT_SHA256


def test_actual_adapter_lists_every_open_numeric_gate() -> None:
    contract = _payload()["contract"]
    evaluation = contract["matrix_evaluation"]
    expected = {
        "stable_power_constant_upper",
        "validated_return_map_split_ball_radius_lower",
        *(f"hessian_blocks.{name}" for name in HESSIAN_FIELD_NAMES),
    }
    assert not evaluation["input_complete"]
    assert set(evaluation["missing_inputs"]) == expected
    assert not evaluation["graph_certificate_closes"]
    assert all(
        contract["hessian_block_budget"][name] is None
        for name in HESSIAN_FIELD_NAMES
    )


def test_synthetic_complete_matrix_budget_closes_all_three_gates() -> None:
    result = evaluate_matrix_lyapunov_perron_majorant(_synthetic_budget())
    assert result.input_complete
    assert result.input_order_conditions_hold
    assert result.contraction_closes
    assert result.self_map_closes
    assert result.split_ball_contains_graph_box
    assert result.graph_certificate_closes
    assert Decimal(result.perron_root_upper or "1") < 1
    assert Decimal(result.weighted_row_sum_upper or "1") < 1
    assert Decimal(
        (result.self_map_slack_vector_lower or {})["stable"]
    ) > 0
    assert Decimal(
        (result.self_map_slack_vector_lower or {})["unstable"]
    ) > 0
    assert Decimal(result.graph_height_upper or "1") < Decimal("0.00001")
    assert Decimal(result.graph_derivative_upper or "1") < Decimal("0.01")


def test_six_blocks_and_physical_return_orientation_are_explicit() -> None:
    contract = _payload()["contract"]
    interface = contract["projected_propagator_certificate_interface"]
    assert interface["required_projected_outputs"].count("D2P(") == 6
    assert interface["required_second_variations"] == "V_ss, V_su, V_uu"
    event = contract["return_event_contract"]
    assert "first positive physical return" in event["return_orientation"]
    assert "dot(U_h)(T)" in event["second_event_core"]
    variation = contract["variational_equation_contract"]
    assert "physical time" in variation["time_orientation"]
    assert variation["mixed_and_recovery_hessian_entries"] == "zero"


def test_direct_blocks_do_not_use_black_box_norm_equivalence() -> None:
    audit = _payload()["contract"]["adapted_norm_transfer_audit"]
    assert "p_s_old+p_u_old" in audit["black_box_hessian_transfer"]
    assert not audit["projection_isometry_alone_guarantees_improvement"]
    assert audit["direct_six_block_route_avoids_global_equivalence_factor"]


def test_radius_1p7e_minus_3_is_only_a_design_target() -> None:
    contract = _payload()["contract"]
    radius = contract["radius_design_target"]
    assert radius["split_total_radius"] == "0.0017"
    assert not radius["validated"]
    assert not radius["used_in_any_crossing_or_onset_claim"]
    claims = contract["claim_status"]
    assert all(claims[name] for name in TRUE_FLAGS)
    assert all(not claims[name] for name in FALSE_FLAGS)


@pytest.mark.parametrize(
    ("path", "value"),
    (
        (
            ("contract", "hessian_block_budget", "stable_output_ss_upper"),
            "1",
        ),
        (
            ("contract", "matrix_input_budget", "stable_power_constant_upper"),
            "1",
        ),
        (
            ("contract", "matrix_evaluation", "graph_certificate_closes"),
            True,
        ),
        (("contract", "radius_design_target", "validated"), True),
        (
            (
                "contract",
                "claim_status",
                "inner_local_stable_graph_quantitatively_validated",
            ),
            True,
        ),
    ),
)
def test_hostile_numeric_or_theorem_promotions_are_rejected(
    path: tuple[str, ...], value: object
) -> None:
    payload = deepcopy(_payload())
    target = payload
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value
    with pytest.raises(ValueError):
        validate_stage4_projected_return_result(payload, REPOSITORY)


def test_four_block_shortcut_is_rejected() -> None:
    payload = deepcopy(_payload())
    payload["contract"]["projected_propagator_certificate_interface"][
        "required_projected_outputs"
    ] = "Pi_s D2P(ss), Pi_s D2P(su), Pi_u D2P(ss), Pi_u D2P(su)"
    with pytest.raises(ValueError):
        validate_stage4_projected_return_result(payload, REPOSITORY)
