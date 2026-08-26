from __future__ import annotations

from copy import deepcopy
from decimal import Decimal
from hashlib import sha256
import json
from pathlib import Path

import pytest

from canard_control.leaky_pulse_outer_third_return_enclosure import (
    EXPECTED_CROSSING_DIRECTIONS,
    FALSE_FLAGS,
    RESULT_RELATIVE_PATH,
    canonical_sha256,
    validate_third_return_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]
EXPECTED_RESULT_SHA256 = (
    "7a01c2a8ec6b5421c090836f4962e595027d78be3381d490c4b6eb56d3beb13d"
)


def _payload() -> dict[str, object]:
    return json.loads(
        (REPOSITORY / RESULT_RELATIVE_PATH).read_text(encoding="utf-8")
    )


def test_registered_third_return_enclosure_is_source_bound() -> None:
    payload = _payload()
    validate_third_return_result(payload, REPOSITORY)
    assert sha256((REPOSITORY / RESULT_RELATIVE_PATH).read_bytes()).hexdigest() == (
        EXPECTED_RESULT_SHA256
    )


def test_all_time_cells_and_both_delay_families_are_closed() -> None:
    arithmetic = _payload()["certificate"]["arithmetic"]
    assert arithmetic["grid_cell_count"] == 2064
    assert arithmetic["forced_cell_count"] == 21
    assert arithmetic["delay_four_initial_cell_count"] == 192
    assert arithmetic["delay_five_initial_cell_count"] == 240
    assert arithmetic["delay_four_translated_cell_count"] == 1872
    assert arithmetic["delay_five_translated_cell_count"] == 1824
    assert Decimal(arithmetic["maximum_p_error_radius_upper"]) < Decimal("5e-22")
    assert Decimal(arithmetic["minimum_cell_closure_gap_lower"]) > 0


def test_third_positive_crossing_has_a_directed_micro_bracket() -> None:
    event = _payload()["certificate"]["event"]
    assert event["candidate_cell_count"] == 6
    assert tuple(event["crossing_directions"]) == EXPECTED_CROSSING_DIRECTIONS
    assert event["positive_crossing_count_through_declared_event"] == 3
    assert event["all_other_cells_excluded_by_bernstein"]
    assert event["all_candidate_crossings_unique"]
    assert Decimal(event["third_event_lower_sign_upper"]) < 0
    assert Decimal(event["third_event_upper_sign_lower"]) > 0
    assert Decimal(event["third_event_speed_lower"]) > Decimal("0.89")
    assert Decimal(event["third_event_time_error_upper"]) < Decimal("4.8e-16")


def test_complete_history_comparison_is_continuous_not_sampled() -> None:
    comparison = _payload()["certificate"][
        "candidate_outer_history_comparison"
    ]
    assert comparison["history_cell_count"] == 241
    assert comparison[
        "continuous_candidate_outer_history_bernstein_distance_validated"
    ]
    assert comparison["complete_history_flow_error_validated"]
    assert Decimal(comparison["maximum_outer_taylor_remainder_upper"]) < Decimal(
        "3.6e-30"
    )
    assert Decimal(comparison["complete_guide_history_distance_upper"]) < Decimal(
        "5.619e-6"
    )
    assert Decimal(comparison["complete_flow_history_error_upper"]) < Decimal(
        "7e-23"
    )


def test_period_error_is_not_silently_absorbed_into_the_wiener_radius() -> None:
    correction = _payload()["certificate"]["exact_outer_orbit_correction"]
    coefficient_radius = Decimal(
        correction["coefficient_and_period_correction_radius_upper"]
    )
    phase_error = Decimal(correction["phase_shift_state_error_upper"])
    history_error = Decimal(
        correction["exact_outer_orbit_history_correction_upper"]
    )
    assert coefficient_radius >= Decimal("1e-5")
    assert phase_error > Decimal("1e-5")
    assert history_error >= coefficient_radius + phase_error


def test_error_decomposition_closes_a_history_ball_not_a_basin() -> None:
    certificate = _payload()["certificate"]
    history = certificate["history_ball"]
    assert history["error_decomposition"] == (
        "E_guide+E_flow+E_orbit+E_time*F_tube+E_section"
    )
    assert Decimal(history["reduced_history_distance_upper"]) < Decimal(
        "2.638e-5"
    )
    assert Decimal(history["complete_history_distance_upper"]) < Decimal(
        "2.638e-5"
    )
    assert Decimal(history["complete_design_ball_margin_lower"]) > Decimal(
        "7.36e-5"
    )
    assert not history["same_exact_poincare_section_inferred_from_E_section"]
    claims = certificate["claim_status"]
    assert claims["third_return_complete_history_ball_inclusion_validated"]
    for name in FALSE_FLAGS:
        assert not claims[name]


def test_hostile_certificate_mutation_is_rejected_by_digest() -> None:
    payload = deepcopy(_payload())
    payload["certificate"]["event"]["candidate_cell_count"] = 5
    with pytest.raises(ValueError, match="certificate digest"):
        validate_third_return_result(payload, REPOSITORY)


def test_hostile_capture_promotion_is_rejected_even_with_refreshed_digest() -> None:
    payload = deepcopy(_payload())
    payload["certificate"]["claim_status"][
        "outer_basin_capture_validated"
    ] = True
    payload["manifest"]["certificate_sha256"] = canonical_sha256(
        payload["certificate"]
    )
    with pytest.raises(ValueError, match="open capture or routing claim"):
        validate_third_return_result(payload, REPOSITORY)


def test_hostile_source_manifest_mutation_is_rejected() -> None:
    payload = deepcopy(_payload())
    source = next(iter(payload["manifest"]["source_sha256"]))
    payload["manifest"]["source_sha256"][source] = "0" * 64
    with pytest.raises(ValueError, match="source changed"):
        validate_third_return_result(payload, REPOSITORY)


def test_note_keeps_history_ball_and_basin_claims_separate() -> None:
    note = (
        REPOSITORY / "docs/leaky-pulse-outer-third-return-enclosure.md"
    ).read_text(encoding="utf-8")
    assert "proved single-pulse ambient history-ball inclusion" in note
    assert "The phrase *history ball*" in note
    assert "invariant or" in note
    assert "attracting." in note
    assert "cannot bypass the phase chart" in note
    assert "capture flag therefore remains false" in note
    assert "not outer" in note
    assert "capture, two-sided routing" in note
