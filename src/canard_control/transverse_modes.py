"""Fold-scaled transverse modes for the two-module delayed VdP/FHN skeleton.

The calculation isolates a feasibility obstruction for the flagship transfer
theorem.  With physical coupling ``J = epsilon*K``, every network eigenmode
has the same leading fold operator.  The coupling separates the modes only in
the ``delta = sqrt(epsilon)`` correction, so a transverse inverse cannot be
assumed uniform as ``epsilon -> 0``.

This module checks algebraic identities and a first Gaussian solvability
projection.  It does not prove a Fredholm theorem or an upper bound for the
full RFDE Green operator.
"""

from __future__ import annotations

from dataclasses import dataclass

import sympy as sp


@dataclass(frozen=True)
class TransverseModeBlowup:
    """Exact physical and fold-scaled linearized mode equations."""

    physical_fast_rhs: sp.Expr
    physical_slow_rhs: sp.Expr
    scaled_fast_rhs: sp.Expr
    scaled_slow_rhs: sp.Expr


@dataclass(frozen=True)
class LeadingFoldMode:
    """Formal whole-line Lyapunov--Schmidt data for one transverse mode.

    These identities diagnose the singular fold chart.  They are not a
    substitute for the Fredholm calculation with the eventual finite Lin
    boundary conditions.
    """

    leading_matrix: sp.Matrix
    tangent_kernel: sp.Matrix
    adjoint_kernel: sp.Matrix
    kernel_residual: sp.Matrix
    adjoint_residual: sp.Matrix
    first_splitting_force: sp.Matrix
    first_splitting_projection: sp.Expr
    first_range_correction: sp.Matrix
    first_range_residual: sp.Matrix
    first_tangent_correction: sp.Matrix
    tangent_correction_residual: sp.Matrix
    second_splitting_projection: sp.Expr


def two_module_eigenpairs() -> tuple[sp.Matrix, sp.Matrix, sp.Matrix, sp.Expr]:
    r"""Return the collective and difference modes of a row-stochastic block matrix.

    The two-module matrix is

    .. math::
       B=\begin{pmatrix}1-p&p\\q&1-q\end{pmatrix}.

    Its collective eigenvalue is one and its difference eigenvalue is
    ``1-p-q``.
    """

    p, q = sp.symbols("p q")
    block_matrix = sp.Matrix([[1 - p, p], [q, 1 - q]])
    collective = sp.Matrix([1, 1])
    difference = sp.Matrix([p, -q])
    difference_eigenvalue = 1 - p - q
    return block_matrix, collective, difference, difference_eigenvalue


def transverse_mode_blowup() -> TransverseModeBlowup:
    r"""Linearize one network eigenmode and apply the exact fold scaling.

    The reference coupling uses the scalar-calibration orientation

    .. math::
       \varepsilon K\,[x_i-\sum_jW_{ij}x_j(t-\tau)].

    For a row-stochastic network eigenmode with eigenvalue ``lambda``, set
    ``x=1+delta*X``, ``dx=delta*u``, ``dy=delta**2*v``, and
    ``s=delta*t``.  The result is

    .. math::
       u'=-2Xu+v+\delta[-X^2u+K(u-\lambda u_\Theta)],
       \qquad v'=-u.
    """

    delta, X, u, u_tau, v, K, lam = sp.symbols(
        "delta X u u_tau v K lambda"
    )
    x = 1 + delta * X
    dx = delta * u
    dy = delta**2 * v
    epsilon = delta**2

    physical_fast_rhs = sp.expand(
        (1 - x**2) * dx
        + dy
        + epsilon * K * (dx - lam * delta * u_tau)
    )
    physical_slow_rhs = sp.expand(-epsilon * dx)

    # d(dx)/dt = delta**2*u' and d(dy)/dt = delta**3*v'.
    scaled_fast_rhs = sp.simplify(physical_fast_rhs / delta**2)
    scaled_slow_rhs = sp.simplify(physical_slow_rhs / delta**3)

    return TransverseModeBlowup(
        physical_fast_rhs=physical_fast_rhs,
        physical_slow_rhs=physical_slow_rhs,
        scaled_fast_rhs=scaled_fast_rhs,
        scaled_slow_rhs=scaled_slow_rhs,
    )


