from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from canard_control.leaky_inner_split_bimeasure_residual_stage4w import (
    BLOCK_NAMES,
    ERROR_CATEGORIES,
    FALSE_FLAGS,
    PARENT_RESULT_SHA256,
    RESULT_RELATIVE_PATH,
    SOURCE_MANIFEST,
    TRUE_FLAGS,
    _formal_core,
    canonical_sha256,
    validate_stage4w_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]
EXPECTED_ARTIFACT_SHA256 = (
    "2fc75c41bc0bb7e00a17320f7de8cb7a112395a67b0c31b62e879ec1fad804c0"
)
EXPECTED_FORMAL_CORE_SHA256 = (
    "96526e1eb85218e602d28302ed005eed509c969a09943af603fd827eaf1073e3"
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


def test_five_parent_results_are_exactly_frozen() -> None:
    assert PARENT_RESULT_SHA256 == {
        "experiments/results/leaky_inner_event_aligned_return_hessian_stage4o_contract.json": (
            "dc0e3951cb529dbdca384ff548ab0d7cd7786fe02573741e80e9c945452b2a23"
        ),
        "experiments/results/leaky_inner_graph_closure_arithmetic_stage4p.json": (
            "860a51d51648919f74bd7bd4e8230a629f7864b2bdcccf490aab5ff9e8e6b542"
        ),
        "experiments/results/leaky_inner_signed_second_variation_stage4q_pilot.json": (
            "e4481bca2d021517073216dab15ee91c43cf301822b15e337c1b5061e9aaf49a"
        ),
        "experiments/results/leaky_inner_stage4s_hessian_bridge.json": (
            "28e7116d855ec1a7e2b169356dce4d4dfb130069b35616a5ed6416f6634522e5"
        ),
        "experiments/results/direct_two_period_derivative_stage4t.json": (
            "6998c1ac89440f180ebe753d1aa41c36c8a849183794fdc38c52f2d8d54e94e1"
        ),
    }


@pytest.mark.skipif(
    not (REPOSITORY / RESULT_RELATIVE_PATH).exists(),
    reason="the Stage-4W result file is absent",
)
def test_registered_result_validates_and_replays() -> None:
    payload = _payload()
    validate_stage4w_result(payload, REPOSITORY, recompute=True)
    assert payload["manifest"]["artifact_sha256"] == EXPECTED_ARTIFACT_SHA256
    assert (
        payload["manifest"]["formal_core_sha256"]
        == EXPECTED_FORMAL_CORE_SHA256
    )


def test_parent_audit_separates_formal_diagnostic_and_numeric_status() -> None:
    audit = _payload()["certificate"]["parent_theorem_audit"]
    assert audit["all_parent_bytes_and_source_manifests_validated"] is True
    assert "every numerical Hessian ingress null" in audit["stage4o"]
    assert "all nineteen theorem flags false" in audit["stage4q"]
    assert "strict numerical ingress null" in audit["stage4s_b"]
    assert "Stage-4S-A/4R direct selected C2 map" in audit["stage4t"]
    assert "D Q_Y(Y_*)=A^2" in audit["stage4t"]


def test_c2_map_implies_only_a_qualitative_local_hessian_bound() -> None:
    theorem = _payload()["certificate"]["qualitative_hessian_localization"]
    assert "Stage-4S-A/4R" in theorem["existence_source"]
    assert "bound and typed by Stage-4T" in theorem["existence_source"]
    assert "Q_coord:D->E_s x R is C2" in theorem["imported_map"]
    assert "for every epsilon>0" in theorem["operator_norm_continuity"]
    assert "B_lambda" in theorem["preferred_shape_ball"]
    assert "lambda_H>0" in theorem["local_boundedness_conclusion"]
    assert "not compactness" in theorem["reason"]
    assert theorem["lambda_H_numeric_lower"] is None
    assert theorem["K_H_numeric_upper"] is None
    assert theorem["lambda_H_equals_preferred_scale_one"] is False
    assert theorem["same_ball_self_map_claimed"] is False
    assert theorem["proved"] is True


def test_hyperbolicity_gives_only_a_qualitative_selected_map_stable_graph() -> None:
    theorem = _payload()["certificate"]["qualitative_local_stable_graph"]
    assert theorem["coordinate_space"].startswith("Z=E_s x R")
    assert "D and D_out are open neighborhoods" in theorem["local_map"]
    assert theorem["stable_power_bound"] == "||(L|Z_s)^n||<=0.01^n"
    assert "rho_u,2<=0.302183" in theorem[
        "unstable_inverse_power_bound"
    ]
    assert "N(0)=0 and DN(0)=0" in theorem["nonlinear_remainder"]
    assert "local stable-manifold theorem" in theorem["theorem_invoked"]
    assert "psi(0)=0 and Dpsi(0)=0" in theorem["conclusion"]
    assert "iterates remain in U" in theorem["local_characterization"]
    assert theorem["global_self_map_needed"] is False
    assert theorem["effective_domain_radius"] is None
    assert theorem["effective_graph_height_or_slope"] is None
    assert theorem["periodic_orbit_stable_set_germ_identified"] is False
    assert "recurrence/phase-isolation" in theorem[
        "why_periodic_germ_still_open"
    ]
    assert theorem["physical_first_return_or_event_ordinal_used"] is False
    assert theorem["pulse_sheet_crossing_implied"] is False
    assert theorem["proved"] is True


def test_phase_and_stable_dual_are_typed_in_the_physical_history_space() -> None:
    dual = _payload()["certificate"]["phase_section_dual"]
    assert "Y=C(K,R) x R" in dual["history_space"]
    assert "Y*=M(K) x R" in dual["dual"]
    assert dual["phase_section"] == (
        "Sigma_0=ker(ell_0), ell_0(phi,w)=phi(0)"
    )
    assert "q_hat in Sigma_0" in dual["fixed_pair"]
    assert "E_s=ker(f_hat) inside Sigma_0" in dual[
        "stable_and_unstable"
    ]
    assert "extension independent" in dual["extension_convention"]


def test_stable_restriction_is_the_exact_two_functional_quotient() -> None:
    theorem = _payload()["certificate"]["stable_quotient_norm_theorem"]
    assert theorem["statement"] == (
        "for every mu in Y*, ||mu|_{E_s}|| = "
        "inf_{alpha,beta in R} ||mu-alpha*ell_0-beta*tilde_f||_{Y*}"
    )
    assert "E_s^perp=span{ell_0,tilde_f}" in theorem[
        "annihilator_identity"
    ]
    assert "metric quotient" in theorem["proof"]
    assert "Hahn-Banach" in theorem["proof"]
    assert theorem["unstable_row_cost"] == "d_u(mu):=|mu(q_hat)|"
    assert theorem["coarse_projection_factor_necessary"] is False
    assert theorem["proved"] is True


def test_split_projective_cost_bounds_every_block_without_raw_projection() -> None:
    theorem = _payload()["certificate"][
        "split_projective_bimeasure_theorem"
    ]
    assert "y_r in Sigma_0" in theorem["admissible_representation"]
    assert theorem["output_costs"]["stable"] == (
        "omega_s(y)=||y-q_hat*f_hat(y)||_Y"
    )
    assert theorem["input_costs"]["stable"] == (
        "d_s(mu)=dist(mu,span{ell_0,tilde_f}) in Y*"
    )
    assert "N_ab^o(B)=inf_rep" in theorem["split_projective_cost"]
    assert "<= N_ab^o(B)" in theorem["operator_inequality"]
    assert "no factor of two" in theorem["symmetry"]
    assert "finite nodal values alone" in theorem["scope"]
    assert theorem["proved"] is True


def test_event_hessian_uses_complete_history_and_one_projection() -> None:
    event = _payload()["certificate"]["complete_history_event_hessian"]
    assert "every voltage output phase theta" in event[
        "complete_history_meaning"
    ]
    assert event["event_time_first_derivative"] == "T_h=-n(h)/a"
    assert event["preprojection_bimeasure"] == (
        "Z=V^T-a^(-1)*(dot_U^T tensor n+n tensor dot_U^T)"
        "+a^(-2)*e tensor n tensor n"
    )
    assert event["event_phase_projection"] == (
        "D2 Q_Y=H=Z-a^(-1)*d tensor (ell_0 o Z)"
    )
    assert event["moving_event_projection_count"] == 1
    assert "one common outward enclosure" in event["correlation_rule"]
    assert "complete translated history first" in event["translation_order"]


def test_qf_output_action_is_exact_and_the_chart_is_affine() -> None:
    action = _payload()["certificate"]["exact_output_split_action"]
    assert action["stable_output"] == (
        "P_s(y tensor mu tensor nu)="
        "(y-q_hat*f_hat(y)) tensor mu tensor nu"
    )
    assert action["unstable_output"] == (
        "f_hat(y tensor mu tensor nu)=f_hat(y)*mu tensor nu"
    )
    assert "exact quotient cost d_s" in action["stable_input"]
    assert "before absolute values" in action["unstable_input"]
    assert "including its recovery atom" in action["output_phase_action"]
    assert "j and chi are affine" in action["affine_chart_identity"]
    assert action["raw_projection_factors_avoided"] is True
    assert action["same_finite_adapter_may_replace_continuous_pair"] is False


def test_six_budget_rows_are_exact_but_all_actual_ingress_is_null() -> None:
    residual = _payload()["certificate"]["six_block_residual_acceptance"]
    assert set(residual["blocks"]) == set(BLOCK_NAMES)
    assert "C_i + sum" in residual["acceptance_inequality"]
    assert residual["all_six_one_correlated_run_required"] is True
    assert residual["direct_split_route_uses_raw_ambient_ceiling"] is False
    assert residual["strict_acceptance_currently_validated"] is False
    for row in residual["blocks"].values():
        assert set(row["projected_error_allowances"]) == set(ERROR_CATEGORIES)
        assert row["actual_directed_center_core_bound"] is None
        assert all(
            value is None for value in row["actual_projected_residuals"].values()
        )
        assert row["strict_acceptance_validated"] is False


def test_center_headroom_implies_a_small_ball_but_not_an_effective_radius() -> None:
    theorem = _payload()["certificate"]["full_ball_inflation_theorem"]
    assert "each B_i is operator-norm continuous" in theorem["continuity"]
    assert "there exists lambda>0" in theorem[
        "qualitative_target_transfer"
    ]
    assert "no compactness" in theorem["proof"]
    assert "Delta_i(lambda)=sup" in theorem["quantitative_inflation"]
    assert theorem["center_strict_caps_currently_validated"] is False
    assert theorem["lambda_numeric_lower_currently_validated"] is False
    assert theorem["inflation_numeric_upper_currently_validated"] is False
    assert theorem["proved_qualitative_implication"] is True


def test_interval_algorithm_requires_signed_defects_and_all_seams() -> None:
    algorithm = _payload()["certificate"]["rigorous_interval_algorithm"]
    assert len(algorithm["steps"]) == 9
    joined = " ".join(algorithm["steps"])
    for token in (
        "delay activation",
        "D1F,D2F,D3F",
        "signed atom-density measures",
        "projective bimeasure norm",
        "same positive event-speed enclosure",
        "all seams",
        "continuous q_hat/f_hat pair",
        "uniform ball residual",
        "six strict inequalities",
    ):
        assert token in joined
    assert "R_U=dot(U_tilde)-DF(X_tilde)U_tilde" in algorithm[
        "first_variation_defect"
    ]
    assert "R_V=dot(V_tilde)-DF(X_tilde)V_tilde" in algorithm[
        "second_variation_defect"
    ]
    assert any(
        "mesh convergence as an error bound" in item
        for item in algorithm["forbidden"]
    )
    assert algorithm["minimally_sufficient"] is True


def test_current_numeric_ingress_is_exactly_zero_of_six() -> None:
    ingress = _payload()["certificate"]["current_numeric_ingress"]
    assert ingress["qualitative_C2_map_and_local_hessian"] is True
    assert (
        ingress["explicit_preferred_shape_lambda_from_bound_parents"] is None
    )
    assert ingress["continuous_history_numeric_blocks_validated"] == 0
    assert ingress["continuous_history_numeric_blocks_required"] == 6
    assert ingress["required_interval_fields_filled"] == 0
    assert ingress["required_interval_fields_total"] > 30
    assert set(ingress["stage4q_heuristic_envelope_diagnostic_only"]) == set(
        BLOCK_NAMES
    )
    assert ingress["stage4q_values_enter_strict_ingress"] is False
    assert ingress["all_six_strict_acceptance_tests_pass"] is False


def test_claim_ledger_is_fail_closed() -> None:
    claims = _payload()["certificate"]["claim_status"]
    assert set(claims) == set(TRUE_FLAGS) | set(FALSE_FLAGS)
    assert all(claims[name] is True for name in TRUE_FLAGS)
    assert all(claims[name] is False for name in FALSE_FLAGS)


def test_validator_rejects_promotion_of_a_numeric_hessian_block() -> None:
    payload = deepcopy(_payload())
    payload["certificate"]["current_numeric_ingress"][
        "directed_center_core_blocks"
    ][BLOCK_NAMES[0]] = "0.00001"
    _refresh_digests(payload)
    with pytest.raises(ValueError):
        validate_stage4w_result(payload, REPOSITORY)


def test_validator_rejects_graph_promotion() -> None:
    payload = deepcopy(_payload())
    payload["certificate"]["claim_status"][
        "quantitative_inner_stable_graph_validated"
    ] = True
    _refresh_digests(payload)
    with pytest.raises(ValueError):
        validate_stage4w_result(payload, REPOSITORY)


def test_all_source_manifest_files_are_present() -> None:
    assert len(SOURCE_MANIFEST) == 4
    assert all((REPOSITORY / relative).is_file() for relative in SOURCE_MANIFEST)
