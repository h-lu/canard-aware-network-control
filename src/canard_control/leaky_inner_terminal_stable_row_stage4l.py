"""Stage-4L direct terminal stable-row certificate.

This module encloses the selected near-one-period phase-fixed linear return
on the Route-C tangent section.  It forms the input stable deflation and the
terminal event correction in one signed atom--density row before taking any
total-variation norm.  The current-voltage atom is removed exactly by the
section quotient.  Stage-4I primitive tubes supply the raw method-of-steps
error, while a cellwise common Taylor--Bernstein calculation supplies the
continuous centre row on the complete returned history.

The result is only a discrete linear ingress.  It neither identifies a first
return nor proves a nonlinear tube, a stable graph, a pulse intersection, a
crossing, or an onset theorem.
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
import sys
from typing import Any, Iterable, Mapping

import gmpy2
import numpy as np

from canard_control.directed_interval import (
    DirectedComplexInterval,
    DirectedInterval,
    decimal_lower,
    decimal_upper,
    upward_division,
    upward_product,
    upward_sum,
)
from canard_control.leaky_inner_signed_stable_flow_stage4h import (
    RESULT_RELATIVE_PATH as STAGE4H_RESULT_RELATIVE_PATH,
    _FourWordDiagnostic,
    validate_stage4h_result,
)
from canard_control.leaky_inner_stable_projection_stage3 import (
    RESULT_RELATIVE_PATH as STAGE3_RESULT_RELATIVE_PATH,
    validate_stage3_stable_projection_result,
)
from canard_control.leaky_inner_word_primitive_stage4i import (
    RESULT_RELATIVE_PATH as STAGE4I_RESULT_RELATIVE_PATH,
    _PrimitiveCell,
    _guide_cells,
    validate_stage4i_result,
)
from canard_control.leaky_route_c_adjoint_stage4d import (
    RESULT_RELATIVE_PATH as STAGE4D_RESULT_RELATIVE_PATH,
    validate_stage4d_result,
)
from canard_control.leaky_shared_yqq_deflation_stage4e import (
    PRECISION_BITS,
    RESULT_RELATIVE_PATH as STAGE4E_RESULT_RELATIVE_PATH,
    _complex_point,
    _dictionary_l1_directed_upper,
    _directed_taylor,
    _directed_taylor_tail_upper,
    _model_uncertainty,
    _validation_trim,
    validate_stage4e_result,
)


SCHEMA_ID = "leaky-inner-terminal-stable-row-stage4l-v1"
MODEL_ID = "autonomous-leaky-recovery-two-delay-fhn-bistable-proposal"
BRANCH = "inner_saddle_candidate"
STATUS = "PROVED_DISCRETE_LINEAR_INGRESS"
SOURCE_RELATIVE_PATH = (
    "src/canard_control/leaky_inner_terminal_stable_row_stage4l.py"
)
GENERATOR_RELATIVE_PATH = (
    "experiments/leaky_inner_terminal_stable_row_stage4l.py"
)
RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_inner_terminal_stable_row_stage4l.json"
)
NOTE_RELATIVE_PATH = "docs/leaky-inner-terminal-stable-row-stage4l.md"
CONTRACT_RELATIVE_PATH = (
    "docs/leaky-inner-terminal-stable-row-stage4l-contract.md"
)
TEST_RELATIVE_PATH = (
    "tests/test_leaky_inner_terminal_stable_row_stage4l.py"
)
DIRECTED_INTERVAL_RELATIVE_PATH = "src/canard_control/directed_interval.py"
DEFAULT_COMMAND = (
    "OPENBLAS_NUM_THREADS=8 OMP_NUM_THREADS=1 PYTHONPATH=src "
    "/usr/bin/python3 experiments/leaky_inner_terminal_stable_row_stage4l.py"
)
ARITHMETIC_SCOPE = (
    "exact parent-byte validation for Stages 3, 4D, 4E, 4H and 4I; "
    "fixed-start four-word method of steps; common input-deflated and "
    "terminal-event-corrected atom-density rows before norms; exact Route-C "
    "section quotient; directed cubic Taylor remainders and continuous "
    "two-variable Bernstein suprema on every returned-history/input-history "
    "cell; Stage-4I primitive-tube and Stage-4D/4E normalization errors; "
    "only the selected discrete linear stable-map bound and K_s=1 are proved"
)
SOURCE_MANIFEST = (
    SOURCE_RELATIVE_PATH,
    GENERATOR_RELATIVE_PATH,
    NOTE_RELATIVE_PATH,
    CONTRACT_RELATIVE_PATH,
    TEST_RELATIVE_PATH,
    DIRECTED_INTERVAL_RELATIVE_PATH,
)

STAGE3_RESULT_SHA256 = (
    "9ea776a6e627745ded7f7023523999bfbd29a0be4878172c76512d623146e2ea"
)
STAGE4D_RESULT_SHA256 = (
    "af51bcfc20000b804134c1d8b9cacc303013676c440a89f2ecb52faf0042d568"
)
STAGE4E_RESULT_SHA256 = (
    "ccdd6023f911e97785ec6f8be97b84d725d6af9f5051e1da602380d225e47acc"
)
STAGE4H_RESULT_SHA256 = (
    "6577a7fcba9888b5126adcd894a361c9436b29a6f619b04f3d54ce5c3218fc15"
)
STAGE4I_RESULT_SHA256 = (
    "1248e9d95444f3cc12565c1e11b4bbeab3d4a9a7bb8922893e38b1ffa439f73e"
)
PARENT_HASHES = {
    STAGE3_RESULT_RELATIVE_PATH: STAGE3_RESULT_SHA256,
    STAGE4D_RESULT_RELATIVE_PATH: STAGE4D_RESULT_SHA256,
    STAGE4E_RESULT_RELATIVE_PATH: STAGE4E_RESULT_SHA256,
    STAGE4H_RESULT_RELATIVE_PATH: STAGE4H_RESULT_SHA256,
    STAGE4I_RESULT_RELATIVE_PATH: STAGE4I_RESULT_SHA256,
}

PINNED_OPENBLAS_NUM_THREADS = "8"
PINNED_OMP_NUM_THREADS = "1"
TARGET_RHO_TERM = "0.1"
LP_RATE_UPPER = "0.1"
FOURIER_CENTRE_DEGREE = 3
T_BERNSTEIN_DEGREE = 6
HISTORY_BERNSTEIN_DEGREE = 9
LOCAL_FLOAT_OPERATION_GUARD = 1.0e-10
CENTER_BINARY_BERNSTEIN_GUARD = "0.00001"
TIME_LIPSCHITZ_CAP = "1000"
BINARY64_UNIT_ROUNDOFF = "1.1102230246251565404236316680908203125e-16"
MAX_GUARDED_REAL_OPERATIONS = 131072
MAX_UNGUARDED_REAL_OPERATIONS = 131072
BINARY_KERNEL_ENVELOPE_CAP = "4096"
ACTIVATION_PADDING_BINARY64 = 1.0e-10

# This mutable audit is active only during one serial centre replay.  It does
# not change arithmetic; it records every BallPoly and bivariate ball array
# actually constructed so that the final envelope is not inferred merely
# from the Fourier inputs.
_ACTIVE_BINARY_AUDIT: dict[str, float | int] | None = None


def _audit_binary_ball(center: np.ndarray, radius: np.ndarray) -> None:
    audit = _ACTIVE_BINARY_AUDIT
    if audit is None or center.size == 0:
        return
    envelope = float(np.max(np.abs(center) + radius))
    audit["actual_envelope"] = max(
        float(audit["actual_envelope"]), envelope
    )
    audit["array_count"] = int(audit["array_count"]) + 1
    audit["scalar_coefficient_count"] = int(
        audit["scalar_coefficient_count"]
    ) + int(center.size)

TRUE_FLAGS = (
    "selected_phase_fixed_linear_return_defined",
    "linear_tangent_section_sigma0_used",
    "exact_eigen_intertwining_identity_registered",
    "exact_four_word_support_validated_on_true_period_interval",
    "complete_true_returned_history_covered",
    "common_double_rank_one_row_formed_before_norm",
    "section_quotient_current_voltage_atom_removed_exactly",
    "continuous_two_variable_bernstein_supremum_validated",
    "outward_voltage_density_total_variation_validated",
    "recovery_output_row_validated_in_same_y_norm",
    "noncircular_stage4i_primitive_error_propagation_validated",
    "phase_fixed_selected_stable_map_norm_at_most_0p1_validated",
    "stable_power_rate_0p1_validated",
    "stable_power_constant_k_s_equals_one_validated",
)
FALSE_FLAGS = (
    "selected_section_map_is_first_positive_return_validated",
    "first_positive_return_and_no_earlier_hit_validated",
    "nonlinear_return_tube_validated",
    "split_return_ball_validated",
    "six_projected_return_hessian_blocks_validated",
    "matrix_lyapunov_perron_graph_certificate_validated",
    "inner_local_stable_graph_quantitatively_validated",
    "full_pulse_interval_stable_seed_containment_validated",
    "selected_pulse_stable_graph_intersection_validated",
    "endpoint_stable_gap_signs_validated",
    "physical_pulse_separator_crossing_validated",
    "unique_physical_pulse_onset_validated",
    "two_sided_routing_validated",
    "network_safety_validated",
)


@dataclass(frozen=True)
class _BallPoly:
    """Complex monomial polynomial with coefficientwise disc radii."""

    center: np.ndarray
    radius: np.ndarray

    def __post_init__(self) -> None:
        if self.center.ndim != 1 or self.radius.ndim != 1:
            raise ValueError("a Stage-4L polynomial is not one-dimensional")
        if self.center.shape != self.radius.shape or len(self.center) == 0:
            raise ValueError("a Stage-4L polynomial shape changed")
        if not np.all(np.isfinite(self.center)):
            raise ValueError("a Stage-4L polynomial centre is not finite")
        if not np.all(np.isfinite(self.radius)) or np.any(self.radius < 0):
            raise ValueError("a Stage-4L polynomial radius is invalid")
        _audit_binary_ball(self.center, self.radius)


@dataclass(frozen=True)
class Stage4LArtifact:
    schema_id: str
    model_id: str
    branch: str
    status: str
    parent_result_sha256: dict[str, str]
    analytic_discrete_lemma: dict[str, Any]
    true_period_and_word_support: dict[str, Any]
    terminal_grid_and_common_row: dict[str, Any]
    directed_common_center: dict[str, Any]
    directed_error_ledger: dict[str, Any]
    stable_power_certificate: dict[str, Any]
    scope_boundary: dict[str, Any]
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


def _upper_float(value: gmpy2.mpfr | float) -> float:
    exact = gmpy2.mpfr(value, PRECISION_BITS)
    converted = float(exact)
    if gmpy2.mpfr(converted, PRECISION_BITS) < exact:
        converted = math.nextafter(converted, math.inf)
    return converted


def _ball_from_complex_interval(value: DirectedComplexInterval) -> tuple[complex, float]:
    real_mid = value.real.midpoint_nearest()
    imag_mid = value.imag.midpoint_nearest()
    center = complex(float(real_mid), float(imag_mid))
    center_real = gmpy2.mpfr(center.real, PRECISION_BITS)
    center_imag = gmpy2.mpfr(center.imag, PRECISION_BITS)
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
        real_radius = max(
            abs(value.real.lower - center_real),
            abs(value.real.upper - center_real),
        )
        imag_radius = max(
            abs(value.imag.lower - center_imag),
            abs(value.imag.upper - center_imag),
        )
        radius = gmpy2.sqrt(real_radius**2 + imag_radius**2)
    return center, _upper_float(radius)


def _point_poly(value: complex | float | int) -> _BallPoly:
    return _BallPoly(
        np.asarray([complex(value)], dtype=complex),
        np.zeros(1, dtype=float),
    )


def _zero_poly() -> _BallPoly:
    return _point_poly(0)


def _pad_poly(value: _BallPoly, size: int) -> _BallPoly:
    if len(value.center) >= size:
        return value
    center = np.zeros(size, dtype=complex)
    radius = np.zeros(size, dtype=float)
    center[: len(value.center)] = value.center
    radius[: len(value.radius)] = value.radius
    return _BallPoly(center, radius)


def _round_radius(magnitude: np.ndarray | float) -> np.ndarray | float:
    return LOCAL_FLOAT_OPERATION_GUARD * (1.0 + magnitude)


def _poly_add(left: _BallPoly, right: _BallPoly) -> _BallPoly:
    size = max(len(left.center), len(right.center))
    lhs = _pad_poly(left, size)
    rhs = _pad_poly(right, size)
    center = lhs.center + rhs.center
    radius = lhs.radius + rhs.radius + _round_radius(
        np.abs(lhs.center) + np.abs(rhs.center)
    )
    return _BallPoly(center, np.nextafter(radius, math.inf))


def _poly_neg(value: _BallPoly) -> _BallPoly:
    return _BallPoly(-value.center, value.radius.copy())


def _poly_sub(left: _BallPoly, right: _BallPoly) -> _BallPoly:
    return _poly_add(left, _poly_neg(right))


def _poly_mul(left: _BallPoly, right: _BallPoly) -> _BallPoly:
    center = np.convolve(left.center, right.center)
    radius = (
        np.convolve(np.abs(left.center), right.radius)
        + np.convolve(left.radius, np.abs(right.center))
        + np.convolve(left.radius, right.radius)
    )
    envelope = np.convolve(
        np.abs(left.center) + left.radius,
        np.abs(right.center) + right.radius,
    )
    radius += _round_radius(envelope)
    return _BallPoly(center, np.nextafter(radius, math.inf))


def _poly_scale(value: _BallPoly, scalar: complex | float) -> _BallPoly:
    return _poly_mul(value, _point_poly(scalar))


def _poly_affine(value: _BallPoly, offset: float, scale: float) -> _BallPoly:
    affine = _BallPoly(
        np.asarray([complex(offset), complex(scale)], dtype=complex),
        np.zeros(2, dtype=float),
    )
    reversed_coefficients = list(
        zip(value.center[::-1], value.radius[::-1], strict=True)
    )
    first_coefficient, first_radius = reversed_coefficients[0]
    result = _BallPoly(
        np.asarray([first_coefficient], dtype=complex),
        np.asarray([first_radius], dtype=float),
    )
    for coefficient, radius in reversed_coefficients[1:]:
        result = _poly_mul(result, affine)
        result = _poly_add(
            result,
            _BallPoly(
                np.asarray([coefficient], dtype=complex),
                np.asarray([radius], dtype=float),
            ),
        )
    return result


def _poly_value(value: _BallPoly, coordinate: float) -> tuple[complex, float]:
    result = _zero_poly()
    point = _point_poly(coordinate)
    for coefficient, radius in zip(
        value.center[::-1], value.radius[::-1], strict=True
    ):
        result = _poly_mul(result, point)
        result = _poly_add(
            result,
            _BallPoly(
                np.asarray([coefficient], dtype=complex),
                np.asarray([radius], dtype=float),
            ),
        )
    return complex(result.center[0]), float(result.radius[0])


@lru_cache(maxsize=None)
def _monomial_to_bernstein_matrix(degree: int) -> np.ndarray:
    result = np.zeros((degree + 1, degree + 1), dtype=float)
    for row in range(degree + 1):
        for column in range(row + 1):
            result[row, column] = (
                math.comb(row, column) / math.comb(degree, column)
            )
    return result


def _bernstein(value: _BallPoly, degree: int) -> _BallPoly:
    if len(value.center) - 1 > degree:
        raise ValueError("a Stage-4L Bernstein target lost polynomial degree")
    padded = _pad_poly(value, degree + 1)
    matrix = _monomial_to_bernstein_matrix(degree)
    center = matrix @ padded.center
    radius = matrix @ padded.radius
    radius += _round_radius(matrix @ (np.abs(padded.center) + padded.radius))
    return _BallPoly(center, np.nextafter(radius, math.inf))


def _univariate_bernstein_upper(value: _BallPoly, degree: int | None = None) -> float:
    target = len(value.center) - 1 if degree is None else degree
    bernstein = _bernstein(value, target)
    upper = float(np.max(np.abs(bernstein.center) + bernstein.radius))
    return math.nextafter(upper, math.inf)


def _matrix_add(
    left: tuple[tuple[_BallPoly, _BallPoly], tuple[_BallPoly, _BallPoly]],
    right: tuple[tuple[_BallPoly, _BallPoly], tuple[_BallPoly, _BallPoly]],
) -> tuple[tuple[_BallPoly, _BallPoly], tuple[_BallPoly, _BallPoly]]:
    return tuple(
        tuple(_poly_add(left[row][column], right[row][column]) for column in range(2))
        for row in range(2)
    )  # type: ignore[return-value]


def _matrix_multiply(
    left: tuple[tuple[_BallPoly, _BallPoly], tuple[_BallPoly, _BallPoly]],
    right: tuple[tuple[_BallPoly, _BallPoly], tuple[_BallPoly, _BallPoly]],
) -> tuple[tuple[_BallPoly, _BallPoly], tuple[_BallPoly, _BallPoly]]:
    return tuple(
        tuple(
            _poly_add(
                _poly_mul(left[row][0], right[0][column]),
                _poly_mul(left[row][1], right[1][column]),
            )
            for column in range(2)
        )
        for row in range(2)
    )  # type: ignore[return-value]


def _matrix_identity() -> tuple[
    tuple[_BallPoly, _BallPoly], tuple[_BallPoly, _BallPoly]
]:
    return (
        (_point_poly(1), _point_poly(0)),
        (_point_poly(0), _point_poly(1)),
    )


def _matrix_point_value(
    value: tuple[tuple[_BallPoly, _BallPoly], tuple[_BallPoly, _BallPoly]],
    coordinate: float,
) -> tuple[tuple[_BallPoly, _BallPoly], tuple[_BallPoly, _BallPoly]]:
    return tuple(
        tuple(
            _BallPoly(
                np.asarray([_poly_value(value[row][column], coordinate)[0]]),
                np.asarray([_poly_value(value[row][column], coordinate)[1]]),
            )
            for column in range(2)
        )
        for row in range(2)
    )  # type: ignore[return-value]


def _ball_poly_from_directed(
    coefficients: Iterable[DirectedComplexInterval],
    remainder: gmpy2.mpfr | float = 0.0,
) -> _BallPoly:
    centers: list[complex] = []
    radii: list[float] = []
    for coefficient in coefficients:
        center, radius = _ball_from_complex_interval(coefficient)
        centers.append(center)
        radii.append(radius)
    if not centers:
        centers = [0.0j]
        radii = [0.0]
    radii[0] = math.nextafter(
        radii[0] + _upper_float(gmpy2.mpfr(remainder, PRECISION_BITS)),
        math.inf,
    )
    return _BallPoly(
        np.asarray(centers, dtype=complex),
        np.asarray(radii, dtype=float),
    )


class _TerminalCentreEvaluator:
    """Common centre row on the Stage-4I delay-aligned grid."""

    def __init__(self, repository: Path):
        self.repository = repository.resolve()
        self.diagnostic = _FourWordDiagnostic(self.repository)
        self.cells = _guide_cells(self.diagnostic)
        self.period = self.diagnostic.period
        self.tau0 = self.diagnostic.tau0
        self.tau1 = self.diagnostic.tau1
        self.step = self.tau0 / 512.0
        self.root_interval = DirectedInterval.from_float(
            float(self.diagnostic.data.root), PRECISION_BITS
        )
        # This is deliberately the exact binary64 *centre* period used by
        # the stored Fourier dictionaries.  It is not the true-period
        # enclosure.  ``_true_period_and_word_support`` constructs the latter
        # from the parent orbit radius and the exact algebraic delays.
        self.centre_period_point = DirectedInterval.from_float(
            self.period, PRECISION_BITS
        )
        self._trimmed: dict[
            int, tuple[Mapping[tuple[int, int], complex], gmpy2.mpfr]
        ] = {}
        self.maximum_polynomial_coefficient_envelope = 0.0
        self.bernstein_rectangle_count = 0
        self.activation_ambiguous_rectangle_count = 0

    def _trimmed_dictionary(
        self, value: Mapping[tuple[int, int], complex]
    ) -> tuple[Mapping[tuple[int, int], complex], gmpy2.mpfr]:
        key = id(value)
        if key not in self._trimmed:
            self._trimmed[key] = _validation_trim(
                value,
                float(self.diagnostic.data.root),
                PRECISION_BITS,
            )
        return self._trimmed[key]

    def fourier_cubic(
        self,
        value: Mapping[tuple[int, int], complex],
        left: float,
        width: float,
    ) -> _BallPoly:
        retained, omitted = self._trimmed_dictionary(value)
        left_interval = DirectedInterval.from_float(left, PRECISION_BITS)
        width_interval = DirectedInterval.from_float(width, PRECISION_BITS)
        coefficients = _directed_taylor(
            retained,
            left_interval,
            width_interval,
            self.centre_period_point,
            self.root_interval,
        )
        with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
            remainder = omitted + _directed_taylor_tail_upper(
                retained,
                width_interval,
                self.centre_period_point,
                self.root_interval,
            )
            for coefficient in coefficients[FOURIER_CENTRE_DEGREE + 1 :]:
                remainder += coefficient.upper_abs()
        result = _ball_poly_from_directed(
            coefficients[: FOURIER_CENTRE_DEGREE + 1], remainder
        )
        self.maximum_polynomial_coefficient_envelope = max(
            self.maximum_polynomial_coefficient_envelope,
            float(np.max(np.abs(result.center) + result.radius)),
        )
        return result

    @staticmethod
    def primitive_matrix(
        cell: _PrimitiveCell,
        name: str,
        segment_left: float | None = None,
        segment_right: float | None = None,
    ) -> tuple[tuple[_BallPoly, _BallPoly], tuple[_BallPoly, _BallPoly]]:
        coefficients = np.asarray(getattr(cell, name), dtype=float)
        matrix = tuple(
            tuple(
                _BallPoly(
                    np.asarray(coefficients[row, column, :], dtype=complex),
                    np.zeros(coefficients.shape[-1], dtype=float),
                )
                for column in range(2)
            )
            for row in range(2)
        )
        if segment_left is None or segment_right is None:
            return matrix  # type: ignore[return-value]
        local_width = cell.right - cell.left
        offset = (segment_left - cell.left) / local_width
        scale = (segment_right - segment_left) / local_width
        return tuple(
            tuple(
                _poly_affine(matrix[row][column], offset, scale)
                for column in range(2)
            )
            for row in range(2)
        )  # type: ignore[return-value]

    def output_segments(
        self,
    ) -> tuple[
        tuple[
            float,
            float,
            tuple[tuple[_BallPoly, _BallPoly], tuple[_BallPoly, _BallPoly]],
            tuple[tuple[_BallPoly, _BallPoly], tuple[_BallPoly, _BallPoly]],
            tuple[tuple[_BallPoly, _BallPoly], tuple[_BallPoly, _BallPoly]],
            tuple[tuple[_BallPoly, _BallPoly], tuple[_BallPoly, _BallPoly]],
            tuple[tuple[_BallPoly, _BallPoly], tuple[_BallPoly, _BallPoly]],
        ],
        ...,
    ]:
        returned_left = self.period - self.tau1
        segments = []
        for cell in self.cells:
            left = max(cell.left, returned_left)
            right = min(cell.right, self.period)
            if right <= left:
                continue
            segments.append(
                (
                    left,
                    right,
                    self.primitive_matrix(cell, "fundamental", left, right),
                    self.primitive_matrix(cell, "inverse", left, right),
                    self.primitive_matrix(cell, "word0", left, right),
                    self.primitive_matrix(cell, "word1", left, right),
                    self.primitive_matrix(cell, "word00", left, right),
                )
            )
        return tuple(segments)

    def terminal_primitive_matrices(
        self,
    ) -> dict[
        str, tuple[tuple[_BallPoly, _BallPoly], tuple[_BallPoly, _BallPoly]]
    ]:
        final_cell = self.cells[-1]
        return {
            name: _matrix_point_value(
                self.primitive_matrix(final_cell, name), 1.0
            )
            for name in ("fundamental", "inverse", "word0", "word1", "word00")
        }

    def history_polynomials(self) -> dict[str, Any]:
        count = 640
        f_polys: list[_BallPoly] = []
        u0_polys: list[tuple[_BallPoly, _BallPoly] | None] = []
        u1_polys: list[tuple[_BallPoly, _BallPoly]] = []
        c0u0_polys: list[tuple[_BallPoly, _BallPoly] | None] = []
        normalized_scalar = 1.0 / self.diagnostic.fq
        for index in range(count):
            eta_left = -self.tau1 + index * self.step
            width = self.step
            f_value = _zero_poly()
            eta_right = eta_left + width
            for delay, density in self.diagnostic.f_densities:
                # Including a whole boundary cell is an outward operation.
                # The exact algebraic-delay displacement is far below the
                # registered activation padding and is checked later.
                if eta_right >= -delay - ACTIVATION_PADDING_BINARY64:
                    f_value = _poly_add(
                        f_value,
                        self.fourier_cubic(density, eta_left, width),
                    )
            f_polys.append(_poly_scale(f_value, normalized_scalar))

            insertion1 = index
            g1 = self.primitive_matrix(self.cells[insertion1], "inverse")
            b1 = self.fourier_cubic(
                self.diagnostic.data.delayed1,
                index * self.step,
                width,
            )
            u1_polys.append(
                (
                    _poly_mul(g1[0][0], b1),
                    _poly_mul(g1[1][0], b1),
                )
            )

            if index < 128:
                u0_polys.append(None)
                c0u0_polys.append(None)
                continue
            insertion0 = index - 128
            g0 = self.primitive_matrix(self.cells[insertion0], "inverse")
            b0 = self.fourier_cubic(
                self.diagnostic.data.delayed0,
                insertion0 * self.step,
                width,
            )
            u0 = (
                _poly_mul(g0[0][0], b0),
                _poly_mul(g0[1][0], b0),
            )
            u0_polys.append(u0)
            shifted_c0 = self.primitive_matrix(
                self.cells[insertion0 + 512], "word0"
            )
            c0u0_polys.append(
                (
                    _poly_add(
                        _poly_mul(shifted_c0[0][0], u0[0]),
                        _poly_mul(shifted_c0[0][1], u0[1]),
                    ),
                    _poly_add(
                        _poly_mul(shifted_c0[1][0], u0[0]),
                        _poly_mul(shifted_c0[1][1], u0[1]),
                    ),
                )
            )
        return {
            "f": tuple(f_polys),
            "u0": tuple(u0_polys),
            "u1": tuple(u1_polys),
            "c0u0": tuple(c0u0_polys),
        }


def _stack_bernstein(
    values: Iterable[_BallPoly], degree: int
) -> tuple[np.ndarray, np.ndarray]:
    rows = [_bernstein(value, degree) for value in values]
    return (
        np.stack([row.center for row in rows]),
        np.stack([row.radius for row in rows]),
    )


def _add_outer_batch(
    center: np.ndarray,
    radius: np.ndarray,
    t_value: _BallPoly,
    history_center: np.ndarray,
    history_radius: np.ndarray,
    mask: np.ndarray,
    *,
    sign: int = 1,
) -> None:
    if not np.any(mask):
        return
    t_center = sign * t_value.center
    t_radius = t_value.radius
    h_center = history_center[mask]
    h_radius = history_radius[mask]
    product_center = t_center[None, :, None] * h_center[:, None, :]
    product_radius = (
        np.abs(t_center)[None, :, None] * h_radius[:, None, :]
        + t_radius[None, :, None] * np.abs(h_center)[:, None, :]
        + t_radius[None, :, None] * h_radius[:, None, :]
    )
    envelope = (
        np.abs(t_center)[None, :, None] + t_radius[None, :, None]
    ) * (np.abs(h_center)[:, None, :] + h_radius[:, None, :])
    product_radius += _round_radius(envelope)
    _audit_binary_ball(product_center, product_radius)
    center[mask] += product_center
    radius[mask] += product_radius + _round_radius(
        np.abs(center[mask]) + np.abs(product_center)
    )
    _audit_binary_ball(center[mask], radius[mask])


def _batch_bounds(center: np.ndarray, radius: np.ndarray) -> np.ndarray:
    _audit_binary_ball(center, radius)
    return np.nextafter(
        np.max(np.abs(center) + radius, axis=(1, 2)), math.inf
    )


def _scalar_ball_poly(value: tuple[complex, float]) -> _BallPoly:
    return _BallPoly(
        np.asarray([value[0]], dtype=complex),
        np.asarray([value[1]], dtype=float),
    )


def _row_dot(
    row: tuple[_BallPoly, _BallPoly],
    column: tuple[_BallPoly, _BallPoly],
) -> _BallPoly:
    return _poly_add(
        _poly_mul(row[0], column[0]),
        _poly_mul(row[1], column[1]),
    )


def _matrix_sum(
    values: Iterable[
        tuple[tuple[_BallPoly, _BallPoly], tuple[_BallPoly, _BallPoly]]
    ],
) -> tuple[tuple[_BallPoly, _BallPoly], tuple[_BallPoly, _BallPoly]]:
    result = (
        (_zero_poly(), _zero_poly()),
        (_zero_poly(), _zero_poly()),
    )
    for value in values:
        result = _matrix_add(result, value)
    return result


def _terminal_density_polynomials(
    terminal: Mapping[
        str, tuple[tuple[_BallPoly, _BallPoly], tuple[_BallPoly, _BallPoly]]
    ],
    histories: Mapping[str, Any],
    q_terminal: tuple[_BallPoly, _BallPoly],
) -> tuple[
    tuple[tuple[_BallPoly, ...], tuple[_BallPoly, ...]],
    tuple[tuple[_BallPoly, ...], tuple[_BallPoly, ...]],
]:
    fundamental = terminal["fundamental"]
    word0 = terminal["word0"]
    fundamental_word0 = _matrix_multiply(fundamental, word0)
    raw_by_component: list[list[_BallPoly]] = [[], []]
    stable_by_component: list[list[_BallPoly]] = [[], []]
    for index in range(640):
        f_value = histories["f"][index]
        u1 = histories["u1"][index]
        u0 = histories["u0"][index]
        c0u0 = histories["c0u0"][index]
        for component in range(2):
            raw = _row_dot(fundamental[component], u1)
            if u0 is not None and c0u0 is not None:
                raw = _poly_add(raw, _row_dot(fundamental[component], u0))
                raw = _poly_add(
                    raw, _row_dot(fundamental_word0[component], u0)
                )
                raw = _poly_sub(
                    raw, _row_dot(fundamental[component], c0u0)
                )
            raw_by_component[component].append(raw)
            stable_by_component[component].append(
                _poly_sub(raw, _poly_mul(q_terminal[component], f_value))
            )
    return (
        (tuple(raw_by_component[0]), tuple(raw_by_component[1])),
        (tuple(stable_by_component[0]), tuple(stable_by_component[1])),
    )


def _integrated_history_upper(
    values: Iterable[_BallPoly], step: float
) -> float:
    bounds = np.asarray(
        [
            _univariate_bernstein_upper(value, HISTORY_BERNSTEIN_DEGREE)
            for value in values
        ]
    )
    return math.nextafter(float(np.sum(bounds) * step), math.inf)


def _common_center_certificate(
    evaluator: _TerminalCentreEvaluator,
) -> dict[str, Any]:
    global _ACTIVE_BINARY_AUDIT
    if _ACTIVE_BINARY_AUDIT is not None:
        raise RuntimeError("a Stage-4L binary audit is already active")
    _ACTIVE_BINARY_AUDIT = {
        "actual_envelope": 0.0,
        "array_count": 0,
        "scalar_coefficient_count": 0,
    }
    histories = evaluator.history_polynomials()
    terminal = evaluator.terminal_primitive_matrices()
    terminal_bracket = _matrix_sum(
        (
            _matrix_identity(),
            terminal["word0"],
            terminal["word1"],
            terminal["word00"],
        )
    )
    terminal_resolvent_atom = _matrix_multiply(
        terminal["fundamental"], terminal_bracket
    )
    final_cell = evaluator.cells[-1]
    final_width = final_cell.right - final_cell.left
    q_terminal = tuple(
        _scalar_ball_poly(
            _poly_value(
                evaluator.fourier_cubic(
                    dictionary, final_cell.left, final_width
                ),
                1.0,
            )
        )
        for dictionary in (
            evaluator.diagnostic.data.qsection_v,
            evaluator.diagnostic.data.qsection_w,
        )
    )
    xdot_terminal = tuple(
        _scalar_ball_poly(
            _poly_value(
                evaluator.fourier_cubic(
                    dictionary, final_cell.left, final_width
                ),
                1.0,
            )
        )
        for dictionary in (
            evaluator.diagnostic.data.xdot_v,
            evaluator.diagnostic.data.xdot_w,
        )
    )
    event_denominator = float(evaluator.diagnostic.xdot(evaluator.period)[0])
    if not event_denominator > 0.24:
        raise ArithmeticError("the Stage-4L centre event denominator changed")
    normalized_recovery_atom = complex(
        evaluator.diagnostic.f_recovery_atom / evaluator.diagnostic.fq
    )
    terminal_raw_atoms = tuple(
        terminal_resolvent_atom[component][1] for component in range(2)
    )
    terminal_stable_atoms = tuple(
        _poly_sub(
            terminal_raw_atoms[component],
            _poly_scale(q_terminal[component], normalized_recovery_atom),
        )
        for component in range(2)
    )
    terminal_raw_density, terminal_stable_density = (
        _terminal_density_polynomials(
            terminal, histories, q_terminal  # type: ignore[arg-type]
        )
    )
    terminal_raw_density_bernstein = tuple(
        _stack_bernstein(values, HISTORY_BERNSTEIN_DEGREE)
        for values in terminal_raw_density
    )
    terminal_stable_density_bernstein = tuple(
        _stack_bernstein(values, HISTORY_BERNSTEIN_DEGREE)
        for values in terminal_stable_density
    )
    terminal_raw_row_norms = tuple(
        _univariate_bernstein_upper(terminal_raw_atoms[component])
        + _integrated_history_upper(
            terminal_raw_density[component], evaluator.step
        )
        for component in range(2)
    )

    recovery_ratio = _poly_scale(
        xdot_terminal[1], 1.0 / event_denominator
    )
    recovery_atom = _poly_sub(
        terminal_stable_atoms[1],
        _poly_mul(recovery_ratio, terminal_stable_atoms[0]),
    )
    recovery_density = tuple(
        _poly_sub(
            terminal_stable_density[1][index],
            _poly_mul(recovery_ratio, terminal_stable_density[0][index]),
        )
        for index in range(640)
    )
    recovery_atom_upper = _univariate_bernstein_upper(recovery_atom)
    recovery_density_tv_upper = _integrated_history_upper(
        recovery_density, evaluator.step
    )
    recovery_row_upper = math.nextafter(
        recovery_atom_upper + recovery_density_tv_upper, math.inf
    )
    recovery_q_event = _poly_sub(
        q_terminal[1], _poly_mul(recovery_ratio, q_terminal[0])
    )
    q_event_upper = _univariate_bernstein_upper(recovery_q_event)

    history_f_center, history_f_radius = _stack_bernstein(
        histories["f"], HISTORY_BERNSTEIN_DEGREE
    )
    history_u1 = tuple(
        _stack_bernstein(
            (histories["u1"][index][component] for index in range(640)),
            HISTORY_BERNSTEIN_DEGREE,
        )
        for component in range(2)
    )
    history_u0 = tuple(
        _stack_bernstein(
            (
                histories["u0"][index][component]
                if histories["u0"][index] is not None
                else _zero_poly()
                for index in range(640)
            ),
            HISTORY_BERNSTEIN_DEGREE,
        )
        for component in range(2)
    )
    history_c0u0 = tuple(
        _stack_bernstein(
            (
                histories["c0u0"][index][component]
                if histories["c0u0"][index] is not None
                else _zero_poly()
                for index in range(640)
            ),
            HISTORY_BERNSTEIN_DEGREE,
        )
        for component in range(2)
    )
    all_history_mask = np.ones(640, dtype=bool)
    indices = np.arange(640)
    eta_left = -evaluator.tau1 + indices * evaluator.step
    eta_right = eta_left + evaluator.step

    output_rows: list[dict[str, Any]] = []
    support_digest = sha256()
    maximum_voltage_row = 0.0
    maximum_voltage_index = 0
    segments = evaluator.output_segments()
    for output_index, (
        time_left,
        time_right,
        fundamental,
        _inverse,
        word0,
        word1,
        word00,
    ) in enumerate(segments):
        width = time_right - time_left
        bracket = _matrix_sum(
            (_matrix_identity(), word0, word1, word00)
        )
        atom_resolvent = _matrix_multiply(fundamental, bracket)
        fundamental_word0 = _matrix_multiply(fundamental, word0)
        q_voltage = evaluator.fourier_cubic(
            evaluator.diagnostic.data.qsection_v, time_left, width
        )
        xdot_voltage = evaluator.fourier_cubic(
            evaluator.diagnostic.data.xdot_v, time_left, width
        )
        ratio_voltage = _poly_scale(
            xdot_voltage, 1.0 / event_denominator
        )
        stable_atom = _poly_sub(
            atom_resolvent[0][1],
            _poly_scale(q_voltage, normalized_recovery_atom),
        )
        event_atom = _poly_sub(
            stable_atom,
            _poly_mul(ratio_voltage, terminal_stable_atoms[0]),
        )
        atom_upper = _univariate_bernstein_upper(
            event_atom, T_BERNSTEIN_DEGREE
        )

        q_event_poly = _poly_sub(
            q_voltage, _poly_mul(ratio_voltage, q_terminal[0])
        )
        q_event_upper = max(
            q_event_upper,
            _univariate_bernstein_upper(
                q_event_poly, T_BERNSTEIN_DEGREE
            ),
        )

        t_fundamental = tuple(
            tuple(
                _bernstein(fundamental[row][column], T_BERNSTEIN_DEGREE)
                for column in range(2)
            )
            for row in range(2)
        )
        t_fundamental_word0 = tuple(
            tuple(
                _bernstein(
                    fundamental_word0[row][column], T_BERNSTEIN_DEGREE
                )
                for column in range(2)
            )
            for row in range(2)
        )
        t_q = _bernstein(q_voltage, T_BERNSTEIN_DEGREE)
        t_ratio = _bernstein(ratio_voltage, T_BERNSTEIN_DEGREE)
        center = np.zeros(
            (640, T_BERNSTEIN_DEGREE + 1, HISTORY_BERNSTEIN_DEGREE + 1),
            dtype=complex,
        )
        radius = np.zeros(center.shape, dtype=float)

        _add_outer_batch(
            center,
            radius,
            t_q,
            history_f_center,
            history_f_radius,
            all_history_mask,
            sign=-1,
        )
        _add_outer_batch(
            center,
            radius,
            t_ratio,
            terminal_stable_density_bernstein[0][0],
            terminal_stable_density_bernstein[0][1],
            all_history_mask,
            sign=-1,
        )

        activation_groups: list[
            tuple[np.ndarray, np.ndarray, list[tuple[_BallPoly, np.ndarray, np.ndarray, int]]]
        ] = []

        def add_activation_group(
            activation_left: np.ndarray,
            activation_right: np.ndarray,
            terms: list[tuple[_BallPoly, np.ndarray, np.ndarray, int]],
            support: np.ndarray,
        ) -> None:
            always = support & (
                activation_right + ACTIVATION_PADDING_BINARY64 <= time_left
            )
            ambiguous = support & ~always & (
                activation_left - ACTIVATION_PADDING_BINARY64 < time_right
            )
            for t_value, h_center, h_radius, sign in terms:
                _add_outer_batch(
                    center,
                    radius,
                    t_value,
                    h_center,
                    h_radius,
                    always,
                    sign=sign,
                )
            activation_groups.append((always, ambiguous, terms))

        support1 = np.ones(640, dtype=bool)
        activation1_left = eta_left + evaluator.tau1
        activation1_right = eta_right + evaluator.tau1
        add_activation_group(
            activation1_left,
            activation1_right,
            [
                (
                    t_fundamental[0][middle],
                    history_u1[middle][0],
                    history_u1[middle][1],
                    1,
                )
                for middle in range(2)
            ],
            support1,
        )

        support0 = indices >= 128
        activation0_left = eta_left + evaluator.tau0
        activation0_right = eta_right + evaluator.tau0
        add_activation_group(
            activation0_left,
            activation0_right,
            [
                (
                    t_fundamental[0][middle],
                    history_u0[middle][0],
                    history_u0[middle][1],
                    1,
                )
                for middle in range(2)
            ],
            support0,
        )

        activation00_left = eta_left + 2.0 * evaluator.tau0
        activation00_right = eta_right + 2.0 * evaluator.tau0
        add_activation_group(
            activation00_left,
            activation00_right,
            [
                *(
                    (
                        t_fundamental_word0[0][middle],
                        history_u0[middle][0],
                        history_u0[middle][1],
                        1,
                    )
                    for middle in range(2)
                ),
                *(
                    (
                        t_fundamental[0][middle],
                        history_c0u0[middle][0],
                        history_c0u0[middle][1],
                        -1,
                    )
                    for middle in range(2)
                ),
            ],
            support0,
        )

        ambiguous_count = np.zeros(640, dtype=int)
        for _always, ambiguous, _terms in activation_groups:
            ambiguous_count += ambiguous.astype(int)
        if np.max(ambiguous_count) > 1:
            raise ArithmeticError(
                "two delay activations entered one Stage-4L rectangle"
            )
        bounds = _batch_bounds(center, radius)
        for _always, ambiguous, terms in activation_groups:
            if not np.any(ambiguous):
                continue
            evaluator.activation_ambiguous_rectangle_count += int(
                np.sum(ambiguous)
            )
            local_center = center[ambiguous].copy()
            local_radius = radius[ambiguous].copy()
            local_mask = np.ones(np.sum(ambiguous), dtype=bool)
            for t_value, h_center, h_radius, sign in terms:
                _add_outer_batch(
                    local_center,
                    local_radius,
                    t_value,
                    h_center[ambiguous],
                    h_radius[ambiguous],
                    local_mask,
                    sign=sign,
                )
            bounds[ambiguous] = np.maximum(
                bounds[ambiguous],
                _batch_bounds(local_center, local_radius),
            )
        density_tv = math.nextafter(
            float(np.sum(bounds) * evaluator.step), math.inf
        )
        row_upper = math.nextafter(atom_upper + density_tv, math.inf)
        if row_upper > maximum_voltage_row:
            maximum_voltage_row = row_upper
            maximum_voltage_index = output_index
        output_rows.append(
            {
                "cell_index": output_index,
                "time_left_binary64": format(time_left, ".17g"),
                "time_right_binary64": format(time_right, ".17g"),
                "current_recovery_atom_upper": format(atom_upper, ".17g"),
                "voltage_density_tv_upper": format(density_tv, ".17g"),
                "row_norm_upper": format(row_upper, ".17g"),
            }
        )
        support_digest.update(
            np.asarray(bounds, dtype="<f8").tobytes(order="C")
        )
        evaluator.bernstein_rectangle_count += 640

    center_upper = max(maximum_voltage_row, recovery_row_upper)
    evaluator.bernstein_rectangle_count += 640
    recovery_density_bounds = np.asarray(
        [
            _univariate_bernstein_upper(
                value, HISTORY_BERNSTEIN_DEGREE
            )
            for value in recovery_density
        ],
        dtype="<f8",
    )
    support_digest.update(recovery_density_bounds.tobytes(order="C"))
    result = {
        "center_common_row_upper_binary64_with_local_ball_guards": format(
            center_upper, ".17g"
        ),
        "voltage_history_row_upper_binary64": format(
            maximum_voltage_row, ".17g"
        ),
        "voltage_history_argmax_cell_index": maximum_voltage_index,
        "recovery_row_upper_binary64": format(recovery_row_upper, ".17g"),
        "recovery_atom_upper_binary64": format(recovery_atom_upper, ".17g"),
        "recovery_density_tv_upper_binary64": format(
            recovery_density_tv_upper, ".17g"
        ),
        "q_event_center_upper_binary64": format(q_event_upper, ".17g"),
        "terminal_raw_row_norm_upper_binary64": format(
            max(terminal_raw_row_norms), ".17g"
        ),
        "terminal_raw_component_row_norms_binary64": [
            format(value, ".17g") for value in terminal_raw_row_norms
        ],
        "event_denominator_center_binary64": format(
            event_denominator, ".17g"
        ),
        "returned_output_cell_count": len(segments),
        "input_history_cell_count": 640,
        "bernstein_rectangle_count_including_recovery": (
            evaluator.bernstein_rectangle_count
        ),
        "activation_ambiguous_rectangle_count": (
            evaluator.activation_ambiguous_rectangle_count
        ),
        "support_cell_bounds_sha256": support_digest.hexdigest(),
        "output_cell_rows": output_rows,
        "maximum_polynomial_coefficient_envelope_binary64": format(
            evaluator.maximum_polynomial_coefficient_envelope, ".17g"
        ),
        "t_bernstein_degree": T_BERNSTEIN_DEGREE,
        "history_bernstein_degree": HISTORY_BERNSTEIN_DEGREE,
        "fourier_centre_degree": FOURIER_CENTRE_DEGREE,
        "common_row_formula": (
            "R_theta*Pi_T*U(T,0)*P_s; stable deflation and terminal event "
            "correction are summed coefficientwise before Bernstein modulus"
        ),
        "section_quotient": (
            "the current-voltage delta_0 atom is absent exactly because "
            "Sigma_0={h:h_v(0)=0}; only the current-recovery atom is normed"
        ),
        "finite_node_maximum_used": False,
        "gaussian_quadrature_used": False,
        "continuous_output_phase_supremum": True,
        "outward_absolute_density_integration": True,
    }
    audit = _ACTIVE_BINARY_AUDIT
    assert audit is not None
    result["actual_all_intermediate_ball_envelope_upper_binary64"] = format(
        math.nextafter(float(audit["actual_envelope"]), math.inf), ".17g"
    )
    result["audited_ball_array_count"] = int(audit["array_count"])
    result["audited_scalar_coefficient_count"] = int(
        audit["scalar_coefficient_count"]
    )
    result["all_ballpoly_and_bivariate_arrays_audited"] = True
    _ACTIVE_BINARY_AUDIT = None
    return result


def _json_roundtrip(value: Any) -> Any:
    return json.loads(
        json.dumps(
            value,
            sort_keys=True,
            ensure_ascii=True,
            allow_nan=False,
        )
    )


def _runtime_record() -> dict[str, str]:
    return {
        "python": platform.python_version(),
        "python_implementation": platform.python_implementation(),
        "numpy": np.__version__,
        "gmpy2": gmpy2.version(),
        "mpfr": gmpy2.mpfr_version(),
        "openblas_num_threads": os.environ.get("OPENBLAS_NUM_THREADS", ""),
        "omp_num_threads": os.environ.get("OMP_NUM_THREADS", ""),
        "arithmetic": (
            "192-bit outward MPFR for true-period/support/error ledgers; "
            "binary64 polynomial centres with coefficientwise balls, an "
            "explicit gamma_n audit, and an independent 1e-5 final guard"
        ),
        "installation": "fresh replay before fsync and atomic replacement",
    }


def _require_runtime() -> None:
    if os.environ.get("OPENBLAS_NUM_THREADS") != PINNED_OPENBLAS_NUM_THREADS:
        raise RuntimeError(
            "Stage-4L requires OPENBLAS_NUM_THREADS=8 for a reproducible replay"
        )
    if os.environ.get("OMP_NUM_THREADS") != PINNED_OMP_NUM_THREADS:
        raise RuntimeError(
            "Stage-4L requires OMP_NUM_THREADS=1 for a reproducible replay"
        )


def _mpfr(value: str | int | float | gmpy2.mpfr) -> gmpy2.mpfr:
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
        return gmpy2.mpfr(value, PRECISION_BITS)


def _parent_payloads(repository: Path) -> dict[str, Mapping[str, Any]]:
    repository = repository.resolve()
    payloads: dict[str, Mapping[str, Any]] = {}
    validators = {
        STAGE3_RESULT_RELATIVE_PATH: validate_stage3_stable_projection_result,
        STAGE4D_RESULT_RELATIVE_PATH: validate_stage4d_result,
        STAGE4E_RESULT_RELATIVE_PATH: validate_stage4e_result,
        STAGE4H_RESULT_RELATIVE_PATH: validate_stage4h_result,
        STAGE4I_RESULT_RELATIVE_PATH: validate_stage4i_result,
    }
    for relative, validator in validators.items():
        path = repository / relative
        if _sha256_path(path) != PARENT_HASHES[relative]:
            raise ValueError(f"the Stage-4L parent changed: {relative}")
        payload = json.loads(path.read_text(encoding="utf-8"))
        validator(payload, repository)
        payloads[relative] = payload
    return payloads


def _binary_operation_components() -> dict[str, int]:
    return {
        # A degree-(6,9) Bernstein rectangle has 7*10 coefficients.  Ten is
        # the maximum number of simultaneous outer-product terms:
        # qf, terminal event, two tau1, two tau0, and four double-delay terms.
        "two_activation_cases_times_7x10_coefficients_times_40_real_ops": (
            2 * 7 * 10 * 10 * 40
        ),
        "two_univariate_bernstein_transforms_real_ops": (
            2 * ((7 * 7) + (10 * 10)) * 16
        ),
        "complex_moduli_and_rectangle_max_real_ops": 7 * 10 * 12,
        "positive_640_cell_density_reduction_real_ops": 640,
        "polynomial_affine_and_convolution_safety_ops": 8192,
    }


def _binary_rounding_certificate(center: Mapping[str, Any]) -> dict[str, Any]:
    operation_components = _binary_operation_components()
    derived_operation_count = sum(operation_components.values())
    if derived_operation_count > MAX_GUARDED_REAL_OPERATIONS:
        raise ArithmeticError("the Stage-4L derived operation count overflowed")
    unit = DirectedInterval.from_decimal(
        BINARY64_UNIT_ROUNDOFF, PRECISION_BITS
    )
    count = DirectedInterval.from_decimal(
        MAX_GUARDED_REAL_OPERATIONS, PRECISION_BITS
    )
    gamma = count * unit / (1 - count * unit)
    local_guard = DirectedInterval.from_float(
        LOCAL_FLOAT_OPERATION_GUARD, PRECISION_BITS
    )
    envelope = DirectedInterval.from_decimal(
        BINARY_KERNEL_ENVELOPE_CAP, PRECISION_BITS
    )
    unguarded = gamma * (1 + envelope)
    final_guard = DirectedInterval.from_decimal(
        CENTER_BINARY_BERNSTEIN_GUARD, PRECISION_BITS
    )
    observed = DirectedInterval.from_decimal(
        center["actual_all_intermediate_ball_envelope_upper_binary64"],
        PRECISION_BITS,
    )
    if not gamma.upper < local_guard.lower:
        raise ArithmeticError("the Stage-4L local gamma_n guard failed")
    if not unguarded.upper < final_guard.lower:
        raise ArithmeticError("the Stage-4L final binary guard failed")
    if not observed.upper < envelope.lower:
        raise ArithmeticError("the Stage-4L coefficient envelope cap failed")
    return {
        "binary64_unit_roundoff_exact": BINARY64_UNIT_ROUNDOFF,
        "maximum_real_operations_per_guarded_kernel": (
            MAX_GUARDED_REAL_OPERATIONS
        ),
        "operation_count_derivation": operation_components,
        "derived_worst_case_real_operation_count": derived_operation_count,
        "derived_operation_count_at_most_registered_maximum": True,
        "gamma_n_upper": decimal_upper(gamma.upper),
        "local_coefficient_ball_guard_binary64": format(
            LOCAL_FLOAT_OPERATION_GUARD, ".17g"
        ),
        "local_guard_strictly_exceeds_gamma_n": True,
        "maximum_unguarded_real_operations_before_final_guard": (
            MAX_UNGUARDED_REAL_OPERATIONS
        ),
        "analytic_binary_kernel_envelope_cap": BINARY_KERNEL_ENVELOPE_CAP,
        "observed_fourier_input_coefficient_envelope_binary64": center[
            "maximum_polynomial_coefficient_envelope_binary64"
        ],
        "actual_all_intermediate_ball_envelope_upper_binary64": center[
            "actual_all_intermediate_ball_envelope_upper_binary64"
        ],
        "audited_ball_array_count": center["audited_ball_array_count"],
        "audited_scalar_coefficient_count": center[
            "audited_scalar_coefficient_count"
        ],
        "all_ballpoly_and_bivariate_arrays_audited": center[
            "all_ballpoly_and_bivariate_arrays_audited"
        ],
        "actual_intermediate_envelope_strictly_below_analytic_cap": True,
        "unguarded_reduction_error_upper": decimal_upper(unguarded.upper),
        "independent_final_binary_bernstein_guard": (
            CENTER_BINARY_BERNSTEIN_GUARD
        ),
        "final_guard_strictly_exceeds_unguarded_error": True,
        "guarded_kernels": [
            "complex polynomial add/subtract/multiply/affine restriction",
            "monomial-to-Bernstein matrix application",
            "bivariate Bernstein outer products and coefficientwise sums",
        ],
        "unGuarded_final_operations": (
            "complex modulus, coefficient maximum, and at most 640-term "
            "positive density reduction; all are covered by the independent "
            "final guard"
        ),
        "numpy_nextafter_is_not_the_rounding_proof": True,
        "ieee_gamma_ledger_is_the_rounding_proof": True,
    }


def _true_period_and_word_support(
    evaluator: _TerminalCentreEvaluator,
    uncertainty: Mapping[str, float],
) -> dict[str, Any]:
    precision = PRECISION_BITS
    sqrt5 = DirectedInterval.from_decimal(5, precision).sqrt()
    tau0 = sqrt5 * 4
    tau1 = sqrt5 * 5
    period = DirectedInterval.symmetric_radius(
        evaluator.period, uncertainty["period_error"], precision
    )
    parent_parameters = evaluator.diagnostic.data.prepared.base.parameters
    parent_tau0 = DirectedInterval.from_bounds(
        parent_parameters["tau_0"].lower,
        parent_parameters["tau_0"].upper,
        precision,
    )
    parent_tau1 = DirectedInterval.from_bounds(
        parent_parameters["tau_1"].lower,
        parent_parameters["tau_1"].upper,
        precision,
    )
    if not (
        parent_tau0.lower <= tau0.lower <= tau0.upper <= parent_tau0.upper
        and parent_tau1.lower <= tau1.lower <= tau1.upper <= parent_tau1.upper
    ):
        raise ArithmeticError("the exact algebraic delays left the parent boxes")

    margins = {
        "T_minus_tau_max_lower": period.lower - tau1.upper,
        "T_minus_two_tau0_lower": period.lower - 2 * tau0.upper,
        "tau0_plus_tau1_minus_T_upper_end_lower": (
            tau0.lower + tau1.lower - period.upper
        ),
        "three_tau0_minus_T_upper_end_lower": (
            3 * tau0.lower - period.upper
        ),
    }
    if any(value <= 0 for value in margins.values()):
        raise ArithmeticError("the directed Stage-4L four-word support failed")

    tau0_center = DirectedInterval.from_float(evaluator.tau0, precision)
    tau1_center = DirectedInterval.from_float(evaluator.tau1, precision)
    step_exact = tau0 / 512
    step_center = DirectedInterval.from_float(evaluator.step, precision)
    tau0_shift = (tau0 - tau0_center).upper_abs()
    tau1_shift = (tau1 - tau1_center).upper_abs()
    step_shift = (step_exact - step_center).upper_abs()
    period_shift = _mpfr(uncertainty["period_error"])
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        # The terms respectively cover the returned-phase origin, terminal
        # time, input-cell origin/width, and both activation diagonals.
        combined_coordinate_shift = (
            2 * period_shift
            + 4 * tau1_shift
            + 4 * tau0_shift
            + 1280 * step_shift
        )
        activation_displacement = (
            period_shift + 2 * tau1_shift + 2 * tau0_shift + 640 * step_shift
        )
    padding = DirectedInterval.from_float(
        ACTIVATION_PADDING_BINARY64, precision
    )
    if not activation_displacement < padding.lower:
        raise ArithmeticError("the Stage-4L activation padding is too small")

    return {
        "precision_bits": precision,
        "true_period_lower": decimal_lower(period.lower),
        "true_period_upper": decimal_upper(period.upper),
        "parent_period_error_upper": decimal_upper(period_shift),
        "tau0_exact": "4*sqrt(5)",
        "tau0_lower": decimal_lower(tau0.lower),
        "tau0_upper": decimal_upper(tau0.upper),
        "tau1_exact": "5*sqrt(5)",
        "tau1_lower": decimal_lower(tau1.lower),
        "tau1_upper": decimal_upper(tau1.upper),
        "parent_delay_intervals_contain_exact_algebraic_delays": True,
        "directed_margin_lower": {
            name: decimal_lower(value) for name, value in margins.items()
        },
        "T_minus_tau_max_strictly_positive": True,
        "T_minus_two_tau0_strictly_positive": True,
        "T_strictly_less_than_tau0_plus_tau1": True,
        "T_strictly_less_than_three_tau0": True,
        "returned_history_has_no_unadvanced_identity_block": True,
        "exact_active_words": ["empty", "(0)", "(1)", "(0,0)"],
        "centre_grid_period_binary64": format(evaluator.period, ".17g"),
        "centre_period_is_not_claimed_exact": True,
        "centre_returned_history_left_binary64": format(
            evaluator.period - evaluator.tau1, ".17g"
        ),
        "true_returned_history_cover_lower": decimal_lower(
            period.lower - tau1.upper
        ),
        "true_returned_history_cover_upper": decimal_upper(period.upper),
        "tau0_centre_displacement_upper": decimal_upper(tau0_shift),
        "tau1_centre_displacement_upper": decimal_upper(tau1_shift),
        "regular_step_centre_displacement_upper": decimal_upper(step_shift),
        "combined_coordinate_shift_upper": decimal_upper(
            combined_coordinate_shift
        ),
        "activation_displacement_upper": decimal_upper(
            activation_displacement
        ),
        "activation_padding_binary64": format(
            ACTIVATION_PADDING_BINARY64, ".17g"
        ),
        "activation_padding_strictly_contains_true_displacement": True,
        "centre_grid_extended_to_true_T_plus_by_lipschitz_remainder": True,
        "complete_true_returned_history_covered": True,
    }


def _dictionary_time_derivative_l1_upper(
    value: Mapping[tuple[int, int], complex],
    evaluator: _TerminalCentreEvaluator,
) -> gmpy2.mpfr:
    precision = PRECISION_BITS
    maximum_time = max(evaluator.period, evaluator.tau1)
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        root_abs = abs(_mpfr(evaluator.diagnostic.data.root))
        period_lower = _mpfr(evaluator.period)
        phase = _mpfr(maximum_time) / period_lower
        total = gmpy2.mpfr(0, precision)
        for (growth, mode), coefficient in value.items():
            exponent = abs(growth) * root_abs * phase
            amplitude = gmpy2.exp(exponent)
            frequency = (
                abs(growth) * root_abs
                + 2 * gmpy2.const_pi(precision) * abs(mode)
            ) / period_lower
            total += (
                _complex_point(complex(coefficient), precision).upper_abs()
                * amplitude
                * frequency
            )
    return total


def _time_lipschitz_certificate(
    evaluator: _TerminalCentreEvaluator,
    parents: Mapping[str, Mapping[str, Any]],
    uncertainty: Mapping[str, float],
    center: Mapping[str, Any],
) -> dict[str, Any]:
    stage4i = parents[STAGE4I_RESULT_RELATIVE_PATH]["artifact"]
    tubes = stage4i["directed_primitive_error_tubes"]
    residual = stage4i["directed_residual_certificate"]
    guide = tubes["maximum_guide_entry_upper"]
    errors = tubes["maximum_error_radius_upper"]
    coefficients = residual["maximum_coefficient_modulus_upper"]

    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
        mf = _mpfr(guide["F"]) + _mpfr(errors["F"])
        mg = _mpfr(guide["G"]) + _mpfr(errors["G"])
        mc0 = _mpfr(guide["C0"]) + _mpfr(errors["C0"])
        mc1 = _mpfr(guide["C1"]) + _mpfr(errors["C1"])
        mc00 = _mpfr(guide["C00"]) + _mpfr(errors["C00"])
        delayed = max(
            _mpfr(coefficients["delayed0"]),
            _mpfr(coefficients["delayed1"]),
        ) + _mpfr(tubes["delayed_coefficient_each_model_error_upper"])
        current = _mpfr(coefficients["current"]) + _mpfr(
            tubes["current_coefficient_model_error_upper"]
        )
        tau1 = _mpfr(evaluator.tau1) + _mpfr("1e-12")
        raw_atom = mf * (1 + 2 * (mc0 + mc1 + mc00))
        insertion = mg * delayed
        raw_density_point = (
            4 * mf * insertion + 8 * mf * mc0 * insertion
        )
        raw_operator = raw_atom + tau1 * raw_density_point
        raw_time_derivative = (current + 1 + 2 * delayed) * raw_operator

        parameters = evaluator.diagnostic.data.prepared.base.parameters
        epsilon = _mpfr(parameters["epsilon"].upper)
        kappa3 = _mpfr(parameters["kappa_3"].upper)
        voltage = _mpfr(uncertainty["voltage_bound"])
        xdot = _mpfr(uncertainty["xdot_bound"]) + _mpfr(
            uncertainty["xdot_error"]
        )
        delayed_derivative = 6 * epsilon * kappa3 * voltage * xdot
        insertion_derivative = (
            2 * mg * max(current, _mpfr(1)) * delayed
            + mg * delayed_derivative
        )
        word_derivative_entry = mf * insertion
        raw_history_derivative_point = (
            4 * mf * insertion_derivative
            + 2
            * mf
            * (
                4 * mc0 * insertion_derivative
                + 4 * word_derivative_entry * insertion
            )
        )
        raw_history_operator_derivative = (
            tau1 * raw_history_derivative_point
        )

        qdot = max(
            _dictionary_l1_directed_upper(
                evaluator.diagnostic.data.udot_v,
                evaluator.diagnostic.data.root,
                precision=PRECISION_BITS,
            ),
            _dictionary_l1_directed_upper(
                evaluator.diagnostic.data.udot_w,
                evaluator.diagnostic.data.root,
                precision=PRECISION_BITS,
            ),
        ) + _mpfr(uncertainty["udot_error"])
        xddot = max(
            _dictionary_l1_directed_upper(
                evaluator.diagnostic.data.xddot_v,
                evaluator.diagnostic.data.root,
                precision=PRECISION_BITS,
            ),
            _dictionary_l1_directed_upper(
                evaluator.diagnostic.data.xddot_w,
                evaluator.diagnostic.data.root,
                precision=PRECISION_BITS,
            ),
        ) + _mpfr(uncertainty["xddot_error"])
        speed = _mpfr(uncertainty["event_speed_lower"])
        qbound = _mpfr(uncertainty["u_bound"]) + _mpfr(
            uncertainty["qsection_error"]
        )
        ratio = _mpfr(uncertainty["xdot_bound"]) / speed
        ratio_output_derivative = xddot / speed
        ratio_terminal_derivative = (
            _mpfr(uncertainty["xdot_bound"]) * xddot / speed**2
        )
        raw_common_time_derivative = (
            (1 + ratio) * raw_time_derivative
            + (ratio_output_derivative + ratio_terminal_derivative)
            * raw_operator
        )
        q_common_time_derivative = (
            (1 + ratio) * qdot
            + (ratio_output_derivative + ratio_terminal_derivative) * qbound
        )

        stage4e = parents[STAGE4E_RESULT_RELATIVE_PATH]["artifact"][
            "continuous_history_correlated_deflation"
        ]
        stage4d = parents[STAGE4D_RESULT_RELATIVE_PATH]["artifact"][
            "continuous_history_measure_enclosure"
        ]
        exact_restricted_f = _mpfr(
            stage4d["current_recovery_atom_modulus_upper"]
        ) + _mpfr(stage4d["voltage_history_density_total_variation_upper"])
        f_difference = _mpfr(stage4e["history_measure_difference_upper"])
        fq_center_lower = _complex_point(
            complex(evaluator.diagnostic.fq), PRECISION_BITS
        ).lower_abs()
        f_center_norm = (exact_restricted_f + f_difference) / fq_center_lower
        rank_time_derivative = q_common_time_derivative * f_center_norm
        f_density_derivative = upward_sum(
            tuple(
                _dictionary_time_derivative_l1_upper(dictionary, evaluator)
                for _delay, dictionary in evaluator.diagnostic.f_densities
            ),
            PRECISION_BITS,
        ) / fq_center_lower
        history_rank_derivative = (
            tau1
            * _mpfr(center["q_event_center_upper_binary64"])
            * f_density_derivative
        )
        candidate = 4 * (
            raw_common_time_derivative
            + rank_time_derivative
            + raw_history_operator_derivative
            + history_rank_derivative
            + 1
        )
        cap = _mpfr(TIME_LIPSCHITZ_CAP)
    if not candidate < cap:
        raise ArithmeticError("the Stage-4L time-Lipschitz cap failed")
    return {
        "derivation": (
            "four-word primitive maxima bound the raw operator and its DDE "
            "time derivative; G'=-GA and the exact polynomial delayed "
            "coefficient derivative bound the history derivative; directed "
            "Fourier first moments bound the centre q, xdot and f rows"
        ),
        "raw_operator_norm_upper": decimal_upper(raw_operator),
        "raw_common_time_derivative_upper": decimal_upper(
            raw_common_time_derivative
        ),
        "raw_history_operator_derivative_upper": decimal_upper(
            raw_history_operator_derivative
        ),
        "rank_one_time_derivative_upper": decimal_upper(rank_time_derivative),
        "rank_one_history_derivative_upper": decimal_upper(
            history_rank_derivative
        ),
        "combined_analytic_candidate_upper": decimal_upper(candidate),
        "registered_lipschitz_cap": TIME_LIPSCHITZ_CAP,
        "candidate_strictly_below_registered_cap": True,
        "unknown_stable_norm_used_in_derivation": False,
        "unknown_k_s_used_in_derivation": False,
        "self_referential_error_propagation_used": False,
    }


def _directed_error_ledger(
    evaluator: _TerminalCentreEvaluator,
    parents: Mapping[str, Mapping[str, Any]],
    uncertainty: Mapping[str, float],
    center: Mapping[str, Any],
    support: Mapping[str, Any],
    binary: Mapping[str, Any],
    lipschitz: Mapping[str, Any],
) -> dict[str, Any]:
    stage4i = parents[STAGE4I_RESULT_RELATIVE_PATH]["artifact"]
    stage4e = parents[STAGE4E_RESULT_RELATIVE_PATH]["artifact"][
        "continuous_history_correlated_deflation"
    ]
    stage4d = parents[STAGE4D_RESULT_RELATIVE_PATH]["artifact"][
        "continuous_history_measure_enclosure"
    ]
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
        center_upper = _mpfr(
            center["center_common_row_upper_binary64_with_local_ball_guards"]
        )
        binary_guard = _mpfr(CENTER_BINARY_BERNSTEIN_GUARD)
        primitive = _mpfr(
            stage4i["induced_measure_error_diagnostic"][
                "coarse_primitive_induced_event_measure_error_upper"
            ]
        )
        exact_restricted_f = _mpfr(
            stage4d["current_recovery_atom_modulus_upper"]
        ) + _mpfr(stage4d["voltage_history_density_total_variation_upper"])
        f_difference = _mpfr(stage4e["history_measure_difference_upper"])
        fq_error = _mpfr(stage4e["f_q_error_upper"])
        fq_lower = _mpfr(stage4e["f_q_modulus_lower"])
        fq_center_lower = _complex_point(
            complex(evaluator.diagnostic.fq), PRECISION_BITS
        ).lower_abs()
        center_f = exact_restricted_f + f_difference
        normalized_f_exact = exact_restricted_f / fq_lower
        normalized_f_difference = (
            f_difference / fq_lower
            + center_f * fq_error / (fq_lower * fq_center_lower)
        )

        xdot_error = _mpfr(uncertainty["xdot_error"])
        xdot_bound = _mpfr(uncertainty["xdot_bound"])
        speed = _mpfr(uncertainty["event_speed_lower"])
        ratio_exact = xdot_bound / speed
        ratio_error = (
            xdot_error / speed + xdot_bound * xdot_error / speed**2
        )
        q_error = _mpfr(uncertainty["qsection_error"])
        q_bound = _mpfr(uncertainty["u_bound"]) + q_error
        q_event_error = (1 + ratio_exact) * q_error + q_bound * ratio_error
        q_event_center = _mpfr(center["q_event_center_upper_binary64"])
        rank_one_error = (
            q_event_error * normalized_f_exact
            + (q_event_center + q_event_error) * normalized_f_difference
        )
        raw_ratio_error = ratio_error * _mpfr(
            center["terminal_raw_row_norm_upper_binary64"]
        )
        time_shift = _mpfr(support["combined_coordinate_shift_upper"])
        time_shift_error = _mpfr(TIME_LIPSCHITZ_CAP) * time_shift
        total = upward_sum(
            (
                center_upper,
                binary_guard,
                primitive,
                rank_one_error,
                raw_ratio_error,
                time_shift_error,
            ),
            PRECISION_BITS,
        )
        target = _mpfr(TARGET_RHO_TERM)
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundDown):
        slack = target - total
    if not total < target or slack <= 0:
        raise ArithmeticError("the Stage-4L terminal stable-row gate did not close")
    return {
        "precision_bits": PRECISION_BITS,
        "centre_common_row_upper": decimal_upper(center_upper),
        "independent_binary_bernstein_guard_upper": decimal_upper(binary_guard),
        "stage4i_primitive_event_measure_error_upper": decimal_upper(primitive),
        "exact_restricted_raw_f_measure_norm_upper": decimal_upper(
            exact_restricted_f
        ),
        "exact_normalized_restricted_f_norm_upper": decimal_upper(
            normalized_f_exact
        ),
        "normalized_f_center_vs_exact_difference_upper": decimal_upper(
            normalized_f_difference
        ),
        "event_ratio_exact_upper": decimal_upper(ratio_exact),
        "event_ratio_center_vs_exact_error_upper": decimal_upper(ratio_error),
        "q_event_center_vs_exact_error_upper": decimal_upper(q_event_error),
        "rank_one_normalization_and_event_error_upper": decimal_upper(
            rank_one_error
        ),
        "raw_terminal_event_ratio_error_upper": decimal_upper(raw_ratio_error),
        "true_period_and_delay_coordinate_shift_upper": decimal_upper(
            time_shift
        ),
        "time_shift_lipschitz_cap": lipschitz["registered_lipschitz_cap"],
        "true_T_plus_and_coordinate_shift_error_upper": decimal_upper(
            time_shift_error
        ),
        "phase_fixed_terminal_stable_row_norm_upper": decimal_upper(total),
        "target_rho_term": TARGET_RHO_TERM,
        "strict_slack_to_target_lower": decimal_lower(slack),
        "strict_target_inequality_validated": True,
        "all_terms_nonnegative_and_summed_outward": True,
        "stage4i_error_used_only_as_raw_primitive_image": True,
        "stage4j_projected_residual_used": False,
        "unknown_terminal_norm_used_in_own_error": False,
        "unknown_k_s_used_in_own_error": False,
        "binary_rounding_certificate_bound": binary[
            "ieee_gamma_ledger_is_the_rounding_proof"
        ],
    }


def build_stage4l_artifact(repository: Path) -> Stage4LArtifact:
    _require_runtime()
    repository = repository.resolve()
    parents = _parent_payloads(repository)
    evaluator = _TerminalCentreEvaluator(repository)
    uncertainty = _model_uncertainty(evaluator.diagnostic.data)
    center = _common_center_certificate(evaluator)
    binary = _binary_rounding_certificate(center)
    support = _true_period_and_word_support(evaluator, uncertainty)
    lipschitz = _time_lipschitz_certificate(
        evaluator, parents, uncertainty, center
    )
    ledger = _directed_error_ledger(
        evaluator,
        parents,
        uncertainty,
        center,
        support,
        binary,
        lipschitz,
    )
    return Stage4LArtifact(
        schema_id=SCHEMA_ID,
        model_id=MODEL_ID,
        branch=BRANCH,
        status=STATUS,
        parent_result_sha256=dict(PARENT_HASHES),
        analytic_discrete_lemma={
            "section": "Sigma_0={h in Y:h_v(0)=0}",
            "selected_linear_map": "A=Pi_T U(T,0)|_{Sigma_0}",
            "event_operator": (
                "Pi_T y=y-Xdot_T*ell_0(y)/Xdot_v(T)"
            ),
            "right_column": "q=q^Sigma",
            "normalized_left_row": "f=f_0/f_0(q^Sigma)",
            "stable_projection": "P_s=I-q f",
            "stable_space": "E_s=ker(f) subset Sigma_0",
            "exact_eigen_relations": [
                "Aq=mu_u q",
                "fA=mu_u f",
                "f(q)=1",
            ],
            "exact_intertwining_relations": [
                "AP_s=P_sA=P_sAP_s",
                "AP_s(Sigma_0) subset E_s",
                "A_s=A|_{E_s}",
            ],
            "intertwining_is_analytic_not_a_numeric_residual": True,
            "no_additional_left_projection_needed": True,
            "selected_map_is_not_claimed_first_positive_return": True,
        },
        true_period_and_word_support=support,
        terminal_grid_and_common_row={
            "input_history_space": (
                "Y=C([-5*sqrt(5),0],R) x R with max norm"
            ),
            "input_tangent_section": "Sigma_0={h:h_v(0)=0}",
            "output_norm": (
                "maximum of complete returned voltage-history sup norm "
                "and current recovery modulus"
            ),
            "common_row": "R_theta Pi_T U(T,0)(I-q f)",
            "formation_order": [
                "form raw U(T,0) minus U(T,0)q f coefficientwise",
                "apply the same terminal event row coefficientwise",
                "remove the section-null current-voltage delta_0 atom",
                "take atom modulus and density total variation",
            ],
            "double_rank_one_formed_before_every_modulus": True,
            "terminal_event_correction_included": True,
            "current_voltage_atom_removed_by_exact_section_quotient": True,
            "current_recovery_atom_retained": True,
            "returned_output_cell_count": center[
                "returned_output_cell_count"
            ],
            "input_history_cell_count": center[
                "input_history_cell_count"
            ],
            "activation_ambiguous_rectangle_count": center[
                "activation_ambiguous_rectangle_count"
            ],
            "every_activation_ambiguous_rectangle_hulls_absent_and_present": True,
            "finite_node_maximum_used": False,
            "gaussian_quadrature_used": False,
            "continuous_output_phase_supremum": True,
            "outward_absolute_density_integration": True,
            "binary_rounding_certificate": binary,
            "true_coordinate_lipschitz_certificate": lipschitz,
        },
        directed_common_center=dict(center),
        directed_error_ledger=ledger,
        stable_power_certificate={
            "one_step_formula": "||A P_s||_{Sigma_0->Y}<=rho_term",
            "one_step_norm_upper": ledger[
                "phase_fixed_terminal_stable_row_norm_upper"
            ],
            "registered_stable_rate_upper": LP_RATE_UPPER,
            "one_step_upper_at_most_registered_rate": True,
            "power_formula": "||A_s^n||_{E_s->Y}<=rho_term^n<=0.1^n",
            "stable_power_constant_upper": "1",
            "k_s_equals_one_validated": True,
            "output_belongs_to_E_s_by_exact_intertwining": True,
            "numerical_left_projection_applied": False,
            "inherited_Y_norm_used_on_E_s": True,
        },
        scope_boundary={
            "proved_object": (
                "selected near-one-period phase-fixed discrete linear stable "
                "operator only"
            ),
            "stage4i_bypass_of_stage4j_is_noncircular": True,
            "first_positive_return": False,
            "no_earlier_section_hit": False,
            "nonlinear_return_tube": False,
            "split_return_ball": False,
            "uniform_hessian_blocks": False,
            "stable_graph": False,
            "pulse_graph_intersection": False,
            "crossing": False,
            "onset": False,
            "two_sided_routing": False,
            "network_safety": False,
        },
        claim_status={
            **{name: True for name in TRUE_FLAGS},
            **{name: False for name in FALSE_FLAGS},
        },
    )


def build_stage4l_result(repository: Path) -> dict[str, Any]:
    repository = repository.resolve()
    artifact = _json_roundtrip(asdict(build_stage4l_artifact(repository)))
    sources = {
        relative: _sha256_path(repository / relative)
        for relative in SOURCE_MANIFEST
    }
    return {
        "artifact": artifact,
        "manifest": {
            "schema_id": SCHEMA_ID,
            "result": RESULT_RELATIVE_PATH,
            "default_command": DEFAULT_COMMAND,
            "arithmetic_scope": ARITHMETIC_SCOPE,
            "proof_status": STATUS,
            "artifact_sha256": canonical_sha256(artifact),
            "source_sha256": sources,
            "parent_result_sha256": dict(PARENT_HASHES),
            "runtime": _runtime_record(),
        },
    }


def _validate_stage4l_semantics(artifact: Mapping[str, Any]) -> None:
    claims = _mapping(artifact.get("claim_status"), "Stage-4L claims")
    if set(claims) != set(TRUE_FLAGS) | set(FALSE_FLAGS):
        raise ValueError("the Stage-4L claim ledger changed")
    if any(claims.get(name) is not True for name in TRUE_FLAGS):
        raise ValueError("a proved Stage-4L linear ingress was demoted")
    if any(claims.get(name) is not False for name in FALSE_FLAGS):
        raise ValueError("a Stage-4L nonlinear or first-return claim was promoted")

    lemma = _mapping(
        artifact.get("analytic_discrete_lemma"), "Stage-4L discrete lemma"
    )
    if (
        lemma.get("section") != "Sigma_0={h in Y:h_v(0)=0}"
        or lemma.get("selected_linear_map")
        != "A=Pi_T U(T,0)|_{Sigma_0}"
        or lemma.get("event_operator")
        != "Pi_T y=y-Xdot_T*ell_0(y)/Xdot_v(T)"
        or lemma.get("right_column") != "q=q^Sigma"
        or lemma.get("normalized_left_row")
        != "f=f_0/f_0(q^Sigma)"
        or lemma.get("stable_projection") != "P_s=I-q f"
        or lemma.get("stable_space") != "E_s=ker(f) subset Sigma_0"
        or lemma.get("exact_eigen_relations")
        != ["Aq=mu_u q", "fA=mu_u f", "f(q)=1"]
        or lemma.get("exact_intertwining_relations")
        != [
            "AP_s=P_sA=P_sAP_s",
            "AP_s(Sigma_0) subset E_s",
            "A_s=A|_{E_s}",
        ]
        or lemma.get("intertwining_is_analytic_not_a_numeric_residual")
        is not True
        or lemma.get("no_additional_left_projection_needed") is not True
        or lemma.get("selected_map_is_not_claimed_first_positive_return")
        is not True
    ):
        raise ValueError("the Stage-4L analytic intertwining changed")

    support = _mapping(
        artifact.get("true_period_and_word_support"),
        "Stage-4L true-period support",
    )
    if support.get("exact_active_words") != [
        "empty",
        "(0)",
        "(1)",
        "(0,0)",
    ]:
        raise ValueError("the Stage-4L four-word support changed")
    for name in (
        "parent_delay_intervals_contain_exact_algebraic_delays",
        "T_minus_tau_max_strictly_positive",
        "T_minus_two_tau0_strictly_positive",
        "T_strictly_less_than_tau0_plus_tau1",
        "T_strictly_less_than_three_tau0",
        "returned_history_has_no_unadvanced_identity_block",
        "centre_period_is_not_claimed_exact",
        "activation_padding_strictly_contains_true_displacement",
        "centre_grid_extended_to_true_T_plus_by_lipschitz_remainder",
        "complete_true_returned_history_covered",
    ):
        if support.get(name) is not True:
            raise ValueError(f"the Stage-4L support gate changed: {name}")

    row = _mapping(
        artifact.get("terminal_grid_and_common_row"),
        "Stage-4L common row",
    )
    if row.get("common_row") != "R_theta Pi_T U(T,0)(I-q f)" or row.get(
        "formation_order"
    ) != [
        "form raw U(T,0) minus U(T,0)q f coefficientwise",
        "apply the same terminal event row coefficientwise",
        "remove the section-null current-voltage delta_0 atom",
        "take atom modulus and density total variation",
    ]:
        raise ValueError("the Stage-4L common-row formation order changed")
    for name in (
        "double_rank_one_formed_before_every_modulus",
        "terminal_event_correction_included",
        "current_voltage_atom_removed_by_exact_section_quotient",
        "current_recovery_atom_retained",
        "every_activation_ambiguous_rectangle_hulls_absent_and_present",
        "continuous_output_phase_supremum",
        "outward_absolute_density_integration",
    ):
        if row.get(name) is not True:
            raise ValueError(f"the Stage-4L common-row gate changed: {name}")
    if row.get("finite_node_maximum_used") is not False or row.get(
        "gaussian_quadrature_used"
    ) is not False:
        raise ValueError("a sampled Stage-4L norm was promoted")
    center_audit = _mapping(
        artifact.get("directed_common_center"), "Stage-4L directed center"
    )
    binary = _mapping(
        row.get("binary_rounding_certificate"),
        "Stage-4L binary rounding certificate",
    )
    operation_derivation = _mapping(
        binary.get("operation_count_derivation"),
        "Stage-4L binary operation derivation",
    )
    for name in (
        "local_guard_strictly_exceeds_gamma_n",
        "final_guard_strictly_exceeds_unguarded_error",
        "numpy_nextafter_is_not_the_rounding_proof",
        "ieee_gamma_ledger_is_the_rounding_proof",
        "derived_operation_count_at_most_registered_maximum",
        "all_ballpoly_and_bivariate_arrays_audited",
        "actual_intermediate_envelope_strictly_below_analytic_cap",
    ):
        if binary.get(name) is not True:
            raise ValueError("the Stage-4L binary64 proof was weakened")
    if (
        binary.get("binary64_unit_roundoff_exact")
        != BINARY64_UNIT_ROUNDOFF
        or binary.get("maximum_real_operations_per_guarded_kernel")
        != MAX_GUARDED_REAL_OPERATIONS
        or binary.get("analytic_binary_kernel_envelope_cap")
        != BINARY_KERNEL_ENVELOPE_CAP
        or binary.get("independent_final_binary_bernstein_guard")
        != CENTER_BINARY_BERNSTEIN_GUARD
        or dict(operation_derivation) != _binary_operation_components()
        or binary.get("derived_worst_case_real_operation_count")
        != sum(operation_derivation.values())
        or binary.get("derived_worst_case_real_operation_count")
        > MAX_GUARDED_REAL_OPERATIONS
        or _mpfr(
            binary.get(
                "actual_all_intermediate_ball_envelope_upper_binary64"
            )
        )
        >= _mpfr(BINARY_KERNEL_ENVELOPE_CAP)
        or binary.get("audited_ball_array_count")
        != center_audit.get("audited_ball_array_count")
        or binary.get("audited_scalar_coefficient_count")
        != center_audit.get("audited_scalar_coefficient_count")
    ):
        raise ValueError("the Stage-4L binary64 ledger constants changed")
    lipschitz = _mapping(
        row.get("true_coordinate_lipschitz_certificate"),
        "Stage-4L time-shift certificate",
    )
    if (
        lipschitz.get("candidate_strictly_below_registered_cap") is not True
        or lipschitz.get("unknown_stable_norm_used_in_derivation") is not False
        or lipschitz.get("unknown_k_s_used_in_derivation") is not False
        or lipschitz.get("self_referential_error_propagation_used") is not False
    ):
        raise ValueError("the Stage-4L time-shift proof became circular")

    center = center_audit
    if (
        _mpfr(center.get("center_common_row_upper_binary64_with_local_ball_guards"))
        >= _mpfr("0.005")
        or center.get("returned_output_cell_count") != 641
        or center.get("input_history_cell_count") != 640
        or center.get("bernstein_rectangle_count_including_recovery")
        != 410880
        or center.get("finite_node_maximum_used") is not False
        or center.get("gaussian_quadrature_used") is not False
    ):
        raise ValueError("the Stage-4L continuous center changed")

    ledger = _mapping(
        artifact.get("directed_error_ledger"), "Stage-4L error ledger"
    )
    if (
        _mpfr(ledger.get("phase_fixed_terminal_stable_row_norm_upper"))
        >= _mpfr(TARGET_RHO_TERM)
        or ledger.get("target_rho_term") != TARGET_RHO_TERM
        or ledger.get("strict_target_inequality_validated") is not True
        or ledger.get("all_terms_nonnegative_and_summed_outward") is not True
        or ledger.get("stage4i_error_used_only_as_raw_primitive_image")
        is not True
        or ledger.get("stage4j_projected_residual_used") is not False
        or ledger.get("unknown_terminal_norm_used_in_own_error") is not False
        or ledger.get("unknown_k_s_used_in_own_error") is not False
    ):
        raise ValueError("the Stage-4L directed error gate changed")

    power = _mapping(
        artifact.get("stable_power_certificate"),
        "Stage-4L stable-power certificate",
    )
    if (
        power.get("registered_stable_rate_upper") != LP_RATE_UPPER
        or power.get("stable_power_constant_upper") != "1"
        or power.get("k_s_equals_one_validated") is not True
        or power.get("output_belongs_to_E_s_by_exact_intertwining") is not True
        or power.get("numerical_left_projection_applied") is not False
        or power.get("inherited_Y_norm_used_on_E_s") is not True
    ):
        raise ValueError("the Stage-4L K_s=1 consequence changed")
    scope = _mapping(
        artifact.get("scope_boundary"), "Stage-4L scope boundary"
    )
    for name in (
        "first_positive_return",
        "no_earlier_section_hit",
        "nonlinear_return_tube",
        "split_return_ball",
        "uniform_hessian_blocks",
        "stable_graph",
        "pulse_graph_intersection",
        "crossing",
        "onset",
        "two_sided_routing",
        "network_safety",
    ):
        if scope.get(name) is not False:
            raise ValueError(f"the Stage-4L scope was promoted: {name}")


def validate_stage4l_result(
    payload: Mapping[str, Any], repository: Path, *, recompute: bool = True
) -> None:
    _require_runtime()
    if not isinstance(payload, Mapping) or set(payload) != {"artifact", "manifest"}:
        raise ValueError("the Stage-4L result has the wrong outer schema")
    artifact = _mapping(payload.get("artifact"), "Stage-4L artifact")
    manifest = _mapping(payload.get("manifest"), "Stage-4L manifest")
    if set(artifact) != {field.name for field in fields(Stage4LArtifact)}:
        raise ValueError("the Stage-4L artifact schema changed")
    if (
        artifact.get("schema_id") != SCHEMA_ID
        or artifact.get("model_id") != MODEL_ID
        or artifact.get("branch") != BRANCH
        or artifact.get("status") != STATUS
        or artifact.get("parent_result_sha256") != PARENT_HASHES
    ):
        raise ValueError("the Stage-4L identity changed")
    _validate_stage4l_semantics(artifact)

    expected_manifest = {
        "schema_id",
        "result",
        "default_command",
        "arithmetic_scope",
        "proof_status",
        "artifact_sha256",
        "source_sha256",
        "parent_result_sha256",
        "runtime",
    }
    if set(manifest) != expected_manifest:
        raise ValueError("the Stage-4L manifest schema changed")
    fixed = {
        "schema_id": SCHEMA_ID,
        "result": RESULT_RELATIVE_PATH,
        "default_command": DEFAULT_COMMAND,
        "arithmetic_scope": ARITHMETIC_SCOPE,
        "proof_status": STATUS,
        "artifact_sha256": canonical_sha256(artifact),
        "parent_result_sha256": dict(PARENT_HASHES),
        "runtime": _runtime_record(),
    }
    if any(manifest.get(name) != value for name, value in fixed.items()):
        raise ValueError("the Stage-4L manifest fixed data changed")
    repository = repository.resolve()
    sources = _mapping(manifest.get("source_sha256"), "Stage-4L sources")
    if set(sources) != set(SOURCE_MANIFEST):
        raise ValueError("the Stage-4L source manifest changed")
    for relative in SOURCE_MANIFEST:
        if sources.get(relative) != _sha256_path(repository / relative):
            raise ValueError(f"the Stage-4L source changed: {relative}")
    _parent_payloads(repository)
    if recompute:
        expected = _json_roundtrip(asdict(build_stage4l_artifact(repository)))
        if dict(artifact) != expected:
            raise ValueError("the Stage-4L artifact differs from a fresh replay")


__all__ = [
    "ARITHMETIC_SCOPE",
    "BRANCH",
    "DEFAULT_COMMAND",
    "FALSE_FLAGS",
    "GENERATOR_RELATIVE_PATH",
    "LP_RATE_UPPER",
    "NOTE_RELATIVE_PATH",
    "RESULT_RELATIVE_PATH",
    "SCHEMA_ID",
    "SOURCE_MANIFEST",
    "SOURCE_RELATIVE_PATH",
    "STATUS",
    "TARGET_RHO_TERM",
    "TEST_RELATIVE_PATH",
    "TRUE_FLAGS",
    "build_stage4l_artifact",
    "build_stage4l_result",
    "canonical_sha256",
    "validate_stage4l_result",
]
