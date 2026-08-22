"""Executable algebra for the canonical one-sided canard Green operator.

Only the identities of the leading planar variational equation are exact
certificates here.  Uniform nonlinear trace estimates are analytic results,
not consequences of this module.
"""

from __future__ import annotations

from dataclasses import dataclass

import sympy as sp


@dataclass(frozen=True)
class GreenPhaseAudit:
    """Symbolic tangent-normal frame and boundary identities."""

    phase: sp.Symbol
    alpha: sp.Symbol
    exponential: sp.Expr
    integral: sp.Expr
    tangent: sp.Matrix
    normal: sp.Matrix
    variational_matrix: sp.Matrix
    tangent_residual: sp.Matrix
    normal_residual: sp.Matrix
    frame_determinant: sp.Expr
    forcing: sp.Matrix
    tangent_coefficient_derivative: sp.Expr
    normal_coefficient_derivative: sp.Expr
    reconstruction_residual: sp.Matrix
    phase_value: sp.Expr
    h_boundary_residual: sp.Expr


def green_phase_audit() -> GreenPhaseAudit:
    r"""Return exact identities for ``L0(U,V)=(U'-sU-V,V'+U)``."""

    s, t = sp.symbols("s t", real=True)
    alpha = sp.Symbol("alpha", positive=True)
    E = sp.exp(s**2 / 2)
    I = sp.Integral(sp.exp(t**2 / 2), (t, 0, s))
    tangent = sp.Matrix([-1, s])
    normal = sp.Matrix([I, E - s * I])
    variational_matrix = sp.Matrix([[s, 1], [-1, 0]])

    tangent_residual = sp.simplify(
        tangent.diff(s) - variational_matrix * tangent
    )
    # Fundamental theorem of calculus is encoded explicitly because SymPy
    # deliberately leaves the non-elementary integral unevaluated.
    normal_derivative = sp.Matrix(
        [E, s * E - I - s * E]
    )
    normal_residual = sp.simplify(
        normal_derivative - variational_matrix * normal
    )
    frame = sp.Matrix.hstack(tangent, normal)
    frame_determinant = sp.simplify(frame.det())

    f_1, f_2 = sp.symbols("f_1 f_2", real=True)
    forcing = sp.Matrix([f_1, f_2])
    coefficient_derivative = sp.simplify(frame.inv() * forcing)

    a, b = sp.symbols("a b", real=True)
    U, V = sp.symbols("U V", real=True)
    coordinates = sp.Matrix(
        [
            sp.exp(-s**2 / 2) * (-(E - s * I) * U + I * V),
            sp.exp(-s**2 / 2) * (s * U + V),
        ]
    )
    reconstruction_residual = sp.simplify(
        frame * coordinates - sp.Matrix([U, V])
    )
    # At s=0, U=-a because I(0)=0; hence U=0 removes the tangent mode.
    phase_value = sp.simplify(
        (a * tangent + b * normal)[0].subs(s, 0)
    )

    # The exact H=0 boundary equation in perturbation coordinates is
    # s*U+V=alpha*U**2.  Substitution of U=-a+I*b and sU+V=E*b yields this
    # residual.
    U_frame = -a + I * b
    h_boundary_residual = sp.expand(
        (s * (a * tangent + b * normal)[0]
         + (a * tangent + b * normal)[1]
         - alpha * U_frame**2)
        - (E * b - alpha * U_frame**2)
    )

    return GreenPhaseAudit(
        phase=s,
        alpha=alpha,
        exponential=E,
        integral=I,
        tangent=tangent,
        normal=normal,
        variational_matrix=variational_matrix,
        tangent_residual=tangent_residual,
        normal_residual=normal_residual,
        frame_determinant=frame_determinant,
        forcing=forcing,
        tangent_coefficient_derivative=coefficient_derivative[0],
        normal_coefficient_derivative=coefficient_derivative[1],
        reconstruction_residual=reconstruction_residual,
        phase_value=phase_value,
        h_boundary_residual=sp.simplify(h_boundary_residual),
    )
