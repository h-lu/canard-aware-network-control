"""Hostile tests for the exact target order-four preparation seam."""

from __future__ import annotations

from copy import deepcopy
import json
import math
from pathlib import Path
import subprocess
import sys

import pytest
import sympy as sp

from canard_control.fixed_epsilon_target_c4_preparation_seam import (
    EXACT_TRUE_FLAGS,
    EXACT_TRANSVERSE,
    NUMERICAL_TRUE_FLAGS,
    OPEN_FALSE_FLAGS,
    PATCH_WIDTH,
    c4_prepared_history_jet,
    c4_prepared_history_transverse_derivative,
    endpoint_jets_transverse_derivative_numeric,
    exact_mixed_compatibility_defects,
    exact_shape_endpoint_matrices,
    exact_target_endpoint_jets,
    right_jet_shape_derivative,
    validate_target_c4_preparation_seam_audit,
    validate_target_c4_preparation_seam_result,
    verify_parent_result,
)
from canard_control.fixed_epsilon_target_causal_tube_candidate import (
    TargetTubeConfiguration,
)


REPOSITORY = Path(__file__).resolve().parents[1]
GENERATOR = REPOSITORY / "experiments/fixed_epsilon_target_c4_preparation_seam.py"
RESULT = REPOSITORY / "experiments/results/fixed_epsilon_target_c4_preparation_seam.json"
NOTE = REPOSITORY / "docs/fixed-epsilon-target-c4-preparation-seam.md"


def _payload() -> dict:
    return json.loads(RESULT.read_text(encoding="utf-8"))


def test_degree_nine_shapes_have_exact_left_zero_and_right_identity_jets() -> None:
    left, right = exact_shape_endpoint_matrices()
    assert left == sp.zeros(5)
    assert right == sp.eye(5)
    for jet_order in range(5):
        for derivative_order in range(5):
            assert right_jet_shape_derivative(
                -PATCH_WIDTH, jet_order, derivative_order
            ) == 0.0
            assert right_jet_shape_derivative(
                0.0, jet_order, derivative_order
            ) == (1.0 if jet_order == derivative_order else 0.0)


def test_recursive_time_and_mixed_endpoint_defects_vanish_exactly() -> None:
    endpoint = exact_target_endpoint_jets()
    assert len(endpoint) == 5
    defects = exact_mixed_compatibility_defects()
    assert len(defects) == 10
    assert all(defect == (0, 0) for _, _, defect in defects)


def test_installed_endpoint_jets_match_the_recursive_jets_in_binary64() -> None:
    config = TargetTubeConfiguration()
    for transverse in (-0.05, 0.0, 0.05):
        exact = exact_target_endpoint_jets(sp.Rational(str(transverse)))
        for order in range(5):
            actual = c4_prepared_history_jet(
                config.incoming_time, transverse, order, config
            )
            expected = tuple(float(sp.N(value, 30)) for value in exact[order])
            assert actual == pytest.approx(expected, rel=0.0, abs=3e-13)
        before = c4_prepared_history_jet(
            config.incoming_time - PATCH_WIDTH, transverse, 0, config
        )
        assert all(math.isfinite(value) for value in before)


def test_incoming_label_derivative_is_evaluated_from_exact_polynomials() -> None:
    config = TargetTubeConfiguration()
    for transverse in (-0.05, 0.0, 0.05):
        exact = exact_target_endpoint_jets()
        actual = endpoint_jets_transverse_derivative_numeric(transverse, config)
        expected = tuple(
            tuple(
                float(sp.N(sp.diff(value, EXACT_TRANSVERSE).subs(
                    EXACT_TRANSVERSE, sp.Rational(str(transverse))
                ), 30))
                for value in point
            )
            for point in exact
        )
        for actual_point, expected_point in zip(actual, expected, strict=True):
            assert actual_point == pytest.approx(
                expected_point, rel=0.0, abs=3e-13
            )
        derivative = c4_prepared_history_transverse_derivative(
            config.incoming_time - 0.25, transverse, config
        )
        assert all(math.isfinite(value) for value in derivative)


def test_ledger_rejects_weakening_and_false_chart_promotion() -> None:
    audit = _payload()["audit"]
    assert all(audit["certificate"][key] is True for key in EXACT_TRUE_FLAGS)
    assert all(audit["certificate"][key] is True for key in NUMERICAL_TRUE_FLAGS)
    assert all(audit["certificate"][key] is False for key in OPEN_FALSE_FLAGS)
    weakened = deepcopy(audit)
    weakened["certificate"][EXACT_TRUE_FLAGS[0]] = False
    with pytest.raises(ValueError, match="weakened"):
        validate_target_c4_preparation_seam_audit(weakened)
    promoted = deepcopy(audit)
    promoted["certificate"]["target_c4_chart_and_seam_compatibility_validated"] = True
    with pytest.raises(ValueError, match="promoted"):
        validate_target_c4_preparation_seam_audit(promoted)
    for key, hostile_value in (
        ("frozen_target_nu", "999"),
        ("exact_endpoint_expression_sha256", "0" * 64),
        ("exact_scope", "all claims proved"),
        ("conditional_scope", "none"),
        ("open_scope", "none"),
    ):
        tampered = deepcopy(audit)
        tampered["certificate"][key] = hostile_value
        with pytest.raises(ValueError, match="authoritative reference"):
            validate_target_c4_preparation_seam_audit(tampered)


def test_parent_manifest_and_generated_result_revalidate() -> None:
    assert all(verify_parent_result(REPOSITORY).values())
    validate_target_c4_preparation_seam_result(_payload(), REPOSITORY)


def test_generator_is_byte_reproducible(tmp_path: Path) -> None:
    replay = tmp_path / "seam.json"
    subprocess.run(
        [sys.executable, str(GENERATOR), "--output", str(replay)],
        cwd=REPOSITORY,
        env={**dict(__import__("os").environ), "PYTHONPATH": "src"},
        check=True,
    )
    assert replay.read_bytes() == RESULT.read_bytes()


def test_note_keeps_the_exact_seam_separate_from_the_open_chart() -> None:
    normalized = " ".join(NOTE.read_text(encoding="utf-8").split())
    assert "incoming seam is exact" in normalized
    assert "twenty scalar" in normalized
    assert "combined flag" in normalized
    assert "remains false" in normalized
    assert "target graph" in normalized
