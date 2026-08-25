"""Tests for the source-bound physical-pulse separator candidate."""

from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path

import pytest

from canard_control.leaky_periodic_branch_artifact import orbit_from_artifact
from canard_control.leaky_pulse_separator_candidate import (
    NUMERICAL_TRUE_FLAGS,
    PROOF_FALSE_FLAGS,
    STEP_COUNTS,
    binary64_value,
    finite_section,
    method_of_steps_breakpoints,
    shooting_data,
    validate_candidate_body,
    validate_separator_candidate_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]
RESULT = REPOSITORY / "experiments/results/leaky_pulse_separator_candidate.json"
PARENT = REPOSITORY / (
    "experiments/results/autonomous_leaky_recovery_inner_branch_artifact.json"
)


def _payload() -> dict[str, object]:
    payload = json.loads(RESULT.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def test_source_bound_candidate_revalidates() -> None:
    payload = _payload()
    validate_separator_candidate_result(payload, REPOSITORY)
    candidate = payload["candidate"]
    claims = candidate["claim_status"]
    assert all(claims[name] is True for name in NUMERICAL_TRUE_FLAGS)
    assert all(claims[name] is False for name in PROOF_FALSE_FLAGS)
    assert candidate["parent_periodic_orbit_existence_validated"] is True


def test_manifest_hashes_every_declared_dependency() -> None:
    manifest = _payload()["manifest"]
    names = (
        "source",
        "generator",
        "note",
        "model_source",
        "terminal_history_source",
        "parent_artifact_source",
        "parent_artifact_result",
    )
    for name in names:
        relative = manifest[name]
        assert manifest[f"{name}_sha256"] == sha256(
            (REPOSITORY / relative).read_bytes()
        ).hexdigest()


def test_validator_rejects_proof_promotion_and_numeric_tampering() -> None:
    candidate = _payload()["candidate"]

    promoted = deepcopy(candidate)
    promoted["claim_status"][PROOF_FALSE_FLAGS[0]] = True
    with pytest.raises(ValueError, match="proof flag was promoted"):
        validate_candidate_body(promoted)

    weakened = deepcopy(candidate)
    weakened["claim_status"][NUMERICAL_TRUE_FLAGS[0]] = False
    with pytest.raises(ValueError, match="observation was weakened"):
        validate_candidate_body(weakened)

    changed = deepcopy(candidate)
    changed["resolutions"][0]["shooting_roots"][2]["pulse_amplitude"][
        "decimal"
    ] = "0.31"
    with pytest.raises(ValueError):
        validate_candidate_body(changed)

    lost_bracket = deepcopy(candidate)
    row = lost_bracket["resolutions"][0]["shooting_roots"][0]
    row["bracket_right_coordinate"] = row["bracket_left_coordinate"]
    with pytest.raises(ValueError, match="bracket has no sign change"):
        validate_candidate_body(lost_bracket)


def test_method_of_steps_grid_tracks_pulse_release_propagation() -> None:
    base = 5.0**0.5
    breakpoints = method_of_steps_breakpoints(20.0)
    assert any(abs(point - (1.0 + 4.0 * base)) < 2.0e-15 for point in breakpoints)
    assert any(abs(point - 5.0 * base) < 2.0e-15 for point in breakpoints)
    assert max(right - left for left, right in zip(breakpoints, breakpoints[1:])) < base
    with pytest.raises(ValueError, match="final_time"):
        method_of_steps_breakpoints(0.0)


def test_resolution_and_return_ladders_have_the_declared_geometry() -> None:
    candidate = _payload()["candidate"]
    assert [row["step_count"] for row in candidate["resolutions"]] == list(
        STEP_COUNTS
    )
    depth_three = []
    translation_residuals = []
    for resolution in candidate["resolutions"]:
        rows = resolution["shooting_roots"]
        roots = [binary64_value(row["pulse_amplitude"], "root") for row in rows]
        distances = [
            binary64_value(row["reference_distance_l2"], "distance")
            for row in rows
        ]
        scaled = [
            binary64_value(row["multiplier_scaled_derivative"], "scaled")
            for row in rows
        ]
        assert distances[0] > distances[1] > distances[2]
        assert abs(roots[2] - roots[1]) < 5.0e-12
        assert min(abs(value) for value in scaled) > 3.0
        translation_residuals.append(
            binary64_value(
                resolution["translation_tangent_relative_residual_l2"],
                "translation residual",
            )
        )
        depth_three.append(roots[2])
    assert max(depth_three) - min(depth_three) < 5.0e-12
    assert (
        translation_residuals[0]
        > translation_residuals[1]
        > translation_residuals[2]
    )


def test_lightweight_replay_of_one_monodromy_and_third_return() -> None:
    payload = _payload()
    parent = json.loads(PARENT.read_text(encoding="utf-8"))
    orbit = orbit_from_artifact(parent["artifact"])
    section = finite_section(orbit, STEP_COUNTS[0])
    stored = payload["candidate"]["resolutions"][0]
    leading = binary64_value(stored["leading_multiplier"]["real"], "leading")
    assert section.leading_multiplier.real == pytest.approx(leading, abs=2.0e-12)
    root_row = stored["shooting_roots"][2]
    root = binary64_value(root_row["pulse_amplitude"], "root")
    coordinate, crossing, distance = shooting_data(section, root, 3)
    assert abs(coordinate) < 2.0e-10
    assert crossing == pytest.approx(
        binary64_value(root_row["crossing_time"], "crossing"), abs=2.0e-8
    )
    assert distance < 3.0e-12
