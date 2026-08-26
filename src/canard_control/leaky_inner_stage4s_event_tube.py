"""Stage-4S-A qualitative near-two-period selected-event tube.

This artifact closes the smallest theorem supported by the present source-bound
evidence.  It does *not* close the preferred Stage-4N ball.  Instead it proves
that some nonzero common scaling of that anisotropic ball has a common physical
near-two-period event window, a uniform positive event speed, and terminal
containment in the exact phase-zero voltage-section patch.

The proof has three layers.  First, exact parent intervals give a numerical
certificate on the validated periodic center.  Second, the exact recovery-
history lift/projection factorization transfers the Stage-4R full-history
smoothness theorem to the reduced history space.  Third, openness of the RFDE
semiflow domain, continuous dependence on continuous histories, and compactness
of the fixed time window give an existential scaling lambda_*>0 only after the
initial and terminal section domains are imposed.  No numerical lower bound
for lambda_* is claimed.  Consequently the original lambda=1 Stage-4N ball, a quantitative
nonlinear flow remainder, first/second-return ordinal semantics, Q=P^2,
Hessian blocks, a stable graph, pulse-sheet crossing, biological onset,
routing, capture, and safety all remain open.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from decimal import Decimal, localcontext
from hashlib import sha256
import json
from pathlib import Path
import platform
from typing import Any, Mapping

from canard_control.leaky_reduced_history import (
    validate_leaky_reduced_history_result,
)


SCHEMA_ID = "leaky-inner-stage4s-event-tube-v2"
STATUS = (
    "PROVED_NUMERIC_CENTER_AND_QUALITATIVE_NONZERO_SCALED_FULL_BALL__"
    "PREFERRED_FULL_BALL_OPEN"
)
MODEL_ID = "autonomous-leaky-recovery-two-delay-fhn-bistable-proposal"
BRANCH = "inner_saddle_candidate_selected_near_two_period_event"

SOURCE_RELATIVE_PATH = (
    "src/canard_control/leaky_inner_stage4s_event_tube.py"
)
GENERATOR_RELATIVE_PATH = "experiments/leaky_inner_stage4s_event_tube.py"
RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_inner_stage4s_event_tube.json"
)
NOTE_RELATIVE_PATH = "docs/leaky_inner_stage4s_event_tube.md"
TEST_RELATIVE_PATH = "tests/test_leaky_inner_stage4s_event_tube.py"

SOURCE_MANIFEST = (
    SOURCE_RELATIVE_PATH,
    GENERATOR_RELATIVE_PATH,
    NOTE_RELATIVE_PATH,
    TEST_RELATIVE_PATH,
)

PARENT_RESULT_SHA256 = {
    "experiments/results/autonomous_leaky_recovery_inner_branch_artifact.json": (
        "bee1da065d213c3c33d724ced1dba37c5914934515c1128588919bed34abe69b"
    ),
    "experiments/results/finite_delay_eventually_smooth_selected_return_stage4r.json": (
        "4e68835bc3ba5fd44432d98a3b6b1d41506533d66f3353cd500df3e95da76418"
    ),
    "experiments/results/leaky_inner_event_aligned_return_hessian_stage4o_contract.json": (
        "dc0e3951cb529dbdca384ff548ab0d7cd7786fe02573741e80e9c945452b2a23"
    ),
    "experiments/results/leaky_inner_enlarged_return_hessian_stage4m_contract.json": (
        "1a7f89c4c61480a76149b88ae6a15fa40b11425f4d678615af3469b59f75100c"
    ),
    "experiments/results/leaky_inner_graph_closure_arithmetic_stage4p.json": (
        "860a51d51648919f74bd7bd4e8230a629f7864b2bdcccf490aab5ff9e8e6b542"
    ),
    "experiments/results/leaky_inner_nonlinear_selected_return_tube_stage4n_contract.json": (
        "b64f5230bb870b889fdc341d5d5139ea4ccac6faa7752ff2a5682eb0206cf160"
    ),
    "experiments/results/leaky_inner_nonlinear_selected_return_tube_stage4n_feasibility.json": (
        "5e7214a2f5ba8ca22649c677a1d054b32342b5cc25966bd8e1da7600c605f1de"
    ),
    "experiments/results/leaky_inner_signed_second_variation_stage4q_pilot.json": (
        "e4481bca2d021517073216dab15ee91c43cf301822b15e337c1b5061e9aaf49a"
    ),
    "experiments/results/leaky_inner_stable_manifold_stage2_contract.json": (
        "eafa4d07b0558d9d4ce7423969379fa51875fcabce55af89a2378261fdb1e18d"
    ),
    "experiments/results/leaky_inner_stable_projection_stage3.json": (
        "9ea776a6e627745ded7f7023523999bfbd29a0be4878172c76512d623146e2ea"
    ),
    "experiments/results/leaky_inner_terminal_stable_row_stage4l.json": (
        "672f92c7c456a54f39afab7d2a5f92b783311cc0ee5341a4d2e72a588039017e"
    ),
    "experiments/results/leaky_reduced_history.json": (
        "4555fb765a5060a3767a7ea669deb2f4921b8d7410d7d4e15ad077e552da8870"
    ),
}

PARENT_OBJECT_KEYS = {
    "autonomous_leaky_recovery_inner_branch_artifact.json": "artifact",
    "finite_delay_eventually_smooth_selected_return_stage4r.json": "theorem",
    "leaky_inner_event_aligned_return_hessian_stage4o_contract.json": "contract",
    "leaky_inner_enlarged_return_hessian_stage4m_contract.json": "contract",
    "leaky_inner_graph_closure_arithmetic_stage4p.json": "design",
    "leaky_inner_nonlinear_selected_return_tube_stage4n_contract.json": "contract",
    "leaky_inner_nonlinear_selected_return_tube_stage4n_feasibility.json": "pilot",
    "leaky_inner_signed_second_variation_stage4q_pilot.json": "pilot",
    "leaky_inner_stable_manifold_stage2_contract.json": "contract",
    "leaky_inner_stable_projection_stage3.json": "certificate",
    "leaky_inner_terminal_stable_row_stage4l.json": "artifact",
    "leaky_reduced_history.json": "certificate",
}

DEFAULT_COMMAND = (
    "PYTHONPATH=src /usr/bin/python3 "
    "experiments/leaky_inner_stage4s_event_tube.py"
)
ARITHMETIC_SCOPE = (
    "exact parent-byte and declared-source validation; 120-digit Decimal "
    "arithmetic on directed parent endpoints; exact full-X/reduced-Y recovery-"
    "history lift/projection; compact-window continuous-dependence/open-domain "
    "argument; Stage-4R C2 selected-event theorem on full X; "
    "no numerical lambda lower bound and no preferred-ball promotion"
)

TOP_KEYS = {"certificate", "manifest"}
MANIFEST_KEYS = {
    "schema_id",
    "result",
    "default_command",
    "arithmetic_scope",
    "certificate_sha256",
    "numeric_core_sha256",
    "source_sha256",
    "parent_result_sha256",
    "parent_source_manifest_sha256",
    "runtime",
}

TRUE_FLAGS = (
    "all_parent_bytes_and_declared_sources_validated",
    "exact_periodic_RFDE_center_validated",
    "physical_two_period_center_window_validated",
    "center_window_histories_inside_declared_voltage_section_ball",
    "center_endpoint_event_gap_margins_validated",
    "center_uniform_positive_event_speed_validated",
    "center_C2_smoothing_margin_validated",
    "center_returned_history_equals_X_star",
    "exact_reduced_history_lift_projection_bridge_validated",
    "reduced_Y_joint_C2_smoothing_corollary_proved",
    "full_X_and_reduced_Y_event_functions_intertwined",
    "qualitative_nonzero_scaled_full_ball_event_tube_proved",
    "scaled_ball_includes_arbitrary_continuous_stable_histories",
    "common_fixed_event_window_on_scaled_full_ball_proved",
    "uniform_positive_event_speed_on_scaled_full_ball_proved",
    "unique_selected_event_in_fixed_window_on_scaled_full_ball_proved",
    "C2_selected_event_hit_on_open_neighborhood_of_scaled_ball_proved",
    "terminal_exact_section_patch_containment_on_scaled_full_ball_proved",
    "induced_section_return_requires_and_has_terminal_chart_containment",
    "initial_section_chart_domain_imposed_before_lambda_choice",
    "terminal_return_preimage_domain_imposed_before_lambda_choice",
    "initial_injection_image_inside_local_section_patch",
    "terminal_chart_codomain_explicitly_registered",
    "selected_window_event_distinguished_from_event_ordinal",
    "stage4o_p_q_r_claim_boundaries_preserved",
    "physical_time_and_history_norm_normalization_preserved",
)

FALSE_FLAGS = (
    "preferred_lambda_one_full_ball_validated",
    "numerical_lambda_star_lower_bound_validated",
    "explicit_preferred_ball_nonlinear_mild_flow_remainder_validated",
    "explicit_scaled_ball_flow_tube_radius_validated",
    "explicit_selected_return_Lipschitz_or_C2_norm_validated",
    "continuous_history_unit_y_normalization_adapter_numerically_validated",
    "return_is_self_map_of_same_scaled_anisotropic_ball_validated",
    "first_positive_return_validated",
    "two_period_event_is_second_positive_oriented_hit_validated",
    "Q_equals_P2_validated",
    "one_period_map_C2_on_full_history_space_validated",
    "six_projected_return_hessian_blocks_validated",
    "signed_second_variation_pilot_promoted_to_proof",
    "conditional_graph_arithmetic_promoted_to_stable_graph",
    "quantitative_inner_stable_graph_validated",
    "selected_pulse_stable_sheet_crossing_validated",
    "exact_phase_zero_section_identified_with_old_binary64_pulse_level",
    "unique_physical_pulse_onset_validated",
    "two_sided_basin_routing_validated",
    "biological_capture_or_control_validated",
    "asynchronous_network_safety_validated",
    "general_network_canard_theory_validated",
    "full_X_and_reduced_Y_phase_spaces_identified_without_bridge",
    "lambda_star_chosen_before_initial_and_terminal_domain_restrictions",
    "ambient_hit_promoted_before_section_domain_containment",
)


@dataclass(frozen=True)
class Stage4SEventTubeCertificate:
    schema_id: str
    status: str
    model_id: str
    branch: str
    parent_result_sha256: dict[str, str]
    exact_inputs: dict[str, Any]
    reduced_history_bridge: dict[str, Any]
    physical_normalization: dict[str, Any]
    exact_center_event_window: dict[str, Any]
    qualitative_scaled_full_ball_theorem: dict[str, Any]
    return_domain_containment: dict[str, Any]
    domain_quantifier_order: dict[str, Any]
    proof_mechanism: dict[str, Any]
    stage_boundary_audit: dict[str, Any]
    proved_conditional_diagnostic_open: dict[str, Any]
    open_numeric_ingress: dict[str, Any]
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


def _decimal(value: Any, name: str) -> Decimal:
    if not isinstance(value, str):
        raise ValueError(f"{name} is not a decimal string")
    try:
        return Decimal(value)
    except Exception as exc:  # pragma: no cover - defensive schema guard
        raise ValueError(f"{name} is not a finite decimal") from exc


def _decimal_string(value: Decimal) -> str:
    return format(value, "f")


def _runtime_record() -> dict[str, str]:
    return {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "arithmetic": (
            "decimal.Decimal at precision 120 on directed decimal parent "
            "endpoints plus a qualitative compactness/openness proof"
        ),
    }


def _load_and_validate_parents(
    repository: Path,
) -> tuple[dict[str, Mapping[str, Any]], dict[str, Any]]:
    objects: dict[str, Mapping[str, Any]] = {}
    source_ledgers: dict[str, Any] = {}
    for relative, expected_digest in PARENT_RESULT_SHA256.items():
        path = repository / relative
        if _sha256_path(path) != expected_digest:
            raise ValueError(f"Stage-4S parent bytes changed: {relative}")
        payload = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(payload, Mapping):
            raise ValueError(f"Stage-4S parent is not a mapping: {relative}")
        if path.name == "leaky_reduced_history.json":
            validate_leaky_reduced_history_result(payload, repository)
        manifest = _mapping(payload.get("manifest"), f"{relative} manifest")
        if manifest.get("result") != relative:
            raise ValueError(f"Stage-4S parent result path changed: {relative}")
        object_key = PARENT_OBJECT_KEYS[path.name]
        objects[path.name] = _mapping(
            payload.get(object_key), f"{relative} {object_key}"
        )

        declared: dict[str, dict[str, str]] = {}
        for ledger_name in ("source_sha256", "dependency_source_sha256"):
            raw = manifest.get(ledger_name, {})
            ledger = _mapping(raw, f"{relative} {ledger_name}")
            normalized: dict[str, str] = {}
            for source_relative, source_digest in ledger.items():
                if not isinstance(source_relative, str) or not isinstance(
                    source_digest, str
                ):
                    raise ValueError(f"{relative} has malformed source ledger")
                if _sha256_path(repository / source_relative) != source_digest:
                    raise ValueError(
                        f"Stage-4S parent source bytes changed: {source_relative}"
                    )
                normalized[source_relative] = source_digest
            declared[ledger_name] = normalized
        source_ledgers[relative] = declared
    return objects, source_ledgers


def _require_claim(
    obj: Mapping[str, Any], name: str, expected: bool, parent: str
) -> None:
    claims = _mapping(obj.get("claim_status"), f"{parent} claim ledger")
    if claims.get(name) is not expected:
        raise ValueError(f"{parent} claim boundary changed: {name}")


def _audit_parent_semantics(parents: Mapping[str, Mapping[str, Any]]) -> None:
    branch = parents["autonomous_leaky_recovery_inner_branch_artifact.json"]
    _require_claim(branch, "periodic_rfde_orbit_validated", True, "orbit")
    if branch.get("branch") != "inner_saddle_candidate":
        raise ValueError("the exact periodic-center branch changed")

    stage4l = parents["leaky_inner_terminal_stable_row_stage4l.json"]
    if stage4l.get("branch") != "inner_saddle_candidate":
        raise ValueError("Stage-4L no longer addresses the inner center")
    period = _mapping(
        stage4l.get("true_period_and_word_support"), "Stage-4L period ledger"
    )
    if period.get("complete_true_returned_history_covered") is not True:
        raise ValueError("Stage-4L complete returned history was weakened")
    if period.get("tau1_exact") != "5*sqrt(5)":
        raise ValueError("Stage-4L physical maximum delay changed")

    stage2 = parents["leaky_inner_stable_manifold_stage2_contract.json"]
    if stage2.get("branch") != "inner_saddle_candidate":
        raise ValueError("Stage-2 no longer addresses the inner center")
    _require_claim(
        stage2,
        "exact_phase_zero_voltage_section_uniform_speed_on_declared_ball_validated",
        True,
        "Stage-2",
    )
    section = _mapping(
        stage2.get("explicit_voltage_section_audit"), "Stage-2 voltage section"
    )
    if section.get("exact_phase_zero_section_formula") != (
        "h_C(phi)=phi_v(0)-V_true(0)"
    ):
        raise ValueError("Stage-2 exact voltage section changed")
    if section.get("uniform_event_speed_on_declared_section_ball_validated") is not True:
        raise ValueError("Stage-2 section-ball speed was weakened")

    reduced = parents["leaky_reduced_history.json"]
    expected_reduced_scalars = {
        "maximum_delay": "5*sqrt(5)",
        "full_history_space": "X=C([-r,0],R^2)",
        "reduced_history_space": "Y=C([-r,0],R)xR",
        "projection_formula": "pi(phi_v,phi_w)=(phi_v,phi_w(0))",
        "reduced_semiflow_formula": "pi*Phi_t=Psi_t*pi for every t>=0",
        "future_factorization_formula": (
            "Phi_t=iota*Psi_t*pi for every t>=r"
        ),
    }
    for name, expected in expected_reduced_scalars.items():
        if reduced.get(name) != expected:
            raise ValueError(f"the exact reduced-history bridge changed: {name}")
    if reduced.get("exact_symbolic_zero_defect_count") != 4:
        raise ValueError("the recovery-history lift identities changed")
    for name in (
        "projection_has_continuous_split_right_inverse_proved",
        "future_depends_only_on_voltage_history_and_current_recovery_proved",
        "old_recovery_history_flushed_after_one_maximum_delay_proved",
        "full_semiflow_factors_through_reduced_semiflow_proved",
        "compatible_history_range_invariant_after_one_delay_proved",
    ):
        if reduced.get(name) is not True:
            raise ValueError(f"a reduced-history theorem was weakened: {name}")
    for name in (
        "inner_stable_manifold_validated",
        "physical_pulse_stable_manifold_crossing_validated",
        "two_sided_physical_onset_validated",
    ):
        if reduced.get(name) is not False:
            raise ValueError(f"a reduced-history boundary was promoted: {name}")

    stage3 = parents["leaky_inner_stable_projection_stage3.json"]
    if stage3.get("section") != (
        "Sigma={phi_v(0)=0} at the exact Route-C phase-zero crossing"
    ):
        raise ValueError("Stage-3 Route-C section changed")

    stage4m = parents[
        "leaky_inner_enlarged_return_hessian_stage4m_contract.json"
    ]
    coordinate_registration = _mapping(
        stage4m.get("coordinate_registration"),
        "Stage-4M coordinate registration",
    )
    if coordinate_registration.get("stable_space") != (
        "E_s=ker(f_hat) in Sigma_0"
    ):
        raise ValueError("Stage-4M stable section space changed")
    if coordinate_registration.get("normalization") != (
        "||q_hat||_Y=1 and f_hat(q_hat)=1 exactly"
    ):
        raise ValueError("Stage-4M coordinate normalization changed")
    _require_claim(
        stage4m,
        "continuous_history_unit_y_normalization_adapter_validated",
        False,
        "Stage-4M",
    )

    stage4n = parents[
        "leaky_inner_nonlinear_selected_return_tube_stage4n_contract.json"
    ]
    coordinates = _mapping(
        stage4n.get("coordinate_and_domain_registration"),
        "Stage-4N coordinates",
    )
    if coordinates.get("full_ball_quantifier") != (
        "all ||x_s||_Y<=0.0097 and |x_u|<=0.00025, including arbitrary "
        "continuous stable histories"
    ):
        raise ValueError("Stage-4N preferred full-ball quantifier changed")
    ingress = _mapping(
        stage4n.get("required_numeric_ingress"), "Stage-4N ingress"
    )
    for name in (
        "T_minus",
        "T_plus",
        "left_endpoint_gap_margin_delta_minus",
        "right_endpoint_gap_margin_delta_plus",
        "uniform_event_speed_lower_a_star",
        "nonlinear_flow_family_Y_tube_remainder_upper",
        "returned_history_tube_radius_R_return",
        "local_section_patch_radius",
    ):
        if ingress.get(name) is not None:
            raise ValueError(f"preferred Stage-4N ingress was promoted: {name}")

    feasibility = parents[
        "leaky_inner_nonlinear_selected_return_tube_stage4n_feasibility.json"
    ]
    _require_claim(
        feasibility,
        "generic_row_sum_gronwall_tube_test_fails",
        True,
        "Stage-4N feasibility",
    )
    _require_claim(
        feasibility,
        "full_ball_nonlinear_mild_flow_remainder_validated",
        False,
        "Stage-4N feasibility",
    )
    _require_claim(
        feasibility,
        "centered_voltage_hessian_semantics_validated",
        True,
        "Stage-4N feasibility",
    )
    stage4i_gronwall = _mapping(
        feasibility.get("stage4i_sharpened_generic_gronwall"),
        "Stage-4N corrected Stage-4I Gronwall row",
    )
    if stage4i_gronwall.get("exact_inner_voltage_bound_coordinate") != (
        "centered z=v-1"
    ):
        raise ValueError("the corrected centered-voltage coordinate changed")
    if stage4i_gronwall.get("field_hessian_row_formula") != (
        "2*(1+B+r)+12*epsilon*kappa3*(B+r), with B=sup|v_*-1|"
    ):
        raise ValueError("the corrected Stage-4N Hessian row changed")
    if stage4i_gronwall.get("closure_passes") is not False:
        raise ValueError("the corrected Stage-4N no-go boundary changed")

    stage4o = parents[
        "leaky_inner_event_aligned_return_hessian_stage4o_contract.json"
    ]
    _require_claim(
        stage4o,
        "near_two_period_smoothing_route_registered",
        True,
        "Stage-4O",
    )
    _require_claim(
        stage4o,
        "common_selected_event_window_validated",
        False,
        "Stage-4O",
    )
    _require_claim(
        stage4o,
        "all_six_projected_return_hessian_blocks_validated",
        False,
        "Stage-4O",
    )

    stage4p = parents["leaky_inner_graph_closure_arithmetic_stage4p.json"]
    _require_claim(
        stage4p,
        "one_return_joint_reference_row_closes_arithmetically",
        True,
        "Stage-4P",
    )
    _require_claim(
        stage4p,
        "quantitative_inner_stable_graph_validated",
        False,
        "Stage-4P",
    )
    _require_claim(
        stage4p,
        "two_return_full_ball_smoothing_window_validated",
        False,
        "Stage-4P",
    )

    stage4q = parents[
        "leaky_inner_signed_second_variation_stage4q_pilot.json"
    ]
    if stage4q.get("status") != "DIAGNOSTIC_NONRIGOROUS_SOURCE_BOUND":
        raise ValueError("Stage-4Q diagnostic status changed")
    claims4q = _mapping(stage4q.get("claim_status"), "Stage-4Q claims")
    if any(value is not False for value in claims4q.values()):
        raise ValueError("a Stage-4Q diagnostic claim was promoted")

    stage4r = parents[
        "finite_delay_eventually_smooth_selected_return_stage4r.json"
    ]
    _require_claim(
        stage4r,
        "strict_T_minus_greater_than_2_tau_star_is_C2_sufficient",
        True,
        "Stage-4R",
    )
    _require_claim(
        stage4r,
        "selected_event_time_and_complete_history_hit_Ck_proved",
        True,
        "Stage-4R",
    )
    _require_claim(
        stage4r,
        "ambient_event_hit_distinguished_from_induced_section_return",
        True,
        "Stage-4R",
    )
    _require_claim(
        stage4r,
        "any_concrete_event_window_validated",
        False,
        "Stage-4R",
    )


def _numeric_data(
    parents: Mapping[str, Mapping[str, Any]],
) -> dict[str, str]:
    period = _mapping(
        parents["leaky_inner_terminal_stable_row_stage4l.json"].get(
            "true_period_and_word_support"
        ),
        "Stage-4L period ledger",
    )
    section = _mapping(
        parents["leaky_inner_stable_manifold_stage2_contract.json"].get(
            "explicit_voltage_section_audit"
        ),
        "Stage-2 voltage section",
    )
    with localcontext() as context:
        context.prec = 120
        period_lower = _decimal(period.get("true_period_lower"), "P lower")
        period_upper = _decimal(period.get("true_period_upper"), "P upper")
        tau_upper = _decimal(period.get("tau1_upper"), "tau max upper")
        orbit_speed = _decimal(
            section.get("physical_orbit_history_speed_upper"),
            "orbit history speed",
        )
        event_speed = _decimal(
            section.get("uniform_event_speed_lower_on_declared_section_ball"),
            "event speed",
        )
        section_radius = _decimal(
            section.get("declared_section_ball_radius"), "section radius"
        )
        half_width = Decimal("0.001")
        period_width = period_upper - period_lower
        time_offset = half_width + Decimal(2) * period_width
        displacement = orbit_speed * time_offset
        center_gap = event_speed * half_width
        data = {
            "period_lower": _decimal_string(period_lower),
            "period_upper": _decimal_string(period_upper),
            "period_width_upper": _decimal_string(period_width),
            "tau_max_upper": _decimal_string(tau_upper),
            "fixed_extra_half_width_h": _decimal_string(half_width),
            "T_minus": _decimal_string(
                Decimal(2) * period_lower - half_width
            ),
            "T_plus": _decimal_string(
                Decimal(2) * period_upper + half_width
            ),
            "maximum_center_phase_offset_upper": _decimal_string(time_offset),
            "physical_orbit_history_speed_upper": _decimal_string(orbit_speed),
            "center_window_history_displacement_upper": _decimal_string(
                displacement
            ),
            "declared_section_ball_radius": _decimal_string(section_radius),
            "center_window_section_ball_margin_lower": _decimal_string(
                section_radius - displacement
            ),
            "center_uniform_event_speed_lower": _decimal_string(event_speed),
            "center_left_endpoint_gap_lower": _decimal_string(center_gap),
            "center_right_endpoint_gap_lower": _decimal_string(center_gap),
            "scaled_ball_uniform_event_speed_lower": _decimal_string(
                event_speed / Decimal(2)
            ),
            "scaled_ball_left_endpoint_gap_lower": _decimal_string(
                center_gap / Decimal(2)
            ),
            "scaled_ball_right_endpoint_gap_lower": _decimal_string(
                center_gap / Decimal(2)
            ),
            "T_minus_minus_2_tau_max_lower": _decimal_string(
                Decimal(2) * period_lower
                - half_width
                - Decimal(2) * tau_upper
            ),
        }
    if not (
        period_lower < period_upper
        and displacement < section_radius
        and center_gap > 0
        and Decimal(data["T_minus_minus_2_tau_max_lower"]) > 0
    ):
        raise ValueError("Stage-4S center inequalities do not close")
    return data


def _numeric_core(certificate: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "exact_inputs": certificate["exact_inputs"],
        "reduced_history_bridge": certificate["reduced_history_bridge"],
        "physical_normalization": certificate["physical_normalization"],
        "exact_center_event_window": certificate["exact_center_event_window"],
        "qualitative_scaled_full_ball_theorem": certificate[
            "qualitative_scaled_full_ball_theorem"
        ],
        "return_domain_containment": certificate[
            "return_domain_containment"
        ],
        "domain_quantifier_order": certificate["domain_quantifier_order"],
        "open_numeric_ingress": certificate["open_numeric_ingress"],
        "claim_status": certificate["claim_status"],
    }


def build_stage4s_event_tube_certificate(
    repository: Path,
) -> Stage4SEventTubeCertificate:
    repository = repository.resolve()
    parents, _ = _load_and_validate_parents(repository)
    _audit_parent_semantics(parents)
    numeric = _numeric_data(parents)
    claims = {name: True for name in TRUE_FLAGS}
    claims.update({name: False for name in FALSE_FLAGS})

    return Stage4SEventTubeCertificate(
        schema_id=SCHEMA_ID,
        status=STATUS,
        model_id=MODEL_ID,
        branch=BRANCH,
        parent_result_sha256=dict(PARENT_RESULT_SHA256),
        exact_inputs={
            "validated_periodic_center": (
                "the exact phase-fixed full RFDE orbit X_*^X and its reduced "
                "projection Y_*=pi(X_*^X)"
            ),
            "equation_class": (
                "a finite-dimensional autonomous RFDE with the two fixed "
                "physical delays 4*sqrt(5) and 5*sqrt(5)"
            ),
            "regularity": (
                "the full-X leaky FHN history functional is polynomial in "
                "current and delayed evaluations, hence C-infinity"
            ),
            "full_history_space": "X=C([-tau_max,0],R^2)",
            "reduced_history_space": (
                "Y=C([-tau_max,0],R)_v x R_w with "
                "||(phi,w)||_Y=max(||phi||_infinity,|w|)"
            ),
            "maximum_delay": "tau_max=5*sqrt(5) in physical time",
            "reduced_event_functional": (
                "g_Y(y)=y_v(0)-Y_{*,v}(0)"
            ),
            "full_event_functional": "g_X=g_Y o pi on X",
            "event_domain_and_regularity": (
                "g_Y:Y->R and g_X:X->R are affine C-infinity"
            ),
            "exact_affine_section_in_Y": (
                "Sigma=Y_*+Sigma_0, Sigma_0={h in Y:h_v(0)=0}"
            ),
            "initial_coordinate_injection": (
                "j(x_s,x_u)=Y_*+x_s+q_hat*x_u, with x_s in "
                "ker(f_hat), ||q_hat||_Y=1, and the fixed Stage-3/4N "
                "Route-C splitting"
            ),
            "preferred_unscaled_radii": {
                "R_s": "0.0097",
                "R_u_hat": "0.00025",
                "sum": "0.00995",
            },
            "scaled_closed_ball": (
                "B_lambda={||x_s||_Y<=lambda*0.0097, "
                "|x_u|<=lambda*0.00025}"
            ),
            "stable_history_quantifier": (
                "every continuous x_s in ker(f_hat) satisfying the norm "
                "bound; no finite-node replacement"
            ),
        },
        reduced_history_bridge={
            "status": "PROVED_EXACT_REDUCED_HISTORY_FACTORISATION",
            "full_space": "X=C([-r,0],R^2)",
            "reduced_space": "Y=C([-r,0],R)xR",
            "projection": "pi(phi_v,phi_w)=(phi_v,phi_w(0))",
            "compatible_lift": (
                "Iota(q,omega)=(q,R(q,omega)), where "
                "R(q,omega)(theta)=exp(-epsilon*theta)*[omega-epsilon*"
                "integral_theta^0 exp(epsilon*s)*(q(s)-a) ds]"
            ),
            "lift_regularity": (
                "Iota is affine C-infinity, DIota is the proved continuous "
                "linear split right inverse of pi, and pi o Iota=Id_Y"
            ),
            "reduced_semiflow": "Psi_t=pi o Phi_t o Iota for every t>=0",
            "intertwining": "pi o Phi_t=Psi_t o pi for every t>=0",
            "compatible_range_after_memory": (
                "Phi_t=Iota o Psi_t o pi for every t>=r"
            ),
            "periodic_center_compatibility": (
                "the full periodic center satisfies X_*^X=Iota(Y_*) because "
                "its recovery history solves the recovery ODE on every "
                "length-r orbit segment"
            ),
            "Stage4R_full_space_input": (
                "Stage-4R is applied only to Phi on X, with initial "
                "parameterization Iota:W subset Y->X and full event "
                "g_X=g_Y o pi; the section injection j is imposed later"
            ),
            "reduced_C2_corollary": (
                "on t>2r, (t,y)->Psi_t(y)=pi(Phi_t(Iota(y))) is jointly C2 "
                "because pi is bounded linear, Iota is affine C-infinity, "
                "and the Stage-4R full-X segment map is jointly C2"
            ),
            "event_intertwining": (
                "g_X(Phi_t(Iota(y)))=g_Y(Psi_t(y)); endpoint signs, speed, "
                "and the selected time are identical in X and Y"
            ),
            "reduced_hit": (
                "R_Y(y)=Psi_{T(y)}(y)=pi(Phi_{T(y)}(Iota(y))) is C2"
            ),
            "compatible_full_hit": (
                "because T_->2r>r, Phi_{T(y)}(Iota(y))=Iota(R_Y(y))"
            ),
            "full_X_identified_with_Y_without_bridge": False,
        },
        physical_normalization={
            "time": "all T, P, h, and delays are physical times",
            "state": "physical voltage history and physical recovery current",
            "norm": "the inherited max history norm Y, not a period-normalized norm",
            "period_lower": numeric["period_lower"],
            "period_upper": numeric["period_upper"],
            "tau_max_upper": numeric["tau_max_upper"],
            "period_rescaling_used": False,
            "finite_history_grid_used": False,
        },
        exact_center_event_window={
            **numeric,
            "declared_ball_semantics": (
                "the ambient Y-norm ball centered at the exact section point "
                "Y_*; intermediate orbit histories need not satisfy g_Y=0"
            ),
            "window_definition": (
                "I=[2*P_lower-h,2*P_upper+h] with h=0.001"
            ),
            "center_selected_time": "T(Y_*)=2P exactly",
            "center_left_sign": (
                "g_Y(Psi_{T_minus}(Y_*)) <= "
                f"-{numeric['center_left_endpoint_gap_lower']}"
            ),
            "center_right_sign": (
                "g_Y(Psi_{T_plus}(Y_*)) >= "
                f"{numeric['center_right_endpoint_gap_lower']}"
            ),
            "center_speed_statement": (
                "partial_t g_Y(Psi_t(Y_*)) is at least the registered center "
                "uniform speed for every t in I; this equals the lifted "
                "full-X event speed"
            ),
            "center_uniqueness": (
                "strict positive speed makes 2P the unique zero in I"
            ),
            "center_returned_history": (
                "Psi_{2P}(Y_*)=Y_* and Phi_{2P}(Iota(Y_*))=Iota(Y_*) exactly"
            ),
        },
        qualitative_scaled_full_ball_theorem={
            "lambda_symbol": "lambda_*",
            "quantifier": "there exists lambda_* in (0,1]",
            "numerical_lower_bound": None,
            "preferred_lambda_one_claimed": False,
            "event_open_neighborhood_W": (
                "there is an open W subset Y containing Y_* on which the "
                "common-window full-lift solution domain, two endpoint signs, "
                "and uniform positive speed all hold"
            ),
            "ambient_strengthening": (
                "the event theorem first holds on W in the ambient reduced "
                "space Y; the local-section coordinate ball is imposed later"
            ),
            "common_solution_domain": (
                "(t,Iota(y)) belongs to the full-X maximal RFDE semiflow "
                "domain for every (t,y) in I x W"
            ),
            "common_window": (
                f"[{numeric['T_minus']},{numeric['T_plus']}] in physical time"
            ),
            "left_endpoint_bound": (
                "sup_{y in W} g_Y(Psi_{T_minus}(y)) <= -"
                f"{numeric['scaled_ball_left_endpoint_gap_lower']}"
            ),
            "right_endpoint_bound": (
                "inf_{y in W} g_Y(Psi_{T_plus}(y)) >= "
                f"{numeric['scaled_ball_right_endpoint_gap_lower']}"
            ),
            "speed_bound": (
                "inf_{(t,y) in I x W} partial_t "
                "g_Y(Psi_t(y)) >= "
                f"{numeric['scaled_ball_uniform_event_speed_lower']}"
            ),
            "selected_event_output": (
                "for every y in W there is exactly one T(y) in the fixed I "
                "with g_Y(Psi_{T(y)}(y))=0 and positive orientation"
            ),
            "regularity_output": (
                "T:W->R and R_Y(y)=Psi_{T(y)}(y):W->Y are C2 by the "
                "proved full-X/reduced-Y bridge"
            ),
            "final_coordinate_domain": (
                "after imposing both initial and terminal section-patch gates, "
                "D is an open neighborhood of 0 in E_s x R"
            ),
            "full_ball_scope": (
                "lambda_* is chosen last so B_{lambda_*} subset D; the "
                "conclusion then holds simultaneously for every member, "
                "including arbitrary continuous stable histories"
            ),
            "ordinal_output": None,
        },
        return_domain_containment={
            "terminal_patch": (
                "Sigma_loc={y in Y:g_Y(y)=0 and "
                f"||y-Y_*||_Y<{numeric['declared_section_ball_radius']}}}"
            ),
            "initial_section_domain": (
                "D_in=j^{-1}(W intersect Sigma_loc), open in E_s x R and "
                "containing 0"
            ),
            "reduced_coordinate_hit": "R_j=R_Y o j on D_in",
            "final_domain": (
                "D=D_in intersect R_j^{-1}(Sigma_loc), open in E_s x R "
                "and containing 0"
            ),
            "initial_containment": "j(D) subset W intersect Sigma_loc",
            "terminal_containment": "R_j(D) subset Sigma_loc",
            "why_event_hyperplane": (
                "g_Y(R_Y(y))=0 by the selected-event equation"
            ),
            "why_local_patch": (
                "R_Y(Y_*)=Y_* and continuity of R_Y make "
                "R_j^{-1}(Sigma_loc) open relative to its event section domain"
            ),
            "terminal_chart_codomain": (
                "D_out=chi(Sigma_loc), an open subset of E_s x R"
            ),
            "terminal_chart": (
                "chi(y)=(P_s(y-Y_*),f_hat(y-Y_*)):Sigma_loc->D_out is "
                "affine C-infinity and has inverse j restricted to D_out"
            ),
            "induced_return": (
                "P_sel=chi o R_j:D->D_out is an induced C2 selected section "
                "return; no assertion P_sel(D) subset D is made"
            ),
            "same_scaled_ball_self_map": False,
        },
        domain_quantifier_order={
            "order": [
                "1 obtain open event neighborhood W in ambient reduced Y",
                "2 construct C2 T:W->R and R_Y:W->Y through the full-X bridge",
                "3 impose initial section-chart domain D_in=j^{-1}(W intersect Sigma_loc)",
                "4 impose terminal domain D=D_in intersect (R_Y o j)^{-1}(Sigma_loc)",
                "5 define chi:Sigma_loc->D_out=chi(Sigma_loc) and P_sel:D->D_out",
                "6 choose lambda_* in (0,1] so B_{lambda_*} subset D",
            ],
            "W_chosen_before_D": True,
            "D_in_chosen_before_lambda_star": True,
            "terminal_preimage_imposed_before_lambda_star": True,
            "lambda_star_chosen_last": True,
            "initial_injection_gate": "j(D) subset Sigma_loc",
            "terminal_hit_gate": "R_Y(j(D)) subset Sigma_loc",
            "ball_gate": "B_{lambda_*} subset D",
            "codomain_gate": "D_out=chi(Sigma_loc)",
        },
        proof_mechanism={
            "step_1_full_X_to_reduced_Y_bridge": (
                "apply Stage-4R to Phi on X with Iota:W->X, then compose with "
                "the exact affine lift Iota and bounded projection pi to obtain "
                "joint C2 smoothing in Y"
            ),
            "step_2_center_geometry": (
                "the true P interval puts 2P strictly inside the fixed I"
            ),
            "step_3_center_tube": (
                "the global physical orbit-history speed times the largest "
                "phase offset is smaller than the declared section-ball radius"
            ),
            "step_4_center_sign_and_speed": (
                "the Stage-2 uniform physical voltage speed integrates over "
                "at least h at both endpoints, giving the two strict signs"
            ),
            "step_5_event_neighborhood_W": (
                "joint continuous dependence and openness of the maximal "
                "semiflow domain, uniformly over compact I, preserve half of "
                "the center endpoint and speed margins on one ambient Y-"
                "neighborhood W of Y_*"
            ),
            "step_6_initial_and_terminal_domains": (
                "apply the Stage-4R selected-event theorem on W to construct "
                "C2 maps T and R_Y, intersect j^{-1}(W) first with the initial "
                "Sigma_loc chart domain and then with the inverse image of "
                "Sigma_loc under R_Y o j; the resulting D is open and contains 0"
            ),
            "step_7_choose_lambda_last": (
                "only after D is fixed, use ||x_s+q_hat*x_u||_Y<="
                "lambda*(0.0097+0.00025) to choose lambda_*>0 with the "
                "complete arbitrary-continuous-history B_{lambda_*} subset D"
            ),
            "compactness_only_no_effective_modulus": True,
        },
        stage_boundary_audit={
            "Reduced_history_bridge": (
                "the exact pi/Iota semiflow factorization is validated and "
                "used to derive the Y-valued C2 hit; X and Y are never "
                "identified as the same Banach phase space"
            ),
            "Stage_4N": (
                "the preferred lambda=1 nonlinear tube remains OPEN; Stage-4S "
                "proves only an existentially scaled full ball"
            ),
            "Stage_4N_feasibility": (
                "the corrected source-bound no-go uses B=sup|v_*-1| and "
                "H_r=2*(1+B+r)+12*epsilon*kappa3*(B+r); its stronger generic "
                "Gronwall failure is preserved and is not a true-flow lower bound"
            ),
            "Stage_4M": (
                "the fixed unit-Y splitting is used only as a qualitative "
                "coordinate interface; its continuous-history numerical "
                "normalization adapter is not promoted"
            ),
            "Stage_4O": (
                "its exact event/Hessian formulas remain an analytic contract; "
                "Stage-4S uses the Stage-4R regularity theorem and validates no Hessian block"
            ),
            "Stage_4P": (
                "its reference graph inequalities are CONDITIONAL arithmetic; "
                "Stage-4S supplies neither the preferred graph box nor six block bounds"
            ),
            "Stage_4Q": (
                "all finite-grid second-variation rows remain DIAGNOSTIC and are "
                "excluded from the proof"
            ),
            "Stage_4R": (
                "the general PROVED theorem is applied on full X; the exact "
                "reduced-history bridge gives the Y corollary, after which "
                "initial and terminal section domains are imposed"
            ),
            "selected_vs_ordinal": (
                "unique in this fixed near-2P window is not first return, not "
                "the second positive crossing, and not Q=P^2"
            ),
            "selected_vs_biological": (
                "the exact phase-zero voltage event is not the old binary64 "
                "pulse separator and proves no pulse onset or biological control"
            ),
        },
        proved_conditional_diagnostic_open={
            "PROVED_numeric": (
                "exact-center physical window, endpoint margins, positive speed, "
                "smoothing margin, and exact returned history"
            ),
            "PROVED_qualitative": (
                "the exact full-X/reduced-Y C2 bridge and existence of one "
                "nonzero scaled arbitrary-continuous-history ball contained "
                "in the final initial-and-terminal section domain"
            ),
            "CONDITIONAL": (
                "Stage-4P graph arithmetic and all uses requiring certified "
                "Hessian blocks or a preferred-size return domain"
            ),
            "DIAGNOSTIC": "every Stage-4Q finite-grid row",
            "OPEN": (
                "a numerical lambda lower bound, lambda=1, quantitative flow/"
                "return derivative bounds, ordinal return, stable graph, pulse "
                "crossing/onset, routing, capture, safety, and general-network transfer"
            ),
        },
        open_numeric_ingress={
            "lambda_star_lower": None,
            "preferred_ball_lambda_one": False,
            "preferred_ball_nonlinear_mild_flow_remainder_upper": None,
            "scaled_ball_explicit_solution_tube_radius": None,
            "selected_return_D1_norm_upper": None,
            "selected_return_D2_norm_upper": None,
            "six_projected_Hessian_blocks": None,
            "same_scaled_ball_return_radius": None,
            "first_or_second_event_ordinal": None,
            "pulse_sheet_gap": None,
            "biological_onset_or_safety_radius": None,
            "evidence_status": (
                "QUALITATIVE_LOCAL_EXISTENCE_ONLY_BEYOND_EXACT_CENTER_ARITHMETIC"
            ),
        },
        theorem_boundary={
            "minimum_closed_subtheorem": (
                "there exists a nonzero scaling of the preferred anisotropic "
                "coordinate ball on which a common physical near-two-period "
                "reduced-Y C2 selected section return is defined through the "
                "exact full-X lift/projection bridge, with both its initial "
                "and terminal histories in one fixed exact phase-zero patch"
            ),
            "full_X_reduced_Y_bridge_required": True,
            "lambda_selected_only_after_final_domain": True,
            "not_a_preferred_ball_certificate": True,
            "not_a_self_map_or_stable_graph_certificate": True,
            "not_an_ordinal_or_P2_identity_certificate": True,
            "not_a_pulse_or_biological_control_certificate": True,
            "flagship_README_or_other_agent_files_modified": False,
        },
        claim_status=claims,
    )


def build_stage4s_event_tube_result(repository: Path) -> dict[str, Any]:
    repository = repository.resolve()
    certificate = asdict(build_stage4s_event_tube_certificate(repository))
    _, parent_source_ledgers = _load_and_validate_parents(repository)
    return {
        "certificate": certificate,
        "manifest": {
            "schema_id": SCHEMA_ID,
            "result": RESULT_RELATIVE_PATH,
            "default_command": DEFAULT_COMMAND,
            "arithmetic_scope": ARITHMETIC_SCOPE,
            "certificate_sha256": canonical_sha256(certificate),
            "numeric_core_sha256": canonical_sha256(_numeric_core(certificate)),
            "source_sha256": {
                relative: _sha256_path(repository / relative)
                for relative in SOURCE_MANIFEST
            },
            "parent_result_sha256": dict(PARENT_RESULT_SHA256),
            "parent_source_manifest_sha256": canonical_sha256(
                parent_source_ledgers
            ),
            "runtime": _runtime_record(),
        },
    }


def validate_stage4s_event_tube_result(
    payload: Mapping[str, Any],
    repository: Path,
    *,
    recompute: bool = False,
) -> None:
    if not isinstance(payload, Mapping) or set(payload) != TOP_KEYS:
        raise ValueError("the Stage-4S event-tube result has the wrong schema")
    certificate = _mapping(payload.get("certificate"), "Stage-4S certificate")
    manifest = _mapping(payload.get("manifest"), "Stage-4S manifest")
    if set(certificate) != {
        field.name for field in fields(Stage4SEventTubeCertificate)
    }:
        raise ValueError("the Stage-4S certificate schema changed")
    if set(manifest) != MANIFEST_KEYS:
        raise ValueError("the Stage-4S manifest schema changed")

    repository = repository.resolve()
    expected_certificate = asdict(
        build_stage4s_event_tube_certificate(repository)
    )
    if dict(certificate) != expected_certificate:
        raise ValueError("the Stage-4S theorem statement or boundary changed")

    claims = _mapping(certificate.get("claim_status"), "Stage-4S claims")
    if set(claims) != set(TRUE_FLAGS) | set(FALSE_FLAGS):
        raise ValueError("the Stage-4S claim ledger changed")
    if any(claims.get(name) is not True for name in TRUE_FLAGS):
        raise ValueError("a proved Stage-4S fact was weakened")
    if any(claims.get(name) is not False for name in FALSE_FLAGS):
        raise ValueError("an excluded Stage-4S claim was promoted")

    bridge = _mapping(
        certificate.get("reduced_history_bridge"),
        "Stage-4S reduced-history bridge",
    )
    if bridge.get("full_X_identified_with_Y_without_bridge") is not False:
        raise ValueError("full X and reduced Y were conflated")
    if "Psi_t(y)=pi(Phi_t(Iota(y)))" not in str(
        bridge.get("reduced_C2_corollary")
    ):
        raise ValueError("the reduced-Y C2 corollary was removed")

    order = _mapping(
        certificate.get("domain_quantifier_order"),
        "Stage-4S domain quantifier order",
    )
    for name in (
        "W_chosen_before_D",
        "D_in_chosen_before_lambda_star",
        "terminal_preimage_imposed_before_lambda_star",
        "lambda_star_chosen_last",
    ):
        if order.get(name) is not True:
            raise ValueError(f"the Stage-4S domain order changed: {name}")
    ordered_steps = order.get("order")
    if not isinstance(ordered_steps, list) or len(ordered_steps) != 6:
        raise ValueError("the Stage-4S ordered domain construction changed")
    if "choose lambda_*" not in ordered_steps[-1]:
        raise ValueError("lambda_* was not chosen after the final domain")

    containment = _mapping(
        certificate.get("return_domain_containment"),
        "Stage-4S return-domain containment",
    )
    if containment.get("initial_containment") != (
        "j(D) subset W intersect Sigma_loc"
    ):
        raise ValueError("the initial section containment changed")
    if containment.get("terminal_containment") != (
        "R_j(D) subset Sigma_loc"
    ):
        raise ValueError("the terminal section containment changed")
    if containment.get("terminal_chart_codomain") != (
        "D_out=chi(Sigma_loc), an open subset of E_s x R"
    ):
        raise ValueError("the terminal chart codomain changed")

    open_ingress = _mapping(
        certificate.get("open_numeric_ingress"), "Stage-4S open ingress"
    )
    for key, value in open_ingress.items():
        if key == "preferred_ball_lambda_one":
            if value is not False:
                raise ValueError("the preferred Stage-4N ball was promoted")
        elif key == "evidence_status":
            if value != (
                "QUALITATIVE_LOCAL_EXISTENCE_ONLY_BEYOND_EXACT_CENTER_ARITHMETIC"
            ):
                raise ValueError("the Stage-4S evidence tier changed")
        elif value is not None:
            raise ValueError(f"an open Stage-4S numeric ingress was filled: {key}")

    _, parent_source_ledgers = _load_and_validate_parents(repository)
    expected_manifest = {
        "schema_id": SCHEMA_ID,
        "result": RESULT_RELATIVE_PATH,
        "default_command": DEFAULT_COMMAND,
        "arithmetic_scope": ARITHMETIC_SCOPE,
        "certificate_sha256": canonical_sha256(certificate),
        "numeric_core_sha256": canonical_sha256(_numeric_core(certificate)),
        "source_sha256": {
            relative: _sha256_path(repository / relative)
            for relative in SOURCE_MANIFEST
        },
        "parent_result_sha256": dict(PARENT_RESULT_SHA256),
        "parent_source_manifest_sha256": canonical_sha256(
            parent_source_ledgers
        ),
        "runtime": _runtime_record(),
    }
    if dict(manifest) != expected_manifest:
        raise ValueError("the Stage-4S manifest or source binding changed")

    if recompute and dict(payload) != build_stage4s_event_tube_result(repository):
        raise ValueError("the Stage-4S fresh replay changed")


__all__ = [
    "ARITHMETIC_SCOPE",
    "BRANCH",
    "DEFAULT_COMMAND",
    "FALSE_FLAGS",
    "GENERATOR_RELATIVE_PATH",
    "MANIFEST_KEYS",
    "MODEL_ID",
    "NOTE_RELATIVE_PATH",
    "PARENT_RESULT_SHA256",
    "RESULT_RELATIVE_PATH",
    "SCHEMA_ID",
    "SOURCE_MANIFEST",
    "SOURCE_RELATIVE_PATH",
    "STATUS",
    "Stage4SEventTubeCertificate",
    "TEST_RELATIVE_PATH",
    "TOP_KEYS",
    "TRUE_FLAGS",
    "_numeric_core",
    "build_stage4s_event_tube_certificate",
    "build_stage4s_event_tube_result",
    "canonical_sha256",
    "validate_stage4s_event_tube_result",
]
