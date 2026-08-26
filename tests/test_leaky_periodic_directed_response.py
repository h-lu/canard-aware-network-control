"""Replay and hostile-tamper tests for the rigorous leaky D4 result."""

from __future__ import annotations

from copy import deepcopy
from decimal import Decimal, localcontext
from hashlib import sha256
import json
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pytest

import canard_control.leaky_periodic_directed_response as response
from canard_control.leaky_periodic_directed_response import (
    FALSE_FLAGS,
    RESULT_RELATIVE_PATH,
    TRUE_FLAGS,
    build_leaky_periodic_directed_response_certificate,
    exact_directed_response_defects,
    validate_leaky_periodic_directed_response_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]
EXPECTED_RESULT_SHA256: str | None = (
    "ec1f9861c1cdab37c081339f8acbd3b787f7870a8ac333871bd060788a3a38ec"
)


@pytest.fixture(scope="module")
def payload() -> dict:
    return json.loads((REPOSITORY / RESULT_RELATIVE_PATH).read_text())


@pytest.fixture(scope="module")
def certificate():
    return build_leaky_periodic_directed_response_certificate(
        str(REPOSITORY.resolve())
    )


def test_exact_leaky_parameter_columns_and_output_chain_rule() -> None:
    assert exact_directed_response_defects() == (0,) * 6


def test_implemented_parameter_columns_have_the_leaky_support_and_sign(
    monkeypatch,
) -> None:
    precision = 96
    point = lambda value: response.DirectedInterval.from_decimal(  # noqa: E731
        value, precision
    )
    zero = response._constant_sequence(point(0), precision)
    cubic = response._constant_sequence(point(3), precision)
    base = SimpleNamespace(
        period=point(2),
        parameters={"epsilon": point("0.2"), "tau_0": point(0), "tau_1": point(0)},
        current_coefficient=zero,
        delayed_coefficients=(zero, zero),
        period_voltage=zero,
        period_recovery=zero,
        phase_voltage=zero,
        phase_recovery=zero,
    )
    sensitivity = (zero, zero, point(0))
    monkeypatch.setattr(
        response, "_candidate_fields", lambda unused: (cubic, (zero, zero))
    )

    a_fast, a_slow, _ = response._sensitivity_residual(
        base, sensitivity, 0
    )
    k3_fast, k3_slow, _ = response._sensitivity_residual(
        base, sensitivity, 1
    )
    assert float(a_fast[0].real.upper_abs()) == 0
    assert float(a_slow[0].real.lower) == pytest.approx(0.4)
    assert float(k3_fast[0].real.upper) == pytest.approx(-1.2)
    assert float(k3_slow[0].real.upper_abs()) == 0


def test_tracked_result_hash_and_directed_replay(payload: dict) -> None:
    assert isinstance(EXPECTED_RESULT_SHA256, str)
    assert sha256((REPOSITORY / RESULT_RELATIVE_PATH).read_bytes()).hexdigest() == (
        EXPECTED_RESULT_SHA256
    )
    validate_leaky_periodic_directed_response_result(payload, REPOSITORY)


def test_both_nested_radii_and_sensitivity_budgets_close(certificate) -> None:
    expected_radii = {
        "inner_saddle_candidate": Decimal("1e-7"),
        "outer_pulse": Decimal("1e-6"),
    }
    for branch in (certificate.inner, certificate.outer):
        radii = branch.nested_radii
        assert Decimal(radii.nested_radius) == expected_radii[branch.branch]
        assert Decimal(radii.contraction_upper) < 1
        assert Decimal(radii.radii_margin_lower) > 0
        for budget in branch.sensitivities:
            assert Decimal(budget.base_preconditioned_residual_upper) >= 0
            assert Decimal(budget.preconditioned_variation_upper) >= 0
            assert Decimal(budget.exact_sensitivity_error_upper) > 0
            assert Decimal(budget.nested_contraction_upper) < 1


