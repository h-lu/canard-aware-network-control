"""Hostile tests for the quadratic reference-slice dual-basin no-go."""

from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest
import sympy as sp

from canard_control.quadratic_reference_dual_basin_no_go import (
    AMPLITUDE_RESULT_SHA256,
    AUTONOMOUS_HANDOFF_RESULT_SHA256,
    PERIODIC_ATTRACTION_RESULT_SHA256,
    STOP_GO_RESULT_SHA256,
    SYNCHRONOUS_FLOQUET_RESULT_SHA256,
    no_go_algebra_is_exact,
    reference_equilibrium_rouche_audit,
    reference_no_go_certificate,
    reference_periodic_face_audit,
    reference_repair_contract_audit,
    validate_no_go_payload,
)


REPOSITORY = Path(__file__).resolve().parents[1]
RESULT = (
    REPOSITORY
    / "experiments/results/quadratic_reference_dual_basin_no_go.json"
)
NOTE = REPOSITORY / "docs/quadratic-reference-slice-dual-basin-no-go.md"
EXPECTED_RESULT_SHA256 = (
    "0f0fe9255b8a3e59f0e4ea245a245d01bb6f1678a748476e00ee0214d38bd78c"
)
EXPECTED_NOTE_SHA256 = (
    "0d06842628a48049e9fa10849bf41bcc7121bf72d29f0d5b90117856e5bc2a65"
)


def _payload() -> dict:
    return json.loads(RESULT.read_text(encoding="utf-8"))


def test_unique_synchronous_equilibrium_and_linear_coefficients_are_exact() -> None:
    audit = reference_equilibrium_rouche_audit()
    assert audit.epsilon == sp.Rational(1, 5)
    assert audit.unfolding == sp.Rational(3, 5)
    assert audit.equilibrium_voltage == sp.Rational(3, 5)
    assert audit.equilibrium_recovery == sp.Rational(66, 125)
    assert audit.local_cubic_derivative == sp.Rational(16, 25)
    assert audit.delayed_cubic_derivative == sp.Rational(12, 25)
    assert audit.effective_delay_gain_center == sp.Rational(8, 125)
    assert audit.reference_current_coefficient == sp.Rational(72, 125)


def test_reference_polynomial_has_two_right_half_plane_centers() -> None:
    audit = reference_equilibrium_rouche_audit()
    plus, minus = audit.reference_polynomial_roots
    assert sp.re(plus) == sp.Rational(36, 125)
    assert sp.re(minus) == sp.Rational(36, 125)
    assert sp.im(plus) == sp.sqrt(1829) / 125
    assert sp.im(minus) == -sp.sqrt(1829) / 125
    assert sp.simplify(abs(plus) - 1 / sp.sqrt(5)) == 0


def test_two_rouche_disks_are_disjoint_and_strictly_right_half_plane() -> None:
    audit = reference_equilibrium_rouche_audit()
    assert audit.disk_radius == sp.Rational(1, 10)
    assert audit.disk_real_part_lower == sp.Rational(47, 250)
    assert audit.disk_center_separation == 2 * sp.sqrt(1829) / 125
    assert audit.two_disks_disjoint
    assert audit.each_disk_in_open_right_half_plane


def test_rouche_margin_survives_gain_and_eta_boxes() -> None:
    audit = reference_equilibrium_rouche_audit()
    assert audit.gain_half_width == sp.Rational(1, 10**12)
    assert audit.eta_abs_upper == sp.Rational(1, 1000)
    assert audit.effective_delay_gain_variation_upper == sp.Rational(
        37, 125 * 10**12
    )
    assert audit.eta_current_delay_gain_per_abs_eta == sp.Rational(4, 25)
    assert audit.polynomial_boundary_lower > 0
    assert audit.characteristic_perturbation_boundary_upper > 0
    assert audit.rouche_margin_lower > 0
    assert float(audit.rouche_margin_lower) > 0.023


def test_periodic_extrema_force_three_two_sided_crossings() -> None:
    audit = reference_periodic_face_audit()
    assert audit.voltage_maximum_lower > sp.Rational(3, 2)
    assert audit.voltage_minimum_upper < -1
    assert audit.positive_detector_two_sided
    assert audit.positive_excursion_two_sided
    assert audit.negative_detector_two_sided
    assert audit.positive_detector_upper_margin > 0
    assert audit.positive_detector_lower_margin > 0
    assert audit.positive_excursion_upper_margin > 0
    assert audit.positive_excursion_lower_margin > 0
    assert audit.negative_detector_upper_margin > 0
    assert audit.negative_detector_lower_margin > 0


def test_negative_excursion_face_lies_strictly_below_periodic_orbit() -> None:
    audit = reference_periodic_face_audit()
    assert audit.negative_excursion_face == -sp.Rational(6, 5)
    assert audit.voltage_minimum_lower > audit.negative_excursion_face
    assert audit.negative_excursion_orbit_strictly_above
    assert audit.negative_excursion_orbit_above_margin > 0


