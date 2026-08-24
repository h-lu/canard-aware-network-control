"""Hostile tests for the selected-Fredholm structural repair."""

from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys

import pytest
import sympy as sp

from canard_control.fixed_epsilon_quadratic_root_bvp import (
    THETA_PERIOD_DIAGNOSTIC,
)
from canard_control.fixed_epsilon_selected_fredholm_structure import (
    BLUEPRINT_NOTE_SHA256,
    BLUEPRINT_RESULT_SHA256,
    BLUEPRINT_SOURCE_SHA256,
    CANDIDATE_NOTE_SHA256,
    CANDIDATE_RESULT_SHA256,
    CANDIDATE_SOURCE_SHA256,
    compatibility_jacobian_from_remainder,
    endpoint_bubble_right_inverse,
    exact_parameter_columns_are_valid,
    reference_claim_ledger,
    reference_compatibility_structure,
    reference_dimension_ledger,
    reference_selected_fredholm_structure_payload,
    retained_projection_matrix,
    stacked_compatibility_coordinates,
    validate_selected_fredholm_structure_payload,
    verify_exact_compatibility_structure,
)


REPOSITORY = Path(__file__).resolve().parents[1]
SOURCE = (
    REPOSITORY
    / "src/canard_control/fixed_epsilon_selected_fredholm_structure.py"
)
RESULT = (
    REPOSITORY
    / "experiments/results/fixed_epsilon_selected_fredholm_structure.json"
)
NOTE = REPOSITORY / "docs/fixed-epsilon-selected-fredholm-structure.md"
GENERATOR = (
    REPOSITORY / "experiments/fixed_epsilon_selected_fredholm_structure.py"
)
EXPECTED_RESULT_SHA256 = (
    "cd800d78a73f539c7f41cc1a8e0b859a93653f2feae1b83b643b2bfed4096529"
)
EXPECTED_NOTE_SHA256 = (
    "a930afe3d7b9bdd7629ebd54a156a719013bd3d83a515e7966b738161159a272"
)
EXPECTED_SOURCE_SHA256 = (
    "2741380ce30b2b99cfa41832bd57be2724eac236a424aba71877412cc0db4f08"
)
EXPECTED_GENERATOR_SHA256 = (
    "0e00a89513eb50f6cedce8fb3acd193165bc5898d06579bb1e9293639c07a535"
)
BLUEPRINT_SOURCE = (
    REPOSITORY / "src/canard_control/fixed_epsilon_quadratic_root_bvp.py"
)
BLUEPRINT_RESULT = (
    REPOSITORY / "experiments/results/fixed_epsilon_quadratic_root_bvp.json"
)
BLUEPRINT_NOTE = REPOSITORY / "docs/fixed-epsilon-quadratic-root-bvp.md"
CANDIDATE_SOURCE = (
    REPOSITORY / "src/canard_control/fixed_epsilon_two_sided_candidate.py"
)
CANDIDATE_RESULT = (
    REPOSITORY / "experiments/results/fixed_epsilon_two_sided_candidate.json"
)
CANDIDATE_NOTE = REPOSITORY / "docs/fixed-epsilon-two-sided-candidate.md"


def _digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def test_raw_and_compatible_dimensions_expose_the_old_hard_error() -> None:
    ledger = reference_dimension_ledger()
    assert ledger.scalar_history_dimension == 6 * 16 + 1 == 97
    assert ledger.raw_history_dimension == 2 * 97 == 194
    assert ledger.compatibility_rank == 2
    assert ledger.compatible_history_dimension == 192
    assert ledger.effective_attracting_trace_dimension == 191
    assert ledger.ambient_entry_chart_coordinates == 193
    claims = reference_claim_ledger()
    assert not claims.raw_775_count_without_compatibility_is_valid
    assert claims.effective_attracting_trace_dimension_if_transverse == 191
    assert not claims.entry_chart_compatibility_transversality_validated
    assert claims.exit_chart_compatibility_is_a_construction_hypothesis
    assert claims.raw_history_space_is_only_c0_across_cell_joins
    assert not claims.global_c1_or_w2_realization_validated
    assert not claims.internal_derivative_jump_rows_counted


