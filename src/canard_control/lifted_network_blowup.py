"""Exact fold blow-up for the arbitrary-size lifted node network.

This module fits the nodewise-cubic class in
``lifted_two_module_network.py`` to the singular special-flow coordinates.
The calculation is performed in the full stable space
``range(I-P_c)``, not only on the block-constant two-module subspace.

All returned residuals are exact SymPy identities.  They certify the affine
blow-up, the stable-variable shift, divisibility by the blow-up amplitude,
and the resulting transverse generator.  They do not construct a Lin gap,
a canard root, an outer slow selection, or a pulse threshold.
"""

from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

from canard_control.lifted_two_module_network import (
    LiftedTwoModuleNetwork,
    lifted_fast_field,
    lifted_final_two_module_network,
    lifted_recovery_slow_field,
)


Matrix = sp.ImmutableMatrix


def _immutable(matrix: sp.MatrixBase) -> Matrix:
    return sp.ImmutableMatrix(matrix)


def _divide_by_delta(
    expression: sp.Expr,
    delta: sp.Symbol,
    power: int,
) -> tuple[sp.Expr, sp.Expr]:
    """Polynomial-divide ``expression`` by ``delta**power`` exactly."""

    numerator = sp.Poly(sp.expand(expression), delta, domain="EX")
    denominator = sp.Poly(delta**power, delta, domain="EX")
    quotient, remainder = sp.div(numerator, denominator)
    return sp.expand(quotient.as_expr()), sp.expand(remainder.as_expr())


def _divide_matrix_by_delta(
    matrix: sp.MatrixBase,
    delta: sp.Symbol,
    power: int,
) -> tuple[sp.Matrix, sp.Matrix]:
    quotients: list[sp.Expr] = []
    remainders: list[sp.Expr] = []
    for entry in matrix:
        quotient, remainder = _divide_by_delta(entry, delta, power)
        quotients.append(quotient)
        remainders.append(remainder)
    return (
        sp.Matrix(matrix.rows, matrix.cols, quotients),
        sp.Matrix(matrix.rows, matrix.cols, remainders),
    )


@dataclass(frozen=True)
class LiftedNetworkBlowupAudit:
    """Exact full-stable-fiber blow-up and special-flow data."""

    network: LiftedTwoModuleNetwork
    delta: sp.Symbol
    unfolding: sp.Symbol
    weak_gain: sp.Symbol
    module_redistribution: sp.Symbol
    critical_x: sp.Symbol
    critical_y: sp.Symbol
    delayed_x_0: sp.Symbol
    delayed_x_1: sp.Symbol
    alpha: sp.Expr
    shifted_voltage: Matrix
    shifted_recovery: Matrix
    delayed_shifted_voltage_0: Matrix
    delayed_shifted_voltage_1: Matrix
    raw_voltage: Matrix
    raw_recovery: Matrix
    delayed_raw_voltage_0: Matrix
    delayed_raw_voltage_1: Matrix
    scaled_voltage: Matrix
    scaled_recovery: Matrix
    delayed_scaled_voltage_0: Matrix
    delayed_scaled_voltage_1: Matrix
    center_rhs: Matrix
    raw_stable_rhs: Matrix
    shifted_stable_rhs: Matrix
    singular_center_rhs: Matrix
    stable_generator: Matrix
    stable_state_projector: Matrix
    center_remainder: Matrix
    stable_remainder: Matrix
    physical_fast_scaling_remainder: Matrix
    physical_slow_scaling_remainder: Matrix
    center_divisibility_remainder: Matrix
    stable_divisibility_remainder: Matrix
    fast_reconstruction_residual: Matrix
    slow_reconstruction_residual: Matrix


@dataclass(frozen=True)
class FixedTwoAtomEvaluationAudit:
    """Matrix realization of the fixed-support history evaluation map."""

    state_dimension: int
    output_dimension: int
    atom_0_injection: Matrix
    atom_1_injection: Matrix
    atom_norms: tuple[sp.Expr, sp.Expr]
    operator_total_variation: sp.Expr
    parameter_derivative_total_variation: sp.Expr


def fixed_two_atom_evaluation_audit(
    network: LiftedTwoModuleNetwork,
) -> FixedTwoAtomEvaluationAudit:
    r"""Audit ``phi -> (phi(-theta_0),phi(-theta_1))`` in max norm.

    The chart state has two critical coordinates and two ambient stable node
    vectors, hence dimension ``2+2N``.  Each atom is a coordinate injection
    into a two-copy maximum-product output.  Both atom norms are one, so the
    operator-valued measure has total variation two, independently of ``N``.
    Its supports and weights are parameter independent, and all parameter
    derivatives of the measure vanish.
    """

    state_dimension = 2 + 2 * network.node_count
    identity = sp.eye(state_dimension)
    zero = sp.zeros(state_dimension)
    atom_0 = sp.Matrix.vstack(identity, zero)
    atom_1 = sp.Matrix.vstack(zero, identity)
    return FixedTwoAtomEvaluationAudit(
        state_dimension=state_dimension,
        output_dimension=2 * state_dimension,
        atom_0_injection=_immutable(atom_0),
        atom_1_injection=_immutable(atom_1),
        atom_norms=(sp.Integer(1), sp.Integer(1)),
        operator_total_variation=sp.Integer(2),
        parameter_derivative_total_variation=sp.Integer(0),
    )


