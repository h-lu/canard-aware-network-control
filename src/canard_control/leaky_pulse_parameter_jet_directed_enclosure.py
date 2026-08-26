"""Directed Stage-5B enclosure for the correlated physical-pulse jet.

The parameter is normalized by ``xi=(J-J0)/h`` with
``J0=2409/8000`` and ``h=3/40000``.  The jointly propagated coefficients

    B(t,xi)=sum_{k=0}^4 b_k(t) xi^k,
    b_k=h^k partial_J^k z(t,J0)/k!,

remain at their physically scaled sizes.  A degree-24 time-Taylor guide is
validated for the ten-dimensional triangular RFDE satisfied by
``b_0,...,b_4``.  Separately, the degree-five-and-higher part of the cubic
substitution is bounded and propagated as a full-family remainder.  Neither
calculation uses the old zero-centered variation majorants.

This module initially exposes the directed computational core.  Event-time,
complete-history section, stable-coordinate, onset, and routing claims are
outside its scope.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
import json
import math
from pathlib import Path
from typing import Any, Mapping, Sequence

import gmpy2

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
from canard_control.leaky_pulse_quiet_capture import (
    FINAL_NODE_INDEX as QUIET_FINAL_NODE_INDEX,
    GRID_DENOMINATOR,
    MAXIMUM_FIXED_POINT_ITERATIONS,
    PRECISION_BITS,
    PULSE_RELEASE_NODE,
    TAYLOR_DEGREE as PARENT_TAYLOR_DEGREE,
    TUBE_FLOOR,
    TUBE_INFLATION,
    ZERO_NODE,
    _Node,
    _alpha_interval,
    _cell_key,
    _current_log_norm_upper,
    _forward_nodes,
    _fraction_interval,
    _gronwall_endpoint,
    _guide_endpoint,
    _mpfr_point,
    _nearest_midpoint,
    _node_compare,
    _node_interval,
    _p_box_norm_upper,
    _p_constants,
    _point,
    _poly_add,
    _poly_add_constant,
    _poly_bernstein_range,
    _poly_l1_upper,
    _poly_multiply,
    _poly_scale,
    _poly_sub,
    _poly_time_derivative,
    _symmetric_enlargement,
)
from canard_control.leaky_quiet_history_basin import P11, P12, P22


SCHEMA_ID = "leaky-pulse-parameter-jet-directed-enclosure-v1"
MODEL_ID = "autonomous-leaky-recovery-physical-pulse"

SOURCE_RELATIVE_PATH = (
    "src/canard_control/leaky_pulse_parameter_jet_directed_enclosure.py"
)
GENERATOR_RELATIVE_PATH = (
    "experiments/leaky_pulse_parameter_jet_directed_enclosure.py"
)
RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_pulse_parameter_jet_directed_enclosure.json"
)
NOTE_RELATIVE_PATH = "docs/leaky-pulse-parameter-jet-directed-enclosure.md"
TEST_RELATIVE_PATH = (
    "tests/test_leaky_pulse_parameter_jet_directed_enclosure.py"
)
STAGE5_CONTRACT_RELATIVE_PATH = (
    "experiments/results/leaky_pulse_event_aligned_parameter_jet_contract.json"
)
STAGE5_CONTRACT_SHA256 = (
    "12993314508d7b31de1ef7e5988b9dbd0798347eee73309d381774faa0d21646"
)
STAGE5A_PILOT_RELATIVE_PATH = (
    "experiments/results/leaky_pulse_parameter_jet_center_pilot.json"
)
STAGE5A_PILOT_SHA256 = (
    "5743c16636e449c921cea45f1b8000c4a043200630d973f7cdfdecd20b740819"
)
FAMILY_PARENT_RELATIVE_PATH = (
    "experiments/results/leaky_pulse_inner_route_c_family_contract.json"
)
FAMILY_PARENT_SHA256 = (
    "6821551f3fab7d4bbc073af20b83daf055482055a81db23664d31c017de81f7c"
)
SOURCE_MANIFEST = (
    SOURCE_RELATIVE_PATH,
    GENERATOR_RELATIVE_PATH,
    NOTE_RELATIVE_PATH,
)
DEPENDENCY_SOURCE_MANIFEST = (
    "src/canard_control/autonomous_leaky_recovery_bistable.py",
    "src/canard_control/directed_interval.py",
    "src/canard_control/leaky_pulse_quiet_capture.py",
    "src/canard_control/leaky_quiet_history_basin.py",
)
DEFAULT_COMMAND = (
    "OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 "
    "PYTHONPATH=.venv/lib/python3.14/site-packages:src /usr/bin/python3 "
    "experiments/leaky_pulse_parameter_jet_directed_enclosure.py"
)
ARITHMETIC_SCOPE = (
    "192-bit outward MPFR on the exact Q(sqrt(5)) two-origin 1152-cell "
    "grid; degree-16 time-Taylor/Bernstein guides for the jointly scaled "
    "parameter coefficients b_k=h^k partial_J^k z/k!, k=0,...,4; block "
    "P-logarithmic norm validation of the triangular coefficient RFDE; "
    "directed cubic parameter convolution through degree twelve; and a "
    "cellwise full-width order-five remainder tube"
)

J0 = Fraction(2409, 8000)
PARAMETER_HALF_WIDTH = Fraction(3, 40000)
PARAMETER_INTERVAL = (J0 - PARAMETER_HALF_WIDTH, J0 + PARAMETER_HALF_WIDTH)
PARAMETER_DEGREE = 4
TAIL_MAXIMUM_DEGREE = 3 * PARAMETER_DEGREE
JET_TAYLOR_DEGREE = 16
if JET_TAYLOR_DEGREE > PARENT_TAYLOR_DEGREE:
    raise AssertionError("the jet guide exceeds the parent Taylor workspace")
DELAY_MULTIPLIERS = (4, 5)
FINAL_SQRT5_MULTIPLIER = 24
FINAL_NODE = _Node(0, FINAL_SQRT5_MULTIPLIER * GRID_DENOMINATOR)

TRUE_FLAGS = (
    "exact_wide_parameter_scaling_validated",
    "exact_two_origin_grid_and_delay_translation_validated",
    "joint_scaled_coefficient_equations_b0_through_b4_validated",
    "directed_coefficient_time_guides_closed_on_all_cells",
    "continuous_time_coefficient_bernstein_envelopes_validated",
    "cubic_parameter_degrees_five_through_twelve_bounded",
    "full_width_order_five_remainder_tube_closed_on_all_cells",
    "fixed_time_wide_parameter_taylor_model_validated",
)

FALSE_FLAGS = (
    "route_c_event_bracket_validated",
    "route_c_event_speed_validated",
    "event_time_parameter_jet_validated",
    "common_event_complete_history_jet_validated",
    "rfde_unstable_riesz_covector_validated",
    "inner_local_stable_graph_validated",
    "stable_coordinate_endpoint_signs_validated",
    "interval_newton_onset_validated",
    "unique_physical_pulse_onset_validated",
    "two_sided_basin_routing_validated",
)


def _nodes() -> tuple[_Node, ...]:
    if QUIET_FINAL_NODE_INDEX <= FINAL_NODE.index:
        raise AssertionError("the parent grid is too short")
    nodes = tuple(
        node for node in _forward_nodes() if _node_compare(node, FINAL_NODE) <= 0
    )
    if nodes[0] != ZERO_NODE or nodes[-1] != FINAL_NODE:
        raise AssertionError("the directed jet horizon is absent from the grid")
    return nodes


def _zero_mpfr_vector() -> list[gmpy2.mpfr]:
    return [gmpy2.mpfr(0) for _ in range(PARAMETER_DEGREE + 1)]


def _append_square_and_cube_nearest(
    value: Sequence[Sequence[gmpy2.mpfr]],
    square: list[list[gmpy2.mpfr]],
    time_order: int,
    precision: int,
) -> list[gmpy2.mpfr]:
    """Append one time coefficient of ``value**2`` and return ``value**3``."""

    with gmpy2.context(precision=precision, round=gmpy2.RoundToNearest):
        square_at_order = _zero_mpfr_vector()
        for parameter_order in range(PARAMETER_DEGREE + 1):
            total = gmpy2.mpfr(0)
            for left_parameter in range(parameter_order + 1):
                right_parameter = parameter_order - left_parameter
                for left_time in range(time_order + 1):
                    right_time = time_order - left_time
                    if (
                        left_time < len(value[left_parameter])
                        and right_time < len(value[right_parameter])
                    ):
                        total += (
                            value[left_parameter][left_time]
                            * value[right_parameter][right_time]
                        )
            square_at_order[parameter_order] = total
            square[parameter_order].append(total)

        cube_at_order = _zero_mpfr_vector()
        for parameter_order in range(PARAMETER_DEGREE + 1):
            total = gmpy2.mpfr(0)
            for square_parameter in range(parameter_order + 1):
                value_parameter = parameter_order - square_parameter
                for square_time in range(time_order + 1):
                    value_time = time_order - square_time
                    if value_time < len(value[value_parameter]):
                        total += (
                            square[square_parameter][square_time]
                            * value[value_parameter][value_time]
                        )
            cube_at_order[parameter_order] = total
        return cube_at_order


def _all_cube_coefficients_nearest(
    value: Sequence[Sequence[gmpy2.mpfr]],
    maximum_time_order: int,
    precision: int,
) -> list[list[gmpy2.mpfr]]:
    square = [[] for _ in range(PARAMETER_DEGREE + 1)]
    cube = [[] for _ in range(PARAMETER_DEGREE + 1)]
    for time_order in range(maximum_time_order + 1):
        coefficient = _append_square_and_cube_nearest(
            value, square, time_order, precision
        )
        for parameter_order in range(PARAMETER_DEGREE + 1):
            cube[parameter_order].append(coefficient[parameter_order])
    return cube


def _shifted_nearest(
    value: Sequence[Sequence[gmpy2.mpfr]],
) -> list[list[gmpy2.mpfr]]:
    shifted = [list(order) for order in value]
    shifted[0][0] -= 1
    return shifted


def _coefficient_taylor_guide(
    start: Sequence[tuple[gmpy2.mpfr, gmpy2.mpfr]],
    step: gmpy2.mpfr,
    delayed_four: Sequence[Sequence[gmpy2.mpfr]],
    delayed_five: Sequence[Sequence[gmpy2.mpfr]],
    pulse_on: bool,
    degree: int,
    precision: int,
) -> tuple[
    tuple[tuple[gmpy2.mpfr, ...], ...],
    tuple[tuple[gmpy2.mpfr, ...], ...],
]:
    """Build the joint nearest-MPFR time guide for the scaled coefficients."""

    with gmpy2.context(precision=precision, round=gmpy2.RoundToNearest):
        epsilon = gmpy2.mpfr(EPSILON.numerator) / EPSILON.denominator
        unfolding = gmpy2.mpfr(UNFOLDING.numerator) / UNFOLDING.denominator
        kappa_1 = gmpy2.mpfr(KAPPA_1.numerator) / KAPPA_1.denominator
        kappa_3 = gmpy2.mpfr(KAPPA_3.numerator) / KAPPA_3.denominator
        pulse_center = gmpy2.mpfr(J0.numerator) / J0.denominator
        pulse_half_width = (
            gmpy2.mpfr(PARAMETER_HALF_WIDTH.numerator)
            / PARAMETER_HALF_WIDTH.denominator
        )
        half = gmpy2.mpfr(1) / 2
        third = gmpy2.mpfr(1) / 3
        voltage = [[gmpy2.mpfr(start[order][0])] for order in range(5)]
        recovery = [[gmpy2.mpfr(start[order][1])] for order in range(5)]
        shifted_voltage = _shifted_nearest(voltage)
        voltage_square = [[] for _ in range(5)]
        shifted_square = [[] for _ in range(5)]
        delayed_four_cube = _all_cube_coefficients_nearest(
            _shifted_nearest(delayed_four), degree - 1, precision
        )
        delayed_five_cube = _all_cube_coefficients_nearest(
            _shifted_nearest(delayed_five), degree - 1, precision
        )
        for time_order in range(degree):
            voltage_cube = _append_square_and_cube_nearest(
                voltage, voltage_square, time_order, precision
            )
            shifted_cube = _append_square_and_cube_nearest(
                shifted_voltage, shifted_square, time_order, precision
            )
            next_voltage = _zero_mpfr_vector()
            next_recovery = _zero_mpfr_vector()
            for parameter_order in range(5):
                fast = (
                    voltage[parameter_order][time_order]
                    - third * voltage_cube[parameter_order]
                    - recovery[parameter_order][time_order]
                    + epsilon
                    * kappa_1
                    * (
                        half
                        * (
                            delayed_four[parameter_order][time_order]
                            + delayed_five[parameter_order][time_order]
                        )
                        - voltage[parameter_order][time_order]
                    )
                    + epsilon
                    * kappa_3
                    * (
                        half
                        * (
                            delayed_four_cube[parameter_order][time_order]
                            + delayed_five_cube[parameter_order][time_order]
                        )
                        - shifted_cube[parameter_order]
                    )
                )
                if pulse_on and time_order == 0:
                    if parameter_order == 0:
                        fast += pulse_center
                    elif parameter_order == 1:
                        fast += pulse_half_width
                slow = epsilon * (
                    voltage[parameter_order][time_order]
                    - recovery[parameter_order][time_order]
                    - (
                        unfolding
                        if parameter_order == 0 and time_order == 0
                        else 0
                    )
                )
                next_voltage[parameter_order] = step * fast / (time_order + 1)
                next_recovery[parameter_order] = step * slow / (time_order + 1)
            for parameter_order in range(5):
                voltage[parameter_order].append(next_voltage[parameter_order])
                recovery[parameter_order].append(next_recovery[parameter_order])
                shifted_voltage[parameter_order].append(
                    next_voltage[parameter_order]
                )
        return (
            tuple(tuple(order) for order in voltage),
            tuple(tuple(order) for order in recovery),
        )


IntervalPolynomial = tuple[DirectedInterval, ...]
ParameterTimePolynomial = tuple[IntervalPolynomial, ...]


def _parameter_zero(precision: int, count: int = 5) -> ParameterTimePolynomial:
    zero = (_point(0, precision),)
    return tuple(zero for _ in range(count))


def _parameter_add(
    left: Sequence[IntervalPolynomial],
    right: Sequence[IntervalPolynomial],
    count: int,
) -> ParameterTimePolynomial:
    zero = (_point(0, left[0][0].precision),)
    return tuple(
        _poly_add(
            left[order] if order < len(left) else zero,
            right[order] if order < len(right) else zero,
        )
        for order in range(count)
    )


def _parameter_sub(
    left: Sequence[IntervalPolynomial],
    right: Sequence[IntervalPolynomial],
    count: int,
) -> ParameterTimePolynomial:
    zero = (_point(0, left[0][0].precision),)
    return tuple(
        _poly_sub(
            left[order] if order < len(left) else zero,
            right[order] if order < len(right) else zero,
        )
        for order in range(count)
    )


def _parameter_scale(
    value: Sequence[IntervalPolynomial], scalar: DirectedInterval
) -> ParameterTimePolynomial:
    return tuple(_poly_scale(order, scalar) for order in value)


def _parameter_multiply(
    left: Sequence[IntervalPolynomial],
    right: Sequence[IntervalPolynomial],
    count: int,
) -> ParameterTimePolynomial:
    precision = left[0][0].precision
    result: list[IntervalPolynomial] = []
    for order in range(count):
        total = (_point(0, precision),)
        for left_order in range(order + 1):
            right_order = order - left_order
            if left_order < len(left) and right_order < len(right):
                total = _poly_add(
                    total,
                    _poly_multiply(left[left_order], right[right_order]),
                )
        result.append(total)
    return tuple(result)


def _parameter_cube(
    value: Sequence[IntervalPolynomial], count: int
) -> ParameterTimePolynomial:
    return _parameter_multiply(
        _parameter_multiply(value, value, count), value, count
    )


def _parameter_shift_one(
    value: Sequence[IntervalPolynomial], count: int
) -> ParameterTimePolynomial:
    result = [tuple(order) for order in value[:count]]
    result[0] = _poly_add_constant(result[0], -_point(1, result[0][0].precision))
    return tuple(result)


def _guide_residual_upper(
    voltage_mpfr: Sequence[Sequence[gmpy2.mpfr]],
    recovery_mpfr: Sequence[Sequence[gmpy2.mpfr]],
    delayed_four_mpfr: Sequence[Sequence[gmpy2.mpfr]],
    delayed_five_mpfr: Sequence[Sequence[gmpy2.mpfr]],
    step: DirectedInterval,
    pulse_on: bool,
) -> gmpy2.mpfr:
    precision = step.precision
    voltage = tuple(
        tuple(_mpfr_point(value, precision) for value in order)
        for order in voltage_mpfr
    )
    recovery = tuple(
        tuple(_mpfr_point(value, precision) for value in order)
        for order in recovery_mpfr
    )
    delayed_four = tuple(
        tuple(_mpfr_point(value, precision) for value in order)
        for order in delayed_four_mpfr
    )
    delayed_five = tuple(
        tuple(_mpfr_point(value, precision) for value in order)
        for order in delayed_five_mpfr
    )
    epsilon = _fraction_interval(EPSILON, precision)
    unfolding = _fraction_interval(UNFOLDING, precision)
    kappa_1 = _fraction_interval(KAPPA_1, precision)
    kappa_3 = _fraction_interval(KAPPA_3, precision)
    half = _point(1, precision) / 2
    third = _point(1, precision) / 3
    voltage_cube = _parameter_cube(voltage, 5)
    shifted_cube = _parameter_cube(_parameter_shift_one(voltage, 5), 5)
    delayed_cubic = _parameter_scale(
        _parameter_add(
            _parameter_cube(_parameter_shift_one(delayed_four, 5), 5),
            _parameter_cube(_parameter_shift_one(delayed_five, 5), 5),
            5,
        ),
        half,
    )
    fast = _parameter_sub(
        voltage, _parameter_scale(voltage_cube, third), 5
    )
    fast = _parameter_sub(fast, recovery, 5)
    average_delay = _parameter_scale(
        _parameter_add(delayed_four, delayed_five, 5), half
    )
    fast = _parameter_add(
        fast,
        _parameter_scale(
            _parameter_sub(average_delay, voltage, 5), epsilon * kappa_1
        ),
        5,
    )
    fast = _parameter_add(
        fast,
        _parameter_scale(
            _parameter_sub(delayed_cubic, shifted_cube, 5),
            epsilon * kappa_3,
        ),
        5,
    )
    if pulse_on:
        fast = list(fast)
        fast[0] = _poly_add_constant(fast[0], _fraction_interval(J0, precision))
        fast[1] = _poly_add_constant(
            fast[1], _fraction_interval(PARAMETER_HALF_WIDTH, precision)
        )
        fast = tuple(fast)
    slow = _parameter_scale(
        _parameter_sub(voltage, recovery, 5), epsilon
    )
    slow = list(slow)
    slow[0] = _poly_add_constant(slow[0], -epsilon * unfolding)
    maximum = gmpy2.mpfr(0)
    for order in range(5):
        fast_residual = _poly_l1_upper(
            _poly_sub(fast[order], _poly_time_derivative(voltage[order], step))
        )
        slow_residual = _poly_l1_upper(
            _poly_sub(slow[order], _poly_time_derivative(recovery[order], step))
        )
        maximum = max(
            maximum,
            _p_box_norm_upper(fast_residual, slow_residual, precision),
        )
    return maximum


def _interval_parameter_multiply(
    left: Sequence[DirectedInterval],
    right: Sequence[DirectedInterval],
    count: int,
) -> tuple[DirectedInterval, ...]:
    precision = left[0].precision
    answer = []
    for order in range(count):
        total = _point(0, precision)
        for left_order in range(order + 1):
            right_order = order - left_order
            if left_order < len(left) and right_order < len(right):
                total = total + left[left_order] * right[right_order]
        answer.append(total)
    return tuple(answer)


def _interval_parameter_cube(
    value: Sequence[DirectedInterval], count: int
) -> tuple[DirectedInterval, ...]:
    return _interval_parameter_multiply(
        _interval_parameter_multiply(value, value, count), value, count
    )


def _interval_parameter_shift_one(
    value: Sequence[DirectedInterval], count: int
) -> tuple[DirectedInterval, ...]:
    result = list(value[:count])
    result[0] = result[0] - 1
    return tuple(result)


def _coefficient_voltage_boxes(
    ranges: Sequence[DirectedInterval], radius: gmpy2.mpfr, precision: int
) -> tuple[DirectedInterval, ...]:
    voltage_coordinate, _, _ = _p_constants(precision)
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        error = voltage_coordinate * radius
    return tuple(_symmetric_enlargement(value, error) for value in ranges)


def _coefficient_current_log_norm_upper(
    voltage_boxes: Sequence[DirectedInterval], precision: int
) -> gmpy2.mpfr:
    epsilon = _fraction_interval(EPSILON, precision)
    kappa_1 = _fraction_interval(KAPPA_1, precision)
    kappa_3 = _fraction_interval(KAPPA_3, precision)
    square = _interval_parameter_multiply(voltage_boxes, voltage_boxes, 5)
    shifted_square = _interval_parameter_multiply(
        _interval_parameter_shift_one(voltage_boxes, 5),
        _interval_parameter_shift_one(voltage_boxes, 5),
        5,
    )
    derivative = []
    for order in range(5):
        value = -square[order] - 3 * epsilon * kappa_3 * shifted_square[order]
        if order == 0:
            value = value + 1 - epsilon * kappa_1
        derivative.append(value)
    base = _current_log_norm_upper(voltage_boxes[0], precision)
    _, forcing_coordinate, _ = _p_constants(precision)
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        off_diagonal = sum(
            (
                forcing_coordinate * derivative[order].upper_abs()
                for order in range(1, 5)
            ),
            gmpy2.mpfr(0),
        )
        return base + off_diagonal


def _coefficient_delay_operator_upper(
    voltage_boxes: Sequence[DirectedInterval], precision: int
) -> gmpy2.mpfr:
    epsilon = _fraction_interval(EPSILON, precision)
    kappa_1 = _fraction_interval(KAPPA_1, precision)
    kappa_3 = _fraction_interval(KAPPA_3, precision)
    shifted = _interval_parameter_shift_one(voltage_boxes, 5)
    square = _interval_parameter_multiply(shifted, shifted, 5)
    derivative = []
    for order in range(5):
        value = 3 * kappa_3 * square[order]
        if order == 0:
            value = value + kappa_1
        derivative.append(epsilon / 2 * value)
    _, forcing_coordinate, _ = _p_constants(precision)
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        return sum(
            (
                forcing_coordinate * value.upper_abs()
                for value in derivative
            ),
            gmpy2.mpfr(0),
        )


def _center_jump_upper(
    starts: Sequence[tuple[gmpy2.mpfr, gmpy2.mpfr]],
    endpoints: Sequence[tuple[DirectedInterval, DirectedInterval]],
    precision: int,
) -> gmpy2.mpfr:
    maximum = gmpy2.mpfr(0)
    for order in range(5):
        voltage = (
            endpoints[order][0] - _mpfr_point(starts[order][0], precision)
        ).upper_abs()
        recovery = (
            endpoints[order][1] - _mpfr_point(starts[order][1], precision)
        ).upper_abs()
        maximum = max(
            maximum, _p_box_norm_upper(voltage, recovery, precision)
        )
    return maximum


@dataclass(frozen=True)
class CoefficientCell:
    left: _Node
    right: _Node
    voltage: tuple[tuple[gmpy2.mpfr, ...], ...]
    recovery: tuple[tuple[gmpy2.mpfr, ...], ...]
    voltage_ranges: tuple[DirectedInterval, ...]
    recovery_ranges: tuple[DirectedInterval, ...]
    endpoint_radius: gmpy2.mpfr
    maximum_radius: gmpy2.mpfr
    residual_upper: gmpy2.mpfr
    logarithmic_norm_upper: gmpy2.mpfr
    delay_four_operator_upper: gmpy2.mpfr
    delay_five_operator_upper: gmpy2.mpfr
    closure_gap_lower: gmpy2.mpfr
    center_jump_upper: gmpy2.mpfr


@dataclass(frozen=True)
class CoefficientPropagation:
    cells: Mapping[tuple[int, int, int, int], CoefficientCell]
    completed: bool
    requested_cell_count: int
    closed_cell_count: int
    failure_cell_key: tuple[int, int, int, int] | None
    failure_reason: str | None
    maximum_radius: gmpy2.mpfr
    maximum_residual: gmpy2.mpfr
    minimum_closure_gap: gmpy2.mpfr
    maximum_log_norm: gmpy2.mpfr
    maximum_delay_four_operator: gmpy2.mpfr
    maximum_delay_five_operator: gmpy2.mpfr


def _history_guide(
    alpha_center: gmpy2.mpfr, precision: int
) -> tuple[
    tuple[tuple[gmpy2.mpfr, ...], ...],
    tuple[DirectedInterval, ...],
]:
    zero_polynomial = tuple(
        [gmpy2.mpfr(0)] * (JET_TAYLOR_DEGREE + 1)
    )
    alpha_polynomial = tuple(
        [alpha_center] + [gmpy2.mpfr(0)] * JET_TAYLOR_DEGREE
    )
    guides = (alpha_polynomial,) + tuple(zero_polynomial for _ in range(4))
    ranges = (_mpfr_point(alpha_center, precision),) + tuple(
        _point(0, precision) for _ in range(4)
    )
    return guides, ranges


def _translated_coefficient_source(
    cells: Mapping[tuple[int, int, int, int], CoefficientCell],
    left: _Node,
    right: _Node,
    delay: int,
    history_guide: tuple[tuple[gmpy2.mpfr, ...], ...],
    history_ranges: tuple[DirectedInterval, ...],
    history_error: gmpy2.mpfr,
) -> tuple[
    tuple[tuple[gmpy2.mpfr, ...], ...],
    tuple[DirectedInterval, ...],
    gmpy2.mpfr,
]:
    source_left = left.shifted(delay)
    source_right = right.shifted(delay)
    if _node_compare(source_right, ZERO_NODE) <= 0:
        return history_guide, history_ranges, history_error
    if _node_compare(source_left, ZERO_NODE) < 0:
        raise AssertionError("a coefficient delay cell crossed the history seam")
    source = cells.get(_cell_key(source_left, source_right))
    if source is None:
        raise AssertionError("an exact coefficient delay cell is unavailable")
    return source.voltage, source.voltage_ranges, source.maximum_radius


@lru_cache(maxsize=1)
def build_coefficient_propagation() -> CoefficientPropagation:
    precision = PRECISION_BITS
    nodes = _nodes()
    alpha = _alpha_interval(precision)
    alpha_center = _nearest_midpoint(alpha)
    with gmpy2.context(precision=precision, round=gmpy2.RoundToNearest):
        recovery_center = alpha_center - (
            gmpy2.mpfr(UNFOLDING.numerator) / UNFOLDING.denominator
        )
    _, _, alpha_diagonal = _p_constants(precision)
    alpha_difference = (alpha - _mpfr_point(alpha_center, precision)).upper_abs()
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        initial_error = alpha_diagonal * alpha_difference
    history_voltage, history_ranges = _history_guide(alpha_center, precision)
    cells: dict[tuple[int, int, int, int], CoefficientCell] = {}
    previous: CoefficientCell | None = None
    failure_key = None
    failure_reason = None
    maximum_radius = initial_error
    maximum_residual = gmpy2.mpfr(0)
    minimum_gap = gmpy2.inf()
    maximum_mu = -gmpy2.inf()
    maximum_beta = {4: gmpy2.mpfr(0), 5: gmpy2.mpfr(0)}

    for left, right in zip(nodes[:-1], nodes[1:], strict=True):
        step_interval = _node_interval(right, precision) - _node_interval(
            left, precision
        )
        if step_interval.lower <= 0:
            raise AssertionError("a directed coefficient step is not positive")
        step_center = _nearest_midpoint(step_interval)
        pulse_on = _node_compare(left, PULSE_RELEASE_NODE) < 0
        if pulse_on and _node_compare(right, PULSE_RELEASE_NODE) > 0:
            raise AssertionError("a coefficient cell crossed pulse release")
        sources = {
            delay: _translated_coefficient_source(
                cells,
                left,
                right,
                delay,
                history_voltage,
                history_ranges,
                initial_error,
            )
            for delay in DELAY_MULTIPLIERS
        }
        if previous is None:
            starts = tuple(
                [(alpha_center, recovery_center)]
                + [(gmpy2.mpfr(0), gmpy2.mpfr(0)) for _ in range(4)]
            )
            start_radius = initial_error
            center_jump = gmpy2.mpfr(0)
        else:
            starts_list = []
            endpoints = []
            for order in range(5):
                voltage_start, voltage_endpoint = _guide_endpoint(
                    previous.voltage[order], precision
                )
                recovery_start, recovery_endpoint = _guide_endpoint(
                    previous.recovery[order], precision
                )
                starts_list.append((voltage_start, recovery_start))
                endpoints.append((voltage_endpoint, recovery_endpoint))
            starts = tuple(starts_list)
            center_jump = _center_jump_upper(starts, endpoints, precision)
            with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
                start_radius = previous.endpoint_radius + center_jump
        voltage, recovery = _coefficient_taylor_guide(
            starts,
            step_center,
            sources[4][0],
            sources[5][0],
            pulse_on,
            JET_TAYLOR_DEGREE,
            precision,
        )
        ranges = tuple(
            _poly_bernstein_range(
                tuple(_mpfr_point(value, precision) for value in voltage[order])
            )
            for order in range(5)
        )
        recovery_ranges = tuple(
            _poly_bernstein_range(
                tuple(_mpfr_point(value, precision) for value in recovery[order])
            )
            for order in range(5)
        )
        residual = _guide_residual_upper(
            voltage,
            recovery,
            sources[4][0],
            sources[5][0],
            step_interval,
            pulse_on,
        )
        with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
            radius = (
                max(start_radius, gmpy2.mpfr(TUBE_FLOOR))
                * gmpy2.mpfr(TUBE_INFLATION)
                + gmpy2.mpfr(TUBE_FLOOR)
            )
        closed = False
        for _ in range(MAXIMUM_FIXED_POINT_ITERATIONS):
            current_boxes = _coefficient_voltage_boxes(ranges, radius, precision)
            mu = _coefficient_current_log_norm_upper(current_boxes, precision)
            delay_operators = {}
            for delay in DELAY_MULTIPLIERS:
                delayed_boxes = _coefficient_voltage_boxes(
                    sources[delay][1], sources[delay][2], precision
                )
                delay_operators[delay] = _coefficient_delay_operator_upper(
                    delayed_boxes, precision
                )
            with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
                forcing = (
                    residual
                    + delay_operators[4] * sources[4][2]
                    + delay_operators[5] * sources[5][2]
                )
            endpoint = _gronwall_endpoint(
                start_radius, forcing, mu, step_interval.upper, precision
            )
            if not gmpy2.is_finite(endpoint):
                failure_key = _cell_key(left, right)
                failure_reason = "nonfinite_coefficient_endpoint"
                break
            with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
                gap = radius - endpoint
            if gap > 0:
                closed = True
                break
            with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
                radius = (
                    max(radius, endpoint)
                    * gmpy2.mpfr(TUBE_INFLATION)
                    + gmpy2.mpfr(TUBE_FLOOR)
                )
        if failure_key is not None:
            break
        if not closed:
            failure_key = _cell_key(left, right)
            failure_reason = "coefficient_fixed_point_did_not_close"
            break
        cell = CoefficientCell(
            left=left,
            right=right,
            voltage=voltage,
            recovery=recovery,
            voltage_ranges=ranges,
            recovery_ranges=recovery_ranges,
            endpoint_radius=endpoint,
            maximum_radius=radius,
            residual_upper=residual,
            logarithmic_norm_upper=mu,
            delay_four_operator_upper=delay_operators[4],
            delay_five_operator_upper=delay_operators[5],
            closure_gap_lower=gap,
            center_jump_upper=center_jump,
        )
        cells[_cell_key(left, right)] = cell
        previous = cell
        maximum_radius = max(maximum_radius, radius)
        maximum_residual = max(maximum_residual, residual)
        minimum_gap = min(minimum_gap, gap)
        maximum_mu = max(maximum_mu, mu)
        maximum_beta[4] = max(maximum_beta[4], delay_operators[4])
        maximum_beta[5] = max(maximum_beta[5], delay_operators[5])

    return CoefficientPropagation(
        cells=cells,
        completed=failure_key is None,
        requested_cell_count=len(nodes) - 1,
        closed_cell_count=len(cells),
        failure_cell_key=failure_key,
        failure_reason=failure_reason,
        maximum_radius=maximum_radius,
        maximum_residual=maximum_residual,
        minimum_closure_gap=minimum_gap,
        maximum_log_norm=maximum_mu,
        maximum_delay_four_operator=maximum_beta[4],
        maximum_delay_five_operator=maximum_beta[5],
    )


def _full_parameter_voltage_range(
    coefficient_boxes: Sequence[DirectedInterval], precision: int
) -> DirectedInterval:
    result = coefficient_boxes[0]
    xi_symmetric = DirectedInterval.from_bounds(-1, 1, precision)
    xi_even = DirectedInterval.from_bounds(0, 1, precision)
    for order in range(1, 5):
        result = result + coefficient_boxes[order] * (
            xi_symmetric if order % 2 else xi_even
        )
    return result


def _degree_five_tail_upper(
    current: Sequence[DirectedInterval],
    delayed_four: Sequence[DirectedInterval],
    delayed_five: Sequence[DirectedInterval],
    precision: int,
) -> gmpy2.mpfr:
    epsilon = _fraction_interval(EPSILON, precision)
    kappa_3 = _fraction_interval(KAPPA_3, precision)
    third = _point(1, precision) / 3
    half = _point(1, precision) / 2
    current_cube = _interval_parameter_cube(current, TAIL_MAXIMUM_DEGREE + 1)
    current_shifted_cube = _interval_parameter_cube(
        _interval_parameter_shift_one(current, 5), TAIL_MAXIMUM_DEGREE + 1
    )
    delayed_four_cube = _interval_parameter_cube(
        _interval_parameter_shift_one(delayed_four, 5),
        TAIL_MAXIMUM_DEGREE + 1,
    )
    delayed_five_cube = _interval_parameter_cube(
        _interval_parameter_shift_one(delayed_five, 5),
        TAIL_MAXIMUM_DEGREE + 1,
    )
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        total = gmpy2.mpfr(0)
        for order in range(5, TAIL_MAXIMUM_DEGREE + 1):
            coefficient = (
                -third * current_cube[order]
                + epsilon
                * kappa_3
                * (
                    half
                    * (delayed_four_cube[order] + delayed_five_cube[order])
                    - current_shifted_cube[order]
                )
            )
            total += coefficient.upper_abs()
        return _p_box_norm_upper(total, gmpy2.mpfr(0), precision)


@dataclass(frozen=True)
class RemainderCell:
    left: _Node
    right: _Node
    endpoint_radius: gmpy2.mpfr
    maximum_radius: gmpy2.mpfr
    degree_five_tail_upper: gmpy2.mpfr
    logarithmic_norm_upper: gmpy2.mpfr
    delay_four_operator_upper: gmpy2.mpfr
    delay_five_operator_upper: gmpy2.mpfr
    closure_gap_lower: gmpy2.mpfr


@dataclass(frozen=True)
class RemainderPropagation:
    cells: Mapping[tuple[int, int, int, int], RemainderCell]
    completed: bool
    requested_cell_count: int
    closed_cell_count: int
    failure_cell_key: tuple[int, int, int, int] | None
    failure_reason: str | None
    maximum_radius: gmpy2.mpfr
    maximum_tail: gmpy2.mpfr
    minimum_closure_gap: gmpy2.mpfr


def _source_remainder_radius(
    cells: Mapping[tuple[int, int, int, int], RemainderCell],
    left: _Node,
    right: _Node,
    delay: int,
) -> gmpy2.mpfr:
    source_left = left.shifted(delay)
    source_right = right.shifted(delay)
    if _node_compare(source_right, ZERO_NODE) <= 0:
        return gmpy2.mpfr(0)
    if _node_compare(source_left, ZERO_NODE) < 0:
        raise AssertionError("a remainder delay crossed the history seam")
    source = cells.get(_cell_key(source_left, source_right))
    if source is None:
        raise AssertionError("a remainder delay source is unavailable")
    return source.maximum_radius


@lru_cache(maxsize=1)
def build_remainder_propagation() -> RemainderPropagation:
    coefficients = build_coefficient_propagation()
    if not coefficients.completed:
        return RemainderPropagation(
            cells={},
            completed=False,
            requested_cell_count=coefficients.requested_cell_count,
            closed_cell_count=0,
            failure_cell_key=coefficients.failure_cell_key,
            failure_reason="coefficient_enclosure_failed_before_remainder",
            maximum_radius=gmpy2.inf(),
            maximum_tail=gmpy2.inf(),
            minimum_closure_gap=-gmpy2.inf(),
        )
    precision = PRECISION_BITS
    cells: dict[tuple[int, int, int, int], RemainderCell] = {}
    previous: RemainderCell | None = None
    failure_key = None
    failure_reason = None
    maximum_radius = gmpy2.mpfr(0)
    maximum_tail = gmpy2.mpfr(0)
    minimum_gap = gmpy2.inf()
    coefficient_cells = coefficients.cells

    for key, coefficient_cell in coefficient_cells.items():
        left = coefficient_cell.left
        right = coefficient_cell.right
        step_interval = _node_interval(right, precision) - _node_interval(
            left, precision
        )
        current_boxes = _coefficient_voltage_boxes(
            coefficient_cell.voltage_ranges,
            coefficient_cell.maximum_radius,
            precision,
        )
        delayed_boxes = {}
        for delay in DELAY_MULTIPLIERS:
            source_key = _cell_key(left.shifted(delay), right.shifted(delay))
            if _node_compare(right.shifted(delay), ZERO_NODE) <= 0:
                alpha = _alpha_interval(precision)
                delayed_boxes[delay] = (alpha,) + tuple(
                    _point(0, precision) for _ in range(4)
                )
            else:
                source = coefficient_cells.get(source_key)
                if source is None:
                    raise AssertionError("a coefficient source vanished")
                delayed_boxes[delay] = _coefficient_voltage_boxes(
                    source.voltage_ranges, source.maximum_radius, precision
                )
        tail = _degree_five_tail_upper(
            current_boxes, delayed_boxes[4], delayed_boxes[5], precision
        )
        start_radius = (
            gmpy2.mpfr(0) if previous is None else previous.endpoint_radius
        )
        delay_radii = {
            delay: _source_remainder_radius(cells, left, right, delay)
            for delay in DELAY_MULTIPLIERS
        }
        with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
            radius = (
                max(start_radius, gmpy2.mpfr(TUBE_FLOOR))
                * gmpy2.mpfr(TUBE_INFLATION)
                + gmpy2.mpfr(TUBE_FLOOR)
            )
        closed = False
        for _ in range(MAXIMUM_FIXED_POINT_ITERATIONS):
            current_family = _full_parameter_voltage_range(
                current_boxes, precision
            )
            voltage_coordinate, _, _ = _p_constants(precision)
            with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
                current_error = voltage_coordinate * radius
            current_tube = _symmetric_enlargement(current_family, current_error)
            mu = _current_log_norm_upper(current_tube, precision)
            delay_operators = {}
            for delay in DELAY_MULTIPLIERS:
                delayed_family = _full_parameter_voltage_range(
                    delayed_boxes[delay], precision
                )
                with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
                    delayed_error = voltage_coordinate * delay_radii[delay]
                delayed_tube = _symmetric_enlargement(
                    delayed_family, delayed_error
                )
                # This is the P-operator norm for one delayed state block.
                epsilon = _fraction_interval(EPSILON, precision)
                kappa_1 = _fraction_interval(KAPPA_1, precision)
                kappa_3 = _fraction_interval(KAPPA_3, precision)
                derivative = epsilon / 2 * (
                    kappa_1 + 3 * kappa_3 * (delayed_tube - 1) ** 2
                )
                _, forcing_coordinate, _ = _p_constants(precision)
                with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
                    delay_operators[delay] = (
                        forcing_coordinate * derivative.upper_abs()
                    )
            with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
                forcing = (
                    tail
                    + delay_operators[4] * delay_radii[4]
                    + delay_operators[5] * delay_radii[5]
                )
            endpoint = _gronwall_endpoint(
                start_radius, forcing, mu, step_interval.upper, precision
            )
            if not gmpy2.is_finite(endpoint):
                failure_key = key
                failure_reason = "nonfinite_remainder_endpoint"
                break
            with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
                gap = radius - endpoint
            if gap > 0:
                closed = True
                break
            with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
                radius = (
                    max(radius, endpoint)
                    * gmpy2.mpfr(TUBE_INFLATION)
                    + gmpy2.mpfr(TUBE_FLOOR)
                )
        if failure_key is not None:
            break
        if not closed:
            failure_key = key
            failure_reason = "remainder_fixed_point_did_not_close"
            break
        cell = RemainderCell(
            left=left,
            right=right,
            endpoint_radius=endpoint,
            maximum_radius=radius,
            degree_five_tail_upper=tail,
            logarithmic_norm_upper=mu,
            delay_four_operator_upper=delay_operators[4],
            delay_five_operator_upper=delay_operators[5],
            closure_gap_lower=gap,
        )
        cells[key] = cell
        previous = cell
        maximum_radius = max(maximum_radius, radius)
        maximum_tail = max(maximum_tail, tail)
        minimum_gap = min(minimum_gap, gap)

    return RemainderPropagation(
        cells=cells,
        completed=failure_key is None,
        requested_cell_count=coefficients.requested_cell_count,
        closed_cell_count=len(cells),
        failure_cell_key=failure_key,
        failure_reason=failure_reason,
        maximum_radius=maximum_radius,
        maximum_tail=maximum_tail,
        minimum_closure_gap=minimum_gap,
    )


def _sha256_path(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def canonical_sha256(value: Any) -> str:
    encoded = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("utf-8")
    return sha256(encoded).hexdigest()


def _mapping(value: Any, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{name} must be a mapping")
    return value


def _load_bound_json(repository: Path, relative: str, expected: str) -> Any:
    path = repository / relative
    if _sha256_path(path) != expected:
        raise ValueError(f"directed jet bound parent changed: {relative}")
    return json.loads(path.read_text(encoding="utf-8"))


def _coordinate_bounds(precision: int) -> tuple[gmpy2.mpfr, gmpy2.mpfr]:
    p11 = _fraction_interval(P11, precision)
    p12 = _fraction_interval(P12, precision)
    p22 = _fraction_interval(P22, precision)
    determinant = p11 * p22 - p12**2
    return (p22 / determinant).sqrt().upper, (p11 / determinant).sqrt().upper


def _scaled_to_unscaled_upper(
    value: gmpy2.mpfr, order: int, precision: int
) -> gmpy2.mpfr:
    if order == 0:
        return value
    half_width = _fraction_interval(PARAMETER_HALF_WIDTH, precision)
    divisor = half_width**order
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        return value / divisor.lower


def _coefficient_envelope_rows(
    propagation: CoefficientPropagation,
) -> list[dict[str, Any]]:
    precision = PRECISION_BITS
    voltage_coordinate, recovery_coordinate = _coordinate_bounds(precision)
    maxima = [
        [gmpy2.mpfr(0), gmpy2.mpfr(0)] for _ in range(PARAMETER_DEGREE + 1)
    ]
    errors = [
        [gmpy2.mpfr(0), gmpy2.mpfr(0)] for _ in range(PARAMETER_DEGREE + 1)
    ]
    for cell in propagation.cells.values():
        with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
            voltage_error = voltage_coordinate * cell.maximum_radius
            recovery_error = recovery_coordinate * cell.maximum_radius
        for order in range(5):
            voltage_box = _symmetric_enlargement(
                cell.voltage_ranges[order], voltage_error
            )
            recovery_box = _symmetric_enlargement(
                cell.recovery_ranges[order], recovery_error
            )
            maxima[order][0] = max(maxima[order][0], voltage_box.upper_abs())
            maxima[order][1] = max(maxima[order][1], recovery_box.upper_abs())
            errors[order][0] = max(errors[order][0], voltage_error)
            errors[order][1] = max(errors[order][1], recovery_error)
    rows = []
    for order in range(5):
        factorial = math.factorial(order)
        a_voltage = _scaled_to_unscaled_upper(maxima[order][0], order, precision)
        a_recovery = _scaled_to_unscaled_upper(maxima[order][1], order, precision)
        a_voltage_error = _scaled_to_unscaled_upper(
            errors[order][0], order, precision
        )
        a_recovery_error = _scaled_to_unscaled_upper(
            errors[order][1], order, precision
        )
        with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
            z_voltage = factorial * a_voltage
            z_recovery = factorial * a_recovery
            z_voltage_error = factorial * a_voltage_error
            z_recovery_error = factorial * a_recovery_error
        rows.append(
            {
                "order": order,
                "scaled_coefficient_definition": (
                    f"b_{order}=h^{order}*partial_J^{order}z/{factorial}"
                ),
                "maximum_scaled_b_voltage_abs_upper": decimal_upper(
                    maxima[order][0]
                ),
                "maximum_scaled_b_recovery_abs_upper": decimal_upper(
                    maxima[order][1]
                ),
                "maximum_scaled_b_voltage_error_upper": decimal_upper(
                    errors[order][0]
                ),
                "maximum_scaled_b_recovery_error_upper": decimal_upper(
                    errors[order][1]
                ),
                "maximum_factorial_coefficient_a_voltage_abs_upper": (
                    decimal_upper(a_voltage)
                ),
                "maximum_factorial_coefficient_a_recovery_abs_upper": (
                    decimal_upper(a_recovery)
                ),
                "maximum_derivative_jet_z_voltage_abs_upper": decimal_upper(
                    z_voltage
                ),
                "maximum_derivative_jet_z_recovery_abs_upper": decimal_upper(
                    z_recovery
                ),
                "maximum_derivative_jet_z_voltage_error_upper": decimal_upper(
                    z_voltage_error
                ),
                "maximum_derivative_jet_z_recovery_error_upper": decimal_upper(
                    z_recovery_error
                ),
            }
        )
    return rows


@lru_cache(maxsize=1)
def build_directed_jet_certificate(repository: Path) -> dict[str, Any]:
    repository = Path(repository).resolve()
    stage5 = _load_bound_json(
        repository, STAGE5_CONTRACT_RELATIVE_PATH, STAGE5_CONTRACT_SHA256
    )
    stage5a = _load_bound_json(
        repository, STAGE5A_PILOT_RELATIVE_PATH, STAGE5A_PILOT_SHA256
    )
    family = _load_bound_json(
        repository, FAMILY_PARENT_RELATIVE_PATH, FAMILY_PARENT_SHA256
    )
    stage5_contract = _mapping(stage5.get("contract"), "Stage-5 contract")
    stage5a_pilot = _mapping(stage5a.get("pilot"), "Stage-5A pilot")
    family_certificate = _mapping(family.get("certificate"), "family certificate")
    if stage5_contract.get("claim_status", {}).get(
        "z0_through_z4_directed_guides_validated"
    ) is not False:
        raise ValueError("Stage-5 parent no longer leaves the jet guide open")
    if stage5a_pilot.get("claim_status", {}).get(
        "center_coefficient_guides_rigorously_enclosed"
    ) is not False:
        raise ValueError("Stage-5A pilot was unexpectedly promoted")
    if family_certificate.get("claim_status", {}).get(
        "full_wide_interval_first_J_variation_enclosure_validated"
    ) is not False:
        raise ValueError("the family parent no longer records its open gate")

    coefficients = build_coefficient_propagation()
    remainder = build_remainder_propagation()
    if not coefficients.completed or coefficients.closed_cell_count != 1152:
        raise ArithmeticError("the directed coefficient guide did not close")
    if not remainder.completed or remainder.closed_cell_count != 1152:
        raise ArithmeticError("the full-width order-five remainder did not close")
    precision = PRECISION_BITS
    voltage_coordinate, recovery_coordinate = _coordinate_bounds(precision)
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        remainder_voltage = voltage_coordinate * remainder.maximum_radius
        remainder_recovery = recovery_coordinate * remainder.maximum_radius
    final_remainder = next(reversed(tuple(remainder.cells.values())))
    forced_count = sum(
        1
        for cell in coefficients.cells.values()
        if _node_compare(cell.left, PULSE_RELEASE_NODE) < 0
    )
    certificate = {
        "schema_id": SCHEMA_ID,
        "model_id": MODEL_ID,
        "parameter_scaling": {
            "center_J0_exact": "2409/8000",
            "half_width_h_exact": "3/40000",
            "interval_exact": "[6021/20000,753/2500]",
            "normalized_parameter": "xi=(J-J0)/h in [-1,1]",
            "polynomial": (
                "B(t,xi)=sum_{k=0}^4 b_k(t)xi^k, "
                "b_k=h^k partial_J^k z(t,J0)/k!"
            ),
        },
        "arithmetic": {
            "precision_bits": PRECISION_BITS,
            "time_taylor_degree": JET_TAYLOR_DEGREE,
            "parameter_degree": PARAMETER_DEGREE,
            "cubic_maximum_parameter_degree": TAIL_MAXIMUM_DEGREE,
            "grid_denominator": GRID_DENOMINATOR,
            "grid_cell_count": coefficients.closed_cell_count,
            "forced_cell_count": forced_count,
            "released_cell_count": coefficients.closed_cell_count - forced_count,
            "final_time_exact": "24*sqrt(5)",
            "delays_exact": ["4*sqrt(5)", "5*sqrt(5)"],
        },
        "joint_coefficient_enclosure": {
            "norm": "max_{k=0,...,4} ||(delta b_{k,v},delta b_{k,w})||_P",
            "all_cells_closed": True,
            "closed_cell_count": coefficients.closed_cell_count,
            "maximum_joint_P_error_radius_upper": decimal_upper(
                coefficients.maximum_radius
            ),
            "maximum_guide_residual_upper": decimal_upper(
                coefficients.maximum_residual
            ),
            "minimum_cell_closure_gap_lower": decimal_lower(
                coefficients.minimum_closure_gap
            ),
            "maximum_block_P_logarithmic_norm_upper": decimal_upper(
                coefficients.maximum_log_norm
            ),
            "maximum_delay_four_block_operator_upper": decimal_upper(
                coefficients.maximum_delay_four_operator
            ),
            "maximum_delay_five_block_operator_upper": decimal_upper(
                coefficients.maximum_delay_five_operator
            ),
            "continuous_time_bernstein_envelopes": (
                _coefficient_envelope_rows(coefficients)
            ),
        },
        "cubic_substitution_tail": {
            "included_parameter_degrees": list(range(5, 13)),
            "formula": (
                "Tail_{>=5}[-V^3/3+epsilon*kappa3*"
                "(((D4-1)^3+(D5-1)^3)/2-(V-1)^3)]"
            ),
            "linear_and_pulse_terms_have_no_degree_ge_5_tail": True,
            "maximum_directed_P_tail_forcing_upper": decimal_upper(
                remainder.maximum_tail
            ),
        },
        "full_width_order_five_remainder": {
            "definition": (
                "R5(t,xi)=z(t,J0+h*xi)-sum_{k=0}^4 b_k(t)xi^k"
            ),
            "parameter_domain": "xi in [-1,1]",
            "time_domain": "t in [0,24*sqrt(5)]",
            "all_cells_closed": True,
            "closed_cell_count": remainder.closed_cell_count,
            "maximum_P_radius_upper": decimal_upper(remainder.maximum_radius),
            "maximum_voltage_coordinate_error_upper": decimal_upper(
                remainder_voltage
            ),
            "maximum_recovery_coordinate_error_upper": decimal_upper(
                remainder_recovery
            ),
            "final_endpoint_P_radius_upper": decimal_upper(
                final_remainder.endpoint_radius
            ),
            "minimum_cell_closure_gap_lower": decimal_lower(
                remainder.minimum_closure_gap
            ),
        },
        "event_interface": {
            "route_c_event_bracket": None,
            "uniform_route_c_event_speed": None,
            "event_time_parameter_jet": None,
            "common_event_complete_history_radius": None,
            "stable_coordinate_gap": None,
            "interval_newton_image": None,
            "fixed_time_flow_jet_does_not_remove_event_alignment": True,
        },
        "theorem_statement": (
            "For the exact quiet initial history, every J in the exact "
            "interval [6021/20000,753/2500], and every "
            "0<=t<=24*sqrt(5), the exact physical-pulse RFDE solution equals "
            "the displayed degree-four center-parameter polynomial with "
            "the directed uniform P-norm remainder bound recorded here. "
            "The scaled coefficient functions b0,...,b4 have the displayed "
            "continuous-time directed Bernstein envelopes. No Route-C event "
            "or onset conclusion is inferred."
        ),
        "claim_status": {
            **{name: True for name in TRUE_FLAGS},
            **{name: False for name in FALSE_FLAGS},
        },
    }
    return certificate


def build_directed_jet_result(repository: Path) -> dict[str, Any]:
    repository = Path(repository).resolve()
    certificate = build_directed_jet_certificate(repository)
    return {
        "certificate": certificate,
        "manifest": {
            "schema_id": SCHEMA_ID,
            "result": RESULT_RELATIVE_PATH,
            "default_command": DEFAULT_COMMAND,
            "arithmetic_scope": ARITHMETIC_SCOPE,
            "parent_sha256": {
                STAGE5_CONTRACT_RELATIVE_PATH: STAGE5_CONTRACT_SHA256,
                STAGE5A_PILOT_RELATIVE_PATH: STAGE5A_PILOT_SHA256,
                FAMILY_PARENT_RELATIVE_PATH: FAMILY_PARENT_SHA256,
            },
            "source_sha256": {
                relative: _sha256_path(repository / relative)
                for relative in SOURCE_MANIFEST
            },
            "dependency_source_sha256": {
                relative: _sha256_path(repository / relative)
                for relative in DEPENDENCY_SOURCE_MANIFEST
            },
            "certificate_sha256": canonical_sha256(certificate),
        },
    }


def validate_directed_jet_result(
    payload: Mapping[str, Any],
    repository: Path,
    *,
    recompute: bool = False,
) -> None:
    if not isinstance(payload, Mapping) or set(payload) != {
        "certificate",
        "manifest",
    }:
        raise ValueError("directed jet result must contain certificate and manifest")
    certificate = _mapping(payload.get("certificate"), "certificate")
    manifest = _mapping(payload.get("manifest"), "manifest")
    if certificate.get("schema_id") != SCHEMA_ID or manifest.get("schema_id") != SCHEMA_ID:
        raise ValueError("directed jet schema changed")
    if manifest.get("result") != RESULT_RELATIVE_PATH:
        raise ValueError("directed jet result path changed")
    if manifest.get("default_command") != DEFAULT_COMMAND:
        raise ValueError("directed jet default command changed")
    if manifest.get("arithmetic_scope") != ARITHMETIC_SCOPE:
        raise ValueError("directed jet arithmetic scope changed")
    if manifest.get("certificate_sha256") != canonical_sha256(certificate):
        raise ValueError("directed jet certificate digest changed")
    claims = _mapping(certificate.get("claim_status"), "claim status")
    if set(claims) != set(TRUE_FLAGS) | set(FALSE_FLAGS):
        raise ValueError("directed jet claim ledger changed")
    for name in TRUE_FLAGS:
        if claims.get(name) is not True:
            raise ValueError(f"proved directed jet claim was removed: {name}")
    for name in FALSE_FLAGS:
        if claims.get(name) is not False:
            raise ValueError(f"open event or onset claim was promoted: {name}")
    coefficient = _mapping(
        certificate.get("joint_coefficient_enclosure"),
        "coefficient enclosure",
    )
    if coefficient.get("all_cells_closed") is not True or coefficient.get(
        "closed_cell_count"
    ) != 1152:
        raise ValueError("directed coefficient cell closure changed")
    coefficient_radius = DirectedInterval.from_decimal(
        str(coefficient.get("maximum_joint_P_error_radius_upper")), 96
    )
    coefficient_gap = DirectedInterval.from_decimal(
        str(coefficient.get("minimum_cell_closure_gap_lower")), 96
    )
    if coefficient_radius.upper >= DirectedInterval.from_decimal("9e-19", 96).lower:
        raise ValueError("directed coefficient error budget no longer closes")
    if coefficient_gap.lower <= 0:
        raise ValueError("directed coefficient closure gap is not positive")
    tail = _mapping(certificate.get("cubic_substitution_tail"), "cubic tail")
    if tail.get("included_parameter_degrees") != list(range(5, 13)):
        raise ValueError("cubic tail degree ledger changed")
    tail_bound = DirectedInterval.from_decimal(
        str(tail.get("maximum_directed_P_tail_forcing_upper")), 96
    )
    if tail_bound.upper >= DirectedInterval.from_decimal("2.1e-9", 96).lower:
        raise ValueError("cubic tail budget no longer closes")
    remainder = _mapping(
        certificate.get("full_width_order_five_remainder"), "remainder"
    )
    if remainder.get("all_cells_closed") is not True or remainder.get(
        "closed_cell_count"
    ) != 1152:
        raise ValueError("order-five remainder cell closure changed")
    remainder_radius = DirectedInterval.from_decimal(
        str(remainder.get("maximum_P_radius_upper")), 96
    )
    remainder_gap = DirectedInterval.from_decimal(
        str(remainder.get("minimum_cell_closure_gap_lower")), 96
    )
    if remainder_radius.upper >= DirectedInterval.from_decimal("1.8e-8", 96).lower:
        raise ValueError("order-five remainder budget no longer closes")
    if remainder_gap.lower <= 0:
        raise ValueError("order-five remainder closure gap is not positive")
    event = _mapping(certificate.get("event_interface"), "event interface")
    for name in (
        "route_c_event_bracket",
        "uniform_route_c_event_speed",
        "event_time_parameter_jet",
        "common_event_complete_history_radius",
        "stable_coordinate_gap",
        "interval_newton_image",
    ):
        if event.get(name) is not None:
            raise ValueError("an open event or stable input was silently populated")
    repository = Path(repository).resolve()
    source_hashes = _mapping(manifest.get("source_sha256"), "source hashes")
    dependency_hashes = _mapping(
        manifest.get("dependency_source_sha256"), "dependency hashes"
    )
    if set(source_hashes) != set(SOURCE_MANIFEST):
        raise ValueError("directed jet source manifest changed")
    if set(dependency_hashes) != set(DEPENDENCY_SOURCE_MANIFEST):
        raise ValueError("directed jet dependency manifest changed")
    for relative in SOURCE_MANIFEST:
        if source_hashes.get(relative) != _sha256_path(repository / relative):
            raise ValueError(f"directed jet source changed: {relative}")
    for relative in DEPENDENCY_SOURCE_MANIFEST:
        if dependency_hashes.get(relative) != _sha256_path(repository / relative):
            raise ValueError(f"directed jet dependency changed: {relative}")
    expected_parents = {
        STAGE5_CONTRACT_RELATIVE_PATH: STAGE5_CONTRACT_SHA256,
        STAGE5A_PILOT_RELATIVE_PATH: STAGE5A_PILOT_SHA256,
        FAMILY_PARENT_RELATIVE_PATH: FAMILY_PARENT_SHA256,
    }
    if dict(_mapping(manifest.get("parent_sha256"), "parent hashes")) != expected_parents:
        raise ValueError("directed jet parent manifest changed")
    for relative, expected in expected_parents.items():
        if _sha256_path(repository / relative) != expected:
            raise ValueError(f"directed jet bound parent changed: {relative}")
    if recompute:
        build_directed_jet_certificate.cache_clear()
        build_remainder_propagation.cache_clear()
        build_coefficient_propagation.cache_clear()
        rebuilt = build_directed_jet_certificate(repository)
        if canonical_sha256(rebuilt) != canonical_sha256(certificate):
            raise ValueError("directed jet replay changed")


__all__ = [
    "CoefficientCell",
    "CoefficientPropagation",
    "J0",
    "JET_TAYLOR_DEGREE",
    "PARAMETER_HALF_WIDTH",
    "PARAMETER_INTERVAL",
    "RemainderCell",
    "RemainderPropagation",
    "RESULT_RELATIVE_PATH",
    "build_directed_jet_certificate",
    "build_directed_jet_result",
    "build_coefficient_propagation",
    "build_remainder_propagation",
    "canonical_sha256",
    "validate_directed_jet_result",
]
