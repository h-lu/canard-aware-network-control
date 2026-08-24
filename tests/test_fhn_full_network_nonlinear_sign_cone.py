"""Regression and refusal tests for the nonlinear full-network sign cones."""

from __future__ import annotations

from copy import deepcopy
from decimal import Decimal, localcontext
from hashlib import sha256
import json
from pathlib import Path

import pytest
import sympy as sp

from canard_control.fhn_full_network_nonlinear_sign_cone import (
    TRACKED_SEPARATOR_RESULT_SHA256,
    full_network_nonlinear_sign_cone_from_payload,
    full_network_sign_cone_algebra,
    load_full_network_nonlinear_sign_cone,
    load_full_network_nonlinear_sign_cone_result,
    validate_full_network_nonlinear_sign_cone_result_payload,
)


REPOSITORY = Path(__file__).resolve().parents[1]
SEPARATOR_RESULT = (
    REPOSITORY / "experiments/results/fhn_same_model_separator.json"
)
CONE_RESULT = (
    REPOSITORY
    / "experiments/results/fhn_full_network_nonlinear_sign_cone.json"
)
EXPECTED_CONE_RESULT_SHA256 = (
    "89c4ff362a8deb9ba722748015ec236f2f0365073e476c27da0b8c079fae6509"
)


def _separator_payload() -> dict:
    return json.loads(SEPARATOR_RESULT.read_text(encoding="utf-8"))


@pytest.mark.parametrize("module_sizes", ((1, 1), (2, 3), (4, 2)))
def test_exact_rank_one_average_and_recovery_identities(
    module_sizes: tuple[int, int],
) -> None:
    audit = full_network_sign_cone_algebra(*module_sizes)
    node_count = sum(module_sizes)
    assert audit.pi_sum_residual == 0
    assert audit.delay_sum_projection_residual == sp.zeros(node_count)
    assert audit.pi_same_delay_residual == sp.zeros(1, node_count)
    assert audit.pi_cross_delay_residual == sp.zeros(1, node_count)
    assert audit.same_delay_collective_residual == sp.zeros(node_count, 1)
    assert audit.cross_delay_collective_residual == sp.zeros(node_count, 1)
    assert audit.recovery_mean_residual == 0
    assert audit.recovery_deviation_residual == sp.zeros(node_count, 1)
    assert audit.positive_intrinsic_factor_residual == 0
    assert audit.negative_intrinsic_factor_residual == 0
    assert audit.boundary_cubic_factor_residual == 0
    assert audit.delay_layers_entrywise_nonnegative


