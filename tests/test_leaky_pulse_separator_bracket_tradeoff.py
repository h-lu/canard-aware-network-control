from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from canard_control.leaky_pulse_separator_bracket_tradeoff import (
    NUMERICAL_TRUE_FLAGS,
    PROOF_FALSE_FLAGS,
    RESULT_RELATIVE_PATH,
    validate_bracket_tradeoff_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def payload():
    return json.loads((REPOSITORY / RESULT_RELATIVE_PATH).read_text(encoding="utf-8"))


def test_registered_bracket_tradeoff_validates(payload):
    validate_bracket_tradeoff_result(payload, REPOSITORY)


def test_claim_boundary_is_explicit(payload):
    claims = payload["certificate"]["claim_status"]
    assert all(claims[name] is True for name in NUMERICAL_TRUE_FLAGS)
    assert all(claims[name] is False for name in PROOF_FALSE_FLAGS)


def test_recommended_row_has_the_registered_tradeoff(payload):
    rows = {
        row["bracket_id"]: row for row in payload["certificate"]["rows"]
    }
    recommended = rows["wide_recommended"]
    narrow = rows["narrow"]
    assert float(recommended["minimum_endpoint_gap_margin"]) > 13 * float(
        narrow["minimum_endpoint_gap_margin"]
    )
    assert (
        float(recommended["maximum_endpoint_reduced_mesh_sup_distance"])
        < 0.0017
    )
    assert rows["wide_dominated"]["pareto_dominated"] is True


def test_hostile_promotion_is_rejected(payload):
    hostile = deepcopy(payload)
    hostile["certificate"]["claim_status"][
        "physical_pulse_separator_crossing_validated"
    ] = True
    with pytest.raises(ValueError):
        validate_bracket_tradeoff_result(hostile, REPOSITORY)


def test_hostile_margin_weakening_is_rejected(payload):
    hostile = deepcopy(payload)
    rows = {
        row["bracket_id"]: row for row in hostile["certificate"]["rows"]
    }
    rows["wide_recommended"]["minimum_endpoint_gap_margin"] = "1e-5"
    with pytest.raises(ValueError):
        validate_bracket_tradeoff_result(hostile, REPOSITORY)
