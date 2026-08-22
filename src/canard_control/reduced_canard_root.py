"""Exact coefficient audit for the reduced planar canard root.

This module starts from the audited formal special-flow invariance jet.  It
checks the canonical planar normalization, the candidate leading parameter,
and the mixed ``delta * eta`` Gaussian coefficient in the conditional
normalized gap.  It deliberately does *not* construct the attracting and
repelling slow curves at infinity.  The graph mixed-regularity and geometric
K1/tail-admissibility statements are separate from the symbolic identities
certified here.
"""

from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

from canard_control.final_model_blowup import final_model_blowup
from canard_control.nonlocal_graph_jet import nonlocal_graph_jet_audit


@dataclass(frozen=True)
class ReducedCanardRootAudit:
    """Symbolic data entering the parameterized splitting proposition."""

    delta: sp.Symbol
    eta: sp.Symbol
    weak_gain: sp.Symbol
    theta_0: sp.Symbol
    theta_1: sp.Symbol
    alpha: sp.Expr
    inner_time: sp.Symbol
    unfolding: sp.Symbol
    section_radius: sp.Symbol
    leading_canard: sp.Matrix
    canonical_canard: sp.Matrix
    canonical_vector_field_residual: sp.Matrix
    canonical_first_integral: sp.Expr
    first_integral_residual: sp.Expr
    adjoint: sp.Matrix
    adjoint_residual: sp.Matrix
    first_reduced_fast_jet_on_canard: sp.Expr
    first_reduced_slow_jet_on_canard: sp.Expr
    leading_normalized_gap: sp.Expr
    leading_gap_unfolding_derivative: sp.Expr
    baseline_unfolding: sp.Expr
    eta_second_fast_jet_on_canard: sp.Expr
    mixed_eta_gap_coefficient: sp.Expr
    eta_root_coefficient: sp.Expr
    leading_root_difference: sp.Expr
    leading_physical_difference: sp.Expr
    ks_inner_parameter: sp.Expr
    ks_physical_parameter: sp.Expr
    ks_physical_difference: sp.Expr
    gaussian_mass: sp.Expr
    finite_gaussian_mass: sp.Expr
    finite_second_moment: sp.Expr
    omitted_second_moment: sp.Expr
    tail_accounting_residual: sp.Expr


