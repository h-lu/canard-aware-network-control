"""Branch-neutral full-operator cells for leaky Floquet compact covers.

This module contains no theorem flags, parent hashes, branch identity, or
adaptive-cover policy.  It evaluates one leaky logarithmic Floquet pencil
cell from a caller-supplied candidate and orbit ball.  The physical main
representation uses an unshifted delayed coefficient and an output-mode
phase.  A shifted-coefficient/input-column helper remains available for the
independent equivalence oracle.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, localcontext
from fractions import Fraction
from hashlib import sha256
import math
from typing import Any, Mapping, Sequence

import gmpy2
import numpy as np

from canard_control.directed_interval import (
    DirectedComplexInterval,
    DirectedInterval,
    complex_unit_interval,
    decimal_upper,
    pi_interval,
    upward_sum,
)
from canard_control.fhn_periodic_infinite_validation import (
    _sequence_box_norm_upper,
)
from canard_control.floquet_cover_arithmetic import (
    _binary_complex_matrix_split_l1_upper,
    _binary_complex_max_split_upper,
    _binary_complex_product_split_l1_upper,
    _binary_complex_split_upper,
    _box_distance_split_upper,
    _coefficient_matrix,
    _formation_error,
    _rotation_data,
    _up,
)


@dataclass(frozen=True)
class CoverLeaf:
    root_id: str
    path: str
    proof_kind: str
    contraction_upper: str
    finite_input_column_sum_upper: str
    tail_input_column_sum_upper: str


@dataclass(frozen=True)
class WorstCoverCell:
    root_id: str
    path: str
    sigma_lower: str
    sigma_center_binary64: str
    sigma_upper: str
    phase_lower: str
    phase_center_binary64: str
    phase_upper: str
    split_parameter_radius_upper: str
    finite_inverse_l1_upper: str
    finite_inverse_defect_upper: str
    finite_first_product_upper: str
    finite_from_tail_center_upper: str
    finite_from_tail_first_upper: str
    tail_from_finite_center_upper: str
    tail_from_finite_first_upper: str
    fast_tail_diagonal_inverse_split_upper: str
    slow_tail_diagonal_inverse_split_upper: str
    finite_full_orbit_correction_upper: str
    finite_convolution_orbit_correction_upper: str
    finite_tail_convolution_orbit_correction_upper: str
    tail_from_finite_orbit_correction_upper: str
    finite_to_finite_upper: str
    finite_from_tail_upper: str
    tail_from_finite_upper: str
    tail_to_tail_voltage_input_upper: str
    tail_to_tail_recovery_input_upper: str
    tail_to_tail_upper: str
    finite_input_column_sum_upper: str
    tail_input_column_sum_upper: str
    contraction_upper: str
    contraction_margin_lower: str


@dataclass(frozen=True)
class BinaryCandidate:
    modes: np.ndarray
    tail_modes: np.ndarray
    current_finite: np.ndarray
    delayed_finite: np.ndarray
    current_finite_tail: np.ndarray
    delayed_finite_tail: np.ndarray
    current_tail_finite: np.ndarray
    delayed_tail_finite: np.ndarray
    current_coefficients: Mapping[int, complex]
    delayed_coefficients: Mapping[int, complex]
    current_error_norm: gmpy2.mpfr
    delayed_error_norm: gmpy2.mpfr
    current_binary_norm: gmpy2.mpfr
    delayed_binary_norm: gmpy2.mpfr
    finite_mode_rotations: tuple[np.ndarray, np.ndarray]
    tail_mode_rotations: tuple[np.ndarray, np.ndarray]
    finite_mode_rotation_split: tuple[gmpy2.mpfr, gmpy2.mpfr]
    tail_mode_rotation_split: tuple[gmpy2.mpfr, gmpy2.mpfr]
    finite_mode_rotation_error: tuple[gmpy2.mpfr, gmpy2.mpfr]
    tail_mode_rotation_error: tuple[gmpy2.mpfr, gmpy2.mpfr]
    finite_mode_binary_split: tuple[gmpy2.mpfr, gmpy2.mpfr]
    tail_mode_binary_split: tuple[gmpy2.mpfr, gmpy2.mpfr]


@dataclass(frozen=True)
class Rectangle:
    root_id: str
    path: str
    sigma_lower: Decimal
    sigma_upper: Decimal
    phase_lower: Decimal
    phase_upper: Decimal


@dataclass(frozen=True)
class CellBounds:
    leaf: CoverLeaf
    worst: WorstCoverCell
    validated: bool


def _exact_decimal_sum(values: Sequence[str]) -> str:
    with localcontext() as context:
        context.prec = max(160, sum(len(value) for value in values) + 10)
        total = sum((Decimal(value) for value in values), Decimal(0))
    return format(total, "f")


def _margin(value: str) -> str:
    with localcontext() as context:
        context.prec = max(160, len(value) + 10)
        return format(Decimal(1) - Decimal(value), "f")


def _center_and_radius(
    rectangle: Rectangle,
    precision: int,
) -> tuple[DirectedInterval, DirectedInterval, gmpy2.mpfr, str, str]:
    with localcontext() as context:
        context.prec = 120
        sigma_decimal = (rectangle.sigma_lower + rectangle.sigma_upper) / 2
        phase_decimal = (rectangle.phase_lower + rectangle.phase_upper) / 2
    sigma_float = float(sigma_decimal)
    phase_float = float(phase_decimal)
    sigma = DirectedInterval.from_float(sigma_float, precision)
    phase = DirectedInterval.from_float(phase_float, precision)
    sigma_lower = DirectedInterval.from_decimal(
        format(rectangle.sigma_lower, "f"), precision
    )
    sigma_upper = DirectedInterval.from_decimal(
        format(rectangle.sigma_upper, "f"), precision
    )
    phase_lower = DirectedInterval.from_decimal(
        format(rectangle.phase_lower, "f"), precision
    )
    phase_upper = DirectedInterval.from_decimal(
        format(rectangle.phase_upper, "f"), precision
    )
    if sigma.lower < sigma_lower.lower or sigma.upper > sigma_upper.upper:
        raise ArithmeticError("the binary sigma centre escaped its rectangle")
    if phase.lower < phase_lower.lower or phase.upper > phase_upper.upper:
        raise ArithmeticError("the binary phase centre escaped its rectangle")
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        delta_sigma = max(
            sigma.upper - sigma_lower.lower,
            sigma_upper.upper - sigma.lower,
        )
        delta_phase = max(
            phase.upper - phase_lower.lower,
            phase_upper.upper - phase.lower,
        )
        radius = delta_sigma + delta_phase
    return (
        sigma,
        phase,
        radius,
        format(sigma_float, ".17g"),
        format(phase_float, ".17g"),
    )


def mode_rotation_basis(
    requested_modes: np.ndarray,
    base: Any,
    precision: int,
) -> tuple[
    tuple[np.ndarray, np.ndarray],
    tuple[gmpy2.mpfr, gmpy2.mpfr],
    tuple[gmpy2.mpfr, gmpy2.mpfr],
    tuple[gmpy2.mpfr, gmpy2.mpfr],
]:
    arrays: list[np.ndarray] = []
    split_bounds: list[gmpy2.mpfr] = []
    error_bounds: list[gmpy2.mpfr] = []
    binary_bounds: list[gmpy2.mpfr] = []
    for tau in (base.parameters["tau_0"], base.parameters["tau_1"]):
        alpha_float = float(tau.lower) / float(base.period.lower)
        stored_values = np.asarray(
            [
                np.exp(-2.0j * math.pi * int(mode) * alpha_float)
                for mode in requested_modes
            ],
            dtype=complex,
        )
        arrays.append(stored_values)
        split = _up(0, precision)
        error = _up(0, precision)
        binary_split = _up(0, precision)
        alpha = tau / base.period
        for mode, stored in zip(
            requested_modes, stored_values, strict=True
        ):
            exact = complex_unit_interval(
                -(pi_interval(precision) * (2 * int(mode)) * alpha)
            )
            split = max(
                split,
                upward_sum(
                    (exact.real.upper_abs(), exact.imag.upper_abs()),
                    precision,
                ),
            )
            error = max(
                error, _box_distance_split_upper(exact, complex(stored))
            )
            binary_split = max(
                binary_split,
                _binary_complex_split_upper(complex(stored), precision),
            )
        split_bounds.append(split)
        error_bounds.append(error)
        binary_bounds.append(binary_split)
    return (
        (arrays[0], arrays[1]),
        (split_bounds[0], split_bounds[1]),
        (error_bounds[0], error_bounds[1]),
        (binary_bounds[0], binary_bounds[1]),
    )


def input_rotated_convolution(
    coefficient_matrix: np.ndarray,
    input_rotations: np.ndarray,
) -> np.ndarray:
    """Apply one delay phase to input Fourier columns."""

    matrix = np.asarray(coefficient_matrix, dtype=complex)
    rotations = np.asarray(input_rotations, dtype=complex)
    if matrix.ndim != 2 or rotations.shape != (matrix.shape[1],):
        raise ValueError("delay rotations must index convolution input modes")
    return matrix * rotations[None, :]


def output_rotated_convolution(
    coefficient_matrix: np.ndarray,
    output_rotations: np.ndarray,
) -> np.ndarray:
    """Apply the physical delay phase to convolution output rows."""

    matrix = np.asarray(coefficient_matrix, dtype=complex)
    rotations = np.asarray(output_rotations, dtype=complex)
    if matrix.ndim != 2 or rotations.shape != (matrix.shape[0],):
        raise ValueError("delay rotations must index convolution output modes")
    return rotations[:, None] * matrix


def candidate_matrices(
    candidate: BinaryCandidate,
    base: Any,
    sigma: DirectedInterval,
    phase: DirectedInterval,
    precision: int,
) -> tuple[
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
    dict[str, gmpy2.mpfr],
]:
    modes = candidate.modes
    tail_modes = candidate.tail_modes
    period = float(base.period.lower)
    epsilon = float(base.parameters["epsilon"].lower)
    taus = (
        float(base.parameters["tau_0"].lower),
        float(base.parameters["tau_1"].lower),
    )
    finite_rotations, finite_rotation_split, finite_rotation_error = (
        _rotation_data(
            candidate.finite_mode_rotations,
            candidate.finite_mode_rotation_split,
            candidate.finite_mode_rotation_error,
            candidate.finite_mode_binary_split,
            sigma,
            phase,
            base,
            precision,
        )
    )
    tail_rotations, tail_rotation_split, tail_rotation_error = _rotation_data(
        candidate.tail_mode_rotations,
        candidate.tail_mode_rotation_split,
        candidate.tail_mode_rotation_error,
        candidate.tail_mode_binary_split,
        sigma,
        phase,
        base,
        precision,
    )
    sigma_float = float(sigma.lower)
    phase_float = float(phase.lower)
    finite_frequency = sigma_float + 1.0j * (
        phase_float + 2.0 * math.pi * modes
    )
    top = np.diag(finite_frequency) - period * candidate.current_finite
    derivative_top = np.eye(len(modes), dtype=complex)
    for tau, rotation in zip(taus, finite_rotations, strict=True):
        rotated = output_rotated_convolution(
            candidate.delayed_finite, rotation
        )
        top -= period * rotated
        derivative_top += tau * rotated
    identity = np.eye(len(modes), dtype=complex)
    zero = np.zeros_like(identity)
    finite = np.block(
        [
            [top, period * identity],
            [
                -period * epsilon * identity,
                np.diag(finite_frequency + period * epsilon),
            ],
        ]
    )
    derivative = np.block([[derivative_top, zero], [zero, identity]])

    finite_tail_top = -period * candidate.current_finite_tail
    finite_tail_derivative_top = np.zeros_like(finite_tail_top)
    for tau, rotation in zip(taus, finite_rotations, strict=True):
        rotated = output_rotated_convolution(
            candidate.delayed_finite_tail, rotation
        )
        finite_tail_top -= period * rotated
        finite_tail_derivative_top += tau * rotated
    finite_tail = np.vstack(
        (finite_tail_top, np.zeros_like(finite_tail_top))
    )
    finite_tail_derivative = np.vstack(
        (finite_tail_derivative_top, np.zeros_like(finite_tail_derivative_top))
    )

    tail_finite = -period * candidate.current_tail_finite
    tail_finite_derivative = np.zeros_like(tail_finite)
    for tau, rotation in zip(taus, tail_rotations, strict=True):
        rotated = output_rotated_convolution(
            candidate.delayed_tail_finite, rotation
        )
        tail_finite -= period * rotated
        tail_finite_derivative += tau * rotated

    current_exact = _sequence_box_norm_upper(
        base.current_coefficient, precision
    )
    delayed_exact = _sequence_box_norm_upper(
        base.delayed_state_derivative, precision
    )
    maximum_frequency = _up(0, precision)
    maximum_diagonal_error = _up(0, precision)
    for mode, stored in zip(modes, finite_frequency, strict=True):
        exact = DirectedComplexInterval(
            sigma,
            pi_interval(precision) * (2 * int(mode)) + phase,
        )
        maximum_frequency = max(
            maximum_frequency,
            upward_sum(
                (exact.real.upper_abs(), exact.imag.upper_abs()), precision
            ),
        )
        maximum_diagonal_error = max(
            maximum_diagonal_error,
            _box_distance_split_upper(exact, complex(stored)),
        )
    exact_period = DirectedComplexInterval.from_real(base.period)
    exact_period_epsilon = DirectedComplexInterval.from_real(
        base.period * base.parameters["epsilon"]
    )
    period_error = _box_distance_split_upper(
        exact_period, complex(period, 0.0)
    )
    period_epsilon_error = _box_distance_split_upper(
        exact_period_epsilon, complex(period * epsilon, 0.0)
    )
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        finite_conv_error = base.period.upper * (
            candidate.current_error_norm
            + 2
            * (
                finite_rotation_split * candidate.delayed_error_norm
                + finite_rotation_error * candidate.delayed_binary_norm
            )
        )
        finite_derivative_error = (
            base.parameters["tau_0"].upper
            + base.parameters["tau_1"].upper
        ) * (
            finite_rotation_split * candidate.delayed_error_norm
            + finite_rotation_error * candidate.delayed_binary_norm
        )
        tail_conv_error = base.period.upper * (
            candidate.current_error_norm
            + 2
            * (
                tail_rotation_split * candidate.delayed_error_norm
                + tail_rotation_error * candidate.delayed_binary_norm
            )
        )
        tail_derivative_error = (
            base.parameters["tau_0"].upper
            + base.parameters["tau_1"].upper
        ) * (
            tail_rotation_split * candidate.delayed_error_norm
            + tail_rotation_error * candidate.delayed_binary_norm
        )
        finite_scale = max(
            maximum_frequency
            + base.period.upper
            * (current_exact + 2 * finite_rotation_split * delayed_exact)
            + base.period.upper,
            maximum_frequency
            + 2 * base.period.upper * base.parameters["epsilon"].upper,
        )
        derivative_scale = max(
            1
            + (
                base.parameters["tau_0"].upper
                + base.parameters["tau_1"].upper
            )
            * finite_rotation_split
            * delayed_exact,
            gmpy2.mpfr(1),
        )
        finite_conv_scale = base.period.upper * (
            current_exact + 2 * finite_rotation_split * delayed_exact
        )
        finite_derivative_conv_scale = (
            base.parameters["tau_0"].upper
            + base.parameters["tau_1"].upper
        ) * finite_rotation_split * delayed_exact
        tail_conv_scale = base.period.upper * (
            current_exact + 2 * tail_rotation_split * delayed_exact
        )
        tail_derivative_conv_scale = (
            base.parameters["tau_0"].upper
            + base.parameters["tau_1"].upper
        ) * tail_rotation_split * delayed_exact
        finite_model_error = max(
            maximum_diagonal_error
            + finite_conv_error
            + period_epsilon_error,
            period_error + maximum_diagonal_error + period_epsilon_error,
        )
        finite_error = finite_model_error + _formation_error(
            finite_scale, 2 * len(modes), precision
        )
        derivative_error = finite_derivative_error + _formation_error(
            derivative_scale, 2 * len(modes), precision
        )
        finite_tail_error = finite_conv_error + _formation_error(
            finite_conv_scale, 2 * len(modes), precision
        )
        finite_tail_derivative_error = (
            finite_derivative_error
            + _formation_error(
                finite_derivative_conv_scale, 2 * len(modes), precision
            )
        )
        tail_finite_error = tail_conv_error + _formation_error(
            tail_conv_scale, len(tail_modes), precision
        )
        tail_finite_derivative_error = (
            tail_derivative_error
            + _formation_error(
                tail_derivative_conv_scale, len(tail_modes), precision
            )
        )
    return (
        finite,
        derivative,
        finite_tail,
        finite_tail_derivative,
        tail_finite,
        tail_finite_derivative,
        {
            "finite": finite_error,
            "derivative": derivative_error,
            "finite_tail": finite_tail_error,
            "finite_tail_derivative": finite_tail_derivative_error,
            "tail_finite": tail_finite_error,
            "tail_finite_derivative": tail_finite_derivative_error,
        },
    )


def _inverse_diagonal_interval(
    mode: int,
    sigma: DirectedInterval,
    phase: DirectedInterval,
    real_shift: DirectedInterval,
) -> DirectedComplexInterval:
    real = sigma + real_shift
    omega = pi_interval(sigma.precision) * (2 * mode) + phase
    denominator = real * real + omega * omega
    return DirectedComplexInterval(real / denominator, -omega / denominator)


def _tail_inverse_bounds(
    sigma: DirectedInterval,
    phase: DirectedInterval,
    base: Any,
    finite_cutoff: int,
    precision: int,
) -> tuple[gmpy2.mpfr, gmpy2.mpfr]:
    zero = DirectedInterval.from_decimal(0, precision)
    slow_shift = base.period * base.parameters["epsilon"]
    edge_modes = (-(finite_cutoff + 1), finite_cutoff + 1)
    fast = tuple(
        _inverse_diagonal_interval(mode, sigma, phase, zero)
        for mode in edge_modes
    )
    slow = tuple(
        _inverse_diagonal_interval(mode, sigma, phase, slow_shift)
        for mode in edge_modes
    )
    fast_bound = max(
        upward_sum((value.real.upper_abs(), value.imag.upper_abs()), precision)
        for value in fast
    )
    slow_bound = max(
        upward_sum((value.real.upper_abs(), value.imag.upper_abs()), precision)
        for value in slow
    )
    return fast_bound, slow_bound


def _orbit_corrections(
    base: Any,
    correction_radius: DirectedInterval,
    rectangle: Rectangle,
    fast_tail_inverse: gmpy2.mpfr,
    finite_cutoff: int,
    precision: int,
) -> tuple[
    gmpy2.mpfr,
    gmpy2.mpfr,
    gmpy2.mpfr,
    gmpy2.mpfr,
    dict[str, gmpy2.mpfr],
]:
    r = correction_radius.upper
    current_center = _sequence_box_norm_upper(
        base.current_coefficient, precision
    )
    delayed_center = _sequence_box_norm_upper(
        base.delayed_state_derivative, precision
    )
    voltage = _sequence_box_norm_upper(base.voltage, precision)
    centered = _sequence_box_norm_upper(base.centered_voltage, precision)
    epsilon = base.parameters["epsilon"].upper
    kappa_3 = base.parameters["kappa_3"].upper
    sqrt_two = DirectedInterval.from_decimal(2, precision).sqrt().upper
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        current_variation = (
            (2 * voltage + r) * r
            + 3 * epsilon * kappa_3 * (2 * centered + r) * r
        )
        delayed_variation = (
            3 * epsilon * kappa_3 * (2 * centered + r) * r / 2
        )
        current_uniform = current_center + current_variation
        delayed_uniform = delayed_center + delayed_variation
        period_upper = base.period.upper + r
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        period_lower = base.period.lower - r
    if period_lower <= 0:
        raise ArithmeticError("the orbit correction crosses zero period")
    sigma_box = DirectedInterval.from_decimal(
        format(rectangle.sigma_upper, "f"), precision
    )
    phase_abs = max(abs(rectangle.phase_lower), abs(rectangle.phase_upper))
    phase_box = DirectedInterval.from_decimal(format(phase_abs, "f"), precision)
    finite_output_frequency = (
        sigma_box * sigma_box
        + (pi_interval(precision) * (2 * finite_cutoff) + phase_box) ** 2
    ).sqrt().upper
    _, _, spectral_radius, _, _ = _center_and_radius(rectangle, precision)
    finite_delay_terms: list[gmpy2.mpfr] = []
    preconditioned_tail_delay_terms: list[gmpy2.mpfr] = []
    for tau in (base.parameters["tau_0"], base.parameters["tau_1"]):
        with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
            common = (
                r * delayed_uniform
                + base.period.upper * delayed_variation
            )
            phase = (
                delayed_center
                * tau.upper
                * finite_output_frequency
                * r
                / period_lower
            )
            finite_delay_terms.append(sqrt_two * (common + phase))
            preconditioned_tail_delay_terms.append(
                sqrt_two
                * (
                    fast_tail_inverse * common
                    + delayed_center
                    * tau.upper
                    * r
                    / period_lower
                    * (1 + fast_tail_inverse * spectral_radius)
                )
            )
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        current_term = r * current_uniform + base.period.upper * current_variation
        finite_convolution = current_term + sum(
            finite_delay_terms, gmpy2.mpfr(0)
        )
        finite_tail_convolution = finite_convolution
        finite_full = max(
            finite_convolution + epsilon * r,
            (1 + epsilon) * r,
        )
        tail_from_finite = fast_tail_inverse * current_term + sum(
            preconditioned_tail_delay_terms, gmpy2.mpfr(0)
        )
    return (
        finite_convolution,
        finite_full,
        finite_tail_convolution,
        tail_from_finite,
        {
            "current_center": current_center,
            "delayed_center": delayed_center,
            "current_uniform": current_uniform,
            "delayed_uniform": delayed_uniform,
            "period_upper": period_upper,
            "period_lower": period_lower,
            "epsilon": epsilon,
            "correction_radius": r,
        },
    )


def validate_cell(
    rectangle: Rectangle,
    candidate: BinaryCandidate,
    base: Any,
    correction_radius: DirectedInterval,
    precision: int,
    acceptance_threshold: Decimal,
) -> CellBounds:
    sigma, phase, h, sigma_text, phase_text = _center_and_radius(
        rectangle, precision
    )
    if rectangle.sigma_lower < 0:
        raise ValueError("a compact-cover cell left the right half-plane")
    (
        finite,
        derivative,
        finite_tail,
        finite_tail_derivative,
        tail_finite,
        tail_finite_derivative,
        errors,
    ) = candidate_matrices(candidate, base, sigma, phase, precision)
    inverse = np.linalg.inv(finite)
    inverse_norm = _binary_complex_matrix_split_l1_upper(inverse, precision)
    finite_norm = _binary_complex_matrix_split_l1_upper(finite, precision)
    eta_binary = _binary_complex_product_split_l1_upper(
        inverse,
        finite,
        precision,
        defect_from_identity=True,
        left_norm=inverse_norm,
        right_norm=finite_norm,
    )
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        eta = eta_binary + inverse_norm * errors["finite"]
        first = (
            _binary_complex_product_split_l1_upper(
                inverse,
                derivative,
                precision,
                left_norm=inverse_norm,
            )
            + inverse_norm * errors["derivative"]
        )
        finite_tail_center = (
            _binary_complex_product_split_l1_upper(
                inverse,
                finite_tail,
                precision,
                left_norm=inverse_norm,
            )
            + inverse_norm * errors["finite_tail"]
        )
        finite_tail_first = (
            _binary_complex_product_split_l1_upper(
                inverse,
                finite_tail_derivative,
                precision,
                left_norm=inverse_norm,
            )
            + inverse_norm * errors["finite_tail_derivative"]
        )

    finite_cutoff = int(np.max(np.abs(candidate.modes)))
    fast_tail_inverse, slow_tail_inverse = _tail_inverse_bounds(
        sigma, phase, base, finite_cutoff, precision
    )
    tail_frequency_binary = complex(float(sigma.lower), float(phase.lower)) + (
        2.0j * math.pi * candidate.tail_modes
    )
    binary_fast_inverse = 1.0 / tail_frequency_binary
    binary_fast_inverse_split = _binary_complex_max_split_upper(
        binary_fast_inverse, precision
    )
    pi_point = DirectedInterval.from_float(math.pi, precision)
    pi_error = (pi_interval(precision) - pi_point).upper_abs()
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        largest_tail_mode = int(np.max(np.abs(candidate.tail_modes)))
        maximum_tail_frequency = (
            sigma.upper
            + phase.upper_abs()
            + 2 * largest_tail_mode * pi_interval(precision).upper
        )
        diagonal_error = (
            2 * largest_tail_mode * pi_error
            + _formation_error(maximum_tail_frequency, 1, precision)
        )
        inverse_formation_error = _formation_error(
            binary_fast_inverse_split, 1, precision
        )
        resolvent_correction = fast_tail_inverse * diagonal_error
        fast_inverse_error = (
            resolvent_correction * binary_fast_inverse_split
            + (1 + resolvent_correction) * inverse_formation_error
        )
    normalized_tail_finite = binary_fast_inverse[:, None] * tail_finite
    normalized_tail_finite_derivative = (
        binary_fast_inverse[:, None] * tail_finite_derivative
    )
    tail_finite_center_binary = _binary_complex_matrix_split_l1_upper(
        normalized_tail_finite, precision
    )
    tail_finite_first_binary = _binary_complex_matrix_split_l1_upper(
        normalized_tail_finite_derivative, precision
    )
    tail_finite_norm = _binary_complex_matrix_split_l1_upper(
        tail_finite, precision
    )
    tail_finite_derivative_norm = _binary_complex_matrix_split_l1_upper(
        tail_finite_derivative, precision
    )
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        tail_finite_center = (
            tail_finite_center_binary
            + fast_tail_inverse * errors["tail_finite"]
            + fast_inverse_error * tail_finite_norm
            + _formation_error(
                tail_finite_center_binary, len(candidate.tail_modes), precision
            )
        )
        tail_finite_first = (
            tail_finite_first_binary
            + fast_tail_inverse * errors["tail_finite_derivative"]
            + fast_inverse_error * tail_finite_derivative_norm
            + _formation_error(
                tail_finite_first_binary,
                len(candidate.tail_modes),
                precision,
            )
        )

    (
        finite_convolution_correction,
        finite_full_correction,
        finite_tail_convolution_correction,
        tail_from_finite_correction,
        values,
    ) = _orbit_corrections(
        base,
        correction_radius,
        rectangle,
        fast_tail_inverse,
        finite_cutoff,
        precision,
    )
    sqrt_two = DirectedInterval.from_decimal(2, precision).sqrt().upper
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        alpha_square_sum = (
            (base.parameters["tau_0"].upper / base.period.lower) ** 2
            + (base.parameters["tau_1"].upper / base.period.lower) ** 2
        )
        second_raw = (
            base.period.upper
            * sqrt_two
            * values["delayed_center"]
            * alpha_square_sum
            / 2
        )
        finite_second = inverse_norm * second_raw
        tail_second = fast_tail_inverse * second_raw
        finite_to_finite = (
            eta
            + h * first
            + h * h * finite_second
            + inverse_norm * finite_full_correction
        )
        finite_from_tail = (
            finite_tail_center
            + h * finite_tail_first
            + h * h * finite_second
            + inverse_norm * finite_tail_convolution_correction
        )
        tail_from_finite = (
            tail_finite_center
            + h * tail_finite_first
            + h * h * tail_second
            + tail_from_finite_correction
        )
        tail_voltage_input = (
            fast_tail_inverse
            * (
                h
                + values["period_upper"]
                * (
                    values["current_uniform"]
                    + 2 * sqrt_two * values["delayed_uniform"]
                )
            )
            + slow_tail_inverse
            * values["period_upper"]
            * values["epsilon"]
        )
        tail_recovery_input = (
            fast_tail_inverse * values["period_upper"]
            + slow_tail_inverse
            * (h + values["epsilon"] * values["correction_radius"])
        )
        tail_to_tail = max(tail_voltage_input, tail_recovery_input)
        finite_input = finite_to_finite + tail_from_finite
        tail_input = finite_from_tail + tail_to_tail
    finite_input_text = _exact_decimal_sum(
        (decimal_upper(finite_to_finite), decimal_upper(tail_from_finite))
    )
    tail_input_text = _exact_decimal_sum(
        (decimal_upper(finite_from_tail), decimal_upper(tail_to_tail))
    )
    contraction_text = str(
        max(Decimal(finite_input_text), Decimal(tail_input_text))
    )
    margin_text = _margin(contraction_text)
    validated = (
        Decimal(contraction_text) < 1
        and Decimal(contraction_text) <= acceptance_threshold
        and Decimal(margin_text) > 0
    )
    leaf = CoverLeaf(
        rectangle.root_id,
        rectangle.path,
        "full_operator_neumann",
        contraction_text,
        finite_input_text,
        tail_input_text,
    )
    worst = WorstCoverCell(
        root_id=rectangle.root_id,
        path=rectangle.path,
        sigma_lower=format(rectangle.sigma_lower, "f"),
        sigma_center_binary64=sigma_text,
        sigma_upper=format(rectangle.sigma_upper, "f"),
        phase_lower=format(rectangle.phase_lower, "f"),
        phase_center_binary64=phase_text,
        phase_upper=format(rectangle.phase_upper, "f"),
        split_parameter_radius_upper=decimal_upper(h),
        finite_inverse_l1_upper=decimal_upper(inverse_norm),
        finite_inverse_defect_upper=decimal_upper(eta),
        finite_first_product_upper=decimal_upper(first),
        finite_from_tail_center_upper=decimal_upper(finite_tail_center),
        finite_from_tail_first_upper=decimal_upper(finite_tail_first),
        tail_from_finite_center_upper=decimal_upper(tail_finite_center),
        tail_from_finite_first_upper=decimal_upper(tail_finite_first),
        fast_tail_diagonal_inverse_split_upper=decimal_upper(fast_tail_inverse),
        slow_tail_diagonal_inverse_split_upper=decimal_upper(slow_tail_inverse),
        finite_full_orbit_correction_upper=decimal_upper(finite_full_correction),
        finite_convolution_orbit_correction_upper=decimal_upper(
            finite_convolution_correction
        ),
        finite_tail_convolution_orbit_correction_upper=decimal_upper(
            finite_tail_convolution_correction
        ),
        tail_from_finite_orbit_correction_upper=decimal_upper(
            tail_from_finite_correction
        ),
        finite_to_finite_upper=decimal_upper(finite_to_finite),
        finite_from_tail_upper=decimal_upper(finite_from_tail),
        tail_from_finite_upper=decimal_upper(tail_from_finite),
        tail_to_tail_voltage_input_upper=decimal_upper(tail_voltage_input),
        tail_to_tail_recovery_input_upper=decimal_upper(tail_recovery_input),
        tail_to_tail_upper=decimal_upper(tail_to_tail),
        finite_input_column_sum_upper=finite_input_text,
        tail_input_column_sum_upper=tail_input_text,
        contraction_upper=contraction_text,
        contraction_margin_lower=margin_text,
    )
    return CellBounds(leaf, worst, validated)


def split_rectangle(rectangle: Rectangle) -> tuple[Rectangle, Rectangle]:
    sigma_width = Fraction(rectangle.sigma_upper) - Fraction(
        rectangle.sigma_lower
    )
    phase_width = Fraction(rectangle.phase_upper) - Fraction(
        rectangle.phase_lower
    )
    if sigma_width >= phase_width:
        with localcontext() as context:
            context.prec = 400
            midpoint = (
                rectangle.sigma_lower + rectangle.sigma_upper
            ) / 2
        return (
            Rectangle(
                rectangle.root_id,
                rectangle.path + "x0",
                rectangle.sigma_lower,
                midpoint,
                rectangle.phase_lower,
                rectangle.phase_upper,
            ),
            Rectangle(
                rectangle.root_id,
                rectangle.path + "x1",
                midpoint,
                rectangle.sigma_upper,
                rectangle.phase_lower,
                rectangle.phase_upper,
            ),
        )
    with localcontext() as context:
        context.prec = 400
        midpoint = (rectangle.phase_lower + rectangle.phase_upper) / 2
    return (
        Rectangle(
            rectangle.root_id,
            rectangle.path + "y0",
            rectangle.sigma_lower,
            rectangle.sigma_upper,
            rectangle.phase_lower,
            midpoint,
        ),
        Rectangle(
            rectangle.root_id,
            rectangle.path + "y1",
            rectangle.sigma_lower,
            rectangle.sigma_upper,
            midpoint,
            rectangle.phase_upper,
        ),
    )


def rectangle_strictly_inside_origin_disk(
    rectangle: Rectangle,
    radius: Decimal,
) -> bool:
    sigma = Fraction(rectangle.sigma_upper)
    phase = Fraction(rectangle.phase_upper)
    exact_radius = Fraction(radius)
    return sigma * sigma + phase * phase < exact_radius * exact_radius


def rectangle_from_path(root: Rectangle, path: str) -> Rectangle:
    if len(path) % 2:
        raise ValueError("a dyadic path has odd length")
    rectangle = root
    for index in range(0, len(path), 2):
        token = path[index : index + 2]
        first, second = split_rectangle(rectangle)
        if first.path.endswith(token):
            rectangle = first
        elif second.path.endswith(token):
            rectangle = second
        else:
            raise ValueError("a dyadic path uses the wrong split axis")
    if rectangle.path != path:
        raise ValueError("a dyadic path reconstruction failed")
    return rectangle


def prefix_complete(
    leaves: Sequence[CoverLeaf],
    root_ids: Sequence[str],
) -> bool:
    by_root = {root: [] for root in root_ids}
    for leaf in leaves:
        if leaf.root_id not in by_root or len(leaf.path) % 2:
            return False
        tokens = tuple(
            leaf.path[index : index + 2]
            for index in range(0, len(leaf.path), 2)
        )
        if any(token not in ("x0", "x1", "y0", "y1") for token in tokens):
            return False
        by_root[leaf.root_id].append(tokens)
    for paths in by_root.values():
        if not paths:
            return False
        trie: dict[str, Any] = {}
        for path in paths:
            node = trie
            for token in path:
                if "leaf" in node:
                    return False
                node = node.setdefault(token, {})
            if node:
                return False
            node["leaf"] = True

        def complete(node: Mapping[str, Any]) -> bool:
            if node.get("leaf") is True:
                return len(node) == 1
            keys = set(node)
            if keys not in ({"x0", "x1"}, {"y0", "y1"}):
                return False
            return all(complete(node[key]) for key in keys)

        if not complete(trie):
            return False
        if sum(Fraction(1, 2 ** len(path)) for path in paths) != 1:
            return False
    return True


def leaf_digest(leaves: Sequence[CoverLeaf]) -> str:
    lines = [
        "|".join(
            (
                leaf.root_id,
                leaf.path,
                leaf.proof_kind,
                leaf.contraction_upper,
                leaf.finite_input_column_sum_upper,
                leaf.tail_input_column_sum_upper,
            )
        )
        for leaf in sorted(leaves, key=lambda item: (item.root_id, item.path))
    ]
    return sha256(("\n".join(lines) + "\n").encode("ascii")).hexdigest()


__all__ = [
    "BinaryCandidate",
    "CellBounds",
    "CoverLeaf",
    "Rectangle",
    "WorstCoverCell",
    "candidate_matrices",
    "input_rotated_convolution",
    "leaf_digest",
    "mode_rotation_basis",
    "output_rotated_convolution",
    "prefix_complete",
    "rectangle_from_path",
    "rectangle_strictly_inside_origin_disk",
    "split_rectangle",
    "validate_cell",
]
