"""Stage-4S-C fixed-splitting bridge for a selected two-return map.

This artifact separates three logically different levels.

1.  A purely algebraic theorem starts from a bounded section operator ``A``,
    a right vector ``q``, and a left functional ``f`` satisfying

        A q = mu q,   f A = mu f,   f(q) = 1.

    It proves the fixed splitting for ``B=A^2``, all associated
    intertwining identities, the squared stable rate, and (when ``mu`` is
    nonzero) the scalar unstable inverse/backward rate.
2.  A conditional nonlinear bridge says exactly what is needed before one
    may write a selected two-return map as ``Q=P^2`` and infer
    ``DQ(p)=A^2``.  The nested composition domain is explicit.
3.  A conditional same-semiflow bridge imports the Stage-4R stable-set-germ
    lemma.  ``Q=P^2`` is sufficient but not necessary there, and it never
    replaces the common intervening tube, bounded positive return times,
    invariant return domain, fixed-point/period, or isolated-section
    hypotheses.

The model-specific linear instance is source-bound to Stage 4L and the
proved one-return unstable multiplier bound.  No nonlinear selected return,
composition domain, repeated-hit tube, first-return property, stable graph,
or periodic-orbit stable-set germ is promoted.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from decimal import Decimal, localcontext
from hashlib import sha256
import json
import os
from pathlib import Path
import platform
from typing import Any, Mapping

from canard_control.finite_delay_eventually_smooth_selected_return_stage4r import (
    validate_stage4r_result,
)
from canard_control.leaky_inner_stable_manifold_stage1_contract import (
    validate_stage1_stable_manifold_result,
)
from canard_control.leaky_inner_terminal_stable_row_stage4l import (
    validate_stage4l_result,
)


SCHEMA_ID = "leaky-inner-two-return-stage4s-split-bridge-v1"
MODEL_ID = "autonomous-leaky-recovery-two-delay-fhn-bistable-proposal"
BRANCH = "inner_saddle_candidate"
STATUS = "PROVED_LINEAR_SPLIT_WITH_CONDITIONAL_NONLINEAR_BRIDGE"

SOURCE_RELATIVE_PATH = (
    "src/canard_control/leaky_inner_two_return_stage4s_split_bridge.py"
)
GENERATOR_RELATIVE_PATH = (
    "experiments/leaky_inner_two_return_stage4s_split_bridge.py"
)
RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_inner_two_return_stage4s_split_bridge.json"
)
NOTE_RELATIVE_PATH = "docs/leaky_inner_two_return_stage4s_split_bridge.md"
TEST_RELATIVE_PATH = (
    "tests/test_leaky_inner_two_return_stage4s_split_bridge.py"
)

STAGE4L_RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_inner_terminal_stable_row_stage4l.json"
)
STAGE4R_RESULT_RELATIVE_PATH = (
    "experiments/results/finite_delay_eventually_smooth_selected_return_stage4r.json"
)
STAGE1_RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_inner_stable_manifold_stage1_contract.json"
)

PARENT_RESULT_SHA256 = {
    STAGE4L_RESULT_RELATIVE_PATH: (
        "672f92c7c456a54f39afab7d2a5f92b783311cc0ee5341a4d2e72a588039017e"
    ),
    STAGE4R_RESULT_RELATIVE_PATH: (
        "4e68835bc3ba5fd44432d98a3b6b1d41506533d66f3353cd500df3e95da76418"
    ),
    STAGE1_RESULT_RELATIVE_PATH: (
        "3c400ec92f00d4c94313b6e0a5b514f60f21335f54cba41ad5ba8a4217e8f21b"
    ),
}

STABLE_RATE_ONE = "0.1"
STABLE_RATE_TWO = "0.01"
STABLE_ONE_STEP_UPPER = (
    "0.00989642748161000022244199598343033161524171712346077110775160712"
)
STABLE_TWO_STEP_UPPER = (
    "0.0000979392768987656512909542642292023934722690772595215680701268436"
    "008663590088133855053307238038569905570840746589878769428346944"
)
UNSTABLE_MULTIPLIER_MODULUS_LOWER = (
    "1.81913372574167842375644213779457264168445028000790971"
)
UNSTABLE_MULTIPLIER_MODULUS_UPPER = (
    "2.22189495008307196905747671092766936323792280049007467"
)
UNSTABLE_BACKWARD_RATE_ONE = (
    "0.549712198641301272665939640423769383243380071590152304446016306796"
    "024304322569720837972565017934"
)
UNSTABLE_BACKWARD_RATE_TWO = (
    "0.302183501335053468766049321268313699617093109911449469063818668425"
    "607982682870864983343314167041012216402531488839876224555070910009"
    "877958313689944253533344086871769103550439695624961741628356"
)

SOURCE_MANIFEST = (
    SOURCE_RELATIVE_PATH,
    GENERATOR_RELATIVE_PATH,
    NOTE_RELATIVE_PATH,
    TEST_RELATIVE_PATH,
)

DEFAULT_COMMAND = (
    "OPENBLAS_NUM_THREADS=8 OMP_NUM_THREADS=1 PYTHONPATH=src "
    "/usr/bin/python3 experiments/"
    "leaky_inner_two_return_stage4s_split_bridge.py"
)
ARITHMETIC_SCOPE = (
    "exact parent-byte and semantic validation; symbolic rank-one projector "
    "algebra for B=A^2; exact finite-decimal squaring of already directed "
    "stable and one-dimensional inverse-unstable bounds; conditional Banach-"
    "space chain rule, nested-domain composition, same-semiflow time sum, "
    "and Stage-4R isolated-section stable-set-germ adapter"
)

TOP_KEYS = {"certificate", "manifest"}
MANIFEST_KEYS = {
    "schema_id",
    "result",
    "default_command",
    "arithmetic_scope",
    "artifact_sha256",
    "formal_core_sha256",
    "source_sha256",
    "parent_result_sha256",
    "runtime",
}

TRUE_FLAGS = (
    "parent_bytes_and_semantics_validated",
    "stage4l_exact_eigen_relations_consumed",
    "stage4l_exact_intertwining_consumed",
    "rank_one_ps_and_pu_are_complementary_projections_proved",
    "sigma_equals_es_direct_sum_eu_proved",
    "a_preserves_fixed_es_and_eu_proved",
    "a_commutes_with_fixed_projections_proved",
    "b_equals_a_squared_preserves_same_fixed_splitting_proved",
    "b_intertwining_relations_proved",
    "b_stable_power_bound_is_squared_proved",
    "b_unstable_inverse_power_formula_proved",
    "model_two_step_stable_rate_0p01_with_k_one_proved",
    "model_sharper_two_step_stable_one_step_bound_proved",
    "model_two_step_unstable_backward_rate_squared_proved",
    "nonlinear_q_equals_p_squared_requires_nested_domain_registered",
    "nonlinear_dq_equals_a_squared_chain_rule_registered",
    "even_iterate_convergence_implies_odd_iterate_convergence_conditionally",
    "same_semiflow_composition_time_sum_registered",
    "repeated_selected_hit_requirements_registered",
    "q_equals_p_squared_sufficient_not_necessary_for_stable_germ_registered",
    "direct_q_stage4r_route_registered",
    "common_tube_not_replaced_by_nested_domain_registered",
    "selected_return_and_first_return_separated",
    "fixed_derivative_splitting_not_promoted_to_nonlinear_invariance",
    "proved_conditional_open_ledger_fail_closed",
)

FALSE_FLAGS = (
    "model_nonlinear_one_return_map_validated",
    "model_nonlinear_two_return_map_validated",
    "model_q_equals_p_squared_identity_validated",
    "model_nested_composition_domain_validated",
    "model_one_return_self_map_ball_validated",
    "model_two_return_self_map_ball_validated",
    "model_uniform_positive_return_time_bounds_validated",
    "model_same_semiflow_time_sum_validated",
    "model_common_intervening_flow_tube_validated",
    "model_repeated_selected_hits_validated",
    "model_q_fixed_point_and_theta_p_equals_2p_validated",
    "model_isolated_section_patch_validated",
    "model_no_earlier_section_hit_validated",
    "model_first_positive_return_validated",
    "model_nonlinear_es_or_eu_invariance_validated",
    "model_two_return_c2_hessian_blocks_validated",
    "model_two_return_hyperbolic_stable_graph_validated",
    "model_periodic_orbit_stable_set_germ_validated",
    "model_pulse_graph_crossing_or_onset_validated",
    "model_routing_capture_or_network_safety_validated",
)


@dataclass(frozen=True)
class Stage4SSplitBridgeCertificate:
    schema_id: str
    model_id: str
    branch: str
    status: str
    parent_result_sha256: dict[str, str]
    formal_two_step_split_theorem: dict[str, Any]
    model_linear_instance: dict[str, Any]
    nonlinear_composition_bridge: dict[str, Any]
    nested_domain_stable_set_bridge: dict[str, Any]
    same_semiflow_time_composition: dict[str, Any]
    stage4r_stable_germ_bridge: dict[str, Any]
    common_tube_and_repeated_hit_audit: dict[str, Any]
    proved_conditional_open_ledger: dict[str, Any]
    scope_boundary: dict[str, bool]
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


def _exact_decimal_square(value: str) -> str:
    digits = len(value.replace(".", "").lstrip("+-0"))
    with localcontext() as context:
        context.prec = max(256, 2 * digits + 8)
        return format(Decimal(value) * Decimal(value), "f")


def _runtime_record() -> dict[str, str]:
    return {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "openblas_num_threads": os.environ.get("OPENBLAS_NUM_THREADS", ""),
        "omp_num_threads": os.environ.get("OMP_NUM_THREADS", ""),
        "arithmetic": (
            "symbolic identities plus exact finite-decimal products; no new "
            "floating-point enclosure"
        ),
    }


def _parent_payloads(repository: Path) -> dict[str, Mapping[str, Any]]:
    repository = repository.resolve()
    payloads: dict[str, Mapping[str, Any]] = {}
    for relative, digest in PARENT_RESULT_SHA256.items():
        path = repository / relative
        if _sha256_path(path) != digest:
            raise ValueError(f"the Stage-4S-C parent changed: {relative}")
        payloads[relative] = json.loads(path.read_text(encoding="utf-8"))

    validate_stage4l_result(
        payloads[STAGE4L_RESULT_RELATIVE_PATH],
        repository,
        recompute=False,
    )
    validate_stage4r_result(
        payloads[STAGE4R_RESULT_RELATIVE_PATH],
        repository,
        recompute=False,
    )
    validate_stage1_stable_manifold_result(
        payloads[STAGE1_RESULT_RELATIVE_PATH], repository
    )
    return payloads


def _validate_parent_semantics(
    parents: Mapping[str, Mapping[str, Any]],
) -> None:
    stage4l = _mapping(
        parents[STAGE4L_RESULT_RELATIVE_PATH].get("artifact"),
        "Stage-4L artifact",
    )
    if (
        stage4l.get("model_id") != MODEL_ID
        or stage4l.get("branch") != BRANCH
        or stage4l.get("status") != "PROVED_DISCRETE_LINEAR_INGRESS"
    ):
        raise ValueError("the Stage-4L model identity changed")
    lemma = _mapping(
        stage4l.get("analytic_discrete_lemma"),
        "Stage-4L exact discrete lemma",
    )
    if lemma.get("exact_eigen_relations") != [
        "Aq=mu_u q",
        "fA=mu_u f",
        "f(q)=1",
    ]:
        raise ValueError("the Stage-4L exact eigen relations changed")
    if (
        lemma.get("right_column") != "q=q^Sigma"
        or lemma.get("normalized_left_row") != "f=f_0/f_0(q^Sigma)"
    ):
        raise ValueError("the Stage-4L physical eigendata changed")
    if lemma.get("exact_intertwining_relations") != [
        "AP_s=P_sA=P_sAP_s",
        "AP_s(Sigma_0) subset E_s",
        "A_s=A|_{E_s}",
    ]:
        raise ValueError("the Stage-4L intertwining relations changed")
    if lemma.get("selected_map_is_not_claimed_first_positive_return") is not True:
        raise ValueError("the Stage-4L selected/first boundary changed")
    power = _mapping(
        stage4l.get("stable_power_certificate"),
        "Stage-4L stable powers",
    )
    if (
        power.get("one_step_norm_upper") != STABLE_ONE_STEP_UPPER
        or power.get("registered_stable_rate_upper") != STABLE_RATE_ONE
        or power.get("stable_power_constant_upper") != "1"
        or power.get("k_s_equals_one_validated") is not True
        or power.get("output_belongs_to_E_s_by_exact_intertwining") is not True
    ):
        raise ValueError("the Stage-4L stable rate changed")

    stage1 = _mapping(
        parents[STAGE1_RESULT_RELATIVE_PATH].get("contract"),
        "Stage-1 stable-manifold contract",
    )
    if stage1.get("model_id") != MODEL_ID or stage1.get("branch") != BRANCH:
        raise ValueError("the Stage-1 model identity changed")
    evidence = _mapping(
        stage1.get("proved_parent_evidence"),
        "Stage-1 proved parent evidence",
    )
    if (
        evidence.get("unstable_multiplier_modulus_lower")
        != UNSTABLE_MULTIPLIER_MODULUS_LOWER
        or evidence.get("unstable_multiplier_modulus_upper")
        != UNSTABLE_MULTIPLIER_MODULUS_UPPER
        or evidence.get("unstable_backward_rate_upper_derived")
        != UNSTABLE_BACKWARD_RATE_ONE
        or evidence.get("inner_nontranslation_unstable_multiplier_count") != 1
    ):
        raise ValueError("the proved one-dimensional unstable evidence changed")

    stage4r = _mapping(
        parents[STAGE4R_RESULT_RELATIVE_PATH].get("theorem"),
        "Stage-4R theorem",
    )
    claims = _mapping(stage4r.get("claim_status"), "Stage-4R claims")
    if (
        stage4r.get("status") != "PROVED_FORMAL_THEOREM"
        or claims.get("direct_same_semiflow_return_stable_set_identification_proved")
        is not True
        or claims.get("Q_equals_Pm_is_sufficient_not_necessary_registered")
        is not True
        or claims.get("any_concrete_return_map_validated") is not False
        or claims.get("any_concrete_stable_graph_validated") is not False
    ):
        raise ValueError("the Stage-4R stable-germ boundary changed")


def _formal_core(certificate: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "formal_two_step_split_theorem": certificate[
            "formal_two_step_split_theorem"
        ],
        "nonlinear_composition_bridge": certificate[
            "nonlinear_composition_bridge"
        ],
        "nested_domain_stable_set_bridge": certificate[
            "nested_domain_stable_set_bridge"
        ],
        "same_semiflow_time_composition": certificate[
            "same_semiflow_time_composition"
        ],
        "stage4r_stable_germ_bridge": certificate[
            "stage4r_stable_germ_bridge"
        ],
        "claim_status": certificate["claim_status"],
    }


def build_stage4s_split_bridge_certificate(
    repository: Path,
) -> Stage4SSplitBridgeCertificate:
    parents = _parent_payloads(repository)
    _validate_parent_semantics(parents)
    if _exact_decimal_square(STABLE_RATE_ONE) != STABLE_RATE_TWO:
        raise ArithmeticError("the registered stable rate did not square exactly")
    if _exact_decimal_square(STABLE_ONE_STEP_UPPER) != STABLE_TWO_STEP_UPPER:
        raise ArithmeticError("the sharper stable bound did not square exactly")
    if (
        _exact_decimal_square(UNSTABLE_BACKWARD_RATE_ONE)
        != UNSTABLE_BACKWARD_RATE_TWO
    ):
        raise ArithmeticError("the unstable backward rate did not square exactly")

    claims = {name: True for name in TRUE_FLAGS}
    claims.update({name: False for name in FALSE_FLAGS})
    scope = {
        "linear_two_step_fixed_splitting": True,
        "linear_two_step_stable_rate": True,
        "linear_two_step_unstable_backward_rate": True,
        "nonlinear_selected_one_return": False,
        "nonlinear_selected_two_return": False,
        "nested_composition_domain": False,
        "common_intervening_flow_tube": False,
        "repeated_selected_hits": False,
        "no_earlier_hit_or_first_return": False,
        "stable_graph": False,
        "periodic_orbit_stable_set_germ": False,
        "pulse_crossing_onset_routing_or_safety": False,
    }
    return Stage4SSplitBridgeCertificate(
        schema_id=SCHEMA_ID,
        model_id=MODEL_ID,
        branch=BRANCH,
        status=STATUS,
        parent_result_sha256=dict(PARENT_RESULT_SHA256),
        formal_two_step_split_theorem={
            "setting": (
                "Sigma is a Banach space, A in L(Sigma), q in Sigma, "
                "f in Sigma*, f(q)=1, Aq=mu q, and fA=mu f"
            ),
            "projections_and_spaces": (
                "P_u=q f, P_s=I-q f, E_u=span{q}=ran(P_u), "
                "E_s=ker(f)=ran(P_s), and Sigma=E_s direct_sum E_u"
            ),
            "projection_identities": (
                "P_s^2=P_s, P_u^2=P_u, P_sP_u=P_uP_s=0, and P_s+P_u=I"
            ),
            "one_step_intertwining": (
                "AP_s=P_sA=P_sAP_s and AP_u=P_uA=mu P_u"
            ),
            "two_step_definition": (
                "B:=A^2 is the linear two-step operator; B is not named a "
                "nonlinear selected return"
            ),
            "two_step_intertwining": (
                "BP_s=P_sB=P_sBP_s=(AP_s)^2 and "
                "BP_u=P_uB=mu^2 P_u"
            ),
            "fixed_invariance": (
                "A(E_s) subset E_s, A(E_u) subset E_u, B(E_s) subset E_s, "
                "and B(E_u) subset E_u"
            ),
            "stable_restriction": (
                "A_s=A|E_s, B_s=B|E_s=A_s^2, and B_s^n=A_s^(2n)"
            ),
            "stable_rate_transfer": (
                "if ||A_s^n||<=K_s*rho_s^n, then "
                "||B_s^n||<=K_s*rho_s^(2n); when K_s=1 this is rate rho_s^2"
            ),
            "unstable_restriction": "B_u=B|E_u=mu^2 I_Eu",
            "unstable_inverse_formula": (
                "if mu!=0, then B_u is invertible and "
                "||(B_u)^(-n)||=|mu|^(-2n) for every n>=0 in any inherited "
                "norm on the one-dimensional E_u"
            ),
            "unstable_rate_transfer": (
                "if |mu|^(-1)<=rho_u<1, then "
                "||(B_u)^(-n)||<=rho_u^(2n), with K_u=1 and backward rate rho_u^2"
            ),
            "proof": (
                "expand P_s=I-qf and P_u=qf, use f(q)=1 for idempotence, "
                "use Aq=mu q and fA=mu f for commutation, and then multiply "
                "the exact identities; the rate statements follow from "
                "B_s^n=A_s^(2n) and scalar multiplication on E_u"
            ),
        },
        model_linear_instance={
            "proved_object": (
                "B=A^2 for the Stage-4L selected near-one-period phase-fixed "
                "discrete linear section operator"
            ),
            "section": "Sigma_0={h in Y:h_v(0)=0}",
            "fixed_splitting": (
                "P_s=I-qf, P_u=qf, E_s=ker(f), E_u=span{q}"
            ),
            "stage4l_exact_relations": [
                "Aq=mu_u q",
                "fA=mu_u f",
                "f(q)=1",
                "AP_s=P_sA=P_sAP_s",
            ],
            "unstable_multiplier_identification": (
                "Stage 4L uses the physical section eigencolumn q=q^Sigma "
                "for mu_u; the source-bound Floquet audit has exactly one "
                "nontranslation unstable multiplier, so its modulus and "
                "inverse bounds apply to this scalar restriction"
            ),
            "one_return_stable_power": (
                "||A_s^n||<=rho_term^n<=0.1^n with K_s=1"
            ),
            "one_return_stable_one_step_upper": STABLE_ONE_STEP_UPPER,
            "two_return_sharper_stable_one_step_upper": STABLE_TWO_STEP_UPPER,
            "two_return_registered_stable_rate_upper": STABLE_RATE_TWO,
            "two_return_stable_power": (
                "||B_s^n||<=rho_term^(2n)<=0.01^n with K_s=1"
            ),
            "one_return_unstable_multiplier_modulus_lower": (
                UNSTABLE_MULTIPLIER_MODULUS_LOWER
            ),
            "one_return_unstable_multiplier_modulus_upper": (
                UNSTABLE_MULTIPLIER_MODULUS_UPPER
            ),
            "one_return_unstable_backward_rate_upper": (
                UNSTABLE_BACKWARD_RATE_ONE
            ),
            "two_return_unstable_backward_rate_upper": (
                UNSTABLE_BACKWARD_RATE_TWO
            ),
            "two_return_unstable_power": (
                "||(B_u)^(-n)||<=rho_u,2^n, rho_u,2<=rho_u,1^2, K_u=1"
            ),
            "forward_backward_orientation": (
                "the unstable forward multiplier of B has modulus |mu_u|^2>1; "
                "the number below one is the norm rate for backward powers, "
                "not a forward contraction rate"
            ),
            "nonlinear_claim": False,
        },
        nonlinear_composition_bridge={
            "hypotheses": (
                "D is an open section-coordinate neighborhood of p, "
                "P:D->Sigma is C1, P(p)=p, P(D) need not lie in D, and "
                "A=DP(p)"
            ),
            "nested_domain": "D_2={x in D:P(x) in D}",
            "openness": (
                "D_2 is open when P is continuous and D is open"
            ),
            "composition": "Q=P o P is defined on D_2",
            "local_fixed_point_requirement": (
                "p belongs to D_2 because P(p)=p belongs to D"
            ),
            "chain_rule": "DQ(p)=DP(p)DP(p)=A^2=B",
            "self_map_not_automatic": (
                "Q:D_2->Sigma need not map D_2, or any chosen N, into itself"
            ),
            "derivative_only": (
                "the fixed E_s direct_sum E_u splitting is invariant for DQ(p); "
                "it does not make affine E_s or E_u invariant under nonlinear Q"
            ),
            "c2_graph_gate": (
                "a stable graph for Q still requires a C2 self-map on a "
                "validated neighborhood, hyperbolicity, and the relevant "
                "quantitative nonlinear bounds"
            ),
            "model_hypotheses_validated": False,
        },
        nested_domain_stable_set_bridge={
            "setting": (
                "P is continuous at p with P(p)=p; N subset D_2; "
                "Q=P^2 maps N into N"
            ),
            "all_even_iterates_exist": (
                "Q(N) subset N gives Q^n(x) in N subset D_2 for every n"
            ),
            "all_odd_iterates_exist": (
                "P(Q^n(x)) is defined and lies in D for every n because N subset D_2"
            ),
            "convergence_equivalence": (
                "Q^n(x)->p iff the full alternating P-orbit P^j(x)->p; "
                "the reverse is immediate, while the forward direction uses "
                "P(Q^n(x))->P(p)=p"
            ),
            "stronger_same_patch_version": (
                "to identify a conventional local stable set W_N^s(P), also "
                "require P(N) subset N; this is not supplied by Q(N) subset N"
            ),
            "does_not_supply": (
                "event times, flow arcs, a common tube, an event ordinal, or "
                "absence of earlier section hits"
            ),
            "model_hypotheses_validated": False,
        },
        same_semiflow_time_composition={
            "one_return_hypotheses": (
                "P(x)=Phi_{theta(x)}(x) on D for one selected branch of the "
                "same semiflow, theta:D->(0,infinity) is continuous, and both "
                "legs are defined on D_2"
            ),
            "two_return_identity": (
                "Q(x)=P(P(x))=Phi_{Theta_2(x)}(x), "
                "Theta_2(x)=theta(x)+theta(P(x))"
            ),
            "semigroup_requirement": (
                "the identity uses the semiflow law and existence of the full "
                "concatenated trajectory; an abstract map composition is not enough"
            ),
            "period_at_fixed_point": (
                "if theta(p)=P_orbit, then Q(p)=p and Theta_2(p)=2*P_orbit"
            ),
            "time_bounds": (
                "if 0<theta_lower<=theta<=theta_upper on N union P(N), then "
                "2*theta_lower<=Theta_2<=2*theta_upper"
            ),
            "common_tube_gate": (
                "to obtain one Q intervening tube G, prove every first leg from "
                "N and every second leg from P(N) stays in the same G"
            ),
            "selected_hit_count": (
                "the composition records the chosen intermediate hit P(x) and "
                "the terminal hit P^2(x), but does not exclude other earlier or "
                "intervening section hits"
            ),
            "first_return_consequence": False,
            "model_hypotheses_validated": False,
        },
        stage4r_stable_germ_bridge={
            "direct_route": (
                "on a local section patch N containing p, a continuous direct "
                "selected return Q:N->N of the same semiflow may be used "
                "without any identity Q=P^2"
            ),
            "required_fixed_data": (
                "Gamma compact P_orbit-periodic, p in Gamma, Q(p)=p, and "
                "Theta(p)=m*P_orbit (m=2 for a near-two-period return)"
            ),
            "required_time_data": (
                "Theta:N->[Theta_lower,Theta_upper] is continuous and "
                "0<Theta_lower<=Theta_upper<infinity"
            ),
            "required_flow_data": (
                "Q(x)=Phi_{Theta(x)}(x) and one common G contains every "
                "Phi_s(x), x in N, 0<=s<=Theta(x)"
            ),
            "required_section_data": (
                "closure(N) intersect Gamma={p}, or the equivalent sequential "
                "section-isolation property"
            ),
            "conclusion_if_all_hypotheses_hold": (
                "W_N^s(Q)=N intersect W_G^s(Gamma), hence equality of germs at p"
            ),
            "q_equals_p_squared_role": (
                "a sufficient nested-domain construction of Q, not a necessary "
                "hypothesis and not a replacement for time/tube/isolation data"
            ),
            "graph_role": (
                "only a C2 hyperbolic stable-graph theorem for this same Q can "
                "identify its graph with the displayed periodic-orbit stable germ"
            ),
            "model_hypotheses_validated": False,
        },
        common_tube_and_repeated_hit_audit={
            "pure_algebra_supplies": [
                "B=A^2",
                "fixed derivative splitting and intertwining",
                "squared stable forward powers",
                "squared unstable backward powers",
            ],
            "nested_q_equals_p2_supplies_conditionally": [
                "two defined selected-map legs",
                "one named intermediate selected hit",
                "the derivative identity DQ(p)=A^2",
                "even/odd discrete convergence equivalence",
            ],
            "still_requires_nonlinear_semiflow_validation": [
                "one C1 or C2 selected one-return branch P",
                "D_2 and an invariant Q-domain N",
                "same-semiflow realization and uniform positive time bounds",
                "one common tube covering both legs for every point",
                "repeated composability for every Q iterate",
                "section isolation at the periodic orbit",
            ],
            "requires_separate_ordinal_validation": [
                "no earlier section hit",
                "first-positive-return status",
                "an m-th-return label if claimed",
            ],
            "stage4l_terminal_operator_norm_is_a_tube_bound": False,
            "stage4l_terminal_operator_norm_proves_repeated_hits": False,
        },
        proved_conditional_open_ledger={
            "proved": [
                "general fixed-splitting algebra for A and B=A^2",
                "general stable and scalar inverse-unstable squared-rate transfer",
                "model B stable rate 0.01 with K_s=1",
                "model B scalar unstable backward rate at most the displayed "
                "square with K_u=1",
                "conditional nested-domain chain-rule and discrete even/odd lemmas",
                "exact audit of the Stage-4R stable-germ hypotheses",
            ],
            "conditional": [
                "Q=P^2 and DQ(p)=A^2 for a validated C1 selected self-composition",
                "same-semiflow time addition and two selected legs",
                "equality of discrete Q-stable and flow periodic-orbit stable germs",
                "a C2 hyperbolic stable graph for Q",
            ],
            "open_model_specific": [
                "nonlinear selected P or direct Q on an open/invariant section ball",
                "nested-domain and repeated-hit closure",
                "uniform return-time bounds and common intervening flow tube",
                "section isolation, nonlinear Hessian blocks, and stable graph",
                "no-earlier/first-return semantics, pulse crossing, onset, "
                "routing, and safety",
            ],
        },
        scope_boundary=scope,
        claim_status=claims,
    )


def build_stage4s_split_bridge_result(repository: Path) -> dict[str, Any]:
    repository = repository.resolve()
    certificate = asdict(build_stage4s_split_bridge_certificate(repository))
    return {
        "certificate": certificate,
        "manifest": {
            "schema_id": SCHEMA_ID,
            "result": RESULT_RELATIVE_PATH,
            "default_command": DEFAULT_COMMAND,
            "arithmetic_scope": ARITHMETIC_SCOPE,
            "artifact_sha256": canonical_sha256(certificate),
            "formal_core_sha256": canonical_sha256(_formal_core(certificate)),
            "source_sha256": {
                relative: _sha256_path(repository / relative)
                for relative in SOURCE_MANIFEST
            },
            "parent_result_sha256": dict(PARENT_RESULT_SHA256),
            "runtime": _runtime_record(),
        },
    }


def validate_stage4s_split_bridge_result(
    payload: Mapping[str, Any],
    repository: Path,
    *,
    recompute: bool = False,
) -> None:
    if not isinstance(payload, Mapping) or set(payload) != TOP_KEYS:
        raise ValueError("the Stage-4S-C result has the wrong outer schema")
    certificate = _mapping(payload.get("certificate"), "Stage-4S-C certificate")
    manifest = _mapping(payload.get("manifest"), "Stage-4S-C manifest")
    if set(certificate) != {
        field.name for field in fields(Stage4SSplitBridgeCertificate)
    }:
        raise ValueError("the Stage-4S-C certificate schema changed")
    if set(manifest) != MANIFEST_KEYS:
        raise ValueError("the Stage-4S-C manifest schema changed")

    expected_certificate = asdict(
        build_stage4s_split_bridge_certificate(repository)
    )
    if dict(certificate) != expected_certificate:
        raise ValueError("the Stage-4S-C theorem or audit changed")

    claims = _mapping(certificate.get("claim_status"), "Stage-4S-C claims")
    if set(claims) != set(TRUE_FLAGS) | set(FALSE_FLAGS):
        raise ValueError("the Stage-4S-C claim ledger changed")
    if any(claims.get(name) is not True for name in TRUE_FLAGS):
        raise ValueError("a proved Stage-4S-C claim was demoted")
    if any(claims.get(name) is not False for name in FALSE_FLAGS):
        raise ValueError("an open Stage-4S-C model claim was promoted")

    expected_manifest = {
        "schema_id": SCHEMA_ID,
        "result": RESULT_RELATIVE_PATH,
        "default_command": DEFAULT_COMMAND,
        "arithmetic_scope": ARITHMETIC_SCOPE,
        "artifact_sha256": canonical_sha256(certificate),
        "formal_core_sha256": canonical_sha256(_formal_core(certificate)),
        "source_sha256": {
            relative: _sha256_path(repository.resolve() / relative)
            for relative in SOURCE_MANIFEST
        },
        "parent_result_sha256": dict(PARENT_RESULT_SHA256),
        "runtime": _runtime_record(),
    }
    if dict(manifest) != expected_manifest:
        raise ValueError("the Stage-4S-C manifest or source binding changed")
    if recompute and dict(payload) != build_stage4s_split_bridge_result(repository):
        raise ValueError("the Stage-4S-C fresh replay changed")


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
    "STABLE_ONE_STEP_UPPER",
    "STABLE_RATE_ONE",
    "STABLE_RATE_TWO",
    "STABLE_TWO_STEP_UPPER",
    "STATUS",
    "Stage4SSplitBridgeCertificate",
    "TEST_RELATIVE_PATH",
    "TOP_KEYS",
    "TRUE_FLAGS",
    "UNSTABLE_BACKWARD_RATE_ONE",
    "UNSTABLE_BACKWARD_RATE_TWO",
    "UNSTABLE_MULTIPLIER_MODULUS_LOWER",
    "UNSTABLE_MULTIPLIER_MODULUS_UPPER",
    "_exact_decimal_square",
    "_formal_core",
    "build_stage4s_split_bridge_certificate",
    "build_stage4s_split_bridge_result",
    "canonical_sha256",
    "validate_stage4s_split_bridge_result",
]
