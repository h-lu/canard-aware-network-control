"""Hostile tests for the Dobrushin periodic-attraction lift."""

from __future__ import annotations

from copy import deepcopy
from decimal import Decimal, localcontext
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys

import pytest

from canard_control.fhn_dobrushin_periodic_attraction import (
    TRACKED_RIGHT_HALF_RESULT_SHA256,
    TRACKED_TRANSVERSE_RESULT_SHA256,
    directed_dobrushin_halanay_bounds,
    dobrushin_periodic_attraction_from_payloads,
    load_dobrushin_periodic_attraction,
    reference_dobrushin_periodic_payload,
    validate_dobrushin_periodic_payload,
)
from canard_control.quadratic_period_lock_dobrushin_lift import (
    dobrushin_lift_algebra,
    dobrushin_lift_algebra_is_exact,
)


REPOSITORY = Path(__file__).resolve().parents[1]
TRANSVERSE = (
    REPOSITORY / "experiments/results/fhn_periodic_transverse_halanay.json"
)
RIGHT_HALF = (
    REPOSITORY
    / "experiments/results/fhn_synchronous_floquet_right_half_cover.json"
)
RESULT = (
    REPOSITORY
    / "experiments/results/fhn_dobrushin_periodic_attraction.json"
)
NOTE = REPOSITORY / "docs/paper-iv-dobrushin-periodic-attraction.md"
EXPECTED_RESULT_SHA256 = (
    "3123c6f2428deb60a0d24267209ddb0a9d52a514465df93dbc72af4ea06cb2ae"
)


def _parents() -> tuple[dict, dict]:
    return (
        json.loads(TRANSVERSE.read_text(encoding="utf-8")),
        json.loads(RIGHT_HALF.read_text(encoding="utf-8")),
    )


def test_exact_non_rank_one_member_reaches_the_gap_threshold() -> None:
    algebra = dobrushin_lift_algebra()
    assert dobrushin_lift_algebra_is_exact(algebra)
    assert str(algebra.topology_dobrushin_coefficient) == "1/4"
    assert not algebra.topology_is_rank_one_projector


def test_directed_weighted_halanay_certificate_closes() -> None:
    certificate = load_dobrushin_periodic_attraction()
    bounds = certificate.bounds
    assert bounds.dobrushin_gap_lower == "0.75"
    assert bounds.recovery_weight == "2.5"
    assert bounds.exponential_rate_candidate == "0.007"
    with localcontext() as context:
        context.prec = 100
        voltage = Decimal(bounds.voltage_local_decay_lower)
        recovery = Decimal(bounds.recovery_local_decay_lower)
        local = Decimal(bounds.local_decay_lower)
        beta = Decimal(bounds.delayed_total_gain_upper)
        margin = Decimal(bounds.zero_rate_margin_lower)
        rate = Decimal(bounds.exponential_rate_candidate)
        exponential = Decimal(bounds.rate_exponential_upper)
        residual = Decimal(bounds.rate_residual_lower)
        assert voltage > Decimal("1.02")
        assert recovery > Decimal("0.999")
        assert local <= min(voltage, recovery)
        assert margin <= local - beta
        assert margin > Decimal("0.087")
        assert residual <= local - rate - beta * exponential
        assert residual > Decimal("0.0058")
    assert certificate.arbitrary_finite_network_size_covered
    assert certificate.arbitrary_admitted_balanced_topology_covered
    assert certificate.uniform_transverse_exponential_rate_validated
    assert certificate.full_network_nonlinear_local_orbital_attraction_validated
    assert not certificate.arbitrary_positive_dobrushin_gap_covered
    assert not certificate.nonzero_eta_full_network_attraction_validated
    assert not certificate.uniform_nonlinear_basin_over_network_class


def test_qualitative_positive_gap_is_not_silently_promoted() -> None:
    with pytest.raises(ValueError, match="margin is nonpositive"):
        directed_dobrushin_halanay_bounds(
            current_coefficient_upper="0.82956521739209414",
            delayed_total_gain_upper="0.91288368642337782",
            maximum_active_delay_upper="11.1803398875",
            gamma="0.5",
        )


