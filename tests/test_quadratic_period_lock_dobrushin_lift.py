"""Hostile tests for the Dobrushin full-network quadratic-root lift."""

from __future__ import annotations

from copy import deepcopy
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys

import pytest
import sympy as sp

from canard_control.quadratic_period_lock_dobrushin_lift import (
    dobrushin_lift_algebra,
    dobrushin_lift_algebra_is_exact,
    reference_dobrushin_lift_certificate,
    reference_dobrushin_lift_payload,
    semigroup_constants,
    validate_dobrushin_lift_payload,
)


REPOSITORY = Path(__file__).resolve().parents[1]
SOURCE = (
    REPOSITORY / "src/canard_control/quadratic_period_lock_dobrushin_lift.py"
)
RESULT = (
    REPOSITORY
    / "experiments/results/quadratic_period_lock_dobrushin_lift.json"
)
NOTE = REPOSITORY / "docs/quadratic-period-lock-dobrushin-full-network.md"


def test_exact_non_rank_one_balanced_witness() -> None:
    algebra = dobrushin_lift_algebra()
    assert dobrushin_lift_algebra_is_exact(algebra)
    assert algebra.topology_dobrushin_coefficient == sp.Rational(1, 4)
    assert not algebra.topology_is_rank_one_projector
    assert not algebra.layer_sum_equals_topology
    assert not algebra.layer_sum_equals_projector
    assert algebra.quadratic_carrier_transverse_output == sp.zeros(3, 1)
    assert algebra.quadratic_carrier_cross_term == 0


def test_uniform_triangular_semigroup_constants() -> None:
    prefactor, rate = semigroup_constants(Fraction(1, 4))
    assert prefactor == 5
    assert rate == Fraction(1, 2)
    with pytest.raises(ValueError, match="Dobrushin gap"):
        semigroup_constants(Fraction(0, 1))


def test_certificate_promotes_only_the_canonical_graph_class() -> None:
    certificate = reference_dobrushin_lift_certificate()
    assert certificate.transverse_block_semigroup_uniformly_exponentially_stable
    assert certificate.fixed_support_history_graph_model_fit_proved
    assert certificate.canonical_retained_transverse_graph_unique_and_zero
    assert certificate.full_network_canonical_selected_root_unique_for_admitted_class
    assert certificate.constants_uniform_in_network_size
    assert not certificate.arbitrary_balanced_topology_without_mixing_gap_covered
    assert not certificate.arbitrary_rfde_history_connection_unique_outside_graph_tube
    assert not certificate.fixed_epsilon_one_fifth_root_response_validated
    assert not certificate.input_independent_physical_onset_identified
    assert not certificate.pulse_quiet_basin_or_no_return_proved


@pytest.mark.parametrize(
    "key",
    [
        "arbitrary_balanced_without_gap",
        "arbitrary_history_global_uniqueness",
        "fixed_epsilon_one_fifth",
        "physical_onset",
        "biological_basin_no_return",
    ],
)
def test_payload_rejects_false_promotions(key: str) -> None:
    payload = reference_dobrushin_lift_payload()
    hostile = deepcopy(payload)
    hostile["scope"][key] = True
    with pytest.raises(ValueError, match="scope does not match"):
        validate_dobrushin_lift_payload(hostile)


def test_generated_record_is_source_bound() -> None:
    payload = json.loads(RESULT.read_text(encoding="utf-8"))
    validate_dobrushin_lift_payload(payload["audit"])
    assert payload["manifest"]["proof_source_sha256"] == sha256(
        SOURCE.read_bytes()
    ).hexdigest()


def test_generator_replays_byte_for_byte(tmp_path: Path) -> None:
    output = tmp_path / "dobrushin-lift.json"
    subprocess.run(
        [
            sys.executable,
            str(
                REPOSITORY
                / "experiments/quadratic_period_lock_dobrushin_lift.py"
            ),
            "--output",
            str(output),
        ],
        check=True,
        cwd=REPOSITORY,
    )
    assert output.read_bytes() == RESULT.read_bytes()


def test_note_keeps_all_promotion_boundaries_explicit() -> None:
    text = NOTE.read_text(encoding="utf-8")
    assert "canonical retained graph" in text
    assert "arbitrary RFDE histories outside that graph tube" in text
    assert "tau(Q_N)\\le1-\\gamma" in text
    assert "(1+\\gamma^{-1})e^{-2\\gamma t}" in text
    assert "-\\frac{\\Theta_*}{2}\\delta^3\\eta" in text
    assert "fixed-\\(\\varepsilon=1/5\\)" in text
    assert "input-independent physical onset" in text
