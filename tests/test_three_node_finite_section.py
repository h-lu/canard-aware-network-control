"""Regression checks for the illustrative three-node finite-section run."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pytest

from canard_control.three_node_finite_section import (
    ThreeNodeParameters,
    convergence_row,
    exact_fold_rhs,
    projected_rhs_difference,
)


REPOSITORY = Path(__file__).resolve().parents[1]
ARCHIVE = (
    REPOSITORY
    / "experiments"
    / "results"
    / "three_node_finite_section_diagnostic.json"
)


def test_exact_three_node_coefficient_and_projection_cancellation() -> None:
    parameters = ThreeNodeParameters(delta=0.05)
    assert parameters.predicted_coefficient == pytest.approx(-1.0 / 3.0)
    assert parameters.singular_center == pytest.approx(-0.25)
    varied = ThreeNodeParameters(
        delta=0.05, sigma=0.4, coupling_gain=1.5, delay=2.0
    )
    assert varied.predicted_coefficient == pytest.approx(-0.4)

    current = np.array([0.2, -0.3, 0.10, -0.04, -0.06])
    delayed = np.array([-0.1, 0.2, -0.02, 0.03, -0.01])
    assert projected_rhs_difference(
        current,
        delayed,
        parameters=parameters,
        zeta=0.04,
        nu=-0.25,
    ) == 0.0

    control_minus = exact_fold_rhs(
        current,
        delayed,
        parameters=parameters,
        zeta=-0.04,
        nu=-0.25,
        coincident_delay_control=True,
    )
    control_plus = exact_fold_rhs(
        current,
        delayed,
        parameters=parameters,
        zeta=0.04,
        nu=-0.25,
        coincident_delay_control=True,
    )
    np.testing.assert_array_equal(control_minus, control_plus)


def test_current_equation_gives_the_predicted_sign_and_scale() -> None:
    row = convergence_row(
        delta=0.05,
        section_half_width=3.0,
        zeta_step=0.04,
        rtol=2.0e-8,
        atol=2.0e-10,
        max_step=0.10,
        root_xtol=2.0e-8,
        root_rtol=2.0e-8,
    )
    assert -0.345 < row.quotient < -0.325
    assert row.root_residual_max < 2.0e-7


def test_archived_figure_values_preserve_scope_and_overall_trend() -> None:
    payload = json.loads(ARCHIVE.read_text(encoding="utf-8"))
    assert payload["status"] == "numerical diagnostic; not used in any proof"
    assert "D_3^fin" in payload["definition"]["not_computed"]
    rows = payload["convergence_rows"]
    assert len(rows) >= 5
    target = payload["parameters"]["predicted_coefficient"]
    assert target == pytest.approx(-1.0 / 3.0)
    assert abs(rows[-1]["quotient"] - target) < abs(rows[0]["quotient"] - target)
    assert payload["coincident_delay_control"]["quotient"] == 0.0
    assert payload["checks"]["projection_rhs_residual"] == 0.0
    for relative, expected in payload["source_sha256"].items():
        digest = hashlib.sha256((REPOSITORY / relative).read_bytes()).hexdigest()
        assert digest == expected
