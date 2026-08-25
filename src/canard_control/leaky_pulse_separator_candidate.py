"""Source-bound finite-section candidate for the physical pulse separator.

The one-unit physical voltage pulse starts from the quiet equilibrium.  This
module follows the released RFDE trajectory to a phase section of the inner
periodic branch, samples the solution-determining reduced state, projects the
resulting finite vector onto a left unstable eigenvector of a finite
monodromy matrix, and solves for the pulse amplitude that zeros this
coordinate at several successive returns.  The sampled vector consists of
voltage-history values plus the current recovery coordinate.  Only the
continuous reduced state determines the RFDE future; the finite vector
determines the declared interpolation-based discretization, and its
Euclidean norm is not the full two-component history norm.

Everything in this module after the exact terminal-history map is a binary64
diagnostic.  In particular, a finite monodromy eigenvector is not a validated
RFDE Floquet covector, a zero of its coordinate is not a stable-manifold
intersection, and convergence over three meshes is not a proof of onset.
"""

from __future__ import annotations

from bisect import bisect_left
from dataclasses import dataclass
from hashlib import sha256
import json
import math
from pathlib import Path
import platform
from typing import Any, Mapping, Sequence

import numpy as np
import scipy
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

from canard_control.autonomous_leaky_recovery_bistable import (
    EPSILON as EPSILON_EXACT,
    KAPPA_1 as KAPPA_1_EXACT,
    KAPPA_3 as KAPPA_3_EXACT,
    UNFOLDING as UNFOLDING_EXACT,
)
from canard_control.fhn_periodic_candidate import PeriodicOrbitCandidate
from canard_control.leaky_periodic_branch_artifact import orbit_from_artifact


SCHEMA_ID = "leaky-pulse-separator-finite-section-candidate-v2"
MODEL_ID = "autonomous-leaky-recovery-physical-pulse"
BRANCH = "inner_saddle_candidate"

SOURCE_RELATIVE_PATH = (
    "src/canard_control/leaky_pulse_separator_candidate.py"
)
GENERATOR_RELATIVE_PATH = "experiments/leaky_pulse_separator_candidate.py"
RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_pulse_separator_candidate.json"
)
NOTE_RELATIVE_PATH = "docs/leaky-pulse-separator-candidate.md"
MODEL_SOURCE_RELATIVE_PATH = (
    "src/canard_control/autonomous_leaky_recovery_bistable.py"
)
TERMINAL_HISTORY_SOURCE_RELATIVE_PATH = (
    "src/canard_control/leaky_pulse_terminal_history.py"
)
PARENT_ARTIFACT_SOURCE_RELATIVE_PATH = (
    "src/canard_control/leaky_periodic_branch_artifact.py"
)
PARENT_ARTIFACT_RESULT_RELATIVE_PATH = (
    "experiments/results/autonomous_leaky_recovery_inner_branch_artifact.json"
)
DEFAULT_COMMAND = (
    "OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONPATH=src "
    "/usr/bin/python3 experiments/leaky_pulse_separator_candidate.py"
)
ARITHMETIC_SCOPE = (
    "SciPy DOP853 method of steps, cubic four-point delay interpolation in "
    "an RK4 finite monodromy matrix, NumPy binary64 eigensolves, and SciPy "
    "Brent roots; no directed rounding, truncation enclosure, validated "
    "Floquet projection, stable manifold, separator, routing, or onset proof"
)

EPSILON = float(EPSILON_EXACT)
UNFOLDING = float(UNFOLDING_EXACT)
KAPPA_1 = float(KAPPA_1_EXACT)
KAPPA_3 = float(KAPPA_3_EXACT)
TAU_0 = 4.0 * math.sqrt(5.0)
TAU_1 = 5.0 * math.sqrt(5.0)
PULSE_DURATION = 1.0

STEP_COUNTS = (120, 180, 240)
CROSSING_DEPTHS = (1, 2, 3)
ROOT_BRACKET = (0.301, 0.3012)
ROOT_XTOL = 5.0e-15
ROOT_RTOL = 1.0e-14
DERIVATIVE_STEP = 2.0e-8
FINAL_TIME = 75.0
SECTION_SEARCH_START = 12.0
INTEGRATION_RTOL = 2.0e-10
INTEGRATION_ATOL = 2.0e-12
INTEGRATION_MAX_STEP = 0.04
INTEGRATION_REFINEMENT_SETTINGS = (
    (2.0e-10, 2.0e-12, 0.04),
    (2.0e-11, 2.0e-13, 0.02),
    (2.0e-12, 2.0e-14, 0.01),
)
INTEGRATION_REFINEMENT_STEP_COUNT = 180
INTEGRATION_REFINEMENT_DEPTH = 3

# Filled only after the generated candidate body has been independently
# inspected.  The manifest is excluded from this digest, avoiding a cycle.
EXPECTED_CANDIDATE_SHA256: str | None = (
    "f62d11f8b6e9423922691cb513ada9522630d03183102b7b5808681bb6b16596"
)

NUMERICAL_TRUE_FLAGS = (
    "finite_section_monodromy_matrices_computed",
    "real_leading_multiplier_outside_unit_disk_observed",
    "three_return_shooting_roots_computed",
    "cross_resolution_root_agreement_observed",
    "successive_return_root_convergence_observed",
    "nonzero_scaled_shooting_derivative_observed",
    "third_return_reduced_sample_approach_observed",
    "integration_refinement_agreement_observed",
    "shooting_bracket_sign_changes_observed",
    "translation_tangent_consistency_observed",
)

