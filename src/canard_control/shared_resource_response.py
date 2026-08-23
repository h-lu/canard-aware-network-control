"""Exact leading-response audit for the shared-resource network class.

The calculation isolates the interior, projection-neutral transverse return
along the singular canard.  It does not construct selected traces or a
complete-history root; endpoint and preparation terms remain separate.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import sympy as sp


Matrix = sp.ImmutableMatrix


@dataclass(frozen=True)
class SharedResourceResponseAudit:
    """Exact certificates for the order-three interior cancellation."""

    transition: Matrix
    stationary: Matrix
    critical_projector: Matrix
    transverse_projector: Matrix
    stable_generator: Matrix
    transverse_inverse: Matrix
    base_first_moment: Matrix
    direction_first_moment: Matrix
    direct_projected_atoms: tuple[sp.Expr, ...]
    transverse_moment_forcing: Matrix
    base_stable_jet: Matrix
    first_stable_direction_jet: Matrix
    stable_jet_is_transverse: sp.Expr
    direction_on_base_constant: sp.Expr
    constant_history_return: sp.Expr
    interior_order_three_response: sp.Expr


def shared_resource_response_audit(
    transition: sp.MatrixBase,
    stationary: sp.MatrixBase,
    base_layers: Sequence[sp.MatrixBase],
    direction_layers: Sequence[sp.MatrixBase],
    delays: Sequence[sp.Expr],
    *,
    coupling_rate: sp.Expr = sp.Integer(1),
    weak_gain: sp.Expr = sp.Integer(1),
) -> SharedResourceResponseAudit:
    """Return the exact projection-neutral interior-response certificate.

    ``transition`` is row stochastic, ``stationary`` is its invariant
    probability column, and all delay atoms are fixed.  The structural
    direction must preserve the complete critical projected delay measure,
    meaning ``stationary.T * direction_layer * 1 == 0`` at every atom.

    The inverse on the transverse space is represented on the ambient space
    by ``(A + P_c)^(-1) P_perp``.  The calculation assumes that this matrix is
    invertible, which is the finite-dimensional counterpart of the declared
    transverse semigroup gap.
    """

    transition_m = sp.Matrix(transition)
    stationary_m = sp.Matrix(stationary)
    if transition_m.rows < 2 or transition_m.rows != transition_m.cols:
        raise ValueError("transition must be square with at least two nodes")
    node_count = transition_m.rows
    if stationary_m.shape == (node_count,):
        stationary_m = stationary_m.reshape(node_count, 1)
    if stationary_m.shape != (node_count, 1):
        raise ValueError("stationary must be a compatible column")
    if not (
        len(base_layers) == len(direction_layers) == len(delays)
        and len(delays) > 0
    ):
        raise ValueError("base layers, directions, and delays must align")

    ones = sp.ones(node_count, 1)
    if sp.simplify(transition_m * ones - ones) != sp.zeros(node_count, 1):
        raise ValueError("transition must be row stochastic")
    if sp.simplify(stationary_m.T * transition_m - stationary_m.T) != (
        sp.zeros(1, node_count)
    ):
        raise ValueError("stationary must be invariant")
    if sp.simplify((stationary_m.T * ones)[0] - 1) != 0:
        raise ValueError("stationary must sum to one")

    base = [sp.Matrix(layer) for layer in base_layers]
    direction = [sp.Matrix(layer) for layer in direction_layers]
    if any(layer.shape != (node_count, node_count) for layer in base + direction):
        raise ValueError("all layers must match the transition dimension")

    delay_values = [sp.sympify(delay) for delay in delays]
    rate = sp.sympify(coupling_rate)
    gain = sp.sympify(weak_gain)
    critical = ones * stationary_m.T
    transverse = sp.eye(node_count) - critical
    generator = sp.expand(rate * (transition_m - sp.eye(node_count)))
    transverse_inverse = sp.simplify(
        (generator + critical).inv() * transverse
    )

    direct_atoms = tuple(
        sp.simplify((stationary_m.T * layer * ones)[0])
        for layer in direction
    )
    if any(value != 0 for value in direct_atoms):
        raise ValueError(
            "direction must preserve the complete projected delay measure"
        )

    base_moment = sp.zeros(node_count)
    direction_moment = sp.zeros(node_count)
    for delay, base_layer, direction_layer in zip(
        delay_values, base, direction
    ):
        base_moment += delay * base_layer
        direction_moment += delay * direction_layer
    base_moment = sp.simplify(base_moment)
    direction_moment = sp.simplify(direction_moment)

    forcing = sp.simplify(transverse * direction_moment * ones)
    base_forcing = sp.simplify(transverse * base_moment * ones)
    base_stable_jet = sp.simplify(gain * transverse_inverse * base_forcing / 2)
    stable_jet = sp.simplify(gain * transverse_inverse * forcing / 2)
    stable_transversality = sp.simplify((stationary_m.T * stable_jet)[0])

    # Every balanced delay operator annihilates a constant history.  The
    # first stable response along X_0(s)=-s/2 is constant because
    # X_0(s)-X_0(s-theta)=-theta/2.  Hence its stable-to-critical delayed
    # return, which is the only possible interior order-three term, is zero.
    total_base = sum(base, sp.zeros(node_count))
    total_direction = sum(direction, sp.zeros(node_count))
    direction_on_base = sp.simplify(
        (
            stationary_m.T
            * (
                total_direction * base_stable_jet
                - sum(
                    (layer * base_stable_jet for layer in direction),
                    sp.zeros(node_count, 1),
                )
            )
        )[0]
    )
    constant_return = sp.simplify(
        (
            stationary_m.T
            * (total_base * stable_jet - sum(
                (layer * stable_jet for layer in base),
                sp.zeros(node_count, 1),
            ))
        )[0]
    )
    order_three = sp.simplify(gain * constant_return)

    return SharedResourceResponseAudit(
        transition=Matrix(transition_m),
        stationary=Matrix(stationary_m),
        critical_projector=Matrix(critical),
        transverse_projector=Matrix(transverse),
        stable_generator=Matrix(generator),
        transverse_inverse=Matrix(transverse_inverse),
        base_first_moment=Matrix(base_moment),
        direction_first_moment=Matrix(direction_moment),
        direct_projected_atoms=direct_atoms,
        transverse_moment_forcing=Matrix(forcing),
        base_stable_jet=Matrix(base_stable_jet),
        first_stable_direction_jet=Matrix(stable_jet),
        stable_jet_is_transverse=stable_transversality,
        direction_on_base_constant=direction_on_base,
        constant_history_return=constant_return,
        interior_order_three_response=order_three,
    )
