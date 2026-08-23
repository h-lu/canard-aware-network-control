"""Quantitative audits for the unforced geometric reset separator.

The local canonical canard theorem supplies an exact retained history near
the right fold.  It does not by itself prove that the forward orbit stays on
the saddle-type middle branch until the reset layer ``rho=-1/2``.  A normal
error is amplified by the repelling action on that outer segment.  The
helpers below keep this action calculation in logarithmic form and record
the two further quantitative budgets used by Gate U-SF:

* strong-unstable domination over the complete-history center-stable
  complement, including the weighted Green contraction budget; and
* the scalar implicit-function estimate for a transverse reset curve.

These functions are theorem diagnostics.  In particular,
``dominated_trichotomy_budget`` checks an already established roughness
bound; it does not infer an RFDE exponential trichotomy from pointwise
eigenvalues alone.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite, log

import numpy as np

from .physical_pulse_bridge import (
    CriticalPoint,
    equilibria_at_recovery,
    repelling_action,
)


@dataclass(frozen=True)
class ResetLayerGeometry:
    """Singular middle-branch data at one bistable recovery layer."""

    middle_point: CriticalPoint
    repelling_action_from_right_fold: float
    right_unstable_vector: tuple[float, float]
    left_unstable_covector: tuple[float, float]


@dataclass(frozen=True)
class DominatedTrichotomyBudget:
    """Algebraic rate ledger for a roughness-based splitting theorem."""

    unstable_rate: float
    center_stable_growth_rate: float
    domination_gap: float
    closes: bool


@dataclass(frozen=True)
class GreenRoughnessBudget:
    """Weighted Lyapunov--Perron contraction ledger."""

    weight: float
    contraction_constant: float
    closes: bool


def reset_layer_geometry(
    collective_recovery: float = -0.5,
) -> ResetLayerGeometry:
    r"""Return the singular saddle geometry used by Gate U-SF.

    The recovery level must lie strictly between the two singular fold
    levels, so that exactly three fast equilibria exist.  The middle one is
    the saddle.  The right and left unstable vectors are normalized by

    ``||e_u||_2 = 1`` and ``p_u.T @ e_u = 1``.

    The action is

    .. math::
       A_R=\int_{\mathfrak f_0}^{\rho_R}
       \frac{\lambda_u(\rho)}{\xi^m(\rho)}\,d\rho>0

    at ``mu=0``.  It is evaluated by the singular-curve quadrature already
    used by :mod:`canard_control.physical_pulse_bridge`.
    """

    if not isfinite(float(collective_recovery)):
        raise ValueError("collective_recovery must be finite")
    equilibria = equilibria_at_recovery(float(collective_recovery))
    if len(equilibria) != 3:
        raise ValueError(
            "collective_recovery must lie strictly in the bistable layer"
        )
    middle = equilibria[1]
    if not middle.critical_voltage < 0.0:
        raise ValueError("the selected middle point is not below the right fold")
    _, action = repelling_action(-middle.critical_voltage)

    jacobian = np.array(
        [
            [0.5 - middle.voltage_1**2, 0.5],
            [2.0, -1.0 - middle.voltage_2**2],
        ],
        dtype=float,
    )
    eigenvalues, right_vectors = np.linalg.eig(jacobian)
    unstable_index = int(np.argmax(eigenvalues.real))
    if not eigenvalues[unstable_index].real > 0.0:
        raise RuntimeError("the middle equilibrium has no unstable eigenvalue")
    right = right_vectors[:, unstable_index].real
    if float(np.sum(right)) < 0.0:
        right *= -1.0
    right /= np.linalg.norm(right)

    left_values, left_vectors = np.linalg.eig(jacobian.T)
    left_index = int(
        np.argmin(abs(left_values - eigenvalues[unstable_index]))
    )
    left = left_vectors[:, left_index].real
    if float(left @ right) < 0.0:
        left *= -1.0
    pairing = float(left @ right)
    if pairing <= 0.0:
        raise RuntimeError("unstable left/right eigenvectors do not pair")
    left /= pairing

    return ResetLayerGeometry(
        middle_point=middle,
        repelling_action_from_right_fold=float(action),
        right_unstable_vector=(float(right[0]), float(right[1])),
        left_unstable_covector=(float(left[0]), float(left[1])),
    )


def log_outer_error_at_reset(
    *,
    log_incoming_error: float,
    repelling_action_value: float,
    epsilon: float,
) -> float:
    r"""Propagate a scalar normal error through a repelling slow segment.

    For the exact normal comparison equation

    .. math::
       \dot u=\lambda_u(\rho(t))u,\qquad
       \dot\rho=\varepsilon q(\rho),

    the outgoing logarithmic error is

    ``log(|u_R|) = log(|u_in|) + action/epsilon``.

    Keeping the calculation in logarithmic form avoids underflow at the
    canard scale.
    """

    values = (log_incoming_error, repelling_action_value, epsilon)
    if not all(isfinite(float(value)) for value in values):
        raise ValueError("all outer-error data must be finite")
    if repelling_action_value <= 0.0:
        raise ValueError("repelling_action_value must be positive")
    if epsilon <= 0.0:
        raise ValueError("epsilon must be positive")
    return float(log_incoming_error + repelling_action_value / epsilon)


def log_required_incoming_error(
    *,
    reset_tube_radius: float,
    repelling_action_value: float,
    epsilon: float,
) -> float:
    r"""Return the sharp scalar log-error threshold at the outer entry.

    To have ``|u_R| <= reset_tube_radius`` in the exact normal comparison
    equation, one needs

    ``log(|u_in|) <= log(reset_tube_radius) - action/epsilon``.
    """

    values = (reset_tube_radius, repelling_action_value, epsilon)
    if not all(isfinite(float(value)) for value in values):
        raise ValueError("all incoming-error data must be finite")
    if reset_tube_radius <= 0.0:
        raise ValueError("reset_tube_radius must be positive")
    if repelling_action_value <= 0.0:
        raise ValueError("repelling_action_value must be positive")
    if epsilon <= 0.0:
        raise ValueError("epsilon must be positive")
    return float(log(reset_tube_radius) - repelling_action_value / epsilon)


def dominated_trichotomy_budget(
    *,
    base_unstable_rate: float,
    base_center_stable_growth_rate: float,
    roughness_rate_loss: float,
) -> DominatedTrichotomyBudget:
    r"""Check a declared strong-unstable roughness budget.

    Suppose an unperturbed complete-history evolution has unstable backward
    rate ``lambda_u`` and center-stable forward growth at most ``alpha_0``.
    Suppose a separate RFDE roughness estimate proves that both exponents
    lose at most ``r``.  The perturbed rates can then be taken as

    ``beta = lambda_u-r`` and ``alpha = alpha_0+r``.

    Domination closes exactly when ``beta>alpha``.  This routine verifies
    only that algebraic implication; obtaining ``r`` uniformly for the
    physical long-delay variational equation is a model theorem.
    """

    values = (
        base_unstable_rate,
        base_center_stable_growth_rate,
        roughness_rate_loss,
    )
    if not all(isfinite(float(value)) for value in values):
        raise ValueError("all trichotomy rates must be finite")
    if base_unstable_rate <= 0.0:
        raise ValueError("base_unstable_rate must be positive")
    if base_center_stable_growth_rate < 0.0:
        raise ValueError(
            "base_center_stable_growth_rate must be nonnegative"
        )
    if roughness_rate_loss < 0.0:
        raise ValueError("roughness_rate_loss must be nonnegative")

    beta = base_unstable_rate - roughness_rate_loss
    alpha = base_center_stable_growth_rate + roughness_rate_loss
    gap = beta - alpha
    return DominatedTrichotomyBudget(
        unstable_rate=float(beta),
        center_stable_growth_rate=float(alpha),
        domination_gap=float(gap),
        closes=bool(beta > alpha and beta > 0.0),
    )


def green_roughness_budget(
    *,
    evolution_bound: float,
    base_center_stable_growth_rate: float,
    base_unstable_rate: float,
    admissible_perturbation_norm: float,
    weight: float | None = None,
) -> GreenRoughnessBudget:
    r"""Check the weighted Green-operator contraction criterion.

    Let a base evolution have center-stable forward bound
    M exp(alpha (t-s)) and unstable backward bound
    M exp(-beta (t-s)), with alpha < beta.  At a weight
    alpha < eta < beta, a pointwise admissible perturbation of norm b has
    Lyapunov--Perron contraction bound

    .. math::
       \kappa=M b\left((\eta-\alpha)^{-1}
                      +(\beta-\eta)^{-1}\right).

    The midpoint weight is used by default.  Closing this scalar criterion
    proves roughness only after the physical delay insertion has genuinely
    been represented by an admissible variation-of-constants operator with
    the supplied norm.
    """

    values = (
        evolution_bound,
        base_center_stable_growth_rate,
        base_unstable_rate,
        admissible_perturbation_norm,
    )
    if not all(isfinite(float(value)) for value in values):
        raise ValueError("all Green-roughness data must be finite")
    if evolution_bound <= 0.0:
        raise ValueError("evolution_bound must be positive")
    if base_center_stable_growth_rate < 0.0:
        raise ValueError(
            "base_center_stable_growth_rate must be nonnegative"
        )
    if base_unstable_rate <= base_center_stable_growth_rate:
        raise ValueError(
            "base_unstable_rate must exceed center-stable growth"
        )
    if admissible_perturbation_norm < 0.0:
        raise ValueError("admissible_perturbation_norm must be nonnegative")
    eta = (
        0.5
        * (base_center_stable_growth_rate + base_unstable_rate)
        if weight is None
        else float(weight)
    )
    if not isfinite(eta):
        raise ValueError("weight must be finite")
    if not base_center_stable_growth_rate < eta < base_unstable_rate:
        raise ValueError(
            "weight must lie strictly between the two base rates"
        )
    contraction = evolution_bound * admissible_perturbation_norm * (
        1.0 / (eta - base_center_stable_growth_rate)
        + 1.0 / (base_unstable_rate - eta)
    )
    return GreenRoughnessBudget(
        weight=float(eta),
        contraction_constant=float(contraction),
        closes=bool(contraction < 1.0),
    )


def separator_root_radius_bound(
    *,
    defining_function_residual: float,
    reset_derivative_floor: float,
) -> float:
    r"""Return the monotone implicit-function bound for a reset root.

    If a scalar complete-history defining function ``g`` has derivative of
    one fixed sign and ``|g'| >= c_a`` on ``[-r,r]``, then a root exists
    uniquely in that interval whenever

    ``|g(0)|/c_a < r``.

    The returned quotient is the corresponding upper bound on the root
    displacement.  The derivative and interval hypotheses must be proved
    separately for the RFDE reset family.
    """

    values = (defining_function_residual, reset_derivative_floor)
    if not all(isfinite(float(value)) for value in values):
        raise ValueError("all separator-root data must be finite")
    if defining_function_residual < 0.0:
        raise ValueError("defining_function_residual must be nonnegative")
    if reset_derivative_floor <= 0.0:
        raise ValueError("reset_derivative_floor must be positive")
    return float(defining_function_residual / reset_derivative_floor)
