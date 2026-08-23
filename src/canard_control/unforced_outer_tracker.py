"""Exact budgets for the unforced outer-tracker matching problem.

The canonical right-fold theorem supplies an exact complete history on a
local outgoing section.  Forward RFDE well-posedness continues that history
exactly until it either reaches the reset layer or leaves a declared middle
tube.  What is not automatic is containment: a normal mismatch is amplified
over the fixed slow distance to the reset layer.

This module records three calculations used to keep those claims separate:

* the causal delay-buffer and hit-time bounds while the recovery coordinate
  is strictly monotone;
* the exact scalar terminal-trace identity
  ``h = exp(-action/epsilon) * beta``; and
* the logarithmic implicit-function budget for matching a canonical history
  to a bounded terminal-normalized outer trace.

The last budget checks hypotheses of a boundary-value theorem.  It does not
construct the physical terminal-normalized RFDE trace or prove its two-sided
action sensitivity.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, isfinite, log

import sympy as sp


@dataclass(frozen=True)
class CausalOuterBounds:
    """Bounds valid before a monotone outer orbit leaves its tube."""

    slow_time_delay: float
    maximum_recovery_backtrack: float
    maximum_fast_hit_time: float


@dataclass(frozen=True)
class ScalarTerminalIdentity:
    """Symbolic identities for the exact scalar two-point problem."""

    epsilon: sp.Symbol
    action: sp.Symbol
    incoming_coordinate: sp.Symbol
    terminal_coordinate: sp.Symbol
    incoming_from_terminal: sp.Expr
    terminal_required_by_incoming: sp.Expr
    round_trip_residual: sp.Expr


@dataclass(frozen=True)
class TerminalMatchingBudget:
    """Logarithmic scalar implicit-function budget at one positive delta."""

    log_derivative_floor: float
    log_reference_mismatch_bound: float
    log_root_radius_bound: float
    terminal_radius: float
    closes: bool


@dataclass(frozen=True)
class ActionSupercriticalBudget:
    """Action-scale specialization of :class:`TerminalMatchingBudget`."""

    delta: float
    action: float
    action_margin: float
    log_derivative_floor: float
    log_reference_mismatch_bound: float
    log_root_radius_bound: float
    terminal_radius: float
    closes: bool


def causal_outer_bounds(
    *,
    delta: float,
    maximum_scaled_delay: float,
    recovery_speed_floor: float,
    recovery_speed_ceiling: float,
    overlap_recovery: float,
    reset_recovery: float,
) -> CausalOuterBounds:
    r"""Return exact comparison bounds for a decreasing recovery base.

    In slow time ``T=epsilon*t``, a physical delay ``theta/delta`` has
    length ``delta*theta``.  Suppose, until a tube exit,

    ``-speed_ceiling <= rho_T <= -speed_floor < 0``.

    A delayed query is then upstream in the recovery coordinate and differs
    from the current recovery by at most
    ``delta*theta*speed_ceiling``.  If no tube exit occurs, the fast time to
    move from ``overlap_recovery`` down to ``reset_recovery`` is at most

    ``(overlap_recovery-reset_recovery)/(delta**2*speed_floor)``.

    The function does not assert that the physical orbit remains in the tube.
    """

    values = (
        delta,
        maximum_scaled_delay,
        recovery_speed_floor,
        recovery_speed_ceiling,
        overlap_recovery,
        reset_recovery,
    )
    if not all(isfinite(float(value)) for value in values):
        raise ValueError("all causal outer data must be finite")
    if delta <= 0.0:
        raise ValueError("delta must be positive")
    if maximum_scaled_delay <= 0.0:
        raise ValueError("maximum_scaled_delay must be positive")
    if recovery_speed_floor <= 0.0:
        raise ValueError("recovery_speed_floor must be positive")
    if recovery_speed_ceiling < recovery_speed_floor:
        raise ValueError(
            "recovery_speed_ceiling must dominate recovery_speed_floor"
        )
    if not reset_recovery < overlap_recovery:
        raise ValueError("reset_recovery must lie below overlap_recovery")

    slow_delay = float(delta * maximum_scaled_delay)
    return CausalOuterBounds(
        slow_time_delay=slow_delay,
        maximum_recovery_backtrack=float(
            slow_delay * recovery_speed_ceiling
        ),
        maximum_fast_hit_time=float(
            (overlap_recovery - reset_recovery)
            / (delta**2 * recovery_speed_floor)
        ),
    )


def scalar_terminal_matching_identity() -> ScalarTerminalIdentity:
    r"""Return the exact symbolic terminal-trace identities.

    For ``epsilon*n_s=a(s)n`` on ``0<=s<=L``, write
    ``action=integral_0^L a(s) ds``.  If ``n(L)=beta`` and ``n(0)=h``, then

    ``h=exp(-action/epsilon)*beta`` and
    ``beta=exp(action/epsilon)*h``.

    The same calculation is an RFDE-subclass obstruction because an ODE is a
    retarded equation whose functional ignores its history.
    """

    epsilon = sp.Symbol("epsilon", positive=True)
    action = sp.Symbol("A", positive=True)
    incoming = sp.Symbol("h", real=True)
    terminal = sp.Symbol("beta", real=True)
    incoming_from_terminal = terminal * sp.exp(-action / epsilon)
    terminal_required = incoming * sp.exp(action / epsilon)
    residual = sp.simplify(
        incoming_from_terminal.subs(terminal, terminal_required) - incoming
    )
    return ScalarTerminalIdentity(
        epsilon=epsilon,
        action=action,
        incoming_coordinate=incoming,
        terminal_coordinate=terminal,
        incoming_from_terminal=incoming_from_terminal,
        terminal_required_by_incoming=terminal_required,
        round_trip_residual=residual,
    )


def log_terminal_coordinate(
    *,
    log_absolute_incoming_coordinate: float,
    action: float,
    epsilon: float,
) -> float:
    r"""Return ``log|beta|`` in the exact scalar terminal problem.

    ``-inf`` is accepted for an exactly zero incoming coordinate and is
    returned unchanged.  Working in logarithms avoids canard-scale overflow.
    """

    incoming_log = float(log_absolute_incoming_coordinate)
    if incoming_log == float("-inf"):
        if not isfinite(float(action)) or action <= 0.0:
            raise ValueError("action must be positive and finite")
        if not isfinite(float(epsilon)) or epsilon <= 0.0:
            raise ValueError("epsilon must be positive and finite")
        return incoming_log
    if not all(
        isfinite(float(value))
        for value in (incoming_log, action, epsilon)
    ):
        raise ValueError("all scalar terminal data must be finite")
    if action <= 0.0:
        raise ValueError("action must be positive")
    if epsilon <= 0.0:
        raise ValueError("epsilon must be positive")
    return float(incoming_log + action / epsilon)


def terminal_matching_budget(
    *,
    log_derivative_floor: float,
    log_reference_mismatch_bound: float,
    terminal_radius: float,
) -> TerminalMatchingBudget:
    r"""Check the exact monotone scalar root-radius implication in logs.

    If a mismatch map ``m(beta,u)`` has one derivative sign and
    ``|partial_beta m| >= d`` on ``[-R,R]``, while ``|m(0,u)| <= r``, then a
    unique zero exists in that interval whenever ``r/d < R``.  Its distance
    from zero is at most ``r/d``.

    The supplied logarithms are ``log(d)`` and ``log(r)``.  They may be very
    negative but must be finite.  An exactly vanishing reference mismatch is
    represented by ``log_reference_mismatch_bound=-inf``.
    """

    derivative_log = float(log_derivative_floor)
    mismatch_log = float(log_reference_mismatch_bound)
    if not isfinite(derivative_log):
        raise ValueError("log_derivative_floor must be finite")
    if mismatch_log != float("-inf") and not isfinite(mismatch_log):
        raise ValueError(
            "log_reference_mismatch_bound must be finite or -inf"
        )
    if not isfinite(float(terminal_radius)) or terminal_radius <= 0.0:
        raise ValueError("terminal_radius must be positive and finite")

    root_log = (
        float("-inf")
        if mismatch_log == float("-inf")
        else mismatch_log - derivative_log
    )
    return TerminalMatchingBudget(
        log_derivative_floor=derivative_log,
        log_reference_mismatch_bound=mismatch_log,
        log_root_radius_bound=root_log,
        terminal_radius=float(terminal_radius),
        closes=bool(root_log < log(float(terminal_radius))),
    )


def action_supercritical_terminal_budget(
    *,
    delta: float,
    action: float,
    action_margin: float,
    derivative_delay_loss_constant: float,
    residual_delay_loss_constant: float,
    derivative_polynomial_power: float,
    residual_polynomial_power: float,
    derivative_prefactor: float = 1.0,
    residual_prefactor: float = 1.0,
    terminal_radius: float = 1.0,
) -> ActionSupercriticalBudget:
    r"""Evaluate the minimal action-supercritical terminal-match budget.

    The physical boundary-value contract sought in Gate U-OUT has the form

    ``d_delta >= c_d delta**M_d exp(-A/delta**2-L_d/delta)``

    for the terminal-to-overlap derivative floor and

    ``r_delta <= C_r delta**(-M_r)``
    ``          * exp(-(A+chi)/delta**2+L_r/delta)``

    for the canonical-to-reference mismatch.  Their ratio bounds the exact
    terminal correction selected by the scalar implicit-function theorem.

    A positive ``action_margin=chi`` beats every fixed polynomial loss and
    the combined long-delay loss ``exp((L_d+L_r)/delta)`` as ``delta``
    tends to zero.  This numerical ledger does not prove either physical
    estimate.
    """

    values = (
        delta,
        action,
        action_margin,
        derivative_delay_loss_constant,
        residual_delay_loss_constant,
        derivative_polynomial_power,
        residual_polynomial_power,
        derivative_prefactor,
        residual_prefactor,
        terminal_radius,
    )
    if not all(isfinite(float(value)) for value in values):
        raise ValueError("all action-supercritical data must be finite")
    if delta <= 0.0:
        raise ValueError("delta must be positive")
    if action <= 0.0:
        raise ValueError("action must be positive")
    if action_margin <= 0.0:
        raise ValueError("action_margin must be positive")
    if derivative_delay_loss_constant < 0.0:
        raise ValueError(
            "derivative_delay_loss_constant must be nonnegative"
        )
    if residual_delay_loss_constant < 0.0:
        raise ValueError(
            "residual_delay_loss_constant must be nonnegative"
        )
    if derivative_polynomial_power < 0.0:
        raise ValueError("derivative_polynomial_power must be nonnegative")
    if residual_polynomial_power < 0.0:
        raise ValueError("residual_polynomial_power must be nonnegative")
    if derivative_prefactor <= 0.0 or residual_prefactor <= 0.0:
        raise ValueError("matching prefactors must be positive")
    if terminal_radius <= 0.0:
        raise ValueError("terminal_radius must be positive")

    epsilon = delta**2
    log_delta = log(delta)
    derivative_log = (
        log(derivative_prefactor)
        + derivative_polynomial_power * log_delta
        - action / epsilon
        - derivative_delay_loss_constant / delta
    )
    mismatch_log = (
        log(residual_prefactor)
        - residual_polynomial_power * log_delta
        - (action + action_margin) / epsilon
        + residual_delay_loss_constant / delta
    )
    generic = terminal_matching_budget(
        log_derivative_floor=derivative_log,
        log_reference_mismatch_bound=mismatch_log,
        terminal_radius=terminal_radius,
    )
    return ActionSupercriticalBudget(
        delta=float(delta),
        action=float(action),
        action_margin=float(action_margin),
        log_derivative_floor=generic.log_derivative_floor,
        log_reference_mismatch_bound=(
            generic.log_reference_mismatch_bound
        ),
        log_root_radius_bound=generic.log_root_radius_bound,
        terminal_radius=generic.terminal_radius,
        closes=generic.closes,
    )


def terminal_root_radius_from_log_budget(
    budget: TerminalMatchingBudget | ActionSupercriticalBudget,
) -> float:
    """Exponentiate a root-radius bound when it fits in binary64."""

    root_log = float(budget.log_root_radius_bound)
    if root_log == float("-inf"):
        return 0.0
    # ``exp`` returning zero is an honest underflow of a diagnostic only.
    return float(exp(root_log))
