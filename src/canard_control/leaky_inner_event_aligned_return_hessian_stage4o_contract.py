"""Stage-4O analytic contract for the event-aligned return Hessian.

Stage 4M records the six projected Hessian blocks and Stage 4N records the
nonlinear selected-event domain that those blocks need.  This module supplies
the missing exact analytic spine.  It differentiates the fixed-time RFDE
flow twice, differentiates the affine event equation twice, translates the
whole returned voltage history, applies the moving event-phase projection
exactly once, and only then applies the fixed stable/unstable output pair.

The audit also separates two issues that earlier contracts left entangled.

* A selected C2 event branch is sufficient to define the six Hessian blocks;
  a no-earlier-hit cover is needed only to identify that branch as the first
  physical local return.
* A separately normed bound on the complete intermediate stable propagator is
  not logically necessary.  A direct signed terminal bilinear kernel can keep
  every intermediate first variation inside the correlated source integral.
  Continuous intermediate-time kernel coverage is nevertheless unavoidable.

There is an additional analytic gate.  On the declared arbitrary-continuous
history ball, the moving translation into a complete returned history is not
automatically C2.  The required smoothing threshold is T>2*tau_max, whereas
the one-period centre has T<2*tau_max.  More specifically,
T<tau_0+tau_1 shows that the earliest returned-history time still reads an
undifferentiated initial voltage history when a second time derivative is
formed.  A compatible C1 solution-history manifold, a stronger history norm,
an eventual-smoothing return, or an equivalent fixed-phase reformulation must
therefore be validated before the displayed D2P formula is a theorem on the
full domain.

This is a source-bound formal contract.  Every numerical theorem ingress and
every return, Hessian, graph, crossing, onset, routing, capture, and safety
claim remains null or false.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from decimal import Decimal, localcontext
from hashlib import sha256
import json
from pathlib import Path
import platform
from typing import Any, Mapping

from canard_control.leaky_inner_enlarged_return_hessian_stage4m_contract import (
    HESSIAN_FIELD_NAMES,
    RESULT_RELATIVE_PATH as STAGE4M_RESULT_RELATIVE_PATH,
    validate_stage4m_result,
)
from canard_control.leaky_inner_nonlinear_selected_return_tube_stage4n_contract import (
    RESULT_RELATIVE_PATH as STAGE4N_RESULT_RELATIVE_PATH,
    validate_stage4n_result,
)
from canard_control.leaky_inner_nonlinear_selected_return_tube_stage4n_feasibility import (
    RESULT_RELATIVE_PATH as STAGE4N_FEASIBILITY_RESULT_RELATIVE_PATH,
    validate_stage4n_feasibility_result,
)
from canard_control.leaky_inner_terminal_stable_row_stage4l import (
    RESULT_RELATIVE_PATH as STAGE4L_RESULT_RELATIVE_PATH,
    validate_stage4l_result,
)
from canard_control.leaky_inner_word_primitive_stage4i import (
    RESULT_RELATIVE_PATH as STAGE4I_RESULT_RELATIVE_PATH,
    validate_stage4i_result,
)
from canard_control.leaky_periodic_branch_artifact import MODEL_EQUATION


SCHEMA_ID = "leaky-inner-event-aligned-return-hessian-stage4o-contract-v1"
MODEL_ID = "autonomous-leaky-recovery-two-delay-fhn-bistable-proposal"
BRANCH = "inner_saddle_candidate_selected_near_period_return"
STATUS = "OPEN_ANALYTIC_CONTRACT"

SOURCE_RELATIVE_PATH = (
    "src/canard_control/"
    "leaky_inner_event_aligned_return_hessian_stage4o_contract.py"
)
GENERATOR_RELATIVE_PATH = (
    "experiments/"
    "leaky_inner_event_aligned_return_hessian_stage4o_contract.py"
)
RESULT_RELATIVE_PATH = (
    "experiments/results/"
    "leaky_inner_event_aligned_return_hessian_stage4o_contract.json"
)
NOTE_RELATIVE_PATH = (
    "docs/leaky-inner-event-aligned-return-hessian-stage4o-contract.md"
)
TEST_RELATIVE_PATH = (
    "tests/test_leaky_inner_event_aligned_return_hessian_stage4o_contract.py"
)

STAGE4I_RESULT_SHA256 = (
    "1248e9d95444f3cc12565c1e11b4bbeab3d4a9a7bb8922893e38b1ffa439f73e"
)
STAGE4L_RESULT_SHA256 = (
    "672f92c7c456a54f39afab7d2a5f92b783311cc0ee5341a4d2e72a588039017e"
)
STAGE4M_RESULT_SHA256 = (
    "1a7f89c4c61480a76149b88ae6a15fa40b11425f4d678615af3469b59f75100c"
)
STAGE4N_RESULT_SHA256 = (
    "b64f5230bb870b889fdc341d5d5139ea4ccac6faa7752ff2a5682eb0206cf160"
)
STAGE4N_FEASIBILITY_RESULT_SHA256 = (
    "5e7214a2f5ba8ca22649c677a1d054b32342b5cc25966bd8e1da7600c605f1de"
)

PARENT_RESULT_SHA256 = {
    STAGE4I_RESULT_RELATIVE_PATH: STAGE4I_RESULT_SHA256,
    STAGE4L_RESULT_RELATIVE_PATH: STAGE4L_RESULT_SHA256,
    STAGE4M_RESULT_RELATIVE_PATH: STAGE4M_RESULT_SHA256,
    STAGE4N_RESULT_RELATIVE_PATH: STAGE4N_RESULT_SHA256,
    STAGE4N_FEASIBILITY_RESULT_RELATIVE_PATH:
        STAGE4N_FEASIBILITY_RESULT_SHA256,
}

SOURCE_MANIFEST = (
    SOURCE_RELATIVE_PATH,
    GENERATOR_RELATIVE_PATH,
    NOTE_RELATIVE_PATH,
    TEST_RELATIVE_PATH,
)
DEPENDENCY_SOURCE_MANIFEST = (
    "src/canard_control/leaky_inner_word_primitive_stage4i.py",
    "src/canard_control/leaky_inner_terminal_stable_row_stage4l.py",
    "src/canard_control/leaky_inner_enlarged_return_hessian_stage4m_contract.py",
    "src/canard_control/leaky_inner_nonlinear_selected_return_tube_stage4n_contract.py",
    "src/canard_control/leaky_inner_nonlinear_selected_return_tube_stage4n_feasibility.py",
    "src/canard_control/leaky_periodic_branch_artifact.py",
)

DEFAULT_COMMAND = (
    "OPENBLAS_NUM_THREADS=8 OMP_NUM_THREADS=1 PYTHONPATH=src "
    "/usr/bin/python3 experiments/"
    "leaky_inner_event_aligned_return_hessian_stage4o_contract.py"
)
ARITHMETIC_SCOPE = (
    "exact formal differentiation of the reduced leaky two-delay RFDE, its "
    "affine selected-event equation, complete returned-history translation, "
    "one moving event-phase projection, and the fixed unit-Y stable/unstable "
    "output pair; byte-exact normal validation of Stage 4I, 4L, 4M, 4N and "
    "the Stage-4N feasibility diagnostic; no numerical flow, event, kernel, "
    "Hessian, graph, crossing, onset, routing, capture, or safety ingress"
)

EXACT_MODEL_EQUATION = (
    "v'=v-v^3/3-w+epsilon*kappa_1*((v_tau0+v_tau1)/2-v)"
    "+epsilon*kappa_3*(((v_tau0-1)^3+(v_tau1-1)^3)/2"
    "-(v-1)^3); w'=epsilon*(v-a-w)"
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
    "all_parent_bytes_and_claim_boundaries_validated",
    "exact_reduced_model_d1_d2_d3_registered",
    "affine_initial_data_second_jet_zero_registered",
    "exact_fixed_time_second_variation_formula_registered",
    "exact_implicit_event_Tx_Txx_registered",
    "complete_terminal_history_translation_registered",
    "moving_event_phase_projection_applied_exactly_once_registered",
    "fixed_stable_unstable_deflation_after_event_projection_registered",
    "all_six_projected_hessian_block_definitions_registered",
    "selected_event_and_first_return_dependencies_separated",
    "scalar_intermediate_stable_flow_certificate_not_logically_required",
    "scalar_K_ret_target_not_logically_required",
    "full_intermediate_correlated_kernel_coverage_still_required",
    "arbitrary_C_history_C2_translation_gate_registered",
    "near_two_period_smoothing_route_registered",
    "minimum_sufficient_condition_ledger_registered",
    "center_kernel_pilot_next_task_registered",
    "all_upstream_and_downstream_claim_boundaries_preserved",
)

FALSE_FLAGS = (
    "compatible_c2_solution_history_domain_validated",
    "moving_time_return_c2_on_full_arbitrary_C_ball_validated",
    "nonlinear_flow_family_on_enlarged_ball_validated",
    "common_selected_event_window_validated",
    "uniform_event_speed_denominator_validated",
    "unique_selected_event_branch_validated",
    "complete_returned_history_tube_validated",
    "complete_intermediate_first_variation_kernel_validated",
    "complete_second_variation_source_kernel_validated",
    "direct_event_aligned_correlated_bilinear_kernel_validated",
    "stable_output_ss_block_validated",
    "stable_output_su_block_validated",
    "stable_output_uu_block_validated",
    "unstable_output_ss_block_validated",
    "unstable_output_su_block_validated",
    "unstable_output_uu_block_validated",
    "all_six_projected_return_hessian_blocks_validated",
    "all_six_blocks_strictly_below_stage4m_caps_validated",
    "selected_return_map_on_full_anisotropic_ball_validated",
    "no_earlier_admissible_positive_return_validated",
    "first_positive_local_return_validated",
    "quantitative_inner_stable_graph_validated",
    "selected_pulse_stable_sheet_crossing_validated",
    "unique_physical_pulse_onset_validated",
    "two_sided_basin_routing_validated",
    "outer_or_quiet_capture_from_both_sides_validated",
    "frequency_amplitude_safety_radius_validated",
    "asynchronous_network_safety_radius_validated",
)


@dataclass(frozen=True)
class Stage4OContract:
    schema_id: str
    model_id: str
    branch: str
    status: str
    parent_result_sha256: dict[str, str]
    exact_model_and_phase_space: dict[str, Any]
    regularity_audit: dict[str, Any]
    near_two_period_smoothing_route: dict[str, Any]
    fixed_time_flow_jet: dict[str, Any]
    implicit_event_time_jet: dict[str, Any]
    terminal_history_and_phase_projection: dict[str, Any]
    projected_six_block_definition: dict[str, Any]
    direct_correlated_kernel_route: dict[str, Any]
    minimum_sufficient_conditions: dict[str, Any]
    selected_versus_first_return_logic: dict[str, Any]
    intermediate_stable_flow_audit: dict[str, Any]
    dependency_graph: dict[str, Any]
    next_numeric_task: dict[str, Any]
    strict_numeric_ingress: dict[str, Any]
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


def _load_parents(repository: Path) -> dict[str, Mapping[str, Any]]:
    validators = {
        STAGE4I_RESULT_RELATIVE_PATH: lambda payload: validate_stage4i_result(
            payload, repository
        ),
        STAGE4L_RESULT_RELATIVE_PATH: lambda payload: validate_stage4l_result(
            payload, repository, recompute=False
        ),
        STAGE4M_RESULT_RELATIVE_PATH: lambda payload: validate_stage4m_result(
            payload, repository, recompute=False
        ),
        STAGE4N_RESULT_RELATIVE_PATH: lambda payload: validate_stage4n_result(
            payload, repository, recompute=False
        ),
        STAGE4N_FEASIBILITY_RESULT_RELATIVE_PATH:
            lambda payload: validate_stage4n_feasibility_result(
                payload, repository, recompute=False
            ),
    }
    parents: dict[str, Mapping[str, Any]] = {}
    for relative, expected_hash in PARENT_RESULT_SHA256.items():
        raw = (repository / relative).read_bytes()
        if sha256(raw).hexdigest() != expected_hash:
            raise ValueError(f"the bound parent changed: {relative}")
        payload = json.loads(raw)
        validators[relative](payload)
        parents[relative] = _mapping(payload, relative)
    return parents


def _parent_semantic_ingress(
    parents: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    if MODEL_EQUATION != EXACT_MODEL_EQUATION:
        raise ValueError("the exact leaky model equation changed")

    stage4i = _mapping(
        parents[STAGE4I_RESULT_RELATIVE_PATH].get("artifact"),
        "Stage-4I artifact",
    )
    grid = _mapping(stage4i.get("guide_and_grid"), "Stage-4I grid")
    if grid.get("primitive_fields") != ["F", "G", "C0", "C1", "C00"]:
        raise ValueError("the Stage-4I exact word skeleton changed")

    stage4l = _mapping(
        parents[STAGE4L_RESULT_RELATIVE_PATH].get("artifact"),
        "Stage-4L artifact",
    )
    support = _mapping(
        stage4l.get("true_period_and_word_support"),
        "Stage-4L period support",
    )
    if (
        support.get("T_minus_tau_max_strictly_positive") is not True
        or support.get("T_strictly_less_than_tau0_plus_tau1") is not True
        or support.get("complete_true_returned_history_covered") is not True
        or support.get("exact_active_words")
        != ["empty", "(0)", "(1)", "(0,0)"]
    ):
        raise ValueError("the Stage-4L terminal support geometry changed")

    stage4m = _mapping(
        parents[STAGE4M_RESULT_RELATIVE_PATH].get("contract"),
        "Stage-4M contract",
    )
    domain = _mapping(stage4m.get("anisotropic_domain"), "Stage-4M domain")
    blocks = _mapping(
        stage4m.get("six_block_certificate_interface"),
        "Stage-4M block interface",
    )
    cap_ledger = _mapping(
        stage4m.get("common_cap_ledger"), "Stage-4M cap ledger"
    )
    cap_records = cap_ledger.get("records")
    if (
        domain.get("stable_radius_R_s") != "0.0097"
        or domain.get("unit_unstable_radius_R_u_hat") != "0.00025"
        or domain.get("split_radius_sum_exact") != "0.00995"
        or not isinstance(cap_records, list)
        or [record.get("block") for record in cap_records]
        != list(HESSIAN_FIELD_NAMES)
        or blocks.get("mixed_slot_symmetry")
        != "D2P[h_s,q_hat]=D2P[q_hat,h_s]"
    ):
        raise ValueError("the Stage-4M domain or six-block interface changed")

    stage4n = _mapping(
        parents[STAGE4N_RESULT_RELATIVE_PATH].get("contract"),
        "Stage-4N contract",
    )
    selected = _mapping(
        stage4n.get("selected_return_definition"),
        "Stage-4N selected-return definition",
    )
    if selected.get("selected_does_not_mean_first_until_cover_closes") is not True:
        raise ValueError("the Stage-4N selected/first-return boundary changed")

    feasibility = _mapping(
        parents[STAGE4N_FEASIBILITY_RESULT_RELATIVE_PATH].get("pilot"),
        "Stage-4N feasibility pilot",
    )
    kernel = _mapping(
        feasibility.get("signed_mild_flow_kernel_interface"),
        "Stage-4N signed-kernel interface",
    )
    target = _mapping(
        feasibility.get("conditional_terminal_kernel_target"),
        "Stage-4N conditional kernel target",
    )
    if (
        kernel.get("stage4i_four_words_supply_algebraic_skeleton") is not True
        or kernel.get("stage4i_primitives_supply_this_kernel_bound") is not False
        or kernel.get("stage4l_terminal_row_supplies_this_intermediate_bound")
        is not False
        or target.get("actual_signed_event_aligned_kernel_upper") is not None
        or target.get("target_is_conditional_design_arithmetic_only") is not True
    ):
        raise ValueError("the Stage-4N kernel claim boundary changed")

    with localcontext() as context:
        context.prec = 100
        period_lower = Decimal(str(support["true_period_lower"]))
        period_upper = Decimal(str(support["true_period_upper"]))
        tau_max_lower = Decimal(str(support["tau1_lower"]))
        tau_max_upper = Decimal(str(support["tau1_upper"]))
        one_period_smoothing_deficit_lower = (
            Decimal(2) * tau_max_lower - period_upper
        )
        two_period_smoothing_margin_lower = (
            Decimal(2) * period_lower - Decimal(2) * tau_max_upper
        )
    if (
        one_period_smoothing_deficit_lower <= 0
        or two_period_smoothing_margin_lower <= 0
    ):
        raise ValueError("the centre one/two-period smoothing geometry changed")

    return {
        "stage4i_exact_center_words": list(grid["primitive_fields"]),
        "stage4l_exact_active_words": list(support["exact_active_words"]),
        "center_true_period_lower": support["true_period_lower"],
        "center_true_period_upper": support["true_period_upper"],
        "center_tau0_lower": support["tau0_lower"],
        "center_tau1_lower": support["tau1_lower"],
        "center_T_minus_tau_max_lower": support[
            "directed_margin_lower"
        ]["T_minus_tau_max_lower"],
        "center_tau0_plus_tau1_minus_T_upper_end_lower": support[
            "directed_margin_lower"
        ]["tau0_plus_tau1_minus_T_upper_end_lower"],
        "center_one_period_2tau_max_minus_T_lower": format(
            one_period_smoothing_deficit_lower, "f"
        ),
        "center_two_period_T2_minus_2tau_max_lower": format(
            two_period_smoothing_margin_lower, "f"
        ),
        "stable_radius_R_s": domain["stable_radius_R_s"],
        "unit_unstable_radius_R_u_hat": domain[
            "unit_unstable_radius_R_u_hat"
        ],
        "split_radius_sum": domain["split_radius_sum_exact"],
        "stage4m_strict_caps": {
            record["block"]: record["strict_cap_decimal_exact"]
            for record in cap_records
        },
        "conditional_K_ret_target_lower": target[
            "strict_kernel_target_lower"
        ],
        "conditional_K_ret_target_is_theorem_ingress": False,
    }


def _numeric_core(contract: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "regularity_audit": contract["regularity_audit"],
        "minimum_sufficient_conditions": contract[
            "minimum_sufficient_conditions"
        ],
        "intermediate_stable_flow_audit": contract[
            "intermediate_stable_flow_audit"
        ],
        "strict_numeric_ingress": contract["strict_numeric_ingress"],
        "claim_status": contract["claim_status"],
    }


def _runtime_record() -> dict[str, str]:
    return {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "arithmetic": (
            "formal identities and exact JSON/SHA-256 binding only; every "
            "numeric theorem ingress is null or false"
        ),
    }


def build_stage4o_contract(repository: Path) -> Stage4OContract:
    repository = repository.resolve()
    parents = _load_parents(repository)
    ingress = _parent_semantic_ingress(parents)
    claims = {name: True for name in TRUE_FLAGS}
    claims.update({name: False for name in FALSE_FLAGS})

    return Stage4OContract(
        schema_id=SCHEMA_ID,
        model_id=MODEL_ID,
        branch=BRANCH,
        status=STATUS,
        parent_result_sha256=dict(PARENT_RESULT_SHA256),
        exact_model_and_phase_space={
            "reduced_history_space": (
                "Y=C([-tau_max,0],R)_v x R_w with the inherited max norm"
            ),
            "state_at_time_t": (
                "S_t(x)=(theta -> v_x(t+theta), w_x(t))"
            ),
            "section_tangent_space": "Sigma_0={h in Y:h_v(0)=0}",
            "model_equation": EXACT_MODEL_EQUATION,
            "field_fast": (
                "F_v(phi,w)=phi(0)-phi(0)^3/3-w+epsilon*kappa_1*"
                "((phi(-tau0)+phi(-tau1))/2-phi(0))+epsilon*kappa_3*"
                "(((phi(-tau0)-1)^3+(phi(-tau1)-1)^3)/2-"
                "(phi(0)-1)^3)"
            ),
            "field_slow": "F_w(phi,w)=epsilon*(phi(0)-a-w)",
            "D1_fast": (
                "[1-v0^2-epsilon*kappa_1-3*epsilon*kappa_3*(v0-1)^2]"
                "*h_v(0)-h_w+sum_j epsilon/2*[kappa_1+"
                "3*kappa_3*(v_j-1)^2]*h_v(-tau_j)"
            ),
            "D1_slow": "epsilon*(h_v(0)-h_w)",
            "D2_fast": (
                "c_0(phi)*h_v(0)*k_v(0)+sum_j c_j(phi)*"
                "h_v(-tau_j)*k_v(-tau_j)"
            ),
            "D2_coefficients": {
                "c_0": "-2*v0-6*epsilon*kappa_3*(v0-1)",
                "c_j": "3*epsilon*kappa_3*(v_j-1), j=0,1",
            },
            "D2_slow_and_all_mixed_entries": "zero",
            "D3_coefficients": {
                "current": "-2-6*epsilon*kappa_3",
                "each_delayed_slot": "3*epsilon*kappa_3",
                "mixed_and_slow": "zero",
            },
            "physical_time_only": True,
            "parent_semantic_ingress": ingress,
        },
        regularity_audit={
            "declared_stage4m_domain": (
                "all x=X_*+x_s+q_hat*x_u with ||x_s||_Y<=0.0097, "
                "|x_u|<=0.00025 and arbitrary continuous stable histories"
            ),
            "moving_return_history": (
                "theta -> v_x(T(x)+theta), -tau_max<=theta<=0"
            ),
            "second_translation_term": (
                "ddot v_x(T(x)+theta)*T_h*T_k"
            ),
            "center_support_facts": (
                "Stage 4L proves T-tau_max>0, while directed arithmetic gives "
                "T<2*tau_max; the stronger concrete witness "
                "T<tau0+tau1 exposes a negative delayed slot"
            ),
            "unresolved_early_history_mechanism": (
                "at theta=-tau1, differentiating dot v at T-tau1 reads "
                "the tau0 slot at T-tau1-tau0<0; an arbitrary C history "
                "has no controlled derivative there"
            ),
            "linear_no_identity_fact_does_not_supply_C2": True,
            "naive_eventual_smoothing_on_one_return_is_sufficient": False,
            "full_arbitrary_C_ball_C2_conclusion_permitted": False,
            "minimum_repair_alternatives": (
                "validate a compatible C1 solution-history manifold and its "
                "tangent splitting in a translation-controlling norm; or use "
                "a later return whose whole history lies beyond the needed "
                "smoothing time; or prove an equivalent fixed-phase return "
                "formulation with a quadratic remainder that avoids the "
                "unsupported moving-translation derivative"
            ),
            "repair_validated_here": False,
        },
        near_two_period_smoothing_route={
            "exact_smoothing_threshold": (
                "T_2-tau_max>tau_max, equivalently T_2>2*tau_max; this "
                "places every returned-history time beyond the C2 time-"
                "smoothing threshold needed by ddot X_T"
            ),
            "one_period_center_fails_threshold": True,
            "center_one_period_2tau_max_minus_T_lower": ingress[
                "center_one_period_2tau_max_minus_T_lower"
            ],
            "two_period_center_passes_threshold": True,
            "center_two_period_T2_minus_2tau_max_lower": ingress[
                "center_two_period_T2_minus_2tau_max_lower"
            ],
            "nonlinear_common_T2_gate": (
                "a future common selected second-event window must prove "
                "T2_minus>2*tau_max on the full anisotropic ball"
            ),
            "composition_identity_gate": (
                "sufficient algebraic route: use nested domains D0,D1 with P "
                "defined on both, P(D0) subset D1, and prove Q=P o P on D0, "
                "including equality of the direct second-event time with "
                "T_1(x)+T_1(P(x)); no invariant full saddle neighborhood is "
                "required"
            ),
            "same_stable_set_reason": (
                "if Q=P^2, convergence of even iterates plus continuity of P "
                "gives convergence of odd iterates, hence W^s(Q)=W^s(P); "
                "local graph uniqueness then gives the same stable sheet germ"
            ),
            "same_semiflow_transfer_alternative": (
                "Q=P^2 is not necessary for the intrinsic sheet: if Q is the "
                "unique near-2P section return of the same semiflow, its event "
                "times stay uniformly positive and bounded, and Q-iterate "
                "convergence is proved equivalent to convergence to the "
                "periodic orbit through the intervening flow arcs, then Q "
                "constructs the same stable-set germ"
            ),
            "direct_second_event_requires_same_semiflow_stable_set_identification": True,
            "Q_equals_P2_needed_only_for_one_period_branch_identity": True,
            "one_step_stage4m_caps_reusable_without_recalibration": False,
            "required_recalibration": (
                "use DQ=A^2, squared stable and inverse-unstable rates, and "
                "six Q-specific projected Hessian caps in one new majorant"
            ),
            "no_earlier_hit_needed_for_Q_stable_graph": False,
            "no_earlier_hit_needed_for_physical_first_return_label": True,
            "nonlinear_two_period_branch_validated_here": False,
        },
        fixed_time_flow_jet={
            "base": "dot X(t;x)=F(X_t(x)), X_0(x)=x",
            "first_variation": (
                "dot U_h(t)=DF(X_t)U_{h,t}, U_{h,v}(theta)=h_v(theta) "
                "for theta<=0 and U_{h,w}(0)=h_w"
            ),
            "second_variation": (
                "dot V_hk(t)=DF(X_t)V_{hk,t}+"
                "D2F(X_t)[U_{h,t},U_{k,t}], V_hk,0=0"
            ),
            "fast_quadratic_source": (
                "b_hk(t)=c_0(t)u_h(t)u_k(t)+sum_j c_j(t)*"
                "u_h(t-tau_j)u_k(t-tau_j)"
            ),
            "slow_quadratic_source": "zero",
            "mild_second_variation": (
                "V_hk(r)=integral_0^r U_x(r,s)e_v*b_hk(s) ds, with the "
                "retarded propagator set to zero for s>r"
            ),
            "affine_initial_history_injection": True,
            "initial_second_jet": "D2[x -> x][h,k]=0",
            "symmetry": "V_hk=V_kh",
            "required_input_sectors": ["ss", "su", "uu"],
            "formula_is_conditional_on_regular_flow_domain": True,
            "numeric_enclosure_supplied_here": False,
        },
        implicit_event_time_jet={
            "event_function": (
                "G(t,x)=g(S_t(x))=v_x(t)-X_{*,v}(0)"
            ),
            "affine_event_row": "ell_0(y)=y_v(0)",
            "event_speed": "a(x)=partial_t G(T(x),x)=dot v_x(T(x))",
            "denominator_gate": "a(x)>=a_*>0 on one common event window",
            "first_numerator": "n_h=ell_0(U_h^T)=u_{h,v}(T)",
            "first_derivative": "T_h=-n_h/a",
            "preprojection_second_core": (
                "Z_hk=V_hk^T-(dot U_h^T*n_k+dot U_k^T*n_h)/a+"
                "ddot X_T*n_h*n_k/a^2"
            ),
            "equivalent_W_formula": (
                "W_hk=V_hk^T+dot U_h^T*T_k+dot U_k^T*T_h+"
                "ddot X_T*T_h*T_k"
            ),
            "second_derivative": "T_hk=-ell_0(Z_hk)/a",
            "largest_explicit_inverse_power_after_phase_projection": "a^-3",
            "same_correlated_denominator_required": True,
            "symmetry": "T_hk=T_kh",
            "numeric_denominator_supplied_here": False,
        },
        terminal_history_and_phase_projection={
            "terminal_lift": (
                "Y_h^T=(theta -> y_{h,v}(T+theta), y_{h,w}(T))"
            ),
            "terminal_velocity_history": (
                "dot X_T=(theta -> dot v(T+theta), dot w(T))"
            ),
            "terminal_acceleration_history": (
                "ddot X_T=(theta -> ddot v(T+theta), ddot w(T))"
            ),
            "moving_event_phase_projection": (
                "Pi_x Y=Y-dot X_T*ell_0(Y)/a(x)"
            ),
            "first_return_derivative": "DP(x)h=Pi_x U_h^T",
            "second_return_derivative": "D2P(x)[h,k]=Pi_x Z_hk",
            "expanded_second_return": (
                "D2P(theta)=W_hk(theta)+dot X(T+theta)*T_hk"
            ),
            "history_coordinate_range": "every theta in [-tau_max,0]",
            "recovery_coordinate_rule": (
                "evaluate U,V,dot U,dot X,ddot X at theta=0/current T"
            ),
            "event_projection_application_count": 1,
            "section_tangency_checks": [
                "ell_0(DP(x)h)=0",
                "ell_0(D2P(x)[h,k])=0",
            ],
            "endpoint_only_translation_sufficient": False,
            "numeric_history_jet_supplied_here": False,
        },
        projected_six_block_definition={
            "fixed_unit_pair": (
                "q_hat=q/||q||_Y, f_hat=||q||_Y*f, f_hat(q_hat)=1"
            ),
            "fixed_stable_projection": "P_s=I-q_hat*f_hat",
            "input_injections": {
                "stable": "I_s h=h for h in E_s=ker(f_hat)",
                "unstable": "I_u c=q_hat*c",
            },
            "event_aligned_bilinear_map": (
                "H_ab(x)=Pi_x Z_{I_a,I_b}, a,b in {s,u}"
            ),
            "stable_outputs": {
                "stable_output_ss": "P_s H_ss",
                "stable_output_su": "P_s H_su=P_s H_us",
                "stable_output_uu": "P_s H_uu",
            },
            "unstable_outputs": {
                "unstable_output_ss": "f_hat(H_ss)",
                "unstable_output_su": "f_hat(H_su)=f_hat(H_us)",
                "unstable_output_uu": "f_hat(H_uu)",
            },
            "operator_norms": (
                "take sup over the full base domain and unit stable inputs; "
                "the unstable input is the fixed q_hat"
            ),
            "correct_order": (
                "fixed-time source -> event quotient -> complete-history "
                "Pi_x -> fixed P_s or f_hat -> one final norm"
            ),
            "moving_event_projection_is_not_stable_deflation": True,
            "fixed_stable_projection_over_base_ball": True,
            "separately_normed_rank_one_terms_forbidden": True,
            "numeric_blocks_supplied_here": {
                name: None for name in HESSIAN_FIELD_NAMES
            },
        },
        direct_correlated_kernel_route={
            "first_variation_rows": (
                "L_{x,m}(s):h -> u_{h,v}(s-tau_m), with tau_current=0"
            ),
            "quadratic_source_kernel": (
                "sum_m c_m(x,s)*L_{x,m}(s) tensor L_{x,m}(s)"
            ),
            "second_variation_terminal_kernel": (
                "integrate the retarded terminal row U_x(T+theta,s)e_v "
                "against the quadratic source kernel before modulus"
            ),
            "event_terms": (
                "retain n_h,n_k,a,dot U_h,dot U_k,ddot X and the terminal "
                "phase row in the same signed atom-density-bimeasure object"
            ),
            "output_terms": (
                "apply P_s or f_hat to that common event-aligned object "
                "before total variation/operator norm"
            ),
            "complete_variables": (
                "base shard x, source time s, output phase theta, both input "
                "history coordinates, current atoms, delay activations and "
                "all time/history seams"
            ),
            "stage4i_role": (
                "F,G,C0,C1,C00 supply the exact center four-word algebraic "
                "skeleton, not the nonlinear uniform kernel bound"
            ),
            "stage4l_role": (
                "the center terminal linear row fixes normalization and a "
                "terminal check, but supplies no intermediate quadratic source"
            ),
            "nonlinear_uniformity_role": (
                "D3F and one base-tube enclosure control coefficient and "
                "first/second-kernel perturbations across the ball"
            ),
            "kernel_validated_here": False,
        },
        minimum_sufficient_conditions={
            "A_regular_domain": (
                "one declared Banach domain on which the full returned-history "
                "moving translation is C2; its tangent stable/unstable split "
                "and norm must be source-bound"
            ),
            "B_nonlinear_base_cover": (
                "one continuous complete-history flow tube for every base "
                "point, all source times, all delayed slots and every seam"
            ),
            "C_selected_event_branch": (
                "one selected-event branch with common T_minus,T_plus, strict "
                "endpoint gap signs, a common positive speed lower a_*, and "
                "returned local-patch containment"
            ),
            "D_first_variation_kernels": (
                "continuous signed current/delayed evaluation rows for stable "
                "inputs and q_hat on every intermediate source time"
            ),
            "E_second_variation_kernels": (
                "the ss,su,uu quadratic source and retarded terminal response "
                "on every output phase, with D3F perturbation remainder"
            ),
            "F_event_quotients": (
                "correlated enclosures of a,n_s,n_u,dot U,ddot X,Z and ell_0 Z "
                "using the same positive denominator enclosure"
            ),
            "G_terminal_and_output_cover": (
                "complete theta range, recovery current, q_hat/f_hat tails, "
                "one Pi_x application, then correlated P_s/f_hat output"
            ),
            "H_six_cap_tests": (
                "all six uniform upper bounds arise from one run and each is "
                "strictly below its corresponding Stage-4M cap"
            ),
            "I_first_return_only": (
                "launch collar plus disjunctive no-earlier admissible-return "
                "cover; not required merely to define selected-branch Hessians"
            ),
            "finite_base_or_time_sampling_sufficient": False,
            "standalone_terminal_linear_row_sufficient": False,
        },
        selected_versus_first_return_logic={
            "selected_hessian_minimum": (
                "A through H give the six Hessian blocks of one unique C2 "
                "selected local event branch"
            ),
            "no_earlier_hit_needed_for_selected_hessian": False,
            "first_physical_local_return_upgrade": (
                "add I and prove there is no earlier positive-oriented zero "
                "inside the declared local complete-history patch"
            ),
            "negative_oriented_earlier_crossings_allowed": True,
            "global_one_sign_event_gap_required": False,
            "no_earlier_hit_validated_here": False,
        },
        intermediate_stable_flow_audit={
            "standalone_quantity": (
                "M_s=sup_{x,t} ||U_x(t,0)P_s|| as a separately normed scalar"
            ),
            "standalone_scalar_is_logically_necessary": False,
            "why_bypass_is_exact": (
                "the final bilinear operator can be assembled by substituting "
                "the signed first-variation rows directly into D2F and "
                "integrating only after event/output correlations are formed"
            ),
            "what_cannot_be_avoided": (
                "validated intermediate-time first-variation row kernels in "
                "every current and delayed slot used by the quadratic source"
            ),
            "stage4l_terminal_row_can_replace_intermediate_rows": False,
            "stage4i_center_words_alone_close_nonlinear_uniformity": False,
            "conditional_scalar_K_ret_target_is_logically_necessary": False,
            "why_K_ret_can_be_bypassed": (
                "a split-correlated return-domain and six-block majorant may "
                "close componentwise even when a cancellation-blind ambient "
                "Hessian row exceeds the old scalar complete-return target"
            ),
            "recommended_norm_order": (
                "retain signs and shared denominators through source integration, "
                "event phase projection and fixed output deflation; norm once"
            ),
        },
        dependency_graph={
            "formal_spine": [
                "exact model D1/D2/D3",
                "fixed-time U and V",
                "selected event T_x and T_xx",
                "complete terminal history",
                "one moving phase projection",
                "fixed P_s/f_hat outputs",
                "six operator suprema",
            ],
            "numeric_branch": [
                "regular C2 history domain",
                "preferably a common selected near-two-period event with "
                "T2_minus>2*tau_max",
                "nonlinear base/event cover and Q=P^2 compatibility",
                "correlated first/second kernels",
                "six strict Q-specific cap tests and a recalibrated majorant",
            ],
            "optional_first_return_branch": [
                "launch collar",
                "middle no-earlier disjunctive cover",
                "first positive local return semantics",
            ],
            "downstream_only_after_all_six_caps": [
                "common Stage-4K majorant",
                "quantitative stable graph",
                "graph-adjusted pulse gap",
                "selected crossing",
                "physical onset/routing/capture/safety",
            ],
        },
        next_numeric_task={
            "name": (
                "Stage-4P near-two-period event-aligned signed bilinear-kernel "
                "pilot"
            ),
            "domain": (
                "first the validated smooth center periodic history at T2=2P; "
                "then the full ball only after a common T2 window and smoothing "
                "gate are source-bound"
            ),
            "inputs": (
                "Stage-4I F,G,C0,C1,C00; Stage-4L fixed q_hat/f_hat and "
                "terminal phase row; exact model D2 coefficients; extend the "
                "method-of-steps word/kernel cover through 2P"
            ),
            "calculation": (
                "assemble ss,su,uu direct two-period Z kernels over every "
                "source cell and "
                "theta cell; apply Pi_* once and then P_s/f_hat before directed "
                "atom-density-bimeasure norms"
            ),
            "outputs": (
                "six center Q-block uppers, dominant source/output cells, "
                "denominator contribution ledger, Q-specific strict caps, "
                "squared-rate majorant and residual headroom"
            ),
            "continuous_coverage": (
                "all source times, both input history variables, every output "
                "theta, delay activations, short final cell and seams"
            ),
            "forbidden_shortcut": (
                "do not first replace stable first-variation rows by one "
                "sup_t operator norm and do not infer a nonlinear-ball theorem"
            ),
            "conditional_complete_return_target": ingress[
                "conditional_K_ret_target_lower"
            ],
            "target_is_design_arithmetic_only": True,
            "unbound_finite_section_hint": {
                "Q_blocks": [
                    "4.27e-8",
                    "5.20e-7",
                    "30.2781",
                    "0.59394",
                    "0.56667",
                    "158.5393",
                ],
                "conservative_caps": ["1e-6", "1e-5", "35", "0.7", "0.7", "180"],
                "squared_rate_majorant_perron": "0.02356",
                "graph_height": "1.743e-5",
                "Dpsi": "0.003086",
                "ambient_H2_row_sum": "approximately 337",
                "evidence_status": (
                    "HEURISTIC_FINITE_SECTION_ONLY; no value enters a theorem"
                ),
            },
            "must_resolve_before_uniform_theorem": (
                "the common selected T2 branch with T2_minus>2*tau_max, "
                "Q=P^2/local-sheet compatibility, and the nonlinear base/kernel "
                "perturbation cover"
            ),
            "pilot_result_exists": False,
        },
        strict_numeric_ingress={
            "regular_history_domain_result": None,
            "regular_history_domain_result_sha256": None,
            "T_minus": None,
            "T_plus": None,
            "left_event_gap_margin": None,
            "right_event_gap_margin": None,
            "event_speed_lower_a_star": None,
            "event_speed_upper": None,
            "nonlinear_base_history_tube_upper": None,
            "returned_history_tube_upper": None,
            "history_translation_C2_modulus_upper": None,
            "stable_first_variation_kernel_upper": None,
            "unstable_first_variation_kernel_upper": None,
            "ss_second_variation_kernel_upper": None,
            "su_second_variation_kernel_upper": None,
            "uu_second_variation_kernel_upper": None,
            "event_quotient_remainder_upper": None,
            "q_hat_f_hat_tail_and_normalization_upper": None,
            "direct_event_aligned_kernel_upper": None,
            "directed_uniform_hessian_blocks": {
                name: None for name in HESSIAN_FIELD_NAMES
            },
            "all_delay_activation_and_history_seams_covered": False,
            "all_output_phase_cells_covered": False,
            "all_six_blocks_from_one_correlated_run": False,
            "all_six_strict_cap_tests_pass": False,
            "no_earlier_hit_cover_complete": False,
            "evidence_status": "OPEN_FORMAL_ONLY",
        },
        theorem_boundary={
            "proved_here": (
                "only the exact conditional chain-rule identities, the six-block "
                "dependency split, the direct-kernel proof interface, and the "
                "source-bound diagnosis of the unresolved moving-translation "
                "regularity gate"
            ),
            "not_proved_here": (
                "C2 regularity on the arbitrary-C ball, a nonlinear flow/event "
                "tube, selected or first return, any kernel or Hessian bound, "
                "stable graph, crossing, onset, routing, capture, or safety"
            ),
            "generic_majorant_failures_mean_theorem_failure": False,
            "stage4i_or_stage4l_substitutes_for_uniform_nonlinear_kernel": False,
            "flagship_files_modified": False,
        },
        claim_status=claims,
    )


def build_stage4o_result(repository: Path) -> dict[str, Any]:
    repository = repository.resolve()
    contract = asdict(build_stage4o_contract(repository))
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


def validate_stage4o_result(
    payload: Mapping[str, Any],
    repository: Path,
    *,
    recompute: bool = False,
) -> None:
    if not isinstance(payload, Mapping) or set(payload) != TOP_KEYS:
        raise ValueError("the Stage-4O result has the wrong outer schema")
    contract = _mapping(payload.get("contract"), "Stage-4O contract")
    manifest = _mapping(payload.get("manifest"), "Stage-4O manifest")
    if set(contract) != {field.name for field in fields(Stage4OContract)}:
        raise ValueError("the Stage-4O contract schema changed")
    if set(manifest) != MANIFEST_KEYS:
        raise ValueError("the Stage-4O manifest schema changed")

    repository = repository.resolve()
    expected_contract = asdict(build_stage4o_contract(repository))
    if dict(contract) != expected_contract:
        raise ValueError("the Stage-4O analytic contract changed")

    claims = _mapping(contract.get("claim_status"), "Stage-4O claims")
    if set(claims) != set(TRUE_FLAGS) | set(FALSE_FLAGS):
        raise ValueError("the Stage-4O claim ledger changed")
    if any(claims.get(name) is not True for name in TRUE_FLAGS):
        raise ValueError("a formal Stage-4O fact was weakened")
    if any(claims.get(name) is not False for name in FALSE_FLAGS):
        raise ValueError("an open Stage-4O theorem gate was promoted")

    numeric = _mapping(
        contract.get("strict_numeric_ingress"),
        "Stage-4O strict numeric ingress",
    )
    for key, value in numeric.items():
        if key == "directed_uniform_hessian_blocks":
            blocks = _mapping(value, "Stage-4O open Hessian blocks")
            if set(blocks) != set(HESSIAN_FIELD_NAMES) or any(
                item is not None for item in blocks.values()
            ):
                raise ValueError("a Stage-4O Hessian block was filled")
        elif key in {
            "all_delay_activation_and_history_seams_covered",
            "all_output_phase_cells_covered",
            "all_six_blocks_from_one_correlated_run",
            "all_six_strict_cap_tests_pass",
            "no_earlier_hit_cover_complete",
        }:
            if value is not False:
                raise ValueError("an open Stage-4O coverage gate was promoted")
        elif key == "evidence_status":
            if value != "OPEN_FORMAL_ONLY":
                raise ValueError("the Stage-4O evidence status changed")
        elif value is not None:
            raise ValueError(f"a Stage-4O numeric ingress was filled: {key}")

    expected_manifest = {
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
    }
    if dict(manifest) != expected_manifest:
        raise ValueError("the Stage-4O manifest or source binding changed")

    if recompute and dict(payload) != build_stage4o_result(repository):
        raise ValueError("the Stage-4O fresh replay changed")


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
    "Stage4OContract",
    "TEST_RELATIVE_PATH",
    "TOP_KEYS",
    "TRUE_FLAGS",
    "_numeric_core",
    "build_stage4o_contract",
    "build_stage4o_result",
    "canonical_sha256",
    "validate_stage4o_result",
]
