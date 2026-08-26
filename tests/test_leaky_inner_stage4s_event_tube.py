from __future__ import annotations

from copy import deepcopy
from decimal import Decimal, localcontext
import hashlib
import json
from pathlib import Path

import pytest

from canard_control.leaky_inner_stage4s_event_tube import (
    FALSE_FLAGS,
    MANIFEST_KEYS,
    PARENT_RESULT_SHA256,
    RESULT_RELATIVE_PATH,
    SOURCE_MANIFEST,
    TOP_KEYS,
    TRUE_FLAGS,
    _numeric_core,
    canonical_sha256,
    validate_stage4s_event_tube_result,
)
from canard_control.leaky_reduced_history import (
    validate_leaky_reduced_history_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]


def _payload() -> dict[str, object]:
    return json.loads(
        (REPOSITORY / RESULT_RELATIVE_PATH).read_text(encoding="utf-8")
    )


def _refresh_certificate_digests(payload: dict[str, object]) -> None:
    certificate = payload["certificate"]
    payload["manifest"]["certificate_sha256"] = canonical_sha256(certificate)
    payload["manifest"]["numeric_core_sha256"] = canonical_sha256(
        _numeric_core(certificate)
    )


def test_registered_stage4s_event_tube_fresh_replays() -> None:
    payload = _payload()
    assert set(payload) == TOP_KEYS
    assert set(payload["manifest"]) == MANIFEST_KEYS
    validate_stage4s_event_tube_result(payload, REPOSITORY, recompute=True)


def test_parent_bytes_and_every_declared_source_are_current() -> None:
    payload = _payload()
    assert payload["certificate"]["parent_result_sha256"] == (
        PARENT_RESULT_SHA256
    )
    assert payload["manifest"]["parent_result_sha256"] == (
        PARENT_RESULT_SHA256
    )
    for relative, digest in PARENT_RESULT_SHA256.items():
        assert hashlib.sha256((REPOSITORY / relative).read_bytes()).hexdigest() == digest
        parent = json.loads((REPOSITORY / relative).read_text(encoding="utf-8"))
        for ledger_name in ("source_sha256", "dependency_source_sha256"):
            for source, source_digest in parent["manifest"].get(
                ledger_name, {}
            ).items():
                assert hashlib.sha256(
                    (REPOSITORY / source).read_bytes()
                ).hexdigest() == source_digest


def test_own_source_manifest_is_exact() -> None:
    payload = _payload()
    assert set(payload["manifest"]["source_sha256"]) == set(SOURCE_MANIFEST)
    for relative, digest in payload["manifest"]["source_sha256"].items():
        assert hashlib.sha256((REPOSITORY / relative).read_bytes()).hexdigest() == digest


def test_exact_center_window_arithmetic_closes_in_physical_units() -> None:
    center = _payload()["certificate"]["exact_center_event_window"]
    with localcontext() as context:
        context.prec = 120
        p_minus = Decimal(center["period_lower"])
        p_plus = Decimal(center["period_upper"])
        h = Decimal(center["fixed_extra_half_width_h"])
        assert Decimal(center["T_minus"]) == 2 * p_minus - h
        assert Decimal(center["T_plus"]) == 2 * p_plus + h
        assert Decimal(center["period_width_upper"]) == p_plus - p_minus
        assert Decimal(center["maximum_center_phase_offset_upper"]) == (
            h + 2 * (p_plus - p_minus)
        )
    assert Decimal(center["center_window_history_displacement_upper"]) < (
        Decimal(center["declared_section_ball_radius"])
    )
    assert Decimal(center["center_window_section_ball_margin_lower"]) > 0
    assert "ambient Y-norm ball" in center["declared_ball_semantics"]
    assert "need not satisfy g_Y=0" in center["declared_ball_semantics"]
    assert Decimal(center["center_uniform_event_speed_lower"]) > 0
    assert Decimal(center["center_left_endpoint_gap_lower"]) > 0
    assert Decimal(center["center_right_endpoint_gap_lower"]) > 0
    assert Decimal(center["T_minus_minus_2_tau_max_lower"]) > 14
    assert center["center_selected_time"] == "T(Y_*)=2P exactly"
    assert "Psi_{2P}(Y_*)=Y_*" in center["center_returned_history"]
    assert "Phi_{2P}(Iota(Y_*))=Iota(Y_*)" in center[
        "center_returned_history"
    ]