def leading_fold_mode() -> LeadingFoldMode:
    r"""Return the repeated leading kernel and its Gaussian adjoint.

    On the canonical leading canard, choose the time origin so that
    ``X_0(s)=-s/2``.  The variational matrix is

    .. math::
       A_0(s)=\begin{pmatrix}s&1\\-1&0\end{pmatrix}.

    The time tangent and an integrable adjoint kernel are

    .. math::
       \phi=(-1,s)^T,
       \qquad
       \psi=e^{-s^2/2}(s,1)^T.

    For a network eigenvalue ``lambda``, write
    ``kappa = K*(1-lambda)``.  The first difference from the collective
    Lin operator sends ``phi`` to ``(kappa, 0)``.  Its whole-line Gaussian
    projection vanishes, and ``(0, kappa)`` solves the corresponding range
    equation.

    Including the first collective-orbit correction for

    .. math::
       Y'=-X+\delta(\nu-bY)

    gives the formal second reduced coefficient

    .. math::
       K(1-\lambda)(1+2b)\sqrt{2\pi}/4.

    This coefficient is specific to the canonical symmetric whole-line
    inner problem.  Finite or asymmetric Lin sections contribute boundary
    terms and must be analyzed separately.
    """

    s, K, lam, b, theta = sp.symbols(
        "s K lambda b Theta", real=True
    )
    leading_matrix = sp.Matrix([[s, 1], [-1, 0]])
    tangent_kernel = sp.Matrix([-1, s])
    gaussian = sp.exp(-(s**2) / 2)
    adjoint_kernel = gaussian * sp.Matrix([s, 1])

    kernel_residual = sp.simplify(
        tangent_kernel.diff(s) - leading_matrix * tangent_kernel
    )
    adjoint_residual = sp.simplify(
        -adjoint_kernel.diff(s) - leading_matrix.T * adjoint_kernel
    )

    kappa = K * (1 - lam)
    first_splitting_force = sp.Matrix([kappa, 0])
    integrand = sp.expand((adjoint_kernel.T * first_splitting_force)[0])
    first_splitting_projection = sp.simplify(
        sp.integrate(integrand, (s, -sp.oo, sp.oo))
    )

    first_range_correction = sp.Matrix([0, kappa])
    first_range_residual = sp.simplify(
        first_range_correction.diff(s)
        - leading_matrix * first_range_correction
        + first_splitting_force
    )

    alpha = sp.Rational(1, 4) - b / 2
    c = (1 + 2 * b) / 8
    first_tangent_correction = sp.Matrix(
        [
            -alpha * s,
            (alpha - b) * s**2 / 2 - alpha,
        ]
    )
    first_collective_operator_on_tangent = sp.Matrix(
        [-c * s**2, b * s]
    )
    tangent_correction_residual = sp.simplify(
        first_tangent_correction.diff(s)
        - leading_matrix * first_tangent_correction
        + first_collective_operator_on_tangent
    )
    delayed_first_component = first_tangent_correction[0].subs(
        s, s - theta
    )
    first_operator_on_range = sp.Matrix([0, b * kappa])
    mode_operator_on_tangent_correction = sp.Matrix(
        [-kappa * delayed_first_component, 0]
    )
    second_integrand = sp.expand(
        (
            adjoint_kernel.T
            * (
                first_operator_on_range
                + mode_operator_on_tangent_correction
            )
        )[0]
    )
    second_splitting_projection = sp.simplify(
        sp.integrate(second_integrand, (s, -sp.oo, sp.oo))
    )

    return LeadingFoldMode(
        leading_matrix=leading_matrix,
        tangent_kernel=tangent_kernel,
        adjoint_kernel=adjoint_kernel,
        kernel_residual=kernel_residual,
        adjoint_residual=adjoint_residual,
        first_splitting_force=first_splitting_force,
        first_splitting_projection=first_splitting_projection,
        first_range_correction=first_range_correction,
        first_range_residual=first_range_residual,
        first_tangent_correction=first_tangent_correction,
        tangent_correction_residual=tangent_correction_residual,
        second_splitting_projection=second_splitting_projection,
    )


if __name__ == "__main__":
    result = leading_fold_mode()
    print("kernel residual =", result.kernel_residual)
    print("adjoint residual =", result.adjoint_residual)
    print("first splitting projection =", result.first_splitting_projection)
    print("first range residual =", result.first_range_residual)
    print("tangent correction residual =", result.tangent_correction_residual)
    print("second splitting projection =", result.second_splitting_projection)
