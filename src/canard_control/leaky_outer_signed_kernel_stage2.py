"""Stage-2 signed matrix-measure pilot for the outer return derivative.

This module performs a directed 160-bit cellwise post-processing of the
360-step binary64 method-of-steps monodromy matrix.  The physical phase row
is normalized with the stored Fourier tangent.  For every retained output
row and every input cell, it evaluates

    M_ij - q_i M_hj / q_h

with outward MPFR arithmetic, and only then sums absolute values.  Fixed-time
and rank-one phase terms are also summed separately to expose the large
cancellation.

The resulting object is a *discrete signed-measure shadow*, not yet a bound
for the operator on C([-tau,0]).  The exact continuous operator has one
current-value Dirac atom, an absolutely continuous history density, and one
initial-recovery scalar column.  A future interval-Taylor/Volterra method of
steps must enclose those densities cellwise and bound their distance from the
registered shadow.  The current-value atom vanishes exactly on the phase
section.  Until the two continuous transfer errors are supplied, arbitrary
C0 coverage and outer contraction remain false.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from decimal import Decimal, InvalidOperation, ROUND_CEILING, ROUND_FLOOR, localcontext
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

from canard_control.directed_interval import (
    DirectedInterval,
    decimal_lower,
    decimal_upper,
)
from canard_control.leaky_outer_high_resolution import (
    RESULT_RELATIVE_PATH as OUTER_RESULT_RELATIVE_PATH,
    validate_outer_high_resolution_artifact,
)
from canard_control.leaky_outer_phase_fixed_return_stage1 import (
    RESULT_RELATIVE_PATH as STAGE1_RESULT_RELATIVE_PATH,
    validate_outer_phase_fixed_return_result,
)
from canard_control.leaky_pulse_separator_candidate import (
    TAU_1,
    _periodic_interpolator,
    finite_section,
)


SCHEMA_ID = "leaky-outer-signed-kernel-stage2-v1"
MODEL_ID = "autonomous-leaky-recovery-two-delay-fhn-bistable-proposal"
BRANCH = "outer_pulse"
SOURCE_RELATIVE_PATH = "src/canard_control/leaky_outer_signed_kernel_stage2.py"
GENERATOR_RELATIVE_PATH = "experiments/leaky_outer_signed_kernel_stage2.py"
RESULT_RELATIVE_PATH = "experiments/results/leaky_outer_signed_kernel_stage2.json"
NOTE_RELATIVE_PATH = "docs/leaky-outer-signed-kernel-stage2.md"
TEST_RELATIVE_PATH = "tests/test_leaky_outer_signed_kernel_stage2.py"
SOURCE_MANIFEST = (
    SOURCE_RELATIVE_PATH,
    GENERATOR_RELATIVE_PATH,
    NOTE_RELATIVE_PATH,
    "src/canard_control/directed_interval.py",
    "src/canard_control/leaky_outer_phase_fixed_return_stage1.py",
    "src/canard_control/leaky_outer_high_resolution.py",
    "src/canard_control/leaky_pulse_separator_candidate.py",
)
DEFAULT_COMMAND = (
    "OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONPATH=build/testdeps:src "
    "/usr/bin/python3 experiments/leaky_outer_signed_kernel_stage2.py"
)
ARITHMETIC_SCOPE = (
    "exact stored binary64 outer orbit and RK4/cubic-interpolation monodromy; "
    "160-bit outward MPFR phase ratios, coefficient differences, cellwise "
    "absolute values, and row sums; exact JSON/source/parent binding.  The "
    "continuous density propagation and discretization error are not enclosed"
)

OUTER_RESULT_SHA256 = (
    "d888916fed919f1515dd31ab851b2229816ea373365fa0221b1e345580f165a7"
)
STAGE1_RESULT_SHA256 = (
    "45cdab890a27698c0929e7a78319333ba886866cf9339756926c5b2979ca6007"
)
PRECISION_BITS = 160
STEP_COUNT = 360
PINNED_OPENBLAS_NUM_THREADS = "1"

TRUE_FLAGS = (
    "stage1_phase_fixed_contract_parent_validated",
    "stored_fourier_tangent_used_instead_of_numerical_eigenvector",
    "binary_method_of_steps_atomic_shadow_computed",
    "directed_mpfr_phase_subtraction_per_input_cell_computed",
    "directed_total_variation_summed_only_after_phase_subtraction",
    "fixed_time_and_phase_terms_separately_audited",
    "physical_history_rows_distinguished_from_interpolation_padding",
    "continuous_dirac_density_scalar_decomposition_registered",
    "current_voltage_dirac_atom_killed_exactly_by_section_constraint",
    "continuous_volterra_kernel_recurrence_registered",
    "phase_chart_discrete_norm_pilot_computed",
)
FALSE_FLAGS = (
    "binary_atomic_shadow_promoted_to_continuous_history_operator",
    "continuous_density_interval_method_of_steps_validated",
    "continuous_density_cellwise_total_variation_validated",
    "exact_orbit_to_stored_kernel_transfer_error_validated",
    "arbitrary_c0_input_covered_by_directed_kernel",
    "phase_fixed_outer_return_linear_contraction_validated",
    "continuous_phase_chart_norm_validated",
    "outer_return_second_variation_validated",
    "outer_nonlinear_return_contraction_validated",
    "outer_quantitative_attracting_tube_validated",
    "pulse_to_outer_section_entry_validated",
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


def _binary64_record(value: float) -> dict[str, str]:
    number = float(value)
    if not math.isfinite(number):
        raise ValueError("binary64 records must be finite")
    return {"binary64_hex": number.hex(), "decimal": format(number, ".17g")}


def _binary64_value(value: Any, name: str) -> float:
    record = _mapping(value, name)
    if set(record) != {"binary64_hex", "decimal"}:
        raise ValueError(f"{name} is not a complete binary64 record")
    hexadecimal = record.get("binary64_hex")
    decimal = record.get("decimal")
    if not isinstance(hexadecimal, str) or not isinstance(decimal, str):
        raise ValueError(f"{name} fields must be strings")
    try:
        number = float.fromhex(hexadecimal)
    except ValueError as error:
        raise ValueError(f"{name} hexadecimal field is invalid") from error
    if (
        not math.isfinite(number)
        or number.hex() != hexadecimal
        or format(number, ".17g") != decimal
    ):
        raise ValueError(f"{name} binary64 fields disagree")
    return number


def _decimal(value: str | None, name: str) -> Decimal | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError(f"{name} must be a decimal string or null")
    try:
        number = Decimal(value)
    except InvalidOperation as error:
        raise ValueError(f"{name} is not a decimal") from error
    if not number.is_finite() or number < 0:
        raise ValueError(f"{name} must be finite and nonnegative")
    return number


def _upper_decimal(value: Decimal) -> str:
    with localcontext() as context:
        context.prec = 96
        context.rounding = ROUND_CEILING
        return format(+value, "f")


def _lower_decimal(value: Decimal) -> str:
    with localcontext() as context:
        context.prec = 96
        context.rounding = ROUND_FLOOR
        return format(+value, "f")


def _mpfr_sum_upper(values: Sequence[gmpy2.mpfr]) -> gmpy2.mpfr:
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
        total = gmpy2.mpfr(0)
        for value in values:
            total += value
        return +total


def _mpfr_difference_lower(left: gmpy2.mpfr, right: gmpy2.mpfr) -> gmpy2.mpfr:
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundDown):
        return left - right


def _interval_digest(intervals: Sequence[DirectedInterval]) -> str:
    body = [
        (
            decimal_lower(interval.lower, 60),
            decimal_upper(interval.upper, 60),
        )
        for interval in intervals
    ]
    return canonical_sha256(body)


@dataclass(frozen=True)
class DirectedOutputRowAudit:
    output_id: str
    output_kind: str
    original_matrix_row: int
    physical_relative_time_binary64: dict[str, str] | None
    history_input_cell_count: int
    interpolation_padding_input_cell_count: int
    directed_sign_definite_corrected_cell_count: int
    directed_zero_containing_corrected_cell_count: int
    fixed_time_history_mass_tv_upper: str
    fixed_time_recovery_scalar_abs_upper: str
    fixed_time_total_row_norm_upper: str
    phase_term_history_mass_tv_upper: str
    phase_term_recovery_scalar_abs_upper: str
    phase_term_total_row_norm_upper: str
    corrected_history_mass_tv_upper: str
    corrected_recovery_scalar_abs_upper: str
    corrected_total_row_norm_upper: str
    corrected_padding_mass_tv_upper: str
    corrected_cell_interval_sha256: str


@dataclass(frozen=True)
class SignedKernelTransferBudget:
    voltage_continuous_transfer_error_upper: str | None
    recovery_continuous_transfer_error_upper: str | None
    phase_chart_continuous_transfer_error_upper: str | None
    continuous_density_interval_method_of_steps_validated: bool
    exact_orbit_coefficient_and_period_transfer_validated: bool
    arbitrary_c0_dual_measure_identity_validated: bool
    continuous_phase_subtraction_before_total_variation_validated: bool
    evidence_status: str


@dataclass(frozen=True)
class SignedKernelTransferEvaluation:
    input_complete: bool
    missing_numeric_inputs: tuple[str, ...]
    missing_proof_inputs: tuple[str, ...]
    continuous_voltage_row_norm_upper: str | None
    continuous_recovery_row_norm_upper: str | None
    continuous_phase_fixed_operator_norm_upper: str | None
    continuous_phase_chart_norm_upper: str | None
    remaining_linear_contraction_margin_lower: str | None
    strict_linear_contraction_inequality_holds: bool
    arbitrary_c0_linear_contraction_closes: bool
    sufficient_inequality: str


@dataclass(frozen=True)
class OuterSignedKernelStage2:
    schema_id: str
    model_id: str
    branch: str
    arithmetic_scope: str
    precision_bits: int
    binary_blas_thread_count: int
    parent_result_sha256: dict[str, str]
    step_count: int
    matrix_dimension: int
    history_step_count_including_padding: int
    physical_history_first_matrix_index: int
    interpolation_padding_cell_count: int
    physical_step_binary64: dict[str, str]
    stored_phase_speed_binary64: dict[str, str]
    directed_output_rows: tuple[DirectedOutputRowAudit, ...]
    directed_voltage_shadow_norm_upper: str
    directed_recovery_shadow_norm_upper: str
    directed_phase_fixed_shadow_norm_upper: str
    directed_fixed_time_shadow_norm_upper: str
    directed_rank_one_phase_shadow_norm_upper: str
    separate_triangle_shadow_norm_upper: str
    directed_cancellation_factor_lower: str
    directed_padding_mass_maximum_upper: str
    directed_phase_chart_shadow_norm_upper: str
    discrete_shadow_remaining_margin_below_one_lower: str
    continuous_kernel_decomposition: dict[str, Any]
    directed_cell_enclosure_contract: dict[str, Any]
    transfer_budget: SignedKernelTransferBudget
    transfer_evaluation: SignedKernelTransferEvaluation
    claim_status: dict[str, bool]
    conclusion: str


def evaluate_signed_kernel_transfer(
    *,
    discrete_voltage_upper: str,
    discrete_recovery_upper: str,
    discrete_phase_chart_upper: str,
    budget: SignedKernelTransferBudget,
) -> SignedKernelTransferEvaluation:
    qv = _decimal(discrete_voltage_upper, "discrete_voltage_upper")
    qw = _decimal(discrete_recovery_upper, "discrete_recovery_upper")
    qphase = _decimal(discrete_phase_chart_upper, "discrete_phase_chart_upper")
    assert qv is not None and qw is not None and qphase is not None
    numeric_names = (
        "voltage_continuous_transfer_error_upper",
        "recovery_continuous_transfer_error_upper",
        "phase_chart_continuous_transfer_error_upper",
    )
    missing_numeric = tuple(
        name for name in numeric_names if getattr(budget, name) is None
    )
    proof_names = (
        "continuous_density_interval_method_of_steps_validated",
        "exact_orbit_coefficient_and_period_transfer_validated",
        "arbitrary_c0_dual_measure_identity_validated",
        "continuous_phase_subtraction_before_total_variation_validated",
    )
    missing_proof = tuple(name for name in proof_names if not getattr(budget, name))
    ev = _decimal(
        budget.voltage_continuous_transfer_error_upper,
        "voltage_continuous_transfer_error_upper",
    )
    ew = _decimal(
        budget.recovery_continuous_transfer_error_upper,
        "recovery_continuous_transfer_error_upper",
    )
    ep = _decimal(
        budget.phase_chart_continuous_transfer_error_upper,
        "phase_chart_continuous_transfer_error_upper",
    )
    voltage_text: str | None = None
    recovery_text: str | None = None
    operator_text: str | None = None
    phase_text: str | None = None
    margin_text: str | None = None
    strict = False
    if not missing_numeric:
        assert ev is not None and ew is not None and ep is not None
        with localcontext() as context:
            context.prec = 96
            context.rounding = ROUND_CEILING
            voltage = qv + ev
            recovery = qw + ew
            operator = max(voltage, recovery)
            phase = qphase + ep
        with localcontext() as context:
            context.prec = 96
            context.rounding = ROUND_FLOOR
            margin = Decimal(1) - operator
        voltage_text = _upper_decimal(voltage)
        recovery_text = _upper_decimal(recovery)
        operator_text = _upper_decimal(operator)
        phase_text = _upper_decimal(phase)
        margin_text = _lower_decimal(margin)
        strict = operator < 1
    closes = not missing_numeric and not missing_proof and strict
    return SignedKernelTransferEvaluation(
        input_complete=not missing_numeric and not missing_proof,
        missing_numeric_inputs=missing_numeric,
        missing_proof_inputs=missing_proof,
        continuous_voltage_row_norm_upper=voltage_text,
        continuous_recovery_row_norm_upper=recovery_text,
        continuous_phase_fixed_operator_norm_upper=operator_text,
        continuous_phase_chart_norm_upper=phase_text,
        remaining_linear_contraction_margin_lower=margin_text,
        strict_linear_contraction_inequality_holds=strict,
        arbitrary_c0_linear_contraction_closes=closes,
        sufficient_inequality=(
            "max(Qv_shadow+E_voltage,Qw_shadow+E_recovery) < 1"
        ),
    )


def _load_parent(repository: Path, relative: str, expected: str) -> Mapping[str, Any]:
    path = repository / relative
    if _sha256_path(path) != expected:
        raise ValueError(f"a signed-kernel parent changed: {relative}")
    return _mapping(json.loads(path.read_text()), relative)


def _row_audit(
    *,
    matrix: np.ndarray,
    tangent: np.ndarray,
    phase_row_index: int,
    input_indices: np.ndarray,
    padding_indices: set[int],
    output_index: int,
    output_kind: str,
    output_id: str,
    relative_time: float | None,
) -> tuple[DirectedOutputRowAudit, gmpy2.mpfr, gmpy2.mpfr, gmpy2.mpfr]:
    phase_speed = DirectedInterval.from_float(
        float(tangent[phase_row_index]), PRECISION_BITS
    )
    tangent_row = DirectedInterval.from_float(
        float(tangent[output_index]), PRECISION_BITS
    )
    fixed_intervals: list[DirectedInterval] = []
    phase_intervals: list[DirectedInterval] = []
    corrected_intervals: list[DirectedInterval] = []
    for input_index in input_indices:
        fixed = DirectedInterval.from_float(
            float(matrix[output_index, input_index]), PRECISION_BITS
        )
        phase = (
            tangent_row
            * DirectedInterval.from_float(
                float(matrix[phase_row_index, input_index]), PRECISION_BITS
            )
            / phase_speed
        )
        fixed_intervals.append(fixed)
        phase_intervals.append(phase)
        corrected_intervals.append(fixed - phase)

    history_count = len(input_indices) - 1
    fixed_history = _mpfr_sum_upper(
        [interval.upper_abs() for interval in fixed_intervals[:history_count]]
    )
    phase_history = _mpfr_sum_upper(
        [interval.upper_abs() for interval in phase_intervals[:history_count]]
    )
    corrected_history = _mpfr_sum_upper(
        [interval.upper_abs() for interval in corrected_intervals[:history_count]]
    )
    fixed_scalar = fixed_intervals[-1].upper_abs()
    phase_scalar = phase_intervals[-1].upper_abs()
    corrected_scalar = corrected_intervals[-1].upper_abs()
    fixed_total = _mpfr_sum_upper((fixed_history, fixed_scalar))
    phase_total = _mpfr_sum_upper((phase_history, phase_scalar))
    corrected_total = _mpfr_sum_upper((corrected_history, corrected_scalar))
    padding_positions = [
        position
        for position, original in enumerate(input_indices[:-1])
        if int(original) in padding_indices
    ]
    padding_total = _mpfr_sum_upper(
        [corrected_intervals[position].upper_abs() for position in padding_positions]
    )
    sign_definite = sum(
        not interval.contains_zero() for interval in corrected_intervals
    )
    zero_containing = len(corrected_intervals) - sign_definite
    audit = DirectedOutputRowAudit(
        output_id=output_id,
        output_kind=output_kind,
        original_matrix_row=output_index,
        physical_relative_time_binary64=(
            None if relative_time is None else _binary64_record(relative_time)
        ),
        history_input_cell_count=history_count,
        interpolation_padding_input_cell_count=len(padding_positions),
        directed_sign_definite_corrected_cell_count=sign_definite,
        directed_zero_containing_corrected_cell_count=zero_containing,
        fixed_time_history_mass_tv_upper=decimal_upper(fixed_history, 60),
        fixed_time_recovery_scalar_abs_upper=decimal_upper(fixed_scalar, 60),
        fixed_time_total_row_norm_upper=decimal_upper(fixed_total, 60),
        phase_term_history_mass_tv_upper=decimal_upper(phase_history, 60),
        phase_term_recovery_scalar_abs_upper=decimal_upper(phase_scalar, 60),
        phase_term_total_row_norm_upper=decimal_upper(phase_total, 60),
        corrected_history_mass_tv_upper=decimal_upper(corrected_history, 60),
        corrected_recovery_scalar_abs_upper=decimal_upper(corrected_scalar, 60),
        corrected_total_row_norm_upper=decimal_upper(corrected_total, 60),
        corrected_padding_mass_tv_upper=decimal_upper(padding_total, 60),
        corrected_cell_interval_sha256=_interval_digest(corrected_intervals),
    )
    return audit, fixed_total, phase_total, corrected_total


def _phase_chart_shadow_upper(
    tangent: np.ndarray,
    phase_row_index: int,
    physical_output_indices: Sequence[int],
) -> gmpy2.mpfr:
    speed = DirectedInterval.from_float(
        float(tangent[phase_row_index]), PRECISION_BITS
    )
    rows: list[gmpy2.mpfr] = []
    one = DirectedInterval.from_decimal(1, PRECISION_BITS)
    for output_index in physical_output_indices:
        ratio = DirectedInterval.from_float(
            float(tangent[output_index]), PRECISION_BITS
        ) / speed
        rows.append(_mpfr_sum_upper((one.upper, ratio.upper_abs())))
    return max(rows)


def build_outer_signed_kernel_stage2(repository: Path) -> OuterSignedKernelStage2:
    repository = repository.resolve()
    if os.environ.get("OPENBLAS_NUM_THREADS") != PINNED_OPENBLAS_NUM_THREADS:
        raise RuntimeError("Stage-2 requires OPENBLAS_NUM_THREADS=1")
    stage1 = _load_parent(
        repository, STAGE1_RESULT_RELATIVE_PATH, STAGE1_RESULT_SHA256
    )
    validate_outer_phase_fixed_return_result(stage1, repository)
    outer = _load_parent(repository, OUTER_RESULT_RELATIVE_PATH, OUTER_RESULT_SHA256)
    orbit = validate_outer_high_resolution_artifact(
        outer, repository, replay_directed=False
    )
    section = finite_section(orbit, STEP_COUNT)
    _, voltage_derivative = _periodic_interpolator(
        orbit.state[:, 0], orbit.period
    )
    _, recovery_derivative = _periodic_interpolator(
        orbit.state[:, 1], orbit.period
    )
    history_steps = section.history_steps
    dimension = section.matrix.shape[0]
    if dimension != history_steps + 2:
        raise ArithmeticError("the finite method-of-steps dimension changed")
    tangent = np.asarray(
        [
            voltage_derivative((index - history_steps) * section.step)
            for index in range(history_steps + 1)
        ]
        + [recovery_derivative(0.0)],
        dtype=float,
    )
    phase_index = history_steps
    if tangent[phase_index] <= 0:
        raise ArithmeticError("the current-voltage phase speed lost orientation")
    first_physical = int(
        math.ceil(history_steps - TAU_1 / section.step - 1.0e-12)
    )
    if first_physical < 0 or first_physical >= phase_index:
        raise ArithmeticError("the physical-history/padding split changed")
    padding_indices = set(range(first_physical))
    history_input_indices = np.asarray(
        [index for index in range(history_steps + 1) if index != phase_index],
        dtype=int,
    )
    input_indices = np.concatenate(
        (history_input_indices, np.asarray([dimension - 1], dtype=int))
    )
    physical_voltage_outputs = tuple(range(first_physical, phase_index))
    output_rows: list[DirectedOutputRowAudit] = []
    fixed_totals: list[gmpy2.mpfr] = []
    phase_totals: list[gmpy2.mpfr] = []
    voltage_totals: list[gmpy2.mpfr] = []
    for output_index in physical_voltage_outputs:
        audit, fixed, phase, corrected = _row_audit(
            matrix=section.matrix,
            tangent=tangent,
            phase_row_index=phase_index,
            input_indices=input_indices,
            padding_indices=padding_indices,
            output_index=output_index,
            output_kind="returned_voltage_history",
            output_id=f"voltage_{output_index:03d}",
            relative_time=(output_index - history_steps) * section.step,
        )
        output_rows.append(audit)
        fixed_totals.append(fixed)
        phase_totals.append(phase)
        voltage_totals.append(corrected)
    recovery_index = dimension - 1
    recovery_audit, recovery_fixed, recovery_phase, recovery_total = _row_audit(
        matrix=section.matrix,
        tangent=tangent,
        phase_row_index=phase_index,
        input_indices=input_indices,
        padding_indices=padding_indices,
        output_index=recovery_index,
        output_kind="returned_current_recovery",
        output_id="recovery_current",
        relative_time=None,
    )
    output_rows.append(recovery_audit)
    fixed_totals.append(recovery_fixed)
    phase_totals.append(recovery_phase)
    qv = max(voltage_totals)
    qw = recovery_total
    q = max(qv, qw)
    fixed_max = max(fixed_totals)
    phase_max = max(phase_totals)
    triangle = _mpfr_sum_upper((fixed_max, phase_max))
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundDown):
        cancellation_factor = triangle / q
        remaining = gmpy2.mpfr(1) - q
    padding_max = max(
        gmpy2.mpfr(row.corrected_padding_mass_tv_upper) for row in output_rows
    )
    physical_phase_outputs = tuple(physical_voltage_outputs) + (recovery_index,)
    qphase = _phase_chart_shadow_upper(
        tangent, phase_index, physical_phase_outputs
    )
    qv_text = decimal_upper(qv, 60)
    qw_text = decimal_upper(qw, 60)
    qphase_text = decimal_upper(qphase, 60)
    budget = SignedKernelTransferBudget(
        voltage_continuous_transfer_error_upper=None,
        recovery_continuous_transfer_error_upper=None,
        phase_chart_continuous_transfer_error_upper=None,
        continuous_density_interval_method_of_steps_validated=False,
        exact_orbit_coefficient_and_period_transfer_validated=False,
        arbitrary_c0_dual_measure_identity_validated=False,
        continuous_phase_subtraction_before_total_variation_validated=False,
        evidence_status=(
            "open: the directed algebra is complete for the exact stored "
            "binary matrix, but a two-variable Volterra/interval-Taylor "
            "density enclosure and its exact-orbit transfer errors are absent"
        ),
    )
    evaluation = evaluate_signed_kernel_transfer(
        discrete_voltage_upper=qv_text,
        discrete_recovery_upper=qw_text,
        discrete_phase_chart_upper=qphase_text,
        budget=budget,
    )
    claims = {name: True for name in TRUE_FLAGS}
    claims.update({name: False for name in FALSE_FLAGS})
    return OuterSignedKernelStage2(
        schema_id=SCHEMA_ID,
        model_id=MODEL_ID,
        branch=BRANCH,
        arithmetic_scope=ARITHMETIC_SCOPE,
        precision_bits=PRECISION_BITS,
        binary_blas_thread_count=1,
        parent_result_sha256={
            STAGE1_RESULT_RELATIVE_PATH: STAGE1_RESULT_SHA256,
            OUTER_RESULT_RELATIVE_PATH: OUTER_RESULT_SHA256,
        },
        step_count=STEP_COUNT,
        matrix_dimension=dimension,
        history_step_count_including_padding=history_steps,
        physical_history_first_matrix_index=first_physical,
        interpolation_padding_cell_count=first_physical,
        physical_step_binary64=_binary64_record(section.step),
        stored_phase_speed_binary64=_binary64_record(float(tangent[phase_index])),
        directed_output_rows=tuple(output_rows),
        directed_voltage_shadow_norm_upper=qv_text,
        directed_recovery_shadow_norm_upper=qw_text,
        directed_phase_fixed_shadow_norm_upper=decimal_upper(q, 60),
        directed_fixed_time_shadow_norm_upper=decimal_upper(fixed_max, 60),
        directed_rank_one_phase_shadow_norm_upper=decimal_upper(phase_max, 60),
        separate_triangle_shadow_norm_upper=decimal_upper(triangle, 60),
        directed_cancellation_factor_lower=decimal_lower(cancellation_factor, 60),
        directed_padding_mass_maximum_upper=decimal_upper(padding_max, 60),
        directed_phase_chart_shadow_norm_upper=qphase_text,
        discrete_shadow_remaining_margin_below_one_lower=decimal_lower(
            remaining, 60
        ),
        continuous_kernel_decomposition={
            "variational_equation": (
                "x'(t)=A(t)x(t)+sum_j B_j(t)x(t-tau_j), with B_j having "
                "only its fast-row/current-voltage entry nonzero"
            ),
            "principal_resolvent": (
                "R(t,s)=0 for t<s, R(s,s)=I, and partial_t R=A(t)R+"
                "sum_j B_j(t)R(t-tau_j,s)"
            ),
            "current_voltage_dirac_atom": "R(t,0)e_v * Dirac_0",
            "history_density": (
                "K(t,theta)=sum_{j: -tau_j<=theta<=0} "
                "R(t,theta+tau_j)B_j(theta+tau_j)e_v"
            ),
            "initial_recovery_scalar_column": "c(t)=R(t,0)e_w",
            "section_constraint": (
                "h_v(0)=0 kills the sole current-voltage Dirac atom exactly"
            ),
            "returned_phase_subtraction": (
                "K_c(T+sigma,theta)=K(T+sigma,theta)-"
                "q(T+sigma)K_v(T,theta)/q_v(T), and likewise for c"
            ),
            "continuous_row_norm": (
                "integral_{-tau1}^0 |K_c,row(theta)| dtheta + "
                "|c_c,row|, after signed subtraction"
            ),
            "arbitrary_c0_coverage": (
                "Riesz representation: the induced C0-to-R row norm equals "
                "the signed-measure total variation plus the scalar-column norm"
            ),
        },
        directed_cell_enclosure_contract={
            "time_domain": "0<=s<=tau1 and T-tau1<=t<=T",
            "history_domain": "-tau1<=theta<=0",
            "cell_unknowns": (
                "interval Taylor/Bernstein enclosures of R(t,s), K(t,theta), "
                "c(t), and the exact-orbit tangent q(t)"
            ),
            "atom_ledger": (
                "store Dirac_0 separately; no other exact input-history atoms "
                "remain in the returned kernel because T-tau1>0"
            ),
            "density_ledger": (
                "each theta-cell stores signed lower/upper density bounds; "
                "phase subtraction precedes absolute-value/TV accumulation"
            ),
            "coefficient_scope": (
                "include the nested 1e-8 exact-orbit/period ball and physical "
                "unshifted delayed coefficients"
            ),
            "quadrature_scope": (
                "enclose cell integrals of absolute corrected densities, not "
                "samples of arbitrary input histories"
            ),
            "required_transfer_outputs": (
                "E_voltage, E_recovery, E_phase such that exact continuous "
                "row norms are bounded by the registered shadows plus E"
            ),
            "single_linear_gate": (
                "max(Qv_shadow+E_voltage,Qw_shadow+E_recovery)<1"
            ),
            "current_status": (
                "contract registered; no continuous interval density cells "
                "or transfer-error constants have yet been emitted"
            ),
        },
        transfer_budget=budget,
        transfer_evaluation=evaluation,
        claim_status=claims,
        conclusion=(
            "directed cellwise algebra proves a strong signed cancellation "
            "for the stored 360-step matrix, leaving more than 0.87 of linear "
            "margin; the sole remaining first-order proof object is a directed "
            "continuous density/atom transfer bound, so no C0 contraction is claimed"
        ),
    )


def build_outer_signed_kernel_stage2_result(repository: Path) -> dict[str, Any]:
    repository = repository.resolve()
    certificate = json.loads(
        json.dumps(
            asdict(build_outer_signed_kernel_stage2(repository)),
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


def validate_outer_signed_kernel_stage2_result(
    payload: Mapping[str, Any], repository: Path
) -> None:
    if not isinstance(payload, Mapping) or set(payload) != {"certificate", "manifest"}:
        raise ValueError("the signed-kernel Stage-2 result schema changed")
    certificate = _mapping(payload.get("certificate"), "Stage-2 certificate")
    manifest = _mapping(payload.get("manifest"), "Stage-2 manifest")
    if set(certificate) != {field.name for field in fields(OuterSignedKernelStage2)}:
        raise ValueError("the signed-kernel Stage-2 fields changed")
    if canonical_sha256(certificate) != manifest.get("certificate_sha256"):
        raise ValueError("the signed-kernel Stage-2 digest changed")
    if certificate.get("schema_id") != SCHEMA_ID or manifest.get("schema_id") != SCHEMA_ID:
        raise ValueError("the signed-kernel Stage-2 schema id changed")
    sources = _mapping(manifest.get("source_sha256"), "Stage-2 source manifest")
    if set(sources) != set(SOURCE_MANIFEST):
        raise ValueError("the signed-kernel Stage-2 source set changed")
    repository = repository.resolve()
    for relative in SOURCE_MANIFEST:
        if sources.get(relative) != _sha256_path(repository / relative):
            raise ValueError(f"a signed-kernel Stage-2 source changed: {relative}")
    claims = _mapping(certificate.get("claim_status"), "Stage-2 claim ledger")
    if set(claims) != set(TRUE_FLAGS + FALSE_FLAGS):
        raise ValueError("the signed-kernel Stage-2 claim ledger changed")
    if any(claims.get(name) is not True for name in TRUE_FLAGS):
        raise ValueError("a directed Stage-2 pilot fact was weakened")
    if any(claims.get(name) is not False for name in FALSE_FLAGS):
        raise ValueError("an open continuous-history claim was promoted")
    rows = certificate.get("directed_output_rows")
    if not isinstance(rows, list) or len(rows) < 100:
        raise ValueError("the directed per-output row ledger is missing")
    if rows[-1].get("output_kind") != "returned_current_recovery":
        raise ValueError("the directed recovery row is missing")
    for row in rows:
        if not isinstance(row, Mapping):
            raise ValueError("a directed output row is malformed")
        if row.get("history_input_cell_count") != certificate.get(
            "history_step_count_including_padding"
        ):
            raise ValueError("a directed row lost an input history cell")
        if row.get("interpolation_padding_input_cell_count") != certificate.get(
            "interpolation_padding_cell_count"
        ):
            raise ValueError("a directed row lost the padding ledger")
    if Decimal(str(certificate["directed_phase_fixed_shadow_norm_upper"])) >= Decimal("0.128"):
        raise ValueError("the directed signed cancellation pilot changed")
    if Decimal(str(certificate["separate_triangle_shadow_norm_upper"])) <= Decimal("5"):
        raise ValueError("the separate-term cancellation audit changed")
    evaluation = _mapping(
        certificate.get("transfer_evaluation"), "Stage-2 transfer evaluation"
    )
    if evaluation.get("input_complete") is not False or evaluation.get(
        "arbitrary_c0_linear_contraction_closes"
    ) is not False:
        raise ValueError("the incomplete continuous transfer was promoted")
    expected = json.loads(
        json.dumps(
            asdict(build_outer_signed_kernel_stage2(repository)),
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        )
    )
    if certificate != expected:
        raise ValueError("the signed-kernel Stage-2 certificate differs from replay")


__all__ = [
    "DEFAULT_COMMAND",
    "FALSE_FLAGS",
    "NOTE_RELATIVE_PATH",
    "RESULT_RELATIVE_PATH",
    "SOURCE_MANIFEST",
    "SignedKernelTransferBudget",
    "SignedKernelTransferEvaluation",
    "TRUE_FLAGS",
    "build_outer_signed_kernel_stage2",
    "build_outer_signed_kernel_stage2_result",
    "canonical_sha256",
    "evaluate_signed_kernel_transfer",
    "validate_outer_signed_kernel_stage2_result",
]
