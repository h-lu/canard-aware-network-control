from __future__ import annotations

from copy import deepcopy
from decimal import Decimal
import json
from pathlib import Path

import pytest

from canard_control.leaky_outer_signed_row_stage3f_adjoint import (
    FALSE_FLAGS,
    RESULT_RELATIVE_PATH,
    SOURCE_MANIFEST,
    TRUE_FLAGS,
    canonical_sha256,
    validate_outer_signed_row_stage3f_adjoint_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def payload():
    return json.loads((REPOSITORY / RESULT_RELATIVE_PATH).read_text())


def test_registered_stage3f_result_replays(payload):
    validate_outer_signed_row_stage3f_adjoint_result(payload, REPOSITORY)


def test_advanced_row_combines_every_cancellation(payload):
    identity = payload["certificate"]["combined_advanced_row_identity"]
    assert "q_v(sigma)/q_v(0)" in identity["voltage_row"]
    assert "p(u+tau_j)B_j" in identity["advanced_equation"]
    assert "sum_{j:theta>=-tau_j}" in identity["history_density"]
    assert "delay words, both injection branches and phase subtraction" in identity[
        "ordering"
    ]


def test_instantaneous_green_is_strict_but_delayed_part_is_open(payload):
    green = payload["certificate"]["instantaneous_green"]
    assert green["phase_cell_count"] == 1024
    assert green["fundamental_polynomial_degree"] == 24
    assert Decimal(green["minimum_replayed_determinant_abs_lower"]) > 0
    assert Decimal(green["instantaneous_green_phase_integral_upper"]) > 0
    assert green["directed_polynomial_replay_validated"]
    assert not green["delayed_green_part_included"]


def test_exact_defect_and_phase_ratio_budgets_are_strict(payload):
    defect = payload["certificate"]["exact_defect_budget"]
    assert defect["coefficient_defect_budget_validated"]
    assert defect["phase_ratio_transfer_validated"]
    assert Decimal(defect["full_advanced_operator_variation_upper"]) > 0
    assert Decimal(defect["rank_one_advanced_operator_variation_upper"]) > 0
    assert Decimal(defect["voltage_phase_ratio_transfer_error_upper"]) < Decimal(
        "1e-5"
    )
    assert Decimal(defect["recovery_phase_ratio_transfer_error_upper"]) < Decimal(
        "1e-5"
    )


def test_center_rows_are_direct_but_diagnostic(payload):
    diagnostic = payload["certificate"]["center_signed_row_diagnostic"]
    assert diagnostic["all_words_injections_and_phase_combined_inside_p"]
    assert diagnostic["diagnostic_only"]
    assert Decimal(
        diagnostic["center_voltage_signed_row_norm_binary64"]["decimal"]
    ) < Decimal("0.14")
    assert Decimal(
        diagnostic["center_recovery_signed_row_norm_binary64"]["decimal"]
    ) < Decimal("0.004")


def test_closure_targets_are_positive_but_not_promoted(payload):
    targets = payload["certificate"]["residual_closure_targets"]
    assert targets["full_advanced_green_target"] == "60000"
    assert targets["no_separate_H_or_L_absolute_budget_used"]
    assert not targets["full_targets_validated"]
    assert Decimal(
        targets["delayed_green_allowance_after_strict_instantaneous_part_lower"]
    ) > 0
    assert Decimal(
        targets["delayed_boundary_allowance_after_strict_instantaneous_part_lower"]
    ) > 0
    for row in targets["rows"].values():
        assert Decimal(row["combined_p_voltage_component_binary64_diagnostic"]) < Decimal(
            row["combined_p_uniform_binary64_diagnostic"]
        )
        assert row["required_combined_p_bernstein_residual_upper"] is not None
        assert Decimal(row["required_combined_p_bernstein_residual_upper"]) > 0
        assert row["budget_closes_if_targets_are_proved"]
        assert not row["diagnostic_inputs_promoted"]


def test_open_transfer_and_contraction_claims_remain_false(payload):
    certificate = payload["certificate"]
    claims = certificate["claim_status"]
    assert all(claims[name] is True for name in TRUE_FLAGS)
    assert all(claims[name] is False for name in FALSE_FLAGS)
    assert certificate["transfer_errors"]["E_voltage"] is None
    assert certificate["transfer_errors"]["E_recovery"] is None
    gate = certificate["transfer_gate"]
    assert gate["instantaneous_green_part_validated"]
    assert not gate["delayed_green_part_validated"]
    assert not gate["arbitrary_c0_linear_contraction_closes"]


def _refresh(value):
    value["manifest"]["certificate_sha256"] = canonical_sha256(
        value["certificate"]
    )


@pytest.mark.parametrize(
    "mutation",
    [
        lambda value: value["certificate"]["claim_status"].update(
            {"delayed_advanced_green_integral_bound_validated": True}
        ),
        lambda value: value["certificate"]["transfer_errors"].update(
            {"E_voltage": "0"}
        ),
        lambda value: value["certificate"]["residual_closure_targets"].update(
            {"full_targets_validated": True}
        ),
        lambda value: value["certificate"]["center_signed_row_diagnostic"].update(
            {"diagnostic_only": False}
        ),
        lambda value: value["manifest"]["source_sha256"].update(
            {SOURCE_MANIFEST[0]: "0" * 64}
        ),
    ],
)
def test_hostile_promotions_are_rejected(payload, mutation):
    changed = deepcopy(payload)
    mutation(changed)
    _refresh(changed)
    with pytest.raises(ValueError):
        validate_outer_signed_row_stage3f_adjoint_result(changed, REPOSITORY)


def test_note_has_no_control_characters_or_false_completion():
    text = (
        REPOSITORY / "docs/leaky-outer-signed-row-stage3f-adjoint.md"
    ).read_text()
    assert "\t" not in text
    assert all(character in "\n\r" or ord(character) >= 32 for character in text)
    normalized = " ".join(text.split())
    assert "All delay words, both injection branches and phase subtraction" in normalized
    assert "not achieved error bounds" in normalized
    assert "all remain false" in normalized
