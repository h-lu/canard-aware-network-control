"""Source-bound extended-precision pilot for the inner split return map.

This module differentiates a fixed-step method-of-steps discretization of
the validated inner orbit polynomial through second order.  It constructs
the Route-C first-return Jacobian and Hessian in physical time, computes the
one-dimensional unstable eigensplit, and reports the six projected Hessian
block majorants used by the Stage-4 matrix contract.

Every numerical row is a pilot, not an interval enclosure.  Long-double
arithmetic, mesh refinement, exact source binding, and hostile claim-ledger
tests do not control time discretization, interpolation, Fourier-orbit
correction, or rounding.  Consequently no stable power constant, return
ball, projected Hessian bound, graph, separator, or onset theorem is
promoted.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from decimal import Decimal, localcontext
from hashlib import sha256
import json
import math
import os
from pathlib import Path
import platform
from typing import Any, Mapping

import numpy as np

from canard_control.leaky_periodic_branch_artifact import (
    validate_leaky_periodic_branch_artifact,
)
from canard_control.leaky_projected_return_hessian_stage4_contract import (
    MatrixLyapunovPerronInputBudget,
    ProjectedReturnHessianBlockBudget,
    RESULT_RELATIVE_PATH as STAGE4_RESULT_RELATIVE_PATH,
    evaluate_matrix_lyapunov_perron_majorant,
    validate_stage4_projected_return_result,
)


SCHEMA_ID = "leaky-projected-return-hessian-stage4a-pilot-v1"
MODEL_ID = "autonomous-leaky-recovery-two-delay-fhn-bistable-proposal"
BRANCH = "inner_saddle_candidate"
SOURCE_RELATIVE_PATH = (
    "src/canard_control/leaky_projected_return_hessian_stage4a_pilot.py"
)
GENERATOR_RELATIVE_PATH = (
    "experiments/leaky_projected_return_hessian_stage4a_pilot.py"
)
RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_projected_return_hessian_stage4a_pilot.json"
)
NOTE_RELATIVE_PATH = "docs/leaky-projected-return-hessian-stage4a-pilot.md"
TEST_RELATIVE_PATH = (
    "tests/test_leaky_projected_return_hessian_stage4a_pilot.py"
)
DEFAULT_STEP_COUNTS = (120, 180, 240)
DEFAULT_COMMAND = (
    "OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONPATH=src "
    "/usr/bin/python3 "
    "experiments/leaky_projected_return_hessian_stage4a_pilot.py"
)
ARITHMETIC_SCOPE = (
    "exact-byte binding to the validated inner orbit and Stage-4 contract; "
    "numpy.longdouble fixed-step RK4 method of steps with cubic delayed "
    "interpolation; analytic first and second variational propagation; "
    "physical-time affine-event differentiation; long-double power "
    "iteration; three-mesh convergence diagnostics; no outward rounding, "
    "continuous-history truncation bound, orbit-ball propagation, interval "
    "return tube, or theorem promotion"
)
SOURCE_MANIFEST = (
    SOURCE_RELATIVE_PATH,
    GENERATOR_RELATIVE_PATH,
    NOTE_RELATIVE_PATH,
)
INNER_ORBIT_RESULT_RELATIVE_PATH = (
    "experiments/results/autonomous_leaky_recovery_inner_branch_artifact.json"
)
INNER_ORBIT_RESULT_SHA256 = (
    "bee1da065d213c3c33d724ced1dba37c5914934515c1128588919bed34abe69b"
)
STAGE4_RESULT_SHA256 = (
    "670fb21874fa26d953ee7bc2dc70f415c47ccc259690567fb20e5e00ea64fe13"
)
PINNED_OPENBLAS_NUM_THREADS = "1"

BLOCK_NAMES = (
    "stable_output_ss_upper",
    "stable_output_su_upper",
    "stable_output_uu_upper",
    "unstable_output_ss_upper",
    "unstable_output_su_upper",
    "unstable_output_uu_upper",
)
TRUE_FLAGS = (
    "source_bound_inner_orbit_polynomial_used",
    "physical_time_first_and_second_event_formulas_executed",
    "six_projected_finite_section_blocks_computed",
    "three_mesh_refinement_pilot_computed",
    "largest_pilot_block_identified",
)
FALSE_FLAGS = (
    "pilot_rows_are_outward_rounded",
    "continuous_history_discretization_error_validated",
    "validated_orbit_ball_propagated_through_variations",
    "stable_power_constant_numeric_upper_validated",
    "split_return_map_ball_validated",
    "six_projected_return_hessian_blocks_validated",
    "matrix_majorant_pilot_promoted_to_proof",
    "inner_local_stable_graph_quantitatively_validated",
    "graph_radius_1p7e_minus_3_validated",
    "physical_pulse_separator_crossing_validated",
    "unique_physical_pulse_onset_validated",
)


@dataclass(frozen=True)
class Stage4APilotArtifact:
    schema_id: str
    model_id: str
    branch: str
    parent_result_sha256: dict[str, str]
    arithmetic_and_discretization: dict[str, Any]
    mesh_rows: tuple[dict[str, Any], ...]
    refinement_pilot_envelope: dict[str, Any]
    stage4_matrix_pilot_evaluation: dict[str, Any]
    pilot_sensitivity: dict[str, Any]
    strict_certificate_ingress: dict[str, Any]
    next_rigorous_certificate: dict[str, Any]
    claim_status: dict[str, bool]


def _sha256_path(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def canonical_sha256(value: Any) -> str:
    encoded = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("ascii")
    return sha256(encoded).hexdigest()


def _mapping(value: Any, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{name} is missing")
    return value


def _format(value: Any) -> str:
    return format(np.longdouble(value), ".21g")


def _norm_infinity_matrix(matrix: np.ndarray) -> np.longdouble:
    return np.max(np.sum(np.abs(matrix), axis=1))


def _load_json_parent(
    repository: Path, relative: str, expected_hash: str, label: str
) -> Mapping[str, Any]:
    raw = (repository / relative).read_bytes()
    if sha256(raw).hexdigest() != expected_hash:
        raise ValueError(f"the bound {label} result changed")
    payload = json.loads(raw)
    if not isinstance(payload, Mapping):
        raise ValueError(f"the bound {label} result is malformed")
    return payload


class _LongDoubleFourierOrbit:
    """Exact-binary64 samples evaluated by a long-double direct DFT."""

    def __init__(self, state: np.ndarray, period: float):
        self.period = np.longdouble(period)
        samples = np.asarray(state, dtype=np.longdouble)
        self.count = len(samples)
        self.modes = np.asarray(
            np.fft.fftfreq(self.count, d=1.0 / self.count),
            dtype=np.longdouble,
        )
        phases = np.arange(self.count, dtype=np.longdouble) / self.count
        imaginary = np.clongdouble(1j)
        two_pi = np.longdouble(2) * np.longdouble(str(math.pi))
        transform = np.exp(
            -imaginary * two_pi * self.modes[:, None] * phases[None, :]
        )
        self.coefficients = (
            transform @ np.asarray(samples, dtype=np.clongdouble)
        ) / np.longdouble(self.count)
        self.two_pi = two_pi

    def evaluate(self, time: Any, derivative: int = 0) -> np.ndarray:
        phase = np.longdouble(time) / self.period
        imaginary = np.clongdouble(1j)
        exponential = np.exp(
            imaginary * self.two_pi * self.modes * phase
        )
        factor = (
            imaginary * self.two_pi * self.modes / self.period
        ) ** derivative
        value = np.sum(
            self.coefficients * (factor * exponential)[:, None], axis=0
        ).real
        return np.asarray(value, dtype=np.longdouble)


@dataclass
class _Model:
    epsilon: np.longdouble
    unfolding: np.longdouble
    kappa_1: np.longdouble
    kappa_3: np.longdouble
    tau_0: np.longdouble
    tau_1: np.longdouble


def _model_from_payload(payload: Mapping[str, Any]) -> _Model:
    artifact = _mapping(payload.get("artifact"), "inner orbit artifact")
    model = _mapping(artifact.get("model"), "inner orbit model")
    parameters = _mapping(model.get("parameters"), "inner orbit parameters")

    def exact(name: str) -> np.longdouble:
        record = _mapping(parameters.get(name), f"parameter {name}")
        hexadecimal = record.get("binary64_hex")
        if not isinstance(hexadecimal, str):
            raise ValueError(f"parameter {name} lacks an exact binary64 value")
        return np.longdouble(float.fromhex(hexadecimal))

    return _Model(
        epsilon=exact("epsilon"),
        unfolding=exact("unfolding_a"),
        kappa_1=exact("kappa_1"),
        kappa_3=exact("kappa_3"),
        tau_0=exact("tau_0"),
        tau_1=exact("tau_1"),
    )


def _field(orbit: _LongDoubleFourierOrbit, model: _Model, time: Any) -> np.ndarray:
    voltage, recovery = orbit.evaluate(time)
    delayed_0 = orbit.evaluate(np.longdouble(time) - model.tau_0)[0]
    delayed_1 = orbit.evaluate(np.longdouble(time) - model.tau_1)[0]
    fast = (
        voltage
        - voltage**3 / np.longdouble(3)
        - recovery
        + model.epsilon
        * model.kappa_1
        * ((delayed_0 + delayed_1) / np.longdouble(2) - voltage)
        + model.epsilon
        * model.kappa_3
        * (
            ((delayed_0 - 1) ** 3 + (delayed_1 - 1) ** 3)
            / np.longdouble(2)
            - (voltage - 1) ** 3
        )
    )
    slow = model.epsilon * (voltage - model.unfolding - recovery)
    return np.asarray([fast, slow], dtype=np.longdouble)


def _linear_coefficients(
    orbit: _LongDoubleFourierOrbit, model: _Model, time: Any
) -> tuple[np.longdouble, np.longdouble, np.longdouble]:
    voltage = orbit.evaluate(time)[0]
    delayed_0 = orbit.evaluate(np.longdouble(time) - model.tau_0)[0]
    delayed_1 = orbit.evaluate(np.longdouble(time) - model.tau_1)[0]
    current = (
        1
        - voltage**2
        - model.epsilon
        * (model.kappa_1 + 3 * model.kappa_3 * (voltage - 1) ** 2)
    )
    delayed_coefficient_0 = (
        model.epsilon
        * (model.kappa_1 + 3 * model.kappa_3 * (delayed_0 - 1) ** 2)
        / 2
    )
    delayed_coefficient_1 = (
        model.epsilon
        * (model.kappa_1 + 3 * model.kappa_3 * (delayed_1 - 1) ** 2)
        / 2
    )
    return current, delayed_coefficient_0, delayed_coefficient_1


def _hessian_coefficients(
    orbit: _LongDoubleFourierOrbit, model: _Model, time: Any
) -> tuple[np.longdouble, np.longdouble, np.longdouble]:
    voltage = orbit.evaluate(time)[0]
    delayed_0 = orbit.evaluate(np.longdouble(time) - model.tau_0)[0]
    delayed_1 = orbit.evaluate(np.longdouble(time) - model.tau_1)[0]
    current = -2 * voltage - 6 * model.epsilon * model.kappa_3 * (
        voltage - 1
    )
    delayed_hessian_0 = (
        3 * model.epsilon * model.kappa_3 * (delayed_0 - 1)
    )
    delayed_hessian_1 = (
        3 * model.epsilon * model.kappa_3 * (delayed_1 - 1)
    )
    return current, delayed_hessian_0, delayed_hessian_1


def _base_second_derivative(
    orbit: _LongDoubleFourierOrbit, model: _Model, time: Any
) -> np.ndarray:
    current, delayed_0, delayed_1 = _linear_coefficients(
        orbit, model, time
    )
    velocity = _field(orbit, model, time)
    velocity_0 = _field(orbit, model, np.longdouble(time) - model.tau_0)[0]
    velocity_1 = _field(orbit, model, np.longdouble(time) - model.tau_1)[0]
    fast = (
        current * velocity[0]
        - velocity[1]
        + delayed_0 * velocity_0
        + delayed_1 * velocity_1
    )
    slow = model.epsilon * (velocity[0] - velocity[1])
    return np.asarray([fast, slow], dtype=np.longdouble)


def _cubic_weights(fraction: np.longdouble) -> tuple[np.longdouble, ...]:
    one = np.longdouble(1)
    two = np.longdouble(2)
    six = np.longdouble(6)
    return (
        -fraction * (fraction - one) * (fraction - two) / six,
        (fraction + one) * (fraction - one) * (fraction - two) / two,
        -(fraction + one) * fraction * (fraction - two) / two,
        (fraction + one) * fraction * (fraction - one) / six,
    )


def _finite_section_variations(
    orbit: _LongDoubleFourierOrbit,
    model: _Model,
    step_count: int,
) -> tuple[np.ndarray, np.ndarray, dict[str, Any]]:
    """Return the section Jacobian, Hessian, and numerical diagnostics."""

    period = orbit.period
    step = period / np.longdouble(step_count)
    history_steps = int(np.ceil(model.tau_1 / step)) + 3
    dimension = history_steps + 1
    storage = history_steps + step_count + 1
    u_voltage: list[np.ndarray | None] = [None] * storage
    v_voltage: list[np.ndarray | None] = [None] * storage
    u_recovery: list[np.ndarray | None] = [None] * storage
    v_recovery: list[np.ndarray | None] = [None] * storage

    for index in range(-history_steps, 0):
        basis = np.zeros(dimension, dtype=np.longdouble)
        basis[index + history_steps] = 1
        u_voltage[index + history_steps] = basis
        v_voltage[index + history_steps] = np.zeros(
            (dimension, dimension), dtype=np.longdouble
        )
    u_voltage[history_steps] = np.zeros(dimension, dtype=np.longdouble)
    v_voltage[history_steps] = np.zeros(
        (dimension, dimension), dtype=np.longdouble
    )
    recovery_basis = np.zeros(dimension, dtype=np.longdouble)
    recovery_basis[-1] = 1
    u_recovery[history_steps] = recovery_basis
    v_recovery[history_steps] = np.zeros(
        (dimension, dimension), dtype=np.longdouble
    )

    def stored(values: list[np.ndarray | None], index: int) -> np.ndarray:
        value = values[index + history_steps]
        if value is None:
            raise ArithmeticError("the pilot requested unavailable grid data")
        return value

    def delayed(values: list[np.ndarray | None], location: np.longdouble) -> np.ndarray:
        left = int(np.floor(location))
        fraction = location - np.longdouble(left)
        weights = _cubic_weights(fraction)
        return sum(
            (weight * stored(values, node) for weight, node in zip(
                weights, (left - 1, left, left + 1, left + 2), strict=True
            )),
            np.zeros_like(stored(values, left)),
        )

    def rhs(
        time: np.longdouble,
        uv: np.ndarray,
        uw: np.ndarray,
        vv: np.ndarray,
        vw: np.ndarray,
        grid_index: int,
        stage: np.longdouble,
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        current, coefficient_0, coefficient_1 = _linear_coefficients(
            orbit, model, time
        )
        h_current, h_0, h_1 = _hessian_coefficients(orbit, model, time)
        location_0 = (
            np.longdouble(grid_index) + stage - model.tau_0 / step
        )
        location_1 = (
            np.longdouble(grid_index) + stage - model.tau_1 / step
        )
        uv_0 = delayed(u_voltage, location_0)
        uv_1 = delayed(u_voltage, location_1)
        vv_0 = delayed(v_voltage, location_0)
        vv_1 = delayed(v_voltage, location_1)
        duv = current * uv - uw + coefficient_0 * uv_0 + coefficient_1 * uv_1
        duw = model.epsilon * (uv - uw)
        dvv = (
            current * vv
            - vw
            + coefficient_0 * vv_0
            + coefficient_1 * vv_1
            + h_current * np.outer(uv, uv)
            + h_0 * np.outer(uv_0, uv_0)
            + h_1 * np.outer(uv_1, uv_1)
        )
        dvw = model.epsilon * (vv - vw)
        return duv, duw, dvv, dvw

    half = np.longdouble("0.5")
    one = np.longdouble(1)
    for grid_index in range(step_count):
        uv = stored(u_voltage, grid_index)
        uw = stored(u_recovery, grid_index)
        vv = stored(v_voltage, grid_index)
        vw = stored(v_recovery, grid_index)
        time = np.longdouble(grid_index) * step
        k1 = rhs(time, uv, uw, vv, vw, grid_index, np.longdouble(0))
        k2 = rhs(
            time + half * step,
            uv + half * step * k1[0],
            uw + half * step * k1[1],
            vv + half * step * k1[2],
            vw + half * step * k1[3],
            grid_index,
            half,
        )
        k3 = rhs(
            time + half * step,
            uv + half * step * k2[0],
            uw + half * step * k2[1],
            vv + half * step * k2[2],
            vw + half * step * k2[3],
            grid_index,
            half,
        )
        k4 = rhs(
            time + step,
            uv + step * k3[0],
            uw + step * k3[1],
            vv + step * k3[2],
            vw + step * k3[3],
            grid_index,
            one,
        )
        index = grid_index + 1
        u_voltage[index + history_steps] = uv + step * (
            k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]
        ) / 6
        u_recovery[index + history_steps] = uw + step * (
            k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]
        ) / 6
        v_voltage[index + history_steps] = vv + step * (
            k1[2] + 2 * k2[2] + 2 * k3[2] + k4[2]
        ) / 6
        v_recovery[index + history_steps] = vw + step * (
            k1[3] + 2 * k2[3] + 2 * k3[3] + k4[3]
        ) / 6

    final_uv = stored(u_voltage, step_count)
    final_uw = stored(u_recovery, step_count)
    final_vv = stored(v_voltage, step_count)
    final_vw = stored(v_recovery, step_count)
    final_rhs = rhs(
        period,
        final_uv,
        final_uw,
        final_vv,
        final_vw,
        step_count,
        np.longdouble(0),
    )
    event_speed = _field(orbit, model, period)[0]
    if event_speed <= 0:
        raise ArithmeticError("the Route-C pilot event has wrong orientation")
    tau_one = -final_uv / event_speed
    second_base = _base_second_derivative(orbit, model, period)
    event_core = (
        final_vv
        + np.outer(final_rhs[0], tau_one)
        + np.outer(tau_one, final_rhs[0])
        + second_base[0] * np.outer(tau_one, tau_one)
    )
    tau_two = -event_core / event_speed

    jacobian_rows: list[np.ndarray] = []
    hessian_rows: list[np.ndarray] = []
    for index in range(step_count - history_steps, step_count):
        uv = stored(u_voltage, index)
        uw = stored(u_recovery, index)
        vv = stored(v_voltage, index)
        vw = stored(v_recovery, index)
        derivative = rhs(
            np.longdouble(index) * step,
            uv,
            uw,
            vv,
            vw,
            index,
            np.longdouble(0),
        )
        velocity = _field(orbit, model, np.longdouble(index) * step)[0]
        acceleration = _base_second_derivative(
            orbit, model, np.longdouble(index) * step
        )[0]
        jacobian_rows.append(uv + velocity * tau_one)
        hessian_rows.append(
            vv
            + np.outer(derivative[0], tau_one)
            + np.outer(tau_one, derivative[0])
            + acceleration * np.outer(tau_one, tau_one)
            + velocity * tau_two
        )
    recovery_velocity = _field(orbit, model, period)[1]
    recovery_acceleration = second_base[1]
    jacobian_rows.append(final_uw + recovery_velocity * tau_one)
    hessian_rows.append(
        final_vw
        + np.outer(final_rhs[1], tau_one)
        + np.outer(tau_one, final_rhs[1])
        + recovery_acceleration * np.outer(tau_one, tau_one)
        + recovery_velocity * tau_two
    )
    jacobian = np.asarray(jacobian_rows, dtype=np.longdouble)
    hessian = np.asarray(hessian_rows, dtype=np.longdouble)

    current_section_jacobian = final_uv + event_speed * tau_one
    current_section_hessian = event_core + event_speed * tau_two
    diagnostics = {
        "step_count": step_count,
        "step_size": _format(step),
        "history_padding_steps": history_steps,
        "section_dimension": dimension,
        "base_event_speed": _format(event_speed),
        "base_orbit_field_vs_fourier_tangent_inf": _format(
            np.max(np.abs(_field(orbit, model, period) - orbit.evaluate(period, 1)))
        ),
        "first_event_identity_defect_inf": _format(
            np.max(np.abs(current_section_jacobian))
        ),
        "second_event_identity_defect_inf": _format(
            np.max(np.abs(current_section_hessian))
        ),
        "return_hessian_symmetry_defect_inf": _format(
            np.max(np.abs(hessian - np.swapaxes(hessian, 1, 2)))
        ),
        "return_time_d1_ambient_linf_operator_norm": _format(
            np.sum(np.abs(tau_one))
        ),
        "return_time_d2_ambient_linf_bilinear_upper": _format(
            np.sum(np.abs(tau_two))
        ),
    }
    return jacobian, hessian, diagnostics


def _dominant_split(
    matrix: np.ndarray,
) -> tuple[np.longdouble, np.ndarray, np.ndarray, dict[str, str]]:
    dimension = matrix.shape[0]
    right = np.linspace(1, 2, dimension, dtype=np.longdouble)
    left = np.linspace(2, 1, dimension, dtype=np.longdouble)
    for _ in range(40):
        right = matrix @ right
        right /= np.max(np.abs(right))
        left = matrix.T @ left
        left /= np.max(np.abs(left))
    pairing = left @ right
    if abs(pairing) < np.longdouble("1e-12"):
        raise ArithmeticError("the finite-section eigenvectors lost pairing")
    left = left / pairing
    multiplier = left @ (matrix @ right)
    right_residual = np.max(np.abs(matrix @ right - multiplier * right))
    left_residual = np.max(np.abs(left @ matrix - multiplier * left))
    projector_u = np.outer(right, left)
    projector_s = np.eye(dimension, dtype=np.longdouble) - projector_u
    diagnostics = {
        "unstable_multiplier": _format(multiplier),
        "unstable_right_residual_inf": _format(right_residual),
        "unstable_left_residual_inf": _format(left_residual),
        "unstable_vector_linf_norm": _format(np.max(np.abs(right))),
        "unstable_covector_l1_norm": _format(np.sum(np.abs(left))),
        "unstable_projection_linf_norm": _format(
            _norm_infinity_matrix(projector_u)
        ),
        "stable_projection_linf_norm": _format(
            _norm_infinity_matrix(projector_s)
        ),
        "projector_idempotence_defect_inf": _format(
            _norm_infinity_matrix(projector_u @ projector_u - projector_u)
        ),
    }
    return multiplier, right, left, diagnostics


def _stable_power_pilot(
    matrix: np.ndarray,
    right: np.ndarray,
    left: np.ndarray,
    rho_s: np.longdouble,
    maximum_power: int = 12,
) -> dict[str, Any]:
    projector_u = np.outer(right, left)
    projector_s = np.eye(len(right), dtype=np.longdouble) - projector_u
    stable_map = projector_s @ matrix @ projector_s
    current = projector_s.copy()
    rows = []
    candidate = np.longdouble(1)
    for power in range(1, maximum_power + 1):
        current = stable_map @ current
        norm = _norm_infinity_matrix(current)
        ratio = norm / rho_s**power
        candidate = max(candidate, ratio)
        rows.append(
            {
                "power": power,
                "projected_power_linf_upper_binary": _format(norm),
                "ratio_to_declared_rho_power": _format(ratio),
            }
        )
    one_step = np.longdouble(rows[0]["projected_power_linf_upper_binary"])
    return {
        "power_horizon": maximum_power,
        "rows": rows,
        "finite_horizon_k_s_candidate": _format(candidate),
        "finite_section_one_step_restriction_candidate": _format(one_step),
        "one_step_below_declared_rho": bool(one_step < rho_s),
        "finite_section_all_power_k_s_candidate": (
            "1" if one_step < rho_s else None
        ),
        "finite_section_all_power_reason": (
            "n=0 is the identity on E_s; the computed projected one-step "
            "restriction is below rho_s, so submultiplicativity gives K_s=1 "
            "for this finite-section map"
        ),
        "all_powers_validated": False,
    }


def _projected_block_pilot(
    hessian: np.ndarray,
    right: np.ndarray,
    left: np.ndarray,
) -> dict[str, str]:
    projector_u = np.outer(right, left)
    projector_s = np.eye(len(right), dtype=np.longdouble) - projector_u
    h_q = np.einsum("oij,j->oi", hessian, right, optimize=True)
    h_qq = np.einsum("oi,i->o", h_q, right, optimize=True)
    h_ss = (
        hessian
        - left[None, :, None] * h_q[:, None, :]
        - h_q[:, :, None] * left[None, None, :]
        + h_qq[:, None, None] * left[None, :, None] * left[None, None, :]
    )
    h_su = h_q - h_qq[:, None] * left[None, :]
    unstable_ss = np.einsum("o,oij->ij", left, h_ss, optimize=True)
    unstable_su = np.einsum("o,oi->i", left, h_su, optimize=True)
    unstable_uu = left @ h_qq
    stable_ss = h_ss - right[:, None, None] * unstable_ss[None, :, :]
    stable_su = h_su - right[:, None] * unstable_su[None, :]
    stable_uu = h_qq - right * unstable_uu
    return {
        "stable_output_ss_upper": _format(
            np.max(np.sum(np.abs(stable_ss), axis=(1, 2)))
        ),
        "stable_output_su_upper": _format(
            np.max(np.sum(np.abs(stable_su), axis=1))
        ),
        "stable_output_uu_upper": _format(np.max(np.abs(stable_uu))),
        "unstable_output_ss_upper": _format(np.sum(np.abs(unstable_ss))),
        "unstable_output_su_upper": _format(np.sum(np.abs(unstable_su))),
        "unstable_output_uu_upper": _format(abs(unstable_uu)),
    }


def _mesh_row(
    orbit: _LongDoubleFourierOrbit,
    model: _Model,
    step_count: int,
    rho_s: np.longdouble,
) -> dict[str, Any]:
    jacobian, hessian, discretization = _finite_section_variations(
        orbit, model, step_count
    )
    _, right, left, split = _dominant_split(jacobian)
    powers = _stable_power_pilot(jacobian, right, left, rho_s)
    blocks = _projected_block_pilot(hessian, right, left)
    largest_name = max(BLOCK_NAMES, key=lambda name: np.longdouble(blocks[name]))
    return {
        **discretization,
        "eigensplit": split,
        "stable_power_pilot": powers,
        "projected_hessian_block_pilot": blocks,
        "largest_projected_hessian_block": {
            "name": largest_name,
            "value": blocks[largest_name],
        },
        "evidence_status": (
            "source-bound long-double finite-section pilot; not an interval "
            "or continuous-history operator bound"
        ),
    }


def _refinement_envelope(rows: list[dict[str, Any]]) -> dict[str, Any]:
    if len(rows) < 2:
        raise ValueError("the refinement pilot needs at least two meshes")
    previous = rows[-2]["projected_hessian_block_pilot"]
    final = rows[-1]["projected_hessian_block_pilot"]
    envelope: dict[str, str] = {}
    changes: dict[str, str] = {}
    for name in BLOCK_NAMES:
        old = np.longdouble(previous[name])
        new = np.longdouble(final[name])
        change = abs(new - old)
        candidate = max(old, new) + 2 * change + np.longdouble("1e-15")
        envelope[name] = _format(candidate)
        changes[name] = _format(change)
    k_values = [
        np.longdouble(row["stable_power_pilot"]["finite_horizon_k_s_candidate"])
        for row in rows
    ]
    k_candidate = max(k_values) + 2 * abs(k_values[-1] - k_values[-2])
    largest_name = max(BLOCK_NAMES, key=lambda name: np.longdouble(envelope[name]))
    return {
        "construction": (
            "max(last two meshes)+2*last-mesh change+1e-15 for each block; "
            "this is a heuristic refinement envelope, not directed error"
        ),
        "last_mesh_absolute_changes": changes,
        "stable_power_finite_horizon_k_s_candidate": _format(k_candidate),
        "projected_hessian_block_candidate_upper": envelope,
        "largest_block": {
            "name": largest_name,
            "candidate_upper": envelope[largest_name],
        },
        "split_return_ball_radius_candidate": "0.0017",
        "split_return_ball_radius_validated": False,
        "continuous_history_upper_bound": False,
    }


def _scaled_pilot_budget(
    budget: MatrixLyapunovPerronInputBudget,
    multipliers: Mapping[str, Decimal],
) -> MatrixLyapunovPerronInputBudget:
    values = asdict(budget.hessian_blocks)
    scaled = {}
    with localcontext() as context:
        context.prec = 96
        for name in BLOCK_NAMES:
            multiplier = multipliers.get(name, Decimal(1))
            scaled[name] = format(Decimal(values[name]) * multiplier, "f")
    return MatrixLyapunovPerronInputBudget(
        stable_power_rate_upper=budget.stable_power_rate_upper,
        unstable_backward_rate_upper=budget.unstable_backward_rate_upper,
        stable_power_constant_upper=budget.stable_power_constant_upper,
        unstable_backward_power_constant_upper=(
            budget.unstable_backward_power_constant_upper
        ),
        sequence_weight_beta=budget.sequence_weight_beta,
        stable_seed_radius=budget.stable_seed_radius,
        stable_graph_radius=budget.stable_graph_radius,
        unstable_graph_radius=budget.unstable_graph_radius,
        validated_return_map_split_ball_radius_lower=(
            budget.validated_return_map_split_ball_radius_lower
        ),
        hessian_blocks=ProjectedReturnHessianBlockBudget(
            **scaled,
            evidence_status="scaled nonrigorous Stage-4A sensitivity pilot",
        ),
        evidence_status="scaled nonrigorous Stage-4A sensitivity pilot",
    )


def _pilot_sensitivity(
    budget: MatrixLyapunovPerronInputBudget,
) -> dict[str, Any]:
    """Bracket isolated and common inflation thresholds of the exact evaluator."""

    def evaluation(name: str, multiplier: Decimal):
        names = BLOCK_NAMES if name == "all_six_blocks" else (name,)
        return evaluate_matrix_lyapunov_perron_majorant(
            _scaled_pilot_budget(
                budget, {block: multiplier for block in names}
            )
        )

    rows: dict[str, Any] = {}
    baseline_blocks = asdict(budget.hessian_blocks)
    for name in (*BLOCK_NAMES, "all_six_blocks"):
        lower = Decimal(1)
        upper = Decimal(2)
        while evaluation(name, upper).graph_certificate_closes:
            lower = upper
            upper *= 2
            if upper > Decimal("1e7"):
                raise ArithmeticError("a pilot sensitivity threshold escaped")
        for _ in range(96):
            midpoint = (lower + upper) / 2
            if evaluation(name, midpoint).graph_certificate_closes:
                lower = midpoint
            else:
                upper = midpoint
        closing = evaluation(name, lower)
        failing = evaluation(name, upper)
        failed_gates = []
        if not failing.contraction_closes:
            failed_gates.append("contraction")
        if not failing.self_map_closes:
            failed_gates.append("self_map")
        if not failing.split_ball_contains_graph_box:
            failed_gates.append("split_ball")
        rows[name] = {
            "closing_multiplier_lower": format(lower, "f"),
            "failing_multiplier_upper": format(upper, "f"),
            "scaled_block_value_at_closing_lower": (
                None
                if name == "all_six_blocks"
                else format(Decimal(baseline_blocks[name]) * lower, "f")
            ),
            "first_failed_gates": failed_gates,
            "closing_perron_upper": closing.perron_root_upper,
            "closing_self_map_slack_lower": closing.self_map_slack_vector_lower,
        }
    ordered = sorted(
        BLOCK_NAMES,
        key=lambda name: Decimal(rows[name]["closing_multiplier_lower"]),
    )
    return {
        "definition": (
            "single-parameter supremum bracket for the exact Stage-4 evaluator: "
            "multiply only the named pilot block, hold all other pilot inputs "
            "fixed, and bisect between the last closing and first failing value"
        ),
        "baseline_is_nonrigorous": True,
        "thresholds_are_theorem_tolerances": False,
        "isolated_block_thresholds": {
            name: rows[name] for name in BLOCK_NAMES
        },
        "common_six_block_threshold": rows["all_six_blocks"],
        "tightness_order": ordered,
        "directed_priority": (
            "stable_output_uu_upper first, then joint stable-output error; "
            "the largest absolute unstable_output_uu_upper block has much "
            "more isolated inflation headroom"
        ),
    }


def build_stage4a_pilot_artifact(repository: Path) -> Stage4APilotArtifact:
    if os.environ.get("OPENBLAS_NUM_THREADS") != PINNED_OPENBLAS_NUM_THREADS:
        raise RuntimeError(
            "the Stage-4A replay requires OPENBLAS_NUM_THREADS="
            + PINNED_OPENBLAS_NUM_THREADS
        )
    repository = repository.resolve()
    orbit_payload = _load_json_parent(
        repository,
        INNER_ORBIT_RESULT_RELATIVE_PATH,
        INNER_ORBIT_RESULT_SHA256,
        "inner orbit",
    )
    stage4_payload = _load_json_parent(
        repository,
        STAGE4_RESULT_RELATIVE_PATH,
        STAGE4_RESULT_SHA256,
        "Stage-4",
    )
    orbit_candidate = validate_leaky_periodic_branch_artifact(
        orbit_payload, repository
    )
    validate_stage4_projected_return_result(stage4_payload, repository)
    stage4_contract = _mapping(stage4_payload.get("contract"), "Stage-4 contract")
    stage4_budget = _mapping(
        stage4_contract.get("matrix_input_budget"), "Stage-4 matrix budget"
    )
    rho_s = np.longdouble(stage4_budget["stable_power_rate_upper"])
    state = np.asarray(orbit_candidate.state, dtype=np.longdouble)
    orbit = _LongDoubleFourierOrbit(state, orbit_candidate.period)
    model = _model_from_payload(orbit_payload)
    rows = [
        _mesh_row(orbit, model, step_count, rho_s)
        for step_count in DEFAULT_STEP_COUNTS
    ]
    envelope = _refinement_envelope(rows)
    blocks = ProjectedReturnHessianBlockBudget(
        **envelope["projected_hessian_block_candidate_upper"],
        evidence_status="nonrigorous Stage-4A refinement pilot",
    )
    pilot_budget = MatrixLyapunovPerronInputBudget(
        stable_power_rate_upper=str(stage4_budget["stable_power_rate_upper"]),
        unstable_backward_rate_upper=str(
            stage4_budget["unstable_backward_rate_upper"]
        ),
        stable_power_constant_upper=envelope[
            "stable_power_finite_horizon_k_s_candidate"
        ],
        unstable_backward_power_constant_upper=str(
            stage4_budget["unstable_backward_power_constant_upper"]
        ),
        sequence_weight_beta=str(stage4_budget["sequence_weight_beta"]),
        stable_seed_radius=str(stage4_budget["stable_seed_radius"]),
        stable_graph_radius=str(stage4_budget["stable_graph_radius"]),
        unstable_graph_radius=str(stage4_budget["unstable_graph_radius"]),
        validated_return_map_split_ball_radius_lower=(
            envelope["split_return_ball_radius_candidate"]
        ),
        hessian_blocks=blocks,
        evidence_status=(
            "nonrigorous diagnostic substitution into the exact Stage-4 "
            "matrix evaluator"
        ),
    )
    matrix_pilot = evaluate_matrix_lyapunov_perron_majorant(pilot_budget)
    sensitivity = _pilot_sensitivity(pilot_budget)
    claims = {name: True for name in TRUE_FLAGS}
    claims.update({name: False for name in FALSE_FLAGS})
    return Stage4APilotArtifact(
        schema_id=SCHEMA_ID,
        model_id=MODEL_ID,
        branch=BRANCH,
        parent_result_sha256={
            INNER_ORBIT_RESULT_RELATIVE_PATH: INNER_ORBIT_RESULT_SHA256,
            STAGE4_RESULT_RELATIVE_PATH: STAGE4_RESULT_SHA256,
        },
        arithmetic_and_discretization={
            "step_counts": list(DEFAULT_STEP_COUNTS),
            "integrator": "fixed-step classical RK4",
            "delay_interpolation": "four-node cubic Lagrange",
            "state_arithmetic": "numpy.longdouble",
            "longdouble_bits": int(np.finfo(np.longdouble).bits),
            "longdouble_epsilon": _format(np.finfo(np.longdouble).eps),
            "orbit_representation": (
                "direct long-double DFT of exact binary64 validated-orbit "
                "polynomial samples"
            ),
            "section": (
                "Route-C affine current-voltage perturbation zero at phase zero"
            ),
            "domain_norm": (
                "nodal ambient l-infinity; stable inputs are precomposed with "
                "the finite-section stable projector"
            ),
            "operator_upper_meaning": (
                "entrywise absolute row sums for the computed finite tensor only"
            ),
        },
        mesh_rows=tuple(rows),
        refinement_pilot_envelope=envelope,
        stage4_matrix_pilot_evaluation=asdict(matrix_pilot),
        pilot_sensitivity=sensitivity,
        strict_certificate_ingress={
            "stable_power_constant_upper": None,
            "validated_split_return_ball_radius_lower": None,
            **{name: None for name in BLOCK_NAMES},
            "pilot_values_promoted": False,
        },
        next_rigorous_certificate={
            "stable_power": (
                "replace the finite-horizon projected powers by a directed "
                "continuous-history deflated resolvent or all-power bound"
            ),
            "return_ball": (
                "enclose the first positive physical return, exclude earlier "
                "hits, and prove a uniform event-speed lower bound on a split ball"
            ),
            "hessian_blocks": (
                "propagate the validated orbit ball and first/second variation "
                "operators by outward-rounded method of steps, then apply split "
                "output coordinates before norms"
            ),
            "minimal_missing_strict_fields": (
                "one K_s upper, one split return-ball lower, and six projected "
                "D2P block uppers"
            ),
        },
        claim_status=claims,
    )


def build_stage4a_pilot_result(repository: Path) -> dict[str, Any]:
    repository = repository.resolve()
    artifact = asdict(build_stage4a_pilot_artifact(repository))
    return {
        "artifact": artifact,
        "manifest": {
            "schema_id": SCHEMA_ID,
            "result": RESULT_RELATIVE_PATH,
            "default_command": DEFAULT_COMMAND,
            "arithmetic_scope": ARITHMETIC_SCOPE,
            "artifact_sha256": canonical_sha256(artifact),
            "source_sha256": {
                relative: _sha256_path(repository / relative)
                for relative in SOURCE_MANIFEST
            },
            "parent_result_sha256": {
                INNER_ORBIT_RESULT_RELATIVE_PATH: INNER_ORBIT_RESULT_SHA256,
                STAGE4_RESULT_RELATIVE_PATH: STAGE4_RESULT_SHA256,
            },
            "environment": {
                "python": platform.python_version(),
                "platform": platform.platform(),
                "numpy": np.__version__,
                "openblas_num_threads": os.environ.get("OPENBLAS_NUM_THREADS"),
            },
        },
    }


def validate_stage4a_pilot_result(
    payload: Mapping[str, Any], repository: Path
) -> None:
    if not isinstance(payload, Mapping) or set(payload) != {"artifact", "manifest"}:
        raise ValueError("the Stage-4A result has the wrong outer schema")
    artifact = _mapping(payload.get("artifact"), "Stage-4A artifact")
    manifest = _mapping(payload.get("manifest"), "Stage-4A manifest")
    if set(artifact) != {field.name for field in fields(Stage4APilotArtifact)}:
        raise ValueError("the Stage-4A artifact schema changed")
    if (
        artifact.get("schema_id") != SCHEMA_ID
        or artifact.get("model_id") != MODEL_ID
        or artifact.get("branch") != BRANCH
    ):
        raise ValueError("the Stage-4A identity changed")
    claims = _mapping(artifact.get("claim_status"), "Stage-4A claims")
    if set(claims) != set(TRUE_FLAGS) | set(FALSE_FLAGS):
        raise ValueError("the Stage-4A claim ledger changed")
    if any(claims.get(name) is not True for name in TRUE_FLAGS):
        raise ValueError("a Stage-4A pilot statement was weakened")
    if any(claims.get(name) is not False for name in FALSE_FLAGS):
        raise ValueError("a Stage-4A pilot was promoted to proof")
    rows = artifact.get("mesh_rows")
    if not isinstance(rows, (list, tuple)) or [
        row.get("step_count") for row in rows
    ] != list(DEFAULT_STEP_COUNTS):
        raise ValueError("the Stage-4A mesh ladder changed")
    for row in rows:
        blocks = _mapping(
            row.get("projected_hessian_block_pilot"), "mesh block pilot"
        )
        if set(blocks) != set(BLOCK_NAMES):
            raise ValueError("a mesh lost one of the six projected blocks")
        if any(float(blocks[name]) < 0 for name in BLOCK_NAMES):
            raise ValueError("a projected block pilot is negative")
        if row.get("stable_power_pilot", {}).get("all_powers_validated") is not False:
            raise ValueError("a finite-horizon power pilot was promoted")
    envelope = _mapping(
        artifact.get("refinement_pilot_envelope"), "refinement envelope"
    )
    block_envelope = _mapping(
        envelope.get("projected_hessian_block_candidate_upper"),
        "block refinement envelope",
    )
    if set(block_envelope) != set(BLOCK_NAMES):
        raise ValueError("the six-block refinement envelope changed")
    if (
        envelope.get("split_return_ball_radius_candidate") != "0.0017"
        or envelope.get("split_return_ball_radius_validated") is not False
        or envelope.get("continuous_history_upper_bound") is not False
    ):
        raise ValueError("the pilot return ball or blocks were promoted")
    sensitivity = _mapping(
        artifact.get("pilot_sensitivity"), "Stage-4A pilot sensitivity"
    )
    thresholds = _mapping(
        sensitivity.get("isolated_block_thresholds"),
        "Stage-4A isolated sensitivity thresholds",
    )
    if set(thresholds) != set(BLOCK_NAMES):
        raise ValueError("the Stage-4A block sensitivity set changed")
    if (
        sensitivity.get("baseline_is_nonrigorous") is not True
        or sensitivity.get("thresholds_are_theorem_tolerances") is not False
        or sensitivity.get("tightness_order", [None])[0]
        != "stable_output_uu_upper"
    ):
        raise ValueError("the Stage-4A sensitivity boundary changed")
    ingress = _mapping(
        artifact.get("strict_certificate_ingress"), "strict certificate ingress"
    )
    required_null = {
        "stable_power_constant_upper",
        "validated_split_return_ball_radius_lower",
        *BLOCK_NAMES,
    }
    if any(ingress.get(name) is not None for name in required_null):
        raise ValueError("a pilot number entered the strict certificate")
    if ingress.get("pilot_values_promoted") is not False:
        raise ValueError("pilot promotion changed")

    expected_manifest_fields = {
        "schema_id",
        "result",
        "default_command",
        "arithmetic_scope",
        "artifact_sha256",
        "source_sha256",
        "parent_result_sha256",
        "environment",
    }
    if set(manifest) != expected_manifest_fields:
        raise ValueError("the Stage-4A manifest schema changed")
    fixed = {
        "schema_id": SCHEMA_ID,
        "result": RESULT_RELATIVE_PATH,
        "default_command": DEFAULT_COMMAND,
        "arithmetic_scope": ARITHMETIC_SCOPE,
        "artifact_sha256": canonical_sha256(artifact),
        "parent_result_sha256": {
            INNER_ORBIT_RESULT_RELATIVE_PATH: INNER_ORBIT_RESULT_SHA256,
            STAGE4_RESULT_RELATIVE_PATH: STAGE4_RESULT_SHA256,
        },
    }
    if any(manifest.get(name) != value for name, value in fixed.items()):
        raise ValueError("the Stage-4A manifest fixed data changed")
    repository = repository.resolve()
    sources = _mapping(manifest.get("source_sha256"), "Stage-4A sources")
    if set(sources) != set(SOURCE_MANIFEST):
        raise ValueError("the Stage-4A source set changed")
    for relative in SOURCE_MANIFEST:
        if sources.get(relative) != _sha256_path(repository / relative):
            raise ValueError(f"the Stage-4A source changed: {relative}")
    for relative, digest in fixed["parent_result_sha256"].items():
        if _sha256_path(repository / relative) != digest:
            raise ValueError(f"the Stage-4A parent changed: {relative}")


__all__ = [
    "ARITHMETIC_SCOPE",
    "BLOCK_NAMES",
    "DEFAULT_COMMAND",
    "DEFAULT_STEP_COUNTS",
    "FALSE_FLAGS",
    "GENERATOR_RELATIVE_PATH",
    "NOTE_RELATIVE_PATH",
    "RESULT_RELATIVE_PATH",
    "SCHEMA_ID",
    "SOURCE_MANIFEST",
    "SOURCE_RELATIVE_PATH",
    "Stage4APilotArtifact",
    "TRUE_FLAGS",
    "build_stage4a_pilot_artifact",
    "build_stage4a_pilot_result",
    "canonical_sha256",
    "validate_stage4a_pilot_result",
]
