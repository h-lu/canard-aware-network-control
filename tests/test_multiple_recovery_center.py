from __future__ import annotations

import pytest
import sympy as sp

from canard_control.multiple_recovery_center import (
    collective_projector,
    generalized_center_coordinates,
    linear_matching_parameter_lower_bound_for_post_phase_center,
    linear_matching_parameter_lower_bound_for_transverse_center,
    multiple_recovery_center_audit,
    no_delay_characteristic_factor,
    positive_epsilon_jacobian,
    rescaled_slow_limit_factor,
    singular_current_jacobian,
    singular_voltage_matrix,
)


@pytest.mark.parametrize(
    ("node_count", "weights"),
    [
        (1, None),
        (2, (1, 1)),
        (3, (1, 2, 4)),
        (6, (1, 1, 2, 3, 5, 8)),
    ],
)
def test_exact_singular_center_dimensions_and_jordan_chain(
    node_count: int, weights: tuple[int, ...] | None
) -> None:
    rate = sp.Rational(7, 3)
    audit = multiple_recovery_center_audit(node_count, rate, weights)
    p = sp.Matrix(audit.collective_projector)
    q = sp.Matrix(audit.transverse_projector)
    a = sp.Matrix(audit.voltage_matrix)
    j = sp.Matrix(audit.singular_jacobian)
    fold = sp.Matrix(audit.fold_eigenvector)
    generalized = sp.Matrix(audit.fold_generalized_vector)
    transverse_center = sp.Matrix(audit.transverse_center_basis)

    assert p * p == p
    assert q * q == q
    assert a == -rate * q
    assert j * fold == sp.zeros(2 * node_count, 1)
    assert j * generalized == fold
    assert j * transverse_center == sp.zeros(
        2 * node_count, node_count - 1
    )

    assert audit.kernel_dimension == node_count
    assert audit.generalized_center_dimension == node_count + 1
    assert 2 * node_count - (j**3).rank() == node_count + 1
    assert audit.generalized_center_basis.rank() == node_count + 1
    assert audit.transverse_center_basis.rank() == node_count - 1
    assert audit.transverse_center_coordinate_count == node_count - 1
    assert audit.post_phase_center_coordinate_count == node_count


def test_generalized_center_coordinate_map_is_exact_and_detects_off_center() -> None:
    node_count = 4
    rate = sp.Rational(5, 2)
    p = sp.Matrix(collective_projector(node_count, (1, 2, 3, 4)))
    a = sp.Matrix(singular_voltage_matrix(node_count, rate, (1, 2, 3, 4)))
    ones = sp.ones(node_count, 1)
    raw = sp.Matrix([2, -1, 4, 3])
    transverse = (sp.eye(node_count) - p) * raw
    alpha = sp.Rational(7, 5)
    beta = sp.Rational(-11, 6)
    state = (alpha * ones + transverse).col_join(
        a * transverse - beta * ones
    )

    coordinates = generalized_center_coordinates(state, a, p)

    assert coordinates.fold_eigen_coordinate == alpha
    assert coordinates.fold_generalized_coordinate == beta
    assert coordinates.transverse_voltage == transverse
    assert coordinates.reconstruction == state
    assert coordinates.residual == sp.zeros(2 * node_count, 1)

    off_center = state + sp.zeros(node_count, 1).col_join(
        sp.Matrix([1, 0, 0, 0])
    )
    off_coordinates = generalized_center_coordinates(off_center, a, p)
    assert off_coordinates.residual != sp.zeros(2 * node_count, 1)


def test_dimension_obstruction_is_not_an_artifact_of_rank_one_coupling() -> None:
    laplacian = sp.Matrix(
        [
            [1, -1, 0],
            [0, 2, -2],
            [-3, 0, 3],
        ]
    )
    assert laplacian * sp.ones(3, 1) == sp.zeros(3, 1)
    assert laplacian.rank() == 2
    assert (laplacian**2).rank() == 2

    singular = sp.Matrix(singular_current_jacobian(-laplacian))
    assert 6 - singular.rank() == 3
    assert 6 - (singular**2).rank() == 4
    assert 6 - (singular**3).rank() == 4

    lam, eps = sp.symbols("lambda epsilon")
    positive = sp.Matrix(positive_epsilon_jacobian(-laplacian, eps))
    assert sp.factor(
        (lam * sp.eye(6) - positive).det()
        - (lam**2 * sp.eye(3) + lam * laplacian + eps * sp.eye(3)).det()
    ) == 0


@pytest.mark.parametrize("node_count", [1, 2, 3, 5])
def test_no_delay_characteristic_determinant_factorization(
    node_count: int,
) -> None:
    lam, eps = sp.symbols("lambda epsilon")
    rate = sp.Rational(9, 4)
    a = sp.Matrix(singular_voltage_matrix(node_count, rate))
    j_eps = sp.Matrix(positive_epsilon_jacobian(a, eps))
    determinant = sp.expand((lam * sp.eye(2 * node_count) - j_eps).det())
    expected = no_delay_characteristic_factor(node_count, lam, eps, rate)

    assert sp.factor(determinant - expected) == 0


def test_slow_rescaling_limit_has_exact_transverse_multiplicity() -> None:
    eps, zeta, rate = sp.symbols("epsilon zeta D", nonzero=True)
    node_count = 5
    characteristic = no_delay_characteristic_factor(
        node_count, eps * zeta, eps, rate
    )
    rescaled = sp.expand(characteristic / eps**node_count)
    limit = sp.limit(rescaled, eps, 0)

    assert sp.factor(
        limit - rescaled_slow_limit_factor(node_count, zeta, rate)
    ) == 0
    assert sp.factor(limit) == (1 + rate * zeta) ** (node_count - 1)


@pytest.mark.parametrize("node_count", [1, 2, 7])
def test_conditional_linear_matching_parameter_lower_bounds(
    node_count: int,
) -> None:
    assert (
        linear_matching_parameter_lower_bound_for_transverse_center(node_count)
        == node_count - 1
    )
    assert (
        linear_matching_parameter_lower_bound_for_post_phase_center(node_count)
        == node_count
    )


def test_input_validation() -> None:
    with pytest.raises(ValueError, match="positive"):
        collective_projector(0)
    with pytest.raises(ValueError, match="node_count entries"):
        collective_projector(3, (1, 2))
    with pytest.raises(ValueError, match="nonzero sum"):
        collective_projector(2, (1, -1))
    with pytest.raises(ValueError, match="nonzero"):
        singular_voltage_matrix(2, 0)
    with pytest.raises(ValueError, match="square"):
        singular_current_jacobian(sp.zeros(2, 3))
    with pytest.raises(ValueError, match="square"):
        positive_epsilon_jacobian(sp.zeros(2, 3), 1)
    with pytest.raises(ValueError, match="positive"):
        no_delay_characteristic_factor(0, 1, 1, 1)
    with pytest.raises(ValueError, match="positive"):
        rescaled_slow_limit_factor(0, 1, 1)
    with pytest.raises(ValueError, match="positive"):
        linear_matching_parameter_lower_bound_for_transverse_center(0)
    with pytest.raises(ValueError, match="positive"):
        linear_matching_parameter_lower_bound_for_post_phase_center(0)
