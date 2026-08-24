"""Hostile tests for the quadratic physical-onset/capture stop-go audit."""

from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys

import pytest
import sympy as sp

from canard_control.quadratic_physical_onset_stop_go import (
    AUTONOMOUS_HANDOFF_RESULT_SHA256,
    BALANCED_CONTROL_CHAIN_RESULT_SHA256,
    BOUNDED_PREPARATION_RESULT_SHA256,
    FIXED_EPSILON_BVP_RESULT_SHA256,
    PERIODIC_ATTRACTION_RESULT_SHA256,
    PERIODIC_BOX_RESULT_SHA256,
    PHYSICAL_OUTER_BRIDGE_DOC_SHA256,
    QUADRATIC_CARRIER_RESULT_SHA256,
    QUADRATIC_DOBRUSHIN_RESULT_SHA256,
    ROBUST_HANDOFF_RESULT_SHA256,
    UNFORCED_CAPTURE_DOC_SHA256,
    reference_composition_mismatch_audit,
    reference_controlled_quadratic_transfer_audit,
    reference_stop_go_certificate,
    stop_go_algebra_is_exact,
    validate_stop_go_payload,
)


REPOSITORY = Path(__file__).resolve().parents[1]
RESULT = REPOSITORY / "experiments/results/quadratic_physical_onset_stop_go.json"
NOTE = REPOSITORY / "docs/quadratic-physical-onset-capture-stop-go.md"
EXPECTED_RESULT_SHA256 = (
    "4bc8ccf41fb0f2d2fd7e3152da59afa24810a5b0d8615a3847d1491f63ff55da"
)
EXPECTED_NOTE_SHA256 = (
    "8bf5e8f5e8f0906ea123c8bf9d7bff09c1f23f2b362bf3c10ad9faeec91534cb"
)


def _payload() -> dict:
    return json.loads(RESULT.read_text(encoding="utf-8"))


def test_delta_a_slice_mismatch_is_exact() -> None:
    audit = reference_composition_mismatch_audit()
    assert audit.reference_delta == 1 / sp.sqrt(5)
    assert audit.reference_epsilon == sp.Rational(1, 5)
    assert audit.singular_root_unfolding_limit == 1
    assert audit.controlled_periodic_unfolding == sp.Rational(3, 5)
    assert audit.limiting_unfolding_gap == sp.Rational(2, 5)
    assert audit.root_family_delay_scaling == (
        4 / sp.Symbol("delta", positive=True),
        5 / sp.Symbol("delta", positive=True),
    )
    assert audit.root_quadratic_delay_scaling == "Theta_*/delta"
    assert "only at delta=1/sqrt(5)" in audit.reference_period_lock_relation


def test_preparation_plant_and_basin_are_not_identified() -> None:
    audit = reference_composition_mismatch_audit()
    assert "canonical flow-hull" in audit.canonical_root_preparation
    assert audit.controlled_reset_preparations == (
        "Phi_{+1/2}",
        "Phi_{-1/2}",
    )
    assert audit.parent_handoff_quadratic_channel == "absent"
    assert "eta=0" in audit.periodic_basin_slice
    assert "not the quadratic dual scaffold" in audit.physical_outer_bridge_plant


def test_two_channel_eta_bounds_and_common_minimum_are_exact() -> None:
    audit = reference_controlled_quadratic_transfer_audit()
    assert audit.positive_quadratic_difference_upper == sp.Rational(
        6265009, 25000000
    )
    assert audit.negative_quadratic_difference_upper == sp.Rational(
        64861, 25000
    )
    assert audit.positive_residual_per_abs_eta_upper == sp.Rational(
        1253008065009, 25000000000000
    )
    assert audit.negative_residual_per_abs_eta_upper == sp.Rational(
        12972264861, 25000000000
    )
    assert audit.positive_abs_eta_strict_upper == sp.Rational(
        250000000, 1253008065009
    )
    assert audit.negative_abs_eta_strict_upper == sp.Rational(
        250000, 12972264861
    )
    assert audit.common_abs_eta_strict_upper == audit.negative_abs_eta_strict_upper
    assert audit.common_abs_eta_strict_upper < audit.positive_abs_eta_strict_upper


def test_cancellation_and_preparation_authority_are_exact() -> None:
    audit = reference_controlled_quadratic_transfer_audit()
    assert stop_go_algebra_is_exact()
    assert audit.constant_history_carrier_action == 0
    assert audit.carrier_plus_exact_cancellation_action == 0
    assert audit.preparation_shifted_square_range == (0, 9)
    assert audit.preparation_carrier_per_abs_eta_upper == sp.Rational(9, 5)
    assert audit.remaining_voltage_authority_margin_lower > 0


def test_certificate_proves_only_controlled_terminal_transfer() -> None:
    certificate = reference_stop_go_certificate()
    assert not certificate.four_gate_existing_module_composition_validated
    assert certificate.quadratic_carrier_zero_on_constant_histories_validated
    assert certificate.exact_control_cancellation_through_preparation_and_decision_validated
    assert certificate.extended_t_star_history_hold_required
    assert certificate.controlled_reference_slice_small_eta_terminal_transfer_validated
    assert certificate.arbitrary_finite_balanced_topology_controlled_transfer_validated
    assert certificate.positive_eta_bound_validated
    assert certificate.negative_eta_bound_validated
    assert certificate.common_eta_bound_is_negative_minimum_validated
    assert certificate.all_additive_inputs_zero_after_quadratic_handoff_validated


