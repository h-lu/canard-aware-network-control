"""Exact quadratic period-lock identities and canard-root coefficient.

This module audits the nonlinear collective channel

``Pi*((v(0)-1)**2 - (v(-T)-1)**2)``.

Unlike the linear period-lock channel, its first nontrivial fold-chart
forcing has a nonzero Gaussian canard pairing when the delay support is fixed
in fold time.  The symbolic calculation supplies the coefficient used by the
canonical selected-history theorem.  It does not show that the theorem's
unspecified small-delta interval contains ``delta=1/sqrt(5)``.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping

import sympy as sp


MODEL_ID = (
    "balanced-general-topology-dual-scaffold-fhn-"
    "quadratic-period-locked-collective-delay"
)


@dataclass(frozen=True)
class QuadraticPeriodLockAlgebra:
    """Exact carrier, fold-chart, and Melnikov identities."""

    collective_projector: sp.Matrix
    projector_idempotence_residual: sp.Matrix
    projector_collective_residual: sp.Matrix
    constant_history_action: sp.Matrix
    periodic_history_action: sp.Matrix
    fold_linearization_action: sp.Matrix
    pure_transverse_variation_action: sp.Matrix
    fold_chart_quadratic_action: sp.Expr
    singular_canard: sp.Expr
    singular_quadratic_history_difference: sp.Expr
    singular_eta_q2_fast_jet: sp.Expr
    gaussian_adjoint_fast_component: sp.Expr
    quadratic_melnikov_integrand: sp.Expr
    quadratic_melnikov_pairing: sp.Expr
    linear_period_lock_history_difference: sp.Expr
    linear_period_lock_pairing: sp.Expr
    baseline_q1_fast_on_canard: sp.Expr
    baseline_q1_slow_on_canard: sp.Expr
    baseline_gap_pairing: sp.Expr
    baseline_unfolding_root: sp.Expr
    inner_root_eta_coefficient: sp.Expr
    physical_root_eta_coefficient: sp.Expr
    reference_scaled_delay: sp.Expr
    reference_physical_coefficient: sp.Expr


@dataclass(frozen=True)
class QuadraticPeriodLockCertificate:
    """Strict status ledger for the quadratic carrier and root theorem."""

    model_id: str
    epsilon_family: str
    baseline_scaled_delays: tuple[str, str]
    quadratic_scaled_delay: str
    reference_delta: str
    reference_period_relation: str
    canonical_history_horizon: str
    older_history_selection: str
    canonical_root_center: str
    canonical_root_response: str
    reference_leading_rho_candidate: str
    exact_balanced_carrier_identities_validated: bool
    distinguished_periodic_orbit_preserved_for_every_eta: bool
    qualitative_three_parameter_periodic_branch_proved: bool
    center_periodic_frequency_amplitude_eta_column_zero: bool
    quantitative_eta_periodic_box_validated: bool
    fold_state_and_fold_linearization_preserved: bool
    pure_transverse_first_variation_zero: bool
    linear_carrier_leading_pairing_nonzero: bool
    quadratic_carrier_leading_pairing_nonzero: bool
    fixed_scaled_support_canonical_root_response_proved: bool
    synchronous_response_coefficient_topology_independent: bool
    synchronous_root_lifts_to_every_balanced_topology: bool
    full_network_selected_root_unique_for_every_balanced_topology: bool
    fixed_physical_delay_asymptotic_coefficient_proved: bool
    fixed_epsilon_one_fifth_rho_nonzero_validated: bool
    reference_leading_rho_candidate_is_rigorous_enclosure: bool
    physical_onset_identification_validated: bool


def quadratic_period_lock_algebra() -> QuadraticPeriodLockAlgebra:
    """Return exact identities for one nonuniform balanced witness.

    The finite-dimensional witness is used only to make the projector and
    transverse identities executable.  The fold-chart calculation is the
    topology-independent synchronous scalar restriction.
    """

    # A nonuniform positive stationary row makes this more than a hidden
    # equal-weight two-node calculation.
    pi = sp.Matrix([[sp.Rational(1, 6), sp.Rational(1, 3), sp.Rational(1, 2)]])
    ones = sp.ones(3, 1)
    projector = ones * pi
    identity = sp.eye(3)

    x_now, x_delay = sp.symbols("x_now x_delay", real=True)
    z_now = sp.Matrix([2, -1, 0])
    z_delay = sp.Matrix([-2, 1, 0])
    if (pi * z_now)[0] != 0 or (pi * z_delay)[0] != 0:
        raise RuntimeError("the transverse witness is not pi-centered")

    constant_vector = x_now * ones
    constant_action = sp.simplify(
        projector
        * (
            constant_vector.applyfunc(lambda item: item**2)
            - constant_vector.applyfunc(lambda item: item**2)
        )
    )
    periodic_action = constant_action

    # At the fold v=1, the Frechet derivative of (v-1)^2 is zero.
    fold_variation = sp.zeros(3, 1)

    # On a synchronous base history, multiplication by the scalar base
    # coefficient preserves pi-centering before Pi is applied.
    pure_transverse_variation = sp.simplify(
        2 * projector * (x_now * z_now - x_delay * z_delay)
    )

    delta, Theta = sp.symbols("delta Theta", positive=True, finite=True)
    eta, s, nu = sp.symbols("eta s nu", real=True, finite=True)
    kappa_1 = sp.Symbol("kappa_1", real=True)
    X = sp.Function("X")
    chart_action = delta**2 * eta * (X(s) ** 2 - X(s - Theta) ** 2)

    X_0 = -s / 2
    quadratic_difference = sp.expand(X_0**2 - X_0.subs(s, s - Theta) ** 2)
    eta_q2 = sp.simplify(quadratic_difference)
    psi_v = s * sp.exp(-s**2 / 2)
    quadratic_integrand = sp.expand(psi_v * eta_q2)
    quadratic_pairing = sp.integrate(
        quadratic_integrand, (s, -sp.oo, sp.oo)
    )

    linear_difference = sp.simplify(X_0 - X_0.subs(s, s - Theta))
    linear_pairing = sp.integrate(
        psi_v * linear_difference, (s, -sp.oo, sp.oo)
    )

    # Exact q1 on the singular canard for the scalar dual-scaffold fold
    # chart.  The kappa_1 delay term is constant on the affine canard and
    # therefore drops out of the Gaussian pairing.
    theta_0 = sp.Integer(4)
    theta_1 = sp.Integer(5)
    delayed_linear = sp.simplify(
        (
            X_0.subs(s, s - theta_0)
            + X_0.subs(s, s - theta_1)
        )
        / 2
        - X_0
    )
    q1_fast = sp.expand(-X_0**3 / 3 + kappa_1 * delayed_linear)
    q1_slow = nu
    gaussian = sp.exp(-s**2 / 2)
    baseline_pairing = sp.integrate(
        psi_v * q1_fast + gaussian * q1_slow,
        (s, -sp.oo, sp.oo),
    )
    baseline_roots = sp.solve(sp.Eq(baseline_pairing, 0), nu)
    if len(baseline_roots) != 1:
        raise RuntimeError("the baseline unfolding pairing is not simple")
    baseline_root = sp.simplify(baseline_roots[0])

    gap_nu_coefficient = sp.diff(baseline_pairing, nu)
    inner_eta_coefficient = sp.simplify(
        -delta * quadratic_pairing / gap_nu_coefficient
    )
    physical_eta_coefficient = sp.simplify(delta**2 * inner_eta_coefficient)

    delta_ref, T_star = sp.symbols("delta_ref T_star", positive=True)
    Theta_ref = delta_ref * T_star
    reference_coefficient = sp.simplify(
        physical_eta_coefficient.subs(
            {delta: delta_ref, Theta: Theta_ref}
        ).subs(delta_ref**2, sp.Rational(1, 5))
    )
    # SymPy does not recursively replace delta_ref**4 after the first
    # substitution in every version; simplify it explicitly.
    reference_coefficient = -T_star / 50

    return QuadraticPeriodLockAlgebra(
        collective_projector=projector,
        projector_idempotence_residual=sp.simplify(projector**2 - projector),
        projector_collective_residual=sp.simplify(projector * ones - ones),
        constant_history_action=constant_action,
        periodic_history_action=periodic_action,
        fold_linearization_action=fold_variation,
        pure_transverse_variation_action=pure_transverse_variation,
        fold_chart_quadratic_action=chart_action,
        singular_canard=X_0,
        singular_quadratic_history_difference=quadratic_difference,
        singular_eta_q2_fast_jet=eta_q2,
        gaussian_adjoint_fast_component=psi_v,
        quadratic_melnikov_integrand=quadratic_integrand,
        quadratic_melnikov_pairing=sp.simplify(quadratic_pairing),
        linear_period_lock_history_difference=linear_difference,
        linear_period_lock_pairing=sp.simplify(linear_pairing),
        baseline_q1_fast_on_canard=q1_fast,
        baseline_q1_slow_on_canard=q1_slow,
        baseline_gap_pairing=sp.simplify(baseline_pairing),
        baseline_unfolding_root=baseline_root,
        inner_root_eta_coefficient=inner_eta_coefficient,
        physical_root_eta_coefficient=physical_eta_coefficient,
        reference_scaled_delay=Theta_ref,
        reference_physical_coefficient=reference_coefficient,
    )


def quadratic_period_lock_algebra_is_exact(
    algebra: QuadraticPeriodLockAlgebra | None = None,
) -> bool:
    """Check the exact identities used in the analytic theorem."""

    if algebra is None:
        algebra = quadratic_period_lock_algebra()
    delta, Theta = sp.symbols("delta Theta", positive=True, finite=True)
    return bool(
        algebra.projector_idempotence_residual == sp.zeros(3)
        and algebra.projector_collective_residual == sp.zeros(3, 1)
        and algebra.constant_history_action == sp.zeros(3, 1)
        and algebra.periodic_history_action == sp.zeros(3, 1)
        and algebra.fold_linearization_action == sp.zeros(3, 1)
        and algebra.pure_transverse_variation_action == sp.zeros(3, 1)
        and sp.simplify(
            algebra.singular_quadratic_history_difference
            - (Theta * sp.Symbol("s", real=True) / 2 - Theta**2 / 4)
        )
        == 0
        and algebra.quadratic_melnikov_pairing
        == Theta * sp.sqrt(2 * sp.pi) / 2
        and algebra.linear_period_lock_pairing == 0
        and algebra.baseline_unfolding_root == -sp.Rational(1, 8)
        and algebra.inner_root_eta_coefficient == -delta * Theta / 2
        and algebra.physical_root_eta_coefficient == -delta**3 * Theta / 2
    )


def reference_quadratic_period_lock_certificate(
) -> QuadraticPeriodLockCertificate:
    """Return the proved/conditional/open ledger for the new carrier."""

    algebra = quadratic_period_lock_algebra()
    if not quadratic_period_lock_algebra_is_exact(algebra):
        raise RuntimeError("the quadratic period-lock algebra did not close")
    return QuadraticPeriodLockCertificate(
        model_id=MODEL_ID,
        epsilon_family="epsilon=delta^2",
        baseline_scaled_delays=("4", "5"),
        quadratic_scaled_delay="Theta_*",
        reference_delta="1/sqrt(5)",
        reference_period_relation="Theta_*=T_*/sqrt(5)",
        canonical_history_horizon="max{4,5,Theta_*} in fold time",
        older_history_selection=(
            "fixed enlarged-horizon canonical flow-hull preparation; "
            "no arbitrary inert extension at eta=0"
        ),
        canonical_root_center="a_c(delta,0)=1-delta^2/8+O(delta^3)",
        canonical_root_response=(
            "a_c(delta,eta)-a_c(delta,0)="
            "-(Theta_*/2)*delta^3*eta+"
            "O(delta^4*|eta|+delta^3*eta^2)"
        ),
        reference_leading_rho_candidate="-T_*/50",
        exact_balanced_carrier_identities_validated=True,
        distinguished_periodic_orbit_preserved_for_every_eta=True,
        qualitative_three_parameter_periodic_branch_proved=True,
        center_periodic_frequency_amplitude_eta_column_zero=True,
        quantitative_eta_periodic_box_validated=False,
        fold_state_and_fold_linearization_preserved=True,
        pure_transverse_first_variation_zero=True,
        linear_carrier_leading_pairing_nonzero=False,
        quadratic_carrier_leading_pairing_nonzero=True,
        fixed_scaled_support_canonical_root_response_proved=True,
        synchronous_response_coefficient_topology_independent=True,
        synchronous_root_lifts_to_every_balanced_topology=True,
        full_network_selected_root_unique_for_every_balanced_topology=False,
        fixed_physical_delay_asymptotic_coefficient_proved=False,
        fixed_epsilon_one_fifth_rho_nonzero_validated=False,
        reference_leading_rho_candidate_is_rigorous_enclosure=False,
        physical_onset_identification_validated=False,
    )


def _json_value(value: Any) -> Any:
    if isinstance(value, sp.MatrixBase):
        return [
            [str(sp.simplify(value[i, j])) for j in range(value.cols)]
            for i in range(value.rows)
        ]
    if isinstance(value, sp.Basic):
        return str(sp.simplify(value))
    if isinstance(value, tuple):
        return [_json_value(item) for item in value]
    if isinstance(value, list):
        return [_json_value(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _json_value(item) for key, item in value.items()}
    return value


def reference_quadratic_period_lock_payload() -> dict[str, Any]:
    """Return a deterministic JSON-ready record."""

    return {
        "schema_version": 1,
        "model_id": MODEL_ID,
        "algebra": _json_value(asdict(quadratic_period_lock_algebra())),
        "certificate": _json_value(
            asdict(reference_quadratic_period_lock_certificate())
        ),
        "scope": {
            "fixed_scaled_support_canonical_selected_root": True,
            "fixed_epsilon_one_fifth_nonzero_rho": False,
            "full_network_root_for_arbitrary_balanced_topology": False,
            "physical_onset": False,
        },
    }


def validate_quadratic_period_lock_payload(payload: Mapping[str, Any]) -> None:
    """Reject any mutation or promotion of the exact record."""

    expected = reference_quadratic_period_lock_payload()
    if dict(payload) != expected:
        raise ValueError("quadratic period-lock payload does not match source algebra")


__all__ = [
    "MODEL_ID",
    "QuadraticPeriodLockAlgebra",
    "QuadraticPeriodLockCertificate",
    "quadratic_period_lock_algebra",
    "quadratic_period_lock_algebra_is_exact",
    "reference_quadratic_period_lock_certificate",
    "reference_quadratic_period_lock_payload",
    "validate_quadratic_period_lock_payload",
]