def test_enlarged_horizon_claim_is_nilpotent_and_eta_zero_only() -> None:
    certificate = load_dobrushin_periodic_attraction()
    assert certificate.enlarged_inert_horizon_adds_only_zero_multipliers_at_eta_zero
    assert not certificate.nonzero_eta_full_network_attraction_validated
    payload = reference_dobrushin_periodic_payload()
    assert payload["scope"]["eta_zero_quadratic_period_locked_model"]
    assert not payload["scope"]["nonzero_eta_full_network_attraction"]
    text = NOTE.read_text(encoding="utf-8")
    assert "nilpotent extension" in text
    assert "multiplier zero" in text
    assert "sufficiently high power of the one-period monodromy is compact" in text


def test_mutated_parent_gain_or_attraction_evidence_is_refused() -> None:
    transverse, right_half = _parents()
    hostile_transverse = deepcopy(transverse)
    hostile_transverse["certificate"]["delayed_total_gain_upper"] = "2"
    with pytest.raises(ValueError, match="margin is nonpositive"):
        dobrushin_periodic_attraction_from_payloads(
            hostile_transverse,
            right_half,
            transverse_result_sha256=TRACKED_TRANSVERSE_RESULT_SHA256,
            right_half_result_sha256=TRACKED_RIGHT_HALF_RESULT_SHA256,
        )

    hostile_right = deepcopy(right_half)
    hostile_right["certificate"][
        "synchronous_nonlinear_orbital_attraction_validated"
    ] = False
    with pytest.raises(ValueError, match="source theorem is absent"):
        dobrushin_periodic_attraction_from_payloads(
            transverse,
            hostile_right,
            transverse_result_sha256=TRACKED_TRANSVERSE_RESULT_SHA256,
            right_half_result_sha256=TRACKED_RIGHT_HALF_RESULT_SHA256,
        )


@pytest.mark.parametrize(
    "flag",
    (
        "arbitrary_positive_dobrushin_gap",
        "nonzero_eta_full_network_attraction",
        "uniform_nonlinear_basin",
        "global_synchronization",
        "biological_pulse_capture",
    ),
)
def test_payload_refuses_scope_promotion(flag: str) -> None:
    payload = reference_dobrushin_periodic_payload()
    hostile = deepcopy(payload)
    hostile["scope"][flag] = True
    with pytest.raises(ValueError, match="scope changed"):
        validate_dobrushin_periodic_payload(hostile)


def test_generated_result_is_source_bound_and_replays(tmp_path: Path) -> None:
    assert sha256(RESULT.read_bytes()).hexdigest() == EXPECTED_RESULT_SHA256
    payload = json.loads(RESULT.read_text(encoding="utf-8"))
    validate_dobrushin_periodic_payload(payload)
    provenance = payload["provenance"]
    generator = REPOSITORY / provenance["generator"]
    assert sha256(generator.read_bytes()).hexdigest() == provenance[
        "generator_sha256"
    ]
    for relative, digest in provenance["proof_source_manifest"].items():
        assert sha256((REPOSITORY / relative).read_bytes()).hexdigest() == digest
    replay = tmp_path / "dobrushin-periodic.json"
    subprocess.run(
        [sys.executable, str(generator), "--output", str(replay)],
        cwd=REPOSITORY,
        check=True,
    )
    assert replay.read_bytes() == RESULT.read_bytes()


def test_note_states_the_gain_and_scope_boundaries() -> None:
    text = NOTE.read_text(encoding="utf-8")
    for phrase in (
        "\\tau(Q)\\le1/4",
        "\\alpha_{\\gamma,c}>\\beta",
        "0.005801775562507711930814267303951807974802876856215296382",
        "each fixed finite admitted network",
        "claimed only at\n\\(\\eta=0\\)",
        "not been validated on\na nonzero \\(\\eta\\)-interval",
    ):
        assert phrase in text
