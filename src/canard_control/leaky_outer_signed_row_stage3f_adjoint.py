"""Stage-3F direct signed-row adjoint and Green-budget certificate.

The cancellation-blind H/L bounds of Stage 3E are intentionally abandoned.
For one phase-corrected output evaluation, put

    p(u) = r_t R(t,u) 1_{u<=t} - alpha e_v^T R(T,u).

Away from its terminal jumps this *single combined row* satisfies the
advanced equation

    -p'(u) = p(u) A(u) + sum_j p(u+tau_j) B_j(u+tau_j).

The input-history density is then

    k(theta) = sum_j p(theta+tau_j) B_j(theta+tau_j) e_v,

and the independent recovery atom is ``p(0)e_w``.  Thus all seven delay
words, both history injections, and phase subtraction have already been
summed before any row total variation is considered.

This stage proves the algebra, exact coefficient/phase-ratio defect budgets,
and a strict instantaneous Green bound obtained from the Stage-3E F/G
polynomial charts.  It also computes a source-bound binary64 center pilot for
the full advanced rows.  The delayed part of the advanced Green bound and a
Bernstein tensor residual for p are not yet proved, so E_voltage and
E_recovery remain null.
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
from typing import Any, Mapping

import gmpy2
import numpy as np
import scipy

from canard_control.directed_interval import (
    DirectedInterval,
    decimal_lower,
    decimal_upper,
    pi_interval,
)
from canard_control.leaky_outer_delay_word_stage3d_primitives import (
    RESULT_RELATIVE_PATH as STAGE3D_RESULT_RELATIVE_PATH,
    _PrimitiveGuide,
)
from canard_control.leaky_outer_delay_word_stage3e_relative_residual import (
    FUNDAMENTAL_DEGREE,
    PHASE_CELL_COUNT,
    PRECISION_BITS,
    RESULT_RELATIVE_PATH as STAGE3E_RESULT_RELATIVE_PATH,
    _FundamentalGuide,
    _cell_coefficient_polynomial,
    _centered_polynomial_lower_abs,
    _determinant_polynomial,
    _guide_polynomial,
    _integrated_polynomial_matrix_inf_norm_upper,
    _matrix_adjugate,
)
from canard_control.leaky_outer_high_resolution import (
    RESULT_RELATIVE_PATH as OUTER_RESULT_RELATIVE_PATH,
    validate_outer_high_resolution_artifact,
)
from canard_control.leaky_outer_signed_kernel_stage2 import (
    RESULT_RELATIVE_PATH as STAGE2_RESULT_RELATIVE_PATH,
)
from canard_control.leaky_periodic_validation import _build_leaky_base_sequences


SCHEMA_ID = "leaky-outer-signed-row-stage3f-adjoint-v1"
MODEL_ID = "autonomous-leaky-recovery-two-delay-fhn-bistable-proposal"
BRANCH = "outer_pulse"
SOURCE_RELATIVE_PATH = "src/canard_control/leaky_outer_signed_row_stage3f_adjoint.py"
GENERATOR_RELATIVE_PATH = "experiments/leaky_outer_signed_row_stage3f_adjoint.py"
RESULT_RELATIVE_PATH = "experiments/results/leaky_outer_signed_row_stage3f_adjoint.json"
NOTE_RELATIVE_PATH = "docs/leaky-outer-signed-row-stage3f-adjoint.md"
TEST_RELATIVE_PATH = "tests/test_leaky_outer_signed_row_stage3f_adjoint.py"
SOURCE_MANIFEST = (
    SOURCE_RELATIVE_PATH,
    GENERATOR_RELATIVE_PATH,
    NOTE_RELATIVE_PATH,
    "src/canard_control/directed_interval.py",
    "src/canard_control/leaky_outer_delay_word_stage3d_primitives.py",
    "src/canard_control/leaky_outer_delay_word_stage3e_relative_residual.py",
    "src/canard_control/leaky_outer_high_resolution.py",
    "src/canard_control/leaky_outer_signed_kernel_stage2.py",
    "src/canard_control/leaky_periodic_validation.py",
)
DEFAULT_COMMAND = (
    "OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONPATH=build/testdeps:src "
    "/usr/bin/python3 experiments/leaky_outer_signed_row_stage3f_adjoint.py"
)
ARITHMETIC_SCOPE = (
    "exact advanced-row/kernel identities; 160-bit outward MPFR reuse and "
    "replay of the 1024-cell degree-24 F/G charts; exact orbit, period, "
    "delayed-coefficient and phase-ratio defect budgets; source-bound "
    "binary64 full-DDE adjoint/Green diagnostics kept nonclaim"
)

STAGE3E_RESULT_SHA256 = (
    "ffc8382c22422af711a0e4517d6ea0b9a7f474ffcaa1fb10a4120136d3002391"
)
STAGE3D_RESULT_SHA256 = (
    "11197f7f64289bd239f6167deedae66e54bc7805eaf84d08762ddc843c7372bf"
)
STAGE2_RESULT_SHA256 = (
    "f4742db560c5de29072adfb0b963d5a21e993fed5a949a2180dcc6d0b355011f"
)
OUTER_RESULT_SHA256 = (
    "d888916fed919f1515dd31ab851b2229816ea373365fa0221b1e345580f165a7"
)
PINNED_OPENBLAS_NUM_THREADS = "1"
EXACT_ORBIT_RADIUS = "1e-8"
DIAGNOSTIC_OUTPUT_COUNT = 65
DIAGNOSTIC_ADJOINT_NODE_COUNT = 2001
FULL_ADVANCED_GREEN_TARGET = "60000"
FULL_ADVANCED_BOUNDARY_TARGET = "70000"
CENTER_TV_RESERVE = "0.01"

TRUE_FLAGS = (
    "stage3e_F_G_parent_digest_validated",
    "stage3d_phase_and_primitive_parent_digest_validated",
    "advanced_combined_row_identity_registered",
    "all_delay_words_combined_inside_advanced_row",
    "both_history_injections_combined_before_total_variation",
    "phase_subtraction_combined_before_total_variation",
    "history_density_recovered_from_combined_row",
    "recovery_atom_recovered_from_combined_row",
    "current_voltage_dirac_killed_on_linear_phase_section",
    "strict_instantaneous_green_integral_bound_validated",
    "strict_instantaneous_boundary_bound_validated",
    "exact_coefficient_defect_budget_validated",
    "exact_phase_ratio_transfer_bound_validated",
    "full_advanced_residual_targets_computed",
    "binary_center_signed_row_pilot_recomputed",
)
FALSE_FLAGS = (
    "binary_center_signed_row_pilot_promoted_to_exact_kernel",
    "delayed_advanced_green_integral_bound_validated",
    "delayed_advanced_boundary_bound_validated",
    "combined_row_bernstein_tensor_residual_validated",
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
        raise ValueError(f"a Stage-3F parent changed: {relative}")
    return _mapping(json.loads(path.read_text()), relative)


def _wiener_norm_upper(sequence: Mapping[int, Any]) -> gmpy2.mpfr:
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
        total = gmpy2.mpfr(0)
        for value in sequence.values():
            total += value.upper_abs()
    return total


def _derivative_wiener_norm_upper(sequence: Mapping[int, Any]) -> gmpy2.mpfr:
    pi = pi_interval(PRECISION_BITS)
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
        total = gmpy2.mpfr(0)
        for mode, value in sequence.items():
            total += 2 * pi.upper * abs(mode) * value.upper_abs()
    return total


@dataclass(frozen=True)
class InstantaneousGreenCertificate:
    phase_cell_count: int
    fundamental_polynomial_degree: int
    Fhat_uniform_upper: str
    Ghat_uniform_upper: str
    Ghat_phase_integral_upper: str
    F_exact_uniform_upper: str
    G_exact_uniform_upper: str
    G_exact_phase_integral_upper: str
    instantaneous_green_phase_integral_upper: str
    instantaneous_boundary_propagator_upper: str
    minimum_replayed_determinant_abs_lower: str
    delayed_green_part_included: bool
    directed_polynomial_replay_validated: bool


@dataclass(frozen=True)
class OuterSignedRowStage3FAdjoint:
    schema_id: str
    model_id: str
    branch: str
    arithmetic_scope: str
    precision_bits: int
    binary_blas_thread_count: int
    parent_result_sha256: dict[str, str]
    combined_advanced_row_identity: dict[str, Any]
    instantaneous_green: InstantaneousGreenCertificate
    exact_defect_budget: dict[str, Any]
    center_signed_row_diagnostic: dict[str, Any]
    residual_closure_targets: dict[str, Any]
    transfer_errors: dict[str, str | None]
    transfer_gate: dict[str, Any]
    claim_status: dict[str, bool]
    conclusion: str


def _strict_instantaneous_green(
    base: Any,
    orbit: Any,
    stage3e_certificate: Mapping[str, Any],
) -> InstantaneousGreenCertificate:
    fundamental = _mapping(
        stage3e_certificate.get("fundamental_certificate"),
        "Stage-3E fundamental certificate",
    )
    fhat = DirectedInterval.from_decimal(
        str(fundamental["maximum_Fhat_inf_norm_upper"]), PRECISION_BITS
    ).upper
    ghat = DirectedInterval.from_decimal(
        str(fundamental["maximum_Ghat_inf_norm_upper"]), PRECISION_BITS
    ).upper
    f_error = DirectedInterval.from_decimal(
        str(fundamental["F_right_relative_error_upper"]), PRECISION_BITS
    ).upper
    g_error = DirectedInterval.from_decimal(
        str(fundamental["G_left_relative_error_upper"]), PRECISION_BITS
    ).upper
    guide = _FundamentalGuide(orbit)
    ghat_integral = gmpy2.mpfr(0, precision=PRECISION_BITS)
    minimum_determinant: gmpy2.mpfr | None = None
    for cell in range(PHASE_CELL_COUNT):
        coefficient = _cell_coefficient_polynomial(base, cell)
        polynomial = _guide_polynomial(guide, coefficient, cell)
        determinant = _determinant_polynomial(polynomial)
        determinant_lower = _centered_polynomial_lower_abs(determinant)
        if determinant_lower <= 0:
            raise ArithmeticError(
                f"the Stage-3F F chart is singular on phase cell {cell}"
            )
        minimum_determinant = (
            determinant_lower
            if minimum_determinant is None
            else min(minimum_determinant, determinant_lower)
        )
        adjugate = tuple(_matrix_adjugate(value) for value in polynomial)
        integrated = _integrated_polynomial_matrix_inf_norm_upper(adjugate)
        with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
            ghat_integral += (
                integrated / (2 * PHASE_CELL_COUNT * determinant_lower)
            )
    if minimum_determinant is None:
        raise AssertionError("the Stage-3F phase cover is empty")
    registered_minimum = DirectedInterval.from_decimal(
        str(fundamental["minimum_polynomial_determinant_abs_lower"]),
        PRECISION_BITS,
    ).lower
    if minimum_determinant < registered_minimum:
        raise ArithmeticError("the Stage-3E determinant replay weakened")
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
        f_exact = fhat * (1 + f_error)
        g_exact = ghat * (1 + g_error)
        g_exact_integral = ghat_integral * (1 + g_error)
        green = f_exact * g_exact_integral
        boundary = f_exact * g_exact
    return InstantaneousGreenCertificate(
        phase_cell_count=PHASE_CELL_COUNT,
        fundamental_polynomial_degree=FUNDAMENTAL_DEGREE,
        Fhat_uniform_upper=decimal_upper(fhat, 60),
        Ghat_uniform_upper=decimal_upper(ghat, 60),
        Ghat_phase_integral_upper=decimal_upper(ghat_integral, 60),
        F_exact_uniform_upper=decimal_upper(f_exact, 60),
        G_exact_uniform_upper=decimal_upper(g_exact, 60),
        G_exact_phase_integral_upper=decimal_upper(g_exact_integral, 60),
        instantaneous_green_phase_integral_upper=decimal_upper(green, 60),
        instantaneous_boundary_propagator_upper=decimal_upper(boundary, 60),
        minimum_replayed_determinant_abs_lower=decimal_lower(
            minimum_determinant, 60
        ),
        delayed_green_part_included=False,
        directed_polynomial_replay_validated=True,
    )


def _phase_ratio_errors(stage3d_certificate: Mapping[str, Any]) -> dict[str, gmpy2.mpfr]:
    phase = _mapping(
        stage3d_certificate.get("continuous_phase_projection"),
        "Stage-3D phase projection",
    )
    q0 = DirectedInterval.from_decimal(
        str(phase["guide_phase_speed_interval"]["lower"]), PRECISION_BITS
    ).lower
    exact_q0 = DirectedInterval.from_decimal(
        str(phase["exact_phase_speed_lower"]), PRECISION_BITS
    ).lower
    fast = DirectedInterval.from_decimal(
        str(phase["fast_field_transfer_error_upper"]), PRECISION_BITS
    ).upper
    slow = DirectedInterval.from_decimal(
        str(phase["slow_field_transfer_error_upper"]), PRECISION_BITS
    ).upper
    qv = DirectedInterval.from_decimal(
        str(phase["guide_voltage_speed_wiener_upper"]), PRECISION_BITS
    ).upper
    qw = DirectedInterval.from_decimal(
        str(phase["guide_recovery_speed_wiener_upper"]), PRECISION_BITS
    ).upper
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
        voltage = fast / exact_q0 + qv * fast / (exact_q0 * q0)
        recovery = slow / exact_q0 + qw * fast / (exact_q0 * q0)
    return {"voltage": voltage, "recovery": recovery}


def _exact_defect_budget(
    base: Any,
    stage3e_certificate: Mapping[str, Any],
    stage3d_certificate: Mapping[str, Any],
) -> dict[str, Any]:
    fundamental = _mapping(
        stage3e_certificate.get("fundamental_certificate"),
        "Stage-3E fundamental certificate",
    )
    radius = DirectedInterval.from_decimal(EXACT_ORBIT_RADIUS, PRECISION_BITS).upper
    current_variation = DirectedInterval.from_decimal(
        str(fundamental["exact_orbit_coefficient_variation_upper"]),
        PRECISION_BITS,
    ).upper
    period_matrix = DirectedInterval.from_decimal(
        str(fundamental["exact_period_matrix_variation_upper"]),
        PRECISION_BITS,
    ).upper
    centered_norm = _wiener_norm_upper(base.centered_voltage)
    b_hat = max(_wiener_norm_upper(value) for value in base.delayed_coefficients)
    b_derivative = max(
        _derivative_wiener_norm_upper(value)
        for value in base.delayed_coefficients
    )
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
        b_orbit = (
            3
            * base.parameters["epsilon"].upper
            * base.parameters["kappa_3"].upper
            / 2
            * (2 * centered_norm + radius)
            * radius
        )
        exact_period_lower = base.period.lower - radius
        maximum_delay = max(
            base.parameters["tau_0"].upper,
            base.parameters["tau_1"].upper,
        )
        delay_phase_shift = (
            maximum_delay
            * radius
            / (exact_period_lower * base.period.lower)
        )
        b_shift = b_derivative * delay_phase_shift
        b_physical_variation = b_orbit + b_shift
        b_matrix_variation = (
            (base.period.upper + radius) * b_physical_variation
            + radius * b_hat
        )
        current_matrix_variation = (
            (base.period.upper + radius) * current_variation + period_matrix
        )
        rank_one_variation = (
            (base.period.upper + radius) * current_variation
            + 2 * b_matrix_variation
        )
        full_operator_variation = rank_one_variation + period_matrix
        b_exact = b_hat + b_physical_variation
        history_lift = 1 + (
            base.parameters["tau_0"].upper
            + base.parameters["tau_1"].upper
        ) * b_exact
        delay_sum = (
            base.parameters["tau_0"].upper
            + base.parameters["tau_1"].upper
        )
    ratios = _phase_ratio_errors(stage3d_certificate)
    return {
        "normalization": "normalized phase x in [0,1]",
        "current_physical_coefficient_variation_upper": decimal_upper(
            current_variation, 60
        ),
        "current_normalized_matrix_variation_upper": decimal_upper(
            current_matrix_variation, 60
        ),
        "center_delayed_coefficient_upper": decimal_upper(b_hat, 60),
        "delayed_orbit_variation_upper": decimal_upper(b_orbit, 60),
        "delay_phase_shift_upper": decimal_upper(delay_phase_shift, 60),
        "delayed_shift_variation_upper": decimal_upper(b_shift, 60),
        "delayed_physical_coefficient_variation_upper": decimal_upper(
            b_physical_variation, 60
        ),
        "one_delayed_normalized_matrix_variation_upper": decimal_upper(
            b_matrix_variation, 60
        ),
        "full_advanced_operator_variation_upper": decimal_upper(
            full_operator_variation, 60
        ),
        "rank_one_advanced_operator_variation_upper": decimal_upper(
            rank_one_variation, 60
        ),
        "full_period_matrix_variation_upper": decimal_upper(
            period_matrix, 60
        ),
        "exact_history_density_lift_factor_upper": decimal_upper(
            history_lift, 60
        ),
        "delay_sum_upper": decimal_upper(delay_sum, 60),
        "voltage_phase_ratio_transfer_error_upper": decimal_upper(
            ratios["voltage"], 60
        ),
        "recovery_phase_ratio_transfer_error_upper": decimal_upper(
            ratios["recovery"], 60
        ),
        "coefficient_defect_budget_validated": True,
        "phase_ratio_transfer_validated": True,
    }


def _binary_record(value: float) -> dict[str, str]:
    number = float(value)
    if not math.isfinite(number):
        raise ValueError("a Stage-3F binary64 diagnostic is not finite")
    return {"binary64_hex": number.hex(), "decimal": format(number, ".17g")}


def _center_diagnostic(orbit: Any, stage3d_certificate: Mapping[str, Any]) -> dict[str, Any]:
    guide = _PrimitiveGuide(orbit, 0.04)
    period = guide.period
    phase_speed = guide.voltage_derivative(0.0)
    nodes = np.linspace(0.0, period, DIAGNOSTIC_ADJOINT_NODE_COUNT)
    terminal = guide.resolvent(period, nodes)
    output_times = np.linspace(
        period - guide.taus[1], period, DIAGNOSTIC_OUTPUT_COUNT
    )
    maximum_green = 0.0
    maximum_boundary = 0.0
    maximum_voltage_p = 0.0
    maximum_voltage_p_voltage_component = 0.0
    maximum_voltage_p_integral = 0.0
    maximizing_time = output_times[0]
    for time in output_times:
        active = nodes <= time + 2.0e-13
        current = np.zeros_like(terminal)
        current[active] = guide.resolvent(time, nodes[active])
        norm = np.max(np.sum(np.abs(current[active]), axis=2), axis=1)
        maximum_green = max(
            maximum_green, float(np.trapezoid(norm, nodes[active]) / period)
        )
        maximum_boundary = max(maximum_boundary, float(np.max(norm)))
        relative = time - period
        alpha = guide.voltage_derivative(relative) / phase_speed
        combined = current[:, 0, :] - alpha * terminal[:, 0, :]
        combined_norm = np.sum(np.abs(combined), axis=1)
        maximum_voltage_p_voltage_component = max(
            maximum_voltage_p_voltage_component,
            float(np.max(np.abs(combined[:, 0]))),
        )
        current_maximum = float(np.max(combined_norm))
        if current_maximum > maximum_voltage_p:
            maximum_voltage_p = current_maximum
            maximizing_time = time
        maximum_voltage_p_integral = max(
            maximum_voltage_p_integral,
            float(np.trapezoid(combined_norm, nodes) / period),
        )
    recovery_alpha = guide.recovery_derivative(0.0) / phase_speed
    recovery = terminal[:, 1, :] - recovery_alpha * terminal[:, 0, :]
    recovery_norm = np.sum(np.abs(recovery), axis=1)
    pilot = stage3d_certificate.get("pilot_levels")
    if not isinstance(pilot, list) or len(pilot) != 2:
        raise ValueError("the Stage-3D pilot ladder changed")
    fine = _mapping(pilot[-1], "Stage-3D fine pilot")
    return {
        "output_time_count": DIAGNOSTIC_OUTPUT_COUNT,
        "adjoint_node_count": DIAGNOSTIC_ADJOINT_NODE_COUNT,
        "full_DDE_green_phase_integral_max_binary64": _binary_record(
            maximum_green
        ),
        "full_DDE_boundary_propagator_max_binary64": _binary_record(
            maximum_boundary
        ),
        "voltage_combined_p_uniform_max_binary64": _binary_record(
            maximum_voltage_p
        ),
        "voltage_combined_p_voltage_component_max_binary64": _binary_record(
            maximum_voltage_p_voltage_component
        ),
        "voltage_combined_p_phase_integral_max_binary64": _binary_record(
            maximum_voltage_p_integral
        ),
        "voltage_p_maximizing_relative_time_binary64": _binary_record(
            maximizing_time - period
        ),
        "recovery_combined_p_uniform_max_binary64": _binary_record(
            float(np.max(recovery_norm))
        ),
        "recovery_combined_p_voltage_component_max_binary64": _binary_record(
            float(np.max(np.abs(recovery[:, 0])))
        ),
        "recovery_combined_p_phase_integral_binary64": _binary_record(
            float(np.trapezoid(recovery_norm, nodes) / period)
        ),
        "center_voltage_signed_row_norm_binary64": fine[
            "center_voltage_return_norm_binary64"
        ],
        "center_recovery_signed_row_norm_binary64": fine[
            "center_recovery_return_norm_binary64"
        ],
        "all_words_injections_and_phase_combined_inside_p": True,
        "diagnostic_only": True,
    }


def _closure_targets(
    *,
    defect: Mapping[str, Any],
    diagnostic: Mapping[str, Any],
    instantaneous: InstantaneousGreenCertificate,
    stage2_certificate: Mapping[str, Any],
) -> dict[str, Any]:
    rank_one_operator = DirectedInterval.from_decimal(
        str(defect["rank_one_advanced_operator_variation_upper"]), PRECISION_BITS
    ).upper
    full_period_operator = DirectedInterval.from_decimal(
        str(defect["full_period_matrix_variation_upper"]), PRECISION_BITS
    ).upper
    lift = DirectedInterval.from_decimal(
        str(defect["exact_history_density_lift_factor_upper"]), PRECISION_BITS
    ).upper
    b_variation = DirectedInterval.from_decimal(
        str(defect["delayed_physical_coefficient_variation_upper"]),
        PRECISION_BITS,
    ).upper
    green_target_interval = DirectedInterval.from_decimal(
        FULL_ADVANCED_GREEN_TARGET, PRECISION_BITS
    )
    boundary_target_interval = DirectedInterval.from_decimal(
        FULL_ADVANCED_BOUNDARY_TARGET, PRECISION_BITS
    )
    green_target = green_target_interval.upper
    boundary_target = boundary_target_interval.upper
    reserve = DirectedInterval.from_decimal(CENTER_TV_RESERVE, PRECISION_BITS).upper
    instant_green = DirectedInterval.from_decimal(
        instantaneous.instantaneous_green_phase_integral_upper,
        PRECISION_BITS,
    ).upper
    instant_boundary = DirectedInterval.from_decimal(
        instantaneous.instantaneous_boundary_propagator_upper,
        PRECISION_BITS,
    ).upper
    delay_sum = DirectedInterval.from_decimal(
        str(defect["delay_sum_upper"]), PRECISION_BITS
    ).upper
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
        lift_green = lift * green_target
    rows: dict[str, Any] = {}
    for row_id, p_key, p_voltage_key, ratio_key, shadow_key in (
        (
            "voltage",
            "voltage_combined_p_uniform_max_binary64",
            "voltage_combined_p_voltage_component_max_binary64",
            "voltage_phase_ratio_transfer_error_upper",
            "directed_voltage_shadow_norm_upper",
        ),
        (
            "recovery",
            "recovery_combined_p_uniform_max_binary64",
            "recovery_combined_p_voltage_component_max_binary64",
            "recovery_phase_ratio_transfer_error_upper",
            "directed_recovery_shadow_norm_upper",
        ),
    ):
        p_max = DirectedInterval.from_float(
            float.fromhex(diagnostic[p_key]["binary64_hex"]), PRECISION_BITS
        ).upper
        p_voltage = DirectedInterval.from_float(
            float.fromhex(diagnostic[p_voltage_key]["binary64_hex"]),
            PRECISION_BITS,
        ).upper
        ratio = DirectedInterval.from_decimal(
            str(defect[ratio_key]), PRECISION_BITS
        ).upper
        shadow = DirectedInterval.from_decimal(
            str(stage2_certificate[shadow_key]), PRECISION_BITS
        ).upper
        with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundDown):
            margin = 1 - shadow
        with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
            orbit_residual = (
                p_voltage * rank_one_operator
                + p_max * full_period_operator
            )
            direct_density = delay_sum * p_voltage * b_variation
            orbit_cost = lift * green_target * orbit_residual
            boundary_cost = lift * boundary_target * ratio
            used = reserve + direct_density + orbit_cost + boundary_cost
        with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundDown):
            remaining = margin - used
        if remaining <= 0:
            required_residual: gmpy2.mpfr | None = None
        else:
            with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundDown):
                required_residual = remaining / lift_green
        with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
            orbit_denominator = lift * orbit_residual
        with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundDown):
            maximum_green = (
                margin - reserve - direct_density - boundary_cost
            ) / orbit_denominator
        rows[row_id] = {
            "stage2_shadow_upper": decimal_upper(shadow, 60),
            "strict_margin_below_one_lower": decimal_lower(margin, 60),
            "combined_p_uniform_binary64_diagnostic": decimal_upper(p_max, 60),
            "combined_p_voltage_component_binary64_diagnostic": decimal_upper(
                p_voltage, 60
            ),
            "orbit_coefficient_row_residual_diagnostic": decimal_upper(
                orbit_residual, 60
            ),
            "direct_delayed_density_cost_diagnostic": decimal_upper(
                direct_density, 60
            ),
            "orbit_cost_at_green_target_diagnostic": decimal_upper(
                orbit_cost, 60
            ),
            "phase_boundary_cost_at_target_diagnostic": decimal_upper(
                boundary_cost, 60
            ),
            "reserved_center_TV_transfer": CENTER_TV_RESERVE,
            "remaining_residual_budget_lower_diagnostic": decimal_lower(
                remaining, 60
            ),
            "required_combined_p_bernstein_residual_upper": (
                decimal_lower(required_residual, 60)
                if required_residual is not None
                else None
            ),
            "maximum_full_green_allowed_by_orbit_defect_diagnostic": decimal_lower(
                maximum_green, 60
            ),
            "budget_closes_if_targets_are_proved": bool(remaining > 0),
            "diagnostic_inputs_promoted": False,
        }
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundDown):
        delayed_green_allowance = green_target_interval.lower - instant_green
        delayed_boundary_allowance = (
            boundary_target_interval.lower - instant_boundary
        )
    return {
        "full_advanced_green_target": FULL_ADVANCED_GREEN_TARGET,
        "full_advanced_boundary_target": FULL_ADVANCED_BOUNDARY_TARGET,
        "strict_instantaneous_green_upper": (
            instantaneous.instantaneous_green_phase_integral_upper
        ),
        "strict_instantaneous_boundary_upper": (
            instantaneous.instantaneous_boundary_propagator_upper
        ),
        "delayed_green_allowance_after_strict_instantaneous_part_lower": decimal_lower(
            delayed_green_allowance, 60
        ),
        "delayed_boundary_allowance_after_strict_instantaneous_part_lower": decimal_lower(
            delayed_boundary_allowance, 60
        ),
        "rows": rows,
        "next_certificate": (
            "degree-24/192-bit tensor Bernstein residual for the two combined "
            "advanced rows, plus delayed Green and boundary corrections below "
            "the displayed allowances"
        ),
        "no_separate_H_or_L_absolute_budget_used": True,
        "full_targets_validated": False,
    }


@lru_cache(maxsize=1)
def build_outer_signed_row_stage3f_adjoint(
    repository: Path,
) -> OuterSignedRowStage3FAdjoint:
    repository = repository.resolve()
    if os.environ.get("OPENBLAS_NUM_THREADS") != PINNED_OPENBLAS_NUM_THREADS:
        raise RuntimeError("Stage-3F requires OPENBLAS_NUM_THREADS=1")
    stage3e = _load_parent(
        repository, STAGE3E_RESULT_RELATIVE_PATH, STAGE3E_RESULT_SHA256
    )
    stage3d = _load_parent(
        repository, STAGE3D_RESULT_RELATIVE_PATH, STAGE3D_RESULT_SHA256
    )
    stage2 = _load_parent(repository, STAGE2_RESULT_RELATIVE_PATH, STAGE2_RESULT_SHA256)
    outer = _load_parent(repository, OUTER_RESULT_RELATIVE_PATH, OUTER_RESULT_SHA256)
    stage3e_certificate = _mapping(stage3e.get("certificate"), "Stage-3E certificate")
    stage3d_certificate = _mapping(stage3d.get("certificate"), "Stage-3D certificate")
    stage2_certificate = _mapping(stage2.get("certificate"), "Stage-2 certificate")
    if _mapping(
        stage3e_certificate.get("transfer_gate"), "Stage-3E transfer gate"
    ).get("exact_F_G_transfer_validated") is not True:
        raise ValueError("the Stage-3E F/G transfer vanished")
    orbit = validate_outer_high_resolution_artifact(
        outer, repository, replay_directed=False
    )
    base = _build_leaky_base_sequences(orbit, PRECISION_BITS)
    instantaneous = _strict_instantaneous_green(
        base, orbit, stage3e_certificate
    )
    defect = _exact_defect_budget(
        base, stage3e_certificate, stage3d_certificate
    )
    diagnostic = _center_diagnostic(orbit, stage3d_certificate)
    targets = _closure_targets(
        defect=defect,
        diagnostic=diagnostic,
        instantaneous=instantaneous,
        stage2_certificate=stage2_certificate,
    )
    claims = {name: True for name in TRUE_FLAGS}
    claims.update({name: False for name in FALSE_FLAGS})
    return OuterSignedRowStage3FAdjoint(
        schema_id=SCHEMA_ID,
        model_id=MODEL_ID,
        branch=BRANCH,
        arithmetic_scope=ARITHMETIC_SCOPE,
        precision_bits=PRECISION_BITS,
        binary_blas_thread_count=1,
        parent_result_sha256={
            STAGE3E_RESULT_RELATIVE_PATH: STAGE3E_RESULT_SHA256,
            STAGE3D_RESULT_RELATIVE_PATH: STAGE3D_RESULT_SHA256,
            STAGE2_RESULT_RELATIVE_PATH: STAGE2_RESULT_SHA256,
            OUTER_RESULT_RELATIVE_PATH: OUTER_RESULT_SHA256,
        },
        combined_advanced_row_identity={
            "voltage_row": (
                "p_sigma(u)=e_v^T R(T+sigma,u)1_{u<=T+sigma}-"
                "[q_v(sigma)/q_v(0)]e_v^T R(T,u)"
            ),
            "recovery_row": (
                "p_w(u)=[e_w^T-q_w(0)e_v^T/q_v(0)]R(T,u)"
            ),
            "advanced_equation": (
                "-p'(u)=p(u)A(u)+sum_{j:u+tau_j<=terminal} "
                "p(u+tau_j)B_j(u+tau_j), with the combined terminal jumps"
            ),
            "history_density": (
                "k(theta)=sum_{j:theta>=-tau_j} "
                "p(theta+tau_j)B_j(theta+tau_j)e_v"
            ),
            "recovery_atom": "c=p(0)e_w",
            "current_voltage_atom": (
                "p(0)e_v h_v(0), killed exactly because h_v(0)=0 on the "
                "linear phase section"
            ),
            "ordering": (
                "delay words, both injection branches and phase subtraction "
                "are inside p before density total variation"
            ),
        },
        instantaneous_green=instantaneous,
        exact_defect_budget=defect,
        center_signed_row_diagnostic=diagnostic,
        residual_closure_targets=targets,
        transfer_errors={
            "E_voltage": None,
            "E_recovery": None,
            "E_phase": _mapping(
                stage3e_certificate.get("transfer_errors"),
                "Stage-3E transfer errors",
            )["E_phase"],
        },
        transfer_gate={
            "instantaneous_green_part_validated": True,
            "delayed_green_part_validated": False,
            "combined_row_residual_validated": False,
            "linear_return_gate_evaluated": False,
            "arbitrary_c0_linear_contraction_closes": False,
            "nonlinear_outer_attraction_closes": False,
        },
        claim_status=claims,
        conclusion=(
            "the 21-term representation is compressed to two combined advanced "
            "rows, and the instantaneous Green/phase/coefficient parts now have "
            "strict source-bound budgets. Binary center diagnostics show ample "
            "scale separation, but the delayed Green correction and the two "
            "combined Bernstein row residuals remain unvalidated; therefore "
            "E_voltage,E_recovery and C0 contraction remain open"
        ),
    )


def build_outer_signed_row_stage3f_adjoint_result(repository: Path) -> dict[str, Any]:
    repository = repository.resolve()
    certificate = json.loads(
        json.dumps(
            asdict(build_outer_signed_row_stage3f_adjoint(repository)),
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


def validate_outer_signed_row_stage3f_adjoint_result(
    payload: Mapping[str, Any], repository: Path
) -> None:
    if not isinstance(payload, Mapping) or set(payload) != {"certificate", "manifest"}:
        raise ValueError("the Stage-3F schema changed")
    certificate = _mapping(payload.get("certificate"), "Stage-3F certificate")
    manifest = _mapping(payload.get("manifest"), "Stage-3F manifest")
    if set(certificate) != {field.name for field in fields(OuterSignedRowStage3FAdjoint)}:
        raise ValueError("the Stage-3F certificate fields changed")
    if manifest.get("schema_id") != SCHEMA_ID or manifest.get("result") != RESULT_RELATIVE_PATH:
        raise ValueError("the Stage-3F manifest changed")
    if canonical_sha256(certificate) != manifest.get("certificate_sha256"):
        raise ValueError("the Stage-3F certificate digest changed")
    sources = _mapping(manifest.get("source_sha256"), "Stage-3F source manifest")
    if set(sources) != set(SOURCE_MANIFEST):
        raise ValueError("the Stage-3F source set changed")
    repository = repository.resolve()
    for relative in SOURCE_MANIFEST:
        if sources.get(relative) != _sha256_path(repository / relative):
            raise ValueError(f"a Stage-3F source changed: {relative}")
    claims = _mapping(certificate.get("claim_status"), "Stage-3F claims")
    if set(claims) != set(TRUE_FLAGS + FALSE_FLAGS):
        raise ValueError("the Stage-3F claim ledger changed")
    if any(claims.get(name) is not True for name in TRUE_FLAGS):
        raise ValueError("a proved Stage-3F fact was weakened")
    if any(claims.get(name) is not False for name in FALSE_FLAGS):
        raise ValueError("an open Stage-3F claim was promoted")
    green = _mapping(certificate.get("instantaneous_green"), "instantaneous Green")
    if green.get("directed_polynomial_replay_validated") is not True:
        raise ValueError("the Stage-3F directed Green replay vanished")
    if green.get("delayed_green_part_included") is not False:
        raise ValueError("the Stage-3F delayed Green part was invented")
    if gmpy2.mpq(str(green["minimum_replayed_determinant_abs_lower"])) <= 0:
        raise ValueError("the Stage-3F determinant gate vanished")
    targets = _mapping(certificate.get("residual_closure_targets"), "closure targets")
    if targets.get("no_separate_H_or_L_absolute_budget_used") is not True:
        raise ValueError("the Stage-3F signed-row ordering changed")
    if targets.get("full_targets_validated") is not False:
        raise ValueError("the Stage-3F residual targets were promoted")
    rows = _mapping(targets.get("rows"), "Stage-3F row targets")
    for row_id in ("voltage", "recovery"):
        row = _mapping(rows.get(row_id), f"Stage-3F {row_id} target")
        if row.get("diagnostic_inputs_promoted") is not False:
            raise ValueError("a Stage-3F binary row was promoted")
        if row.get("required_combined_p_bernstein_residual_upper") is None:
            raise ValueError("a Stage-3F residual budget failed to remain positive")
    diagnostic = _mapping(
        certificate.get("center_signed_row_diagnostic"), "center diagnostic"
    )
    if diagnostic.get("diagnostic_only") is not True:
        raise ValueError("the Stage-3F center row was promoted")
    transfer = _mapping(certificate.get("transfer_errors"), "Stage-3F transfer")
    if transfer.get("E_voltage") is not None or transfer.get("E_recovery") is not None:
        raise ValueError("a Stage-3F transfer error was invented")
    gate = _mapping(certificate.get("transfer_gate"), "Stage-3F gate")
    if gate.get("instantaneous_green_part_validated") is not True:
        raise ValueError("the Stage-3F instantaneous Green gate vanished")
    if gate.get("delayed_green_part_validated") is not False:
        raise ValueError("the Stage-3F delayed Green gate was promoted")
    if gate.get("arbitrary_c0_linear_contraction_closes") is not False:
        raise ValueError("the Stage-3F C0 gate was promoted")
    expected = json.loads(
        json.dumps(
            asdict(build_outer_signed_row_stage3f_adjoint(repository)),
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        )
    )
    if certificate != expected:
        raise ValueError("the Stage-3F certificate differs from replay")


__all__ = [
    "DEFAULT_COMMAND",
    "FALSE_FLAGS",
    "NOTE_RELATIVE_PATH",
    "RESULT_RELATIVE_PATH",
    "SOURCE_MANIFEST",
    "TRUE_FLAGS",
    "build_outer_signed_row_stage3f_adjoint",
    "build_outer_signed_row_stage3f_adjoint_result",
    "canonical_sha256",
    "validate_outer_signed_row_stage3f_adjoint_result",
]
