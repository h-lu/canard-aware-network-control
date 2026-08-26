"""Stage-3 lower bound for the inner stable Riesz projection.

The Stage-2 Lyapunov--Perron row used unit placeholders for both Riesz
projection norms.  This module extracts a *lower* bound in the declared
Route-C reduced-history sup norm.  It refines the already isolated positive
Floquet root, encloses one normalized infinite-dimensional Grushin kernel
column, and transports that column to the physical point-evaluation section.

The conclusion is deliberately one-sided: ``||P_s|| >= 2``.  It disproves
the old ``C_N=10`` scalar-majorant row, even after optimizing its sequence
weight, but supplies no projection upper bound, stable power bound, return
map ``C^2`` bound, stable graph, separator, or onset theorem.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR, localcontext
from hashlib import sha256
import json
import os
from pathlib import Path
import platform
from typing import Any, Mapping

import gmpy2
import numpy as np
import scipy

from canard_control.directed_interval import (
    DirectedComplexInterval,
    DirectedInterval,
    complex_unit_interval,
    decimal_lower,
    decimal_upper,
    pi_interval,
)
from canard_control.floquet_cover_arithmetic import (
    _binary_complex_product_split_l1_upper,
)
from canard_control.leaky_floquet_inner_unstable_root import (
    PINNED_OPENBLAS_NUM_THREADS,
    PRECISION_BITS,
    RESULT_RELATIVE_PATH as ROOT_RESULT_RELATIVE_PATH,
    _augment_finite,
    _dependency_fingerprint,
    _evaluate_prepared,
    _exp_interval,
    _grushin_block_bounds,
    _prepare_cached,
    _vector_l1_upper,
    validate_leaky_inner_unstable_root_result,
)
from canard_control.leaky_inner_stable_manifold_stage2_contract import (
    RESULT_RELATIVE_PATH as STAGE2_RESULT_RELATIVE_PATH,
    validate_stage2_stable_manifold_result,
)


SCHEMA_ID = "leaky-inner-stable-projection-stage3-v1"
MODEL_ID = "autonomous-leaky-recovery-two-delay-fhn-bistable-proposal"
BRANCH = "inner_saddle_candidate"
SOURCE_RELATIVE_PATH = (
    "src/canard_control/leaky_inner_stable_projection_stage3.py"
)
GENERATOR_RELATIVE_PATH = (
    "experiments/leaky_inner_stable_projection_stage3.py"
)
RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_inner_stable_projection_stage3.json"
)
NOTE_RELATIVE_PATH = "docs/leaky-inner-stable-projection-stage3.md"
TEST_RELATIVE_PATH = "tests/test_leaky_inner_stable_projection_stage3.py"
DEFAULT_COMMAND = (
    "OPENBLAS_NUM_THREADS=8 OMP_NUM_THREADS=1 PYTHONPATH=src "
    "/usr/bin/python3 experiments/leaky_inner_stable_projection_stage3.py"
)
ARITHMETIC_SCOPE = (
    "160-bit outward MPFR arithmetic around the source-bound inner orbit; "
    "the complete cutoff-64 plus infinite-tail Grushin preconditioner; "
    "pointwise effective-Hamiltonian sign enclosures; a column-specific "
    "finite/tail residual and Neumann enclosure; physical-time interval "
    "evaluation of the Route-C section; exact rank-one projection geometry; "
    "and directed Decimal evaluation of the Stage-1 scalar budget"
)
SOURCE_MANIFEST = (
    SOURCE_RELATIVE_PATH,
    GENERATOR_RELATIVE_PATH,
    NOTE_RELATIVE_PATH,
    "src/canard_control/directed_interval.py",
    "src/canard_control/floquet_cover_arithmetic.py",
    "src/canard_control/leaky_floquet_inner_unstable_root.py",
    "src/canard_control/leaky_inner_stable_manifold_stage2_contract.py",
)

ROOT_RESULT_SHA256 = (
    "ab2876efc8a26df544f56257ab00b9fde0fea4ba043f4500f1450e0d0885fa2c"
)
STAGE2_RESULT_SHA256 = (
    "eafa4d07b0558d9d4ce7423969379fa51875fcabce55af89a2378261fdb1e18d"
)

ROOT_BRACKET_LOWER = 0.69836041
ROOT_BRACKET_UPPER = 0.69836043
EIGENCOLUMN_CENTER = 0.69836042
EIGENCOLUMN_NEIGHBORHOOD = "1.1e-8"
HISTORY_TEST_TIME = "-3.1724"
NESTED_ORBIT_RADIUS = "1e-12"

TRUE_FLAGS = (
    "refined_positive_root_bracket_validated",
    "full_infinite_grushin_eigencolumn_enclosed",
    "route_c_section_unstable_voltage_component_dominates_recovery",
    "unstable_adjoint_history_measure_nonatomic_away_from_current_time",
    "stable_projection_norm_lower_two_validated",
    "selected_beta_c_n_10_scalar_row_falsified",
    "all_beta_c_n_10_scalar_rows_falsified",
)
FALSE_FLAGS = (
    "binary_projection_diagnostic_promoted_to_proof",
    "stable_projection_norm_upper_validated",
    "unstable_projection_norm_upper_validated",
    "stable_dichotomy_constant_upper_validated",
    "actual_return_map_c_n_upper_validated",
    "adapted_splitting_norm_scalar_gate_validated",
    "quantitative_stable_graph_validated",
    "physical_pulse_separator_validated",
    "physical_pulse_onset_validated",
)


@dataclass(frozen=True)
class Stage3StableProjectionCertificate:
    schema_id: str
    model_id: str
    branch: str
    history_space: str
    section: str
    root_bracket: dict[str, Any]
    eigencolumn_enclosure: dict[str, Any]
    route_c_component_audit: dict[str, Any]
    projection_geometry: dict[str, Any]
    scalar_majorant_no_go: dict[str, Any]
    adapted_splitting_norm_audit: dict[str, Any]
    binary_diagnostic: dict[str, Any]
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


def _symmetric(radius: gmpy2.mpfr, precision: int) -> DirectedInterval:
    return DirectedInterval.from_bounds(-radius, radius, precision)


def _complex_point(value: complex, precision: int) -> DirectedComplexInterval:
    return DirectedComplexInterval(
        DirectedInterval.from_float(float(value.real), precision),
        DirectedInterval.from_float(float(value.imag), precision),
    )


def _complex_expand(
    value: DirectedComplexInterval,
    radius: gmpy2.mpfr,
) -> DirectedComplexInterval:
    error = _symmetric(radius, value.precision)
    return DirectedComplexInterval(value.real + error, value.imag + error)


def _binary_series_box(
    coefficients: np.ndarray,
    modes: np.ndarray,
    phase: DirectedInterval,
) -> DirectedComplexInterval:
    precision = phase.precision
    zero = DirectedInterval.from_decimal(0, precision)
    total = DirectedComplexInterval(zero, zero)
    for coefficient, mode in zip(coefficients, modes, strict=True):
        angle = pi_interval(precision) * (2 * int(mode)) * phase
        total = total + _complex_point(complex(coefficient), precision) * (
            complex_unit_interval(angle)
        )
    return total


def _orbit_series_real_box(
    coefficients: Mapping[int, DirectedComplexInterval],
    phase: DirectedInterval,
) -> DirectedInterval:
    precision = phase.precision
    zero = DirectedInterval.from_decimal(0, precision)
    total = DirectedComplexInterval(zero, zero)
    for mode, coefficient in coefficients.items():
        angle = pi_interval(precision) * (2 * int(mode)) * phase
        total = total + coefficient * complex_unit_interval(angle)
    return total.real


def _effective_hamiltonian_point(
    prepared: Any,
    spectral_point: float,
) -> dict[str, str]:
    precision = PRECISION_BITS
    evaluated = _evaluate_prepared(prepared, complex(spectral_point, 0.0))
    finite, _, _, finite_tail, finite_tail_first, tail_finite, errors = evaluated
    augmented = _augment_finite(
        finite, prepared.right_border, prepared.left_border
    )
    inverse = np.linalg.inv(augmented)
    block = _grushin_block_bounds(
        prepared,
        s=complex(spectral_point, 0.0),
        neighborhood=gmpy2.mpfr(0, precision),
        inverse=inverse,
        finite=finite,
        finite_tail=finite_tail,
        finite_tail_first=finite_tail_first,
        tail_finite=tail_finite,
        errors=errors,
        include_disk_s_variation=False,
    )
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        error = (
            block["bottom_row"]
            * block["scalar_column_norm"]
            / (1 - block["contraction"])
        )
    center = DirectedInterval.from_float(float(inverse[-1, -1].real), precision)
    enclosure = center + _symmetric(error, precision)
    return {
        "spectral_point_binary64": format(spectral_point, ".17g"),
        "finite_effective_hamiltonian_real_binary64": format(
            float(inverse[-1, -1].real), ".17g"
        ),
        "full_effective_hamiltonian_error_upper": decimal_upper(error),
        "full_effective_hamiltonian_real_lower": decimal_lower(
            enclosure.lower
        ),
        "full_effective_hamiltonian_real_upper": decimal_upper(
            enclosure.upper
        ),
        "full_grushin_contraction_upper": decimal_upper(
            block["contraction"]
        ),
    }


def _eigencolumn_enclosure(
    prepared: Any,
) -> tuple[dict[str, Any], np.ndarray, gmpy2.mpfr, Any]:
    precision = PRECISION_BITS
    radius = gmpy2.mpfr(EIGENCOLUMN_NEIGHBORHOOD, precision)
    center = complex(EIGENCOLUMN_CENTER, 0.0)
    evaluated = _evaluate_prepared(prepared, center)
    finite, _, _, finite_tail, finite_tail_first, tail_finite, errors = evaluated
    augmented = _augment_finite(
        finite, prepared.right_border, prepared.left_border
    )
    inverse = np.linalg.inv(augmented)
    approximate_column = inverse[:, -1]
    approximate_state = approximate_column[:-1]
    block = _grushin_block_bounds(
        prepared,
        s=center,
        neighborhood=radius,
        inverse=inverse,
        finite=finite,
        finite_tail=finite_tail,
        finite_tail_first=finite_tail_first,
        tail_finite=tail_finite,
        errors=errors,
        include_disk_s_variation=True,
    )
    finite_binary_residual = _binary_complex_product_split_l1_upper(
        block["defect_matrix"],
        approximate_column.reshape(-1, 1),
        precision,
    )
    state_norm = _vector_l1_upper(approximate_state, precision)
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        finite_residual = finite_binary_residual + (
            block["inverse_norm"]
            * block["finite_change"]
            * state_norm
        )
    tail_binary_residual = _binary_complex_product_split_l1_upper(
        tail_finite,
        approximate_state.reshape(-1, 1),
        precision,
    )
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        tail_residual = (
            block["fast_tail_inverse"] * tail_binary_residual
            + (
                block["fast_tail_inverse"]
                * block["tail_finite_change"]
                + block["tail_finite_orbit"]
            )
            * state_norm
        )
        total_residual = finite_residual + tail_residual
        column_error = total_residual / (1 - block["contraction"])
    return (
        {
            "spectral_center_binary64": format(EIGENCOLUMN_CENTER, ".17g"),
            "spectral_neighborhood_radius": EIGENCOLUMN_NEIGHBORHOOD,
            "root_bracket_contained_in_neighborhood": True,
            "approximate_state_split_wiener_norm_upper": decimal_upper(
                state_norm
            ),
            "finite_column_residual_upper": decimal_upper(finite_residual),
            "tail_column_residual_upper": decimal_upper(tail_residual),
            "total_preconditioned_column_residual_upper": decimal_upper(
                total_residual
            ),
            "full_grushin_contraction_upper": decimal_upper(
                block["contraction"]
            ),
            "exact_normalized_eigencolumn_split_wiener_error_upper": (
                decimal_upper(column_error)
            ),
            "normalization": (
                "the exact Grushin domain border equals one; at the exact "
                "root the scalar effective-Hamiltonian coordinate is zero"
            ),
            "full_infinite_grushin_eigencolumn_enclosed": True,
        },
        approximate_state,
        column_error,
        block,
    )


def _route_c_component_audit(
    prepared: Any,
    approximate_state: np.ndarray,
    column_error: gmpy2.mpfr,
) -> dict[str, Any]:
    precision = PRECISION_BITS
    zero = DirectedInterval.from_decimal(0, precision)
    orbit_radius = DirectedInterval.from_decimal(
        NESTED_ORBIT_RADIUS, precision
    )
    exact_period = prepared.base.period + _symmetric(
        orbit_radius.upper, precision
    )
    exact_root = DirectedInterval.from_bounds(
        format(ROOT_BRACKET_LOWER, ".17g"),
        format(ROOT_BRACKET_UPPER, ".17g"),
        precision,
    )
    theta = DirectedInterval.from_decimal(HISTORY_TEST_TIME, precision)
    modes = prepared.modes
    mode_count = len(modes)

    def orbit_value(component: int, time: DirectedInterval) -> DirectedInterval:
        coefficient = (
            prepared.base.voltage
            if component == 0
            else prepared.base.recovery
        )
        candidate = _orbit_series_real_box(coefficient, time / exact_period)
        return candidate + _symmetric(orbit_radius.upper, precision)

    def physical_field(
        time: DirectedInterval,
    ) -> tuple[DirectedInterval, DirectedInterval]:
        voltage = orbit_value(0, time)
        recovery = orbit_value(1, time)
        delayed = tuple(
            orbit_value(0, time - prepared.base.parameters[name])
            for name in ("tau_0", "tau_1")
        )
        epsilon = prepared.base.parameters["epsilon"]
        kappa_1 = prepared.base.parameters["kappa_1"]
        kappa_3 = prepared.base.parameters["kappa_3"]
        unfolding = prepared.base.parameters["unfolding"]
        fast = (
            voltage
            - voltage**3 / 3
            - recovery
            + epsilon
            * kappa_1
            * ((delayed[0] + delayed[1]) / 2 - voltage)
            + epsilon
            * kappa_3
            * (
                ((delayed[0] - 1) ** 3 + (delayed[1] - 1) ** 3) / 2
                - (voltage - 1) ** 3
            )
        )
        slow = epsilon * (voltage - unfolding - recovery)
        return fast, slow

    phase = theta / exact_period
    voltage_profile = _binary_series_box(
        approximate_state[:mode_count], modes, phase
    )
    exponential = _exp_interval(exact_root * phase)
    voltage_history = DirectedComplexInterval.from_real(exponential) * (
        voltage_profile
    )
    voltage_history = _complex_expand(
        voltage_history, exponential.upper * column_error
    )
    voltage_current = _complex_expand(
        _binary_series_box(
            approximate_state[:mode_count], modes, zero
        ),
        column_error,
    )
    recovery_current = _complex_expand(
        _binary_series_box(
            approximate_state[mode_count:], modes, zero
        ),
        column_error,
    )

    field_theta = physical_field(theta)
    field_zero = physical_field(zero)
    if field_zero[0].lower <= 0:
        raise ArithmeticError("the Route-C phase denominator crossed zero")
    voltage_tangent_ratio = field_theta[0] / field_zero[0]
    recovery_tangent_ratio = field_zero[1] / field_zero[0]
    section_voltage = voltage_history - (
        DirectedComplexInterval.from_real(voltage_tangent_ratio)
        * voltage_current
    )
    section_recovery = recovery_current - (
        DirectedComplexInterval.from_real(recovery_tangent_ratio)
        * voltage_current
    )
    voltage_lower = section_voltage.lower_abs()
    recovery_upper = section_recovery.upper_abs()
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        dominance_margin = voltage_lower - recovery_upper
    if dominance_margin <= 0:
        raise ArithmeticError("the unstable voltage component did not dominate")
    return {
        "history_test_time": HISTORY_TEST_TIME,
        "history_test_time_strictly_inside_delay_interval": True,
        "exact_physical_voltage_field_at_test_time_lower": decimal_lower(
            field_theta[0].lower
        ),
        "exact_physical_voltage_field_at_test_time_upper": decimal_upper(
            field_theta[0].upper
        ),
        "exact_physical_voltage_field_at_phase_zero_lower": decimal_lower(
            field_zero[0].lower
        ),
        "exact_physical_voltage_field_at_phase_zero_upper": decimal_upper(
            field_zero[0].upper
        ),
        "exact_physical_recovery_field_at_phase_zero_lower": decimal_lower(
            field_zero[1].lower
        ),
        "exact_physical_recovery_field_at_phase_zero_upper": decimal_upper(
            field_zero[1].upper
        ),
        "section_voltage_component_at_test_time_abs_lower": decimal_lower(
            voltage_lower
        ),
        "section_recovery_component_abs_upper": decimal_upper(
            recovery_upper
        ),
        "voltage_minus_recovery_dominance_margin_lower": decimal_lower(
            dominance_margin
        ),
        "route_c_section_formula": (
            "q^Sigma=q-dot(x)_0*q_v(0)/dot(v)(0)"
        ),
        "route_c_section_unstable_voltage_component_dominates_recovery": True,
    }


def _decimal_budget(stage2: Mapping[str, Any]) -> dict[str, Any]:
    strengthened = _mapping(
        stage2["contract"]["strengthened_gamma01_spectral_ingress"],
        "Stage-2 strengthened spectral ingress",
    )
    rho_s = Decimal(strengthened["working_stable_power_rate_upper"])
    rho_u = Decimal(strengthened["unstable_backward_rate_upper"])
    beta = Decimal(strengthened["sequence_weight_beta"])
    with localcontext() as context:
        context.prec = 110
        context.rounding = ROUND_FLOOR
        stable_coefficient_lower = Decimal(1) / (beta - rho_s)
        unstable_coefficient_lower = rho_u / (1 - beta * rho_u)
        selected_denominator_lower = (
            2 * stable_coefficient_lower + unstable_coefficient_lower
        )
        selected_lhs_lower = Decimal(10) * selected_denominator_lower
        limiting_denominator_lower = (
            Decimal(2) / (Decimal(1) - rho_s)
            + rho_u / (Decimal(1) - rho_u)
        )
        limiting_lhs_lower = Decimal(10) * limiting_denominator_lower
    with localcontext() as context:
        context.prec = 110
        context.rounding = ROUND_CEILING
        selected_c_n_ceiling_upper = (
            Decimal(2500) / selected_denominator_lower
        )
        all_beta_c_n_ceiling_supremum_upper = (
            Decimal(2500) / limiting_denominator_lower
        )
    if not selected_lhs_lower > 2500:
        raise ArithmeticError("the selected-beta no-go did not close")
    if not limiting_lhs_lower > 2500:
        raise ArithmeticError("the all-beta no-go did not close")
    return {
        "stage1_scalar_budget_formula": (
            "K_s*C_N*(a_s*K_s*p_s+a_u*K_u*p_u)<2500"
        ),
        "universal_lower_inputs_used": (
            "K_s>=1, p_s>=2, K_u=1, p_u>=1"
        ),
        "selected_sequence_weight_beta": str(beta),
        "selected_stable_kernel_coefficient_lower": format(
            stable_coefficient_lower, "f"
        ),
        "selected_unstable_kernel_coefficient_lower": format(
            unstable_coefficient_lower, "f"
        ),
        "selected_beta_c_n_10_lhs_lower": format(
            selected_lhs_lower, "f"
        ),
        "selected_beta_c_n_10_scalar_row_falsified": True,
        "selected_beta_necessary_c_n_ceiling_upper": format(
            selected_c_n_ceiling_upper, "f"
        ),
        "kernel_strictly_decreasing_up_to_beta_one_under_p_s_two": True,
        "all_beta_infimum_denominator_lower": format(
            limiting_denominator_lower, "f"
        ),
        "all_beta_c_n_10_lhs_infimum_lower": format(
            limiting_lhs_lower, "f"
        ),
        "all_beta_c_n_10_scalar_rows_falsified": True,
        "all_beta_necessary_c_n_ceiling_supremum_upper": format(
            all_beta_c_n_ceiling_supremum_upper, "f"
        ),
        "actual_return_map_c_n_upper": None,
        "current_history_norm_intrinsically_impossible": False,
        "interpretation": (
            "the proved no-go concerns C_N=10 inside the disclosed Stage-1 "
            "scalar majorant; the same norm could still close if a directed "
            "return calculation proves a sufficiently smaller C_N"
        ),
    }


def _binary_diagnostic() -> dict[str, Any]:
    # These converged method-of-steps values are diagnostics only.  The proof
    # above does not consume them; keeping them separate prevents a finite
    # grid eigenprojection from being mistaken for a history-space theorem.
    return {
        "method": (
            "piecewise-linear initial histories, DOP853 method of steps, "
            "Route-C event projection, induced matrix infinity norm"
        ),
        "grid_rows": [
            {
                "history_node_count": 41,
                "unstable_multiplier_binary64": "2.01041271492",
                "unstable_projection_norm_binary64": "1.40065215025",
                "stable_projection_norm_binary64": "2.39935599840",
                "deflated_one_step_norm_binary64": "0.00410292566097",
            },
            {
                "history_node_count": 81,
                "unstable_multiplier_binary64": "2.01044345568",
                "unstable_projection_norm_binary64": "1.40125739631",
                "stable_projection_norm_binary64": "2.40071576904",
                "deflated_one_step_norm_binary64": "0.00411293653319",
            },
            {
                "history_node_count": 161,
                "unstable_multiplier_binary64": "2.01045113900",
                "unstable_projection_norm_binary64": "1.40142070517",
                "stable_projection_norm_binary64": "2.40112275235",
                "deflated_one_step_norm_binary64": "0.00411677508881",
            },
        ],
        "diagnostic_stable_power_ratio_maximum_occurs_at_n_zero": True,
        "binary_projection_diagnostic_promoted_to_proof": False,
    }


def build_stage3_stable_projection_certificate(
    repository: Path,
) -> Stage3StableProjectionCertificate:
    if os.environ.get("OPENBLAS_NUM_THREADS") != PINNED_OPENBLAS_NUM_THREADS:
        raise RuntimeError(
            "the Stage-3 Grushin replay requires OPENBLAS_NUM_THREADS="
            + PINNED_OPENBLAS_NUM_THREADS
        )
    repository = repository.resolve()
    root_path = repository / ROOT_RESULT_RELATIVE_PATH
    stage2_path = repository / STAGE2_RESULT_RELATIVE_PATH
    if _sha256_path(root_path) != ROOT_RESULT_SHA256:
        raise ValueError("the Stage-3 inner-root parent changed")
    if _sha256_path(stage2_path) != STAGE2_RESULT_SHA256:
        raise ValueError("the Stage-3 Stage-2 parent changed")
    root_payload = json.loads(root_path.read_text(encoding="utf-8"))
    stage2_payload = json.loads(stage2_path.read_text(encoding="utf-8"))
    validate_leaky_inner_unstable_root_result(root_payload, repository)
    validate_stage2_stable_manifold_result(stage2_payload, repository)

    fingerprint = _dependency_fingerprint(repository)
    prepared, _ = _prepare_cached(str(repository), fingerprint)
    lower = _effective_hamiltonian_point(prepared, ROOT_BRACKET_LOWER)
    upper = _effective_hamiltonian_point(prepared, ROOT_BRACKET_UPPER)
    if Decimal(lower["full_effective_hamiltonian_real_upper"]) >= 0:
        raise ArithmeticError("the refined root lower endpoint is not negative")
    if Decimal(upper["full_effective_hamiltonian_real_lower"]) <= 0:
        raise ArithmeticError("the refined root upper endpoint is not positive")
    eigencolumn, approximate_state, column_error, _ = (
        _eigencolumn_enclosure(prepared)
    )
    component = _route_c_component_audit(
        prepared, approximate_state, column_error
    )
    no_go = _decimal_budget(stage2_payload)

    claims = {name: True for name in TRUE_FLAGS}
    claims.update({name: False for name in FALSE_FLAGS})
    return Stage3StableProjectionCertificate(
        schema_id=SCHEMA_ID,
        model_id=MODEL_ID,
        branch=BRANCH,
        history_space=(
            "Y=C([-tau_max,0],R) x R with "
            "||(phi,w)||=max(||phi||_infinity,|w|)"
        ),
        section="Sigma={phi_v(0)=0} at the exact Route-C phase-zero crossing",
        root_bracket={
            "lower_endpoint": lower,
            "upper_endpoint": upper,
            "root_real_lower": format(ROOT_BRACKET_LOWER, ".17g"),
            "root_real_upper": format(ROOT_BRACKET_UPPER, ".17g"),
            "parent_disk_contains_exactly_one_real_simple_root": True,
            "endpoint_sign_change_validated": True,
            "refined_positive_root_bracket_validated": True,
        },
        eigencolumn_enclosure=eigencolumn,
        route_c_component_audit=component,
        projection_geometry={
            "unstable_section_vector": (
                "q^Sigma=Qq, where Q=I-dot(x)_0*h_C/dot(v)(0)"
            ),
            "unstable_left_covector": (
                "the nonneutral monodromy adjoint covector restricted to Sigma"
            ),
            "adjoint_history_measure_structure": (
                "an atom in the current voltage coordinate, an atom in the "
                "current recovery coordinate, and an absolutely continuous "
                "voltage-history density from the two discrete delays"
            ),
            "unstable_adjoint_history_measure_nonatomic_away_from_current_time": True,
            "rank_one_stable_projection_row_formula": (
                "(P_s z)_v(theta)=delta_theta(z)-"
                "q^Sigma_v(theta)*f(z)/f(q^Sigma)"
            ),
            "stable_projection_lower_formula": (
                "p_s>=1+||q^Sigma_v||_infinity/||q^Sigma||"
            ),
            "component_dominance_implies_section_vector_norm_is_voltage_sup": True,
            "stable_projection_norm_lower": "2",
            "stable_projection_norm_lower_two_validated": True,
            "stable_projection_norm_upper": None,
            "unstable_projection_norm_upper": None,
        },
        scalar_majorant_no_go=no_go,
        adapted_splitting_norm_audit={
            "direct_sum_norm": (
                "||x||_split=||P_s x||_old+||P_u x||_old"
            ),
            "projection_norms_in_direct_sum_norm": "p_s=p_u=1 exactly",
            "norm_equivalence": (
                "||x||_old<=||x||_split<=(p_s_old+p_u_old)||x||_old"
            ),
            "black_box_nonlinear_transfer": (
                "C_N_split<=(p_s_old+p_u_old)*C_N_old"
            ),
            "weighted_sum_norm": (
                "||x||_lambda=||P_s x||_old+lambda||P_u x||_old"
            ),
            "weighted_black_box_inflation": (
                "(p_s_old+lambda*p_u_old)*max(1,lambda^{-1})^2"
            ),
            "weighted_black_box_factor_minimized_at_lambda_one": True,
            "projection_isometry_alone_improves_scalar_gate": False,
            "section_quotient_route": (
                "validate the four projected D2P blocks directly in "
                "(stable history, unstable scalar) coordinates; this can "
                "avoid the global norm-equivalence factor but is not yet done"
            ),
            "direct_projected_return_c2_blocks_validated": False,
            "adapted_splitting_norm_scalar_gate_validated": False,
        },
        binary_diagnostic=_binary_diagnostic(),
        claim_status=claims,
    )


def build_stage3_stable_projection_result(repository: Path) -> dict[str, Any]:
    repository = repository.resolve()
    certificate = asdict(build_stage3_stable_projection_certificate(repository))
    return {
        "certificate": certificate,
        "manifest": {
            "schema_id": SCHEMA_ID,
            "result": RESULT_RELATIVE_PATH,
            "default_command": DEFAULT_COMMAND,
            "arithmetic_scope": ARITHMETIC_SCOPE,
            "certificate_sha256": canonical_sha256(certificate),
            "source_sha256": {
                relative: _sha256_path(repository / relative)
                for relative in SOURCE_MANIFEST
            },
            "parent_result_sha256": {
                ROOT_RESULT_RELATIVE_PATH: ROOT_RESULT_SHA256,
                STAGE2_RESULT_RELATIVE_PATH: STAGE2_RESULT_SHA256,
            },
            "environment": {
                "python": platform.python_version(),
                "platform": platform.platform(),
                "numpy": np.__version__,
                "scipy": scipy.__version__,
                "gmpy2": gmpy2.__version__,
                "mpfr": gmpy2.mpfr_version(),
                "openblas_num_threads": os.environ.get(
                    "OPENBLAS_NUM_THREADS"
                ),
            },
        },
    }


def validate_stage3_stable_projection_result(
    payload: Mapping[str, Any], repository: Path
) -> None:
    if not isinstance(payload, Mapping) or set(payload) != {
        "certificate",
        "manifest",
    }:
        raise ValueError("the Stage-3 result has the wrong outer schema")
    certificate = _mapping(payload.get("certificate"), "Stage-3 certificate")
    manifest = _mapping(payload.get("manifest"), "Stage-3 manifest")
    if set(certificate) != {
        field.name for field in fields(Stage3StableProjectionCertificate)
    }:
        raise ValueError("the Stage-3 certificate schema changed")
    if certificate.get("schema_id") != SCHEMA_ID:
        raise ValueError("the Stage-3 schema id changed")
    if certificate.get("model_id") != MODEL_ID or certificate.get("branch") != BRANCH:
        raise ValueError("the Stage-3 certificate belongs to another model")
    claims = _mapping(certificate.get("claim_status"), "Stage-3 claim status")
    if set(claims) != set(TRUE_FLAGS) | set(FALSE_FLAGS):
        raise ValueError("the Stage-3 claim ledger changed")
    if any(claims.get(name) is not True for name in TRUE_FLAGS):
        raise ValueError("a proved Stage-3 statement was weakened")
    if any(claims.get(name) is not False for name in FALSE_FLAGS):
        raise ValueError("an open Stage-3 statement was promoted")

    root = _mapping(certificate.get("root_bracket"), "Stage-3 root bracket")
    lower = _mapping(root.get("lower_endpoint"), "root lower endpoint")
    upper = _mapping(root.get("upper_endpoint"), "root upper endpoint")
    if Decimal(lower["full_effective_hamiltonian_real_upper"]) >= 0:
        raise ValueError("the registered lower endpoint is not strictly negative")
    if Decimal(upper["full_effective_hamiltonian_real_lower"]) <= 0:
        raise ValueError("the registered upper endpoint is not strictly positive")
    if not Decimal(root["root_real_lower"]) < Decimal(root["root_real_upper"]):
        raise ValueError("the registered root bracket is empty")

    eigen = _mapping(
        certificate.get("eigencolumn_enclosure"), "Stage-3 eigencolumn"
    )
    if Decimal(eigen["exact_normalized_eigencolumn_split_wiener_error_upper"]) >= Decimal("3e-8"):
        raise ValueError("the registered eigencolumn error is too large")
    if Decimal(eigen["full_grushin_contraction_upper"]) >= 1:
        raise ValueError("the local full Grushin contraction failed")

    component = _mapping(
        certificate.get("route_c_component_audit"), "Route-C component audit"
    )
    voltage = Decimal(
        component["section_voltage_component_at_test_time_abs_lower"]
    )
    recovery = Decimal(component["section_recovery_component_abs_upper"])
    margin = Decimal(component["voltage_minus_recovery_dominance_margin_lower"])
    if not voltage > recovery > 0 or margin <= Decimal("0.0213"):
        raise ValueError("the Route-C unstable component dominance failed")

    geometry = _mapping(
        certificate.get("projection_geometry"), "projection geometry"
    )
    if geometry.get("stable_projection_norm_lower") != "2":
        raise ValueError("the Stage-3 stable projection lower bound changed")
    if geometry.get("stable_projection_norm_upper") is not None:
        raise ValueError("a stable projection upper bound was invented")
    if geometry.get("unstable_projection_norm_upper") is not None:
        raise ValueError("an unstable projection upper bound was invented")

    no_go = _mapping(
        certificate.get("scalar_majorant_no_go"), "scalar-majorant no-go"
    )
    if Decimal(no_go["selected_beta_c_n_10_lhs_lower"]) <= 2500:
        raise ValueError("the selected-beta C_N=10 no-go vanished")
    if Decimal(no_go["all_beta_c_n_10_lhs_infimum_lower"]) <= 2500:
        raise ValueError("the all-beta C_N=10 no-go vanished")
    if Decimal(no_go["selected_beta_necessary_c_n_ceiling_upper"]) >= Decimal("5.43"):
        raise ValueError("the selected-beta C_N ceiling was weakened")
    if Decimal(no_go["all_beta_necessary_c_n_ceiling_supremum_upper"]) >= Decimal("6.21"):
        raise ValueError("the all-beta C_N ceiling was weakened")
    if no_go.get("actual_return_map_c_n_upper") is not None:
        raise ValueError("an actual return-map C_N bound was invented")
    if no_go.get("current_history_norm_intrinsically_impossible") is not False:
        raise ValueError("the scalar-majorant no-go was overstated")

    adapted = _mapping(
        certificate.get("adapted_splitting_norm_audit"),
        "adapted splitting-norm audit",
    )
    if adapted.get("projection_isometry_alone_improves_scalar_gate") is not False:
        raise ValueError("projection isometry was promoted without C_N transfer")
    if adapted.get("adapted_splitting_norm_scalar_gate_validated") is not False:
        raise ValueError("the adapted-norm gate was promoted")

    expected_manifest_fields = {
        "schema_id",
        "result",
        "default_command",
        "arithmetic_scope",
        "certificate_sha256",
        "source_sha256",
        "parent_result_sha256",
        "environment",
    }
    if set(manifest) != expected_manifest_fields:
        raise ValueError("the Stage-3 manifest schema changed")
    fixed = {
        "schema_id": SCHEMA_ID,
        "result": RESULT_RELATIVE_PATH,
        "default_command": DEFAULT_COMMAND,
        "arithmetic_scope": ARITHMETIC_SCOPE,
        "certificate_sha256": canonical_sha256(certificate),
        "parent_result_sha256": {
            ROOT_RESULT_RELATIVE_PATH: ROOT_RESULT_SHA256,
            STAGE2_RESULT_RELATIVE_PATH: STAGE2_RESULT_SHA256,
        },
    }
    if any(manifest.get(name) != value for name, value in fixed.items()):
        raise ValueError("the Stage-3 manifest fixed data changed")
    repository = repository.resolve()
    source_hashes = _mapping(
        manifest.get("source_sha256"), "Stage-3 source manifest"
    )
    if set(source_hashes) != set(SOURCE_MANIFEST):
        raise ValueError("the Stage-3 source set changed")
    for relative in SOURCE_MANIFEST:
        if source_hashes.get(relative) != _sha256_path(repository / relative):
            raise ValueError(f"the Stage-3 source changed: {relative}")
    for relative, digest in fixed["parent_result_sha256"].items():
        if _sha256_path(repository / relative) != digest:
            raise ValueError(f"the Stage-3 parent changed: {relative}")


__all__ = [
    "ARITHMETIC_SCOPE",
    "DEFAULT_COMMAND",
    "FALSE_FLAGS",
    "GENERATOR_RELATIVE_PATH",
    "NOTE_RELATIVE_PATH",
    "RESULT_RELATIVE_PATH",
    "SCHEMA_ID",
    "SOURCE_MANIFEST",
    "SOURCE_RELATIVE_PATH",
    "Stage3StableProjectionCertificate",
    "TRUE_FLAGS",
    "build_stage3_stable_projection_certificate",
    "build_stage3_stable_projection_result",
    "canonical_sha256",
    "validate_stage3_stable_projection_result",
]
