"""Regression and refusal tests for periodic transverse Halanay decay."""

from __future__ import annotations

from copy import deepcopy
from decimal import Decimal, localcontext
from hashlib import sha256
import json
from pathlib import Path

import pytest
import sympy as sp

from canard_control.fhn_periodic_transverse_halanay import (
    TRACKED_BLOCH_RESULT_SHA256,
    TRACKED_PARAMETER_BOX_SHA256,
    load_periodic_transverse_halanay,
    load_periodic_transverse_result,
    periodic_transverse_algebra,
    periodic_transverse_network_algebra,
    periodic_transverse_halanay_from_payloads,
    validate_periodic_transverse_result_payload,
)


REPOSITORY = Path(__file__).resolve().parents[1]
PARAMETER_RESULT = (
    REPOSITORY / "experiments/results/fhn_periodic_parameter_box.json"
)
BLOCH_RESULT = (
    REPOSITORY / "experiments/results/fhn_bloch_outer_validation.json"
)
TRANSVERSE_RESULT = (
    REPOSITORY / "experiments/results/fhn_periodic_transverse_halanay.json"
)
EXPECTED_TRANSVERSE_RESULT_SHA256 = (
    "ec4b3204695bf40d4309681b0f57d93e3e1e524ca3680cdce316aaee8ad015fb"
)


def _parameter_payload() -> dict:
    return json.loads(PARAMETER_RESULT.read_text(encoding="utf-8"))


def _bloch_payload() -> dict:
    return json.loads(BLOCH_RESULT.read_text(encoding="utf-8"))


def _semantic(parameter: dict, bloch: dict):
    return periodic_transverse_halanay_from_payloads(
        parameter,
        bloch,
        parameter_box_result_sha256=TRACKED_PARAMETER_BOX_SHA256,
        bloch_result_sha256=TRACKED_BLOCH_RESULT_SHA256,
    )


def test_completed_square_and_delay_mode_algebra_are_exact() -> None:
    algebra = periodic_transverse_algebra()
    assert algebra.completed_square_residual == 0
    assert algebra.same_delay_collective_residual == sp.zeros(2, 1)
    assert algebra.same_delay_difference_residual == sp.zeros(2, 1)
    assert algebra.cross_delay_collective_residual == sp.zeros(2, 1)
    assert algebra.cross_delay_difference_residual == sp.zeros(2, 1)


@pytest.mark.parametrize("module_sizes", ((1, 1), (2, 3), (4, 2)))
def test_exact_full_node_delay_lift_and_scaffolds(
    module_sizes: tuple[int, int],
) -> None:
    audit = periodic_transverse_network_algebra(*module_sizes)
    node_count = sum(module_sizes)
    within_count = node_count - 2
    assert audit.delay_sum_projection_residual == sp.zeros(node_count)
    assert audit.modal_rank == node_count
    assert audit.collective_same_delay_residual == sp.zeros(node_count, 1)
    assert audit.collective_cross_delay_residual == sp.zeros(node_count, 1)
    assert audit.difference_same_delay_residual == sp.zeros(node_count, 1)
    assert audit.difference_cross_delay_residual == sp.zeros(node_count, 1)
    assert audit.within_same_delay_residual == sp.zeros(
        node_count, within_count
    )
    assert audit.within_cross_delay_residual == sp.zeros(
        node_count, within_count
    )
    assert audit.collective_scaffold_residual == sp.zeros(node_count, 1)
    assert audit.transverse_voltage_scaffold_residual == sp.zeros(
        node_count, node_count - 1
    )
    assert audit.transverse_recovery_scaffold_residual == sp.zeros(
        node_count, node_count - 1
    )
    assert audit.reference_projection_residual == sp.zeros(node_count)
    assert audit.reference_collective_residual == sp.zeros(node_count, 1)
    assert audit.reference_difference_residual == sp.zeros(node_count, 1)


