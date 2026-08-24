"""Hostile tests for the sliding-window and W1p Fredholm repair."""

from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest
import sympy as sp

from canard_control.fixed_epsilon_sliding_window_w1p_bridge import (
    AUDIT_ID,
    CANONICAL_LONG_DELAY_DOC_SHA256,
    GREEN_PHASE_TRACES_DOC_SHA256,
    GROWING_TUBE_GRAPH_DOC_SHA256,
    MODEL_ID,
    QUADRATIC_PERIOD_LOCKED_ROOT_DOC_SHA256,
    SELECTED_REPELLING_ENDPOINT_RESULT_SHA256,
    TWO_SIDED_CANDIDATE_RESULT_SHA256,
    reference_bridge_certificate,
    reference_candidate_phase_diagnostic,
    reference_fredholm_pair_reduction,
    reference_natural_discrete_ledger,
    reference_physical_fold_phase_audit,
    reference_sliding_window_identity_audit,
    reference_sliding_window_w1p_bridge_payload,
    reference_weak_space_audit,
    validate_sliding_window_w1p_bridge_payload,
)


REPOSITORY = Path(__file__).resolve().parents[1]
RESULT = (
    REPOSITORY
    / "experiments/results/fixed_epsilon_sliding_window_w1p_bridge.json"
)
SOURCE = (
    REPOSITORY
    / "src/canard_control/fixed_epsilon_sliding_window_w1p_bridge.py"
)
GENERATOR = (
    REPOSITORY
    / "experiments/fixed_epsilon_sliding_window_w1p_bridge.py"
)
NOTE = REPOSITORY / "docs/fixed-epsilon-sliding-window-w1p-bridge.md"
CANDIDATE_RESULT = (
    REPOSITORY / "experiments/results/fixed_epsilon_two_sided_candidate.json"
)
ENDPOINT_RESULT = (
    REPOSITORY
    / "experiments/results/fixed_epsilon_selected_repelling_endpoint.json"
)
GROWING_TUBE_DOC = REPOSITORY / "docs/growing-tube-graph-proof.md"
GREEN_PHASE_DOC = REPOSITORY / "docs/green-phase-selected-traces.md"
CANONICAL_LONG_DELAY_DOC = REPOSITORY / "docs/canonical-long-delay-theorem.md"
QUADRATIC_ROOT_DOC = (
    REPOSITORY / "docs/quadratic-period-locked-selected-root.md"
)
EXPECTED_SOURCE_SHA256 = (
    "67d87882041893ca8fa321c36b9329f10fbfc1de376df605b76317b8a8fc8714"
)
EXPECTED_GENERATOR_SHA256 = (
    "3ad6fa40ae2cfee71a9110710b3ee3e9dfe5d754b92a11619b7b4ed5d8a609eb"
)
EXPECTED_RESULT_SHA256 = (
    "4afc81cc6472f1c24fe938147623d0042f27d3ab4f30d3f5f052e924b60c3b05"
)
EXPECTED_NOTE_SHA256 = (
    "d9fea3261b855d0e397c0461a7d3f72ad68c2d6a255d48b8390b4d85717b6eaa"
)


def _digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _candidate() -> dict:
    return json.loads(CANDIDATE_RESULT.read_text(encoding="utf-8"))


def _payload() -> dict:
    return json.loads(RESULT.read_text(encoding="utf-8"))


def test_inverse_phase_and_circularity_identities_are_exact() -> None:
    audit = reference_sliding_window_identity_audit()
    assert audit.fixed_phase_gauge_defect == 0
    assert audit.internal_field_chain_rule_defect == 0
    assert audit.circular_endpoint_residual == 0
    assert audit.circular_endpoint_total_derivative == 0
    assert audit.chart_is_inside_solution_manifold
    assert audit.chart_rank_is_one
    assert not audit.ambient_backward_rfde_ivp_used
    assert "tail/outer residual" in audit.selected_orbit_requirement
    assert "cannot contain x^- or x^+" in audit.independent_selection_block
    assert "Gamma_x(xi_L)=End_L(x)" in audit.circular_endpoint_definition
    assert "dR=Gamma_xi*(ell(dE)-d xi)" in (
        audit.independent_phase_endpoint_derivative
    )
    assert "span{Gamma_xi}" in audit.independent_phase_endpoint_derivative_range
    assert "DR=0" in audit.independent_phase_endpoint_derivative_range


