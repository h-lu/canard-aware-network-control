"""Hostile tests for the fixed-epsilon attracting-endpoint audit."""

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

from canard_control.fixed_epsilon_selected_attracting_endpoint_chart import (
    AUDIT_ID,
    BLUEPRINT_DOC_SHA256,
    BLUEPRINT_RESULT_SHA256,
    BLUEPRINT_SOURCE_SHA256,
    CANDIDATE_DOC_SHA256,
    CANDIDATE_RESULT_SHA256,
    CANDIDATE_SOURCE_SHA256,
    MODEL_ID,
    endpoint_chart_algebra_is_exact,
    expected_parent_sha256,
    reference_compatibility_audit,
    reference_dimension_audit,
    reference_old_history_audit,
    reference_repaired_bvp_ledger_audit,
    reference_selected_endpoint_certificate,
    validate_selected_endpoint_payload,
)


REPOSITORY = Path(__file__).resolve().parents[1]
RESULT = (
    REPOSITORY
    / "experiments/results/fixed_epsilon_selected_attracting_endpoint_chart.json"
)
NOTE = REPOSITORY / "docs/fixed-epsilon-selected-attracting-endpoint-chart.md"
SOURCE = (
    REPOSITORY
    / "src/canard_control/fixed_epsilon_selected_attracting_endpoint_chart.py"
)
GENERATOR = (
    REPOSITORY
    / "experiments/fixed_epsilon_selected_attracting_endpoint_chart.py"
)
EXPECTED_RESULT_SHA256 = (
    "a7355bd5a6a19c93fba171235dc69929c536e7b21810097a55b984313e6d10bc"
)
EXPECTED_NOTE_SHA256 = (
    "49c6886f7834d11f00d4eb47f38937b7c6b8a2395fbf0b744620ab30e4d78eda"
)
EXPECTED_SOURCE_SHA256 = (
    "2dc2fc28b722b7c7109311ffefb3388a3a623862155c177620195158fd43d457"
)
EXPECTED_GENERATOR_SHA256 = (
    "e8bcbb17e45b057d64896de2ec2bde00cdd7f8e0ce39ba16f39eb07e8d64f9ad"
)


def _record() -> dict:
    return json.loads(RESULT.read_text(encoding="utf-8"))


def test_raw_history_and_compatibility_dimensions_are_exact() -> None:
    audit = reference_dimension_audit()
    assert audit.polynomial_degree == 6
    assert audit.history_cells == 16
    assert audit.state_components == 2
    assert audit.scalar_history_dimension == 16 * 6 + 1 == 97
    assert audit.raw_history_dimension == 2 * 97 == 194
    assert audit.compatibility_equation_dimension == 2
    assert audit.compatibility_rank == 2
    assert audit.discrete_endpoint_compatible_level_dimension == 192
    assert "C0 across internal cell joins" in audit.raw_history_internal_regularity
    assert audit.compatible_level_is_discrete_endpoint_level_not_global_c1
    assert audit.internal_cell_joins == 15
    assert audit.global_c1_derivative_continuity_constraints == 30
    assert audit.global_c1_history_dimension == 164
    assert audit.global_c1_endpoint_compatible_level_dimension == 162
    assert audit.proposed_attracting_chart_dimension == 193
    assert audit.proposed_dimension_excess == 1
    assert not audit.proposed_fixed_parameter_immersion_possible


def test_last_cell_bump_is_an_exact_rank_two_witness() -> None:
    audit = reference_dimension_audit()
    assert audit.bump_degree == 3 <= audit.polynomial_degree
    assert audit.bump_value_at_left_join == 0
    assert audit.bump_derivative_at_left_join == 0
    assert audit.bump_value_at_current == 0
    assert audit.bump_derivative_at_current == 1
    assert audit.all_active_delays_outside_last_cell
    assert audit.compatibility_direction_matrix == sp.eye(2)
    assert audit.compatibility_direction_determinant == 1


def test_compatibility_bump_identity_and_retraction_are_exact() -> None:
    audit = reference_compatibility_audit()
    alpha, beta = sp.symbols("alpha beta", real=True)
    assert audit.bump_increment == sp.Matrix([alpha, beta])
    assert audit.bump_jacobian == sp.eye(2)
    assert audit.exact_retraction_residual == sp.zeros(2, 1)
    assert endpoint_chart_algebra_is_exact()


def test_parameter_compatibility_columns_have_correct_signs() -> None:
    audit = reference_compatibility_audit()
    x0, x_theta = sp.symbols("x0 x_theta", real=True)
    assert audit.partial_nu_compatibility == sp.Matrix(
        [0, -1 / sp.sqrt(5)]
    )
    assert audit.partial_eta_compatibility == sp.Matrix(
        [-(x0**2 - x_theta**2) / 5, 0]
    )
    assert "-partial_nu C=(0,delta)" in audit.nu_jet_identity
    assert "delta^2*(x0^2-x_theta^2)" in audit.eta_jet_identity
    assert "D_phiphi C" in audit.second_parameter_jet_identity


