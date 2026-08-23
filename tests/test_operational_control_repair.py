from __future__ import annotations

from math import pi

import numpy as np
import pytest

from canard_control.operational_control_repair import (
    block_triangular_lower_bound,
    floating_interval_candidate_diagnostic,
    hopf_normal_form_certificate,
    operational_response_certificate,
    quantitative_inverse_radius,
    threshold_gradient_bound,
)


def test_reset_only_column_and_block_inverse_are_exact() -> None:
    base = np.array([[0.8, -0.2], [1.1, 0.6]])
    threshold_gradient = np.array([2.0, -0.75])
    result = operational_response_certificate(base, threshold_gradient)

    assert np.array_equal(result.response_matrix[:2, 2], np.zeros(2))
    assert result.response_matrix[2, 2] == -1.0
    assert np.array_equal(
        result.response_matrix[2, :2],
        threshold_gradient,
    )

    expected_inverse = np.block(
        [
            [np.linalg.inv(base), np.zeros((2, 1))],
            [
                threshold_gradient.reshape(1, 2) @ np.linalg.inv(base),
                -np.ones((1, 1)),
            ],
        ]
    )
    assert np.allclose(
        expected_inverse @ result.response_matrix,
        np.eye(3),
        rtol=1e-14,
        atol=1e-14,
    )


def test_analytic_full_singular_value_bound_holds_for_random_blocks() -> None:
    rng = np.random.default_rng(20260823)
    for _ in range(250):
        base = rng.normal(size=(2, 2)) + 1.5 * np.eye(2)
        if np.linalg.svd(base, compute_uv=False)[-1] < 0.05:
            continue
        gradient = rng.normal(size=2)
        result = operational_response_certificate(base, gradient)
        assert (
            result.full_smallest_singular_value_lower_bound
            <= result.full_smallest_singular_value + 2e-14
        )
        actual_inverse_norm_squared = np.linalg.norm(
            np.linalg.inv(result.response_matrix),
            ord=2,
        ) ** 2
        assert (
            actual_inverse_norm_squared
            <= result.inverse_norm_squared_bound + 2e-12
        )


def test_zero_threshold_slope_recovers_the_diagonal_block_bound() -> None:
    beta = 0.37
    inverse_squared, lower = block_triangular_lower_bound(beta, 0.0)
    assert np.isclose(inverse_squared, beta**-2)
    assert np.isclose(lower, beta)

    inverse_squared_large, lower_large = block_triangular_lower_bound(2.0, 0.0)
    assert np.isclose(inverse_squared_large, 1.0)
    assert np.isclose(lower_large, 1.0)


def test_block_bound_is_scaled_for_extreme_finite_inputs() -> None:
    smallest_subnormal = np.nextafter(0.0, 1.0)
    maximum = np.finfo(float).max
    cases = (
        (1e-308, 0.0),
        (1e308, 1e308),
        (1.0, 1e308),
        (1e308, 1e-308),
        (smallest_subnormal, maximum),
    )
    with np.errstate(over="raise", divide="raise", invalid="raise"):
        results = [block_triangular_lower_bound(*case) for case in cases]

    for inverse_squared, lower in results:
        assert inverse_squared > 0.0
        assert not np.isnan(inverse_squared)
        assert 0.0 <= lower <= 1.0
        assert not np.isnan(lower)
    assert np.isclose(results[0][1], 1e-308, rtol=1e-15, atol=0.0)
    assert np.isclose(
        results[1][1],
        1.0 / np.sqrt(2.0),
        rtol=1e-15,
        atol=0.0,
    )
    assert np.isclose(results[3][1], 1.0, rtol=1e-15, atol=0.0)
    assert results[4][0] == float("inf")
    assert results[4][1] == 0.0


def test_separator_ift_constants_feed_the_full_bound() -> None:
    gamma = threshold_gradient_bound(
        base_gap_gradient_norm_upper_bound=0.9,
        stimulus_gap_derivative_lower_bound=0.3,
    )
    assert np.isclose(gamma, 3.0)
    _, bound = block_triangular_lower_bound(0.4, gamma)
    assert 0.0 < bound < 0.4