def test_nonstationary_toy_chart_satisfies_gauge_and_equilibrium_counterexample_does_not() -> None:
    xi, theta = sp.symbols("xi theta", positive=True, real=True)
    gamma = xi * sp.exp(theta)
    q = xi
    assert sp.simplify(q * sp.diff(gamma, xi) - sp.diff(gamma, theta)) == 0
    assert sp.simplify(q * sp.diff(gamma, xi).subs(theta, 0) - gamma.subs(theta, 0)) == 0
    assert gamma.subs(theta, 0) == xi
    assert sp.diff(gamma, xi).subs(theta, 0) == 1

    equilibrium_gamma = sp.Integer(0)
    assert sp.diff(equilibrium_gamma, xi) == 0
    # It satisfies the two zero invariance equations for F(0)=0, but the
    # affine phase gauge excludes it from the converse theorem.
    assert q * sp.diff(equilibrium_gamma, xi) == sp.diff(
        equilibrium_gamma, theta
    )
    assert sp.diff(equilibrium_gamma, xi) != 1


def test_sliding_window_contract_has_full_history_and_parameter_jets() -> None:
    audit = reference_sliding_window_identity_audit()
    assert "z^r(tau(xi,lambda)+theta" in audit.sliding_window_chart
    assert "q^r Gamma^r_xi=partial_theta" in audit.shift_invariance
    assert "holds in Lp" in audit.transport_equation_interpretation
    assert "bootstraps each history to W2p" in (
        audit.transport_equation_interpretation
    )
    assert "Sobolev ACL" in audit.transport_equation_interpretation
    assert "F(Gamma^r;lambda)" in audit.boundary_invariance
    assert "integral" in audit.local_backward_time
    assert "D_phi F" in audit.fixed_time_orbit_jet_equation
    assert "W2p in time" in audit.orbit_and_jet_regularity_hypothesis
    assert "not an equivalent one" in audit.orbit_and_jet_regularity_hypothesis
    assert "z in W4p" in audit.orbit_and_jet_regularity_hypothesis
    assert "affine history phase" in audit.phase_function
    assert "ell=D chi" in audit.phase_linear_part
    assert audit.inverse_phase_parameter_jet == "tau_lambda=-p_lambda/q"
    assert "p_lambda Gamma_xi" in audit.fixed_phase_history_jet
    assert "p_{tt}" in audit.fixed_phase_internal_field_jet
    assert "tau_{lambda mu}" in audit.second_inverse_phase_jet
    assert "Gamma_{lambda mu}" in audit.fixed_phase_second_history_jet
    assert "q_{lambda mu}" in audit.fixed_phase_second_internal_field_jet


def test_physical_fold_phase_and_clock_scaling_are_exact() -> None:
    audit = reference_physical_fold_phase_audit()
    assert audit.delta == sp.sqrt(5) / 5
    assert audit.physical_minus_scaled_fold_defect == 0
    assert audit.fold_phase == "xi=Y(0)"
    assert "a-V" not in str(audit.fold_internal_field)
    assert audit.clock_conversion == "q_fold=q_phys/delta"
    assert "phi_V(sigma/delta)" in audit.history_rescaling
    assert "-u_W(sigma/delta)" in audit.history_rescaling_derivative
    assert "delta-(Gamma^f_nu)_X" in audit.fold_nu_jet
    assert "delta^2 D S_delta" in audit.fold_history_nu_conversion
    assert audit.fold_internal_nu_conversion == "q^f_nu=delta q^p_a"
    assert audit.fold_internal_eta_conversion == "q^f_eta=q^p_eta/delta"


