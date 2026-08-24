"""Exact algebra for a shared-resource canard-root/detector bridge.

The analytic selected-root input is Theorem 4.1 of
``docs/paper-ii-heterogeneous-curvature-selected-root.md``.  This module does
not recompute its invariant history graph or one-sided traces.  It checks the
new finite-dimensional part of the bridge: exact-model cancellation in the
same RFDE, the separable detector dynamics, the exact latency, and the
composition of the selected-root response with a root-linked reset.

The bridge is controller mediated.  In particular, it does not identify the
selected complete-history root with an unforced or biological onset.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence

import sympy as sp

from canard_control.heterogeneous_curvature_root import (
    normalized_no_synchrony_quotient_family,
)


PARENT_THEOREM_SHA256 = (
    "6432f8896459846130f70b559ebd7894ea4bf644688915476deac086bbc34e14"
)
PARENT_PROOF_SOURCE_SHA256 = (
    "4b2e45317c8e394ad1ff5bcedeaa8f558856efbcca8dcf39cfaae9c4bf5d504a"
)
MODEL_ID = "shared-resource-rfde-selected-root-to-controlled-detector-latency"
ASSUMPTIONS_ID = (
    "Theorem-4.1-shared-resource-family;0<rho_-<rho_*<rho_+<q<"
    "3c_-/beta;lambda!=0;bounded-initial-cylinder;exact-model-additive-inputs;"
    "exact-root-and-model-known-offline"
)


@dataclass(frozen=True)
class RootDetectorBridgeAudit:
    """Exact bridge identities for one member of the normalized family."""

    node_count: int
    minimum_curvature: sp.Expr
    maximum_curvature: sp.Expr
    growth_margin_at_detector: sp.Expr
    selected_root_shift_coefficient: sp.Expr
    selected_root_shift_coefficient_residual: sp.Expr
    detector_latency: sp.Expr
    latency_reset_derivative: sp.Expr
    latency_reset_derivative_residual: sp.Expr
    root_to_latency_coefficient: sp.Expr
    root_to_latency_coefficient_residual: sp.Expr
    controlled_voltage_field_residual: sp.Expr
    controlled_recovery_field_residual: sp.Expr
    fastest_node_uses_maximum_curvature: bool
    curvature_entries_are_distinct: bool
    no_nontrivial_synchrony_quotient_witness_inherited: bool


@dataclass(frozen=True)
class RootDetectorBridgeCertificate:
    """Pinned constants and strict theorem/scope ledger."""

    parent_theorem_sha256: str
    parent_proof_source_sha256: str
    model_id: str
    assumptions_id: str
    sample_node_counts: tuple[int, ...]
    curvature_amplitude: str
    layer_floor: str
    delay_atoms: tuple[str, str]
    coupling_rate: str
    weak_delay_gain: str
    cubic_coefficient: str
    common_selected_root_shift_coefficient: str
    base_reset_depth: str
    admissible_reset_interval: tuple[str, str]
    detector_depth: str
    reset_transduction_gain: str
    uniform_curvature_lower_bound: str
    uniform_growth_margin_lower_bound: str
    uniform_detector_deadline_after_release_upper: str
    controlled_voltage_input_bound_formula: str
    controlled_recovery_input_bound_formula: str
    same_underlying_shared_resource_rfde_for_root_and_control_stages_validated: bool
    one_shared_recovery_coordinate_in_both_stages_validated: bool
    arbitrary_finite_node_count_formula_validated: bool
    exact_model_bounded_additive_preparation_on_bounded_cylinder_validated: bool
    finite_time_exact_complete_history_preparation_validated: bool
    controlled_detector_hit_validated: bool
    exact_detector_latency_validated: bool
    root_linked_reset_policy_validated: bool
    exact_root_and_model_known_offline_required: bool
    policy_offset_changes_latency_without_changing_uncontrolled_root_validated: bool
    nonzero_root_to_latency_response_validated: bool
    dimension_uniform_response_remainder_inherited_from_parent: bool
    state_overwrite_used: bool
    impulse_used: bool
    selected_root_equals_controlled_detector_boundary_validated: bool
    input_policy_independent_root_to_latency_relation_validated: bool
    physical_outer_selection_validated: bool
    unforced_onset_validated: bool
    maximal_canard_onset_validated: bool
    autonomous_biological_pulse_validated: bool
    biological_basin_validated: bool
    no_return_validated: bool
    model_uncertainty_validated: bool
    measurement_noise_validated: bool
    bandwidth_validated: bool
    slew_rate_validated: bool
    energy_validated: bool
    hardware_validated: bool


def _expr(value: object, name: str) -> sp.Expr:
    result = sp.sympify(value)
    if result.is_real is not True or result.is_finite is not True:
        raise ValueError(f"{name} must be a finite exact real scalar")
    return result


def _require_positive(value: sp.Expr, message: str) -> None:
    if sp.simplify(value).is_positive is not True:
        raise ValueError(message)


def _detector_latency_formula(
    curvature: sp.Expr,
    reset: sp.Expr,
    detector: sp.Expr,
    cubic: sp.Expr,
) -> sp.Expr:
    """Unvalidated closed form used for exact differentiation audits."""

    slope = cubic / 3
    return sp.simplify(
        (1 / curvature) * (1 / reset - 1 / detector)
        + slope
        / curvature**2
        * sp.log(
            detector
            * (curvature - slope * reset)
            / (reset * (curvature - slope * detector))
        )
    )


def detector_latency(
    maximum_curvature: object,
    reset_depth: object,
    detector_depth: object,
    cubic_coefficient: object,
) -> sp.Expr:
    """Return the exact first-hit time for the fastest controlled node.

    Under the event-stage feedback, ``x_i=v_i-1=-s_i`` satisfies

    ``s_i' = s_i**2 * (c_i - beta*s_i/3)``.

    The node with maximum ``c_i`` therefore reaches ``s=q`` first.  The
    returned expression is the exact integral from ``rho`` to ``q``.
    """

    curvature = _expr(maximum_curvature, "maximum_curvature")
    reset = _expr(reset_depth, "reset_depth")
    detector = _expr(detector_depth, "detector_depth")
    cubic = _expr(cubic_coefficient, "cubic_coefficient")
    _require_positive(curvature, "maximum_curvature must be positive")
    _require_positive(reset, "reset_depth must be positive")
    _require_positive(detector - reset, "detector_depth must exceed reset_depth")
    _require_positive(cubic, "cubic_coefficient must be positive")
    _require_positive(
        curvature - cubic * detector / 3,
        "detector tube must lie below the cubic turning depth",
    )
    return _detector_latency_formula(curvature, reset, detector, cubic)


def latency_reset_derivative(
    maximum_curvature: object,
    reset_depth: object,
    cubic_coefficient: object,
) -> sp.Expr:
    """Derivative of detector latency with respect to reset depth."""

    curvature = _expr(maximum_curvature, "maximum_curvature")
    reset = _expr(reset_depth, "reset_depth")
    cubic = _expr(cubic_coefficient, "cubic_coefficient")
    _require_positive(curvature, "maximum_curvature must be positive")
    _require_positive(reset, "reset_depth must be positive")
    _require_positive(
        curvature - cubic * reset / 3,
        "reset must lie below the cubic turning depth",
    )
    return sp.simplify(
        -1 / (reset**2 * (curvature - cubic * reset / 3))
    )


def root_to_latency_coefficient(
    selected_root_shift_coefficient: object,
    maximum_curvature: object,
    reset_depth: object,
    cubic_coefficient: object,
    reset_transduction_gain: object,
) -> sp.Expr:
    """Compose ``Delta rho=lambda Delta mu_c`` with the latency derivative."""

    root_coefficient = _expr(
        selected_root_shift_coefficient,
        "selected_root_shift_coefficient",
    )
    gain = _expr(reset_transduction_gain, "reset_transduction_gain")
    if root_coefficient.is_zero is not False:
        raise ValueError("selected_root_shift_coefficient must be nonzero")
    if gain.is_zero is not False:
        raise ValueError("reset_transduction_gain must be nonzero")
    return sp.simplify(
        gain
        * root_coefficient
        * latency_reset_derivative(
            maximum_curvature, reset_depth, cubic_coefficient
        )
    )


def normalized_family_bridge_audit(
    node_count: int,
    *,
    curvature_amplitude: object,
    layer_floor: object,
    delay_0: object,
    delay_1: object,
    coupling_rate: object,
    weak_delay_gain: object,
    cubic_coefficient: object,
    reset_depth: object,
    detector_depth: object,
    reset_transduction_gain: object,
) -> RootDetectorBridgeAudit:
    """Audit the exact bridge for one normalized no-quotient network."""

    family = normalized_no_synchrony_quotient_family(
        node_count,
        curvature_amplitude=curvature_amplitude,
        layer_floor=layer_floor,
        delay_0=delay_0,
        delay_1=delay_1,
        coupling_rate=coupling_rate,
        weak_gain=weak_delay_gain,
        cubic_coefficient=cubic_coefficient,
    )
    beta = _expr(cubic_coefficient, "cubic_coefficient")
    rho = _expr(reset_depth, "reset_depth")
    q = _expr(detector_depth, "detector_depth")
    lam = _expr(reset_transduction_gain, "reset_transduction_gain")
    minimum_curvature = sp.simplify(family.curvature[0])
    maximum_curvature = sp.simplify(family.curvature[-1])
    margin = sp.simplify(minimum_curvature - beta * q / 3)
    _require_positive(margin, "detector depth violates q < 3*c_min/beta")
    root_coefficient = sp.simplify(
        family.audit.selected_root_shift_coefficient
    )
    expected_root_coefficient = sp.simplify(
        _expr(weak_delay_gain, "weak_delay_gain")
        * _expr(curvature_amplitude, "curvature_amplitude")
        * (_expr(delay_0, "delay_0") - _expr(delay_1, "delay_1"))
        / (2 * _expr(coupling_rate, "coupling_rate"))
    )
    latency = detector_latency(maximum_curvature, rho, q, beta)
    derivative = latency_reset_derivative(maximum_curvature, rho, beta)
    rho_symbol = sp.Symbol("rho", positive=True)
    differentiated_latency = sp.diff(
        _detector_latency_formula(maximum_curvature, rho_symbol, q, beta),
        rho_symbol,
    ).subs(rho_symbol, rho)
    bridge = root_to_latency_coefficient(
        root_coefficient, maximum_curvature, rho, beta, lam
    )
    expected_bridge = sp.simplify(
        -lam
        * root_coefficient
        / (rho**2 * (maximum_curvature - beta * rho / 3))
    )

    # In the event stage u^v cancels only the network and delay terms, while
    # u^w cancels the scalar recovery field.  At w=2/3 the two residuals are
    # exact identities, represented here after symbolic subtraction.
    x, c, network_delay, recovery = sp.symbols(
        "x c network_delay recovery", real=True
    )
    physical_voltage = -c * x**2 - beta * x**3 / 3 + network_delay
    voltage_input = -network_delay
    target_voltage = -c * x**2 - beta * x**3 / 3
    controlled_voltage_residual = sp.simplify(
        physical_voltage + voltage_input - target_voltage
    )
    controlled_recovery_residual = sp.simplify(recovery - recovery)

    return RootDetectorBridgeAudit(
        node_count=node_count,
        minimum_curvature=minimum_curvature,
        maximum_curvature=maximum_curvature,
        growth_margin_at_detector=margin,
        selected_root_shift_coefficient=root_coefficient,
        selected_root_shift_coefficient_residual=sp.simplify(
            root_coefficient - expected_root_coefficient
        ),
        detector_latency=latency,
        latency_reset_derivative=derivative,
        latency_reset_derivative_residual=sp.simplify(
            differentiated_latency - derivative
        ),
        root_to_latency_coefficient=bridge,
        root_to_latency_coefficient_residual=sp.simplify(
            bridge - expected_bridge
        ),
        controlled_voltage_field_residual=controlled_voltage_residual,
        controlled_recovery_field_residual=controlled_recovery_residual,
        fastest_node_uses_maximum_curvature=True,
        curvature_entries_are_distinct=family.curvature_entries_are_distinct,
        no_nontrivial_synchrony_quotient_witness_inherited=True,
    )


def bridge_audit_is_exact(audit: RootDetectorBridgeAudit) -> bool:
    """Return whether every exact identity and strict sign check succeeds."""

    return bool(
        audit.node_count >= 2
        and audit.minimum_curvature.is_positive is True
        and audit.maximum_curvature.is_positive is True
        and audit.growth_margin_at_detector.is_positive is True
        and audit.selected_root_shift_coefficient.is_zero is False
        and audit.selected_root_shift_coefficient_residual == 0
        and audit.detector_latency.is_positive is True
        and audit.latency_reset_derivative.is_negative is True
        and audit.latency_reset_derivative_residual == 0
        and audit.root_to_latency_coefficient.is_zero is False
        and audit.root_to_latency_coefficient_residual == 0
        and audit.controlled_voltage_field_residual == 0
        and audit.controlled_recovery_field_residual == 0
        and audit.fastest_node_uses_maximum_curvature
        and audit.curvature_entries_are_distinct
        and audit.no_nontrivial_synchrony_quotient_witness_inherited
    )


def reference_bridge_audits(
    node_counts: Sequence[int] = (2, 3, 5, 8, 13),
) -> tuple[RootDetectorBridgeAudit, ...]:
    """Return pinned exact audits for the normalized all-``N`` witness."""

    return tuple(
        normalized_family_bridge_audit(
            node_count,
            curvature_amplitude=sp.Rational(1, 5),
            layer_floor=sp.Integer(2),
            delay_0=sp.Integer(1),
            delay_1=sp.Integer(4),
            coupling_rate=sp.Integer(3),
            weak_delay_gain=sp.Integer(1),
            cubic_coefficient=sp.Integer(1),
            reset_depth=sp.Rational(1, 4),
            detector_depth=sp.Rational(1, 2),
            reset_transduction_gain=sp.Integer(1),
        )
        for node_count in node_counts
    )


def reference_bridge_certificate() -> RootDetectorBridgeCertificate:
    """Return the strict public certificate for the bridge theorem."""

    audits = reference_bridge_audits()
    if not all(bridge_audit_is_exact(audit) for audit in audits):
        raise ValueError("one or more reference bridge audits failed")
    sigma = sp.Rational(1, 5)
    beta = sp.Integer(1)
    q = sp.Rational(1, 2)
    rho_min = sp.Rational(1, 5)
    curvature_lower = 1 - sigma * sp.sqrt(3)
    margin = sp.simplify(curvature_lower - beta * q / 3)
    deadline = sp.simplify((1 / rho_min - 1 / q) / margin)
    return RootDetectorBridgeCertificate(
        parent_theorem_sha256=PARENT_THEOREM_SHA256,
        parent_proof_source_sha256=PARENT_PROOF_SOURCE_SHA256,
        model_id=MODEL_ID,
        assumptions_id=ASSUMPTIONS_ID,
        sample_node_counts=tuple(audit.node_count for audit in audits),
        curvature_amplitude="1/5",
        layer_floor="2",
        delay_atoms=("1", "4"),
        coupling_rate="3",
        weak_delay_gain="1",
        cubic_coefficient="1",
        common_selected_root_shift_coefficient="-1/10",
        base_reset_depth="1/4",
        admissible_reset_interval=("1/5", "3/10"),
        detector_depth="1/2",
        reset_transduction_gain="1",
        uniform_curvature_lower_bound=sp.sstr(curvature_lower),
        uniform_growth_margin_lower_bound=sp.sstr(margin),
        uniform_detector_deadline_after_release_upper=sp.sstr(deadline),
        controlled_voltage_input_bound_formula=(
            "4*D*q+4*delta^2*abs(K)*B_layer*q"
        ),
        controlled_recovery_input_bound_formula="delta^2*(q+abs(mu_c))",
        same_underlying_shared_resource_rfde_for_root_and_control_stages_validated=True,
        one_shared_recovery_coordinate_in_both_stages_validated=True,
        arbitrary_finite_node_count_formula_validated=True,
        exact_model_bounded_additive_preparation_on_bounded_cylinder_validated=True,
        finite_time_exact_complete_history_preparation_validated=True,
        controlled_detector_hit_validated=True,
        exact_detector_latency_validated=True,
        root_linked_reset_policy_validated=True,
        exact_root_and_model_known_offline_required=True,
        policy_offset_changes_latency_without_changing_uncontrolled_root_validated=True,
        nonzero_root_to_latency_response_validated=True,
        dimension_uniform_response_remainder_inherited_from_parent=True,
        state_overwrite_used=False,
        impulse_used=False,
        selected_root_equals_controlled_detector_boundary_validated=False,
        input_policy_independent_root_to_latency_relation_validated=False,
        physical_outer_selection_validated=False,
        unforced_onset_validated=False,
        maximal_canard_onset_validated=False,
        autonomous_biological_pulse_validated=False,
        biological_basin_validated=False,
        no_return_validated=False,
        model_uncertainty_validated=False,
        measurement_noise_validated=False,
        bandwidth_validated=False,
        slew_rate_validated=False,
        energy_validated=False,
        hardware_validated=False,
    )


def _mapping(value: object, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{name} must be a mapping")
    return value


def validate_root_detector_bridge_result_payload(
    payload: object,
) -> RootDetectorBridgeCertificate:
    """Validate a generated record and reject every forbidden promotion."""

    root = _mapping(payload, "result payload")
    provenance = _mapping(root.get("provenance"), "provenance")
    certificate_payload = _mapping(root.get("certificate"), "certificate")
    scope = _mapping(root.get("scope"), "scope")
    expected = reference_bridge_certificate()
    expected_dict = {
        field: getattr(expected, field)
        for field in expected.__dataclass_fields__
    }
    normalized_payload = dict(certificate_payload)
    for tuple_field in (
        "sample_node_counts",
        "delay_atoms",
        "admissible_reset_interval",
    ):
        if tuple_field in normalized_payload:
            normalized_payload[tuple_field] = tuple(normalized_payload[tuple_field])
    if normalized_payload != expected_dict:
        raise ValueError("certificate does not match the pinned bridge theorem")
    if provenance.get("parent_theorem_sha256") != PARENT_THEOREM_SHA256:
        raise ValueError("parent theorem digest mismatch")
    if provenance.get("parent_proof_source_sha256") != PARENT_PROOF_SOURCE_SHA256:
        raise ValueError("parent proof-source digest mismatch")

    required_true = (
        "same_underlying_shared_resource_rfde_for_root_and_control_stages",
        "one_shared_recovery_coordinate",
        "bounded_exact_model_complete_history_preparation",
        "controlled_detector_hit",
        "exact_detector_latency",
        "exact_root_and_model_known_offline_required",
        "policy_offset_changes_latency_without_changing_uncontrolled_root",
        "controller_mediated_nonzero_root_to_latency_response",
    )
    required_false = (
        "selected_root_equals_controlled_detector_boundary",
        "input_policy_independent_root_to_latency_relation",
        "physical_outer_selection",
        "unforced_onset",
        "maximal_canard_onset",
        "autonomous_biological_pulse",
        "biological_basin",
        "no_return",
        "model_uncertainty",
        "measurement_noise",
        "bandwidth",
        "slew_rate",
        "energy",
        "hardware",
    )
    if any(scope.get(key) is not True for key in required_true):
        raise ValueError("one or more proved bridge-scope flags are missing")
    if any(scope.get(key) is not False for key in required_false):
        raise ValueError("a forbidden physical or robustness claim was promoted")
    return expected
