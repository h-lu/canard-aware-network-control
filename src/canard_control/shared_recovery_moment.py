"""Formal inner calculation for the shared-recovery two-module example.

The exact parts of this module audit the center dimension of three recovery
architectures, the modal change of coordinates, and elementary adjoint
identities.  The calculated threshold coefficient belongs to a canonical
whole-line or fixed finite-section *formal inner problem*.  It is not an RFDE
Fredholm theorem and does not include the true slow-manifold endpoint maps,
history-jump multipliers, or a uniform remainder.
"""

from __future__ import annotations

from dataclasses import dataclass

import sympy as sp


@dataclass(frozen=True)
class SharedRecoveryInnerResult:
    """Exact modal data and the formal shared-recovery inner coefficient."""

    sigma: sp.Expr
    canonical_scale: sp.Expr
    critical_right: sp.Matrix
    critical_left: sp.Matrix
    transverse_right: sp.Matrix
    transverse_left: sp.Matrix
    fast_jacobian: sp.Matrix
    unrepaired_singular_matrix: sp.Matrix
    shared_recovery_singular_matrix: sp.Matrix
    recovery_scaffold_singular_matrix: sp.Matrix
    unrepaired_characteristic: sp.Expr
    shared_recovery_characteristic: sp.Expr
    recovery_scaffold_characteristic: sp.Expr
    unrepaired_kernel_dimension: int
    shared_recovery_kernel_dimension: int
    recovery_scaffold_kernel_dimension: int
    scaffold_transverse_matrix: sp.Matrix
    scaffold_transverse_response: sp.Matrix
    canonical_critical_quadratic: sp.Expr
    canonical_transverse_quadratic: sp.Expr
    leading_matrix: sp.Matrix
    tangent_kernel: sp.Matrix
    adjoint_kernel: sp.Matrix
    kernel_residual: sp.Matrix
    adjoint_residual: sp.Matrix
    leading_canard: sp.Expr
    delay_translation_difference: sp.Expr
    fiber_transverse_response: sp.Expr
    fiber_range_residual: sp.Expr
    zero_incoming_transverse_response: sp.Expr
    zero_incoming_range_residual: sp.Expr
    zero_incoming_boundary_residual: sp.Expr
    second_order_transverse_coefficient: sp.Expr
    critical_return_force: sp.Expr
    whole_line_numerator: sp.Expr
    parameter_denominator: sp.Expr
    whole_line_root_coefficient: sp.Expr
    whole_line_transverse_functional: sp.Expr


@dataclass(frozen=True)
class FiniteSectionAdjointResult:
    """Formal adjoint pairing on the symmetric section ``[-L,L]``."""

    tangent_kernel: sp.Matrix
    adjoint_kernel: sp.Matrix
    left_endpoint_multiplier: sp.Expr
    right_endpoint_multiplier: sp.Expr
    left_endpoint_annihilation: sp.Matrix
    right_endpoint_annihilation: sp.Matrix
    phase_multiplier: sp.Expr
    parameter_pairing: sp.Expr
    quadratic_pairing: sp.Expr
    interior_numerator: sp.Expr
    boundary_pairing: sp.Expr
    total_numerator: sp.Expr
    formal_root_coefficient: sp.Expr
    interior_root_coefficient: sp.Expr
    interior_transverse_functional: sp.Expr
    whole_line_limit: sp.Expr


def _truncate_total_degree(
    expression: sp.Expr,
    variables: tuple[sp.Symbol, ...],
    degree: int,
) -> sp.Expr:
    """Return the polynomial terms of total degree at most ``degree``."""

    polynomial = sp.Poly(sp.expand(expression), *variables)
    retained = sp.Integer(0)
    for powers, coefficient in polynomial.terms():
        if sum(powers) <= degree:
            monomial = sp.prod(
                variable**power
                for variable, power in zip(variables, powers, strict=True)
            )
            retained += coefficient * monomial
    return sp.expand(retained)


