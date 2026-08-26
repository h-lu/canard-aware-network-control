from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import shutil

import pytest

from canard_control.leaky_dobrushin_collective_defect import (
    OPEN_FLAGS,
    PROVED_FLAGS,
    RESULT_RELATIVE_PATH,
    TEST_RELATIVE_PATH,
    build_collective_defect_certificate,
    validate_collective_defect_result,
)
from canard_control.leaky_dobrushin_nonlinear_synchronization import (
    RESULT_RELATIVE_PATH as SYNCHRONIZATION_RESULT_RELATIVE_PATH,
    SOURCE_RELATIVE_PATH as SYNCHRONIZATION_SOURCE_RELATIVE_PATH,
    canonical_sha256 as synchronization_canonical_sha256,
)


REPOSITORY = Path(__file__).resolve().parents[1]


def _payload() -> dict[str, object]:
    return json.loads((REPOSITORY / RESULT_RELATIVE_PATH).read_text())


def test_collective_defect_certificate_replays() -> None:
    payload = _payload()
    validate_collective_defect_result(payload, REPOSITORY)
    assert payload["certificate"] == build_collective_defect_certificate(
        REPOSITORY
    ).__dict__


def test_collective_defect_exact_constants_and_boundary() -> None:
    certificate = _payload()["certificate"]
    assert certificate["pointwise_defect_constant_exact"] == "703/200"
    assert certificate["accumulated_defect_constant_exact"] == (
        "703/40+27*sqrt(5)/800"
    )
    assert certificate["accumulated_defect_constant_rational_upper"] == (
        "56483/3200"
    )
    assert "M(t-tau0)^2" in certificate[
        "componentwise_pointwise_defect_estimate"
    ]
    assert "(1403/400)*M(t)^2" in certificate[
        "componentwise_pointwise_defect_estimate"
    ]
    assert "(3/800)" in certificate[
        "componentwise_pointwise_defect_estimate"
    ]
    assert "H_M(t)^2" in certificate["pointwise_defect_estimate"]
    assert certificate["quadratic_collective_defect_bound_proved"]
    assert certificate["delayed_history_residence_accounted_exactly"]
    assert certificate["conditional_integrable_collective_defect_proved"]
    assert not certificate["collective_scalar_shadowing_tube_proved"]
    assert not certificate["topology_uniform_asynchronous_threshold_radius_proved"]


def test_collective_defect_claim_ledgers_are_unique_and_disjoint() -> None:
    assert len(PROVED_FLAGS) == len(set(PROVED_FLAGS))
    assert len(OPEN_FLAGS) == len(set(OPEN_FLAGS))
    assert set(PROVED_FLAGS).isdisjoint(OPEN_FLAGS)


def test_collective_defect_result_binds_this_test() -> None:
    payload = _payload()
    assert payload["manifest"]["test"] == TEST_RELATIVE_PATH
    assert len(payload["manifest"]["test_sha256"]) == 64


def test_collective_defect_rejects_threshold_promotion() -> None:
    payload = deepcopy(_payload())
    payload["certificate"][
        "topology_uniform_asynchronous_threshold_radius_proved"
    ] = True
    with pytest.raises(ValueError, match="differs from replay|open collective"):
        validate_collective_defect_result(payload, REPOSITORY)


def test_collective_defect_rejects_dropped_history_residence() -> None:
    payload = deepcopy(_payload())
    payload["certificate"]["accumulated_defect_constant_exact"] = "703/40"
    with pytest.raises(ValueError, match="accumulated constant|differs from replay"):
        validate_collective_defect_result(payload, REPOSITORY)


def test_collective_defect_rejects_parent_hash_mutation() -> None:
    payload = deepcopy(_payload())
    payload["manifest"]["parent_result_sha256"] = "0" * 64
    with pytest.raises(ValueError, match="parent_result hash"):
        validate_collective_defect_result(payload, REPOSITORY)


def test_collective_defect_rejects_test_hash_mutation() -> None:
    payload = deepcopy(_payload())
    payload["manifest"]["test_sha256"] = "0" * 64
    with pytest.raises(ValueError, match="test hash"):
        validate_collective_defect_result(payload, REPOSITORY)


def test_collective_validator_replays_live_parent_after_warm_cache(
    tmp_path: Path,
) -> None:
    copied = tmp_path / "repository"
    shutil.copytree(
        REPOSITORY,
        copied,
        ignore=shutil.ignore_patterns(
            ".git",
            ".venv",
            ".pytest_cache",
            "build",
            "output",
            "tmp",
            "manuscript",
            "__pycache__",
            "*.pyc",
        ),
    )
    child_path = copied / RESULT_RELATIVE_PATH
    child = json.loads(child_path.read_bytes())
    validate_collective_defect_result(child, copied)

    parent_source = copied / SYNCHRONIZATION_SOURCE_RELATIVE_PATH
    parent_source.write_bytes(
        parent_source.read_bytes() + b"\n# hostile live-source mutation\n"
    )
    parent_path = copied / SYNCHRONIZATION_RESULT_RELATIVE_PATH
    parent = json.loads(parent_path.read_bytes())
    parent["certificate"]["declared_voltage_strip_forward_invariant_proved"] = True
    parent["manifest"]["certificate_sha256"] = (
        synchronization_canonical_sha256(parent["certificate"])
    )
    parent["manifest"]["source_sha256"] = sha256(
        parent_source.read_bytes()
    ).hexdigest()
    parent_path.write_text(
        json.dumps(parent, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    child["manifest"]["parent_result_sha256"] = sha256(
        parent_path.read_bytes()
    ).hexdigest()
    with pytest.raises(ValueError):
        validate_collective_defect_result(child, copied)


def test_collective_defect_note_keeps_shadowing_open() -> None:
    note = (REPOSITORY / "docs/leaky-dobrushin-collective-defect.md").read_text()
    assert "proved conditionally" in note
    assert "703}{200" in note
    assert "27\\sqrt5}{800" in note
    assert "cannot be replaced by the current" in note
    assert "scalar shadowing" in note
    assert "still required" in note