def reduced_canard_root_audit() -> ReducedCanardRootAudit:
    """Derive conditional root coefficients from the exact formal jet."""

    base = final_model_blowup()
    graph = nonlocal_graph_jet_audit()

    delta = base.delta
    eta = base.eta
    weak_gain = base.weak_gain
    theta_0 = base.theta_0
    theta_1 = base.theta_1
    alpha = base.alpha
    inner_time = base.inner_time
    unfolding = base.chart_unfolding
    X = base.chart_x
    Y = base.chart_y

    leading_canard = sp.Matrix(
        [base.leading_canard_x, base.leading_canard_y]
    )

    # Krupa--Szmolyan rescaling-chart coordinates.  No time rescaling is
    # needed: x=-alpha*X and y=alpha*Y transform q_0 exactly to
    # x'=-y+x**2, y'=x.
    x, y = sp.symbols("x y", real=True)
    q_0 = sp.Matrix([Y - alpha * X**2, -X])
    canonical_rhs_from_q_0 = sp.Matrix(
        [-alpha * q_0[0], alpha * q_0[1]]
    ).subs({X: -x / alpha, Y: y / alpha})
    canonical_rhs = sp.Matrix([-y + x**2, x])
    canonical_vector_field_residual = sp.simplify(
        canonical_rhs_from_q_0 - canonical_rhs
    )
    canonical_canard = sp.simplify(
        sp.Matrix(
            [
                -alpha * leading_canard[0],
                alpha * leading_canard[1],
            ]
        )
    )

    canonical_first_integral = (
        sp.exp(-2 * y) * (y - x**2 + sp.Rational(1, 2)) / 2
    )
    first_integral_residual = sp.simplify(
        sp.Matrix(
            [
                sp.diff(canonical_first_integral, x),
                sp.diff(canonical_first_integral, y),
            ]
        ).dot(canonical_rhs)
    )

    # Linearization along the leading canard in the (X,Y) chart.
    variational_matrix = sp.Matrix([[inner_time, 1], [-1, 0]])
    gaussian = sp.exp(-inner_time**2 / 2)
    adjoint = gaussian * sp.Matrix([inner_time, 1])
    adjoint_residual = sp.simplify(
        sp.diff(adjoint, inner_time)
        + variational_matrix.T * adjoint
    )

    # Extract Q_1 from the exact shifted graph equation rather than entering
    # a second hard-coded copy.  At delta=0 the shifted stable graph is zero.
    q_1_fast = graph.center_remainder.subs(
        {
            graph.delta: 0,
            graph.shifted_voltage: 0,
            graph.shifted_recovery: 0,
            X: leading_canard[0],
            base.delayed_x_0: leading_canard[0].subs(
                inner_time, inner_time - theta_0
            ),
            base.delayed_x_1: leading_canard[0].subs(
                inner_time, inner_time - theta_1
            ),
        }
    )
    first_reduced_fast_jet_on_canard = sp.simplify(q_1_fast)
    first_reduced_slow_jet_on_canard = unfolding

    gaussian_mass = sp.integrate(
        gaussian, (inner_time, -sp.oo, sp.oo)
    )
    leading_normalized_gap = sp.simplify(
        sp.integrate(
            adjoint[0] * first_reduced_fast_jet_on_canard
            + adjoint[1] * first_reduced_slow_jet_on_canard,
            (inner_time, -sp.oo, sp.oo),
        )
    )
    leading_gap_unfolding_derivative = sp.simplify(
        sp.diff(leading_normalized_gap, unfolding)
    )
    baseline_solutions = sp.solve(
        sp.Eq(leading_normalized_gap, 0), unfolding
    )
    if len(baseline_solutions) != 1:
        raise RuntimeError("the leading normalized gap is not simple")
    baseline_unfolding = sp.simplify(baseline_solutions[0])

    # This is partial_eta Q_{2,X}(gamma_0), already derived from the exact
    # nonlocal graph equation.  Its pairing is the mixed gap coefficient.
    eta_second_fast_jet_on_canard = sp.simplify(
        graph.eta_second_center_jet_on_canard
    )
    mixed_eta_gap_coefficient = sp.simplify(
        sp.integrate(
            adjoint[0] * eta_second_fast_jet_on_canard,
            (inner_time, -sp.oo, sp.oo),
        )
    )
    eta_root_coefficient = sp.simplify(
        -mixed_eta_gap_coefficient
        / leading_gap_unfolding_derivative
    )
    leading_root_difference = sp.simplify(
        delta * eta * eta_root_coefficient
    )
    leading_physical_difference = sp.simplify(
        delta**2 * leading_root_difference
    )

    # In the Krupa--Szmolyan notation r_2=delta and
    # lambda_2=lambda_KS/delta=-alpha*delta*nu.  Consequently the physical
    # KS parameter is lambda_KS=-alpha*mu.
    ks_inner_parameter = sp.simplify(-alpha * delta * unfolding)
    ks_physical_parameter = sp.simplify(
        delta * ks_inner_parameter
    )
    ks_physical_difference = sp.simplify(
        -alpha * leading_physical_difference
    )

    # A finite-section interior pairing omits a nonzero Gaussian tail.  The
    # identity below is bookkeeping only; the geometric origin of that tail
    # must be supplied by the selected K1 slow-manifold traces.
    section_radius = sp.Symbol("L", positive=True)
    finite_gaussian_mass = sp.integrate(
        gaussian, (inner_time, -section_radius, section_radius)
    )
    finite_second_moment = sp.integrate(
        inner_time**2 * gaussian,
        (inner_time, -section_radius, section_radius),
    )
    omitted_second_moment = sp.simplify(
        gaussian_mass - finite_second_moment
    )
    tail_accounting_residual = sp.simplify(
        finite_second_moment
        + omitted_second_moment
        - gaussian_mass
    )

    return ReducedCanardRootAudit(
        delta=delta,
        eta=eta,
        weak_gain=weak_gain,
        theta_0=theta_0,
        theta_1=theta_1,
        alpha=alpha,
        inner_time=inner_time,
        unfolding=unfolding,
        section_radius=section_radius,
        leading_canard=leading_canard,
        canonical_canard=canonical_canard,
        canonical_vector_field_residual=(
            canonical_vector_field_residual
        ),
        canonical_first_integral=canonical_first_integral,
        first_integral_residual=first_integral_residual,
        adjoint=adjoint,
        adjoint_residual=adjoint_residual,
        first_reduced_fast_jet_on_canard=(
            first_reduced_fast_jet_on_canard
        ),
        first_reduced_slow_jet_on_canard=(
            first_reduced_slow_jet_on_canard
        ),
        leading_normalized_gap=leading_normalized_gap,
        leading_gap_unfolding_derivative=(
            leading_gap_unfolding_derivative
        ),
        baseline_unfolding=baseline_unfolding,
        eta_second_fast_jet_on_canard=(
            eta_second_fast_jet_on_canard
        ),
        mixed_eta_gap_coefficient=mixed_eta_gap_coefficient,
        eta_root_coefficient=eta_root_coefficient,
        leading_root_difference=leading_root_difference,
        leading_physical_difference=leading_physical_difference,
        ks_inner_parameter=ks_inner_parameter,
        ks_physical_parameter=ks_physical_parameter,
        ks_physical_difference=ks_physical_difference,
        gaussian_mass=gaussian_mass,
        finite_gaussian_mass=finite_gaussian_mass,
        finite_second_moment=finite_second_moment,
        omitted_second_moment=omitted_second_moment,
        tail_accounting_residual=tail_accounting_residual,
    )


if __name__ == "__main__":
    audit = reduced_canard_root_audit()
    print("nu_0 =", audit.baseline_unfolding)
    print("partial_eta mixed gap =", audit.mixed_eta_gap_coefficient)
    print("delta*eta root coefficient =", audit.leading_root_difference)
    print("physical mu difference =", audit.leading_physical_difference)