def test_quantitative_inverse_radius_has_the_claimed_contraction_constants() -> None:
    result = quantitative_inverse_radius(
        smallest_singular_value_lower_bound=0.8,
        derivative_lipschitz_bound=0.4,
        available_domain_radius=10.0,
    )
    assert np.isclose(result.certified_input_radius, 1.0)
    assert np.isclose(result.contraction_factor_bound, 0.5)
    assert np.isclose(result.certified_output_radius, 0.6)

    affine = quantitative_inverse_radius(
        smallest_singular_value_lower_bound=0.8,
        derivative_lipschitz_bound=0.0,
        available_domain_radius=2.5,
    )
    assert affine.contraction_factor_bound == 0.0
    assert np.isclose(affine.certified_input_radius, 1.25)
    assert np.isclose(affine.certified_output_radius, 1.0)


def test_exact_hopf_normal_form_response_and_singular_value_formula() -> None:
    growth = np.array([1.2, -0.4])
    angular_frequency = np.array([0.3, 1.1])
    shear = 0.7
    result = hopf_normal_form_certificate(growth, angular_frequency, shear)

    expected = np.vstack(
        (
            (angular_frequency - shear * growth) / (2.0 * pi),
            4.0 * growth,
        )
    )
    assert np.allclose(result.response_matrix, expected)
    assert np.isclose(result.determinant, np.linalg.det(expected))
    assert np.isclose(
        abs(result.determinant),
        2.0 / pi * abs(np.linalg.det(np.vstack((growth, angular_frequency)))),
    )
    assert np.isclose(
        result.smallest_singular_value,
        np.linalg.svd(expected, compute_uv=False)[-1],
    )
    assert (
        result.determinant_over_frobenius_lower_bound
        <= result.smallest_singular_value + 1e-15
    )

    # Direct finite differences of F=(omega-c*lambda)/(2*pi), A=4*lambda.
    base_parameter = np.array([0.2, -0.1])

    def outputs(parameter: np.ndarray) -> np.ndarray:
        growth_rate = 0.8 + growth @ (parameter - base_parameter)
        frequency = 3.0 + angular_frequency @ (parameter - base_parameter)
        return np.array(
            [(frequency - shear * growth_rate) / (2.0 * pi), 4.0 * growth_rate]
        )

    step = 1e-6
    finite_difference = np.column_stack(
        [
            (
                outputs(base_parameter + step * np.eye(2)[column])
                - outputs(base_parameter - step * np.eye(2)[column])
            )
            / (2.0 * step)
            for column in range(2)
        ]
    )
    assert np.allclose(finite_difference, expected, rtol=2e-10, atol=2e-10)


def test_canonical_hopf_coordinates_are_nondegenerate_for_every_shear() -> None:
    for shear in (-100.0, -0.25, 0.0, 2.0, 100.0):
        result = hopf_normal_form_certificate(
            np.array([1.0, 0.0]),
            np.array([0.0, 1.0]),
            shear,
        )
        assert np.isclose(result.determinant, -2.0 / pi)
        assert result.smallest_singular_value > 0.0


def test_floating_interval_candidate_screens_sampled_responses() -> None:
    midpoint = np.array([[0.8, -0.1], [0.2, 1.1]])
    radius = np.full((2, 2), 0.01)
    result = floating_interval_candidate_diagnostic(midpoint, radius)
    assert result.candidate_margin_positive

    # This sample check is only a floating-point regression.  Neither it nor
    # the helper is a directed-rounding interval proof.
    rng = np.random.default_rng(81021)
    for _ in range(1000):
        perturbation = rng.uniform(-radius, radius)
        singular = np.linalg.svd(
            midpoint + perturbation,
            compute_uv=False,
        )[-1]
        assert singular + 2e-15 >= result.candidate_margin


def test_certificate_helpers_reject_unproved_or_invalid_bounds() -> None:
    with pytest.raises(ValueError, match="positive"):
        block_triangular_lower_bound(0.0, 1.0)
    with pytest.raises(ValueError, match="nonnegative"):
        threshold_gradient_bound(-1.0, 0.2)
    with pytest.raises(ValueError, match="positive"):
        threshold_gradient_bound(1.0, 0.0)
    with pytest.raises(ValueError, match="nonnegative"):
        floating_interval_candidate_diagnostic(np.eye(2), -np.ones((2, 2)))
    with pytest.raises(ValueError, match="nonsingular"):
        operational_response_certificate(np.zeros((2, 2)), np.ones(2))
