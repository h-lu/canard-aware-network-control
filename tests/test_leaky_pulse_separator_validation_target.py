from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from canard_control.leaky_pulse_separator_validation_target import (
    PARENT_CANDIDATE_RESULT_RELATIVE_PATH,
    PARENT_ORBIT_RESULT_RELATIVE_PATH,
    RESULT_RELATIVE_PATH,
    build_target,
    validate_target_body,
    validate_target_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]


def _payload() -> dict[str, object]:
    return json.loads((REPOSITORY / RESULT_RELATIVE_PATH).read_text())


def test_registered_separator_validation_target_is_self_consistent() -> None:
    payload = _payload()
    validate_target_result(payload, REPOSITORY)
    target = payload["target"]
    claims = target["claim_status"]
    assert claims["narrow_third_return_sign_change_observed"]
    assert claims["sampled_derivative_separated_from_zero_observed"]
    assert not claims["directed_endpoint_gap_enclosures_validated"]
    assert not claims["inner_local_stable_graph_validated"]
    assert not claims["unique_physical_pulse_onset_validated"]
    assert target["requested_directed_certificate_bounds"][
        "these_are_validation_targets_not_proved_bounds"
    ]


def test_separator_validation_target_replays_from_bound_parents() -> None:
    payload = _payload()
    parent_candidate = json.loads(
        (REPOSITORY / PARENT_CANDIDATE_RESULT_RELATIVE_PATH).read_text()
    )
    parent_orbit = json.loads(
        (REPOSITORY / PARENT_ORBIT_RESULT_RELATIVE_PATH).read_text()
    )
    assert build_target(parent_candidate, parent_orbit, REPOSITORY) == payload[
        "target"
    ]


def test_separator_validation_target_rejects_proof_promotion() -> None:
    target = deepcopy(_payload()["target"])
    target["claim_status"]["unique_physical_pulse_onset_validated"] = True
    with pytest.raises(ValueError, match="unproved separator target claim"):
        validate_target_body(target)


def test_separator_validation_target_rejects_lost_endpoint_sign() -> None:
    target = deepcopy(_payload()["target"])
    target["sample_rows"][-1]["third_return_coordinate"] = target[
        "sample_rows"
    ][0]["third_return_coordinate"]
    with pytest.raises(ValueError, match="endpoint sign change"):
        validate_target_body(target)


def test_separator_validation_contract_discloses_open_gates() -> None:
    note = (REPOSITORY / "docs/leaky-pulse-separator-validation-contract.md").read_text()
    assert "not a separator proof" in note
    assert "requested bounds, never as proved bounds" in note
    assert "separator, onset, and routing" in note
