"""Exact physical-modal identities used by the outer matching argument.

The audit starts from the already independently reconstructed chart in
``final_model_blowup`` and undoes its anisotropic scaling.  It therefore
checks the physical modal equations, rather than introducing another model.
The singular-curve and small fast-eigenvalue coefficients are formal Taylor
jets of exact polynomial equations; no invariant RFDE slow manifold is
asserted here.
"""

from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

from .final_model_blowup import final_model_blowup


@dataclass(frozen=True)
class OuterModalAudit:
    """Physical modal equations and exact singular Taylor coefficients."""

    delta: sp.Symbol
    epsilon: sp.Expr
    critical_voltage: sp.Symbol
    transverse_voltage: sp.Symbol
    critical_recovery: sp.Symbol
    transverse_recovery: sp.Symbol
    unfolding: sp.Symbol
    delayed_critical_0: sp.Symbol
    delayed_critical_1: sp.Symbol
    delayed_transverse_0: sp.Symbol
    delayed_transverse_1: sp.Symbol
    alpha: sp.Expr
    critical_voltage_rhs: sp.Expr
    transverse_voltage_rhs: sp.Expr
    critical_recovery_rhs: sp.Expr
    transverse_recovery_rhs: sp.Expr
    singular_transverse_series: sp.Expr
    singular_recovery_series: sp.Expr
    small_fast_eigenvalue_series: sp.Expr
    slow_time_delay_0: sp.Expr
    slow_time_delay_1: sp.Expr


def _series_branch(
    equation: sp.Expr,
    independent: sp.Symbol,
    dependent: sp.Symbol,
    first_power: int,
    stop_power: int,
) -> sp.Expr:
    """Solve a unique formal branch coefficient by coefficient."""

    coefficients = sp.symbols(
        f"c_{first_power}:{stop_power}", real=True
    )
    ansatz = sum(
        coefficients[power - first_power] * independent**power
        for power in range(first_power, stop_power)
    )
    expanded = sp.series(
        equation.subs(dependent, ansatz),
        independent,
        0,
        stop_power,
    ).removeO().expand()
    solution: dict[sp.Symbol, sp.Expr] = {}
    for power in range(first_power, stop_power):
        coefficient = coefficients[power - first_power]
        scalar_equation = sp.expand(expanded.subs(solution)).coeff(
            independent, power
        )
        roots = sp.solve(scalar_equation, coefficient)
        if len(roots) != 1:
            raise RuntimeError(
                f"formal branch is not unique at power {power}"
            )
        solution[coefficient] = sp.simplify(roots[0])
    return sp.expand(ansatz.subs(solution))


