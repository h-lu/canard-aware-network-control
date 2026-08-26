"""Directed common ``(a,kappa_3)`` boxes for the leaky periodic branches.

This module adapts the already audited leaky finite/tail periodic-orbit
validation to interval unfolding and cubic-gain parameters.  It proves only
what its returned inequalities support: a uniform phase-fixed orbit and
bordered inverse, followed (when successful) by uniform isolation of the two
simple voltage extrema.  It does not enclose first sensitivities or validate
the frequency--amplitude response inverse.
"""

from __future__ import annotations

import ctypes
from dataclasses import dataclass

import gmpy2
import numpy as np

from canard_control.directed_interval import (
    DirectedComplexInterval,
    DirectedInterval,
    decimal_lower,
    decimal_upper,
    pi_interval,
    upward_division,
)
from canard_control.fhn_periodic_candidate import PeriodicOrbitCandidate
from canard_control.fhn_periodic_directed_validation import (
    ComplexSequence,
    _binary_product_defect_upper,
    _constant_sequence,
    _interval_parameters,
    _one,
    _sequence_add,
    _sequence_convolution,
    _sequence_derivative,
    _sequence_neg,
    _sequence_scale,
    _sequence_shift,
    _sequence_sub,
    directed_dft,
)
from canard_control.fhn_periodic_infinite_validation import (
    _BaseSequences,
    _binary_matvec_l1_upper,
    _float_matrix_l1_upper,
    _residual_vector,
    _sequence_box_norm_upper,
    _tail_from_finite_upper,
    _tail_residual_upper,
)
from canard_control.leaky_periodic_validation import (
    _leaky_finite_coefficient_matrix,
    _leaky_finite_from_tail_upper,
    _leaky_nonlinear_coefficients,
    _leaky_tail_to_tail_upper,
)


@dataclass(frozen=True)
class DirectedLeakyParameterBoxContinuation:
    """Uniform radii result for one leaky branch."""

    branch: str
    half_width_unfolding_a: str
    half_width_kappa_3: str
    unfolding_a_lower: str
    unfolding_a_upper: str
    kappa_3_lower: str
    kappa_3_upper: str
    cutoff: int
    precision_bits: int
    real_conjugate_dimension: int
    approximate_inverse_l1_upper: str
    analytic_tail_inverse_l1_upper: str
    global_preconditioner_l1_upper: str
    finite_inverse_defect_upper: str
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
class DirectedLeakyExtremaBox:
    """Uniform directed isolation of one maximum and one minimum."""

    phase_partition_count: int
    maximum_phase_lower: str | None
    maximum_phase_upper: str | None
    minimum_phase_lower: str | None
    minimum_phase_upper: str | None
    maximum_curvature_window_lower: str | None
    maximum_curvature_window_upper: str | None
    minimum_curvature_window_lower: str | None
    minimum_curvature_window_upper: str | None
    maximum_curvature_upper: str | None
    minimum_curvature_lower: str | None
    complement_derivative_gap_lower: str | None
    derivative_error_upper: str | None
    all_complement_cells_strict: bool
    extrema_validated: bool
    failure_reason: str | None


@dataclass(frozen=True)
class DirectedLeakyParameterBoxValidation:
    """Combined orbit and extrema gates for one branch."""

    continuation: DirectedLeakyParameterBoxContinuation
    extrema: DirectedLeakyExtremaBox
    uniform_orbit_and_bordered_inverse_validated: bool
    uniform_simple_extrema_validated: bool
    exact_response_derivative_enclosed: bool
    frequency_amplitude_local_inverse_validated: bool
    remaining_gates: tuple[str, ...]


@dataclass
class _Workspace:
    orbit: PeriodicOrbitCandidate
    base: _BaseSequences
    approximate_inverse: np.ndarray
    approximate_inverse_l1: gmpy2.mpfr
    global_preconditioner_l1: gmpy2.mpfr
    chosen_radius: DirectedInterval
    contraction: gmpy2.mpfr
    inverse_norm: gmpy2.mpfr | None
    continuation: DirectedLeakyParameterBoxContinuation


@dataclass(frozen=True)
class _VariationBounds:
    derivative_error: gmpy2.mpfr
    field_difference: gmpy2.mpfr
    cubic_field_difference: gmpy2.mpfr
    current_coefficient_difference: gmpy2.mpfr
    delayed_coefficient_differences: tuple[gmpy2.mpfr, gmpy2.mpfr]


def _symmetric_mpfr_interval(
    radius: gmpy2.mpfr, precision: int
) -> DirectedInterval:
    positive = DirectedInterval.from_bounds(radius, radius, precision)
    if positive.lower < 0:
        raise ValueError("symmetric radius must be nonnegative")
    negative = -positive
    return DirectedInterval.from_bounds(
        negative.lower, positive.upper, precision
    )


