"""Tests for the exact C4-history Bernstein P-matrix certificate."""

from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest
import sympy as sp

from canard_control.fixed_epsilon_target_c4_history_bernstein import (
    EXACT_TRUE_FLAGS,
    OPEN_FALSE_FLAGS,
    RELATIVE_TIME,
    TRANSVERSE,
    build_target_c4_history_bernstein_certificate,
    exact_bernstein_margin_records,
    exact_c4_patch_state,
    exact_history_p_matrix_polynomials,
    exact_unpatched_history_state,
    quadratic_field_parts,
    quadratic_field_sign,
    validate_target_c4_history_bernstein_audit,
    validate_target_c4_history_bernstein_result,
)
from canard_control.fixed_epsilon_target_c4_preparation_seam import (
    EXACT_PATCH_WIDTH,
    EXACT_TRANSVERSE,
    c4_prepared_history_jet,
)


REPOSITORY = Path(__file__).resolve().parents[1]
RESULT = (
    REPOSITORY
    / "experiments/results/fixed_epsilon_target_c4_history_bernstein.json"
)


def _result() -> dict:
    payload = json.loads(RESULT.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def test_quadratic_field_sign_is_exact_for_opposite_sign_parts() -> None:
    assert quadratic_field_sign(3 - sp.sqrt(5)) == 1
    assert quadratic_field_sign(2 - sp.sqrt(5)) == -1
    assert quadratic_field_sign(-2 + sp.sqrt(5)) == 1
    assert quadratic_field_sign(-3 + sp.sqrt(5)) == -1
    assert quadratic_field_parts(sp.Rational(7, 3) - 2 * sp.sqrt(5)) == (
        sp.Rational(7, 3),
        sp.Integer(-2),
    )


def test_exact_patch_formula_matches_seam_at_rational_points() -> None:
    x_exact, y_exact = exact_c4_patch_state()
    for relative in (sp.Rational(-1, 2), sp.Rational(-1, 4), sp.Integer(0)):
        for label in (sp.Rational(-1, 20), sp.Integer(0), sp.Rational(1, 20)):
            exact = (
                x_exact.subs({RELATIVE_TIME: relative, TRANSVERSE: label}),
                y_exact.subs({RELATIVE_TIME: relative, TRANSVERSE: label}),
            )
            numeric = c4_prepared_history_jet(
                float(-3 + relative), float(label), 0
            )
            assert float(sp.N(exact[0], 17)) == pytest.approx(numeric[0], abs=2e-13)
            assert float(sp.N(exact[1], 17)) == pytest.approx(numeric[1], abs=2e-13)
    far = exact_unpatched_history_state(-EXACT_PATCH_WIDTH, EXACT_TRANSVERSE)
    assert all(
        sp.expand(
            component.subs(RELATIVE_TIME, -EXACT_PATCH_WIDTH)
            - far[index]
        )
        == 0
        for index, component in enumerate((x_exact, y_exact))
    )


def test_all_210_bernstein_coefficients_have_exact_strict_margins() -> None:
    records = exact_bernstein_margin_records()
    assert [(record.degree_u, record.degree_v) for record in records] == [
        (12, 3),
        (13, 1),
        (25, 4),
    ]
    assert sum(record.coefficient_count for record in records) == 210
    assert all(record.accepted_unit_box_count == 1 for record in records)
    assert all(record.subdivision_depth == 0 for record in records)
    assert all(record.exact_reconstruction_identity_verified for record in records)
    assert all(
        record.every_coefficient_strictly_above_rational_bound
        for record in records
    )
    assert [record.strict_rational_lower_bound for record in records] == [
        "9/100",
        "24/25",
        "2/5",
    ]
    assert [record.minimum_coefficient_index for record in records] == [
        (4, 0),
        (6, 0),
        (7, 0),
    ]


def test_certificate_promotes_only_the_retained_history_gate() -> None:
    certificate = build_target_c4_history_bernstein_certificate()
    assert all(getattr(certificate, key) for key in EXACT_TRUE_FLAGS)
    assert all(not getattr(certificate, key) for key in OPEN_FALSE_FLAGS)
    assert certificate.retained_history_strict_rational_margins == (
        "9/100",
        "24/25",
        "2/5",
    )
    polynomials = exact_history_p_matrix_polynomials()
    assert tuple(polynomials) == (
        "negative_x_time_derivative",
        "positive_y_transverse_derivative",
        "negative_raw_jacobian_determinant",
    )


def test_audit_rejects_exact_weakening_and_open_gate_promotion() -> None:
    audit = _result()["audit"]
    weakened = deepcopy(audit)
    weakened["certificate"][EXACT_TRUE_FLAGS[0]] = False
    with pytest.raises(ValueError, match="weakened"):
        validate_target_c4_history_bernstein_audit(weakened)
    promoted = deepcopy(audit)
    promoted["certificate"][OPEN_FALSE_FLAGS[0]] = True
    with pytest.raises(ValueError, match="promoted"):
        validate_target_c4_history_bernstein_audit(promoted)
    falsified = deepcopy(audit)
    falsified["certificate"]["patch_exact_bernstein_margins"][0][
        "strict_rational_lower_bound"
    ] = "1/2"
    with pytest.raises(ValueError, match="differs from reference"):
        validate_target_c4_history_bernstein_audit(falsified)


def test_generated_result_and_manifest_revalidate() -> None:
    validate_target_c4_history_bernstein_result(_result(), REPOSITORY)
