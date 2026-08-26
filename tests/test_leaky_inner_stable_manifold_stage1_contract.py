from __future__ import annotations

from copy import deepcopy
from dataclasses import replace
from decimal import Decimal
from hashlib import sha256
import json
from pathlib import Path

import pytest

from canard_control.leaky_inner_stable_manifold_stage1_contract import (
    QUANTITATIVE_FALSE_FLAGS,
    RESULT_RELATIVE_PATH,
    StableGraphInputBudget,
    evaluate_lyapunov_perron_majorant,
    validate_stage1_stable_manifold_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]
EXPECTED_RESULT_SHA256 = (
    "3c400ec92f00d4c94313b6e0a5b514f60f21335f54cba41ad5ba8a4217e8f21b"
)


def _payload() -> dict[str, object]:
    return json.loads(
        (REPOSITORY / RESULT_RELATIVE_PATH).read_text(encoding="utf-8")
    )


def _budget(name: str) -> StableGraphInputBudget:
    payload = _payload()
    return StableGraphInputBudget(**payload["contract"][name])


def test_registered_stage1_contract_is_source_bound() -> None:
    payload = _payload()
    validate_stage1_stable_manifold_result(payload, REPOSITORY)
    assert sha256(
        (REPOSITORY / RESULT_RELATIVE_PATH).read_bytes()
    ).hexdigest() == EXPECTED_RESULT_SHA256


def test_qualitative_codimension_one_is_separate_from_quantitative_claims() -> None:
    contract = _payload()["contract"]
    audit = contract["qualitative_audit"]
    claims = contract["claim_status"]
    assert audit["theorem_hypothesis_rfde_c1_or_better_matched"]
    assert audit["hyperbolic_periodic_orbit_in_rfde_sense"]
    assert audit["full_history_local_stable_manifold_c1_proved"]
    assert audit["full_history_local_stable_manifold_codimension"] == 1
    assert audit["reduced_history_local_stable_manifold_c1_proved"]
    assert audit[
        "reduced_phase_section_local_stable_manifold_c1_codimension_one_proved"
    ]
    assert not audit["particular_pulse_voltage_section_speed_lower_validated"]
    assert not audit["qualitative_result_supplies_explicit_radius_or_graph_constant"]
    assert not audit["qualitative_result_proves_separator_or_onset"]
    assert all(not claims[name] for name in QUANTITATIVE_FALSE_FLAGS)


def test_actual_evidence_stays_incomplete_and_cannot_emit_q_or_radius() -> None:
    evaluation = _payload()["contract"]["actual_evidence_evaluation"]
    assert not evaluation["input_complete"]
    assert set(evaluation["missing_inputs"]) == {
        "stable_spectral_radius_upper",
        "stable_projection_norm_upper",
        "unstable_projection_norm_upper",
        "stable_dichotomy_constant_upper",
        "unstable_dichotomy_constant_upper",
        "sequence_weight_beta",
        "section_event_speed_lower",
        "poincare_return_c2_upper",
        "nonlinear_derivative_remainder_coefficient_upper",
        "validated_return_map_ball_radius_lower",
    }
    assert evaluation["candidate_contraction_upper"] is None
    assert evaluation["candidate_sequence_radius_upper"] is None
    assert not evaluation["graph_majorant_closes"]


def test_design_row_closes_the_scalar_majorant_but_is_not_evidence() -> None:
    contract = _payload()["contract"]
    budget = contract["design_budget_not_evidence"]
    evaluation = contract["design_budget_evaluation"]
    assert budget["evidence_status"] == "design_target_not_proved"
    assert evaluation["input_complete"]
    assert evaluation["graph_majorant_closes"]
    assert Decimal("84.60") < Decimal(
        evaluation["lyapunov_perron_kernel_upper"]
    ) < Decimal("84.61")
    assert Decimal("0.0005100") < Decimal(
        evaluation["candidate_sequence_radius_upper"]
    ) < Decimal("0.0005101")
    assert Decimal(evaluation["candidate_contraction_upper"]) < Decimal(
        "0.432"
    )
    assert Decimal(evaluation["strict_feasibility_discriminant_lower"]) > 0
    assert Decimal(evaluation["candidate_invariance_margin_lower"]) >= 0
    assert Decimal("14.77") < Decimal(
        evaluation["critical_nonlinear_remainder_upper_strict"]
    ) < Decimal("14.78")
    assert not contract["claim_status"]["design_budget_promoted_to_rfde_evidence"]


