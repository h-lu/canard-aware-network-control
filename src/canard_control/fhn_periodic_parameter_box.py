"""Directed parameter-box continuation and response audit for FHN.

This module deliberately reuses the coefficient space, real-conjugate
layout, and finite/tail preconditioner of
``fhn_periodic_infinite_validation``.  The new ingredient is that the two
gain parameters are intervals.  The same center Fourier polynomial and one
midpoint inverse are used for every parameter in the box.

Only MPFR-directed endpoints enter a proved flag.  NumPy is used to build a
binary64 midpoint inverse and center sensitivity candidates; every use of
those stored numbers is followed by the directed Higham error bounds already
used by the center certificate.
"""

from __future__ import annotations

import ctypes
from dataclasses import dataclass
from typing import Mapping

import gmpy2
import numpy as np

from canard_control.directed_interval import (
    DirectedComplexInterval,
    DirectedInterval,
    decimal_lower,
    decimal_upper,
    pi_interval,
    upward_division,
    upward_sum,
)
from canard_control.fhn_periodic_candidate import (
    PeriodicOrbitCandidate,
    _collocation_system,
    _field_data,
    odd_fourier_matrices,
    periodic_response_candidate,
)
from canard_control.fhn_periodic_directed_validation import (
    ComplexSequence,
    _binary_product_defect_upper,
    _complex_zero,
    _constant_sequence,
    _interval_parameters,
    _one,
    _sequence_add,
    _sequence_convolution,
    _sequence_derivative,
    _sequence_scale,
    _sequence_shift,
    _sequence_sub,
    directed_dft,
)
from canard_control.fhn_periodic_infinite_validation import (
    _BaseSequences,
    _RealConjugateLayout,
    _binary_matvec_l1_upper,
    _box_abs_upper,
    _finite_coefficient_matrix,
    _finite_from_tail_upper,
    _float_matrix_l1_upper,
    _nonlinear_coefficients,
    _residual_vector,
    _scaled_real_coordinate_intervals,
    _sequence_box_norm_upper,
    _sequence_neg,
    _tail_from_finite_upper,
    _tail_residual_upper,
    _tail_to_tail_upper,
)


@dataclass(frozen=True)
class DirectedGainBox:
    """Human-declared decimal gain box."""

    kappa_1_lower: str
    kappa_1_upper: str
    kappa_3_lower: str
    kappa_3_upper: str
    half_width: str


@dataclass(frozen=True)
class DirectedBoxContinuation:
    """Uniform radii certificate for one phase-fixed periodic branch."""

    cutoff: int
    precision_bits: int
    real_conjugate_dimension: int
    residual_support_half_bandwidth: int
    approximate_inverse_l1_upper: str
    analytic_tail_inverse_l1_upper: str
    global_preconditioner_l1_upper: str
    finite_inverse_defect_upper: str
    finite_to_finite_upper: str
    tail_from_finite_upper: str
    finite_from_tail_upper: str
    tail_to_tail_upper: str
    full_point_defect_upper: str
    preconditioned_box_residual_upper: str
    coefficient_z1_upper: str
    coefficient_z2_upper: str
    coefficient_z3_upper: str
    chosen_radius: str
    derivative_variation_upper: str
    uniform_contraction_upper: str
    radii_left_upper: str
    radii_margin_lower: str
    uniform_bordered_inverse_norm_upper: str | None
    parameter_box_orbit_validated: bool
    parameter_box_bordered_inverse_validated: bool


@dataclass(frozen=True)
class DirectedExtremaBox:
    """Directed isolation of the unique voltage maximum and minimum."""

    phase_partition_count: int
    maximum_phase_lower: str | None
    maximum_phase_upper: str | None
    minimum_phase_lower: str | None
    minimum_phase_upper: str | None
    root_refinement_denominator: int
    maximum_curvature_window_lower: str | None
    maximum_curvature_window_upper: str | None
    minimum_curvature_window_lower: str | None
    minimum_curvature_window_upper: str | None
    maximum_curvature_upper: str | None
    minimum_curvature_lower: str | None
    complement_derivative_gap_lower: str | None
    derivative_error_upper: str
    all_complement_cells_strict: bool
    extrema_validated: bool
    failure_reason: str | None


@dataclass(frozen=True)
class DirectedResponseBox:
    """Directed enclosure of D_(kappa_1,kappa_3)(F,R_h)."""

    control_order: tuple[str, str]
    output_order: tuple[str, str]
    sensitivity_error_upper: tuple[str, str]
    sensitivity_budgets: (
        tuple["DirectedSensitivityBudget", "DirectedSensitivityBudget"]
        | None
    )
    response_lower: tuple[tuple[str, str], tuple[str, str]] | None
    response_upper: tuple[tuple[str, str], tuple[str, str]] | None
    midpoint_binary64: tuple[tuple[float, float], tuple[float, float]]
    midpoint_smallest_singular_value_lower: str
    response_frobenius_radius_upper: str | None
    smallest_singular_value_lower: str | None
    response_box_validated: bool
    derivative_lipschitz_bound_supplied: bool
    failure_reason: str | None


@dataclass(frozen=True)
class DirectedSensitivityBudget:
    """Auditable decomposition of one directed sensitivity error."""

    control: str
    finite_preconditioned_residual_upper: str
    finite_interval_remainder_upper: str
    analytic_tail_residual_upper: str
    base_preconditioned_residual_upper: str
    global_preconditioner_l1_upper: str
    state_jacobian_variation_upper: str
    period_column_variation_upper: str
    slow_equation_variation_upper: str
    gain_forcing_variation_upper: str
    raw_variation_upper: str
    preconditioned_variation_upper: str
    exact_sensitivity_error_upper: str


@dataclass(frozen=True)
class DirectedPeriodicParameterBoxValidation:
    """Combined D1/D3/D4 result with explicit theorem gates."""

    gain_box: DirectedGainBox
    continuation: DirectedBoxContinuation
    extrema: DirectedExtremaBox
    response: DirectedResponseBox
    d1_validated: bool
    d3_validated: bool
    d4_response_lower_bound_validated: bool
    all_d1_d3_d4_validated: bool
    issue_15_closed: bool
    remaining_gates: tuple[str, ...]


@dataclass
class _Workspace:
    orbit: PeriodicOrbitCandidate
    base: _BaseSequences
    layout: _RealConjugateLayout
    approximate_inverse: np.ndarray
    approximate_inverse_l1: gmpy2.mpfr
    analytic_tail_inverse_l1: gmpy2.mpfr
    global_preconditioner_l1: gmpy2.mpfr
    chosen_radius: DirectedInterval
    contraction: gmpy2.mpfr
    inverse_norm: gmpy2.mpfr | None
    continuation: DirectedBoxContinuation


@dataclass(frozen=True)
class _VariationBounds:
    derivative_error: gmpy2.mpfr
    field_difference: gmpy2.mpfr
    linear_field_difference: gmpy2.mpfr
    cubic_field_difference: gmpy2.mpfr
    current_coefficient_difference: gmpy2.mpfr
    delayed_coefficient_differences: tuple[gmpy2.mpfr, gmpy2.mpfr]
    shifted_voltage_differences: tuple[gmpy2.mpfr, gmpy2.mpfr]


