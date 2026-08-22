import sympy as sp

from canard_control.two_module_moment import two_module_moment_audit


def test_fhn_core_has_one_non_degenerate_critical_mode() -> None:
    result = two_module_moment_audit()

    assert result.fast_jacobian == sp.Matrix(
        [[-1, sp.Rational(1, 2)], [2, -1]]
    )
    assert result.fast_kernel_residual == sp.zeros(2, 1)
    assert result.adjoint_kernel_residual == sp.zeros(1, 2)
    assert (
        result.critical_left.T * result.critical_right
    )[0] == 1
    assert result.fast_jacobian == -2 * result.transverse_projector
    assert result.fold_nondegeneracy == -result.sigma


def test_original_two_recovery_counterexample_has_an_extra_slow_center() -> None:
    result = two_module_moment_audit()
    spectral_parameter = sp.symbols("z")
    jacobian = result.full_singular_jacobian

    assert sp.factor(jacobian.charpoly(spectral_parameter).as_expr()) == (
        spectral_parameter**3 * (spectral_parameter + 2)
    )
    assert 4 - jacobian.rank() == 2
    assert 4 - (jacobian**2).rank() == 3


def test_delay_redistribution_keeps_total_gain_and_projected_layers() -> None:
    result = two_module_moment_audit()

    assert result.total_gain_residual == sp.zeros(2, 2)
    assert result.total_gain * result.critical_right == result.critical_right
    assert result.layer_0_mode_residual == sp.zeros(2, 1)
    assert result.layer_1_mode_residual == sp.zeros(2, 1)
    assert result.projected_layer_0_weight == sp.Rational(1, 3)
    assert result.projected_layer_1_weight == sp.Rational(2, 3)


def test_same_projected_first_moment_can_hide_transverse_forcing() -> None:
    result = two_module_moment_audit()
    eta, theta_0, theta_1 = sp.symbols(
        "eta theta_0 theta_1", real=True
    )

    expected_moment = theta_0 / 3 + 2 * theta_1 / 3
    expected_transverse = (
        eta * (theta_0 - theta_1) * result.transverse_vector
    )

    assert result.projected_first_moment == expected_moment
    assert sp.simplify(
        result.transverse_first_moment - expected_transverse
    ) == sp.zeros(2, 1)
    assert not result.projected_first_moment.has(eta)


def test_transverse_response_returns_to_critical_solvability() -> None:
    result = two_module_moment_audit()

    assert (
        result.fast_jacobian * result.transverse_fast_response
        == result.transverse_vector
    )
    assert result.nonlinear_return_coefficient == result.sigma / 2


def test_delay_layers_are_positive_on_declared_eta_interval() -> None:
    result = two_module_moment_audit()
    eta = sp.symbols("eta", real=True)

    # Every entry is affine in eta, so positivity at both closed endpoints
    # proves positivity throughout the declared open interval.
    for value in (sp.Rational(-1, 20), sp.Rational(1, 20)):
        layer_0 = result.perturbed_layer_0.subs(eta, value)
        layer_1 = result.perturbed_layer_1.subs(eta, value)
        assert all(entry > 0 for entry in layer_0)
        assert all(entry > 0 for entry in layer_1)
