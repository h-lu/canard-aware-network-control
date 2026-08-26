"""Negative-real-part cells for the leaky Floquet full-operator cover.

The audited right-half engine uses several estimates specialized to
``Re s >= 0``.  This module reuses its physical matrix construction and
binary arithmetic, but restores the factors ``exp(-alpha Re s)`` needed on
a source-bound strip ``Re s >= -gamma``.  It deliberately contains no
branch, theorem, or root-count claim.
"""

from __future__ import annotations

from decimal import Decimal
import math
from typing import Any

import gmpy2
import numpy as np

from canard_control.directed_interval import (
    DirectedInterval,
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
    _formation_error,
)
from canard_control.leaky_floquet_compact_cover_engine import (
    BinaryCandidate,
    CellBounds,
    CoverLeaf,
    Rectangle,
    WorstCoverCell,
    _center_and_radius,
    _exact_decimal_sum,
    _margin,
    _tail_inverse_bounds,
    candidate_matrices,
)


def _left_delay_modulus_upper(
    rectangle: Rectangle,
    base: Any,
    correction_radius: DirectedInterval,
    precision: int,
) -> gmpy2.mpfr:
    """Bound every physical delay factor on the full source orbit ball."""

    if rectangle.sigma_lower >= 0:
        return gmpy2.mpfr(1, precision)
    negative_real = DirectedInterval.from_decimal(
        format(-rectangle.sigma_lower, "f"), precision
    ).upper
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        minimum_period = base.period.lower - correction_radius.upper
    if minimum_period <= 0:
        raise ArithmeticError("the delay modulus crosses zero period")
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        maximum_alpha = max(
            base.parameters["tau_0"].upper / minimum_period,
            base.parameters["tau_1"].upper / minimum_period,
        )
        return gmpy2.exp(negative_real * maximum_alpha)


def _left_tail_frequency_upper(
    sigma: DirectedInterval,
    phase: DirectedInterval,
    largest_tail_mode: int,
    precision: int,
) -> gmpy2.mpfr:
    """Formation scale using ``|Re s|``, not the RHP-only upper endpoint."""

    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        return (
            sigma.upper_abs()
            + phase.upper_abs()
            + 2 * largest_tail_mode * pi_interval(precision).upper
        )


def _left_orbit_corrections(
    base: Any,
    correction_radius: DirectedInterval,
    rectangle: Rectangle,
    fast_tail_inverse: gmpy2.mpfr,
    finite_cutoff: int,
    delay_modulus: gmpy2.mpfr,
    precision: int,
) -> tuple[
    gmpy2.mpfr,
    gmpy2.mpfr,
    gmpy2.mpfr,
    gmpy2.mpfr,
    dict[str, gmpy2.mpfr],
]:
    """Orbit/period perturbations with the left-strip exponential factor."""

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

    sigma_abs = max(abs(rectangle.sigma_lower), abs(rectangle.sigma_upper))
    sigma_box = DirectedInterval.from_decimal(format(sigma_abs, "f"), precision)
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
            common = delay_modulus * (
                r * delayed_uniform
                + base.period.upper * delayed_variation
            )
            phase = (
                delay_modulus
                * delayed_center
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
                    + delay_modulus
                    * delayed_center
                    * tau.upper
                    * r
                    / period_lower
                    * (1 + fast_tail_inverse * spectral_radius)
                )
            )
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        current_term = (
            r * current_uniform + base.period.upper * current_variation
        )
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
            "delay_modulus": delay_modulus,
        },
    )


def _left_second_order_raw(
    base: Any,
    period_upper: gmpy2.mpfr,
    delayed_center: gmpy2.mpfr,
    delay_modulus: gmpy2.mpfr,
    precision: int,
) -> gmpy2.mpfr:
    """Delay-exponential second remainder on the negative strip."""

    sqrt_two = DirectedInterval.from_decimal(2, precision).sqrt().upper
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        alpha_square_sum = (
            (base.parameters["tau_0"].upper / base.period.lower) ** 2
            + (base.parameters["tau_1"].upper / base.period.lower) ** 2
        )
        return (
            period_upper
            * sqrt_two
            * delayed_center
            * delay_modulus
            * alpha_square_sum
            / 2
        )


def validate_left_cell(
    rectangle: Rectangle,
    candidate: BinaryCandidate,
    base: Any,
    correction_radius: DirectedInterval,
    precision: int,
    acceptance_threshold: Decimal,
) -> CellBounds:
    """Validate one cell, including every ``Re s < 0`` correction."""

    sigma, phase, h, sigma_text, phase_text = _center_and_radius(
        rectangle, precision
    )
    if rectangle.sigma_upper > 0:
        raise ValueError("a left-strip cell crossed its sigma=0 seam")
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
        maximum_tail_frequency = _left_tail_frequency_upper(
            sigma,
            phase,
            largest_tail_mode,
            precision,
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

    delay_modulus = _left_delay_modulus_upper(
        rectangle, base, correction_radius, precision
    )
    (
        finite_convolution_correction,
        finite_full_correction,
        finite_tail_convolution_correction,
        tail_from_finite_correction,
        values,
    ) = _left_orbit_corrections(
        base,
        correction_radius,
        rectangle,
        fast_tail_inverse,
        finite_cutoff,
        delay_modulus,
        precision,
    )
    sqrt_two = DirectedInterval.from_decimal(2, precision).sqrt().upper
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        second_raw = _left_second_order_raw(
            base,
            values["period_upper"],
            values["delayed_center"],
            delay_modulus,
            precision,
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
                    + 2
                    * sqrt_two
                    * delay_modulus
                    * values["delayed_uniform"]
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


__all__ = [
    "_left_delay_modulus_upper",
    "_left_orbit_corrections",
    "_left_second_order_raw",
    "_left_tail_frequency_upper",
    "validate_left_cell",
]
