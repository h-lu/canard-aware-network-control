"""Hostile tests for the fixed-epsilon quadratic-root BVP gate."""

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
    fixed_epsilon_bvp_algebra,
    fixed_epsilon_bvp_algebra_is_exact,
    reference_fixed_epsilon_bvp_contract,
    reference_fixed_epsilon_quadratic_root_certificate,
    reference_fixed_epsilon_quadratic_root_payload,
    reference_shooting_rows,
    shooting_row,
    validate_fixed_epsilon_quadratic_root_payload,
)


REPOSITORY = Path(__file__).resolve().parents[1]
RESULT = (
    REPOSITORY
    / "experiments/results/fixed_epsilon_quadratic_root_bvp.json"
)
SOURCE = (
    REPOSITORY / "src/canard_control/fixed_epsilon_quadratic_root_bvp.py"
)
NOTE = REPOSITORY / "docs/fixed-epsilon-quadratic-root-bvp.md"


def test_exact_chart_columns_and_zero_period_delay_linearization() -> None:
    algebra = fixed_epsilon_bvp_algebra()
    assert fixed_epsilon_bvp_algebra_is_exact(algebra)
    assert algebra.epsilon == sp.Rational(1, 5)
    assert algebra.physical_delay_0 == 4 * sp.sqrt(5)
    assert algebra.physical_delay_1 == 5 * sp.sqrt(5)
    assert algebra.period_delay_linearization_at_eta_zero == sp.zeros(2)
    assert algebra.a_residual_column == sp.Matrix([0, sp.Rational(1, 5)])


def test_contract_requires_full_history_jump_and_dynamic_adjoint() -> None:
    contract = reference_fixed_epsilon_bvp_contract()
    assert "-h<=theta<=0" in contract.complete_history_jump
    assert "W^{2,p}" in contract.strong_left_domain
    assert "W^{2,p}" in contract.strong_right_domain
    assert "A_j(t+tau_j)^T" in contract.dynamic_adjoint
    assert "entry, exit, phase, seam, and jump" in contract.dynamic_adjoint
    assert "isomorphism" in contract.augmented_operator
    assert contract.root_response == "rho_*=-m_eta/m_a"
    assert len(contract.required_validation_gates) == 8


def test_shooting_candidate_has_expected_sign_and_section_drift() -> None:
    rows = reference_shooting_rows()
    assert tuple(row.section_half_width for row in rows) == (2.5, 3.0, 3.5)
    assert all(row.forward_rho < 0.0 for row in rows)
    assert all(row.bracket_sign_margin > 0.0 for row in rows)
    assert all(row.scalar_gap_inverse_norm > 0.0 for row in rows)
    assert max(row.forward_rho for row in rows) - min(
        row.forward_rho for row in rows
    ) > 0.08
    assert max(abs(row.gap_residual) for row in rows) < 4.0e-8
    assert max(
        row.forward_finite_difference_disagreement for row in rows
    ) < 1.4e-6
    central = shooting_row(3.0)
    assert central.forward_rho == pytest.approx(-0.2809514461, abs=2.0e-9)
    assert central.a_root == pytest.approx(1.0327891472, abs=2.0e-9)


def test_certificate_refuses_every_unproved_promotion() -> None:
    certificate = reference_fixed_epsilon_quadratic_root_certificate()
    assert certificate.exact_full_history_bvp_contract_specified
    assert certificate.finite_section_shooting_diagnostic_computed
    assert not certificate.prescribed_older_history_is_selected_attracting_trace
    assert not certificate.selected_repelling_trace_constructed
    assert not certificate.complete_history_jump_solved
    assert not certificate.phase_fixed_augmented_inverse_validated
    assert not certificate.dynamic_adjoint_validated
    assert not certificate.interval_newton_or_radii_polynomial_validated
    assert not certificate.endpoint_zero_fiber_implication_validated
    assert not certificate.fixed_epsilon_selected_root_validated
    assert not certificate.fixed_epsilon_nonzero_rho_validated
    assert not certificate.physical_onset_identification_validated
    assert float(certificate.section_rho_spread) > 0.08


def test_payload_rejects_false_fixed_epsilon_root() -> None:
    payload = reference_fixed_epsilon_quadratic_root_payload()
    validate_fixed_epsilon_quadratic_root_payload(payload)
    hostile = deepcopy(payload)
    hostile["scope"]["fixed_epsilon_selected_root"] = True
    with pytest.raises(ValueError, match="does not match"):
        validate_fixed_epsilon_quadratic_root_payload(hostile)


def test_generated_record_is_source_bound() -> None:
    payload = json.loads(RESULT.read_text(encoding="utf-8"))
    validate_fixed_epsilon_quadratic_root_payload(payload["audit"])
    assert payload["manifest"]["proof_source_sha256"] == sha256(
        SOURCE.read_bytes()
    ).hexdigest()


def test_generator_replays_byte_for_byte(tmp_path: Path) -> None:
    output = tmp_path / "fixed.json"
    subprocess.run(
        [
            sys.executable,
            str(REPOSITORY / "experiments/fixed_epsilon_quadratic_root_bvp.py"),
            "--output",
            str(output),
        ],
        check=True,
        cwd=REPOSITORY,
    )
    assert output.read_bytes() == RESULT.read_bytes()


def test_note_states_equations_candidate_and_exact_refusal() -> None:
    text = NOTE.read_text(encoding="utf-8")
    assert "J(\\theta)=x^-(\\theta)-x^+(\\theta)" in text
    assert "\\rho_*=-\\frac{m_\\eta}{m_a}" in text
    assert "Y+(Z_1-1)r+Z_2(r)r^2<0" in text
    assert "-0.2809514461" in text
    assert "section dependence" in text
    assert "not the norm of the augmented complete-history inverse" in text
    assert "Fixed-\\(\\varepsilon\\) selected root | **Open**" in text