def shared_recovery_inner() -> SharedRecoveryInnerResult:
    r"""Derive the shared-recovery formal transverse contribution.

    The two-module fast core has critical and transverse modes

    .. math::
       r=(1,2)^T,\qquad q=(1,-2)^T,

    with transverse eigenvalue ``-2``.  Replacing the two independent slow
    recovery variables by one shared recovery produces a two-dimensional
    generalized center with a one-dimensional kernel: the critical voltage
    and its recovery generalized direction.  Equivalently, an ``O(1)``
    recovery scaffold leaves the same center and makes the other recovery
    mode hyperbolic.

    In canonical modal coordinates, the quadratic fast fields are

    .. math::
       \dot x=y-(x+z)^2,\qquad
       \dot z=-2z-(x+z)^2.

    For the delay-layer redistribution in ``two_module_moment.py``, the
    transverse equation receives

    .. math::
       -\varepsilon K\eta
       [x(t-\theta_0/\delta)-x(t-\theta_1/\delta)].

    The returned coefficient is a formal inner solvability coefficient.  A
    true RFDE result still requires the dynamic advanced adjoint, derived
    endpoint bundles, complete-history jump, and a uniform remainder.
    """

    delta = sp.Symbol("delta", positive=True)
    eta, K = sp.symbols("eta K", real=True)
    theta_0, theta_1, s = sp.symbols(
        "theta_0 theta_1 s", real=True
    )
    spectral_parameter = sp.Symbol("lambda")
    recovery_gap = sp.Symbol("D_w", positive=True)
    section_length = sp.Symbol("L", positive=True)

    sigma = sp.sqrt(sp.Rational(3, 2))
    canonical_scale = sigma / 2
    critical_right = sp.Matrix([1, 2])
    critical_left = sp.Matrix(
        [sp.Rational(1, 2), sp.Rational(1, 4)]
    )
    transverse_right = sp.Matrix([1, -2])
    transverse_left = sp.Matrix(
        [sp.Rational(1, 2), -sp.Rational(1, 4)]
    )
    critical_projector = critical_right * critical_left.T
    transverse_projector = sp.eye(2) - critical_projector
    fast_jacobian = -2 * transverse_projector

    # With two independent recoveries, the zero eigenvalue has algebraic
    # multiplicity three and geometric multiplicity two.  A scalar canard
    # root is therefore not intrinsic without an additional fiber selection.
    unrepaired_singular_matrix = fast_jacobian.row_join(
        -sp.eye(2)
    ).col_join(sp.zeros(2, 4))

    # A shared recovery W enters the fast field as -r*W.  Its singular
    # matrix has one zero Jordan chain and one transverse stable eigenvalue.
    shared_recovery_singular_matrix = fast_jacobian.row_join(
        -critical_right
    ).col_join(sp.zeros(1, 3))

    # An O(1) recovery scaffold leaves the collective recovery line fixed and
    # damps the transverse recovery by D_w.
    recovery_scaffold_singular_matrix = fast_jacobian.row_join(
        -sp.eye(2)
    ).col_join(
        sp.zeros(2, 2).row_join(-recovery_gap * transverse_projector)
    )

    unrepaired_characteristic = sp.factor(
        (
            spectral_parameter * sp.eye(4)
            - unrepaired_singular_matrix
        ).det()
    )
    shared_recovery_characteristic = sp.factor(
        (
            spectral_parameter * sp.eye(3)
            - shared_recovery_singular_matrix
        ).det()
    )
    recovery_scaffold_characteristic = sp.factor(
        (
            spectral_parameter * sp.eye(4)
            - recovery_scaffold_singular_matrix
        ).det()
    )

    scaffold_transverse_matrix = sp.Matrix(
        [[-2, -1], [0, -recovery_gap]]
    )
    scaffold_transverse_response = sp.simplify(
        scaffold_transverse_matrix.inv() * sp.Matrix([1, 0])
    )

    # Verify the canonical quadratic modal equations directly from a shared
    # recovery FHN realization.  A constant input -2*sigma in the second
    # module makes (v_1,v_2,W)=(sigma,0,0) an equilibrium.
    x, z, y = sp.symbols("x z y")
    xi = x / canonical_scale
    zeta = z / canonical_scale
    v_1 = sigma + xi + zeta
    v_2 = 2 * xi - 2 * zeta
    shared_recovery = -y / canonical_scale
    fast_field = sp.Matrix(
        [
            v_1
            - v_1**3 / 3
            - shared_recovery
            + (v_2 - v_1) / 2,
            v_2
            - v_2**3 / 3
            - 2 * shared_recovery
            + 2 * (v_1 - v_2)
            - 2 * sigma,
        ]
    )
    canonical_critical_field = sp.simplify(
        canonical_scale * (critical_left.T * fast_field)[0]
    )
    canonical_transverse_field = sp.simplify(
        canonical_scale * (transverse_left.T * fast_field)[0]
    )
    canonical_critical_quadratic = _truncate_total_degree(
        canonical_critical_field, (x, z, y), 2
    )
    canonical_transverse_quadratic = _truncate_total_degree(
        canonical_transverse_field, (x, z, y), 2
    )

    leading_matrix = sp.Matrix([[s, 1], [-1, 0]])
    tangent_kernel = sp.Matrix([-1, s])
    gaussian = sp.exp(-s**2 / 2)
    adjoint_kernel = gaussian * sp.Matrix([s, 1])
    kernel_residual = sp.simplify(
        tangent_kernel.diff(s) - leading_matrix * tangent_kernel
    )
    adjoint_residual = sp.simplify(
        -adjoint_kernel.diff(s) - leading_matrix.T * adjoint_kernel
    )

    leading_canard = -s / 2
    delayed_0 = leading_canard.subs(s, s - theta_0)
    delayed_1 = leading_canard.subs(s, s - theta_1)
    delay_translation_difference = sp.simplify(delayed_0 - delayed_1)

    # In z=delta^2*Z coordinates, the eta-dependent range equation is
    # delta Z_eta' + 2 Z_eta = -delta*K*eta*(X_theta0-X_theta1).
    # The unique bounded whole-line solution of this frozen inner equation is
    # constant on the affine leading canard.  It is only a candidate fiber
    # response until the RFDE invariant fibers are constructed.  A zero
    # incoming value produces an entry layer.
    fiber_transverse_response = sp.simplify(
        -delta * K * eta * delay_translation_difference / 2
    )
    fiber_range_residual = sp.simplify(
        delta * sp.diff(fiber_transverse_response, s)
        + 2 * fiber_transverse_response
        + delta * K * eta * delay_translation_difference
    )
    zero_incoming_transverse_response = sp.simplify(
        fiber_transverse_response
        * (1 - sp.exp(-2 * (s + section_length) / delta))
    )
    zero_incoming_range_residual = sp.simplify(
        delta * sp.diff(zero_incoming_transverse_response, s)
        + 2 * zero_incoming_transverse_response
        + delta * K * eta * delay_translation_difference
    )
    zero_incoming_boundary_residual = sp.simplify(
        zero_incoming_transverse_response.subs(s, -section_length)
    )

    second_order_transverse_coefficient = sp.simplify(
        fiber_transverse_response / delta
    )
    critical_return_force = sp.simplify(
        -2 * leading_canard * second_order_transverse_coefficient
    )

    whole_line_numerator = sp.simplify(
        sp.integrate(
            adjoint_kernel[0] * critical_return_force,
            (s, -sp.oo, sp.oo),
        )
    )
    parameter_denominator = sp.simplify(
        sp.integrate(adjoint_kernel[1], (s, -sp.oo, sp.oo))
    )
    # For L_0 u=(f_eta, nu_1), Fredholm solvability gives
    # <psi_1,f_eta> + nu_1 <psi_2,1> = 0.
    whole_line_root_coefficient = sp.simplify(
        -whole_line_numerator / parameter_denominator
    )
    whole_line_transverse_functional = sp.simplify(
        whole_line_root_coefficient / K
    )

    return SharedRecoveryInnerResult(
        sigma=sigma,
        canonical_scale=canonical_scale,
        critical_right=critical_right,
        critical_left=critical_left,
        transverse_right=transverse_right,
        transverse_left=transverse_left,
        fast_jacobian=fast_jacobian,
        unrepaired_singular_matrix=unrepaired_singular_matrix,
        shared_recovery_singular_matrix=shared_recovery_singular_matrix,
        recovery_scaffold_singular_matrix=recovery_scaffold_singular_matrix,
        unrepaired_characteristic=unrepaired_characteristic,
        shared_recovery_characteristic=shared_recovery_characteristic,
        recovery_scaffold_characteristic=recovery_scaffold_characteristic,
        unrepaired_kernel_dimension=len(
            unrepaired_singular_matrix.nullspace()
        ),
        shared_recovery_kernel_dimension=len(
            shared_recovery_singular_matrix.nullspace()
        ),
        recovery_scaffold_kernel_dimension=len(
            recovery_scaffold_singular_matrix.nullspace()
        ),
        scaffold_transverse_matrix=scaffold_transverse_matrix,
        scaffold_transverse_response=scaffold_transverse_response,
        canonical_critical_quadratic=canonical_critical_quadratic,
        canonical_transverse_quadratic=canonical_transverse_quadratic,
        leading_matrix=leading_matrix,
        tangent_kernel=tangent_kernel,
        adjoint_kernel=adjoint_kernel,
        kernel_residual=kernel_residual,
        adjoint_residual=adjoint_residual,
        leading_canard=leading_canard,
        delay_translation_difference=delay_translation_difference,
        fiber_transverse_response=fiber_transverse_response,
        fiber_range_residual=fiber_range_residual,
        zero_incoming_transverse_response=zero_incoming_transverse_response,
        zero_incoming_range_residual=zero_incoming_range_residual,
        zero_incoming_boundary_residual=zero_incoming_boundary_residual,
        second_order_transverse_coefficient=(
            second_order_transverse_coefficient
        ),
        critical_return_force=critical_return_force,
        whole_line_numerator=whole_line_numerator,
        parameter_denominator=parameter_denominator,
        whole_line_root_coefficient=whole_line_root_coefficient,
        whole_line_transverse_functional=(
            whole_line_transverse_functional
        ),
    )