@pytest.mark.parametrize(
    ("attribute", "sign"),
    [("inner", -1), ("outer", 1)],
)
def test_directed_response_determinants_exclude_zero(
    certificate, attribute: str, sign: int
) -> None:
    branch = getattr(certificate, attribute)
    lower = Decimal(branch.determinant_lower)
    upper = Decimal(branch.determinant_upper)
    assert lower < upper
    assert upper < 0 if sign < 0 else lower > 0
    assert Decimal(branch.determinant_absolute_margin_lower) > 0
    assert Decimal(branch.smallest_singular_value_lower) > 0
    assert branch.determinant_sign == sign
    assert branch.determinant_nonzero_validated
    assert branch.pointwise_local_diffeomorphism_validated


def test_exact_extrema_are_bracketed_inside_disjoint_parent_windows(
    certificate,
) -> None:
    for branch in (certificate.inner, certificate.outer):
        maximum = branch.maximum_window
        minimum = branch.minimum_window
        assert Decimal(maximum.parent_phase_lower) <= Decimal(
            maximum.refined_phase_lower
        )
        assert Decimal(maximum.refined_phase_upper) <= Decimal(
            maximum.parent_phase_upper
        )
        assert Decimal(minimum.parent_phase_lower) <= Decimal(
            minimum.refined_phase_lower
        )
        assert Decimal(minimum.refined_phase_upper) <= Decimal(
            minimum.parent_phase_upper
        )
        assert Decimal(maximum.refined_phase_upper) < Decimal(
            minimum.refined_phase_lower
        )
        assert Decimal(maximum.left_derivative_lower) > 0
        assert Decimal(maximum.right_derivative_upper) < 0
        assert Decimal(minimum.left_derivative_upper) < 0
        assert Decimal(minimum.right_derivative_lower) > 0
        assert Decimal(maximum.parent_curvature_bound) < 0
        assert Decimal(minimum.parent_curvature_bound) > 0
        assert branch.exact_extremum_phase_terms_vanish


def test_claim_ledger_does_not_promote_pulse_or_safety_claims(certificate) -> None:
    for name in TRUE_FLAGS:
        assert getattr(certificate, name) is True
    for name in FALSE_FLAGS:
        assert getattr(certificate, name) is False
    assert certificate.quantitative_common_target_ball_validated == (
        certificate.inner.quantitative_target_ball_validated
        and certificate.outer.quantitative_target_ball_validated
    )


def test_new_directed_theorem_does_not_relabel_the_parent_padded_diagnostic(
    certificate,
) -> None:
    parent = json.loads(
        (
            REPOSITORY
            / "experiments/results/autonomous_leaky_recovery_parameter_response.json"
        ).read_text()
    )["artifact"]
    assert not parent["claim_status"]["exact_rfde_response_derivative_enclosed"]
    assert not parent["claim_status"][
        "uniform_frequency_amplitude_local_inverse_validated"
    ]
    assert not parent["directed_common_box"][
        "exact_first_sensitivities_validated"
    ]
    assert not parent["directed_common_box"][
        "exact_response_determinant_or_inverse_validated"
    ]
    assert certificate.directed_first_sensitivities_validated
    assert certificate.response_determinants_bounded_away_from_zero


