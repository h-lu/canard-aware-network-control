"""Exact algebra and a minimal spectral diagnostic for the final model (M).

The symbolic audit in :func:`final_two_module_audit` concerns finite-
dimensional identities of the frozen two-module FitzHugh--Nagumo RFDE.  The
root utility evaluates the *full* linear RFDE characteristic determinant at
fixed positive ``delta`` and follows one root from a supplied seed.

Neither calculation proves a uniform RFDE spectral gap, constructs an
invariant history manifold, or proves a maximal-canard theorem.  In
particular, :func:`diagnostic_root_branch` is deliberately local: it follows
one characteristic root and does not enclose the infinitely many other RFDE
roots.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Iterable

import mpmath as mp
import sympy as sp


@dataclass(frozen=True)
class FinalTwoModuleAudit:
    """Exact equilibrium, fold, delay-layer, and singular-spectrum data."""

    eta: sp.Symbol
    theta_0: sp.Symbol
    theta_1: sp.Symbol
    history_now: sp.Symbol
    history_0: sp.Symbol
    history_1: sp.Symbol
    sigma: sp.Expr
    equilibrium_v: sp.Matrix
    equilibrium_w: sp.Matrix
    critical_right: sp.Matrix
    critical_left: sp.Matrix
    transverse_right: sp.Matrix
    transverse_left: sp.Matrix
    critical_projector: sp.Matrix
    transverse_projector: sp.Matrix
    fast_equilibrium_residual: sp.Matrix
    recovery_equilibrium_residual: sp.Matrix
    constant_history_feedback_residual: sp.Matrix
    fast_jacobian: sp.Matrix
    right_kernel_residual: sp.Matrix
    fast_adjoint_kernel_residual: sp.Matrix
    fold_curvature: sp.Expr
    slow_line_residual: sp.Matrix
    layer_0: sp.Matrix
    layer_1: sp.Matrix
    redistribution: sp.Matrix
    perturbed_layer_0: sp.Matrix
    perturbed_layer_1: sp.Matrix
    total_gain: sp.Matrix
    total_gain_residual: sp.Matrix
    strict_entrywise_positivity_interval: tuple[sp.Expr, sp.Expr]
    safe_closed_radius: sp.Expr
    safe_closed_interval_minimum_entry: sp.Expr
    projected_layer_weights: tuple[sp.Expr, sp.Expr]
    projected_measure_pairing: sp.Expr
    projected_measure_eta_derivative: sp.Expr
    transverse_measure_pairing: sp.Matrix
    source_history_critical_component: sp.Expr
    source_history_transverse_component: sp.Matrix
    singular_jacobian: sp.Matrix
    singular_characteristic: sp.Expr
    zero_algebraic_multiplicity: int
    kernel_dimension: int
    squared_kernel_dimension: int
    cubed_kernel_dimension: int
    zero_eigenvector: sp.Matrix
    zero_generalized_vector: sp.Matrix
    jordan_chain_residual: sp.Matrix
    left_zero_eigenvector: sp.Matrix
    full_left_kernel_residual: sp.Matrix


def final_two_module_audit() -> FinalTwoModuleAudit:
    r"""Audit the exact algebra of the fixed two-module model ``(M)``.

    The model is

    .. math::
       \dot v=F(v,w)+\varepsilon K
       [Bv-C_0^\eta v(t-\theta_0/\delta)
             -C_1^\eta v(t-\theta_1/\delta)],

    .. math::
       \dot w=\varepsilon(v_1-\sigma-\mu,\,v_2-2\mu)^T
       -D_w P_\perp(w-w_*).

    All returned identities use exact SymPy arithmetic.  Positivity below
    means entrywise positivity; the nonsymmetric layer matrices are not being
    asserted to be positive definite.
    """

    eta = sp.Symbol("eta", real=True)
    theta_0, theta_1 = sp.symbols(
        "theta_0 theta_1", positive=True
    )
    history_now, history_0, history_1 = sp.symbols(
        "x_now x_0 x_1", real=True
    )
    mu, collective_coordinate = sp.symbols("mu X", real=True)
    spectral_parameter = sp.Symbol("z")
    recovery_gap = sp.Symbol("D_w", positive=True)

    sigma = sp.sqrt(sp.Rational(3, 2))
    equilibrium_v = sp.Matrix([sigma, 0])
    equilibrium_w = sp.Matrix([0, 2 * sigma])

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

    v_1, v_2, w_1, w_2 = sp.symbols("v_1 v_2 w_1 w_2")
    fast_field = sp.Matrix(
        [
            v_1 - v_1**3 / 3 - w_1 + (v_2 - v_1) / 2,
            v_2 - v_2**3 / 3 - w_2 + 2 * (v_1 - v_2),
        ]
    )
    equilibrium_substitution = {
        v_1: equilibrium_v[0],
        v_2: equilibrium_v[1],
        w_1: equilibrium_w[0],
        w_2: equilibrium_w[1],
    }
    fast_equilibrium_residual = sp.simplify(
        fast_field.subs(equilibrium_substitution)
    )
    recovery_equilibrium_residual = sp.Matrix(
        [equilibrium_v[0] - sigma, equilibrium_v[1]]
    )

    fast_jacobian = sp.simplify(
        fast_field.jacobian((v_1, v_2)).subs(
            equilibrium_substitution
        )
    )
    right_kernel_residual = sp.simplify(
        fast_jacobian * critical_right
    )
    fast_adjoint_kernel_residual = sp.simplify(
        critical_left.T * fast_jacobian
    )

    hessians = tuple(
        sp.hessian(component, (v_1, v_2)).subs(
            equilibrium_substitution
        )
        for component in fast_field
    )
    quadratic_vector = sp.Matrix(
        [
            (critical_right.T * hessian * critical_right)[0]
            for hessian in hessians
        ]
    )
    fold_curvature = sp.simplify(
        (critical_left.T * quadratic_vector)[0]
    )

    voltage_on_slow_line = (
        equilibrium_v + collective_coordinate * critical_right
    )
    slow_field_on_line = sp.Matrix(
        [
            voltage_on_slow_line[0] - sigma - mu,
            voltage_on_slow_line[1] - 2 * mu,
        ]
    )
    slow_line_residual = sp.simplify(
        slow_field_on_line
        - critical_right * (collective_coordinate - mu)
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
    total_gain = layer_0 + layer_1
    total_gain_residual = sp.simplify(
        perturbed_layer_0 + perturbed_layer_1 - total_gain
    )
    constant_history_feedback_residual = sp.simplify(
        total_gain * equilibrium_v
        - perturbed_layer_0 * equilibrium_v
        - perturbed_layer_1 * equilibrium_v
    )

    # The only eta-dependent entries give eta > -1/6, eta < 1/12,
    # eta < 1/3, and eta > -1/4.  Their intersection is (-1/6, 1/12).
    positivity_interval = (
        -sp.Rational(1, 6),
        sp.Rational(1, 12),
    )
    safe_closed_radius = sp.Rational(1, 20)
    endpoint_entries = []
    for endpoint in (-safe_closed_radius, safe_closed_radius):
        endpoint_entries.extend(
            perturbed_layer_0.subs(eta, endpoint)
        )
        endpoint_entries.extend(
            perturbed_layer_1.subs(eta, endpoint)
        )
    safe_closed_interval_minimum_entry = min(endpoint_entries)

    projected_weight_0 = sp.simplify(
        (critical_left.T * perturbed_layer_0 * critical_right)[0]
    )
    projected_weight_1 = sp.simplify(
        (critical_left.T * perturbed_layer_1 * critical_right)[0]
    )
    projected_measure_pairing = sp.simplify(
        projected_weight_0 * history_0
        + projected_weight_1 * history_1
    )
    projected_measure_eta_derivative = sp.diff(
        projected_measure_pairing, eta
    )
    transverse_measure_pairing = sp.simplify(
        transverse_projector
        * (
            perturbed_layer_0 * critical_right * history_0
            + perturbed_layer_1 * critical_right * history_1
        )
    )

    source_history_feedback = sp.simplify(
        total_gain * critical_right * history_now
        - perturbed_layer_0 * critical_right * history_0
        - perturbed_layer_1 * critical_right * history_1
    )
    source_history_critical_component = sp.simplify(
        (critical_left.T * source_history_feedback)[0]
    )
    source_history_transverse_component = sp.simplify(
        transverse_projector * source_history_feedback
    )

    singular_jacobian = sp.Matrix.vstack(
        sp.Matrix.hstack(fast_jacobian, -sp.eye(2)),
        sp.Matrix.hstack(
            sp.zeros(2, 2),
            -recovery_gap * transverse_projector,
        ),
    )
    singular_characteristic = sp.factor(
        singular_jacobian.charpoly(spectral_parameter).as_expr()
    )
    zero_algebraic_multiplicity = 2
    kernel_dimension = 4 - singular_jacobian.rank()
    squared_kernel_dimension = 4 - (singular_jacobian**2).rank()
    cubed_kernel_dimension = 4 - (singular_jacobian**3).rank()

    zero_eigenvector = sp.Matrix.vstack(
        critical_right, sp.zeros(2, 1)
    )
    zero_generalized_vector = sp.Matrix.vstack(
        sp.zeros(2, 1), -critical_right
    )
    jordan_chain_residual = sp.simplify(
        singular_jacobian * zero_generalized_vector - zero_eigenvector
    )
    left_zero_eigenvector = sp.Matrix.vstack(
        sp.zeros(2, 1), critical_left
    )
    full_left_kernel_residual = sp.simplify(
        singular_jacobian.T * left_zero_eigenvector
    )

    return FinalTwoModuleAudit(
        eta=eta,
        theta_0=theta_0,
        theta_1=theta_1,
        history_now=history_now,
        history_0=history_0,
        history_1=history_1,
        sigma=sigma,
        equilibrium_v=equilibrium_v,
        equilibrium_w=equilibrium_w,
        critical_right=critical_right,
        critical_left=critical_left,
        transverse_right=transverse_right,
        transverse_left=transverse_left,
        critical_projector=critical_projector,
        transverse_projector=transverse_projector,
        fast_equilibrium_residual=fast_equilibrium_residual,
        recovery_equilibrium_residual=recovery_equilibrium_residual,
        constant_history_feedback_residual=(
            constant_history_feedback_residual
        ),
        fast_jacobian=fast_jacobian,
        right_kernel_residual=right_kernel_residual,
        fast_adjoint_kernel_residual=fast_adjoint_kernel_residual,
        fold_curvature=fold_curvature,
        slow_line_residual=slow_line_residual,
        layer_0=layer_0,
        layer_1=layer_1,
        redistribution=redistribution,
        perturbed_layer_0=perturbed_layer_0,
        perturbed_layer_1=perturbed_layer_1,
        total_gain=total_gain,
        total_gain_residual=total_gain_residual,
        strict_entrywise_positivity_interval=positivity_interval,
        safe_closed_radius=safe_closed_radius,
        safe_closed_interval_minimum_entry=(
            safe_closed_interval_minimum_entry
        ),
        projected_layer_weights=(
            projected_weight_0,
            projected_weight_1,
        ),
        projected_measure_pairing=projected_measure_pairing,
        projected_measure_eta_derivative=(
            projected_measure_eta_derivative
        ),
        transverse_measure_pairing=transverse_measure_pairing,
        source_history_critical_component=(
            source_history_critical_component
        ),
        source_history_transverse_component=(
            source_history_transverse_component
        ),
        singular_jacobian=singular_jacobian,
        singular_characteristic=singular_characteristic,
        zero_algebraic_multiplicity=zero_algebraic_multiplicity,
        kernel_dimension=kernel_dimension,
        squared_kernel_dimension=squared_kernel_dimension,
        cubed_kernel_dimension=cubed_kernel_dimension,
        zero_eigenvector=zero_eigenvector,
        zero_generalized_vector=zero_generalized_vector,
        jordan_chain_residual=jordan_chain_residual,
        left_zero_eigenvector=left_zero_eigenvector,
        full_left_kernel_residual=full_left_kernel_residual,
    )


@dataclass(frozen=True)
class CharacteristicParameters:
    """Fixed positive-``delta`` parameters for a local root diagnostic."""

    delta: float = 0.2
    weak_gain: float = 1.0
    recovery_gap: float = 1.0
    theta_0: float = 0.5
    theta_1: float = 1.0
    eta: float = 0.0

    def validate(self) -> None:
        """Reject values outside the fixed-model diagnostic contract."""

        if self.delta <= 0.0:
            raise ValueError("delta must be positive")
        if self.recovery_gap <= 0.0:
            raise ValueError("recovery_gap must be positive")
        if not 0.0 < self.theta_0 < self.theta_1:
            raise ValueError("require 0 < theta_0 < theta_1")
        if not -1.0 / 6.0 < self.eta < 1.0 / 12.0:
            raise ValueError(
                "eta must keep both delay layers entrywise positive"
            )


@dataclass(frozen=True)
class CharacteristicRootPoint:
    """One numerically followed root; not an enclosure of the spectrum."""

    eta: float
    root: complex
    determinant_residual: float


def _numeric_characteristic_determinant(
    value: mp.mpc,
    parameters: CharacteristicParameters,
) -> mp.mpc:
    """Evaluate the 4-by-4 RFDE characteristic determinant with mpmath."""

    parameters.validate()
    delta = mp.mpf(parameters.delta)
    epsilon = delta**2
    weak_gain = mp.mpf(parameters.weak_gain)
    recovery_gap = mp.mpf(parameters.recovery_gap)
    theta_0 = mp.mpf(parameters.theta_0)
    theta_1 = mp.mpf(parameters.theta_1)
    eta = mp.mpf(parameters.eta)

    fast_jacobian = mp.matrix([[-1, mp.mpf("0.5")], [2, -1]])
    transverse_projector = mp.matrix(
        [[mp.mpf("0.5"), mp.mpf("-0.25")], [-1, mp.mpf("0.5")]]
    )
    layer_0 = mp.matrix(
        [
            [mp.mpf(1) / 6 + eta, mp.mpf(1) / 12],
            [mp.mpf(1) / 6 - 2 * eta, mp.mpf(1) / 4],
        ]
    )
    layer_1 = mp.matrix(
        [
            [mp.mpf(1) / 3 - eta, mp.mpf(1) / 6],
            [mp.mpf(1) / 2 + 2 * eta, mp.mpf(5) / 12],
        ]
    )
    total_gain = layer_0 + layer_1
    identity = mp.eye(2)
    delayed_gain = (
        layer_0 * mp.exp(-value * theta_0 / delta)
        + layer_1 * mp.exp(-value * theta_1 / delta)
    )

    voltage_block = (
        value * identity
        - fast_jacobian
        - epsilon * weak_gain * total_gain
        + epsilon * weak_gain * delayed_gain
    )
    recovery_block = (
        value * identity + recovery_gap * transverse_projector
    )
    characteristic_matrix = mp.matrix(4, 4)
    for row in range(2):
        for column in range(2):
            characteristic_matrix[row, column] = voltage_block[
                row, column
            ]
            characteristic_matrix[row, column + 2] = identity[
                row, column
            ]
            characteristic_matrix[row + 2, column] = (
                -epsilon * identity[row, column]
            )
            characteristic_matrix[row + 2, column + 2] = (
                recovery_block[row, column]
            )
    return mp.det(characteristic_matrix)


def characteristic_determinant(
    value: complex,
    parameters: CharacteristicParameters = CharacteristicParameters(),
    *,
    decimal_digits: int = 40,
) -> complex:
    """Return the characteristic determinant at one complex test value.

    This evaluates the full exponential-polynomial determinant of the RFDE
    linearization at ``(v_*, w_*)``.  A small value at one point is not a
    spectral enclosure.
    """

    if decimal_digits < 20:
        raise ValueError("decimal_digits must be at least 20")
    with mp.workdps(decimal_digits):
        evaluated = _numeric_characteristic_determinant(
            mp.mpc(value.real, value.imag), parameters
        )
        return complex(evaluated)


def diagnostic_root_branch(
    eta_values: Iterable[float],
    *,
    initial_root: complex = 0.01 + 0.21j,
    parameters: CharacteristicParameters = CharacteristicParameters(),
    decimal_digits: int = 50,
) -> tuple[CharacteristicRootPoint, ...]:
    """Follow one characteristic root through a supplied sequence of eta.

    The previous root is the next secant seed.  The routine neither searches
    for other roots nor certifies that this branch is rightmost or simple.
    Its role is limited to a reproducible fixed-parameter diagnostic.
    """

    if decimal_digits < 30:
        raise ValueError("decimal_digits must be at least 30")
    values = tuple(float(value) for value in eta_values)
    if not values:
        raise ValueError("eta_values must be nonempty")

    points: list[CharacteristicRootPoint] = []
    with mp.workdps(decimal_digits):
        current = mp.mpc(initial_root.real, initial_root.imag)
        for eta in values:
            current_parameters = replace(parameters, eta=eta)
            current_parameters.validate()
            second_seed = current + mp.mpc("1e-4", "1e-4")
            try:
                current = mp.findroot(
                    lambda value: _numeric_characteristic_determinant(
                        value, current_parameters
                    ),
                    (current, second_seed),
                    solver="secant",
                    tol=mp.power(10, -(decimal_digits - 10)),
                    maxsteps=100,
                    verify=True,
                )
            except (ValueError, ZeroDivisionError) as error:
                raise RuntimeError(
                    f"root continuation failed at eta={eta}"
                ) from error
            residual = abs(
                _numeric_characteristic_determinant(
                    current, current_parameters
                )
            )
            points.append(
                CharacteristicRootPoint(
                    eta=eta,
                    root=complex(current),
                    determinant_residual=float(residual),
                )
            )
    return tuple(points)


if __name__ == "__main__":
    exact = final_two_module_audit()
    print("fold curvature =", exact.fold_curvature)
    print("projected measure =", exact.projected_measure_pairing)
    print("transverse forcing =", exact.transverse_measure_pairing)
    print("singular characteristic =", exact.singular_characteristic)
    for point in diagnostic_root_branch((-0.02, 0.0, 0.02)):
        print(point)