def test_c0_piecewise_polynomial_counts_are_w1p_conforming() -> None:
    audit = reference_weak_space_audit()
    assert audit.scalar_history_coefficients == 97
    assert audit.history_coefficients == 194
    assert audit.scalar_branch_coefficients == 145
    assert audit.branch_coefficients == 290
    assert audit.history_derivative_seams_needed_for_w1p == 0
    assert audit.history_derivative_seams_needed_for_global_c1_w2p == 30
    assert audit.global_c1_history_coefficients == 164
    assert audit.global_c1_endpoint_compatible_coefficients == 162
    assert audit.branch_derivative_seams_needed_for_global_c1_w2p == 46
    assert audit.global_c1_branch_coefficients == 244
    assert "value-jump Dirac masses" in audit.distributional_derivative_statement


def test_endpoint_bump_has_unit_derivative_and_vanishing_w12_norm() -> None:
    audit = reference_weak_space_audit()
    assert audit.endpoint_bump_value_at_left == 0
    assert audit.endpoint_bump_derivative_at_left == 0
    assert audit.endpoint_bump_value_at_current == 0
    assert audit.endpoint_bump_derivative_at_current == 1
    ell = sp.symbols("ell", positive=True)
    assert sp.simplify(audit.endpoint_bump_l2_norm_squared - ell**3 / 105) == 0
    assert sp.simplify(
        audit.endpoint_bump_derivative_l2_norm_squared - 2 * ell / 15
    ) == 0
    assert audit.endpoint_bump_w12_norm_limit == 0
    assert audit.compatible_strong_histories_dense_in_w1p_for_this_finite_delay_field
    assert not audit.endpoint_derivative_trace_continuous_on_w1p
    assert not audit.compatibility_is_closed_codimension_two_in_w1p
    assert not audit.discrete_194_to_192_is_continuous_w1p_solution_manifold_count


def test_old_w2p_to_lp_principal_scale_is_explicitly_rejected() -> None:
    audit = reference_weak_space_audit()
    assert "compactly embeds" in audit.w2p_to_lp_branch_column
    assert "is compact" in audit.w2p_to_w1p_history_trace
    assert not audit.old_w2p_to_lp_principal_operator_can_be_fredholm
    assert "W1p flow codomain" in audit.strong_space_alternative
    assert "Banach-scale" in audit.moving_delay_or_flight_time_warning


def test_natural_full_history_and_implicit_entry_ledgers_have_index_minus_one() -> None:
    ledger = reference_natural_discrete_ledger()
    assert ledger.explicit_chart_unknowns == 774
    assert ledger.explicit_chart_residuals == 775
    assert ledger.explicit_chart_residual_minus_unknown == 1
    assert ledger.full_history_rows_each == 194
    assert ledger.compatibility_rows == 0
    assert ledger.projected_history_rows == 0
    assert ledger.implicit_entry_unknowns == 581
    assert ledger.implicit_entry_residuals == 582
    assert ledger.implicit_entry_residual_minus_unknown == 1
    assert "B_-(history)=0" in ledger.implicit_attracting_function
    assert ledger.arithmetic_775_by_774_recovered
    assert not ledger.arithmetic_is_fredholm_proof
    assert not ledger.point_collocation_uniform_inf_sup_validated


