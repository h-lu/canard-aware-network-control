"""Hostile regression tests for the autonomous FHN handoff corridors."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict
from decimal import Decimal, localcontext
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path

import pytest

from canard_control.fhn_autonomous_handoff_excursion import (
    ASSUMPTIONS_ID,
    MODEL_ID,
    TRACKED_BALANCED_CONTROL_CHAIN_SHA256,
    autonomous_handoff_from_payload,
    handoff_algebra_audit,
    load_autonomous_handoff_result,
    negative_autonomous_barrier_audit,
    negative_unit_handoff_obstruction_audit,
    positive_autonomous_barrier_audit,
    validate_autonomous_handoff_result_payload,
)


REPOSITORY = Path(__file__).resolve().parents[1]
PARENT = REPOSITORY / "experiments/results/fhn_balanced_control_chain.json"
RESULT = (
    REPOSITORY
    / "experiments/results/fhn_autonomous_handoff_excursion.json"
)
NOTE = REPOSITORY / "docs/paper-iv-autonomous-handoff-excursion.md"
EXPECTED_RESULT_SHA256 = (
    "38f612771fd5f7e50ffd4f77103ea680b447fd11a7af25cc5ccea95b9bf606f2"
)
EXPECTED_NOTE_SHA256 = (
    "74621b92919f97fea90cca5fd21c43b6794b8869e32e23a6a4cad468f1ecf192"
)


def _read(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def _certificate(parent: dict | None = None, precision: int = 160):
    return autonomous_handoff_from_payload(
        _read(PARENT) if parent is None else parent,
        balanced_control_chain_result_sha256=(
            TRACKED_BALANCED_CONTROL_CHAIN_SHA256
        ),
        precision=precision,
    )


def test_parent_digest_is_the_pinned_balanced_control_chain() -> None:
    assert sha256(PARENT.read_bytes()).hexdigest() == (
        TRACKED_BALANCED_CONTROL_CHAIN_SHA256
    )


def test_frozen_delay_handoff_algebra_is_exact() -> None:
    audit = handoff_algebra_audit()
    assert audit.positive_voltage_residual == 0
    assert audit.positive_recovery_residual == 0
    assert audit.negative_voltage_residual == 0
    assert audit.negative_recovery_residual == 0
    assert audit.positive_vector_derivative_residual == 0
    assert audit.negative_vector_derivative_residual == 0
    assert str(audit.positive_vector_derivative_at_one) == "-kappa_1/5"
    assert str(audit.negative_vector_derivative_at_one) == (
        "-kappa_1/5 - 12*kappa_3/5"
    )


def test_positive_phase_barrier_closes_every_exact_segment() -> None:
    audit = positive_autonomous_barrier_audit()
    assert audit.branch == "positive"
    assert audit.start == 1
    assert audit.target == Fraction(3, 2)
    assert audit.step == Fraction(1, 40)
    assert len(audit.segments) == 20
    assert audit.segments[0].barrier_left == 0
    assert audit.segments[-1].barrier_right == (
        audit.terminal_barrier_upper
    )
    assert all(segment.slope > 0 for segment in audit.segments)
    assert all(
        segment.vector_lower_at_right > 0 for segment in audit.segments
    )
    assert all(segment.inward_margin > 0 for segment in audit.segments)
    assert audit.minimum_vector_lower == Fraction(549148907883, 4_000_000_000_000)
    assert audit.terminal_barrier_upper == Fraction(
        148170218423, 800_000_000_000
    )
    assert audit.crossing_time_upper == sum(
        (segment.crossing_time_upper for segment in audit.segments),
        Fraction(0),
    )
    for left, right in zip(audit.segments, audit.segments[1:]):
        assert left.right == right.left
        assert left.barrier_right == right.barrier_left
        assert right.inward_margin > 0


def test_negative_phase_barrier_closes_every_exact_segment() -> None:
    audit = negative_autonomous_barrier_audit()
    assert audit.branch == "negative"
    assert audit.start == Fraction(28, 25)
    assert audit.target == Fraction(6, 5)
    assert audit.step == Fraction(1, 200)
    assert len(audit.segments) == 16
    assert all(
        segment.vector_lower_at_right > 0 for segment in audit.segments
    )
    assert all(segment.inward_margin > 0 for segment in audit.segments)
    assert audit.minimum_vector_lower == Fraction(
        93553253235201, 1_250_000_000_000_000
    )
    assert audit.terminal_barrier_upper == Fraction(
        3150147948173, 20_000_000_000_000
    )
    for left, right in zip(audit.segments, audit.segments[1:]):
        assert left.right == right.left
        assert left.barrier_right == right.barrier_left
        assert right.inward_margin > 0


def test_barrier_velocity_bounds_have_the_declared_orientations() -> None:
    positive = positive_autonomous_barrier_audit()
    negative = negative_autonomous_barrier_audit()
    assert positive.minimum_vector_lower > Fraction(1372872, 10_000_000)
    assert negative.minimum_vector_lower > Fraction(748426, 10_000_000)
    assert positive.minimum_inward_margin > Fraction(1, 10**10)
    assert negative.minimum_inward_margin > Fraction(1, 2 * 10**9)


def test_negative_unit_handoff_forces_a_turn_before_1_17() -> None:
    audit = negative_unit_handoff_obstruction_audit()
    assert len(audit.segments) == 17
    assert audit.endpoint == Fraction(117, 100)
    assert audit.initial_vector_lower == Fraction(
        24924999999877, 60_000_000_000_000
    )
    assert all(segment.inward_margin > 0 for segment in audit.segments)
    assert audit.minimum_inward_margin > 0
    assert audit.terminal_barrier_lower > audit.terminal_vector_upper
    assert audit.terminal_crossing_margin == Fraction(
        92721922530336687, 2_500_000_000_000_000_000
    )
    assert audit.turn_time_upper < Fraction(13, 10)
    for left, right in zip(audit.segments, audit.segments[1:]):
        assert left.right == right.left
        assert left.barrier_right == right.barrier_left
        assert right.inward_margin > 0


def test_composed_certificate_has_exactly_the_supported_scope() -> None:
    certificate = _certificate()
    assert certificate.model_id == MODEL_ID
    assert certificate.assumptions_id == ASSUMPTIONS_ID
    assert certificate.exact_positive_phase_barrier_validated
    assert certificate.exact_negative_phase_barrier_validated
    assert certificate.piecewise_barrier_corner_forward_invariance_validated
    assert certificate.method_of_steps_frozen_delay_window_validated
    assert certificate.all_additive_inputs_zero_after_handoff_validated
    assert certificate.positive_finite_autonomous_excursion_validated
    assert certificate.negative_finite_autonomous_excursion_validated
    assert certificate.positive_finite_horizon_no_reversal_validated
    assert certificate.negative_finite_horizon_no_reversal_validated
    assert certificate.negative_unit_handoff_turn_before_minus_1_17_validated
    assert Decimal(
        certificate.negative_unit_initial_magnitude_velocity_lower
    ) > Decimal("0.4154")
    assert not certificate.negative_unit_handoff_monotone_no_return_validated
    assert not certificate.asynchronous_autonomous_excursion_validated
    assert not certificate.autonomous_onset_validated
    assert not certificate.permanent_no_return_validated
    assert not certificate.biological_action_potential_validated
    assert not certificate.quiet_or_pulse_basin_validated
    assert not certificate.landing_on_periodic_branch_validated
    assert not certificate.full_network_periodic_attraction_validated


def test_total_times_strictly_close_the_method_of_steps_loop() -> None:
    certificate = _certificate()
    with localcontext() as context:
        context.prec = 100
        minimum_delay = Decimal(certificate.minimum_delay_lower)
        positive_total = Decimal(
            certificate.positive_decision_release_to_excursion_time_upper
        )
        negative_total = Decimal(
            certificate.negative_decision_release_to_excursion_time_upper
        )
        unit_detector = Decimal(
            certificate.negative_unit_controlled_detector_deadline_upper
        )
        unit_turn = Decimal(certificate.negative_unit_handoff_turn_time_upper)
        unit_total = Decimal(
            certificate.negative_unit_decision_release_to_turn_time_upper
        )
        assert positive_total < minimum_delay
        assert negative_total < minimum_delay
        assert unit_total >= unit_detector + unit_turn
        assert unit_total < minimum_delay
        assert Decimal(certificate.positive_frozen_delay_slack_lower) <= (
            minimum_delay - positive_total
        )
        assert Decimal(certificate.negative_frozen_delay_slack_lower) <= (
            minimum_delay - negative_total
        )
        assert Decimal(
            certificate.negative_unit_handoff_frozen_delay_slack_lower
        ) <= (minimum_delay - unit_total)
        assert positive_total < Decimal("2.733")
        assert negative_total < Decimal("5.450")
        assert minimum_delay > Decimal("8.944")


def test_public_controlled_deadlines_dominate_the_formulas() -> None:
    certificate = _certificate()
    with localcontext() as context:
        context.prec = 100
        kappa_1 = Decimal("0.200000000002")
        kappa_3 = Decimal("0.250000000002")
        epsilon = Decimal(1) / Decimal(5)
        positive_growth = Decimal(2) / Decimal(3) - epsilon * (
            kappa_1 + Decimal(3) * kappa_3
        )
        h = Decimal("1.12")
        negative_growth = (
            Decimal(1)
            - h**2 / Decimal(3)
            - epsilon
            * (kappa_1 + kappa_3 * (h**2 + Decimal(3) * h + Decimal(3)))
        )
        assert Decimal(certificate.positive_controlled_handoff_growth_lower) <= (
            positive_growth
        )
        assert Decimal(certificate.negative_controlled_handoff_growth_lower) <= (
            negative_growth
        )
        positive_deadline = Decimal(2).ln() / positive_growth
        negative_deadline = Decimal("2.24").ln() / negative_growth
        assert Decimal(certificate.positive_controlled_handoff_deadline_upper) >= (
            positive_deadline
        )
        assert Decimal(certificate.negative_controlled_handoff_deadline_upper) >= (
            negative_deadline
        )


def test_full_deadlines_include_parent_preparation_time() -> None:
    certificate = _certificate()
    parent = _read(PARENT)["certificate"]
    with localcontext() as context:
        context.prec = 100
        preparation = Decimal(parent["complete_history_preparation_time_upper"])
        assert Decimal(certificate.positive_control_start_to_excursion_time_upper) >= (
            preparation
            + Decimal(certificate.positive_decision_release_to_excursion_time_upper)
        )
        assert Decimal(certificate.negative_control_start_to_excursion_time_upper) >= (
            preparation
            + Decimal(certificate.negative_decision_release_to_excursion_time_upper)
        )
        assert Decimal(
            certificate.positive_control_start_to_excursion_time_upper
        ) < Decimal("17.23")
        assert Decimal(
            certificate.negative_control_start_to_excursion_time_upper
        ) < Decimal("19.95")


@pytest.mark.parametrize("precision", (True, 63, 64.5))
def test_invalid_precision_is_rejected(precision) -> None:
    with pytest.raises(ValueError, match="precision"):
        _certificate(precision=precision)


def test_wrong_parent_digest_is_rejected() -> None:
    with pytest.raises(ValueError, match="tracked source"):
        autonomous_handoff_from_payload(
            _read(PARENT),
            balanced_control_chain_result_sha256="0" * 64,
        )


def test_tampered_parent_proof_flag_is_rejected() -> None:
    parent = deepcopy(_read(PARENT))
    parent["certificate"][
        "bounded_nodewise_recovery_cancellation_on_decision_tube_validated"
    ] = False
    with pytest.raises(ValueError, match="must be true"):
        _certificate(parent=parent)


def test_parent_gain_box_outside_enclosing_box_is_rejected() -> None:
    parent = deepcopy(_read(PARENT))
    parent["certificate"]["kappa_1_interval"][1] = "0.21"
    with pytest.raises(ValueError, match="gain box"):
        _certificate(parent=parent)


def test_stored_artifact_and_note_are_pinned() -> None:
    assert sha256(RESULT.read_bytes()).hexdigest() == EXPECTED_RESULT_SHA256
    assert sha256(NOTE.read_bytes()).hexdigest() == EXPECTED_NOTE_SHA256
    payload = load_autonomous_handoff_result(
        RESULT, expected_sha256=EXPECTED_RESULT_SHA256
    )
    assert payload["certificate"]["model_id"] == MODEL_ID


@pytest.mark.parametrize(
    "field",
    (
        "positive_finite_autonomous_excursion_validated",
        "negative_finite_autonomous_excursion_validated",
        "method_of_steps_frozen_delay_window_validated",
        "all_additive_inputs_zero_after_handoff_validated",
        "piecewise_barrier_corner_forward_invariance_validated",
    ),
)
def test_missing_proof_flags_are_rejected(field: str) -> None:
    payload = deepcopy(_read(RESULT))
    payload["certificate"][field] = False
    with pytest.raises(ValueError, match="must be true"):
        validate_autonomous_handoff_result_payload(payload)


@pytest.mark.parametrize(
    "field",
    (
        "asynchronous_autonomous_excursion_validated",
        "autonomous_onset_validated",
        "permanent_no_return_validated",
        "biological_action_potential_validated",
        "quiet_or_pulse_basin_validated",
        "landing_on_periodic_branch_validated",
    ),
)
def test_unsupported_promotions_are_rejected(field: str) -> None:
    payload = deepcopy(_read(RESULT))
    payload["certificate"][field] = True
    with pytest.raises(ValueError, match="must be false"):
        validate_autonomous_handoff_result_payload(payload)


def test_nonpositive_public_margin_is_rejected() -> None:
    payload = deepcopy(_read(RESULT))
    payload["certificate"]["negative_frozen_delay_slack_lower"] = "0"
    with pytest.raises(ValueError, match="not positive"):
        validate_autonomous_handoff_result_payload(payload)


@pytest.mark.parametrize(
    "field",
    (
        "positive_frozen_delay_slack_lower",
        "negative_frozen_delay_slack_lower",
    ),
)
def test_inflated_public_method_of_steps_slack_is_rejected(field: str) -> None:
    payload = deepcopy(_read(RESULT))
    payload["certificate"][field] = payload["certificate"]["minimum_delay_lower"]
    with pytest.raises(ValueError, match="deadline composition"):
        validate_autonomous_handoff_result_payload(payload)


@pytest.mark.parametrize(
    ("field", "value", "message"),
    (
        (
            "positive_decision_release_to_excursion_time_upper",
            "1",
            "total deadline",
        ),
        (
            "negative_unit_decision_release_to_turn_time_upper",
            "1",
            "turn deadline",
        ),
        (
            "positive_autonomous_velocity_lower",
            "1",
            "wrong orientation",
        ),
        (
            "negative_autonomous_recovery_magnitude_at_landing_upper",
            "0",
            "wrong orientation",
        ),
    ),
)
def test_shortened_deadlines_or_enlarged_margins_are_rejected(
    field: str, value: str, message: str
) -> None:
    payload = deepcopy(_read(RESULT))
    payload["certificate"][field] = value
    with pytest.raises(ValueError, match=message):
        validate_autonomous_handoff_result_payload(payload)


def test_note_keeps_the_biological_and_synchrony_boundaries_explicit() -> None:
    text = NOTE.read_text(encoding="utf-8")
    required = (
        "exactly prepared synchronous leaf",
        "u^v=u^w=0",
        "identify the excursion with a biological action potential",
        "does **not** prove",
        r"before the trajectory reaches \(-1.17\)",
        "does **not** prove that the delayed trajectory can",
    )
    assert all(item in text for item in required)
