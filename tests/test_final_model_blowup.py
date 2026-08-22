import sympy as sp

from canard_control.final_model_blowup import final_model_blowup


def test_modal_matrices_separate_projected_and_transverse_delay_data() -> None:
    result = final_model_blowup()
    eta = result.eta

    assert result.layer_0_modal == sp.Matrix(
        [
            [sp.Rational(1, 3), -sp.Rational(1, 12)],
            [eta, sp.Rational(1, 12) + eta],
        ]
    )
    assert result.layer_1_modal == sp.Matrix(
        [
            [sp.Rational(2, 3), -sp.Rational(1, 12)],
            [-eta, sp.Rational(1, 12) - eta],
        ]
    )
    assert result.total_gain_modal == sp.Matrix(
        [[1, -sp.Rational(1, 6)], [0, sp.Rational(1, 6)]]
    )
    assert result.redistribution_modal == sp.Matrix([[0, 0], [1, 1]])


def test_fixed_recovery_scaffold_leaves_one_collective_jordan_chain() -> None:
    result = final_model_blowup()
    spectral_parameter = sp.Symbol("lambda")

    assert result.singular_characteristic == (
        spectral_parameter**2
        * (spectral_parameter + 2)
        * (spectral_parameter + result.recovery_gap)
    )
    assert len(result.singular_jacobian.nullspace()) == 1
    assert len((result.singular_jacobian**2).nullspace()) == 2


def test_raw_blowup_has_anisotropic_recovery_scaling() -> None:
    result = final_model_blowup()

    assert result.critical_voltage_scale == result.delta
    assert result.transverse_voltage_scale == result.delta**2
    assert result.critical_recovery_scale == -result.delta**2
    assert result.transverse_recovery_scale == result.delta**4
    assert result.scaled_parameter == (
        result.delta**2 * sp.Symbol("nu", real=True)
    )
    assert result.displayed_transverse_recovery_rhs == (
        sp.Symbol("Z", real=True)
        - result.recovery_gap * sp.Symbol("W", real=True)
    )


def test_displayed_chart_is_the_exact_transform_of_physical_model_m() -> None:
    result = final_model_blowup()

    # These residuals compare the displayed chart with the independently
    # constructed physical FHN field, delay layers, and recovery scaffold.
    assert result.critical_residual == 0
    assert result.transverse_residual == 0
    assert result.collective_recovery_residual == 0
    assert result.transverse_recovery_residual == 0
    assert result.fast_reconstruction_residual == sp.zeros(2, 1)
    assert result.slow_reconstruction_residual == sp.zeros(2, 1)


def test_delta_zero_constraints_give_the_unique_transverse_graph() -> None:
    result = final_model_blowup()
    X = sp.Symbol("X", real=True)

    assert result.leading_graph_z == -result.alpha * X**2 / 2
    assert result.leading_graph_w == (
        -result.alpha * X**2 / (2 * result.recovery_gap)
    )


def test_formal_eta_channel_has_the_audited_order_coefficient_and_sign() -> None:
    result = final_model_blowup()
    expected_delay_gap = (
        result.theta_0 - result.theta_1
    ) / (2 * result.alpha)
    expected_z_coefficient = (
        -result.weak_gain
        * (result.theta_0 - result.theta_1)
        / (4 * result.alpha)
    )
    expected_nu_coefficient = (
        result.weak_gain
        * (result.theta_0 - result.theta_1)
        / (4 * result.alpha)
    )

    assert result.delay_translation_difference == expected_delay_gap
    assert sp.simplify(
        result.eta_order_transverse_forcing
        + result.weak_gain * expected_delay_gap
    ) == 0
    assert result.leading_transverse_linearization == -2
    assert sp.simplify(
        result.eta_transverse_coefficient - expected_z_coefficient
    ) == 0
    assert sp.simplify(
        result.formal_nu_coefficient - expected_nu_coefficient
    ) == 0
    assert sp.simplify(
        result.formal_mu_derivative
        - result.delta**3 * expected_nu_coefficient
    ) == 0
    assert sp.simplify(1 / (4 * result.alpha)) == 1 / sp.sqrt(6)
    assert not result.formal_mu_derivative.has(result.recovery_gap)

    signed_value = result.formal_mu_derivative.subs(
        {
            result.weak_gain: 1,
            result.theta_0: 1,
            result.theta_1: 2,
            result.delta: sp.Rational(1, 10),
        }
    )
    assert signed_value < 0
