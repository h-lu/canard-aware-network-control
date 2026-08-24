"""Tests for the first outward-rounded target physical cell."""

from __future__ import annotations

from copy import deepcopy
from decimal import Decimal
import json
from pathlib import Path

import pytest

from canard_control.fixed_epsilon_target_first_step_interval import (
    FALSE_METHOD_FLAGS,
    OPEN_FLAGS,
    RIGOROUS_TRUE_FLAGS,
    build_target_first_step_interval_certificate,
    exact_first_step_delay_remainder_and_frame_defects,
    exact_first_step_reduction_defects,
    json_ready_target_first_step_interval,
    validate_target_first_step_interval_audit,
    validate_target_first_step_interval_result,
)
from canard_control.fixed_epsilon_target_chart_univalence_gate import (
    PHYSICAL_FRAME_DETERMINANT,
    PHYSICAL_TIME_FRAME,
    PMatrixIntervalCell,
    validate_p_matrix_interval_cover,
)


REPOSITORY = Path(__file__).resolve().parents[1]
RESULT = (
    REPOSITORY
    / "experiments/results/fixed_epsilon_target_first_step_interval.json"
)


def _audit() -> dict[str, object]:
    return json_ready_target_first_step_interval()


def _result() -> dict[str, object]:
    return json.loads(RESULT.read_text(encoding="utf-8"))


def test_first_step_picard_taylor_cell_closes_with_strict_margins() -> None:
    certificate = build_target_first_step_interval_certificate()
    cell = certificate.primary_cell
    assert Decimal(cell.time_cell.lower) <= Decimal("-3")
    assert Decimal(cell.time_cell.upper) >= Decimal("-2.99")
    assert Decimal(cell.label_cell.lower) <= Decimal("-0.05")
    assert Decimal(cell.label_cell.upper) >= Decimal("0.05")
    assert all(Decimal(value) > Decimal("0.0008") for value in cell.picard_left_gap_lower)
    assert all(Decimal(value) > Decimal("0.0008") for value in cell.picard_right_gap_lower)
    assert all(Decimal(value) > 0 for value in cell.local_truncation_radius_upper)
    assert Decimal(cell.time_principal_minor.lower) > Decimal("0.11")
    assert Decimal(cell.lambda_principal_minor.lower) > Decimal("0.999")
    assert Decimal(cell.oriented_determinant.lower) > Decimal("5.34")
    assert Decimal(cell.raw_chart_determinant.upper) < Decimal("-0.41")


def test_first_step_state_and_variation_reduction_matches_rfde_exactly() -> None:
    assert exact_first_step_reduction_defects() == (0, 0, 0, 0)
    defects = exact_first_step_delay_remainder_and_frame_defects()
    assert len(defects) == 16
    assert all(defect == 0 for defect in defects)


def test_claim_ledger_keeps_one_cell_separate_from_the_open_cover() -> None:
    certificate = build_target_first_step_interval_certificate()
    assert all(getattr(certificate, name) for name in RIGOROUS_TRUE_FLAGS)
    assert all(not getattr(certificate, name) for name in FALSE_METHOD_FLAGS)
    assert all(not getattr(certificate, name) for name in OPEN_FLAGS)
    assert certificate.refinement_nested_in_primary
    assert certificate.physical_output_frame == PHYSICAL_TIME_FRAME
    assert certificate.physical_frame_determinant == PHYSICAL_FRAME_DETERMINANT
    assert certificate.primary_cell.precision_bits == 192
    assert certificate.refinement_precision_bits == 256
    assert "one physical" in certificate.exact_scope
    assert "full physical strip" in certificate.remaining_gate


def test_cell_is_accepted_by_the_existing_exact_cover_schema() -> None:
    cell = build_target_first_step_interval_certificate().primary_cell
    schema_cell = PMatrixIntervalCell(
        time_left="-3",
        time_right="-2.99",
        lambda_left="-0.05",
        lambda_right="0.05",
        time_minor_lower=cell.time_principal_minor.lower,
        lambda_minor_lower=cell.lambda_principal_minor.lower,
        oriented_determinant_lower=cell.oriented_determinant.lower,
    )
    margins = validate_p_matrix_interval_cover(
        [schema_cell],
        time_nodes=["-3", "-2.99"],
        lambda_nodes=["-0.05", "0.05"],
    )
    assert margins[0] > Decimal("0.11")
    assert margins[1] > Decimal("0.999")
    assert margins[2] > Decimal("5.34")


def test_validator_rejects_claim_promotion_and_bound_tampering() -> None:
    promoted = deepcopy(_audit())
    promoted["certificate"]["full_physical_strip_interval_cover_validated"] = True
    with pytest.raises(ValueError, match="open target-chart claim"):
        validate_target_first_step_interval_audit(promoted)

    binary = deepcopy(_audit())
    binary["certificate"]["binary64_flow_or_sampling_used"] = True
    with pytest.raises(ValueError, match="forbidden numerical method"):
        validate_target_first_step_interval_audit(binary)

    changed = deepcopy(_audit())
    changed["certificate"]["primary_cell"]["time_principal_minor"]["lower"] = "0.2"
    with pytest.raises(ValueError, match="differs from reference"):
        validate_target_first_step_interval_audit(changed)

    wrong_frame = deepcopy(_audit())
    wrong_frame["certificate"]["physical_output_frame"][0][0] = -6
    with pytest.raises(ValueError, match="physical output frame"):
        validate_target_first_step_interval_audit(wrong_frame)


def test_validator_rejects_missing_or_nonfinite_truncation_data() -> None:
    missing = deepcopy(_audit())
    missing["certificate"]["primary_cell"]["local_truncation_radius_upper"].pop()
    with pytest.raises(ValueError, match="wrong shape"):
        validate_target_first_step_interval_audit(missing)

    nonfinite = deepcopy(_audit())
    nonfinite["certificate"]["primary_cell"]["local_truncation_radius_upper"][0] = "nan"
    with pytest.raises(ValueError, match="must be finite"):
        validate_target_first_step_interval_audit(nonfinite)


def test_validator_rejects_zero_picard_or_p_matrix_margin() -> None:
    zero_gap = deepcopy(_audit())
    zero_gap["certificate"]["primary_cell"]["picard_left_gap_lower"][0] = "0"
    with pytest.raises(ValueError, match="lost strict inclusion"):
        validate_target_first_step_interval_audit(zero_gap)

    zero_minor = deepcopy(_audit())
    zero_minor["certificate"]["primary_cell"]["lambda_principal_minor"]["lower"] = "0"
    with pytest.raises(ValueError, match="strict positive margin"):
        validate_target_first_step_interval_audit(zero_minor)


def test_generated_result_and_provenance_validate() -> None:
    validate_target_first_step_interval_result(_result(), REPOSITORY)

    corrupted = deepcopy(_result())
    corrupted["manifest"]["interval_backend_source_sha256"] = "0" * 64
    with pytest.raises(ValueError, match="interval_backend_source hash changed"):
        validate_target_first_step_interval_result(corrupted, REPOSITORY)


def test_note_states_single_cell_scope_and_all_three_error_sources() -> None:
    text = (
        REPOSITORY / "docs/fixed-epsilon-target-first-step-interval.md"
    ).read_text(encoding="utf-8")
    assert "one rigorous computer-assisted physical cell" in text
    assert "directed MPFR rounding" in text
    assert "local truncation remainder" in text
    assert "wrapping" in text
    assert "no global chart" in text
    assert "full physical cover" in text
