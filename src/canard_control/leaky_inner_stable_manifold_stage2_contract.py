"""Stage-2 ingress for a quantitative inner stable manifold.

Stage 1 records the qualitative codimension-one stable manifold and the
Lyapunov--Perron scalar majorant.  This module admits the independently
validated left-strip gap, separates a spectral-radius bound from a power
bound, and records every remaining constant needed for a quantitative
Poincare graph theorem.

Only consequences that follow from the bound parents are promoted.  In
particular, the periodic-BVP phase condition is not silently identified with
a functional on one RFDE history, and a zero-free Floquet strip is not
silently promoted to a Riesz-projection or dichotomy-norm bound.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from decimal import (
    Decimal,
    InvalidOperation,
    ROUND_CEILING,
    ROUND_FLOOR,
    localcontext,
)
from functools import lru_cache
from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Mapping

import gmpy2

from canard_control.directed_interval import (
    DirectedInterval,
    decimal_lower,
    decimal_upper,
    upward_sum,
)
from canard_control.fhn_periodic_infinite_validation import (
    _sequence_box_norm_upper,
)
from canard_control.leaky_floquet_transfer import (
    load_validated_leaky_orbit_evidence,
)
from canard_control.leaky_inner_stable_manifold_stage1_contract import (
    StableGraphInputBudget,
    TARGET_STABLE_SEED_RADIUS,
    evaluate_lyapunov_perron_majorant,
    validate_stage1_stable_manifold_result,
)
from canard_control.leaky_periodic_validation import (
    _build_leaky_base_sequences,
)
from canard_control.rfde_floquet_transfer import (
    _residual_sequence_norm_upper,
    _state_sequence_norm_upper,
)


SCHEMA_ID = "leaky-inner-stable-manifold-stage2-contract-v1"
MODEL_ID = "autonomous-leaky-recovery-two-delay-fhn-bistable-proposal"
BRANCH = "inner_saddle_candidate"

SOURCE_RELATIVE_PATH = (
    "src/canard_control/leaky_inner_stable_manifold_stage2_contract.py"
)
GENERATOR_RELATIVE_PATH = (
    "experiments/leaky_inner_stable_manifold_stage2_contract.py"
)
RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_inner_stable_manifold_stage2_contract.json"
)
NOTE_RELATIVE_PATH = (
    "docs/leaky-inner-stable-manifold-stage2-contract.md"
)
TEST_RELATIVE_PATH = (
    "tests/test_leaky_inner_stable_manifold_stage2_contract.py"
)

STAGE1_RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_inner_stable_manifold_stage1_contract.json"
)
BASE_STABLE_GAP_RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_floquet_inner_stable_gap.json"
)
STRONG_STABLE_GAP_RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_floquet_inner_strong_stable_gap.json"
)
FLOQUET_TRANSFER_RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_floquet_transfer.json"
)
PULSE_TARGET_RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_pulse_separator_validation_target.json"
)
PULSE_CANDIDATE_RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_pulse_separator_candidate.json"
)

STAGE1_RESULT_SHA256 = (
    "3c400ec92f00d4c94313b6e0a5b514f60f21335f54cba41ad5ba8a4217e8f21b"
)
BASE_STABLE_GAP_RESULT_SHA256: str | None = (
    "9180fd43b6c19d8c6d8ee1e34a88cbdaee714a7f784b5ce862625a9f8015190a"
)
STRONG_STABLE_GAP_RESULT_SHA256: str | None = (
    "e61792cd946103b33da8209cae1c3123baa07b14aa6ccef4ae63b1c9a14848cc"
)
FLOQUET_TRANSFER_RESULT_SHA256 = (
    "5a3709ec792b29ed41533101245b13b3d35084ae508bdd1d420728200a5a5b16"
)
INNER_ORBIT_RESULT_SHA256 = (
    "bee1da065d213c3c33d724ced1dba37c5914934515c1128588919bed34abe69b"
)
PULSE_TARGET_RESULT_SHA256 = (
    "175a03bad09c81c9289ee5747d870113c6afcc22b1ec23942379c4c81bcda917"
)
PULSE_CANDIDATE_RESULT_SHA256 = (
    "9313ed2b07e285eedd30920853f69c1981c3a409339d316262e8621dfb8ffc85"
)

SOURCE_MANIFEST = (
    SOURCE_RELATIVE_PATH,
    GENERATOR_RELATIVE_PATH,
    NOTE_RELATIVE_PATH,
)

DEFAULT_COMMAND = (
    "PYTHONPATH=build/testdeps:src /usr/bin/python3 "
    "experiments/leaky_inner_stable_manifold_stage2_contract.py"
)
ARITHMETIC_SCOPE = (
    "exact parent-byte and source-manifest binding; 96-digit directed Decimal "
    "ingress of the baseline and strengthened stable spectral radii; exact "
    "midpoint strict power rates, directed beta-majorant optimization, and an "
    "explicit near-unit sequence weight; "
    "source-level phase-condition separation; and an executable affine-section "
    "return-C2 majorant"
)

RETURN_C2_REQUIRED_FIELDS = (
    "section_history_ball_radius_lower",
    "flow_history_tube_radius_lower",
    "return_time_lower",
    "return_time_upper",
    "phase_functional_norm_upper",
    "uniform_event_speed_lower",
    "section_defining_function_c2_upper",
    "section_chart_projection_norm_upper",
    "vector_field_norm_upper",
    "vector_field_d1_upper",
    "flow_d1_upper",
    "flow_d2_upper",
    "validated_return_map_ball_radius_lower",
)

QUANTITATIVE_FALSE_FLAGS = (
    "optimistic_unknown_norms_one_row_promoted_to_rfde_evidence",
    "stable_riesz_projection_norm_validated",
    "unstable_riesz_projection_norm_validated",
    "stable_dichotomy_constant_numeric_upper_validated",
    "phase_row_history_pullback_operator_norm_validated",
    "uniform_phase_section_speed_on_return_tube_validated",
    "continuous_history_flow_tube_validated",
    "poincare_return_c2_bound_validated",
    "nonlinear_remainder_bound_validated",
    "continuous_return_map_ball_validated",
    "lyapunov_perron_contraction_for_rfde_validated",
    "inner_local_stable_graph_quantitatively_validated",
    "specific_pulse_voltage_section_transversality_validated",
    "physical_pulse_separator_crossing_validated",
    "unique_physical_pulse_onset_validated",
    "two_sided_basin_routing_validated",
)


def _sha256_path(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def canonical_sha256(value: Any) -> str:
    encoded = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("ascii")
    return sha256(encoded).hexdigest()


def _json_normalize(value: Any) -> Any:
    return json.loads(
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        )
    )


def _decimal(value: str | None, name: str) -> Decimal | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError(f"{name} must be a decimal string or null")
    try:
        number = Decimal(value)
    except InvalidOperation as error:
        raise ValueError(f"{name} is not a decimal") from error
    if not number.is_finite():
        raise ValueError(f"{name} must be finite")
    return number


def _positive(value: Any, name: str) -> Decimal:
    number = _decimal(value if isinstance(value, str) else None, name)
    if number is None or number <= 0:
        raise ValueError(f"{name} must be a positive decimal string")
    return number


def _upper(value: Decimal) -> str:
    with localcontext() as context:
        context.prec = 96
        context.rounding = ROUND_CEILING
        return format(+value, "f")


def _lower(value: Decimal) -> str:
    with localcontext() as context:
        context.prec = 96
        context.rounding = ROUND_FLOOR
        return format(+value, "f")


def _mapping(value: Any, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{name} is missing")
    return value


def _validate_source_hashes(manifest: Mapping[str, Any], repository: Path) -> None:
    source_hashes = _mapping(manifest.get("source_sha256"), "source manifest")
    for relative, digest in source_hashes.items():
        if not isinstance(relative, str) or not isinstance(digest, str):
            raise ValueError("a bound source manifest is malformed")
        if _sha256_path(repository / relative) != digest:
            raise ValueError(f"a bound parent source changed: {relative}")


def _validate_named_parent_hashes(
    manifest: Mapping[str, Any], repository: Path
) -> None:
    for name, digest in manifest.items():
        if not name.endswith("_sha256") or name in {
            "certificate_sha256",
            "contract_sha256",
        }:
            continue
        relative = manifest.get(name[: -len("_sha256")])
        if isinstance(relative, str) and isinstance(digest, str):
            if _sha256_path(repository / relative) != digest:
                raise ValueError(f"a bound parent changed: {relative}")
    parent_hashes = manifest.get("parent_result_sha256")
    if parent_hashes is not None:
        for relative, digest in _mapping(
            parent_hashes, "parent digest map"
        ).items():
            if not isinstance(relative, str) or not isinstance(digest, str):
                raise ValueError("a bound parent digest map is malformed")
            if _sha256_path(repository / relative) != digest:
                raise ValueError(f"a bound parent changed: {relative}")


def _load_json(path: Path, expected_sha256: str, label: str) -> Mapping[str, Any]:
    raw = path.read_bytes()
    if sha256(raw).hexdigest() != expected_sha256:
        raise ValueError(f"the bound {label} result changed: {path}")
    payload = json.loads(raw)
    if not isinstance(payload, Mapping):
        raise ValueError(f"the bound {label} result is malformed")
    return payload


def _parent_hash_map() -> dict[str, str]:
    if BASE_STABLE_GAP_RESULT_SHA256 is None:
        raise RuntimeError("the final baseline stable-gap hash is not registered")
    if STRONG_STABLE_GAP_RESULT_SHA256 is None:
        raise RuntimeError("the final strengthened stable-gap hash is not registered")
    return {
        STAGE1_RESULT_RELATIVE_PATH: STAGE1_RESULT_SHA256,
        BASE_STABLE_GAP_RESULT_RELATIVE_PATH: BASE_STABLE_GAP_RESULT_SHA256,
        STRONG_STABLE_GAP_RESULT_RELATIVE_PATH: STRONG_STABLE_GAP_RESULT_SHA256,
    }


@dataclass(frozen=True)
class AffineReturnC2InputBudget:
    """Inputs for a C2 first-return bound on one affine history section."""

    section_history_ball_radius_lower: str | None
    flow_history_tube_radius_lower: str | None
    return_time_lower: str | None
    return_time_upper: str | None
    phase_functional_norm_upper: str | None
    uniform_event_speed_lower: str | None
    section_defining_function_c2_upper: str | None
    section_chart_projection_norm_upper: str | None
    vector_field_norm_upper: str | None
    vector_field_d1_upper: str | None
    flow_d1_upper: str | None
    flow_d2_upper: str | None
    validated_return_map_ball_radius_lower: str | None
    evidence_status: str


@dataclass(frozen=True)
class AffineReturnC2Majorant:
    input_complete: bool
    missing_inputs: tuple[str, ...]
    input_order_conditions_hold: bool
    return_time_d1_upper: str | None
    return_time_d2_upper: str | None
    poincare_return_c2_upper: str | None
    nonlinear_derivative_remainder_coefficient_upper: str | None
    return_ball_within_flow_tube: bool
    return_c2_majorant_closes: bool
    return_time_d1_formula: str
    return_time_d2_formula: str
    poincare_return_c2_formula: str
    nonlinear_remainder_formula: str


@dataclass(frozen=True)
class StableSpectralIngress:
    certificate_role: str
    used_for_stage1_partial_adapter: bool
    gamma_lower: str
    stable_spectrum_modulus_upper: str
    stable_spectrum_gap_to_unit_lower: str
    working_stable_power_rate_upper: str
    working_rate_minus_spectrum_upper_lower: str
    sequence_weight_beta: str
    sequence_weight_selection_formula: str
    beta_minus_working_rate_lower: str
    unstable_backward_rate_upper: str
    unstable_restriction_dimension: int
    unstable_dichotomy_constant_upper_intrinsic: str
    stable_dichotomy_constant_upper: str | None
    stable_power_constant_exists_qualitatively_at_working_rate: bool
    stable_power_constant_numeric_upper_validated: bool
    unstable_backward_power_bound_on_eigenline_validated: bool
    spectral_radius_bound_used_as_boundary_power_bound: bool
    midpoint_diagnostic_sequence_weight_beta: str
    midpoint_optimistic_kernel_with_all_unknown_norms_set_to_one: str
    midpoint_optimistic_critical_c_n_sufficient_threshold: str
    near_unit_diagnostic_sequence_weight_beta: str
    near_unit_diagnostic_sequence_weight_formula: str
    near_unit_stable_kernel_coefficient_upper: str
    near_unit_unstable_kernel_coefficient_upper: str
    near_unit_optimistic_kernel_with_all_unknown_norms_set_to_one: str
    near_unit_optimistic_critical_c_n_sufficient_threshold: str
    near_unit_optimistic_old_c_n_discriminant_lower: str
    near_unit_optimistic_old_c_n_discriminant_upper: str
    near_unit_optimistic_old_c_n_scalar_gate_closes: bool
    optimistic_kernel_beta_derivative_formula: str
    optimistic_stationary_beta_lower: str
    optimistic_stationary_beta_above_one_validated: bool
    optimistic_kernel_strictly_decreasing_on_admissible_beta_interval: bool
    fixed_working_beta_to_one_optimistic_kernel_infimum: str
    fixed_working_beta_to_one_critical_c_n_supremum_lower: str
    fixed_working_optimistic_old_c_n_window_possible: bool
    old_stage1_design_c_n: str
    general_scalar_feasibility_formula_at_selected_rates: str
    general_scalar_feasibility_budget_rhs: str


@dataclass(frozen=True)
class AbstractPhaseSectionAudit:
    periodic_bvp_phase_border_description: str
    periodic_bvp_bordered_inverse_norm_upper: str
    periodic_bvp_phase_pairing_abs_lower: str
    periodic_bvp_phase_normal_vector_norm_upper: str
    periodic_bvp_phase_functional_norm_upper: str
    periodic_bvp_phase_projection_norm_upper: str
    periodic_bvp_phase_condition_affine_c2_upper: str
    periodic_bvp_phase_condition_quantitatively_transverse: bool
    periodic_bvp_phase_functional_is_one_history_functional: bool
    phase_row_history_pullback_formula: str
    phase_row_history_pullback_exists_as_bounded_linear_functional: bool
    phase_row_history_pullback_operator_norm_upper: str | None
    phase_row_history_section_c2_upper: str
    phase_row_history_event_speed_at_orbit_lower: str
    phase_row_history_section_constructively_registered: bool
    nonconstant_fourier_mode_lower: str
    normalized_tangent_sup_norm_lower: str
    orbit_period_binary64_hex: str
    orbit_period_upper: str
    existential_history_coordinate_section_functional_norm_upper: str
    existential_history_coordinate_section_projection_norm_upper: str
    existential_history_coordinate_section_c2_upper: str
    existential_history_coordinate_event_speed_at_orbit_lower: str
    existential_history_coordinate_section_pointwise_transverse_proved: bool
    fourier_existence_argument_alone_registers_phase_and_component: bool
    uniform_event_speed_lower_on_return_tube: str | None
    uniform_event_speed_on_return_tube_validated: bool
    specific_pulse_voltage_section_speed_lower_validated: bool


@dataclass(frozen=True)
class ExplicitVoltageSectionAudit:
    exact_phase_zero_section_formula: str
    registered_pulse_section_description: str
    normalized_phase: str
    state_component: str
    same_history_evaluation_functional_as_registered_pulse_section: bool
    registered_pulse_section_level_binary64_hex: str
    registered_pulse_section_level_decimal: str
    registered_pulse_section_level_inside_phase_zero_orbit_value_enclosure: bool
    exact_section_level_equals_registered_pulse_section_level_validated: bool
    candidate_section_voltage_lower: str
    candidate_section_voltage_upper: str
    validated_orbit_section_voltage_lower: str
    validated_orbit_section_voltage_upper: str
    candidate_normalized_voltage_tangent_lower: str
    normalized_tangent_correction_upper: str
    validated_normalized_voltage_tangent_lower: str
    orbit_period_upper: str
    physical_voltage_event_speed_at_orbit_lower: str
    section_functional_norm_upper: str
    section_chart_projection_norm_upper: str
    section_defining_function_c2_upper: str
    unweighted_wiener_ball_directly_controls_derivative: bool
    rfde_vector_field_identity_closes_tangent_correction: bool
    additional_first_order_weighted_tail_bound_required_for_point_speed: bool
    pointwise_orbit_speed_validated: bool
    old_binary64_voltage_level_error_from_true_phase_zero_upper: str
    physical_orbit_history_speed_upper: str
    old_binary64_voltage_level_crossing_time_offset_upper: str
    old_binary64_voltage_level_crossing_phase_offset_upper: str
    orbit_history_displacement_over_local_crossing_bracket_upper: str
    local_crossing_bracket_within_declared_section_ball: bool
    old_binary64_voltage_level_local_orbit_crossing_speed_lower: str
    old_binary64_voltage_level_has_unique_local_true_orbit_crossing_validated: bool
    pulse_reshoot_required_before_route_c_target_can_be_used: bool
    tube_uniform_speed_reduction_formula: str
    declared_section_ball_radius: str
    vector_field_lipschitz_upper_on_declared_section_ball: str
    event_speed_variation_upper_on_declared_section_ball: str
    uniform_event_speed_lower_on_declared_section_ball: str
    uniform_event_speed_on_declared_section_ball_validated: bool
    uniform_event_speed_lower_on_return_tube: str | None
    uniform_event_speed_on_return_tube_validated: bool


@dataclass(frozen=True)
class Stage2StableManifoldContract:
    schema_id: str
    model_id: str
    branch: str
    phase_space: str
    history_norm: str
    parent_result_sha256: dict[str, str]
    baseline_gamma001_spectral_ingress: dict[str, Any]
    strengthened_gamma01_spectral_ingress: dict[str, Any]
    abstract_phase_section_audit: dict[str, Any]
    explicit_voltage_section_audit: dict[str, Any]
    riesz_projection_and_dichotomy_ledger: dict[str, Any]
    return_c2_actual_budget: dict[str, Any]
    return_c2_actual_evaluation: dict[str, Any]
    stage1_budget_after_stage2_ingress: dict[str, Any]
    stage1_majorant_after_stage2_ingress: dict[str, Any]
    next_certificate_interface: dict[str, Any]
    claim_status: dict[str, bool]


def evaluate_affine_return_c2_majorant(
    budget: AffineReturnC2InputBudget,
) -> AffineReturnC2Majorant:
    """Evaluate implicit-return and Poincare C2 bounds for an affine section."""

    values = asdict(budget)
    parsed = {
        field.name: _decimal(values[field.name], field.name)
        for field in fields(AffineReturnC2InputBudget)
        if field.name != "evidence_status"
    }
    missing = tuple(
        name for name in RETURN_C2_REQUIRED_FIELDS if values[name] is None
    )
    formulas = {
        "return_time_d1_formula": "tau_1=H*U_1/a",
        "return_time_d2_formula": (
            "tau_2=H*(U_2+2*F_1*U_1*tau_1+"
            "F_1*F_0*tau_1^2)/a"
        ),
        "poincare_return_c2_formula": (
            "M_2=Q*(U_2+2*F_1*U_1*tau_1+"
            "F_1*F_0*tau_1^2+F_0*tau_2)"
        ),
        "nonlinear_remainder_formula": (
            "C_N=M_2 gives ||DN(x)||<=C_N||x|| and "
            "||N(x)||<=C_N||x||^2/2"
        ),
    }
    if missing:
        return AffineReturnC2Majorant(
            input_complete=False,
            missing_inputs=missing,
            input_order_conditions_hold=False,
            return_time_d1_upper=None,
            return_time_d2_upper=None,
            poincare_return_c2_upper=None,
            nonlinear_derivative_remainder_coefficient_upper=None,
            return_ball_within_flow_tube=False,
            return_c2_majorant_closes=False,
            **formulas,
        )
    if any(number is None for number in parsed.values()):
        raise AssertionError("a complete return-C2 budget has null fields")
    numbers = {name: number for name, number in parsed.items() if number is not None}
    section_ball = numbers["section_history_ball_radius_lower"]
    flow_tube = numbers["flow_history_tube_radius_lower"]
    time_lower = numbers["return_time_lower"]
    time_upper = numbers["return_time_upper"]
    functional = numbers["phase_functional_norm_upper"]
    speed = numbers["uniform_event_speed_lower"]
    section_c2 = numbers["section_defining_function_c2_upper"]
    projection = numbers["section_chart_projection_norm_upper"]
    field_zero = numbers["vector_field_norm_upper"]
    field_one = numbers["vector_field_d1_upper"]
    flow_one = numbers["flow_d1_upper"]
    flow_two = numbers["flow_d2_upper"]
    return_ball = numbers["validated_return_map_ball_radius_lower"]
    positive = all(
        value > 0
        for value in (
            section_ball,
            flow_tube,
            time_lower,
            time_upper,
            functional,
            speed,
            projection,
            field_zero,
            field_one,
            flow_one,
            flow_two,
            return_ball,
        )
    )
    order = (
        positive
        and time_lower < time_upper
        and section_c2 == 0
        and projection >= 1
        and return_ball <= section_ball
        and return_ball <= flow_tube
    )
    if not order:
        raise ValueError(
            "the affine return-C2 budget violates time, positivity, section, "
            "projection, or tube conditions"
        )
    with localcontext() as context:
        context.prec = 96
        context.rounding = ROUND_CEILING
        tau_one = functional * flow_one / speed
        core = (
            flow_two
            + 2 * field_one * flow_one * tau_one
            + field_one * field_zero * tau_one * tau_one
        )
        tau_two = functional * core / speed
        return_c2 = projection * (core + field_zero * tau_two)
    return AffineReturnC2Majorant(
        input_complete=True,
        missing_inputs=(),
        input_order_conditions_hold=True,
        return_time_d1_upper=_upper(tau_one),
        return_time_d2_upper=_upper(tau_two),
        poincare_return_c2_upper=_upper(return_c2),
        nonlinear_derivative_remainder_coefficient_upper=_upper(return_c2),
        return_ball_within_flow_tube=True,
        return_c2_majorant_closes=True,
        **formulas,
    )


def _binary64_exact_decimal(record: Any, name: str) -> tuple[str, Decimal]:
    mapping = _mapping(record, name)
    if set(mapping) != {"binary64_hex", "decimal"}:
        raise ValueError(f"{name} is not an exact binary64 record")
    hexadecimal = mapping.get("binary64_hex")
    decimal_text = mapping.get("decimal")
    if not isinstance(hexadecimal, str) or not isinstance(decimal_text, str):
        raise ValueError(f"{name} is malformed")
    value = float.fromhex(hexadecimal)
    if format(value, ".17g") != decimal_text:
        raise ValueError(f"{name} decimal rendering changed")
    return hexadecimal, Decimal.from_float(value)


def _load_parents(
    repository: Path,
) -> tuple[
    Mapping[str, Any],
    Mapping[str, Any],
    Mapping[str, Any],
    Mapping[str, Any],
    Mapping[str, Any],
    Mapping[str, Any],
]:
    parent_hashes = _parent_hash_map()
    stage1 = _load_json(
        repository / STAGE1_RESULT_RELATIVE_PATH,
        parent_hashes[STAGE1_RESULT_RELATIVE_PATH],
        "Stage-1",
    )
    validate_stage1_stable_manifold_result(stage1, repository)
    base_gap = _load_json(
        repository / BASE_STABLE_GAP_RESULT_RELATIVE_PATH,
        parent_hashes[BASE_STABLE_GAP_RESULT_RELATIVE_PATH],
        "baseline stable-gap",
    )
    gap_manifest = _mapping(
        base_gap.get("manifest"), "baseline stable-gap manifest"
    )
    _validate_source_hashes(gap_manifest, repository)
    _validate_named_parent_hashes(gap_manifest, repository)
    gap_certificate = _mapping(
        base_gap.get("certificate"), "baseline stable-gap certificate"
    )
    if not (
        gap_certificate.get("quantitative_inner_stable_spectral_gap_validated")
        is True
        and gap_certificate.get("poincare_stable_spectral_radius_bound_validated")
        is True
        and gap_certificate.get("source_validated_compact_history_monodromy_used")
        is True
        and gap_certificate.get(
            "history_spectrum_to_fourier_characteristic_values_bridge_used"
        )
        is True
        and gap_certificate.get("binary_blas_thread_count") == 1
        and gap_certificate.get("stable_spectral_projection_constructed") is False
        and gap_certificate.get("inner_stable_manifold_validated") is False
    ):
        raise ValueError("the stable-gap theorem boundary is incomplete")

    strong_gap = _load_json(
        repository / STRONG_STABLE_GAP_RESULT_RELATIVE_PATH,
        parent_hashes[STRONG_STABLE_GAP_RESULT_RELATIVE_PATH],
        "strengthened stable-gap",
    )
    strong_manifest = _mapping(
        strong_gap.get("manifest"), "strengthened stable-gap manifest"
    )
    _validate_source_hashes(strong_manifest, repository)
    _validate_named_parent_hashes(strong_manifest, repository)
    if (
        strong_manifest.get("base_gap_result")
        != BASE_STABLE_GAP_RESULT_RELATIVE_PATH
        or strong_manifest.get("base_gap_result_sha256")
        != BASE_STABLE_GAP_RESULT_SHA256
    ):
        raise ValueError("the strengthened theorem's baseline parent changed")
    strong_certificate = _mapping(
        strong_gap.get("certificate"), "strengthened stable-gap certificate"
    )
    if not (
        strong_certificate.get(
            "quantitative_inner_strong_stable_spectral_gap_validated"
        )
        is True
        and strong_certificate.get(
            "poincare_strong_stable_spectral_radius_bound_validated"
        )
        is True
        and strong_certificate.get("source_validated_base_gap_used") is True
        and strong_certificate.get("source_validated_same_inner_orbit_used")
        is True
        and strong_certificate.get("base_compact_history_monodromy_bridge_used")
        is True
        and strong_certificate.get(
            "base_extension_vertical_seam_zero_free_validated"
        )
        is True
        and strong_certificate.get("base_full_complex_neutral_disk_used") is True
        and strong_certificate.get("extension_closed_slab_zero_free_validated")
        is True
        and strong_certificate.get(
            "extension_upper_half_exact_partition_validated"
        )
        is True
        and strong_certificate.get(
            "combined_left_open_strip_zero_free_validated"
        )
        is True
        and strong_certificate.get(
            "physical_unshifted_coefficient_output_phase_used"
        )
        is True
        and strong_certificate.get("negative_real_delay_modulus_restored") is True
        and strong_certificate.get(
            "negative_real_tail_frequency_absolute_value_restored"
        )
        is True
        and strong_certificate.get("negative_real_delay_taylor_factor_restored")
        is True
        and strong_certificate.get("tail_diagonal_edge_monotonicity_validated")
        is True
        and strong_certificate.get("binary_blas_thread_count") == 1
        and strong_certificate.get("stable_boundary_power_bound_validated")
        is False
        and strong_certificate.get("stable_spectral_projection_constructed")
        is False
        and strong_certificate.get("inner_stable_manifold_validated") is False
    ):
        raise ValueError("the strengthened stable-gap boundary is incomplete")
    if (
        strong_certificate.get("base_gap_result_sha256")
        != BASE_STABLE_GAP_RESULT_SHA256
        or strong_certificate.get("inner_orbit_result_sha256")
        != INNER_ORBIT_RESULT_SHA256
    ):
        raise ValueError("the strengthened gap theorem parent chain changed")
    transfer_relative = gap_manifest.get("floquet_transfer_result")
    transfer_hash = gap_manifest.get("floquet_transfer_result_sha256")
    if (
        transfer_relative != FLOQUET_TRANSFER_RESULT_RELATIVE_PATH
        or transfer_hash != FLOQUET_TRANSFER_RESULT_SHA256
    ):
        raise ValueError("the stable-gap Floquet-transfer parent changed")
    transfer = _load_json(
        repository / FLOQUET_TRANSFER_RESULT_RELATIVE_PATH,
        FLOQUET_TRANSFER_RESULT_SHA256,
        "Floquet-transfer",
    )
    transfer_manifest = _mapping(transfer.get("manifest"), "transfer manifest")
    _validate_source_hashes(transfer_manifest, repository)
    _validate_named_parent_hashes(transfer_manifest, repository)
    orbit_relative = gap_manifest.get("inner_orbit_result")
    orbit_hash = gap_manifest.get("inner_orbit_result_sha256")
    if not isinstance(orbit_relative, str) or orbit_hash != INNER_ORBIT_RESULT_SHA256:
        raise ValueError("the stable-gap source orbit changed")
    orbit = _load_json(
        repository / orbit_relative,
        INNER_ORBIT_RESULT_SHA256,
        "inner orbit",
    )
    orbit_manifest = _mapping(orbit.get("manifest"), "orbit manifest")
    _validate_source_hashes(orbit_manifest, repository)
    _validate_named_parent_hashes(orbit_manifest, repository)

    stage1_contract = _mapping(stage1.get("contract"), "Stage-1 contract")
    stage1_parent_hashes = _mapping(
        stage1_contract.get("parent_result_sha256"), "Stage-1 parent hashes"
    )
    if stage1_parent_hashes.get(PULSE_TARGET_RESULT_RELATIVE_PATH) != (
        PULSE_TARGET_RESULT_SHA256
    ):
        raise ValueError("the Stage-1 pulse target parent changed")
    pulse_target = _load_json(
        repository / PULSE_TARGET_RESULT_RELATIVE_PATH,
        PULSE_TARGET_RESULT_SHA256,
        "pulse target",
    )
    pulse_target_manifest = _mapping(
        pulse_target.get("manifest"), "pulse target manifest"
    )
    _validate_named_parent_hashes(pulse_target_manifest, repository)
    candidate_relative = pulse_target_manifest.get("parent_candidate_result")
    candidate_hash = pulse_target_manifest.get("parent_candidate_result_sha256")
    if (
        candidate_relative != PULSE_CANDIDATE_RESULT_RELATIVE_PATH
        or candidate_hash != PULSE_CANDIDATE_RESULT_SHA256
    ):
        raise ValueError("the pulse target's separator candidate changed")
    pulse_candidate = _load_json(
        repository / PULSE_CANDIDATE_RESULT_RELATIVE_PATH,
        PULSE_CANDIDATE_RESULT_SHA256,
        "pulse candidate",
    )
    pulse_candidate_manifest = _mapping(
        pulse_candidate.get("manifest"), "pulse candidate manifest"
    )
    _validate_named_parent_hashes(pulse_candidate_manifest, repository)
    return stage1, base_gap, strong_gap, transfer, orbit, pulse_candidate


def _stable_spectral_ingress(
    stage1: Mapping[str, Any],
    gap: Mapping[str, Any],
    *,
    certificate_role: str,
    expected_gamma: Decimal,
    used_for_stage1_partial_adapter: bool,
) -> StableSpectralIngress:
    certificate = _mapping(gap.get("certificate"), "stable-gap certificate")
    stable = _positive(
        certificate.get("stable_multiplier_spectral_radius_upper"),
        "stable spectral-radius upper bound",
    )
    gap_lower = _positive(
        certificate.get("one_minus_stable_multiplier_modulus_lower"),
        "stable multiplier gap lower bound",
    )
    gamma = _positive(certificate.get("gamma_lower"), "left-strip gamma")
    if gamma != expected_gamma:
        raise ValueError(f"the {certificate_role} gamma changed")
    if not stable < 1 or stable + gap_lower > 1:
        raise ValueError("the directed stable spectral gap is inconsistent")
    contract = _mapping(stage1.get("contract"), "Stage-1 contract")
    evidence = _mapping(
        contract.get("proved_parent_evidence"), "Stage-1 evidence"
    )
    rho_u = _positive(
        evidence.get("unstable_backward_rate_upper_derived"),
        "unstable backward rate",
    )
    if not rho_u < 1:
        raise ValueError("the unstable backward rate is not below one")
    with localcontext() as up:
        up.prec = 96
        up.rounding = ROUND_CEILING
        working = (Decimal(1) + stable) / 2
        midpoint_beta = (Decimal(1) + working) / 2
        beta = (Decimal(7) + working) / 8
        midpoint_kernel = (
            Decimal(1) / (midpoint_beta - working)
            + rho_u / (Decimal(1) - midpoint_beta * rho_u)
        )
        near_unit_stable_coefficient = Decimal(1) / (beta - working)
        near_unit_unstable_coefficient = rho_u / (
            Decimal(1) - beta * rho_u
        )
        near_unit_kernel = (
            near_unit_stable_coefficient + near_unit_unstable_coefficient
        )
        fixed_working_limiting_kernel = (
            Decimal(1) / (Decimal(1) - working)
            + rho_u / (Decimal(1) - rho_u)
        )
        near_unit_old_loss_upper = (
            2
            * Decimal(10)
            * near_unit_kernel
            * Decimal(TARGET_STABLE_SEED_RADIUS)
        )
    with localcontext() as down:
        down.prec = 96
        down.rounding = ROUND_FLOOR
        near_unit_kernel_lower = (
            Decimal(1) / (beta - working)
            + rho_u / (Decimal(1) - beta * rho_u)
        )
        midpoint_critical = Decimal(1) / (
            2 * Decimal(TARGET_STABLE_SEED_RADIUS) * midpoint_kernel
        )
        near_unit_critical = Decimal(1) / (
            2 * Decimal(TARGET_STABLE_SEED_RADIUS) * near_unit_kernel
        )
        fixed_working_limiting_critical = Decimal(1) / (
            2
            * Decimal(TARGET_STABLE_SEED_RADIUS)
            * fixed_working_limiting_kernel
        )
        stationary_beta = (
            Decimal(1) + rho_u * working
        ) / (2 * rho_u)
        near_unit_old_discriminant = Decimal(1) - near_unit_old_loss_upper
        working_slack = working - stable
        beta_slack = beta - working
        near_unit_old_loss_lower = (
            2
            * Decimal(10)
            * near_unit_kernel_lower
            * Decimal(TARGET_STABLE_SEED_RADIUS)
        )
    with localcontext() as up:
        up.prec = 96
        up.rounding = ROUND_CEILING
        near_unit_old_discriminant_upper = (
            Decimal(1) - near_unit_old_loss_lower
        )
    if not stable < working < beta < 1:
        raise ArithmeticError("the strict stable rate and sequence weight failed")
    return StableSpectralIngress(
        certificate_role=certificate_role,
        used_for_stage1_partial_adapter=used_for_stage1_partial_adapter,
        gamma_lower=_lower(gamma),
        stable_spectrum_modulus_upper=_upper(stable),
        stable_spectrum_gap_to_unit_lower=_lower(gap_lower),
        working_stable_power_rate_upper=_upper(working),
        working_rate_minus_spectrum_upper_lower=_lower(working_slack),
        sequence_weight_beta=_upper(beta),
        sequence_weight_selection_formula="beta=1-(1-working_rate)/8",
        beta_minus_working_rate_lower=_lower(beta_slack),
        unstable_backward_rate_upper=_upper(rho_u),
        unstable_restriction_dimension=1,
        unstable_dichotomy_constant_upper_intrinsic="1",
        stable_dichotomy_constant_upper=None,
        stable_power_constant_exists_qualitatively_at_working_rate=True,
        stable_power_constant_numeric_upper_validated=False,
        unstable_backward_power_bound_on_eigenline_validated=True,
        spectral_radius_bound_used_as_boundary_power_bound=False,
        midpoint_diagnostic_sequence_weight_beta=_upper(midpoint_beta),
        midpoint_optimistic_kernel_with_all_unknown_norms_set_to_one=(
            _upper(midpoint_kernel)
        ),
        midpoint_optimistic_critical_c_n_sufficient_threshold=(
            _lower(midpoint_critical)
        ),
        near_unit_diagnostic_sequence_weight_beta=_upper(beta),
        near_unit_diagnostic_sequence_weight_formula=(
            "beta_near=1-(1-working_rate)/8"
        ),
        near_unit_stable_kernel_coefficient_upper=(
            _upper(near_unit_stable_coefficient)
        ),
        near_unit_unstable_kernel_coefficient_upper=(
            _upper(near_unit_unstable_coefficient)
        ),
        near_unit_optimistic_kernel_with_all_unknown_norms_set_to_one=(
            _upper(near_unit_kernel)
        ),
        near_unit_optimistic_critical_c_n_sufficient_threshold=(
            _lower(near_unit_critical)
        ),
        near_unit_optimistic_old_c_n_discriminant_lower=(
            _lower(near_unit_old_discriminant)
        ),
        near_unit_optimistic_old_c_n_discriminant_upper=(
            _upper(near_unit_old_discriminant_upper)
        ),
        near_unit_optimistic_old_c_n_scalar_gate_closes=(
            near_unit_old_discriminant > 0
        ),
        optimistic_kernel_beta_derivative_formula=(
            "dC/dbeta=-1/(beta-working_rate)^2+"
            "rho_u^2/(1-beta*rho_u)^2"
        ),
        optimistic_stationary_beta_lower=_lower(stationary_beta),
        optimistic_stationary_beta_above_one_validated=(stationary_beta > 1),
        optimistic_kernel_strictly_decreasing_on_admissible_beta_interval=(
            stationary_beta > 1
        ),
        fixed_working_beta_to_one_optimistic_kernel_infimum=(
            _upper(fixed_working_limiting_kernel)
        ),
        fixed_working_beta_to_one_critical_c_n_supremum_lower=(
            _lower(fixed_working_limiting_critical)
        ),
        fixed_working_optimistic_old_c_n_window_possible=(
            Decimal(10) < fixed_working_limiting_critical
        ),
        old_stage1_design_c_n="10",
        general_scalar_feasibility_formula_at_selected_rates=(
            "K_s*C_N*(a_s*K_s*p_s+a_u*K_u*p_u)<2500, where "
            "a_s=1/(beta-working_rate), a_u=rho_u/(1-beta*rho_u)"
        ),
        general_scalar_feasibility_budget_rhs="2500",
    )


def _abstract_phase_section_audit(
    transfer: Mapping[str, Any], orbit: Mapping[str, Any]
) -> AbstractPhaseSectionAudit:
    artifact = _mapping(transfer.get("artifact"), "transfer artifact")
    branches = _mapping(artifact.get("branches"), "transfer branches")
    inner = _mapping(branches.get(BRANCH), "inner transfer branch")
    bordered_inverse = _positive(
        inner.get("bordered_inverse_norm_upper"), "bordered inverse norm"
    )
    nonconstant = _positive(
        inner.get("nonconstant_fourier_mode_lower"), "nonconstant mode"
    )
    tangent_upper = _positive(
        inner.get("orbit_tangent_norm_upper"), "orbit tangent norm"
    )
    correction = _positive(inner.get("correction_radius"), "orbit correction")
    if not (
        inner.get("neutral_multiplier_algebraically_simple_validated") is True
        and inner.get("regularity_bridge_to_history_monodromy") is True
    ):
        raise ValueError("the phase-bordered transfer hypotheses regressed")
    orbit_artifact = _mapping(orbit.get("artifact"), "orbit artifact")
    collocation = _mapping(orbit_artifact.get("collocation"), "orbit collocation")
    phase_border = collocation.get("phase_border")
    expected_phase_border = (
        "mean Euclidean pairing with D_phase(reference); reference and state "
        "are stored as exact binary64 samples"
    )
    if phase_border != expected_phase_border:
        raise ValueError("the periodic-BVP phase functional changed")
    period_hex, period_exact = _binary64_exact_decimal(
        collocation.get("period"), "inner orbit period"
    )
    with localcontext() as up:
        up.prec = 96
        up.rounding = ROUND_CEILING
        period_upper = period_exact + correction
        bvp_projection = Decimal(1) + bordered_inverse * tangent_upper
    with localcontext() as down:
        down.prec = 96
        down.rounding = ROUND_FLOOR
        tangent_lower = Decimal(6) * nonconstant
        bvp_pairing = tangent_lower / bordered_inverse
        pulled_back_history_speed = bvp_pairing / period_upper
        history_speed = tangent_lower / period_upper
    if history_speed <= 0 or bvp_pairing <= 0 or pulled_back_history_speed <= 0:
        raise ArithmeticError("the abstract phase speed lower bound vanished")
    return AbstractPhaseSectionAudit(
        periodic_bvp_phase_border_description=expected_phase_border,
        periodic_bvp_bordered_inverse_norm_upper=_upper(bordered_inverse),
        periodic_bvp_phase_pairing_abs_lower=_lower(bvp_pairing),
        periodic_bvp_phase_normal_vector_norm_upper=_upper(bordered_inverse),
        periodic_bvp_phase_functional_norm_upper=_upper(tangent_upper),
        periodic_bvp_phase_projection_norm_upper=_upper(bvp_projection),
        periodic_bvp_phase_condition_affine_c2_upper="0",
        periodic_bvp_phase_condition_quantitatively_transverse=True,
        periodic_bvp_phase_functional_is_one_history_functional=False,
        phase_row_history_pullback_formula=(
            "ell_H=ell_BVP o E_gamma, where E_gamma maps one initial "
            "history to its finite-time variational trajectory on [0,T], "
            "and the mean-pairing formula for ell_BVP is extended to that "
            "continuous, not necessarily periodic, trajectory"
        ),
        phase_row_history_pullback_exists_as_bounded_linear_functional=True,
        phase_row_history_pullback_operator_norm_upper=None,
        phase_row_history_section_c2_upper="0",
        phase_row_history_event_speed_at_orbit_lower=(
            _lower(pulled_back_history_speed)
        ),
        phase_row_history_section_constructively_registered=False,
        nonconstant_fourier_mode_lower=_lower(nonconstant),
        normalized_tangent_sup_norm_lower=_lower(tangent_lower),
        orbit_period_binary64_hex=period_hex,
        orbit_period_upper=_upper(period_upper),
        existential_history_coordinate_section_functional_norm_upper="1",
        existential_history_coordinate_section_projection_norm_upper="2",
        existential_history_coordinate_section_c2_upper="0",
        existential_history_coordinate_event_speed_at_orbit_lower=(
            _lower(history_speed)
        ),
        existential_history_coordinate_section_pointwise_transverse_proved=True,
        fourier_existence_argument_alone_registers_phase_and_component=False,
        uniform_event_speed_lower_on_return_tube=None,
        uniform_event_speed_on_return_tube_validated=False,
        specific_pulse_voltage_section_speed_lower_validated=False,
    )


def _sequence_value_at_zero(sequence: Mapping[int, Any]) -> Any:
    values = list(sequence.values())
    if not values:
        raise ValueError("cannot evaluate an empty Fourier sequence")
    total = values[0]
    for value in values[1:]:
        total = total + value
    return total


@lru_cache(maxsize=4)
def _explicit_voltage_section_numbers(repository_text: str) -> dict[str, str]:
    """Replay the transfer's tangent-change bound at the explicit phase zero."""

    repository = Path(repository_text)
    precision = 160
    orbit, evidence = load_validated_leaky_orbit_evidence(repository, BRANCH)
    if (
        evidence.source_result_sha256 != INNER_ORBIT_RESULT_SHA256
        or evidence.correction_radius != "1e-5"
    ):
        raise ValueError("the explicit section belongs to a different orbit ball")
    base = _build_leaky_base_sequences(orbit, precision)
    radius = DirectedInterval.from_decimal(
        evidence.correction_radius, precision
    ).upper
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        minimum_period = base.period.lower - radius
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        maximum_period = base.period.upper + radius
    voltage_bar = _sequence_box_norm_upper(base.voltage, precision)
    centered_bar = _sequence_box_norm_upper(base.centered_voltage, precision)
    delayed_field_derivative_bar = _sequence_box_norm_upper(
        base.delayed_field_derivative, precision
    )
    tangent_bar = _state_sequence_norm_upper(base, precision)
    residual_bar = _residual_sequence_norm_upper(base, precision)
    epsilon = base.parameters["epsilon"].upper
    kappa_1 = base.parameters["kappa_1"].upper
    kappa_3 = base.parameters["kappa_3"].upper
    one = gmpy2.mpfr(1, precision)
    two = gmpy2.mpfr(2, precision)
    three = gmpy2.mpfr(3, precision)
    six = gmpy2.mpfr(6, precision)
    section_ball = DirectedInterval.from_decimal("0.01", precision)
    section_ball_radius = section_ball.upper
    sqrt_two = DirectedInterval.from_decimal(2, precision).sqrt().upper
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        voltage = voltage_bar + radius
        centered = centered_bar + radius
        voltage_cubic_slope = (
            voltage * voltage
            + voltage * voltage_bar
            + voltage_bar * voltage_bar
        ) / three
        centered_cubic_slope = (
            centered * centered
            + centered * centered_bar
            + centered_bar * centered_bar
        )
        fast_voltage_lipschitz = (
            one
            + epsilon * kappa_1
            + voltage_cubic_slope
            + epsilon * kappa_3 * centered_cubic_slope
        )
        state_field_lipschitz = max(
            fast_voltage_lipschitz + epsilon,
            one + epsilon,
        )
        delayed_field_lipschitz = (
            epsilon * kappa_1 / two
            + epsilon * kappa_3 * centered_cubic_slope / two
        )
    delay_field_changes: list[gmpy2.mpfr] = []
    for key in ("tau_0", "tau_1"):
        tau = base.parameters[key].upper
        with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
            delay_fraction_change = (
                tau
                * radius
                / (minimum_period * base.period.lower)
            )
            delay_field_changes.append(
                sqrt_two * delayed_field_lipschitz * radius
                + sqrt_two
                * delay_fraction_change
                * delayed_field_derivative_bar
            )
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        field_change = (
            state_field_lipschitz * radius
            + upward_sum(delay_field_changes, precision)
        )
        candidate_field = (
            tangent_bar + residual_bar
        ) / base.period.lower
        tangent_change = (
            maximum_period * field_change
            + radius * candidate_field
            + residual_bar
        )
        tangent_upper = tangent_bar + tangent_change
        physical_history_speed_upper = tangent_upper / minimum_period

    candidate_voltage = _sequence_value_at_zero(base.voltage)
    candidate_tangent = _sequence_value_at_zero(base.phase_voltage)
    if not (
        candidate_voltage.imag.lower <= 0 <= candidate_voltage.imag.upper
        and candidate_tangent.imag.lower <= 0 <= candidate_tangent.imag.upper
        and candidate_tangent.real.lower > 0
    ):
        raise ArithmeticError("the explicit phase-zero voltage section changed")
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        orbit_voltage_lower = candidate_voltage.real.lower - radius
        tangent_lower = candidate_tangent.real.lower - tangent_change
        physical_speed_lower = tangent_lower / maximum_period
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        orbit_voltage_upper = candidate_voltage.real.upper + radius
        section_voltage_bound = voltage_bar + radius + section_ball_radius
        section_centered_bound = centered_bar + radius + section_ball_radius
        section_field_lipschitz = (
            two
            + section_voltage_bound * section_voltage_bound
            + two * epsilon * kappa_1
            + six
            * epsilon
            * kappa_3
            * section_centered_bound
            * section_centered_bound
        )
        section_speed_variation = (
            section_field_lipschitz * section_ball_radius
        )
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        section_uniform_speed = physical_speed_lower - section_speed_variation
    if (
        tangent_lower <= 0
        or physical_speed_lower <= 0
        or section_uniform_speed <= 0
    ):
        raise ArithmeticError("the explicit voltage section lost transversality")
    return {
        "candidate_section_voltage_lower": decimal_lower(
            candidate_voltage.real.lower
        ),
        "candidate_section_voltage_upper": decimal_upper(
            candidate_voltage.real.upper
        ),
        "validated_orbit_section_voltage_lower": decimal_lower(
            orbit_voltage_lower
        ),
        "validated_orbit_section_voltage_upper": decimal_upper(
            orbit_voltage_upper
        ),
        "candidate_normalized_voltage_tangent_lower": decimal_lower(
            candidate_tangent.real.lower
        ),
        "normalized_tangent_correction_upper": decimal_upper(tangent_change),
        "validated_normalized_voltage_tangent_lower": decimal_lower(
            tangent_lower
        ),
        "orbit_period_upper": decimal_upper(maximum_period),
        "orbit_period_lower": decimal_lower(minimum_period),
        "physical_voltage_event_speed_at_orbit_lower": decimal_lower(
            physical_speed_lower
        ),
        "declared_section_ball_radius": decimal_lower(section_ball.lower),
        "vector_field_lipschitz_upper_on_declared_section_ball": decimal_upper(
            section_field_lipschitz
        ),
        "event_speed_variation_upper_on_declared_section_ball": decimal_upper(
            section_speed_variation
        ),
        "uniform_event_speed_lower_on_declared_section_ball": decimal_lower(
            section_uniform_speed
        ),
        "physical_orbit_history_speed_upper": decimal_upper(
            physical_history_speed_upper
        ),
        "replayed_orbit_tangent_norm_upper": decimal_upper(tangent_upper),
    }


