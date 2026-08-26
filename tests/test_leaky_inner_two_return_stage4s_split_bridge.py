from __future__ import annotations

import ast
from copy import deepcopy
import json
from pathlib import Path

import pytest

import canard_control.leaky_inner_two_return_stage4s_split_bridge as stage4s
from canard_control.leaky_inner_two_return_stage4s_split_bridge import (
    FALSE_FLAGS,
    GENERATOR_RELATIVE_PATH,
    NOTE_RELATIVE_PATH,
    PARENT_RESULT_SHA256,
    RESULT_RELATIVE_PATH,
    SOURCE_MANIFEST,
    STABLE_ONE_STEP_UPPER,
    STABLE_RATE_ONE,
    STABLE_RATE_TWO,
    STABLE_TWO_STEP_UPPER,
    TRUE_FLAGS,
    UNSTABLE_BACKWARD_RATE_ONE,
    UNSTABLE_BACKWARD_RATE_TWO,
    _exact_decimal_square,
    _formal_core,
    canonical_sha256,
    validate_stage4s_split_bridge_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]
EXPECTED_ARTIFACT_SHA256: str | None = (
    "e374068f4c6dc1ea2c8c40ddac64c21453efb93ec98d8765a13f890caa444770"
)
EXPECTED_FORMAL_CORE_SHA256: str | None = (
    "efeaea278ce03a5de22bae8444dc431e99b9e91409b685b8b0529787f90fe107"
)


def _payload() -> dict[str, object]:
    return json.loads(
        (REPOSITORY / RESULT_RELATIVE_PATH).read_text(encoding="utf-8")
    )


def _refresh_digests(payload: dict[str, object]) -> None:
    certificate = payload["certificate"]
    payload["manifest"]["artifact_sha256"] = canonical_sha256(certificate)
    payload["manifest"]["formal_core_sha256"] = canonical_sha256(
        _formal_core(certificate)
    )


def test_registered_stage4s_split_bridge_validates_and_replays() -> None:
    assert EXPECTED_ARTIFACT_SHA256 is not None
    assert EXPECTED_FORMAL_CORE_SHA256 is not None
    payload = _payload()
    validate_stage4s_split_bridge_result(
        payload, REPOSITORY, recompute=True
    )
    assert (
        payload["manifest"]["artifact_sha256"]
        == EXPECTED_ARTIFACT_SHA256
    )
    assert (
        payload["manifest"]["formal_core_sha256"]
        == EXPECTED_FORMAL_CORE_SHA256
    )


def test_all_three_parent_results_are_exactly_bound() -> None:
    payload = _payload()
    assert payload["certificate"]["parent_result_sha256"] == (
        PARENT_RESULT_SHA256
    )
    assert payload["manifest"]["parent_result_sha256"] == (
        PARENT_RESULT_SHA256
    )
    assert len(PARENT_RESULT_SHA256) == 3
    for relative, digest in PARENT_RESULT_SHA256.items():
        assert stage4s._sha256_path(REPOSITORY / relative) == digest


def test_formal_projectors_direct_sum_and_one_step_intertwining_are_exact() -> None:
    theorem = _payload()["certificate"]["formal_two_step_split_theorem"]
    for identity in (
        "P_s^2=P_s",
        "P_u^2=P_u",
        "P_sP_u=P_uP_s=0",
        "P_s+P_u=I",
    ):
        assert identity in theorem["projection_identities"]
    assert "Sigma=E_s direct_sum E_u" in theorem[
        "projections_and_spaces"
    ]
    assert theorem["one_step_intertwining"] == (
        "AP_s=P_sA=P_sAP_s and AP_u=P_uA=mu P_u"
    )


