"""Regression and hostile refusal tests for the staged three-output theorem."""

from __future__ import annotations

from copy import deepcopy
from decimal import Decimal, localcontext
from hashlib import sha256
import json
from pathlib import Path

import numpy as np
import pytest

from canard_control.fhn_same_model_three_output import (
    FULL_NETWORK_INSTANCE_ID,
    INPUT_ORDER,
    OUTPUT_ORDER,
    SYNCHRONOUS_MODEL_ID,
    TRACKED_PARAMETER_BOX_SHA256,
    TRACKED_SEPARATOR_SHA256,
    TRACKED_TARGET_BALL_SHA256,
    decimal_three_output_composition,
    load_same_model_three_output,
    load_same_model_three_output_result,
    same_model_three_output_from_payloads,
    validate_same_model_three_output_result_payload,
)


REPOSITORY = Path(__file__).resolve().parents[1]
TARGET_RESULT = REPOSITORY / "experiments/results/fhn_response_target_ball.json"
SEPARATOR_RESULT = REPOSITORY / "experiments/results/fhn_same_model_separator.json"
THREE_OUTPUT_RESULT = (
    REPOSITORY / "experiments/results/fhn_same_model_three_output.json"
)
EXPECTED_THREE_OUTPUT_RESULT_SHA256 = (
    "afc03431d61d86c6bda8b56a73bdeea76b357e9a31a4a843d9f55cebbf666532"
)


def _target_payload() -> dict:
    return json.loads(TARGET_RESULT.read_text(encoding="utf-8"))


def _separator_payload() -> dict:
    return json.loads(SEPARATOR_RESULT.read_text(encoding="utf-8"))


def _result_payload() -> dict:
    return json.loads(THREE_OUTPUT_RESULT.read_text(encoding="utf-8"))


def _semantic_sources(target: dict, separator: dict):
    return same_model_three_output_from_payloads(
        target,
        separator,
        target_result_sha256=TRACKED_TARGET_BALL_SHA256,
        separator_result_sha256=TRACKED_SEPARATOR_SHA256,
    )


def test_tracked_sources_give_the_exact_block_three_output_theorem() -> None:
    certificate = load_same_model_three_output(
        TARGET_RESULT,
        SEPARATOR_RESULT,
        repository=REPOSITORY,
    )
    assert certificate.target_ball_result_sha256 == TRACKED_TARGET_BALL_SHA256
    assert certificate.separator_result_sha256 == TRACKED_SEPARATOR_SHA256
    assert (
        certificate.shared_parameter_box_result_sha256
        == TRACKED_PARAMETER_BOX_SHA256
    )
    assert certificate.source_synchronous_model_id == SYNCHRONOUS_MODEL_ID
    assert certificate.certified_full_network_instance_id == (
        FULL_NETWORK_INSTANCE_ID
    )
    assert certificate.input_order == INPUT_ORDER
    assert certificate.output_order == OUTPUT_ORDER
    assert certificate.map_definition == "Q_op(kappa_1,kappa_3,r)=(F,R_h,-r)"
    assert certificate.input_center == ("0.2", "0.25", "0")
    assert certificate.exact_input_ball_radius == "1e-12"

    matrix = np.asarray(certificate.midpoint_matrix_3d_binary64)
    assert np.array_equal(matrix[:2, :2], np.asarray(
        [
            [0.03669982799550202, 0.13633946068777764],
            [-3.645615771771411, -6.136337974459385],
        ]
    ))
    assert np.array_equal(matrix[:2, 2], np.zeros(2))
    assert np.array_equal(matrix[2, :2], np.zeros(2))
    assert matrix[2, 2] == -1.0
    assert np.linalg.svd(matrix, compute_uv=False)[-1] > float(
        certificate.midpoint_singular_value_lower
    )

    assert float(certificate.midpoint_singular_value_lower) > 0.038
    assert float(certificate.derivative_defect_frobenius_upper) < 0.022
    assert float(certificate.response_margin_lower) > 0.0162
    assert float(certificate.fixed_inverse_contraction_upper) < 0.575
    assert float(certificate.fixed_inverse_contraction_margin_lower) > 0.425
    assert float(certificate.certified_output_ball_radius_lower) > 1.62e-14
    assert certificate.target_source_manifest_validated
    assert certificate.separator_source_manifest_validated
    assert certificate.shared_gain_box_and_model_validated
    assert certificate.exact_block_diagonal_reset_column_validated
    assert certificate.midpoint_singular_value_block_transfer_validated
    assert certificate.derivative_defect_block_transfer_validated
    assert certificate.three_dimensional_input_ball_contained
    assert certificate.unique_input_for_each_certified_target_validated
    assert (
        certificate.frequency_squared_range_operational_margin_target_ball_validated
    )
    assert certificate.same_baseline_staged_protocol_validated


