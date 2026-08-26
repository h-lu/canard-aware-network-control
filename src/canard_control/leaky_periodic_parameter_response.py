"""Source-bound leaky periodic parameter-response calculations.

The two validated leaky periodic-orbit artifacts use the control coordinates
``(a, kappa_3)``.  This module computes binary64 bordered first variations,
the frequency--unsquared-voltage-amplitude derivative, refinement and
centered-difference checks, and a sampled common parameter-box candidate.  It
also delegates to the MPFR-directed validator for a smaller continuum box of
orbits, bordered inverses, and simple extrema.

The response matrices, sampled box, and determinant margins remain binary64
diagnostics: the directed calculation does not enclose first sensitivities or
the exact RFDE response Jacobian.  Those distinctions are represented by
explicit claim flags in the tracked artifact.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from decimal import Decimal, InvalidOperation, localcontext
from hashlib import sha256
import json
import math
from pathlib import Path
import platform
from typing import Any, Mapping, Sequence

import gmpy2
import numpy as np
import scipy
from scipy.optimize import brentq

from canard_control.fhn_periodic_candidate import (
    FHNPeriodicParameters,
    PeriodicOrbitCandidate,
    odd_fourier_matrices,
)
from canard_control.leaky_outer_high_resolution import (
    orbit_from_resolution,
    trigonometric_values,
    validate_outer_high_resolution_artifact,
)
from canard_control.leaky_periodic_branch_artifact import (
    MODEL_VALUES,
    _binary64_array,
    _collocation_system,
    binary64_record,
    canonical_sha256,
    validate_leaky_periodic_branch_artifact,
)
from canard_control.leaky_periodic_parameter_box import (
    validate_leaky_parameter_box,
)


SCHEMA_ID = "leaky-periodic-a-kappa3-response-candidate-v1"
SOURCE_RELATIVE_PATH = (
    "src/canard_control/leaky_periodic_parameter_response.py"
)
GENERATOR_RELATIVE_PATH = (
    "experiments/autonomous_leaky_recovery_parameter_response.py"
)
NOTE_RELATIVE_PATH = "docs/leaky-periodic-parameter-response.md"
RESULT_RELATIVE_PATH = (
    "experiments/results/"
    "autonomous_leaky_recovery_parameter_response.json"
)
INNER_PARENT_RELATIVE_PATH = (
    "experiments/results/"
    "autonomous_leaky_recovery_inner_branch_artifact.json"
)
OUTER_PARENT_RELATIVE_PATH = (
    "experiments/results/"
    "autonomous_leaky_recovery_outer_high_resolution.json"
)
DEFAULT_COMMAND = (
    "OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONPATH=src "
    "/usr/bin/python3 "
    "experiments/autonomous_leaky_recovery_parameter_response.py"
)
ARITHMETIC_SCOPE = (
    "binary64 collocation response diagnostics plus 160-bit MPFR-directed "
    "finite/tail and extrema enclosures"
)

SOURCE_MANIFEST = (
    SOURCE_RELATIVE_PATH,
    GENERATOR_RELATIVE_PATH,
    NOTE_RELATIVE_PATH,
    "src/canard_control/leaky_periodic_branch_artifact.py",
    "src/canard_control/leaky_outer_high_resolution.py",
    "src/canard_control/leaky_periodic_validation.py",
    "src/canard_control/leaky_periodic_parameter_box.py",
    "src/canard_control/leaky_periodic_majorant_audit.py",
    "src/canard_control/fhn_periodic_candidate.py",
    "src/canard_control/fhn_periodic_directed_validation.py",
    "src/canard_control/fhn_periodic_infinite_validation.py",
    "src/canard_control/directed_interval.py",
)

CONTROL_ORDER = ("unfolding_a", "kappa_3")
OUTPUT_ORDER = ("frequency", "voltage_amplitude")
COMMON_BOX_HALF_WIDTHS = (1.0e-4, 1.0e-4)
DIRECTED_COMMON_BOX_HALF_WIDTHS = ("1e-10", "1e-10")
SAMPLE_LEVELS = (-1.0, 0.0, 1.0)
FINITE_DIFFERENCE_STEPS = (
    2.0e-4,
    1.0e-4,
    5.0e-5,
    2.5e-5,
    1.25e-5,
)
INNER_REFINEMENT_NODE_COUNTS = (129, 193, 257)
OUTER_RESPONSE_NODE_COUNTS = (257, 385)
EXTREMA_SCAN_FACTOR = 32
NEWTON_RESIDUAL_TOLERANCE = 8.0e-13
NEWTON_MAX_ITERATIONS = 36

PARAMETER_COLUMN_FORMULAS = {
    "unfolding_a": (
        "F_a=(0,T*epsilon*1,0), hence J*x_a=-F_a has slow "
        "right-hand side -T*epsilon*1"
    ),
    "kappa_3": (
        "F_kappa3=(-T*epsilon*C(v),0,0), hence J*x_kappa3=-F_kappa3 "
        "has fast right-hand side T*epsilon*C(v)"
    ),
}
AMPLITUDE_DERIVATIVE_FORMULA = (
    "A_q=v_q(phi_max)-v_q(phi_min) at simple voltage extrema; the "
    "phase-location terms vanish because v_phase=0 there"
)

CLAIM_STATUS = {
    "parent_inner_periodic_rfde_orbit_validated": True,
    "parent_outer_periodic_rfde_orbit_validated": True,
    "a_kappa3_parameter_columns_derived_exactly": True,
    "binary64_center_sensitivities_replayed": True,
    "binary64_forward_adjoint_agreement_checked": True,
    "binary64_resolution_convergence_checked": True,
    "binary64_centered_difference_convergence_checked": True,
    "sampled_common_parameter_box_candidate": True,
    "sampled_simple_voltage_extrema_candidate": True,
    "sampled_nonzero_response_determinant_margin": True,
    "uniform_common_parameter_box_orbits_validated": True,
    "uniform_common_parameter_box_bordered_inverses_validated": True,
    "uniform_simple_extrema_validated": True,
    "exact_rfde_response_derivative_enclosed": False,
    "uniform_frequency_amplitude_local_inverse_validated": False,
}

# Filled after the generated body has been audited.  The manifest is excluded
# from this digest, so registering it does not create a hash cycle.
EXPECTED_ARTIFACT_SHA256: str | None = (
    "c9abbe13fe7e3ed38b6e03d6919a804457bafdb84957eec735f5aab47436aa09"
)


@dataclass(frozen=True)
class LeakyResponseCalculation:
    """One finite bordered sensitivity and output calculation."""

    node_count: int
    collocation_residual_inf: float
    frequency: float
    voltage_amplitude: float
    maximum_phase: float
    minimum_phase: float
    maximum_voltage: float
    minimum_voltage: float
    maximum_curvature: float
    minimum_curvature: float
    extrema_root_count: int
    unique_simple_extrema_candidate: bool
    period_derivatives: np.ndarray
    response_matrix: np.ndarray
    determinant: float
    singular_values: np.ndarray
    forward_adjoint_disagreement_inf: float
    sensitivity_linear_residual_inf: float
    bordered_smallest_singular_value: float
    bordered_condition_number_2: float


def _sha256_path(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _record_value(value: object, name: str) -> float:
    if not isinstance(value, Mapping) or set(value) != {
        "binary64_hex",
        "decimal",
    }:
        raise ValueError(f"{name} is not a complete binary64 record")
    hexadecimal = value.get("binary64_hex")
    decimal = value.get("decimal")
    if not isinstance(hexadecimal, str) or not isinstance(decimal, str):
        raise ValueError(f"{name} binary64 fields must be strings")
    try:
        number = float.fromhex(hexadecimal)
    except ValueError as error:
        raise ValueError(f"{name} has invalid binary64 data") from error
    if (
        not math.isfinite(number)
        or number.hex() != hexadecimal
        or format(number, ".17g") != decimal
    ):
        raise ValueError(f"{name} binary64 fields disagree")
    return number


def _decimal_value(value: object, name: str) -> Decimal:
    """Parse one finite directed endpoint without passing through binary64."""

    if not isinstance(value, str):
        raise ValueError(f"{name} must be a decimal string")
    try:
        number = Decimal(value)
    except InvalidOperation as error:
        raise ValueError(f"{name} is not a decimal number") from error
    if not number.is_finite():
        raise ValueError(f"{name} must be finite")
    return number


def _array_records(array: np.ndarray) -> list[list[dict[str, str]]]:
    values = np.asarray(array, dtype=float)
    if values.ndim != 2:
        raise ValueError("response arrays must be matrices")
    return [
        [binary64_record(float(value)) for value in row] for row in values
    ]


def _vector_records(array: np.ndarray) -> list[dict[str, str]]:
    values = np.asarray(array, dtype=float)
    if values.ndim != 1:
        raise ValueError("response vectors must be one-dimensional")
    return [binary64_record(float(value)) for value in values]


def _matrix_from_records(value: object, name: str) -> np.ndarray:
    if not isinstance(value, list) or not value:
        raise ValueError(f"{name} must be a nonempty matrix")
    rows = []
    for row_index, row in enumerate(value):
        if not isinstance(row, list):
            raise ValueError(f"{name} rows must be lists")
        rows.append(
            [
                _record_value(item, f"{name}[{row_index},{column_index}]")
                for column_index, item in enumerate(row)
            ]
        )
    result = np.asarray(rows, dtype=float)
    if result.ndim != 2 or any(len(row) != result.shape[1] for row in rows):
        raise ValueError(f"{name} has inconsistent rows")
    return result


def _load_parents(
    repository: Path,
) -> tuple[
    tuple[PeriodicOrbitCandidate, np.ndarray],
    dict[int, tuple[PeriodicOrbitCandidate, np.ndarray]],
]:
    inner_payload = json.loads(
        (repository / INNER_PARENT_RELATIVE_PATH).read_text(encoding="utf-8")
    )
    inner = validate_leaky_periodic_branch_artifact(
        inner_payload, repository
    )
    inner_reference = _binary64_array(
        inner_payload["artifact"]["collocation"][
            "phase_reference_binary64"
        ],
        "inner phase reference",
        2,
    )

    outer_payload = json.loads(
        (repository / OUTER_PARENT_RELATIVE_PATH).read_text(encoding="utf-8")
    )
    validate_outer_high_resolution_artifact(outer_payload, repository)
    outer: dict[int, tuple[PeriodicOrbitCandidate, np.ndarray]] = {}
    for count in OUTER_RESPONSE_NODE_COUNTS:
        record = outer_payload["artifact"]["resolutions"][str(count)]
        orbit = orbit_from_resolution(record)
        reference = _binary64_array(
            record["phase_reference_binary64"],
            f"outer {count} phase reference",
            2,
        )
        outer[count] = (orbit, reference)
    return (inner, inner_reference), outer


def _parameter_rhs(
    orbit: PeriodicOrbitCandidate,
) -> tuple[np.ndarray, np.ndarray]:
    """Return exact finite collocation right-hand sides for ``(a,kappa3)``."""

    state = np.asarray(orbit.state, dtype=float)
    count = len(state)
    period = orbit.period
    parameters = orbit.parameters
    voltage = state[:, 0]
    tau_0, tau_1 = parameters.physical_delays
    _, shift_0 = odd_fourier_matrices(count, tau_0 / period)
    _, shift_1 = odd_fourier_matrices(count, tau_1 / period)
    delayed_0 = shift_0 @ voltage
    delayed_1 = shift_1 @ voltage
    cubic = (
        ((delayed_0 - 1.0) ** 3 + (delayed_1 - 1.0) ** 3) / 2.0
        - (voltage - 1.0) ** 3
    )
    rhs = np.zeros((2 * count + 1, 2), dtype=float)
    rhs[count : 2 * count, 0] = -period * parameters.epsilon
    rhs[:count, 1] = period * parameters.epsilon * cubic
    return rhs, cubic


def _extrema(
    voltage: np.ndarray,
) -> tuple[list[float], np.ndarray, np.ndarray]:
    count = len(voltage)
    scan_count = EXTREMA_SCAN_FACTOR * count
    phases = np.arange(scan_count + 1, dtype=float) / scan_count
    tangent_values = trigonometric_values(
        voltage, phases, derivative_order=1
    )

    def tangent(phase: float) -> float:
        return float(
            trigonometric_values(
                voltage, np.asarray([phase]), derivative_order=1
            )[0]
        )

    roots: list[float] = []
    for index in range(scan_count):
        left_value = float(tangent_values[index])
        right_value = float(tangent_values[index + 1])
        if left_value == 0.0:
            root = float(phases[index])
        elif left_value * right_value < 0.0:
            root = float(
                brentq(
                    tangent,
                    float(phases[index]),
                    float(phases[index + 1]),
                    xtol=2.0e-14,
                )
            )
        else:
            continue
        root %= 1.0
        if not roots or min(abs(root - prior) for prior in roots) > 1.0e-9:
            roots.append(root)
    roots.sort()
    if not roots:
        raise RuntimeError("no voltage critical point was found")
    root_array = np.asarray(roots, dtype=float)
    values = trigonometric_values(voltage, root_array)
    curvature = trigonometric_values(
        voltage, root_array, derivative_order=2
    )
    return roots, values, curvature


def _evaluation_row(node_count: int, phase: float) -> np.ndarray:
    modes = np.fft.fftfreq(node_count, d=1.0 / node_count)
    weights = np.exp(2.0j * np.pi * modes * phase)
    rows = np.fft.fft(np.eye(node_count), axis=0)
    return np.real_if_close(weights @ rows / node_count, tol=1000).real


def calculate_response(
    orbit: PeriodicOrbitCandidate,
    phase_reference: np.ndarray,
) -> LeakyResponseCalculation:
    """Compute the finite ``D_(a,kappa3)(F,A)`` by two dual routes."""

    state = np.asarray(orbit.state, dtype=float)
    count = len(state)
    if phase_reference.shape != state.shape:
        raise ValueError("phase reference has the wrong shape")
    residual, jacobian = _collocation_system(
        state, orbit.period, orbit.parameters, phase_reference
    )
    rhs, _ = _parameter_rhs(orbit)
    sensitivities = np.linalg.solve(jacobian, rhs)
    linear_residual = jacobian @ sensitivities - rhs

    roots, values, curvatures = _extrema(state[:, 0])
    maximum_index = int(np.argmax(values))
    minimum_index = int(np.argmin(values))
    maximum_phase = roots[maximum_index]
    minimum_phase = roots[minimum_index]
    maximum_voltage = float(values[maximum_index])
    minimum_voltage = float(values[minimum_index])
    maximum_curvature = float(curvatures[maximum_index])
    minimum_curvature = float(curvatures[minimum_index])
    simple = (
        len(roots) == 2
        and maximum_index != minimum_index
        and maximum_curvature < 0.0
        and minimum_curvature > 0.0
    )

    response = np.empty((2, 2), dtype=float)
    response[0, :] = -sensitivities[-1, :] / orbit.period**2
    for column in range(2):
        voltage_sensitivity = sensitivities[:count, column]
        response[1, column] = float(
            trigonometric_values(
                voltage_sensitivity, np.asarray([maximum_phase])
            )[0]
            - trigonometric_values(
                voltage_sensitivity, np.asarray([minimum_phase])
            )[0]
        )

    gradients = np.zeros((2 * count + 1, 2), dtype=float)
    gradients[-1, 0] = -1.0 / orbit.period**2
    gradients[:count, 1] = _evaluation_row(
        count, maximum_phase
    ) - _evaluation_row(count, minimum_phase)
    adjoints = np.linalg.solve(jacobian.T, gradients)
    adjoint_response = adjoints.T @ rhs

    singular_values = np.linalg.svd(jacobian, compute_uv=False)
    response_singular_values = np.linalg.svd(response, compute_uv=False)
    return LeakyResponseCalculation(
        node_count=count,
        collocation_residual_inf=float(np.max(np.abs(residual))),
        frequency=float(1.0 / orbit.period),
        voltage_amplitude=maximum_voltage - minimum_voltage,
        maximum_phase=maximum_phase,
        minimum_phase=minimum_phase,
        maximum_voltage=maximum_voltage,
        minimum_voltage=minimum_voltage,
        maximum_curvature=maximum_curvature,
        minimum_curvature=minimum_curvature,
        extrema_root_count=len(roots),
        unique_simple_extrema_candidate=bool(simple),
        period_derivatives=np.asarray(sensitivities[-1, :]),
        response_matrix=response,
        determinant=float(np.linalg.det(response)),
        singular_values=response_singular_values,
        forward_adjoint_disagreement_inf=float(
            np.max(np.abs(response - adjoint_response))
        ),
        sensitivity_linear_residual_inf=float(
            np.max(np.abs(linear_residual))
        ),
        bordered_smallest_singular_value=float(singular_values[-1]),
        bordered_condition_number_2=float(
            singular_values[0] / singular_values[-1]
        ),
    )


def _candidate_orbit(
    state: np.ndarray,
    period: float,
    parameters: FHNPeriodicParameters,
    residual: float,
    iterations: int,
    final_step: float,
) -> PeriodicOrbitCandidate:
    count = len(state)
    return PeriodicOrbitCandidate(
        parameters=parameters,
        phase_nodes=np.arange(count, dtype=float) / count,
        state=np.asarray(state, dtype=float),
        period=float(period),
        collocation_residual_inf=float(residual),
        oversampled_residual_inf=float("nan"),
        newton_iterations=int(iterations),
        final_step_inf=float(final_step),
        spectral_tail_l1=float("nan"),
    )


def solve_nearby_orbit(
    center: PeriodicOrbitCandidate,
    phase_reference: np.ndarray,
    *,
    unfolding_a: float,
    kappa_3: float,
) -> PeriodicOrbitCandidate:
    """Newton-solve one nearby finite collocation orbit from the center."""

    parameters = replace(
        center.parameters,
        unfolding=float(unfolding_a),
        kappa_3=float(kappa_3),
    )
    count = len(center.state)
    unknown = np.concatenate(
        (center.state[:, 0], center.state[:, 1], [center.period])
    )
    final_step = float("inf")
    for iteration in range(NEWTON_MAX_ITERATIONS):
        state = np.column_stack(
            (unknown[:count], unknown[count : 2 * count])
        )
        residual, jacobian = _collocation_system(
            state, float(unknown[-1]), parameters, phase_reference
        )
        residual_inf = float(np.max(np.abs(residual)))
        if residual_inf <= NEWTON_RESIDUAL_TOLERANCE:
            return _candidate_orbit(
                state,
                float(unknown[-1]),
                parameters,
                residual_inf,
                iteration,
                final_step,
            )
        step = np.linalg.solve(jacobian, -residual)
        final_step = float(np.max(np.abs(step)))
        accepted = False
        for power in range(30):
            damping = 2.0 ** (-power)
            proposal = unknown + damping * step
            if proposal[-1] <= 0.0:
                continue
            proposal_state = np.column_stack(
                (proposal[:count], proposal[count : 2 * count])
            )
            proposal_residual, _ = _collocation_system(
                proposal_state,
                float(proposal[-1]),
                parameters,
                phase_reference,
            )
            if float(np.max(np.abs(proposal_residual))) < residual_inf:
                unknown = proposal
                final_step *= damping
                accepted = True
                break
        if not accepted:
            raise RuntimeError(
                "nearby leaky periodic Newton line search failed at "
                f"a={unfolding_a:.17g}, kappa_3={kappa_3:.17g}"
            )
    raise RuntimeError(
        "nearby leaky periodic Newton iteration cap reached at "
        f"a={unfolding_a:.17g}, kappa_3={kappa_3:.17g}"
    )


def refine_inner_orbit(
    inner: PeriodicOrbitCandidate,
    inner_reference: np.ndarray,
    node_count: int,
) -> tuple[PeriodicOrbitCandidate, np.ndarray]:
    """Spectrally resample and Newton-correct the smooth inner branch."""

    if node_count < len(inner.state) or node_count % 2 != 1:
        raise ValueError("inner refinement count must be odd and nondecreasing")
    if node_count == len(inner.state):
        return inner, inner_reference
    phases = np.arange(node_count, dtype=float) / node_count
    state = trigonometric_values(inner.state, phases)
    reference = trigonometric_values(inner_reference, phases)
    seed = _candidate_orbit(
        state,
        inner.period,
        inner.parameters,
        float("inf"),
        0,
        float("inf"),
    )
    corrected = solve_nearby_orbit(
        seed,
        reference,
        unfolding_a=inner.parameters.unfolding,
        kappa_3=inner.parameters.kappa_3,
    )
    return corrected, reference


def response_record(
    calculation: LeakyResponseCalculation,
) -> dict[str, object]:
    return {
        "node_count": calculation.node_count,
        "collocation_residual_inf": binary64_record(
            calculation.collocation_residual_inf
        ),
        "outputs": {
            "frequency": binary64_record(calculation.frequency),
            "voltage_amplitude": binary64_record(
                calculation.voltage_amplitude
            ),
        },
        "extrema": {
            "maximum_phase": binary64_record(calculation.maximum_phase),
            "minimum_phase": binary64_record(calculation.minimum_phase),
            "maximum_voltage": binary64_record(
                calculation.maximum_voltage
            ),
            "minimum_voltage": binary64_record(
                calculation.minimum_voltage
            ),
            "maximum_curvature": binary64_record(
                calculation.maximum_curvature
            ),
            "minimum_curvature": binary64_record(
                calculation.minimum_curvature
            ),
            "root_count": calculation.extrema_root_count,
            "unique_simple_extrema_candidate": (
                calculation.unique_simple_extrema_candidate
            ),
        },
        "period_derivatives": _vector_records(
            calculation.period_derivatives
        ),
        "response_matrix": _array_records(calculation.response_matrix),
        "determinant": binary64_record(calculation.determinant),
        "singular_values": _vector_records(calculation.singular_values),
        "forward_adjoint_disagreement_inf": binary64_record(
            calculation.forward_adjoint_disagreement_inf
        ),
        "sensitivity_linear_residual_inf": binary64_record(
            calculation.sensitivity_linear_residual_inf
        ),
        "bordered_smallest_singular_value": binary64_record(
            calculation.bordered_smallest_singular_value
        ),
        "bordered_condition_number_2": binary64_record(
            calculation.bordered_condition_number_2
        ),
    }


def _output_vector(calculation: LeakyResponseCalculation) -> np.ndarray:
    return np.asarray(
        [calculation.frequency, calculation.voltage_amplitude], dtype=float
    )


def _finite_difference_ladder(
    center: PeriodicOrbitCandidate,
    phase_reference: np.ndarray,
    center_response: LeakyResponseCalculation,
) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for step in FINITE_DIFFERENCE_STEPS:
        columns: list[np.ndarray] = []
        maximum_residual = 0.0
        for control_index in range(2):
            outputs: list[np.ndarray] = []
            for sign in (-1.0, 1.0):
                unfolding = center.parameters.unfolding
                kappa_3 = center.parameters.kappa_3
                if control_index == 0:
                    unfolding += sign * step
                else:
                    kappa_3 += sign * step
                orbit = solve_nearby_orbit(
                    center,
                    phase_reference,
                    unfolding_a=unfolding,
                    kappa_3=kappa_3,
                )
                response = calculate_response(orbit, phase_reference)
                outputs.append(_output_vector(response))
                maximum_residual = max(
                    maximum_residual, response.collocation_residual_inf
                )
            columns.append((outputs[1] - outputs[0]) / (2.0 * step))
        matrix = np.column_stack(columns)
        records.append(
            {
                "step": binary64_record(step),
                "centered_difference_matrix": _array_records(matrix),
                "matrix_disagreement_inf": binary64_record(
                    float(
                        np.max(
                            np.abs(matrix - center_response.response_matrix)
                        )
                    )
                ),
                "determinant": binary64_record(float(np.linalg.det(matrix))),
                "maximum_collocation_residual_inf": binary64_record(
                    maximum_residual
                ),
            }
        )
    return records


def _sample_box(
    center: PeriodicOrbitCandidate,
    phase_reference: np.ndarray,
) -> dict[str, object]:
    samples: list[dict[str, object]] = []
    determinants: list[float] = []
    maximum_residual = 0.0
    all_simple = True
    for level_a in SAMPLE_LEVELS:
        for level_kappa_3 in SAMPLE_LEVELS:
            unfolding = (
                center.parameters.unfolding
                + level_a * COMMON_BOX_HALF_WIDTHS[0]
            )
            kappa_3 = (
                center.parameters.kappa_3
                + level_kappa_3 * COMMON_BOX_HALF_WIDTHS[1]
            )
            orbit = solve_nearby_orbit(
                center,
                phase_reference,
                unfolding_a=unfolding,
                kappa_3=kappa_3,
            )
            response = calculate_response(orbit, phase_reference)
            determinants.append(response.determinant)
            maximum_residual = max(
                maximum_residual, response.collocation_residual_inf
            )
            all_simple = (
                all_simple and response.unique_simple_extrema_candidate
            )
            samples.append(
                {
                    "levels": [level_a, level_kappa_3],
                    "parameters": {
                        "unfolding_a": binary64_record(unfolding),
                        "kappa_3": binary64_record(kappa_3),
                    },
                    "response": response_record(response),
                }
            )
    signs = {int(np.sign(value)) for value in determinants}
    return {
        "samples": samples,
        "maximum_collocation_residual_inf": binary64_record(
            maximum_residual
        ),
        "all_sampled_extrema_simple": bool(all_simple),
        "all_sampled_determinants_same_nonzero_sign": len(signs) == 1
        and 0 not in signs,
        "determinant_sign": next(iter(signs)) if len(signs) == 1 else 0,
        "minimum_sampled_absolute_determinant": binary64_record(
            min(abs(value) for value in determinants)
        ),
        "minimum_sampled_determinant": binary64_record(min(determinants)),
        "maximum_sampled_determinant": binary64_record(max(determinants)),
    }


def _resolution_summary(
    records: Sequence[dict[str, object]],
) -> dict[str, object]:
    matrices = [
        _matrix_from_records(item["response_matrix"], "response matrix")
        for item in records
    ]
    determinants = [
        _record_value(item["determinant"], "response determinant")
        for item in records
    ]
    primary = matrices[0]
    return {
        "maximum_response_entry_span": binary64_record(
            max(
                float(np.max(np.abs(matrix - primary)))
                for matrix in matrices[1:]
            )
            if len(matrices) > 1
            else 0.0
        ),
        "determinant_span": binary64_record(
            max(determinants) - min(determinants)
        ),
        "all_determinants_same_nonzero_sign": len(
            {int(np.sign(value)) for value in determinants}
        )
        == 1
        and all(value != 0.0 for value in determinants),
    }


def _branch_artifact(
    branch: str,
    center: PeriodicOrbitCandidate,
    phase_reference: np.ndarray,
    resolution_orbits: Sequence[
        tuple[str, PeriodicOrbitCandidate, np.ndarray]
    ],
) -> dict[str, object]:
    response_records = []
    for source, orbit, reference in resolution_orbits:
        record = response_record(calculate_response(orbit, reference))
        record["source"] = source
        response_records.append(record)
    center_response = calculate_response(center, phase_reference)
    finite_differences = _finite_difference_ladder(
        center, phase_reference, center_response
    )
    sampled = _sample_box(center, phase_reference)
    resolution = _resolution_summary(response_records)
    finest_fd_determinant = _record_value(
        finite_differences[-1]["determinant"],
        "finest centered difference determinant",
    )
    center_determinant = center_response.determinant
    resolution_span = _record_value(
        resolution["determinant_span"], "determinant resolution span"
    )
    sampled_margin = _record_value(
        sampled["minimum_sampled_absolute_determinant"],
        "sampled determinant margin",
    )
    # This padding is deliberately diagnostic: it combines observed
    # discretization and centered-difference discrepancies but is not an
    # interval truncation bound for the continuum parameter box.
    diagnostic_padding = resolution_span + abs(
        finest_fd_determinant - center_determinant
    )
    return {
        "branch": branch,
        "center_node_count": len(center.state),
        "center_response": response_record(center_response),
        "resolution_replay": response_records,
        "resolution_summary": resolution,
        "centered_difference_ladder": finite_differences,
        "sampled_box": sampled,
        "numerical_nonzero_margin": {
            "minimum_sampled_absolute_determinant": binary64_record(
                sampled_margin
            ),
            "diagnostic_discrepancy_padding": binary64_record(
                diagnostic_padding
            ),
            "padded_margin": binary64_record(
                sampled_margin - diagnostic_padding
            ),
            "strictly_positive": sampled_margin > diagnostic_padding,
            "rigorous_interval_margin": False,
        },
    }


def build_artifact(repository: Path) -> dict[str, object]:
    """Build the complete binary64 response and sampled-box body."""

    (inner, inner_reference), outer = _load_parents(repository)
    inner_resolutions: list[
        tuple[str, PeriodicOrbitCandidate, np.ndarray]
    ] = []
    for count in INNER_REFINEMENT_NODE_COUNTS:
        orbit, reference = refine_inner_orbit(
            inner, inner_reference, count
        )
        inner_resolutions.append(
            (
                "parent" if count == 129 else "spectral_refinement",
                orbit,
                reference,
            )
        )
    outer_resolutions = [
        (
            "parent_primary" if count == 257 else "parent_reference",
            *outer[count],
        )
        for count in OUTER_RESPONSE_NODE_COUNTS
    ]
    directed_boxes = {
        "inner_saddle_candidate": validate_leaky_parameter_box(
            inner,
            branch="inner_saddle_candidate",
            half_width_unfolding_a=DIRECTED_COMMON_BOX_HALF_WIDTHS[0],
            half_width_kappa_3=DIRECTED_COMMON_BOX_HALF_WIDTHS[1],
            cutoff=192,
            precision=160,
            maximum_radius="1e-5",
            chosen_radius="1e-5",
            phase_partition_count=4096,
        ),
        "outer_pulse": validate_leaky_parameter_box(
            outer[257][0],
            branch="outer_pulse",
            half_width_unfolding_a=DIRECTED_COMMON_BOX_HALF_WIDTHS[0],
            half_width_kappa_3=DIRECTED_COMMON_BOX_HALF_WIDTHS[1],
            cutoff=384,
            precision=160,
            maximum_radius="1e-5",
            chosen_radius="1e-5",
            phase_partition_count=4096,
        ),
    }
    from dataclasses import asdict

    for name, certificate in directed_boxes.items():
        if not certificate.uniform_orbit_and_bordered_inverse_validated:
            raise ArithmeticError(f"{name} directed parameter box did not close")
        if not certificate.uniform_simple_extrema_validated:
            raise ArithmeticError(f"{name} directed extrema did not close")
    branches = {
        "inner_saddle_candidate": _branch_artifact(
            "inner_saddle_candidate",
            inner,
            inner_reference,
            inner_resolutions,
        ),
        "outer_pulse": _branch_artifact(
            "outer_pulse",
            outer[257][0],
            outer[257][1],
            outer_resolutions,
        ),
    }
    all_positive = all(
        branch["numerical_nonzero_margin"]["strictly_positive"]
        for branch in branches.values()
    )
    artifact = {
        "schema_id": SCHEMA_ID,
        "model": {
            "epsilon": binary64_record(float(MODEL_VALUES["epsilon"])),
            "unfolding_a": binary64_record(
                float(MODEL_VALUES["unfolding_a"])
            ),
            "kappa_1": binary64_record(float(MODEL_VALUES["kappa_1"])),
            "kappa_3": binary64_record(float(MODEL_VALUES["kappa_3"])),
            "theta_0": binary64_record(float(MODEL_VALUES["theta_0"])),
            "theta_1": binary64_record(float(MODEL_VALUES["theta_1"])),
            "recovery_leak_b": binary64_record(1.0),
        },
        "control_order": list(CONTROL_ORDER),
        "output_order": list(OUTPUT_ORDER),
        "parameter_column_formulas": dict(PARAMETER_COLUMN_FORMULAS),
        "amplitude_derivative_formula": AMPLITUDE_DERIVATIVE_FORMULA,
        "common_sampled_box": {
            "half_width_unfolding_a": binary64_record(
                COMMON_BOX_HALF_WIDTHS[0]
            ),
            "half_width_kappa_3": binary64_record(
                COMMON_BOX_HALF_WIDTHS[1]
            ),
            "sample_levels": list(SAMPLE_LEVELS),
            "continuum_between_samples_enclosed": False,
        },
        "directed_common_box": {
            "half_width_unfolding_a": DIRECTED_COMMON_BOX_HALF_WIDTHS[0],
            "half_width_kappa_3": DIRECTED_COMMON_BOX_HALF_WIDTHS[1],
            "branches": {
                name: asdict(certificate)
                for name, certificate in directed_boxes.items()
            },
            "uniform_orbit_and_bordered_inverse_validated": True,
            "uniform_simple_extrema_validated": True,
            "exact_first_sensitivities_validated": False,
            "exact_response_determinant_or_inverse_validated": False,
        },
        "finite_difference_steps": [
            binary64_record(value) for value in FINITE_DIFFERENCE_STEPS
        ],
        "branches": branches,
        "joint_diagnostics": {
            "both_branches_have_positive_padded_numerical_margin": (
                all_positive
            ),
            "determinant_orientations_are_opposite": (
                branches["inner_saddle_candidate"]["sampled_box"][
                    "determinant_sign"
                ]
                * branches["outer_pulse"]["sampled_box"][
                    "determinant_sign"
                ]
                == -1
            ),
            "the_1e_minus_4_box_is_only_sampled": True,
            "the_1e_minus_10_box_has_uniform_orbit_and_extrema_proofs": True,
        },
        "claim_status": dict(CLAIM_STATUS),
    }
    return artifact


def manifest_for_artifact(
    artifact: Mapping[str, Any], repository: Path
) -> dict[str, object]:
    return {
        "schema_id": SCHEMA_ID,
        "result": RESULT_RELATIVE_PATH,
        "default_command": DEFAULT_COMMAND,
        "arithmetic_scope": ARITHMETIC_SCOPE,
        "artifact_sha256": canonical_sha256(artifact),
        "parent_result_sha256": {
            "inner": _sha256_path(repository / INNER_PARENT_RELATIVE_PATH),
            "outer": _sha256_path(repository / OUTER_PARENT_RELATIVE_PATH),
        },
        "source_sha256": {
            relative: _sha256_path(repository / relative)
            for relative in SOURCE_MANIFEST
        },
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "gmpy2": gmpy2.__version__,
        },
    }


def _compare_response_record(
    stored: Mapping[str, Any],
    recomputed: LeakyResponseCalculation,
) -> None:
    matrix = _matrix_from_records(stored.get("response_matrix"), "response")
    if matrix.shape != (2, 2) or not np.allclose(
        matrix,
        recomputed.response_matrix,
        rtol=0.0,
        atol=1.0e-10,
    ):
        raise ValueError("center response matrix replay changed")
    scalar_fields = {
        "collocation_residual_inf": recomputed.collocation_residual_inf,
        "determinant": recomputed.determinant,
        "forward_adjoint_disagreement_inf": (
            recomputed.forward_adjoint_disagreement_inf
        ),
        "sensitivity_linear_residual_inf": (
            recomputed.sensitivity_linear_residual_inf
        ),
        "bordered_smallest_singular_value": (
            recomputed.bordered_smallest_singular_value
        ),
        "bordered_condition_number_2": recomputed.bordered_condition_number_2,
    }
    replay_tolerances = {
        "collocation_residual_inf": 1.0e-12,
        "determinant": 1.0e-10,
        "forward_adjoint_disagreement_inf": 1.0e-9,
        "sensitivity_linear_residual_inf": 2.0e-9,
        "bordered_smallest_singular_value": 1.0e-10,
        "bordered_condition_number_2": 1.0e-5,
    }
    for name, expected in scalar_fields.items():
        stored_value = _record_value(stored.get(name), name)
        tolerance = replay_tolerances[name]
        if not math.isclose(
            stored_value, expected, rel_tol=0.0, abs_tol=tolerance
        ):
            raise ValueError(f"center response replay changed for {name}")


def _validate_directed_box_semantics(directed: Mapping[str, Any]) -> None:
    """Recheck the strict inequalities encoded by the directed box body.

    The source-registered body digest prevents silent replacement of the
    stored endpoints.  These checks are deliberately independent of that
    digest: they ensure that the truth-valued gates still follow from the
    decimal endpoints and that the two extrema windows are disjoint.
    """

    expected_keys = {
        "half_width_unfolding_a",
        "half_width_kappa_3",
        "branches",
        "uniform_orbit_and_bordered_inverse_validated",
        "uniform_simple_extrema_validated",
        "exact_first_sensitivities_validated",
        "exact_response_determinant_or_inverse_validated",
    }
    if set(directed) != expected_keys:
        raise ValueError("directed common-box schema changed")
    if (
        directed.get("half_width_unfolding_a")
        != DIRECTED_COMMON_BOX_HALF_WIDTHS[0]
        or directed.get("half_width_kappa_3")
        != DIRECTED_COMMON_BOX_HALF_WIDTHS[1]
    ):
        raise ValueError("directed common-box half-width changed")
    branches = directed.get("branches")
    expected_branches = {"inner_saddle_candidate", "outer_pulse"}
    if not isinstance(branches, Mapping) or set(branches) != expected_branches:
        raise ValueError("directed common-box branch set changed")

    continuation_keys = {
        "branch",
        "half_width_unfolding_a",
        "half_width_kappa_3",
        "unfolding_a_lower",
        "unfolding_a_upper",
        "kappa_3_lower",
        "kappa_3_upper",
        "cutoff",
        "precision_bits",
        "real_conjugate_dimension",
        "approximate_inverse_l1_upper",
        "analytic_tail_inverse_l1_upper",
        "global_preconditioner_l1_upper",
        "finite_inverse_defect_upper",
        "tail_from_finite_upper",
        "finite_from_tail_upper",
        "tail_to_tail_upper",
        "full_point_defect_upper",
        "preconditioned_box_residual_upper",
        "coefficient_z1_upper",
        "coefficient_z2_upper",
        "coefficient_z3_upper",
        "chosen_radius",
        "derivative_variation_upper",
        "uniform_contraction_upper",
        "radii_left_upper",
        "radii_margin_lower",
        "uniform_bordered_inverse_norm_upper",
        "parameter_box_orbit_validated",
        "parameter_box_bordered_inverse_validated",
    }
    extrema_keys = {
        "phase_partition_count",
        "maximum_phase_lower",
        "maximum_phase_upper",
        "minimum_phase_lower",
        "minimum_phase_upper",
        "maximum_curvature_window_lower",
        "maximum_curvature_window_upper",
        "minimum_curvature_window_lower",
        "minimum_curvature_window_upper",
        "maximum_curvature_upper",
        "minimum_curvature_lower",
        "complement_derivative_gap_lower",
        "derivative_error_upper",
        "all_complement_cells_strict",
        "extrema_validated",
        "failure_reason",
    }
    certificate_keys = {
        "continuation",
        "extrema",
        "uniform_orbit_and_bordered_inverse_validated",
        "uniform_simple_extrema_validated",
        "exact_response_derivative_enclosed",
        "frequency_amplitude_local_inverse_validated",
        "remaining_gates",
    }
    expected_cutoffs = {
        "inner_saddle_candidate": 192,
        "outer_pulse": 384,
    }
    center_a = Decimal("0.25")
    center_kappa_3 = Decimal("0.005")
    half_width = Decimal("1e-10")
    branch_gates: list[tuple[bool, bool]] = []
    for name in sorted(expected_branches):
        certificate = branches[name]
        if not isinstance(certificate, Mapping) or set(certificate) != certificate_keys:
            raise ValueError(f"directed certificate schema changed for {name}")
        continuation = certificate.get("continuation")
        extrema = certificate.get("extrema")
        if (
            not isinstance(continuation, Mapping)
            or set(continuation) != continuation_keys
        ):
            raise ValueError(f"directed continuation schema changed for {name}")
        if not isinstance(extrema, Mapping) or set(extrema) != extrema_keys:
            raise ValueError(f"directed extrema schema changed for {name}")
        if continuation.get("branch") != name:
            raise ValueError(f"directed continuation branch changed for {name}")
        if (
            continuation.get("half_width_unfolding_a") != "1e-10"
            or continuation.get("half_width_kappa_3") != "1e-10"
            or continuation.get("cutoff") != expected_cutoffs[name]
            or continuation.get("precision_bits") != 160
        ):
            raise ValueError(f"directed continuation settings changed for {name}")

        a_lower = _decimal_value(
            continuation.get("unfolding_a_lower"), f"{name} a lower"
        )
        a_upper = _decimal_value(
            continuation.get("unfolding_a_upper"), f"{name} a upper"
        )
        k3_lower = _decimal_value(
            continuation.get("kappa_3_lower"), f"{name} kappa3 lower"
        )
        k3_upper = _decimal_value(
            continuation.get("kappa_3_upper"), f"{name} kappa3 upper"
        )
        if not (
            a_lower <= center_a - half_width
            and a_upper >= center_a + half_width
            and k3_lower <= center_kappa_3 - half_width
            and k3_upper >= center_kappa_3 + half_width
        ):
            raise ValueError(
                f"directed parameter interval does not cover the box for {name}"
            )

        y_bound = _decimal_value(
            continuation.get("preconditioned_box_residual_upper"),
            f"{name} residual",
        )
        defect = _decimal_value(
            continuation.get("full_point_defect_upper"), f"{name} defect"
        )
        variation = _decimal_value(
            continuation.get("derivative_variation_upper"),
            f"{name} derivative variation",
        )
        contraction = _decimal_value(
            continuation.get("uniform_contraction_upper"),
            f"{name} contraction",
        )
        radius = _decimal_value(
            continuation.get("chosen_radius"), f"{name} radius"
        )
        radii_left = _decimal_value(
            continuation.get("radii_left_upper"), f"{name} radii left"
        )
        margin = _decimal_value(
            continuation.get("radii_margin_lower"), f"{name} radii margin"
        )
        preconditioner = _decimal_value(
            continuation.get("global_preconditioner_l1_upper"),
            f"{name} preconditioner",
        )
        inverse_norm = _decimal_value(
            continuation.get("uniform_bordered_inverse_norm_upper"),
            f"{name} inverse norm",
        )
        if min(y_bound, defect, variation, contraction, radius) < 0:
            raise ValueError(f"directed radii data became negative for {name}")
        with localcontext() as context:
            context.prec = 120
            if contraction < defect + variation:
                raise ValueError(
                    f"directed contraction underbounds its terms for {name}"
                )
            if radii_left < y_bound + contraction * radius:
                raise ValueError(
                    f"directed radii left side underbounds its terms for {name}"
                )
            if margin > radius - radii_left:
                raise ValueError(f"directed radii margin is not downward for {name}")
            # The separately rounded decimal upper endpoints need not
            # preserve the equality A/(1-q) at their final printed digit.
            # Positivity and strict enlargement are robust semantic checks;
            # the directed source calculation supplies the sharp quotient.
            if inverse_norm < preconditioner:
                raise ValueError(
                    "directed inverse norm did not enlarge the "
                    f"preconditioner for {name}"
                )
        orbit_gate = (
            continuation.get("parameter_box_orbit_validated") is True
            and continuation.get("parameter_box_bordered_inverse_validated") is True
            and contraction < 1
            and margin > 0
        )
        if (
            certificate.get("uniform_orbit_and_bordered_inverse_validated")
            is not orbit_gate
        ):
            raise ValueError(
                f"directed orbit gate disagrees with inequalities for {name}"
            )

        if extrema.get("phase_partition_count") != 4096:
            raise ValueError(f"directed extrema partition changed for {name}")
        maximum = (
            _decimal_value(extrema.get("maximum_phase_lower"), f"{name} max lower"),
            _decimal_value(extrema.get("maximum_phase_upper"), f"{name} max upper"),
        )
        minimum = (
            _decimal_value(extrema.get("minimum_phase_lower"), f"{name} min lower"),
            _decimal_value(extrema.get("minimum_phase_upper"), f"{name} min upper"),
        )
        if not (
            Decimal(0) <= maximum[0] < maximum[1] <= Decimal(1)
            and Decimal(0) <= minimum[0] < minimum[1] <= Decimal(1)
            and (maximum[1] < minimum[0] or minimum[1] < maximum[0])
        ):
            raise ValueError(
                "directed extrema windows overlap or leave the phase domain "
                f"for {name}"
            )
        if (
            extrema.get("maximum_curvature_window_lower")
            != extrema.get("maximum_phase_lower")
            or extrema.get("maximum_curvature_window_upper")
            != extrema.get("maximum_phase_upper")
            or extrema.get("minimum_curvature_window_lower")
            != extrema.get("minimum_phase_lower")
            or extrema.get("minimum_curvature_window_upper")
            != extrema.get("minimum_phase_upper")
        ):
            raise ValueError(f"directed curvature window changed for {name}")
        maximum_curvature = _decimal_value(
            extrema.get("maximum_curvature_upper"), f"{name} max curvature"
        )
        minimum_curvature = _decimal_value(
            extrema.get("minimum_curvature_lower"), f"{name} min curvature"
        )
        complement_gap = _decimal_value(
            extrema.get("complement_derivative_gap_lower"),
            f"{name} complement gap",
        )
        derivative_error = _decimal_value(
            extrema.get("derivative_error_upper"), f"{name} derivative error"
        )
        extrema_gate = (
            extrema.get("all_complement_cells_strict") is True
            and extrema.get("extrema_validated") is True
            and extrema.get("failure_reason") is None
            and maximum_curvature < 0
            and minimum_curvature > 0
            and complement_gap > 0
            and derivative_error >= 0
        )
        if certificate.get("uniform_simple_extrema_validated") is not extrema_gate:
            raise ValueError(
                f"directed extrema gate disagrees with inequalities for {name}"
            )
        if certificate.get("exact_response_derivative_enclosed") is not False:
            raise ValueError(f"exact response derivative was overpromoted for {name}")
        if certificate.get("frequency_amplitude_local_inverse_validated") is not False:
            raise ValueError(f"local response inverse was overpromoted for {name}")
        branch_gates.append((orbit_gate, extrema_gate))

    if directed.get("uniform_orbit_and_bordered_inverse_validated") is not all(
        item[0] for item in branch_gates
    ):
        raise ValueError("joint directed orbit gate disagrees with branch gates")
    if directed.get("uniform_simple_extrema_validated") is not all(
        item[1] for item in branch_gates
    ):
        raise ValueError("joint directed extrema gate disagrees with branch gates")
    if directed.get("exact_first_sensitivities_validated") is not False:
        raise ValueError("directed first sensitivities were overpromoted")
    if directed.get("exact_response_determinant_or_inverse_validated") is not False:
        raise ValueError("directed response determinant was overpromoted")


def validate_parameter_response_artifact(
    payload: Mapping[str, Any], repository: Path, *, replay_centers: bool = True
) -> None:
    """Validate source binding, claim boundaries, and center replays."""

    if not isinstance(payload, Mapping) or set(payload) != {
        "artifact",
        "manifest",
    }:
        raise ValueError("response result must contain artifact and manifest")
    artifact = payload.get("artifact")
    manifest = payload.get("manifest")
    if not isinstance(artifact, Mapping) or not isinstance(manifest, Mapping):
        raise ValueError("response artifact and manifest must be mappings")
    expected_artifact_keys = {
        "schema_id",
        "model",
        "control_order",
        "output_order",
        "parameter_column_formulas",
        "amplitude_derivative_formula",
        "common_sampled_box",
        "directed_common_box",
        "finite_difference_steps",
        "branches",
        "joint_diagnostics",
        "claim_status",
    }
    if set(artifact) != expected_artifact_keys:
        raise ValueError("response artifact schema changed")
    if artifact.get("schema_id") != SCHEMA_ID:
        raise ValueError("response schema changed")
    if artifact.get("control_order") != list(CONTROL_ORDER):
        raise ValueError("response control order changed")
    if artifact.get("output_order") != list(OUTPUT_ORDER):
        raise ValueError("response output order changed")
    if artifact.get("parameter_column_formulas") != PARAMETER_COLUMN_FORMULAS:
        raise ValueError("parameter-column formulas changed")
    if artifact.get("claim_status") != CLAIM_STATUS:
        raise ValueError("response claim ledger changed")
    expected_digest = EXPECTED_ARTIFACT_SHA256
    if not isinstance(expected_digest, str) or len(expected_digest) != 64:
        raise ValueError("response artifact body is not source registered")
    if canonical_sha256(artifact) != expected_digest:
        raise ValueError("response artifact body changed")
    expected_manifest_keys = {
        "schema_id",
        "result",
        "default_command",
        "arithmetic_scope",
        "artifact_sha256",
        "parent_result_sha256",
        "source_sha256",
        "environment",
    }
    if set(manifest) != expected_manifest_keys:
        raise ValueError("response manifest schema changed")
    if manifest.get("schema_id") != SCHEMA_ID:
        raise ValueError("response manifest schema changed")
    if manifest.get("result") != RESULT_RELATIVE_PATH:
        raise ValueError("response manifest result changed")
    if manifest.get("default_command") != DEFAULT_COMMAND:
        raise ValueError("response manifest command changed")
    if manifest.get("arithmetic_scope") != ARITHMETIC_SCOPE:
        raise ValueError("response manifest arithmetic scope changed")
    if manifest.get("artifact_sha256") != expected_digest:
        raise ValueError("response manifest body digest changed")
    parent_hashes = manifest.get("parent_result_sha256")
    if not isinstance(parent_hashes, Mapping) or set(parent_hashes) != {
        "inner",
        "outer",
    }:
        raise ValueError("response parent manifest changed")
    expected_parent_paths = {
        "inner": INNER_PARENT_RELATIVE_PATH,
        "outer": OUTER_PARENT_RELATIVE_PATH,
    }
    for name, relative in expected_parent_paths.items():
        if parent_hashes.get(name) != _sha256_path(repository / relative):
            raise ValueError(f"response parent hash changed for {name}")
    source_hashes = manifest.get("source_sha256")
    if not isinstance(source_hashes, Mapping) or set(source_hashes) != set(
        SOURCE_MANIFEST
    ):
        raise ValueError("response source manifest changed")
    for relative in SOURCE_MANIFEST:
        if source_hashes.get(relative) != _sha256_path(repository / relative):
            raise ValueError(f"response source hash changed for {relative}")
    environment = manifest.get("environment")
    expected_environment = {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "gmpy2": gmpy2.__version__,
    }
    if environment != expected_environment:
        raise ValueError("response replay environment changed")

    branches = artifact.get("branches")
    if not isinstance(branches, Mapping) or set(branches) != {
        "inner_saddle_candidate",
        "outer_pulse",
    }:
        raise ValueError("response branch set changed")
    for name, branch in branches.items():
        if not isinstance(branch, Mapping) or branch.get("branch") != name:
            raise ValueError("response branch record changed")
        sampled = branch.get("sampled_box")
        margin = branch.get("numerical_nonzero_margin")
        if not isinstance(sampled, Mapping) or not isinstance(margin, Mapping):
            raise ValueError("response sampled evidence is missing")
        if sampled.get("all_sampled_extrema_simple") is not True:
            raise ValueError("a sampled branch lost simple extrema")
        if sampled.get("all_sampled_determinants_same_nonzero_sign") is not True:
            raise ValueError("a sampled determinant lost its orientation")
        if margin.get("strictly_positive") is not True:
            raise ValueError("a numerical determinant margin is not positive")
        if margin.get("rigorous_interval_margin") is not False:
            raise ValueError("a numerical determinant margin was overpromoted")

    directed = artifact.get("directed_common_box")
    if not isinstance(directed, Mapping):
        raise ValueError("directed common parameter box is missing")
    _validate_directed_box_semantics(directed)

    if replay_centers:
        (inner, inner_reference), outer = _load_parents(repository)
        inner_radius = _decimal_value(
            directed["branches"]["inner_saddle_candidate"]["continuation"][
                "chosen_radius"
            ],
            "inner correction radius",
        )
        outer_radius = _decimal_value(
            directed["branches"]["outer_pulse"]["continuation"][
                "chosen_radius"
            ],
            "outer correction radius",
        )
        if Decimal(str(abs(inner.period - outer[257][0].period))) <= (
            inner_radius + outer_radius
        ):
            raise ValueError("inner and outer validated orbit balls overlap in period")
        _compare_response_record(
            branches["inner_saddle_candidate"]["center_response"],
            calculate_response(inner, inner_reference),
        )
        _compare_response_record(
            branches["outer_pulse"]["center_response"],
            calculate_response(outer[257][0], outer[257][1]),
        )


__all__ = [
    "ARITHMETIC_SCOPE",
    "CLAIM_STATUS",
    "COMMON_BOX_HALF_WIDTHS",
    "CONTROL_ORDER",
    "EXPECTED_ARTIFACT_SHA256",
    "OUTPUT_ORDER",
    "RESULT_RELATIVE_PATH",
    "SOURCE_MANIFEST",
    "build_artifact",
    "calculate_response",
    "manifest_for_artifact",
    "solve_nearby_orbit",
    "validate_parameter_response_artifact",
]
