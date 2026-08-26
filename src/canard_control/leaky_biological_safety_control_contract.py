"""Biological frequency--amplitude--safety control contract.

This module composes four already validated interfaces:

* the outer periodic (F,A) target ball;
* the fixed-common-time wide physical-pulse parameter family;
* the source-bound Stage-5C Route-C event and complete-history tube; and
* the conditional Dobrushin threshold-shift and safety guard.

The algebraic control theorems below are exact.  Stage-5C now supplies a
unique transverse Route-C event in one declared bracket, a fourth-order
event-time graph tube, and a continuous common-event complete-history tube.
It supplies no stable-coordinate signs, interval-Newton root, physical onset,
or routed capture.  Hence the current leaky model still has no validated
event-aligned biological threshold J_c or Lipschitz bound for it, and every
numerical three-output biological-control flag remains false.  This refusal is
part of the certificate.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
import platform
from typing import Any, Mapping

from canard_control.leaky_dobrushin_async_routing_transfer import (
    RESULT_RELATIVE_PATH as ASYNC_RESULT_RELATIVE_PATH,
)
from canard_control.leaky_periodic_directed_response import (
    RESULT_RELATIVE_PATH as PERIODIC_RESULT_RELATIVE_PATH,
)
from canard_control.leaky_pulse_parameter_jet_directed_enclosure import (
    RESULT_RELATIVE_PATH as PULSE_JET_RESULT_RELATIVE_PATH,
)


SCHEMA_ID = "leaky-biological-safety-control-contract-v2"
SOURCE_RELATIVE_PATH = (
    "src/canard_control/leaky_biological_safety_control_contract.py"
)
GENERATOR_RELATIVE_PATH = (
    "experiments/leaky_biological_safety_control_contract.py"
)
NOTE_RELATIVE_PATH = "docs/leaky-biological-safety-control-contract.md"
RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_biological_safety_control_contract.json"
)
TEST_RELATIVE_PATH = "tests/test_leaky_biological_safety_control_contract.py"
ROUTE_C_EVENT_PARENT_RELATIVE_PATH = (
    "experiments/results/leaky_pulse_route_c_event_stage5c.json"
)
ROUTE_C_EVENT_PARENT_RESULT_SHA256 = (
    "f1f198d68cb736bc9b5a48a0bff3eb5a93d39ee3f0b8f7cb6f7e07779483128d"
)
ROUTE_C_EVENT_PARENT_CERTIFICATE_SHA256 = (
    "6fc2db81bfed3864aabafa0f46b76d3ca67db12ee54e483f0472c4923b66aa5e"
)
DEFAULT_COMMAND = (
    "PYTHONPATH=src /usr/bin/python3 "
    "experiments/leaky_biological_safety_control_contract.py"
)
ARITHMETIC_SCOPE = (
    "exact rational composition of validated parent decimals and exact "
    "block-triangular, product-target, pulse-containment, and safety-erosion "
    "inequalities, plus source-bound transcription of exactly six Stage-5C "
    "event-side outputs; no stable-sheet, onset, routing, capture, or "
    "event-aligned J_c data are inserted"
)

PROVED_FLAGS = (
    "outer_frequency_amplitude_parent_validated",
    "fixed_time_wide_pulse_parent_validated",
    "conditional_async_safety_parent_validated",
    "block_triangular_determinant_identity_proved",
    "threshold_adapted_product_bijection_proved",
    "rectangular_target_radius_formula_proved",
    "euclidean_inverse_shear_bound_proved",
    "pulse_interval_containment_formula_proved",
    "network_safety_erosion_formula_proved",
)

OPEN_FLAGS = (
    "event_aligned_biological_threshold_validated",
    "biological_threshold_parameter_lipschitz_validated",
    "stable_coordinate_endpoint_signs_validated",
    "interval_newton_onset_validated",
    "unique_physical_pulse_onset_validated",
    "two_sided_biological_routing_validated",
    "outer_or_quiet_capture_from_both_sides_validated",
    "outer_attraction_tube_validated",
    "three_output_biological_target_radius_certified",
    "concrete_asynchronous_threshold_shift_certified",
    "concrete_network_robust_safety_radius_certified",
    "frequency_amplitude_biological_safety_controllability_validated",
)


def _mapping(value: Any, label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{label} must be a mapping")
    return value


def _positive(value: Fraction | int | str, label: str) -> Fraction:
    result = Fraction(value)
    if result <= 0:
        raise ValueError(f"{label} must be strictly positive")
    return result


def _nonnegative(value: Fraction | int | str, label: str) -> Fraction:
    result = Fraction(value)
    if result < 0:
        raise ValueError(f"{label} must be nonnegative")
    return result


def adapted_product_target_radius_lower(
    frequency_amplitude_radius: Fraction | int | str,
    safety_half_width: Fraction | int | str,
) -> Fraction:
    """Return the exact Euclidean inner radius of the adapted product image."""

    return min(
        _positive(frequency_amplitude_radius, "frequency_amplitude_radius"),
        _positive(safety_half_width, "safety_half_width"),
    )


def rectangular_target_radius_lower(
    frequency_amplitude_radius: Fraction | int | str,
    parameter_radius: Fraction | int | str,
    pulse_radius: Fraction | int | str,
    frequency_amplitude_inverse_lipschitz: Fraction | int | str,
    threshold_parameter_lipschitz: Fraction | int | str,
) -> Fraction:
    """Return the exact sufficient three-output radius in a product box."""

    rho_fa = _positive(
        frequency_amplitude_radius, "frequency_amplitude_radius"
    )
    radius_xi = _positive(parameter_radius, "parameter_radius")
    radius_j = _positive(pulse_radius, "pulse_radius")
    inverse = _positive(
        frequency_amplitude_inverse_lipschitz,
        "frequency_amplitude_inverse_lipschitz",
    )
    threshold = _nonnegative(
        threshold_parameter_lipschitz,
        "threshold_parameter_lipschitz",
    )
    return min(
        rho_fa,
        radius_xi / inverse,
        radius_j / (threshold * inverse + 1),
    )


def euclidean_target_radius_holds(
    target_radius: Fraction | int | str,
    frequency_amplitude_radius: Fraction | int | str,
    input_radius: Fraction | int | str,
    frequency_amplitude_inverse_lipschitz: Fraction | int | str,
    threshold_parameter_lipschitz: Fraction | int | str,
) -> bool:
    """Check a rational Frobenius upper bound for a Euclidean input ball."""

    rho = _positive(target_radius, "target_radius")
    rho_fa = _positive(
        frequency_amplitude_radius, "frequency_amplitude_radius"
    )
    radius = _positive(input_radius, "input_radius")
    inverse = _positive(
        frequency_amplitude_inverse_lipschitz,
        "frequency_amplitude_inverse_lipschitz",
    )
    threshold = _nonnegative(
        threshold_parameter_lipschitz,
        "threshold_parameter_lipschitz",
    )
    inverse_squared_upper = inverse * inverse * (
        1 + threshold * threshold
    ) + 1
    return rho <= rho_fa and rho * rho * inverse_squared_upper <= radius * radius


def pulse_interval_containment_holds(
    center_pulse: Fraction | int | str,
    target_radius: Fraction | int | str,
    frequency_amplitude_inverse_lipschitz: Fraction | int | str,
    threshold_parameter_lipschitz: Fraction | int | str,
    pulse_lower: Fraction | int | str,
    pulse_upper: Fraction | int | str,
) -> bool:
    """Check that every reconstructed pulse remains in the validated interval."""

    center = Fraction(center_pulse)
    rho = _nonnegative(target_radius, "target_radius")
    inverse = _positive(
        frequency_amplitude_inverse_lipschitz,
        "frequency_amplitude_inverse_lipschitz",
    )
    threshold = _nonnegative(
        threshold_parameter_lipschitz,
        "threshold_parameter_lipschitz",
    )
    lower = Fraction(pulse_lower)
    upper = Fraction(pulse_upper)
    if not lower < center < upper:
        raise ValueError("center_pulse must lie strictly inside the interval")
    excursion = (threshold * inverse + 1) * rho
    return center - excursion >= lower and center + excursion <= upper


def threshold_shift_upper(
    gap_value_error: Fraction | int | str,
    scalar_gap_slope: Fraction | int | str,
) -> Fraction:
    """Return the exact monotone-root shift epsilon_H/m_J."""

    error = _nonnegative(gap_value_error, "gap_value_error")
    slope = _positive(scalar_gap_slope, "scalar_gap_slope")
    return error / slope


def robust_safety_side_holds(
    safety_center: Fraction | int | str,
    safety_target_radius: Fraction | int | str,
    threshold_shift: Fraction | int | str,
    actuator_error: Fraction | int | str,
) -> bool:
    """Check strict sign preservation for an entire commanded safety ball."""

    center = abs(Fraction(safety_center))
    radius = _nonnegative(safety_target_radius, "safety_target_radius")
    shift = _nonnegative(threshold_shift, "threshold_shift")
    actuator = _nonnegative(actuator_error, "actuator_error")
    return center > radius + shift + actuator


def _sha256_path(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def canonical_sha256(value: Any) -> str:
    return sha256(
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
        ).encode("ascii")
    ).hexdigest()


def _json_ready(value: Any) -> Any:
    return json.loads(json.dumps(value, sort_keys=True))


def _load_parent(
    repository: Path,
    relative: str,
) -> Mapping[str, Any]:
    payload = json.loads((repository / relative).read_text(encoding="utf-8"))
    parent = _mapping(payload, relative)
    certificate = _mapping(parent.get("certificate"), f"{relative} certificate")
    manifest = _mapping(parent.get("manifest"), f"{relative} manifest")
    if manifest.get("certificate_sha256") != canonical_sha256(certificate):
        raise ValueError(f"{relative} has a stale certificate hash")
    return parent


def _load_stage5c_parent(repository: Path) -> Mapping[str, Any]:
    path = repository / ROUTE_C_EVENT_PARENT_RELATIVE_PATH
    if _sha256_path(path) != ROUTE_C_EVENT_PARENT_RESULT_SHA256:
        raise ValueError("the Stage-5C parent result SHA changed")
    parent = _load_parent(repository, ROUTE_C_EVENT_PARENT_RELATIVE_PATH)
    certificate = _mapping(parent.get("certificate"), "Stage-5C certificate")
    manifest = _mapping(parent.get("manifest"), "Stage-5C manifest")
    if canonical_sha256(certificate) != ROUTE_C_EVENT_PARENT_CERTIFICATE_SHA256:
        raise ValueError("the Stage-5C parent certificate SHA changed")
    if (
        manifest.get("certificate_sha256")
        != ROUTE_C_EVENT_PARENT_CERTIFICATE_SHA256
    ):
        raise ValueError("the Stage-5C parent manifest certificate SHA changed")
    return parent


@dataclass(frozen=True)
class BiologicalSafetyControlContract:
    schema_id: str
    model_id: str
    control_order: tuple[str, str, str]
    output_order: tuple[str, str, str]
    biological_safety_definition: str
    exact_control_map: str
    exact_jacobian_factorization: str
    exact_inverse_factorization: str
    threshold_adapted_domain: str
    threshold_adapted_image: str
    rectangular_target_radius_formula: str
    euclidean_inverse_squared_upper_formula: str
    pulse_interval_containment_formula: str
    network_threshold_shift_formula: str
    network_safety_guard_formula: str
    outer_frequency_amplitude_inverse_lipschitz_upper: str
    outer_frequency_amplitude_target_radius_lower: str
    validated_fixed_time_pulse_interval: tuple[str, str]
    validated_fixed_time_remainder_P_radius_upper: str
    validated_route_c_exact_section_level: dict[str, str]
    validated_route_c_parameter_interval_exact: str
    validated_route_c_unique_declared_bracket_event: dict[str, Any]
    validated_route_c_positive_event_speed: tuple[str, str]
    validated_route_c_order_four_event_time_graph_remainder_upper: str
    validated_route_c_common_event_Y_tube: dict[str, Any]
    validated_event_aligned_threshold_Jc: str | None
    validated_threshold_parameter_lipschitz: str | None
    validated_stable_coordinate_endpoint_signs: dict[str, Any] | None
    validated_interval_newton_image: tuple[str, str] | None
    validated_physical_pulse_onset: str | None
    validated_two_sided_biological_routing: dict[str, Any] | None
    validated_outer_or_quiet_capture_from_both_sides: dict[str, Any] | None
    validated_scalar_gap_slope: str | None
    validated_network_gap_error: str | None
    validated_actuator_error: str | None
    certified_three_output_biological_radius: str | None
    certified_network_threshold_shift: str | None
    certified_network_robust_safety_radius: str | None
    strict_scope_boundary: str
    outer_frequency_amplitude_parent_validated: bool
    fixed_time_wide_pulse_parent_validated: bool
    conditional_async_safety_parent_validated: bool
    block_triangular_determinant_identity_proved: bool
    threshold_adapted_product_bijection_proved: bool
    rectangular_target_radius_formula_proved: bool
    euclidean_inverse_shear_bound_proved: bool
    pulse_interval_containment_formula_proved: bool
    network_safety_erosion_formula_proved: bool
    event_aligned_biological_threshold_validated: bool
    biological_threshold_parameter_lipschitz_validated: bool
    stable_coordinate_endpoint_signs_validated: bool
    interval_newton_onset_validated: bool
    unique_physical_pulse_onset_validated: bool
    two_sided_biological_routing_validated: bool
    outer_or_quiet_capture_from_both_sides_validated: bool
    outer_attraction_tube_validated: bool
    three_output_biological_target_radius_certified: bool
    concrete_asynchronous_threshold_shift_certified: bool
    concrete_network_robust_safety_radius_certified: bool
    frequency_amplitude_biological_safety_controllability_validated: bool


def build_biological_safety_control_contract(
    repository: Path,
) -> BiologicalSafetyControlContract:
    periodic = _load_parent(
        repository,
        PERIODIC_RESULT_RELATIVE_PATH,
    )
    pulse = _load_parent(
        repository,
        PULSE_JET_RESULT_RELATIVE_PATH,
    )
    async_parent = _load_parent(
        repository,
        ASYNC_RESULT_RELATIVE_PATH,
    )
    route_c_event = _load_stage5c_parent(repository)

    periodic_certificate = _mapping(periodic.get("certificate"), "periodic")
    pulse_certificate = _mapping(pulse.get("certificate"), "pulse")
    pulse_claims = _mapping(
        pulse_certificate.get("claim_status"), "pulse claim_status"
    )
    async_certificate = _mapping(
        async_parent.get("certificate"), "asynchronous"
    )
    route_c_event_certificate = _mapping(
        route_c_event.get("certificate"), "Stage-5C event"
    )
    route_c_event_claims = _mapping(
        route_c_event_certificate.get("claim_status"),
        "Stage-5C event claim_status",
    )
    remainder = _mapping(
        pulse_certificate.get("full_width_order_five_remainder"),
        "pulse remainder",
    )
    scaling = _mapping(
        pulse_certificate.get("parameter_scaling"), "pulse scaling"
    )

    if not periodic_certificate.get(
        "uniform_pointwise_local_diffeomorphisms_validated"
    ):
        raise ValueError("the periodic parent has no validated local inverse")
    if not periodic_certificate.get(
        "response_determinants_bounded_away_from_zero"
    ):
        raise ValueError("the periodic parent determinant is not separated")
    if not pulse_claims.get(
        "fixed_time_wide_parameter_taylor_model_validated"
    ):
        raise ValueError("the fixed-time wide pulse parent is not validated")
    if not pulse_claims.get(
        "full_width_order_five_remainder_tube_closed_on_all_cells"
    ):
        raise ValueError("the full-width pulse remainder is not validated")
    if not async_certificate.get("conditional_safety_guard_formula_proved"):
        raise ValueError("the asynchronous safety parent is incomplete")

    required_event_claims = (
        "route_c_exact_phase_zero_level_source_bound",
        "wide_parameter_event_bracket_endpoint_signs_validated",
        "uniform_positive_event_speed_on_whole_event_bracket_validated",
        "one_and_only_one_route_c_event_in_declared_bracket_for_every_J_validated",
        "uniform_fourth_order_event_time_graph_remainder_validated",
        "common_event_complete_history_pullback_defined_in_Y",
        "common_event_complete_history_tube_validated",
    )
    for claim in required_event_claims:
        if route_c_event_claims.get(claim) is not True:
            raise ValueError(f"the Stage-5C event claim is unavailable: {claim}")
    required_open_event_claims = (
        "inner_local_stable_graph_validated",
        "stable_coordinate_endpoint_signs_validated",
        "stable_gap_derivative_excludes_zero_validated",
        "interval_newton_onset_validated",
        "unique_physical_pulse_onset_validated",
        "two_sided_basin_routing_validated",
        "outer_or_quiet_capture_from_both_sides_validated",
    )
    for claim in required_open_event_claims:
        if route_c_event_claims.get(claim) is not False:
            raise ValueError(f"the Stage-5C open boundary changed: {claim}")

    interval_exact = scaling.get("interval_exact")
    if interval_exact != "[6021/20000,753/2500]":
        raise ValueError("the pulse parent interval is malformed")
    if route_c_event_certificate.get("parameter_interval_exact") != interval_exact:
        raise ValueError("the fixed-time and event parameter intervals differ")

    route_c_section = _mapping(
        route_c_event_certificate.get("route_c_section"),
        "Stage-5C Route-C section",
    )
    if route_c_section.get("formula") != "h_C(phi)=phi_v(0)-V_true(0)":
        raise ValueError("the Stage-5C Route-C section formula changed")
    section_level = _mapping(
        route_c_section.get("phase_zero_voltage_level"),
        "Stage-5C exact section level",
    )
    if section_level != {
        "lower": (
            "0.905383843282120025506287674943450838327407828420353068999752401"
        ),
        "upper": (
            "0.905403843282120025506287674943450838327407845269557922000191891"
        ),
    }:
        raise ValueError("the Stage-5C exact-orbit section level changed")
    uniform_event = _mapping(
        route_c_event_certificate.get("uniform_event_bracket"),
        "Stage-5C uniform event bracket",
    )
    event_speed = _mapping(
        uniform_event.get("voltage_event_speed_on_whole_bracket"),
        "Stage-5C event speed",
    )
    event_time_model = _mapping(
        route_c_event_certificate.get("uniform_event_time_model"),
        "Stage-5C event-time model",
    )
    common_event_history = _mapping(
        route_c_event_certificate.get("common_event_complete_history"),
        "Stage-5C common-event history",
    )

    return BiologicalSafetyControlContract(
        schema_id=SCHEMA_ID,
        model_id="autonomous-leaky-recovery-two-delay-rfde",
        control_order=("unfolding_a", "kappa_3", "physical_pulse_J"),
        output_order=(
            "outer_frequency_F",
            "outer_unsquared_voltage_amplitude_A",
            "biological_safety_S=J-J_c",
        ),
        biological_safety_definition=(
            "S=J-J_c(xi), where J_c is the unique event-aligned "
            "stable-sheet crossing with two-sided biological basin routing"
        ),
        exact_control_map="Q(xi,J)=(P(xi),J-J_c(xi)); P=(F,A)",
        exact_jacobian_factorization=(
            "DQ=[[B,0],[-c^T,1]], B=D_xi(F,A), c=D_xi J_c; det DQ=det B"
        ),
        exact_inverse_factorization=(
            "DQ^{-1}=[[B^{-1},0],[c^T B^{-1},1]]"
        ),
        threshold_adapted_domain=(
            "{(xi,J): xi in U, |J-J_c(xi)-S0|<sigma}"
        ),
        threshold_adapted_image=(
            "P(U) times (S0-sigma,S0+sigma), bijectively when P is bijective"
        ),
        rectangular_target_radius_formula=(
            "rho<=min(rho_FA,R_xi/K,R_J/(L_c*K+1))"
        ),
        euclidean_inverse_squared_upper_formula=(
            "||DQ^{-1}||_2^2<=lambda_max([[K^2(1+L_c^2),"
            "L_c*K],[L_c*K,1]])<=K^2(1+L_c^2)+1"
        ),
        pulse_interval_containment_formula=(
            "J0 +/- (L_c*K+1)*rho lies in [J_minus,J_plus]"
        ),
        network_threshold_shift_formula="Delta_J=epsilon_H/m_J",
        network_safety_guard_formula=(
            "|S0|-rho_S>Delta_J+e_J for an entire routed target ball"
        ),
        outer_frequency_amplitude_inverse_lipschitz_upper=str(
            periodic_certificate[
                "flagship_outer_parameter_inverse_lipschitz_upper"
            ]
        ),
        outer_frequency_amplitude_target_radius_lower=str(
            periodic_certificate["flagship_outer_target_ball_radius_lower"]
        ),
        validated_fixed_time_pulse_interval=(
            "6021/20000",
            "753/2500",
        ),
        validated_fixed_time_remainder_P_radius_upper=str(
            remainder["maximum_P_radius_upper"]
        ),
        validated_route_c_exact_section_level={
            "formula": str(route_c_section["formula"]),
            "lower": str(section_level["lower"]),
            "upper": str(section_level["upper"]),
        },
        validated_route_c_parameter_interval_exact=str(interval_exact),
        validated_route_c_unique_declared_bracket_event={
            "left_time_exact": str(uniform_event["left_time_exact"]),
            "right_time_exact": str(uniform_event["right_time_exact"]),
            "uniqueness_statement": str(uniform_event["uniqueness_statement"]),
            "ordinal_scope": str(uniform_event["ordinal_scope"]),
        },
        validated_route_c_positive_event_speed=(
            str(event_speed["lower"]),
            str(event_speed["upper"]),
        ),
        validated_route_c_order_four_event_time_graph_remainder_upper=str(
            event_time_model["event_time_remainder_upper"]
        ),
        validated_route_c_common_event_Y_tube={
            "phase_space": str(common_event_history["phase_space"]),
            "Y_max_radius_upper": str(
                common_event_history["Y_max_radius_upper"]
            ),
        },
        validated_event_aligned_threshold_Jc=None,
        validated_threshold_parameter_lipschitz=None,
        validated_stable_coordinate_endpoint_signs=None,
        validated_interval_newton_image=None,
        validated_physical_pulse_onset=None,
        validated_two_sided_biological_routing=None,
        validated_outer_or_quiet_capture_from_both_sides=None,
        validated_scalar_gap_slope=None,
        validated_network_gap_error=None,
        validated_actuator_error=None,
        certified_three_output_biological_radius=None,
        certified_network_threshold_shift=None,
        certified_network_robust_safety_radius=None,
        strict_scope_boundary=(
            "The outer (F,A) inverse, fixed-time pulse family, unique "
            "declared-bracket Route-C event, order-four event-time graph "
            "remainder, and continuous common-event Y tube are validated. "
            "They do not supply stable-coordinate endpoint signs, an "
            "interval-Newton onset, event-aligned J_c, D_xi J_c, a physical "
            "onset, two-sided biological routing or capture, an outer "
            "attraction tube, or a concrete asynchronous gap error."
        ),
        outer_frequency_amplitude_parent_validated=True,
        fixed_time_wide_pulse_parent_validated=True,
        conditional_async_safety_parent_validated=True,
        block_triangular_determinant_identity_proved=True,
        threshold_adapted_product_bijection_proved=True,
        rectangular_target_radius_formula_proved=True,
        euclidean_inverse_shear_bound_proved=True,
        pulse_interval_containment_formula_proved=True,
        network_safety_erosion_formula_proved=True,
        event_aligned_biological_threshold_validated=False,
        biological_threshold_parameter_lipschitz_validated=False,
        stable_coordinate_endpoint_signs_validated=False,
        interval_newton_onset_validated=False,
        unique_physical_pulse_onset_validated=False,
        two_sided_biological_routing_validated=False,
        outer_or_quiet_capture_from_both_sides_validated=False,
        outer_attraction_tube_validated=False,
        three_output_biological_target_radius_certified=False,
        concrete_asynchronous_threshold_shift_certified=False,
        concrete_network_robust_safety_radius_certified=False,
        frequency_amplitude_biological_safety_controllability_validated=False,
    )


def validate_biological_safety_control_result(
    payload: Mapping[str, Any],
    repository: Path,
) -> None:
    certificate = _mapping(payload.get("certificate"), "certificate")
    manifest = _mapping(payload.get("manifest"), "manifest")
    if set(certificate) != {
        field.name for field in fields(BiologicalSafetyControlContract)
    }:
        raise ValueError("certificate schema changed")
    if certificate.get("schema_id") != SCHEMA_ID:
        raise ValueError("certificate schema_id changed")
    for flag in PROVED_FLAGS:
        if certificate.get(flag) is not True:
            raise ValueError(f"proved flag weakened: {flag}")
    for flag in OPEN_FLAGS:
        if certificate.get(flag) is not False:
            raise ValueError(f"open biological-control flag promoted: {flag}")
    for field in (
        "validated_event_aligned_threshold_Jc",
        "validated_threshold_parameter_lipschitz",
        "validated_stable_coordinate_endpoint_signs",
        "validated_interval_newton_image",
        "validated_physical_pulse_onset",
        "validated_two_sided_biological_routing",
        "validated_outer_or_quiet_capture_from_both_sides",
        "validated_scalar_gap_slope",
        "validated_network_gap_error",
        "validated_actuator_error",
        "certified_three_output_biological_radius",
        "certified_network_threshold_shift",
        "certified_network_robust_safety_radius",
    ):
        if certificate.get(field) is not None:
            raise ValueError(f"unvalidated biological field inserted: {field}")

    if manifest.get("schema_id") != SCHEMA_ID:
        raise ValueError("manifest schema_id changed")
    if manifest.get("certificate_sha256") != canonical_sha256(certificate):
        raise ValueError("certificate hash changed")
    expected_paths = {
        "source": SOURCE_RELATIVE_PATH,
        "generator": GENERATOR_RELATIVE_PATH,
        "note": NOTE_RELATIVE_PATH,
        "test": TEST_RELATIVE_PATH,
        "periodic_parent": PERIODIC_RESULT_RELATIVE_PATH,
        "pulse_jet_parent": PULSE_JET_RESULT_RELATIVE_PATH,
        "route_c_event_parent": ROUTE_C_EVENT_PARENT_RELATIVE_PATH,
        "async_parent": ASYNC_RESULT_RELATIVE_PATH,
    }
    for label, relative in expected_paths.items():
        if manifest.get(label) != relative:
            raise ValueError(f"manifest path changed: {label}")
        if manifest.get(f"{label}_sha256") != _sha256_path(
            repository / relative
        ):
            raise ValueError(f"manifest hash changed: {label}")
    if manifest.get("arithmetic_scope") != ARITHMETIC_SCOPE:
        raise ValueError("arithmetic scope changed")
    if (
        manifest.get("route_c_event_parent_sha256")
        != ROUTE_C_EVENT_PARENT_RESULT_SHA256
    ):
        raise ValueError("Stage-5C parent result binding changed")
    if (
        manifest.get("route_c_event_parent_certificate_sha256")
        != ROUTE_C_EVENT_PARENT_CERTIFICATE_SHA256
    ):
        raise ValueError("Stage-5C parent certificate binding changed")
    expected = _json_ready(
        asdict(build_biological_safety_control_contract(repository))
    )
    if certificate != expected:
        raise ValueError("certificate differs from the exact parent replay")


def make_payload(repository: Path) -> dict[str, Any]:
    certificate = _json_ready(
        asdict(build_biological_safety_control_contract(repository))
    )
    paths = {
        "source": SOURCE_RELATIVE_PATH,
        "generator": GENERATOR_RELATIVE_PATH,
        "note": NOTE_RELATIVE_PATH,
        "test": TEST_RELATIVE_PATH,
        "periodic_parent": PERIODIC_RESULT_RELATIVE_PATH,
        "pulse_jet_parent": PULSE_JET_RESULT_RELATIVE_PATH,
        "route_c_event_parent": ROUTE_C_EVENT_PARENT_RELATIVE_PATH,
        "async_parent": ASYNC_RESULT_RELATIVE_PATH,
    }
    manifest: dict[str, Any] = {
        "schema_id": SCHEMA_ID,
        "certificate_sha256": canonical_sha256(certificate),
        "default_command": DEFAULT_COMMAND,
        "arithmetic_scope": ARITHMETIC_SCOPE,
        "python": platform.python_version(),
        "platform": platform.platform(),
        "route_c_event_parent_certificate_sha256": (
            ROUTE_C_EVENT_PARENT_CERTIFICATE_SHA256
        ),
    }
    for label, relative in paths.items():
        manifest[label] = relative
        manifest[f"{label}_sha256"] = _sha256_path(repository / relative)
    return {"certificate": certificate, "manifest": manifest}


__all__ = [
    "ARITHMETIC_SCOPE",
    "DEFAULT_COMMAND",
    "GENERATOR_RELATIVE_PATH",
    "NOTE_RELATIVE_PATH",
    "RESULT_RELATIVE_PATH",
    "ROUTE_C_EVENT_PARENT_CERTIFICATE_SHA256",
    "ROUTE_C_EVENT_PARENT_RELATIVE_PATH",
    "ROUTE_C_EVENT_PARENT_RESULT_SHA256",
    "SCHEMA_ID",
    "SOURCE_RELATIVE_PATH",
    "TEST_RELATIVE_PATH",
    "adapted_product_target_radius_lower",
    "build_biological_safety_control_contract",
    "canonical_sha256",
    "euclidean_target_radius_holds",
    "make_payload",
    "pulse_interval_containment_holds",
    "rectangular_target_radius_lower",
    "robust_safety_side_holds",
    "threshold_shift_upper",
    "validate_biological_safety_control_result",
]
