"""Exact finite-dimensional algebra audit for a two-module network.

This module checks only finite-dimensional block identities with SymPy exact
arithmetic.  It does not construct an RFDE phase space, prove persistence of a
canard, estimate a Lin inverse, or justify a network-to-module approximation.
The optional recovery scaffold below is an exact audit of a candidate model
redesign, not evidence that the redesigned RFDE has the required Fredholm
properties.

The two modules contain ``n1`` and ``n2`` nodes.  ``S`` embeds two module
values into node space and ``R`` takes exact module averages, so ``R*S=I_2``
and ``Q=S*R`` projects onto the block-constant subspace.  The frozen reference
gives each module mass one half, independent of its node count.  Consequently
its rank-one collective projector has node weights ``1/(2*n_a)`` in module
``a``; it is not the uniform average over all nodes when ``n1 != n2``.

For source-history layers ``A_k``, the exact row condition is

    A_k S = S C_k.

The audit also exposes its two independent failures: a mismatch in the
restricted 2-by-2 layer ``R A_k S-C_k`` and the transverse forcing
``(I-Q) A_k S``.  These are algebraic residuals, not RFDE error bounds.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import sympy as sp


Matrix = sp.ImmutableMatrix


def _immutable(matrix: sp.MatrixBase) -> Matrix:
    return sp.ImmutableMatrix(matrix)


def _validate_size(size: int, name: str) -> None:
    if not isinstance(size, int) or isinstance(size, bool) or size < 1:
        raise ValueError(f"{name} must be a positive integer")


@dataclass(frozen=True)
class TwoModuleBlockAlgebra:
    """Exact projectors and a collective/difference/within modal basis."""

    n1: int
    n2: int
    embedding: Matrix
    module_average: Matrix
    module_projector: Matrix
    module_metric: Matrix
    node_metric: Matrix
    module_collective_projector: Matrix
    collective_projector: Matrix
    collective_vector: Matrix
    module_difference_vector: Matrix
    within_basis: Matrix
    modal_basis: Matrix

    @property
    def node_count(self) -> int:
        return self.n1 + self.n2


def two_module_block_algebra(n1: int, n2: int) -> TwoModuleBlockAlgebra:
    """Construct exact equal-module-mass projectors for two nonempty modules."""

    _validate_size(n1, "n1")
    _validate_size(n2, "n2")
    node_count = n1 + n2

    embedding = sp.zeros(node_count, 2)
    for row in range(n1):
        embedding[row, 0] = 1
    for row in range(n1, node_count):
        embedding[row, 1] = 1

    module_average = sp.zeros(2, node_count)
    for column in range(n1):
        module_average[0, column] = sp.Rational(1, n1)
    for column in range(n1, node_count):
        module_average[1, column] = sp.Rational(1, n2)

    module_projector = embedding * module_average
    module_metric = sp.diag(sp.Rational(1, 2), sp.Rational(1, 2))
    node_metric = sp.diag(
        *(
            [sp.Rational(1, 2 * n1)] * n1
            + [sp.Rational(1, 2 * n2)] * n2
        )
    )
    collective_module_vector = sp.ones(2, 1)
    collective_weights = sp.Matrix([[sp.Rational(1, 2), sp.Rational(1, 2)]])
    module_collective_projector = (
        collective_module_vector * collective_weights
    )
    collective_projector = (
        embedding * module_collective_projector * module_average
    )

    collective_vector = sp.ones(node_count, 1)
    module_difference_vector = embedding * sp.Matrix([1, -1])

    within_columns: list[sp.Matrix] = []
    for offset, size in ((0, n1), (n1, n2)):
        anchor = offset + size - 1
        for local_index in range(size - 1):
            vector = sp.zeros(node_count, 1)
            vector[offset + local_index, 0] = 1
            vector[anchor, 0] = -1
            within_columns.append(vector)

    if within_columns:
        within_basis = sp.Matrix.hstack(*within_columns)
        modal_basis = sp.Matrix.hstack(
            collective_vector,
            module_difference_vector,
            within_basis,
        )
    else:
        within_basis = sp.zeros(node_count, 0)
        modal_basis = sp.Matrix.hstack(
            collective_vector,
            module_difference_vector,
        )

    return TwoModuleBlockAlgebra(
        n1=n1,
        n2=n2,
        embedding=_immutable(embedding),
        module_average=_immutable(module_average),
        module_projector=_immutable(module_projector),
        module_metric=_immutable(module_metric),
        node_metric=_immutable(node_metric),
        module_collective_projector=_immutable(module_collective_projector),
        collective_projector=_immutable(collective_projector),
        collective_vector=_immutable(collective_vector),
        module_difference_vector=_immutable(module_difference_vector),
        within_basis=_immutable(within_basis),
        modal_basis=_immutable(modal_basis),
    )


def fast_voltage_jacobian(
    algebra: TwoModuleBlockAlgebra,
    coupling: sp.Expr,
) -> Matrix:
    """Return ``D(P-I)`` for the rank-one collective averaging projector."""

    node_count = algebra.node_count
    return _immutable(
        sp.sympify(coupling)
        * (algebra.collective_projector - sp.eye(node_count))
    )


def full_fold_jacobian(
    algebra: TwoModuleBlockAlgebra,
    coupling: sp.Expr,
    *,
    fast_slow_entry: sp.Expr = sp.Integer(-1),
    recovery_coupling: sp.Expr = sp.Integer(0),
) -> Matrix:
    """Return the epsilon=0 fold Jacobian in ``(v,w)`` node coordinates.

    The upper-right block is the derivative of the fast voltage equation with
    respect to the slow variable; its default ``-1`` matches the frozen FHN
    convention.  The optional lower-right block is
    ``E(P-I)``, where ``E=recovery_coupling``.  It represents a candidate fixed
    recovery-variable synchronizer that vanishes on the collective mode.

    With ``E=0`` and a nonzero fast-slow entry, the collective zero eigenvalue
    belongs to a length-two Jordan chain while every recovery direction has
    zero eigenvalue.  The algebraic/generalized-center multiplicity is then
    ``N+1`` and the ordinary kernel dimension is ``N``.

    With nonzero ``D`` and ``E``, every transverse ``(v,w)`` block is
    ``[[-D, fast_slow_entry], [0, -E]]``.  Only the collective length-two
    Jordan block remains at zero, so its algebraic/generalized-center
    multiplicity is two and its ordinary kernel dimension is one.  These are
    finite-dimensional identities, not an RFDE Fredholm or Lin-inverse proof.
    """

    node_count = algebra.node_count
    voltage = fast_voltage_jacobian(algebra, coupling)
    fast_slow = sp.sympify(fast_slow_entry) * sp.eye(node_count)
    recovery = fast_voltage_jacobian(algebra, recovery_coupling)
    zero = sp.zeros(node_count, node_count)
    return _immutable(
        sp.Matrix.vstack(
            sp.Matrix.hstack(voltage, fast_slow),
            sp.Matrix.hstack(zero, recovery),
        )
    )


def uniform_history_layer(
    algebra: TwoModuleBlockAlgebra,
    module_layer: sp.MatrixBase,
) -> Matrix:
    """Lift a 2-by-2 source-history layer with uniform source-block weights."""

    module_layer = sp.Matrix(module_layer)
    if module_layer.shape != (2, 2):
        raise ValueError("module_layer must be 2-by-2")
    return _immutable(
        algebra.embedding * module_layer * algebra.module_average
    )


@dataclass(frozen=True)
class HistoryLayerAudit:
    """Exact restriction and transverse residuals for source-history layers."""

    restrictions: tuple[Matrix, ...]
    declared_layers: tuple[Matrix, ...]
    restriction_mismatches: tuple[Matrix, ...]
    declared_row_residuals: tuple[Matrix, ...]
    transverse_forcing: tuple[Matrix, ...]
    eta_squared: sp.Expr


def audit_source_history_layers(
    algebra: TwoModuleBlockAlgebra,
    full_layers: Iterable[sp.MatrixBase],
    declared_layers: Iterable[sp.MatrixBase],
) -> HistoryLayerAudit:
    """Audit a finite collection of delayed source-history layer matrices.

    For layer ``k``, exact closure with the declared module matrix ``C_k`` is
    ``A_k*S=S*C_k``.  The identity

    ``A_k*S = S*C_k + declared_row_residual_k``

    is exact regardless of closure.  ``eta_squared`` is the sum of squared
    Frobenius norms of ``(I-Q)A_kS``; it records only transverse forcing and is
    not a norm on RFDE histories.
    """

    full_tuple = tuple(sp.Matrix(layer) for layer in full_layers)
    declared_tuple = tuple(sp.Matrix(layer) for layer in declared_layers)
    if not full_tuple:
        raise ValueError("at least one source-history layer is required")
    if len(full_tuple) != len(declared_tuple):
        raise ValueError("full_layers and declared_layers must have equal length")

    node_count = algebra.node_count
    identity = sp.eye(node_count)
    restrictions: list[Matrix] = []
    immutable_declared: list[Matrix] = []
    restriction_mismatches: list[Matrix] = []
    declared_row_residuals: list[Matrix] = []
    transverse_forcing: list[Matrix] = []
    eta_squared = sp.Integer(0)

    for full_layer, declared_layer in zip(full_tuple, declared_tuple, strict=True):
        if full_layer.shape != (node_count, node_count):
            raise ValueError(
                f"each full layer must be {node_count}-by-{node_count}"
            )
        if declared_layer.shape != (2, 2):
            raise ValueError("each declared layer must be 2-by-2")

        restriction = algebra.module_average * full_layer * algebra.embedding
        mismatch = restriction - declared_layer
        row_residual = (
            full_layer * algebra.embedding
            - algebra.embedding * declared_layer
        )
        transverse = (
            (identity - algebra.module_projector)
            * full_layer
            * algebra.embedding
        )

        restrictions.append(_immutable(restriction))
        immutable_declared.append(_immutable(declared_layer))
        restriction_mismatches.append(_immutable(mismatch))
        declared_row_residuals.append(_immutable(row_residual))
        transverse_forcing.append(_immutable(transverse))
        eta_squared += sp.trace(transverse.T * transverse)

    return HistoryLayerAudit(
        restrictions=tuple(restrictions),
        declared_layers=tuple(immutable_declared),
        restriction_mismatches=tuple(restriction_mismatches),
        declared_row_residuals=tuple(declared_row_residuals),
        transverse_forcing=tuple(transverse_forcing),
        eta_squared=sp.simplify(eta_squared),
    )
