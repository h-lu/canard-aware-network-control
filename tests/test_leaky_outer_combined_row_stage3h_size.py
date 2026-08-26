from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path

import pytest

import canard_control.leaky_outer_combined_row_stage3h_size as stage3h
from canard_control.leaky_outer_combined_row_stage3h_size import (
    CONCLUSION,
    EVENT_SEAM_PATCH_COUNT,
    FALSE_FLAGS,
    LOCAL_PATCH_COUNT,
    ONE_SIDED_VOLTAGE_ROW_EVALUATION_COUNT,
    ORDINARY_RECTANGLE_COUNT,
    RECOVERY_ONE_DIMENSIONAL_PATCH_COUNT,
    RESULT_RELATIVE_PATH,
    ROW_SCOPE,
    STAGE3G_CANDIDATE_ERROR_SEMANTICS,
    STAGE3G_RESULT_RELATIVE_PATH,
    STAGE3G_RESULT_SHA256,
    TERMINAL_CLIPPED_RECTANGLE_COUNT,
    TERMINAL_LINE_ONE_SIDED_EVENT_PATCH_COUNT,
    TRUE_FLAGS,
    TWO_SIDED_EVENT_SEAM_PATCH_COUNT,
    _load_parent,
    _frontier_rows_from_size_records,
    _require_unique_disjoint_flags,
    _validate_parent_artifact_lock,
    canonical_sha256,
    validate_outer_combined_row_stage3h_size_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def payload() -> dict:
    return json.loads((REPOSITORY / RESULT_RELATIVE_PATH).read_text())


def _refresh_certificate_digest(value: dict) -> None:
    value["manifest"]["certificate_sha256"] = canonical_sha256(
        value["certificate"]
    )


def _reject_before_replay(
    changed: dict, monkeypatch: pytest.MonkeyPatch, match: str
) -> None:
    def forbidden(_: Path) -> object:
        raise AssertionError("an invalid Stage-3H payload reached full replay")

    monkeypatch.setattr(stage3h, "build_outer_combined_row_stage3h_size", forbidden)
    with pytest.raises(ValueError, match=match):
        validate_outer_combined_row_stage3h_size_result(changed, REPOSITORY)


def test_stage3g_v2_parent_is_exact_and_source_bound() -> None:
    path = REPOSITORY / STAGE3G_RESULT_RELATIVE_PATH
    assert sha256(path.read_bytes()).hexdigest() == STAGE3G_RESULT_SHA256
    parent = _load_parent(
        REPOSITORY, STAGE3G_RESULT_RELATIVE_PATH, STAGE3G_RESULT_SHA256
    )
    _validate_parent_artifact_lock(
        parent,
        REPOSITORY,
        label="Stage-3G",
        schema_id="leaky-outer-resolvent-stage3g-tensor-v2",
        result_relative_path=STAGE3G_RESULT_RELATIVE_PATH,
    )


def test_geometry_constants_are_complete_and_unique() -> None:
    assert ORDINARY_RECTANGLE_COUNT == 730
    assert TERMINAL_CLIPPED_RECTANGLE_COUNT == 40
    assert LOCAL_PATCH_COUNT == (730 + 40) * 4**2 == 12320
    assert EVENT_SEAM_PATCH_COUNT == 3080
    assert TWO_SIDED_EVENT_SEAM_PATCH_COUNT == 3000
    assert TERMINAL_LINE_ONE_SIDED_EVENT_PATCH_COUNT == 80
    assert ONE_SIDED_VOLTAGE_ROW_EVALUATION_COUNT == 15200
    assert RECOVERY_ONE_DIMENSIONAL_PATCH_COUNT == 48 * 4 == 192
    source = (REPOSITORY / stage3h.SOURCE_RELATIVE_PATH).read_text()
    assert source.count("TERMINAL_CLIPPED_RECTANGLE_COUNT = 40") == 1
    assert "TERMINAL_CLIPPED_RECTANGLE_COUNT = 20" not in source


def test_flag_registries_reject_duplicates_and_overlap() -> None:
    _require_unique_disjoint_flags(TRUE_FLAGS, FALSE_FLAGS)
    with pytest.raises(ValueError, match="true-flag.*duplicates"):
        _require_unique_disjoint_flags(("a", "a"), ("b",))
    with pytest.raises(ValueError, match="registries overlap"):
        _require_unique_disjoint_flags(("a",), ("a",))


def test_generator_validates_before_atomic_replace() -> None:
    source = (REPOSITORY / stage3h.GENERATOR_RELATIVE_PATH).read_text()
    validation = source.index("validate_outer_combined_row_stage3h_size_result(")
    temporary = source.index('temporary_path = result_path.with_suffix(".json.tmp")')
    replacement = source.index("temporary_path.replace(result_path)")
    assert validation < temporary < replacement


def test_frontier_formula_recomputes_from_serialized_strict_sizes() -> None:
    stage3g = json.loads((REPOSITORY / STAGE3G_RESULT_RELATIVE_PATH).read_text())
    stage3f = json.loads(
        (REPOSITORY / stage3h.STAGE3F_RESULT_RELATIVE_PATH).read_text()
    )
    stage2 = json.loads((REPOSITORY / stage3h.STAGE2_RESULT_RELATIVE_PATH).read_text())
    sizes = {
        "voltage_combined_p_uniform_upper": "41.483",
        "voltage_combined_p_voltage_component_upper": "11.985",
        "recovery_combined_p_uniform_upper": "1.178",
        "recovery_combined_p_voltage_component_upper": "0.254",
    }
    rows = _frontier_rows_from_size_records(
        sizes,
        stage3g["certificate"],
        stage3f["certificate"],
        stage2["certificate"],
    )
    assert (
        rows["voltage"]["conditional_total_if_center_TV_reserve_is_validated"]
        == "0.13889504881493858"
    )
    assert (
        rows["recovery"]["conditional_total_if_center_TV_reserve_is_validated"]
        == "0.012872561162318007"
    )
    assert rows["voltage"]["conditional_contraction_below_one"] is True
    assert rows["recovery"]["conditional_contraction_below_one"] is True


def test_complete_output_specific_cover(payload: dict) -> None:
    geometry = payload["certificate"]["chart_geometry"]
    assert geometry["ordinary_rectangle_count"] == 730
    assert geometry["terminal_clipped_rectangle_count"] == 40
    assert geometry["local_patch_count"] == 12320
    assert geometry["event_seam_patch_count"] == 3080
    assert geometry["two_sided_event_seam_patch_count"] == 3000
    assert geometry["terminal_line_one_sided_event_patch_count"] == 80
    assert geometry["one_sided_voltage_row_evaluation_count"] == 15200
    assert geometry["recovery_one_dimensional_patch_count"] == 192


def test_strict_combined_row_sizes_are_nonempty(payload: dict) -> None:
    sizes = payload["certificate"]["combined_row_size"]
    assert sizes["signed_center_subtraction_precedes_row_norm"]
    assert sizes["ratio_radius_paid_after_signed_center_subtraction"]
    assert (
        sizes["stage3g_resolvent_candidate_row_error_semantics"]
        == STAGE3G_CANDIDATE_ERROR_SEMANTICS
    )
    assert float(sizes["voltage_combined_p_uniform_upper"]) > 0
    assert float(sizes["voltage_combined_p_voltage_component_upper"]) > 0
    assert float(sizes["recovery_combined_p_uniform_upper"]) > 0
    assert float(sizes["recovery_combined_p_voltage_component_upper"]) > 0


def test_phase_remainders_are_present(payload: dict) -> None:
    phase = payload["certificate"]["phase_ratio_enclosures"]
    assert phase["fourier_cutoff"] == 128
    assert phase["taylor_degree"] == 24
    assert float(phase["voltage_local_ratio_radius_maximum_upper"]) >= 0
    assert float(phase["recovery_ratio_radius_upper"]) >= 0
    center_hex = phase["recovery_ratio_center_binary64_hex"]
    assert float.fromhex(center_hex).hex() == center_hex


def test_certificate_locks_center_guide_scope(payload: dict) -> None:
    certificate = payload["certificate"]
    assert certificate["row_scope"] == ROW_SCOPE
    assert "center-guide" in certificate["conclusion"]
    assert "exact-orbit" in certificate["conclusion"].lower()


def test_conditional_frontier_does_not_promote_c0(payload: dict) -> None:
    certificate = payload["certificate"]
    frontier = certificate["linear_transfer_frontier"]
    assert frontier["strict_sizes_validated"] is True
    assert frontier["continuous_center_TV_reserve_validated"] is False
    assert frontier[
        "conditional_only_until_center_TV_cell_integral_is_validated"
    ] is True
    assert certificate["transfer_errors"]["E_voltage"] is None
    assert certificate["transfer_errors"]["E_recovery"] is None
    assert certificate["transfer_gate"][
        "arbitrary_c0_linear_contraction_closes"
    ] is False


def test_claim_ledger_preserves_open_flags(payload: dict) -> None:
    claims = payload["certificate"]["claim_status"]
    assert set(claims) == set(TRUE_FLAGS + FALSE_FLAGS)
    assert all(claims[name] is True for name in TRUE_FLAGS)
    assert all(claims[name] is False for name in FALSE_FLAGS)


def test_result_replays_source_bound(payload: dict) -> None:
    validate_outer_combined_row_stage3h_size_result(payload, REPOSITORY)


def test_source_tampering_is_rejected(
    payload: dict, monkeypatch: pytest.MonkeyPatch
) -> None:
    changed = deepcopy(payload)
    source = next(iter(changed["manifest"]["source_sha256"]))
    changed["manifest"]["source_sha256"][source] = "0" * 64
    _reject_before_replay(changed, monkeypatch, "source changed")


def test_claim_promotion_is_rejected(
    payload: dict, monkeypatch: pytest.MonkeyPatch
) -> None:
    changed = deepcopy(payload)
    changed["certificate"]["claim_status"][
        "arbitrary_c0_linear_return_contraction_validated"
    ] = True
    _refresh_certificate_digest(changed)
    _reject_before_replay(changed, monkeypatch, "open Stage-3H claim")


def test_manifest_environment_and_parent_tampering_is_rejected_before_replay(
    payload: dict, monkeypatch: pytest.MonkeyPatch
) -> None:
    changed = deepcopy(payload)
    changed["manifest"]["environment"]["arb_precision_bits"] = 191
    _reject_before_replay(changed, monkeypatch, "environment changed")

    changed = deepcopy(payload)
    changed["certificate"]["parent_result_sha256"][
        STAGE3G_RESULT_RELATIVE_PATH
    ] = "0" * 64
    _refresh_certificate_digest(changed)
    _reject_before_replay(changed, monkeypatch, "parent digest map changed")


def test_coordinated_geometry_and_maximizer_tampering_is_rejected_before_replay(
    payload: dict, monkeypatch: pytest.MonkeyPatch
) -> None:
    changed = deepcopy(payload)
    geometry = changed["certificate"]["chart_geometry"]
    geometry["ordinary_rectangle_count"] -= 1
    geometry["terminal_clipped_rectangle_count"] += 1
    _refresh_certificate_digest(changed)
    _reject_before_replay(changed, monkeypatch, "complete row chart geometry")

    changed = deepcopy(payload)
    changed["certificate"]["combined_row_size"]["voltage_uniform_maximizer"][
        "q_cell"
    ] = 99
    _refresh_certificate_digest(changed)
    _reject_before_replay(changed, monkeypatch, "maximizer chart side")


def test_frontier_gate_and_conclusion_tampering_is_rejected_before_replay(
    payload: dict, monkeypatch: pytest.MonkeyPatch
) -> None:
    changed = deepcopy(payload)
    changed["certificate"]["linear_transfer_frontier"]["rows"]["voltage"][
        "center_TV_transfer_reserve_not_yet_validated"
    ] = "0.009"
    _refresh_certificate_digest(changed)
    _reject_before_replay(changed, monkeypatch, "center reserve changed")

    changed = deepcopy(payload)
    voltage = changed["certificate"]["linear_transfer_frontier"]["rows"][
        "voltage"
    ]
    voltage["orbit_cost_at_strict_stage3g_green_upper"] = "0"
    voltage["conditional_total_if_center_TV_reserve_is_validated"] = "0.5"
    voltage["conditional_contraction_below_one"] = True
    _refresh_certificate_digest(changed)
    _reject_before_replay(changed, monkeypatch, "frontier formula ledger")

    changed = deepcopy(payload)
    changed["certificate"]["transfer_gate"][
        "arbitrary_c0_linear_contraction_closes"
    ] = True
    _refresh_certificate_digest(changed)
    _reject_before_replay(changed, monkeypatch, "transfer gate ledger")

    changed = deepcopy(payload)
    changed["certificate"]["conclusion"] = CONCLUSION + "; onset validated"
    _refresh_certificate_digest(changed)
    _reject_before_replay(changed, monkeypatch, "conclusion changed")


def test_candidate_error_hex_and_nested_schema_tampering_is_rejected_before_replay(
    payload: dict, monkeypatch: pytest.MonkeyPatch
) -> None:
    changed = deepcopy(payload)
    changed["certificate"]["combined_row_size"][
        "stage3g_resolvent_candidate_row_error_upper"
    ] = "0.01"
    _refresh_certificate_digest(changed)
    _reject_before_replay(changed, monkeypatch, "resolvent error ingress")

    changed = deepcopy(payload)
    changed["certificate"]["phase_ratio_enclosures"][
        "recovery_ratio_center_binary64_hex"
    ] = "0x1p+0"
    _refresh_certificate_digest(changed)
    _reject_before_replay(changed, monkeypatch, "center hex is not canonical")

    changed = deepcopy(payload)
    changed["certificate"]["phase_ratio_enclosures"]["extra"] = "0"
    _refresh_certificate_digest(changed)
    _reject_before_replay(changed, monkeypatch, "phase ledger schema changed")