def test_abstract_trace_pair_theorem_has_correct_kernel_cokernel_and_border() -> None:
    audit = reference_fredholm_pair_reduction()
    assert audit.assumed_intersection_dimension == 1
    assert audit.assumed_sum_codimension == 1
    assert audit.trace_ranges_assumed_closed
    assert audit.trace_maps_split_topological_embeddings_assumed
    assert audit.difference_operator_index == 0
    assert audit.phase_augmented_kernel_dimension == 0
    assert audit.phase_augmented_cokernel_dimension == 1
    assert audit.phase_augmented_index == -1
    assert audit.bordered_operator_index == 0
    assert audit.bordered_operator_isomorphism_under_hypotheses
    assert not audit.actual_trace_pair_closedness_validated
    assert not audit.actual_trace_maps_split_embeddings_validated
    assert not audit.actual_selected_trace_pair_hypotheses_validated
    assert not audit.coefficient_count_can_replace_trace_pair_proof
    assert "endpoint evaluations" in audit.adjoint_space
    assert "zero-boundary W^{-1,q}" in audit.adjoint_space
    assert audit.classical_advanced_equation_requires_extra_multiplier_regularity


def test_candidate_phase_diagnostic_is_recomputed_without_promotion() -> None:
    diagnostic = reference_candidate_phase_diagnostic(_candidate())
    assert diagnostic.source_result_sha256 == TWO_SIDED_CANDIDATE_RESULT_SHA256
    assert diagnostic.section_half_width == 3.0
    assert diagnostic.mesh_per_scaled_time == 32
    assert diagnostic.represented_history_steps == 237
    assert diagnostic.right_flight_nodes == 97
    assert diagnostic.two_flight_length == 6.0
    assert diagnostic.artificial_entry_tail_remaining_at_exit == pytest.approx(
        1.397086298188131, abs=1.0e-15
    )
    assert diagnostic.fold_internal_field_node_minimum == pytest.approx(
        0.09505982129277968, abs=1.0e-15
    )
    assert diagnostic.fold_internal_field_node_maximum == pytest.approx(
        1.7244298573163501, abs=1.0e-15
    )
    assert diagnostic.physical_internal_field_node_minimum == pytest.approx(
        0.04251204446792746, abs=1.0e-15
    )
    assert diagnostic.exit_gap_crossing_derivative == pytest.approx(
        -1.5031215576539718, abs=1.0e-14
    )
    assert diagnostic.nodewise_phase_monotonicity_observed
    assert not diagnostic.interval_phase_monotonicity_validated
    assert not diagnostic.candidate_right_trace_independent_of_connection
    assert not diagnostic.entry_template_q_is_repelling_internal_field
    assert diagnostic.candidate_exit_gap_crossing_nonzero_observed
    assert not diagnostic.selected_orbit_exit_gap_anchor_validated
    assert not diagnostic.exit_gap_selects_repelling_orbit
    assert diagnostic.candidate_can_seed_independent_orbit_continuation
    assert not diagnostic.candidate_endpoint_and_adjoint_can_be_reused


def test_certificate_keeps_every_selected_root_claim_open() -> None:
    certificate = reference_bridge_certificate()
    assert certificate.model_id == MODEL_ID
    assert certificate.audit_id == AUDIT_ID
    assert certificate.sliding_window_chart_from_independent_orbit_proved
    assert certificate.invariant_nonstationary_chart_is_locally_sliding_window_proved
    assert certificate.fixed_phase_parameter_jet_formulas_proved
    assert certificate.c0_piecewise_polynomials_are_w1p_conforming_proved
    assert not certificate.derivative_seams_required_for_w1p
    assert not certificate.compatibility_continuous_on_w1p
    assert certificate.w2p_to_lp_old_principal_scale_rejected
    assert certificate.natural_w1p_formal_775_by_774_ledger_derived
    assert certificate.abstract_index_minus_one_trace_pair_reduction_proved
    assert not certificate.independent_selected_attracting_trace_constructed
    assert not certificate.attracting_stable_fibre_trace_range_constructed
    assert not certificate.independent_selected_repelling_orbit_constructed
    assert not certificate.frozen_target_graph_family_validated
    assert not certificate.prepared_planar_trace_family_validated
    assert not certificate.fixed_window_gap_row_validated
    assert not certificate.canonical_graph_continuation_completed
    assert not certificate.regularized_gap_validated
    assert not certificate.retained_physical_history_hull_validated
    assert not certificate.terminal_local_phase_validated
    assert not certificate.actual_trace_pair_fredholm_hypotheses_validated
    assert not certificate.continuous_advanced_adjoint_validated
    assert not certificate.fixed_epsilon_selected_root_validated
    assert not certificate.fixed_epsilon_response_validated
    assert not certificate.physical_onset_validated
    assert "wider graph cutoff S_hat=S+B" in certificate.shortest_next_problem
    assert "A_{S,P} nu+B_{S,P}" in certificate.shortest_next_problem
    assert "stable-fibre endpoint trace range" in certificate.shortest_next_problem


