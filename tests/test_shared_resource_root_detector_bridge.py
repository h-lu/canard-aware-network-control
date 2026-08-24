"""Hostile tests for the shared-resource root-to-detector bridge."""

from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys

import mpmath as mp
import pytest
import sympy as sp

from canard_control.shared_resource_root_detector_bridge import (
    PARENT_PROOF_SOURCE_SHA256,
    PARENT_THEOREM_SHA256,
    bridge_audit_is_exact,
    detector_latency,
    latency_reset_derivative,
    normalized_family_bridge_audit,
    reference_bridge_audits,
    reference_bridge_certificate,
    root_to_latency_coefficient,
    validate_root_detector_bridge_result_payload,
)


REPOSITORY = Path(__file__).resolve().parents[1]
RESULT = (
    REPOSITORY
    / "experiments/results/shared_resource_root_detector_bridge.json"
)
NOTE = (
    REPOSITORY
    / "docs/same-model-shared-resource-root-detector-bridge.md"
)
PARENT_NOTE = (
    REPOSITORY / "docs/paper-ii-heterogeneous-curvature-selected-root.md"
)
PARENT_SOURCE = (
    REPOSITORY / "src/canard_control/heterogeneous_curvature_root.py"
)
EXPECTED_RESULT_SHA256 = (
    "3417d3f0a6e0a6225fc57dd5a1618e6a3ebda6bc6dc1460461e9d261e2799b4a"
)
EXPECTED_NOTE_SHA256 = (
    "e8aae096d59e1212f93dc82f9dc820bbbfb90a141bc86abe62ecb5edf03b04c6"
)


def _payload() -> dict:
    return json.loads(RESULT.read_text(encoding="utf-8"))


def test_reference_all_n_witnesses_are_exact_and_nonzero() -> None:
    audits = reference_bridge_audits()
    assert tuple(audit.node_count for audit in audits) == (2, 3, 5, 8, 13)
    assert all(bridge_audit_is_exact(audit) for audit in audits)
    assert all(
        audit.selected_root_shift_coefficient == -sp.Rational(1, 10)
        for audit in audits
    )
    assert all(audit.root_to_latency_coefficient > 0 for audit in audits)
    assert all(audit.latency_reset_derivative < 0 for audit in audits)


@pytest.mark.parametrize("node_count", (2, 4, 9, 21))
def test_exact_latency_composition_for_arbitrary_finite_samples(
    node_count: int,
) -> None:
    audit = normalized_family_bridge_audit(
        node_count,
        curvature_amplitude=sp.Rational(1, 5),
        layer_floor=sp.Integer(2),
        delay_0=sp.Integer(1),
        delay_1=sp.Integer(4),
        coupling_rate=sp.Integer(3),
        weak_delay_gain=sp.Integer(1),
        cubic_coefficient=sp.Integer(1),
        reset_depth=sp.Rational(1, 4),
        detector_depth=sp.Rational(1, 2),
        reset_transduction_gain=sp.Integer(1),
    )
    assert bridge_audit_is_exact(audit)
    expected = -audit.selected_root_shift_coefficient / (
        sp.Rational(1, 4) ** 2
        * (audit.maximum_curvature - sp.Rational(1, 12))
    )
    assert sp.simplify(audit.root_to_latency_coefficient - expected) == 0


def test_latency_closed_form_matches_high_precision_quadrature() -> None:
    mp.mp.dps = 80
    curvature = mp.mpf("1.17")
    rho = mp.mpf("0.24")
    q = mp.mpf("0.51")
    beta = mp.mpf("0.93")
    quadrature = mp.quad(
        lambda s: 1 / (s**2 * (curvature - beta * s / 3)),
        [rho, q],
    )
    exact = detector_latency(
        sp.Rational(117, 100),
        sp.Rational(6, 25),
        sp.Rational(51, 100),
        sp.Rational(93, 100),
    )
    assert abs(mp.mpf(str(sp.N(exact, 90))) - quadrature) < mp.mpf("1e-70")


def test_reset_derivative_and_root_composition_have_the_required_sign() -> None:
    derivative = latency_reset_derivative(
        sp.Rational(6, 5), sp.Rational(1, 4), sp.Integer(1)
    )
    coefficient = root_to_latency_coefficient(
        -sp.Rational(1, 10),
        sp.Rational(6, 5),
        sp.Rational(1, 4),
        sp.Integer(1),
        sp.Integer(1),
    )
    assert derivative == -sp.Rational(960, 67)
    assert coefficient == sp.Rational(96, 67)


