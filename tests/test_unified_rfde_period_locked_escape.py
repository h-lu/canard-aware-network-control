"""Hostile tests for the period-locked unified-RFDE escape audit."""

from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys

import pytest
import sympy as sp

from canard_control.unified_rfde_period_locked_escape import (
    AUTONOMOUS_HANDOFF_RESULT_SHA256,
    BALANCED_CONTROL_CHAIN_RESULT_SHA256,
    COMPATIBILITY_RESULT_SHA256,
    HETEROGENEOUS_ROOT_DOC_SHA256,
    PERIODIC_BOX_RESULT_SHA256,
    QUADRATIC_CARRIER_RESULT_SHA256,
    ROOT_ADJOINT_GATE_RESULT_SHA256,
    balanced_period_locked_escape_audit,
    balanced_period_locked_escape_audit_is_exact,
    escape_audits_are_exact,
    linear_canard_parity_audit_is_exact,
    reference_finite_atom_invisibility_audit,
    reference_heterogeneous_curvature_synchrony_audit,
    reference_linear_canard_parity_audit,
    reference_period_locked_escape_audit,
    reference_unified_escape_certificate,
    validate_unified_escape_payload,
)


REPOSITORY = Path(__file__).resolve().parents[1]
RESULT = (
    REPOSITORY
    / "experiments/results/unified_rfde_period_locked_escape.json"
)
NOTE = REPOSITORY / "docs/unified-rfde-period-locked-escape.md"
EXPECTED_RESULT_SHA256 = (
    "4e4121a7b8d982545161c641caa4a8d783612db1b9889dca2b51572efbf90364"
)
EXPECTED_NOTE_SHA256 = (
    "176301151105b7e17c4b43c1cfb383c0e14a0b86d6e7028dea773e363485459c"
)


def _payload() -> dict:
    return json.loads(RESULT.read_text(encoding="utf-8"))


def _cycle(size: int) -> sp.Matrix:
    matrix = sp.zeros(size)
    for row in range(size):
        matrix[row, (row + 1) % size] = 1
    return matrix


def test_finite_fixed_atoms_require_atomwise_sync_annihilation() -> None:
    audit = reference_finite_atom_invisibility_audit()
    assert audit.action_coefficient_matrix == audit.atom_sync_columns
    assert audit.universal_invisibility_substitution_action == sp.zeros(2, 1)
    assert (
        audit.third_atom_coefficient_after_first_two_annihilate
        == audit.atom_sync_columns[:, 2]
    )
    assert audit.atom_sync_columns[:, 2] != sp.zeros(2, 1)


def test_heterogeneous_curvature_return_dies_when_synchrony_is_restored() -> None:
    audit = reference_heterogeneous_curvature_synchrony_audit()
    c_1, c_2, h = sp.symbols("c_1 c_2 h", real=True)
    assert audit.synchrony_residual == sp.Matrix(
        [(c_1 - c_2) / 2, (-c_1 + c_2) / 2]
    )
    assert audit.heterogeneous_return == h * (c_1 - c_2) / 2
    assert audit.homogeneous_synchrony_substitution_residual == sp.zeros(2, 1)
    assert audit.homogeneous_synchrony_substitution_return == 0


def test_normalized_and_actual_period_locked_moments_include_epsilon() -> None:
    audit = reference_period_locked_escape_audit()
    period = sp.symbols("T_p", positive=True)
    assert audit.epsilon == sp.Rational(1, 5)
    assert audit.periodic_output_unfolding == sp.Rational(3, 5)
    assert audit.kappa_center == (sp.Rational(1, 5), sp.Rational(1, 4))
    assert audit.base_delays == (4 * sp.sqrt(5), 5 * sp.sqrt(5))
    assert audit.normalized_structural_total_mass == sp.zeros(3, 3)
    assert (
        audit.normalized_structural_first_moment
        == -period * audit.collective_projection
    )
    assert audit.normalized_projected_synchronous_first_moment == period
    assert audit.actual_eta_derivative_total_mass == sp.zeros(3, 3)
    assert (
        audit.actual_eta_derivative_first_moment
        == -period * audit.collective_projection / 5
    )
    assert audit.actual_projected_synchronous_first_moment == period / 5
    assert audit.constant_history_action == sp.zeros(3, 1)
    assert audit.period_locked_action == sp.zeros(3, 1)
    assert audit.affine_synchronous_action != sp.zeros(3, 1)


