"""Exact shifted form and the first transverse jet of the special-flow graph.

This module performs algebra needed by the constructive Gate-B proof.  It
shifts the singular transverse graph to the origin, verifies that the two
remaining transverse variables form a uniformly Hurwitz block after the
factor ``delta`` is restored, and derives the eta-dependent first graph jet
from that block.

The identities are exact.  They do not, on their own, prove existence or
regularity of the nonlocal invariant graph.  Separate analytic arguments in
``docs/special-flow-graph-theorem.md`` and
``docs/mixed-jet-graph-proof.md`` prove the bounded graph and the finite mixed
regularity needed to identify these expressions with fixed-tube Taylor
coefficients.  Neither the code nor those fixed-tube results prove the
selected physical long-delay canard root.
"""

from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

from canard_control.final_model_blowup import final_model_blowup


@dataclass(frozen=True)
class NonlocalGraphJetAudit:
    """Shifted singular system and its exact eta-dependent graph jet."""

    delta: sp.Symbol
    eta: sp.Symbol
    weak_gain: sp.Symbol
    recovery_gap: sp.Symbol
    alpha: sp.Expr
    chart_x: sp.Symbol
    chart_y: sp.Symbol
    shifted_voltage: sp.Symbol
    shifted_recovery: sp.Symbol
    stable_matrix: sp.Matrix
    stable_characteristic: sp.Expr
    shifted_critical_rhs: sp.Expr
    shifted_delta_voltage_rhs: sp.Expr
    shifted_delta_recovery_rhs: sp.Expr
    center_remainder: sp.Expr
    stable_remainder: sp.Matrix
    center_divisibility_residual: sp.Expr
    stable_divisibility_residual: sp.Matrix
    eta_stable_forcing: sp.Matrix
    eta_first_graph_jet: sp.Matrix
    eta_first_graph_residual: sp.Matrix
    eta_first_graph_on_canard: sp.Matrix
    eta_second_center_jet_on_canard: sp.Expr
    formal_nu_derivative: sp.Expr
    formal_mu_derivative: sp.Expr


