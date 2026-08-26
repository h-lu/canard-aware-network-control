"""Stage-5 contract for event-aligned physical-pulse parameter jets.

This file registers the proof architecture that replaces the unusably large
zero-centered variation majorants in the wide Route-C family pilot.  It is a
source-bound schema, not a numerical jet, event, stable-manifold, onset, or
routing certificate.  Every strict constant needed by those conclusions is
deliberately null until a directed computation supplies it.
"""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Mapping


SCHEMA_ID = "leaky-pulse-event-aligned-parameter-jet-contract-v1"
MODEL_ID = "autonomous-leaky-recovery-physical-pulse"

SOURCE_RELATIVE_PATH = (
    "src/canard_control/leaky_pulse_event_aligned_parameter_jet_contract.py"
)
GENERATOR_RELATIVE_PATH = (
    "experiments/leaky_pulse_event_aligned_parameter_jet_contract.py"
)
RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_pulse_event_aligned_parameter_jet_contract.json"
)
NOTE_RELATIVE_PATH = (
    "docs/leaky-pulse-event-aligned-parameter-jet-contract.md"
)
TEST_RELATIVE_PATH = (
    "tests/test_leaky_pulse_event_aligned_parameter_jet_contract.py"
)
FAMILY_PARENT_RELATIVE_PATH = (
    "experiments/results/leaky_pulse_inner_route_c_family_contract.json"
)
FAMILY_PARENT_SHA256 = (
    "6821551f3fab7d4bbc073af20b83daf055482055a81db23664d31c017de81f7c"
)
ROUTE_C_PARENT_RELATIVE_PATH = (
    "experiments/results/leaky_inner_stable_manifold_stage2_contract.json"
)
ROUTE_C_PARENT_SHA256 = (
    "eafa4d07b0558d9d4ce7423969379fa51875fcabce55af89a2378261fdb1e18d"
)
SOURCE_MANIFEST = (
    SOURCE_RELATIVE_PATH,
    GENERATOR_RELATIVE_PATH,
    NOTE_RELATIVE_PATH,
)
DEFAULT_COMMAND = (
    "PYTHONPATH=src /usr/bin/python3 "
    "experiments/leaky_pulse_event_aligned_parameter_jet_contract.py"
)
ARITHMETIC_SCOPE = (
    "source-bound Stage-5 proof schema for factorial-normalized parameter "
    "derivative jets z0,...,z4, a directed order-five remainder tube, an "
    "implicit Route-C event jet, a common-event complete-history pullback, "
    "the RFDE stable-coordinate gap, and an interval-Newton uniqueness gate; "
    "no strict numerical input is supplied by this contract"
)


JET_EQUATION_CONTRACT: dict[str, Any] = {
    "parameter": "delta=J-J0",
    "normalization": (
        "z(t,J0+delta)=sum_{k=0}^4 delta^k*z_k(t)/k!+R_5(t,delta), "
        "z_k=partial_J^k z(t,J0)"
    ),
    "lifted_linearization": (
        "L_t q=A_0(t)q(t)+A_4(t)q(t-4*sqrt(5))"
        "+A_5(t)q(t-5*sqrt(5))"
    ),
    "multilinear_derivatives": (
        "B_m(t)[q_1,...,q_m]=D^m F evaluated along z_0, with current "
        "and each delayed slot retained separately; B_m=0 for m>=4"
    ),
    "equations": {
        "z0": "dot(z_0)=F(z_0,z_0[-tau4],z_0[-tau5])+J0*chi_[0,1)*e_v",
        "z1": "dot(z_1)=L_t z_1+chi_[0,1)*e_v",
        "z2": "dot(z_2)=L_t z_2+B_2[z_1,z_1]",
        "z3": "dot(z_3)=L_t z_3+3*B_2[z_1,z_2]+B_3[z_1,z_1,z_1]",
        "z4": (
            "dot(z_4)=L_t z_4+4*B_2[z_1,z_3]+3*B_2[z_2,z_2]"
            "+6*B_3[z_1,z_1,z_2]"
        ),
    },
    "initial_history": (
        "z_0 is the exact J-independent quiet history; z_k=0 on the initial "
        "history for k=1,...,4"
    ),
    "breakpoint_rule": (
        "the pulse release t=1 and both delay translates by 4*sqrt(5) and "
        "5*sqrt(5) are exact cell boundaries for every coefficient"
    ),
}