def test_b_is_linear_a_squared_and_keeps_the_fixed_splitting() -> None:
    theorem = _payload()["certificate"]["formal_two_step_split_theorem"]
    assert "B:=A^2" in theorem["two_step_definition"]
    assert "not named a nonlinear selected return" in theorem[
        "two_step_definition"
    ]
    assert "BP_s=P_sB=P_sBP_s=(AP_s)^2" in theorem[
        "two_step_intertwining"
    ]
    assert "BP_u=P_uB=mu^2 P_u" in theorem["two_step_intertwining"]
    assert theorem["stable_restriction"] == (
        "A_s=A|E_s, B_s=B|E_s=A_s^2, and B_s^n=A_s^(2n)"
    )


def test_stable_rate_is_squared_with_k_s_one() -> None:
    instance = _payload()["certificate"]["model_linear_instance"]
    assert _exact_decimal_square(STABLE_RATE_ONE) == STABLE_RATE_TWO
    assert _exact_decimal_square(STABLE_ONE_STEP_UPPER) == (
        STABLE_TWO_STEP_UPPER
    )
    assert instance["two_return_registered_stable_rate_upper"] == "0.01"
    assert "K_s=1" in instance["two_return_stable_power"]
    assert instance["two_return_sharper_stable_one_step_upper"] == (
        STABLE_TWO_STEP_UPPER
    )


def test_unstable_inverse_rate_is_squared_and_not_forward_rate() -> None:
    theorem = _payload()["certificate"]["formal_two_step_split_theorem"]
    instance = _payload()["certificate"]["model_linear_instance"]
    assert _exact_decimal_square(UNSTABLE_BACKWARD_RATE_ONE) == (
        UNSTABLE_BACKWARD_RATE_TWO
    )
    assert "||(B_u)^(-n)||=|mu|^(-2n)" in theorem[
        "unstable_inverse_formula"
    ]
    assert instance["two_return_unstable_backward_rate_upper"] == (
        UNSTABLE_BACKWARD_RATE_TWO
    )
    assert "K_u=1" in instance["two_return_unstable_power"]
    assert "|mu_u|^2>1" in instance["forward_backward_orientation"]
    assert "not a forward contraction rate" in instance[
        "forward_backward_orientation"
    ]


def test_nonlinear_q_equals_p_squared_uses_the_nested_domain() -> None:
    bridge = _payload()["certificate"]["nonlinear_composition_bridge"]
    assert bridge["nested_domain"] == "D_2={x in D:P(x) in D}"
    assert "D_2 is open" in bridge["openness"]
    assert bridge["composition"] == "Q=P o P is defined on D_2"
    assert bridge["chain_rule"] == "DQ(p)=DP(p)DP(p)=A^2=B"
    assert "need not map D_2" in bridge["self_map_not_automatic"]
    assert bridge["model_hypotheses_validated"] is False


def test_derivative_splitting_is_not_nonlinear_invariance() -> None:
    bridge = _payload()["certificate"]["nonlinear_composition_bridge"]
    assert "invariant for DQ(p)" in bridge["derivative_only"]
    assert "does not make affine E_s or E_u invariant" in bridge[
        "derivative_only"
    ]
    assert "C2 self-map" in bridge["c2_graph_gate"]


def test_even_odd_convergence_needs_continuity_and_precise_domains() -> None:
    bridge = _payload()["certificate"]["nested_domain_stable_set_bridge"]
    assert "N subset D_2" in bridge["setting"]
    assert "Q=P^2 maps N into N" in bridge["setting"]
    assert "P(Q^n(x))" in bridge["all_odd_iterates_exist"]
    assert "P(Q^n(x))->P(p)=p" in bridge["convergence_equivalence"]
    assert "also require P(N) subset N" in bridge[
        "stronger_same_patch_version"
    ]


def test_same_semiflow_composition_adds_return_times_only_conditionally() -> None:
    bridge = _payload()["certificate"]["same_semiflow_time_composition"]
    assert "P(x)=Phi_{theta(x)}(x)" in bridge["one_return_hypotheses"]
    assert "theta:D->(0,infinity) is continuous" in bridge[
        "one_return_hypotheses"
    ]
    assert "Theta_2(x)=theta(x)+theta(P(x))" in bridge[
        "two_return_identity"
    ]
    assert "semiflow law" in bridge["semigroup_requirement"]
    assert "Theta_2(p)=2*P_orbit" in bridge["period_at_fixed_point"]
    assert "2*theta_lower<=Theta_2<=2*theta_upper" in bridge[
        "time_bounds"
    ]
    assert bridge["first_return_consequence"] is False
    assert bridge["model_hypotheses_validated"] is False


