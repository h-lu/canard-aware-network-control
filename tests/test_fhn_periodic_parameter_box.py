"""Regression tests for the directed FHN parameter-box certificate."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from canard_control.directed_interval import DirectedInterval
from canard_control.fhn_periodic_parameter_box import (
    _midpoint_singular_lower,
    _symmetric_decimal_interval,
)


def test_declared_gain_box_contains_its_exact_decimal_endpoints() -> None:
    interval = _symmetric_decimal_interval(0.2, "1e-12", 160)
    lower = DirectedInterval.from_decimal("0.199999999999", 160)
    upper = DirectedInterval.from_decimal("0.200000000001", 160)
    assert interval.lower <= lower.lower
    assert interval.upper >= upper.upper


def test_directed_two_by_two_singular_bound_is_below_binary_svd() -> None:
    matrix = np.array(
        [[0.0366998279955, 0.136339460688], [-3.64561577, -6.13633797]]
    )
    lower = float(_midpoint_singular_lower(matrix, 160))
    observed = float(np.linalg.svd(matrix, compute_uv=False)[-1])
    assert 0.038 < lower <= observed


def test_tracked_parameter_box_keeps_unproved_issue_gates_false() -> None:
    path = (
        Path(__file__).resolve().parents[1]
        / "experiments/results/fhn_periodic_parameter_box.json"
    )
    payload = json.loads(path.read_text(encoding="utf-8"))
    validation = payload["validation"]
    continuation = validation["continuation"]
    extrema = validation["extrema"]
    response = validation["response"]

    assert continuation["cutoff"] == 144
    assert continuation["real_conjugate_dimension"] == 579
    assert continuation["residual_support_half_bandwidth"] == 192
    assert validation["d1_validated"]
    assert float(continuation["radii_margin_lower"]) > 0.0
    assert float(continuation["analytic_tail_inverse_l1_upper"]) > 0.0
    assert float(continuation["global_preconditioner_l1_upper"]) == max(
        float(continuation["approximate_inverse_l1_upper"]),
        float(continuation["analytic_tail_inverse_l1_upper"]),
    )
    assert validation["d3_validated"]
    assert float(extrema["maximum_curvature_upper"]) < 0.0
    assert float(extrema["minimum_curvature_lower"]) > 0.0
    assert validation["d4_response_lower_bound_validated"]
    assert response["response_box_validated"]
    assert response["sensitivity_budgets"] is not None
    assert [item["control"] for item in response["sensitivity_budgets"]] == [
        "kappa_1",
        "kappa_3",
    ]
    for item, total_error in zip(
        response["sensitivity_budgets"],
        response["sensitivity_error_upper"],
        strict=True,
    ):
        for field in (
            "finite_preconditioned_residual_upper",
            "finite_interval_remainder_upper",
            "analytic_tail_residual_upper",
            "base_preconditioned_residual_upper",
            "global_preconditioner_l1_upper",
            "state_jacobian_variation_upper",
            "period_column_variation_upper",
            "slow_equation_variation_upper",
            "gain_forcing_variation_upper",
            "raw_variation_upper",
            "preconditioned_variation_upper",
            "exact_sensitivity_error_upper",
        ):
            assert float(item[field]) >= 0.0
        residual_parts = sum(
            float(item[field])
            for field in (
                "finite_preconditioned_residual_upper",
                "finite_interval_remainder_upper",
                "analytic_tail_residual_upper",
            )
        )
        assert np.isclose(
            residual_parts,
            float(item["base_preconditioned_residual_upper"]),
            rtol=1e-12,
            atol=1e-30,
        )
        assert float(item["global_preconditioner_l1_upper"]) == float(
            continuation["global_preconditioner_l1_upper"]
        )
        raw_parts = sum(
            float(item[field])
            for field in (
                "state_jacobian_variation_upper",
                "period_column_variation_upper",
                "slow_equation_variation_upper",
                "gain_forcing_variation_upper",
            )
        )
        assert np.isclose(
            raw_parts,
            float(item["raw_variation_upper"]),
            rtol=1e-12,
            atol=1e-30,
        )
        assert np.isclose(
            float(item["global_preconditioner_l1_upper"])
            * float(item["raw_variation_upper"]),
            float(item["preconditioned_variation_upper"]),
            rtol=1e-12,
            atol=1e-30,
        )
        expected_error = (
            float(item["base_preconditioned_residual_upper"])
            + float(item["preconditioned_variation_upper"])
        ) / (1.0 - float(continuation["uniform_contraction_upper"]))
        assert np.isclose(
            expected_error,
            float(item["exact_sensitivity_error_upper"]),
            rtol=1e-12,
            atol=1e-30,
        )
        assert float(item["exact_sensitivity_error_upper"]) == float(
            total_error
        )
    assert float(response["smallest_singular_value_lower"]) > 0.016
    assert float(response["response_frobenius_radius_upper"]) < 0.022
    for row in range(2):
        for column in range(2):
            midpoint = response["midpoint_binary64"][row][column]
            assert float(response["response_lower"][row][column]) <= midpoint
            assert midpoint <= float(response["response_upper"][row][column])

    # These assertions deliberately prevent promotion beyond the generated
    # directed record.  In particular the second-sensitivity Lipschitz gate
    # and the remaining compact Bloch arc remain open even if D4 closes.
    assert not response["derivative_lipschitz_bound_supplied"]
    assert not validation["issue_15_closed"]
    assert "Fredholm-to-monodromy transfer" not in " ".join(
        validation["remaining_gates"]
    )
