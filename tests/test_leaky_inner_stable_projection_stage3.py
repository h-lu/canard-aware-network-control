from __future__ import annotations

from copy import deepcopy
from decimal import Decimal
from hashlib import sha256
import json
from pathlib import Path

import pytest

from canard_control.leaky_inner_stable_projection_stage3 import (
    FALSE_FLAGS,
    RESULT_RELATIVE_PATH,
    TRUE_FLAGS,
    validate_stage3_stable_projection_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]
EXPECTED_RESULT_SHA256: str | None = (
    "9ea776a6e627745ded7f7023523999bfbd29a0be4878172c76512d623146e2ea"
)


def _payload() -> dict[str, object]:
    return json.loads(
        (REPOSITORY / RESULT_RELATIVE_PATH).read_text(encoding="utf-8")
    )


def test_registered_stage3_result_is_source_bound() -> None:
    assert EXPECTED_RESULT_SHA256 is not None
    payload = _payload()
    validate_stage3_stable_projection_result(payload, REPOSITORY)
    assert sha256(
        (REPOSITORY / RESULT_RELATIVE_PATH).read_bytes()
    ).hexdigest() == EXPECTED_RESULT_SHA256


def test_root_and_eigencolumn_are_full_operator_enclosures() -> None:
    certificate = _payload()["certificate"]
    root = certificate["root_bracket"]
    assert Decimal(root["root_real_lower"]) < Decimal(
        root["root_real_upper"]
    )
    assert Decimal(
        root["lower_endpoint"]["full_effective_hamiltonian_real_upper"]
    ) < 0
    assert Decimal(
        root["upper_endpoint"]["full_effective_hamiltonian_real_lower"]
    ) > 0
    eigen = certificate["eigencolumn_enclosure"]
    assert eigen["full_infinite_grushin_eigencolumn_enclosed"]
    assert Decimal(eigen["full_grushin_contraction_upper"]) < Decimal("0.095")
    assert Decimal(
        eigen["exact_normalized_eigencolumn_split_wiener_error_upper"]
    ) < Decimal("3e-8")


def test_route_c_component_dominance_proves_only_a_projection_lower_bound() -> None:
    certificate = _payload()["certificate"]
    component = certificate["route_c_component_audit"]
    assert Decimal(
        component["section_voltage_component_at_test_time_abs_lower"]
    ) > Decimal(component["section_recovery_component_abs_upper"])
    assert Decimal(
        component["voltage_minus_recovery_dominance_margin_lower"]
    ) > Decimal("0.0213")
    geometry = certificate["projection_geometry"]
    assert geometry["stable_projection_norm_lower"] == "2"
    assert geometry["stable_projection_norm_lower_two_validated"]
    assert geometry["stable_projection_norm_upper"] is None
    assert geometry["unstable_projection_norm_upper"] is None


def test_c_n_10_no_go_is_not_an_intrinsic_norm_no_go() -> None:
    no_go = _payload()["certificate"]["scalar_majorant_no_go"]
    assert Decimal(no_go["selected_beta_c_n_10_lhs_lower"]) > 2500
    assert Decimal(no_go["all_beta_c_n_10_lhs_infimum_lower"]) > 2500
    assert Decimal(
        no_go["selected_beta_necessary_c_n_ceiling_upper"]
    ) < Decimal("5.43")
    assert Decimal(
        no_go["all_beta_necessary_c_n_ceiling_supremum_upper"]
    ) < Decimal("6.21")
    assert no_go["actual_return_map_c_n_upper"] is None
    assert not no_go["current_history_norm_intrinsically_impossible"]


def test_adapted_norm_keeps_the_nonlinear_tradeoff_explicit() -> None:
    audit = _payload()["certificate"]["adapted_splitting_norm_audit"]
    assert audit["projection_norms_in_direct_sum_norm"] == (
        "p_s=p_u=1 exactly"
    )
    assert "p_s_old+p_u_old" in audit["black_box_nonlinear_transfer"]
    assert audit["weighted_black_box_factor_minimized_at_lambda_one"]
    assert not audit["projection_isometry_alone_improves_scalar_gate"]
    assert not audit["direct_projected_return_c2_blocks_validated"]
    assert not audit["adapted_splitting_norm_scalar_gate_validated"]


def test_claim_ledger_separates_proof_diagnostic_and_open_gates() -> None:
    certificate = _payload()["certificate"]
    claims = certificate["claim_status"]
    assert all(claims[name] for name in TRUE_FLAGS)
    assert all(not claims[name] for name in FALSE_FLAGS)
    diagnostic = certificate["binary_diagnostic"]
    assert not diagnostic["binary_projection_diagnostic_promoted_to_proof"]
    assert len(diagnostic["grid_rows"]) == 3
    assert Decimal(
        diagnostic["grid_rows"][-1]["stable_projection_norm_binary64"]
    ) > Decimal("2.4")


@pytest.mark.parametrize(
    ("path", "value"),
    (
        (("certificate", "projection_geometry", "stable_projection_norm_upper"), "2.5"),
        (("certificate", "scalar_majorant_no_go", "actual_return_map_c_n_upper"), "5"),
        (("certificate", "claim_status", "physical_pulse_onset_validated"), True),
        (("certificate", "binary_diagnostic", "binary_projection_diagnostic_promoted_to_proof"), True),
    ),
)
def test_hostile_promotions_are_rejected(
    path: tuple[str, ...], value: object
) -> None:
    payload = deepcopy(_payload())
    target = payload
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value
    with pytest.raises(ValueError):
        validate_stage3_stable_projection_result(payload, REPOSITORY)
