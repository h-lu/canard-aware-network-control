"""Dimension-free budgets for a relative strong-unstable history graph.

The physical long-delay problem does not have a stable spectral gap that is
uniform as ``delta -> 0``.  A geometric separator needs less: one uniformly
strong unstable direction and a codimension-one forward-growth history
graph.  This module records the scalar estimates used by the corresponding
proof note.  The routines audit hypotheses; they do not infer an RFDE
dichotomy or invariant projectors from pointwise eigenvalues.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import isfinite

import numpy as np

from .physical_pulse_bridge import equilibria_at_recovery


@dataclass(frozen=True)
class PhaseLiftBound:
    """Uniform constants for lifting an ODE separation to history space."""

    delay_length: float
    current_evolution_bound: float
    projector_bound: float
    history_evolution_bound: float


@dataclass(frozen=True)
class StrongUnstableRoughnessBudget:
    """Weighted contraction data for a relative-growth history graph."""

    center_stable_rate: float
    unstable_rate: float
    weight: float
    perturbation_norm: float
    contraction_constant: float
    resolvent_bound: float
    closes: bool


@dataclass(frozen=True)
class SingularCurrentIndex:
    """Frozen current-state spectrum at one middle-branch point."""

    collective_recovery: float
    eigenvalues: tuple[complex, ...]
    unstable_count: int
    center_count: int
    stable_count: int
    unstable_floor: float


def exact_safe_layer_history_norm() -> Fraction:
    r"""Return the exact max-norm bound for the final two-delay functional.

    On ``|eta| <= 1/20`` all layer entries are positive.  In the vector
    infinity norm,

    ``||B phi(0)-C0 phi(-tau0)-C1 phi(-tau1)||``

    is bounded by

    ``||[B,-C0,-C1]||_inf ||phi||_C = 8/3 ||phi||_C``.

    The same value is obtained from
    ``||B||_inf+||C0(eta)||_inf+||C1(eta)||_inf`` for each *common*
    ``eta`` in the box.  Maximizing the two delayed-layer norms at
    different endpoint values would give the valid but non-sharp bound
    ``43/15``.
    """

    endpoint_etas = (Fraction(-1, 20), Fraction(1, 20))
    total_layer = (
        (Fraction(1, 2), Fraction(1, 4)),
        (Fraction(2, 3), Fraction(2, 3)),
    )

    def infinity_norm(matrix: tuple[tuple[Fraction, ...], ...]) -> Fraction:
        return max(sum(abs(value) for value in row) for row in matrix)

    combined_norms: list[Fraction] = []
    for eta in endpoint_etas:
        layer_0 = (
            (Fraction(1, 6) + eta, Fraction(1, 12)),
            (Fraction(1, 6) - 2 * eta, Fraction(1, 4)),
        )
        layer_1 = (
            (Fraction(1, 3) - eta, Fraction(1, 6)),
            (Fraction(1, 2) + 2 * eta, Fraction(5, 12)),
        )
        combined_rows = tuple(
            total_layer[row] + layer_0[row] + layer_1[row]
            for row in range(2)
        )
        combined_norms.append(infinity_norm(combined_rows))
    return max(combined_norms)


def phase_lift_bound(
    *,
    delay_length: float,
    current_evolution_bound: float,
    projector_bound: float,
) -> PhaseLiftBound:
    r"""Lift a current-state ODE bound to ``C([-tau,0])``.

    Old history is translated isometrically until it leaves the interval.
    Consequently the history evolution constant is the maximum of the
    current evolution and projector constants and contains no factor that
    grows with ``delay_length``.
    """

    values = (delay_length, current_evolution_bound, projector_bound)
    if not all(isfinite(float(value)) for value in values):
        raise ValueError("all phase-lift data must be finite")
    if delay_length <= 0.0:
        raise ValueError("delay_length must be positive")
    if current_evolution_bound < 1.0:
        raise ValueError("current_evolution_bound must be at least one")
    if projector_bound < 1.0:
        raise ValueError("projector_bound must be at least one")
    history_bound = max(
        1.0, float(current_evolution_bound), float(projector_bound)
    )
    return PhaseLiftBound(
        delay_length=float(delay_length),
        current_evolution_bound=float(current_evolution_bound),
        projector_bound=float(projector_bound),
        history_evolution_bound=history_bound,
    )


def strong_unstable_roughness_budget(
    *,
    evolution_bound: float,
    center_stable_rate: float,
    unstable_rate: float,
    perturbation_norm: float,
    weight: float | None = None,
) -> StrongUnstableRoughnessBudget:
    r"""Evaluate the forward Lyapunov--Perron contraction budget.

    For ``alpha < eta < beta`` the exact estimate is

    ``kappa=M*b*(1/(eta-alpha)+1/(beta-eta))``.

    The midpoint weight minimizes the displayed upper bound and is used by
    default.  ``kappa < 1`` is the relative-history-graph gate.  It is not,
    by itself, a phase-space dichotomy certificate.
    """

    values = (
        evolution_bound,
        center_stable_rate,
        unstable_rate,
        perturbation_norm,
    )
    if not all(isfinite(float(value)) for value in values):
        raise ValueError("all roughness data must be finite")
    if evolution_bound <= 0.0:
        raise ValueError("evolution_bound must be positive")
    if center_stable_rate < 0.0:
        raise ValueError("center_stable_rate must be nonnegative")
    if unstable_rate <= center_stable_rate:
        raise ValueError("unstable_rate must exceed center_stable_rate")
    if perturbation_norm < 0.0:
        raise ValueError("perturbation_norm must be nonnegative")
    eta = (
        0.5 * (center_stable_rate + unstable_rate)
        if weight is None
        else float(weight)
    )
    if not isfinite(eta):
        raise ValueError("weight must be finite")
    if not center_stable_rate < eta < unstable_rate:
        raise ValueError("weight must lie strictly between the rates")
    contraction = evolution_bound * perturbation_norm * (
        1.0 / (eta - center_stable_rate)
        + 1.0 / (unstable_rate - eta)
    )
    closes = contraction < 1.0
    return StrongUnstableRoughnessBudget(
        center_stable_rate=float(center_stable_rate),
        unstable_rate=float(unstable_rate),
        weight=float(eta),
        perturbation_norm=float(perturbation_norm),
        contraction_constant=float(contraction),
        resolvent_bound=(
            float(1.0 / (1.0 - contraction))
            if closes
            else float("inf")
        ),
        closes=bool(closes),
    )


def physical_tracker_perturbation_bound(
    *,
    delta: float,
    weak_gain: float,
    frame_and_tracker_constant: float,
    coordinate_condition: float = 1.0,
) -> float:
    r"""Return the declared ``O(delta)`` model-fit bound.

    ``frame_and_tracker_constant*delta`` bounds the current Jacobian error
    and moving-frame terms supplied by the outer tracker.  The exact delayed
    part is ``delta**2*|K|*(8/3)`` in physical time.  A fixed coordinate
    condition number multiplies both contributions.
    """

    values = (
        delta,
        weak_gain,
        frame_and_tracker_constant,
        coordinate_condition,
    )
    if not all(isfinite(float(value)) for value in values):
        raise ValueError("all model-fit data must be finite")
    if delta <= 0.0:
        raise ValueError("delta must be positive")
    if frame_and_tracker_constant < 0.0:
        raise ValueError("frame_and_tracker_constant must be nonnegative")
    if coordinate_condition < 1.0:
        raise ValueError("coordinate_condition must be at least one")
    delay_norm = float(exact_safe_layer_history_norm())
    return float(
        coordinate_condition
        * (
            frame_and_tracker_constant * delta
            + delta**2 * abs(weak_gain) * delay_norm
        )
    )


def singular_middle_current_index(
    *,
    collective_recovery: float = -0.5,
    recovery_damping: float = 1.5,
    zero_tolerance: float = 1.0e-9,
) -> SingularCurrentIndex:
    r"""Audit the singular current-state index on a bistable layer.

    The four-by-four singular Jacobian is block triangular with the physical
    fast Jacobian above and ``-D_w P_perp`` below.  On the middle branch it
    has one positive fast eigenvalue, one exact collective zero, and two
    stable eigenvalues.  This finite-dimensional audit is not an RFDE
    spectrum calculation.
    """

    values = (collective_recovery, recovery_damping, zero_tolerance)
    if not all(isfinite(float(value)) for value in values):
        raise ValueError("all current-index data must be finite")
    if recovery_damping <= 0.0:
        raise ValueError("recovery_damping must be positive")
    if zero_tolerance <= 0.0:
        raise ValueError("zero_tolerance must be positive")
    points = equilibria_at_recovery(float(collective_recovery))
    if len(points) != 3:
        raise ValueError("collective_recovery must be in the bistable interval")
    middle = points[1]
    fast = np.array(
        [
            [0.5 - middle.voltage_1**2, 0.5],
            [2.0, -1.0 - middle.voltage_2**2],
        ],
        dtype=float,
    )
    critical_right = np.array([1.0, 2.0])
    critical_left = np.array([0.5, 0.25])
    transverse = np.eye(2) - np.outer(critical_right, critical_left)
    singular = np.block(
        [
            [fast, -np.eye(2)],
            [np.zeros((2, 2)), -recovery_damping * transverse],
        ]
    )
    eigenvalues = np.linalg.eigvals(singular)
    unstable = [value for value in eigenvalues if value.real > zero_tolerance]
    center = [value for value in eigenvalues if abs(value.real) <= zero_tolerance]
    stable = [value for value in eigenvalues if value.real < -zero_tolerance]
    if len(unstable) != 1 or len(center) != 1 or len(stable) != 2:
        raise RuntimeError("the declared one-unstable/one-center index failed")
    ordered = tuple(
        complex(value)
        for value in sorted(eigenvalues, key=lambda z: z.real)
    )
    return SingularCurrentIndex(
        collective_recovery=float(collective_recovery),
        eigenvalues=ordered,
        unstable_count=len(unstable),
        center_count=len(center),
        stable_count=len(stable),
        unstable_floor=float(unstable[0].real),
    )
