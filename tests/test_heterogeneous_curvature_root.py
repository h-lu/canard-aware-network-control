import sympy as sp
import pytest

from canard_control.heterogeneous_curvature_root import (
    heterogeneous_curvature_root_audit,
    normalized_no_synchrony_quotient_family,
)


def test_general_projection_neutral_hessian_return_is_exact():
    transition = sp.Matrix(
        [
            [sp.Rational(1, 2), sp.Rational(1, 3), sp.Rational(1, 6)],
            [sp.Rational(1, 4), sp.Rational(1, 2), sp.Rational(1, 4)],
            [sp.Rational(1, 6), sp.Rational(1, 3), sp.Rational(1, 2)],
        ]
    )
    stationary = sp.Matrix([sp.Rational(3, 10), sp.Rational(2, 5), sp.Rational(3, 10)])
    curvature = sp.Matrix([sp.Rational(4, 5), 1, sp.Rational(6, 5)])
    transverse_vector = sp.Matrix([-1, 0, 1])
    direction = transverse_vector * stationary.T
    theta_0, theta_1 = sp.Integer(1), sp.Integer(3)

    audit = heterogeneous_curvature_root_audit(
        transition,
        stationary,
        curvature,
        [direction, -direction],
        [theta_0, theta_1],
        coupling_rate=sp.Integer(2),
        weak_gain=sp.Integer(5),
    )

    assert all(row == sp.zeros(1, 3) for row in audit.full_row_projection_atoms)
    assert sp.simplify((stationary.T * audit.first_stable_direction_jet)[0]) == 0
    assert audit.transverse_delay_forcing != sp.zeros(3, 1)
    assert audit.critical_hessian_return != 0
    assert sp.simplify(
        audit.q2_melnikov_pairing
        - sp.sqrt(2 * sp.pi)
        * audit.critical_hessian_return
        / audit.mean_curvature
    ) == 0
    assert sp.simplify(
        audit.selected_root_shift_coefficient
        + audit.critical_hessian_return / audit.mean_curvature
    ) == 0


def test_normalized_family_has_dimension_independent_root_coefficient():
    sigma = sp.Rational(1, 5)
    floor = sp.Integer(2)
    theta_0, theta_1 = sp.Integer(1), sp.Integer(4)
    rate = sp.Integer(3)
    gain = sp.Integer(7)
    expected_root_coefficient = sp.simplify(
        gain * sigma * (theta_0 - theta_1) / (2 * rate)
    )
    expected_leading_root = sp.simplify(
        -sp.Rational(1, 8) + 3 * sigma**2 / (4 * rate)
    )

    for node_count in (2, 3, 4, 7, 11):
        family = normalized_no_synchrony_quotient_family(
            node_count,
            curvature_amplitude=sigma,
            layer_floor=floor,
            delay_0=theta_0,
            delay_1=theta_1,
            coupling_rate=rate,
            weak_gain=gain,
        )
        assert family.profile_mean == 0
        assert family.profile_variance == 1
        assert family.curvature_entries_are_distinct
        assert family.audit.mean_curvature == 1
        assert sp.simplify(
            family.audit.selected_root_shift_coefficient
            - expected_root_coefficient
        ) == 0
        assert sp.simplify(family.audit.leading_root - expected_leading_root) == 0


def test_positive_delay_layers_inside_exact_radius():
    family = normalized_no_synchrony_quotient_family(
        8,
        curvature_amplitude=sp.Rational(1, 10),
        layer_floor=sp.Integer(1),
        delay_0=sp.Integer(1),
        delay_1=sp.Integer(2),
    )
    zeta = family.positivity_radius / 2
    for base, direction in zip(family.base_layers, family.direction_layers):
        layer = sp.simplify(base + zeta * direction)
        assert all(entry.is_positive is True for entry in layer)


def test_full_row_neutrality_is_required():
    transition = sp.ones(2, 2) / 2
    stationary = sp.ones(2, 1) / 2
    curvature = sp.Matrix([sp.Rational(4, 5), sp.Rational(6, 5)])
    merely_collective_neutral = sp.Matrix([[1, -1], [0, 0]])

    try:
        heterogeneous_curvature_root_audit(
            transition,
            stationary,
            curvature,
            [merely_collective_neutral],
            [sp.Integer(1)],
        )
    except ValueError as error:
        assert "pi.T * R_k" in str(error)
    else:
        raise AssertionError("full-row projection neutrality was not enforced")


@pytest.mark.parametrize(
    ("weak_gain", "cubic_coefficient", "message"),
    [
        (sp.Integer(0), sp.Integer(1), "weak_gain"),
        (sp.Integer(1), sp.Integer(0), "cubic_coefficient"),
        (sp.Integer(1), sp.Integer(-1), "cubic_coefficient"),
    ],
)
def test_model_parameters_reject_degenerate_gain_or_cubic(
    weak_gain,
    cubic_coefficient,
    message,
):
    transition = sp.ones(2, 2) / 2
    stationary = sp.ones(2, 1) / 2
    curvature = sp.Matrix([sp.Rational(4, 5), sp.Rational(6, 5)])
    transverse_vector = sp.Matrix([-1, 1])
    direction = transverse_vector * stationary.T

    with pytest.raises(ValueError, match=message):
        heterogeneous_curvature_root_audit(
            transition,
            stationary,
            curvature,
            [direction, -direction],
            [sp.Integer(1), sp.Integer(2)],
            weak_gain=weak_gain,
            cubic_coefficient=cubic_coefficient,
        )
