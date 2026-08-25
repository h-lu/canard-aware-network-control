"""Replay, convergence, and hostile-tamper tests for the outer orbit."""

from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path

import numpy as np
import pytest

from canard_control.fhn_periodic_candidate import odd_fourier_matrices
from canard_control.leaky_outer_high_resolution import (
    CLAIM_STATUS,
    DIRECTED_CUTOFF,
    EXPECTED_ARTIFACT_SHA256,
    NODE_COUNTS,
    PRIMARY_NODE_COUNT,
    REFERENCE_NODE_COUNT,
    RESULT_RELATIVE_PATH,
    SOURCE_MANIFEST,
    canonical_sha256,
    orbit_from_resolution,
    validate_outer_high_resolution_artifact,
)


REPOSITORY = Path(__file__).resolve().parents[1]
RESULT = REPOSITORY / RESULT_RELATIVE_PATH
EXPECTED_RESULT_SHA256 = (
    "d888916fed919f1515dd31ab851b2229816ea373365fa0221b1e345580f165a7"
)


def _payload() -> dict:
    return json.loads(RESULT.read_text(encoding="utf-8"))


def _metric(record: dict, name: str, factor: str = "16") -> float:
    return float.fromhex(record["metrics"][factor][name]["binary64_hex"])


def test_outer_artifact_is_source_bound_and_replays_all_resolutions() -> None:
    raw = RESULT.read_bytes()
    assert isinstance(EXPECTED_RESULT_SHA256, str)
    assert sha256(raw).hexdigest() == EXPECTED_RESULT_SHA256
    payload = json.loads(raw)
    primary = validate_outer_high_resolution_artifact(payload, REPOSITORY)
    artifact = payload["artifact"]

    assert primary.state.shape == (PRIMARY_NODE_COUNT, 2)
    assert artifact["claim_status"] == CLAIM_STATUS
    assert canonical_sha256(artifact) == EXPECTED_ARTIFACT_SHA256
    assert payload["manifest"]["artifact_sha256"] == EXPECTED_ARTIFACT_SHA256
    for relative in SOURCE_MANIFEST:
        assert payload["manifest"]["source_sha256"][relative] == sha256(
            (REPOSITORY / relative).read_bytes()
        ).hexdigest()

    for count in NODE_COUNTS:
        record = artifact["resolutions"][str(count)]
        orbit = orbit_from_resolution(record)
        assert orbit.state.shape == (count, 2)
        assert np.array_equal(
            orbit.phase_nodes, np.arange(count, dtype=float) / count
        )
        assert [
            [float(value).hex() for value in row] for row in orbit.state
        ] == record["state_binary64"]


