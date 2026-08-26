"""Full-operator right-half zero-free cover for the outer leaky orbit.

The source-validated outer periodic orbit and the leaky Riesz theorem leave
one compact logarithmic keyhole.  This module covers its upper half by an
exact three-root rectilinear forest.  A small square around the neutral root
lies strictly inside the parent punctured disk and is the only root owned by
that theorem; the two complementary roots are uniformly separated from zero
and always use the full-operator estimate.  At the centre of every such
rectangle it
constructs a binary64 finite inverse and an exact two-component Fourier-tail
inverse.  Directed split-Wiener bounds then prove

    ||I-A L_s|| < 1

for the complete infinite operator, uniformly over the validated orbit
ball.  The homotopy ``I-t(I-A L_s)`` is consequently invertible on the
whole cell.

The recovery row is genuinely leaky:

    (D+s)y_w - T*epsilon*y_v + T*epsilon*y_w.

In particular, the finite bottom-right block is ``D+s+T*epsilon`` and the
slow tail inverse is ``(D+s+T*epsilon)^(-1)``.  Neither is imported from the
non-leaky FHN certificate.  The 257-node outer orbit also gives quadratic
coefficient support through mode 256; truncating that support at 128 would
not be a full-operator proof.

The local punctured disk and ``Re(s)>=256`` are supplied by the validated
leaky Riesz parent.  Real conjugacy supplies the lower half-strip.  Only a
complete strict cover promotes the nontranslation zero count and the outer
Floquet index.  Nonlinear attraction, a global attracting block, pulse
onset, and separator claims remain outside this module.

The physical delayed linearization is ``S_alpha M_b``.  This module stores
the unshifted coefficient ``b`` and therefore attaches its Fourier phase to
the output mode (matrix row).  Equivalently one may first shift each
delay-specific coefficient and then attach the residual phase to the input
mode (matrix column).  Directed and exact-convolution oracles verify those
two representations and reject either mixed convention.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from decimal import Decimal, localcontext
from fractions import Fraction
from hashlib import sha256
import json
import math
from pathlib import Path
import platform
from typing import Any, Callable, Iterable, Mapping, Sequence

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
    upward_sum,
)
from canard_control.fhn_periodic_infinite_validation import (
    _BaseSequences,
    _sequence_box_norm_upper,
)
from canard_control.floquet_cover_arithmetic import (
    _binary_environment_checked,
    _box_distance_split_upper,
    _binary_coefficients,
    _binary_complex_matrix_split_l1_upper,
    _binary_complex_max_split_upper,
    _binary_complex_product_split_l1_upper,
    _binary_complex_split_upper,
    _coefficient_matrix,
    _formation_error,
    _rotation_data,
    _up,
)
from canard_control.leaky_floquet_riesz_reduction import (
    RESULT_RELATIVE_PATH as RIESZ_RESULT_RELATIVE_PATH,
    validate_leaky_floquet_riesz_result,
)
from canard_control.leaky_floquet_transfer import (
    OUTER_RESULT_RELATIVE_PATH as OUTER_ORBIT_RESULT_RELATIVE_PATH,
    RESULT_RELATIVE_PATH as FLOQUET_TRANSFER_RESULT_RELATIVE_PATH,
    load_validated_leaky_orbit_evidence,
)
from canard_control.leaky_periodic_validation import (
    _build_leaky_base_sequences,
)


SCHEMA_ID = "leaky-floquet-outer-right-half-cover-v1"
CHECKPOINT_SCHEMA_ID = "leaky-floquet-outer-right-half-cover-checkpoint-v1"
MODEL_ID = "autonomous-leaky-recovery-two-delay-fhn-bistable-proposal"
BRANCH = "outer_pulse"
SOURCE_RELATIVE_PATH = (
    "src/canard_control/leaky_floquet_outer_right_half_cover.py"
)
GENERATOR_RELATIVE_PATH = (
    "experiments/leaky_floquet_outer_right_half_cover.py"
)
NOTE_RELATIVE_PATH = "docs/leaky-floquet-outer-right-half-cover.md"
RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_floquet_outer_right_half_cover.json"
)
DEFAULT_COMMAND = (
    "OPENBLAS_NUM_THREADS=8 PYTHONPATH=build/testdeps:src /usr/bin/python3 "
    "experiments/leaky_floquet_outer_right_half_cover.py"
)
ARITHMETIC_SCOPE = (
    "160-bit outward MPFR split-Wiener bounds with audited IEEE binary64 "
    "four-real-GEMM finite inverses; full leaky two-component pencil, "
    "physical S_alpha M_b output-mode phases with a directed dual-"
    "representation oracle, mode-256 coefficient support, exact fast/slow "
    "tail diagonals, orbit correction and period variation on every cell; "
    "256-bit limiting-cell and four-grandchild stress replay"
)

PRECISION_BITS = 160
FOURIER_CUTOFF = 64
COEFFICIENT_SUPPORT_RADIUS = 256
OUTER_REAL_PART = Decimal(256)
NEUTRAL_CORE_SIZE = Decimal("0.002")
ACCEPTANCE_THRESHOLD = Decimal("0.995")
MAXIMUM_PROCESSED_CELLS = 300000
MAXIMUM_DEPTH = 88
EXPECTED_COMPLETE_LEAF_PARTITION_SHA256: str | None = None
EXPECTED_RIESZ_RESULT_SHA256 = (
    "5185f8f39cd8f87052a50b072af2bfee591d8cd626301bd9a9470134c14df55c"
)
EXPECTED_RIESZ_ARTIFACT_SHA256 = (
    "ea0faca8100a054bbb32750ec4d5150c65a8056a6da1e08fa0781305d3e50298"
)
EXPECTED_OUTER_RESULT_SHA256 = (
    "d888916fed919f1515dd31ab851b2229816ea373365fa0221b1e345580f165a7"
)
EXPECTED_OUTER_ARTIFACT_SHA256 = (
    "91189b24c491f4d0ad3ec6a68df3f25108124566a2f89f40b9ad8aa532058a2f"
)
EXPECTED_FLOQUET_TRANSFER_RESULT_SHA256 = (
    "5a3709ec792b29ed41533101245b13b3d35084ae508bdd1d420728200a5a5b16"
)
EXPECTED_FLOQUET_TRANSFER_ARTIFACT_SHA256 = (
    "baf5eef52bc67a14224a4a228ded74aced7315f9f0b92ee6be7562e91d917089"
)
EXPECTED_SHARED_ARITHMETIC_SHA256 = (
    "5fdd8eae881456a2aecb8a5211a9936abaa8fa1479099bcb205462c8f1296463"
)
NESTED_OUTER_CORRECTION_RADIUS = "1e-8"

TRUE_ON_COMPLETE = (
    "source_validated_outer_orbit_ball_used",
    "leaky_recovery_bottom_right_pencil_validated",
    "full_mode_256_coefficient_support_used",
    "unshifted_delayed_coefficient_output_phase_validated",
    "shifted_coefficient_column_phase_equivalence_validated",
    "mixed_delay_phase_representations_rejected",
    "exact_delay_ratio_alpha_enclosure_used",
    "complex_split_wiener_norm_used",
    "correct_fast_and_slow_tail_inverses_used",
    "nested_outer_orbit_ball_radii_polynomial_validated",
    "outer_translation_root_algebraically_simple_parent_used",
    "orbit_correction_and_period_variation_included_every_cell",
    "local_disk_and_far_right_riesz_parent_used",
    "rectilinear_neutral_core_partition_validated",
    "riesz_local_neumann_seam_and_corner_validated",
    "upper_rectangle_exact_partition_validated",
    "real_axis_conjugacy_seam_validated",
    "positive_half_strip_nontranslation_zero_free_validated",
    "negative_half_by_real_conjugacy_validated",
    "complete_nontranslation_right_half_strip_zero_free_validated",
    "all_nonlocal_cells_full_operator_left_preconditioned_homotopy_validated",
    "outer_nontranslation_floquet_zero_count_validated",
    "center_parameter_outer_floquet_count_validated",
    "outer_nontrivial_unit_circle_exclusion_validated",
    "outer_attracting_floquet_index_validated",
)

ALWAYS_FALSE = (
    "finite_binary_winding_promoted_to_proof",
    "outer_nonlinear_attracting_block_validated",
    "inner_saddle_floquet_index_validated",
    "history_space_separator_validated",
    "physical_pulse_onset_validated",
    "canard_root_equals_physical_onset_proved",
    "parameter_box_uniform_outer_floquet_count_validated",
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


@dataclass(frozen=True)
class CoverLeaf:
    root_id: str
    path: str
    proof_kind: str
    contraction_upper: str
    finite_input_column_sum_upper: str
    tail_input_column_sum_upper: str


@dataclass(frozen=True)
class WorstCoverCell:
    root_id: str
    path: str
    sigma_lower: str
    sigma_center_binary64: str
    sigma_upper: str
    phase_lower: str
    phase_center_binary64: str
    phase_upper: str
    split_parameter_radius_upper: str
    finite_inverse_l1_upper: str
    finite_inverse_defect_upper: str
    finite_first_product_upper: str
    finite_from_tail_center_upper: str
    finite_from_tail_first_upper: str
    tail_from_finite_center_upper: str
    tail_from_finite_first_upper: str
    fast_tail_diagonal_inverse_split_upper: str
    slow_tail_diagonal_inverse_split_upper: str
    finite_output_frequency_upper: str
    finite_full_orbit_correction_upper: str
    finite_convolution_orbit_correction_upper: str
    finite_from_tail_convolution_orbit_correction_upper: str
    tail_from_finite_orbit_correction_upper: str
    finite_to_finite_upper: str
    finite_from_tail_upper: str
    tail_from_finite_upper: str
    tail_to_tail_voltage_input_upper: str
    tail_to_tail_recovery_input_upper: str
    tail_to_tail_upper: str
    finite_input_column_sum_upper: str
    tail_input_column_sum_upper: str
    contraction_upper: str
    contraction_margin_lower: str


@dataclass(frozen=True)
class OuterRightHalfCoverCertificate:
    schema_id: str
    model_id: str
    branch: str
    riesz_result_sha256: str
    riesz_artifact_sha256: str
    outer_orbit_result_sha256: str
    outer_orbit_artifact_sha256: str
    candidate_fingerprint: str
    source_orbit_correction_radius: str
    correction_radius: str
    nested_ball_majorant_validity_radius: str
    nested_ball_preconditioned_residual_upper: str
    nested_ball_coefficient_z0_upper: str
    nested_ball_coefficient_z1_upper: str
    nested_ball_coefficient_z2_upper: str
    nested_ball_coefficient_z3_upper: str
    nested_ball_contraction_upper: str
    nested_ball_radii_left_upper: str
    nested_ball_radii_margin_lower: str
    precision_bits: int
    norm_id: str
    delay_operator_representation: str
    period_correction_frequency_representation: str
    fourier_cutoff: int
    coefficient_support_half_bandwidth: int
    complex_finite_dimension: int
    outer_real_part: str
    upper_phase_lower: str
    upper_phase_upper: str
    local_complex_exclusion_radius_lower: str
    parent_local_keyhole_radius: str
    neutral_core_size: str
    neutral_core_disk_squared_margin_fraction: str
    tail_inverse_monotonicity_condition_validated: bool
    root_rectangle_count: int
    accepted_leaf_count: int
    local_disk_leaf_count: int
    neumann_leaf_count: int
    processed_cell_count: int
    pending_cell_count: int
    accepted_normalized_area_fraction: str
    maximum_depth: int
    acceptance_threshold: str
    maximum_contraction_upper: str | None
    minimum_contraction_margin_lower: str | None
    stress_replay_precision_bits: int
    worst_cell_stress_contraction_upper: str | None
    worst_cell_finer_split_stress_maximum_contraction_upper: str | None
    worst_cell_finer_split_stress_strict: bool
    leaf_partition_sha256: str
    directed_outer_nontranslation_right_half_zero_count: int | None
    source_validated_outer_orbit_ball_used: bool
    leaky_recovery_bottom_right_pencil_validated: bool
    full_mode_256_coefficient_support_used: bool
    unshifted_delayed_coefficient_output_phase_validated: bool
    shifted_coefficient_column_phase_equivalence_validated: bool
    mixed_delay_phase_representations_rejected: bool
    exact_delay_ratio_alpha_enclosure_used: bool
    complex_split_wiener_norm_used: bool
    correct_fast_and_slow_tail_inverses_used: bool
    nested_outer_orbit_ball_radii_polynomial_validated: bool
    outer_translation_root_algebraically_simple_parent_used: bool
    orbit_correction_and_period_variation_included_every_cell: bool
    local_disk_and_far_right_riesz_parent_used: bool
    rectilinear_neutral_core_partition_validated: bool
    riesz_local_neumann_seam_and_corner_validated: bool
    upper_rectangle_exact_partition_validated: bool
    real_axis_conjugacy_seam_validated: bool
    positive_half_strip_nontranslation_zero_free_validated: bool
    negative_half_by_real_conjugacy_validated: bool
    complete_nontranslation_right_half_strip_zero_free_validated: bool
    all_nonlocal_cells_full_operator_left_preconditioned_homotopy_validated: bool
    outer_nontranslation_floquet_zero_count_validated: bool
    center_parameter_outer_floquet_count_validated: bool
    outer_nontrivial_unit_circle_exclusion_validated: bool
    outer_attracting_floquet_index_validated: bool
    finite_binary_winding_promoted_to_proof: bool
    outer_nonlinear_attracting_block_validated: bool
    inner_saddle_floquet_index_validated: bool
    history_space_separator_validated: bool
    physical_pulse_onset_validated: bool
    canard_root_equals_physical_onset_proved: bool
    parameter_box_uniform_outer_floquet_count_validated: bool
    leaves: tuple[CoverLeaf, ...]
    worst_cell: WorstCoverCell | None
    failure_reason: str | None


@dataclass(frozen=True)
class _BinaryCandidate:
    modes: np.ndarray
    tail_modes: np.ndarray
    current_finite: np.ndarray
    delayed_finite: np.ndarray
    current_finite_tail: np.ndarray
    delayed_finite_tail: np.ndarray
    current_tail_finite: np.ndarray
    delayed_tail_finite: np.ndarray
    current_coefficients: Mapping[int, complex]
    delayed_coefficients: Mapping[int, complex]
    current_error_norm: gmpy2.mpfr
    delayed_error_norm: gmpy2.mpfr
    current_binary_norm: gmpy2.mpfr
    delayed_binary_norm: gmpy2.mpfr
    finite_mode_rotations: tuple[np.ndarray, np.ndarray]
    tail_mode_rotations: tuple[np.ndarray, np.ndarray]
    finite_mode_rotation_split: tuple[gmpy2.mpfr, gmpy2.mpfr]
    tail_mode_rotation_split: tuple[gmpy2.mpfr, gmpy2.mpfr]
    finite_mode_rotation_error: tuple[gmpy2.mpfr, gmpy2.mpfr]
    tail_mode_rotation_error: tuple[gmpy2.mpfr, gmpy2.mpfr]
    finite_mode_binary_split: tuple[gmpy2.mpfr, gmpy2.mpfr]
    tail_mode_binary_split: tuple[gmpy2.mpfr, gmpy2.mpfr]


@dataclass(frozen=True)
class _Rectangle:
    root_id: str
    path: str
    sigma_lower: Decimal
    sigma_upper: Decimal
    phase_lower: Decimal
    phase_upper: Decimal


@dataclass(frozen=True)
class _CellBounds:
    leaf: CoverLeaf
    worst: WorstCoverCell
    validated: bool


@dataclass(frozen=True)
class _NestedOrbitBall:
    radius: DirectedInterval
    validity_radius: str
    residual_upper: str
    z0_upper: str
    z1_upper: str
    z2_upper: str
    z3_upper: str
    contraction_upper: str
    radii_left_upper: str
    margin_lower: str


@dataclass(frozen=True)
class _StressReplay:
    precision_bits: int
    same_cell_upper: str | None
    finer_split_upper: str | None
    strict: bool


@dataclass(frozen=True)
class _CoverCheckpointState:
    pending: tuple[_Rectangle, ...]
    leaves: tuple[CoverLeaf, ...]
    local_leaf_count: int
    neumann_leaf_count: int
    processed: int
    deepest: int
    worst: WorstCoverCell | None


def _mapping(value: object, label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{label} must be a mapping")
    return value


def _sha256_path(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def canonical_sha256(value: Any) -> str:
    return sha256(
        json.dumps(
            value, sort_keys=True, separators=(",", ":"), ensure_ascii=True
        ).encode("ascii")
    ).hexdigest()


def _exact_decimal_sum(values: Iterable[str]) -> str:
    items = tuple(values)
    with localcontext() as context:
        context.prec = max(160, sum(len(value) for value in items) + 10)
        total = sum((Decimal(value) for value in items), Decimal(0))
    return format(total, "f")


def _margin(value: str) -> str:
    with localcontext() as context:
        context.prec = max(160, len(value) + 10)
        return format(Decimal(1) - Decimal(value), "f")


def _center_and_radius(
    rectangle: _Rectangle, precision: int
) -> tuple[DirectedInterval, DirectedInterval, gmpy2.mpfr, str, str]:
    with localcontext() as context:
        context.prec = 120
        sigma_decimal = (rectangle.sigma_lower + rectangle.sigma_upper) / 2
        phase_decimal = (rectangle.phase_lower + rectangle.phase_upper) / 2
    sigma_float = float(sigma_decimal)
    phase_float = float(phase_decimal)
    sigma = DirectedInterval.from_float(sigma_float, precision)
    phase = DirectedInterval.from_float(phase_float, precision)
    sigma_lower = DirectedInterval.from_decimal(
        format(rectangle.sigma_lower, "f"), precision
    )
    sigma_upper = DirectedInterval.from_decimal(
        format(rectangle.sigma_upper, "f"), precision
    )
    phase_lower = DirectedInterval.from_decimal(
        format(rectangle.phase_lower, "f"), precision
    )
    phase_upper = DirectedInterval.from_decimal(
        format(rectangle.phase_upper, "f"), precision
    )
    if sigma.lower < sigma_lower.lower or sigma.upper > sigma_upper.upper:
        raise ArithmeticError("the binary sigma centre escaped its rectangle")
    if phase.lower < phase_lower.lower or phase.upper > phase_upper.upper:
        raise ArithmeticError("the binary phase centre escaped its rectangle")
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        delta_sigma = max(
            sigma.upper - sigma_lower.lower,
            sigma_upper.upper - sigma.lower,
        )
        delta_phase = max(
            phase.upper - phase_lower.lower,
            phase_upper.upper - phase.lower,
        )
        radius = delta_sigma + delta_phase
    return (
        sigma,
        phase,
        radius,
        format(sigma_float, ".17g"),
        format(phase_float, ".17g"),
    )


def _mode_rotation_basis(
    requested_modes: np.ndarray,
    base: _BaseSequences,
    precision: int,
) -> tuple[
    tuple[np.ndarray, np.ndarray],
    tuple[gmpy2.mpfr, gmpy2.mpfr],
    tuple[gmpy2.mpfr, gmpy2.mpfr],
    tuple[gmpy2.mpfr, gmpy2.mpfr],
]:
    arrays: list[np.ndarray] = []
    split_bounds: list[gmpy2.mpfr] = []
    error_bounds: list[gmpy2.mpfr] = []
    binary_bounds: list[gmpy2.mpfr] = []
    for tau in (base.parameters["tau_0"], base.parameters["tau_1"]):
        alpha_float = float(tau.lower) / float(base.period.lower)
        stored_values = np.asarray(
            [
                np.exp(-2.0j * math.pi * int(mode) * alpha_float)
                for mode in requested_modes
            ],
            dtype=complex,
        )
        arrays.append(stored_values)
        split = _up(0, precision)
        error = _up(0, precision)
        binary_split = _up(0, precision)
        alpha = tau / base.period
        for mode, stored in zip(
            requested_modes, stored_values, strict=True
        ):
            exact = complex_unit_interval(
                -(pi_interval(precision) * (2 * int(mode)) * alpha)
            )
            split = max(
                split,
                upward_sum(
                    (exact.real.upper_abs(), exact.imag.upper_abs()),
                    precision,
                ),
            )
            error = max(
                error, _box_distance_split_upper(exact, complex(stored))
            )
            binary_split = max(
                binary_split,
                _binary_complex_split_upper(complex(stored), precision),
            )
        split_bounds.append(split)
        error_bounds.append(error)
        binary_bounds.append(binary_split)
    return (
        (arrays[0], arrays[1]),
        (split_bounds[0], split_bounds[1]),
        (error_bounds[0], error_bounds[1]),
        (binary_bounds[0], binary_bounds[1]),
    )


def _prepare_outer_candidate(
    orbit: Any, base: _BaseSequences, precision: int
) -> _BinaryCandidate:
    """Prepare every coefficient through the true quadratic support 256."""

    current, delayed = _binary_coefficients(orbit)
    expected_modes = set(
        range(-COEFFICIENT_SUPPORT_RADIUS, COEFFICIENT_SUPPORT_RADIUS + 1)
    )
    if set(current) != expected_modes or set(delayed) != expected_modes:
        raise ValueError("the 257-node outer coefficient support is incomplete")
    modes = np.arange(-FOURIER_CUTOFF, FOURIER_CUTOFF + 1, dtype=int)
    tail_modes = np.concatenate(
        (
            np.arange(
                -FOURIER_CUTOFF - COEFFICIENT_SUPPORT_RADIUS,
                -FOURIER_CUTOFF,
                dtype=int,
            ),
            np.arange(
                FOURIER_CUTOFF + 1,
                FOURIER_CUTOFF + COEFFICIENT_SUPPORT_RADIUS + 1,
                dtype=int,
            ),
        )
    )
    current_errors: list[gmpy2.mpfr] = []
    delayed_errors: list[gmpy2.mpfr] = []
    current_terms: list[gmpy2.mpfr] = []
    delayed_terms: list[gmpy2.mpfr] = []
    for mode in range(
        -COEFFICIENT_SUPPORT_RADIUS,
        COEFFICIENT_SUPPORT_RADIUS + 1,
    ):
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
        current_terms.append(
            _binary_complex_split_upper(current[mode], precision)
        )
        delayed_terms.append(
            _binary_complex_split_upper(delayed[mode], precision)
        )
    finite_basis = _mode_rotation_basis(modes, base, precision)
    tail_basis = _mode_rotation_basis(tail_modes, base, precision)
    return _BinaryCandidate(
        modes=modes,
        tail_modes=tail_modes,
        current_finite=_coefficient_matrix(modes, modes, current),
        delayed_finite=_coefficient_matrix(modes, modes, delayed),
        current_finite_tail=_coefficient_matrix(modes, tail_modes, current),
        delayed_finite_tail=_coefficient_matrix(modes, tail_modes, delayed),
        current_tail_finite=_coefficient_matrix(tail_modes, modes, current),
        delayed_tail_finite=_coefficient_matrix(tail_modes, modes, delayed),
        current_coefficients=current,
        delayed_coefficients=delayed,
        current_error_norm=upward_sum(current_errors, precision),
        delayed_error_norm=upward_sum(delayed_errors, precision),
        current_binary_norm=upward_sum(current_terms, precision),
        delayed_binary_norm=upward_sum(delayed_terms, precision),
        finite_mode_rotations=finite_basis[0],
        tail_mode_rotations=tail_basis[0],
        finite_mode_rotation_split=finite_basis[1],
        tail_mode_rotation_split=tail_basis[1],
        finite_mode_rotation_error=finite_basis[2],
        tail_mode_rotation_error=tail_basis[2],
        finite_mode_binary_split=finite_basis[3],
        tail_mode_binary_split=tail_basis[3],
    )


def _input_rotated_convolution(
    coefficient_matrix: np.ndarray, input_rotations: np.ndarray
) -> np.ndarray:
    """Apply the column phase for an already shifted coefficient."""

    matrix = np.asarray(coefficient_matrix, dtype=complex)
    rotations = np.asarray(input_rotations, dtype=complex)
    if matrix.ndim != 2 or rotations.shape != (matrix.shape[1],):
        raise ValueError("delay rotations must index convolution input modes")
    return matrix * rotations[None, :]


def _output_rotated_convolution(
    coefficient_matrix: np.ndarray, output_rotations: np.ndarray
) -> np.ndarray:
    """Shift an unshifted coefficient-product by its output Fourier mode."""

    matrix = np.asarray(coefficient_matrix, dtype=complex)
    rotations = np.asarray(output_rotations, dtype=complex)
    if matrix.ndim != 2 or rotations.shape != (matrix.shape[0],):
        raise ValueError("delay rotations must index convolution output modes")
    return rotations[:, None] * matrix


def _candidate_matrices(
    candidate: _BinaryCandidate,
    base: _BaseSequences,
    sigma: DirectedInterval,
    phase: DirectedInterval,
    precision: int,
) -> tuple[
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
    dict[str, gmpy2.mpfr],
]:
    """Build the leaky finite and finite/tail blocks at one centre."""

    modes = candidate.modes
    tail_modes = candidate.tail_modes
    period = float(base.period.lower)
    epsilon = float(base.parameters["epsilon"].lower)
    taus = (
        float(base.parameters["tau_0"].lower),
        float(base.parameters["tau_1"].lower),
    )
    finite_rotations, finite_rotation_split, finite_rotation_error = (
        _rotation_data(
            candidate.finite_mode_rotations,
            candidate.finite_mode_rotation_split,
            candidate.finite_mode_rotation_error,
            candidate.finite_mode_binary_split,
            sigma,
            phase,
            base,
            precision,
        )
    )
    tail_rotations, tail_rotation_split, tail_rotation_error = _rotation_data(
        candidate.tail_mode_rotations,
        candidate.tail_mode_rotation_split,
        candidate.tail_mode_rotation_error,
        candidate.tail_mode_binary_split,
        sigma,
        phase,
        base,
        precision,
    )
    sigma_float = float(sigma.lower)
    phase_float = float(phase.lower)
    finite_frequency = sigma_float + 1.0j * (
        phase_float + 2.0 * math.pi * modes
    )
    top = np.diag(finite_frequency) - period * candidate.current_finite
    derivative_top = np.eye(len(modes), dtype=complex)
    # The stored derivative coefficient is unshifted, so S_alpha M_b acts
    # on output rows.  The delay-shifted-coefficient/column representation
    # is algebraically equivalent and is checked independently in tests.
    for tau, rotation in zip(taus, finite_rotations, strict=True):
        rotated = _output_rotated_convolution(
            candidate.delayed_finite, rotation
        )
        top -= period * rotated
        derivative_top += tau * rotated
    identity = np.eye(len(modes), dtype=complex)
    zero = np.zeros_like(identity)
    finite = np.block(
        [
            [top, period * identity],
            [
                -period * epsilon * identity,
                np.diag(finite_frequency + period * epsilon),
            ],
        ]
    )
    derivative = np.block([[derivative_top, zero], [zero, identity]])

    finite_tail_top = -period * candidate.current_finite_tail
    finite_tail_derivative_top = np.zeros_like(finite_tail_top)
    for tau, rotation in zip(taus, finite_rotations, strict=True):
        rotated = _output_rotated_convolution(
            candidate.delayed_finite_tail, rotation
        )
        finite_tail_top -= period * rotated
        finite_tail_derivative_top += tau * rotated
    finite_tail = np.vstack(
        (finite_tail_top, np.zeros_like(finite_tail_top))
    )
    finite_tail_derivative = np.vstack(
        (finite_tail_derivative_top, np.zeros_like(finite_tail_derivative_top))
    )

    tail_finite = -period * candidate.current_tail_finite
    tail_finite_derivative = np.zeros_like(tail_finite)
    for tau, rotation in zip(taus, tail_rotations, strict=True):
        rotated = _output_rotated_convolution(
            candidate.delayed_tail_finite, rotation
        )
        tail_finite -= period * rotated
        tail_finite_derivative += tau * rotated

    current_exact = _sequence_box_norm_upper(
        base.current_coefficient, precision
    )
    delayed_exact = _sequence_box_norm_upper(
        base.delayed_state_derivative, precision
    )
    maximum_frequency = _up(0, precision)
    maximum_diagonal_error = _up(0, precision)
    for mode, stored in zip(modes, finite_frequency, strict=True):
        exact = DirectedComplexInterval(
            sigma,
            pi_interval(precision) * (2 * int(mode)) + phase,
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
    exact_period = DirectedComplexInterval.from_real(base.period)
    exact_period_epsilon = DirectedComplexInterval.from_real(
        base.period * base.parameters["epsilon"]
    )
    period_error = _box_distance_split_upper(
        exact_period, complex(period, 0.0)
    )
    period_epsilon_error = _box_distance_split_upper(
        exact_period_epsilon, complex(period * epsilon, 0.0)
    )
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        finite_conv_error = base.period.upper * (
            candidate.current_error_norm
            + 2
            * (
                finite_rotation_split * candidate.delayed_error_norm
                + finite_rotation_error * candidate.delayed_binary_norm
            )
        )
        finite_derivative_error = (
            base.parameters["tau_0"].upper
            + base.parameters["tau_1"].upper
        ) * (
            finite_rotation_split * candidate.delayed_error_norm
            + finite_rotation_error * candidate.delayed_binary_norm
        )
        tail_conv_error = base.period.upper * (
            candidate.current_error_norm
            + 2
            * (
                tail_rotation_split * candidate.delayed_error_norm
                + tail_rotation_error * candidate.delayed_binary_norm
            )
        )
        tail_derivative_error = (
            base.parameters["tau_0"].upper
            + base.parameters["tau_1"].upper
        ) * (
            tail_rotation_split * candidate.delayed_error_norm
            + tail_rotation_error * candidate.delayed_binary_norm
        )
        finite_scale = max(
            maximum_frequency
            + base.period.upper
            * (current_exact + 2 * finite_rotation_split * delayed_exact)
            + base.period.upper,
            maximum_frequency
            + 2 * base.period.upper * base.parameters["epsilon"].upper,
        )
        derivative_scale = max(
            1
            + (
                base.parameters["tau_0"].upper
                + base.parameters["tau_1"].upper
            )
            * finite_rotation_split
            * delayed_exact,
            gmpy2.mpfr(1),
        )
        finite_conv_scale = base.period.upper * (
            current_exact + 2 * finite_rotation_split * delayed_exact
        )
        finite_derivative_conv_scale = (
            base.parameters["tau_0"].upper
            + base.parameters["tau_1"].upper
        ) * finite_rotation_split * delayed_exact
        tail_conv_scale = base.period.upper * (
            current_exact + 2 * tail_rotation_split * delayed_exact
        )
        tail_derivative_conv_scale = (
            base.parameters["tau_0"].upper
            + base.parameters["tau_1"].upper
        ) * tail_rotation_split * delayed_exact
        finite_model_error = max(
            maximum_diagonal_error
            + finite_conv_error
            + period_epsilon_error,
            period_error
            + maximum_diagonal_error
            + period_epsilon_error,
        )
        finite_error = finite_model_error + _formation_error(
            finite_scale, 2 * len(modes), precision
        )
        derivative_error = finite_derivative_error + _formation_error(
            derivative_scale, 2 * len(modes), precision
        )
        finite_tail_error = finite_conv_error + _formation_error(
            finite_conv_scale, 2 * len(modes), precision
        )
        finite_tail_derivative_error = (
            finite_derivative_error
            + _formation_error(
                finite_derivative_conv_scale, 2 * len(modes), precision
            )
        )
        tail_finite_error = tail_conv_error + _formation_error(
            tail_conv_scale, len(tail_modes), precision
        )
        tail_finite_derivative_error = (
            tail_derivative_error
            + _formation_error(
                tail_derivative_conv_scale, len(tail_modes), precision
            )
        )
    return (
        finite,
        derivative,
        finite_tail,
        finite_tail_derivative,
        tail_finite,
        tail_finite_derivative,
        {
            "finite": finite_error,
            "derivative": derivative_error,
            "finite_tail": finite_tail_error,
            "finite_tail_derivative": finite_tail_derivative_error,
            "tail_finite": tail_finite_error,
            "tail_finite_derivative": tail_finite_derivative_error,
        },
    )


def _inverse_diagonal_interval(
    mode: int,
    sigma: DirectedInterval,
    phase: DirectedInterval,
    real_shift: DirectedInterval,
) -> DirectedComplexInterval:
    real = sigma + real_shift
    omega = pi_interval(sigma.precision) * (2 * mode) + phase
    denominator = real * real + omega * omega
    return DirectedComplexInterval(real / denominator, -omega / denominator)


def _tail_inverse_bounds(
    sigma: DirectedInterval,
    phase: DirectedInterval,
    base: _BaseSequences,
    precision: int,
) -> tuple[gmpy2.mpfr, gmpy2.mpfr]:
    zero = DirectedInterval.from_decimal(0, precision)
    slow_shift = base.period * base.parameters["epsilon"]
    fast = tuple(
        _inverse_diagonal_interval(mode, sigma, phase, zero)
        for mode in (-(FOURIER_CUTOFF + 1), FOURIER_CUTOFF + 1)
    )
    slow = tuple(
        _inverse_diagonal_interval(mode, sigma, phase, slow_shift)
        for mode in (-(FOURIER_CUTOFF + 1), FOURIER_CUTOFF + 1)
    )
    fast_bound = max(
        upward_sum((value.real.upper_abs(), value.imag.upper_abs()), precision)
        for value in fast
    )
    slow_bound = max(
        upward_sum((value.real.upper_abs(), value.imag.upper_abs()), precision)
        for value in slow
    )
    return fast_bound, slow_bound


def _orbit_corrections(
    base: _BaseSequences,
    correction_radius: DirectedInterval,
    rectangle: _Rectangle,
    split_radius: gmpy2.mpfr,
    fast_tail_inverse: gmpy2.mpfr,
    precision: int,
) -> tuple[
    gmpy2.mpfr,
    gmpy2.mpfr,
    gmpy2.mpfr,
    gmpy2.mpfr,
    dict[str, gmpy2.mpfr],
]:
    """Bound state and period corrections on the complete cell."""

    r = correction_radius.upper
    current_center = _sequence_box_norm_upper(
        base.current_coefficient, precision
    )
    delayed_center = _sequence_box_norm_upper(
        base.delayed_state_derivative, precision
    )
    voltage = _sequence_box_norm_upper(base.voltage, precision)
    centered = _sequence_box_norm_upper(base.centered_voltage, precision)
    epsilon = base.parameters["epsilon"].upper
    kappa_3 = base.parameters["kappa_3"].upper
    sqrt_two = DirectedInterval.from_decimal(2, precision).sqrt().upper
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        current_variation = (
            (2 * voltage + r) * r
            + 3 * epsilon * kappa_3 * (2 * centered + r) * r
        )
        delayed_variation = (
            3 * epsilon * kappa_3 * (2 * centered + r) * r / 2
        )
        current_uniform = current_center + current_variation
        delayed_uniform = delayed_center + delayed_variation
        period_upper = base.period.upper + r
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        period_lower = base.period.lower - r
    if period_lower <= 0:
        raise ArithmeticError("the outer orbit correction crosses zero period")
    sigma_box = DirectedInterval.from_decimal(
        format(rectangle.sigma_upper, "f"), precision
    )
    phase_abs = max(abs(rectangle.phase_lower), abs(rectangle.phase_upper))
    phase_box = DirectedInterval.from_decimal(format(phase_abs, "f"), precision)
    finite_output_frequency = (
        sigma_box * sigma_box
        + (pi_interval(precision) * (2 * FOURIER_CUTOFF) + phase_box) ** 2
    ).sqrt().upper
    finite_delay_terms: list[gmpy2.mpfr] = []
    tail_delay_terms: list[gmpy2.mpfr] = []
    for tau in (base.parameters["tau_0"], base.parameters["tau_1"]):
        with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
            common = (
                r * delayed_uniform
                + base.period.upper * delayed_variation
            )
            finite_delay_terms.append(
                sqrt_two
                * (
                    common
                    + delayed_center
                    * tau.upper
                    * finite_output_frequency
                    * r
                    / period_lower
                )
            )
            tail_delay_terms.append(
                sqrt_two
                * (
                    fast_tail_inverse * common
                    + delayed_center
                    * tau.upper
                    * r
                    / period_lower
                    * (1 + fast_tail_inverse * split_radius)
                )
            )
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        current_term = r * current_uniform + base.period.upper * current_variation
        finite_convolution = current_term + sum(
            finite_delay_terms, gmpy2.mpfr(0)
        )
        finite_full = max(
            finite_convolution + epsilon * r,
            (1 + epsilon) * r,
        )
        tail_from_finite = (
            fast_tail_inverse * current_term
            + sum(tail_delay_terms, gmpy2.mpfr(0))
        )
    return (
        finite_convolution,
        finite_full,
        finite_convolution,
        tail_from_finite,
        {
            "current_center": current_center,
            "delayed_center": delayed_center,
            "current_uniform": current_uniform,
            "delayed_uniform": delayed_uniform,
            "period_upper": period_upper,
            "period_lower": period_lower,
            "epsilon": epsilon,
            "correction_radius": r,
            "finite_output_frequency": finite_output_frequency,
        },
    )


def _validate_cell(
    rectangle: _Rectangle,
    candidate: _BinaryCandidate,
    base: _BaseSequences,
    correction_radius: DirectedInterval,
    precision: int,
    acceptance_threshold: Decimal,
) -> _CellBounds:
    sigma, phase, h, sigma_text, phase_text = _center_and_radius(
        rectangle, precision
    )
    if rectangle.sigma_lower < 0:
        raise ValueError("a keyhole cell left the closed right half-plane")
    (
        finite,
        derivative,
        finite_tail,
        finite_tail_derivative,
        tail_finite,
        tail_finite_derivative,
        errors,
    ) = _candidate_matrices(candidate, base, sigma, phase, precision)
    inverse = np.linalg.inv(finite)
    inverse_norm = _binary_complex_matrix_split_l1_upper(inverse, precision)
    finite_norm = _binary_complex_matrix_split_l1_upper(finite, precision)
    eta_binary = _binary_complex_product_split_l1_upper(
        inverse,
        finite,
        precision,
        defect_from_identity=True,
        left_norm=inverse_norm,
        right_norm=finite_norm,
    )
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        eta = eta_binary + inverse_norm * errors["finite"]
        first = (
            _binary_complex_product_split_l1_upper(
                inverse,
                derivative,
                precision,
                left_norm=inverse_norm,
            )
            + inverse_norm * errors["derivative"]
        )
        finite_tail_center = (
            _binary_complex_product_split_l1_upper(
                inverse,
                finite_tail,
                precision,
                left_norm=inverse_norm,
            )
            + inverse_norm * errors["finite_tail"]
        )
        finite_tail_first = (
            _binary_complex_product_split_l1_upper(
                inverse,
                finite_tail_derivative,
                precision,
                left_norm=inverse_norm,
            )
            + inverse_norm * errors["finite_tail_derivative"]
        )

    fast_tail_inverse, slow_tail_inverse = _tail_inverse_bounds(
        sigma, phase, base, precision
    )
    tail_frequency_binary = complex(float(sigma.lower), float(phase.lower)) + (
        2.0j * math.pi * candidate.tail_modes
    )
    binary_fast_inverse = 1.0 / tail_frequency_binary
    binary_fast_inverse_split = _binary_complex_max_split_upper(
        binary_fast_inverse, precision
    )
    pi_point = DirectedInterval.from_float(math.pi, precision)
    pi_error = (pi_interval(precision) - pi_point).upper_abs()
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        largest_tail_mode = int(np.max(np.abs(candidate.tail_modes)))
        maximum_tail_frequency = (
            sigma.upper
            + phase.upper_abs()
            + 2 * largest_tail_mode * pi_interval(precision).upper
        )
        diagonal_error = (
            2 * largest_tail_mode * pi_error
            + _formation_error(maximum_tail_frequency, 1, precision)
        )
        inverse_formation_error = _formation_error(
            binary_fast_inverse_split, 1, precision
        )
        resolvent_correction = fast_tail_inverse * diagonal_error
        fast_inverse_error = (
            resolvent_correction * binary_fast_inverse_split
            + (1 + resolvent_correction) * inverse_formation_error
        )
    normalized_tail_finite = binary_fast_inverse[:, None] * tail_finite
    normalized_tail_finite_derivative = (
        binary_fast_inverse[:, None] * tail_finite_derivative
    )
    tail_finite_center_binary = _binary_complex_matrix_split_l1_upper(
        normalized_tail_finite, precision
    )
    tail_finite_first_binary = _binary_complex_matrix_split_l1_upper(
        normalized_tail_finite_derivative, precision
    )
    tail_finite_norm = _binary_complex_matrix_split_l1_upper(
        tail_finite, precision
    )
    tail_finite_derivative_norm = _binary_complex_matrix_split_l1_upper(
        tail_finite_derivative, precision
    )
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        tail_finite_center = (
            tail_finite_center_binary
            + fast_tail_inverse * errors["tail_finite"]
            + fast_inverse_error * tail_finite_norm
            + _formation_error(
                tail_finite_center_binary, len(candidate.tail_modes), precision
            )
        )
        tail_finite_first = (
            tail_finite_first_binary
            + fast_tail_inverse * errors["tail_finite_derivative"]
            + fast_inverse_error * tail_finite_derivative_norm
            + _formation_error(
                tail_finite_first_binary,
                len(candidate.tail_modes),
                precision,
            )
        )

    (
        finite_convolution_correction,
        finite_full_correction,
        finite_from_tail_convolution_correction,
        tail_from_finite_correction,
        values,
    ) = _orbit_corrections(
        base,
        correction_radius,
        rectangle,
        h,
        fast_tail_inverse,
        precision,
    )
    sqrt_two = DirectedInterval.from_decimal(2, precision).sqrt().upper
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        alpha_square_sum = (
            (base.parameters["tau_0"].upper / base.period.lower) ** 2
            + (base.parameters["tau_1"].upper / base.period.lower) ** 2
        )
        second_raw = (
            base.period.upper
            * sqrt_two
            * values["delayed_center"]
            * alpha_square_sum
            / 2
        )
        finite_second = inverse_norm * second_raw
        tail_second = fast_tail_inverse * second_raw
        finite_to_finite = (
            eta
            + h * first
            + h * h * finite_second
            + inverse_norm * finite_full_correction
        )
        finite_from_tail = (
            finite_tail_center
            + h * finite_tail_first
            + h * h * finite_second
            + inverse_norm * finite_from_tail_convolution_correction
        )
        tail_from_finite = (
            tail_finite_center
            + h * tail_finite_first
            + h * h * tail_second
            + tail_from_finite_correction
        )
        tail_voltage_input = (
            fast_tail_inverse
            * (
                h
                + values["period_upper"]
                * (
                    values["current_uniform"]
                    + 2 * sqrt_two * values["delayed_uniform"]
                )
            )
            + slow_tail_inverse
            * values["period_upper"]
            * values["epsilon"]
        )
        tail_recovery_input = (
            fast_tail_inverse * values["period_upper"]
            + slow_tail_inverse
            * (h + values["epsilon"] * values["correction_radius"])
        )
        tail_to_tail = max(tail_voltage_input, tail_recovery_input)
        finite_input = finite_to_finite + tail_from_finite
        tail_input = finite_from_tail + tail_to_tail
        contraction = max(finite_input, tail_input)
    finite_input_text = _exact_decimal_sum(
        (decimal_upper(finite_to_finite), decimal_upper(tail_from_finite))
    )
    tail_input_text = _exact_decimal_sum(
        (decimal_upper(finite_from_tail), decimal_upper(tail_to_tail))
    )
    contraction_text = str(
        max(Decimal(finite_input_text), Decimal(tail_input_text))
    )
    margin_text = _margin(contraction_text)
    validated = (
        Decimal(contraction_text) < 1
        and Decimal(contraction_text) <= acceptance_threshold
        and Decimal(margin_text) > 0
    )
    leaf = CoverLeaf(
        root_id=rectangle.root_id,
        path=rectangle.path,
        proof_kind="full_operator_neumann",
        contraction_upper=contraction_text,
        finite_input_column_sum_upper=finite_input_text,
        tail_input_column_sum_upper=tail_input_text,
    )
    worst = WorstCoverCell(
        root_id=rectangle.root_id,
        path=rectangle.path,
        sigma_lower=format(rectangle.sigma_lower, "f"),
        sigma_center_binary64=sigma_text,
        sigma_upper=format(rectangle.sigma_upper, "f"),
        phase_lower=format(rectangle.phase_lower, "f"),
        phase_center_binary64=phase_text,
        phase_upper=format(rectangle.phase_upper, "f"),
        split_parameter_radius_upper=decimal_upper(h),
        finite_inverse_l1_upper=decimal_upper(inverse_norm),
        finite_inverse_defect_upper=decimal_upper(eta),
        finite_first_product_upper=decimal_upper(first),
        finite_from_tail_center_upper=decimal_upper(finite_tail_center),
        finite_from_tail_first_upper=decimal_upper(finite_tail_first),
        tail_from_finite_center_upper=decimal_upper(tail_finite_center),
        tail_from_finite_first_upper=decimal_upper(tail_finite_first),
        fast_tail_diagonal_inverse_split_upper=decimal_upper(fast_tail_inverse),
        slow_tail_diagonal_inverse_split_upper=decimal_upper(slow_tail_inverse),
        finite_output_frequency_upper=decimal_upper(
            values["finite_output_frequency"]
        ),
        finite_full_orbit_correction_upper=decimal_upper(finite_full_correction),
        finite_convolution_orbit_correction_upper=decimal_upper(
            finite_convolution_correction
        ),
        finite_from_tail_convolution_orbit_correction_upper=decimal_upper(
            finite_from_tail_convolution_correction
        ),
        tail_from_finite_orbit_correction_upper=decimal_upper(
            tail_from_finite_correction
        ),
        finite_to_finite_upper=decimal_upper(finite_to_finite),
        finite_from_tail_upper=decimal_upper(finite_from_tail),
        tail_from_finite_upper=decimal_upper(tail_from_finite),
        tail_to_tail_voltage_input_upper=decimal_upper(tail_voltage_input),
        tail_to_tail_recovery_input_upper=decimal_upper(tail_recovery_input),
        tail_to_tail_upper=decimal_upper(tail_to_tail),
        finite_input_column_sum_upper=finite_input_text,
        tail_input_column_sum_upper=tail_input_text,
        contraction_upper=contraction_text,
        contraction_margin_lower=margin_text,
    )
    return _CellBounds(leaf=leaf, worst=worst, validated=validated)


def _split_rectangle(rectangle: _Rectangle) -> tuple[_Rectangle, _Rectangle]:
    sigma_width = Fraction(rectangle.sigma_upper) - Fraction(
        rectangle.sigma_lower
    )
    phase_width = Fraction(rectangle.phase_upper) - Fraction(
        rectangle.phase_lower
    )
    if sigma_width >= phase_width:
        with localcontext() as context:
            context.prec = 400
            midpoint = (
                rectangle.sigma_lower + rectangle.sigma_upper
            ) / 2
        return (
            _Rectangle(
                rectangle.root_id,
                rectangle.path + "x0",
                rectangle.sigma_lower,
                midpoint,
                rectangle.phase_lower,
                rectangle.phase_upper,
            ),
            _Rectangle(
                rectangle.root_id,
                rectangle.path + "x1",
                midpoint,
                rectangle.sigma_upper,
                rectangle.phase_lower,
                rectangle.phase_upper,
            ),
        )
    with localcontext() as context:
        context.prec = 400
        midpoint = (rectangle.phase_lower + rectangle.phase_upper) / 2
    return (
        _Rectangle(
            rectangle.root_id,
            rectangle.path + "y0",
            rectangle.sigma_lower,
            rectangle.sigma_upper,
            rectangle.phase_lower,
            midpoint,
        ),
        _Rectangle(
            rectangle.root_id,
            rectangle.path + "y1",
            rectangle.sigma_lower,
            rectangle.sigma_upper,
            midpoint,
            rectangle.phase_upper,
        ),
    )


def _root_rectangles(phase_upper: Decimal) -> tuple[_Rectangle, ...]:
    a = NEUTRAL_CORE_SIZE
    return (
        _Rectangle(
            "neutral_core",
            "",
            Decimal(0),
            a,
            Decimal(0),
            a,
        ),
        _Rectangle(
            "right_strip",
            "",
            a,
            OUTER_REAL_PART,
            Decimal(0),
            phase_upper,
        ),
        _Rectangle(
            "upper_left_strip",
            "",
            Decimal(0),
            a,
            a,
            phase_upper,
        ),
    )


def _rectangle_area_fraction(rectangle: _Rectangle) -> Fraction:
    return (
        (Fraction(rectangle.sigma_upper) - Fraction(rectangle.sigma_lower))
        * (Fraction(rectangle.phase_upper) - Fraction(rectangle.phase_lower))
    )


def _neutral_core_disk_squared_margin_fraction(radius: Decimal) -> Fraction:
    return Fraction(radius) ** 2 - 2 * Fraction(NEUTRAL_CORE_SIZE) ** 2


def _fraction_text(value: Fraction) -> str:
    return (
        str(value.numerator)
        if value.denominator == 1
        else f"{value.numerator}/{value.denominator}"
    )


def _rectilinear_root_partition_validated(
    roots: Sequence[_Rectangle], phase_upper: Decimal, local_radius: Decimal
) -> bool:
    expected = _root_rectangles(phase_upper)
    if tuple(roots) != expected or len(roots) != 3:
        return False
    if not Decimal(0) < NEUTRAL_CORE_SIZE < min(
        OUTER_REAL_PART, phase_upper
    ):
        return False
    if _neutral_core_disk_squared_margin_fraction(local_radius) <= 0:
        return False
    if not _rectangle_strictly_inside_disk(roots[0], local_radius):
        return False
    total = Fraction(OUTER_REAL_PART) * Fraction(phase_upper)
    if sum((_rectangle_area_fraction(root) for root in roots), Fraction()) != total:
        return False
    # Exact ownership: the local square, right strip, and upper-left strip
    # meet only on sigma=a or phase=a and have disjoint interiors.
    core, right, upper = roots
    return bool(
        core.sigma_upper == right.sigma_lower == upper.sigma_upper
        and core.phase_upper == upper.phase_lower == NEUTRAL_CORE_SIZE
        and core.sigma_lower == upper.sigma_lower == Decimal(0)
        and core.phase_lower == right.phase_lower == Decimal(0)
        and right.sigma_upper == OUTER_REAL_PART
        and right.phase_upper == upper.phase_upper == phase_upper
    )


def _rectangle_strictly_inside_disk(
    rectangle: _Rectangle, radius: Decimal
) -> bool:
    """Use exact rational geometry for the circular parent seam."""

    sigma = Fraction(rectangle.sigma_upper)
    phase = Fraction(rectangle.phase_upper)
    exact_radius = Fraction(radius)
    return sigma * sigma + phase * phase < exact_radius * exact_radius


def _rectangle_is_neutral_core_root(rectangle: _Rectangle) -> bool:
    """Recognize the one root owned by the parent local theorem.

    The rectilinear construction removes the circular Riesz seam only if
    local ownership stops at this root.  In particular, descendants of the
    two complementary roots are *not* reclassified merely because their
    upper corner happens to lie in the parent's disk.
    """

    return bool(
        rectangle.root_id == "neutral_core"
        and rectangle.path == ""
        and rectangle.sigma_lower == Decimal(0)
        and rectangle.sigma_upper == NEUTRAL_CORE_SIZE
        and rectangle.phase_lower == Decimal(0)
        and rectangle.phase_upper == NEUTRAL_CORE_SIZE
    )


def _rectangle_from_path(root: _Rectangle, path: str) -> _Rectangle:
    if len(path) % 2:
        raise ValueError("a dyadic path has odd length")
    rectangle = root
    for index in range(0, len(path), 2):
        token = path[index : index + 2]
        first, second = _split_rectangle(rectangle)
        if first.path.endswith(token):
            rectangle = first
        elif second.path.endswith(token):
            rectangle = second
        else:
            raise ValueError("a dyadic path uses the wrong split axis")
    if rectangle.path != path:
        raise ValueError("a dyadic path reconstruction failed")
    return rectangle


def _prefix_complete(
    leaves: Sequence[CoverLeaf], root_ids: Sequence[str]
) -> bool:
    by_root = {root: [] for root in root_ids}
    for leaf in leaves:
        if leaf.root_id not in by_root or len(leaf.path) % 2:
            return False
        tokens = tuple(
            leaf.path[index : index + 2]
            for index in range(0, len(leaf.path), 2)
        )
        if any(token not in ("x0", "x1", "y0", "y1") for token in tokens):
            return False
        by_root[leaf.root_id].append(tokens)
    for paths in by_root.values():
        if not paths:
            return False
        trie: dict[str, Any] = {}
        for path in paths:
            node = trie
            for token in path:
                if "leaf" in node:
                    return False
                node = node.setdefault(token, {})
            if node:
                return False
            node["leaf"] = True

        def complete(node: Mapping[str, Any]) -> bool:
            if node.get("leaf") is True:
                return len(node) == 1
            keys = set(node)
            if keys not in ({"x0", "x1"}, {"y0", "y1"}):
                return False
            return all(complete(_mapping(node[key], "cover trie")) for key in keys)

        if not complete(trie):
            return False
        if sum(Fraction(1, 2 ** len(path)) for path in paths) != 1:
            return False
    return True


def _leaf_digest(leaves: Sequence[CoverLeaf]) -> str:
    lines = [
        "|".join(
            (
                leaf.root_id,
                leaf.path,
                leaf.proof_kind,
                leaf.contraction_upper,
                leaf.finite_input_column_sum_upper,
                leaf.tail_input_column_sum_upper,
            )
        )
        for leaf in sorted(leaves, key=lambda item: (item.root_id, item.path))
    ]
    return sha256(("\n".join(lines) + "\n").encode("ascii")).hexdigest()


def _normalized_area_fraction(
    leaves: Sequence[CoverLeaf],
    roots: Sequence[_Rectangle] | None = None,
) -> str:
    if roots is None:
        roots = _root_rectangles(
            Decimal(decimal_upper(pi_interval(PRECISION_BITS).upper))
        )
    by_id = {root.root_id: root for root in roots}
    if len(by_id) != len(roots):
        raise ValueError("outer root identifiers are not unique")
    total_area = sum(
        (_rectangle_area_fraction(root) for root in roots), Fraction()
    )
    if total_area <= 0:
        raise ValueError("outer root area is not positive")
    accepted_area = Fraction()
    for leaf in leaves:
        if leaf.root_id not in by_id:
            raise ValueError("an outer leaf has an unknown weighted root")
        accepted_area += _rectangle_area_fraction(by_id[leaf.root_id]) / (
            2 ** (len(leaf.path) // 2)
        )
    return _fraction_text(accepted_area / total_area)


def _checkpoint_environment() -> dict[str, Any]:
    return {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "gmpy2": gmpy2.__version__,
        "mpfr": gmpy2.mpfr_version(),
        "numpy_blas": np.__config__.CONFIG.get("Build Dependencies", {}).get(
            "blas", {}
        ),
    }


def _rectangle_record(rectangle: _Rectangle) -> dict[str, str]:
    return {
        "root_id": rectangle.root_id,
        "path": rectangle.path,
        "sigma_lower": format(rectangle.sigma_lower, "f"),
        "sigma_upper": format(rectangle.sigma_upper, "f"),
        "phase_lower": format(rectangle.phase_lower, "f"),
        "phase_upper": format(rectangle.phase_upper, "f"),
    }


def _cover_checkpoint(
    repository: Path,
    *,
    roots: Sequence[_Rectangle],
    candidate_fingerprint: str,
    precision: int,
    threshold: Decimal,
    maximum_depth: int,
    phase_upper: Decimal,
    local_radius: Decimal,
    keyhole_radius: Decimal,
    pending: Sequence[_Rectangle],
    leaves: Sequence[CoverLeaf],
    local_leaf_count: int,
    neumann_leaf_count: int,
    processed: int,
    deepest: int,
    worst: WorstCoverCell | None,
    source_sha256: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    """Serialize one deterministic source-bound DFS frontier.

    The checkpoint is not a theorem artifact.  It is a lossless execution
    frontier whose accepted leaves and pending cells still form the exact
    root prefix partition.  Final leaves are sorted independently of DFS
    order, so resumption has the same claim-bearing leaf digest as a one-shot
    run.
    """

    repository = repository.resolve()
    current_source_hashes = {
        relative: _sha256_path(repository / relative)
        for relative in SOURCE_MANIFEST
    }
    if source_sha256 is None:
        frozen_source_hashes = current_source_hashes
    else:
        if dict(source_sha256) != current_source_hashes:
            raise ValueError("outer cover sources changed during execution")
        frozen_source_hashes = dict(source_sha256)
    body: dict[str, Any] = {
        "schema_id": CHECKPOINT_SCHEMA_ID,
        "source_sha256": frozen_source_hashes,
        "riesz_result_sha256": _sha256_path(
            repository / RIESZ_RESULT_RELATIVE_PATH
        ),
        "riesz_artifact_sha256": EXPECTED_RIESZ_ARTIFACT_SHA256,
        "outer_orbit_result_sha256": EXPECTED_OUTER_RESULT_SHA256,
        "outer_orbit_artifact_sha256": EXPECTED_OUTER_ARTIFACT_SHA256,
        "candidate_fingerprint": candidate_fingerprint,
        "arithmetic_environment": _checkpoint_environment(),
        "precision_bits": precision,
        "acceptance_threshold": format(threshold, "f"),
        "maximum_depth": maximum_depth,
        "correction_radius": NESTED_OUTER_CORRECTION_RADIUS,
        "phase_upper": format(phase_upper, "f"),
        "local_complex_exclusion_radius_lower": format(local_radius, "f"),
        "parent_local_keyhole_radius": format(keyhole_radius, "f"),
        "root_rectangles": [_rectangle_record(root) for root in roots],
        "pending_stack_order": (
            "depth-first-pop-last; roots-reversed; children-appended-"
            "second-then-first"
        ),
        "leaf_sort_order": "root-id-then-dyadic-path",
        "processed_cell_count": processed,
        "local_disk_leaf_count": local_leaf_count,
        "neumann_leaf_count": neumann_leaf_count,
        "maximum_depth_reached": deepest,
        "accepted_leaf_partition_sha256": _leaf_digest(leaves),
        "leaves": [asdict(leaf) for leaf in leaves],
        "pending": [_rectangle_record(rectangle) for rectangle in pending],
        "worst_cell": None if worst is None else asdict(worst),
    }
    return {
        "checkpoint": body,
        "checkpoint_sha256": canonical_sha256(body),
    }


def _restore_cover_checkpoint(
    payload: Mapping[str, Any],
    repository: Path,
    *,
    roots: Sequence[_Rectangle],
    candidate_fingerprint: str,
    precision: int,
    threshold: Decimal,
    maximum_depth: int,
    phase_upper: Decimal,
    local_radius: Decimal,
    keyhole_radius: Decimal,
) -> _CoverCheckpointState:
    """Hostile-validate and restore a deterministic DFS frontier."""

    if not isinstance(payload, Mapping) or set(payload) != {
        "checkpoint",
        "checkpoint_sha256",
    }:
        raise ValueError("outer cover checkpoint has the wrong wrapper schema")
    body = _mapping(payload.get("checkpoint"), "outer cover checkpoint")
    if payload.get("checkpoint_sha256") != canonical_sha256(body):
        raise ValueError("outer cover checkpoint digest changed")
    expected_keys = {
        "schema_id",
        "source_sha256",
        "riesz_result_sha256",
        "riesz_artifact_sha256",
        "outer_orbit_result_sha256",
        "outer_orbit_artifact_sha256",
        "candidate_fingerprint",
        "arithmetic_environment",
        "precision_bits",
        "acceptance_threshold",
        "maximum_depth",
        "correction_radius",
        "phase_upper",
        "local_complex_exclusion_radius_lower",
        "parent_local_keyhole_radius",
        "root_rectangles",
        "pending_stack_order",
        "leaf_sort_order",
        "processed_cell_count",
        "local_disk_leaf_count",
        "neumann_leaf_count",
        "maximum_depth_reached",
        "accepted_leaf_partition_sha256",
        "leaves",
        "pending",
        "worst_cell",
    }
    if set(body) != expected_keys:
        raise ValueError("outer cover checkpoint body schema changed")
    repository = repository.resolve()
    source_hashes = body.get("source_sha256")
    if not isinstance(source_hashes, Mapping) or set(source_hashes) != set(
        SOURCE_MANIFEST
    ):
        raise ValueError("outer cover checkpoint source manifest changed")
    for relative in SOURCE_MANIFEST:
        if source_hashes.get(relative) != _sha256_path(repository / relative):
            raise ValueError(
                f"outer cover checkpoint source hash changed: {relative}"
            )
    fixed = {
        "schema_id": CHECKPOINT_SCHEMA_ID,
        "riesz_result_sha256": _sha256_path(
            repository / RIESZ_RESULT_RELATIVE_PATH
        ),
        "riesz_artifact_sha256": EXPECTED_RIESZ_ARTIFACT_SHA256,
        "outer_orbit_result_sha256": EXPECTED_OUTER_RESULT_SHA256,
        "outer_orbit_artifact_sha256": EXPECTED_OUTER_ARTIFACT_SHA256,
        "candidate_fingerprint": candidate_fingerprint,
        "arithmetic_environment": _checkpoint_environment(),
        "precision_bits": precision,
        "acceptance_threshold": format(threshold, "f"),
        "maximum_depth": maximum_depth,
        "correction_radius": NESTED_OUTER_CORRECTION_RADIUS,
        "phase_upper": format(phase_upper, "f"),
        "local_complex_exclusion_radius_lower": format(local_radius, "f"),
        "parent_local_keyhole_radius": format(keyhole_radius, "f"),
        "root_rectangles": [_rectangle_record(root) for root in roots],
        "pending_stack_order": (
            "depth-first-pop-last; roots-reversed; children-appended-"
            "second-then-first"
        ),
        "leaf_sort_order": "root-id-then-dyadic-path",
    }
    if any(body.get(name) != value for name, value in fixed.items()):
        raise ValueError("outer cover checkpoint theorem binding changed")

    leaves_value = body.get("leaves")
    pending_value = body.get("pending")
    if not isinstance(leaves_value, list) or not isinstance(pending_value, list):
        raise ValueError("outer cover checkpoint frontier must use JSON lists")
    leaf_fields = {field.name for field in fields(CoverLeaf)}
    leaves: list[CoverLeaf] = []
    root_by_id = {root.root_id: root for root in roots}
    root_order = {root.root_id: index for index, root in enumerate(roots)}

    def dfs_key(root_id: str, path: str) -> tuple[int, tuple[int, ...]]:
        return (
            root_order[root_id],
            tuple(
                int(path[index + 1]) for index in range(0, len(path), 2)
            ),
        )

    local_count = 0
    neumann_count = 0
    for value in leaves_value:
        record = _mapping(value, "outer checkpoint leaf")
        if set(record) != leaf_fields:
            raise ValueError("outer checkpoint leaf schema changed")
        leaf = CoverLeaf(**dict(record))
        if leaf.root_id not in root_by_id:
            raise ValueError("outer checkpoint leaf has an unknown root")
        rectangle = _rectangle_from_path(root_by_id[leaf.root_id], leaf.path)
        contraction = Decimal(leaf.contraction_upper)
        finite = Decimal(leaf.finite_input_column_sum_upper)
        tail = Decimal(leaf.tail_input_column_sum_upper)
        if leaf.proof_kind == "riesz_local_disk":
            local_count += 1
            if (contraction, finite, tail) != (Decimal(0),) * 3:
                raise ValueError("outer checkpoint local leaf has Neumann data")
            if not _rectangle_is_neutral_core_root(rectangle):
                raise ValueError(
                    "outer checkpoint local leaf is not the neutral-core root"
                )
        elif leaf.proof_kind == "full_operator_neumann":
            neumann_count += 1
            if contraction != max(finite, tail) or not (
                Decimal(0) < contraction <= threshold
            ):
                raise ValueError("outer checkpoint Neumann leaf is invalid")
            if rectangle.root_id == "neutral_core":
                raise ValueError(
                    "outer checkpoint split the locally owned neutral core"
                )
        else:
            raise ValueError("outer checkpoint leaf has an unknown proof kind")
        leaves.append(leaf)
    if len({(leaf.root_id, leaf.path) for leaf in leaves}) != len(leaves):
        raise ValueError("outer checkpoint leaves are not unique")
    if leaves != sorted(
        leaves, key=lambda leaf: dfs_key(leaf.root_id, leaf.path)
    ):
        raise ValueError("outer checkpoint accepted leaves changed DFS order")
    if _leaf_digest(leaves) != body.get("accepted_leaf_partition_sha256"):
        raise ValueError("outer checkpoint accepted-leaf digest changed")

    rectangle_fields = set(_rectangle_record(roots[0]))
    pending: list[_Rectangle] = []
    for value in pending_value:
        record = _mapping(value, "outer checkpoint pending rectangle")
        if set(record) != rectangle_fields:
            raise ValueError("outer checkpoint rectangle schema changed")
        root_id = str(record["root_id"])
        path = str(record["path"])
        if root_id not in root_by_id:
            raise ValueError("outer checkpoint rectangle has an unknown root")
        rectangle = _rectangle_from_path(root_by_id[root_id], path)
        if dict(record) != _rectangle_record(rectangle):
            raise ValueError("outer checkpoint rectangle geometry changed")
        if rectangle.root_id == "neutral_core":
            raise ValueError("outer checkpoint left the neutral core pending")
        pending.append(rectangle)
    if list(reversed(pending)) != sorted(
        pending,
        key=lambda rectangle: dfs_key(rectangle.root_id, rectangle.path),
    ):
        raise ValueError("outer checkpoint pending stack changed DFS order")
    identifiers = [(leaf.root_id, leaf.path) for leaf in leaves] + [
        (rectangle.root_id, rectangle.path) for rectangle in pending
    ]
    if len(set(identifiers)) != len(identifiers):
        raise ValueError("outer checkpoint frontier contains duplicates")
    frontier = [
        CoverLeaf(root_id, path, "frontier", "0", "0", "0")
        for root_id, path in identifiers
    ]
    if not _prefix_complete(frontier, tuple(root_by_id)):
        raise ValueError("outer checkpoint frontier is not prefix-complete")

    processed = body.get("processed_cell_count")
    deepest = body.get("maximum_depth_reached")
    if not isinstance(processed, int) or processed < 0:
        raise ValueError("outer checkpoint processed count is invalid")
    if not isinstance(deepest, int) or deepest < 0:
        raise ValueError("outer checkpoint maximum depth is invalid")
    if processed != 2 * len(leaves) + len(pending) - len(roots):
        raise ValueError("outer checkpoint binary-tree count changed")
    derived_deepest = max(
        [len(leaf.path) // 2 for leaf in leaves]
        + [max(0, len(rectangle.path) // 2 - 1) for rectangle in pending]
        + [0]
    )
    if deepest != derived_deepest or deepest > maximum_depth:
        raise ValueError("outer checkpoint reached depth changed")
    if body.get("local_disk_leaf_count") != local_count:
        raise ValueError("outer checkpoint local leaf count changed")
    if local_count != 1:
        raise ValueError(
            "outer checkpoint must contain exactly one neutral-core local leaf"
        )
    if body.get("neumann_leaf_count") != neumann_count:
        raise ValueError("outer checkpoint Neumann leaf count changed")
    if local_count + neumann_count != len(leaves):
        raise ValueError("outer checkpoint proof-kind count changed")

    worst_value = body.get("worst_cell")
    worst: WorstCoverCell | None = None
    if neumann_count:
        record = _mapping(worst_value, "outer checkpoint worst cell")
        if set(record) != {field.name for field in fields(WorstCoverCell)}:
            raise ValueError("outer checkpoint worst-cell schema changed")
        worst = WorstCoverCell(**dict(record))
        maximum = max(
            Decimal(leaf.contraction_upper)
            for leaf in leaves
            if leaf.proof_kind == "full_operator_neumann"
        )
        matching = next(
            (
                leaf
                for leaf in leaves
                if leaf.root_id == worst.root_id and leaf.path == worst.path
            ),
            None,
        )
        if (
            matching is None
            or Decimal(matching.contraction_upper) != maximum
            or Decimal(worst.contraction_upper) != maximum
        ):
            raise ValueError("outer checkpoint worst cell is not maximal")
        rectangle = _rectangle_from_path(
            root_by_id[worst.root_id], worst.path
        )
        for name, expected in _rectangle_record(rectangle).items():
            if name in ("root_id", "path"):
                continue
            if getattr(worst, name) != expected:
                raise ValueError("outer checkpoint worst geometry changed")
    elif worst_value is not None:
        raise ValueError("outer checkpoint has a worst cell without Neumann leaves")

    return _CoverCheckpointState(
        pending=tuple(pending),
        leaves=tuple(leaves),
        local_leaf_count=local_count,
        neumann_leaf_count=neumann_count,
        processed=processed,
        deepest=deepest,
        worst=worst,
    )


def _derive_nested_outer_ball(
    repository: Path,
    precision: int,
) -> _NestedOrbitBall:
    """Re-evaluate the fixed-parameter orbit majorant at a smaller radius.

    The outer source constructs ``Z1,Z2,Z3`` uniformly on its stated
    maximum radius, rather than only at its selected endpoint.  Hence the
    same source-registered centre-parameter majorant

        q(r) = Z0 + Z1 r + Z2 r^2 + Z3 r^3

    may be evaluated at every ``0 <= r <= 1e-5``.  A negative radii
    polynomial at ``r=1e-8`` proves that the exact centre orbit lies in the
    nested ball; no midpoint inverse or nonlinear estimate is replaced.
    This implication is only for the fixed centre parameters.  It does not
    promote the separate common-parameter-box continuation theorem.
    """

    _, evidence = load_validated_leaky_orbit_evidence(repository, BRANCH)
    path = repository.resolve() / evidence.source_result
    if _sha256_path(path) != EXPECTED_OUTER_RESULT_SHA256:
        raise ValueError("the fixed-parameter outer source hash changed")
    payload = json.loads(path.read_text(encoding="utf-8"))
    artifact = _mapping(payload.get("artifact"), "outer source artifact")
    if evidence.source_artifact_sha256 != EXPECTED_OUTER_ARTIFACT_SHA256:
        raise ValueError("the fixed-parameter outer artifact changed")
    wrapper = _mapping(
        artifact.get("directed_radii_certificate"), "outer radii wrapper"
    )
    settings = _mapping(wrapper.get("settings"), "outer radii settings")
    validation = _mapping(wrapper.get("validation"), "outer radii validation")
    for name in (
        "periodic_rfde_orbit_validated",
        "phase_bordered_rfde_inverse_validated",
        "directed_radii_inequality_candidate_closed",
        "formula_adaptation_independently_audited",
    ):
        if validation.get(name) is not True:
            raise ValueError(f"the fixed outer radii gate is absent: {name}")
    if validation.get("branch") != BRANCH:
        raise ValueError("the nested-ball parent branch changed")
    finite = _mapping(validation.get("finite"), "outer radii finite block")
    blocks = _mapping(validation.get("blocks"), "outer radii point blocks")
    correction = _mapping(
        validation.get("correction"), "outer radii correction"
    )
    if settings.get("precision_bits") != precision:
        raise ValueError("the nested-ball parent precision changed")

    validity = str(correction["maximum_radius"])
    if validity != str(settings.get("maximum_radius")):
        raise ValueError("the source majorant validity radius is inconsistent")
    radius = DirectedInterval.from_decimal(
        NESTED_OUTER_CORRECTION_RADIUS, precision
    )
    validity_interval = DirectedInterval.from_decimal(validity, precision)
    if radius.upper > validity_interval.lower:
        raise ValueError("the proposed nested radius exceeds parent validity")
    names = {
        "residual": (finite, "preconditioned_residual_l1_upper"),
        "z0": (blocks, "full_point_defect_upper"),
        "z1": (correction, "coefficient_z1_upper"),
        "z2": (correction, "coefficient_z2_upper"),
        "z3": (correction, "coefficient_z3_upper"),
    }
    text_values = {
        key: str(record[name]) for key, (record, name) in names.items()
    }
    intervals = {
        key: DirectedInterval.from_decimal(value, precision)
        for key, value in text_values.items()
    }
    if any(interval.lower < 0 for interval in intervals.values()):
        raise ValueError("a nested-ball majorant coefficient became negative")
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        r = radius.upper
        contraction = (
            intervals["z0"].upper
            + intervals["z1"].upper * r
            + intervals["z2"].upper * r * r
            + intervals["z3"].upper * r * r * r
        )
        radii_left = intervals["residual"].upper + contraction * r
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        margin = radius.lower - radii_left
    if not contraction < 1 or not margin > 0:
        raise ArithmeticError("the nested outer radii polynomial did not close")
    return _NestedOrbitBall(
        radius=radius,
        validity_radius=validity,
        residual_upper=text_values["residual"],
        z0_upper=text_values["z0"],
        z1_upper=text_values["z1"],
        z2_upper=text_values["z2"],
        z3_upper=text_values["z3"],
        contraction_upper=decimal_upper(contraction),
        radii_left_upper=decimal_upper(radii_left),
        margin_lower=decimal_lower(margin),
    )


def _validate_sources(
    repository: Path,
    riesz_payload: Mapping[str, Any],
    *,
    replay_parent: bool = True,
) -> tuple[Any, Any, Mapping[str, Any]]:
    repository = repository.resolve()
    shared_path = repository / "src/canard_control/floquet_cover_arithmetic.py"
    if _sha256_path(shared_path) != EXPECTED_SHARED_ARITHMETIC_SHA256:
        raise ValueError("the phase-neutral shared Floquet arithmetic changed")
    riesz_path = repository / RIESZ_RESULT_RELATIVE_PATH
    if _sha256_path(riesz_path) != EXPECTED_RIESZ_RESULT_SHA256:
        raise ValueError("the leaky Riesz parent hash changed")
    if replay_parent:
        validate_leaky_floquet_riesz_result(riesz_payload, repository)
    manifest = _mapping(riesz_payload.get("manifest"), "Riesz manifest")
    if manifest.get("artifact_sha256") != EXPECTED_RIESZ_ARTIFACT_SHA256:
        raise ValueError("the leaky Riesz artifact hash changed")
    if (
        manifest.get("floquet_parent_result")
        != FLOQUET_TRANSFER_RESULT_RELATIVE_PATH
        or manifest.get("floquet_parent_result_sha256")
        != EXPECTED_FLOQUET_TRANSFER_RESULT_SHA256
    ):
        raise ValueError("the Riesz neutral-Floquet parent changed")
    floquet_path = repository / FLOQUET_TRANSFER_RESULT_RELATIVE_PATH
    if _sha256_path(floquet_path) != EXPECTED_FLOQUET_TRANSFER_RESULT_SHA256:
        raise ValueError("the neutral-Floquet transfer result changed")
    floquet_payload = json.loads(floquet_path.read_text(encoding="utf-8"))
    floquet_manifest = _mapping(
        floquet_payload.get("manifest"), "neutral-Floquet manifest"
    )
    if (
        floquet_manifest.get("artifact_sha256")
        != EXPECTED_FLOQUET_TRANSFER_ARTIFACT_SHA256
    ):
        raise ValueError("the neutral-Floquet artifact changed")
    floquet_artifact = _mapping(
        floquet_payload.get("artifact"), "neutral-Floquet artifact"
    )
    floquet_branches = _mapping(
        floquet_artifact.get("branches"), "neutral-Floquet branches"
    )
    floquet_outer = _mapping(
        floquet_branches.get(BRANCH), "outer neutral-Floquet branch"
    )
    if (
        floquet_outer.get("neutral_multiplier_algebraically_simple_validated")
        is not True
        or floquet_outer.get("translation_jordan_vector_excluded") is not True
    ):
        raise ValueError("the outer translation root is not algebraically simple")
    artifact = _mapping(riesz_payload.get("artifact"), "Riesz artifact")
    theorem = _mapping(artifact.get("theorem"), "Riesz theorem")
    if theorem.get("leaky_recovery_row") != (
        "(d_theta+s)y_w-T*epsilon*y_v+T*epsilon*y_w"
    ):
        raise ValueError("the source Riesz pencil is not the leaky pencil")
    branches = _mapping(artifact.get("branches"), "Riesz branches")
    outer = _mapping(branches.get(BRANCH), "outer Riesz branch")
    for name in (
        "principal_logarithmic_strip_covers_all_nonzero_unstable_multipliers",
        "uniform_tail_block_invertible_on_closed_right_half_strip",
        "analytic_finite_schur_reduction_proved",
        "analytic_characteristic_multiplicity_preserved_by_schur_reduction",
        "outer_half_plane_excluded",
        "local_complex_punctured_half_disk_excluded",
    ):
        if outer.get(name) is not True:
            raise ValueError(f"the required outer Riesz theorem is absent: {name}")
    for name in (
        "remaining_compact_keyhole_boundary_invertibility_validated",
        "unstable_multiplier_count_validated",
        "outer_attracting_floquet_index_validated",
        "outer_nonlinear_attracting_block_validated",
        "physical_pulse_onset_validated",
    ):
        if outer.get(name) is not False:
            raise ValueError(f"the Riesz parent promoted an open claim: {name}")
    if outer.get("outer_real_part") != str(OUTER_REAL_PART):
        raise ValueError("the Riesz far-right boundary changed")
    orbit, evidence = load_validated_leaky_orbit_evidence(repository, BRANCH)
    if evidence.source_result_sha256 != EXPECTED_OUTER_RESULT_SHA256:
        raise ValueError("the source-validated outer orbit hash changed")
    if evidence.source_result_sha256 != outer.get("source_result_sha256"):
        raise ValueError("the Riesz parent and outer orbit differ")
    if evidence.candidate_fingerprint != outer.get("candidate_fingerprint"):
        raise ValueError("the Riesz parent and outer orbit fingerprint differ")
    if evidence.correction_radius != outer.get("correction_radius"):
        raise ValueError("the Riesz parent and outer correction radius differ")
    return orbit, evidence, outer


def _stress_replay_worst_cell(
    orbit: Any,
    worst: WorstCoverCell | None,
    phase_upper: Decimal,
) -> _StressReplay:
    """Re-run the limiting cell at 256 bits and on four finer cells."""

    stress_precision = 256
    if worst is None:
        return _StressReplay(stress_precision, None, None, False)
    roots = {
        root.root_id: root for root in _root_rectangles(phase_upper)
    }
    if worst.root_id not in roots:
        raise ValueError("the stress cell has an unknown root")
    rectangle = _rectangle_from_path(roots[worst.root_id], worst.path)
    base = _build_leaky_base_sequences(orbit, stress_precision)
    candidate = _prepare_outer_candidate(orbit, base, stress_precision)
    correction = DirectedInterval.from_decimal(
        NESTED_OUTER_CORRECTION_RADIUS, stress_precision
    )
    same = _validate_cell(
        rectangle,
        candidate,
        base,
        correction,
        stress_precision,
        Decimal("0.999999999999"),
    )
    children: list[_Rectangle] = []
    for child in _split_rectangle(rectangle):
        children.extend(_split_rectangle(child))
    finer = [
        _validate_cell(
            child,
            candidate,
            base,
            correction,
            stress_precision,
            Decimal("0.999999999999"),
        )
        for child in children
    ]
    same_upper = same.worst.contraction_upper
    finer_upper = max(
        (Decimal(item.worst.contraction_upper) for item in finer),
        default=Decimal("Infinity"),
    )
    strict = Decimal(same_upper) < 1 and finer_upper < 1
    return _StressReplay(
        precision_bits=stress_precision,
        same_cell_upper=same_upper,
        finer_split_upper=format(finer_upper, "f"),
        strict=strict,
    )


def build_outer_right_half_cover(
    repository: Path,
    riesz_payload: Mapping[str, Any],
    *,
    precision: int = PRECISION_BITS,
    acceptance_threshold: str = str(ACCEPTANCE_THRESHOLD),
    maximum_processed_cells: int = MAXIMUM_PROCESSED_CELLS,
    maximum_depth: int = MAXIMUM_DEPTH,
    replay_parent: bool = True,
    progress: Callable[[int, int, int], None] | None = None,
    resume_checkpoint: Mapping[str, Any] | None = None,
    checkpoint_interval: int = 1000,
    checkpoint_callback: Callable[[dict[str, Any]], None] | None = None,
) -> OuterRightHalfCoverCertificate:
    """Build a complete proof or an explicit source-bound failure cover."""

    repository = repository.resolve()
    checkpoint_source_hashes = {
        relative: _sha256_path(repository / relative)
        for relative in SOURCE_MANIFEST
    }
    orbit, evidence, riesz = _validate_sources(
        repository, riesz_payload, replay_parent=replay_parent
    )
    if precision != PRECISION_BITS:
        raise ValueError("the theorem precision is pinned at 160 bits")
    threshold = Decimal(acceptance_threshold)
    if not Decimal(0) < threshold < Decimal(1):
        raise ValueError("the acceptance threshold must lie in (0,1)")
    if maximum_processed_cells < 1 or maximum_depth < 1:
        raise ValueError("the cover budgets must be positive")
    if checkpoint_interval < 1:
        raise ValueError("the checkpoint interval must be positive")
    nested_ball = _derive_nested_outer_ball(repository, precision)
    _binary_environment_checked()
    base = _build_leaky_base_sequences(orbit, precision)
    correction_radius = nested_ball.radius
    candidate = _prepare_outer_candidate(orbit, base, precision)
    local_radius = Decimal(str(riesz["local_complex_exclusion_radius_lower"]))
    keyhole_radius = Decimal(str(riesz["local_keyhole_radius"]))
    # Use the same outward decimal endpoint for construction, serialization,
    # and replay.  A plain ``str(mpfr)`` is only a round-trip representation
    # and need not lie above the MPFR value; mixing the two would leave a tiny
    # unproved seam at pi and reconstruct a different dyadic tree.
    phase_upper = Decimal(decimal_upper(pi_interval(precision).upper))
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        maximum_slow_real = (
            gmpy2.mpfr(str(OUTER_REAL_PART))
            + (base.period.upper + correction_radius.upper)
            * base.parameters["epsilon"].upper
        )
        nearest_tail_frequency = 129 * pi_interval(precision).lower
        monotonicity = (
            (DirectedInterval.from_decimal(2, precision).sqrt().upper - 1)
            * maximum_slow_real
            < nearest_tail_frequency
        )
    if not monotonicity:
        raise ArithmeticError("the shifted slow tail inverse is not monotone")

    roots = _root_rectangles(phase_upper)
    rectilinear_partition = _rectilinear_root_partition_validated(
        roots, phase_upper, local_radius
    )
    if not rectilinear_partition:
        raise ArithmeticError("the rectilinear neutral-core partition failed")
    if resume_checkpoint is None:
        pending = list(reversed(roots))
        leaves: list[CoverLeaf] = []
        local_leaf_count = 0
        neumann_leaf_count = 0
        worst: WorstCoverCell | None = None
        processed = 0
        deepest = 0
    else:
        restored = _restore_cover_checkpoint(
            resume_checkpoint,
            repository,
            roots=roots,
            candidate_fingerprint=evidence.candidate_fingerprint,
            precision=precision,
            threshold=threshold,
            maximum_depth=maximum_depth,
            phase_upper=phase_upper,
            local_radius=local_radius,
            keyhole_radius=keyhole_radius,
        )
        pending = list(restored.pending)
        leaves = list(restored.leaves)
        local_leaf_count = restored.local_leaf_count
        neumann_leaf_count = restored.neumann_leaf_count
        worst = restored.worst
        processed = restored.processed
        deepest = restored.deepest
    blocking: WorstCoverCell | None = None

    def emit_checkpoint() -> None:
        if checkpoint_callback is None:
            return
        checkpoint_callback(
            _cover_checkpoint(
                repository,
                roots=roots,
                candidate_fingerprint=evidence.candidate_fingerprint,
                precision=precision,
                threshold=threshold,
                maximum_depth=maximum_depth,
                phase_upper=phase_upper,
                local_radius=local_radius,
                keyhole_radius=keyhole_radius,
                pending=pending,
                leaves=leaves,
                local_leaf_count=local_leaf_count,
                neumann_leaf_count=neumann_leaf_count,
                processed=processed,
                deepest=deepest,
                worst=worst,
                source_sha256=checkpoint_source_hashes,
            )
        )

    while pending and processed < maximum_processed_cells:
        rectangle = pending.pop()
        depth = len(rectangle.path) // 2
        deepest = max(deepest, depth)
        # Exactly one root is owned by the source-validated punctured disk
        # (with s=0 supplied by algebraic simplicity of translation).  The
        # two complementary roots always use the full-operator estimate,
        # even when a later descendant lies geometrically in the disk.  This
        # fixed ownership is what removes the non-dyadic circular seam.
        if _rectangle_is_neutral_core_root(rectangle):
            leaves.append(
                CoverLeaf(
                    root_id=rectangle.root_id,
                    path=rectangle.path,
                    proof_kind="riesz_local_disk",
                    contraction_upper="0",
                    finite_input_column_sum_upper="0",
                    tail_input_column_sum_upper="0",
                )
            )
            local_leaf_count += 1
            processed += 1
            if progress is not None and processed % 100 == 0:
                progress(processed, len(leaves), len(pending))
            if processed % checkpoint_interval == 0:
                emit_checkpoint()
            continue
        if rectangle.root_id == "neutral_core":
            raise ArithmeticError("the locally owned neutral core was split")
        bounds = _validate_cell(
            rectangle,
            candidate,
            base,
            correction_radius,
            precision,
            threshold,
        )
        processed += 1
        if bounds.validated:
            leaves.append(bounds.leaf)
            neumann_leaf_count += 1
            if worst is None or Decimal(bounds.worst.contraction_upper) > Decimal(
                worst.contraction_upper
            ):
                worst = bounds.worst
        else:
            if depth >= maximum_depth:
                blocking = bounds.worst
                pending.append(rectangle)
                break
            first, second = _split_rectangle(rectangle)
            pending.extend((second, first))
        if progress is not None and processed % 100 == 0:
            progress(processed, len(leaves), len(pending))
        if processed % checkpoint_interval == 0:
            emit_checkpoint()

    if checkpoint_callback is not None:
        emit_checkpoint()

    complete = not pending
    prefix = complete and _prefix_complete(
        leaves, tuple(root.root_id for root in roots)
    )
    maximum_contraction = max(
        (Decimal(leaf.contraction_upper) for leaf in leaves), default=None
    )
    minimum_margin = (
        None
        if maximum_contraction is None
        else _margin(format(maximum_contraction, "f"))
    )
    every_leaf_strict = bool(leaves) and all(
        Decimal(leaf.contraction_upper) < 1 for leaf in leaves
    )
    normalized_area = _normalized_area_fraction(leaves, roots)
    zero_free = (
        complete
        and prefix
        and every_leaf_strict
        and monotonicity
        and rectilinear_partition
        and normalized_area == "1"
    )
    stress = (
        _stress_replay_worst_cell(orbit, worst, phase_upper)
        if zero_free
        else _StressReplay(256, None, None, False)
    )
    zero_free = zero_free and stress.strict
    leaf_digest = _leaf_digest(leaves)
    if (
        zero_free
        and isinstance(EXPECTED_COMPLETE_LEAF_PARTITION_SHA256, str)
        and leaf_digest != EXPECTED_COMPLETE_LEAF_PARTITION_SHA256
    ):
        raise ValueError("the complete outer leaf partition changed")
    reason = None
    if not zero_free:
        reason = (
            f"directed cover incomplete: processed={processed}, "
            f"accepted={len(leaves)}, pending={len(pending)}; "
            + (
                "blocking contraction=" + blocking.contraction_upper + "; "
                if blocking is not None
                else ""
            )
            + (
                "256-bit finer-split stress replay failed; "
                if complete and prefix and every_leaf_strict and not stress.strict
                else ""
            )
            + "the outer index remains open"
        )
    flags = {name: zero_free for name in TRUE_ON_COMPLETE}
    return OuterRightHalfCoverCertificate(
        schema_id=SCHEMA_ID,
        model_id=MODEL_ID,
        branch=BRANCH,
        riesz_result_sha256=EXPECTED_RIESZ_RESULT_SHA256,
        riesz_artifact_sha256=EXPECTED_RIESZ_ARTIFACT_SHA256,
        outer_orbit_result_sha256=EXPECTED_OUTER_RESULT_SHA256,
        outer_orbit_artifact_sha256=EXPECTED_OUTER_ARTIFACT_SHA256,
        candidate_fingerprint=evidence.candidate_fingerprint,
        source_orbit_correction_radius=evidence.correction_radius,
        correction_radius=NESTED_OUTER_CORRECTION_RADIUS,
        nested_ball_majorant_validity_radius=nested_ball.validity_radius,
        nested_ball_preconditioned_residual_upper=nested_ball.residual_upper,
        nested_ball_coefficient_z0_upper=nested_ball.z0_upper,
        nested_ball_coefficient_z1_upper=nested_ball.z1_upper,
        nested_ball_coefficient_z2_upper=nested_ball.z2_upper,
        nested_ball_coefficient_z3_upper=nested_ball.z3_upper,
        nested_ball_contraction_upper=nested_ball.contraction_upper,
        nested_ball_radii_left_upper=nested_ball.radii_left_upper,
        nested_ball_radii_margin_lower=nested_ball.margin_lower,
        precision_bits=precision,
        norm_id="complex-component-wiener-l1-split-re-im",
        delay_operator_representation=(
            "unshifted-coefficient-output-phase; equivalently "
            "delay-shifted-coefficient-input-phase"
        ),
        period_correction_frequency_representation=(
            "total-output-mode phase for S_alpha M_b"
        ),
        fourier_cutoff=FOURIER_CUTOFF,
        coefficient_support_half_bandwidth=COEFFICIENT_SUPPORT_RADIUS,
        complex_finite_dimension=2 * (2 * FOURIER_CUTOFF + 1),
        outer_real_part=str(OUTER_REAL_PART),
        upper_phase_lower="0",
        upper_phase_upper=decimal_upper(pi_interval(precision).upper),
        local_complex_exclusion_radius_lower=str(local_radius),
        parent_local_keyhole_radius=str(keyhole_radius),
        neutral_core_size=str(NEUTRAL_CORE_SIZE),
        neutral_core_disk_squared_margin_fraction=_fraction_text(
            _neutral_core_disk_squared_margin_fraction(local_radius)
        ),
        tail_inverse_monotonicity_condition_validated=monotonicity,
        root_rectangle_count=len(roots),
        accepted_leaf_count=len(leaves),
        local_disk_leaf_count=local_leaf_count,
        neumann_leaf_count=neumann_leaf_count,
        processed_cell_count=processed,
        pending_cell_count=len(pending),
        accepted_normalized_area_fraction=normalized_area,
        maximum_depth=deepest,
        acceptance_threshold=str(threshold),
        maximum_contraction_upper=(
            None
            if maximum_contraction is None
            else format(maximum_contraction, "f")
        ),
        minimum_contraction_margin_lower=minimum_margin,
        stress_replay_precision_bits=stress.precision_bits,
        worst_cell_stress_contraction_upper=stress.same_cell_upper,
        worst_cell_finer_split_stress_maximum_contraction_upper=(
            stress.finer_split_upper
        ),
        worst_cell_finer_split_stress_strict=stress.strict,
        leaf_partition_sha256=leaf_digest,
        directed_outer_nontranslation_right_half_zero_count=(
            0 if zero_free else None
        ),
        **flags,
        **{name: False for name in ALWAYS_FALSE},
        leaves=tuple(sorted(leaves, key=lambda item: (item.root_id, item.path))),
        worst_cell=worst if worst is not None else blocking,
        failure_reason=reason,
    )


def validate_outer_right_half_checkpoint(
    payload: Mapping[str, Any],
    repository: Path,
    *,
    riesz_payload: Mapping[str, Any] | None = None,
    precision: int = PRECISION_BITS,
    acceptance_threshold: str = str(ACCEPTANCE_THRESHOLD),
    maximum_depth: int = MAXIMUM_DEPTH,
    replay_parent: bool = False,
) -> None:
    """Validate a resumable execution frontier without promoting a claim."""

    repository = repository.resolve()
    if riesz_payload is None:
        riesz_payload = json.loads(
            (repository / RIESZ_RESULT_RELATIVE_PATH).read_text(
                encoding="utf-8"
            )
        )
    _, evidence, riesz = _validate_sources(
        repository, riesz_payload, replay_parent=replay_parent
    )
    if precision != PRECISION_BITS:
        raise ValueError("the theorem precision is pinned at 160 bits")
    threshold = Decimal(acceptance_threshold)
    if not Decimal(0) < threshold < Decimal(1):
        raise ValueError("the acceptance threshold must lie in (0,1)")
    phase_upper = Decimal(decimal_upper(pi_interval(precision).upper))
    roots = _root_rectangles(phase_upper)
    _restore_cover_checkpoint(
        payload,
        repository,
        roots=roots,
        candidate_fingerprint=evidence.candidate_fingerprint,
        precision=precision,
        threshold=threshold,
        maximum_depth=maximum_depth,
        phase_upper=phase_upper,
        local_radius=Decimal(
            str(riesz["local_complex_exclusion_radius_lower"])
        ),
        keyhole_radius=Decimal(str(riesz["local_keyhole_radius"])),
    )


def build_outer_right_half_result(
    repository: Path,
    *,
    maximum_processed_cells: int = MAXIMUM_PROCESSED_CELLS,
    progress: Callable[[int, int, int], None] | None = None,
    resume_checkpoint: Mapping[str, Any] | None = None,
    checkpoint_interval: int = 1000,
    checkpoint_callback: Callable[[dict[str, Any]], None] | None = None,
) -> dict[str, Any]:
    repository = repository.resolve()
    initial_sources = {
        relative: _sha256_path(repository / relative)
        for relative in SOURCE_MANIFEST
    }
    riesz_path = repository / RIESZ_RESULT_RELATIVE_PATH
    riesz_payload = json.loads(riesz_path.read_text(encoding="utf-8"))
    # Normalize tuple-valued dataclass fields to their tracked JSON form before
    # the in-memory replay.  In particular, ``leaves`` must have exactly the
    # same list representation here and after ``json.loads`` of the artifact.
    certificate = json.loads(
        json.dumps(
            asdict(
                build_outer_right_half_cover(
                    repository,
                    riesz_payload,
                    maximum_processed_cells=maximum_processed_cells,
                    progress=progress,
                    resume_checkpoint=resume_checkpoint,
                    checkpoint_interval=checkpoint_interval,
                    checkpoint_callback=checkpoint_callback,
                )
            ),
            ensure_ascii=True,
        )
    )
    sources = {
        relative: _sha256_path(repository / relative)
        for relative in SOURCE_MANIFEST
    }
    if sources != initial_sources:
        raise ValueError("outer right-half sources changed during generation")
    result = {
        "certificate": certificate,
        "scope": {
            "outer_nontranslation_right_half_zero_count": certificate[
                "directed_outer_nontranslation_right_half_zero_count"
            ],
            "outer_attracting_floquet_index_validated": certificate[
                "outer_attracting_floquet_index_validated"
            ],
            "center_parameter_outer_floquet_count_validated": certificate[
                "center_parameter_outer_floquet_count_validated"
            ],
            "parameter_box_uniform_outer_floquet_count_validated": False,
            "outer_nonlinear_attracting_block_validated": False,
            "inner_saddle_floquet_index_validated": False,
            "history_space_separator_validated": False,
            "physical_pulse_onset_validated": False,
        },
    }
    result["manifest"] = {
        "schema_id": SCHEMA_ID,
        "result": RESULT_RELATIVE_PATH,
        "default_command": DEFAULT_COMMAND,
        "arithmetic_scope": ARITHMETIC_SCOPE,
        "certificate_sha256": canonical_sha256(certificate),
        "source_sha256": sources,
        "riesz_result": RIESZ_RESULT_RELATIVE_PATH,
        "riesz_result_sha256": _sha256_path(riesz_path),
        "outer_orbit_result": str(
            json.loads(riesz_path.read_text(encoding="utf-8"))["artifact"]
            ["branches"][BRANCH]["source_result"]
        ),
        "outer_orbit_result_sha256": EXPECTED_OUTER_RESULT_SHA256,
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "gmpy2": gmpy2.__version__,
            "mpfr": gmpy2.mpfr_version(),
            "numpy_blas": np.__config__.CONFIG.get("Build Dependencies", {}).get(
                "blas", {}
            ),
        },
    }
    return result


def validate_outer_right_half_result(
    payload: Mapping[str, Any], repository: Path, *, validate_parent: bool = True
) -> None:
    if not isinstance(payload, Mapping) or set(payload) != {
        "certificate",
        "scope",
        "manifest",
    }:
        raise ValueError("outer right-half result has the wrong outer schema")
    certificate = payload.get("certificate")
    scope = payload.get("scope")
    manifest = payload.get("manifest")
    if not all(isinstance(item, Mapping) for item in (certificate, scope, manifest)):
        raise ValueError("outer right-half result records must be mappings")
    assert isinstance(certificate, Mapping)
    assert isinstance(scope, Mapping)
    assert isinstance(manifest, Mapping)
    if set(certificate) != {
        field.name for field in fields(OuterRightHalfCoverCertificate)
    }:
        raise ValueError("outer right-half certificate schema changed")
    fixed = {
        "schema_id": SCHEMA_ID,
        "model_id": MODEL_ID,
        "branch": BRANCH,
        "riesz_result_sha256": EXPECTED_RIESZ_RESULT_SHA256,
        "riesz_artifact_sha256": EXPECTED_RIESZ_ARTIFACT_SHA256,
        "outer_orbit_result_sha256": EXPECTED_OUTER_RESULT_SHA256,
        "outer_orbit_artifact_sha256": EXPECTED_OUTER_ARTIFACT_SHA256,
        "source_orbit_correction_radius": "1e-5",
        "correction_radius": NESTED_OUTER_CORRECTION_RADIUS,
        "precision_bits": PRECISION_BITS,
        "norm_id": "complex-component-wiener-l1-split-re-im",
        "delay_operator_representation": (
            "unshifted-coefficient-output-phase; equivalently "
            "delay-shifted-coefficient-input-phase"
        ),
        "period_correction_frequency_representation": (
            "total-output-mode phase for S_alpha M_b"
        ),
        "fourier_cutoff": FOURIER_CUTOFF,
        "coefficient_support_half_bandwidth": COEFFICIENT_SUPPORT_RADIUS,
        "complex_finite_dimension": 258,
        "outer_real_part": str(OUTER_REAL_PART),
        "upper_phase_lower": "0",
        "upper_phase_upper": decimal_upper(
            pi_interval(PRECISION_BITS).upper
        ),
        "neutral_core_size": str(NEUTRAL_CORE_SIZE),
        "root_rectangle_count": 3,
        "acceptance_threshold": str(ACCEPTANCE_THRESHOLD),
        "stress_replay_precision_bits": 256,
    }
    if any(certificate.get(name) != expected for name, expected in fixed.items()):
        raise ValueError("outer right-half fixed theorem data changed")
    nested_ball = _derive_nested_outer_ball(repository, PRECISION_BITS)
    nested_expected = {
        "nested_ball_majorant_validity_radius": nested_ball.validity_radius,
        "nested_ball_preconditioned_residual_upper": nested_ball.residual_upper,
        "nested_ball_coefficient_z0_upper": nested_ball.z0_upper,
        "nested_ball_coefficient_z1_upper": nested_ball.z1_upper,
        "nested_ball_coefficient_z2_upper": nested_ball.z2_upper,
        "nested_ball_coefficient_z3_upper": nested_ball.z3_upper,
        "nested_ball_contraction_upper": nested_ball.contraction_upper,
        "nested_ball_radii_left_upper": nested_ball.radii_left_upper,
        "nested_ball_radii_margin_lower": nested_ball.margin_lower,
    }
    if any(
        certificate.get(name) != expected
        for name, expected in nested_expected.items()
    ):
        raise ValueError("the derived nested outer orbit ball changed")
    if certificate.get("tail_inverse_monotonicity_condition_validated") is not True:
        raise ValueError("the shifted tail inverse monotonicity gate failed")
    if any(certificate.get(name) is not False for name in ALWAYS_FALSE):
        raise ValueError("an open outer/onset claim was promoted")
    leaves_value = certificate.get("leaves")
    if not isinstance(leaves_value, list):
        raise ValueError("outer right-half leaves must be a list")
    leaf_fields = {field.name for field in fields(CoverLeaf)}
    leaves = []
    for value in leaves_value:
        record = _mapping(value, "cover leaf")
        if set(record) != leaf_fields:
            raise ValueError("outer right-half leaf schema changed")
        leaves.append(CoverLeaf(**dict(record)))
    if len(leaves) != certificate.get("accepted_leaf_count"):
        raise ValueError("outer right-half leaf count changed")
    if len({(leaf.root_id, leaf.path) for leaf in leaves}) != len(leaves):
        raise ValueError("outer right-half leaves are not unique")
    actual_maximum_depth = max(
        (len(leaf.path) // 2 for leaf in leaves), default=0
    )
    if certificate.get("maximum_depth") != actual_maximum_depth:
        raise ValueError("the outer cover maximum depth changed")
    if _leaf_digest(leaves) != certificate.get("leaf_partition_sha256"):
        raise ValueError("outer right-half leaf digest changed")
    if not isinstance(EXPECTED_COMPLETE_LEAF_PARTITION_SHA256, str):
        raise ValueError("the complete outer leaf partition is not registered")
    roots = {
        root.root_id: root
        for root in _root_rectangles(
            Decimal(str(certificate["upper_phase_upper"]))
        )
    }
    if _normalized_area_fraction(leaves, tuple(roots.values())) != certificate.get(
        "accepted_normalized_area_fraction"
    ):
        raise ValueError("the accepted normalized cover area changed")
    local_radius = Decimal(
        str(certificate["local_complex_exclusion_radius_lower"])
    )
    if local_radius <= 0:
        raise ValueError("the local Riesz exclusion radius is not positive")
    expected_core_margin = _fraction_text(
        _neutral_core_disk_squared_margin_fraction(local_radius)
    )
    if certificate.get(
        "neutral_core_disk_squared_margin_fraction"
    ) != expected_core_margin:
        raise ValueError("the neutral-core disk margin changed")
    if not _rectilinear_root_partition_validated(
        tuple(roots.values()),
        Decimal(str(certificate["upper_phase_upper"])),
        local_radius,
    ):
        raise ValueError("the rectilinear outer root partition changed")
    local_count = 0
    neumann_count = 0
    for leaf in leaves:
        if leaf.root_id not in roots:
            raise ValueError("an outer cover leaf has an unknown root")
        rectangle = _rectangle_from_path(roots[leaf.root_id], leaf.path)
        contraction = Decimal(leaf.contraction_upper)
        finite = Decimal(leaf.finite_input_column_sum_upper)
        tail = Decimal(leaf.tail_input_column_sum_upper)
        if min(contraction, finite, tail) < 0:
            raise ValueError("an outer leaf bound became negative")
        if leaf.proof_kind == "riesz_local_disk":
            local_count += 1
            if (contraction, finite, tail) != (Decimal(0),) * 3:
                raise ValueError("a local-disk leaf contains Neumann data")
            if not _rectangle_is_neutral_core_root(rectangle):
                raise ValueError(
                    "a local-disk leaf is not the neutral-core root"
                )
        elif leaf.proof_kind == "full_operator_neumann":
            neumann_count += 1
            if contraction != max(finite, tail):
                raise ValueError("an outer Neumann contraction is inconsistent")
            if contraction <= 0:
                raise ValueError("an outer Neumann leaf has no strict proof data")
            if rectangle.root_id == "neutral_core":
                raise ValueError("the neutral core was misclassified as Neumann")
        else:
            raise ValueError("an outer leaf has an unknown proof kind")
    if local_count != certificate.get("local_disk_leaf_count"):
        raise ValueError("the local-disk leaf count changed")
    if local_count != 1:
        raise ValueError("the cover must have exactly one neutral-core local leaf")
    if neumann_count != certificate.get("neumann_leaf_count"):
        raise ValueError("the Neumann leaf count changed")
    if local_count + neumann_count != len(leaves):
        raise ValueError("the outer proof-kind partition changed")
    complete = certificate.get("pending_cell_count") == 0
    prefix = complete and _prefix_complete(
        leaves, tuple(roots)
    )
    zero_free = bool(
        certificate.get("complete_nontranslation_right_half_strip_zero_free_validated")
    )
    if zero_free and certificate.get("leaf_partition_sha256") != (
        EXPECTED_COMPLETE_LEAF_PARTITION_SHA256
    ):
        raise ValueError("the registered outer leaf partition changed")
    worst_object: WorstCoverCell | None = None
    if zero_free:
        if certificate.get("failure_reason") is not None:
            raise ValueError("a completed outer cover retained a failure reason")
        if not prefix:
            raise ValueError("the promoted outer cover is not prefix-complete")
        if certificate.get("accepted_normalized_area_fraction") != "1":
            raise ValueError("the promoted upper rectangle has an area gap")
        if certificate.get("processed_cell_count") != (
            2 * len(leaves) - len(roots)
        ):
            raise ValueError("the outer binary-forest count changed")
        if certificate.get("worst_cell_finer_split_stress_strict") is not True:
            raise ValueError("the promoted outer stress replay is not strict")
        for name in (
            "worst_cell_stress_contraction_upper",
            "worst_cell_finer_split_stress_maximum_contraction_upper",
        ):
            value = certificate.get(name)
            if value is None or Decimal(str(value)) >= 1:
                raise ValueError("a promoted outer stress bound is non-strict")
        maximum = max(Decimal(leaf.contraction_upper) for leaf in leaves)
        if maximum >= 1 or maximum > ACCEPTANCE_THRESHOLD:
            raise ValueError("a promoted outer cover leaf is non-strict")
        if format(maximum, "f") != certificate.get("maximum_contraction_upper"):
            raise ValueError("the outer maximum contraction changed")
        if _margin(format(maximum, "f")) != certificate.get(
            "minimum_contraction_margin_lower"
        ):
            raise ValueError("the outer contraction margin changed")
        if any(
            Decimal(leaf.contraction_upper) > ACCEPTANCE_THRESHOLD
            for leaf in leaves
            if leaf.proof_kind == "full_operator_neumann"
        ):
            raise ValueError("a promoted Neumann leaf exceeds the threshold")
        if any(certificate.get(name) is not True for name in TRUE_ON_COMPLETE):
            raise ValueError("a required completed-cover flag is absent")
        if certificate.get("directed_outer_nontranslation_right_half_zero_count") != 0:
            raise ValueError("the completed outer zero count is not zero")
        worst = _mapping(certificate.get("worst_cell"), "worst outer cell")
        if set(worst) != {field.name for field in fields(WorstCoverCell)}:
            raise ValueError("the detailed worst outer cell schema changed")
        worst_object = WorstCoverCell(**dict(worst))
        if Decimal(str(worst.get("contraction_upper"))) != maximum:
            raise ValueError("the detailed worst outer cell is not maximal")
        root_id = str(worst.get("root_id"))
        if root_id not in roots:
            raise ValueError("the worst outer cell has an unknown root")
        reconstructed = _rectangle_from_path(
            roots[root_id], str(worst.get("path"))
        )
        for name, expected in {
            "sigma_lower": format(reconstructed.sigma_lower, "f"),
            "sigma_upper": format(reconstructed.sigma_upper, "f"),
            "phase_lower": format(reconstructed.phase_lower, "f"),
            "phase_upper": format(reconstructed.phase_upper, "f"),
        }.items():
            if worst.get(name) != expected:
                raise ValueError("the worst outer cell geometry changed")
    else:
        if any(certificate.get(name) is not False for name in TRUE_ON_COMPLETE):
            raise ValueError("an incomplete outer cover promoted a theorem flag")
        if certificate.get(
            "directed_outer_nontranslation_right_half_zero_count"
        ) is not None:
            raise ValueError("an incomplete outer cover inserted a zero count")
        if certificate.get("worst_cell_finer_split_stress_strict") is not False:
            raise ValueError("an incomplete outer cover promoted stress replay")
        if any(
            certificate.get(name) is not None
            for name in (
                "worst_cell_stress_contraction_upper",
                "worst_cell_finer_split_stress_maximum_contraction_upper",
            )
        ):
            raise ValueError("an incomplete outer cover inserted stress bounds")
    expected_scope = {
        "outer_nontranslation_right_half_zero_count": certificate.get(
            "directed_outer_nontranslation_right_half_zero_count"
        ),
        "outer_attracting_floquet_index_validated": certificate.get(
            "outer_attracting_floquet_index_validated"
        ),
        "center_parameter_outer_floquet_count_validated": certificate.get(
            "center_parameter_outer_floquet_count_validated"
        ),
        "parameter_box_uniform_outer_floquet_count_validated": False,
        "outer_nonlinear_attracting_block_validated": False,
        "inner_saddle_floquet_index_validated": False,
        "history_space_separator_validated": False,
        "physical_pulse_onset_validated": False,
    }
    if dict(scope) != expected_scope:
        raise ValueError("the outer right-half scope ledger changed")

    expected_manifest_keys = {
        "schema_id",
        "result",
        "default_command",
        "arithmetic_scope",
        "certificate_sha256",
        "source_sha256",
        "riesz_result",
        "riesz_result_sha256",
        "outer_orbit_result",
        "outer_orbit_result_sha256",
        "environment",
    }
    if set(manifest) != expected_manifest_keys:
        raise ValueError("outer right-half manifest schema changed")
    for name, expected in {
        "schema_id": SCHEMA_ID,
        "result": RESULT_RELATIVE_PATH,
        "default_command": DEFAULT_COMMAND,
        "arithmetic_scope": ARITHMETIC_SCOPE,
        "riesz_result": RIESZ_RESULT_RELATIVE_PATH,
        "riesz_result_sha256": EXPECTED_RIESZ_RESULT_SHA256,
        "outer_orbit_result": OUTER_ORBIT_RESULT_RELATIVE_PATH,
        "outer_orbit_result_sha256": EXPECTED_OUTER_RESULT_SHA256,
    }.items():
        if manifest.get(name) != expected:
            raise ValueError(f"outer right-half manifest {name} changed")
    if manifest.get("certificate_sha256") != canonical_sha256(certificate):
        raise ValueError("outer right-half certificate digest changed")
    repository = repository.resolve()
    hashes = manifest.get("source_sha256")
    if not isinstance(hashes, Mapping) or set(hashes) != set(SOURCE_MANIFEST):
        raise ValueError("outer right-half source manifest changed")
    for relative in SOURCE_MANIFEST:
        if hashes.get(relative) != _sha256_path(repository / relative):
            raise ValueError(f"outer right-half source hash changed: {relative}")
    environment = manifest.get("environment")
    if not isinstance(environment, Mapping):
        raise ValueError("outer right-half environment is absent")
    expected_environment = {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "gmpy2": gmpy2.__version__,
        "mpfr": gmpy2.mpfr_version(),
        "numpy_blas": np.__config__.CONFIG.get("Build Dependencies", {}).get(
            "blas", {}
        ),
    }
    if environment != expected_environment:
        raise ValueError("outer right-half environment changed")
    riesz_path = repository / RIESZ_RESULT_RELATIVE_PATH
    if _sha256_path(riesz_path) != EXPECTED_RIESZ_RESULT_SHA256:
        raise ValueError("the outer right-half Riesz parent hash changed")
    riesz_payload = json.loads(riesz_path.read_text(encoding="utf-8"))
    orbit, evidence, outer = _validate_sources(
        repository, riesz_payload, replay_parent=validate_parent
    )
    if certificate.get("candidate_fingerprint") != evidence.candidate_fingerprint:
        raise ValueError("the outer right-half orbit fingerprint changed")
    if certificate.get("source_orbit_correction_radius") != evidence.correction_radius:
        raise ValueError("the source outer correction radius changed")
    for name, expected in {
        "local_complex_exclusion_radius_lower": outer.get(
            "local_complex_exclusion_radius_lower"
        ),
        "parent_local_keyhole_radius": outer.get("local_keyhole_radius"),
    }.items():
        if certificate.get(name) != expected:
            raise ValueError(f"the Riesz-derived {name} changed")
    if zero_free:
        assert worst_object is not None
        roots = {
            root.root_id: root
            for root in _root_rectangles(
                Decimal(str(certificate["upper_phase_upper"]))
            )
        }
        rectangle = _rectangle_from_path(
            roots[worst_object.root_id], worst_object.path
        )
        replay_base = _build_leaky_base_sequences(orbit, PRECISION_BITS)
        replay_candidate = _prepare_outer_candidate(
            orbit, replay_base, PRECISION_BITS
        )
        replay_cell = _validate_cell(
            rectangle,
            replay_candidate,
            replay_base,
            DirectedInterval.from_decimal(
                NESTED_OUTER_CORRECTION_RADIUS, PRECISION_BITS
            ),
            PRECISION_BITS,
            ACCEPTANCE_THRESHOLD,
        )
        if not replay_cell.validated or asdict(replay_cell.worst) != dict(
            _mapping(certificate.get("worst_cell"), "worst outer cell")
        ):
            raise ValueError("the 160-bit worst-cell replay changed")
        replay = _stress_replay_worst_cell(
            orbit,
            worst_object,
            Decimal(str(certificate["upper_phase_upper"])),
        )
        for name, expected in {
            "stress_replay_precision_bits": replay.precision_bits,
            "worst_cell_stress_contraction_upper": replay.same_cell_upper,
            "worst_cell_finer_split_stress_maximum_contraction_upper": (
                replay.finer_split_upper
            ),
            "worst_cell_finer_split_stress_strict": replay.strict,
        }.items():
            if certificate.get(name) != expected:
                raise ValueError(f"the 256-bit stress replay changed: {name}")
