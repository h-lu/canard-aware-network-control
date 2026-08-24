"""Regression, provenance, and refusal tests for the same-model separator."""

from __future__ import annotations

from copy import deepcopy
from decimal import Decimal, localcontext
from hashlib import sha256
import json
from pathlib import Path

import sympy as sp
import pytest

from canard_control.fhn_same_model_separator import (
    TRACKED_PARAMETER_BOX_SHA256,
    collective_clamp_network_algebra,
    decimal_parent_endpoint_recomposition,
    load_same_model_separator,
    load_same_model_separator_result,
    same_model_separator_algebra,
    same_model_separator_from_payload,
    validate_same_model_separator_result_payload,
)


REPOSITORY = Path(__file__).resolve().parents[1]
SOURCE_RESULT = REPOSITORY / "experiments/results/fhn_periodic_parameter_box.json"
SEPARATOR_RESULT = REPOSITORY / "experiments/results/fhn_same_model_separator.json"
EXPECTED_SEPARATOR_RESULT_SHA256 = (
    "9e859f31c177638a70b3ca451fe743227308343792d77eeca286fca26afc8a86"
)


def _source_payload() -> dict:
    return json.loads(SOURCE_RESULT.read_text(encoding="utf-8"))


def _result_payload() -> dict:
    return json.loads(SEPARATOR_RESULT.read_text(encoding="utf-8"))


def _semantic_source(payload: dict):
    encoded = (json.dumps(payload, sort_keys=True) + "\n").encode()
    return same_model_separator_from_payload(
        payload,
        source_result_sha256=sha256(encoded).hexdigest(),
    )


def test_exact_constant_history_and_signed_secant_algebra() -> None:
    algebra = same_model_separator_algebra()
    assert algebra.delayed_constant_history_residual == 0
    assert algebra.voltage_scaffold_constant_history_residual == 0
    assert algebra.controlled_collective_recovery_residual == 0
    assert algebra.zero_saddle_fast_residual == 0

    x = sp.Symbol("x", real=True)
    u = sp.Symbol("u", nonnegative=True)
    assert algebra.positive_cubic_secant_polynomial == x**2 - 3 * x + 3
    assert algebra.negative_cubic_secant_polynomial == u**2 + 3 * u + 3
    assert algebra.positive_cubic_secant_endpoint == 3
    assert algebra.negative_cubic_secant_endpoint == 7


@pytest.mark.parametrize("module_sizes", ((1, 1), (2, 3), (5, 2)))
def test_exact_full_network_collective_clamp(module_sizes: tuple[int, int]) -> None:
    audit = collective_clamp_network_algebra(*module_sizes)
    dimension = sum(module_sizes)
    assert audit.projection_row_sum == 1
    assert audit.projection_idempotence_residual == sp.zeros(dimension)
    assert sp.simplify(
        audit.collective_actuator_projection
        - audit.expected_collective_actuator_projection
    ) == 0
    assert audit.transverse_actuator_residual == sp.zeros(dimension, 1)
    assert audit.controlled_collective_recovery_derivative == 0
    assert audit.transverse_recovery_derivative_residual == sp.zeros(
        dimension, 1
    )


