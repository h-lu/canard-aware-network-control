"""One rigorously isolated positive Floquet exponent of the inner orbit.

The source-validated inner periodic orbit and the leaky Floquet--Riesz
theorem leave a finite analytic characteristic problem after an invertible
Fourier tail has been removed.  This module performs a one-dimensional
Grushin reduction near the numerically observed positive exponent.  Its
border is made from cutoff-64 binary64 singular vectors, but every use of
that border is subsequently validated against the complete Fourier
operator, the full orbit correction ball, and the infinite tail.

The scalar effective Hamiltonian is compared with one nonzero affine
function on a symmetric complex circle.  Rouché's theorem then proves one
characteristic value in that disk, counted with analytic algebraic
multiplicity.  Real conjugacy makes the unique value real, and the disk lies
strictly in the open right half-plane.

This is only a local center-orbit theorem.  It neither excludes other roots
in the remaining principal logarithmic strip nor proves the total unstable
index, a common parameter-box result, a stable manifold, or pulse onset.
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
import subprocess
import sys
from typing import Any, Iterable, Mapping

import gmpy2
import numpy as np
import scipy

from canard_control.directed_interval import (
    DirectedComplexInterval,
    DirectedInterval,
    complex_unit_interval,
    cos_interval,
    decimal_lower,
    decimal_upper,
    pi_interval,
    sin_interval,
    upward_sum,
)
from canard_control.fhn_periodic_infinite_validation import (
    _sequence_box_norm_upper,
)
from canard_control.floquet_cover_arithmetic import (
    _binary_environment_checked,
    _binary_coefficients,
    _binary_complex_matrix_split_l1_upper,
    _binary_complex_product_split_l1_upper,
    _box_distance_split_upper,
    _coefficient_matrix,
    _formation_error,
)
from canard_control.leaky_floquet_riesz_reduction import (
    RESULT_RELATIVE_PATH as RIESZ_RESULT_RELATIVE_PATH,
    validate_leaky_floquet_riesz_result,
)
from canard_control.leaky_floquet_transfer import (
    RESULT_RELATIVE_PATH as FLOQUET_TRANSFER_RESULT_RELATIVE_PATH,
    load_validated_leaky_orbit_evidence,
)
from canard_control.leaky_periodic_validation import (
    _build_leaky_base_sequences,
)


SCHEMA_ID = "leaky-floquet-inner-unstable-root-v3"
MODEL_ID = "autonomous-leaky-recovery-two-delay-fhn-bistable-proposal"
BRANCH = "inner_saddle_candidate"
SOURCE_RELATIVE_PATH = (
    "src/canard_control/leaky_floquet_inner_unstable_root.py"
)
GENERATOR_RELATIVE_PATH = (
    "experiments/leaky_floquet_inner_unstable_root.py"
)
NOTE_RELATIVE_PATH = "docs/leaky-floquet-inner-unstable-root.md"
TEST_RELATIVE_PATH = "tests/test_leaky_floquet_inner_unstable_root.py"
RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_floquet_inner_unstable_root.json"
)
DEFAULT_COMMAND = (
    "OPENBLAS_NUM_THREADS=8 PYTHONPATH=build/testdeps:src /usr/bin/python3 "
    "experiments/leaky_floquet_inner_unstable_root.py"
)
ARITHMETIC_SCOPE = (
    "160-bit outward MPFR bounds around exact stored binary64 Fourier data; "
    "four-real-GEMM inverse/product error bounds; full inner orbit correction "
    "ball, physical unshifted-coefficient/output-phase delay pencil, a "
    "shifted-coefficient/input-phase equivalence oracle, delay exponent "
    "remainders, and infinite Fourier tail; one local characteristic value only"
)
SOURCE_MANIFEST = (
    SOURCE_RELATIVE_PATH,
    GENERATOR_RELATIVE_PATH,
    NOTE_RELATIVE_PATH,
    "src/canard_control/directed_interval.py",
    "src/canard_control/fhn_periodic_infinite_validation.py",
    "src/canard_control/floquet_cover_arithmetic.py",
    "src/canard_control/leaky_floquet_riesz_reduction.py",
    "src/canard_control/leaky_floquet_transfer.py",
    "src/canard_control/leaky_periodic_validation.py",
)

PRECISION_BITS = 160
FOURIER_CUTOFF = 64
ROOT_DISK_RADIUS = "0.1"
ROOT_CENTER_BINARY64 = 0.6983604129095
BOUNDARY_ARC_COUNT = 256
RIGHT_BORDER_SCALE = 20.0
LEFT_BORDER_SCALE = 5.0
NESTED_ORBIT_RADIUS = "1e-12"
PINNED_OPENBLAS_NUM_THREADS = "8"

TRUE_FLAGS = (
    "source_validated_inner_orbit_ball_used",
    "source_validated_riesz_tail_and_multiplicity_reduction_used",
    "complex_modulus_wiener_grushin_norm_used",
    "physical_delay_dual_representation_oracle_validated",
    "unshifted_coefficient_output_phase_pencil_used",
    "orbit_period_phase_variation_uses_output_modes",
    "tail_output_frequency_cancellation_validated",
    "cutoff64_left_right_singular_vectors_used_only_as_borders",
    "full_infinite_dimensional_grushin_operator_invertible_on_closed_disk",
    "scalar_effective_hamiltonian_rouche_count_validated",
    "exactly_one_characteristic_value_in_root_disk",
    "root_analytic_algebraic_multiplicity_one",
    "unique_disk_root_real_by_conjugacy",
    "root_strictly_positive",
    "associated_multiplier_strictly_greater_than_one",
)

FALSE_FLAGS = (
    "finite_svd_root_promoted_without_full_operator_validation",
    "remaining_compact_keyhole_zero_free_validated",
    "inner_no_other_right_half_roots_validated",
    "inner_total_unstable_multiplier_count_validated",
    "inner_saddle_floquet_index_validated",
    "common_parameter_box_root_validated",
    "inner_stable_manifold_validated",
    "physical_pulse_onset_validated",
)


@dataclass(frozen=True)
class BoundaryWorstCell:
    index: int
    center_real_binary64: str
    center_imag_binary64: str
    arc_radius_upper: str
    finite_bordered_inverse_norm_upper: str
    finite_bordered_inverse_defect_upper: str
    full_grushin_contraction_upper: str
    bottom_row_defect_upper: str
    local_affine_comparison_error_upper: str


@dataclass(frozen=True)
class LeakyInnerUnstableRootCertificate:
    schema_id: str
    model_id: str
    branch: str
    riesz_result_sha256: str
    inner_orbit_result: str
    inner_orbit_result_sha256: str
    candidate_fingerprint: str
    source_correction_radius: str
    nested_correction_radius: str
    nested_radii_contraction_upper: str
    nested_radii_margin_lower: str
    precision_bits: int
    binary_blas_thread_count: int
    norm_id: str
    fourier_cutoff: int
    coefficient_support_half_bandwidth: int
    finite_block_maximum_delay_output_mode: int
    finite_tail_maximum_delay_output_mode: int
    tail_finite_maximum_delay_output_mode: int
    complex_finite_dimension: int
    grushin_finite_dimension: int
    root_disk_center_binary64: str
    root_disk_center_hex: str
    root_disk_radius: str
    root_disk_real_part_lower: str
    root_disk_real_part_upper: str
    multiplier_modulus_lower: str
    multiplier_modulus_upper: str
    boundary_arc_count: int
    unshifted_row_oracle_error_binary64: str
    shifted_column_oracle_error_binary64: str
    unshifted_column_mutation_separation_binary64: str
    shifted_row_mutation_separation_binary64: str
    directed_equivalent_entry_count: int
    directed_equivalent_entry_total: int
    directed_unshifted_column_mutation_separation_lower: str
    directed_shifted_row_mutation_separation_lower: str
    right_border_scale: str
    left_border_scale: str
    right_border_sha256: str
    left_border_sha256: str
    center_finite_smallest_singular_value_binary64: str
    center_finite_second_smallest_singular_value_binary64: str
    center_grushin_inverse_norm_upper: str
    center_grushin_inverse_defect_upper: str
    closed_disk_full_grushin_contraction_upper: str
    closed_disk_full_grushin_margin_lower: str
    reference_effective_slope_real_binary64: str
    reference_effective_slope_imag_binary64: str
    reference_effective_slope_modulus_lower: str
    affine_boundary_modulus_lower: str
    maximum_boundary_comparison_error_upper: str
    rouche_margin_lower: str
    allowable_additional_pencil_perturbation_upper: str
    continuation_interface_scope: str
    boundary_partition_sha256: str
    worst_boundary_cell: BoundaryWorstCell
    source_validated_inner_orbit_ball_used: bool
    source_validated_riesz_tail_and_multiplicity_reduction_used: bool
    complex_modulus_wiener_grushin_norm_used: bool
    physical_delay_dual_representation_oracle_validated: bool
    unshifted_coefficient_output_phase_pencil_used: bool
    orbit_period_phase_variation_uses_output_modes: bool
    tail_output_frequency_cancellation_validated: bool
    cutoff64_left_right_singular_vectors_used_only_as_borders: bool
    full_infinite_dimensional_grushin_operator_invertible_on_closed_disk: bool
    scalar_effective_hamiltonian_rouche_count_validated: bool
    exactly_one_characteristic_value_in_root_disk: bool
    root_analytic_algebraic_multiplicity_one: bool
    unique_disk_root_real_by_conjugacy: bool
    root_strictly_positive: bool
    associated_multiplier_strictly_greater_than_one: bool
    finite_svd_root_promoted_without_full_operator_validation: bool
    remaining_compact_keyhole_zero_free_validated: bool
    inner_no_other_right_half_roots_validated: bool
    inner_total_unstable_multiplier_count_validated: bool
    inner_saddle_floquet_index_validated: bool
    common_parameter_box_root_validated: bool
    inner_stable_manifold_validated: bool
    physical_pulse_onset_validated: bool
    minimal_remaining_gate: str


@dataclass(frozen=True)
class _Prepared:
    orbit: Any
    evidence: Any
    base: Any
    riesz_branch: Mapping[str, Any]
    modes: np.ndarray
    tail_modes: np.ndarray
    current_finite: np.ndarray
    delayed_finite: np.ndarray
    current_finite_tail: np.ndarray
    delayed_finite_tail: np.ndarray
    current_tail_finite: np.ndarray
    delayed_tail_finite: np.ndarray
    current_binary_norm: gmpy2.mpfr
    delayed_binary_norm: gmpy2.mpfr
    current_center_error: gmpy2.mpfr
    delayed_center_error_sum: gmpy2.mpfr
    current_total_variation: gmpy2.mpfr
    delayed_total_variation: gmpy2.mpfr
    period_radius: gmpy2.mpfr
    nested_radii_contraction: gmpy2.mpfr
    nested_radii_margin: gmpy2.mpfr
    center_matrix: np.ndarray
    center_first: np.ndarray
    center_second: np.ndarray
    center_finite_tail: np.ndarray
    center_finite_tail_first: np.ndarray
    center_tail_finite: np.ndarray
    center_errors: Mapping[str, gmpy2.mpfr]
    right_border: np.ndarray
    left_border: np.ndarray
    finite_grushin: np.ndarray
    finite_grushin_inverse: np.ndarray
    center_singular_values: np.ndarray


@dataclass(frozen=True)
class _CellData:
    summary: Mapping[str, str | int]
    comparison: gmpy2.mpfr
    contraction: gmpy2.mpfr
    inverse_norm: gmpy2.mpfr
    bottom_row_norm: gmpy2.mpfr
    scalar_column_norm: gmpy2.mpfr


def _mapping(value: object, label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{label} must be a mapping")
    return value


def _sha256_path(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def canonical_sha256(value: Any) -> str:
    return sha256(
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        ).encode("ascii")
    ).hexdigest()


def _require_pinned_binary_blas_environment() -> None:
    """Pin the discovery SVD/inverses to the artifact's BLAS schedule.

    The rigorous MPFR bounds validate whichever stored binary64 border is
    produced, but a nearly singular SVD is not bitwise invariant under an
    OpenBLAS thread-count change.  Exact artifact replay therefore requires
    the same schedule that is declared by ``DEFAULT_COMMAND``.
    """

    if os.environ.get("OPENBLAS_NUM_THREADS") != PINNED_OPENBLAS_NUM_THREADS:
        raise RuntimeError(
            "the inner-root binary replay requires "
            f"OPENBLAS_NUM_THREADS={PINNED_OPENBLAS_NUM_THREADS}"
        )


def _build_result_in_pinned_binary_blas_subprocess(
    repository: Path,
) -> dict[str, Any]:
    """Replay in a fresh process before NumPy loads OpenBLAS."""

    environment = dict(os.environ)
    environment["OPENBLAS_NUM_THREADS"] = PINNED_OPENBLAS_NUM_THREADS
    source_path = str(repository / "src")
    inherited_pythonpath = environment.get("PYTHONPATH", "")
    environment["PYTHONPATH"] = (
        source_path
        if not inherited_pythonpath
        else source_path + os.pathsep + inherited_pythonpath
    )
    program = (
        "import json,sys; from pathlib import Path; "
        "from canard_control.leaky_floquet_inner_unstable_root import "
        "build_leaky_inner_unstable_root_result; "
        "print(json.dumps(build_leaky_inner_unstable_root_result("
        "Path(sys.argv[1])),sort_keys=True,separators=(',',':'),"
        "allow_nan=False))"
    )
    completed = subprocess.run(
        [sys.executable, "-c", program, str(repository)],
        cwd=repository,
        env=environment,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            "the pinned inner-root replay subprocess failed: "
            + completed.stderr.strip()
        )
    value = json.loads(completed.stdout)
    if not isinstance(value, dict):
        raise RuntimeError("the pinned inner-root replay returned no result")
    return value


def _dependency_fingerprint(repository: Path) -> str:
    """Hash every mutable input used behind the numerical replay cache."""

    repository = repository.resolve()
    riesz_path = repository / RIESZ_RESULT_RELATIVE_PATH
    riesz_payload = _mapping(json.loads(riesz_path.read_text()), "Riesz cache key")
    artifact = _mapping(riesz_payload.get("artifact"), "Riesz cache artifact")
    branches = _mapping(artifact.get("branches"), "Riesz cache branches")
    branch = _mapping(branches.get(BRANCH), "Riesz cache inner branch")
    orbit_relative = branch.get("source_result")
    if not isinstance(orbit_relative, str) or not orbit_relative:
        raise ValueError("the Riesz cache key has no inner orbit source")
    orbit_path = (repository / orbit_relative).resolve()
    try:
        orbit_path.relative_to(repository)
    except ValueError as error:
        raise ValueError("the Riesz orbit cache key escaped the repository") from error
    return canonical_sha256(
        {
            "sources": {
                relative: _sha256_path(repository / relative)
                for relative in SOURCE_MANIFEST
            },
            "results": {
                RIESZ_RESULT_RELATIVE_PATH: _sha256_path(riesz_path),
                FLOQUET_TRANSFER_RESULT_RELATIVE_PATH: _sha256_path(
                    repository / FLOQUET_TRANSFER_RESULT_RELATIVE_PATH
                ),
                orbit_relative: _sha256_path(orbit_path),
            },
        }
    )


def _up(value: object, precision: int = PRECISION_BITS) -> gmpy2.mpfr:
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        return gmpy2.mpfr(value)


def _down(value: object, precision: int = PRECISION_BITS) -> gmpy2.mpfr:
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        return gmpy2.mpfr(value)


def _split_upper(value: complex, precision: int) -> gmpy2.mpfr:
    real = DirectedInterval.from_float(abs(complex(value).real), precision).upper
    imag = DirectedInterval.from_float(abs(complex(value).imag), precision).upper
    return upward_sum((real, imag), precision)


def _complex_abs_upper(value: complex, precision: int) -> gmpy2.mpfr:
    real = DirectedInterval.from_float(complex(value).real, precision)
    imag = DirectedInterval.from_float(complex(value).imag, precision)
    return DirectedComplexInterval(real, imag).upper_abs()


def _complex_abs_lower(value: complex, precision: int) -> gmpy2.mpfr:
    real = DirectedInterval.from_float(complex(value).real, precision)
    imag = DirectedInterval.from_float(complex(value).imag, precision)
    return DirectedComplexInterval(real, imag).lower_abs()


def _vector_l1_upper(vector: np.ndarray, precision: int) -> gmpy2.mpfr:
    return _binary_complex_matrix_split_l1_upper(
        np.asarray(vector, dtype=complex).reshape(-1, 1), precision
    )


def _row_dual_upper(row: np.ndarray, precision: int) -> gmpy2.mpfr:
    values = np.asarray(row, dtype=complex).reshape(-1)
    return max((_split_upper(value, precision) for value in values), default=_up(0))


def _matrix_max_entry_upper(matrix: np.ndarray, precision: int) -> gmpy2.mpfr:
    values = np.asarray(matrix, dtype=complex).reshape(-1)
    return max((_split_upper(value, precision) for value in values), default=_up(0))


def _exp_interval(value: DirectedInterval) -> DirectedInterval:
    with gmpy2.context(precision=value.precision, round=gmpy2.RoundDown):
        lower = gmpy2.exp(value.lower)
    with gmpy2.context(precision=value.precision, round=gmpy2.RoundUp):
        upper = gmpy2.exp(value.upper)
    return DirectedInterval(lower, upper, value.precision)


def _rotation_arrays(
    modes: np.ndarray,
    s: complex,
    base: Any,
    precision: int,
) -> tuple[tuple[np.ndarray, np.ndarray], gmpy2.mpfr]:
    """Return binary rotations and their maximum split evaluation error."""

    sigma = DirectedInterval.from_float(float(s.real), precision)
    phase = DirectedInterval.from_float(float(s.imag), precision)
    arrays: list[np.ndarray] = []
    maximum_error = _up(0, precision)
    for tau in (base.parameters["tau_0"], base.parameters["tau_1"]):
        alpha_float = float(tau.lower) / float(base.period.lower)
        binary = np.exp(
            -(complex(float(s.real), float(s.imag)) + 2.0j * np.pi * modes)
            * alpha_float
        )
        arrays.append(np.asarray(binary, dtype=complex))
        alpha = tau / base.period
        amplitude = _exp_interval(-(sigma * alpha))
        for mode, stored in zip(modes, binary, strict=True):
            angle = -(
                (pi_interval(precision) * (2 * int(mode)) + phase) * alpha
            )
            exact = DirectedComplexInterval.from_real(amplitude) * (
                complex_unit_interval(angle)
            )
            maximum_error = max(
                maximum_error,
                _box_distance_split_upper(exact, complex(stored)),
            )
    return (arrays[0], arrays[1]), maximum_error


def physical_delay_convolution_oracle_error(*, representation: str) -> float:
    """Compare four Fourier formulas with the physical delayed product.

    If ``b`` is the unshifted coefficient, then

        b(t-alpha) y(t-alpha)

    is represented either by unshifted ``b`` with the delay phase on output
    mode ``k``, or by shifted ``b_alpha`` with the phase on input mode ``m``.
    Mixing an unshifted coefficient with column phase, or a shifted
    coefficient with row phase, is a different operator.  Rectangular blocks
    are included so the oracle also fixes both finite/tail coupling axes.
    """

    finite_modes = np.arange(-2, 3, dtype=int)
    tail_modes = np.asarray([-6, -5, 5, 6], dtype=int)
    unshifted = {
        mode: complex(0.013 * (mode + 9), -0.007 * (mode - 2))
        for mode in range(-8, 9)
    }
    alpha = 0.37
    s = 0.23 + 0.17j
    maximum = 0.0
    for output_modes, input_modes in (
        (finite_modes, finite_modes),
        (finite_modes, tail_modes),
        (tail_modes, finite_modes),
    ):
        input_rotation = np.exp(
            -(s + 2.0j * np.pi * input_modes) * alpha
        )
        output_rotation = np.exp(
            -(s + 2.0j * np.pi * output_modes) * alpha
        )
        shifted = {
            mode: value * np.exp(-2.0j * np.pi * mode * alpha)
            for mode, value in unshifted.items()
        }
        unshifted_matrix = _coefficient_matrix(
            output_modes, input_modes, unshifted
        )
        shifted_matrix = _coefficient_matrix(
            output_modes, input_modes, shifted
        )
        formulas = {
            "unshifted_row": output_rotation[:, None] * unshifted_matrix,
            "shifted_column": shifted_matrix * input_rotation[None, :],
            "unshifted_column": unshifted_matrix * input_rotation[None, :],
            "shifted_row": output_rotation[:, None] * shifted_matrix,
        }
        if representation not in formulas:
            raise ValueError("unknown physical delay oracle representation")
        tested = formulas[representation]
        direct = np.asarray(
            [
                [
                    unshifted.get(int(k - mode), 0.0)
                    * output_rotation[row]
                    for mode in input_modes
                ]
                for row, k in enumerate(output_modes)
            ],
            dtype=complex,
        )
        maximum = max(maximum, float(np.max(np.abs(tested - direct))))
    return maximum


def _directed_box_gap_lower(
    left: DirectedComplexInterval,
    right: DirectedComplexInterval,
) -> gmpy2.mpfr:
    precision = left.precision
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        real_gap = max(
            gmpy2.mpfr(0, precision),
            left.real.lower - right.real.upper,
            right.real.lower - left.real.upper,
        )
        imag_gap = max(
            gmpy2.mpfr(0, precision),
            left.imag.lower - right.imag.upper,
            right.imag.lower - left.imag.upper,
        )
        return max(real_gap, imag_gap)


def _directed_physical_delay_entry_oracle(
    precision: int = PRECISION_BITS,
) -> tuple[int, int, gmpy2.mpfr, gmpy2.mpfr]:
    """Directed entrywise oracle for the two equivalent delay formulas."""

    zero = DirectedInterval.from_decimal(0, precision)
    alpha = DirectedInterval.from_decimal("0.37", precision)
    sigma = DirectedInterval.from_decimal("0.23", precision)
    phase = DirectedInterval.from_decimal("0.17", precision)
    amplitude = DirectedComplexInterval.from_real(_exp_interval(-(sigma * alpha)))
    finite_modes = (-2, -1, 0, 1, 2)
    tail_modes = (-6, -5, 5, 6)
    coefficients = {
        mode: DirectedComplexInterval(
            DirectedInterval.from_decimal(
                format(0.013 * (mode + 9), ".17g"), precision
            ),
            DirectedInterval.from_decimal(
                format(-0.007 * (mode - 2), ".17g"), precision
            ),
        )
        for mode in range(-8, 9)
    }
    correct = 0
    total = 0
    unshifted_column_gap = gmpy2.mpfr(0, precision)
    shifted_row_gap = gmpy2.mpfr(0, precision)
    for outputs, inputs in (
        (finite_modes, finite_modes),
        (finite_modes, tail_modes),
        (tail_modes, finite_modes),
    ):
        for output_mode in outputs:
            row_phase = amplitude * complex_unit_interval(
                -(
                    phase
                    + pi_interval(precision) * (2 * output_mode)
                )
                * alpha
            )
            for input_mode in inputs:
                coefficient = coefficients.get(
                    output_mode - input_mode,
                    DirectedComplexInterval(zero, zero),
                )
                input_phase = amplitude * complex_unit_interval(
                    -(
                        phase
                        + pi_interval(precision) * (2 * input_mode)
                    )
                    * alpha
                )
                coefficient_phase = complex_unit_interval(
                    -pi_interval(precision)
                    * (2 * (output_mode - input_mode))
                    * alpha
                )
                physical_row = coefficient * row_phase
                physical_column = coefficient * coefficient_phase * input_phase
                total += 1
                if _directed_box_gap_lower(physical_row, physical_column) == 0:
                    correct += 1
                unshifted_column_gap = max(
                    unshifted_column_gap,
                    _directed_box_gap_lower(
                        physical_row, coefficient * input_phase
                    ),
                )
                shifted_row_gap = max(
                    shifted_row_gap,
                    _directed_box_gap_lower(
                        physical_row,
                        coefficient * coefficient_phase * row_phase,
                    ),
                )
    return correct, total, unshifted_column_gap, shifted_row_gap


def _validate_physical_delay_oracle() -> tuple[
    float,
    float,
    float,
    float,
    int,
    int,
    gmpy2.mpfr,
    gmpy2.mpfr,
]:
    unshifted_row = physical_delay_convolution_oracle_error(
        representation="unshifted_row"
    )
    shifted_column = physical_delay_convolution_oracle_error(
        representation="shifted_column"
    )
    unshifted_column = physical_delay_convolution_oracle_error(
        representation="unshifted_column"
    )
    shifted_row = physical_delay_convolution_oracle_error(
        representation="shifted_row"
    )
    if max(unshifted_row, shifted_column) > 5.0e-15:
        raise ArithmeticError("the two physical delay representations disagree")
    if min(unshifted_column, shifted_row) < 1.0e-3:
        raise ArithmeticError("a mixed coefficient/phase mutation was not detected")
    directed = _directed_physical_delay_entry_oracle()
    if directed[0] != directed[1]:
        raise ArithmeticError("the directed physical delay boxes do not overlap")
    if min(directed[2], directed[3]) <= 0:
        raise ArithmeticError("a directed mixed delay mutation was not detected")
    return (
        unshifted_row,
        shifted_column,
        unshifted_column,
        shifted_row,
        *directed,
    )


def _evaluate_blocks(
    prepared: _Prepared | None,
    *,
    orbit: Any,
    base: Any,
    modes: np.ndarray,
    tail_modes: np.ndarray,
    current_finite: np.ndarray,
    delayed_finite: np.ndarray,
    current_finite_tail: np.ndarray,
    delayed_finite_tail: np.ndarray,
    current_tail_finite: np.ndarray,
    delayed_tail_finite: np.ndarray,
    current_binary_norm: gmpy2.mpfr,
    delayed_binary_norm: gmpy2.mpfr,
    s: complex,
    precision: int,
) -> tuple[
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
    Mapping[str, gmpy2.mpfr],
]:
    """Evaluate the physical unshifted-coefficient/output-phase pencil."""

    del prepared
    period = float(orbit.period)
    epsilon = float(orbit.parameters.epsilon)
    rotations, rotation_error = _rotation_arrays(modes, s, base, precision)
    tail_rotations, tail_rotation_error = _rotation_arrays(
        tail_modes, s, base, precision
    )
    frequencies = complex(s) + 2.0j * np.pi * modes
    top = np.diag(frequencies) - period * current_finite
    first_top = np.eye(len(modes), dtype=complex)
    second_top = np.zeros_like(first_top)
    finite_tail_top = -period * current_finite_tail
    finite_tail_first_top = np.zeros_like(finite_tail_top)
    tail_finite_top = -period * current_tail_finite
    for tau, rotation, tail_rotation in zip(
        orbit.parameters.physical_delays,
        rotations,
        tail_rotations,
        strict=True,
    ):
        alpha = float(tau) / period
        rotated = rotation[:, None] * delayed_finite
        top -= period * rotated
        first_top += float(tau) * rotated
        second_top -= float(tau) * alpha * rotated
        finite_rotated = rotation[:, None] * delayed_finite_tail
        finite_tail_top -= period * finite_rotated
        finite_tail_first_top += float(tau) * finite_rotated
        tail_finite_top -= period * (
            tail_rotation[:, None] * delayed_tail_finite
        )

    identity = np.eye(len(modes), dtype=complex)
    zero = np.zeros_like(identity)
    finite = np.block(
        [
            [top, period * identity],
            [
                -period * epsilon * identity,
                np.diag(frequencies + period * epsilon),
            ],
        ]
    )
    first = np.block([[first_top, zero], [zero, identity]])
    second = np.block([[second_top, zero], [zero, zero]])
    finite_tail = np.hstack(
        (
            np.vstack((finite_tail_top, np.zeros_like(finite_tail_top))),
            np.zeros((2 * len(modes), len(tail_modes)), dtype=complex),
        )
    )
    finite_tail_first = np.hstack(
        (
            np.vstack(
                (
                    finite_tail_first_top,
                    np.zeros_like(finite_tail_first_top),
                )
            ),
            np.zeros((2 * len(modes), len(tail_modes)), dtype=complex),
        )
    )
    tail_finite = np.hstack(
        (
            np.vstack((tail_finite_top, np.zeros_like(tail_finite_top))),
            np.zeros((2 * len(tail_modes), len(modes)), dtype=complex),
        )
    )

    maximum_frequency = _up(0, precision)
    maximum_diagonal_error = _up(0, precision)
    sigma = DirectedInterval.from_float(float(s.real), precision)
    phase = DirectedInterval.from_float(float(s.imag), precision)
    for mode, stored in zip(modes, frequencies, strict=True):
        exact = DirectedComplexInterval(
            sigma, pi_interval(precision) * (2 * int(mode)) + phase
        )
        maximum_frequency = max(
            maximum_frequency,
            upward_sum(
                (exact.real.upper_abs(), exact.imag.upper_abs()), precision
            ),
        )
        maximum_diagonal_error = max(
            maximum_diagonal_error,
            _box_distance_split_upper(exact, complex(stored)),
        )

    tau_sum = upward_sum(
        (
            base.parameters["tau_0"].upper,
            base.parameters["tau_1"].upper,
        ),
        precision,
    )
    tau_square_over_period_sum = upward_sum(
        tuple(
            (tau.upper * tau.upper / base.period.lower)
            for tau in (
                base.parameters["tau_0"],
                base.parameters["tau_1"],
            )
        ),
        precision,
    )
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        finite_scale = max(
            maximum_frequency
            + base.period.upper
            * (current_binary_norm + 2 * delayed_binary_norm)
            + base.period.upper,
            maximum_frequency
            + 2 * base.period.upper * base.parameters["epsilon"].upper,
        )
        first_scale = max(
            1 + tau_sum * delayed_binary_norm,
            gmpy2.mpfr(1, precision),
        )
        second_scale = tau_square_over_period_sum * delayed_binary_norm
        convolution_scale = base.period.upper * (
            current_binary_norm + 2 * delayed_binary_norm
        )
        first_convolution_scale = tau_sum * delayed_binary_norm
        finite_error = (
            maximum_diagonal_error
            + 2 * base.period.upper * rotation_error * delayed_binary_norm
            + _formation_error(finite_scale, 2 * len(modes), precision)
        )
        first_error = (
            tau_sum * rotation_error * delayed_binary_norm
            + _formation_error(first_scale, 2 * len(modes), precision)
        )
        second_error = (
            tau_square_over_period_sum
            * rotation_error
            * delayed_binary_norm
            + _formation_error(second_scale, 2 * len(modes), precision)
        )
        finite_tail_error = (
            2
            * base.period.upper
            * rotation_error
            * delayed_binary_norm
            + _formation_error(
                convolution_scale, 2 * len(modes), precision
            )
        )
        finite_tail_first_error = (
            tau_sum * rotation_error * delayed_binary_norm
            + _formation_error(
                first_convolution_scale, 2 * len(modes), precision
            )
        )
        tail_finite_error = (
            2
            * base.period.upper
            * tail_rotation_error
            * delayed_binary_norm
            + _formation_error(
                convolution_scale, 2 * len(tail_modes), precision
            )
        )
    return (
        finite,
        first,
        second,
        finite_tail,
        finite_tail_first,
        tail_finite,
        {
            "finite": finite_error,
            "first": first_error,
            "second": second_error,
            "finite_tail": finite_tail_error,
            "finite_tail_first": finite_tail_first_error,
            "tail_finite": tail_finite_error,
        },
    )


def _load_riesz(repository: Path) -> tuple[Mapping[str, Any], str]:
    path = repository / RIESZ_RESULT_RELATIVE_PATH
    raw = path.read_bytes()
    payload = _mapping(json.loads(raw), "leaky Riesz result")
    validate_leaky_floquet_riesz_result(payload, repository)
    artifact = _mapping(payload.get("artifact"), "leaky Riesz artifact")
    branches = _mapping(artifact.get("branches"), "leaky Riesz branches")
    return _mapping(branches.get(BRANCH), "inner Riesz branch"), sha256(raw).hexdigest()


def _coefficient_error_norms(
    base: Any,
    current: Mapping[int, complex],
    delayed: Mapping[int, complex],
    precision: int,
) -> tuple[gmpy2.mpfr, gmpy2.mpfr, gmpy2.mpfr, gmpy2.mpfr]:
    current_errors = []
    delayed_errors = []
    current_terms = []
    delayed_terms = []
    for mode in sorted(current):
        current_errors.append(
            _box_distance_split_upper(
                base.current_coefficient[mode], current[mode]
            )
        )
        delayed_errors.append(
            _box_distance_split_upper(
                base.delayed_state_derivative[mode], delayed[mode]
            )
        )
        current_terms.append(_split_upper(current[mode], precision))
        delayed_terms.append(_split_upper(delayed[mode], precision))
    return (
        upward_sum(current_errors, precision),
        upward_sum(delayed_errors, precision),
        upward_sum(current_terms, precision),
        upward_sum(delayed_terms, precision),
    )


def _nested_radii_radius(
    repository: Path,
    evidence: Any,
    precision: int,
) -> tuple[gmpy2.mpfr, gmpy2.mpfr, gmpy2.mpfr]:
    """Derive a smaller ball from the already validated radii polynomial.

    The stored coefficients were proved on the source maximum radius
    ``1e-5``.  The same monotone polynomial is therefore valid at every
    smaller nonnegative radius.  No new orbit solve or parameter
    continuation is used here.
    """

    payload = _mapping(
        json.loads((repository / evidence.source_result).read_text()),
        "inner orbit artifact",
    )
    artifact = _mapping(payload.get("artifact"), "inner orbit body")
    wrapper = _mapping(
        artifact.get("directed_radii_prototype"), "inner radii wrapper"
    )
    validation = _mapping(wrapper.get("validation"), "inner validation")
    finite = _mapping(validation.get("finite"), "inner finite proof")
    blocks = _mapping(validation.get("blocks"), "inner tail proof")
    correction = _mapping(validation.get("correction"), "inner correction")
    if correction.get("chosen_radius") != evidence.correction_radius:
        raise ValueError("the source correction radius changed")
    if correction.get("maximum_radius") != evidence.correction_radius:
        raise ValueError("the source maximum radius changed")
    if correction.get("radii_polynomial_negative") is not True:
        raise ValueError("the source radii polynomial is not strict")
    if finite.get("finite_inverse_validated") is not True:
        raise ValueError("the source finite inverse is absent")
    if blocks.get("full_point_inverse_gate") is not True:
        raise ValueError("the source full point inverse is absent")

    radius = DirectedInterval.from_decimal(NESTED_ORBIT_RADIUS, precision)
    maximum = DirectedInterval.from_decimal(
        correction["maximum_radius"], precision
    )
    if radius.upper > maximum.lower:
        raise ValueError("the nested radius exceeds its source validity ball")
    total_y = DirectedInterval.from_decimal(
        finite["preconditioned_residual_l1_upper"], precision
    ).upper
    full_defect = DirectedInterval.from_decimal(
        blocks["full_point_defect_upper"], precision
    ).upper
    z1 = DirectedInterval.from_decimal(
        correction["coefficient_z1_upper"], precision
    ).upper
    z2 = DirectedInterval.from_decimal(
        correction["coefficient_z2_upper"], precision
    ).upper
    z3 = DirectedInterval.from_decimal(
        correction["coefficient_z3_upper"], precision
    ).upper
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        variation = (
            z1 * radius.upper
            + z2 * radius.upper * radius.upper
            + z3 * radius.upper * radius.upper * radius.upper
        )
        contraction = full_defect + variation
        radii_left = total_y + contraction * radius.upper
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        margin = radius.lower - radii_left
    if not contraction < 1 or margin <= 0:
        raise ArithmeticError("the source-bound nested orbit radius did not close")
    return radius.upper, contraction, margin


def _nested_coefficient_variations(
    base: Any,
    radius: gmpy2.mpfr,
    precision: int,
) -> tuple[gmpy2.mpfr, gmpy2.mpfr]:
    voltage = _sequence_box_norm_upper(base.voltage, precision)
    centered = _sequence_box_norm_upper(base.centered_voltage, precision)
    epsilon = base.parameters["epsilon"].upper
    kappa_3 = base.parameters["kappa_3"].upper
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        square_voltage = 2 * voltage * radius + radius * radius
        square_centered = 2 * centered * radius + radius * radius
        current = square_voltage + 3 * epsilon * kappa_3 * square_centered
        delayed_sum = 3 * epsilon * kappa_3 * square_centered
    return current, delayed_sum


def _augment_finite(
    finite: np.ndarray,
    right_border: np.ndarray,
    left_border: np.ndarray,
) -> np.ndarray:
    return np.block(
        [
            [finite, right_border[:, None]],
            [left_border[None, :], np.zeros((1, 1), dtype=complex)],
        ]
    )


def _augment_derivative(matrix: np.ndarray) -> np.ndarray:
    result = np.zeros(
        (matrix.shape[0] + 1, matrix.shape[1] + 1), dtype=complex
    )
    result[:-1, :-1] = matrix
    return result


def _augment_finite_tail(matrix: np.ndarray) -> np.ndarray:
    return np.vstack((matrix, np.zeros((1, matrix.shape[1]), dtype=complex)))


def _augment_tail_finite(matrix: np.ndarray) -> np.ndarray:
    return np.hstack((matrix, np.zeros((matrix.shape[0], 1), dtype=complex)))


@lru_cache(maxsize=4)
def _prepare_cached(
    repository_text: str,
    dependency_fingerprint: str,
) -> tuple[_Prepared, str]:
    del dependency_fingerprint
    repository = Path(repository_text).resolve()
    _validate_physical_delay_oracle()
    riesz_branch, riesz_hash = _load_riesz(repository)
    orbit, evidence = load_validated_leaky_orbit_evidence(repository, BRANCH)
    if evidence.candidate_fingerprint != riesz_branch["candidate_fingerprint"]:
        raise ValueError("the inner root and Riesz orbit fingerprints differ")
    if evidence.source_result_sha256 != riesz_branch["source_result_sha256"]:
        raise ValueError("the inner root and Riesz orbit artifacts differ")
    if int(riesz_branch["fourier_cutoff"]) != FOURIER_CUTOFF:
        raise ValueError("the inner root requires the audited cutoff 64")
    if riesz_branch.get("analytic_characteristic_multiplicity_preserved_by_schur_reduction") is not True:
        raise ValueError("the analytic multiplicity bridge is absent")

    precision = PRECISION_BITS
    base = _build_leaky_base_sequences(orbit, precision)
    current, delayed = _binary_coefficients(orbit)
    support = max(abs(mode) for mode in current)
    if support != len(orbit.state) - 1 or support != 128:
        raise ValueError("the inner quadratic coefficient support changed")
    modes = np.arange(-FOURIER_CUTOFF, FOURIER_CUTOFF + 1, dtype=int)
    tail_modes = np.concatenate(
        (
            np.arange(-FOURIER_CUTOFF - support, -FOURIER_CUTOFF, dtype=int),
            np.arange(FOURIER_CUTOFF + 1, FOURIER_CUTOFF + support + 1, dtype=int),
        )
    )
    current_error, delayed_error, current_norm, delayed_norm = (
        _coefficient_error_norms(base, current, delayed, precision)
    )
    current_finite = _coefficient_matrix(modes, modes, current)
    delayed_finite = _coefficient_matrix(modes, modes, delayed)
    current_finite_tail = _coefficient_matrix(modes, tail_modes, current)
    delayed_finite_tail = _coefficient_matrix(modes, tail_modes, delayed)
    current_tail_finite = _coefficient_matrix(tail_modes, modes, current)
    delayed_tail_finite = _coefficient_matrix(tail_modes, modes, delayed)

    radius, nested_contraction, nested_margin = _nested_radii_radius(
        repository, evidence, precision
    )
    variation_current, variation_delayed = _nested_coefficient_variations(
        base, radius, precision
    )
    center_data = _evaluate_blocks(
        None,
        orbit=orbit,
        base=base,
        modes=modes,
        tail_modes=tail_modes,
        current_finite=current_finite,
        delayed_finite=delayed_finite,
        current_finite_tail=current_finite_tail,
        delayed_finite_tail=delayed_finite_tail,
        current_tail_finite=current_tail_finite,
        delayed_tail_finite=delayed_tail_finite,
        current_binary_norm=current_norm,
        delayed_binary_norm=delayed_norm,
        s=complex(ROOT_CENTER_BINARY64, 0.0),
        precision=precision,
    )
    finite, first, second, finite_tail, finite_tail_first, tail_finite, errors = center_data
    _binary_environment_checked()
    left_vectors, singular_values, right_adjoint = np.linalg.svd(
        finite, full_matrices=True
    )
    _binary_environment_checked()
    # The added range column must span the approximate cokernel (the left
    # singular vector), while the scalar domain row must detect the right
    # kernel.  Reversing these two vectors can leave a square finite border
    # invertible in binary64 yet destroys the full-operator margin.
    right = RIGHT_BORDER_SCALE * left_vectors[:, -1]
    left = LEFT_BORDER_SCALE * right_adjoint[-1, :]
    grushin = _augment_finite(finite, right, left)
    inverse = np.linalg.inv(grushin)
    _binary_environment_checked()
    prepared = _Prepared(
        orbit=orbit,
        evidence=evidence,
        base=base,
        riesz_branch=riesz_branch,
        modes=modes,
        tail_modes=tail_modes,
        current_finite=current_finite,
        delayed_finite=delayed_finite,
        current_finite_tail=current_finite_tail,
        delayed_finite_tail=delayed_finite_tail,
        current_tail_finite=current_tail_finite,
        delayed_tail_finite=delayed_tail_finite,
        current_binary_norm=current_norm,
        delayed_binary_norm=delayed_norm,
        current_center_error=current_error,
        delayed_center_error_sum=2 * delayed_error,
        current_total_variation=current_error + variation_current,
        delayed_total_variation=2 * delayed_error + variation_delayed,
        period_radius=radius,
        nested_radii_contraction=nested_contraction,
        nested_radii_margin=nested_margin,
        center_matrix=finite,
        center_first=first,
        center_second=second,
        center_finite_tail=finite_tail,
        center_finite_tail_first=finite_tail_first,
        center_tail_finite=tail_finite,
        center_errors=errors,
        right_border=right,
        left_border=left,
        finite_grushin=grushin,
        finite_grushin_inverse=inverse,
        center_singular_values=singular_values,
    )
    return prepared, riesz_hash


def _evaluate_prepared(
    prepared: _Prepared, s: complex
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, Mapping[str, gmpy2.mpfr]]:
    return _evaluate_blocks(
        prepared,
        orbit=prepared.orbit,
        base=prepared.base,
        modes=prepared.modes,
        tail_modes=prepared.tail_modes,
        current_finite=prepared.current_finite,
        delayed_finite=prepared.delayed_finite,
        current_finite_tail=prepared.current_finite_tail,
        delayed_finite_tail=prepared.delayed_finite_tail,
        current_tail_finite=prepared.current_tail_finite,
        delayed_tail_finite=prepared.delayed_tail_finite,
        current_binary_norm=prepared.current_binary_norm,
        delayed_binary_norm=prepared.delayed_binary_norm,
        s=s,
        precision=PRECISION_BITS,
    )


def _operator_variations(
    prepared: _Prepared,
    *,
    maximum_output_mode: int,
    s_modulus_upper: gmpy2.mpfr,
) -> gmpy2.mpfr:
    """Full orbit-ball perturbation for a bounded output-mode block."""

    precision = PRECISION_BITS
    base = prepared.base
    period = base.period.upper
    period_lower = base.period.lower - prepared.period_radius
    if period_lower <= 0:
        raise ArithmeticError("the inner orbit correction crosses zero period")
    radius = prepared.period_radius
    tau_max = max(
        base.parameters["tau_0"].upper,
        base.parameters["tau_1"].upper,
    )
    pi_upper = pi_interval(precision).upper
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        frequency = s_modulus_upper + 2 * pi_upper * maximum_output_mode
        rotation_change = (
            frequency
            * tau_max
            * radius
            / (period_lower * base.period.lower)
        )
        current = (
            (base.period.upper + radius) * prepared.current_total_variation
            + radius * prepared.current_binary_norm
        )
        delayed = (
            (base.period.upper + radius) * prepared.delayed_total_variation
            + radius * (2 * prepared.delayed_binary_norm)
            + base.period.upper
            * rotation_change
            * (2 * prepared.delayed_binary_norm)
        )
        convolution = current + delayed
        diagonal_voltage = radius * base.parameters["epsilon"].upper
        diagonal_recovery = radius * (
            1 + base.parameters["epsilon"].upper
        )
        return max(convolution + diagonal_voltage, diagonal_recovery)


def _coupling_variation(
    prepared: _Prepared,
    *,
    maximum_output_mode: int,
    s_modulus_upper: gmpy2.mpfr,
) -> gmpy2.mpfr:
    precision = PRECISION_BITS
    base = prepared.base
    period_lower = base.period.lower - prepared.period_radius
    radius = prepared.period_radius
    tau_max = max(
        base.parameters["tau_0"].upper,
        base.parameters["tau_1"].upper,
    )
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        frequency = (
            s_modulus_upper
            + 2 * pi_interval(precision).upper * maximum_output_mode
        )
        rotation_change = (
            frequency
            * tau_max
            * radius
            / (period_lower * base.period.lower)
        )
        return (
            (base.period.upper + radius) * prepared.current_total_variation
            + radius * prepared.current_binary_norm
            + (base.period.upper + radius)
            * prepared.delayed_total_variation
            + radius * (2 * prepared.delayed_binary_norm)
            + base.period.upper
            * rotation_change
            * (2 * prepared.delayed_binary_norm)
        )


def _preconditioned_tail_coupling_variation(
    prepared: _Prepared,
    *,
    fast_tail_inverse: gmpy2.mpfr,
    spectral_neighborhood: gmpy2.mpfr,
) -> gmpy2.mpfr:
    """Orbit/T correction after the fast tail diagonal inverse.

    In the physical unshifted-coefficient representation the delay phase is
    indexed by the output mode.  For a fixed-center tail inverse ``A`` the
    aligned factor obeys ``A(s+2*pi*i*k) = I + A(s-s_center)``.  This retains
    the output-frequency cancellation without ever treating an input phase
    as an output phase.
    """

    precision = PRECISION_BITS
    base = prepared.base
    radius = prepared.period_radius
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        period_lower = base.period.lower - radius
    tau_sum = upward_sum(
        (
            base.parameters["tau_0"].upper,
            base.parameters["tau_1"].upper,
        ),
        precision,
    )
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        common = (
            (base.period.upper + radius)
            * (
                prepared.current_total_variation
                + prepared.delayed_total_variation
            )
            + radius
            * (
                prepared.current_binary_norm
                + 2 * prepared.delayed_binary_norm
            )
        )
        phase = (
            prepared.delayed_binary_norm
            * tau_sum
            * radius
            / period_lower
            * (1 + fast_tail_inverse * spectral_neighborhood)
        )
        return fast_tail_inverse * common + phase


def _first_and_second_bounds(
    prepared: _Prepared,
) -> tuple[gmpy2.mpfr, gmpy2.mpfr, gmpy2.mpfr]:
    precision = PRECISION_BITS
    first = DirectedInterval.from_decimal(
        prepared.riesz_branch["local_complex_first_order_coefficient_upper"],
        precision,
    ).upper
    delayed_uniform = DirectedInterval.from_decimal(
        prepared.riesz_branch[
            "delayed_coefficient_uniform_sum_wiener_upper"
        ],
        precision,
    ).upper
    minimum_period = DirectedInterval.from_decimal(
        prepared.riesz_branch["minimum_period_lower"], precision
    ).lower
    maximum_period = DirectedInterval.from_decimal(
        prepared.riesz_branch["maximum_period_upper"], precision
    ).upper
    tau_max = max(
        prepared.base.parameters["tau_0"].upper,
        prepared.base.parameters["tau_1"].upper,
    )
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        second = (
            maximum_period
            * (tau_max / minimum_period) ** 2
            * delayed_uniform
        )
        finite_tail_first = (
            prepared.base.parameters["tau_0"].upper
            + prepared.base.parameters["tau_1"].upper
        ) * (
            2 * prepared.delayed_binary_norm
            + prepared.delayed_total_variation
        )
    return first, second, finite_tail_first


def _tail_inverse_upper(
    prepared: _Prepared,
    *,
    real_center: float,
    imag_center: float,
    neighborhood: gmpy2.mpfr,
) -> tuple[gmpy2.mpfr, gmpy2.mpfr]:
    precision = PRECISION_BITS
    sigma = DirectedInterval.from_float(real_center, precision)
    phase = DirectedInterval.from_float(imag_center, precision)
    center = DirectedComplexInterval(sigma, phase)
    epsilon_period = prepared.base.period * prepared.base.parameters["epsilon"]
    fast_values: list[gmpy2.mpfr] = []
    slow_values: list[gmpy2.mpfr] = []
    for mode in (-FOURIER_CUTOFF - 1, FOURIER_CUTOFF + 1):
        frequency = DirectedComplexInterval(
            center.real,
            center.imag + pi_interval(precision) * (2 * mode),
        )
        fast_values.append(frequency.lower_abs())
        slow_values.append(
            (frequency + DirectedComplexInterval.from_real(epsilon_period)).lower_abs()
        )
    fast_gap = min(fast_values)
    slow_gap = min(slow_values)
    if fast_gap <= neighborhood or slow_gap <= neighborhood:
        raise ArithmeticError("the local tail diagonal neighborhood crosses zero")
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        return 1 / (fast_gap - neighborhood), 1 / (
            slow_gap
            - neighborhood
            - prepared.base.parameters["epsilon"].upper
            * prepared.period_radius
        )


def _tail_to_tail_upper(
    prepared: _Prepared,
    *,
    fast_inverse: gmpy2.mpfr,
    slow_inverse: gmpy2.mpfr,
    diagonal_radius: gmpy2.mpfr,
) -> gmpy2.mpfr:
    precision = PRECISION_BITS
    current = DirectedInterval.from_decimal(
        prepared.riesz_branch["current_coefficient_uniform_wiener_upper"],
        precision,
    ).upper
    delayed = DirectedInterval.from_decimal(
        prepared.riesz_branch[
            "delayed_coefficient_uniform_sum_wiener_upper"
        ],
        precision,
    ).upper
    period = DirectedInterval.from_decimal(
        prepared.riesz_branch["maximum_period_upper"], precision
    ).upper
    epsilon = prepared.base.parameters["epsilon"].upper
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        voltage_column = (
            fast_inverse * (diagonal_radius + period * (current + delayed))
            + slow_inverse * period * epsilon
        )
        recovery_column = (
            fast_inverse * period
            + slow_inverse
            * (diagonal_radius + epsilon * prepared.period_radius)
        )
        return max(voltage_column, recovery_column)


def _product_norm(
    left: np.ndarray,
    right: np.ndarray,
    precision: int,
    *,
    left_norm: gmpy2.mpfr | None = None,
) -> gmpy2.mpfr:
    return _binary_complex_product_split_l1_upper(
        left, right, precision, left_norm=left_norm
    )


def _inverse_defect(
    inverse: np.ndarray,
    matrix: np.ndarray,
    precision: int,
    inverse_norm: gmpy2.mpfr,
) -> tuple[gmpy2.mpfr, np.ndarray]:
    defect = _binary_complex_product_split_l1_upper(
        inverse,
        matrix,
        precision,
        defect_from_identity=True,
        left_norm=inverse_norm,
    )
    product = (
        inverse.real @ matrix.real
        - inverse.imag @ matrix.imag
        + 1.0j
        * (inverse.real @ matrix.imag + inverse.imag @ matrix.real)
    )
    return defect, np.eye(matrix.shape[0], dtype=complex) - product


def _grushin_block_bounds(
    prepared: _Prepared,
    *,
    s: complex,
    neighborhood: gmpy2.mpfr,
    inverse: np.ndarray,
    finite: np.ndarray,
    finite_tail: np.ndarray,
    finite_tail_first: np.ndarray,
    tail_finite: np.ndarray,
    errors: Mapping[str, gmpy2.mpfr],
    include_disk_s_variation: bool,
) -> Mapping[str, Any]:
    precision = PRECISION_BITS
    inverse_norm = _binary_complex_matrix_split_l1_upper(inverse, precision)
    grushin = _augment_finite(
        finite, prepared.right_border, prepared.left_border
    )
    defect, defect_matrix = _inverse_defect(
        inverse, grushin, precision, inverse_norm
    )
    row_norm = _row_dual_upper(inverse[-1, :-1], precision)
    scalar_column_norm = _vector_l1_upper(inverse[:, -1], precision)
    scalar_state_column_norm = _vector_l1_upper(inverse[:-1, -1], precision)
    s_abs = _up(abs(s), precision) + neighborhood
    fast_inverse, slow_inverse = _tail_inverse_upper(
        prepared,
        real_center=float(s.real),
        imag_center=float(s.imag),
        neighborhood=neighborhood,
    )
    finite_orbit = _operator_variations(
        prepared,
        maximum_output_mode=FOURIER_CUTOFF,
        s_modulus_upper=s_abs,
    )
    finite_tail_orbit = _coupling_variation(
        prepared,
        maximum_output_mode=FOURIER_CUTOFF,
        s_modulus_upper=s_abs,
    )
    tail_finite_orbit = _preconditioned_tail_coupling_variation(
        prepared,
        fast_tail_inverse=fast_inverse,
        spectral_neighborhood=neighborhood,
    )
    first_bound, _, finite_tail_first_bound = _first_and_second_bounds(prepared)
    finite_change = errors["finite"] + finite_orbit
    finite_tail_change = errors["finite_tail"] + finite_tail_orbit
    tail_finite_change = errors["tail_finite"]
    if include_disk_s_variation:
        finite_change += first_bound * neighborhood
        finite_tail_change += finite_tail_first_bound * neighborhood
        tail_finite_change += finite_tail_first_bound * neighborhood

    augmented_finite_tail = _augment_finite_tail(finite_tail)
    augmented_tail_finite = _augment_tail_finite(tail_finite)
    finite_tail_product = _product_norm(
        inverse,
        augmented_finite_tail,
        precision,
        left_norm=inverse_norm,
    )
    row_tail_product_matrix = inverse[-1:, :] @ augmented_finite_tail
    row_tail_product = _matrix_max_entry_upper(
        row_tail_product_matrix, precision
    ) + _formation_error(
        row_norm
        * _binary_complex_matrix_split_l1_upper(
            augmented_finite_tail, precision
        ),
        augmented_finite_tail.shape[0],
        precision,
    )
    finite_tail_column = (
        finite_tail_product + inverse_norm * finite_tail_change
    )
    row_tail = row_tail_product + row_norm * finite_tail_change

    tail_finite_norm = _binary_complex_matrix_split_l1_upper(
        augmented_tail_finite, precision
    )
    tail_finite_column = fast_inverse * (
        tail_finite_norm + tail_finite_change
    ) + tail_finite_orbit
    tail_tail = _tail_to_tail_upper(
        prepared,
        fast_inverse=fast_inverse,
        slow_inverse=slow_inverse,
        diagonal_radius=neighborhood,
    )
    finite_column = defect + inverse_norm * finite_change
    contraction = max(
        finite_column + tail_finite_column,
        finite_tail_column + tail_tail,
    )
    bottom_finite = _row_dual_upper(defect_matrix[-1, :], precision) + (
        row_norm * finite_change
    )
    bottom_row = max(bottom_finite, row_tail)
    return {
        "inverse_norm": inverse_norm,
        "defect": defect,
        "defect_matrix": defect_matrix,
        "row_norm": row_norm,
        "scalar_column_norm": scalar_column_norm,
        "scalar_state_column_norm": scalar_state_column_norm,
        "finite_orbit": finite_orbit,
        "finite_tail_orbit": finite_tail_orbit,
        "tail_finite_orbit": tail_finite_orbit,
        "finite_change": finite_change,
        "finite_tail_change": finite_tail_change,
        "tail_finite_change": tail_finite_change,
        "finite_tail_column": finite_tail_column,
        "tail_finite_column": tail_finite_column,
        "tail_tail": tail_tail,
        "contraction": contraction,
        "bottom_row": bottom_row,
        "row_tail": row_tail,
        "fast_tail_inverse": fast_inverse,
        "slow_tail_inverse": slow_inverse,
    }


def _circle_cell_center(
    index: int, precision: int
) -> tuple[complex, gmpy2.mpfr]:
    radius = DirectedInterval.from_decimal(ROOT_DISK_RADIUS, precision)
    angle = pi_interval(precision) * (2 * index) / BOUNDARY_ARC_COUNT
    cosine = cos_interval(angle)
    sine = sin_interval(angle)
    theta_float = 2.0 * math.pi * index / BOUNDARY_ARC_COUNT
    center = complex(
        ROOT_CENTER_BINARY64 + float(ROOT_DISK_RADIUS) * math.cos(theta_float),
        float(ROOT_DISK_RADIUS) * math.sin(theta_float),
    )
    exact_real = DirectedInterval.from_float(
        ROOT_CENTER_BINARY64, precision
    ) + radius * cosine
    exact_imag = radius * sine
    stored = DirectedComplexInterval(
        DirectedInterval.from_float(center.real, precision),
        DirectedInterval.from_float(center.imag, precision),
    )
    exact = DirectedComplexInterval(exact_real, exact_imag)
    center_error = (exact - stored).upper_abs()
    half_angle = pi_interval(precision) / BOUNDARY_ARC_COUNT
    sine_half = sin_interval(half_angle).upper
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        arc_radius = 2 * radius.upper * sine_half + center_error
    return center, arc_radius


def _reference_difference_upper(
    b00: complex,
    slope: complex,
    center: complex,
    reference_slope: complex,
    arc_radius: gmpy2.mpfr,
    precision: int,
) -> gmpy2.mpfr:
    center_offset = center - complex(ROOT_CENTER_BINARY64, 0.0)
    center_difference = b00 - reference_slope * center_offset
    slope_difference = slope - reference_slope
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        return (
            _complex_abs_upper(center_difference, precision)
            + _complex_abs_upper(slope_difference, precision) * arc_radius
            + _formation_error(
                _split_upper(reference_slope, precision)
                * _up(abs(center_offset), precision),
                8,
                precision,
            )
        )


def _boundary_cell(
    prepared: _Prepared,
    index: int,
    reference_slope: complex,
) -> _CellData:
    precision = PRECISION_BITS
    center, arc_radius = _circle_cell_center(index, precision)
    finite, first, second, finite_tail, finite_tail_first, tail_finite, errors = (
        _evaluate_prepared(prepared, center)
    )
    grushin = _augment_finite(
        finite, prepared.right_border, prepared.left_border
    )
    inverse = np.linalg.inv(grushin)
    _binary_environment_checked()
    block = _grushin_block_bounds(
        prepared,
        s=center,
        neighborhood=arc_radius,
        inverse=inverse,
        finite=finite,
        finite_tail=finite_tail,
        finite_tail_first=finite_tail_first,
        tail_finite=tail_finite,
        errors=errors,
        include_disk_s_variation=True,
    )
    q = block["contraction"]
    if not 0 < q < 1:
        raise ArithmeticError(f"boundary Grushin cell {index} did not contract")
    b = inverse[:, -1]
    b_state = b[:-1]
    row = inverse[-1, :]
    first_augmented = _augment_derivative(first)
    first_b = first_augmented @ b
    slope = -complex(row @ first_b)
    slope_round = _formation_error(
        block["row_norm"]
        * _binary_complex_matrix_split_l1_upper(first_augmented, precision)
        * block["scalar_column_norm"],
        2 * grushin.shape[0],
        precision,
    )
    defect_times_b = block["defect_matrix"] @ b
    center_first_error = (
        _complex_abs_upper(complex(defect_times_b[-1]), precision)
        + _formation_error(
            _row_dual_upper(block["defect_matrix"][-1, :], precision)
            * block["scalar_column_norm"],
            grushin.shape[0],
            precision,
        )
        + block["row_norm"]
        * (errors["finite"] + block["finite_orbit"])
        * block["scalar_state_column_norm"]
    )
    _, second_bound, _ = _first_and_second_bounds(prepared)
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        local_taylor_error = (
            slope_round * arc_radius
            + block["row_norm"]
            * errors["first"]
            * block["scalar_state_column_norm"]
            * arc_radius
            + block["row_norm"]
            * (errors["second"] + second_bound)
            * block["scalar_state_column_norm"]
            * arc_radius
            * arc_radius
            / 2
        )
        neumann_remainder = (
            block["bottom_row"]
            * q
            * block["scalar_column_norm"]
            / (1 - q)
        )
        reference_error = _reference_difference_upper(
            complex(inverse[-1, -1]),
            slope,
            center,
            reference_slope,
            arc_radius,
            precision,
        )
        comparison = (
            reference_error
            + center_first_error
            + local_taylor_error
            + neumann_remainder
        )
    summary: Mapping[str, str | int] = {
        "index": index,
        "center_real_binary64": format(center.real, ".17g"),
        "center_imag_binary64": format(center.imag, ".17g"),
        "arc_radius_upper": decimal_upper(arc_radius),
        "finite_bordered_inverse_norm_upper": decimal_upper(
            block["inverse_norm"]
        ),
        "finite_bordered_inverse_defect_upper": decimal_upper(block["defect"]),
        "full_grushin_contraction_upper": decimal_upper(q),
        "bottom_row_defect_upper": decimal_upper(block["bottom_row"]),
        "local_affine_comparison_error_upper": decimal_upper(comparison),
    }
    return _CellData(
        summary=summary,
        comparison=comparison,
        contraction=q,
        inverse_norm=block["inverse_norm"],
        bottom_row_norm=block["row_norm"],
        scalar_column_norm=block["scalar_column_norm"],
    )


def _partition_sha256(cells: Iterable[_CellData]) -> str:
    return canonical_sha256([dict(cell.summary) for cell in cells])


def build_leaky_inner_unstable_root_certificate(
    repository: Path,
) -> LeakyInnerUnstableRootCertificate:
    _require_pinned_binary_blas_environment()
    repository = repository.resolve()
    fingerprint = _dependency_fingerprint(repository)
    return _build_leaky_inner_unstable_root_certificate_cached(
        str(repository), fingerprint
    )


@lru_cache(maxsize=4)
def _build_leaky_inner_unstable_root_certificate_cached(
    repository_text: str,
    dependency_fingerprint: str,
) -> LeakyInnerUnstableRootCertificate:
    repository = Path(repository_text).resolve()
    prepared, riesz_hash = _prepare_cached(
        str(repository), dependency_fingerprint
    )
    (
        unshifted_row_error,
        shifted_column_error,
        unshifted_column_separation,
        shifted_row_separation,
        directed_equivalent_count,
        directed_equivalent_total,
        directed_unshifted_column_separation,
        directed_shifted_row_separation,
    ) = _validate_physical_delay_oracle()
    precision = PRECISION_BITS
    center_inverse = prepared.finite_grushin_inverse
    center_inverse_norm = _binary_complex_matrix_split_l1_upper(
        center_inverse, precision
    )
    center_defect, _ = _inverse_defect(
        center_inverse,
        prepared.finite_grushin,
        precision,
        center_inverse_norm,
    )
    b = center_inverse[:, -1]
    center_first_augmented = _augment_derivative(prepared.center_first)
    reference_slope = -complex(
        center_inverse[-1, :] @ (center_first_augmented @ b)
    )
    reference_slope_lower = _complex_abs_lower(reference_slope, precision)
    if reference_slope_lower <= 0:
        raise ArithmeticError("the effective Hamiltonian slope vanished")

    root_radius = DirectedInterval.from_decimal(ROOT_DISK_RADIUS, precision)
    first_bound, _, finite_tail_first = _first_and_second_bounds(prepared)
    center_disk_block = _grushin_block_bounds(
        prepared,
        s=complex(ROOT_CENTER_BINARY64, 0.0),
        neighborhood=root_radius.upper,
        inverse=center_inverse,
        finite=prepared.center_matrix,
        finite_tail=prepared.center_finite_tail,
        finite_tail_first=prepared.center_finite_tail_first,
        tail_finite=prepared.center_tail_finite,
        errors=prepared.center_errors,
        include_disk_s_variation=True,
    )
    del first_bound, finite_tail_first
    disk_q = center_disk_block["contraction"]
    if not 0 < disk_q < 1:
        raise ArithmeticError("the full infinite Grushin disk did not contract")

    cells = tuple(
        _boundary_cell(prepared, index, reference_slope)
        for index in range(BOUNDARY_ARC_COUNT)
    )
    worst = max(cells, key=lambda cell: cell.comparison)
    maximum_comparison = worst.comparison
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        affine_boundary = reference_slope_lower * root_radius.lower
        rouche_margin = affine_boundary - maximum_comparison
    if rouche_margin <= 0:
        raise ArithmeticError("the scalar effective Hamiltonian Rouché margin failed")

    maximum_cell_q = max(cell.contraction for cell in cells)
    maximum_cell_inverse = max(cell.inverse_norm for cell in cells)
    maximum_cell_row = max(cell.bottom_row_norm for cell in cells)
    maximum_cell_column = max(cell.scalar_column_norm for cell in cells)
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        contraction_budget = (1 - maximum_cell_q) / (
            2 * maximum_cell_inverse
        )
        rouche_budget = (
            rouche_margin
            * (1 - maximum_cell_q)
            / (4 * maximum_cell_row * maximum_cell_column)
        )
        additional_perturbation = min(contraction_budget, rouche_budget)
    if additional_perturbation <= 0:
        raise ArithmeticError("the continuation perturbation interface vanished")

    center_box = DirectedInterval.from_float(ROOT_CENTER_BINARY64, precision)
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        real_lower = center_box.lower - root_radius.upper
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        real_upper = center_box.upper + root_radius.upper
    if real_lower <= 0:
        raise ArithmeticError("the inner root disk crossed the imaginary axis")
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        multiplier_lower = gmpy2.exp(real_lower)
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        multiplier_upper = gmpy2.exp(real_upper)
    if multiplier_lower <= 1:
        raise ArithmeticError("the isolated multiplier did not exceed one")

    source_path = repository / prepared.evidence.source_result
    singular_values = prepared.center_singular_values
    return LeakyInnerUnstableRootCertificate(
        schema_id=SCHEMA_ID,
        model_id=MODEL_ID,
        branch=BRANCH,
        riesz_result_sha256=riesz_hash,
        inner_orbit_result=prepared.evidence.source_result,
        inner_orbit_result_sha256=_sha256_path(source_path),
        candidate_fingerprint=prepared.evidence.candidate_fingerprint,
        source_correction_radius=prepared.evidence.correction_radius,
        nested_correction_radius=NESTED_ORBIT_RADIUS,
        nested_radii_contraction_upper=decimal_upper(
            prepared.nested_radii_contraction
        ),
        nested_radii_margin_lower=decimal_lower(prepared.nested_radii_margin),
        precision_bits=precision,
        binary_blas_thread_count=int(PINNED_OPENBLAS_NUM_THREADS),
        norm_id="complex-modulus Wiener l1; split real/imaginary majorants",
        fourier_cutoff=FOURIER_CUTOFF,
        coefficient_support_half_bandwidth=128,
        finite_block_maximum_delay_output_mode=FOURIER_CUTOFF,
        finite_tail_maximum_delay_output_mode=FOURIER_CUTOFF,
        tail_finite_maximum_delay_output_mode=FOURIER_CUTOFF + 128,
        complex_finite_dimension=2 * (2 * FOURIER_CUTOFF + 1),
        grushin_finite_dimension=2 * (2 * FOURIER_CUTOFF + 1) + 1,
        root_disk_center_binary64=format(ROOT_CENTER_BINARY64, ".17g"),
        root_disk_center_hex=ROOT_CENTER_BINARY64.hex(),
        root_disk_radius=ROOT_DISK_RADIUS,
        root_disk_real_part_lower=decimal_lower(real_lower),
        root_disk_real_part_upper=decimal_upper(real_upper),
        multiplier_modulus_lower=decimal_lower(multiplier_lower),
        multiplier_modulus_upper=decimal_upper(multiplier_upper),
        boundary_arc_count=BOUNDARY_ARC_COUNT,
        unshifted_row_oracle_error_binary64=format(
            unshifted_row_error, ".17g"
        ),
        shifted_column_oracle_error_binary64=format(
            shifted_column_error, ".17g"
        ),
        unshifted_column_mutation_separation_binary64=format(
            unshifted_column_separation, ".17g"
        ),
        shifted_row_mutation_separation_binary64=format(
            shifted_row_separation, ".17g"
        ),
        directed_equivalent_entry_count=directed_equivalent_count,
        directed_equivalent_entry_total=directed_equivalent_total,
        directed_unshifted_column_mutation_separation_lower=decimal_lower(
            directed_unshifted_column_separation
        ),
        directed_shifted_row_mutation_separation_lower=decimal_lower(
            directed_shifted_row_separation
        ),
        right_border_scale=format(RIGHT_BORDER_SCALE, ".17g"),
        left_border_scale=format(LEFT_BORDER_SCALE, ".17g"),
        right_border_sha256=sha256(prepared.right_border.tobytes()).hexdigest(),
        left_border_sha256=sha256(prepared.left_border.tobytes()).hexdigest(),
        center_finite_smallest_singular_value_binary64=format(
            float(singular_values[-1]), ".17g"
        ),
        center_finite_second_smallest_singular_value_binary64=format(
            float(singular_values[-2]), ".17g"
        ),
        center_grushin_inverse_norm_upper=decimal_upper(center_inverse_norm),
        center_grushin_inverse_defect_upper=decimal_upper(center_defect),
        closed_disk_full_grushin_contraction_upper=decimal_upper(disk_q),
        closed_disk_full_grushin_margin_lower=decimal_lower(1 - disk_q),
        reference_effective_slope_real_binary64=format(
            reference_slope.real, ".17g"
        ),
        reference_effective_slope_imag_binary64=format(
            reference_slope.imag, ".17g"
        ),
        reference_effective_slope_modulus_lower=decimal_lower(
            reference_slope_lower
        ),
        affine_boundary_modulus_lower=decimal_lower(affine_boundary),
        maximum_boundary_comparison_error_upper=decimal_upper(
            maximum_comparison
        ),
        rouche_margin_lower=decimal_lower(rouche_margin),
        allowable_additional_pencil_perturbation_upper=decimal_lower(
            additional_perturbation
        ),
        continuation_interface_scope=(
            "an additional analytic full-pencil perturbation in the declared "
            "operator norm; this budget is not itself a common parameter-box "
            "orbit or root theorem"
        ),
        boundary_partition_sha256=_partition_sha256(cells),
        worst_boundary_cell=BoundaryWorstCell(**dict(worst.summary)),
        **{name: True for name in TRUE_FLAGS},
        **{name: False for name in FALSE_FLAGS},
        minimal_remaining_gate=(
            "cover the rest of the principal logarithmic keyhole and count "
            "all other characteristic values before asserting the inner "
            "total unstable index; separately continue the orbit and this "
            "disk on a common parameter box before any uniform claim"
        ),
    )


def build_leaky_inner_unstable_root_result(repository: Path) -> dict[str, Any]:
    repository = repository.resolve()
    certificate = asdict(build_leaky_inner_unstable_root_certificate(repository))
    sources = {
        relative: _sha256_path(repository / relative)
        for relative in SOURCE_MANIFEST
    }
    riesz_path = repository / RIESZ_RESULT_RELATIVE_PATH
    orbit_path = repository / certificate["inner_orbit_result"]
    return {
        "certificate": certificate,
        "manifest": {
            "schema_id": SCHEMA_ID,
            "result": RESULT_RELATIVE_PATH,
            "default_command": DEFAULT_COMMAND,
            "arithmetic_scope": ARITHMETIC_SCOPE,
            "certificate_sha256": canonical_sha256(certificate),
            "source_sha256": sources,
            "riesz_parent_result": RIESZ_RESULT_RELATIVE_PATH,
            "riesz_parent_result_sha256": _sha256_path(riesz_path),
            "inner_orbit_result": certificate["inner_orbit_result"],
            "inner_orbit_result_sha256": _sha256_path(orbit_path),
            "environment": {
                "python": platform.python_version(),
                "platform": platform.platform(),
                "numpy": np.__version__,
                "scipy": scipy.__version__,
                "gmpy2": gmpy2.__version__,
                "mpfr": gmpy2.mpfr_version(),
            },
        },
    }


def validate_leaky_inner_unstable_root_result(
    payload: Mapping[str, Any], repository: Path
) -> None:
    if not isinstance(payload, Mapping) or set(payload) != {
        "certificate",
        "manifest",
    }:
        raise ValueError("the inner unstable-root result has the wrong outer schema")
    certificate = _mapping(payload.get("certificate"), "inner root certificate")
    manifest = _mapping(payload.get("manifest"), "inner root manifest")
    expected_manifest_fields = {
        "schema_id",
        "result",
        "default_command",
        "arithmetic_scope",
        "certificate_sha256",
        "source_sha256",
        "riesz_parent_result",
        "riesz_parent_result_sha256",
        "inner_orbit_result",
        "inner_orbit_result_sha256",
        "environment",
    }
    if set(manifest) != expected_manifest_fields:
        raise ValueError("the inner unstable-root manifest schema changed")
    expected_fields = {
        field.name for field in fields(LeakyInnerUnstableRootCertificate)
    }
    if set(certificate) != expected_fields:
        raise ValueError("the inner unstable-root certificate schema changed")
    if any(certificate.get(name) is not True for name in TRUE_FLAGS):
        raise ValueError("a proved local inner-root statement was weakened")
    if any(certificate.get(name) is not False for name in FALSE_FLAGS):
        raise ValueError("an open inner Floquet or onset claim was promoted")
    if certificate.get("branch") != BRANCH:
        raise ValueError("the local root was attached to another branch")
    if int(certificate["fourier_cutoff"]) != FOURIER_CUTOFF:
        raise ValueError("the local root cutoff changed")
    if int(certificate["binary_blas_thread_count"]) != int(
        PINNED_OPENBLAS_NUM_THREADS
    ):
        raise ValueError("the local root BLAS replay schedule changed")
    if (
        int(certificate["finite_block_maximum_delay_output_mode"])
        != FOURIER_CUTOFF
        or int(certificate["finite_tail_maximum_delay_output_mode"])
        != FOURIER_CUTOFF
        or int(certificate["tail_finite_maximum_delay_output_mode"])
        != FOURIER_CUTOFF + 128
    ):
        raise ValueError("a local root delay variation uses a nonphysical mode bound")
    if gmpy2.mpq(certificate["root_disk_real_part_lower"]) <= 0:
        raise ValueError("the stored root disk is not strictly right-half-plane")
    if gmpy2.mpq(certificate["multiplier_modulus_lower"]) <= 1:
        raise ValueError("the stored multiplier is not strictly unstable")
    if not (
        gmpy2.mpq(certificate["closed_disk_full_grushin_contraction_upper"])
        < 1
    ):
        raise ValueError("the stored full Grushin disk is not invertible")
    if gmpy2.mpq(certificate["rouche_margin_lower"]) <= 0:
        raise ValueError("the stored Rouché margin is not strict")
    if gmpy2.mpq(
        certificate["allowable_additional_pencil_perturbation_upper"]
    ) <= 0:
        raise ValueError("the continuation perturbation interface vanished")
    if max(
        float(certificate["unshifted_row_oracle_error_binary64"]),
        float(certificate["shifted_column_oracle_error_binary64"]),
    ) > 5e-15:
        raise ValueError("the stored physical delay equivalence oracle failed")
    if min(
        float(certificate["unshifted_column_mutation_separation_binary64"]),
        float(certificate["shifted_row_mutation_separation_binary64"]),
    ) < 1e-3:
        raise ValueError("a stored mixed delay mutation was not detected")
    if (
        int(certificate["directed_equivalent_entry_count"])
        != int(certificate["directed_equivalent_entry_total"])
        or int(certificate["directed_equivalent_entry_total"]) <= 0
    ):
        raise ValueError("the directed physical delay entry oracle failed")
    if min(
        gmpy2.mpq(
            certificate[
                "directed_unshifted_column_mutation_separation_lower"
            ]
        ),
        gmpy2.mpq(
            certificate["directed_shifted_row_mutation_separation_lower"]
        ),
    ) <= 0:
        raise ValueError("a directed mixed delay mutation was not separated")

    repository = repository.resolve()
    if manifest.get("schema_id") != SCHEMA_ID:
        raise ValueError("the inner unstable-root manifest schema id changed")
    if manifest.get("result") != RESULT_RELATIVE_PATH:
        raise ValueError("the inner unstable-root result path changed")
    if manifest.get("default_command") != DEFAULT_COMMAND:
        raise ValueError("the inner unstable-root replay command changed")
    if manifest.get("arithmetic_scope") != ARITHMETIC_SCOPE:
        raise ValueError("the inner unstable-root arithmetic scope changed")
    if manifest.get("certificate_sha256") != canonical_sha256(certificate):
        raise ValueError("the inner unstable-root certificate hash changed")
    source_hashes = _mapping(
        manifest.get("source_sha256"), "inner root source manifest"
    )
    if set(source_hashes) != set(SOURCE_MANIFEST):
        raise ValueError("the inner unstable-root source set changed")
    for relative in SOURCE_MANIFEST:
        if source_hashes.get(relative) != _sha256_path(repository / relative):
            raise ValueError(f"the inner unstable-root source changed: {relative}")
    if manifest.get("riesz_parent_result") != RIESZ_RESULT_RELATIVE_PATH:
        raise ValueError("the inner unstable-root Riesz parent path changed")
    if manifest.get("riesz_parent_result_sha256") != _sha256_path(
        repository / RIESZ_RESULT_RELATIVE_PATH
    ):
        raise ValueError("the inner unstable-root Riesz parent changed")
    orbit_relative = certificate.get("inner_orbit_result")
    if not isinstance(orbit_relative, str) or not orbit_relative:
        raise ValueError("the inner unstable-root orbit path is invalid")
    orbit_path = (repository / orbit_relative).resolve()
    try:
        orbit_path.relative_to(repository)
    except ValueError as error:
        raise ValueError("the inner unstable-root orbit escaped the repository") from error
    if manifest.get("inner_orbit_result") != orbit_relative:
        raise ValueError("the inner unstable-root orbit manifest disagrees")
    if manifest.get("inner_orbit_result_sha256") != _sha256_path(orbit_path):
        raise ValueError("the inner unstable-root orbit artifact changed")
    expected = (
        build_leaky_inner_unstable_root_result(repository)
        if os.environ.get("OPENBLAS_NUM_THREADS")
        == PINNED_OPENBLAS_NUM_THREADS
        else _build_result_in_pinned_binary_blas_subprocess(repository)
    )
    if dict(payload) != expected:
        raise ValueError("the inner unstable-root result differs from full replay")


__all__ = [
    "ARITHMETIC_SCOPE",
    "BOUNDARY_ARC_COUNT",
    "BoundaryWorstCell",
    "DEFAULT_COMMAND",
    "FALSE_FLAGS",
    "FOURIER_CUTOFF",
    "GENERATOR_RELATIVE_PATH",
    "LeakyInnerUnstableRootCertificate",
    "NOTE_RELATIVE_PATH",
    "NESTED_ORBIT_RADIUS",
    "PINNED_OPENBLAS_NUM_THREADS",
    "RESULT_RELATIVE_PATH",
    "ROOT_CENTER_BINARY64",
    "ROOT_DISK_RADIUS",
    "SCHEMA_ID",
    "SOURCE_MANIFEST",
    "SOURCE_RELATIVE_PATH",
    "TEST_RELATIVE_PATH",
    "TRUE_FLAGS",
    "build_leaky_inner_unstable_root_certificate",
    "build_leaky_inner_unstable_root_result",
    "canonical_sha256",
    "physical_delay_convolution_oracle_error",
    "validate_leaky_inner_unstable_root_result",
]
