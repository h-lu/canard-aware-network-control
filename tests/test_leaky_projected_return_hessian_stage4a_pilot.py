from __future__ import annotations

from copy import deepcopy
from decimal import Decimal
from hashlib import sha256
import json
from pathlib import Path

import pytest

from canard_control.leaky_projected_return_hessian_stage4a_pilot import (
    BLOCK_NAMES,
    DEFAULT_STEP_COUNTS,
    FALSE_FLAGS,
    NOTE_RELATIVE_PATH,
    RESULT_RELATIVE_PATH,
    TRUE_FLAGS,
    validate_stage4a_pilot_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]
EXPECTED_RESULT_SHA256: str | None = (
    "b9308d01137559f5b88e42f7120b6eb01490aaa6bda3ac7b6eed2fd2ce5421c7"
)


def _payload() -> dict[str, object]:
    return json.loads(
        (REPOSITORY / RESULT_RELATIVE_PATH).read_text(encoding="utf-8")
    )


def test_registered_stage4a_result_is_source_bound() -> None:
    assert EXPECTED_RESULT_SHA256 is not None
    payload = _payload()
    validate_stage4a_pilot_result(payload, REPOSITORY)
    assert sha256(
        (REPOSITORY / RESULT_RELATIVE_PATH).read_bytes()
    ).hexdigest() == EXPECTED_RESULT_SHA256


def test_three_mesh_pilot_converges_to_the_known_unstable_split() -> None:
    rows = _payload()["artifact"]["mesh_rows"]
    assert [row["step_count"] for row in rows] == list(DEFAULT_STEP_COUNTS)
    multipliers = [
        Decimal(row["eigensplit"]["unstable_multiplier"]) for row in rows
    ]
    assert all(Decimal("2.0104") < value < Decimal("2.0105") for value in multipliers)
    assert abs(multipliers[-1] - multipliers[-2]) < Decimal("7e-8")
    final = rows[-1]
    assert Decimal(final["eigensplit"]["stable_projection_linf_norm"]) > Decimal(
        "2.4"
    )
    assert Decimal(final["eigensplit"]["unstable_projection_linf_norm"]) > Decimal(
        "1.4"
    )
    assert Decimal(final["return_hessian_symmetry_defect_inf"]) < Decimal(
        "1e-17"
    )


def test_k_s_one_candidate_is_a_split_finite_section_statement_only() -> None:
    power = _payload()["artifact"]["mesh_rows"][-1]["stable_power_pilot"]
    assert power["finite_section_all_power_k_s_candidate"] == "1"
    assert power["one_step_below_declared_rho"]
    assert Decimal(
        power["finite_section_one_step_restriction_candidate"]
    ) < Decimal("0.0045")
    assert not power["all_powers_validated"]
    ingress = _payload()["artifact"]["strict_certificate_ingress"]
    assert ingress["stable_power_constant_upper"] is None


def test_all_six_blocks_and_largest_block_are_reported() -> None:
    artifact = _payload()["artifact"]
    final_blocks = artifact["mesh_rows"][-1][
        "projected_hessian_block_pilot"
    ]
    assert set(final_blocks) == set(BLOCK_NAMES)
    assert Decimal(final_blocks["unstable_output_uu_upper"]) > Decimal("26.19")
    assert Decimal(final_blocks["stable_output_uu_upper"]) > Decimal("7.26")
    envelope = artifact["refinement_pilot_envelope"]
    assert envelope["largest_block"]["name"] == "unstable_output_uu_upper"
    assert Decimal(envelope["largest_block"]["candidate_upper"]) > Decimal(
        "26.196"
    )
    assert not envelope["continuous_history_upper_bound"]


def test_matrix_pilot_closes_but_is_not_promoted() -> None:
    artifact = _payload()["artifact"]
    evaluation = artifact["stage4_matrix_pilot_evaluation"]
    assert evaluation["contraction_closes"]
    assert evaluation["self_map_closes"]
    assert evaluation["split_ball_contains_graph_box"]
    assert evaluation["graph_certificate_closes"]
    assert Decimal(evaluation["perron_root_upper"]) < Decimal("0.05")
    assert Decimal(evaluation["derivative_lipschitz_matrix_upper"]["m_su"]) > 1
    assert Decimal(evaluation["derivative_lipschitz_matrix_upper"]["m_us"]) < Decimal(
        "0.001"
    )
    ingress = artifact["strict_certificate_ingress"]
    assert not ingress["pilot_values_promoted"]
    assert all(ingress[name] is None for name in BLOCK_NAMES)
    claims = artifact["claim_status"]
    assert all(claims[name] for name in TRUE_FLAGS)
    assert all(not claims[name] for name in FALSE_FLAGS)


def test_sensitivity_identifies_stable_output_uu_as_the_tight_block() -> None:
    sensitivity = _payload()["artifact"]["pilot_sensitivity"]
    thresholds = sensitivity["isolated_block_thresholds"]
    stable_uu = Decimal(
        thresholds["stable_output_uu_upper"]["closing_multiplier_lower"]
    )
    unstable_uu = Decimal(
        thresholds["unstable_output_uu_upper"]["closing_multiplier_lower"]
    )
    common = Decimal(
        sensitivity["common_six_block_threshold"]["closing_multiplier_lower"]
    )
    assert Decimal("1.74") < stable_uu < Decimal("1.76")
    assert unstable_uu > 44
    assert Decimal("1.72") < common < Decimal("1.73")
    assert sensitivity["tightness_order"][0] == "stable_output_uu_upper"
    assert sensitivity["baseline_is_nonrigorous"]
    assert not sensitivity["thresholds_are_theorem_tolerances"]


def test_note_explains_projection_norm_and_k_s_are_different() -> None:
    text = (REPOSITORY / NOTE_RELATIVE_PATH).read_text(encoding="utf-8")
    assert "does not contradict the old-norm result" in text
    assert "ambient projection" in text
    assert "already split stable coordinate" in text
    assert "Every theorem flag nevertheless remains false" in text


@pytest.mark.parametrize(
    ("path", "value"),
    (
        (
            (
                "artifact",
                "strict_certificate_ingress",
                "stable_power_constant_upper",
            ),
            "1",
        ),
        (
            (
                "artifact",
                "strict_certificate_ingress",
                "stable_output_uu_upper",
            ),
            "8",
        ),
        (
            (
                "artifact",
                "refinement_pilot_envelope",
                "split_return_ball_radius_validated",
            ),
            True,
        ),
        (
            (
                "artifact",
                "claim_status",
                "matrix_majorant_pilot_promoted_to_proof",
            ),
            True,
        ),
        (
            (
                "artifact",
                "claim_status",
                "inner_local_stable_graph_quantitatively_validated",
            ),
            True,
        ),
    ),
)
def test_hostile_pilot_promotions_are_rejected(
    path: tuple[str, ...], value: object
) -> None:
    payload = deepcopy(_payload())
    target = payload
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value
    with pytest.raises(ValueError):
        validate_stage4a_pilot_result(payload, REPOSITORY)