def test_nonzero_linear_moment_has_exact_leading_parity_cancellation() -> None:
    audit = reference_linear_canard_parity_audit()
    delta, period, alpha = sp.symbols(
        "delta T_star alpha", positive=True, finite=True
    )
    s = sp.Symbol("s", real=True)
    assert linear_canard_parity_audit_is_exact(audit)
    assert audit.scaled_delay_shift == delta * period
    assert audit.singular_history_difference == -delta * period / (2 * alpha)
    assert audit.singular_fast_forcing_coefficient == (
        -delta**2 * period / (2 * alpha)
    )
    assert audit.leading_integrand == (
        -delta**2 * period * s * sp.exp(-s**2 / 2) / (2 * alpha)
    )
    assert audit.leading_pairing == 0


def test_general_balanced_topology_preserves_sync_and_period_lock() -> None:
    audit = reference_period_locked_escape_audit()
    one = sp.ones(3, 1)
    assert audit.base_scaffold_rank == 3
    assert audit.base_scaffold != audit.collective_projection
    assert audit.base_delay_0 + audit.base_delay_1 != audit.base_scaffold
    assert (
        audit.base_delay_0 + audit.base_delay_1
        != audit.collective_projection
    )
    assert audit.base_scaffold_row_balance_residual == sp.zeros(3, 1)
    assert audit.base_scaffold_left_balance_residual == sp.zeros(1, 3)
    assert audit.base_delay_0_row_balance_residual == sp.zeros(3, 1)
    assert audit.base_delay_1_row_balance_residual == sp.zeros(3, 1)
    assert audit.combined_delay_row_balance_residual == sp.zeros(3, 1)
    assert audit.combined_delay_left_balance_residual == sp.zeros(1, 3)
    assert audit.synchronous_scaffold_action == sp.zeros(3, 1)
    assert (
        audit.synchronous_linear_delay_action
        == audit.expected_synchronous_linear_delay_action
    )
    assert len(set(audit.synchronous_action)) == 1
    assert audit.structural_action_on_transverse_history == sp.zeros(3, 1)
    assert audit.transverse_projection_of_structural_action == sp.zeros(3, 3)
    assert audit.collective_projection * one == one


@pytest.mark.parametrize("size", (1, 2, 5, 8))
def test_carrier_identities_hold_for_arbitrary_finite_cycle_sizes(
    size: int,
) -> None:
    scaffold = _cycle(size)
    audit = balanced_period_locked_escape_audit(
        scaffold,
        [sp.Rational(1, size)] * size,
        scaffold / 2,
        sp.eye(size) / 2,
    )
    assert audit.node_count == size
    assert balanced_period_locked_escape_audit_is_exact(audit)
    assert audit.synchronous_scaffold_action == sp.zeros(size, 1)
    assert audit.structural_action_on_transverse_history == sp.zeros(size, 1)


def test_unbalanced_scaffold_is_not_promoted_to_general_carrier() -> None:
    audit = balanced_period_locked_escape_audit(
        [[1, 0], [1, 0]],
        [sp.Rational(1, 2), sp.Rational(1, 2)],
        [[sp.Rational(1, 2), 0], [0, sp.Rational(1, 2)]],
        [[sp.Rational(1, 2), 0], [0, sp.Rational(1, 2)]],
    )
    assert audit.base_scaffold_left_balance_residual != sp.zeros(1, 2)
    assert not balanced_period_locked_escape_audit_is_exact(audit)


def test_fixed_events_and_block_triangular_determinant_are_exact() -> None:
    audit = reference_period_locked_escape_audit()
    event_state = sp.symbols("x_event", real=True)
    assert audit.positive_event_functional == event_state - sp.Rational(3, 2)
    assert audit.negative_event_functional == -event_state - sp.Rational(6, 5)
    assert sp.expand(
        audit.response_determinant - audit.expected_response_determinant
    ) == 0


