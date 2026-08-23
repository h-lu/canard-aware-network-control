"""Exact audits for the arbitrary-N shared-resource Markov network.

The module verifies finite-dimensional graph identities and the exact
fold-chart scaling.  It does not construct selected slow histories, a
complete-history gap, a canard root, or a pulse event.
"""

from __future__ import annotations

from dataclasses import dataclass

import sympy as sp


Matrix = sp.ImmutableMatrix


def _matrix(value: sp.MatrixBase) -> sp.Matrix:
    return sp.Matrix(value)


def _divide_matrix(
    value: sp.MatrixBase,
    delta: sp.Symbol,
    power: int,
) -> tuple[sp.Matrix, sp.Matrix]:
    quotients: list[sp.Expr] = []
    remainders: list[sp.Expr] = []
    divisor = sp.Poly(delta**power, delta, domain="EX")
    for entry in value:
        quotient, remainder = sp.div(
            sp.Poly(sp.expand(entry), delta, domain="EX"),
            divisor,
        )
        quotients.append(sp.expand(quotient.as_expr()))
        remainders.append(sp.expand(remainder.as_expr()))
    return (
        sp.Matrix(value.rows, value.cols, quotients),
        sp.Matrix(value.rows, value.cols, remainders),
    )


def dobrushin_coefficient(matrix: sp.MatrixBase) -> sp.Expr:
    """Return the exact Dobrushin row-contraction coefficient."""

    matrix = _matrix(matrix)
    if matrix.rows < 1 or matrix.rows != matrix.cols:
        raise ValueError("matrix must be nonempty and square")
    row_distances = []
    for row_i in range(matrix.rows):
        for row_k in range(matrix.rows):
            row_distances.append(
                sp.simplify(
                    sp.Rational(1, 2)
                    * sum(
                        (
                            sp.Abs(matrix[row_i, column] - matrix[row_k, column])
                            for column in range(matrix.cols)
                        ),
                        sp.Integer(0),
                    )
                )
            )
    return sp.simplify(sp.Max(*row_distances))


@dataclass(frozen=True)
class MarkovGraphAudit:
    """Exact algebra and norm certificates for one Markov graph."""

    transition: Matrix
    stationary: Matrix
    critical_projector: Matrix
    transverse_projector: Matrix
    dobrushin: sp.Expr
    mixing_gap: sp.Expr
    fast_jacobian: Matrix
    fold_curvature: sp.Expr
    critical_projector_bound: sp.Expr
    transverse_projector_bound: sp.Expr


def markov_graph_audit(
    transition: sp.MatrixBase,
    stationary: sp.MatrixBase,
    *,
    coupling_rate: sp.Expr = sp.Integer(1),
) -> MarkovGraphAudit:
    """Validate a row-stochastic graph with a positive stationary column.

    The transpose of the supplied column is the invariant row covector.
    """

    transition = _matrix(transition)
    stationary = _matrix(stationary)
    if transition.rows < 1 or transition.rows != transition.cols:
        raise ValueError("transition must be nonempty and square")
    node_count = transition.rows
    if stationary.shape == (node_count,):
        stationary = stationary.reshape(node_count, 1)
    if stationary.shape != (node_count, 1):
        raise ValueError("stationary must be a compatible column")
    if any(entry.is_nonnegative is not True for entry in transition):
        raise ValueError("transition entries must be known nonnegative")
    if any(entry.is_positive is not True for entry in stationary):
        raise ValueError("stationary entries must be known positive")

    ones = sp.ones(node_count, 1)
    if sp.simplify(transition * ones - ones) != sp.zeros(node_count, 1):
        raise ValueError("transition must be row stochastic")
    if sp.simplify((stationary.T * ones)[0] - 1) != 0:
        raise ValueError("stationary weights must sum to one")
    if sp.simplify(stationary.T * transition - stationary.T) != sp.zeros(
        1, node_count
    ):
        raise ValueError("stationary weights must be invariant")

    rate = sp.sympify(coupling_rate)
    if rate.is_positive is not True:
        raise ValueError("coupling_rate must be known positive")
    critical = ones * stationary.T
    transverse = sp.eye(node_count) - critical
    tau = dobrushin_coefficient(transition)
    return MarkovGraphAudit(
        transition=sp.ImmutableMatrix(transition),
        stationary=sp.ImmutableMatrix(stationary),
        critical_projector=sp.ImmutableMatrix(critical),
        transverse_projector=sp.ImmutableMatrix(transverse),
        dobrushin=tau,
        mixing_gap=sp.simplify(1 - tau),
        fast_jacobian=sp.ImmutableMatrix(rate * (transition - sp.eye(node_count))),
        fold_curvature=sp.Integer(-2),
        critical_projector_bound=sp.Integer(1),
        transverse_projector_bound=sp.Integer(1),
    )


