"""Regression and hostile tests for the leaky majorant proof certificate."""

from __future__ import annotations

from copy import deepcopy
from decimal import Decimal
from hashlib import sha256
import json
from pathlib import Path

import pytest

from canard_control.leaky_periodic_majorant_audit import (
    AUDIT_RESULT_RELATIVE_PATH,
    AUDIT_SOURCE_MANIFEST,
    validate_leaky_periodic_majorant_audit_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]
RESULT = REPOSITORY / AUDIT_RESULT_RELATIVE_PATH
EXPECTED_RESULT_SHA256 = (
    "bfaafe9d12876cc3fc879e6423543bd34fd5526630ce310a8590948d35ea1b9e"
)


def _payload() -> dict:
    return json.loads(RESULT.read_text(encoding="utf-8"))


def test_inner_majorant_certificate_is_source_bound_and_strict() -> None:
    raw = RESULT.read_bytes()
    assert sha256(raw).hexdigest() == EXPECTED_RESULT_SHA256
    payload = json.loads(raw)
    validate_leaky_periodic_majorant_audit_result(payload, REPOSITORY)
    manifest = payload["manifest"]
    for relative in AUDIT_SOURCE_MANIFEST:
        assert manifest["source_sha256"][relative] == sha256(
            (REPOSITORY / relative).read_bytes()
        ).hexdigest()


def test_certificate_promotes_only_formula_orbit_and_bordered_inverse() -> None:
    certificate = _payload()["certificate"]
    ledger = certificate["formula_audit"]["proof_ledger"]
    assert all(ledger.values())
    claims = certificate["claims"]
    assert claims["formula_adaptation_independently_audited"]
    assert claims["inner_periodic_rfde_orbit_validated"]
    assert claims["phase_bordered_rfde_inverse_validated"]
    for name, value in claims.items():
        if name not in {
            "formula_adaptation_independently_audited",
            "inner_periodic_rfde_orbit_validated",
            "phase_bordered_rfde_inverse_validated",
        }:
            assert value is False

    directed = certificate["directed_radii"]
    assert Decimal(directed["contraction_upper"]) < 1
    assert Decimal(directed["radii_margin_lower"]) > Decimal("9e-6")
    specialization = certificate["formula_audit"]["directed_specialization"]
    assert specialization["finite_block_dominates_tail_block"]
    assert Decimal(specialization["full_preconditioner_l1_upper"]) == Decimal(
        specialization["finite_preconditioner_l1_upper"]
    )


@pytest.mark.parametrize(
    ("path", "replacement", "message"),
    [
        (
            (
                "certificate",
                "formula_audit",
                "proof_ledger",
                "nonlinear_z1_increment_proved",
            ),
            False,
            "proof ledger",
        ),
        (
            ("certificate", "claims", "unstable_multiplier_count_validated"),
            True,
            "claim ledger",
        ),
        (
            (
                "certificate",
                "formula_audit",
                "directed_specialization",
                "full_preconditioner_l1_upper",
            ),
            "1e-12",
            "preconditioner norm",
        ),
        (
            ("certificate", "directed_radii", "radii_margin_lower"),
            "-1e-6",
            "directed bounds",
        ),
    ],
)
def test_hostile_tampering_is_rejected(
    path: tuple[str, ...], replacement: object, message: str
) -> None:
    tampered = deepcopy(_payload())
    target = tampered
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = replacement
    # Recompute the internal digest so the test reaches the semantic gate.
    from canard_control.leaky_periodic_majorant_audit import canonical_sha256

    tampered["manifest"]["certificate_sha256"] = canonical_sha256(
        tampered["certificate"]
    )
    with pytest.raises(ValueError, match=message):
        validate_leaky_periodic_majorant_audit_result(tampered, REPOSITORY)


def test_source_hash_tampering_is_rejected() -> None:
    tampered = deepcopy(_payload())
    relative = AUDIT_SOURCE_MANIFEST[0]
    tampered["manifest"]["source_sha256"][relative] = "0" * 64
    with pytest.raises(ValueError, match="source hash changed"):
        validate_leaky_periodic_majorant_audit_result(tampered, REPOSITORY)