def finite_section_adjoint() -> FiniteSectionAdjointResult:
    r"""Return the formal adjoint coefficient on ``[-L,L]``.

    The leading critical operator is

    .. math::
       L_0(U,V)=(U'-sU-V,\;V'+U).

    Use the tangent-compatible endpoint lines

    .. math::
       V(-L)-LU(-L)=0,\qquad V(L)+LU(L)=0,

    and the phase condition ``U(0)=0``.  The dynamic adjoint is
    ``exp(-s^2/2)*(s,1)``.  Its endpoint multipliers are respectively
    ``exp(-L^2/2)`` and ``-exp(-L^2/2)``; the phase multiplier is zero.

    The returned coefficient includes symbolic direct endpoint residuals
    ``beta_minus`` and ``beta_plus``.  They vanish for the frozen endpoint
    lines used here, but the true RFDE entry/exit bundles may have nonzero
    structural derivatives.
    """

    s = sp.Symbol("s", real=True)
    L = sp.Symbol("L", positive=True)
    K, eta, delta_theta = sp.symbols(
        "K eta DeltaTheta", real=True
    )
    beta_minus, beta_plus = sp.symbols(
        "beta_minus beta_plus", real=True
    )

    tangent_kernel = sp.Matrix([-1, s])
    gaussian = sp.exp(-s**2 / 2)
    adjoint_kernel = gaussian * sp.Matrix([s, 1])
    endpoint_weight = sp.exp(-L**2 / 2)
    left_endpoint_multiplier = endpoint_weight
    right_endpoint_multiplier = -endpoint_weight

    left_boundary_covector = sp.Matrix([-L, 1])
    right_boundary_covector = sp.Matrix([L, 1])
    left_endpoint_annihilation = sp.simplify(
        -adjoint_kernel.subs(s, -L)
        + left_endpoint_multiplier * left_boundary_covector
    )
    right_endpoint_annihilation = sp.simplify(
        adjoint_kernel.subs(s, L)
        + right_endpoint_multiplier * right_boundary_covector
    )

    parameter_pairing = sp.simplify(
        sp.integrate(gaussian, (s, -L, L))
    )
    quadratic_pairing = sp.simplify(
        sp.integrate(s**2 * gaussian, (s, -L, L))
    )
    critical_return_force = -K * eta * delta_theta * s / 4
    interior_numerator = sp.simplify(
        sp.integrate(
            adjoint_kernel[0] * critical_return_force,
            (s, -L, L),
        )
    )
    boundary_pairing = sp.simplify(
        endpoint_weight * beta_minus - endpoint_weight * beta_plus
    )
    total_numerator = sp.simplify(
        interior_numerator + boundary_pairing
    )
    formal_root_coefficient = sp.simplify(
        -total_numerator / parameter_pairing
    )
    interior_root_coefficient = sp.simplify(
        -interior_numerator / parameter_pairing
    )
    interior_transverse_functional = sp.simplify(
        interior_root_coefficient / K
    )
    whole_line_limit = sp.simplify(
        sp.limit(interior_transverse_functional, L, sp.oo)
    )

    return FiniteSectionAdjointResult(
        tangent_kernel=tangent_kernel,
        adjoint_kernel=adjoint_kernel,
        left_endpoint_multiplier=left_endpoint_multiplier,
        right_endpoint_multiplier=right_endpoint_multiplier,
        left_endpoint_annihilation=left_endpoint_annihilation,
        right_endpoint_annihilation=right_endpoint_annihilation,
        phase_multiplier=sp.Integer(0),
        parameter_pairing=parameter_pairing,
        quadratic_pairing=quadratic_pairing,
        interior_numerator=interior_numerator,
        boundary_pairing=boundary_pairing,
        total_numerator=total_numerator,
        formal_root_coefficient=formal_root_coefficient,
        interior_root_coefficient=interior_root_coefficient,
        interior_transverse_functional=interior_transverse_functional,
        whole_line_limit=whole_line_limit,
    )


if __name__ == "__main__":
    inner = shared_recovery_inner()
    section = finite_section_adjoint()
    print("unrepaired characteristic =", inner.unrepaired_characteristic)
    print("shared characteristic =", inner.shared_recovery_characteristic)
    print("formal whole-line J_perp =", inner.whole_line_transverse_functional)
    print("formal finite-section J_perp =", section.interior_transverse_functional)
