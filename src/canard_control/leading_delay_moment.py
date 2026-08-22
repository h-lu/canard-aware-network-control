"""Leading delayed-canard coefficient from polynomial solvability.

This is an independent SymPy derivation in the normalization fixed by
``symbolic_blowup.py``.  It computes only the first two parameter coefficients;
it is not a replacement for the high-order nonlocal center-manifold proof.
"""

from __future__ import annotations

from dataclasses import dataclass

import sympy as sp


@dataclass(frozen=True)
class LeadingDelayResult:
    """Objects required by the first two solvability conditions."""

    critical_graph_0: sp.Expr
    delayed_state_0: sp.Expr
    critical_graph_1: sp.Expr
    fast_field_1: sp.Expr
    delayed_state_1: sp.Expr
    critical_graph_2: sp.Expr
    nu_0: sp.Expr
    nu_1: sp.Expr


@dataclass(frozen=True)
class LeadingDistributedDelayResult:
    """First coefficients for a normalized row-equivalent delay measure."""

    critical_graph_0: sp.Expr
    critical_graph_1: sp.Expr
    fast_field_1: sp.Expr
    mean_delayed_state_1: sp.Expr
    critical_graph_2: sp.Expr
    nu_0: sp.Expr
    nu_1: sp.Expr


def _solve_polynomial_identity(
    expression: sp.Expr,
    variable: sp.Symbol,
    unknowns: tuple[sp.Symbol, ...],
) -> dict[sp.Symbol, sp.Expr]:
    equations = sp.Poly(sp.expand(expression), variable).all_coeffs()
    solutions = sp.solve(equations, unknowns, dict=True)
    if len(solutions) != 1:
        raise ValueError(f"Expected one polynomial solution, found {len(solutions)}")
    return solutions[0]


def leading_delay_coefficients() -> LeadingDelayResult:
    r"""Derive ``nu_0=-1/8`` and ``nu_1=K*Theta/8``.

    For the scaled system

    .. math::
       X'=Y-X^2+\delta[-X^3/3+K(X-X_\Theta)],\qquad
       Y'=-X+\delta\nu,

    seek ``Y(X;delta)`` and ``nu(delta)`` as power series.  The delay map is
    imposed by ``W(X)-W(X_Theta)=Theta`` with ``W'=1/X'``.
    """

    X, K, Theta = sp.symbols("X K Theta")
    nu_0, nu_1 = sp.symbols("nu_0 nu_1")

    Y_0 = X**2 - sp.Rational(1, 2)
    V_0 = -sp.Rational(1, 2)
    X_theta_0 = X + Theta / 2
    delayed_force_0 = -X**3 / 3 + K * (X - X_theta_0)

    a = sp.symbols("a0:4")
    Y_1_ansatz = sum(a[k] * X**k for k in range(4))
    order_1 = (
        sp.diff(Y_0, X) * (Y_1_ansatz + delayed_force_0)
        + sp.diff(Y_1_ansatz, X) * V_0
        - nu_0
    )
    solution_1 = _solve_polynomial_identity(
        order_1, X, (*a, nu_0)
    )
    Y_1 = sp.expand(Y_1_ansatz.subs(solution_1))
    solved_nu_0 = sp.simplify(solution_1[nu_0])

    V_1 = sp.simplify(Y_1 + delayed_force_0)
    W_0 = -2 * X
    W_1 = sp.integrate(-V_1 / V_0**2, X)
    X_theta_1 = sp.simplify(
        (W_1 - W_1.subs(X, X_theta_0)) / sp.diff(W_0, X)
    )

    b = sp.symbols("b0:3")
    Y_2_ansatz = sum(b[k] * X**k for k in range(3))
    delayed_force_1 = -K * X_theta_1
    V_2 = Y_2_ansatz + delayed_force_1
    order_2 = (
        sp.diff(Y_0, X) * V_2
        + sp.diff(Y_1, X) * V_1
        + sp.diff(Y_2_ansatz, X) * V_0
        - nu_1
    )
    solution_2 = _solve_polynomial_identity(
        order_2, X, (*b, nu_1)
    )
    Y_2 = sp.expand(Y_2_ansatz.subs(solution_2))
    solved_nu_1 = sp.simplify(solution_2[nu_1])

    return LeadingDelayResult(
        critical_graph_0=Y_0,
        delayed_state_0=X_theta_0,
        critical_graph_1=Y_1,
        fast_field_1=V_1,
        delayed_state_1=X_theta_1,
        critical_graph_2=Y_2,
        nu_0=solved_nu_0,
        nu_1=solved_nu_1,
    )


def leading_distributed_delay_coefficients() -> LeadingDistributedDelayResult:
    r"""Derive the leading law for a row-equivalent delay measure.

    Let ``m_1`` and ``m_2`` be its first two scaled-delay moments.  Along the
    zeroth-order critical orbit,

    ``E[X_Theta,0] = X + m_1/2`` and
    ``E[X_Theta,1] = -(m_2 + 4*X*m_1)/16``.

    Polynomial solvability then selects ``nu_1 = K*m_1/8``; the second moment
    changes the critical graph but not this parameter coefficient.
    """

    X, K, m_1, m_2 = sp.symbols("X K m_1 m_2")
    nu_0, nu_1 = sp.symbols("nu_0 nu_1")

    Y_0 = X**2 - sp.Rational(1, 2)
    V_0 = -sp.Rational(1, 2)
    mean_delayed_state_0 = X + m_1 / 2
    delayed_force_0 = -X**3 / 3 + K * (X - mean_delayed_state_0)

    a = sp.symbols("da0:4")
    Y_1_ansatz = sum(a[k] * X**k for k in range(4))
    order_1 = (
        sp.diff(Y_0, X) * (Y_1_ansatz + delayed_force_0)
        + sp.diff(Y_1_ansatz, X) * V_0
        - nu_0
    )
    solution_1 = _solve_polynomial_identity(
        order_1, X, (*a, nu_0)
    )
    Y_1 = sp.expand(Y_1_ansatz.subs(solution_1))
    V_1 = sp.simplify(Y_1 + delayed_force_0)

    mean_delayed_state_1 = -(m_2 + 4 * X * m_1) / 16
    delayed_force_1 = -K * mean_delayed_state_1
    b = sp.symbols("db0:3")
    Y_2_ansatz = sum(b[k] * X**k for k in range(3))
    order_2 = (
        sp.diff(Y_0, X) * (Y_2_ansatz + delayed_force_1)
        + sp.diff(Y_1, X) * V_1
        + sp.diff(Y_2_ansatz, X) * V_0
        - nu_1
    )
    solution_2 = _solve_polynomial_identity(
        order_2, X, (*b, nu_1)
    )

    return LeadingDistributedDelayResult(
        critical_graph_0=Y_0,
        critical_graph_1=Y_1,
        fast_field_1=V_1,
        mean_delayed_state_1=mean_delayed_state_1,
        critical_graph_2=sp.expand(Y_2_ansatz.subs(solution_2)),
        nu_0=sp.simplify(solution_1[nu_0]),
        nu_1=sp.simplify(solution_2[nu_1]),
    )


if __name__ == "__main__":
    result = leading_delay_coefficients()
    print("nu_0 =", result.nu_0)
    print("nu_1 =", result.nu_1)
