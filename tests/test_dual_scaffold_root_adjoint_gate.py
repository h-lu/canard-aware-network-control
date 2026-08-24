"""Hostile tests for the fixed-epsilon selected-root adjoint gate."""

from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys

import pytest
import sympy as sp

from canard_control.dual_scaffold_root_adjoint_gate import (
    reference_root_adjoint_gate_certificate,
    reference_root_adjoint_gate_payload,
    root_adjoint_gate_algebra,
    root_adjoint_gate_is_exact,
    validate_root_adjoint_gate_payload,
)


REPOSITORY = Path(__file__).resolve().parents[1]
RESULT = REPOSITORY / "experiments/results/dual_scaffold_root_adjoint_gate.json"
SOURCE = REPOSITORY / "src/canard_control/dual_scaffold_root_adjoint_gate.py"
NOTE = REPOSITORY / "docs/dual-scaffold-period-locked-root-adjoint-gate.md"


def test_exact_residual_columns_and_parity_cancellation() -> None:
    algebra = root_adjoint_gate_algebra()
    assert root_adjoint_gate_is_exact(algebra)
    assert algebra.singular_fast_adjoint_pairing == 0
    assert algebra.clamped_zero_period_lock_action == 0
    assert algebra.clamped_zero_fast_residual == 0
    assert algebra.clamped_zero_recovery_residual == 0
    assert sp.simplify(algebra.actual_first_moment_scalar) != 0


def test_open_gates_are_not_promoted() -> None:
    certificate = reference_root_adjoint_gate_certificate()
    assert certificate.exact_adjoint_ratio_theorem_validated
    assert certificate.residual_columns_validated
    assert certificate.nonzero_first_moment_validated
    assert not certificate.leading_singular_interior_pairing_nonzero
    assert not certificate.nonzero_moment_implies_nonzero_selected_root_response
    assert certificate.clamped_zero_reset_equilibrium_for_all_eta_validated
    assert not certificate.clamped_operational_threshold_supplies_nonzero_eta_column
    assert not certificate.same_extended_rfde_selected_root_validated
    assert not certificate.augmented_complete_history_bvp_inverse_validated
    assert not certificate.dynamic_adjoint_with_endpoint_multipliers_validated
    assert not certificate.nonzero_selected_root_eta_response_validated
    assert not certificate.fixed_epsilon_one_fifth_overlap_validated
    assert not certificate.arbitrary_balanced_topology_full_root_validated
    assert not certificate.input_independent_physical_onset_comparison_validated


def test_payload_rejects_false_promotion() -> None:
    payload = reference_root_adjoint_gate_payload()
    validate_root_adjoint_gate_payload(payload)
    hostile = deepcopy(payload)
    hostile["scope"]["nonzero_rho_star"] = True
    with pytest.raises(ValueError, match="does not match"):
        validate_root_adjoint_gate_payload(hostile)


def test_generated_record_is_source_bound() -> None:
    payload = json.loads(RESULT.read_text(encoding="utf-8"))
    validate_root_adjoint_gate_payload(payload["audit"])
    assert payload["manifest"]["proof_source_sha256"] == sha256(
        SOURCE.read_bytes()
    ).hexdigest()


def test_generator_replays_byte_for_byte(tmp_path: Path) -> None:
    output = tmp_path / "gate.json"
    subprocess.run(
        [
            sys.executable,
            str(REPOSITORY / "experiments/dual_scaffold_root_adjoint_gate.py"),
            "--output",
            str(output),
        ],
        check=True,
        cwd=REPOSITORY,
    )
    assert output.read_bytes() == RESULT.read_bytes()


def test_note_states_ratio_cancellation_and_open_fixed_epsilon_gate() -> None:
    text = NOTE.read_text(encoding="utf-8")
    assert "\\partial_\\eta a_c(0)" in text
    assert "nonzero delay moment" in text
    assert "=0" in text
    assert "Not yet validated" in text
    assert "input-independent" in text
