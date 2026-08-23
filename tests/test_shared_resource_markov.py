from __future__ import annotations

import numpy as np
import pytest
import sympy as sp
from scipy.linalg import expm

from canard_control.shared_resource_markov import (
    dobrushin_coefficient,
    markov_graph_audit,
    shared_resource_blowup_audit,
)


def _example_data():
    pi = sp.Matrix(
        [sp.Rational(1, 6), sp.Rational(1, 3), sp.Rational(1, 2)]
    )
    mixing = sp.Rational(1, 3)
    transition = (
        (1 - mixing) * sp.eye(3)
        + mixing * sp.ones(3, 1) * pi.T
    )
    layer_0 = sp.Matrix(
        [
            [sp.Rational(1, 6), sp.Rational(1, 12), sp.Rational(1, 9)],
            [sp.Rational(1, 10), sp.Rational(1, 5), sp.Rational(1, 8)],
            [sp.Rational(1, 7), sp.Rational(1, 11), sp.Rational(1, 6)],
        ]
    )
    layer_1 = sp.Matrix(
        [
            [sp.Rational(1, 4), sp.Rational(1, 13), sp.Rational(1, 5)],
            [sp.Rational(1, 9), sp.Rational(1, 6), sp.Rational(1, 7)],
            [sp.Rational(1, 8), sp.Rational(1, 10), sp.Rational(1, 4)],
        ]
    )
    return transition, pi, layer_0, layer_1


def _oscillation(vector: np.ndarray) -> float:
    return float(np.max(vector) - np.min(vector))


def test_dobrushin_gap_and_transverse_semigroup() -> None:
    transition, pi, _, _ = _example_data()
    audit = markov_graph_audit(
        transition,
        pi,
        coupling_rate=sp.Rational(5, 2),
    )
    assert audit.dobrushin == sp.Rational(2, 3)
    assert audit.mixing_gap == sp.Rational(1, 3)
    assert dobrushin_coefficient(transition) == audit.dobrushin
    assert audit.critical_projector * audit.critical_projector == (
        audit.critical_projector
    )
    assert audit.transverse_projector * audit.transverse_projector == (
        audit.transverse_projector
    )
    assert audit.fast_jacobian * sp.ones(3, 1) == sp.zeros(3, 1)
    assert pi.T * audit.fast_jacobian == sp.zeros(1, 3)
    assert audit.fold_curvature == -2

    generator = np.asarray(audit.fast_jacobian, dtype=float)
    pi_np = np.asarray(pi, dtype=float).reshape(-1)
    rate_gap = 2.5 / 3.0
    for vector in (
        np.array([-2.0, 1.0, 4.0]),
        np.array([3.0, -1.0, 2.0]),
    ):
        vector = vector - np.dot(pi_np, vector)
        initial = _oscillation(vector)
        for time in (0.0, 0.2, 1.0, 3.0):
            evolved = expm(generator * time) @ vector
            assert _oscillation(evolved) <= (
                np.exp(-rate_gap * time) * initial + 1.0e-12
            )


def test_exact_shared_resource_fold_chart() -> None:
    transition, pi, layer_0, layer_1 = _example_data()
    audit = shared_resource_blowup_audit(
        transition,
        pi,
        layer_0,
        layer_1,
        coupling_rate=sp.Rational(5, 2),
    )
    assert audit.critical_division_remainder == 0
    assert audit.resource_division_remainder == 0
    assert audit.stable_division_remainder.is_zero_matrix
    assert audit.critical_residual == 0
    assert audit.resource_residual == 0
    assert audit.stable_residual.is_zero_matrix
    assert pi.T * audit.stable_voltage == sp.zeros(1, 1)
    assert pi.T * audit.delayed_stable_voltage_0 == sp.zeros(1, 1)
    assert pi.T * audit.delayed_stable_voltage_1 == sp.zeros(1, 1)
    assert audit.displayed_resource_rhs == (
        -audit.critical_x + audit.delta * audit.unfolding
    )


def test_projection_neutral_layer_can_force_the_transverse_space() -> None:
    transition, pi, _, _ = _example_data()
    graph = markov_graph_audit(transition, pi)
    transverse_vector = sp.Matrix([1, 1, -1])
    assert (pi.T * transverse_vector)[0] == 0
    residual = transverse_vector * pi.T
    ones = sp.ones(3, 1)
    assert pi.T * residual * ones == sp.zeros(1, 1)
    assert graph.transverse_projector * residual * ones == transverse_vector

    # Opposite residuals at distinct atoms preserve total current gain while
    # their history forcing is nonzero.
    assert residual + (-residual) == sp.zeros(3)


def test_invalid_stationary_data_are_rejected() -> None:
    transition, pi, _, _ = _example_data()
    with pytest.raises(ValueError, match="invariant"):
        markov_graph_audit(transition, sp.Matrix([sp.Rational(1, 3)] * 3))
    with pytest.raises(ValueError, match="nonnegative"):
        bad = sp.Matrix(transition)
        bad[0, 0] = -1
        markov_graph_audit(bad, pi)


def test_symbolic_positive_markov_family_has_exact_dobrushin_gap() -> None:
    p = sp.Symbol("p", positive=True)
    pi = sp.Matrix([sp.Rational(1, 2), sp.Rational(1, 2)])
    transition = (
        p / (1 + p) * sp.eye(2)
        + 1 / (1 + p) * sp.ones(2, 1) * pi.T
    )
    audit = markov_graph_audit(transition, pi)

    assert sp.simplify(audit.dobrushin - p / (1 + p)) == 0
    assert sp.simplify(audit.mixing_gap - 1 / (1 + p)) == 0
