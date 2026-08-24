"""Balanced-general-topology bounded FHN control chain.

This module composes three source-bound results and supplies the two algebraic
bridges that those results do not themselves claim:

* nonnegative row masses give ``||P-I||_inf <= 2`` and
  ``||B_0||_inf + ||B_1||_inf = 1`` for every finite balanced topology, so
  the fixed-topology exact-cancellation preparation bounds extend without a
  node-count or topology constant;
* the same balance identities make the synchronous subspace invariant and
  reduce every topology in the class to the tracked scalar two-delay model.

The initial-data set is a bounded cylinder, not a compact subset of the RFDE
phase space.  The resulting actuator statement is a bounded mathematical
exact-model additive feedback statement on declared state/history tubes.  It
is not a bandwidth, slew, energy, uncertainty, noisy-measurement, or hardware
robustness statement.  Frequency and amplitude refer only to the synchronous
periodic branch; asynchronous or arbitrary-history outputs are not defined.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import (
    Context,
    Decimal,
    InvalidOperation,
    ROUND_CEILING,
    localcontext,
)
from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Mapping

import sympy as sp

from canard_control.fhn_general_network_sign_cone import (
    validate_general_network_sign_cone_result_payload,
)
from canard_control.fhn_same_model_amplitude_safety import (
    validate_same_model_amplitude_safety_result_payload,
)


TRACKED_BOUNDED_PREPARATION_SHA256 = (
    "8681f800c42420207a94f505b3c8831c7409f3619cf640cbd24de580cd87f548"
)
TRACKED_GENERAL_SIGN_CONE_SHA256 = (
    "1dd606d7f4aec1ea857f1c53d4e60106fc2737089b67e989aa7b192fe3ca43fb"
)
TRACKED_AMPLITUDE_SAFETY_SHA256 = (
    "b9d00edd48c4ae5e61291dfd08fa13d6bb6775acf7f2683b69d3d2838130da36"
)
TRACKED_SEPARATOR_SHA256 = (
    "9e859f31c177638a70b3ca451fe743227308343792d77eeca286fca26afc8a86"
)
MODEL_ID = "balanced-general-topology-fhn-bounded-staged-control-chain"
ASSUMPTIONS_ID = (
    "N>=1;P>=0,P1=1;pi>0,pi^T1=1,pi^TP=pi^T;"
    "B_l>=0,B_l1=(1/2)1,pi^TB_l=(1/2)pi^T,l=0,1;"
    "D=3,E=2,epsilon=1/5,a=3/5,tau=(4sqrt5,5sqrt5)"
)
MAP_DEFINITION = "Q_A(kappa_1,kappa_3,r)=(F_sync,A_sync,-r)"
TRACKED_OUTPUT_BALL_RADIUS = (
    "2.75138166016477172021072951467987182906462947064987861e-15"
)


@dataclass(frozen=True)
class BalancedControlChainSourceEvidence:
    """Immutable digests of the three composed result records."""

    bounded_preparation_result_sha256: str
    general_sign_cone_result_sha256: str
    amplitude_safety_result_sha256: str


@dataclass(frozen=True)
class BalancedTwoDelayAudit:
    """Exact residuals and infinity norms for one rational topology."""

    node_count: int
    stationary_sum_residual: sp.Expr
    scaffold_row_mass_residual: sp.Matrix
    scaffold_stationarity_residual: sp.Matrix
    delay_0_row_mass_residual: sp.Matrix
    delay_1_row_mass_residual: sp.Matrix
    delay_0_stationarity_residual: sp.Matrix
    delay_1_stationarity_residual: sp.Matrix
    combined_delay_row_mass_residual: sp.Matrix
    combined_delay_stationarity_residual: sp.Matrix
    scaffold_entrywise_nonnegative: bool
    delay_layers_entrywise_nonnegative: bool
    stationary_weight_strictly_positive: bool
    scaffold_rank: int
    scaffold_infinity_norm: sp.Expr
    scaffold_minus_identity_infinity_norm: sp.Expr
    scaffold_minus_identity_two_bound_gap: sp.Expr
    delay_0_infinity_norm: sp.Expr
    delay_1_infinity_norm: sp.Expr
    delay_norm_sum: sp.Expr
    synchronous_scaffold_residual: sp.Matrix
    synchronous_delay_0_residual: sp.Matrix
    synchronous_delay_1_residual: sp.Matrix


@dataclass(frozen=True)
class BalancedControlAlgebra:
    """Exact cancellation and synchronous-restriction residuals."""

    node_count: int
    preparation_voltage_cancellation_residual: sp.Matrix
    preparation_recovery_cancellation_residual: sp.Matrix
    decision_recovery_cancellation_residual: sp.Matrix
    decision_voltage_input_residual: sp.Matrix
    synchronous_voltage_restriction_residual: sp.Matrix
    synchronous_recovery_restriction_residual: sp.Matrix


@dataclass(frozen=True)
class BalancedControlChainCertificate:
    """Public constants and a strict theorem/scope ledger."""

    bounded_preparation_result_sha256: str
    general_sign_cone_result_sha256: str
    amplitude_safety_result_sha256: str
    separator_result_sha256: str
    model_id: str
    assumptions_id: str
    map_definition: str
    epsilon: str
    unfolding: str
    voltage_scaffold: str
    recovery_scaffold: str
    scaled_delays: tuple[str, str]
    delay_row_masses: tuple[str, str]
    kappa_1_interval: tuple[str, str]
    kappa_3_interval: tuple[str, str]
    voltage_history_sup_bound: str
    recovery_current_sup_bound: str
    reset_abs_bound: str
    voltage_reaching_gain: str
    recovery_reaching_gain: str
    scaffold_infinity_norm: str
    scaffold_minus_identity_infinity_norm_upper: str
    delay_0_infinity_norm: str
    delay_1_infinity_norm: str
    delay_norm_sum: str
    voltage_input_authority_upper: str
    recovery_input_authority_upper: str
    settling_time_upper: str
    maximum_delay_hold_time_upper: str
    complete_history_preparation_time_upper: str
    decision_voltage_tube_abs_bound: str
    decision_recovery_input_authority_upper: str
    sign_cone_initial_mean_lower: str
    pulse_reset_projection: tuple[str, str]
    quiet_reset_projection: tuple[str, str]
    pulse_initial_mean_margin_over_sign_cone_lower: str
    quiet_initial_mean_margin_over_sign_cone_lower: str
    positive_detector_face: str
    negative_detector_face: str
    positive_excursion_face: str
    negative_excursion_face: str
    positive_detector_deadline_after_release_upper: str
    negative_detector_deadline_after_release_upper: str
    positive_excursion_deadline_after_release_upper: str
    negative_excursion_deadline_after_release_upper: str
    positive_detector_deadline_from_start_upper: str
    negative_detector_deadline_from_start_upper: str
    positive_excursion_deadline_from_start_upper: str
    negative_excursion_deadline_from_start_upper: str
    input_ball_radius: str
    output_ball_radius_lower: str
    pulse_input_center: tuple[str, str, str]
    quiet_input_center: tuple[str, str, str]
    output_order: tuple[str, str, str]
    exact_balanced_operator_identities_validated: bool
    arbitrary_finite_node_count_formula_validated: bool
    topology_and_node_count_independent_authority_validated: bool
    bounded_initial_data_cylinder_required: bool
    rfde_phase_space_compactness_validated: bool
    exact_model_additive_preparation_validated: bool
    finite_time_exact_complete_history_preparation_validated: bool
    state_overwrite_used: bool
    impulse_used: bool
    bounded_nodewise_recovery_cancellation_on_decision_tube_validated: bool
    voltage_preparation_feedback_closed_at_release: bool
    positive_controlled_onset_validated: bool
    negative_controlled_onset_validated: bool
    positive_finite_controlled_excursion_validated: bool
    negative_finite_controlled_excursion_validated: bool
    synchronous_subspace_invariance_validated: bool
    topology_independent_synchronous_scalar_restriction_validated: bool
    synchronous_branch_frequency_amplitude_outputs_validated: bool
    general_topology_synchronous_branch_three_output_balls_validated: bool
    unique_preimage_for_each_target_validated: bool
    end_to_end_staged_control_chain_validated: bool
    asynchronous_frequency_amplitude_outputs_validated: bool
    transverse_attraction_validated: bool
    full_network_periodic_attraction_validated: bool
    unforced_onset_validated: bool
    maximal_canard_onset_validated: bool
    biological_basin_validated: bool
    action_potential_validated: bool
    general_topology_canard_root_equivalence_validated: bool
    model_uncertainty_validated: bool
    measurement_noise_validated: bool
    bandwidth_validated: bool
    slew_rate_validated: bool
    energy_validated: bool
    hardware_validated: bool
    uniform_authority_on_unbounded_initial_data_validated: bool


def _mapping(value: object, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{name} must be a mapping")
    return value


def _matrix(value: object, name: str) -> sp.Matrix:
    try:
        matrix = sp.Matrix(value)
    except (TypeError, ValueError) as error:
        raise ValueError(f"{name} must be a rectangular matrix") from error
    if matrix.rows < 1 or matrix.cols < 1:
        raise ValueError(f"{name} must be nonempty")
    if not all(
        entry.is_number
        and entry.is_real is True
        and entry.is_finite is True
        for entry in matrix
    ):
        raise ValueError(f"{name} must have finite exact real entries")
    return matrix


def _stationary_row(value: object, node_count: int) -> sp.Matrix:
    row = _matrix(value, "stationary weight")
    if row.shape == (node_count, 1):
        row = row.T
    if row.shape != (1, node_count):
        raise ValueError("stationary weight must have one entry per node")
    return row


def _matrix_infinity_norm(matrix: sp.Matrix) -> sp.Expr:
    return max(
        sp.simplify(
            sum(abs(matrix[row, column]) for column in range(matrix.cols))
        )
        for row in range(matrix.rows)
    )


def _entrywise_nonnegative(matrix: sp.Matrix) -> bool:
    return all(entry.is_nonnegative is True for entry in matrix)


def balanced_two_delay_audit(
    scaffold: object,
    stationary_weight: object,
    delay_0: object,
    delay_1: object,
) -> BalancedTwoDelayAudit:
    """Return exact balance residuals for a two-half-layer topology."""

    p_matrix = _matrix(scaffold, "scaffold")
    if p_matrix.rows != p_matrix.cols:
        raise ValueError("scaffold must be square")
    node_count = p_matrix.rows
    pi = _stationary_row(stationary_weight, node_count)
    b_0 = _matrix(delay_0, "delay_0")
    b_1 = _matrix(delay_1, "delay_1")
    if b_0.shape != p_matrix.shape or b_1.shape != p_matrix.shape:
        raise ValueError("delay layers must match the scaffold shape")
    one = sp.ones(node_count, 1)
    half = sp.Rational(1, 2)
    identity = sp.eye(node_count)
    scaffold_difference = p_matrix - identity
    scaffold_difference_norm = _matrix_infinity_norm(scaffold_difference)
    return BalancedTwoDelayAudit(
        node_count=node_count,
        stationary_sum_residual=sp.simplify((pi * one)[0] - 1),
        scaffold_row_mass_residual=sp.ImmutableMatrix(p_matrix * one - one),
        scaffold_stationarity_residual=sp.ImmutableMatrix(pi * p_matrix - pi),
        delay_0_row_mass_residual=sp.ImmutableMatrix(
            b_0 * one - half * one
        ),
        delay_1_row_mass_residual=sp.ImmutableMatrix(
            b_1 * one - half * one
        ),
        delay_0_stationarity_residual=sp.ImmutableMatrix(
            pi * b_0 - half * pi
        ),
        delay_1_stationarity_residual=sp.ImmutableMatrix(
            pi * b_1 - half * pi
        ),
        combined_delay_row_mass_residual=sp.ImmutableMatrix(
            (b_0 + b_1) * one - one
        ),
        combined_delay_stationarity_residual=sp.ImmutableMatrix(
            pi * (b_0 + b_1) - pi
        ),
        scaffold_entrywise_nonnegative=_entrywise_nonnegative(p_matrix),
        delay_layers_entrywise_nonnegative=(
            _entrywise_nonnegative(b_0) and _entrywise_nonnegative(b_1)
        ),
        stationary_weight_strictly_positive=all(
            entry.is_positive is True for entry in pi
        ),
        scaffold_rank=int(p_matrix.rank()),
        scaffold_infinity_norm=_matrix_infinity_norm(p_matrix),
        scaffold_minus_identity_infinity_norm=scaffold_difference_norm,
        scaffold_minus_identity_two_bound_gap=sp.simplify(
            2 - scaffold_difference_norm
        ),
        delay_0_infinity_norm=_matrix_infinity_norm(b_0),
        delay_1_infinity_norm=_matrix_infinity_norm(b_1),
        delay_norm_sum=sp.simplify(
            _matrix_infinity_norm(b_0) + _matrix_infinity_norm(b_1)
        ),
        synchronous_scaffold_residual=sp.ImmutableMatrix(
            scaffold_difference * one
        ),
        synchronous_delay_0_residual=sp.ImmutableMatrix(
            b_0 * one - half * one
        ),
        synchronous_delay_1_residual=sp.ImmutableMatrix(
            b_1 * one - half * one
        ),
    )


def balanced_two_delay_audit_is_exact(audit: BalancedTwoDelayAudit) -> bool:
    """Return whether every defining identity and sharp norm fact holds."""

    zero_column = sp.zeros(audit.node_count, 1)
    zero_row = sp.zeros(1, audit.node_count)
    return (
        audit.stationary_sum_residual == 0
        and audit.scaffold_row_mass_residual == zero_column
        and audit.scaffold_stationarity_residual == zero_row
        and audit.delay_0_row_mass_residual == zero_column
        and audit.delay_1_row_mass_residual == zero_column
        and audit.delay_0_stationarity_residual == zero_row
        and audit.delay_1_stationarity_residual == zero_row
        and audit.combined_delay_row_mass_residual == zero_column
        and audit.combined_delay_stationarity_residual == zero_row
        and audit.scaffold_entrywise_nonnegative
        and audit.delay_layers_entrywise_nonnegative
        and audit.stationary_weight_strictly_positive
        and audit.scaffold_infinity_norm == 1
        and audit.scaffold_minus_identity_two_bound_gap.is_nonnegative is True
        and audit.delay_0_infinity_norm == sp.Rational(1, 2)
        and audit.delay_1_infinity_norm == sp.Rational(1, 2)
        and audit.delay_norm_sum == 1
        and audit.synchronous_scaffold_residual == zero_column
        and audit.synchronous_delay_0_residual == zero_column
        and audit.synchronous_delay_1_residual == zero_column
    )


def reference_balanced_two_delay_audits() -> tuple[BalancedTwoDelayAudit, ...]:
    """Audit scalar, non-rank-one, reducible, and cyclic exact examples."""

    half = sp.Rational(1, 2)
    scalar = sp.eye(1)
    scalar_audit = balanced_two_delay_audit(
        scalar, [1], scalar / 2, scalar / 2
    )

    pi_nonuniform = [sp.Rational(1, 6), sp.Rational(1, 3), half]
    nonrank = sp.Matrix(
        [
            [half, sp.Rational(1, 4), sp.Rational(1, 4)],
            [sp.Rational(1, 8), sp.Rational(5, 8), sp.Rational(1, 4)],
            [sp.Rational(1, 12), sp.Rational(1, 6), sp.Rational(3, 4)],
        ]
    )
    nonrank_audit = balanced_two_delay_audit(
        nonrank, pi_nonuniform, nonrank / 2, sp.eye(3) / 2
    )

    reducible = sp.Matrix(
        [
            [0, 1, 0, 0],
            [1, 0, 0, 0],
            [0, 0, 0, 1],
            [0, 0, 1, 0],
        ]
    )
    reducible_audit = balanced_two_delay_audit(
        reducible,
        [sp.Rational(1, 4)] * 4,
        reducible / 2,
        sp.eye(4) / 2,
    )

    cycle = sp.zeros(5)
    for row in range(5):
        cycle[row, (row + 1) % 5] = 1
    cycle_audit = balanced_two_delay_audit(
        cycle,
        [sp.Rational(1, 5)] * 5,
        cycle / 2,
        sp.eye(5) / 2,
    )
    return scalar_audit, nonrank_audit, reducible_audit, cycle_audit


def balanced_control_algebra(
    scaffold: object,
    stationary_weight: object,
    delay_0: object,
    delay_1: object,
) -> BalancedControlAlgebra:
    """Verify cancellation and scalar restriction for one exact topology."""

    audit = balanced_two_delay_audit(
        scaffold, stationary_weight, delay_0, delay_1
    )
    if not balanced_two_delay_audit_is_exact(audit):
        raise ValueError("topology does not satisfy the balanced two-delay class")
    p_matrix = _matrix(scaffold, "scaffold")
    b_0 = _matrix(delay_0, "delay_0")
    b_1 = _matrix(delay_1, "delay_1")
    node_count = p_matrix.rows
    one = sp.ones(node_count, 1)
    identity = sp.eye(node_count)
    v = sp.Matrix(sp.symbols(f"v_0:{node_count}", real=True))
    w = sp.Matrix(sp.symbols(f"w_0:{node_count}", real=True))
    delayed_0 = sp.Matrix(sp.symbols(f"d0_0:{node_count}", real=True))
    delayed_1 = sp.Matrix(sp.symbols(f"d1_0:{node_count}", real=True))
    sigma_v = sp.Matrix(sp.symbols(f"sv_0:{node_count}", real=True))
    sigma_w = sp.Matrix(sp.symbols(f"sw_0:{node_count}", real=True))
    epsilon, unfolding, kappa_1, kappa_3, k_v, k_w = sp.symbols(
        "epsilon unfolding kappa_1 kappa_3 K_v K_w", real=True
    )
    voltage_scaffold, recovery_scaffold = sp.symbols("D E", real=True)

    def shifted_cube(vector: sp.Matrix) -> sp.Matrix:
        return vector.applyfunc(lambda item: (item - 1) ** 3)

    baseline_voltage = (
        v
        - v.applyfunc(lambda item: item**3) / 3
        - w
        + voltage_scaffold * (p_matrix - identity) * v
        + epsilon
        * kappa_1
        * (b_0 * delayed_0 + b_1 * delayed_1 - v)
        + epsilon
        * kappa_3
        * (
            b_0 * shifted_cube(delayed_0)
            + b_1 * shifted_cube(delayed_1)
            - shifted_cube(v)
        )
    )
    baseline_recovery = (
        epsilon * (v - unfolding * one)
        + recovery_scaffold * (p_matrix - identity) * w
    )
    preparation_voltage_input = -baseline_voltage - k_v * sigma_v
    preparation_recovery_input = -baseline_recovery - k_w * sigma_w
    decision_recovery_input = -baseline_recovery

    scalar_current, scalar_recovery, scalar_delay_0, scalar_delay_1 = sp.symbols(
        "s q s_0 s_1", real=True
    )
    synchronized_voltage = baseline_voltage.subs(
        {
            **{v[index]: scalar_current for index in range(node_count)},
            **{w[index]: scalar_recovery for index in range(node_count)},
            **{
                delayed_0[index]: scalar_delay_0
                for index in range(node_count)
            },
            **{
                delayed_1[index]: scalar_delay_1
                for index in range(node_count)
            },
        }
    )
    h_current = (scalar_current - 1) ** 3
    scalar_voltage = (
        scalar_current
        - scalar_current**3 / 3
        - scalar_recovery
        + epsilon
        * kappa_1
        * (sp.Rational(1, 2) * scalar_delay_0
           + sp.Rational(1, 2) * scalar_delay_1
           - scalar_current)
        + epsilon
        * kappa_3
        * (sp.Rational(1, 2) * (scalar_delay_0 - 1) ** 3
           + sp.Rational(1, 2) * (scalar_delay_1 - 1) ** 3
           - h_current)
    )
    synchronized_recovery = baseline_recovery.subs(
        {
            **{v[index]: scalar_current for index in range(node_count)},
            **{w[index]: scalar_recovery for index in range(node_count)},
        }
    )
    scalar_recovery_rhs = epsilon * (scalar_current - unfolding)
    return BalancedControlAlgebra(
        node_count=node_count,
        preparation_voltage_cancellation_residual=sp.simplify(
            baseline_voltage + preparation_voltage_input + k_v * sigma_v
        ),
        preparation_recovery_cancellation_residual=sp.simplify(
            baseline_recovery + preparation_recovery_input + k_w * sigma_w
        ),
        decision_recovery_cancellation_residual=sp.simplify(
            baseline_recovery + decision_recovery_input
        ),
        decision_voltage_input_residual=sp.zeros(node_count, 1),
        synchronous_voltage_restriction_residual=sp.simplify(
            synchronized_voltage - scalar_voltage * one
        ),
        synchronous_recovery_restriction_residual=sp.simplify(
            synchronized_recovery - scalar_recovery_rhs * one
        ),
    )


def _require_true(mapping: Mapping[str, Any], key: str) -> None:
    if mapping.get(key) is not True:
        raise ValueError(f"required proof flag {key!r} must be true")


def _require_false(mapping: Mapping[str, Any], key: str) -> None:
    if mapping.get(key) is not False:
        raise ValueError(f"scope flag {key!r} must be false")


def _decimal(value: object, name: str) -> Decimal:
    if not isinstance(value, str):
        raise ValueError(f"{name} must be a decimal string")
    try:
        number = Decimal(value)
    except InvalidOperation as error:
        raise ValueError(f"{name} is not a decimal") from error
    if not number.is_finite():
        raise ValueError(f"{name} must be finite")
    return number


def _validate_preparation_payload(
    payload: Mapping[str, Any],
) -> Mapping[str, Any]:
    root = _mapping(payload, "bounded-preparation result")
    certificate = _mapping(root.get("certificate"), "preparation certificate")
    scope = _mapping(root.get("scope"), "preparation scope")
    evidence = _mapping(root.get("source_evidence"), "preparation evidence")
    if evidence.get("separator_result_sha256") != TRACKED_SEPARATOR_SHA256:
        raise ValueError("bounded preparation uses a different separator")
    expected_values = {
        "epsilon": "1/5",
        "unfolding": "3/5",
        "voltage_scaffold": "3",
        "recovery_scaffold": "2",
        "scaled_delays": ["4", "5"],
        "voltage_history_sup_bound": "2",
        "recovery_current_sup_bound": "2",
        "reset_abs_bound": "0.75",
        "voltage_reaching_gain": "1",
        "recovery_reaching_gain": "1",
        "reachable_voltage_sup_bound": "2",
        "reachable_recovery_sup_bound": "2",
        "averaging_operator_sup_norm": "1",
        "each_delay_operator_sup_norm": "1/2",
    }
    for key, expected in expected_values.items():
        if certificate.get(key) != expected:
            raise ValueError(f"bounded preparation constant changed: {key}")
    for key in (
        "finite_time_exact_state_preparation",
        "maximum_delay_hold_produces_exact_complete_history",
        "bounded_additive_input_on_declared_bounded_cylinder",
        "bounded_initial_data_cylinder_required",
        "input_bound_independent_of_node_count",
        "exact_model_cancellation_required",
        "optional_nodewise_recovery_cancellation_exact",
        "optional_nodewise_zero_recovery_leaf_invariant",
        "optional_nodewise_voltage_dynamics_preserved",
    ):
        _require_true(certificate, key)
    for key in (
        "rfde_phase_space_compactness_validated",
        "general_network_topology_validated",
        "hardware_implementation_validated",
        "bandwidth_validated",
        "model_uncertainty_validated",
        "measurement_noise_validated",
    ):
        _require_false(certificate, key)
    _require_true(
        scope,
        "bounded_additive_finite_time_preparation_on_declared_bounded_cylinder",
    )
    _require_false(scope, "rfde_phase_space_compactness")
    _require_false(scope, "general_network_topology")
    return certificate


def _validate_cross_sources(
    preparation_payload: Mapping[str, Any],
    sign_cone_payload: Mapping[str, Any],
    amplitude_safety_payload: Mapping[str, Any],
    evidence: BalancedControlChainSourceEvidence,
) -> tuple[Mapping[str, Any], Mapping[str, Any], Mapping[str, Any]]:
    expected_digests = {
        "bounded_preparation_result_sha256": (
            TRACKED_BOUNDED_PREPARATION_SHA256
        ),
        "general_sign_cone_result_sha256": TRACKED_GENERAL_SIGN_CONE_SHA256,
        "amplitude_safety_result_sha256": TRACKED_AMPLITUDE_SAFETY_SHA256,
    }
    for field, expected in expected_digests.items():
        if getattr(evidence, field) != expected:
            raise ValueError(f"source evidence digest is invalid: {field}")
    preparation = _validate_preparation_payload(preparation_payload)
    validate_general_network_sign_cone_result_payload(sign_cone_payload)
    validate_same_model_amplitude_safety_result_payload(
        amplitude_safety_payload
    )
    sign = _mapping(sign_cone_payload.get("certificate"), "sign certificate")
    amplitude = _mapping(
        amplitude_safety_payload.get("certificate"), "amplitude certificate"
    )
    if sign.get("separator_result_sha256") != TRACKED_SEPARATOR_SHA256:
        raise ValueError("sign-cone result uses a different separator")
    if amplitude.get("separator_result_sha256") != TRACKED_SEPARATOR_SHA256:
        raise ValueError("amplitude-safety result uses a different separator")
    if sign.get("epsilon") != "0.2" or preparation.get("epsilon") != "1/5":
        raise ValueError("epsilon constants do not represent 1/5")
    if sign.get("voltage_scaffold") != preparation.get("voltage_scaffold"):
        raise ValueError("voltage scaffold constants disagree")
    if sign.get("reference_scaled_delays") != preparation.get("scaled_delays"):
        raise ValueError("delay pairs disagree")
    if sign.get("reference_delay_weights") != ["0.5", "0.5"]:
        raise ValueError("sign-cone source is not the two-half-layer theorem")
    for key in ("kappa_1_interval", "kappa_3_interval"):
        if sign.get(key) != preparation.get(key):
            raise ValueError(f"gain boxes disagree: {key}")
    if amplitude.get("map_definition") != (
        "Q_A(kappa_1,kappa_3,r)=(F,A,-r)"
    ):
        raise ValueError("amplitude-safety map definition changed")
    return preparation, sign, amplitude


def _ceiling_context() -> Context:
    return Context(prec=110, rounding=ROUND_CEILING)


def _add_upper(left: str, right: str) -> str:
    context = _ceiling_context()
    return format(
        context.add(_decimal(left, "left upper"), _decimal(right, "right upper")),
        "f",
    )


def balanced_control_chain_from_payloads(
    preparation_payload: Mapping[str, Any],
    sign_cone_payload: Mapping[str, Any],
    amplitude_safety_payload: Mapping[str, Any],
    evidence: BalancedControlChainSourceEvidence,
) -> BalancedControlChainCertificate:
    """Compose the source records after proving the two topology bridges."""

    preparation, sign, amplitude = _validate_cross_sources(
        preparation_payload,
        sign_cone_payload,
        amplitude_safety_payload,
        evidence,
    )
    audits = reference_balanced_two_delay_audits()
    if not all(balanced_two_delay_audit_is_exact(audit) for audit in audits):
        raise RuntimeError("balanced reference topology audit failed")
    if not (
        audits[1].scaffold_rank > 1
        and audits[2].scaffold_rank > 1
        and audits[3].scaffold_minus_identity_infinity_norm == 2
    ):
        raise RuntimeError("reference topologies miss a hostile topology case")

    # Every reference topology must also give exact preparation cancellation,
    # bounded-decision recovery cancellation, and the tracked scalar restriction.
    half = sp.Rational(1, 2)
    exact_topologies: tuple[tuple[sp.Matrix, list[sp.Expr]], ...] = (
        (sp.eye(1), [sp.Integer(1)]),
        (
            sp.Matrix(
                [
                    [half, sp.Rational(1, 4), sp.Rational(1, 4)],
                    [sp.Rational(1, 8), sp.Rational(5, 8), sp.Rational(1, 4)],
                    [sp.Rational(1, 12), sp.Rational(1, 6), sp.Rational(3, 4)],
                ]
            ),
            [sp.Rational(1, 6), sp.Rational(1, 3), half],
        ),
        (
            sp.Matrix(
                [
                    [0, 1, 0, 0],
                    [1, 0, 0, 0],
                    [0, 0, 0, 1],
                    [0, 0, 1, 0],
                ]
            ),
            [sp.Rational(1, 4)] * 4,
        ),
    )
    algebra_records = tuple(
        balanced_control_algebra(p_matrix, pi, p_matrix / 2, sp.eye(p_matrix.rows) / 2)
        for p_matrix, pi in exact_topologies
    )
    for algebra in algebra_records:
        zero = sp.zeros(algebra.node_count, 1)
        if not all(
            residual == zero
            for residual in (
                algebra.preparation_voltage_cancellation_residual,
                algebra.preparation_recovery_cancellation_residual,
                algebra.decision_recovery_cancellation_residual,
                algebra.decision_voltage_input_residual,
                algebra.synchronous_voltage_restriction_residual,
                algebra.synchronous_recovery_restriction_residual,
            )
        ):
            raise RuntimeError("balanced control algebra audit failed")

    context = _ceiling_context()
    with localcontext(context):
        v_bound = Decimal(2)
        w_bound = Decimal(2)
        reset_bound = Decimal("0.75")
        epsilon = Decimal(1) / Decimal(5)
        unfolding = Decimal(3) / Decimal(5)
        kappa_1_upper = _decimal(
            sign["kappa_1_interval"][1], "kappa_1 upper"
        )
        kappa_3_upper = _decimal(
            sign["kappa_3_interval"][1], "kappa_3 upper"
        )
        reaching_voltage = (v_bound + reset_bound).sqrt()
        reaching_recovery = w_bound.sqrt()
        voltage_formula = (
            v_bound
            + v_bound**3 / Decimal(3)
            + w_bound
            + Decimal(2) * Decimal(3) * v_bound
            + Decimal(2) * epsilon * kappa_1_upper * v_bound
            + Decimal(2) * epsilon * kappa_3_upper * (v_bound + 1) ** 3
            + reaching_voltage
        )
        recovery_formula = (
            epsilon * (v_bound + unfolding)
            + Decimal(2) * Decimal(2) * w_bound
            + reaching_recovery
        )
    voltage_authority = _decimal(
        preparation.get("voltage_input_authority_upper"),
        "voltage authority",
    )
    recovery_authority = _decimal(
        preparation.get("recovery_input_authority_upper"),
        "recovery authority",
    )
    if voltage_authority < voltage_formula:
        raise ValueError("preparation voltage authority is below the universal bound")
    if recovery_authority < recovery_formula:
        raise ValueError("preparation recovery authority is below the universal bound")

    with localcontext(context):
        decision_tube = Decimal("1.5")
        decision_formula = epsilon * (decision_tube + unfolding)
    decision_authority = _decimal(
        preparation.get("optional_nodewise_recovery_authority_upper"),
        "decision recovery authority",
    )
    if decision_authority < decision_formula:
        raise ValueError("nodewise decision authority is too small")

    pulse = _mapping(amplitude.get("pulse_side_chart"), "pulse chart")
    quiet = _mapping(amplitude.get("quiet_side_chart"), "quiet chart")
    pulse_lower = _decimal(pulse.get("reset_projection_lower"), "pulse lower")
    pulse_upper = _decimal(pulse.get("reset_projection_upper"), "pulse upper")
    quiet_lower = _decimal(quiet.get("reset_projection_lower"), "quiet lower")
    quiet_upper = _decimal(quiet.get("reset_projection_upper"), "quiet upper")
    sign_mean_lower = _decimal(
        sign.get("declared_initial_mean_magnitude_lower"), "sign mean lower"
    )
    if not (
        Decimal(0) < sign_mean_lower <= pulse_lower <= pulse_upper < reset_bound
    ):
        raise ValueError("pulse chart is not inside the preparation/sign cone")
    if not (
        -reset_bound < quiet_lower <= quiet_upper <= -sign_mean_lower < Decimal(0)
    ):
        raise ValueError("quiet chart is not inside the preparation/sign cone")
    output_radius = _decimal(
        amplitude.get("certified_output_ball_radius_lower"),
        "output ball radius",
    )
    if output_radius <= 0:
        raise ValueError("the three-output radius must be positive")
    for flag in (
        "frequency_amplitude_operational_safety_target_ball_validated",
        "unique_input_for_each_certified_target_validated",
        "translated_input_balls_contained_validated",
    ):
        _require_true(amplitude, flag)

    prep_time = preparation["complete_history_preparation_time_upper"]
    positive_detector = sign["positive_detector_deadline_upper"]
    negative_detector = sign["negative_detector_deadline_upper"]
    positive_excursion = sign["positive_excursion_deadline_upper"]
    negative_excursion = sign["negative_excursion_deadline_upper"]
    return BalancedControlChainCertificate(
        bounded_preparation_result_sha256=(
            evidence.bounded_preparation_result_sha256
        ),
        general_sign_cone_result_sha256=evidence.general_sign_cone_result_sha256,
        amplitude_safety_result_sha256=evidence.amplitude_safety_result_sha256,
        separator_result_sha256=TRACKED_SEPARATOR_SHA256,
        model_id=MODEL_ID,
        assumptions_id=ASSUMPTIONS_ID,
        map_definition=MAP_DEFINITION,
        epsilon="1/5",
        unfolding="3/5",
        voltage_scaffold="3",
        recovery_scaffold="2",
        scaled_delays=("4", "5"),
        delay_row_masses=("1/2", "1/2"),
        kappa_1_interval=tuple(sign["kappa_1_interval"]),
        kappa_3_interval=tuple(sign["kappa_3_interval"]),
        voltage_history_sup_bound="2",
        recovery_current_sup_bound="2",
        reset_abs_bound="0.75",
        voltage_reaching_gain="1",
        recovery_reaching_gain="1",
        scaffold_infinity_norm="1",
        scaffold_minus_identity_infinity_norm_upper="2",
        delay_0_infinity_norm="1/2",
        delay_1_infinity_norm="1/2",
        delay_norm_sum="1",
        voltage_input_authority_upper=str(voltage_authority),
        recovery_input_authority_upper=str(recovery_authority),
        settling_time_upper=preparation["settling_time_upper"],
        maximum_delay_hold_time_upper=preparation[
            "exact_history_hold_time_upper"
        ],
        complete_history_preparation_time_upper=prep_time,
        decision_voltage_tube_abs_bound="1.5",
        decision_recovery_input_authority_upper=str(decision_authority),
        sign_cone_initial_mean_lower=str(sign_mean_lower),
        pulse_reset_projection=(str(pulse_lower), str(pulse_upper)),
        quiet_reset_projection=(str(quiet_lower), str(quiet_upper)),
        pulse_initial_mean_margin_over_sign_cone_lower=str(
            pulse_lower - sign_mean_lower
        ),
        quiet_initial_mean_margin_over_sign_cone_lower=str(
            abs(quiet_upper) - sign_mean_lower
        ),
        positive_detector_face="1",
        negative_detector_face="-1",
        positive_excursion_face=sign["positive_excursion_face"],
        negative_excursion_face=sign["negative_excursion_face"],
        positive_detector_deadline_after_release_upper=positive_detector,
        negative_detector_deadline_after_release_upper=negative_detector,
        positive_excursion_deadline_after_release_upper=positive_excursion,
        negative_excursion_deadline_after_release_upper=negative_excursion,
        positive_detector_deadline_from_start_upper=_add_upper(
            prep_time, positive_detector
        ),
        negative_detector_deadline_from_start_upper=_add_upper(
            prep_time, negative_detector
        ),
        positive_excursion_deadline_from_start_upper=_add_upper(
            prep_time, positive_excursion
        ),
        negative_excursion_deadline_from_start_upper=_add_upper(
            prep_time, negative_excursion
        ),
        input_ball_radius=amplitude["exact_input_ball_radius"],
        output_ball_radius_lower=amplitude[
            "certified_output_ball_radius_lower"
        ],
        pulse_input_center=tuple(pulse["input_center"]),
        quiet_input_center=tuple(quiet["input_center"]),
        output_order=("F_sync", "A_sync=V_max-V_min", "S_op=-r"),
        exact_balanced_operator_identities_validated=True,
        arbitrary_finite_node_count_formula_validated=True,
        topology_and_node_count_independent_authority_validated=True,
        bounded_initial_data_cylinder_required=True,
        rfde_phase_space_compactness_validated=False,
        exact_model_additive_preparation_validated=True,
        finite_time_exact_complete_history_preparation_validated=True,
        state_overwrite_used=False,
        impulse_used=False,
        bounded_nodewise_recovery_cancellation_on_decision_tube_validated=True,
        voltage_preparation_feedback_closed_at_release=True,
        positive_controlled_onset_validated=True,
        negative_controlled_onset_validated=True,
        positive_finite_controlled_excursion_validated=True,
        negative_finite_controlled_excursion_validated=True,
        synchronous_subspace_invariance_validated=True,
        topology_independent_synchronous_scalar_restriction_validated=True,
        synchronous_branch_frequency_amplitude_outputs_validated=True,
        general_topology_synchronous_branch_three_output_balls_validated=True,
        unique_preimage_for_each_target_validated=True,
        end_to_end_staged_control_chain_validated=True,
        asynchronous_frequency_amplitude_outputs_validated=False,
        transverse_attraction_validated=False,
        full_network_periodic_attraction_validated=False,
        unforced_onset_validated=False,
        maximal_canard_onset_validated=False,
        biological_basin_validated=False,
        action_potential_validated=False,
        general_topology_canard_root_equivalence_validated=False,
        model_uncertainty_validated=False,
        measurement_noise_validated=False,
        bandwidth_validated=False,
        slew_rate_validated=False,
        energy_validated=False,
        hardware_validated=False,
        uniform_authority_on_unbounded_initial_data_validated=False,
    )


_TRUE_CERTIFICATE_FLAGS = (
    "exact_balanced_operator_identities_validated",
    "arbitrary_finite_node_count_formula_validated",
    "topology_and_node_count_independent_authority_validated",
    "bounded_initial_data_cylinder_required",
    "exact_model_additive_preparation_validated",
    "finite_time_exact_complete_history_preparation_validated",
    "bounded_nodewise_recovery_cancellation_on_decision_tube_validated",
    "voltage_preparation_feedback_closed_at_release",
    "positive_controlled_onset_validated",
    "negative_controlled_onset_validated",
    "positive_finite_controlled_excursion_validated",
    "negative_finite_controlled_excursion_validated",
    "synchronous_subspace_invariance_validated",
    "topology_independent_synchronous_scalar_restriction_validated",
    "synchronous_branch_frequency_amplitude_outputs_validated",
    "general_topology_synchronous_branch_three_output_balls_validated",
    "unique_preimage_for_each_target_validated",
    "end_to_end_staged_control_chain_validated",
)
_FALSE_CERTIFICATE_FLAGS = (
    "rfde_phase_space_compactness_validated",
    "state_overwrite_used",
    "impulse_used",
    "asynchronous_frequency_amplitude_outputs_validated",
    "transverse_attraction_validated",
    "full_network_periodic_attraction_validated",
    "unforced_onset_validated",
    "maximal_canard_onset_validated",
    "biological_basin_validated",
    "action_potential_validated",
    "general_topology_canard_root_equivalence_validated",
    "model_uncertainty_validated",
    "measurement_noise_validated",
    "bandwidth_validated",
    "slew_rate_validated",
    "energy_validated",
    "hardware_validated",
    "uniform_authority_on_unbounded_initial_data_validated",
)
_TRUE_SCOPE_FLAGS = (
    "balanced_general_topology_bounded_additive_preparation_on_declared_bounded_initial_data_cylinder",
    "exact_complete_history_phi_r_after_finite_preparation",
    "bounded_mathematical_additive_actuator_on_declared_preparation_cylinder",
    "bounded_nodewise_recovery_cancellation_on_declared_decision_tube",
    "balanced_general_topology_controlled_positive_and_negative_onset",
    "balanced_general_topology_controlled_finite_excursion",
    "topology_independent_synchronous_branch_frequency_amplitude_outputs",
    "general_topology_synchronous_branch_frequency_amplitude_operational_safety_target_balls",
    "unique_preimage_in_each_translated_input_ball",
    "end_to_end_staged_control_chain",
)
_FALSE_SCOPE_FLAGS = (
    "rfde_phase_space_compactness",
    "uniform_authority_on_unbounded_initial_data",
    "asynchronous_frequency_amplitude_outputs",
    "transverse_attraction",
    "full_network_periodic_attraction",
    "unforced_onset",
    "maximal_canard_onset",
    "biological_basin",
    "action_potential",
    "general_topology_canard_root_equivalence",
    "model_uncertainty",
    "measurement_noise",
    "bandwidth",
    "slew_rate",
    "energy",
    "hardware",
)


def validate_balanced_control_chain_result_payload(
    payload: Mapping[str, Any],
) -> None:
    """Reject missing bridges, forged constants, and scope promotions."""

    root = _mapping(payload, "balanced control-chain result")
    evidence = _mapping(root.get("source_evidence"), "source evidence")
    certificate = _mapping(root.get("certificate"), "certificate")
    scope = _mapping(root.get("scope"), "scope")
    expected = {
        "bounded_preparation_result_sha256": (
            TRACKED_BOUNDED_PREPARATION_SHA256
        ),
        "general_sign_cone_result_sha256": TRACKED_GENERAL_SIGN_CONE_SHA256,
        "amplitude_safety_result_sha256": TRACKED_AMPLITUDE_SAFETY_SHA256,
    }
    for key, digest in expected.items():
        if evidence.get(key) != digest or certificate.get(key) != digest:
            raise ValueError(f"result source digest is invalid: {key}")
    if certificate.get("separator_result_sha256") != TRACKED_SEPARATOR_SHA256:
        raise ValueError("result separator digest is invalid")
    if certificate.get("model_id") != MODEL_ID:
        raise ValueError("result model identifier is invalid")
    if certificate.get("assumptions_id") != ASSUMPTIONS_ID:
        raise ValueError("result topology assumptions are invalid")
    if certificate.get("map_definition") != MAP_DEFINITION:
        raise ValueError("result staged map is invalid")
    exact_values = {
        "epsilon": "1/5",
        "unfolding": "3/5",
        "voltage_scaffold": "3",
        "recovery_scaffold": "2",
        "scaled_delays": ["4", "5"],
        "delay_row_masses": ["1/2", "1/2"],
        "voltage_history_sup_bound": "2",
        "recovery_current_sup_bound": "2",
        "reset_abs_bound": "0.75",
        "scaffold_infinity_norm": "1",
        "scaffold_minus_identity_infinity_norm_upper": "2",
        "delay_0_infinity_norm": "1/2",
        "delay_1_infinity_norm": "1/2",
        "delay_norm_sum": "1",
        "decision_voltage_tube_abs_bound": "1.5",
        "input_ball_radius": "1e-12",
        "output_order": ["F_sync", "A_sync=V_max-V_min", "S_op=-r"],
    }
    for key, wanted in exact_values.items():
        if certificate.get(key) != wanted:
            raise ValueError(f"result constant is invalid: {key}")
    if _decimal(
        certificate.get("output_ball_radius_lower"), "output radius"
    ) != Decimal(TRACKED_OUTPUT_BALL_RADIUS):
        raise ValueError("result output radius is invalid")
    voltage_authority = _decimal(
        certificate.get("voltage_input_authority_upper"),
        "voltage authority",
    )
    recovery_authority = _decimal(
        certificate.get("recovery_input_authority_upper"),
        "recovery authority",
    )
    decision_authority = _decimal(
        certificate.get("decision_recovery_input_authority_upper"),
        "decision authority",
    )
    if not (
        voltage_authority < Decimal("23.19")
        and recovery_authority < Decimal("9.94")
        and Decimal("0.42") <= decision_authority < Decimal("0.421")
    ):
        raise ValueError("result authority bounds are invalid")
    if decision_authority < Decimal("0.42"):
        raise ValueError("result decision authority is too small")
    if certificate.get("pulse_reset_projection") != [
        "0.499999999999",
        "0.500000000001",
    ]:
        raise ValueError("result pulse reset projection is invalid")
    if certificate.get("quiet_reset_projection") != [
        "-0.500000000001",
        "-0.499999999999",
    ]:
        raise ValueError("result quiet reset projection is invalid")
    if certificate.get("pulse_input_center") != ["0.2", "0.25", "0.5"]:
        raise ValueError("result pulse input center is invalid")
    if certificate.get("quiet_input_center") != ["0.2", "0.25", "-0.5"]:
        raise ValueError("result quiet input center is invalid")
    if certificate.get("sign_cone_initial_mean_lower") != "0.06":
        raise ValueError("result sign-cone lower mean is invalid")
    expected_faces = {
        "positive_detector_face": "1",
        "negative_detector_face": "-1",
        "positive_excursion_face": "1.5",
        "negative_excursion_face": "-1.2",
    }
    for key, wanted in expected_faces.items():
        if certificate.get(key) != wanted:
            raise ValueError(f"result face is invalid: {key}")
    preparation_time = _decimal(
        certificate.get("complete_history_preparation_time_upper"),
        "preparation time",
    )
    deadline_pairs = (
        (
            "positive_detector_deadline_after_release_upper",
            "positive_detector_deadline_from_start_upper",
        ),
        (
            "negative_detector_deadline_after_release_upper",
            "negative_detector_deadline_from_start_upper",
        ),
        (
            "positive_excursion_deadline_after_release_upper",
            "positive_excursion_deadline_from_start_upper",
        ),
        (
            "negative_excursion_deadline_after_release_upper",
            "negative_excursion_deadline_from_start_upper",
        ),
    )
    with localcontext(_ceiling_context()):
        for after_key, start_key in deadline_pairs:
            after = _decimal(certificate.get(after_key), after_key)
            start = _decimal(certificate.get(start_key), start_key)
            if after <= 0 or start < preparation_time + after:
                raise ValueError(f"result deadline composition is invalid: {start_key}")
    for key in _TRUE_CERTIFICATE_FLAGS:
        _require_true(certificate, key)
    for key in _FALSE_CERTIFICATE_FLAGS:
        _require_false(certificate, key)
    if set(scope) != set(_TRUE_SCOPE_FLAGS) | set(_FALSE_SCOPE_FLAGS):
        raise ValueError("result scope keys are missing or unexpected")
    for key in _TRUE_SCOPE_FLAGS:
        _require_true(scope, key)
    for key in _FALSE_SCOPE_FLAGS:
        _require_false(scope, key)


def load_balanced_control_chain_result(
    path: str | Path,
    *,
    expected_sha256: str,
) -> Mapping[str, Any]:
    """Hash-check and semantically validate the composed result."""

    if not isinstance(expected_sha256, str) or len(expected_sha256) != 64:
        raise ValueError("expected_sha256 must be a 64-character digest")
    raw = Path(path).read_bytes()
    digest = sha256(raw).hexdigest()
    if digest != expected_sha256:
        raise ValueError(
            "balanced control-chain result SHA-256 mismatch: "
            f"expected {expected_sha256}, got {digest}"
        )
    try:
        payload = json.loads(raw)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError("balanced control-chain result is not UTF-8 JSON") from error
    validate_balanced_control_chain_result_payload(payload)
    return _mapping(payload, "balanced control-chain result")


__all__ = [
    "ASSUMPTIONS_ID",
    "BalancedControlAlgebra",
    "BalancedControlChainCertificate",
    "BalancedControlChainSourceEvidence",
    "BalancedTwoDelayAudit",
    "MAP_DEFINITION",
    "MODEL_ID",
    "TRACKED_AMPLITUDE_SAFETY_SHA256",
    "TRACKED_BOUNDED_PREPARATION_SHA256",
    "TRACKED_GENERAL_SIGN_CONE_SHA256",
    "balanced_control_algebra",
    "balanced_control_chain_from_payloads",
    "balanced_two_delay_audit",
    "balanced_two_delay_audit_is_exact",
    "load_balanced_control_chain_result",
    "reference_balanced_two_delay_audits",
    "validate_balanced_control_chain_result_payload",
]