def test_time_tangent_is_inside_not_outside_compatible_tangent() -> None:
    dimension = reference_dimension_audit()
    certificate = reference_selected_endpoint_certificate()
    compatibility = reference_compatibility_audit()
    assert (
        dimension.maximum_discrete_level_coordinates_beside_one_time_tangent
        == 191
    )
    assert "D_phi C(x_t)[dot{x}_t]=0" in compatibility.time_tangent_identity
    assert not certificate.one_time_tangent_adds_dimension_outside_compatible_tangent
    assert not certificate.later_phase_condition_repairs_endpoint_rank_mismatch


def test_old_history_pair_is_base_inert_but_eta_jet_visible() -> None:
    audit = reference_old_history_audit()
    assert audit.scaled_horizon > 5
    assert audit.first_cell_right_endpoint < -5
    assert audit.first_cell_is_strictly_older_than_minus_five
    assert audit.old_bump_value_at_minus_horizon == 1
    assert audit.old_bump_value_at_first_join == 0
    assert audit.old_bump_derivative_at_first_join == 0
    assert audit.zero_history_compatibility_at_nu_eta_zero == sp.zeros(2, 1)
    assert (
        audit.old_bump_history_compatibility_at_nu_eta_zero
        == sp.zeros(2, 1)
    )
    assert audit.zero_history_eta_field_column == sp.zeros(2, 1)
    assert audit.old_bump_history_eta_field_column == sp.Matrix(
        [-sp.Rational(1, 5), 0]
    )
    assert audit.eta_compatibility_column_difference == sp.Matrix(
        [sp.Rational(1, 5), 0]
    )
    assert not audit.base_eta_zero_future_current_trajectory_distinguishes_old_extensions
    assert not audit.enlarged_history_semiflow_states_are_identical_before_old_tail_ages_out
    assert audit.eta_derivative_distinguishes_old_extensions
    assert not audit.eta_zero_dynamics_selects_parameter_coherent_old_extension


def test_repaired_ledger_preserves_one_cokernel_arithmetic_only() -> None:
    audit = reference_repaired_bvp_ledger_audit()
    assert audit.coefficients_per_branch == 2 * ((16 + 8) * 6 + 1) == 290
    assert audit.two_branch_coefficients == 580
    assert audit.total_phase_fixed_unknowns == 580 + 193 + 1 == 774
    assert audit.flow_rows_per_branch == 96
    assert audit.projected_history_rows_per_block == 192
    assert audit.projected_history_blocks == ("entry", "exit", "seam")
    assert audit.projected_history_rows_total == 576
    assert audit.explicit_compatibility_blocks == (
        "C_N(Gamma_-(xi_-))",
        "C_N(h^-_entry)",
        "C_N(h^+_seam)",
    )
    assert audit.explicit_compatibility_rows_total == 6
    assert audit.total_phase_fixed_residuals == 192 + 576 + 6 + 1 == 775
    assert audit.residual_minus_unknown == 1
    assert audit.transverse_effective_attracting_dimension == 193 - 2 == 191
    assert audit.arithmetic_count_is_consistent
    assert audit.ambient_193_chart_is_not_a_compatible_193_immersion
    assert not audit.selected_invariant_endpoint_operator_constructed


def test_certificate_separates_ambient_chart_from_compatible_immersion() -> None:
    certificate = reference_selected_endpoint_certificate()
    assert MODEL_ID == "synchronous-dual-scaffold-fhn-quadratic-period-lock"
    assert AUDIT_ID == "fixed-epsilon-quadratic-selected-attracting-endpoint-audit"
    assert certificate.model_id == MODEL_ID
    assert certificate.audit_id == AUDIT_ID
    assert certificate.raw_history_dimension_194_derived_exactly
    assert certificate.compatibility_residual_has_exact_rank_two
    assert certificate.discrete_endpoint_compatible_level_dimension_192_derived_exactly
    assert certificate.algebraic_parameter_coherent_compatible_retraction_constructed
    assert not certificate.advertised_193_dimensional_fixed_parameter_compatible_immersion_exists
    assert certificate.ambient_193_dimensional_parameterization_is_algebraically_admissible
    assert certificate.repaired_775_by_774_projected_compatibility_ledger_is_exact
    assert not certificate.repaired_ledger_selected_endpoint_operator_constructed


