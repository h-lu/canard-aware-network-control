from __future__ import annotations

import mpmath as mp
import numpy as np
import pytest
import sympy as sp

from canard_control.fhn_control_no_go import (
    canonical_sharpness_diagnostic,
    declared_two_scale_no_go_bounds,
    leading_safety_direction,
    transverse_halanay_certificate,
    transverse_mode_multiplicities,
    two_module_delay_layer_audit,
)


@pytest.mark.parametrize("module_sizes", [(1, 1), (2, 3), (4, 2)])
def test_two_module_delay_layers_have_exact_size_independent_modes(
    module_sizes: tuple[int, int],
) -> None:
    result = two_module_delay_layer_audit(*module_sizes)
    zero_vectors = (
        result.collective_same_residual,
        result.collective_cross_residual,
        result.difference_same_residual,
        result.difference_cross_residual,
        result.within_same_residual,
        result.within_cross_residual,
    )
    assert all(item == sp.zeros(*item.shape) for item in zero_vectors)
    assert result.within_module_basis.rank() == sum(module_sizes) - 2
    assert transverse_mode_multiplicities(*module_sizes) == (
        1,
        1,
        sum(module_sizes) - 2,
    )


def test_halanay_certificate_closes_every_transverse_mode() -> None:
    result = transverse_halanay_certificate(
        epsilon=0.01,
        voltage_radius=2.5,
        voltage_scaffold=3.0,
        recovery_scaffold=1.5,
        linear_gain=0.8,
        cubic_gain=0.04,
        weight=2.0,
        maximal_scaled_delay=1.2,
    )
    assert result.certified
    assert result.local_decay > result.delayed_gain > 0.0
    assert result.maximal_physical_delay == pytest.approx(12.0)
    assert result.decay_rate < result.local_decay
    assert result.decay_rate == pytest.approx(
        result.local_decay
        - result.delayed_gain
        * np.exp(result.decay_rate * result.maximal_physical_delay),
        rel=2e-12,
        abs=2e-12,
    )


def test_halanay_certificate_rejects_an_insufficient_scaffold() -> None:
    result = transverse_halanay_certificate(
        epsilon=0.04,
        voltage_radius=3.0,
        voltage_scaffold=1.01,
        recovery_scaffold=0.6,
        linear_gain=1.0,
        cubic_gain=0.2,
        weight=2.0,
        maximal_scaled_delay=1.0,
    )
    assert not result.certified
    assert result.decay_rate == 0.0


def test_declared_safety_direction_keeps_cubic_actuator_out_at_leading_order() -> None:
    result = leading_safety_direction(linear_gain=0.8, first_delay_moment=1.5)
    assert np.allclose(result, np.array([1.5 / 8.0, 0.0, 0.8 / 8.0]))
    assert np.linalg.norm(result) >= 0.8 / 8.0


def test_two_scale_bounds_are_exponentially_small_after_natural_scaling() -> None:
    epsilon = 0.025
    width = float(mp.exp(-mp.mpf("0.45") / epsilon))
    result = declared_two_scale_no_go_bounds(
        epsilon=epsilon,
        width=width,
        linear_gain=0.8,
        first_delay_moment=1.5,
        safety_remainder_constant=0.2,
        profile_slope_lower_bound=0.4,
        shape_derivative_bound=2.0,
    )
    assert result.physical_combined_bound <= result.safety_row_bound
    assert result.physical_combined_bound <= result.physical_layer_bound
    assert result.physical_layer_bound < 6.0 * width
    assert result.natural_scaled_layer_bound < 6.0 * width / epsilon**1.5


def test_high_precision_family_asymptotically_attains_both_layer_bounds() -> None:
    diagnostic = canonical_sharpness_diagnostic(
        epsilon="0.02",
        width=mp.nstr(mp.exp(-mp.mpf("0.7") / mp.mpf("0.02")), 90),
        safety_direction_norm="0.23",
        decimal_digits=120,
    )
    assert abs(diagnostic.physical_ratio - 1) < mp.mpf("1e-20")
    assert abs(diagnostic.scaled_ratio - 1) < mp.mpf("1e-20")
    assert diagnostic.physical_smallest_singular_value < mp.mpf("1e-14")
    assert diagnostic.scaled_smallest_singular_value < mp.mpf("1e-11")


@pytest.mark.parametrize(
    "kwargs",
    [
        {"epsilon": 0.0},
        {"width": -1.0},
        {"profile_slope_lower_bound": 0.0},
        {"shape_derivative_bound": -1.0},
    ],
)
def test_two_scale_bounds_reject_invalid_hypotheses(kwargs: dict[str, float]) -> None:
    values = dict(
        epsilon=0.02,
        width=1e-8,
        linear_gain=0.8,
        first_delay_moment=1.5,
        safety_remainder_constant=0.2,
        profile_slope_lower_bound=0.4,
        shape_derivative_bound=2.0,
    )
    values.update(kwargs)
    with pytest.raises(ValueError):
        declared_two_scale_no_go_bounds(**values)
