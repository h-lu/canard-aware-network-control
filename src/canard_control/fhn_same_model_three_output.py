"""Three-output staged-control target ball for the same FHN model.

This module composes two independently tracked artifacts:

* the directed baseline response target ball for
  ``P(kappa_1,kappa_3)=(F,R_h)`` with
  ``R_h=(V_max-V_min)**2``; and
* the same-model recovery-clamped separator whose operational first-hit
  threshold is exactly ``r_c=0`` for the constant-history reset coordinate
  ``r``.

The staged output is

``Q_op(kappa_1,kappa_3,r)=(F,R_h,-r)``.

The reset is absent from the baseline periodic RFDE and is used only during
the later decision stage.  Hence

``D Q_op = diag(DP,-1)`` and ``M0=diag(B0,-1)``.

In Euclidean norm, ``sigma_min(M0)=min(sigma_min(B0),1)`` and
``||D Q_op-M0||_F=||DP-B0||_F``.  The two-output fixed-matrix defect theorem
therefore transfers without loss to three outputs.  Decimal arithmetic
recomposes the margin and radius from the public directed parent endpoints;
the final radius is the minimum of that recomposition and the already
published parent lower endpoint.

This is an operational first-hit margin for a staged controlled protocol.
It is not an unsquared-amplitude theorem, a physical finite-pulse theorem, a
biological basin-capture theorem, or an unforced/maximal-canard theorem.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Context, Decimal, InvalidOperation, ROUND_CEILING, ROUND_FLOOR
from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Mapping, Sequence


TRACKED_TARGET_BALL_SHA256 = (
    "dc17c3f845c3e317570c71af3acff670fb6955e2920ad2cea256507c1353dc05"
)
TRACKED_SEPARATOR_SHA256 = (
    "9e859f31c177638a70b3ca451fe743227308343792d77eeca286fca26afc8a86"
)
TRACKED_PARAMETER_BOX_SHA256 = (
    "ff13b5352c2b4e9898a4044be63fd490a3e7bb4217445a6a062188c2457c22a0"
)
SYNCHRONOUS_MODEL_ID = "dual-scaffold-synchronous-fhn-two-delay"
FULL_NETWORK_INSTANCE_ID = "rank-one-two-module-fhn-D3-E2"
INPUT_ORDER = ("kappa_1", "kappa_3", "r")
OUTPUT_ORDER = ("F", "R_h", "S_op=-r")
TARGET_CENTER = ("0.2", "0.25", "0")
EXACT_INPUT_RADIUS = "1e-12"


@dataclass(frozen=True)
class ThreeOutputDecimalComposition:
    """Directed Decimal reconstruction from public target-ball endpoints."""

    precision_digits: int
    parent_s0_lower: str
    parent_derivative_defect_upper: str
    parent_certified_input_radius_lower: str
    parent_response_margin_lower: str
    parent_contraction_upper: str
    parent_contraction_margin_lower: str
    parent_output_radius_lower: str
    recomposed_margin_lower: str
    recomposed_contraction_upper: str
    recomposed_contraction_margin_lower: str
    recomposed_output_radius_lower: str
    selected_margin_lower: str
    selected_contraction_upper: str
    selected_contraction_margin_lower: str
    selected_output_radius_lower: str


@dataclass(frozen=True)
class SameModelThreeOutputCertificate:
    """Fixed-inverse certificate and deliberately narrow claim ledger."""

    target_ball_result_sha256: str
    separator_result_sha256: str
    shared_parameter_box_result_sha256: str
    source_synchronous_model_id: str
    certified_full_network_instance_id: str
    norm_id: str
    input_order: tuple[str, str, str]
    output_order: tuple[str, str, str]
    map_definition: str
    input_center: tuple[str, str, str]
    output_center: str
    exact_input_ball_radius: str
    parent_certified_input_radius_lower: str
    reset_interval: tuple[str, str]
    midpoint_matrix_3d_binary64: tuple[
        tuple[float, float, float],
        tuple[float, float, float],
        tuple[float, float, float],
    ]
    midpoint_singular_value_lower: str
    derivative_defect_frobenius_upper: str
    response_margin_lower: str
    fixed_inverse_contraction_upper: str
    fixed_inverse_contraction_margin_lower: str
    certified_output_ball_radius_lower: str
    decimal_composition: ThreeOutputDecimalComposition
    target_source_manifest_validated: bool
    separator_source_manifest_validated: bool
    shared_gain_box_and_model_validated: bool
    exact_block_diagonal_reset_column_validated: bool
    midpoint_singular_value_block_transfer_validated: bool
    derivative_defect_block_transfer_validated: bool
    three_dimensional_input_ball_contained: bool
    unique_input_for_each_certified_target_validated: bool
    frequency_squared_range_operational_margin_target_ball_validated: bool
    same_baseline_staged_protocol_validated: bool
    unsquared_amplitude_validated: bool
    physical_finite_pulse_validated: bool
    biological_basin_beyond_channel_faces_validated: bool
    noise_hardware_robustness_validated: bool
    unforced_onset_validated: bool
    maximal_canard_onset_validated: bool
    periodic_attraction_validated: bool
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


def _matrix_2d(value: object) -> tuple[tuple[float, float], tuple[float, float]]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        raise ValueError("parent midpoint matrix must be 2 by 2")
    rows = tuple(value)
    if len(rows) != 2:
        raise ValueError("parent midpoint matrix must be 2 by 2")
    result: list[tuple[float, float]] = []
    for row in rows:
        if not isinstance(row, Sequence) or isinstance(row, (str, bytes)):
            raise ValueError("parent midpoint matrix must be 2 by 2")
        entries = tuple(row)
        if len(entries) != 2:
            raise ValueError("parent midpoint matrix must be 2 by 2")
        numbers = (float(entries[0]), float(entries[1]))
        if any(not Decimal.from_float(number).is_finite() for number in numbers):
            raise ValueError("parent midpoint matrix entries must be finite")
        result.append(numbers)
    return result[0], result[1]


def decimal_three_output_composition(
    target_ball: Mapping[str, Any],
    *,
    precision_digits: int = 120,
) -> ThreeOutputDecimalComposition:
    """Recompose the three-output constants from public parent endpoints."""

    if (
        isinstance(precision_digits, bool)
        or int(precision_digits) != precision_digits
        or int(precision_digits) < 90
    ):
        raise ValueError("Decimal precision must be an integer of at least 90")
    digits = int(precision_digits)
    parent = _mapping(target_ball, "target_ball")
    s0 = _decimal(
        parent.get("recomputed_midpoint_singular_value_lower"),
        "parent s0 lower",
    )
    defect = _decimal(
        parent.get("recomputed_derivative_frobenius_radius_upper"),
        "parent derivative defect upper",
    )
    parent_input = _decimal(
        parent.get("certified_input_ball_radius"),
        "parent input radius lower",
    )
    parent_output = _decimal(
        parent.get("certified_output_ball_radius_lower"),
        "parent output radius lower",
    )
    parent_margin = _decimal(
        parent.get("recomputed_response_margin_lower"),
        "parent response margin lower",
    )
    parent_contraction = _decimal(
        parent.get("fixed_inverse_contraction_upper"),
        "parent contraction upper",
    )
    parent_contraction_margin = _decimal(
        parent.get("fixed_inverse_contraction_margin_lower"),
        "parent contraction margin lower",
    )
    exact_input = Decimal(EXACT_INPUT_RADIUS)
    if not (Decimal(0) < defect < s0 < Decimal(1)):
        raise ValueError("parent endpoints do not give 0<defect<s0<1")
    if not (Decimal(0) < parent_input <= exact_input):
        raise ValueError("parent input radius is incompatible with 1e-12")

    downward = Context(prec=digits, rounding=ROUND_FLOOR)
    upward = Context(prec=digits, rounding=ROUND_CEILING)
    margin = downward.subtract(s0, defect)
    contraction = upward.divide(defect, s0)
    direct_contraction_margin = downward.subtract(Decimal(1), contraction)
    if parent_margin > margin:
        raise ValueError("parent response margin exceeds public endpoint difference")
    if parent_contraction < contraction:
        raise ValueError("parent contraction upper bound is understated")
    if parent_contraction_margin > downward.subtract(
        Decimal(1), parent_contraction
    ):
        raise ValueError("parent contraction margin lower bound is overstated")
    selected_margin = min(margin, parent_margin)
    selected_contraction = max(contraction, parent_contraction)
    selected_contraction_margin = min(
        direct_contraction_margin,
        parent_contraction_margin,
        downward.subtract(Decimal(1), selected_contraction),
    )
    recomposed_output = downward.multiply(selected_margin, parent_input)
    if min(
        selected_margin,
        selected_contraction_margin,
        recomposed_output,
        parent_output,
    ) <= 0:
        raise ValueError("public parent endpoints give no positive target ball")
    if parent_output > recomposed_output:
        raise ValueError("parent output radius exceeds its public recomposition")
    selected_output = min(parent_output, recomposed_output)
    return ThreeOutputDecimalComposition(
        precision_digits=digits,
        parent_s0_lower=str(s0),
        parent_derivative_defect_upper=str(defect),
        parent_certified_input_radius_lower=str(parent_input),
        parent_response_margin_lower=str(parent_margin),
        parent_contraction_upper=str(parent_contraction),
        parent_contraction_margin_lower=str(parent_contraction_margin),
        parent_output_radius_lower=str(parent_output),
        recomposed_margin_lower=str(margin),
        recomposed_contraction_upper=str(contraction),
        recomposed_contraction_margin_lower=str(direct_contraction_margin),
        recomposed_output_radius_lower=str(recomposed_output),
        selected_margin_lower=str(selected_margin),
        selected_contraction_upper=str(selected_contraction),
        selected_contraction_margin_lower=str(selected_contraction_margin),
        selected_output_radius_lower=str(selected_output),
    )


def _validate_target_source(payload: Mapping[str, Any]) -> tuple[Mapping[str, Any], Mapping[str, Any]]:
    root = _mapping(payload, "target-ball result")
    target = _mapping(root.get("target_ball"), "target_ball")
    scope = _mapping(root.get("scope"), "target scope")
    evidence = _mapping(root.get("source_evidence"), "target source_evidence")
    for flag in (
        "source_d1_branch_validated",
        "source_d3_extrema_validated",
        "source_d4_derivative_box_validated",
        "source_record_consistent",
        "centered_input_ball_contained_in_gain_box",
        "fixed_inverse_contraction_validated",
        "base_frequency_squared_range_target_ball_validated",
    ):
        _require_true(target, flag)
    for flag in (
        "calibrated_reset_target_ball_validated",
        "second_sensitivity_validated",
        "second_sensitivity_required_for_base_target_ball",
        "physical_pulse_onset_validated",
        "issue_15_closed",
    ):
        _require_false(target, flag)
    _require_true(scope, "base_frequency_squared_range_target_ball")
    _require_true(scope, "synchronous_orbital_hyperbolicity")
    for flag in (
        "attraction",
        "full_network_transverse_stability",
        "calibrated_three_output_target_ball",
        "same_model_periodic_separator_bridge",
        "physical_pulse_onset",
        "issue_15_closed",
    ):
        _require_false(scope, flag)
    if scope.get("calibrated_reset_transfer") != "conditional":
        raise ValueError("parent calibrated reset scope must remain conditional")
    if tuple(target.get("control_order", ())) != ("kappa_1", "kappa_3"):
        raise ValueError("target parent has a different control order")
    if tuple(target.get("output_order", ())) != ("F", "R_h"):
        raise ValueError("target parent has a different output order")
    if tuple(target.get("parameter_center", ())) != ("0.2", "0.25"):
        raise ValueError("target parent has a different gain center")
    if target.get("gain_half_width") != EXACT_INPUT_RADIUS:
        raise ValueError("target parent has a different gain half-width")
    if target.get("norm_id") != (
        "euclidean-input-output-fixed-midpoint-inverse"
    ):
        raise ValueError("target parent uses a different norm")
    if evidence.get("parameter_box_result_sha256") != (
        TRACKED_PARAMETER_BOX_SHA256
    ):
        raise ValueError("target parent uses a different parameter box")
    return target, evidence


def _validate_separator_source(
    payload: Mapping[str, Any],
) -> tuple[Mapping[str, Any], Mapping[str, Any]]:
    root = _mapping(payload, "separator result")
    certificate = _mapping(root.get("certificate"), "separator certificate")
    scope = _mapping(root.get("scope"), "separator scope")
    evidence = _mapping(
        root.get("source_evidence"), "separator source_evidence"
    )
    for flag in (
        "same_synchronous_baseline_and_gain_box_validated",
        "full_network_d3_e2_instance_fixed_by_this_certificate",
        "full_network_collective_projection_exact",
        "physical_collective_recovery_actuator_exact",
        "actuator_has_zero_transverse_projection_exact",
        "controlled_collective_recovery_leaf_invariant_exact",
        "controlled_operational_onset_validated",
        "reset_family_complete_history_threshold_validated",
        "controlled_clamped_complete_history_stable_manifold_validated",
    ):
        _require_true(certificate, flag)
    for flag in (
        "source_periodic_artifact_certifies_full_network_scaffolds",
        "quantified_noisy_history_capture_validated",
        "nonlinear_transverse_synchronization_during_clamped_decision_validated",
        "periodic_full_network_transverse_stability_validated",
        "unforced_complete_history_stable_manifold_validated",
        "unforced_onset_validated",
        "maximal_canard_onset_validated",
        "periodic_orbit_attraction_validated",
        "general_network_topology_validated",
        "issue_15_closed",
    ):
        _require_false(certificate, flag)
    for flag in (
        "same_synchronous_baseline_and_gain_box",
        "full_network_d3_e2_instance_fixed_by_separator_certificate",
        "full_network_collective_clamp_exact",
        "controlled_operational_first_hit_onset",
        "reset_family_complete_history_threshold",
        "controlled_clamped_complete_history_stable_manifold",
    ):
        _require_true(scope, flag)
    for flag in (
        "source_periodic_artifact_certifies_full_network_scaffolds",
        "biological_pulse_or_quiet_basin_capture_beyond_channel_faces",
        "quantified_noisy_history_capture",
        "nonlinear_transverse_synchronization_during_clamped_decision",
        "periodic_full_network_transverse_stability",
        "unforced_complete_history_stable_manifold",
        "unforced_onset",
        "maximal_canard_onset",
        "periodic_orbit_attraction",
        "general_network_topology",
        "issue_15_closed",
    ):
        _require_false(scope, flag)
    if certificate.get("source_synchronous_model_id") != SYNCHRONOUS_MODEL_ID:
        raise ValueError("separator parent has a different synchronous model")
    if certificate.get("certified_full_network_instance_id") != (
        FULL_NETWORK_INSTANCE_ID
    ):
        raise ValueError("separator parent has a different network instance")
    if tuple(certificate.get("control_order", ())) != ("kappa_1", "kappa_3"):
        raise ValueError("separator parent has a different control order")
    if tuple(certificate.get("output_order", ())) != ("F", "R_h"):
        raise ValueError("separator parent has a different baseline output order")
    if certificate.get("gain_half_width") != EXACT_INPUT_RADIUS:
        raise ValueError("separator parent has a different gain half-width")
    if tuple(certificate.get("reset_voltage_interval", ())) != ("-1", "1"):
        raise ValueError("separator parent has a different reset interval")
    if evidence.get("parameter_box_result_sha256") != (
        TRACKED_PARAMETER_BOX_SHA256
    ):
        raise ValueError("separator parent uses a different parameter box")
    if evidence.get("source_synchronous_model") != SYNCHRONOUS_MODEL_ID:
        raise ValueError("separator evidence has a different model identifier")
    return certificate, evidence


def _validate_shared_gain_box(
    target: Mapping[str, Any], separator: Mapping[str, Any]
) -> None:
    center_1 = _decimal(target["parameter_center"][0], "gain center 1")
    center_3 = _decimal(target["parameter_center"][1], "gain center 3")
    width = _decimal(target["gain_half_width"], "gain half-width")
    if center_1 != Decimal(1) / Decimal(5) or center_3 != (
        Decimal(1) / Decimal(4)
    ):
        raise ValueError("target and separator gain centers disagree")
    intervals = (
        separator.get("kappa_1_interval"),
        separator.get("kappa_3_interval"),
    )
    for center, interval, name in zip(
        (center_1, center_3), intervals, ("kappa_1", "kappa_3"), strict=True
    ):
        if not isinstance(interval, Sequence) or isinstance(interval, (str, bytes)):
            raise ValueError(f"separator {name} interval is invalid")
        endpoints = tuple(interval)
        if len(endpoints) != 2:
            raise ValueError(f"separator {name} interval is invalid")
        lower = _decimal(endpoints[0], f"separator {name} lower")
        upper = _decimal(endpoints[1], f"separator {name} upper")
        if lower > center - width or upper < center + width:
            raise ValueError("target and separator gain boxes disagree")


def same_model_three_output_from_payloads(
    target_payload: Mapping[str, Any],
    separator_payload: Mapping[str, Any],
    *,
    target_result_sha256: str,
    separator_result_sha256: str,
    target_source_manifest_validated: bool = False,
    separator_source_manifest_validated: bool = False,
) -> SameModelThreeOutputCertificate:
    """Validate both parent records and compose their three-output theorem."""

    if target_result_sha256 != TRACKED_TARGET_BALL_SHA256:
        raise ValueError("target-ball result SHA-256 is not the tracked digest")
    if separator_result_sha256 != TRACKED_SEPARATOR_SHA256:
        raise ValueError("separator result SHA-256 is not the tracked digest")
    target, target_evidence = _validate_target_source(target_payload)
    separator, separator_evidence = _validate_separator_source(
        separator_payload
    )
    if target_evidence["parameter_box_result_sha256"] != separator_evidence[
        "parameter_box_result_sha256"
    ]:
        raise ValueError("parent artifacts use different parameter boxes")
    _validate_shared_gain_box(target, separator)

    composition = decimal_three_output_composition(target)
    matrix_2d = _matrix_2d(target.get("midpoint_matrix_binary64"))
    matrix_3d = (
        (matrix_2d[0][0], matrix_2d[0][1], 0.0),
        (matrix_2d[1][0], matrix_2d[1][1], 0.0),
        (0.0, 0.0, -1.0),
    )
    exact_radius = Decimal(EXACT_INPUT_RADIUS)
    reset_lower = _decimal(separator["reset_voltage_interval"][0], "reset lower")
    reset_upper = _decimal(separator["reset_voltage_interval"][1], "reset upper")
    if not (reset_lower < -exact_radius and exact_radius < reset_upper):
        raise ValueError("the reset interval does not contain the 3D input ball")

    return SameModelThreeOutputCertificate(
        target_ball_result_sha256=target_result_sha256,
        separator_result_sha256=separator_result_sha256,
        shared_parameter_box_result_sha256=TRACKED_PARAMETER_BOX_SHA256,
        source_synchronous_model_id=SYNCHRONOUS_MODEL_ID,
        certified_full_network_instance_id=FULL_NETWORK_INSTANCE_ID,
        norm_id="three-dimensional-euclidean-fixed-block-inverse",
        input_order=INPUT_ORDER,
        output_order=OUTPUT_ORDER,
        map_definition="Q_op(kappa_1,kappa_3,r)=(F,R_h,-r)",
        input_center=TARGET_CENTER,
        output_center="exact (F(0.2,0.25),R_h(0.2,0.25),0)",
        exact_input_ball_radius=EXACT_INPUT_RADIUS,
        parent_certified_input_radius_lower=(
            composition.parent_certified_input_radius_lower
        ),
        reset_interval=("-1", "1"),
        midpoint_matrix_3d_binary64=matrix_3d,
        midpoint_singular_value_lower=composition.parent_s0_lower,
        derivative_defect_frobenius_upper=(
            composition.parent_derivative_defect_upper
        ),
        response_margin_lower=composition.selected_margin_lower,
        fixed_inverse_contraction_upper=(
            composition.selected_contraction_upper
        ),
        fixed_inverse_contraction_margin_lower=(
            composition.selected_contraction_margin_lower
        ),
        certified_output_ball_radius_lower=(
            composition.selected_output_radius_lower
        ),
        decimal_composition=composition,
        target_source_manifest_validated=target_source_manifest_validated,
        separator_source_manifest_validated=separator_source_manifest_validated,
        shared_gain_box_and_model_validated=True,
        exact_block_diagonal_reset_column_validated=True,
        midpoint_singular_value_block_transfer_validated=True,
        derivative_defect_block_transfer_validated=True,
        three_dimensional_input_ball_contained=True,
        unique_input_for_each_certified_target_validated=True,
        frequency_squared_range_operational_margin_target_ball_validated=True,
        same_baseline_staged_protocol_validated=True,
        unsquared_amplitude_validated=False,
        physical_finite_pulse_validated=False,
        biological_basin_beyond_channel_faces_validated=False,
        noise_hardware_robustness_validated=False,
        unforced_onset_validated=False,
        maximal_canard_onset_validated=False,
        periodic_attraction_validated=False,
        general_topology_validated=False,
        issue_15_closed=False,
    )


def _load_json_with_hash(path: Path, expected: str, label: str) -> tuple[dict, str]:
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


def _verify_manifest(payload: Mapping[str, Any], repository: Path, label: str) -> None:
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


def load_same_model_three_output(
    target_ball_path: str | Path,
    separator_path: str | Path,
    *,
    repository: str | Path,
) -> SameModelThreeOutputCertificate:
    """Hash-check both source artifacts, verify manifests, and compose."""

    target_payload, target_digest = _load_json_with_hash(
        Path(target_ball_path), TRACKED_TARGET_BALL_SHA256, "target-ball result"
    )
    separator_payload, separator_digest = _load_json_with_hash(
        Path(separator_path), TRACKED_SEPARATOR_SHA256, "separator result"
    )
    repository_path = Path(repository)
    _verify_manifest(target_payload, repository_path, "target-ball result")
    _verify_manifest(separator_payload, repository_path, "separator result")
    return same_model_three_output_from_payloads(
        target_payload,
        separator_payload,
        target_result_sha256=target_digest,
        separator_result_sha256=separator_digest,
        target_source_manifest_validated=True,
        separator_source_manifest_validated=True,
    )


_TRUE_RESULT_SCOPE = (
    "frequency_squared_range_operational_first_hit_margin_target_ball",
    "same_baseline_staged_protocol",
)
_FALSE_RESULT_SCOPE = (
    "unsquared_amplitude",
    "physical_finite_pulse",
    "biological_basin_beyond_channel_faces",
    "noise_hardware_robustness",
    "unforced_onset",
    "maximal_canard_onset",
    "periodic_attraction",
    "general_topology",
    "issue_15_closed",
)


def validate_same_model_three_output_result_payload(
    payload: Mapping[str, Any],
) -> None:
    """Reject missing evidence or any promotion of the staged theorem."""

    root = _mapping(payload, "three-output result")
    sources = _mapping(root.get("source_evidence"), "source_evidence")
    certificate = _mapping(root.get("certificate"), "certificate")
    scope = _mapping(root.get("scope"), "scope")
    if sources.get("target_ball_result_sha256") != TRACKED_TARGET_BALL_SHA256:
        raise ValueError("result is not bound to the tracked target-ball artifact")
    if sources.get("separator_result_sha256") != TRACKED_SEPARATOR_SHA256:
        raise ValueError("result is not bound to the tracked separator artifact")
    if sources.get("shared_parameter_box_result_sha256") != (
        TRACKED_PARAMETER_BOX_SHA256
    ):
        raise ValueError("result parents do not share the tracked parameter box")
    if sources.get("source_synchronous_model_id") != SYNCHRONOUS_MODEL_ID:
        raise ValueError("result source model identifier is invalid")
    if sources.get("certified_full_network_instance_id") != (
        FULL_NETWORK_INSTANCE_ID
    ):
        raise ValueError("result full-network instance identifier is invalid")
    if tuple(certificate.get("input_order", ())) != INPUT_ORDER:
        raise ValueError("result input order is invalid")
    if tuple(certificate.get("output_order", ())) != OUTPUT_ORDER:
        raise ValueError("result output order is invalid")
    if certificate.get("map_definition") != (
        "Q_op(kappa_1,kappa_3,r)=(F,R_h,-r)"
    ):
        raise ValueError("result staged map definition is invalid")
    if certificate.get("exact_input_ball_radius") != EXACT_INPUT_RADIUS:
        raise ValueError("result input-ball radius is invalid")
    for flag in (
        "target_source_manifest_validated",
        "separator_source_manifest_validated",
        "shared_gain_box_and_model_validated",
        "exact_block_diagonal_reset_column_validated",
        "midpoint_singular_value_block_transfer_validated",
        "derivative_defect_block_transfer_validated",
        "three_dimensional_input_ball_contained",
        "unique_input_for_each_certified_target_validated",
        "frequency_squared_range_operational_margin_target_ball_validated",
        "same_baseline_staged_protocol_validated",
    ):
        _require_true(certificate, flag)
    for flag in (
        "unsquared_amplitude_validated",
        "physical_finite_pulse_validated",
        "biological_basin_beyond_channel_faces_validated",
        "noise_hardware_robustness_validated",
        "unforced_onset_validated",
        "maximal_canard_onset_validated",
        "periodic_attraction_validated",
        "general_topology_validated",
        "issue_15_closed",
    ):
        _require_false(certificate, flag)
    expected_scope = set(_TRUE_RESULT_SCOPE) | set(_FALSE_RESULT_SCOPE)
    if set(scope) != expected_scope:
        raise ValueError("result scope keys are missing or unexpected")
    for flag in _TRUE_RESULT_SCOPE:
        _require_true(scope, flag)
    for flag in _FALSE_RESULT_SCOPE:
        _require_false(scope, flag)


def load_same_model_three_output_result(
    path: str | Path,
    *,
    expected_sha256: str,
) -> Mapping[str, Any]:
    """Hash-check and semantically validate a generated result artifact."""

    payload, _ = _load_json_with_hash(
        Path(path), expected_sha256, "three-output result"
    )
    validate_same_model_three_output_result_payload(payload)
    return payload