REMAINDER_CONTRACT: dict[str, Any] = {
    "definition": (
        "R_5=z-sum_{k=0}^4 delta^k*z_k/k!, uniformly for |delta|<=h"
    ),
    "residual_source": (
        "substitute the degree-four parameter polynomial into the cubic RFDE; "
        "bound every parameter coefficient of degree at least five plus all "
        "time-Taylor truncation residuals by directed Bernstein arithmetic"
    ),
    "cell_inequality": (
        "D^+||R_5||_P<=mu_P(T)||R_5(t)||_P+b_4(T)||R_5(t-tau4)||_P"
        "+b_5(T)||R_5(t-tau5)||_P+rho_5(T,h)+N_2(T,r)"
    ),
    "acceptance_gate": (
        "on every exact time cell, a directed fixed-point radius r has "
        "strictly positive closure gap r-r_endpoint; translated remainder "
        "sources use already closed cells"
    ),
}


EVENT_JET_CONTRACT: dict[str, Any] = {
    "section": "g(t,J)=h_C(z_t(J))=v(t,J)-V_true(0)",
    "event_graph": (
        "T(delta)=t0+sum_{k=1}^4 tau_k*delta^k/k!+R_tau5(delta)"
    ),
    "transversality": "a=partial_t g(t0,J0), with 0 notin a_interval",
    "first_derivative": "tau_1=-g_J/g_t",
    "second_derivative": (
        "tau_2=-(g_JJ+2*g_tJ*tau_1+g_tt*tau_1^2)/g_t"
    ),
    "third_derivative": (
        "tau_3=-(g_JJJ+3*g_tJJ*tau_1+3*g_ttJ*tau_1^2"
        "+g_ttt*tau_1^3+3*(g_tJ+g_tt*tau_1)*tau_2)/g_t"
    ),
    "orders_three_and_four_rule": (
        "for k=3,4, expand the factorial Taylor coefficient of "
        "g(T(delta),J0+delta); isolate its unique linear term g_t*tau_k "
        "and set tau_k=-(all remaining order-k terms)/g_t"
    ),
    "event_remainder_gate": (
        "directed substitution of T(delta) into g gives an order-five "
        "residual; interval Newton in time and the uniform speed lower bound "
        "enclose R_tau5 and prove one event for every delta"
    ),
}


HISTORY_PULLBACK_CONTRACT: dict[str, Any] = {
    "phase_space": "Y=C([-5*sqrt(5),0],R)xR",
    "definition": (
        "Y(delta)=(theta->v(T(delta)+theta,J0+delta), "
        "w(T(delta),J0+delta)), theta in [-5*sqrt(5),0]"
    ),
    "first_jet": "Y_1(theta)=z_1(t0+theta)+tau_1*dot(z_0)(t0+theta)",
    "second_jet": (
        "Y_2(theta)=z_2+2*tau_1*dot(z_1)+tau_1^2*ddot(z_0)"
        "+tau_2*dot(z_0), evaluated at t0+theta"
    ),
    "orders_three_and_four_rule": (
        "obtain Y_k by the factorial Faà-di-Bruno composition of the flow "
        "jet z(t,J) with the event jet T(delta), cellwise in theta"
    ),
    "continuous_history_gate": (
        "Bernstein bounds cover every theta cell continuously, split at all "
        "translated time-grid breakpoints; sampled histories are forbidden"
    ),
    "remainder_decomposition": (
        "E_history=E_flow_jet+E_flow_remainder+F_tube*E_event_time"
        "+E_event_composition+E_section_center"
    ),
}


