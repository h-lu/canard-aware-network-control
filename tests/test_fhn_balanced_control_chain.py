"""Hostile regression tests for the balanced bounded FHN control chain."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import replace
from decimal import Decimal, localcontext
from hashlib import sha256
import json
from pathlib import Path

import pytest
import sympy as sp

from canard_control.fhn_balanced_control_chain import (
    BalancedControlChainSourceEvidence,
    TRACKED_AMPLITUDE_SAFETY_SHA256,
    TRACKED_BOUNDED_PREPARATION_SHA256,
    TRACKED_GENERAL_SIGN_CONE_SHA256,
    balanced_control_algebra,
    balanced_control_chain_from_payloads,
    balanced_two_delay_audit,
    balanced_two_delay_audit_is_exact,
    load_balanced_control_chain_result,
    reference_balanced_two_delay_audits,
    validate_balanced_control_chain_result_payload,
)


REPOSITORY = Path(__file__).resolve().parents[1]
PREPARATION = (
    REPOSITORY
    / "experiments/results/fhn_bounded_additive_preparation.json"
)
SIGN_CONE = (
    REPOSITORY / "experiments/results/fhn_general_network_sign_cone.json"
)
AMPLITUDE_SAFETY = (
    REPOSITORY
    / "experiments/results/fhn_same_model_amplitude_safety.json"
)
RESULT = REPOSITORY / "experiments/results/fhn_balanced_control_chain.json"
NOTE = (
    REPOSITORY
    / "docs/paper-iv-balanced-general-topology-bounded-control-chain.md"
)
EXPECTED_RESULT_SHA256 = (
    "090e690808d9106152958c1338980fde686875a4113241c8c842683a43d1ebf9"
)
EXPECTED_NOTE_SHA256 = (
    "c421ebd7305698bb8a8bbd508b5ae314390a17f24aab04b79e6609c9c46fb87d"
)


def _read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _payloads() -> tuple[dict, dict, dict]:
    return _read(PREPARATION), _read(SIGN_CONE), _read(AMPLITUDE_SAFETY)


def _evidence() -> BalancedControlChainSourceEvidence:
    return BalancedControlChainSourceEvidence(
        bounded_preparation_result_sha256=(
            TRACKED_BOUNDED_PREPARATION_SHA256
        ),
        general_sign_cone_result_sha256=TRACKED_GENERAL_SIGN_CONE_SHA256,
        amplitude_safety_result_sha256=TRACKED_AMPLITUDE_SAFETY_SHA256,
    )


def _compose(
    preparation: dict | None = None,
    sign: dict | None = None,
    amplitude: dict | None = None,
    evidence: BalancedControlChainSourceEvidence | None = None,
):
    default_preparation, default_sign, default_amplitude = _payloads()
    return balanced_control_chain_from_payloads(
        default_preparation if preparation is None else preparation,
        default_sign if sign is None else sign,
        default_amplitude if amplitude is None else amplitude,
        _evidence() if evidence is None else evidence,
    )


def _cycle(size: int) -> sp.Matrix:
    matrix = sp.zeros(size)
    for row in range(size):
        matrix[row, (row + 1) % size] = 1
    return matrix


def test_reference_audits_include_hostile_balanced_topologies() -> None:
    audits = reference_balanced_two_delay_audits()
    assert len(audits) == 4
    assert all(balanced_two_delay_audit_is_exact(audit) for audit in audits)
    assert audits[1].scaffold_rank == 3
    assert audits[2].scaffold_rank == 4
    assert audits[3].scaffold_rank == 5
    assert audits[2].scaffold_minus_identity_infinity_norm == 2
    assert audits[3].scaffold_minus_identity_infinity_norm == 2
    for audit in audits:
        assert audit.scaffold_infinity_norm == 1
        assert audit.scaffold_minus_identity_infinity_norm <= 2
        assert audit.delay_0_infinity_norm == sp.Rational(1, 2)
        assert audit.delay_1_infinity_norm == sp.Rational(1, 2)
        assert audit.delay_norm_sum == 1


@pytest.mark.parametrize("size", (1, 2, 5, 8))
def test_cycle_topologies_have_exact_cancellation_and_scalar_restriction(
    size: int,
) -> None:
    scaffold = _cycle(size)
    pi = [sp.Rational(1, size)] * size
    algebra = balanced_control_algebra(
        scaffold, pi, scaffold / 2, sp.eye(size) / 2
    )
    zero = sp.zeros(size, 1)
    assert algebra.preparation_voltage_cancellation_residual == zero
    assert algebra.preparation_recovery_cancellation_residual == zero
    assert algebra.decision_recovery_cancellation_residual == zero
    assert algebra.decision_voltage_input_residual == zero
    assert algebra.synchronous_voltage_restriction_residual == zero
    assert algebra.synchronous_recovery_restriction_residual == zero


def test_nonuniform_stationary_weight_and_nonrank_topology_are_allowed() -> None:
    half = sp.Rational(1, 2)
    scaffold = sp.Matrix(
        [
            [half, sp.Rational(1, 4), sp.Rational(1, 4)],
            [sp.Rational(1, 8), sp.Rational(5, 8), sp.Rational(1, 4)],
            [sp.Rational(1, 12), sp.Rational(1, 6), sp.Rational(3, 4)],
        ]
    )
    audit = balanced_two_delay_audit(
        scaffold,
        [sp.Rational(1, 6), sp.Rational(1, 3), half],
        scaffold / 2,
        sp.eye(3) / 2,
    )
    assert balanced_two_delay_audit_is_exact(audit)
    assert audit.scaffold_rank == 3


@pytest.mark.parametrize(
    ("scaffold", "pi", "delay_0", "delay_1"),
    (
        ([[1, 0], [0, 1]], [1, 0], [[sp.Rational(1, 2), 0], [0, sp.Rational(1, 2)]], [[sp.Rational(1, 2), 0], [0, sp.Rational(1, 2)]]),
        ([[1, 0], [0, 1]], [sp.Rational(1, 2)] * 2, [[1, 0], [0, 1]], [[0, 0], [0, 0]]),
        ([[1, 0], [0, 1]], [sp.Rational(1, 2)] * 2, [[sp.Rational(1, 2), 0], [0, sp.Rational(1, 2)]], [[sp.Rational(1, 2), 0], [-1, sp.Rational(3, 2)]]),
    ),
)
def test_missing_positive_balance_or_half_layer_structure_is_refused(
    scaffold, pi, delay_0, delay_1
) -> None:
    audit = balanced_two_delay_audit(scaffold, pi, delay_0, delay_1)
    assert not balanced_two_delay_audit_is_exact(audit)
    with pytest.raises(ValueError, match="balanced two-delay class"):
        balanced_control_algebra(scaffold, pi, delay_0, delay_1)


def test_composed_theorem_closes_the_entire_bounded_staged_chain() -> None:
    certificate = _compose()
    assert certificate.exact_balanced_operator_identities_validated
    assert certificate.arbitrary_finite_node_count_formula_validated
    assert certificate.topology_and_node_count_independent_authority_validated
    assert certificate.bounded_initial_data_cylinder_required
    assert not certificate.rfde_phase_space_compactness_validated
    assert certificate.exact_model_additive_preparation_validated
    assert certificate.finite_time_exact_complete_history_preparation_validated
    assert not certificate.state_overwrite_used
    assert not certificate.impulse_used
    assert (
        certificate.bounded_nodewise_recovery_cancellation_on_decision_tube_validated
    )
    assert certificate.voltage_preparation_feedback_closed_at_release
    assert certificate.positive_controlled_onset_validated
    assert certificate.negative_controlled_onset_validated
    assert certificate.positive_finite_controlled_excursion_validated
    assert certificate.negative_finite_controlled_excursion_validated
    assert certificate.synchronous_subspace_invariance_validated
    assert certificate.topology_independent_synchronous_scalar_restriction_validated
    assert certificate.synchronous_branch_frequency_amplitude_outputs_validated
    assert certificate.general_topology_synchronous_branch_three_output_balls_validated
    assert certificate.unique_preimage_for_each_target_validated
    assert certificate.end_to_end_staged_control_chain_validated


def test_universal_authority_recomposes_below_parent_directed_endpoints() -> None:
    certificate = _compose()
    with localcontext() as context:
        context.prec = 110
        v = Decimal(2)
        w = Decimal(2)
        reset = Decimal("0.75")
        epsilon = Decimal(1) / Decimal(5)
        unfolding = Decimal(3) / Decimal(5)
        kappa_1 = Decimal(certificate.kappa_1_interval[1])
        kappa_3 = Decimal(certificate.kappa_3_interval[1])
        voltage_formula = (
            v
            + v**3 / Decimal(3)
            + w
            + Decimal(2) * Decimal(3) * v
            + Decimal(2) * epsilon * kappa_1 * v
            + Decimal(2) * epsilon * kappa_3 * (v + 1) ** 3
            + (v + reset).sqrt()
        )
        recovery_formula = (
            epsilon * (v + unfolding)
            + Decimal(2) * Decimal(2) * w
            + w.sqrt()
        )
        assert Decimal(certificate.voltage_input_authority_upper) >= (
            voltage_formula
        )
        assert Decimal(certificate.recovery_input_authority_upper) >= (
            recovery_formula
        )
        assert Decimal(
            certificate.decision_recovery_input_authority_upper
        ) >= epsilon * (Decimal("1.5") + unfolding)
    assert float(certificate.voltage_input_authority_upper) < 23.19
    assert float(certificate.recovery_input_authority_upper) < 9.94
    assert float(certificate.decision_recovery_input_authority_upper) < 0.421


def test_translated_reset_balls_enter_the_sign_cones_with_large_margin() -> None:
    certificate = _compose()
    assert certificate.pulse_reset_projection == (
        "0.499999999999",
        "0.500000000001",
    )
    assert certificate.quiet_reset_projection == (
        "-0.500000000001",
        "-0.499999999999",
    )
    assert Decimal(
        certificate.pulse_initial_mean_margin_over_sign_cone_lower
    ) == Decimal("0.439999999999")
    assert Decimal(
        certificate.quiet_initial_mean_margin_over_sign_cone_lower
    ) == Decimal("0.439999999999")
    assert Decimal(certificate.reset_abs_bound) > max(
        abs(Decimal(item))
        for item in (
            *certificate.pulse_reset_projection,
            *certificate.quiet_reset_projection,
        )
    )


def test_deadlines_are_composed_from_preparation_start_in_safe_direction() -> None:
    certificate = _compose()
    preparation = Decimal(certificate.complete_history_preparation_time_upper)
    with localcontext() as context:
        context.prec = 110
        for after_release, from_start in (
            (
                certificate.positive_detector_deadline_after_release_upper,
                certificate.positive_detector_deadline_from_start_upper,
            ),
            (
                certificate.negative_detector_deadline_after_release_upper,
                certificate.negative_detector_deadline_from_start_upper,
            ),
            (
                certificate.positive_excursion_deadline_after_release_upper,
                certificate.positive_excursion_deadline_from_start_upper,
            ),
            (
                certificate.negative_excursion_deadline_after_release_upper,
                certificate.negative_excursion_deadline_from_start_upper,
            ),
        ):
            assert Decimal(from_start) >= preparation + Decimal(after_release)
    assert float(certificate.positive_detector_deadline_from_start_upper) < 20.40
    assert float(certificate.negative_detector_deadline_from_start_upper) < 24.67
    assert float(certificate.positive_excursion_deadline_from_start_upper) < 68.15
    assert float(certificate.negative_excursion_deadline_from_start_upper) < 52.91


def test_frequency_amplitude_claim_is_synchronous_only() -> None:
    certificate = _compose()
    assert certificate.map_definition == (
        "Q_A(kappa_1,kappa_3,r)=(F_sync,A_sync,-r)"
    )
    assert certificate.output_order == (
        "F_sync",
        "A_sync=V_max-V_min",
        "S_op=-r",
    )
    assert float(certificate.output_ball_radius_lower) > 2.75e-15
    assert certificate.input_ball_radius == "1e-12"
    assert not certificate.asynchronous_frequency_amplitude_outputs_validated
    assert not certificate.transverse_attraction_validated
    assert not certificate.full_network_periodic_attraction_validated


@pytest.mark.parametrize(
    "field",
    (
        "bounded_preparation_result_sha256",
        "general_sign_cone_result_sha256",
        "amplitude_safety_result_sha256",
    ),
)
def test_mismatched_parent_digest_is_refused(field: str) -> None:
    forged = replace(_evidence(), **{field: "0" * 64})
    with pytest.raises(ValueError, match="source evidence digest"):
        _compose(evidence=forged)


def test_fixed_topology_parent_is_extended_without_forging_parent_scope() -> None:
    preparation, _, _ = _payloads()
    assert not preparation["scope"]["general_network_topology"]
    forged = deepcopy(preparation)
    forged["scope"]["general_network_topology"] = True
    with pytest.raises(ValueError, match="must be false"):
        _compose(preparation=forged)


def test_bounded_cylinder_must_not_be_promoted_to_phase_space_compactness() -> None:
    preparation, _, _ = _payloads()
    forged = deepcopy(preparation)
    forged["certificate"]["rfde_phase_space_compactness_validated"] = True
    with pytest.raises(ValueError, match="must be false"):
        _compose(preparation=forged)


def test_ideal_sign_cone_clamp_is_realized_without_promoting_hardware() -> None:
    _, sign, _ = _payloads()
    assert not sign["scope"]["bounded_actuator"]
    assert not sign["scope"]["hardware"]
    forged = deepcopy(sign)
    forged["scope"]["bounded_actuator"] = True
    with pytest.raises(ValueError, match="must be false"):
        _compose(sign=forged)


def test_cross_source_gain_or_delay_mismatch_is_refused() -> None:
    preparation, sign, _ = _payloads()
    wrong_gain = deepcopy(preparation)
    wrong_gain["certificate"]["kappa_1_interval"][1] = "0.3"
    with pytest.raises(ValueError, match="gain boxes disagree"):
        _compose(preparation=wrong_gain)
    wrong_delay = deepcopy(sign)
    wrong_delay["certificate"]["reference_delay_weights"] = ["1", "0"]
    with pytest.raises(ValueError, match="two-half-layer|invalid"):
        _compose(sign=wrong_delay)


def test_amplitude_parent_cannot_be_promoted_to_asynchronous_output() -> None:
    _, _, amplitude = _payloads()
    forged = deepcopy(amplitude)
    forged["scope"]["general_topology"] = True
    with pytest.raises(ValueError, match="must be false"):
        _compose(amplitude=forged)


def test_tracked_result_is_hash_and_manifest_bound() -> None:
    raw = RESULT.read_bytes()
    assert sha256(raw).hexdigest() == EXPECTED_RESULT_SHA256
    payload = json.loads(raw)
    validate_balanced_control_chain_result_payload(payload)
    provenance = payload["provenance"]
    generator = REPOSITORY / provenance["generator"]
    assert sha256(generator.read_bytes()).hexdigest() == provenance[
        "generator_sha256"
    ]
    for manifest_name in ("proof_source_manifest", "parent_result_manifest"):
        for relative, digest in provenance[manifest_name].items():
            assert sha256((REPOSITORY / relative).read_bytes()).hexdigest() == digest
    loaded = load_balanced_control_chain_result(
        RESULT, expected_sha256=EXPECTED_RESULT_SHA256
    )
    assert loaded["scope"]["end_to_end_staged_control_chain"]
    assert not loaded["scope"]["rfde_phase_space_compactness"]


@pytest.mark.parametrize(
    "scope_key",
    (
        "rfde_phase_space_compactness",
        "asynchronous_frequency_amplitude_outputs",
        "transverse_attraction",
        "full_network_periodic_attraction",
        "unforced_onset",
        "maximal_canard_onset",
        "biological_basin",
        "action_potential",
        "general_topology_canard_root_equivalence",
        "model_uncertainty",
        "measurement_noise",
        "bandwidth",
        "hardware",
    ),
)
def test_result_validator_refuses_scope_promotions(scope_key: str) -> None:
    forged = _read(RESULT)
    forged["scope"][scope_key] = True
    with pytest.raises(ValueError, match="must be false"):
        validate_balanced_control_chain_result_payload(forged)


def test_result_loader_refuses_wrong_digest() -> None:
    with pytest.raises(ValueError, match="SHA-256 mismatch"):
        load_balanced_control_chain_result(RESULT, expected_sha256="0" * 64)


def test_result_validator_refuses_enlarged_ball_or_shortened_deadline() -> None:
    enlarged = _read(RESULT)
    enlarged["certificate"]["output_ball_radius_lower"] = "1e-3"
    with pytest.raises(ValueError, match="output radius is invalid"):
        validate_balanced_control_chain_result_payload(enlarged)
    shortened = _read(RESULT)
    shortened["certificate"][
        "positive_detector_deadline_from_start_upper"
    ] = "1"
    with pytest.raises(ValueError, match="deadline composition is invalid"):
        validate_balanced_control_chain_result_payload(shortened)


def test_note_uses_bounded_cylinder_and_synchronous_output_language() -> None:
    raw = NOTE.read_bytes()
    assert sha256(raw).hexdigest() == EXPECTED_NOTE_SHA256
    assert not any(
        byte <= 9 or 11 <= byte <= 31 or byte == 127
        for byte in raw
    )
    text = raw.decode("utf-8")
    assert "bounded initial-data cylinder" in text
    assert "not compact" in text
    assert "synchronous-branch" in text
    assert "asynchronous" in text
    assert EXPECTED_RESULT_SHA256 in text
    assert text.count(r"\(") == text.count(r"\)")
    assert text.count(r"\[") == text.count(r"\]")
    assert r"\square" in text