def test_exact_reduced_history_parent_validates_and_bridges_stage4r_to_Y() -> None:
    relative = "experiments/results/leaky_reduced_history.json"
    assert PARENT_RESULT_SHA256[relative] == (
        "4555fb765a5060a3767a7ea669deb2f4921b8d7410d7d4e15ad077e552da8870"
    )
    reduced_payload = json.loads(
        (REPOSITORY / relative).read_text(encoding="utf-8")
    )
    validate_leaky_reduced_history_result(reduced_payload, REPOSITORY)

    bridge = _payload()["certificate"]["reduced_history_bridge"]
    assert bridge["full_space"] == "X=C([-r,0],R^2)"
    assert bridge["reduced_space"] == "Y=C([-r,0],R)xR"
    assert bridge["projection"].startswith("pi(phi_v,phi_w)")
    assert "Iota(q,omega)" in bridge["compatible_lift"]
    assert "pi o Iota=Id_Y" in bridge["lift_regularity"]
    assert bridge["reduced_semiflow"] == (
        "Psi_t=pi o Phi_t o Iota for every t>=0"
    )
    assert "X_*^X=Iota(Y_*)" in bridge["periodic_center_compatibility"]
    assert "Stage-4R is applied only to Phi on X" in bridge[
        "Stage4R_full_space_input"
    ]
    assert "Psi_t(y)=pi(Phi_t(Iota(y)))" in bridge[
        "reduced_C2_corollary"
    ]
    assert "g_X(Phi_t(Iota(y)))=g_Y(Psi_t(y))" in bridge[
        "event_intertwining"
    ]
    assert bridge["full_X_identified_with_Y_without_bridge"] is False


def test_corrected_stage4n_feasibility_parent_semantics_are_frozen() -> None:
    relative = (
        "experiments/results/"
        "leaky_inner_nonlinear_selected_return_tube_stage4n_feasibility.json"
    )
    assert PARENT_RESULT_SHA256[relative] == (
        "5e7214a2f5ba8ca22649c677a1d054b32342b5cc25966bd8e1da7600c605f1de"
    )
    parent = json.loads((REPOSITORY / relative).read_text(encoding="utf-8"))
    pilot = parent["pilot"]
    assert pilot["claim_status"][
        "centered_voltage_hessian_semantics_validated"
    ] is True
    row = pilot["stage4i_sharpened_generic_gronwall"]
    assert row["exact_inner_voltage_bound_coordinate"] == "centered z=v-1"
    assert row["field_hessian_row_formula"] == (
        "2*(1+B+r)+12*epsilon*kappa3*(B+r), with B=sup|v_*-1|"
    )
    assert row["closure_passes"] is False
    assert "does not lower-bound the true nonlinear flow deviation" in row[
        "scope_of_no_go"
    ]


def test_scaled_full_ball_output_is_existential_but_uniform() -> None:
    theorem = _payload()["certificate"][
        "qualitative_scaled_full_ball_theorem"
    ]
    assert theorem["quantifier"] == "there exists lambda_* in (0,1]"
    assert theorem["numerical_lower_bound"] is None
    assert theorem["preferred_lambda_one_claimed"] is False
    assert "open W subset Y" in theorem["event_open_neighborhood_W"]
    assert "ambient reduced space Y" in theorem["ambient_strengthening"]
    assert "D is an open neighborhood" in theorem["final_coordinate_domain"]
    assert "every member" in theorem["full_ball_scope"]
    assert "arbitrary continuous stable histories" in theorem[
        "full_ball_scope"
    ]
    assert "exactly one T(y)" in theorem["selected_event_output"]
    assert "R_Y" in theorem["regularity_output"]
    assert "proved full-X/reduced-Y bridge" in theorem["regularity_output"]
    assert "lambda_* is chosen last" in theorem["full_ball_scope"]
    assert theorem["ordinal_output"] is None


