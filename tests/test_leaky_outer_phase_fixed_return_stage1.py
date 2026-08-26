from __future__ import annotations

from copy import deepcopy
from dataclasses import replace
from decimal import Decimal
import json
from pathlib import Path

import pytest

from canard_control.leaky_outer_phase_fixed_return_stage1 import (
    AmbientToSectionInputBudget,
    DirectedReturnInputBudget,
    FALSE_FLAGS,
    FINITE_SECTION_STEPS,
    RESULT_RELATIVE_PATH,
    SOURCE_MANIFEST,
    TRUE_FLAGS,
    canonical_sha256,
    evaluate_directed_return_budget,
    evaluate_ambient_to_section_budget,
    validate_outer_phase_fixed_return_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def payload():
    return json.loads((REPOSITORY / RESULT_RELATIVE_PATH).read_text())


def test_registered_result_replays(payload):
    validate_outer_phase_fixed_return_result(payload, REPOSITORY)


def test_four_level_pilot_has_large_diagnostic_margin(payload):
    rows = payload["certificate"]["finite_section_pilot"]
    assert [row["step_count"] for row in rows] == list(FINITE_SECTION_STEPS)
    for row in rows:
        assert float(row["phase_fixed_spectral_radius_binary64"]["decimal"]) < 0.023
        assert float(row["phase_fixed_one_return_inf_norm_binary64"]["decimal"]) < 0.128
        assert float(row["phase_fixed_two_return_inf_norm_binary64"]["decimal"]) < 0.0029
        assert float(
            row["fixed_time_section_input_inf_norm_binary64"]["decimal"]
        ) > 2.7
        assert float(
            row["rank_one_phase_correction_inf_norm_binary64"]["decimal"]
        ) > 2.7
        assert float(
            row["algebraic_phase_projection_tangent_residual_inf_binary64"][
                "decimal"
            ]
        ) < 1e-14


def test_claim_ledger_keeps_pilot_and_theorem_separate(payload):
    claims = payload["certificate"]["claim_status"]
    assert all(claims[name] is True for name in TRUE_FLAGS)
    assert all(claims[name] is False for name in FALSE_FLAGS)
    evaluation = payload["certificate"]["evaluation"]
    assert not evaluation["input_complete"]
    assert not evaluation["direct_outer_return_contraction_closes"]
    attachment = payload["certificate"]["ambient_to_section_evaluation"]
    assert not attachment["input_complete"]
    assert not attachment["pulse_to_section_entry_closes"]


def test_complete_synthetic_budget_closes_only_the_registered_inequality():
    budget = DirectedReturnInputBudget(
        phase_fixed_voltage_history_row_norm_upper="0.14",
        phase_fixed_recovery_row_norm_upper="0.12",
        return_derivative_lipschitz_upper="120",
        chosen_section_radius="0.0001",
        validated_section_tube_radius_lower="0.00011",
        directed_kernel_recurrence_validated=True,
        arbitrary_c0_input_covered_by_measure_representation=True,
        corrected_signed_measure_total_variation_validated=True,
        unique_first_positive_return_and_event_speed_validated=True,
        second_variational_return_kernel_validated=True,
        evidence_status="synthetic hostile-control budget",
    )
    evaluation = evaluate_directed_return_budget(budget)
    assert evaluation.input_complete
    assert Decimal(evaluation.phase_fixed_return_lipschitz_upper) == Decimal("0.152")
    assert evaluation.direct_outer_return_contraction_closes
    failed = evaluate_directed_return_budget(
        replace(budget, return_derivative_lipschitz_upper="9000")
    )
    assert not failed.single_strict_inequality_holds
    assert not failed.direct_outer_return_contraction_closes


def test_ambient_distance_requires_a_phase_chart_before_section_entry():
    budget = AmbientToSectionInputBudget(
        ambient_complete_history_distance_upper="0.00002",
        phase_chart_lipschitz_upper="3",
        validated_section_radius="0.0001",
        ambient_distance_to_exact_phase_zero_orbit_validated=True,
        nonlinear_phase_chart_validated_on_ambient_tube=True,
        evidence_status="synthetic hostile-control budget",
    )
    evaluation = evaluate_ambient_to_section_budget(budget)
    assert evaluation.projected_section_distance_upper == "0.00006"
    assert evaluation.pulse_to_section_entry_closes
    failed = evaluate_ambient_to_section_budget(
        replace(budget, nonlinear_phase_chart_validated_on_ambient_tube=False)
    )
    assert not failed.input_complete
    assert not failed.pulse_to_section_entry_closes


def _refresh(value):
    value["manifest"]["certificate_sha256"] = canonical_sha256(
        value["certificate"]
    )


@pytest.mark.parametrize(
    "mutation",
    [
        lambda value: value["certificate"]["claim_status"].update(
            {"phase_fixed_outer_return_derivative_contraction_validated": True}
        ),
        lambda value: value["certificate"]["evaluation"].update(
            {"direct_outer_return_contraction_closes": True}
        ),
        lambda value: value["certificate"]["finite_section_pilot"][0][
            "phase_fixed_one_return_inf_norm_binary64"
        ].update({"decimal": "0"}),
        lambda value: value["manifest"]["source_sha256"].update(
            {SOURCE_MANIFEST[0]: "0" * 64}
        ),
    ],
)
def test_hostile_mutations_are_rejected(payload, mutation):
    changed = deepcopy(payload)
    mutation(changed)
    _refresh(changed)
    with pytest.raises(ValueError):
        validate_outer_phase_fixed_return_result(changed, REPOSITORY)


def test_note_states_measure_route_and_open_status():
    text = (REPOSITORY / "docs/leaky-outer-phase-fixed-return-stage1.md").read_text()
    normalized = " ".join(text.split())
    assert "not an attraction theorem" in normalized
    assert "signed measure subtraction" in normalized
    assert "does not require a modulus of continuity" in normalized
    assert "pulse history on the exact phase section" in normalized
    assert "Q_{\\rm phase}d_X<r_{\\rm section}" in text
    assert "physical pulse onset all remain false" in normalized