def outer_modal_audit() -> OuterModalAudit:
    r"""Undo the inner scaling and compute the local outer singular jets.

    Physical modal variables are

    .. math::
       \xi=\delta X,\quad \zeta=\delta^2 Z,\quad
       \rho=-\delta^2Y,\quad \kappa=\delta^4W,
       \quad \mu=\delta^2\nu.

    The slow time is ``T=epsilon*t``.  Hence a physical delay
    ``theta_k/delta`` is exactly the small slow-time shift
    ``delta*theta_k``.
    """

    chart = final_model_blowup()
    delta = chart.delta
    epsilon = delta**2
    xi, zeta, rho, kappa, mu = sp.symbols(
        "xi zeta rho kappa mu", real=True
    )
    xi_0, xi_1, zeta_0, zeta_1 = sp.symbols(
        "xi_0 xi_1 zeta_0 zeta_1", real=True
    )
    X, Y, Z, W, nu = sp.symbols("X Y Z W nu", real=True)

    physical_substitution = {
        X: xi / delta,
        Y: -rho / delta**2,
        Z: zeta / delta**2,
        W: kappa / delta**4,
        nu: mu / delta**2,
        chart.delayed_x_0: xi_0 / delta,
        chart.delayed_x_1: xi_1 / delta,
        chart.delayed_z_0: zeta_0 / delta**2,
        chart.delayed_z_1: zeta_1 / delta**2,
    }

    # Since ds/dt=delta, dot(xi)=delta**2 X',
    # dot(zeta)=delta**2(delta Z'), dot(rho)=-delta**3 Y', and
    # dot(kappa)=delta**4(delta W').
    critical_voltage_rhs = sp.expand(
        delta**2
        * chart.displayed_critical_rhs.subs(physical_substitution)
    )
    transverse_voltage_rhs = sp.expand(
        delta**2
        * chart.displayed_transverse_rhs.subs(physical_substitution)
    )
    critical_recovery_rhs = sp.expand(
        -delta**3
        * chart.displayed_collective_recovery_rhs.subs(
            physical_substitution
        )
    )
    transverse_recovery_rhs = sp.expand(
        delta**4
        * chart.displayed_transverse_recovery_rhs.subs(
            physical_substitution
        )
    )
    local_substitution = {
        delta: 0,
        chart.weak_gain: 0,
        rho: 0,
        kappa: 0,
    }
    singular_transverse_equation = sp.expand(
        transverse_voltage_rhs.subs(local_substitution)
    )
    singular_transverse_series = _series_branch(
        singular_transverse_equation,
        xi,
        zeta,
        first_power=2,
        stop_power=7,
    )

    # On the fast equilibrium curve kappa=0.  The critical equation is
    # ``-rho + local_polynomial = 0``.
    singular_recovery_series = sp.series(
        (critical_voltage_rhs + rho)
        .subs({delta: 0, chart.weak_gain: 0, zeta: singular_transverse_series}),
        xi,
        0,
        7,
    ).removeO().expand()

    local_critical = sp.expand(
        (critical_voltage_rhs + rho).subs(
            {delta: 0, chart.weak_gain: 0}
        )
    )
    local_transverse = sp.expand(
        (transverse_voltage_rhs + kappa).subs(
            {delta: 0, chart.weak_gain: 0}
        )
    )
    fast_jacobian = sp.Matrix(
        [local_critical, local_transverse]
    ).jacobian((xi, zeta)).subs(
        zeta, singular_transverse_series
    )
    spectral = sp.Symbol("lambda", real=True)
    characteristic = sp.expand(
        (spectral * sp.eye(2) - fast_jacobian).det()
    )
    eigen_coefficients = sp.symbols("d_1:5", real=True)
    eigen_ansatz = sum(
        eigen_coefficients[power - 1] * xi**power
        for power in range(1, 5)
    )
    eigen_equation = sp.series(
        characteristic.subs(spectral, eigen_ansatz), xi, 0, 5
    ).removeO().expand()
    eigen_solution: dict[sp.Symbol, sp.Expr] = {}
    for power, coefficient in enumerate(eigen_coefficients, start=1):
        scalar_equation = sp.expand(
            eigen_equation.subs(eigen_solution)
        ).coeff(xi, power)
        roots = sp.solve(scalar_equation, coefficient)
        if len(roots) != 1:
            raise RuntimeError(
                f"small eigenvalue jet is not unique at power {power}"
            )
        eigen_solution[coefficient] = sp.simplify(roots[0])
    small_fast_eigenvalue_series = sp.expand(
        eigen_ansatz.subs(eigen_solution)
    )

    return OuterModalAudit(
        delta=delta,
        epsilon=epsilon,
        critical_voltage=xi,
        transverse_voltage=zeta,
        critical_recovery=rho,
        transverse_recovery=kappa,
        unfolding=mu,
        delayed_critical_0=xi_0,
        delayed_critical_1=xi_1,
        delayed_transverse_0=zeta_0,
        delayed_transverse_1=zeta_1,
        alpha=chart.alpha,
        critical_voltage_rhs=critical_voltage_rhs,
        transverse_voltage_rhs=transverse_voltage_rhs,
        critical_recovery_rhs=critical_recovery_rhs,
        transverse_recovery_rhs=transverse_recovery_rhs,
        singular_transverse_series=singular_transverse_series,
        singular_recovery_series=singular_recovery_series,
        small_fast_eigenvalue_series=small_fast_eigenvalue_series,
        slow_time_delay_0=sp.simplify(epsilon * chart.theta_0 / delta),
        slow_time_delay_1=sp.simplify(epsilon * chart.theta_1 / delta),
    )
