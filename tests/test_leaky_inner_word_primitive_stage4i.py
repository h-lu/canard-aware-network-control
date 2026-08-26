from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path

import gmpy2
import pytest

from canard_control.leaky_inner_word_primitive_stage4i import (
    FALSE_FLAGS,
    NOTE_RELATIVE_PATH,
    RESULT_RELATIVE_PATH,
    TRUE_FLAGS,
    canonical_sha256,
    validate_stage4i_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]
EXPECTED_RESULT_SHA256 = (
    "1248e9d95444f3cc12565c1e11b4bbeab3d4a9a7bb8922893e38b1ffa439f73e"
)


def _payload() -> dict[str, object]:
    return json.loads(
        (REPOSITORY / RESULT_RELATIVE_PATH).read_text(encoding="utf-8")
    )


def test_registered_stage4i_result_is_source_bound() -> None:
    assert EXPECTED_RESULT_SHA256 is not None
    payload = _payload()
    validate_stage4i_result(payload, REPOSITORY)
    assert sha256(
        (REPOSITORY / RESULT_RELATIVE_PATH).read_bytes()
    ).hexdigest() == EXPECTED_RESULT_SHA256


def test_all_five_primitive_residuals_are_directed_and_small() -> None:
    residual = _payload()["artifact"]["directed_residual_certificate"]
    assert residual["precision_bits"] == 192
    assert residual["cell_count"] == 1042
    assert residual["analytic_tails_and_trimmed_coefficients_added"]
    assert not residual["binary_mesh_spread_used_as_error"]
    assert set(residual["maximum_residual_upper"]) == {
        "F",
        "G",
        "C0",
        "C1",
        "C00",
    }
    assert max(
        gmpy2.mpq(value)
        for value in residual["maximum_residual_upper"].values()
    ) < gmpy2.mpq("8e-7")
    assert gmpy2.mpq(
        residual["maximum_guide_inverse_defect_infinity_upper"]
    ) < gmpy2.mpq("2e-8")
    assert residual["intercell_guide_jumps_added"]
    assert max(
        gmpy2.mpq(value)
        for value in residual[
            "maximum_intercell_guide_jump_infinity_upper"
        ].values()
    ) < gmpy2.mpq("1e-12")


def test_raw_frame_no_go_and_moving_frame_repair_are_both_recorded() -> None:
    tubes = _payload()["artifact"]["directed_primitive_error_tubes"]
    raw = tubes["raw_physical_frame_gronwall_no_go"]
    assert not raw["usable_for_signed_stable_certificate"]
    assert gmpy2.mpq(raw["maximum_error_radius_upper"]["F"]) > 10**6
    assert gmpy2.mpq(raw["maximum_error_radius_upper"]["G"]) > 10**6
    moving = tubes["maximum_error_radius_upper"]
    assert tubes["error_radius_norm_by_field"] == {
        "F": "matrix_infinity_norm",
        "G": "matrix_infinity_norm",
        "C0": "maximum_entry_modulus",
        "C1": "maximum_entry_modulus",
        "C00": "maximum_entry_modulus",
    }
    assert gmpy2.mpq(moving["F"]) < gmpy2.mpq("5e-4")
    assert gmpy2.mpq(moving["G"]) < gmpy2.mpq("3e-4")
    assert gmpy2.mpq(moving["C0"]) < gmpy2.mpq("2e-6")
    assert gmpy2.mpq(moving["C1"]) < gmpy2.mpq("2e-6")
    assert gmpy2.mpq(moving["C00"]) < gmpy2.mpq("4e-11")


def test_primitive_budget_fits_but_full_signed_gate_remains_open() -> None:
    artifact = _payload()["artifact"]
    induced = artifact["induced_measure_error_diagnostic"]
    status = artifact["stable_power_ingress_status"]
    assert gmpy2.mpq(
        induced["coarse_primitive_induced_event_measure_error_upper"]
    ) < gmpy2.mpq("0.002")
    assert induced["double_delay_history_support_length_upper"] == (
        "8.9442719099991592"
    )
    assert status["primitive_budget_below_stage4h_numerical_margin"]
    assert not status[
        "primitive_budget_is_sufficient_for_full_stable_power_proof"
    ]
    assert status["phase_fixed_one_step_stable_map_norm_upper"] is None
    assert status["stable_power_constant_upper"] is None
    assert not status["k_s_equals_one_validated"]
    assert "common signed density" in status["next_exact_object"]