def test_resolution_ladder_exposes_the_129_node_aliasing_failure() -> None:
    resolutions = _payload()["artifact"]["resolutions"]
    off_grid = [
        _metric(resolutions[str(count)], "oversampled_residual_inf")
        for count in NODE_COUNTS
    ]
    tails = [
        _metric(resolutions[str(count)], "spectral_tail_l1")
        for count in NODE_COUNTS
    ]

    assert off_grid[0] > 3.0e-5
    assert off_grid[1] < 1.0e-8
    assert off_grid[2] < 1.0e-10
    assert off_grid[3] < 2.0e-12
    assert all(left > right for left, right in zip(off_grid, off_grid[1:]))
    assert all(left > right for left, right in zip(tails, tails[1:]))
    assert off_grid[0] / off_grid[2] > 4.0e6
    assert DIRECTED_CUTOFF == 3 * ((PRIMARY_NODE_COUNT - 1) // 2)


def test_257_and_385_polynomials_agree_beyond_the_primary_defect_scale() -> None:
    artifact = _payload()["artifact"]
    cross = artifact["cross_resolution"]["metrics"]

    assert artifact["cross_resolution"]["primary_node_count"] == 257
    assert artifact["cross_resolution"]["reference_node_count"] == 385
    assert float.fromhex(
        cross["period_absolute_difference"]["binary64_hex"]
    ) < 7.0e-13
    assert float.fromhex(
        cross["state_inf_difference"]["binary64_hex"]
    ) < 2.0e-13
    assert float.fromhex(
        cross["phase_derivative_inf_difference"]["binary64_hex"]
    ) < 1.0e-11


def test_directed_outer_orbit_closes_without_promoting_floquet_index() -> None:
    artifact = _payload()["artifact"]
    directed = artifact["directed_radii_certificate"]["validation"]

    assert directed["directed_radii_inequality_candidate_closed"]
    assert directed["formula_adaptation_independently_audited"]
    assert directed["periodic_rfde_orbit_validated"]
    assert directed["phase_bordered_rfde_inverse_validated"]
    assert directed["finite"]["finite_inverse_validated"]
    assert directed["blocks"]["full_point_inverse_gate"]
    assert directed["correction"]["radii_polynomial_negative"]
    assert float(directed["finite"]["preconditioned_residual_l1_upper"]) < 3e-13
    assert float(directed["blocks"]["full_point_defect_upper"]) < 0.082
    assert float(directed["correction"]["contraction_upper"]) < 0.243
    assert float(directed["correction"]["radii_margin_lower"]) > 7.5e-6

    floquet = directed["floquet"]
    for name in (
        "translation_identity_exact_for_validated_orbit",
        "phase_bordered_rfde_inverse_validated",
        "geometric_translation_kernel_conditional_on_standard_bvp_identification",
    ):
        assert floquet[name]
    for name in (
        "fredholm_to_monodromy_multiplicity_transfer_registered",
        "neutral_multiplier_algebraically_simple_validated",
        "nontranslation_unit_circle_exclusion_validated",
        "unstable_multiplier_count_validated",
        "attracting_or_saddle_index_validated",
    ):
        assert not floquet[name]
    assert not artifact["claim_status"][
        "outer_attracting_floquet_index_validated"
    ]


def test_outer_replay_uses_leaky_recovery_equation() -> None:
    record = _payload()["artifact"]["resolutions"][str(PRIMARY_NODE_COUNT)]
    orbit = orbit_from_resolution(record)
    derivative, _ = odd_fourier_matrices(PRIMARY_NODE_COUNT)
    nonleaky_slow = (
        derivative @ orbit.state[:, 1]
        - orbit.period
        * orbit.parameters.epsilon
        * (orbit.state[:, 0] - orbit.parameters.unfolding)
    )
    assert np.max(np.abs(nonleaky_slow)) > 2.7


@pytest.mark.parametrize(
    ("path", "replacement"),
    [
        (
            ("artifact", "claim_status", "outer_attracting_floquet_index_validated"),
            True,
        ),
        (
            (
                "artifact",
                "directed_radii_certificate",
                "validation",
                "floquet",
                "unstable_multiplier_count_validated",
            ),
            True,
        ),
        (
            ("artifact", "resolutions", "257", "state_binary64", 0, 0),
            "0x0.0p+0",
        ),
        (("manifest", "artifact_sha256"), "0" * 64),
        (("manifest", "environment", "numpy"), "hostile"),
    ],
)
def test_outer_validator_rejects_body_and_claim_tampering(
    path: tuple[object, ...], replacement: object
) -> None:
    tampered = deepcopy(_payload())
    target = tampered
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = replacement
    with pytest.raises(ValueError):
        validate_outer_high_resolution_artifact(tampered, REPOSITORY)


def test_outer_validator_rejects_source_hash_tampering() -> None:
    tampered = deepcopy(_payload())
    source = SOURCE_MANIFEST[0]
    tampered["manifest"]["source_sha256"][source] = "0" * 64
    with pytest.raises(ValueError, match="source hash changed"):
        validate_outer_high_resolution_artifact(tampered, REPOSITORY)