def test_tracked_source_certifies_a_nonempty_nonlinear_cone() -> None:
    certificate = load_full_network_nonlinear_sign_cone(SEPARATOR_RESULT)
    assert certificate.separator_result_sha256 == (
        TRACKED_SEPARATOR_RESULT_SHA256
    )
    assert certificate.theorem_condition == "D*m>max(W0,epsilon/E)"
    assert Decimal(certificate.declared_voltage_sign_margin) == Decimal("0.04")
    assert Decimal(certificate.effective_recovery_bound) > Decimal("0.1")
    assert Decimal(certificate.effective_recovery_bound) < Decimal("0.101")
    assert Decimal(certificate.inward_boundary_margin_lower) > Decimal("0.019")
    assert Decimal(certificate.positive_release_deadline_upper) < Decimal("6.8")
    assert Decimal(certificate.negative_release_deadline_upper) < Decimal("11.7")
    assert (
        Decimal(certificate.positive_total_protocol_deadline_upper)
        < Decimal("18")
    )
    assert (
        Decimal(certificate.negative_total_protocol_deadline_upper)
        < Decimal("23")
    )
    assert Decimal(certificate.declared_excursion_voltage_sign_margin) == (
        Decimal("0.06")
    )
    assert Decimal(certificate.positive_excursion_face) == Decimal("1.5")
    assert Decimal(certificate.negative_excursion_face) == Decimal("-1.2")
    assert Decimal(certificate.positive_excursion_growth_lower) > Decimal(
        "0.059"
    )
    assert Decimal(certificate.negative_excursion_growth_lower) > Decimal(
        "0.077"
    )
    assert (
        Decimal(certificate.positive_excursion_inward_boundary_margin_lower)
        > Decimal("0.029")
    )
    assert (
        Decimal(certificate.negative_excursion_inward_boundary_margin_lower)
        > Decimal("0.059")
    )
    assert (
        Decimal(certificate.positive_excursion_release_deadline_upper)
        < Decimal("53.7")
    )
    assert (
        Decimal(certificate.negative_excursion_release_deadline_upper)
        < Decimal("38.5")
    )
    assert certificate.exact_pi_delay_layer_identities_validated
    assert certificate.exact_collective_recovery_deviation_equation_validated
    assert certificate.arbitrary_positive_module_sizes_formula_validated
    assert (
        certificate.positive_full_network_nonlinear_sign_cone_first_hit_validated
    )
    assert (
        certificate.negative_full_network_nonlinear_sign_cone_first_hit_validated
    )
    assert certificate.nodewise_detector_first_hit_validated
    assert certificate.positive_finite_controlled_suprathreshold_excursion_validated
    assert certificate.negative_finite_controlled_excursion_validated
    assert certificate.latched_nodewise_detector_then_excursion_validated
    assert not certificate.same_detector_node_reaches_excursion_face_validated
    assert not certificate.detector_face_no_return_validated
    assert not certificate.nonlinear_synchronization_validated
    assert not certificate.noise_across_voltage_sign_boundary_validated
    assert not certificate.bounded_additive_hold_or_hardware_validated
    assert not certificate.beyond_face_biological_basin_validated
    assert not certificate.general_network_topology_validated


def test_public_boundary_and_deadline_constants_compose_safely() -> None:
    certificate = load_full_network_nonlinear_sign_cone(SEPARATOR_RESULT)
    with localcontext() as context:
        context.prec = 120
        scaffold = Decimal(certificate.voltage_scaffold)
        margin = Decimal(certificate.declared_voltage_sign_margin)
        effective = Decimal(certificate.effective_recovery_bound)
        inward = Decimal(certificate.inward_boundary_margin_lower)
        assert inward <= scaffold * margin - effective
        positive_growth = Decimal(certificate.positive_mean_growth_lower)
        negative_growth = Decimal(certificate.negative_mean_growth_lower)
        positive_deadline = Decimal(
            certificate.positive_release_deadline_upper
        )
        negative_deadline = Decimal(
            certificate.negative_release_deadline_upper
        )
        logarithm = (Decimal(1) / margin).ln()
        assert positive_deadline >= logarithm / positive_growth
        assert negative_deadline >= logarithm / negative_growth
        hold = Decimal(certificate.physical_hold_duration_upper)
        assert Decimal(
            certificate.positive_total_protocol_deadline_upper
        ) >= hold + positive_deadline
        assert Decimal(
            certificate.negative_total_protocol_deadline_upper
        ) >= hold + negative_deadline

        excursion_margin = Decimal(
            certificate.declared_excursion_voltage_sign_margin
        )
        positive_face = Decimal(certificate.positive_excursion_face)
        negative_magnitude = -Decimal(certificate.negative_excursion_face)
        positive_excursion_growth = Decimal(
            certificate.positive_excursion_growth_lower
        )
        negative_excursion_growth = Decimal(
            certificate.negative_excursion_growth_lower
        )
        positive_excursion_deadline = Decimal(
            certificate.positive_excursion_release_deadline_upper
        )
        negative_excursion_deadline = Decimal(
            certificate.negative_excursion_release_deadline_upper
        )
        assert positive_excursion_deadline >= (
            positive_face / excursion_margin
        ).ln() / positive_excursion_growth
        assert negative_excursion_deadline >= (
            negative_magnitude / excursion_margin
        ).ln() / negative_excursion_growth
        assert Decimal(
            certificate.positive_excursion_total_protocol_deadline_upper
        ) >= hold + positive_excursion_deadline
        assert Decimal(
            certificate.negative_excursion_total_protocol_deadline_upper
        ) >= hold + negative_excursion_deadline