def test_half_center_margins_are_the_uniform_scaled_ball_targets() -> None:
    center = _payload()["certificate"]["exact_center_event_window"]
    with localcontext() as context:
        context.prec = 120
        assert Decimal(center["scaled_ball_uniform_event_speed_lower"]) == (
            Decimal(center["center_uniform_event_speed_lower"]) / 2
        )
        assert Decimal(center["scaled_ball_left_endpoint_gap_lower"]) == (
            Decimal(center["center_left_endpoint_gap_lower"]) / 2
        )
        assert Decimal(center["scaled_ball_right_endpoint_gap_lower"]) == (
            Decimal(center["center_right_endpoint_gap_lower"]) / 2
        )


def test_return_is_induced_only_after_terminal_patch_containment() -> None:
    containment = _payload()["certificate"]["return_domain_containment"]
    assert "g_Y(y)=0" in containment["terminal_patch"]
    assert containment["initial_containment"] == (
        "j(D) subset W intersect Sigma_loc"
    )
    assert containment["terminal_containment"] == (
        "R_j(D) subset Sigma_loc"
    )
    assert "D_in=j^{-1}" in containment["initial_section_domain"]
    assert "R_j^{-1}(Sigma_loc)" in containment["final_domain"]
    assert "continuity" in containment["why_local_patch"]
    assert "affine C-infinity" in containment["terminal_chart"]
    assert containment["terminal_chart_codomain"] == (
        "D_out=chi(Sigma_loc), an open subset of E_s x R"
    )
    assert "induced C2 selected section return" in containment[
        "induced_return"
    ]
    assert "no assertion P_sel(D) subset D" in containment[
        "induced_return"
    ]
    assert containment["same_scaled_ball_self_map"] is False


def test_domain_quantifiers_choose_lambda_only_after_both_patch_gates() -> None:
    order = _payload()["certificate"]["domain_quantifier_order"]
    assert len(order["order"]) == 6
    assert "obtain open event neighborhood W" in order["order"][0]
    assert "initial section-chart domain" in order["order"][2]
    assert "terminal domain" in order["order"][3]
    assert "define chi:Sigma_loc->D_out" in order["order"][4]
    assert "choose lambda_*" in order["order"][5]
    assert order["W_chosen_before_D"] is True
    assert order["D_in_chosen_before_lambda_star"] is True
    assert order["terminal_preimage_imposed_before_lambda_star"] is True
    assert order["lambda_star_chosen_last"] is True
    assert order["initial_injection_gate"] == "j(D) subset Sigma_loc"
    assert order["terminal_hit_gate"] == (
        "R_Y(j(D)) subset Sigma_loc"
    )
    assert order["ball_gate"] == "B_{lambda_*} subset D"
    assert order["codomain_gate"] == "D_out=chi(Sigma_loc)"


def test_stage_boundaries_keep_proof_conditional_diagnostic_open_separate() -> None:
    certificate = _payload()["certificate"]
    audit = certificate["stage_boundary_audit"]
    assert "lambda=1" in audit["Stage_4N"] and "OPEN" in audit["Stage_4N"]
    assert "no Hessian block" in audit["Stage_4O"]
    assert "CONDITIONAL" in audit["Stage_4P"]
    assert "DIAGNOSTIC" in audit["Stage_4Q"]
    assert "exact pi/Iota semiflow factorization" in audit[
        "Reduced_history_bridge"
    ]
    assert "applied on full X" in audit["Stage_4R"]
    assert "not first return" in audit["selected_vs_ordinal"]
    assert "proves no pulse onset" in audit["selected_vs_biological"]

    tiers = certificate["proved_conditional_diagnostic_open"]
    assert set(tiers) == {
        "PROVED_numeric",
        "PROVED_qualitative",
        "CONDITIONAL",
        "DIAGNOSTIC",
        "OPEN",
    }


def test_claim_ledger_is_fail_closed() -> None:
    claims = _payload()["certificate"]["claim_status"]
    assert set(claims) == set(TRUE_FLAGS) | set(FALSE_FLAGS)
    assert all(claims[name] is True for name in TRUE_FLAGS)
    assert all(claims[name] is False for name in FALSE_FLAGS)


