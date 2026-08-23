"""Finite-dimensional constants for a calibrated reset coordinate.

The infinite-dimensional calibration theorem is proved in
docs/paper-iv-calibrated-reset-coordinate.md. This module evaluates the
block-diagonal response and its conservative product-neighborhood radius. It
does not construct an RFDE separator or validate a periodic FHN parameter
box.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite

import numpy as np


@dataclass(frozen=True)
class FloatingCalibratedResponseDiagnostic:
    """Binary64 screen for the block diagonal matrix (B, -1)."""

    base_response: np.ndarray
    calibrated_response: np.ndarray
    floating_base_smallest_singular_value: float
    floating_full_smallest_singular_value: float
    floating_expected_minimum: float


@dataclass(frozen=True)
class FloatingCalibratedTargetBallDiagnostic:
    """Binary64 evaluation of the exact product-radius formula."""

    base_singular_value_lower_bound: float
    base_derivative_lipschitz_bound: float
    available_base_radius: float
    available_calibration_half_width: float
    floating_base_radius: float
    floating_base_output_radius: float
    floating_output_ball_radius: float


def calibrated_block_lower_bound(
    base_smallest_singular_value_lower_bound: float,
) -> float:
    """Propagate a supplied rigorous base lower bound through diag(B, -1)."""

    beta = float(base_smallest_singular_value_lower_bound)
    if not isfinite(beta) or beta <= 0.0:
        raise ValueError("base singular-value lower bound must be positive")
    return min(beta, 1.0)


def floating_calibrated_response_diagnostic(
    base_response: np.ndarray,
) -> FloatingCalibratedResponseDiagnostic:
    """Screen a floating response; this is not a directed certificate."""

    base = np.asarray(base_response, dtype=float)
    if base.shape != (2, 2):
        raise ValueError("base_response must have shape (2, 2)")
    if not np.all(np.isfinite(base)):
        raise ValueError("base_response must be finite")
    base_singular = float(np.linalg.svd(base, compute_uv=False)[-1])
    if base_singular <= 0.0:
        raise ValueError("base_response must be nonsingular")
    response = np.block(
        [
            [base, np.zeros((2, 1), dtype=float)],
            [np.zeros((1, 2), dtype=float), -np.ones((1, 1), dtype=float)],
        ]
    )
    full_singular = float(np.linalg.svd(response, compute_uv=False)[-1])
    lower = min(base_singular, 1.0)
    return FloatingCalibratedResponseDiagnostic(
        base_response=base,
        calibrated_response=response,
        floating_base_smallest_singular_value=base_singular,
        floating_full_smallest_singular_value=full_singular,
        floating_expected_minimum=float(lower),
    )


def floating_calibrated_target_ball_diagnostic(
    *,
    base_singular_value_lower_bound: float,
    base_derivative_lipschitz_bound: float,
    available_base_radius: float,
    available_calibration_half_width: float,
) -> FloatingCalibratedTargetBallDiagnostic:
    """Evaluate the exact radius formula in non-directed binary64."""

    beta = float(base_singular_value_lower_bound)
    lipschitz = float(base_derivative_lipschitz_bound)
    base_radius = float(available_base_radius)
    calibration_width = float(available_calibration_half_width)
    if not isfinite(beta) or beta <= 0.0:
        raise ValueError("base singular-value lower bound must be positive")
    if not isfinite(lipschitz) or lipschitz < 0.0:
        raise ValueError("base derivative Lipschitz bound must be nonnegative")
    if not isfinite(base_radius) or base_radius <= 0.0:
        raise ValueError("available base radius must be positive")
    if not isfinite(calibration_width) or calibration_width <= 0.0:
        raise ValueError("calibration half-width must be positive")

    if lipschitz == 0.0:
        floating_base_radius = base_radius / 2.0
    else:
        floating_base_radius = min(
            base_radius / 2.0,
            beta / (2.0 * lipschitz),
        )
    base_output = (
        beta * floating_base_radius
        - 0.5 * lipschitz * floating_base_radius**2
    )
    output = min(base_output, calibration_width / 2.0)
    return FloatingCalibratedTargetBallDiagnostic(
        base_singular_value_lower_bound=beta,
        base_derivative_lipschitz_bound=lipschitz,
        available_base_radius=base_radius,
        available_calibration_half_width=calibration_width,
        floating_base_radius=float(floating_base_radius),
        floating_base_output_radius=float(base_output),
        floating_output_ball_radius=float(output),
    )