def _explicit_voltage_section_audit(
    repository: Path,
    transfer: Mapping[str, Any],
    pulse_candidate: Mapping[str, Any],
) -> ExplicitVoltageSectionAudit:
    artifact = _mapping(transfer.get("artifact"), "transfer artifact")
    branches = _mapping(artifact.get("branches"), "transfer branches")
    inner = _mapping(branches.get(BRANCH), "inner transfer branch")
    candidate = _mapping(
        pulse_candidate.get("candidate"), "pulse separator candidate"
    )
    method = _mapping(candidate.get("method"), "pulse separator method")
    registered_description = "v=v_inner(0), positive crossing"
    if method.get("section") != registered_description:
        raise ValueError("the registered pulse voltage section changed")
    resolutions = candidate.get("resolutions")
    if not isinstance(resolutions, list) or not resolutions:
        raise ValueError("the registered pulse voltage resolutions changed")
    registered_levels = {
        _binary64_exact_decimal(
            _mapping(row, "pulse resolution").get("phase_section_voltage"),
            "registered pulse section voltage",
        )
        for row in resolutions
    }
    if len(registered_levels) != 1:
        raise ValueError("the registered pulse section level is inconsistent")
    registered_level_hex, registered_level = next(iter(registered_levels))
    numbers = _explicit_voltage_section_numbers(str(repository.resolve()))
    if numbers["replayed_orbit_tangent_norm_upper"] != inner.get(
        "orbit_tangent_norm_upper"
    ):
        raise ValueError("the explicit section tangent replay changed")
    orbit_voltage_lower = Decimal(numbers["validated_orbit_section_voltage_lower"])
    orbit_voltage_upper = Decimal(numbers["validated_orbit_section_voltage_upper"])
    if not orbit_voltage_lower <= registered_level <= orbit_voltage_upper:
        raise ValueError("the old pulse section left the phase-zero orbit enclosure")
    section_ball_lower = Decimal(numbers["declared_section_ball_radius"])
    section_speed_lower = Decimal(
        numbers["uniform_event_speed_lower_on_declared_section_ball"]
    )
    physical_history_speed_upper = Decimal(
        numbers["physical_orbit_history_speed_upper"]
    )
    period_lower = Decimal(numbers["orbit_period_lower"])
    with localcontext() as up:
        up.prec = 96
        up.rounding = ROUND_CEILING
        old_level_error = max(
            registered_level - orbit_voltage_lower,
            orbit_voltage_upper - registered_level,
        )
        local_time_offset = 2 * old_level_error / section_speed_lower
        local_phase_offset = local_time_offset / period_lower
        local_history_displacement = (
            physical_history_speed_upper * local_time_offset
        )
    with localcontext() as down:
        down.prec = 96
        down.rounding = ROUND_FLOOR
        local_voltage_change = section_speed_lower * local_time_offset
        local_bracket_margin = local_voltage_change - old_level_error
    local_crossing_closes = (
        old_level_error > 0
        and local_bracket_margin > 0
        and local_history_displacement < section_ball_lower
    )
    if not local_crossing_closes:
        raise ArithmeticError("the old binary64 section lost its local bracket")
    return ExplicitVoltageSectionAudit(
        exact_phase_zero_section_formula="h_C(phi)=phi_v(0)-V_true(0)",
        registered_pulse_section_description=registered_description,
        normalized_phase="0",
        state_component="voltage",
        same_history_evaluation_functional_as_registered_pulse_section=True,
        registered_pulse_section_level_binary64_hex=registered_level_hex,
        registered_pulse_section_level_decimal=_upper(registered_level),
        registered_pulse_section_level_inside_phase_zero_orbit_value_enclosure=True,
        exact_section_level_equals_registered_pulse_section_level_validated=False,
        candidate_section_voltage_lower=numbers[
            "candidate_section_voltage_lower"
        ],
        candidate_section_voltage_upper=numbers[
            "candidate_section_voltage_upper"
        ],
        validated_orbit_section_voltage_lower=numbers[
            "validated_orbit_section_voltage_lower"
        ],
        validated_orbit_section_voltage_upper=numbers[
            "validated_orbit_section_voltage_upper"
        ],
        candidate_normalized_voltage_tangent_lower=numbers[
            "candidate_normalized_voltage_tangent_lower"
        ],
        normalized_tangent_correction_upper=numbers[
            "normalized_tangent_correction_upper"
        ],
        validated_normalized_voltage_tangent_lower=numbers[
            "validated_normalized_voltage_tangent_lower"
        ],
        orbit_period_upper=numbers["orbit_period_upper"],
        physical_voltage_event_speed_at_orbit_lower=numbers[
            "physical_voltage_event_speed_at_orbit_lower"
        ],
        section_functional_norm_upper="1",
        section_chart_projection_norm_upper="2",
        section_defining_function_c2_upper="0",
        unweighted_wiener_ball_directly_controls_derivative=False,
        rfde_vector_field_identity_closes_tangent_correction=True,
        additional_first_order_weighted_tail_bound_required_for_point_speed=False,
        pointwise_orbit_speed_validated=True,
        old_binary64_voltage_level_error_from_true_phase_zero_upper=(
            _upper(old_level_error)
        ),
        physical_orbit_history_speed_upper=_upper(
            physical_history_speed_upper
        ),
        old_binary64_voltage_level_crossing_time_offset_upper=(
            _upper(local_time_offset)
        ),
        old_binary64_voltage_level_crossing_phase_offset_upper=(
            _upper(local_phase_offset)
        ),
        orbit_history_displacement_over_local_crossing_bracket_upper=(
            _upper(local_history_displacement)
        ),
        local_crossing_bracket_within_declared_section_ball=True,
        old_binary64_voltage_level_local_orbit_crossing_speed_lower=(
            numbers["uniform_event_speed_lower_on_declared_section_ball"]
        ),
        old_binary64_voltage_level_has_unique_local_true_orbit_crossing_validated=(
            True
        ),
        pulse_reshoot_required_before_route_c_target_can_be_used=True,
        tube_uniform_speed_reduction_formula=(
            "a_tube>=a_orbit-H*L_F*R_tube; positivity follows from "
            "R_tube<a_orbit/(H*L_F)"
        ),
        declared_section_ball_radius=numbers["declared_section_ball_radius"],
        vector_field_lipschitz_upper_on_declared_section_ball=numbers[
            "vector_field_lipschitz_upper_on_declared_section_ball"
        ],
        event_speed_variation_upper_on_declared_section_ball=numbers[
            "event_speed_variation_upper_on_declared_section_ball"
        ],
        uniform_event_speed_lower_on_declared_section_ball=numbers[
            "uniform_event_speed_lower_on_declared_section_ball"
        ],
        uniform_event_speed_on_declared_section_ball_validated=True,
        uniform_event_speed_lower_on_return_tube=None,
        uniform_event_speed_on_return_tube_validated=False,
    )


