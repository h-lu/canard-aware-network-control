"""Hostile regression tests for the robust FHN shutdown tube."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict
from decimal import Decimal, localcontext
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path

import pytest

from canard_control.fhn_robust_handoff_tube import (
    ASSUMPTIONS_ID,
    MODEL_ID,
    TRACKED_AUTONOMOUS_HANDOFF_SHA256,
    TRACKED_BALANCED_CONTROL_CHAIN_SHA256,
    load_robust_handoff_tube_result,
    robust_handoff_tube_from_payload,
    robust_tube_algebra_audit,
    validate_robust_handoff_tube_result_payload,
)


REPOSITORY = Path(__file__).resolve().parents[1]
HANDOFF = (
    REPOSITORY
    / "experiments/results/fhn_autonomous_handoff_excursion.json"
)
BALANCED = REPOSITORY / "experiments/results/fhn_balanced_control_chain.json"
RESULT = REPOSITORY / "experiments/results/fhn_robust_handoff_tube.json"
NOTE = REPOSITORY / "docs/paper-iv-robust-handoff-tube.md"
EXPECTED_RESULT_SHA256 = (
    "ff0320038842cbdbf6481d634f67844d418fba13e804654c2c335e9c3381140e"
)
EXPECTED_NOTE_SHA256 = (
    "f676d047fd7fbc25d12cf3a48999d74cc37a51fa3eea5a3c8c34eea582d1a39f"
)


def _read(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def _certificate(parent: dict | None = None, precision: int = 160):
    return robust_handoff_tube_from_payload(
        _read(HANDOFF) if parent is None else parent,
        autonomous_handoff_result_sha256=(
            TRACKED_AUTONOMOUS_HANDOFF_SHA256
        ),
        precision=precision,
    )


def test_both_parent_artifacts_are_digest_pinned() -> None:
    assert sha256(HANDOFF.read_bytes()).hexdigest() == (
        TRACKED_AUTONOMOUS_HANDOFF_SHA256
    )
    assert sha256(BALANCED.read_bytes()).hexdigest() == (
        TRACKED_BALANCED_CONTROL_CHAIN_SHA256
    )


def test_every_exact_rational_domination_margin_closes() -> None:
    audit = robust_tube_algebra_audit()
    values = asdict(audit)
    margins = {
        name: value
        for name, value in values.items()
        if name.endswith("_margin")
    }
    assert margins
    assert all(value > 0 for value in margins.values())
    assert audit.voltage_forcing_upper == Fraction(13, 250_000)
    assert audit.recovery_forcing_upper == Fraction(12_201, 1_000_000_000)
    assert audit.common_forcing_upper == Fraction(13, 250_000)
    assert audit.voltage_field_perturbation_upper == Fraction(1513, 250_000)


def test_nonsymmetric_row_stochastic_scaffold_is_max_norm_dissipative() -> None:
    # A deliberately nonsymmetric rational Markov matrix.  The proof uses
    # only nonnegativity and row mass one; this example guards against a
    # silent symmetry assumption in executable refactors.
    matrix = (
        (Fraction(0), Fraction(1), Fraction(0)),
        (Fraction(1, 3), Fraction(0), Fraction(2, 3)),
        (Fraction(3, 4), Fraction(1, 4), Fraction(0)),
    )
    error = (Fraction(-2), Fraction(1, 2), Fraction(2))
    norm = max(map(abs, error))
    for index, value in enumerate(error):
        if abs(value) != norm:
            continue
        sign = 1 if value > 0 else -1
        average = sum(
            matrix[index][column] * error[column]
            for column in range(len(error))
        )
        assert sign * (average - value) <= 0
    assert matrix != tuple(zip(*matrix))


def test_certificate_closes_the_full_tracking_bootstrap() -> None:
    certificate = _certificate()
    assert certificate.model_id == MODEL_ID
    assert certificate.assumptions_id == ASSUMPTIONS_ID
    with localcontext() as context:
        context.prec = 100
        radius = Decimal(certificate.common_tracking_tube_radius)
        positive = Decimal(certificate.positive_tracking_error_upper)
        negative = Decimal(certificate.negative_tracking_error_upper)
        assert positive < radius
        assert negative < radius
        assert Decimal(certificate.positive_tracking_slack_lower) <= (
            radius - positive
        )
        assert Decimal(certificate.negative_tracking_slack_lower) <= (
            radius - negative
        )
        assert positive < Decimal("0.000523")
        assert negative < Decimal("0.000189")


def test_remote_windows_remain_strictly_before_handoff() -> None:
    certificate = _certificate()
    with localcontext() as context:
        context.prec = 100
        minimum_delay = Decimal(certificate.minimum_delay_lower)
        assert Decimal(certificate.positive_nominal_horizon_upper) < minimum_delay
        assert Decimal(certificate.negative_nominal_horizon_upper) < minimum_delay
    assert certificate.remote_history_window_definition == (
        "I_{j,sigma}=[-tau_j,H_sigma-tau_j], j=0,1"
    )


def test_componentwise_velocity_signs_survive_the_field_error() -> None:
    certificate = _certificate()
    handoff = _read(HANDOFF)["certificate"]
    with localcontext() as context:
        context.prec = 100
        field = Decimal(certificate.voltage_field_perturbation_upper)
        assert Decimal(certificate.positive_component_velocity_lower) <= (
            Decimal(handoff["positive_autonomous_velocity_lower"]) - field
        )
        assert Decimal(
            certificate.negative_component_velocity_magnitude_lower
        ) <= (
            Decimal(handoff["negative_autonomous_magnitude_velocity_lower"])
            - field
        )
        assert Decimal(certificate.positive_component_velocity_lower) == (
            Decimal("0.131")
        )
        assert Decimal(
            certificate.negative_component_velocity_magnitude_lower
        ) == Decimal("0.068")


def test_terminal_blocks_are_outward_enclosures() -> None:
    certificate = _certificate()
    handoff = _read(HANDOFF)["certificate"]
    radius = Decimal(certificate.common_tracking_tube_radius)
    positive_v = tuple(map(Decimal, certificate.positive_capture_voltage_interval))
    negative_v = tuple(map(Decimal, certificate.negative_capture_voltage_interval))
    positive_w = tuple(map(Decimal, certificate.positive_capture_recovery_interval))
    negative_w = tuple(map(Decimal, certificate.negative_capture_recovery_interval))
    assert positive_v[0] <= Decimal("1.5") - radius
    assert positive_v[1] >= Decimal("1.5") + radius
    assert negative_v[0] <= Decimal("-1.2") - radius
    assert negative_v[1] >= Decimal("-1.2") + radius
    assert positive_w[0] <= -radius
    assert positive_w[1] >= (
        Decimal(handoff["positive_autonomous_recovery_at_landing_upper"])
        + radius
    )
    assert negative_w[0] <= -(
        Decimal(
            handoff[
                "negative_autonomous_recovery_magnitude_at_landing_upper"
            ]
        )
        + radius
    )
    assert negative_w[1] >= radius


def test_certificate_scope_is_open_asynchronous_and_finite_horizon_only() -> None:
    certificate = _certificate()
    assert certificate.full_rfde_open_handoff_cylinder_validated
    assert certificate.asynchronous_finite_horizon_tracking_tube_validated
    assert certificate.row_stochastic_scaffold_max_norm_dissipativity_validated
    assert certificate.bounded_shutdown_residual_inputs_validated
    assert not certificate.exact_synchrony_required
    assert not certificate.exact_zero_input_after_handoff_required
    assert not certificate.robust_history_preparation_validated
    assert not certificate.delay_perturbations_validated
    assert not certificate.permanent_no_return_validated
    assert not certificate.biological_action_potential_validated
    assert not certificate.quiet_or_pulse_basin_validated
    assert not certificate.actuator_bandwidth_or_slew_rate_validated
    assert not certificate.hardware_validated


@pytest.mark.parametrize("precision", (True, 63, 64.5))
def test_invalid_precision_is_rejected(precision) -> None:
    with pytest.raises(ValueError, match="precision"):
        _certificate(precision=precision)


def test_wrong_handoff_digest_is_rejected() -> None:
    with pytest.raises(ValueError, match="tracked source"):
        robust_handoff_tube_from_payload(
            _read(HANDOFF),
            autonomous_handoff_result_sha256="0" * 64,
        )


def test_tampered_parent_proof_is_rejected() -> None:
    parent = deepcopy(_read(HANDOFF))
    parent["certificate"][
        "positive_finite_autonomous_excursion_validated"
    ] = False
    with pytest.raises(ValueError, match="must be true"):
        _certificate(parent=parent)


def test_tampered_parent_numerical_endpoint_is_rejected() -> None:
    parent = deepcopy(_read(HANDOFF))
    parent["certificate"]["positive_autonomous_velocity_lower"] = "0.2"
    with pytest.raises(ValueError, match="endpoint"):
        _certificate(parent=parent)


@pytest.mark.parametrize(
    "field",
    (
        "asynchronous_finite_horizon_tracking_tube_validated",
        "full_rfde_open_handoff_cylinder_validated",
        "bounded_shutdown_residual_inputs_validated",
        "positive_componentwise_no_reversal_validated",
    ),
)
def test_missing_proof_flags_are_rejected(field: str) -> None:
    payload = deepcopy(_read(RESULT))
    payload["certificate"][field] = False
    with pytest.raises(ValueError, match="must be true"):
        validate_robust_handoff_tube_result_payload(payload)


@pytest.mark.parametrize(
    "field",
    (
        "robust_history_preparation_validated",
        "delay_perturbations_validated",
        "permanent_no_return_validated",
        "biological_action_potential_validated",
        "quiet_or_pulse_basin_validated",
        "actuator_bandwidth_or_slew_rate_validated",
        "hardware_validated",
    ),
)
def test_unsupported_promotions_are_rejected(field: str) -> None:
    payload = deepcopy(_read(RESULT))
    payload["certificate"][field] = True
    with pytest.raises(ValueError, match="must be false"):
        validate_robust_handoff_tube_result_payload(payload)


@pytest.mark.parametrize(
    ("field", "value", "message"),
    (
        ("positive_tracking_error_upper", "0", "tracking composition"),
        ("positive_tracking_slack_lower", "0.001", "tracking composition"),
        ("voltage_field_perturbation_upper", "0", "invalid"),
        ("positive_component_velocity_lower", "0.14", "invalid"),
        (
            "positive_capture_recovery_interval",
            ["0", "0.18"],
            "not outward safe",
        ),
    ),
)
def test_inward_tampering_of_directed_endpoints_is_rejected(
    field: str, value, message: str
) -> None:
    payload = deepcopy(_read(RESULT))
    payload["certificate"][field] = value
    with pytest.raises(ValueError, match=message):
        validate_robust_handoff_tube_result_payload(payload)


def test_stored_artifact_and_note_are_pinned() -> None:
    assert sha256(RESULT.read_bytes()).hexdigest() == EXPECTED_RESULT_SHA256
    assert sha256(NOTE.read_bytes()).hexdigest() == EXPECTED_NOTE_SHA256
    payload = load_robust_handoff_tube_result(
        RESULT, expected_sha256=EXPECTED_RESULT_SHA256
    )
    assert payload["certificate"]["model_id"] == MODEL_ID


def test_artifact_manifests_are_live() -> None:
    payload = _read(RESULT)
    for relative, digest in payload["provenance"][
        "proof_source_manifest"
    ].items():
        assert sha256((REPOSITORY / relative).read_bytes()).hexdigest() == digest
    for relative, digest in payload["provenance"][
        "parent_result_manifest"
    ].items():
        assert sha256((REPOSITORY / relative).read_bytes()).hexdigest() == digest


def test_note_keeps_the_open_cylinder_and_claim_boundary_explicit() -> None:
    text = NOTE.read_text(encoding="utf-8")
    flat = " ".join(text.split())
    required = (
        "open cylinder in the full RFDE history space",
        r"I_{j,\sigma}=[-\tau_j,H_\sigma-\tau_j]",
        "arbitrary-sign",
        "first entry",
        "does not prove that feedback reaches this entrance cylinder",
        "does **not** prove",
        "biological action potential",
    )
    assert all(item in flat for item in required)
