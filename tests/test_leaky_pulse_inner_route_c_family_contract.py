from __future__ import annotations

from copy import deepcopy
from decimal import Decimal
from hashlib import sha256
import json
from pathlib import Path

import pytest

from canard_control.leaky_pulse_inner_route_c_family_contract import (
    FALSE_FLAGS,
    RESULT_RELATIVE_PATH,
    canonical_sha256,
    validate_route_c_family_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]
EXPECTED_RESULT_SHA256 = (
    "6821551f3fab7d4bbc073af20b83daf055482055a81db23664d31c017de81f7c"
)


def _payload() -> dict[str, object]:
    return json.loads(
        (REPOSITORY / RESULT_RELATIVE_PATH).read_text(encoding="utf-8")
    )


def test_registered_route_c_family_contract_is_source_bound() -> None:
    payload = _payload()
    validate_route_c_family_result(payload, REPOSITORY)
    assert sha256((REPOSITORY / RESULT_RELATIVE_PATH).read_bytes()).hexdigest() == (
        EXPECTED_RESULT_SHA256
    )


def test_full_width_failure_frontier_is_exact() -> None:
    pilot = _payload()["certificate"]["directed_full_width_pilot"]
    assert not pilot["completed"]
    assert pilot["closed_cell_count"] == 730
    assert pilot["remaining_cell_count"] == 422
    assert pilot["failure"]["cell_key"] == [0, 365, 1, 355]
    assert pilot["failure"]["reason"] == "nonfinite_state_endpoint_bound"
    assert Decimal(pilot["minimum_closed_cell_gap_lower"]) > 0


def test_one_exact_partition_shard_closes_but_29999_remain() -> None:
    certificate = _payload()["certificate"]
    pilot = certificate["directed_partition_shard_pilot"]
    cover = certificate["equal_width_shard_contract"]
    assert pilot["completed"]
    assert pilot["closed_cell_count"] == 1152
    assert Decimal(pilot["maximum_state_P_radius_upper"]) < Decimal("0.01")
    assert Decimal(pilot["minimum_closed_cell_gap_lower"]) > Decimal("6.2e-13")
    assert pilot["not_a_route_c_history_ball"]
    assert cover["exact_shard_count"] == 30000
    assert cover["partition_shards_replayed"] == 1
    assert cover["partition_shards_remaining"] == 29999


def test_zero_width_baseline_exposes_structural_variation_wrapping() -> None:
    certificate = _payload()["certificate"]
    point = certificate["zero_width_variation_baseline"]
    shard = certificate["directed_partition_shard_pilot"]
    assert point["completed"]
    assert Decimal(point["maximum_first_J_variation_P_norm_upper"]) > Decimal(
        "3.8e6"
    )
    assert Decimal(point["maximum_second_J_variation_P_norm_upper"]) > Decimal(
        "2.5e13"
    )
    assert Decimal(shard["maximum_first_J_variation_P_norm_upper"]) < (
        Decimal("1.01")
        * Decimal(point["maximum_first_J_variation_P_norm_upper"])
    )
    assert not certificate["method_diagnosis"][
        "zero_centered_variation_majorant_is_structurally_usable"
    ]


def test_event_history_and_stable_coordinates_remain_open() -> None:
    certificate = _payload()["certificate"]
    event = certificate["event_and_complete_history_interface"]
    stable = certificate["stable_coordinate_interface"]
    assert all(
        event[name] is None
        for name in (
            "route_c_event_bracket",
            "unique_event_speed_lower",
            "event_time_first_J_variation",
            "event_time_second_J_variation",
            "complete_history_family_radius",
        )
    )
    assert stable["left_endpoint_stable_coordinate"] is None
    assert stable["right_endpoint_stable_coordinate"] is None
    assert not stable["finite_section_values_used_as_stable_coordinate_proof"]
    for name in FALSE_FLAGS:
        assert not certificate["claim_status"][name]


def test_hostile_claim_promotion_is_rejected_after_digest_refresh() -> None:
    payload = deepcopy(_payload())
    payload["certificate"]["claim_status"][
        "unique_route_c_pulse_event_validated"
    ] = True
    payload["manifest"]["certificate_sha256"] = canonical_sha256(
        payload["certificate"]
    )
    with pytest.raises(ValueError, match="open Route-C family claim"):
        validate_route_c_family_result(payload, REPOSITORY)


def test_hostile_finite_section_promotion_is_rejected() -> None:
    payload = deepcopy(_payload())
    payload["certificate"]["stable_coordinate_interface"][
        "finite_section_values_used_as_stable_coordinate_proof"
    ] = True
    payload["manifest"]["certificate_sha256"] = canonical_sha256(
        payload["certificate"]
    )
    with pytest.raises(ValueError, match="finite-section data"):
        validate_route_c_family_result(payload, REPOSITORY)


def test_hostile_source_mutation_is_rejected() -> None:
    payload = deepcopy(_payload())
    source = next(iter(payload["manifest"]["source_sha256"]))
    payload["manifest"]["source_sha256"][source] = "0" * 64
    with pytest.raises(ValueError, match="source changed"):
        validate_route_c_family_result(payload, REPOSITORY)


def test_note_states_the_exact_nonproof_boundary() -> None:
    note = (
        REPOSITORY / "docs/leaky-pulse-inner-route-c-family-contract.md"
    ).read_text(encoding="utf-8")
    assert "leaving exactly 422 time cells" in note
    assert "leaves 29,999 partition members unreplayed" in note
    assert "P-norm pilot cap" in note
    assert "not evidence for either side of the stable manifold" in note
    assert "event-time first" in note
    assert "second variations" in note