def build_stage2_stable_manifold_contract(
    repository: Path,
) -> Stage2StableManifoldContract:
    repository = repository.resolve()
    (
        stage1,
        base_gap,
        strong_gap,
        transfer,
        orbit,
        pulse_candidate,
    ) = _load_parents(repository)
    baseline_spectral = _stable_spectral_ingress(
        stage1,
        base_gap,
        certificate_role="baseline_gamma_0.001_honest_failure_row",
        expected_gamma=Decimal("0.001"),
        used_for_stage1_partial_adapter=False,
    )
    strengthened_spectral = _stable_spectral_ingress(
        stage1,
        strong_gap,
        certificate_role="strengthened_gamma_0.01_partial_adapter_row",
        expected_gamma=Decimal("0.01"),
        used_for_stage1_partial_adapter=True,
    )
    if baseline_spectral.near_unit_optimistic_old_c_n_scalar_gate_closes:
        raise ArithmeticError("the baseline honest-failure row unexpectedly closed")
    if not strengthened_spectral.near_unit_optimistic_old_c_n_scalar_gate_closes:
        raise ArithmeticError("the strengthened gap lost its explicit scalar window")
    if baseline_spectral.fixed_working_optimistic_old_c_n_window_possible:
        raise ArithmeticError("the baseline fixed-working infimum acquired a window")
    if not strengthened_spectral.fixed_working_optimistic_old_c_n_window_possible:
        raise ArithmeticError("the strengthened fixed-working window vanished")
    phase = _abstract_phase_section_audit(transfer, orbit)
    voltage_section = _explicit_voltage_section_audit(
        repository, transfer, pulse_candidate
    )

    return_budget = AffineReturnC2InputBudget(
        section_history_ball_radius_lower=(
            voltage_section.declared_section_ball_radius
        ),
        flow_history_tube_radius_lower=None,
        return_time_lower=None,
        return_time_upper=None,
        phase_functional_norm_upper=(
            voltage_section.section_functional_norm_upper
        ),
        uniform_event_speed_lower=(
            voltage_section.uniform_event_speed_lower_on_declared_section_ball
        ),
        section_defining_function_c2_upper="0",
        section_chart_projection_norm_upper=(
            voltage_section.section_chart_projection_norm_upper
        ),
        vector_field_norm_upper=None,
        vector_field_d1_upper=None,
        flow_d1_upper=None,
        flow_d2_upper=None,
        validated_return_map_ball_radius_lower=None,
        evidence_status=(
            "source_bound_section_ball_and_uniform_speed_no_return_flow_tube"
        ),
    )
    return_evaluation = evaluate_affine_return_c2_majorant(return_budget)
    if return_evaluation.return_c2_majorant_closes:
        raise AssertionError("incomplete Stage-2 evidence closed a return-C2 bound")

    stage1_budget = StableGraphInputBudget(
        stable_spectral_radius_upper=(
            strengthened_spectral.working_stable_power_rate_upper
        ),
        unstable_backward_rate_upper=(
            strengthened_spectral.unstable_backward_rate_upper
        ),
        stable_projection_norm_upper=None,
        unstable_projection_norm_upper=None,
        stable_dichotomy_constant_upper=None,
        unstable_dichotomy_constant_upper=(
            strengthened_spectral.unstable_dichotomy_constant_upper_intrinsic
        ),
        sequence_weight_beta=strengthened_spectral.sequence_weight_beta,
        section_event_speed_lower=(
            voltage_section.uniform_event_speed_lower_on_declared_section_ball
        ),
        section_defining_function_c2_upper="0",
        poincare_return_c2_upper=None,
        nonlinear_derivative_remainder_coefficient_upper=None,
        validated_return_map_ball_radius_lower=None,
        stable_seed_radius_target=TARGET_STABLE_SEED_RADIUS,
        evidence_status="source_bound_stage2_partial_evidence",
    )
    stage1_evaluation = evaluate_lyapunov_perron_majorant(stage1_budget)
    if stage1_evaluation.graph_majorant_closes:
        raise AssertionError("Stage-2 partial ingress closed a stable graph")

    claims = {
        "stable_spectral_radius_numeric_bound_ingressed": True,
        "baseline_gamma001_honest_failure_budget_recorded": True,
        "strengthened_gamma01_spectral_radius_ingressed": True,
        "strengthened_gap_near_unit_optimistic_scalar_gate_closes": True,
        "strict_working_stable_power_rate_selected": True,
        "stable_power_constant_exists_qualitatively_at_working_rate": True,
        "unstable_eigenline_dichotomy_constant_one_validated": True,
        "periodic_bvp_phase_condition_quantitatively_transverse": True,
        "variational_pullback_phase_row_defines_affine_history_section": True,
        "existential_history_coordinate_section_pointwise_speed_validated": True,
        "existential_history_coordinate_section_affine_c2_zero": True,
        "concrete_history_phase_and_component_registered": True,
        "exact_phase_zero_voltage_section_pointwise_orbit_speed_validated": True,
        "exact_phase_zero_voltage_section_uniform_speed_on_declared_ball_validated": (
            True
        ),
        "old_binary64_voltage_level_has_unique_local_true_orbit_crossing_validated": (
            True
        ),
        **{name: False for name in QUANTITATIVE_FALSE_FLAGS},
    }
    return Stage2StableManifoldContract(
        schema_id=SCHEMA_ID,
        model_id=MODEL_ID,
        branch=BRANCH,
        phase_space="Y=C([-5*sqrt(5),0],R)xR",
        history_norm="||(phi,w)||_Y=max(||phi||_infinity,|w|)",
        parent_result_sha256=_parent_hash_map(),
        baseline_gamma001_spectral_ingress=asdict(baseline_spectral),
        strengthened_gamma01_spectral_ingress=asdict(strengthened_spectral),
        abstract_phase_section_audit=asdict(phase),
        explicit_voltage_section_audit=asdict(voltage_section),
        riesz_projection_and_dichotomy_ledger={
            "stable_subspace_exists_qualitatively": True,
            "unstable_subspace_dimension": 1,
            "stable_riesz_projection_norm_upper": None,
            "unstable_riesz_projection_norm_upper": None,
            "stable_dichotomy_constant_upper": None,
            "unstable_dichotomy_constant_upper_on_eigenline": "1",
            "stable_working_rate": (
                strengthened_spectral.working_stable_power_rate_upper
            ),
            "unstable_backward_rate": (
                strengthened_spectral.unstable_backward_rate_upper
            ),
            "stable_projection_on_phase_section_formula": "P_s=I-P_u",
            "stable_projection_norm_reduction_formula": "p_s<=1+p_u",
            "unstable_projection_formula": (
                "P_u=(2*pi*i)^(-1)*integral_Gamma_u "
                "(z*I-M_section)^(-1) dz"
            ),
            "projection_norm_contour_formula": (
                "p_u<=length(Gamma_u)/(2*pi)*"
                "sup_Gamma_u||(z*I-M_section)^(-1)||"
            ),
            "stable_power_contour_formula": (
                "K_s<=rho_s*sup_|z|=rho_s "
                "||(z*I-L_s)^(-1)||"
            ),
            "periodic_pencil_zero_free_cover_is_history_resolvent_bound": False,
            "local_unstable_grushin_border_is_history_riesz_covector": False,
            "next_minimal_projection_certificate": (
                "a directed history-section monodromy resolvent bound on one "
                "unstable contour, or directed right/left eigenhistories with "
                "a nonzero normalization pairing"
            ),
            "next_minimal_stable_dichotomy_certificate": (
                "a deflated history-section resolvent bound on the circle at "
                "the declared working stable rate"
            ),
        },
        return_c2_actual_budget=asdict(return_budget),
        return_c2_actual_evaluation=asdict(return_evaluation),
        stage1_budget_after_stage2_ingress=asdict(stage1_budget),
        stage1_majorant_after_stage2_ingress=asdict(stage1_evaluation),
        next_certificate_interface={
            "return_c2_required_fields": list(RETURN_C2_REQUIRED_FIELDS),
            "history_norm": "||(phi,w)||_Y=max(||phi||_infinity,|w|)",
            "constructive_section_gate": (
                "the exact phase-zero voltage section and its uniform speed on "
                "the radius-0.01 section ball are registered; next bind the "
                "return flow tube and exact level used by the pulse reshoot"
            ),
            "section_route_comparison": {
                "A_existing_voltage_section": (
                    "keep the binary64 candidate level used by the old pulse "
                    "target; its unique local true-orbit crossing and section-ball "
                    "speed are validated, but its exact reference history, return "
                    "map, stable graph, and pulse-history errors remain open"
                ),
                "B_phase_row_pullback_section": (
                    "register E_gamma and ell_H=ell_BVP o E_gamma, bound its "
                    "history dual norm and tube speed, then re-shoot every pulse "
                    "trajectory to this new section"
                ),
                "C_exact_phase_zero_voltage_section": (
                    "use h_C(phi)=phi_v(0)-V_true(0), whose pointwise orbit speed "
                    "and radius-0.01 section-ball speed are source-bound; prove "
                    "the return endpoint stays in that ball and re-shoot the old "
                    "pulse target because its binary64 level is not proved exact"
                ),
                "old_third_return_signs_transfer_to_route_B": False,
                "old_third_return_signs_transfer_to_route_C": False,
                "any_route_currently_proves_crossing": False,
            },
            "flow_gate": (
                "directed F_0,F_1,U_1,U_2 bounds on the full return-time window "
                "and continuous-history tube"
            ),
            "return_time_formulas": {
                "first_derivative": "tau_1=H*U_1/a",
                "second_derivative": (
                    "tau_2=H*(U_2+2*F_1*U_1*tau_1+"
                    "F_1*F_0*tau_1^2)/a"
                ),
            },
            "return_c2_formula": (
                "M_2=Q*(U_2+2*F_1*U_1*tau_1+"
                "F_1*F_0*tau_1^2+F_0*tau_2)"
            ),
            "nonlinear_remainder_from_return_c2": "C_N=M_2",
            "orbit_bvp_correction_ball_is_return_map_ball": False,
            "pulse_voltage_section_is_separate_from_abstract_section": True,
            "old_pulse_level_equals_true_phase_zero_voltage_validated": False,
        },
        claim_status=claims,
    )