PROOF_FALSE_FLAGS = (
    "finite_section_multiplier_is_validated_rfde_multiplier",
    "finite_section_left_vector_is_validated_floquet_covector",
    "inner_orbit_unstable_multiplier_count_validated",
    "inner_orbit_local_stable_manifold_validated",
    "physical_pulse_stable_manifold_intersection_validated",
    "history_space_separator_and_routing_validated",
    "endpoint_basin_inclusions_validated",
    "unique_physical_pulse_onset_validated",
    "finite_section_spectral_convergence_validated",
    "finite_shooting_roots_enclosed_by_directed_arithmetic",
    "physical_pulse_transversality_validated",
)


def canonical_sha256(value: object) -> str:
    encoded = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    return sha256(encoded).hexdigest()


def binary64_record(value: float) -> dict[str, str]:
    number = float(value)
    if not math.isfinite(number):
        raise ValueError("candidate numbers must be finite")
    return {
        "binary64_hex": number.hex(),
        "decimal": format(number, ".17g"),
    }


def binary64_value(value: object, name: str) -> float:
    if not isinstance(value, Mapping) or set(value) != {
        "binary64_hex",
        "decimal",
    }:
        raise ValueError(f"{name} must be a complete binary64 record")
    hexadecimal = value.get("binary64_hex")
    decimal = value.get("decimal")
    if not isinstance(hexadecimal, str) or not isinstance(decimal, str):
        raise ValueError(f"{name} binary64 fields must be strings")
    try:
        number = float.fromhex(hexadecimal)
    except ValueError as error:
        raise ValueError(f"{name} has an invalid hexadecimal value") from error
    if (
        not math.isfinite(number)
        or number.hex() != hexadecimal
        or format(number, ".17g") != decimal
    ):
        raise ValueError(f"{name} is not a canonical finite binary64 record")
    return number


def _periodic_interpolator(samples: np.ndarray, period: float):
    count = len(samples)
    coefficients = np.fft.fft(np.asarray(samples, dtype=float)) / count
    modes = np.fft.fftfreq(count, d=1.0 / count)

    def evaluate(time: float) -> float:
        phase = (time / period) % 1.0
        return float(
            np.sum(
                coefficients
                * np.exp(2.0j * np.pi * modes * phase)
            ).real
        )

    def derivative(time: float) -> float:
        phase = (time / period) % 1.0
        return float(
            np.sum(
                coefficients
                * (2.0j * np.pi * modes / period)
                * np.exp(2.0j * np.pi * modes * phase)
            ).real
        )

    return evaluate, derivative


@dataclass(frozen=True)
class FiniteSection:
    step_count: int
    step: float
    history_steps: int
    matrix: np.ndarray
    left_vector: np.ndarray
    reference: np.ndarray
    section_voltage: float
    section_voltage_derivative: float
    leading_multiplier: complex
    nearest_unit_multiplier: complex
    observed_nontrivial_outside_count: int
    left_eigen_residual_l2: float
    translation_tangent_residual_l2: float
    translation_tangent_relative_residual_l2: float


