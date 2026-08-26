from __future__ import annotations

from copy import deepcopy
from decimal import Decimal
from hashlib import sha256
import json
from pathlib import Path

import pytest

from canard_control.leaky_stable_output_uu_stage4b_contract import (
    BLOCK_NAMES,
    DESIGN_BLOCK_TARGETS,
    FALSE_FLAGS,
    NOTE_RELATIVE_PATH,
    REQUIRED_NUMERIC_FIELDS,
    REQUIRED_PROOF_FLAGS,
    RESULT_RELATIVE_PATH,
    STABLE_OUTPUT_UU_TARGET,
    Stage4BDirectedInputBudget,
    TRUE_FLAGS,
    evaluate_stage4b_directed_budget,
    validate_stage4b_contract_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]
EXPECTED_RESULT_SHA256: str | None = (
    "a310e4c1dba96961cc6fe7f70e4ee978f3b25a46956f9bcdde9f31286b40f7f7"
)


def _payload() -> dict[str, object]:
    return json.loads(
        (REPOSITORY / RESULT_RELATIVE_PATH).read_text(encoding="utf-8")
    )


def _synthetic_complete_budget() -> Stage4BDirectedInputBudget:
    return Stage4BDirectedInputBudget(
        stable_power_constant_upper="1",
        validated_split_return_ball_radius_lower="0.0017",
        return_tube_history_radius_upper="0.009",
        first_positive_return_time_lower="18",
        first_positive_return_time_upper="19",
        uniform_event_speed_lower="0.2",
        **DESIGN_BLOCK_TARGETS,
        continuous_history_atom_density_kernel_validated=True,
        validated_orbit_ball_propagated=True,
        split_return_tube_validated=True,
        first_positive_return_and_no_earlier_hit_validated=True,
        physical_time_event_hessian_validated=True,
        stable_adjoint_deflation_validated=True,
        uniform_ball_block_bounds_validated=True,
        evidence_status="synthetic complete directed budget",
    )


def test_registered_stage4b_result_is_source_bound() -> None:
    assert EXPECTED_RESULT_SHA256 is not None
    payload = _payload()
    validate_stage4b_contract_result(payload, REPOSITORY)
    assert sha256(
        (REPOSITORY / RESULT_RELATIVE_PATH).read_bytes()
    ).hexdigest() == EXPECTED_RESULT_SHA256


def test_actual_directed_ingress_is_completely_open() -> None:
    artifact = _payload()["artifact"]
    budget = artifact["actual_directed_input_budget"]
    assert all(budget[name] is None for name in REQUIRED_NUMERIC_FIELDS)
    assert all(not budget[name] for name in REQUIRED_PROOF_FLAGS)
    evaluation = artifact["actual_directed_evaluation"]
    assert not evaluation["input_complete"]
    assert set(evaluation["missing_inputs"]) == set(REQUIRED_NUMERIC_FIELDS) | set(
        REQUIRED_PROOF_FLAGS
    )
    assert not evaluation["strict_certificate_closes"]


def test_safe_target_row_closes_with_positive_margin() -> None:
    artifact = _payload()["artifact"]
    target = artifact["bottleneck_and_safe_target"]
    assert target["bottleneck_block"] == "stable_output_uu_upper"
    assert target["directed_design_target"] == STABLE_OUTPUT_UU_TARGET
    assert target["target_is_strictly_below_pilot_failure_ceiling"]
    assert not target["target_is_validated_bound"]
    evaluation = artifact["design_target_matrix_evaluation"]
    assert evaluation["graph_certificate_closes"]
    assert Decimal(evaluation["perron_root_upper"]) < Decimal("0.075")
    assert Decimal(
        evaluation["self_map_slack_vector_lower"]["stable"]
    ) > Decimal("0.00009")


def test_synthetic_complete_directed_budget_would_close() -> None:
    evaluation = evaluate_stage4b_directed_budget(_synthetic_complete_budget())
    assert evaluation.input_complete
    assert evaluation.numeric_order_conditions_hold
    assert evaluation.proof_flags_hold
    assert evaluation.return_tube_inside_validated_section_ball
    assert evaluation.stable_output_uu_target_met
    assert evaluation.matrix_majorant_evaluation is not None
    assert evaluation.matrix_majorant_evaluation["graph_certificate_closes"]
    assert evaluation.strict_certificate_closes


def test_continuous_history_and_correlated_deflation_are_mandatory() -> None:
    artifact = _payload()["artifact"]
    kernel = artifact["continuous_history_kernel_contract"]
    assert "atoms" in kernel["history_operator_representation"]
    assert "density kernels" in kernel["history_operator_representation"]
    assert not kernel["nodal_matrix_substitution_allowed"]
    deflation = artifact["stable_deflation_contract"]
    assert "correlated" in deflation["required_operation"]
    assert not deflation["left_adjoint_action_directed_upper_available"]
    assert not deflation["global_projection_norm_transfer_allowed"]


def test_physical_return_tube_and_uu_equations_are_explicit() -> None:
    artifact = _payload()["artifact"]
    event = artifact["return_tube_and_event_contract"]
    assert event["target_split_return_ball_radius"] == "0.0017"
    assert event["validated_section_ball_radius"] == "0.01"
    assert event["time_coordinate"] == "physical time only"
    assert "no earlier hit" in event["required_first_return_gate"]
    variation = artifact["unstable_uu_variational_contract"]
    assert "U_q" in variation["first_variation"]
    assert "V_qq" in variation["second_variation"]
    assert variation["recovery_forcing"] == "zero"


def test_claim_ledger_keeps_every_actual_theorem_false() -> None:
    claims = _payload()["artifact"]["claim_status"]
    assert all(claims[name] for name in TRUE_FLAGS)
    assert all(not claims[name] for name in FALSE_FLAGS)
    assert set(DESIGN_BLOCK_TARGETS) == set(BLOCK_NAMES)


def test_note_states_mesh_error_is_not_interval_error() -> None:
    text = (REPOSITORY / NOTE_RELATIVE_PATH).read_text(encoding="utf-8")
    assert "The heuristic difference is not an interval" in text
    assert "error and cannot be entered into a proof" in text
    assert "correlated expression before taking the" in text
    assert "A finite nodal matrix" in text


@pytest.mark.parametrize(
    ("path", "value"),
    (
        (
            (
                "artifact",
                "actual_directed_input_budget",
                "stable_output_uu_upper",
            ),
            "12",
        ),
        (
            (
                "artifact",
                "actual_directed_input_budget",
                "split_return_tube_validated",
            ),
            True,
        ),
        (
            (
                "artifact",
                "actual_directed_evaluation",
                "strict_certificate_closes",
            ),
            True,
        ),
        (
            (
                "artifact",
                "stable_deflation_contract",
                "left_adjoint_action_directed_upper_available",
            ),
            True,
        ),
        (
            (
                "artifact",
                "claim_status",
                "inner_local_stable_graph_quantitatively_validated",
            ),
            True,
        ),
    ),
)
def test_hostile_directed_promotions_are_rejected(
    path: tuple[str, ...], value: object
) -> None:
    payload = deepcopy(_payload())
    target = payload
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value
    with pytest.raises(ValueError):
        validate_stage4b_contract_result(payload, REPOSITORY)