def test_certificate_refuses_every_onset_capture_and_basin_promotion() -> None:
    certificate = reference_stop_go_certificate()
    refused = (
        certificate.controlled_transfer_is_input_independent_onset_validated,
        certificate.root_family_quadratic_channel_period_locked_validated,
        certificate.fixed_epsilon_selected_root_validated,
        certificate.fixed_epsilon_nonzero_root_response_validated,
        certificate.physical_outer_history_equals_canonical_root_history_validated,
        certificate.selected_root_event_factorization_validated,
        certificate.pulse_quiet_capture_validated,
        certificate.permanent_detector_face_no_return_validated,
        certificate.periodic_basin_eta_neighborhood_validated,
        certificate.terminal_block_periodic_basin_containment_validated,
        certificate.quiet_basin_validated,
        certificate.biological_pulse_onset_validated,
    )
    assert refused == (False,) * len(refused)


def test_parent_hashes_are_pinned() -> None:
    pairs = (
        ("experiments/results/quadratic_period_locked_root_carrier.json", QUADRATIC_CARRIER_RESULT_SHA256),
        ("experiments/results/quadratic_period_lock_dobrushin_lift.json", QUADRATIC_DOBRUSHIN_RESULT_SHA256),
        ("experiments/results/fixed_epsilon_quadratic_root_bvp.json", FIXED_EPSILON_BVP_RESULT_SHA256),
        ("experiments/results/fhn_bounded_additive_preparation.json", BOUNDED_PREPARATION_RESULT_SHA256),
        ("experiments/results/fhn_balanced_control_chain.json", BALANCED_CONTROL_CHAIN_RESULT_SHA256),
        ("experiments/results/fhn_robust_handoff_tube.json", ROBUST_HANDOFF_RESULT_SHA256),
        ("experiments/results/fhn_autonomous_handoff_excursion.json", AUTONOMOUS_HANDOFF_RESULT_SHA256),
        ("experiments/results/fhn_periodic_parameter_box.json", PERIODIC_BOX_RESULT_SHA256),
        ("experiments/results/fhn_dobrushin_periodic_attraction.json", PERIODIC_ATTRACTION_RESULT_SHA256),
        ("docs/paper-iii-physical-outer-pulse-bridge.md", PHYSICAL_OUTER_BRIDGE_DOC_SHA256),
        ("docs/paper-iii-unforced-capture-no-return.md", UNFORCED_CAPTURE_DOC_SHA256),
    )
    for relative_path, expected in pairs:
        assert sha256((REPOSITORY / relative_path).read_bytes()).hexdigest() == expected


def test_artifact_validates_and_false_claim_promotion_is_rejected() -> None:
    payload = _payload()
    assert validate_stop_go_payload(payload) == reference_stop_go_certificate()
    promoted = deepcopy(payload)
    promoted["scope"]["biological_pulse_onset"] = True
    with pytest.raises(ValueError, match="promoted"):
        validate_stop_go_payload(promoted)


def test_exact_audit_and_parent_check_tampering_are_rejected() -> None:
    payload = _payload()
    changed = deepcopy(payload)
    changed["exact_audits"]["controlled_quadratic_transfer"][
        "common_abs_eta_strict_upper"
    ] = "1"
    with pytest.raises(ValueError, match="exact_audits"):
        validate_stop_go_payload(changed)
    changed = deepcopy(payload)
    changed["provenance"]["parent_claim_checks"][
        "fixed_epsilon_root_refused"
    ] = False
    with pytest.raises(ValueError, match="parent claim"):
        validate_stop_go_payload(changed)


def test_source_provenance_tampering_is_rejected() -> None:
    payload = _payload()
    changed = deepcopy(payload)
    changed["provenance"]["proof_source_sha256"] = "0" * 64
    with pytest.raises(ValueError, match="source-bound"):
        validate_stop_go_payload(changed)


def test_default_generator_replay_is_byte_identical(tmp_path: Path) -> None:
    replay = tmp_path / "replay.json"
    subprocess.run(
        [
            sys.executable,
            "experiments/quadratic_physical_onset_stop_go.py",
            "--output",
            str(replay),
        ],
        cwd=REPOSITORY,
        env={**dict(__import__("os").environ), "PYTHONPATH": "build/testdeps:src"},
        check=True,
    )
    assert replay.read_bytes() == RESULT.read_bytes()


def test_frozen_artifact_and_note_hashes() -> None:
    assert sha256(RESULT.read_bytes()).hexdigest() == EXPECTED_RESULT_SHA256
    assert sha256(NOTE.read_bytes()).hexdigest() == EXPECTED_NOTE_SHA256


def test_note_uses_strict_stop_go_language() -> None:
    text = NOTE.read_text(encoding="utf-8")
    for phrase in (
        "does not compose",
        "controlled terminal transfer",
        "not an input-independent onset theorem",
        "not a basin theorem",
        "canonical flow-hull history",
        "permanent face no-return",
        "strict common bound",
    ):
        assert phrase in text