def test_decimal_recomposition_uses_parent_upper_endpoints_in_safe_direction() -> None:
    payload = _source_payload()
    result = decimal_parent_endpoint_recomposition(payload)
    gain_box = payload["validation"]["gain_box"]
    kappa_1_upper = Decimal(gain_box["kappa_1_upper"])
    kappa_3_upper = Decimal(gain_box["kappa_3_upper"])
    with localcontext() as context:
        context.prec = 100
        exact_spectral = Decimal(1) - Decimal("0.4") * (
            kappa_1_upper + Decimal(3) * kappa_3_upper
        )
        transverse = kappa_1_upper + Decimal(12) * kappa_3_upper
        beta = Decimal("0.2") * transverse
        voltage_decay = Decimal(2) - Decimal("0.2") * (
            transverse + Decimal(1)
        )
        exact_halanay = min(Decimal(1), voltage_decay) - beta
    assert Decimal(result.spectral_margin_lower) <= exact_spectral
    assert Decimal(result.halanay_margin_lower) <= exact_halanay
    assert exact_spectral - Decimal(result.spectral_margin_lower) < Decimal(
        "1e-90"
    )
    assert exact_halanay - Decimal(result.halanay_margin_lower) < Decimal(
        "1e-90"
    )
    assert Decimal(result.rate_residual_lower) > Decimal("0.074")
    with localcontext() as context:
        context.prec = 160
        exact_delay_nearest = Decimal(5) * Decimal(5).sqrt()
        exact_exponential_nearest = (
            Decimal("0.03") * exact_delay_nearest
        ).exp()
        exact_rate_residual_nearest = (
            min(Decimal(1), voltage_decay)
            - Decimal("0.03")
            - beta * exact_exponential_nearest
        )
    assert Decimal(result.physical_delay_upper) >= exact_delay_nearest
    assert Decimal(result.rate_exponential_upper) >= exact_exponential_nearest
    assert Decimal(result.rate_residual_lower) <= exact_rate_residual_nearest

    widened = deepcopy(payload)
    widened["validation"]["gain_box"]["kappa_3_upper"] = "0.251"
    widened_result = decimal_parent_endpoint_recomposition(widened)
    assert Decimal(widened_result.spectral_margin_lower) < Decimal(
        result.spectral_margin_lower
    )
    assert Decimal(widened_result.halanay_margin_lower) < Decimal(
        result.halanay_margin_lower
    )
    assert Decimal(widened_result.rate_residual_lower) < Decimal(
        result.rate_residual_lower
    )


def test_tracked_box_closes_spectrum_channels_projection_and_halanay() -> None:
    certificate = load_same_model_separator(SOURCE_RESULT)
    assert certificate.source_result_sha256 == TRACKED_PARAMETER_BOX_SHA256
    assert certificate.epsilon == "1/5"
    assert certificate.unfolding == "3/5"
    assert certificate.scaled_delays == ("4", "5")
    assert certificate.voltage_scaffold == "3"
    assert certificate.recovery_scaffold == "2"

    d_lower, d_upper = map(
        float, certificate.linearized_delayed_gain_interval
    )
    a_lower, a_upper = map(
        float, certificate.linearized_current_growth_interval
    )
    assert 0.189 < d_lower <= d_upper < 0.191
    assert 0.809 < a_lower <= a_upper < 0.811
    assert float(certificate.spectral_small_gain_margin_lower) > 0.619
    assert Decimal(certificate.spectral_small_gain_margin_lower) <= Decimal(
        certificate.decimal_recomposed_spectral_margin_lower
    )
    assert d_upper < a_lower
    assert certificate.one_simple_rhp_characteristic_root_validated
    assert certificate.no_imaginary_characteristic_roots_validated

    # The negative capture constant uses the exact secant coefficient 7,
    # whereas the variational Halanay coefficient uses the derivative
    # coefficient 12.  These are different estimates for different tasks.
    assert certificate.positive_cubic_secant_upper == "3"
    assert certificate.negative_cubic_secant_upper == "7"
    assert float(certificate.positive_channel_growth_lower) > 0.476
    assert float(certificate.negative_channel_growth_lower) > 0.276
    assert float(certificate.transverse_coefficient_upper) < 3.201
    assert certificate.positive_channel_capture_validated
    assert certificate.negative_channel_capture_validated

    assert float(certificate.reset_projection_lower) > 0.84
    assert certificate.reset_projection_transversality_validated
    assert float(certificate.halanay_local_decay_lower) > 0.999
    assert float(certificate.halanay_delayed_gain_upper) < 0.641
    assert float(certificate.halanay_margin_lower) > 0.359
    assert Decimal(certificate.halanay_margin_lower) <= Decimal(
        certificate.decimal_recomposed_halanay_margin_lower
    )
    assert certificate.halanay_rate_candidate == "0.03"
    assert float(certificate.halanay_rate_residual_lower) > 0.074
    assert Decimal(certificate.halanay_rate_residual_lower) <= Decimal(
        certificate.decimal_recomposed_halanay_rate_residual_lower
    )
    assert (
        certificate.arbitrary_two_module_sizes_linear_variational_transverse_decay_during_clamped_decision_validated
    )
    assert certificate.full_network_collective_projection_exact
    assert certificate.physical_collective_recovery_actuator_exact
    assert certificate.actuator_has_zero_transverse_projection_exact
    assert certificate.controlled_collective_recovery_leaf_invariant_exact


