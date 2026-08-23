from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path

import numpy as np
import pytest

from canard_control.fhn_periodic_candidate import (
    FHNPeriodicParameters,
    _collocation_system,
    odd_fourier_matrices,
    periodic_response_candidate,
    sampled_response_box_candidate,
    solve_fhn_periodic_orbit,
)


def test_odd_fourier_derivative_and_retarded_shift_are_spectral() -> None:
    node_count = 17
    phases = np.arange(node_count, dtype=float) / node_count
    values = 0.4 + np.sin(6.0 * np.pi * phases) - 0.3 * np.cos(
        10.0 * np.pi * phases
    )
    delay_fraction = 0.173
    derivative, shift = odd_fourier_matrices(node_count, delay_fraction)
    expected_derivative = 6.0 * np.pi * np.cos(6.0 * np.pi * phases) + (
        3.0 * np.pi
    ) * np.sin(10.0 * np.pi * phases)
    expected_shift = 0.4 + np.sin(
        6.0 * np.pi * (phases - delay_fraction)
    ) - 0.3 * np.cos(10.0 * np.pi * (phases - delay_fraction))
    assert np.allclose(derivative @ values, expected_derivative, atol=2.0e-13)
    assert np.allclose(shift @ values, expected_shift, atol=2.0e-13)


@pytest.mark.parametrize("node_count", [4, 8, 10])
def test_fourier_grid_refuses_even_node_counts(node_count: int) -> None:
    with pytest.raises(ValueError, match="odd"):
        odd_fourier_matrices(node_count)


def test_collocation_jacobian_includes_the_moving_delay_period_column() -> None:
    parameters = FHNPeriodicParameters()
    node_count = 9
    phases = np.arange(node_count, dtype=float) / node_count
    derivative, _ = odd_fourier_matrices(node_count)
    state = np.column_stack(
        (
            0.3 + 0.6 * np.sin(2.0 * np.pi * phases),
            -0.2 + 0.4 * np.cos(2.0 * np.pi * phases),
        )
    )
    reference_derivative = derivative @ state
    unknown = np.concatenate((state[:, 0], state[:, 1], [17.2]))
    _, jacobian, _ = _collocation_system(
        unknown,
        parameters,
        derivative,
        state,
        reference_derivative,
    )

    step = 2.0e-7
    finite_difference = np.empty_like(jacobian)
    for column in range(len(unknown)):
        direction = np.zeros_like(unknown)
        direction[column] = step
        plus = _collocation_system(
            unknown + direction,
            parameters,
            derivative,
            state,
            reference_derivative,
        )[0]
        minus = _collocation_system(
            unknown - direction,
            parameters,
            derivative,
            state,
            reference_derivative,
        )[0]
        finite_difference[:, column] = (plus - minus) / (2.0 * step)
    assert np.allclose(jacobian, finite_difference, rtol=2.0e-7, atol=2.0e-7)

    # Deleting the derivative of tau/T gives merely -f in the fast period
    # column.  It must disagree for this nonconstant delayed state.
    voltage = state[:, 0]
    recovery = state[:, 1]
    tau_0, tau_1 = parameters.physical_delays
    _, shift_0 = odd_fourier_matrices(node_count, tau_0 / unknown[-1])
    _, shift_1 = odd_fourier_matrices(node_count, tau_1 / unknown[-1])
    delayed_0 = shift_0 @ voltage
    delayed_1 = shift_1 @ voltage
    fast_without_period_motion = (
        voltage
        - voltage**3 / 3.0
        - recovery
        + parameters.epsilon
        * parameters.kappa_1
        * ((delayed_0 + delayed_1) / 2.0 - voltage)
        + parameters.epsilon
        * parameters.kappa_3
        * (
            ((delayed_0 - 1.0) ** 3 + (delayed_1 - 1.0) ** 3) / 2.0
            - (voltage - 1.0) ** 3
        )
    )
    assert np.linalg.norm(
        jacobian[:node_count, -1] + fast_without_period_motion,
        ord=np.inf,
    ) > 1.0e-3


def test_default_fhn_orbit_has_reproducible_response_and_simple_extrema() -> None:
    orbit = solve_fhn_periodic_orbit(node_count=65)
    response = periodic_response_candidate(orbit)
    assert orbit.collocation_residual_inf < 2.0e-11
    assert orbit.oversampled_residual_inf < 2.0e-3
    assert np.isclose(orbit.period, 16.5403877970, rtol=0.0, atol=3.0e-9)
    assert np.allclose(
        response.response_matrix,
        np.array(
            [
                [0.0366998280, 0.1363394609],
                [-3.6451999930, -6.1347857640],
            ]
        ),
        rtol=3.0e-7,
        atol=3.0e-7,
    )
    assert np.linalg.svd(response.response_matrix, compute_uv=False)[-1] > 0.038
    assert response.forward_adjoint_disagreement_inf < 2.0e-11
    assert response.extrema.unique_maximum_and_minimum_candidate
    assert response.extrema.maximum_curvature < -70.0
    assert response.extrema.minimum_curvature > 70.0
    assert response.bordered.smallest_singular_value > 0.3
    assert response.bordered.inverse_defect_inf < 2.0e-11


def test_sampled_gain_box_has_positive_floating_weyl_candidate_only() -> None:
    result, orbits = sampled_response_box_candidate(
        half_widths=(5.0e-5, 5.0e-5),
        node_count=65,
    )
    assert len(orbits) == 9
    assert result.sample_controls.shape == (9, 2)
    assert result.all_sampled_extrema_simple
    assert result.candidate_beta > 0.018
    assert result.sampled_smallest_singular_value > 0.038
    assert result.maximum_oversampled_residual_inf < 2.0e-3


def test_recorded_candidate_has_provenance_and_refuses_interval_claims() -> None:
    repository = Path(__file__).resolve().parents[1]
    record = json.loads(
        (
            repository
            / "experiments"
            / "results"
            / "fhn_periodic_box_candidate.json"
        ).read_text(encoding="utf-8")
    )
    assert record["provenance"]["arithmetic"].endswith(
        "without directed rounding"
    )
    assert record["claim_status"]["directed_interval_proof"] is False
    assert record["claim_status"]["validated_periodic_orbit"] is False
    assert record["claim_status"]["validated_response_box"] is False
    assert record["sampled_box"]["candidate_beta"] > 0.018
    convergence = record["spectral_convergence"]
    assert convergence[0]["node_count"] == 65
    assert convergence[-1]["node_count"] == 193
    assert convergence[0]["oversampled_residual_inf"] > 1.0e-3
    assert convergence[-1]["oversampled_residual_inf"] < 1.0e-11


@pytest.mark.parametrize(
    "replacement, message",
    [
        ({"epsilon": 0.0}, "epsilon"),
        ({"unfolding": 1.0}, "unfolding"),
        ({"theta_0": -0.1}, "delay"),
    ],
)
def test_parameter_domain_is_explicit(
    replacement: dict[str, float], message: str
) -> None:
    with pytest.raises(ValueError, match=message):
        replace(FHNPeriodicParameters(), **replacement)


def test_solver_refuses_a_zero_continuation_count_before_integration() -> None:
    with pytest.raises(ValueError, match="continuation_steps"):
        solve_fhn_periodic_orbit(node_count=9, continuation_steps=0)
