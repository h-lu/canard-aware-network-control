"""Regression and hostile-tamper tests for the inner branch artifact."""

from __future__ import annotations

from copy import deepcopy
from decimal import Decimal
from hashlib import sha256
import json
from pathlib import Path

import numpy as np
import pytest

from canard_control.leaky_periodic_branch_artifact import (
    CLAIM_STATUS,
    EXPECTED_ARTIFACT_SHA256,
    RESULT_RELATIVE_PATHS,
    SOURCE_MANIFEST,
    _binary64_array,
    _collocation_system,
    _compare_directed_replay,
    _validate_directed_gate_semantics,
    canonical_sha256,
    orbit_from_artifact,
    validate_leaky_periodic_branch_artifact,
)
from canard_control.fhn_periodic_candidate import odd_fourier_matrices


REPOSITORY = Path(__file__).resolve().parents[1]
RESULT = REPOSITORY / RESULT_RELATIVE_PATHS["inner_saddle_candidate"]
EXPECTED_RESULT_SHA256 = (
    "e978346a121c366473c3f826c03f3c187719e8bd05d2c3a848bd3651348f2043"
)


def _payload() -> dict:
    return json.loads(RESULT.read_text(encoding="utf-8"))


def test_inner_artifact_is_source_bound_and_replays_binary64_state() -> None:
    raw = RESULT.read_bytes()
    assert sha256(raw).hexdigest() == EXPECTED_RESULT_SHA256
    payload = json.loads(raw)
    orbit = validate_leaky_periodic_branch_artifact(payload, REPOSITORY)
    artifact = payload["artifact"]
    manifest = payload["manifest"]

    assert artifact["branch"] == "inner_saddle_candidate"
    assert len(orbit.phase_nodes) == 129
    assert orbit.state.shape == (129, 2)
    assert orbit.period == float.fromhex(
        artifact["collocation"]["period"]["binary64_hex"]
    )
    assert np.array_equal(
        orbit.phase_nodes, np.arange(129, dtype=float) / 129
    )
    stored_state = artifact["collocation"]["state_binary64"]
    assert [
        [float(value).hex() for value in row] for row in orbit.state
    ] == stored_state
    assert canonical_sha256(artifact) == EXPECTED_ARTIFACT_SHA256[
        "inner_saddle_candidate"
    ]
    assert manifest["artifact_sha256"] == canonical_sha256(artifact)
    for relative in SOURCE_MANIFEST:
        assert manifest["source_sha256"][relative] == sha256(
            (REPOSITORY / relative).read_bytes()
        ).hexdigest()


def test_inner_candidate_metrics_and_directed_margin_are_not_proof_flags() -> None:
    payload = _payload()
    validate_leaky_periodic_branch_artifact(payload, REPOSITORY)
    artifact = payload["artifact"]
    orbit = orbit_from_artifact(artifact)
    directed = artifact["directed_radii_prototype"]["validation"]

    assert orbit.collocation_residual_inf < 2.0e-13
    assert orbit.oversampled_residual_inf < 2.0e-13
    assert orbit.spectral_tail_l1 < 1.0e-14
    assert directed["directed_radii_inequality_candidate_closed"]
    assert directed["finite"]["finite_inverse_validated"]
    assert directed["blocks"]["full_point_inverse_gate"]
    assert directed["correction"]["radii_polynomial_negative"]
    assert float(directed["correction"]["radii_margin_lower"]) > 9.0e-6

    assert artifact["claim_status"] == CLAIM_STATUS
    assert not directed["formula_adaptation_independently_audited"]
    assert not directed["periodic_rfde_orbit_validated"]
    assert not directed["phase_bordered_rfde_inverse_validated"]
    for name, value in directed["floquet"].items():
        if name != "required_next_certificates":
            assert value is False


def test_stored_mapping_replays_the_leaky_not_nonleaky_collocation() -> None:
    artifact = _payload()["artifact"]
    orbit = orbit_from_artifact(artifact)
    collocation = artifact["collocation"]
    reference = _binary64_array(
        collocation["phase_reference_binary64"], "phase reference", 2
    )
    residual, _ = _collocation_system(
        orbit.state, orbit.period, orbit.parameters, reference
    )
    derivative, _ = odd_fourier_matrices(len(orbit.state))
    nonleaky_slow = (
        derivative @ orbit.state[:, 1]
        - orbit.period
        * orbit.parameters.epsilon
        * (orbit.state[:, 0] - orbit.parameters.unfolding)
    )
    model_parameters = artifact["model"]["parameters"]
    stored_delays = tuple(
        float.fromhex(model_parameters[name]["binary64_hex"])
        for name in ("tau_0", "tau_1")
    )

    assert orbit.parameters.physical_delays == stored_delays
    assert np.max(np.abs(residual[:-1])) < 2.0e-13
    assert abs(residual[-1]) < 1.0e-16
    assert np.max(np.abs(nonleaky_slow)) > 2.7