def finite_section(orbit: PeriodicOrbitCandidate, step_count: int) -> FiniteSection:
    """Construct one non-directed finite monodromy section."""

    if type(step_count) is not int or step_count < 20:
        raise ValueError("step_count must be an integer at least 20")
    voltage, voltage_derivative = _periodic_interpolator(
        orbit.state[:, 0], orbit.period
    )
    recovery, recovery_derivative = _periodic_interpolator(
        orbit.state[:, 1], orbit.period
    )
    step = orbit.period / step_count
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
            raise ArithmeticError("finite monodromy requested future data")
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
                weights, (left - 1, left, left + 1, left + 2), strict=True
            )
        )

    def variational_field(
        time: float,
        current_voltage: np.ndarray,
        current_recovery: np.ndarray,
        grid_index: int,
        stage: float,
    ) -> tuple[np.ndarray, np.ndarray]:
        orbit_voltage = voltage(time)
        current_coefficient = (
            1.0
            - orbit_voltage**2
            - EPSILON
            * (KAPPA_1 + 3.0 * KAPPA_3 * (orbit_voltage - 1.0) ** 2)
        )
        delayed = np.zeros(dimension)
        for delay in (TAU_0, TAU_1):
            delayed += (
                KAPPA_1
                + 3.0 * KAPPA_3 * (voltage(time - delay) - 1.0) ** 2
            ) * delayed_map(grid_index + stage - delay / step)
        fast = (
            current_coefficient * current_voltage
            - current_recovery
            + 0.5 * EPSILON * delayed
        )
        slow = EPSILON * (current_voltage - current_recovery)
        return fast, slow

    for grid_index in range(step_count):
        current_voltage = stored(grid_index)
        time = grid_index * step
        k1_v, k1_w = variational_field(
            time, current_voltage, recovery_map, grid_index, 0.0
        )
        k2_v, k2_w = variational_field(
            time + 0.5 * step,
            current_voltage + 0.5 * step * k1_v,
            recovery_map + 0.5 * step * k1_w,
            grid_index,
            0.5,
        )
        k3_v, k3_w = variational_field(
            time + 0.5 * step,
            current_voltage + 0.5 * step * k2_v,
            recovery_map + 0.5 * step * k2_w,
            grid_index,
            0.5,
        )
        k4_v, k4_w = variational_field(
            time + step,
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

    matrix = np.vstack(
        [
            stored(index)
            for index in range(step_count - history_steps, step_count + 1)
        ]
        + [recovery_map]
    )
    eigenvalues = np.linalg.eigvals(matrix)
    neutral_index = int(np.argmin(np.abs(eigenvalues - 1.0)))
    nearest_unit = complex(eigenvalues[neutral_index])
    nontrivial = np.delete(eigenvalues, neutral_index)
    observed_outside = int(np.count_nonzero(np.abs(nontrivial) > 1.0))

    left_values, left_vectors = np.linalg.eig(matrix.T)
    leading_index = int(np.argmax(np.abs(left_values)))
    leading = complex(left_values[leading_index])
    raw_left = left_vectors[:, leading_index]
    pivot = int(np.argmax(np.abs(raw_left)))
    raw_left = raw_left * np.exp(-1.0j * np.angle(raw_left[pivot]))
    if abs(leading.imag) > 2.0e-8 or np.linalg.norm(raw_left.imag) > 2.0e-7:
        raise ArithmeticError("leading finite-section eigenpair is not real")
    left = np.asarray(raw_left.real, dtype=float)
    left /= np.linalg.norm(left)
    if left[-1] < 0.0:
        left = -left
    leading_real = complex(float(leading.real), 0.0)
    left_residual = float(
        np.linalg.norm(left @ matrix - leading_real.real * left)
    )
    reference = np.asarray(
        [
            voltage((index - history_steps) * step)
            for index in range(history_steps + 1)
        ]
        + [recovery(0.0)],
        dtype=float,
    )
    translation_tangent = np.asarray(
        [
            voltage_derivative((index - history_steps) * step)
            for index in range(history_steps + 1)
        ]
        + [recovery_derivative(0.0)],
        dtype=float,
    )
    translation_residual = float(
        np.linalg.norm(matrix @ translation_tangent - translation_tangent)
    )
    translation_tangent_norm = float(np.linalg.norm(translation_tangent))
    if translation_tangent_norm == 0.0:
        raise ArithmeticError("periodic translation tangent vanished")
    return FiniteSection(
        step_count=step_count,
        step=step,
        history_steps=history_steps,
        matrix=matrix,
        left_vector=left,
        reference=reference,
        section_voltage=voltage(0.0),
        section_voltage_derivative=voltage_derivative(0.0),
        leading_multiplier=leading_real,
        nearest_unit_multiplier=nearest_unit,
        observed_nontrivial_outside_count=observed_outside,
        left_eigen_residual_l2=left_residual,
        translation_tangent_residual_l2=translation_residual,
        translation_tangent_relative_residual_l2=(
            translation_residual / translation_tangent_norm
        ),
    )


@dataclass
class _Segment:
    start: float
    finish: float
    solution: Any


@dataclass
class PulseTrajectory:
    equilibrium: np.ndarray
    segments: list[_Segment]
    crossings: list[float]

    def state(self, time: float) -> np.ndarray:
        if time <= 0.0:
            return self.equilibrium.copy()
        finishes = [segment.finish for segment in self.segments]
        index = bisect_left(finishes, time - 2.0e-13)
        if index >= len(self.segments):
            if time <= self.segments[-1].finish + 2.0e-11:
                index = len(self.segments) - 1
            else:
                raise ValueError("trajectory evaluation is beyond final time")
        segment = self.segments[index]
        if time < segment.start - 2.0e-11:
            raise ArithmeticError("method-of-steps segment lookup failed")
        return np.asarray(segment.solution(time), dtype=float)


def _quiet_equilibrium() -> np.ndarray:
    alpha = (3.0 * UNFOLDING) ** (1.0 / 3.0)
    return np.asarray([alpha, alpha - UNFOLDING], dtype=float)


def method_of_steps_breakpoints(final_time: float) -> tuple[float, ...]:
    """Return causal and propagated-regularity breakpoints for the pulse.

    Both delays are integer multiples of ``sqrt(5)``.  The two grids based
    at zero and at pulse release therefore include every propagation of the
    possible regularity losses at pulse onset and release.  The deliberately
    finer grids also keep every segment shorter than the shortest delay, so
    all delayed evaluations lie in completed segments.
    """

    horizon = float(final_time)
    if not math.isfinite(horizon) or horizon <= 0.0:
        raise ValueError("final_time must be finite and positive")
    base_step = math.sqrt(5.0)
    breakpoints = {0.0, horizon}
    for origin in (0.0, PULSE_DURATION):
        if origin >= horizon:
            continue
        maximum_index = math.floor((horizon - origin) / base_step) + 1
        for index in range(maximum_index + 1):
            point = origin + index * base_step
            if 0.0 < point < horizon:
                breakpoints.add(point)
    return tuple(sorted(breakpoints))


def simulate_physical_pulse(
    amplitude: float,
    section_voltage: float,
    *,
    final_time: float = FINAL_TIME,
    integration_rtol: float = INTEGRATION_RTOL,
    integration_atol: float = INTEGRATION_ATOL,
    integration_max_step: float = INTEGRATION_MAX_STEP,
) -> PulseTrajectory:
    """Integrate the released RFDE by a non-directed method of steps."""

    if not math.isfinite(float(amplitude)):
        raise ValueError("pulse amplitude must be finite")
    if not math.isfinite(float(section_voltage)):
        raise ValueError("section voltage must be finite")
    tolerances = (
        float(integration_rtol),
        float(integration_atol),
        float(integration_max_step),
    )
    if any(not math.isfinite(value) or value <= 0.0 for value in tolerances):
        raise ValueError("integration tolerances and maximum step must be positive")
    equilibrium = _quiet_equilibrium()
    ordered = method_of_steps_breakpoints(final_time)
    segments: list[_Segment] = []
    crossings: list[float] = []

    def past(time: float) -> np.ndarray:
        if time <= 0.0:
            return equilibrium
        finishes = [segment.finish for segment in segments]
        index = bisect_left(finishes, time - 2.0e-13)
        if index >= len(segments):
            raise ArithmeticError("delay evaluation entered the current step")
        return np.asarray(segments[index].solution(time), dtype=float)

    state = equilibrium.copy()
    for start, finish in zip(ordered[:-1], ordered[1:], strict=True):
        forced_segment = start < PULSE_DURATION - 1.0e-14

        def field(time: float, current: np.ndarray) -> np.ndarray:
            voltage, recovery = current
            delayed_0 = past(time - TAU_0)[0]
            delayed_1 = past(time - TAU_1)[0]
            applied = amplitude if forced_segment else 0.0
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
                + applied
            )
            slow = EPSILON * (voltage - UNFOLDING - recovery)
            return np.asarray([fast, slow])

        def section_event(time: float, current: np.ndarray) -> float:
            del time
            return float(current[0] - section_voltage)

        section_event.direction = 1.0  # type: ignore[attr-defined]
        section_event.terminal = False  # type: ignore[attr-defined]
        integration = solve_ivp(
            field,
            (start, finish),
            state,
            events=section_event,
            dense_output=True,
            method="DOP853",
            rtol=integration_rtol,
            atol=integration_atol,
            max_step=integration_max_step,
        )
        if not integration.success or integration.sol is None:
            raise RuntimeError("physical-pulse method-of-steps solve failed")
        segment = _Segment(start, finish, integration.sol)
        segments.append(segment)
        state = np.asarray(integration.y[:, -1], dtype=float)
        for event_time in integration.t_events[0]:
            time = float(event_time)
            if time <= SECTION_SEARCH_START:
                continue
            if not crossings or abs(time - crossings[-1]) > 1.0e-7:
                crossings.append(time)
    return PulseTrajectory(equilibrium, segments, crossings)


