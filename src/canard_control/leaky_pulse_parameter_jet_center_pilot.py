"""Source-bound Stage-5A center-parameter jet feasibility pilot.

The five factorial-correlated coefficient functions are integrated together
at ``J0=2409/8000`` by a binary64 DOP853 method of steps.  Three solver
refinements are sampled on one two-origin mesh and their pointwise hull is
recorded as an *observed mesh envelope*.  This is deliberately not directed
arithmetic and is not an order-five remainder, event, stable-gap, onset, or
routing certificate.
"""

from __future__ import annotations

from bisect import bisect_left
from dataclasses import dataclass
from fractions import Fraction
from hashlib import sha256
import json
import math
from pathlib import Path
import platform
from typing import Any, Mapping, Sequence

import numpy as np
import scipy
from scipy.integrate import solve_ivp

from canard_control.autonomous_leaky_recovery_bistable import (
    EPSILON as EPSILON_EXACT,
    KAPPA_1 as KAPPA_1_EXACT,
    KAPPA_3 as KAPPA_3_EXACT,
    UNFOLDING as UNFOLDING_EXACT,
)


SCHEMA_ID = "leaky-pulse-parameter-jet-center-pilot-v1"
MODEL_ID = "autonomous-leaky-recovery-physical-pulse"

SOURCE_RELATIVE_PATH = (
    "src/canard_control/leaky_pulse_parameter_jet_center_pilot.py"
)
GENERATOR_RELATIVE_PATH = (
    "experiments/leaky_pulse_parameter_jet_center_pilot.py"
)
RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_pulse_parameter_jet_center_pilot.json"
)
NOTE_RELATIVE_PATH = "docs/leaky-pulse-parameter-jet-center-pilot.md"
TEST_RELATIVE_PATH = (
    "tests/test_leaky_pulse_parameter_jet_center_pilot.py"
)
STAGE5_CONTRACT_RELATIVE_PATH = (
    "experiments/results/leaky_pulse_event_aligned_parameter_jet_contract.json"
)
STAGE5_CONTRACT_SHA256 = (
    "12993314508d7b31de1ef7e5988b9dbd0798347eee73309d381774faa0d21646"
)
FAMILY_PARENT_RELATIVE_PATH = (
    "experiments/results/leaky_pulse_inner_route_c_family_contract.json"
)
FAMILY_PARENT_SHA256 = (
    "6821551f3fab7d4bbc073af20b83daf055482055a81db23664d31c017de81f7c"
)
MODEL_SOURCE_RELATIVE_PATH = (
    "src/canard_control/autonomous_leaky_recovery_bistable.py"
)
SOURCE_MANIFEST = (
    SOURCE_RELATIVE_PATH,
    GENERATOR_RELATIVE_PATH,
    NOTE_RELATIVE_PATH,
)
DEPENDENCY_SOURCE_MANIFEST = (MODEL_SOURCE_RELATIVE_PATH,)
DEFAULT_COMMAND = (
    "OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 "
    "PYTHONPATH=.venv/lib/python3.14/site-packages:src /usr/bin/python3 "
    "experiments/leaky_pulse_parameter_jet_center_pilot.py"
)
ARITHMETIC_SCOPE = (
    "binary64 SciPy DOP853 method of steps for the jointly propagated "
    "factorial parameter coefficients a_k=z_k/k!, k=0,...,4; three "
    "tolerance/max-step refinements sampled on a common two-origin mesh; "
    "the pointwise refinement hull is an observed envelope, not a directed "
    "flow or order-five remainder enclosure"
)

EPSILON = float(EPSILON_EXACT)
UNFOLDING = float(UNFOLDING_EXACT)
KAPPA_1 = float(KAPPA_1_EXACT)
KAPPA_3 = float(KAPPA_3_EXACT)
TAU_4 = 4.0 * math.sqrt(5.0)
TAU_5 = 5.0 * math.sqrt(5.0)
PULSE_DURATION = 1.0
J0_EXACT = Fraction(2409, 8000)
J0 = float(J0_EXACT)
WIDE_HALF_WIDTH_EXACT = Fraction(3, 40000)
WIDE_HALF_WIDTH = float(WIDE_HALF_WIDTH_EXACT)
FINAL_SQRT5_MULTIPLIER = 24
FINAL_TIME = FINAL_SQRT5_MULTIPLIER * math.sqrt(5.0)
SAMPLE_GRID_DENOMINATOR = 24
FACTORIALS = np.asarray([1.0, 1.0, 2.0, 6.0, 24.0])


