from __future__ import annotations

from dataclasses import replace
import json
from pathlib import Path

import numpy as np
import pytest

from canard_control.fhn_periodic_candidate import solve_fhn_periodic_orbit
from canard_control.fhn_periodic_infinite_validation import (
    _RealConjugateLayout,
    _build_base_sequences,
    _embed_normalized_real_coordinates,
    _finite_coefficient_matrix,
    _restrict_normalized_real_coordinates,
    validate_infinite_periodic_candidate,
)


def _convolve(
    left: dict[int, complex],
    right: dict[int, complex],
) -> dict[int, complex]:
    result: dict[int, complex] = {}
    for left_mode, left_value in left.items():
        for right_mode, right_value in right.items():
            mode = left_mode + right_mode
            result[mode] = result.get(mode, 0.0j) + left_value * right_value
    return result


def _combine(
    *terms: tuple[complex, dict[int, complex]],
) -> dict[int, complex]:
    result: dict[int, complex] = {}
    for factor, sequence in terms:
        for mode, value in sequence.items():
            result[mode] = result.get(mode, 0.0j) + factor * value
    return result


def _floating_coefficient_residual(
    voltage: dict[int, complex],
    recovery: dict[int, complex],
    period: float,
    orbit,
) -> tuple[dict[int, complex], dict[int, complex], float]:
    parameters = orbit.parameters
    one = {0: 1.0 + 0.0j}
    centered = _combine((1.0, voltage), (-1.0, one))
    voltage_cubed = _convolve(_convolve(voltage, voltage), voltage)
    centered_cubed = _convolve(_convolve(centered, centered), centered)
    delayed: list[dict[int, complex]] = []
    delayed_centered_cubed: list[dict[int, complex]] = []
    for delay in parameters.physical_delays:
        shifted = {
            mode: value * np.exp(-2j * np.pi * mode * delay / period)
            for mode, value in voltage.items()
        }
        shifted_centered = _combine((1.0, shifted), (-1.0, one))
        delayed.append(shifted)
        delayed_centered_cubed.append(
            _convolve(
                _convolve(shifted_centered, shifted_centered),
                shifted_centered,
            )
        )
    linear_difference = _combine(
        (0.5, delayed[0]),
        (0.5, delayed[1]),
        (-1.0, voltage),
    )
    cubic_difference = _combine(
        (0.5, delayed_centered_cubed[0]),
        (0.5, delayed_centered_cubed[1]),
        (-1.0, centered_cubed),
    )
    fast = _combine(
        (1.0, voltage),
        (-1.0 / 3.0, voltage_cubed),
        (-1.0, recovery),
        (parameters.epsilon * parameters.kappa_1, linear_difference),
        (parameters.epsilon * parameters.kappa_3, cubic_difference),
    )
    slow = _combine(
        (parameters.epsilon, voltage),
        (-parameters.epsilon * parameters.unfolding, one),
    )
    derivative_voltage = {
        mode: 2j * np.pi * mode * value
        for mode, value in voltage.items()
    }
    derivative_recovery = {
        mode: 2j * np.pi * mode * value
        for mode, value in recovery.items()
    }
    residual_voltage = _combine(
        (1.0, derivative_voltage), (-period, fast)
    )
    residual_recovery = _combine(
        (1.0, derivative_recovery), (-period, slow)
    )
    reference_voltage, reference_recovery = _candidate_coefficients(orbit)
    phase = 0.0j
    for reference, value in (
        (reference_voltage, voltage),
        (reference_recovery, recovery),
    ):
        for mode, coefficient in reference.items():
            tangent = 2j * np.pi * (-mode) * reference[-mode]
            phase += tangent * (value.get(mode, 0.0j) - coefficient)
    return residual_voltage, residual_recovery, float(phase.real)


def _candidate_coefficients(orbit) -> tuple[dict[int, complex], dict[int, complex]]:
    count = len(orbit.state)
    cutoff = (count - 1) // 2
    sequences: list[dict[int, complex]] = []
    for component in (0, 1):
        transform = np.fft.fft(orbit.state[:, component]) / count
        sequences.append(
            {mode: transform[mode % count] for mode in range(-cutoff, cutoff + 1)}
        )
    return sequences[0], sequences[1]


def test_weighted_real_coordinates_are_exactly_the_conjugate_wiener_norm() -> None:
    layout = _RealConjugateLayout(4)
    coordinates = np.linspace(-1.1, 0.9, layout.dimension)
    voltage, recovery, period = _embed_normalized_real_coordinates(
        layout, coordinates
    )
    recovered = _restrict_normalized_real_coordinates(
        layout, voltage, recovery, period
    )
    full_wiener_norm = abs(period)
    for sequence in (voltage, recovery):
        full_wiener_norm += sum(
            abs(value.real) + abs(value.imag)
            for value in sequence.values()
        )

    assert layout.dimension == 4 * layout.cutoff + 3
    assert np.array_equal(recovered, coordinates)
    assert np.isclose(full_wiener_norm, np.linalg.norm(coordinates, 1))