def test_public_decimal_composition_is_conservative_in_every_direction() -> None:
    target = _target_payload()["target_ball"]
    composition = decimal_three_output_composition(target)
    with localcontext() as context:
        context.prec = 160
        s0 = Decimal(composition.parent_s0_lower)
        defect = Decimal(composition.parent_derivative_defect_upper)
        parent_input = Decimal(
            composition.parent_certified_input_radius_lower
        )
        direct_margin = s0 - defect
        direct_contraction = defect / s0
        selected_contraction_margin = Decimal(1) - Decimal(
            composition.selected_contraction_upper
        )
        selected_output_product = Decimal(
            composition.selected_margin_lower
        ) * parent_input
    assert Decimal(composition.recomposed_margin_lower) <= direct_margin
    assert Decimal(composition.recomposed_contraction_upper) >= (
        direct_contraction
    )
    assert Decimal(composition.selected_margin_lower) <= Decimal(
        composition.recomposed_margin_lower
    )
    assert Decimal(composition.selected_contraction_upper) >= Decimal(
        composition.recomposed_contraction_upper
    )
    assert Decimal(composition.selected_contraction_margin_lower) <= (
        selected_contraction_margin
    )
    assert Decimal(composition.recomposed_output_radius_lower) <= (
        selected_output_product
    )
    assert Decimal(composition.selected_output_radius_lower) <= Decimal(
        composition.recomposed_output_radius_lower
    )
    assert Decimal(composition.selected_output_radius_lower) == Decimal(
        composition.parent_output_radius_lower
    )


def test_decimal_composition_refuses_an_overstated_parent_radius() -> None:
    target = deepcopy(_target_payload()["target_ball"])
    target["certified_output_ball_radius_lower"] = "2e-14"
    with pytest.raises(ValueError, match="exceeds its public recomposition"):
        decimal_three_output_composition(target)


def test_decimal_composition_refuses_an_understated_parent_contraction() -> None:
    target = deepcopy(_target_payload()["target_ball"])
    target["fixed_inverse_contraction_upper"] = "0.5"
    with pytest.raises(ValueError, match="understated"):
        decimal_three_output_composition(target)


def test_claim_boundary_is_exactly_operational_and_staged() -> None:
    certificate = load_same_model_three_output(
        TARGET_RESULT,
        SEPARATOR_RESULT,
        repository=REPOSITORY,
    )
    assert certificate.frequency_squared_range_operational_margin_target_ball_validated
    assert certificate.same_baseline_staged_protocol_validated
    assert not certificate.unsquared_amplitude_validated
    assert not certificate.physical_finite_pulse_validated
    assert not certificate.biological_basin_beyond_channel_faces_validated
    assert not certificate.noise_hardware_robustness_validated
    assert not certificate.unforced_onset_validated
    assert not certificate.maximal_canard_onset_validated
    assert not certificate.periodic_attraction_validated
    assert not certificate.general_topology_validated
    assert not certificate.issue_15_closed