def _symmetric_decimal_interval(
    center: float, radius: str, precision: int
) -> DirectedInterval:
    point = DirectedInterval.from_decimal(str(float(center)), precision)
    width = DirectedInterval.from_decimal(radius, precision)
    if width.lower < 0:
        raise ValueError("parameter half-width must be nonnegative")
    return point + _symmetric_mpfr_interval(width.upper, precision)


def _build_leaky_parameter_box_sequences(
    orbit: PeriodicOrbitCandidate,
    precision: int,
    half_width_unfolding_a: str,
    half_width_kappa_3: str,
) -> _BaseSequences:
    """Build the leaky residual and bordered derivative over the box."""

    parameters = _interval_parameters(orbit.parameters, precision)
    parameters["unfolding"] = _symmetric_decimal_interval(
        orbit.parameters.unfolding, half_width_unfolding_a, precision
    )
    parameters["kappa_3"] = _symmetric_decimal_interval(
        orbit.parameters.kappa_3, half_width_kappa_3, precision
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
        _sequence_sub(_sequence_sub(voltage, unfolding), recovery),
        epsilon,
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
    branch: str,
    half_width_unfolding_a: str,
    half_width_kappa_3: str,
    cutoff: int,
    precision: int,
    maximum_radius: str,
    chosen_radius: str,
) -> _Workspace:
    if branch not in {"inner_saddle_candidate", "outer_pulse"}:
        raise ValueError("unknown leaky periodic branch")
    if cutoff < 3 * ((len(orbit.state) - 1) // 2):
        raise ValueError("cutoff must contain the cubic residual support")
    base = _build_leaky_parameter_box_sequences(
        orbit,
        precision,
        half_width_unfolding_a,
        half_width_kappa_3,
    )
    if base.parameters["kappa_3"].lower < 0:
        raise ValueError("the cubic-gain box must remain nonnegative")

    real_matrix, matrix_distance, layout = (
        _leaky_finite_coefficient_matrix(base, cutoff)
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
    finite_from_tail = _leaky_finite_from_tail_upper(
        base, layout, approximate_inverse, approximate_inverse_l1
    )
    tail_to_tail = _leaky_tail_to_tail_upper(base, cutoff)
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        finite_input = finite_defect + tail_from_finite
        tail_input = finite_from_tail + tail_to_tail
        full_defect = max(finite_input, tail_input)

    z1, z2, z3 = _leaky_nonlinear_coefficients(
        base, cutoff, approximate_inverse_l1, maximum_radius
    )
    radius = DirectedInterval.from_decimal(chosen_radius, precision)
    maximum = DirectedInterval.from_decimal(maximum_radius, precision)
    if radius.upper > maximum.upper:
        raise ValueError("chosen radius exceeds coefficient-bound radius")
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

    continuation = DirectedLeakyParameterBoxContinuation(
        branch=branch,
        half_width_unfolding_a=half_width_unfolding_a,
        half_width_kappa_3=half_width_kappa_3,
        unfolding_a_lower=decimal_lower(
            base.parameters["unfolding"].lower
        ),
        unfolding_a_upper=decimal_upper(
            base.parameters["unfolding"].upper
        ),
        kappa_3_lower=decimal_lower(base.parameters["kappa_3"].lower),
        kappa_3_upper=decimal_upper(base.parameters["kappa_3"].upper),
        cutoff=cutoff,
        precision_bits=precision,
        real_conjugate_dimension=layout.dimension,
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
        approximate_inverse=approximate_inverse,
        approximate_inverse_l1=approximate_inverse_l1,
        global_preconditioner_l1=global_preconditioner_l1,
        chosen_radius=radius,
        contraction=contraction,
        inverse_norm=inverse_norm,
        continuation=continuation,
    )


def _candidate_fields(
    base: _BaseSequences,
) -> tuple[ComplexSequence, tuple[ComplexSequence, ComplexSequence]]:
    precision = base.period.precision
    one = _constant_sequence(_one(precision), precision)
    shifted = tuple(
        _sequence_shift(base.voltage, tau / base.period)
        for tau in (base.parameters["tau_0"], base.parameters["tau_1"])
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
    return cubic, (shifted[0], shifted[1])


def _variation_bounds(workspace: _Workspace) -> _VariationBounds:
    """Raw Wiener bounds for voltage derivatives over the parameter box."""

    base = workspace.base
    precision = base.period.precision
    rho = workspace.chosen_radius.upper
    epsilon = base.parameters["epsilon"].upper
    kappa_1 = base.parameters["kappa_1"].upper
    kappa_3_max = base.parameters["kappa_3"].upper
    center_kappa_3 = DirectedInterval.from_decimal(
        str(float(workspace.orbit.parameters.kappa_3)), precision
    )
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
    cubic, shifted = _candidate_fields(base)
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
            * (3 * norm * norm + 3 * norm * delta + delta * delta)
            for delta, norm in zip(
                shifted_differences, shifted_centered_norms, strict=True
            )
        )
        cubic_difference = (
            (shifted_cubic_differences[0] + shifted_cubic_differences[1])
            / 2
            + local_cubic_difference
        )
        local_field_difference = 2 * rho + rho * (
            voltage_norm * voltage_norm
            + voltage_norm * rho
            + rho * rho / 3
        )
        field_difference = (
            local_field_difference
            + epsilon * kappa_1 * linear_difference
            + epsilon
            * (kappa_3_max * cubic_difference + h3 * cubic_norm)
        )
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
            * 3
            * (
                kappa_3_max * delta * (2 * norm + delta)
                + h3 * norm * norm
            )
            for delta, norm in zip(
                shifted_differences, shifted_centered_norms, strict=True
            )
        )
    return _VariationBounds(
        derivative_error=derivative_error,
        field_difference=field_difference,
        cubic_field_difference=cubic_difference,
        current_coefficient_difference=current_difference,
        delayed_coefficient_differences=(
            delayed_coefficient_differences[0],
            delayed_coefficient_differences[1],
        ),
    )


def _evaluate_real_sequence(
    sequence: dict[int, DirectedComplexInterval],
    phase: DirectedInterval,
) -> DirectedInterval:
    from canard_control.directed_interval import complex_unit_interval

    precision = phase.precision
    result = DirectedInterval.from_decimal(0, precision)
    two_pi = pi_interval(precision) * 2
    for mode, coefficient in sequence.items():
        exponential = complex_unit_interval(two_pi * mode * phase)
        result += (coefficient * exponential).real
    return result


def _state_interval(
    sequence: dict[int, DirectedComplexInterval],
    phase: DirectedInterval,
    radius: gmpy2.mpfr,
) -> DirectedInterval:
    return _evaluate_real_sequence(sequence, phase) + _symmetric_mpfr_interval(
        radius, phase.precision
    )


def _vprime_interval(
    workspace: _Workspace,
    variation: _VariationBounds,
    phase: DirectedInterval,
) -> DirectedInterval:
    center = _evaluate_real_sequence(workspace.base.phase_voltage, phase)
    return center + _symmetric_mpfr_interval(
        variation.derivative_error, phase.precision
    )


def _vsecond_interval(
    workspace: _Workspace,
    variation: _VariationBounds,
    phase: DirectedInterval,
) -> DirectedInterval:
    """Evaluate ``V''`` from the leaky RFDE on one phase window."""

    base = workspace.base
    precision = phase.precision
    rho = workspace.chosen_radius.upper
    period = base.period + _symmetric_mpfr_interval(rho, precision)
    epsilon = base.parameters["epsilon"]
    kappa_1 = base.parameters["kappa_1"]
    kappa_3 = base.parameters["kappa_3"]
    one = DirectedInterval.from_decimal(1, precision)
    voltage = _state_interval(base.voltage, phase, rho)
    recovery = _state_interval(base.recovery, phase, rho)
    voltage_prime = _vprime_interval(workspace, variation, phase)
    recovery_prime = period * epsilon * (
        voltage - base.parameters["unfolding"] - recovery
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


def _empty_extrema(
    partition_count: int, reason: str
) -> DirectedLeakyExtremaBox:
    return DirectedLeakyExtremaBox(
        phase_partition_count=partition_count,
        maximum_phase_lower=None,
        maximum_phase_upper=None,
        minimum_phase_lower=None,
        minimum_phase_upper=None,
        maximum_curvature_window_lower=None,
        maximum_curvature_window_upper=None,
        minimum_curvature_window_lower=None,
        minimum_curvature_window_upper=None,
        maximum_curvature_upper=None,
        minimum_curvature_lower=None,
        complement_derivative_gap_lower=None,
        derivative_error_upper=None,
        all_complement_cells_strict=False,
        extrema_validated=False,
        failure_reason=reason,
    )


def _floating_extrema_phases(orbit: PeriodicOrbitCandidate) -> tuple[float, float]:
    from canard_control.fhn_periodic_candidate import voltage_extrema_candidate

    extrema = voltage_extrema_candidate(orbit, scan_factor=32)
    if not extrema.unique_maximum_and_minimum_candidate:
        raise RuntimeError("center polynomial does not have two simple extrema")
    return extrema.maximum_phase, extrema.minimum_phase


def _validate_extrema(
    workspace: _Workspace,
    *,
    partition_count: int,
) -> DirectedLeakyExtremaBox:
    if workspace.inverse_norm is None:
        return _empty_extrema(
            partition_count, "the parameter-box radii inequality did not close"
        )
    if partition_count < 512:
        raise ValueError("phase partition must contain at least 512 cells")
    precision = workspace.base.period.precision
    variation = _variation_bounds(workspace)
    roots = _floating_extrema_phases(workspace.orbit)
    # The outer relaxation orbit has large third derivatives near its sharp
    # jumps.  Three cells on either side at the registered 4096-cell
    # partition include every phase cell whose derivative enclosure meets
    # zero, while retaining strict curvature signs on both windows.
    half_window_cells = max(3, partition_count // 8192)
    denominator = DirectedInterval.from_decimal(partition_count, precision)
    windows: list[tuple[int, int, DirectedInterval]] = []
    for root in roots:
        center_index = int(np.floor(root * partition_count))
        left_index = center_index - half_window_cells
        right_index = center_index + half_window_cells + 1
        if left_index <= 0 or right_index >= partition_count:
            raise RuntimeError("extremum window crosses the phase cut")
        left = DirectedInterval.from_decimal(left_index, precision) / denominator
        right = (
            DirectedInterval.from_decimal(right_index, precision) / denominator
        )
        windows.append(
            (
                left_index,
                right_index,
                DirectedInterval.from_bounds(
                    left.lower, right.upper, precision
                ),
            )
        )

    occupied: set[int] = set()
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
        complement_gap = (
            gap if complement_gap is None else min(complement_gap, gap)
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
    failures = []
    if not complement_strict:
        failures.append("a complementary phase cell contains zero in V'")
    if not maximum_ok:
        failures.append("maximum window failed endpoint signs or curvature")
    if not minimum_ok:
        failures.append("minimum window failed endpoint signs or curvature")
    return DirectedLeakyExtremaBox(
        phase_partition_count=partition_count,
        maximum_phase_lower=decimal_lower(windows[0][2].lower),
        maximum_phase_upper=decimal_upper(windows[0][2].upper),
        minimum_phase_lower=decimal_lower(windows[1][2].lower),
        minimum_phase_upper=decimal_upper(windows[1][2].upper),
        maximum_curvature_window_lower=decimal_lower(windows[0][2].lower),
        maximum_curvature_window_upper=decimal_upper(windows[0][2].upper),
        minimum_curvature_window_lower=decimal_lower(windows[1][2].lower),
        minimum_curvature_window_upper=decimal_upper(windows[1][2].upper),
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
        failure_reason="; ".join(failures) if failures else None,
    )


def validate_leaky_parameter_box(
    orbit: PeriodicOrbitCandidate,
    *,
    branch: str,
    half_width_unfolding_a: str = "1e-10",
    half_width_kappa_3: str = "1e-10",
    cutoff: int = 192,
    precision: int = 160,
    maximum_radius: str = "1e-5",
    chosen_radius: str = "1e-5",
    phase_partition_count: int = 4096,
) -> DirectedLeakyParameterBoxValidation:
    """Validate a uniform orbit/bordered inverse and simple extrema."""

    workspace = _validate_continuation(
        orbit,
        branch=branch,
        half_width_unfolding_a=half_width_unfolding_a,
        half_width_kappa_3=half_width_kappa_3,
        cutoff=cutoff,
        precision=precision,
        maximum_radius=maximum_radius,
        chosen_radius=chosen_radius,
    )
    extrema = _validate_extrema(
        workspace, partition_count=phase_partition_count
    )
    orbit_gate = workspace.continuation.parameter_box_orbit_validated
    remaining = [
        "directed first-sensitivity error bounds in the (a,kappa_3) columns",
        "a directed nonzero lower bound for D_(a,kappa_3)(F,A)",
        "a Lipschitz bound for the response derivative for a target radius",
    ]
    if not orbit_gate:
        remaining.insert(0, "uniform parameter-box radii inequality")
    if not extrema.extrema_validated:
        remaining.insert(0, "uniform simple-extrema isolation")
    return DirectedLeakyParameterBoxValidation(
        continuation=workspace.continuation,
        extrema=extrema,
        uniform_orbit_and_bordered_inverse_validated=orbit_gate,
        uniform_simple_extrema_validated=extrema.extrema_validated,
        exact_response_derivative_enclosed=False,
        frequency_amplitude_local_inverse_validated=False,
        remaining_gates=tuple(remaining),
    )


__all__ = [
    "DirectedLeakyExtremaBox",
    "DirectedLeakyParameterBoxContinuation",
    "DirectedLeakyParameterBoxValidation",
    "validate_leaky_parameter_box",
]
