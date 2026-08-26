"""Stage-4R theorem for eventually smooth selected-event RFDE maps.

This standalone formal artifact treats autonomous retarded equations

    x'(t) = F(x_t),  x_t(theta)=x(t+theta),

on X=C([-tau_star,0],R^d), with finitely many constant discrete delays (or,
more generally, a C^k functional F on X).  It separates two facts which are
often conflated:

* for each fixed time, the solution map can be C^k in the initial history
  even while an untranslated part of that history remains in the segment;
* joint time/initial-history C^k regularity of the complete segment map needs
  eventual time smoothing, because time differentiation differentiates the
  translated history.

For C2, the strict common-window condition T_minus>2*tau_star is sufficient.
For an integer k>=1, F in C^k and T_minus>k*tau_star give the corresponding
safe C^k statement.  These thresholds are sufficient, not asserted necessary
or sharp.  The proof records the operator-valued mixed-jet induction needed
for joint Frechet smoothness; pointwise time derivatives alone are not used as
a substitute.

The event theorem is stated on a C^k initial-section parameterization
iota:D subset M -> U, with an open event-functional domain V and explicit
image containment.  Common endpoint signs and a common positive event speed
give a unique C^k selected event time and C^k complete-history hit.  This hit
is called an induced section return only after return-to-chart containment and
a C^k terminal chart inverse are separately assumed.

The proof is independent of the finite network dimension.  A selected branch
need not be the first return.  A direct near-m-period return Q:N->N of the same
semiflow identifies the periodic-orbit stable-set germ under bounded positive
return times, a common intervening tube, a fixed point Q(p)=p, and an isolated
local section patch whose closure meets the periodic orbit only at p.  An
identity Q=P^m is one sufficient algebraic route, not a necessary one.

No model-specific number or biological, graph, crossing, onset, routing,
capture, or safety claim is imported or promoted.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from hashlib import sha256
import json
from pathlib import Path
import platform
from typing import Any, Mapping


SCHEMA_ID = "finite-delay-eventually-smooth-selected-return-stage4r-v2"
STATUS = "PROVED_FORMAL_THEOREM"
THEOREM_CLASS = "finite-dimensional autonomous constant-delay RFDE"

SOURCE_RELATIVE_PATH = (
    "src/canard_control/"
    "finite_delay_eventually_smooth_selected_return_stage4r.py"
)
GENERATOR_RELATIVE_PATH = (
    "experiments/finite_delay_eventually_smooth_selected_return_stage4r.py"
)
RESULT_RELATIVE_PATH = (
    "experiments/results/"
    "finite_delay_eventually_smooth_selected_return_stage4r.json"
)
NOTE_RELATIVE_PATH = (
    "docs/finite-delay-eventually-smooth-selected-return-stage4r.md"
)
TEST_RELATIVE_PATH = (
    "tests/test_finite_delay_eventually_smooth_selected_return_stage4r.py"
)

PARENT_RESULT_SHA256: dict[str, str] = {}
SOURCE_MANIFEST = (
    SOURCE_RELATIVE_PATH,
    GENERATOR_RELATIVE_PATH,
    NOTE_RELATIVE_PATH,
    TEST_RELATIVE_PATH,
)
DEPENDENCY_SOURCE_MANIFEST: tuple[str, ...] = ()

DEFAULT_COMMAND = (
    "PYTHONPATH=src /usr/bin/python3 experiments/"
    "finite_delay_eventually_smooth_selected_return_stage4r.py"
)
ARITHMETIC_SCOPE = (
    "symbolic Banach-space chain rule, operator-valued method-of-steps "
    "time-smoothing induction, parameterized scalar implicit-function "
    "theorem, section-chart adapter, and isolated-section semiflow stable-set "
    "identification only; no model-specific numerical ingress"
)

TOP_KEYS = {"theorem", "manifest"}
MANIFEST_KEYS = {
    "schema_id",
    "result",
    "default_command",
    "arithmetic_scope",
    "theorem_sha256",
    "formal_core_sha256",
    "source_sha256",
    "dependency_source_sha256",
    "parent_result_sha256",
    "runtime",
}

TRUE_FLAGS = (
    "fixed_time_initial_history_smoothness_distinguished_from_joint_time_smoothness",
    "maximal_semiflow_open_domain_registered",
    "eventual_C2_complete_segment_lemma_proved",
    "eventual_joint_operator_valued_Ck_smoothing_proved",
    "strict_T_minus_greater_than_2_tau_star_is_C2_sufficient",
    "safe_Ck_extension_with_T_minus_greater_than_k_tau_star_proved",
    "common_window_endpoint_signs_and_speed_imply_unique_selected_event",
    "Ck_initial_section_parameterization_registered",
    "open_event_domain_and_image_containment_registered",
    "selected_event_time_and_complete_history_hit_Ck_proved",
    "ambient_event_hit_distinguished_from_induced_section_return",
    "first_and_second_event_return_chain_rules_registered",
    "selected_branch_and_ordinal_first_return_separated",
    "network_dimension_independence_proved",
    "direct_same_semiflow_return_stable_set_identification_proved",
    "stable_set_section_isolation_and_precise_domains_registered",
    "stable_return_fixed_point_and_period_registered",
    "Q_equals_Pm_is_sufficient_not_necessary_registered",
    "threshold_claimed_sufficient_only",
    "formal_theorem_has_no_model_specific_parent",
)

FALSE_FLAGS = (
    "pointwise_solution_derivatives_claimed_sufficient_for_joint_Frechet_Ck",
    "ambient_event_hit_claimed_to_be_section_self_return_without_containment",
    "section_return_induced_without_terminal_chart_containment",
    "recurrent_hits_alone_claimed_to_force_Qn_to_p",
    "section_isolation_omitted_from_stable_set_germ_lemma",
    "T_greater_than_k_tau_star_claimed_necessary",
    "T_greater_than_k_tau_star_claimed_sharp",
    "state_dependent_delay_extension_proved",
    "neutral_equation_extension_proved",
    "infinite_delay_extension_proved",
    "infinite_dimensional_node_state_extension_proved",
    "any_concrete_RFDE_tube_validated",
    "any_concrete_event_window_validated",
    "any_concrete_event_speed_validated",
    "any_concrete_selected_event_validated",
    "any_concrete_event_ordinal_validated",
    "any_concrete_return_map_validated",
    "any_concrete_stable_graph_validated",
    "any_model_specific_Hessian_block_validated",
    "any_pulse_stable_sheet_crossing_validated",
    "any_biological_onset_or_control_claim_validated",
    "any_routing_capture_or_safety_claim_validated",
)


@dataclass(frozen=True)
class Stage4RTheorem:
    schema_id: str
    status: str
    theorem_class: str
    parent_result_sha256: dict[str, str]
    phase_space_and_equation: dict[str, Any]
    fixed_time_initial_data_smoothness: dict[str, Any]
    eventual_time_smoothing_lemma: dict[str, Any]
    selected_event_return_theorem: dict[str, Any]
    event_and_return_derivative_formulas: dict[str, Any]
    safe_Ck_extension: dict[str, Any]
    nonautomaticity_example: dict[str, Any]
    ordinal_and_no_earlier_boundary: dict[str, Any]
    network_dimension_audit: dict[str, Any]
    direct_return_stable_set_lemma: dict[str, Any]
    minimum_application_certificate: dict[str, Any]
    references_and_proof_status: dict[str, Any]
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


def _formal_core(theorem: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "phase_space_and_equation": theorem["phase_space_and_equation"],
        "eventual_time_smoothing_lemma": theorem[
            "eventual_time_smoothing_lemma"
        ],
        "selected_event_return_theorem": theorem[
            "selected_event_return_theorem"
        ],
        "safe_Ck_extension": theorem["safe_Ck_extension"],
        "direct_return_stable_set_lemma": theorem[
            "direct_return_stable_set_lemma"
        ],
        "strict_numeric_ingress": theorem["strict_numeric_ingress"],
        "claim_status": theorem["claim_status"],
    }


def _runtime_record() -> dict[str, str]:
    return {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "arithmetic": (
            "formal theorem text and exact JSON/SHA-256 binding; no floating-"
            "point or model-specific numerical arithmetic"
        ),
    }


def build_stage4r_theorem() -> Stage4RTheorem:
    claims = {name: True for name in TRUE_FLAGS}
    claims.update({name: False for name in FALSE_FLAGS})
    return Stage4RTheorem(
        schema_id=SCHEMA_ID,
        status=STATUS,
        theorem_class=THEOREM_CLASS,
        parent_result_sha256={},
        phase_space_and_equation={
            "phase_space": "X=C([-tau_star,0],R^d) with the sup norm",
            "dimension": "d is any positive finite integer",
            "maximum_delay": "tau_star>0",
            "equation": "x'(t)=F(x_t), x_t(theta)=x(t+theta)",
            "functional_domain": "F:U subset X -> R^d on an open set U",
            "regularity": "F belongs to C^r, r>=2",
            "maximal_semiflow_domain": (
                "Phi:Omega->X is the maximal local semiflow, with Omega a "
                "relatively open subset of [0,infinity) x U; (t,phi) belongs "
                "to Omega exactly on the declared solution-existence domain"
            ),
            "constant_delay_scope": (
                "every finite system x'=f(x(t),x(t-tau_1),...,"
                "x(t-tau_N)) with fixed 0<=tau_j<=tau_star and f in C^r; "
                "the proof also applies to any C^r functional F on X"
            ),
            "excluded_classes": (
                "state-dependent delays, neutral equations, infinite delays, "
                "and infinite-dimensional node state require separate proofs"
            ),
        },
        fixed_time_initial_data_smoothness={
            "statement": (
                "on every common existence tube contained in U, for each fixed "
                "t the segment solution operator Phi_t:phi->x_t(phi) has the "
                "same C^k initial-history smoothness as F, 1<=k<=r"
            ),
            "proof_mechanism": (
                "differentiate the Volterra integral equation in the initial "
                "history; the first and higher jets solve the triangular "
                "retarded variational hierarchy"
            ),
            "unadvanced_history_piece": (
                "for t<tau_star, part of Phi_t(phi) is a fixed translation of "
                "phi and is affine, hence harmless for fixed-t differentiation"
            ),
            "does_not_imply_joint_time_smoothness": True,
            "key_distinction": (
                "varying t moves the translated evaluation point, whereas "
                "varying phi at fixed t does not"
            ),
        },
        eventual_time_smoothing_lemma={
            "smooth_domain_order_k": (
                "Omega_k=Omega intersect ((k*tau_star,infinity) x U)"
            ),
            "operator_jet_space": (
                "J_ab(t,phi)=partial_t^a D_phi^b Phi_t(phi) belongs to "
                "L^b(X,X), with L^0(X,X)=X and a+b<=k"
            ),
            "operator_norm_induction_statement": (
                "for every 1<=j<=k and a+b<=j, J_ab exists and is continuous "
                "in the norm of L^b(X,X) on Omega_j; this is the induction "
                "statement that yields joint Frechet C^j"
            ),
            "C1_base": (
                "fixed-time Volterra differentiation gives D_phi Phi_t; for "
                "t>tau_star the translated arbitrary initial-history piece "
                "has cleared the complete output segment, and the solution "
                "and first-variation integral equations give J_10 and J_01 "
                "continuously in X and L(X,X), respectively"
            ),
            "C2_step": (
                "for s>tau_star the segment x_s is C1 and "
                "x''(s)=DF(x_s)[theta->x'(s+theta)]"
            ),
            "complete_segment_C2": (
                "if t>2*tau_star, then every s=t+theta in the output segment "
                "satisfies s>tau_star, so x'', first-variation time "
                "derivatives, and all second mixed jets are continuous over "
                "the complete theta interval"
            ),
            "joint_map": "S(t,phi)=Phi_t(phi)",
            "C2_conclusion": (
                "S restricted to Omega_2 is jointly Frechet C2 in (t,phi)"
            ),
            "induction_step": (
                "differentiate x'=F(x_t) and the triangular variational "
                "hierarchy; the highest pure spatial jet satisfies a linear "
                "Volterra variational equation with coefficient DF, whose "
                "inhomogeneous source is a finite Banach Faà di Bruno "
                "combination of D^qF and lower operator-valued jets; the "
                "mixed time jets follow by differentiating the equation; "
                "t>j*tau_star makes the earliest output time exceed "
                "(j-1)*tau_star, so the lower-jet induction applies on the "
                "whole segment; local Volterra estimates give continuity in "
                "multilinear operator norm"
            ),
            "joint_Frechet_Ck_conclusion": (
                "S restricted to Omega_k is C^k jointly in time and initial "
                "history"
            ),
            "pointwise_derivatives_alone_are_sufficient": False,
            "locality": (
                "at each base point, a compact trajectory-time interval and "
                "a sufficiently small solution neighborhood give the local "
                "Volterra bounds needed for Frechet C^k regularity; no global "
                "uniform derivative bound over an unbounded D is asserted"
            ),
            "strict_boundary": (
                "the inequality is strict to avoid propagated compatibility "
                "faces at integer combinations of delays"
            ),
            "proof_style": (
                "operator-valued method-of-steps induction, the Volterra "
                "variational hierarchy, and the Banach chain rule; no "
                "dimension-dependent estimate enters"
            ),
            "sufficient_not_necessary": True,
        },
        selected_event_return_theorem={
            "parameter_domain": (
                "M is a Banach section-coordinate space, D is open in M, and "
                "iota:D->U is a C^k initial-history parameterization; the "
                "ambient specialization is M=X and iota=id"
            ),
            "semiflow_domain_containment": (
                "(t,iota(u)) belongs to the open maximal semiflow domain "
                "Omega for every (t,u) in I x D"
            ),
            "event_functional_domain": (
                "V is open in X, g:V->R belongs to C^k, and "
                "Phi_t(iota(u)) belongs to V for every (t,u) in I x D"
            ),
            "event_function": "H(t,u)=g(Phi_t(iota(u)))",
            "common_window": "I=[T_minus,T_plus] for every u in D",
            "smoothing_gate_C2": "T_minus>2*tau_star",
            "left_sign": "sup_u H(T_minus,u)<=-delta_minus<0",
            "right_sign": "inf_u H(T_plus,u)>=delta_plus>0",
            "speed_gate": (
                "partial_t H(t,u)>=a_star>0 for every (t,u) in I x D"
            ),
            "selected_event_conclusion": (
                "there is exactly one T(u) in (T_minus,T_plus), and local "
                "implicit-function branches agree globally by uniqueness"
            ),
            "regularity_conclusion_C2": "T belongs to C2(D,R)",
            "complete_history_hit": "R(u)=Phi_{T(u)}(iota(u))",
            "hit_conclusion_C2": "R belongs to C2(D,X)",
            "ambient_event_hit_specialization": (
                "for M=X and iota=id, R is an ambient selected-event hit map "
                "into g^{-1}(0); this alone does not make R a section "
                "self-map"
            ),
            "induced_section_return": (
                "if iota is a C^k chart of an initial section patch, the hit "
                "satisfies R(D) subset Sigma_out, and chi:Sigma_out->D_out is "
                "a C^k terminal section chart, then P=chi o R:D->D_out is the "
                "induced C^k selected section return"
            ),
            "return_without_terminal_chart_containment_claimed": False,
            "endpoint_signs_are_existence_not_regularity_inputs": True,
            "positive_speed_is_uniqueness_and_IFT_denominator": True,
        },
        event_and_return_derivative_formulas={
            "notation": (
                "set S(t,u)=Phi_t(iota(u)); evaluate S, H=g o S and their "
                "partial derivatives at (T(u),u); h,k are directions in M"
            ),
            "first_event_derivative": "T_h=-H_u[h]/H_t",
            "second_event_derivative": (
                "T_hk=-(H_uu[h,k]+H_tu[h]*T_k+H_tu[k]*T_h+"
                "H_tt*T_h*T_k)/H_t"
            ),
            "H_uu": (
                "D2g(S)[S_u h,S_u k]+Dg(S)[S_uu[h,k]]"
            ),
            "H_tu": (
                "D2g(S)[S_t,S_u h]+Dg(S)[S_tu h]"
            ),
            "H_tt": "D2g(S)[S_t,S_t]+Dg(S)[S_tt]",
            "first_hit_derivative": "DR[h]=S_u[h]+S_t*T_h",
            "second_hit_derivative": (
                "D2R[h,k]=S_uu[h,k]+S_tu[h]*T_k+S_tu[k]*T_h+"
                "S_tt*T_h*T_k+S_t*T_hk"
            ),
            "affine_section_specialization": (
                "if g is affine then D2g=0, recovering the usual event-"
                "aligned variational formula"
            ),
            "phase_correction_count": 1,
        },
        safe_Ck_extension={
            "integer_range": "1<=k<=r",
            "operator_valued_regularization": (
                "for every a+b<=j, partial_t^a D_phi^b Phi_t is continuous "
                "in L^b(X,X) on Omega_j, 1<=j<=k"
            ),
            "induction": (
                "the highest order-j pure spatial jet solves its linear "
                "Volterra variational equation with an inhomogeneous Banach "
                "Faà di Bruno source built from lower jets; mixed time jets "
                "then use the equation on the complete segment; the earliest "
                "output time t-tau_star exceeds the order-(j-1) threshold "
                "when t>j*tau_star"
            ),
            "complete_segment_gate": "T_minus>k*tau_star",
            "joint_segment_conclusion": (
                "S(t,u)=Phi_t(iota(u)) is jointly C^k on I x D by the "
                "operator-valued smoothing lemma and the C^k chain rule"
            ),
            "event_and_hit_conclusion": (
                "for open V, g in C^k, image containment, and the same "
                "signs/speed gate, T and the complete-history hit R are C^k"
            ),
            "induced_return_conclusion": (
                "a C^k section return follows only after terminal section-"
                "chart containment and composition with its C^k inverse chart"
            ),
            "strictly_sufficient": True,
            "necessity_or_optimality_claimed": False,
        },
        nonautomaticity_example={
            "equation": "scalar x'(t)=x(t-tau_star)",
            "early_solution": (
                "x(r;phi)=phi(0)+integral_0^r phi(s-tau_star) ds for "
                "0<r<tau_star"
            ),
            "variable_time_functional": (
                "J(phi)=integral_0^(r0+ell(phi)) phi(s-tau_star) ds"
            ),
            "first_derivative": (
                "DJ(phi)h=integral_0^r h(s-tau_star) ds+"
                "phi(r-tau_star)*ell(h)"
            ),
            "second_derivative_obstruction": (
                "differentiating again requires the derivative of phi at "
                "r-tau_star when both time directions are nonzero"
            ),
            "conclusion": (
                "fixed-time smooth dependence does not make a variable-time "
                "complete-history map C2 on an open ball of arbitrary "
                "continuous histories"
            ),
            "example_claims_threshold_sharp": False,
        },
        ordinal_and_no_earlier_boundary={
            "selected_branch": (
                "the signs and speed prove one unique event in the declared "
                "window, independent of all earlier events"
            ),
            "m_th_label": (
                "calling it the m-th admissible return additionally requires "
                "a directed count/exclusion of all earlier admissible events"
            ),
            "no_earlier_hit_hypothesis_required_for_Ck_selected_branch": False,
            "no_earlier_hit_hypothesis_required_for_first_return_or_ordinal": True,
            "negative_or_other_section_crossings_may_exist": True,
        },
        network_dimension_audit={
            "dimension_quantifier": "every finite d>=1",
            "network_encoding": (
                "a finite network with finitely many node coordinates is one "
                "larger vector x in R^d"
            ),
            "delay_count": "any finite number of fixed discrete delays",
            "threshold_depends_on": "only k and the maximum delay tau_star",
            "threshold_depends_on_network_size": False,
            "constants_for_a_concrete_tube_may_depend_on_dimension": True,
            "infinite_network_claim": False,
        },
        direct_return_stable_set_lemma={
            "setting": (
                "Phi is a continuous semiflow on a metric phase space, Gamma "
                "is a compact P-periodic orbit, p belongs to Gamma, and N is "
                "a local section patch containing p"
            ),
            "section_isolation": (
                "the closure of N meets Gamma only at p; equivalently for the "
                "proof, y_n in N and dist(y_n,Gamma)->0 imply y_n->p"
            ),
            "selected_return_domain": (
                "Theta:N->[Theta_lower,Theta_upper] and Q:N->N are continuous, "
                "0<Theta_lower<=Theta_upper<infinity, "
                "Q(x)=Phi_{Theta(x)}(x), Theta(p)=m*P for an integer m>=1, "
                "and Q(p)=p"
            ),
            "intervening_tube": (
                "there is one common local tube G such that Phi_s(x) belongs "
                "to G for every x in N and 0<=s<=Theta(x)"
            ),
            "discrete_stable_set_definition": (
                "W_N^s(Q)={x in N: Q^n(x) is in N for all n and Q^n(x)->p}"
            ),
            "flow_stable_set_definition": (
                "W_G^s(Gamma)={x: Phi_t(x) is in G for all t>=0 and "
                "dist(Phi_t(x),Gamma)->0}"
            ),
            "selected_times": (
                "t_0=0 and t_n=sum_{j=0}^{n-1} Theta(Q^j(x)); the positive "
                "lower bound gives t_n->infinity and the upper bound covers "
                "each interval [t_n,t_{n+1}] by one uniformly bounded arc"
            ),
            "forward_implication": (
                "Q^n(x)->p implies dist(Phi_t(x),Gamma)->0 because every "
                "large t lies on a uniformly bounded flow arc issuing from "
                "Q^n(x), and joint continuity is uniform on that compact "
                "time band"
            ),
            "reverse_implication": (
                "flow convergence gives dist(Q^n(x),Gamma)->0 at t_n; since "
                "Q^n(x) remains in N, compactness of Gamma and the isolated "
                "section closure force Q^n(x)->p"
            ),
            "recurrent_hits_alone_are_sufficient_for_reverse": False,
            "exact_local_equality": (
                "W_N^s(Q)=N intersect W_G^s(Gamma) under the displayed "
                "domain and tube hypotheses"
            ),
            "stable_set_germ": (
                "germ_p W^s(Q)=germ_p(Sigma intersect W^s(Gamma)) after "
                "shrinking isolated section patches N"
            ),
            "Q_equals_Pm_route": (
                "Q=P^m on suitable nested domains is a sufficient algebraic "
                "way to identify the same germ"
            ),
            "Q_equals_Pm_is_necessary": False,
            "first_return_status_is_necessary": False,
            "C2_graph_consequence": (
                "only if Q is C2, p is its hyperbolic fixed point, and DQ(p) "
                "has the required splitting does a stable graph theorem for "
                "Q construct this same periodic-orbit stable-set germ"
            ),
        },
        minimum_application_certificate={
            "A_equation": "finite d, finite constant delays, F in C^k",
            "B_semiflow_domain": (
                "the parameterized initial histories and common event window "
                "belong to the open maximal semiflow domain Omega"
            ),
            "C_smoothing": "strict T_minus>k*tau_star",
            "D_initial_parameterization": (
                "a C^k map iota:D subset M->U from an open Banach coordinate "
                "domain"
            ),
            "E_event_domain": (
                "V open in X, g:V->R in C^k, and Phi_t(iota(D)) subset V "
                "throughout the common window"
            ),
            "F_event": (
                "two strict endpoint signs and one uniform positive speed"
            ),
            "G_local_return_optional": (
                "to call the hit a section return, validate terminal section-"
                "chart containment and a C^k terminal inverse chart"
            ),
            "H_ordinal_optional": (
                "earlier-event count/exclusion only if m-th or first-return "
                "semantics are claimed"
            ),
            "I_stable_set_optional": (
                "for stable-germ identification validate Q:N->N, Q(p)=p, "
                "Theta(p)=mP, bounded positive return times, one intervening "
                "tube, and closure(N) intersect Gamma={p}"
            ),
            "finite_sampling_sufficient": False,
        },
        references_and_proof_status={
            "classical_background": (
                "Diekmann, van Gils, Verduyn Lunel and Walther, Delay "
                "Equations (1995), Chapters VII.4 and XIV.3"
            ),
            "use_of_background": (
                "fixed-time RFDE smooth dependence and Poincare-map context; "
                "the operator-valued method-of-steps induction, threshold, "
                "parameterized selected-event composition, and isolated-"
                "section stable-germ proof are spelled out in this artifact"
            ),
            "proof_complete_at_formal_level": True,
            "external_numeric_or_model_parent": None,
        },
        strict_numeric_ingress={
            "dimension_d": None,
            "number_of_discrete_delays": None,
            "tau_star": None,
            "regularity_order_k": None,
            "T_minus": None,
            "T_plus": None,
            "left_event_margin": None,
            "right_event_margin": None,
            "speed_lower_a_star": None,
            "solution_tube_result": None,
            "selected_return_result": None,
            "ordinal_count_result": None,
            "stable_set_tube_result": None,
            "all_concrete_hypotheses_validated": False,
            "any_model_application_validated": False,
            "evidence_status": "FORMAL_GENERAL_THEOREM_ONLY",
        },
        theorem_boundary={
            "proved_here": (
                "the general operator-valued eventual-smoothing lemma, the "
                "parameterized selected-event hit C2 theorem and safe Ck "
                "extension, exact event/hit chain rules, the conditional "
                "induced-section-return adapter, and the isolated-section "
                "direct-return stable-set identification lemma"
            ),
            "not_proved_here": (
                "necessity or sharpness of k*tau_star, state-dependent or "
                "neutral extensions, a section return without terminal chart "
                "containment, stable-germ identification without section "
                "isolation, any concrete flow/event tube, event ordinal, "
                "graph, Hessian, crossing, biological control, routing, "
                "capture, or safety statement"
            ),
            "stage4o_or_flagship_files_modified": False,
        },
        claim_status=claims,
    )


def build_stage4r_result(repository: Path) -> dict[str, Any]:
    repository = repository.resolve()
    theorem = asdict(build_stage4r_theorem())
    return {
        "theorem": theorem,
        "manifest": {
            "schema_id": SCHEMA_ID,
            "result": RESULT_RELATIVE_PATH,
            "default_command": DEFAULT_COMMAND,
            "arithmetic_scope": ARITHMETIC_SCOPE,
            "theorem_sha256": canonical_sha256(theorem),
            "formal_core_sha256": canonical_sha256(_formal_core(theorem)),
            "source_sha256": {
                relative: _sha256_path(repository / relative)
                for relative in SOURCE_MANIFEST
            },
            "dependency_source_sha256": {},
            "parent_result_sha256": {},
            "runtime": _runtime_record(),
        },
    }


def validate_stage4r_result(
    payload: Mapping[str, Any],
    repository: Path,
    *,
    recompute: bool = False,
) -> None:
    if not isinstance(payload, Mapping) or set(payload) != TOP_KEYS:
        raise ValueError("the Stage-4R result has the wrong outer schema")
    theorem = _mapping(payload.get("theorem"), "Stage-4R theorem")
    manifest = _mapping(payload.get("manifest"), "Stage-4R manifest")
    if set(theorem) != {field.name for field in fields(Stage4RTheorem)}:
        raise ValueError("the Stage-4R theorem schema changed")
    if set(manifest) != MANIFEST_KEYS:
        raise ValueError("the Stage-4R manifest schema changed")

    expected_theorem = asdict(build_stage4r_theorem())
    if dict(theorem) != expected_theorem:
        raise ValueError("the Stage-4R theorem statement changed")

    claims = _mapping(theorem.get("claim_status"), "Stage-4R claims")
    if set(claims) != set(TRUE_FLAGS) | set(FALSE_FLAGS):
        raise ValueError("the Stage-4R claim ledger changed")
    if any(claims.get(name) is not True for name in TRUE_FLAGS):
        raise ValueError("a proved Stage-4R formal fact was weakened")
    if any(claims.get(name) is not False for name in FALSE_FLAGS):
        raise ValueError("an excluded Stage-4R claim was promoted")

    numeric = _mapping(
        theorem.get("strict_numeric_ingress"), "Stage-4R numeric ingress"
    )
    for key, value in numeric.items():
        if key in {
            "all_concrete_hypotheses_validated",
            "any_model_application_validated",
        }:
            if value is not False:
                raise ValueError("a concrete Stage-4R application was promoted")
        elif key == "evidence_status":
            if value != "FORMAL_GENERAL_THEOREM_ONLY":
                raise ValueError("the Stage-4R evidence status changed")
        elif value is not None:
            raise ValueError(f"a Stage-4R numeric ingress was filled: {key}")

    repository = repository.resolve()
    expected_manifest = {
        "schema_id": SCHEMA_ID,
        "result": RESULT_RELATIVE_PATH,
        "default_command": DEFAULT_COMMAND,
        "arithmetic_scope": ARITHMETIC_SCOPE,
        "theorem_sha256": canonical_sha256(theorem),
        "formal_core_sha256": canonical_sha256(_formal_core(theorem)),
        "source_sha256": {
            relative: _sha256_path(repository / relative)
            for relative in SOURCE_MANIFEST
        },
        "dependency_source_sha256": {},
        "parent_result_sha256": {},
        "runtime": _runtime_record(),
    }
    if dict(manifest) != expected_manifest:
        raise ValueError("the Stage-4R manifest or source binding changed")

    if recompute and dict(payload) != build_stage4r_result(repository):
        raise ValueError("the Stage-4R fresh replay changed")


__all__ = [
    "ARITHMETIC_SCOPE",
    "DEFAULT_COMMAND",
    "DEPENDENCY_SOURCE_MANIFEST",
    "FALSE_FLAGS",
    "GENERATOR_RELATIVE_PATH",
    "MANIFEST_KEYS",
    "NOTE_RELATIVE_PATH",
    "PARENT_RESULT_SHA256",
    "RESULT_RELATIVE_PATH",
    "SCHEMA_ID",
    "SOURCE_MANIFEST",
    "SOURCE_RELATIVE_PATH",
    "STATUS",
    "Stage4RTheorem",
    "TEST_RELATIVE_PATH",
    "THEOREM_CLASS",
    "TOP_KEYS",
    "TRUE_FLAGS",
    "_formal_core",
    "build_stage4r_result",
    "build_stage4r_theorem",
    "canonical_sha256",
    "validate_stage4r_result",
]