def test_outer_branch_is_explicitly_unregistered_and_absent() -> None:
    assert EXPECTED_ARTIFACT_SHA256["outer_pulse"] is None
    assert not (REPOSITORY / RESULT_RELATIVE_PATHS["outer_pulse"]).exists()


def test_directed_replay_tolerates_only_blas_last_bit_drift() -> None:
    stored = _payload()["artifact"]["directed_radii_prototype"][
        "validation"
    ]
    replayed = deepcopy(stored)
    value = Decimal(replayed["finite"]["approximate_inverse_l1_upper"])
    replayed["finite"]["approximate_inverse_l1_upper"] = str(
        value * (Decimal(1) + Decimal("5e-11"))
    )
    _compare_directed_replay(stored, replayed)

    escaped = deepcopy(stored)
    value = Decimal(escaped["finite"]["approximate_inverse_l1_upper"])
    escaped["finite"]["approximate_inverse_l1_upper"] = str(
        value * (Decimal(1) + Decimal("1e-8"))
    )
    with pytest.raises(ValueError, match="left the replay tolerance"):
        _compare_directed_replay(stored, escaped)


def test_directed_replay_never_accepts_a_radii_sign_flip() -> None:
    flipped = deepcopy(
        _payload()["artifact"]["directed_radii_prototype"]["validation"]
    )
    flipped["correction"]["radii_margin_lower"] = "-1e-6"
    with pytest.raises(ValueError, match="strict signs"):
        _validate_directed_gate_semantics(flipped, "hostile")


def test_directed_replay_requires_margin_after_defect_buffer() -> None:
    thin = deepcopy(
        _payload()["artifact"]["directed_radii_prototype"]["validation"]
    )
    thin["correction"]["radii_margin_lower"] = "1e-9"
    with pytest.raises(ValueError, match="exhausts a strict gate margin"):
        _compare_directed_replay(thin, deepcopy(thin))


@pytest.mark.parametrize(
    ("path", "replacement"),
    [
        (
            ("artifact", "claim_status", "periodic_rfde_orbit_validated"),
            True,
        ),
        (
            (
                "artifact",
                "directed_radii_prototype",
                "validation",
                "periodic_rfde_orbit_validated",
            ),
            True,
        ),
        (
            (
                "artifact",
                "directed_radii_prototype",
                "validation",
                "floquet",
                "unstable_multiplier_count_validated",
            ),
            True,
        ),
        (
            (
                "artifact",
                "directed_radii_prototype",
                "settings",
                "cutoff",
            ),
            191,
        ),
        (
            ("artifact", "collocation", "state_binary64", 0, 0),
            "0x0.0p+0",
        ),
        (
            ("manifest", "artifact_sha256"),
            "0" * 64,
        ),
    ],
)
def test_strict_validator_rejects_artifact_and_claim_tampering(
    path: tuple[object, ...], replacement: object
) -> None:
    tampered = deepcopy(_payload())
    target = tampered
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = replacement
    with pytest.raises(ValueError):
        validate_leaky_periodic_branch_artifact(tampered, REPOSITORY)


def test_strict_validator_rejects_source_hash_tampering() -> None:
    tampered = deepcopy(_payload())
    source = SOURCE_MANIFEST[0]
    tampered["manifest"]["source_sha256"][source] = "0" * 64
    with pytest.raises(ValueError, match="source hash changed"):
        validate_leaky_periodic_branch_artifact(tampered, REPOSITORY)


def test_loader_rejects_noncanonical_phase_hex_even_before_proof_use() -> None:
    tampered = deepcopy(_payload()["artifact"])
    tampered["collocation"]["phase_nodes_binary64"][0] = "0x0p+0"
    with pytest.raises(ValueError, match="noncanonical"):
        orbit_from_artifact(tampered)
