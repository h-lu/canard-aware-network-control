import sympy as sp

from canard_control.reference_fhn import (
    block_averaging_matrix,
    symmetric_reference_algebra,
)


def test_rank_one_block_averaging_matrix() -> None:
    n_1, n_2 = 2, 3
    matrix = block_averaging_matrix(n_1, n_2)

    assert matrix.shape == (n_1 + n_2, n_1 + n_2)
    assert matrix * sp.ones(n_1 + n_2, 1) == sp.ones(n_1 + n_2, 1)
    assert matrix**2 == matrix
    assert matrix.rank() == 1


def test_reference_modes_and_delay_deformation() -> None:
    result = symmetric_reference_algebra()

    assert result.collective_residual == sp.zeros(5, 1)
    assert result.difference_residual == sp.zeros(5, 1)
    assert result.shifted_moment_derivative == 1


def test_instantaneous_scaffold_has_one_fast_collective_zero() -> None:
    result = symmetric_reference_algebra()
    D = sp.symbols("D", positive=True)
    fast_scaffold = D * (result.averaging_matrix - sp.eye(5))

    assert fast_scaffold * result.collective_mode == sp.zeros(5, 1)
    assert (
        fast_scaffold * result.difference_mode
        + D * result.difference_mode
    ) == sp.zeros(5, 1)
    assert fast_scaffold.rank() == 4


def test_delay_shift_changes_formal_safety_column_when_gain_is_nonzero() -> None:
    result = symmetric_reference_algebra()
    epsilon = sp.symbols("epsilon", positive=True)
    kappa_1 = sp.symbols("kappa_1", real=True)
    shift = sp.symbols("s", real=True)

    derivative = sp.diff(result.formal_threshold, shift)

    assert sp.simplify(
        derivative + kappa_1 * epsilon ** sp.Rational(3, 2) / 8
    ) == 0
