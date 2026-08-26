from __future__ import annotations

import ast
from copy import deepcopy
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

import canard_control.finite_delay_eventually_smooth_selected_return_stage4r as stage4r
from canard_control.finite_delay_eventually_smooth_selected_return_stage4r import (
    FALSE_FLAGS,
    MANIFEST_KEYS,
    PARENT_RESULT_SHA256,
    RESULT_RELATIVE_PATH,
    TOP_KEYS,
    TRUE_FLAGS,
    _formal_core,
    canonical_sha256,
    validate_stage4r_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]


def _payload() -> dict[str, object]:
    return json.loads(
        (REPOSITORY / RESULT_RELATIVE_PATH).read_text(encoding="utf-8")
    )


def _refresh_digests(payload: dict[str, object]) -> None:
    theorem = payload["theorem"]
    payload["manifest"]["theorem_sha256"] = canonical_sha256(theorem)
    payload["manifest"]["formal_core_sha256"] = canonical_sha256(
        _formal_core(theorem)
    )


def test_registered_stage4r_result_validates_and_fresh_replays() -> None:
    payload = _payload()
    assert payload["theorem"]["schema_id"].endswith("stage4r-v2")
    assert payload["manifest"]["schema_id"].endswith("stage4r-v2")
    validate_stage4r_result(payload, REPOSITORY, recompute=True)


def test_theorem_is_independent_and_has_no_model_parent() -> None:
    payload = _payload()
    assert PARENT_RESULT_SHA256 == {}
    assert payload["theorem"]["parent_result_sha256"] == {}
    assert payload["manifest"]["parent_result_sha256"] == {}
    assert payload["manifest"]["dependency_source_sha256"] == {}
    assert payload["theorem"]["references_and_proof_status"][
        "external_numeric_or_model_parent"
    ] is None


def test_phase_space_covers_finite_constant_delay_networks_only() -> None:
    setting = _payload()["theorem"]["phase_space_and_equation"]
    assert setting["phase_space"] == "X=C([-tau_star,0],R^d) with the sup norm"
    assert setting["dimension"] == "d is any positive finite integer"
    assert "finite system" in setting["constant_delay_scope"]
    assert "fixed" in setting["constant_delay_scope"]
    assert "any C^r functional F on X" in setting["constant_delay_scope"]
    assert "Phi:Omega->X" in setting["maximal_semiflow_domain"]
    assert "relatively open" in setting["maximal_semiflow_domain"]
    for excluded in (
        "state-dependent delays",
        "neutral equations",
        "infinite delays",
        "infinite-dimensional node state",
    ):
        assert excluded in setting["excluded_classes"]


def test_fixed_time_and_joint_time_smoothness_are_not_conflated() -> None:
    fixed = _payload()["theorem"]["fixed_time_initial_data_smoothness"]
    assert "for each fixed t" in fixed["statement"]
    assert "Volterra integral equation" in fixed["proof_mechanism"]
    assert "affine" in fixed["unadvanced_history_piece"]
    assert fixed["does_not_imply_joint_time_smoothness"] is True
    assert "moves the translated evaluation point" in fixed["key_distinction"]


def test_operator_valued_smoothing_is_joint_Frechet_and_only_sufficient() -> None:
    lemma = _payload()["theorem"]["eventual_time_smoothing_lemma"]
    assert lemma["smooth_domain_order_k"] == (
        "Omega_k=Omega intersect ((k*tau_star,infinity) x U)"
    )
    assert "L^b(X,X)" in lemma["operator_jet_space"]
    assert "norm of L^b(X,X)" in lemma["operator_norm_induction_statement"]
    assert "J_10 and J_01" in lemma["C1_base"]
    assert "s>tau_star" in lemma["C2_step"]
    assert "t>2*tau_star" in lemma["complete_segment_C2"]
    assert "jointly Frechet C2" in lemma["C2_conclusion"]
    assert "Faà di Bruno" in lemma["induction_step"]
    assert "multilinear operator norm" in lemma["induction_step"]
    assert "C^k jointly" in lemma["joint_Frechet_Ck_conclusion"]
    assert lemma["pointwise_derivatives_alone_are_sufficient"] is False
    assert "strict" in lemma["strict_boundary"]
    assert lemma["sufficient_not_necessary"] is True


