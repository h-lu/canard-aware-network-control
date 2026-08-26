"""Stage-3E relative-residual certificate for the outer fundamental flow.

Stage 3D reduced every delay word to the one-dimensional primitives
``F,G,H,L``.  The first analytic obstruction left there was the transfer of
the binary guide for ``F`` to the exact orbit.  This module closes precisely
that obstruction.

On each normalized-phase cell a degree-24 centered Taylor polynomial
``Fhat`` is stored implicitly by its source-replay construction.  The
coefficient matrix is represented by a directed degree-12 Fourier--Taylor
polynomial plus a rigorous Fourier tail and Taylor remainder.  Before any
absolute value is taken, the code forms the matrix-polynomial numerator

    adj(Fhat) * (d_y Fhat - h A_exact Fhat).

The determinant of the *same* polynomial matrix is bounded away from zero.
The resulting relative residual, together with rigorously enclosed chart
jumps, gives a multiplicative propagator for
``Y=Fhat^{-1}F_exact``.  Thus both ``F`` and ``G=F^{-1}`` receive uniform
relative error bounds without an absolute logarithmic-norm Gronwall factor.

A deliberately coarse triangular consequence for abstract ``H`` and ``L``
primitives is also recorded.  It is rigorous, but it separates primitive
norms and therefore loses the signed word cancellation.  It is not a signed
kernel transfer certificate: ``E_voltage`` and ``E_recovery`` remain null.
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
    DirectedComplexInterval,
    DirectedInterval,
    complex_unit_interval,
    decimal_lower,
    decimal_upper,
    pi_interval,
)
from canard_control.leaky_outer_delay_word_stage3d_primitives import (
    RESULT_RELATIVE_PATH as STAGE3D_RESULT_RELATIVE_PATH,
)
from canard_control.leaky_outer_high_resolution import (
    RESULT_RELATIVE_PATH as OUTER_RESULT_RELATIVE_PATH,
    validate_outer_high_resolution_artifact,
)
from canard_control.leaky_outer_phase_fixed_return_stage1 import (
    _periodic_interpolator,
)
from canard_control.leaky_periodic_validation import _build_leaky_base_sequences
from canard_control.leaky_pulse_separator_candidate import (
    EPSILON,
    KAPPA_1,
    KAPPA_3,
)


SCHEMA_ID = "leaky-outer-delay-word-stage3e-relative-residual-v1"
MODEL_ID = "autonomous-leaky-recovery-two-delay-fhn-bistable-proposal"
BRANCH = "outer_pulse"
SOURCE_RELATIVE_PATH = (
    "src/canard_control/leaky_outer_delay_word_stage3e_relative_residual.py"
)
GENERATOR_RELATIVE_PATH = (
    "experiments/leaky_outer_delay_word_stage3e_relative_residual.py"
)
RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_outer_delay_word_stage3e_relative_residual.json"
)
NOTE_RELATIVE_PATH = "docs/leaky-outer-delay-word-stage3e-relative-residual.md"
TEST_RELATIVE_PATH = "tests/test_leaky_outer_delay_word_stage3e_relative_residual.py"
SOURCE_MANIFEST = (
    SOURCE_RELATIVE_PATH,
    GENERATOR_RELATIVE_PATH,
    NOTE_RELATIVE_PATH,
    "src/canard_control/directed_interval.py",
    "src/canard_control/leaky_outer_delay_word_stage3d_primitives.py",
    "src/canard_control/leaky_outer_high_resolution.py",
    "src/canard_control/leaky_outer_phase_fixed_return_stage1.py",
    "src/canard_control/leaky_periodic_validation.py",
    "src/canard_control/leaky_pulse_separator_candidate.py",
)
DEFAULT_COMMAND = (
    "OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONPATH=build/testdeps:src "
    "/usr/bin/python3 "
    "experiments/leaky_outer_delay_word_stage3e_relative_residual.py"
)
ARITHMETIC_SCOPE = (
    "160-bit outward MPFR Fourier-Taylor coefficient and tail arithmetic; "
    "degree-24 source-replayed binary64 guide coefficients treated as exact "
    "dyadic constants; same-cell signed matrix-polynomial residual, "
    "determinant, interface-jump and multiplicative-error propagation"
)

STAGE3D_RESULT_SHA256 = (
    "11197f7f64289bd239f6167deedae66e54bc7805eaf84d08762ddc843c7372bf"
)
OUTER_RESULT_SHA256 = (
    "d888916fed919f1515dd31ab851b2229816ea373365fa0221b1e345580f165a7"
)
PRECISION_BITS = 160
PINNED_OPENBLAS_NUM_THREADS = "1"
EXACT_ORBIT_RADIUS = "1e-8"
PHASE_CELL_COUNT = 1024
FUNDAMENTAL_DEGREE = 24
COEFFICIENT_TAYLOR_DEGREE = 12
FOURIER_CUTOFF = 96
GUIDE_MAXIMUM_STEP = 0.01

TRUE_FLAGS = (
    "stage3d_primitive_parent_validated",
    "exact_orbit_and_period_ball_included",
    "degree24_fundamental_chart_constructed",
    "retained_fourier_taylor_coefficients_directed",
    "omitted_fourier_tail_directed",
    "fourier_taylor_remainder_directed",
    "same_cell_matrix_correlation_retained",
    "relative_residual_numerator_signed_before_norm",
    "polynomial_determinant_nonvanishing_validated",
    "all_chart_interface_jumps_directed",
    "multiplicative_F_error_propagator_validated",
    "multiplicative_G_error_propagator_validated",
    "abstract_H_L_triangular_majorant_validated",
)
FALSE_FLAGS = (
    "abstract_H_L_majorant_promoted_to_signed_kernel_transfer",
    "binary_H_L_guides_transferred_to_exact_primitives",
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

IntervalMatrix = tuple[
    tuple[DirectedInterval, DirectedInterval],
    tuple[DirectedInterval, DirectedInterval],
]


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
        raise ValueError(f"a Stage-3E parent changed: {relative}")
    return _mapping(json.loads(path.read_text()), relative)


def _zero() -> DirectedInterval:
    return DirectedInterval.from_decimal(0, PRECISION_BITS)


def _one() -> DirectedInterval:
    return DirectedInterval.from_decimal(1, PRECISION_BITS)


def _point(value: float) -> DirectedInterval:
    return DirectedInterval.from_float(float(value), PRECISION_BITS)


def _zero_matrix() -> IntervalMatrix:
    zero = _zero()
    return ((zero, zero), (zero, zero))


def _identity_matrix() -> IntervalMatrix:
    zero = _zero()
    one = _one()
    return ((one, zero), (zero, one))


def _float_matrix(value: np.ndarray) -> IntervalMatrix:
    array = np.asarray(value, dtype=float)
    if array.shape != (2, 2):
        raise ValueError("a Stage-3E guide coefficient is not 2 by 2")
    return tuple(
        tuple(_point(array[i, j]) for j in range(2)) for i in range(2)
    )  # type: ignore[return-value]


def _matrix_add(left: IntervalMatrix, right: IntervalMatrix) -> IntervalMatrix:
    return tuple(
        tuple(left[i][j] + right[i][j] for j in range(2))
        for i in range(2)
    )  # type: ignore[return-value]


def _matrix_sub(left: IntervalMatrix, right: IntervalMatrix) -> IntervalMatrix:
    return tuple(
        tuple(left[i][j] - right[i][j] for j in range(2))
        for i in range(2)
    )  # type: ignore[return-value]


def _matrix_scale(matrix: IntervalMatrix, scalar: object) -> IntervalMatrix:
    return tuple(
        tuple(value * scalar for value in row) for row in matrix
    )  # type: ignore[return-value]


def _matrix_multiply(left: IntervalMatrix, right: IntervalMatrix) -> IntervalMatrix:
    return tuple(
        tuple(
            left[i][0] * right[0][j] + left[i][1] * right[1][j]
            for j in range(2)
        )
        for i in range(2)
    )  # type: ignore[return-value]


def _matrix_adjugate(matrix: IntervalMatrix) -> IntervalMatrix:
    return (
        (matrix[1][1], -matrix[0][1]),
        (-matrix[1][0], matrix[0][0]),
    )


def _matrix_inf_norm_upper(matrix: IntervalMatrix) -> gmpy2.mpfr:
    rows: list[gmpy2.mpfr] = []
    for row in matrix:
        with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
            rows.append(row[0].upper_abs() + row[1].upper_abs())
    return max(rows)


def _polynomial_matrix_inf_norm_upper(
    coefficients: Sequence[IntervalMatrix],
) -> gmpy2.mpfr:
    rows: list[gmpy2.mpfr] = []
    for row in range(2):
        with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
            total = gmpy2.mpfr(0)
            for matrix in coefficients:
                total += matrix[row][0].upper_abs()
                total += matrix[row][1].upper_abs()
        rows.append(total)
    return max(rows)


def _polynomial_matrix_evaluate(
    coefficients: Sequence[IntervalMatrix], sign: int
) -> IntervalMatrix:
    if sign not in (-1, 1):
        raise ValueError("a centered endpoint sign must be -1 or 1")
    answer = _zero_matrix()
    factor = 1
    for coefficient in coefficients:
        answer = _matrix_add(answer, _matrix_scale(coefficient, factor))
        factor *= sign
    return answer


def _polynomial_matrix_product(
    left: Sequence[IntervalMatrix], right: Sequence[IntervalMatrix]
) -> tuple[IntervalMatrix, ...]:
    answer = [_zero_matrix() for _ in range(len(left) + len(right) - 1)]
    for left_index, left_value in enumerate(left):
        for right_index, right_value in enumerate(right):
            index = left_index + right_index
            answer[index] = _matrix_add(
                answer[index], _matrix_multiply(left_value, right_value)
            )
    return tuple(answer)


def _scalar_polynomial_product(
    left: Sequence[DirectedInterval], right: Sequence[DirectedInterval]
) -> list[DirectedInterval]:
    answer = [_zero() for _ in range(len(left) + len(right) - 1)]
    for left_index, left_value in enumerate(left):
        for right_index, right_value in enumerate(right):
            index = left_index + right_index
            answer[index] = answer[index] + left_value * right_value
    return answer


def _determinant_polynomial(
    coefficients: Sequence[IntervalMatrix],
) -> tuple[DirectedInterval, ...]:
    a = [value[0][0] for value in coefficients]
    b = [value[0][1] for value in coefficients]
    c = [value[1][0] for value in coefficients]
    d = [value[1][1] for value in coefficients]
    ad = _scalar_polynomial_product(a, d)
    bc = _scalar_polynomial_product(b, c)
    return tuple(left - right for left, right in zip(ad, bc, strict=True))


def _centered_polynomial_lower_abs(
    coefficients: Sequence[DirectedInterval],
) -> gmpy2.mpfr:
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
        variation = gmpy2.mpfr(0)
        for coefficient in coefficients[1:]:
            variation += coefficient.upper_abs()
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundDown):
        return coefficients[0].lower_abs() - variation


def _integrated_polynomial_matrix_inf_norm_upper(
    coefficients: Sequence[IntervalMatrix],
) -> gmpy2.mpfr:
    rows: list[gmpy2.mpfr] = []
    for row in range(2):
        with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
            total = gmpy2.mpfr(0)
            for degree, matrix in enumerate(coefficients):
                weight = gmpy2.mpfr(2) / (degree + 1)
                total += weight * matrix[row][0].upper_abs()
                total += weight * matrix[row][1].upper_abs()
        rows.append(total)
    return max(rows)


def _wiener_norm_upper(sequence: Mapping[int, DirectedComplexInterval]) -> gmpy2.mpfr:
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
        total = gmpy2.mpfr(0)
        for value in sequence.values():
            total += value.upper_abs()
    return total


class _FundamentalGuide:
    """Binary64 center used only to choose the exact dyadic polynomial."""

    def __init__(self, orbit: Any):
        self.period = float(orbit.period)
        self.voltage, _ = _periodic_interpolator(orbit.state[:, 0], orbit.period)
        self.solution = solve_ivp(
            self._rhs,
            (0.0, self.period),
            np.eye(2).ravel(),
            method="DOP853",
            rtol=2.0e-13,
            atol=2.0e-15,
            max_step=GUIDE_MAXIMUM_STEP,
            dense_output=True,
        )
        if not self.solution.success:
            raise ArithmeticError("the Stage-3E binary guide failed")

    def _rhs(self, time: float, value: np.ndarray) -> np.ndarray:
        voltage = self.voltage(time)
        coefficient = 1.0 - voltage * voltage - EPSILON * (
            KAPPA_1 + 3.0 * KAPPA_3 * (voltage - 1.0) ** 2
        )
        matrix = np.asarray(
            ((coefficient, -1.0), (EPSILON, -EPSILON)), dtype=float
        )
        return (matrix @ value.reshape(2, 2)).ravel()

    def F(self, phase: float) -> np.ndarray:
        return np.asarray(self.solution.sol(self.period * phase)).reshape(2, 2)


@dataclass(frozen=True)
class FundamentalResidualCertificate:
    phase_cell_count: int
    fundamental_polynomial_degree: int
    coefficient_taylor_degree: int
    retained_fourier_cutoff: int
    retained_fourier_mode_count: int
    omitted_fourier_wiener_tail_upper: str
    coefficient_taylor_remainder_upper: str
    exact_orbit_coefficient_variation_upper: str
    exact_period_matrix_variation_upper: str
    minimum_polynomial_determinant_abs_lower: str
    maximum_Fhat_inf_norm_upper: str
    maximum_Ghat_inf_norm_upper: str
    maximum_polynomial_condition_upper: str
    central_polynomial_residual_exponent_upper: str
    omitted_fourier_tail_exponent_upper: str
    coefficient_taylor_remainder_exponent_upper: str
    exact_orbit_ball_exponent_upper: str
    exact_period_ball_exponent_upper: str
    interface_jump_log_exponent_upper: str
    maximum_interface_relative_jump_upper: str
    total_multiplicative_exponent_upper: str
    F_right_relative_error_upper: str
    G_left_relative_error_upper: str
    determinant_nonvanishing_on_every_cell: bool
    chart_interfaces_included: bool
    source_replayed_binary_guide_is_nonclaim_center: bool


@dataclass(frozen=True)
class OuterDelayWordStage3ERelativeResidual:
    schema_id: str
    model_id: str
    branch: str
    arithmetic_scope: str
    precision_bits: int
    binary_blas_thread_count: int
    parent_result_sha256: dict[str, str]
    relative_residual_identity: dict[str, Any]
    fundamental_certificate: FundamentalResidualCertificate
    triangular_primitive_propagation: dict[str, Any]
    signed_kernel_frontier: dict[str, Any]
    transfer_errors: dict[str, str | None]
    transfer_gate: dict[str, Any]
    claim_status: dict[str, bool]
    conclusion: str


def _coefficient_variations(base: Any) -> dict[str, gmpy2.mpfr]:
    radius = DirectedInterval.from_decimal(EXACT_ORBIT_RADIUS, PRECISION_BITS).upper
    v_norm = _wiener_norm_upper(base.voltage)
    centered_norm = _wiener_norm_upper(base.centered_voltage)
    current_norm = _wiener_norm_upper(base.current_coefficient)
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
        orbit_current = (
            (2 * v_norm + radius) * radius
            + 3
            * base.parameters["epsilon"].upper
            * base.parameters["kappa_3"].upper
            * (2 * centered_norm + radius)
            * radius
        )
        orbit_delay = (
            3
            * base.parameters["epsilon"].upper
            * base.parameters["kappa_3"].upper
            / 2
            * (2 * centered_norm + radius)
            * radius
        )
        orbit_matrix = (base.period.upper + radius) * orbit_current
        period_row_zero = radius * (current_norm + 1)
        period_row_one = radius * 2 * base.parameters["epsilon"].upper
        period_matrix = max(period_row_zero, period_row_one)
    return {
        "radius": radius,
        "current_norm": current_norm,
        "orbit_current": orbit_current,
        "orbit_delay": orbit_delay,
        "orbit_matrix": orbit_matrix,
        "period_matrix": period_matrix,
    }


def _fourier_tail_and_taylor_remainder(
    base: Any,
) -> tuple[gmpy2.mpfr, gmpy2.mpfr, int]:
    pi = pi_interval(PRECISION_BITS)
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
        tail = gmpy2.mpfr(0)
        remainder = gmpy2.mpfr(0)
        retained = 0
        factorial = gmpy2.fac(COEFFICIENT_TAYLOR_DEGREE + 1)
        for mode, coefficient in base.current_coefficient.items():
            magnitude = coefficient.upper_abs()
            if abs(mode) > FOURIER_CUTOFF:
                tail += magnitude
                continue
            retained += 1
            lam = pi.upper * abs(mode) / PHASE_CELL_COUNT
            remainder += magnitude * lam ** (COEFFICIENT_TAYLOR_DEGREE + 1) / factorial
    return tail, remainder, retained


def _cell_coefficient_polynomial(base: Any, cell: int) -> tuple[IntervalMatrix, ...]:
    pi = pi_interval(PRECISION_BITS)
    zero = _zero()
    one = _one()
    scalar_coefficients = [
        DirectedComplexInterval.zero(PRECISION_BITS)
        for _ in range(COEFFICIENT_TAYLOR_DEGREE + 1)
    ]
    for mode, coefficient in base.current_coefficient.items():
        if abs(mode) > FOURIER_CUTOFF:
            continue
        angle = pi * (mode * (2 * cell + 1)) / PHASE_CELL_COUNT
        factor = complex_unit_interval(angle)
        lam = DirectedComplexInterval(zero, pi * mode / PHASE_CELL_COUNT)
        scalar_coefficients[0] = scalar_coefficients[0] + coefficient * factor
        for degree in range(1, COEFFICIENT_TAYLOR_DEGREE + 1):
            factor = factor * lam * (one / degree)
            scalar_coefficients[degree] = (
                scalar_coefficients[degree] + coefficient * factor
            )
    answer: list[IntervalMatrix] = []
    for degree, scalar in enumerate(scalar_coefficients):
        fast = base.period * scalar.real
        if degree == 0:
            answer.append(
                (
                    (fast, -base.period),
                    (
                        base.period * base.parameters["epsilon"],
                        -(base.period * base.parameters["epsilon"]),
                    ),
                )
            )
        else:
            answer.append(((fast, zero), (zero, zero)))
    return tuple(answer)


def _midpoint_float_matrix(matrix: IntervalMatrix) -> np.ndarray:
    return np.asarray(
        [
            [float(matrix[i][j].midpoint_nearest()) for j in range(2)]
            for i in range(2)
        ],
        dtype=float,
    )


def _guide_polynomial(
    guide: _FundamentalGuide,
    coefficient: Sequence[IntervalMatrix],
    cell: int,
) -> tuple[IntervalMatrix, ...]:
    center = (cell + 0.5) / PHASE_CELL_COUNT
    half = 1.0 / (2.0 * PHASE_CELL_COUNT)
    coefficient_midpoint = tuple(_midpoint_float_matrix(value) for value in coefficient)
    values: list[np.ndarray] = [guide.F(center)]
    for degree in range(FUNDAMENTAL_DEGREE):
        derivative = np.zeros((2, 2), dtype=float)
        for left_degree in range(min(degree, COEFFICIENT_TAYLOR_DEGREE) + 1):
            derivative += (
                coefficient_midpoint[left_degree]
                @ values[degree - left_degree]
            )
        values.append(half * derivative / (degree + 1))
    return tuple(_float_matrix(value) for value in values)


def _cell_residual(
    coefficient: Sequence[IntervalMatrix],
    fundamental: Sequence[IntervalMatrix],
) -> tuple[IntervalMatrix, ...]:
    half = DirectedInterval.from_decimal(1, PRECISION_BITS) / (
        2 * PHASE_CELL_COUNT
    )
    maximum_degree = COEFFICIENT_TAYLOR_DEGREE + FUNDAMENTAL_DEGREE
    answer: list[IntervalMatrix] = []
    for degree in range(maximum_degree + 1):
        derivative = (
            _matrix_scale(fundamental[degree + 1], degree + 1)
            if degree < FUNDAMENTAL_DEGREE
            else _zero_matrix()
        )
        product = _zero_matrix()
        first = max(0, degree - FUNDAMENTAL_DEGREE)
        last = min(COEFFICIENT_TAYLOR_DEGREE, degree)
        for left_degree in range(first, last + 1):
            product = _matrix_add(
                product,
                _matrix_multiply(
                    coefficient[left_degree], fundamental[degree - left_degree]
                ),
            )
        answer.append(_matrix_sub(derivative, _matrix_scale(product, half)))
    return tuple(answer)


def _relative_jump(
    new_chart: IntervalMatrix,
    old_chart: IntervalMatrix,
    determinant_lower: gmpy2.mpfr,
) -> gmpy2.mpfr:
    numerator = _matrix_multiply(
        _matrix_adjugate(new_chart), _matrix_sub(old_chart, new_chart)
    )
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
        return _matrix_inf_norm_upper(numerator) / determinant_lower


def _build_fundamental_certificate(
    base: Any, guide: _FundamentalGuide
) -> FundamentalResidualCertificate:
    tail, taylor_remainder, retained = _fourier_tail_and_taylor_remainder(base)
    variations = _coefficient_variations(base)
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
        tail_matrix = base.period.upper * tail
        taylor_matrix = base.period.upper * taylor_remainder

    central_exponent = gmpy2.mpfr(0, precision=PRECISION_BITS)
    tail_exponent = gmpy2.mpfr(0, precision=PRECISION_BITS)
    taylor_exponent = gmpy2.mpfr(0, precision=PRECISION_BITS)
    orbit_exponent = gmpy2.mpfr(0, precision=PRECISION_BITS)
    period_exponent = gmpy2.mpfr(0, precision=PRECISION_BITS)
    jump_exponent = gmpy2.mpfr(0, precision=PRECISION_BITS)
    minimum_determinant: gmpy2.mpfr | None = None
    maximum_f = gmpy2.mpfr(0, precision=PRECISION_BITS)
    maximum_g = gmpy2.mpfr(0, precision=PRECISION_BITS)
    maximum_condition = gmpy2.mpfr(0, precision=PRECISION_BITS)
    maximum_jump = gmpy2.mpfr(0, precision=PRECISION_BITS)
    previous_plus: IntervalMatrix | None = None
    identity = _identity_matrix()

    for cell in range(PHASE_CELL_COUNT):
        coefficient = _cell_coefficient_polynomial(base, cell)
        fundamental = _guide_polynomial(guide, coefficient, cell)
        determinant = _determinant_polynomial(fundamental)
        determinant_lower = _centered_polynomial_lower_abs(determinant)
        if determinant_lower <= 0:
            raise ArithmeticError(
                f"the Stage-3E polynomial determinant failed on cell {cell}"
            )
        minimum_determinant = (
            determinant_lower
            if minimum_determinant is None
            else min(minimum_determinant, determinant_lower)
        )
        adjugate = tuple(_matrix_adjugate(value) for value in fundamental)
        f_norm = _polynomial_matrix_inf_norm_upper(fundamental)
        adj_norm = _polynomial_matrix_inf_norm_upper(adjugate)
        with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
            g_norm = adj_norm / determinant_lower
            condition = f_norm * g_norm
            remainder_factor = condition / PHASE_CELL_COUNT
        maximum_f = max(maximum_f, f_norm)
        maximum_g = max(maximum_g, g_norm)
        maximum_condition = max(maximum_condition, condition)

        residual = _cell_residual(coefficient, fundamental)
        numerator = _polynomial_matrix_product(adjugate, residual)
        integrated_numerator = _integrated_polynomial_matrix_inf_norm_upper(
            numerator
        )
        with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
            central_exponent += integrated_numerator / determinant_lower
            tail_exponent += remainder_factor * tail_matrix
            taylor_exponent += remainder_factor * taylor_matrix
            orbit_exponent += remainder_factor * variations["orbit_matrix"]
            period_exponent += remainder_factor * variations["period_matrix"]

        minus = _polynomial_matrix_evaluate(fundamental, -1)
        plus = _polynomial_matrix_evaluate(fundamental, 1)
        old = identity if previous_plus is None else previous_plus
        jump = _relative_jump(minus, old, determinant_lower)
        maximum_jump = max(maximum_jump, jump)
        with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
            jump_exponent += gmpy2.log1p(jump)
        previous_plus = plus

    if minimum_determinant is None:
        raise AssertionError("the Stage-3E cell cover is empty")
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
        total_exponent = (
            central_exponent
            + tail_exponent
            + taylor_exponent
            + orbit_exponent
            + period_exponent
            + jump_exponent
        )
        f_error = gmpy2.expm1(total_exponent)
    if f_error >= 1:
        raise ArithmeticError("the Stage-3E multiplicative F error reached one")
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
        g_error = f_error / (1 - f_error)
    return FundamentalResidualCertificate(
        phase_cell_count=PHASE_CELL_COUNT,
        fundamental_polynomial_degree=FUNDAMENTAL_DEGREE,
        coefficient_taylor_degree=COEFFICIENT_TAYLOR_DEGREE,
        retained_fourier_cutoff=FOURIER_CUTOFF,
        retained_fourier_mode_count=retained,
        omitted_fourier_wiener_tail_upper=decimal_upper(tail, 60),
        coefficient_taylor_remainder_upper=decimal_upper(taylor_remainder, 60),
        exact_orbit_coefficient_variation_upper=decimal_upper(
            variations["orbit_current"], 60
        ),
        exact_period_matrix_variation_upper=decimal_upper(
            variations["period_matrix"], 60
        ),
        minimum_polynomial_determinant_abs_lower=decimal_lower(
            minimum_determinant, 60
        ),
        maximum_Fhat_inf_norm_upper=decimal_upper(maximum_f, 60),
        maximum_Ghat_inf_norm_upper=decimal_upper(maximum_g, 60),
        maximum_polynomial_condition_upper=decimal_upper(maximum_condition, 60),
        central_polynomial_residual_exponent_upper=decimal_upper(
            central_exponent, 60
        ),
        omitted_fourier_tail_exponent_upper=decimal_upper(tail_exponent, 60),
        coefficient_taylor_remainder_exponent_upper=decimal_upper(
            taylor_exponent, 60
        ),
        exact_orbit_ball_exponent_upper=decimal_upper(orbit_exponent, 60),
        exact_period_ball_exponent_upper=decimal_upper(period_exponent, 60),
        interface_jump_log_exponent_upper=decimal_upper(jump_exponent, 60),
        maximum_interface_relative_jump_upper=decimal_upper(maximum_jump, 60),
        total_multiplicative_exponent_upper=decimal_upper(total_exponent, 60),
        F_right_relative_error_upper=decimal_upper(f_error, 60),
        G_left_relative_error_upper=decimal_upper(g_error, 60),
        determinant_nonvanishing_on_every_cell=True,
        chart_interfaces_included=True,
        source_replayed_binary_guide_is_nonclaim_center=True,
    )


def _triangular_propagation(
    base: Any, fundamental: FundamentalResidualCertificate
) -> dict[str, Any]:
    fhat = DirectedInterval.from_decimal(
        fundamental.maximum_Fhat_inf_norm_upper, PRECISION_BITS
    ).upper
    ghat = DirectedInterval.from_decimal(
        fundamental.maximum_Ghat_inf_norm_upper, PRECISION_BITS
    ).upper
    f_error = DirectedInterval.from_decimal(
        fundamental.F_right_relative_error_upper, PRECISION_BITS
    ).upper
    g_error = DirectedInterval.from_decimal(
        fundamental.G_left_relative_error_upper, PRECISION_BITS
    ).upper
    variations = _coefficient_variations(base)
    b_hat = max(_wiener_norm_upper(value) for value in base.delayed_coefficients)
    b_error = variations["orbit_delay"]
    radius = variations["radius"]
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
        period = base.period.upper + radius
        f_exact = fhat * (1 + f_error)
        g_exact = ghat * (1 + g_error)
        b_exact = b_hat + b_error
        c_hat = ghat * b_hat * fhat
        c_exact = g_exact * b_exact * f_exact
        c_error = (
            ghat * g_error * b_exact * f_exact
            + ghat * b_error * f_exact
            + ghat * b_hat * fhat * f_error
        )
        h_hat = period * c_hat
        h_exact = period * c_exact
        h_error = period * c_error
        l_hat = period * c_hat * h_hat
        l_exact = period * c_exact * h_exact
        l_error = period * (c_error * h_exact + c_hat * h_error)
    return {
        "definition": (
            "Chat_j=Ghat Bbar_j Fhat_shift; Hhat_j is its exact-period "
            "phase primitive and Lhat_jk is the corresponding triangular "
            "second primitive"
        ),
        "norm": "matrix infinity norm, uniform in normalized phase and delay id",
        "center_delayed_coefficient_upper": decimal_upper(b_hat, 60),
        "exact_delayed_coefficient_variation_upper": decimal_upper(b_error, 60),
        "exact_F_uniform_upper": decimal_upper(f_exact, 60),
        "exact_G_uniform_upper": decimal_upper(g_exact, 60),
        "Chat_uniform_upper": decimal_upper(c_hat, 60),
        "C_exact_uniform_upper": decimal_upper(c_exact, 60),
        "C_transfer_error_upper": decimal_upper(c_error, 60),
        "Hhat_uniform_upper": decimal_upper(h_hat, 60),
        "H_exact_uniform_upper": decimal_upper(h_exact, 60),
        "H_transfer_error_upper": decimal_upper(h_error, 60),
        "Lhat_uniform_upper": decimal_upper(l_hat, 60),
        "L_exact_uniform_upper": decimal_upper(l_exact, 60),
        "L_transfer_error_upper": decimal_upper(l_error, 60),
        "triangular_majorant_validated": True,
        "binary_stage3d_H_L_guides_transferred": False,
        "signed_word_cancellation_retained": False,
        "usable_as_E_voltage_or_E_recovery": False,
    }


@lru_cache(maxsize=1)
def build_outer_delay_word_stage3e_relative_residual(
    repository: Path,
) -> OuterDelayWordStage3ERelativeResidual:
    repository = repository.resolve()
    if os.environ.get("OPENBLAS_NUM_THREADS") != PINNED_OPENBLAS_NUM_THREADS:
        raise RuntimeError("Stage-3E requires OPENBLAS_NUM_THREADS=1")
    stage3d = _load_parent(
        repository, STAGE3D_RESULT_RELATIVE_PATH, STAGE3D_RESULT_SHA256
    )
    stage3d_claims = _mapping(
        _mapping(stage3d.get("certificate"), "Stage-3D certificate").get(
            "claim_status"
        ),
        "Stage-3D claims",
    )
    if stage3d_claims.get("duffy_two_simplex_collapsed_to_one_dimensional_primitives") is not True:
        raise ValueError("the Stage-3D primitive reduction vanished")
    outer = _load_parent(repository, OUTER_RESULT_RELATIVE_PATH, OUTER_RESULT_SHA256)
    orbit = validate_outer_high_resolution_artifact(
        outer, repository, replay_directed=False
    )
    base = _build_leaky_base_sequences(orbit, PRECISION_BITS)
    guide = _FundamentalGuide(orbit)
    fundamental = _build_fundamental_certificate(base, guide)
    triangular = _triangular_propagation(base, fundamental)
    claims = {name: True for name in TRUE_FLAGS}
    claims.update({name: False for name in FALSE_FLAGS})
    return OuterDelayWordStage3ERelativeResidual(
        schema_id=SCHEMA_ID,
        model_id=MODEL_ID,
        branch=BRANCH,
        arithmetic_scope=ARITHMETIC_SCOPE,
        precision_bits=PRECISION_BITS,
        binary_blas_thread_count=1,
        parent_result_sha256={
            STAGE3D_RESULT_RELATIVE_PATH: STAGE3D_RESULT_SHA256,
            OUTER_RESULT_RELATIVE_PATH: OUTER_RESULT_SHA256,
        },
        relative_residual_identity={
            "factorization": "F_exact=Fhat Y",
            "cell_equation": (
                "d_y Y=-Fhat^{-1}(d_y Fhat-h A_exact Fhat)Y"
            ),
            "same_cell_numerator": (
                "adj(Fhat)(d_y Fhat-h A_exact Fhat)"
            ),
            "flow_factor": "exp(integral ||relative residual|| dy)",
            "interface_factor": (
                "1+||Fhat_plus^{-1}(Fhat_minus-Fhat_plus)||"
            ),
            "F_error": "||Fhat^{-1}F_exact-I|| <= exp(eta)-1",
            "G_error": (
                "||G_exact Fhat-I|| <= (exp(eta)-1)/(2-exp(eta))"
            ),
        },
        fundamental_certificate=fundamental,
        triangular_primitive_propagation=triangular,
        signed_kernel_frontier={
            "first_remaining_object": (
                "a piecewise polynomial H/L guide residual inserted into the "
                "complete signed 21-term density tensor before row total variation"
            ),
            "why_uniform_triangular_bounds_fail": (
                "separate sup norms pay the maximum Fhat/Ghat condition and "
                "destroy cross-word, cross-injection and phase cancellation"
            ),
            "dominant_FG_error_source": "exact 1e-8 orbit ball, not polynomial residual",
            "current_partition_degree": [PHASE_CELL_COUNT, FUNDAMENTAL_DEGREE],
            "next_partition_degree": [PHASE_CELL_COUNT, FUNDAMENTAL_DEGREE],
            "next_precision_bits": 192,
            "required_voltage_error_target": "E_voltage < 0.8730921051856016985675559066",
            "required_recovery_error_target": "E_recovery < 0.9972399927438704453544963998",
            "required_ordering": (
                "sum words, both injection branches and phase subtraction as "
                "one polynomial row; only then integrate absolute value"
            ),
            "more_partitioning_of_F_alone_is_not_the_next_bottleneck": True,
        },
        transfer_errors={
            "E_voltage": None,
            "E_recovery": None,
            "E_phase": _mapping(
                _mapping(stage3d.get("certificate"), "Stage-3D certificate").get(
                    "transfer_errors"
                ),
                "Stage-3D transfer errors",
            )["E_phase"],
        },
        transfer_gate={
            "exact_F_G_transfer_validated": True,
            "binary_H_L_transfer_validated": False,
            "linear_return_gate_evaluated": False,
            "arbitrary_c0_linear_contraction_closes": False,
            "nonlinear_outer_attraction_closes": False,
        },
        claim_status=claims,
        conclusion=(
            "the exact-orbit F/G obstruction is closed by a same-cell relative "
            "residual and a strict multiplicative propagator; a rigorous but "
            "deliberately cancellation-blind triangular H/L majorant is also "
            "given. The binary H/L guides and the complete signed density tensor "
            "are not yet transferred, so E_voltage,E_recovery and C0 contraction "
            "remain open"
        ),
    )


def build_outer_delay_word_stage3e_relative_residual_result(
    repository: Path,
) -> dict[str, Any]:
    repository = repository.resolve()
    certificate = json.loads(
        json.dumps(
            asdict(build_outer_delay_word_stage3e_relative_residual(repository)),
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


def validate_outer_delay_word_stage3e_relative_residual_result(
    payload: Mapping[str, Any], repository: Path
) -> None:
    if not isinstance(payload, Mapping) or set(payload) != {"certificate", "manifest"}:
        raise ValueError("the Stage-3E schema changed")
    certificate = _mapping(payload.get("certificate"), "Stage-3E certificate")
    manifest = _mapping(payload.get("manifest"), "Stage-3E manifest")
    if set(certificate) != {
        field.name for field in fields(OuterDelayWordStage3ERelativeResidual)
    }:
        raise ValueError("the Stage-3E certificate fields changed")
    if manifest.get("schema_id") != SCHEMA_ID or manifest.get("result") != RESULT_RELATIVE_PATH:
        raise ValueError("the Stage-3E manifest changed")
    if canonical_sha256(certificate) != manifest.get("certificate_sha256"):
        raise ValueError("the Stage-3E certificate digest changed")
    sources = _mapping(manifest.get("source_sha256"), "Stage-3E source manifest")
    if set(sources) != set(SOURCE_MANIFEST):
        raise ValueError("the Stage-3E source set changed")
    repository = repository.resolve()
    for relative in SOURCE_MANIFEST:
        if sources.get(relative) != _sha256_path(repository / relative):
            raise ValueError(f"a Stage-3E source changed: {relative}")
    claims = _mapping(certificate.get("claim_status"), "Stage-3E claims")
    if set(claims) != set(TRUE_FLAGS + FALSE_FLAGS):
        raise ValueError("the Stage-3E claim ledger changed")
    if any(claims.get(name) is not True for name in TRUE_FLAGS):
        raise ValueError("a proved Stage-3E fact was weakened")
    if any(claims.get(name) is not False for name in FALSE_FLAGS):
        raise ValueError("an open Stage-3E claim was promoted")
    fundamental = _mapping(
        certificate.get("fundamental_certificate"), "fundamental certificate"
    )
    if fundamental.get("phase_cell_count") != PHASE_CELL_COUNT:
        raise ValueError("the Stage-3E phase partition changed")
    if fundamental.get("fundamental_polynomial_degree") != FUNDAMENTAL_DEGREE:
        raise ValueError("the Stage-3E polynomial degree changed")
    if gmpy2.mpq(str(fundamental["minimum_polynomial_determinant_abs_lower"])) <= 0:
        raise ValueError("the Stage-3E determinant gate vanished")
    f_error = gmpy2.mpq(str(fundamental["F_right_relative_error_upper"]))
    g_error = gmpy2.mpq(str(fundamental["G_left_relative_error_upper"]))
    if not (0 < f_error < 1 and 0 < g_error < 1):
        raise ValueError("the Stage-3E multiplicative errors do not close")
    if fundamental.get("chart_interfaces_included") is not True:
        raise ValueError("the Stage-3E chart jumps vanished")
    triangular = _mapping(
        certificate.get("triangular_primitive_propagation"),
        "triangular primitive propagation",
    )
    if triangular.get("triangular_majorant_validated") is not True:
        raise ValueError("the Stage-3E triangular propagator vanished")
    if triangular.get("usable_as_E_voltage_or_E_recovery") is not False:
        raise ValueError("the cancellation-blind H/L bound was promoted")
    transfer = _mapping(certificate.get("transfer_errors"), "Stage-3E transfer")
    if transfer.get("E_voltage") is not None or transfer.get("E_recovery") is not None:
        raise ValueError("a Stage-3E signed-kernel error was invented")
    gate = _mapping(certificate.get("transfer_gate"), "Stage-3E gate")
    if gate.get("exact_F_G_transfer_validated") is not True:
        raise ValueError("the Stage-3E F/G transfer vanished")
    if gate.get("binary_H_L_transfer_validated") is not False:
        raise ValueError("the Stage-3E binary H/L transfer was invented")
    if gate.get("arbitrary_c0_linear_contraction_closes") is not False:
        raise ValueError("the Stage-3E C0 gate was promoted")
    expected = json.loads(
        json.dumps(
            asdict(build_outer_delay_word_stage3e_relative_residual(repository)),
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        )
    )
    if certificate != expected:
        raise ValueError("the Stage-3E certificate differs from replay")


__all__ = [
    "DEFAULT_COMMAND",
    "FALSE_FLAGS",
    "NOTE_RELATIVE_PATH",
    "RESULT_RELATIVE_PATH",
    "SOURCE_MANIFEST",
    "TRUE_FLAGS",
    "build_outer_delay_word_stage3e_relative_residual",
    "build_outer_delay_word_stage3e_relative_residual_result",
    "canonical_sha256",
    "validate_outer_delay_word_stage3e_relative_residual_result",
]
