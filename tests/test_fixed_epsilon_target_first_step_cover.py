"""Tests for the complete first method-of-steps target interval cover."""

from __future__ import annotations

from copy import deepcopy
from decimal import Decimal
import json
from pathlib import Path

import gmpy2
import pytest

from canard_control.fixed_epsilon_target_first_step_cover import (
    FALSE_METHOD_FLAGS,
    OPEN_FLAGS,
    RIGOROUS_TRUE_FLAGS,
    TargetFirstMethodStepCoverCertificate,
    _symmetric_error,
    build_target_first_method_step_cover_certificate,
    exact_first_step_cover_defects,
    json_ready_target_first_method_step_cover,
    validate_target_first_method_step_cover_audit,
    validate_target_first_method_step_cover_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]
RESULT = (
    REPOSITORY
    / "experiments/results/fixed_epsilon_target_first_step_cover.json"
)


@pytest.fixture(scope="module")
def certificate() -> TargetFirstMethodStepCoverCertificate:
    return build_target_first_method_step_cover_certificate()


def _audit() -> dict[str, object]:
    return json_ready_target_first_method_step_cover()


def _result() -> dict[str, object]:
    return json.loads(RESULT.read_text(encoding="utf-8"))


def test_exact_patch_variation_hermite_and_frame_audit_is_zero() -> None:
    defects = exact_first_step_cover_defects()
    assert len(defects) == 14
    assert all(defect == 0 for defect in defects)


def test_picard_symmetric_error_uses_declared_precision_endpoints() -> None:
    precision = 192
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        radius = gmpy2.mpfr("1.23456789012345678901234567890123456789e-10")
    box = _symmetric_error(radius, precision)
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        exact_lower = -box.upper
    assert box.lower.precision == precision
    assert box.upper.precision == precision
    assert box.lower == exact_lower


def test_complete_first_method_step_grid_closes(
    certificate: TargetFirstMethodStepCoverCertificate,
) -> None:
    assert certificate.physical_time_interval == ("-3", "1")
    assert certificate.label_interval == ("-0.05", "0.05")
    assert certificate.time_cell_count_per_label == 400
    assert certificate.label_cell_count == 20
    assert certificate.total_time_label_cell_count == 8000
    assert certificate.patch_time_cell_count_per_label == 50
    for probe, precision in (
        (certificate.primary, 192),
        (certificate.refinement, 256),
    ):
        assert probe.precision_bits == precision
        assert probe.completed_label_cells == 20
        assert probe.completed_time_cells == 8000
        assert probe.c4_patch_cell_count == 1000
        assert probe.first_failure is None
        assert len(probe.proof_cell_digest_sha256) == 64


def test_primary_cover_has_strict_p_matrix_and_picard_margins(
    certificate: TargetFirstMethodStepCoverCertificate,
) -> None:
    probe = certificate.primary
    assert Decimal(probe.minimum_central_picard_gap) > Decimal("1.6e-13")
    assert Decimal(probe.minimum_first_variation_picard_gap) > Decimal("1.8e-10")
    assert Decimal(probe.minimum_second_variation_picard_gap) > Decimal("1.2e-11")
    assert Decimal(probe.maximum_central_error_radius) < Decimal("0.00017")
    assert Decimal(probe.maximum_first_variation_error_radius) < Decimal("0.0017")
    assert Decimal(probe.maximum_second_variation_error_radius) < Decimal("0.148")
    assert Decimal(probe.minimum_time_minor) > Decimal("0.278")
    assert Decimal(probe.minimum_label_minor) > Decimal("0.9999999")
    assert Decimal(probe.minimum_oriented_determinant) > Decimal("1.47")
    assert Decimal(probe.maximum_raw_determinant) < Decimal("-0.113")
    assert Decimal(probe.maximum_early_x_time_derivative) < Decimal("-0.449")


def test_claim_ledger_promotes_only_the_first_method_step(
    certificate: TargetFirstMethodStepCoverCertificate,
) -> None:
    assert all(getattr(certificate, name) for name in RIGOROUS_TRUE_FLAGS)
    assert all(not getattr(certificate, name) for name in FALSE_METHOD_FLAGS)
    assert all(not getattr(certificate, name) for name in OPEN_FLAGS)
    assert "complete first method-of-steps strip" in certificate.exact_scope
    assert "(1,3]" in certificate.open_scope


def test_validator_rejects_bound_tampering_and_claim_promotion(
    certificate: TargetFirstMethodStepCoverCertificate,
) -> None:
    del certificate
    promoted = deepcopy(_audit())
    promoted["certificate"]["full_physical_strip_interval_cover_validated"] = True
    with pytest.raises(ValueError, match="open target-chart claim"):
        validate_target_first_method_step_cover_audit(promoted)

    sampled = deepcopy(_audit())
    sampled["certificate"][
        "binary64_sampling_or_flow_values_used_to_accept_a_margin"
    ] = True
    with pytest.raises(ValueError, match="forbidden acceptance method"):
        validate_target_first_method_step_cover_audit(sampled)

    changed = deepcopy(_audit())
    changed["certificate"]["primary"]["minimum_time_minor"] = "0.5"
    with pytest.raises(ValueError, match="differs from reference"):
        validate_target_first_method_step_cover_audit(changed)


def test_validator_rejects_nonpositive_picard_or_p_matrix_data(
    certificate: TargetFirstMethodStepCoverCertificate,
) -> None:
    del certificate
    zero_gap = deepcopy(_audit())
    zero_gap["certificate"]["primary"]["minimum_second_variation_picard_gap"] = "0"
    with pytest.raises(ValueError, match="is not positive"):
        validate_target_first_method_step_cover_audit(zero_gap)

    zero_minor = deepcopy(_audit())
    zero_minor["certificate"]["refinement"]["minimum_oriented_determinant"] = "0"
    with pytest.raises(ValueError, match="is not positive"):
        validate_target_first_method_step_cover_audit(zero_minor)


def test_generated_result_and_source_provenance_validate(
    certificate: TargetFirstMethodStepCoverCertificate,
) -> None:
    del certificate
    validate_target_first_method_step_cover_result(_result(), REPOSITORY)

    corrupted = deepcopy(_result())
    corrupted["manifest"]["c4_seam_source_sha256"] = "0" * 64
    with pytest.raises(ValueError, match="c4_seam_source hash changed"):
        validate_target_first_method_step_cover_result(corrupted, REPOSITORY)


def test_note_separates_first_step_proof_from_open_full_strip() -> None:
    text = (
        REPOSITORY / "docs/fixed-epsilon-target-first-step-cover.md"
    ).read_text(encoding="utf-8")
    assert "complete first method-of-steps rectangle" in text
    assert "8,000" in text
    assert "second label variation" in text
    assert "Bernstein" in text
    assert "Binary64 RK4 values" in " ".join(text.split())
    assert "not yet the full physical strip" in text
    assert "(1,3]" in text
