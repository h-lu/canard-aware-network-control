"""Numerical target-amplitude candidate for a prepared causal graph tube.

The bounded clocked-tail graph extension supplies a genuine graph theorem at
non-explicit small amplitude, but its singular ``sigma`` clock fails at the
target value ``rho=1/sqrt(5)``.  This module tests the actual target-amplitude
geometry rather than reusing singular slots.

The construction is deliberately local and numerical.  A one-parameter
family satisfying the first RFDE compatibility condition is prepared at
scaled time ``t=-3``.
The physical delay equation is then integrated by the method of steps through
``t=3``.  The resulting map

    (t, lambda) -> u(t, lambda)

is a candidate tubular chart.  Its time coordinate has the algebraic clock
identity ``grad(t) dot u_t = 1`` wherever the chart is invertible.  Delayed
slots retain the same ``lambda`` and have smaller time, so they are causal by
construction.

An exact proposition also records that a sufficiently smooth embedded RFDE
solution family induces a local fixed graph with intrinsic time clock one and
transverse first integral.  This proposition is conditional: the numerical
family does not validate its embedding or regularity hypotheses.

All reported hulls, Jacobian margins, boundary checks, and integration errors
are binary64 diagnostics.  They do not prove injectivity, construct a global
cutoff extension, validate an interval self-map, or prove a target fixed graph.
In fact, the diagnostics show that the old normal cutoff is not one on every
delayed slot, so this candidate is not a fixed point of the existing
clocked-tail operator.  Its purpose is to isolate a viable recentered-tube
route and the exact interval gates still needed.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from hashlib import sha256
import json
import math
from pathlib import Path
import platform
from typing import Any, Mapping, Sequence

import numpy as np
from numpy.typing import NDArray
from scipy.integrate import solve_ivp

from canard_control.fixed_epsilon_clocked_tail_graph_extension import (
    canard_coordinates,
    clocked_tail_slot_transform,
    clocked_tail_weight,
    smooth_step,
    smooth_step_derivative,
)
from canard_control.fixed_epsilon_frozen_graph_operator import (
    FlowSlots,
    uncut_physical_transform,
)
from canard_control.fixed_epsilon_quadratic_root_bvp import (
    DELTA,
    THETA_PERIOD_DIAGNOSTIC,
)


MODEL_ID = "fixed-epsilon-target-prepared-causal-tube-candidate"
AUDIT_ID = "fixed-epsilon-target-prepared-causal-tube-candidate-v1"

TARGET_RHO = DELTA
TARGET_ETA = 0.0
TARGET_THETA = THETA_PERIOD_DIAGNOSTIC
TARGET_NU = 0.21256022233963731
TARGET_PHASE_SHIFT = -0.061579261574946566
SECTION_HALF_WIDTH = 3.0
INCOMING_TIME = -SECTION_HALF_WIDTH
OUTGOING_TIME = SECTION_HALF_WIDTH
TRANSVERSE_RADIUS = 0.05
TRANSVERSE_SAMPLE_COUNT = 41
CURRENT_TIME_SAMPLE_COUNT = 601
EXTENDED_TIME_SAMPLE_COUNT = 1001
BOUNDARY_TIME_SAMPLE_COUNT = 301
PREPARATION_BUMP_WIDTH = 1.0
REFINEMENT_MAX_STEPS = (0.04, 0.02, 0.01)
SOLVER_RTOL = 1.0e-10
SOLVER_ATOL = 1.0e-12

TWO_SIDED_RESULT_SHA256 = (
    "a35c23f58cb80a83b5d14d303edccc160a66e402e9f042b18d0e992a2388dabd"
)
CLOCKED_TAIL_RESULT_SHA256 = (
    "826c8ddbd2e9794cec344456f09ccefc8d4d8d737950350859f1679691f1760e"
)

PROOF_SOURCE_RELATIVE_PATH = (
    "src/canard_control/fixed_epsilon_target_causal_tube_candidate.py"
)
GENERATOR_RELATIVE_PATH = (
    "experiments/fixed_epsilon_target_causal_tube_candidate.py"
)
RESULT_RELATIVE_PATH = (
    "experiments/results/fixed_epsilon_target_causal_tube_candidate.json"
)
NOTE_RELATIVE_PATH = "docs/fixed-epsilon-target-causal-tube-candidate.md"
DEFAULT_COMMAND = (
    "PYTHONPATH=src /usr/bin/python3 "
    "experiments/fixed_epsilon_target_causal_tube_candidate.py"
)
MANIFEST_ARITHMETIC = (
    "binary64 SciPy DOP853 method of steps with dense output; sampled hull, "
    "Jacobian, boundary, cutoff, and residual diagnostics; no intervals, "
    "global injectivity proof, cutoff extension, target graph theorem, "
    "trace solve, Fredholm inverse, or root validation"
)

PARENT_SHA256 = {
    "fixed_epsilon_two_sided_candidate_result": TWO_SIDED_RESULT_SHA256,
    "fixed_epsilon_clocked_tail_graph_extension_result": (
        CLOCKED_TAIL_RESULT_SHA256
    ),
}

PARENT_CLAIM_CHECK_KEYS = {
    "two_sided_parent_supplies_only_a_nonselected_binary64_anchor",
    "anchor_values_replayed_from_two_sided_parent",
    "clocked_tail_parent_leaves_target_graph_and_clock_open",
    "clocked_tail_parent_records_raw_sigma_clock_failure",
}


Point = tuple[float, float]


def _finite(value: object, name: str) -> float:
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result


def _format(value: float) -> str:
    return format(float(value), ".17g")


@dataclass(frozen=True)
class TargetTubeConfiguration:
    """Frozen operating slice and sampling configuration."""

    rho: float = TARGET_RHO
    nu: float = TARGET_NU
    eta: float = TARGET_ETA
    theta: float = TARGET_THETA
    phase_shift: float = TARGET_PHASE_SHIFT
    section_half_width: float = SECTION_HALF_WIDTH
    transverse_radius: float = TRANSVERSE_RADIUS
    transverse_sample_count: int = TRANSVERSE_SAMPLE_COUNT

    @property
    def incoming_time(self) -> float:
        return -self.section_half_width

    @property
    def outgoing_time(self) -> float:
        return self.section_half_width

    @property
    def oldest_retained_time(self) -> float:
        return self.incoming_time - self.theta

    def validate(self) -> None:
        for name in (
            "rho",
            "nu",
            "eta",
            "theta",
            "phase_shift",
            "section_half_width",
            "transverse_radius",
        ):
            _finite(getattr(self, name), name)
        if self.rho <= 0.0 or self.theta <= 0.0:
            raise ValueError("rho and theta must be positive")
        if self.section_half_width <= 0.0:
            raise ValueError("section_half_width must be positive")
        if self.transverse_radius <= 0.0:
            raise ValueError("transverse_radius must be positive")
        if (
            type(self.transverse_sample_count) is not int
            or self.transverse_sample_count < 5
            or self.transverse_sample_count % 2 == 0
        ):
            raise ValueError(
                "transverse_sample_count must be an odd integer at least five"
            )


def preparation_bump(relative_time: float) -> float:
    """Return the flat-left compatible X-history perturbation.

    The argument is ``r=t-t_in<=0``.  On ``r<=-1`` the perturbation is zero;
    on ``[-1,0]`` it is ``r*S(r+1)``.  Thus ``b(0)=0`` and the left derivative
    is one, while every derivative vanishes at ``r=-1``.
    """

    relative = _finite(relative_time, "relative_time")
    if relative > 0.0:
        raise ValueError("preparation bump is defined only for r<=0")
    if relative <= -PREPARATION_BUMP_WIDTH:
        return 0.0
    return relative * smooth_step(relative / PREPARATION_BUMP_WIDTH + 1.0)


def preparation_bump_derivative(relative_time: float) -> float:
    """Return the left derivative of :func:`preparation_bump`."""

    relative = _finite(relative_time, "relative_time")
    if relative > 0.0:
        raise ValueError("preparation bump is defined only for r<=0")
    if relative <= -PREPARATION_BUMP_WIDTH:
        return 0.0
    argument = relative / PREPARATION_BUMP_WIDTH + 1.0
    return smooth_step(argument) + (
        relative
        * smooth_step_derivative(argument)
        / PREPARATION_BUMP_WIDTH
    )


def entry_compatibility_shift(
    configuration: TargetTubeConfiguration,
) -> float:
    """Return the exact constant Y shift used by the incoming template."""

    configuration.validate()
    q_value = configuration.phase_shift
    section = configuration.section_half_width
    rho = configuration.rho
    eta = configuration.eta
    x0 = (section - q_value) / 2.0
    x4 = (section + 4.0 - q_value) / 2.0
    x5 = (section + 5.0 - q_value) / 2.0
    xtheta = (section + configuration.theta - q_value) / 2.0
    correction = (
        rho * (-x0**3 / 3.0 + 0.2 * ((x4 + x5) / 2.0 - x0))
        + rho**2 * eta * (x0 * x0 - xtheta * xtheta)
        + rho**3
        * 0.25
        * ((x4**3 + x5**3) / 2.0 - x0**3)
    )
    return -correction


def prepared_history_state(
    time: float,
    transverse: float,
    configuration: TargetTubeConfiguration | None = None,
) -> Point:
    """Evaluate one incoming history in the prepared transverse family."""

    config = configuration or TargetTubeConfiguration()
    config.validate()
    time_value = _finite(time, "time")
    transverse_value = _finite(transverse, "transverse")
    if time_value > config.incoming_time:
        raise ValueError("prepared history is defined only up to incoming time")
    if abs(transverse_value) > config.transverse_radius * (1.0 + 1e-14):
        raise ValueError("transverse parameter lies outside the frozen strip")
    shifted = time_value + config.phase_shift
    bump = preparation_bump(time_value - config.incoming_time)
    x_value = -shifted / 2.0 + transverse_value * bump
    y_value = (
        (shifted * shifted - 2.0) / 4.0
        + config.rho
        * config.nu
        * (time_value + config.section_half_width)
        + entry_compatibility_shift(config)
        + transverse_value
    )
    return _finite(x_value, "prepared X"), _finite(y_value, "prepared Y")


def prepared_history_derivative(
    time: float,
    transverse: float,
    configuration: TargetTubeConfiguration | None = None,
) -> Point:
    """Evaluate the time derivative of the prepared history."""

    config = configuration or TargetTubeConfiguration()
    config.validate()
    time_value = _finite(time, "time")
    transverse_value = _finite(transverse, "transverse")
    if time_value > config.incoming_time:
        raise ValueError("prepared history is defined only up to incoming time")
    if abs(transverse_value) > config.transverse_radius * (1.0 + 1e-14):
        raise ValueError("transverse parameter lies outside the frozen strip")
    return (
        -0.5
        + transverse_value
        * preparation_bump_derivative(time_value - config.incoming_time),
        (time_value + config.phase_shift) / 2.0
        + config.rho * config.nu,
    )


def prepared_history_transverse_derivative(
    time: float,
    configuration: TargetTubeConfiguration | None = None,
) -> Point:
    """Return the exact lambda derivative on the prepared branch."""

    config = configuration or TargetTubeConfiguration()
    config.validate()
    time_value = _finite(time, "time")
    if time_value > config.incoming_time:
        raise ValueError("prepared history is defined only up to incoming time")
    return preparation_bump(time_value - config.incoming_time), 1.0


def _physical_fields(
    current: NDArray[np.float64],
    delayed_4: NDArray[np.float64],
    delayed_5: NDArray[np.float64],
    delayed_theta: NDArray[np.float64],
    configuration: TargetTubeConfiguration,
) -> NDArray[np.float64]:
    count = current.shape[0]
    output = np.empty_like(current)
    for index in range(count):
        output[index] = uncut_physical_transform(
            FlowSlots(
                current=tuple(map(float, current[index])),
                delay_4=tuple(map(float, delayed_4[index])),
                delay_5=tuple(map(float, delayed_5[index])),
                delay_theta=tuple(map(float, delayed_theta[index])),
            ),
            rho=configuration.rho,
            nu=configuration.nu,
            eta=configuration.eta,
        )
    return output


@dataclass
class TargetTubeNumericalSolution:
    """Dense method-of-steps solution for every sampled transverse label."""

    configuration: TargetTubeConfiguration
    transverse_values: NDArray[np.float64]
    segments: list[tuple[float, float, Any]]
    function_evaluations: int
    maximum_step: float

    def states(self, time: float) -> NDArray[np.float64]:
        time_value = _finite(time, "time")
        config = self.configuration
        tolerance = 2.0e-11 * max(1.0, abs(time_value))
        if time_value <= config.incoming_time:
            return np.asarray(
                [
                    prepared_history_state(time_value, value, config)
                    for value in self.transverse_values
                ],
                dtype=float,
            )
        for left, right, interpolant in reversed(self.segments):
            if left - tolerance <= time_value <= right + tolerance:
                clipped = min(max(time_value, left), right)
                return np.asarray(interpolant(clipped), dtype=float).reshape(
                    len(self.transverse_values), 2
                )
        if time_value <= config.incoming_time + tolerance:
            return np.asarray(
                [
                    prepared_history_state(
                        config.incoming_time, value, config
                    )
                    for value in self.transverse_values
                ],
                dtype=float,
            )
        raise ValueError("time lies outside the computed causal tube")

    def slot_states(
        self, time: float
    ) -> tuple[
        NDArray[np.float64],
        NDArray[np.float64],
        NDArray[np.float64],
        NDArray[np.float64],
    ]:
        time_value = _finite(time, "time")
        config = self.configuration
        if not config.incoming_time <= time_value <= config.outgoing_time:
            raise ValueError("current time lies outside the physical strip")
        return (
            self.states(time_value),
            self.states(time_value - 4.0),
            self.states(time_value - 5.0),
            self.states(time_value - config.theta),
        )

    def fields(self, time: float) -> NDArray[np.float64]:
        time_value = _finite(time, "time")
        config = self.configuration
        if time_value < config.incoming_time:
            return np.asarray(
                [
                    prepared_history_derivative(time_value, value, config)
                    for value in self.transverse_values
                ],
                dtype=float,
            )
        current, delayed_4, delayed_5, delayed_theta = self.slot_states(
            time_value
        )
        return _physical_fields(
            current,
            delayed_4,
            delayed_5,
            delayed_theta,
            config,
        )


def solve_target_causal_tube(
    maximum_step: float = REFINEMENT_MAX_STEPS[-1],
    configuration: TargetTubeConfiguration | None = None,
) -> TargetTubeNumericalSolution:
    """Integrate the transverse family by method of steps."""

    config = configuration or TargetTubeConfiguration()
    config.validate()
    step = _finite(maximum_step, "maximum_step")
    if step <= 0.0 or step > 4.0:
        raise ValueError("maximum_step must lie in (0,4]")
    transverse_values = np.linspace(
        -config.transverse_radius,
        config.transverse_radius,
        config.transverse_sample_count,
        dtype=float,
    )
    count = len(transverse_values)
    segments: list[tuple[float, float, Any]] = []

    def prepared_states(time: float) -> NDArray[np.float64]:
        return np.asarray(
            [
                prepared_history_state(time, value, config)
                for value in transverse_values
            ],
            dtype=float,
        )

    def known_states(time: float) -> NDArray[np.float64]:
        tolerance = 2.0e-11 * max(1.0, abs(time))
        if time <= config.incoming_time:
            return prepared_states(time)
        for left, right, interpolant in reversed(segments):
            if left - tolerance <= time <= right + tolerance:
                clipped = min(max(time, left), right)
                return np.asarray(interpolant(clipped), dtype=float).reshape(
                    count, 2
                )
        if time <= config.incoming_time + tolerance:
            return prepared_states(config.incoming_time)
        raise RuntimeError("method of steps queried unfinished history")

    def right_hand_side(
        time: float, flattened_state: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        current = np.asarray(flattened_state, dtype=float).reshape(count, 2)
        output = _physical_fields(
            current,
            known_states(time - 4.0),
            known_states(time - 5.0),
            known_states(time - config.theta),
            config,
        )
        return output.ravel()

    left = config.incoming_time
    state = prepared_states(left).ravel()
    function_evaluations = 0
    while left < config.outgoing_time - 1.0e-14:
        right = min(left + 4.0, config.outgoing_time)
        integration = solve_ivp(
            right_hand_side,
            (left, right),
            state,
            method="DOP853",
            rtol=SOLVER_RTOL,
            atol=SOLVER_ATOL,
            max_step=step,
            dense_output=True,
        )
        if not integration.success or integration.sol is None:
            raise RuntimeError(
                f"target tube integration failed: {integration.message}"
            )
        segments.append((left, right, integration.sol))
        state = np.asarray(integration.y[:, -1], dtype=float)
        function_evaluations += int(integration.nfev)
        left = right
    return TargetTubeNumericalSolution(
        configuration=config,
        transverse_values=transverse_values,
        segments=segments,
        function_evaluations=function_evaluations,
        maximum_step=step,
    )


@dataclass(frozen=True)
class HullRecord:
    phase_minimum: str
    phase_maximum: str
    normal_minimum: str
    normal_maximum: str


@dataclass(frozen=True)
class RefinementRecord:
    maximum_step: str
    function_evaluations: int
    maximum_state_change_to_next: str


@dataclass(frozen=True)
class TargetCausalTubeCandidateCertificate:
    model_id: str
    audit_id: str
    arithmetic: str
    target_rho: str
    target_nu: str
    target_eta: str
    target_theta: str
    phase_shift_anchor: str
    anchor_scope: str
    physical_time_interval: tuple[str, str]
    retained_time_interval: tuple[str, str]
    transverse_interval: tuple[str, str]
    transverse_sample_count: int
    current_time_sample_count: int
    extended_time_sample_count: int
    preparation_formula: str
    preparation_endpoint_values: tuple[str, str]
    preparation_endpoint_derivatives: tuple[str, str]
    maximum_entry_compatibility_residual: str
    refinement_rows: tuple[RefinementRecord, ...]
    current_hull: HullRecord
    delay_4_hull: HullRecord
    delay_5_hull: HullRecord
    delay_theta_hull: HullRecord
    minimum_current_old_cutoff_weight: str
    minimum_all_delayed_old_cutoff_weight: str
    maximum_old_clocked_tail_operator_defect: str
    minimum_sampled_sigma_clock: str
    maximum_sampled_sigma_clock: str
    sigma_clock_negative_time_hull: tuple[str, str]
    minimum_sampled_chart_determinant: str
    maximum_sampled_chart_determinant: str
    minimum_sampled_absolute_chart_determinant: str
    maximum_sampled_time_gradient_norm: str
    maximum_sampled_time_clock_identity_residual: str
    strict_sampled_boundary_segment_intersections: int
    sampled_boundary_signed_area: str
    maximum_sampled_dde_derivative_residual: str
    causal_slot_time_order: tuple[str, str, str]
    proposed_interval_chart: str
    conditional_local_graph_domain: str
    conditional_embedding_hypothesis: str
    conditional_regularities: str
    conditional_complete_cutoff_extension: str
    conditional_flow_shift_identity: str
    conditional_graph_fixed_identity: str
    conditional_intrinsic_coordinate_identities: tuple[str, str]
    conditional_lambda_face_barriers: tuple[str, str, str]
    target_prepared_local_causal_graph_candidate_computed: bool
    first_order_compatible_transverse_preparation_constructed_exactly: bool
    candidate_time_clock_identity_is_algebraic_where_chart_invertible: bool
    sampled_current_tube_inside_old_uncut_plateau: bool
    sampled_delayed_slots_have_same_label_causal_representation: bool
    sampled_chart_jacobian_nonzero: bool
    sampled_boundary_polygon_simple: bool
    actual_candidate_sigma_clock_changes_sign: bool
    old_clocked_tail_delayed_plateau_containment_fails_on_candidate: bool
    refinement_stabilization_observed: bool
    conditional_prepared_embedding_local_graph_theorem_proved: bool
    conditional_c2_embedding_implies_complete_cb1_extension_proved: bool
    conditional_c4_embedding_implies_complete_cb3_extension_proved: bool
    conditional_flow_shift_and_fixed_identity_proved: bool
    conditional_time_clock_and_lambda_first_integral_proved: bool
    conditional_lambda_faces_are_invariant_nonstrict_barriers_proved: bool
    target_old_clocked_tail_fixed_graph_validated: bool
    target_centered_global_cutoff_extension_constructed: bool
    target_chart_global_injectivity_proved: bool
    target_interval_flow_enclosure_validated: bool
    target_interval_slot_self_map_validated: bool
    target_candidate_class_self_map_validated: bool
    target_uniform_chart_inverse_bound_validated: bool
    target_c4_chart_and_seam_compatibility_validated: bool
    target_j_barriers_validated: bool
    target_strict_lambda_barrier_margin_validated: bool
    target_global_graph_fixed_point_validated: bool
    target_volterra_constants_validated: bool
    target_parameter_box_validated: bool
    target_trace_pair_fredholm_validated: bool
    fixed_epsilon_complete_history_root_validated: bool
    minimal_interval_gate: str


NUMERICAL_TRUE_FLAGS = (
    "target_prepared_local_causal_graph_candidate_computed",
    "first_order_compatible_transverse_preparation_constructed_exactly",
    "candidate_time_clock_identity_is_algebraic_where_chart_invertible",
    "sampled_current_tube_inside_old_uncut_plateau",
    "sampled_delayed_slots_have_same_label_causal_representation",
    "sampled_chart_jacobian_nonzero",
    "sampled_boundary_polygon_simple",
    "actual_candidate_sigma_clock_changes_sign",
    "old_clocked_tail_delayed_plateau_containment_fails_on_candidate",
    "refinement_stabilization_observed",
)

CONDITIONAL_THEOREM_FLAGS = (
    "conditional_prepared_embedding_local_graph_theorem_proved",
    "conditional_c2_embedding_implies_complete_cb1_extension_proved",
    "conditional_c4_embedding_implies_complete_cb3_extension_proved",
    "conditional_flow_shift_and_fixed_identity_proved",
    "conditional_time_clock_and_lambda_first_integral_proved",
    "conditional_lambda_faces_are_invariant_nonstrict_barriers_proved",
)

OPEN_FLAGS = (
    "target_old_clocked_tail_fixed_graph_validated",
    "target_centered_global_cutoff_extension_constructed",
    "target_chart_global_injectivity_proved",
    "target_interval_flow_enclosure_validated",
    "target_interval_slot_self_map_validated",
    "target_candidate_class_self_map_validated",
    "target_uniform_chart_inverse_bound_validated",
    "target_c4_chart_and_seam_compatibility_validated",
    "target_j_barriers_validated",
    "target_strict_lambda_barrier_margin_validated",
    "target_global_graph_fixed_point_validated",
    "target_volterra_constants_validated",
    "target_parameter_box_validated",
    "target_trace_pair_fredholm_validated",
    "fixed_epsilon_complete_history_root_validated",
)


def _hull(points: NDArray[np.float64]) -> HullRecord:
    flattened = np.asarray(points, dtype=float).reshape(-1, 2)
    phases = -2.0 * flattened[:, 0]
    normals = flattened[:, 1] - flattened[:, 0] ** 2 + 0.5
    return HullRecord(
        phase_minimum=_format(np.min(phases)),
        phase_maximum=_format(np.max(phases)),
        normal_minimum=_format(np.min(normals)),
        normal_maximum=_format(np.max(normals)),
    )


def _strict_boundary_intersections(polyline: NDArray[np.float64]) -> int:
    """Count strict intersections of nonadjacent closed-polygon segments."""

    points = np.asarray(polyline, dtype=float)
    count = len(points)

    def orientation(a: NDArray, b: NDArray, c: NDArray) -> float:
        first = b - a
        second = c - a
        return float(first[0] * second[1] - first[1] * second[0])

    intersections = 0
    for first_index in range(count):
        first_next = (first_index + 1) % count
        for second_index in range(first_index + 1, count):
            second_next = (second_index + 1) % count
            if second_index == first_next or first_index == second_next:
                continue
            a = points[first_index]
            b = points[first_next]
            c = points[second_index]
            d = points[second_next]
            o1 = orientation(a, b, c)
            o2 = orientation(a, b, d)
            o3 = orientation(c, d, a)
            o4 = orientation(c, d, b)
            if o1 * o2 < -1.0e-24 and o3 * o4 < -1.0e-24:
                intersections += 1
    return intersections


def _boundary_polyline(
    solution: TargetTubeNumericalSolution,
) -> NDArray[np.float64]:
    config = solution.configuration
    times = np.linspace(
        config.oldest_retained_time,
        config.outgoing_time,
        BOUNDARY_TIME_SAMPLE_COUNT,
    )
    bottom = solution.states(config.oldest_retained_time)
    right = np.asarray([solution.states(time)[-1] for time in times])
    top = solution.states(config.outgoing_time)
    left = np.asarray([solution.states(time)[0] for time in times])
    return np.vstack(
        (
            bottom,
            right[1:],
            top[-2::-1],
            left[-2:0:-1],
        )
    )


def _entry_compatibility_residual(
    solution: TargetTubeNumericalSolution,
) -> float:
    config = solution.configuration
    time = config.incoming_time
    current = solution.states(time)
    physical = _physical_fields(
        current,
        solution.states(time - 4.0),
        solution.states(time - 5.0),
        solution.states(time - config.theta),
        config,
    )
    prepared = np.asarray(
        [
            prepared_history_derivative(time, value, config)
            for value in solution.transverse_values
        ]
    )
    return float(np.max(np.abs(prepared - physical)))


def _maximum_dde_derivative_residual(
    solution: TargetTubeNumericalSolution,
) -> float:
    config = solution.configuration
    difference_step = 2.0e-5
    sample_times = np.linspace(
        config.incoming_time + 0.01,
        config.outgoing_time - 0.01,
        241,
    )
    residual = 0.0
    for time in sample_times:
        if abs(time - (config.incoming_time + 4.0)) < 4 * difference_step:
            continue
        derivative = (
            solution.states(time + difference_step)
            - solution.states(time - difference_step)
        ) / (2.0 * difference_step)
        residual = max(
            residual,
            float(np.max(np.abs(derivative - solution.fields(time)))),
        )
    return residual


def _refinement_records(
    solutions: Sequence[TargetTubeNumericalSolution],
) -> tuple[RefinementRecord, ...]:
    if len(solutions) != len(REFINEMENT_MAX_STEPS):
        raise ValueError("the frozen refinement list has the wrong length")
    config = solutions[0].configuration
    if any(solution.configuration != config for solution in solutions[1:]):
        raise ValueError("refinement solutions use different configurations")
    sample_times = np.linspace(
        config.incoming_time, config.outgoing_time, 301
    )
    changes: list[float] = []
    for coarse, fine in zip(solutions[:-1], solutions[1:], strict=True):
        changes.append(
            max(
                float(np.max(np.abs(coarse.states(time) - fine.states(time))))
                for time in sample_times
            )
        )
    records = []
    for index, solution in enumerate(solutions):
        change = changes[index] if index < len(changes) else 0.0
        records.append(
            RefinementRecord(
                maximum_step=_format(solution.maximum_step),
                function_evaluations=solution.function_evaluations,
                maximum_state_change_to_next=_format(change),
            )
        )
    return tuple(records)


def build_target_causal_tube_candidate(
    configuration: TargetTubeConfiguration | None = None,
) -> TargetCausalTubeCandidateCertificate:
    """Compute the frozen binary64 target-tube candidate diagnostics."""

    config = configuration or TargetTubeConfiguration()
    config.validate()
    solutions = [
        solve_target_causal_tube(step, config)
        for step in REFINEMENT_MAX_STEPS
    ]
    solution = solutions[-1]

    current_times = np.linspace(
        config.incoming_time,
        config.outgoing_time,
        CURRENT_TIME_SAMPLE_COUNT,
    )
    extended_times = np.linspace(
        config.oldest_retained_time,
        config.outgoing_time,
        EXTENDED_TIME_SAMPLE_COUNT,
    )
    current_slots = [solution.slot_states(time) for time in current_times]
    current = np.asarray([slots[0] for slots in current_slots])
    delayed_4 = np.asarray([slots[1] for slots in current_slots])
    delayed_5 = np.asarray([slots[2] for slots in current_slots])
    delayed_theta = np.asarray([slots[3] for slots in current_slots])
    current_fields = np.asarray(
        [solution.fields(time) for time in current_times]
    )
    sigma_clock = -2.0 * current_fields[:, :, 0]
    negative_clock_times = np.repeat(
        current_times[:, None], config.transverse_sample_count, axis=1
    )[sigma_clock < 0.0]

    extended_states = np.asarray(
        [solution.states(time) for time in extended_times]
    )
    extended_fields = np.asarray(
        [solution.fields(time) for time in extended_times]
    )
    lambda_denominator = (
        solution.transverse_values[2:] - solution.transverse_values[:-2]
    )[None, :, None]
    lambda_derivative = (
        extended_states[:, 2:, :] - extended_states[:, :-2, :]
    ) / lambda_denominator
    interior_fields = extended_fields[:, 1:-1, :]
    determinants = (
        interior_fields[:, :, 0] * lambda_derivative[:, :, 1]
        - interior_fields[:, :, 1] * lambda_derivative[:, :, 0]
    )
    time_gradient_x = lambda_derivative[:, :, 1] / determinants
    time_gradient_y = -lambda_derivative[:, :, 0] / determinants
    clock_identity = (
        time_gradient_x * interior_fields[:, :, 0]
        + time_gradient_y * interior_fields[:, :, 1]
    )
    time_gradient_norm = np.sqrt(time_gradient_x**2 + time_gradient_y**2)

    current_weights: list[float] = []
    delayed_weights: list[float] = []
    old_operator_defect = 0.0
    for slots_at_time in current_slots:
        for index in range(config.transverse_sample_count):
            slot = FlowSlots(
                current=tuple(map(float, slots_at_time[0][index])),
                delay_4=tuple(map(float, slots_at_time[1][index])),
                delay_5=tuple(map(float, slots_at_time[2][index])),
                delay_theta=tuple(map(float, slots_at_time[3][index])),
            )
            current_weights.append(clocked_tail_weight(slot.current))
            delayed_weights.extend(
                (
                    clocked_tail_weight(slot.delay_4),
                    clocked_tail_weight(slot.delay_5),
                    clocked_tail_weight(slot.delay_theta),
                )
            )
            old_value = clocked_tail_slot_transform(
                slot,
                rho=config.rho,
                nu=config.nu,
                eta=config.eta,
            )
            physical_value = uncut_physical_transform(
                slot,
                rho=config.rho,
                nu=config.nu,
                eta=config.eta,
            )
            old_operator_defect = max(
                old_operator_defect,
                abs(old_value[0] - physical_value[0]),
                abs(old_value[1] - physical_value[1]),
            )

    boundary = _boundary_polyline(solution)
    boundary_intersections = _strict_boundary_intersections(boundary)
    boundary_area = 0.5 * float(
        np.sum(
            boundary[:, 0] * np.roll(boundary[:, 1], -1)
            - boundary[:, 1] * np.roll(boundary[:, 0], -1)
        )
    )
    refinement_rows = _refinement_records(solutions)
    finest_change = float(refinement_rows[-2].maximum_state_change_to_next)
    current_hull = _hull(current)
    delayed_hulls = (
        _hull(delayed_4),
        _hull(delayed_5),
        _hull(delayed_theta),
    )
    current_inside = (
        float(current_hull.phase_minimum) >= -29.0
        and float(current_hull.phase_maximum) <= 21.0
        and float(current_hull.normal_minimum) >= -1.0
        and float(current_hull.normal_maximum) <= 1.0
    )
    delayed_old_plateau_failure = min(delayed_weights) < 1.0

    return TargetCausalTubeCandidateCertificate(
        model_id=MODEL_ID,
        audit_id=AUDIT_ID,
        arithmetic=MANIFEST_ARITHMETIC,
        target_rho=_format(config.rho),
        target_nu=_format(config.nu),
        target_eta=_format(config.eta),
        target_theta=_format(config.theta),
        phase_shift_anchor=_format(config.phase_shift),
        anchor_scope=(
            "finest two-sided binary64 candidate only; that parent explicitly "
            "does not construct selected attracting/repelling trace bundles"
        ),
        physical_time_interval=(
            _format(config.incoming_time),
            _format(config.outgoing_time),
        ),
        retained_time_interval=(
            _format(config.oldest_retained_time),
            _format(config.outgoing_time),
        ),
        transverse_interval=(
            _format(-config.transverse_radius),
            _format(config.transverse_radius),
        ),
        transverse_sample_count=config.transverse_sample_count,
        current_time_sample_count=CURRENT_TIME_SAMPLE_COUNT,
        extended_time_sample_count=EXTENDED_TIME_SAMPLE_COUNT,
        preparation_formula=(
            "h_lambda(t)=h_0(t)+lambda*(b(t+3),1), "
            "b(r)=r*S(r+1) on -1<r<=0 and 0 on r<=-1"
        ),
        preparation_endpoint_values=("b(0)=0", "partial_lambda Y=1"),
        preparation_endpoint_derivatives=(
            "b'_-(0)=1",
            "partial_t h_lambda(-3)=F_phys((h_lambda)_{-3}); C1 seam only",
        ),
        maximum_entry_compatibility_residual=_format(
            _entry_compatibility_residual(solution)
        ),
        refinement_rows=refinement_rows,
        current_hull=current_hull,
        delay_4_hull=delayed_hulls[0],
        delay_5_hull=delayed_hulls[1],
        delay_theta_hull=delayed_hulls[2],
        minimum_current_old_cutoff_weight=_format(min(current_weights)),
        minimum_all_delayed_old_cutoff_weight=_format(min(delayed_weights)),
        maximum_old_clocked_tail_operator_defect=_format(
            old_operator_defect
        ),
        minimum_sampled_sigma_clock=_format(np.min(sigma_clock)),
        maximum_sampled_sigma_clock=_format(np.max(sigma_clock)),
        sigma_clock_negative_time_hull=(
            _format(np.min(negative_clock_times)),
            _format(np.max(negative_clock_times)),
        ),
        minimum_sampled_chart_determinant=_format(np.min(determinants)),
        maximum_sampled_chart_determinant=_format(np.max(determinants)),
        minimum_sampled_absolute_chart_determinant=_format(
            np.min(np.abs(determinants))
        ),
        maximum_sampled_time_gradient_norm=_format(
            np.max(time_gradient_norm)
        ),
        maximum_sampled_time_clock_identity_residual=_format(
            np.max(np.abs(clock_identity - 1.0))
        ),
        strict_sampled_boundary_segment_intersections=boundary_intersections,
        sampled_boundary_signed_area=_format(boundary_area),
        maximum_sampled_dde_derivative_residual=_format(
            _maximum_dde_derivative_residual(solution)
        ),
        causal_slot_time_order=(
            "t-4<t",
            "t-5<t",
            "t-Theta_*<t",
        ),
        proposed_interval_chart=(
            "validate Psi(t,lambda)=u(t,lambda) on "
            "[-3-Theta_*,3]x[-0.05,0.05], enclose det D_Psi away "
            "from zero and certify its boundary degree; freeze a plateau "
            "around this curved hull before applying the causal Volterra map"
        ),
        conditional_local_graph_domain=(
            "Psi:U->Omega=Psi(U), with U open and containing compactly the "
            "entire smaller segment rectangle K=[a-tau_max,b]x[-r,r]; "
            "the fixed identity is asserted only on the smaller current "
            "image Psi([a,b]x[-r,r])"
        ),
        conditional_embedding_hypothesis=(
            "Psi is a C2 embedding on open U, hence Omega=Psi(U) is open and "
            "Q0=partial_t Psi composed with Psi^{-1} is C1 on Omega; Psi is "
            "an exact RFDE solution family on the smaller current rectangle"
        ),
        conditional_regularities=(
            "Psi in C^{k+1} implies Q0=partial_t Psi composed with Psi^{-1} "
            "is locally C^k; C2 gives Q0 in C1 and C4 gives Q0 in C3; the "
            "C4 case requires preparation/RFDE seam compatibility through "
            "total order four"
        ),
        conditional_complete_cutoff_extension=(
            "choose chi in C_c^infinity(Omega), chi=1 on a neighborhood of "
            "Psi(K), and define Q_tilde=chi*Q0 on Omega and zero outside; "
            "then Q_tilde is complete C_b^1 for C2 Psi and complete C_b^3 "
            "for C4 Psi"
        ),
        conditional_flow_shift_identity=(
            "Phi_{Q_tilde}^{-tau}(Psi(t,lambda))=Psi(t-tau,lambda) only "
            "when the entire chart segment from t-tau to t lies in the "
            "chi=1 retained neighborhood"
        ),
        conditional_graph_fixed_identity=(
            "T_phys(Q_tilde)(Psi(t,lambda))=partial_t Psi(t,lambda)="
            "Q_tilde(Psi(t,lambda)) only on the smaller physical current "
            "image; no global fixed point is claimed"
        ),
        conditional_intrinsic_coordinate_identities=(
            "D t_tube[Q_tilde]=1 on the retained agreement tube",
            "D lambda_tube[Q_tilde]=0 on the retained agreement tube",
        ),
        conditional_lambda_face_barriers=(
            "J_-=lambda_tube+r",
            "J_+=r-lambda_tube",
            "D J_-[Q_tilde]=D J_+[Q_tilde]=0 on the retained agreement "
            "tube; locally invariant nonstrict faces, not a uniform strict "
            "barrier margin for nearby candidate fields",
        ),
        target_prepared_local_causal_graph_candidate_computed=True,
        first_order_compatible_transverse_preparation_constructed_exactly=(
            True
        ),
        candidate_time_clock_identity_is_algebraic_where_chart_invertible=(
            True
        ),
        sampled_current_tube_inside_old_uncut_plateau=bool(current_inside),
        sampled_delayed_slots_have_same_label_causal_representation=True,
        sampled_chart_jacobian_nonzero=bool(
            np.min(np.abs(determinants)) > 0.0
        ),
        sampled_boundary_polygon_simple=(boundary_intersections == 0),
        actual_candidate_sigma_clock_changes_sign=bool(
            np.min(sigma_clock) < 0.0 < np.max(sigma_clock)
        ),
        old_clocked_tail_delayed_plateau_containment_fails_on_candidate=(
            delayed_old_plateau_failure and old_operator_defect > 0.0
        ),
        refinement_stabilization_observed=bool(finest_change < 1.0e-10),
        conditional_prepared_embedding_local_graph_theorem_proved=True,
        conditional_c2_embedding_implies_complete_cb1_extension_proved=True,
        conditional_c4_embedding_implies_complete_cb3_extension_proved=True,
        conditional_flow_shift_and_fixed_identity_proved=True,
        conditional_time_clock_and_lambda_first_integral_proved=True,
        conditional_lambda_faces_are_invariant_nonstrict_barriers_proved=(
            True
        ),
        target_old_clocked_tail_fixed_graph_validated=False,
        target_centered_global_cutoff_extension_constructed=False,
        target_chart_global_injectivity_proved=False,
        target_interval_flow_enclosure_validated=False,
        target_interval_slot_self_map_validated=False,
        target_candidate_class_self_map_validated=False,
        target_uniform_chart_inverse_bound_validated=False,
        target_c4_chart_and_seam_compatibility_validated=False,
        target_j_barriers_validated=False,
        target_strict_lambda_barrier_margin_validated=False,
        target_global_graph_fixed_point_validated=False,
        target_volterra_constants_validated=False,
        target_parameter_box_validated=False,
        target_trace_pair_fredholm_validated=False,
        fixed_epsilon_complete_history_root_validated=False,
        minimal_interval_gate=(
            "replace point samples by interval/Taylor-model enclosures of the "
            "prepared history and method-of-steps flow; prove det D_Psi has "
            "one sign and the boundary has degree one; then construct a "
            "target-centered cutoff plateau containing every 4,5,Theta_* "
            "slot, close the parameterized compatibility seam through total "
            "order four, and bound its inverse chart, strict robust barriers, "
            "and Volterra constants"
        ),
    )


def json_ready_target_causal_tube_candidate() -> dict[str, Any]:
    """Return the canonical JSON-ready target-tube diagnostic."""

    return json.loads(
        json.dumps({"certificate": asdict(build_target_causal_tube_candidate())})
    )


def validate_target_causal_tube_audit(payload: Mapping[str, Any]) -> None:
    """Reject scalar-type, numerical-record, or claim-ledger tampering."""

    if not isinstance(payload, Mapping):
        raise ValueError("target tube audit must be a mapping")
    certificate = payload.get("certificate")
    if not isinstance(certificate, Mapping):
        raise ValueError("target tube certificate must be a mapping")
    integer_keys = (
        "transverse_sample_count",
        "current_time_sample_count",
        "extended_time_sample_count",
        "strict_sampled_boundary_segment_intersections",
    )
    if any(type(certificate.get(key)) is not int for key in integer_keys):
        raise ValueError("an integer target-tube diagnostic has wrong type")
    if any(certificate.get(key) is not True for key in NUMERICAL_TRUE_FLAGS):
        raise ValueError("a numerical or exact-construction flag was weakened")
    if any(
        certificate.get(key) is not True for key in CONDITIONAL_THEOREM_FLAGS
    ):
        raise ValueError("a conditional local-graph theorem flag was weakened")
    if any(certificate.get(key) is not False for key in OPEN_FLAGS):
        raise ValueError("an open target theorem gate was promoted")
    boolean_fields = {
        field.name
        for field in fields(TargetCausalTubeCandidateCertificate)
        if field.type in (bool, "bool")
    }
    expected_boolean_fields = (
        set(NUMERICAL_TRUE_FLAGS)
        | set(CONDITIONAL_THEOREM_FLAGS)
        | set(OPEN_FLAGS)
    )
    if boolean_fields != expected_boolean_fields:
        raise AssertionError("the claim ledger does not cover every boolean")
    if dict(payload) != json_ready_target_causal_tube_candidate():
        raise ValueError("target causal tube audit differs from reference")


def _sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _read_json_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def verify_target_causal_tube_parent_evidence(
    repository: Path,
) -> tuple[dict[str, str], dict[str, bool]]:
    """Verify the two numerical parents and replay their scope boundaries."""

    paths = {
        "fixed_epsilon_two_sided_candidate_result": repository
        / "experiments/results/fixed_epsilon_two_sided_candidate.json",
        "fixed_epsilon_clocked_tail_graph_extension_result": repository
        / "experiments/results/fixed_epsilon_clocked_tail_graph_extension.json",
    }
    actual = {name: _sha256(path) for name, path in paths.items()}
    if actual != PARENT_SHA256:
        raise ValueError("a target causal tube parent hash changed")

    two_sided = _read_json_object(
        paths["fixed_epsilon_two_sided_candidate_result"]
    )
    clocked = _read_json_object(
        paths["fixed_epsilon_clocked_tail_graph_extension_result"]
    )
    two_certificate = two_sided.get("audit", {}).get("certificate", {})
    clock_certificate = clocked.get("audit", {}).get("certificate", {})
    two_rows = two_sided.get("audit", {}).get("rows", [])
    anchor_rows = [
        row
        for row in two_rows
        if isinstance(row, Mapping)
        and float(row.get("section_half_width", math.nan))
        == SECTION_HALF_WIDTH
        and row.get("mesh_per_scaled_time")
        == two_certificate.get("finest_mesh_per_scaled_time")
    ]
    checks = {
        "two_sided_parent_supplies_only_a_nonselected_binary64_anchor": (
            two_certificate.get("two_branch_discrete_candidate_computed")
            is True
            and two_certificate.get("selected_attracting_trace_bundle_constructed")
            is False
            and two_certificate.get("backward_extendible_repelling_bundle_constructed")
            is False
            and two_certificate.get("fixed_epsilon_selected_root_validated")
            is False
        ),
        "anchor_values_replayed_from_two_sided_parent": (
            len(anchor_rows) == 1
            and float(two_certificate.get("central_section_half_width"))
            == SECTION_HALF_WIDTH
            and float(two_certificate.get("finest_nu_candidate")) == TARGET_NU
            and math.isclose(
                float(anchor_rows[0]["q_candidate"]),
                TARGET_PHASE_SHIFT,
                rel_tol=0.0,
                abs_tol=0.0,
            )
        ),
        "clocked_tail_parent_leaves_target_graph_and_clock_open": (
            clock_certificate.get(
                "target_positive_amplitude_graph_candidate_computed"
            )
            is False
            and clock_certificate.get("target_uniform_clock_bound_validated")
            is False
            and clock_certificate.get("target_candidate_self_map_validated")
            is False
        ),
        "clocked_tail_parent_records_raw_sigma_clock_failure": (
            clock_certificate.get("raw_singular_slot_target_clock_failure_proved")
            is True
        ),
    }
    if set(checks) != PARENT_CLAIM_CHECK_KEYS or not all(checks.values()):
        raise ValueError("a target causal tube parent claim check failed")
    return actual, checks


def validate_target_causal_tube_result(
    payload: Mapping[str, Any], repository: Path
) -> None:
    """Validate a generated result including manifest and parent evidence."""

    if not isinstance(payload, Mapping):
        raise ValueError("target tube result must be a mapping")
    audit = payload.get("audit")
    manifest = payload.get("manifest")
    if not isinstance(audit, Mapping) or not isinstance(manifest, Mapping):
        raise ValueError("target tube result requires audit and manifest")
    validate_target_causal_tube_audit(audit)
    parent_hashes, parent_checks = verify_target_causal_tube_parent_evidence(
        repository
    )
    expected_paths = {
        "proof_source": PROOF_SOURCE_RELATIVE_PATH,
        "generator": GENERATOR_RELATIVE_PATH,
        "note": NOTE_RELATIVE_PATH,
    }
    for key, relative in expected_paths.items():
        if manifest.get(key) != relative:
            raise ValueError(f"manifest {key} path changed")
        if manifest.get(f"{key}_sha256") != _sha256(repository / relative):
            raise ValueError(f"manifest {key} hash changed")
    if manifest.get("parent_sha256") != parent_hashes:
        raise ValueError("manifest parent hashes changed")
    if manifest.get("parent_claim_checks") != parent_checks:
        raise ValueError("manifest parent checks changed")
    if manifest.get("default_command") != DEFAULT_COMMAND:
        raise ValueError("manifest default command changed")
    if manifest.get("arithmetic") != MANIFEST_ARITHMETIC:
        raise ValueError("manifest arithmetic changed")
    if manifest.get("python") != platform.python_version():
        raise ValueError("manifest Python version changed")
    if manifest.get("platform") != platform.platform():
        raise ValueError("manifest platform changed")


__all__ = [
    "AUDIT_ID",
    "CLOCKED_TAIL_RESULT_SHA256",
    "CONDITIONAL_THEOREM_FLAGS",
    "CURRENT_TIME_SAMPLE_COUNT",
    "DEFAULT_COMMAND",
    "EXTENDED_TIME_SAMPLE_COUNT",
    "GENERATOR_RELATIVE_PATH",
    "MANIFEST_ARITHMETIC",
    "MODEL_ID",
    "NOTE_RELATIVE_PATH",
    "NUMERICAL_TRUE_FLAGS",
    "OPEN_FLAGS",
    "PARENT_CLAIM_CHECK_KEYS",
    "PARENT_SHA256",
    "PROOF_SOURCE_RELATIVE_PATH",
    "REFINEMENT_MAX_STEPS",
    "RESULT_RELATIVE_PATH",
    "TARGET_ETA",
    "TARGET_NU",
    "TARGET_PHASE_SHIFT",
    "TARGET_RHO",
    "TARGET_THETA",
    "TRANSVERSE_RADIUS",
    "TRANSVERSE_SAMPLE_COUNT",
    "TWO_SIDED_RESULT_SHA256",
    "TargetCausalTubeCandidateCertificate",
    "TargetTubeConfiguration",
    "TargetTubeNumericalSolution",
    "build_target_causal_tube_candidate",
    "entry_compatibility_shift",
    "json_ready_target_causal_tube_candidate",
    "prepared_history_derivative",
    "prepared_history_state",
    "prepared_history_transverse_derivative",
    "preparation_bump",
    "preparation_bump_derivative",
    "solve_target_causal_tube",
    "validate_target_causal_tube_audit",
    "validate_target_causal_tube_result",
    "verify_target_causal_tube_parent_evidence",
]
