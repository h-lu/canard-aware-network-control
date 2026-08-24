"""Hostile tests for the fixed-epsilon selected repelling endpoint audit."""

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

from canard_control.fixed_epsilon_selected_repelling_endpoint import (
    FIXED_EPSILON_BVP_RESULT_SHA256,
    TWO_SIDED_CANDIDATE_RESULT_SHA256,
    compatible_history_fiber_algebra_is_exact,
    invariant_chart_backward_extension_identity_is_exact,
    reference_compatible_endpoint_count_audit,
    reference_compatible_history_fiber_audit,
    reference_selected_repelling_endpoint_certificate,
    reference_selected_repelling_endpoint_contract,
    reference_selected_repelling_endpoint_payload,
    validate_selected_repelling_endpoint_payload,
)


REPOSITORY = Path(__file__).resolve().parents[1]
RESULT = (
    REPOSITORY
    / "experiments/results/fixed_epsilon_selected_repelling_endpoint.json"
)
SOURCE = (
    REPOSITORY
    / "src/canard_control/fixed_epsilon_selected_repelling_endpoint.py"
)
GENERATOR = (
    REPOSITORY / "experiments/fixed_epsilon_selected_repelling_endpoint.py"
)
NOTE = REPOSITORY / "docs/fixed_epsilon_selected_repelling_endpoint.md"
EXPECTED_RESULT_SHA256 = (
    "1ab9678e2fdd28439c6552c05e80c1c751a88a493fb02319fbc76d9a73a337e4"
)
EXPECTED_NOTE_SHA256 = (
    "cf3916ed88c93e15aa20da9dcf52959e9f617f29c96c6298829c948cdca0e85c"
)
EXPECTED_SOURCE_SHA256 = (
    "513bc9f88040108bcf8dc6bc352cc16335e403d26602816d9c1058100b9c5a21"
)
EXPECTED_GENERATOR_SHA256 = (
    "ebd39bb6d45c9b058d9e198667a68992fb1b053e05237fd371b92ed7486f77ca"
)


def _payload() -> dict:
    return json.loads(RESULT.read_text(encoding="utf-8"))


def test_solution_manifold_node_polynomial_has_exact_hermite_data() -> None:
    audit = reference_compatible_history_fiber_audit()
    s = audit.history_variable
    theta = audit.scaled_period_delay
    node = audit.solution_manifold_node_polynomial
    assert sp.simplify(node.subs(s, 0)) == 0
    assert sp.simplify(node.subs(s, -4)) == 0
    assert sp.simplify(node.subs(s, -5)) == 0
    assert sp.simplify(node.subs(s, -theta)) == 0
    assert sp.simplify(sp.diff(node, s).subs(s, 0)) == 1


def test_period_atom_pair_has_same_current_and_exact_future_difference() -> None:
    audit = reference_compatible_history_fiber_audit()
    r, eta = audit.perturbation_amplitude, audit.eta
    assert audit.exit_observable_at_base_current == 0
    assert audit.exit_observable_current_gradient_at_base == sp.Matrix(
        [1, -sp.Rational(1, 2)]
    )
    assert audit.period_perturbation_current_value == 0
    assert audit.period_perturbation_delay_4_value == 0
    assert audit.period_perturbation_delay_5_value == 0
    assert audit.period_perturbation_period_delay_value == r
    assert (
        audit.period_fast_field_difference
        == audit.period_perturbation_current_derivative
    )
    assert sp.simplify(
        audit.period_fast_field_difference + eta * r * (r + 2) / 5
    ) == 0
    assert audit.period_unit_witness_difference == -3 * eta / 5
    assert audit.period_unit_witness_difference.subs(eta, 1) != 0


def test_eta_zero_baseline_delay_pair_has_exact_future_difference() -> None:
    audit = reference_compatible_history_fiber_audit()
    r = audit.perturbation_amplitude
    assert audit.delay_4_perturbation_current_value == 0
    assert audit.delay_4_perturbation_delay_4_value == r
    assert audit.delay_4_perturbation_delay_5_value == 0
    assert audit.delay_4_perturbation_period_delay_value == 0
    assert (
        audit.delay_4_fast_field_difference
        == audit.delay_4_perturbation_current_derivative
    )
    assert audit.delay_4_fast_field_difference == (
        sp.sqrt(5) * r * (r**2 + 3 * r + 7) / 200
    )
    assert (
        audit.delay_4_unit_witness_difference
        == 11 * sp.sqrt(5) / 200
    )
    assert audit.delay_4_unit_witness_difference > 0


def test_all_three_histories_are_exactly_solution_manifold_compatible() -> None:
    audit = reference_compatible_history_fiber_audit()
    assert compatible_history_fiber_algebra_is_exact(audit)
    assert audit.base_solution_manifold_compatibility_defect == sp.zeros(2, 1)
    assert (
        audit.period_solution_manifold_compatibility_defect
        == sp.zeros(2, 1)
    )
    assert (
        audit.delay_4_solution_manifold_compatibility_defect
        == sp.zeros(2, 1)
    )