def test_selected_event_theorem_has_parameterization_open_domains_and_hit() -> None:
    theorem = _payload()["theorem"]["selected_event_return_theorem"]
    assert "M is a Banach section-coordinate space" in theorem["parameter_domain"]
    assert "iota:D->U" in theorem["parameter_domain"]
    assert "open maximal semiflow domain" in theorem[
        "semiflow_domain_containment"
    ]
    assert "V is open in X" in theorem["event_functional_domain"]
    assert "Phi_t(iota(u)) belongs to V" in theorem[
        "event_functional_domain"
    ]
    assert theorem["event_function"] == "H(t,u)=g(Phi_t(iota(u)))"
    assert theorem["smoothing_gate_C2"] == "T_minus>2*tau_star"
    assert "-delta_minus<0" in theorem["left_sign"]
    assert "delta_plus>0" in theorem["right_sign"]
    assert "a_star>0" in theorem["speed_gate"]
    assert "exactly one" in theorem["selected_event_conclusion"]
    assert theorem["regularity_conclusion_C2"] == "T belongs to C2(D,R)"
    assert theorem["complete_history_hit"] == "R(u)=Phi_{T(u)}(iota(u))"
    assert theorem["hit_conclusion_C2"] == "R belongs to C2(D,X)"


def test_ambient_hit_is_not_promoted_to_section_return() -> None:
    theorem = _payload()["theorem"]["selected_event_return_theorem"]
    assert "ambient selected-event hit map" in theorem[
        "ambient_event_hit_specialization"
    ]
    assert "does not make R a section self-map" in theorem[
        "ambient_event_hit_specialization"
    ]
    assert "R(D) subset Sigma_out" in theorem["induced_section_return"]
    assert "chi:Sigma_out->D_out" in theorem["induced_section_return"]
    assert theorem["return_without_terminal_chart_containment_claimed"] is False


def test_event_and_return_second_chain_rules_are_complete() -> None:
    formulas = _payload()["theorem"]["event_and_return_derivative_formulas"]
    assert formulas["first_event_derivative"] == "T_h=-H_u[h]/H_t"
    for term in ("H_uu", "H_tu[h]", "H_tu[k]", "H_tt"):
        assert term in formulas["second_event_derivative"]
    for term in ("S_uu", "S_tu[h]", "S_tu[k]", "S_tt", "S_t*T_hk"):
        assert term in formulas["second_hit_derivative"]
    assert "D2g" in formulas["H_uu"]
    assert formulas["first_hit_derivative"] == "DR[h]=S_u[h]+S_t*T_h"
    assert formulas["phase_correction_count"] == 1


def test_safe_Ck_extension_uses_T_minus_greater_than_k_tau() -> None:
    extension = _payload()["theorem"]["safe_Ck_extension"]
    assert extension["integer_range"] == "1<=k<=r"
    assert "partial_t^a D_phi^b Phi_t" in extension[
        "operator_valued_regularization"
    ]
    assert "L^b(X,X)" in extension["operator_valued_regularization"]
    assert extension["complete_segment_gate"] == "T_minus>k*tau_star"
    assert "jointly C^k" in extension["joint_segment_conclusion"]
    assert "hit R are C^k" in extension["event_and_hit_conclusion"]
    assert "only after terminal section" in extension[
        "induced_return_conclusion"
    ]
    assert extension["strictly_sufficient"] is True
    assert extension["necessity_or_optimality_claimed"] is False


def test_variable_limit_example_exposes_nonautomatic_C2() -> None:
    example = _payload()["theorem"]["nonautomaticity_example"]
    assert example["equation"] == "scalar x'(t)=x(t-tau_star)"
    assert "integral_0^r" in example["early_solution"]
    assert "r0+ell(phi)" in example["variable_time_functional"]
    assert "derivative of phi" in example["second_derivative_obstruction"]
    assert "arbitrary continuous histories" in example["conclusion"]
    assert example["example_claims_threshold_sharp"] is False


def test_selected_branch_regularization_does_not_prove_ordinal() -> None:
    boundary = _payload()["theorem"]["ordinal_and_no_earlier_boundary"]
    assert "independent of all earlier events" in boundary["selected_branch"]
    assert "count/exclusion" in boundary["m_th_label"]
    assert boundary[
        "no_earlier_hit_hypothesis_required_for_Ck_selected_branch"
    ] is False
    assert boundary[
        "no_earlier_hit_hypothesis_required_for_first_return_or_ordinal"
    ] is True
    assert boundary["negative_or_other_section_crossings_may_exist"] is True


def test_network_threshold_is_dimension_independent_but_constants_need_not_be() -> None:
    audit = _payload()["theorem"]["network_dimension_audit"]
    assert audit["dimension_quantifier"] == "every finite d>=1"
    assert "larger vector" in audit["network_encoding"]
    assert audit["threshold_depends_on"] == "only k and the maximum delay tau_star"
    assert audit["threshold_depends_on_network_size"] is False
    assert audit["constants_for_a_concrete_tube_may_depend_on_dimension"] is True
    assert audit["infinite_network_claim"] is False