def test_payload_validator_rejects_root_and_phase_promotions() -> None:
    payload = reference_sliding_window_w1p_bridge_payload(_candidate())
    validate_sliding_window_w1p_bridge_payload(payload)

    broken = deepcopy(payload)
    broken["schema_version"] = 2
    with pytest.raises(ValueError, match="schema version"):
        validate_sliding_window_w1p_bridge_payload(broken)

    promoted = deepcopy(payload)
    promoted["certificate"]["fixed_epsilon_selected_root_validated"] = True
    with pytest.raises(ValueError, match="open claim"):
        validate_sliding_window_w1p_bridge_payload(promoted)

    promoted = deepcopy(payload)
    promoted["certificate"][
        "independent_selected_attracting_trace_constructed"
    ] = True
    with pytest.raises(ValueError, match="open claim"):
        validate_sliding_window_w1p_bridge_payload(promoted)

    promoted = deepcopy(payload)
    promoted["certificate"][
        "attracting_stable_fibre_trace_range_constructed"
    ] = True
    with pytest.raises(ValueError, match="open claim"):
        validate_sliding_window_w1p_bridge_payload(promoted)

    promoted = deepcopy(payload)
    promoted["certificate"]["fixed_window_gap_row_validated"] = True
    with pytest.raises(ValueError, match="open claim"):
        validate_sliding_window_w1p_bridge_payload(promoted)

    promoted = deepcopy(payload)
    promoted["certificate"]["continuous_advanced_adjoint_validated"] = True
    with pytest.raises(ValueError, match="open claim"):
        validate_sliding_window_w1p_bridge_payload(promoted)

    broken = deepcopy(payload)
    broken["assumptions_id"] = "forged"
    with pytest.raises(ValueError, match="assumptions identifier"):
        validate_sliding_window_w1p_bridge_payload(broken)

    broken = deepcopy(payload)
    broken["certificate"]["assumptions_id"] = "forged"
    with pytest.raises(ValueError, match="certificate assumptions"):
        validate_sliding_window_w1p_bridge_payload(broken)

    promoted = deepcopy(payload)
    promoted["candidate_phase_diagnostic"][
        "interval_phase_monotonicity_validated"
    ] = True
    with pytest.raises(ValueError, match="open claim"):
        validate_sliding_window_w1p_bridge_payload(promoted)

    broken = deepcopy(payload)
    broken["natural_discrete_ledger"]["explicit_chart_residuals"] = 774
    with pytest.raises(ValueError, match="residual count"):
        validate_sliding_window_w1p_bridge_payload(broken)

    broken = deepcopy(payload)
    broken["fredholm_pair_reduction"]["trace_ranges_assumed_closed"] = False
    with pytest.raises(ValueError, match="proved identity"):
        validate_sliding_window_w1p_bridge_payload(broken)

    broken = deepcopy(payload)
    broken["fredholm_pair_reduction"][
        "trace_maps_split_topological_embeddings_assumed"
    ] = False
    with pytest.raises(ValueError, match="proved identity"):
        validate_sliding_window_w1p_bridge_payload(broken)

    promoted = deepcopy(payload)
    promoted["fredholm_pair_reduction"][
        "actual_selected_trace_pair_hypotheses_validated"
    ] = True
    with pytest.raises(ValueError, match="open claim"):
        validate_sliding_window_w1p_bridge_payload(promoted)