@dataclass(frozen=True)
class Refinement:
    name: str
    rtol: float
    atol: float
    max_step: float


REFINEMENTS = (
    Refinement("coarse", 2.0e-9, 2.0e-11, 0.04),
    Refinement("medium", 2.0e-10, 2.0e-12, 0.02),
    Refinement("fine", 2.0e-11, 2.0e-13, 0.01),
)

NUMERICAL_TRUE_FLAGS = (
    "center_z0_through_z4_integrated_jointly",
    "factorial_parameter_correlation_preserved_in_state_vector",
    "pulse_release_and_both_delay_breakpoint_families_preserved",
    "three_solver_refinements_completed",
    "common_two_origin_mesh_sampled",
    "pointwise_refinement_envelope_recorded",
    "wide_endpoint_fourth_order_reconstruction_compared_with_direct_flows",
)

PROOF_FALSE_FLAGS = (
    "directed_rounding_used",
    "center_coefficient_guides_rigorously_enclosed",
    "mesh_refinement_envelope_is_a_true_solution_enclosure",
    "order_five_parameter_remainder_validated",
    "uniform_wide_interval_parameter_jet_validated",
    "route_c_event_bracket_validated",
    "route_c_event_speed_validated",
    "event_time_jet_validated",
    "common_event_complete_history_jet_validated",
    "rfde_stable_coordinate_validated",
    "interval_newton_onset_validated",
    "unique_physical_pulse_onset_validated",
    "two_sided_basin_routing_validated",
)


def canonical_sha256(value: object) -> str:
    encoded = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("utf-8")
    return sha256(encoded).hexdigest()


def binary64_record(value: float) -> dict[str, str]:
    number = float(value)
    if not math.isfinite(number):
        raise ValueError("pilot numbers must be finite")
    return {"binary64_hex": number.hex(), "decimal": format(number, ".17g")}


def binary64_value(value: object, name: str) -> float:
    if not isinstance(value, Mapping) or set(value) != {
        "binary64_hex",
        "decimal",
    }:
        raise ValueError(f"{name} must be a canonical binary64 record")
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
        raise ValueError(f"{name} is not a canonical finite binary64 value")
    return number


