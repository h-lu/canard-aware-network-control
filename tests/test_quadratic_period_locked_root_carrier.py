"""Hostile tests for the quadratic period-lock root carrier."""

from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys

import pytest
import sympy as sp

from canard_control.quadratic_period_locked_root_carrier import (
    quadratic_period_lock_algebra,
    quadratic_period_lock_algebra_is_exact,
    reference_quadratic_period_lock_certificate,
    reference_quadratic_period_lock_payload,
    validate_quadratic_period_lock_payload,
)


REPOSITORY = Path(__file__).resolve().parents[1]
RESULT = (
    REPOSITORY / "experiments/results/quadratic_period_locked_root_carrier.json"
)
SOURCE = (
    REPOSITORY / "src/canard_control/quadratic_period_locked_root_carrier.py"
)
NOTE = REPOSITORY / "docs/quadratic-period-locked-selected-root.md"


def test_exact_carrier_and_melnikov_identities() -> None:
    algebra = quadratic_period_lock_algebra()
    assert quadratic_period_lock_algebra_is_exact(algebra)
    delta, Theta = sp.symbols("delta Theta", positive=True, finite=True)
    assert algebra.constant_history_action == sp.zeros(3, 1)
    assert algebra.periodic_history_action == sp.zeros(3, 1)
    assert algebra.fold_linearization_action == sp.zeros(3, 1)
    assert algebra.pure_transverse_variation_action == sp.zeros(3, 1)
    assert algebra.linear_period_lock_pairing == 0
    assert algebra.quadratic_melnikov_pairing == Theta * sp.sqrt(2 * sp.pi) / 2
    assert algebra.baseline_unfolding_root == -sp.Rational(1, 8)
    assert algebra.inner_root_eta_coefficient == -delta * Theta / 2
    assert algebra.physical_root_eta_coefficient == -delta**3 * Theta / 2


def test_certificate_separates_asymptotic_from_fixed_epsilon_claims() -> None:
    certificate = reference_quadratic_period_lock_certificate()
    assert certificate.exact_balanced_carrier_identities_validated
    assert certificate.distinguished_periodic_orbit_preserved_for_every_eta
    assert certificate.qualitative_three_parameter_periodic_branch_proved
    assert certificate.center_periodic_frequency_amplitude_eta_column_zero
    assert not certificate.quantitative_eta_periodic_box_validated
    assert certificate.fold_state_and_fold_linearization_preserved
    assert certificate.pure_transverse_first_variation_zero
    assert not certificate.linear_carrier_leading_pairing_nonzero
    assert certificate.quadratic_carrier_leading_pairing_nonzero
    assert certificate.fixed_scaled_support_canonical_root_response_proved
    assert certificate.synchronous_response_coefficient_topology_independent
    assert certificate.synchronous_root_lifts_to_every_balanced_topology
    assert not certificate.full_network_selected_root_unique_for_every_balanced_topology
    assert not certificate.fixed_physical_delay_asymptotic_coefficient_proved
    assert not certificate.fixed_epsilon_one_fifth_rho_nonzero_validated
    assert not certificate.reference_leading_rho_candidate_is_rigorous_enclosure
    assert not certificate.physical_onset_identification_validated
    assert "enlarged-horizon" in certificate.older_history_selection
    assert "no arbitrary inert extension" in certificate.older_history_selection


def test_payload_rejects_fixed_epsilon_promotion() -> None:
    payload = reference_quadratic_period_lock_payload()
    validate_quadratic_period_lock_payload(payload)
    hostile = deepcopy(payload)
    hostile["scope"]["fixed_epsilon_one_fifth_nonzero_rho"] = True
    with pytest.raises(ValueError, match="does not match"):
        validate_quadratic_period_lock_payload(hostile)


def test_generated_record_is_source_bound() -> None:
    payload = json.loads(RESULT.read_text(encoding="utf-8"))
    validate_quadratic_period_lock_payload(payload["audit"])
    assert payload["manifest"]["proof_source_sha256"] == sha256(
        SOURCE.read_bytes()
    ).hexdigest()


def test_generator_replays_byte_for_byte(tmp_path: Path) -> None:
    output = tmp_path / "quadratic.json"
    subprocess.run(
        [
            sys.executable,
            str(
                REPOSITORY
                / "experiments/quadratic_period_locked_root_carrier.py"
            ),
            "--output",
            str(output),
        ],
        check=True,
        cwd=REPOSITORY,
    )
    assert output.read_bytes() == RESULT.read_bytes()


def test_note_keeps_preparation_scale_and_fixed_epsilon_seams_explicit() -> None:
    text = NOTE.read_text(encoding="utf-8")
    assert "phase space is fixed" in text
    assert "enlarged-horizon canonical" in text
    assert "arbitrary constant" in text
    assert "-\\frac{\\Theta_*}{2}\\delta^3\\eta" in text
    assert "-\\frac{T_*}{50}" in text
    assert "not a directed enclosure" in text
    assert "moving/coalescing-support" in text
    assert "input-independent event/root comparison" in text