def test_result_artifact_hash_manifests_and_scope() -> None:
    payload = load_same_model_three_output_result(
        THREE_OUTPUT_RESULT,
        expected_sha256=EXPECTED_THREE_OUTPUT_RESULT_SHA256,
    )
    provenance = payload["provenance"]
    generator = REPOSITORY / provenance["generator"]
    assert sha256(generator.read_bytes()).hexdigest() == provenance[
        "generator_sha256"
    ]
    for relative, digest in provenance["proof_source_manifest"].items():
        assert sha256((REPOSITORY / relative).read_bytes()).hexdigest() == digest
    for name, source_path in (
        ("target_parent_provenance", TARGET_RESULT),
        ("separator_parent_provenance", SEPARATOR_RESULT),
    ):
        parent = payload["source_evidence"][name]
        assert sha256(source_path.read_bytes()).hexdigest() == parent[
            "result_sha256"
        ]
        parent_generator = REPOSITORY / parent["generator"]
        assert sha256(parent_generator.read_bytes()).hexdigest() == parent[
            "generator_sha256"
        ]
        for relative, digest in parent["proof_source_manifest"].items():
            assert sha256((REPOSITORY / relative).read_bytes()).hexdigest() == digest

    scope = payload["scope"]
    assert set(name for name, value in scope.items() if value) == {
        "frequency_squared_range_operational_first_hit_margin_target_ball",
        "same_baseline_staged_protocol",
    }


def test_loader_refuses_a_forged_target_artifact(tmp_path: Path) -> None:
    forged = tmp_path / "target.json"
    forged.write_bytes(TARGET_RESULT.read_bytes() + b" ")
    with pytest.raises(ValueError, match="target-ball result SHA-256 mismatch"):
        load_same_model_three_output(
            forged,
            SEPARATOR_RESULT,
            repository=REPOSITORY,
        )


def test_loader_refuses_a_forged_separator_artifact(tmp_path: Path) -> None:
    forged = tmp_path / "separator.json"
    forged.write_bytes(SEPARATOR_RESULT.read_bytes() + b" ")
    with pytest.raises(ValueError, match="separator result SHA-256 mismatch"):
        load_same_model_three_output(
            TARGET_RESULT,
            forged,
            repository=REPOSITORY,
        )


@pytest.mark.parametrize(
    "flag",
    (
        "base_frequency_squared_range_target_ball_validated",
        "centered_input_ball_contained_in_gain_box",
        "fixed_inverse_contraction_validated",
    ),
)
def test_semantic_composer_refuses_missing_target_flags(flag: str) -> None:
    target = deepcopy(_target_payload())
    target["target_ball"][flag] = False
    with pytest.raises(ValueError, match="must be true"):
        _semantic_sources(target, _separator_payload())


@pytest.mark.parametrize(
    "flag",
    (
        "physical_pulse_onset",
        "attraction",
        "same_model_periodic_separator_bridge",
        "issue_15_closed",
    ),
)
def test_semantic_composer_refuses_promoted_target_scope(flag: str) -> None:
    target = deepcopy(_target_payload())
    target["scope"][flag] = True
    with pytest.raises(ValueError, match="must be false"):
        _semantic_sources(target, _separator_payload())


@pytest.mark.parametrize(
    "flag",
    (
        "controlled_operational_onset_validated",
        "reset_family_complete_history_threshold_validated",
        "same_synchronous_baseline_and_gain_box_validated",
        "physical_collective_recovery_actuator_exact",
    ),
)
def test_semantic_composer_refuses_missing_separator_flags(flag: str) -> None:
    separator = deepcopy(_separator_payload())
    separator["certificate"][flag] = False
    with pytest.raises(ValueError, match="must be true"):
        _semantic_sources(_target_payload(), separator)


@pytest.mark.parametrize(
    "flag",
    (
        "unforced_onset",
        "maximal_canard_onset",
        "periodic_orbit_attraction",
        "general_network_topology",
        "biological_pulse_or_quiet_basin_capture_beyond_channel_faces",
    ),
)
def test_semantic_composer_refuses_promoted_separator_scope(flag: str) -> None:
    separator = deepcopy(_separator_payload())
    separator["scope"][flag] = True
    with pytest.raises(ValueError, match="must be false"):
        _semantic_sources(_target_payload(), separator)


def test_semantic_composer_refuses_different_parameter_boxes() -> None:
    separator = deepcopy(_separator_payload())
    separator["source_evidence"]["parameter_box_result_sha256"] = "0" * 64
    with pytest.raises(ValueError, match="different parameter box"):
        _semantic_sources(_target_payload(), separator)


