"""Bounded additive finite-time preparation for the fixed FHN network.

The earlier causal-hold note creates a constant complete history by an ideal
state overwrite. Here the initial voltage history and the current recovery
state are restricted to a declared bounded initial-data cylinder. Exact causal
cancellation of the baseline right-hand side, followed by a componentwise
square-root reaching law, gives a bounded additive preparation input on that
cylinder. No compactness in the infinite-dimensional RFDE phase-space topology
is used or claimed.

The square-root field is continuous but not locally Lipschitz at zero.
Forward uniqueness is instead supplied by monotonicity: sigma_1/2 is
increasing, so x -> -K sigma_1/2(x) is one-sided Lipschitz with constant zero.
The result is only forward uniqueness; no backward uniqueness is claimed.

This is a mathematical exact-model cancellation theorem. It requires every
current node state and both delayed voltage layers. It proves neither a
bandwidth, slew, energy, uncertainty, noisy-measurement, nor hardware theorem.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from hashlib import sha256
import json
import math
from pathlib import Path
from typing import Any, Mapping

import gmpy2
import sympy as sp

from canard_control.directed_interval import DirectedInterval, decimal_upper
from canard_control.fhn_same_model_separator import (
    FULL_NETWORK_INSTANCE_ID,
    SYNCHRONOUS_MODEL_ID,
    validate_same_model_separator_result_payload,
)


TRACKED_SEPARATOR_RESULT_SHA256 = (
    "9e859f31c177638a70b3ca451fe743227308343792d77eeca286fca26afc8a86"
)
TRACKED_CAUSAL_HOLD_NOTE_SHA256 = (
    "1f68aed9409bf4e04799903993b77b1d939b7f39e588f887cb54aec7f9aa459e"
)
PREPARATION_PROTOCOL_ID = (
    "exact-cancellation-componentwise-sigma-half-finite-time-preparation"
)


@dataclass(frozen=True)
class BoundedPreparationSourceEvidence:
    """Byte and model identity of the two prior records used here."""

    separator_result_sha256: str
    causal_hold_note_sha256: str
    source_synchronous_model_id: str
    full_network_instance_id: str


@dataclass(frozen=True)
class PreparationNetworkAlgebra:
    """Exact finite-node identities behind the size-independent theorem."""

    module_sizes: tuple[int, int]
    averaging_matrix: sp.Matrix
    same_module_delay_matrix: sp.Matrix
    cross_module_delay_matrix: sp.Matrix
    delay_sum_residual: sp.Matrix
    averaging_row_sums: tuple[sp.Expr, ...]
    same_delay_row_sums: tuple[sp.Expr, ...]
    cross_delay_row_sums: tuple[sp.Expr, ...]
    averaging_sup_norm: sp.Expr
    same_delay_sup_norm: sp.Expr
    cross_delay_sup_norm: sp.Expr
    scaffold_sup_norm: sp.Expr
    scaffold_strict_two_gap: sp.Expr
    voltage_cancellation_residual: sp.Matrix
    recovery_cancellation_residual: sp.Matrix
    nodewise_decision_recovery_residual: sp.Matrix
    nodewise_decision_voltage_preservation_residual: sp.Matrix


@dataclass(frozen=True)
class BoundedAdditivePreparationCertificate:
    """Directed authority, time, and exact-scope ledger."""

    separator_result_sha256: str
    causal_hold_note_sha256: str
    protocol_id: str
    source_synchronous_model_id: str
    certified_full_network_instance_id: str
    precision_bits: int
    epsilon: str
    unfolding: str
    voltage_scaffold: str
    recovery_scaffold: str
    scaled_delays: tuple[str, str]
    maximum_physical_delay_upper: str
    kappa_1_interval: tuple[str, str]
    kappa_3_interval: tuple[str, str]
    voltage_history_sup_bound: str
    recovery_current_sup_bound: str
    reset_abs_bound: str
    voltage_reaching_gain: str
    recovery_reaching_gain: str
    decision_voltage_tube_bound: str
    reachable_voltage_sup_bound: str
    reachable_recovery_sup_bound: str
    voltage_initial_error_sup_bound: str
    averaging_operator_sup_norm: str
    each_delay_operator_sup_norm: str
    scaffold_operator_sup_norm_strict_upper: str
    voltage_intrinsic_term_upper: str
    voltage_recovery_term_upper: str
    voltage_scaffold_term_upper: str
    voltage_linear_delay_term_upper: str
    voltage_cubic_delay_term_upper: str
    voltage_reaching_term_upper: str
    voltage_input_authority_upper: str
    recovery_intrinsic_term_upper: str
    recovery_scaffold_term_upper: str
    recovery_reaching_term_upper: str
    recovery_input_authority_upper: str
    voltage_settling_time_upper: str
    recovery_settling_time_upper: str
    settling_time_upper: str
    exact_history_hold_time_upper: str
    complete_history_preparation_time_upper: str
    voltage_authority_ceiling: str
    recovery_authority_ceiling: str
    complete_preparation_time_ceiling: str
    voltage_authority_below_ceiling: bool
    recovery_authority_below_ceiling: bool
    complete_preparation_time_below_ceiling: bool
    optional_nodewise_recovery_authority_upper: str
    exact_baseline_voltage_cancellation: bool
    exact_baseline_recovery_cancellation: bool
    closed_loop_componentwise_reaching_law: bool
    sigma_half_continuous: bool
    sigma_half_locally_lipschitz_at_zero: bool
    closed_loop_one_sided_lipschitz: bool
    caratheodory_forward_existence: bool
    forward_uniqueness: bool
    backward_uniqueness_validated: bool
    finite_time_exact_state_preparation: bool
    predetermined_settling_schedule_validated: bool
    same_feedback_holds_target_after_settling: bool
    maximum_delay_hold_produces_exact_complete_history: bool
    causal_current_and_discrete_delay_measurement: bool
    future_history_measurement_required: bool
    recovery_history_measurement_required: bool
    bounded_additive_input_on_declared_bounded_cylinder: bool
    bounded_initial_data_cylinder_required: bool
    rfde_phase_space_compactness_validated: bool
    input_bound_independent_of_node_count: bool
    state_overwrite_used: bool
    impulse_used: bool
    release_switch_preserves_state_continuity: bool
    exact_model_cancellation_required: bool
    full_node_state_measurement_required: bool
    both_delayed_voltage_layers_required: bool
    optional_nodewise_recovery_cancellation_exact: bool
    optional_nodewise_zero_recovery_leaf_invariant: bool
    optional_nodewise_voltage_dynamics_preserved: bool
    optional_nodewise_authority_conditional_on_voltage_tube: bool
    optional_nodewise_route_distinct_from_collective_clamp: bool
    collective_clamp_route_still_available_separately: bool
    bandwidth_validated: bool
    slew_rate_validated: bool
    energy_validated: bool
    model_uncertainty_validated: bool
    measurement_noise_validated: bool
    hardware_implementation_validated: bool
    uniform_control_from_unbounded_initial_sets: bool
    general_network_topology_validated: bool
    issue_15_closed: bool


def _mapping(value: Any, label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{label} must be a mapping")
    return value


def _require_true(mapping: Mapping[str, Any], key: str) -> None:
    if mapping.get(key) is not True:
        raise ValueError(f"required source theorem flag must be true: {key}")


def _require_false(mapping: Mapping[str, Any], key: str) -> None:
    if mapping.get(key) is not False:
        raise ValueError(f"historical source scope was forged or promoted: {key}")


def _decimal(text: str, label: str) -> Decimal:
    if not isinstance(text, str):
        raise ValueError(f"{label} must be an exact decimal string")
    try:
        value = Decimal(text)
    except InvalidOperation as error:
        raise ValueError(f"{label} is not a valid decimal") from error
    if not value.is_finite():
        raise ValueError(f"{label} must be finite")
    return value


def _point(value: Decimal | str, precision: int) -> DirectedInterval:
    return DirectedInterval.from_decimal(format(value, "f"), precision)


def _upper(value: DirectedInterval | gmpy2.mpfr) -> str:
    endpoint = value.upper if isinstance(value, DirectedInterval) else value
    return decimal_upper(endpoint)


def _matrix_sup_norm(matrix: sp.Matrix) -> sp.Expr:
    return max(
        sp.simplify(sum(abs(matrix[row, column]) for column in range(matrix.cols)))
        for row in range(matrix.rows)
    )


def preparation_network_algebra(
    first_module_size: int = 2,
    second_module_size: int = 3,
) -> PreparationNetworkAlgebra:
    """Build the fixed rank-one delay layers and verify exact cancellation."""

    for value in (first_module_size, second_module_size):
        if isinstance(value, bool) or int(value) != value or int(value) <= 0:
            raise ValueError("module sizes must be positive integers")
    n_1 = int(first_module_size)
    n_2 = int(second_module_size)
    node_count = n_1 + n_2
    one = sp.ones(node_count, 1)
    pi = sp.Matrix(
        [[sp.Rational(1, 2 * n_1)] * n_1 + [sp.Rational(1, 2 * n_2)] * n_2]
    )
    projection = one * pi
    same = sp.zeros(node_count)
    cross = sp.zeros(node_count)
    for row in range(node_count):
        same_module = range(0, n_1) if row < n_1 else range(n_1, node_count)
        other_module = range(n_1, node_count) if row < n_1 else range(0, n_1)
        same_weight = sp.Rational(1, 2 * (n_1 if row < n_1 else n_2))
        cross_weight = sp.Rational(1, 2 * (n_2 if row < n_1 else n_1))
        for column in same_module:
            same[row, column] = same_weight
        for column in other_module:
            cross[row, column] = cross_weight

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
    identity = sp.eye(node_count)

    def cube_shift(vector: sp.Matrix) -> sp.Matrix:
        return vector.applyfunc(lambda item: (item - 1) ** 3)

    baseline_voltage = (
        v
        - v.applyfunc(lambda item: item**3) / 3
        - w
        + voltage_scaffold * (projection - identity) * v
        + epsilon
        * kappa_1
        * (same * delayed_0 + cross * delayed_1 - v)
        + epsilon
        * kappa_3
        * (
            same * cube_shift(delayed_0)
            + cross * cube_shift(delayed_1)
            - cube_shift(v)
        )
    )
    baseline_recovery = (
        epsilon * (v - unfolding * one)
        + recovery_scaffold * (projection - identity) * w
    )
    voltage_input = -baseline_voltage - k_v * sigma_v
    recovery_input = -baseline_recovery - k_w * sigma_w
    nodewise_decision_recovery_input = -baseline_recovery
    nodewise_decision_voltage_input = sp.zeros(node_count, 1)

    scaffold_norm = _matrix_sup_norm(projection - identity)
    return PreparationNetworkAlgebra(
        module_sizes=(n_1, n_2),
        averaging_matrix=projection,
        same_module_delay_matrix=same,
        cross_module_delay_matrix=cross,
        delay_sum_residual=sp.simplify(same + cross - projection),
        averaging_row_sums=tuple(
            sp.simplify(sum(projection[row, column] for column in range(node_count)))
            for row in range(node_count)
        ),
        same_delay_row_sums=tuple(
            sp.simplify(sum(same[row, column] for column in range(node_count)))
            for row in range(node_count)
        ),
        cross_delay_row_sums=tuple(
            sp.simplify(sum(cross[row, column] for column in range(node_count)))
            for row in range(node_count)
        ),
        averaging_sup_norm=_matrix_sup_norm(projection),
        same_delay_sup_norm=_matrix_sup_norm(same),
        cross_delay_sup_norm=_matrix_sup_norm(cross),
        scaffold_sup_norm=scaffold_norm,
        scaffold_strict_two_gap=sp.simplify(2 - scaffold_norm),
        voltage_cancellation_residual=sp.simplify(
            baseline_voltage + voltage_input + k_v * sigma_v
        ),
        recovery_cancellation_residual=sp.simplify(
            baseline_recovery + recovery_input + k_w * sigma_w
        ),
        nodewise_decision_recovery_residual=sp.simplify(
            baseline_recovery + nodewise_decision_recovery_input
        ),
        nodewise_decision_voltage_preservation_residual=sp.simplify(
            baseline_voltage
            + nodewise_decision_voltage_input
            - baseline_voltage
        ),
    )


def _validate_source(
    separator_payload: Mapping[str, Any],
    evidence: BoundedPreparationSourceEvidence,
) -> Mapping[str, Any]:
    if evidence.separator_result_sha256 != TRACKED_SEPARATOR_RESULT_SHA256:
        raise ValueError("separator result SHA-256 is outside the tracked scope")
    if evidence.causal_hold_note_sha256 != TRACKED_CAUSAL_HOLD_NOTE_SHA256:
        raise ValueError("causal-hold note SHA-256 is outside the tracked scope")
    if evidence.source_synchronous_model_id != SYNCHRONOUS_MODEL_ID:
        raise ValueError("the preparation source belongs to a different model")
    if evidence.full_network_instance_id != FULL_NETWORK_INSTANCE_ID:
        raise ValueError("the preparation source belongs to a different network")
    validate_same_model_separator_result_payload(separator_payload)
    root = _mapping(separator_payload, "separator payload")
    certificate = _mapping(root.get("certificate"), "separator certificate")
    source = _mapping(root.get("source_evidence"), "separator source")
    scope = _mapping(root.get("scope"), "separator scope")
    if certificate.get("source_synchronous_model_id") != SYNCHRONOUS_MODEL_ID:
        raise ValueError("separator synchronous model identifier changed")
    if certificate.get("certified_full_network_instance_id") != (
        FULL_NETWORK_INSTANCE_ID
    ):
        raise ValueError("separator full-network instance identifier changed")
    expected_constants = {
        "epsilon": "1/5",
        "unfolding": "3/5",
        "scaled_delays": ["4", "5"],
        "voltage_scaffold": "3",
        "recovery_scaffold": "2",
        "gain_half_width": "1e-12",
    }
    for key, wanted in expected_constants.items():
        if certificate.get(key) != wanted:
            raise ValueError(f"separator model/gain constant changed: {key}")
    _require_true(certificate, "same_synchronous_baseline_and_gain_box_validated")
    _require_true(certificate, "full_network_d3_e2_instance_fixed_by_this_certificate")
    _require_true(certificate, "reset_family_complete_history_threshold_validated")
    _require_true(scope, "same_synchronous_baseline_and_gain_box")
    _require_true(
        scope, "full_network_d3_e2_instance_fixed_by_separator_certificate"
    )
    _require_false(source, "source_periodic_artifact_certifies_full_network_scaffolds")
    _require_false(scope, "general_network_topology")
    return certificate


def bounded_additive_preparation_from_payload(
    separator_payload: Mapping[str, Any],
    evidence: BoundedPreparationSourceEvidence,
    *,
    voltage_history_sup_bound: str,
    recovery_current_sup_bound: str,
    reset_abs_bound: str,
    voltage_reaching_gain: str,
    recovery_reaching_gain: str,
    decision_voltage_tube_bound: str = "1.5",
    voltage_authority_ceiling: str = "23.19",
    recovery_authority_ceiling: str = "9.94",
    complete_preparation_time_ceiling: str = "14.50",
    precision: int = 160,
) -> BoundedAdditivePreparationCertificate:
    """Derive directed authority and preparation-time bounds."""

    source = _validate_source(separator_payload, evidence)
    if isinstance(precision, bool) or int(precision) != precision or precision < 64:
        raise ValueError("precision must be an integer of at least 64 bits")
    exact_inputs = {
        "voltage_history_sup_bound": _decimal(
            voltage_history_sup_bound, "voltage_history_sup_bound"
        ),
        "recovery_current_sup_bound": _decimal(
            recovery_current_sup_bound, "recovery_current_sup_bound"
        ),
        "reset_abs_bound": _decimal(reset_abs_bound, "reset_abs_bound"),
        "voltage_reaching_gain": _decimal(
            voltage_reaching_gain, "voltage_reaching_gain"
        ),
        "recovery_reaching_gain": _decimal(
            recovery_reaching_gain, "recovery_reaching_gain"
        ),
        "decision_voltage_tube_bound": _decimal(
            decision_voltage_tube_bound, "decision_voltage_tube_bound"
        ),
        "voltage_authority_ceiling": _decimal(
            voltage_authority_ceiling, "voltage_authority_ceiling"
        ),
        "recovery_authority_ceiling": _decimal(
            recovery_authority_ceiling, "recovery_authority_ceiling"
        ),
        "complete_preparation_time_ceiling": _decimal(
            complete_preparation_time_ceiling,
            "complete_preparation_time_ceiling",
        ),
    }
    for key in (
        "voltage_history_sup_bound",
        "recovery_current_sup_bound",
        "reset_abs_bound",
        "decision_voltage_tube_bound",
    ):
        if exact_inputs[key] < 0:
            raise ValueError(f"{key} must be nonnegative")
    if exact_inputs["reset_abs_bound"] > 1:
        raise ValueError("reset_abs_bound must remain inside the separator faces")
    for key in ("voltage_reaching_gain", "recovery_reaching_gain"):
        if exact_inputs[key] <= 0:
            raise ValueError(f"{key} must be strictly positive")
    for key in (
        "voltage_authority_ceiling",
        "recovery_authority_ceiling",
        "complete_preparation_time_ceiling",
    ):
        if exact_inputs[key] <= 0:
            raise ValueError(f"{key} must be positive")

    p = int(precision)
    v_0 = _point(exact_inputs["voltage_history_sup_bound"], p)
    w_0 = _point(exact_inputs["recovery_current_sup_bound"], p)
    reset = _point(exact_inputs["reset_abs_bound"], p)
    k_v = _point(exact_inputs["voltage_reaching_gain"], p)
    k_w = _point(exact_inputs["recovery_reaching_gain"], p)
    decision_bound = _point(exact_inputs["decision_voltage_tube_bound"], p)
    voltage_ceiling = _point(exact_inputs["voltage_authority_ceiling"], p)
    recovery_ceiling = _point(exact_inputs["recovery_authority_ceiling"], p)
    time_ceiling = _point(exact_inputs["complete_preparation_time_ceiling"], p)

    epsilon = DirectedInterval.from_decimal(1, p) / 5
    unfolding = DirectedInterval.from_decimal(3, p) / 5
    voltage_scaffold = DirectedInterval.from_decimal(3, p)
    recovery_scaffold = DirectedInterval.from_decimal(2, p)
    kappa_1_data = source.get("kappa_1_interval")
    kappa_3_data = source.get("kappa_3_interval")
    if not (
        isinstance(kappa_1_data, list)
        and len(kappa_1_data) == 2
        and isinstance(kappa_3_data, list)
        and len(kappa_3_data) == 2
    ):
        raise ValueError("separator gain endpoints are missing")
    kappa_1 = DirectedInterval.from_bounds(
        kappa_1_data[0], kappa_1_data[1], p
    )
    kappa_3 = DirectedInterval.from_bounds(
        kappa_3_data[0], kappa_3_data[1], p
    )
    if kappa_1.lower <= 0 or kappa_3.lower <= 0:
        raise ValueError("the tracked preparation requires positive gains")

    reachable_voltage_decimal = max(
        exact_inputs["voltage_history_sup_bound"],
        exact_inputs["reset_abs_bound"],
    )
    reachable_voltage = _point(reachable_voltage_decimal, p)
    voltage_error = v_0 + reset
    voltage_sqrt_error = voltage_error.sqrt()
    recovery_sqrt = w_0.sqrt()

    voltage_intrinsic = reachable_voltage + reachable_voltage**3 / 3
    voltage_recovery = w_0
    voltage_scaffold_term = 2 * voltage_scaffold * reachable_voltage
    voltage_linear_delay = 2 * epsilon * kappa_1 * reachable_voltage
    voltage_cubic_delay = (
        2 * epsilon * kappa_3 * (reachable_voltage + 1) ** 3
    )
    voltage_reaching = k_v * voltage_sqrt_error
    voltage_authority = (
        voltage_intrinsic
        + voltage_recovery
        + voltage_scaffold_term
        + voltage_linear_delay
        + voltage_cubic_delay
        + voltage_reaching
    )

    recovery_intrinsic = epsilon * (reachable_voltage + unfolding)
    recovery_scaffold_term = 2 * recovery_scaffold * w_0
    recovery_reaching = k_w * recovery_sqrt
    recovery_authority = (
        recovery_intrinsic + recovery_scaffold_term + recovery_reaching
    )

    voltage_settling = 2 * voltage_sqrt_error / k_v
    recovery_settling = 2 * recovery_sqrt / k_w
    settling_upper = max(voltage_settling.upper, recovery_settling.upper)
    settling = DirectedInterval.from_bounds(0, settling_upper, p)
    history_hold = (
        DirectedInterval.from_decimal(5, p)
        * DirectedInterval.from_decimal(5, p).sqrt()
    )
    complete_time = settling + history_hold
    optional_nodewise_authority = epsilon * (decision_bound + unfolding)

    algebra_audits = tuple(
        preparation_network_algebra(*sizes)
        for sizes in ((1, 1), (2, 3), (4, 2))
    )
    exact_algebra = all(
        audit.delay_sum_residual == sp.zeros(sum(audit.module_sizes))
        and audit.averaging_sup_norm == 1
        and audit.same_delay_sup_norm == sp.Rational(1, 2)
        and audit.cross_delay_sup_norm == sp.Rational(1, 2)
        and audit.scaffold_sup_norm < 2
        and audit.voltage_cancellation_residual
        == sp.zeros(sum(audit.module_sizes), 1)
        and audit.recovery_cancellation_residual
        == sp.zeros(sum(audit.module_sizes), 1)
        and audit.nodewise_decision_recovery_residual
        == sp.zeros(sum(audit.module_sizes), 1)
        for audit in algebra_audits
    )
    if not exact_algebra:
        raise ArithmeticError("the exact full-network preparation algebra failed")

    return BoundedAdditivePreparationCertificate(
        separator_result_sha256=evidence.separator_result_sha256,
        causal_hold_note_sha256=evidence.causal_hold_note_sha256,
        protocol_id=PREPARATION_PROTOCOL_ID,
        source_synchronous_model_id=evidence.source_synchronous_model_id,
        certified_full_network_instance_id=evidence.full_network_instance_id,
        precision_bits=p,
        epsilon="1/5",
        unfolding="3/5",
        voltage_scaffold="3",
        recovery_scaffold="2",
        scaled_delays=("4", "5"),
        maximum_physical_delay_upper=_upper(history_hold),
        kappa_1_interval=(str(kappa_1_data[0]), str(kappa_1_data[1])),
        kappa_3_interval=(str(kappa_3_data[0]), str(kappa_3_data[1])),
        voltage_history_sup_bound=format(
            exact_inputs["voltage_history_sup_bound"], "f"
        ),
        recovery_current_sup_bound=format(
            exact_inputs["recovery_current_sup_bound"], "f"
        ),
        reset_abs_bound=format(exact_inputs["reset_abs_bound"], "f"),
        voltage_reaching_gain=format(
            exact_inputs["voltage_reaching_gain"], "f"
        ),
        recovery_reaching_gain=format(
            exact_inputs["recovery_reaching_gain"], "f"
        ),
        decision_voltage_tube_bound=format(
            exact_inputs["decision_voltage_tube_bound"], "f"
        ),
        reachable_voltage_sup_bound=format(reachable_voltage_decimal, "f"),
        reachable_recovery_sup_bound=format(
            exact_inputs["recovery_current_sup_bound"], "f"
        ),
        voltage_initial_error_sup_bound=_upper(voltage_error),
        averaging_operator_sup_norm="1",
        each_delay_operator_sup_norm="1/2",
        scaffold_operator_sup_norm_strict_upper="2",
        voltage_intrinsic_term_upper=_upper(voltage_intrinsic),
        voltage_recovery_term_upper=_upper(voltage_recovery),
        voltage_scaffold_term_upper=_upper(voltage_scaffold_term),
        voltage_linear_delay_term_upper=_upper(voltage_linear_delay),
        voltage_cubic_delay_term_upper=_upper(voltage_cubic_delay),
        voltage_reaching_term_upper=_upper(voltage_reaching),
        voltage_input_authority_upper=_upper(voltage_authority),
        recovery_intrinsic_term_upper=_upper(recovery_intrinsic),
        recovery_scaffold_term_upper=_upper(recovery_scaffold_term),
        recovery_reaching_term_upper=_upper(recovery_reaching),
        recovery_input_authority_upper=_upper(recovery_authority),
        voltage_settling_time_upper=_upper(voltage_settling),
        recovery_settling_time_upper=_upper(recovery_settling),
        settling_time_upper=_upper(settling_upper),
        exact_history_hold_time_upper=_upper(history_hold),
        complete_history_preparation_time_upper=_upper(complete_time),
        voltage_authority_ceiling=format(
            exact_inputs["voltage_authority_ceiling"], "f"
        ),
        recovery_authority_ceiling=format(
            exact_inputs["recovery_authority_ceiling"], "f"
        ),
        complete_preparation_time_ceiling=format(
            exact_inputs["complete_preparation_time_ceiling"], "f"
        ),
        voltage_authority_below_ceiling=(
            voltage_authority.upper < voltage_ceiling.lower
        ),
        recovery_authority_below_ceiling=(
            recovery_authority.upper < recovery_ceiling.lower
        ),
        complete_preparation_time_below_ceiling=(
            complete_time.upper < time_ceiling.lower
        ),
        optional_nodewise_recovery_authority_upper=_upper(
            optional_nodewise_authority
        ),
        exact_baseline_voltage_cancellation=True,
        exact_baseline_recovery_cancellation=True,
        closed_loop_componentwise_reaching_law=True,
        sigma_half_continuous=True,
        sigma_half_locally_lipschitz_at_zero=False,
        closed_loop_one_sided_lipschitz=True,
        caratheodory_forward_existence=True,
        forward_uniqueness=True,
        backward_uniqueness_validated=False,
        finite_time_exact_state_preparation=True,
        predetermined_settling_schedule_validated=True,
        same_feedback_holds_target_after_settling=True,
        maximum_delay_hold_produces_exact_complete_history=True,
        causal_current_and_discrete_delay_measurement=True,
        future_history_measurement_required=False,
        recovery_history_measurement_required=False,
        bounded_additive_input_on_declared_bounded_cylinder=True,
        bounded_initial_data_cylinder_required=True,
        rfde_phase_space_compactness_validated=False,
        input_bound_independent_of_node_count=True,
        state_overwrite_used=False,
        impulse_used=False,
        release_switch_preserves_state_continuity=True,
        exact_model_cancellation_required=True,
        full_node_state_measurement_required=True,
        both_delayed_voltage_layers_required=True,
        optional_nodewise_recovery_cancellation_exact=True,
        optional_nodewise_zero_recovery_leaf_invariant=True,
        optional_nodewise_voltage_dynamics_preserved=True,
        optional_nodewise_authority_conditional_on_voltage_tube=True,
        optional_nodewise_route_distinct_from_collective_clamp=True,
        collective_clamp_route_still_available_separately=True,
        bandwidth_validated=False,
        slew_rate_validated=False,
        energy_validated=False,
        model_uncertainty_validated=False,
        measurement_noise_validated=False,
        hardware_implementation_validated=False,
        uniform_control_from_unbounded_initial_sets=False,
        general_network_topology_validated=False,
        issue_15_closed=False,
    )


def sigma_half(value: float) -> float:
    """Return sign(value)*sqrt(abs(value)) for diagnostics and tests."""

    number = float(value)
    if not math.isfinite(number):
        raise ValueError("value must be finite")
    if number > 0:
        return number**0.5
    if number < 0:
        return -(-number) ** 0.5
    return 0.0


def finite_time_reaching_profile(
    initial_value: float,
    gain: float,
    time: float,
) -> float:
    """Explicit forward solution of x'=-K sigma_half(x)."""

    x_0 = float(initial_value)
    k = float(gain)
    t = float(time)
    if not all(math.isfinite(item) for item in (x_0, k, t)):
        raise ValueError("profile arguments must be finite")
    if k <= 0 or t < 0:
        raise ValueError("gain must be positive and time nonnegative")
    sign = 1.0 if x_0 > 0 else -1.0 if x_0 < 0 else 0.0
    amplitude = max(abs(x_0) ** 0.5 - 0.5 * k * t, 0.0)
    return sign * amplitude**2


