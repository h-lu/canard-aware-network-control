"""Same-model three-output transfer to unsquared amplitude and safety.

The parent three-output theorem covers a Euclidean ball for

    Q_R(kappa_1,kappa_3,r) = (F, R_h, -r),  R_h=A**2.

This module transfers that *three-dimensional* ball to

    Q_A(kappa_1,kappa_3,r) = (F, A, -r)

through the inverse coordinate change

    (dF,dA,dS) -> (dF, 2*A_c*dA+dA**2, dS).

The reset column is an exact translation.  The theorem can therefore be
recentered at r0=+1/2 and r0=-1/2 without changing either radius.  These are
positive-face and negative-face operational charts; they are not assertions
about biological pulse or quiet basins.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Context, Decimal, InvalidOperation, ROUND_CEILING, ROUND_FLOOR
from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Mapping

from canard_control.fhn_same_model_three_output import (
    validate_same_model_three_output_result_payload,
)


TRACKED_AMPLITUDE_SHA256 = (
    "28e74d2316f7e9324f03874c3294d27d83708c9dbb3f4eefaf04925f55bbba60"
)
TRACKED_THREE_OUTPUT_SHA256 = (
    "afc03431d61d86c6bda8b56a73bdeea76b357e9a31a4a843d9f55cebbf666532"
)
TRACKED_SEPARATOR_SHA256 = (
    "9e859f31c177638a70b3ca451fe743227308343792d77eeca286fca26afc8a86"
)
TRACKED_PARAMETER_BOX_SHA256 = (
    "ff13b5352c2b4e9898a4044be63fd490a3e7bb4217445a6a062188c2457c22a0"
)
TRACKED_TARGET_BALL_SHA256 = (
    "dc17c3f845c3e317570c71af3acff670fb6955e2920ad2cea256507c1353dc05"
)
SYNCHRONOUS_MODEL_ID = "dual-scaffold-synchronous-fhn-two-delay"
FULL_NETWORK_INSTANCE_ID = "rank-one-two-module-fhn-D3-E2"
INPUT_ORDER = ("kappa_1", "kappa_3", "r")
OUTPUT_ORDER = ("F", "A=V_max-V_min", "S_op=-r")
EXACT_INPUT_RADIUS = "1e-12"
RESET_INTERVAL = ("-1", "1")
POSITIVE_RESET_CENTER = "0.5"
NEGATIVE_RESET_CENTER = "-0.5"
TRACKED_SQUARED_OUTPUT_RADIUS = (
    "1.62187273782174089504757331762715967009378618047942197e-14"
)
TRACKED_AMPLITUDE_OUTPUT_RADIUS = (
    "2.75138166016477172021072951467987182906462947064987861e-15"
)


@dataclass(frozen=True)
class AmplitudeSafetyNormComposition:
    """Directed decimal check of the three-dimensional coordinate transfer."""

    precision_digits: int
    amplitude_lower: str
    amplitude_upper: str
    squared_output_radius_lower: str
    amplitude_output_radius_lower: str
    inverse_coordinate_factor_upper: str
    transformed_three_norm_upper: str
    squared_ball_slack_lower: str
    target_amplitude_positive_margin_lower: str
    frequency_component_unchanged: bool
    safety_component_unchanged: bool
    three_dimensional_euclidean_norm_transfer_validated: bool


@dataclass(frozen=True)
class OperationalDeadbandChart:
    """One translated reset chart contained in a single detector channel."""

    chart_id: str
    detector_face: str
    reset_center: str
    safety_center: str
    input_center: tuple[str, str, str]
    output_center: str
    input_radius: str
    reset_projection_lower: str
    reset_projection_upper: str
    threshold_deadband_lower: str
    face_deadband_lower: str
    reset_projection_inside_declared_interval: bool
    reset_projection_does_not_cross_threshold: bool
    reset_projection_does_not_cross_detector_face: bool
    unique_preimage_in_translated_input_ball: bool
    biological_outcome_claimed: bool


@dataclass(frozen=True)
class SameModelAmplitudeSafetyCertificate:
    """Source-bound staged frequency--amplitude--safety theorem."""

    amplitude_result_sha256: str
    three_output_result_sha256: str
    separator_result_sha256: str
    parameter_box_result_sha256: str
    squared_target_ball_result_sha256: str
    source_synchronous_model_id: str
    certified_full_network_instance_id: str
    norm_id: str
    input_order: tuple[str, str, str]
    output_order: tuple[str, str, str]
    map_definition: str
    exact_input_ball_radius: str
    certified_output_ball_radius_lower: str
    parent_squared_output_ball_radius_lower: str
    reset_interval: tuple[str, str]
    norm_composition: AmplitudeSafetyNormComposition
    pulse_side_chart: OperationalDeadbandChart
    quiet_side_chart: OperationalDeadbandChart
    amplitude_source_manifest_validated: bool
    three_output_source_manifest_validated: bool
    separator_source_manifest_validated: bool
    shared_parameter_box_validated: bool
    shared_squared_target_ball_validated: bool
    same_model_staged_protocol_validated: bool
    exact_reset_translation_validated: bool
    three_dimensional_inverse_coordinate_validated: bool
    translated_input_balls_contained_validated: bool
    pulse_and_quiet_operational_deadbands_validated: bool
    unique_input_for_each_certified_target_validated: bool
    frequency_amplitude_operational_safety_target_ball_validated: bool
    bounded_additive_finite_time_preparation_validated: bool
    biological_basin_capture_validated: bool
    physical_finite_pulse_validated: bool
    periodic_attraction_validated: bool
    unforced_onset_validated: bool
    maximal_canard_onset_validated: bool
    noise_hardware_robustness_validated: bool
    general_topology_validated: bool
    issue_15_closed: bool


def _mapping(value: object, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{name} must be a mapping")
    return value


def _require_true(mapping: Mapping[str, Any], name: str) -> None:
    if mapping.get(name) is not True:
        raise ValueError(f"source proof flag {name!r} must be true")


def _require_false(mapping: Mapping[str, Any], name: str) -> None:
    if mapping.get(name) is not False:
        raise ValueError(f"source scope flag {name!r} must be false")


def _decimal(value: object, name: str) -> Decimal:
    if not isinstance(value, str):
        raise ValueError(f"{name} must be a serialized decimal string")
    try:
        result = Decimal(value)
    except InvalidOperation as error:
        raise ValueError(f"{name} is not a decimal") from error
    if not result.is_finite():
        raise ValueError(f"{name} must be finite")
    return result


def _validate_amplitude_payload(
    payload: Mapping[str, Any],
) -> tuple[Mapping[str, Any], Mapping[str, Any]]:
    root = _mapping(payload, "amplitude result")
    certificate = _mapping(root.get("certificate"), "amplitude certificate")
    evidence = _mapping(root.get("source_evidence"), "amplitude evidence")
    scope = _mapping(root.get("scope"), "amplitude scope")
    for flag in (
        "candidate_binary64_is_exact_polynomial_data",
        "exact_orbit_in_wiener_correction_ball",
        "unique_voltage_extrema_on_gain_box",
        "uniform_positive_amplitude_enclosure_validated",
        "frequency_amplitude_target_ball_validated",
    ):
        _require_true(certificate, flag)
    for flag in (
        "candidate_binary64_is_exact_orbit",
        "calibrated_three_output_target_ball_validated",
        "physical_pulse_onset_validated",
    ):
        _require_false(certificate, flag)
    for flag in (
        "uniform_unsquared_amplitude_enclosure",
        "frequency_unsquared_amplitude_target_ball",
    ):
        _require_true(scope, flag)
    for flag in (
        "binary64_candidate_is_exact_orbit",
        "calibrated_three_output_target_ball",
        "physical_pulse_onset",
    ):
        _require_false(scope, flag)
    if tuple(certificate.get("parameter_center", ())) != ("0.2", "0.25"):
        raise ValueError("amplitude result has a different gain center")
    if certificate.get("gain_half_width") != EXACT_INPUT_RADIUS:
        raise ValueError("amplitude result has a different gain half-width")
    if evidence.get("parameter_box_result_sha256") != (
        TRACKED_PARAMETER_BOX_SHA256
    ):
        raise ValueError("amplitude result uses a different parameter box")
    if evidence.get("squared_target_ball_result_sha256") != (
        TRACKED_TARGET_BALL_SHA256
    ):
        raise ValueError("amplitude result uses a different squared target ball")
    if evidence.get("parameter_validation_exact_replay") is not True:
        raise ValueError("amplitude parameter validation was not replayed")
    if evidence.get("squared_target_radius_exact_match") is not True:
        raise ValueError("amplitude squared target radius did not match")
    return certificate, evidence


def _validate_three_output_payload(
    payload: Mapping[str, Any],
) -> tuple[Mapping[str, Any], Mapping[str, Any]]:
    validate_same_model_three_output_result_payload(payload)
    root = _mapping(payload, "three-output result")
    certificate = _mapping(root.get("certificate"), "three-output certificate")
    evidence = _mapping(root.get("source_evidence"), "three-output evidence")
    if certificate.get("source_synchronous_model_id") != SYNCHRONOUS_MODEL_ID:
        raise ValueError("three-output result uses a different model")
    if certificate.get("certified_full_network_instance_id") != (
        FULL_NETWORK_INSTANCE_ID
    ):
        raise ValueError("three-output result uses a different network instance")
    if tuple(certificate.get("input_order", ())) != INPUT_ORDER:
        raise ValueError("three-output result has a different input order")
    if tuple(certificate.get("output_order", ())) != (
        "F",
        "R_h",
        "S_op=-r",
    ):
        raise ValueError("three-output result has a different output order")
    if tuple(certificate.get("input_center", ())) != ("0.2", "0.25", "0"):
        raise ValueError("three-output result has a different input center")
    if certificate.get("exact_input_ball_radius") != EXACT_INPUT_RADIUS:
        raise ValueError("three-output result has a different input radius")
    if tuple(certificate.get("reset_interval", ())) != RESET_INTERVAL:
        raise ValueError("three-output result has a different reset interval")
    if evidence.get("target_ball_result_sha256") != TRACKED_TARGET_BALL_SHA256:
        raise ValueError("three-output result uses a different target ball")
    if evidence.get("separator_result_sha256") != TRACKED_SEPARATOR_SHA256:
        raise ValueError("three-output result uses a different separator")
    if evidence.get("shared_parameter_box_result_sha256") != (
        TRACKED_PARAMETER_BOX_SHA256
    ):
        raise ValueError("three-output result uses a different parameter box")
    return certificate, evidence


def _validate_separator_payload(payload: Mapping[str, Any]) -> None:
    root = _mapping(payload, "separator result")
    certificate = _mapping(root.get("certificate"), "separator certificate")
    evidence = _mapping(root.get("source_evidence"), "separator evidence")
    scope = _mapping(root.get("scope"), "separator scope")
    for flag in (
        "same_synchronous_baseline_and_gain_box_validated",
        "full_network_d3_e2_instance_fixed_by_this_certificate",
        "full_network_collective_projection_exact",
        "physical_collective_recovery_actuator_exact",
        "actuator_has_zero_transverse_projection_exact",
        "controlled_collective_recovery_leaf_invariant_exact",
        "controlled_operational_onset_validated",
        "reset_family_complete_history_threshold_validated",
    ):
        _require_true(certificate, flag)
    for flag in (
        "unforced_onset_validated",
        "maximal_canard_onset_validated",
        "periodic_orbit_attraction_validated",
        "general_network_topology_validated",
        "issue_15_closed",
    ):
        _require_false(certificate, flag)
    for flag in (
        "same_synchronous_baseline_and_gain_box",
        "controlled_operational_first_hit_onset",
        "reset_family_complete_history_threshold",
    ):
        _require_true(scope, flag)
    for flag in (
        "biological_pulse_or_quiet_basin_capture_beyond_channel_faces",
        "unforced_onset",
        "maximal_canard_onset",
        "periodic_orbit_attraction",
        "general_network_topology",
        "issue_15_closed",
    ):
        _require_false(scope, flag)
    if certificate.get("source_synchronous_model_id") != SYNCHRONOUS_MODEL_ID:
        raise ValueError("separator result uses a different model")
    if certificate.get("certified_full_network_instance_id") != (
        FULL_NETWORK_INSTANCE_ID
    ):
        raise ValueError("separator result uses a different network instance")
    if tuple(certificate.get("reset_voltage_interval", ())) != RESET_INTERVAL:
        raise ValueError("separator result has a different reset interval")
    if evidence.get("parameter_box_result_sha256") != (
        TRACKED_PARAMETER_BOX_SHA256
    ):
        raise ValueError("separator result uses a different parameter box")


def _validate_parameter_payload(payload: Mapping[str, Any]) -> None:
    root = _mapping(payload, "parameter-box result")
    validation = _mapping(root.get("validation"), "parameter validation")
    continuation = _mapping(
        validation.get("continuation"), "parameter continuation"
    )
    extrema = _mapping(validation.get("extrema"), "parameter extrema")
    response = _mapping(validation.get("response"), "parameter response")
    for mapping, flags in (
        (
            validation,
            (
                "d1_validated",
                "d3_validated",
                "d4_response_lower_bound_validated",
                "all_d1_d3_d4_validated",
            ),
        ),
        (
            continuation,
            (
                "parameter_box_orbit_validated",
                "parameter_box_bordered_inverse_validated",
            ),
        ),
        (extrema, ("extrema_validated",)),
        (response, ("response_box_validated",)),
    ):
        for flag in flags:
            _require_true(mapping, flag)
    if tuple(response.get("output_order", ())) != ("F", "R_h"):
        raise ValueError("parameter response has a different output order")
    gain_box = _mapping(validation.get("gain_box"), "gain box")
    if gain_box.get("half_width") != EXACT_INPUT_RADIUS:
        raise ValueError("parameter box has a different gain half-width")


def decimal_amplitude_safety_composition(
    amplitude_certificate: Mapping[str, Any],
    three_output_certificate: Mapping[str, Any],
    *,
    precision_digits: int = 140,
) -> AmplitudeSafetyNormComposition:
    """Check the inverse amplitude coordinate in three-dimensional norm."""

    if (
        isinstance(precision_digits, bool)
        or int(precision_digits) != precision_digits
        or int(precision_digits) < 100
    ):
        raise ValueError("Decimal precision must be an integer of at least 100")
    digits = int(precision_digits)
    amplitude = _mapping(amplitude_certificate, "amplitude certificate")
    three = _mapping(three_output_certificate, "three-output certificate")
    a_lower = _decimal(amplitude.get("amplitude_lower"), "amplitude lower")
    a_upper = _decimal(amplitude.get("amplitude_upper"), "amplitude upper")
    rho_a = _decimal(
        amplitude.get("unsquared_amplitude_target_radius_lower"),
        "amplitude target radius",
    )
    rho_r_from_amplitude = _decimal(
        amplitude.get("squared_range_target_radius_lower"),
        "amplitude parent squared radius",
    )
    rho_r = _decimal(
        three.get("certified_output_ball_radius_lower"),
        "three-output squared radius",
    )
    if rho_r_from_amplitude != rho_r:
        raise ValueError("amplitude and three-output squared radii disagree")
    if not (Decimal(0) < rho_a < rho_r and Decimal(0) < a_lower <= a_upper):
        raise ValueError("source radii or amplitude enclosure have invalid signs")

    upward = Context(prec=digits, rounding=ROUND_CEILING)
    downward = Context(prec=digits, rounding=ROUND_FLOOR)
    factor = upward.add(upward.multiply(Decimal(2), a_upper), rho_a)
    norm_factor = max(Decimal(1), factor)
    transformed_norm = upward.multiply(norm_factor, rho_a)
    slack = downward.subtract(rho_r, transformed_norm)
    positive_margin = downward.subtract(a_lower, rho_a)
    if transformed_norm > rho_r:
        raise ValueError("inverse amplitude coordinate leaves the 3D target ball")
    if positive_margin <= 0:
        raise ValueError("amplitude target ball crosses the zero-amplitude branch")
    return AmplitudeSafetyNormComposition(
        precision_digits=digits,
        amplitude_lower=str(a_lower),
        amplitude_upper=str(a_upper),
        squared_output_radius_lower=str(rho_r),
        amplitude_output_radius_lower=str(rho_a),
        inverse_coordinate_factor_upper=str(factor),
        transformed_three_norm_upper=str(transformed_norm),
        squared_ball_slack_lower=str(slack),
        target_amplitude_positive_margin_lower=str(positive_margin),
        frequency_component_unchanged=True,
        safety_component_unchanged=True,
        three_dimensional_euclidean_norm_transfer_validated=True,
    )


def _deadband_chart(
    reset_center_text: str,
    *,
    chart_id: str,
    detector_face: str,
    input_radius_text: str,
    precision_digits: int,
) -> OperationalDeadbandChart:
    reset_center = Decimal(reset_center_text)
    input_radius = Decimal(input_radius_text)
    downward = Context(prec=precision_digits, rounding=ROUND_FLOOR)
    upward = Context(prec=precision_digits, rounding=ROUND_CEILING)
    lower = downward.subtract(reset_center, input_radius)
    upper = upward.add(reset_center, input_radius)
    if not (Decimal(-1) < lower < upper < Decimal(1)):
        raise ValueError("translated reset projection leaves (-1,1)")
    if reset_center > 0:
        if not (Decimal(0) < lower and upper < Decimal(1)):
            raise ValueError("positive chart crosses r=0 or r=1")
        threshold_deadband = lower
        face_deadband = downward.subtract(Decimal(1), upper)
    else:
        if not (Decimal(-1) < lower and upper < Decimal(0)):
            raise ValueError("negative chart crosses r=-1 or r=0")
        threshold_deadband = -upper
        face_deadband = downward.add(lower, Decimal(1))
    if min(threshold_deadband, face_deadband) <= 0:
        raise ValueError("translated chart has no operational deadband")
    safety_center = -reset_center
    input_center = ("0.2", "0.25", str(reset_center))
    output_center = (
        "exact (F(0.2,0.25),A(0.2,0.25),"
        f"{str(safety_center)})"
    )
    return OperationalDeadbandChart(
        chart_id=chart_id,
        detector_face=detector_face,
        reset_center=str(reset_center),
        safety_center=str(safety_center),
        input_center=input_center,
        output_center=output_center,
        input_radius=str(input_radius),
        reset_projection_lower=str(lower),
        reset_projection_upper=str(upper),
        threshold_deadband_lower=str(threshold_deadband),
        face_deadband_lower=str(face_deadband),
        reset_projection_inside_declared_interval=True,
        reset_projection_does_not_cross_threshold=True,
        reset_projection_does_not_cross_detector_face=True,
        unique_preimage_in_translated_input_ball=True,
        biological_outcome_claimed=False,
    )


def same_model_amplitude_safety_from_payloads(
    amplitude_payload: Mapping[str, Any],
    three_output_payload: Mapping[str, Any],
    separator_payload: Mapping[str, Any],
    parameter_payload: Mapping[str, Any],
    *,
    amplitude_result_sha256: str,
    three_output_result_sha256: str,
    separator_result_sha256: str,
    parameter_box_result_sha256: str,
    amplitude_source_manifest_validated: bool = False,
    three_output_source_manifest_validated: bool = False,
    separator_source_manifest_validated: bool = False,
) -> SameModelAmplitudeSafetyCertificate:
    """Validate the four parents and compose the two translated target balls."""

    expected = (
        (amplitude_result_sha256, TRACKED_AMPLITUDE_SHA256, "amplitude"),
        (three_output_result_sha256, TRACKED_THREE_OUTPUT_SHA256, "three-output"),
        (separator_result_sha256, TRACKED_SEPARATOR_SHA256, "separator"),
        (
            parameter_box_result_sha256,
            TRACKED_PARAMETER_BOX_SHA256,
            "parameter-box",
        ),
    )
    for actual, tracked, label in expected:
        if actual != tracked:
            raise ValueError(f"{label} result SHA-256 is not the tracked digest")

    amplitude, amplitude_evidence = _validate_amplitude_payload(
        amplitude_payload
    )
    three, three_evidence = _validate_three_output_payload(
        three_output_payload
    )
    _validate_separator_payload(separator_payload)
    _validate_parameter_payload(parameter_payload)
    if amplitude_evidence["parameter_box_result_sha256"] != (
        three_evidence["shared_parameter_box_result_sha256"]
    ):
        raise ValueError("amplitude and three-output parents use different boxes")
    if amplitude_evidence["squared_target_ball_result_sha256"] != (
        three_evidence["target_ball_result_sha256"]
    ):
        raise ValueError("amplitude and three-output parents use different targets")

    composition = decimal_amplitude_safety_composition(amplitude, three)
    pulse_chart = _deadband_chart(
        POSITIVE_RESET_CENTER,
        chart_id="pulse-side-positive-face-operational-chart",
        detector_face="+1",
        input_radius_text=EXACT_INPUT_RADIUS,
        precision_digits=composition.precision_digits,
    )
    quiet_chart = _deadband_chart(
        NEGATIVE_RESET_CENTER,
        chart_id="quiet-side-negative-face-operational-chart",
        detector_face="-1",
        input_radius_text=EXACT_INPUT_RADIUS,
        precision_digits=composition.precision_digits,
    )
    return SameModelAmplitudeSafetyCertificate(
        amplitude_result_sha256=amplitude_result_sha256,
        three_output_result_sha256=three_output_result_sha256,
        separator_result_sha256=separator_result_sha256,
        parameter_box_result_sha256=parameter_box_result_sha256,
        squared_target_ball_result_sha256=TRACKED_TARGET_BALL_SHA256,
        source_synchronous_model_id=SYNCHRONOUS_MODEL_ID,
        certified_full_network_instance_id=FULL_NETWORK_INSTANCE_ID,
        norm_id="three-dimensional-euclidean-inverse-amplitude-coordinate",
        input_order=INPUT_ORDER,
        output_order=OUTPUT_ORDER,
        map_definition="Q_A(kappa_1,kappa_3,r)=(F,A,-r)",
        exact_input_ball_radius=EXACT_INPUT_RADIUS,
        certified_output_ball_radius_lower=(
            composition.amplitude_output_radius_lower
        ),
        parent_squared_output_ball_radius_lower=(
            composition.squared_output_radius_lower
        ),
        reset_interval=RESET_INTERVAL,
        norm_composition=composition,
        pulse_side_chart=pulse_chart,
        quiet_side_chart=quiet_chart,
        amplitude_source_manifest_validated=(
            amplitude_source_manifest_validated
        ),
        three_output_source_manifest_validated=(
            three_output_source_manifest_validated
        ),
        separator_source_manifest_validated=(
            separator_source_manifest_validated
        ),
        shared_parameter_box_validated=True,
        shared_squared_target_ball_validated=True,
        same_model_staged_protocol_validated=True,
        exact_reset_translation_validated=True,
        three_dimensional_inverse_coordinate_validated=True,
        translated_input_balls_contained_validated=True,
        pulse_and_quiet_operational_deadbands_validated=True,
        unique_input_for_each_certified_target_validated=True,
        frequency_amplitude_operational_safety_target_ball_validated=True,
        bounded_additive_finite_time_preparation_validated=False,
        biological_basin_capture_validated=False,
        physical_finite_pulse_validated=False,
        periodic_attraction_validated=False,
        unforced_onset_validated=False,
        maximal_canard_onset_validated=False,
        noise_hardware_robustness_validated=False,
        general_topology_validated=False,
        issue_15_closed=False,
    )


def _load_json_with_hash(
    path: Path, expected: str, label: str
) -> tuple[dict[str, Any], str]:
    raw = path.read_bytes()
    digest = sha256(raw).hexdigest()
    if digest != expected:
        raise ValueError(
            f"{label} SHA-256 mismatch: expected {expected}, got {digest}"
        )
    try:
        payload = json.loads(raw)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError(f"{label} is not valid UTF-8 JSON") from error
    if not isinstance(payload, dict):
        raise ValueError(f"{label} must contain a JSON object")
    return payload, digest


def _verify_manifest(
    payload: Mapping[str, Any], repository: Path, label: str
) -> None:
    provenance = _mapping(payload.get("provenance"), f"{label} provenance")
    generator = provenance.get("generator")
    generator_digest = provenance.get("generator_sha256")
    manifest = _mapping(
        provenance.get("proof_source_manifest"), f"{label} source manifest"
    )
    if not isinstance(generator, str) or not isinstance(generator_digest, str):
        raise ValueError(f"{label} generator provenance is invalid")
    root = repository.resolve()

    def checked_path(relative: str) -> Path:
        candidate = (root / relative).resolve()
        try:
            candidate.relative_to(root)
        except ValueError as error:
            raise ValueError(f"{label} manifest path escapes repository") from error
        return candidate

    generator_path = checked_path(generator)
    if sha256(generator_path.read_bytes()).hexdigest() != generator_digest:
        raise ValueError(f"{label} generator manifest SHA-256 mismatch")
    if not manifest:
        raise ValueError(f"{label} proof source manifest is empty")
    for relative, digest in manifest.items():
        if not isinstance(relative, str) or not isinstance(digest, str):
            raise ValueError(f"{label} proof source manifest is invalid")
        if sha256(checked_path(relative).read_bytes()).hexdigest() != digest:
            raise ValueError(f"{label} proof source manifest SHA-256 mismatch")


def load_same_model_amplitude_safety(
    amplitude_path: str | Path,
    three_output_path: str | Path,
    separator_path: str | Path,
    parameter_box_path: str | Path,
    *,
    repository: str | Path,
) -> SameModelAmplitudeSafetyCertificate:
    """Hash-check all four parents, verify manifests, and compose."""

    amplitude, amplitude_digest = _load_json_with_hash(
        Path(amplitude_path), TRACKED_AMPLITUDE_SHA256, "amplitude result"
    )
    three, three_digest = _load_json_with_hash(
        Path(three_output_path), TRACKED_THREE_OUTPUT_SHA256, "three-output result"
    )
    separator, separator_digest = _load_json_with_hash(
        Path(separator_path), TRACKED_SEPARATOR_SHA256, "separator result"
    )
    parameter, parameter_digest = _load_json_with_hash(
        Path(parameter_box_path),
        TRACKED_PARAMETER_BOX_SHA256,
        "parameter-box result",
    )
    repository_path = Path(repository)
    _verify_manifest(amplitude, repository_path, "amplitude result")
    _verify_manifest(three, repository_path, "three-output result")
    _verify_manifest(separator, repository_path, "separator result")
    return same_model_amplitude_safety_from_payloads(
        amplitude,
        three,
        separator,
        parameter,
        amplitude_result_sha256=amplitude_digest,
        three_output_result_sha256=three_digest,
        separator_result_sha256=separator_digest,
        parameter_box_result_sha256=parameter_digest,
        amplitude_source_manifest_validated=True,
        three_output_source_manifest_validated=True,
        separator_source_manifest_validated=True,
    )


_TRUE_RESULT_SCOPE = (
    "frequency_unsquared_amplitude_operational_safety_target_ball",
    "same_baseline_staged_protocol",
    "controlled_operational_first_hit_safety",
    "pulse_side_positive_face_deadband_chart",
    "quiet_side_negative_face_deadband_chart",
)
_FALSE_RESULT_SCOPE = (
    "bounded_additive_finite_time_preparation",
    "biological_basin_capture",
    "physical_finite_pulse",
    "periodic_attraction",
    "unforced_onset",
    "maximal_canard_onset",
    "noise_hardware_robustness",
    "general_topology",
    "issue_15_closed",
)


def validate_same_model_amplitude_safety_result_payload(
    payload: Mapping[str, Any],
) -> None:
    """Reject missing evidence or any promotion beyond operational safety."""

    root = _mapping(payload, "amplitude-safety result")
    evidence = _mapping(root.get("source_evidence"), "source_evidence")
    certificate = _mapping(root.get("certificate"), "certificate")
    scope = _mapping(root.get("scope"), "scope")
    expected_hashes = {
        "amplitude_result_sha256": TRACKED_AMPLITUDE_SHA256,
        "three_output_result_sha256": TRACKED_THREE_OUTPUT_SHA256,
        "separator_result_sha256": TRACKED_SEPARATOR_SHA256,
        "parameter_box_result_sha256": TRACKED_PARAMETER_BOX_SHA256,
    }
    for name, expected in expected_hashes.items():
        if evidence.get(name) != expected:
            raise ValueError(f"result evidence {name!r} is invalid")
        if certificate.get(name) != expected:
            raise ValueError(f"result certificate {name!r} is invalid")
    if certificate.get("squared_target_ball_result_sha256") != (
        TRACKED_TARGET_BALL_SHA256
    ):
        raise ValueError("result squared target-ball evidence is invalid")
    if certificate.get("source_synchronous_model_id") != SYNCHRONOUS_MODEL_ID:
        raise ValueError("result source model identifier is invalid")
    if certificate.get("certified_full_network_instance_id") != (
        FULL_NETWORK_INSTANCE_ID
    ):
        raise ValueError("result full-network instance identifier is invalid")
    if tuple(certificate.get("input_order", ())) != INPUT_ORDER:
        raise ValueError("result input order is invalid")
    if tuple(certificate.get("output_order", ())) != OUTPUT_ORDER:
        raise ValueError("result output order is invalid")
    if certificate.get("map_definition") != (
        "Q_A(kappa_1,kappa_3,r)=(F,A,-r)"
    ):
        raise ValueError("result map definition is invalid")
    if certificate.get("exact_input_ball_radius") != EXACT_INPUT_RADIUS:
        raise ValueError("result input radius is invalid")
    if tuple(certificate.get("reset_interval", ())) != RESET_INTERVAL:
        raise ValueError("result reset interval is invalid")
    output_radius = _decimal(
        certificate.get("certified_output_ball_radius_lower"),
        "result amplitude output radius",
    )
    squared_radius = _decimal(
        certificate.get("parent_squared_output_ball_radius_lower"),
        "result squared output radius",
    )
    if output_radius != Decimal(TRACKED_AMPLITUDE_OUTPUT_RADIUS):
        raise ValueError("result amplitude output radius is invalid")
    if squared_radius != Decimal(TRACKED_SQUARED_OUTPUT_RADIUS):
        raise ValueError("result squared output radius is invalid")
    composition = _mapping(
        certificate.get("norm_composition"), "result norm composition"
    )
    _require_true(
        composition, "three_dimensional_euclidean_norm_transfer_validated"
    )
    _require_true(composition, "frequency_component_unchanged")
    _require_true(composition, "safety_component_unchanged")
    if _decimal(
        composition.get("amplitude_output_radius_lower"),
        "composition amplitude radius",
    ) != output_radius:
        raise ValueError("composition amplitude radius disagrees with result")
    if _decimal(
        composition.get("squared_output_radius_lower"),
        "composition squared radius",
    ) != squared_radius:
        raise ValueError("composition squared radius disagrees with result")
    transformed = _decimal(
        composition.get("transformed_three_norm_upper"),
        "composition transformed norm",
    )
    slack = _decimal(
        composition.get("squared_ball_slack_lower"),
        "composition squared-ball slack",
    )
    positive_margin = _decimal(
        composition.get("target_amplitude_positive_margin_lower"),
        "composition amplitude margin",
    )
    if transformed > squared_radius or min(slack, positive_margin) <= 0:
        raise ValueError("result inverse-coordinate inequalities are invalid")
    for chart_name, center, detector_face in (
        ("pulse_side_chart", Decimal("0.5"), "+1"),
        ("quiet_side_chart", Decimal("-0.5"), "-1"),
    ):
        chart = _mapping(certificate.get(chart_name), chart_name)
        if _decimal(chart.get("reset_center"), f"{chart_name} center") != center:
            raise ValueError(f"{chart_name} reset center is invalid")
        if chart.get("detector_face") != detector_face:
            raise ValueError(f"{chart_name} detector face is invalid")
        for flag in (
            "reset_projection_inside_declared_interval",
            "reset_projection_does_not_cross_threshold",
            "reset_projection_does_not_cross_detector_face",
            "unique_preimage_in_translated_input_ball",
        ):
            _require_true(chart, flag)
        _require_false(chart, "biological_outcome_claimed")
        lower = _decimal(chart.get("reset_projection_lower"), "chart lower")
        upper = _decimal(chart.get("reset_projection_upper"), "chart upper")
        if center > 0 and not (Decimal(0) < lower < upper < Decimal(1)):
            raise ValueError("pulse-side chart crosses an operational boundary")
        if center < 0 and not (Decimal(-1) < lower < upper < Decimal(0)):
            raise ValueError("quiet-side chart crosses an operational boundary")
    for flag in (
        "amplitude_source_manifest_validated",
        "three_output_source_manifest_validated",
        "separator_source_manifest_validated",
        "shared_parameter_box_validated",
        "shared_squared_target_ball_validated",
        "same_model_staged_protocol_validated",
        "exact_reset_translation_validated",
        "three_dimensional_inverse_coordinate_validated",
        "translated_input_balls_contained_validated",
        "pulse_and_quiet_operational_deadbands_validated",
        "unique_input_for_each_certified_target_validated",
        "frequency_amplitude_operational_safety_target_ball_validated",
    ):
        _require_true(certificate, flag)
    for flag in (
        "bounded_additive_finite_time_preparation_validated",
        "biological_basin_capture_validated",
        "physical_finite_pulse_validated",
        "periodic_attraction_validated",
        "unforced_onset_validated",
        "maximal_canard_onset_validated",
        "noise_hardware_robustness_validated",
        "general_topology_validated",
        "issue_15_closed",
    ):
        _require_false(certificate, flag)
    expected_scope = set(_TRUE_RESULT_SCOPE) | set(_FALSE_RESULT_SCOPE)
    if set(scope) != expected_scope:
        raise ValueError("result scope keys are missing or unexpected")
    for name in _TRUE_RESULT_SCOPE:
        _require_true(scope, name)
    for name in _FALSE_RESULT_SCOPE:
        _require_false(scope, name)


def load_same_model_amplitude_safety_result(
    path: str | Path,
    *,
    expected_sha256: str,
) -> Mapping[str, Any]:
    """Hash-check and semantically validate a generated result."""

    payload, _ = _load_json_with_hash(
        Path(path), expected_sha256, "amplitude-safety result"
    )
    validate_same_model_amplitude_safety_result_payload(payload)
    return payload
