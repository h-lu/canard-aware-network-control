"""Exact singular geometry and falsifiers for the physical pulse bridge.

This module starts from the unprepared two-module FitzHugh--Nagumo fast
field used in the JNS base paper.  It proves algebraic facts about its
singular critical curve and weighted-gradient structure, and provides
numerical falsifiers for the two fast channels and the outer repelling
action.  It does *not* construct the positive-epsilon RFDE outer slow
histories; that is the analytic Gate P3-A isolated in the accompanying
Paper III note.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import sympy as sp
from scipy.integrate import quad, solve_ivp
from scipy.optimize import brentq


@dataclass(frozen=True)
class PhysicalPulseBridgeAudit:
    """Exact certificates for the singular fast subsystem."""

    scaled_voltage_1: sp.Symbol
    scaled_voltage_2: sp.Symbol
    voltage_1: sp.Symbol
    voltage_2: sp.Symbol
    recovery_1: sp.Symbol
    recovery_2: sp.Symbol
    sigma: sp.Expr
    fast_field: sp.Matrix
    potential: sp.Expr
    weighted_gradient_residual: sp.Matrix
    critical_constraint: sp.Expr
    critical_constraint_b_derivative: sp.Expr
    critical_voltage: sp.Expr
    collective_recovery: sp.Expr
    fold_equation: sp.Expr
    fold_resultant: sp.Expr
    fold_resultant_real_root_count: int
    left_fold_resultant_interval: tuple[sp.Rational, sp.Rational]
    left_fold_resultant_interval_root_count: int
    left_fold_b_squared: sp.Expr
    left_fold_real_lift_certified: bool
    fast_trace: sp.Expr
    fast_determinant: sp.Expr
    determinant_fold_residual: sp.Expr


@dataclass(frozen=True)
class CriticalPoint:
    """A point on the one-dimensional singular critical curve."""

    a: float
    b: float
    voltage_1: float
    voltage_2: float
    critical_voltage: float
    collective_recovery: float
    fast_trace: float
    fast_determinant: float
    unstable_eigenvalue: float


@dataclass(frozen=True)
class FastChannelResult:
    """Numerical first-hit diagnostic for one singular fast channel."""

    direction: str
    hit_time: float
    hit_critical_voltage: float
    hit_speed: float
    endpoint_error: float
    maximum_potential_increase: float


def physical_pulse_bridge_audit() -> PhysicalPulseBridgeAudit:
    """Build the exact singular geometry from the physical fast field.

    Put ``v_1=sigma*a`` and ``v_2=sigma*b``, where
    ``sigma=sqrt(3/2)``.  On the collective recovery line
    ``w_2-2*w_1=2*sigma``, the critical curve is the single graph defined by

    ``2*a**3 + 2*a - 4*b - b**3 - 4 = 0``.

    Its derivative with respect to ``b`` is strictly negative.  The fold
    certificate combines a Sturm count for the resultant with an exact
    real-lift check for its left root; a resultant count alone would not
    exclude a candidate having only complex ``b``-coordinates.
    """

    a, b = sp.symbols("a b", real=True)
    v_1, v_2, w_1, w_2 = sp.symbols(
        "v_1 v_2 w_1 w_2", real=True
    )
    sigma = sp.sqrt(sp.Rational(3, 2))

    fast_field = sp.Matrix(
        [
            v_1
            - v_1**3 / 3
            - w_1
            + (v_2 - v_1) / 2,
            v_2
            - v_2**3 / 3
            - w_2
            + 2 * (v_1 - v_2),
        ]
    )
    potential = (
        v_1**4 / 3
        - v_1**2
        - 2 * v_1 * v_2
        + 4 * w_1 * v_1
        + v_2**2 / 2
        + v_2**4 / 12
        + w_2 * v_2
    )
    weighted_gradient_residual = sp.simplify(
        sp.Matrix([4 * fast_field[0], fast_field[1]])
        + sp.Matrix([sp.diff(potential, v_1), sp.diff(potential, v_2)])
    )

    critical_constraint = sp.expand(
        2 * a**3 + 2 * a - 4 * b - b**3 - 4
    )
    critical_constraint_b_derivative = sp.diff(critical_constraint, b)
    critical_voltage = sp.simplify(
        sigma * ((a - 1) / 2 + b / 4)
    )
    collective_recovery = sp.simplify(
        sigma * (a - a**3 + b) / 2
    )
    fold_equation = sp.expand(
        2 + b**2 - 2 * a**2 - 3 * a**2 * b**2
    )
    fold_resultant = sp.factor(
        sp.resultant(critical_constraint, fold_equation, b)
    )
    fold_resultant_real_root_count = int(
        sp.Poly(fold_resultant, a).count_roots(-sp.oo, sp.oo)
    )
    left_fold_interval = (
        sp.Rational(-743, 1000),
        sp.Rational(-742, 1000),
    )
    left_fold_resultant_interval_root_count = int(
        sp.Poly(fold_resultant, a).count_roots(*left_fold_interval)
    )
    left_fold_b_squared = sp.factor(
        2 * (a**2 - 1) / (1 - 3 * a**2)
    )
    smallest_absolute_a = -left_fold_interval[1]
    largest_absolute_a = -left_fold_interval[0]
    left_fold_real_lift_certified = bool(
        left_fold_resultant_interval_root_count == 1
        and largest_absolute_a**2 < 1
        and 3 * smallest_absolute_a**2 > 1
    )

    fast_jacobian = fast_field.jacobian((v_1, v_2))
    fast_trace = sp.factor(sp.trace(fast_jacobian))
    fast_determinant = sp.factor(fast_jacobian.det())
    scaled_determinant = sp.expand(
        fast_determinant.subs({v_1: sigma * a, v_2: sigma * b})
    )
    determinant_fold_residual = sp.simplify(
        4 * scaled_determinant + sp.Rational(3, 1) * fold_equation
    )

    return PhysicalPulseBridgeAudit(
        scaled_voltage_1=a,
        scaled_voltage_2=b,
        voltage_1=v_1,
        voltage_2=v_2,
        recovery_1=w_1,
        recovery_2=w_2,
        sigma=sigma,
        fast_field=fast_field,
        potential=potential,
        weighted_gradient_residual=weighted_gradient_residual,
        critical_constraint=critical_constraint,
        critical_constraint_b_derivative=(
            critical_constraint_b_derivative
        ),
        critical_voltage=critical_voltage,
        collective_recovery=collective_recovery,
        fold_equation=fold_equation,
        fold_resultant=fold_resultant,
        fold_resultant_real_root_count=(
            fold_resultant_real_root_count
        ),
        left_fold_resultant_interval=left_fold_interval,
        left_fold_resultant_interval_root_count=(
            left_fold_resultant_interval_root_count
        ),
        left_fold_b_squared=left_fold_b_squared,
        left_fold_real_lift_certified=left_fold_real_lift_certified,
        fast_trace=fast_trace,
        fast_determinant=fast_determinant,
        determinant_fold_residual=determinant_fold_residual,
    )


def critical_b(a: float) -> float:
    """Return the unique ``b`` on the singular critical graph."""

    target = 2 * a**3 + 2 * a - 4

    def cubic(value: float) -> float:
        return value**3 + 4 * value - target

    radius = max(2.0, 2.0 * abs(a) + 2.0)
    while cubic(-radius) > 0 or cubic(radius) < 0:
        radius *= 2.0
    return float(brentq(cubic, -radius, radius, xtol=1e-14))


def critical_point(a: float) -> CriticalPoint:
    """Evaluate the singular critical graph and its fast spectrum."""

    sigma = float(np.sqrt(1.5))
    b = critical_b(a)
    v_1 = sigma * a
    v_2 = sigma * b
    xi = sigma * ((a - 1.0) / 2.0 + b / 4.0)
    rho = sigma * (a - a**3 + b) / 2.0
    trace = -0.5 - v_1**2 - v_2**2
    determinant = (
        2 * v_1**2 * (1 + v_2**2) - (3 + v_2**2)
    ) / 2.0
    discriminant = trace**2 - 4.0 * determinant
    unstable = (trace + np.sqrt(max(0.0, discriminant))) / 2.0
    return CriticalPoint(
        a=float(a),
        b=b,
        voltage_1=v_1,
        voltage_2=v_2,
        critical_voltage=xi,
        collective_recovery=rho,
        fast_trace=trace,
        fast_determinant=determinant,
        unstable_eigenvalue=float(unstable),
    )


def fold_points() -> tuple[CriticalPoint, CriticalPoint]:
    """Return the left and local folds on the unique critical graph."""

    def fold_value(a: float) -> float:
        b = critical_b(a)
        return 2 + b**2 - 2 * a**2 - 3 * a**2 * b**2

    left_a = brentq(fold_value, -0.743, -0.742, xtol=1e-14)
    return critical_point(left_a), critical_point(1.0)


def _rho_derivative(a: float, b: float) -> float:
    sigma = float(np.sqrt(1.5))
    b_derivative = (6 * a**2 + 2) / (3 * b**2 + 4)
    return sigma * (1 - 3 * a**2 + b_derivative) / 2


def repelling_action(detector_level: float) -> tuple[float, float]:
    r"""Compute the singular outer repelling action for ``H=-xi``.

    ``detector_level`` must lie strictly between zero and the value of
    ``-xi`` at the left fold.  The returned pair is ``(a_H, A_H)``, where

    .. math::
       A_H=\int_{1}^{a_H}
       \lambda_u(a)\frac{\rho'(a)}{\xi(a)}\,da>0.

    This coefficient controls only the logarithmic scale of a detector
    offset after the positive-epsilon exchange and landing hypotheses have
    been proved.
    """

    left, _ = fold_points()
    maximum_level = -left.critical_voltage
    if not 0.0 < detector_level < maximum_level:
        raise ValueError(
            "detector_level must lie between the two fold levels"
        )

    def level_residual(a: float) -> float:
        return -critical_point(a).critical_voltage - detector_level

    # Strict interior levels already give opposite signs at the folds.  Do
    # not trim this bracket: doing so rejects valid levels close to a fold.
    a_h = brentq(level_residual, left.a, 1.0, xtol=1e-14)

    def integrand(a: float) -> float:
        point = critical_point(a)
        if abs(point.critical_voltage) < 1e-11:
            return 0.0
        rho_prime = _rho_derivative(a, point.b)
        return (
            point.unstable_eigenvalue
            * rho_prime
            / point.critical_voltage
        )

    action, _ = quad(
        integrand,
        1.0,
        a_h,
        epsabs=1e-11,
        epsrel=1e-11,
        limit=200,
    )
    return float(a_h), float(action)


def equilibria_at_recovery(
    collective_recovery: float,
) -> tuple[CriticalPoint, ...]:
    """Find every distinct singular fast equilibrium at one recovery value.

    The critical recovery graph has exactly two folds.  We therefore solve
    once on each of its three monotone intervals instead of scanning a
    bounded grid; this retains near-fold pairs and the unique far-field root.
    """

    def residual(a: float) -> float:
        return critical_point(a).collective_recovery - collective_recovery

    target = float(collective_recovery)
    if not np.isfinite(target):
        raise ValueError("collective_recovery must be finite")
    left, right = fold_points()
    rho_left = left.collective_recovery
    rho_right = right.collective_recovery
    roots: list[float] = []

    def append_root(lower: float, upper: float) -> None:
        root = float(brentq(residual, lower, upper, xtol=1e-13))
        if not roots or all(abs(root - old) > 1e-8 for old in roots):
            roots.append(root)

    if target >= rho_left:
        upper = left.a
        span = 1.0
        lower = upper - span
        while residual(lower) * residual(upper) > 0.0:
            span *= 2.0
            lower = upper - span
        append_root(lower, upper)

    if rho_left <= target <= rho_right:
        append_root(left.a, right.a)

    if target <= rho_right:
        lower = right.a
        span = 1.0
        upper = lower + span
        while residual(lower) * residual(upper) > 0.0:
            span *= 2.0
            upper = lower + span
        append_root(lower, upper)

    roots.sort()
    return tuple(critical_point(root) for root in roots)


def _fast_potential(
    v_1: np.ndarray,
    v_2: np.ndarray,
    w_1: float,
    w_2: float,
) -> np.ndarray:
    return (
        v_1**4 / 3
        - v_1**2
        - 2 * v_1 * v_2
        + 4 * w_1 * v_1
        + v_2**2 / 2
        + v_2**4 / 12
        + w_2 * v_2
    )


def fast_channel_falsifier(
    collective_recovery: float = -0.5,
    pulse_level: float = 1.4,
    quiet_level: float = 0.0,
) -> tuple[FastChannelResult, FastChannelResult]:
    """Numerically test the two singular fast heteroclinic channels.

    The fixed weighted observable is ``H=-xi``.  The lower channel is
    tested against ``H=pulse_level`` and the upper channel against
    ``H=quiet_level``.  Exact gradient/cooperative arguments, not this
    integration, carry the theorem in the accompanying note.
    """

    equilibria = equilibria_at_recovery(collective_recovery)
    if len(equilibria) != 3:
        raise RuntimeError("the selected recovery level is not bistable")
    lower, saddle, upper = equilibria
    sigma = float(np.sqrt(1.5))
    w_1 = collective_recovery
    w_2 = 2 * sigma + 2 * collective_recovery

    saddle_state = np.array([saddle.voltage_1, saddle.voltage_2])
    jacobian = np.array(
        [
            [0.5 - saddle_state[0] ** 2, 0.5],
            [2.0, -1.0 - saddle_state[1] ** 2],
        ]
    )
    eigenvalues, eigenvectors = np.linalg.eig(jacobian)
    unstable_index = int(np.argmax(eigenvalues.real))
    unstable_vector = eigenvectors[:, unstable_index].real
    if np.sum(unstable_vector) < 0:
        unstable_vector *= -1
    unstable_vector /= np.linalg.norm(unstable_vector)

    ell = np.array([0.5, 0.25])
    xi_offset = ell @ np.array([sigma, 0.0])

    def rhs(_time: float, state: np.ndarray) -> np.ndarray:
        v_1, v_2 = state
        return np.array(
            [
                v_1 - v_1**3 / 3 - w_1 + (v_2 - v_1) / 2,
                v_2 - v_2**3 / 3 - w_2 + 2 * (v_1 - v_2),
            ]
        )

    def xi(state: np.ndarray) -> float:
        return float(ell @ state - xi_offset)

    def integrate(direction: str) -> FastChannelResult:
        sign = -1.0 if direction == "pulse" else 1.0
        target = -pulse_level if direction == "pulse" else -quiet_level
        endpoint = lower if direction == "pulse" else upper
        initial = saddle_state + sign * 1e-7 * unstable_vector

        def event(_time: float, state: np.ndarray) -> float:
            return xi(state) - target

        event.terminal = False  # type: ignore[attr-defined]
        event.direction = sign  # type: ignore[attr-defined]
        solution = solve_ivp(
            rhs,
            (0.0, 80.0),
            initial,
            events=event,
            rtol=2e-10,
            atol=2e-12,
            max_step=0.05,
            dense_output=False,
        )
        if not solution.t_events[0].size:
            raise RuntimeError(f"{direction} section was not reached")
        hit_state = solution.y_events[0][0]
        hit_speed = float(ell @ rhs(0.0, hit_state))
        endpoint_state = np.array([endpoint.voltage_1, endpoint.voltage_2])
        endpoint_error = float(
            np.linalg.norm(solution.y[:, -1] - endpoint_state)
        )
        potentials = _fast_potential(
            solution.y[0], solution.y[1], w_1, w_2
        )
        maximum_increase = float(np.max(np.diff(potentials)))
        return FastChannelResult(
            direction=direction,
            hit_time=float(solution.t_events[0][0]),
            hit_critical_voltage=xi(hit_state),
            hit_speed=hit_speed,
            endpoint_error=endpoint_error,
            maximum_potential_increase=maximum_increase,
        )

    return integrate("pulse"), integrate("quiet")
