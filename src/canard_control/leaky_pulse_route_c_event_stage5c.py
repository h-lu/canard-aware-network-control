"""Stage-5C Route-C event certificate for the physical pulse family.

The Stage-5B artifact validates a correlated fourth-order parameter model at
fixed physical time.  This module uses that *same* coefficient enclosure to
prove a transverse Route-C crossing for every pulse amplitude in the wide
interval.  It also encloses the four implicit event-time derivatives at the
centre parameter and validates a uniform fourth-order event-time model.

The output stops before the inner stable sheet.  In particular, the Route-C
adjoint by itself is not a stable graph and is not used to manufacture endpoint
stable-coordinate signs or an onset root.
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
from canard_control.leaky_pulse_parameter_jet_directed_enclosure import (
    J0,
    PARAMETER_HALF_WIDTH,
    PARAMETER_INTERVAL,
    CoefficientCell,
    CoefficientPropagation,
    RemainderPropagation,
    _coordinate_bounds,
    build_coefficient_propagation,
    build_remainder_propagation,
    canonical_sha256,
)
from canard_control.leaky_pulse_quiet_capture import (
    GRID_DENOMINATOR,
    PRECISION_BITS,
    _Node,
    _cell_key,
    _fraction_interval,
    _mpfr_point,
    _node_compare,
    _node_interval,
    _point,
    _poly_add,
    _poly_add_constant,
    _poly_bernstein_range,
    _poly_multiply,
    _symmetric_enlargement,
)


SCHEMA_ID = "leaky-pulse-route-c-event-stage5c-v1"
MODEL_ID = "autonomous-leaky-recovery-physical-pulse"

SOURCE_RELATIVE_PATH = "src/canard_control/leaky_pulse_route_c_event_stage5c.py"
GENERATOR_RELATIVE_PATH = "experiments/leaky_pulse_route_c_event_stage5c.py"
RESULT_RELATIVE_PATH = "experiments/results/leaky_pulse_route_c_event_stage5c.json"
NOTE_RELATIVE_PATH = "docs/leaky-pulse-route-c-event-stage5c.md"
TEST_RELATIVE_PATH = "tests/test_leaky_pulse_route_c_event_stage5c.py"

STAGE5B_RELATIVE_PATH = (
    "experiments/results/leaky_pulse_parameter_jet_directed_enclosure.json"
)
STAGE5B_SHA256 = "71276785fd803b663fc11de9489751ccd53dd8a408323a0bb140d0c9e7b7862b"
ROUTE_C_CONTRACT_RELATIVE_PATH = (
    "experiments/results/leaky_inner_stable_manifold_stage2_contract.json"
)
ROUTE_C_CONTRACT_SHA256 = (
    "eafa4d07b0558d9d4ce7423969379fa51875fcabce55af89a2378261fdb1e18d"
)
ROUTE_C_ADJOINT_RELATIVE_PATH = (
    "experiments/results/leaky_route_c_adjoint_stage4d.json"
)
ROUTE_C_ADJOINT_SHA256 = (
    "af51bcfc20000b804134c1d8b9cacc303013676c440a89f2ecb52faf0042d568"
)

SOURCE_MANIFEST = (
    SOURCE_RELATIVE_PATH,
    GENERATOR_RELATIVE_PATH,
    NOTE_RELATIVE_PATH,
)
DEPENDENCY_SOURCE_MANIFEST = (
    "src/canard_control/autonomous_leaky_recovery_bistable.py",
    "src/canard_control/directed_interval.py",
    "src/canard_control/leaky_pulse_parameter_jet_directed_enclosure.py",
    "src/canard_control/leaky_pulse_quiet_capture.py",
)
DEFAULT_COMMAND = (
    "OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 "
    "PYTHONPATH=.venv/lib/python3.14/site-packages:src /usr/bin/python3 "
    "experiments/leaky_pulse_route_c_event_stage5c.py"
)
ARITHMETIC_SCOPE = (
    "192-bit outward MPFR reuse of the source-bound Stage-5B 1152-cell "
    "correlated parameter enclosure; exact Route-C phase-zero voltage-level "
    "binding; cellwise Bernstein endpoint and vector-field bounds; recursive "
    "mixed time/parameter differential algebra at the centre event; and a "
    "subdivided Bernstein proof of a fourth-order event-time graph tube"
)

# This is the three-cell bracket containing the late positive crossing selected
# by the finite-section pilot throughout the wide pulse family.  The certificate
# proves one crossing in this bracket; it deliberately does not infer that
# exactly two earlier crossings occurred.
EVENT_BRACKET_LEFT_NODE = _Node(0, 555)
EVENT_BRACKET_RIGHT_NODE = _Node(1, 546)
CENTER_EVENT_LEFT_NODE = _Node(1, 545)
CENTER_EVENT_RIGHT_NODE = _Node(0, 556)
CENTER_EVENT_CELL_KEY = _cell_key(
    CENTER_EVENT_LEFT_NODE, CENTER_EVENT_RIGHT_NODE
)
PARAMETER_SUBDIVISIONS = 64
EVENT_GRAPH_REMAINDER = Fraction(1, 10_000)
CENTER_EVENT_SIGN_MARGIN = Fraction(1, 10**16)
IMPLICIT_JET_ORDER = 4


TRUE_FLAGS = (
    "route_c_exact_phase_zero_level_source_bound",
    "stage5b_correlated_fixed_time_family_reused_without_state_sharding",
    "wide_parameter_event_bracket_endpoint_signs_validated",
    "uniform_positive_event_speed_on_whole_event_bracket_validated",
    "one_and_only_one_route_c_event_in_declared_bracket_for_every_J_validated",
    "center_parameter_event_bracket_validated",
    "center_implicit_event_time_jet_through_order_four_validated",
    "uniform_fourth_order_event_time_graph_remainder_validated",
    "common_event_complete_history_pullback_defined_in_Y",
    "common_event_complete_history_tube_validated",
    "stable_sheet_inputs_kept_separate_from_event_certificate",
)

FALSE_FLAGS = (
    "declared_event_proved_to_be_the_third_post_release_crossing",
    "uniform_J_derivative_tube_for_event_aligned_complete_history_validated",
    "common_event_complete_history_jet_through_order_four_validated",
    "inner_local_stable_graph_validated",
    "stable_coordinate_endpoint_signs_validated",
    "stable_gap_derivative_excludes_zero_validated",
    "interval_newton_onset_validated",
    "unique_physical_pulse_onset_validated",
    "two_sided_basin_routing_validated",
    "outer_or_quiet_capture_from_both_sides_validated",
)


def _sha256_path(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _mapping(value: Any, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{name} must be a mapping")
    return value


def _load_bound_json(repository: Path, relative: str, expected: str) -> Any:
    path = repository / relative
    if _sha256_path(path) != expected:
        raise ValueError(f"Stage-5C bound parent changed: {relative}")
    return json.loads(path.read_text(encoding="utf-8"))


def _zero(precision: int = PRECISION_BITS) -> DirectedInterval:
    return _point(0, precision)


def _hull(values: Sequence[DirectedInterval]) -> DirectedInterval:
    if not values:
        raise ValueError("cannot hull an empty interval family")
    precision = values[0].precision
    return DirectedInterval.from_bounds(
        min(value.lower for value in values),
        max(value.upper for value in values),
        precision,
    )


def _intersection(
    left: DirectedInterval, right: DirectedInterval
) -> DirectedInterval:
    if left.precision != right.precision:
        raise ValueError("interval precisions differ")
    lower = max(left.lower, right.lower)
    upper = min(left.upper, right.upper)
    if lower > upper:
        raise ArithmeticError("two proved enclosures have empty intersection")
    return DirectedInterval.from_bounds(lower, upper, left.precision)


def _power_eval(
    coefficients: Sequence[DirectedInterval], value: DirectedInterval
) -> DirectedInterval:
    answer = _zero(value.precision)
    for coefficient in reversed(coefficients):
        answer = answer * value + coefficient
    return answer


def _power_shift(
    coefficients: Sequence[DirectedInterval], positions: int
) -> tuple[DirectedInterval, ...]:
    if positions < 0:
        raise ValueError("negative polynomial shift")
    return tuple([_zero(coefficients[0].precision)] * positions) + tuple(
        coefficients
    )


def _power_range(
    coefficients: Sequence[DirectedInterval],
    lower: DirectedInterval,
    upper: DirectedInterval,
) -> DirectedInterval:
    """Bernstein range of a power polynomial on ``[lower, upper]``."""

    if lower.lower != lower.upper or upper.lower != upper.upper:
        raise ValueError("parameter shard endpoints must be points")
    if lower.lower >= upper.lower:
        raise ValueError("parameter shard is not positively oriented")
    affine = (lower, upper - lower)
    transformed: tuple[DirectedInterval, ...] = (_zero(lower.precision),)
    for coefficient in reversed(coefficients):
        transformed = _poly_multiply(transformed, affine)
        transformed = _poly_add_constant(transformed, coefficient)
    return _poly_bernstein_range(transformed)


def _parameter_shards(
    count: int = PARAMETER_SUBDIVISIONS,
) -> tuple[tuple[DirectedInterval, DirectedInterval], ...]:
    if count <= 0:
        raise ValueError("the parameter subdivision count must be positive")
    shards = []
    for index in range(count):
        lower = _fraction_interval(Fraction(-1) + Fraction(2 * index, count), PRECISION_BITS)
        upper = _fraction_interval(
            Fraction(-1) + Fraction(2 * (index + 1), count), PRECISION_BITS
        )
        shards.append((lower, upper))
    return tuple(shards)


def _cell_step(cell: CoefficientCell) -> DirectedInterval:
    return _node_interval(cell.right, PRECISION_BITS) - _node_interval(
        cell.left, PRECISION_BITS
    )


def _guide_value(
    guide: Sequence[gmpy2.mpfr], scaled_time: DirectedInterval
) -> DirectedInterval:
    coefficients = tuple(
        _mpfr_point(item, PRECISION_BITS) for item in guide
    )
    return _power_eval(coefficients, scaled_time)


def _coordinate_error(
    radius: gmpy2.mpfr, *, voltage: bool
) -> gmpy2.mpfr:
    voltage_coordinate, recovery_coordinate = _coordinate_error_factors()
    coordinate = voltage_coordinate if voltage else recovery_coordinate
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
        return coordinate * radius


@lru_cache(maxsize=1)
def _coordinate_error_factors() -> tuple[gmpy2.mpfr, gmpy2.mpfr]:
    return _coordinate_bounds(PRECISION_BITS)


def _coefficient_boxes_at_scaled_time(
    cell: CoefficientCell,
    scaled_time: DirectedInterval,
    *,
    voltage: bool,
) -> tuple[DirectedInterval, ...]:
    guides = cell.voltage if voltage else cell.recovery
    error = _coordinate_error(cell.maximum_radius, voltage=voltage)
    return tuple(
        _symmetric_enlargement(_guide_value(guide, scaled_time), error)
        for guide in guides
    )


def _coefficient_ranges_on_cell(
    cell: CoefficientCell, *, voltage: bool
) -> tuple[DirectedInterval, ...]:
    ranges = cell.voltage_ranges if voltage else cell.recovery_ranges
    error = _coordinate_error(cell.maximum_radius, voltage=voltage)
    return tuple(_symmetric_enlargement(item, error) for item in ranges)


def _parameter_polynomial_hull(
    coefficients: Sequence[DirectedInterval],
    *,
    shards: Sequence[tuple[DirectedInterval, DirectedInterval]] | None = None,
) -> DirectedInterval:
    selected = _parameter_shards() if shards is None else tuple(shards)
    return _hull(
        tuple(_power_range(coefficients, lower, upper) for lower, upper in selected)
    )


def _family_state_range_on_cell(
    coefficient_cell: CoefficientCell,
    remainder: RemainderPropagation,
    *,
    voltage: bool,
) -> DirectedInterval:
    coefficients = _coefficient_ranges_on_cell(
        coefficient_cell, voltage=voltage
    )
    nominal = _parameter_polynomial_hull(coefficients)
    remainder_cell = remainder.cells[
        _cell_key(coefficient_cell.left, coefficient_cell.right)
    ]
    error = _coordinate_error(remainder_cell.maximum_radius, voltage=voltage)
    return _symmetric_enlargement(nominal, error)


def _fast_field(
    voltage: DirectedInterval,
    recovery: DirectedInterval,
    delayed_four: DirectedInterval,
    delayed_five: DirectedInterval,
) -> DirectedInterval:
    precision = voltage.precision
    epsilon = _fraction_interval(EPSILON, precision)
    kappa_1 = _fraction_interval(KAPPA_1, precision)
    kappa_3 = _fraction_interval(KAPPA_3, precision)
    half = _point(1, precision) / 2
    third = _point(1, precision) / 3
    return (
        voltage
        - third * voltage**3
        - recovery
        + epsilon
        * kappa_1
        * (half * (delayed_four + delayed_five) - voltage)
        + epsilon
        * kappa_3
        * (
            half * ((delayed_four - 1) ** 3 + (delayed_five - 1) ** 3)
            - (voltage - 1) ** 3
        )
    )


def _slow_field(
    voltage: DirectedInterval, recovery: DirectedInterval
) -> DirectedInterval:
    return _fraction_interval(EPSILON, voltage.precision) * (
        voltage - recovery - _fraction_interval(UNFOLDING, voltage.precision)
    )


def _cell_field_range(
    propagation: CoefficientPropagation,
    remainder: RemainderPropagation,
    cell: CoefficientCell,
) -> tuple[DirectedInterval, DirectedInterval]:
    current_voltage = _family_state_range_on_cell(
        cell, remainder, voltage=True
    )
    current_recovery = _family_state_range_on_cell(
        cell, remainder, voltage=False
    )
    delayed = {}
    for delay in (4, 5):
        key = _cell_key(cell.left.shifted(delay), cell.right.shifted(delay))
        source = propagation.cells.get(key)
        if source is None:
            raise ArithmeticError("event-speed delayed source cell is absent")
        delayed[delay] = _family_state_range_on_cell(
            source, remainder, voltage=True
        )
    return (
        _fast_field(
            current_voltage,
            current_recovery,
            delayed[4],
            delayed[5],
        ),
        _slow_field(current_voltage, current_recovery),
    )


def _section_level(route_contract: Mapping[str, Any]) -> DirectedInterval:
    audit = _mapping(
        route_contract.get("explicit_voltage_section_audit"),
        "Route-C voltage section audit",
    )
    if audit.get("exact_phase_zero_section_formula") != (
        "h_C(phi)=phi_v(0)-V_true(0)"
    ):
        raise ValueError("the Route-C section formula changed")
    return DirectedInterval.from_bounds(
        str(audit.get("validated_orbit_section_voltage_lower")),
        str(audit.get("validated_orbit_section_voltage_upper")),
        PRECISION_BITS,
    )


def _event_gap_at_scaled_time(
    cell: CoefficientCell,
    remainder: RemainderPropagation,
    scaled_time: DirectedInterval,
    section_level: DirectedInterval,
) -> DirectedInterval:
    coefficients = _coefficient_boxes_at_scaled_time(
        cell, scaled_time, voltage=True
    )
    nominal = _parameter_polynomial_hull(coefficients)
    remainder_cell = remainder.cells[_cell_key(cell.left, cell.right)]
    error = _coordinate_error(remainder_cell.maximum_radius, voltage=True)
    return _symmetric_enlargement(nominal, error) - section_level


def _center_gap_at_scaled_time(
    cell: CoefficientCell,
    scaled_time: DirectedInterval,
    section_level: DirectedInterval,
) -> DirectedInterval:
    return _coefficient_boxes_at_scaled_time(
        cell, scaled_time, voltage=True
    )[0] - section_level


@dataclass(frozen=True)
class CenterEventBracket:
    scaled: DirectedInterval
    physical: DirectedInterval
    lower_gap: DirectedInterval
    upper_gap: DirectedInterval


def _center_event_bracket(
    cell: CoefficientCell, section_level: DirectedInterval
) -> CenterEventBracket:
    zero = _point(0, PRECISION_BITS)
    one = _point(1, PRECISION_BITS)
    lower = zero
    upper = one
    lower_gap = _center_gap_at_scaled_time(cell, zero, section_level)
    upper_gap = _center_gap_at_scaled_time(cell, one, section_level)
    if lower_gap.upper >= 0 or upper_gap.lower <= 0:
        raise ArithmeticError("the center event is not bracketed by the cell")
    requested_margin = _fraction_interval(
        CENTER_EVENT_SIGN_MARGIN, PRECISION_BITS
    ).upper

    # Locate the last time at which *every* admissible section level is still
    # above the pulse voltage.  An indeterminate midpoint moves the opposite
    # frontier instead of stopping the whole bisection.
    negative_left = zero
    negative_right = one
    for _ in range(220):
        with gmpy2.context(
            precision=PRECISION_BITS, round=gmpy2.RoundToNearest
        ):
            midpoint_value = (
                negative_left.lower + negative_right.upper
            ) / 2
        midpoint = _mpfr_point(midpoint_value, PRECISION_BITS)
        if midpoint.lower in (negative_left.lower, negative_right.lower):
            break
        gap = _center_gap_at_scaled_time(cell, midpoint, section_level)
        if gap.upper < -requested_margin:
            negative_left = midpoint
            lower = midpoint
            lower_gap = gap
        else:
            negative_right = midpoint

    # Dually locate the first time at which the pulse voltage is above every
    # admissible section level.
    positive_left = zero
    positive_right = one
    for _ in range(220):
        with gmpy2.context(
            precision=PRECISION_BITS, round=gmpy2.RoundToNearest
        ):
            midpoint_value = (
                positive_left.lower + positive_right.upper
            ) / 2
        midpoint = _mpfr_point(midpoint_value, PRECISION_BITS)
        if midpoint.lower in (positive_left.lower, positive_right.lower):
            break
        gap = _center_gap_at_scaled_time(cell, midpoint, section_level)
        if gap.lower > requested_margin:
            positive_right = midpoint
            upper = midpoint
            upper_gap = gap
        else:
            positive_left = midpoint

    scaled = DirectedInterval.from_bounds(lower.lower, upper.upper, PRECISION_BITS)
    left_time = _node_interval(cell.left, PRECISION_BITS)
    step = _cell_step(cell)
    lower_time = left_time + lower * step
    upper_time = left_time + upper * step
    physical = DirectedInterval.from_bounds(
        lower_time.lower, upper_time.upper, PRECISION_BITS
    )
    return CenterEventBracket(
        scaled=scaled,
        physical=physical,
        lower_gap=lower_gap,
        upper_gap=upper_gap,
    )


def _cube_coefficient(
    values: Sequence[Sequence[DirectedInterval]],
    parameter_order: int,
    time_order: int,
    *,
    shift_one: bool = False,
) -> DirectedInterval:
    precision = values[0][0].precision
    total = _zero(precision)

    def value(p_order: int, t_order: int) -> DirectedInterval:
        answer = values[p_order][t_order]
        if shift_one and p_order == 0 and t_order == 0:
            answer = answer - 1
        return answer

    for p_first in range(parameter_order + 1):
        for p_second in range(parameter_order - p_first + 1):
            p_third = parameter_order - p_first - p_second
            for t_first in range(time_order + 1):
                for t_second in range(time_order - t_first + 1):
                    t_third = time_order - t_first - t_second
                    total = total + (
                        value(p_first, t_first)
                        * value(p_second, t_second)
                        * value(p_third, t_third)
                    )
    return total


def _mixed_time_parameter_jet(
    propagation: CoefficientPropagation,
    cell: CoefficientCell,
    scaled_time: DirectedInterval,
    degree: int,
    *,
    impose_section: DirectedInterval | None = None,
    cache: dict[
        tuple[int, int, int, int, int],
        tuple[
            tuple[tuple[DirectedInterval, ...], ...],
            tuple[tuple[DirectedInterval, ...], ...],
        ],
    ] | None = None,
) -> tuple[
    tuple[tuple[DirectedInterval, ...], ...],
    tuple[tuple[DirectedInterval, ...], ...],
]:
    if degree < 0:
        raise ValueError("negative differential-algebra order")
    if cache is None:
        cache = {}
    key = (*_cell_key(cell.left, cell.right), degree)
    if impose_section is None and key in cache:
        return cache[key]
    voltage = [
        [item]
        for item in _coefficient_boxes_at_scaled_time(
            cell, scaled_time, voltage=True
        )
    ]
    recovery = [
        [item]
        for item in _coefficient_boxes_at_scaled_time(
            cell, scaled_time, voltage=False
        )
    ]
    if impose_section is not None:
        voltage[0][0] = _intersection(voltage[0][0], impose_section)
    if degree == 0:
        answer = (
            tuple(tuple(row) for row in voltage),
            tuple(tuple(row) for row in recovery),
        )
        if impose_section is None:
            cache[key] = answer
        return answer

    delayed = {}
    for delay in (4, 5):
        source_key = _cell_key(cell.left.shifted(delay), cell.right.shifted(delay))
        source = propagation.cells.get(source_key)
        if source is None:
            raise ArithmeticError("implicit-jet delayed source cell is absent")
        delayed[delay] = _mixed_time_parameter_jet(
            propagation,
            source,
            scaled_time,
            degree - 1,
            cache=cache,
        )[0]

    precision = PRECISION_BITS
    epsilon = _fraction_interval(EPSILON, precision)
    unfolding = _fraction_interval(UNFOLDING, precision)
    kappa_1 = _fraction_interval(KAPPA_1, precision)
    kappa_3 = _fraction_interval(KAPPA_3, precision)
    half = _point(1, precision) / 2
    third = _point(1, precision) / 3
    for time_order in range(degree):
        for parameter_order in range(5):
            current_cube = _cube_coefficient(
                voltage, parameter_order, time_order
            )
            current_shifted_cube = _cube_coefficient(
                voltage,
                parameter_order,
                time_order,
                shift_one=True,
            )
            delayed_four_cube = _cube_coefficient(
                delayed[4],
                parameter_order,
                time_order,
                shift_one=True,
            )
            delayed_five_cube = _cube_coefficient(
                delayed[5],
                parameter_order,
                time_order,
                shift_one=True,
            )
            fast = (
                voltage[parameter_order][time_order]
                - third * current_cube
                - recovery[parameter_order][time_order]
                + epsilon
                * kappa_1
                * (
                    half
                    * (
                        delayed[4][parameter_order][time_order]
                        + delayed[5][parameter_order][time_order]
                    )
                    - voltage[parameter_order][time_order]
                )
                + epsilon
                * kappa_3
                * (
                    half * (delayed_four_cube + delayed_five_cube)
                    - current_shifted_cube
                )
            )
            slow = epsilon * (
                voltage[parameter_order][time_order]
                - recovery[parameter_order][time_order]
                - (
                    unfolding
                    if parameter_order == 0 and time_order == 0
                    else 0
                )
            )
            divisor = _point(time_order + 1, precision)
            voltage[parameter_order].append(fast / divisor)
            recovery[parameter_order].append(slow / divisor)
    answer = (
        tuple(tuple(row) for row in voltage),
        tuple(tuple(row) for row in recovery),
    )
    if impose_section is None:
        cache[key] = answer
    return answer


def _series_multiply(
    left: Sequence[DirectedInterval],
    right: Sequence[DirectedInterval],
    degree: int,
) -> tuple[DirectedInterval, ...]:
    precision = left[0].precision
    result = [_zero(precision) for _ in range(degree + 1)]
    for left_order, left_value in enumerate(left):
        for right_order, right_value in enumerate(right):
            if left_order + right_order <= degree:
                result[left_order + right_order] = (
                    result[left_order + right_order] + left_value * right_value
                )
    return tuple(result)


def _series_power(
    value: Sequence[DirectedInterval], exponent: int, degree: int
) -> tuple[DirectedInterval, ...]:
    result = tuple([_point(1, value[0].precision)] + [_zero(value[0].precision)] * degree)
    for _ in range(exponent):
        result = _series_multiply(result, value, degree)
    return result


def _implicit_event_coefficients(
    voltage_jet: Sequence[Sequence[DirectedInterval]],
    degree: int = IMPLICIT_JET_ORDER,
) -> tuple[DirectedInterval, ...]:
    precision = voltage_jet[0][0].precision
    speed = voltage_jet[0][1]
    if speed.lower <= 0:
        raise ArithmeticError("the center event speed does not exclude zero")
    coefficients = [_zero(precision) for _ in range(degree + 1)]
    for order in range(1, degree + 1):
        shift = tuple(coefficients)
        remainder = _zero(precision)
        for parameter_order in range(min(4, order) + 1):
            for time_order in range(degree + 1):
                power = _series_power(shift, time_order, order)
                index = order - parameter_order
                if index < len(power):
                    remainder = remainder + (
                        voltage_jet[parameter_order][time_order] * power[index]
                    )
        coefficients[order] = -remainder / speed
    return tuple(coefficients)


def _compose_guide_with_scaled_time(
    cell: CoefficientCell,
    scaled_time_polynomial: Sequence[DirectedInterval],
    *,
    voltage: bool,
) -> tuple[DirectedInterval, ...]:
    guides = cell.voltage if voltage else cell.recovery
    precision = PRECISION_BITS
    total: tuple[DirectedInterval, ...] = (_zero(precision),)
    for parameter_order, guide in enumerate(guides):
        composed: tuple[DirectedInterval, ...] = (_zero(precision),)
        for coefficient in reversed(guide):
            composed = _poly_multiply(composed, scaled_time_polynomial)
            composed = _poly_add_constant(
                composed, _mpfr_point(coefficient, precision)
            )
        total = _poly_add(total, _power_shift(composed, parameter_order))
    return total


def _candidate_time_polynomial(
    center_time: DirectedInterval,
    event_coefficients: Sequence[DirectedInterval],
    offset: Fraction,
) -> tuple[DirectedInterval, ...]:
    if center_time.lower != center_time.upper:
        raise ValueError("the event-model centre must be a point")
    answer = [center_time + _fraction_interval(offset, PRECISION_BITS)]
    answer.extend(
        _mpfr_point(coefficient.midpoint_nearest(), PRECISION_BITS)
        for coefficient in event_coefficients[1:]
    )
    return tuple(answer)


def _scaled_time_polynomial_for_cell(
    cell: CoefficientCell,
    time_polynomial: Sequence[DirectedInterval],
) -> tuple[DirectedInterval, ...]:
    left = _node_interval(cell.left, PRECISION_BITS)
    step = _cell_step(cell)
    answer = [(time_polynomial[0] - left) / step]
    answer.extend(coefficient / step for coefficient in time_polynomial[1:])
    return tuple(answer)


def _correlated_voltage_on_event_graph(
    cell: CoefficientCell,
    remainder: RemainderPropagation,
    composed_voltage: Sequence[DirectedInterval],
    parameter_lower: DirectedInterval,
    parameter_upper: DirectedInterval,
) -> DirectedInterval:
    nominal = _power_range(
        composed_voltage, parameter_lower, parameter_upper
    )
    coefficient_error = _coordinate_error(cell.maximum_radius, voltage=True)
    remainder_error = _coordinate_error(
        remainder.cells[_cell_key(cell.left, cell.right)].maximum_radius,
        voltage=True,
    )
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
        total_error = 5 * coefficient_error + remainder_error
    return _symmetric_enlargement(nominal, total_error)


def _event_bracket_cells(
    propagation: CoefficientPropagation,
) -> tuple[CoefficientCell, ...]:
    answer = tuple(
        cell
        for cell in propagation.cells.values()
        if _node_compare(cell.left, EVENT_BRACKET_LEFT_NODE) >= 0
        and _node_compare(cell.right, EVENT_BRACKET_RIGHT_NODE) <= 0
    )
    if not answer:
        raise ArithmeticError("the declared event bracket has no cells")
    if answer[0].left != EVENT_BRACKET_LEFT_NODE:
        raise ArithmeticError("the event bracket left node is not a cell seam")
    if answer[-1].right != EVENT_BRACKET_RIGHT_NODE:
        raise ArithmeticError("the event bracket right node is not a cell seam")
    return answer


def _time_range_intersection_with_cell(
    time_range: DirectedInterval, cell: CoefficientCell
) -> DirectedInterval | None:
    left = _node_interval(cell.left, PRECISION_BITS)
    right = _node_interval(cell.right, PRECISION_BITS)
    lower = max(time_range.lower, left.lower)
    upper = min(time_range.upper, right.upper)
    if lower > upper:
        return None
    return DirectedInterval.from_bounds(lower, upper, PRECISION_BITS)


def _family_voltage_on_time_parameter_box(
    cell: CoefficientCell,
    remainder: RemainderPropagation,
    time_range: DirectedInterval,
    parameter_lower: DirectedInterval,
    parameter_upper: DirectedInterval,
) -> DirectedInterval:
    intersection = _time_range_intersection_with_cell(time_range, cell)
    if intersection is None:
        raise ValueError("the requested time box misses the guide cell")
    left = _node_interval(cell.left, PRECISION_BITS)
    scaled = (intersection - left) / _cell_step(cell)
    unit = DirectedInterval.from_bounds(0, 1, PRECISION_BITS)
    scaled = _intersection(scaled, unit)
    coefficient_error = _coordinate_error(cell.maximum_radius, voltage=True)
    coefficients = tuple(
        _symmetric_enlargement(_guide_value(guide, scaled), coefficient_error)
        for guide in cell.voltage
    )
    nominal = _power_range(coefficients, parameter_lower, parameter_upper)
    remainder_error = _coordinate_error(
        remainder.cells[_cell_key(cell.left, cell.right)].maximum_radius,
        voltage=True,
    )
    return _symmetric_enlargement(nominal, remainder_error)


def _event_graph_gap_on_parameter_box(
    event_cells: Sequence[CoefficientCell],
    remainder: RemainderPropagation,
    time_polynomial: Sequence[DirectedInterval],
    section_level: DirectedInterval,
    parameter_lower: DirectedInterval,
    parameter_upper: DirectedInterval,
    correlated_polynomials: Mapping[
        tuple[int, int, int, int], tuple[DirectedInterval, ...]
    ],
) -> tuple[DirectedInterval, DirectedInterval]:
    time_range = _power_range(
        time_polynomial, parameter_lower, parameter_upper
    )
    bracket_left = _node_interval(EVENT_BRACKET_LEFT_NODE, PRECISION_BITS)
    bracket_right = _node_interval(EVENT_BRACKET_RIGHT_NODE, PRECISION_BITS)
    if (
        time_range.lower < bracket_left.upper
        or time_range.upper > bracket_right.lower
    ):
        raise ArithmeticError("the event graph is not covered by the full bracket")

    # Most parameter shards lie strictly in one time cell.  There we compose
    # the time guide with the candidate event polynomial before taking any
    # range, preserving the decisive time--parameter cancellation.
    for cell in event_cells:
        left = _node_interval(cell.left, PRECISION_BITS)
        right = _node_interval(cell.right, PRECISION_BITS)
        if time_range.lower >= left.upper and time_range.upper <= right.lower:
            voltage = _correlated_voltage_on_event_graph(
                cell,
                remainder,
                correlated_polynomials[_cell_key(cell.left, cell.right)],
                parameter_lower,
                parameter_upper,
            )
            return voltage - section_level, time_range

    # A shard that actually straddles a grid seam is bisected below.  On that
    # vanishing family of shards it is safe to retain both adjacent guides.
    voltage_boxes = []
    for cell in event_cells:
        if _time_range_intersection_with_cell(time_range, cell) is not None:
            voltage_boxes.append(
                _family_voltage_on_time_parameter_box(
                    cell,
                    remainder,
                    time_range,
                    parameter_lower,
                    parameter_upper,
                )
            )
    if not voltage_boxes:
        raise ArithmeticError("the event graph left the declared bracket")
    return _hull(tuple(voltage_boxes)) - section_level, time_range


def _adaptive_event_graph_gap(
    event_cells: Sequence[CoefficientCell],
    remainder: RemainderPropagation,
    time_polynomial: Sequence[DirectedInterval],
    section_level: DirectedInterval,
    *,
    negative: bool,
) -> tuple[DirectedInterval, DirectedInterval, int, int]:
    correlated_polynomials = {}
    for cell in event_cells:
        scaled_time = _scaled_time_polynomial_for_cell(cell, time_polynomial)
        correlated_polynomials[_cell_key(cell.left, cell.right)] = (
            _compose_guide_with_scaled_time(cell, scaled_time, voltage=True)
        )
    stack = [
        (lower, upper, 0)
        for lower, upper in reversed(_parameter_shards(PARAMETER_SUBDIVISIONS))
    ]
    accepted_gaps = []
    accepted_times = []
    maximum_depth = 0
    while stack:
        lower, upper, depth = stack.pop()
        gap, time_range = _event_graph_gap_on_parameter_box(
            event_cells,
            remainder,
            time_polynomial,
            section_level,
            lower,
            upper,
            correlated_polynomials,
        )
        closes = gap.upper < 0 if negative else gap.lower > 0
        if closes:
            accepted_gaps.append(gap)
            accepted_times.append(time_range)
            maximum_depth = max(maximum_depth, depth)
            continue
        if depth >= 28:
            raise ArithmeticError("adaptive event-graph Bernstein sign did not close")
        with gmpy2.context(
            precision=PRECISION_BITS, round=gmpy2.RoundToNearest
        ):
            midpoint_value = (lower.lower + upper.upper) / 2
        midpoint = _mpfr_point(midpoint_value, PRECISION_BITS)
        stack.append((midpoint, upper, depth + 1))
        stack.append((lower, midpoint, depth + 1))
    return (
        _hull(tuple(accepted_gaps)),
        _hull(tuple(accepted_times)),
        len(accepted_gaps),
        maximum_depth,
    )


def _event_graph_gap_hull(
    event_cells: Sequence[CoefficientCell],
    remainder: RemainderPropagation,
    center_time: DirectedInterval,
    event_coefficients: Sequence[DirectedInterval],
    section_level: DirectedInterval,
    offset: Fraction,
) -> tuple[DirectedInterval, DirectedInterval, int, int]:
    time_polynomial = _candidate_time_polynomial(
        center_time, event_coefficients, offset
    )
    return _adaptive_event_graph_gap(
        event_cells,
        remainder,
        time_polynomial,
        section_level,
        negative=offset < 0,
    )


def _event_time_displacement_upper(
    event_coefficients: Sequence[DirectedInterval],
) -> gmpy2.mpfr:
    precision = PRECISION_BITS
    polynomial = [_zero(precision)]
    polynomial.extend(
        _mpfr_point(item.midpoint_nearest(), precision)
        for item in event_coefficients[1:]
    )
    nominal = _parameter_polynomial_hull(tuple(polynomial))
    remainder = _fraction_interval(EVENT_GRAPH_REMAINDER, precision)
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        return nominal.upper_abs() + remainder.upper


def _history_window_speed(
    propagation: CoefficientPropagation,
    remainder: RemainderPropagation,
    center_time: DirectedInterval,
    displacement: gmpy2.mpfr,
) -> tuple[gmpy2.mpfr, gmpy2.mpfr, int]:
    precision = PRECISION_BITS
    delay_five = _point(5, precision) * _point(5, precision).sqrt()
    radius = DirectedInterval.from_bounds(displacement, displacement, precision)
    window_left = center_time - delay_five - radius
    window_right = center_time + radius
    maximum_fast = gmpy2.mpfr(0)
    maximum_slow = gmpy2.mpfr(0)
    count = 0
    for cell in propagation.cells.values():
        left = _node_interval(cell.left, precision)
        right = _node_interval(cell.right, precision)
        if right.upper < window_left.lower or left.lower > window_right.upper:
            continue
        fast, slow = _cell_field_range(propagation, remainder, cell)
        maximum_fast = max(maximum_fast, fast.upper_abs())
        maximum_slow = max(maximum_slow, slow.upper_abs())
        count += 1
    if count == 0:
        raise ArithmeticError("the event-history speed window is empty")
    return maximum_fast, maximum_slow, count


def _interval_record(value: DirectedInterval) -> dict[str, str]:
    return {
        "lower": decimal_lower(value.lower),
        "upper": decimal_upper(value.upper),
    }


@lru_cache(maxsize=1)
def build_stage5c_certificate(repository: Path) -> dict[str, Any]:
    repository = Path(repository).resolve()
    stage5b = _load_bound_json(repository, STAGE5B_RELATIVE_PATH, STAGE5B_SHA256)
    route_parent = _load_bound_json(
        repository, ROUTE_C_CONTRACT_RELATIVE_PATH, ROUTE_C_CONTRACT_SHA256
    )
    adjoint_parent = _load_bound_json(
        repository, ROUTE_C_ADJOINT_RELATIVE_PATH, ROUTE_C_ADJOINT_SHA256
    )
    stage5b_certificate = _mapping(stage5b.get("certificate"), "Stage-5B certificate")
    stage5b_claims = _mapping(
        stage5b_certificate.get("claim_status"), "Stage-5B claims"
    )
    if stage5b_claims.get("fixed_time_wide_parameter_taylor_model_validated") is not True:
        raise ValueError("the Stage-5B fixed-time theorem is unavailable")
    route_contract = _mapping(route_parent.get("contract"), "Route-C contract")
    section_level = _section_level(route_contract)
    adjoint_artifact = _mapping(adjoint_parent.get("artifact"), "Route-C adjoint")
    adjoint_claims = _mapping(adjoint_artifact.get("claim_status"), "adjoint claims")
    if adjoint_claims.get("history_atom_density_measure_numeric_enclosed") is not True:
        raise ValueError("the Stage-4D Route-C history measure is unavailable")
    if adjoint_claims.get("directed_shared_action_on_physical_y_qq_available") is not False:
        raise ValueError("Stage-4D no longer records its physical-time open gate")

    propagation = build_coefficient_propagation()
    remainder = build_remainder_propagation()
    if not propagation.completed or not remainder.completed:
        raise ArithmeticError("the Stage-5B parent replay did not close")
    event_cell = propagation.cells.get(CENTER_EVENT_CELL_KEY)
    if event_cell is None:
        raise ArithmeticError("the declared Route-C event cell is absent")
    event_cells = _event_bracket_cells(propagation)

    zero = _point(0, PRECISION_BITS)
    one = _point(1, PRECISION_BITS)
    left_gap = _event_gap_at_scaled_time(
        event_cells[0], remainder, zero, section_level
    )
    right_gap = _event_gap_at_scaled_time(
        event_cells[-1], remainder, one, section_level
    )
    if left_gap.upper >= 0 or right_gap.lower <= 0:
        raise ArithmeticError("the wide family lacks strict event endpoint signs")
    event_speeds = tuple(
        _cell_field_range(propagation, remainder, cell)[0]
        for cell in event_cells
    )
    event_speed = _hull(event_speeds)
    if event_speed.lower <= 0:
        raise ArithmeticError("the event-cell voltage speed does not stay positive")

    center_bracket = _center_event_bracket(event_cell, section_level)
    mixed_voltage, _ = _mixed_time_parameter_jet(
        propagation,
        event_cell,
        center_bracket.scaled,
        IMPLICIT_JET_ORDER,
        impose_section=section_level,
    )
    event_coefficients = _implicit_event_coefficients(mixed_voltage)
    if any(not gmpy2.is_finite(item.upper) for item in event_coefficients):
        raise ArithmeticError("an implicit event coefficient is nonfinite")
    center_time = _mpfr_point(
        center_bracket.physical.midpoint_nearest(), PRECISION_BITS
    )
    (
        negative_graph_gap,
        negative_time_range,
        negative_graph_shards,
        negative_graph_depth,
    ) = _event_graph_gap_hull(
        event_cells,
        remainder,
        center_time,
        event_coefficients,
        section_level,
        -EVENT_GRAPH_REMAINDER,
    )
    (
        positive_graph_gap,
        positive_time_range,
        positive_graph_shards,
        positive_graph_depth,
    ) = _event_graph_gap_hull(
        event_cells,
        remainder,
        center_time,
        event_coefficients,
        section_level,
        EVENT_GRAPH_REMAINDER,
    )
    if negative_graph_gap.upper >= 0 or positive_graph_gap.lower <= 0:
        raise ArithmeticError("the fourth-order event graph tube did not close")

    displacement = _event_time_displacement_upper(event_coefficients)
    maximum_fast, maximum_slow, history_cells = _history_window_speed(
        propagation, remainder, center_time, displacement
    )
    voltage_remainder = _coordinate_error(remainder.maximum_radius, voltage=True)
    recovery_remainder = _coordinate_error(remainder.maximum_radius, voltage=False)
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
        voltage_history_radius = maximum_fast * displacement + voltage_remainder
        recovery_history_radius = maximum_slow * displacement + recovery_remainder
        history_radius = max(voltage_history_radius, recovery_history_radius)

    half_width = _fraction_interval(PARAMETER_HALF_WIDTH, PRECISION_BITS)
    jet_rows = []
    for order in range(1, IMPLICIT_JET_ORDER + 1):
        scaled = event_coefficients[order]
        physical = (
            _point(math.factorial(order), PRECISION_BITS)
            * scaled
            / (half_width**order)
        )
        jet_rows.append(
            {
                "order": order,
                "scaled_xi_power_coefficient": _interval_record(scaled),
                "physical_J_derivative_tau_k": _interval_record(physical),
                "conversion": f"tau_{order}={math.factorial(order)}*a_{order}/h^{order}",
            }
        )

    event_left = _node_interval(EVENT_BRACKET_LEFT_NODE, PRECISION_BITS)
    event_right = _node_interval(EVENT_BRACKET_RIGHT_NODE, PRECISION_BITS)
    certificate = {
        "schema_id": SCHEMA_ID,
        "model_id": MODEL_ID,
        "parameter_interval_exact": (
            f"[{PARAMETER_INTERVAL[0].numerator}/{PARAMETER_INTERVAL[0].denominator},"
            f"{PARAMETER_INTERVAL[1].numerator}/{PARAMETER_INTERVAL[1].denominator}]"
        ),
        "route_c_section": {
            "formula": "h_C(phi)=phi_v(0)-V_true(0)",
            "phase_zero_voltage_level": _interval_record(section_level),
        },
        "uniform_event_bracket": {
            "left_time_exact": "555*sqrt(5)/24",
            "right_time_exact": "1+546*sqrt(5)/24",
            "left_time": _interval_record(event_left),
            "right_time": _interval_record(event_right),
            "left_gap_for_all_J": _interval_record(left_gap),
            "right_gap_for_all_J": _interval_record(right_gap),
            "voltage_event_speed_on_whole_bracket": _interval_record(event_speed),
            "validated_cell_count": len(event_cells),
            "uniqueness_statement": (
                "For every J in the declared interval, the exact pulse solution "
                "has one and only one positive Route-C crossing in this bracket."
            ),
            "ordinal_scope": (
                "No count of earlier crossings is made, so the word third is "
                "not part of the proved conclusion."
            ),
        },
        "center_event": {
            "J0_exact": f"{J0.numerator}/{J0.denominator}",
            "requested_endpoint_gap_margin_exact": (
                f"{CENTER_EVENT_SIGN_MARGIN.numerator}/"
                f"{CENTER_EVENT_SIGN_MARGIN.denominator}"
            ),
            "scaled_time_bracket": _interval_record(center_bracket.scaled),
            "physical_time_bracket": _interval_record(center_bracket.physical),
            "lower_gap": _interval_record(center_bracket.lower_gap),
            "upper_gap": _interval_record(center_bracket.upper_gap),
            "event_speed_at_center_bracket": _interval_record(mixed_voltage[0][1]),
        },
        "implicit_event_time_jet": {
            "normalization": (
                "xi=(J-J0)/h and T(xi)=T0+sum_{k=1}^4 a_k xi^k+R_T(xi)"
            ),
            "rows": jet_rows,
            "recurrence": (
                "At each order m, compose the validated mixed factorial "
                "time/parameter series for g; isolate g_t*a_m and divide the "
                "remaining coefficient by the positive interval g_t."
            ),
        },
        "uniform_event_time_model": {
            "parameter_subdivision_count": PARAMETER_SUBDIVISIONS,
            "event_time_remainder_upper": (
                f"{EVENT_GRAPH_REMAINDER.numerator}/{EVENT_GRAPH_REMAINDER.denominator}"
            ),
            "negative_graph_gap": _interval_record(negative_graph_gap),
            "positive_graph_gap": _interval_record(positive_graph_gap),
            "negative_graph_time_range": _interval_record(negative_time_range),
            "positive_graph_time_range": _interval_record(positive_time_range),
            "negative_graph_accepted_shard_count": negative_graph_shards,
            "positive_graph_accepted_shard_count": positive_graph_shards,
            "negative_graph_maximum_refinement_depth": negative_graph_depth,
            "positive_graph_maximum_refinement_depth": positive_graph_depth,
            "maximum_time_displacement_from_center_upper": decimal_upper(displacement),
            "proof": (
                "The exact gap is negative on T_hat(xi)-10^-4 and positive "
                "on T_hat(xi)+10^-4 on every Bernstein xi shard; the uniform "
                "positive speed traps the unique event between these graphs."
            ),
        },
        "common_event_complete_history": {
            "phase_space": "Y=C([-5*sqrt(5),0],R)xR",
            "exact_definition": (
                "Y(xi)=(theta->v(T(xi)+theta,J0+h*xi), "
                "w(T(xi),J0+h*xi))"
            ),
            "continuous_reference_family": (
                "B_c(xi)=(theta->sum_{k=0}^4 b_{k,v}(T0+theta)xi^k, "
                "sum_{k=0}^4 b_{k,w}(T0)xi^k), where the exact coefficient "
                "solutions b_k are those enclosed by Stage-5B"
            ),
            "history_speed_cell_count": history_cells,
            "maximum_voltage_speed_upper": decimal_upper(maximum_fast),
            "maximum_recovery_speed_upper": decimal_upper(maximum_slow),
            "voltage_history_radius_upper": decimal_upper(voltage_history_radius),
            "recovery_current_radius_upper": decimal_upper(recovery_history_radius),
            "Y_max_radius_upper": decimal_upper(history_radius),
            "inclusion": (
                "||Y(xi)-B_c(xi)||_Y <= max(F_v*d_T+E_R5,v, "
                "F_w*d_T+E_R5,w), uniformly for xi in [-1,1]"
            ),
            "regularity_scope": (
                "This is a continuous complete-history tube.  A uniform "
                "J-derivative tube and a fourth-order Y-valued jet are not "
                "claimed, because the Stage-5B state remainder alone does not "
                "bound its J derivative and propagated smoothness fronts must "
                "be handled cellwise."
            ),
        },
        "stable_sheet_interface": {
            "stage4d_continuous_route_c_measure_available": True,
            "stage4d_physical_time_correlated_Yqq_action_available": False,
            "quantitative_inner_stable_graph_available": False,
            "event_output_supplied_to_next_stage": (
                "a unique transverse event, T0 and tau_1,...,tau_4 intervals, "
                "a uniform event-time graph tube, and a continuous Y-history tube"
            ),
            "stable_gap_endpoint_intervals": None,
            "stable_gap_derivative_interval": None,
            "interval_newton_image": None,
        },
        "theorem_statement": (
            "For every physical pulse amplitude in the exact Stage-5B wide "
            "interval, the pulse trajectory has exactly one positive crossing "
            "of the exact inner-orbit phase-zero voltage section inside the "
            "declared late event bracket.  Its centre-parameter event time has the "
            "displayed four implicit derivatives, and the whole event graph is "
            "enclosed by the displayed fourth-order polynomial plus the proved "
            "uniform remainder.  Pulling the voltage history and current "
            "recovery to that graph gives the displayed continuous Y-tube.  No "
            "stable-sheet intersection, onset root, side routing, or capture "
            "conclusion follows from this event certificate."
        ),
        "claim_status": {
            **{name: True for name in TRUE_FLAGS},
            **{name: False for name in FALSE_FLAGS},
        },
    }
    return certificate


def build_stage5c_result(repository: Path) -> dict[str, Any]:
    repository = Path(repository).resolve()
    certificate = build_stage5c_certificate(repository)
    return {
        "certificate": certificate,
        "manifest": {
            "schema_id": SCHEMA_ID,
            "result": RESULT_RELATIVE_PATH,
            "default_command": DEFAULT_COMMAND,
            "arithmetic_scope": ARITHMETIC_SCOPE,
            "parent_sha256": {
                STAGE5B_RELATIVE_PATH: STAGE5B_SHA256,
                ROUTE_C_CONTRACT_RELATIVE_PATH: ROUTE_C_CONTRACT_SHA256,
                ROUTE_C_ADJOINT_RELATIVE_PATH: ROUTE_C_ADJOINT_SHA256,
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


def validate_stage5c_result(
    payload: Mapping[str, Any],
    repository: Path,
    *,
    recompute: bool = False,
) -> None:
    if not isinstance(payload, Mapping) or set(payload) != {"certificate", "manifest"}:
        raise ValueError("Stage-5C result must contain certificate and manifest")
    certificate = _mapping(payload.get("certificate"), "Stage-5C certificate")
    manifest = _mapping(payload.get("manifest"), "Stage-5C manifest")
    if certificate.get("schema_id") != SCHEMA_ID or manifest.get("schema_id") != SCHEMA_ID:
        raise ValueError("Stage-5C schema changed")
    if manifest.get("result") != RESULT_RELATIVE_PATH:
        raise ValueError("Stage-5C result path changed")
    if manifest.get("default_command") != DEFAULT_COMMAND:
        raise ValueError("Stage-5C default command changed")
    if manifest.get("arithmetic_scope") != ARITHMETIC_SCOPE:
        raise ValueError("Stage-5C arithmetic scope changed")
    if manifest.get("certificate_sha256") != canonical_sha256(certificate):
        raise ValueError("Stage-5C certificate digest changed")
    claims = _mapping(certificate.get("claim_status"), "Stage-5C claims")
    if set(claims) != set(TRUE_FLAGS) | set(FALSE_FLAGS):
        raise ValueError("Stage-5C claim ledger changed")
    for name in TRUE_FLAGS:
        if claims.get(name) is not True:
            raise ValueError(f"proved Stage-5C claim was removed: {name}")
    for name in FALSE_FLAGS:
        if claims.get(name) is not False:
            raise ValueError(f"open Stage-5C claim was promoted: {name}")
    section = _mapping(certificate.get("route_c_section"), "Route-C section")
    if section.get("formula") != "h_C(phi)=phi_v(0)-V_true(0)":
        raise ValueError("the exact Route-C section formula changed")
    section_level = _mapping(
        section.get("phase_zero_voltage_level"), "phase-zero voltage level"
    )
    if section_level.get("lower") != (
        "0.905383843282120025506287674943450838327407828420353068999752401"
    ) or section_level.get("upper") != (
        "0.905403843282120025506287674943450838327407845269557922000191891"
    ):
        raise ValueError("the exact-orbit Route-C level enclosure changed")
    event = _mapping(
        certificate.get("uniform_event_bracket"), "uniform event bracket"
    )
    left_gap = _mapping(event.get("left_gap_for_all_J"), "left event gap")
    right_gap = _mapping(event.get("right_gap_for_all_J"), "right event gap")
    speed = _mapping(event.get("voltage_event_speed_on_whole_bracket"), "event speed")
    if DirectedInterval.from_decimal(str(left_gap.get("upper")), 96).upper >= 0:
        raise ValueError("the left event sign is not strict")
    if DirectedInterval.from_decimal(str(right_gap.get("lower")), 96).lower <= 0:
        raise ValueError("the right event sign is not strict")
    if DirectedInterval.from_decimal(str(speed.get("lower")), 96).lower <= 0:
        raise ValueError("the event speed does not exclude zero")
    if event.get("validated_cell_count") != 3:
        raise ValueError("the three-cell event bracket changed")
    center = _mapping(certificate.get("center_event"), "center event")
    if center.get("requested_endpoint_gap_margin_exact") != (
        "1/10000000000000000"
    ):
        raise ValueError("the center event sign margin changed")
    center_lower_gap = _mapping(center.get("lower_gap"), "center lower gap")
    center_upper_gap = _mapping(center.get("upper_gap"), "center upper gap")
    negative_margin = DirectedInterval.from_decimal("-9e-17", 96)
    positive_margin = DirectedInterval.from_decimal("9e-17", 96)
    if DirectedInterval.from_decimal(
        str(center_lower_gap.get("upper")), 96
    ).upper >= negative_margin.lower:
        raise ValueError("the center lower event sign margin was lost")
    if DirectedInterval.from_decimal(
        str(center_upper_gap.get("lower")), 96
    ).lower <= positive_margin.upper:
        raise ValueError("the center upper event sign margin was lost")
    center_time = _mapping(
        center.get("physical_time_bracket"), "center time bracket"
    )
    center_time_interval = DirectedInterval.from_bounds(
        str(center_time.get("lower")), str(center_time.get("upper")), 96
    )
    if center_time_interval.width_upper() >= DirectedInterval.from_decimal(
        "9e-5", 96
    ).lower:
        raise ValueError("the center event bracket is too wide")
    event_jet = _mapping(
        certificate.get("implicit_event_time_jet"), "implicit event jet"
    )
    rows = event_jet.get("rows")
    if not isinstance(rows, list) or [row.get("order") for row in rows] != [
        1,
        2,
        3,
        4,
    ]:
        raise ValueError("the four implicit event derivatives changed")
    for row in rows:
        scaled = _mapping(
            row.get("scaled_xi_power_coefficient"), "scaled event coefficient"
        )
        interval = DirectedInterval.from_bounds(
            str(scaled.get("lower")), str(scaled.get("upper")), 96
        )
        if interval.lower <= 0:
            raise ValueError("an implicit event coefficient lost positivity")
    model = _mapping(certificate.get("uniform_event_time_model"), "event model")
    if model.get("event_time_remainder_upper") != "1/10000":
        raise ValueError("the event-time remainder changed")
    if model.get("parameter_subdivision_count") != PARAMETER_SUBDIVISIONS:
        raise ValueError("the event graph base subdivision changed")
    negative = _mapping(model.get("negative_graph_gap"), "negative graph gap")
    positive = _mapping(model.get("positive_graph_gap"), "positive graph gap")
    if DirectedInterval.from_decimal(str(negative.get("upper")), 96).upper >= 0:
        raise ValueError("the lower event graph sign is not strict")
    if DirectedInterval.from_decimal(str(positive.get("lower")), 96).lower <= 0:
        raise ValueError("the upper event graph sign is not strict")
    history = _mapping(
        certificate.get("common_event_complete_history"), "event history"
    )
    history_radius = DirectedInterval.from_decimal(
        str(history.get("Y_max_radius_upper")), 96
    )
    if history_radius.lower < 0 or history_radius.upper >= (
        DirectedInterval.from_decimal("0.02", 96).lower
    ):
        raise ValueError("the common-event history tube exceeds its audit budget")
    interface = _mapping(certificate.get("stable_sheet_interface"), "stable interface")
    for name in (
        "stable_gap_endpoint_intervals",
        "stable_gap_derivative_interval",
        "interval_newton_image",
    ):
        if interface.get(name) is not None:
            raise ValueError("an open stable-sheet field was silently populated")

    repository = Path(repository).resolve()
    source_hashes = _mapping(manifest.get("source_sha256"), "source hashes")
    dependency_hashes = _mapping(
        manifest.get("dependency_source_sha256"), "dependency hashes"
    )
    if set(source_hashes) != set(SOURCE_MANIFEST):
        raise ValueError("Stage-5C source manifest changed")
    if set(dependency_hashes) != set(DEPENDENCY_SOURCE_MANIFEST):
        raise ValueError("Stage-5C dependency manifest changed")
    for relative in SOURCE_MANIFEST:
        if source_hashes.get(relative) != _sha256_path(repository / relative):
            raise ValueError(f"Stage-5C source changed: {relative}")
    for relative in DEPENDENCY_SOURCE_MANIFEST:
        if dependency_hashes.get(relative) != _sha256_path(repository / relative):
            raise ValueError(f"Stage-5C dependency changed: {relative}")
    expected_parents = {
        STAGE5B_RELATIVE_PATH: STAGE5B_SHA256,
        ROUTE_C_CONTRACT_RELATIVE_PATH: ROUTE_C_CONTRACT_SHA256,
        ROUTE_C_ADJOINT_RELATIVE_PATH: ROUTE_C_ADJOINT_SHA256,
    }
    if dict(_mapping(manifest.get("parent_sha256"), "parent hashes")) != expected_parents:
        raise ValueError("Stage-5C parent manifest changed")
    for relative, expected in expected_parents.items():
        if _sha256_path(repository / relative) != expected:
            raise ValueError(f"Stage-5C bound parent changed: {relative}")
    if recompute:
        build_stage5c_certificate.cache_clear()
        build_remainder_propagation.cache_clear()
        build_coefficient_propagation.cache_clear()
        rebuilt = build_stage5c_certificate(repository)
        if canonical_sha256(rebuilt) != canonical_sha256(certificate):
            raise ValueError("Stage-5C directed replay changed")


__all__ = [
    "FALSE_FLAGS",
    "RESULT_RELATIVE_PATH",
    "TRUE_FLAGS",
    "build_stage5c_certificate",
    "build_stage5c_result",
    "validate_stage5c_result",
]
