import sympy as sp

from canard_control.nonlocal_graph_jet import nonlocal_graph_jet_audit


def test_shift_removes_the_singular_algebraic_graph_exactly() -> None:
    result = nonlocal_graph_jet_audit()

    assert result.center_divisibility_residual == 0
    assert result.stable_divisibility_residual == sp.zeros(2, 1)
    # A successful Poly construction rules out negative powers of delta in
    # the certified quotients.  This prevents a divide-and-multiply-back test
    # from passing tautologically.
    sp.Poly(result.center_remainder, result.delta, domain="EX")
    for component in result.stable_remainder:
        sp.Poly(component, result.delta, domain="EX")
    assert result.shifted_critical_rhs.subs(
        {
            result.delta: 0,
            result.shifted_voltage: 0,
            result.shifted_recovery: 0,
        }
    ) == result.chart_y - result.alpha * result.chart_x**2


def test_shifted_transverse_block_is_uniformly_hurwitz() -> None:
    result = nonlocal_graph_jet_audit()
    spectral_parameter = sp.Symbol("lambda")

    assert result.stable_matrix == sp.Matrix(
        [[-2, 0], [1, -result.recovery_gap]]
    )
    assert result.stable_characteristic == (
        (spectral_parameter + 2)
        * (spectral_parameter + result.recovery_gap)
    )


def test_first_center_and_stable_coefficients_have_audited_signs() -> None:
    result = nonlocal_graph_jet_audit()
    X = result.chart_x
    Y = result.chart_y
    U = result.shifted_voltage
    V = result.shifted_recovery
    X_0 = sp.Symbol("X_theta_0", real=True)
    X_1 = sp.Symbol("X_theta_1", real=True)
    U_0 = sp.Symbol("U_theta_0", real=True)
    U_1 = sp.Symbol("U_theta_1", real=True)
    zero_stable = {U: 0, V: 0, U_0: 0, U_1: 0}

    q_1_x = sp.simplify(
        result.center_remainder.subs(
            {result.delta: 0, **zero_stable}
        )
    )
    expected_q_1_x = (
        result.weak_gain * (X - X_0 / 3 - 2 * X_1 / 3)
        - sp.Rational(11, 9) * result.alpha**2 * X**3
    )
    assert sp.simplify(q_1_x - expected_q_1_x) == 0

    g_0 = sp.simplify(
        result.stable_remainder.subs(
            {result.delta: 0, **zero_stable}
        )
    )
    expected_g_0 = sp.Matrix(
        [
            result.alpha * X * Y
            + sp.Rational(4, 3) * result.alpha**2 * X**3
            - result.weak_gain * result.eta * (X_0 - X_1),
            result.alpha
            * X
            * (Y - result.alpha * X**2)
            / result.recovery_gap,
        ]
    )
    assert sp.simplify(g_0 - expected_g_0) == sp.zeros(2, 1)


def test_eta_graph_jet_solves_the_exact_stable_range_equation() -> None:
    result = nonlocal_graph_jet_audit()
    X_0 = sp.Symbol("X_theta_0", real=True)
    X_1 = sp.Symbol("X_theta_1", real=True)
    delay_gap = X_0 - X_1

    assert sp.simplify(
        result.eta_stable_forcing
        - sp.Matrix([-result.weak_gain * delay_gap, 0])
    ) == sp.zeros(2, 1)
    assert sp.simplify(
        result.eta_first_graph_jet
        - sp.Matrix(
            [
                -result.weak_gain * delay_gap / 2,
                -result.weak_gain
                * delay_gap
                / (2 * result.recovery_gap),
            ]
        )
    ) == sp.zeros(2, 1)
    assert result.eta_first_graph_residual == sp.zeros(2, 1)


def test_eta_graph_return_recovers_the_formal_physical_coefficient() -> None:
    result = nonlocal_graph_jet_audit()
    expected = (
        result.weak_gain
        * (sp.Symbol("theta_0", real=True) - sp.Symbol("theta_1", real=True))
        / (4 * result.alpha)
    )

    assert sp.simplify(result.formal_nu_derivative - expected) == 0
    assert sp.simplify(
        result.formal_mu_derivative - result.delta**3 * expected
    ) == 0
    assert not result.formal_mu_derivative.has(result.recovery_gap)