def test_sync_annihilating_operator_only_escapes_on_an_offsync_direction() -> None:
    audit = reference_period_locked_escape_audit()
    assert audit.offsync_operator_on_sync == sp.zeros(2, 1)
    assert audit.offsync_operator_on_direction == sp.Matrix([1, -2])
    assert audit.offsync_projected_pairing == 0


def test_certificate_keeps_every_missing_analytic_bridge_false() -> None:
    assert escape_audits_are_exact()
    certificate = reference_unified_escape_certificate()
    assert certificate.balanced_general_topology_carrier_validated
    assert certificate.delay_layers_need_not_sum_to_scaffold_or_projector_validated
    assert certificate.topology_independent_synchronous_periodic_outputs_validated
    assert certificate.period_locked_operator_preserves_synchrony_validated
    assert certificate.distinguished_periodic_orbit_annihilated_validated
    assert certificate.normalized_projected_synchronous_first_moment_nonzero_validated
    assert certificate.actual_eta_derivative_epsilon_factor_validated
    assert certificate.actual_projected_synchronous_first_moment_nonzero_validated
    assert certificate.linear_leading_singular_interior_pairing_zero_validated
    assert not certificate.nonzero_moment_sufficient_for_nonzero_root_response_validated
    assert not certificate.collective_mode_is_simple_canard_critical_direction_validated
    assert not certificate.general_topology_stable_history_invertibility_validated
    assert certificate.block_triangular_response_identity_validated
    assert certificate.block_response_is_parameter_linked_validated
    assert not certificate.trajectory_linked_root_periodic_event_chain_validated
    assert not certificate.arbitrary_third_atom_escapes_universal_invisibility_validated
    assert not certificate.same_extended_rfde_selected_root_validated
    assert not certificate.nonzero_selected_root_eta_response_validated
    assert not certificate.common_epsilon_root_and_periodic_regime_validated
    assert certificate.qualitative_three_parameter_periodic_branch_validated
    assert certificate.center_periodic_frequency_amplitude_eta_column_zero_validated
    assert not certificate.quantitative_eta_neighborhood_periodic_box_validated
    assert certificate.eta_zero_inert_history_trajectory_embedding_validated
    assert not (
        certificate.linear_enlarged_horizon_parameter_coherent_root_preparation_validated
    )
    assert certificate.quadratic_leading_singular_pairing_nonzero_parent_validated
    assert (
        certificate.quadratic_fixed_scaled_support_canonical_root_response_parent_validated
    )
    assert not certificate.quadratic_fixed_epsilon_one_fifth_rho_nonzero_validated
    assert certificate.eta_zero_balanced_controlled_voltage_excursions_validated
    assert not (
        certificate.eta_neighborhood_balanced_controlled_voltage_excursions_validated
    )
    assert not certificate.eta_neighborhood_autonomous_event_crossing_validated
    assert not certificate.root_event_zero_set_equivalence_validated
    assert not certificate.unforced_onset_validated
    assert not certificate.biological_pulse_basin_validated
    assert not certificate.full_network_periodic_attraction_validated
    assert not certificate.sparse_local_collective_channel_implementation_validated


def test_parent_hashes_are_pinned_to_current_files() -> None:
    pairs = (
        (
            "experiments/results/fhn_root_periodic_compatibility.json",
            COMPATIBILITY_RESULT_SHA256,
        ),
        (
            "experiments/results/fhn_periodic_parameter_box.json",
            PERIODIC_BOX_RESULT_SHA256,
        ),
        (
            "experiments/results/fhn_balanced_control_chain.json",
            BALANCED_CONTROL_CHAIN_RESULT_SHA256,
        ),
        (
            "experiments/results/fhn_autonomous_handoff_excursion.json",
            AUTONOMOUS_HANDOFF_RESULT_SHA256,
        ),
        (
            "docs/paper-ii-heterogeneous-curvature-selected-root.md",
            HETEROGENEOUS_ROOT_DOC_SHA256,
        ),
        (
            "experiments/results/dual_scaffold_root_adjoint_gate.json",
            ROOT_ADJOINT_GATE_RESULT_SHA256,
        ),
        (
            "experiments/results/quadratic_period_locked_root_carrier.json",
            QUADRATIC_CARRIER_RESULT_SHA256,
        ),
    )
    for relative, expected in pairs:
        assert sha256((REPOSITORY / relative).read_bytes()).hexdigest() == expected


