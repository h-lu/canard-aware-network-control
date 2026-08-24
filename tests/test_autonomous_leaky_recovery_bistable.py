"""Audit tests for the autonomous leaky-recovery bistable RFDE proposal."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict, fields
from fractions import Fraction
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest
import sympy as sp

from canard_control.autonomous_leaky_recovery_bistable import (
    ALPHA_LOWER,
    ALPHA_UPPER,
    CANDIDATE_FLAGS,
    OPEN_FLAGS,
    OUTPUT_CONTROL_COORDINATES,
    PROVED_FLAGS,
    REFUSED_FLAGS,
    AutonomousBistableClaimLedger,
    EquilibriumStabilityCertificate,
    build_claim_ledger,
    build_equilibrium_stability_certificate,
    exact_equilibrium_algebra,
    json_ready_autonomous_bistable_audit,
    validate_autonomous_bistable_audit,
    validate_autonomous_bistable_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]
SOURCE = (
    REPOSITORY
    / "src/canard_control/autonomous_leaky_recovery_bistable.py"
)
GENERATOR = (
    REPOSITORY
    / "experiments/autonomous_leaky_recovery_bistable_probe.py"
)
RESULT = (
    REPOSITORY
    / "experiments/results/autonomous_leaky_recovery_bistable_probe.json"
)
NOTE = REPOSITORY / "docs/autonomous-leaky-recovery-bistable-rfde-proposal.md"
EXPECTED_RESULT_SHA256 = (
    "3361f43f0667ac7eafe25983d61ec999ca58baf0cabc807821088081ae78039b"
)


def _digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _result() -> dict:
    value = json.loads(RESULT.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def _fraction_interval(payload: dict[str, str]) -> tuple[Fraction, Fraction]:
    return (
        Fraction(payload["lower_fraction"]),
        Fraction(payload["upper_fraction"]),
    )


def test_equilibrium_and_characteristic_symbols_reconstruct_exactly() -> None:
    algebra = exact_equilibrium_algebra()
    alpha = algebra.equilibrium_voltage
    lam = algebra.spectral_parameter
    epsilon = algebra.epsilon
    current = algebra.current_coefficient
    gain = algebra.delayed_gain
    average = algebra.delay_average

    assert sp.simplify(alpha**3 - sp.Rational(3, 4)) == 0
    assert sp.simplify(
        algebra.equilibrium_recovery - (alpha - algebra.unfolding)
    ) == 0
    assert sp.simplify(
        alpha - alpha**3 / 3 - algebra.equilibrium_recovery
    ) == 0
    assert sp.simplify(current - (1 - alpha**2 - gain)) == 0
    assert sp.simplify(
        algebra.characteristic_determinant
        - ((lam - current - gain * average) * (lam + epsilon) + epsilon)
    ) == 0
    assert sp.simplify(
        algebra.reference_polynomial
        - ((lam - current) * (lam + epsilon) + epsilon)
    ) == 0

    omega = sp.symbols("omega", real=True)
    real_part = epsilon * (1 - current) - omega**2
    imaginary_coefficient = epsilon - current
    boundary_difference = sp.expand(
        real_part**2
        + omega**2 * imaginary_coefficient**2
        - gain**2 * (omega**2 + epsilon**2)
    )
    expected = omega**4 + algebra.beta * omega**2 + algebra.gamma
    assert sp.simplify(boundary_difference - expected) == 0


def test_exact_rational_interval_certificate_has_strict_margins() -> None:
    certificate = asdict(build_equilibrium_stability_certificate())
    assert ALPHA_LOWER**3 < Fraction(3, 4) < ALPHA_UPPER**3
    assert certificate["alpha_interval"]["lower_fraction"] == "1817/2000"
    assert certificate["alpha_interval"]["upper_fraction"] == "4543/5000"

    gain = _fraction_interval(certificate["effective_delay_gain_interval"])
    current = _fraction_interval(certificate["current_coefficient_interval"])
    epsilon_minus = _fraction_interval(
        certificate["epsilon_minus_current_interval"]
    )
    beta = _fraction_interval(certificate["beta_interval"])
    gamma = _fraction_interval(certificate["gamma_interval"])
    margin = _fraction_interval(
        certificate["four_gamma_minus_beta_squared_interval"]
    )
    assert Fraction(825, 1_000_000) < gain[0] < gain[1]
    assert Fraction(173, 1_000) < current[0] < current[1] < Fraction(174, 1_000)
    assert epsilon_minus[0] > Fraction(26, 1_000)
    assert beta[1] < 0
    assert gamma[0] > Fraction(27, 1_000)
    assert margin[0] > Fraction(1, 2_500)

    proof_flags = {
        field.name
        for field in fields(EquilibriumStabilityCertificate)
        if field.name.endswith("_proved")
    }
    assert proof_flags
    assert all(certificate[name] is True for name in proof_flags)


def test_claim_ledger_is_exhaustive_and_keeps_open_gates_false() -> None:
    ledger = asdict(build_claim_ledger())
    declared = PROVED_FLAGS | CANDIDATE_FLAGS | OPEN_FLAGS | REFUSED_FLAGS
    schema = {field.name for field in fields(AutonomousBistableClaimLedger)}
    assert schema == declared
    assert all(ledger[name] is True for name in PROVED_FLAGS)
    assert all(ledger[name] is True for name in CANDIDATE_FLAGS)
    assert all(ledger[name] is False for name in OPEN_FLAGS)
    assert all(ledger[name] is False for name in REFUSED_FLAGS)
    assert OUTPUT_CONTROL_COORDINATES == (
        "unfolding_a",
        "kappa_3",
        "pulse_amplitude_J",
    )


def test_audit_rejects_promotion_weakening_wrong_types_and_algebra_tampering() -> None:
    audit = json_ready_autonomous_bistable_audit()

    promoted = deepcopy(audit)
    promoted["claim_ledger"][next(iter(OPEN_FLAGS))] = True
    with pytest.raises(ValueError, match="open theorem gate was promoted"):
        validate_autonomous_bistable_audit(promoted)

    weakened = deepcopy(audit)
    weakened["claim_ledger"][next(iter(PROVED_FLAGS))] = False
    with pytest.raises(ValueError, match="proved equilibrium/autonomy flag"):
        validate_autonomous_bistable_audit(weakened)

    wrong_type = deepcopy(audit)
    wrong_type["equilibrium_certificate"][
        "local_exponential_equilibrium_stability_proved"
    ] = 1
    with pytest.raises(ValueError, match="wrong type"):
        validate_autonomous_bistable_audit(wrong_type)

    wrong_formula = deepcopy(audit)
    wrong_formula["equilibrium_certificate"]["beta_formula"] = "beta=0"
    with pytest.raises(ValueError, match="differs from reference"):
        validate_autonomous_bistable_audit(wrong_formula)

    wrong_interval = deepcopy(audit)
    wrong_interval["equilibrium_certificate"]["gamma_interval"][
        "lower_fraction"
    ] = "0"
    with pytest.raises(ValueError, match="differs from reference"):
        validate_autonomous_bistable_audit(wrong_interval)


def test_result_manifest_controls_and_reference_audit_revalidate() -> None:
    payload = _result()
    validate_autonomous_bistable_result(payload, REPOSITORY)
    manifest = payload["manifest"]
    assert manifest["proof_source_sha256"] == _digest(SOURCE)
    assert manifest["generator_sha256"] == _digest(GENERATOR)
    assert manifest["note_sha256"] == _digest(NOTE)
    assert manifest["output_control_coordinates"] == [
        "unfolding_a",
        "kappa_3",
        "pulse_amplitude_J",
    ]
    assert payload["frequency_amplitude_response_candidate"]["controls"] == [
        "unfolding_a",
        "kappa_3",
    ]
    assert _digest(RESULT) == EXPECTED_RESULT_SHA256


def test_result_validator_rejects_coordinate_claim_and_hash_tampering() -> None:
    payload = _result()

    for missing_key in (
        "ode_diagnostic",
        "rfde_periodic_candidates",
        "constant_history_kick_diagnostic",
    ):
        missing_evidence = deepcopy(payload)
        missing_evidence.pop(missing_key)
        with pytest.raises(ValueError, match="candidate evidence"):
            validate_autonomous_bistable_result(missing_evidence, REPOSITORY)

    nonfinite_period = deepcopy(payload)
    nonfinite_period["rfde_periodic_candidates"]["outer_pulse"]["period"] = (
        "nan"
    )
    with pytest.raises(ValueError, match="period is nonfinite"):
        validate_autonomous_bistable_result(nonfinite_period, REPOSITORY)

    missing_monodromy = deepcopy(payload)
    missing_monodromy["rfde_periodic_candidates"]["inner_saddle_candidate"][
        "monodromy_diagnostic"
    ] = []
    with pytest.raises(ValueError, match="monodromy evidence is missing"):
        validate_autonomous_bistable_result(missing_monodromy, REPOSITORY)

    epsilon_control = deepcopy(payload)
    epsilon_control["frequency_amplitude_response_candidate"]["controls"] = [
        "unfolding_a",
        "epsilon",
    ]
    with pytest.raises(ValueError, match=r"not \(a,kappa_3\)"):
        validate_autonomous_bistable_result(epsilon_control, REPOSITORY)

    threshold_promotion = deepcopy(payload)
    threshold_promotion["finite_duration_physical_pulse_diagnostic"][
        "unique_threshold_validated"
    ] = True
    with pytest.raises(ValueError, match="promoted to onset proof"):
        validate_autonomous_bistable_result(threshold_promotion, REPOSITORY)

    ledger_promotion = deepcopy(payload)
    ledger_promotion["audit"]["claim_ledger"][next(iter(OPEN_FLAGS))] = True
    ledger_promotion["claim_status"] = ledger_promotion["audit"][
        "claim_ledger"
    ]
    with pytest.raises(ValueError, match="open theorem gate was promoted"):
        validate_autonomous_bistable_result(ledger_promotion, REPOSITORY)

    bad_hash = deepcopy(payload)
    bad_hash["manifest"]["proof_source_sha256"] = "0" * 64
    with pytest.raises(ValueError, match="proof_source SHA-256 changed"):
        validate_autonomous_bistable_result(bad_hash, REPOSITORY)


def test_generator_replays_committed_result_bytes(tmp_path: Path) -> None:
    replay = tmp_path / "autonomous-leaky-recovery-bistable.json"
    environment = {
        **os.environ,
        "PYTHONPATH": "src",
        "OMP_NUM_THREADS": "1",
        "OPENBLAS_NUM_THREADS": "1",
        "MKL_NUM_THREADS": "1",
        "PYTHONHASHSEED": "0",
    }
    subprocess.run(
        [sys.executable, str(GENERATOR), "--output", str(replay)],
        cwd=REPOSITORY,
        env=environment,
        check=True,
    )
    assert replay.read_bytes() == RESULT.read_bytes()


def test_note_uses_rfde_history_space_and_local_routing_only() -> None:
    note = NOTE.read_text(encoding="utf-8")
    normalized = " ".join(note.split())
    assert "isolating annulus" not in normalized.lower()
    assert "X=C([-\\tau _1,0],\\mathbb R^2)" in normalized
    assert "Within the same history-space block" in normalized
    assert "local pulse-history tube" in normalized
    assert "pulled back to \\(X\\)" in normalized
    assert "the terminal-history map" in normalized
    assert "a jointly \\(C^1\\) map" in normalized
    assert "h:U\\times\\mathcal V\\longrightarrow\\mathbb R" in normalized
    assert "\\partial_J\\{h_{\\xi_0}(K_{\\xi_0}(J))\\}_{J=J_c}>0" in normalized
    assert "\\((\\xi,J)\\in U\\times I\\)" in normalized
    assert "signed local stimulus margin" in normalized
    assert "signed basin-safety margin" not in normalized
    assert "\\mathcal Q(a,\\kappa_3,J)" in normalized
    assert "D_{(a,\\kappa_3)}(F,A_p)" in normalized
