"""Exact two-module audit showing when a scalar delay moment is incomplete.

The construction keeps the total delayed-gain matrix and its projected first
moment fixed while redistributing two delay layers.  The redistribution is
invisible to the critical left projection but forces the transverse mode.

All identities in this module are exact finite-dimensional algebra.  The
candidate canard-threshold expansion and its uniform remainder are not proved
here.
"""

from __future__ import annotations

from dataclasses import dataclass

import sympy as sp


@dataclass(frozen=True)
class TwoModuleMomentAudit:
    """Exact mode, delay-layer, and nonlinear feedback identities."""

    sigma: sp.Expr
    equilibrium_v: sp.Matrix
    equilibrium_w: sp.Matrix
    fast_jacobian: sp.Matrix
    critical_right: sp.Matrix
    critical_left: sp.Matrix
    critical_projector: sp.Matrix
    transverse_projector: sp.Matrix
    transverse_vector: sp.Matrix
    total_gain: sp.Matrix
    layer_0: sp.Matrix
    layer_1: sp.Matrix
    redistribution: sp.Matrix
    perturbed_layer_0: sp.Matrix
    perturbed_layer_1: sp.Matrix
    fast_kernel_residual: sp.Matrix
    adjoint_kernel_residual: sp.Matrix
    fold_nondegeneracy: sp.Expr
    total_gain_residual: sp.Matrix
    layer_0_mode_residual: sp.Matrix
    layer_1_mode_residual: sp.Matrix
    projected_layer_0_weight: sp.Expr
    projected_layer_1_weight: sp.Expr
    first_moment_vector: sp.Matrix
    projected_first_moment: sp.Expr
    transverse_first_moment: sp.Matrix
    transverse_fast_response: sp.Matrix
    nonlinear_return_coefficient: sp.Expr