@dataclass(frozen=True)
class _SensitivityVariationBudget:
    state_part: gmpy2.mpfr
    period_part: gmpy2.mpfr
    slow_part: gmpy2.mpfr
    gain_part: gmpy2.mpfr
    raw_total: gmpy2.mpfr
    preconditioned_total: gmpy2.mpfr


@dataclass(frozen=True)
class _PreconditionedResidualBudget:
    finite_center: gmpy2.mpfr
    finite_interval_remainder: gmpy2.mpfr
    analytic_tail: gmpy2.mpfr
    total: gmpy2.mpfr


def _symmetric_decimal_interval(
    center: float, radius: str, precision: int
) -> DirectedInterval:
    point = DirectedInterval.from_decimal(str(float(center)), precision)
    width = DirectedInterval.from_decimal(radius, precision)
    if width.lower < 0:
        raise ValueError("gain half-width must be nonnegative")
    return point + _symmetric_mpfr_interval(width.upper, precision)


def _symmetric_mpfr_interval(
    radius: gmpy2.mpfr, precision: int
) -> DirectedInterval:
    """Return ``[-radius,radius]`` without a default-context unary minus.

    Applying unary ``-`` directly to an MPFR value before constructing an
    interval can silently round at the process default precision.  Negating
    a :class:`DirectedInterval` keeps the declared precision and directions.
    """

    positive = DirectedInterval.from_bounds(radius, radius, precision)
    if positive.lower < 0:
        raise ValueError("symmetric radius must be nonnegative")
    negative = -positive
    return DirectedInterval.from_bounds(
        negative.lower, positive.upper, precision
    )


def _build_parameter_box_sequences(
    orbit: PeriodicOrbitCandidate,
    precision: int,
    half_width: str,
) -> _BaseSequences:
    """Build the center polynomial residual/Jacobian over a gain box."""

    parameters = _interval_parameters(orbit.parameters, precision)
    parameters["kappa_1"] = _symmetric_decimal_interval(
        orbit.parameters.kappa_1, half_width, precision
    )
    parameters["kappa_3"] = _symmetric_decimal_interval(
        orbit.parameters.kappa_3, half_width, precision
    )
    epsilon = parameters["epsilon"]
    kappa_1 = parameters["kappa_1"]
    kappa_3 = parameters["kappa_3"]
    period = DirectedInterval.from_float(orbit.period, precision)
    voltage = directed_dft(orbit.state[:, 0], precision)
    recovery = directed_dft(orbit.state[:, 1], precision)
    one = _constant_sequence(_one(precision), precision)
    unfolding = _constant_sequence(parameters["unfolding"], precision)
    centered = _sequence_sub(voltage, one)
    voltage_squared = _sequence_convolution(voltage, voltage)
    voltage_cubed = _sequence_convolution(voltage_squared, voltage)
    centered_squared = _sequence_convolution(centered, centered)
    centered_cubed = _sequence_convolution(centered_squared, centered)

    delayed: list[ComplexSequence] = []
    delayed_centered_cubed: list[ComplexSequence] = []
    delayed_coefficients: list[ComplexSequence] = []
    for tau in (parameters["tau_0"], parameters["tau_1"]):
        shifted = _sequence_shift(voltage, tau / period)
        shifted_centered = _sequence_sub(shifted, one)
        shifted_centered_squared = _sequence_convolution(
            shifted_centered, shifted_centered
        )
        delayed.append(shifted)
        delayed_centered_cubed.append(
            _sequence_convolution(
                shifted_centered_squared, shifted_centered
            )
        )
        delayed_coefficients.append(
            _sequence_scale(
                _sequence_add(
                    _constant_sequence(kappa_1, precision),
                    _sequence_scale(
                        shifted_centered_squared, 3 * kappa_3
                    ),
                ),
                epsilon / 2,
            )
        )

    linear_difference = _sequence_sub(
        _sequence_scale(_sequence_add(delayed[0], delayed[1]), "0.5"),
        voltage,
    )
    cubic_difference = _sequence_sub(
        _sequence_scale(
            _sequence_add(
                delayed_centered_cubed[0], delayed_centered_cubed[1]
            ),
            "0.5",
        ),
        centered_cubed,
    )
    fast = _sequence_sub(
        _sequence_sub(
            voltage,
            _sequence_scale(voltage_cubed, _one(precision) / 3),
        ),
        recovery,
    )
    fast = _sequence_add(
        fast, _sequence_scale(linear_difference, epsilon * kappa_1)
    )
    fast = _sequence_add(
        fast, _sequence_scale(cubic_difference, epsilon * kappa_3)
    )
    slow = _sequence_scale(
        _sequence_sub(voltage, unfolding), epsilon
    )
    residual_voltage = _sequence_sub(
        _sequence_derivative(voltage, precision),
        _sequence_scale(fast, period),
    )
    residual_recovery = _sequence_sub(
        _sequence_derivative(recovery, precision),
        _sequence_scale(slow, period),
    )

    current = _sequence_sub(
        _constant_sequence(_one(precision) - epsilon * kappa_1, precision),
        voltage_squared,
    )
    current = _sequence_sub(
        current,
        _sequence_scale(centered_squared, 3 * epsilon * kappa_3),
    )
    period_voltage = _sequence_neg(fast)
    tangent_voltage = _sequence_derivative(voltage, precision)
    for tau, coefficient in zip(
        (parameters["tau_0"], parameters["tau_1"]),
        delayed_coefficients,
        strict=True,
    ):
        shifted_tangent = _sequence_shift(tangent_voltage, tau / period)
        period_voltage = _sequence_sub(
            period_voltage,
            _sequence_scale(
                _sequence_convolution(coefficient, shifted_tangent),
                tau / period,
            ),
        )
    period_recovery = _sequence_neg(slow)

    delayed_field = _sequence_add(
        _sequence_scale(voltage, epsilon * kappa_1 / 2),
        _sequence_scale(centered_cubed, epsilon * kappa_3 / 2),
    )
    delayed_field_derivative = _sequence_derivative(
        delayed_field, precision
    )
    delayed_state_derivative = _sequence_add(
        _constant_sequence(epsilon * kappa_1 / 2, precision),
        _sequence_scale(centered_squared, 3 * epsilon * kappa_3 / 2),
    )
    return _BaseSequences(
        parameters=parameters,
        period=period,
        voltage=voltage,
        recovery=recovery,
        current_coefficient=current,
        delayed_coefficients=(
            delayed_coefficients[0], delayed_coefficients[1]
        ),
        residual_voltage=residual_voltage,
        residual_recovery=residual_recovery,
        period_voltage=period_voltage,
        period_recovery=period_recovery,
        phase_voltage=tangent_voltage,
        phase_recovery=_sequence_derivative(recovery, precision),
        centered_voltage=centered,
        delayed_field=delayed_field,
        delayed_field_derivative=delayed_field_derivative,
        delayed_state_derivative=delayed_state_derivative,
    )


