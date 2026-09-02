"""Finite-section diagnostic for an explicit growing network family.

The calculation in this module is deliberately narrower than the analytical
results in Paper A.  It integrates the exact fold-coordinate RFDE from a
prescribed singular history and tunes a scalar outgoing-section mismatch to
zero.  Consequently, its roots are numerical diagnostics: they are not the
finite-interval matching function ``D_N^{fin}``, a stable/unstable manifold
intersection, a heteroclinic connection, or a maximal canard.

For every ``N >= 2`` the network family is

``pi_N = 1/N``, ``P_N = (1-rho) I + rho 1 pi_N^T``,

with a centered direction ``q_N`` normalized by
``pi_N^T q_N^2 = 1`` and curvature ``c_N = 1 + sigma q_N``.  The two delayed
layers are ``P_N/2 +/- zeta q_N pi_N^T`` at the strictly positive fold-time
delays 1 and 2.  The exact Fredholm coefficient is therefore
``-K sigma / (2 D rho)``, independently of ``N``.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Callable

import numpy as np
from numpy.typing import NDArray


State = NDArray[np.float64]


@dataclass(frozen=True)
class GrowingNetworkParameters:
    """Parameters for one member of the growing complete-mixing family."""

    node_count: int
    delta: float
    rho: float = 1.0
    sigma: float = 0.5
    beta: float = 3.0
    diffusion: float = 1.0
    coupling_gain: float = 2.0
    delay_0: float = 1.0
    delay_1: float = 2.0

    def __post_init__(self) -> None:
        if self.node_count < 2:
            raise ValueError("node_count must be at least two")
        if not self.delta > 0.0:
            raise ValueError("delta must be positive")
        if not 0.0 < self.rho <= 1.0:
            raise ValueError("require 0 < rho <= 1")
        if not 0.0 < self.sigma < 1.0 / np.sqrt(3.0):
            raise ValueError("require 0 < sigma < 1/sqrt(3)")
        if not self.beta > 0.0:
            raise ValueError("beta must be positive")
        if not self.diffusion > 0.0:
            raise ValueError("diffusion must be positive")
        if self.coupling_gain == 0.0:
            raise ValueError("coupling_gain must be nonzero")
        if not 0.0 < self.delay_0 < self.delay_1:
            raise ValueError("require 0 < delay_0 < delay_1")

    @property
    def delay_gap(self) -> float:
        """Return the separation of the two positive fold-time delays."""

        return self.delay_1 - self.delay_0

    @property
    def dobrushin_coefficient(self) -> float:
        """Return the exact Dobrushin coefficient of ``P_N``."""

        return 1.0 - self.rho

    @property
    def predicted_coefficient(self) -> float:
        """Return the dimension-independent Fredholm coefficient."""

        return (
            -self.coupling_gain
            * self.sigma
            * self.delay_gap
            / (2.0 * self.diffusion * self.rho)
        )

    @property
    def singular_center(self) -> float:
        """Return the leading fold root ``nu_0`` for this family."""

        kappa = (
            self.beta / 3.0
            - 2.0 * self.sigma**2 / (self.diffusion * self.rho)
        )
        return -3.0 * kappa / 8.0


@dataclass(frozen=True)
class IntegrationResult:
    """Exit data from one method-of-steps integration."""

    final_state: State
    exit_gap: float
    segment_count: int
    function_evaluations: int
    transverse_mean: float


@dataclass(frozen=True)
class SectionRoot:
    """One zero of the prescribed-history outgoing-section condition."""

    nu: float
    zeta: float
    residual: float
    bracket: tuple[float, float]
    orbit_integrations: int
    function_evaluations: int
    transverse_mean: float


@dataclass(frozen=True)
class NetworkSizeRow:
    """Centered response quotient for one network size."""

    node_count: int
    delta: float
    section_half_width: float
    zeta_step: float
    nu_minus: float
    nu_zero: float
    nu_plus: float
    quotient: float
    predicted_coefficient: float
    absolute_error: float
    relative_error: float
    root_residual_max: float
    transverse_mean_max: float
    orbit_integrations: int
    function_evaluations: int

    def as_dict(self) -> dict[str, int | float]:
        """Return a JSON-serializable representation."""

        return asdict(self)


def growing_direction(node_count: int) -> State:
    """Return the distinct centered direction ``q_N`` with mean square one."""

    if node_count < 2:
        raise ValueError("node_count must be at least two")
    indices = np.arange(1.0, node_count + 1.0)
    scale = np.sqrt(12.0 / (node_count**2 - 1.0))
    return scale * (indices - (node_count + 1.0) / 2.0)


def network_objects(
    parameters: GrowingNetworkParameters,
) -> tuple[State, State, State]:
    """Return ``(q_N,c_N,z_2,N)`` for the selected network size."""

    direction = growing_direction(parameters.node_count)
    curvature = np.ones(parameters.node_count) + parameters.sigma * direction
    graph_coefficient = (
        -parameters.sigma
        * direction
        / (parameters.diffusion * parameters.rho)
    )
    return direction, curvature, graph_coefficient


def singular_history(inner_time: float, node_count: int) -> State:
    """Return ``(X,Y,h)`` on the singular orbit with ``h=0``."""

    chart_x = -0.5 * inner_time
    chart_y = 0.25 * (inner_time**2 - 2.0)
    return np.concatenate(
        ([chart_x, chart_y], np.zeros(node_count, dtype=float))
    )


def normalized_exit_gap(state: State) -> float:
    """Return the zero factor of the singular first integral."""

    chart_x, chart_y = state[:2]
    return float(chart_y - chart_x**2 + 0.5)


def _collective_projection(vector: State) -> State:
    """Apply ``1 pi_N^T`` without constructing a dense matrix."""

    return np.full_like(vector, np.mean(vector))


def _transverse_projection(vector: State) -> State:
    """Apply ``I-1 pi_N^T`` without constructing a dense matrix."""

    return vector - np.mean(vector)


def _markov_action(vector: State, rho: float) -> State:
    """Apply ``P_N=(1-rho)I+rho 1 pi_N^T`` in linear time."""

    return (1.0 - rho) * vector + rho * _collective_projection(vector)


def exact_fold_rhs(
    current: State,
    delayed_states: tuple[State, State],
    *,
    parameters: GrowingNetworkParameters,
    zeta: float,
    nu: float,
) -> State:
    """Evaluate the exact fold-coordinate RFDE for the growing family."""

    node_count = parameters.node_count
    if current.shape != (node_count + 2,):
        raise ValueError("current state has the wrong dimension")
    if any(state.shape != current.shape for state in delayed_states):
        raise ValueError("delayed state has the wrong dimension")

    direction, curvature, graph_coefficient = network_objects(parameters)
    delta = parameters.delta
    beta = parameters.beta
    diffusion = parameters.diffusion
    coupling_gain = parameters.coupling_gain
    chart_x, chart_y = current[:2]
    transverse = current[2:]
    graph_state = graph_coefficient * chart_x**2 + transverse

    delayed_collective = np.zeros(node_count)
    delayed_graph = np.zeros(node_count)
    for sign, delayed in zip((1.0, -1.0), delayed_states, strict=True):
        delayed_x = delayed[0]
        delayed_graph_state = (
            graph_coefficient * delayed_x**2 + delayed[2:]
        )
        collective_difference = np.full(
            node_count, chart_x - delayed_x, dtype=float
        )
        graph_difference = graph_state - delayed_graph_state
        delayed_collective += (
            0.5 * _markov_action(collective_difference, parameters.rho)
            + sign
            * zeta
            * direction
            * np.mean(collective_difference)
        )
        delayed_graph += (
            0.5 * _markov_action(graph_difference, parameters.rho)
            + sign * zeta * direction * np.mean(graph_difference)
        )

    chart_x_prime = (
        chart_y
        - chart_x**2
        + delta
        * (
            -2.0 * chart_x * np.mean(curvature * graph_state)
            - beta * chart_x**3 / 3.0
            + coupling_gain * np.mean(delayed_collective)
        )
        + delta**2
        * (
            -np.mean(curvature * graph_state**2)
            + coupling_gain * np.mean(delayed_graph)
        )
        - delta**3 * beta * chart_x * np.mean(graph_state**2)
        - delta**4 * beta * np.mean(graph_state**3) / 3.0
    )
    chart_y_prime = -chart_x + delta * nu

    transverse_generator = (
        diffusion
        * parameters.rho
        * (_collective_projection(transverse) - transverse)
    )
    first_transverse_source = _transverse_projection(
        -2.0 * chart_x * curvature * graph_state
        + coupling_gain * delayed_collective
    ) - 2.0 * graph_coefficient * chart_x * chart_x_prime
    second_transverse_source = _transverse_projection(
        -curvature * graph_state**2
        - beta * chart_x**2 * graph_state
        + coupling_gain * delayed_graph
    )
    transverse_prime = (
        transverse_generator
        + delta * first_transverse_source
        + delta**2 * second_transverse_source
        - delta**3
        * beta
        * chart_x
        * _transverse_projection(graph_state**2)
        - delta**4
        * beta
        * _transverse_projection(graph_state**3)
        / 3.0
    ) / delta
    return np.concatenate(
        ([chart_x_prime, chart_y_prime], transverse_prime)
    )


def integrate_finite_section(
    parameters: GrowingNetworkParameters,
    *,
    zeta: float,
    nu: float,
    section_half_width: float,
    rtol: float = 2.0e-9,
    atol: float = 2.0e-11,
    max_step: float = 0.08,
) -> IntegrationResult:
    """Integrate from ``-S`` to ``S`` by a literal method of steps."""

    from scipy.integrate import solve_ivp

    if not section_half_width > 0.0:
        raise ValueError("section_half_width must be positive")
    if not rtol > 0.0 or not atol > 0.0 or not max_step > 0.0:
        raise ValueError("solver tolerances and max_step must be positive")

    start = -float(section_half_width)
    stop = float(section_half_width)
    delays = (parameters.delay_0, parameters.delay_1)
    step = min(delays)
    completed: list[tuple[float, float, Callable[[float], State]]] = []

    def known_state(query_time: float, current_left: float) -> State:
        tolerance = 2.0e-11 * max(
            1.0, abs(query_time), abs(current_left), abs(start)
        )
        if query_time <= start + tolerance:
            return singular_history(
                min(query_time, start), parameters.node_count
            )
        for left, right, interpolant in reversed(completed):
            if left - tolerance <= query_time <= right + tolerance:
                clipped = min(max(query_time, left), right)
                return np.asarray(interpolant(clipped), dtype=float)
        if query_time > current_left + tolerance:
            raise RuntimeError("method-of-steps queried an unfinished history")
        raise RuntimeError("no completed segment contains delayed query")

    left = start
    current_state = singular_history(start, parameters.node_count)
    function_evaluations = 0
    while left < stop - 1.0e-14:
        right = min(stop, left + step)

        def right_hand_side(inner_time: float, state: State) -> State:
            delayed_states = tuple(
                known_state(inner_time - delay, left) for delay in delays
            )
            return exact_fold_rhs(
                state,
                delayed_states,
                parameters=parameters,
                zeta=zeta,
                nu=nu,
            )

        solution = solve_ivp(
            right_hand_side,
            (left, right),
            current_state,
            method="Radau",
            dense_output=True,
            rtol=rtol,
            atol=atol,
            max_step=max_step,
        )
        if not solution.success or solution.sol is None:
            raise RuntimeError(f"Radau integration failed: {solution.message}")
        completed.append((left, right, solution.sol))
        current_state = np.asarray(solution.y[:, -1], dtype=float)
        function_evaluations += int(solution.nfev)
        left = right

    return IntegrationResult(
        final_state=current_state,
        exit_gap=normalized_exit_gap(current_state),
        segment_count=len(completed),
        function_evaluations=function_evaluations,
        transverse_mean=float(np.mean(current_state[2:])),
    )


def tune_section_root(
    parameters: GrowingNetworkParameters,
    *,
    zeta: float,
    section_half_width: float,
    bracket_half_width: float = 0.4,
    root_xtol: float = 2.0e-10,
    root_rtol: float = 2.0e-10,
    rtol: float = 2.0e-9,
    atol: float = 2.0e-11,
    max_step: float = 0.08,
) -> SectionRoot:
    """Tune ``nu`` until the outgoing section mismatch vanishes."""

    from scipy.optimize import root_scalar

    evaluations: list[IntegrationResult] = []

    def scalar_gap(nu: float) -> float:
        result = integrate_finite_section(
            parameters,
            zeta=zeta,
            nu=nu,
            section_half_width=section_half_width,
            rtol=rtol,
            atol=atol,
            max_step=max_step,
        )
        evaluations.append(result)
        return result.exit_gap

    center = parameters.singular_center
    half_width = bracket_half_width
    lower = center - half_width
    upper = center + half_width
    lower_value = scalar_gap(lower)
    upper_value = scalar_gap(upper)
    expansion_count = 0
    while lower_value * upper_value > 0.0 and expansion_count < 4:
        half_width *= 2.0
        lower = center - half_width
        upper = center + half_width
        lower_value = scalar_gap(lower)
        upper_value = scalar_gap(upper)
        expansion_count += 1
    if lower_value * upper_value > 0.0:
        raise RuntimeError("could not bracket the outgoing-section zero")

    root = root_scalar(
        scalar_gap,
        bracket=(lower, upper),
        method="brentq",
        xtol=root_xtol,
        rtol=root_rtol,
    )
    if not root.converged:
        raise RuntimeError("outgoing-section root solve did not converge")
    residual_result = integrate_finite_section(
        parameters,
        zeta=zeta,
        nu=float(root.root),
        section_half_width=section_half_width,
        rtol=rtol,
        atol=atol,
        max_step=max_step,
    )
    evaluations.append(residual_result)
    return SectionRoot(
        nu=float(root.root),
        zeta=float(zeta),
        residual=float(residual_result.exit_gap),
        bracket=(float(lower), float(upper)),
        orbit_integrations=len(evaluations),
        function_evaluations=sum(item.function_evaluations for item in evaluations),
        transverse_mean=residual_result.transverse_mean,
    )


def network_size_row(
    *,
    node_count: int,
    delta: float = 0.02,
    section_half_width: float = 3.5,
    zeta_step: float = 0.04,
    **solver_options: float,
) -> NetworkSizeRow:
    """Compute the centered normalized quotient for one network size."""

    parameters = GrowingNetworkParameters(node_count=node_count, delta=delta)
    roots = {
        zeta: tune_section_root(
            parameters,
            zeta=zeta,
            section_half_width=section_half_width,
            **solver_options,
        )
        for zeta in (-zeta_step, 0.0, zeta_step)
    }
    quotient = (
        roots[zeta_step].nu - roots[-zeta_step].nu
    ) / (2.0 * zeta_step * delta)
    predicted = parameters.predicted_coefficient
    absolute_error = abs(quotient - predicted)
    return NetworkSizeRow(
        node_count=node_count,
        delta=delta,
        section_half_width=section_half_width,
        zeta_step=zeta_step,
        nu_minus=roots[-zeta_step].nu,
        nu_zero=roots[0.0].nu,
        nu_plus=roots[zeta_step].nu,
        quotient=float(quotient),
        predicted_coefficient=predicted,
        absolute_error=float(absolute_error),
        relative_error=float(absolute_error / abs(predicted)),
        root_residual_max=max(abs(item.residual) for item in roots.values()),
        transverse_mean_max=max(
            abs(item.transverse_mean) for item in roots.values()
        ),
        orbit_integrations=sum(item.orbit_integrations for item in roots.values()),
        function_evaluations=sum(
            item.function_evaluations for item in roots.values()
        ),
    )


def projected_rhs_difference(
    current: State,
    delayed_states: tuple[State, State],
    *,
    parameters: GrowingNetworkParameters,
    zeta: float,
    nu: float,
) -> float:
    """Return the residual in the two collective RHS components."""

    perturbed = exact_fold_rhs(
        current,
        delayed_states,
        parameters=parameters,
        zeta=zeta,
        nu=nu,
    )
    base = exact_fold_rhs(
        current,
        delayed_states,
        parameters=parameters,
        zeta=0.0,
        nu=nu,
    )
    return float(np.max(np.abs(perturbed[:2] - base[:2])))
