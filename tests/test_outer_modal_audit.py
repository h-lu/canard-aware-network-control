import sympy as sp

from canard_control.outer_modal_audit import outer_modal_audit


def test_physical_recovery_equations_and_slow_delay_are_exact() -> None:
    result = outer_modal_audit()

    assert sp.simplify(
        result.critical_recovery_rhs
        - result.epsilon
        * (result.critical_voltage - result.unfolding)
    ) == 0
    assert sp.simplify(
        result.transverse_recovery_rhs
        - result.epsilon * result.transverse_voltage
        + sp.Symbol("D_w", positive=True) * result.transverse_recovery
    ) == 0
    assert result.slow_time_delay_0 == result.delta * sp.Symbol(
        "theta_0", real=True
    )
    assert result.slow_time_delay_1 == result.delta * sp.Symbol(
        "theta_1", real=True
    )


def test_weak_history_terms_keep_the_physical_epsilon_prefactor() -> None:
    result = outer_modal_audit()
    K = sp.Symbol("K", real=True)
    eta = sp.Symbol("eta", real=True)
    xi, zeta = result.critical_voltage, result.transverse_voltage
    xi_0 = result.delayed_critical_0
    xi_1 = result.delayed_critical_1
    zeta_0 = result.delayed_transverse_0
    zeta_1 = result.delayed_transverse_1

    expected_critical_history = result.epsilon * K * (
        xi - xi_0 / 3 - 2 * xi_1 / 3
        - zeta / 6 + zeta_0 / 12 + zeta_1 / 12
    )
    expected_transverse_history = result.epsilon * K * (
        zeta / 6 - zeta_0 / 12 - zeta_1 / 12
        + eta * (-xi_0 + xi_1 - zeta_0 + zeta_1)
    )

    assert sp.simplify(
        sp.diff(result.critical_voltage_rhs, K) * K
        - expected_critical_history
    ) == 0
    assert sp.simplify(
        sp.diff(result.transverse_voltage_rhs, K) * K
        - expected_transverse_history
    ) == 0


def test_singular_outer_curve_has_the_fold_and_gap_jets() -> None:
    result = outer_modal_audit()
    xi = result.critical_voltage
    alpha = result.alpha

    assert sp.expand(result.singular_transverse_series).coeff(xi, 2) == (
        -alpha / 2
    )
    assert sp.expand(result.singular_transverse_series).coeff(xi, 3) == (
        sp.Rational(7, 16)
    )
    assert sp.expand(result.singular_recovery_series).coeff(xi, 2) == (
        -alpha
    )
    assert sp.expand(result.singular_recovery_series).coeff(xi, 3) == (
        -sp.Rational(11, 24)
    )
    assert sp.expand(result.small_fast_eigenvalue_series).coeff(xi, 1) == (
        -2 * alpha
    )
    assert sp.expand(result.small_fast_eigenvalue_series).coeff(xi, 2) == (
        -sp.Rational(11, 8)
    )