def test_endpoint_bubbles_give_an_exact_rank_two_right_inverse() -> None:
    assert THETA_PERIOD_DIAGNOSTIC / 16 < 4
    assert verify_exact_compatibility_structure()
    structure = reference_compatibility_structure()
    assert structure.projection_shape == (192, 194)
    assert structure.bubble_right_inverse_shape == (194, 2)
    assert structure.delayed_samples_unchanged
    assert structure.projection_times_right_inverse_is_zero
    assert structure.compatibility_jacobian_times_right_inverse_is_identity
    assert structure.stacked_coordinate_jacobian_determinant == "1"
    assert structure.compatibility_rank_two_proved_for_every_frozen_history

    remainder = sp.Matrix(
        2,
        192,
        lambda i, j: sp.Rational((i + 2) * (j - 5), j + 17),
    )
    projection = retained_projection_matrix()
    right_inverse = endpoint_bubble_right_inverse()
    derivative = compatibility_jacobian_from_remainder(remainder)
    stacked = stacked_compatibility_coordinates(remainder)
    inverse = sp.eye(192).row_join(sp.zeros(192, 2)).col_join(
        (-remainder).row_join(sp.eye(2))
    )
    assert projection * right_inverse == sp.zeros(192, 2)
    assert derivative * right_inverse == sp.eye(2)
    assert stacked * inverse == sp.eye(194)
    assert inverse * stacked == sp.eye(194)


def test_repaired_ambient_and_intrinsic_ledgers_are_exact() -> None:
    ledger = reference_dimension_ledger()
    assert ledger.branch_state_coefficients == 2 * (6 * 24 + 1) == 290
    assert ledger.phase_fixed_unknown_dimension == 2 * 290 + 193 + 1 == 774
    assert ledger.flow_rows_per_branch == 2 * 6 * 8 == 96
    assert ledger.phase_fixed_residual_dimension == (
        2 * 96 + 3 * 192 + 6 + 1
    ) == 775
    assert ledger.jump_complement_square_dimension == 775
    assert ledger.gap_root_square_dimension == 776

    payload = reference_selected_fredholm_structure_payload()
    intrinsic = payload["intrinsic_compatible_ledger"]
    assert intrinsic["branch_coefficients_after_initial_compatibility"] == 288
    assert intrinsic["phase_fixed_unknown_dimension"] == (
        2 * 288 + 191 + 1
    ) == 768
    assert intrinsic["phase_fixed_residual_dimension"] == (
        2 * 96 + 3 * 192 + 1
    ) == 769
    assert intrinsic["intended_fredholm_index_if_all_analytic_gates_hold"] == -1


def test_three_history_equalities_are_replaced_not_dropped() -> None:
    payload = reference_selected_fredholm_structure_payload()
    blocks = payload["repaired_residual_order"]
    assert sum(int(block.rsplit(": ", 1)[1]) for block in blocks) == 775
    assert sum("projected" in block for block in blocks) == 3
    assert sum("compatibility" in block for block in blocks) == 3
    claims = reference_claim_ledger()
    assert not claims.three_raw_194_history_equalities_are_retained
    assert not claims.three_raw_equalities_are_simply_deleted
    assert claims.three_projected_equalities_plus_compatibility_rows_defined
    assert claims.terminal_compatibility_requires_right_inclusive_flow_collocation


def test_moving_delay_columns_have_the_exact_signs_and_delta_factors() -> None:
    assert exact_parameter_columns_are_valid()
    columns = reference_selected_fredholm_structure_payload()[
        "parameter_columns"
    ]
    assert columns["residual_convention"] == "R=x'-f"
    assert columns["nu_interior_column"] == "R_nu=(0,-delta)^T"
    assert columns["physical_period_column"].startswith("R_T=delta*R_Theta")
    assert "delta^3" in columns["physical_period_column"]
    assert columns["physical_period_column_at_eta_zero"] == "R_T|_{eta=0}=0"
    assert "delta^3" in columns["eta_period_mixed_column_at_eta_zero"]


def test_rectangular_border_and_adjoint_sign_are_pinned() -> None:
    contract = reference_selected_fredholm_structure_payload()[
        "rectangular_operator_contract"
    ]
    assert contract["operator"] == (
        "raw C0 ambient template L_N=D_z F_N in R^(775x774); "
        "nu,eta,d are excluded; the strong selected derivative "
        "requires a fresh realization and count"
    )
    assert contract["border"] == (
        "conditional raw-template border B_N=[L_N,-e_N] in R^(775x775)"
    )
    assert contract["normalization"] == "L_N^T psi=0 and psi^T e_N=1"
    assert contract["transpose_identity"] == "B_N^T psi=(0_774,-1)"
    assert "economy-SVD" in contract["cokernel_gate"]
    assert "fresh dimension count" in reference_selected_fredholm_structure_payload()[
        "minimal_next_certificate"
    ][3]