def test_tracked_periodic_branch_has_size_uniform_transverse_decay() -> None:
    certificate = load_periodic_transverse_halanay(
        PARAMETER_RESULT, BLOCH_RESULT
    )
    assert certificate.parameter_box_result_sha256 == (
        TRACKED_PARAMETER_BOX_SHA256
    )
    assert certificate.bloch_result_sha256 == TRACKED_BLOCH_RESULT_SHA256
    assert certificate.voltage_scaffold == "3"
    assert certificate.recovery_scaffold == "2"
    assert certificate.max_norm_weight == "1"
    assert float(certificate.current_coefficient_global_maximum_upper) < 0.83
    assert float(certificate.delayed_each_wiener_norm_upper) < 0.457
    assert float(certificate.delayed_total_gain_upper) < 0.913
    assert float(certificate.voltage_local_decay_lower) > 1.17
    assert float(certificate.recovery_local_decay_lower) > 1.79
    assert float(certificate.halanay_local_decay_lower) > 1.17
    assert float(certificate.halanay_margin_lower) > 0.257
    assert certificate.halanay_rate_candidate == "0.02"
    assert float(certificate.halanay_rate_residual_lower) > 0.008
    assert certificate.exact_rank_one_modal_decomposition_validated
    assert certificate.representative_full_node_delay_layer_audits_validated
    assert certificate.within_module_delay_annihilation_validated
    assert certificate.instantaneous_scaffold_modal_action_validated
    assert certificate.full_node_audit_module_sizes == (
        (1, 1),
        (2, 3),
        (4, 2),
    )
    assert not certificate.arbitrary_size_quantifier_from_enumeration
    assert certificate.arbitrary_positive_module_sizes_formulaic_theorem
    assert certificate.periodic_transverse_variational_decay_validated
    assert certificate.full_network_orbital_hyperbolicity_validated
    assert not certificate.synchronous_attraction_validated
    assert not certificate.full_network_attraction_validated
    assert not certificate.nonlinear_synchronization_validated
    assert not certificate.general_network_topology_validated


def test_public_decimal_constants_compose_in_the_safe_direction() -> None:
    certificate = load_periodic_transverse_halanay(
        PARAMETER_RESULT, BLOCH_RESULT
    )
    with localcontext() as context:
        context.prec = 120
        current = Decimal(
            certificate.current_coefficient_global_maximum_upper
        )
        each = Decimal(certificate.delayed_each_wiener_norm_upper)
        delayed = Decimal(certificate.delayed_total_gain_upper)
        voltage = Decimal(certificate.voltage_local_decay_lower)
        recovery = Decimal(certificate.recovery_local_decay_lower)
        local = Decimal(certificate.halanay_local_decay_lower)
        margin = Decimal(certificate.halanay_margin_lower)
        rate = Decimal(certificate.halanay_rate_candidate)
        exponential = Decimal(certificate.halanay_rate_exponential_upper)
        residual = Decimal(certificate.halanay_rate_residual_lower)
        assert voltage <= Decimal(3) - current - Decimal(1)
        assert recovery <= Decimal(2) - Decimal("0.2")
        assert local <= min(voltage, recovery)
        assert delayed >= Decimal(2) * each
        assert margin <= local - delayed
        assert residual <= local - rate - delayed * exponential


def test_generated_result_is_hash_source_and_scope_bound() -> None:
    payload = load_periodic_transverse_result(
        TRANSVERSE_RESULT,
        expected_sha256=EXPECTED_TRANSVERSE_RESULT_SHA256,
    )
    provenance = payload["provenance"]
    generator = REPOSITORY / provenance["generator"]
    assert sha256(generator.read_bytes()).hexdigest() == provenance[
        "generator_sha256"
    ]
    for relative, digest in provenance["proof_source_manifest"].items():
        assert sha256((REPOSITORY / relative).read_bytes()).hexdigest() == digest
    scope = payload["scope"]
    assert scope["periodic_transverse_variational_decay"]
    assert scope["full_network_orbital_hyperbolicity"]
    assert scope[
        "arbitrary_positive_module_sizes_for_fixed_rank_one_topology"
    ]
    for name in (
        "synchronous_attraction",
        "full_network_attraction",
        "nonlinear_synchronization",
        "general_network_topology",
        "physical_pulse_onset",
        "issue_15_closed",
    ):
        assert not scope[name]


