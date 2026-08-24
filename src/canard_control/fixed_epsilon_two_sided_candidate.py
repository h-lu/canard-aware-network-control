"""Two-sided full-history-matched candidate at fixed epsilon.

This module advances the fixed-epsilon blueprint by solving an actual split
discrete boundary-value residual.  A left trace is launched from one smooth,
parameter-coherent finite-section entry template, a right trace is matched to
the complete represented history at the phase section, and a scalar exit
observable is set to zero.  The square system is solved by sparse Newton and
its full discrete left adjoint is computed.

The calculation deliberately stops short of a selected-root theorem.  The
entry template is not a validated attracting trace bundle, and the scalar
exit observable is not the codimension-(history dimension minus one)
backward-extendible repelling trace bundle required by the Fredholm BVP.
All arithmetic is binary64 and no interval inverse or tail estimate is used.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from functools import lru_cache
from hashlib import sha256
import math
from typing import Any, Mapping

import numpy as np
from numpy.typing import NDArray
from scipy.integrate import solve_ivp
from scipy.optimize import root
from scipy.sparse import csc_matrix, lil_matrix
from scipy.sparse.linalg import splu

from .fixed_epsilon_quadratic_root_bvp import (
    DELTA,
    MODEL_ID,
    PERIOD_DIAGNOSTIC,
    THETA_PERIOD_DIAGNOSTIC,
)


BLUEPRINT_SOURCE_SHA256 = (
    "03423f924baa23afc8a1c5093392f67836af7864cc37e1b47aa7f7c30c1f36c4"
)
BLUEPRINT_RESULT_SHA256 = (
    "1af8aa46b31bb099a8f07e7646b656577d010dc413094ad3be0afb32c70c993a"
)
BLUEPRINT_NOTE_SHA256 = (
    "f3a32e08104d28d06b4e3f7a83308126d318e2bc38026ab39cd0d65a389b9b63"
)


@dataclass(frozen=True)
class TwoSidedCandidateRow:
    """One converged split-history trapezoidal candidate."""

    section_half_width: float
    mesh_per_scaled_time: int
    mesh_step: float
    physical_history_diagnostic: float
    active_scaled_history: float
    represented_scaled_history: float
    history_rounding_excess: float
    full_dimension: int
    complete_history_node_count: int
    q_candidate: float
    nu_candidate: float
    a_candidate: float
    total_residual_inf: float
    entry_residual_inf: float
    entry_solution_manifold_compatibility_defect: float
    left_flow_residual_inf: float
    phase_residual: float
    complete_history_jump_inf: float
    right_flow_residual_inf: float
    exit_gap_residual: float
    newton_iterations: int
    minimum_lu_pivot: float
    adjoint_residual_inf: float
    adjoint_normalization_error: float
    discrete_m_eta: float
    discrete_m_nu: float
    rho_adjoint_candidate: float
    rho_direct_tangent_candidate: float
    adjoint_direct_disagreement: float
    eta_finite_difference_step: float
    rho_finite_difference_candidate: float
    adjoint_finite_difference_disagreement: float


@dataclass(frozen=True)
class TwoSidedCandidateCertificate:
    """Aggregate diagnostics together with non-promotion gates."""

    model_id: str
    arithmetic: str
    discretization: str
    blueprint_source_sha256: str
    blueprint_result_sha256: str
    blueprint_note_sha256: str
    central_section_half_width: str
    finest_mesh_per_scaled_time: int
    finest_nu_candidate: str
    finest_a_candidate: str
    finest_rho_candidate: str
    maximum_candidate_residual_inf: str
    maximum_jump_residual_inf: str
    maximum_entry_compatibility_defect: str
    maximum_adjoint_residual_inf: str
    maximum_adjoint_direct_disagreement: str
    maximum_adjoint_finite_difference_disagreement: str
    central_mesh_nu_spread: str
    central_mesh_rho_spread: str
    central_nu_refinement_ratio: str
    central_rho_refinement_ratio: str
    section_nu_spread: str
    section_rho_spread: str
    two_branch_discrete_candidate_computed: bool
    parameter_coherent_entry_template_used: bool
    entry_solution_manifold_compatibility_enforced: bool
    phase_solved: bool
    full_discrete_history_jump_solved: bool
    finite_exit_observable_zero: bool
    square_candidate_residual_solved: bool
    discrete_full_residual_adjoint_computed: bool
    local_eta_continuation_diagnostic_computed: bool
    selected_attracting_trace_bundle_constructed: bool
    backward_extendible_repelling_bundle_constructed: bool
    correct_fredholm_endpoint_chart_count_implemented: bool
    selected_complete_history_bvp_solved: bool
    continuous_collocation_solution_validated: bool
    interval_inverse_or_tail_bound_validated: bool
    period_delay_uncertainty_propagated: bool
    continuous_advanced_adjoint_validated: bool
    singular_to_fixed_epsilon_trace_bundle_continuation_completed: bool
    candidate_branch_uniqueness_established: bool
    fixed_epsilon_selected_root_validated: bool
    rho_star_enclosed_away_from_zero: bool
    physical_onset_or_capture_validated: bool
    minimal_failure: str


@dataclass
class _Layout:
    section: float
    mesh_per_unit: int
    step: float
    history_steps: int
    flight_steps: int
    nodes_per_branch: int
    left_offset: int
    right_offset: int
    q_column: int
    nu_column: int
    dimension: int
    entry_slice: slice
    left_flow_slice: slice
    phase_index: int
    jump_slice: slice
    right_flow_slice: slice
    exit_index: int


@dataclass
class _SystemEvaluation:
    residual: NDArray[np.float64]
    jacobian: csc_matrix
    eta_column: NDArray[np.float64]
    layout: _Layout


def _layout(section: float, mesh_per_unit: int) -> _Layout:
    if section <= 0.0:
        raise ValueError("section_half_width must be positive")
    if mesh_per_unit <= 0:
        raise ValueError("mesh_per_scaled_time must be positive")
    rounded_flight = round(section * mesh_per_unit)
    if abs(rounded_flight / mesh_per_unit - section) > 2.0e-14:
        raise ValueError("the section must align with the uniform mesh")
    history_steps = int(math.ceil(THETA_PERIOD_DIAGNOSTIC * mesh_per_unit))
    flight_steps = int(rounded_flight)
    nodes = history_steps + flight_steps + 1
    state_dimension = 4 * nodes
    q_column = state_dimension
    nu_column = state_dimension + 1
    dimension = state_dimension + 2
    cursor = 0
    entry = slice(cursor, cursor + 2 * (history_steps + 1))
    cursor = entry.stop
    left_flow = slice(cursor, cursor + 2 * flight_steps)
    cursor = left_flow.stop
    phase_index = cursor
    cursor += 1
    jump = slice(cursor, cursor + 2 * (history_steps + 1))
    cursor = jump.stop
    right_flow = slice(cursor, cursor + 2 * flight_steps)
    cursor = right_flow.stop
    exit_index = cursor
    cursor += 1
    if cursor != dimension:
        raise RuntimeError("the split-history residual is not square")
    return _Layout(
        section=float(section),
        mesh_per_unit=int(mesh_per_unit),
        step=1.0 / mesh_per_unit,
        history_steps=history_steps,
        flight_steps=flight_steps,
        nodes_per_branch=nodes,
        left_offset=0,
        right_offset=2 * nodes,
        q_column=q_column,
        nu_column=nu_column,
        dimension=dimension,
        entry_slice=entry,
        left_flow_slice=left_flow,
        phase_index=phase_index,
        jump_slice=jump,
        right_flow_slice=right_flow,
        exit_index=exit_index,
    )


def _entry_template(
    time: float,
    q_value: float,
    nu_value: float,
    section: float,
    eta: float,
) -> NDArray[np.float64]:
    shifted = time + q_value
    compatibility_shift, _, _ = _entry_compatibility_shift(
        q_value, eta, section
    )
    return np.asarray(
        [
            -shifted / 2.0,
            (shifted * shifted - 2.0) / 4.0
            + DELTA * nu_value * (time + section)
            + compatibility_shift,
        ],
        dtype=float,
    )


def _entry_template_columns(
    time: float, q_value: float, section: float, eta: float
) -> tuple[
    NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]
]:
    shifted = time + q_value
    _, shift_q, shift_eta = _entry_compatibility_shift(
        q_value, eta, section
    )
    q_column = np.asarray([-0.5, shifted / 2.0 + shift_q], dtype=float)
    nu_column = np.asarray([0.0, DELTA * (time + section)], dtype=float)
    eta_column = np.asarray([0.0, shift_eta], dtype=float)
    return q_column, nu_column, eta_column


def _entry_compatibility_shift(
    q_value: float, eta: float, section: float
) -> tuple[float, float, float]:
    """Return the constant Y shift enforcing entry compatibility.

    The unshifted singular template already satisfies both chart equations
    at delta=0.  At the finite delta, its X derivative remains -1/2.  Since
    the fast field is affine in Y, one constant shift cancels all finite-delta
    corrections at the current endpoint t=-section.  The slow compatibility
    equation remains exact because the shift is constant in history time.
    """

    x0 = (section - q_value) / 2.0
    x4 = (section + 4.0 - q_value) / 2.0
    x5 = (section + 5.0 - q_value) / 2.0
    xt = (section + THETA_PERIOD_DIAGNOSTIC - q_value) / 2.0
    correction = (
        DELTA * (-x0**3 / 3.0 + 0.2 * ((x4 + x5) / 2.0 - x0))
        + DELTA**2 * eta * (x0 * x0 - xt * xt)
        + DELTA**3 * 0.25 * ((x4**3 + x5**3) / 2.0 - x0**3)
    )
    correction_q = (
        0.5 * DELTA * x0 * x0
        + DELTA**2 * eta * (xt - x0)
        + DELTA**3
        * 0.25
        * (1.5 * x0 * x0 - 0.75 * (x4 * x4 + x5 * x5))
    )
    correction_eta = DELTA**2 * (x0 * x0 - xt * xt)
    return -correction, -correction_q, -correction_eta


def _entry_compatibility_defect(
    q_value: float, nu_value: float, eta: float, section: float
) -> float:
    """Evaluate both solution-manifold compatibility equations."""

    current_time = -section
    current = _entry_template(
        current_time, q_value, nu_value, section, eta
    )
    x4 = _entry_template(
        current_time - 4.0, q_value, nu_value, section, eta
    )[0]
    x5 = _entry_template(
        current_time - 5.0, q_value, nu_value, section, eta
    )[0]
    xt = _entry_template(
        current_time - THETA_PERIOD_DIAGNOSTIC,
        q_value,
        nu_value,
        section,
        eta,
    )[0]
    x_value, y_value = map(float, current)
    fast = (
        y_value
        - x_value * x_value
        + DELTA * (-x_value**3 / 3.0 + 0.2 * ((x4 + x5) / 2.0 - x_value))
        + DELTA**2 * eta * (x_value * x_value - xt * xt)
        + DELTA**3 * 0.25 * ((x4**3 + x5**3) / 2.0 - x_value**3)
    )
    shifted = current_time + q_value
    history_derivative = np.asarray(
        [-0.5, shifted / 2.0 + DELTA * nu_value], dtype=float
    )
    field = np.asarray([fast, -x_value + DELTA * nu_value], dtype=float)
    return float(np.max(np.abs(history_derivative - field)))


def _continuous_seed(
    section: float,
    eta: float,
    initial_q_nu: tuple[float, float] = (0.4, 0.13),
) -> tuple[float, float, Any]:
    """Solve the two scalar seed conditions by method of steps."""

    start = -section

    def integrate(q_value: float, nu_value: float) -> Any:
        initial = _entry_template(start, q_value, nu_value, section, eta)
        completed: list[tuple[float, float, Any]] = []
        left = start

        def known(time: float) -> NDArray[np.float64]:
            tolerance = 2.0e-10 * max(1.0, abs(time), abs(left))
            if time <= start + tolerance:
                return _entry_template(
                    time, q_value, nu_value, section, eta
                )
            for lower, upper, interpolant in reversed(completed):
                if lower - tolerance <= time <= upper + tolerance:
                    clipped = min(max(time, lower), upper)
                    return np.asarray(interpolant(clipped), dtype=float)
            raise RuntimeError("continuous seed queried unfinished history")

        while left < section - 1.0e-14:
            right = min(section, left + 4.0)

            def rhs(time: float, state: NDArray[np.float64]) -> NDArray[np.float64]:
                delayed_4 = known(time - 4.0)[0]
                delayed_5 = known(time - 5.0)[0]
                delayed_period = known(time - THETA_PERIOD_DIAGNOSTIC)[0]
                x_value, y_value = state
                fast = (
                    y_value
                    - x_value * x_value
                    + DELTA
                    * (
                        -x_value**3 / 3.0
                        + 0.2 * ((delayed_4 + delayed_5) / 2.0 - x_value)
                    )
                    + DELTA**2
                    * eta
                    * (x_value * x_value - delayed_period * delayed_period)
                    + DELTA**3
                    * 0.25
                    * (
                        (delayed_4**3 + delayed_5**3) / 2.0
                        - x_value**3
                    )
                )
                return np.asarray(
                    [fast, -x_value + DELTA * nu_value], dtype=float
                )

            solution = solve_ivp(
                rhs,
                (left, right),
                initial,
                method="DOP853",
                dense_output=True,
                rtol=2.0e-11,
                atol=2.0e-13,
                max_step=0.025,
            )
            if not solution.success or solution.sol is None:
                raise RuntimeError(f"continuous seed failed: {solution.message}")
            completed.append((left, right, solution.sol))
            initial = np.asarray(solution.y[:, -1], dtype=float)
            left = right

        def value(time: float) -> NDArray[np.float64]:
            if time <= start:
                return _entry_template(
                    time, q_value, nu_value, section, eta
                )
            for lower, upper, interpolant in completed:
                if lower - 2.0e-10 <= time <= upper + 2.0e-10:
                    clipped = min(max(time, lower), upper)
                    return np.asarray(interpolant(clipped), dtype=float)
            if abs(time - section) <= 2.0e-10:
                return initial.copy()
            raise RuntimeError("continuous seed evaluation is out of range")

        return value

    def endpoint_residual(values: NDArray[np.float64]) -> NDArray[np.float64]:
        value = integrate(float(values[0]), float(values[1]))
        phase_state = value(0.0)
        exit_state = value(section)
        gap = exit_state[0] ** 2 / 2.0 - exit_state[1] / 2.0 - 0.25
        return np.asarray([phase_state[0], gap], dtype=float)

    solved = root(endpoint_residual, np.asarray(initial_q_nu, dtype=float))
    if not solved.success or np.max(np.abs(solved.fun)) > 2.0e-9:
        raise RuntimeError(f"continuous seed root failed: {solved.message}")
    q_value, nu_value = map(float, solved.x)
    return q_value, nu_value, integrate(q_value, nu_value)


def _split_state(
    vector: NDArray[np.float64], layout: _Layout
) -> tuple[NDArray[np.float64], NDArray[np.float64], float, float]:
    nodes = layout.nodes_per_branch
    left = vector[: 2 * nodes].reshape((nodes, 2))
    right = vector[2 * nodes : 4 * nodes].reshape((nodes, 2))
    return left, right, float(vector[layout.q_column]), float(
        vector[layout.nu_column]
    )


def _initial_vector(
    section: float, mesh_per_unit: int, eta: float
) -> NDArray[np.float64]:
    layout = _layout(section, mesh_per_unit)
    q_value, nu_value, continuous = _continuous_seed(section, eta)
    represented_history = layout.history_steps * layout.step
    left_times = (
        -section
        - represented_history
        + layout.step * np.arange(layout.nodes_per_branch)
    )
    right_times = (
        -represented_history
        + layout.step * np.arange(layout.nodes_per_branch)
    )
    left = np.vstack([continuous(float(time)) for time in left_times])
    right = np.vstack([continuous(float(time)) for time in right_times])
    return np.concatenate((left.ravel(), right.ravel(), [q_value, nu_value]))


def _trace_variable(layout: _Layout, branch: str, node: int, component: int) -> int:
    offset = layout.left_offset if branch == "left" else layout.right_offset
    return offset + 2 * node + component


def _period_interpolation(
    trace: NDArray[np.float64], node: int, layout: _Layout
) -> tuple[float, tuple[tuple[int, float], ...]]:
    offset = THETA_PERIOD_DIAGNOSTIC / layout.step
    integer = int(math.floor(offset))
    fraction = float(offset - integer)
    upper = node - integer
    if fraction <= 2.0e-13:
        if upper < 0:
            raise RuntimeError("represented history does not contain period delay")
        return float(trace[upper, 0]), ((upper, 1.0),)
    lower = upper - 1
    if lower < 0:
        raise RuntimeError("represented history does not contain period delay")
    weights = ((lower, fraction), (upper, 1.0 - fraction))
    value = sum(weight * float(trace[index, 0]) for index, weight in weights)
    return value, weights


def _field_partials(
    trace: NDArray[np.float64],
    node: int,
    nu_value: float,
    eta: float,
    layout: _Layout,
) -> tuple[
    NDArray[np.float64],
    NDArray[np.float64],
    tuple[tuple[int, NDArray[np.float64]], ...],
    NDArray[np.float64],
    NDArray[np.float64],
]:
    delay_4_node = node - 4 * layout.mesh_per_unit
    delay_5_node = node - 5 * layout.mesh_per_unit
    if delay_4_node < 0 or delay_5_node < 0:
        raise RuntimeError("represented history does not contain fixed delays")
    x_value, y_value = map(float, trace[node])
    x4 = float(trace[delay_4_node, 0])
    x5 = float(trace[delay_5_node, 0])
    xt, period_weights = _period_interpolation(trace, node, layout)
    fast = (
        y_value
        - x_value * x_value
        + DELTA * (-x_value**3 / 3.0 + 0.2 * ((x4 + x5) / 2.0 - x_value))
        + DELTA**2 * eta * (x_value * x_value - xt * xt)
        + DELTA**3 * 0.25 * ((x4**3 + x5**3) / 2.0 - x_value**3)
    )
    field = np.asarray([fast, -x_value + DELTA * nu_value], dtype=float)
    current = np.asarray(
        [
            [
                -2.0 * x_value
                + DELTA * (-x_value * x_value - 0.2)
                + 2.0 * DELTA**2 * eta * x_value
                - 0.75 * DELTA**3 * x_value * x_value,
                1.0,
            ],
            [-1.0, 0.0],
        ],
        dtype=float,
    )
    delayed: list[tuple[int, NDArray[np.float64]]] = []
    for delay_node, delayed_value in (
        (delay_4_node, x4),
        (delay_5_node, x5),
    ):
        coefficient = DELTA * 0.1 + DELTA**3 * 0.375 * delayed_value**2
        delayed.append(
            (
                delay_node,
                np.asarray([[coefficient, 0.0], [0.0, 0.0]], dtype=float),
            )
        )
    if eta != 0.0:
        for period_node, weight in period_weights:
            coefficient = -2.0 * DELTA**2 * eta * xt * weight
            delayed.append(
                (
                    period_node,
                    np.asarray(
                        [[coefficient, 0.0], [0.0, 0.0]], dtype=float
                    ),
                )
            )
    eta_column = np.asarray(
        [DELTA**2 * (x_value * x_value - xt * xt), 0.0], dtype=float
    )
    nu_column = np.asarray([0.0, DELTA], dtype=float)
    return field, current, tuple(delayed), eta_column, nu_column


def _evaluate_system(
    vector: NDArray[np.float64],
    section: float,
    mesh_per_unit: int,
    eta: float,
) -> _SystemEvaluation:
    layout = _layout(section, mesh_per_unit)
    if vector.shape != (layout.dimension,):
        raise ValueError("candidate vector has the wrong dimension")
    left, right, q_value, nu_value = _split_state(vector, layout)
    residual = np.zeros(layout.dimension, dtype=float)
    eta_column = np.zeros(layout.dimension, dtype=float)
    jacobian = lil_matrix((layout.dimension, layout.dimension), dtype=float)
    represented_history = layout.history_steps * layout.step

    row = layout.entry_slice.start
    for node in range(layout.history_steps + 1):
        time = -section - represented_history + node * layout.step
        target = _entry_template(time, q_value, nu_value, section, eta)
        q_target, nu_target, eta_target = _entry_template_columns(
            time, q_value, section, eta
        )
        for component in range(2):
            residual[row] = left[node, component] - target[component]
            jacobian[row, _trace_variable(layout, "left", node, component)] = 1.0
            jacobian[row, layout.q_column] = -q_target[component]
            jacobian[row, layout.nu_column] = -nu_target[component]
            eta_column[row] = -eta_target[component]
            row += 1
    if row != layout.entry_slice.stop:
        raise RuntimeError("entry block count drifted")

    def add_flow_block(
        branch: str,
        trace: NDArray[np.float64],
        first_row: int,
    ) -> int:
        flow_row = first_row
        for node in range(layout.history_steps, layout.nodes_per_branch - 1):
            endpoint_data = (
                _field_partials(trace, node, nu_value, eta, layout),
                _field_partials(trace, node + 1, nu_value, eta, layout),
            )
            residual[flow_row : flow_row + 2] = (
                (trace[node + 1] - trace[node]) / layout.step
                - 0.5 * (endpoint_data[0][0] + endpoint_data[1][0])
            )
            eta_column[flow_row : flow_row + 2] = -0.5 * (
                endpoint_data[0][3] + endpoint_data[1][3]
            )
            for endpoint, sign in ((node, -1.0), (node + 1, 1.0)):
                data = endpoint_data[0] if endpoint == node else endpoint_data[1]
                current = sign * np.eye(2) / layout.step - 0.5 * data[1]
                for output_component in range(2):
                    for input_component in range(2):
                        jacobian[
                            flow_row + output_component,
                            _trace_variable(
                                layout, branch, endpoint, input_component
                            ),
                        ] += current[output_component, input_component]
                for delayed_node, delayed_matrix in data[2]:
                    for output_component in range(2):
                        for input_component in range(2):
                            jacobian[
                                flow_row + output_component,
                                _trace_variable(
                                    layout,
                                    branch,
                                    delayed_node,
                                    input_component,
                                ),
                            ] += -0.5 * delayed_matrix[
                                output_component, input_component
                            ]
                for output_component in range(2):
                    jacobian[
                        flow_row + output_component, layout.nu_column
                    ] += -0.5 * data[4][output_component]
            flow_row += 2
        return flow_row

    row = add_flow_block("left", left, layout.left_flow_slice.start)
    if row != layout.left_flow_slice.stop:
        raise RuntimeError("left flow block count drifted")

    residual[layout.phase_index] = left[-1, 0]
    jacobian[
        layout.phase_index,
        _trace_variable(layout, "left", layout.nodes_per_branch - 1, 0),
    ] = 1.0

    row = layout.jump_slice.start
    left_jump_start = layout.flight_steps
    for node in range(layout.history_steps + 1):
        left_node = left_jump_start + node
        for component in range(2):
            residual[row] = right[node, component] - left[left_node, component]
            jacobian[
                row, _trace_variable(layout, "right", node, component)
            ] = 1.0
            jacobian[
                row, _trace_variable(layout, "left", left_node, component)
            ] = -1.0
            row += 1
    if row != layout.jump_slice.stop:
        raise RuntimeError("jump block count drifted")

    row = add_flow_block("right", right, layout.right_flow_slice.start)
    if row != layout.right_flow_slice.stop:
        raise RuntimeError("right flow block count drifted")

    exit_state = right[-1]
    residual[layout.exit_index] = (
        exit_state[0] ** 2 / 2.0 - exit_state[1] / 2.0 - 0.25
    )
    jacobian[
        layout.exit_index,
        _trace_variable(layout, "right", layout.nodes_per_branch - 1, 0),
    ] = exit_state[0]
    jacobian[
        layout.exit_index,
        _trace_variable(layout, "right", layout.nodes_per_branch - 1, 1),
    ] = -0.5
    return _SystemEvaluation(
        residual=residual,
        jacobian=jacobian.tocsc(),
        eta_column=eta_column,
        layout=layout,
    )


def _newton_solve(
    section: float,
    mesh_per_unit: int,
    eta: float,
    initial: NDArray[np.float64] | None = None,
) -> tuple[NDArray[np.float64], _SystemEvaluation, int, float]:
    vector = (
        _initial_vector(section, mesh_per_unit, eta)
        if initial is None
        else np.asarray(initial, dtype=float).copy()
    )
    layout = _layout(section, mesh_per_unit)
    if vector.shape != (layout.dimension,):
        raise ValueError("Newton initial vector has the wrong dimension")
    iterations = 0
    for iterations in range(13):
        evaluation = _evaluate_system(vector, section, mesh_per_unit, eta)
        residual_norm = float(np.max(np.abs(evaluation.residual)))
        if residual_norm < 3.0e-11:
            break
        factor = splu(evaluation.jacobian)
        correction = factor.solve(-evaluation.residual)
        if not np.all(np.isfinite(correction)):
            raise RuntimeError("Newton correction is nonfinite")
        accepted = False
        step_scale = 1.0
        for _ in range(12):
            trial = vector + step_scale * correction
            trial_evaluation = _evaluate_system(
                trial, section, mesh_per_unit, eta
            )
            trial_norm = float(np.max(np.abs(trial_evaluation.residual)))
            if trial_norm < residual_norm:
                vector = trial
                accepted = True
                break
            step_scale *= 0.5
        if not accepted:
            raise RuntimeError("sparse Newton line search failed")
    evaluation = _evaluate_system(vector, section, mesh_per_unit, eta)
    residual_norm = float(np.max(np.abs(evaluation.residual)))
    if residual_norm >= 3.0e-10:
        raise RuntimeError(
            f"split-history Newton did not converge: residual {residual_norm}"
        )
    factor = splu(evaluation.jacobian)
    minimum_pivot = float(np.min(np.abs(factor.U.diagonal())))
    return vector, evaluation, iterations, minimum_pivot


def compute_two_sided_candidate_row(
    section_half_width: float,
    mesh_per_scaled_time: int,
    *,
    eta_difference_step: float = 2.0e-4,
) -> TwoSidedCandidateRow:
    """Compute one candidate, its discrete adjoint, and an eta check."""

    section = float(section_half_width)
    mesh = int(mesh_per_scaled_time)
    vector, evaluation, iterations, minimum_pivot = _newton_solve(
        section, mesh, 0.0
    )
    layout = evaluation.layout
    factor = splu(evaluation.jacobian)
    tangent = factor.solve(-evaluation.eta_column)
    direct_rho = DELTA**2 * float(tangent[layout.nu_column])

    normalization_target = np.zeros(layout.dimension, dtype=float)
    normalization_target[layout.nu_column] = 1.0
    adjoint = factor.solve(normalization_target, trans="T")
    jacobian_without_nu = evaluation.jacobian[:, : layout.nu_column]
    nu_column = np.asarray(
        evaluation.jacobian[:, layout.nu_column].toarray()
    ).ravel()
    adjoint_residual = float(
        np.max(np.abs(jacobian_without_nu.T @ adjoint))
    )
    m_nu = float(adjoint @ nu_column)
    normalization_error = abs(m_nu - 1.0)
    m_eta = float(adjoint @ evaluation.eta_column)
    adjoint_rho = DELTA**2 * (-m_eta / m_nu)

    step = float(eta_difference_step)
    if step <= 0.0:
        raise ValueError("eta_difference_step must be positive")
    plus, _, _, _ = _newton_solve(section, mesh, step, vector)
    minus, _, _, _ = _newton_solve(section, mesh, -step, vector)
    plus_nu = float(plus[layout.nu_column])
    minus_nu = float(minus[layout.nu_column])
    finite_difference_rho = DELTA**2 * (plus_nu - minus_nu) / (2.0 * step)

    left, right, q_value, nu_value = _split_state(vector, layout)
    residual = evaluation.residual
    return TwoSidedCandidateRow(
        section_half_width=section,
        mesh_per_scaled_time=mesh,
        mesh_step=layout.step,
        physical_history_diagnostic=PERIOD_DIAGNOSTIC,
        active_scaled_history=THETA_PERIOD_DIAGNOSTIC,
        represented_scaled_history=layout.history_steps * layout.step,
        history_rounding_excess=(
            layout.history_steps * layout.step - THETA_PERIOD_DIAGNOSTIC
        ),
        full_dimension=layout.dimension,
        complete_history_node_count=layout.history_steps + 1,
        q_candidate=q_value,
        nu_candidate=nu_value,
        a_candidate=1.0 + DELTA**2 * nu_value,
        total_residual_inf=float(np.max(np.abs(residual))),
        entry_residual_inf=float(
            np.max(np.abs(residual[layout.entry_slice]))
        ),
        entry_solution_manifold_compatibility_defect=(
            _entry_compatibility_defect(q_value, nu_value, 0.0, section)
        ),
        left_flow_residual_inf=float(
            np.max(np.abs(residual[layout.left_flow_slice]))
        ),
        phase_residual=float(residual[layout.phase_index]),
        complete_history_jump_inf=float(
            np.max(np.abs(residual[layout.jump_slice]))
        ),
        right_flow_residual_inf=float(
            np.max(np.abs(residual[layout.right_flow_slice]))
        ),
        exit_gap_residual=float(residual[layout.exit_index]),
        newton_iterations=iterations,
        minimum_lu_pivot=minimum_pivot,
        adjoint_residual_inf=adjoint_residual,
        adjoint_normalization_error=normalization_error,
        discrete_m_eta=m_eta,
        discrete_m_nu=m_nu,
        rho_adjoint_candidate=adjoint_rho,
        rho_direct_tangent_candidate=direct_rho,
        adjoint_direct_disagreement=abs(adjoint_rho - direct_rho),
        eta_finite_difference_step=step,
        rho_finite_difference_candidate=float(finite_difference_rho),
        adjoint_finite_difference_disagreement=abs(
            adjoint_rho - finite_difference_rho
        ),
    )


@lru_cache(maxsize=1)
def reference_two_sided_candidate_rows() -> tuple[TwoSidedCandidateRow, ...]:
    """Return a central mesh study and a fixed-mesh section study."""

    specifications = (
        (3.0, 8),
        (3.0, 16),
        (3.0, 32),
        (2.5, 16),
        (3.5, 16),
    )
    return tuple(
        compute_two_sided_candidate_row(section, mesh)
        for section, mesh in specifications
    )


def _format(value: float) -> str:
    return format(float(value), ".17g")


def reference_two_sided_candidate_certificate(
) -> TwoSidedCandidateCertificate:
    """Build aggregate diagnostics without promoting the selected BVP."""

    rows = reference_two_sided_candidate_rows()
    central = [row for row in rows if row.section_half_width == 3.0]
    central.sort(key=lambda row: row.mesh_per_scaled_time)
    sections = [row for row in rows if row.mesh_per_scaled_time == 16]
    finest = max(central, key=lambda row: row.mesh_per_scaled_time)
    nu_ratio = abs(central[0].nu_candidate - central[1].nu_candidate) / abs(
        central[1].nu_candidate - central[2].nu_candidate
    )
    rho_ratio = abs(
        central[0].rho_adjoint_candidate - central[1].rho_adjoint_candidate
    ) / abs(
        central[1].rho_adjoint_candidate - central[2].rho_adjoint_candidate
    )
    return TwoSidedCandidateCertificate(
        model_id=MODEL_ID,
        arithmetic="binary64 SciPy sparse Newton and discrete adjoint; no intervals",
        discretization=(
            "uniform trapezoidal left/right RFDE traces; linear period-delay "
            "interpolation; nodewise complete-history jump"
        ),
        blueprint_source_sha256=BLUEPRINT_SOURCE_SHA256,
        blueprint_result_sha256=BLUEPRINT_RESULT_SHA256,
        blueprint_note_sha256=BLUEPRINT_NOTE_SHA256,
        central_section_half_width="3",
        finest_mesh_per_scaled_time=finest.mesh_per_scaled_time,
        finest_nu_candidate=_format(finest.nu_candidate),
        finest_a_candidate=_format(finest.a_candidate),
        finest_rho_candidate=_format(finest.rho_adjoint_candidate),
        maximum_candidate_residual_inf=_format(
            max(row.total_residual_inf for row in rows)
        ),
        maximum_jump_residual_inf=_format(
            max(row.complete_history_jump_inf for row in rows)
        ),
        maximum_entry_compatibility_defect=_format(
            max(
                row.entry_solution_manifold_compatibility_defect
                for row in rows
            )
        ),
        maximum_adjoint_residual_inf=_format(
            max(row.adjoint_residual_inf for row in rows)
        ),
        maximum_adjoint_direct_disagreement=_format(
            max(row.adjoint_direct_disagreement for row in rows)
        ),
        maximum_adjoint_finite_difference_disagreement=_format(
            max(row.adjoint_finite_difference_disagreement for row in rows)
        ),
        central_mesh_nu_spread=_format(
            max(row.nu_candidate for row in central)
            - min(row.nu_candidate for row in central)
        ),
        central_mesh_rho_spread=_format(
            max(row.rho_adjoint_candidate for row in central)
            - min(row.rho_adjoint_candidate for row in central)
        ),
        central_nu_refinement_ratio=_format(nu_ratio),
        central_rho_refinement_ratio=_format(rho_ratio),
        section_nu_spread=_format(
            max(row.nu_candidate for row in sections)
            - min(row.nu_candidate for row in sections)
        ),
        section_rho_spread=_format(
            max(row.rho_adjoint_candidate for row in sections)
            - min(row.rho_adjoint_candidate for row in sections)
        ),
        two_branch_discrete_candidate_computed=True,
        parameter_coherent_entry_template_used=True,
        entry_solution_manifold_compatibility_enforced=True,
        phase_solved=True,
        full_discrete_history_jump_solved=True,
        finite_exit_observable_zero=True,
        square_candidate_residual_solved=True,
        discrete_full_residual_adjoint_computed=True,
        local_eta_continuation_diagnostic_computed=True,
        selected_attracting_trace_bundle_constructed=False,
        backward_extendible_repelling_bundle_constructed=False,
        correct_fredholm_endpoint_chart_count_implemented=False,
        selected_complete_history_bvp_solved=False,
        continuous_collocation_solution_validated=False,
        interval_inverse_or_tail_bound_validated=False,
        period_delay_uncertainty_propagated=False,
        continuous_advanced_adjoint_validated=False,
        singular_to_fixed_epsilon_trace_bundle_continuation_completed=False,
        candidate_branch_uniqueness_established=False,
        fixed_epsilon_selected_root_validated=False,
        rho_star_enclosed_away_from_zero=False,
        physical_onset_or_capture_validated=False,
        minimal_failure=(
            "replace the artificial full entry template and scalar G=0 exit "
            "by a 193-dimensional attracting endpoint chart and a "
            "one-dimensional terminal-collocation repelling chart on the "
            "194-dimensional represented history; then validate the "
            "775x774 Fredholm derivative, its jump complement, and tails"
        ),
    )


@lru_cache(maxsize=1)
def _reference_finest_primal_adjoint(
) -> tuple[tuple[float, ...], tuple[float, ...]]:
    """Return every component of the finest pinned primal and adjoint."""

    vector, evaluation, _, _ = _newton_solve(3.0, 32, 0.0)
    factor = splu(evaluation.jacobian)
    target = np.zeros(evaluation.layout.dimension, dtype=float)
    target[evaluation.layout.nu_column] = 1.0
    adjoint = factor.solve(target, trans="T")
    return tuple(map(float, vector)), tuple(map(float, adjoint))


def _binary64_digest(values: tuple[float, ...]) -> str:
    array = np.asarray(values, dtype="<f8")
    return sha256(array.tobytes(order="C")).hexdigest()


def reference_two_sided_candidate_payload() -> dict[str, Any]:
    """Return the deterministic candidate and refusal record."""

    primal, adjoint = _reference_finest_primal_adjoint()
    return {
        "schema_version": 1,
        "model_id": MODEL_ID,
        "rows": [asdict(row) for row in reference_two_sided_candidate_rows()],
        "certificate": asdict(reference_two_sided_candidate_certificate()),
        "finest_primal_and_adjoint_candidate": {
            "section_half_width": 3,
            "mesh_per_scaled_time": 32,
            "dimension": len(primal),
            "unknown_order": (
                "left interleaved (X,Y), right interleaved (X,Y), q, nu"
            ),
            "adjoint_order": "entry, left flow, phase, jump, right flow, exit",
            "adjoint_normalization": (
                "J_u^T psi=0 and psi^T partial_nu(F)=1"
            ),
            "primal_binary64_sha256": _binary64_digest(primal),
            "adjoint_binary64_sha256": _binary64_digest(adjoint),
            "primal_components": list(primal),
            "adjoint_components": list(adjoint),
        },
        "faithful_next_discretization": {
            "section_half_widths": [3, 3],
            "scaled_history": _format(THETA_PERIOD_DIAGNOSTIC),
            "history_dimension": 194,
            "attracting_endpoint_chart_dimension": 193,
            "repelling_endpoint_chart_dimension": 1,
            "phase_fixed_residual_dimension": 775,
            "phase_fixed_unknown_dimension": 774,
            "jump_complement_square_dimension": 775,
            "root_system_square_dimension": 776,
            "terminal_repelling_chart_requires_collocation_continuation": True,
            "backward_ivp_is_not_an_admissible_substitute": True,
        },
        "scope": {
            "actual_two_branch_numerical_candidate": True,
            "entry_solution_manifold_compatibility_at_template_current": True,
            "nodewise_complete_history_match": True,
            "discrete_adjoint_candidate": True,
            "local_eta_continuation_diagnostic": True,
            "selected_attracting_bundle": False,
            "backward_extendible_repelling_bundle": False,
            "selected_complete_history_bvp": False,
            "interval_validation": False,
            "selected_root": False,
            "rho_enclosure": False,
            "candidate_branch_uniqueness": False,
            "physical_onset_or_capture": False,
        },
    }


def validate_two_sided_candidate_payload(payload: Mapping[str, Any]) -> None:
    """Reject mutation or promotion of the pinned numerical candidate."""

    if dict(payload) != reference_two_sided_candidate_payload():
        raise ValueError(
            "two-sided fixed-epsilon candidate payload does not match the "
            "pinned numerical computation and claim refusals"
        )


__all__ = [
    "BLUEPRINT_NOTE_SHA256",
    "BLUEPRINT_RESULT_SHA256",
    "BLUEPRINT_SOURCE_SHA256",
    "TwoSidedCandidateCertificate",
    "TwoSidedCandidateRow",
    "compute_two_sided_candidate_row",
    "reference_two_sided_candidate_certificate",
    "reference_two_sided_candidate_payload",
    "reference_two_sided_candidate_rows",
    "validate_two_sided_candidate_payload",
]
