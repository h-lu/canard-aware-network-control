"""Periodic-RFDE sensitivity identities and executable sign audits.

The analytic results are stated in ``docs/paper-iv-periodic-rfde-adjoints.md``.
This module has three deliberately limited roles:

* differentiate the declared synchronous FitzHugh--Nagumo RFDE exactly;
* check the retarded/advanced shift transpose on a periodic grid; and
* test period and peak-amplitude adjoints on a manufactured delayed
  Stuart--Landau rotating wave with closed-form sensitivities.

It does not certify a hyperbolic periodic orbit, a physical pulse separator,
or a response-matrix rank for the FitzHugh--Nagumo network.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import numpy as np
import sympy as sp
from scipy.integrate import quad


@dataclass(frozen=True)
class DeclaredFHNPeriodicAudit:
    """Exact coefficient data for the synchronous two-delay FHN reduction."""

    current_voltage: sp.Symbol
    current_recovery: sp.Symbol
    delayed_voltage_0: sp.Symbol
    delayed_voltage_1: sp.Symbol
    delayed_tangent_0: sp.Symbol
    delayed_tangent_1: sp.Symbol
    epsilon: sp.Symbol
    unfolding: sp.Symbol
    linear_gain: sp.Symbol
    cubic_gain: sp.Symbol
    vector_field: sp.Matrix
    current_jacobian: sp.Matrix
    delayed_jacobian_0: sp.Matrix
    delayed_jacobian_1: sp.Matrix
    explicit_linear_gain_field: sp.Matrix
    explicit_cubic_gain_field: sp.Matrix
    explicit_delay_shift_field: sp.Matrix
    physical_delay_shift_derivative: sp.Expr
    normalized_delay_shift_forcing: sp.Matrix
    observable_gradient: sp.Matrix


@dataclass(frozen=True)
class RotatingWaveSensitivityAudit:
    """Closed-form and adjoint responses for a delayed rotating wave."""

    parameter_order: tuple[str, str, str]
    angular_frequency: float
    intrinsic_frequency: float
    coupling: float
    delay: float
    period: float
    radius: float
    implicit_denominator: float
    linearized_rotating_operator: np.ndarray
    advanced_adjoint_operator: np.ndarray
    period_column: np.ndarray
    parameter_forcings: np.ndarray
    period_adjoint: np.ndarray
    exact_period_derivatives: np.ndarray
    exact_frequency_derivatives: np.ndarray
    forward_squared_amplitude_derivatives: np.ndarray
    adjoint_squared_amplitude_derivatives: np.ndarray
    exact_squared_amplitude_derivatives: np.ndarray
    forward_equation_residuals: np.ndarray
    advanced_adjoint_residual: np.ndarray
    amplitude_adjoint_period_orthogonality: float


@dataclass(frozen=True)
class ResetLandingSensitivityAudit:
    """Exact one-step DDE landing derivatives and their event adjoints."""

    explicit_parameter: float
    delay: float
    landing_time: float
    coupling: float
    exact_parameter_derivative: float
    adjoint_parameter_derivative: float
    exact_delay_derivative: float
    adjoint_delay_derivative: float
    maximum_advanced_adjoint_residual: float


def declared_fhn_periodic_audit() -> DeclaredFHNPeriodicAudit:
    r"""Differentiate the exact synchronous RFDE from the reference model.

    The physical delays are
    ``tau_j=(Theta_j^0+s)/sqrt(epsilon)``.  The field has no explicit
    ``s`` dependence at fixed delayed arguments.  Consequently its
    normalized-periodic forcing in the shift direction is entirely the
    moving-delay term

    ``-sum_j tau_{j,s} A_j X'(theta-alpha_j)``.
    """

    voltage, recovery = sp.symbols("V W", real=True)
    delayed_0, delayed_1 = sp.symbols("V_0 V_1", real=True)
    tangent_0, tangent_1 = sp.symbols("Vprime_0 Vprime_1", real=True)
    epsilon = sp.Symbol("epsilon", positive=True)
    unfolding = sp.Symbol("a", real=True)
    linear_gain, cubic_gain = sp.symbols("kappa_1 kappa_3", real=True)

    fast = (
        voltage
        - voltage**3 / 3
        - recovery
        + epsilon
        * linear_gain
        * ((delayed_0 + delayed_1) / 2 - voltage)
        + epsilon
        * cubic_gain
        * (
            ((delayed_0 - 1) ** 3 + (delayed_1 - 1) ** 3) / 2
            - (voltage - 1) ** 3
        )
    )
    slow = epsilon * (voltage - unfolding)
    field = sp.Matrix([fast, slow])

    current_jacobian = sp.simplify(field.jacobian((voltage, recovery)))
    delayed_jacobian_0 = sp.simplify(
        field.jacobian((delayed_0, sp.Symbol("dummy_0")))
    )
    delayed_jacobian_1 = sp.simplify(
        field.jacobian((delayed_1, sp.Symbol("dummy_1")))
    )
    # The dummy delayed-recovery coordinates do not occur in the field.
    explicit_linear = sp.simplify(sp.diff(field, linear_gain))
    explicit_cubic = sp.simplify(sp.diff(field, cubic_gain))
    explicit_shift = sp.zeros(2, 1)
    delay_shift_derivative = 1 / sp.sqrt(epsilon)
    tangent_vectors = (
        sp.Matrix([tangent_0, 0]),
        sp.Matrix([tangent_1, 0]),
    )
    shift_forcing = sp.simplify(
        -delay_shift_derivative
        * (
            delayed_jacobian_0 * tangent_vectors[0]
            + delayed_jacobian_1 * tangent_vectors[1]
        )
    )

    return DeclaredFHNPeriodicAudit(
        current_voltage=voltage,
        current_recovery=recovery,
        delayed_voltage_0=delayed_0,
        delayed_voltage_1=delayed_1,
        delayed_tangent_0=tangent_0,
        delayed_tangent_1=tangent_1,
        epsilon=epsilon,
        unfolding=unfolding,
        linear_gain=linear_gain,
        cubic_gain=cubic_gain,
        vector_field=field,
        current_jacobian=current_jacobian,
        delayed_jacobian_0=delayed_jacobian_0,
        delayed_jacobian_1=delayed_jacobian_1,
        explicit_linear_gain_field=explicit_linear,
        explicit_cubic_gain_field=explicit_cubic,
        explicit_delay_shift_field=explicit_shift,
        physical_delay_shift_derivative=delay_shift_derivative,
        normalized_delay_shift_forcing=shift_forcing,
        observable_gradient=sp.Matrix([[1, 0]]),
    )


def _validated_periodic_arrays(
    state: np.ndarray,
    current_jacobian: np.ndarray,
    delayed_jacobians: Sequence[np.ndarray],
    shifts: Sequence[int],
    derivative_matrix: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, tuple[np.ndarray, ...], tuple[int, ...], np.ndarray]:
    values = np.asarray(state, dtype=float)
    current = np.asarray(current_jacobian, dtype=float)
    derivative = np.asarray(derivative_matrix, dtype=float)
    delays = tuple(np.asarray(item, dtype=float) for item in delayed_jacobians)
    integer_shifts = tuple(int(item) for item in shifts)
    if values.ndim != 2:
        raise ValueError("state must have shape (nodes, dimension)")
    node_count, dimension = values.shape
    if current.shape != (node_count, dimension, dimension):
        raise ValueError("current_jacobian has incompatible shape")
    if derivative.shape != (node_count, node_count):
        raise ValueError("derivative_matrix has incompatible shape")
    if len(delays) != len(integer_shifts):
        raise ValueError("one integer shift is required per delayed Jacobian")
    if any(item.shape != current.shape for item in delays):
        raise ValueError("delayed Jacobians must match current_jacobian")
    if not all(
        np.all(np.isfinite(item))
        for item in (values, current, derivative, *delays)
    ):
        raise ValueError("all periodic arrays must be finite")
    return values, current, delays, integer_shifts, derivative


def apply_periodic_linearized_operator(
    state: np.ndarray,
    current_jacobian: np.ndarray,
    delayed_jacobians: Sequence[np.ndarray],
    shifts: Sequence[int],
    derivative_matrix: np.ndarray,
    period: float,
) -> np.ndarray:
    r"""Apply the grid analogue of ``y'-T A0 y-T sum Ak S_alpha y``.

    ``shifts[k]=q`` means the retarded value at grid index ``j`` is
    ``state[j-q]`` with periodic indexing.
    """

    values, current, delays, integer_shifts, derivative = _validated_periodic_arrays(
        state,
        current_jacobian,
        delayed_jacobians,
        shifts,
        derivative_matrix,
    )
    period_value = float(period)
    if not np.isfinite(period_value) or period_value <= 0:
        raise ValueError("period must be finite and positive")
    result = derivative @ values - period_value * np.einsum(
        "nij,nj->ni", current, values
    )
    for jacobian, shift in zip(delays, integer_shifts, strict=True):
        retarded = np.roll(values, shift=shift, axis=0)
        result -= period_value * np.einsum(
            "nij,nj->ni", jacobian, retarded
        )
    return result


def apply_periodic_advanced_adjoint(
    adjoint: np.ndarray,
    current_jacobian: np.ndarray,
    delayed_jacobians: Sequence[np.ndarray],
    shifts: Sequence[int],
    derivative_matrix: np.ndarray,
    period: float,
) -> np.ndarray:
    r"""Apply the exact Euclidean transpose of the periodic grid operator.

    A retarded term ``A_k[j] y[j-q]`` becomes the advanced term
    ``A_k[j+q].T z[j+q]``.  The derivative action is the matrix transpose,
    so this function also works for nonskew differentiation matrices.
    """

    values, current, delays, integer_shifts, derivative = _validated_periodic_arrays(
        adjoint,
        current_jacobian,
        delayed_jacobians,
        shifts,
        derivative_matrix,
    )
    period_value = float(period)
    if not np.isfinite(period_value) or period_value <= 0:
        raise ValueError("period must be finite and positive")
    result = derivative.T @ values - period_value * np.einsum(
        "nji,nj->ni", current, values
    )
    for jacobian, shift in zip(delays, integer_shifts, strict=True):
        advanced_values = np.roll(values, shift=-shift, axis=0)
        advanced_jacobian = np.roll(jacobian, shift=-shift, axis=0)
        result -= period_value * np.einsum(
            "nji,nj->ni", advanced_jacobian, advanced_values
        )
    return result


def normalized_period_and_frequency_derivative(
    adjoint: np.ndarray,
    period_column: np.ndarray,
    parameter_forcing: np.ndarray,
    period: float,
) -> tuple[float, float]:
    r"""Return ``(T_p,F_p)`` from the normalized periodic adjoint formula.

    Arrays are sampled on a uniform periodic grid, so their integral pairing
    is the sample mean.  No normalization of the supplied adjoint is assumed.
    """

    covector = np.asarray(adjoint, dtype=float)
    column = np.asarray(period_column, dtype=float)
    forcing = np.asarray(parameter_forcing, dtype=float)
    if not (covector.shape == column.shape == forcing.shape):
        raise ValueError("adjoint, period column, and forcing must have equal shape")
    if covector.ndim != 2 or not all(
        np.all(np.isfinite(item)) for item in (covector, column, forcing)
    ):
        raise ValueError("periodic data must be finite two-dimensional arrays")
    period_value = float(period)
    if not np.isfinite(period_value) or period_value <= 0:
        raise ValueError("period must be finite and positive")
    denominator = float(np.mean(np.einsum("ni,ni->n", covector, column)))
    numerator = float(np.mean(np.einsum("ni,ni->n", covector, forcing)))
    if abs(denominator) <= 100 * np.finfo(float).eps:
        raise ValueError("period column is adjoint-orthogonal")
    period_derivative = -numerator / denominator
    frequency_derivative = -period_derivative / period_value**2
    return float(period_derivative), float(frequency_derivative)


def squared_peak_range_derivative(
    maximum_value: float,
    minimum_value: float,
    maximum_state_gradient: np.ndarray,
    minimum_state_gradient: np.ndarray,
    maximum_state_sensitivity: np.ndarray,
    minimum_state_sensitivity: np.ndarray,
    maximum_explicit_derivative: np.ndarray | float = 0.0,
    minimum_explicit_derivative: np.ndarray | float = 0.0,
) -> np.ndarray:
    """Apply the envelope formula for a squared unique peak-to-peak range."""

    maximum_gradient = np.asarray(maximum_state_gradient, dtype=float).reshape(-1)
    minimum_gradient = np.asarray(minimum_state_gradient, dtype=float).reshape(-1)
    maximum_sensitivity = np.asarray(maximum_state_sensitivity, dtype=float)
    minimum_sensitivity = np.asarray(minimum_state_sensitivity, dtype=float)
    if maximum_sensitivity.ndim == 1:
        maximum_sensitivity = maximum_sensitivity[:, None]
    if minimum_sensitivity.ndim == 1:
        minimum_sensitivity = minimum_sensitivity[:, None]
    if not (
        maximum_gradient.shape == minimum_gradient.shape
        and maximum_sensitivity.shape == minimum_sensitivity.shape
        and maximum_sensitivity.shape[0] == maximum_gradient.size
    ):
        raise ValueError("peak gradients and state sensitivities are incompatible")
    actuator_count = maximum_sensitivity.shape[1]
    explicit_maximum = np.broadcast_to(
        np.asarray(maximum_explicit_derivative, dtype=float),
        (actuator_count,),
    )
    explicit_minimum = np.broadcast_to(
        np.asarray(minimum_explicit_derivative, dtype=float),
        (actuator_count,),
    )
    if not all(
        np.all(np.isfinite(item))
        for item in (
            maximum_gradient,
            minimum_gradient,
            maximum_sensitivity,
            minimum_sensitivity,
            explicit_maximum,
            explicit_minimum,
        )
    ):
        raise ValueError("peak derivative data must be finite")
    range_value = float(maximum_value) - float(minimum_value)
    range_derivative = (
        maximum_gradient @ maximum_sensitivity
        - minimum_gradient @ minimum_sensitivity
        + explicit_maximum
        - explicit_minimum
    )
    return 2.0 * range_value * np.asarray(range_derivative, dtype=float)


def safety_row_from_simple_gap(
    gap_actuator_gradient: np.ndarray,
    gap_unfolding_derivative: float,
    operating_unfolding_gradient: np.ndarray | None = None,
) -> np.ndarray:
    r"""Differentiate ``S=a_op-a_c(u)`` when ``Gamma(a_c(u),u)=0``.

    The exact row is ``D a_op + Gamma_u/Gamma_a``.  This function checks
    only the scalar simple-root algebra; it does not construct ``Gamma``.
    """

    gradient = np.asarray(gap_actuator_gradient, dtype=float).reshape(-1)
    slope = float(gap_unfolding_derivative)
    if not np.all(np.isfinite(gradient)) or not np.isfinite(slope):
        raise ValueError("gap derivatives must be finite")
    if abs(slope) <= 100 * np.finfo(float).eps:
        raise ValueError("gap root is not numerically simple")
    if operating_unfolding_gradient is None:
        operating = np.zeros_like(gradient)
    else:
        operating = np.asarray(
            operating_unfolding_gradient, dtype=float
        ).reshape(-1)
        if operating.shape != gradient.shape or not np.all(np.isfinite(operating)):
            raise ValueError("operating gradient is incompatible")
    return operating + gradient / slope


def rotating_wave_sensitivity_audit(
    angular_frequency: float = 1.3,
    coupling: float = 0.2,
    delay: float = 0.7,
) -> RotatingWaveSensitivityAudit:
    r"""Audit all sensitivity signs on a delayed Stuart--Landau wave.

    For

    ``z_dot=(1-|z|^2)z+i*omega*z+K*(z(t-tau)-z(t))``

    choose ``omega=Omega+K*sin(Omega*tau)``.  Then
    ``z(t)=r exp(i Omega t)`` with
    ``r^2=1+K*(cos(Omega*tau)-1)``.  The implicit response is available in
    closed form, while the normalized periodic linearization contains a
    genuine retarded rotation and its adjoint contains the advanced
    rotation.  This is a regression model, not the FHN periodic orbit.
    """

    omega_value = float(angular_frequency)
    coupling_value = float(coupling)
    delay_value = float(delay)
    values = np.asarray((omega_value, coupling_value, delay_value), dtype=float)
    if not np.all(np.isfinite(values)) or omega_value <= 0 or delay_value <= 0:
        raise ValueError("frequency and delay must be positive finite values")
    phase = omega_value * delay_value
    radius_squared = 1.0 + coupling_value * (np.cos(phase) - 1.0)
    denominator = 1.0 + coupling_value * delay_value * np.cos(phase)
    if radius_squared <= 0 or abs(denominator) <= 1e-10:
        raise ValueError("rotating wave or its implicit frequency derivative is singular")

    radius = float(np.sqrt(radius_squared))
    intrinsic_frequency = float(omega_value + coupling_value * np.sin(phase))
    period = float(2.0 * np.pi / omega_value)
    rotation_generator = np.array([[0.0, -1.0], [1.0, 0.0]])

    def rotation(angle: float) -> np.ndarray:
        return np.array(
            [
                [np.cos(angle), -np.sin(angle)],
                [np.sin(angle), np.cos(angle)],
            ]
        )

    radial_projector = np.array([[1.0, 0.0], [0.0, 0.0]])
    rotating_current_jacobian = (
        (1.0 - radius_squared - coupling_value) * np.eye(2)
        - 2.0 * radius_squared * radial_projector
        + intrinsic_frequency * rotation_generator
    )
    linearized = (
        2.0 * np.pi * rotation_generator
        - period * rotating_current_jacobian
        - period * coupling_value * rotation(-phase)
    )
    advanced_adjoint = (
        -2.0 * np.pi * rotation_generator
        - period * rotating_current_jacobian.T
        - period * coupling_value * rotation(phase)
    )

    radial = np.array([1.0, 0.0])
    tangent = np.array([0.0, 1.0])
    period_column = radius * (
        omega_value * tangent
        + coupling_value * phase * (rotation(-phase) @ tangent)
    )
    forcings = np.vstack(
        (
            period * radius * tangent,
            period * radius * (rotation(-phase) @ radial - radial),
            -coupling_value
            * 2.0
            * np.pi
            * radius
            * (rotation(-phase) @ tangent),
        )
    )

    _, _, right_singular_vectors = np.linalg.svd(advanced_adjoint)
    period_adjoint_vector = right_singular_vectors[-1]
    period_adjoint_vector /= period_adjoint_vector @ period_column
    period_adjoint = -forcings @ period_adjoint_vector

    angular_derivatives = np.array(
        (
            1.0 / denominator,
            -np.sin(phase) / denominator,
            -coupling_value * omega_value * np.cos(phase) / denominator,
        )
    )
    exact_period = -2.0 * np.pi * angular_derivatives / omega_value**2
    exact_frequency = angular_derivatives / (2.0 * np.pi)

    radius_squared_derivatives = np.array(
        (
            -coupling_value * np.sin(phase) * delay_value * angular_derivatives[0],
            np.cos(phase)
            - 1.0
            - coupling_value
            * np.sin(phase)
            * delay_value
            * angular_derivatives[1],
            -coupling_value
            * np.sin(phase)
            * (omega_value + delay_value * angular_derivatives[2]),
        )
    )
    radius_derivatives = radius_squared_derivatives / (2.0 * radius)
    exact_squared_amplitude = 4.0 * radius_squared_derivatives

    phase_row = tangent.reshape(1, 2)
    augmented = np.block(
        [
            [linearized, -period_column[:, None]],
            [phase_row, np.zeros((1, 1))],
        ]
    )
    forward_squared_amplitude = np.empty(3)
    forward_residuals = np.empty((3, 2))
    output_row = 8.0 * radius * radial
    for index, forcing in enumerate(forcings):
        solution = np.linalg.solve(augmented, np.r_[forcing, 0.0])
        forward_squared_amplitude[index] = output_row @ solution[:2]
        expected_state = radius_derivatives[index] * radial
        forward_residuals[index] = (
            linearized @ expected_state
            - period_column * exact_period[index]
            - forcing
        )

    amplitude_dual = np.linalg.solve(augmented.T, np.r_[output_row, 0.0])
    amplitude_adjoint = forcings @ amplitude_dual[:2]

    return RotatingWaveSensitivityAudit(
        parameter_order=("omega", "coupling", "delay"),
        angular_frequency=omega_value,
        intrinsic_frequency=intrinsic_frequency,
        coupling=coupling_value,
        delay=delay_value,
        period=period,
        radius=radius,
        implicit_denominator=float(denominator),
        linearized_rotating_operator=linearized,
        advanced_adjoint_operator=advanced_adjoint,
        period_column=period_column,
        parameter_forcings=forcings,
        period_adjoint=period_adjoint,
        exact_period_derivatives=exact_period,
        exact_frequency_derivatives=exact_frequency,
        forward_squared_amplitude_derivatives=forward_squared_amplitude,
        adjoint_squared_amplitude_derivatives=amplitude_adjoint,
        exact_squared_amplitude_derivatives=exact_squared_amplitude,
        forward_equation_residuals=forward_residuals,
        advanced_adjoint_residual=advanced_adjoint @ period_adjoint_vector,
        amplitude_adjoint_period_orthogonality=float(
            amplitude_dual[:2] @ period_column
        ),
    )


def reset_landing_sensitivity_audit(
    explicit_parameter: float = 0.3,
    delay: float = 0.8,
    landing_time: float = 1.3,
    coupling: float = 0.4,
    history_level: float = 0.7,
    history_parameter_level: float = 0.2,
    history_parameter_slope: float = -0.15,
) -> ResetLandingSensitivityAudit:
    """Check the finite-horizon event adjoint on a one-step linear DDE.

    A clock variable makes ``t=landing_time`` a transverse autonomous event.
    The landing coordinate solves

    ``y'=p+k*y(t-tau)``,
    ``y(s)=c+p*(h0+h1*s)`` for ``s <= 0``.

    The restriction ``tau < landing_time < 2*tau`` gives a closed-form
    method-of-steps solution and a nonconstant advanced adjoint.  Both the
    parameter-dependent history term and the moving-delay term are active.
    """

    parameter = float(explicit_parameter)
    tau = float(delay)
    final_time = float(landing_time)
    gain = float(coupling)
    level = float(history_level)
    history_level_derivative = float(history_parameter_level)
    history_slope_derivative = float(history_parameter_slope)
    values = np.asarray(
        (
            parameter,
            tau,
            final_time,
            gain,
            level,
            history_level_derivative,
            history_slope_derivative,
        )
    )
    if not np.all(np.isfinite(values)):
        raise ValueError("reset landing parameters must be finite")
    if not 0.0 < tau < final_time < 2.0 * tau:
        raise ValueError("the audit requires delay < landing_time < 2*delay")

    def history(time: float, parameter_value: float) -> float:
        return level + parameter_value * (
            history_level_derivative + history_slope_derivative * time
        )

    def landing_adjoint(time: float) -> float:
        switch = final_time - tau
        if time >= switch:
            return 1.0
        return 1.0 + gain * (switch - time)

    def delayed_time_derivative(time: float) -> float:
        if time < 0.0:
            return parameter * history_slope_derivative
        return parameter + gain * history(time - tau, parameter)

    parameter_history_term = landing_adjoint(0.0) * history_level_derivative
    parameter_explicit_term = quad(
        landing_adjoint,
        0.0,
        final_time,
        epsabs=2e-14,
        points=(final_time - tau,),
    )[0]
    parameter_delayed_history_term = gain * quad(
        lambda time: landing_adjoint(time + tau)
        * (history_level_derivative + history_slope_derivative * time),
        -tau,
        0.0,
        epsabs=2e-14,
        points=(final_time - 2.0 * tau,),
    )[0]
    adjoint_parameter = (
        parameter_history_term
        + parameter_explicit_term
        + parameter_delayed_history_term
    )
    adjoint_delay = -gain * quad(
        lambda time: landing_adjoint(time)
        * delayed_time_derivative(time - tau),
        0.0,
        final_time,
        epsabs=2e-14,
        points=(tau, final_time - tau),
    )[0]

    parameter_symbol, delay_symbol = sp.symbols("p tau", real=True)
    remainder_symbol = sp.Float(final_time) - delay_symbol
    first_at_delay = (
        sp.Float(level)
        + parameter_symbol * sp.Float(history_level_derivative)
        + parameter_symbol * delay_symbol
        + sp.Float(gain)
        * (
            (
                sp.Float(level)
                + parameter_symbol * sp.Float(history_level_derivative)
                - parameter_symbol
                * sp.Float(history_slope_derivative)
                * delay_symbol
            )
            * delay_symbol
            + parameter_symbol
            * sp.Float(history_slope_derivative)
            * delay_symbol**2
            / 2
        )
    )
    first_step_integral = (
        sp.Float(level) * remainder_symbol
        + parameter_symbol
        * sp.Float(history_level_derivative)
        * remainder_symbol
        + parameter_symbol * remainder_symbol**2 / 2
        + sp.Float(gain)
        * (
            (
                sp.Float(level)
                + parameter_symbol * sp.Float(history_level_derivative)
                - parameter_symbol
                * sp.Float(history_slope_derivative)
                * delay_symbol
            )
            * remainder_symbol**2
            / 2
            + parameter_symbol
            * sp.Float(history_slope_derivative)
            * remainder_symbol**3
            / 6
        )
    )
    landing_expression = (
        first_at_delay
        + parameter_symbol * remainder_symbol
        + sp.Float(gain) * first_step_integral
    )
    substitution = {parameter_symbol: parameter, delay_symbol: tau}
    exact_parameter = float(
        sp.diff(landing_expression, parameter_symbol).subs(substitution)
    )
    exact_delay = float(
        sp.diff(landing_expression, delay_symbol).subs(substitution)
    )

    sample = np.linspace(0.0, final_time - tau, 31)
    advanced_residual = np.max(
        np.abs(
            gain
            - gain
            * np.asarray([landing_adjoint(time + tau) for time in sample])
        )
    )

    return ResetLandingSensitivityAudit(
        explicit_parameter=parameter,
        delay=tau,
        landing_time=final_time,
        coupling=gain,
        exact_parameter_derivative=float(exact_parameter),
        adjoint_parameter_derivative=float(adjoint_parameter),
        exact_delay_derivative=float(exact_delay),
        adjoint_delay_derivative=float(adjoint_delay),
        maximum_advanced_adjoint_residual=float(advanced_residual),
    )
