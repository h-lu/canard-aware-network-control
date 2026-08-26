from __future__ import annotations

from copy import deepcopy
from fractions import Fraction
import json
from pathlib import Path

import pytest

from canard_control.leaky_dobrushin_async_routing_transfer import (
    DEFECT_L1_CONSTANT,
    DEFECT_L1_RECIPROCAL,
    OPEN_FLAGS,
    PROVED_FLAGS,
    RESULT_RELATIVE_PATH,
    TEST_RELATIVE_PATH,
    build_async_routing_transfer_certificate,
    exact_mean_routing_radius_squared,
    full_history_route_budget_holds,
    gap_derivative_error_bound,
    gap_value_error_bound,
    threshold_budget_holds,
    threshold_shift_bound,
    validate_async_routing_transfer_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]


def _payload() -> dict[str, object]:
    return json.loads((REPOSITORY / RESULT_RELATIVE_PATH).read_text())


def test_async_routing_certificate_replays() -> None:
    payload = _payload()
    validate_async_routing_transfer_result(payload, REPOSITORY)
    assert payload["certificate"] == build_async_routing_transfer_certificate(
        REPOSITORY
    ).__dict__


def test_exact_collective_composition_constants() -> None:
    assert DEFECT_L1_CONSTANT == Fraction(56483, 3200)
    assert DEFECT_L1_RECIPROCAL == Fraction(3200, 56483)
    radius_squared = exact_mean_routing_radius_squared(
        Fraction(1, 10), Fraction(1, 20), Fraction(1, 1000)
    )
    assert radius_squared == Fraction(16, 282415)


def test_async_claim_ledgers_are_unique_and_disjoint() -> None:
    assert len(PROVED_FLAGS) == len(set(PROVED_FLAGS))
    assert len(OPEN_FLAGS) == len(set(OPEN_FLAGS))
    assert set(PROVED_FLAGS).isdisjoint(OPEN_FLAGS)


def test_async_result_binds_this_test() -> None:
    payload = _payload()
    assert payload["manifest"]["test"] == TEST_RELATIVE_PATH
    assert len(payload["manifest"]["test_sha256"]) == 64


def test_full_history_budget_is_strict() -> None:
    assert full_history_route_budget_holds(
        Fraction(1, 1000),
        Fraction(1, 10),
        Fraction(1, 20),
        Fraction(2),
        Fraction(1, 100),
    )
    assert not full_history_route_budget_holds(
        Fraction(1, 20),
        Fraction(1, 10),
        Fraction(1, 20),
        Fraction(0),
        Fraction(1),
    )


def test_monotone_threshold_budget_and_shift_are_exact() -> None:
    radius = Fraction(1, 100)
    value_error = gap_value_error_bound(radius, 2, 3)
    derivative_error = gap_derivative_error_bound(radius, 1, 2)
    assert value_error == Fraction(809449, 32000000)
    assert derivative_error == Fraction(216483, 16000000)
    assert threshold_budget_holds(
        radius,
        gap_slope=1,
        parameter_half_width=1,
        initial_gap_response=2,
        forcing_gap_response=3,
        initial_derivative_response=1,
        forcing_derivative_response=2,
    )
    assert threshold_shift_bound(radius, 1, 2, 3) == value_error


def test_threshold_budget_rejects_missing_endpoint_margin() -> None:
    assert not threshold_budget_holds(
        Fraction(1, 10),
        gap_slope=Fraction(1, 100),
        parameter_half_width=Fraction(1, 100),
        initial_gap_response=1,
        forcing_gap_response=1,
        initial_derivative_response=0,
        forcing_derivative_response=0,
    )


def test_concrete_asynchronous_claims_remain_false_and_null() -> None:
    certificate = _payload()["certificate"]
    assert certificate["parent_accumulated_defect_constant_exact"] == (
        "703/40+27*sqrt(5)/800"
    )
    assert certificate[
        "parent_accumulated_defect_constant_rational_upper"
    ] == "56483/3200"
    assert "56483/3200" in certificate["full_history_ball_budget"]
    assert "in [Jc-r_J,Jc+r_J]" in certificate[
        "threshold_existence_conditions"
    ]
    assert "for J in [Jc-r_J,Jc+r_J]" in certificate[
        "safety_guard_formula"
    ]
    assert certificate["first_strip_exit_bootstrap_implication_proved"]
    assert certificate["monotone_gap_root_perturbation_lemma_proved"]
    assert not certificate["scalar_forced_routing_tube_validated"]
    assert not certificate["concrete_positive_asynchronous_radius_certified"]
    assert not certificate["asynchronous_unique_pulse_threshold_certified"]
    assert certificate["concrete_asynchronous_radius"] is None
    assert certificate["concrete_threshold_shift_bound"] is None


def test_validator_rejects_asynchronous_threshold_promotion() -> None:
    payload = deepcopy(_payload())
    payload["certificate"]["asynchronous_unique_pulse_threshold_certified"] = True
    with pytest.raises(ValueError, match="differs from replay|open asynchronous"):
        validate_async_routing_transfer_result(payload, REPOSITORY)


def test_validator_rejects_inserted_radius() -> None:
    payload = deepcopy(_payload())
    payload["certificate"]["concrete_asynchronous_radius"] = "1/100"
    with pytest.raises(ValueError, match="differs from replay|unvalidated"):
        validate_async_routing_transfer_result(payload, REPOSITORY)


def test_validator_rejects_parent_hash_mutation() -> None:
    payload = deepcopy(_payload())
    payload["manifest"]["parent_result_sha256"] = "0" * 64
    with pytest.raises(ValueError, match="parent_result hash"):
        validate_async_routing_transfer_result(payload, REPOSITORY)


def test_validator_rejects_test_hash_mutation() -> None:
    payload = deepcopy(_payload())
    payload["manifest"]["test_sha256"] = "0" * 64
    with pytest.raises(ValueError, match="test hash"):
        validate_async_routing_transfer_result(payload, REPOSITORY)


def test_validator_rejects_restored_prehistory_omission() -> None:
    payload = deepcopy(_payload())
    payload["certificate"][
        "parent_accumulated_defect_constant_exact"
    ] = "703/40"
    with pytest.raises(ValueError, match="parent budget|differs from replay"):
        validate_async_routing_transfer_result(payload, REPOSITORY)


def test_note_keeps_biological_claims_open() -> None:
    note = (
        REPOSITORY / "docs/leaky-dobrushin-async-routing-transfer.md"
    ).read_text()
    assert "proved" in note
    assert "56483}{3200" in note
    assert "27\\sqrt5}{800" in note
    assert "absence of roots outside" in note
    assert "global threshold uniqueness" in note
    assert "does **not** prove" in note
    assert r"asynchronous \(J_c\)" in note
