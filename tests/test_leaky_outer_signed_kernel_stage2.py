from __future__ import annotations

from copy import deepcopy
from dataclasses import replace
from decimal import Decimal
import json
from pathlib import Path

import pytest

from canard_control.leaky_outer_signed_kernel_stage2 import (
    FALSE_FLAGS,
    RESULT_RELATIVE_PATH,
    SOURCE_MANIFEST,
    TRUE_FLAGS,
    SignedKernelTransferBudget,
    canonical_sha256,
    evaluate_signed_kernel_transfer,
    validate_outer_signed_kernel_stage2_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def payload():
    return json.loads((REPOSITORY / RESULT_RELATIVE_PATH).read_text())


def test_registered_stage2_replays(payload):
    validate_outer_signed_kernel_stage2_result(payload, REPOSITORY)


def test_directed_cellwise_phase_cancellation_is_large(payload):
    certificate = payload["certificate"]
    corrected = Decimal(certificate["directed_phase_fixed_shadow_norm_upper"])
    fixed = Decimal(certificate["directed_fixed_time_shadow_norm_upper"])
    phase = Decimal(certificate["directed_rank_one_phase_shadow_norm_upper"])
    triangle = Decimal(certificate["separate_triangle_shadow_norm_upper"])
    factor = Decimal(certificate["directed_cancellation_factor_lower"])
    assert corrected < Decimal("0.128")
    assert fixed > Decimal("2.58")
    assert phase > Decimal("2.58")
    assert triangle > Decimal("5.16")
    assert factor > Decimal("40")
    assert Decimal(
        certificate["discrete_shadow_remaining_margin_below_one_lower"]
    ) > Decimal("0.872")


def test_atoms_density_scalar_and_padding_are_not_conflated(payload):
    certificate = payload["certificate"]
    decomposition = certificate["continuous_kernel_decomposition"]
    assert "Dirac_0" in decomposition["current_voltage_dirac_atom"]
    assert "K(t,theta)" in decomposition["history_density"]
    assert "R(t,0)e_w" in decomposition["initial_recovery_scalar_column"]
    assert certificate["interpolation_padding_cell_count"] == 4
    assert Decimal(certificate["directed_padding_mass_maximum_upper"]) < Decimal(
        "1.2e-8"
    )
    rows = certificate["directed_output_rows"]
    assert len(rows) > 150
    assert rows[-1]["output_kind"] == "returned_current_recovery"
    assert all(row["history_input_cell_count"] == 155 for row in rows)
    assert all(row["interpolation_padding_input_cell_count"] == 4 for row in rows)


def test_registered_adapter_remains_open_for_arbitrary_c0(payload):
    certificate = payload["certificate"]
    claims = certificate["claim_status"]
    assert all(claims[name] is True for name in TRUE_FLAGS)
    assert all(claims[name] is False for name in FALSE_FLAGS)
    evaluation = certificate["transfer_evaluation"]
    assert not evaluation["input_complete"]
    assert not evaluation["arbitrary_c0_linear_contraction_closes"]
    assert evaluation["continuous_phase_fixed_operator_norm_upper"] is None


def test_complete_synthetic_transfer_budget_closes_linear_gate(payload):
    certificate = payload["certificate"]
    budget = SignedKernelTransferBudget(
        voltage_continuous_transfer_error_upper="0.05",
        recovery_continuous_transfer_error_upper="0.04",
        phase_chart_continuous_transfer_error_upper="0.02",
        continuous_density_interval_method_of_steps_validated=True,
        exact_orbit_coefficient_and_period_transfer_validated=True,
        arbitrary_c0_dual_measure_identity_validated=True,
        continuous_phase_subtraction_before_total_variation_validated=True,
        evidence_status="synthetic hostile-control budget",
    )
    evaluation = evaluate_signed_kernel_transfer(
        discrete_voltage_upper=certificate["directed_voltage_shadow_norm_upper"],
        discrete_recovery_upper=certificate["directed_recovery_shadow_norm_upper"],
        discrete_phase_chart_upper=certificate[
            "directed_phase_chart_shadow_norm_upper"
        ],
        budget=budget,
    )
    assert evaluation.input_complete
    assert evaluation.strict_linear_contraction_inequality_holds
    assert evaluation.arbitrary_c0_linear_contraction_closes
    failed = evaluate_signed_kernel_transfer(
        discrete_voltage_upper=certificate["directed_voltage_shadow_norm_upper"],
        discrete_recovery_upper=certificate["directed_recovery_shadow_norm_upper"],
        discrete_phase_chart_upper=certificate[
            "directed_phase_chart_shadow_norm_upper"
        ],
        budget=replace(budget, voltage_continuous_transfer_error_upper="0.9"),
    )
    assert not failed.strict_linear_contraction_inequality_holds
    assert not failed.arbitrary_c0_linear_contraction_closes


def _refresh(value):
    value["manifest"]["certificate_sha256"] = canonical_sha256(
        value["certificate"]
    )


@pytest.mark.parametrize(
    "mutation",
    [
        lambda value: value["certificate"]["claim_status"].update(
            {"arbitrary_c0_input_covered_by_directed_kernel": True}
        ),
        lambda value: value["certificate"]["transfer_evaluation"].update(
            {"arbitrary_c0_linear_contraction_closes": True}
        ),
        lambda value: value["certificate"].update(
            {"directed_phase_fixed_shadow_norm_upper": "0"}
        ),
        lambda value: value["certificate"]["directed_output_rows"][0].update(
            {"interpolation_padding_input_cell_count": 0}
        ),
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
        validate_outer_signed_kernel_stage2_result(changed, REPOSITORY)


def test_note_keeps_directed_shadow_and_continuous_theorem_separate():
    text = (REPOSITORY / "docs/leaky-outer-signed-kernel-stage2.md").read_text()
    normalized = " ".join(text.split())
    assert "not yet a" in normalized and "history operator bound" in normalized
    assert "current-value Dirac atom" in normalized
    assert "absolutely continuous history density" in normalized
    assert "phase-corrected density before integrating its absolute value" in normalized
    assert "linear return contraction remain false" in normalized
