"""Lower-fold diagnostics for the unforced Paper III exchange gate.

The routines in this module do three deliberately different jobs.

* :func:`lower_fold_orientation_audit` checks the ordinary-fold orientation
  of the *singular* two-module FitzHugh--Nagumo layer.
* :func:`middle_branch_action` evaluates the positive unstable action from a
  declared reset layer to the lower fold.  The sign of that action is an
  analytic consequence of the exact critical-curve geometry; its decimal
  value is only a numerical diagnostic.
* The Airy helpers solve an exact dynamic saddle-node normal form.  They
  show that the negative side of a repelling slow trajectory contains an
  exponentially thin subinterval which reaches the same fold side as the
  repelling trajectory.  Hence a local unstable sign cannot, by itself,
  classify every nonzero offset through a drifting ordinary fold.

The Airy model is an ODE and therefore an RFDE subclass for every chosen
history length.  It is a rigorous obstruction to a proof shortcut, not a
claim that the full delayed FHN transition map has already been reduced to
Airy form.  The latter still requires a complete-history outer exchange
theorem.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, isfinite, log, pi, sqrt

import numpy as np
import sympy as sp
from scipy.integrate import quad
from scipy.special import airy, airye

from .physical_pulse_bridge import (
    critical_point,
    equilibria_at_recovery,
    fold_points,
)


@dataclass(frozen=True)
class LowerFoldOrientationAudit:
    """Numerical values accompanying the exact lower-fold sign proof."""

    fold_a: float
    fold_b: float
    fold_collective_voltage: float
    fold_collective_recovery: float
    recovery_second_derivative: float
    strong_fast_eigenvalue: float
    normal_quadratic_coefficient: float
    collective_recovery_loading: float
    slow_drift: float
    ordinary_fold_orientation: bool


@dataclass(frozen=True)
class LowerFoldRationalCertificate:
    """Exact rational signs used in the lower-fold orientation proof."""

    a_interval: tuple[sp.Rational, sp.Rational]
    b_interval: tuple[sp.Rational, sp.Rational]
    constraint_at_lower_corner: sp.Rational
    constraint_at_upper_corner: sp.Rational
    b_second_first_term_lower_bound: sp.Rational
    rho_second_bracket_lower_bound: sp.Rational
    certified: bool


@dataclass(frozen=True)
class MiddleBranchAction:
    """Unstable action from one reset layer to the lower fold."""

    reset_collective_recovery: float
    reset_a: float
    reset_collective_voltage: float
    fold_collective_recovery: float
    unfolding: float
    action: float
    quadrature_error: float


@dataclass(frozen=True)
class AiryFoldBoundary:
    """Exact dynamic-fold threshold data in logarithmic coordinates."""

    epsilon: float
    entry_distance: float
    action: float
    selected_repelling_reset_state: float
    log_absolute_reset_shift: float
    leading_log_absolute_reset_shift: float
    asymptotic_ratio: float


def _critical_graph_derivatives(a: float, b: float) -> tuple[float, float]:
    """Return ``b'(a)`` and ``b''(a)`` on the exact critical graph."""

    denominator = 3.0 * b**2 + 4.0
    numerator = 6.0 * a**2 + 2.0
    b_prime = numerator / denominator
    b_second = (
        12.0 * a * denominator
        - numerator * 6.0 * b * b_prime
    ) / denominator**2
    return float(b_prime), float(b_second)