def nonlocal_graph_jet_audit() -> NonlocalGraphJetAudit:
    """Shift the exact chart and derive the first eta-dependent graph jet."""

    base = final_model_blowup()
    delta = base.delta
    eta = base.eta
    weak_gain = base.weak_gain
    recovery_gap = base.recovery_gap
    alpha = base.alpha
    X = base.chart_x
    Y = base.chart_y
    Z = base.chart_z
    W = base.chart_w
    X_0 = base.delayed_x_0
    X_1 = base.delayed_x_1
    Z_0 = base.delayed_z_0
    Z_1 = base.delayed_z_1

    U, V = sp.symbols("U V", real=True)
    U_0, U_1 = sp.symbols("U_theta_0 U_theta_1", real=True)

    # Both shifts subtract the exact delta=0 algebraic graph.  The second
    # choice depends only on X; this produces the triangular stable matrix
    # [[-2, 0], [1, -D_w]].
    z_from_shift = U - alpha * X**2 / 2
    w_from_shift = V - alpha * X**2 / (2 * recovery_gap)
    z_0_from_shift = U_0 - alpha * X_0**2 / 2
    z_1_from_shift = U_1 - alpha * X_1**2 / 2
    shift_substitution = {
        Z: z_from_shift,
        W: w_from_shift,
        Z_0: z_0_from_shift,
        Z_1: z_1_from_shift,
    }

    shifted_critical_rhs = sp.expand(
        base.displayed_critical_rhs.subs(shift_substitution)
    )
    shifted_transverse_rhs = sp.expand(
        base.displayed_transverse_rhs.subs(shift_substitution)
    )
    shifted_recovery_rhs = sp.expand(
        base.displayed_transverse_recovery_rhs.subs(
            shift_substitution
        )
    )

    # U=Z+alpha*X**2/2 and
    # V=W+alpha*X**2/(2*D_w).
    shifted_delta_voltage_rhs = sp.expand(
        shifted_transverse_rhs
        + delta * alpha * X * shifted_critical_rhs
    )
    shifted_delta_recovery_rhs = sp.expand(
        shifted_recovery_rhs
        + delta
        * alpha
        * X
        * shifted_critical_rhs
        / recovery_gap
    )

    unperturbed_center_rhs = Y - alpha * X**2
    stable_matrix = sp.Matrix(
        [[-2, 0], [1, -recovery_gap]]
    )
    stable_state = sp.Matrix([U, V])
    stable_linear_rhs = stable_matrix * stable_state

    center_numerator = sp.expand(
        shifted_critical_rhs - unperturbed_center_rhs
    )
    stable_numerator = sp.expand(
        sp.Matrix(
            [
                shifted_delta_voltage_rhs,
                shifted_delta_recovery_rhs,
            ]
        )
        - stable_linear_rhs
    )
    # Certify divisibility by polynomial division.  Defining the quotient as
    # ``numerator / delta`` and then multiplying back would make a zero
    # residual tautological even when the quotient contained ``delta**-1``.
    # ``EX`` treats the other symbols (including 1 / D_w) as coefficients.
    delta_polynomial = sp.Poly(delta, delta, domain="EX")
    center_quotient, center_division_remainder = sp.div(
        sp.Poly(center_numerator, delta, domain="EX"),
        delta_polynomial,
    )
    stable_divisions = [
        sp.div(
            sp.Poly(component, delta, domain="EX"),
            delta_polynomial,
        )
        for component in stable_numerator
    ]
    center_remainder = sp.simplify(center_quotient.as_expr())
    stable_remainder = sp.Matrix(
        [sp.simplify(quotient.as_expr()) for quotient, _ in stable_divisions]
    )
    center_divisibility_residual = sp.simplify(
        center_division_remainder.as_expr()
    )
    stable_divisibility_residual = sp.Matrix(
        [
            sp.simplify(remainder.as_expr())
            for _, remainder in stable_divisions
        ]
    )

    # In delta*h'=A*h+delta*g, the first graph coefficient satisfies
    # A*(partial_eta h_1)+partial_eta g_0=0.
    eta_stable_forcing = sp.simplify(
        sp.diff(stable_remainder, eta).subs(
            {delta: 0, eta: 0, U: 0, V: 0, U_0: 0, U_1: 0}
        )
    )
    eta_first_graph_jet = sp.simplify(
        -stable_matrix.inv() * eta_stable_forcing
    )
    eta_first_graph_residual = sp.simplify(
        stable_matrix * eta_first_graph_jet
        + eta_stable_forcing
    )

    canard_substitution = {
        X: base.leading_canard_x,
        X_0: base.leading_canard_x.subs(
            base.inner_time, base.inner_time - base.theta_0
        ),
        X_1: base.leading_canard_x.subs(
            base.inner_time, base.inner_time - base.theta_1
        ),
    }
    eta_first_graph_on_canard = sp.simplify(
        eta_first_graph_jet.subs(canard_substitution)
    )

    # Only the U component returns to the critical equation at order
    # delta**2 through -2*alpha*X*U.
    eta_second_center_jet_on_canard = sp.simplify(
        -2
        * alpha
        * base.leading_canard_x
        * eta_first_graph_on_canard[0]
    )
    gaussian = sp.exp(-base.inner_time**2 / 2)
    numerator = sp.integrate(
        gaussian
        * base.inner_time
        * eta_second_center_jet_on_canard,
        (base.inner_time, -sp.oo, sp.oo),
    )
    denominator = sp.integrate(
        gaussian, (base.inner_time, -sp.oo, sp.oo)
    )
    formal_nu_derivative = sp.simplify(-numerator / denominator)
    formal_mu_derivative = sp.simplify(
        delta**3 * formal_nu_derivative
    )

    stable_parameter = sp.Symbol("lambda")
    stable_characteristic = sp.factor(
        stable_matrix.charpoly(stable_parameter).as_expr()
    )

    return NonlocalGraphJetAudit(
        delta=delta,
        eta=eta,
        weak_gain=weak_gain,
        recovery_gap=recovery_gap,
        alpha=alpha,
        chart_x=X,
        chart_y=Y,
        shifted_voltage=U,
        shifted_recovery=V,
        stable_matrix=stable_matrix,
        stable_characteristic=stable_characteristic,
        shifted_critical_rhs=shifted_critical_rhs,
        shifted_delta_voltage_rhs=shifted_delta_voltage_rhs,
        shifted_delta_recovery_rhs=shifted_delta_recovery_rhs,
        center_remainder=center_remainder,
        stable_remainder=stable_remainder,
        center_divisibility_residual=center_divisibility_residual,
        stable_divisibility_residual=stable_divisibility_residual,
        eta_stable_forcing=eta_stable_forcing,
        eta_first_graph_jet=eta_first_graph_jet,
        eta_first_graph_residual=eta_first_graph_residual,
        eta_first_graph_on_canard=eta_first_graph_on_canard,
        eta_second_center_jet_on_canard=(
            eta_second_center_jet_on_canard
        ),
        formal_nu_derivative=formal_nu_derivative,
        formal_mu_derivative=formal_mu_derivative,
    )


if __name__ == "__main__":
    audit = nonlocal_graph_jet_audit()
    print("stable matrix =", audit.stable_matrix)
    print("eta forcing =", audit.eta_stable_forcing)
    print("eta h_1 =", audit.eta_first_graph_jet)
    print("formal d_mu/d_eta =", audit.formal_mu_derivative)