def test_common_two_leg_tube_is_a_separate_gate() -> None:
    bridge = _payload()["certificate"]["same_semiflow_time_composition"]
    audit = _payload()["certificate"][
        "common_tube_and_repeated_hit_audit"
    ]
    assert "first leg from N" in bridge["common_tube_gate"]
    assert "second leg from P(N)" in bridge["common_tube_gate"]
    assert "same G" in bridge["common_tube_gate"]
    assert audit["stage4l_terminal_operator_norm_is_a_tube_bound"] is False
    assert audit[
        "stage4l_terminal_operator_norm_proves_repeated_hits"
    ] is False


def test_selected_hits_do_not_imply_first_or_no_earlier_return() -> None:
    bridge = _payload()["certificate"]["same_semiflow_time_composition"]
    audit = _payload()["certificate"][
        "common_tube_and_repeated_hit_audit"
    ]
    assert "does not exclude other earlier" in bridge["selected_hit_count"]
    assert audit["requires_separate_ordinal_validation"] == [
        "no earlier section hit",
        "first-positive-return status",
        "an m-th-return label if claimed",
    ]


def test_stage4r_direct_q_route_does_not_require_q_equals_p_squared() -> None:
    bridge = _payload()["certificate"]["stage4r_stable_germ_bridge"]
    assert "without any identity Q=P^2" in bridge["direct_route"]
    assert "local section patch N containing p" in bridge["direct_route"]
    assert "Q(p)=p" in bridge["required_fixed_data"]
    assert "Theta(p)=m*P_orbit" in bridge["required_fixed_data"]
    assert "Theta:N->[Theta_lower,Theta_upper] is continuous" in bridge[
        "required_time_data"
    ]
    assert "0<Theta_lower" in bridge["required_time_data"]
    assert "one common G" in bridge["required_flow_data"]
    assert "closure(N) intersect Gamma={p}" in bridge[
        "required_section_data"
    ]
    assert "W_N^s(Q)=N intersect W_G^s(Gamma)" in bridge[
        "conclusion_if_all_hypotheses_hold"
    ]


def test_q_equals_p_squared_is_not_a_tube_or_isolation_substitute() -> None:
    bridge = _payload()["certificate"]["stage4r_stable_germ_bridge"]
    assert "sufficient nested-domain construction" in bridge[
        "q_equals_p_squared_role"
    ]
    assert "not a necessary hypothesis" in bridge[
        "q_equals_p_squared_role"
    ]
    assert "not a replacement for time/tube/isolation data" in bridge[
        "q_equals_p_squared_role"
    ]
    assert bridge["model_hypotheses_validated"] is False


def test_proved_conditional_open_ledger_is_explicit() -> None:
    ledger = _payload()["certificate"]["proved_conditional_open_ledger"]
    assert set(ledger) == {"proved", "conditional", "open_model_specific"}
    assert any("B=A^2" in item for item in ledger["proved"])
    assert any("Q=P^2" in item for item in ledger["conditional"])
    assert any("common intervening flow tube" in item for item in ledger[
        "open_model_specific"
    ])


def test_scope_has_only_the_three_linear_model_outputs_true() -> None:
    scope = _payload()["certificate"]["scope_boundary"]
    true_scope = {name for name, value in scope.items() if value is True}
    assert true_scope == {
        "linear_two_step_fixed_splitting",
        "linear_two_step_stable_rate",
        "linear_two_step_unstable_backward_rate",
    }
    assert all(
        value is False for name, value in scope.items() if name not in true_scope
    )


