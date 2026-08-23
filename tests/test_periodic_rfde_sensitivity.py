from __future__ import annotations

import numpy as np
import pytest
import sympy as sp

from canard_control.periodic_rfde_sensitivity import (
    apply_periodic_advanced_adjoint,
    apply_periodic_linearized_operator,
    declared_fhn_periodic_audit,
    normalized_period_and_frequency_derivative,
    reset_landing_sensitivity_audit,
    rotating_wave_sensitivity_audit,
    safety_row_from_simple_gap,
    squared_peak_range_derivative,
)


def test_declared_fhn_periodic_coefficients_are_exact_derivatives() -> None:
    result = declared_fhn_periodic_audit()
    state = (result.current_voltage, result.current_recovery)
    delayed_0 = (result.delayed_voltage_0, sp.Symbol("unused_0"))
    delayed_1 = (result.delayed_voltage_1, sp.Symbol("unused_1"))

    assert result.current_jacobian == result.vector_field.jacobian(state)
    assert sp.simplify(
        result.delayed_jacobian_0[:, 0]
        - result.vector_field.diff(result.delayed_voltage_0)
    ) == sp.zeros(2, 1)
    assert sp.simplify(
        result.delayed_jacobian_1[:, 0]
        - result.vector_field.diff(result.delayed_voltage_1)
    ) == sp.zeros(2, 1)
    assert result.vector_field.jacobian(delayed_0)[:, 1] == sp.zeros(2, 1)
    assert result.vector_field.jacobian(delayed_1)[:, 1] == sp.zeros(2, 1)
    assert sp.simplify(
        result.explicit_linear_gain_field
        - result.vector_field.diff(result.linear_gain)
    ) == sp.zeros(2, 1)
    assert sp.simplify(
        result.explicit_cubic_gain_field
        - result.vector_field.diff(result.cubic_gain)
    ) == sp.zeros(2, 1)
    assert result.explicit_delay_shift_field == sp.zeros(2, 1)


def test_common_scaled_delay_shift_has_the_required_moving_history_sign() -> None:
    result = declared_fhn_periodic_audit()
    epsilon = result.epsilon
    expected_fast = -sp.sqrt(epsilon) / 2 * (
        (
            result.linear_gain
            + 3
            * result.cubic_gain
            * (result.delayed_voltage_0 - 1) ** 2
        )
        * result.delayed_tangent_0
        + (
            result.linear_gain
            + 3
            * result.cubic_gain
            * (result.delayed_voltage_1 - 1) ** 2
        )
        * result.delayed_tangent_1
    )
    assert sp.simplify(
        result.normalized_delay_shift_forcing[0] - expected_fast
    ) == 0
    assert result.normalized_delay_shift_forcing[1] == 0
    assert result.physical_delay_shift_derivative == 1 / sp.sqrt(epsilon)


def test_periodic_retarded_operator_and_advanced_formula_are_transposes() -> None:
    rng = np.random.default_rng(20260823)
    node_count = 19
    dimension = 3
    state = rng.normal(size=(node_count, dimension))
    adjoint = rng.normal(size=(node_count, dimension))
    current = rng.normal(size=(node_count, dimension, dimension))
    delayed = (
        rng.normal(size=(node_count, dimension, dimension)),
        rng.normal(size=(node_count, dimension, dimension)),
    )
    shifts = (3, 7)
    raw_derivative = rng.normal(size=(node_count, node_count))
    derivative = raw_derivative - raw_derivative.T
    period = 2.7

    direct = apply_periodic_linearized_operator(
        state,
        current,
        delayed,
        shifts,
        derivative,
        period,
    )
    advanced = apply_periodic_advanced_adjoint(
        adjoint,
        current,
        delayed,
        shifts,
        derivative,
        period,
    )
    assert np.isclose(np.vdot(adjoint, direct), np.vdot(advanced, state))

    # Replacing A[j+q] by A[j] is wrong for nonconstant coefficients.
    wrong = derivative.T @ adjoint - period * np.einsum(
        "nji,nj->ni", current, adjoint
    )
    for jacobian, shift in zip(delayed, shifts, strict=True):
        wrong -= period * np.einsum(
            "nji,nj->ni",
            jacobian,
            np.roll(adjoint, shift=-shift, axis=0),
        )
    assert abs(np.vdot(adjoint, direct) - np.vdot(wrong, state)) > 1e-3


def test_rotating_wave_period_adjoint_matches_closed_form_with_moving_delay() -> None:
    result = rotating_wave_sensitivity_audit()
    assert np.linalg.norm(result.advanced_adjoint_residual) < 1e-12
    assert np.allclose(
        result.period_adjoint,
        result.exact_period_derivatives,
        rtol=2e-12,
        atol=2e-12,
    )

    sampled_adjoint = np.tile(
        # The rotating-frame adjoint is normalized inside the audit.  Recover
        # any nonzero kernel vector and let the public formula renormalize it.
        np.linalg.svd(result.advanced_adjoint_operator)[2][-1],
        (13, 1),
    )
    period_column = np.tile(result.period_column, (13, 1))
    for index, forcing in enumerate(result.parameter_forcings):
        period_derivative, frequency_derivative = (
            normalized_period_and_frequency_derivative(
                sampled_adjoint,
                period_column,
                np.tile(forcing, (13, 1)),
                result.period,
            )
        )
        assert np.isclose(
            period_derivative,
            result.exact_period_derivatives[index],
            rtol=2e-12,
            atol=2e-12,
        )
        assert np.isclose(
            frequency_derivative,
            result.exact_frequency_derivatives[index],
            rtol=2e-12,
            atol=2e-12,
        )