@pytest.mark.parametrize(
    ("key", "value"),
    [
        ("lambda_star_lower", "1e-12"),
        ("preferred_ball_nonlinear_mild_flow_remainder_upper", "0.1"),
        ("six_projected_Hessian_blocks", {"ss": "1"}),
        ("first_or_second_event_ordinal", "second"),
    ],
)
def test_open_numeric_ingress_cannot_be_filled(key: str, value: object) -> None:
    payload = deepcopy(_payload())
    payload["certificate"]["open_numeric_ingress"][key] = value
    _refresh_certificate_digests(payload)
    with pytest.raises(ValueError):
        validate_stage4s_event_tube_result(payload, REPOSITORY)


def test_lambda_one_promotion_is_rejected_even_with_refreshed_digests() -> None:
    payload = deepcopy(_payload())
    payload["certificate"]["claim_status"][
        "preferred_lambda_one_full_ball_validated"
    ] = True
    payload["certificate"]["qualitative_scaled_full_ball_theorem"][
        "preferred_lambda_one_claimed"
    ] = True
    _refresh_certificate_digests(payload)
    with pytest.raises(ValueError):
        validate_stage4s_event_tube_result(payload, REPOSITORY)


def test_stage4q_diagnostic_or_graph_arithmetic_cannot_be_promoted() -> None:
    payload = deepcopy(_payload())
    payload["certificate"]["stage_boundary_audit"]["Stage_4Q"] = (
        "PROVED numerical Hessian evidence"
    )
    payload["certificate"]["claim_status"][
        "signed_second_variation_pilot_promoted_to_proof"
    ] = True
    _refresh_certificate_digests(payload)
    with pytest.raises(ValueError):
        validate_stage4s_event_tube_result(payload, REPOSITORY)


def test_terminal_containment_cannot_be_replaced_by_ambient_hit() -> None:
    payload = deepcopy(_payload())
    payload["certificate"]["return_domain_containment"][
        "terminal_containment"
    ] = None
    _refresh_certificate_digests(payload)
    with pytest.raises(ValueError):
        validate_stage4s_event_tube_result(payload, REPOSITORY)


def test_full_X_cannot_be_identified_with_reduced_Y_without_bridge() -> None:
    payload = deepcopy(_payload())
    bridge = payload["certificate"]["reduced_history_bridge"]
    bridge["full_X_identified_with_Y_without_bridge"] = True
    bridge["reduced_C2_corollary"] = "Stage-4R acts directly on Y"
    payload["certificate"]["claim_status"][
        "full_X_and_reduced_Y_phase_spaces_identified_without_bridge"
    ] = True
    _refresh_certificate_digests(payload)
    with pytest.raises(ValueError, match="theorem statement|conflated"):
        validate_stage4s_event_tube_result(payload, REPOSITORY)


def test_lambda_cannot_be_chosen_before_terminal_preimage_domain() -> None:
    payload = deepcopy(_payload())
    order = payload["certificate"]["domain_quantifier_order"]
    lambda_step = order["order"].pop()
    order["order"].insert(2, lambda_step)
    order["terminal_preimage_imposed_before_lambda_star"] = False
    order["lambda_star_chosen_last"] = False
    payload["certificate"]["claim_status"][
        "lambda_star_chosen_before_initial_and_terminal_domain_restrictions"
    ] = True
    _refresh_certificate_digests(payload)
    with pytest.raises(ValueError, match="theorem statement|domain order"):
        validate_stage4s_event_tube_result(payload, REPOSITORY)


def test_initial_patch_and_explicit_terminal_codomain_cannot_be_removed() -> None:
    payload = deepcopy(_payload())
    containment = payload["certificate"]["return_domain_containment"]
    containment["initial_containment"] = "j(D) subset W"
    containment["terminal_chart_codomain"] = "unspecified"
    payload["certificate"]["claim_status"][
        "ambient_hit_promoted_before_section_domain_containment"
    ] = True
    _refresh_certificate_digests(payload)
    with pytest.raises(ValueError, match="theorem statement|containment|codomain"):
        validate_stage4s_event_tube_result(payload, REPOSITORY)


def test_parent_hash_mutation_is_rejected() -> None:
    payload = deepcopy(_payload())
    relative = next(iter(PARENT_RESULT_SHA256))
    payload["manifest"]["parent_result_sha256"][relative] = "0" * 64
    with pytest.raises(ValueError):
        validate_stage4s_event_tube_result(payload, REPOSITORY)
