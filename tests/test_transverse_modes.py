import sympy as sp

from canard_control.transverse_modes import (
    leading_fold_mode,
    transverse_mode_blowup,
    two_module_eigenpairs,
)


def test_two_module_collective_and_difference_eigenpairs() -> None:
    matrix, collective, difference, difference_eigenvalue = (
        two_module_eigenpairs()
    )

    assert sp.simplify(matrix * collective - collective) == sp.zeros(2, 1)
    assert sp.simplify(
        matrix * difference - difference_eigenvalue * difference
    ) == sp.zeros(2, 1)


def test_transverse_mode_fold_scaling_is_exact() -> None:
    delta, X, u, u_tau, v, K, lam = sp.symbols(
        "delta X u u_tau v K lambda"
    )
    result = transverse_mode_blowup()

    expected_fast = -2 * X * u + v + delta * (
        -(X**2) * u + K * (u - lam * u_tau)
    )

    assert sp.simplify(result.scaled_fast_rhs - expected_fast) == 0
    assert sp.simplify(result.scaled_slow_rhs + u) == 0


def test_leading_fold_kernel_and_formal_splitting_coefficients() -> None:
    result = leading_fold_mode()
    K, lam, b = sp.symbols("K lambda b", real=True)

    assert result.kernel_residual == sp.zeros(2, 1)
    assert result.adjoint_residual == sp.zeros(2, 1)
    assert result.first_splitting_projection == 0
    assert result.first_range_residual == sp.zeros(2, 1)
    assert result.tangent_correction_residual == sp.zeros(2, 1)
    assert sp.simplify(
        result.second_splitting_projection
        - K * (1 - lam) * (1 + 2 * b) * sp.sqrt(2 * sp.pi) / 4
    ) == 0