def test_rotating_wave_peak_amplitude_forward_and_adjoint_rows_agree() -> None:
    result = rotating_wave_sensitivity_audit()
    assert np.linalg.norm(result.forward_equation_residuals) < 3e-12
    assert abs(result.amplitude_adjoint_period_orthogonality) < 1e-12
    assert np.allclose(
        result.forward_squared_amplitude_derivatives,
        result.exact_squared_amplitude_derivatives,
        rtol=2e-12,
        atol=2e-12,
    )
    assert np.allclose(
        result.adjoint_squared_amplitude_derivatives,
        result.exact_squared_amplitude_derivatives,
        rtol=2e-12,
        atol=2e-12,
    )


def test_peak_envelope_formula_is_phase_gauge_invariant_at_extrema() -> None:
    maximum_gradient = np.array([1.0, 2.0])
    minimum_gradient = np.array([-0.5, 1.0])
    maximum_tangent = np.array([2.0, -1.0])
    minimum_tangent = np.array([2.0, 1.0])
    assert maximum_gradient @ maximum_tangent == 0.0
    assert minimum_gradient @ minimum_tangent == 0.0

    maximum_sensitivity = np.array([[0.2, -0.3], [0.4, 0.1]])
    minimum_sensitivity = np.array([[-0.1, 0.2], [0.3, -0.4]])
    baseline = squared_peak_range_derivative(
        3.0,
        -1.0,
        maximum_gradient,
        minimum_gradient,
        maximum_sensitivity,
        minimum_sensitivity,
        maximum_explicit_derivative=np.array([0.1, -0.2]),
        minimum_explicit_derivative=np.array([-0.3, 0.05]),
    )
    phase_offsets = np.array([7.0, -2.0])
    gauged = squared_peak_range_derivative(
        3.0,
        -1.0,
        maximum_gradient,
        minimum_gradient,
        maximum_sensitivity
        + maximum_tangent[:, None] * phase_offsets[None, :],
        minimum_sensitivity
        + minimum_tangent[:, None] * phase_offsets[None, :],
        maximum_explicit_derivative=np.array([0.1, -0.2]),
        minimum_explicit_derivative=np.array([-0.3, 0.05]),
    )
    assert np.allclose(gauged, baseline)


def test_simple_gap_safety_row_matches_an_exact_implicit_root() -> None:
    controls = np.array([0.4, -0.2, 0.3])
    # Gamma(a,u)=a-u0^2-2*u1+sin(u2), so a_c is explicit.
    gap_gradient = np.array(
        [-2.0 * controls[0], -2.0, np.cos(controls[2])]
    )
    operating_gradient = np.array([0.1, 0.0, -0.2])
    row = safety_row_from_simple_gap(
        gap_gradient,
        gap_unfolding_derivative=1.0,
        operating_unfolding_gradient=operating_gradient,
    )

    def safety(value: np.ndarray) -> float:
        a_operating = 1.0 + 0.1 * value[0] - 0.2 * value[2]
        a_canard = value[0] ** 2 + 2.0 * value[1] - np.sin(value[2])
        return float(a_operating - a_canard)

    step = 1e-6
    finite_difference = np.empty(3)
    for index in range(3):
        direction = np.zeros(3)
        direction[index] = step
        finite_difference[index] = (
            safety(controls + direction) - safety(controls - direction)
        ) / (2.0 * step)
    assert np.allclose(row, finite_difference, rtol=1e-9, atol=1e-9)


def test_reset_landing_event_adjoint_includes_history_and_delay_motion() -> None:
    result = reset_landing_sensitivity_audit()
    assert result.maximum_advanced_adjoint_residual < 1e-14
    assert np.isclose(
        result.adjoint_parameter_derivative,
        result.exact_parameter_derivative,
        rtol=2e-12,
        atol=2e-12,
    )
    assert np.isclose(
        result.adjoint_delay_derivative,
        result.exact_delay_derivative,
        rtol=2e-12,
        atol=2e-12,
    )
    # Both derivatives are nonzero, so the test exercises rather than erases
    # the parameter-history and moving-delay contributions.
    assert abs(result.exact_parameter_derivative) > 0.1
    assert abs(result.exact_delay_derivative) > 1e-3


def test_sensitivity_helpers_reject_singular_normalizations() -> None:
    with pytest.raises(ValueError, match="adjoint-orthogonal"):
        normalized_period_and_frequency_derivative(
            np.ones((4, 1)),
            np.zeros((4, 1)),
            np.ones((4, 1)),
            1.0,
        )
    with pytest.raises(ValueError, match="not numerically simple"):
        safety_row_from_simple_gap(np.ones(3), 0.0)
