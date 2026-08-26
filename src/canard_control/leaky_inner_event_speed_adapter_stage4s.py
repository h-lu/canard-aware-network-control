"""Stage-4S exact radius adapter for the Route-C event-speed gate.

Stage 2 proves a positive voltage-event speed on a complete-history max-norm
ball about the exact phase-zero Route-C history.  Stage 4N later declares a
preferred-B anisotropic initial domain, but intentionally leaves its common
nonlinear event window and returned-history tube open.  This module connects
the two ledgers without pretending that the missing tube has been enclosed.

The exact triangle inequality places every *declared initial history* at
distance at most ``0.0097 + 0.00025 = 0.00995`` from the Route-C centre.  The
same radius is strictly inside the source-bound Stage-2 ball.  Hence any
evolved history that is proved to stay in that smaller ball has directed
event speed at least

    a_* = a_orbit_lower - L_F_upper * 0.00995 > 0.

This is a proved conditional implication.  It does not prove the common
event window, the nonlinear flow-tube containment premise, a returned-history
containment, a selected return, or any downstream stable-sheet/onset claim.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from decimal import Decimal, ROUND_FLOOR, localcontext
from functools import lru_cache
from hashlib import sha256
import json
from pathlib import Path
import platform
from typing import Any, Mapping

from canard_control.leaky_inner_nonlinear_selected_return_tube_stage4n_contract import (
    BRANCH as STAGE4N_BRANCH,
    MODEL_ID as STAGE4N_MODEL_ID,
    RESULT_RELATIVE_PATH as STAGE4N_RESULT_RELATIVE_PATH,
    SPLIT_RETURN_RADIUS,
    STABLE_GRAPH_RADIUS,
    UNIT_UNSTABLE_GRAPH_RADIUS,
    validate_stage4n_result,
)
from canard_control.leaky_inner_stable_manifold_stage2_contract import (
    BRANCH as STAGE2_BRANCH,
    MODEL_ID as STAGE2_MODEL_ID,
    validate_stage2_stable_manifold_result,
)


SCHEMA_ID = "leaky-inner-event-speed-adapter-stage4s-v1"
MODEL_ID = STAGE4N_MODEL_ID
BRANCH = STAGE4N_BRANCH
STATUS = "PROVED_CONDITIONAL_IMPLICATION_SOURCE_BOUND"

SOURCE_RELATIVE_PATH = (
    "src/canard_control/leaky_inner_event_speed_adapter_stage4s.py"
)
GENERATOR_RELATIVE_PATH = (
    "experiments/leaky_inner_event_speed_adapter_stage4s.py"
)
RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_inner_event_speed_adapter_stage4s.json"
)
NOTE_RELATIVE_PATH = "docs/leaky-inner-event-speed-adapter-stage4s.md"
TEST_RELATIVE_PATH = "tests/test_leaky_inner_event_speed_adapter_stage4s.py"

STAGE2_RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_inner_stable_manifold_stage2_contract.json"
)
STAGE2_RESULT_SHA256 = (
    "eafa4d07b0558d9d4ce7423969379fa51875fcabce55af89a2378261fdb1e18d"
)
STAGE4N_RESULT_SHA256 = (
    "b64f5230bb870b889fdc341d5d5139ea4ccac6faa7752ff2a5682eb0206cf160"
)
PARENT_RESULT_SHA256 = {
    STAGE2_RESULT_RELATIVE_PATH: STAGE2_RESULT_SHA256,
    STAGE4N_RESULT_RELATIVE_PATH: STAGE4N_RESULT_SHA256,
}

SOURCE_MANIFEST = (
    SOURCE_RELATIVE_PATH,
    GENERATOR_RELATIVE_PATH,
    NOTE_RELATIVE_PATH,
    TEST_RELATIVE_PATH,
)
DEPENDENCY_SOURCE_MANIFEST = (
    "src/canard_control/leaky_inner_stable_manifold_stage2_contract.py",
    "src/canard_control/leaky_inner_nonlinear_selected_return_tube_stage4n_contract.py",
)

DEFAULT_COMMAND = (
    "PYTHONPATH=src /usr/bin/python3 "
    "experiments/leaky_inner_event_speed_adapter_stage4s.py"
)
ARITHMETIC_SCOPE = (
    "normal validation and byte binding of the Stage-2 Route-C section-speed "
    "certificate and the open Stage-4N selected-return contract; exact-decimal "
    "preferred-B radius addition, strict radius inclusion, and directed "
    "a_orbit-L_F*R lower-bound arithmetic; a proved implication from a common "
    "complete-history tube containment to positive event speed; no nonlinear "
    "tube, common event window, returned-history containment, selected return, "
    "Hessian, graph, crossing, onset, routing, capture, or safety promotion"
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
    "dependency_source_sha256",
    "parent_result_sha256",
    "runtime",
}

TRUE_FLAGS = (
    "stage2_and_stage4n_parent_bytes_and_claim_boundaries_validated",
    "same_model_and_route_c_event_row_registered",
    "preferred_b_fixed_unit_y_coordinate_triangle_proved",
    "preferred_b_declared_initial_ball_radius_sum_exact",
    "preferred_b_radius_strictly_inside_stage2_speed_ball_proved",
    "directed_event_speed_lower_on_smaller_ball_proved",
    "directed_event_speed_lower_strictly_positive",
    "stage4n_speed_gate_reduced_to_common_window_history_containment",
    "endpoint_speed_gate_reduced_to_returned_history_containment",
    "finite_history_nodes_cannot_supply_the_containment_premise",
)
FALSE_FLAGS = (
    "stage4n_declared_initial_domain_is_a_validated_return_domain",
    "nonlinear_flow_family_on_full_anisotropic_ball_validated",
    "common_event_window_validated",
    "common_window_histories_lie_in_smaller_ball_validated",
    "uniform_positive_event_speed_on_stage4n_window_validated",
    "complete_returned_history_tube_validated",
    "returned_histories_lie_in_smaller_ball_validated",
    "unique_selected_event_on_common_window_validated",
    "c2_selected_return_map_validated",
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
class Stage4SEventSpeedAdapter:
    schema_id: str
    model_id: str
    branch: str
    status: str
    parent_result_sha256: dict[str, str]
    center_norm_and_event_row_registration: dict[str, Any]
    exact_radius_adapter: dict[str, Any]
    directed_event_speed_adapter: dict[str, Any]
    conditional_stage4n_discharge: dict[str, Any]
    remaining_dependency_order: dict[str, Any]
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
        raise ValueError(f"{name} must be a directed decimal string")
    number = Decimal(value)
    if not number.is_finite():
        raise ValueError(f"{name} must be finite")
    return number


def _down(value: Decimal) -> str:
    if not value.is_finite():
        raise ArithmeticError("a directed lower bound became nonfinite")
    return format(value, "f")


@lru_cache(maxsize=4)
def _validated_stage2_payload(repository_text: str) -> Mapping[str, Any]:
    repository = Path(repository_text)
    path = repository / STAGE2_RESULT_RELATIVE_PATH
    payload = json.loads(path.read_text(encoding="utf-8"))
    validate_stage2_stable_manifold_result(payload, repository)
    return payload


@lru_cache(maxsize=4)
def _validated_stage4n_payload(repository_text: str) -> Mapping[str, Any]:
    repository = Path(repository_text)
    path = repository / STAGE4N_RESULT_RELATIVE_PATH
    payload = json.loads(path.read_text(encoding="utf-8"))
    validate_stage4n_result(payload, repository, recompute=False)
    return payload


def _load_parent(
    repository: Path,
    relative: str,
    expected_sha256: str,
    loader: Any,
) -> Mapping[str, Any]:
    path = repository / relative
    if _sha256_path(path) != expected_sha256:
        raise ValueError(f"the bound parent result changed: {relative}")
    return _mapping(loader(str(repository.resolve())), relative)


def _numeric_core(certificate: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "exact_radius_adapter": certificate["exact_radius_adapter"],
        "directed_event_speed_adapter": certificate[
            "directed_event_speed_adapter"
        ],
        "conditional_stage4n_discharge": certificate[
            "conditional_stage4n_discharge"
        ],
        "claim_status": certificate["claim_status"],
    }


def _runtime_record() -> dict[str, str]:
    return {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "arithmetic": (
            "Decimal exact input parsing with ROUND_FLOOR lower-bound "
            "subtraction; normal parent validation and SHA-256 binding"
        ),
    }


def build_stage4s_event_speed_adapter(
    repository: Path,
) -> Stage4SEventSpeedAdapter:
    repository = repository.resolve()
    stage2 = _load_parent(
        repository,
        STAGE2_RESULT_RELATIVE_PATH,
        STAGE2_RESULT_SHA256,
        _validated_stage2_payload,
    )
    stage4n = _load_parent(
        repository,
        STAGE4N_RESULT_RELATIVE_PATH,
        STAGE4N_RESULT_SHA256,
        _validated_stage4n_payload,
    )
    stage2_contract = _mapping(stage2.get("contract"), "Stage-2 contract")
    stage4n_contract = _mapping(stage4n.get("contract"), "Stage-4N contract")
    if (
        stage2_contract.get("model_id") != STAGE2_MODEL_ID
        or stage4n_contract.get("model_id") != STAGE4N_MODEL_ID
        or STAGE2_MODEL_ID != STAGE4N_MODEL_ID
        or stage2_contract.get("branch") != STAGE2_BRANCH
        or stage4n_contract.get("branch") != STAGE4N_BRANCH
    ):
        raise ValueError("the Stage-2/Stage-4N model or branch identity changed")

    section = _mapping(
        stage2_contract.get("explicit_voltage_section_audit"),
        "Stage-2 explicit voltage section",
    )
    stage2_claims = _mapping(
        stage2_contract.get("claim_status"), "Stage-2 claims"
    )
    domain = _mapping(
        stage4n_contract.get("coordinate_and_domain_registration"),
        "Stage-4N domain",
    )
    selected = _mapping(
        stage4n_contract.get("selected_return_definition"),
        "Stage-4N selected return",
    )
    stage4n_claims = _mapping(
        stage4n_contract.get("claim_status"), "Stage-4N claims"
    )

    if (
        section.get("exact_phase_zero_section_formula")
        != "h_C(phi)=phi_v(0)-V_true(0)"
        or section.get("state_component") != "voltage"
        or section.get("normalized_phase") != "0"
        or section.get("section_functional_norm_upper") != "1"
        or section.get("pointwise_orbit_speed_validated") is not True
        or section.get("uniform_event_speed_on_declared_section_ball_validated")
        is not True
        or stage2_claims.get(
            "exact_phase_zero_voltage_section_uniform_speed_on_declared_ball_validated"
        )
        is not True
        or stage2_claims.get(
            "uniform_phase_section_speed_on_return_tube_validated"
        )
        is not False
    ):
        raise ValueError("the Stage-2 Route-C speed boundary changed")
    if (
        domain.get("history_space")
        != "Y=C([-tau_max,0],R)_v x R_w with the inherited max norm"
        or domain.get("stable_radius_R_s") != STABLE_GRAPH_RADIUS
        or domain.get("unit_unstable_radius_R_u_hat")
        != UNIT_UNSTABLE_GRAPH_RADIUS
        or domain.get("split_radius_sum") != SPLIT_RETURN_RADIUS
        or "||q_hat||_Y=1" not in str(
            domain.get("fixed_unit_y_splitting")
        )
        or domain.get("domain_validated_here") is not False
        or selected.get("event_functional")
        != "g(phi)=phi_v(0)-X_{*,v}(0), an affine complete-history row"
        or stage4n_claims.get(
            "uniform_positive_event_speed_lower_bound_validated"
        )
        is not False
    ):
        raise ValueError("the Stage-4N Route-C domain or event row changed")

    stable_radius = _decimal(STABLE_GRAPH_RADIUS, "stable radius")
    unstable_radius = _decimal(
        UNIT_UNSTABLE_GRAPH_RADIUS, "unit unstable radius"
    )
    split_radius = _decimal(SPLIT_RETURN_RADIUS, "split radius")
    if stable_radius + unstable_radius != split_radius:
        raise ArithmeticError("the preferred-B radius sum no longer closes")

    stage2_radius = _decimal(
        section.get("declared_section_ball_radius"),
        "Stage-2 declared section-ball radius",
    )
    orbit_speed_lower = _decimal(
        section.get("physical_voltage_event_speed_at_orbit_lower"),
        "Stage-2 orbit event-speed lower bound",
    )
    field_lipschitz_upper = _decimal(
        section.get("vector_field_lipschitz_upper_on_declared_section_ball"),
        "Stage-2 field Lipschitz upper bound",
    )
    inherited_speed_lower = _decimal(
        section.get("uniform_event_speed_lower_on_declared_section_ball"),
        "Stage-2 declared-ball event-speed lower bound",
    )
    if split_radius >= stage2_radius:
        raise ArithmeticError("the preferred-B radius left the Stage-2 ball")
    with localcontext() as context:
        context.prec = 96
        context.rounding = ROUND_FLOOR
        inclusion_slack = stage2_radius - split_radius
        variation_upper = field_lipschitz_upper * split_radius
        smaller_ball_speed_lower = orbit_speed_lower - variation_upper
    if smaller_ball_speed_lower <= 0:
        raise ArithmeticError("the smaller-ball event-speed lower bound is not positive")
    if smaller_ball_speed_lower < inherited_speed_lower:
        raise ArithmeticError("the radius restriction unexpectedly weakened speed")

    claims = {name: True for name in TRUE_FLAGS}
    claims.update({name: False for name in FALSE_FLAGS})
    return Stage4SEventSpeedAdapter(
        schema_id=SCHEMA_ID,
        model_id=MODEL_ID,
        branch=BRANCH,
        status=STATUS,
        parent_result_sha256=dict(PARENT_RESULT_SHA256),
        center_norm_and_event_row_registration={
            "history_space": domain["history_space"],
            "history_norm": "||(phi,w)||_Y=max(||phi||_infinity,|w|)",
            "stage2_center": "the exact phase-zero Route-C history V_true",
            "stage4n_center": "X_* at the fixed Route-C return phase",
            "center_identification": (
                "X_* is the exact phase-zero Route-C reference history by "
                "the declared Route-C coordinate convention"
            ),
            "center_identity_status": "DECLARED_ROUTE_C_DEFINITION",
            "stage2_event_functional": section[
                "exact_phase_zero_section_formula"
            ],
            "stage4n_event_functional": selected["event_functional"],
            "same_voltage_current-history_row_after_center_identification": True,
            "event_functional_norm_upper": section[
                "section_functional_norm_upper"
            ],
            "no_finite_node_norm_substitution": True,
        },
        exact_radius_adapter={
            "coordinate_formula": "x-X_*=x_s+q_hat*x_u",
            "unit_vector_normalization": "||q_hat||_Y=1",
            "triangle_inequality": (
                "||x-X_*||_Y<=||x_s||_Y+||q_hat||_Y*|x_u|"
            ),
            "stable_radius_R_s": STABLE_GRAPH_RADIUS,
            "unit_unstable_radius_R_u_hat": UNIT_UNSTABLE_GRAPH_RADIUS,
            "preferred_b_radius_sum_exact": SPLIT_RETURN_RADIUS,
            "stage2_declared_ball_radius_lower": _down(stage2_radius),
            "strict_inclusion_slack_lower": _down(inclusion_slack),
            "preferred_b_declared_initial_ball_inside_stage2_ball": True,
            "stage4n_return_domain_validated": False,
        },
        directed_event_speed_adapter={
            "orbit_event_speed_lower": _down(orbit_speed_lower),
            "vector_field_lipschitz_upper": _down(field_lipschitz_upper),
            "smaller_complete_history_ball_radius": SPLIT_RETURN_RADIUS,
            "event_speed_variation_upper": _down(variation_upper),
            "formula": "a_*(R)=a_orbit_lower-L_F_upper*R",
            "smaller_ball_event_speed_lower": _down(
                smaller_ball_speed_lower
            ),
            "inherited_stage2_declared_ball_event_speed_lower": _down(
                inherited_speed_lower
            ),
            "smaller_ball_bound_strictly_positive": True,
            "smaller_ball_bound_at_least_inherited_bound": True,
            "arithmetic_direction": (
                "lower minus upper times exact nonnegative radius, rounded "
                "toward minus infinity"
            ),
        },
        conditional_stage4n_discharge={
            "common_window_containment_premise": (
                "for every declared initial history x and every t in "
                "[T_minus,T_plus], ||X_t(x)-X_*||_Y<=0.00995"
            ),
            "common_window_containment_premise_validated": False,
            "proved_conclusion_if_premise_holds": (
                "inf_{x,t in [T_minus,T_plus]} Dg[F(X_t(x))] >= "
                + _down(smaller_ball_speed_lower)
                + " > 0"
            ),
            "stage4n_uniform_event_speed_ingress_can_then_be_filled_with": _down(
                smaller_ball_speed_lower
            ),
            "returned_history_containment_premise": (
                "for every declared x, ||R(x)-X_*||_Y<=0.00995"
            ),
            "returned_history_containment_premise_validated": False,
            "endpoint_speed_conclusion_if_returned_history_premise_holds": (
                "Dg[F(R(x))]>=" + _down(smaller_ball_speed_lower) + ">0"
            ),
            "logical_status": "PROVED_IMPLICATION_WITH_OPEN_CONTAINMENT_PREMISES",
            "stage4n_speed_claim_promoted_here": False,
        },
        remaining_dependency_order={
            "next_single_shared_object": (
                "one source-bound complete-history nonlinear flow tube on the "
                "full preferred-B initial ball through a common event window"
            ),
            "what_that_object_can_discharge": (
                "endpoint signs, the present speed premise, returned-history "
                "containment, and the domain for event-time derivatives"
            ),
            "still_separate_after_tube": (
                "no-earlier-admissible-return cover and six correlated "
                "continuous-history Hessian block bounds"
            ),
            "sampled_trajectories_or_nodal_histories_sufficient": False,
        },
        theorem_boundary={
            "proved_here": (
                "the preferred-B declared initial-radius inclusion and the "
                "conditional uniform positive Route-C event-speed theorem on "
                "any common window contained in the radius-0.00995 Y ball"
            ),
            "not_proved_here": (
                "the containment premises themselves, a common event window, "
                "a nonlinear returned-history tube, selected return, C2 map, "
                "Hessian blocks, stable graph, crossing, physical onset, "
                "routing, capture, or safety theorem"
            ),
            "forbidden_upgrade": (
                "do not relabel this conditional implication as Stage-4N "
                "uniform-speed validation until the full continuous-history "
                "window containment is source-bound"
            ),
        },
        claim_status=claims,
    )


def build_stage4s_event_speed_result(repository: Path) -> dict[str, Any]:
    repository = repository.resolve()
    certificate = asdict(build_stage4s_event_speed_adapter(repository))
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
            "dependency_source_sha256": {
                relative: _sha256_path(repository / relative)
                for relative in DEPENDENCY_SOURCE_MANIFEST
            },
            "parent_result_sha256": dict(PARENT_RESULT_SHA256),
            "runtime": _runtime_record(),
        },
    }


def validate_stage4s_event_speed_result(
    payload: Mapping[str, Any],
    repository: Path,
    *,
    recompute: bool = False,
) -> None:
    if not isinstance(payload, Mapping) or set(payload) != TOP_KEYS:
        raise ValueError("the Stage-4S event-speed result has the wrong schema")
    certificate = _mapping(payload.get("certificate"), "Stage-4S certificate")
    manifest = _mapping(payload.get("manifest"), "Stage-4S manifest")
    if set(certificate) != {
        field.name for field in fields(Stage4SEventSpeedAdapter)
    }:
        raise ValueError("the Stage-4S event-speed certificate schema changed")
    if (
        certificate.get("schema_id") != SCHEMA_ID
        or certificate.get("model_id") != MODEL_ID
        or certificate.get("branch") != BRANCH
        or certificate.get("status") != STATUS
        or certificate.get("parent_result_sha256") != PARENT_RESULT_SHA256
    ):
        raise ValueError("the Stage-4S event-speed identity changed")

    claims = _mapping(certificate.get("claim_status"), "Stage-4S claims")
    if set(claims) != set(TRUE_FLAGS) | set(FALSE_FLAGS):
        raise ValueError("the Stage-4S event-speed claim ledger changed")
    if any(claims.get(name) is not True for name in TRUE_FLAGS):
        raise ValueError("a proved Stage-4S event-speed fact was weakened")
    if any(claims.get(name) is not False for name in FALSE_FLAGS):
        raise ValueError("an open Stage-4S event-speed gate was promoted")

    repository = repository.resolve()
    expected_certificate = asdict(build_stage4s_event_speed_adapter(repository))
    if dict(certificate) != expected_certificate:
        raise ValueError("the Stage-4S event-speed certificate changed")

    if set(manifest) != MANIFEST_KEYS:
        raise ValueError("the Stage-4S event-speed manifest schema changed")
    fixed_manifest = {
        "schema_id": SCHEMA_ID,
        "result": RESULT_RELATIVE_PATH,
        "default_command": DEFAULT_COMMAND,
        "arithmetic_scope": ARITHMETIC_SCOPE,
        "certificate_sha256": canonical_sha256(certificate),
        "numeric_core_sha256": canonical_sha256(_numeric_core(certificate)),
        "parent_result_sha256": PARENT_RESULT_SHA256,
        "runtime": _runtime_record(),
    }
    if any(manifest.get(key) != value for key, value in fixed_manifest.items()):
        raise ValueError("the Stage-4S event-speed manifest fixed data changed")

    source_hashes = _mapping(
        manifest.get("source_sha256"), "Stage-4S source hashes"
    )
    dependency_hashes = _mapping(
        manifest.get("dependency_source_sha256"),
        "Stage-4S dependency hashes",
    )
    if set(source_hashes) != set(SOURCE_MANIFEST):
        raise ValueError("the Stage-4S event-speed source set changed")
    if set(dependency_hashes) != set(DEPENDENCY_SOURCE_MANIFEST):
        raise ValueError("the Stage-4S dependency source set changed")
    for relative in SOURCE_MANIFEST:
        if source_hashes.get(relative) != _sha256_path(repository / relative):
            raise ValueError(f"the Stage-4S source changed: {relative}")
    for relative in DEPENDENCY_SOURCE_MANIFEST:
        if dependency_hashes.get(relative) != _sha256_path(repository / relative):
            raise ValueError(f"the Stage-4S dependency changed: {relative}")
    for relative, digest in PARENT_RESULT_SHA256.items():
        if _sha256_path(repository / relative) != digest:
            raise ValueError(f"the Stage-4S parent changed: {relative}")

    if recompute:
        replay = build_stage4s_event_speed_result(repository)
        if payload != replay:
            raise ValueError("the Stage-4S event-speed result differs from replay")


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
    "Stage4SEventSpeedAdapter",
    "TEST_RELATIVE_PATH",
    "TOP_KEYS",
    "TRUE_FLAGS",
    "_numeric_core",
    "build_stage4s_event_speed_adapter",
    "build_stage4s_event_speed_result",
    "canonical_sha256",
    "validate_stage4s_event_speed_result",
]
