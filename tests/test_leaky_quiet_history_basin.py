"""Tests for the exact leaky quiet-history basin theorem."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict
from fractions import Fraction
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest
import sympy as sp

from canard_control.leaky_quiet_history_basin import (
    GENERATOR_RELATIVE_PATH,
    NOTE_RELATIVE_PATH,
    P11,
    P12,
    P22,
    RESULT_RELATIVE_PATH,
    SOURCE_MANIFEST,
    STATE_RADIUS,
    build_quiet_history_basin_certificate,
    validate_quiet_history_basin_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]
RESULT = REPOSITORY / RESULT_RELATIVE_PATH
GENERATOR = REPOSITORY / GENERATOR_RELATIVE_PATH
NOTE = REPOSITORY / NOTE_RELATIVE_PATH


def _payload() -> dict[str, object]:
    value = json.loads(RESULT.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def _fraction(record: dict[str, str]) -> Fraction:
    return Fraction(record["fraction"])


def test_exact_perturbation_remainder_matches_the_authoritative_field() -> None:
    alpha, x, y, x0, x1 = sp.symbols("alpha x y x0 x1", real=True)
    eps = sp.Rational(1, 5)
    k1 = sp.Rational(1, 250)
    k3 = sp.Rational(1, 200)
    a = sp.Rational(1, 4)
    v = alpha + x
    w = alpha - a + y
    delayed0 = alpha + x0
    delayed1 = alpha + x1
    fast = (
        v
        - v**3 / 3
        - w
        + eps * k1 * ((delayed0 + delayed1) / 2 - v)
        + eps
        * k3
        * (
            ((delayed0 - 1) ** 3 + (delayed1 - 1) ** 3) / 2
            - (v - 1) ** 3
        )
    )
    beta = alpha - 1
    delayed_gain = eps * (k1 + 3 * k3 * beta**2)
    current = 1 - alpha**2 - delayed_gain
    remainder = (
        -(alpha + 3 * eps * k3 * beta) * x**2
        - (sp.Rational(1, 3) + eps * k3) * x**3
        + eps
        * k3
        / 2
        * (3 * beta * x0**2 + x0**3 + 3 * beta * x1**2 + x1**3)
    )
    difference = sp.together(
        fast
        - (
            current * x
            - y
            + delayed_gain * (x0 + x1) / 2
            + remainder
        )
    )
    numerator = sp.Poly(difference.as_numer_denom()[0], alpha)
    assert numerator.rem(sp.Poly(alpha**3 - sp.Rational(3, 4), alpha)).is_zero


def test_rational_matrix_and_halanay_margins_are_strict() -> None:
    certificate = asdict(build_quiet_history_basin_certificate())
    assert P11 == Fraction(2823, 100)
    assert P12 == Fraction(-1351, 50)
    assert P22 == Fraction(13759, 100)
    assert _fraction(certificate["state_radius"]) == STATE_RADIUS
    assert _fraction(
        certificate["p_minus_lower_identity_determinant"]
    ) == Fraction(1128653, 10000)
    assert _fraction(
        certificate["upper_identity_minus_p_determinant"]
    ) == Fraction(120053, 10000)
    assert _fraction(
        certificate["q_minus_lower_identity_determinant_lower"]
    ) > Fraction(1, 100000)
    assert _fraction(certificate["halanay_strict_margin_lower"]) == Fraction(
        841037, 3150000000
    )
    assert _fraction(certificate["decay_rate_margin_lower"]) == Fraction(
        134750597, 825300000000
    )
    assert _fraction(
        certificate["initial_history_lyapunov_sublevel"]
    ) == Fraction(21, 1000000)


def test_claim_ledger_proves_only_the_local_quiet_basin() -> None:
    certificate = asdict(build_quiet_history_basin_certificate())
    proved = (
        "exact_perturbation_identity_proved",
        "rational_lyapunov_matrix_positive_definite_proved",
        "uniform_current_dissipation_proved",
        "nonlinear_history_gain_proved",
        "strict_halanay_margin_proved",
        "explicit_history_ellipsoid_forward_invariant_proved",
        "explicit_exponential_decay_rate_proved",
        "quiet_local_history_basin_validated",
    )
    open_claims = (
        "pulse_J_030_enters_quiet_ball_validated",
        "global_quiet_basin_validated",
        "history_space_separator_validated",
        "physical_pulse_onset_validated",
    )
    assert all(certificate[name] is True for name in proved)
    assert all(certificate[name] is False for name in open_claims)


def test_tracked_result_is_source_bound_and_revalidates() -> None:
    payload = _payload()
    validate_quiet_history_basin_result(payload, REPOSITORY)
    hashes = payload["manifest"]["source_sha256"]
    for relative in SOURCE_MANIFEST:
        assert hashes[relative] == sha256(
            (REPOSITORY / relative).read_bytes()
        ).hexdigest()


def test_validator_rejects_claim_and_source_tampering() -> None:
    payload = _payload()
    promoted = deepcopy(payload)
    promoted["certificate"][
        "pulse_J_030_enters_quiet_ball_validated"
    ] = True
    with pytest.raises(ValueError, match="differs from exact replay"):
        validate_quiet_history_basin_result(promoted, REPOSITORY)

    changed_hash = deepcopy(payload)
    changed_hash["manifest"]["source_sha256"][SOURCE_MANIFEST[0]] = "0" * 64
    with pytest.raises(ValueError, match="source hash changed"):
        validate_quiet_history_basin_result(changed_hash, REPOSITORY)

    changed_command = deepcopy(payload)
    changed_command["manifest"]["default_command"] = "python fake.py"
    with pytest.raises(ValueError, match="manifest default_command changed"):
        validate_quiet_history_basin_result(changed_command, REPOSITORY)

    changed_result_path = deepcopy(payload)
    changed_result_path["manifest"]["result"] = "results/fake.json"
    with pytest.raises(ValueError, match="manifest result changed"):
        validate_quiet_history_basin_result(changed_result_path, REPOSITORY)

    changed_arithmetic = deepcopy(payload)
    changed_arithmetic["manifest"]["arithmetic"] = "binary64"
    with pytest.raises(ValueError, match="manifest arithmetic changed"):
        validate_quiet_history_basin_result(changed_arithmetic, REPOSITORY)

    extra_manifest_field = deepcopy(payload)
    extra_manifest_field["manifest"]["untracked"] = True
    with pytest.raises(ValueError, match="missing or unknown fields"):
        validate_quiet_history_basin_result(extra_manifest_field, REPOSITORY)


def test_generator_replays_tracked_bytes(tmp_path: Path) -> None:
    replay = tmp_path / "quiet-basin.json"
    environment = {**os.environ, "PYTHONPATH": "src"}
    subprocess.run(
        [sys.executable, str(GENERATOR), "--output", str(replay)],
        cwd=REPOSITORY,
        env=environment,
        check=True,
    )
    assert replay.read_bytes() == RESULT.read_bytes()


def test_note_states_the_history_space_and_open_routing_gate() -> None:
    text = " ".join(NOTE.read_text(encoding="utf-8").split())
    assert "explicit quiet-history basin" in text
    assert "full RFDE history space" in text
    assert "forward-invariant" in text
    assert "J=0.30" in text
    assert "does not prove" in text
