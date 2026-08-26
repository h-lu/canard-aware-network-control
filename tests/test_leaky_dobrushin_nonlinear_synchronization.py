from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from canard_control.leaky_dobrushin_nonlinear_synchronization import (
    RESULT_RELATIVE_PATH,
    build_nonlinear_synchronization_certificate,
    validate_nonlinear_synchronization_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]


def _payload() -> dict[str, object]:
    return json.loads((REPOSITORY / RESULT_RELATIVE_PATH).read_text())


def test_nonlinear_synchronization_certificate_replays() -> None:
    payload = _payload()
    validate_nonlinear_synchronization_result(payload, REPOSITORY)
    assert payload["certificate"] == build_nonlinear_synchronization_certificate(
        REPOSITORY
    ).__dict__


def test_nonlinear_synchronization_claim_boundary() -> None:
    certificate = _payload()["certificate"]
    assert certificate["conditional_exponential_node_synchronization_proved"]
    assert certificate["decay_rate_uniform_in_finite_network_size_proved"]
    assert not certificate["declared_voltage_strip_forward_invariant_proved"]
    assert not certificate["topology_uniform_nonlinear_basin_radius_proved"]
    assert not certificate["nonlinear_asynchronous_canard_connection_proved"]


def test_nonlinear_synchronization_rejects_basin_promotion() -> None:
    payload = deepcopy(_payload())
    payload["certificate"]["topology_uniform_nonlinear_basin_radius_proved"] = True
    with pytest.raises(ValueError, match="differs from replay|open nonlinear"):
        validate_nonlinear_synchronization_result(payload, REPOSITORY)


def test_nonlinear_synchronization_rejects_parent_hash_mutation() -> None:
    payload = deepcopy(_payload())
    payload["manifest"]["parent_result_sha256"] = "0" * 64
    with pytest.raises(ValueError, match="parent_result hash"):
        validate_nonlinear_synchronization_result(payload, REPOSITORY)


def test_nonlinear_synchronization_note_states_strip_condition() -> None:
    note = (
        REPOSITORY / "docs/leaky-dobrushin-nonlinear-synchronization.md"
    ).read_text()
    assert "conditionally on strip residence" in note
    assert "does not control the collective component" in note
    assert "asynchronous physical pulse threshold" in note
