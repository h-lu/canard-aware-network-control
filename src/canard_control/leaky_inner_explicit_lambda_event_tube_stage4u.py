"""Stage-4U explicit scaled-ball near-two-period event tube.

This module turns the deliberately coarse Stage-4N scalar comparison into a
positive (but extremely small) theorem.  It works in the reduced history
space Y=C([-tau_max,0],R)_v x R_w, keeps exact initial-history translations
inside one global supremum majorant, and runs the comparison from time zero
through the upper end of the fixed near-two-period window.

The certified closed reduced-Y coordinate ball uses lambda_0=9e-31.  A
strictly larger open comparison scale 9.1e-31 is used so the closed ball lies
in an explicit open ambient history neighborhood for the Stage-4R C2 theorem.
The ambient theorem on W_open is then restricted through the fixed section
chart j to D_open=j^{-1}(W_open intersect Sigma_loc).  No preferred-ball,
full-X same-radius ball, event-ordinal, self-map, Hessian, graph, pulse, onset,
routing, capture, or safety statement is proved.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from decimal import Decimal, localcontext
from functools import lru_cache
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
SCHEMA_ID = "leaky-inner-explicit-lambda-event-tube-stage4u-v2"
MODEL_ID = "autonomous-leaky-recovery-two-delay-fhn-bistable-proposal"
BRANCH = "inner_saddle_candidate_selected_near_two_period_event"
STATUS = "PROVED_EXPLICIT_SCALED_REDUCED_Y_BALL_EVENT_TUBE"

SOURCE_RELATIVE_PATH = (
    "src/canard_control/leaky_inner_explicit_lambda_event_tube_stage4u.py"
)
GENERATOR_RELATIVE_PATH = (
    "experiments/leaky_inner_explicit_lambda_event_tube_stage4u.py"
)
RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_inner_explicit_lambda_event_tube_stage4u.json"
)
NOTE_RELATIVE_PATH = "docs/leaky-inner-explicit-lambda-event-tube-stage4u.md"
TEST_RELATIVE_PATH = (
    "tests/test_leaky_inner_explicit_lambda_event_tube_stage4u.py"
)

STAGE4N_FEASIBILITY_RELATIVE_PATH = (
    "experiments/results/"
    "leaky_inner_nonlinear_selected_return_tube_stage4n_feasibility.json"
)
STAGE4N_CONTRACT_RELATIVE_PATH = (
    "experiments/results/"
    "leaky_inner_nonlinear_selected_return_tube_stage4n_contract.json"
)
STAGE4M_RELATIVE_PATH = (
    "experiments/results/"
    "leaky_inner_enlarged_return_hessian_stage4m_contract.json"
)
STAGE2_RELATIVE_PATH = (
    "experiments/results/leaky_inner_stable_manifold_stage2_contract.json"
)
STAGE4L_RELATIVE_PATH = (
    "experiments/results/leaky_inner_terminal_stable_row_stage4l.json"
)
REDUCED_HISTORY_RELATIVE_PATH = (
    "experiments/results/leaky_reduced_history.json"
)
STAGE4R_RELATIVE_PATH = (
    "experiments/results/"
    "finite_delay_eventually_smooth_selected_return_stage4r.json"
)

PARENT_RESULT_SHA256 = {
    STAGE4N_FEASIBILITY_RELATIVE_PATH: (
        "5e7214a2f5ba8ca22649c677a1d054b32342b5cc25966bd8e1da7600c605f1de"
    ),
    STAGE4N_CONTRACT_RELATIVE_PATH: (
        "b64f5230bb870b889fdc341d5d5139ea4ccac6faa7752ff2a5682eb0206cf160"
    ),
    STAGE4M_RELATIVE_PATH: (
        "1a7f89c4c61480a76149b88ae6a15fa40b11425f4d678615af3469b59f75100c"
    ),
    STAGE2_RELATIVE_PATH: (
        "eafa4d07b0558d9d4ce7423969379fa51875fcabce55af89a2378261fdb1e18d"
    ),
    STAGE4L_RELATIVE_PATH: (
        "672f92c7c456a54f39afab7d2a5f92b783311cc0ee5341a4d2e72a588039017e"
    ),
    REDUCED_HISTORY_RELATIVE_PATH: (
        "4555fb765a5060a3767a7ea669deb2f4921b8d7410d7d4e15ad077e552da8870"
    ),
    STAGE4R_RELATIVE_PATH: (
        "4e68835bc3ba5fd44432d98a3b6b1d41506533d66f3353cd500df3e95da76418"
    ),
}

SOURCE_MANIFEST = (
    SOURCE_RELATIVE_PATH,
    GENERATOR_RELATIVE_PATH,
    NOTE_RELATIVE_PATH,
    TEST_RELATIVE_PATH,
)
DEPENDENCY_SOURCE_MANIFEST = (
    "src/canard_control/directed_interval.py",
    "src/canard_control/autonomous_leaky_recovery_bistable.py",
    "src/canard_control/"
    "leaky_inner_nonlinear_selected_return_tube_stage4n_feasibility.py",
    "src/canard_control/"
    "leaky_inner_nonlinear_selected_return_tube_stage4n_contract.py",
    "src/canard_control/"
    "leaky_inner_enlarged_return_hessian_stage4m_contract.py",
    "src/canard_control/leaky_inner_stable_manifold_stage2_contract.py",
    "src/canard_control/leaky_inner_terminal_stable_row_stage4l.py",
    "src/canard_control/leaky_reduced_history.py",
    "src/canard_control/"
    "finite_delay_eventually_smooth_selected_return_stage4r.py",
)

DEFAULT_COMMAND = (
    "OPENBLAS_NUM_THREADS=8 OMP_NUM_THREADS=1 PYTHONPATH=src "
    "/usr/bin/python3 experiments/"
    "leaky_inner_explicit_lambda_event_tube_stage4u.py"
)
ARITHMETIC_SCOPE = (
    "exact-byte and semantic validation of corrected Stage-4N feasibility, "
    "Stage-4N coordinates, the exact Stage-4M section splitting, Stage-2 "
    "Route-C speed, Stage-4L true period and delays, the exact reduced-history "
    "factorization, and the formal Stage-4R C2 theorem; explicit registration "
    "of the global polynomial full-X functional and affine event functional; "
    "256-bit outward MPFR scalar complete-history Gronwall "
    "bootstrap from t=0 through the near-two-period T_plus; directed endpoint "
    "sign, speed, initial/terminal patch, and smoothing margins; no Stage-4S-A "
    "parent and no downstream graph, onset, routing, capture, or safety claim"
)

PRECISION_BITS = 256
STABLE_RADIUS = "0.0097"
UNSTABLE_RADIUS = "0.00025"
SPLIT_RADIUS = "0.00995"
CERTIFIED_LAMBDA = "9e-31"
OPEN_DOMAIN_LAMBDA = "9.1e-31"
HALF_WIDTH = "0.001"
EPSILON = "0.2"
KAPPA_3 = "0.005"
EXPECTED_NUMERIC_CORE_SHA256 = (
    "322dbd248b16c7075648e37e8932c731c90bd82d3b8be495ff30dd60670f6d8d"
)

TRUE_FLAGS = (
    "all_seven_parent_bytes_and_used_semantic_ingress_validated",
    "corrected_centered_voltage_hessian_semantics_inherited",
    "stage4m_exact_section_splitting_semantics_validated",
    "explicit_lambda_lower_bound_validated",
    "strictly_larger_open_y_neighborhood_validated",
    "scaled_ball_includes_arbitrary_continuous_reduced_y_stable_histories",
    "unit_y_coordinate_triangle_used_exactly",
    "ambient_w_open_theorem_and_coordinate_d_open_restriction_distinguished",
    "initial_scaled_ball_inside_local_section_patch",
    "common_solution_existence_through_T_plus_validated",
    "complete_y_history_flow_tube_validated",
    "initial_history_translation_before_delay_activation_retained",
    "all_delay_activation_faces_and_time_history_seams_covered",
    "near_two_period_center_window_validated",
    "half_center_endpoint_margins_on_open_neighborhood_validated",
    "uniform_positive_event_speed_on_open_neighborhood_validated",
    "unique_selected_event_in_common_window_validated",
    "complete_returned_y_history_inside_local_patch_validated",
    "exact_reduced_full_history_lift_and_projection_used",
    "global_polynomial_full_x_field_and_affine_event_domains_registered",
    "strict_stage4r_C2_smoothing_gate_validated",
    "C2_selected_event_and_complete_history_hit_validated",
    "coordinate_output_domain_d_out_registered",
    "induced_local_section_return_validated",
    "physical_time_and_y_norm_preserved",
)

FALSE_FLAGS = (
    "preferred_lambda_one_ball_validated",
    "unscaled_stage4n_nonlinear_tube_validated",
    "same_scaled_ball_self_map_validated",
    "full_x_sup_norm_tube_with_same_y_radius_validated",
    "scaled_ball_contains_arbitrary_full_x_two_component_histories_validated",
    "continuous_history_unit_y_normalization_adapter_numerically_validated",
    "first_positive_return_validated",
    "second_positive_oriented_event_validated",
    "no_earlier_admissible_return_validated",
    "Q_equals_P2_validated",
    "six_projected_return_hessian_blocks_validated",
    "quantitative_inner_stable_graph_validated",
    "selected_pulse_stable_sheet_crossing_validated",
    "biological_onset_or_control_validated",
    "two_sided_routing_validated",
    "outer_or_quiet_capture_validated",
    "frequency_amplitude_safety_radius_validated",
    "asynchronous_network_safety_validated",
    "general_network_canard_theorem_validated",
)


@dataclass(frozen=True)
class Stage4UCertificate:
    schema_id: str
    model_id: str
    branch: str
    status: str
    parent_result_sha256: dict[str, str]
    scaled_domain: dict[str, Any]
    exact_center_window: dict[str, Any]
    corrected_gronwall_bootstrap: dict[str, Any]
    common_event_certificate: dict[str, Any]
    complete_history_and_patch: dict[str, Any]
    reduced_full_bridge_and_regularity: dict[str, Any]
    theorem_boundary: dict[str, Any]
    claim_status: dict[str, bool]


def _sha256_path(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def canonical_sha256(value: Any) -> str:
    encoded = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("utf-8")
    return sha256(encoded).hexdigest()


def _mapping(value: Any, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{name} is not a mapping")
    return value


def _point(value: object) -> DirectedInterval:
    return DirectedInterval.from_decimal(str(value), PRECISION_BITS)


def _exp(value: DirectedInterval) -> DirectedInterval:
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundDown):
        lower = gmpy2.exp(value.lower)
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
        upper = gmpy2.exp(value.upper)
    return DirectedInterval.from_bounds(lower, upper, PRECISION_BITS)


def _record(value: DirectedInterval) -> dict[str, str]:
    return {
        "lower": decimal_lower(value.lower, 110),
        "upper": decimal_upper(value.upper, 110),
    }


def _exact_decimal(value: Decimal) -> str:
    return format(value, "f")


def _load_json(repository: Path, relative: str, digest: str) -> Mapping[str, Any]:
    path = repository / relative
    if _sha256_path(path) != digest:
        raise ValueError(f"the Stage-4U parent bytes changed: {relative}")
    payload = json.loads(path.read_text(encoding="utf-8"))
    return _mapping(payload, relative)


def _load_and_validate_parents(repository: Path) -> dict[str, Mapping[str, Any]]:
    # The registered parents bind their generating runtime in their own
    # manifests.  Calling those validators under a different Python/MPFR host
    # would reject valid exact bytes for a provenance-only runtime mismatch.
    # Stage 4U therefore binds every parent byte exactly here and checks every
    # mathematical ingress it uses below, without replaying a parent in the
    # current host runtime.
    return {
        relative: _load_json(repository, relative, digest)
        for relative, digest in PARENT_RESULT_SHA256.items()
    }


def _require_claim(
    payload: Mapping[str, Any], name: str, expected: bool, parent: str
) -> None:
    claims = _mapping(payload.get("claim_status"), f"{parent} claims")
    if claims.get(name) is not expected:
        raise ValueError(f"{parent} claim changed: {name}")


def _numeric_core(certificate: Mapping[str, Any]) -> dict[str, Any]:
    return {
        name: certificate[name]
        for name in (
            "scaled_domain",
            "exact_center_window",
            "corrected_gronwall_bootstrap",
            "common_event_certificate",
            "complete_history_and_patch",
            "reduced_full_bridge_and_regularity",
        )
    }


def _runtime_record() -> dict[str, str]:
    return {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "gmpy2": gmpy2.version(),
        "mpfr": gmpy2.mpfr_version(),
        "precision_bits": str(PRECISION_BITS),
        "openblas_num_threads": os.environ.get("OPENBLAS_NUM_THREADS", ""),
        "omp_num_threads": os.environ.get("OMP_NUM_THREADS", ""),
    }


@lru_cache(maxsize=4)
def build_stage4u_certificate(repository: Path) -> Stage4UCertificate:
    repository = repository.resolve()
    parents = _load_and_validate_parents(repository)

    feasibility = _mapping(
        parents[STAGE4N_FEASIBILITY_RELATIVE_PATH].get("pilot"),
        "Stage-4N feasibility pilot",
    )
    if (
        feasibility.get("schema_id")
        != "leaky-inner-nonlinear-selected-return-tube-stage4n-feasibility-v1"
        or feasibility.get("model_id") != MODEL_ID
        or feasibility.get("status")
        != "NONCLOSING_SOURCE_BOUND_FEASIBILITY_PILOT"
    ):
        raise ValueError("the corrected Stage-4N feasibility identity changed")
    sharp = _mapping(
        feasibility.get("stage4i_sharpened_generic_gronwall"),
        "corrected Stage-4N sharp row",
    )
    if (
        sharp.get("exact_inner_voltage_bound_coordinate") != "centered z=v-1"
        or sharp.get("field_hessian_row_formula")
        != "2*(1+B+r)+12*epsilon*kappa3*(B+r), with B=sup|v_*-1|"
    ):
        raise ValueError("Stage-4N centered-voltage correction was lost")
    _require_claim(
        feasibility,
        "centered_voltage_hessian_semantics_validated",
        True,
        "Stage-4N feasibility",
    )

    anisotropic = _mapping(
        feasibility.get("anisotropic_domain"), "Stage-4N anisotropic domain"
    )
    if (
        anisotropic.get("stable_radius_R_s") != STABLE_RADIUS
        or anisotropic.get("unit_unstable_radius_R_u_hat")
        != UNSTABLE_RADIUS
        or anisotropic.get("split_radius_sum") != SPLIT_RADIUS
        or anisotropic.get("arbitrary_continuous_stable_histories_included")
        is not True
    ):
        raise ValueError("the inherited anisotropic domain changed")

    stage4n = _mapping(
        parents[STAGE4N_CONTRACT_RELATIVE_PATH].get("contract"),
        "Stage-4N contract",
    )
    if stage4n.get("model_id") != MODEL_ID:
        raise ValueError("the Stage-4N coordinate model changed")
    coordinates = _mapping(
        stage4n.get("coordinate_and_domain_registration"),
        "Stage-4N coordinates",
    )
    if "||q_hat||_Y=1" not in str(coordinates.get("fixed_unit_y_splitting")):
        raise ValueError("the exact unit-Y coordinate triangle changed")

    stage4m = _mapping(
        parents[STAGE4M_RELATIVE_PATH].get("contract"), "Stage-4M contract"
    )
    if (
        stage4m.get("schema_id")
        != "leaky-inner-enlarged-return-hessian-stage4m-contract-v1"
        or stage4m.get("model_id") != MODEL_ID
        or stage4m.get("status") != "NONCLOSING_CONTRACT"
    ):
        raise ValueError("the Stage-4M section-splitting identity changed")
    splitting = _mapping(
        stage4m.get("coordinate_registration"),
        "Stage-4M section splitting",
    )
    expected_splitting = {
        "section_tangent_space": "Sigma_0={h in Y:h_v(0)=0}",
        "physical_pair": "q,f with f(q)=1 on Sigma_0",
        "unit_y_vector": "q_hat=q/||q||_Y",
        "unit_y_functional": "f_hat=||q||_Y*f",
        "normalization": "||q_hat||_Y=1 and f_hat(q_hat)=1 exactly",
        "fixed_projection": "P_s=I-q_hat*f_hat=I-q*f",
        "stable_space": "E_s=ker(f_hat) in Sigma_0",
    }
    if any(
        splitting.get(name) != value
        for name, value in expected_splitting.items()
    ):
        raise ValueError("the exact Stage-4M section splitting changed")
    if splitting.get("normalization_transfer_validated_here") is not False:
        raise ValueError("the open numerical normalization boundary changed")
    _require_claim(
        stage4m,
        "fixed_unit_y_splitting_interface_registered",
        True,
        "Stage-4M",
    )
    _require_claim(
        stage4m,
        "continuous_history_unit_y_normalization_adapter_validated",
        False,
        "Stage-4M",
    )

    stage2 = _mapping(
        parents[STAGE2_RELATIVE_PATH].get("contract"), "Stage-2 contract"
    )
    section = _mapping(
        stage2.get("explicit_voltage_section_audit"),
        "Stage-2 voltage section",
    )
    _require_claim(
        stage2,
        "exact_phase_zero_voltage_section_uniform_speed_on_declared_ball_validated",
        True,
        "Stage-2",
    )
    if section.get("uniform_event_speed_on_declared_section_ball_validated") is not True:
        raise ValueError("the Stage-2 section-ball speed changed")

    stage4l = _mapping(
        parents[STAGE4L_RELATIVE_PATH].get("artifact"), "Stage-4L artifact"
    )
    period = _mapping(
        stage4l.get("true_period_and_word_support"), "Stage-4L period"
    )
    if period.get("complete_true_returned_history_covered") is not True:
        raise ValueError("the complete true returned-history support changed")

    reduced = _mapping(
        parents[REDUCED_HISTORY_RELATIVE_PATH].get("certificate"),
        "reduced-history certificate",
    )
    for name in (
        "projection_has_continuous_split_right_inverse_proved",
        "future_depends_only_on_voltage_history_and_current_recovery_proved",
        "old_recovery_history_flushed_after_one_maximum_delay_proved",
        "full_semiflow_factors_through_reduced_semiflow_proved",
        "compatible_history_range_invariant_after_one_delay_proved",
    ):
        if reduced.get(name) is not True:
            raise ValueError(f"the reduced-history bridge changed: {name}")

    stage4r = _mapping(
        parents[STAGE4R_RELATIVE_PATH].get("theorem"), "Stage-4R theorem"
    )
    for name in (
        "common_window_endpoint_signs_and_speed_imply_unique_selected_event",
        "strict_T_minus_greater_than_2_tau_star_is_C2_sufficient",
        "selected_event_time_and_complete_history_hit_Ck_proved",
        "open_event_domain_and_image_containment_registered",
    ):
        _require_claim(stage4r, name, True, "Stage-4R")

    with localcontext() as context:
        context.prec = 180
        p_lower_d = Decimal(str(period["true_period_lower"]))
        p_upper_d = Decimal(str(period["true_period_upper"]))
        tau_upper_d = Decimal(str(period["tau1_upper"]))
        h_d = Decimal(HALF_WIDTH)
        t_minus_d = Decimal(2) * p_lower_d - h_d
        t_plus_d = Decimal(2) * p_upper_d + h_d
        period_width_d = p_upper_d - p_lower_d
        phase_offset_d = h_d + Decimal(2) * period_width_d
        center_speed_d = Decimal(
            str(section["uniform_event_speed_lower_on_declared_section_ball"])
        )
        half_center_speed_d = center_speed_d / Decimal(2)
        center_gap_d = center_speed_d * h_d
        half_gap_d = center_gap_d / Decimal(2)

    p_lower = _point(_exact_decimal(p_lower_d))
    p_upper = _point(_exact_decimal(p_upper_d))
    t_minus = _point(_exact_decimal(t_minus_d))
    t_plus = _point(_exact_decimal(t_plus_d))
    tau_upper = _point(_exact_decimal(tau_upper_d))
    phase_offset = _point(_exact_decimal(phase_offset_d))
    center_gap = _point(_exact_decimal(center_gap_d))
    half_gap = _point(_exact_decimal(half_gap_d))
    section_radius = _point(section["declared_section_ball_radius"])
    orbit_history_speed = _point(section["physical_orbit_history_speed_upper"])
    center_displacement = orbit_history_speed * phase_offset
    center_patch_margin = section_radius - center_displacement
    smoothing_margin = t_minus - 2 * tau_upper

    if (
        center_patch_margin.lower <= 0
        or smoothing_margin.lower <= 0
        or p_lower.lower <= 0
        or p_upper.lower <= p_lower.lower
    ):
        raise ArithmeticError("the exact-center near-two-period window failed")

    beta = half_gap
    centered_voltage = _point(
        sharp["exact_inner_centered_voltage_abs_upper"]
    )
    base_fast_row = _point(
        _mapping(
            sharp["base_fast_jacobian_row_sum"], "Stage-4N base row"
        )["upper"]
    )
    epsilon = _point(EPSILON)
    kappa3 = _point(KAPPA_3)
    hessian_beta = 2 * (1 + centered_voltage + beta) + (
        12 * epsilon * kappa3 * (centered_voltage + beta)
    )
    nonlinear_fast_row = base_fast_row + hessian_beta * beta
    flow_row = DirectedInterval.from_bounds(
        max(nonlinear_fast_row.lower, (2 * epsilon).lower),
        max(nonlinear_fast_row.upper, (2 * epsilon).upper),
        PRECISION_BITS,
    )
    gain = _exp(flow_row * t_plus)
    split_radius = _point(SPLIT_RADIUS)
    closed_lambda = _point(CERTIFIED_LAMBDA)
    open_lambda = _point(OPEN_DOMAIN_LAMBDA)
    closed_initial_radius = closed_lambda * split_radius
    open_initial_radius = open_lambda * split_radius
    open_flow_deviation = gain * open_initial_radius
    bootstrap_slack = beta - open_flow_deviation
    lambda_ceiling = beta / (split_radius * gain)
    strip_margin = _point(sharp["registered_centered_voltage_strip_margin_lower"])
    strip_slack = strip_margin - beta

    if (
        open_lambda.lower <= closed_lambda.upper
        or bootstrap_slack.lower <= 0
        or strip_slack.lower <= 0
        or lambda_ceiling.lower <= open_lambda.upper
    ):
        raise ArithmeticError("the explicit Stage-4U Gronwall bootstrap failed")

    endpoint_gap = center_gap - open_flow_deviation
    endpoint_half_margin_slack = endpoint_gap - half_gap
    full_window_y_radius = center_displacement + open_flow_deviation
    terminal_patch_margin = section_radius - full_window_y_radius
    orbit_event_speed = _point(section["physical_voltage_event_speed_at_orbit_lower"])
    field_lipschitz = _point(
        section["vector_field_lipschitz_upper_on_declared_section_ball"]
    )
    event_speed = orbit_event_speed - field_lipschitz * full_window_y_radius
    half_center_speed = _point(_exact_decimal(half_center_speed_d))
    speed_half_margin_slack = event_speed - half_center_speed

    if (
        endpoint_half_margin_slack.lower <= 0
        or terminal_patch_margin.lower <= 0
        or event_speed.lower <= 0
        or speed_half_margin_slack.lower <= 0
    ):
        raise ArithmeticError("a Stage-4U event or terminal-patch gate failed")

    claims = {name: True for name in TRUE_FLAGS}
    claims.update({name: False for name in FALSE_FLAGS})
    return Stage4UCertificate(
        schema_id=SCHEMA_ID,
        model_id=MODEL_ID,
        branch=BRANCH,
        status=STATUS,
        parent_result_sha256=dict(PARENT_RESULT_SHA256),
        scaled_domain={
            "history_space": (
                "Y=C([-tau_max,0],R)_v x R_w with "
                "||(phi,w)||_Y=max(||phi||_infinity,|w|)"
            ),
            "coordinate_space": "M=E_s x R with E_s=ker(f_hat) in Sigma_0",
            "fixed_coordinate_injection": (
                "j(x_s,x_u)=Y_*+x_s+q_hat*x_u, x_s in ker(f_hat), "
                "q_hat in Sigma_0, ||q_hat||_Y=1, and "
                "f_hat(q_hat)=1 exactly"
            ),
            "stable_radius_R_s": STABLE_RADIUS,
            "unit_unstable_radius_R_u_hat": UNSTABLE_RADIUS,
            "radius_sum": SPLIT_RADIUS,
            "certified_closed_lambda_lower": CERTIFIED_LAMBDA,
            "strict_open_domain_lambda": OPEN_DOMAIN_LAMBDA,
            "closed_ball": (
                "B_lambda={||x_s||_Y<=0.0097*lambda, "
                "|x_u|<=0.00025*lambda}"
            ),
            "closed_ball_initial_y_radius": _record(closed_initial_radius),
            "ambient_open_history_neighborhood": (
                "W_open={y in Y:||y-Y_*||_Y<0.00995*(9.1e-31)}"
            ),
            "ambient_open_y_radius": _record(open_initial_radius),
            "coordinate_open_domain": (
                "D_open=j^{-1}(W_open intersect Sigma_loc), open in M"
            ),
            "explicit_coordinate_diamond_subset": (
                "D_diamond={||x_s||_Y+|x_u|<0.00995*(9.1e-31)} "
                "is contained in D_open"
            ),
            "anisotropic_absorption": (
                "||x_s+q_hat*x_u||_Y<=||x_s||_Y+|x_u|; "
                "B_(9e-31) is strictly inside D_diamond and hence D_open"
            ),
            "arbitrary_continuous_reduced_y_stable_histories_included": True,
            "arbitrary_full_x_two_component_histories_included": False,
            "normalization_adapter_numerically_promoted": False,
        },
        exact_center_window={
            "period_lower": _exact_decimal(p_lower_d),
            "period_upper": _exact_decimal(p_upper_d),
            "period_width": _exact_decimal(period_width_d),
            "tau_max_upper": _exact_decimal(tau_upper_d),
            "half_width_h": HALF_WIDTH,
            "T_minus": _exact_decimal(t_minus_d),
            "T_plus": _exact_decimal(t_plus_d),
            "maximum_phase_offset_from_2P": _record(phase_offset),
            "physical_orbit_history_speed_upper": str(
                section["physical_orbit_history_speed_upper"]
            ),
            "center_window_y_displacement": _record(center_displacement),
            "declared_local_section_patch_radius": str(
                section["declared_section_ball_radius"]
            ),
            "center_patch_margin": _record(center_patch_margin),
            "center_uniform_event_speed_lower": str(
                section["uniform_event_speed_lower_on_declared_section_ball"]
            ),
            "center_endpoint_gap_lower": _exact_decimal(center_gap_d),
            "target_half_endpoint_gap": _exact_decimal(half_gap_d),
            "T_minus_minus_2_tau_max": _record(smoothing_margin),
            "center_event_time": "T(Y_*)=2P exactly",
            "center_returned_history": "Psi_(2P)(Y_*)=Y_* exactly",
        },
        corrected_gronwall_bootstrap={
            "comparison_horizon": "all physical times 0<=t<=T_plus",
            "periodic_coefficient_extension": (
                "the source-bound A0 and B maxima cover one exact period and "
                "repeat on [0,T_plus] by exact periodicity of Y_*"
            ),
            "bootstrap_y_radius_beta": _record(beta),
            "beta_choice": "one half of the certified center endpoint gap",
            "exact_orbit_centered_voltage_abs_upper": str(
                sharp["exact_inner_centered_voltage_abs_upper"]
            ),
            "centered_voltage_coordinate": "B=sup|v_*-1|",
            "base_fast_jacobian_row_sum_upper": str(
                _mapping(
                    sharp["base_fast_jacobian_row_sum"],
                    "Stage-4N base row",
                )["upper"]
            ),
            "corrected_hessian_row_formula": (
                "H_beta=2*(1+B+beta)+12*epsilon*kappa3*(B+beta)"
            ),
            "corrected_hessian_row_at_beta": _record(hessian_beta),
            "flow_row_formula": (
                "L_beta=max(A0+H_beta*beta,2*epsilon)"
            ),
            "flow_row_upper": _record(flow_row),
            "gain_formula": "G_beta=exp(L_beta*T_plus)",
            "complete_history_flow_gain": _record(gain),
            "open_domain_flow_deviation": _record(open_flow_deviation),
            "bootstrap_slack_beta_minus_deviation": _record(bootstrap_slack),
            "strict_open_lambda_ceiling": _record(lambda_ceiling),
            "centered_strip_slack": _record(strip_slack),
            "majorant_definition": (
                "M(t)=max(||eta_v||_[-tau,0],|eta_w(0)|,"
                "sup_(0<=s<=t) max(|eta_v(s)|,|eta_w(s)|))"
            ),
            "directed_integral_inequality": (
                "M(t)<=rho_open+integral_0^t L_beta*M(s) ds"
            ),
            "exit_time_argument": (
                "if beta were first reached by T_plus, Gronwall would give "
                "M<=rho_open*exp(L_beta*T_plus)<beta, a contradiction"
            ),
            "continuation_argument": (
                "the reduced polynomial finite-delay field is bounded on "
                "the resulting orbit-centered tube, so no finite maximal "
                "solution endpoint can occur before T_plus"
            ),
        },
        common_event_certificate={
            "common_window": (
                f"[{_exact_decimal(t_minus_d)},{_exact_decimal(t_plus_d)}]"
            ),
            "event_functional": "g_Y(y)=y_v(0)-Y_*,v(0), ||Dg_Y||=1",
            "same_time_event_perturbation_upper": _record(open_flow_deviation),
            "left_endpoint_sign": (
                "sup_(y in W_open) g_Y(Psi_Tminus(y)) "
                "<=-endpoint_gap_lower<0"
            ),
            "right_endpoint_sign": (
                "inf_(y in W_open) g_Y(Psi_Tplus(y)) "
                ">=endpoint_gap_lower>0"
            ),
            "endpoint_gap_lower": _record(endpoint_gap),
            "advertised_half_gap_target": _record(half_gap),
            "endpoint_margin_beyond_half_target": _record(
                endpoint_half_margin_slack
            ),
            "window_y_radius_about_phase_zero_center": _record(
                full_window_y_radius
            ),
            "event_speed_formula": (
                "a_open=a_orbit_lower-L_F_upper*"
                "(center_displacement+flow_deviation)"
            ),
            "uniform_event_speed_lower": _record(event_speed),
            "advertised_half_center_speed_target": _record(half_center_speed),
            "speed_margin_beyond_half_target": _record(speed_half_margin_slack),
            "existence_and_uniqueness": (
                "endpoint signs give existence by continuity; the uniform "
                "positive physical speed gives strict monotonicity and one "
                "unique selected event in this window"
            ),
            "orientation": "positive physical voltage-event orientation",
            "event_ordinal": None,
        },
        complete_history_and_patch={
            "initial_translation_rule": (
                "when s-tau_j<0 the delayed difference is the exact arbitrary "
                "initial-history translate and is bounded by rho_open; when "
                "s-tau_j>=0 it is bounded by M(s)"
            ),
            "activation_and_seam_rule": (
                "the single continuous integral majorant covers every "
                "t=tau_j activation face and every later method-of-steps/time-"
                "history seam; no time or history-node sampling is used"
            ),
            "physical_cover": (
                "given initial histories cover [-tau_max,0], and the majorant "
                "covers [0,T_plus], hence in particular every complete "
                "returned-history time in [T_minus-tau_max,T_plus]"
            ),
            "flow_tube_statement": (
                "sup_(y in W_open,0<=t<=T_plus) "
                "||Psi_t(y)-Psi_t(Y_*)||_Y<=flow_deviation_upper"
            ),
            "moving_event_history_bound": (
                "||Psi_{T(y)}(y)-Y_*||_Y<="
                "||Psi_{T(y)}(y)-Psi_{T(y)}(Y_*)||_Y+"
                "||Psi_{T(y)}(Y_*)-Y_*||_Y"
            ),
            "complete_returned_y_history_radius": _record(full_window_y_radius),
            "terminal_patch": (
                "Sigma_loc={y:g_Y(y)=0 and ||y-Y_*||_Y<R0}, "
                f"R0={section['declared_section_ball_radius']}"
            ),
            "terminal_patch_margin": _record(terminal_patch_margin),
            "initial_patch_margin": _record(
                section_radius - closed_initial_radius
            ),
            "initial_section_membership": (
                "the direct Stage-4M parent gives E_s=ker(f_hat) in Sigma_0, "
                "q_hat in Sigma_0, and f_hat(q_hat)=1; hence j(D_open) is in "
                "W_open intersect Sigma_loc and every injected B_lambda "
                "history lies there"
            ),
            "terminal_section_membership": (
                "the selected-event equation gives g_Y=0 and the complete-Y "
                "history bound gives strict local-patch containment"
            ),
            "same_scaled_ball_self_map": False,
        },
        reduced_full_bridge_and_regularity={
            "full_phase_space": "X=C([-tau_max,0],R^2)",
            "full_field_regularity": (
                "the model functional F:X->R^2 is a finite-evaluation "
                "polynomial, hence globally C-infinity; take the Stage-4R "
                "functional domain U=X"
            ),
            "full_event_functional": (
                "g_X(phi)=phi_v(0)-Y_*,v(0)=g_Y(pi(phi)) is globally "
                "affine C-infinity; take the Stage-4R event domain V=X"
            ),
            "reduced_projection": "pi(phi_v,phi_w)=(phi_v,phi_w(0))",
            "compatible_lift": str(reduced["compatible_lift_formula"]),
            "semiflow_intertwining": str(reduced["reduced_semiflow_formula"]),
            "full_future_factorization": str(
                reduced["future_factorization_formula"]
            ),
            "full_solution_domain_consequence": (
                "the reduced common-existence proof and exact compatible lift "
                "place (t,Iota(y)) in the full-X maximal semiflow domain for "
                "0<=t<=T_plus and y in W_open"
            ),
            "full_x_same_radius_claimed": False,
            "smoothing_gate": "T_minus>2*tau_max",
            "smoothing_margin": _record(smoothing_margin),
            "stage4r_application": (
                "first apply Stage-4R with parameter domain W_open subset Y, "
                "initial parameterization Iota:W_open->X, U=V=X, and "
                "g_X=g_Y o pi; then compose the full hit with bounded pi and "
                "restrict through j:D_open->W_open intersect Sigma_loc"
            ),
            "ambient_C2_event_time": "T_tilde:W_open->R is C2",
            "ambient_C2_reduced_hit": (
                "R_tilde_Y(y)=Psi_{T_tilde(y)}(y):W_open->Y is C2"
            ),
            "coordinate_C2_restriction": (
                "T=T_tilde o j:D_open->R and "
                "R_Y=R_tilde_Y o j:D_open->Sigma_loc are C2"
            ),
            "terminal_chart": (
                "chi(y)=(P_s(y-Y_*),f_hat(y-Y_*)) on Sigma_loc is affine "
                "C-infinity with inverse j; D_out=chi(Sigma_loc) is open in M"
            ),
            "coordinate_output_domain": "D_out=chi(Sigma_loc)",
            "induced_return": (
                "P_sel=chi o R_tilde_Y o j:D_open->D_out is a C2 selected "
                "local-section return; no D_out subset D_open or self-map "
                "assertion is made"
            ),
        },
        theorem_boundary={
            "proved_here": (
                "the explicit lower scale lambda_0=9e-31, a strictly larger "
                "ambient open reduced-history neighborhood W_open and its "
                "coordinate restriction D_open, common existence through the "
                "fixed near-two-period window, two endpoint signs retaining "
                "the registered half margins, uniform positive speed, one "
                "unique selected event, ambient and coordinate-restricted C2 "
                "event/hit maps, and initial/terminal local reduced-section "
                "containment with output domain D_out"
            ),
            "not_proved_here": (
                "lambda=1, a same-ball self-map, a full-X tube with the same "
                "Y radius or a scaled ball of arbitrary full-X two-component "
                "histories, event ordinal or no-earlier-return statement, "
                "Q=P^2, any projected Hessian block, stable graph, pulse "
                "crossing, biological onset/control, routing, capture, safety "
                "radius, or general-network canard theorem"
            ),
            "stage4s_a_result_is_a_parent": False,
            "stage4s_a_files_modified": False,
        },
        claim_status=claims,
    )


def build_stage4u_result(repository: Path) -> dict[str, Any]:
    repository = repository.resolve()
    certificate = asdict(build_stage4u_certificate(repository))
    return {
        "certificate": certificate,
        "manifest": {
            "schema_id": SCHEMA_ID,
            "result": RESULT_RELATIVE_PATH,
            "default_command": DEFAULT_COMMAND,
            "arithmetic_scope": ARITHMETIC_SCOPE,
            "status": STATUS,
            "certificate_sha256": canonical_sha256(certificate),
            "numeric_core_sha256": canonical_sha256(_numeric_core(certificate)),
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


def validate_stage4u_result(
    payload: Mapping[str, Any], repository: Path, *, recompute: bool = True
) -> None:
    repository = repository.resolve()
    if not isinstance(payload, Mapping) or set(payload) != {"certificate", "manifest"}:
        raise ValueError("the Stage-4U result schema changed")
    certificate = _mapping(payload.get("certificate"), "Stage-4U certificate")
    manifest = _mapping(payload.get("manifest"), "Stage-4U manifest")
    if set(certificate) != {field.name for field in fields(Stage4UCertificate)}:
        raise ValueError("the Stage-4U certificate schema changed")
    expected = asdict(build_stage4u_certificate(repository))
    if certificate != expected:
        raise ValueError("the Stage-4U theorem statement or arithmetic changed")

    claims = _mapping(certificate.get("claim_status"), "Stage-4U claims")
    if set(claims) != set(TRUE_FLAGS) | set(FALSE_FLAGS):
        raise ValueError("the Stage-4U claim ledger changed")
    if any(claims.get(name) is not True for name in TRUE_FLAGS):
        raise ValueError("a proved Stage-4U gate was weakened")
    if any(claims.get(name) is not False for name in FALSE_FLAGS):
        raise ValueError("an open downstream Stage-4U gate was promoted")

    expected_manifest_keys = {
        "schema_id",
        "result",
        "default_command",
        "arithmetic_scope",
        "status",
        "certificate_sha256",
        "numeric_core_sha256",
        "source_sha256",
        "dependency_source_sha256",
        "parent_result_sha256",
        "runtime",
    }
    if set(manifest) != expected_manifest_keys:
        raise ValueError("the Stage-4U manifest schema changed")
    fixed = {
        "schema_id": SCHEMA_ID,
        "result": RESULT_RELATIVE_PATH,
        "default_command": DEFAULT_COMMAND,
        "arithmetic_scope": ARITHMETIC_SCOPE,
        "status": STATUS,
        "certificate_sha256": canonical_sha256(certificate),
        "numeric_core_sha256": canonical_sha256(_numeric_core(certificate)),
        "parent_result_sha256": PARENT_RESULT_SHA256,
    }
    if any(manifest.get(name) != value for name, value in fixed.items()):
        raise ValueError("the Stage-4U manifest fixed data changed")
    if manifest.get("numeric_core_sha256") != EXPECTED_NUMERIC_CORE_SHA256:
        raise ValueError("the frozen Stage-4U numeric core changed")
    runtime = _mapping(manifest.get("runtime"), "Stage-4U runtime provenance")
    if (
        set(runtime) != set(_runtime_record())
        or runtime.get("precision_bits") != str(PRECISION_BITS)
    ):
        raise ValueError("the Stage-4U runtime provenance schema changed")

    source_hashes = _mapping(manifest.get("source_sha256"), "Stage-4U sources")
    dependency_hashes = _mapping(
        manifest.get("dependency_source_sha256"), "Stage-4U dependencies"
    )
    if set(source_hashes) != set(SOURCE_MANIFEST):
        raise ValueError("the Stage-4U source set changed")
    if set(dependency_hashes) != set(DEPENDENCY_SOURCE_MANIFEST):
        raise ValueError("the Stage-4U dependency set changed")
    for relative in SOURCE_MANIFEST:
        if source_hashes.get(relative) != _sha256_path(repository / relative):
            raise ValueError(f"a Stage-4U source changed: {relative}")
    for relative in DEPENDENCY_SOURCE_MANIFEST:
        if dependency_hashes.get(relative) != _sha256_path(repository / relative):
            raise ValueError(f"a Stage-4U dependency changed: {relative}")
    for relative, digest in PARENT_RESULT_SHA256.items():
        if _sha256_path(repository / relative) != digest:
            raise ValueError(f"a Stage-4U parent changed: {relative}")

    if recompute:
        replay = build_stage4u_result(repository)
        if replay["certificate"] != certificate or replay["manifest"][
            "numeric_core_sha256"
        ] != manifest["numeric_core_sha256"]:
            raise ValueError("the Stage-4U mathematics differs from fresh replay")


__all__ = [
    "CERTIFIED_LAMBDA",
    "EXPECTED_NUMERIC_CORE_SHA256",
    "FALSE_FLAGS",
    "OPEN_DOMAIN_LAMBDA",
    "PARENT_RESULT_SHA256",
    "RESULT_RELATIVE_PATH",
    "SOURCE_MANIFEST",
    "Stage4UCertificate",
    "TRUE_FLAGS",
    "_numeric_core",
    "build_stage4u_certificate",
    "build_stage4u_result",
    "canonical_sha256",
    "validate_stage4u_result",
]
