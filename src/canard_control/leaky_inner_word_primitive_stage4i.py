"""Stage-4I directed residual ingress for the inner four-word primitives.

The Stage-4H signed calculation reduces the one-period resolvent to
``F, C_0, C_1, C_00``.  This module supplies the first rigorous part of the
missing continuous certificate: cubic Hermite guides on the delay-aligned
physical grid, 192-bit Taylor--Bernstein residuals, and a triangular error
propagation for ``F``, its inverse ``G``, and the three word primitives.

The result does not by itself validate the signed history total variation.
That last step requires a common two-variable enclosure of the *difference*
between the resolvent row and the Stage-4D rank-one row.  All stable-power,
split-tube and graph flags therefore remain false even when the primitive
error budget is much smaller than the Stage-4H numerical margin.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
import math
import os
from pathlib import Path
import platform
from typing import Any, Iterable, Mapping

import gmpy2
import numpy as np

from canard_control.directed_interval import (
    DirectedComplexInterval,
    DirectedInterval,
    decimal_upper,
)
from canard_control.leaky_inner_signed_stable_flow_stage4h import (
    RESULT_RELATIVE_PATH as STAGE4H_RESULT_RELATIVE_PATH,
    _FourWordDiagnostic,
    validate_stage4h_result,
)
from canard_control.leaky_shared_yqq_deflation_stage4e import (
    DELAY_GRID_DIVISOR,
    PRECISION_BITS,
    _complex_point,
    _complex_poly_add,
    _complex_poly_bernstein_upper,
    _complex_poly_derivative,
    _complex_poly_multiply,
    _complex_poly_neg,
    _complex_poly_sub,
    _directed_taylor,
    _directed_taylor_tail_upper,
    _model_uncertainty,
    _point_polynomial,
    _real_point,
    _validation_trim,
)


SCHEMA_ID = "leaky-inner-word-primitive-stage4i-v1"
MODEL_ID = "autonomous-leaky-recovery-two-delay-fhn-bistable-proposal"
BRANCH = "inner_saddle_candidate"
SOURCE_RELATIVE_PATH = "src/canard_control/leaky_inner_word_primitive_stage4i.py"
GENERATOR_RELATIVE_PATH = "experiments/leaky_inner_word_primitive_stage4i.py"
RESULT_RELATIVE_PATH = "experiments/results/leaky_inner_word_primitive_stage4i.json"
NOTE_RELATIVE_PATH = "docs/leaky-inner-word-primitive-stage4i.md"
TEST_RELATIVE_PATH = "tests/test_leaky_inner_word_primitive_stage4i.py"
DEFAULT_COMMAND = (
    "OPENBLAS_NUM_THREADS=8 OMP_NUM_THREADS=1 PYTHONPATH=src "
    "/usr/bin/python3 experiments/leaky_inner_word_primitive_stage4i.py"
)
ARITHMETIC_SCOPE = (
    "exact Stage-4H parent-byte and source binding; cubic Hermite guides on "
    "1042 physical cells aligned with both delays; 192-bit outward MPFR "
    "Taylor--Bernstein residuals for F,G,C0,C1,C00; analytic coefficient "
    "tails and omitted Fourier coefficients added before norms; triangular "
    "cellwise error propagation including every outward intercell guide "
    "jump and validated orbit-coefficient error; explicit infinity/max-entry "
    "norm metadata; "
    "no directed signed two-variable density integral, output-time supremum, "
    "stable power, split tube, graph, separator, or onset theorem"
)
SOURCE_MANIFEST = (SOURCE_RELATIVE_PATH, GENERATOR_RELATIVE_PATH, NOTE_RELATIVE_PATH)
STAGE4H_RESULT_SHA256 = (
    "6577a7fcba9888b5126adcd894a361c9436b29a6f619b04f3d54ce5c3218fc15"
)
PINNED_OPENBLAS_NUM_THREADS = "8"
GUIDE_DEGREE = 3

TRUE_FLAGS = (
    "exact_four_word_system_reused",
    "physical_delay_grid_alignment_validated",
    "primitive_cubic_guides_constructed",
    "primitive_taylor_bernstein_residuals_192bit_validated",
    "primitive_coefficient_tails_added_before_norm",
    "intercell_guide_jumps_outward_added",
    "raw_physical_frame_gronwall_no_go_validated",
    "primitive_error_tubes_propagated",
    "primitive_error_budget_compared_with_stage4h_margin",
)
FALSE_FLAGS = (
    "binary_guide_is_exact_solution",
    "primitive_residual_is_full_signed_density_residual",
    "signed_two_variable_density_integral_validated",
    "continuous_output_phase_supremum_validated",
    "stage4d_rank_one_uncertainty_fully_propagated",
    "phase_fixed_one_step_stable_map_norm_upper_validated",
    "stable_power_constant_numeric_upper_validated",
    "k_s_equals_one_validated",
    "split_return_tube_validated",
    "inner_local_stable_graph_quantitatively_validated",
    "physical_pulse_separator_crossing_validated",
    "unique_physical_pulse_onset_validated",
)


Poly = tuple[DirectedComplexInterval, ...]
PolyMatrix = tuple[tuple[Poly, Poly], tuple[Poly, Poly]]


@dataclass(frozen=True)
class _PrimitiveCell:
    left: float
    right: float
    fundamental: np.ndarray
    inverse: np.ndarray
    word0: np.ndarray
    word1: np.ndarray
    word00: np.ndarray


@dataclass(frozen=True)
class Stage4IArtifact:
    schema_id: str
    model_id: str
    branch: str
    parent_result_sha256: dict[str, str]
    guide_and_grid: dict[str, Any]
    directed_residual_certificate: dict[str, Any]
    directed_primitive_error_tubes: dict[str, Any]
    induced_measure_error_diagnostic: dict[str, Any]
    stable_power_ingress_status: dict[str, Any]
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


def _mapping(value: Any, label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{label} is missing")
    return value


def _format(value: float | np.floating[Any]) -> str:
    return format(float(value), ".17g")


def _hermite(
    left_value: np.ndarray,
    right_value: np.ndarray,
    left_derivative: np.ndarray,
    right_derivative: np.ndarray,
    step: float,
) -> np.ndarray:
    result = np.empty(left_value.shape + (4,), dtype=float)
    result[..., 0] = left_value
    result[..., 1] = step * left_derivative
    result[..., 2] = (
        3.0 * (right_value - left_value)
        - 2.0 * step * left_derivative
        - step * right_derivative
    )
    result[..., 3] = (
        2.0 * (left_value - right_value)
        + step * left_derivative
        + step * right_derivative
    )
    return result


def _guide_cells(diagnostic: _FourWordDiagnostic) -> tuple[_PrimitiveCell, ...]:
    step = diagnostic.tau0 / DELAY_GRID_DIVISOR
    cell_count = int(math.ceil(diagnostic.period / step))
    cells: list[_PrimitiveCell] = []

    def values(time: float) -> tuple[np.ndarray, ...]:
        fundamental = diagnostic.fundamental(time)
        inverse = np.linalg.inv(fundamental)
        return (
            fundamental,
            inverse,
            diagnostic.word_primitive(0, time),
            diagnostic.word_primitive(1, time),
            diagnostic.double_word_primitive(time),
        )

    def derivatives(
        time: float, active0: bool, active1: bool, active00: bool
    ) -> tuple[np.ndarray, ...]:
        fundamental, inverse, _, _, _ = values(time)
        current = diagnostic.current_matrix(time)
        derivative_f = current @ fundamental
        derivative_g = -inverse @ current
        derivative_c0 = np.zeros((2, 2))
        derivative_c1 = np.zeros((2, 2))
        derivative_c00 = np.zeros((2, 2))
        if active0:
            derivative_c0 = np.outer(
                diagnostic.insertion_column(0, time),
                diagnostic.fundamental(time - diagnostic.tau0)[0, :],
            )
        if active1:
            derivative_c1 = np.outer(
                diagnostic.insertion_column(1, time),
                diagnostic.fundamental(time - diagnostic.tau1)[0, :],
            )
        if active00:
            derivative_c00 = np.outer(
                diagnostic.insertion_column(0, time),
                diagnostic.fundamental(time - diagnostic.tau0)[0, :]
                @ diagnostic.word_primitive(
                    0, time - diagnostic.tau0
                ),
            )
        return (
            derivative_f,
            derivative_g,
            derivative_c0,
            derivative_c1,
            derivative_c00,
        )

    for index in range(cell_count):
        left = index * step
        right = min((index + 1) * step, diagnostic.period)
        local_step = right - left
        left_values = values(left)
        right_values = values(right)
        active0 = index >= 512
        active1 = index >= 640
        active00 = index >= 1024
        left_derivatives = derivatives(
            left, active0, active1, active00
        )
        right_derivatives = derivatives(
            right, active0, active1, active00
        )
        polynomials = tuple(
            _hermite(y0, y1, f0, f1, local_step)
            for y0, y1, f0, f1 in zip(
                left_values,
                right_values,
                left_derivatives,
                right_derivatives,
                strict=True,
            )
        )
        cells.append(
            _PrimitiveCell(
                left=left,
                right=right,
                fundamental=polynomials[0],
                inverse=polynomials[1],
                word0=polynomials[2],
                word1=polynomials[3],
                word00=polynomials[4],
            )
        )
    return tuple(cells)


def _poly_scale(value: Poly, scalar: DirectedInterval | float | int) -> Poly:
    return tuple(coefficient * scalar for coefficient in value)


def _poly_sum(values: Iterable[Poly], precision: int = PRECISION_BITS) -> Poly:
    result: Poly = (DirectedComplexInterval.zero(precision),)
    for value in values:
        result = _complex_poly_add(result, value)
    return result


def _matrix_point(value: np.ndarray) -> PolyMatrix:
    return tuple(
        tuple(_point_polynomial(value[row, column]) for column in range(2))
        for row in range(2)
    )  # type: ignore[return-value]


def _matrix_add(left: PolyMatrix, right: PolyMatrix) -> PolyMatrix:
    return tuple(
        tuple(
            _complex_poly_add(left[row][column], right[row][column])
            for column in range(2)
        )
        for row in range(2)
    )  # type: ignore[return-value]


def _matrix_neg(value: PolyMatrix) -> PolyMatrix:
    return tuple(
        tuple(_complex_poly_neg(value[row][column]) for column in range(2))
        for row in range(2)
    )  # type: ignore[return-value]


def _matrix_sub(left: PolyMatrix, right: PolyMatrix) -> PolyMatrix:
    return _matrix_add(left, _matrix_neg(right))


def _matrix_multiply(left: PolyMatrix, right: PolyMatrix) -> PolyMatrix:
    return tuple(
        tuple(
            _poly_sum(
                _complex_poly_multiply(
                    left[row][middle], right[middle][column]
                )
                for middle in range(2)
            )
            for column in range(2)
        )
        for row in range(2)
    )  # type: ignore[return-value]


def _matrix_derivative(
    value: PolyMatrix, step: DirectedInterval
) -> PolyMatrix:
    return tuple(
        tuple(
            _complex_poly_derivative(value[row][column], step)
            for column in range(2)
        )
        for row in range(2)
    )  # type: ignore[return-value]


def _matrix_bernstein_upper(value: PolyMatrix) -> gmpy2.mpfr:
    return max(
        _complex_poly_bernstein_upper(value[row][column])
        for row in range(2)
        for column in range(2)
    )


def _matrix_intercell_jump_bounds(
    previous: PolyMatrix,
    current: PolyMatrix,
    precision: int = PRECISION_BITS,
) -> tuple[gmpy2.mpfr, gmpy2.mpfr]:
    """Return outward max-entry and matrix-infinity seam-jump bounds."""

    entry_bounds: list[list[gmpy2.mpfr]] = [[], []]
    for row in range(2):
        for column in range(2):
            endpoint = DirectedComplexInterval.zero(precision)
            for coefficient in previous[row][column]:
                endpoint = endpoint + coefficient
            jump = endpoint - current[row][column][0]
            entry_bounds[row].append(jump.upper_abs())
    maximum_entry = max(value for row in entry_bounds for value in row)
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        infinity_norm = max(sum(row) for row in entry_bounds)
    return maximum_entry, infinity_norm


def _outer(column: tuple[Poly, Poly], row: tuple[Poly, Poly]) -> PolyMatrix:
    return tuple(
        tuple(
            _complex_poly_multiply(column[i], row[j]) for j in range(2)
        )
        for i in range(2)
    )  # type: ignore[return-value]


def _scaled_delayed_matrix(
    cells: tuple[_PrimitiveCell, ...],
    field: str,
    index: int,
    delay_cells: int,
    local_step: DirectedInterval,
    regular_step: DirectedInterval,
) -> PolyMatrix:
    source = _matrix_point(getattr(cells[index - delay_cells], field))
    if (
        local_step.lower == regular_step.lower
        and local_step.upper == regular_step.upper
    ):
        return source
    ratio = local_step / regular_step

    def scale_polynomial(value: Poly) -> Poly:
        result = []
        power = _real_point(1)
        for coefficient in value:
            result.append(coefficient * power)
            power = power * ratio
        return tuple(result)

    return tuple(
        tuple(scale_polynomial(source[row][column]) for column in range(2))
        for row in range(2)
    )  # type: ignore[return-value]


def _current_matrix_polynomial(
    current: Poly, epsilon: float
) -> PolyMatrix:
    one = _point_polynomial(np.asarray([-1.0]))
    eps = _point_polynomial(np.asarray([epsilon]))
    minus_eps = _point_polynomial(np.asarray([-epsilon]))
    return ((current, one), (eps, minus_eps))


def _word_source(
    inverse: PolyMatrix, delayed_fundamental: PolyMatrix, delayed: Poly
) -> PolyMatrix:
    column = tuple(
        _complex_poly_multiply(inverse[row][0], delayed) for row in range(2)
    )
    row = (delayed_fundamental[0][0], delayed_fundamental[0][1])
    return _outer(column, row)


def _double_word_source(
    inverse: PolyMatrix,
    delayed_fundamental: PolyMatrix,
    delayed_word0: PolyMatrix,
    delayed: Poly,
) -> PolyMatrix:
    column = tuple(
        _complex_poly_multiply(inverse[row][0], delayed) for row in range(2)
    )
    row = tuple(
        _poly_sum(
            _complex_poly_multiply(
                delayed_fundamental[0][middle],
                delayed_word0[middle][column_index],
            )
            for middle in range(2)
        )
        for column_index in range(2)
    )
    return _outer(column, row)  # type: ignore[arg-type]


def _directed_residual_and_tube(
    diagnostic: _FourWordDiagnostic,
    cells: tuple[_PrimitiveCell, ...],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    precision = PRECISION_BITS
    period = DirectedInterval.from_float(diagnostic.period, precision)
    regular_step = (
        DirectedInterval.from_float(diagnostic.tau0, precision)
        / DELAY_GRID_DIVISOR
    )
    root = DirectedInterval.from_float(float(diagnostic.data.root), precision)
    current_dictionary, current_omitted = _validation_trim(
        diagnostic.data.current, float(diagnostic.data.root), precision
    )
    delayed0_dictionary, delayed0_omitted = _validation_trim(
        diagnostic.data.delayed0, float(diagnostic.data.root), precision
    )
    delayed1_dictionary, delayed1_omitted = _validation_trim(
        diagnostic.data.delayed1, float(diagnostic.data.root), precision
    )
    uncertainty = _model_uncertainty(diagnostic.data)
    current_error = gmpy2.mpfr(
        uncertainty["current_coefficient_error"], precision
    )
    delayed_error = gmpy2.mpfr(
        uncertainty["delayed_coefficient_each_error"], precision
    )

    maximum_residual = {name: gmpy2.mpfr(0, precision) for name in ("F", "G", "C0", "C1", "C00")}
    residual_argmax = {name: 0 for name in maximum_residual}
    maximum_guide = {name: gmpy2.mpfr(0, precision) for name in ("F", "G", "C0", "C1", "C00")}
    maximum_tail = {name: gmpy2.mpfr(0, precision) for name in ("current", "delayed0", "delayed1")}
    maximum_coefficient = {
        name: gmpy2.mpfr(0, precision)
        for name in ("current", "delayed0", "delayed1")
    }
    maximum_inverse_defect = gmpy2.mpfr(0, precision)
    cumulative_moving_rate = gmpy2.mpfr(0, precision)
    cumulative_intercell_jump_log = gmpy2.mpfr(0, precision)
    error_cells = {name: [] for name in ("F", "G", "C0", "C1", "C00")}
    endpoint_error = {name: gmpy2.mpfr(0, precision) for name in error_cells}
    max_error = {name: gmpy2.mpfr(0, precision) for name in error_cells}
    raw_endpoint_error = {
        name: gmpy2.mpfr(0, precision) for name in ("F", "G")
    }
    raw_max_error = {
        name: gmpy2.mpfr(0, precision) for name in ("F", "G")
    }
    maximum_jump_entry = {
        name: gmpy2.mpfr(0, precision)
        for name in ("F", "G", "C0", "C1", "C00")
    }
    maximum_jump_infinity = {
        name: gmpy2.mpfr(0, precision)
        for name in ("F", "G", "C0", "C1", "C00")
    }
    previous_guides: dict[str, PolyMatrix] | None = None

    for index, cell in enumerate(cells):
        left = regular_step * index
        step = regular_step if index < len(cells) - 1 else period - left
        current = _directed_taylor(
            current_dictionary, left, step, period, root
        )
        delayed0 = _directed_taylor(
            delayed0_dictionary, left, step, period, root
        )
        delayed1 = _directed_taylor(
            delayed1_dictionary, left, step, period, root
        )
        current_tail = (
            _directed_taylor_tail_upper(
                current_dictionary, step, period, root
            )
            + current_omitted
        )
        delayed0_tail = (
            _directed_taylor_tail_upper(
                delayed0_dictionary, step, period, root
            )
            + delayed0_omitted
        )
        delayed1_tail = (
            _directed_taylor_tail_upper(
                delayed1_dictionary, step, period, root
            )
            + delayed1_omitted
        )
        maximum_tail["current"] = max(maximum_tail["current"], current_tail)
        maximum_tail["delayed0"] = max(maximum_tail["delayed0"], delayed0_tail)
        maximum_tail["delayed1"] = max(maximum_tail["delayed1"], delayed1_tail)

        f = _matrix_point(cell.fundamental)
        g = _matrix_point(cell.inverse)
        c0 = _matrix_point(cell.word0)
        c1 = _matrix_point(cell.word1)
        c00 = _matrix_point(cell.word00)
        guides = {"F": f, "G": g, "C0": c0, "C1": c1, "C00": c00}
        jump_entry = {
            name: gmpy2.mpfr(0, precision) for name in guides
        }
        jump_infinity = {
            name: gmpy2.mpfr(0, precision) for name in guides
        }
        if previous_guides is not None:
            for name, value in guides.items():
                entry_jump, infinity_jump = _matrix_intercell_jump_bounds(
                    previous_guides[name], value, precision
                )
                jump_entry[name] = entry_jump
                jump_infinity[name] = infinity_jump
                maximum_jump_entry[name] = max(
                    maximum_jump_entry[name], entry_jump
                )
                maximum_jump_infinity[name] = max(
                    maximum_jump_infinity[name], infinity_jump
                )
        guide_bounds = {
            name: _matrix_bernstein_upper(value)
            for name, value in guides.items()
        }
        for name, value in guide_bounds.items():
            maximum_guide[name] = max(maximum_guide[name], value)

        identity_poly = _matrix_point(np.eye(2)[..., None])
        inverse_defect = _matrix_sub(
            _matrix_multiply(g, f), identity_poly
        )
        inverse_defect_inf = 2 * _matrix_bernstein_upper(inverse_defect)
        maximum_inverse_defect = max(
            maximum_inverse_defect, inverse_defect_inf
        )
        if inverse_defect_inf >= 1:
            raise ArithmeticError("the primitive guide lost invertibility")

        a_matrix = _current_matrix_polynomial(current, diagnostic.epsilon)
        residual_f = _matrix_sub(
            _matrix_derivative(f, step), _matrix_multiply(a_matrix, f)
        )
        residual_g = _matrix_add(
            _matrix_derivative(g, step), _matrix_multiply(g, a_matrix)
        )
        polynomial_residuals = {
            "F": _matrix_bernstein_upper(residual_f),
            "G": _matrix_bernstein_upper(residual_g),
            "C0": gmpy2.mpfr(0, precision),
            "C1": gmpy2.mpfr(0, precision),
            "C00": gmpy2.mpfr(0, precision),
        }
        analytic_tails = {
            "F": current_tail * guide_bounds["F"],
            "G": current_tail * guide_bounds["G"],
            "C0": gmpy2.mpfr(0, precision),
            "C1": gmpy2.mpfr(0, precision),
            "C00": gmpy2.mpfr(0, precision),
        }

        delayed_f0 = delayed_g0 = None
        if index >= 512:
            delayed_f0 = _scaled_delayed_matrix(
                cells, "fundamental", index, 512, step, regular_step
            )
            source0 = _word_source(g, delayed_f0, delayed0)
            polynomial_residuals["C0"] = _matrix_bernstein_upper(
                _matrix_sub(_matrix_derivative(c0, step), source0)
            )
            analytic_tails["C0"] = (
                delayed0_tail
                * guide_bounds["G"]
                * _matrix_bernstein_upper(delayed_f0)
            )
        else:
            polynomial_residuals["C0"] = _matrix_bernstein_upper(
                _matrix_derivative(c0, step)
            )
        if index >= 640:
            delayed_f1 = _scaled_delayed_matrix(
                cells, "fundamental", index, 640, step, regular_step
            )
            source1 = _word_source(g, delayed_f1, delayed1)
            polynomial_residuals["C1"] = _matrix_bernstein_upper(
                _matrix_sub(_matrix_derivative(c1, step), source1)
            )
            analytic_tails["C1"] = (
                delayed1_tail
                * guide_bounds["G"]
                * _matrix_bernstein_upper(delayed_f1)
            )
        else:
            polynomial_residuals["C1"] = _matrix_bernstein_upper(
                _matrix_derivative(c1, step)
            )
        if index >= 1024:
            if delayed_f0 is None:
                raise ArithmeticError("the double word lost its F delay")
            delayed_c0 = _scaled_delayed_matrix(
                cells, "word0", index, 512, step, regular_step
            )
            source00 = _double_word_source(
                g, delayed_f0, delayed_c0, delayed0
            )
            polynomial_residuals["C00"] = _matrix_bernstein_upper(
                _matrix_sub(_matrix_derivative(c00, step), source00)
            )
            analytic_tails["C00"] = (
                2
                * delayed0_tail
                * guide_bounds["G"]
                * _matrix_bernstein_upper(delayed_f0)
                * _matrix_bernstein_upper(delayed_c0)
            )
        else:
            polynomial_residuals["C00"] = _matrix_bernstein_upper(
                _matrix_derivative(c00, step)
            )

        residuals = {
            name: polynomial_residuals[name] + analytic_tails[name]
            for name in polynomial_residuals
        }
        for name, value in residuals.items():
            if value > maximum_residual[name]:
                maximum_residual[name] = value
                residual_argmax[name] = index

        current_bound = (
            _complex_poly_bernstein_upper(current) + current_tail
        )
        delayed_bounds = (
            _complex_poly_bernstein_upper(delayed0) + delayed0_tail,
            _complex_poly_bernstein_upper(delayed1) + delayed1_tail,
        )
        maximum_coefficient["current"] = max(
            maximum_coefficient["current"], current_bound
        )
        maximum_coefficient["delayed0"] = max(
            maximum_coefficient["delayed0"], delayed_bounds[0]
        )
        maximum_coefficient["delayed1"] = max(
            maximum_coefficient["delayed1"], delayed_bounds[1]
        )
        with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
            h = step.upper
            raw_linear_rate = (
                current_bound + 1 + 2 * diagnostic.epsilon + current_error
            )
            raw_exponential = gmpy2.exp(raw_linear_rate * h)
            for name in ("F", "G"):
                raw_source = (
                    residuals[name] + current_error * guide_bounds[name]
                )
                raw_cell_error = raw_exponential * (
                    raw_endpoint_error[name]
                    + jump_entry[name]
                    + h * raw_source
                )
                raw_endpoint_error[name] = raw_cell_error
                raw_max_error[name] = max(
                    raw_max_error[name], raw_cell_error
                )
            guide_f_inf = 2 * guide_bounds["F"]
            guide_g_inf = 2 * guide_bounds["G"]
            guide_inverse_inf = guide_g_inf / (1 - inverse_defect_inf)
            exact_residual_inf = (
                2 * residuals["F"] + current_error * guide_f_inf
            )
            cumulative_moving_rate += h * guide_inverse_inf * exact_residual_inf
            cumulative_intercell_jump_log += gmpy2.log1p(
                guide_inverse_inf * jump_infinity["F"]
            )
            cumulative_moving_budget = (
                cumulative_moving_rate + cumulative_intercell_jump_log
            )
            relative_error = gmpy2.exp(cumulative_moving_budget) - 1
            if relative_error >= 1:
                raise ArithmeticError(
                    "the primitive moving-frame relative error reached one"
                )
            f_error = guide_f_inf * relative_error
            inverse_relative_error = relative_error / (1 - relative_error)
            g_error = guide_inverse_inf * (
                inverse_defect_inf + inverse_relative_error
            )
            endpoint_error["F"] = f_error
            endpoint_error["G"] = g_error
            error_cells["F"].append(f_error)
            error_cells["G"].append(g_error)
            max_error["F"] = max(max_error["F"], f_error)
            max_error["G"] = max(max_error["G"], g_error)

            for name, delay_index, delay_cells in (
                ("C0", 0, 512),
                ("C1", 1, 640),
            ):
                source_error = residuals[name]
                if index >= delay_cells:
                    delayed_f_bound = _matrix_bernstein_upper(
                        delayed_f0
                        if delay_index == 0
                        else delayed_f1
                    )
                    delayed_f_error = error_cells["F"][index - delay_cells]
                    exact_g = guide_bounds["G"] + error_cells["G"][index]
                    exact_f = delayed_f_bound + delayed_f_error
                    product_difference = (
                        exact_g * exact_f
                        - guide_bounds["G"] * delayed_f_bound
                    )
                    source_error += (
                        delayed_bounds[delay_index] * product_difference
                        + delayed_error * exact_g * exact_f
                    )
                cell_error = (
                    endpoint_error[name]
                    + jump_entry[name]
                    + h * source_error
                )
                endpoint_error[name] = cell_error
                error_cells[name].append(cell_error)
                max_error[name] = max(max_error[name], cell_error)

            source_error = residuals["C00"]
            if index >= 1024:
                delayed_f_bound = _matrix_bernstein_upper(delayed_f0)
                delayed_c_bound = _matrix_bernstein_upper(delayed_c0)
                delayed_f_error = error_cells["F"][index - 512]
                delayed_c_error = error_cells["C0"][index - 512]
                exact_g = guide_bounds["G"] + error_cells["G"][index]
                exact_f = delayed_f_bound + delayed_f_error
                exact_c = delayed_c_bound + delayed_c_error
                product_difference = 2 * (
                    exact_g * exact_f * exact_c
                    - guide_bounds["G"]
                    * delayed_f_bound
                    * delayed_c_bound
                )
                source_error += (
                    delayed_bounds[0] * product_difference
                    + 2
                    * delayed_error
                    * exact_g
                    * exact_f
                    * exact_c
                )
            cell_error = (
                endpoint_error["C00"]
                + jump_entry["C00"]
                + h * source_error
            )
            endpoint_error["C00"] = cell_error
            error_cells["C00"].append(cell_error)
            max_error["C00"] = max(max_error["C00"], cell_error)
        previous_guides = guides

    residual_certificate = {
        "precision_bits": PRECISION_BITS,
        "cell_count": len(cells),
        "guide_degree": GUIDE_DEGREE,
        "coefficient_taylor_degree": 24,
        "maximum_residual_upper": {
            name: decimal_upper(value) for name, value in maximum_residual.items()
        },
        "maximum_residual_cell_index": residual_argmax,
        "maximum_coefficient_tail_upper": {
            name: decimal_upper(value) for name, value in maximum_tail.items()
        },
        "maximum_coefficient_modulus_upper": {
            name: decimal_upper(value)
            for name, value in maximum_coefficient.items()
        },
        "maximum_guide_inverse_defect_infinity_upper": decimal_upper(
            maximum_inverse_defect
        ),
        "cumulative_moving_frame_rate_upper": decimal_upper(
            cumulative_moving_rate
        ),
        "cumulative_intercell_jump_log_upper": decimal_upper(
            cumulative_intercell_jump_log
        ),
        "cumulative_moving_frame_log_budget_upper": decimal_upper(
            cumulative_moving_rate + cumulative_intercell_jump_log
        ),
        "maximum_intercell_guide_jump_max_entry_upper": {
            name: decimal_upper(value)
            for name, value in maximum_jump_entry.items()
        },
        "maximum_intercell_guide_jump_infinity_upper": {
            name: decimal_upper(value)
            for name, value in maximum_jump_infinity.items()
        },
        "intercell_guide_jumps_added": True,
        "analytic_tails_and_trimmed_coefficients_added": True,
        "binary_mesh_spread_used_as_error": False,
    }
    tube_certificate = {
        "maximum_guide_entry_upper": {
            name: decimal_upper(value) for name, value in maximum_guide.items()
        },
        "maximum_error_radius_upper": {
            name: decimal_upper(value) for name, value in max_error.items()
        },
        "final_error_radius_upper": {
            name: decimal_upper(value) for name, value in endpoint_error.items()
        },
        "current_coefficient_model_error_upper": decimal_upper(current_error),
        "delayed_coefficient_each_model_error_upper": decimal_upper(delayed_error),
        "triangular_dependency_order": ["F", "G", "C0", "C1", "C00"],
        "error_radius_norm_by_field": {
            "F": "matrix_infinity_norm",
            "G": "matrix_infinity_norm",
            "C0": "maximum_entry_modulus",
            "C1": "maximum_entry_modulus",
            "C00": "maximum_entry_modulus",
        },
        "fundamental_error_method": (
            "moving frame through the directed guide inverse defect; no raw "
            "physical-coordinate Gronwall exponential"
        ),
        "raw_physical_frame_gronwall_no_go": {
            "maximum_error_radius_upper": {
                name: decimal_upper(value)
                for name, value in raw_max_error.items()
            },
            "final_error_radius_upper": {
                name: decimal_upper(value)
                for name, value in raw_endpoint_error.items()
            },
            "usable_for_signed_stable_certificate": False,
            "mechanism": (
                "the scalar physical-frame majorant retains the unstable "
                "growth that the final rank-one deflation must cancel"
            ),
        },
        "primitive_error_tubes_propagated": True,
    }

    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        mf = maximum_guide["F"]
        mg = maximum_guide["G"]
        mc0 = maximum_guide["C0"]
        mc1 = maximum_guide["C1"]
        mj = maximum_guide["C00"]
        ef = max_error["F"]
        eg = max_error["G"]
        ec0 = max_error["C0"]
        ec1 = max_error["C1"]
        ej = max_error["C00"]
        # F/G radii are matrix infinity norms; C radii are maximum-entry
        # bounds.  These formulas keep those norm conventions explicit and
        # exploit that only one atom column and one history-input column act.
        atom_error = ef * (1 + mc0 + mc1 + mj) + (2 * mf + ef) * (
            ec0 + ec1 + ej
        )
        b0 = maximum_coefficient["delayed0"]
        b1 = maximum_coefficient["delayed1"]
        fg_difference = ef * (mg + eg) + 2 * mf * eg
        exact_fg = (2 * mf + ef) * (mg + eg)
        one_delay_error = (
            diagnostic.tau0
            * (b0 * fg_difference + delayed_error * exact_fg)
            + diagnostic.tau1
            * (b1 * fg_difference + delayed_error * exact_fg)
        )
        fcg_difference = (
            ef * 2 * (mc0 + ec0) * (mg + eg)
            + 2 * mf * 2 * ec0 * (mg + eg)
            + 2 * mf * 2 * mc0 * eg
        )
        exact_fcg = (2 * mf + ef) * 2 * (mc0 + ec0) * (mg + eg)
        # At t=T the active (0,0) history support is theta in [-tau0,0].
        # The inner factors two are the matrix-dimension conversions; the
        # outer factor two bounds the two C0 values in their difference.
        double_delay_error = diagnostic.tau0 * 2 * (
            b0 * fcg_difference + delayed_error * exact_fcg
        )
        event_factor = 1 + (
            uncertainty["xdot_bound"] / uncertainty["event_speed_lower"]
        )
        induced_error = event_factor * (
            atom_error + one_delay_error + double_delay_error
        )
    measure_diagnostic = {
        "atom_error_upper": decimal_upper(atom_error),
        "one_delay_density_tv_error_upper": decimal_upper(one_delay_error),
        "double_delay_density_tv_error_upper": decimal_upper(double_delay_error),
        "event_projection_factor_upper": _format(event_factor),
        "coarse_primitive_induced_event_measure_error_upper": decimal_upper(induced_error),
        "coefficient_cap_used_for_diagnostic": (
            "directed global Bernstein-plus-tail maxima of |b_0| and |b_1|"
        ),
        "primitive_error_norm_convention": (
            "F and G errors use the matrix infinity norm; C0, C1 and C00 "
            "errors use maximum-entry modulus; every downstream dimension "
            "factor is explicit"
        ),
        "double_delay_history_support_length_upper": _format(
            diagnostic.tau0
        ),
        "status": (
            "directed consequence of the primitive tubes, but deliberately "
            "coarse and not a signed stable-row certificate"
        ),
    }
    return residual_certificate, tube_certificate, measure_diagnostic


def build_stage4i_artifact(repository: Path) -> Stage4IArtifact:
    if os.environ.get("OPENBLAS_NUM_THREADS") != PINNED_OPENBLAS_NUM_THREADS:
        raise RuntimeError(
            "the Stage-4I replay requires OPENBLAS_NUM_THREADS="
            + PINNED_OPENBLAS_NUM_THREADS
        )
    repository = repository.resolve()
    parent_path = repository / STAGE4H_RESULT_RELATIVE_PATH
    if STAGE4H_RESULT_SHA256.startswith("TO_FILL"):
        raise RuntimeError("freeze Stage 4H and fill its parent hash first")
    if _sha256_path(parent_path) != STAGE4H_RESULT_SHA256:
        raise ValueError("the bound Stage-4H result changed")
    parent = json.loads(parent_path.read_text(encoding="utf-8"))
    validate_stage4h_result(parent, repository)
    diagnostic = _FourWordDiagnostic(repository)
    cells = _guide_cells(diagnostic)
    residual, tubes, induced = _directed_residual_and_tube(
        diagnostic, cells
    )
    stage4h = _mapping(parent.get("artifact"), "Stage-4H artifact")
    one_step = _mapping(
        stage4h.get("phase_fixed_one_step_diagnostic"),
        "Stage-4H one-step diagnostic",
    )
    sampled_center = float(
        one_step["sampled_phase_fixed_one_step_stable_map_norm_binary64"]
    )
    declared_rate = float(one_step["declared_strong_rate_rho_s"])
    primitive_error = float(
        induced["coarse_primitive_induced_event_measure_error_upper"]
    )
    primitive_budget_below_margin = (
        sampled_center + primitive_error < declared_rate
    )
    claims = {name: True for name in TRUE_FLAGS}
    claims.update({name: False for name in FALSE_FLAGS})
    return Stage4IArtifact(
        schema_id=SCHEMA_ID,
        model_id=MODEL_ID,
        branch=BRANCH,
        parent_result_sha256={
            STAGE4H_RESULT_RELATIVE_PATH: STAGE4H_RESULT_SHA256
        },
        guide_and_grid={
            "period": _format(diagnostic.period),
            "regular_step": _format(diagnostic.tau0 / DELAY_GRID_DIVISOR),
            "tau0_aligned_cell_count": 512,
            "tau1_aligned_cell_count": 640,
            "full_cells_plus_final_short_cell": len(cells),
            "primitive_fields": ["F", "G", "C0", "C1", "C00"],
            "guide_construction": (
                "binary DOP853 centres enter only as cubic Hermite guide "
                "coefficients; validity comes from the directed residual"
            ),
        },
        directed_residual_certificate=residual,
        directed_primitive_error_tubes=tubes,
        induced_measure_error_diagnostic=induced,
        stable_power_ingress_status={
            "stage4h_sampled_signed_center": _format(sampled_center),
            "declared_rate_rho_s": _format(declared_rate),
            "coarse_primitive_error_plus_sampled_center": _format(
                sampled_center + primitive_error
            ),
            "primitive_budget_below_stage4h_numerical_margin": (
                primitive_budget_below_margin
            ),
            "primitive_budget_is_sufficient_for_full_stable_power_proof": False,
            "reason_full_proof_remains_open": (
                "the Stage-4H centre is a sampled Gauss total variation and "
                "not an outward two-variable signed-density integral or "
                "continuous output-phase supremum; the Stage-4D rank-one "
                "uncertainties have not yet been inserted into that common row"
            ),
            "next_exact_object": (
                "Taylor--Bernstein cells for the common signed density "
                "S(t,theta), followed by outward absolute integration and a "
                "continuous t supremum"
            ),
            "phase_fixed_one_step_stable_map_norm_upper": None,
            "stable_power_constant_upper": None,
            "k_s_equals_one_validated": False,
        },
        claim_status=claims,
    )


def build_stage4i_result(repository: Path) -> dict[str, Any]:
    repository = repository.resolve()
    artifact = asdict(build_stage4i_artifact(repository))
    parents = {STAGE4H_RESULT_RELATIVE_PATH: STAGE4H_RESULT_SHA256}
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
            "parent_result_sha256": parents,
            "environment": {
                "python": platform.python_version(),
                "platform": platform.platform(),
                "numpy": np.__version__,
                "gmpy2": gmpy2.__version__,
                "mpfr": gmpy2.mpfr_version(),
                "openblas_num_threads": os.environ.get("OPENBLAS_NUM_THREADS"),
                "omp_num_threads": os.environ.get("OMP_NUM_THREADS"),
            },
        },
    }


def validate_stage4i_result(payload: Mapping[str, Any], repository: Path) -> None:
    repository = repository.resolve()
    primitive_names = {"F", "G", "C0", "C1", "C00"}

    def nonnegative_rationals(
        value: object, names: set[str], label: str
    ) -> dict[str, gmpy2.mpq]:
        mapping = _mapping(value, label)
        if set(mapping) != names:
            raise ValueError(f"the {label} key set changed")
        try:
            parsed = {name: gmpy2.mpq(mapping[name]) for name in names}
        except (TypeError, ValueError) as error:
            raise ValueError(f"the {label} values changed") from error
        if any(item < 0 for item in parsed.values()):
            raise ValueError(f"the {label} gained a negative radius")
        return parsed

    def nonnegative_rational(value: object, label: str) -> gmpy2.mpq:
        try:
            parsed = gmpy2.mpq(value)
        except (TypeError, ValueError) as error:
            raise ValueError(f"the {label} changed") from error
        if parsed < 0:
            raise ValueError(f"the {label} became negative")
        return parsed

    artifact = _mapping(payload.get("artifact"), "Stage-4I artifact")
    manifest = _mapping(payload.get("manifest"), "Stage-4I manifest")
    if set(artifact) != set(Stage4IArtifact.__dataclass_fields__):
        raise ValueError("the Stage-4I artifact schema changed")
    if (
        artifact.get("schema_id") != SCHEMA_ID
        or artifact.get("model_id") != MODEL_ID
        or artifact.get("branch") != BRANCH
    ):
        raise ValueError("the Stage-4I identity changed")
    residual = _mapping(
        artifact.get("directed_residual_certificate"),
        "Stage-4I residual",
    )
    expected_residual_keys = {
        "precision_bits",
        "cell_count",
        "guide_degree",
        "coefficient_taylor_degree",
        "maximum_residual_upper",
        "maximum_residual_cell_index",
        "maximum_coefficient_tail_upper",
        "maximum_coefficient_modulus_upper",
        "maximum_guide_inverse_defect_infinity_upper",
        "cumulative_moving_frame_rate_upper",
        "cumulative_intercell_jump_log_upper",
        "cumulative_moving_frame_log_budget_upper",
        "maximum_intercell_guide_jump_max_entry_upper",
        "maximum_intercell_guide_jump_infinity_upper",
        "intercell_guide_jumps_added",
        "analytic_tails_and_trimmed_coefficients_added",
        "binary_mesh_spread_used_as_error",
    }
    if (
        set(residual) != expected_residual_keys
        or residual.get("precision_bits") != 192
        or residual.get("cell_count") != 1042
        or residual.get("guide_degree") != 3
        or residual.get("coefficient_taylor_degree") != 24
        or residual.get("intercell_guide_jumps_added") is not True
        or residual.get("analytic_tails_and_trimmed_coefficients_added")
        is not True
        or residual.get("binary_mesh_spread_used_as_error") is not False
    ):
        raise ValueError("the Stage-4I directed residual changed")
    residual_maximum = nonnegative_rationals(
        residual.get("maximum_residual_upper"),
        primitive_names,
        "Stage-4I residual maxima",
    )
    if max(residual_maximum.values()) >= gmpy2.mpq("8e-7"):
        raise ValueError("the Stage-4I residual maximum changed")
    coefficient_names = {"current", "delayed0", "delayed1"}
    coefficient_tails = nonnegative_rationals(
        residual.get("maximum_coefficient_tail_upper"),
        coefficient_names,
        "Stage-4I coefficient tails",
    )
    coefficient_moduli = nonnegative_rationals(
        residual.get("maximum_coefficient_modulus_upper"),
        coefficient_names,
        "Stage-4I coefficient moduli",
    )
    if (
        max(coefficient_tails.values()) >= gmpy2.mpq("4e-8")
        or coefficient_moduli["current"] >= 1
        or coefficient_moduli["delayed0"] >= gmpy2.mpq("0.001")
        or coefficient_moduli["delayed1"] >= gmpy2.mpq("0.001")
    ):
        raise ValueError("the Stage-4I coefficient certificate changed")
    residual_indices = _mapping(
        residual.get("maximum_residual_cell_index"),
        "Stage-4I residual indices",
    )
    if set(residual_indices) != primitive_names or any(
        not isinstance(value, int) or not 0 <= value < 1042
        for value in residual_indices.values()
    ):
        raise ValueError("the Stage-4I residual indices changed")
    inverse_defect = nonnegative_rational(
        residual.get("maximum_guide_inverse_defect_infinity_upper"),
        "Stage-4I inverse defect",
    )
    if inverse_defect >= gmpy2.mpq("2e-8"):
        raise ValueError("the Stage-4I inverse defect changed")
    moving_rate = nonnegative_rational(
        residual.get("cumulative_moving_frame_rate_upper"),
        "Stage-4I differential moving-frame rate",
    )
    seam_log = nonnegative_rational(
        residual.get("cumulative_intercell_jump_log_upper"),
        "Stage-4I intercell jump log",
    )
    moving_budget = nonnegative_rational(
        residual.get("cumulative_moving_frame_log_budget_upper"),
        "Stage-4I moving-frame log budget",
    )
    if (
        moving_budget >= gmpy2.mpq("0.001")
        or abs(moving_budget - moving_rate - seam_log)
        > gmpy2.mpq("1e-18")
    ):
        raise ValueError("the Stage-4I moving-frame budget lost a summand")
    jump_entry = nonnegative_rationals(
        residual.get("maximum_intercell_guide_jump_max_entry_upper"),
        primitive_names,
        "Stage-4I max-entry seam jumps",
    )
    jump_infinity = nonnegative_rationals(
        residual.get("maximum_intercell_guide_jump_infinity_upper"),
        primitive_names,
        "Stage-4I infinity seam jumps",
    )
    if (
        max(jump_infinity.values()) >= gmpy2.mpq("1e-12")
        or any(jump_infinity[name] < jump_entry[name] for name in primitive_names)
    ):
        raise ValueError("the Stage-4I seam jumps changed")
    tubes = _mapping(
        artifact.get("directed_primitive_error_tubes"),
        "Stage-4I tubes",
    )
    expected_tube_keys = {
        "maximum_guide_entry_upper",
        "maximum_error_radius_upper",
        "final_error_radius_upper",
        "current_coefficient_model_error_upper",
        "delayed_coefficient_each_model_error_upper",
        "triangular_dependency_order",
        "error_radius_norm_by_field",
        "fundamental_error_method",
        "raw_physical_frame_gronwall_no_go",
        "primitive_error_tubes_propagated",
    }
    if (
        set(tubes) != expected_tube_keys
        or tubes.get("primitive_error_tubes_propagated") is not True
        or tubes.get("triangular_dependency_order")
        != ["F", "G", "C0", "C1", "C00"]
        or tubes.get("error_radius_norm_by_field")
        != {
            "F": "matrix_infinity_norm",
            "G": "matrix_infinity_norm",
            "C0": "maximum_entry_modulus",
            "C1": "maximum_entry_modulus",
            "C00": "maximum_entry_modulus",
        }
    ):
        raise ValueError("the Stage-4I primitive tube changed")
    guide_maximum = nonnegative_rationals(
        tubes.get("maximum_guide_entry_upper"),
        primitive_names,
        "Stage-4I guide maxima",
    )
    current_model_error = nonnegative_rational(
        tubes.get("current_coefficient_model_error_upper"),
        "Stage-4I current coefficient model error",
    )
    delayed_model_error = nonnegative_rational(
        tubes.get("delayed_coefficient_each_model_error_upper"),
        "Stage-4I delayed coefficient model error",
    )
    if (
        guide_maximum["F"] >= 10
        or guide_maximum["G"] >= 10
        or guide_maximum["C0"] >= gmpy2.mpq("0.01")
        or guide_maximum["C1"] >= gmpy2.mpq("0.01")
        or guide_maximum["C00"] >= gmpy2.mpq("1e-7")
        or current_model_error >= gmpy2.mpq("2e-8")
        or delayed_model_error >= gmpy2.mpq("2e-8")
    ):
        raise ValueError("the Stage-4I guide/model bounds changed")
    raw = _mapping(
        tubes.get("raw_physical_frame_gronwall_no_go"),
        "Stage-4I raw-frame no-go",
    )
    if set(raw) != {
        "maximum_error_radius_upper",
        "final_error_radius_upper",
        "usable_for_signed_stable_certificate",
        "mechanism",
    }:
        raise ValueError("the Stage-4I raw-frame schema changed")
    raw_maximum = nonnegative_rationals(
        raw.get("maximum_error_radius_upper"),
        {"F", "G"},
        "Stage-4I raw-frame maximum radii",
    )
    raw_final = nonnegative_rationals(
        raw.get("final_error_radius_upper"),
        {"F", "G"},
        "Stage-4I raw-frame final radii",
    )
    moving_maximum = nonnegative_rationals(
        tubes.get("maximum_error_radius_upper"),
        primitive_names,
        "Stage-4I moving-frame maximum radii",
    )
    moving_final = nonnegative_rationals(
        tubes.get("final_error_radius_upper"),
        primitive_names,
        "Stage-4I moving-frame final radii",
    )
    raw_f = raw_maximum["F"]
    raw_g = raw_maximum["G"]
    if (
        raw.get("usable_for_signed_stable_certificate") is not False
        or raw_f <= 10**6
        or raw_g <= 10**6
        or any(raw_final[name] > raw_maximum[name] for name in ("F", "G"))
    ):
        raise ValueError("the Stage-4I raw-frame no-go changed")
    moving_f = moving_maximum["F"]
    moving_g = moving_maximum["G"]
    moving_c0 = moving_maximum["C0"]
    moving_c1 = moving_maximum["C1"]
    moving_c00 = moving_maximum["C00"]
    if (
        moving_f >= gmpy2.mpq("5e-4")
        or moving_g >= gmpy2.mpq("3e-4")
        or moving_c0 >= gmpy2.mpq("2e-6")
        or moving_c1 >= gmpy2.mpq("2e-6")
        or moving_c00 >= gmpy2.mpq("4e-11")
        or any(
            moving_final[name] > moving_maximum[name]
            for name in primitive_names
        )
    ):
        raise ValueError("the Stage-4I moving-frame tube changed")
    induced = _mapping(
        artifact.get("induced_measure_error_diagnostic"),
        "Stage-4I induced measure diagnostic",
    )
    expected_induced_keys = {
        "atom_error_upper",
        "one_delay_density_tv_error_upper",
        "double_delay_density_tv_error_upper",
        "event_projection_factor_upper",
        "coarse_primitive_induced_event_measure_error_upper",
        "coefficient_cap_used_for_diagnostic",
        "primitive_error_norm_convention",
        "double_delay_history_support_length_upper",
        "status",
    }
    if set(induced) != expected_induced_keys:
        raise ValueError("the Stage-4I induced measure schema changed")
    induced_parts = {
        name: nonnegative_rational(induced.get(name), f"Stage-4I {name}")
        for name in (
            "atom_error_upper",
            "one_delay_density_tv_error_upper",
            "double_delay_density_tv_error_upper",
            "coarse_primitive_induced_event_measure_error_upper",
        )
    }
    event_factor = nonnegative_rational(
        induced.get("event_projection_factor_upper"),
        "Stage-4I event projection factor",
    )
    if (
        induced.get("double_delay_history_support_length_upper")
        != "8.9442719099991592"
        or induced.get("event_projection_factor_upper")
        != "2.0135805680204055"
        or induced_parts[
            "coarse_primitive_induced_event_measure_error_upper"
        ]
        >= gmpy2.mpq("0.002")
    ):
        raise ValueError("the Stage-4I induced measure budget changed")
    component_total = (
        induced_parts["atom_error_upper"]
        + induced_parts["one_delay_density_tv_error_upper"]
        + induced_parts["double_delay_density_tv_error_upper"]
    )
    induced_total = induced_parts[
        "coarse_primitive_induced_event_measure_error_upper"
    ]
    if (
        induced_total < event_factor * component_total
        or induced_total - event_factor * component_total
        > gmpy2.mpq("1e-15")
    ):
        raise ValueError("the Stage-4I induced components lost consistency")
    status = _mapping(
        artifact.get("stable_power_ingress_status"), "Stage-4I status"
    )
    expected_status_keys = {
        "stage4h_sampled_signed_center",
        "declared_rate_rho_s",
        "coarse_primitive_error_plus_sampled_center",
        "primitive_budget_below_stage4h_numerical_margin",
        "primitive_budget_is_sufficient_for_full_stable_power_proof",
        "reason_full_proof_remains_open",
        "next_exact_object",
        "phase_fixed_one_step_stable_map_norm_upper",
        "stable_power_constant_upper",
        "k_s_equals_one_validated",
    }
    try:
        center = float(status.get("stage4h_sampled_signed_center"))
        rate = float(status.get("declared_rate_rho_s"))
        combined = float(
            status.get("coarse_primitive_error_plus_sampled_center")
        )
        induced_error = float(
            induced["coarse_primitive_induced_event_measure_error_upper"]
        )
    except (TypeError, ValueError) as error:
        raise ValueError("the Stage-4I numerical margin changed") from error
    parent_payload = json.loads(
        (repository / STAGE4H_RESULT_RELATIVE_PATH).read_text(encoding="utf-8")
    )
    parent_artifact = _mapping(
        parent_payload.get("artifact"), "Stage-4H parent artifact"
    )
    parent_one_step = _mapping(
        parent_artifact.get("phase_fixed_one_step_diagnostic"),
        "Stage-4H parent one-step diagnostic",
    )
    if (
        set(status) != expected_status_keys
        or not all(
            math.isfinite(value) and value >= 0
            for value in (center, rate, combined, induced_error)
        )
        or status.get("coarse_primitive_error_plus_sampled_center")
        != _format(center + induced_error)
        or status.get("stage4h_sampled_signed_center")
        != parent_one_step.get(
            "sampled_phase_fixed_one_step_stable_map_norm_binary64"
        )
        or status.get("declared_rate_rho_s")
        != parent_one_step.get("declared_strong_rate_rho_s")
        or status.get("primitive_budget_below_stage4h_numerical_margin")
        is not (center + induced_error < rate)
        or status.get("primitive_budget_is_sufficient_for_full_stable_power_proof")
        is not False
        or status.get("phase_fixed_one_step_stable_map_norm_upper") is not None
        or status.get("stable_power_constant_upper") is not None
        or status.get("k_s_equals_one_validated") is not False
    ):
        raise ValueError("the Stage-4I open stable power was promoted")
    claims = _mapping(artifact.get("claim_status"), "Stage-4I claims")
    if set(claims) != set(TRUE_FLAGS) | set(FALSE_FLAGS):
        raise ValueError("the Stage-4I claim ledger changed")
    if any(claims.get(name) is not True for name in TRUE_FLAGS):
        raise ValueError("a proved Stage-4I flag changed")
    if any(claims.get(name) is not False for name in FALSE_FLAGS):
        raise ValueError("an open Stage-4I flag was promoted")

    parents = {STAGE4H_RESULT_RELATIVE_PATH: STAGE4H_RESULT_SHA256}
    expected_manifest = {
        "schema_id",
        "result",
        "default_command",
        "arithmetic_scope",
        "artifact_sha256",
        "source_sha256",
        "parent_result_sha256",
        "environment",
    }
    if set(manifest) != expected_manifest:
        raise ValueError("the Stage-4I manifest schema changed")
    fixed = {
        "schema_id": SCHEMA_ID,
        "result": RESULT_RELATIVE_PATH,
        "default_command": DEFAULT_COMMAND,
        "arithmetic_scope": ARITHMETIC_SCOPE,
        "artifact_sha256": canonical_sha256(artifact),
        "parent_result_sha256": parents,
    }
    if any(manifest.get(name) != value for name, value in fixed.items()):
        raise ValueError("the Stage-4I manifest fixed data changed")
    if artifact.get("parent_result_sha256") != parents:
        raise ValueError("the Stage-4I artifact parents changed")
    sources = _mapping(manifest.get("source_sha256"), "Stage-4I sources")
    if set(sources) != set(SOURCE_MANIFEST):
        raise ValueError("the Stage-4I source set changed")
    for relative in SOURCE_MANIFEST:
        if sources.get(relative) != _sha256_path(repository / relative):
            raise ValueError(f"the Stage-4I source changed: {relative}")
    for relative, digest in parents.items():
        if _sha256_path(repository / relative) != digest:
            raise ValueError(f"the Stage-4I parent changed: {relative}")


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
    "Stage4IArtifact",
    "TRUE_FLAGS",
    "build_stage4i_artifact",
    "build_stage4i_result",
    "canonical_sha256",
    "validate_stage4i_result",
]
