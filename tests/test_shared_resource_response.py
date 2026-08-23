from __future__ import annotations

import pytest
import sympy as sp

from canard_control.shared_resource_response import (
    shared_resource_response_audit,
)


def _data():
    pi = sp.Matrix(
        [sp.Rational(1, 6), sp.Rational(1, 3), sp.Rational(1, 2)]
    )
    mixing = sp.Rational(1, 3)
    transition = (
        (1 - mixing) * sp.eye(3)
        + mixing * sp.ones(3, 1) * pi.T
    )
    base_0 = sp.Matrix(
        [
            [sp.Rational(1, 4), sp.Rational(1, 8), sp.Rational(1, 6)],
            [sp.Rational(1, 7), sp.Rational(1, 5), sp.Rational(1, 9)],
            [sp.Rational(1, 10), sp.Rational(1, 6), sp.Rational(1, 4)],
        ]
    )
    base_1 = sp.Matrix(
        [
            [sp.Rational(1, 5), sp.Rational(1, 11), sp.Rational(1, 7)],
            [sp.Rational(1, 8), sp.Rational(1, 6), sp.Rational(1, 10)],
            [sp.Rational(1, 9), sp.Rational(1, 12), sp.Rational(1, 5)],
        ]
    )
    transverse_vector = sp.Matrix([1, 1, -1])
    assert (pi.T * transverse_vector)[0] == 0
    direction_0 = transverse_vector * pi.T
    direction_1 = -direction_0
    return transition, pi, (base_0, base_1), (direction_0, direction_1)


def test_projection_neutral_direction_forces_stable_jet_but_not_order_three() -> None:
    transition, pi, base, direction = _data()
    result = shared_resource_response_audit(
        transition,
        pi,
        base,
        direction,
        (sp.Rational(1, 2), sp.Rational(3, 2)),
        coupling_rate=sp.Rational(5, 2),
        weak_gain=sp.Rational(7, 3),
    )

    assert result.direct_projected_atoms == (0, 0)
    assert not result.transverse_moment_forcing.is_zero_matrix
    assert not result.first_stable_direction_jet.is_zero_matrix
    assert result.stable_jet_is_transverse == 0
    assert result.direction_on_base_constant == 0
    assert result.constant_history_return == 0
    assert result.interior_order_three_response == 0


def test_transverse_inverse_is_the_inverse_on_the_stable_space() -> None:
    transition, pi, base, direction = _data()
    result = shared_resource_response_audit(
        transition,
        pi,
        base,
        direction,
        (1, 2),
    )
    generator = sp.Matrix(result.stable_generator)
    inverse = sp.Matrix(result.transverse_inverse)
    transverse = sp.Matrix(result.transverse_projector)

    assert sp.simplify(generator * inverse - transverse) == sp.zeros(3)
    assert sp.simplify(inverse * generator - transverse) == sp.zeros(3)


def test_non_neutral_atom_is_rejected() -> None:
    transition, pi, base, direction = _data()
    bad = list(direction)
    bad[0] = bad[0] + sp.eye(3)
    with pytest.raises(ValueError, match="complete projected"):
        shared_resource_response_audit(
            transition,
            pi,
            base,
            bad,
            (1, 2),
        )