def lower_fold_rational_certificate() -> LowerFoldRationalCertificate:
    r"""Return exact signs enclosing the fold and proving convexity.

    The already-proved Sturm certificate gives the stated rational
    a-interval. Since G_a is positive and G_b is negative, opposite signs
    at the two rational corners enclose b. In the formula for b'', the term
    containing -6*b*b' is positive. The remaining negative term is bounded
    below by the returned rational number, which is greater than -11/10.
    This leaves a strictly positive rational lower bound for -6*a+b''.
    """

    a_lower = sp.Rational(-743, 1000)
    a_upper = sp.Rational(-742, 1000)
    b_lower = sp.Rational(-1174, 1000)
    b_upper = sp.Rational(-1171, 1000)

    def constraint(a: sp.Rational, b: sp.Rational) -> sp.Rational:
        return sp.Rational(2) * a**3 + 2 * a - 4 * b - b**3 - 4

    lower_corner = constraint(a_lower, b_lower)
    upper_corner = constraint(a_upper, b_upper)
    denominator_lower = 4 + 3 * b_upper**2
    first_term_lower = sp.factor(12 * a_lower / denominator_lower)
    bracket_lower = sp.factor(-6 * a_upper - sp.Rational(11, 10))
    certified = bool(
        lower_corner > 0
        and upper_corner < 0
        and first_term_lower > -sp.Rational(11, 10)
        and bracket_lower > 0
    )
    return LowerFoldRationalCertificate(
        a_interval=(a_lower, a_upper),
        b_interval=(b_lower, b_upper),
        constraint_at_lower_corner=lower_corner,
        constraint_at_upper_corner=upper_corner,
        b_second_first_term_lower_bound=first_term_lower,
        rho_second_bracket_lower_bound=bracket_lower,
        certified=certified,
    )


def lower_fold_orientation_audit(
    *, unfolding: float = 0.0
) -> LowerFoldOrientationAudit:
    r"""Evaluate the ordinary-fold coefficients at ``mathfrak f_-``.

    Let ``p`` be a positive right nullvector of the frozen fast Jacobian and
    normalize the positive left nullvector ``q`` by ``q.T*p=1``.  In a
    center coordinate ``x`` and ``y=rho-rho_-`` the leading fast equation is

    ``x' = alpha*x**2 + beta*y + higher order``.

    For the declared model ``alpha>0`` and ``beta<0``.  Moreover
    ``y'=epsilon*(xi_- - unfolding)<0`` whenever the unfolding lies above
    the lower-fold collective voltage.  This is the orientation

    ``x' = positive*x**2 - positive*y``, ``y'<0``:

    the lower attracting and middle saddle branches coalesce, and the
    repelling middle trajectory is carried into the dynamic-fold channel.
    """

    if not isfinite(float(unfolding)):
        raise ValueError("unfolding must be finite")

    fold, _ = fold_points()
    a = fold.a
    b = fold.b
    v_1 = fold.voltage_1
    v_2 = fold.voltage_2
    sigma = sqrt(1.5)

    _, b_second = _critical_graph_derivatives(a, b)
    rho_second = sigma * (-6.0 * a + b_second) / 2.0

    # At det(A)=0, these are positive right and left nullvectors.  The
    # rational formulas expose the sign proof: v_1,v_2<0 and v_1**2>1/2.
    right = np.array([0.5, v_1**2 - 0.5], dtype=float)
    left = np.array([1.0 + v_2**2, 0.5], dtype=float)
    left /= float(left @ right)

    # D^2 f[p,p]=(-2*v_1*p_1^2,-2*v_2*p_2^2).
    alpha = -float(
        left[0] * v_1 * right[0] ** 2
        + left[1] * v_2 * right[1] ** 2
    )
    beta = -float(left @ np.array([1.0, 2.0]))
    slow_drift = fold.critical_voltage - float(unfolding)
    strong_eigenvalue = fold.fast_trace
    rational_certificate = lower_fold_rational_certificate()

    orientation = bool(
        rational_certificate.certified
        and rho_second > 0.0
        and strong_eigenvalue < 0.0
        and alpha > 0.0
        and beta < 0.0
        and slow_drift < 0.0
    )
    return LowerFoldOrientationAudit(
        fold_a=a,
        fold_b=b,
        fold_collective_voltage=fold.critical_voltage,
        fold_collective_recovery=fold.collective_recovery,
        recovery_second_derivative=rho_second,
        strong_fast_eigenvalue=strong_eigenvalue,
        normal_quadratic_coefficient=alpha,
        collective_recovery_loading=beta,
        slow_drift=slow_drift,
        ordinary_fold_orientation=orientation,
    )


def _rho_derivative(a: float, b: float) -> float:
    b_prime, _ = _critical_graph_derivatives(a, b)
    return sqrt(1.5) * (1.0 - 3.0 * a**2 + b_prime) / 2.0


