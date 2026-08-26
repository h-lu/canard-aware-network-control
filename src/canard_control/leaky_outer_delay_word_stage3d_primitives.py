"""Stage-3D primitive reduction and continuous-kernel pilot.

The finite delay-word expansion of Stage-3C can be reduced further.  If
``F'=A F`` and ``G=F^{-1}``, put

    C_j(r) = G(r) B_j(r) F(r-tau_j),
    H_j'   = C_j,
    L_jk'  = C_j(r) H_k(r-tau_j).

Every word of length at most two is then evaluated from one-dimensional
primitives H and L; no numerical two-simplex quadrature is required.  This
module registers that exact algebra, rebuilds a binary64 continuous-density
pilot without sampling the input history, and proves a continuous tangent
phase-projection bound with outward MPFR arithmetic.

The exact-orbit transfer of the signed density is not validated here.  Thus
E_voltage and E_recovery remain null, while E_phase is supplied rigorously.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from functools import lru_cache
from hashlib import sha256
import json
import math
import os
from pathlib import Path
import platform
from typing import Any, Mapping, Sequence

import gmpy2
import numpy as np
import scipy
from scipy.integrate import solve_ivp

from canard_control.directed_interval import (
    DirectedInterval,
    decimal_lower,
    decimal_upper,
)
from canard_control.leaky_outer_continuous_kernel_stage3_shard import (
    _build_leaky_base_sequences,
    _current_matrix,
    _series_real_box,
)
from canard_control.leaky_outer_high_resolution import (
    RESULT_RELATIVE_PATH as OUTER_RESULT_RELATIVE_PATH,
    validate_outer_high_resolution_artifact,
)
from canard_control.leaky_outer_phase_fixed_return_stage1 import (
    _periodic_interpolator,
)
from canard_control.leaky_pulse_separator_candidate import (
    EPSILON,
    KAPPA_1,
    KAPPA_3,
    TAU_0,
    TAU_1,
)


SCHEMA_ID = "leaky-outer-delay-word-stage3d-primitives-v1"
MODEL_ID = "autonomous-leaky-recovery-two-delay-fhn-bistable-proposal"
BRANCH = "outer_pulse"
SOURCE_RELATIVE_PATH = (
    "src/canard_control/leaky_outer_delay_word_stage3d_primitives.py"
)
GENERATOR_RELATIVE_PATH = (
    "experiments/leaky_outer_delay_word_stage3d_primitives.py"
)
RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_outer_delay_word_stage3d_primitives.json"
)
NOTE_RELATIVE_PATH = "docs/leaky-outer-delay-word-stage3d-primitives.md"
TEST_RELATIVE_PATH = "tests/test_leaky_outer_delay_word_stage3d_primitives.py"
SOURCE_MANIFEST = (
    SOURCE_RELATIVE_PATH,
    GENERATOR_RELATIVE_PATH,
    NOTE_RELATIVE_PATH,
    "src/canard_control/directed_interval.py",
    "src/canard_control/leaky_outer_delay_word_stage3c_compression.py",
    "src/canard_control/leaky_outer_continuous_kernel_stage3_shard.py",
    "src/canard_control/leaky_outer_high_resolution.py",
    "src/canard_control/leaky_outer_phase_fixed_return_stage1.py",
    "src/canard_control/leaky_pulse_separator_candidate.py",
)
DEFAULT_COMMAND = (
    "OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONPATH=build/testdeps:src "
    "/usr/bin/python3 experiments/leaky_outer_delay_word_stage3d_primitives.py"
)
ARITHMETIC_SCOPE = (
    "exact finite-word/primitive algebra; source-bound DOP853 continuous-"
    "density guides and resolution comparison; 160-bit outward MPFR Wiener "
    "coefficient, orbit-residual, tangent, phase-projection and coarse "
    "logarithmic-growth arithmetic"
)

STAGE3C_RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_outer_delay_word_stage3c_compression.json"
)
STAGE3C_RESULT_SHA256 = (
    "5e3abaaccbc7a9c4aa4ded0f3ec785f48df67d5371c198066415159eab78979a"
)
STAGE2_RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_outer_signed_kernel_stage2.json"
)
STAGE2_RESULT_SHA256 = (
    "f4742db560c5de29072adfb0b963d5a21e993fed5a949a2180dcc6d0b355011f"
)
OUTER_RESULT_SHA256 = (
    "d888916fed919f1515dd31ab851b2229816ea373365fa0221b1e345580f165a7"
)
PULSE_ATTACHMENT_RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_pulse_outer_third_return_enclosure.json"
)
PULSE_ATTACHMENT_RESULT_SHA256 = (
    "7a01c2a8ec6b5421c090836f4962e595027d78be3381d490c4b6eb56d3beb13d"
)

PRECISION_BITS = 160
PINNED_OPENBLAS_NUM_THREADS = "1"
EXACT_ORBIT_RADIUS = "1e-8"
WORDS = ((), (0,), (1,), (0, 0), (0, 1), (1, 0), (1, 1))
PILOT_LEVELS = (
    ("coarse", "0.04", 61, 401),
    ("fine", "0.02", 121, 801),
)
COARSE_DIRECTED_PHASE_PARTITION = 512

TRUE_FLAGS = (
    "stage3c_finite_word_parent_validated",
    "all_words_have_length_at_most_two",
    "duffy_two_simplex_collapsed_to_one_dimensional_primitives",
    "one_word_primitive_identity_registered",
    "two_word_primitive_identity_registered",
    "cross_word_and_cross_injection_signed_sum_precedes_absolute_value",
    "continuous_center_density_pilot_uses_no_input_history_interpolation",
    "binary_primitive_resolution_ladder_recomputed",
    "binary_fundamental_inverse_consistency_recomputed",
    "exact_orbit_vector_field_tangent_transfer_validated",
    "continuous_linear_phase_projection_norm_validated",
    "phase_chart_continuous_transfer_error_validated",
    "linearized_ambient_projection_radius_gate_validated",
    "coarse_directed_logarithmic_growth_failure_recomputed",
    "directed_bernstein_frontier_registered",
)
FALSE_FLAGS = (
    "binary_primitive_pilot_promoted_to_exact_orbit_kernel",
    "duffy_primitive_guides_directedly_transferred_to_exact_F_H_L",
    "continuous_signed_density_total_variation_validated",
    "voltage_shadow_transfer_error_validated",
    "recovery_shadow_transfer_error_validated",
    "arbitrary_c0_linear_return_contraction_validated",
    "nonlinear_phase_chart_validated_on_ambient_tube",
    "outer_nonlinear_return_contraction_validated",
    "outer_quantitative_attracting_tube_validated",
    "outer_pulse_capture_validated",
    "physical_pulse_onset_validated",
)


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
        raise ValueError(f"{name} must be a mapping")
    return value


def _load_parent(repository: Path, relative: str, expected: str) -> Mapping[str, Any]:
    path = repository / relative
    if _sha256_path(path) != expected:
        raise ValueError(f"a Stage-3D parent changed: {relative}")
    return _mapping(json.loads(path.read_text()), relative)


def _binary64_record(value: float) -> dict[str, str]:
    number = float(value)
    if not math.isfinite(number):
        raise ValueError("a Stage-3D binary64 value is not finite")
    return {"binary64_hex": number.hex(), "decimal": format(number, ".17g")}


def _wiener_norm_upper(sequence: Mapping[int, Any]) -> gmpy2.mpfr:
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
        total = gmpy2.mpfr(0)
        for value in sequence.values():
            total += value.upper_abs()
        return total


@dataclass(frozen=True)
class PrimitivePilotLevel:
    level_id: str
    maximum_step_binary64: dict[str, str]
    output_time_node_count: int
    history_quadrature_node_count: int
    fundamental_nfev: int
    first_primitive_nfev: int
    second_primitive_nfev: int
    fundamental_inverse_consistency_max_binary64: dict[str, str]
    center_voltage_return_norm_binary64: dict[str, str]
    center_voltage_maximizing_relative_time_binary64: dict[str, str]
    center_recovery_return_norm_binary64: dict[str, str]
    continuous_history_density_evaluated_without_input_sampling: bool
    signed_sum_before_absolute_quadrature: bool
    diagnostic_only: bool


@dataclass(frozen=True)
class OuterDelayWordStage3DPrimitives:
    schema_id: str
    model_id: str
    branch: str
    arithmetic_scope: str
    precision_bits: int
    binary_blas_thread_count: int
    parent_result_sha256: dict[str, str]
    primitive_identity: dict[str, Any]
    pilot_levels: tuple[PrimitivePilotLevel, ...]
    pilot_cross_resolution: dict[str, str]
    continuous_phase_projection: dict[str, Any]
    coarse_directed_failure: dict[str, Any]
    directed_bernstein_frontier: dict[str, Any]
    transfer_errors: dict[str, str | None]
    transfer_gate: dict[str, Any]
    claim_status: dict[str, bool]
    conclusion: str


class _PrimitiveGuide:
    """Binary64 continuous guide for F, G, H_j and L_jk."""

    def __init__(self, orbit: Any, maximum_step: float):
        self.orbit = orbit
        self.period = float(orbit.period)
        self.taus = (float(TAU_0), float(TAU_1))
        self.voltage, self.voltage_derivative = _periodic_interpolator(
            orbit.state[:, 0], orbit.period
        )
        self.recovery, self.recovery_derivative = _periodic_interpolator(
            orbit.state[:, 1], orbit.period
        )

        initial = np.concatenate((np.eye(2).ravel(), np.eye(2).ravel()))
        self.fundamental_solution = solve_ivp(
            self._fundamental_rhs,
            (0.0, self.period),
            initial,
            method="DOP853",
            rtol=2.0e-12,
            atol=2.0e-14,
            max_step=maximum_step,
            dense_output=True,
        )
        if not self.fundamental_solution.success:
            raise ArithmeticError("the Stage-3D fundamental guide failed")
        self.first_solution = solve_ivp(
            self._first_rhs,
            (0.0, self.period),
            np.zeros(8, dtype=float),
            method="DOP853",
            rtol=2.0e-12,
            atol=2.0e-14,
            max_step=maximum_step / 2.0,
            dense_output=True,
        )
        if not self.first_solution.success:
            raise ArithmeticError("the Stage-3D first primitive guide failed")
        self.second_solution = solve_ivp(
            self._second_rhs,
            (0.0, self.period),
            np.zeros(16, dtype=float),
            method="DOP853",
            rtol=2.0e-12,
            atol=2.0e-14,
            max_step=maximum_step / 2.0,
            dense_output=True,
        )
        if not self.second_solution.success:
            raise ArithmeticError("the Stage-3D second primitive guide failed")

    def current_matrix(self, time: float) -> np.ndarray:
        voltage = self.voltage(time)
        coefficient = 1.0 - voltage * voltage - EPSILON * (
            KAPPA_1 + 3.0 * KAPPA_3 * (voltage - 1.0) ** 2
        )
        return np.asarray(
            ((coefficient, -1.0), (EPSILON, -EPSILON)), dtype=float
        )

    def delayed_scalar(self, delay_index: int, time: Any) -> Any:
        delay = self.taus[delay_index]
        if np.ndim(time) == 0:
            voltage = self.voltage(float(time) - delay)
            return 0.5 * EPSILON * (
                KAPPA_1 + 3.0 * KAPPA_3 * (voltage - 1.0) ** 2
            )
        values = np.asarray(time, dtype=float)
        voltage = np.asarray(
            [self.voltage(float(value) - delay) for value in values]
        )
        return 0.5 * EPSILON * (
            KAPPA_1 + 3.0 * KAPPA_3 * (voltage - 1.0) ** 2
        )

    def _fundamental_rhs(self, time: float, value: np.ndarray) -> np.ndarray:
        current = self.current_matrix(time)
        forward = value[:4].reshape(2, 2)
        inverse = value[4:].reshape(2, 2)
        return np.concatenate(
            ((current @ forward).ravel(), (-inverse @ current).ravel())
        )

    def F(self, time: Any) -> np.ndarray:
        values = np.asarray(time)
        raw = np.asarray(self.fundamental_solution.sol(time))
        if values.ndim == 0:
            return raw[:4].reshape(2, 2)
        return raw[:4].T.reshape(-1, 2, 2)

    def G(self, time: Any) -> np.ndarray:
        values = np.asarray(time)
        raw = np.asarray(self.fundamental_solution.sol(time))
        if values.ndim == 0:
            return raw[4:].reshape(2, 2)
        return raw[4:].T.reshape(-1, 2, 2)

    def C(self, delay_index: int, time: float) -> np.ndarray:
        delay = self.taus[delay_index]
        if time < delay:
            return np.zeros((2, 2), dtype=float)
        delayed = np.zeros((2, 2), dtype=float)
        delayed[0, 0] = self.delayed_scalar(delay_index, time)
        return self.G(time) @ delayed @ self.F(time - delay)

    def _first_rhs(self, time: float, _: np.ndarray) -> np.ndarray:
        return np.concatenate(
            tuple(self.C(index, time).ravel() for index in range(2))
        )

    def H(self, delay_index: int, time: Any) -> np.ndarray:
        values = np.asarray(time)
        raw = np.asarray(self.first_solution.sol(time))
        start = 4 * delay_index
        if values.ndim == 0:
            answer = raw[start : start + 4].reshape(2, 2)
            if float(time) <= self.taus[delay_index]:
                return np.zeros((2, 2), dtype=float)
            return answer
        answer = raw[start : start + 4].T.reshape(-1, 2, 2)
        answer[values <= self.taus[delay_index]] = 0.0
        return answer

    def _second_rhs(self, time: float, _: np.ndarray) -> np.ndarray:
        result = []
        for first in range(2):
            for second in range(2):
                if time < self.taus[first] + self.taus[second]:
                    value = np.zeros((2, 2), dtype=float)
                else:
                    value = self.C(first, time) @ self.H(
                        second, time - self.taus[first]
                    )
                result.append(value.ravel())
        return np.concatenate(tuple(result))

    def L(self, first: int, second: int, time: Any) -> np.ndarray:
        values = np.asarray(time)
        raw = np.asarray(self.second_solution.sol(time))
        start = 4 * (2 * first + second)
        threshold = self.taus[first] + self.taus[second]
        if values.ndim == 0:
            answer = raw[start : start + 4].reshape(2, 2)
            if float(time) <= threshold:
                return np.zeros((2, 2), dtype=float)
            return answer
        answer = raw[start : start + 4].T.reshape(-1, 2, 2)
        answer[values <= threshold] = 0.0
        return answer

    def word_integral(self, word: tuple[int, ...], time: float, start: np.ndarray) -> np.ndarray:
        start = np.asarray(start, dtype=float)
        count = len(start)
        if len(word) == 0:
            return np.broadcast_to(np.eye(2), (count, 2, 2)).copy()
        delay_sum = sum(self.taus[index] for index in word)
        active = time - start >= delay_sum - 2.0e-13
        answer = np.zeros((count, 2, 2), dtype=float)
        if len(word) == 1:
            first = word[0]
            values = self.H(first, time)[None, :, :] - self.H(
                first, start + self.taus[first]
            )
            answer[active] = values[active]
            return answer
        first, second = word
        lower = start + self.taus[first] + self.taus[second]
        first_difference = self.H(first, time)[None, :, :] - self.H(
            first, lower
        )
        product = np.einsum(
            "nij,njk->nik",
            first_difference,
            self.H(second, start + self.taus[second]),
        )
        values = (
            self.L(first, second, time)[None, :, :]
            - self.L(first, second, lower)
            - product
        )
        answer[active] = values[active]
        return answer

    def resolvent(self, time: float, start: np.ndarray) -> np.ndarray:
        start = np.asarray(start, dtype=float)
        middle = np.zeros((len(start), 2, 2), dtype=float)
        for word in WORDS:
            middle += self.word_integral(word, time, start)
        return np.einsum(
            "ij,njk,nkl->nil", self.F(time), middle, self.G(start)
        )

    def history_density(self, time: float, theta: np.ndarray) -> np.ndarray:
        theta = np.asarray(theta, dtype=float)
        result = np.zeros((len(theta), 2), dtype=float)
        for delay_index, delay in enumerate(self.taus):
            active = theta >= -delay - 2.0e-13
            if not np.any(active):
                continue
            start = theta[active] + delay
            resolvent = self.resolvent(time, start)
            scalar = self.delayed_scalar(delay_index, start)
            result[active] += resolvent[:, :, 0] * scalar[:, None]
        return result

    def scalar_column(self, time: float) -> np.ndarray:
        return self.resolvent(time, np.asarray([0.0]))[0, :, 1]

    def inverse_consistency(self) -> float:
        nodes = np.linspace(0.0, self.period, 1001)
        products = np.einsum("nij,njk->nik", self.F(nodes), self.G(nodes))
        return float(
            np.max(np.sum(np.abs(products - np.eye(2)[None, :, :]), axis=2))
        )


def _history_segments(total_nodes: int) -> tuple[np.ndarray, np.ndarray]:
    left_length = TAU_1 - TAU_0
    left_intervals = max(16, round((total_nodes - 2) * left_length / TAU_1))
    right_intervals = total_nodes - 2 - left_intervals
    return (
        np.linspace(-TAU_1, -TAU_0, left_intervals + 1),
        np.linspace(-TAU_0, 0.0, right_intervals + 1),
    )


def _primitive_pilot(
    orbit: Any,
    level_id: str,
    maximum_step: float,
    output_nodes: int,
    history_nodes: int,
) -> PrimitivePilotLevel:
    guide = _PrimitiveGuide(orbit, maximum_step)
    segments = _history_segments(history_nodes)
    density_at_period = tuple(
        guide.history_density(guide.period, theta) for theta in segments
    )
    scalar_at_period = guide.scalar_column(guide.period)
    phase_speed = guide.voltage_derivative(0.0)
    if phase_speed <= 0:
        raise ArithmeticError("the Stage-3D guide phase speed vanished")
    relative_times = np.linspace(-TAU_1, 0.0, output_nodes)
    voltage_rows = []
    for relative in relative_times:
        time = guide.period + relative
        tangent = np.asarray(
            (
                guide.voltage_derivative(relative),
                guide.recovery_derivative(relative),
            )
        )
        ratio = tangent / phase_speed
        row_mass = 0.0
        for theta, terminal_density in zip(
            segments, density_at_period, strict=True
        ):
            current = guide.history_density(time, theta)
            corrected = current - terminal_density[:, 0, None] * ratio[None, :]
            row_mass += float(np.trapezoid(np.abs(corrected[:, 0]), theta))
        scalar = guide.scalar_column(time) - ratio * scalar_at_period[0]
        voltage_rows.append(row_mass + abs(float(scalar[0])))
    maximum_index = int(np.argmax(voltage_rows))

    recovery_mass = 0.0
    recovery_ratio = guide.recovery_derivative(0.0) / phase_speed
    for theta, terminal_density in zip(segments, density_at_period, strict=True):
        corrected = terminal_density[:, 1] - recovery_ratio * terminal_density[:, 0]
        recovery_mass += float(np.trapezoid(np.abs(corrected), theta))
    recovery_scalar = scalar_at_period[1] - recovery_ratio * scalar_at_period[0]
    recovery_norm = recovery_mass + abs(float(recovery_scalar))
    return PrimitivePilotLevel(
        level_id=level_id,
        maximum_step_binary64=_binary64_record(maximum_step),
        output_time_node_count=output_nodes,
        history_quadrature_node_count=sum(len(value) for value in segments),
        fundamental_nfev=int(guide.fundamental_solution.nfev),
        first_primitive_nfev=int(guide.first_solution.nfev),
        second_primitive_nfev=int(guide.second_solution.nfev),
        fundamental_inverse_consistency_max_binary64=_binary64_record(
            guide.inverse_consistency()
        ),
        center_voltage_return_norm_binary64=_binary64_record(
            voltage_rows[maximum_index]
        ),
        center_voltage_maximizing_relative_time_binary64=_binary64_record(
            relative_times[maximum_index]
        ),
        center_recovery_return_norm_binary64=_binary64_record(recovery_norm),
        continuous_history_density_evaluated_without_input_sampling=True,
        signed_sum_before_absolute_quadrature=True,
        diagnostic_only=True,
    )


def _continuous_phase_projection(
    *,
    base: Any,
    stage2: Mapping[str, Any],
    attachment: Mapping[str, Any],
) -> dict[str, Any]:
    radius = DirectedInterval.from_decimal(
        EXACT_ORBIT_RADIUS, PRECISION_BITS
    ).upper
    epsilon = base.parameters["epsilon"]
    v_norm = _wiener_norm_upper(base.voltage)
    centered_norm = _wiener_norm_upper(base.centered_voltage)
    current_norm = _wiener_norm_upper(base.current_coefficient)
    delayed_norms = tuple(
        _wiener_norm_upper(value) for value in base.delayed_coefficients
    )
    residual_voltage = _wiener_norm_upper(base.residual_voltage)
    residual_recovery = _wiener_norm_upper(base.residual_recovery)
    phase_voltage = _wiener_norm_upper(base.phase_voltage)
    phase_recovery = _wiener_norm_upper(base.phase_recovery)
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
        current_variation = (
            (2 * v_norm + radius) * radius
            + 3
            * epsilon.upper
            * base.parameters["kappa_3"].upper
            * (2 * centered_norm + radius)
            * radius
        )
        delayed_variation = (
            3
            * epsilon.upper
            * base.parameters["kappa_3"].upper
            / 2
            * (2 * centered_norm + radius)
            * radius
        )
        fast_field_error = (
            current_norm
            + current_variation
            + delayed_norms[0]
            + delayed_norms[1]
            + 2 * delayed_variation
            + 1
        ) * radius + residual_voltage / base.period.lower
        slow_field_error = (
            2 * epsilon.upper * radius
            + residual_recovery / base.period.lower
        )
        guide_voltage_speed_norm = phase_voltage / base.period.lower
        guide_recovery_speed_norm = phase_recovery / base.period.lower
        exact_voltage_speed_norm = guide_voltage_speed_norm + fast_field_error
        exact_recovery_speed_norm = guide_recovery_speed_norm + slow_field_error

    zero = DirectedInterval.from_decimal(0, PRECISION_BITS)
    guide_phase_speed = _series_real_box(base.phase_voltage, zero) / base.period
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundDown):
        exact_phase_speed_lower = guide_phase_speed.lower - fast_field_error
    if exact_phase_speed_lower <= 0:
        raise ArithmeticError("the exact Stage-3D phase speed lost orientation")
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
        exact_speed_norm = max(
            exact_voltage_speed_norm, exact_recovery_speed_norm
        )
        projection_norm = 1 + exact_speed_norm / exact_phase_speed_lower

    stage2_certificate = _mapping(stage2.get("certificate"), "Stage-2 certificate")
    shadow = DirectedInterval.from_decimal(
        str(stage2_certificate["directed_phase_chart_shadow_norm_upper"]),
        PRECISION_BITS,
    ).upper
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
        transfer_error = max(gmpy2.mpfr(0), projection_norm - shadow)
    attachment_certificate = _mapping(
        attachment.get("certificate"), "pulse attachment certificate"
    )
    history_ball = _mapping(
        attachment_certificate.get("history_ball"), "attachment history ball"
    )
    distance = DirectedInterval.from_decimal(
        str(history_ball["complete_history_distance_upper"]), PRECISION_BITS
    ).upper
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
        projected_distance = projection_norm * distance
    section_radius = DirectedInterval.from_decimal(
        "0.0001", PRECISION_BITS
    ).lower
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundDown):
        radius_margin = section_radius - projected_distance
    if radius_margin <= 0:
        raise ArithmeticError("the Stage-3D linear phase projection gate failed")
    return {
        "norm": (
            "Y->Y norm of I-q tensor ell, ell(h)=h_v(0)/q_v(0); "
            "bounded by 1+max{sup|q_v|,sup|q_w|}/q_v(0)"
        ),
        "orbit_tangent_transfer": (
            "q_exact=f(X_exact); compare with Xbar'/Tbar by the validated "
            "periodic residual and a Wiener mean-value bound on the RFDE field"
        ),
        "guide_voltage_speed_wiener_upper": decimal_upper(
            guide_voltage_speed_norm, 60
        ),
        "guide_recovery_speed_wiener_upper": decimal_upper(
            guide_recovery_speed_norm, 60
        ),
        "fast_field_transfer_error_upper": decimal_upper(
            fast_field_error, 60
        ),
        "slow_field_transfer_error_upper": decimal_upper(
            slow_field_error, 60
        ),
        "guide_phase_speed_interval": {
            "lower": decimal_lower(guide_phase_speed.lower, 60),
            "upper": decimal_upper(guide_phase_speed.upper, 60),
        },
        "exact_phase_speed_lower": decimal_lower(exact_phase_speed_lower, 60),
        "continuous_projection_norm_upper": decimal_upper(projection_norm, 60),
        "stage2_phase_shadow_upper": decimal_upper(shadow, 60),
        "phase_chart_continuous_transfer_error_upper": decimal_upper(
            transfer_error, 60
        ),
        "ambient_complete_history_distance_upper": decimal_upper(distance, 60),
        "linear_projected_distance_upper": decimal_upper(projected_distance, 60),
        "declared_section_radius": "0.0001",
        "linear_projection_radius_margin_lower": decimal_lower(radius_margin, 60),
        "continuous_linear_phase_projection_validated": True,
        "nonlinear_phase_chart_on_ambient_tube_validated": False,
    }


def _coarse_directed_growth(base: Any) -> dict[str, Any]:
    radius = DirectedInterval.from_decimal(EXACT_ORBIT_RADIUS, PRECISION_BITS)
    exact_period = base.period + DirectedInterval.from_bounds(
        -radius.upper, radius.upper, PRECISION_BITS
    )
    count = COARSE_DIRECTED_PHASE_PARTITION
    with gmpy2.context(precision=PRECISION_BITS):
        exponent = gmpy2.mpfr(0)
    maximum_mu = gmpy2.mpfr(0)
    for index in range(count):
        phase = DirectedInterval.from_bounds(
            gmpy2.mpq(index, count), gmpy2.mpq(index + 1, count), PRECISION_BITS
        )
        voltage = _series_real_box(base.voltage, phase) + DirectedInterval.from_bounds(
            -radius.upper, radius.upper, PRECISION_BITS
        )
        current = _current_matrix(voltage, base.parameters)
        with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
            mu = max(current[0][0].upper + 1, gmpy2.mpfr(0))
            exponent += exact_period.upper / count * mu
        maximum_mu = max(maximum_mu, mu)
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
        growth = gmpy2.exp(exponent)
    return {
        "phase_partition_count": count,
        "maximum_mu_infinity_upper": decimal_upper(maximum_mu, 60),
        "accumulated_logarithmic_exponent_upper": decimal_upper(exponent, 60),
        "full_period_growth_upper": decimal_upper(growth, 60),
        "growth_exceeds_stage2_linear_margin": bool(growth > 1),
        "failure_reason": (
            "an absolute logarithmic-norm wrapper discards the signed phase "
            "and delay-word cancellation; it is rigorous but unusable"
        ),
        "not_used_as_transfer_error": True,
    }


@lru_cache(maxsize=1)
def _validated_orbit(repository_text: str, parent_sha256: str) -> Any:
    repository = Path(repository_text)
    path = repository / OUTER_RESULT_RELATIVE_PATH
    if _sha256_path(path) != parent_sha256:
        raise ValueError("the cached Stage-3D outer parent changed")
    return validate_outer_high_resolution_artifact(
        json.loads(path.read_text()), repository, replay_directed=False
    )


@lru_cache(maxsize=1)
def build_outer_delay_word_stage3d_primitives(
    repository: Path,
) -> OuterDelayWordStage3DPrimitives:
    repository = repository.resolve()
    if os.environ.get("OPENBLAS_NUM_THREADS") != PINNED_OPENBLAS_NUM_THREADS:
        raise RuntimeError("Stage-3D requires OPENBLAS_NUM_THREADS=1")
    stage3c = _load_parent(
        repository, STAGE3C_RESULT_RELATIVE_PATH, STAGE3C_RESULT_SHA256
    )
    stage2 = _load_parent(
        repository, STAGE2_RESULT_RELATIVE_PATH, STAGE2_RESULT_SHA256
    )
    _load_parent(repository, OUTER_RESULT_RELATIVE_PATH, OUTER_RESULT_SHA256)
    attachment = _load_parent(
        repository,
        PULSE_ATTACHMENT_RESULT_RELATIVE_PATH,
        PULSE_ATTACHMENT_RESULT_SHA256,
    )
    stage3c_certificate = _mapping(
        stage3c.get("certificate"), "Stage-3C certificate"
    )
    if stage3c_certificate.get("total_phase_fixed_word_term_count") != 21:
        raise ValueError("the Stage-3C 21-word representation changed")
    gap = _mapping(
        stage3c_certificate.get("minimum_remaining_gap"), "Stage-3C gap"
    )
    if gap.get("maximum_nested_integral_dimension") != 2:
        raise ValueError("the Stage-3C word depth changed")

    orbit = _validated_orbit(str(repository), OUTER_RESULT_SHA256)
    base = _build_leaky_base_sequences(orbit, PRECISION_BITS)
    pilots = tuple(
        _primitive_pilot(
            orbit,
            level_id,
            float(maximum_step),
            output_nodes,
            history_nodes,
        )
        for level_id, maximum_step, output_nodes, history_nodes in PILOT_LEVELS
    )
    coarse, fine = pilots
    voltage_difference = abs(
        float.fromhex(fine.center_voltage_return_norm_binary64["binary64_hex"])
        - float.fromhex(coarse.center_voltage_return_norm_binary64["binary64_hex"])
    )
    recovery_difference = abs(
        float.fromhex(fine.center_recovery_return_norm_binary64["binary64_hex"])
        - float.fromhex(coarse.center_recovery_return_norm_binary64["binary64_hex"])
    )
    phase = _continuous_phase_projection(
        base=base, stage2=stage2, attachment=attachment
    )
    failure = _coarse_directed_growth(base)
    stage2_certificate = _mapping(stage2.get("certificate"), "Stage-2 certificate")
    qv = DirectedInterval.from_decimal(
        str(stage2_certificate["directed_voltage_shadow_norm_upper"]),
        PRECISION_BITS,
    ).upper
    qw = DirectedInterval.from_decimal(
        str(stage2_certificate["directed_recovery_shadow_norm_upper"]),
        PRECISION_BITS,
    ).upper
    claims = {name: True for name in TRUE_FLAGS}
    claims.update({name: False for name in FALSE_FLAGS})
    return OuterDelayWordStage3DPrimitives(
        schema_id=SCHEMA_ID,
        model_id=MODEL_ID,
        branch=BRANCH,
        arithmetic_scope=ARITHMETIC_SCOPE,
        precision_bits=PRECISION_BITS,
        binary_blas_thread_count=1,
        parent_result_sha256={
            STAGE3C_RESULT_RELATIVE_PATH: STAGE3C_RESULT_SHA256,
            STAGE2_RESULT_RELATIVE_PATH: STAGE2_RESULT_SHA256,
            OUTER_RESULT_RELATIVE_PATH: OUTER_RESULT_SHA256,
            PULSE_ATTACHMENT_RESULT_RELATIVE_PATH: (
                PULSE_ATTACHMENT_RESULT_SHA256
            ),
        },
        primitive_identity={
            "fundamental": "F'=A F, F(0)=I, G=F^{-1}",
            "conjugated_delay": "C_j(r)=G(r) B_j(r) F(r-tau_j)",
            "first_primitive": "H_j'=C_j, H_j(t)=0 for t<=tau_j",
            "second_primitive": (
                "L_jk'=C_j(r) H_k(r-tau_j), "
                "L_jk(t)=0 for t<=tau_j+tau_k"
            ),
            "empty_word": "R_empty(t,s)=F(t)G(s)",
            "one_word": (
                "R_j(t,s)=F(t)[H_j(t)-H_j(s+tau_j)]G(s)"
            ),
            "two_word": (
                "R_jk(t,s)=F(t){L_jk(t)-L_jk(a)-"
                "[H_j(t)-H_j(a)]H_k(s+tau_k)}G(s), "
                "a=s+tau_j+tau_k"
            ),
            "duffy_reduction": (
                "the ordered two-simplex is integrated exactly by H and L; "
                "only one-dimensional primitive ODEs remain"
            ),
            "signed_ordering": (
                "sum all seven words and both history injections, subtract "
                "the phase row, and only then integrate absolute value"
            ),
            "maximum_primitive_delay_depth": 2,
        },
        pilot_levels=pilots,
        pilot_cross_resolution={
            "voltage_norm_absolute_difference_binary64": _binary64_record(
                voltage_difference
            )["decimal"],
            "recovery_norm_absolute_difference_binary64": _binary64_record(
                recovery_difference
            )["decimal"],
            "status": "binary64 diagnostic only; not a directed error bound",
        },
        continuous_phase_projection=phase,
        coarse_directed_failure=failure,
        directed_bernstein_frontier={
            "validated_algebra": (
                "Duffy word integrals reduced to the F,G,H,L primitive "
                "identities before any interval absolute value"
            ),
            "requested_partition_ladder": [256, 512, 1024],
            "requested_taylor_bernstein_degree_ladder": [12, 16, 20, 24],
            "current_reached_partition": COARSE_DIRECTED_PHASE_PARTITION,
            "current_reached_degree": 0,
            "first_unvalidated_object": (
                "piecewise polynomial relative-residual enclosure for F and "
                "the induced triangular H_j,L_jk primitives on the exact "
                "1e-8 orbit ball"
            ),
            "required_correlation": (
                "retain F(t){sum_word I_word(t,s)}G(s) and phase subtraction "
                "as one tensor polynomial; separate word norms are forbidden"
            ),
            "voltage_error_target": (
                "E_voltage < 0.8730921051856016985675559066"
            ),
            "recovery_error_target": (
                "E_recovery < 0.9972399927438704453544963998"
            ),
            "failure_is_numerical_not_structural": True,
        },
        transfer_errors={
            "E_voltage": None,
            "E_recovery": None,
            "E_phase": phase["phase_chart_continuous_transfer_error_upper"],
        },
        transfer_gate={
            "continuous_voltage_row_norm_upper": None,
            "continuous_recovery_row_norm_upper": None,
            "continuous_phase_projection_norm_upper": phase[
                "continuous_projection_norm_upper"
            ],
            "stage2_voltage_shadow_upper": decimal_upper(qv, 60),
            "stage2_recovery_shadow_upper": decimal_upper(qw, 60),
            "linear_return_gate_evaluated": False,
            "arbitrary_c0_linear_contraction_closes": False,
            "linearized_ambient_projection_gate_closes": True,
            "nonlinear_ambient_phase_chart_gate_closes": False,
        },
        claim_status=claims,
        conclusion=(
            "the 21 Duffy word terms collapse exactly to one-dimensional F,G,H,L "
            "primitives and an independent continuous phase-projection bound "
            "now supplies E_phase; the center continuous-density pilot agrees "
            "with Stage-2, but exact-orbit Bernstein residuals for the signed "
            "F-H-L tensor remain absent, so E_voltage,E_recovery and C0 "
            "contraction remain open"
        ),
    )


def build_outer_delay_word_stage3d_primitives_result(
    repository: Path,
) -> dict[str, Any]:
    repository = repository.resolve()
    certificate = json.loads(
        json.dumps(
            asdict(build_outer_delay_word_stage3d_primitives(repository)),
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        )
    )
    return {
        "certificate": certificate,
        "manifest": {
            "schema_id": SCHEMA_ID,
            "result": RESULT_RELATIVE_PATH,
            "default_command": DEFAULT_COMMAND,
            "certificate_sha256": canonical_sha256(certificate),
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
                "mpfr": gmpy2.mpfr_version(),
                "openblas_num_threads": os.environ.get("OPENBLAS_NUM_THREADS"),
            },
        },
    }


def validate_outer_delay_word_stage3d_primitives_result(
    payload: Mapping[str, Any], repository: Path
) -> None:
    if not isinstance(payload, Mapping) or set(payload) != {"certificate", "manifest"}:
        raise ValueError("the Stage-3D schema changed")
    certificate = _mapping(payload.get("certificate"), "Stage-3D certificate")
    manifest = _mapping(payload.get("manifest"), "Stage-3D manifest")
    if set(certificate) != {
        field.name for field in fields(OuterDelayWordStage3DPrimitives)
    }:
        raise ValueError("the Stage-3D certificate fields changed")
    if manifest.get("schema_id") != SCHEMA_ID:
        raise ValueError("the Stage-3D manifest schema changed")
    if manifest.get("result") != RESULT_RELATIVE_PATH:
        raise ValueError("the Stage-3D result path changed")
    if canonical_sha256(certificate) != manifest.get("certificate_sha256"):
        raise ValueError("the Stage-3D certificate digest changed")
    sources = _mapping(manifest.get("source_sha256"), "Stage-3D source manifest")
    if set(sources) != set(SOURCE_MANIFEST):
        raise ValueError("the Stage-3D source set changed")
    repository = repository.resolve()
    for relative in SOURCE_MANIFEST:
        if sources.get(relative) != _sha256_path(repository / relative):
            raise ValueError(f"a Stage-3D source changed: {relative}")
    claims = _mapping(certificate.get("claim_status"), "Stage-3D claim ledger")
    if set(claims) != set(TRUE_FLAGS + FALSE_FLAGS):
        raise ValueError("the Stage-3D claim ledger changed")
    if any(claims.get(name) is not True for name in TRUE_FLAGS):
        raise ValueError("a proved Stage-3D fact was weakened")
    if any(claims.get(name) is not False for name in FALSE_FLAGS):
        raise ValueError("an open Stage-3D claim was promoted")
    identity = _mapping(certificate.get("primitive_identity"), "primitive identity")
    if identity.get("maximum_primitive_delay_depth") != 2:
        raise ValueError("the Stage-3D primitive depth changed")
    pilots = certificate.get("pilot_levels")
    if not isinstance(pilots, list) or [row.get("level_id") for row in pilots] != [
        "coarse",
        "fine",
    ]:
        raise ValueError("the Stage-3D primitive ladder changed")
    for row in pilots:
        if row.get("diagnostic_only") is not True:
            raise ValueError("a Stage-3D binary pilot was promoted")
        if row.get("continuous_history_density_evaluated_without_input_sampling") is not True:
            raise ValueError("the Stage-3D continuous density guide changed")
        if row.get("signed_sum_before_absolute_quadrature") is not True:
            raise ValueError("the Stage-3D signed ordering changed")
        inverse_error = float.fromhex(
            row["fundamental_inverse_consistency_max_binary64"]["binary64_hex"]
        )
        if not 0 <= inverse_error < 1.0e-6:
            raise ValueError("the Stage-3D guide inverse consistency changed")
    phase = _mapping(
        certificate.get("continuous_phase_projection"), "phase projection"
    )
    if phase.get("continuous_linear_phase_projection_validated") is not True:
        raise ValueError("the Stage-3D continuous phase projection vanished")
    if phase.get("nonlinear_phase_chart_on_ambient_tube_validated") is not False:
        raise ValueError("the Stage-3D nonlinear phase chart was invented")
    if gmpy2.mpq(str(phase["exact_phase_speed_lower"])) <= 0:
        raise ValueError("the Stage-3D exact phase speed vanished")
    if gmpy2.mpq(str(phase["linear_projection_radius_margin_lower"])) <= 0:
        raise ValueError("the Stage-3D linear projection radius margin vanished")
    transfer = _mapping(certificate.get("transfer_errors"), "Stage-3D transfer")
    if transfer.get("E_voltage") is not None or transfer.get("E_recovery") is not None:
        raise ValueError("a Stage-3D density transfer error was invented")
    if transfer.get("E_phase") != phase.get(
        "phase_chart_continuous_transfer_error_upper"
    ):
        raise ValueError("the Stage-3D phase transfer error changed")
    gate = _mapping(certificate.get("transfer_gate"), "Stage-3D gate")
    if gate.get("linear_return_gate_evaluated") is not False:
        raise ValueError("the Stage-3D linear return gate was promoted")
    if gate.get("arbitrary_c0_linear_contraction_closes") is not False:
        raise ValueError("the Stage-3D C0 contraction was promoted")
    if gate.get("linearized_ambient_projection_gate_closes") is not True:
        raise ValueError("the Stage-3D linear ambient gate vanished")
    if gate.get("nonlinear_ambient_phase_chart_gate_closes") is not False:
        raise ValueError("the Stage-3D nonlinear ambient gate was promoted")
    failure = _mapping(
        certificate.get("coarse_directed_failure"), "Stage-3D failure"
    )
    if failure.get("not_used_as_transfer_error") is not True:
        raise ValueError("the Stage-3D coarse growth was promoted")
    if gmpy2.mpq(str(failure["full_period_growth_upper"])) <= 1:
        raise ValueError("the Stage-3D coarse failure disappeared")
    expected = json.loads(
        json.dumps(
            asdict(build_outer_delay_word_stage3d_primitives(repository)),
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        )
    )
    if certificate != expected:
        raise ValueError("the Stage-3D certificate differs from replay")


__all__ = [
    "DEFAULT_COMMAND",
    "FALSE_FLAGS",
    "NOTE_RELATIVE_PATH",
    "RESULT_RELATIVE_PATH",
    "SOURCE_MANIFEST",
    "TRUE_FLAGS",
    "build_outer_delay_word_stage3d_primitives",
    "build_outer_delay_word_stage3d_primitives_result",
    "canonical_sha256",
    "validate_outer_delay_word_stage3d_primitives_result",
]
