"""Exact stop/go audit for quadratic-root to physical-onset composition.

The quadratic period-locked RFDE has a proved small-delta canonical selected
root, while the bounded preparation, handoff, and periodic-attraction
theorems live on a fixed operating slice.  This module records the exact
slice and model mismatches.  It also proves one positive but explicitly
controlled transfer: exact cancellation of the quadratic carrier through
preparation and decision, followed by absorption of the released carrier in
the existing robust post-handoff residual budget for sufficiently small
``eta``.

Nothing here identifies the selected root with an input-independent event,
constructs pulse/quiet basins, or proves permanent no return.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from hashlib import sha256
from pathlib import Path
from typing import Any, Mapping

import sympy as sp


QUADRATIC_CARRIER_RESULT_SHA256 = (
    "4f80cd8ef53161e16886c06fdc52d99be774a9b1cf15d3e7ba534fe37925f7f8"
)
QUADRATIC_DOBRUSHIN_RESULT_SHA256 = (
    "c4ccae41965c2cfc8059bb7ec87dd4a7e583e6db914ff36087095945c8b1fdea"
)
FIXED_EPSILON_BVP_RESULT_SHA256 = (
    "1af8aa46b31bb099a8f07e7646b656577d010dc413094ad3be0afb32c70c993a"
)
BOUNDED_PREPARATION_RESULT_SHA256 = (
    "8681f800c42420207a94f505b3c8831c7409f3619cf640cbd24de580cd87f548"
)
BALANCED_CONTROL_CHAIN_RESULT_SHA256 = (
    "090e690808d9106152958c1338980fde686875a4113241c8c842683a43d1ebf9"
)
ROBUST_HANDOFF_RESULT_SHA256 = (
    "ff0320038842cbdbf6481d634f67844d418fba13e804654c2c335e9c3381140e"
)
AUTONOMOUS_HANDOFF_RESULT_SHA256 = (
    "38f612771fd5f7e50ffd4f77103ea680b447fd11a7af25cc5ccea95b9bf606f2"
)
PERIODIC_BOX_RESULT_SHA256 = (
    "ff13b5352c2b4e9898a4044be63fd490a3e7bb4217445a6a062188c2457c22a0"
)
PERIODIC_ATTRACTION_RESULT_SHA256 = (
    "20fb3f0259f7d2bf8d5ccd24303250661a405418ea733e5419de5f2f07ddea72"
)
PHYSICAL_OUTER_BRIDGE_DOC_SHA256 = (
    "e9adc33a9286aff8d3c431e87769237cdd4351fdf8b011f1ca233cb964e5ba24"
)
UNFORCED_CAPTURE_DOC_SHA256 = (
    "af12957136b0800692d8f38052e729f1641cde2cd59b114e0d7422a219d9a764"
)

PROOF_SOURCE_RELATIVE_PATH = (
    "src/canard_control/quadratic_physical_onset_stop_go.py"
)
GENERATOR_RELATIVE_PATH = "experiments/quadratic_physical_onset_stop_go.py"
DEFAULT_COMMAND = (
    "PYTHONPATH=build/testdeps:src /usr/bin/python3 "
    "experiments/quadratic_physical_onset_stop_go.py"
)
MODEL_ID = "quadratic-period-locked-fhn-physical-onset-stop-go-audit"
ASSUMPTIONS_ID = (
    "arbitrary-finite-balanced-two-half-delay-layer-network;"
    "extended-T-star-history-cylinder;"
    "exact-quadratic-cancellation-through-controlled-decision;"
    "zero-other-post-handoff-residual;strict-small-eta-release"
)
ARITHMETIC_DESCRIPTION = (
    "exact SymPy slice-separation, quadratic-carrier cancellation, "
    "branch-square-range, residual-budget, and authority-margin identities"
)


@dataclass(frozen=True)
class CompositionMismatchAudit:
    """Exact data behind the four non-composition gates."""

    singular_root_unfolding_limit: sp.Expr
    controlled_periodic_unfolding: sp.Expr
    limiting_unfolding_gap: sp.Expr
    reference_delta: sp.Expr
    reference_epsilon: sp.Expr
    reference_base_delays: tuple[sp.Expr, sp.Expr]
    root_family_delay_scaling: tuple[sp.Expr, sp.Expr]
    root_quadratic_delay_scaling: str
    reference_period_lock_relation: str
    root_history_horizon: str
    parent_preparation_horizon: sp.Expr
    canonical_root_preparation: str
    controlled_reset_preparations: tuple[str, str]
    root_plant_quadratic_channel: str
    parent_handoff_quadratic_channel: str
    periodic_basin_slice: str
    physical_outer_bridge_plant: str


@dataclass(frozen=True)
class ControlledQuadraticTransferAudit:
    """Exact bounds for the controlled small-eta handoff transfer."""

    epsilon_reference: sp.Expr
    epsilon_robust_upper: sp.Expr
    voltage_residual_budget: sp.Expr
    collective_projector_sup_norm: sp.Expr
    positive_voltage_interval: tuple[sp.Expr, sp.Expr]
    negative_voltage_interval: tuple[sp.Expr, sp.Expr]
    positive_shifted_square_range: tuple[sp.Expr, sp.Expr]
    negative_shifted_square_range: tuple[sp.Expr, sp.Expr]
    positive_quadratic_difference_upper: sp.Expr
    negative_quadratic_difference_upper: sp.Expr
    positive_residual_per_abs_eta_upper: sp.Expr
    negative_residual_per_abs_eta_upper: sp.Expr
    positive_abs_eta_strict_upper: sp.Expr
    negative_abs_eta_strict_upper: sp.Expr
    common_abs_eta_strict_upper: sp.Expr
    preparation_voltage_abs_bound: sp.Expr
    preparation_shifted_square_range: tuple[sp.Expr, sp.Expr]
    preparation_carrier_per_abs_eta_upper: sp.Expr
    old_voltage_authority_upper: sp.Expr
    voltage_authority_ceiling: sp.Expr
    old_voltage_authority_slack: sp.Expr
    added_preparation_authority_at_common_eta_upper: sp.Expr
    remaining_voltage_authority_margin_lower: sp.Expr
    constant_history_carrier_action: sp.Expr
    carrier_plus_exact_cancellation_action: sp.Expr


@dataclass(frozen=True)
class QuadraticPhysicalOnsetStopGoCertificate:
    """Machine-readable proved/open ledger."""

    model_id: str
    assumptions_id: str
    quadratic_carrier_result_sha256: str
    quadratic_dobrushin_result_sha256: str
    fixed_epsilon_bvp_result_sha256: str
    bounded_preparation_result_sha256: str
    balanced_control_chain_result_sha256: str
    robust_handoff_result_sha256: str
    autonomous_handoff_result_sha256: str
    periodic_box_result_sha256: str
    periodic_attraction_result_sha256: str
    physical_outer_bridge_doc_sha256: str
    unforced_capture_doc_sha256: str
    delta_and_unfolding_theorem_domains_overlap_validated: bool
    root_family_quadratic_channel_period_locked_validated: bool
    canonical_root_and_controlled_reset_preparations_identified_validated: bool
    nonzero_eta_handoff_parent_has_literal_quadratic_plant_validated: bool
    handoff_terminal_blocks_inside_periodic_or_quiet_basins_validated: bool
    paper_iii_literal_quadratic_plant_identity_validated: bool
    four_gate_existing_module_composition_validated: bool
    quadratic_carrier_zero_on_constant_histories_validated: bool
    exact_control_cancellation_through_preparation_and_decision_validated: bool
    extended_t_star_history_hold_required: bool
    controlled_reference_slice_small_eta_terminal_transfer_validated: bool
    arbitrary_finite_balanced_topology_controlled_transfer_validated: bool
    positive_eta_bound_validated: bool
    negative_eta_bound_validated: bool
    common_eta_bound_is_negative_minimum_validated: bool
    all_additive_inputs_zero_after_quadratic_handoff_validated: bool
    controlled_transfer_is_input_independent_onset_validated: bool
    fixed_epsilon_selected_root_validated: bool
    fixed_epsilon_nonzero_root_response_validated: bool
    physical_outer_history_equals_canonical_root_history_validated: bool
    selected_root_event_factorization_validated: bool
    pulse_quiet_capture_validated: bool
    permanent_detector_face_no_return_validated: bool
    periodic_basin_eta_neighborhood_validated: bool
    terminal_block_periodic_basin_containment_validated: bool
    quiet_basin_validated: bool
    biological_pulse_onset_validated: bool


@lru_cache(maxsize=1)
def reference_composition_mismatch_audit() -> CompositionMismatchAudit:
    """Return the exact slice, preparation, plant, and basin mismatches."""

    delta = sp.Symbol("delta", positive=True)
    return CompositionMismatchAudit(
        singular_root_unfolding_limit=sp.Integer(1),
        controlled_periodic_unfolding=sp.Rational(3, 5),
        limiting_unfolding_gap=sp.Rational(2, 5),
        reference_delta=1 / sp.sqrt(5),
        reference_epsilon=sp.Rational(1, 5),
        reference_base_delays=(4 * sp.sqrt(5), 5 * sp.sqrt(5)),
        root_family_delay_scaling=(4 / delta, 5 / delta),
        root_quadratic_delay_scaling="Theta_*/delta",
        reference_period_lock_relation="Theta_*=T_*/sqrt(5) only at delta=1/sqrt(5)",
        root_history_horizon="max{4,5,Theta_*}/delta",
        parent_preparation_horizon=5 * sp.sqrt(5),
        canonical_root_preparation=(
            "parameter-coherent enlarged-horizon canonical flow-hull preparation"
        ),
        controlled_reset_preparations=("Phi_{+1/2}", "Phi_{-1/2}"),
        root_plant_quadratic_channel=(
            "epsilon*eta*Pi*((v(t)-1)^2-(v(t-T_*)-1)^2)"
        ),
        parent_handoff_quadratic_channel="absent",
        periodic_basin_slice=(
            "epsilon=1/5,a=3/5,eta=0,tau(Q)<=1/4; local basin for each fixed "
            "finite network, without a uniform radius"
        ),
        physical_outer_bridge_plant=(
            "heterogeneous-curvature two-module physical RFDE, not the quadratic dual scaffold"
        ),
    )


@lru_cache(maxsize=1)
def reference_controlled_quadratic_transfer_audit(
) -> ControlledQuadraticTransferAudit:
    """Return exact carrier/residual bounds on the inherited handoff tubes."""

    epsilon = sp.Rational(1, 5)
    epsilon_upper = sp.Rational(200001, 1000000)
    residual_budget = sp.Rational(1, 100000)
    pi_norm = sp.Integer(1)

    positive_interval = (sp.Rational(2497, 5000), sp.Rational(7503, 5000))
    negative_interval = (-sp.Rational(6003, 5000), -sp.Rational(2497, 5000))

    positive_square = (
        sp.Integer(0),
        sp.Rational(2503, 5000) ** 2,
    )
    negative_square = (
        sp.Rational(7497, 5000) ** 2,
        sp.Rational(11003, 5000) ** 2,
    )
    positive_difference = sp.simplify(positive_square[1] - positive_square[0])
    negative_difference = sp.simplify(negative_square[1] - negative_square[0])
    positive_residual = sp.simplify(
        epsilon_upper * pi_norm * positive_difference
    )
    negative_residual = sp.simplify(
        epsilon_upper * pi_norm * negative_difference
    )
    positive_eta = sp.simplify(residual_budget / positive_residual)
    negative_eta = sp.simplify(residual_budget / negative_residual)
    common_eta = sp.Min(positive_eta, negative_eta)

    # On ||v||_inf <= 2, both (v-1)^2 values lie in [0,9], so their
    # componentwise difference, and hence its stochastic Pi average, has
    # norm at most 9.  Exact cancellation adds this amount to the old
    # preparation authority.
    prep_abs_bound = sp.Integer(2)
    prep_square = (sp.Integer(0), sp.Integer(9))
    prep_carrier = sp.simplify(epsilon * (prep_square[1] - prep_square[0]))
    old_authority = sp.Rational(
        "23.1849790618559665912241330350020100086302109395593948"
    )
    authority_ceiling = sp.Rational(2319, 100)
    old_slack = sp.simplify(authority_ceiling - old_authority)
    added_at_common = sp.simplify(prep_carrier * common_eta)
    remaining_margin = sp.simplify(old_slack - added_at_common)

    r, current_square, delayed_square = sp.symbols(
        "r current_square delayed_square", real=True
    )
    constant_action = sp.expand((r - 1) ** 2 - (r - 1) ** 2)
    carrier = epsilon * (current_square - delayed_square)
    cancellation = -carrier

    return ControlledQuadraticTransferAudit(
        epsilon_reference=epsilon,
        epsilon_robust_upper=epsilon_upper,
        voltage_residual_budget=residual_budget,
        collective_projector_sup_norm=pi_norm,
        positive_voltage_interval=positive_interval,
        negative_voltage_interval=negative_interval,
        positive_shifted_square_range=positive_square,
        negative_shifted_square_range=negative_square,
        positive_quadratic_difference_upper=positive_difference,
        negative_quadratic_difference_upper=negative_difference,
        positive_residual_per_abs_eta_upper=positive_residual,
        negative_residual_per_abs_eta_upper=negative_residual,
        positive_abs_eta_strict_upper=positive_eta,
        negative_abs_eta_strict_upper=negative_eta,
        common_abs_eta_strict_upper=common_eta,
        preparation_voltage_abs_bound=prep_abs_bound,
        preparation_shifted_square_range=prep_square,
        preparation_carrier_per_abs_eta_upper=prep_carrier,
        old_voltage_authority_upper=old_authority,
        voltage_authority_ceiling=authority_ceiling,
        old_voltage_authority_slack=old_slack,
        added_preparation_authority_at_common_eta_upper=added_at_common,
        remaining_voltage_authority_margin_lower=remaining_margin,
        constant_history_carrier_action=constant_action,
        carrier_plus_exact_cancellation_action=sp.expand(carrier + cancellation),
    )


@lru_cache(maxsize=1)
def stop_go_algebra_is_exact() -> bool:
    """Check every exact identity used by the positive and stop gates."""

    mismatch = reference_composition_mismatch_audit()
    transfer = reference_controlled_quadratic_transfer_audit()
    return bool(
        mismatch.limiting_unfolding_gap == sp.Rational(2, 5)
        and mismatch.reference_delta**2 == sp.Rational(1, 5)
        and transfer.positive_quadratic_difference_upper
        == sp.Rational(6265009, 25000000)
        and transfer.negative_quadratic_difference_upper
        == sp.Rational(64861, 25000)
        and transfer.positive_residual_per_abs_eta_upper
        == sp.Rational(1253008065009, 25000000000000)
        and transfer.negative_residual_per_abs_eta_upper
        == sp.Rational(12972264861, 25000000000)
        and transfer.negative_abs_eta_strict_upper
        < transfer.positive_abs_eta_strict_upper
        and transfer.common_abs_eta_strict_upper
        == transfer.negative_abs_eta_strict_upper
        and transfer.preparation_carrier_per_abs_eta_upper == sp.Rational(9, 5)
        and transfer.remaining_voltage_authority_margin_lower > 0
        and transfer.constant_history_carrier_action == 0
        and transfer.carrier_plus_exact_cancellation_action == 0
    )


@lru_cache(maxsize=1)
def reference_stop_go_certificate() -> QuadraticPhysicalOnsetStopGoCertificate:
    """Return the strict proved/open claim ledger."""

    if not stop_go_algebra_is_exact():
        raise ValueError("quadratic onset stop/go algebra failed")
    return QuadraticPhysicalOnsetStopGoCertificate(
        model_id=MODEL_ID,
        assumptions_id=ASSUMPTIONS_ID,
        quadratic_carrier_result_sha256=QUADRATIC_CARRIER_RESULT_SHA256,
        quadratic_dobrushin_result_sha256=QUADRATIC_DOBRUSHIN_RESULT_SHA256,
        fixed_epsilon_bvp_result_sha256=FIXED_EPSILON_BVP_RESULT_SHA256,
        bounded_preparation_result_sha256=BOUNDED_PREPARATION_RESULT_SHA256,
        balanced_control_chain_result_sha256=BALANCED_CONTROL_CHAIN_RESULT_SHA256,
        robust_handoff_result_sha256=ROBUST_HANDOFF_RESULT_SHA256,
        autonomous_handoff_result_sha256=AUTONOMOUS_HANDOFF_RESULT_SHA256,
        periodic_box_result_sha256=PERIODIC_BOX_RESULT_SHA256,
        periodic_attraction_result_sha256=PERIODIC_ATTRACTION_RESULT_SHA256,
        physical_outer_bridge_doc_sha256=PHYSICAL_OUTER_BRIDGE_DOC_SHA256,
        unforced_capture_doc_sha256=UNFORCED_CAPTURE_DOC_SHA256,
        delta_and_unfolding_theorem_domains_overlap_validated=False,
        root_family_quadratic_channel_period_locked_validated=False,
        canonical_root_and_controlled_reset_preparations_identified_validated=False,
        nonzero_eta_handoff_parent_has_literal_quadratic_plant_validated=False,
        handoff_terminal_blocks_inside_periodic_or_quiet_basins_validated=False,
        paper_iii_literal_quadratic_plant_identity_validated=False,
        four_gate_existing_module_composition_validated=False,
        quadratic_carrier_zero_on_constant_histories_validated=True,
        exact_control_cancellation_through_preparation_and_decision_validated=True,
        extended_t_star_history_hold_required=True,
        controlled_reference_slice_small_eta_terminal_transfer_validated=True,
        arbitrary_finite_balanced_topology_controlled_transfer_validated=True,
        positive_eta_bound_validated=True,
        negative_eta_bound_validated=True,
        common_eta_bound_is_negative_minimum_validated=True,
        all_additive_inputs_zero_after_quadratic_handoff_validated=True,
        controlled_transfer_is_input_independent_onset_validated=False,
        fixed_epsilon_selected_root_validated=False,
        fixed_epsilon_nonzero_root_response_validated=False,
        physical_outer_history_equals_canonical_root_history_validated=False,
        selected_root_event_factorization_validated=False,
        pulse_quiet_capture_validated=False,
        permanent_detector_face_no_return_validated=False,
        periodic_basin_eta_neighborhood_validated=False,
        terminal_block_periodic_basin_containment_validated=False,
        quiet_basin_validated=False,
        biological_pulse_onset_validated=False,
    )


def _mapping(value: object, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{name} must be a mapping")
    return value


def _audit_value(value: Any) -> Any:
    if isinstance(value, sp.Basic):
        return sp.sstr(value)
    if isinstance(value, tuple):
        return [_audit_value(item) for item in value]
    return value


def validate_stop_go_payload(
    payload: object,
) -> QuadraticPhysicalOnsetStopGoCertificate:
    """Validate source-bound exact audits and reject physical promotions."""

    root = _mapping(payload, "result payload")
    if set(root) != {"certificate", "exact_audits", "provenance", "scope"}:
        raise ValueError("result payload contains an unpinned section")
    provenance = _mapping(root.get("provenance"), "provenance")
    certificate_payload = _mapping(root.get("certificate"), "certificate")
    exact_audits = _mapping(root.get("exact_audits"), "exact_audits")
    scope = _mapping(root.get("scope"), "scope")

    expected_provenance_keys = {
        "generator",
        "generator_sha256",
        "proof_source",
        "proof_source_sha256",
        "parent_sha256",
        "parent_claim_checks",
        "argv",
        "default_command",
        "python",
        "platform",
        "arithmetic",
    }
    if set(provenance) != expected_provenance_keys:
        raise ValueError("provenance contains an unpinned or missing field")
    source_path = Path(__file__).resolve()
    repository = source_path.parents[2]
    generator_path = repository / GENERATOR_RELATIVE_PATH
    source_bound = {
        "generator": GENERATOR_RELATIVE_PATH,
        "generator_sha256": sha256(generator_path.read_bytes()).hexdigest(),
        "proof_source": PROOF_SOURCE_RELATIVE_PATH,
        "proof_source_sha256": sha256(source_path.read_bytes()).hexdigest(),
        "default_command": DEFAULT_COMMAND,
        "arithmetic": ARITHMETIC_DESCRIPTION,
    }
    for key, expected_value in source_bound.items():
        if provenance.get(key) != expected_value:
            raise ValueError(f"provenance {key} is not source-bound")
    argv = provenance.get("argv")
    if (
        not isinstance(argv, list)
        or len(argv) != 2
        or not isinstance(argv[0], str)
        or not argv[0]
        or argv[1] != GENERATOR_RELATIVE_PATH
    ):
        raise ValueError("provenance argv is not the declared generator call")
    for key in ("python", "platform"):
        if not isinstance(provenance.get(key), str) or not provenance[key]:
            raise ValueError(f"provenance {key} must be a nonempty string")

    expected = reference_stop_go_certificate()
    expected_certificate = {
        field: getattr(expected, field) for field in expected.__dataclass_fields__
    }
    if dict(certificate_payload) != expected_certificate:
        raise ValueError("certificate does not match the strict stop/go ledger")

    expected_parents = {
        "quadratic_carrier_result": QUADRATIC_CARRIER_RESULT_SHA256,
        "quadratic_dobrushin_result": QUADRATIC_DOBRUSHIN_RESULT_SHA256,
        "fixed_epsilon_bvp_result": FIXED_EPSILON_BVP_RESULT_SHA256,
        "bounded_preparation_result": BOUNDED_PREPARATION_RESULT_SHA256,
        "balanced_control_chain_result": BALANCED_CONTROL_CHAIN_RESULT_SHA256,
        "robust_handoff_result": ROBUST_HANDOFF_RESULT_SHA256,
        "autonomous_handoff_result": AUTONOMOUS_HANDOFF_RESULT_SHA256,
        "periodic_box_result": PERIODIC_BOX_RESULT_SHA256,
        "periodic_attraction_result": PERIODIC_ATTRACTION_RESULT_SHA256,
        "physical_outer_bridge_doc": PHYSICAL_OUTER_BRIDGE_DOC_SHA256,
        "unforced_capture_doc": UNFORCED_CAPTURE_DOC_SHA256,
    }
    parents = _mapping(provenance.get("parent_sha256"), "parent_sha256")
    if dict(parents) != expected_parents:
        raise ValueError("parent provenance does not match the pinned inputs")

    expected_parent_checks = {
        "small_delta_canonical_root_proved": True,
        "fixed_epsilon_root_refused": True,
        "physical_onset_refused_by_root_parents": True,
        "bounded_preparation_is_controlled_fixed_slice": True,
        "balanced_control_chain_has_general_bounded_preparation": True,
        "robust_handoff_has_residual_budget": True,
        "robust_handoff_refuses_basin_and_no_return": True,
        "autonomous_handoff_refuses_autonomous_onset": True,
        "periodic_branch_is_fixed_reference_slice": True,
        "periodic_attraction_is_local_eta_zero": True,
        "periodic_attraction_refuses_biological_capture": True,
        "paper_iii_physical_bridge_still_conditional": True,
        "paper_iii_capture_gate_still_open": True,
    }
    parent_checks = _mapping(
        provenance.get("parent_claim_checks"), "parent_claim_checks"
    )
    if dict(parent_checks) != expected_parent_checks:
        raise ValueError("parent claim checks do not match the pinned inputs")

    expected_audits = {
        "composition_mismatch": {
            field: _audit_value(
                getattr(reference_composition_mismatch_audit(), field)
            )
            for field in CompositionMismatchAudit.__dataclass_fields__
        },
        "controlled_quadratic_transfer": {
            field: _audit_value(
                getattr(reference_controlled_quadratic_transfer_audit(), field)
            )
            for field in ControlledQuadraticTransferAudit.__dataclass_fields__
        },
    }
    if dict(exact_audits) != expected_audits:
        raise ValueError("exact_audits do not match the exact algebra")

    expected_scope = {
        field.removesuffix("_validated"): getattr(expected, field)
        for field in expected.__dataclass_fields__
        if field.endswith("_validated")
    }
    if dict(scope) != expected_scope:
        false_promotions = [
            key
            for key, value in expected_scope.items()
            if value is False and scope.get(key) is True
        ]
        if false_promotions:
            raise ValueError("an unforced, root, basin, or onset claim was promoted")
        raise ValueError("scope contains an unpinned or missing claim")
    return expected


__all__ = [
    "ARITHMETIC_DESCRIPTION",
    "ASSUMPTIONS_ID",
    "AUTONOMOUS_HANDOFF_RESULT_SHA256",
    "BALANCED_CONTROL_CHAIN_RESULT_SHA256",
    "BOUNDED_PREPARATION_RESULT_SHA256",
    "CompositionMismatchAudit",
    "ControlledQuadraticTransferAudit",
    "DEFAULT_COMMAND",
    "FIXED_EPSILON_BVP_RESULT_SHA256",
    "GENERATOR_RELATIVE_PATH",
    "MODEL_ID",
    "PERIODIC_ATTRACTION_RESULT_SHA256",
    "PERIODIC_BOX_RESULT_SHA256",
    "PHYSICAL_OUTER_BRIDGE_DOC_SHA256",
    "PROOF_SOURCE_RELATIVE_PATH",
    "QUADRATIC_CARRIER_RESULT_SHA256",
    "QUADRATIC_DOBRUSHIN_RESULT_SHA256",
    "QuadraticPhysicalOnsetStopGoCertificate",
    "ROBUST_HANDOFF_RESULT_SHA256",
    "UNFORCED_CAPTURE_DOC_SHA256",
    "reference_composition_mismatch_audit",
    "reference_controlled_quadratic_transfer_audit",
    "reference_stop_go_certificate",
    "stop_go_algebra_is_exact",
    "validate_stop_go_payload",
]
