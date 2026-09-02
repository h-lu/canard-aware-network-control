"""Finite-section diagnostic for the three-node example in Paper A.

This module integrates the *current manuscript's* exact fold-coordinate RFDE
for the three-node direction displayed in the introduction.  The history at
the incoming section is prescribed from the singular orbit and the scalar
condition at the outgoing section is the zero level of the singular first
integral.  The resulting zero is therefore a numerical diagnostic only: it
is not the finite-boundary-value matching function ``D_3^{fin}``, a
heteroclinic connection, or a maximal canard.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Callable

import numpy as np
from numpy.typing import NDArray


State = NDArray[np.float64]


@dataclass(frozen=True)
class ThreeNodeParameters:
    """Parameters fixed for the reproducible three-node diagnostic."""

    delta: float
    sigma: float = 0.5
    beta: float = 3.0
    coupling_gain: float = 2.0
    delay: float = 1.0

    def __post_init__(self) -> None:
        if not self.delta > 0.0:
            raise ValueError("delta must be positive")
        if not 0.0 < self.sigma < 1.0:
            raise ValueError("require 0 < sigma < 1")
        if not self.beta > 0.0:
            raise ValueError("beta must be positive")
        if not self.delay > 0.0:
            raise ValueError("delay must be positive")

    @property
    def predicted_coefficient(self) -> float:
        """Return the exact Fredholm coefficient for this delay direction."""

        return -self.coupling_gain * self.delay * self.sigma / 3.0

    @property
    def singular_center(self) -> float:
        """Return nu_0=(4 sigma^2-beta)/8 for this example."""

        return (4.0 * self.sigma**2 - self.beta) / 8.0


@dataclass(frozen=True)
class IntegrationResult:
    """Exit data from one literal method-of-steps integration."""

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


@dataclass(frozen=True)
class ConvergenceRow:
    """Centered response quotient for one pair (delta,S)."""

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

    def as_dict(self) -> dict[str, float]:
        return asdict(self)


def singular_history(inner_time: float) -> State:
    """Return ``(X,Y,h)`` on the singular orbit with ``h=0``."""

    chart_x = -0.5 * inner_time
    chart_y = 0.25 * (inner_time**2 - 2.0)
    return np.array([chart_x, chart_y, 0.0, 0.0, 0.0], dtype=float)


def normalized_exit_gap(state: State) -> float:
    """Return the zero factor of the singular first integral."""

    chart_x, chart_y = state[:2]
    return float(chart_y - chart_x**2 + 0.5)


def _network_objects(parameters: ThreeNodeParameters) -> tuple[State, ...]:
    stationary = np.full(3, 1.0 / 3.0)
    collective = np.ones((3, 3), dtype=float) / 3.0
    transverse_projection = np.eye(3) - collective
    direction = np.array([-1.0, 0.0, 1.0])
    curvature = np.array(
        [1.0 - parameters.sigma, 1.0, 1.0 + parameters.sigma]
    )
    graph_coefficient = -parameters.sigma * direction
    transverse_generator = collective - np.eye(3)
    return (
        stationary,
        collective,
        transverse_projection,
        direction,
        curvature,
        graph_coefficient,
        transverse_generator,
    )


def exact_fold_rhs(
    current: State,
    delayed: State,
    *,
    parameters: ThreeNodeParameters,
    zeta: float,
    nu: float,
    coincident_delay_control: bool = False,
) -> State:
    """Evaluate the specialized exact fold system from equation (4.2).

    In the two-delay example the zero-delay current-minus-delay term is
    identically zero.  The remaining delayed matrix is
    ``P-zeta*s*pi^T``.  In the coincident-delay control the opposite
    perturbation layers are combined first and cancel, leaving the same base
    matrix ``P`` and no dependence on ``zeta``.
    """

    (
        stationary,
        collective,
        transverse_projection,
        direction,
        curvature,
        graph_coefficient,
        transverse_generator,
    ) = _network_objects(parameters)

    delta = parameters.delta
    beta = parameters.beta
    coupling_gain = parameters.coupling_gain
    chart_x, chart_y = current[:2]
    transverse = current[2:]
    delayed_x = delayed[0]
    delayed_transverse = delayed[2:]
    graph_state = graph_coefficient * chart_x**2 + transverse
    delayed_graph_state = (
        graph_coefficient * delayed_x**2 + delayed_transverse
    )

    if coincident_delay_control:
        delayed_matrix = collective
    else:
        delayed_matrix = collective - zeta * np.outer(direction, stationary)

    delayed_collective = (
        delayed_matrix @ np.ones(3) * (chart_x - delayed_x)
    )
    delayed_graph = delayed_matrix @ (graph_state - delayed_graph_state)

    chart_x_prime = (
        chart_y
        - chart_x**2
        + delta
        * (
            -2.0
            * chart_x
            * (stationary @ (curvature * graph_state))
            - beta * chart_x**3 / 3.0
            + coupling_gain * (stationary @ delayed_collective)
        )
        + delta**2
        * (
            -(stationary @ (curvature * graph_state**2))
            + coupling_gain * (stationary @ delayed_graph)
        )
        - delta**3
        * beta
        * chart_x
        * (stationary @ graph_state**2)
        - delta**4 * beta * (stationary @ graph_state**3) / 3.0
    )
    chart_y_prime = -chart_x + delta * nu
    transverse_rhs = (
        transverse_generator @ transverse
        + delta
        * (
            transverse_projection
            @ (
                -2.0 * chart_x * curvature * graph_state
                + coupling_gain * delayed_collective
            )
            - 2.0 * graph_coefficient * chart_x * chart_x_prime
        )
        + delta**2
        * (
            transverse_projection
            @ (
                -curvature * graph_state**2
                - beta * chart_x**2 * graph_state
                + coupling_gain * delayed_graph
            )
        )
        - delta**3
        * beta
        * chart_x
        * (transverse_projection @ graph_state**2)
        - delta**4
        * beta
        * (transverse_projection @ graph_state**3)
        / 3.0
    )
    return np.concatenate(
        ([chart_x_prime, chart_y_prime], transverse_rhs / delta)
    )


def integrate_finite_section(
    parameters: ThreeNodeParameters,
    *,
    zeta: float,
    nu: float,
    section_half_width: float,
    coincident_delay_control: bool = False,
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
    delay = parameters.delay
    completed: list[tuple[float, float, Callable[[float], State]]] = []

    def known_state(query_time: float, current_left: float) -> State:
        tolerance = 2.0e-11 * max(
            1.0, abs(query_time), abs(current_left), abs(start)
        )
        if query_time <= start + tolerance:
            return singular_history(min(query_time, start))
        for left, right, interpolant in reversed(completed):
            if left - tolerance <= query_time <= right + tolerance:
                clipped = min(max(query_time, left), right)
                return np.asarray(interpolant(clipped), dtype=float)
        if query_time > current_left + tolerance:
            raise RuntimeError("method-of-steps queried an unfinished history")
        raise RuntimeError("no completed segment contains delayed query")

    left = start
    current_state = singular_history(start)
    function_evaluations = 0
    while left < stop - 1.0e-14:
        right = min(stop, left + delay)

        def right_hand_side(inner_time: float, state: State) -> State:
            delayed_state = known_state(inner_time - delay, left)
            return exact_fold_rhs(
                state,
                delayed_state,
                parameters=parameters,
                zeta=zeta,
                nu=nu,
                coincident_delay_control=coincident_delay_control,
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
    parameters: ThreeNodeParameters,
    *,
    zeta: float,
    section_half_width: float,
    coincident_delay_control: bool = False,
    bracket_half_width: float = 0.4,
    root_xtol: float = 2.0e-10,
    root_rtol: float = 2.0e-10,
    rtol: float = 2.0e-9,
    atol: float = 2.0e-11,
    max_step: float = 0.08,
) -> SectionRoot:
    """Tune ``nu`` until the outgoing singular-Hamiltonian gap vanishes."""

    from scipy.optimize import root_scalar

    evaluations: list[IntegrationResult] = []

    def scalar_gap(nu: float) -> float:
        result = integrate_finite_section(
            parameters,
            zeta=zeta,
            nu=nu,
            section_half_width=section_half_width,
            coincident_delay_control=coincident_delay_control,
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
    residual = scalar_gap(float(root.root))
    return SectionRoot(
        nu=float(root.root),
        zeta=float(zeta),
        residual=float(residual),
        bracket=(float(lower), float(upper)),
        orbit_integrations=len(evaluations),
        function_evaluations=sum(item.function_evaluations for item in evaluations),
    )


def convergence_row(
    *,
    delta: float,
    section_half_width: float,
    zeta_step: float = 0.04,
    **solver_options: float,
) -> ConvergenceRow:
    """Compute the centered normalized quotient for one diagonal pair."""

    parameters = ThreeNodeParameters(delta=delta)
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
    return ConvergenceRow(
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
    )


def projected_rhs_difference(
    current: State,
    delayed: State,
    *,
    parameters: ThreeNodeParameters,
    zeta: float,
    nu: float,
) -> float:
    """Return the numerical residual in the two collective RHS components."""

    perturbed = exact_fold_rhs(
        current,
        delayed,
        parameters=parameters,
        zeta=zeta,
        nu=nu,
    )
    base = exact_fold_rhs(
        current,
        delayed,
        parameters=parameters,
        zeta=0.0,
        nu=nu,
    )
    return float(np.max(np.abs(perturbed[:2] - base[:2])))