def _validate_continuation(
    orbit: PeriodicOrbitCandidate,
    *,
    half_width: str,
    cutoff: int,
    precision: int,
    maximum_radius: str,
    chosen_radius: str,
) -> _Workspace:
    if cutoff < (len(orbit.state) - 1) // 2:
        raise ValueError("cutoff must contain the candidate Fourier support")
    base = _build_parameter_box_sequences(orbit, precision, half_width)
    if (
        base.parameters["kappa_1"].lower < 0
        or base.parameters["kappa_3"].lower < 0
    ):
        raise ValueError("the gain box must stay in the nonnegative quadrant")
    real_matrix, matrix_distance, layout = _finite_coefficient_matrix(
        base, cutoff
    )
    approximate_inverse = np.linalg.inv(real_matrix)
    approximate_inverse_l1 = _float_matrix_l1_upper(
        approximate_inverse, precision
    )
    tail_denominator = (
        pi_interval(precision) * (2 * (cutoff + 1))
    ).lower
    analytic_tail_inverse_l1 = upward_division(
        gmpy2.mpfr(1, precision), tail_denominator, precision
    )
    global_preconditioner_l1 = max(
        approximate_inverse_l1, analytic_tail_inverse_l1
    )
    base_defect, _, _, ieee_checked = _binary_product_defect_upper(
        real_matrix.T, approximate_inverse.T, precision
    )
    if not ieee_checked or ctypes.sizeof(ctypes.c_double) != 8:
        raise RuntimeError("the binary64 product model is unavailable")
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        finite_defect = (
            base_defect + approximate_inverse_l1 * matrix_distance
        )

    residual_midpoint, residual_distance = _residual_vector(base, layout)
    finite_y = _binary_matvec_l1_upper(
        approximate_inverse,
        residual_midpoint,
        precision,
        approximate_inverse_l1,
    )
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        finite_y += approximate_inverse_l1 * residual_distance
        total_y = finite_y + _tail_residual_upper(base, cutoff)

    tail_from_finite = _tail_from_finite_upper(base, layout)
    finite_from_tail = _finite_from_tail_upper(
        base, layout, approximate_inverse, approximate_inverse_l1
    )
    tail_to_tail = _tail_to_tail_upper(base, cutoff)
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        finite_input = finite_defect + tail_from_finite
        tail_input = finite_from_tail + tail_to_tail
        full_defect = max(finite_input, tail_input)

    z1, z2, z3 = _nonlinear_coefficients(
        base, cutoff, approximate_inverse_l1, maximum_radius
    )
    radius = DirectedInterval.from_decimal(chosen_radius, precision)
    maximum = DirectedInterval.from_decimal(maximum_radius, precision)
    if radius.upper > maximum.upper:
        raise ValueError("chosen radius exceeds maximum radius")
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        variation = (
            z1 * radius.upper
            + z2 * radius.upper * radius.upper
            + z3 * radius.upper * radius.upper * radius.upper
        )
        contraction = full_defect + variation
        radii_left = total_y + contraction * radius.upper
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        margin = radius.lower - radii_left
    validated = contraction < 1 and margin > 0
    inverse_norm: gmpy2.mpfr | None = None
    if validated:
        with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
            inverse_norm = global_preconditioner_l1 / (1 - contraction)

    residual_support = max(
        max(abs(mode) for mode in base.residual_voltage),
        max(abs(mode) for mode in base.residual_recovery),
    )
    continuation = DirectedBoxContinuation(
        cutoff=cutoff,
        precision_bits=precision,
        real_conjugate_dimension=layout.dimension,
        residual_support_half_bandwidth=residual_support,
        approximate_inverse_l1_upper=decimal_upper(
            approximate_inverse_l1
        ),
        analytic_tail_inverse_l1_upper=decimal_upper(
            analytic_tail_inverse_l1
        ),
        global_preconditioner_l1_upper=decimal_upper(
            global_preconditioner_l1
        ),
        finite_inverse_defect_upper=decimal_upper(finite_defect),
        finite_to_finite_upper=decimal_upper(finite_defect),
        tail_from_finite_upper=decimal_upper(tail_from_finite),
        finite_from_tail_upper=decimal_upper(finite_from_tail),
        tail_to_tail_upper=decimal_upper(tail_to_tail),
        full_point_defect_upper=decimal_upper(full_defect),
        preconditioned_box_residual_upper=decimal_upper(total_y),
        coefficient_z1_upper=decimal_upper(z1),
        coefficient_z2_upper=decimal_upper(z2),
        coefficient_z3_upper=decimal_upper(z3),
        chosen_radius=chosen_radius,
        derivative_variation_upper=decimal_upper(variation),
        uniform_contraction_upper=decimal_upper(contraction),
        radii_left_upper=decimal_upper(radii_left),
        radii_margin_lower=decimal_lower(margin),
        uniform_bordered_inverse_norm_upper=(
            decimal_upper(inverse_norm) if inverse_norm is not None else None
        ),
        parameter_box_orbit_validated=validated,
        parameter_box_bordered_inverse_validated=validated,
    )
    return _Workspace(
        orbit=orbit,
        base=base,
        layout=layout,
        approximate_inverse=approximate_inverse,
        approximate_inverse_l1=approximate_inverse_l1,
        analytic_tail_inverse_l1=analytic_tail_inverse_l1,
        global_preconditioner_l1=global_preconditioner_l1,
        chosen_radius=radius,
        contraction=contraction,
        inverse_norm=inverse_norm,
        continuation=continuation,
    )


def _candidate_fields(
    base: _BaseSequences,
) -> tuple[ComplexSequence, ComplexSequence, tuple[ComplexSequence, ...]]:
    """Return center linear/cubic gain fields and shifted voltages."""

    precision = base.period.precision
    one = _constant_sequence(_one(precision), precision)
    shifted = tuple(
        _sequence_shift(base.voltage, tau / base.period)
        for tau in (base.parameters["tau_0"], base.parameters["tau_1"])
    )
    linear = _sequence_sub(
        _sequence_scale(_sequence_add(shifted[0], shifted[1]), "0.5"),
        base.voltage,
    )
    centered = base.centered_voltage
    centered_cubed = _sequence_convolution(
        _sequence_convolution(centered, centered), centered
    )
    delayed_cubed: list[ComplexSequence] = []
    for item in shifted:
        shifted_centered = _sequence_sub(item, one)
        delayed_cubed.append(
            _sequence_convolution(
                _sequence_convolution(
                    shifted_centered, shifted_centered
                ),
                shifted_centered,
            )
        )
    cubic = _sequence_sub(
        _sequence_scale(
            _sequence_add(delayed_cubed[0], delayed_cubed[1]), "0.5"
        ),
        centered_cubed,
    )
    return linear, cubic, shifted