def test_semantic_composer_refuses_different_models() -> None:
    separator = deepcopy(_separator_payload())
    separator["certificate"]["source_synchronous_model_id"] = "other-model"
    with pytest.raises(ValueError, match="different synchronous model"):
        _semantic_sources(_target_payload(), separator)


def test_semantic_composer_refuses_different_gain_boxes() -> None:
    separator = deepcopy(_separator_payload())
    separator["certificate"]["gain_half_width"] = "2e-12"
    with pytest.raises(ValueError, match="different gain half-width"):
        _semantic_sources(_target_payload(), separator)


def test_semantic_composer_refuses_a_different_gain_center() -> None:
    target = deepcopy(_target_payload())
    target["target_ball"]["parameter_center"] = ["0.21", "0.25"]
    with pytest.raises(ValueError, match="different gain center"):
        _semantic_sources(target, _separator_payload())


def test_semantic_composer_refuses_an_interval_missing_the_gain_box() -> None:
    separator = deepcopy(_separator_payload())
    separator["certificate"]["kappa_1_interval"][0] = "0.2"
    with pytest.raises(ValueError, match="gain boxes disagree"):
        _semantic_sources(_target_payload(), separator)


def test_semantic_composer_refuses_wrong_source_digests() -> None:
    with pytest.raises(ValueError, match="target-ball result SHA-256"):
        same_model_three_output_from_payloads(
            _target_payload(),
            _separator_payload(),
            target_result_sha256="0" * 64,
            separator_result_sha256=TRACKED_SEPARATOR_SHA256,
        )


@pytest.mark.parametrize(
    ("section", "flag"),
    (
        (
            "certificate",
            "frequency_squared_range_operational_margin_target_ball_validated",
        ),
        ("certificate", "exact_block_diagonal_reset_column_validated"),
        (
            "scope",
            "frequency_squared_range_operational_first_hit_margin_target_ball",
        ),
        ("scope", "same_baseline_staged_protocol"),
    ),
)
def test_result_semantics_refuse_missing_positive_flags(
    section: str, flag: str
) -> None:
    payload = deepcopy(_result_payload())
    payload[section][flag] = False
    with pytest.raises(ValueError, match="must be true"):
        validate_same_model_three_output_result_payload(payload)


@pytest.mark.parametrize(
    "flag",
    (
        "unsquared_amplitude",
        "physical_finite_pulse",
        "biological_basin_beyond_channel_faces",
        "noise_hardware_robustness",
        "unforced_onset",
        "maximal_canard_onset",
        "periodic_attraction",
        "general_topology",
        "issue_15_closed",
    ),
)
def test_result_semantics_refuse_scope_promotion(flag: str) -> None:
    payload = deepcopy(_result_payload())
    payload["scope"][flag] = True
    with pytest.raises(ValueError, match="must be false"):
        validate_same_model_three_output_result_payload(payload)


def test_result_semantics_refuse_certificate_promotion() -> None:
    payload = deepcopy(_result_payload())
    payload["certificate"]["physical_finite_pulse_validated"] = True
    with pytest.raises(ValueError, match="must be false"):
        validate_same_model_three_output_result_payload(payload)


def test_result_semantics_refuse_an_extra_true_scope() -> None:
    payload = deepcopy(_result_payload())
    payload["scope"]["physical_onset_alias"] = True
    with pytest.raises(ValueError, match="scope keys"):
        validate_same_model_three_output_result_payload(payload)


def test_result_semantics_refuse_wrong_map_order() -> None:
    payload = deepcopy(_result_payload())
    payload["certificate"]["input_order"] = ["r", "kappa_1", "kappa_3"]
    with pytest.raises(ValueError, match="input order"):
        validate_same_model_three_output_result_payload(payload)


def test_result_loader_refuses_forged_bytes(tmp_path: Path) -> None:
    forged = tmp_path / "three-output.json"
    forged.write_bytes(THREE_OUTPUT_RESULT.read_bytes() + b" ")
    with pytest.raises(ValueError, match="three-output result SHA-256 mismatch"):
        load_same_model_three_output_result(
            forged,
            expected_sha256=EXPECTED_THREE_OUTPUT_RESULT_SHA256,
        )
