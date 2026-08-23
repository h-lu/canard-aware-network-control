"""Floating-point periodic-orbit candidates for the synchronous FHN RFDE.

This module implements an odd Fourier collocation discretization of the
two-delay synchronous equation declared in ``docs/two-module-reference.md``.
It is deliberately a *candidate generator*, not a validated-numerics
library: NumPy and SciPy do not provide directed rounding, the finite
Fourier tail is not enclosed, and the reported singular values concern a
finite bordered matrix only.

The implementation nevertheless preserves the analytic structure needed
by a later proof.  In particular, the period column differentiates the
normalized delay fractions ``tau_j / T``; the two gain sensitivities solve
the bordered first-variation equation; and independent discrete adjoints
must reproduce both response rows.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, replace
from typing import Iterable, Sequence

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq


@dataclass(frozen=True)
class FHNPeriodicParameters:
    """Parameters of the completely synchronous two-delay FHN equation."""

    epsilon: float = 0.2
    unfolding: float = 0.6
    theta_0: float = 4.0
    theta_1: float = 5.0
    kappa_1: float = 0.2
    kappa_3: float = 0.25

    def __post_init__(self) -> None:
        values = np.asarray(tuple(asdict(self).values()), dtype=float)
        if not np.all(np.isfinite(values)):
            raise ValueError("all FHN parameters must be finite")
        if self.epsilon <= 0.0:
            raise ValueError("epsilon must be positive")
        if not -1.0 < self.unfolding < 1.0:
            raise ValueError(
                "the candidate generator requires -1 < unfolding < 1"
            )
        if self.theta_0 <= 0.0 or self.theta_1 <= 0.0:
            raise ValueError("scaled delays must be positive")

    @property
    def physical_delays(self) -> tuple[float, float]:
        scale = np.sqrt(self.epsilon)
        return (self.theta_0 / scale, self.theta_1 / scale)


@dataclass(frozen=True)
class PeriodicOrbitCandidate:
    """One finite Fourier-collocation orbit and its Newton diagnostics."""

    parameters: FHNPeriodicParameters
    phase_nodes: np.ndarray
    state: np.ndarray
    period: float
    collocation_residual_inf: float
    oversampled_residual_inf: float
    newton_iterations: int
    final_step_inf: float
    spectral_tail_l1: float


@dataclass(frozen=True)
class ExtremaCandidate:
    """Floating-point root and curvature checks for the voltage extrema."""

    root_phases: tuple[float, ...]
    maximum_phase: float
    minimum_phase: float
    maximum_voltage: float
    minimum_voltage: float
    maximum_curvature: float
    minimum_curvature: float
    minimum_root_separation: float
    unique_maximum_and_minimum_candidate: bool


@dataclass(frozen=True)
class BorderedMatrixCandidate:
    """Finite-dimensional diagnostics for the bordered periodic BVP."""

    dimension: int
    smallest_singular_value: float
    largest_singular_value: float
    condition_number_2: float
    inverse_defect_inf: float
    phase_tangent_pairing: float
    translation_residual_inf: float


@dataclass(frozen=True)
class PeriodicResponseCandidate:
    """Frequency--squared-range derivative at one collocation orbit."""

    control_order: tuple[str, str]
    response_matrix: np.ndarray
    period_derivatives: np.ndarray
    forward_adjoint_disagreement_inf: float
    bordered: BorderedMatrixCandidate
    extrema: ExtremaCandidate


@dataclass(frozen=True)
class ResponseBoxCandidate:
    """Sampled floating-point enclosure proposal over a gain box.

    ``entrywise_radius`` encloses only the matrices actually sampled, plus
    the declared numerical-discrepancy padding.  It is not an interval
    enclosure of the continuum between samples.
    """

    center: FHNPeriodicParameters
    half_widths: tuple[float, float]
    sample_controls: np.ndarray
    midpoint_response: np.ndarray
    centered_output_finite_difference: np.ndarray
    centered_output_finite_difference_disagreement_inf: float
    entrywise_radius: np.ndarray
    sampled_smallest_singular_value: float
    midpoint_smallest_singular_value: float
    frobenius_radius: float
    candidate_beta: float
    maximum_collocation_residual_inf: float
    maximum_oversampled_residual_inf: float
    minimum_bordered_singular_value: float
    maximum_forward_adjoint_disagreement_inf: float
    all_sampled_extrema_simple: bool


@dataclass(frozen=True)
class ODEPersistenceRouteCandidate:
    """Nonrigorous inputs for an ODE-to-delay persistence proof route.

    The theorem of Gimeno--Lessard--Mireles James--Yang is not evaluated
    here.  In particular, these sampled quantities are not coefficients of
    its interval polynomial inequalities.
    """

    ode_period: float
    ode_monodromy: np.ndarray
    ode_floquet_multipliers: np.ndarray
    tangent_multiplier_error: float
    nontrivial_multiplier_distance_from_one: float
    maximum_forward_variational_norm_2: float
    maximum_backward_variational_norm_2: float
    target_orbit_c0_distance_after_discrete_phase_alignment: float
    target_phase_shift_nodes: int
    physical_delays: tuple[float, float]
    normalized_delay_fractions_at_target: tuple[float, float]
    sampled_perturbation_norm: float
    sampled_perturbation_state_jacobian_norm: float
    perturbation_amplitude_times_norm: float
    direct_single_delay_theorem_applies: bool
    required_adaptations: tuple[str, ...]


def odd_fourier_matrices(
    node_count: int, delay_fraction: float = 0.0
) -> tuple[np.ndarray, np.ndarray]:
    """Return real Fourier derivative and retarded-shift matrices.

    Odd node counts avoid the unpaired Nyquist mode.  If ``S`` is the
    second returned matrix, then ``S @ x`` samples
    ``x(theta-delay_fraction)`` for every resolved trigonometric polynomial.
    """

    if isinstance(node_count, bool) or int(node_count) != node_count:
        raise ValueError("node_count must be an odd integer")
    count = int(node_count)
    if count < 5 or count % 2 == 0:
        raise ValueError("node_count must be odd and at least five")
    fraction = float(delay_fraction)
    if not np.isfinite(fraction):
        raise ValueError("delay_fraction must be finite")
    modes = np.fft.fftfreq(count, d=1.0 / count)
    transformed_basis = np.fft.fft(np.eye(count), axis=0)
    derivative = np.fft.ifft(
        (2.0j * np.pi * modes)[:, None] * transformed_basis,
        axis=0,
    ).real
    shift = np.fft.ifft(
        np.exp(-2.0j * np.pi * modes * fraction)[:, None]
        * transformed_basis,
        axis=0,
    ).real
    return derivative, shift


def _validated_state(state: np.ndarray, node_count: int) -> np.ndarray:
    values = np.asarray(state, dtype=float)
    if values.shape != (node_count, 2):
        raise ValueError(f"state must have shape ({node_count}, 2)")
    if not np.all(np.isfinite(values)):
        raise ValueError("state must be finite")
    return values


def _field_data(
    voltage: np.ndarray,
    recovery: np.ndarray,
    delayed_0: np.ndarray,
    delayed_1: np.ndarray,
    parameters: FHNPeriodicParameters,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    eps = parameters.epsilon
    linear_difference = (delayed_0 + delayed_1) / 2.0 - voltage
    cubic_difference = (
        ((delayed_0 - 1.0) ** 3 + (delayed_1 - 1.0) ** 3) / 2.0
        - (voltage - 1.0) ** 3
    )
    fast = (
        voltage
        - voltage**3 / 3.0
        - recovery
        + eps * parameters.kappa_1 * linear_difference
        + eps * parameters.kappa_3 * cubic_difference
    )
    slow = eps * (voltage - parameters.unfolding)
    return fast, slow, linear_difference, cubic_difference


def _collocation_system(
    unknown: np.ndarray,
    parameters: FHNPeriodicParameters,
    derivative: np.ndarray,
    phase_reference: np.ndarray,
    phase_reference_derivative: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, tuple[np.ndarray, np.ndarray]]:
    count = derivative.shape[0]
    vector = np.asarray(unknown, dtype=float)
    if vector.shape != (2 * count + 1,):
        raise ValueError("unknown has incompatible shape")
    voltage = vector[:count]
    recovery = vector[count : 2 * count]
    period = float(vector[-1])
    if not np.isfinite(period) or period <= 0.0:
        raise ValueError("period iterate must be positive and finite")

    tau_0, tau_1 = parameters.physical_delays
    _, shift_0 = odd_fourier_matrices(count, tau_0 / period)
    _, shift_1 = odd_fourier_matrices(count, tau_1 / period)
    delayed_0 = shift_0 @ voltage
    delayed_1 = shift_1 @ voltage
    fast, slow, _, _ = _field_data(
        voltage, recovery, delayed_0, delayed_1, parameters
    )

    residual_fast = derivative @ voltage - period * fast
    residual_slow = derivative @ recovery - period * slow
    phase = float(
        np.vdot(
            phase_reference_derivative,
            np.column_stack((voltage, recovery)) - phase_reference,
        ).real
        / count
    )
    residual = np.concatenate((residual_fast, residual_slow, [phase]))

    eps = parameters.epsilon
    current_voltage = (
        1.0
        - voltage**2
        - eps * parameters.kappa_1
        - 3.0 * eps * parameters.kappa_3 * (voltage - 1.0) ** 2
    )
    delayed_voltage_0 = eps / 2.0 * (
        parameters.kappa_1
        + 3.0 * parameters.kappa_3 * (delayed_0 - 1.0) ** 2
    )
    delayed_voltage_1 = eps / 2.0 * (
        parameters.kappa_1
        + 3.0 * parameters.kappa_3 * (delayed_1 - 1.0) ** 2
    )

    identity = np.eye(count)
    jacobian = np.zeros((2 * count + 1, 2 * count + 1), dtype=float)
    jacobian[:count, :count] = derivative - period * (
        np.diag(current_voltage)
        + np.diag(delayed_voltage_0) @ shift_0
        + np.diag(delayed_voltage_1) @ shift_1
    )
    jacobian[:count, count : 2 * count] = period * identity
    jacobian[count : 2 * count, :count] = -period * eps * identity
    jacobian[count : 2 * count, count : 2 * count] = derivative

    delayed_tangent_0 = shift_0 @ (derivative @ voltage)
    delayed_tangent_1 = shift_1 @ (derivative @ voltage)
    period_column_fast = -fast - (
        tau_0 / period * delayed_voltage_0 * delayed_tangent_0
        + tau_1 / period * delayed_voltage_1 * delayed_tangent_1
    )
    jacobian[:count, -1] = period_column_fast
    jacobian[count : 2 * count, -1] = -slow
    jacobian[-1, :count] = phase_reference_derivative[:, 0] / count
    jacobian[-1, count : 2 * count] = (
        phase_reference_derivative[:, 1] / count
    )
    return residual, jacobian, (shift_0, shift_1)


def _ode_cycle_initial_guess(
    parameters: FHNPeriodicParameters,
    node_count: int,
) -> tuple[np.ndarray, float]:
    """Approach the uncoupled FHN limit cycle and sample its last period."""

    def field(_time: float, state: np.ndarray) -> np.ndarray:
        voltage, recovery = state
        return np.array(
            [
                voltage - voltage**3 / 3.0 - recovery,
                parameters.epsilon * (voltage - parameters.unfolding),
            ]
        )

    def positive_crossing(_time: float, state: np.ndarray) -> float:
        return float(state[0] - parameters.unfolding)

    positive_crossing.direction = 1.0  # type: ignore[attr-defined]
    positive_crossing.terminal = False  # type: ignore[attr-defined]
    duration = max(500.0, 40.0 / parameters.epsilon)
    integration = solve_ivp(
        field,
        (0.0, duration),
        np.array([1.8, 0.0]),
        events=positive_crossing,
        dense_output=True,
        rtol=2.0e-11,
        atol=2.0e-13,
        max_step=0.08,
    )
    events = integration.t_events[0]
    if not integration.success or events.size < 4 or integration.sol is None:
        raise RuntimeError("failed to obtain an uncoupled FHN cycle")
    start, finish = float(events[-2]), float(events[-1])
    period = finish - start
    phases = np.arange(node_count, dtype=float) / node_count
    state = integration.sol(start + period * phases).T
    return state, period


def solve_fhn_periodic_orbit(
    parameters: FHNPeriodicParameters = FHNPeriodicParameters(),
    *,
    node_count: int = 97,
    initial: PeriodicOrbitCandidate | None = None,
    residual_tolerance: float = 2.0e-11,
    step_tolerance: float = 2.0e-12,
    maximum_iterations: int = 18,
    continuation_steps: int = 8,
) -> PeriodicOrbitCandidate:
    """Compute a floating-point periodic-orbit candidate.

    With no supplied candidate, the function starts from the uncoupled FHN
    ODE and continues both delayed gains linearly to their requested values.
    A supplied candidate must use the same node count and is used directly
    as the Newton initial value.
    """

    if not np.isfinite(residual_tolerance) or residual_tolerance <= 0.0:
        raise ValueError("residual_tolerance must be finite and positive")
    if not np.isfinite(step_tolerance) or step_tolerance <= 0.0:
        raise ValueError("step_tolerance must be finite and positive")
    if (
        isinstance(maximum_iterations, bool)
        or int(maximum_iterations) != maximum_iterations
        or maximum_iterations < 1
    ):
        raise ValueError("maximum_iterations must be a positive integer")
    if (
        isinstance(continuation_steps, bool)
        or int(continuation_steps) != continuation_steps
        or continuation_steps < 1
    ):
        raise ValueError("continuation_steps must be a positive integer")
    derivative, _ = odd_fourier_matrices(node_count)
    if initial is None:
        state, period = _ode_cycle_initial_guess(parameters, node_count)
        start_parameters = replace(parameters, kappa_1=0.0, kappa_3=0.0)
        path = [
            replace(
                parameters,
                kappa_1=parameters.kappa_1 * index / continuation_steps,
                kappa_3=parameters.kappa_3 * index / continuation_steps,
            )
            for index in range(continuation_steps + 1)
        ]
        path[0] = start_parameters
    else:
        state = _validated_state(initial.state, node_count).copy()
        period = float(initial.period)
        path = [parameters]

    total_iterations = 0
    final_step = np.inf
    final_residual = np.inf
    for path_parameters in path:
        phase_reference = state.copy()
        phase_reference_derivative = derivative @ phase_reference
        unknown = np.concatenate((state[:, 0], state[:, 1], [period]))
        converged = False
        for _ in range(maximum_iterations):
            residual, jacobian, _ = _collocation_system(
                unknown,
                path_parameters,
                derivative,
                phase_reference,
                phase_reference_derivative,
            )
            final_residual = float(np.linalg.norm(residual, ord=np.inf))
            if final_residual <= residual_tolerance and final_step <= step_tolerance:
                converged = True
                break
            step = np.linalg.solve(jacobian, -residual)
            final_step = float(np.linalg.norm(step, ord=np.inf))
            merit = final_residual
            accepted = False
            damping = 1.0
            for _line_search in range(14):
                proposal = unknown + damping * step
                if proposal[-1] <= 0.0:
                    damping *= 0.5
                    continue
                proposal_residual, _, _ = _collocation_system(
                    proposal,
                    path_parameters,
                    derivative,
                    phase_reference,
                    phase_reference_derivative,
                )
                proposal_merit = float(
                    np.linalg.norm(proposal_residual, ord=np.inf)
                )
                if proposal_merit < merit:
                    unknown = proposal
                    final_step *= damping
                    accepted = True
                    break
                damping *= 0.5
            total_iterations += 1
            if not accepted:
                break
        residual, _, _ = _collocation_system(
            unknown,
            path_parameters,
            derivative,
            phase_reference,
            phase_reference_derivative,
        )
        final_residual = float(np.linalg.norm(residual, ord=np.inf))
        if not converged:
            converged = (
                final_residual <= residual_tolerance
                and final_step <= 20.0 * step_tolerance
            )
        if not converged:
            raise RuntimeError(
                "Fourier--Newton solve failed at "
                f"(kappa_1,kappa_3)=({path_parameters.kappa_1},"
                f"{path_parameters.kappa_3}); residual={final_residual:.3e}, "
                f"step={final_step:.3e}"
            )
        state = np.column_stack((unknown[:node_count], unknown[node_count:-1]))
        period = float(unknown[-1])

    phases = np.arange(node_count, dtype=float) / node_count
    tail = _spectral_tail_l1(state)
    oversampled = oversampled_orbit_residual(
        state, period, parameters, oversampling_factor=6
    )
    return PeriodicOrbitCandidate(
        parameters=parameters,
        phase_nodes=phases,
        state=state,
        period=period,
        collocation_residual_inf=final_residual,
        oversampled_residual_inf=oversampled,
        newton_iterations=total_iterations,
        final_step_inf=final_step,
        spectral_tail_l1=tail,
    )


def _fourier_coefficients(values: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    array = np.asarray(values, dtype=float)
    count = array.shape[0]
    coefficients = np.fft.fft(array, axis=0) / count
    modes = np.fft.fftfreq(count, d=1.0 / count)
    return coefficients, modes


def _evaluate_fourier(
    values: np.ndarray,
    phases: np.ndarray | float,
    derivative_order: int = 0,
) -> np.ndarray:
    coefficients, modes = _fourier_coefficients(values)
    points = np.atleast_1d(np.asarray(phases, dtype=float))
    multiplier = (2.0j * np.pi * modes) ** derivative_order
    basis = np.exp(2.0j * np.pi * points[:, None] * modes[None, :])
    evaluated = basis @ (multiplier[:, None] * coefficients.reshape(len(modes), -1))
    real = np.real_if_close(evaluated, tol=1000).real
    if np.ndim(phases) == 0:
        return real[0]
    return real


def _spectral_tail_l1(state: np.ndarray) -> float:
    coefficients, modes = _fourier_coefficients(state)
    cutoff = max(1, int(np.floor(0.8 * np.max(np.abs(modes)))))
    return float(np.sum(np.abs(coefficients[np.abs(modes) >= cutoff])))


def oversampled_orbit_residual(
    state: np.ndarray,
    period: float,
    parameters: FHNPeriodicParameters,
    *,
    oversampling_factor: int = 6,
) -> float:
    """Evaluate the spectral polynomial in the RFDE away from its nodes."""

    values = np.asarray(state, dtype=float)
    count = values.shape[0]
    _validated_state(values, count)
    if oversampling_factor < 2:
        raise ValueError("oversampling_factor must be at least two")
    sample_count = oversampling_factor * count
    phases = (np.arange(sample_count, dtype=float) + 0.38196601125) / sample_count
    current = _evaluate_fourier(values, phases)
    tangent = _evaluate_fourier(values, phases, derivative_order=1)
    tau_0, tau_1 = parameters.physical_delays
    delayed_0 = _evaluate_fourier(values[:, 0], phases - tau_0 / period)
    delayed_1 = _evaluate_fourier(values[:, 0], phases - tau_1 / period)
    fast, slow, _, _ = _field_data(
        current[:, 0], current[:, 1], delayed_0[:, 0], delayed_1[:, 0], parameters
    )
    residual = tangent - period * np.column_stack((fast, slow))
    return float(np.linalg.norm(residual, ord=np.inf))


def voltage_extrema_candidate(
    orbit: PeriodicOrbitCandidate,
    *,
    scan_factor: int = 24,
) -> ExtremaCandidate:
    """Locate all resolved voltage critical points and test simple extrema."""

    if (
        isinstance(scan_factor, bool)
        or int(scan_factor) != scan_factor
        or scan_factor < 4
    ):
        raise ValueError("scan_factor must be an integer of at least four")
    voltage = orbit.state[:, 0]
    count = len(voltage)
    scan_count = scan_factor * count
    phases = np.arange(scan_count + 1, dtype=float) / scan_count

    def tangent(phase: float) -> float:
        return float(_evaluate_fourier(voltage, phase, 1)[0])

    tangent_values = _evaluate_fourier(voltage, phases, 1)[:, 0]
    roots: list[float] = []
    for index in range(scan_count):
        left = float(phases[index])
        right = float(phases[index + 1])
        left_value = float(tangent_values[index])
        right_value = float(tangent_values[index + 1])
        if left_value == 0.0:
            root = left
        elif left_value * right_value < 0.0:
            root = float(brentq(tangent, left, right, xtol=2.0e-14))
        else:
            continue
        root %= 1.0
        if not roots or min(abs(root - item) for item in roots) > 1.0e-9:
            roots.append(root)
    roots.sort()
    if not roots:
        raise RuntimeError("no voltage extrema found")
    root_array = np.asarray(roots)
    voltages = _evaluate_fourier(voltage, root_array)[:, 0]
    curvatures = _evaluate_fourier(voltage, root_array, 2)[:, 0]
    maximum_index = int(np.argmax(voltages))
    minimum_index = int(np.argmin(voltages))
    cyclic_separations = np.diff(np.r_[root_array, root_array[0] + 1.0])
    simple_pair = (
        len(roots) == 2
        and curvatures[maximum_index] < 0.0
        and curvatures[minimum_index] > 0.0
        and maximum_index != minimum_index
    )
    return ExtremaCandidate(
        root_phases=tuple(float(item) for item in roots),
        maximum_phase=float(root_array[maximum_index]),
        minimum_phase=float(root_array[minimum_index]),
        maximum_voltage=float(voltages[maximum_index]),
        minimum_voltage=float(voltages[minimum_index]),
        maximum_curvature=float(curvatures[maximum_index]),
        minimum_curvature=float(curvatures[minimum_index]),
        minimum_root_separation=float(np.min(cyclic_separations)),
        unique_maximum_and_minimum_candidate=bool(simple_pair),
    )


def periodic_response_candidate(
    orbit: PeriodicOrbitCandidate,
) -> PeriodicResponseCandidate:
    """Compute the gain response by bordered forward and adjoint solves."""

    parameters = orbit.parameters
    state = np.asarray(orbit.state, dtype=float)
    count = len(state)
    derivative, _ = odd_fourier_matrices(count)
    reference_derivative = derivative @ state
    unknown = np.concatenate((state[:, 0], state[:, 1], [orbit.period]))
    residual, jacobian, shifts = _collocation_system(
        unknown,
        parameters,
        derivative,
        state,
        reference_derivative,
    )
    delayed_0 = shifts[0] @ state[:, 0]
    delayed_1 = shifts[1] @ state[:, 0]
    _, _, linear_field, cubic_field = _field_data(
        state[:, 0], state[:, 1], delayed_0, delayed_1, parameters
    )
    right_hand_sides = np.zeros((2 * count + 1, 2), dtype=float)
    right_hand_sides[:count, 0] = (
        orbit.period * parameters.epsilon * linear_field
    )
    right_hand_sides[:count, 1] = (
        orbit.period * parameters.epsilon * cubic_field
    )
    sensitivities = np.linalg.solve(jacobian, right_hand_sides)
    period_derivatives = sensitivities[-1, :]

    extrema = voltage_extrema_candidate(orbit)
    maximum_rows = _fourier_evaluation_rows(
        count, extrema.maximum_phase, derivative_order=0
    )
    minimum_rows = _fourier_evaluation_rows(
        count, extrema.minimum_phase, derivative_order=0
    )
    delta = extrema.maximum_voltage - extrema.minimum_voltage
    response_gradient_amplitude = np.zeros(2 * count + 1, dtype=float)
    response_gradient_amplitude[:count] = (
        2.0 * delta * (maximum_rows - minimum_rows)
    )
    response_gradient_frequency = np.zeros(2 * count + 1, dtype=float)
    response_gradient_frequency[-1] = -1.0 / orbit.period**2
    output_gradients = np.column_stack(
        (response_gradient_frequency, response_gradient_amplitude)
    )
    forward_response = output_gradients.T @ sensitivities
    adjoints = np.linalg.solve(jacobian.T, output_gradients)
    adjoint_response = adjoints.T @ right_hand_sides
    disagreement = float(
        np.linalg.norm(forward_response - adjoint_response, ord=np.inf)
    )

    singular_values = np.linalg.svd(jacobian, compute_uv=False)
    inverse = np.linalg.inv(jacobian)
    inverse_defect = float(
        np.linalg.norm(np.eye(jacobian.shape[0]) - jacobian @ inverse, ord=np.inf)
    )
    tangent_vector = np.concatenate(
        (reference_derivative[:, 0], reference_derivative[:, 1])
    )
    unbordered_translation = jacobian[:-1, :-1] @ tangent_vector
    phase_pairing = float(np.vdot(reference_derivative, reference_derivative) / count)
    bordered = BorderedMatrixCandidate(
        dimension=int(jacobian.shape[0]),
        smallest_singular_value=float(singular_values[-1]),
        largest_singular_value=float(singular_values[0]),
        condition_number_2=float(singular_values[0] / singular_values[-1]),
        inverse_defect_inf=inverse_defect,
        phase_tangent_pairing=phase_pairing,
        translation_residual_inf=float(
            np.linalg.norm(unbordered_translation, ord=np.inf)
        ),
    )
    if np.linalg.norm(residual, ord=np.inf) > 20.0 * max(
        orbit.collocation_residual_inf, 1.0e-14
    ):
        raise RuntimeError("stored orbit is inconsistent with its parameters")
    return PeriodicResponseCandidate(
        control_order=("kappa_1", "kappa_3"),
        response_matrix=forward_response,
        period_derivatives=period_derivatives,
        forward_adjoint_disagreement_inf=disagreement,
        bordered=bordered,
        extrema=extrema,
    )


def _fourier_evaluation_rows(
    node_count: int,
    phase: float,
    *,
    derivative_order: int,
) -> np.ndarray:
    modes = np.fft.fftfreq(node_count, d=1.0 / node_count)
    weights = (
        np.exp(2.0j * np.pi * modes * phase)
        * (2.0j * np.pi * modes) ** derivative_order
    )
    # For x_hat=FFT(x)/n, evaluation is weights @ FFT(x)/n.
    rows = np.fft.fft(np.eye(node_count), axis=0)
    return np.real_if_close(weights @ rows / node_count, tol=1000).real


def sampled_response_box_candidate(
    center: FHNPeriodicParameters = FHNPeriodicParameters(),
    *,
    half_widths: tuple[float, float] = (5.0e-5, 5.0e-5),
    node_count: int = 129,
    sample_levels: Sequence[float] = (-1.0, 0.0, 1.0),
) -> tuple[ResponseBoxCandidate, tuple[PeriodicOrbitCandidate, ...]]:
    """Sample a gain box and propose entrywise response radii.

    The center is solved first.  Every other sample is initialized from the
    center, so no path-dependent reuse of a neighboring sample can hide a
    branch switch.  The returned radii cover the finite sample only.
    """

    widths = np.asarray(half_widths, dtype=float)
    if widths.shape != (2,) or np.any(~np.isfinite(widths)) or np.any(widths <= 0):
        raise ValueError("half_widths must contain two finite positive values")
    levels = tuple(float(item) for item in sample_levels)
    if len(levels) < 2 or any(not np.isfinite(item) for item in levels):
        raise ValueError("sample_levels must contain at least two finite values")
    if len(set(levels)) != len(levels):
        raise ValueError("sample_levels must not contain duplicates")
    if not {-1.0, 0.0, 1.0}.issubset(levels):
        raise ValueError("sample_levels must include -1, zero, and 1")

    central_orbit = solve_fhn_periodic_orbit(center, node_count=node_count)
    central_response = periodic_response_candidate(central_orbit)
    controls: list[tuple[float, float]] = []
    orbits: list[PeriodicOrbitCandidate] = []
    responses: list[PeriodicResponseCandidate] = []
    for level_1 in levels:
        for level_3 in levels:
            parameters = replace(
                center,
                kappa_1=center.kappa_1 + level_1 * widths[0],
                kappa_3=center.kappa_3 + level_3 * widths[1],
            )
            if level_1 == 0.0 and level_3 == 0.0:
                orbit = central_orbit
                response = central_response
            else:
                orbit = solve_fhn_periodic_orbit(
                    parameters,
                    node_count=node_count,
                    initial=central_orbit,
                )
                response = periodic_response_candidate(orbit)
            controls.append((parameters.kappa_1, parameters.kappa_3))
            orbits.append(orbit)
            responses.append(response)

    matrices = np.asarray([item.response_matrix for item in responses])
    midpoint = central_response.response_matrix
    level_indices: dict[tuple[float, float], int] = {}
    for index, pair in enumerate(
        [(level_1, level_3) for level_1 in levels for level_3 in levels]
    ):
        level_indices[pair] = index

    def outputs(index: int) -> np.ndarray:
        sample_orbit = orbits[index]
        sample_extrema = responses[index].extrema
        voltage_range = (
            sample_extrema.maximum_voltage - sample_extrema.minimum_voltage
        )
        return np.array([1.0 / sample_orbit.period, voltage_range**2])

    finite_difference = np.column_stack(
        (
            (
                outputs(level_indices[(1.0, 0.0)])
                - outputs(level_indices[(-1.0, 0.0)])
            )
            / (2.0 * widths[0]),
            (
                outputs(level_indices[(0.0, 1.0)])
                - outputs(level_indices[(0.0, -1.0)])
            )
            / (2.0 * widths[1]),
        )
    )
    finite_difference_disagreement = float(
        np.linalg.norm(finite_difference - midpoint, ord=np.inf)
    )
    # Only a numerical padding: forward/adjoint disagreement and residuals
    # are not rigorous error estimators, much less tail enclosures.
    discrepancy = max(
        max(item.forward_adjoint_disagreement_inf for item in responses),
        max(item.collocation_residual_inf for item in orbits),
        finite_difference_disagreement,
    )
    radius = np.max(np.abs(matrices - midpoint[None, :, :]), axis=0)
    radius += 10.0 * discrepancy
    midpoint_smin = float(np.linalg.svd(midpoint, compute_uv=False)[-1])
    frobenius_radius = float(np.linalg.norm(radius, ord="fro"))
    sampled_smins = np.linalg.svd(matrices, compute_uv=False)[:, -1]
    result = ResponseBoxCandidate(
        center=center,
        half_widths=(float(widths[0]), float(widths[1])),
        sample_controls=np.asarray(controls),
        midpoint_response=midpoint,
        centered_output_finite_difference=finite_difference,
        centered_output_finite_difference_disagreement_inf=(
            finite_difference_disagreement
        ),
        entrywise_radius=radius,
        sampled_smallest_singular_value=float(np.min(sampled_smins)),
        midpoint_smallest_singular_value=midpoint_smin,
        frobenius_radius=frobenius_radius,
        candidate_beta=midpoint_smin - frobenius_radius,
        maximum_collocation_residual_inf=max(
            item.collocation_residual_inf for item in orbits
        ),
        maximum_oversampled_residual_inf=max(
            item.oversampled_residual_inf for item in orbits
        ),
        minimum_bordered_singular_value=min(
            item.bordered.smallest_singular_value for item in responses
        ),
        maximum_forward_adjoint_disagreement_inf=max(
            item.forward_adjoint_disagreement_inf for item in responses
        ),
        all_sampled_extrema_simple=all(
            item.extrema.unique_maximum_and_minimum_candidate
            for item in responses
        ),
    )
    return result, tuple(orbits)


def ode_persistence_route_candidate(
    orbit: PeriodicOrbitCandidate,
) -> ODEPersistenceRouteCandidate:
    """Audit the primary ODE-persistence route with floating-point data.

    The unperturbed equation is the FHN core obtained by setting both
    delayed gains to zero while keeping the same fixed ``epsilon`` and
    ``unfolding``.  The full feedback is then a sum of a zero-delay current
    perturbation and two constant-delay perturbations, all multiplied by
    ``epsilon``.  The published single-delay theorem therefore motivates,
    but does not literally cover, this decomposition.
    """

    parameters = orbit.parameters
    node_count = len(orbit.state)
    ode_state, ode_period = _ode_cycle_initial_guess(parameters, node_count)

    def augmented_field(_time: float, augmented: np.ndarray) -> np.ndarray:
        voltage, recovery = augmented[:2]
        fundamental = augmented[2:].reshape(2, 2)
        field = np.array(
            [
                voltage - voltage**3 / 3.0 - recovery,
                parameters.epsilon * (voltage - parameters.unfolding),
            ]
        )
        jacobian = np.array(
            [[1.0 - voltage**2, -1.0], [parameters.epsilon, 0.0]]
        )
        return np.concatenate((field, (jacobian @ fundamental).ravel()))

    integration = solve_ivp(
        augmented_field,
        (0.0, ode_period),
        np.concatenate((ode_state[0], np.eye(2).ravel())),
        dense_output=True,
        rtol=2.0e-11,
        atol=2.0e-13,
        max_step=0.04,
    )
    if not integration.success or integration.sol is None:
        raise RuntimeError("failed to integrate the ODE variational equation")
    audit_times = np.linspace(0.0, ode_period, 1001)
    audit_values = integration.sol(audit_times)
    flows = audit_values[2:].T.reshape(-1, 2, 2)
    monodromy = flows[-1]
    multipliers = np.linalg.eigvals(monodromy)
    tangent_index = int(np.argmin(np.abs(multipliers - 1.0)))
    nontrivial_index = 1 - tangent_index
    forward_norm = max(np.linalg.norm(item, ord=2) for item in flows)
    backward_norm = max(np.linalg.norm(np.linalg.inv(item), ord=2) for item in flows)

    target = orbit.state
    shift_errors = np.asarray(
        [
            np.max(np.linalg.norm(target - np.roll(ode_state, shift, axis=0), axis=1))
            for shift in range(node_count)
        ]
    )
    phase_shift = int(np.argmin(shift_errors))

    tau_0, tau_1 = parameters.physical_delays
    phases = np.arange(node_count, dtype=float) / node_count
    delayed_0 = _evaluate_fourier(
        target[:, 0], phases - tau_0 / orbit.period
    )[:, 0]
    delayed_1 = _evaluate_fourier(
        target[:, 0], phases - tau_1 / orbit.period
    )[:, 0]
    voltage = target[:, 0]
    perturbation_without_epsilon = (
        parameters.kappa_1 * ((delayed_0 + delayed_1) / 2.0 - voltage)
        + parameters.kappa_3
        * (
            ((delayed_0 - 1.0) ** 3 + (delayed_1 - 1.0) ** 3) / 2.0
            - (voltage - 1.0) ** 3
        )
    )
    current_derivative = (
        -parameters.kappa_1
        - 3.0 * parameters.kappa_3 * (voltage - 1.0) ** 2
    )
    delayed_derivative_0 = 0.5 * (
        parameters.kappa_1
        + 3.0 * parameters.kappa_3 * (delayed_0 - 1.0) ** 2
    )
    delayed_derivative_1 = 0.5 * (
        parameters.kappa_1
        + 3.0 * parameters.kappa_3 * (delayed_1 - 1.0) ** 2
    )
    sampled_jacobian_norm = float(
        np.max(
            np.abs(current_derivative)
            + np.abs(delayed_derivative_0)
            + np.abs(delayed_derivative_1)
        )
    )
    sampled_norm = float(np.max(np.abs(perturbation_without_epsilon)))
    return ODEPersistenceRouteCandidate(
        ode_period=float(ode_period),
        ode_monodromy=monodromy,
        ode_floquet_multipliers=np.real_if_close(multipliers, tol=1000).real,
        tangent_multiplier_error=float(abs(multipliers[tangent_index] - 1.0)),
        nontrivial_multiplier_distance_from_one=float(
            abs(multipliers[nontrivial_index] - 1.0)
        ),
        maximum_forward_variational_norm_2=float(forward_norm),
        maximum_backward_variational_norm_2=float(backward_norm),
        target_orbit_c0_distance_after_discrete_phase_alignment=float(
            shift_errors[phase_shift]
        ),
        target_phase_shift_nodes=phase_shift,
        physical_delays=(float(tau_0), float(tau_1)),
        normalized_delay_fractions_at_target=(
            float(tau_0 / orbit.period),
            float(tau_1 / orbit.period),
        ),
        sampled_perturbation_norm=sampled_norm,
        sampled_perturbation_state_jacobian_norm=sampled_jacobian_norm,
        perturbation_amplitude_times_norm=(
            parameters.epsilon * sampled_norm
        ),
        direct_single_delay_theorem_applies=False,
        required_adaptations=(
            "replace one delayed perturbation by a sum of zero-delay and two constant-delay terms",
            "validate the FHN ODE orbit and forward/backward variational flows with Chebyshev radii polynomials",
            "evaluate the six persistence inequalities with outward-rounded parameter-box bounds",
            "differentiate the validated fixed point over the two-gain box to enclose the response matrix",
            "transfer unique extrema using interval first- and second-derivative bounds",
        ),
    )


def convergence_table(
    parameters: FHNPeriodicParameters,
    node_counts: Iterable[int],
) -> tuple[dict[str, float | int | list[list[float]]], ...]:
    """Compute independent resolutions for a spectral convergence audit."""

    rows: list[dict[str, float | int | list[list[float]]]] = []
    for node_count in node_counts:
        orbit = solve_fhn_periodic_orbit(parameters, node_count=int(node_count))
        response = periodic_response_candidate(orbit)
        rows.append(
            {
                "node_count": int(node_count),
                "period": orbit.period,
                "frequency": 1.0 / orbit.period,
                "spectral_tail_l1": orbit.spectral_tail_l1,
                "collocation_residual_inf": orbit.collocation_residual_inf,
                "oversampled_residual_inf": orbit.oversampled_residual_inf,
                "response_matrix": response.response_matrix.tolist(),
                "bordered_smallest_singular_value": (
                    response.bordered.smallest_singular_value
                ),
            }
        )
    return tuple(rows)