def test_direct_return_stable_germ_has_fixed_point_domains_and_isolation() -> None:
    lemma = _payload()["theorem"]["direct_return_stable_set_lemma"]
    assert "compact P-periodic orbit" in lemma["setting"]
    assert "closure of N meets Gamma only at p" in lemma["section_isolation"]
    assert "Q:N->N" in lemma["selected_return_domain"]
    assert "Theta(p)=m*P" in lemma["selected_return_domain"]
    assert "Q(p)=p" in lemma["selected_return_domain"]
    assert "one common local tube" in lemma["intervening_tube"]
    assert "W_N^s(Q)" in lemma["discrete_stable_set_definition"]
    assert "W_G^s(Gamma)" in lemma["flow_stable_set_definition"]
    assert "t_n=sum" in lemma["selected_times"]
    assert "uniformly bounded flow arc" in lemma["forward_implication"]
    assert "isolated section closure" in lemma["reverse_implication"]
    assert lemma["recurrent_hits_alone_are_sufficient_for_reverse"] is False
    assert "W_N^s(Q)=N intersect W_G^s(Gamma)" in lemma[
        "exact_local_equality"
    ]
    assert "germ_p" in lemma["stable_set_germ"]
    assert "nested domains" in lemma["Q_equals_Pm_route"]
    assert lemma["Q_equals_Pm_is_necessary"] is False
    assert lemma["first_return_status_is_necessary"] is False
    assert "hyperbolic fixed point" in lemma["C2_graph_consequence"]


def test_application_certificate_keeps_concrete_inputs_external() -> None:
    certificate = _payload()["theorem"]["minimum_application_certificate"]
    assert "F in C^k" in certificate["A_equation"]
    assert "open maximal semiflow domain" in certificate["B_semiflow_domain"]
    assert certificate["C_smoothing"] == "strict T_minus>k*tau_star"
    assert "iota:D subset M->U" in certificate[
        "D_initial_parameterization"
    ]
    assert "V open in X" in certificate["E_event_domain"]
    assert "two strict endpoint signs" in certificate["F_event"]
    assert "terminal section-chart containment" in certificate[
        "G_local_return_optional"
    ]
    assert "only if m-th or first-return" in certificate["H_ordinal_optional"]
    assert "closure(N) intersect Gamma={p}" in certificate[
        "I_stable_set_optional"
    ]
    assert certificate["finite_sampling_sufficient"] is False


def test_every_numeric_or_model_ingress_is_null_or_false() -> None:
    numeric = _payload()["theorem"]["strict_numeric_ingress"]
    for key, value in numeric.items():
        if key in {
            "all_concrete_hypotheses_validated",
            "any_model_application_validated",
        }:
            assert value is False
        elif key == "evidence_status":
            assert value == "FORMAL_GENERAL_THEOREM_ONLY"
        else:
            assert value is None


def test_claim_ledger_is_exact_and_excludes_unsupported_extensions() -> None:
    claims = _payload()["theorem"]["claim_status"]
    assert set(claims) == set(TRUE_FLAGS) | set(FALSE_FLAGS)
    assert all(claims[name] is True for name in TRUE_FLAGS)
    assert all(claims[name] is False for name in FALSE_FLAGS)
    assert claims["safe_Ck_extension_with_T_minus_greater_than_k_tau_star_proved"]
    assert claims["eventual_joint_operator_valued_Ck_smoothing_proved"]
    assert claims["ambient_event_hit_distinguished_from_induced_section_return"]
    assert claims["stable_set_section_isolation_and_precise_domains_registered"]
    assert claims[
        "ambient_event_hit_claimed_to_be_section_self_return_without_containment"
    ] is False
    assert claims["recurrent_hits_alone_claimed_to_force_Qn_to_p"] is False
    assert claims["state_dependent_delay_extension_proved"] is False
    assert claims["T_greater_than_k_tau_star_claimed_necessary"] is False


def test_note_states_theorems_and_scope_with_valid_inline_math() -> None:
    note = (
        REPOSITORY
        / "docs/finite-delay-eventually-smooth-selected-return-stage4r.md"
    ).read_text(encoding="utf-8")
    assert "T_->2\\tau_*," in note
    assert "$T_->k\\tau_*$" in note
    assert "### Theorem 4.1" in note
    assert "### Lemma 3.1" in note
    assert "### Lemma 10.1" in note
    assert "multilinear operator norm" in note
    assert "selected complete-history **hit map**" in note
    assert "Ambient hit versus induced section return" in note
    assert "\\overline N\\cap\\Gamma=\\{p\\}" in note
    assert "recurrence alone would not" in note
    assert "sufficient conditions" in note
    assert "No infinite-network" in note
    assert "(C^2)" not in note
    assert "(T_->" not in note


