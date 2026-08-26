"""Directed pulse propagation toward the ``J=8/25`` third outer return.

This module reuses the exact ``Q(sqrt(5))`` union grid and the directed
Taylor/Bernstein error machinery of :mod:`leaky_pulse_quiet_capture`, but it
does not reuse that module's pulse amplitude or terminal quiet-basin test.
The present target is the complete reduced history at the third positive
crossing of the source-bound outer voltage section.

The first computational gate is a directed method-of-steps enclosure from
the exact quiet equilibrium through ``43*sqrt(5)``.  Subsequent gates bracket
the third crossing, compare the whole delayed history with the validated
outer Fourier orbit, and expose the error decomposition

    E_raw = E_guide + E_flow + E_orbit + E_time*F_tube + E_section.

Entry into an attracting tube is deliberately a separate, conditional
statement: the outer attracting-tube radius is not presently validated.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields
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
    DirectedComplexInterval,
    DirectedInterval,
    complex_unit_interval,
    decimal_lower,
    decimal_upper,
    pi_interval,
    upward_sum,
)
from canard_control.fhn_periodic_infinite_validation import (
    _sequence_box_norm_upper,
)
from canard_control.fhn_periodic_directed_validation import directed_dft
from canard_control.leaky_outer_high_resolution import (
    validate_outer_high_resolution_artifact,
)
from canard_control.leaky_floquet_transfer import (
    validate_leaky_floquet_transfer_artifact,
)
from canard_control.leaky_pulse_quiet_capture import (
    FINAL_NODE_INDEX as QUIET_FINAL_NODE_INDEX,
    GRID_DENOMINATOR,
    MAXIMUM_FIXED_POINT_ITERATIONS,
    PRECISION_BITS,
    PULSE_RELEASE_NODE,
    TAYLOR_DEGREE,
    TUBE_FLOOR,
    TUBE_INFLATION,
    ZERO_NODE,
    _CellProof,
    _Node,
    _alpha_interval,
    _cell_key,
    _center_jump_norm,
    _current_log_norm_upper,
    _delayed_forcing_upper,
    _forward_nodes,
    _fraction_interval,
    _gronwall_endpoint,
    _guide_endpoint,
    _mpfr_point,
    _nearest,
    _nearest_midpoint,
    _node_compare,
    _node_interval,
    _p_box_norm_upper,
    _p_constants,
    _point,
    _poly_add,
    _poly_add_constant,
    _poly_bernstein_range,
    _poly_cube,
    _poly_l1_upper,
    _poly_multiply,
    _poly_scale,
    _poly_sub,
    _poly_time_derivative,
    _symmetric_enlargement,
    _translated_source,
    _cube_coefficients_nearest,
)
from canard_control.leaky_quiet_history_basin import P11, P12, P22


SCHEMA_ID = "leaky-pulse-outer-third-return-enclosure-v1"
MODEL_ID = "autonomous-leaky-recovery-physical-pulse"

SOURCE_RELATIVE_PATH = (
    "src/canard_control/leaky_pulse_outer_third_return_enclosure.py"
)
GENERATOR_RELATIVE_PATH = (
    "experiments/leaky_pulse_outer_third_return_enclosure.py"
)
RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_pulse_outer_third_return_enclosure.json"
)
NOTE_RELATIVE_PATH = "docs/leaky-pulse-outer-third-return-enclosure.md"
TEST_RELATIVE_PATH = (
    "tests/test_leaky_pulse_outer_third_return_enclosure.py"
)
OUTER_ORBIT_RESULT_RELATIVE_PATH = (
    "experiments/results/autonomous_leaky_recovery_outer_high_resolution.json"
)
FLOQUET_TRANSFER_RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_floquet_transfer.json"
)
ROUTING_CONTRACT_RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_outer_two_sided_routing_contract.json"
)
OUTER_ORBIT_RESULT_SHA256 = (
    "d888916fed919f1515dd31ab851b2229816ea373365fa0221b1e345580f165a7"
)
FLOQUET_TRANSFER_RESULT_SHA256 = (
    "5a3709ec792b29ed41533101245b13b3d35084ae508bdd1d420728200a5a5b16"
)
ROUTING_CONTRACT_RESULT_SHA256 = (
    "1f9920ab25eec017c6cf06d1cd6a0ce9a3c349ef20c400b86ca0e65d56ee8cab"
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
    "src/canard_control/fhn_periodic_directed_validation.py",
    "src/canard_control/fhn_periodic_infinite_validation.py",
    "src/canard_control/leaky_outer_high_resolution.py",
    "src/canard_control/leaky_floquet_transfer.py",
)
DEFAULT_COMMAND = (
    "OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONPATH=src "
    "/usr/bin/python3 experiments/leaky_pulse_outer_third_return_enclosure.py"
)
ARITHMETIC_SCOPE = (
    "192-bit outward MPFR on the exact Q(sqrt(5)) two-origin grid; "
    "degree-24 directed Taylor method of steps; Bernstein exclusion and "
    "monotone counting of all candidate section crossings; degree-24 "
    "cellwise Taylor/Bernstein comparison with the exact binary64 Fourier "
    "center; and the source-validated Wiener orbit/period correction ball"
)

PULSE_AMPLITUDE = Fraction(8, 25)
PULSE_DURATION = Fraction(1)
DELAY_MULTIPLIERS = (4, 5)
FINAL_SQRT5_MULTIPLIER = 43
FINAL_NODE = _Node(0, FINAL_SQRT5_MULTIPLIER * GRID_DENOMINATOR)
OUTER_TAYLOR_DEGREE = 24
THIRD_EVENT_X_LOWER = "0.324758328677411"
THIRD_EVENT_X_REFERENCE = "0.324758328677418"
THIRD_EVENT_X_UPPER = "0.324758328677425"
EXPECTED_CROSSING_DIRECTIONS = (-1, 1, -1, 1, -1, 1)

TRUE_FLAGS = (
    "exact_quiet_initial_history_validated",
    "physical_J_032_pulse_and_release_validated",
    "both_delay_breakpoint_families_preserved",
    "directed_method_of_steps_closed",
    "all_section_crossing_cells_bernstein_isolated",
    "all_section_crossings_monotone_and_unique",
    "third_positive_section_event_bracket_validated",
    "third_positive_section_event_time_error_validated",
    "continuous_candidate_outer_history_bernstein_distance_validated",
    "complete_history_flow_error_validated",
    "exact_outer_orbit_and_period_correction_transferred",
    "third_return_reduced_history_ball_inclusion_validated",
    "third_return_complete_history_ball_inclusion_validated",
)

FALSE_FLAGS = (
    "outer_zero_index_validated",
    "outer_stable_projection_norm_validated",
    "outer_stable_power_bound_validated",
    "outer_attracting_tube_radius_validated",
    "outer_attracting_tube_entry_validated",
    "outer_basin_capture_validated",
    "pulse_event_and_outer_phase_zero_on_same_exact_section_validated",
    "complete_signed_inner_exit_face_propagated",
    "two_sided_basin_routing_validated",
    "physical_pulse_stable_sheet_crossing_validated",
    "unique_physical_pulse_onset_validated",
    "physical_pulse_Jc_validated",
    "frequency_amplitude_safety_control_theorem_validated",
)


def _taylor_guide(
    start: tuple[gmpy2.mpfr, gmpy2.mpfr],
    step: gmpy2.mpfr,
    delayed_four: tuple[gmpy2.mpfr, ...],
    delayed_five: tuple[gmpy2.mpfr, ...],
    pulse_on: bool,
    degree: int,
    precision: int,
) -> tuple[tuple[gmpy2.mpfr, ...], tuple[gmpy2.mpfr, ...]]:
    """Nearest-rounded guide for the ``8/25`` pulse; not an enclosure."""

    with gmpy2.context(precision=precision, round=gmpy2.RoundToNearest):
        epsilon = gmpy2.mpfr(EPSILON.numerator) / EPSILON.denominator
        unfolding = gmpy2.mpfr(UNFOLDING.numerator) / UNFOLDING.denominator
        kappa_1 = gmpy2.mpfr(KAPPA_1.numerator) / KAPPA_1.denominator
        kappa_3 = gmpy2.mpfr(KAPPA_3.numerator) / KAPPA_3.denominator
        pulse = (
            gmpy2.mpfr(PULSE_AMPLITUDE.numerator)
            / PULSE_AMPLITUDE.denominator
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
                    (
                        voltage[index] * voltage[order - index]
                        for index in range(order + 1)
                    ),
                    gmpy2.mpfr(0),
                )
            )
            shifted_square.append(
                sum(
                    (
                        shifted[index] * shifted[order - index]
                        for index in range(order + 1)
                    ),
                    gmpy2.mpfr(0),
                )
            )
            voltage_cube = sum(
                (
                    voltage_square[index] * voltage[order - index]
                    for index in range(order + 1)
                ),
                gmpy2.mpfr(0),
            )
            shifted_cube = sum(
                (
                    shifted_square[index] * shifted[order - index]
                    for index in range(order + 1)
                ),
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
    """Outward residual of the ``8/25`` guide polynomial."""

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


def _propagation_nodes() -> tuple[_Node, ...]:
    if QUIET_FINAL_NODE_INDEX <= FINAL_NODE.index:
        raise AssertionError("the parent union grid no longer reaches the target")
    nodes = tuple(
        node
        for node in _forward_nodes()
        if _node_compare(node, FINAL_NODE) <= 0
    )
    if nodes[0] != ZERO_NODE or nodes[-1] != FINAL_NODE:
        raise AssertionError("the target endpoint is absent from the union grid")
    return nodes


@dataclass(frozen=True)
class DirectedPropagation:
    cells: Mapping[tuple[int, int, int, int], _CellProof]
    initial_error: gmpy2.mpfr
    maximum_error: gmpy2.mpfr
    maximum_residual: gmpy2.mpfr
    maximum_log_norm: gmpy2.mpfr
    minimum_log_norm: gmpy2.mpfr
    minimum_closure_gap: gmpy2.mpfr
    forced_cell_count: int
    delay_initial_counts: Mapping[int, int]
    delay_translated_counts: Mapping[int, int]


@lru_cache(maxsize=1)
def build_directed_propagation() -> DirectedPropagation:
    """Enclose the exact ``J=8/25`` pulse through ``43*sqrt(5)``."""

    precision = PRECISION_BITS
    nodes = _propagation_nodes()
    alpha = _alpha_interval(precision)
    alpha_center = _nearest_midpoint(alpha)
    with gmpy2.context(precision=precision, round=gmpy2.RoundToNearest):
        recovery_center = alpha_center - (
            gmpy2.mpfr(UNFOLDING.numerator) / UNFOLDING.denominator
        )
    coordinate_bound, _, alpha_diagonal = _p_constants(precision)
    alpha_difference = (alpha - _mpfr_point(alpha_center, precision)).upper_abs()
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
    maximum_residual = gmpy2.mpfr(0)
    maximum_log_norm = -gmpy2.inf()
    minimum_log_norm = gmpy2.inf()
    maximum_error = initial_error
    minimum_closure_gap = gmpy2.inf()

    for left, right in zip(nodes[:-1], nodes[1:], strict=True):
        step_interval = _node_interval(right, precision) - _node_interval(
            left, precision
        )
        if step_interval.lower <= 0:
            raise AssertionError("a directed union-grid step is not positive")
        step_center = _nearest_midpoint(step_interval)
        pulse_on = _node_compare(left, PULSE_RELEASE_NODE) < 0
        if pulse_on:
            if _node_compare(right, PULSE_RELEASE_NODE) > 0:
                raise AssertionError("a cell crossed the physical pulse release")
            forced_count += 1

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
        voltage_range = _poly_bernstein_range(
            tuple(_mpfr_point(value, precision) for value in voltage)
        )
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
        maximum_residual = max(maximum_residual, residual)
        maximum_log_norm = max(maximum_log_norm, log_norm)
        minimum_log_norm = min(minimum_log_norm, log_norm)
        maximum_error = max(maximum_error, radius)
        minimum_closure_gap = min(minimum_closure_gap, closure_gap)

    return DirectedPropagation(
        cells=cells,
        initial_error=initial_error,
        maximum_error=maximum_error,
        maximum_residual=maximum_residual,
        maximum_log_norm=maximum_log_norm,
        minimum_log_norm=minimum_log_norm,
        minimum_closure_gap=minimum_closure_gap,
        forced_cell_count=forced_count,
        delay_initial_counts=delay_initial_counts,
        delay_translated_counts=delay_translated_counts,
    )


def _poly_interval_value(
    coefficients: Sequence[gmpy2.mpfr], argument: DirectedInterval
) -> DirectedInterval:
    result = _point(0, argument.precision)
    for coefficient in reversed(coefficients):
        result = result * argument + _mpfr_point(
            coefficient, argument.precision
        )
    return result


def _poly_affine_restriction(
    coefficients: Sequence[gmpy2.mpfr],
    left: DirectedInterval,
    right: DirectedInterval,
) -> tuple[DirectedInterval, ...]:
    """Return interval coefficients of ``p(left+(right-left)*y)``."""

    if left.precision != right.precision or left.lower > right.upper:
        raise ValueError("invalid normalized restriction interval")
    precision = left.precision
    width = right - left
    result = [_point(0, precision) for _ in coefficients]
    for power, coefficient in enumerate(coefficients):
        value = _mpfr_point(coefficient, precision)
        for output_power in range(power + 1):
            result[output_power] = result[output_power] + (
                value
                * math.comb(power, output_power)
                * left ** (power - output_power)
                * width**output_power
            )
    return tuple(result)


def _coordinate_error_constants(
    precision: int,
) -> tuple[gmpy2.mpfr, gmpy2.mpfr]:
    p11 = _fraction_interval(P11, precision)
    p12 = _fraction_interval(P12, precision)
    p22 = _fraction_interval(P22, precision)
    determinant = p11 * p22 - p12**2
    return (p22 / determinant).sqrt().upper, (p11 / determinant).sqrt().upper


def _cell_state_tubes(
    cell: _CellProof,
    *,
    precision: int,
) -> tuple[DirectedInterval, DirectedInterval]:
    voltage_coordinate, recovery_coordinate = _coordinate_error_constants(
        precision
    )
    voltage = _symmetric_enlargement(
        cell.voltage_range, voltage_coordinate * cell.maximum_radius
    )
    recovery_guide = _poly_bernstein_range(
        tuple(_mpfr_point(value, precision) for value in cell.recovery)
    )
    recovery = _symmetric_enlargement(
        recovery_guide, recovery_coordinate * cell.maximum_radius
    )
    return voltage, recovery


def _field_intervals(
    cell: _CellProof,
    cells: Mapping[tuple[int, int, int, int], _CellProof],
    *,
    precision: int,
) -> tuple[DirectedInterval, DirectedInterval]:
    voltage, recovery = _cell_state_tubes(cell, precision=precision)
    voltage_coordinate, _ = _coordinate_error_constants(precision)
    delayed: list[DirectedInterval] = []
    for delay in DELAY_MULTIPLIERS:
        source = cells.get(
            _cell_key(cell.left.shifted(delay), cell.right.shifted(delay))
        )
        if source is None:
            raise AssertionError("field evaluation requested an initial delay cell")
        delayed.append(
            _symmetric_enlargement(
                source.voltage_range,
                voltage_coordinate * source.maximum_radius,
            )
        )
    epsilon = _fraction_interval(EPSILON, precision)
    kappa_1 = _fraction_interval(KAPPA_1, precision)
    kappa_3 = _fraction_interval(KAPPA_3, precision)
    average_delay = (delayed[0] + delayed[1]) / 2
    delayed_cubic = ((delayed[0] - 1) ** 3 + (delayed[1] - 1) ** 3) / 2
    fast = voltage - voltage**3 / 3 - recovery
    fast = fast + epsilon * kappa_1 * (average_delay - voltage)
    fast = fast + epsilon * kappa_3 * (
        delayed_cubic - (voltage - 1) ** 3
    )
    slow = epsilon * (
        voltage - recovery - _fraction_interval(UNFOLDING, precision)
    )
    return fast, slow


def _event_and_crossing_certificate(
    propagation: DirectedPropagation,
    section_voltage: float,
) -> tuple[dict[str, Any], _CellProof, DirectedInterval]:
    precision = PRECISION_BITS
    section = DirectedInterval.from_float(section_voltage, precision)
    voltage_coordinate, _ = _coordinate_error_constants(precision)
    candidates: list[dict[str, Any]] = []
    positive_count = 0
    target_cell: _CellProof | None = None
    for cell_index, cell in enumerate(propagation.cells.values()):
        error = voltage_coordinate * cell.maximum_radius
        voltage_tube = _symmetric_enlargement(cell.voltage_range, error)
        if not voltage_tube.intersects(section):
            continue
        field, _ = _field_intervals(
            cell, propagation.cells, precision=precision
        )
        if field.lower > 0:
            direction = 1
            speed_lower = field.lower
        elif field.upper < 0:
            direction = -1
            speed_lower = -field.upper
        else:
            raise ArithmeticError("a candidate section cell is not monotone")
        left_value = _symmetric_enlargement(
            _poly_interval_value(
                cell.voltage, DirectedInterval.from_decimal(0, precision)
            ),
            error,
        ) - section
        right_value = _symmetric_enlargement(
            _poly_interval_value(
                cell.voltage, DirectedInterval.from_decimal(1, precision)
            ),
            error,
        ) - section
        if direction > 0:
            crossed = left_value.upper < 0 < right_value.lower
            positive_count += 1
        else:
            crossed = right_value.upper < 0 < left_value.lower
        if not crossed:
            raise ArithmeticError("a monotone candidate cell lacks endpoint signs")
        left_time = _node_interval(cell.left, precision)
        right_time = _node_interval(cell.right, precision)
        candidates.append(
            {
                "cell_index": cell_index,
                "left_time_lower": decimal_lower(left_time.lower),
                "right_time_upper": decimal_upper(right_time.upper),
                "direction": direction,
                "event_speed_lower": decimal_lower(speed_lower),
                "left_section_difference_upper": decimal_upper(left_value.upper),
                "right_section_difference_lower": decimal_lower(
                    right_value.lower
                ),
            }
        )
        if direction > 0 and positive_count == 3:
            target_cell = cell

    directions = tuple(row["direction"] for row in candidates)
    if directions != EXPECTED_CROSSING_DIRECTIONS or target_cell is None:
        raise ArithmeticError("the directed crossing itinerary changed")

    x_lower = DirectedInterval.from_decimal(THIRD_EVENT_X_LOWER, precision)
    x_reference = DirectedInterval.from_decimal(
        THIRD_EVENT_X_REFERENCE, precision
    )
    x_upper = DirectedInterval.from_decimal(THIRD_EVENT_X_UPPER, precision)
    target_error = voltage_coordinate * target_cell.maximum_radius
    lower_sign = _symmetric_enlargement(
        _poly_interval_value(target_cell.voltage, x_lower), target_error
    ) - section
    upper_sign = _symmetric_enlargement(
        _poly_interval_value(target_cell.voltage, x_upper), target_error
    ) - section
    if lower_sign.upper >= 0 or upper_sign.lower <= 0:
        raise ArithmeticError("the third event micro-bracket lost its signs")
    target_field, _ = _field_intervals(
        target_cell, propagation.cells, precision=precision
    )
    if target_field.lower <= 0:
        raise ArithmeticError("the third event speed is not positive")
    cell_left = _node_interval(target_cell.left, precision)
    step = _node_interval(target_cell.right, precision) - cell_left
    event_lower = cell_left + x_lower * step
    event_reference = cell_left + x_reference * step
    event_upper = cell_left + x_upper * step
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        time_error = max(
            (event_reference - event_lower).upper_abs(),
            (event_upper - event_reference).upper_abs(),
        )
    return (
        {
            "candidate_section_voltage_binary64": {
                "binary64_hex": float(section_voltage).hex(),
                "decimal": format(float(section_voltage), ".17g"),
            },
            "candidate_cell_count": len(candidates),
            "crossing_directions": list(directions),
            "positive_crossing_count_through_declared_event": 3,
            "candidate_cells": candidates,
            "third_event_normalized_bracket": [
                THIRD_EVENT_X_LOWER,
                THIRD_EVENT_X_UPPER,
            ],
            "third_event_normalized_reference": THIRD_EVENT_X_REFERENCE,
            "third_event_lower_time": decimal_lower(event_lower.lower),
            "third_event_upper_time": decimal_upper(event_upper.upper),
            "third_event_reference_time_lower": decimal_lower(
                event_reference.lower
            ),
            "third_event_reference_time_upper": decimal_upper(
                event_reference.upper
            ),
            "third_event_time_error_upper": decimal_upper(time_error),
            "third_event_speed_lower": decimal_lower(target_field.lower),
            "third_event_lower_sign_upper": decimal_upper(lower_sign.upper),
            "third_event_upper_sign_lower": decimal_lower(upper_sign.lower),
            "all_other_cells_excluded_by_bernstein": True,
            "all_candidate_cells_monotone": True,
            "all_candidate_crossings_unique": True,
            "third_positive_event_bracket_validated": True,
        },
        target_cell,
        event_reference,
    )


def _complex_one(precision: int) -> DirectedComplexInterval:
    return DirectedComplexInterval.from_real(_point(1, precision))


def _outer_taylor_polynomial(
    sequence: Mapping[int, DirectedComplexInterval],
    period: DirectedInterval,
    relative_left: DirectedInterval,
    physical_width: DirectedInterval,
    degree: int,
) -> tuple[tuple[DirectedInterval, ...], gmpy2.mpfr]:
    """Taylor-enclose one Fourier component on a physical-time cell."""

    precision = period.precision
    two_pi = 2 * pi_interval(precision)
    coefficients = [
        DirectedComplexInterval.zero(precision) for _ in range(degree + 1)
    ]
    remainder_terms: list[gmpy2.mpfr] = []
    for mode, value in sequence.items():
        angle = two_pi * mode * relative_left / period
        phase = complex_unit_interval(angle)
        imaginary_rate = two_pi * mode * physical_width / period
        rate = DirectedComplexInterval(
            _point(0, precision), imaginary_rate
        )
        power = _complex_one(precision)
        factorial = 1
        phased = value * phase
        for order in range(degree + 1):
            if order:
                factorial *= order
            coefficients[order] = coefficients[order] + (
                phased * power * (_point(1, precision) / factorial)
            )
            power = power * rate
        with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
            magnitude = (
                two_pi.upper
                * abs(mode)
                * physical_width.upper
                / period.lower
            )
            remainder = (
                value.upper_abs()
                * gmpy2.exp(magnitude)
                * magnitude ** (degree + 1)
                / math.factorial(degree + 1)
            )
        remainder_terms.append(remainder)
    return (
        tuple(value.real for value in coefficients),
        upward_sum(remainder_terms, precision),
    )


def _difference_sup_upper(
    pulse: Sequence[DirectedInterval],
    outer: Sequence[DirectedInterval],
    outer_remainder: gmpy2.mpfr,
) -> gmpy2.mpfr:
    precision = pulse[0].precision
    zero = _point(0, precision)
    difference = tuple(
        (pulse[index] if index < len(pulse) else zero)
        - (outer[index] if index < len(outer) else zero)
        for index in range(max(len(pulse), len(outer)))
    )
    difference_range = _poly_bernstein_range(difference)
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        return difference_range.upper_abs() + outer_remainder


def _history_cells(
    propagation: DirectedPropagation, target: _CellProof
) -> tuple[_CellProof, ...]:
    ordered = tuple(propagation.cells.values())
    target_index = ordered.index(target)
    first_key = _cell_key(target.left.shifted(5), target.right.shifted(5))
    first = propagation.cells.get(first_key)
    if first is None:
        raise AssertionError("the five-delay history source cell is absent")
    first_index = ordered.index(first)
    if first_index >= target_index:
        raise AssertionError("the history cell ordering changed")
    return ordered[first_index : target_index + 1]


def _continuous_history_comparison(
    propagation: DirectedPropagation,
    target: _CellProof,
    event_reference: DirectedInterval,
    orbit: Any,
) -> dict[str, Any]:
    precision = PRECISION_BITS
    period = DirectedInterval.from_float(float(orbit.period), precision)
    voltage_sequence = directed_dft(orbit.state[:, 0], precision)
    recovery_sequence = directed_dft(orbit.state[:, 1], precision)
    history = _history_cells(propagation, target)
    x_reference = DirectedInterval.from_decimal(
        THIRD_EVENT_X_REFERENCE, precision
    )
    zero = DirectedInterval.from_decimal(0, precision)
    one = DirectedInterval.from_decimal(1, precision)
    maximum_voltage_guide = gmpy2.mpfr(0, precision)
    maximum_recovery_guide = gmpy2.mpfr(0, precision)
    maximum_outer_remainder = gmpy2.mpfr(0, precision)
    maximum_voltage_flow = gmpy2.mpfr(0, precision)
    maximum_recovery_flow = gmpy2.mpfr(0, precision)
    maximum_pulse_speed = gmpy2.mpfr(0, precision)
    voltage_coordinate, recovery_coordinate = _coordinate_error_constants(
        precision
    )
    target_recovery_guide_distance: gmpy2.mpfr | None = None

    for index, cell in enumerate(history):
        left_normalized = x_reference if index == 0 else zero
        right_normalized = x_reference if index == len(history) - 1 else one
        if left_normalized.lower >= right_normalized.upper:
            raise AssertionError("a retained history restriction is empty")
        voltage_pulse = _poly_affine_restriction(
            cell.voltage, left_normalized, right_normalized
        )
        recovery_pulse = _poly_affine_restriction(
            cell.recovery, left_normalized, right_normalized
        )
        cell_left = _node_interval(cell.left, precision)
        cell_step = _node_interval(cell.right, precision) - cell_left
        absolute_left = cell_left + left_normalized * cell_step
        physical_width = (right_normalized - left_normalized) * cell_step
        relative_left = absolute_left - event_reference
        voltage_outer, voltage_remainder = _outer_taylor_polynomial(
            voltage_sequence,
            period,
            relative_left,
            physical_width,
            OUTER_TAYLOR_DEGREE,
        )
        recovery_outer, recovery_remainder = _outer_taylor_polynomial(
            recovery_sequence,
            period,
            relative_left,
            physical_width,
            OUTER_TAYLOR_DEGREE,
        )
        voltage_difference = _difference_sup_upper(
            voltage_pulse, voltage_outer, voltage_remainder
        )
        recovery_difference = _difference_sup_upper(
            recovery_pulse, recovery_outer, recovery_remainder
        )
        maximum_voltage_guide = max(
            maximum_voltage_guide, voltage_difference
        )
        maximum_recovery_guide = max(
            maximum_recovery_guide, recovery_difference
        )
        maximum_outer_remainder = max(
            maximum_outer_remainder,
            voltage_remainder,
            recovery_remainder,
        )
        maximum_voltage_flow = max(
            maximum_voltage_flow,
            voltage_coordinate * cell.maximum_radius,
        )
        maximum_recovery_flow = max(
            maximum_recovery_flow,
            recovery_coordinate * cell.maximum_radius,
        )
        fast, slow = _field_intervals(
            cell, propagation.cells, precision=precision
        )
        maximum_pulse_speed = max(
            maximum_pulse_speed, fast.upper_abs(), slow.upper_abs()
        )
        if index == len(history) - 1:
            pulse_recovery_at_reference = _poly_interval_value(
                cell.recovery, x_reference
            )
            outer_recovery_at_phase_zero = DirectedInterval.from_float(
                float(orbit.state[0, 1]), precision
            )
            target_recovery_guide_distance = (
                pulse_recovery_at_reference - outer_recovery_at_phase_zero
            ).upper_abs()

    if target_recovery_guide_distance is None:
        raise AssertionError("the target recovery comparison was not evaluated")
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        complete_guide = max(
            maximum_voltage_guide, maximum_recovery_guide
        )
        reduced_guide = max(
            maximum_voltage_guide, target_recovery_guide_distance
        )
        complete_flow = max(maximum_voltage_flow, maximum_recovery_flow)
        reduced_flow = max(
            maximum_voltage_flow,
            recovery_coordinate * target.maximum_radius,
        )
    return {
        "history_cell_count": len(history),
        "history_delay_exact": "5*sqrt(5)",
        "outer_fourier_node_count": len(orbit.state),
        "outer_taylor_degree": OUTER_TAYLOR_DEGREE,
        "candidate_voltage_wiener_norm_upper": decimal_upper(
            _sequence_box_norm_upper(voltage_sequence, precision)
        ),
        "candidate_recovery_wiener_norm_upper": decimal_upper(
            _sequence_box_norm_upper(recovery_sequence, precision)
        ),
        "maximum_outer_taylor_remainder_upper": decimal_upper(
            maximum_outer_remainder
        ),
        "voltage_guide_history_distance_upper": decimal_upper(
            maximum_voltage_guide
        ),
        "recovery_guide_history_distance_upper": decimal_upper(
            maximum_recovery_guide
        ),
        "current_recovery_guide_distance_upper": decimal_upper(
            target_recovery_guide_distance
        ),
        "reduced_guide_history_distance_upper": decimal_upper(reduced_guide),
        "complete_guide_history_distance_upper": decimal_upper(
            complete_guide
        ),
        "maximum_voltage_flow_error_upper": decimal_upper(
            maximum_voltage_flow
        ),
        "maximum_recovery_flow_error_upper": decimal_upper(
            maximum_recovery_flow
        ),
        "reduced_flow_history_error_upper": decimal_upper(reduced_flow),
        "complete_flow_history_error_upper": decimal_upper(complete_flow),
        "history_speed_upper_on_event_sweep": decimal_upper(
            maximum_pulse_speed
        ),
        "continuous_candidate_outer_history_bernstein_distance_validated": True,
        "complete_history_flow_error_validated": True,
    }


def _mapping(value: Any, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{name} must be a mapping")
    return value


def _load_bound_json(
    repository: Path, relative: str, expected_sha256: str
) -> Mapping[str, Any]:
    path = repository / relative
    raw = path.read_bytes()
    if sha256(raw).hexdigest() != expected_sha256:
        raise ValueError(f"a bound parent changed: {relative}")
    return _mapping(json.loads(raw), relative)


def _declared_section_voltage(
    routing_payload: Mapping[str, Any],
) -> float:
    contract = _mapping(routing_payload.get("contract"), "routing contract")
    target = _mapping(
        contract.get("pulse_J_032_outer_attachment_target"),
        "J=.32 routing target",
    )
    record = _mapping(
        target.get("candidate_outer_section_voltage"),
        "declared section voltage",
    )
    if set(record) != {"binary64_hex", "decimal"}:
        raise ValueError("the declared section record changed")
    hexadecimal = record.get("binary64_hex")
    decimal = record.get("decimal")
    if not isinstance(hexadecimal, str) or not isinstance(decimal, str):
        raise ValueError("the declared section record is malformed")
    value = float.fromhex(hexadecimal)
    if value.hex() != hexadecimal or format(value, ".17g") != decimal:
        raise ValueError("the declared section binary64 record is not canonical")
    if hexadecimal != "0x1.cb8b5dd1391f4p-5":
        raise ValueError("the declared J=.32 section level changed")
    return value


def canonical_sha256(value: Any) -> str:
    return sha256(
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        ).encode("ascii")
    ).hexdigest()


def _sha256_path(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _phase_zero_interpolation_error(
    sequence: Mapping[int, DirectedComplexInterval], sample: float
) -> gmpy2.mpfr:
    precision = next(iter(sequence.values())).precision
    total = DirectedComplexInterval.zero(precision)
    for value in sequence.values():
        total = total + value
    difference = total.real - DirectedInterval.from_float(sample, precision)
    return difference.upper_abs()


def _outer_orbit_history_correction(
    orbit: Any,
    outer_payload: Mapping[str, Any],
    floquet_payload: Mapping[str, Any],
) -> dict[str, Any]:
    precision = PRECISION_BITS
    artifact = _mapping(outer_payload.get("artifact"), "outer artifact")
    directed = _mapping(
        artifact.get("directed_radii_certificate"), "outer directed certificate"
    )
    validation = _mapping(directed.get("validation"), "outer validation")
    correction_record = _mapping(
        validation.get("correction"), "outer correction"
    )
    correction = DirectedInterval.from_decimal(
        str(correction_record.get("chosen_radius")), precision
    )
    floquet_artifact = _mapping(
        floquet_payload.get("artifact"), "Floquet artifact"
    )
    branches = _mapping(floquet_artifact.get("branches"), "Floquet branches")
    branch = _mapping(branches.get("outer_pulse"), "outer Floquet branch")
    if branch.get("source_result_sha256") != OUTER_ORBIT_RESULT_SHA256:
        raise ValueError("the Floquet tangent belongs to another outer orbit")
    tangent = DirectedInterval.from_decimal(
        str(branch.get("orbit_tangent_norm_upper")), precision
    )
    maximum_delay = DirectedInterval.from_decimal(
        str(branch.get("maximum_delay_upper")), precision
    )
    candidate_period = DirectedInterval.from_float(float(orbit.period), precision)
    exact_period_lower = candidate_period - correction
    if exact_period_lower.lower <= 0:
        raise ArithmeticError("the outer period correction reaches zero")
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        phase_mismatch = (
            maximum_delay.upper
            * correction.upper
            / (candidate_period.lower * exact_period_lower.lower)
        )
        phase_shift_state_error = tangent.upper * phase_mismatch
        history_error = correction.upper + phase_shift_state_error
    return {
        "coefficient_and_period_correction_radius_upper": decimal_upper(
            correction.upper
        ),
        "candidate_period": format(float(orbit.period), ".17g"),
        "exact_period_lower": decimal_lower(exact_period_lower.lower),
        "maximum_history_delay_upper": decimal_upper(maximum_delay.upper),
        "exact_phase_tangent_norm_upper": decimal_upper(tangent.upper),
        "physical_history_phase_mismatch_upper": decimal_upper(phase_mismatch),
        "phase_shift_state_error_upper": decimal_upper(
            phase_shift_state_error
        ),
        "exact_outer_orbit_history_correction_upper": decimal_upper(
            history_error
        ),
        "formula": (
            "E_orbit=R_A+||dz_*/dx||*tau_max*R_T/"
            "(T_bar*(T_bar-R_T))"
        ),
        "exact_outer_orbit_and_period_correction_transferred": True,
    }


@lru_cache(maxsize=1)
def build_third_return_certificate(repository: Path) -> dict[str, Any]:
    repository = Path(repository).resolve()
    outer_payload = _load_bound_json(
        repository,
        OUTER_ORBIT_RESULT_RELATIVE_PATH,
        OUTER_ORBIT_RESULT_SHA256,
    )
    floquet_payload = _load_bound_json(
        repository,
        FLOQUET_TRANSFER_RESULT_RELATIVE_PATH,
        FLOQUET_TRANSFER_RESULT_SHA256,
    )
    routing_payload = _load_bound_json(
        repository,
        ROUTING_CONTRACT_RESULT_RELATIVE_PATH,
        ROUTING_CONTRACT_RESULT_SHA256,
    )
    orbit = validate_outer_high_resolution_artifact(
        outer_payload, repository, replay_directed=False
    )
    validate_leaky_floquet_transfer_artifact(
        floquet_payload, repository, recompute=False
    )
    declared_section_voltage = _declared_section_voltage(routing_payload)
    propagation = build_directed_propagation()
    event, target, event_reference = _event_and_crossing_certificate(
        propagation, declared_section_voltage
    )
    comparison = _continuous_history_comparison(
        propagation, target, event_reference, orbit
    )
    correction = _outer_orbit_history_correction(
        orbit, outer_payload, floquet_payload
    )
    precision = PRECISION_BITS
    voltage_sequence = directed_dft(orbit.state[:, 0], precision)
    recovery_sequence = directed_dft(orbit.state[:, 1], precision)
    section_error = max(
        _phase_zero_interpolation_error(
            voltage_sequence, float(orbit.state[0, 0])
        ),
        _phase_zero_interpolation_error(
            recovery_sequence, float(orbit.state[0, 1])
        ),
    )
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        declared_to_phase_zero = abs(
            gmpy2.mpfr(declared_section_voltage)
            - gmpy2.mpfr(float(orbit.state[0, 0]))
        )
        section_error += declared_to_phase_zero
    e_time = DirectedInterval.from_decimal(
        str(event["third_event_time_error_upper"]), precision
    )
    f_tube = DirectedInterval.from_decimal(
        str(comparison["history_speed_upper_on_event_sweep"]), precision
    )
    e_orbit = DirectedInterval.from_decimal(
        str(correction["exact_outer_orbit_history_correction_upper"]),
        precision,
    )
    reduced_guide = DirectedInterval.from_decimal(
        str(comparison["reduced_guide_history_distance_upper"]), precision
    )
    complete_guide = DirectedInterval.from_decimal(
        str(comparison["complete_guide_history_distance_upper"]), precision
    )
    reduced_flow = DirectedInterval.from_decimal(
        str(comparison["reduced_flow_history_error_upper"]), precision
    )
    complete_flow = DirectedInterval.from_decimal(
        str(comparison["complete_flow_history_error_upper"]), precision
    )
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        time_shift = e_time.upper * f_tube.upper
        reduced_total = (
            reduced_guide.upper
            + reduced_flow.upper
            + e_orbit.upper
            + time_shift
            + section_error
        )
        complete_total = (
            complete_guide.upper
            + complete_flow.upper
            + e_orbit.upper
            + time_shift
            + section_error
        )
    design_radius = DirectedInterval.from_decimal("0.0001", precision)
    if reduced_total >= design_radius.lower or complete_total >= design_radius.lower:
        raise ArithmeticError("the validated history ball exceeds its design radius")
    cells = tuple(propagation.cells.values())
    certificate = {
        "schema_id": SCHEMA_ID,
        "model_id": MODEL_ID,
        "arithmetic": {
            "precision_bits": PRECISION_BITS,
            "grid_denominator": GRID_DENOMINATOR,
            "taylor_degree": TAYLOR_DEGREE,
            "outer_taylor_degree": OUTER_TAYLOR_DEGREE,
            "grid_cell_count": len(cells),
            "forced_cell_count": propagation.forced_cell_count,
            "released_cell_count": len(cells) - propagation.forced_cell_count,
            "delay_four_initial_cell_count": propagation.delay_initial_counts[4],
            "delay_five_initial_cell_count": propagation.delay_initial_counts[5],
            "delay_four_translated_cell_count": propagation.delay_translated_counts[4],
            "delay_five_translated_cell_count": propagation.delay_translated_counts[5],
            "final_time_exact": "43*sqrt(5)",
            "maximum_p_error_radius_upper": decimal_upper(
                propagation.maximum_error
            ),
            "maximum_guide_residual_upper": decimal_upper(
                propagation.maximum_residual
            ),
            "maximum_current_logarithmic_norm_upper": decimal_upper(
                propagation.maximum_log_norm
            ),
            "minimum_current_logarithmic_norm_upper": decimal_upper(
                propagation.minimum_log_norm
            ),
            "minimum_cell_closure_gap_lower": decimal_lower(
                propagation.minimum_closure_gap
            ),
        },
        "event": event,
        "candidate_outer_history_comparison": comparison,
        "exact_outer_orbit_correction": correction,
        "history_ball": {
            "error_decomposition": (
                "E_guide+E_flow+E_orbit+E_time*F_tube+E_section"
            ),
            "E_time_times_F_tube_upper": decimal_upper(time_shift),
            "E_section_upper": decimal_upper(section_error),
            "declared_section_to_fourier_phase_zero_upper": decimal_upper(
                declared_to_phase_zero
            ),
            "reduced_history_distance_upper": decimal_upper(reduced_total),
            "complete_history_distance_upper": decimal_upper(complete_total),
            "design_history_ball_radius": "0.0001",
            "reduced_design_ball_margin_lower": decimal_lower(
                design_radius.lower - reduced_total
            ),
            "complete_design_ball_margin_lower": decimal_lower(
                design_radius.lower - complete_total
            ),
            "phase_center": (
                "phase zero of the unique phase-fixed outer RFDE orbit "
                "validated in the bound parent"
            ),
            "outer_attracting_tube_implication": (
                "conditional only: the ambient history bound gives entry if "
                "a validated ambient orbital attracting tube contains that "
                "ball; a Poincare-section return theorem additionally needs "
                "a validated phase chart with Q_phase*E_history below the "
                "section radius"
            ),
            "same_exact_poincare_section_inferred_from_E_section": False,
        },
        "theorem_statement": (
            "For the exact quiet initial history and the physical pulse "
            "u(t)=8/25 on 0<=t<1, the third positive crossing of the exact "
            "binary64 voltage level bound by the old routing target is unique "
            "in the declared "
            "directed event bracket. At that event, the reduced and complete "
            "histories lie within the displayed directed radii of phase zero "
            "of the validated exact outer periodic orbit. No attracting tube "
            "or basin capture is inferred."
        ),
        "claim_status": {
            **{name: True for name in TRUE_FLAGS},
            **{name: False for name in FALSE_FLAGS},
        },
    }
    return certificate


def build_third_return_result(repository: Path) -> dict[str, Any]:
    repository = Path(repository).resolve()
    certificate = build_third_return_certificate(repository)
    return {
        "certificate": certificate,
        "manifest": {
            "schema_id": SCHEMA_ID,
            "result": RESULT_RELATIVE_PATH,
            "default_command": DEFAULT_COMMAND,
            "arithmetic_scope": ARITHMETIC_SCOPE,
            "parent_sha256": {
                OUTER_ORBIT_RESULT_RELATIVE_PATH: OUTER_ORBIT_RESULT_SHA256,
                FLOQUET_TRANSFER_RESULT_RELATIVE_PATH: FLOQUET_TRANSFER_RESULT_SHA256,
                ROUTING_CONTRACT_RESULT_RELATIVE_PATH: ROUTING_CONTRACT_RESULT_SHA256,
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


def validate_third_return_result(
    payload: Mapping[str, Any],
    repository: Path,
    *,
    recompute: bool = False,
) -> None:
    if not isinstance(payload, Mapping) or set(payload) != {
        "certificate",
        "manifest",
    }:
        raise ValueError("third-return result must contain certificate and manifest")
    certificate = _mapping(payload.get("certificate"), "certificate")
    manifest = _mapping(payload.get("manifest"), "manifest")
    if manifest.get("schema_id") != SCHEMA_ID or certificate.get("schema_id") != SCHEMA_ID:
        raise ValueError("third-return schema changed")
    if manifest.get("result") != RESULT_RELATIVE_PATH:
        raise ValueError("third-return result path changed")
    if manifest.get("default_command") != DEFAULT_COMMAND:
        raise ValueError("third-return default command changed")
    if manifest.get("arithmetic_scope") != ARITHMETIC_SCOPE:
        raise ValueError("third-return arithmetic scope changed")
    if manifest.get("certificate_sha256") != canonical_sha256(certificate):
        raise ValueError("third-return certificate digest changed")
    repository = Path(repository).resolve()
    source_hashes = _mapping(manifest.get("source_sha256"), "source hashes")
    dependency_hashes = _mapping(
        manifest.get("dependency_source_sha256"), "dependency hashes"
    )
    if set(source_hashes) != set(SOURCE_MANIFEST):
        raise ValueError("third-return source manifest changed")
    if set(dependency_hashes) != set(DEPENDENCY_SOURCE_MANIFEST):
        raise ValueError("third-return dependency manifest changed")
    for relative in SOURCE_MANIFEST:
        if source_hashes.get(relative) != _sha256_path(repository / relative):
            raise ValueError(f"third-return source changed: {relative}")
    for relative in DEPENDENCY_SOURCE_MANIFEST:
        if dependency_hashes.get(relative) != _sha256_path(repository / relative):
            raise ValueError(f"third-return dependency changed: {relative}")
    parents = _mapping(manifest.get("parent_sha256"), "parent hashes")
    expected_parents = {
        OUTER_ORBIT_RESULT_RELATIVE_PATH: OUTER_ORBIT_RESULT_SHA256,
        FLOQUET_TRANSFER_RESULT_RELATIVE_PATH: FLOQUET_TRANSFER_RESULT_SHA256,
        ROUTING_CONTRACT_RESULT_RELATIVE_PATH: ROUTING_CONTRACT_RESULT_SHA256,
    }
    if dict(parents) != expected_parents:
        raise ValueError("third-return parent manifest changed")
    for relative, expected in expected_parents.items():
        if _sha256_path(repository / relative) != expected:
            raise ValueError(f"third-return bound parent changed: {relative}")
    claims = _mapping(certificate.get("claim_status"), "claim status")
    if set(claims) != set(TRUE_FLAGS) | set(FALSE_FLAGS):
        raise ValueError("third-return claim ledger changed")
    for name in TRUE_FLAGS:
        if claims.get(name) is not True:
            raise ValueError(f"proved third-return claim was removed: {name}")
    for name in FALSE_FLAGS:
        if claims.get(name) is not False:
            raise ValueError(f"open capture or routing claim was promoted: {name}")
    event = _mapping(certificate.get("event"), "event certificate")
    if (
        event.get("candidate_cell_count") != 6
        or tuple(event.get("crossing_directions", ())) != EXPECTED_CROSSING_DIRECTIONS
        or event.get("positive_crossing_count_through_declared_event") != 3
        or event.get("third_positive_event_bracket_validated") is not True
    ):
        raise ValueError("third positive event certificate changed")
    history_ball = _mapping(certificate.get("history_ball"), "history ball")
    if history_ball.get("error_decomposition") != (
        "E_guide+E_flow+E_orbit+E_time*F_tube+E_section"
    ):
        raise ValueError("third-return error decomposition changed")
    for name in (
        "reduced_history_distance_upper",
        "complete_history_distance_upper",
    ):
        value = DirectedInterval.from_decimal(str(history_ball.get(name)), 96)
        if value.upper >= DirectedInterval.from_decimal("0.0001", 96).lower:
            raise ValueError("third-return history ball no longer closes")
    if recompute:
        build_third_return_certificate.cache_clear()
        build_directed_propagation.cache_clear()
        rebuilt = build_third_return_certificate(repository)
        if canonical_sha256(rebuilt) != canonical_sha256(certificate):
            raise ValueError("third-return directed replay changed")


__all__ = [
    "DirectedPropagation",
    "EXPECTED_CROSSING_DIRECTIONS",
    "FINAL_SQRT5_MULTIPLIER",
    "FALSE_FLAGS",
    "MODEL_ID",
    "PULSE_AMPLITUDE",
    "RESULT_RELATIVE_PATH",
    "SCHEMA_ID",
    "build_directed_propagation",
    "build_third_return_certificate",
    "build_third_return_result",
    "canonical_sha256",
    "validate_third_return_result",
]