def build_stage2_stable_manifold_result(repository: Path) -> dict[str, Any]:
    contract = _json_normalize(
        asdict(build_stage2_stable_manifold_contract(repository))
    )
    return {
        "contract": contract,
        "manifest": {
            "schema_id": SCHEMA_ID,
            "result": RESULT_RELATIVE_PATH,
            "default_command": DEFAULT_COMMAND,
            "arithmetic_scope": ARITHMETIC_SCOPE,
            "contract_sha256": canonical_sha256(contract),
            "source_sha256": {
                relative: _sha256_path(repository / relative)
                for relative in SOURCE_MANIFEST
            },
            "parent_result_sha256": _parent_hash_map(),
        },
    }


def validate_stage2_stable_manifold_result(
    payload: Mapping[str, Any], repository: Path
) -> None:
    if not isinstance(payload, Mapping) or set(payload) != {"contract", "manifest"}:
        raise ValueError("the Stage-2 result schema changed")
    contract = _mapping(payload.get("contract"), "Stage-2 contract")
    manifest = _mapping(payload.get("manifest"), "Stage-2 manifest")
    expected_fields = {field.name for field in fields(Stage2StableManifoldContract)}
    if set(contract) != expected_fields:
        raise ValueError("the Stage-2 contract dataclass schema changed")
    expected = _json_normalize(
        asdict(build_stage2_stable_manifold_contract(repository))
    )
    if dict(contract) != expected:
        raise ValueError("the Stage-2 contract differs from source replay")
    expected_manifest_fields = {
        "schema_id",
        "result",
        "default_command",
        "arithmetic_scope",
        "contract_sha256",
        "source_sha256",
        "parent_result_sha256",
    }
    if set(manifest) != expected_manifest_fields:
        raise ValueError("the Stage-2 manifest schema changed")
    fixed = {
        "schema_id": SCHEMA_ID,
        "result": RESULT_RELATIVE_PATH,
        "default_command": DEFAULT_COMMAND,
        "arithmetic_scope": ARITHMETIC_SCOPE,
        "contract_sha256": canonical_sha256(contract),
        "parent_result_sha256": _parent_hash_map(),
    }
    if any(manifest.get(name) != value for name, value in fixed.items()):
        raise ValueError("the Stage-2 manifest fixed data changed")
    source_hashes = _mapping(manifest.get("source_sha256"), "Stage-2 sources")
    if set(source_hashes) != set(SOURCE_MANIFEST):
        raise ValueError("the Stage-2 source manifest changed")
    for relative in SOURCE_MANIFEST:
        if source_hashes.get(relative) != _sha256_path(repository / relative):
            raise ValueError(f"the Stage-2 source changed: {relative}")
    for relative, digest in _parent_hash_map().items():
        if _sha256_path(repository / relative) != digest:
            raise ValueError(f"the Stage-2 parent changed: {relative}")


__all__ = [
    "ARITHMETIC_SCOPE",
    "AffineReturnC2InputBudget",
    "AffineReturnC2Majorant",
    "DEFAULT_COMMAND",
    "GENERATOR_RELATIVE_PATH",
    "NOTE_RELATIVE_PATH",
    "QUANTITATIVE_FALSE_FLAGS",
    "RESULT_RELATIVE_PATH",
    "RETURN_C2_REQUIRED_FIELDS",
    "SCHEMA_ID",
    "SOURCE_MANIFEST",
    "SOURCE_RELATIVE_PATH",
    "BASE_STABLE_GAP_RESULT_RELATIVE_PATH",
    "BASE_STABLE_GAP_RESULT_SHA256",
    "STRONG_STABLE_GAP_RESULT_RELATIVE_PATH",
    "STRONG_STABLE_GAP_RESULT_SHA256",
    "STAGE1_RESULT_RELATIVE_PATH",
    "STAGE1_RESULT_SHA256",
    "Stage2StableManifoldContract",
    "build_stage2_stable_manifold_contract",
    "build_stage2_stable_manifold_result",
    "canonical_sha256",
    "evaluate_affine_return_c2_majorant",
    "validate_stage2_stable_manifold_result",
]