def test_certificate_refuses_rest_quiet_basin_and_permanent_faces() -> None:
    assert no_go_algebra_is_exact()
    certificate = reference_no_go_certificate()
    assert certificate.unique_synchronous_equilibrium_validated
    assert certificate.two_distinct_synchronous_right_half_plane_roots_validated
    assert certificate.equilibrium_instability_uniform_on_gain_eta_box_validated
    assert not certificate.synchronous_equilibrium_local_attractor_validated
    assert not certificate.synchronous_equilibrium_quiet_basin_validated
    assert certificate.eta_zero_pulse_periodic_local_attraction_validated
    assert certificate.permanent_face_no_return_incompatible_with_periodic_capture_validated
    assert not certificate.periodic_capture_permanent_positive_detector_upper_side_validated
    assert not certificate.periodic_capture_permanent_positive_excursion_upper_side_validated
    assert not certificate.periodic_capture_permanent_negative_detector_lower_side_validated
    assert not certificate.periodic_capture_permanent_negative_excursion_lower_side_validated


def test_certificate_does_not_promote_local_no_go_to_global_uniqueness() -> None:
    certificate = reference_no_go_certificate()
    assert not certificate.current_slice_rest_versus_pulse_dual_basin_validated
    assert not certificate.different_quiet_attractor_existence_validated
    assert not certificate.different_quiet_attractor_excluded_validated
    assert not certificate.current_slice_any_dual_basin_structurally_impossible_validated
    assert not certificate.global_single_attractor_validated
    assert not certificate.terminal_blocks_inside_periodic_basin_validated


def test_three_repairs_keep_their_scopes_distinct() -> None:
    audit = reference_repair_contract_audit()
    assert len(audit.autonomous_bistable_slice_required_tasks) == 5
    assert len(audit.latch_contract) == 4
    assert len(audit.post_event_switch_required_tasks) == 4
    assert "neither a physical invariant half-space" in audit.latch_scope
    assert "not an autonomous dual basin" in audit.post_event_switch_scope
    certificate = reference_no_go_certificate()
    assert certificate.autonomous_bistable_repair_contract_specified_validated
    assert not certificate.autonomous_bistable_repair_completed_validated
    assert certificate.latched_first_hit_label_is_immutable_by_definition_validated
    assert not certificate.latched_first_hit_is_physical_basin_validated
    assert certificate.post_event_parameter_switch_contract_specified_validated
    assert not certificate.post_event_parameter_switch_capture_validated
    assert not certificate.post_event_parameter_switch_is_autonomous_dual_basin_validated


def test_parent_hashes_are_pinned() -> None:
    pairs = (
        ("experiments/results/fhn_unsquared_amplitude_transfer.json", AMPLITUDE_RESULT_SHA256),
        ("experiments/results/fhn_dobrushin_periodic_attraction.json", PERIODIC_ATTRACTION_RESULT_SHA256),
        ("experiments/results/fhn_synchronous_floquet_right_half_cover.json", SYNCHRONOUS_FLOQUET_RESULT_SHA256),
        ("experiments/results/fhn_autonomous_handoff_excursion.json", AUTONOMOUS_HANDOFF_RESULT_SHA256),
        ("experiments/results/quadratic_physical_onset_stop_go.json", STOP_GO_RESULT_SHA256),
    )
    for relative_path, expected in pairs:
        assert sha256((REPOSITORY / relative_path).read_bytes()).hexdigest() == expected


def test_artifact_validates_and_basin_promotion_is_rejected() -> None:
    payload = _payload()
    assert validate_no_go_payload(payload) == reference_no_go_certificate()
    promoted = deepcopy(payload)
    promoted["scope"]["synchronous_equilibrium_quiet_basin"] = True
    with pytest.raises(ValueError, match="promoted"):
        validate_no_go_payload(promoted)


def test_audit_parent_and_source_tampering_are_rejected() -> None:
    payload = _payload()
    changed = deepcopy(payload)
    changed["exact_audits"]["equilibrium_rouche"]["rouche_margin_lower"] = "0"
    with pytest.raises(ValueError, match="exact_audits"):
        validate_no_go_payload(changed)
    changed = deepcopy(payload)
    changed["provenance"]["parent_claim_checks"]["uniform_basin_refused"] = False
    with pytest.raises(ValueError, match="parent claim"):
        validate_no_go_payload(changed)
    changed = deepcopy(payload)
    changed["provenance"]["proof_source_sha256"] = "0" * 64
    with pytest.raises(ValueError, match="source-bound"):
        validate_no_go_payload(changed)


def test_default_generator_replay_is_byte_identical(tmp_path: Path) -> None:
    replay = tmp_path / "replay.json"
    subprocess.run(
        [
            sys.executable,
            "experiments/quadratic_reference_dual_basin_no_go.py",
            "--output",
            str(replay),
        ],
        cwd=REPOSITORY,
        env={**os.environ, "PYTHONPATH": "build/testdeps:src"},
        check=True,
    )
    assert replay.read_bytes() == RESULT.read_bytes()


def test_frozen_artifact_and_note_hashes() -> None:
    assert sha256(RESULT.read_bytes()).hexdigest() == EXPECTED_RESULT_SHA256
    assert sha256(NOTE.read_bytes()).hexdigest() == EXPECTED_NOTE_SHA256


def test_note_keeps_no_go_and_repairs_non_tautological() -> None:
    text = NOTE.read_text(encoding="utf-8")
    for phrase in (
        "not a quiet attractor",
        "does not exclude a different quiet attractor",
        "permanent detector-face no-return is incompatible",
        "immutable event memory",
        "not a physical basin",
        "policy-dependent hybrid capture",
        "same autonomous RFDE",
    ):
        assert phrase in text