def _history_vector(
    trajectory: PulseTrajectory,
    section: FiniteSection,
    time: float,
) -> np.ndarray:
    voltage_history = [
        trajectory.state(time + (index - section.history_steps) * section.step)[0]
        for index in range(section.history_steps + 1)
    ]
    recovery = trajectory.state(time)[1]
    return np.asarray(voltage_history + [recovery], dtype=float)


def shooting_data(
    section: FiniteSection,
    amplitude: float,
    depth: int,
    *,
    integration_rtol: float = INTEGRATION_RTOL,
    integration_atol: float = INTEGRATION_ATOL,
    integration_max_step: float = INTEGRATION_MAX_STEP,
) -> tuple[float, float, float]:
    """Return finite-section coordinate, crossing time, and reference distance."""

    if depth not in CROSSING_DEPTHS:
        raise ValueError("unsupported crossing depth")
    trajectory = simulate_physical_pulse(
        amplitude,
        section.section_voltage,
        integration_rtol=integration_rtol,
        integration_atol=integration_atol,
        integration_max_step=integration_max_step,
    )
    if len(trajectory.crossings) < depth:
        raise ArithmeticError("physical trajectory has too few positive returns")
    crossing = trajectory.crossings[depth - 1]
    vector = _history_vector(trajectory, section, crossing)
    difference = vector - section.reference
    return (
        float(section.left_vector @ difference),
        crossing,
        float(np.linalg.norm(difference)),
    )


def _complex_record(value: complex) -> dict[str, dict[str, str]]:
    return {
        "real": binary64_record(value.real),
        "imag": binary64_record(value.imag),
        "modulus": binary64_record(abs(value)),
    }


