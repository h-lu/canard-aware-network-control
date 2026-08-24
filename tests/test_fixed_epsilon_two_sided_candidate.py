"""Hostile tests for the fixed-epsilon two-sided numerical candidate."""

from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys

import numpy as np
import pytest

import canard_control.fixed_epsilon_two_sided_candidate as candidate_module
from canard_control.fixed_epsilon_quadratic_root_bvp import DELTA
from canard_control.fixed_epsilon_two_sided_candidate import (
    BLUEPRINT_NOTE_SHA256,
    BLUEPRINT_RESULT_SHA256,
    BLUEPRINT_SOURCE_SHA256,
    compute_two_sided_candidate_row,
    reference_two_sided_candidate_certificate,
    reference_two_sided_candidate_payload,
    reference_two_sided_candidate_rows,
    validate_two_sided_candidate_payload,
)


REPOSITORY = Path(__file__).resolve().parents[1]
RESULT = (
    REPOSITORY
    / "experiments/results/fixed_epsilon_two_sided_candidate.json"
)
SOURCE = (
    REPOSITORY
    / "src/canard_control/fixed_epsilon_two_sided_candidate.py"
)
BLUEPRINT_SOURCE = (
    REPOSITORY / "src/canard_control/fixed_epsilon_quadratic_root_bvp.py"
)
BLUEPRINT_RESULT = (
    REPOSITORY
    / "experiments/results/fixed_epsilon_quadratic_root_bvp.json"
)
BLUEPRINT_NOTE = REPOSITORY / "docs/fixed-epsilon-quadratic-root-bvp.md"
NOTE = REPOSITORY / "docs/fixed-epsilon-two-sided-candidate.md"


def _digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def test_blueprint_bindings_are_exact_and_do_not_use_status_field() -> None:
    assert _digest(BLUEPRINT_SOURCE) == BLUEPRINT_SOURCE_SHA256
    assert _digest(BLUEPRINT_RESULT) == BLUEPRINT_RESULT_SHA256
    assert _digest(BLUEPRINT_NOTE) == BLUEPRINT_NOTE_SHA256
    source_text = SOURCE.read_text(encoding="utf-8")
    assert "exact_full_history_bvp_contract_specified" not in source_text
    assert "exact_full_history_bvp_contract_validated" not in source_text


def test_split_layout_is_square_and_contains_complete_scaled_horizon() -> None:
    for row in reference_two_sided_candidate_rows():
        assert row.represented_scaled_history >= row.active_scaled_history
        assert row.complete_history_node_count == (
            round(row.represented_scaled_history / row.mesh_step) + 1
        )
        expected_nodes = (
            row.complete_history_node_count
            + round(row.section_half_width / row.mesh_step)
        )
        assert row.full_dimension == 4 * expected_nodes + 2
        assert row.physical_history_diagnostic == pytest.approx(
            row.active_scaled_history / DELTA, abs=2.0e-14
        )


def test_actual_candidates_solve_every_residual_block() -> None:
    rows = reference_two_sided_candidate_rows()
    assert {(row.section_half_width, row.mesh_per_scaled_time) for row in rows} == {
        (3.0, 8),
        (3.0, 16),
        (3.0, 32),
        (2.5, 16),
        (3.5, 16),
    }
    assert max(row.total_residual_inf for row in rows) < 4.0e-12
    assert max(row.entry_residual_inf for row in rows) < 4.0e-13
    assert max(row.left_flow_residual_inf for row in rows) < 4.0e-12
    assert max(abs(row.phase_residual) for row in rows) < 1.0e-18
    assert max(row.complete_history_jump_inf for row in rows) < 1.0e-20
    assert max(row.right_flow_residual_inf for row in rows) < 2.0e-13
    assert max(abs(row.exit_gap_residual) for row in rows) < 2.0e-14
    assert all(row.minimum_lu_pivot > 0.25 for row in rows)


