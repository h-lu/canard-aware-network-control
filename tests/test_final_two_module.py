from __future__ import annotations

import sympy as sp

from canard_control.final_two_module import (
    CharacteristicParameters,
    characteristic_determinant,
    diagnostic_root_branch,
    final_two_module_audit,
)


def test_final_model_equilibrium_and_fold_are_exact() -> None:
    result = final_two_module_audit()

    assert result.fast_equilibrium_residual == sp.zeros(2, 1)
    assert result.recovery_equilibrium_residual == sp.zeros(2, 1)
    assert result.constant_history_feedback_residual == sp.zeros(2, 1)
    assert result.slow_line_residual == sp.zeros(2, 1)
    assert result.fold_curvature == -result.sigma
    assert result.fold_curvature != 0


def test_final_model_critical_and_transverse_projections_are_biorthogonal() -> None:
    result = final_two_module_audit()
    identity = sp.eye(2)

    assert (result.critical_left.T * result.critical_right)[0] == 1
    assert (result.transverse_left.T * result.transverse_right)[0] == 1
    assert (result.critical_left.T * result.transverse_right)[0] == 0
    assert (result.transverse_left.T * result.critical_right)[0] == 0
    assert result.critical_projector**2 == result.critical_projector
    assert result.transverse_projector**2 == result.transverse_projector
    assert (
        result.critical_projector + result.transverse_projector
        == identity
    )
    assert result.fast_jacobian == -2 * result.transverse_projector
    assert result.right_kernel_residual == sp.zeros(2, 1)
    assert result.fast_adjoint_kernel_residual == sp.zeros(1, 2)


def test_final_model_delay_layers_have_the_declared_exact_positivity_range() -> None:
    result = final_two_module_audit()
    eta = result.eta
    lower, upper = result.strict_entrywise_positivity_interval

    assert (lower, upper) == (
        -sp.Rational(1, 6),
        sp.Rational(1, 12),
    )
    assert result.perturbed_layer_0[0, 0] == sp.Rational(1, 6) + eta
    assert result.perturbed_layer_0[1, 0] == sp.Rational(1, 6) - 2 * eta
    assert result.perturbed_layer_1[0, 0] == sp.Rational(1, 3) - eta
    assert result.perturbed_layer_1[1, 0] == sp.Rational(1, 2) + 2 * eta
    assert result.perturbed_layer_0[0, 0].subs(eta, lower) == 0
    assert result.perturbed_layer_0[1, 0].subs(eta, upper) == 0

    radius = result.safe_closed_radius
    assert radius == sp.Rational(1, 20)
    assert result.safe_closed_interval_minimum_entry == sp.Rational(1, 15)
    for endpoint in (-radius, radius):
        assert all(
            entry > 0
            for entry in result.perturbed_layer_0.subs(eta, endpoint)
        )
        assert all(
            entry > 0
            for entry in result.perturbed_layer_1.subs(eta, endpoint)
        )


def test_complete_projected_delay_measure_is_eta_invariant() -> None:
    result = final_two_module_audit()
    expected_pairing = (
        result.history_0 / 3 + 2 * result.history_1 / 3
    )

    assert result.total_gain_residual == sp.zeros(2, 2)
    assert result.total_gain * result.critical_right == result.critical_right
    assert result.projected_layer_weights == (
        sp.Rational(1, 3),
        sp.Rational(2, 3),
    )
    assert result.projected_measure_pairing == expected_pairing
    assert result.projected_measure_eta_derivative == 0
    assert not result.projected_measure_pairing.has(result.eta)


def test_eta_redistribution_produces_the_exact_transverse_history_forcing() -> None:
    result = final_two_module_audit()
    q = result.transverse_right
    eta = result.eta
    x_now = result.history_now
    x_0 = result.history_0
    x_1 = result.history_1

    assert result.redistribution * result.critical_right == q
    assert result.transverse_projector * q == q
    assert sp.simplify(
        result.transverse_measure_pairing - eta * q * (x_0 - x_1)
    ) == sp.zeros(2, 1)
    assert result.source_history_critical_component == (
        x_now - x_0 / 3 - 2 * x_1 / 3
    )
    assert sp.simplify(
        result.source_history_transverse_component
        - eta * q * (x_1 - x_0)
    ) == sp.zeros(2, 1)


def test_recovery_scaffold_leaves_one_length_two_zero_jordan_chain() -> None:
    result = final_two_module_audit()
    z = sp.Symbol("z")
    recovery_gap = sp.Symbol("D_w", positive=True)

    assert result.singular_characteristic == (
        z**2 * (z + 2) * (z + recovery_gap)
    )
    assert result.zero_algebraic_multiplicity == 2
    assert result.kernel_dimension == 1
    assert result.squared_kernel_dimension == 2
    assert result.cubed_kernel_dimension == 2
    assert (
        result.singular_jacobian * result.zero_eigenvector
        == sp.zeros(4, 1)
    )
    assert result.jordan_chain_residual == sp.zeros(4, 1)
    assert result.full_left_kernel_residual == sp.zeros(4, 1)


def test_fixed_parameter_characteristic_root_following_is_reproducible() -> None:
    parameters = CharacteristicParameters()
    eta_values = (-0.02, 0.0, 0.02)
    points = diagnostic_root_branch(eta_values, parameters=parameters)

    assert tuple(point.eta for point in points) == eta_values
    for point in points:
        assert point.determinant_residual < 1e-30
        assert 0.008 < point.root.real < 0.010
        assert 0.214 < point.root.imag < 0.216

    test_value = -0.3 + 0.7j
    determinant = characteristic_determinant(test_value, parameters)
    conjugate_determinant = characteristic_determinant(
        test_value.conjugate(), parameters
    )
    assert abs(conjugate_determinant - determinant.conjugate()) < 1e-35


def test_characteristic_diagnostic_rejects_nonpositive_layer_parameters() -> None:
    invalid = CharacteristicParameters(eta=sp.Rational(1, 12))

    try:
        characteristic_determinant(0.1j, invalid)
    except ValueError as error:
        assert "entrywise positive" in str(error)
    else:
        raise AssertionError("invalid eta should have been rejected")
