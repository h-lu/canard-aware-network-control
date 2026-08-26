"""Tests for the leaky finite-network transverse Halanay theorem."""

from __future__ import annotations

from copy import deepcopy
from decimal import Decimal, localcontext
from fractions import Fraction
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest
import sympy as sp

from canard_control.leaky_dobrushin_transverse_halanay import (
    GENERATOR_RELATIVE_PATH,
    NOTE_RELATIVE_PATH,
    RESULT_RELATIVE_PATH,
    SOURCE_MANIFEST,
    build_leaky_dobrushin_transverse_certificate,
    directed_leaky_dobrushin_bounds,
    validate_leaky_dobrushin_transverse_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]
RESULT = REPOSITORY / RESULT_RELATIVE_PATH


def _payload() -> dict[str, object]:
    value = json.loads(RESULT.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_exact_weighted_oscillation_coefficients() -> None:
    eps = sp.Rational(1, 5)
    k1 = sp.Rational(1, 250)
    k3 = sp.Rational(1, 200)
    radius = sp.Rational(5, 2)
    gap = sp.Rational(1, 2)
    weight = sp.Integer(3)
    current = 1 - eps * k1
    delayed = eps * (k1 + 3 * k3 * radius**2)
    voltage = 3 * gap - current - 1 / weight
    recovery = 2 * gap + eps - weight * eps
    assert current == sp.Rational(1249, 1250)
    assert delayed == sp.Rational(391, 20000)
    assert voltage == sp.Rational(314, 1875)
    assert recovery == sp.Rational(3, 5)


def test_directed_halanay_margins_are_strict() -> None:
    bounds = directed_leaky_dobrushin_bounds()
    assert Decimal(bounds.zero_rate_margin_lower) > Decimal("0.147")
    assert Decimal(bounds.rate_residual_lower) > Decimal("0.007")
    assert Decimal(bounds.delayed_total_gain_upper) < Decimal("0.0195500000000001")


def test_both_exact_periodic_orbits_lie_in_declared_strip() -> None:
    certificate = build_leaky_dobrushin_transverse_certificate(REPOSITORY)
    assert certificate.inner.exact_periodic_orbit_strip_validated
    assert certificate.outer.exact_periodic_orbit_strip_validated
    assert Fraction(certificate.quiet_centered_voltage_abs_upper) < Fraction(5, 2)
    assert Decimal(certificate.inner.strict_strip_margin_lower) > 0
    assert Decimal(certificate.outer.strict_strip_margin_lower) > 0
    assert certificate.inner.phase_sample_count == 1024
    assert certificate.outer.phase_sample_count == 1024
    assert Decimal(certificate.inner.exact_centered_voltage_abs_upper) < Decimal("2.5")
    assert Decimal(certificate.outer.exact_centered_voltage_abs_upper) < Decimal("2.5")
    for branch in (certificate.inner, certificate.outer):
        weighted = Decimal(
            branch.exponentially_weighted_history_monodromy_norm_upper
        )
        unweighted = Decimal(
            branch.unweighted_history_monodromy_norm_upper
        )
        multiplier = Decimal(branch.transverse_multiplier_modulus_upper)
        assert Decimal(0) < weighted < unweighted < Decimal(1)
        assert multiplier == weighted


def test_history_operator_and_multiplier_exponents_are_not_conflated() -> None:
    certificate = build_leaky_dobrushin_transverse_certificate(REPOSITORY)
    rate = Decimal(certificate.bounds.exponential_rate)
    delay = Decimal(certificate.bounds.maximum_delay_upper)
    with localcontext() as context:
        context.prec = 100
        for branch in (certificate.inner, certificate.outer):
            period = Decimal(branch.minimum_period_lower)
            expected_unweighted = (-rate * (period - delay)).exp()
            expected_weighted = (-rate * period).exp()
            stored_unweighted = Decimal(
                branch.unweighted_history_monodromy_norm_upper
            )
            stored_weighted = Decimal(
                branch.exponentially_weighted_history_monodromy_norm_upper
            )
            # This replay uses the separately serialized outward endpoints,
            # so its last digits can lie on either side of the value computed
            # from the original MPFR endpoints.
            assert abs(stored_unweighted - expected_unweighted) < Decimal(
                "1e-45"
            )
            assert abs(stored_weighted - expected_weighted) < Decimal(
                "1e-45"
            )


def test_claim_ledger_stops_before_collective_indices_and_onset() -> None:
    certificate = build_leaky_dobrushin_transverse_certificate(REPOSITORY)
    assert certificate.arbitrary_finite_network_size_covered
    assert certificate.arbitrary_admitted_balanced_topology_covered
    assert certificate.collective_transverse_splitting_invariant_proved
    assert certificate.complexified_transverse_diameter_estimate_proved
    assert certificate.exponentially_weighted_history_contraction_proved
    assert certificate.full_network_quiet_local_exponential_stability_proved
    assert certificate.all_noncollective_periodic_multipliers_inside_rate_disk_proved
    assert not certificate.inner_full_network_one_unstable_multiplier_validated
    assert not certificate.outer_full_network_orbital_attraction_validated
    assert not certificate.uniform_nonlinear_basin_radius_validated
    assert not certificate.physical_pulse_onset_lift_validated
    assert not certificate.general_closing_gap_networks_covered


def test_tracked_result_revalidates_and_binds_sources() -> None:
    payload = _payload()
    validate_leaky_dobrushin_transverse_result(payload, REPOSITORY)
    hashes = payload["manifest"]["source_sha256"]
    for relative in SOURCE_MANIFEST:
        assert hashes[relative] == sha256(
            (REPOSITORY / relative).read_bytes()
        ).hexdigest()


def test_validator_rejects_claim_and_manifest_tampering() -> None:
    payload = _payload()
    promoted = deepcopy(payload)
    promoted["certificate"][
        "outer_full_network_orbital_attraction_validated"
    ] = True
    with pytest.raises(ValueError, match="differs from directed replay"):
        validate_leaky_dobrushin_transverse_result(promoted, REPOSITORY)
    extra = deepcopy(payload)
    extra["manifest"]["extra"] = "forbidden"
    with pytest.raises(ValueError, match="manifest schema changed"):
        validate_leaky_dobrushin_transverse_result(extra, REPOSITORY)
    parent = deepcopy(payload)
    parent_paths = parent["manifest"]["parent_result_sha256"]
    first_parent = next(iter(parent_paths))
    parent_paths[first_parent] = "0" * 64
    with pytest.raises(ValueError, match="parent result hash changed"):
        validate_leaky_dobrushin_transverse_result(parent, REPOSITORY)


def test_generator_replays_tracked_bytes(tmp_path: Path) -> None:
    replay = tmp_path / "leaky-network-halanay.json"
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


def test_note_states_general_network_scope_and_open_gates() -> None:
    text = " ".join(
        (REPOSITORY / NOTE_RELATIVE_PATH).read_text(encoding="utf-8").split()
    )
    assert "every finite topology" in text
    assert "Dobrushin" in text
    assert "complex transverse variational solution" in text
    assert "multiplier disk has the stronger radius" in text
    assert "does not promote network orbital attraction" in text
    assert "pulse capture" in text
