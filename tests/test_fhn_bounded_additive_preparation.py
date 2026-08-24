"""Hostile regression tests for bounded-additive FHN preparation."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import replace
from decimal import Decimal, localcontext
from hashlib import sha256
import json
import math
from pathlib import Path

import pytest
import sympy as sp

from canard_control.fhn_bounded_additive_preparation import (
    BoundedPreparationSourceEvidence,
    TRACKED_CAUSAL_HOLD_NOTE_SHA256,
    TRACKED_SEPARATOR_RESULT_SHA256,
    bounded_additive_preparation_from_payload,
    finite_time_reaching_profile,
    load_bounded_additive_preparation_result,
    preparation_network_algebra,
    sigma_half,
)


REPOSITORY = Path(__file__).resolve().parents[1]
SEPARATOR_RESULT = (
    REPOSITORY / "experiments/results/fhn_same_model_separator.json"
)
CAUSAL_HOLD_NOTE = REPOSITORY / "docs/paper-iv-causal-hold-sign-cone.md"
PREPARATION_RESULT = (
    REPOSITORY / "experiments/results/fhn_bounded_additive_preparation.json"
)
PREPARATION_NOTE = (
    REPOSITORY / "docs/paper-iv-bounded-additive-preparation.md"
)
EXPECTED_PREPARATION_RESULT_SHA256 = (
    "8681f800c42420207a94f505b3c8831c7409f3619cf640cbd24de580cd87f548"
)


def _separator() -> dict:
    return json.loads(SEPARATOR_RESULT.read_text(encoding="utf-8"))


def _evidence() -> BoundedPreparationSourceEvidence:
    return BoundedPreparationSourceEvidence(
        separator_result_sha256=TRACKED_SEPARATOR_RESULT_SHA256,
        causal_hold_note_sha256=TRACKED_CAUSAL_HOLD_NOTE_SHA256,
        source_synchronous_model_id=(
            "dual-scaffold-synchronous-fhn-two-delay"
        ),
        full_network_instance_id="rank-one-two-module-fhn-D3-E2",
    )


def _certificate(separator: dict | None = None, **changes):
    arguments = {
        "voltage_history_sup_bound": "2",
        "recovery_current_sup_bound": "2",
        "reset_abs_bound": "0.75",
        "voltage_reaching_gain": "1",
        "recovery_reaching_gain": "1",
        "decision_voltage_tube_bound": "1.5",
    }
    arguments.update(changes)
    return bounded_additive_preparation_from_payload(
        _separator() if separator is None else separator,
        _evidence(),
        **arguments,
    )


@pytest.mark.parametrize("module_sizes", ((1, 1), (2, 3), (4, 2), (3, 7)))
def test_delay_layers_and_exact_cancellation_are_formulaic(
    module_sizes: tuple[int, int],
) -> None:
    algebra = preparation_network_algebra(*module_sizes)
    dimension = sum(module_sizes)
    assert algebra.delay_sum_residual == sp.zeros(dimension)
    assert algebra.averaging_row_sums == (sp.Integer(1),) * dimension
    assert algebra.same_delay_row_sums == (sp.Rational(1, 2),) * dimension
    assert algebra.cross_delay_row_sums == (sp.Rational(1, 2),) * dimension
    assert algebra.averaging_sup_norm == 1
    assert algebra.same_delay_sup_norm == sp.Rational(1, 2)
    assert algebra.cross_delay_sup_norm == sp.Rational(1, 2)
    expected_scaffold = 2 - sp.Rational(1, max(module_sizes))
    assert algebra.scaffold_sup_norm == expected_scaffold
    assert algebra.scaffold_strict_two_gap == sp.Rational(
        1, max(module_sizes)
    )
    assert algebra.voltage_cancellation_residual == sp.zeros(dimension, 1)
    assert algebra.recovery_cancellation_residual == sp.zeros(dimension, 1)
    assert algebra.nodewise_decision_recovery_residual == sp.zeros(
        dimension, 1
    )
    assert algebra.nodewise_decision_voltage_preservation_residual == sp.zeros(
        dimension, 1
    )


def test_directed_numerical_instance_closes_the_declared_bounds() -> None:
    certificate = _certificate()
    assert certificate.reachable_voltage_sup_bound == "2"
    assert certificate.voltage_initial_error_sup_bound.startswith("2.75")
    assert float(certificate.voltage_input_authority_upper) < 23.19
    assert float(certificate.voltage_input_authority_upper) > 23.184
    assert float(certificate.recovery_input_authority_upper) < 9.94
    assert float(certificate.recovery_input_authority_upper) > 9.934
    assert float(certificate.settling_time_upper) < 3.317
    assert float(certificate.exact_history_hold_time_upper) < 11.181
    assert float(certificate.complete_history_preparation_time_upper) < 14.50
    assert certificate.voltage_authority_below_ceiling
    assert certificate.recovery_authority_below_ceiling
    assert certificate.complete_preparation_time_below_ceiling


def test_public_upper_endpoints_recompose_in_the_safe_direction() -> None:
    certificate = _certificate()
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
        settling_formula = Decimal(2) * (v + reset).sqrt()
        complete_formula = settling_formula + Decimal(5) * Decimal(5).sqrt()
        assert Decimal(certificate.voltage_input_authority_upper) >= (
            voltage_formula
        )
        assert Decimal(certificate.recovery_input_authority_upper) >= (
            recovery_formula
        )
        assert Decimal(certificate.voltage_settling_time_upper) >= (
            settling_formula
        )
        assert Decimal(certificate.complete_history_preparation_time_upper) >= (
            complete_formula
        )


def test_sigma_half_is_monotone_and_closed_field_is_one_sided_lipschitz() -> None:
    samples = (-4.0, -1.0, -0.01, 0.0, 0.01, 1.0, 4.0)
    values = [sigma_half(item) for item in samples]
    assert values == sorted(values)
    for x in samples:
        for y in samples:
            closed_difference = -sigma_half(x) + sigma_half(y)
            assert (x - y) * closed_difference <= 1e-15
    with pytest.raises(ValueError, match="finite"):
        sigma_half(float("nan"))


@pytest.mark.parametrize("initial", (-2.75, -0.25, 0.0, 0.25, 2.75))
def test_explicit_reaching_profile_hits_and_sticks(initial: float) -> None:
    settling = 2 * math.sqrt(abs(initial))
    assert finite_time_reaching_profile(initial, 1, 0) == initial
    assert abs(finite_time_reaching_profile(initial, 1, settling)) < 1e-28
    assert finite_time_reaching_profile(initial, 1, settling + 10) == 0
    if initial:
        midpoint = finite_time_reaching_profile(initial, 1, settling / 2)
        assert math.copysign(1, midpoint) == math.copysign(1, initial)
        assert abs(midpoint) < abs(initial)
    with pytest.raises(ValueError):
        finite_time_reaching_profile(initial, 0, 1)


def test_optional_nodewise_recovery_continuation_is_separate_and_bounded() -> None:
    certificate = _certificate()
    assert certificate.optional_nodewise_recovery_cancellation_exact
    assert certificate.optional_nodewise_zero_recovery_leaf_invariant
    assert certificate.optional_nodewise_voltage_dynamics_preserved
    assert certificate.optional_nodewise_authority_conditional_on_voltage_tube
    assert certificate.optional_nodewise_route_distinct_from_collective_clamp
    assert certificate.collective_clamp_route_still_available_separately
    assert Decimal(
        certificate.optional_nodewise_recovery_authority_upper
    ) >= Decimal("0.42")
    assert float(certificate.optional_nodewise_recovery_authority_upper) < 0.421


def test_exact_scope_distinguishes_bounded_input_from_hardware() -> None:
    certificate = _certificate()
    assert certificate.exact_baseline_voltage_cancellation
    assert certificate.exact_baseline_recovery_cancellation
    assert certificate.closed_loop_componentwise_reaching_law
    assert certificate.sigma_half_continuous
    assert not certificate.sigma_half_locally_lipschitz_at_zero
    assert certificate.closed_loop_one_sided_lipschitz
    assert certificate.caratheodory_forward_existence
    assert certificate.forward_uniqueness
    assert not certificate.backward_uniqueness_validated
    assert certificate.finite_time_exact_state_preparation
    assert certificate.predetermined_settling_schedule_validated
    assert certificate.same_feedback_holds_target_after_settling
    assert certificate.maximum_delay_hold_produces_exact_complete_history
    assert certificate.causal_current_and_discrete_delay_measurement
    assert not certificate.future_history_measurement_required
    assert not certificate.recovery_history_measurement_required
    assert certificate.bounded_additive_input_on_declared_bounded_cylinder
    assert certificate.bounded_initial_data_cylinder_required
    assert not certificate.rfde_phase_space_compactness_validated
    assert certificate.input_bound_independent_of_node_count
    assert not certificate.state_overwrite_used
    assert not certificate.impulse_used
    assert certificate.release_switch_preserves_state_continuity
    assert certificate.exact_model_cancellation_required
    assert certificate.full_node_state_measurement_required
    assert certificate.both_delayed_voltage_layers_required
    for value in (
        certificate.bandwidth_validated,
        certificate.slew_rate_validated,
        certificate.energy_validated,
        certificate.model_uncertainty_validated,
        certificate.measurement_noise_validated,
        certificate.hardware_implementation_validated,
        certificate.uniform_control_from_unbounded_initial_sets,
        certificate.general_network_topology_validated,
        certificate.issue_15_closed,
    ):
        assert not value


@pytest.mark.parametrize(
    ("field", "value", "message"),
    (
        ("separator_result_sha256", "0" * 64, "separator result SHA-256"),
        ("causal_hold_note_sha256", "0" * 64, "causal-hold note SHA-256"),
        ("source_synchronous_model_id", "generic-fhn", "different model"),
        ("full_network_instance_id", "generic-network", "different network"),
    ),
)
def test_mismatched_source_evidence_is_refused(
    field: str, value: str, message: str
) -> None:
    evidence = replace(_evidence(), **{field: value})
    with pytest.raises(ValueError, match=message):
        bounded_additive_preparation_from_payload(
            _separator(),
            evidence,
            voltage_history_sup_bound="2",
            recovery_current_sup_bound="2",
            reset_abs_bound="0.75",
            voltage_reaching_gain="1",
            recovery_reaching_gain="1",
        )


@pytest.mark.parametrize(
    ("field", "value"),
    (
        ("voltage_history_sup_bound", "-1"),
        ("recovery_current_sup_bound", "-1"),
        ("reset_abs_bound", "1.01"),
        ("voltage_reaching_gain", "0"),
        ("recovery_reaching_gain", "-1"),
        ("decision_voltage_tube_bound", "-1"),
    ),
)
def test_invalid_bounded_cylinder_or_gain_is_refused(
    field: str, value: str
) -> None:
    with pytest.raises(ValueError):
        _certificate(**{field: value})


def test_forged_model_constant_and_scope_promotion_are_refused() -> None:
    wrong_constant = _separator()
    wrong_constant["certificate"]["voltage_scaffold"] = "4"
    with pytest.raises(ValueError):
        _certificate(wrong_constant)
    promoted = _separator()
    promoted["scope"]["general_network_topology"] = True
    with pytest.raises(ValueError, match="must be false|forged or promoted"):
        _certificate(promoted)


def test_generated_result_is_hash_source_and_scope_bound() -> None:
    raw = PREPARATION_RESULT.read_bytes()
    assert sha256(raw).hexdigest() == EXPECTED_PREPARATION_RESULT_SHA256
    payload = load_bounded_additive_preparation_result(
        PREPARATION_RESULT,
        expected_sha256=EXPECTED_PREPARATION_RESULT_SHA256,
    )
    provenance = payload["provenance"]
    generator = REPOSITORY / provenance["generator"]
    assert sha256(generator.read_bytes()).hexdigest() == provenance[
        "generator_sha256"
    ]
    for relative, digest in provenance["proof_source_manifest"].items():
        assert sha256((REPOSITORY / relative).read_bytes()).hexdigest() == digest
    evidence = payload["source_evidence"]
    assert sha256(SEPARATOR_RESULT.read_bytes()).hexdigest() == evidence[
        "separator_result_sha256"
    ]
    assert sha256(CAUSAL_HOLD_NOTE.read_bytes()).hexdigest() == evidence[
        "causal_hold_note_sha256"
    ]
    scope = payload["scope"]
    assert scope[
        "bounded_additive_finite_time_preparation_on_declared_bounded_cylinder"
    ]
    assert scope["exact_complete_history_phi_r_after_scheduled_hold"]
    assert scope["node_count_independent_input_authority"]
    assert scope["bounded_initial_data_cylinder_required"]
    assert scope["exact_model_cancellation_required"]
    assert scope[
        "full_node_state_and_both_delayed_voltage_layers_required"
    ]
    assert scope[
        "optional_nodewise_zero_recovery_continuation_on_declared_voltage_tube"
    ]
    for key in (
        "state_overwrite",
        "impulse",
        "bandwidth",
        "slew_rate",
        "energy",
        "model_uncertainty",
        "measurement_noise",
        "hardware_implementation",
        "uniform_control_from_unbounded_initial_sets",
        "rfde_phase_space_compactness",
        "general_network_topology",
        "issue_15_closed",
    ):
        assert not scope[key]


def test_generated_result_loader_refuses_forged_bytes(tmp_path: Path) -> None:
    forged = tmp_path / "preparation.json"
    forged.write_bytes(PREPARATION_RESULT.read_bytes() + b" ")
    with pytest.raises(ValueError, match="SHA-256 mismatch"):
        load_bounded_additive_preparation_result(
            forged,
            expected_sha256=EXPECTED_PREPARATION_RESULT_SHA256,
        )


def test_semantic_loader_refuses_missing_or_promoted_scope(
    tmp_path: Path,
) -> None:
    payload = json.loads(PREPARATION_RESULT.read_text(encoding="utf-8"))
    payload["certificate"]["forward_uniqueness"] = False
    missing = tmp_path / "missing.json"
    missing.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="must be true"):
        load_bounded_additive_preparation_result(
            missing,
            expected_sha256=sha256(missing.read_bytes()).hexdigest(),
        )

    payload = json.loads(PREPARATION_RESULT.read_text(encoding="utf-8"))
    payload["certificate"]["hardware_implementation_validated"] = True
    payload["scope"]["hardware_implementation"] = True
    promoted = tmp_path / "promoted.json"
    promoted.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="forged or promoted"):
        load_bounded_additive_preparation_result(
            promoted,
            expected_sha256=sha256(promoted.read_bytes()).hexdigest(),
        )

    payload = json.loads(PREPARATION_RESULT.read_text(encoding="utf-8"))
    payload["certificate"]["rfde_phase_space_compactness_validated"] = True
    payload["scope"]["rfde_phase_space_compactness"] = True
    compactness_promotion = tmp_path / "compactness-promotion.json"
    compactness_promotion.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="forged or promoted"):
        load_bounded_additive_preparation_result(
            compactness_promotion,
            expected_sha256=sha256(
                compactness_promotion.read_bytes()
            ).hexdigest(),
        )


def test_note_has_raw_safe_math_delimiters_and_no_controls() -> None:
    raw = PREPARATION_NOTE.read_bytes()
    forbidden = set(range(0x00, 0x09)) | {0x0B, 0x0C} | set(
        range(0x0E, 0x20)
    ) | {0x7F}
    assert not any(byte in forbidden for byte in raw)
    text = raw.decode("utf-8")
    assert text.count(r"\(") == text.count(r"\)")
    assert text.count(r"\[") == text.count(r"\]")
    assert r"\sigma_{1/2}(z)=\operatorname{sgn}(z)\sqrt{|z|}" in text
