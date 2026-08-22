"""Exact symbolic scaling check for the weakly delayed van der Pol fold chart.

The calculation deliberately stops before a history Taylor expansion: the
scaled delay Theta is O(1), so replacing X(s-Theta) by a short Taylor series is
not justified without the nonlocal center-manifold argument.
"""

from __future__ import annotations

from dataclasses import dataclass

import sympy as sp


@dataclass(frozen=True)
class BlowupResult:
    """Symbolic identities before and after division by the chart scale."""

    local_fast_rhs: sp.Expr
    delayed_fast_rhs: sp.Expr
    slow_rhs: sp.Expr
    scaled_fast_rhs: sp.Expr
    scaled_slow_rhs: sp.Expr


def delayed_vdp_blowup() -> BlowupResult:
    r"""Return the exact right-fold blow-up identities.

    Starting system in fast time ``t``:

    .. math::
       \dot x=x-x^3/3+y+J[x(t)-x(t-\tau)],\qquad
       \dot y=\varepsilon(a-x).

    Substitute ``epsilon=delta**2``, ``x=1+delta*X``,
    ``y=-2/3+delta**2*Y``, ``s=delta*t``, ``J=delta**2*K``,
    ``Theta=delta*tau``, and ``a=1+delta**2*nu``.
    """

    delta, X, X_tau, Y, K, nu = sp.symbols(
        "delta X X_tau Y K nu", nonzero=True
    )
    x = 1 + delta * X
    y = -sp.Rational(2, 3) + delta**2 * Y
    a = 1 + delta**2 * nu
    epsilon = delta**2
    J = delta**2 * K

    local_fast_rhs = sp.expand(x - x**3 / 3 + y)
    delayed_fast_rhs = sp.expand(J * (x - (1 + delta * X_tau)))
    slow_rhs = sp.expand(epsilon * (a - x))

    # dx/dt = delta**2 dX/ds and dy/dt = delta**3 dY/ds.
    scaled_fast_rhs = sp.simplify(
        (local_fast_rhs + delayed_fast_rhs) / delta**2
    )
    scaled_slow_rhs = sp.simplify(slow_rhs / delta**3)

    return BlowupResult(
        local_fast_rhs=local_fast_rhs,
        delayed_fast_rhs=delayed_fast_rhs,
        slow_rhs=slow_rhs,
        scaled_fast_rhs=scaled_fast_rhs,
        scaled_slow_rhs=scaled_slow_rhs,
    )


if __name__ == "__main__":
    result = delayed_vdp_blowup()
    print("dX/ds =", result.scaled_fast_rhs)
    print("dY/ds =", result.scaled_slow_rhs)