def load_bounded_additive_preparation_result(
    path: str | Path,
    *,
    expected_sha256: str,
) -> Mapping[str, Any]:
    """Hash-check a generated preparation record and its strict scope."""

    if not isinstance(expected_sha256, str) or len(expected_sha256) != 64:
        raise ValueError("expected_sha256 must be a 64-character digest")
    source = Path(path)
    raw = source.read_bytes()
    digest = sha256(raw).hexdigest()
    if digest != expected_sha256:
        raise ValueError(
            "bounded preparation result SHA-256 mismatch: "
            f"expected {expected_sha256}, got {digest}"
        )
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as error:
        raise ValueError("bounded preparation result is not valid JSON") from error
    root = _mapping(payload, "preparation result")
    evidence = _mapping(root.get("source_evidence"), "source_evidence")
    certificate = _mapping(root.get("certificate"), "certificate")
    scope = _mapping(root.get("scope"), "scope")
    if evidence.get("separator_result_sha256") != TRACKED_SEPARATOR_RESULT_SHA256:
        raise ValueError("generated result is not bound to the separator")
    if evidence.get("causal_hold_note_sha256") != TRACKED_CAUSAL_HOLD_NOTE_SHA256:
        raise ValueError("generated result is not bound to the causal-hold note")
    for key in (
        "finite_time_exact_state_preparation",
        "maximum_delay_hold_produces_exact_complete_history",
        "bounded_additive_input_on_declared_bounded_cylinder",
        "bounded_initial_data_cylinder_required",
        "input_bound_independent_of_node_count",
        "forward_uniqueness",
        "optional_nodewise_recovery_cancellation_exact",
        "optional_nodewise_zero_recovery_leaf_invariant",
        "optional_nodewise_voltage_dynamics_preserved",
        "exact_model_cancellation_required",
        "full_node_state_measurement_required",
        "both_delayed_voltage_layers_required",
    ):
        _require_true(certificate, key)
    for key in (
        "state_overwrite_used",
        "impulse_used",
        "bandwidth_validated",
        "slew_rate_validated",
        "energy_validated",
        "model_uncertainty_validated",
        "measurement_noise_validated",
        "hardware_implementation_validated",
        "uniform_control_from_unbounded_initial_sets",
        "rfde_phase_space_compactness_validated",
        "general_network_topology_validated",
        "issue_15_closed",
    ):
        _require_false(certificate, key)
    for key in (
        "bounded_additive_finite_time_preparation_on_declared_bounded_cylinder",
        "exact_complete_history_phi_r_after_scheduled_hold",
        "node_count_independent_input_authority",
        "bounded_initial_data_cylinder_required",
        "exact_model_cancellation_required",
        "full_node_state_and_both_delayed_voltage_layers_required",
        "optional_nodewise_zero_recovery_continuation_on_declared_voltage_tube",
    ):
        _require_true(scope, key)
    for key in (
        "state_overwrite",
        "impulse",
        "bandwidth",
        "slew_rate",
        "energy",
        "model_uncertainty",
        "measurement_noise",
        "hardware_implementation",
        "uniform_control_from_unbounded_initial_sets",
        "rfde_phase_space_compactness",
        "general_network_topology",
        "issue_15_closed",
    ):
        _require_false(scope, key)
    return root


__all__ = [
    "BoundedAdditivePreparationCertificate",
    "BoundedPreparationSourceEvidence",
    "PreparationNetworkAlgebra",
    "PREPARATION_PROTOCOL_ID",
    "TRACKED_CAUSAL_HOLD_NOTE_SHA256",
    "TRACKED_SEPARATOR_RESULT_SHA256",
    "bounded_additive_preparation_from_payload",
    "finite_time_reaching_profile",
    "load_bounded_additive_preparation_result",
    "preparation_network_algebra",
    "sigma_half",
]