def test_mesh_refinement_is_second_order_but_section_drift_remains() -> None:
    certificate = reference_two_sided_candidate_certificate()
    assert 3.8 < float(certificate.central_nu_refinement_ratio) < 4.2
    assert 3.8 < float(certificate.central_rho_refinement_ratio) < 4.2
    assert float(certificate.central_mesh_nu_spread) < 6.1e-4
    assert float(certificate.central_mesh_rho_spread) < 6.0e-5
    assert float(certificate.section_nu_spread) > 0.10
    assert float(certificate.section_rho_spread) > 0.006
    finest = compute_two_sided_candidate_row(3.0, 32)
    assert finest.nu_candidate == pytest.approx(0.2125602223, abs=2.0e-10)
    assert finest.rho_adjoint_candidate == pytest.approx(
        -0.3463310348, abs=2.0e-10
    )


def test_discrete_adjoint_direct_tangent_and_finite_difference_agree() -> None:
    for row in reference_two_sided_candidate_rows():
        assert row.discrete_m_nu == pytest.approx(1.0, abs=3.0e-15)
        assert row.entry_solution_manifold_compatibility_defect < 3.0e-16
        assert row.adjoint_residual_inf < 1.4e-15
        assert row.adjoint_normalization_error < 3.0e-15
        assert row.adjoint_direct_disagreement < 4.0e-16
        assert row.adjoint_finite_difference_disagreement < 5.0e-9
        assert row.rho_adjoint_candidate == pytest.approx(
            -DELTA**2 * row.discrete_m_eta / row.discrete_m_nu,
            abs=2.0e-15,
        )


def test_analytic_state_and_eta_columns_match_finite_differences() -> None:
    vector, evaluation, _, _ = candidate_module._newton_solve(3.0, 4, 0.0)
    rng = np.random.default_rng(20260824)
    direction = rng.standard_normal(vector.size)
    direction /= np.linalg.norm(direction)
    step = 2.0e-7
    plus = candidate_module._evaluate_system(vector + step * direction, 3.0, 4, 0.0)
    minus = candidate_module._evaluate_system(vector - step * direction, 3.0, 4, 0.0)
    difference = (plus.residual - minus.residual) / (2.0 * step)
    analytic = evaluation.jacobian @ direction
    assert np.max(np.abs(difference - analytic)) < 2.0e-8

    eta_plus = candidate_module._evaluate_system(vector, 3.0, 4, step)
    eta_minus = candidate_module._evaluate_system(vector, 3.0, 4, -step)
    eta_difference = (eta_plus.residual - eta_minus.residual) / (2.0 * step)
    assert np.max(np.abs(eta_difference - evaluation.eta_column)) < 2.0e-9


def test_certificate_refuses_selected_trace_root_and_enclosure() -> None:
    certificate = reference_two_sided_candidate_certificate()
    assert certificate.two_branch_discrete_candidate_computed
    assert certificate.parameter_coherent_entry_template_used
    assert certificate.entry_solution_manifold_compatibility_enforced
    assert certificate.phase_solved
    assert certificate.full_discrete_history_jump_solved
    assert certificate.finite_exit_observable_zero
    assert certificate.square_candidate_residual_solved
    assert certificate.discrete_full_residual_adjoint_computed
    assert not certificate.selected_attracting_trace_bundle_constructed
    assert not certificate.backward_extendible_repelling_bundle_constructed
    assert not certificate.correct_fredholm_endpoint_chart_count_implemented
    assert not certificate.selected_complete_history_bvp_solved
    assert not certificate.continuous_collocation_solution_validated
    assert not certificate.interval_inverse_or_tail_bound_validated
    assert not certificate.period_delay_uncertainty_propagated
    assert not certificate.continuous_advanced_adjoint_validated
    assert not certificate.fixed_epsilon_selected_root_validated
    assert not certificate.rho_star_enclosed_away_from_zero
    assert not certificate.physical_onset_or_capture_validated
    assert "193-dimensional" in certificate.minimal_failure
    assert "775x774" in certificate.minimal_failure


def test_faithful_next_count_and_backward_ivp_refusal_are_pinned() -> None:
    payload = reference_two_sided_candidate_payload()
    next_step = payload["faithful_next_discretization"]
    assert next_step["history_dimension"] == 194
    assert next_step["attracting_endpoint_chart_dimension"] == 193
    assert next_step["repelling_endpoint_chart_dimension"] == 1
    assert next_step["phase_fixed_residual_dimension"] == 775
    assert next_step["phase_fixed_unknown_dimension"] == 774
    assert next_step["jump_complement_square_dimension"] == 775
    assert next_step["root_system_square_dimension"] == 776
    assert next_step["terminal_repelling_chart_requires_collocation_continuation"]
    assert next_step["backward_ivp_is_not_an_admissible_substitute"]


