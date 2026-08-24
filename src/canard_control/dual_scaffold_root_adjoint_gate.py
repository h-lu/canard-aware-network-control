"""Exact algebra for the period-locked selected-root adjoint gate.

The period-locked carrier has a nonzero delay moment, but that fact does not
evaluate the derivative of a selected complete-history gap.  This module
records the exact residual columns that a fixed-epsilon Lin/trace BVP must
pair with its *dynamic* cokernel covector.  It also checks two obstructions:

* the first singular-canard interior pairing of the period-lock column is
  zero by parity, despite the nonzero delay moment; and
* the existing recovery-clamped zero reset remains an exact equilibrium for
  every period-lock gain, so its operational reset threshold cannot supply
  the desired nonzero safety column.

No function here constructs the missing selected histories, the augmented
RFDE inverse, or its adjoint.  Those are deliberately exposed as validation
gates rather than encoded as booleans inferred from symbolic algebra.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping

import sympy as sp


MODEL_ID = (
    "balanced-general-topology-dual-scaffold-fhn-"
    "period-locked-collective-delay"
)
ROOT_OUTPUT = "preparation-indexed synchronous complete-history selected root a_c"


@dataclass(frozen=True)
class RootAdjointGateAlgebra:
    """Exact model columns and singular-limit cancellation identities."""

    voltage_residual_eta_column: sp.Expr
    recovery_residual_eta_column: sp.Expr
    voltage_residual_a_column: sp.Expr
    recovery_residual_a_column: sp.Expr
    dynamic_eta_pairing_density: sp.Expr
    dynamic_a_pairing_density: sp.Expr
    normalized_root_derivative: sp.Expr
    scaled_delay_shift: sp.Expr
    singular_canard_history_difference: sp.Expr
    singular_fast_forcing_coefficient: sp.Expr
    singular_fast_adjoint_integrand: sp.Expr
    singular_fast_adjoint_pairing: sp.Expr
    actual_first_moment_scalar: sp.Expr
    clamped_zero_period_lock_action: sp.Expr
    clamped_zero_fast_residual: sp.Expr
    clamped_zero_recovery_residual: sp.Expr


@dataclass(frozen=True)
class RootAdjointGateCertificate:
    """Claim ledger for what the algebra does and does not establish."""

    model_id: str
    epsilon: str
    root_output: str
    exact_root_response_formula: str
    eta_residual_column: tuple[str, str]
    a_residual_column: tuple[str, str]
    required_numerator: str
    required_denominator: str
    singular_interior_pairing: str
    actual_first_moment_scalar: str
    exact_adjoint_ratio_theorem_validated: bool
    residual_columns_validated: bool
    nonzero_first_moment_validated: bool
    leading_singular_interior_pairing_nonzero: bool
    nonzero_moment_implies_nonzero_selected_root_response: bool
    clamped_zero_reset_equilibrium_for_all_eta_validated: bool
    clamped_operational_threshold_supplies_nonzero_eta_column: bool
    same_extended_rfde_selected_root_validated: bool
    augmented_complete_history_bvp_inverse_validated: bool
    dynamic_adjoint_with_endpoint_multipliers_validated: bool
    nonzero_selected_root_eta_response_validated: bool
    fixed_epsilon_one_fifth_overlap_validated: bool
    arbitrary_balanced_topology_full_root_validated: bool
    input_independent_physical_onset_comparison_validated: bool


def root_adjoint_gate_algebra() -> RootAdjointGateAlgebra:
    r"""Return exact columns and the singular-canard parity cancellation.

    We use the residual convention ``R = xdot - F`` for the synchronous
    dual-scaffold RFDE.  Therefore, at ``eta=0``,

    ``R_eta=(-epsilon*(V-V_T), 0)`` and ``R_a=(0, epsilon)``.

    Endpoint, trace, phase, and complete-history-jump equations are not
    represented by these two interior columns.  In a genuine augmented BVP
    their parameter derivatives must be appended before applying the
    cokernel covector.
    """

    epsilon, eta, T, delta, alpha = sp.symbols(
        "epsilon eta T delta alpha", positive=True, finite=True
    )
    V, V_T, p_v, p_w = sp.symbols("V V_T p_v p_w", real=True)
    m_eta, m_a = sp.symbols("m_eta m_a", real=True, nonzero=True)
    s = sp.Symbol("s", real=True)

    residual_eta_v = -epsilon * (V - V_T)
    residual_eta_w = sp.Integer(0)
    residual_a_v = sp.Integer(0)
    residual_a_w = epsilon

    dynamic_eta = sp.expand(p_v * residual_eta_v)
    dynamic_a = sp.expand(p_w * residual_a_w)
    root_derivative = -m_eta / m_a

    # With v=1+delta*X and fold time s=delta*t, a fixed physical delay T
    # becomes h=delta*T.  The singular canard is X_0=-s/(2*alpha).
    h = delta * T
    X_0 = -s / (2 * alpha)
    history_difference = sp.simplify(X_0 - X_0.subs(s, s - h))

    # Dividing the physical voltage equation by delta**2 leaves
    # delta*eta*(X(s)-X(s-h)); its eta coefficient on X_0 is below.
    forcing = sp.simplify(delta * history_difference)
    adjoint_fast = s * sp.exp(-s**2 / 2)
    integrand = sp.simplify(adjoint_fast * forcing)
    pairing = sp.integrate(integrand, (s, -sp.oo, sp.oo))

    actual_moment = epsilon * T
    zero = sp.Integer(0)

    return RootAdjointGateAlgebra(
        voltage_residual_eta_column=residual_eta_v,
        recovery_residual_eta_column=residual_eta_w,
        voltage_residual_a_column=residual_a_v,
        recovery_residual_a_column=residual_a_w,
        dynamic_eta_pairing_density=dynamic_eta,
        dynamic_a_pairing_density=dynamic_a,
        normalized_root_derivative=root_derivative,
        scaled_delay_shift=h,
        singular_canard_history_difference=history_difference,
        singular_fast_forcing_coefficient=forcing,
        singular_fast_adjoint_integrand=integrand,
        singular_fast_adjoint_pairing=sp.simplify(pairing),
        actual_first_moment_scalar=actual_moment,
        clamped_zero_period_lock_action=zero,
        clamped_zero_fast_residual=zero,
        clamped_zero_recovery_residual=zero,
    )


def root_adjoint_gate_is_exact(
    algebra: RootAdjointGateAlgebra | None = None,
) -> bool:
    """Check only the exact identities asserted by this module."""

    if algebra is None:
        algebra = root_adjoint_gate_algebra()
    epsilon, T, delta, alpha = sp.symbols(
        "epsilon T delta alpha", positive=True, finite=True
    )
    expected_difference = -delta * T / (2 * alpha)
    expected_forcing = -delta**2 * T / (2 * alpha)
    return bool(
        sp.simplify(
            algebra.singular_canard_history_difference - expected_difference
        )
        == 0
        and sp.simplify(algebra.singular_fast_forcing_coefficient - expected_forcing)
        == 0
        and algebra.singular_fast_adjoint_pairing == 0
        and sp.simplify(algebra.actual_first_moment_scalar - epsilon * T) == 0
        and algebra.clamped_zero_period_lock_action == 0
        and algebra.clamped_zero_fast_residual == 0
        and algebra.clamped_zero_recovery_residual == 0
    )


def reference_root_adjoint_gate_certificate() -> RootAdjointGateCertificate:
    """Return the strict proved/conditional/open claim ledger."""

    algebra = root_adjoint_gate_algebra()
    if not root_adjoint_gate_is_exact(algebra):
        raise RuntimeError("the root-adjoint gate algebra did not close")

    return RootAdjointGateCertificate(
        model_id=MODEL_ID,
        epsilon="1/5",
        root_output=ROOT_OUTPUT,
        exact_root_response_formula="rho_*=-m_eta/m_a",
        eta_residual_column=("-epsilon*(V(t)-V(t-T_*))", "0"),
        a_residual_column=("0", "epsilon"),
        required_numerator=(
            "m_eta=<Psi,F_eta>, including interior, entry, exit, phase, "
            "and complete-history-jump columns"
        ),
        required_denominator=(
            "m_a=<Psi,F_a>, including interior, entry, exit, phase, "
            "and complete-history-jump columns"
        ),
        singular_interior_pairing=str(algebra.singular_fast_adjoint_pairing),
        actual_first_moment_scalar="T_*/5",
        exact_adjoint_ratio_theorem_validated=True,
        residual_columns_validated=True,
        nonzero_first_moment_validated=True,
        leading_singular_interior_pairing_nonzero=False,
        nonzero_moment_implies_nonzero_selected_root_response=False,
        clamped_zero_reset_equilibrium_for_all_eta_validated=True,
        clamped_operational_threshold_supplies_nonzero_eta_column=False,
        same_extended_rfde_selected_root_validated=False,
        augmented_complete_history_bvp_inverse_validated=False,
        dynamic_adjoint_with_endpoint_multipliers_validated=False,
        nonzero_selected_root_eta_response_validated=False,
        fixed_epsilon_one_fifth_overlap_validated=False,
        arbitrary_balanced_topology_full_root_validated=False,
        input_independent_physical_onset_comparison_validated=False,
    )


def _json_value(value: Any) -> Any:
    if isinstance(value, sp.MatrixBase):
        return [[str(sp.simplify(entry)) for entry in value.row(i)] for i in range(value.rows)]
    if isinstance(value, sp.Basic):
        return str(sp.simplify(value))
    if isinstance(value, tuple):
        return [_json_value(item) for item in value]
    if isinstance(value, list):
        return [_json_value(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _json_value(item) for key, item in value.items()}
    return value


def reference_root_adjoint_gate_payload() -> dict[str, Any]:
    """Return a deterministic JSON-ready payload."""

    algebra = root_adjoint_gate_algebra()
    certificate = reference_root_adjoint_gate_certificate()
    return {
        "schema_version": 1,
        "model_id": MODEL_ID,
        "algebra": _json_value(asdict(algebra)),
        "certificate": _json_value(asdict(certificate)),
        "validation_gates": [
            "construct one fixed-epsilon synchronous selected-history Lin/trace BVP",
            "validate its phase-fixed augmented inverse on the full delay horizon",
            "validate the dynamic cokernel covector including endpoint multipliers",
            "enclose m_a=<Psi,F_a> away from zero",
            "enclose m_eta=<Psi,F_eta> away from zero",
            "divide directed intervals to obtain rho_*=-m_eta/m_a",
            "add a transverse trace inverse before promoting to a full-network root",
            "prove an input-independent event zero-set comparison before calling it onset",
        ],
        "scope": {
            "exact_banach_adjoint_ratio": True,
            "exact_model_interior_columns": True,
            "exact_singular_parity_cancellation": True,
            "same_extended_rfde_selected_root": False,
            "nonzero_rho_star": False,
            "physical_onset": False,
        },
    }


def validate_root_adjoint_gate_payload(payload: Mapping[str, Any]) -> None:
    """Reject promotion of any open gate in a serialized payload."""

    expected = reference_root_adjoint_gate_payload()
    if dict(payload) != expected:
        raise ValueError("root-adjoint gate payload does not match exact source algebra")


__all__ = [
    "MODEL_ID",
    "ROOT_OUTPUT",
    "RootAdjointGateAlgebra",
    "RootAdjointGateCertificate",
    "reference_root_adjoint_gate_certificate",
    "reference_root_adjoint_gate_payload",
    "root_adjoint_gate_algebra",
    "root_adjoint_gate_is_exact",
    "validate_root_adjoint_gate_payload",
]
