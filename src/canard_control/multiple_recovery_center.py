"""Exact algebra for a delayed FHN network with independent recoveries.

The calculations concern the singular current-state Jacobian.  They do not
construct an RFDE center manifold, a Lin operator, selected endpoint traces,
or a physical canard.  The accompanying note states those boundaries.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import sympy as sp


Matrix = sp.ImmutableMatrix


def _immutable(matrix: sp.MatrixBase) -> Matrix:
    return sp.ImmutableMatrix(matrix)


def collective_projector(
    node_count: int, weights: Iterable[sp.Expr] | None = None
) -> Matrix:
    """Return the rank-one projector 1 ell^T with ell^T 1 = 1."""

    if node_count < 1:
        raise ValueError("node_count must be positive")
    if weights is None:
        ell = sp.Matrix(
            [[sp.Rational(1, node_count) for _ in range(node_count)]]
        )
    else:
        entries = tuple(sp.sympify(value) for value in weights)
        if len(entries) != node_count:
            raise ValueError("weights must have node_count entries")
        total = sp.simplify(sum(entries))
        if total == 0:
            raise ValueError("weights must have nonzero sum")
        ell = sp.Matrix([[sp.simplify(value / total) for value in entries]])
    ones = sp.ones(node_count, 1)
    return _immutable(ones * ell)


def singular_voltage_matrix(
    node_count: int,
    transverse_rate: sp.Expr = sp.Integer(1),
    weights: Iterable[sp.Expr] | None = None,
) -> Matrix:
    """Return the fold voltage Jacobian -D_v (I-P)."""

    rate = sp.sympify(transverse_rate)
    if rate == 0:
        raise ValueError("transverse_rate must be nonzero")
    projector = sp.Matrix(collective_projector(node_count, weights))
    return _immutable(-rate * (sp.eye(node_count) - projector))


def singular_current_jacobian(voltage_matrix: sp.MatrixBase) -> Matrix:
    """Return the block matrix [[A,-I],[0,0]]."""

    matrix = sp.Matrix(voltage_matrix)
    if matrix.rows != matrix.cols:
        raise ValueError("voltage_matrix must be square")
    node_count = matrix.rows
    return _immutable(
        matrix.row_join(-sp.eye(node_count)).col_join(
            sp.zeros(node_count, 2 * node_count)
        )
    )


def positive_epsilon_jacobian(
    voltage_matrix: sp.MatrixBase, epsilon: sp.Expr
) -> Matrix:
    """Return the block matrix [[A,-I],[epsilon I,0]]."""

    matrix = sp.Matrix(voltage_matrix)
    if matrix.rows != matrix.cols:
        raise ValueError("voltage_matrix must be square")
    node_count = matrix.rows
    eps = sp.sympify(epsilon)
    top = matrix.row_join(-sp.eye(node_count))
    bottom = (eps * sp.eye(node_count)).row_join(
        sp.zeros(node_count, node_count)
    )
    return _immutable(top.col_join(bottom))


@dataclass(frozen=True)
class MultipleRecoveryCenterAudit:
    """Exact singular-center decomposition."""

    node_count: int
    collective_projector: Matrix
    transverse_projector: Matrix
    voltage_matrix: Matrix
    singular_jacobian: Matrix
    fold_eigenvector: Matrix
    fold_generalized_vector: Matrix
    transverse_voltage_basis: Matrix
    transverse_center_basis: Matrix
    generalized_center_basis: Matrix
    kernel_dimension: int
    generalized_center_dimension: int
    post_phase_center_coordinate_count: int
    transverse_center_coordinate_count: int


def multiple_recovery_center_audit(
    node_count: int,
    transverse_rate: sp.Expr = sp.Integer(1),
    weights: Iterable[sp.Expr] | None = None,
) -> MultipleRecoveryCenterAudit:
    """Construct the fold chain and all recovery-center modes."""

    projector = sp.Matrix(collective_projector(node_count, weights))
    transverse = sp.eye(node_count) - projector
    voltage = sp.Matrix(
        singular_voltage_matrix(node_count, transverse_rate, weights)
    )
    jacobian = sp.Matrix(singular_current_jacobian(voltage))

    ones = sp.ones(node_count, 1)
    zeros = sp.zeros(node_count, 1)
    fold_eigenvector = ones.col_join(zeros)
    fold_generalized_vector = zeros.col_join(-ones)

    ell = projector[0, :]
    transverse_vectors = ell.nullspace()
    if transverse_vectors:
        transverse_voltage_basis = sp.Matrix.hstack(*transverse_vectors)
        transverse_center_basis = sp.Matrix.hstack(
            *[
                vector.col_join(voltage * vector)
                for vector in transverse_vectors
            ]
        )
        generalized_center_basis = sp.Matrix.hstack(
            fold_eigenvector,
            fold_generalized_vector,
            transverse_center_basis,
        )
    else:
        transverse_voltage_basis = sp.zeros(node_count, 0)
        transverse_center_basis = sp.zeros(2 * node_count, 0)
        generalized_center_basis = sp.Matrix.hstack(
            fold_eigenvector, fold_generalized_vector
        )

    kernel_dimension = 2 * node_count - jacobian.rank()
    square = jacobian**2
    generalized_center_dimension = 2 * node_count - square.rank()

    return MultipleRecoveryCenterAudit(
        node_count=node_count,
        collective_projector=_immutable(projector),
        transverse_projector=_immutable(transverse),
        voltage_matrix=_immutable(voltage),
        singular_jacobian=_immutable(jacobian),
        fold_eigenvector=_immutable(fold_eigenvector),
        fold_generalized_vector=_immutable(fold_generalized_vector),
        transverse_voltage_basis=_immutable(transverse_voltage_basis),
        transverse_center_basis=_immutable(transverse_center_basis),
        generalized_center_basis=_immutable(generalized_center_basis),
        kernel_dimension=kernel_dimension,
        generalized_center_dimension=generalized_center_dimension,
        post_phase_center_coordinate_count=node_count,
        transverse_center_coordinate_count=node_count - 1,
    )


@dataclass(frozen=True)
class GeneralizedCenterCoordinates:
    """Coordinates (a,b,q) on ker(J_0^2)."""

    fold_eigen_coordinate: sp.Expr
    fold_generalized_coordinate: sp.Expr
    transverse_voltage: Matrix
    reconstruction: Matrix
    residual: Matrix


def generalized_center_coordinates(
    state: sp.MatrixBase,
    voltage_matrix: sp.MatrixBase,
    projector: sp.MatrixBase,
) -> GeneralizedCenterCoordinates:
    """Decompose a generalized-center state as (a r+q, A q-b r)."""

    matrix = sp.Matrix(voltage_matrix)
    projection = sp.Matrix(projector)
    node_count = matrix.rows
    vector = sp.Matrix(state)
    if matrix.shape != (node_count, node_count):
        raise ValueError("voltage_matrix must be square")
    if projection.shape != matrix.shape:
        raise ValueError("projector has incompatible shape")
    if vector.shape != (2 * node_count, 1):
        raise ValueError("state must be a 2N column")

    ones = sp.ones(node_count, 1)
    ell = projection[0, :]
    voltage = vector[:node_count, :]
    recovery = vector[node_count:, :]
    a = sp.simplify((ell * voltage)[0])
    b = sp.simplify(-(ell * recovery)[0])
    q = sp.simplify((sp.eye(node_count) - projection) * voltage)
    reconstruction = (a * ones + q).col_join(matrix * q - b * ones)
    residual = sp.simplify(vector - reconstruction)
    return GeneralizedCenterCoordinates(
        fold_eigen_coordinate=a,
        fold_generalized_coordinate=b,
        transverse_voltage=_immutable(q),
        reconstruction=_immutable(reconstruction),
        residual=_immutable(residual),
    )


def no_delay_characteristic_factor(
    node_count: int,
    spectral_parameter: sp.Expr,
    epsilon: sp.Expr,
    transverse_rate: sp.Expr,
) -> sp.Expr:
    """Closed characteristic determinant for the rank-one fold model."""

    if node_count < 1:
        raise ValueError("node_count must be positive")
    lam = sp.sympify(spectral_parameter)
    eps = sp.sympify(epsilon)
    rate = sp.sympify(transverse_rate)
    return sp.expand(
        (lam**2 + eps) * (lam**2 + rate * lam + eps) ** (node_count - 1)
    )


def rescaled_slow_limit_factor(
    node_count: int, slow_parameter: sp.Expr, transverse_rate: sp.Expr
) -> sp.Expr:
    """Limit determinant at lambda=epsilon*zeta."""

    if node_count < 1:
        raise ValueError("node_count must be positive")
    zeta = sp.sympify(slow_parameter)
    rate = sp.sympify(transverse_rate)
    return sp.expand((1 + rate * zeta) ** (node_count - 1))


def linear_matching_parameter_lower_bound_for_transverse_center(
    node_count: int,
) -> int:
    """Rank lower bound if all transverse center coordinates are matched."""

    if node_count < 1:
        raise ValueError("node_count must be positive")
    return node_count - 1


def linear_matching_parameter_lower_bound_for_post_phase_center(
    node_count: int,
) -> int:
    """Rank lower bound if all post-phase center coordinates are matched."""

    if node_count < 1:
        raise ValueError("node_count must be positive")
    return node_count