@pytest.mark.parametrize(
    ("curvature", "rho", "q", "beta", "message"),
    (
        (1, 0, sp.Rational(1, 2), 1, "reset_depth"),
        (1, sp.Rational(1, 2), sp.Rational(1, 2), 1, "exceed"),
        (1, sp.Rational(1, 4), 4, 1, "turning"),
        (1, sp.Rational(1, 4), sp.Rational(1, 2), 0, "cubic"),
    ),
)
def test_latency_refuses_degenerate_or_nonmonotone_tubes(
    curvature, rho, q, beta, message
) -> None:
    with pytest.raises(ValueError, match=message):
        detector_latency(curvature, rho, q, beta)


def test_reference_certificate_keeps_physical_claims_false() -> None:
    certificate = reference_bridge_certificate()
    assert (
        certificate.same_underlying_shared_resource_rfde_for_root_and_control_stages_validated
    )
    assert certificate.one_shared_recovery_coordinate_in_both_stages_validated
    assert certificate.controlled_detector_hit_validated
    assert certificate.exact_root_and_model_known_offline_required
    assert (
        certificate.policy_offset_changes_latency_without_changing_uncontrolled_root_validated
    )
    assert certificate.nonzero_root_to_latency_response_validated
    assert not certificate.selected_root_equals_controlled_detector_boundary_validated
    assert not certificate.input_policy_independent_root_to_latency_relation_validated
    assert not certificate.physical_outer_selection_validated
    assert not certificate.unforced_onset_validated
    assert not certificate.maximal_canard_onset_validated
    assert not certificate.autonomous_biological_pulse_validated
    assert not certificate.biological_basin_validated
    assert not certificate.no_return_validated
    assert not certificate.model_uncertainty_validated
    assert not certificate.hardware_validated


def test_parent_theorem_and_source_digests_are_pinned() -> None:
    assert sha256(PARENT_NOTE.read_bytes()).hexdigest() == PARENT_THEOREM_SHA256
    assert sha256(PARENT_SOURCE.read_bytes()).hexdigest() == PARENT_PROOF_SOURCE_SHA256


def test_generated_payload_validates_and_rejects_claim_promotion() -> None:
    payload = _payload()
    certificate = validate_root_detector_bridge_result_payload(payload)
    assert certificate.common_selected_root_shift_coefficient == "-1/10"
    assert sha256(RESULT.read_bytes()).hexdigest() == EXPECTED_RESULT_SHA256
    assert sha256(NOTE.read_bytes()).hexdigest() == EXPECTED_NOTE_SHA256
    hostile = deepcopy(payload)
    hostile["scope"]["unforced_onset"] = True
    with pytest.raises(ValueError, match="forbidden"):
        validate_root_detector_bridge_result_payload(hostile)
    policy_hostile = deepcopy(payload)
    policy_hostile["scope"][
        "input_policy_independent_root_to_latency_relation"
    ] = True
    with pytest.raises(ValueError, match="forbidden"):
        validate_root_detector_bridge_result_payload(policy_hostile)


def test_policy_offset_changes_latency_coefficient_but_not_parent_root() -> None:
    curvature = sp.Rational(6, 5)
    rho = sp.Rational(1, 4)
    beta = sp.Integer(1)
    root_coefficient = -sp.Rational(1, 10)
    gain = sp.Integer(1)
    offset = sp.Rational(7, 13)
    base = root_to_latency_coefficient(
        root_coefficient, curvature, rho, beta, gain
    )
    endpoint_derivative = latency_reset_derivative(curvature, rho, beta)
    perturbed = sp.simplify(base + offset * endpoint_derivative)
    assert sp.simplify(perturbed - base - offset * endpoint_derivative) == 0
    assert perturbed != base
    # The offset belongs only to the reset policy; the pinned parent-root
    # coefficient is unchanged.
    assert root_coefficient == -sp.Rational(1, 10)


def test_generated_record_is_byte_reproducible(tmp_path: Path) -> None:
    output = tmp_path / "bridge.json"
    subprocess.run(
        [
            sys.executable,
            str(REPOSITORY / "experiments/shared_resource_root_detector_bridge.py"),
            "--output",
            str(output),
        ],
        cwd=REPOSITORY,
        check=True,
        stdout=subprocess.DEVNULL,
    )
    assert output.read_bytes() == RESULT.read_bytes()


def test_note_uses_controller_mediated_naming_and_explicitly_denies_equality() -> None:
    text = NOTE.read_text(encoding="utf-8")
    assert "controller-mediated" in text
    assert "does not identify" in text
    assert "selected root with the detector boundary" in text
    assert "autonomous biological pulse" in text