def test_reduced_jacobian_matches_a_real_conjugate_finite_difference() -> None:
    orbit = solve_fhn_periodic_orbit(node_count=33)
    cutoff = (len(orbit.state) - 1) // 2
    base = _build_base_sequences(orbit, precision=100)
    matrix, _, layout = _finite_coefficient_matrix(base, cutoff)
    direction = np.zeros(layout.dimension)
    direction[layout.state_index(0, 3, "real")] = 0.4
    direction[layout.state_index(0, 4, "imag")] = -0.3
    direction[layout.state_index(1, 2, "imag")] = 0.2
    direction[layout.period_index] = 0.1
    delta_voltage, delta_recovery, delta_period = (
        _embed_normalized_real_coordinates(layout, direction)
    )
    center_voltage, center_recovery = _candidate_coefficients(orbit)

    def evaluate(sign: float) -> np.ndarray:
        voltage = {
            mode: center_voltage[mode] + sign * 1.0e-6 * value
            for mode, value in delta_voltage.items()
        }
        recovery = {
            mode: center_recovery[mode] + sign * 1.0e-6 * value
            for mode, value in delta_recovery.items()
        }
        fast, slow, phase = _floating_coefficient_residual(
            voltage,
            recovery,
            orbit.period + sign * 1.0e-6 * delta_period,
            orbit,
        )
        return _restrict_normalized_real_coordinates(
            layout, fast, slow, phase
        )

    finite_difference = (evaluate(1.0) - evaluate(-1.0)) / 2.0e-6
    assert matrix.shape == (4 * cutoff + 3, 4 * cutoff + 3)
    assert np.linalg.norm(finite_difference - matrix @ direction, np.inf) < 2e-7


def test_coefficient_map_preserves_fourier_conjugacy_for_real_period() -> None:
    orbit = solve_fhn_periodic_orbit(node_count=33)
    layout = _RealConjugateLayout((len(orbit.state) - 1) // 2)
    coordinates = np.linspace(-0.02, 0.02, layout.dimension)
    voltage, recovery, period_offset = _embed_normalized_real_coordinates(
        layout, coordinates
    )
    fast, slow, phase = _floating_coefficient_residual(
        voltage,
        recovery,
        orbit.period + period_offset,
        orbit,
    )
    for sequence in (fast, slow):
        for mode in range(1, 3 * layout.cutoff + 1):
            assert np.isclose(
                sequence.get(-mode, 0.0j),
                sequence.get(mode, 0.0j).conjugate(),
                atol=2e-12,
            )
        assert abs(sequence.get(0, 0.0j).imag) < 2e-12
    assert np.isfinite(phase)


def test_cutoff_must_contain_the_full_cubic_residual() -> None:
    orbit = solve_fhn_periodic_orbit(node_count=33)
    with pytest.raises(ValueError, match="full cubic residual support"):
        validate_infinite_periodic_candidate(
            orbit, cutoff=47, precision=80
        )


def test_current_nonlinear_majorant_refuses_negative_gains() -> None:
    orbit = solve_fhn_periodic_orbit(node_count=33)
    orbit = replace(
        orbit,
        parameters=replace(orbit.parameters, kappa_3=-0.25),
    )
    with pytest.raises(ValueError, match="requires nonnegative gains"):
        validate_infinite_periodic_candidate(
            orbit, cutoff=48, precision=80
        )


def test_tracked_infinite_result_closes_only_the_center_orbit() -> None:
    path = (
        Path(__file__).resolve().parents[1]
        / "experiments/results/fhn_periodic_infinite_validation.json"
    )
    payload = json.loads(path.read_text(encoding="utf-8"))
    validation = payload["validation"]
    blocks = validation["blocks"]
    correction = validation["correction"]
    assert validation["finite"]["cutoff"] == 144
    assert validation["finite"]["ambient_complex_dimension"] == 579
    assert validation["finite"]["real_conjugate_dimension"] == 579
    assert not validation["finite"]["ambient_complexification_used"]
    assert validation["finite"]["residual_support_half_bandwidth"] == 144
    assert float(blocks["full_point_defect_upper"]) < 0.18
    assert blocks["full_point_inverse_gate"]
    assert correction["radii_polynomial_evaluated"]
    assert correction["radii_polynomial_negative"]
    assert float(correction["radii_margin_lower"]) > 5.0e-8
    assert validation["periodic_rfde_orbit_validated"]
    assert validation["bordered_rfde_inverse_validated"]

    # The center-orbit theorem does not close the parameter-box issue.
    assert not validation["unit_multiplier_simple_validated"]
    assert not validation["full_floquet_hyperbolicity_validated"]
    assert not validation["extrema_validated"]
    assert not validation["response_box_validated"]
    assert not validation["issue_15_closed"]