def test_generated_payload_validates_and_rejects_promotions() -> None:
    payload = _payload()
    validate_unified_escape_payload(payload)
    for key in (
        "same_extended_rfde_selected_root",
        "nonzero_selected_root_eta_response",
        "collective_mode_is_simple_canard_critical_direction",
        "general_topology_stable_history_invertibility",
        "eta_neighborhood_balanced_controlled_voltage_excursions",
        "trajectory_linked_root_periodic_event_chain",
        "root_event_zero_set_equivalence",
        "unforced_onset",
        "biological_pulse_basin",
        "nonzero_moment_sufficient_for_nonzero_root_response",
        "quantitative_eta_neighborhood_periodic_box",
        "linear_enlarged_horizon_parameter_coherent_root_preparation",
        "quadratic_fixed_epsilon_one_fifth_rho_nonzero",
    ):
        hostile = deepcopy(payload)
        hostile["scope"][key] = True
        with pytest.raises(ValueError, match="promoted"):
            validate_unified_escape_payload(hostile)
    for field, replacement in (
        ("epsilon", "1/4"),
        ("actual_projected_synchronous_first_moment", "0"),
        (
            "actual_eta_derivative_first_moment",
            [["0", "0", "0"], ["0", "0", "0"], ["0", "0", "0"]],
        ),
    ):
        hostile = deepcopy(payload)
        hostile["exact_audits"]["period_locked"][field] = replacement
        with pytest.raises(ValueError, match="exact_audits"):
            validate_unified_escape_payload(hostile)
    hostile = deepcopy(payload)
    hostile["exact_audits"]["linear_canard_parity"]["leading_pairing"] = "1"
    with pytest.raises(ValueError, match="exact_audits"):
        validate_unified_escape_payload(hostile)
    hostile = deepcopy(payload)
    hostile["scope"]["end_to_end_physical_onset"] = True
    with pytest.raises(ValueError, match="unpinned"):
        validate_unified_escape_payload(hostile)
    for key in (
        "handoff_refuses_autonomous_onset",
        "linear_parent_has_exact_singular_parity_cancellation",
        "quadratic_parent_has_canonical_small_delta_root_response",
        "quadratic_parent_refuses_fixed_epsilon_nonzero_rho",
    ):
        hostile = deepcopy(payload)
        hostile["provenance"]["parent_claim_checks"][key] = False
        with pytest.raises(ValueError, match="parent claim checks"):
            validate_unified_escape_payload(hostile)
    for key, replacement in (
        ("proof_source_sha256", "0" * 64),
        ("generator_sha256", "1" * 64),
        ("distinguished_period_definition", "mistuned period"),
    ):
        hostile = deepcopy(payload)
        hostile["provenance"][key] = replacement
        with pytest.raises(ValueError, match="source-bound"):
            validate_unified_escape_payload(hostile)
    assert sha256(RESULT.read_bytes()).hexdigest() == EXPECTED_RESULT_SHA256
    assert sha256(NOTE.read_bytes()).hexdigest() == EXPECTED_NOTE_SHA256


def test_generated_record_is_byte_reproducible(tmp_path: Path) -> None:
    output = tmp_path / "escape.json"
    subprocess.run(
        [
            sys.executable,
            str(REPOSITORY / "experiments/unified_rfde_period_locked_escape.py"),
            "--output",
            str(output),
        ],
        cwd=REPOSITORY,
        check=True,
        stdout=subprocess.DEVNULL,
    )
    assert output.read_bytes() == RESULT.read_bytes()


def test_note_keeps_period_lock_and_physical_scope_separate() -> None:
    text = " ".join(NOTE.read_text(encoding="utf-8").split())
    lowered = text.lower()
    assert "period-locked collective-delay" in lowered
    assert "arbitrary finite balanced topology" in lowered
    assert "full-network attraction" in lowered
    assert "not invisible on every synchronous history" in lowered
    assert "common physical time" in lowered
    assert "conditional block response" in lowered
    assert "parity cancellation" in lowered
    assert "qualitative" in lowered
    assert "enlarged horizon" in lowered
    assert "quadratic" in lowered
    assert "input-policy-independent" in lowered
    assert "does not identify" in lowered
    assert "autonomous onset" in lowered
