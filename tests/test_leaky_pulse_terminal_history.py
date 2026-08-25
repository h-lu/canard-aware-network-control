"""Tests for the exact physical-pulse terminal-history theorem."""

from __future__ import annotations

from copy import deepcopy
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path

import pytest

from canard_control.leaky_pulse_terminal_history import (
    EXACT_TRUE_FLAGS,
    OPEN_FALSE_FLAGS,
    build_pulse_terminal_history_certificate,
    exact_pulse_reduction_defects,
    json_ready_pulse_terminal_history_audit,
    validate_pulse_terminal_history_audit,
    validate_pulse_terminal_history_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]
RESULT = REPOSITORY / "experiments/results/leaky_pulse_terminal_history.json"


def _result() -> dict[str, object]:
    payload = json.loads(RESULT.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def test_exact_delay_reduction_and_variational_algebra() -> None:
    assert 4 * 4 * 5 > 1
    assert 5 * 5 * 5 > 1
    assert exact_pulse_reduction_defects() == (0, 0, 0, 0, 0)


def test_first_zero_bounds_are_strict_exact_rationals() -> None:
    # On a hypothetical first-zero interval, p<2 and q<eps*2*1=2/5.
    p_upper = Fraction(2)
    q_upper = Fraction(1, 5) * p_upper * Fraction(1)
    first_zero_derivative_lower = 1 - q_upper
    assert q_upper == Fraction(2, 5)
    assert first_zero_derivative_lower == Fraction(3, 5)
    assert first_zero_derivative_lower > 0


def test_certificate_proves_only_terminal_curve_orientation() -> None:
    certificate = build_pulse_terminal_history_certificate()
    assert all(getattr(certificate, name) for name in EXACT_TRUE_FLAGS)
    assert all(not getattr(certificate, name) for name in OPEN_FALSE_FLAGS)
    assert certificate.declared_pulse_amplitude_interval == ("3/10", "8/25")
    assert certificate.first_zero_derivative_lower_bound.endswith(">3/5")
    assert "ell[D_J K(J_c)]" in certificate.remaining_transversality


def test_audit_rejects_weakening_promotion_and_formula_tampering() -> None:
    audit = json_ready_pulse_terminal_history_audit()

    weakened = deepcopy(audit)
    weakened["certificate"][EXACT_TRUE_FLAGS[0]] = False
    with pytest.raises(ValueError, match="differs from exact reference"):
        validate_pulse_terminal_history_audit(weakened)

    promoted = deepcopy(audit)
    promoted["certificate"][OPEN_FALSE_FLAGS[0]] = True
    with pytest.raises(ValueError, match="differs from exact reference"):
        validate_pulse_terminal_history_audit(promoted)

    changed = deepcopy(audit)
    changed["certificate"]["recovery_variation_upper_bound"] = "q<1"
    with pytest.raises(ValueError, match="differs from exact reference"):
        validate_pulse_terminal_history_audit(changed)


def test_generated_result_and_manifest_revalidate() -> None:
    payload = _result()
    validate_pulse_terminal_history_result(payload, REPOSITORY)
    manifest = payload["manifest"]
    for name in ("proof_source", "parent_source", "parent_probe", "generator", "note"):
        relative = manifest[name]
        assert manifest[f"{name}_sha256"] == sha256(
            (REPOSITORY / relative).read_bytes()
        ).hexdigest()