def test_frozen_finest_primal_and_adjoint_rebuild_the_equations() -> None:
    payload = reference_two_sided_candidate_payload()
    frozen = payload["finest_primal_and_adjoint_candidate"]
    primal = np.asarray(frozen["primal_components"], dtype="<f8")
    adjoint = np.asarray(frozen["adjoint_components"], dtype="<f8")
    assert frozen["dimension"] == primal.size == adjoint.size == 1338
    assert sha256(primal.tobytes()).hexdigest() == frozen[
        "primal_binary64_sha256"
    ]
    assert sha256(adjoint.tobytes()).hexdigest() == frozen[
        "adjoint_binary64_sha256"
    ]
    evaluation = candidate_module._evaluate_system(primal, 3.0, 32, 0.0)
    layout = evaluation.layout
    assert np.max(np.abs(evaluation.residual)) < 8.0e-15
    jacobian_without_nu = evaluation.jacobian[:, : layout.nu_column]
    nu_column = np.asarray(
        evaluation.jacobian[:, layout.nu_column].toarray()
    ).ravel()
    assert np.max(np.abs(jacobian_without_nu.T @ adjoint)) < 8.0e-16
    assert adjoint @ nu_column == pytest.approx(1.0, abs=2.0e-15)
    rho = -DELTA**2 * (adjoint @ evaluation.eta_column) / (
        adjoint @ nu_column
    )
    assert rho == pytest.approx(-0.3463310348461952, abs=2.0e-15)


def test_payload_rejects_false_selected_root_or_rho_enclosure() -> None:
    payload = reference_two_sided_candidate_payload()
    validate_two_sided_candidate_payload(payload)
    for key in ("selected_root", "rho_enclosure"):
        hostile = deepcopy(payload)
        hostile["scope"][key] = True
        with pytest.raises(ValueError, match="does not match"):
            validate_two_sided_candidate_payload(hostile)


def test_generated_record_is_source_and_blueprint_bound() -> None:
    payload = json.loads(RESULT.read_text(encoding="utf-8"))
    validate_two_sided_candidate_payload(payload["audit"])
    manifest = payload["manifest"]
    assert manifest["proof_source_sha256"] == _digest(SOURCE)
    assert manifest["blueprint_source_sha256"] == _digest(BLUEPRINT_SOURCE)
    assert manifest["blueprint_result_sha256"] == _digest(BLUEPRINT_RESULT)
    assert manifest["blueprint_note_sha256"] == _digest(BLUEPRINT_NOTE)


def test_generator_replays_byte_for_byte(tmp_path: Path) -> None:
    output = tmp_path / "two-sided.json"
    subprocess.run(
        [
            sys.executable,
            str(REPOSITORY / "experiments/fixed_epsilon_two_sided_candidate.py"),
            "--output",
            str(output),
        ],
        check=True,
        cwd=REPOSITORY,
    )
    assert output.read_bytes() == RESULT.read_bytes()


def test_note_reports_candidate_convergence_adjoint_and_exact_refusal() -> None:
    text = NOTE.read_text(encoding="utf-8")
    assert "two-sided full-history-matched candidate" in text
    assert "z^+|_{[-H_N,0]}-z^-|_{[-H_N,0]}" in text
    assert "K_N^T\\psi_N=e_{M_N}" in text
    assert "-\\delta^2\\frac{m_{\\eta,N}}{m_{\\nu,N}}" in text
    assert "-0.3463310348461952" in text
    assert "solution-manifold compatibility" in text
    assert "238 two-state history nodes, hence 476 scalar history" in text
    assert "second-order" in text
    assert "section spreads" in text
    assert "wrong Fredholm endpoint geometry" in text
    assert "Fixed-\\(\\varepsilon\\) selected root | **Open**" in text
    assert "Enclosure \\(0\\notin\\rho_*\\) | **Open**" in text
