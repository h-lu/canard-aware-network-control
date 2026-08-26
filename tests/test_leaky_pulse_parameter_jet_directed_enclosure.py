from __future__ import annotations

from copy import deepcopy
from decimal import Decimal
from hashlib import sha256
import json
from pathlib import Path

import pytest

from canard_control.leaky_pulse_parameter_jet_directed_enclosure import (
    FALSE_FLAGS,
    RESULT_RELATIVE_PATH,
    canonical_sha256,
    validate_directed_jet_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]
EXPECTED_RESULT_SHA256 = (
    "71276785fd803b663fc11de9489751ccd53dd8a408323a0bb140d0c9e7b7862b"
)


def _payload() -> dict[str, object]:
    return json.loads(
        (REPOSITORY / RESULT_RELATIVE_PATH).read_text(encoding="utf-8")
    )


def test_registered_directed_jet_enclosure_is_source_bound() -> None:
    payload = _payload()
    validate_directed_jet_result(payload, REPOSITORY)
    assert sha256((REPOSITORY / RESULT_RELATIVE_PATH).read_bytes()).hexdigest() == (
        EXPECTED_RESULT_SHA256
    )


def test_all_joint_coefficient_cells_close_with_small_error() -> None:
    coefficient = _payload()["certificate"]["joint_coefficient_enclosure"]
    assert coefficient["all_cells_closed"]
    assert coefficient["closed_cell_count"] == 1152
    assert Decimal(coefficient["maximum_joint_P_error_radius_upper"]) < Decimal(
        "9e-19"
    )
    assert Decimal(coefficient["maximum_guide_residual_upper"]) < Decimal(
        "2.4e-24"
    )
    assert Decimal(coefficient["minimum_cell_closure_gap_lower"]) > 0


def test_continuous_bernstein_envelopes_cover_all_five_derivative_orders() -> None:
    rows = _payload()["certificate"]["joint_coefficient_enclosure"][
        "continuous_time_bernstein_envelopes"
    ]
    assert [row["order"] for row in rows] == [0, 1, 2, 3, 4]
    assert Decimal(rows[4]["maximum_derivative_jet_z_voltage_abs_upper"]) > Decimal(
        "1e10"
    )
    assert Decimal(rows[4]["maximum_derivative_jet_z_voltage_error_upper"]) < 1


def test_explicit_cubic_tail_contains_exactly_degrees_five_through_twelve() -> None:
    tail = _payload()["certificate"]["cubic_substitution_tail"]
    assert tail["included_parameter_degrees"] == list(range(5, 13))
    assert tail["linear_and_pulse_terms_have_no_degree_ge_5_tail"]
    assert Decimal(tail["maximum_directed_P_tail_forcing_upper"]) < Decimal(
        "2.1e-9"
    )


def test_full_width_order_five_remainder_closes_on_every_cell() -> None:
    remainder = _payload()["certificate"]["full_width_order_five_remainder"]
    assert remainder["parameter_domain"] == "xi in [-1,1]"
    assert remainder["all_cells_closed"]
    assert remainder["closed_cell_count"] == 1152
    assert Decimal(remainder["maximum_P_radius_upper"]) < Decimal("1.8e-8")
    assert Decimal(remainder["maximum_voltage_coordinate_error_upper"]) < Decimal(
        "4e-9"
    )
    assert Decimal(remainder["minimum_cell_closure_gap_lower"]) > 0


def test_event_and_onset_claims_remain_open() -> None:
    certificate = _payload()["certificate"]
    event = certificate["event_interface"]
    assert all(
        event[name] is None
        for name in (
            "route_c_event_bracket",
            "uniform_route_c_event_speed",
            "event_time_parameter_jet",
            "common_event_complete_history_radius",
            "stable_coordinate_gap",
            "interval_newton_image",
        )
    )
    for name in FALSE_FLAGS:
        assert not certificate["claim_status"][name]


def test_hostile_tail_degree_mutation_is_rejected_after_digest_refresh() -> None:
    payload = deepcopy(_payload())
    payload["certificate"]["cubic_substitution_tail"][
        "included_parameter_degrees"
    ] = list(range(6, 13))
    payload["manifest"]["certificate_sha256"] = canonical_sha256(
        payload["certificate"]
    )
    with pytest.raises(ValueError, match="tail degree ledger"):
        validate_directed_jet_result(payload, REPOSITORY)


def test_hostile_event_promotion_is_rejected_after_digest_refresh() -> None:
    payload = deepcopy(_payload())
    payload["certificate"]["claim_status"][
        "route_c_event_bracket_validated"
    ] = True
    payload["manifest"]["certificate_sha256"] = canonical_sha256(
        payload["certificate"]
    )
    with pytest.raises(ValueError, match="open event or onset claim"):
        validate_directed_jet_result(payload, REPOSITORY)


def test_hostile_open_event_input_population_is_rejected() -> None:
    payload = deepcopy(_payload())
    payload["certificate"]["event_interface"]["route_c_event_bracket"] = [51, 52]
    payload["manifest"]["certificate_sha256"] = canonical_sha256(
        payload["certificate"]
    )
    with pytest.raises(ValueError, match="silently populated"):
        validate_directed_jet_result(payload, REPOSITORY)


def test_hostile_source_hash_mutation_is_rejected() -> None:
    payload = deepcopy(_payload())
    source = next(iter(payload["manifest"]["source_sha256"]))
    payload["manifest"]["source_sha256"][source] = "0" * 64
    with pytest.raises(ValueError, match="source changed"):
        validate_directed_jet_result(payload, REPOSITORY)


def test_note_separates_the_flow_model_from_event_alignment() -> None:
    note = (
        REPOSITORY / "docs/leaky-pulse-parameter-jet-directed-enclosure.md"
    ).read_text(encoding="utf-8")
    assert "joint correlated coefficient enclosure" in note
    assert "degrees zero through four exactly" in note
    assert "genuine wide-parameter fourth-order flow model" in note
    assert "The theorem is at common physical times" in note
    assert "does not pull the delayed history" in note
