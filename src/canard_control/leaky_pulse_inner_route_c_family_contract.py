"""Directed family pilot for the physical pulse at the inner Route-C section.

The parameter interval is ``J in [0.30105, 0.30120]``.  A degree-24
method-of-steps guide is built at the exact midpoint ``2409/8000`` on the
same two-origin ``Q(sqrt(5))`` grid used by the single-pulse certificates.
The error tube includes the whole pulse-amplitude half-width.  Along that
tube, scalar P-norm majorants enclose the first and second J variations.

This module initially supplies the expensive directed pilot on which the
source-bound family contract is based.  A stable-coordinate sign is not
deduced from any finite-section coordinate: it remains an interface for a
future validated Riesz covector and stable graph.
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
    _poly_cube,
    _poly_l1_upper,
    _poly_scale,
    _poly_sub,
    _poly_time_derivative,
    _symmetric_enlargement,
    _translated_source,
    _cube_coefficients_nearest,
)
from canard_control.leaky_quiet_history_basin import P11


SCHEMA_ID = "leaky-pulse-inner-route-c-family-contract-v1"
MODEL_ID = "autonomous-leaky-recovery-physical-pulse"

SOURCE_RELATIVE_PATH = (
    "src/canard_control/leaky_pulse_inner_route_c_family_contract.py"
)
GENERATOR_RELATIVE_PATH = (
    "experiments/leaky_pulse_inner_route_c_family_contract.py"
)
RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_pulse_inner_route_c_family_contract.json"
)
NOTE_RELATIVE_PATH = "docs/leaky-pulse-inner-route-c-family-contract.md"
TEST_RELATIVE_PATH = (
    "tests/test_leaky_pulse_inner_route_c_family_contract.py"
)
ROUTE_C_PARENT_RELATIVE_PATH = (
    "experiments/results/leaky_inner_stable_manifold_stage2_contract.json"
)
ROUTE_C_PARENT_SHA256 = (
    "eafa4d07b0558d9d4ce7423969379fa51875fcabce55af89a2378261fdb1e18d"
)
FINITE_SECTION_DIAGNOSTIC_RELATIVE_PATH = (
    "experiments/results/leaky_pulse_separator_bracket_tradeoff.json"
)
FINITE_SECTION_DIAGNOSTIC_SHA256 = (
    "afc4eaa10e85e0fca9236e019a184f381d41a01213423e38645eadd1720faa8c"
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
    "experiments/leaky_pulse_inner_route_c_family_contract.py"
)
ARITHMETIC_SCOPE = (
    "192-bit outward MPFR on the exact Q(sqrt(5)) two-origin grid; "
    "degree-24 directed Taylor/Bernstein method of steps at rational "
    "pulse centers; symmetric state tubes and first/second J-variation "
    "P-norm majorants. The registered finite-section signs remain "
    "binary64 diagnostics and are not stable-coordinate evidence."
)

PULSE_INTERVAL = (Fraction(6021, 20000), Fraction(753, 2500))
PULSE_CENTER = Fraction(2409, 8000)
PULSE_HALF_WIDTH = Fraction(3, 40000)
SHARD_HALF_WIDTH = Fraction(1, 400_000_000)
SHARD_WIDTH = 2 * SHARD_HALF_WIDTH
SHARD_COUNT = (PULSE_INTERVAL[1] - PULSE_INTERVAL[0]) / SHARD_WIDTH
if SHARD_COUNT.denominator != 1:
    raise AssertionError("the declared shard width does not tile the interval")
SHARD_COUNT_INTEGER = SHARD_COUNT.numerator
PILOT_SHARD_INDEX = SHARD_COUNT_INTEGER // 2
PILOT_SHARD_CENTER = (
    PULSE_INTERVAL[0]
    + (2 * PILOT_SHARD_INDEX + 1) * SHARD_HALF_WIDTH
)
PILOT_P_RADIUS_CAP = Fraction(1, 100)
DELAY_MULTIPLIERS = (4, 5)
FINAL_SQRT5_MULTIPLIER = 24
FINAL_NODE = _Node(0, FINAL_SQRT5_MULTIPLIER * GRID_DENOMINATOR)

TRUE_FLAGS = (
    "exact_wide_pulse_interval_registered",
    "route_c_exact_phase_zero_section_source_bound",
    "both_delay_breakpoint_families_preserved_in_runner",
    "full_width_directed_prefix_cells_closed",
    "one_exact_partition_shard_state_tube_closed_through_horizon",
    "one_exact_partition_shard_first_J_variation_majorant_closed",
    "one_exact_partition_shard_second_J_variation_majorant_closed",
    "exact_equal_width_partition_contract_registered",
    "finite_section_endpoint_signs_registered_as_nonproof_diagnostic",
)

FALSE_FLAGS = (
    "full_wide_interval_state_family_enclosure_validated",
    "all_equal_width_shards_replayed",
    "full_wide_interval_first_J_variation_enclosure_validated",
    "full_wide_interval_second_J_variation_enclosure_validated",
    "unique_route_c_pulse_event_validated",
    "uniform_route_c_pulse_event_speed_validated",
    "route_c_event_time_first_J_variation_validated",
    "route_c_event_time_second_J_variation_validated",
    "complete_history_route_c_family_ball_validated",
    "rfde_unstable_riesz_covector_validated",
    "inner_local_stable_graph_validated",
    "left_endpoint_stable_coordinate_positive_validated",
    "right_endpoint_stable_coordinate_negative_validated",
    "stable_gap_strictly_monotone_on_wide_interval_validated",
    "unique_physical_pulse_onset_validated",
    "two_sided_basin_routing_validated",
)


def _taylor_guide(
    start: tuple[gmpy2.mpfr, gmpy2.mpfr],
    step: gmpy2.mpfr,
    delayed_four: tuple[gmpy2.mpfr, ...],
    delayed_five: tuple[gmpy2.mpfr, ...],
    pulse_on: bool,
    pulse_center: Fraction,
    degree: int,
    precision: int,
) -> tuple[tuple[gmpy2.mpfr, ...], tuple[gmpy2.mpfr, ...]]:
    with gmpy2.context(precision=precision, round=gmpy2.RoundToNearest):
        epsilon = gmpy2.mpfr(EPSILON.numerator) / EPSILON.denominator
        unfolding = gmpy2.mpfr(UNFOLDING.numerator) / UNFOLDING.denominator
        kappa_1 = gmpy2.mpfr(KAPPA_1.numerator) / KAPPA_1.denominator
        kappa_3 = gmpy2.mpfr(KAPPA_3.numerator) / KAPPA_3.denominator
        pulse = (
            gmpy2.mpfr(pulse_center.numerator) / pulse_center.denominator
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
    pulse_center: Fraction,
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
    fast = _poly_add(
        fast,
        _poly_scale(
            _poly_sub(
                delayed_cubic,
                _poly_cube(_poly_add_constant(voltage, -_point(1, precision))),
            ),
            epsilon * kappa_3,
        ),
    )
    if pulse_on:
        fast = _poly_add_constant(
            fast, _fraction_interval(pulse_center, precision)
        )
    slow = _poly_scale(
        _poly_sub(
            _poly_sub(voltage, recovery),
            (_fraction_interval(UNFOLDING, precision),),
        ),
        epsilon,
    )
    return _p_box_norm_upper(
        _poly_l1_upper(_poly_sub(fast, _poly_time_derivative(voltage, step))),
        _poly_l1_upper(_poly_sub(slow, _poly_time_derivative(recovery, step))),
        precision,
    )


def _gronwall_upper(
    initial: gmpy2.mpfr,
    forcing: gmpy2.mpfr,
    mu: gmpy2.mpfr,
    elapsed: gmpy2.mpfr,
    precision: int,
) -> gmpy2.mpfr:
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        exponential = gmpy2.exp(mu * elapsed)
        if mu < 0:
            return exponential * initial + elapsed * forcing
        if mu == 0:
            return initial + elapsed * forcing
        return exponential * initial + (exponential - 1) / mu * forcing


def _nodes(final_node: _Node = FINAL_NODE) -> tuple[_Node, ...]:
    if QUIET_FINAL_NODE_INDEX <= final_node.index:
        raise AssertionError("the parent grid is too short")
    nodes = tuple(
        node for node in _forward_nodes() if _node_compare(node, final_node) <= 0
    )
    if nodes[0] != ZERO_NODE or nodes[-1] != final_node:
        raise AssertionError("the family horizon is absent from the grid")
    return nodes


@dataclass(frozen=True)
class FamilyCell:
    state: _CellProof
    first_endpoint_upper: gmpy2.mpfr
    first_maximum_upper: gmpy2.mpfr
    second_endpoint_upper: gmpy2.mpfr
    second_maximum_upper: gmpy2.mpfr


@dataclass(frozen=True)
class RouteCFamilyPilot:
    cells: Mapping[tuple[int, int, int, int], FamilyCell]
    pulse_center: Fraction
    pulse_half_width: Fraction
    final_sqrt5_multiplier: int
    requested_cell_count: int
    closed_cell_count: int
    completed: bool
    failure_cell_key: tuple[int, int, int, int] | None
    failure_reason: str | None
    maximum_state_family_radius: gmpy2.mpfr
    maximum_first_variation_p_norm: gmpy2.mpfr
    maximum_second_variation_p_norm: gmpy2.mpfr
    minimum_state_closure_gap: gmpy2.mpfr


@lru_cache(maxsize=None)
def run_route_c_family_pilot(
    pulse_center: Fraction = PULSE_CENTER,
    pulse_half_width: Fraction = PULSE_HALF_WIDTH,
    final_sqrt5_multiplier: int = FINAL_SQRT5_MULTIPLIER,
) -> RouteCFamilyPilot:
    if pulse_half_width < 0:
        raise ValueError("the pulse half-width must be nonnegative")
    if final_sqrt5_multiplier <= 0:
        raise ValueError("the final sqrt(5) multiplier must be positive")
    final_node = _Node(0, final_sqrt5_multiplier * GRID_DENOMINATOR)
    nodes = _nodes(final_node)
    precision = PRECISION_BITS
    alpha = _alpha_interval(precision)
    alpha_center = _nearest_midpoint(alpha)
    with gmpy2.context(precision=precision, round=gmpy2.RoundToNearest):
        recovery_center = alpha_center - (
            gmpy2.mpfr(UNFOLDING.numerator) / UNFOLDING.denominator
        )
    voltage_coordinate, _, alpha_diagonal = _p_constants(precision)
    alpha_difference = (alpha - _mpfr_point(alpha_center, precision)).upper_abs()
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        initial_error = alpha_diagonal * alpha_difference
        p11 = gmpy2.mpfr(P11.numerator) / P11.denominator
        fast_input_p_norm = gmpy2.sqrt(p11)
        pulse_family_forcing = fast_input_p_norm * (
            gmpy2.mpfr(pulse_half_width.numerator) / pulse_half_width.denominator
        )
    history_voltage = tuple(
        [alpha_center] + [gmpy2.mpfr(0)] * TAYLOR_DEGREE
    )
    state_cells: dict[tuple[int, int, int, int], _CellProof] = {}
    family_cells: dict[tuple[int, int, int, int], FamilyCell] = {}
    previous: FamilyCell | None = None
    maximum_state = initial_error
    maximum_first = gmpy2.mpfr(0)
    maximum_second = gmpy2.mpfr(0)
    minimum_gap = gmpy2.inf()

    failure_cell_key: tuple[int, int, int, int] | None = None
    failure_reason: str | None = None

    for left, right in zip(nodes[:-1], nodes[1:], strict=True):
        step_interval = _node_interval(right, precision) - _node_interval(
            left, precision
        )
        step_center = _nearest_midpoint(step_interval)
        pulse_on = _node_compare(left, PULSE_RELEASE_NODE) < 0
        sources = {}
        source_family: dict[int, FamilyCell | None] = {}
        for delay in DELAY_MULTIPLIERS:
            sources[delay] = _translated_source(
                state_cells,
                left,
                right,
                delay,
                history_voltage,
                initial_error,
            )
            source_family[delay] = family_cells.get(
                _cell_key(left.shifted(delay), right.shifted(delay))
            )
        if previous is None:
            start = (alpha_center, recovery_center)
            state_start = initial_error
            first_start = gmpy2.mpfr(0)
            second_start = gmpy2.mpfr(0)
            center_jump = gmpy2.mpfr(0)
        else:
            voltage_start, voltage_endpoint = _guide_endpoint(
                previous.state.voltage, precision
            )
            recovery_start, recovery_endpoint = _guide_endpoint(
                previous.state.recovery, precision
            )
            start = (voltage_start, recovery_start)
            center_jump = _center_jump_norm(
                start, (voltage_endpoint, recovery_endpoint), precision
            )
            with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
                state_start = previous.state.endpoint_radius + center_jump
            first_start = previous.first_endpoint_upper
            second_start = previous.second_endpoint_upper
        voltage, recovery = _taylor_guide(
            start,
            step_center,
            sources[4][0],
            sources[5][0],
            pulse_on,
            pulse_center,
            TAYLOR_DEGREE,
            precision,
        )
        voltage_range = _poly_bernstein_range(
            tuple(_mpfr_point(value, precision) for value in voltage)
        )
        residual = _guide_residual_upper(
            voltage,
            recovery,
            sources[4][0],
            sources[5][0],
            step_interval,
            pulse_on,
            pulse_center,
        )
        with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
            radius = (
                max(state_start, gmpy2.mpfr(TUBE_FLOOR))
                * gmpy2.mpfr(TUBE_INFLATION)
                + gmpy2.mpfr(TUBE_FLOOR)
            )
        for _ in range(MAXIMUM_FIXED_POINT_ITERATIONS):
            if not gmpy2.is_finite(radius):
                failure_cell_key = _cell_key(left, right)
                failure_reason = "nonfinite_state_radius"
                break
            current_tube = _symmetric_enlargement(
                voltage_range, voltage_coordinate * radius
            )
            mu = _current_log_norm_upper(current_tube, precision)
            delay_forcing = {}
            for delay in DELAY_MULTIPLIERS:
                delayed_tube = _symmetric_enlargement(
                    sources[delay][1], voltage_coordinate * sources[delay][2]
                )
                delay_forcing[delay] = _delayed_forcing_upper(
                    delayed_tube, precision
                )
            with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
                state_forcing = (
                    residual
                    + delay_forcing[4] * sources[4][2]
                    + delay_forcing[5] * sources[5][2]
                    + (pulse_family_forcing if pulse_on else 0)
                )
            state_endpoint = _gronwall_upper(
                state_start,
                state_forcing,
                mu,
                step_interval.upper,
                precision,
            )
            if not gmpy2.is_finite(state_endpoint):
                failure_cell_key = _cell_key(left, right)
                failure_reason = "nonfinite_state_endpoint_bound"
                break
            with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
                closure_gap = radius - state_endpoint
            if closure_gap > 0:
                break
            with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
                radius = (
                    max(radius, state_endpoint)
                    * gmpy2.mpfr(TUBE_INFLATION)
                    + gmpy2.mpfr(TUBE_FLOOR)
                )
        else:
            failure_cell_key = _cell_key(left, right)
            failure_reason = "state_fixed_point_did_not_close"

        if failure_cell_key is not None:
            break

        first_delayed = {
            delay: (
                source_family[delay].first_maximum_upper
                if source_family[delay] is not None
                else gmpy2.mpfr(0)
            )
            for delay in DELAY_MULTIPLIERS
        }
        with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
            first_forcing = (
                (fast_input_p_norm if pulse_on else 0)
                + delay_forcing[4] * first_delayed[4]
                + delay_forcing[5] * first_delayed[5]
            )
        first_endpoint = _gronwall_upper(
            first_start,
            first_forcing,
            mu,
            step_interval.upper,
            precision,
        )
        first_maximum = max(first_start, first_endpoint)

        second_delayed = {
            delay: (
                source_family[delay].second_maximum_upper
                if source_family[delay] is not None
                else gmpy2.mpfr(0)
            )
            for delay in DELAY_MULTIPLIERS
        }
        current_voltage_error = voltage_coordinate * radius
        current_state_tube = _symmetric_enlargement(
            voltage_range, current_voltage_error
        )
        epsilon = _fraction_interval(EPSILON, precision)
        kappa_3 = _fraction_interval(KAPPA_3, precision)
        current_second_coefficient = (
            -2 * current_state_tube
            - 6 * epsilon * kappa_3 * (current_state_tube - 1)
        ).upper_abs()
        with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
            quadratic_scalar = current_second_coefficient * (
                voltage_coordinate * first_maximum
            ) ** 2
        for delay in DELAY_MULTIPLIERS:
            delayed_tube = _symmetric_enlargement(
                sources[delay][1], voltage_coordinate * sources[delay][2]
            )
            delayed_second_coefficient = (
                3 * epsilon * kappa_3 * (delayed_tube - 1)
            ).upper_abs()
            with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
                quadratic_scalar += delayed_second_coefficient * (
                    voltage_coordinate * first_delayed[delay]
                ) ** 2
        with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
            quadratic_p = fast_input_p_norm * quadratic_scalar
            second_forcing = (
                delay_forcing[4] * second_delayed[4]
                + delay_forcing[5] * second_delayed[5]
                + quadratic_p
            )
        second_endpoint = _gronwall_upper(
            second_start,
            second_forcing,
            mu,
            step_interval.upper,
            precision,
        )
        second_maximum = max(second_start, second_endpoint)

        state = _CellProof(
            left=left,
            right=right,
            voltage=voltage,
            recovery=recovery,
            voltage_range=voltage_range,
            endpoint_radius=state_endpoint,
            maximum_radius=radius,
            residual_upper=residual,
            logarithmic_norm_upper=mu,
            delay_four_forcing_upper=delay_forcing[4],
            delay_five_forcing_upper=delay_forcing[5],
            closure_gap_lower=closure_gap,
            center_jump_upper=center_jump,
        )
        family = FamilyCell(
            state=state,
            first_endpoint_upper=first_endpoint,
            first_maximum_upper=first_maximum,
            second_endpoint_upper=second_endpoint,
            second_maximum_upper=second_maximum,
        )
        key = _cell_key(left, right)
        state_cells[key] = state
        family_cells[key] = family
        previous = family
        maximum_state = max(maximum_state, radius)
        maximum_first = max(maximum_first, first_maximum)
        maximum_second = max(maximum_second, second_maximum)
        minimum_gap = min(minimum_gap, closure_gap)

    return RouteCFamilyPilot(
        cells=family_cells,
        pulse_center=pulse_center,
        pulse_half_width=pulse_half_width,
        final_sqrt5_multiplier=final_sqrt5_multiplier,
        requested_cell_count=len(nodes) - 1,
        closed_cell_count=len(family_cells),
        completed=failure_cell_key is None,
        failure_cell_key=failure_cell_key,
        failure_reason=failure_reason,
        maximum_state_family_radius=maximum_state,
        maximum_first_variation_p_norm=maximum_first,
        maximum_second_variation_p_norm=maximum_second,
        minimum_state_closure_gap=minimum_gap,
    )


def build_route_c_family_pilot() -> RouteCFamilyPilot:
    """Replay the unsplit full-width pilot.

    Failure is returned as structured evidence because the full-width
    symmetric tube is expected to lose closure before the requested horizon.
    """

    return run_route_c_family_pilot()


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
        raise ValueError(f"bound parent changed: {relative}")
    return json.loads(path.read_text(encoding="utf-8"))


def _fraction_payload(value: Fraction) -> dict[str, str]:
    return {
        "numerator": str(value.numerator),
        "denominator": str(value.denominator),
        "binary64_decimal_diagnostic": format(float(value), ".17g"),
    }


def _node_payload(node: _Node) -> dict[str, Any]:
    value = _node_interval(node, PRECISION_BITS)
    return {
        "origin": node.origin,
        "index": node.index,
        "exact": f"{node.origin}+({node.index}/{GRID_DENOMINATOR})*sqrt(5)",
        "lower": decimal_lower(value.lower),
        "upper": decimal_upper(value.upper),
    }


def _pilot_summary(pilot: RouteCFamilyPilot) -> dict[str, Any]:
    voltage_coordinate, recovery_coordinate, _ = _p_constants(PRECISION_BITS)
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
        y_conversion = max(voltage_coordinate, recovery_coordinate)
        y_error = y_conversion * pilot.maximum_state_family_radius
    failure = None
    if pilot.failure_cell_key is not None:
        left = _Node(pilot.failure_cell_key[0], pilot.failure_cell_key[1])
        right = _Node(pilot.failure_cell_key[2], pilot.failure_cell_key[3])
        failure = {
            "cell_key": list(pilot.failure_cell_key),
            "left_time": _node_payload(left),
            "right_time": _node_payload(right),
            "reason": pilot.failure_reason,
        }
    return {
        "pulse_center": _fraction_payload(pilot.pulse_center),
        "pulse_half_width": _fraction_payload(pilot.pulse_half_width),
        "pulse_interval_lower": _fraction_payload(
            pilot.pulse_center - pilot.pulse_half_width
        ),
        "pulse_interval_upper": _fraction_payload(
            pilot.pulse_center + pilot.pulse_half_width
        ),
        "final_time_exact": f"{pilot.final_sqrt5_multiplier}*sqrt(5)",
        "requested_cell_count": pilot.requested_cell_count,
        "closed_cell_count": pilot.closed_cell_count,
        "remaining_cell_count": (
            pilot.requested_cell_count - pilot.closed_cell_count
        ),
        "completed": pilot.completed,
        "failure": failure,
        "maximum_state_P_radius_upper": decimal_upper(
            pilot.maximum_state_family_radius
        ),
        "P_to_Y_coordinate_norm_upper": decimal_upper(y_conversion),
        "state_tube_Y_coordinate_error_upper": decimal_upper(y_error),
        "maximum_first_J_variation_P_norm_upper": decimal_upper(
            pilot.maximum_first_variation_p_norm
        ),
        "maximum_second_J_variation_P_norm_upper": decimal_upper(
            pilot.maximum_second_variation_p_norm
        ),
        "minimum_closed_cell_gap_lower": decimal_lower(
            pilot.minimum_state_closure_gap
        ),
    }


@lru_cache(maxsize=1)
def build_route_c_family_certificate(repository: Path) -> dict[str, Any]:
    repository = Path(repository).resolve()
    route_c_payload = _load_bound_json(
        repository, ROUTE_C_PARENT_RELATIVE_PATH, ROUTE_C_PARENT_SHA256
    )
    diagnostic_payload = _load_bound_json(
        repository,
        FINITE_SECTION_DIAGNOSTIC_RELATIVE_PATH,
        FINITE_SECTION_DIAGNOSTIC_SHA256,
    )
    route_c = _mapping(route_c_payload.get("contract"), "Route-C contract")
    route_c_audit = _mapping(
        route_c.get("explicit_voltage_section_audit"),
        "Route-C voltage-section audit",
    )
    if route_c_audit.get("exact_phase_zero_section_formula") != (
        "h_C(phi)=phi_v(0)-V_true(0)"
    ):
        raise ValueError("the bound Route-C section changed")
    rows = _mapping(
        diagnostic_payload.get("certificate"), "finite-section certificate"
    ).get("rows")
    if not isinstance(rows, list):
        raise ValueError("finite-section rows changed")
    wide_rows = [row for row in rows if row.get("bracket_id") == "wide_recommended"]
    if len(wide_rows) != 1:
        raise ValueError("the recommended finite-section row changed")
    wide_row = _mapping(wide_rows[0], "wide finite-section row")

    full = run_route_c_family_pilot(PULSE_CENTER, PULSE_HALF_WIDTH)
    shard = run_route_c_family_pilot(PILOT_SHARD_CENTER, SHARD_HALF_WIDTH)
    point = run_route_c_family_pilot(PILOT_SHARD_CENTER, Fraction(0))
    if full.completed or full.closed_cell_count <= 0:
        raise ArithmeticError("the registered full-width failure row changed")
    if not shard.completed or not point.completed:
        raise ArithmeticError("a registered shard pilot no longer closes")
    cap = gmpy2.mpfr(PILOT_P_RADIUS_CAP.numerator) / PILOT_P_RADIUS_CAP.denominator
    if shard.maximum_state_family_radius >= cap:
        raise ArithmeticError("the registered pilot shard exceeds its P-radius cap")

    certificate = {
        "schema_id": SCHEMA_ID,
        "model_id": MODEL_ID,
        "wide_interval": {
            "lower": _fraction_payload(PULSE_INTERVAL[0]),
            "upper": _fraction_payload(PULSE_INTERVAL[1]),
            "center": _fraction_payload(PULSE_CENTER),
            "half_width": _fraction_payload(PULSE_HALF_WIDTH),
        },
        "route_c_section_binding": {
            "formula": route_c_audit["exact_phase_zero_section_formula"],
            "validated_orbit_section_voltage_lower": route_c_audit[
                "validated_orbit_section_voltage_lower"
            ],
            "validated_orbit_section_voltage_upper": route_c_audit[
                "validated_orbit_section_voltage_upper"
            ],
            "physical_orbit_event_speed_lower": route_c_audit[
                "physical_voltage_event_speed_at_orbit_lower"
            ],
            "declared_section_ball_radius": route_c_audit[
                "declared_section_ball_radius"
            ],
            "uniform_orbit_ball_speed_lower": route_c_audit[
                "uniform_event_speed_lower_on_declared_section_ball"
            ],
            "section_chart_projection_norm_upper": route_c_audit[
                "section_chart_projection_norm_upper"
            ],
            "these_orbit_section_constants_do_not_prove_a_pulse_crossing": True,
        },
        "directed_full_width_pilot": _pilot_summary(full),
        "directed_partition_shard_pilot": {
            **_pilot_summary(shard),
            "partition_index_zero_based": PILOT_SHARD_INDEX,
            "P_radius_cap": _fraction_payload(PILOT_P_RADIUS_CAP),
            "P_radius_cap_met": True,
            "not_a_route_c_history_ball": True,
        },
        "zero_width_variation_baseline": {
            **_pilot_summary(point),
            "interpretation": (
                "shrinking the parameter width to zero does not cure the "
                "large zero-centered first/second variation majorants"
            ),
        },
        "equal_width_shard_contract": {
            "shard_half_width": _fraction_payload(SHARD_HALF_WIDTH),
            "shard_width": _fraction_payload(SHARD_WIDTH),
            "exact_shard_count": SHARD_COUNT_INTEGER,
            "center_formula": (
                "c_k=6021/20000+(2*k+1)/400000000, "
                "k=0,...,29999"
            ),
            "pilot_partition_index_zero_based": PILOT_SHARD_INDEX,
            "partition_shards_replayed": 1,
            "partition_shards_remaining": SHARD_COUNT_INTEGER - 1,
            "per_shard_acceptance_gate": (
                "completed=true on all 1152 cells, finite first/second "
                "J-variation majorants, then independent event/history gates"
            ),
            "state_tube_only_compute_estimate_is_not_a_family_proof": True,
        },
        "event_and_complete_history_interface": {
            "route_c_event_bracket": None,
            "unique_event_speed_lower": None,
            "event_time_first_J_variation": None,
            "event_time_second_J_variation": None,
            "complete_history_family_radius": None,
            "required_event_alignment": (
                "solve h_C(z(tau(J),J))=0 on each shard and pull the whole "
                "history theta->z(tau(J)+theta,J), theta in [-5*sqrt(5),0]"
            ),
        },
        "stable_coordinate_interface": {
            "definition": "H(J)=ell_u(y_u(J))-h_s(y_s(J))",
            "left_endpoint_stable_coordinate": None,
            "right_endpoint_stable_coordinate": None,
            "uniform_stable_gap_derivative": None,
            "required_inputs": [
                "validated RFDE unstable Riesz covector ell_u",
                "validated local stable graph h_s and its derivative bounds",
                "event-aligned complete-history family enclosure",
            ],
            "finite_section_left_coordinate_observed": wide_row[
                "left_coordinate"
            ],
            "finite_section_right_coordinate_observed": wide_row[
                "right_coordinate"
            ],
            "finite_section_left_centered_derivative_observed": wide_row[
                "left_centered_derivative"
            ],
            "finite_section_right_centered_derivative_observed": wide_row[
                "right_centered_derivative"
            ],
            "finite_section_values_used_as_stable_coordinate_proof": False,
        },
        "method_diagnosis": {
            "state_sharding_is_computationally_executable": True,
            "state_sharding_alone_solves_event_or_history_alignment": False,
            "zero_centered_variation_majorant_is_structurally_usable": False,
            "recommended_replacement": (
                "cellwise parameter Taylor jets z0,...,z4 with only the "
                "highest-order remainder enclosed symmetrically; implicit "
                "event jets and a common-event complete-history pullback"
            ),
        },
        "theorem_statement": (
            "The unsplit interval J in [0.30105,0.30120] has a directed "
            "730-cell prefix but loses symmetric-tube closure with 422 cells "
            "remaining. One exact member of a 30000-shard rational partition "
            "closes all 1152 cells, together with finite but unusably large "
            "first/second J-variation norm majorants. No Route-C pulse event, "
            "complete-history family ball, stable-coordinate sign, onset, or "
            "routing statement follows."
        ),
        "claim_status": {
            **{name: True for name in TRUE_FLAGS},
            **{name: False for name in FALSE_FLAGS},
        },
    }
    return certificate


def build_route_c_family_result(repository: Path) -> dict[str, Any]:
    repository = Path(repository).resolve()
    certificate = build_route_c_family_certificate(repository)
    return {
        "certificate": certificate,
        "manifest": {
            "schema_id": SCHEMA_ID,
            "result": RESULT_RELATIVE_PATH,
            "default_command": DEFAULT_COMMAND,
            "arithmetic_scope": ARITHMETIC_SCOPE,
            "parent_sha256": {
                ROUTE_C_PARENT_RELATIVE_PATH: ROUTE_C_PARENT_SHA256,
                FINITE_SECTION_DIAGNOSTIC_RELATIVE_PATH: (
                    FINITE_SECTION_DIAGNOSTIC_SHA256
                ),
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


def validate_route_c_family_result(
    payload: Mapping[str, Any],
    repository: Path,
    *,
    recompute: bool = False,
) -> None:
    if not isinstance(payload, Mapping) or set(payload) != {
        "certificate",
        "manifest",
    }:
        raise ValueError("Route-C family result must contain certificate and manifest")
    certificate = _mapping(payload.get("certificate"), "certificate")
    manifest = _mapping(payload.get("manifest"), "manifest")
    if manifest.get("schema_id") != SCHEMA_ID or certificate.get("schema_id") != SCHEMA_ID:
        raise ValueError("Route-C family schema changed")
    if manifest.get("result") != RESULT_RELATIVE_PATH:
        raise ValueError("Route-C family result path changed")
    if manifest.get("default_command") != DEFAULT_COMMAND:
        raise ValueError("Route-C family default command changed")
    if manifest.get("arithmetic_scope") != ARITHMETIC_SCOPE:
        raise ValueError("Route-C family arithmetic scope changed")
    if manifest.get("certificate_sha256") != canonical_sha256(certificate):
        raise ValueError("Route-C family certificate digest changed")
    repository = Path(repository).resolve()
    source_hashes = _mapping(manifest.get("source_sha256"), "source hashes")
    dependency_hashes = _mapping(
        manifest.get("dependency_source_sha256"), "dependency hashes"
    )
    if set(source_hashes) != set(SOURCE_MANIFEST):
        raise ValueError("Route-C family source manifest changed")
    if set(dependency_hashes) != set(DEPENDENCY_SOURCE_MANIFEST):
        raise ValueError("Route-C family dependency manifest changed")
    for relative in SOURCE_MANIFEST:
        if source_hashes.get(relative) != _sha256_path(repository / relative):
            raise ValueError(f"Route-C family source changed: {relative}")
    for relative in DEPENDENCY_SOURCE_MANIFEST:
        if dependency_hashes.get(relative) != _sha256_path(repository / relative):
            raise ValueError(f"Route-C family dependency changed: {relative}")
    expected_parents = {
        ROUTE_C_PARENT_RELATIVE_PATH: ROUTE_C_PARENT_SHA256,
        FINITE_SECTION_DIAGNOSTIC_RELATIVE_PATH: FINITE_SECTION_DIAGNOSTIC_SHA256,
    }
    if dict(_mapping(manifest.get("parent_sha256"), "parent hashes")) != expected_parents:
        raise ValueError("Route-C family parent manifest changed")
    for relative, expected in expected_parents.items():
        if _sha256_path(repository / relative) != expected:
            raise ValueError(f"Route-C family bound parent changed: {relative}")
    claims = _mapping(certificate.get("claim_status"), "claim status")
    if set(claims) != set(TRUE_FLAGS) | set(FALSE_FLAGS):
        raise ValueError("Route-C family claim ledger changed")
    for name in TRUE_FLAGS:
        if claims.get(name) is not True:
            raise ValueError(f"proved Route-C pilot claim was removed: {name}")
    for name in FALSE_FLAGS:
        if claims.get(name) is not False:
            raise ValueError(f"open Route-C family claim was promoted: {name}")
    full = _mapping(
        certificate.get("directed_full_width_pilot"), "full-width pilot"
    )
    if (
        full.get("completed") is not False
        or full.get("closed_cell_count") != 730
        or full.get("remaining_cell_count") != 422
    ):
        raise ValueError("full-width failure frontier changed")
    shard = _mapping(
        certificate.get("directed_partition_shard_pilot"), "shard pilot"
    )
    if (
        shard.get("completed") is not True
        or shard.get("closed_cell_count") != 1152
        or shard.get("P_radius_cap_met") is not True
    ):
        raise ValueError("registered Route-C shard closure changed")
    cover = _mapping(
        certificate.get("equal_width_shard_contract"), "shard contract"
    )
    if (
        cover.get("exact_shard_count") != 30000
        or cover.get("partition_shards_replayed") != 1
        or cover.get("partition_shards_remaining") != 29999
    ):
        raise ValueError("Route-C shard budget changed")
    stable = _mapping(
        certificate.get("stable_coordinate_interface"),
        "stable-coordinate interface",
    )
    if (
        stable.get("left_endpoint_stable_coordinate") is not None
        or stable.get("right_endpoint_stable_coordinate") is not None
        or stable.get("finite_section_values_used_as_stable_coordinate_proof")
        is not False
    ):
        raise ValueError("finite-section data were promoted to stable evidence")
    event = _mapping(
        certificate.get("event_and_complete_history_interface"),
        "event/history interface",
    )
    for key in (
        "route_c_event_bracket",
        "unique_event_speed_lower",
        "event_time_first_J_variation",
        "event_time_second_J_variation",
        "complete_history_family_radius",
    ):
        if event.get(key) is not None:
            raise ValueError("an open event/history input was silently populated")
    if recompute:
        build_route_c_family_certificate.cache_clear()
        run_route_c_family_pilot.cache_clear()
        rebuilt = build_route_c_family_certificate(repository)
        if canonical_sha256(rebuilt) != canonical_sha256(certificate):
            raise ValueError("Route-C family directed replay changed")


__all__ = [
    "FALSE_FLAGS",
    "PULSE_CENTER",
    "PULSE_HALF_WIDTH",
    "PULSE_INTERVAL",
    "RESULT_RELATIVE_PATH",
    "RouteCFamilyPilot",
    "SHARD_COUNT_INTEGER",
    "SHARD_HALF_WIDTH",
    "TRUE_FLAGS",
    "build_route_c_family_pilot",
    "build_route_c_family_certificate",
    "build_route_c_family_result",
    "canonical_sha256",
    "run_route_c_family_pilot",
    "validate_route_c_family_result",
]