def middle_branch_action(
    *,
    reset_collective_recovery: float = -0.5,
    unfolding: float = 0.0,
) -> MiddleBranchAction:
    r"""Compute the positive middle-branch action down to ``mathfrak f_-``.

    If ``a_R`` is the middle equilibrium at the reset recovery, then

    .. math::
       \mathcal A_-
       =\int_{a_-}^{a_R}
          \frac{\lambda_u(a)\rho'(a)}{\mu-\xi(a)}\,da.

    The routine requires ``mu>xi(a_R)``.  Since ``xi`` is strictly
    increasing on this segment, that condition makes the slow drift point
    toward the lower fold everywhere and makes the integrand positive.
    A reset unstable coordinate is amplified by
    ``exp(mathcal A_-/epsilon)`` at logarithmic leading order.
    """

    values = (reset_collective_recovery, unfolding)
    if not all(isfinite(float(value)) for value in values):
        raise ValueError("reset recovery and unfolding must be finite")

    lower_fold, right_fold = fold_points()
    rho_reset = float(reset_collective_recovery)
    if not lower_fold.collective_recovery < rho_reset < (
        right_fold.collective_recovery
    ):
        raise ValueError(
            "reset recovery must lie strictly between the two folds"
        )

    equilibria = equilibria_at_recovery(rho_reset)
    if len(equilibria) != 3:
        raise RuntimeError("reset layer is not in the bistable interval")
    middle = equilibria[1]
    mu = float(unfolding)
    if not mu > middle.critical_voltage:
        raise ValueError(
            "unfolding must exceed the reset middle-branch voltage so "
            "that recovery drifts toward the lower fold"
        )

    def integrand(a: float) -> float:
        point = critical_point(a)
        denominator = mu - point.critical_voltage
        value = (
            point.unstable_eigenvalue
            * _rho_derivative(a, point.b)
            / denominator
        )
        # Roundoff can produce a signed zero at the fold.  A genuinely
        # negative interior integrand would contradict the contract.
        if value < -1.0e-11:
            raise RuntimeError("middle-branch action lost its positive sign")
        return max(0.0, float(value))

    action, error = quad(
        integrand,
        lower_fold.a,
        middle.a,
        epsabs=1.0e-12,
        epsrel=1.0e-12,
        limit=300,
    )
    return MiddleBranchAction(
        reset_collective_recovery=rho_reset,
        reset_a=middle.a,
        reset_collective_voltage=middle.critical_voltage,
        fold_collective_recovery=lower_fold.collective_recovery,
        unfolding=mu,
        action=float(action),
        quadrature_error=float(error),
    )


def log_fold_visibility_scale(
    *, epsilon: float, action: float, algebraic_prefactor: float = 1.0
) -> float:
    """Return ``log(prefactor)-action/epsilon`` without underflow."""

    values = (epsilon, action, algebraic_prefactor)
    if not all(isfinite(float(value)) for value in values):
        raise ValueError("visibility-scale data must be finite")
    if epsilon <= 0.0:
        raise ValueError("epsilon must be positive")
    if action <= 0.0:
        raise ValueError("action must be positive")
    if algebraic_prefactor <= 0.0:
        raise ValueError("algebraic_prefactor must be positive")
    return log(algebraic_prefactor) - action / epsilon


def airy_repelling_state(*, epsilon: float, distance_to_fold: float) -> float:
    r"""Return the exact repelling Airy solution of the dynamic fold.

    For

    ``x'=x**2-y`` and ``y'=-epsilon``, put
    ``z=y/epsilon**(2/3)``.  The selected repelling solution is

    ``x_r=epsilon**(1/3)*Bi'(z)/Bi(z)``.

    Exponentially scaled Airy functions avoid overflow for large positive
    ``z``.
    """

    if not isfinite(float(epsilon)) or epsilon <= 0.0:
        raise ValueError("epsilon must be positive and finite")
    if (
        not isfinite(float(distance_to_fold))
        or distance_to_fold < 0.0
    ):
        raise ValueError("distance_to_fold must be finite and nonnegative")
    z = float(distance_to_fold) / float(epsilon) ** (2.0 / 3.0)
    _, _, scaled_bi, scaled_bi_prime = airye(z)
    return float(epsilon) ** (1.0 / 3.0) * float(
        scaled_bi_prime / scaled_bi
    )


