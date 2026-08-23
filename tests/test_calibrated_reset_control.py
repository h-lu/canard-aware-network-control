from __future__ import annotations

import numpy as np
import pytest

from canard_control.calibrated_reset_control import (
    calibrated_block_lower_bound,
    floating_calibrated_response_diagnostic,
    floating_calibrated_target_ball_diagnostic,
)


def test_calibrated_response_is_exactly_block_diagonal() -> None:
    base = np.array([[0.2, -0.1], [1.4, 0.8]], dtype=float)
    diagnostic = floating_calibrated_response_diagnostic(base)

    assert np.array_equal(diagnostic.calibrated_response[:2, :2], base)
    assert np.array_equal(
        diagnostic.calibrated_response[:2, 2], np.zeros(2)
    )
    assert np.array_equal(
        diagnostic.calibrated_response[2, :2], np.zeros(2)
    )
    assert diagnostic.calibrated_response[2, 2] == -1.0
    assert np.isclose(
        diagnostic.floating_full_smallest_singular_value,
        min(diagnostic.floating_base_smallest_singular_value, 1.0),
    )
    assert np.isclose(
        diagnostic.floating_expected_minimum,
        diagnostic.floating_full_smallest_singular_value,
    )
    assert calibrated_block_lower_bound(0.04) == 0.04
    assert calibrated_block_lower_bound(2.0) == 1.0


def test_calibrated_target_ball_uses_periodic_and_reset_radii() -> None:
    diagnostic = floating_calibrated_target_ball_diagnostic(
        base_singular_value_lower_bound=0.04,
        base_derivative_lipschitz_bound=2.0,
        available_base_radius=0.1,
        available_calibration_half_width=0.02,
    )

    assert np.isclose(diagnostic.floating_base_radius, 0.01)
    assert np.isclose(diagnostic.floating_base_output_radius, 0.0003)
    assert np.isclose(diagnostic.floating_output_ball_radius, 0.0003)


def test_affine_base_uses_half_available_radius() -> None:
    diagnostic = floating_calibrated_target_ball_diagnostic(
        base_singular_value_lower_bound=0.5,
        base_derivative_lipschitz_bound=0.0,
        available_base_radius=0.4,
        available_calibration_half_width=0.05,
    )

    assert np.isclose(diagnostic.floating_base_radius, 0.2)
    assert np.isclose(diagnostic.floating_base_output_radius, 0.1)
    assert np.isclose(diagnostic.floating_output_ball_radius, 0.025)


@pytest.mark.parametrize(
    "kwargs",
    [
        {
            "base_singular_value_lower_bound": 0.0,
            "base_derivative_lipschitz_bound": 1.0,
            "available_base_radius": 1.0,
            "available_calibration_half_width": 1.0,
        },
        {
            "base_singular_value_lower_bound": 1.0,
            "base_derivative_lipschitz_bound": -1.0,
            "available_base_radius": 1.0,
            "available_calibration_half_width": 1.0,
        },
        {
            "base_singular_value_lower_bound": 1.0,
            "base_derivative_lipschitz_bound": 1.0,
            "available_base_radius": 0.0,
            "available_calibration_half_width": 1.0,
        },
        {
            "base_singular_value_lower_bound": 1.0,
            "base_derivative_lipschitz_bound": 1.0,
            "available_base_radius": 1.0,
            "available_calibration_half_width": float("inf"),
        },
    ],
)
def test_calibrated_target_ball_rejects_invalid_data(kwargs) -> None:
    with pytest.raises(ValueError):
        floating_calibrated_target_ball_diagnostic(**kwargs)


def test_calibrated_response_rejects_singular_or_nonfinite_base() -> None:
    with pytest.raises(ValueError):
        floating_calibrated_response_diagnostic(np.zeros((2, 2)))
    with pytest.raises(ValueError):
        floating_calibrated_response_diagnostic(
            np.array([[1.0, 0.0], [0.0, np.nan]])
        )
    with pytest.raises(ValueError):
        calibrated_block_lower_bound(0.0)
