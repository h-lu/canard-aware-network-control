"""Stage-4N contract for a nonlinear selected-return tube and event graph.

Stage 4M freezes the first missing parent for enlarged-ball return-Hessian
bounds: a common nonlinear selected-return family on the full preferred-B
anisotropic complete-history ball.  This module specifies that parent without
inventing any numerical enclosure.

The contract requires one common event window, strict endpoint gap margins, a
uniform positive event-speed lower bound, a C2 event-time graph, a complete
returned-history tube, and a directed exclusion of every earlier admissible
positive-oriented return to the local Route-C section patch.  It distinguishes
the affine event hyperplane from the local return patch, so an earlier
negative-oriented crossing outside the patch is not confused with the
selected return.

No Stage-4L numerical result is a parent.  A terminal linear stable-row bound
cannot supply a nonlinear flow tube, an event graph, or no-earlier-return
separation.  Every numerical ingress and every return, Hessian, graph,
crossing, onset, routing, capture, and safety claim remains false.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from hashlib import sha256
import json
from pathlib import Path
import platform
from typing import Any, Mapping

from canard_control.leaky_inner_enlarged_return_hessian_stage4m_contract import (
    RESULT_RELATIVE_PATH as STAGE4M_RESULT_RELATIVE_PATH,
    SPLIT_RETURN_RADIUS,
    STABLE_GRAPH_RADIUS,
    UNIT_UNSTABLE_GRAPH_RADIUS,
    validate_stage4m_result,
)


SCHEMA_ID = "leaky-inner-nonlinear-selected-return-tube-stage4n-contract-v1"
MODEL_ID = "autonomous-leaky-recovery-two-delay-fhn-bistable-proposal"
BRANCH = "inner_saddle_candidate_selected_near_period_return"
STATUS = "OPEN_NUMERICAL_CONTRACT"

SOURCE_RELATIVE_PATH = (
    "src/canard_control/"
    "leaky_inner_nonlinear_selected_return_tube_stage4n_contract.py"
)
GENERATOR_RELATIVE_PATH = (
    "experiments/leaky_inner_nonlinear_selected_return_tube_stage4n_contract.py"
)
RESULT_RELATIVE_PATH = (
    "experiments/results/"
    "leaky_inner_nonlinear_selected_return_tube_stage4n_contract.json"
)
NOTE_RELATIVE_PATH = (
    "docs/leaky-inner-nonlinear-selected-return-tube-stage4n-contract.md"
)
TEST_RELATIVE_PATH = (
    "tests/test_leaky_inner_nonlinear_selected_return_tube_stage4n_contract.py"
)

STAGE4M_RESULT_SHA256 = (
    "1a7f89c4c61480a76149b88ae6a15fa40b11425f4d678615af3469b59f75100c"
)
PARENT_RESULT_SHA256 = {
    STAGE4M_RESULT_RELATIVE_PATH: STAGE4M_RESULT_SHA256,
}
SOURCE_MANIFEST = (
    SOURCE_RELATIVE_PATH,
    GENERATOR_RELATIVE_PATH,
    NOTE_RELATIVE_PATH,
    TEST_RELATIVE_PATH,
)
DEPENDENCY_SOURCE_MANIFEST = (
    "src/canard_control/leaky_inner_enlarged_return_hessian_stage4m_contract.py",
)

DEFAULT_COMMAND = (
    "PYTHONPATH=src /usr/bin/python3 "
    "experiments/leaky_inner_nonlinear_selected_return_tube_stage4n_contract.py"
)
ARITHMETIC_SCOPE = (
    "normal validation and byte binding of the nonclosing Stage-4M contract; "
    "exact registration of its preferred-B anisotropic radii; and an open "
    "continuous-history nonlinear flow, common-event-window, C2 event-graph, "
    "returned-history tube, and no-earlier-admissible-return interface; no "
    "Stage-4L numerical ingress and no return-map, Hessian, graph, crossing, "
    "onset, routing, capture, or safety promotion"
)

TOP_KEYS = {"contract", "manifest"}
MANIFEST_KEYS = {
    "schema_id",
    "result",
    "default_command",
    "arithmetic_scope",
    "contract_sha256",
    "numeric_core_sha256",
    "source_sha256",
    "dependency_source_sha256",
    "parent_result_sha256",
    "runtime",
}

TRUE_FLAGS = (
    "stage4m_parent_bytes_and_nonclosing_boundary_validated",
    "preferred_b_complete_history_ball_registered",
    "affine_event_hyperplane_and_local_return_patch_distinguished",
    "common_event_window_acceptance_interface_registered",
    "uniform_positive_event_speed_interface_registered",
    "complete_returned_history_tube_interface_registered",
    "c2_moving_event_graph_interface_registered",
    "no_earlier_admissible_positive_return_cover_registered",
    "continuous_time_and_history_coverage_required",
    "stage4l_numeric_result_excluded_from_parent_set",
)
FALSE_FLAGS = (
    "nonlinear_flow_family_on_full_anisotropic_ball_validated",
    "common_event_window_validated",
    "left_endpoint_gap_margin_validated",
    "right_endpoint_gap_margin_validated",
    "uniform_positive_event_speed_lower_bound_validated",
    "unique_selected_event_on_common_window_validated",
    "c2_event_time_graph_validated",
    "complete_returned_history_tube_validated",
    "returned_history_lies_in_local_section_patch_validated",
    "launch_collar_exclusion_validated",
    "no_earlier_admissible_positive_return_validated",
    "selected_return_map_on_full_anisotropic_ball_validated",
    "first_positive_local_return_validated",
    "stage4m_six_projected_return_hessian_blocks_validated",
    "quantitative_inner_stable_graph_validated",
    "selected_pulse_stable_sheet_crossing_validated",
    "unique_physical_pulse_onset_validated",
    "two_sided_basin_routing_validated",
    "outer_or_quiet_capture_from_both_sides_validated",
    "frequency_amplitude_safety_radius_validated",
    "asynchronous_network_safety_radius_validated",
)


@dataclass(frozen=True)
class Stage4NContract:
    schema_id: str
    model_id: str
    branch: str
    status: str
    parent_result_sha256: dict[str, str]
    coordinate_and_domain_registration: dict[str, Any]
    selected_return_definition: dict[str, Any]
    nonlinear_flow_family_contract: dict[str, Any]
    common_event_window_contract: dict[str, Any]
    c2_event_graph_contract: dict[str, Any]
    complete_returned_history_tube_contract: dict[str, Any]
    no_earlier_admissible_return_contract: dict[str, Any]
    directed_cover_interface: dict[str, Any]
    required_numeric_ingress: dict[str, Any]
    first_missing_error_term: dict[str, Any]
    handoff_to_stage4m: dict[str, Any]
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


def _load_stage4m(repository: Path) -> Mapping[str, Any]:
    path = repository / STAGE4M_RESULT_RELATIVE_PATH
    raw = path.read_bytes()
    if sha256(raw).hexdigest() != STAGE4M_RESULT_SHA256:
        raise ValueError("the bound Stage-4M result changed")
    payload = json.loads(raw)
    validate_stage4m_result(payload, repository)
    return _mapping(payload, "Stage-4M result")


def _numeric_core(contract: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "coordinate_and_domain_registration": contract[
            "coordinate_and_domain_registration"
        ],
        "common_event_window_contract": contract[
            "common_event_window_contract"
        ],
        "complete_returned_history_tube_contract": contract[
            "complete_returned_history_tube_contract"
        ],
        "no_earlier_admissible_return_contract": contract[
            "no_earlier_admissible_return_contract"
        ],
        "required_numeric_ingress": contract["required_numeric_ingress"],
        "first_missing_error_term": contract["first_missing_error_term"],
        "claim_status": contract["claim_status"],
    }


def _runtime_record() -> dict[str, str]:
    return {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "arithmetic": (
            "contract-only exact string registration and source/parent SHA-256 "
            "binding; no numerical flow enclosure"
        ),
    }


def build_stage4n_contract(repository: Path) -> Stage4NContract:
    repository = repository.resolve()
    stage4m = _load_stage4m(repository)
    stage4m_contract = _mapping(stage4m.get("contract"), "Stage-4M contract")
    domain = _mapping(
        stage4m_contract.get("anisotropic_domain"), "Stage-4M domain"
    )
    if (
        domain.get("stable_radius_R_s") != STABLE_GRAPH_RADIUS
        or domain.get("unit_unstable_radius_R_u_hat")
        != UNIT_UNSTABLE_GRAPH_RADIUS
        or domain.get("split_radius_sum_exact") != SPLIT_RETURN_RADIUS
        or domain.get("validated_return_domain") is not False
    ):
        raise ValueError("the Stage-4M preferred-B open domain changed")

    claims = {name: True for name in TRUE_FLAGS}
    claims.update({name: False for name in FALSE_FLAGS})
    return Stage4NContract(
        schema_id=SCHEMA_ID,
        model_id=MODEL_ID,
        branch=BRANCH,
        status=STATUS,
        parent_result_sha256=dict(PARENT_RESULT_SHA256),
        coordinate_and_domain_registration={
            "history_space": (
                "Y=C([-tau_max,0],R)_v x R_w with the inherited max norm"
            ),
            "affine_route_c_section": (
                "Sigma=X_*+Sigma_0, Sigma_0={h in Y:h_v(0)=0}"
            ),
            "fixed_unit_y_splitting": (
                "x=X_*+x_s+q_hat*x_u with x_s in ker(f_hat), "
                "||q_hat||_Y=1, and P_s=I-q_hat*f_hat fixed"
            ),
            "stable_radius_R_s": STABLE_GRAPH_RADIUS,
            "unit_unstable_radius_R_u_hat": UNIT_UNSTABLE_GRAPH_RADIUS,
            "split_radius_sum": SPLIT_RETURN_RADIUS,
            "full_ball_quantifier": (
                "all ||x_s||_Y<=0.0097 and |x_u|<=0.00025, including "
                "arbitrary continuous stable histories"
            ),
            "finite_node_initial_ball_forbidden": True,
            "domain_validated_here": False,
        },
        selected_return_definition={
            "event_functional": (
                "g(phi)=phi_v(0)-X_{*,v}(0), an affine complete-history row"
            ),
            "event_hyperplane": "g(phi)=0",
            "local_return_patch": (
                "the event hyperplane intersected with one declared "
                "complete-history neighborhood of X_*"
            ),
            "positive_orientation": "Dg[F(phi)]>0",
            "selected_event": (
                "the unique positive-oriented hit in one common near-period "
                "window whose returned history lies in the local patch"
            ),
            "earlier_negative_crossing_is_not_selected_return": True,
            "selected_does_not_mean_first_until_cover_closes": True,
        },
        nonlinear_flow_family_contract={
            "equation": "dX/dt=F(X_t), X_0=x in the full anisotropic ball",
            "physical_time_interval": "[-tau_max,T_plus]",
            "required_state_components": (
                "the full voltage history and current recovery coordinate"
            ),
            "required_uniformity": (
                "continuous in physical time and uniform over every initial "
                "history in the infinite-dimensional ball"
            ),
            "method_of_steps_requirement": (
                "include exact initial-history translation before each delay "
                "activates, all delayed branches, activation faces, and seams"
            ),
            "acceptable_engines": (
                "directed Taylor--Bernstein/method-of-steps enclosure, a "
                "validated mild-equation radii argument, or an equivalent "
                "continuous-history proof"
            ),
            "sampled_trajectories_or_finite_nodes_sufficient": False,
        },
        common_event_window_contract={
            "window": "I_T=[T_minus,T_plus], common to the full ball",
            "left_endpoint_sign": "sup_x g(X_{T_minus}(x)) <= -delta_minus < 0",
            "right_endpoint_sign": "inf_x g(X_{T_plus}(x)) >= delta_plus > 0",
            "speed_gate": (
                "inf_{x,t in I_T} Dg[F(X_t(x))] >= a_star > 0"
            ),
            "consequence": (
                "exactly one selected event T(x) in I_T for every x in the "
                "full ball"
            ),
            "parameter_sampling_forbidden": True,
            "validated_here": False,
        },
        c2_event_graph_contract={
            "regularity": "T belongs to C2 on an open neighborhood of the ball",
            "first_derivative": "T_h=-Dg[U_h(T)]/Dg[dot X(T)]",
            "second_core": (
                "W_hk(0)=V_hk(T)+dot U_h(T)T_k+dot U_k(T)T_h+"
                "ddot X(T)T_h*T_k"
            ),
            "second_derivative": "T_hk=-Dg[W_hk(0)]/Dg[dot X(T)]",
            "common_denominator": (
                "the same directed event-speed enclosure is retained in the "
                "state, first-event, and second-event rows"
            ),
            "endpoint_only_event_correction_forbidden": True,
            "validated_here": False,
        },
        complete_returned_history_tube_contract={
            "returned_history": (
                "R(x)=(theta -> v(T(x)+theta;x), w(T(x);x)) for every "
                "theta in [-tau_max,0]"
            ),
            "reference_history": "X_* at the fixed Route-C return phase",
            "tube_gate": "sup_x ||R(x)-X_*||_Y <= R_return",
            "coverage_interval": (
                "all physical times in [T_minus-tau_max,T_plus], not only "
                "the event endpoint"
            ),
            "local_patch_gate": (
                "R(x) lies in the declared local Route-C section patch"
            ),
            "moving_time_translation_retained": True,
            "finite_history_nodes_or_endpoint_only_bound_forbidden": True,
            "validated_here": False,
        },
        no_earlier_admissible_return_contract={
            "admissible_return": (
                "g(X_t(x))=0, Dg[F(X_t(x))]>0, and X_t(x) in the local "
                "Route-C return patch"
            ),
            "excluded_time_set": "0<t<T(x), uniformly over the full ball",
            "launch_collar": (
                "a directed short-time sign/speed argument separates t=0 "
                "from every later admissible return"
            ),
            "compact_middle_cover": (
                "cover [t_launch,T_minus] by directed slabs; on each slab "
                "prove at least one exclusion alternative"
            ),
            "exclusion_alternatives": (
                "section gap excludes zero; or event speed is nonpositive; "
                "or every zero lies outside the local complete-history patch"
            ),
            "negative_oriented_crossings_may_exist": True,
            "single_global_sign_requirement": False,
            "time_sampling_forbidden": True,
            "validated_here": False,
        },
        directed_cover_interface={
            "time_partition_boundaries": (
                "include t=0, launch collar, every delay activation, every "
                "candidate section crossing, T_minus, and T_plus"
            ),
            "history_support": (
                "each slab covers the complete lag interval needed by every "
                "delayed field evaluation"
            ),
            "seam_rule": (
                "adjacent enclosures overlap or share directed endpoint "
                "bounds; no uncovered floating-point seam is allowed"
            ),
            "event_row_order": (
                "form the event gap and speed from the correlated state and "
                "vector-field enclosure before testing signs"
            ),
            "local_patch_distance": (
                "use the inherited complete-history Y norm, not a current-"
                "state or finite-node proxy"
            ),
        },
        required_numeric_ingress={
            "T_minus": None,
            "T_plus": None,
            "left_endpoint_gap_margin_delta_minus": None,
            "right_endpoint_gap_margin_delta_plus": None,
            "uniform_event_speed_lower_a_star": None,
            "nonlinear_flow_family_Y_tube_remainder_upper": None,
            "returned_history_tube_radius_R_return": None,
            "local_section_patch_radius": None,
            "launch_collar_time": None,
            "launch_collar_separation_margin": None,
            "middle_time_slab_count": None,
            "no_earlier_hit_minimum_margin": None,
            "event_graph_first_derivative_norm_upper": None,
            "event_graph_second_derivative_norm_upper": None,
            "all_delay_activation_and_history_seams_covered": False,
            "one_common_tube_used_for_event_and_return_history": False,
            "stage4l_numeric_parent": None,
            "evidence_status": "OPEN_NONCLOSING",
        },
        first_missing_error_term={
            "name": "full_ball_nonlinear_mild_flow_remainder_in_Y",
            "value_upper": None,
            "domain": (
                "all initial histories in the Rs=0.0097, Ru_hat=0.00025 "
                "ball and all physical times through T_plus"
            ),
            "why_first": (
                "endpoint gap, speed, returned-history, no-earlier-return, "
                "and event-graph derivative bounds all require this same "
                "nonlinear state family"
            ),
            "finite_mesh_pilot_can_fill": False,
            "linear_stage4l_row_can_fill": False,
        },
        handoff_to_stage4m={
            "required_result_hash_binding": True,
            "same_R_s": STABLE_GRAPH_RADIUS,
            "same_R_u_hat": UNIT_UNSTABLE_GRAPH_RADIUS,
            "same_split_radius": SPLIT_RETURN_RADIUS,
            "same_fixed_q_hat_f_hat_projection": True,
            "supplies_common_domain_for_D2P": (
                "only after every Stage-4N numerical ingress and claim gate "
                "above is validated"
            ),
            "supplies_any_hessian_block_by_itself": False,
            "stage4m_must_still_enclose_variations_and_six_correlated_outputs": True,
        },
        theorem_boundary={
            "proved_here": (
                "only the source-bound nonlinear-return/event-graph contract "
                "and its dependency order"
            ),
            "not_proved_here": (
                "a nonlinear return tube, selected or first return, event "
                "graph, Hessian block, stable graph, crossing, onset, routing, "
                "capture, or safety theorem"
            ),
            "stage4l_substitution": (
                "forbidden: a linear terminal stable row has neither the "
                "nonlinear base family nor moving-event/no-earlier-hit data"
            ),
        },
        claim_status=claims,
    )


def build_stage4n_result(repository: Path) -> dict[str, Any]:
    repository = repository.resolve()
    contract = asdict(build_stage4n_contract(repository))
    return {
        "contract": contract,
        "manifest": {
            "schema_id": SCHEMA_ID,
            "result": RESULT_RELATIVE_PATH,
            "default_command": DEFAULT_COMMAND,
            "arithmetic_scope": ARITHMETIC_SCOPE,
            "contract_sha256": canonical_sha256(contract),
            "numeric_core_sha256": canonical_sha256(_numeric_core(contract)),
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


def validate_stage4n_result(
    payload: Mapping[str, Any],
    repository: Path,
    *,
    recompute: bool = False,
) -> None:
    if not isinstance(payload, Mapping) or set(payload) != TOP_KEYS:
        raise ValueError("the Stage-4N result has the wrong outer schema")
    contract = _mapping(payload.get("contract"), "Stage-4N contract")
    manifest = _mapping(payload.get("manifest"), "Stage-4N manifest")
    if set(contract) != {field.name for field in fields(Stage4NContract)}:
        raise ValueError("the Stage-4N contract schema changed")
    if (
        contract.get("schema_id") != SCHEMA_ID
        or contract.get("model_id") != MODEL_ID
        or contract.get("branch") != BRANCH
        or contract.get("status") != STATUS
    ):
        raise ValueError("the Stage-4N identity changed")

    repository = repository.resolve()
    _load_stage4m(repository)
    if contract.get("parent_result_sha256") != PARENT_RESULT_SHA256:
        raise ValueError("the Stage-4N parent ledger changed")
    if any("stage4l" in path.lower() for path in PARENT_RESULT_SHA256):
        raise ValueError("Stage 4N may not bind an unpublished Stage-4L result")

    claims = _mapping(contract.get("claim_status"), "Stage-4N claims")
    if set(claims) != set(TRUE_FLAGS) | set(FALSE_FLAGS):
        raise ValueError("the Stage-4N claim ledger changed")
    if any(claims.get(name) is not True for name in TRUE_FLAGS):
        raise ValueError("a Stage-4N contract fact was weakened")
    if any(claims.get(name) is not False for name in FALSE_FLAGS):
        raise ValueError("an open Stage-4N theorem gate was promoted")

    domain = _mapping(
        contract.get("coordinate_and_domain_registration"),
        "Stage-4N domain",
    )
    if (
        domain.get("stable_radius_R_s") != STABLE_GRAPH_RADIUS
        or domain.get("unit_unstable_radius_R_u_hat")
        != UNIT_UNSTABLE_GRAPH_RADIUS
        or domain.get("split_radius_sum") != SPLIT_RETURN_RADIUS
        or domain.get("finite_node_initial_ball_forbidden") is not True
        or domain.get("domain_validated_here") is not False
    ):
        raise ValueError("the Stage-4N anisotropic domain changed")

    selected = _mapping(
        contract.get("selected_return_definition"),
        "Stage-4N selected return",
    )
    if (
        selected.get("earlier_negative_crossing_is_not_selected_return")
        is not True
        or selected.get("selected_does_not_mean_first_until_cover_closes")
        is not True
        or "local patch" not in str(selected.get("selected_event"))
    ):
        raise ValueError("the Stage-4N selected-return definition changed")

    window = _mapping(
        contract.get("common_event_window_contract"),
        "Stage-4N event window",
    )
    if (
        "-delta_minus < 0" not in str(window.get("left_endpoint_sign"))
        or "delta_plus > 0" not in str(window.get("right_endpoint_sign"))
        or "a_star > 0" not in str(window.get("speed_gate"))
        or window.get("parameter_sampling_forbidden") is not True
        or window.get("validated_here") is not False
    ):
        raise ValueError("the Stage-4N event-window gate changed")

    returned = _mapping(
        contract.get("complete_returned_history_tube_contract"),
        "Stage-4N returned-history tube",
    )
    if (
        "every theta in [-tau_max,0]" not in str(
            returned.get("returned_history")
        )
        or returned.get("moving_time_translation_retained") is not True
        or returned.get("finite_history_nodes_or_endpoint_only_bound_forbidden")
        is not True
        or returned.get("validated_here") is not False
    ):
        raise ValueError("the Stage-4N complete-history tube changed")

    earlier = _mapping(
        contract.get("no_earlier_admissible_return_contract"),
        "Stage-4N no-earlier-return contract",
    )
    alternatives = str(earlier.get("exclusion_alternatives"))
    if (
        "section gap" not in alternatives
        or "event speed is nonpositive" not in alternatives
        or "outside the local complete-history patch" not in alternatives
        or earlier.get("negative_oriented_crossings_may_exist") is not True
        or earlier.get("single_global_sign_requirement") is not False
        or earlier.get("time_sampling_forbidden") is not True
        or earlier.get("validated_here") is not False
    ):
        raise ValueError("the Stage-4N no-earlier-return logic changed")

    numeric = _mapping(
        contract.get("required_numeric_ingress"),
        "Stage-4N numeric ingress",
    )
    allowed_false = {
        "all_delay_activation_and_history_seams_covered",
        "one_common_tube_used_for_event_and_return_history",
    }
    allowed_text = {"evidence_status"}
    for key, value in numeric.items():
        if key in allowed_false:
            if value is not False:
                raise ValueError("an open Stage-4N coverage gate was promoted")
        elif key in allowed_text:
            if value != "OPEN_NONCLOSING":
                raise ValueError("the Stage-4N evidence status changed")
        elif value is not None:
            raise ValueError(f"an unvalidated Stage-4N numeric field was filled: {key}")
    if numeric.get("stage4l_numeric_parent") is not None:
        raise ValueError("a Stage-4L numeric parent entered Stage 4N")

    first = _mapping(
        contract.get("first_missing_error_term"),
        "Stage-4N first missing error",
    )
    if (
        first.get("name") != "full_ball_nonlinear_mild_flow_remainder_in_Y"
        or first.get("value_upper") is not None
        or first.get("finite_mesh_pilot_can_fill") is not False
        or first.get("linear_stage4l_row_can_fill") is not False
    ):
        raise ValueError("the Stage-4N first missing error term changed")

    handoff = _mapping(
        contract.get("handoff_to_stage4m"), "Stage-4N handoff"
    )
    if (
        handoff.get("same_R_s") != STABLE_GRAPH_RADIUS
        or handoff.get("same_R_u_hat") != UNIT_UNSTABLE_GRAPH_RADIUS
        or handoff.get("same_split_radius") != SPLIT_RETURN_RADIUS
        or handoff.get("same_fixed_q_hat_f_hat_projection") is not True
        or handoff.get("supplies_any_hessian_block_by_itself") is not False
        or handoff.get(
            "stage4m_must_still_enclose_variations_and_six_correlated_outputs"
        )
        is not True
    ):
        raise ValueError("the Stage-4N to Stage-4M handoff changed")

    if set(manifest) != MANIFEST_KEYS:
        raise ValueError("the Stage-4N manifest schema changed")
    fixed_manifest = {
        "schema_id": SCHEMA_ID,
        "result": RESULT_RELATIVE_PATH,
        "default_command": DEFAULT_COMMAND,
        "arithmetic_scope": ARITHMETIC_SCOPE,
        "contract_sha256": canonical_sha256(contract),
        "numeric_core_sha256": canonical_sha256(_numeric_core(contract)),
        "parent_result_sha256": PARENT_RESULT_SHA256,
        "runtime": _runtime_record(),
    }
    if any(manifest.get(key) != value for key, value in fixed_manifest.items()):
        raise ValueError("the Stage-4N manifest fixed data changed")
    source_hashes = _mapping(
        manifest.get("source_sha256"), "Stage-4N source manifest"
    )
    dependency_hashes = _mapping(
        manifest.get("dependency_source_sha256"),
        "Stage-4N dependency manifest",
    )
    if set(source_hashes) != set(SOURCE_MANIFEST):
        raise ValueError("the Stage-4N source set changed")
    if set(dependency_hashes) != set(DEPENDENCY_SOURCE_MANIFEST):
        raise ValueError("the Stage-4N dependency set changed")
    for relative in SOURCE_MANIFEST:
        if source_hashes.get(relative) != _sha256_path(repository / relative):
            raise ValueError(f"the Stage-4N source changed: {relative}")
    for relative in DEPENDENCY_SOURCE_MANIFEST:
        if dependency_hashes.get(relative) != _sha256_path(repository / relative):
            raise ValueError(f"the Stage-4N dependency changed: {relative}")
    for relative, digest in PARENT_RESULT_SHA256.items():
        if _sha256_path(repository / relative) != digest:
            raise ValueError(f"the Stage-4N parent changed: {relative}")

    if recompute:
        expected = json.loads(
            json.dumps(asdict(build_stage4n_contract(repository)), sort_keys=True)
        )
        if dict(contract) != expected:
            raise ValueError("the Stage-4N contract differs from a fresh replay")


__all__ = [
    "ARITHMETIC_SCOPE",
    "BRANCH",
    "DEFAULT_COMMAND",
    "DEPENDENCY_SOURCE_MANIFEST",
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
    "Stage4NContract",
    "TEST_RELATIVE_PATH",
    "TOP_KEYS",
    "TRUE_FLAGS",
    "_numeric_core",
    "build_stage4n_contract",
    "build_stage4n_result",
    "canonical_sha256",
    "validate_stage4n_result",
]