def test_claim_boundary_is_operational_not_unforced_or_general() -> None:
    certificate = load_same_model_separator(SOURCE_RESULT)
    assert certificate.same_synchronous_baseline_and_gain_box_validated
    assert certificate.full_network_d3_e2_instance_fixed_by_this_certificate
    assert not certificate.source_periodic_artifact_certifies_full_network_scaffolds
    assert certificate.controlled_operational_onset_validated
    assert certificate.reset_family_complete_history_threshold_validated
    assert (
        certificate.controlled_clamped_complete_history_stable_manifold_validated
    )
    assert not certificate.quantified_noisy_history_capture_validated
    assert not (
        certificate.nonlinear_transverse_synchronization_during_clamped_decision_validated
    )
    assert not certificate.periodic_full_network_transverse_stability_validated
    assert not certificate.unforced_complete_history_stable_manifold_validated
    assert not certificate.unforced_onset_validated
    assert not certificate.maximal_canard_onset_validated
    assert not certificate.periodic_orbit_attraction_validated
    assert not certificate.general_network_topology_validated
    assert not certificate.issue_15_closed


def test_tracked_result_hash_manifest_and_semantic_scope() -> None:
    payload = load_same_model_separator_result(
        SEPARATOR_RESULT,
        expected_sha256=EXPECTED_SEPARATOR_RESULT_SHA256,
    )
    provenance = payload["provenance"]
    generator = REPOSITORY / provenance["generator"]
    assert sha256(generator.read_bytes()).hexdigest() == provenance[
        "generator_sha256"
    ]
    for relative, digest in provenance["proof_source_manifest"].items():
        assert sha256((REPOSITORY / relative).read_bytes()).hexdigest() == digest

    scope = payload["scope"]
    assert scope["same_synchronous_baseline_and_gain_box"]
    assert scope["full_network_d3_e2_instance_fixed_by_separator_certificate"]
    assert scope["full_network_collective_clamp_exact"]
    assert not scope["source_periodic_artifact_certifies_full_network_scaffolds"]
    assert scope["controlled_operational_first_hit_onset"]
    assert scope["reset_family_complete_history_threshold"]
    assert scope["controlled_clamped_complete_history_stable_manifold"]
    assert scope[
        "arbitrary_two_module_sizes_linear_variational_transverse_decay_during_clamped_decision"
    ]
    for name in (
        "quantified_noisy_history_capture",
        "nonlinear_transverse_synchronization_during_clamped_decision",
        "periodic_full_network_transverse_stability",
        "unforced_complete_history_stable_manifold",
        "unforced_onset",
        "maximal_canard_onset",
        "periodic_orbit_attraction",
        "general_network_topology",
        "biological_pulse_or_quiet_basin_capture_beyond_channel_faces",
        "issue_15_closed",
    ):
        assert not scope[name]


def test_source_loader_refuses_forged_bytes(tmp_path: Path) -> None:
    forged = tmp_path / "forged-source.json"
    forged.write_bytes(SOURCE_RESULT.read_bytes() + b" ")
    with pytest.raises(ValueError, match="SHA-256 mismatch"):
        load_same_model_separator(forged)


def test_result_loader_refuses_forged_bytes(tmp_path: Path) -> None:
    forged = tmp_path / "forged-result.json"
    forged.write_bytes(SEPARATOR_RESULT.read_bytes() + b" ")
    with pytest.raises(ValueError, match="SHA-256 mismatch"):
        load_same_model_separator_result(
            forged,
            expected_sha256=EXPECTED_SEPARATOR_RESULT_SHA256,
        )


@pytest.mark.parametrize(
    ("section", "flag"),
    (
        ("validation", "d1_validated"),
        ("validation", "d3_validated"),
        ("validation", "d4_response_lower_bound_validated"),
        ("continuation", "parameter_box_orbit_validated"),
        ("extrema", "extrema_validated"),
        ("response", "response_box_validated"),
        ("scope", "d4_directed_response_lower_bound"),
    ),
)
def test_semantic_source_refuses_missing_positive_proof_flags(
    section: str, flag: str
) -> None:
    payload = deepcopy(_source_payload())
    if section in {"validation", "scope"}:
        payload[section][flag] = False
    else:
        payload["validation"][section][flag] = False
    with pytest.raises(ValueError, match="must be true"):
        _semantic_source(payload)