def airy_fold_coordinate(*, epsilon: float, airy_mixing: float) -> float:
    r"""Return ``x`` at ``y=0`` for ``Bi(z)+c*Ai(z)``.

    Every ``c>0`` starts below the selected repelling solution.  At the
    fold its sign is the sign of ``sqrt(3)-c``.  In particular the exact
    fold-side boundary is ``c=sqrt(3)``, not the selected repelling
    solution ``c=0``.
    """

    if not isfinite(float(epsilon)) or epsilon <= 0.0:
        raise ValueError("epsilon must be positive and finite")
    if not isfinite(float(airy_mixing)) or airy_mixing < 0.0:
        raise ValueError("airy_mixing must be finite and nonnegative")
    ai, ai_prime, bi, bi_prime = airy(0.0)
    c = float(airy_mixing)
    denominator = bi + c * ai
    return float(epsilon) ** (1.0 / 3.0) * float(
        (bi_prime + c * ai_prime) / denominator
    )


def airy_reset_offset_log(
    *, epsilon: float, entry_distance: float, airy_mixing: float
) -> float:
    r"""Return the log magnitude of the exact negative reset offset.

    Relative to the selected ``Bi`` solution, the member
    ``Bi+c*Ai`` has

    .. math::
       \Delta x_0
       =-\frac{\epsilon^{1/3}c}
       {\pi\,Bi(z_0)[Bi(z_0)+cAi(z_0)]}<0.

    This follows from the Airy Wronskian.  The logarithmic implementation
    remains finite when ``Delta x_0`` is far below binary64 range.
    """

    values = (epsilon, entry_distance, airy_mixing)
    if not all(isfinite(float(value)) for value in values):
        raise ValueError("Airy reset data must be finite")
    if epsilon <= 0.0:
        raise ValueError("epsilon must be positive")
    if entry_distance <= 0.0:
        raise ValueError("entry_distance must be positive")
    if airy_mixing <= 0.0:
        raise ValueError("airy_mixing must be positive")

    eps = float(epsilon)
    y_0 = float(entry_distance)
    c = float(airy_mixing)
    z = y_0 / eps ** (2.0 / 3.0)
    scaled_ai, _, scaled_bi, _ = airye(z)
    exponential_action = 4.0 * z ** 1.5 / 3.0
    log_denominator_scaled = float(
        np.logaddexp(
            log(float(scaled_bi)),
            log(c) + log(float(scaled_ai)) - exponential_action,
        )
    )
    return (
        log(eps) / 3.0
        + log(c)
        - log(pi)
        - log(float(scaled_bi))
        - log_denominator_scaled
        - exponential_action
    )


def airy_fold_boundary_audit(
    *, epsilon: float, entry_distance: float
) -> AiryFoldBoundary:
    r"""Audit the exact fold-side boundary ``c=sqrt(3)``.

    Its reset shift from the selected repelling solution satisfies

    .. math::
       \Delta x_{\rm EX}
       \sim-\sqrt{3y_0}
       \exp\{-4y_0^{3/2}/(3\epsilon)\}.

    Thus the geometric repelling trajectory and the fold-side event root
    agree to every algebraic order but are different for each fixed positive
    ``epsilon``.
    """

    values = (epsilon, entry_distance)
    if not all(isfinite(float(value)) for value in values):
        raise ValueError("Airy boundary data must be finite")
    if epsilon <= 0.0:
        raise ValueError("epsilon must be positive")
    if entry_distance <= 0.0:
        raise ValueError("entry_distance must be positive")

    eps = float(epsilon)
    y_0 = float(entry_distance)
    action = 4.0 * y_0 ** 1.5 / 3.0
    log_exact = airy_reset_offset_log(
        epsilon=eps,
        entry_distance=y_0,
        airy_mixing=sqrt(3.0),
    )
    log_leading = 0.5 * log(3.0 * y_0) - action / eps
    return AiryFoldBoundary(
        epsilon=eps,
        entry_distance=y_0,
        action=action,
        selected_repelling_reset_state=airy_repelling_state(
            epsilon=eps, distance_to_fold=y_0
        ),
        log_absolute_reset_shift=log_exact,
        leading_log_absolute_reset_shift=log_leading,
        asymptotic_ratio=exp(log_exact - log_leading),
    )
