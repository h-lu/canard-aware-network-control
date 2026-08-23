from __future__ import annotations

import numpy as np
import sympy as sp

from canard_control.canard_conditioning import (
    cancellation_audit,
    exact_determinant_shear_identity,
    row_surjectivity_modulus,
    scaled_layer_conditioning_bound,
)


def test_exact_determinant_is_invariant_under_amplitude_safety_shear() -> None:
    f = sp.Matrix([[1, 2, -1]])
    a = sp.Matrix([[3, -2, 4]])
    s = sp.Matrix([[2, 1, 5]])
    c = sp.Symbol("c")
    assert exact_determinant_shear_identity(f, a, s, c) == 0


def test_cancellation_upper_bound_holds() -> None:
    safety = np.array([1.0, -0.5, 2.0, 0.25])
    frequency = np.array([0.3, 1.2, -0.4, 0.8])
    residual = np.array([0.2, -0.1, 0.4, -0.3])
    cancellation = 100.0
    amplitude = cancellation * safety + residual
    audit = cancellation_audit(
        frequency,
        amplitude,
        safety,
        cancellation,
    )
    assert audit.smallest_singular_value <= audit.cancellation_bound + 1e-13
    assert np.allclose(audit.residual_row, residual)


def test_conditioning_bound_scales_with_canard_width() -> None:
    safety = np.array([1.0, 0.0, 0.0])
    frequency = np.array([0.0, 1.0, 0.0])
    residual = np.array([0.0, 0.0, 1.0])
    bounds = []
    widths = (1e-1, 1e-2, 1e-3, 1e-4)
    for width in widths:
        cancellation = 1.0 / width
        amplitude = cancellation * safety + residual
        audit = cancellation_audit(
            frequency,
            amplitude,
            safety,
            cancellation,
        )
        bounds.append(audit.cancellation_bound)
        assert audit.smallest_singular_value <= audit.cancellation_bound + 1e-13
        assert audit.cancellation_bound <= width
    ratios = np.asarray(bounds[1:]) / np.asarray(bounds[:-1])
    assert np.allclose(ratios, 0.1, rtol=2e-2)


def test_zero_shape_row_is_rank_deficient() -> None:
    safety = np.array([1.0, 2.0, -1.0])
    frequency = np.array([0.0, 1.0, 1.0])
    cancellation = 7.0
    audit = cancellation_audit(
        frequency,
        cancellation * safety,
        safety,
        cancellation,
    )
    assert audit.cancellation_bound == 0.0
    assert audit.smallest_singular_value < 1e-14


def test_random_wide_response_matrices_satisfy_row_cancellation_bound() -> None:
    rng = np.random.default_rng(20260823)
    for actuator_count in (3, 4, 9):
        for _ in range(20):
            frequency = rng.normal(size=actuator_count)
            safety = rng.normal(size=actuator_count)
            residual = rng.normal(size=actuator_count)
            cancellation = float(rng.normal())
            audit = cancellation_audit(
                frequency,
                cancellation * safety + residual,
                safety,
                cancellation,
            )
            assert audit.smallest_singular_value <= audit.cancellation_bound + 1e-12


def test_large_finite_cancellation_uses_overflow_safe_normalization() -> None:
    cancellation = 1e155
    safety = np.array([1e-155, 0.0, 0.0])
    residual = np.array([0.0, 1.0, 0.0])
    audit = cancellation_audit(
        np.array([0.0, 0.0, 1.0]),
        cancellation * safety + residual,
        safety,
        cancellation,
    )

    assert np.isfinite(audit.cancellation_bound)
    assert audit.cancellation_bound > 0.0
    assert np.isclose(audit.cancellation_bound, 1e-155)
    assert audit.smallest_singular_value <= audit.cancellation_bound * (1 + 1e-12)


def test_scaled_safety_bound_contains_the_kappa_factor() -> None:
    width = 1e-3
    kappa = 1e-1
    amplitude_scale = 1.0
    safety = np.array([1.0, 0.0, 0.0])
    frequency = np.array([0.0, 1.0, 0.0])
    residual = np.array([0.0, 0.0, 1.0])
    amplitude = safety / width + residual
    scaled_matrix = np.vstack(
        (frequency, amplitude / amplitude_scale, safety / kappa)
    )
    modulus = row_surjectivity_modulus(scaled_matrix)
    corrected_bound = scaled_layer_conditioning_bound(
        width=width,
        profile_slope_lower_bound=1.0,
        residual_derivative_bound=1.0,
        amplitude_scale=amplitude_scale,
        safety_scale=kappa,
    )
    assert modulus <= corrected_bound + 1e-12
    # The obsolete unscaled bound would be false for this scaled response.
    assert modulus > 5.0 * width


def test_every_linear_right_inverse_obeys_surjectivity_lower_bound() -> None:
    rng = np.random.default_rng(314159)
    matrix = rng.normal(size=(3, 7))
    gram_inverse = np.linalg.inv(matrix @ matrix.T)
    moore_penrose_right_inverse = matrix.T @ gram_inverse
    modulus = row_surjectivity_modulus(matrix)
    assert np.allclose(matrix @ moore_penrose_right_inverse, np.eye(3))
    assert np.isclose(
        np.linalg.norm(moore_penrose_right_inverse, ord=2),
        1.0 / modulus,
    )

    null_projection = np.eye(7) - moore_penrose_right_inverse @ matrix
    perturbed_right_inverse = (
        moore_penrose_right_inverse + null_projection @ rng.normal(size=(7, 3))
    )
    assert np.allclose(matrix @ perturbed_right_inverse, np.eye(3))
    assert np.linalg.norm(perturbed_right_inverse, ord=2) >= 1.0 / modulus - 1e-12