def test_source_loaders_refuse_forged_bytes(tmp_path: Path) -> None:
    forged_parameter = tmp_path / "parameter.json"
    forged_parameter.write_bytes(PARAMETER_RESULT.read_bytes() + b" ")
    with pytest.raises(ValueError, match="parameter-box result SHA-256"):
        load_periodic_transverse_halanay(forged_parameter, BLOCH_RESULT)
    forged_bloch = tmp_path / "bloch.json"
    forged_bloch.write_bytes(BLOCH_RESULT.read_bytes() + b" ")
    with pytest.raises(ValueError, match="Bloch result SHA-256"):
        load_periodic_transverse_halanay(PARAMETER_RESULT, forged_bloch)


def test_generated_result_loader_refuses_forged_bytes(tmp_path: Path) -> None:
    forged = tmp_path / "transverse.json"
    forged.write_bytes(TRANSVERSE_RESULT.read_bytes() + b" ")
    with pytest.raises(ValueError, match="periodic transverse result SHA-256"):
        load_periodic_transverse_result(
            forged, expected_sha256=EXPECTED_TRANSVERSE_RESULT_SHA256
        )


@pytest.mark.parametrize(
    ("section", "flag"),
    (
        ("validation", "d1_validated"),
        ("continuation", "parameter_box_orbit_validated"),
        ("source", "periodic_branch_validated"),
        ("scope", "synchronous_orbital_hyperbolicity"),
        ("local", "regularity_bridge_to_history_monodromy"),
        ("local", "monodromy_compact"),
    ),
)
def test_semantic_source_refuses_missing_positive_evidence(
    section: str, flag: str
) -> None:
    parameter = _parameter_payload()
    bloch = _bloch_payload()
    if section == "validation":
        parameter["validation"][flag] = False
    elif section == "continuation":
        parameter["validation"]["continuation"][flag] = False
    else:
        key = {
            "source": "source_evidence",
            "scope": "scope",
            "local": "local_transfer",
        }[section]
        bloch[key][flag] = False
    with pytest.raises(ValueError, match="must be true"):
        _semantic(parameter, bloch)


@pytest.mark.parametrize(
    ("section", "flag"),
    (
        ("scope", "attraction"),
        ("scope", "full_network_transverse_stability"),
    ),
)
def test_semantic_source_refuses_historical_scope_promotion(
    section: str, flag: str
) -> None:
    parameter = _parameter_payload()
    bloch = _bloch_payload()
    bloch[section][flag] = True
    with pytest.raises(ValueError, match="must be false"):
        _semantic(parameter, bloch)


def test_semantic_source_refuses_wrong_norm_or_nonpositive_margin() -> None:
    parameter = _parameter_payload()
    bloch = _bloch_payload()
    bloch["local_transfer"]["norm_id"] = "point-sampled-sup-norm"
    with pytest.raises(ValueError, match="coefficient norm"):
        _semantic(parameter, bloch)

    bloch = _bloch_payload()
    bloch["local_transfer"][
        "delayed_coefficient_uniform_norm_upper"
    ] = "2"
    with pytest.raises(ValueError, match="margin is nonpositive"):
        _semantic(parameter, bloch)


def test_result_semantics_refuse_missing_or_promoted_claims() -> None:
    payload = json.loads(TRANSVERSE_RESULT.read_text(encoding="utf-8"))
    missing = deepcopy(payload)
    missing["scope"]["full_network_orbital_hyperbolicity"] = False
    with pytest.raises(ValueError, match="must be true"):
        validate_periodic_transverse_result_payload(missing)
    promoted = deepcopy(payload)
    promoted["scope"]["full_network_attraction"] = True
    with pytest.raises(ValueError, match="must be false"):
        validate_periodic_transverse_result_payload(promoted)