def test_claim_ledger_is_exact_and_fail_closed() -> None:
    claims = _payload()["certificate"]["claim_status"]
    assert set(claims) == set(TRUE_FLAGS) | set(FALSE_FLAGS)
    assert all(claims[name] is True for name in TRUE_FLAGS)
    assert all(claims[name] is False for name in FALSE_FLAGS)
    assert len(TRUE_FLAGS) == 25
    assert len(FALSE_FLAGS) == 20


@pytest.mark.parametrize(
    "flag",
    [
        "model_nonlinear_two_return_map_validated",
        "model_common_intervening_flow_tube_validated",
        "model_first_positive_return_validated",
        "model_periodic_orbit_stable_set_germ_validated",
    ],
)
def test_promoting_any_representative_open_claim_fails(flag: str) -> None:
    payload = deepcopy(_payload())
    payload["certificate"]["claim_status"][flag] = True
    _refresh_digests(payload)
    with pytest.raises(ValueError):
        validate_stage4s_split_bridge_result(payload, REPOSITORY)


def test_demoting_a_proved_linear_claim_fails_even_after_rehash() -> None:
    payload = deepcopy(_payload())
    payload["certificate"]["claim_status"][
        "b_equals_a_squared_preserves_same_fixed_splitting_proved"
    ] = False
    _refresh_digests(payload)
    with pytest.raises(ValueError):
        validate_stage4s_split_bridge_result(payload, REPOSITORY)


def test_changing_squared_unstable_rate_fails_even_after_rehash() -> None:
    payload = deepcopy(_payload())
    payload["certificate"]["model_linear_instance"][
        "two_return_unstable_backward_rate_upper"
    ] = "0.31"
    _refresh_digests(payload)
    with pytest.raises(ValueError):
        validate_stage4s_split_bridge_result(payload, REPOSITORY)


def test_promoting_model_q_equals_p_squared_fails_even_after_rehash() -> None:
    payload = deepcopy(_payload())
    payload["certificate"]["nonlinear_composition_bridge"][
        "model_hypotheses_validated"
    ] = True
    _refresh_digests(payload)
    with pytest.raises(ValueError):
        validate_stage4s_split_bridge_result(payload, REPOSITORY)


def test_parent_digest_mutation_fails() -> None:
    payload = deepcopy(_payload())
    relative = next(iter(PARENT_RESULT_SHA256))
    payload["manifest"]["parent_result_sha256"][relative] = "0" * 64
    with pytest.raises(ValueError):
        validate_stage4s_split_bridge_result(payload, REPOSITORY)


def test_source_digest_mutation_fails() -> None:
    payload = deepcopy(_payload())
    payload["manifest"]["source_sha256"][NOTE_RELATIVE_PATH] = "0" * 64
    with pytest.raises(ValueError):
        validate_stage4s_split_bridge_result(payload, REPOSITORY)


def test_extra_outer_key_fails() -> None:
    payload = deepcopy(_payload())
    payload["unexpected"] = None
    with pytest.raises(ValueError):
        validate_stage4s_split_bridge_result(payload, REPOSITORY)


def test_generator_uses_fsync_and_atomic_replace() -> None:
    tree = ast.parse(
        (REPOSITORY / GENERATOR_RELATIVE_PATH).read_text(encoding="utf-8")
    )
    attributes = {
        node.attr for node in ast.walk(tree) if isinstance(node, ast.Attribute)
    }
    assert "fsync" in attributes
    assert "replace" in attributes


def test_every_new_artifact_filename_contains_stage4s_split_bridge() -> None:
    assert len(SOURCE_MANIFEST) == 4
    for relative in (*SOURCE_MANIFEST, RESULT_RELATIVE_PATH):
        assert "stage4s_split_bridge" in Path(relative).name


def test_no_flagship_or_readme_file_is_in_the_source_manifest() -> None:
    for relative in SOURCE_MANIFEST:
        assert not relative.startswith("manuscript/")
        assert Path(relative).name != "README.md"
