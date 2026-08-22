"""Exact raw-coordinate blow-up audit for the final two-module model.

The function in this module starts from the physical RFDE ``(M)``: it builds
the FitzHugh--Nagumo vector field, the two delayed layers, and the fixed
transverse recovery coupling before making any modal or scaling
substitution.  The displayed blown-up equations are then checked against
the transformed physical equations by exact SymPy residuals.

The algebraic identities returned here are exact.  The final Gaussian
pairing is only the formal whole-line coefficient of the leading inner
problem; this module does not prove a singular RFDE invariant-manifold or
maximal-canard theorem.
"""

from __future__ import annotations

from dataclasses import dataclass

import sympy as sp


@dataclass(frozen=True)
class FinalModelBlowup:
    """Exact transformed model and the isolated formal eta coefficient."""

    delta: sp.Symbol
    eta: sp.Symbol
    weak_gain: sp.Symbol
    recovery_gap: sp.Symbol
    theta_0: sp.Symbol
    theta_1: sp.Symbol
    inner_time: sp.Symbol
    chart_x: sp.Symbol
    chart_y: sp.Symbol
    chart_z: sp.Symbol
    chart_w: sp.Symbol
    chart_unfolding: sp.Symbol
    delayed_x_0: sp.Symbol
    delayed_x_1: sp.Symbol
    delayed_z_0: sp.Symbol
    delayed_z_1: sp.Symbol
    sigma: sp.Expr
    alpha: sp.Expr
    critical_right: sp.Matrix
    transverse_right: sp.Matrix
    critical_left: sp.Matrix
    transverse_left: sp.Matrix
    critical_projector: sp.Matrix
    transverse_projector: sp.Matrix
    equilibrium_v: sp.Matrix
    equilibrium_w: sp.Matrix
    layer_0_modal: sp.Matrix
    layer_1_modal: sp.Matrix
    total_gain_modal: sp.Matrix
    redistribution_modal: sp.Matrix
    singular_jacobian: sp.Matrix
    singular_characteristic: sp.Expr
    scaled_voltage: sp.Matrix
    scaled_recovery: sp.Matrix
    scaled_parameter: sp.Expr
    critical_voltage_scale: sp.Expr
    transverse_voltage_scale: sp.Expr
    critical_recovery_scale: sp.Expr
    transverse_recovery_scale: sp.Expr
    critical_rhs_from_model: sp.Expr
    transverse_rhs_from_model: sp.Expr
    collective_recovery_rhs_from_model: sp.Expr
    transverse_recovery_rhs_from_model: sp.Expr
    displayed_critical_rhs: sp.Expr
    displayed_transverse_rhs: sp.Expr
    displayed_collective_recovery_rhs: sp.Expr
    displayed_transverse_recovery_rhs: sp.Expr
    critical_residual: sp.Expr
    transverse_residual: sp.Expr
    collective_recovery_residual: sp.Expr
    transverse_recovery_residual: sp.Expr
    fast_reconstruction_residual: sp.Matrix
    slow_reconstruction_residual: sp.Matrix
    leading_graph_z: sp.Expr
    leading_graph_w: sp.Expr
    leading_canard_x: sp.Expr
    leading_canard_y: sp.Expr
    delay_translation_difference: sp.Expr
    eta_order_transverse_forcing: sp.Expr
    leading_transverse_linearization: sp.Expr
    eta_transverse_coefficient: sp.Expr
    eta_critical_force: sp.Expr
    formal_numerator: sp.Expr
    formal_denominator: sp.Expr
    formal_nu_coefficient: sp.Expr
    formal_mu_derivative: sp.Expr