def test_raw_and_compatible_endpoint_counts_are_not_conflated() -> None:
    audit = reference_compatible_endpoint_count_audit()
    assert audit.raw_history_coefficient_dimension == 194
    assert audit.value_continuous_history_dimension == 194
    assert audit.global_c1_internal_derivative_continuity_codimension == 30
    assert audit.global_c1_history_dimension == 164
    assert audit.endpoint_compatibility_codimension == 2
    assert audit.discrete_endpoint_compatible_level_dimension == 192
    assert audit.global_c1_endpoint_compatible_level_dimension == 162
    assert audit.scalar_current_exit_constraints == 1
    assert audit.exit_observable_transverse_at_witness
    assert audit.scalar_exit_fiber_dimension_on_discrete_endpoint_level == 191
    assert (
        audit.scalar_exit_fiber_dimension_on_global_c1_compatible_level
        == 161
    )
    assert audit.repelling_chart_dimension_inside_solution_manifold == 1
    assert (
        audit.scalar_exit_fiber_excess_over_repelling_curve_on_discrete_level
        == 190
    )
    assert (
        audit.scalar_exit_fiber_excess_over_repelling_curve_on_global_c1_level
        == 160
    )
    assert audit.repelling_curve_codimension_in_raw_history_space == 193
    assert audit.repelling_curve_codimension_on_discrete_endpoint_level == 191
    assert (
        audit.repelling_curve_codimension_on_global_c1_compatible_level
        == 161
    )
    assert audit.raw_net_endpoint_conditions == 193
    assert audit.ambient_incoming_coordinate_dimension_reported_by_candidate == 193
    assert audit.ambient_incoming_compatibility_rows == 2
    assert audit.effective_discrete_incoming_zero_fiber_dimension == 191
    assert audit.ambient_repaired_775_by_774_ledger_is_arithmetic_only
    assert not audit.global_c1_or_w2_multicell_realization_validated
    assert not audit.candidate_193_plus_1_is_compatible_fredholm_count_validated
    assert len(audit.unresolved_alternatives) == 3


def test_invariant_chart_contract_tracks_history_phase_parameters_and_flight() -> None:
    assert invariant_chart_backward_extension_identity_is_exact()
    contract = reference_selected_repelling_endpoint_contract()
    assert "X_phys=C([-T_*,0]" in contract.physical_phase_space
    assert "X_fold=C([-Theta_*,0]" in contract.physical_phase_space
    assert "M^1_{a,eta}" in contract.strong_solution_manifold
    assert "M^1_fold_{nu,eta}" in contract.strong_solution_manifold
    assert "partial_theta Gamma" in contract.shift_invariance_equation
    assert "F(Gamma^r" in contract.boundary_invariance_equation
    assert "backward scalar flow" in contract.backward_extension_identity
    assert "chi(Gamma^r" in contract.phase_coordinate
    assert contract.a_vector_field_column == "partial_a F=(0,-1/5)^T"
    assert "V(-T_*)" in contract.eta_vector_field_column
    assert "frozen plant delay" in contract.period_delay_parameter_convention
    assert "translated-history derivative" in contract.period_delay_parameter_convention
    assert "Gamma_{xi,lambda}" in contract.parameter_shift_sensitivity
    assert "Gamma_lambda+F_lambda" in contract.parameter_boundary_sensitivity
    assert "Gamma_a=5 Gamma_nu" in contract.physical_a_to_scaled_nu_conversion
    assert "D S_delta" in contract.physical_a_to_scaled_nu_conversion
    assert "q_fold=q_phys/delta" in contract.physical_a_to_scaled_nu_conversion
    assert "End_{L_+}x^+" in contract.right_flight_endpoint_residual
    assert "in X_phys" in contract.right_flight_endpoint_residual
    assert "dot x^+" in contract.moving_time_endpoint_derivative
    assert len(contract.minimum_validation_gates) == 7