def two_module_moment_audit() -> TwoModuleMomentAudit:
    r"""Build the positive two-delay family and verify its exact identities.

    The FHN fast core is

    .. math::
       F_1=v_1-v_1^3/3-w_1+(v_2-v_1)/2,

    .. math::
       F_2=v_2-v_2^3/3-w_2+2(v_1-v_2).

    At ``v_*=(sqrt(3/2),0)`` its critical right and left modes are
    ``r=(1,2)`` and ``ell=(1/2,1/4)``.  Weak feedback has the
    source-history form

    .. math::
       Bv(t)-C_0^\eta v(t-\theta_0)
             -C_1^\eta v(t-\theta_1),

    where ``C_0^eta+C_1^eta=B``.  Thus it vanishes on every constant
    history.  At ``eta=0`` both delay layers preserve ``r``.  At nonzero
    ``eta`` their opposite transverse forcings cancel in total gain and in
    the critical projection, but not as delay measures.
    """

    eta, theta_0, theta_1 = sp.symbols(
        "eta theta_0 theta_1", real=True
    )
    sigma = sp.sqrt(sp.Rational(3, 2))
    equilibrium_v = sp.Matrix([sigma, 0])
    equilibrium_w = sp.Matrix([0, 2 * sigma])

    v_1, v_2, w_1, w_2 = sp.symbols("v_1 v_2 w_1 w_2")
    fast_field = sp.Matrix(
        [
            v_1 - v_1**3 / 3 - w_1 + (v_2 - v_1) / 2,
            v_2 - v_2**3 / 3 - w_2 + 2 * (v_1 - v_2),
        ]
    )
    fast_jacobian = sp.simplify(
        fast_field.jacobian((v_1, v_2)).subs(
            {v_1: equilibrium_v[0], v_2: equilibrium_v[1]}
        )
    )

    critical_right = sp.Matrix([1, 2])
    critical_left = sp.Matrix([sp.Rational(1, 2), sp.Rational(1, 4)])
    critical_projector = critical_right * critical_left.T
    transverse_projector = sp.eye(2) - critical_projector

    total_gain = sp.Matrix(
        [
            [sp.Rational(1, 2), sp.Rational(1, 4)],
            [sp.Rational(2, 3), sp.Rational(2, 3)],
        ]
    )
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
    perturbed_layer_0 = layer_0 + eta * redistribution
    perturbed_layer_1 = layer_1 - eta * redistribution
    transverse_vector = redistribution * critical_right

    fast_kernel_residual = sp.simplify(
        fast_jacobian * critical_right
    )
    adjoint_kernel_residual = sp.simplify(
        critical_left.T * fast_jacobian
    )

    hessians = [
        sp.hessian(component, (v_1, v_2)).subs(
            {v_1: equilibrium_v[0], v_2: equilibrium_v[1]}
        )
        for component in fast_field
    ]
    quadratic_vector = sp.Matrix(
        [
            (critical_right.T * hessian * critical_right)[0]
            for hessian in hessians
        ]
    )
    fold_nondegeneracy = sp.simplify(
        (critical_left.T * quadratic_vector)[0]
    )

    total_gain_residual = sp.simplify(
        perturbed_layer_0 + perturbed_layer_1 - total_gain
    )
    layer_0_mode_residual = sp.simplify(
        perturbed_layer_0 * critical_right
        - sp.Rational(1, 3) * critical_right
        - eta * transverse_vector
    )
    layer_1_mode_residual = sp.simplify(
        perturbed_layer_1 * critical_right
        - sp.Rational(2, 3) * critical_right
        + eta * transverse_vector
    )
    projected_layer_0_weight = sp.simplify(
        (critical_left.T * perturbed_layer_0 * critical_right)[0]
    )
    projected_layer_1_weight = sp.simplify(
        (critical_left.T * perturbed_layer_1 * critical_right)[0]
    )

    first_moment_vector = sp.simplify(
        theta_0 * perturbed_layer_0 * critical_right
        + theta_1 * perturbed_layer_1 * critical_right
    )
    projected_first_moment = sp.simplify(
        (critical_left.T * first_moment_vector)[0]
    )
    transverse_first_moment = sp.simplify(
        transverse_projector * first_moment_vector
    )

    # The transverse restriction of A_0 is -2, so this is A_perp^{-1} q.
    transverse_fast_response = -transverse_vector / 2
    mixed_quadratic_vector = sp.Matrix(
        [
            (
                critical_right.T
                * hessian
                * transverse_fast_response
            )[0]
            for hessian in hessians
        ]
    )
    nonlinear_return_coefficient = sp.simplify(
        (critical_left.T * mixed_quadratic_vector)[0]
    )

    return TwoModuleMomentAudit(
        sigma=sigma,
        equilibrium_v=equilibrium_v,
        equilibrium_w=equilibrium_w,
        fast_jacobian=fast_jacobian,
        critical_right=critical_right,
        critical_left=critical_left,
        critical_projector=critical_projector,
        transverse_projector=transverse_projector,
        transverse_vector=transverse_vector,
        total_gain=total_gain,
        layer_0=layer_0,
        layer_1=layer_1,
        redistribution=redistribution,
        perturbed_layer_0=perturbed_layer_0,
        perturbed_layer_1=perturbed_layer_1,
        fast_kernel_residual=fast_kernel_residual,
        adjoint_kernel_residual=adjoint_kernel_residual,
        fold_nondegeneracy=fold_nondegeneracy,
        total_gain_residual=total_gain_residual,
        layer_0_mode_residual=layer_0_mode_residual,
        layer_1_mode_residual=layer_1_mode_residual,
        projected_layer_0_weight=projected_layer_0_weight,
        projected_layer_1_weight=projected_layer_1_weight,
        first_moment_vector=first_moment_vector,
        projected_first_moment=projected_first_moment,
        transverse_first_moment=transverse_first_moment,
        transverse_fast_response=transverse_fast_response,
        nonlinear_return_coefficient=nonlinear_return_coefficient,
    )


if __name__ == "__main__":
    result = two_module_moment_audit()
    print("A_0 =", result.fast_jacobian)
    print("fold coefficient =", result.fold_nondegeneracy)
    print("projected M_1 =", result.projected_first_moment)
    print("transverse M_1 =", result.transverse_first_moment)
    print("nonlinear return =", result.nonlinear_return_coefficient)
