"""Tests for the exact leaky reduced-history factorization."""

from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

from canard_control.leaky_reduced_history import (
    DEFAULT_COMMAND,
    FLOQUET_RESULT_RELATIVE_PATH,
    GENERATOR_RELATIVE_PATH,
    NOTE_RELATIVE_PATH,
    PULSE_RESULT_RELATIVE_PATH,
    RESULT_RELATIVE_PATH,
    SOURCE_MANIFEST,
    TRACKED_FLOQUET_RESULT_SHA256,
    TRACKED_PULSE_RESULT_SHA256,
    build_leaky_reduced_history_certificate,
    exact_recovery_lift_defects,
    validate_leaky_reduced_history_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]
RESULT = REPOSITORY / RESULT_RELATIVE_PATH


def _payload() -> dict[str, object]:
    value = json.loads(RESULT.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_recovery_lift_and_derivative_are_exact() -> None:
    assert exact_recovery_lift_defects() == (0, 0, 0, 0)


def test_exact_factorization_claims_and_open_boundary() -> None:
    certificate = build_leaky_reduced_history_certificate(REPOSITORY)
    assert certificate.projection_has_continuous_split_right_inverse_proved
    assert certificate.full_semiflow_factors_through_reduced_semiflow_proved
    assert certificate.global_orbital_stable_set_pullback_equality_proved
    assert certificate.local_stable_manifold_codimension_preserved_by_pullback_proved
    assert certificate.inner_monodromy_nonzero_spectrum_reduction_proved
    assert certificate.outer_monodromy_nonzero_spectrum_reduction_proved
    assert certificate.old_recovery_history_fiber_contributes_only_zero_spectrum_proved
    assert certificate.physical_pulse_terminal_history_compatible_proved
    assert certificate.pulse_crossing_derivative_uses_only_reduced_terminal_derivative_proved
    assert not certificate.inner_reduced_dichotomy_validated
    assert not certificate.inner_stable_manifold_validated
    assert not certificate.physical_pulse_stable_manifold_crossing_validated
    assert not certificate.two_sided_physical_onset_validated


def test_periods_are_strictly_longer_than_maximum_memory() -> None:
    certificate = build_leaky_reduced_history_certificate(REPOSITORY)
    maximum_delay = 5 * 5**0.5
    assert float(certificate.inner_period_lower) > maximum_delay
    assert float(certificate.outer_period_lower) > maximum_delay


def test_tracked_result_revalidates_and_binds_sources() -> None:
    payload = _payload()
    validate_leaky_reduced_history_result(payload, REPOSITORY)
    hashes = payload["manifest"]["source_sha256"]
    for relative in SOURCE_MANIFEST:
        assert hashes[relative] == sha256(
            (REPOSITORY / relative).read_bytes()
        ).hexdigest()
    assert payload["manifest"]["parent_result_sha256"] == {
        PULSE_RESULT_RELATIVE_PATH: TRACKED_PULSE_RESULT_SHA256,
        FLOQUET_RESULT_RELATIVE_PATH: TRACKED_FLOQUET_RESULT_SHA256,
    }
    assert sha256(
        (REPOSITORY / PULSE_RESULT_RELATIVE_PATH).read_bytes()
    ).hexdigest() == TRACKED_PULSE_RESULT_SHA256
    assert sha256(
        (REPOSITORY / FLOQUET_RESULT_RELATIVE_PATH).read_bytes()
    ).hexdigest() == TRACKED_FLOQUET_RESULT_SHA256


def test_validator_rejects_claim_and_manifest_tampering() -> None:
    payload = _payload()
    promoted = deepcopy(payload)
    promoted["certificate"]["inner_stable_manifold_validated"] = True
    with pytest.raises(ValueError, match="differs from replay"):
        validate_leaky_reduced_history_result(promoted, REPOSITORY)
    extra = deepcopy(payload)
    extra["manifest"]["extra"] = True
    with pytest.raises(ValueError, match="manifest schema changed"):
        validate_leaky_reduced_history_result(extra, REPOSITORY)

    extra_certificate = deepcopy(payload)
    extra_certificate["certificate"]["extra"] = True
    with pytest.raises(ValueError, match="differs from replay"):
        validate_leaky_reduced_history_result(extra_certificate, REPOSITORY)

    command = deepcopy(payload)
    command["manifest"]["default_command"] = DEFAULT_COMMAND + " --quiet"
    with pytest.raises(ValueError, match="default_command changed"):
        validate_leaky_reduced_history_result(command, REPOSITORY)

    arithmetic = deepcopy(payload)
    arithmetic["manifest"]["arithmetic"] = "binary64"
    with pytest.raises(ValueError, match="arithmetic changed"):
        validate_leaky_reduced_history_result(arithmetic, REPOSITORY)

    source = deepcopy(payload)
    source["manifest"]["source_sha256"][SOURCE_MANIFEST[0]] = "0" * 64
    with pytest.raises(ValueError, match="source hash changed"):
        validate_leaky_reduced_history_result(source, REPOSITORY)

    parent = deepcopy(payload)
    parent["manifest"]["parent_result_sha256"][
        FLOQUET_RESULT_RELATIVE_PATH
    ] = "0" * 64
    with pytest.raises(ValueError, match="parent hashes changed"):
        validate_leaky_reduced_history_result(parent, REPOSITORY)


def test_generator_replays_tracked_bytes(tmp_path: Path) -> None:
    replay = tmp_path / "leaky-reduced-history.json"
    environment = {**os.environ, "PYTHONPATH": "src"}
    subprocess.run(
        [
            sys.executable,
            str(REPOSITORY / GENERATOR_RELATIVE_PATH),
            "--output",
            str(replay),
        ],
        cwd=REPOSITORY,
        env=environment,
        check=True,
    )
    assert replay.read_bytes() == RESULT.read_bytes()


def test_note_states_reduction_and_open_onset_gate() -> None:
    text = " ".join(
        (REPOSITORY / NOTE_RELATIVE_PATH).read_text(encoding="utf-8").split()
    )
    assert "exact factorization" in text
    assert "nonzero spectra" in text
    assert "old-recovery history fiber contributes only zero spectrum" in text
    assert "direct-sum identity" in text
    assert "source manifest" in text
    assert "does not validate" in text