def test_certificate_refuses_every_unvalidated_selected_chart_claim() -> None:
    certificate = reference_selected_repelling_endpoint_certificate()
    assert certificate.exact_quadratic_rfde_used
    assert certificate.full_period_horizon_used
    assert (
        certificate.same_current_and_same_scalar_exit_compatible_histories_constructed
    )
    assert certificate.eta_nonzero_period_atom_future_nonuniqueness_validated
    assert certificate.eta_zero_baseline_delay_future_nonuniqueness_validated
    assert not certificate.scalar_exit_observable_determines_complete_history_validated
    assert not certificate.scalar_exit_observable_determines_right_flight_validated
    assert not certificate.scalar_exit_observable_is_one_dimensional_repelling_chart_validated
    assert certificate.required_chart_is_inside_solution_manifold
    assert certificate.invariant_chart_implies_local_backward_extension_validated
    assert certificate.repaired_ambient_775_by_774_arithmetic_validated
    assert not certificate.repaired_ledger_strong_fredholm_operator_validated
    assert not certificate.backward_extendible_selected_repelling_chart_constructed
    assert not certificate.selected_chart_parameter_a_derivative_validated
    assert not certificate.selected_chart_parameter_eta_derivative_validated
    assert not certificate.selected_chart_phase_transversality_validated
    assert not certificate.right_flight_to_selected_chart_validated
    assert not certificate.fixed_epsilon_selected_root_validated
    assert not certificate.fixed_epsilon_root_response_validated
    assert not certificate.physical_onset_validated


def test_parent_artifacts_are_pinned() -> None:
    pairs = (
        (
            "experiments/results/fixed_epsilon_quadratic_root_bvp.json",
            FIXED_EPSILON_BVP_RESULT_SHA256,
        ),
        (
            "experiments/results/fixed_epsilon_two_sided_candidate.json",
            TWO_SIDED_CANDIDATE_RESULT_SHA256,
        ),
    )
    for relative_path, expected in pairs:
        assert sha256((REPOSITORY / relative_path).read_bytes()).hexdigest() == expected


def test_payload_rejects_selected_chart_or_root_promotion() -> None:
    payload = reference_selected_repelling_endpoint_payload()
    validate_selected_repelling_endpoint_payload(payload)
    for key in (
        "backward_extendible_selected_repelling_chart",
        "validated_chart_eta_derivative",
        "validated_right_flight_endpoint_composition",
        "validated_strong_fredholm_endpoint_operator",
        "fixed_epsilon_selected_root",
        "fixed_epsilon_root_response",
        "physical_onset",
    ):
        hostile = deepcopy(payload)
        hostile["scope"][key] = True
        with pytest.raises(ValueError, match="changed or promoted"):
            validate_selected_repelling_endpoint_payload(hostile)
    hostile = deepcopy(payload)
    hostile["scope"]["repaired_ambient_775_by_774_arithmetic"] = False
    with pytest.raises(ValueError, match="changed or promoted"):
        validate_selected_repelling_endpoint_payload(hostile)


def test_generated_artifact_is_source_and_parent_bound() -> None:
    payload = _payload()
    validate_selected_repelling_endpoint_payload(payload["audit"])
    manifest = payload["manifest"]
    assert manifest["proof_source_sha256"] == sha256(SOURCE.read_bytes()).hexdigest()
    assert manifest["generator_sha256"] == sha256(GENERATOR.read_bytes()).hexdigest()
    assert (
        manifest["parent_sha256"]["fixed_epsilon_bvp_result"]
        == FIXED_EPSILON_BVP_RESULT_SHA256
    )
    assert (
        manifest["parent_sha256"]["two_sided_candidate_result"]
        == TWO_SIDED_CANDIDATE_RESULT_SHA256
    )
    assert all(manifest["parent_claim_checks"].values())


def test_default_generator_replay_is_byte_identical(tmp_path: Path) -> None:
    replay = tmp_path / "replay.json"
    subprocess.run(
        [
            sys.executable,
            "experiments/fixed_epsilon_selected_repelling_endpoint.py",
            "--output",
            str(replay),
        ],
        cwd=REPOSITORY,
        env={**os.environ, "PYTHONPATH": "build/testdeps:src"},
        check=True,
    )
    assert replay.read_bytes() == RESULT.read_bytes()


def test_frozen_files_are_bound() -> None:
    assert sha256(RESULT.read_bytes()).hexdigest() == EXPECTED_RESULT_SHA256
    assert sha256(NOTE.read_bytes()).hexdigest() == EXPECTED_NOTE_SHA256
    assert sha256(SOURCE.read_bytes()).hexdigest() == EXPECTED_SOURCE_SHA256
    assert sha256(GENERATOR.read_bytes()).hexdigest() == EXPECTED_GENERATOR_SHA256


def test_note_keeps_exact_result_contract_and_refusals_distinct() -> None:
    text = NOTE.read_text(encoding="utf-8")
    for phrase in (
        "Exact compatible-history counterexamples",
        "scalar exit is not an RFDE endpoint chart",
        "not by inversion of the ambient RFDE semiflow",
        "The fixed-\\(\\xi\\) gauge",
        "complete-history endpoint evaluation",
        "endpoint compatibility rows",
        "accepts the repaired arithmetic identity",
        "validated compatible Fredholm operator",
        "Fixed-\\(\\varepsilon\\) selected repelling chart",
        "**Open**",
    ):
        assert phrase in text
    assert "neither the complete history" in text
    assert "Input-independent physical onset | **Open**" in text
