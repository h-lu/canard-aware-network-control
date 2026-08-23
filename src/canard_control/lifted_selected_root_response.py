"""Exact symmetry algebra behind the arbitrary-size selected-root lift.

The analytic selected-history theorem is stated and proved in
``docs/paper-ii-selected-root-lift-and-symmetry-breaking.md``.  This module
checks its finite-dimensional representation-theoretic identities.  It does
not construct the invariant history graph or the one-sided selected traces.

There are two distinct structural directions:

* ``S*T*R`` is the equitable module-difference direction inherited from the
  two-module theorem;
* ``G=u*rho`` has zero module-average output and breaks equitability.

The within-module permutation Reynolds projection kills ``G``.  Hence every
relabeling-invariant *linear* scalar response reads the combined direction
``S*T*R + kappa*G`` exactly as ``S*T*R``.  This is a first-response identity,
not a claim that the nonlinear roots agree away from zero amplitude.
"""

from __future__ import annotations

from dataclasses import dataclass
from collections.abc import Sequence

import sympy as sp

from canard_control.lifted_two_module_network import (
    LiftedTwoModuleNetwork,
    equitability_breaking_redistribution,
)


Matrix = sp.ImmutableMatrix


def _immutable(matrix: sp.MatrixBase) -> Matrix:
    return sp.ImmutableMatrix(matrix)


def module_permutation_matrix(
    network: LiftedTwoModuleNetwork,
    module: int,
    permutation: Sequence[int],
) -> Matrix:
    """Return a node permutation acting only inside one declared module.

    ``permutation[j]`` is the new local row occupied by the old local index
    ``j``.  The convention is immaterial for conjugacy tests as long as it is
    used consistently.  A genuine permutation of ``range(n_module)`` is
    required.
    """

    if module not in (1, 2):
        raise ValueError("module must be 1 or 2")
    size = network.n1 if module == 1 else network.n2
    if tuple(sorted(permutation)) != tuple(range(size)):
        raise ValueError("permutation must contain every local index once")
    offset = 0 if module == 1 else network.n1
    matrix = sp.eye(network.node_count)
    for local_row in range(size):
        for local_column in range(size):
            matrix[offset + local_row, offset + local_column] = 0
    for old_local, new_local in enumerate(permutation):
        matrix[offset + new_local, offset + old_local] = 1
    return _immutable(matrix)


@dataclass(frozen=True)
class SymmetryBreakingResponseAudit:
    """Exact layer and Reynolds identities for one non-equitable tangent."""

    module_direction: Matrix
    within_generator: Matrix
    combined_layer_0_direction: Matrix
    combined_layer_1_direction: Matrix
    reynolds_within_generator: Matrix
    reynolds_combined_layer_0_direction: Matrix
    module_restriction_0: Matrix
    module_restriction_1: Matrix
    critical_pairing_0: sp.Expr
    critical_pairing_1: sp.Expr
    total_direction: Matrix
    equitability_defect: Matrix


def symmetry_breaking_response_audit(
    network: LiftedTwoModuleNetwork,
    *,
    kappa: sp.Expr = sp.Integer(1),
    receiving_module: int = 1,
    source_module: int = 1,
) -> SymmetryBreakingResponseAudit:
    r"""Audit ``D_0=S*T*R+kappa*G`` and ``D_1=-D_0`` exactly.

    The rank-one generator ``G=u*rho`` is the distributed zero-mean family
    from :func:`equitability_breaking_redistribution`, at unit amplitude.
    Since ``G*Q=G`` and ``Q*G=0``, where ``Q=S*R``, averaging its conjugates
    over all within-module permutations gives zero.  The Reynolds projection
    of the combined direction is therefore precisely ``S*T*R``.
    """

    kappa = sp.sympify(kappa)
    breaker = equitability_breaking_redistribution(
        network,
        sp.Integer(1),
        receiving_module=receiving_module,
        source_module=source_module,
        receiving_pattern="distributed",
    )
    generator = sp.Matrix(breaker.generator)
    module_t = sp.Matrix([[1, 0], [-2, 0]])
    lifted_t = sp.Matrix(network.embedding * module_t * network.module_average)
    direction_0 = sp.simplify(lifted_t + kappa * generator)
    direction_1 = -direction_0

    # For this rank-one family the source covector is fixed by every
    # within-module permutation.  Hence the conjugacy Reynolds average is
    # (average P)*G = Q*G = 0.  The commonly guessed formula Q*G*Q is not
    # the conjugacy average of a general matrix.
    q = sp.Matrix(network.module_projector)
    if sp.simplify(generator * q - generator) != sp.zeros(network.node_count):
        raise AssertionError("the source functional must be permutation invariant")
    if sp.simplify(q * generator) != sp.zeros(network.node_count):
        raise AssertionError("the receiving vector must have zero module average")
    reynolds_generator = sp.simplify(q * generator)
    reynolds_direction = sp.simplify(lifted_t + kappa * reynolds_generator)

    r = sp.Matrix(network.critical_right)
    ell = sp.Matrix(network.critical_left)
    defect = sp.simplify(
        network.within_projector * direction_0 * network.embedding
    )

    return SymmetryBreakingResponseAudit(
        module_direction=_immutable(lifted_t),
        within_generator=_immutable(generator),
        combined_layer_0_direction=_immutable(direction_0),
        combined_layer_1_direction=_immutable(direction_1),
        reynolds_within_generator=_immutable(reynolds_generator),
        reynolds_combined_layer_0_direction=_immutable(reynolds_direction),
        module_restriction_0=_immutable(
            network.module_average * direction_0 * network.embedding
        ),
        module_restriction_1=_immutable(
            network.module_average * direction_1 * network.embedding
        ),
        critical_pairing_0=sp.simplify((ell.T * direction_0 * r)[0]),
        critical_pairing_1=sp.simplify((ell.T * direction_1 * r)[0]),
        total_direction=_immutable(sp.simplify(direction_0 + direction_1)),
        equitability_defect=_immutable(defect),
    )


def balanced_sign_swap_permutation(
    network: LiftedTwoModuleNetwork,
    *,
    receiving_module: int,
) -> Matrix | None:
    """Return a permutation sending the distributed breaker ``u`` to ``-u``.

    Such a permutation exists for the declared distributed construction when
    the receiving-module size is even.  For odd size the two level sets have
    different cardinalities, so this function returns ``None``.  The latter
    does not obstruct the Reynolds first-response cancellation.
    """

    if receiving_module not in (1, 2):
        raise ValueError("receiving_module must be 1 or 2")
    size = network.n1 if receiving_module == 1 else network.n2
    if size % 2:
        return None
    half = size // 2
    permutation = tuple(range(half, size)) + tuple(range(half))
    return module_permutation_matrix(network, receiving_module, permutation)


def canonical_root_response_coefficient(
    coupling: sp.Expr,
    delay_0: sp.Expr,
    delay_1: sp.Expr,
) -> sp.Expr:
    r"""Return the inherited coefficient ``K*(theta_0-theta_1)/(4*alpha)``."""

    alpha = sp.sqrt(6) / 4
    return sp.simplify(
        sp.sympify(coupling)
        * (sp.sympify(delay_0) - sp.sympify(delay_1))
        / (4 * alpha)
    )