def test_payload_refuses_fredholm_root_and_rho_promotions() -> None:
    payload = reference_selected_fredholm_structure_payload()
    validate_selected_fredholm_structure_payload(payload)
    for path in (
        ("scope", "actual_selected_fredholm_operator"),
        ("scope", "global_c1_or_w2_collocation_ledger"),
        ("scope", "continuous_fredholm_theorem"),
        ("scope", "selected_root"),
        ("scope", "rho_enclosure"),
        ("claim_ledger", "actual_775_by_774_derivative_constructed"),
        ("claim_ledger", "bordered_inverse_validated"),
    ):
        hostile = deepcopy(payload)
        hostile[path[0]][path[1]] = True
        with pytest.raises(ValueError, match="does not match"):
            validate_selected_fredholm_structure_payload(hostile)


def test_generated_record_is_source_and_upstream_bound() -> None:
    assert _digest(BLUEPRINT_SOURCE) == BLUEPRINT_SOURCE_SHA256
    assert _digest(BLUEPRINT_RESULT) == BLUEPRINT_RESULT_SHA256
    assert _digest(BLUEPRINT_NOTE) == BLUEPRINT_NOTE_SHA256
    assert _digest(CANDIDATE_SOURCE) == CANDIDATE_SOURCE_SHA256
    assert _digest(CANDIDATE_RESULT) == CANDIDATE_RESULT_SHA256
    assert _digest(CANDIDATE_NOTE) == CANDIDATE_NOTE_SHA256
    payload = json.loads(RESULT.read_text(encoding="utf-8"))
    validate_selected_fredholm_structure_payload(payload["audit"])
    manifest = payload["manifest"]
    assert manifest["proof_source_sha256"] == _digest(SOURCE)
    assert manifest["generator_sha256"] == _digest(GENERATOR)
    assert manifest["blueprint_source_sha256"] == _digest(BLUEPRINT_SOURCE)
    assert manifest["blueprint_result_sha256"] == _digest(BLUEPRINT_RESULT)
    assert manifest["blueprint_note_sha256"] == _digest(BLUEPRINT_NOTE)
    assert manifest["candidate_source_sha256"] == _digest(CANDIDATE_SOURCE)
    assert manifest["candidate_result_sha256"] == _digest(CANDIDATE_RESULT)
    assert manifest["candidate_note_sha256"] == _digest(CANDIDATE_NOTE)


def test_generator_replays_byte_for_byte(tmp_path: Path) -> None:
    output = tmp_path / "fredholm-structure.json"
    subprocess.run(
        [
            sys.executable,
            str(
                REPOSITORY
                / "experiments/fixed_epsilon_selected_fredholm_structure.py"
            ),
            "--output",
            str(output),
        ],
        check=True,
        cwd=REPOSITORY,
    )
    assert output.read_bytes() == RESULT.read_bytes()


def test_frozen_files_are_bound() -> None:
    assert _digest(RESULT) == EXPECTED_RESULT_SHA256
    assert _digest(NOTE) == EXPECTED_NOTE_SHA256
    assert _digest(SOURCE) == EXPECTED_SOURCE_SHA256
    assert _digest(GENERATOR) == EXPECTED_GENERATOR_SHA256


def test_note_states_the_hard_error_repair_and_claim_refusal() -> None:
    text = NOTE.read_text(encoding="utf-8")
    compact = " ".join(text.split())
    assert "compatible layer has dimension 192" in text
    assert "dimension 191, not 193" in compact
    assert "b(u)=\\ell u(u-1)" in text
    assert "[I_{192}\\ \\ 0]" in text
    assert "replaced**, not silently shortened" in text
    assert "775\\times774" in text
    assert "769\\times768" in text
    assert "B_N=[L_N,-e_N]" in text
    assert "B_N^T\\psi_N=(0_{774},-1)^T" in text
    assert "There is no extra factor of \\(T\\)" in text
    assert "repaired ambient ledger only" in compact
    assert "No derivative matching at the 15 internal joins is imposed" in text
    assert "Neither is yet a \\(W^{2,p}\\) Fredholm" in text
    assert "does not validate internal derivative continuity" in compact