def test_certificate_keeps_selected_and_continuous_gates_open() -> None:
    certificate = reference_selected_endpoint_certificate()
    assert certificate.continuous_rfde_solution_manifold_smoothness_at_fixed_epsilon_validated
    assert not certificate.finite_discrete_selected_attracting_chart_constructed
    assert not certificate.finite_discrete_invariant_attracting_foliation_validated
    assert not certificate.continuous_rfde_selected_attracting_chart_constructed
    assert not certificate.continuous_rfde_selected_attracting_chart_nonexistence_proved
    assert not certificate.parameter_coherent_first_and_second_endpoint_jets_validated
    assert not certificate.corrected_fredholm_dimension_ledger_validated
    assert not certificate.fixed_epsilon_selected_root_validated
    assert "ambient 193 chart" in certificate.precise_finite_dimensional_verdict
    assert "old extension" in certificate.continuous_rfde_open_gate


def test_all_six_parent_hashes_are_pinned() -> None:
    pairs = (
        ("docs/fixed-epsilon-two-sided-candidate.md", CANDIDATE_DOC_SHA256),
        (
            "src/canard_control/fixed_epsilon_two_sided_candidate.py",
            CANDIDATE_SOURCE_SHA256,
        ),
        (
            "experiments/results/fixed_epsilon_two_sided_candidate.json",
            CANDIDATE_RESULT_SHA256,
        ),
        ("docs/fixed-epsilon-quadratic-root-bvp.md", BLUEPRINT_DOC_SHA256),
        (
            "src/canard_control/fixed_epsilon_quadratic_root_bvp.py",
            BLUEPRINT_SOURCE_SHA256,
        ),
        (
            "experiments/results/fixed_epsilon_quadratic_root_bvp.json",
            BLUEPRINT_RESULT_SHA256,
        ),
    )
    assert expected_parent_sha256() == {
        "candidate_doc": CANDIDATE_DOC_SHA256,
        "candidate_source": CANDIDATE_SOURCE_SHA256,
        "candidate_result": CANDIDATE_RESULT_SHA256,
        "blueprint_doc": BLUEPRINT_DOC_SHA256,
        "blueprint_source": BLUEPRINT_SOURCE_SHA256,
        "blueprint_result": BLUEPRINT_RESULT_SHA256,
    }
    for relative, expected in pairs:
        assert sha256((REPOSITORY / relative).read_bytes()).hexdigest() == expected


def test_payload_validates_and_rejects_dimension_or_scope_promotion() -> None:
    record = _record()
    validate_selected_endpoint_payload(record["audit"])
    hostile = deepcopy(record["audit"])
    hostile["exact_audits"]["finite_history_dimension"][
        "discrete_endpoint_compatible_level_dimension"
    ] = 193
    with pytest.raises(ValueError, match="exact finite algebra"):
        validate_selected_endpoint_payload(hostile)
    hostile = deepcopy(record["audit"])
    hostile["scope"]["continuous_rfde_selected_attracting_chart"] = True
    with pytest.raises(ValueError, match="strict claim boundary"):
        validate_selected_endpoint_payload(hostile)
    hostile = deepcopy(record["audit"])
    hostile["scope"]["repaired_selected_endpoint_operator"] = True
    with pytest.raises(ValueError, match="strict claim boundary"):
        validate_selected_endpoint_payload(hostile)


def test_manifest_is_source_generator_parent_and_claim_bound() -> None:
    manifest = _record()["manifest"]
    assert manifest["proof_source_sha256"] == sha256(SOURCE.read_bytes()).hexdigest()
    assert manifest["generator_sha256"] == sha256(GENERATOR.read_bytes()).hexdigest()
    assert manifest["parent_sha256"] == expected_parent_sha256()
    assert all(manifest["parent_claim_checks"].values())
    assert manifest["parent_claim_checks"][
        "candidate_entry_template_is_compatible_but_unselected"
    ]
    assert manifest["parent_claim_checks"]["blueprint_requires_solution_manifold"]


def test_generator_replays_byte_for_byte(tmp_path: Path) -> None:
    replay = tmp_path / "selected-endpoint.json"
    subprocess.run(
        [sys.executable, str(GENERATOR), "--output", str(replay)],
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


def test_note_states_narrow_no_go_repair_and_open_boundary() -> None:
    text = NOTE.read_text(encoding="utf-8")
    normalized = " ".join(text.split())
    for phrase in (
        "193-dimensional fixed-parameter immersion",
        "**inside** either compatible level",
        "ambient 193-coordinate endpoint parameterization",
        "endpoint-compatible level has dimension 192",
        "dimensions to 164 and 162",
        "exact arithmetic repair, not a constructed endpoint operator",
        "translation tangent is therefore already a direction",
        "enlarged history states still carry the shifted inert tail",
        "Parameter-coherent selected attracting chart | **Open**",
        "Fixed-\\(\\varepsilon\\) selected root | **Open**",
    ):
        assert phrase in normalized