def lifted_network_blowup_audit(
    n1: int,
    n2: int,
    *,
    within_voltage_rate: sp.Expr = sp.Rational(3, 2),
    recovery_rate: sp.Expr = sp.Rational(5, 2),
) -> LiftedNetworkBlowupAudit:
    r"""Return the exact arbitrary-``N`` fold blow-up audit.

    Write ``P_perp=I-P_c`` and let ``q_N`` be the lifted module-difference
    vector.  The raw chart is

    .. math::
       v=v_*+\delta r_NX+\delta^2z,\qquad
       w=w_*-\delta^2r_NY+\delta^4W,\qquad
       \mu=\delta^2\nu,\quad s=\delta t,

    with ``z,W`` in ``range(P_perp)``.  The shifted stable variables are

    .. math::
       U=z+\frac\alpha2q_NX^2,\qquad
       V=W+\frac\alpha{2D_w}q_NX^2.

    Ambient symbols are projected with ``P_perp`` before they are used, so
    every returned stable vector lies in the declared stable fiber.  Delayed
    values at the two fixed inner-time atoms are independent symbols.
    """

    delta = sp.Symbol("delta", positive=True)
    unfolding = sp.Symbol("nu", real=True)
    weak_gain = sp.Symbol("K", real=True)
    redistribution = sp.Symbol("eta", real=True)
    X, Y = sp.symbols("X Y", real=True)
    X_0, X_1 = sp.symbols("X_theta_0 X_theta_1", real=True)

    network = lifted_final_two_module_network(
        n1,
        n2,
        within_voltage_rate=within_voltage_rate,
        recovery_rate=recovery_rate,
        module_redistribution=redistribution,
    )
    node_count = network.node_count
    transverse = sp.Matrix(network.transverse_projector)
    r = sp.Matrix(network.critical_right)
    ell = sp.Matrix(network.critical_left)
    q = sp.Matrix(network.module_transverse_right_lift)
    alpha = sp.sqrt(sp.Rational(3, 2)) / 2
    recovery = network.recovery_rate

    def projected_symbols(prefix: str) -> sp.Matrix:
        ambient = sp.Matrix(sp.symbols(f"{prefix}0:{node_count}", real=True))
        return sp.expand(transverse * ambient)

    shifted_voltage = projected_symbols("U")
    shifted_recovery = projected_symbols("V")
    shifted_voltage_0 = projected_symbols("Utheta0_")
    shifted_voltage_1 = projected_symbols("Utheta1_")

    voltage_shift = alpha * q * X**2 / 2
    recovery_shift = alpha * q * X**2 / (2 * recovery)
    delayed_voltage_shift_0 = alpha * q * X_0**2 / 2
    delayed_voltage_shift_1 = alpha * q * X_1**2 / 2
    raw_voltage = sp.expand(shifted_voltage - voltage_shift)
    raw_recovery = sp.expand(shifted_recovery - recovery_shift)
    raw_voltage_0 = sp.expand(shifted_voltage_0 - delayed_voltage_shift_0)
    raw_voltage_1 = sp.expand(shifted_voltage_1 - delayed_voltage_shift_1)

    scaled_voltage = sp.expand(
        sp.Matrix(network.equilibrium_voltage)
        + delta * r * X
        + delta**2 * raw_voltage
    )
    scaled_recovery = sp.expand(
        sp.Matrix(network.equilibrium_recovery)
        - delta**2 * r * Y
        + delta**4 * raw_recovery
    )
    delayed_scaled_voltage_0 = sp.expand(
        sp.Matrix(network.equilibrium_voltage)
        + delta * r * X_0
        + delta**2 * raw_voltage_0
    )
    delayed_scaled_voltage_1 = sp.expand(
        sp.Matrix(network.equilibrium_voltage)
        + delta * r * X_1
        + delta**2 * raw_voltage_1
    )

    local_fast = sp.Matrix(
        lifted_fast_field(network, scaled_voltage, scaled_recovery)
    )
    delayed_feedback = sp.expand(
        sp.Matrix(network.total_layer) * scaled_voltage
        - sp.Matrix(network.layer_0) * delayed_scaled_voltage_0
        - sp.Matrix(network.layer_1) * delayed_scaled_voltage_1
    )
    physical_fast = sp.expand(
        local_fast + delta**2 * weak_gain * delayed_feedback
    )
    physical_slow = sp.expand(
        delta**2
        * sp.Matrix(
            lifted_recovery_slow_field(
                network, scaled_voltage, delta**2 * unfolding
            )
        )
        - recovery
        * transverse
        * (
            scaled_recovery
            - sp.Matrix(network.equilibrium_recovery)
        )
    )

    critical_fast_numerator = (ell.T * physical_fast)[0]
    stable_fast_numerator = transverse * physical_fast
    critical_slow_numerator = -(ell.T * physical_slow)[0]
    stable_slow_numerator = transverse * physical_slow

    X_rhs, X_scaling_remainder = _divide_by_delta(
        critical_fast_numerator, delta, 2
    )
    raw_voltage_rhs, z_scaling_remainder = _divide_matrix_by_delta(
        stable_fast_numerator, delta, 2
    )
    Y_rhs, Y_scaling_remainder = _divide_by_delta(
        critical_slow_numerator, delta, 3
    )
    raw_recovery_rhs, W_scaling_remainder = _divide_matrix_by_delta(
        stable_slow_numerator, delta, 4
    )

    center_rhs = sp.Matrix([X_rhs, Y_rhs])
    raw_stable_rhs = sp.Matrix.vstack(
        raw_voltage_rhs, raw_recovery_rhs
    )
    shifted_voltage_rhs = sp.expand(
        raw_voltage_rhs + delta * alpha * q * X * X_rhs
    )
    shifted_recovery_rhs = sp.expand(
        raw_recovery_rhs
        + delta * alpha * q * X * X_rhs / recovery
    )
    shifted_stable_rhs = sp.Matrix.vstack(
        shifted_voltage_rhs, shifted_recovery_rhs
    )

    singular_center_rhs = sp.Matrix([Y - alpha * X**2, -X])
    stable_generator = sp.Matrix.vstack(
        sp.Matrix.hstack(
            sp.Matrix(network.fast_voltage_jacobian),
            sp.zeros(node_count),
        ),
        sp.Matrix.hstack(sp.eye(node_count), -recovery * sp.eye(node_count)),
    )
    stable_state = sp.Matrix.vstack(shifted_voltage, shifted_recovery)
    stable_state_projector = sp.diag(transverse, transverse)

    center_remainder, center_divisibility_remainder = (
        _divide_matrix_by_delta(
            sp.expand(center_rhs - singular_center_rhs), delta, 1
        )
    )
    stable_remainder, stable_divisibility_remainder = (
        _divide_matrix_by_delta(
            sp.expand(
                shifted_stable_rhs - stable_generator * stable_state
            ),
            delta,
            1,
        )
    )

    fast_reconstruction_residual = sp.simplify(
        physical_fast
        - delta**2 * (r * X_rhs + raw_voltage_rhs)
    )
    slow_reconstruction_residual = sp.simplify(
        physical_slow
        - (-delta**3 * r * Y_rhs + delta**4 * raw_recovery_rhs)
    )

    return LiftedNetworkBlowupAudit(
        network=network,
        delta=delta,
        unfolding=unfolding,
        weak_gain=weak_gain,
        module_redistribution=redistribution,
        critical_x=X,
        critical_y=Y,
        delayed_x_0=X_0,
        delayed_x_1=X_1,
        alpha=alpha,
        shifted_voltage=_immutable(shifted_voltage),
        shifted_recovery=_immutable(shifted_recovery),
        delayed_shifted_voltage_0=_immutable(shifted_voltage_0),
        delayed_shifted_voltage_1=_immutable(shifted_voltage_1),
        raw_voltage=_immutable(raw_voltage),
        raw_recovery=_immutable(raw_recovery),
        delayed_raw_voltage_0=_immutable(raw_voltage_0),
        delayed_raw_voltage_1=_immutable(raw_voltage_1),
        scaled_voltage=_immutable(scaled_voltage),
        scaled_recovery=_immutable(scaled_recovery),
        delayed_scaled_voltage_0=_immutable(delayed_scaled_voltage_0),
        delayed_scaled_voltage_1=_immutable(delayed_scaled_voltage_1),
        center_rhs=_immutable(center_rhs),
        raw_stable_rhs=_immutable(raw_stable_rhs),
        shifted_stable_rhs=_immutable(shifted_stable_rhs),
        singular_center_rhs=_immutable(singular_center_rhs),
        stable_generator=_immutable(stable_generator),
        stable_state_projector=_immutable(stable_state_projector),
        center_remainder=_immutable(center_remainder),
        stable_remainder=_immutable(stable_remainder),
        physical_fast_scaling_remainder=_immutable(
            sp.Matrix([X_scaling_remainder]).col_join(z_scaling_remainder)
        ),
        physical_slow_scaling_remainder=_immutable(
            sp.Matrix([Y_scaling_remainder]).col_join(W_scaling_remainder)
        ),
        center_divisibility_remainder=_immutable(
            center_divisibility_remainder
        ),
        stable_divisibility_remainder=_immutable(
            stable_divisibility_remainder
        ),
        fast_reconstruction_residual=_immutable(
            fast_reconstruction_residual
        ),
        slow_reconstruction_residual=_immutable(
            slow_reconstruction_residual
        ),
    )


if __name__ == "__main__":
    audit = lifted_network_blowup_audit(1, 1)
    print("center divisibility remainder =", audit.center_divisibility_remainder)
    print("stable divisibility remainder =", audit.stable_divisibility_remainder)
    print("stable generator =", audit.stable_generator)