def _variation_bounds(workspace: _Workspace) -> _VariationBounds:
    """Specific raw-Wiener bounds used by D3 and the two D4 columns."""

    base = workspace.base
    precision = base.period.precision
    rho = workspace.chosen_radius.upper
    epsilon = base.parameters["epsilon"].upper
    kappa_1_max = base.parameters["kappa_1"].upper
    kappa_3_max = base.parameters["kappa_3"].upper
    center_kappa_1 = DirectedInterval.from_decimal(
        str(float(workspace.orbit.parameters.kappa_1)), precision
    )
    center_kappa_3 = DirectedInterval.from_decimal(
        str(float(workspace.orbit.parameters.kappa_3)), precision
    )
    h1 = (base.parameters["kappa_1"] - center_kappa_1).upper_abs()
    h3 = (base.parameters["kappa_3"] - center_kappa_3).upper_abs()
    sigma = DirectedInterval.from_decimal(2, precision).sqrt().upper
    minimum_period = (base.period - workspace.chosen_radius).lower
    maximum_period = (base.period + workspace.chosen_radius).upper

    voltage_norm = _sequence_box_norm_upper(base.voltage, precision)
    centered_norm = _sequence_box_norm_upper(
        base.centered_voltage, precision
    )
    derivative_voltage_norm = _sequence_box_norm_upper(
        base.phase_voltage, precision
    )
    linear, cubic, shifted = _candidate_fields(base)
    linear_norm = _sequence_box_norm_upper(linear, precision)
    cubic_norm = _sequence_box_norm_upper(cubic, precision)
    shifted_centered_norms = tuple(
        _sequence_box_norm_upper(
            _sequence_sub(
                item, _constant_sequence(_one(precision), precision)
            ),
            precision,
        )
        for item in shifted
    )

    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        inverse_period_difference = rho / (
            minimum_period * base.period.lower
        )
        shifted_differences = tuple(
            sigma * rho
            + sigma
            * derivative_voltage_norm
            * tau.upper
            * inverse_period_difference
            for tau in (
                base.parameters["tau_0"], base.parameters["tau_1"]
            )
        )
        linear_difference = (
            (shifted_differences[0] + shifted_differences[1]) / 2
            + rho
        )
        local_cubic_difference = rho * (
            3 * centered_norm * centered_norm
            + 3 * centered_norm * rho
            + rho * rho
        )
        shifted_cubic_differences = tuple(
            delta
            * (
                3 * norm * norm + 3 * norm * delta + delta * delta
            )
            for delta, norm in zip(
                shifted_differences, shifted_centered_norms, strict=True
            )
        )
        cubic_difference = (
            (shifted_cubic_differences[0] + shifted_cubic_differences[1])
            / 2
            + local_cubic_difference
        )
        local_field_difference = (
            2 * rho
            + rho
            * (
                voltage_norm * voltage_norm
                + voltage_norm * rho
                + rho * rho / 3
            )
        )
        field_difference = (
            local_field_difference
            + epsilon
            * (kappa_1_max * linear_difference + h1 * linear_norm)
            + epsilon
            * (kappa_3_max * cubic_difference + h3 * cubic_norm)
        )

        # The center field is recovered from Dv = T f + residual.  This
        # avoids rebuilding another dependency-heavy interval polynomial.
        center_fast_norm = (
            derivative_voltage_norm
            + _sequence_box_norm_upper(base.residual_voltage, precision)
        ) / base.period.lower
        derivative_error = (
            rho * center_fast_norm
            + maximum_period * field_difference
            + _sequence_box_norm_upper(base.residual_voltage, precision)
        )

        current_difference = (
            rho * (2 * voltage_norm + rho)
            + epsilon * h1
            + 3
            * epsilon
            * (
                kappa_3_max * rho * (2 * centered_norm + rho)
                + h3 * centered_norm * centered_norm
            )
        )
        delayed_coefficient_differences = tuple(
            epsilon
            / 2
            * (
                h1
                + 3
                * (
                    kappa_3_max * delta * (2 * norm + delta)
                    + h3 * norm * norm
                )
            )
            for delta, norm in zip(
                shifted_differences, shifted_centered_norms, strict=True
            )
        )
    return _VariationBounds(
        derivative_error=derivative_error,
        field_difference=field_difference,
        linear_field_difference=linear_difference,
        cubic_field_difference=cubic_difference,
        current_coefficient_difference=current_difference,
        delayed_coefficient_differences=(
            delayed_coefficient_differences[0],
            delayed_coefficient_differences[1],
        ),
        shifted_voltage_differences=(
            shifted_differences[0], shifted_differences[1]
        ),
    )


def _evaluate_real_sequence(
    sequence: Mapping[int, DirectedComplexInterval],
    phase: DirectedInterval,
) -> DirectedInterval:
    """Evaluate a real-conjugate Fourier polynomial on a phase interval."""

    precision = phase.precision
    result = DirectedInterval.from_decimal(0, precision)
    two_pi = pi_interval(precision) * 2
    from canard_control.directed_interval import complex_unit_interval

    for mode, coefficient in sequence.items():
        exponential = complex_unit_interval(two_pi * mode * phase)
        result += (coefficient * exponential).real
    return result


def _vprime_interval(
    workspace: _Workspace,
    variation: _VariationBounds,
    phase: DirectedInterval,
) -> DirectedInterval:
    center = _evaluate_real_sequence(workspace.base.phase_voltage, phase)
    error = _symmetric_mpfr_interval(
        variation.derivative_error, phase.precision
    )
    return center + error


def _state_interval(
    sequence: Mapping[int, DirectedComplexInterval],
    phase: DirectedInterval,
    radius: gmpy2.mpfr,
) -> DirectedInterval:
    return _evaluate_real_sequence(sequence, phase) + _symmetric_mpfr_interval(
        radius, phase.precision
    )


def _vsecond_interval(
    workspace: _Workspace,
    variation: _VariationBounds,
    phase: DirectedInterval,
) -> DirectedInterval:
    """Evaluate V'' from the RFDE, avoiding an unproved X^2 ball."""

    base = workspace.base
    precision = phase.precision
    rho = workspace.chosen_radius.upper
    period = base.period + _symmetric_mpfr_interval(rho, precision)
    epsilon = base.parameters["epsilon"]
    kappa_1 = base.parameters["kappa_1"]
    kappa_3 = base.parameters["kappa_3"]
    one = DirectedInterval.from_decimal(1, precision)
    voltage = _state_interval(base.voltage, phase, rho)
    voltage_prime = _vprime_interval(workspace, variation, phase)
    recovery_prime = period * epsilon * (
        voltage - base.parameters["unfolding"]
    )
    current = (
        one
        - voltage * voltage
        - epsilon * kappa_1
        - 3 * epsilon * kappa_3 * (voltage - one) ** 2
    )
    bracket = current * voltage_prime - recovery_prime
    for tau in (base.parameters["tau_0"], base.parameters["tau_1"]):
        delayed_phase = phase - tau / period
        delayed_voltage = _state_interval(base.voltage, delayed_phase, rho)
        delayed_prime = _vprime_interval(
            workspace, variation, delayed_phase
        )
        coefficient = epsilon / 2 * (
            kappa_1 + 3 * kappa_3 * (delayed_voltage - one) ** 2
        )
        bracket += coefficient * delayed_prime
    return period * bracket


