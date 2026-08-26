"""Directed Stage-5D event-aligned first-parameter derivative certificate.

Stage 5B proves a correlated fixed-time fourth-order parameter model

    z(t,J0+h*xi) = B(t,xi) + R(t,xi).

The state remainder bound cannot be differentiated.  This module instead
validates the first variational equation itself.  With

    W = partial_xi z = h*partial_J z,
    C = partial_xi B,
    E = W-C,

the error equation has the exact form

    E' = DF(z)E + (DF(z)-DF(B))C + partial_xi Tail_{>=5}(B).

All terms on the right are enclosed from the source-bound Stage-5B
coefficient and state-remainder cells.  The comparison is propagated on the
same exact delay grid, so no derivative of ``R`` and no finite sampling are
used.

Stage 5C supplies the unique transverse event graph.  The chain rule then
gives

    T_xi = -W_v(T,xi)/v_t(T,xi),
    D_J K = h^{-1}(W + z_t*T_xi),

on the complete event history.  The translation term is retained.  The
result is an enclosure of a continuous Y-valued derivative, not a stable
sheet, onset, interval-Newton, or routing certificate.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

import gmpy2

from canard_control.autonomous_leaky_recovery_bistable import (
    EPSILON,
    KAPPA_3,
    UNFOLDING,
)
from canard_control.directed_interval import (
    DirectedInterval,
    decimal_lower,
    decimal_upper,
)
from canard_control.leaky_pulse_parameter_jet_directed_enclosure import (
    DELAY_MULTIPLIERS,
    J0,
    PARAMETER_HALF_WIDTH,
    PARAMETER_INTERVAL,
    CoefficientCell,
    CoefficientPropagation,
    RemainderCell,
    RemainderPropagation,
    _coordinate_bounds,
    _interval_parameter_cube,
    _interval_parameter_shift_one,
    build_coefficient_propagation,
    build_remainder_propagation,
    canonical_sha256,
)
from canard_control.leaky_pulse_quiet_capture import (
    MAXIMUM_FIXED_POINT_ITERATIONS,
    PRECISION_BITS,
    TUBE_FLOOR,
    TUBE_INFLATION,
    ZERO_NODE,
    _Node,
    _cell_key,
    _fraction_interval,
    _gronwall_endpoint,
    _node_compare,
    _node_interval,
    _p_box_norm_upper,
    _point,
    _symmetric_enlargement,
)
from canard_control.leaky_pulse_route_c_event_stage5c import (
    EVENT_BRACKET_LEFT_NODE,
    EVENT_BRACKET_RIGHT_NODE,
    _cell_field_range,
    _cell_step,
    _coefficient_boxes_at_scaled_time,
    _event_bracket_cells,
    _hull,
    _intersection,
    _parameter_shards,
    _power_range,
    _time_range_intersection_with_cell,
)


SCHEMA_ID = "leaky-pulse-event-aligned-derivative-stage5d-v1"
MODEL_ID = "autonomous-leaky-recovery-physical-pulse"

SOURCE_RELATIVE_PATH = (
    "src/canard_control/leaky_pulse_event_aligned_derivative_stage5d.py"
)
GENERATOR_RELATIVE_PATH = (
    "experiments/leaky_pulse_event_aligned_derivative_stage5d.py"
)
RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_pulse_event_aligned_derivative_stage5d.json"
)
NOTE_RELATIVE_PATH = "docs/leaky-pulse-event-aligned-derivative-stage5d.md"
TEST_RELATIVE_PATH = (
    "tests/test_leaky_pulse_event_aligned_derivative_stage5d.py"
)

STAGE5B_RELATIVE_PATH = (
    "experiments/results/leaky_pulse_parameter_jet_directed_enclosure.json"
)
STAGE5B_SHA256 = "71276785fd803b663fc11de9489751ccd53dd8a408323a0bb140d0c9e7b7862b"
STAGE5C_RELATIVE_PATH = (
    "experiments/results/leaky_pulse_route_c_event_stage5c.json"
)
STAGE5C_SHA256 = "f1f198d68cb736bc9b5a48a0bff3eb5a93d39ee3f0b8f7cb6f7e07779483128d"
STAGE4D_RELATIVE_PATH = (
    "experiments/results/leaky_route_c_adjoint_stage4d.json"
)
STAGE4D_SHA256 = "af51bcfc20000b804134c1d8b9cacc303013676c440a89f2ecb52faf0042d568"

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
    "src/canard_control/leaky_pulse_route_c_event_stage5c.py",
)
DEFAULT_COMMAND = (
    "OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 "
    "PYTHONPATH=.venv/lib/python3.14/site-packages:src /usr/bin/python3 "
    "experiments/leaky_pulse_event_aligned_derivative_stage5d.py"
)
ARITHMETIC_SCOPE = (
    "192-bit outward MPFR on the exact Stage-5B two-origin 1152-cell delay "
    "grid; 64-shard Bernstein retention of the normalized pulse parameter; "
    "a cellwise P-logarithmic-norm enclosure of the exact first variational "
    "equation relative to partial_xi B; Stage-5C interval event-graph and "
    "positive-speed division; a continuous complete-history chain-rule "
    "tube including z_t*T_J; and a Stage-4D atom-plus-density action modulus "
    "bound; no finite-sampling, stable-sheet, onset, Newton, or routing claim"
)

SENSITIVITY_PARAMETER_SUBDIVISIONS = 64
EVENT_PARAMETER_SUBDIVISIONS = 128


TRUE_FLAGS = (
    "stage5b_and_stage5c_parent_bytes_source_bound",
    "stage4d_fixed_center_continuous_functional_source_bound",
    "state_remainder_not_differentiated",
    "scaled_first_variation_error_equation_derived_exactly",
    "scaled_first_variation_error_tube_closed_on_all_cells",
    "full_interval_fixed_time_first_J_variation_enclosed",
    "full_interval_event_time_first_J_derivative_enclosed",
    "event_time_J_derivative_strictly_positive_validated",
    "event_translation_term_retained_in_history_derivative",
    "continuous_event_aligned_complete_history_J_derivative_enclosed_in_Y",
    "section_current_voltage_J_derivative_is_exactly_zero",
    "event_current_recovery_J_derivative_strictly_negative_validated",
    "fixed_center_normalized_functional_action_modulus_enclosed",
    "finite_parameter_sampling_excluded_from_proof",
)

FALSE_FLAGS = (
    "fixed_center_functional_action_sign_validated",
    "fixed_center_functional_action_excludes_zero_validated",
    "common_event_complete_history_jet_through_order_four_validated",
    "inner_local_stable_graph_validated",
    "stable_coordinate_endpoint_signs_validated",
    "stable_gap_derivative_excludes_zero_validated",
    "interval_newton_strict_inclusion_validated",
    "unique_stable_sheet_pulse_parameter_Jc_validated",
    "unique_physical_pulse_onset_validated",
    "two_sided_basin_routing_validated",
    "outer_or_quiet_capture_from_both_sides_validated",
)


@dataclass(frozen=True)
class SensitivityErrorCell:
    left: _Node
    right: _Node
    endpoint_radius: gmpy2.mpfr
    maximum_radius: gmpy2.mpfr
    source_upper: gmpy2.mpfr
    tail_derivative_source_upper: gmpy2.mpfr
    linearization_mismatch_source_upper: gmpy2.mpfr
    logarithmic_norm_upper: gmpy2.mpfr
    delay_four_operator_upper: gmpy2.mpfr
    delay_five_operator_upper: gmpy2.mpfr
    closure_gap_lower: gmpy2.mpfr


@dataclass(frozen=True)
class SensitivityErrorPropagation:
    cells: Mapping[tuple[int, int, int, int], SensitivityErrorCell]
    completed: bool
    requested_cell_count: int
    closed_cell_count: int
    failure_cell_key: tuple[int, int, int, int] | None
    failure_reason: str | None
    maximum_radius: gmpy2.mpfr
    maximum_source: gmpy2.mpfr
    maximum_tail_derivative_source: gmpy2.mpfr
    maximum_linearization_mismatch_source: gmpy2.mpfr
    minimum_closure_gap: gmpy2.mpfr


def _sha256_path(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _mapping(value: Any, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{name} must be a mapping")
    return value


def _load_bound_json(repository: Path, relative: str, expected: str) -> Any:
    path = repository / relative
    if _sha256_path(path) != expected:
        raise ValueError(f"Stage-5D bound parent changed: {relative}")
    return json.loads(path.read_text(encoding="utf-8"))


def _interval_record(value: DirectedInterval) -> dict[str, str]:
    return {
        "lower": decimal_lower(value.lower),
        "upper": decimal_upper(value.upper),
    }


def _zero() -> DirectedInterval:
    return _point(0, PRECISION_BITS)


def _symmetric(radius: gmpy2.mpfr) -> DirectedInterval:
    return DirectedInterval.from_bounds(-radius, radius, PRECISION_BITS)


def _coefficient_boxes(
    cell: CoefficientCell, *, voltage: bool
) -> tuple[DirectedInterval, ...]:
    voltage_coordinate, recovery_coordinate = _coordinate_bounds(PRECISION_BITS)
    coordinate = voltage_coordinate if voltage else recovery_coordinate
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
        error = coordinate * cell.maximum_radius
    ranges = cell.voltage_ranges if voltage else cell.recovery_ranges
    return tuple(_symmetric_enlargement(item, error) for item in ranges)


def _parameter_derivative(
    coefficients: Sequence[DirectedInterval],
) -> tuple[DirectedInterval, ...]:
    if len(coefficients) < 2:
        return (_zero(),)
    return tuple(order * coefficients[order] for order in range(1, len(coefficients)))


def _range_on_shards(
    coefficients: Sequence[DirectedInterval],
    subdivisions: int = SENSITIVITY_PARAMETER_SUBDIVISIONS,
) -> DirectedInterval:
    return _hull(
        tuple(
            _power_range(coefficients, lower, upper)
            for lower, upper in _parameter_shards(subdivisions)
        )
    )


def _delayed_coefficient_cell(
    propagation: CoefficientPropagation,
    left: _Node,
    right: _Node,
    delay: int,
) -> CoefficientCell | None:
    source_left = left.shifted(delay)
    source_right = right.shifted(delay)
    if _node_compare(source_right, ZERO_NODE) <= 0:
        return None
    if _node_compare(source_left, ZERO_NODE) < 0:
        raise AssertionError("a sensitivity delay cell crossed the history seam")
    source = propagation.cells.get(_cell_key(source_left, source_right))
    if source is None:
        raise AssertionError("a sensitivity coefficient source is absent")
    return source


def _delayed_remainder_cell(
    propagation: RemainderPropagation,
    left: _Node,
    right: _Node,
    delay: int,
) -> RemainderCell | None:
    source_left = left.shifted(delay)
    source_right = right.shifted(delay)
    if _node_compare(source_right, ZERO_NODE) <= 0:
        return None
    if _node_compare(source_left, ZERO_NODE) < 0:
        raise AssertionError("a sensitivity remainder delay crossed the history seam")
    source = propagation.cells.get(_cell_key(source_left, source_right))
    if source is None:
        raise AssertionError("a sensitivity remainder source is absent")
    return source


def _delayed_sensitivity_radius(
    cells: Mapping[tuple[int, int, int, int], SensitivityErrorCell],
    left: _Node,
    right: _Node,
    delay: int,
) -> gmpy2.mpfr:
    source_left = left.shifted(delay)
    source_right = right.shifted(delay)
    if _node_compare(source_right, ZERO_NODE) <= 0:
        return gmpy2.mpfr(0, PRECISION_BITS)
    if _node_compare(source_left, ZERO_NODE) < 0:
        raise AssertionError("a sensitivity error delay crossed the history seam")
    source = cells.get(_cell_key(source_left, source_right))
    if source is None:
        raise AssertionError("a sensitivity error source is absent")
    return source.maximum_radius


def _quiet_voltage_coefficients() -> tuple[DirectedInterval, ...]:
    # Only the parameter derivative of this history is used.  Its b_0
    # interval is immaterial to C, while its delayed state range is supplied
    # by the Stage-5B remainder propagation.  Keep the exact alpha enclosure
    # through the coefficient parent when a pre-zero delay is encountered.
    from canard_control.leaky_pulse_quiet_capture import _alpha_interval

    return (_alpha_interval(PRECISION_BITS),) + tuple(_zero() for _ in range(4))


def _tail_derivative_polynomial(
    current: Sequence[DirectedInterval],
    delayed_four: Sequence[DirectedInterval],
    delayed_five: Sequence[DirectedInterval],
) -> tuple[DirectedInterval, ...]:
    """Return ``partial_xi Tail_{>=5}`` for the Stage-5B cubic residual."""

    count = 13
    epsilon = _fraction_interval(EPSILON, PRECISION_BITS)
    kappa_3 = _fraction_interval(KAPPA_3, PRECISION_BITS)
    third = _point(1, PRECISION_BITS) / 3
    half = _point(1, PRECISION_BITS) / 2
    current_cube = _interval_parameter_cube(current, count)
    shifted_current_cube = _interval_parameter_cube(
        _interval_parameter_shift_one(current, 5), count
    )
    delayed_four_cube = _interval_parameter_cube(
        _interval_parameter_shift_one(delayed_four, 5), count
    )
    delayed_five_cube = _interval_parameter_cube(
        _interval_parameter_shift_one(delayed_five, 5), count
    )
    tail = [_zero() for _ in range(count)]
    for order in range(5, count):
        tail[order] = (
            -third * current_cube[order]
            + epsilon
            * kappa_3
            * (
                half * (delayed_four_cube[order] + delayed_five_cube[order])
                - shifted_current_cube[order]
            )
        )
    return _parameter_derivative(tuple(tail))


def _cell_sensitivity_sources(
    coefficient_propagation: CoefficientPropagation,
    remainder_propagation: RemainderPropagation,
    coefficient_cell: CoefficientCell,
) -> tuple[gmpy2.mpfr, gmpy2.mpfr, gmpy2.mpfr]:
    """Bound the exact source in the scaled sensitivity-error equation."""

    precision = PRECISION_BITS
    epsilon = _fraction_interval(EPSILON, precision)
    kappa_3 = _fraction_interval(KAPPA_3, precision)
    current = _coefficient_boxes(coefficient_cell, voltage=True)
    delayed_coefficients: dict[int, tuple[DirectedInterval, ...]] = {}
    delayed_remainders: dict[int, gmpy2.mpfr] = {}
    for delay in DELAY_MULTIPLIERS:
        source = _delayed_coefficient_cell(
            coefficient_propagation,
            coefficient_cell.left,
            coefficient_cell.right,
            delay,
        )
        delayed_coefficients[delay] = (
            _quiet_voltage_coefficients()
            if source is None
            else _coefficient_boxes(source, voltage=True)
        )
        remainder_source = _delayed_remainder_cell(
            remainder_propagation,
            coefficient_cell.left,
            coefficient_cell.right,
            delay,
        )
        delayed_remainders[delay] = (
            gmpy2.mpfr(0, precision)
            if remainder_source is None
            else remainder_source.maximum_radius
        )

    tail_derivative = _tail_derivative_polynomial(
        current, delayed_coefficients[4], delayed_coefficients[5]
    )
    tail_upper = _range_on_shards(tail_derivative).upper_abs()

    current_remainder = remainder_propagation.cells[
        _cell_key(coefficient_cell.left, coefficient_cell.right)
    ].maximum_radius
    voltage_coordinate, _ = _coordinate_bounds(precision)
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        current_voltage_error = voltage_coordinate * current_remainder
        delayed_voltage_errors = {
            delay: voltage_coordinate * delayed_remainders[delay]
            for delay in DELAY_MULTIPLIERS
        }
    current_error = _symmetric(current_voltage_error)
    delayed_errors = {
        delay: _symmetric(delayed_voltage_errors[delay])
        for delay in DELAY_MULTIPLIERS
    }
    current_derivative = _parameter_derivative(current)
    delayed_derivatives = {
        delay: _parameter_derivative(delayed_coefficients[delay])
        for delay in DELAY_MULTIPLIERS
    }

    mismatch_upper = gmpy2.mpfr(0, precision)
    tail_range_upper = gmpy2.mpfr(0, precision)
    for lower, upper in _parameter_shards(SENSITIVITY_PARAMETER_SUBDIVISIONS):
        base = _power_range(current, lower, upper)
        sensitivity = _power_range(current_derivative, lower, upper)
        # a(B+r)-a(B), where
        # a(v)=1-v^2-eps*kappa_1-3*eps*kappa_3*(v-1)^2.
        current_difference = -(
            2 * base * current_error + current_error**2
        ) - 3 * epsilon * kappa_3 * (
            2 * (base - 1) * current_error + current_error**2
        )
        mismatch = current_difference * sensitivity
        for delay in DELAY_MULTIPLIERS:
            delayed_base = _power_range(
                delayed_coefficients[delay], lower, upper
            )
            delayed_sensitivity = _power_range(
                delayed_derivatives[delay], lower, upper
            )
            delayed_difference = (
                3
                * epsilon
                * kappa_3
                / 2
                * (
                    2
                    * (delayed_base - 1)
                    * delayed_errors[delay]
                    + delayed_errors[delay] ** 2
                )
            )
            mismatch = mismatch + delayed_difference * delayed_sensitivity
        mismatch_upper = max(mismatch_upper, mismatch.upper_abs())
        tail_range_upper = max(
            tail_range_upper,
            _power_range(tail_derivative, lower, upper).upper_abs(),
        )

    # Both sources enter only the fast coordinate of the two-dimensional
    # variational equation.
    tail_p = _p_box_norm_upper(tail_range_upper, gmpy2.mpfr(0), precision)
    mismatch_p = _p_box_norm_upper(mismatch_upper, gmpy2.mpfr(0), precision)
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        total = tail_p + mismatch_p
    return total, tail_p, mismatch_p


@lru_cache(maxsize=1)
def build_sensitivity_error_propagation() -> SensitivityErrorPropagation:
    coefficients = build_coefficient_propagation()
    remainder = build_remainder_propagation()
    if not coefficients.completed or not remainder.completed:
        return SensitivityErrorPropagation(
            cells={},
            completed=False,
            requested_cell_count=coefficients.requested_cell_count,
            closed_cell_count=0,
            failure_cell_key=coefficients.failure_cell_key,
            failure_reason="Stage-5B parent propagation is incomplete",
            maximum_radius=gmpy2.inf(),
            maximum_source=gmpy2.inf(),
            maximum_tail_derivative_source=gmpy2.inf(),
            maximum_linearization_mismatch_source=gmpy2.inf(),
            minimum_closure_gap=-gmpy2.inf(),
        )

    precision = PRECISION_BITS
    cells: dict[tuple[int, int, int, int], SensitivityErrorCell] = {}
    previous: SensitivityErrorCell | None = None
    failure_key = None
    failure_reason = None
    maximum_radius = gmpy2.mpfr(0, precision)
    maximum_source = gmpy2.mpfr(0, precision)
    maximum_tail = gmpy2.mpfr(0, precision)
    maximum_mismatch = gmpy2.mpfr(0, precision)
    minimum_gap = gmpy2.inf()

    for key, coefficient_cell in coefficients.cells.items():
        remainder_cell = remainder.cells[key]
        step = _node_interval(coefficient_cell.right, precision) - _node_interval(
            coefficient_cell.left, precision
        )
        source, tail_source, mismatch_source = _cell_sensitivity_sources(
            coefficients, remainder, coefficient_cell
        )
        start_radius = (
            gmpy2.mpfr(0, precision)
            if previous is None
            else previous.endpoint_radius
        )
        delay_radii = {
            delay: _delayed_sensitivity_radius(
                cells, coefficient_cell.left, coefficient_cell.right, delay
            )
            for delay in DELAY_MULTIPLIERS
        }
        with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
            forcing = (
                source
                + remainder_cell.delay_four_operator_upper * delay_radii[4]
                + remainder_cell.delay_five_operator_upper * delay_radii[5]
            )
            radius = (
                max(start_radius, gmpy2.mpfr(TUBE_FLOOR))
                * gmpy2.mpfr(TUBE_INFLATION)
                + gmpy2.mpfr(TUBE_FLOOR)
            )
        closed = False
        endpoint = gmpy2.inf()
        gap = -gmpy2.inf()
        for _ in range(MAXIMUM_FIXED_POINT_ITERATIONS):
            endpoint = _gronwall_endpoint(
                start_radius,
                forcing,
                remainder_cell.logarithmic_norm_upper,
                step.upper,
                precision,
            )
            if not gmpy2.is_finite(endpoint):
                failure_key = key
                failure_reason = "nonfinite_sensitivity_error_endpoint"
                break
            required = max(start_radius, endpoint)
            with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
                gap = radius - required
            if gap > 0:
                closed = True
                break
            with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
                radius = (
                    max(radius, required)
                    * gmpy2.mpfr(TUBE_INFLATION)
                    + gmpy2.mpfr(TUBE_FLOOR)
                )
        if failure_key is not None:
            break
        if not closed:
            failure_key = key
            failure_reason = "sensitivity_error_cell_did_not_close"
            break
        cell = SensitivityErrorCell(
            left=coefficient_cell.left,
            right=coefficient_cell.right,
            endpoint_radius=endpoint,
            maximum_radius=radius,
            source_upper=source,
            tail_derivative_source_upper=tail_source,
            linearization_mismatch_source_upper=mismatch_source,
            logarithmic_norm_upper=remainder_cell.logarithmic_norm_upper,
            delay_four_operator_upper=remainder_cell.delay_four_operator_upper,
            delay_five_operator_upper=remainder_cell.delay_five_operator_upper,
            closure_gap_lower=gap,
        )
        cells[key] = cell
        previous = cell
        maximum_radius = max(maximum_radius, radius)
        maximum_source = max(maximum_source, source)
        maximum_tail = max(maximum_tail, tail_source)
        maximum_mismatch = max(maximum_mismatch, mismatch_source)
        minimum_gap = min(minimum_gap, gap)

    return SensitivityErrorPropagation(
        cells=cells,
        completed=failure_key is None,
        requested_cell_count=coefficients.requested_cell_count,
        closed_cell_count=len(cells),
        failure_cell_key=failure_key,
        failure_reason=failure_reason,
        maximum_radius=maximum_radius,
        maximum_source=maximum_source,
        maximum_tail_derivative_source=maximum_tail,
        maximum_linearization_mismatch_source=maximum_mismatch,
        minimum_closure_gap=minimum_gap,
    )


def _parse_interval(record: Mapping[str, Any], name: str) -> DirectedInterval:
    lower = record.get("lower")
    upper = record.get("upper")
    if lower is None or upper is None:
        raise ValueError(f"{name} interval is incomplete")
    return DirectedInterval.from_bounds(str(lower), str(upper), PRECISION_BITS)


def _event_time_polynomial(
    stage5c_certificate: Mapping[str, Any],
) -> tuple[DirectedInterval, ...]:
    center = _mapping(stage5c_certificate.get("center_event"), "center event")
    center_time = _parse_interval(
        _mapping(center.get("physical_time_bracket"), "center event time"),
        "center event time",
    )
    model = _mapping(
        stage5c_certificate.get("uniform_event_time_model"), "event time model"
    )
    if model.get("event_time_remainder_upper") != "1/10000":
        raise ValueError("the Stage-5C event-time remainder changed")
    center_time = _symmetric_enlargement(
        center_time,
        _fraction_interval(Fraction(1, 10_000), PRECISION_BITS).upper,
    )
    jet = _mapping(
        stage5c_certificate.get("implicit_event_time_jet"), "event-time jet"
    )
    rows = jet.get("rows")
    if not isinstance(rows, list) or [row.get("order") for row in rows] != [1, 2, 3, 4]:
        raise ValueError("the Stage-5C event-time coefficients changed")
    coefficients = [center_time]
    coefficients.extend(
        _parse_interval(
            _mapping(row.get("scaled_xi_power_coefficient"), "event coefficient"),
            f"event coefficient {row.get('order')}",
        )
        for row in rows
    )
    return tuple(coefficients)


def _scaled_sensitivity_on_time_parameter_box(
    coefficient_cell: CoefficientCell,
    sensitivity_cell: SensitivityErrorCell,
    time_range: DirectedInterval,
    parameter_lower: DirectedInterval,
    parameter_upper: DirectedInterval,
    *,
    voltage: bool,
) -> DirectedInterval:
    intersection = _time_range_intersection_with_cell(time_range, coefficient_cell)
    if intersection is None:
        raise ValueError("the sensitivity time box misses its coefficient cell")
    left = _node_interval(coefficient_cell.left, PRECISION_BITS)
    scaled_time = (intersection - left) / _cell_step(coefficient_cell)
    scaled_time = _intersection(
        scaled_time, DirectedInterval.from_bounds(0, 1, PRECISION_BITS)
    )
    coefficients = _coefficient_boxes_at_scaled_time(
        coefficient_cell, scaled_time, voltage=voltage
    )
    nominal = _power_range(
        _parameter_derivative(coefficients), parameter_lower, parameter_upper
    )
    voltage_coordinate, recovery_coordinate = _coordinate_bounds(PRECISION_BITS)
    coordinate = voltage_coordinate if voltage else recovery_coordinate
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
        error = coordinate * sensitivity_cell.maximum_radius
    return _symmetric_enlargement(nominal, error)


def _state_on_time_parameter_box(
    coefficient_cell: CoefficientCell,
    remainder_cell: RemainderCell,
    time_range: DirectedInterval,
    parameter_lower: DirectedInterval,
    parameter_upper: DirectedInterval,
    *,
    voltage: bool,
) -> DirectedInterval:
    intersection = _time_range_intersection_with_cell(time_range, coefficient_cell)
    if intersection is None:
        raise ValueError("the state time box misses its coefficient cell")
    left = _node_interval(coefficient_cell.left, PRECISION_BITS)
    scaled_time = (intersection - left) / _cell_step(coefficient_cell)
    scaled_time = _intersection(
        scaled_time, DirectedInterval.from_bounds(0, 1, PRECISION_BITS)
    )
    coefficients = _coefficient_boxes_at_scaled_time(
        coefficient_cell, scaled_time, voltage=voltage
    )
    nominal = _power_range(coefficients, parameter_lower, parameter_upper)
    voltage_coordinate, recovery_coordinate = _coordinate_bounds(PRECISION_BITS)
    coordinate = voltage_coordinate if voltage else recovery_coordinate
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
        error = coordinate * remainder_cell.maximum_radius
    return _symmetric_enlargement(nominal, error)


def _event_graph_boxes(
    coefficients: CoefficientPropagation,
    remainder: RemainderPropagation,
    sensitivity: SensitivityErrorPropagation,
    event_time_polynomial: Sequence[DirectedInterval],
) -> tuple[DirectedInterval, DirectedInterval, DirectedInterval, DirectedInterval, int]:
    event_cells = _event_bracket_cells(coefficients)
    scaled_voltage = []
    scaled_recovery = []
    state_voltage = []
    state_recovery = []
    intersections = 0
    for lower, upper in _parameter_shards(EVENT_PARAMETER_SUBDIVISIONS):
        time_range = _power_range(event_time_polynomial, lower, upper)
        if (
            time_range.lower
            < _node_interval(EVENT_BRACKET_LEFT_NODE, PRECISION_BITS).lower
            or time_range.upper
            > _node_interval(EVENT_BRACKET_RIGHT_NODE, PRECISION_BITS).upper
        ):
            raise ArithmeticError("the Stage-5D event graph left the Stage-5C bracket")
        for cell in event_cells:
            if _time_range_intersection_with_cell(time_range, cell) is None:
                continue
            key = _cell_key(cell.left, cell.right)
            scaled_voltage.append(
                _scaled_sensitivity_on_time_parameter_box(
                    cell,
                    sensitivity.cells[key],
                    time_range,
                    lower,
                    upper,
                    voltage=True,
                )
            )
            scaled_recovery.append(
                _scaled_sensitivity_on_time_parameter_box(
                    cell,
                    sensitivity.cells[key],
                    time_range,
                    lower,
                    upper,
                    voltage=False,
                )
            )
            state_voltage.append(
                _state_on_time_parameter_box(
                    cell,
                    remainder.cells[key],
                    time_range,
                    lower,
                    upper,
                    voltage=True,
                )
            )
            state_recovery.append(
                _state_on_time_parameter_box(
                    cell,
                    remainder.cells[key],
                    time_range,
                    lower,
                    upper,
                    voltage=False,
                )
            )
            intersections += 1
    if not scaled_voltage:
        raise ArithmeticError("the Stage-5D event graph has no cell enclosure")
    return (
        _hull(tuple(scaled_voltage)),
        _hull(tuple(scaled_recovery)),
        _hull(tuple(state_voltage)),
        _hull(tuple(state_recovery)),
        intersections,
    )


def _full_cell_scaled_sensitivity_range(
    coefficient_cell: CoefficientCell,
    sensitivity_cell: SensitivityErrorCell,
    *,
    voltage: bool,
) -> DirectedInterval:
    nominal = _range_on_shards(
        _parameter_derivative(_coefficient_boxes(coefficient_cell, voltage=voltage))
    )
    voltage_coordinate, recovery_coordinate = _coordinate_bounds(PRECISION_BITS)
    coordinate = voltage_coordinate if voltage else recovery_coordinate
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
        error = coordinate * sensitivity_cell.maximum_radius
    return _symmetric_enlargement(nominal, error)


def _history_window_boxes(
    coefficients: CoefficientPropagation,
    remainder: RemainderPropagation,
    sensitivity: SensitivityErrorPropagation,
    event_time_range: DirectedInterval,
) -> tuple[DirectedInterval, DirectedInterval, DirectedInterval, DirectedInterval, int]:
    delay_five = _point(5, PRECISION_BITS) * _point(5, PRECISION_BITS).sqrt()
    window_left = event_time_range - delay_five
    window_right = event_time_range
    scaled_voltage = []
    scaled_recovery = []
    fast = []
    slow = []
    for cell in coefficients.cells.values():
        left = _node_interval(cell.left, PRECISION_BITS)
        right = _node_interval(cell.right, PRECISION_BITS)
        if right.upper < window_left.lower or left.lower > window_right.upper:
            continue
        key = _cell_key(cell.left, cell.right)
        scaled_voltage.append(
            _full_cell_scaled_sensitivity_range(
                cell, sensitivity.cells[key], voltage=True
            )
        )
        scaled_recovery.append(
            _full_cell_scaled_sensitivity_range(
                cell, sensitivity.cells[key], voltage=False
            )
        )
        fast_cell, slow_cell = _cell_field_range(coefficients, remainder, cell)
        fast.append(fast_cell)
        slow.append(slow_cell)
    if not scaled_voltage:
        raise ArithmeticError("the Stage-5D complete-history window is empty")
    return (
        _hull(tuple(scaled_voltage)),
        _hull(tuple(scaled_recovery)),
        _hull(tuple(fast)),
        _hull(tuple(slow)),
        len(scaled_voltage),
    )


@lru_cache(maxsize=1)
def build_stage5d_certificate(repository: Path) -> dict[str, Any]:
    repository = Path(repository).resolve()
    stage5b = _load_bound_json(repository, STAGE5B_RELATIVE_PATH, STAGE5B_SHA256)
    stage5c = _load_bound_json(repository, STAGE5C_RELATIVE_PATH, STAGE5C_SHA256)
    stage4d = _load_bound_json(repository, STAGE4D_RELATIVE_PATH, STAGE4D_SHA256)
    stage5b_certificate = _mapping(stage5b.get("certificate"), "Stage-5B certificate")
    stage5c_certificate = _mapping(stage5c.get("certificate"), "Stage-5C certificate")
    stage4d_artifact = _mapping(stage4d.get("artifact"), "Stage-4D artifact")
    if stage5b_certificate.get("claim_status", {}).get(
        "fixed_time_wide_parameter_taylor_model_validated"
    ) is not True:
        raise ValueError("the Stage-5B fixed-time family is unavailable")
    if stage5c_certificate.get("claim_status", {}).get(
        "one_and_only_one_route_c_event_in_declared_bracket_for_every_J_validated"
    ) is not True:
        raise ValueError("the Stage-5C event family is unavailable")
    if stage4d_artifact.get("claim_status", {}).get(
        "history_atom_density_measure_numeric_enclosed"
    ) is not True:
        raise ValueError("the Stage-4D continuous functional is unavailable")

    coefficients = build_coefficient_propagation()
    remainder = build_remainder_propagation()
    sensitivity = build_sensitivity_error_propagation()
    if not coefficients.completed or not remainder.completed:
        raise ArithmeticError("the Stage-5B parent replay did not close")
    if not sensitivity.completed or sensitivity.closed_cell_count != 1152:
        raise ArithmeticError(
            f"the Stage-5D sensitivity error did not close: "
            f"{sensitivity.failure_cell_key} {sensitivity.failure_reason}"
        )

    event_time_polynomial = _event_time_polynomial(stage5c_certificate)
    event_time_range = _power_range(
        event_time_polynomial,
        DirectedInterval.from_decimal(-1, PRECISION_BITS),
        DirectedInterval.from_decimal(1, PRECISION_BITS),
    )
    (
        event_scaled_voltage,
        event_scaled_recovery,
        event_state_voltage,
        event_state_recovery,
        event_box_count,
    ) = _event_graph_boxes(
        coefficients, remainder, sensitivity, event_time_polynomial
    )

    uniform_event = _mapping(
        stage5c_certificate.get("uniform_event_bracket"), "uniform event"
    )
    event_speed = _parse_interval(
        _mapping(
            uniform_event.get("voltage_event_speed_on_whole_bracket"),
            "event speed",
        ),
        "event speed",
    )
    if event_speed.lower <= 0:
        raise ArithmeticError("the event speed does not exclude zero")
    event_time_xi_derivative = -event_scaled_voltage / event_speed
    half_width = _fraction_interval(PARAMETER_HALF_WIDTH, PRECISION_BITS)
    event_time_J_derivative = event_time_xi_derivative / half_width
    if event_time_J_derivative.lower <= 0:
        raise ArithmeticError("the event-time J derivative lost strict positivity")

    section = _mapping(stage5c_certificate.get("route_c_section"), "Route-C section")
    section_level = _parse_interval(
        _mapping(section.get("phase_zero_voltage_level"), "section level"),
        "section level",
    )
    epsilon = _fraction_interval(EPSILON, PRECISION_BITS)
    unfolding = _fraction_interval(UNFOLDING, PRECISION_BITS)
    event_slow_field = epsilon * (
        section_level - event_state_recovery - unfolding
    )
    event_recovery_xi_derivative = (
        event_scaled_recovery
        + event_slow_field * event_time_xi_derivative
    )
    event_recovery_J_derivative = event_recovery_xi_derivative / half_width
    if event_recovery_J_derivative.upper >= 0:
        raise ArithmeticError(
            "the event-aligned recovery J derivative lost strict negativity"
        )
    current_voltage_chain_box = (
        event_scaled_voltage + event_speed * event_time_xi_derivative
    )
    if not current_voltage_chain_box.contains_zero():
        raise ArithmeticError("the section chain-rule box lost the exact zero")

    (
        history_scaled_voltage,
        history_scaled_recovery,
        history_fast_field,
        history_slow_field,
        history_cell_count,
    ) = _history_window_boxes(
        coefficients, remainder, sensitivity, event_time_range
    )
    history_voltage_fixed_J = history_scaled_voltage / half_width
    history_recovery_fixed_J = history_scaled_recovery / half_width
    history_voltage_translation_J = (
        history_fast_field * event_time_xi_derivative / half_width
    )
    history_recovery_translation_J = (
        history_slow_field * event_time_xi_derivative / half_width
    )
    history_voltage_J_derivative = (
        history_voltage_fixed_J + history_voltage_translation_J
    )
    history_recovery_J_derivative = (
        history_recovery_fixed_J + history_recovery_translation_J
    )
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
        history_voltage_sup = history_voltage_J_derivative.upper_abs()
        event_recovery_abs = event_recovery_J_derivative.upper_abs()
        y_norm = max(history_voltage_sup, event_recovery_abs)

    measure = _mapping(
        stage4d_artifact.get("continuous_history_measure_enclosure"),
        "Stage-4D continuous measure",
    )
    normalization = _mapping(
        stage4d_artifact.get("grushin_border_normalization"),
        "Stage-4D normalization",
    )
    density_tv = DirectedInterval.from_decimal(
        str(measure.get("voltage_history_density_total_variation_upper")),
        PRECISION_BITS,
    )
    recovery_atom = DirectedInterval.from_decimal(
        str(measure.get("current_recovery_atom_modulus_upper")),
        PRECISION_BITS,
    )
    raw_measure_norm = DirectedInterval.from_decimal(
        str(measure.get("unnormalized_history_measure_norm_upper")),
        PRECISION_BITS,
    )
    normalized_measure_norm = DirectedInterval.from_decimal(
        str(measure.get("normalized_history_measure_norm_upper")),
        PRECISION_BITS,
    )
    f_q_lower = DirectedInterval.from_decimal(
        str(normalization.get("f_of_q_modulus_lower")), PRECISION_BITS
    )
    if f_q_lower.lower <= 0:
        raise ArithmeticError("the Stage-4D functional normalization vanished")
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
        raw_action_upper = (
            density_tv.upper * history_voltage_sup
            + recovery_atom.upper * event_recovery_abs
        )
        normalized_action_upper = raw_action_upper / f_q_lower.lower
        fallback_action_upper = normalized_measure_norm.upper * y_norm
    if normalized_action_upper > fallback_action_upper:
        raise ArithmeticError("the endpoint-zero action structure did not improve the norm bound")

    voltage_coordinate, recovery_coordinate = _coordinate_bounds(PRECISION_BITS)
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
        maximum_voltage_scaled_error = voltage_coordinate * sensitivity.maximum_radius
        maximum_recovery_scaled_error = recovery_coordinate * sensitivity.maximum_radius
        maximum_voltage_J_error = maximum_voltage_scaled_error / half_width.lower
        maximum_recovery_J_error = maximum_recovery_scaled_error / half_width.lower

    certificate = {
        "schema_id": SCHEMA_ID,
        "model_id": MODEL_ID,
        "parameter_scaling": {
            "center_J0_exact": f"{J0.numerator}/{J0.denominator}",
            "half_width_h_exact": (
                f"{PARAMETER_HALF_WIDTH.numerator}/{PARAMETER_HALF_WIDTH.denominator}"
            ),
            "interval_exact": (
                f"[{PARAMETER_INTERVAL[0].numerator}/{PARAMETER_INTERVAL[0].denominator},"
                f"{PARAMETER_INTERVAL[1].numerator}/{PARAMETER_INTERVAL[1].denominator}]"
            ),
            "normalized_parameter": "xi=(J-J0)/h in [-1,1]",
            "scaled_variation": "W=partial_xi z=h*partial_J z",
        },
        "fixed_time_first_variation": {
            "comparison": "C=partial_xi B=sum_{k=1}^4 k*b_k*xi^(k-1), E=W-C",
            "exact_error_equation": (
                "E'=DF(z)E+(DF(z)-DF(B))C+partial_xi Tail_{>=5}(B)"
            ),
            "state_remainder_derivative_used": False,
            "parameter_subdivision_count": SENSITIVITY_PARAMETER_SUBDIVISIONS,
            "closed_cell_count": sensitivity.closed_cell_count,
            "all_cells_closed": sensitivity.completed,
            "maximum_scaled_P_error_radius_upper": decimal_upper(
                sensitivity.maximum_radius
            ),
            "maximum_scaled_voltage_error_upper": decimal_upper(
                maximum_voltage_scaled_error
            ),
            "maximum_scaled_recovery_error_upper": decimal_upper(
                maximum_recovery_scaled_error
            ),
            "maximum_physical_J_voltage_error_upper": decimal_upper(
                maximum_voltage_J_error
            ),
            "maximum_physical_J_recovery_error_upper": decimal_upper(
                maximum_recovery_J_error
            ),
            "maximum_total_source_upper": decimal_upper(sensitivity.maximum_source),
            "maximum_tail_derivative_source_upper": decimal_upper(
                sensitivity.maximum_tail_derivative_source
            ),
            "maximum_linearization_mismatch_source_upper": decimal_upper(
                sensitivity.maximum_linearization_mismatch_source
            ),
            "minimum_cell_closure_gap_lower": decimal_lower(
                sensitivity.minimum_closure_gap
            ),
            "differentiability_reason": (
                "The RFDE vector field is polynomial in the current and delayed "
                "states and affine in J.  The exact quiet history is J-independent; "
                "the pulse-release seam is an exact grid boundary.  Standard "
                "piecewise RFDE parameter differentiation therefore gives W, and "
                "the displayed directed comparison encloses it continuously."
            ),
        },
        "event_time_first_derivative": {
            "event_graph_parameter_subdivision_count": EVENT_PARAMETER_SUBDIVISIONS,
            "event_graph_cell_intersection_count": event_box_count,
            "event_time_range": _interval_record(event_time_range),
            "event_scaled_voltage_variation_Wv": _interval_record(
                event_scaled_voltage
            ),
            "uniform_positive_voltage_speed": _interval_record(event_speed),
            "identity": "T_xi=-W_v(T(xi),xi)/v_t(T(xi),xi)",
            "T_xi_interval": _interval_record(event_time_xi_derivative),
            "T_J_interval": _interval_record(event_time_J_derivative),
            "strict_monotonicity": (
                "T_J>0 on the whole interval: increasing the physical pulse "
                "amplitude strictly delays the selected Route-C event"
            ),
        },
        "continuous_Y_derivative": {
            "phase_space": "Y=C([-5*sqrt(5),0],R)xR",
            "exact_history": (
                "K(J)=(theta->v(T(J)+theta,J),w(T(J),J))"
            ),
            "exact_chain_rule": (
                "D_J K=(partial_J z+z_t*T_J) on the voltage history and "
                "current recovery coordinate"
            ),
            "history_cell_count": history_cell_count,
            "fixed_time_voltage_partial_J_interval": _interval_record(
                history_voltage_fixed_J
            ),
            "voltage_translation_z_t_times_T_J_interval": _interval_record(
                history_voltage_translation_J
            ),
            "event_aligned_voltage_history_D_J_interval": _interval_record(
                history_voltage_J_derivative
            ),
            "fixed_time_recovery_partial_J_interval": _interval_record(
                history_recovery_fixed_J
            ),
            "recovery_translation_z_t_times_T_J_interval": _interval_record(
                history_recovery_translation_J
            ),
            "event_aligned_recovery_history_D_J_interval": _interval_record(
                history_recovery_J_derivative
            ),
            "event_current_recovery_D_J_interval": _interval_record(
                event_recovery_J_derivative
            ),
            "event_current_recovery_monotonicity": (
                "D_J K_w<0 on the whole interval after event alignment"
            ),
            "event_current_voltage_D_J_exact": "0",
            "section_chain_rule_outer_box": _interval_record(
                current_voltage_chain_box / half_width
            ),
            "Y_norm_upper": decimal_upper(y_norm),
            "continuity_statement": (
                "For every J in the closed pulse interval, D_J K(J) exists in Y; "
                "the voltage-history derivative is continuous in theta.  Every "
                "value of that function and the current recovery derivative lie "
                "in the displayed directed intervals."
            ),
        },
        "fixed_center_route_c_functional_action": {
            "functional": (
                "the fixed Stage-4D Route-C atom-plus-density functional, "
                "normalized by its nonzero action on q"
            ),
            "voltage_current_atom_contribution": (
                "exactly zero because D_J K_v(0)=0 on the fixed section"
            ),
            "voltage_density_total_variation_upper": decimal_upper(density_tv.upper),
            "current_recovery_atom_modulus_upper": decimal_upper(recovery_atom.upper),
            "raw_measure_norm_upper": decimal_upper(raw_measure_norm.upper),
            "normalization_f_of_q_modulus_lower": decimal_lower(f_q_lower.lower),
            "raw_action_modulus_upper": decimal_upper(raw_action_upper),
            "normalized_action_modulus_upper": decimal_upper(
                normalized_action_upper
            ),
            "global_operator_norm_fallback_upper": decimal_upper(
                fallback_action_upper
            ),
            "oriented_interval": None,
            "sign_scope": (
                "Stage 4D certifies atom and density moduli and total variation, "
                "not a common oriented signed coefficient enclosure suitable for "
                "a sign proof on this pulse family.  The rigorous output here is "
                "therefore a modulus disk containing zero, not a stable-gap slope."
            ),
        },
        "stable_gap_interface": {
            "event_history_derivative_input_available": True,
            "fixed_center_functional_action_modulus_available": True,
            "oriented_functional_action_sign_available": False,
            "quantitative_inner_stable_graph_available": False,
            "stable_gap_endpoint_intervals": None,
            "stable_gap_derivative_interval": None,
            "interval_newton_image": None,
            "pulse_parameter_Jc": None,
        },
        "theorem_statement": (
            "For every J in the exact Stage-5B interval, the event-aligned "
            "physical-pulse history K(J) at the unique Stage-5C Route-C event is "
            "continuously differentiable as a Y-valued map.  Its derivative is "
            "enclosed by the displayed fixed-time and translation-term intervals. "
            "The fixed Stage-4D normalized Route-C functional has the displayed "
            "action-modulus bound on D_J K.  No action sign, stable-sheet "
            "intersection, onset root, interval-Newton, side routing, or capture "
            "conclusion follows."
        ),
        "claim_status": {
            **{name: True for name in TRUE_FLAGS},
            **{name: False for name in FALSE_FLAGS},
        },
    }
    return certificate


def build_stage5d_result(repository: Path) -> dict[str, Any]:
    repository = Path(repository).resolve()
    certificate = build_stage5d_certificate(repository)
    return {
        "certificate": certificate,
        "manifest": {
            "schema_id": SCHEMA_ID,
            "result": RESULT_RELATIVE_PATH,
            "default_command": DEFAULT_COMMAND,
            "arithmetic_scope": ARITHMETIC_SCOPE,
            "parent_sha256": {
                STAGE5B_RELATIVE_PATH: STAGE5B_SHA256,
                STAGE5C_RELATIVE_PATH: STAGE5C_SHA256,
                STAGE4D_RELATIVE_PATH: STAGE4D_SHA256,
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


def validate_stage5d_result(
    payload: Mapping[str, Any],
    repository: Path,
    *,
    recompute: bool = False,
) -> None:
    if not isinstance(payload, Mapping) or set(payload) != {"certificate", "manifest"}:
        raise ValueError("Stage-5D result must contain certificate and manifest")
    certificate = _mapping(payload.get("certificate"), "Stage-5D certificate")
    manifest = _mapping(payload.get("manifest"), "Stage-5D manifest")
    if certificate.get("schema_id") != SCHEMA_ID or manifest.get("schema_id") != SCHEMA_ID:
        raise ValueError("Stage-5D schema changed")
    if manifest.get("result") != RESULT_RELATIVE_PATH:
        raise ValueError("Stage-5D result path changed")
    if manifest.get("default_command") != DEFAULT_COMMAND:
        raise ValueError("Stage-5D default command changed")
    if manifest.get("arithmetic_scope") != ARITHMETIC_SCOPE:
        raise ValueError("Stage-5D arithmetic scope changed")
    if manifest.get("certificate_sha256") != canonical_sha256(certificate):
        raise ValueError("Stage-5D certificate digest changed")

    claims = _mapping(certificate.get("claim_status"), "Stage-5D claims")
    if set(claims) != set(TRUE_FLAGS) | set(FALSE_FLAGS):
        raise ValueError("Stage-5D claim ledger changed")
    for name in TRUE_FLAGS:
        if claims.get(name) is not True:
            raise ValueError(f"proved Stage-5D claim was removed: {name}")
    for name in FALSE_FLAGS:
        if claims.get(name) is not False:
            raise ValueError(f"open Stage-5D claim was promoted: {name}")

    fixed = _mapping(
        certificate.get("fixed_time_first_variation"), "fixed-time variation"
    )
    if fixed.get("state_remainder_derivative_used") is not False:
        raise ValueError("the Stage-5B state remainder was illicitly differentiated")
    if fixed.get("all_cells_closed") is not True or fixed.get("closed_cell_count") != 1152:
        raise ValueError("the Stage-5D cell closure changed")
    if DirectedInterval.from_decimal(
        str(fixed.get("minimum_cell_closure_gap_lower")), 96
    ).lower <= 0:
        raise ValueError("the Stage-5D closure gap is not positive")
    if DirectedInterval.from_decimal(
        str(fixed.get("maximum_scaled_P_error_radius_upper")), 96
    ).lower < 0:
        raise ValueError("the Stage-5D sensitivity radius is negative")

    event = _mapping(
        certificate.get("event_time_first_derivative"), "event derivative"
    )
    speed = _parse_interval(
        _mapping(event.get("uniform_positive_voltage_speed"), "event speed"),
        "event speed",
    )
    if speed.lower <= 0:
        raise ValueError("the Stage-5D event speed does not exclude zero")
    for name in ("T_xi_interval", "T_J_interval"):
        interval = _parse_interval(_mapping(event.get(name), name), name)
        if not gmpy2.is_finite(interval.lower) or not gmpy2.is_finite(interval.upper):
            raise ValueError(f"the Stage-5D {name} is nonfinite")
    if _parse_interval(
        _mapping(event.get("T_J_interval"), "T_J interval"), "T_J interval"
    ).lower <= 0:
        raise ValueError("the Stage-5D event-time monotonicity was lost")

    history = _mapping(certificate.get("continuous_Y_derivative"), "Y derivative")
    if history.get("phase_space") != "Y=C([-5*sqrt(5),0],R)xR":
        raise ValueError("the Stage-5D phase space changed")
    if history.get("event_current_voltage_D_J_exact") != "0":
        raise ValueError("the exact section derivative was lost")
    for name in (
        "voltage_translation_z_t_times_T_J_interval",
        "event_aligned_voltage_history_D_J_interval",
        "event_current_recovery_D_J_interval",
    ):
        _parse_interval(_mapping(history.get(name), name), name)
    y_norm = DirectedInterval.from_decimal(str(history.get("Y_norm_upper")), 96)
    if y_norm.lower <= 0 or not gmpy2.is_finite(y_norm.upper):
        raise ValueError("the Stage-5D Y-derivative norm is invalid")
    event_recovery = _parse_interval(
        _mapping(
            history.get("event_current_recovery_D_J_interval"),
            "event recovery derivative",
        ),
        "event recovery derivative",
    )
    if event_recovery.upper >= 0:
        raise ValueError("the event-aligned recovery monotonicity was lost")

    action = _mapping(
        certificate.get("fixed_center_route_c_functional_action"),
        "functional action",
    )
    if action.get("oriented_interval") is not None:
        raise ValueError("an oriented Stage-4D action was silently manufactured")
    normalized_action = DirectedInterval.from_decimal(
        str(action.get("normalized_action_modulus_upper")), 96
    )
    fallback_action = DirectedInterval.from_decimal(
        str(action.get("global_operator_norm_fallback_upper")), 96
    )
    if normalized_action.lower <= 0 or normalized_action.upper > fallback_action.lower:
        raise ValueError("the Stage-5D functional action bound changed")

    interface = _mapping(certificate.get("stable_gap_interface"), "stable interface")
    for name in (
        "stable_gap_endpoint_intervals",
        "stable_gap_derivative_interval",
        "interval_newton_image",
        "pulse_parameter_Jc",
    ):
        if interface.get(name) is not None:
            raise ValueError("an open stable-sheet or onset field was populated")
    if interface.get("oriented_functional_action_sign_available") is not False:
        raise ValueError("the missing oriented action sign was promoted")

    repository = Path(repository).resolve()
    source_hashes = _mapping(manifest.get("source_sha256"), "source hashes")
    dependency_hashes = _mapping(
        manifest.get("dependency_source_sha256"), "dependency hashes"
    )
    if set(source_hashes) != set(SOURCE_MANIFEST):
        raise ValueError("Stage-5D source manifest changed")
    if set(dependency_hashes) != set(DEPENDENCY_SOURCE_MANIFEST):
        raise ValueError("Stage-5D dependency manifest changed")
    for relative in SOURCE_MANIFEST:
        if source_hashes.get(relative) != _sha256_path(repository / relative):
            raise ValueError(f"Stage-5D source changed: {relative}")
    for relative in DEPENDENCY_SOURCE_MANIFEST:
        if dependency_hashes.get(relative) != _sha256_path(repository / relative):
            raise ValueError(f"Stage-5D dependency changed: {relative}")
    expected_parents = {
        STAGE5B_RELATIVE_PATH: STAGE5B_SHA256,
        STAGE5C_RELATIVE_PATH: STAGE5C_SHA256,
        STAGE4D_RELATIVE_PATH: STAGE4D_SHA256,
    }
    if dict(_mapping(manifest.get("parent_sha256"), "parent hashes")) != expected_parents:
        raise ValueError("Stage-5D parent manifest changed")
    for relative, expected in expected_parents.items():
        if _sha256_path(repository / relative) != expected:
            raise ValueError(f"Stage-5D bound parent changed: {relative}")

    if recompute:
        build_stage5d_certificate.cache_clear()
        build_sensitivity_error_propagation.cache_clear()
        build_remainder_propagation.cache_clear()
        build_coefficient_propagation.cache_clear()
        rebuilt = build_stage5d_certificate(repository)
        if canonical_sha256(rebuilt) != canonical_sha256(certificate):
            raise ValueError("Stage-5D directed replay changed")


__all__ = [
    "FALSE_FLAGS",
    "RESULT_RELATIVE_PATH",
    "TRUE_FLAGS",
    "build_sensitivity_error_propagation",
    "build_stage5d_certificate",
    "build_stage5d_result",
    "validate_stage5d_result",
]
