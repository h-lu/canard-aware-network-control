from __future__ import annotations

import ast
from copy import deepcopy
import json
from pathlib import Path

import pytest

import canard_control.direct_two_period_derivative_stage4t as stage4t
from canard_control.direct_two_period_derivative_stage4t import (
    FALSE_FLAGS,
    GENERATOR_RELATIVE_PATH,
    NOTE_RELATIVE_PATH,
    RESULT_RELATIVE_PATH,
    SOURCE_MANIFEST,
    STABLE_RATE_TWO,
    TRUE_FLAGS,
    UNSTABLE_BACKWARD_RATE_TWO,
    _formal_core,
    canonical_sha256,
    parent_result_sha256,
    validate_direct_two_period_derivative_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]
EXPECTED_ARTIFACT_SHA256 = (
    "c08107e05bb3dc293fb94d41f9d9a20c66b26983459bd885127e70a1d34061a9"
)
EXPECTED_FORMAL_CORE_SHA256 = (
    "186600d1ced96ee975df3d2104a07c61d7a46e1f219fc007ac4ffed26d55dfe9"
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


def test_stage4sa_parent_is_frozen_and_byte_bound() -> None:
    expected = (
        "b552c5c6fc8afce53ed047ad8264a9d428351d9f031dc566af60969307a1d91f"
    )
    assert stage4t.STAGE4SA_RESULT_SHA256 == expected
    assert parent_result_sha256()[stage4t.STAGE4SA_RESULT_RELATIVE_PATH] == (
        expected
    )


@pytest.mark.skipif(
    not (REPOSITORY / RESULT_RELATIVE_PATH).exists(),
    reason="the Stage-4T result file is absent",
)
def test_registered_stage4t_result_validates_and_replays() -> None:
    assert EXPECTED_ARTIFACT_SHA256 is not None
    assert EXPECTED_FORMAL_CORE_SHA256 is not None
    payload = _payload()
    validate_direct_two_period_derivative_result(
        payload, REPOSITORY, recompute=True
    )
    assert payload["manifest"]["artifact_sha256"] == EXPECTED_ARTIFACT_SHA256
    assert (
        payload["manifest"]["formal_core_sha256"]
        == EXPECTED_FORMAL_CORE_SHA256
    )


def test_map_types_are_explicit() -> None:
    audit = _payload()["certificate"]["map_type_audit"]
    assert "R_Y(y)=Psi_{T(y)}(y)" in audit["stage4sa_reduced_hit"]
    assert audit["reduced_physical_section_map"] == (
        "Q_Y=R_Y|_{j(D)}:j(D)->Sigma_loc"
    )
    assert "Q_coord=chi o R_Y o j" in audit["coordinate_section_map"]
    assert "Q_X(Iota(y))" in audit["compatible_full_section_map"]
    assert audit["reduced_fixed_point_notation"] == "Q_Y(Y_*)=Y_*"
    assert audit["full_fixed_point_notation"] == (
        "Q_X(Iota(Y_*))=Iota(Y_*)"
    )
    assert audit["coordinate_fixed_point_notation"] == "Q_coord(0)=0"
    assert "not literal typed" in audit["ill_typed_notation_rejected"]


def test_direct_center_time_and_fixed_points_are_exact() -> None:
    center = _payload()["certificate"]["direct_two_period_center"]
    assert center["selected_center_time"] == "T(Y_*)=2*P_orb exactly"
    assert "Psi_{2*P_orb}(Y_*)=Y_*" in center["returned_history"]
    assert "Phi_{2*P_orb}(Iota(Y_*))" in center["returned_history"]
    assert center["reduced_fixed_point"] == "Q_Y(Y_*)=Y_*"
    assert center["full_fixed_point"] == (
        "Q_X(Iota(Y_*))=Iota(Y_*)"
    )
    assert center["coordinate_fixed_point"] == "Q_coord(0)=0"
    assert center["first_return_used"] is False
    assert center["nonlinear_one_period_map_used"] is False


def test_direct_event_derivative_formula_has_the_phase_correction() -> None:
    theorem = _payload()["certificate"]["selected_event_derivative_theorem"]
    assert "ell=Dg_Y=ell_0" in theorem["setting"]
    assert "a=ell(v)!=0" in theorem["setting"]
    assert "D_y Psi" in theorem["variational_operator"]
    assert theorem["direct_event_time_derivative"] == (
        "D T(Y_*)[h]=-ell(U_Y(2P_orb,0)h)/a"
    )
    assert theorem["event_projection"] == "Pi=I-v*ell/a"
    assert theorem["direct_reduced_derivative"] == (
        "D Q_Y(Y_*)=Pi U_Y(2P_orb,0)|_{Sigma_0}"
    )
    assert theorem["first_or_ordinal_return_needed"] is False


def test_periodic_cocycle_is_forward_only_and_exact() -> None:
    identity = _payload()["certificate"][
        "periodic_cocycle_projection_identity"
    ]
    assert identity["one_period_monodromy"] == "M=U_Y(P_orb,0)"
    assert "U_Y(2P_orb,P_orb)=U_Y(P_orb,0)=M" in identity[
        "periodic_cocycle"
    ]
    assert "U_Y(2P_orb,0)=M^2" in identity["periodic_cocycle"]
    assert identity["phase_tangent"] == "M v=v"
    assert "Pi_{P_orb}=Pi_{2P_orb}=Pi" in identity[
        "periodic_projection"
    ]
    assert identity["invertibility_of_semiflow_used"] is False
    assert identity["nonlinear_one_period_return_used"] is False


def test_middle_event_projection_vanishes_on_the_phase_tangent() -> None:
    identity = _payload()["certificate"][
        "periodic_cocycle_projection_identity"
    ]
    assert "(I-Pi)y=v*ell(y)/a" in identity["projection_kernel"]
    assert "Pi M v=0" in identity["projection_kernel"]
    assert "Pi M Pi M h=Pi M^2 h" in identity["square_calculation"]
    assert "Pi M(I-Pi)M h=0" in identity["square_calculation"]


def test_reduced_derivative_is_a_squared_but_map_is_not_p_squared() -> None:
    bridge = _payload()["certificate"][
        "reduced_physical_derivative_identification"
    ]
    assert bridge["stage4l_operator"] == "A=Pi M|_{Sigma_0}"
    assert bridge["direct_two_period_operator"] == (
        "D Q_Y(Y_*)=Pi M^2|_{Sigma_0}"
    )
    assert bridge["exact_identity"] == "D Q_Y(Y_*)=A^2"
    assert "D Q_X(Iota(Y_*))" in bridge[
        "compatible_full_lift_intertwining"
    ]
    assert bridge["full_X_literal_A_squared"] is False
    assert bridge["identity_is_linearization_not_map_equality"] is True
    assert bridge["Q_equals_P_squared"] is False
    assert bridge["nonlinear_one_period_P_required"] is False


def test_coordinate_derivative_is_conjugate_not_literally_a_squared() -> None:
    bridge = _payload()["certificate"]["coordinate_conjugacy"]
    assert bridge["chart_differentials"] == (
        "D j(0)=J and D chi(Y_*)=J^{-1}"
    )
    assert bridge["exact_identity"] == "D Q_coord(0)=J^{-1} A^2 J"
    assert "through J" in bridge[
        "literal_A_squared_only_after_identification"
    ]
    assert bridge["arbitrary_product_norm_isometry_claimed"] is False
    assert bridge["pullback_norm"] == "||z||_J:=||Jz||_Y"


def test_fixed_splitting_and_rates_transfer_in_the_declared_norm() -> None:
    transfer = _payload()["certificate"]["linear_split_and_rate_transfer"]
    assert "Sigma_0=E_s direct_sum E_u" in transfer[
        "physical_fixed_splitting"
    ]
    assert transfer["stable_rate_upper"] == STABLE_RATE_TWO == "0.01"
    assert "K_s=1" in transfer["stable_power_bound"]
    assert transfer["unstable_backward_rate_upper"] == (
        UNSTABLE_BACKWARD_RATE_TWO
    )
    assert "K_u=1" in transfer["unstable_backward_power_bound"]
    assert transfer["coordinate_spaces"] == (
        "J^{-1}E_s direct_sum J^{-1}E_u"
    )
    assert "pullback norm" in transfer["coordinate_rate_norm"]
    assert transfer["arbitrary_coordinate_product_norm_rate"] is None


def test_six_semantic_bindings_are_registered() -> None:
    ledger = _payload()["certificate"]["semantic_binding_ledger"]
    assert ledger["all_bindings_required"] is True
    assert "same source-bound periodic orbit in Y" in ledger[
        "same_exact_center"
    ]
    assert "same exact period" in ledger["same_period"]
    assert "U_Y=D_y Psi" in ledger[
        "same_semiflow_and_variational_cocycle"
    ]
    assert "pi/Iota factorisation" in ledger[
        "same_semiflow_and_variational_cocycle"
    ]
    assert "identical physical phase-zero voltage event" in ledger[
        "same_event_and_section"
    ]
    for term in ("U(2P,P)=U(P,0)", "U(P,0)v=v", "Pi_P=Pi_2P"):
        assert term in ledger["periodic_standard_identities"]
    assert "J^{-1}A^2J" in ledger["chart_type_binding"]


def test_proved_conditional_open_ledger_is_fail_closed() -> None:
    ledger = _payload()["certificate"]["proved_conditional_open_ledger"]
    assert set(ledger) == {"proved", "conditional", "open"}
    assert any("D Q_Y(Y_*)=A^2" in item for item in ledger["proved"])
    assert any("D Q_X(Iota(Y_*))" in item for item in ledger["proved"])
    assert any("J^{-1}A^2J" in item for item in ledger["proved"])
    assert any("pullback J norm" in item for item in ledger["conditional"])
    assert any("Q=P^2" in item for item in ledger["open"])
    assert any("self-map" in item for item in ledger["open"])


def test_scope_promotes_only_center_linear_bridge_outputs() -> None:
    scope = _payload()["certificate"]["scope_boundary"]
    assert scope == {
        "direct_selected_C2_map_on_qualitative_scaled_ball": True,
        "center_fixed_point_and_two_period_time": True,
        "reduced_Y_derivative_equals_A_squared": True,
        "compatible_full_X_derivative_intertwining": True,
        "coordinate_derivative_conjugate_to_A_squared": True,
        "fixed_linear_split_and_rates_at_center": True,
        "Q_equals_nonlinear_P_squared": False,
        "same_scaled_ball_self_map": False,
        "first_return_or_event_ordinal": False,
        "uniform_Hessian_blocks_or_quantitative_stable_graph": False,
        "periodic_orbit_stable_set_germ": False,
        "pulse_onset_routing_or_safety": False,
    }


def test_claim_ledger_is_exact() -> None:
    claims = _payload()["certificate"]["claim_status"]
    assert set(claims) == set(TRUE_FLAGS) | set(FALSE_FLAGS)
    assert all(claims[name] is True for name in TRUE_FLAGS)
    assert all(claims[name] is False for name in FALSE_FLAGS)
    assert len(TRUE_FLAGS) == 22
    assert len(FALSE_FLAGS) == 15


@pytest.mark.parametrize(
    "flag",
    [
        "direct_selected_map_equals_square_of_nonlinear_one_period_map_validated",
        "coordinate_derivative_literally_equals_a_squared_without_identification",
        "same_scaled_anisotropic_ball_self_map_validated",
        "first_positive_return_validated",
        "periodic_orbit_stable_set_germ_identification_validated",
    ],
)
def test_promoting_excluded_claim_fails_after_rehash(flag: str) -> None:
    payload = deepcopy(_payload())
    payload["certificate"]["claim_status"][flag] = True
    _refresh_digests(payload)
    with pytest.raises(ValueError):
        validate_direct_two_period_derivative_result(payload, REPOSITORY)


def test_demoting_physical_derivative_identity_fails_after_rehash() -> None:
    payload = deepcopy(_payload())
    payload["certificate"]["claim_status"][
        "reduced_physical_direct_two_period_derivative_equals_a_squared_proved"
    ] = False
    _refresh_digests(payload)
    with pytest.raises(ValueError):
        validate_direct_two_period_derivative_result(payload, REPOSITORY)


def test_replacing_conjugacy_by_literal_equality_fails_after_rehash() -> None:
    payload = deepcopy(_payload())
    payload["certificate"]["coordinate_conjugacy"]["exact_identity"] = (
        "D Q_coord(0)=A^2"
    )
    _refresh_digests(payload)
    with pytest.raises(ValueError):
        validate_direct_two_period_derivative_result(payload, REPOSITORY)


def test_parent_digest_mutation_fails() -> None:
    payload = deepcopy(_payload())
    relative = next(iter(parent_result_sha256()))
    payload["manifest"]["parent_result_sha256"][relative] = "0" * 64
    with pytest.raises(ValueError):
        validate_direct_two_period_derivative_result(payload, REPOSITORY)


def test_source_digest_mutation_fails() -> None:
    payload = deepcopy(_payload())
    payload["manifest"]["source_sha256"][NOTE_RELATIVE_PATH] = "0" * 64
    with pytest.raises(ValueError):
        validate_direct_two_period_derivative_result(payload, REPOSITORY)


def test_extra_outer_key_fails() -> None:
    payload = deepcopy(_payload())
    payload["unexpected"] = None
    with pytest.raises(ValueError):
        validate_direct_two_period_derivative_result(payload, REPOSITORY)


def test_generator_uses_fsync_and_atomic_replace() -> None:
    tree = ast.parse(
        (REPOSITORY / GENERATOR_RELATIVE_PATH).read_text(encoding="utf-8")
    )
    attributes = {
        node.attr for node in ast.walk(tree) if isinstance(node, ast.Attribute)
    }
    assert "fsync" in attributes
    assert "replace" in attributes


def test_every_new_filename_contains_direct_two_period_derivative_stage4t() -> None:
    assert len(SOURCE_MANIFEST) == 4
    for relative in (*SOURCE_MANIFEST, RESULT_RELATIVE_PATH):
        assert "direct_two_period_derivative_stage4t" in Path(relative).name


def test_no_existing_stage4s_or_flagship_file_is_in_source_manifest() -> None:
    for relative in SOURCE_MANIFEST:
        assert "leaky_inner_stage4s" not in Path(relative).name
        assert not relative.startswith("manuscript/")
        assert Path(relative).name != "README.md"