def _root_rows(
    section: FiniteSection,
    *,
    integration_rtol: float = INTEGRATION_RTOL,
    integration_atol: float = INTEGRATION_ATOL,
    integration_max_step: float = INTEGRATION_MAX_STEP,
) -> list[dict[str, object]]:
    cache: dict[float, tuple[list[float], list[float], list[float]]] = {}

    def all_depths(amplitude: float) -> tuple[list[float], list[float], list[float]]:
        key = float(amplitude)
        if key in cache:
            return cache[key]
        trajectory = simulate_physical_pulse(
            key,
            section.section_voltage,
            integration_rtol=integration_rtol,
            integration_atol=integration_atol,
            integration_max_step=integration_max_step,
        )
        if len(trajectory.crossings) < max(CROSSING_DEPTHS):
            raise ArithmeticError("shooting trajectory has too few returns")
        coordinates: list[float] = []
        times: list[float] = []
        distances: list[float] = []
        for depth in CROSSING_DEPTHS:
            crossing = trajectory.crossings[depth - 1]
            vector = _history_vector(trajectory, section, crossing)
            difference = vector - section.reference
            coordinates.append(float(section.left_vector @ difference))
            times.append(crossing)
            distances.append(float(np.linalg.norm(difference)))
        cache[key] = (coordinates, times, distances)
        return cache[key]

    rows: list[dict[str, object]] = []
    for depth in CROSSING_DEPTHS:
        offset = depth - 1

        def coordinate(amplitude: float) -> float:
            return all_depths(amplitude)[0][offset]

        root = float(
            brentq(
                coordinate,
                ROOT_BRACKET[0],
                ROOT_BRACKET[1],
                xtol=ROOT_XTOL,
                rtol=ROOT_RTOL,
            )
        )
        left_coordinate = coordinate(ROOT_BRACKET[0])
        right_coordinate = coordinate(ROOT_BRACKET[1])
        if left_coordinate * right_coordinate >= 0.0:
            raise ArithmeticError("shooting bracket lost its sign change")
        coordinates, times, distances = all_depths(root)
        derivative = (
            coordinate(root + DERIVATIVE_STEP)
            - coordinate(root - DERIVATIVE_STEP)
        ) / (2.0 * DERIVATIVE_STEP)
        scaled = derivative / abs(section.leading_multiplier) ** (depth - 1)
        rows.append(
            {
                "crossing_depth": depth,
                "pulse_amplitude": binary64_record(root),
                "finite_coordinate_at_root": binary64_record(
                    coordinates[offset]
                ),
                "bracket_left_coordinate": binary64_record(left_coordinate),
                "bracket_right_coordinate": binary64_record(right_coordinate),
                "crossing_time": binary64_record(times[offset]),
                "reference_distance_l2": binary64_record(distances[offset]),
                "centered_derivative_step": binary64_record(DERIVATIVE_STEP),
                "finite_coordinate_derivative": binary64_record(derivative),
                "multiplier_scaled_derivative": binary64_record(scaled),
            }
        )
    return rows


def _single_root_row(
    section: FiniteSection,
    depth: int,
    *,
    integration_rtol: float,
    integration_atol: float,
    integration_max_step: float,
) -> dict[str, object]:
    cache: dict[float, tuple[float, float, float]] = {}

    def data(amplitude: float) -> tuple[float, float, float]:
        key = float(amplitude)
        if key not in cache:
            cache[key] = shooting_data(
                section,
                key,
                depth,
                integration_rtol=integration_rtol,
                integration_atol=integration_atol,
                integration_max_step=integration_max_step,
            )
        return cache[key]

    root = float(
        brentq(
            lambda amplitude: data(amplitude)[0],
            ROOT_BRACKET[0],
            ROOT_BRACKET[1],
            xtol=ROOT_XTOL,
            rtol=ROOT_RTOL,
        )
    )
    left_coordinate = data(ROOT_BRACKET[0])[0]
    right_coordinate = data(ROOT_BRACKET[1])[0]
    if left_coordinate * right_coordinate >= 0.0:
        raise ArithmeticError("refinement bracket lost its sign change")
    coordinate, crossing_time, distance = data(root)
    return {
        "integration_rtol": binary64_record(integration_rtol),
        "integration_atol": binary64_record(integration_atol),
        "integration_max_step": binary64_record(integration_max_step),
        "pulse_amplitude": binary64_record(root),
        "finite_coordinate_at_root": binary64_record(coordinate),
        "bracket_left_coordinate": binary64_record(left_coordinate),
        "bracket_right_coordinate": binary64_record(right_coordinate),
        "crossing_time": binary64_record(crossing_time),
        "reference_distance_l2": binary64_record(distance),
    }