def _sha256_path(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _mapping(value: Any, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{name} must be a mapping")
    return value


def _load_bound_json(repository: Path, relative: str, expected: str) -> Any:
    path = repository / relative
    if _sha256_path(path) != expected:
        raise ValueError(f"center-jet bound parent changed: {relative}")
    return json.loads(path.read_text(encoding="utf-8"))


def _quiet_equilibrium() -> np.ndarray:
    alpha = (3.0 * UNFOLDING) ** (1.0 / 3.0)
    return np.asarray([alpha, alpha - UNFOLDING], dtype=float)


def method_of_steps_breakpoints(final_time: float = FINAL_TIME) -> tuple[float, ...]:
    horizon = float(final_time)
    if not math.isfinite(horizon) or horizon <= 0.0:
        raise ValueError("final time must be finite and positive")
    base = math.sqrt(5.0)
    points = {0.0, horizon}
    for origin in (0.0, PULSE_DURATION):
        lower = math.floor(-origin / base) - 1
        upper = math.ceil((horizon - origin) / base) + 1
        for index in range(lower, upper + 1):
            point = origin + index * base
            if 0.0 < point < horizon:
                points.add(point)
    return tuple(sorted(points))


def common_two_origin_mesh() -> tuple[float, ...]:
    base = math.sqrt(5.0) / SAMPLE_GRID_DENOMINATOR
    points = {0.0, FINAL_TIME}
    for origin in (0.0, PULSE_DURATION):
        lower = math.floor(-origin / base) - 1
        upper = math.ceil((FINAL_TIME - origin) / base) + 1
        for index in range(lower, upper + 1):
            point = origin + index * base
            if 0.0 < point < FINAL_TIME:
                points.add(point)
    return tuple(sorted(points))


@dataclass
class _Segment:
    start: float
    finish: float
    solution: Any


@dataclass
class CoefficientTrajectory:
    initial: np.ndarray
    segments: list[_Segment]

    def coefficients(self, time: float) -> np.ndarray:
        """Return factorial coefficients ``a_k=z_k/k!`` as shape ``(5,2)``."""

        if time <= 0.0:
            return self.initial.copy()
        finishes = [segment.finish for segment in self.segments]
        index = bisect_left(finishes, time - 2.0e-13)
        if index >= len(self.segments):
            if time <= self.segments[-1].finish + 2.0e-11:
                index = len(self.segments) - 1
            else:
                raise ValueError("coefficient evaluation is beyond final time")
        segment = self.segments[index]
        if time < segment.start - 2.0e-11:
            raise ArithmeticError("coefficient segment lookup failed")
        return np.asarray(segment.solution(time), dtype=float).reshape(5, 2)

    def derivative_jets(self, time: float) -> np.ndarray:
        return self.coefficients(time) * FACTORIALS[:, None]


@dataclass
class StateTrajectory:
    equilibrium: np.ndarray
    segments: list[_Segment]

    def state(self, time: float) -> np.ndarray:
        if time <= 0.0:
            return self.equilibrium.copy()
        finishes = [segment.finish for segment in self.segments]
        index = bisect_left(finishes, time - 2.0e-13)
        if index >= len(self.segments):
            if time <= self.segments[-1].finish + 2.0e-11:
                index = len(self.segments) - 1
            else:
                raise ValueError("state evaluation is beyond final time")
        segment = self.segments[index]
        if time < segment.start - 2.0e-11:
            raise ArithmeticError("state segment lookup failed")
        return np.asarray(segment.solution(time), dtype=float)


def _poly_product(left: np.ndarray, right: np.ndarray) -> np.ndarray:
    return np.convolve(left, right)[:5]


def _poly_cube(value: np.ndarray) -> np.ndarray:
    return _poly_product(_poly_product(value, value), value)


def _shifted_cube(value: np.ndarray) -> np.ndarray:
    shifted = value.copy()
    shifted[0] -= 1.0
    return _poly_cube(shifted)


def integrate_center_coefficients(refinement: Refinement) -> CoefficientTrajectory:
    """Jointly integrate the five correlated factorial coefficients."""

    if refinement not in REFINEMENTS:
        raise ValueError("unregistered center-jet refinement")
    equilibrium = _quiet_equilibrium()
    initial = np.zeros((5, 2), dtype=float)
    initial[0] = equilibrium
    segments: list[_Segment] = []

    def past(time: float) -> np.ndarray:
        if time <= 0.0:
            return initial
        finishes = [segment.finish for segment in segments]
        index = bisect_left(finishes, time - 2.0e-13)
        if index >= len(segments):
            raise ArithmeticError("coefficient delay entered the current step")
        return np.asarray(segments[index].solution(time), dtype=float).reshape(5, 2)

    current = initial.copy()
    ordered = method_of_steps_breakpoints()
    for start, finish in zip(ordered[:-1], ordered[1:], strict=True):
        forced = start < PULSE_DURATION - 1.0e-14

        def field(time: float, flattened: np.ndarray) -> np.ndarray:
            coefficients = np.asarray(flattened, dtype=float).reshape(5, 2)
            voltage = coefficients[:, 0]
            recovery = coefficients[:, 1]
            delayed_4 = past(time - TAU_4)[:, 0]
            delayed_5 = past(time - TAU_5)[:, 0]
            fast = voltage - _poly_cube(voltage) / 3.0 - recovery
            fast += EPSILON * KAPPA_1 * (
                (delayed_4 + delayed_5) / 2.0 - voltage
            )
            fast += EPSILON * KAPPA_3 * (
                (_shifted_cube(delayed_4) + _shifted_cube(delayed_5)) / 2.0
                - _shifted_cube(voltage)
            )
            if forced:
                fast[0] += J0
                fast[1] += 1.0
            slow = EPSILON * (voltage - recovery)
            slow[0] -= EPSILON * UNFOLDING
            return np.column_stack((fast, slow)).reshape(-1)

        integration = solve_ivp(
            field,
            (start, finish),
            current.reshape(-1),
            dense_output=True,
            method="DOP853",
            rtol=refinement.rtol,
            atol=refinement.atol,
            max_step=refinement.max_step,
        )
        if not integration.success or integration.sol is None:
            raise RuntimeError("center coefficient method-of-steps solve failed")
        segments.append(_Segment(start, finish, integration.sol))
        current = np.asarray(integration.y[:, -1], dtype=float).reshape(5, 2)
    return CoefficientTrajectory(initial, segments)


def integrate_physical_state(
    amplitude: float, refinement: Refinement
) -> StateTrajectory:
    """Direct two-dimensional comparison flow; still binary64 and non-directed."""

    if not math.isfinite(float(amplitude)):
        raise ValueError("pulse amplitude must be finite")
    if refinement not in REFINEMENTS:
        raise ValueError("unregistered direct-flow refinement")
    equilibrium = _quiet_equilibrium()
    segments: list[_Segment] = []

    def past(time: float) -> np.ndarray:
        if time <= 0.0:
            return equilibrium
        finishes = [segment.finish for segment in segments]
        index = bisect_left(finishes, time - 2.0e-13)
        if index >= len(segments):
            raise ArithmeticError("direct-flow delay entered the current step")
        return np.asarray(segments[index].solution(time), dtype=float)

    current = equilibrium.copy()
    ordered = method_of_steps_breakpoints()
    for start, finish in zip(ordered[:-1], ordered[1:], strict=True):
        forced = start < PULSE_DURATION - 1.0e-14

        def field(time: float, state: np.ndarray) -> np.ndarray:
            voltage, recovery = state
            delayed_4 = past(time - TAU_4)[0]
            delayed_5 = past(time - TAU_5)[0]
            fast = (
                voltage
                - voltage**3 / 3.0
                - recovery
                + EPSILON
                * KAPPA_1
                * ((delayed_4 + delayed_5) / 2.0 - voltage)
                + EPSILON
                * KAPPA_3
                * (
                    ((delayed_4 - 1.0) ** 3 + (delayed_5 - 1.0) ** 3)
                    / 2.0
                    - (voltage - 1.0) ** 3
                )
                + (amplitude if forced else 0.0)
            )
            slow = EPSILON * (voltage - UNFOLDING - recovery)
            return np.asarray([fast, slow])

        integration = solve_ivp(
            field,
            (start, finish),
            current,
            dense_output=True,
            method="DOP853",
            rtol=refinement.rtol,
            atol=refinement.atol,
            max_step=refinement.max_step,
        )
        if not integration.success or integration.sol is None:
            raise RuntimeError("direct comparison method-of-steps solve failed")
        segments.append(_Segment(start, finish, integration.sol))
        current = np.asarray(integration.y[:, -1], dtype=float)
    return StateTrajectory(equilibrium, segments)


def _array_hex_digest(value: np.ndarray) -> str:
    array = np.asarray(value, dtype=np.float64)
    payload = {
        "shape": list(array.shape),
        "binary64_hex": [float(item).hex() for item in array.reshape(-1)],
    }
    return canonical_sha256(payload)


def _matrix_records(value: np.ndarray) -> list[list[dict[str, str]]]:
    matrix = np.asarray(value, dtype=float)
    if matrix.shape != (5, 2):
        raise ValueError("a center-jet record must have shape (5,2)")
    return [
        [binary64_record(matrix[order, component]) for component in range(2)]
        for order in range(5)
    ]


def _component_summary(value: np.ndarray) -> list[dict[str, dict[str, str]]]:
    array = np.asarray(value, dtype=float)
    if array.shape != (5, 2):
        raise ValueError("a component summary must have shape (5,2)")
    return [
        {
            "voltage": binary64_record(array[order, 0]),
            "recovery": binary64_record(array[order, 1]),
        }
        for order in range(5)
    ]


def _refinement_record(refinement: Refinement) -> dict[str, Any]:
    return {
        "name": refinement.name,
        "rtol": binary64_record(refinement.rtol),
        "atol": binary64_record(refinement.atol),
        "max_step": binary64_record(refinement.max_step),
    }


def build_center_jet_pilot() -> dict[str, Any]:
    mesh = np.asarray(common_two_origin_mesh(), dtype=float)
    trajectories = [integrate_center_coefficients(row) for row in REFINEMENTS]
    coefficients = np.asarray(
        [
            [trajectory.coefficients(float(time)) for time in mesh]
            for trajectory in trajectories
        ],
        dtype=float,
    )
    derivative_jets = coefficients * FACTORIALS[None, None, :, None]
    envelope_lower = np.min(derivative_jets, axis=0)
    envelope_upper = np.max(derivative_jets, axis=0)
    envelope_width = envelope_upper - envelope_lower
    maximum_width = np.max(envelope_width, axis=0)
    maximum_abs = np.max(np.abs(derivative_jets[-1]), axis=0)
    maximum_abs_factorial = np.max(np.abs(coefficients[-1]), axis=0)
    wide_scaled_terms = maximum_abs_factorial * np.asarray(
        [WIDE_HALF_WIDTH**order for order in range(5)]
    )[:, None]

    adjacent_rows = []
    for left_index in range(len(REFINEMENTS) - 1):
        right_index = left_index + 1
        difference = np.abs(
            derivative_jets[left_index] - derivative_jets[right_index]
        )
        relative = difference / np.maximum(1.0, np.abs(derivative_jets[right_index]))
        adjacent_rows.append(
            {
                "left": REFINEMENTS[left_index].name,
                "right": REFINEMENTS[right_index].name,
                "maximum_absolute_difference_by_order_component": (
                    _component_summary(np.max(difference, axis=0))
                ),
                "maximum_relative_difference_by_order_component": (
                    _component_summary(np.max(relative, axis=0))
                ),
                "joint_maximum_absolute_difference": binary64_record(
                    float(np.max(difference))
                ),
                "joint_maximum_relative_difference": binary64_record(
                    float(np.max(relative))
                ),
            }
        )

    landmark_targets = (
        ("pulse_release", 1.0),
        ("delay_4", TAU_4),
        ("delay_5", TAU_5),
        ("twenty_sqrt5", 20.0 * math.sqrt(5.0)),
        ("final", FINAL_TIME),
    )
    landmarks = []
    for name, target in landmark_targets:
        index = int(np.argmin(np.abs(mesh - target)))
        if abs(mesh[index] - target) > 2.0e-12:
            raise ArithmeticError("a required center-jet landmark left the mesh")
        landmarks.append(
            {
                "name": name,
                "time": binary64_record(float(mesh[index])),
                "fine_derivative_jets": _matrix_records(
                    derivative_jets[-1, index]
                ),
                "refinement_envelope_lower": _matrix_records(
                    envelope_lower[index]
                ),
                "refinement_envelope_upper": _matrix_records(
                    envelope_upper[index]
                ),
            }
        )

    reconstruction_rows = []
    fine_coefficients = coefficients[-1]
    for sign in (-1, 1):
        delta = sign * WIDE_HALF_WIDTH
        direct = integrate_physical_state(J0 + delta, REFINEMENTS[-1])
        direct_values = np.asarray(
            [direct.state(float(time)) for time in mesh], dtype=float
        )
        powers = np.asarray([delta**order for order in range(5)])
        reconstructed = np.einsum("k,tkc->tc", powers, fine_coefficients)
        difference = np.abs(reconstructed - direct_values)
        reconstruction_rows.append(
            {
                "side": "lower" if sign < 0 else "upper",
                "amplitude": binary64_record(J0 + delta),
                "delta": binary64_record(delta),
                "maximum_absolute_state_difference": {
                    "voltage": binary64_record(float(np.max(difference[:, 0]))),
                    "recovery": binary64_record(float(np.max(difference[:, 1]))),
                    "joint": binary64_record(float(np.max(difference))),
                },
                "terminal_absolute_state_difference": {
                    "voltage": binary64_record(float(difference[-1, 0])),
                    "recovery": binary64_record(float(difference[-1, 1])),
                    "joint": binary64_record(float(np.max(difference[-1]))),
                },
                "direct_mesh_digest": _array_hex_digest(direct_values),
                "reconstructed_mesh_digest": _array_hex_digest(reconstructed),
            }
        )

    claims = {name: True for name in NUMERICAL_TRUE_FLAGS}
    claims.update({name: False for name in PROOF_FALSE_FLAGS})
    return {
        "schema_id": SCHEMA_ID,
        "model_id": MODEL_ID,
        "status": (
            "binary64 jointly correlated coefficient-guide feasibility pilot; "
            "not a directed parameter-family or event certificate"
        ),
        "center_amplitude_exact": {
            "numerator": str(J0_EXACT.numerator),
            "denominator": str(J0_EXACT.denominator),
            "binary64": binary64_record(J0),
        },
        "coefficient_normalization": (
            "a_k=z_k/k!, and z(J0+delta)=sum_{k=0}^4 a_k*delta^k+R_5"
        ),
        "joint_state_order": [
            "a0_voltage",
            "a0_recovery",
            "a1_voltage",
            "a1_recovery",
            "a2_voltage",
            "a2_recovery",
            "a3_voltage",
            "a3_recovery",
            "a4_voltage",
            "a4_recovery",
        ],
        "method_of_steps": {
            "final_time": binary64_record(FINAL_TIME),
            "final_time_exact": "24*sqrt(5)",
            "segment_breakpoint_count": len(method_of_steps_breakpoints()),
            "breakpoint_origins": ["0", "1"],
            "base_spacing": "sqrt(5)",
            "delays": ["4*sqrt(5)", "5*sqrt(5)"],
            "pulse_release": "1",
        },
        "refinements": [_refinement_record(row) for row in REFINEMENTS],
        "common_sample_mesh": {
            "point_count": len(mesh),
            "cell_count": len(mesh) - 1,
            "origins": ["0", "1"],
            "spacing": "sqrt(5)/24",
            "time_mesh_digest": _array_hex_digest(mesh),
        },
        "coefficient_guide": {
            "orders": [0, 1, 2, 3, 4],
            "fine_factorial_coefficient_mesh_digest": _array_hex_digest(
                coefficients[-1]
            ),
            "fine_derivative_jet_mesh_digest": _array_hex_digest(
                derivative_jets[-1]
            ),
            "maximum_absolute_factorial_coefficient_by_order_component": (
                _component_summary(maximum_abs_factorial)
            ),
            "maximum_absolute_derivative_jet_by_order_component": (
                _component_summary(maximum_abs)
            ),
            "maximum_absolute_wide_half_width_scaled_term_by_order_component": (
                _component_summary(wide_scaled_terms)
            ),
            "wide_scaled_term_formula": "max_t |a_k(t)|*(3/40000)^k",
            "landmarks": landmarks,
        },
        "mesh_refinement_envelope": {
            "definition": (
                "pointwise componentwise min/max of the three binary64 "
                "refinement trajectories on the common mesh"
            ),
            "rigorous_solution_enclosure": False,
            "lower_mesh_digest": _array_hex_digest(envelope_lower),
            "upper_mesh_digest": _array_hex_digest(envelope_upper),
            "maximum_width_by_order_component": _component_summary(maximum_width),
            "adjacent_refinement_differences": adjacent_rows,
        },
        "wide_endpoint_reconstruction": {
            "half_width_exact": {
                "numerator": str(WIDE_HALF_WIDTH_EXACT.numerator),
                "denominator": str(WIDE_HALF_WIDTH_EXACT.denominator),
            },
            "degree": 4,
            "rows": reconstruction_rows,
            "diagnostic_only_no_order_five_bound": True,
        },
        "open_stage5_inputs": {
            "directed_coefficient_error_radii": None,
            "directed_order_five_remainder_radius": None,
            "route_c_event_bracket": None,
            "uniform_route_c_event_speed": None,
            "event_time_jet": None,
            "common_event_complete_history_radius": None,
            "stable_coordinate_gap": None,
            "interval_newton_image": None,
        },
        "claim_status": claims,
    }


def build_center_jet_result(repository: Path) -> dict[str, Any]:
    repository = Path(repository).resolve()
    stage5 = _load_bound_json(
        repository, STAGE5_CONTRACT_RELATIVE_PATH, STAGE5_CONTRACT_SHA256
    )
    family = _load_bound_json(
        repository, FAMILY_PARENT_RELATIVE_PATH, FAMILY_PARENT_SHA256
    )
    stage5_contract = _mapping(stage5.get("contract"), "Stage-5 contract")
    family_certificate = _mapping(family.get("certificate"), "family certificate")
    if stage5_contract.get("claim_status", {}).get(
        "z0_through_z4_directed_guides_validated"
    ) is not False:
        raise ValueError("Stage-5 parent no longer leaves coefficient guides open")
    if family_certificate.get("claim_status", {}).get(
        "full_wide_interval_first_J_variation_enclosure_validated"
    ) is not False:
        raise ValueError("family parent no longer records the variation gap")
    pilot = build_center_jet_pilot()
    return {
        "pilot": pilot,
        "manifest": {
            "schema_id": SCHEMA_ID,
            "result": RESULT_RELATIVE_PATH,
            "default_command": DEFAULT_COMMAND,
            "arithmetic_scope": ARITHMETIC_SCOPE,
            "environment": {
                "python": platform.python_version(),
                "platform": platform.platform(),
                "numpy": np.__version__,
                "scipy": scipy.__version__,
            },
            "parent_sha256": {
                STAGE5_CONTRACT_RELATIVE_PATH: STAGE5_CONTRACT_SHA256,
                FAMILY_PARENT_RELATIVE_PATH: FAMILY_PARENT_SHA256,
            },
            "source_sha256": {
                relative: _sha256_path(repository / relative)
                for relative in SOURCE_MANIFEST
            },
            "dependency_source_sha256": {
                relative: _sha256_path(repository / relative)
                for relative in DEPENDENCY_SOURCE_MANIFEST
            },
            "pilot_sha256": canonical_sha256(pilot),
        },
    }


def _validate_binary64_tree(value: Any, name: str) -> None:
    if isinstance(value, Mapping):
        if set(value) == {"binary64_hex", "decimal"}:
            binary64_value(value, name)
            return
        for key, item in value.items():
            _validate_binary64_tree(item, f"{name}.{key}")
    elif isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        for index, item in enumerate(value):
            _validate_binary64_tree(item, f"{name}[{index}]")


def validate_center_jet_result(
    payload: Mapping[str, Any],
    repository: Path,
    *,
    recompute: bool = False,
) -> None:
    if not isinstance(payload, Mapping) or set(payload) != {"pilot", "manifest"}:
        raise ValueError("center-jet result must contain pilot and manifest")
    pilot = _mapping(payload.get("pilot"), "pilot")
    manifest = _mapping(payload.get("manifest"), "manifest")
    if pilot.get("schema_id") != SCHEMA_ID or manifest.get("schema_id") != SCHEMA_ID:
        raise ValueError("center-jet schema changed")
    if manifest.get("result") != RESULT_RELATIVE_PATH:
        raise ValueError("center-jet result path changed")
    if manifest.get("default_command") != DEFAULT_COMMAND:
        raise ValueError("center-jet default command changed")
    if manifest.get("arithmetic_scope") != ARITHMETIC_SCOPE:
        raise ValueError("center-jet arithmetic scope changed")
    if manifest.get("pilot_sha256") != canonical_sha256(pilot):
        raise ValueError("center-jet pilot digest changed")
    _validate_binary64_tree(pilot, "pilot")
    claims = _mapping(pilot.get("claim_status"), "claim status")
    if set(claims) != set(NUMERICAL_TRUE_FLAGS) | set(PROOF_FALSE_FLAGS):
        raise ValueError("center-jet claim ledger changed")
    for name in NUMERICAL_TRUE_FLAGS:
        if claims.get(name) is not True:
            raise ValueError(f"center-jet numerical observation removed: {name}")
    for name in PROOF_FALSE_FLAGS:
        if claims.get(name) is not False:
            raise ValueError(f"center-jet proof claim was promoted: {name}")
    mesh = _mapping(pilot.get("common_sample_mesh"), "sample mesh")
    if mesh.get("point_count") != 1153 or mesh.get("cell_count") != 1152:
        raise ValueError("center-jet common mesh changed")
    guide = _mapping(pilot.get("coefficient_guide"), "coefficient guide")
    if guide.get("orders") != [0, 1, 2, 3, 4]:
        raise ValueError("center-jet coefficient orders changed")
    envelope = _mapping(
        pilot.get("mesh_refinement_envelope"), "refinement envelope"
    )
    if envelope.get("rigorous_solution_enclosure") is not False:
        raise ValueError("mesh envelope was promoted to a rigorous enclosure")
    reconstruction = _mapping(
        pilot.get("wide_endpoint_reconstruction"), "endpoint reconstruction"
    )
    if reconstruction.get("diagnostic_only_no_order_five_bound") is not True:
        raise ValueError("endpoint reconstruction was promoted beyond a diagnostic")
    open_inputs = _mapping(pilot.get("open_stage5_inputs"), "open Stage-5 inputs")
    if any(value is not None for value in open_inputs.values()):
        raise ValueError("an open Stage-5 input was silently populated")
    repository = Path(repository).resolve()
    source_hashes = _mapping(manifest.get("source_sha256"), "source hashes")
    dependency_hashes = _mapping(
        manifest.get("dependency_source_sha256"), "dependency hashes"
    )
    if set(source_hashes) != set(SOURCE_MANIFEST):
        raise ValueError("center-jet source manifest changed")
    if set(dependency_hashes) != set(DEPENDENCY_SOURCE_MANIFEST):
        raise ValueError("center-jet dependency manifest changed")
    for relative in SOURCE_MANIFEST:
        if source_hashes.get(relative) != _sha256_path(repository / relative):
            raise ValueError(f"center-jet source changed: {relative}")
    for relative in DEPENDENCY_SOURCE_MANIFEST:
        if dependency_hashes.get(relative) != _sha256_path(repository / relative):
            raise ValueError(f"center-jet dependency changed: {relative}")
    expected_parents = {
        STAGE5_CONTRACT_RELATIVE_PATH: STAGE5_CONTRACT_SHA256,
        FAMILY_PARENT_RELATIVE_PATH: FAMILY_PARENT_SHA256,
    }
    if dict(_mapping(manifest.get("parent_sha256"), "parent hashes")) != expected_parents:
        raise ValueError("center-jet parent manifest changed")
    for relative, expected in expected_parents.items():
        if _sha256_path(repository / relative) != expected:
            raise ValueError(f"center-jet bound parent changed: {relative}")
    if recompute:
        rebuilt = build_center_jet_pilot()
        if canonical_sha256(rebuilt) != canonical_sha256(pilot):
            raise ValueError("center-jet numerical replay changed")


__all__ = [
    "J0_EXACT",
    "NUMERICAL_TRUE_FLAGS",
    "PROOF_FALSE_FLAGS",
    "REFINEMENTS",
    "RESULT_RELATIVE_PATH",
    "binary64_record",
    "build_center_jet_pilot",
    "build_center_jet_result",
    "canonical_sha256",
    "common_two_origin_mesh",
    "integrate_center_coefficients",
    "integrate_physical_state",
    "validate_center_jet_result",
]
