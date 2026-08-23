"""Exact diagnostics for the physical outer-selection gate.

The scalar equations in this module are ordinary differential equations and
therefore a special case of every retarded phase-space formulation obtained
by allowing the vector field to ignore its delayed arguments.  They isolate
an issue which is independent of the long-delay algebra: forward attraction
and bounded backward extension are decay properties, not selection rules.

The functions below also record the elementary exponential estimate behind
an anchored boundary-protocol repair.  They are diagnostics for theorem
design; they do not certify the nonlinear outer FitzHugh--Nagumo RFDE.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import hypot, log, sqrt

import sympy as sp


@dataclass(frozen=True)
class OuterSelectionCoherenceAudit:
    """Exact scalar counterexample and its parameter jets."""

    epsilon: sp.Symbol
    slow_time: sp.Symbol
    unfolding: sp.Symbol
    redistribution: sp.Symbol
    amplitude_action: sp.Symbol
    frequency_action: sp.Symbol
    boundary_amplitude: sp.Expr
    repelling_solution: sp.Expr
    repelling_equation_residual: sp.Expr
    first_eta_jet_at_zero: sp.Expr
    second_eta_jet_at_zero: sp.Expr
    mixed_nu_eta_jet_at_zero: sp.Expr


def outer_selection_coherence_audit() -> OuterSelectionCoherenceAudit:
    r"""Return an exact nonuniqueness certificate.

    Consider ``epsilon*x_T=x`` on ``T<=0``.  Every

    ``x(T)=C(epsilon,nu,eta)*exp(T/epsilon)``

    is bounded and converges to zero as ``T`` tends to minus infinity.  The
    chosen amplitude is exponentially small for bounded ``nu,eta`` but has
    arbitrarily large parameter derivatives when ``frequency_action`` is
    larger than ``amplitude_action``.
    """

    epsilon = sp.Symbol("epsilon", positive=True)
    slow_time = sp.Symbol("T", real=True)
    unfolding, redistribution = sp.symbols("nu eta", real=True)
    amplitude_action = sp.Symbol("a", positive=True)
    frequency_action = sp.Symbol("b", positive=True)

    frequency = sp.exp(frequency_action / epsilon)
    boundary_amplitude = sp.exp(-amplitude_action / epsilon) * (
        (1 + unfolding) * sp.sin(redistribution * frequency)
        + 1
        - sp.cos(redistribution * frequency)
    )
    repelling_solution = boundary_amplitude * sp.exp(
        slow_time / epsilon
    )
    residual = sp.simplify(
        epsilon * sp.diff(repelling_solution, slow_time)
        - repelling_solution
    )
    at_zero = {redistribution: 0}
    first_eta = sp.simplify(
        sp.diff(boundary_amplitude, redistribution).subs(at_zero)
    )
    second_eta = sp.simplify(
        sp.diff(boundary_amplitude, redistribution, 2).subs(at_zero)
    )
    mixed_nu_eta = sp.simplify(
        sp.diff(
            boundary_amplitude,
            unfolding,
            redistribution,
        ).subs(at_zero)
    )

    return OuterSelectionCoherenceAudit(
        epsilon=epsilon,
        slow_time=slow_time,
        unfolding=unfolding,
        redistribution=redistribution,
        amplitude_action=amplitude_action,
        frequency_action=frequency_action,
        boundary_amplitude=boundary_amplitude,
        repelling_solution=repelling_solution,
        repelling_equation_residual=residual,
        first_eta_jet_at_zero=first_eta,
        second_eta_jet_at_zero=second_eta,
        mixed_nu_eta_jet_at_zero=mixed_nu_eta,
    )


def logarithmic_matching_scale(delta: float, p: float) -> float:
    """Return ``sqrt(2*p*log(1/delta))`` with domain checks."""

    if not 0.0 < delta < 1.0:
        raise ValueError("delta must lie in (0, 1)")
    if p <= 0.0:
        raise ValueError("p must be positive")
    return sqrt(2.0 * p * log(1.0 / delta))


def tame_envelope_log(
    delta: float,
    *,
    p: float,
    algebraic_loss: float,
    polynomial_loss: float,
    exponential_loss: float,
) -> float:
    r"""Logarithm of the Gate P3-A tame envelope without its constant.

    The returned quantity is

    ``log(delta**(-M) * <S_delta>**m * exp(c*S_delta))``.
    """

    scale = logarithmic_matching_scale(delta, p)
    return (
        algebraic_loss * log(1.0 / delta)
        + polynomial_loss * log(hypot(1.0, scale))
        + exponential_loss * scale
    )


def incoherent_selection_jet_log(
    delta: float,
    *,
    amplitude_action: float,
    frequency_action: float,
    eta_order: int,
) -> float:
    r"""Log-size of the bad first or second ``eta`` jet at ``eta=0``."""

    if not 0.0 < delta < 1.0:
        raise ValueError("delta must lie in (0, 1)")
    if amplitude_action <= 0.0 or frequency_action <= 0.0:
        raise ValueError("actions must be positive")
    if eta_order not in (1, 2):
        raise ValueError("eta_order must be one or two")
    epsilon = delta**2
    return (
        eta_order * frequency_action - amplitude_action
    ) / epsilon


def anchored_trace_jet_log_bound(
    delta: float,
    *,
    normal_action: float,
    boundary_algebraic_loss: float,
    slow_delay: float = 0.0,
    history_rate: float = 1.0,
) -> float:
    r"""Log-bound after propagation from a tame anchored outer boundary.

    For ``epsilon=delta**2``, a positive normal action contributes
    ``-normal_action/epsilon``.  Looking back through a slow-time history of
    length ``delta*slow_delay`` can cost at most
    ``history_rate*slow_delay/delta``.  An algebraically tame boundary jet
    contributes ``boundary_algebraic_loss*log(1/delta)``.
    """

    if not 0.0 < delta < 1.0:
        raise ValueError("delta must lie in (0, 1)")
    if normal_action <= 0.0:
        raise ValueError("normal_action must be positive")
    if slow_delay < 0.0 or history_rate < 0.0:
        raise ValueError("delay and history rate must be nonnegative")
    return (
        -normal_action / delta**2
        + history_rate * slow_delay / delta
        + boundary_algebraic_loss * log(1.0 / delta)
    )