def test_fixed_left_preconditioners_prove_branch_centered_target_balls(
    certificate,
) -> None:
    assert certificate.quantitative_common_target_ball_validated
    assert "exact G_branch(1/4,1/200)" in certificate.target_ball_definition
    assert "Euclidean output ball" in certificate.target_ball_definition
    assert "flagship outer interface" in certificate.target_ball_definition
    radii = []
    inverse_bounds = []
    for branch in (certificate.inner, certificate.outer):
        formation = Decimal(
            branch.left_preconditioner_formation_defect_upper
        )
        contraction = Decimal(
            branch.left_preconditioned_derivative_defect_upper
        )
        b_norm = Decimal(
            branch.left_preconditioner_2_to_infinity_norm_upper
        )
        radius = Decimal(branch.quantitative_target_ball_radius_lower)
        inverse_bound = Decimal(branch.parameter_inverse_lipschitz_upper)
        assert branch.left_preconditioner_formation_audited
        assert branch.derivative_defect_uniform_on_common_parameter_box
        assert formation < Decimal("1e-12")
        assert contraction < 1
        assert radius > 0
        assert inverse_bound > 0

        midpoint = np.asarray(
            [
                [float.fromhex(item) for item in row]
                for row in branch.response_midpoint_binary64_hex
            ]
        )
        stored_b = np.asarray(
            [
                [float.fromhex(item) for item in row]
                for row in branch.left_preconditioner_binary64_hex
            ]
        )
        assert stored_b == pytest.approx(np.linalg.inv(midpoint), abs=0, rel=0)
        binary_row_norm = max(np.linalg.norm(row) for row in stored_b)
        assert float(b_norm) >= binary_row_norm

        # Euclidean output distance is carried by ||B||_{2->infinity};
        # the parameter box is the infinity ball of radius h=1e-10.  Use
        # enough Decimal precision to retain the certificate's MPFR guard
        # digits rather than rounding the comparison at the default 28.
        with localcontext() as context:
            context.prec = 100
            assert radius <= Decimal("1e-10") * (1 - contraction) / b_norm
            assert inverse_bound >= b_norm / (1 - contraction)
        radii.append(radius)
        inverse_bounds.append(inverse_bound)

    common_radius = Decimal(
        certificate.quantitative_common_target_ball_radius_lower
    )
    common_inverse_bound = Decimal(
        certificate.common_parameter_inverse_lipschitz_upper
    )
    assert 0 < common_radius <= min(radii)
    assert common_inverse_bound >= max(inverse_bounds)
    assert Decimal(
        certificate.flagship_outer_target_ball_radius_lower
    ) == Decimal(certificate.outer.quantitative_target_ball_radius_lower)
    assert Decimal(
        certificate.flagship_outer_parameter_inverse_lipschitz_upper
    ) == Decimal(certificate.outer.parameter_inverse_lipschitz_upper)
    assert Decimal(
        certificate.flagship_outer_target_ball_radius_lower
    ) > Decimal(certificate.quantitative_common_target_ball_radius_lower)


@pytest.mark.parametrize(
    "mutation",
    [
        lambda value: value["certificate"].update(
            {"physical_pulse_unique_onset_validated": True}
        ),
        lambda value: value["certificate"]["inner"].update(
            {"determinant_nonzero_validated": 1}
        ),
        lambda value: value["certificate"]["outer"].update(
            {"determinant_lower": "0"}
        ),
        lambda value: value["certificate"]["inner"]["sensitivities"][0].update(
            {"exact_sensitivity_error_upper": "0"}
        ),
        lambda value: value["certificate"]["inner"]["maximum_window"].update(
            {"extra": False}
        ),
        lambda value: value["manifest"].update({"extra": "forbidden"}),
        lambda value: value["manifest"].update(
            {"certificate_sha256": "0" * 64}
        ),
        lambda value: value["manifest"]["parent_result_sha256"].update(
            {"parameter_box_parent": "0" * 64}
        ),
        lambda value: value["manifest"]["source_sha256"].update(
            {"source": "0" * 64}
        ),
        lambda value: value["manifest"]["sources"].update(
            {"extra": "hostile.py"}
        ),
    ],
)
def test_hostile_tampering_is_rejected(payload: dict, mutation) -> None:
    changed = deepcopy(payload)
    mutation(changed)
    with pytest.raises((ValueError, TypeError)):
        validate_leaky_periodic_directed_response_result(changed, REPOSITORY)


def test_note_keeps_the_pulse_threshold_claim_boundary() -> None:
    text = (REPOSITORY / "docs/leaky-periodic-directed-response.md").read_text()
    assert "does **not** prove" in text
    assert "unsquared" in text
    assert "pointwise local diffeomorphism" in text
    assert "target ball" in text