@pytest.mark.parametrize(
    ("section", "flag"),
    (
        ("scope", "issue_15_closed"),
        ("scope", "response_derivative_lipschitz"),
        ("response", "derivative_lipschitz_bound_supplied"),
    ),
)
def test_semantic_source_refuses_scope_promotion(
    section: str, flag: str
) -> None:
    payload = deepcopy(_source_payload())
    if section == "scope":
        payload[section][flag] = True
    else:
        payload["validation"][section][flag] = True
    with pytest.raises(ValueError, match="must be false"):
        _semantic_source(payload)


def test_semantic_source_refuses_wrong_model_coordinates() -> None:
    payload = deepcopy(_source_payload())
    payload["validation"]["response"]["control_order"] = [
        "kappa_3",
        "kappa_1",
    ]
    with pytest.raises(ValueError, match="control order"):
        _semantic_source(payload)


def test_semantic_source_refuses_nonpositive_gain_box() -> None:
    payload = deepcopy(_source_payload())
    gain_box = payload["validation"]["gain_box"]
    gain_box["kappa_3_lower"] = "-1"
    with pytest.raises(ValueError, match="positive gain intervals"):
        _semantic_source(payload)


def test_semantic_source_refuses_box_missing_declared_centered_box() -> None:
    payload = deepcopy(_source_payload())
    payload["validation"]["gain_box"]["kappa_1_lower"] = "0.2"
    with pytest.raises(ValueError, match="does not contain"):
        _semantic_source(payload)


@pytest.mark.parametrize(
    ("section", "flag"),
    (
        ("certificate", "controlled_operational_onset_validated"),
        ("certificate", "physical_collective_recovery_actuator_exact"),
        (
            "certificate",
            "controlled_collective_recovery_leaf_invariant_exact",
        ),
        ("scope", "controlled_operational_first_hit_onset"),
        (
            "scope",
            "arbitrary_two_module_sizes_linear_variational_transverse_decay_during_clamped_decision",
        ),
    ),
)
def test_result_semantics_refuse_missing_positive_flags(
    section: str, flag: str
) -> None:
    payload = deepcopy(_result_payload())
    payload[section][flag] = False
    with pytest.raises(ValueError, match="must be true"):
        validate_same_model_separator_result_payload(payload)


@pytest.mark.parametrize(
    ("section", "flag"),
    (
        ("certificate", "unforced_onset_validated"),
        ("certificate", "general_network_topology_validated"),
        (
            "certificate",
            "periodic_full_network_transverse_stability_validated",
        ),
        (
            "scope",
            "source_periodic_artifact_certifies_full_network_scaffolds",
        ),
        (
            "scope",
            "nonlinear_transverse_synchronization_during_clamped_decision",
        ),
        ("scope", "maximal_canard_onset"),
        ("scope", "periodic_orbit_attraction"),
        (
            "scope",
            "biological_pulse_or_quiet_basin_capture_beyond_channel_faces",
        ),
    ),
)
def test_result_semantics_refuse_scope_promotion(
    section: str, flag: str
) -> None:
    payload = deepcopy(_result_payload())
    payload[section][flag] = True
    with pytest.raises(ValueError, match="must be false"):
        validate_same_model_separator_result_payload(payload)


def test_result_semantics_refuse_attributing_d3_e2_to_parent_artifact() -> None:
    payload = deepcopy(_result_payload())
    payload["source_evidence"][
        "source_periodic_artifact_certifies_full_network_scaffolds"
    ] = True
    with pytest.raises(ValueError, match="must be false"):
        validate_same_model_separator_result_payload(payload)


def test_result_semantics_refuse_a_changed_full_network_instance() -> None:
    payload = deepcopy(_result_payload())
    payload["source_evidence"][
        "full_network_instance_fixed_by_separator_certificate"
    ]["voltage_scaffold"] = "4"
    with pytest.raises(ValueError, match="full-network instance"):
        validate_same_model_separator_result_payload(payload)


def test_result_semantics_refuse_an_uncontrolled_phase_space_label() -> None:
    payload = deepcopy(_result_payload())
    payload["source_evidence"][
        "controlled_complete_history_phase_space"
    ] = "unforced history space"
    with pytest.raises(ValueError, match="controlled complete-history"):
        validate_same_model_separator_result_payload(payload)