@pytest.mark.parametrize(
    ("path", "replacement"),
    (
        (("theorem", "strict_numeric_ingress", "tau_star"), "1"),
        (
            (
                "theorem",
                "strict_numeric_ingress",
                "all_concrete_hypotheses_validated",
            ),
            True,
        ),
        (
            (
                "theorem",
                "claim_status",
                "T_greater_than_k_tau_star_claimed_necessary",
            ),
            True,
        ),
        (
            (
                "theorem",
                "claim_status",
                "state_dependent_delay_extension_proved",
            ),
            True,
        ),
        (
            (
                "theorem",
                "eventual_time_smoothing_lemma",
                "sufficient_not_necessary",
            ),
            False,
        ),
        (
            (
                "theorem",
                "event_and_return_derivative_formulas",
                "phase_correction_count",
            ),
            2,
        ),
        (
            (
                "theorem",
                "ordinal_and_no_earlier_boundary",
                "no_earlier_hit_hypothesis_required_for_Ck_selected_branch",
            ),
            True,
        ),
        (
            (
                "theorem",
                "eventual_time_smoothing_lemma",
                "pointwise_derivatives_alone_are_sufficient",
            ),
            True,
        ),
        (
            (
                "theorem",
                "selected_event_return_theorem",
                "return_without_terminal_chart_containment_claimed",
            ),
            True,
        ),
        (
            (
                "theorem",
                "direct_return_stable_set_lemma",
                "recurrent_hits_alone_are_sufficient_for_reverse",
            ),
            True,
        ),
        (
            (
                "theorem",
                "direct_return_stable_set_lemma",
                "section_isolation",
            ),
            "no isolation required",
        ),
        (
            (
                "theorem",
                "direct_return_stable_set_lemma",
                "Q_equals_Pm_is_necessary",
            ),
            True,
        ),
    ),
)
def test_hostile_theorem_numeric_and_scope_changes_are_rejected(
    path: tuple[str, ...], replacement: object
) -> None:
    payload = deepcopy(_payload())
    target = payload
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = replacement
    _refresh_digests(payload)
    with pytest.raises(ValueError):
        validate_stage4r_result(payload, REPOSITORY)


def test_hostile_parent_insertion_is_rejected() -> None:
    payload = deepcopy(_payload())
    fake = "experiments/results/model_specific_parent.json"
    payload["theorem"]["parent_result_sha256"][fake] = "0" * 64
    payload["manifest"]["parent_result_sha256"][fake] = "0" * 64
    _refresh_digests(payload)
    with pytest.raises(ValueError):
        validate_stage4r_result(payload, REPOSITORY)


def test_manifest_digests_and_outer_schema_are_exact() -> None:
    payload = _payload()
    assert set(payload) == TOP_KEYS
    assert set(payload["manifest"]) == MANIFEST_KEYS
    assert payload["manifest"]["theorem_sha256"] == canonical_sha256(
        payload["theorem"]
    )
    assert payload["manifest"]["formal_core_sha256"] == canonical_sha256(
        _formal_core(payload["theorem"])
    )


def test_generator_validates_before_atomic_replace_and_fsyncs() -> None:
    source = (
        REPOSITORY
        / "experiments/finite_delay_eventually_smooth_selected_return_stage4r.py"
    ).read_text(encoding="utf-8")
    ast.parse(source)
    assert source.index("validate_stage4r_result(") < source.index(
        "tempfile.mkstemp("
    )
    assert "os.replace" in source
    assert source.count("os.fsync") >= 2


def test_fresh_interpreter_validation() -> None:
    code = (
        "import json; from pathlib import Path; "
        "from canard_control.finite_delay_eventually_smooth_selected_return_stage4r "
        "import RESULT_RELATIVE_PATH, validate_stage4r_result; "
        "r=Path.cwd(); p=json.loads((r/RESULT_RELATIVE_PATH).read_text()); "
        "validate_stage4r_result(p,r,recompute=True); print('STAGE4R_FRESH_OK')"
    )
    completed = subprocess.run(
        [sys.executable, "-c", code],
        cwd=REPOSITORY,
        check=True,
        capture_output=True,
        text=True,
        env={**os.environ, "PYTHONPATH": "src"},
    )
    assert completed.stdout.strip() == "STAGE4R_FRESH_OK"


def test_result_builder_is_deterministic() -> None:
    assert stage4r.build_stage4r_result(
        REPOSITORY
    ) == stage4r.build_stage4r_result(REPOSITORY)