def test_scalar_gate_rejects_nonclosing_discriminant_and_small_map_ball() -> None:
    design = _budget("design_budget_not_evidence")
    excessive_remainder = replace(
        design,
        nonlinear_derivative_remainder_coefficient_upper="20",
    )
    failed_discriminant = evaluate_lyapunov_perron_majorant(
        excessive_remainder
    )
    assert Decimal(
        failed_discriminant.strict_feasibility_discriminant_lower
    ) < 0
    assert failed_discriminant.candidate_sequence_radius_upper is None
    assert not failed_discriminant.graph_majorant_closes

    undersized_ball = replace(
        design,
        validated_return_map_ball_radius_lower="0.0005",
    )
    failed_ball = evaluate_lyapunov_perron_majorant(undersized_ball)
    assert failed_ball.candidate_contraction_upper is not None
    assert not failed_ball.candidate_within_validated_return_ball
    assert not failed_ball.graph_majorant_closes


@pytest.mark.parametrize(
    ("changes", "message"),
    [
        (
            {
                "stable_spectral_radius_upper": "0.95",
                "sequence_weight_beta": "0.95",
            },
            "violates rate",
        ),
        ({"stable_projection_norm_upper": "0.5"}, "violates rate"),
        (
            {"nonlinear_derivative_remainder_coefficient_upper": "9"},
            "violates rate",
        ),
    ],
)
def test_hostile_complete_budgets_reject_invalid_norm_rate_or_c2_order(
    changes: dict[str, str], message: str
) -> None:
    design = _budget("design_budget_not_evidence")
    with pytest.raises(ValueError, match=message):
        evaluate_lyapunov_perron_majorant(replace(design, **changes))


def test_hostile_partial_budget_rejects_malformed_nonnull_number() -> None:
    actual = _budget("actual_evidence_budget")
    with pytest.raises(ValueError, match="not a decimal"):
        evaluate_lyapunov_perron_majorant(
            replace(actual, unstable_backward_rate_upper="not-a-number")
        )


def test_hostile_result_rejects_qualitative_to_onset_promotion() -> None:
    payload = deepcopy(_payload())
    payload["contract"]["claim_status"][
        "unique_physical_pulse_onset_validated"
    ] = True
    with pytest.raises(ValueError, match="differs from source replay"):
        validate_stage1_stable_manifold_result(payload, REPOSITORY)


def test_hostile_result_rejects_design_row_as_rfde_evidence() -> None:
    payload = deepcopy(_payload())
    payload["contract"]["design_budget_not_evidence"][
        "evidence_status"
    ] = "source_bound_complete_evidence"
    payload["contract"]["claim_status"][
        "design_budget_promoted_to_rfde_evidence"
    ] = True
    with pytest.raises(ValueError, match="differs from source replay"):
        validate_stage1_stable_manifold_result(payload, REPOSITORY)


def test_hostile_result_rejects_parent_digest_mutation() -> None:
    payload = deepcopy(_payload())
    payload["manifest"]["parent_result_sha256"][
        next(iter(payload["manifest"]["parent_result_sha256"]))
    ] = "0" * 64
    with pytest.raises(ValueError, match="parent digest map changed"):
        validate_stage1_stable_manifold_result(payload, REPOSITORY)


def test_stage1_note_discloses_the_strict_claim_boundary() -> None:
    note = (
        REPOSITORY / "docs/leaky-inner-stable-manifold-stage1-contract.md"
    ).read_text(encoding="utf-8")
    assert "Qualitative theorem (proved)" in note
    assert "Quantitative graph and pulse onset (open)" in note
    assert "if and only if" in note
    assert "necessary condition for the" in note
    assert "binary64 observed crossing speed" in note
    assert "separator, onset, and routing remain outside Stage 1" in note
