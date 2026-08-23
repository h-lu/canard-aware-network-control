"""Exact and numerical certificates for canard-control conditioning.

The functions implement the row-cancellation theorem.  They do not compute
RFDE frequency, amplitude, pulse thresholds, or their adjoints.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import sympy as sp


@dataclass(frozen=True)
class ConditioningAudit:
    """Numerical singular-value certificate for one response matrix."""

    matrix: np.ndarray
    cancellation: float
    residual_row: np.ndarray
    smallest_singular_value: float
    cancellation_bound: float


def row_surjectivity_modulus(matrix: np.ndarray) -> float:
    """Return ``inf_{|y|=1} |matrix.T @ y|`` for a wide response matrix.

    For an ``outputs x actuators`` matrix with at least as many actuators as
    outputs, this is the full-row-rank (surjectivity) modulus.  Calling it the
    smallest singular value without this definition can be ambiguous because
    the actuator-side operator has a nullspace when it is overactuated.
    """

    response = np.asarray(matrix, dtype=float)
    if (
        response.ndim != 2
        or response.shape[0] == 0
        or response.shape[0] > response.shape[1]
    ):
        raise ValueError("matrix must be nonempty with no more rows than columns")
    if not np.all(np.isfinite(response)):
        raise ValueError("matrix entries must be finite")
    singular_values = np.linalg.svd(response, compute_uv=False)
    return float(singular_values[-1])


def scaled_layer_conditioning_bound(
    width: float,
    profile_slope_lower_bound: float,
    residual_derivative_bound: float,
    amplitude_scale: float,
    safety_scale: float,
) -> float:
    """Return the row-cancellation bound after output scaling.

    The scaled outputs are ``A_hat=A/q_A`` and ``S_hat=S/kappa``.  If
    ``A' = c S' + r`` with ``c=profile_slope/width``, then the cancellation
    coefficient for the scaled rows is ``kappa*c/q_A``.  The returned value
    uses only ``|profile_slope| >= profile_slope_lower_bound`` and
    ``|r| <= residual_derivative_bound``.
    """

    values = np.asarray(
        (
            width,
            profile_slope_lower_bound,
            residual_derivative_bound,
            amplitude_scale,
            safety_scale,
        ),
        dtype=float,
    )
    if not np.all(np.isfinite(values)):
        raise ValueError("all scales and bounds must be finite")
    width_value, slope, residual, q_amplitude, kappa = values
    if width_value <= 0 or slope <= 0 or q_amplitude <= 0 or kappa <= 0:
        raise ValueError("width, slope bound, and output scales must be positive")
    if residual < 0:
        raise ValueError("residual derivative bound must be nonnegative")
    denominator = np.hypot(q_amplitude * width_value, slope * kappa)
    return float(residual * width_value / denominator)


def cancellation_audit(
    frequency_row: np.ndarray,
    amplitude_row: np.ndarray,
    safety_row: np.ndarray,
    cancellation: float,
) -> ConditioningAudit:
    """Evaluate the universal row-cancellation upper bound."""

    frequency = np.asarray(frequency_row, dtype=float).reshape(-1)
    amplitude = np.asarray(amplitude_row, dtype=float).reshape(-1)
    safety = np.asarray(safety_row, dtype=float).reshape(-1)
    if not (
        frequency.shape == amplitude.shape == safety.shape
        and frequency.size >= 3
    ):
        raise ValueError("all rows must have the same length at least three")
    matrix = np.vstack((frequency, amplitude, safety))
    cancellation_value = float(cancellation)
    if not np.isfinite(cancellation_value) or not np.all(np.isfinite(matrix)):
        raise ValueError("response rows and cancellation must be finite")
    residual = amplitude - cancellation_value * safety
    bound = np.linalg.norm(residual) / np.hypot(1.0, cancellation_value)
    return ConditioningAudit(
        matrix=matrix,
        cancellation=cancellation_value,
        residual_row=residual,
        smallest_singular_value=row_surjectivity_modulus(matrix),
        cancellation_bound=float(bound),
    )


def exact_determinant_shear_identity(
    frequency_row: sp.MatrixBase,
    amplitude_row: sp.MatrixBase,
    safety_row: sp.MatrixBase,
    cancellation: sp.Expr,
) -> sp.Expr:
    """Return the exact determinant difference before and after row shear."""

    frequency = sp.Matrix(frequency_row)
    amplitude = sp.Matrix(amplitude_row)
    safety = sp.Matrix(safety_row)
    if frequency.shape == (3, 1):
        frequency = frequency.T
    if amplitude.shape == (3, 1):
        amplitude = amplitude.T
    if safety.shape == (3, 1):
        safety = safety.T
    if not (
        frequency.shape == amplitude.shape == safety.shape == (1, 3)
    ):
        raise ValueError("exact determinant audit requires three length-3 rows")
    original = sp.Matrix.vstack(frequency, amplitude, safety).det()
    sheared = sp.Matrix.vstack(
        frequency,
        amplitude - sp.sympify(cancellation) * safety,
        safety,
    ).det()
    return sp.simplify(original - sheared)