def final_model_blowup() -> FinalModelBlowup:
    r"""Transform the physical final model and verify the exact raw chart.

    The raw modal scaling is

    .. math::
       v=v_*+\delta rX+\delta^2qZ,\qquad
       w=w_*-\delta^2rY+\delta^4qW,\qquad
       \mu=\delta^2\nu,\qquad s=\delta t.

    With this convention ``X=delta**(-1)*ell.T*(v-v_*)``.  The function
    returns the right-hand side for ``X'``, ``delta*Z'``, ``Y'``, and
    ``delta*W'``.  Delayed values are represented by independent symbols;
    the change of time sends ``t-theta_k/delta`` exactly to ``s-theta_k``.
    """

    delta = sp.Symbol("delta", positive=True)
    eta, weak_gain = sp.symbols("eta K", real=True)
    recovery_gap = sp.Symbol("D_w", positive=True)
    theta_0, theta_1, inner_time = sp.symbols(
        "theta_0 theta_1 s", real=True
    )
    X, Y, Z, W, nu = sp.symbols("X Y Z W nu", real=True)
    X_theta_0, X_theta_1 = sp.symbols(
        "X_theta_0 X_theta_1", real=True
    )
    Z_theta_0, Z_theta_1 = sp.symbols(
        "Z_theta_0 Z_theta_1", real=True
    )

    sigma = sp.sqrt(sp.Rational(3, 2))
    alpha = sigma / 2
    critical_right = sp.Matrix([1, 2])
    transverse_right = sp.Matrix([1, -2])
    critical_left = sp.Matrix(
        [sp.Rational(1, 2), sp.Rational(1, 4)]
    )
    transverse_left = sp.Matrix(
        [sp.Rational(1, 2), -sp.Rational(1, 4)]
    )
    modal_rows = sp.Matrix.vstack(
        critical_left.T, transverse_left.T
    )
    modal_columns = sp.Matrix.hstack(
        critical_right, transverse_right
    )
    critical_projector = critical_right * critical_left.T
    transverse_projector = sp.eye(2) - critical_projector

    equilibrium_v = sp.Matrix([sigma, 0])
    equilibrium_w = sp.Matrix([0, 2 * sigma])
    layer_0 = sp.Matrix(
        [
            [sp.Rational(1, 6), sp.Rational(1, 12)],
            [sp.Rational(1, 6), sp.Rational(1, 4)],
        ]
    )
    layer_1 = sp.Matrix(
        [
            [sp.Rational(1, 3), sp.Rational(1, 6)],
            [sp.Rational(1, 2), sp.Rational(5, 12)],
        ]
    )
    redistribution = sp.Matrix([[1, 0], [-2, 0]])
    total_gain = layer_0 + layer_1
    perturbed_layer_0 = layer_0 + eta * redistribution
    perturbed_layer_1 = layer_1 - eta * redistribution
    layer_0_modal = sp.simplify(
        modal_rows * perturbed_layer_0 * modal_columns
    )
    layer_1_modal = sp.simplify(
        modal_rows * perturbed_layer_1 * modal_columns
    )
    total_gain_modal = sp.simplify(
        modal_rows * total_gain * modal_columns
    )
    redistribution_modal = sp.simplify(
        modal_rows * redistribution * modal_columns
    )

    # Build the physical current-state singular matrix directly from (M).
    v_1, v_2, w_1, w_2 = sp.symbols("v_1 v_2 w_1 w_2")
    physical_fast_local = sp.Matrix(
        [
            v_1 - v_1**3 / 3 - w_1 + (v_2 - v_1) / 2,
            v_2 - v_2**3 / 3 - w_2 + 2 * (v_1 - v_2),
        ]
    )
    fast_jacobian = sp.simplify(
        physical_fast_local.jacobian((v_1, v_2)).subs(
            {v_1: equilibrium_v[0], v_2: equilibrium_v[1]}
        )
    )
    singular_jacobian = sp.Matrix.vstack(
        sp.Matrix.hstack(fast_jacobian, -sp.eye(2)),
        sp.Matrix.hstack(
            sp.zeros(2), -recovery_gap * transverse_projector
        ),
    )
    spectral_parameter = sp.Symbol("lambda")
    singular_characteristic = sp.factor(
        singular_jacobian.charpoly(spectral_parameter).as_expr()
    )

    # Make the raw blow-up substitution in the physical RFDE itself.
    scaled_voltage = (
        equilibrium_v
        + delta * critical_right * X
        + delta**2 * transverse_right * Z
    )
    scaled_recovery = (
        equilibrium_w
        - delta**2 * critical_right * Y
        + delta**4 * transverse_right * W
    )
    scaled_parameter = delta**2 * nu
    delayed_voltage_0 = (
        equilibrium_v
        + delta * critical_right * X_theta_0
        + delta**2 * transverse_right * Z_theta_0
    )
    delayed_voltage_1 = (
        equilibrium_v
        + delta * critical_right * X_theta_1
        + delta**2 * transverse_right * Z_theta_1
    )

    local_substitution = {
        v_1: scaled_voltage[0],
        v_2: scaled_voltage[1],
        w_1: scaled_recovery[0],
        w_2: scaled_recovery[1],
    }
    local_fast_after_scaling = sp.expand(
        physical_fast_local.subs(local_substitution)
    )
    delay_feedback_after_scaling = sp.expand(
        total_gain * scaled_voltage
        - perturbed_layer_0 * delayed_voltage_0
        - perturbed_layer_1 * delayed_voltage_1
    )
    physical_fast_after_scaling = sp.expand(
        local_fast_after_scaling
        + delta**2 * weak_gain * delay_feedback_after_scaling
    )
    physical_slow_after_scaling = sp.expand(
        delta**2
        * (
            scaled_voltage
            - equilibrium_v
            - scaled_parameter * critical_right
        )
        - recovery_gap
        * transverse_projector
        * (scaled_recovery - equilibrium_w)
    )

    # Because ds/dt=delta, the projected fast left sides are delta**2*X'
    # and delta**2*(delta*Z').  The recovery left sides are
    # -delta**3*Y' and delta**4*(delta*W').
    critical_rhs_from_model = sp.expand(
        (critical_left.T * physical_fast_after_scaling)[0] / delta**2
    )
    transverse_rhs_from_model = sp.expand(
        (transverse_left.T * physical_fast_after_scaling)[0]
        / delta**2
    )
    collective_recovery_rhs_from_model = sp.expand(
        -(critical_left.T * physical_slow_after_scaling)[0]
        / delta**3
    )
    transverse_recovery_rhs_from_model = sp.expand(
        (transverse_left.T * physical_slow_after_scaling)[0]
        / delta**4
    )

    delay_critical = (
        X - sp.Rational(1, 3) * X_theta_0
        - sp.Rational(2, 3) * X_theta_1
    )
    delay_cross = (
        -sp.Rational(1, 6) * Z
        + sp.Rational(1, 12) * Z_theta_0
        + sp.Rational(1, 12) * Z_theta_1
    )
    delay_transverse = -delay_cross
    delay_gap_x = X_theta_0 - X_theta_1
    delay_gap_z = Z_theta_0 - Z_theta_1

    displayed_critical_rhs = sp.expand(
        Y
        - alpha * X**2
        + delta
        * (
            weak_gain * delay_critical
            - 2 * alpha * X * Z
            - sp.Rational(20, 9) * alpha**2 * X**3
        )
        + delta**2
        * (
            weak_gain * delay_cross
            - alpha * Z**2
            + 4 * alpha**2 * X**2 * Z
        )
        - delta**3 * sp.Rational(20, 3) * alpha**2 * X * Z**2
        + delta**4 * sp.Rational(4, 3) * alpha**2 * Z**3
    )
    displayed_transverse_rhs = sp.expand(
        -2 * Z
        - alpha * X**2
        + delta
        * (
            -2 * alpha * X * Z
            + sp.Rational(4, 3) * alpha**2 * X**3
            - weak_gain * eta * delay_gap_x
        )
        + delta**2
        * (
            -W
            - alpha * Z**2
            - sp.Rational(20, 3) * alpha**2 * X**2 * Z
            + weak_gain
            * (delay_transverse - eta * delay_gap_z)
        )
        + delta**3 * 4 * alpha**2 * X * Z**2
        - delta**4 * sp.Rational(20, 9) * alpha**2 * Z**3
    )
    displayed_collective_recovery_rhs = -X + delta * nu
    displayed_transverse_recovery_rhs = Z - recovery_gap * W

    critical_residual = sp.simplify(
        critical_rhs_from_model - displayed_critical_rhs
    )
    transverse_residual = sp.simplify(
        transverse_rhs_from_model - displayed_transverse_rhs
    )
    collective_recovery_residual = sp.simplify(
        collective_recovery_rhs_from_model
        - displayed_collective_recovery_rhs
    )
    transverse_recovery_residual = sp.simplify(
        transverse_recovery_rhs_from_model
        - displayed_transverse_recovery_rhs
    )
    fast_reconstruction_residual = sp.simplify(
        physical_fast_after_scaling
        - delta**2
        * (
            critical_right * displayed_critical_rhs
            + transverse_right * displayed_transverse_rhs
        )
    )
    slow_reconstruction_residual = sp.simplify(
        physical_slow_after_scaling
        - (
            -delta**3
            * critical_right
            * displayed_collective_recovery_rhs
            + delta**4
            * transverse_right
            * displayed_transverse_recovery_rhs
        )
    )

    critical_voltage_scale = sp.simplify(
        (critical_left.T * (scaled_voltage - equilibrium_v))[0] / X
    )
    transverse_voltage_scale = sp.simplify(
        (transverse_left.T * (scaled_voltage - equilibrium_v))[0] / Z
    )
    critical_recovery_scale = sp.simplify(
        (critical_left.T * (scaled_recovery - equilibrium_w))[0] / Y
    )
    transverse_recovery_scale = sp.simplify(
        (transverse_left.T * (scaled_recovery - equilibrium_w))[0] / W
    )

    # Derive, rather than prescribe, the delta=0 algebraic transverse graph.
    graph_solutions = sp.solve(
        (
            transverse_rhs_from_model.subs(delta, 0),
            transverse_recovery_rhs_from_model.subs(delta, 0),
        ),
        (Z, W),
        dict=True,
    )
    if len(graph_solutions) != 1:
        raise RuntimeError("the leading transverse algebraic graph is not unique")
    leading_graph_z = sp.simplify(graph_solutions[0][Z])
    leading_graph_w = sp.simplify(graph_solutions[0][W])

    # Formal whole-line calculation.  It isolates the lowest-order eta
    # channel but deliberately does not assert a geometric RFDE theorem.
    leading_canard_x = -inner_time / (2 * alpha)
    leading_canard_y = (inner_time**2 - 2) / (4 * alpha)
    delayed_canard_0 = leading_canard_x.subs(
        inner_time, inner_time - theta_0
    )
    delayed_canard_1 = leading_canard_x.subs(
        inner_time, inner_time - theta_1
    )
    delay_translation_difference = sp.simplify(
        delayed_canard_0 - delayed_canard_1
    )
    eta_order_transverse_forcing = sp.simplify(
        sp.diff(
            sp.diff(transverse_rhs_from_model, eta), delta
        ).subs(
            {
                delta: 0,
                eta: 0,
                X: leading_canard_x,
                X_theta_0: delayed_canard_0,
                X_theta_1: delayed_canard_1,
            }
        )
    )
    leading_transverse_linearization = sp.simplify(
        sp.diff(
            transverse_rhs_from_model.subs(delta, 0), Z
        )
    )
    eta_transverse_coefficient = sp.simplify(
        -eta_order_transverse_forcing
        / leading_transverse_linearization
    )
    eta_probe = sp.Symbol("eta_probe", real=True)
    leading_graph_on_canard = leading_graph_z.subs(
        X, leading_canard_x
    )
    critical_eta_probe = critical_rhs_from_model.subs(
        {
            X: leading_canard_x,
            Z: (
                leading_graph_on_canard
                + delta * eta_probe * eta_transverse_coefficient
            ),
        }
    )
    eta_critical_force = sp.simplify(
        sp.limit(
            sp.diff(critical_eta_probe, eta_probe) / delta**2,
            delta,
            0,
        )
    )
    gaussian = sp.exp(-inner_time**2 / 2)
    formal_numerator = sp.simplify(
        sp.integrate(
            gaussian * inner_time * eta_critical_force,
            (inner_time, -sp.oo, sp.oo),
        )
    )
    formal_denominator = sp.simplify(
        sp.integrate(
            gaussian, (inner_time, -sp.oo, sp.oo)
        )
    )
    formal_nu_coefficient = sp.simplify(
        -formal_numerator / formal_denominator
    )
    formal_mu_derivative = sp.simplify(
        delta**3 * formal_nu_coefficient
    )

    return FinalModelBlowup(
        delta=delta,
        eta=eta,
        weak_gain=weak_gain,
        recovery_gap=recovery_gap,
        theta_0=theta_0,
        theta_1=theta_1,
        inner_time=inner_time,
        chart_x=X,
        chart_y=Y,
        chart_z=Z,
        chart_w=W,
        chart_unfolding=nu,
        delayed_x_0=X_theta_0,
        delayed_x_1=X_theta_1,
        delayed_z_0=Z_theta_0,
        delayed_z_1=Z_theta_1,
        sigma=sigma,
        alpha=alpha,
        critical_right=critical_right,
        transverse_right=transverse_right,
        critical_left=critical_left,
        transverse_left=transverse_left,
        critical_projector=critical_projector,
        transverse_projector=transverse_projector,
        equilibrium_v=equilibrium_v,
        equilibrium_w=equilibrium_w,
        layer_0_modal=layer_0_modal,
        layer_1_modal=layer_1_modal,
        total_gain_modal=total_gain_modal,
        redistribution_modal=redistribution_modal,
        singular_jacobian=singular_jacobian,
        singular_characteristic=singular_characteristic,
        scaled_voltage=scaled_voltage,
        scaled_recovery=scaled_recovery,
        scaled_parameter=scaled_parameter,
        critical_voltage_scale=critical_voltage_scale,
        transverse_voltage_scale=transverse_voltage_scale,
        critical_recovery_scale=critical_recovery_scale,
        transverse_recovery_scale=transverse_recovery_scale,
        critical_rhs_from_model=critical_rhs_from_model,
        transverse_rhs_from_model=transverse_rhs_from_model,
        collective_recovery_rhs_from_model=(
            collective_recovery_rhs_from_model
        ),
        transverse_recovery_rhs_from_model=(
            transverse_recovery_rhs_from_model
        ),
        displayed_critical_rhs=displayed_critical_rhs,
        displayed_transverse_rhs=displayed_transverse_rhs,
        displayed_collective_recovery_rhs=(
            displayed_collective_recovery_rhs
        ),
        displayed_transverse_recovery_rhs=(
            displayed_transverse_recovery_rhs
        ),
        critical_residual=critical_residual,
        transverse_residual=transverse_residual,
        collective_recovery_residual=collective_recovery_residual,
        transverse_recovery_residual=transverse_recovery_residual,
        fast_reconstruction_residual=fast_reconstruction_residual,
        slow_reconstruction_residual=slow_reconstruction_residual,
        leading_graph_z=leading_graph_z,
        leading_graph_w=leading_graph_w,
        leading_canard_x=leading_canard_x,
        leading_canard_y=leading_canard_y,
        delay_translation_difference=delay_translation_difference,
        eta_order_transverse_forcing=eta_order_transverse_forcing,
        leading_transverse_linearization=(
            leading_transverse_linearization
        ),
        eta_transverse_coefficient=eta_transverse_coefficient,
        eta_critical_force=eta_critical_force,
        formal_numerator=formal_numerator,
        formal_denominator=formal_denominator,
        formal_nu_coefficient=formal_nu_coefficient,
        formal_mu_derivative=formal_mu_derivative,
    )


if __name__ == "__main__":
    result = final_model_blowup()
    print("critical residual =", result.critical_residual)
    print("transverse residual =", result.transverse_residual)
    print("slow residual =", result.slow_reconstruction_residual)
    print("formal d_eta mu_c =", result.formal_mu_derivative)
