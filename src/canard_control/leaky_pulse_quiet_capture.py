"""Directed capture of the physical ``J=3/10`` pulse by the quiet basin.

The physical voltage pulse acts on ``0 <= t < 1`` and the RFDE is autonomous
after release.  Its delays are ``4*sqrt(5)`` and ``5*sqrt(5)``.  We cover the
trajectory through ``T=161*sqrt(5)`` on the sorted union

    {n*sqrt(5)/N} union {1+n*sqrt(5)/N}.

Both delayed cells therefore translate to already completed cells with the
same normalized time.  The second grid also isolates the pulse release and
every propagated loss of smoothness.

Each cell has an MPFR Taylor polynomial guide.  The guide is not an
enclosure.  A scalar error in the quadratic ``P`` norm is propagated using
the current-state logarithmic norm, one forcing term for each delayed slot,
and an outward-rounded polynomial residual.  On the complete terminal
history ``[T-5*sqrt(5),T]``, Bernstein bounds for the quadratic Lyapunov
function, enlarged by the validated error radii, lie strictly below
``1/125``.  The large Razumikhin theorem then proves convergence to the
quiet equilibrium.

This module proves only the ``J=3/10`` quiet-side basin inclusion.  It does
not validate an onset, a separator, an outer capture, or uniqueness of a
pulse threshold.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from fractions import Fraction
from functools import cmp_to_key, lru_cache
from hashlib import sha256
import json
import math
from pathlib import Path
import platform
from typing import Any, Mapping, Sequence

import gmpy2
import sympy as sp

from canard_control.autonomous_leaky_recovery_bistable import (
    EPSILON,
    KAPPA_1,
    KAPPA_3,
    UNFOLDING,
)
from canard_control.directed_interval import (
    DirectedInterval,
    decimal_lower,
    decimal_upper,
)
from canard_control.leaky_pulse_terminal_history import (
    RESULT_RELATIVE_PATH as PULSE_TERMINAL_RESULT_RELATIVE_PATH,
    validate_pulse_terminal_history_result,
)
from canard_control.leaky_quiet_history_basin import P11, P12, P22
from canard_control.leaky_quiet_large_razumikhin_basin import (
    HISTORY_SUBLEVEL,
    RESULT_RELATIVE_PATH as LARGE_BASIN_RESULT_RELATIVE_PATH,
    validate_large_quiet_basin_result,
)


SCHEMA_ID = "leaky-pulse-quiet-capture-v1"
MODEL_ID = "autonomous-leaky-recovery-physical-pulse"
SOURCE_RELATIVE_PATH = "src/canard_control/leaky_pulse_quiet_capture.py"
GENERATOR_RELATIVE_PATH = "experiments/leaky_pulse_quiet_capture.py"
NOTE_RELATIVE_PATH = "docs/leaky-pulse-quiet-capture.md"
RESULT_RELATIVE_PATH = "experiments/results/leaky_pulse_quiet_capture.json"
INTERVAL_SOURCE_RELATIVE_PATH = "src/canard_control/directed_interval.py"
MODEL_SOURCE_RELATIVE_PATH = (
    "src/canard_control/autonomous_leaky_recovery_bistable.py"
)
PULSE_TERMINAL_SOURCE_RELATIVE_PATH = (
    "src/canard_control/leaky_pulse_terminal_history.py"
)
LARGE_BASIN_SOURCE_RELATIVE_PATH = (
    "src/canard_control/leaky_quiet_large_razumikhin_basin.py"
)
QUIET_P_SOURCE_RELATIVE_PATH = (
    "src/canard_control/leaky_quiet_history_basin.py"
)
DEFAULT_COMMAND = (
    "PYTHONPATH=src /usr/bin/python3 experiments/leaky_pulse_quiet_capture.py"
)
MANIFEST_ARITHMETIC = (
    "192-bit outward-rounded MPFR; exact Q(sqrt(5)) ordering and delay-cell "
    "translation on the union grid {n*sqrt(5)/24} union "
    "{1+n*sqrt(5)/24}; degree-24 MPFR Taylor polynomial guides; current "
    "P-logarithmic norm plus two distinct delayed P-error forcings; "
    "outward polynomial residual; complete retained-history degree-48 "
    "Bernstein Lyapunov bound"
)

PRECISION_BITS = 192
GRID_DENOMINATOR = 24
TAYLOR_DEGREE = 24
FINAL_SQRT5_MULTIPLIER = 161
FINAL_NODE_INDEX = FINAL_SQRT5_MULTIPLIER * GRID_DENOMINATOR
PULSE_AMPLITUDE = Fraction(3, 10)
PULSE_DURATION = Fraction(1)
DELAY_MULTIPLIERS = (4, 5)
MAXIMUM_FIXED_POINT_ITERATIONS = 40
TUBE_INFLATION = "1.0078125"
TUBE_FLOOR = "1e-90"

TRUE_FLAGS = (
    "exact_alpha_enclosure_validated",
    "exact_union_grid_ordering_validated",
    "pulse_release_isolated_at_one_validated",
    "both_delay_cells_translate_exactly_validated",
    "current_p_logarithmic_norm_enclosed",
    "delay_four_error_forcing_enclosed",
    "delay_five_error_forcing_enclosed",
    "directed_taylor_method_of_steps_closed",
    "complete_retained_history_bernstein_bound_validated",
    "pulse_J_030_enters_large_quiet_ball_validated",
    "pulse_J_030_quiet_capture_proved",
)

FALSE_FLAGS = (
    "pulse_J_032_outer_capture_validated",
    "history_space_separator_validated",
    "unique_physical_pulse_onset_validated",
    "physical_pulse_transversality_validated",
    "canard_root_equals_physical_onset_proved",
    "global_quiet_basin_validated",
)


IntervalPolynomial = tuple[DirectedInterval, ...]


def _point(value: str | int, precision: int) -> DirectedInterval:
    return DirectedInterval.from_decimal(value, precision)


def _fraction_interval(value: Fraction, precision: int) -> DirectedInterval:
    return _point(value.numerator, precision) / _point(value.denominator, precision)


def _mpfr_point(value: gmpy2.mpfr, precision: int) -> DirectedInterval:
    return DirectedInterval.from_bounds(value, value, precision)


def _lower_text(value: gmpy2.mpfr, digits: int = 64) -> str:
    return decimal_lower(value, digits)


def _upper_text(value: gmpy2.mpfr, digits: int = 64) -> str:
    return decimal_upper(value, digits)


def _alpha_interval(precision: int) -> DirectedInterval:
    """Outward enclosure of the exact equilibrium voltage ``(3/4)^(1/3)``."""

    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        lower = gmpy2.cbrt(gmpy2.mpfr(3) / gmpy2.mpfr(4))
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        upper = gmpy2.cbrt(gmpy2.mpfr(3) / gmpy2.mpfr(4))
    return DirectedInterval(lower, upper, precision)


def _nearest(value: object, precision: int) -> gmpy2.mpfr:
    with gmpy2.context(precision=precision, round=gmpy2.RoundToNearest):
        return gmpy2.mpfr(value)


def _nearest_midpoint(value: DirectedInterval) -> gmpy2.mpfr:
    with gmpy2.context(
        precision=value.precision, round=gmpy2.RoundToNearest
    ):
        return (value.lower + value.upper) / 2


@dataclass(frozen=True)
class _Node:
    """The exact time ``origin + index*sqrt(5)/GRID_DENOMINATOR``."""

    origin: int
    index: int

    def shifted(self, delay_multiplier: int) -> _Node:
        return _Node(
            self.origin,
            self.index - delay_multiplier * GRID_DENOMINATOR,
        )


ZERO_NODE = _Node(0, 0)
PULSE_RELEASE_NODE = _Node(1, 0)
FINAL_NODE = _Node(0, FINAL_NODE_INDEX)
RETAINED_LEFT_NODE = _Node(
    0, (FINAL_SQRT5_MULTIPLIER - 5) * GRID_DENOMINATOR
)


def _node_compare(left: _Node, right: _Node) -> int:
    """Compare two nodes by exact arithmetic in ``Q(sqrt(5))``."""

    rational = (left.origin - right.origin) * GRID_DENOMINATOR
    radical = left.index - right.index
    if rational == 0:
        return (radical > 0) - (radical < 0)
    if radical == 0:
        return (rational > 0) - (rational < 0)
    if rational > 0 and radical > 0:
        return 1
    if rational < 0 and radical < 0:
        return -1
    rational_square = rational * rational
    radical_square = 5 * radical * radical
    if rational > 0:
        return 1 if rational_square > radical_square else -1
    return 1 if radical_square > rational_square else -1


def _node_interval(node: _Node, precision: int) -> DirectedInterval:
    root = _point(5, precision).sqrt()
    return _point(node.origin, precision) + (
        _point(node.index, precision) * root / _point(GRID_DENOMINATOR, precision)
    )


@lru_cache(maxsize=1)
def _forward_nodes() -> tuple[_Node, ...]:
    nodes = [_Node(0, index) for index in range(FINAL_NODE_INDEX + 1)]
    padding = math.ceil(GRID_DENOMINATOR / math.sqrt(5.0)) + 2
    for index in range(-padding, FINAL_NODE_INDEX + padding + 1):
        node = _Node(1, index)
        if (
            _node_compare(ZERO_NODE, node) < 0
            and _node_compare(node, FINAL_NODE) < 0
        ):
            nodes.append(node)
    ordered = tuple(sorted(nodes, key=cmp_to_key(_node_compare)))
    if ordered[0] != ZERO_NODE or ordered[-1] != FINAL_NODE:
        raise AssertionError("the exact union grid endpoints changed")
    if len(set(ordered)) != len(ordered):
        raise AssertionError("the irrational union grid acquired a duplicate")
    if PULSE_RELEASE_NODE not in ordered or RETAINED_LEFT_NODE not in ordered:
        raise AssertionError("a required pulse/retained-history node is absent")
    if any(
        _node_compare(left, right) >= 0
        for left, right in zip(ordered[:-1], ordered[1:], strict=True)
    ):
        raise AssertionError("the exact union grid is not strictly ordered")
    return ordered


def _cell_key(left: _Node, right: _Node) -> tuple[int, int, int, int]:
    return left.origin, left.index, right.origin, right.index


def _poly_add(
    left: Sequence[DirectedInterval], right: Sequence[DirectedInterval]
) -> IntervalPolynomial:
    precision = left[0].precision
    zero = _point(0, precision)
    return tuple(
        (left[index] if index < len(left) else zero)
        + (right[index] if index < len(right) else zero)
        for index in range(max(len(left), len(right)))
    )


def _poly_neg(value: Sequence[DirectedInterval]) -> IntervalPolynomial:
    return tuple(-item for item in value)


def _poly_sub(
    left: Sequence[DirectedInterval], right: Sequence[DirectedInterval]
) -> IntervalPolynomial:
    return _poly_add(left, _poly_neg(right))


def _poly_scale(
    value: Sequence[DirectedInterval], scalar: DirectedInterval
) -> IntervalPolynomial:
    return tuple(item * scalar for item in value)


def _poly_multiply(
    left: Sequence[DirectedInterval], right: Sequence[DirectedInterval]
) -> IntervalPolynomial:
    precision = left[0].precision
    result = [_point(0, precision) for _ in range(len(left) + len(right) - 1)]
    for left_index, left_value in enumerate(left):
        for right_index, right_value in enumerate(right):
            position = left_index + right_index
            result[position] = result[position] + left_value * right_value
    return tuple(result)


def _poly_cube(value: Sequence[DirectedInterval]) -> IntervalPolynomial:
    return _poly_multiply(_poly_multiply(value, value), value)


def _poly_add_constant(
    value: Sequence[DirectedInterval], constant: DirectedInterval
) -> IntervalPolynomial:
    result = list(value)
    result[0] = result[0] + constant
    return tuple(result)


def _poly_time_derivative(
    value: Sequence[DirectedInterval], step: DirectedInterval
) -> IntervalPolynomial:
    if len(value) == 1:
        return (_point(0, step.precision),)
    return tuple(
        _point(index, step.precision) * value[index] / step
        for index in range(1, len(value))
    )


@lru_cache(maxsize=128)
def _bernstein_weights(
    degree: int, precision: int
) -> tuple[tuple[DirectedInterval, ...], ...]:
    rows = []
    for index in range(degree + 1):
        rows.append(
            tuple(
                _point(math.comb(index, power), precision)
                / _point(math.comb(degree, power), precision)
                for power in range(index + 1)
            )
        )
    return tuple(rows)


def _poly_bernstein_range(
    value: Sequence[DirectedInterval],
) -> DirectedInterval:
    precision = value[0].precision
    weights = _bernstein_weights(len(value) - 1, precision)
    coefficients = []
    for row in weights:
        item = _point(0, precision)
        for power, weight in enumerate(row):
            item = item + weight * value[power]
        coefficients.append(item)
    return DirectedInterval.from_bounds(
        min(item.lower for item in coefficients),
        max(item.upper for item in coefficients),
        precision,
    )


def _poly_l1_upper(value: Sequence[DirectedInterval]) -> gmpy2.mpfr:
    precision = value[0].precision
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        total = gmpy2.mpfr(0)
        for coefficient in value:
            total += coefficient.upper_abs()
        return total


def _p_box_norm_upper(
    first: gmpy2.mpfr, second: gmpy2.mpfr, precision: int
) -> gmpy2.mpfr:
    """Upper bound of the P norm on ``[-first,first] x [-second,second]``."""

    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        p11 = gmpy2.mpfr(P11.numerator) / P11.denominator
        # Form the magnitude from a positive numerator.  Rounding a negative
        # quotient upward and only then taking ``abs`` would round its
        # magnitude downward, which is the wrong direction for this bound.
        p12 = gmpy2.mpfr(abs(P12.numerator)) / P12.denominator
        p22 = gmpy2.mpfr(P22.numerator) / P22.denominator
        return gmpy2.sqrt(
            p11 * first * first
            + 2 * p12 * first * second
            + p22 * second * second
        )


@lru_cache(maxsize=8)
def _p_constants(precision: int) -> tuple[gmpy2.mpfr, ...]:
    p11 = _fraction_interval(P11, precision)
    p12 = _fraction_interval(P12, precision)
    p22 = _fraction_interval(P22, precision)
    determinant = p11 * p22 - p12**2
    coordinate = (p22 / determinant).sqrt()
    forcing = (p11 * p22 / determinant).sqrt()
    alpha_diagonal = (p11 + 2 * p12 + p22).sqrt()
    return coordinate.upper, forcing.upper, alpha_diagonal.upper


def _generalized_log_norm_point(
    current_coefficient: gmpy2.mpfr, precision: int
) -> gmpy2.mpfr:
    """Upper bound for ``mu_P([[a,-1],[epsilon,-epsilon]])`` at one ``a``."""

    a = _mpfr_point(current_coefficient, precision)
    epsilon = _fraction_interval(EPSILON, precision)
    p = _fraction_interval(P11, precision)
    q = _fraction_interval(P12, precision)
    r = _fraction_interval(P22, precision)
    determinant_p = p * r - q**2
    s11 = p * a + q * epsilon
    s12 = (-p - q * epsilon + q * a + r * epsilon) / 2
    s22 = -q - r * epsilon
    trace = (r * s11 + p * s22 - 2 * q * s12) / determinant_p
    determinant = (s11 * s22 - s12**2) / determinant_p
    discriminant = trace**2 - 4 * determinant
    if discriminant.upper < 0:
        raise ArithmeticError(
            "the generalized logarithmic-norm discriminant is negative"
        )
    discriminant = DirectedInterval.from_bounds(
        0 if discriminant.lower < 0 else discriminant.lower,
        discriminant.upper,
        precision,
    )
    return ((trace + discriminant.sqrt()) / 2).upper


def _current_log_norm_upper(
    voltage: DirectedInterval, precision: int
) -> gmpy2.mpfr:
    epsilon = _fraction_interval(EPSILON, precision)
    kappa_1 = _fraction_interval(KAPPA_1, precision)
    kappa_3 = _fraction_interval(KAPPA_3, precision)
    coefficient = (
        1
        - voltage**2
        - epsilon * kappa_1
        - 3 * epsilon * kappa_3 * (voltage - 1) ** 2
    )
    # A matrix measure is a supremum of affine Rayleigh quotients and hence
    # convex in the scalar coefficient.  Its maximum on an interval is at an
    # endpoint.
    return max(
        _generalized_log_norm_point(coefficient.lower, precision),
        _generalized_log_norm_point(coefficient.upper, precision),
    )


def _delayed_forcing_upper(
    voltage: DirectedInterval, precision: int
) -> gmpy2.mpfr:
    epsilon = _fraction_interval(EPSILON, precision)
    kappa_1 = _fraction_interval(KAPPA_1, precision)
    kappa_3 = _fraction_interval(KAPPA_3, precision)
    coefficient = epsilon / 2 * (
        kappa_1 + 3 * kappa_3 * (voltage - 1) ** 2
    )
    _, forcing_coordinate, _ = _p_constants(precision)
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        return forcing_coordinate * max(abs(coefficient.lower), abs(coefficient.upper))


def _square_coefficients_nearest(
    value: Sequence[gmpy2.mpfr], degree: int, precision: int
) -> list[gmpy2.mpfr]:
    with gmpy2.context(precision=precision, round=gmpy2.RoundToNearest):
        result = []
        zero = gmpy2.mpfr(0)
        for order in range(degree + 1):
            total = gmpy2.mpfr(0)
            for index in range(order + 1):
                if index < len(value) and order - index < len(value):
                    total += value[index] * value[order - index]
            result.append(total if total else zero)
        return result


def _cube_coefficients_nearest(
    value: Sequence[gmpy2.mpfr], degree: int, precision: int
) -> list[gmpy2.mpfr]:
    square = _square_coefficients_nearest(value, degree, precision)
    with gmpy2.context(precision=precision, round=gmpy2.RoundToNearest):
        result = []
        for order in range(degree + 1):
            total = gmpy2.mpfr(0)
            for index in range(order + 1):
                if index < len(square) and order - index < len(value):
                    total += square[index] * value[order - index]
            result.append(total)
        return result


def _taylor_guide(
    start: tuple[gmpy2.mpfr, gmpy2.mpfr],
    step: gmpy2.mpfr,
    delayed_four: tuple[gmpy2.mpfr, ...],
    delayed_five: tuple[gmpy2.mpfr, ...],
    pulse_on: bool,
    degree: int,
    precision: int,
) -> tuple[tuple[gmpy2.mpfr, ...], tuple[gmpy2.mpfr, ...]]:
    """Choose a nearest-rounded Taylor guide; no coefficient is a claim."""

    with gmpy2.context(precision=precision, round=gmpy2.RoundToNearest):
        epsilon = gmpy2.mpfr(EPSILON.numerator) / EPSILON.denominator
        unfolding = gmpy2.mpfr(UNFOLDING.numerator) / UNFOLDING.denominator
        kappa_1 = gmpy2.mpfr(KAPPA_1.numerator) / KAPPA_1.denominator
        kappa_3 = gmpy2.mpfr(KAPPA_3.numerator) / KAPPA_3.denominator
        pulse = (
            gmpy2.mpfr(PULSE_AMPLITUDE.numerator) / PULSE_AMPLITUDE.denominator
            if pulse_on
            else gmpy2.mpfr(0)
        )
        half = gmpy2.mpfr(1) / 2
        third = gmpy2.mpfr(1) / 3
        d4_shift = list(delayed_four)
        d5_shift = list(delayed_five)
        d4_shift[0] -= 1
        d5_shift[0] -= 1
        d4_cube = _cube_coefficients_nearest(d4_shift, degree - 1, precision)
        d5_cube = _cube_coefficients_nearest(d5_shift, degree - 1, precision)

        voltage = [gmpy2.mpfr(start[0])]
        recovery = [gmpy2.mpfr(start[1])]
        voltage_square: list[gmpy2.mpfr] = []
        shifted_square: list[gmpy2.mpfr] = []
        for order in range(degree):
            shifted = list(voltage)
            shifted[0] -= 1
            voltage_square.append(
                sum(
                    (voltage[index] * voltage[order - index]
                     for index in range(order + 1)),
                    gmpy2.mpfr(0),
                )
            )
            shifted_square.append(
                sum(
                    (shifted[index] * shifted[order - index]
                     for index in range(order + 1)),
                    gmpy2.mpfr(0),
                )
            )
            voltage_cube = sum(
                (voltage_square[index] * voltage[order - index]
                 for index in range(order + 1)),
                gmpy2.mpfr(0),
            )
            shifted_cube = sum(
                (shifted_square[index] * shifted[order - index]
                 for index in range(order + 1)),
                gmpy2.mpfr(0),
            )
            v_order = voltage[order]
            w_order = recovery[order]
            d4_order = delayed_four[order] if order < len(delayed_four) else 0
            d5_order = delayed_five[order] if order < len(delayed_five) else 0
            fast = (
                v_order
                - third * voltage_cube
                - w_order
                + epsilon
                * kappa_1
                * (half * (d4_order + d5_order) - v_order)
                + epsilon
                * kappa_3
                * (half * (d4_cube[order] + d5_cube[order]) - shifted_cube)
                + (pulse if order == 0 else 0)
            )
            slow = epsilon * (
                v_order - w_order - (unfolding if order == 0 else 0)
            )
            voltage.append(step * fast / (order + 1))
            recovery.append(step * slow / (order + 1))
        return tuple(voltage), tuple(recovery)


def _guide_residual_upper(
    voltage_mpfr: Sequence[gmpy2.mpfr],
    recovery_mpfr: Sequence[gmpy2.mpfr],
    delayed_four_mpfr: Sequence[gmpy2.mpfr],
    delayed_five_mpfr: Sequence[gmpy2.mpfr],
    step: DirectedInterval,
    pulse_on: bool,
) -> gmpy2.mpfr:
    precision = step.precision
    voltage = tuple(_mpfr_point(value, precision) for value in voltage_mpfr)
    recovery = tuple(_mpfr_point(value, precision) for value in recovery_mpfr)
    delayed_four = tuple(
        _mpfr_point(value, precision) for value in delayed_four_mpfr
    )
    delayed_five = tuple(
        _mpfr_point(value, precision) for value in delayed_five_mpfr
    )
    epsilon = _fraction_interval(EPSILON, precision)
    unfolding = _fraction_interval(UNFOLDING, precision)
    kappa_1 = _fraction_interval(KAPPA_1, precision)
    kappa_3 = _fraction_interval(KAPPA_3, precision)
    half = _point(1, precision) / 2
    fast = _poly_sub(
        voltage,
        _poly_scale(_poly_cube(voltage), _point(1, precision) / 3),
    )
    fast = _poly_sub(fast, recovery)
    average_delay = _poly_scale(_poly_add(delayed_four, delayed_five), half)
    fast = _poly_add(
        fast,
        _poly_scale(_poly_sub(average_delay, voltage), epsilon * kappa_1),
    )
    delayed_cubic = _poly_scale(
        _poly_add(
            _poly_cube(_poly_add_constant(delayed_four, -_point(1, precision))),
            _poly_cube(_poly_add_constant(delayed_five, -_point(1, precision))),
        ),
        half,
    )
    current_cubic = _poly_cube(
        _poly_add_constant(voltage, -_point(1, precision))
    )
    fast = _poly_add(
        fast,
        _poly_scale(_poly_sub(delayed_cubic, current_cubic), epsilon * kappa_3),
    )
    if pulse_on:
        fast = _poly_add_constant(
            fast, _fraction_interval(PULSE_AMPLITUDE, precision)
        )
    slow = _poly_scale(
        _poly_sub(
            _poly_sub(voltage, recovery),
            (_fraction_interval(UNFOLDING, precision),),
        ),
        epsilon,
    )
    fast_residual = _poly_sub(fast, _poly_time_derivative(voltage, step))
    slow_residual = _poly_sub(slow, _poly_time_derivative(recovery, step))
    return _p_box_norm_upper(
        _poly_l1_upper(fast_residual),
        _poly_l1_upper(slow_residual),
        precision,
    )


def _guide_endpoint(
    polynomial: Sequence[gmpy2.mpfr], precision: int
) -> tuple[gmpy2.mpfr, DirectedInterval]:
    intervals = tuple(_mpfr_point(value, precision) for value in polynomial)
    exact_interval = _point(0, precision)
    for coefficient in intervals:
        exact_interval = exact_interval + coefficient
    with gmpy2.context(precision=precision, round=gmpy2.RoundToNearest):
        center = sum(polynomial, gmpy2.mpfr(0))
    return center, exact_interval


def _center_jump_norm(
    centers: tuple[gmpy2.mpfr, gmpy2.mpfr],
    endpoint_intervals: tuple[DirectedInterval, DirectedInterval],
    precision: int,
) -> gmpy2.mpfr:
    first = (endpoint_intervals[0] - _mpfr_point(centers[0], precision)).upper_abs()
    second = (endpoint_intervals[1] - _mpfr_point(centers[1], precision)).upper_abs()
    return _p_box_norm_upper(first, second, precision)


def _symmetric_enlargement(
    value: DirectedInterval, radius: gmpy2.mpfr
) -> DirectedInterval:
    precision = value.precision
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        lower = value.lower - radius
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        upper = value.upper + radius
    return DirectedInterval(lower, upper, precision)


def _gronwall_endpoint(
    initial_radius: gmpy2.mpfr,
    forcing: gmpy2.mpfr,
    logarithmic_norm: gmpy2.mpfr,
    elapsed: gmpy2.mpfr,
    precision: int,
) -> gmpy2.mpfr:
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        mu = max(gmpy2.mpfr(0), logarithmic_norm)
        if mu == 0:
            return initial_radius + elapsed * forcing
        exponential = gmpy2.exp(mu * elapsed)
        return exponential * initial_radius + (exponential - 1) / mu * forcing


@dataclass(frozen=True)
class _CellProof:
    left: _Node
    right: _Node
    voltage: tuple[gmpy2.mpfr, ...]
    recovery: tuple[gmpy2.mpfr, ...]
    voltage_range: DirectedInterval
    endpoint_radius: gmpy2.mpfr
    maximum_radius: gmpy2.mpfr
    residual_upper: gmpy2.mpfr
    logarithmic_norm_upper: gmpy2.mpfr
    delay_four_forcing_upper: gmpy2.mpfr
    delay_five_forcing_upper: gmpy2.mpfr
    closure_gap_lower: gmpy2.mpfr
    center_jump_upper: gmpy2.mpfr


def _translated_source(
    cells: Mapping[tuple[int, int, int, int], _CellProof],
    left: _Node,
    right: _Node,
    delay: int,
    history_voltage: tuple[gmpy2.mpfr, ...],
    history_error: gmpy2.mpfr,
) -> tuple[tuple[gmpy2.mpfr, ...], DirectedInterval, gmpy2.mpfr]:
    source_left = left.shifted(delay)
    source_right = right.shifted(delay)
    if _node_compare(source_right, ZERO_NODE) <= 0:
        point = _mpfr_point(history_voltage[0], PRECISION_BITS)
        return history_voltage, point, history_error
    if _node_compare(source_left, ZERO_NODE) < 0:
        raise AssertionError("a delayed cell crossed the initial-history seam")
    source = cells.get(_cell_key(source_left, source_right))
    if source is None:
        raise AssertionError("an exact delayed cell was not previously completed")
    return source.voltage, source.voltage_range, source.maximum_radius


@lru_cache(maxsize=1)
def exact_pulse_capture_defects() -> tuple[sp.Expr, ...]:
    """Exact algebra behind the field split, P norm, and log norm."""

    v, w, d, epsilon, k1, k3 = sp.symbols(
        "v w d epsilon k1 k3", real=True
    )
    p, q, r, a, lam = sp.symbols("p q r a lambda", real=True)
    local_fast = v - v**3 / 3 - w - epsilon * k1 * v - epsilon * k3 * (v - 1) ** 3
    delayed_fast = epsilon / 2 * (k1 * d + k3 * (d - 1) ** 3)
    current_derivative = 1 - v**2 - epsilon * k1 - 3 * epsilon * k3 * (v - 1) ** 2
    delayed_derivative = epsilon / 2 * (k1 + 3 * k3 * (d - 1) ** 2)
    matrix_p = sp.Matrix([[p, q], [q, r]])
    matrix_a = sp.Matrix([[a, -1], [epsilon, -epsilon]])
    symmetric = sp.simplify((matrix_p * matrix_a + matrix_a.T * matrix_p) / 2)
    determinant_identity = sp.expand(
        (symmetric - lam * matrix_p).det()
        - (
            (p * r - q**2) * lam**2
            - (
                r * symmetric[0, 0]
                + p * symmetric[1, 1]
                - 2 * q * symmetric[0, 1]
            )
            * lam
            + symmetric.det()
        )
    )
    coordinate_identity = sp.simplify(
        sp.Matrix([1, 0]).dot(matrix_p.inv() * sp.Matrix([1, 0]))
        - r / (p * r - q**2)
    )
    forcing_dual_identity = sp.simplify(
        p * sp.Matrix([1, 0]).dot(matrix_p.inv() * sp.Matrix([1, 0]))
        - p * r / (p * r - q**2)
    )
    equilibrium_diagonal_identity = sp.expand(
        sp.Matrix([1, 1]).dot(matrix_p * sp.Matrix([1, 1]))
        - (p + 2 * q + r)
    )
    return tuple(
        sp.simplify(item)
        for item in (
            sp.diff(local_fast, v) - current_derivative,
            sp.diff(delayed_fast, d) - delayed_derivative,
            determinant_identity,
            coordinate_identity,
            sp.diff(epsilon * (v - sp.Rational(1, 4) - w), v) - epsilon,
            sp.diff(epsilon * (v - sp.Rational(1, 4) - w), w) + epsilon,
            forcing_dual_identity,
            equilibrium_diagonal_identity,
        )
    )


@dataclass(frozen=True)
class PulseQuietCaptureCertificate:
    schema_id: str
    model_id: str
    precision_bits: int
    grid_denominator: int
    taylor_degree: int
    pulse_amplitude: str
    pulse_interval: tuple[str, str]
    physical_delays: tuple[str, str]
    final_time_exact: str
    final_time_lower: str
    final_time_upper: str
    retained_history_interval_exact: tuple[str, str]
    grid_cell_count: int
    forced_cell_count: int
    released_cell_count: int
    retained_history_cell_count: int
    delay_four_translated_cell_count: int
    delay_five_translated_cell_count: int
    delay_four_initial_history_cell_count: int
    delay_five_initial_history_cell_count: int
    alpha_lower: str
    alpha_upper: str
    alpha_width_upper: str
    initial_p_error_radius_upper: str
    maximum_center_jump_upper: str
    maximum_guide_residual_upper: str
    maximum_current_p_logarithmic_norm_upper: str
    minimum_current_p_logarithmic_norm_upper: str
    maximum_delay_four_forcing_upper: str
    maximum_delay_five_forcing_upper: str
    maximum_validated_p_error_radius_upper: str
    maximum_retained_p_error_radius_upper: str
    minimum_cell_closure_gap_lower: str
    maximum_retained_guide_lyapunov_upper: str
    maximum_retained_total_p_norm_upper: str
    maximum_retained_total_lyapunov_upper: str
    quiet_basin_p_norm_threshold_lower: str
    retained_history_p_norm_margin_lower: str
    maximizing_retained_cell_index: int
    exact_symbolic_zero_defect_count: int
    theorem_statement: str
    exact_alpha_enclosure_validated: bool
    exact_union_grid_ordering_validated: bool
    pulse_release_isolated_at_one_validated: bool
    both_delay_cells_translate_exactly_validated: bool
    current_p_logarithmic_norm_enclosed: bool
    delay_four_error_forcing_enclosed: bool
    delay_five_error_forcing_enclosed: bool
    directed_taylor_method_of_steps_closed: bool
    complete_retained_history_bernstein_bound_validated: bool
    pulse_J_030_enters_large_quiet_ball_validated: bool
    pulse_J_030_quiet_capture_proved: bool
    pulse_J_032_outer_capture_validated: bool
    history_space_separator_validated: bool
    unique_physical_pulse_onset_validated: bool
    physical_pulse_transversality_validated: bool
    canard_root_equals_physical_onset_proved: bool
    global_quiet_basin_validated: bool


@lru_cache(maxsize=1)
def build_pulse_quiet_capture_certificate() -> PulseQuietCaptureCertificate:
    """Run the complete directed method-of-steps and terminal-history proof."""

    if exact_pulse_capture_defects() != (0,) * 8:
        raise AssertionError("the exact pulse-capture algebra changed")
    precision = PRECISION_BITS
    nodes = _forward_nodes()
    alpha = _alpha_interval(precision)
    alpha_lower_numerator, alpha_lower_denominator = (
        alpha.lower.as_integer_ratio()
    )
    alpha_upper_numerator, alpha_upper_denominator = (
        alpha.upper.as_integer_ratio()
    )
    alpha_lower_exact = Fraction(
        int(alpha_lower_numerator), int(alpha_lower_denominator)
    )
    alpha_upper_exact = Fraction(
        int(alpha_upper_numerator), int(alpha_upper_denominator)
    )
    if not alpha_lower_exact**3 < Fraction(3, 4) < alpha_upper_exact**3:
        raise ArithmeticError("the directed equilibrium cuberoot failed")
    alpha_center = _nearest_midpoint(alpha)
    with gmpy2.context(precision=precision, round=gmpy2.RoundToNearest):
        recovery_center = alpha_center - (
            gmpy2.mpfr(UNFOLDING.numerator) / UNFOLDING.denominator
        )
    coordinate_bound, _, alpha_diagonal = _p_constants(precision)
    alpha_center_interval = _mpfr_point(alpha_center, precision)
    alpha_difference = (alpha - alpha_center_interval).upper_abs()
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        initial_error = alpha_diagonal * alpha_difference

    history_voltage = tuple(
        [alpha_center] + [gmpy2.mpfr(0)] * TAYLOR_DEGREE
    )
    cells: dict[tuple[int, int, int, int], _CellProof] = {}
    previous: _CellProof | None = None
    forced_count = 0
    delay_initial_counts = {4: 0, 5: 0}
    delay_translated_counts = {4: 0, 5: 0}
    maximum_center_jump = gmpy2.mpfr(0)
    maximum_residual = gmpy2.mpfr(0)
    maximum_log_norm = -gmpy2.inf()
    minimum_log_norm = gmpy2.inf()
    maximum_delay_forcing = {4: gmpy2.mpfr(0), 5: gmpy2.mpfr(0)}
    maximum_error = initial_error
    minimum_closure_gap = gmpy2.inf()

    for left, right in zip(nodes[:-1], nodes[1:], strict=True):
        left_time = _node_interval(left, precision)
        right_time = _node_interval(right, precision)
        step_interval = right_time - left_time
        if step_interval.lower <= 0:
            raise AssertionError("a directed union-grid step is not positive")
        step_center = _nearest_midpoint(step_interval)
        if _node_compare(left, PULSE_RELEASE_NODE) < 0:
            if _node_compare(right, PULSE_RELEASE_NODE) > 0:
                raise AssertionError("a cell crossed the physical pulse release")
            pulse_on = True
            forced_count += 1
        else:
            pulse_on = False

        source_data: dict[
            int,
            tuple[tuple[gmpy2.mpfr, ...], DirectedInterval, gmpy2.mpfr],
        ] = {}
        for delay in DELAY_MULTIPLIERS:
            source_data[delay] = _translated_source(
                cells,
                left,
                right,
                delay,
                history_voltage,
                initial_error,
            )
            if _node_compare(right.shifted(delay), ZERO_NODE) <= 0:
                delay_initial_counts[delay] += 1
            else:
                delay_translated_counts[delay] += 1

        if previous is None:
            start = (alpha_center, recovery_center)
            start_error = initial_error
            center_jump = gmpy2.mpfr(0)
        else:
            voltage_start, voltage_endpoint_interval = _guide_endpoint(
                previous.voltage, precision
            )
            recovery_start, recovery_endpoint_interval = _guide_endpoint(
                previous.recovery, precision
            )
            start = (voltage_start, recovery_start)
            center_jump = _center_jump_norm(
                start,
                (voltage_endpoint_interval, recovery_endpoint_interval),
                precision,
            )
            with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
                start_error = previous.endpoint_radius + center_jump

        voltage, recovery = _taylor_guide(
            start,
            step_center,
            source_data[4][0],
            source_data[5][0],
            pulse_on,
            TAYLOR_DEGREE,
            precision,
        )
        voltage_polynomial = tuple(_mpfr_point(value, precision) for value in voltage)
        voltage_range = _poly_bernstein_range(voltage_polynomial)
        residual = _guide_residual_upper(
            voltage,
            recovery,
            source_data[4][0],
            source_data[5][0],
            step_interval,
            pulse_on,
        )

        with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
            radius = (
                max(start_error, gmpy2.mpfr(TUBE_FLOOR))
                * gmpy2.mpfr(TUBE_INFLATION)
                + gmpy2.mpfr(TUBE_FLOOR)
            )
        closure_gap = None
        endpoint_radius = None
        log_norm = None
        forcing_four = None
        forcing_five = None
        for _ in range(MAXIMUM_FIXED_POINT_ITERATIONS):
            with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
                voltage_error = coordinate_bound * radius
            current_tube = _symmetric_enlargement(voltage_range, voltage_error)
            log_norm = _current_log_norm_upper(current_tube, precision)
            delay_forcings: dict[int, gmpy2.mpfr] = {}
            for delay in DELAY_MULTIPLIERS:
                delayed_guide_range = source_data[delay][1]
                delayed_error_radius = source_data[delay][2]
                with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
                    delayed_voltage_error = coordinate_bound * delayed_error_radius
                delayed_tube = _symmetric_enlargement(
                    delayed_guide_range, delayed_voltage_error
                )
                delay_forcings[delay] = _delayed_forcing_upper(
                    delayed_tube, precision
                )
            forcing_four = delay_forcings[4]
            forcing_five = delay_forcings[5]
            with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
                total_forcing = (
                    residual
                    + forcing_four * source_data[4][2]
                    + forcing_five * source_data[5][2]
                )
            endpoint_radius = _gronwall_endpoint(
                start_error,
                total_forcing,
                log_norm,
                step_interval.upper,
                precision,
            )
            with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
                closure_gap = radius - endpoint_radius
            if closure_gap > 0:
                break
            with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
                radius = (
                    max(radius, endpoint_radius)
                    * gmpy2.mpfr(TUBE_INFLATION)
                    + gmpy2.mpfr(TUBE_FLOOR)
                )
        else:
            raise ArithmeticError(
                f"the P-error tube failed on cell {_cell_key(left, right)}"
            )
        assert closure_gap is not None
        assert endpoint_radius is not None
        assert log_norm is not None
        assert forcing_four is not None
        assert forcing_five is not None
        proof = _CellProof(
            left=left,
            right=right,
            voltage=voltage,
            recovery=recovery,
            voltage_range=voltage_range,
            endpoint_radius=endpoint_radius,
            maximum_radius=radius,
            residual_upper=residual,
            logarithmic_norm_upper=log_norm,
            delay_four_forcing_upper=forcing_four,
            delay_five_forcing_upper=forcing_five,
            closure_gap_lower=closure_gap,
            center_jump_upper=center_jump,
        )
        cells[_cell_key(left, right)] = proof
        previous = proof
        maximum_center_jump = max(maximum_center_jump, center_jump)
        maximum_residual = max(maximum_residual, residual)
        maximum_log_norm = max(maximum_log_norm, log_norm)
        minimum_log_norm = min(minimum_log_norm, log_norm)
        maximum_delay_forcing[4] = max(maximum_delay_forcing[4], forcing_four)
        maximum_delay_forcing[5] = max(maximum_delay_forcing[5], forcing_five)
        maximum_error = max(maximum_error, radius)
        minimum_closure_gap = min(minimum_closure_gap, closure_gap)

    # The large-basin Lyapunov function is centered at the exact equilibrium,
    # not at the nearest MPFR guide center.  Retaining the full alpha interval
    # here encloses that final change of center, including its P cross term.
    alpha_polynomial = (alpha,)
    equilibrium_recovery = _poly_add_constant(
        alpha_polynomial, -_fraction_interval(UNFOLDING, precision)
    )
    p11 = _fraction_interval(P11, precision)
    p12 = _fraction_interval(P12, precision)
    p22 = _fraction_interval(P22, precision)
    threshold = _fraction_interval(HISTORY_SUBLEVEL, precision).sqrt()
    retained_count = 0
    maximizing_retained = -1
    maximum_guide_v = gmpy2.mpfr(0)
    maximum_total_norm = gmpy2.mpfr(0)
    maximum_retained_error = gmpy2.mpfr(0)
    minimum_retained_margin = gmpy2.inf()
    for cell_index, proof in enumerate(cells.values()):
        if _node_compare(proof.right, RETAINED_LEFT_NODE) <= 0:
            continue
        if _node_compare(proof.left, RETAINED_LEFT_NODE) < 0:
            raise AssertionError("the retained-history left endpoint split a cell")
        retained_count += 1
        voltage_poly = tuple(_mpfr_point(value, precision) for value in proof.voltage)
        recovery_poly = tuple(_mpfr_point(value, precision) for value in proof.recovery)
        x = _poly_sub(voltage_poly, alpha_polynomial)
        y = _poly_sub(recovery_poly, equilibrium_recovery)
        lyapunov = _poly_add(
            _poly_add(
                _poly_scale(_poly_multiply(x, x), p11),
                _poly_scale(_poly_multiply(x, y), 2 * p12),
            ),
            _poly_scale(_poly_multiply(y, y), p22),
        )
        guide_range = _poly_bernstein_range(lyapunov)
        if guide_range.upper < 0:
            raise ArithmeticError("a nonnegative guide Lyapunov polynomial is negative")
        with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
            guide_norm = gmpy2.sqrt(max(gmpy2.mpfr(0), guide_range.upper))
            total_norm = guide_norm + proof.maximum_radius
        with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
            margin = threshold.lower - total_norm
        if margin <= 0:
            raise ArithmeticError(
                f"the retained-history basin margin failed on cell {cell_index}"
            )
        if total_norm > maximum_total_norm:
            maximum_total_norm = total_norm
            maximizing_retained = cell_index
        maximum_guide_v = max(maximum_guide_v, guide_range.upper)
        maximum_retained_error = max(
            maximum_retained_error, proof.maximum_radius
        )
        minimum_retained_margin = min(minimum_retained_margin, margin)

    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        maximum_total_lyapunov = maximum_total_norm * maximum_total_norm
    final_time = _node_interval(FINAL_NODE, precision)
    return PulseQuietCaptureCertificate(
        schema_id=SCHEMA_ID,
        model_id=MODEL_ID,
        precision_bits=precision,
        grid_denominator=GRID_DENOMINATOR,
        taylor_degree=TAYLOR_DEGREE,
        pulse_amplitude=str(PULSE_AMPLITUDE),
        pulse_interval=("0", "1"),
        physical_delays=("4*sqrt(5)", "5*sqrt(5)"),
        final_time_exact="161*sqrt(5)",
        final_time_lower=_lower_text(final_time.lower),
        final_time_upper=_upper_text(final_time.upper),
        retained_history_interval_exact=("156*sqrt(5)", "161*sqrt(5)"),
        grid_cell_count=len(cells),
        forced_cell_count=forced_count,
        released_cell_count=len(cells) - forced_count,
        retained_history_cell_count=retained_count,
        delay_four_translated_cell_count=delay_translated_counts[4],
        delay_five_translated_cell_count=delay_translated_counts[5],
        delay_four_initial_history_cell_count=delay_initial_counts[4],
        delay_five_initial_history_cell_count=delay_initial_counts[5],
        alpha_lower=_lower_text(alpha.lower),
        alpha_upper=_upper_text(alpha.upper),
        alpha_width_upper=_upper_text(alpha.width_upper()),
        initial_p_error_radius_upper=_upper_text(initial_error),
        maximum_center_jump_upper=_upper_text(maximum_center_jump),
        maximum_guide_residual_upper=_upper_text(maximum_residual),
        maximum_current_p_logarithmic_norm_upper=_upper_text(maximum_log_norm),
        minimum_current_p_logarithmic_norm_upper=_upper_text(minimum_log_norm),
        maximum_delay_four_forcing_upper=_upper_text(maximum_delay_forcing[4]),
        maximum_delay_five_forcing_upper=_upper_text(maximum_delay_forcing[5]),
        maximum_validated_p_error_radius_upper=_upper_text(maximum_error),
        maximum_retained_p_error_radius_upper=_upper_text(maximum_retained_error),
        minimum_cell_closure_gap_lower=_lower_text(minimum_closure_gap),
        maximum_retained_guide_lyapunov_upper=_upper_text(maximum_guide_v),
        maximum_retained_total_p_norm_upper=_upper_text(maximum_total_norm),
        maximum_retained_total_lyapunov_upper=_upper_text(maximum_total_lyapunov),
        quiet_basin_p_norm_threshold_lower=_lower_text(threshold.lower),
        retained_history_p_norm_margin_lower=_lower_text(minimum_retained_margin),
        maximizing_retained_cell_index=maximizing_retained,
        exact_symbolic_zero_defect_count=8,
        theorem_statement=(
            "the solution from the exact quiet history under u(t)=3/10 for "
            "0<=t<1 and u(t)=0 for t>=1 satisfies sup_{theta in "
            "[-5*sqrt(5),0]} V(z(161*sqrt(5)+theta)-E_q)<1/125 and "
            "therefore converges exponentially to the quiet equilibrium"
        ),
        **{name: True for name in TRUE_FLAGS},
        **{name: False for name in FALSE_FLAGS},
    )


def canonical_sha256(value: Any) -> str:
    return sha256(
        json.dumps(
            value, sort_keys=True, separators=(",", ":"), ensure_ascii=True
        ).encode("ascii")
    ).hexdigest()


def _sha256_path(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def build_pulse_quiet_capture_result(repository: Path) -> dict[str, Any]:
    large_path = repository / LARGE_BASIN_RESULT_RELATIVE_PATH
    large_payload = json.loads(large_path.read_text(encoding="utf-8"))
    validate_large_quiet_basin_result(large_payload, repository)
    terminal_path = repository / PULSE_TERMINAL_RESULT_RELATIVE_PATH
    terminal_payload = json.loads(terminal_path.read_text(encoding="utf-8"))
    validate_pulse_terminal_history_result(terminal_payload, repository)
    certificate = json.loads(
        json.dumps(asdict(build_pulse_quiet_capture_certificate()))
    )
    sources = {
        "source": SOURCE_RELATIVE_PATH,
        "generator": GENERATOR_RELATIVE_PATH,
        "note": NOTE_RELATIVE_PATH,
        "interval_source": INTERVAL_SOURCE_RELATIVE_PATH,
        "model_source": MODEL_SOURCE_RELATIVE_PATH,
        "pulse_terminal_source": PULSE_TERMINAL_SOURCE_RELATIVE_PATH,
        "large_basin_source": LARGE_BASIN_SOURCE_RELATIVE_PATH,
        "quiet_p_source": QUIET_P_SOURCE_RELATIVE_PATH,
    }
    return {
        "certificate": certificate,
        "manifest": {
            "schema_id": SCHEMA_ID,
            "result": RESULT_RELATIVE_PATH,
            "default_command": DEFAULT_COMMAND,
            "arithmetic": MANIFEST_ARITHMETIC,
            "python": platform.python_version(),
            "platform": platform.platform(),
            "gmpy2": gmpy2.__version__,
            "mpfr": gmpy2.mpfr_version(),
            "sympy": sp.__version__,
            "certificate_sha256": canonical_sha256(certificate),
            "large_basin_result": LARGE_BASIN_RESULT_RELATIVE_PATH,
            "large_basin_result_sha256": _sha256_path(large_path),
            "pulse_terminal_result": PULSE_TERMINAL_RESULT_RELATIVE_PATH,
            "pulse_terminal_result_sha256": _sha256_path(terminal_path),
            "source_sha256": {
                name: _sha256_path(repository / relative)
                for name, relative in sources.items()
            },
            **sources,
        },
    }


def validate_pulse_quiet_capture_result(
    payload: Mapping[str, Any], repository: Path
) -> None:
    if not isinstance(payload, Mapping) or set(payload) != {
        "certificate",
        "manifest",
    }:
        raise ValueError("pulse quiet-capture result has the wrong outer schema")
    certificate = payload.get("certificate")
    manifest = payload.get("manifest")
    if not isinstance(certificate, Mapping) or not isinstance(manifest, Mapping):
        raise ValueError("pulse quiet-capture records must be mappings")
    if set(certificate) != {
        field.name for field in fields(PulseQuietCaptureCertificate)
    }:
        raise ValueError("pulse quiet-capture certificate schema changed")
    expected_certificate = json.loads(
        json.dumps(asdict(build_pulse_quiet_capture_certificate()))
    )
    normalized_certificate = json.loads(json.dumps(certificate))
    for name, expected_value in expected_certificate.items():
        if type(normalized_certificate.get(name)) is not type(expected_value):
            raise ValueError(
                f"pulse quiet-capture certificate {name} has the wrong type"
            )
    if normalized_certificate != expected_certificate:
        raise ValueError("pulse quiet-capture certificate differs from replay")
    if any(certificate.get(name) is not True for name in TRUE_FLAGS):
        raise ValueError("a proved pulse quiet-capture flag was weakened")
    if any(certificate.get(name) is not False for name in FALSE_FLAGS):
        raise ValueError("an open onset/outer/separator flag was promoted")

    sources = {
        "source": SOURCE_RELATIVE_PATH,
        "generator": GENERATOR_RELATIVE_PATH,
        "note": NOTE_RELATIVE_PATH,
        "interval_source": INTERVAL_SOURCE_RELATIVE_PATH,
        "model_source": MODEL_SOURCE_RELATIVE_PATH,
        "pulse_terminal_source": PULSE_TERMINAL_SOURCE_RELATIVE_PATH,
        "large_basin_source": LARGE_BASIN_SOURCE_RELATIVE_PATH,
        "quiet_p_source": QUIET_P_SOURCE_RELATIVE_PATH,
    }
    expected_manifest_keys = {
        "schema_id",
        "result",
        "default_command",
        "arithmetic",
        "python",
        "platform",
        "gmpy2",
        "mpfr",
        "sympy",
        "certificate_sha256",
        "large_basin_result",
        "large_basin_result_sha256",
        "pulse_terminal_result",
        "pulse_terminal_result_sha256",
        "source_sha256",
        *sources,
    }
    if set(manifest) != expected_manifest_keys:
        raise ValueError("pulse quiet-capture manifest schema changed")
    scalar_expected = {
        "schema_id": SCHEMA_ID,
        "result": RESULT_RELATIVE_PATH,
        "default_command": DEFAULT_COMMAND,
        "arithmetic": MANIFEST_ARITHMETIC,
        "python": platform.python_version(),
        "platform": platform.platform(),
        "gmpy2": gmpy2.__version__,
        "mpfr": gmpy2.mpfr_version(),
        "sympy": sp.__version__,
        "large_basin_result": LARGE_BASIN_RESULT_RELATIVE_PATH,
        "pulse_terminal_result": PULSE_TERMINAL_RESULT_RELATIVE_PATH,
    }
    for name, expected in scalar_expected.items():
        if manifest.get(name) != expected:
            raise ValueError(f"pulse quiet-capture manifest {name} changed")
    if manifest.get("certificate_sha256") != canonical_sha256(
        normalized_certificate
    ):
        raise ValueError("pulse quiet-capture certificate digest changed")
    parent_results = {
        "large_basin_result": LARGE_BASIN_RESULT_RELATIVE_PATH,
        "pulse_terminal_result": PULSE_TERMINAL_RESULT_RELATIVE_PATH,
    }
    for name, relative in parent_results.items():
        if manifest.get(f"{name}_sha256") != _sha256_path(repository / relative):
            raise ValueError(f"pulse quiet-capture parent {name} hash changed")
    validate_large_quiet_basin_result(
        json.loads((repository / LARGE_BASIN_RESULT_RELATIVE_PATH).read_text()),
        repository,
    )
    validate_pulse_terminal_history_result(
        json.loads((repository / PULSE_TERMINAL_RESULT_RELATIVE_PATH).read_text()),
        repository,
    )
    source_hashes = manifest.get("source_sha256")
    if not isinstance(source_hashes, Mapping) or set(source_hashes) != set(sources):
        raise ValueError("pulse quiet-capture source-hash schema changed")
    for name, relative in sources.items():
        if manifest.get(name) != relative:
            raise ValueError(f"pulse quiet-capture {name} path changed")
        if source_hashes.get(name) != _sha256_path(repository / relative):
            raise ValueError(f"pulse quiet-capture {name} hash changed")
