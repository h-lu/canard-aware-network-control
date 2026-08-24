"""Exact compatibility audit for the lifted root and periodic FHN models.

The arbitrary-size selected-root theorem and the validated periodic/control
chain both use nodewise voltage--recovery variables and an FHN cubic.  They do
not, however, use the same RFDE.  This module records the decisive exact
two-module identities and the delay-redistribution obstruction.

In particular, the selected-root direction ``T`` is invisible to the root
model's critical projection because ``ell_root.T*T*r_root == 0`` while it
forces the root stable mode.  The same matrix is visible on the periodic
model's completely synchronous direction: ``T*ones != 0``.  Conversely, a
two-atom redistribution that is exactly invisible on every synchronous
history must annihilate ``ones`` and hence cannot supply that direct
lifted-style critical-history forcing.

This is an incompatibility certificate, not a no-go theorem for every
possible extension of either model.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

import sympy as sp

from canard_control.lifted_two_module_network import (
    lifted_final_two_module_network,
)


ROOT_CLASS_DOC_SHA256 = (
    "b05fc49c6421121522d4b8dbc28d81892bbbe78c165aea1976bf40d58c658106"
)
ROOT_THEOREM_DOC_SHA256 = (
    "3f6d92487e7fb4f1602a5b07485b81315850c3ae5ea69d3b20a838ed29c257bb"
)
ROOT_MODEL_SOURCE_SHA256 = (
    "a781eb6378f8db95243c5eabb175b5772270f49980715e126144cee12e981796"
)
ROOT_RESPONSE_SOURCE_SHA256 = (
    "32c8cfe6b365c6f78faf4387b2f00569da633ac4b6d34d2a92102de57573a58e"
)
PERIODIC_MODEL_DOC_SHA256 = (
    "b2128ac939bb8940aafe7397771c2e1e33e9b022e016be32dc31f4cdbe1ede95"
)
PERIODIC_BOX_RESULT_SHA256 = (
    "ff13b5352c2b4e9898a4044be63fd490a3e7bb4217445a6a062188c2457c22a0"
)
BALANCED_CHAIN_RESULT_SHA256 = (
    "090e690808d9106152958c1338980fde686875a4113241c8c842683a43d1ebf9"
)
AUTONOMOUS_HANDOFF_RESULT_SHA256 = (
    "38f612771fd5f7e50ffd4f77103ea680b447fd11a7af25cc5ccea95b9bf606f2"
)

MODEL_ID = "lifted-root-versus-dual-scaffold-periodic-compatibility-audit"
ROOT_MODEL_ID = "unequal-two-module-lifted-selected-root-rfde"
PERIODIC_MODEL_ID = "dual-scaffold-rank-one-two-module-fhn-two-delay"
ASSUMPTIONS_ID = (
    "literal-equation-comparison;two-fixed-distinct-delay-atoms;"
    "linear-delay-layer-redistribution;all-scalar-synchronous-histories"
)


Matrix = sp.ImmutableMatrix


def _matrix(value: sp.MatrixBase) -> Matrix:
    return sp.ImmutableMatrix(value)


@dataclass(frozen=True)
class RootPeriodicCompatibilityAudit:
    """Exact two-module identities deciding literal model compatibility."""

    root_fold_voltage: Matrix
    periodic_fold_voltage: Matrix
    fold_voltage_difference: Matrix
    root_critical_right: Matrix
    root_critical_left: Matrix
    periodic_sync_right: Matrix
    periodic_sync_left: Matrix
    root_fast_fold_jacobian: Matrix
    periodic_fast_fold_jacobian: Matrix
    fast_fold_jacobian_difference: Matrix
    root_recovery_scaffold: Matrix
    periodic_recovery_scaffold: Matrix
    recovery_scaffold_difference: Matrix
    root_unfolding_column: Matrix
    periodic_unfolding_column: Matrix
    unfolding_column_difference: Matrix
    root_layer_0: Matrix
    root_layer_1: Matrix
    periodic_layer_0: Matrix
    periodic_layer_1: Matrix
    layer_0_difference: Matrix
    layer_1_difference: Matrix
    root_current_linear_compensator: Matrix
    periodic_current_linear_compensator: Matrix
    current_linear_compensator_difference: Matrix
    root_layer_0_half_row_mass_residual: Matrix
    root_layer_1_half_row_mass_residual: Matrix
    root_layer_0_half_left_balance_residual: Matrix
    root_layer_1_half_left_balance_residual: Matrix
    root_eta_direction: Matrix
    root_eta_action_on_root_critical: Matrix
    root_eta_root_critical_pairing: sp.Expr
    root_eta_action_on_periodic_sync: Matrix
    root_eta_periodic_sync_pairing: sp.Expr
    generic_redistribution_sync_action: Matrix
    generic_sync_invisible_substitution_action: Matrix
    root_eta_preserves_periodic_synchrony: bool
    root_eta_is_invisible_on_periodic_sync_branch: bool
    root_eta_has_nonzero_root_stable_forcing: bool
    root_eta_has_zero_root_critical_pairing: bool


@dataclass(frozen=True)
class RootPeriodicCompatibilityCertificate:
    """Pinned incompatibility result and strict claim ledger."""

    model_id: str
    root_model_id: str
    periodic_model_id: str
    assumptions_id: str
    root_class_doc_sha256: str
    root_theorem_doc_sha256: str
    root_model_source_sha256: str
    root_response_source_sha256: str
    periodic_model_doc_sha256: str
    periodic_box_result_sha256: str
    balanced_chain_result_sha256: str
    autonomous_handoff_result_sha256: str
    root_fold_voltage: tuple[str, str]
    periodic_fold_voltage: tuple[str, str]
    root_critical_right: tuple[str, str]
    periodic_sync_right: tuple[str, str]
    root_eta_action_on_root_critical: tuple[str, str]
    root_eta_action_on_periodic_sync: tuple[str, str]
    root_eta_periodic_sync_pairing: str
    same_nodewise_voltage_recovery_state_type_validated: bool
    same_local_fhn_cubic_term_validated: bool
    same_literal_rfde_validated: bool
    same_fold_state_validated: bool
    same_instantaneous_voltage_scaffold_validated: bool
    same_recovery_scaffold_validated: bool
    same_slow_unfolding_field_validated: bool
    same_delay_layers_validated: bool
    same_linear_current_compensator_validated: bool
    lifted_root_layers_satisfy_balanced_two_half_delay_class_validated: bool
    lifted_eta_zero_root_critical_pairing_validated: bool
    lifted_eta_nonzero_root_stable_forcing_validated: bool
    lifted_eta_preserves_periodic_synchrony_validated: bool
    lifted_eta_invisible_on_validated_periodic_branch_validated: bool
    sync_invisible_two_atom_redistribution_annihilates_sync_critical_forcing_validated: bool
    balanced_control_and_autonomous_handoff_same_baseline_validated: bool
    balanced_synchronous_restriction_matches_periodic_scalar_rfde_validated: bool
    periodic_branch_validated_in_eta_neighborhood: bool
    lifted_selected_root_theorem_applies_to_dual_scaffold_periodic_model: bool
    three_input_three_output_parameter_linked_theorem_validated: bool
    canard_root_to_handoff_trajectory_link_validated: bool
    controlled_onset_to_autonomous_finite_excursion_in_balanced_model_inherited: bool
    autonomous_onset_validated: bool
    biological_basin_validated: bool
    landing_on_periodic_branch_validated: bool


def reference_compatibility_audit() -> RootPeriodicCompatibilityAudit:
    """Return the exact comparison and two-fixed-delay linear obstruction."""

    root = lifted_final_two_module_network(
        1,
        1,
        within_voltage_rate=sp.Integer(2),
        recovery_rate=sp.Integer(1),
        module_redistribution=sp.Integer(0),
    )
    one = sp.ones(2, 1)
    half = sp.Rational(1, 2)
    periodic_projection = one * one.T / 2
    periodic_fold = one
    periodic_fast = 3 * (periodic_projection - sp.eye(2))
    periodic_recovery = 2 * (periodic_projection - sp.eye(2))
    periodic_layer_0 = sp.eye(2) / 2
    periodic_layer_1 = sp.Matrix([[0, half], [half, 0]])
    periodic_current_linear_compensator = sp.eye(2)
    periodic_left = one / 2

    root_unfolding = sp.Matrix([-1, -2])
    periodic_unfolding = -one
    root_eta = sp.Matrix([[1, 0], [-2, 0]])
    root_eta_on_root = sp.simplify(root_eta * root.critical_module_right)
    root_eta_on_sync = sp.simplify(root_eta * one)
    root_stable_projection = sp.eye(2) - (
        root.critical_module_right * root.critical_module_left.T
    )
    periodic_transverse_projection = sp.eye(2) - periodic_projection

    a, b, c, d = sp.symbols("a b c d", real=True)
    generic = sp.Matrix([[a, b], [c, d]])
    generic_action = sp.simplify(generic * one)
    invisible_action = sp.simplify(
        generic_action.subs({b: -a, d: -c})
    )

    return RootPeriodicCompatibilityAudit(
        root_fold_voltage=_matrix(root.equilibrium_voltage),
        periodic_fold_voltage=_matrix(periodic_fold),
        fold_voltage_difference=_matrix(root.equilibrium_voltage - periodic_fold),
        root_critical_right=_matrix(root.critical_module_right),
        root_critical_left=_matrix(root.critical_module_left),
        periodic_sync_right=_matrix(one),
        periodic_sync_left=_matrix(periodic_left),
        root_fast_fold_jacobian=_matrix(root.base_fast_jacobian),
        periodic_fast_fold_jacobian=_matrix(periodic_fast),
        fast_fold_jacobian_difference=_matrix(
            root.base_fast_jacobian - periodic_fast
        ),
        root_recovery_scaffold=_matrix(root.recovery_jacobian),
        periodic_recovery_scaffold=_matrix(periodic_recovery),
        recovery_scaffold_difference=_matrix(
            root.recovery_jacobian - periodic_recovery
        ),
        root_unfolding_column=_matrix(root_unfolding),
        periodic_unfolding_column=_matrix(periodic_unfolding),
        unfolding_column_difference=_matrix(
            root_unfolding - periodic_unfolding
        ),
        root_layer_0=_matrix(root.module_layer_0),
        root_layer_1=_matrix(root.module_layer_1),
        periodic_layer_0=_matrix(periodic_layer_0),
        periodic_layer_1=_matrix(periodic_layer_1),
        layer_0_difference=_matrix(root.module_layer_0 - periodic_layer_0),
        layer_1_difference=_matrix(root.module_layer_1 - periodic_layer_1),
        root_current_linear_compensator=_matrix(root.module_total_layer),
        periodic_current_linear_compensator=_matrix(
            periodic_current_linear_compensator
        ),
        current_linear_compensator_difference=_matrix(
            root.module_total_layer - periodic_current_linear_compensator
        ),
        root_layer_0_half_row_mass_residual=_matrix(
            root.module_layer_0 * one - one / 2
        ),
        root_layer_1_half_row_mass_residual=_matrix(
            root.module_layer_1 * one - one / 2
        ),
        root_layer_0_half_left_balance_residual=_matrix(
            periodic_left.T * root.module_layer_0 - periodic_left.T / 2
        ),
        root_layer_1_half_left_balance_residual=_matrix(
            periodic_left.T * root.module_layer_1 - periodic_left.T / 2
        ),
        root_eta_direction=_matrix(root_eta),
        root_eta_action_on_root_critical=_matrix(root_eta_on_root),
        root_eta_root_critical_pairing=sp.simplify(
            (root.critical_module_left.T * root_eta_on_root)[0]
        ),
        root_eta_action_on_periodic_sync=_matrix(root_eta_on_sync),
        root_eta_periodic_sync_pairing=sp.simplify(
            (periodic_left.T * root_eta_on_sync)[0]
        ),
        generic_redistribution_sync_action=_matrix(generic_action),
        generic_sync_invisible_substitution_action=_matrix(invisible_action),
        root_eta_preserves_periodic_synchrony=bool(
            periodic_transverse_projection * root_eta_on_sync
            == sp.zeros(2, 1)
        ),
        root_eta_is_invisible_on_periodic_sync_branch=bool(
            root_eta_on_sync == sp.zeros(2, 1)
        ),
        root_eta_has_nonzero_root_stable_forcing=bool(
            root_stable_projection * root_eta_on_root != sp.zeros(2, 1)
        ),
        root_eta_has_zero_root_critical_pairing=bool(
            (root.critical_module_left.T * root_eta_on_root)[0] == 0
        ),
    )


def compatibility_audit_is_exact(
    audit: RootPeriodicCompatibilityAudit,
) -> bool:
    """Return whether all decisive equalities and inequalities hold."""

    zero_2 = sp.zeros(2, 1)
    zero_row = sp.zeros(1, 2)
    return bool(
        audit.fold_voltage_difference != zero_2
        and audit.fast_fold_jacobian_difference != sp.zeros(2, 2)
        and audit.recovery_scaffold_difference != sp.zeros(2, 2)
        and audit.unfolding_column_difference != zero_2
        and audit.layer_0_difference != sp.zeros(2, 2)
        and audit.layer_1_difference != sp.zeros(2, 2)
        and audit.current_linear_compensator_difference != sp.zeros(2, 2)
        and audit.root_layer_0_half_row_mass_residual != zero_2
        and audit.root_layer_1_half_row_mass_residual != zero_2
        and audit.root_layer_0_half_left_balance_residual != zero_row
        and audit.root_layer_1_half_left_balance_residual != zero_row
        and audit.root_eta_action_on_root_critical == sp.Matrix([1, -2])
        and audit.root_eta_root_critical_pairing == 0
        and audit.root_eta_action_on_periodic_sync == sp.Matrix([1, -2])
        and audit.root_eta_periodic_sync_pairing == -sp.Rational(1, 2)
        and audit.generic_sync_invisible_substitution_action == zero_2
        and not audit.root_eta_preserves_periodic_synchrony
        and not audit.root_eta_is_invisible_on_periodic_sync_branch
        and audit.root_eta_has_nonzero_root_stable_forcing
        and audit.root_eta_has_zero_root_critical_pairing
    )


def reference_compatibility_certificate() -> RootPeriodicCompatibilityCertificate:
    """Return the strict public incompatibility certificate."""

    audit = reference_compatibility_audit()
    if not compatibility_audit_is_exact(audit):
        raise ValueError("the exact model-compatibility audit failed")
    return RootPeriodicCompatibilityCertificate(
        model_id=MODEL_ID,
        root_model_id=ROOT_MODEL_ID,
        periodic_model_id=PERIODIC_MODEL_ID,
        assumptions_id=ASSUMPTIONS_ID,
        root_class_doc_sha256=ROOT_CLASS_DOC_SHA256,
        root_theorem_doc_sha256=ROOT_THEOREM_DOC_SHA256,
        root_model_source_sha256=ROOT_MODEL_SOURCE_SHA256,
        root_response_source_sha256=ROOT_RESPONSE_SOURCE_SHA256,
        periodic_model_doc_sha256=PERIODIC_MODEL_DOC_SHA256,
        periodic_box_result_sha256=PERIODIC_BOX_RESULT_SHA256,
        balanced_chain_result_sha256=BALANCED_CHAIN_RESULT_SHA256,
        autonomous_handoff_result_sha256=AUTONOMOUS_HANDOFF_RESULT_SHA256,
        root_fold_voltage=tuple(sp.sstr(item) for item in audit.root_fold_voltage),
        periodic_fold_voltage=tuple(
            sp.sstr(item) for item in audit.periodic_fold_voltage
        ),
        root_critical_right=tuple(
            sp.sstr(item) for item in audit.root_critical_right
        ),
        periodic_sync_right=tuple(
            sp.sstr(item) for item in audit.periodic_sync_right
        ),
        root_eta_action_on_root_critical=tuple(
            sp.sstr(item) for item in audit.root_eta_action_on_root_critical
        ),
        root_eta_action_on_periodic_sync=tuple(
            sp.sstr(item) for item in audit.root_eta_action_on_periodic_sync
        ),
        root_eta_periodic_sync_pairing=sp.sstr(
            audit.root_eta_periodic_sync_pairing
        ),
        same_nodewise_voltage_recovery_state_type_validated=True,
        same_local_fhn_cubic_term_validated=True,
        same_literal_rfde_validated=False,
        same_fold_state_validated=False,
        same_instantaneous_voltage_scaffold_validated=False,
        same_recovery_scaffold_validated=False,
        same_slow_unfolding_field_validated=False,
        same_delay_layers_validated=False,
        same_linear_current_compensator_validated=False,
        lifted_root_layers_satisfy_balanced_two_half_delay_class_validated=False,
        lifted_eta_zero_root_critical_pairing_validated=True,
        lifted_eta_nonzero_root_stable_forcing_validated=True,
        lifted_eta_preserves_periodic_synchrony_validated=False,
        lifted_eta_invisible_on_validated_periodic_branch_validated=False,
        sync_invisible_two_atom_redistribution_annihilates_sync_critical_forcing_validated=True,
        balanced_control_and_autonomous_handoff_same_baseline_validated=True,
        balanced_synchronous_restriction_matches_periodic_scalar_rfde_validated=True,
        periodic_branch_validated_in_eta_neighborhood=False,
        lifted_selected_root_theorem_applies_to_dual_scaffold_periodic_model=False,
        three_input_three_output_parameter_linked_theorem_validated=False,
        canard_root_to_handoff_trajectory_link_validated=False,
        controlled_onset_to_autonomous_finite_excursion_in_balanced_model_inherited=True,
        autonomous_onset_validated=False,
        biological_basin_validated=False,
        landing_on_periodic_branch_validated=False,
    )


def _mapping(value: object, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{name} must be a mapping")
    return value


def validate_root_periodic_compatibility_payload(
    payload: object,
) -> RootPeriodicCompatibilityCertificate:
    """Validate the generated record and reject every false promotion."""

    root = _mapping(payload, "result payload")
    provenance = _mapping(root.get("provenance"), "provenance")
    parent_sha256 = _mapping(
        provenance.get("parent_sha256"), "parent_sha256"
    )
    certificate_payload = _mapping(root.get("certificate"), "certificate")
    exact_audit_payload = _mapping(root.get("exact_audit"), "exact_audit")
    parent_claim_checks = _mapping(
        root.get("parent_claim_checks"), "parent_claim_checks"
    )
    scope = _mapping(root.get("scope"), "scope")
    if set(root) != {
        "certificate",
        "exact_audit",
        "parent_claim_checks",
        "provenance",
        "scope",
    }:
        raise ValueError("result payload contains an unpinned section")
    expected = reference_compatibility_certificate()
    expected_dict = {
        field: getattr(expected, field) for field in expected.__dataclass_fields__
    }
    normalized = dict(certificate_payload)
    for tuple_field in (
        "root_fold_voltage",
        "periodic_fold_voltage",
        "root_critical_right",
        "periodic_sync_right",
        "root_eta_action_on_root_critical",
        "root_eta_action_on_periodic_sync",
    ):
        if tuple_field in normalized:
            normalized[tuple_field] = tuple(normalized[tuple_field])
    if normalized != expected_dict:
        raise ValueError("certificate does not match the pinned incompatibility audit")

    expected_audit = reference_compatibility_audit()

    def _audit_value(value: Any) -> Any:
        if isinstance(value, sp.MatrixBase):
            return [[sp.sstr(item) for item in row] for row in value.tolist()]
        if isinstance(value, sp.Basic):
            return sp.sstr(value)
        return value

    expected_exact_audit = {
        field: _audit_value(getattr(expected_audit, field))
        for field in expected_audit.__dataclass_fields__
    }
    if dict(exact_audit_payload) != expected_exact_audit:
        raise ValueError("exact_audit does not match the exact algebra")
    expected_parent_sha256 = {
        "root_class_doc": ROOT_CLASS_DOC_SHA256,
        "root_theorem_doc": ROOT_THEOREM_DOC_SHA256,
        "root_model_source": ROOT_MODEL_SOURCE_SHA256,
        "root_response_source": ROOT_RESPONSE_SOURCE_SHA256,
        "periodic_model_doc": PERIODIC_MODEL_DOC_SHA256,
        "periodic_box_result": PERIODIC_BOX_RESULT_SHA256,
        "balanced_chain_result": BALANCED_CHAIN_RESULT_SHA256,
        "autonomous_handoff_result": AUTONOMOUS_HANDOFF_RESULT_SHA256,
    }
    if dict(parent_sha256) != expected_parent_sha256:
        raise ValueError("parent provenance does not match the pinned inputs")
    expected_parent_claim_checks = {
        "periodic_box_orbit_and_response_validated": True,
        "periodic_box_unique_extrema_validated": True,
        "balanced_synchronous_subspace_invariance_validated": True,
        "balanced_scalar_periodic_restriction_validated": True,
        "balanced_frequency_amplitude_outputs_validated": True,
        "balanced_positive_and_negative_controlled_onset_validated": True,
        "handoff_pins_balanced_parent": True,
        "handoff_same_delayed_baseline_validated": True,
        "handoff_positive_and_negative_autonomous_excursions_validated": True,
        "handoff_rejects_autonomous_onset_and_periodic_landing": True,
    }
    if dict(parent_claim_checks) != expected_parent_claim_checks:
        raise ValueError("parent claim checks do not match the pinned parents")

    required_true = (
        "same_nodewise_voltage_recovery_state_type",
        "same_local_fhn_cubic_term",
        "lifted_eta_zero_root_critical_pairing",
        "lifted_eta_nonzero_root_stable_forcing",
        "sync_invisible_redistribution_annihilates_sync_critical_forcing",
        "balanced_control_and_autonomous_handoff_same_baseline",
        "balanced_synchronous_restriction_matches_periodic_scalar_rfde",
        "controlled_onset_to_autonomous_finite_excursion_in_balanced_model",
    )
    required_false = (
        "same_literal_rfde",
        "same_fold_state",
        "same_instantaneous_voltage_scaffold",
        "same_recovery_scaffold",
        "same_slow_unfolding_field",
        "same_delay_layers",
        "same_linear_current_compensator",
        "lifted_root_layers_satisfy_balanced_two_half_delay_class",
        "lifted_eta_preserves_periodic_synchrony",
        "lifted_eta_invisible_on_validated_periodic_branch",
        "periodic_branch_validated_in_eta_neighborhood",
        "lifted_selected_root_theorem_applies_to_dual_scaffold_periodic_model",
        "three_input_three_output_parameter_linked_theorem",
        "canard_root_to_handoff_trajectory_link",
        "autonomous_onset",
        "biological_basin",
        "landing_on_periodic_branch",
    )
    if any(scope.get(key) is not True for key in required_true):
        raise ValueError("one or more proved compatibility facts are missing")
    if any(scope.get(key) is not False for key in required_false):
        raise ValueError("an incompatible or open claim was promoted")
    expected_scope = {
        field.removesuffix("_validated"): getattr(expected, field)
        for field in expected.__dataclass_fields__
        if field.endswith("_validated")
    }
    expected_scope[
        "controlled_onset_to_autonomous_finite_excursion_in_balanced_model"
    ] = expected.controlled_onset_to_autonomous_finite_excursion_in_balanced_model_inherited
    expected_scope[
        "sync_invisible_redistribution_annihilates_sync_critical_forcing"
    ] = expected_scope.pop(
        "sync_invisible_two_atom_redistribution_annihilates_sync_critical_forcing"
    )
    expected_scope["periodic_branch_validated_in_eta_neighborhood"] = (
        expected.periodic_branch_validated_in_eta_neighborhood
    )
    expected_scope[
        "lifted_selected_root_theorem_applies_to_dual_scaffold_periodic_model"
    ] = expected.lifted_selected_root_theorem_applies_to_dual_scaffold_periodic_model
    if dict(scope) != expected_scope:
        raise ValueError("scope contains an unpinned or missing claim")
    return expected


__all__ = [
    "ASSUMPTIONS_ID",
    "AUTONOMOUS_HANDOFF_RESULT_SHA256",
    "BALANCED_CHAIN_RESULT_SHA256",
    "MODEL_ID",
    "PERIODIC_BOX_RESULT_SHA256",
    "PERIODIC_MODEL_DOC_SHA256",
    "PERIODIC_MODEL_ID",
    "ROOT_CLASS_DOC_SHA256",
    "ROOT_MODEL_ID",
    "ROOT_MODEL_SOURCE_SHA256",
    "ROOT_RESPONSE_SOURCE_SHA256",
    "ROOT_THEOREM_DOC_SHA256",
    "RootPeriodicCompatibilityAudit",
    "RootPeriodicCompatibilityCertificate",
    "compatibility_audit_is_exact",
    "reference_compatibility_audit",
    "reference_compatibility_certificate",
    "validate_root_periodic_compatibility_payload",
]