@pytest.mark.parametrize(
    ("voltage_margin", "recovery_bound", "message"),
    (
        ("0.03", "0.1", "D\\*m"),
        ("0.04", "0.2", "D\\*m"),
        ("0", "0.1", "strictly between"),
        ("1", "0.1", "strictly between"),
        ("0.04", "-0.1", "nonnegative"),
    ),
)
def test_unsafe_or_invalid_cones_are_refused(
    voltage_margin: str,
    recovery_bound: str,
    message: str,
) -> None:
    with pytest.raises(ValueError, match=message):
        full_network_nonlinear_sign_cone_from_payload(
            _separator_payload(),
            separator_result_sha256=TRACKED_SEPARATOR_RESULT_SHA256,
            voltage_sign_margin=voltage_margin,
            recovery_history_bound=recovery_bound,
        )


def test_source_loader_refuses_forged_separator_bytes(tmp_path: Path) -> None:
    forged = tmp_path / "separator.json"
    forged.write_bytes(SEPARATOR_RESULT.read_bytes() + b" ")
    with pytest.raises(ValueError, match="separator result SHA-256"):
        load_full_network_nonlinear_sign_cone(forged)


def test_unsafe_excursion_cone_is_refused() -> None:
    with pytest.raises(ValueError, match="H_plus"):
        full_network_nonlinear_sign_cone_from_payload(
            _separator_payload(),
            separator_result_sha256=TRACKED_SEPARATOR_RESULT_SHA256,
            excursion_voltage_sign_margin="0.04",
        )


def test_generated_result_is_hash_and_manifest_bound() -> None:
    payload = load_full_network_nonlinear_sign_cone_result(
        CONE_RESULT,
        expected_sha256=EXPECTED_CONE_RESULT_SHA256,
    )
    provenance = payload["provenance"]
    generator = REPOSITORY / provenance["generator"]
    assert sha256(generator.read_bytes()).hexdigest() == provenance[
        "generator_sha256"
    ]
    for relative, digest in provenance["proof_source_manifest"].items():
        assert sha256((REPOSITORY / relative).read_bytes()).hexdigest() == digest
    source = payload["source_evidence"]
    assert source["separator_result_sha256"] == sha256(
        SEPARATOR_RESULT.read_bytes()
    ).hexdigest()
    for relative, digest in source[
        "separator_proof_source_manifest"
    ].items():
        assert sha256((REPOSITORY / relative).read_bytes()).hexdigest() == digest


def test_generated_result_loader_refuses_forged_bytes(tmp_path: Path) -> None:
    forged = tmp_path / "cone.json"
    forged.write_bytes(CONE_RESULT.read_bytes() + b" ")
    with pytest.raises(ValueError, match="full-network sign-cone result"):
        load_full_network_nonlinear_sign_cone_result(
            forged,
            expected_sha256=EXPECTED_CONE_RESULT_SHA256,
        )


def test_result_semantics_refuse_missing_or_promoted_claims() -> None:
    payload = json.loads(CONE_RESULT.read_text(encoding="utf-8"))
    missing = deepcopy(payload)
    missing["scope"][
        "positive_full_network_nonlinear_sign_cone_first_hit"
    ] = False
    with pytest.raises(ValueError, match="must be true"):
        validate_full_network_nonlinear_sign_cone_result_payload(missing)
    promoted = deepcopy(payload)
    promoted["scope"]["beyond_face_biological_basin"] = True
    with pytest.raises(ValueError, match="must be false"):
        validate_full_network_nonlinear_sign_cone_result_payload(promoted)
    same_node = deepcopy(payload)
    same_node["scope"]["same_detector_node_reaches_excursion_face"] = True
    with pytest.raises(ValueError, match="must be false"):
        validate_full_network_nonlinear_sign_cone_result_payload(same_node)
    no_return = deepcopy(payload)
    no_return["scope"]["detector_face_no_return"] = True
    with pytest.raises(ValueError, match="must be false"):
        validate_full_network_nonlinear_sign_cone_result_payload(no_return)