def test_loaded_json_audit_validates_after_exact_serialization() -> None:
    validate_sliding_window_w1p_bridge_payload(_payload()["audit"])


def test_parent_hashes_and_manifest_are_pinned() -> None:
    assert _digest(CANDIDATE_RESULT) == TWO_SIDED_CANDIDATE_RESULT_SHA256
    assert _digest(ENDPOINT_RESULT) == SELECTED_REPELLING_ENDPOINT_RESULT_SHA256
    assert _digest(GROWING_TUBE_DOC) == GROWING_TUBE_GRAPH_DOC_SHA256
    assert _digest(GREEN_PHASE_DOC) == GREEN_PHASE_TRACES_DOC_SHA256
    assert _digest(CANONICAL_LONG_DELAY_DOC) == CANONICAL_LONG_DELAY_DOC_SHA256
    assert _digest(QUADRATIC_ROOT_DOC) == QUADRATIC_PERIOD_LOCKED_ROOT_DOC_SHA256
    payload = _payload()
    manifest = payload["manifest"]
    assert manifest["parent_sha256"]["two_sided_candidate_result"] == (
        TWO_SIDED_CANDIDATE_RESULT_SHA256
    )
    assert manifest["parent_sha256"]["selected_repelling_endpoint_result"] == (
        SELECTED_REPELLING_ENDPOINT_RESULT_SHA256
    )
    assert manifest["parent_sha256"]["growing_tube_graph_doc"] == (
        GROWING_TUBE_GRAPH_DOC_SHA256
    )
    assert manifest["parent_sha256"]["green_phase_traces_doc"] == (
        GREEN_PHASE_TRACES_DOC_SHA256
    )
    assert manifest["parent_sha256"]["canonical_long_delay_doc"] == (
        CANONICAL_LONG_DELAY_DOC_SHA256
    )
    assert manifest["parent_sha256"]["quadratic_period_locked_root_doc"] == (
        QUADRATIC_PERIOD_LOCKED_ROOT_DOC_SHA256
    )
    assert all(manifest["parent_claim_checks"].values())
    assert manifest["proof_source_sha256"] == EXPECTED_SOURCE_SHA256
    assert manifest["generator_sha256"] == EXPECTED_GENERATOR_SHA256


def test_generated_artifacts_are_byte_reproducible(tmp_path: Path) -> None:
    generated = tmp_path / "audit.json"
    environment = os.environ.copy()
    environment["PYTHONPATH"] = os.pathsep.join(
        [str(REPOSITORY / "src"), str(REPOSITORY / "build/testdeps")]
    )
    subprocess.run(
        [sys.executable, str(GENERATOR), "--output", str(generated)],
        cwd=REPOSITORY,
        env=environment,
        check=True,
    )
    assert generated.read_bytes() == RESULT.read_bytes()


def test_source_result_note_and_generator_hashes_are_frozen() -> None:
    assert _digest(SOURCE) == EXPECTED_SOURCE_SHA256
    assert _digest(GENERATOR) == EXPECTED_GENERATOR_SHA256
    assert _digest(RESULT) == EXPECTED_RESULT_SHA256
    assert _digest(NOTE) == EXPECTED_NOTE_SHA256


def test_note_states_the_breakthrough_and_every_remaining_gate() -> None:
    text = NOTE.read_text(encoding="utf-8")
    required = (
        "root remains open",
        "sliding-window equivalence theorem",
        "strict circularity",
        "Compatibility is not a \\(W^{1,p}\\) boundary row",
        "compatible histories are dense in \\(W^{1,p}\\)",
        "\\(W^{2,p}\\to L^p\\) is the wrong principal scale",
        "natural full-history coefficient ledger",
        "exact abstract index-\\(-1\\) reduction",
        "Correct adjoint dual space",
        "binary64",
        "canonical special-flow graph continuation",
        "Input-independent biological onset and pulse-control theorem",
    )
    for phrase in required:
        assert phrase in text