def _validate_extrema(
    workspace: _Workspace,
    *,
    partition_count: int,
) -> DirectedExtremaBox:
    precision = workspace.base.period.precision
    variation = _variation_bounds(workspace)
    if workspace.inverse_norm is None:
        return DirectedExtremaBox(
            phase_partition_count=partition_count,
            maximum_phase_lower=None,
            maximum_phase_upper=None,
            minimum_phase_lower=None,
            minimum_phase_upper=None,
            root_refinement_denominator=2**26,
            maximum_curvature_window_lower=None,
            maximum_curvature_window_upper=None,
            minimum_curvature_window_lower=None,
            minimum_curvature_window_upper=None,
            maximum_curvature_upper=None,
            minimum_curvature_lower=None,
            complement_derivative_gap_lower=None,
            derivative_error_upper=decimal_upper(
                variation.derivative_error
            ),
            all_complement_cells_strict=False,
            extrema_validated=False,
            failure_reason="D1 did not validate the parameter box",
        )
    if partition_count < 512:
        raise ValueError("phase partition must contain at least 512 cells")
    extrema = periodic_response_candidate(workspace.orbit).extrema
    roots = (extrema.maximum_phase, extrema.minimum_phase)
    # Four cells on each side are wide enough for robust endpoint signs at
    # N_phase=4096, while avoiding needless response-evaluation wrapping.
    half_window_cells = max(4, partition_count // 2048)
    denominator = DirectedInterval.from_decimal(partition_count, precision)

    windows: list[tuple[int, int, DirectedInterval]] = []
    for root in roots:
        center_index = int(np.floor(root * partition_count))
        left_index = center_index - half_window_cells
        right_index = center_index + half_window_cells + 1
        if left_index <= 0 or right_index >= partition_count:
            raise RuntimeError("declared extremum window crosses the phase cut")
        phase = DirectedInterval.from_decimal(left_index, precision) / denominator
        phase = DirectedInterval.from_bounds(
            phase.lower,
            (
                DirectedInterval.from_decimal(right_index, precision)
                / denominator
            ).upper,
            precision,
        )
        windows.append((left_index, right_index, phase))
    occupied = set()
    for left, right, _ in windows:
        occupied.update(range(left, right))

    complement_gap: gmpy2.mpfr | None = None
    complement_strict = True
    for index in range(partition_count):
        if index in occupied:
            continue
        left = DirectedInterval.from_decimal(index, precision) / denominator
        right = (
            DirectedInterval.from_decimal(index + 1, precision) / denominator
        )
        cell = DirectedInterval.from_bounds(
            left.lower, right.upper, precision
        )
        derivative = _vprime_interval(workspace, variation, cell)
        gap = derivative.lower_abs()
        if gap <= 0:
            complement_strict = False
            break
        complement_gap = gap if complement_gap is None else min(
            complement_gap, gap
        )

    curvatures = [
        _vsecond_interval(workspace, variation, phase)
        for _, _, phase in windows
    ]
    endpoint_signs: list[tuple[DirectedInterval, DirectedInterval]] = []
    for left_index, right_index, _ in windows:
        left = DirectedInterval.from_decimal(left_index, precision) / denominator
        right = DirectedInterval.from_decimal(right_index, precision) / denominator
        endpoint_signs.append(
            (
                _vprime_interval(workspace, variation, left),
                _vprime_interval(workspace, variation, right),
            )
        )
    maximum_ok = (
        curvatures[0].upper < 0
        and endpoint_signs[0][0].lower > 0
        and endpoint_signs[0][1].upper < 0
    )
    minimum_ok = (
        curvatures[1].lower > 0
        and endpoint_signs[1][0].upper < 0
        and endpoint_signs[1][1].lower > 0
    )
    validated = complement_strict and maximum_ok and minimum_ok
    refined_phases: list[DirectedInterval] = []
    if validated:
        # The broad grid windows prove uniqueness and curvature.  Refine only
        # the location used by D4 on a dyadic grid: endpoint signs then place
        # that already-unique zero in a much narrower interval.  The floating
        # roots merely choose the finite search neighborhood; every accepted
        # endpoint sign is directed.
        refinement_count = 2**26
        refinement_denominator = DirectedInterval.from_decimal(
            refinement_count, precision
        )
        for root_index, root in enumerate(roots):
            center_index = int(np.floor(root * refinement_count))
            signed_points: list[tuple[int, DirectedInterval]] = []
            for index in range(center_index - 64, center_index + 65):
                point = (
                    DirectedInterval.from_decimal(index, precision)
                    / refinement_denominator
                )
                signed_points.append(
                    (index, _vprime_interval(workspace, variation, point))
                )
            if root_index == 0:
                left_candidates = [
                    index for index, value in signed_points if value.lower > 0
                ]
                right_candidates = [
                    index for index, value in signed_points if value.upper < 0
                ]
            else:
                left_candidates = [
                    index for index, value in signed_points if value.upper < 0
                ]
                right_candidates = [
                    index for index, value in signed_points if value.lower > 0
                ]
            brackets = [
                (left, right)
                for left in left_candidates
                for right in right_candidates
                if left < right
            ]
            if not brackets:
                validated = False
                break
            left_index, right_index = min(
                brackets, key=lambda item: item[1] - item[0]
            )
            left = (
                DirectedInterval.from_decimal(left_index, precision)
                / refinement_denominator
            )
            right = (
                DirectedInterval.from_decimal(right_index, precision)
                / refinement_denominator
            )
            refined = DirectedInterval.from_bounds(
                left.lower, right.upper, precision
            )
            broad = windows[root_index][2]
            if refined.lower < broad.lower or refined.upper > broad.upper:
                validated = False
                break
            refined_phases.append(refined)
    if validated and len(refined_phases) != 2:
        validated = False
    reason = None
    if not validated:
        failed = []
        if not complement_strict:
            failed.append("a complementary phase cell contains zero in V'")
        if not maximum_ok:
            failed.append("maximum window failed curvature/endpoint signs")
        if not minimum_ok:
            failed.append("minimum window failed curvature/endpoint signs")
        if maximum_ok and minimum_ok and len(refined_phases) != 2:
            failed.append("dyadic directed root refinement found no bracket")
        reason = "; ".join(failed)
    max_phase = refined_phases[0] if len(refined_phases) == 2 else windows[0][2]
    min_phase = refined_phases[1] if len(refined_phases) == 2 else windows[1][2]
    return DirectedExtremaBox(
        phase_partition_count=partition_count,
        maximum_phase_lower=decimal_lower(max_phase.lower),
        maximum_phase_upper=decimal_upper(max_phase.upper),
        minimum_phase_lower=decimal_lower(min_phase.lower),
        minimum_phase_upper=decimal_upper(min_phase.upper),
        root_refinement_denominator=2**26,
        maximum_curvature_window_lower=decimal_lower(
            windows[0][2].lower
        ),
        maximum_curvature_window_upper=decimal_upper(
            windows[0][2].upper
        ),
        minimum_curvature_window_lower=decimal_lower(
            windows[1][2].lower
        ),
        minimum_curvature_window_upper=decimal_upper(
            windows[1][2].upper
        ),
        maximum_curvature_upper=decimal_upper(curvatures[0].upper),
        minimum_curvature_lower=decimal_lower(curvatures[1].lower),
        complement_derivative_gap_lower=(
            decimal_lower(complement_gap)
            if complement_gap is not None
            else None
        ),
        derivative_error_upper=decimal_upper(variation.derivative_error),
        all_complement_cells_strict=complement_strict,
        extrema_validated=validated,
        failure_reason=reason,
    )


def _floating_sensitivity_sequences(
    orbit: PeriodicOrbitCandidate, precision: int
) -> tuple[
    tuple[ComplexSequence, ComplexSequence, DirectedInterval],
    tuple[ComplexSequence, ComplexSequence, DirectedInterval],
]:
    state = np.asarray(orbit.state, dtype=float)
    count = len(state)
    derivative, _ = odd_fourier_matrices(count)
    reference_derivative = derivative @ state
    unknown = np.concatenate((state[:, 0], state[:, 1], [orbit.period]))
    _, jacobian, shifts = _collocation_system(
        unknown,
        orbit.parameters,
        derivative,
        state,
        reference_derivative,
    )
    delayed_0 = shifts[0] @ state[:, 0]
    delayed_1 = shifts[1] @ state[:, 0]
    _, _, linear, cubic = _field_data(
        state[:, 0],
        state[:, 1],
        delayed_0,
        delayed_1,
        orbit.parameters,
    )
    rhs = np.zeros((2 * count + 1, 2), dtype=float)
    rhs[:count, 0] = orbit.period * orbit.parameters.epsilon * linear
    rhs[:count, 1] = orbit.period * orbit.parameters.epsilon * cubic
    sensitivities = np.linalg.solve(jacobian, rhs)
    result = []
    for column in range(2):
        result.append(
            (
                directed_dft(sensitivities[:count, column], precision),
                directed_dft(
                    sensitivities[count : 2 * count, column], precision
                ),
                DirectedInterval.from_float(
                    float(sensitivities[-1, column]), precision
                ),
            )
        )
    return result[0], result[1]


def _phase_pairing(
    base: _BaseSequences,
    voltage: Mapping[int, DirectedComplexInterval],
    recovery: Mapping[int, DirectedComplexInterval],
) -> DirectedComplexInterval:
    precision = base.period.precision
    result = _complex_zero(precision)
    for mode, value in voltage.items():
        result += base.phase_voltage.get(-mode, _complex_zero(precision)) * value
    for mode, value in recovery.items():
        result += base.phase_recovery.get(-mode, _complex_zero(precision)) * value
    return result


def _sensitivity_residual(
    base: _BaseSequences,
    sensitivity: tuple[ComplexSequence, ComplexSequence, DirectedInterval],
    control_index: int,
) -> tuple[ComplexSequence, ComplexSequence, DirectedComplexInterval]:
    """Return J_box(x_bar) s_bar + F_kappa(x_bar)."""

    precision = base.period.precision
    sv, sw, st = sensitivity
    local = _sequence_sub(
        _sequence_convolution(base.current_coefficient, sv), sw
    )
    for tau, coefficient in zip(
        (base.parameters["tau_0"], base.parameters["tau_1"]),
        base.delayed_coefficients,
        strict=True,
    ):
        local = _sequence_add(
            local,
            _sequence_convolution(
                coefficient, _sequence_shift(sv, tau / base.period)
            ),
        )
    fast = _sequence_sub(
        _sequence_derivative(sv, precision),
        _sequence_scale(local, base.period),
    )
    fast = _sequence_add(
        fast, _sequence_scale(base.period_voltage, st)
    )
    slow = _sequence_sub(
        _sequence_derivative(sw, precision),
        _sequence_scale(
            sv, base.period * base.parameters["epsilon"]
        ),
    )
    slow = _sequence_add(
        slow, _sequence_scale(base.period_recovery, st)
    )
    linear, cubic, _ = _candidate_fields(base)
    gain_field = linear if control_index == 0 else cubic
    fast = _sequence_sub(
        fast,
        _sequence_scale(
            gain_field, base.period * base.parameters["epsilon"]
        ),
    )
    return fast, slow, _phase_pairing(base, sv, sw)


def _preconditioned_sequence_upper(
    workspace: _Workspace,
    fast: Mapping[int, DirectedComplexInterval],
    slow: Mapping[int, DirectedComplexInterval],
    phase: DirectedComplexInterval,
) -> _PreconditionedResidualBudget:
    precision = workspace.base.period.precision
    cutoff = workspace.layout.cutoff
    zero = _complex_zero(precision)
    finite_fast = {mode: fast.get(mode, zero) for mode in range(cutoff + 1)}
    finite_slow = {mode: slow.get(mode, zero) for mode in range(cutoff + 1)}
    intervals = _scaled_real_coordinate_intervals(
        workspace.layout,
        finite_fast,
        finite_slow,
        phase,
        input_weight=1,
    )
    centers = np.asarray(
        [float(value.midpoint_nearest()) for value in intervals], dtype=float
    )
    distance = upward_sum(
        [
            (
                value
                - DirectedInterval.from_float(float(center), precision)
            ).upper_abs()
            for value, center in zip(intervals, centers, strict=True)
        ],
        precision,
    )
    finite_center = _binary_matvec_l1_upper(
        workspace.approximate_inverse,
        centers,
        precision,
        workspace.approximate_inverse_l1,
    )
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        finite_interval_remainder = (
            workspace.approximate_inverse_l1 * distance
        )
    tail_terms: list[gmpy2.mpfr] = []
    for sequence in (fast, slow):
        for mode, value in sequence.items():
            if abs(mode) <= cutoff:
                continue
            denominator = (pi_interval(precision) * (2 * abs(mode))).lower
            tail_terms.append(
                upward_division(_box_abs_upper(value), denominator, precision)
            )
    analytic_tail = upward_sum(tail_terms, precision)
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        total = finite_center + finite_interval_remainder + analytic_tail
    return _PreconditionedResidualBudget(
        finite_center=finite_center,
        finite_interval_remainder=finite_interval_remainder,
        analytic_tail=analytic_tail,
        total=total,
    )


def _sequence_derivative_norm(
    sequence: Mapping[int, DirectedComplexInterval], precision: int
) -> gmpy2.mpfr:
    return _sequence_box_norm_upper(
        _sequence_derivative(sequence, precision), precision
    )


def _specific_sensitivity_variation_upper(
    workspace: _Workspace,
    variation: _VariationBounds,
    sensitivity: tuple[ComplexSequence, ComplexSequence, DirectedInterval],
    control_index: int,
) -> _SensitivityVariationBudget:
    """Decompose ``A[(J(z)-J(xbar))s + F_q(z)-F_q(xbar)]``."""

    base = workspace.base
    precision = base.period.precision
    rho = workspace.chosen_radius.upper
    epsilon = base.parameters["epsilon"].upper
    sigma = DirectedInterval.from_decimal(2, precision).sqrt().upper
    minimum_period = (base.period - workspace.chosen_radius).lower
    maximum_period = (base.period + workspace.chosen_radius).upper
    sv, sw, st_interval = sensitivity
    st = st_interval.upper_abs()
    sv_norm = _sequence_box_norm_upper(sv, precision)
    sw_norm = _sequence_box_norm_upper(sw, precision)
    dsv_norm = _sequence_derivative_norm(sv, precision)
    linear, cubic, _ = _candidate_fields(base)
    gain_norm = _sequence_box_norm_upper(
        linear if control_index == 0 else cubic, precision
    )
    field_change = (
        variation.linear_field_difference
        if control_index == 0
        else variation.cubic_field_difference
    )
    delayed_coefficient_norms = tuple(
        _sequence_box_norm_upper(item, precision)
        for item in base.delayed_coefficients
    )
    delayed_state_shift_changes: list[gmpy2.mpfr] = []
    shifted_derivative_changes: list[gmpy2.mpfr] = []
    alpha_changes: list[gmpy2.mpfr] = []
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        for tau in (base.parameters["tau_0"], base.parameters["tau_1"]):
            alpha_change = (
                tau.upper
                * rho
                / (minimum_period * base.period.lower)
            )
            alpha_changes.append(alpha_change)
            delayed_state_shift_changes.append(
                sigma * dsv_norm * alpha_change
            )
            shifted_derivative_changes.append(
                sigma * variation.derivative_error
                + sigma
                * _sequence_box_norm_upper(
                    _sequence_derivative(base.phase_voltage, precision),
                    precision,
                )
                * alpha_change
            )

        local_center_norm = (
            _sequence_box_norm_upper(base.current_coefficient, precision)
            * sv_norm
            + sw_norm
            + sum(
                coefficient_norm * sigma * sv_norm
                for coefficient_norm in delayed_coefficient_norms
            )
        )
        local_difference = (
            variation.current_coefficient_difference * sv_norm
        )
        for coefficient_norm, coefficient_change, shift_change in zip(
            delayed_coefficient_norms,
            variation.delayed_coefficient_differences,
            delayed_state_shift_changes,
            strict=True,
        ):
            local_difference += (
                coefficient_change * sigma * sv_norm
                + (coefficient_norm + coefficient_change) * shift_change
            )
        state_part = rho * local_center_norm + maximum_period * local_difference

        # Period-column variation.  Dv is controlled through the RFDE
        # equation (variation.derivative_error), not by assuming an X^1 ball.
        period_column_difference = variation.field_difference
        derivative_voltage_norm = _sequence_box_norm_upper(
            base.phase_voltage, precision
        )
        period_terms = zip(
            (base.parameters["tau_0"], base.parameters["tau_1"]),
            delayed_coefficient_norms,
            variation.delayed_coefficient_differences,
            shifted_derivative_changes,
            alpha_changes,
            strict=True,
        )
        for (
            tau,
            coefficient_norm,
            coefficient_change,
            shifted_change,
            alpha_change,
        ) in period_terms:
            alpha_maximum = tau.upper / minimum_period
            period_column_difference += (
                alpha_change
                * coefficient_norm
                * sigma
                * derivative_voltage_norm
                + alpha_maximum
                * (
                    coefficient_change
                    * sigma
                    * derivative_voltage_norm
                    + (coefficient_norm + coefficient_change)
                    * shifted_change
                )
            )
        period_part = st * period_column_difference
        slow_raw = epsilon * rho * sv_norm + st * epsilon * rho
        gain_raw = epsilon * (
            rho * gain_norm + maximum_period * field_change
        )
        raw = state_part + period_part + slow_raw + gain_raw
        return _SensitivityVariationBudget(
            state_part=state_part,
            period_part=period_part,
            slow_part=slow_raw,
            gain_part=gain_raw,
            raw_total=raw,
            preconditioned_total=workspace.global_preconditioner_l1 * raw,
        )


def _midpoint_singular_lower(
    matrix: np.ndarray, precision: int
) -> gmpy2.mpfr:
    entries = [
        DirectedInterval.from_float(float(item), precision)
        for item in np.asarray(matrix, dtype=float).ravel()
    ]
    determinant = entries[0] * entries[3] - entries[1] * entries[2]
    determinant_lower = determinant.lower_abs()
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        frobenius_squared = sum(
            item.upper_abs() * item.upper_abs() for item in entries
        )
        frobenius = gmpy2.sqrt(frobenius_squared)
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        return determinant_lower / frobenius


def _validate_response(
    workspace: _Workspace,
    extrema: DirectedExtremaBox,
) -> DirectedResponseBox:
    precision = workspace.base.period.precision
    midpoint = periodic_response_candidate(workspace.orbit).response_matrix
    midpoint_tuple = (
        (float(midpoint[0, 0]), float(midpoint[0, 1])),
        (float(midpoint[1, 0]), float(midpoint[1, 1])),
    )
    midpoint_lower = _midpoint_singular_lower(midpoint, precision)
    if workspace.inverse_norm is None or not extrema.extrema_validated:
        reason = (
            "D1 did not validate the box"
            if workspace.inverse_norm is None
            else "D3 did not isolate the extrema"
        )
        return DirectedResponseBox(
            control_order=("kappa_1", "kappa_3"),
            output_order=("F", "R_h"),
            sensitivity_error_upper=("nan", "nan"),
            sensitivity_budgets=None,
            response_lower=None,
            response_upper=None,
            midpoint_binary64=midpoint_tuple,
            midpoint_smallest_singular_value_lower=decimal_lower(
                midpoint_lower
            ),
            response_frobenius_radius_upper=None,
            smallest_singular_value_lower=None,
            response_box_validated=False,
            derivative_lipschitz_bound_supplied=False,
            failure_reason=reason,
        )

    variation = _variation_bounds(workspace)
    sensitivities = _floating_sensitivity_sequences(
        workspace.orbit, precision
    )
    errors: list[gmpy2.mpfr] = []
    budget_data: list[
        tuple[
            _PreconditionedResidualBudget,
            _SensitivityVariationBudget,
            gmpy2.mpfr,
        ]
    ] = []
    for control_index, sensitivity in enumerate(sensitivities):
        residual = _sensitivity_residual(
            workspace.base, sensitivity, control_index
        )
        base_budget = _preconditioned_sequence_upper(
            workspace, *residual
        )
        variation_budget = _specific_sensitivity_variation_upper(
            workspace, variation, sensitivity, control_index
        )
        with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
            exact_error = (
                base_budget.total + variation_budget.preconditioned_total
            ) / (1 - workspace.contraction)
            errors.append(exact_error)
            budget_data.append(
                (base_budget, variation_budget, exact_error)
            )

    maximum_phase = DirectedInterval.from_bounds(
        extrema.maximum_phase_lower,
        extrema.maximum_phase_upper,
        precision,
    )
    minimum_phase = DirectedInterval.from_bounds(
        extrema.minimum_phase_lower,
        extrema.minimum_phase_upper,
        precision,
    )
    rho = workspace.chosen_radius.upper
    voltage_maximum = _state_interval(
        workspace.base.voltage, maximum_phase, rho
    )
    voltage_minimum = _state_interval(
        workspace.base.voltage, minimum_phase, rho
    )
    voltage_range = voltage_maximum - voltage_minimum
    period = workspace.base.period + _symmetric_mpfr_interval(rho, precision)
    rows: list[list[DirectedInterval]] = [[], []]
    for sensitivity, error in zip(sensitivities, errors, strict=True):
        sv, _, st = sensitivity
        st_box = st + _symmetric_mpfr_interval(error, precision)
        rows[0].append(-st_box / (period * period))
        maximum_sensitivity = _evaluate_real_sequence(sv, maximum_phase)
        minimum_sensitivity = _evaluate_real_sequence(sv, minimum_phase)
        sensitivity_difference = (
            maximum_sensitivity
            - minimum_sensitivity
            + _symmetric_mpfr_interval(
                (DirectedInterval.from_bounds(error, error, precision) * 2).upper,
                precision,
            )
        )
        rows[1].append(2 * voltage_range * sensitivity_difference)

    radii: list[gmpy2.mpfr] = []
    for row_index in range(2):
        for column_index in range(2):
            center = DirectedInterval.from_float(
                float(midpoint[row_index, column_index]), precision
            )
            radii.append((rows[row_index][column_index] - center).upper_abs())
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        radius = gmpy2.sqrt(sum(item * item for item in radii))
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        beta = midpoint_lower - radius
    positive_range = voltage_range.lower > 0
    validated = beta > 0 and positive_range
    reason = None
    if not positive_range:
        reason = "the directed maximum-minus-minimum interval is not positive"
    elif beta <= 0:
        reason = (
            "directed response radius is not smaller than the midpoint "
            "singular-value lower bound"
        )
    response_lower = (
        (
            decimal_lower(rows[0][0].lower),
            decimal_lower(rows[0][1].lower),
        ),
        (
            decimal_lower(rows[1][0].lower),
            decimal_lower(rows[1][1].lower),
        ),
    )
    response_upper = (
        (
            decimal_upper(rows[0][0].upper),
            decimal_upper(rows[0][1].upper),
        ),
        (
            decimal_upper(rows[1][0].upper),
            decimal_upper(rows[1][1].upper),
        ),
    )
    return DirectedResponseBox(
        control_order=("kappa_1", "kappa_3"),
        output_order=("F", "R_h"),
        sensitivity_error_upper=(
            decimal_upper(errors[0]), decimal_upper(errors[1])
        ),
        sensitivity_budgets=tuple(
            DirectedSensitivityBudget(
                control=control,
                finite_preconditioned_residual_upper=decimal_upper(
                    base_budget.finite_center
                ),
                finite_interval_remainder_upper=decimal_upper(
                    base_budget.finite_interval_remainder
                ),
                analytic_tail_residual_upper=decimal_upper(
                    base_budget.analytic_tail
                ),
                base_preconditioned_residual_upper=decimal_upper(
                    base_budget.total
                ),
                global_preconditioner_l1_upper=decimal_upper(
                    workspace.global_preconditioner_l1
                ),
                state_jacobian_variation_upper=decimal_upper(
                    budget.state_part
                ),
                period_column_variation_upper=decimal_upper(
                    budget.period_part
                ),
                slow_equation_variation_upper=decimal_upper(
                    budget.slow_part
                ),
                gain_forcing_variation_upper=decimal_upper(
                    budget.gain_part
                ),
                raw_variation_upper=decimal_upper(budget.raw_total),
                preconditioned_variation_upper=decimal_upper(
                    budget.preconditioned_total
                ),
                exact_sensitivity_error_upper=decimal_upper(exact_error),
            )
            for control, (base_budget, budget, exact_error) in zip(
                ("kappa_1", "kappa_3"), budget_data, strict=True
            )
        ),
        response_lower=response_lower,
        response_upper=response_upper,
        midpoint_binary64=midpoint_tuple,
        midpoint_smallest_singular_value_lower=decimal_lower(midpoint_lower),
        response_frobenius_radius_upper=decimal_upper(radius),
        smallest_singular_value_lower=decimal_lower(beta),
        response_box_validated=validated,
        derivative_lipschitz_bound_supplied=False,
        failure_reason=reason,
    )


def validate_periodic_parameter_box(
    orbit: PeriodicOrbitCandidate,
    *,
    half_width: str = "1e-10",
    cutoff: int = 144,
    precision: int = 160,
    maximum_radius: str = "5e-8",
    chosen_radius: str = "5e-8",
    phase_partition_count: int = 4096,
) -> DirectedPeriodicParameterBoxValidation:
    """Validate D1, D3, and as much of D4 as directed bounds permit."""

    workspace = _validate_continuation(
        orbit,
        half_width=half_width,
        cutoff=cutoff,
        precision=precision,
        maximum_radius=maximum_radius,
        chosen_radius=chosen_radius,
    )
    extrema = _validate_extrema(
        workspace, partition_count=phase_partition_count
    )
    response = _validate_response(workspace, extrema)
    kappa_1 = workspace.base.parameters["kappa_1"]
    kappa_3 = workspace.base.parameters["kappa_3"]
    gain_box = DirectedGainBox(
        kappa_1_lower=decimal_lower(kappa_1.lower),
        kappa_1_upper=decimal_upper(kappa_1.upper),
        kappa_3_lower=decimal_lower(kappa_3.lower),
        kappa_3_upper=decimal_upper(kappa_3.upper),
        half_width=half_width,
    )
    d1 = workspace.continuation.parameter_box_orbit_validated
    d3 = extrema.extrema_validated
    d4 = response.response_box_validated
    remaining = [
        "directed exclusion of the remaining compact Bloch arc and full Floquet hyperbolicity",
        "a directed Lipschitz bound for the response derivative (second sensitivities)",
        "controlled-separator/reset constants and the final target-ball radius",
    ]
    if not d1:
        remaining.insert(0, "D1 parameter-box radii inequality")
    if not d3:
        remaining.insert(0, "D3 unique-extrema isolation")
    if not d4:
        remaining.insert(0, "D4 positive directed response lower bound")
    return DirectedPeriodicParameterBoxValidation(
        gain_box=gain_box,
        continuation=workspace.continuation,
        extrema=extrema,
        response=response,
        d1_validated=d1,
        d3_validated=d3,
        d4_response_lower_bound_validated=d4,
        all_d1_d3_d4_validated=d1 and d3 and d4,
        issue_15_closed=False,
        remaining_gates=tuple(remaining),
    )