def build_candidate(parent_payload: Mapping[str, Any]) -> dict[str, object]:
    """Build the complete non-directed candidate body."""

    artifact = parent_payload.get("artifact")
    if not isinstance(artifact, Mapping):
        raise ValueError("parent inner artifact is missing")
    if artifact.get("branch") != BRANCH:
        raise ValueError("wrong parent periodic branch")
    orbit = orbit_from_artifact(artifact)
    resolutions: list[dict[str, object]] = []
    sections: dict[int, FiniteSection] = {}
    for step_count in STEP_COUNTS:
        section = finite_section(orbit, step_count)
        sections[step_count] = section
        if section.section_voltage_derivative <= 0.0:
            raise ArithmeticError("stored phase section is not positively crossed")
        rows = _root_rows(section)
        resolutions.append(
            {
                "step_count": step_count,
                "history_steps": section.history_steps,
                "matrix_dimension": section.matrix.shape[0],
                "step_size": binary64_record(section.step),
                "phase_section_voltage": binary64_record(section.section_voltage),
                "phase_section_voltage_derivative": binary64_record(
                    section.section_voltage_derivative
                ),
                "leading_multiplier": _complex_record(
                    section.leading_multiplier
                ),
                "nearest_unit_multiplier": _complex_record(
                    section.nearest_unit_multiplier
                ),
                "observed_nontrivial_outside_unit_disk_count": (
                    section.observed_nontrivial_outside_count
                ),
                "left_eigen_residual_l2": binary64_record(
                    section.left_eigen_residual_l2
                ),
                "translation_tangent_residual_l2": binary64_record(
                    section.translation_tangent_residual_l2
                ),
                "translation_tangent_relative_residual_l2": binary64_record(
                    section.translation_tangent_relative_residual_l2
                ),
                "left_covector_recovery_coordinate": binary64_record(
                    section.left_vector[-1]
                ),
                "shooting_roots": rows,
            }
        )

    refinement_section = sections[INTEGRATION_REFINEMENT_STEP_COUNT]
    integration_refinement = [
        _single_root_row(
            refinement_section,
            INTEGRATION_REFINEMENT_DEPTH,
            integration_rtol=rtol,
            integration_atol=atol,
            integration_max_step=max_step,
        )
        for rtol, atol, max_step in INTEGRATION_REFINEMENT_SETTINGS
    ]

    depth_three_roots = [
        binary64_value(row["shooting_roots"][2]["pulse_amplitude"], "root")
        for row in resolutions
    ]
    depth_two_three_gaps = [
        abs(
            binary64_value(row["shooting_roots"][2]["pulse_amplitude"], "root3")
            - binary64_value(row["shooting_roots"][1]["pulse_amplitude"], "root2")
        )
        for row in resolutions
    ]
    scaled_derivatives = [
        binary64_value(
            root["multiplier_scaled_derivative"], "scaled derivative"
        )
        for row in resolutions
        for root in row["shooting_roots"]
    ]
    depth_three_distances = [
        binary64_value(
            row["shooting_roots"][2]["reference_distance_l2"], "distance"
        )
        for row in resolutions
    ]
    convergence = {
        "third_return_root_cross_resolution_span": binary64_record(
            max(depth_three_roots) - min(depth_three_roots)
        ),
        "maximum_second_to_third_return_root_gap": binary64_record(
            max(depth_two_three_gaps)
        ),
        "minimum_absolute_scaled_derivative": binary64_record(
            min(abs(value) for value in scaled_derivatives)
        ),
        "maximum_third_return_reference_distance_l2": binary64_record(
            max(depth_three_distances)
        ),
        "integration_refinement_root_span": binary64_record(
            max(
                binary64_value(row["pulse_amplitude"], "refined root")
                for row in integration_refinement
            )
            - min(
                binary64_value(row["pulse_amplitude"], "refined root")
                for row in integration_refinement
            )
        ),
    }
    flags = {name: True for name in NUMERICAL_TRUE_FLAGS}
    flags.update({name: False for name in PROOF_FALSE_FLAGS})
    parent_claims = artifact.get("claim_status")
    parent_orbit_validated = bool(
        isinstance(parent_claims, Mapping)
        and parent_claims.get("periodic_rfde_orbit_validated") is True
    )
    return {
        "schema_id": SCHEMA_ID,
        "model_id": MODEL_ID,
        "parent_branch": BRANCH,
        "parent_periodic_orbit_existence_validated": parent_orbit_validated,
        "finite_section_uses_binary64_polynomial_center": True,
        "method": {
            "step_counts": list(STEP_COUNTS),
            "crossing_depths": list(CROSSING_DEPTHS),
            "root_bracket": [binary64_record(value) for value in ROOT_BRACKET],
            "root_xtol": binary64_record(ROOT_XTOL),
            "root_rtol": binary64_record(ROOT_RTOL),
            "derivative_step": binary64_record(DERIVATIVE_STEP),
            "final_time": binary64_record(FINAL_TIME),
            "section_search_start": binary64_record(SECTION_SEARCH_START),
            "integration_rtol": binary64_record(INTEGRATION_RTOL),
            "integration_atol": binary64_record(INTEGRATION_ATOL),
            "integration_max_step": binary64_record(INTEGRATION_MAX_STEP),
            "integration_refinement_step_count": INTEGRATION_REFINEMENT_STEP_COUNT,
            "integration_refinement_depth": INTEGRATION_REFINEMENT_DEPTH,
            "monodromy_integrator": "classical RK4",
            "delay_interpolation": "four-point cubic Lagrange",
            "section": "v=v_inner(0), positive crossing",
            "left_covector_orientation": "current recovery coordinate positive",
            "breakpoint_lattices": [
                "m*sqrt(5)",
                "1+m*sqrt(5)",
            ],
        },
        "resolutions": resolutions,
        "integration_refinement": integration_refinement,
        "convergence": convergence,
        "claim_status": flags,
    }


