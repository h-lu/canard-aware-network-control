from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path

import gmpy2
import pytest

from canard_control.leaky_shared_yqq_deflation_stage4e import (
    FALSE_FLAGS,
    NOTE_RELATIVE_PATH,
    RESULT_RELATIVE_PATH,
    TRUE_FLAGS,
    validate_stage4e_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]
EXPECTED_RESULT_SHA256: str | None = (
    "ccdd6023f911e97785ec6f8be97b84d725d6af9f5051e1da602380d225e47acc"
)


def _payload() -> dict[str, object]:
    return json.loads(
        (REPOSITORY / RESULT_RELATIVE_PATH).read_text(encoding="utf-8")
    )


def test_registered_stage4e_result_is_source_bound() -> None:
    assert EXPECTED_RESULT_SHA256 is not None
    payload = _payload()
    validate_stage4e_result(payload, REPOSITORY)
    assert sha256(
        (REPOSITORY / RESULT_RELATIVE_PATH).read_bytes()
    ).hexdigest() == EXPECTED_RESULT_SHA256


def test_physical_time_vqq_tube_is_directed() -> None:
    artifact = _payload()["artifact"]
    grid = artifact["physical_time_grid"]
    residual = artifact["directed_vqq_residual"]
    tube = artifact["directed_vqq_tube"]
    assert grid["tau0_aligned_cell_count"] == 512
    assert grid["tau1_aligned_cell_count"] == 640
    assert grid["full_cell_count_plus_final_short_cell"] == 1042
    assert residual["taylor_bernstein_outward_mpfr"]
    assert residual["omitted_coefficients_added_before_norm"]
    assert tube["delayed_source_radii_propagated_cell_by_cell"]
    assert not tube["mesh_spread_used_as_error"]
    assert gmpy2.mpq(tube["maximum_p_radius_upper"]) < gmpy2.mpq("0.0082")


def test_correlated_action_precedes_norm_and_closes_base_target() -> None:
    artifact = _payload()["artifact"]
    action = artifact["continuous_history_correlated_deflation"]
    base = artifact["base_orbit_stable_output_uu"]
    assert action["same_adjoint_coefficients_in_numerator_and_denominator"]
    assert not action["independent_num_den_triangle_bound_used"]
    assert "Y_qq-c*q" in action["quotient_residual_identity"]
    assert gmpy2.mpq(
        action["center_adjoint_inhomogeneous_identity_defect_upper"]
    ) > 0
    assert gmpy2.mpq(action["history_measure_difference_upper"]) > 0
    assert gmpy2.mpq(action["adjoint_density_basis_shift_upper"]) > 0
    assert gmpy2.mpq(action["vqq_seam_action_error_upper"]) > 0
    assert gmpy2.mpq(action["total_correlated_action_error_upper"]) < gmpy2.mpq("8e-6")
    assert base["strictly_below_twelve"]
    assert not base["uniform_split_ball_statement"]
    assert gmpy2.mpq(base["normalized_stable_output_uu_upper"]) < 12
    assert gmpy2.mpq(base["unscaled_target_margin_lower"]) > 0


def test_stage4b_graph_claims_remain_conditional() -> None:
    artifact = _payload()["artifact"]
    conditional = artifact["stage4b_conditional_substitution"]
    remaining = artifact["exact_remaining_gates"]
    assert conditional["conditional_matrix_closes"]
    assert conditional["stage4e_value_is_not_a_uniform_block_bound"]
    assert not conditional["strict_stage4b_certificate_closes"]
    assert not remaining["uniform_ball_block_bounds_validated"]
    assert not remaining["stable_power_validated"]
    assert not remaining["split_return_tube_validated"]
    assert not remaining["six_block_graph_transform_validated"]


def test_claim_ledger_separates_base_orbit_from_graph_theorem() -> None:
    claims = _payload()["artifact"]["claim_status"]
    assert all(claims[name] for name in TRUE_FLAGS)
    assert all(not claims[name] for name in FALSE_FLAGS)


def test_note_states_the_uniform_gap() -> None:
    prose = " ".join(
        (REPOSITORY / NOTE_RELATIVE_PATH).read_text(encoding="utf-8").split()
    )
    assert "at the periodic base orbit" in prose
    assert "This is not yet the quantitative local-stable-graph theorem" in prose
    assert "five Stage-4B design targets" in prose
    assert "conditional" in prose


@pytest.mark.parametrize(
    ("path", "value"),
    (
        (("artifact", "directed_vqq_tube", "mesh_spread_used_as_error"), True),
        (
            (
                "artifact",
                "base_orbit_stable_output_uu",
                "normalized_stable_output_uu_upper",
            ),
            "12",
        ),
        (
            (
                "artifact",
                "continuous_history_correlated_deflation",
                "center_adjoint_inhomogeneous_identity_defect_upper",
            ),
            "0",
        ),
        (
            (
                "artifact",
                "continuous_history_correlated_deflation",
                "history_measure_difference_upper",
            ),
            "0",
        ),
        (
            (
                "artifact",
                "base_orbit_stable_output_uu",
                "uniform_split_ball_statement",
            ),
            True,
        ),
        (
            (
                "artifact",
                "stage4b_conditional_substitution",
                "strict_stage4b_certificate_closes",
            ),
            True,
        ),
        (
            (
                "artifact",
                "claim_status",
                "graph_radius_1p7e_minus_3_validated",
            ),
            True,
        ),
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
        validate_stage4e_result(payload, REPOSITORY)