def test_claim_ledger_preserves_stable_power_and_graph_scope() -> None:
    claims = _payload()["artifact"]["claim_status"]
    assert all(claims[name] for name in TRUE_FLAGS)
    assert all(not claims[name] for name in FALSE_FLAGS)


def test_note_names_the_projected_error_mechanism() -> None:
    prose = " ".join(
        (REPOSITORY / NOTE_RELATIVE_PATH).read_text(encoding="utf-8").split()
    )
    assert "strictly rejected" in prose
    assert "common density" in prose
    assert "bordered stable inverse" in prose
    assert "unstable direction is absent" in prose


@pytest.mark.parametrize(
    ("path", "value"),
    (
        (
            (
                "artifact",
                "directed_residual_certificate",
                "binary_mesh_spread_used_as_error",
            ),
            True,
        ),
        (
            (
                "artifact",
                "directed_residual_certificate",
                "cumulative_moving_frame_log_budget_upper",
            ),
            "100",
        ),
        (
            (
                "artifact",
                "directed_primitive_error_tubes",
                "raw_physical_frame_gronwall_no_go",
                "usable_for_signed_stable_certificate",
            ),
            True,
        ),
        (
            (
                "artifact",
                "directed_primitive_error_tubes",
                "maximum_error_radius_upper",
                "F",
            ),
            "-1",
        ),
        (
            (
                "artifact",
                "directed_primitive_error_tubes",
                "final_error_radius_upper",
                "F",
            ),
            "0.1",
        ),
        (
            (
                "artifact",
                "induced_measure_error_diagnostic",
                "atom_error_upper",
            ),
            "100",
        ),
        (
            (
                "artifact",
                "induced_measure_error_diagnostic",
                "event_projection_factor_upper",
            ),
            "1",
        ),
        (
            (
                "artifact",
                "induced_measure_error_diagnostic",
                "coarse_primitive_induced_event_measure_error_upper",
            ),
            "0.01",
        ),
        (
            (
                "artifact",
                "stable_power_ingress_status",
                "primitive_budget_below_stage4h_numerical_margin",
            ),
            False,
        ),
        (
            (
                "artifact",
                "stable_power_ingress_status",
                "phase_fixed_one_step_stable_map_norm_upper",
            ),
            "0.01",
        ),
        (
            (
                "artifact",
                "stable_power_ingress_status",
                "k_s_equals_one_validated",
            ),
            True,
        ),
        (
            (
                "artifact",
                "claim_status",
                "split_return_tube_validated",
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
    payload["manifest"]["artifact_sha256"] = canonical_sha256(
        payload["artifact"]
    )
    with pytest.raises(ValueError):
        validate_stage4i_result(payload, REPOSITORY)


def test_missing_radius_is_semantically_rejected_after_digest_refresh() -> None:
    payload = deepcopy(_payload())
    del payload["artifact"]["directed_primitive_error_tubes"][
        "maximum_error_radius_upper"
    ]["C00"]
    payload["manifest"]["artifact_sha256"] = canonical_sha256(
        payload["artifact"]
    )
    with pytest.raises(ValueError):
        validate_stage4i_result(payload, REPOSITORY)


def test_parent_center_and_rate_cannot_be_consistently_rebased() -> None:
    payload = deepcopy(_payload())
    status = payload["artifact"]["stable_power_ingress_status"]
    status["stage4h_sampled_signed_center"] = "0.1"
    status["declared_rate_rho_s"] = "0.2"
    status["coarse_primitive_error_plus_sampled_center"] = (
        "0.10146354618385727"
    )
    status["primitive_budget_below_stage4h_numerical_margin"] = True
    payload["manifest"]["artifact_sha256"] = canonical_sha256(
        payload["artifact"]
    )
    with pytest.raises(ValueError):
        validate_stage4i_result(payload, REPOSITORY)