STABLE_AND_NEWTON_CONTRACT: dict[str, Any] = {
    "splitting": (
        "write the event history in validated coordinates y=(y_s,y_u) from "
        "the RFDE Riesz splitting"
    ),
    "stable_gap": "H(J)=f_u*y_u(J)-h_s(y_s(J))",
    "stable_gap_derivative": (
        "H'(J)=f_u*D_J y_u-Dh_s(y_s)*D_J y_s, including event-time terms "
        "already present in the common-event history jet"
    ),
    "interval_newton": "N(I)=m-H(m)/H'(I), where m=mid(I)",
    "acceptance_gate": (
        "all histories lie in the validated stable-graph chart; 0 notin "
        "H'(I); the directed interval Newton image N(I) is a strict subset "
        "of int(I); endpoint H intervals have the declared opposite signs"
    ),
    "conclusion_if_all_gates_close": (
        "one and only one J_c in I satisfies H(J_c)=0; this is a local "
        "stable-sheet intersection, not two-sided basin routing"
    ),
}


TRUE_FLAGS = (
    "factorial_parameter_jet_equations_z0_through_z4_registered",
    "order_five_remainder_tube_gate_registered",
    "implicit_route_c_event_jet_gate_registered",
    "common_event_complete_history_pullback_registered",
    "rfde_stable_coordinate_gap_registered",
    "interval_newton_uniqueness_gate_registered",
    "finite_section_coordinate_excluded_from_proof_inputs",
)

FALSE_FLAGS = (
    "z0_through_z4_directed_guides_validated",
    "order_five_remainder_tube_validated",
    "uniform_route_c_event_bracket_validated",
    "uniform_route_c_event_speed_validated",
    "event_time_jet_through_order_four_validated",
    "event_time_order_five_remainder_validated",
    "common_event_complete_history_jet_validated",
    "complete_history_remainder_validated",
    "rfde_unstable_riesz_covector_validated",
    "rfde_stable_projection_validated",
    "inner_local_stable_graph_validated",
    "stable_gap_endpoint_signs_validated",
    "stable_gap_derivative_excludes_zero_validated",
    "interval_newton_strict_inclusion_validated",
    "unique_local_physical_pulse_onset_validated",
    "two_sided_basin_routing_validated",
)


NUMERICAL_INPUT_TEMPLATE: dict[str, Any] = {
    "parameter_shard": {
        "center_J0": None,
        "half_width_h": None,
        "shard_index": None,
    },
    "jet_flow": {
        "coefficient_guide_hash": None,
        "cell_count": None,
        "maximum_z0_error": None,
        "maximum_z1_error": None,
        "maximum_z2_error": None,
        "maximum_z3_error": None,
        "maximum_z4_error": None,
        "maximum_order_five_remainder": None,
        "minimum_cell_closure_gap": None,
    },
    "event": {
        "time_bracket_lower": None,
        "time_bracket_upper": None,
        "lower_endpoint_sign": None,
        "upper_endpoint_sign": None,
        "uniform_speed_lower": None,
        "tau_1_interval": None,
        "tau_2_interval": None,
        "tau_3_interval": None,
        "tau_4_interval": None,
        "tau_order_five_remainder": None,
    },
    "history": {
        "continuous_theta_cell_count": None,
        "complete_history_radius": None,
        "stable_chart_radius": None,
        "history_ball_margin": None,
    },
    "stable_coordinate": {
        "unstable_riesz_covector_hash": None,
        "stable_projection_norm_upper": None,
        "stable_graph_hash": None,
        "stable_graph_radius": None,
        "stable_graph_D1_upper": None,
        "stable_graph_D2_upper": None,
        "left_endpoint_H_interval": None,
        "right_endpoint_H_interval": None,
        "H_prime_interval": None,
    },
    "interval_newton": {
        "input_interval": None,
        "midpoint_H_interval": None,
        "derivative_interval": None,
        "newton_image": None,
        "strict_interior_margin": None,
    },
}


def canonical_sha256(value: Any) -> str:
    encoded = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("utf-8")
    return sha256(encoded).hexdigest()