def _sha256_path(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _validate_claims(candidate: Mapping[str, Any]) -> None:
    claims = candidate.get("claim_status")
    if not isinstance(claims, Mapping) or set(claims) != {
        *NUMERICAL_TRUE_FLAGS,
        *PROOF_FALSE_FLAGS,
    }:
        raise ValueError("separator candidate claim ledger changed")
    if any(claims.get(name) is not True for name in NUMERICAL_TRUE_FLAGS):
        raise ValueError("a recorded numerical observation was weakened")
    if any(claims.get(name) is not False for name in PROOF_FALSE_FLAGS):
        raise ValueError("a separator or onset proof flag was promoted")


def _validate_numerical_contract(candidate: Mapping[str, Any]) -> None:
    resolutions = candidate.get("resolutions")
    if not isinstance(resolutions, Sequence) or len(resolutions) != len(STEP_COUNTS):
        raise ValueError("separator resolution ladder changed")
    roots_by_depth: dict[int, list[float]] = {depth: [] for depth in CROSSING_DEPTHS}
    translation_relative_residuals: list[float] = []
    for expected_step, resolution in zip(STEP_COUNTS, resolutions, strict=True):
        if (
            not isinstance(resolution, Mapping)
            or resolution.get("step_count") != expected_step
        ):
            raise ValueError("separator resolution row changed")
        if resolution.get("observed_nontrivial_outside_unit_disk_count") != 1:
            raise ValueError("finite-section unstable count observation changed")
        leading = resolution.get("leading_multiplier")
        if not isinstance(leading, Mapping):
            raise ValueError("leading multiplier record is missing")
        if binary64_value(leading.get("real"), "leading real") <= 1.9:
            raise ValueError("leading finite-section multiplier lost separation")
        if abs(binary64_value(leading.get("imag"), "leading imag")) > 1.0e-12:
            raise ValueError("leading finite-section multiplier ceased to be real")
        if (
            binary64_value(
                resolution.get("phase_section_voltage_derivative"),
                "section derivative",
            )
            <= 0.2
        ):
            raise ValueError("phase section orientation changed")
        if (
            binary64_value(
                resolution.get("left_eigen_residual_l2"), "left residual"
            )
            >= 1.0e-11
        ):
            raise ValueError("finite left eigenpair residual changed scale")
        translation_relative_residual = binary64_value(
            resolution.get("translation_tangent_relative_residual_l2"),
            "translation tangent relative residual",
        )
        if translation_relative_residual >= 4.0e-6:
            raise ValueError("finite translation tangent residual changed scale")
        translation_relative_residuals.append(translation_relative_residual)
        rows = resolution.get("shooting_roots")
        if not isinstance(rows, Sequence) or len(rows) != len(CROSSING_DEPTHS):
            raise ValueError("shooting root ladder changed")
        previous_distance = math.inf
        for depth, row in zip(CROSSING_DEPTHS, rows, strict=True):
            if not isinstance(row, Mapping) or row.get("crossing_depth") != depth:
                raise ValueError("shooting root row changed")
            amplitude = binary64_value(row.get("pulse_amplitude"), "pulse amplitude")
            if not ROOT_BRACKET[0] <= amplitude <= ROOT_BRACKET[1]:
                raise ValueError("shooting root left the declared bracket")
            roots_by_depth[depth].append(amplitude)
            coordinate = abs(
                binary64_value(
                    row.get("finite_coordinate_at_root"), "root coordinate"
                )
            )
            if coordinate >= 2.0e-10:
                raise ValueError("stored shooting coordinate is not a root candidate")
            left_coordinate = binary64_value(
                row.get("bracket_left_coordinate"), "left bracket coordinate"
            )
            right_coordinate = binary64_value(
                row.get("bracket_right_coordinate"), "right bracket coordinate"
            )
            if left_coordinate * right_coordinate >= 0.0:
                raise ValueError("stored shooting bracket has no sign change")
            distance = binary64_value(
                row.get("reference_distance_l2"), "reference distance"
            )
            if distance >= previous_distance:
                raise ValueError("successive return did not approach the reference")
            previous_distance = distance
            scaled = binary64_value(
                row.get("multiplier_scaled_derivative"), "scaled derivative"
            )
            if abs(scaled) <= 3.0:
                raise ValueError("scaled shooting derivative lost nondegeneracy")
    if max(roots_by_depth[3]) - min(roots_by_depth[3]) >= 5.0e-12:
        raise ValueError("third-return roots lost cross-resolution agreement")
    for resolution in resolutions:
        rows = resolution["shooting_roots"]
        root2 = binary64_value(rows[1]["pulse_amplitude"], "root2")
        root3 = binary64_value(rows[2]["pulse_amplitude"], "root3")
        if abs(root3 - root2) >= 5.0e-12:
            raise ValueError("successive-return roots ceased to converge")
        distance3 = binary64_value(rows[2]["reference_distance_l2"], "distance3")
        if distance3 >= 3.0e-12:
            raise ValueError("third return no longer approaches the inner reference")
    if any(
        right >= left
        for left, right in zip(
            translation_relative_residuals,
            translation_relative_residuals[1:],
        )
    ):
        raise ValueError(
            "translation tangent residual did not decrease with refinement"
        )


def validate_candidate_body(candidate: Mapping[str, Any]) -> None:
    expected_keys = {
        "schema_id",
        "model_id",
        "parent_branch",
        "parent_periodic_orbit_existence_validated",
        "finite_section_uses_binary64_polynomial_center",
        "method",
        "resolutions",
        "integration_refinement",
        "convergence",
        "claim_status",
    }
    if not isinstance(candidate, Mapping) or set(candidate) != expected_keys:
        raise ValueError("separator candidate body schema changed")
    if candidate.get("schema_id") != SCHEMA_ID or candidate.get("model_id") != MODEL_ID:
        raise ValueError("separator candidate identity changed")
    if candidate.get("parent_branch") != BRANCH:
        raise ValueError("separator candidate parent branch changed")
    if candidate.get("finite_section_uses_binary64_polynomial_center") is not True:
        raise ValueError("finite-section center disclosure was removed")
    method = candidate.get("method")
    if not isinstance(method, Mapping):
        raise ValueError("separator method record is missing")
    if method.get("step_counts") != list(STEP_COUNTS) or method.get(
        "crossing_depths"
    ) != list(CROSSING_DEPTHS):
        raise ValueError("separator mesh or return ladder changed")
    _validate_claims(candidate)
    _validate_numerical_contract(candidate)
    refinement = candidate.get("integration_refinement")
    if not isinstance(refinement, Sequence) or len(refinement) != len(
        INTEGRATION_REFINEMENT_SETTINGS
    ):
        raise ValueError("integration refinement ladder changed")
    refinement_roots = []
    for expected, row in zip(INTEGRATION_REFINEMENT_SETTINGS, refinement, strict=True):
        if not isinstance(row, Mapping):
            raise ValueError("integration refinement row is not a mapping")
        actual = (
            binary64_value(row.get("integration_rtol"), "refinement rtol"),
            binary64_value(row.get("integration_atol"), "refinement atol"),
            binary64_value(row.get("integration_max_step"), "refinement max step"),
        )
        if actual != expected:
            raise ValueError("integration refinement settings changed")
        refinement_roots.append(
            binary64_value(row.get("pulse_amplitude"), "refined root")
        )
        if (
            abs(
                binary64_value(
                    row.get("finite_coordinate_at_root"), "refined coordinate"
                )
            )
            >= 2.0e-10
        ):
            raise ValueError("refined shooting coordinate is not a root candidate")
        left_coordinate = binary64_value(
            row.get("bracket_left_coordinate"), "refined left bracket coordinate"
        )
        right_coordinate = binary64_value(
            row.get("bracket_right_coordinate"), "refined right bracket coordinate"
        )
        if left_coordinate * right_coordinate >= 0.0:
            raise ValueError("refined shooting bracket has no sign change")
    if max(refinement_roots) - min(refinement_roots) >= 5.0e-11:
        raise ValueError("integration refinement roots lost agreement")
    if EXPECTED_CANDIDATE_SHA256 is None:
        raise ValueError("separator candidate has no source-registered digest")
    if canonical_sha256(candidate) != EXPECTED_CANDIDATE_SHA256:
        raise ValueError("separator candidate differs from source-registered body")


def validate_separator_candidate_result(
    payload: Mapping[str, Any], repository: Path
) -> None:
    if not isinstance(payload, Mapping) or set(payload) != {"candidate", "manifest"}:
        raise ValueError("separator result requires candidate and manifest")
    candidate = payload.get("candidate")
    manifest = payload.get("manifest")
    if not isinstance(candidate, Mapping) or not isinstance(manifest, Mapping):
        raise ValueError("separator result records must be mappings")
    validate_candidate_body(candidate)
    sources = {
        "source": SOURCE_RELATIVE_PATH,
        "generator": GENERATOR_RELATIVE_PATH,
        "note": NOTE_RELATIVE_PATH,
        "model_source": MODEL_SOURCE_RELATIVE_PATH,
        "terminal_history_source": TERMINAL_HISTORY_SOURCE_RELATIVE_PATH,
        "parent_artifact_source": PARENT_ARTIFACT_SOURCE_RELATIVE_PATH,
        "parent_artifact_result": PARENT_ARTIFACT_RESULT_RELATIVE_PATH,
    }
    expected_keys = {
        "schema_id",
        "candidate_sha256",
        "default_command",
        "arithmetic_scope",
        "python",
        "platform",
        "numpy",
        "scipy",
        *sources.keys(),
        *(f"{name}_sha256" for name in sources),
    }
    if set(manifest) != expected_keys:
        raise ValueError("separator manifest schema changed")
    if manifest.get("schema_id") != SCHEMA_ID:
        raise ValueError("separator manifest identity changed")
    if manifest.get("candidate_sha256") != canonical_sha256(candidate):
        raise ValueError("separator manifest candidate digest changed")
    if manifest.get("default_command") != DEFAULT_COMMAND or manifest.get(
        "arithmetic_scope"
    ) != ARITHMETIC_SCOPE:
        raise ValueError("separator manifest method disclosure changed")
    versions = {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
    }
    for name, expected in versions.items():
        if manifest.get(name) != expected:
            raise ValueError(f"separator manifest {name} changed")
    for name, relative in sources.items():
        if manifest.get(name) != relative:
            raise ValueError(f"separator manifest {name} path changed")
        if manifest.get(f"{name}_sha256") != _sha256_path(repository / relative):
            raise ValueError(f"separator manifest {name} hash changed")


__all__ = [
    "ARITHMETIC_SCOPE",
    "BRANCH",
    "CROSSING_DEPTHS",
    "DEFAULT_COMMAND",
    "EXPECTED_CANDIDATE_SHA256",
    "GENERATOR_RELATIVE_PATH",
    "MODEL_ID",
    "NOTE_RELATIVE_PATH",
    "NUMERICAL_TRUE_FLAGS",
    "PARENT_ARTIFACT_RESULT_RELATIVE_PATH",
    "PROOF_FALSE_FLAGS",
    "RESULT_RELATIVE_PATH",
    "ROOT_BRACKET",
    "SCHEMA_ID",
    "SOURCE_RELATIVE_PATH",
    "STEP_COUNTS",
    "binary64_record",
    "binary64_value",
    "build_candidate",
    "canonical_sha256",
    "finite_section",
    "method_of_steps_breakpoints",
    "shooting_data",
    "simulate_physical_pulse",
    "validate_candidate_body",
    "validate_separator_candidate_result",
]
