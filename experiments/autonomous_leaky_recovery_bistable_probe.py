"""Binary64 probe for an autonomous leaky-recovery bistable RFDE slice.

The experiment has two deliberately separate roles.

* It evaluates an exact rational interval certificate for delay-independent
  linear stability of the unique synchronous equilibrium.
* It computes non-directed candidates for an attracting pulse cycle, an
  intermediate saddle cycle, a constant-history onset bracket, Floquet
  indices, and the frequency--amplitude response.

Only the equilibrium statement is analytic.  Fourier collocation,
method-of-steps integration, and finite monodromy matrices are diagnostics;
they have no directed truncation or rounding enclosure and must not be used
as proof flags.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
import math
from pathlib import Path
import platform

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from scipy.signal import resample

from canard_control import autonomous_leaky_recovery_bistable as certificate
from canard_control.autonomous_leaky_recovery_bistable import (
    DEFAULT_COMMAND,
    GENERATOR_RELATIVE_PATH,
    MANIFEST_ARITHMETIC,
    NOTE_RELATIVE_PATH,
    OUTPUT_CONTROL_COORDINATES,
    PROOF_SOURCE_RELATIVE_PATH,
    RESULT_RELATIVE_PATH,
    json_ready_autonomous_bistable_audit,
    validate_autonomous_bistable_result,
)
from canard_control.fhn_periodic_candidate import odd_fourier_matrices


REPOSITORY = Path(__file__).resolve().parents[1]
EPSILON = float(certificate.EPSILON)
UNFOLDING = float(certificate.UNFOLDING)
RECOVERY_LEAK = float(certificate.RECOVERY_LEAK)
KAPPA_1 = float(certificate.KAPPA_1)
KAPPA_3 = float(certificate.KAPPA_3)
TAU_0 = 4.0 * math.sqrt(5.0)
TAU_1 = 5.0 * math.sqrt(5.0)
COLLOCATION_NODES = 129
CONTINUATION_STEPS = 10
KICK_QUIET = 0.30
KICK_PULSE = 0.32
RECTANGULAR_PULSE_DURATION = 1.0
RECTANGULAR_PULSE_QUIET = 0.30
RECTANGULAR_PULSE_CAPTURE = 0.32
DEFAULT_RESULT = REPOSITORY / RESULT_RELATIVE_PATH


def _digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _manifest() -> dict[str, object]:
    return {
        "generator": GENERATOR_RELATIVE_PATH,
        "generator_sha256": _digest(REPOSITORY / GENERATOR_RELATIVE_PATH),
        "proof_source": PROOF_SOURCE_RELATIVE_PATH,
        "proof_source_sha256": _digest(
            REPOSITORY / PROOF_SOURCE_RELATIVE_PATH
        ),
        "note": NOTE_RELATIVE_PATH,
        "note_sha256": _digest(REPOSITORY / NOTE_RELATIVE_PATH),
        "default_command": DEFAULT_COMMAND,
        "arithmetic": MANIFEST_ARITHMETIC,
        "output_control_coordinates": list(OUTPUT_CONTROL_COORDINATES),
        "python": platform.python_version(),
        "platform": platform.platform(),
    }


def _ode_field(
    time: float,
    state: np.ndarray,
    *,
    unfolding: float,
    epsilon: float,
) -> np.ndarray:
    del time
    voltage, recovery = state
    return np.asarray(
        [
            voltage - voltage**3 / 3.0 - recovery,
            epsilon * (voltage - unfolding - recovery),
        ]
    )


def _positive_zero_event(time: float, state: np.ndarray) -> float:
    del time
    return float(state[0])


_positive_zero_event.direction = 1.0  # type: ignore[attr-defined]
_positive_zero_event.terminal = False  # type: ignore[attr-defined]


def _stable_ode_cycle(
    *, node_count: int, unfolding: float, epsilon: float
) -> tuple[np.ndarray, float]:
    integration = solve_ivp(
        lambda time, state: _ode_field(
            time, state, unfolding=unfolding, epsilon=epsilon
        ),
        (0.0, 700.0),
        np.asarray([2.0, 0.0]),
        events=_positive_zero_event,
        dense_output=True,
        method="DOP853",
        rtol=1.0e-11,
        atol=1.0e-13,
        max_step=0.04,
    )
    events = integration.t_events[0]
    if not integration.success or integration.sol is None or len(events) < 3:
        raise RuntimeError("failed to compute the attracting ODE cycle")
    start, finish = float(events[-2]), float(events[-1])
    period = finish - start
    phases = np.arange(node_count, dtype=float) / node_count
    state = integration.sol(start + period * phases).T
    return np.asarray(state), period


def _unstable_ode_cycle(
    *, node_count: int, unfolding: float, epsilon: float
) -> tuple[np.ndarray, float, float, float]:
    equilibrium_voltage = (3.0 * unfolding) ** (1.0 / 3.0)

    def return_data(initial_recovery: float):
        initial = np.asarray([equilibrium_voltage, initial_recovery])
        tangent = _ode_field(
            0.0, initial, unfolding=unfolding, epsilon=epsilon
        )
        initial = initial + 1.0e-8 * tangent

        def section(time: float, state: np.ndarray) -> float:
            del time
            return float(state[0] - equilibrium_voltage)

        section.direction = 1.0  # type: ignore[attr-defined]
        section.terminal = True  # type: ignore[attr-defined]
        integration = solve_ivp(
            lambda time, state: _ode_field(
                time, state, unfolding=unfolding, epsilon=epsilon
            ),
            (1.0e-8, 80.0),
            initial,
            events=section,
            dense_output=True,
            method="DOP853",
            rtol=1.0e-11,
            atol=1.0e-13,
            max_step=0.03,
        )
        if (
            not integration.success
            or integration.sol is None
            or not len(integration.t_events[0])
        ):
            raise RuntimeError("failed to return to the unstable-cycle section")
        returned = float(integration.y_events[0][0, 1])
        return returned - initial_recovery, integration

    recovery = brentq(
        lambda value: return_data(value)[0], 0.40, 0.45, xtol=1.0e-14
    )
    _, integration = return_data(recovery)
    period = float(integration.t_events[0][0])
    phases = np.arange(node_count, dtype=float) / node_count
    state = integration.sol(1.0e-8 + (period - 1.0e-8) * phases).T
    step = 1.0e-6

    def poincare(value: float) -> float:
        defect, _ = return_data(value)
        return value + defect

    derivative = (poincare(recovery + step) - poincare(recovery - step)) / (
        2.0 * step
    )
    return np.asarray(state), period, recovery, derivative


def _collocation_system(
    unknown: np.ndarray,
    *,
    unfolding: float,
    epsilon: float,
    gain_fraction: float,
    kappa_1_center: float,
    kappa_3_center: float,
    derivative: np.ndarray,
    phase_reference: np.ndarray,
    phase_tangent: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    count = derivative.shape[0]
    voltage = unknown[:count]
    recovery = unknown[count : 2 * count]
    period = float(unknown[-1])
    if period <= 0.0 or not np.isfinite(period):
        raise ArithmeticError("the period iterate left the positive axis")

    _, shift_0 = odd_fourier_matrices(count, TAU_0 / period)
    _, shift_1 = odd_fourier_matrices(count, TAU_1 / period)
    delayed_0 = shift_0 @ voltage
    delayed_1 = shift_1 @ voltage
    kappa_1 = gain_fraction * kappa_1_center
    kappa_3 = gain_fraction * kappa_3_center
    linear_difference = (delayed_0 + delayed_1) / 2.0 - voltage
    cubic_difference = (
        ((delayed_0 - 1.0) ** 3 + (delayed_1 - 1.0) ** 3) / 2.0
        - (voltage - 1.0) ** 3
    )
    fast = (
        voltage
        - voltage**3 / 3.0
        - recovery
        + epsilon * kappa_1 * linear_difference
        + epsilon * kappa_3 * cubic_difference
    )
    slow = epsilon * (voltage - unfolding - recovery)
    phase = float(
        np.vdot(
            phase_tangent,
            np.column_stack((voltage, recovery)) - phase_reference,
        ).real
        / count
    )
    residual = np.concatenate(
        (derivative @ voltage - period * fast,
         derivative @ recovery - period * slow,
         [phase])
    )

    current = (
        1.0
        - voltage**2
        - epsilon * kappa_1
        - 3.0 * epsilon * kappa_3 * (voltage - 1.0) ** 2
    )
    delayed_coefficient_0 = epsilon / 2.0 * (
        kappa_1 + 3.0 * kappa_3 * (delayed_0 - 1.0) ** 2
    )
    delayed_coefficient_1 = epsilon / 2.0 * (
        kappa_1 + 3.0 * kappa_3 * (delayed_1 - 1.0) ** 2
    )
    identity = np.eye(count)
    jacobian = np.zeros((2 * count + 1, 2 * count + 1))
    jacobian[:count, :count] = derivative - period * (
        np.diag(current)
        + np.diag(delayed_coefficient_0) @ shift_0
        + np.diag(delayed_coefficient_1) @ shift_1
    )
    jacobian[:count, count : 2 * count] = period * identity
    jacobian[count : 2 * count, :count] = -period * epsilon * identity
    jacobian[count : 2 * count, count : 2 * count] = (
        derivative + period * epsilon * identity
    )

    delayed_tangent_0 = shift_0 @ (derivative @ voltage)
    delayed_tangent_1 = shift_1 @ (derivative @ voltage)
    jacobian[:count, -1] = (
        -fast
        - TAU_0 / period * delayed_coefficient_0 * delayed_tangent_0
        - TAU_1 / period * delayed_coefficient_1 * delayed_tangent_1
    )
    jacobian[count : 2 * count, -1] = -slow
    jacobian[-1, :count] = phase_tangent[:, 0] / count
    jacobian[-1, count : 2 * count] = phase_tangent[:, 1] / count
    return residual, jacobian


def _newton_cycle(
    initial: np.ndarray,
    *,
    unfolding: float,
    epsilon: float,
    gain_fraction: float,
    kappa_1_center: float = KAPPA_1,
    kappa_3_center: float = KAPPA_3,
    derivative: np.ndarray,
    phase_reference: np.ndarray,
    phase_tangent: np.ndarray,
) -> tuple[np.ndarray, float, float]:
    unknown = np.asarray(initial, dtype=float).copy()
    for _ in range(14):
        residual, jacobian = _collocation_system(
            unknown,
            unfolding=unfolding,
            epsilon=epsilon,
            gain_fraction=gain_fraction,
            kappa_1_center=kappa_1_center,
            kappa_3_center=kappa_3_center,
            derivative=derivative,
            phase_reference=phase_reference,
            phase_tangent=phase_tangent,
        )
        step = np.linalg.solve(jacobian, -residual)
        unknown += step
        if np.max(np.abs(step)) < 2.0e-13:
            break
    residual, jacobian = _collocation_system(
        unknown,
        unfolding=unfolding,
        epsilon=epsilon,
        gain_fraction=gain_fraction,
        kappa_1_center=kappa_1_center,
        kappa_3_center=kappa_3_center,
        derivative=derivative,
        phase_reference=phase_reference,
        phase_tangent=phase_tangent,
    )
    return (
        unknown,
        float(np.max(np.abs(residual))),
        float(np.linalg.svd(jacobian, compute_uv=False)[-1]),
    )


def _continue_cycle(
    state: np.ndarray,
    period: float,
    *,
    unfolding: float,
    epsilon: float,
    derivative: np.ndarray,
) -> tuple[np.ndarray, float, float]:
    unknown = np.concatenate((state[:, 0], state[:, 1], [period]))
    residual = math.inf
    smallest_singular = 0.0
    for gain_fraction in np.linspace(0.0, 1.0, CONTINUATION_STEPS + 1):
        reference = np.column_stack(
            (unknown[: len(state)], unknown[len(state) : 2 * len(state)])
        )
        tangent = np.column_stack(
            (derivative @ reference[:, 0], derivative @ reference[:, 1])
        )
        unknown, residual, smallest_singular = _newton_cycle(
            unknown,
            unfolding=unfolding,
            epsilon=epsilon,
            gain_fraction=float(gain_fraction),
            derivative=derivative,
            phase_reference=reference,
            phase_tangent=tangent,
        )
    return unknown, residual, smallest_singular


def _trigonometric_values(
    samples: np.ndarray, phases: np.ndarray, *, derivative_order: int = 0
) -> np.ndarray:
    count = len(samples)
    coefficients = np.fft.fft(samples) / count
    modes = np.fft.fftfreq(count, d=1.0 / count)
    multiplier = (2.0j * np.pi * modes) ** derivative_order
    basis = np.exp(2.0j * np.pi * phases[:, None] * modes[None, :])
    return (basis @ (multiplier * coefficients)).real


def _cycle_diagnostics(
    unknown: np.ndarray,
    *,
    unfolding: float,
    epsilon: float,
    node_residual: float,
    smallest_singular: float,
) -> dict[str, object]:
    count = (len(unknown) - 1) // 2
    voltage = unknown[:count]
    recovery = unknown[count : 2 * count]
    period = float(unknown[-1])
    phases = np.arange(8 * count, dtype=float) / (8 * count)
    voltage_dense = _trigonometric_values(voltage, phases)
    recovery_dense = _trigonometric_values(recovery, phases)
    voltage_derivative = _trigonometric_values(
        voltage, phases, derivative_order=1
    )
    recovery_derivative = _trigonometric_values(
        recovery, phases, derivative_order=1
    )
    delayed_0 = _trigonometric_values(
        voltage, (phases - TAU_0 / period) % 1.0
    )
    delayed_1 = _trigonometric_values(
        voltage, (phases - TAU_1 / period) % 1.0
    )
    fast = (
        voltage_dense
        - voltage_dense**3 / 3.0
        - recovery_dense
        + epsilon * KAPPA_1
        * ((delayed_0 + delayed_1) / 2.0 - voltage_dense)
        + epsilon * KAPPA_3
        * (
            ((delayed_0 - 1.0) ** 3 + (delayed_1 - 1.0) ** 3) / 2.0
            - (voltage_dense - 1.0) ** 3
        )
    )
    slow = epsilon * (voltage_dense - unfolding - recovery_dense)
    oversampled_residual = max(
        float(np.max(np.abs(voltage_derivative - period * fast))),
        float(np.max(np.abs(recovery_derivative - period * slow))),
    )
    return {
        "period": format(period, ".17g"),
        "frequency": format(1.0 / period, ".17g"),
        "voltage_minimum": format(float(np.min(voltage_dense)), ".17g"),
        "voltage_maximum": format(float(np.max(voltage_dense)), ".17g"),
        "voltage_amplitude": format(float(np.ptp(voltage_dense)), ".17g"),
        "collocation_residual_inf": format(node_residual, ".17g"),
        "oversampled_residual_inf": format(oversampled_residual, ".17g"),
        "bordered_smallest_singular_value": format(
            smallest_singular, ".17g"
        ),
    }


def _periodic_interpolator(samples: np.ndarray, period: float):
    count = len(samples)
    coefficients = np.fft.fft(samples) / count
    modes = np.fft.fftfreq(count, d=1.0 / count)

    def evaluate(time: float) -> float:
        phase = (time / period) % 1.0
        return float(
            np.sum(coefficients * np.exp(2.0j * np.pi * modes * phase)).real
        )

    return evaluate


def _monodromy_row(unknown: np.ndarray, step_count: int) -> dict[str, object]:
    count = (len(unknown) - 1) // 2
    voltage_samples = unknown[:count]
    period = float(unknown[-1])
    voltage = _periodic_interpolator(voltage_samples, period)
    step = period / step_count
    history_steps = math.ceil(TAU_1 / step) + 3
    dimension = history_steps + 2
    voltage_maps: list[np.ndarray | None] = [None] * (
        history_steps + step_count + 1
    )
    for index in range(-history_steps, 1):
        basis = np.zeros(dimension)
        basis[index + history_steps] = 1.0
        voltage_maps[index + history_steps] = basis
    recovery_map = np.zeros(dimension)
    recovery_map[history_steps + 1] = 1.0

    def stored(index: int) -> np.ndarray:
        value = voltage_maps[index + history_steps]
        if value is None:
            raise ArithmeticError("the monodromy interpolant requested future data")
        return value

    def delayed_map(index: float) -> np.ndarray:
        left = math.floor(index)
        fraction = index - left
        weights = (
            -fraction * (fraction - 1.0) * (fraction - 2.0) / 6.0,
            (fraction + 1.0) * (fraction - 1.0) * (fraction - 2.0) / 2.0,
            -(fraction + 1.0) * fraction * (fraction - 2.0) / 2.0,
            (fraction + 1.0) * fraction * (fraction - 1.0) / 6.0,
        )
        return sum(
            weight * stored(node)
            for weight, node in zip(
                weights, (left - 1, left, left + 1, left + 2)
            )
        )

    def right_hand_side(
        time: float,
        current_voltage: np.ndarray,
        current_recovery: np.ndarray,
        grid_index: int,
        stage: float,
    ) -> tuple[np.ndarray, np.ndarray]:
        orbit_voltage = voltage(time)
        current = (
            1.0
            - orbit_voltage**2
            - EPSILON
            * (KAPPA_1 + 3.0 * KAPPA_3 * (orbit_voltage - 1.0) ** 2)
        )
        delayed = np.zeros(dimension)
        for delay in (TAU_0, TAU_1):
            delayed += (
                KAPPA_1 + 3.0 * KAPPA_3 * (voltage(time - delay) - 1.0) ** 2
            ) * delayed_map(grid_index + stage - delay / step)
        fast = (
            current * current_voltage
            - current_recovery
            + 0.5 * EPSILON * delayed
        )
        slow = EPSILON * current_voltage - EPSILON * current_recovery
        return fast, slow

    for grid_index in range(step_count):
        current_voltage = stored(grid_index)
        k1_v, k1_w = right_hand_side(
            grid_index * step,
            current_voltage,
            recovery_map,
            grid_index,
            0.0,
        )
        k2_v, k2_w = right_hand_side(
            (grid_index + 0.5) * step,
            current_voltage + 0.5 * step * k1_v,
            recovery_map + 0.5 * step * k1_w,
            grid_index,
            0.5,
        )
        k3_v, k3_w = right_hand_side(
            (grid_index + 0.5) * step,
            current_voltage + 0.5 * step * k2_v,
            recovery_map + 0.5 * step * k2_w,
            grid_index,
            0.5,
        )
        k4_v, k4_w = right_hand_side(
            (grid_index + 1.0) * step,
            current_voltage + step * k3_v,
            recovery_map + step * k3_w,
            grid_index,
            1.0,
        )
        voltage_maps[grid_index + 1 + history_steps] = (
            current_voltage
            + step * (k1_v + 2.0 * k2_v + 2.0 * k3_v + k4_v) / 6.0
        )
        recovery_map = recovery_map + step * (
            k1_w + 2.0 * k2_w + 2.0 * k3_w + k4_w
        ) / 6.0

    monodromy = np.vstack(
        [
            stored(index)
            for index in range(step_count - history_steps, step_count + 1)
        ]
        + [recovery_map]
    )
    eigenvalues = np.linalg.eigvals(monodromy)
    neutral_index = int(np.argmin(np.abs(eigenvalues - 1.0)))
    neutral = complex(eigenvalues[neutral_index])
    nontrivial = np.delete(eigenvalues, neutral_index)
    order = np.argsort(-np.abs(nontrivial))
    leading = [complex(nontrivial[index]) for index in order[:4]]
    return {
        "step_count": step_count,
        "history_steps": history_steps,
        "matrix_dimension": dimension,
        "neutral_multiplier": [
            format(neutral.real, ".17g"),
            format(neutral.imag, ".17g"),
        ],
        "neutral_error_from_one": format(abs(neutral - 1.0), ".17g"),
        "observed_nontrivial_outside_unit_disk_count": int(
            np.count_nonzero(np.abs(nontrivial) > 1.0)
        ),
        "leading_nontrivial_multipliers": [
            {
                "real": format(value.real, ".17g"),
                "imag": format(value.imag, ".17g"),
                "modulus": format(abs(value), ".17g"),
            }
            for value in leading
        ],
    }


def _simulate_protocol(
    *,
    initial_voltage_kick: float,
    pulse_amplitude: float,
    pulse_duration: float,
    final_time: float = 800.0,
) -> dict[str, object]:
    equilibrium_voltage = (3.0 * UNFOLDING) ** (1.0 / 3.0)
    equilibrium_recovery = equilibrium_voltage - equilibrium_voltage**3 / 3.0
    history = np.asarray(
        [equilibrium_voltage + initial_voltage_kick, equilibrium_recovery],
        dtype=float,
    )
    base_step = math.sqrt(5.0)
    segments = []

    def past(time: float) -> np.ndarray:
        if time <= 0.0:
            return history
        index = min(
            int(math.floor(time / base_step + 1.0e-12)), len(segments) - 1
        )
        return segments[index].sol(time)

    state = history.copy()
    start = 0.0
    while start < final_time - 1.0e-12:
        finish = min(start + base_step, final_time)

        def field(time: float, current: np.ndarray) -> np.ndarray:
            voltage, recovery = current
            delayed_0 = past(time - TAU_0)[0]
            delayed_1 = past(time - TAU_1)[0]
            applied_current = (
                pulse_amplitude if 0.0 <= time <= pulse_duration else 0.0
            )
            fast = (
                voltage
                - voltage**3 / 3.0
                - recovery
                + EPSILON
                * KAPPA_1
                * ((delayed_0 + delayed_1) / 2.0 - voltage)
                + EPSILON
                * KAPPA_3
                * (
                    ((delayed_0 - 1.0) ** 3 + (delayed_1 - 1.0) ** 3)
                    / 2.0
                    - (voltage - 1.0) ** 3
                )
                + applied_current
            )
            slow = EPSILON * (voltage - UNFOLDING - recovery)
            return np.asarray([fast, slow])

        solution = solve_ivp(
            field,
            (start, finish),
            state,
            dense_output=True,
            method="DOP853",
            rtol=1.0e-8,
            atol=1.0e-10,
            max_step=0.15,
        )
        if not solution.success or solution.sol is None:
            raise RuntimeError("the RFDE method-of-steps integration failed")
        segments.append(solution)
        state = solution.y[:, -1]
        start = finish

    sample_times = np.linspace(final_time - 150.0, final_time, 3001)
    voltage = np.asarray(
        [
            segments[
                min(
                    int(math.floor(time / base_step + 1.0e-12)),
                    len(segments) - 1,
                )
            ].sol(float(time))[0]
            for time in sample_times
        ]
    )
    amplitude = float(np.ptp(voltage))
    classification = (
        "quiet_candidate"
        if amplitude < 0.01
        else "pulse_candidate" if amplitude > 2.5 else "unresolved"
    )
    return {
        "initial_voltage_kick": format(initial_voltage_kick, ".17g"),
        "pulse_amplitude": format(pulse_amplitude, ".17g"),
        "pulse_duration": format(pulse_duration, ".17g"),
        "final_time": format(final_time, ".17g"),
        "tail_voltage_minimum": format(float(np.min(voltage)), ".17g"),
        "tail_voltage_maximum": format(float(np.max(voltage)), ".17g"),
        "tail_voltage_amplitude": format(amplitude, ".17g"),
        "classification": classification,
    }


def _simulate_constant_kick(
    kick: float, *, final_time: float = 800.0
) -> dict[str, object]:
    return _simulate_protocol(
        initial_voltage_kick=kick,
        pulse_amplitude=0.0,
        pulse_duration=0.0,
        final_time=final_time,
    )


def _simulate_rectangular_pulse(
    amplitude: float,
    *,
    duration: float = RECTANGULAR_PULSE_DURATION,
    final_time: float = 800.0,
) -> dict[str, object]:
    return _simulate_protocol(
        initial_voltage_kick=0.0,
        pulse_amplitude=amplitude,
        pulse_duration=duration,
        final_time=final_time,
    )


def _response_candidate(
    center: np.ndarray, derivative: np.ndarray
) -> dict[str, object]:
    count = derivative.shape[0]
    reference = np.column_stack(
        (center[:count], center[count : 2 * count])
    )
    tangent = np.column_stack(
        (derivative @ reference[:, 0], derivative @ reference[:, 1])
    )

    def output(unfolding: float, kappa_3: float) -> np.ndarray:
        solution, residual, _ = _newton_cycle(
            center,
            unfolding=unfolding,
            epsilon=EPSILON,
            gain_fraction=1.0,
            kappa_3_center=kappa_3,
            derivative=derivative,
            phase_reference=reference,
            phase_tangent=tangent,
        )
        if residual > 1.0e-9:
            raise ArithmeticError("a response collocation solve did not converge")
        dense = resample(solution[:count], 200 * count)
        return np.asarray([1.0 / solution[-1], float(np.ptp(dense))])

    step = 5.0e-5
    kappa_step = 5.0e-5
    a_plus = output(UNFOLDING + step, KAPPA_3)
    a_minus = output(UNFOLDING - step, KAPPA_3)
    kappa_plus = output(UNFOLDING, KAPPA_3 + kappa_step)
    kappa_minus = output(UNFOLDING, KAPPA_3 - kappa_step)
    jacobian = np.column_stack(
        ((a_plus - a_minus) / (2.0 * step),
         (kappa_plus - kappa_minus) / (2.0 * kappa_step))
    )
    singular_values = np.linalg.svd(jacobian, compute_uv=False)
    return {
        "controls": ["unfolding_a", "kappa_3"],
        "outputs": ["frequency", "voltage_amplitude"],
        "centered_difference_step": format(step, ".17g"),
        "kappa_3_centered_difference_step": format(kappa_step, ".17g"),
        "jacobian": [
            [format(float(value), ".17g") for value in row]
            for row in jacobian
        ],
        "determinant": format(float(np.linalg.det(jacobian)), ".17g"),
        "singular_values": [
            format(float(value), ".17g") for value in singular_values
        ],
    }


def build_probe() -> dict[str, object]:
    audit = json_ready_autonomous_bistable_audit()
    analytic = audit["equilibrium_certificate"]
    derivative, _ = odd_fourier_matrices(COLLOCATION_NODES)
    stable_state, stable_period = _stable_ode_cycle(
        node_count=COLLOCATION_NODES,
        unfolding=UNFOLDING,
        epsilon=EPSILON,
    )
    unstable_state, unstable_period, section_recovery, poincare_derivative = (
        _unstable_ode_cycle(
            node_count=COLLOCATION_NODES,
            unfolding=UNFOLDING,
            epsilon=EPSILON,
        )
    )
    stable, stable_residual, stable_singular = _continue_cycle(
        stable_state,
        stable_period,
        unfolding=UNFOLDING,
        epsilon=EPSILON,
        derivative=derivative,
    )
    unstable, unstable_residual, unstable_singular = _continue_cycle(
        unstable_state,
        unstable_period,
        unfolding=UNFOLDING,
        epsilon=EPSILON,
        derivative=derivative,
    )
    stable_diagnostic = _cycle_diagnostics(
        stable,
        unfolding=UNFOLDING,
        epsilon=EPSILON,
        node_residual=stable_residual,
        smallest_singular=stable_singular,
    )
    unstable_diagnostic = _cycle_diagnostics(
        unstable,
        unfolding=UNFOLDING,
        epsilon=EPSILON,
        node_residual=unstable_residual,
        smallest_singular=unstable_singular,
    )
    stable_diagnostic["monodromy_diagnostic"] = [
        _monodromy_row(stable, count) for count in (120, 180, 240)
    ]
    unstable_diagnostic["monodromy_diagnostic"] = [
        _monodromy_row(unstable, count) for count in (120, 180, 240)
    ]

    quiet = _simulate_constant_kick(KICK_QUIET)
    pulse = _simulate_constant_kick(KICK_PULSE)
    if quiet["classification"] != "quiet_candidate":
        raise ArithmeticError("the declared quiet endpoint did not return to rest")
    if pulse["classification"] != "pulse_candidate":
        raise ArithmeticError("the declared pulse endpoint did not reach the cycle")
    physical_quiet = _simulate_rectangular_pulse(RECTANGULAR_PULSE_QUIET)
    physical_capture = _simulate_rectangular_pulse(RECTANGULAR_PULSE_CAPTURE)
    if physical_quiet["classification"] != "quiet_candidate":
        raise ArithmeticError("the subthreshold physical pulse did not return to rest")
    if physical_capture["classification"] != "pulse_candidate":
        raise ArithmeticError("the suprathreshold physical pulse missed the cycle")

    return {
        "model": {
            "equations": (
                "v'=v-v^3/3-w+epsilon*kappa_1*((v_tau0+v_tau1)/2-v)"
                "+epsilon*kappa_3*(((v_tau0-1)^3+(v_tau1-1)^3)/2"
                "-(v-1)^3); w'=epsilon*(v-a-w)"
            ),
            "epsilon": format(EPSILON, ".17g"),
            "unfolding_a": format(UNFOLDING, ".17g"),
            "recovery_leak_b": format(RECOVERY_LEAK, ".17g"),
            "kappa_1": format(KAPPA_1, ".17g"),
            "kappa_3": format(KAPPA_3, ".17g"),
            "tau_0": format(TAU_0, ".17g"),
            "tau_1": format(TAU_1, ".17g"),
        },
        "audit": audit,
        "proved_analytic_equilibrium_certificate": analytic,
        "ode_diagnostic": {
            "stable_cycle_period": format(stable_period, ".17g"),
            "unstable_cycle_period": format(unstable_period, ".17g"),
            "unstable_cycle_section_recovery": format(
                section_recovery, ".17g"
            ),
            "unstable_cycle_poincare_derivative": format(
                poincare_derivative, ".17g"
            ),
        },
        "rfde_periodic_candidates": {
            "outer_pulse": stable_diagnostic,
            "inner_saddle_candidate": unstable_diagnostic,
        },
        "constant_history_kick_diagnostic": {
            "history_family": (
                "Phi_I(theta)=(v_e+I,w_e), -tau_1<=theta<=0"
            ),
            "quiet_endpoint": quiet,
            "pulse_endpoint": pulse,
            "candidate_onset_bracket": [
                format(KICK_QUIET, ".17g"),
                format(KICK_PULSE, ".17g"),
            ],
            "unique_threshold_validated": False,
        },
        "finite_duration_physical_pulse_diagnostic": {
            "protocol": (
                "start at the equilibrium history, add u(t)=J to the voltage "
                "equation for 0<=t<=1, and set u(t)=0 for all t>1"
            ),
            "subthreshold_endpoint": physical_quiet,
            "suprathreshold_endpoint": physical_capture,
            "candidate_onset_amplitude_bracket": [
                format(RECTANGULAR_PULSE_QUIET, ".17g"),
                format(RECTANGULAR_PULSE_CAPTURE, ".17g"),
            ],
            "post_pulse_vector_field_autonomous": True,
            "unique_threshold_validated": False,
        },
        "frequency_amplitude_response_candidate": _response_candidate(
            stable, derivative
        ),
        "claim_status": audit["claim_ledger"],
        "manifest": _manifest(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_RESULT)
    parser.add_argument("--stdout", action="store_true")
    arguments = parser.parse_args()
    result = build_probe()
    validate_autonomous_bistable_result(result, REPOSITORY)
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(encoded, encoding="utf-8")
    if arguments.stdout:
        print(encoded, end="")
    else:
        print(arguments.output)


if __name__ == "__main__":
    main()
