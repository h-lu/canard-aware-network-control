"""Stage-4N enlarged-ball nonlinear-flow feasibility certificate.

The open Stage-4N contract asks for a common nonlinear selected-return
family on the preferred-B ball

    ||x_s||_Y <= 0.0097,  |x_u| <= 0.00025.

This module tests the first deliberately generic route.  It imports the
directed Stage-4I current/delay coefficient maxima, adds the exact local
Hessian row perturbation on the radius-0.00995 ball, and applies a scalar
row-sum Gronwall comparison through the lower exact inner period.  It also
records the still coarser Stage-6A-style polynomial row sum.  Both routes
fail before an event window can be formed.

The artifact then uses the Stage-4L terminal stable row and the exact
unstable eigen-relation only to compute a *conditional design ceiling* for
a future signed, event-aligned complete-history second-variation kernel.
No kernel upper bound, nonlinear flow tube, event, return map, Hessian
block, graph, crossing, or onset statement is proved here.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from hashlib import sha256
import json
import os
from pathlib import Path
import platform
from typing import Any, Mapping

import gmpy2

from canard_control.directed_interval import (
    DirectedInterval,
    decimal_lower,
    decimal_upper,
)
from canard_control.leaky_dobrushin_transverse_halanay import (
    RESULT_RELATIVE_PATH as DOBRUSHIN_RESULT_RELATIVE_PATH,
)
from canard_control.leaky_inner_nonlinear_selected_return_tube_stage4n_contract import (
    RESULT_RELATIVE_PATH as STAGE4N_CONTRACT_RESULT_RELATIVE_PATH,
    validate_stage4n_result,
)
from canard_control.leaky_inner_stable_projection_stage3 import (
    RESULT_RELATIVE_PATH as STAGE3_RESULT_RELATIVE_PATH,
    validate_stage3_stable_projection_result,
)
from canard_control.leaky_inner_terminal_stable_row_stage4l import (
    RESULT_RELATIVE_PATH as STAGE4L_RESULT_RELATIVE_PATH,
    validate_stage4l_result,
)
from canard_control.leaky_inner_word_primitive_stage4i import (
    RESULT_RELATIVE_PATH as STAGE4I_RESULT_RELATIVE_PATH,
    validate_stage4i_result,
)


SCHEMA_ID = (
    "leaky-inner-nonlinear-selected-return-tube-stage4n-feasibility-v1"
)
MODEL_ID = "autonomous-leaky-recovery-two-delay-fhn-bistable-proposal"
BRANCH = "inner_saddle_candidate_selected_near_period_return"
STATUS = "NONCLOSING_SOURCE_BOUND_FEASIBILITY_PILOT"

SOURCE_RELATIVE_PATH = (
    "src/canard_control/"
    "leaky_inner_nonlinear_selected_return_tube_stage4n_feasibility.py"
)
GENERATOR_RELATIVE_PATH = (
    "experiments/"
    "leaky_inner_nonlinear_selected_return_tube_stage4n_feasibility.py"
)
RESULT_RELATIVE_PATH = (
    "experiments/results/"
    "leaky_inner_nonlinear_selected_return_tube_stage4n_feasibility.json"
)
NOTE_RELATIVE_PATH = (
    "docs/"
    "leaky-inner-nonlinear-selected-return-tube-stage4n-feasibility.md"
)
TEST_RELATIVE_PATH = (
    "tests/"
    "test_leaky_inner_nonlinear_selected_return_tube_stage4n_feasibility.py"
)

STAGE4N_CONTRACT_RESULT_SHA256 = (
    "b64f5230bb870b889fdc341d5d5139ea4ccac6faa7752ff2a5682eb0206cf160"
)
STAGE4I_RESULT_SHA256 = (
    "1248e9d95444f3cc12565c1e11b4bbeab3d4a9a7bb8922893e38b1ffa439f73e"
)
STAGE4L_RESULT_SHA256 = (
    "672f92c7c456a54f39afab7d2a5f92b783311cc0ee5341a4d2e72a588039017e"
)
STAGE3_RESULT_SHA256 = (
    "9ea776a6e627745ded7f7023523999bfbd29a0be4878172c76512d623146e2ea"
)
DOBRUSHIN_RESULT_SHA256 = (
    "21e2e3d282e287f2246d2bc5c3d4dd92b6314e9b46c20d27737db7a94f7c0e25"
)
PARENT_RESULT_SHA256 = {
    STAGE4N_CONTRACT_RESULT_RELATIVE_PATH: STAGE4N_CONTRACT_RESULT_SHA256,
    STAGE4I_RESULT_RELATIVE_PATH: STAGE4I_RESULT_SHA256,
    STAGE4L_RESULT_RELATIVE_PATH: STAGE4L_RESULT_SHA256,
    STAGE3_RESULT_RELATIVE_PATH: STAGE3_RESULT_SHA256,
    DOBRUSHIN_RESULT_RELATIVE_PATH: DOBRUSHIN_RESULT_SHA256,
}

SOURCE_MANIFEST = (
    SOURCE_RELATIVE_PATH,
    GENERATOR_RELATIVE_PATH,
    NOTE_RELATIVE_PATH,
    TEST_RELATIVE_PATH,
)
DEPENDENCY_SOURCE_MANIFEST = (
    "src/canard_control/directed_interval.py",
    "src/canard_control/"
    "leaky_inner_nonlinear_selected_return_tube_stage4n_contract.py",
    "src/canard_control/leaky_inner_word_primitive_stage4i.py",
    "src/canard_control/leaky_inner_terminal_stable_row_stage4l.py",
    "src/canard_control/leaky_inner_stable_projection_stage3.py",
    "src/canard_control/leaky_dobrushin_transverse_halanay.py",
)

DEFAULT_COMMAND = (
    "OPENBLAS_NUM_THREADS=8 OMP_NUM_THREADS=1 PYTHONPATH=src "
    "/usr/bin/python3 experiments/"
    "leaky_inner_nonlinear_selected_return_tube_stage4n_feasibility.py"
)
ARITHMETIC_SCOPE = (
    "exact-byte binding and normal semantic validation of Stages 4N-contract, "
    "4I, 4L, and 3; exact-byte and certificate-digest validation of the "
    "Dobrushin strip parent; 192-bit outward MPFR evaluation of a Stage-4I-"
    "sharpened scalar row-sum Gronwall test and a Stage-6A-style polynomial "
    "comparison; outward conditional terminal signed-second-variation target; "
    "no nonlinear flow, event, return, Hessian, graph, crossing, or onset "
    "promotion"
)

PRECISION_BITS = 192
STABLE_RADIUS = "0.0097"
UNIT_UNSTABLE_RADIUS = "0.00025"
SPLIT_RADIUS = "0.00995"
EPSILON = "0.2"
KAPPA_1 = "0.004"
KAPPA_3 = "0.005"
DECLARED_CENTERED_VOLTAGE_RADIUS = "2.5"
EXPECTED_NUMERIC_CORE_SHA256 = (
    "50abeab56ee06a439d8a524131bdcc59ccba58fafa6d906b49af45f8fbd1b17e"
)

TRUE_FLAGS = (
    "stage4n_open_contract_bytes_and_semantics_validated",
    "stage4i_four_word_primitive_bytes_and_semantics_validated",
    "stage4l_terminal_linear_center_bytes_and_semantics_validated",
    "stage3_unstable_root_bytes_and_semantics_validated",
    "inner_exact_orbit_strip_parent_bytes_and_digest_validated",
    "preferred_b_enlarged_anisotropic_ball_used",
    "stage4i_sharpened_generic_row_sum_computed_outward",
    "centered_voltage_hessian_semantics_validated",
    "stage6a_style_generic_row_sum_computed_outward",
    "generic_row_sum_gronwall_tube_test_fails",
    "first_numeric_explosion_term_frozen",
    "conditional_signed_second_variation_kernel_target_computed",
    "stage4l_not_substituted_for_nonlinear_flow_tube",
    "common_event_window_semantics_retained",
    "complete_returned_history_semantics_retained",
    "no_earlier_admissible_return_semantics_retained",
)
FALSE_FLAGS = (
    "full_ball_nonlinear_mild_flow_remainder_validated",
    "sharp_signed_intermediate_second_variation_kernel_validated",
    "common_event_window_validated",
    "left_endpoint_event_gap_validated",
    "right_endpoint_event_gap_validated",
    "uniform_positive_event_speed_validated",
    "unique_selected_event_validated",
    "complete_returned_history_tube_validated",
    "returned_history_inside_local_patch_validated",
    "launch_collar_exclusion_validated",
    "no_earlier_admissible_positive_return_validated",
    "selected_return_map_on_full_anisotropic_ball_validated",
    "first_positive_local_return_validated",
    "six_projected_return_hessian_blocks_validated",
    "quantitative_inner_stable_graph_validated",
    "selected_pulse_stable_sheet_crossing_validated",
    "unique_physical_pulse_onset_validated",
    "two_sided_basin_routing_validated",
    "outer_or_quiet_capture_from_both_sides_validated",
    "frequency_amplitude_safety_radius_validated",
    "asynchronous_network_safety_radius_validated",
)


@dataclass(frozen=True)
class Stage4NFeasibilityPilot:
    schema_id: str
    model_id: str
    branch: str
    status: str
    parent_result_sha256: dict[str, str]
    anisotropic_domain: dict[str, Any]
    parent_ingress: dict[str, Any]
    stage4i_sharpened_generic_gronwall: dict[str, Any]
    stage6a_style_generic_gronwall: dict[str, Any]
    first_numeric_explosion: dict[str, Any]
    signed_mild_flow_kernel_interface: dict[str, Any]
    conditional_terminal_kernel_target: dict[str, Any]
    open_event_and_history_ledger: dict[str, Any]
    theorem_boundary: dict[str, Any]
    claim_status: dict[str, bool]


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


def _mapping(value: Any, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{name} is missing")
    return value


def _point(value: object) -> DirectedInterval:
    return DirectedInterval.from_decimal(str(value), PRECISION_BITS)


def _exp(value: DirectedInterval) -> DirectedInterval:
    with gmpy2.context(precision=value.precision, round=gmpy2.RoundDown):
        lower = gmpy2.exp(value.lower)
    with gmpy2.context(precision=value.precision, round=gmpy2.RoundUp):
        upper = gmpy2.exp(value.upper)
    return DirectedInterval(lower, upper, value.precision)


def _interval_record(value: DirectedInterval) -> dict[str, str]:
    return {
        "lower": decimal_lower(value.lower, 70),
        "upper": decimal_upper(value.upper, 70),
    }


def _load_json(repository: Path, relative: str, digest: str) -> Mapping[str, Any]:
    path = repository / relative
    raw = path.read_bytes()
    if sha256(raw).hexdigest() != digest:
        raise ValueError(f"a Stage-4N feasibility parent changed: {relative}")
    return _mapping(json.loads(raw), relative)


def _validate_dobrushin_frozen_parent(
    payload: Mapping[str, Any], repository: Path
) -> None:
    """Validate the frozen strip fields without an expensive theorem replay.

    Exact parent bytes are already bound.  The certificate digest and every
    registered source/parent digest are checked here; the parent's own test
    suite is responsible for its full MPFR recomputation.
    """

    if set(payload) != {"certificate", "manifest"}:
        raise ValueError("the Dobrushin parent schema changed")
    certificate = _mapping(payload.get("certificate"), "Dobrushin certificate")
    manifest = _mapping(payload.get("manifest"), "Dobrushin manifest")
    if manifest.get("certificate_sha256") != canonical_sha256(certificate):
        raise ValueError("the Dobrushin parent certificate digest changed")
    source_hashes = _mapping(
        manifest.get("source_sha256"), "Dobrushin source hashes"
    )
    parent_hashes = _mapping(
        manifest.get("parent_result_sha256"), "Dobrushin parent hashes"
    )
    for relative, digest in source_hashes.items():
        if _sha256_path(repository / str(relative)) != digest:
            raise ValueError(f"a Dobrushin source changed: {relative}")
    for relative, digest in parent_hashes.items():
        if _sha256_path(repository / str(relative)) != digest:
            raise ValueError(f"a Dobrushin parent changed: {relative}")
    inner = _mapping(certificate.get("inner"), "Dobrushin inner branch")
    if (
        inner.get("exact_periodic_orbit_strip_validated") is not True
        or inner.get("branch") != "inner_saddle_candidate"
        or inner.get("declared_centered_voltage_radius")
        != DECLARED_CENTERED_VOLTAGE_RADIUS
    ):
        raise ValueError("the Dobrushin inner strip claim changed")


def _load_and_validate_parents(repository: Path) -> dict[str, Mapping[str, Any]]:
    repository = repository.resolve()
    parents = {
        relative: _load_json(repository, relative, digest)
        for relative, digest in PARENT_RESULT_SHA256.items()
    }
    validate_stage4n_result(
        parents[STAGE4N_CONTRACT_RESULT_RELATIVE_PATH],
        repository,
        recompute=False,
    )
    validate_stage4i_result(parents[STAGE4I_RESULT_RELATIVE_PATH], repository)
    validate_stage4l_result(
        parents[STAGE4L_RESULT_RELATIVE_PATH], repository, recompute=False
    )
    validate_stage3_stable_projection_result(
        parents[STAGE3_RESULT_RELATIVE_PATH], repository
    )
    _validate_dobrushin_frozen_parent(
        parents[DOBRUSHIN_RESULT_RELATIVE_PATH], repository
    )
    return parents


def _stage4i_sharpened_gronwall(
    stage4i: Mapping[str, Any],
    stage4l: Mapping[str, Any],
    dobrushin: Mapping[str, Any],
) -> dict[str, Any]:
    artifact4i = _mapping(stage4i.get("artifact"), "Stage-4I artifact")
    residual = _mapping(
        artifact4i.get("directed_residual_certificate"),
        "Stage-4I residual certificate",
    )
    tubes = _mapping(
        artifact4i.get("directed_primitive_error_tubes"),
        "Stage-4I primitive tubes",
    )
    coefficient = _mapping(
        residual.get("maximum_coefficient_modulus_upper"),
        "Stage-4I coefficient maxima",
    )
    exact_inner = _mapping(
        _mapping(dobrushin.get("certificate"), "Dobrushin certificate").get(
            "inner"
        ),
        "Dobrushin inner branch",
    )
    period = _mapping(
        _mapping(stage4l.get("artifact"), "Stage-4L artifact").get(
            "true_period_and_word_support"
        ),
        "Stage-4L true period",
    )

    radius = _point(SPLIT_RADIUS)
    epsilon = _point(EPSILON)
    kappa3 = _point(KAPPA_3)
    centered_voltage = _point(
        exact_inner["exact_centered_voltage_abs_upper"]
    )
    strip_margin = _point(exact_inner["strict_strip_margin_lower"])
    period_lower = _point(period["true_period_lower"])
    current = _point(coefficient["current"]) + _point(
        tubes["current_coefficient_model_error_upper"]
    )
    delayed0 = _point(coefficient["delayed0"]) + _point(
        tubes["delayed_coefficient_each_model_error_upper"]
    )
    delayed1 = _point(coefficient["delayed1"]) + _point(
        tubes["delayed_coefficient_each_model_error_upper"]
    )

    base_fast_row = current + 1 + delayed0 + delayed1
    # Here B bounds |v-1|, not |v|.  The physical fast-field Hessian rows are
    #   -(2+6 eps k3)v+6 eps k3,
    #   3 eps k3(v_tau0-1),  3 eps k3(v_tau1-1).
    # Thus |v| <= 1+B+r in the current slot, while the cubic centered factors
    # in all three slots are bounded by B+r.  Their absolute row sum is
    # therefore bounded by the expression below.
    hessian_row = 2 * (1 + centered_voltage + radius) + (
        12 * epsilon * kappa3 * (centered_voltage + radius)
    )
    fast_row_on_input_tube = base_fast_row + hessian_row * radius
    flow_row_sum = DirectedInterval.from_bounds(
        max(fast_row_on_input_tube.lower, (2 * epsilon).lower),
        max(fast_row_on_input_tube.upper, (2 * epsilon).upper),
        PRECISION_BITS,
    )
    optimistic_gain = _exp(flow_row_sum * period_lower)
    optimistic_deviation = optimistic_gain * radius
    failure_factor = optimistic_deviation / strip_margin
    if optimistic_deviation.lower <= strip_margin.upper:
        raise ArithmeticError("the Stage-4I-sharpened Gronwall no-go vanished")

    return {
        "comparison_space": (
            "the scalar complete-history Y-radius about the exact inner orbit"
        ),
        "input_radius": SPLIT_RADIUS,
        "exact_inner_centered_voltage_abs_upper": str(
            exact_inner["exact_centered_voltage_abs_upper"]
        ),
        "exact_inner_voltage_bound_coordinate": "centered z=v-1",
        "registered_centered_voltage_strip_margin_lower": str(
            exact_inner["strict_strip_margin_lower"]
        ),
        "exact_period_lower": str(period["true_period_lower"]),
        "why_T_plus_is_at_least_the_exact_period": (
            "the base history x=0 belongs to the ball and its selected "
            "near-period event is the exact period"
        ),
        "stage4i_current_coefficient_plus_model_error": _interval_record(current),
        "stage4i_delayed0_coefficient_plus_model_error": _interval_record(
            delayed0
        ),
        "stage4i_delayed1_coefficient_plus_model_error": _interval_record(
            delayed1
        ),
        "base_fast_jacobian_row_sum": _interval_record(base_fast_row),
        "field_hessian_row_sum_on_input_radius_tube": _interval_record(
            hessian_row
        ),
        "field_hessian_row_formula": (
            "2*(1+B+r)+12*epsilon*kappa3*(B+r), with B=sup|v_*-1|"
        ),
        "stage4i_sharpened_flow_row_sum_on_input_radius_tube": (
            _interval_record(flow_row_sum)
        ),
        "optimistic_generic_flow_gain_through_period_lower": _interval_record(
            optimistic_gain
        ),
        "optimistic_generic_flow_deviation": _interval_record(
            optimistic_deviation
        ),
        "deviation_to_registered_strip_margin_factor": _interval_record(
            failure_factor
        ),
        "decimal_order_failure_lower": decimal_lower(
            gmpy2.log10(failure_factor.lower), 70
        ),
        "closure_test": "exp(L_4I*T_lower)*0.00995 < strip_margin",
        "closure_passes": False,
        "scope_of_no_go": (
            "this falsifies the registered scalar row-sum/Gronwall closure; "
            "it does not lower-bound the true nonlinear flow deviation"
        ),
    }


def _stage6a_style_gronwall(
    stage4l: Mapping[str, Any], dobrushin: Mapping[str, Any]
) -> dict[str, Any]:
    exact_inner = _mapping(
        _mapping(dobrushin.get("certificate"), "Dobrushin certificate").get(
            "inner"
        ),
        "Dobrushin inner branch",
    )
    period = _mapping(
        _mapping(stage4l.get("artifact"), "Stage-4L artifact").get(
            "true_period_and_word_support"
        ),
        "Stage-4L true period",
    )
    radius = _point(SPLIT_RADIUS)
    voltage = _point(exact_inner["exact_centered_voltage_abs_upper"])
    strip_margin = _point(exact_inner["strict_strip_margin_lower"])
    epsilon = _point(EPSILON)
    kappa1 = _point(KAPPA_1)
    kappa3 = _point(KAPPA_3)
    period_lower = _point(period["true_period_lower"])
    voltage_strip = voltage + radius
    fast_row = (
        2
        + (1 + voltage_strip) ** 2
        + 2 * epsilon * kappa1
        + 6 * epsilon * kappa3 * voltage_strip**2
    )
    flow_row = DirectedInterval.from_bounds(
        max(fast_row.lower, (2 * epsilon).lower),
        max(fast_row.upper, (2 * epsilon).upper),
        PRECISION_BITS,
    )
    gain = _exp(flow_row * period_lower)
    deviation = gain * radius
    failure_factor = deviation / strip_margin
    if deviation.lower <= strip_margin.upper:
        raise ArithmeticError("the Stage-6A-style inner Gronwall no-go vanished")
    return {
        "formula": (
            "L=2+(1+B+r)^2+2*epsilon*kappa1+"
            "6*epsilon*kappa3*(B+r)^2"
        ),
        "flow_row_sum": _interval_record(flow_row),
        "optimistic_generic_flow_gain_through_period_lower": _interval_record(
            gain
        ),
        "optimistic_generic_flow_deviation": _interval_record(deviation),
        "deviation_to_registered_strip_margin_factor": _interval_record(
            failure_factor
        ),
        "decimal_order_failure_lower": decimal_lower(
            gmpy2.log10(failure_factor.lower), 70
        ),
        "closure_passes": False,
        "used_as_primary_no_go": False,
        "reason_secondary": (
            "Stage 4I supplies a strictly sharper source-bound coefficient "
            "row sum, which already fails"
        ),
    }


def _conditional_terminal_target(
    stage4l: Mapping[str, Any], stage3: Mapping[str, Any]
) -> dict[str, Any]:
    artifact4l = _mapping(stage4l.get("artifact"), "Stage-4L artifact")
    stable = _mapping(
        artifact4l.get("stable_power_certificate"),
        "Stage-4L stable power certificate",
    )
    certificate3 = _mapping(stage3.get("certificate"), "Stage-3 certificate")
    root = _mapping(certificate3.get("root_bracket"), "Stage-3 root bracket")

    stable_rate = _point(stable["one_step_norm_upper"])
    unstable_exponent_upper = _point(root["root_real_upper"])
    unstable_multiplier = _exp(unstable_exponent_upper)
    stable_radius = _point(STABLE_RADIUS)
    unstable_radius = _point(UNIT_UNSTABLE_RADIUS)
    patch_radius = _point(SPLIT_RADIUS)
    linear_image = (
        stable_rate * stable_radius
        + unstable_multiplier * unstable_radius
    )
    slack = patch_radius - linear_image
    target = 2 * slack / patch_radius**2
    if slack.lower <= 0 or target.lower <= 0:
        raise ArithmeticError("the conditional Stage-4N terminal target vanished")
    return {
        "conditional_local_patch_radius": SPLIT_RADIUS,
        "stage4l_stable_terminal_rate_upper": str(
            stable["one_step_norm_upper"]
        ),
        "stage3_unstable_exponent_upper": str(root["root_real_upper"]),
        "unstable_multiplier_upper": _interval_record(unstable_multiplier),
        "linear_terminal_complete_history_image_upper": _interval_record(
            linear_image
        ),
        "nonlinear_terminal_remainder_slack": _interval_record(slack),
        "kernel_definition": (
            "K_ret bounds the event-aligned complete-history second "
            "derivative after the common event row, time translations, and "
            "fixed q_hat/f_hat correlations are formed before every norm"
        ),
        "quadratic_remainder_formula": (
            "||R(x)-X_*-A*x||_Y <= (K_ret/2)*"
            "(||x_s||_Y+|x_u|)^2"
        ),
        "strict_kernel_target_lower": decimal_lower(target.lower, 70),
        "acceptance_rule": "future source-bound K_ret < strict_kernel_target_lower",
        "actual_signed_event_aligned_kernel_upper": None,
        "target_is_conditional_design_arithmetic_only": True,
        "target_proves_event_existence": False,
        "target_proves_any_stage4m_hessian_block": False,
        "stage4m_six_separate_caps_still_required": True,
    }


def _numeric_core(pilot: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "anisotropic_domain": pilot["anisotropic_domain"],
        "stage4i_sharpened_generic_gronwall": pilot[
            "stage4i_sharpened_generic_gronwall"
        ],
        "stage6a_style_generic_gronwall": pilot[
            "stage6a_style_generic_gronwall"
        ],
        "first_numeric_explosion": pilot["first_numeric_explosion"],
        "conditional_terminal_kernel_target": pilot[
            "conditional_terminal_kernel_target"
        ],
        "open_event_and_history_ledger": pilot[
            "open_event_and_history_ledger"
        ],
        "claim_status": pilot["claim_status"],
    }


def _runtime_record() -> dict[str, str]:
    return {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "gmpy2": gmpy2.version(),
        "mpfr": gmpy2.mpfr_version(),
        "precision_bits": str(PRECISION_BITS),
        "openblas_num_threads": str(os.environ.get("OPENBLAS_NUM_THREADS")),
        "omp_num_threads": str(os.environ.get("OMP_NUM_THREADS")),
    }


def build_stage4n_feasibility_pilot(
    repository: Path,
) -> Stage4NFeasibilityPilot:
    repository = repository.resolve()
    parents = _load_and_validate_parents(repository)
    stage4n = _mapping(
        parents[STAGE4N_CONTRACT_RESULT_RELATIVE_PATH].get("contract"),
        "Stage-4N contract",
    )
    domain = _mapping(
        stage4n.get("coordinate_and_domain_registration"),
        "Stage-4N domain",
    )
    if (
        domain.get("stable_radius_R_s") != STABLE_RADIUS
        or domain.get("unit_unstable_radius_R_u_hat")
        != UNIT_UNSTABLE_RADIUS
        or domain.get("split_radius_sum") != SPLIT_RADIUS
        or domain.get("domain_validated_here") is not False
    ):
        raise ValueError("the inherited Stage-4N open ball changed")

    stage4i = parents[STAGE4I_RESULT_RELATIVE_PATH]
    stage4l = parents[STAGE4L_RESULT_RELATIVE_PATH]
    stage3 = parents[STAGE3_RESULT_RELATIVE_PATH]
    dobrushin = parents[DOBRUSHIN_RESULT_RELATIVE_PATH]
    stage4i_artifact = _mapping(stage4i.get("artifact"), "Stage-4I artifact")
    stage4i_tubes = _mapping(
        stage4i_artifact.get("directed_primitive_error_tubes"),
        "Stage-4I primitive tubes",
    )
    stage4i_grid = _mapping(
        stage4i_artifact.get("guide_and_grid"), "Stage-4I guide grid"
    )
    sharpened = _stage4i_sharpened_gronwall(stage4i, stage4l, dobrushin)
    stage6a_style = _stage6a_style_gronwall(stage4l, dobrushin)
    terminal_target = _conditional_terminal_target(stage4l, stage3)

    claims = {name: True for name in TRUE_FLAGS}
    claims.update({name: False for name in FALSE_FLAGS})
    return Stage4NFeasibilityPilot(
        schema_id=SCHEMA_ID,
        model_id=MODEL_ID,
        branch=BRANCH,
        status=STATUS,
        parent_result_sha256=dict(PARENT_RESULT_SHA256),
        anisotropic_domain={
            "fixed_splitting": "x=X_*+x_s+q_hat*x_u",
            "stable_radius_R_s": STABLE_RADIUS,
            "unit_unstable_radius_R_u_hat": UNIT_UNSTABLE_RADIUS,
            "split_radius_sum": SPLIT_RADIUS,
            "arbitrary_continuous_stable_histories_included": True,
            "domain_validated_by_this_pilot": False,
        },
        parent_ingress={
            "stage4i_use": (
                "directed four-word coefficient maxima and model-error "
                "radii; no sampled trajectory norm"
            ),
            "stage4i_missing_object": (
                "a common signed continuous intermediate history row after "
                "stable deflation"
            ),
            "stage4i_primitive_fields": stage4i_grid["primitive_fields"],
            "stage4i_maximum_guide_entry_upper": stage4i_tubes[
                "maximum_guide_entry_upper"
            ],
            "stage4i_maximum_error_radius_upper": stage4i_tubes[
                "maximum_error_radius_upper"
            ],
            "stage4i_raw_physical_frame_primitive_error_no_go": stage4i_tubes[
                "raw_physical_frame_gronwall_no_go"
            ],
            "stage4l_use": (
                "only the selected terminal linear stable row and exact "
                "intertwining relation"
            ),
            "stage4l_is_not_nonlinear_tube_parent": True,
            "stage3_use": "the source-bound real unstable exponent bracket",
            "dobrushin_use": (
                "the source-bound exact inner voltage amplitude and the "
                "registered centered strip margin"
            ),
        },
        stage4i_sharpened_generic_gronwall=sharpened,
        stage6a_style_generic_gronwall=stage6a_style,
        first_numeric_explosion={
            "name": "generic_total_flow_gain_before_mild_remainder_isolation",
            "source": "stage4i_sharpened_generic_gronwall",
            "failed_inequality": sharpened["closure_test"],
            "failure_factor_lower": sharpened[
                "deviation_to_registered_strip_margin_factor"
            ]["lower"],
            "decimal_order_failure_lower": sharpened[
                "decimal_order_failure_lower"
            ],
            "consequence": (
                "the scalar row-sum route cannot supply the common state "
                "tube needed to test endpoint gaps or event speed"
            ),
            "full_ball_nonlinear_mild_flow_remainder_upper": None,
        },
        signed_mild_flow_kernel_interface={
            "mild_equation": (
                "eta_t=U(t,0)eta_0+integral_0^t U(t,s)N_s(eta_s) ds"
            ),
            "nonlinear_remainder": (
                "N_s(eta)=integral_0^1 (1-lambda) "
                "D2F(X_*s+lambda*eta_s)[eta_s,eta_s] dlambda"
            ),
            "required_sharp_kernel": (
                "one continuous (t,s,theta) signed second-variation kernel "
                "on the complete method-of-steps cover, with stable "
                "deflation or unstable action and all event-translation "
                "terms combined before modulus"
            ),
            "stage4i_four_words_supply_algebraic_skeleton": True,
            "stage4i_primitives_supply_this_kernel_bound": False,
            "stage4l_terminal_row_supplies_this_intermediate_bound": False,
            "initial_history_translation_before_delay_activation_retained": True,
            "complete_theta_range": "-tau_max<=theta<=0",
            "actual_intermediate_kernel_upper": None,
            "first_future_parent": (
                "source-bound signed intermediate first/second-variation "
                "kernel with continuous time-history Bernstein or equivalent "
                "directed coverage"
            ),
        },
        conditional_terminal_kernel_target=terminal_target,
        open_event_and_history_ledger={
            "T_minus": None,
            "T_plus": None,
            "left_endpoint_gap_margin": None,
            "right_endpoint_gap_margin": None,
            "uniform_event_speed_lower": None,
            "common_event_window": None,
            "complete_history_flow_tube_radius": None,
            "complete_returned_history_radius": None,
            "local_patch_radius_validated": None,
            "launch_collar": None,
            "middle_slab_cover": None,
            "no_earlier_admissible_return_margin": None,
            "event_semantics": (
                "one positive-oriented event in a common near-period window"
            ),
            "no_earlier_semantics": (
                "exclude only earlier positive-oriented hits lying in the "
                "local complete-history patch; negative crossings may remain"
            ),
            "coverage_semantics": (
                "cover [T_minus-tau_max,T_plus] continuously, including all "
                "delay activations, initial-history translations, and seams"
            ),
            "evidence_status": "OPEN_AFTER_GENERIC_GRONWALL_FAILURE",
        },
        theorem_boundary={
            "proved_here": (
                "only the source-bound failure of two disclosed generic "
                "Gronwall constructions and a conditional scalar target for "
                "a future signed event-aligned second-variation kernel"
            ),
            "not_proved_here": (
                "a nonlinear mild-flow remainder, common event window, event "
                "speed, selected or first return, complete-history tube, any "
                "projected Hessian block, stable graph, crossing, onset, "
                "routing, capture, or safety theorem"
            ),
            "stage4l_substitution_for_stage4n": False,
            "flagship_files_modified": False,
        },
        claim_status=claims,
    )


def build_stage4n_feasibility_result(repository: Path) -> dict[str, Any]:
    repository = repository.resolve()
    pilot = asdict(build_stage4n_feasibility_pilot(repository))
    return {
        "pilot": pilot,
        "manifest": {
            "schema_id": SCHEMA_ID,
            "result": RESULT_RELATIVE_PATH,
            "default_command": DEFAULT_COMMAND,
            "arithmetic_scope": ARITHMETIC_SCOPE,
            "status": STATUS,
            "pilot_sha256": canonical_sha256(pilot),
            "numeric_core_sha256": canonical_sha256(_numeric_core(pilot)),
            "source_sha256": {
                relative: _sha256_path(repository / relative)
                for relative in SOURCE_MANIFEST
            },
            "dependency_source_sha256": {
                relative: _sha256_path(repository / relative)
                for relative in DEPENDENCY_SOURCE_MANIFEST
            },
            "parent_result_sha256": dict(PARENT_RESULT_SHA256),
            "runtime": _runtime_record(),
        },
    }


def _validate_open_ledger(ledger: Mapping[str, Any]) -> None:
    text_fields = {"event_semantics", "no_earlier_semantics", "coverage_semantics"}
    for name, value in ledger.items():
        if name in text_fields:
            if not isinstance(value, str) or not value:
                raise ValueError("a Stage-4N feasibility semantic field vanished")
        elif name == "evidence_status":
            if value != "OPEN_AFTER_GENERIC_GRONWALL_FAILURE":
                raise ValueError("the Stage-4N feasibility evidence status changed")
        elif value is not None:
            raise ValueError(f"an open Stage-4N feasibility field was filled: {name}")


def validate_stage4n_feasibility_result(
    payload: Mapping[str, Any], repository: Path, *, recompute: bool = True
) -> None:
    repository = repository.resolve()
    if not isinstance(payload, Mapping) or set(payload) != {"pilot", "manifest"}:
        raise ValueError("the Stage-4N feasibility result schema changed")
    pilot = _mapping(payload.get("pilot"), "Stage-4N feasibility pilot")
    manifest = _mapping(payload.get("manifest"), "Stage-4N feasibility manifest")
    if set(pilot) != {field.name for field in fields(Stage4NFeasibilityPilot)}:
        raise ValueError("the Stage-4N feasibility pilot schema changed")
    if (
        pilot.get("schema_id") != SCHEMA_ID
        or pilot.get("model_id") != MODEL_ID
        or pilot.get("branch") != BRANCH
        or pilot.get("status") != STATUS
        or pilot.get("parent_result_sha256") != PARENT_RESULT_SHA256
    ):
        raise ValueError("the Stage-4N feasibility identity changed")

    claims = _mapping(pilot.get("claim_status"), "Stage-4N feasibility claims")
    if set(claims) != set(TRUE_FLAGS) | set(FALSE_FLAGS):
        raise ValueError("the Stage-4N feasibility claim ledger changed")
    if any(claims.get(name) is not True for name in TRUE_FLAGS):
        raise ValueError("a Stage-4N feasibility fact was weakened")
    if any(claims.get(name) is not False for name in FALSE_FLAGS):
        raise ValueError("an open Stage-4N theorem gate was promoted")

    domain = _mapping(pilot.get("anisotropic_domain"), "Stage-4N pilot domain")
    if (
        domain.get("stable_radius_R_s") != STABLE_RADIUS
        or domain.get("unit_unstable_radius_R_u_hat") != UNIT_UNSTABLE_RADIUS
        or domain.get("split_radius_sum") != SPLIT_RADIUS
        or domain.get("arbitrary_continuous_stable_histories_included") is not True
        or domain.get("domain_validated_by_this_pilot") is not False
    ):
        raise ValueError("the Stage-4N pilot ball changed")

    sharpened = _mapping(
        pilot.get("stage4i_sharpened_generic_gronwall"),
        "Stage-4I-sharpened Gronwall row",
    )
    expected_hessian = 2 * (
        1
        + _point(sharpened.get("exact_inner_centered_voltage_abs_upper"))
        + _point(sharpened.get("input_radius"))
    ) + 12 * _point(EPSILON) * _point(KAPPA_3) * (
        _point(sharpened.get("exact_inner_centered_voltage_abs_upper"))
        + _point(sharpened.get("input_radius"))
    )
    if (
        sharpened.get("closure_passes") is not False
        or gmpy2.mpq(
            _mapping(
                sharpened.get("deviation_to_registered_strip_margin_factor"),
                "Stage-4I failure factor",
            )["lower"]
        )
        <= 1
        or "does not lower-bound" not in str(sharpened.get("scope_of_no_go"))
        or sharpened.get("exact_inner_voltage_bound_coordinate")
        != "centered z=v-1"
        or sharpened.get("field_hessian_row_formula")
        != "2*(1+B+r)+12*epsilon*kappa3*(B+r), with B=sup|v_*-1|"
        or sharpened.get("field_hessian_row_sum_on_input_radius_tube")
        != _interval_record(expected_hessian)
    ):
        raise ValueError("the Stage-4I-sharpened Gronwall no-go changed")
    stage6a_style = _mapping(
        pilot.get("stage6a_style_generic_gronwall"),
        "Stage-6A-style Gronwall row",
    )
    if (
        stage6a_style.get("closure_passes") is not False
        or stage6a_style.get("used_as_primary_no_go") is not False
    ):
        raise ValueError("the Stage-6A-style comparison changed")

    explosion = _mapping(
        pilot.get("first_numeric_explosion"), "Stage-4N first explosion"
    )
    if (
        explosion.get("name")
        != "generic_total_flow_gain_before_mild_remainder_isolation"
        or explosion.get("full_ball_nonlinear_mild_flow_remainder_upper")
        is not None
    ):
        raise ValueError("the first Stage-4N numerical obstruction changed")

    kernel = _mapping(
        pilot.get("signed_mild_flow_kernel_interface"),
        "Stage-4N signed kernel interface",
    )
    if (
        kernel.get("stage4i_four_words_supply_algebraic_skeleton") is not True
        or kernel.get("stage4i_primitives_supply_this_kernel_bound") is not False
        or kernel.get("stage4l_terminal_row_supplies_this_intermediate_bound")
        is not False
        or kernel.get("actual_intermediate_kernel_upper") is not None
        or kernel.get("initial_history_translation_before_delay_activation_retained")
        is not True
    ):
        raise ValueError("the Stage-4N signed kernel boundary changed")

    target = _mapping(
        pilot.get("conditional_terminal_kernel_target"),
        "Stage-4N conditional kernel target",
    )
    if (
        gmpy2.mpq(target.get("strict_kernel_target_lower")) <= 0
        or target.get("actual_signed_event_aligned_kernel_upper") is not None
        or target.get("target_is_conditional_design_arithmetic_only") is not True
        or target.get("target_proves_event_existence") is not False
        or target.get("target_proves_any_stage4m_hessian_block") is not False
        or target.get("stage4m_six_separate_caps_still_required") is not True
    ):
        raise ValueError("the conditional Stage-4N kernel target changed")

    _validate_open_ledger(
        _mapping(
            pilot.get("open_event_and_history_ledger"),
            "Stage-4N open event ledger",
        )
    )
    theorem = _mapping(
        pilot.get("theorem_boundary"), "Stage-4N theorem boundary"
    )
    if (
        theorem.get("stage4l_substitution_for_stage4n") is not False
        or theorem.get("flagship_files_modified") is not False
        or "a nonlinear mild-flow remainder" not in str(
            theorem.get("not_proved_here")
        )
        or "stable graph" not in str(theorem.get("not_proved_here"))
    ):
        raise ValueError("the Stage-4N feasibility theorem boundary changed")

    expected_manifest_keys = {
        "schema_id",
        "result",
        "default_command",
        "arithmetic_scope",
        "status",
        "pilot_sha256",
        "numeric_core_sha256",
        "source_sha256",
        "dependency_source_sha256",
        "parent_result_sha256",
        "runtime",
    }
    if set(manifest) != expected_manifest_keys:
        raise ValueError("the Stage-4N feasibility manifest schema changed")
    fixed = {
        "schema_id": SCHEMA_ID,
        "result": RESULT_RELATIVE_PATH,
        "default_command": DEFAULT_COMMAND,
        "arithmetic_scope": ARITHMETIC_SCOPE,
        "status": STATUS,
        "pilot_sha256": canonical_sha256(pilot),
        "numeric_core_sha256": canonical_sha256(_numeric_core(pilot)),
        "parent_result_sha256": PARENT_RESULT_SHA256,
        "runtime": _runtime_record(),
    }
    if any(manifest.get(name) != value for name, value in fixed.items()):
        raise ValueError("the Stage-4N feasibility manifest fixed data changed")
    if manifest.get("numeric_core_sha256") != EXPECTED_NUMERIC_CORE_SHA256:
        raise ValueError("the frozen Stage-4N feasibility numeric core changed")

    source_hashes = _mapping(
        manifest.get("source_sha256"), "Stage-4N feasibility source hashes"
    )
    dependency_hashes = _mapping(
        manifest.get("dependency_source_sha256"),
        "Stage-4N feasibility dependency hashes",
    )
    if set(source_hashes) != set(SOURCE_MANIFEST):
        raise ValueError("the Stage-4N feasibility source set changed")
    if set(dependency_hashes) != set(DEPENDENCY_SOURCE_MANIFEST):
        raise ValueError("the Stage-4N feasibility dependency set changed")
    for relative in SOURCE_MANIFEST:
        if source_hashes.get(relative) != _sha256_path(repository / relative):
            raise ValueError(f"a Stage-4N feasibility source changed: {relative}")
    for relative in DEPENDENCY_SOURCE_MANIFEST:
        if dependency_hashes.get(relative) != _sha256_path(
            repository / relative
        ):
            raise ValueError(f"a Stage-4N feasibility dependency changed: {relative}")
    for relative, digest in PARENT_RESULT_SHA256.items():
        if _sha256_path(repository / relative) != digest:
            raise ValueError(f"a Stage-4N feasibility parent changed: {relative}")

    if recompute:
        expected = json.loads(
            json.dumps(
                asdict(build_stage4n_feasibility_pilot(repository)),
                sort_keys=True,
            )
        )
        if dict(pilot) != expected:
            raise ValueError(
                "the Stage-4N feasibility pilot differs from fresh replay"
            )


__all__ = [
    "ARITHMETIC_SCOPE",
    "BRANCH",
    "DEFAULT_COMMAND",
    "DEPENDENCY_SOURCE_MANIFEST",
    "FALSE_FLAGS",
    "GENERATOR_RELATIVE_PATH",
    "MODEL_ID",
    "NOTE_RELATIVE_PATH",
    "PARENT_RESULT_SHA256",
    "RESULT_RELATIVE_PATH",
    "SCHEMA_ID",
    "SOURCE_MANIFEST",
    "SOURCE_RELATIVE_PATH",
    "STATUS",
    "Stage4NFeasibilityPilot",
    "TEST_RELATIVE_PATH",
    "TRUE_FLAGS",
    "_numeric_core",
    "build_stage4n_feasibility_pilot",
    "build_stage4n_feasibility_result",
    "canonical_sha256",
    "validate_stage4n_feasibility_result",
]
