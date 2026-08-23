"""Exact response identities for a heterogeneous-curvature canard network.

The module checks the finite-dimensional algebra behind the selected-root
theorem in ``docs/paper-ii-heterogeneous-curvature-selected-root.md``.  It
does not numerically construct the invariant history graph or the selected
traces; those are analytic objects in the accompanying theorem.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import sympy as sp


Matrix = sp.ImmutableMatrix


def _column(value: sp.MatrixBase, size: int, name: str) -> sp.Matrix:
    result = sp.Matrix(value)
    if result.shape == (size,):
        result = result.reshape(size, 1)
    if result.shape != (size, 1):
        raise ValueError(f"{name} must be a compatible column")
    return result


@dataclass(frozen=True)
class HeterogeneousCurvatureRootAudit:
    """Exact Schur--Melnikov data for one finite network."""

    transition: Matrix
    stationary: Matrix
    curvature: Matrix
    critical_projector: Matrix
    transverse_projector: Matrix
    stable_generator: Matrix
    transverse_inverse: Matrix
    mean_curvature: sp.Expr
    leading_stable_shift: Matrix
    local_cubic_coefficient: sp.Expr
    leading_root: sp.Expr
    direction_first_moment: Matrix
    full_row_projection_atoms: tuple[Matrix, ...]
    transverse_delay_forcing: Matrix
    first_stable_direction_jet: Matrix
    critical_hessian_return: sp.Expr
    q2_melnikov_pairing: sp.Expr
    selected_root_shift_coefficient: sp.Expr


def heterogeneous_curvature_root_audit(
    transition: sp.MatrixBase,
    stationary: sp.MatrixBase,
    curvature: sp.MatrixBase,
    direction_layers: Sequence[sp.MatrixBase],
    delays: Sequence[sp.Expr],
    *,
    coupling_rate: sp.Expr = sp.Integer(1),
    weak_gain: sp.Expr = sp.Integer(1),
    cubic_coefficient: sp.Expr = sp.Integer(1),
) -> HeterogeneousCurvatureRootAudit:
    """Compute the exact projection-neutral root-response coefficient.

    ``transition`` is row stochastic and ``stationary.T`` is invariant.
    Every structural delay layer must satisfy the stronger neutrality
    identity ``stationary.T * R_k == 0``.  This removes the structural
    direction from the critical delay equation for every history, not only
    for the collective history.

    The ambient representation

    ``(A + P_c)^(-1) P_perp``

    is the inverse of ``A = rate * (transition - I)`` on the stationary
    transverse space.  Invertibility is checked exactly for the supplied
    finite matrix.
    """

    transition_m = sp.Matrix(transition)
    if transition_m.rows < 2 or transition_m.rows != transition_m.cols:
        raise ValueError("transition must be square with at least two nodes")
    node_count = transition_m.rows
    stationary_m = _column(stationary, node_count, "stationary")
    curvature_m = _column(curvature, node_count, "curvature")
    if len(direction_layers) != len(delays) or not delays:
        raise ValueError("direction layers and delays must be nonempty and align")

    ones = sp.ones(node_count, 1)
    if any(entry.is_nonnegative is not True for entry in transition_m):
        raise ValueError("transition entries must be known nonnegative")
    if any(entry.is_positive is not True for entry in stationary_m):
        raise ValueError("stationary entries must be known positive")
    if any(entry.is_positive is not True for entry in curvature_m):
        raise ValueError("curvature entries must be known positive")
    if sp.simplify(transition_m * ones - ones) != sp.zeros(node_count, 1):
        raise ValueError("transition must be row stochastic")
    if sp.simplify(stationary_m.T * transition_m - stationary_m.T) != (
        sp.zeros(1, node_count)
    ):
        raise ValueError("stationary must be invariant")
    if sp.simplify((stationary_m.T * ones)[0] - 1) != 0:
        raise ValueError("stationary must sum to one")

    layers = [sp.Matrix(layer) for layer in direction_layers]
    if any(layer.shape != (node_count, node_count) for layer in layers):
        raise ValueError("every direction layer must match the network")
    row_projections = tuple(
        sp.ImmutableMatrix(sp.simplify(stationary_m.T * layer))
        for layer in layers
    )
    if any(row != sp.zeros(1, node_count) for row in row_projections):
        raise ValueError("every direction layer must satisfy pi.T * R_k == 0")

    rate = sp.sympify(coupling_rate)
    gain = sp.sympify(weak_gain)
    cubic = sp.sympify(cubic_coefficient)
    if rate.is_positive is not True:
        raise ValueError("coupling_rate must be known positive")
    if gain.is_zero is not False:
        raise ValueError("weak_gain must be known nonzero")
    if cubic.is_positive is not True:
        raise ValueError("cubic_coefficient must be known positive")
    critical = ones * stationary_m.T
    transverse = sp.eye(node_count) - critical
    generator = sp.expand(rate * (transition_m - sp.eye(node_count)))
    transverse_inverse = sp.simplify((generator + critical).inv() * transverse)

    mean_curvature = sp.simplify((stationary_m.T * curvature_m)[0])
    if mean_curvature == 0:
        raise ValueError("mean fold curvature must be nonzero")
    stable_shift = sp.simplify(
        transverse_inverse * transverse * curvature_m
    )
    curvature_return = sp.simplify(
        (stationary_m.T * sp.diag(*curvature_m) * stable_shift)[0]
    )
    local_cubic = sp.simplify(cubic / 3 + 2 * curvature_return)
    leading_root = sp.simplify(
        -3 * local_cubic / (8 * mean_curvature**3)
    )

    first_moment = sp.zeros(node_count)
    for delay, layer in zip(delays, layers):
        first_moment += sp.sympify(delay) * layer
    first_moment = sp.simplify(first_moment)
    forcing = sp.simplify(transverse * first_moment * ones)

    # Along X_0(s)=-s/(2*mean_curvature), the balanced delay difference is
    # X_0(s)-X_0(s-theta)=-theta/(2*mean_curvature).
    stable_direction = sp.simplify(
        gain
        * transverse_inverse
        * forcing
        / (2 * mean_curvature)
    )
    hessian_return = sp.simplify(
        (
            stationary_m.T
            * sp.diag(*curvature_m)
            * stable_direction
        )[0]
    )
    melnikov_pairing = sp.simplify(
        sp.sqrt(2 * sp.pi) * hessian_return / mean_curvature
    )
    root_coefficient = sp.simplify(
        -hessian_return / mean_curvature
    )

    return HeterogeneousCurvatureRootAudit(
        transition=Matrix(transition_m),
        stationary=Matrix(stationary_m),
        curvature=Matrix(curvature_m),
        critical_projector=Matrix(critical),
        transverse_projector=Matrix(transverse),
        stable_generator=Matrix(generator),
        transverse_inverse=Matrix(transverse_inverse),
        mean_curvature=mean_curvature,
        leading_stable_shift=Matrix(stable_shift),
        local_cubic_coefficient=local_cubic,
        leading_root=leading_root,
        direction_first_moment=Matrix(first_moment),
        full_row_projection_atoms=row_projections,
        transverse_delay_forcing=Matrix(forcing),
        first_stable_direction_jet=Matrix(stable_direction),
        critical_hessian_return=hessian_return,
        q2_melnikov_pairing=melnikov_pairing,
        selected_root_shift_coefficient=root_coefficient,
    )


@dataclass(frozen=True)
class NormalizedNoSynchronyQuotientFamily:
    """A positive-layer witness with no nontrivial synchrony quotient."""

    node_count: int
    transition: Matrix
    stationary: Matrix
    heterogeneity_profile: Matrix
    curvature: Matrix
    base_layers: tuple[Matrix, Matrix]
    direction_layers: tuple[Matrix, Matrix]
    delays: tuple[sp.Expr, sp.Expr]
    positivity_radius: sp.Expr
    profile_mean: sp.Expr
    profile_variance: sp.Expr
    curvature_entries_are_distinct: bool
    audit: HeterogeneousCurvatureRootAudit


def normalized_no_synchrony_quotient_family(
    node_count: int,
    *,
    curvature_amplitude: sp.Expr,
    layer_floor: sp.Expr,
    delay_0: sp.Expr,
    delay_1: sp.Expr,
    coupling_rate: sp.Expr = sp.Integer(1),
    weak_gain: sp.Expr = sp.Integer(1),
    cubic_coefficient: sp.Expr = sp.Integer(1),
) -> NormalizedNoSynchronyQuotientFamily:
    """Return an exact all-``N`` family with a constant nonzero coefficient.

    The centered grid profile has mean zero, variance one, pairwise distinct
    entries, and sup norm below ``sqrt(3)``.  The base delay layers are
    positive multiples of the collective projector.  The two signed
    directions are opposite rank-one layers.  Consequently
    ``B_k + zeta R_k`` stays entrywise positive for
    ``|zeta| < positivity_radius``.
    """

    if node_count < 2:
        raise ValueError("node_count must be at least two")
    sigma = sp.sympify(curvature_amplitude)
    floor = sp.sympify(layer_floor)
    theta_0 = sp.sympify(delay_0)
    theta_1 = sp.sympify(delay_1)
    rate = sp.sympify(coupling_rate)
    gain = sp.sympify(weak_gain)
    cubic = sp.sympify(cubic_coefficient)
    if sp.simplify(theta_1 - theta_0).is_positive is not True:
        raise ValueError("delays must satisfy delay_0 < delay_1")
    if floor.is_positive is not True:
        raise ValueError("layer_floor must be known positive")
    if rate.is_positive is not True:
        raise ValueError("coupling_rate must be known positive")
    if sigma.is_positive is not True or sp.simplify(
        1 / sp.sqrt(3) - sigma
    ).is_positive is not True:
        raise ValueError(
            "curvature_amplitude must be known to lie in (0, 1/sqrt(3))"
        )

    n = sp.Integer(node_count)
    stationary = sp.ones(node_count, 1) / n
    critical = sp.ones(node_count, 1) * stationary.T
    profile_scale = sp.sqrt(3) / sp.sqrt((n - 1) * (n + 1))
    profile = sp.Matrix(
        [
            (2 * sp.Integer(index) - n - 1) * profile_scale
            for index in range(1, node_count + 1)
        ]
    )
    curvature = sp.ones(node_count, 1) + sigma * profile
    base = floor * critical
    direction = profile * stationary.T
    delays = (theta_0, theta_1)
    direction_layers = (direction, -direction)
    audit = heterogeneous_curvature_root_audit(
        critical,
        stationary,
        curvature,
        direction_layers,
        delays,
        coupling_rate=rate,
        weak_gain=gain,
        cubic_coefficient=cubic,
    )

    max_profile = sp.sqrt(3 * (n - 1) / (n + 1))
    positivity_radius = sp.simplify(floor / max_profile)
    entries = list(profile)
    distinct = all(
        sp.simplify(entries[index] - entries[other]) != 0
        for index in range(node_count)
        for other in range(index)
    )
    return NormalizedNoSynchronyQuotientFamily(
        node_count=node_count,
        transition=Matrix(critical),
        stationary=Matrix(stationary),
        heterogeneity_profile=Matrix(profile),
        curvature=Matrix(curvature),
        base_layers=(Matrix(base), Matrix(base)),
        direction_layers=(Matrix(direction), Matrix(-direction)),
        delays=delays,
        positivity_radius=positivity_radius,
        profile_mean=sp.simplify((stationary.T * profile)[0]),
        profile_variance=sp.simplify(
            (stationary.T * profile.applyfunc(lambda x: x**2))[0]
        ),
        curvature_entries_are_distinct=distinct,
        audit=audit,
    )