def _sha256_path(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _mapping(value: Any, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{name} must be a mapping")
    return value


def _load_bound_json(repository: Path, relative: str, expected: str) -> Any:
    path = repository / relative
    if _sha256_path(path) != expected:
        raise ValueError(f"event-jet bound parent changed: {relative}")
    return json.loads(path.read_text(encoding="utf-8"))


def _all_leaves_none(value: Any) -> bool:
    if isinstance(value, Mapping):
        return all(_all_leaves_none(item) for item in value.values())
    return value is None


def build_event_aligned_jet_contract(repository: Path) -> dict[str, Any]:
    repository = Path(repository).resolve()
    family = _load_bound_json(
        repository, FAMILY_PARENT_RELATIVE_PATH, FAMILY_PARENT_SHA256
    )
    route_c = _load_bound_json(
        repository, ROUTE_C_PARENT_RELATIVE_PATH, ROUTE_C_PARENT_SHA256
    )
    family_certificate = _mapping(family.get("certificate"), "family certificate")
    route_contract = _mapping(route_c.get("contract"), "Route-C contract")
    family_claims = _mapping(
        family_certificate.get("claim_status"), "family claims"
    )
    if family_claims.get("full_wide_interval_first_J_variation_enclosure_validated") is not False:
        raise ValueError("the family parent no longer records the variation gap")
    route_audit = _mapping(
        route_contract.get("explicit_voltage_section_audit"),
        "Route-C section audit",
    )
    if route_audit.get("exact_phase_zero_section_formula") != (
        "h_C(phi)=phi_v(0)-V_true(0)"
    ):
        raise ValueError("the Route-C section changed")

    contract = {
        "schema_id": SCHEMA_ID,
        "model_id": MODEL_ID,
        "stage": "Stage-5 event-aligned parameter-jet proof contract",
        "target_interval_exact": "[6021/20000,753/2500]",
        "route_c_section": "h_C(phi)=phi_v(0)-V_true(0)",
        "jet_equations": JET_EQUATION_CONTRACT,
        "highest_order_remainder_tube": REMAINDER_CONTRACT,
        "implicit_event_jet": EVENT_JET_CONTRACT,
        "common_event_history_pullback": HISTORY_PULLBACK_CONTRACT,
        "stable_gap_and_interval_newton": STABLE_AND_NEWTON_CONTRACT,
        "numerical_inputs": NUMERICAL_INPUT_TEMPLATE,
        "forbidden_substitutes": [
            "binary64 finite-section endpoint coordinate",
            "sampled history mesh norm",
            "pointwise orbit speed without a pulse-history tube",
            "Floquet eigenvalue without a validated RFDE Riesz splitting",
        ],
        "theorem_statement": (
            "This artifact fixes the equations and acceptance gates for an "
            "event-aligned fourth-order parameter-jet proof. It supplies no "
            "strict numerical constant, hence validates no jet tube, pulse "
            "event, complete-history family, stable-sheet intersection, "
            "physical onset, or two-sided routing."
        ),
        "claim_status": {
            **{name: True for name in TRUE_FLAGS},
            **{name: False for name in FALSE_FLAGS},
        },
    }
    return contract


def build_event_aligned_jet_result(repository: Path) -> dict[str, Any]:
    repository = Path(repository).resolve()
    contract = build_event_aligned_jet_contract(repository)
    return {
        "contract": contract,
        "manifest": {
            "schema_id": SCHEMA_ID,
            "result": RESULT_RELATIVE_PATH,
            "default_command": DEFAULT_COMMAND,
            "arithmetic_scope": ARITHMETIC_SCOPE,
            "parent_sha256": {
                FAMILY_PARENT_RELATIVE_PATH: FAMILY_PARENT_SHA256,
                ROUTE_C_PARENT_RELATIVE_PATH: ROUTE_C_PARENT_SHA256,
            },
            "source_sha256": {
                relative: _sha256_path(repository / relative)
                for relative in SOURCE_MANIFEST
            },
            "contract_sha256": canonical_sha256(contract),
        },
    }


def validate_event_aligned_jet_result(
    payload: Mapping[str, Any], repository: Path
) -> None:
    if not isinstance(payload, Mapping) or set(payload) != {"contract", "manifest"}:
        raise ValueError("event-jet result must contain contract and manifest")
    contract = _mapping(payload.get("contract"), "contract")
    manifest = _mapping(payload.get("manifest"), "manifest")
    if contract.get("schema_id") != SCHEMA_ID or manifest.get("schema_id") != SCHEMA_ID:
        raise ValueError("event-jet schema changed")
    if manifest.get("result") != RESULT_RELATIVE_PATH:
        raise ValueError("event-jet result path changed")
    if manifest.get("default_command") != DEFAULT_COMMAND:
        raise ValueError("event-jet default command changed")
    if manifest.get("arithmetic_scope") != ARITHMETIC_SCOPE:
        raise ValueError("event-jet arithmetic scope changed")
    if manifest.get("contract_sha256") != canonical_sha256(contract):
        raise ValueError("event-jet contract digest changed")
    if contract.get("jet_equations") != JET_EQUATION_CONTRACT:
        raise ValueError("event-jet coefficient equations changed")
    if contract.get("highest_order_remainder_tube") != REMAINDER_CONTRACT:
        raise ValueError("event-jet remainder gate changed")
    if contract.get("implicit_event_jet") != EVENT_JET_CONTRACT:
        raise ValueError("implicit event-jet recurrence changed")
    if contract.get("common_event_history_pullback") != HISTORY_PULLBACK_CONTRACT:
        raise ValueError("common-event history pullback changed")
    if contract.get("stable_gap_and_interval_newton") != STABLE_AND_NEWTON_CONTRACT:
        raise ValueError("stable-gap or interval-Newton gate changed")
    if contract.get("numerical_inputs") != NUMERICAL_INPUT_TEMPLATE:
        raise ValueError("an unvalidated numerical input was populated")
    if not _all_leaves_none(contract.get("numerical_inputs")):
        raise ValueError("strict event-jet inputs must remain null in this contract")
    claims = _mapping(contract.get("claim_status"), "claim status")
    if set(claims) != set(TRUE_FLAGS) | set(FALSE_FLAGS):
        raise ValueError("event-jet claim ledger changed")
    for name in TRUE_FLAGS:
        if claims.get(name) is not True:
            raise ValueError(f"registered event-jet schema claim removed: {name}")
    for name in FALSE_FLAGS:
        if claims.get(name) is not False:
            raise ValueError(f"open event-jet claim was promoted: {name}")
    repository = Path(repository).resolve()
    source_hashes = _mapping(manifest.get("source_sha256"), "source hashes")
    if set(source_hashes) != set(SOURCE_MANIFEST):
        raise ValueError("event-jet source manifest changed")
    for relative in SOURCE_MANIFEST:
        if source_hashes.get(relative) != _sha256_path(repository / relative):
            raise ValueError(f"event-jet source changed: {relative}")
    expected_parents = {
        FAMILY_PARENT_RELATIVE_PATH: FAMILY_PARENT_SHA256,
        ROUTE_C_PARENT_RELATIVE_PATH: ROUTE_C_PARENT_SHA256,
    }
    if dict(_mapping(manifest.get("parent_sha256"), "parent hashes")) != expected_parents:
        raise ValueError("event-jet parent manifest changed")
    for relative, expected in expected_parents.items():
        if _sha256_path(repository / relative) != expected:
            raise ValueError(f"event-jet bound parent changed: {relative}")


__all__ = [
    "EVENT_JET_CONTRACT",
    "FALSE_FLAGS",
    "HISTORY_PULLBACK_CONTRACT",
    "JET_EQUATION_CONTRACT",
    "NUMERICAL_INPUT_TEMPLATE",
    "REMAINDER_CONTRACT",
    "RESULT_RELATIVE_PATH",
    "STABLE_AND_NEWTON_CONTRACT",
    "TRUE_FLAGS",
    "build_event_aligned_jet_contract",
    "build_event_aligned_jet_result",
    "canonical_sha256",
    "validate_event_aligned_jet_result",
]