@dataclass(frozen=True)
class SharedResourceBlowupAudit:
    """Exact scaled RFDE residuals for the shared-resource network."""

    graph: MarkovGraphAudit
    delta: sp.Symbol
    critical_x: sp.Symbol
    critical_y: sp.Symbol
    unfolding: sp.Symbol
    weak_gain: sp.Symbol
    delayed_x_0: sp.Symbol
    delayed_x_1: sp.Symbol
    stable_voltage: Matrix
    delayed_stable_voltage_0: Matrix
    delayed_stable_voltage_1: Matrix
    scaled_voltage: Matrix
    scaled_resource: sp.Expr
    displayed_critical_rhs: sp.Expr
    displayed_resource_rhs: sp.Expr
    displayed_stable_rhs: Matrix
    critical_rhs_from_physical_model: sp.Expr
    resource_rhs_from_physical_model: sp.Expr
    stable_rhs_from_physical_model: Matrix
    critical_division_remainder: sp.Expr
    resource_division_remainder: sp.Expr
    stable_division_remainder: Matrix
    critical_residual: sp.Expr
    resource_residual: sp.Expr
    stable_residual: Matrix
    critical_projected_layer_0: Matrix
    critical_projected_layer_1: Matrix


def shared_resource_blowup_audit(
    transition: sp.MatrixBase,
    stationary: sp.MatrixBase,
    layer_0: sp.MatrixBase,
    layer_1: sp.MatrixBase,
    *,
    coupling_rate: sp.Expr = sp.Integer(1),
) -> SharedResourceBlowupAudit:
    """Build the physical RFDE first and verify the exact fold chart."""

    graph = markov_graph_audit(
        transition,
        stationary,
        coupling_rate=coupling_rate,
    )
    node_count = graph.transition.rows
    layer_0 = _matrix(layer_0)
    layer_1 = _matrix(layer_1)
    if layer_0.shape != (node_count, node_count):
        raise ValueError("layer_0 has incompatible shape")
    if layer_1.shape != (node_count, node_count):
        raise ValueError("layer_1 has incompatible shape")

    delta = sp.Symbol("delta", positive=True)
    X, Y, nu, weak_gain = sp.symbols("X Y nu K", real=True)
    X_0, X_1 = sp.symbols("X_theta_0 X_theta_1", real=True)
    ones = sp.ones(node_count, 1)
    pi = sp.Matrix(graph.stationary)
    transverse = sp.Matrix(graph.transverse_projector)
    transition_m = sp.Matrix(graph.transition)
    total_layer = layer_0 + layer_1

    def projected_symbols(prefix: str) -> sp.Matrix:
        ambient = sp.Matrix(sp.symbols(f"{prefix}0:{node_count}", real=True))
        return sp.expand(transverse * ambient)

    z = projected_symbols("z")
    z_0 = projected_symbols("ztheta0_")
    z_1 = projected_symbols("ztheta1_")
    v = sp.expand(ones + delta * ones * X + delta**2 * z)
    v_0 = sp.expand(ones + delta * ones * X_0 + delta**2 * z_0)
    v_1 = sp.expand(ones + delta * ones * X_1 + delta**2 * z_1)
    w = sp.Rational(2, 3) - delta**2 * Y
    a = 1 + delta**2 * nu

    local = sp.expand(
        v - v.applyfunc(lambda entry: entry**3) / 3 - w * ones
    )
    coupling = sp.sympify(coupling_rate) * (
        transition_m - sp.eye(node_count)
    ) * v
    delay = sp.expand(
        total_layer * v - layer_0 * v_0 - layer_1 * v_1
    )
    physical_fast = sp.expand(local + coupling + delta**2 * weak_gain * delay)
    physical_resource = sp.expand(delta**2 * ((pi.T * v)[0] - a))

    critical_matrix, critical_remainder_matrix = _divide_matrix(
        pi.T * physical_fast,
        delta,
        2,
    )
    stable_matrix, stable_remainder = _divide_matrix(
        transverse * physical_fast,
        delta,
        2,
    )
    resource_matrix, resource_remainder_matrix = _divide_matrix(
        sp.Matrix([-physical_resource]),
        delta,
        3,
    )
    critical_rhs = sp.expand(critical_matrix[0])
    stable_rhs = sp.expand(stable_matrix)
    resource_rhs = sp.expand(resource_matrix[0])

    chart_delay = sp.expand(
        total_layer * (ones * X + delta * z)
        - layer_0 * (ones * X_0 + delta * z_0)
        - layer_1 * (ones * X_1 + delta * z_1)
    )
    displayed_critical = sp.expand(
        Y
        - X**2
        + delta
        * (-X**3 / 3 + weak_gain * (pi.T * chart_delay)[0])
        - delta**2 * (pi.T * z.applyfunc(lambda entry: entry**2))[0]
        - delta**3
        * X
        * (pi.T * z.applyfunc(lambda entry: entry**2))[0]
        - delta**4
        * (pi.T * z.applyfunc(lambda entry: entry**3))[0]
        / 3
    )
    displayed_resource = -X + delta * nu
    displayed_stable = sp.expand(
        sp.sympify(coupling_rate) * (transition_m - sp.eye(node_count)) * z
        + delta
        * transverse
        * (-2 * X * z + weak_gain * chart_delay)
        - delta**2
        * transverse
        * (
            z.applyfunc(lambda entry: entry**2)
            + X**2 * z
        )
        - delta**3
        * transverse
        * (X * z.applyfunc(lambda entry: entry**2))
        - delta**4
        * transverse
        * z.applyfunc(lambda entry: entry**3)
        / 3
    )

    return SharedResourceBlowupAudit(
        graph=graph,
        delta=delta,
        critical_x=X,
        critical_y=Y,
        unfolding=nu,
        weak_gain=weak_gain,
        delayed_x_0=X_0,
        delayed_x_1=X_1,
        stable_voltage=sp.ImmutableMatrix(z),
        delayed_stable_voltage_0=sp.ImmutableMatrix(z_0),
        delayed_stable_voltage_1=sp.ImmutableMatrix(z_1),
        scaled_voltage=sp.ImmutableMatrix(v),
        scaled_resource=w,
        displayed_critical_rhs=displayed_critical,
        displayed_resource_rhs=displayed_resource,
        displayed_stable_rhs=sp.ImmutableMatrix(displayed_stable),
        critical_rhs_from_physical_model=critical_rhs,
        resource_rhs_from_physical_model=resource_rhs,
        stable_rhs_from_physical_model=sp.ImmutableMatrix(stable_rhs),
        critical_division_remainder=sp.expand(critical_remainder_matrix[0]),
        resource_division_remainder=sp.expand(resource_remainder_matrix[0]),
        stable_division_remainder=sp.ImmutableMatrix(stable_remainder),
        critical_residual=sp.simplify(critical_rhs - displayed_critical),
        resource_residual=sp.simplify(resource_rhs - displayed_resource),
        stable_residual=sp.ImmutableMatrix(
            sp.simplify(stable_rhs - displayed_stable)
        ),
        critical_projected_layer_0=sp.ImmutableMatrix(pi.T * layer_0),
        critical_projected_layer_1=sp.ImmutableMatrix(pi.T * layer_1),
    )
