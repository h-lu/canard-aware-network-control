"""Diagnostic threshold calculation for the fixed-scaled-delay chart.

This module integrates equation (6) of ``docs/final-model-blowup.md`` by a
literal method of steps.  It is deliberately a *diagnostic*: the prescribed
leading-canard history and the finite exit section are not the invariant
histories used in the theorem.  Consequently, convergence in this module is
evidence for the formal coefficient, not a proof of the geometric canard
root or its section-independent remainder.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Callable

import numpy as np
from numpy.typing import NDArray


State = NDArray[np.float64]


@dataclass(frozen=True)
class ExactChartParameters:
    """Parameters of the exact four-dimensional fixed-scaled-delay chart."""

    delta: float
    weak_gain: float = 1.0
    recovery_gap: float = 1.5
    theta_0: float = 0.5
    theta_1: float = 1.0

    def __post_init__(self) -> None:
        if not self.delta > 0.0:
            raise ValueError("delta must be positive")
        if not self.recovery_gap > 0.0:
            raise ValueError("recovery_gap must be positive")
        if not 0.0 < self.theta_0 < self.theta_1:
            raise ValueError("require 0 < theta_0 < theta_1")


@dataclass(frozen=True)
class IntegrationResult:
    """Final state and solver accounting for one method-of-steps orbit."""

    final_state: State
    hamiltonian: float
    normalized_energy_gap: float
    segment_count: int
    function_evaluations: int


@dataclass(frozen=True)
class ThresholdResult:
    """One finite-section scalar root."""

    nu: float
    eta: float
    residual: float
    bracket: tuple[float, float]
    orbit_integrations: int
    function_evaluations: int


@dataclass(frozen=True)
class ConvergenceRow:
    """Central-difference comparison with the formal eta coefficient."""

    delta: float
    section_half_width: float
    eta_step: float
    nu_zero: float
    nu_plus: float
    nu_minus: float
    quotient_plus: float
    quotient_minus: float
    quotient_central: float
    predicted_coefficient: float
    absolute_error: float
    relative_error: float
    root_residual_max: float

    def as_dict(self) -> dict[str, float]:
        return asdict(self)


def alpha_value() -> float:
    """Return the exact-chart constant alpha = sqrt(6) / 4."""

    return float(np.sqrt(6.0) / 4.0)


def leading_canard_state(
    inner_time: float, recovery_gap: float
) -> State:
    """Leading canard and singular transverse graph at ``inner_time``."""

    alpha = alpha_value()
    chart_x = -inner_time / (2.0 * alpha)
    chart_y = (inner_time**2 - 2.0) / (4.0 * alpha)
    chart_z = -0.5 * alpha * chart_x**2
    chart_w = chart_z / recovery_gap
    return np.array([chart_x, chart_y, chart_z, chart_w], dtype=float)


def ks_hamiltonian(chart_x: float, chart_y: float) -> float:
    r"""Hamiltonian of the leading inner system.

    For ``X'=Y-alpha*X**2`` and ``Y'=-X``, an integrating factor gives

    .. math::
       H=e^{-2\alpha Y}\left(
       \frac{X^2}{2}-\frac{Y}{2\alpha}-\frac{1}{4\alpha^2}
       \right).

    Its zero level contains the leading maximal canard.
    """

    alpha = alpha_value()
    gap = ks_normalized_energy_gap(chart_x, chart_y)
    return float(np.exp(-2.0 * alpha * chart_y) * gap)


def ks_normalized_energy_gap(chart_x: float, chart_y: float) -> float:
    """Return ``exp(2*alpha*Y) H``; it has exactly the same zero set."""

    alpha = alpha_value()
    return float(
        0.5 * chart_x**2
        - chart_y / (2.0 * alpha)
        - 1.0 / (4.0 * alpha**2)
    )


def exact_chart_rhs(
    current: State,
    delayed_0: State,
    delayed_1: State,
    *,
    parameters: ExactChartParameters,
    eta: float,
    nu: float,
) -> State:
    """Evaluate the exact polynomial RFDE chart (equation (6))."""

    delta = parameters.delta
    weak_gain = parameters.weak_gain
    recovery_gap = parameters.recovery_gap
    alpha = alpha_value()

    chart_x, chart_y, chart_z, chart_w = current
    delayed_x_0, _, delayed_z_0, _ = delayed_0
    delayed_x_1, _, delayed_z_1, _ = delayed_1

    delay_critical_x = (
        chart_x - delayed_x_0 / 3.0 - 2.0 * delayed_x_1 / 3.0
    )
    delay_cross_z = (
        -chart_z / 6.0 + delayed_z_0 / 12.0 + delayed_z_1 / 12.0
    )
    delay_transverse_z = -delay_cross_z
    delay_gap_x = delayed_x_0 - delayed_x_1
    delay_gap_z = delayed_z_0 - delayed_z_1

    dx = (
        chart_y
        - alpha * chart_x**2
        + delta
        * (
            weak_gain * delay_critical_x
            - 2.0 * alpha * chart_x * chart_z
            - (20.0 / 9.0) * alpha**2 * chart_x**3
        )
        + delta**2
        * (
            weak_gain * delay_cross_z
            - alpha * chart_z**2
            + 4.0 * alpha**2 * chart_x**2 * chart_z
        )
        - delta**3 * (20.0 / 3.0) * alpha**2 * chart_x * chart_z**2
        + delta**4 * (4.0 / 3.0) * alpha**2 * chart_z**3
    )
    dy = -chart_x + delta * nu
    delta_dz = (
        -2.0 * chart_z
        - alpha * chart_x**2
        + delta
        * (
            -2.0 * alpha * chart_x * chart_z
            + (4.0 / 3.0) * alpha**2 * chart_x**3
            - weak_gain * eta * delay_gap_x
        )
        + delta**2
        * (
            -chart_w
            - alpha * chart_z**2
            - (20.0 / 3.0) * alpha**2 * chart_x**2 * chart_z
            + weak_gain * (delay_transverse_z - eta * delay_gap_z)
        )
        + delta**3 * 4.0 * alpha**2 * chart_x * chart_z**2
        - delta**4 * (20.0 / 9.0) * alpha**2 * chart_z**3
    )
    delta_dw = chart_z - recovery_gap * chart_w
    return np.array([dx, dy, delta_dz / delta, delta_dw / delta])


def integrate_exact_chart(
    parameters: ExactChartParameters,
    *,
    eta: float,
    nu: float,
    section_half_width: float,
    rtol: float = 2.0e-9,
    atol: float = 2.0e-11,
    max_step: float | None = None,
) -> IntegrationResult:
    """Integrate from ``-S`` to ``S`` by a literal method of steps.

    The history on ``[-S-theta_1,-S]`` is the leading canard together with
    the singular transverse graph.  Each integration interval has length at
    most ``theta_0``, so both delayed arguments lie in completed intervals.
    """

    # Imported lazily so symbolic-only use of the package does not require
    # SciPy.  The experiment dependency is documented next to its driver.
    from scipy.integrate import solve_ivp

    if not section_half_width > 0.0:
        raise ValueError("section_half_width must be positive")
    if rtol <= 0.0 or atol <= 0.0:
        raise ValueError("rtol and atol must be positive")

    start = -float(section_half_width)
    stop = float(section_half_width)
    state_at_start = leading_canard_state(start, parameters.recovery_gap)
    segment_limit = parameters.theta_0
    if max_step is None:
        max_step = min(segment_limit / 4.0, 0.08)
    if not max_step > 0.0:
        raise ValueError("max_step must be positive")

    # Tuples are (left endpoint, right endpoint, dense OdeSolution).
    completed: list[tuple[float, float, Callable[[float], State]]] = []

    def prescribed_history(query_time: float) -> State:
        if query_time < start - parameters.theta_1 - 1.0e-10:
            raise RuntimeError("delayed query precedes the prescribed history")
        return leading_canard_state(query_time, parameters.recovery_gap)

    def known_state(query_time: float, current_left: float) -> State:
        tolerance = 2.0e-11 * max(1.0, abs(query_time), abs(current_left))
        if query_time <= start + tolerance:
            return prescribed_history(min(query_time, start))
        for left, right, interpolant in reversed(completed):
            if left - tolerance <= query_time <= right + tolerance:
                clipped = min(max(query_time, left), right)
                return np.asarray(interpolant(clipped), dtype=float)
        if query_time > current_left + tolerance:
            raise RuntimeError(
                "method-of-steps segment queried an unfinished history"
            )
        raise RuntimeError("no completed history segment contains query")

    left = start
    initial_state = state_at_start
    function_evaluations = 0
    while left < stop - 1.0e-14:
        right = min(stop, left + segment_limit)

        def rhs(inner_time: float, current: State) -> State:
            delayed_0 = known_state(inner_time - parameters.theta_0, left)
            delayed_1 = known_state(inner_time - parameters.theta_1, left)
            return exact_chart_rhs(
                current,
                delayed_0,
                delayed_1,
                parameters=parameters,
                eta=eta,
                nu=nu,
            )

        solution = solve_ivp(
            rhs,
            (left, right),
            initial_state,
            method="Radau",
            dense_output=True,
            rtol=rtol,
            atol=atol,
            max_step=max_step,
        )
        if not solution.success or solution.sol is None:
            raise RuntimeError(f"solve_ivp failed: {solution.message}")
        function_evaluations += int(solution.nfev)
        completed.append((left, right, solution.sol))
        initial_state = np.asarray(solution.y[:, -1], dtype=float)
        if not np.all(np.isfinite(initial_state)):
            raise RuntimeError("non-finite state produced by exact-chart solve")
        left = right

    final_x, final_y, _, _ = initial_state
    return IntegrationResult(
        final_state=initial_state,
        hamiltonian=ks_hamiltonian(final_x, final_y),
        normalized_energy_gap=ks_normalized_energy_gap(final_x, final_y),
        segment_count=len(completed),
        function_evaluations=function_evaluations,
    )


def find_finite_section_threshold(
    parameters: ExactChartParameters,
    *,
    eta: float,
    section_half_width: float,
    center: float = 0.0,
    initial_half_width: float = 0.25,
    maximum_half_width: float = 16.0,
    rtol: float = 2.0e-9,
    atol: float = 2.0e-11,
    root_xtol: float = 2.0e-10,
    root_rtol: float = 2.0e-10,
    max_step: float | None = None,
) -> ThresholdResult:
    """Tune ``nu`` so the exit point lies on the leading zero-energy level."""

    from scipy.optimize import brentq

    if initial_half_width <= 0.0 or maximum_half_width < initial_half_width:
        raise ValueError("invalid root-bracket widths")

    cache: dict[float, IntegrationResult] = {}
    function_evaluations = 0

    def gap(candidate: float) -> float:
        nonlocal function_evaluations
        key = float(candidate)
        if key not in cache:
            cache[key] = integrate_exact_chart(
                parameters,
                eta=eta,
                nu=key,
                section_half_width=section_half_width,
                rtol=rtol,
                atol=atol,
                max_step=max_step,
            )
            function_evaluations += cache[key].function_evaluations
        return cache[key].normalized_energy_gap

    center_value = gap(center)
    half_width = float(initial_half_width)
    bracket: tuple[float, float] | None = None
    while half_width <= maximum_half_width * (1.0 + 1.0e-14):
        left = center - half_width
        right = center + half_width
        left_value = gap(left)
        right_value = gap(right)
        candidates = (
            (left, center, left_value, center_value),
            (center, right, center_value, right_value),
            (left, right, left_value, right_value),
        )
        for candidate_left, candidate_right, value_left, value_right in candidates:
            if value_left == 0.0:
                bracket = (candidate_left, candidate_left)
                break
            if value_right == 0.0:
                bracket = (candidate_right, candidate_right)
                break
            if np.signbit(value_left) != np.signbit(value_right):
                bracket = (candidate_left, candidate_right)
                break
        if bracket is not None:
            break
        half_width *= 2.0
    if bracket is None:
        raise RuntimeError(
            "could not bracket the finite-section energy-gap root near center"
        )

    if bracket[0] == bracket[1]:
        root = bracket[0]
    else:
        root = float(
            brentq(
                gap,
                bracket[0],
                bracket[1],
                xtol=root_xtol,
                rtol=root_rtol,
            )
        )
    residual = abs(gap(root))
    return ThresholdResult(
        nu=root,
        eta=float(eta),
        residual=residual,
        bracket=bracket,
        orbit_integrations=len(cache),
        function_evaluations=function_evaluations,
    )


def threshold_coefficient_row(
    parameters: ExactChartParameters,
    *,
    eta_step: float,
    section_half_width: float,
    root_center: float = 0.0,
    rtol: float = 2.0e-9,
    atol: float = 2.0e-11,
    root_xtol: float = 2.0e-10,
    root_rtol: float = 2.0e-10,
    max_step: float | None = None,
) -> ConvergenceRow:
    """Compute plus, minus, and central normalized eta quotients."""

    if not eta_step > 0.0:
        raise ValueError("eta_step must be positive")

    zero = find_finite_section_threshold(
        parameters,
        eta=0.0,
        section_half_width=section_half_width,
        center=root_center,
        rtol=rtol,
        atol=atol,
        root_xtol=root_xtol,
        root_rtol=root_rtol,
        max_step=max_step,
    )
    # The eta roots differ from the zero root by O(delta*eta), so centering
    # their brackets at the computed zero root selects the same local branch.
    local_half_width = max(0.02, 8.0 * parameters.delta * eta_step)
    plus = find_finite_section_threshold(
        parameters,
        eta=eta_step,
        section_half_width=section_half_width,
        center=zero.nu,
        initial_half_width=local_half_width,
        rtol=rtol,
        atol=atol,
        root_xtol=root_xtol,
        root_rtol=root_rtol,
        max_step=max_step,
    )
    minus = find_finite_section_threshold(
        parameters,
        eta=-eta_step,
        section_half_width=section_half_width,
        center=zero.nu,
        initial_half_width=local_half_width,
        rtol=rtol,
        atol=atol,
        root_xtol=root_xtol,
        root_rtol=root_rtol,
        max_step=max_step,
    )

    scale = parameters.delta * eta_step
    quotient_plus = (plus.nu - zero.nu) / scale
    quotient_minus = (zero.nu - minus.nu) / scale
    quotient_central = (plus.nu - minus.nu) / (2.0 * scale)
    predicted = (
        parameters.weak_gain
        * (parameters.theta_0 - parameters.theta_1)
        / (4.0 * alpha_value())
    )
    absolute_error = abs(quotient_central - predicted)
    relative_error = absolute_error / abs(predicted) if predicted else np.nan
    return ConvergenceRow(
        delta=parameters.delta,
        section_half_width=float(section_half_width),
        eta_step=float(eta_step),
        nu_zero=zero.nu,
        nu_plus=plus.nu,
        nu_minus=minus.nu,
        quotient_plus=quotient_plus,
        quotient_minus=quotient_minus,
        quotient_central=quotient_central,
        predicted_coefficient=predicted,
        absolute_error=absolute_error,
        relative_error=relative_error,
        root_residual_max=max(zero.residual, plus.residual, minus.residual),
    )
