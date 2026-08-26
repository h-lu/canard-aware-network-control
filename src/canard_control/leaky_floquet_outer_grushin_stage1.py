"""Local pole subtraction at the neutral outer Floquet exponent.

This module constructs a fixed one-dimensional Grushin border for the
source-validated outer periodic orbit at ``s=0``.  The cutoff-64 singular
vectors are only binary64 guides for that border.  A directed finite/tail
Neumann argument subsequently validates the complete bordered Fourier
operator on a closed complex disk, including the mode-256 coefficient
support, the explicit coupling tail through mode 320, and the nested
``1e-8`` outer-orbit ball.

The scalar effective Hamiltonian is compared with its nonzero affine guide
on the boundary.  A full-disk Bloch-amplitude factor is included because the
circle crosses ``Re(s)<0``; the right-half-plane estimate
``|exp(-alpha*s)|<=1`` is not used there.  The complete bordered operator is
proved invertible, but the final scalar Rouche inequality is evaluated and
fails.  This file is therefore a Stage-1 failure contract, not a local root
count.

The parent theorem still excludes the punctured right half-disk of radius
``0.0028635...``.  The failed full-disk comparison does not weaken that
separate result, but it also cannot be used to enlarge it or to count the
remaining logarithmic keyhole.
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
    cos_interval,
    decimal_lower,
    decimal_upper,
    pi_interval,
    sin_interval,
    upward_sum,
)
from canard_control.floquet_cover_arithmetic import (
    _binary_coefficients,
    _binary_complex_matrix_split_l1_upper,
    _binary_complex_product_split_l1_upper,
    _coefficient_matrix,
    _formation_error,
)
from canard_control.leaky_floquet_inner_unstable_root import (
    _augment_derivative,
    _augment_finite,
    _augment_finite_tail,
    _augment_tail_finite,
    _binary_environment_checked,
    _coefficient_error_norms,
    _complex_abs_lower,
    _complex_abs_upper,
    _evaluate_blocks,
    _inverse_defect,
    _matrix_max_entry_upper,
    _nested_coefficient_variations,
    _product_norm,
    _row_dual_upper,
    _split_upper,
    _validate_physical_delay_oracle,
    _vector_l1_upper,
)
from canard_control.leaky_floquet_outer_right_half_cover import (
    _derive_nested_outer_ball,
    _validate_sources,
)
from canard_control.leaky_floquet_riesz_reduction import (
    RESULT_RELATIVE_PATH as RIESZ_RESULT_RELATIVE_PATH,
)
from canard_control.leaky_floquet_transfer import (
    RESULT_RELATIVE_PATH as FLOQUET_TRANSFER_RESULT_RELATIVE_PATH,
)
from canard_control.leaky_periodic_validation import (
    _build_leaky_base_sequences,
)


SCHEMA_ID = "leaky-floquet-outer-grushin-stage1-v1"
MODEL_ID = "autonomous-leaky-recovery-two-delay-fhn-bistable-proposal"
BRANCH = "outer_pulse"
SOURCE_RELATIVE_PATH = (
    "src/canard_control/leaky_floquet_outer_grushin_stage1.py"
)
GENERATOR_RELATIVE_PATH = (
    "experiments/leaky_floquet_outer_grushin_stage1.py"
)
NOTE_RELATIVE_PATH = "docs/leaky-floquet-outer-grushin-stage1.md"
TEST_RELATIVE_PATH = "tests/test_leaky_floquet_outer_grushin_stage1.py"
RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_floquet_outer_grushin_stage1.json"
)
DEFAULT_COMMAND = (
    "OPENBLAS_NUM_THREADS=8 PYTHONPATH=build/testdeps:src /usr/bin/python3 "
    "experiments/leaky_floquet_outer_grushin_stage1.py"
)
ARITHMETIC_SCOPE = (
    "160-bit outward MPFR bounds around exact stored binary64 outer Fourier "
    "data; fixed cutoff-64 SVD-guide borders at scales 20 and 5; complete "
    "finite/tail Grushin operator with physical unshifted-coefficient/output-"
    "row delay phases, mode-256 coefficient support, explicit coupling modes "
    "through 320, the nested 1e-8 orbit ball, full-disk Bloch-amplitude "
    "majorants, and a local scalar Rouche comparison at the exact translation "
    "exponent; no global outer Floquet or attraction claim"
)
SOURCE_MANIFEST = (
    SOURCE_RELATIVE_PATH,
    GENERATOR_RELATIVE_PATH,
    NOTE_RELATIVE_PATH,
    "src/canard_control/directed_interval.py",
    "src/canard_control/fhn_periodic_infinite_validation.py",
    "src/canard_control/floquet_cover_arithmetic.py",
    "src/canard_control/leaky_floquet_inner_unstable_root.py",
    "src/canard_control/leaky_floquet_outer_right_half_cover.py",
    "src/canard_control/leaky_floquet_riesz_reduction.py",
    "src/canard_control/leaky_floquet_transfer.py",
    "src/canard_control/leaky_periodic_validation.py",
)

PRECISION_BITS = 160
FOURIER_CUTOFF = 64
COEFFICIENT_SUPPORT_RADIUS = 256
EXPLICIT_COUPLING_TAIL_MAXIMUM_MODE = 320
ROOT_CENTER_BINARY64 = 0.0
ROOT_DISK_RADIUS = "0.0028"
BOUNDARY_ARC_COUNT = 64
RIGHT_BORDER_SCALE = 20.0
LEFT_BORDER_SCALE = 5.0
NESTED_ORBIT_RADIUS = "1e-8"
PINNED_OPENBLAS_NUM_THREADS = "8"

TRUE_FLAGS = (
    "source_validated_outer_orbit_ball_used",
    "source_validated_riesz_tail_and_multiplicity_reduction_used",
    "exact_translation_root_and_algebraic_simplicity_parent_used",
    "complex_modulus_wiener_grushin_norm_used",
    "physical_delay_dual_representation_oracle_validated",
    "unshifted_coefficient_output_phase_pencil_used",
    "full_disk_negative_real_bloch_amplitude_included",
    "cutoff64_left_right_singular_vectors_used_only_as_fixed_borders",
    "mode256_coefficient_support_used",
    "explicit_finite_tail_coupling_through_mode320_used",
    "full_infinite_dimensional_grushin_operator_invertible_on_closed_disk",
    "parent_punctured_right_half_disk_nontranslation_exclusion_retained",
    "exact_translation_zero_of_effective_hamiltonian_retained",
    "single_remaining_scalar_rouche_inequality_identified",
)

FALSE_FLAGS = (
    "finite_svd_neutral_diagnostic_promoted_without_full_operator_validation",
    "scalar_effective_hamiltonian_rouche_count_validated",
    "exactly_one_characteristic_value_in_local_disk",
    "local_disk_zero_is_exact_translation_root",
    "local_nontranslation_characteristic_values_excluded",
    "effective_hamiltonian_factors_as_s_times_zero_free_analytic_factor",
    "remaining_compact_keyhole_zero_free_validated",
    "complete_nontranslation_right_half_strip_zero_free_validated",
    "outer_nontranslation_floquet_zero_count_validated",
    "center_parameter_outer_floquet_count_validated",
    "outer_nontrivial_unit_circle_exclusion_validated",
    "outer_attracting_floquet_index_validated",
    "outer_nonlinear_attracting_block_validated",
    "history_space_separator_validated",
    "physical_pulse_onset_validated",
    "canard_root_equals_physical_onset_proved",
    "parameter_box_uniform_outer_floquet_count_validated",
)


@dataclass(frozen=True)
class BoundaryWorstCell:
    index: int
    center_real_binary64: str
    center_imag_binary64: str
    arc_radius_upper: str
    negative_real_part_lower: str
    bloch_amplitude_upper: str
    finite_bordered_inverse_norm_upper: str
    finite_bordered_inverse_defect_upper: str
    full_grushin_contraction_upper: str
    bottom_row_defect_upper: str
    reference_affine_difference_upper: str
    center_inverse_first_error_upper: str
    local_taylor_error_upper: str
    neumann_remainder_upper: str
    local_affine_comparison_error_upper: str


@dataclass(frozen=True)
class LeakyOuterGrushinStage1Certificate:
    schema_id: str
    model_id: str
    branch: str
    riesz_result_sha256: str
    floquet_transfer_result_sha256: str
    outer_orbit_result: str
    outer_orbit_result_sha256: str
    candidate_fingerprint: str
    source_correction_radius: str
    nested_correction_radius: str
    nested_radii_contraction_upper: str
    nested_radii_margin_lower: str
    precision_bits: int
    binary_blas_thread_count: int
    norm_id: str
    delay_operator_representation: str
    fourier_cutoff: int
    coefficient_support_half_bandwidth: int
    explicit_coupling_tail_minimum_mode: int
    explicit_coupling_tail_maximum_mode: int
    complex_finite_dimension: int
    grushin_finite_dimension: int
    root_disk_center_binary64: str
    root_disk_center_hex: str
    root_disk_radius: str
    parent_punctured_right_half_disk_radius_lower: str
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
    center_grushin_condition_number_binary64: str
    center_grushin_inverse_norm_upper: str
    center_grushin_inverse_defect_upper: str
    closed_disk_bloch_amplitude_upper: str
    closed_disk_full_grushin_contraction_upper: str
    closed_disk_full_grushin_margin_lower: str
    reference_effective_slope_real_binary64: str
    reference_effective_slope_imag_binary64: str
    reference_effective_slope_modulus_lower: str
    affine_boundary_modulus_lower: str
    maximum_boundary_comparison_error_upper: str
    rouche_margin_lower: str
    rouche_deficit_upper: str
    worst_reference_affine_difference_upper: str
    worst_center_inverse_first_error_upper: str
    worst_local_taylor_error_upper: str
    worst_neumann_remainder_upper: str
    boundary_partition_sha256: str
    worst_boundary_cell: BoundaryWorstCell
    source_validated_outer_orbit_ball_used: bool
    source_validated_riesz_tail_and_multiplicity_reduction_used: bool
    exact_translation_root_and_algebraic_simplicity_parent_used: bool
    complex_modulus_wiener_grushin_norm_used: bool
    physical_delay_dual_representation_oracle_validated: bool
    unshifted_coefficient_output_phase_pencil_used: bool
    full_disk_negative_real_bloch_amplitude_included: bool
    cutoff64_left_right_singular_vectors_used_only_as_fixed_borders: bool
    mode256_coefficient_support_used: bool
    explicit_finite_tail_coupling_through_mode320_used: bool
    full_infinite_dimensional_grushin_operator_invertible_on_closed_disk: bool
    parent_punctured_right_half_disk_nontranslation_exclusion_retained: bool
    exact_translation_zero_of_effective_hamiltonian_retained: bool
    single_remaining_scalar_rouche_inequality_identified: bool
    scalar_effective_hamiltonian_rouche_count_validated: bool
    exactly_one_characteristic_value_in_local_disk: bool
    local_disk_zero_is_exact_translation_root: bool
    local_nontranslation_characteristic_values_excluded: bool
    effective_hamiltonian_factors_as_s_times_zero_free_analytic_factor: bool
    finite_svd_neutral_diagnostic_promoted_without_full_operator_validation: bool
    remaining_compact_keyhole_zero_free_validated: bool
    complete_nontranslation_right_half_strip_zero_free_validated: bool
    outer_nontranslation_floquet_zero_count_validated: bool
    center_parameter_outer_floquet_count_validated: bool
    outer_nontrivial_unit_circle_exclusion_validated: bool
    outer_attracting_floquet_index_validated: bool
    outer_nonlinear_attracting_block_validated: bool
    history_space_separator_validated: bool
    physical_pulse_onset_validated: bool
    canard_root_equals_physical_onset_proved: bool
    parameter_box_uniform_outer_floquet_count_validated: bool
    next_single_inequality: str
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


def _up(value: object, precision: int = PRECISION_BITS) -> gmpy2.mpfr:
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        return gmpy2.mpfr(value)


def _exp_upper(value: gmpy2.mpfr, precision: int = PRECISION_BITS) -> gmpy2.mpfr:
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        return gmpy2.exp(value)


def _require_pinned_binary_blas_environment() -> None:
    if os.environ.get("OPENBLAS_NUM_THREADS") != PINNED_OPENBLAS_NUM_THREADS:
        raise RuntimeError(
            "the outer Grushin replay requires "
            f"OPENBLAS_NUM_THREADS={PINNED_OPENBLAS_NUM_THREADS}"
        )


def _build_result_in_pinned_binary_blas_subprocess(
    repository: Path,
) -> dict[str, Any]:
    environment = dict(os.environ)
    environment["OPENBLAS_NUM_THREADS"] = PINNED_OPENBLAS_NUM_THREADS
    source_path = str(repository / "src")
    inherited = environment.get("PYTHONPATH", "")
    environment["PYTHONPATH"] = (
        source_path if not inherited else source_path + os.pathsep + inherited
    )
    program = (
        "import json,sys; from pathlib import Path; "
        "from canard_control.leaky_floquet_outer_grushin_stage1 import "
        "build_leaky_outer_grushin_stage1_result; "
        "print(json.dumps(build_leaky_outer_grushin_stage1_result(" 
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
            "the pinned outer Grushin replay subprocess failed: "
            + completed.stderr.strip()
        )
    value = json.loads(completed.stdout)
    if not isinstance(value, dict):
        raise RuntimeError("the pinned outer Grushin replay returned no result")
    return value


def _dependency_fingerprint(repository: Path) -> str:
    repository = repository.resolve()
    riesz_path = repository / RIESZ_RESULT_RELATIVE_PATH
    payload = _mapping(json.loads(riesz_path.read_text()), "Riesz cache key")
    artifact = _mapping(payload.get("artifact"), "Riesz cache artifact")
    branches = _mapping(artifact.get("branches"), "Riesz cache branches")
    branch = _mapping(branches.get(BRANCH), "Riesz cache outer branch")
    orbit_relative = branch.get("source_result")
    if not isinstance(orbit_relative, str) or not orbit_relative:
        raise ValueError("the Riesz cache key has no outer orbit source")
    orbit_path = (repository / orbit_relative).resolve()
    orbit_path.relative_to(repository)
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


@lru_cache(maxsize=4)
def _prepare_cached(
    repository_text: str,
    dependency_fingerprint: str,
) -> tuple[_Prepared, str, str]:
    del dependency_fingerprint
    repository = Path(repository_text).resolve()
    _validate_physical_delay_oracle()
    riesz_path = repository / RIESZ_RESULT_RELATIVE_PATH
    riesz_payload = _mapping(json.loads(riesz_path.read_text()), "Riesz result")
    orbit, evidence, riesz_branch = _validate_sources(
        repository, riesz_payload, replay_parent=True
    )
    if int(riesz_branch["fourier_cutoff"]) != FOURIER_CUTOFF:
        raise ValueError("the outer Grushin contract requires cutoff 64")
    if riesz_branch.get(
        "analytic_characteristic_multiplicity_preserved_by_schur_reduction"
    ) is not True:
        raise ValueError("the outer analytic multiplicity bridge is absent")

    precision = PRECISION_BITS
    base = _build_leaky_base_sequences(orbit, precision)
    current, delayed = _binary_coefficients(orbit)
    support = max(abs(mode) for mode in current)
    if support != COEFFICIENT_SUPPORT_RADIUS:
        raise ValueError("the outer quadratic coefficient support changed")
    modes = np.arange(-FOURIER_CUTOFF, FOURIER_CUTOFF + 1, dtype=int)
    tail_modes = np.concatenate(
        (
            np.arange(-FOURIER_CUTOFF - support, -FOURIER_CUTOFF, dtype=int),
            np.arange(FOURIER_CUTOFF + 1, FOURIER_CUTOFF + support + 1, dtype=int),
        )
    )
    if int(np.max(np.abs(tail_modes))) != EXPLICIT_COUPLING_TAIL_MAXIMUM_MODE:
        raise ValueError("the explicit outer coupling tail no longer ends at 320")
    current_error, delayed_error, current_norm, delayed_norm = (
        _coefficient_error_norms(base, current, delayed, precision)
    )
    current_finite = _coefficient_matrix(modes, modes, current)
    delayed_finite = _coefficient_matrix(modes, modes, delayed)
    current_finite_tail = _coefficient_matrix(modes, tail_modes, current)
    delayed_finite_tail = _coefficient_matrix(modes, tail_modes, delayed)
    current_tail_finite = _coefficient_matrix(tail_modes, modes, current)
    delayed_tail_finite = _coefficient_matrix(tail_modes, modes, delayed)

    nested = _derive_nested_outer_ball(repository, precision)
    registered_nested_radius = DirectedInterval.from_decimal(
        NESTED_ORBIT_RADIUS, precision
    )
    if not (
        nested.radius.lower <= registered_nested_radius.lower
        and nested.radius.upper >= registered_nested_radius.upper
    ):
        raise ValueError("the nested outer correction radius changed")
    radius = nested.radius.upper
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
        s=0.0j,
        precision=precision,
    )
    finite, first, second, finite_tail, finite_tail_first, tail_finite, errors = (
        center_data
    )
    _binary_environment_checked()
    left_vectors, singular_values, right_adjoint = np.linalg.svd(
        finite, full_matrices=True
    )
    _binary_environment_checked()
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
        nested_radii_contraction=DirectedInterval.from_decimal(
            nested.contraction_upper, precision
        ).upper,
        nested_radii_margin=DirectedInterval.from_decimal(
            nested.margin_lower, precision
        ).lower,
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
    return (
        prepared,
        _sha256_path(riesz_path),
        _sha256_path(repository / FLOQUET_TRANSFER_RESULT_RELATIVE_PATH),
    )


def _evaluate_prepared(
    prepared: _Prepared, s: complex
) -> tuple[
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
    Mapping[str, gmpy2.mpfr],
]:
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


def _bloch_amplitude_upper(
    prepared: _Prepared,
    *,
    real_center: float,
    neighborhood: gmpy2.mpfr,
) -> tuple[gmpy2.mpfr, gmpy2.mpfr]:
    real_box = DirectedInterval.from_float(real_center, PRECISION_BITS)
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundDown):
        real_lower = real_box.lower - neighborhood
    alpha_max = max(
        prepared.base.parameters["tau_0"].upper,
        prepared.base.parameters["tau_1"].upper,
    ) / (prepared.base.period.lower - prepared.period_radius)
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
        exponent = max(gmpy2.mpfr(0), -real_lower) * alpha_max
    return real_lower, _exp_upper(exponent)


def _operator_variation(
    prepared: _Prepared,
    *,
    maximum_output_mode: int,
    s_modulus_upper: gmpy2.mpfr,
    bloch_amplitude_upper: gmpy2.mpfr,
) -> gmpy2.mpfr:
    base = prepared.base
    radius = prepared.period_radius
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundDown):
        period_lower = base.period.lower - radius
    tau_max = max(
        base.parameters["tau_0"].upper,
        base.parameters["tau_1"].upper,
    )
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
        frequency = (
            s_modulus_upper
            + 2 * pi_interval(PRECISION_BITS).upper * maximum_output_mode
        )
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
        delayed = bloch_amplitude_upper * (
            (base.period.upper + radius) * prepared.delayed_total_variation
            + radius * (2 * prepared.delayed_binary_norm)
            + base.period.upper
            * rotation_change
            * (2 * prepared.delayed_binary_norm)
        )
        convolution = current + delayed
        return max(
            convolution + radius * base.parameters["epsilon"].upper,
            radius * (1 + base.parameters["epsilon"].upper),
        )


def _coupling_variation(
    prepared: _Prepared,
    *,
    maximum_output_mode: int,
    s_modulus_upper: gmpy2.mpfr,
    bloch_amplitude_upper: gmpy2.mpfr,
) -> gmpy2.mpfr:
    base = prepared.base
    radius = prepared.period_radius
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundDown):
        period_lower = base.period.lower - radius
    tau_max = max(
        base.parameters["tau_0"].upper,
        base.parameters["tau_1"].upper,
    )
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
        frequency = (
            s_modulus_upper
            + 2 * pi_interval(PRECISION_BITS).upper * maximum_output_mode
        )
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
        delayed = bloch_amplitude_upper * (
            (base.period.upper + radius) * prepared.delayed_total_variation
            + radius * (2 * prepared.delayed_binary_norm)
            + base.period.upper
            * rotation_change
            * (2 * prepared.delayed_binary_norm)
        )
        return current + delayed


def _preconditioned_tail_coupling_variation(
    prepared: _Prepared,
    *,
    fast_tail_inverse: gmpy2.mpfr,
    spectral_neighborhood: gmpy2.mpfr,
    bloch_amplitude_upper: gmpy2.mpfr,
) -> gmpy2.mpfr:
    base = prepared.base
    radius = prepared.period_radius
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundDown):
        period_lower = base.period.lower - radius
    tau_sum = upward_sum(
        (base.parameters["tau_0"].upper, base.parameters["tau_1"].upper),
        PRECISION_BITS,
    )
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
        current = (
            (base.period.upper + radius) * prepared.current_total_variation
            + radius * prepared.current_binary_norm
        )
        delayed = bloch_amplitude_upper * (
            (base.period.upper + radius) * prepared.delayed_total_variation
            + radius * 2 * prepared.delayed_binary_norm
        )
        phase = bloch_amplitude_upper * (
            prepared.delayed_binary_norm
            * tau_sum
            * radius
            / period_lower
            * (1 + fast_tail_inverse * spectral_neighborhood)
        )
        return fast_tail_inverse * (current + delayed) + phase


def _first_second_bounds(
    prepared: _Prepared,
    bloch_amplitude_upper: gmpy2.mpfr,
) -> tuple[gmpy2.mpfr, gmpy2.mpfr, gmpy2.mpfr]:
    first_parent = DirectedInterval.from_decimal(
        prepared.riesz_branch["local_complex_first_order_coefficient_upper"],
        PRECISION_BITS,
    ).upper
    delayed_uniform = DirectedInterval.from_decimal(
        prepared.riesz_branch[
            "delayed_coefficient_uniform_sum_wiener_upper"
        ],
        PRECISION_BITS,
    ).upper
    minimum_period = DirectedInterval.from_decimal(
        prepared.riesz_branch["minimum_period_lower"], PRECISION_BITS
    ).lower
    maximum_period = DirectedInterval.from_decimal(
        prepared.riesz_branch["maximum_period_upper"], PRECISION_BITS
    ).upper
    tau_max = max(
        prepared.base.parameters["tau_0"].upper,
        prepared.base.parameters["tau_1"].upper,
    )
    tau_sum = upward_sum(
        (
            prepared.base.parameters["tau_0"].upper,
            prepared.base.parameters["tau_1"].upper,
        ),
        PRECISION_BITS,
    )
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
        first = first_parent * bloch_amplitude_upper
        second = (
            maximum_period
            * (tau_max / minimum_period) ** 2
            * delayed_uniform
            * bloch_amplitude_upper
        )
        finite_tail_first = (
            tau_sum
            * (2 * prepared.delayed_binary_norm + prepared.delayed_total_variation)
            * bloch_amplitude_upper
        )
    return first, second, finite_tail_first


def _tail_inverse_upper(
    prepared: _Prepared,
    *,
    real_center: float,
    imag_center: float,
    neighborhood: gmpy2.mpfr,
) -> tuple[gmpy2.mpfr, gmpy2.mpfr]:
    sigma = DirectedInterval.from_float(real_center, PRECISION_BITS)
    phase = DirectedInterval.from_float(imag_center, PRECISION_BITS)
    center = DirectedComplexInterval(sigma, phase)
    epsilon_period = prepared.base.period * prepared.base.parameters["epsilon"]
    fast_values: list[gmpy2.mpfr] = []
    slow_values: list[gmpy2.mpfr] = []
    for mode in (-FOURIER_CUTOFF - 1, FOURIER_CUTOFF + 1):
        frequency = DirectedComplexInterval(
            center.real,
            center.imag + pi_interval(PRECISION_BITS) * (2 * mode),
        )
        fast_values.append(frequency.lower_abs())
        slow_values.append(
            (
                frequency
                + DirectedComplexInterval.from_real(epsilon_period)
            ).lower_abs()
        )
    fast_gap = min(fast_values)
    slow_gap = min(slow_values)
    if fast_gap <= neighborhood or slow_gap <= neighborhood:
        raise ArithmeticError("the outer local tail diagonal crosses zero")
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
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
    bloch_amplitude_upper: gmpy2.mpfr,
) -> gmpy2.mpfr:
    current = DirectedInterval.from_decimal(
        prepared.riesz_branch["current_coefficient_uniform_wiener_upper"],
        PRECISION_BITS,
    ).upper
    delayed = DirectedInterval.from_decimal(
        prepared.riesz_branch[
            "delayed_coefficient_uniform_sum_wiener_upper"
        ],
        PRECISION_BITS,
    ).upper
    period = DirectedInterval.from_decimal(
        prepared.riesz_branch["maximum_period_upper"], PRECISION_BITS
    ).upper
    epsilon = prepared.base.parameters["epsilon"].upper
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
        voltage_column = (
            fast_inverse
            * (
                diagonal_radius
                + period * (current + bloch_amplitude_upper * delayed)
            )
            + slow_inverse * period * epsilon
        )
        recovery_column = (
            fast_inverse * period
            + slow_inverse
            * (diagonal_radius + epsilon * prepared.period_radius)
        )
        return max(voltage_column, recovery_column)


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
    negative_real, amplitude = _bloch_amplitude_upper(
        prepared, real_center=float(s.real), neighborhood=neighborhood
    )
    fast_inverse, slow_inverse = _tail_inverse_upper(
        prepared,
        real_center=float(s.real),
        imag_center=float(s.imag),
        neighborhood=neighborhood,
    )
    finite_orbit = _operator_variation(
        prepared,
        maximum_output_mode=FOURIER_CUTOFF,
        s_modulus_upper=s_abs,
        bloch_amplitude_upper=amplitude,
    )
    finite_tail_orbit = _coupling_variation(
        prepared,
        maximum_output_mode=FOURIER_CUTOFF,
        s_modulus_upper=s_abs,
        bloch_amplitude_upper=amplitude,
    )
    tail_finite_orbit = _preconditioned_tail_coupling_variation(
        prepared,
        fast_tail_inverse=fast_inverse,
        spectral_neighborhood=neighborhood,
        bloch_amplitude_upper=amplitude,
    )
    first_bound, _, finite_tail_first_bound = _first_second_bounds(
        prepared, amplitude
    )
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
    row_tail_matrix = inverse[-1:, :] @ augmented_finite_tail
    row_tail = _matrix_max_entry_upper(row_tail_matrix, precision) + (
        _formation_error(
            row_norm
            * _binary_complex_matrix_split_l1_upper(
                augmented_finite_tail, precision
            ),
            augmented_finite_tail.shape[0],
            precision,
        )
    )
    finite_tail_column = (
        finite_tail_product + inverse_norm * finite_tail_change
    )
    row_tail += row_norm * finite_tail_change

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
        bloch_amplitude_upper=amplitude,
    )
    finite_column = defect + inverse_norm * finite_change
    contraction = max(
        finite_column + tail_finite_column,
        finite_tail_column + tail_tail,
    )
    bottom_finite = _row_dual_upper(defect_matrix[-1, :], precision) + (
        row_norm * finite_change
    )
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
        "contraction": contraction,
        "bottom_row": max(bottom_finite, row_tail),
        "negative_real": negative_real,
        "bloch_amplitude": amplitude,
    }


def _circle_cell_center(
    index: int,
) -> tuple[complex, gmpy2.mpfr]:
    precision = PRECISION_BITS
    radius = DirectedInterval.from_decimal(ROOT_DISK_RADIUS, precision)
    angle = pi_interval(precision) * (2 * index) / BOUNDARY_ARC_COUNT
    theta_float = 2.0 * math.pi * index / BOUNDARY_ARC_COUNT
    center = complex(
        float(ROOT_DISK_RADIUS) * math.cos(theta_float),
        float(ROOT_DISK_RADIUS) * math.sin(theta_float),
    )
    exact = DirectedComplexInterval(radius * cos_interval(angle), radius * sin_interval(angle))
    stored = DirectedComplexInterval(
        DirectedInterval.from_float(center.real, precision),
        DirectedInterval.from_float(center.imag, precision),
    )
    center_error = (exact - stored).upper_abs()
    half_angle = pi_interval(precision) / BOUNDARY_ARC_COUNT
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        arc_radius = (
            2 * radius.upper * sin_interval(half_angle).upper + center_error
        )
    return center, arc_radius


def _reference_difference_upper(
    b00: complex,
    slope: complex,
    center: complex,
    reference_slope: complex,
    arc_radius: gmpy2.mpfr,
) -> gmpy2.mpfr:
    center_difference = b00 - reference_slope * center
    slope_difference = slope - reference_slope
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
        return (
            _complex_abs_upper(center_difference, PRECISION_BITS)
            + _complex_abs_upper(slope_difference, PRECISION_BITS) * arc_radius
            + _formation_error(
                _split_upper(reference_slope, PRECISION_BITS)
                * _up(abs(center), PRECISION_BITS),
                8,
                PRECISION_BITS,
            )
        )


def _boundary_cell(
    prepared: _Prepared,
    index: int,
    reference_slope: complex,
) -> _CellData:
    center, arc_radius = _circle_cell_center(index)
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
        raise ArithmeticError(f"outer boundary Grushin cell {index} failed")
    b = inverse[:, -1]
    first_augmented = _augment_derivative(first)
    slope = -complex(inverse[-1, :] @ (first_augmented @ b))
    slope_round = _formation_error(
        block["row_norm"]
        * _binary_complex_matrix_split_l1_upper(first_augmented, PRECISION_BITS)
        * block["scalar_column_norm"],
        2 * grushin.shape[0],
        PRECISION_BITS,
    )
    defect_times_b = block["defect_matrix"] @ b
    center_first_error = (
        _complex_abs_upper(complex(defect_times_b[-1]), PRECISION_BITS)
        + _formation_error(
            _row_dual_upper(block["defect_matrix"][-1, :], PRECISION_BITS)
            * block["scalar_column_norm"],
            grushin.shape[0],
            PRECISION_BITS,
        )
        + block["row_norm"]
        * (errors["finite"] + block["finite_orbit"])
        * block["scalar_state_column_norm"]
    )
    _, second_bound, _ = _first_second_bounds(
        prepared, block["bloch_amplitude"]
    )
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
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
        reference_difference = _reference_difference_upper(
            complex(inverse[-1, -1]),
            slope,
            center,
            reference_slope,
            arc_radius,
        )
        comparison = (
            reference_difference
            + center_first_error
            + local_taylor_error
            + neumann_remainder
        )
    summary: Mapping[str, str | int] = {
        "index": index,
        "center_real_binary64": format(center.real, ".17g"),
        "center_imag_binary64": format(center.imag, ".17g"),
        "arc_radius_upper": decimal_upper(arc_radius),
        "negative_real_part_lower": decimal_lower(block["negative_real"]),
        "bloch_amplitude_upper": decimal_upper(block["bloch_amplitude"]),
        "finite_bordered_inverse_norm_upper": decimal_upper(
            block["inverse_norm"]
        ),
        "finite_bordered_inverse_defect_upper": decimal_upper(block["defect"]),
        "full_grushin_contraction_upper": decimal_upper(q),
        "bottom_row_defect_upper": decimal_upper(block["bottom_row"]),
        "reference_affine_difference_upper": decimal_upper(
            reference_difference
        ),
        "center_inverse_first_error_upper": decimal_upper(center_first_error),
        "local_taylor_error_upper": decimal_upper(local_taylor_error),
        "neumann_remainder_upper": decimal_upper(neumann_remainder),
        "local_affine_comparison_error_upper": decimal_upper(comparison),
    }
    return _CellData(summary=summary, comparison=comparison, contraction=q)


def _partition_sha256(cells: Iterable[_CellData]) -> str:
    return canonical_sha256([dict(cell.summary) for cell in cells])


def build_leaky_outer_grushin_stage1_certificate(
    repository: Path,
) -> LeakyOuterGrushinStage1Certificate:
    _require_pinned_binary_blas_environment()
    repository = repository.resolve()
    fingerprint = _dependency_fingerprint(repository)
    prepared, riesz_hash, floquet_hash = _prepare_cached(
        str(repository), fingerprint
    )
    oracle = _validate_physical_delay_oracle()
    center_inverse = prepared.finite_grushin_inverse
    center_inverse_norm = _binary_complex_matrix_split_l1_upper(
        center_inverse, PRECISION_BITS
    )
    center_defect, _ = _inverse_defect(
        center_inverse,
        prepared.finite_grushin,
        PRECISION_BITS,
        center_inverse_norm,
    )
    b = center_inverse[:, -1]
    reference_slope = -complex(
        center_inverse[-1, :]
        @ (_augment_derivative(prepared.center_first) @ b)
    )
    slope_lower = _complex_abs_lower(reference_slope, PRECISION_BITS)
    if slope_lower <= 0:
        raise ArithmeticError("the outer effective Hamiltonian guide vanished")

    root_radius = DirectedInterval.from_decimal(
        ROOT_DISK_RADIUS, PRECISION_BITS
    )
    center_block = _grushin_block_bounds(
        prepared,
        s=0.0j,
        neighborhood=root_radius.upper,
        inverse=center_inverse,
        finite=prepared.center_matrix,
        finite_tail=prepared.center_finite_tail,
        finite_tail_first=prepared.center_finite_tail_first,
        tail_finite=prepared.center_tail_finite,
        errors=prepared.center_errors,
        include_disk_s_variation=True,
    )
    disk_q = center_block["contraction"]
    if not 0 < disk_q < 1:
        raise ArithmeticError("the complete outer Grushin disk did not contract")

    cells = tuple(
        _boundary_cell(prepared, index, reference_slope)
        for index in range(BOUNDARY_ARC_COUNT)
    )
    worst = max(cells, key=lambda cell: cell.comparison)
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundDown):
        affine_boundary = slope_lower * root_radius.lower
        rouche_margin = affine_boundary - worst.comparison
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
        rouche_deficit = worst.comparison - affine_boundary
    if not rouche_margin < 0 or not rouche_deficit > 0:
        raise ArithmeticError(
            "the registered Stage-1 failure inequality unexpectedly closed"
        )

    singular_values = prepared.center_singular_values
    condition = np.linalg.cond(prepared.finite_grushin)
    source_path = repository / prepared.evidence.source_result
    return LeakyOuterGrushinStage1Certificate(
        schema_id=SCHEMA_ID,
        model_id=MODEL_ID,
        branch=BRANCH,
        riesz_result_sha256=riesz_hash,
        floquet_transfer_result_sha256=floquet_hash,
        outer_orbit_result=prepared.evidence.source_result,
        outer_orbit_result_sha256=_sha256_path(source_path),
        candidate_fingerprint=prepared.evidence.candidate_fingerprint,
        source_correction_radius=prepared.evidence.correction_radius,
        nested_correction_radius=NESTED_ORBIT_RADIUS,
        nested_radii_contraction_upper=decimal_upper(
            prepared.nested_radii_contraction
        ),
        nested_radii_margin_lower=decimal_lower(prepared.nested_radii_margin),
        precision_bits=PRECISION_BITS,
        binary_blas_thread_count=int(PINNED_OPENBLAS_NUM_THREADS),
        norm_id="complex-modulus Wiener l1; split real/imaginary majorants",
        delay_operator_representation=(
            "physical unshifted coefficient with Bloch-delay phase on output row"
        ),
        fourier_cutoff=FOURIER_CUTOFF,
        coefficient_support_half_bandwidth=COEFFICIENT_SUPPORT_RADIUS,
        explicit_coupling_tail_minimum_mode=FOURIER_CUTOFF + 1,
        explicit_coupling_tail_maximum_mode=EXPLICIT_COUPLING_TAIL_MAXIMUM_MODE,
        complex_finite_dimension=2 * (2 * FOURIER_CUTOFF + 1),
        grushin_finite_dimension=2 * (2 * FOURIER_CUTOFF + 1) + 1,
        root_disk_center_binary64="0",
        root_disk_center_hex=ROOT_CENTER_BINARY64.hex(),
        root_disk_radius=ROOT_DISK_RADIUS,
        parent_punctured_right_half_disk_radius_lower=prepared.riesz_branch[
            "local_complex_exclusion_radius_lower"
        ],
        boundary_arc_count=BOUNDARY_ARC_COUNT,
        unshifted_row_oracle_error_binary64=format(oracle[0], ".17g"),
        shifted_column_oracle_error_binary64=format(oracle[1], ".17g"),
        unshifted_column_mutation_separation_binary64=format(
            oracle[2], ".17g"
        ),
        shifted_row_mutation_separation_binary64=format(oracle[3], ".17g"),
        directed_equivalent_entry_count=oracle[4],
        directed_equivalent_entry_total=oracle[5],
        directed_unshifted_column_mutation_separation_lower=decimal_lower(
            oracle[6]
        ),
        directed_shifted_row_mutation_separation_lower=decimal_lower(oracle[7]),
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
        center_grushin_condition_number_binary64=format(condition, ".17g"),
        center_grushin_inverse_norm_upper=decimal_upper(center_inverse_norm),
        center_grushin_inverse_defect_upper=decimal_upper(center_defect),
        closed_disk_bloch_amplitude_upper=decimal_upper(
            center_block["bloch_amplitude"]
        ),
        closed_disk_full_grushin_contraction_upper=decimal_upper(disk_q),
        closed_disk_full_grushin_margin_lower=decimal_lower(1 - disk_q),
        reference_effective_slope_real_binary64=format(
            reference_slope.real, ".17g"
        ),
        reference_effective_slope_imag_binary64=format(
            reference_slope.imag, ".17g"
        ),
        reference_effective_slope_modulus_lower=decimal_lower(slope_lower),
        affine_boundary_modulus_lower=decimal_lower(affine_boundary),
        maximum_boundary_comparison_error_upper=decimal_upper(worst.comparison),
        rouche_margin_lower=decimal_lower(rouche_margin),
        rouche_deficit_upper=decimal_upper(rouche_deficit),
        worst_reference_affine_difference_upper=worst.summary[
            "reference_affine_difference_upper"
        ],
        worst_center_inverse_first_error_upper=worst.summary[
            "center_inverse_first_error_upper"
        ],
        worst_local_taylor_error_upper=worst.summary[
            "local_taylor_error_upper"
        ],
        worst_neumann_remainder_upper=worst.summary[
            "neumann_remainder_upper"
        ],
        boundary_partition_sha256=_partition_sha256(cells),
        worst_boundary_cell=BoundaryWorstCell(**dict(worst.summary)),
        **{name: True for name in TRUE_FLAGS},
        **{name: False for name in FALSE_FLAGS},
        next_single_inequality=(
            "On a larger radius R, certify sup_{|s|=R}|E_-+(s)-a_* s| "
            "< |a_*| R with the same fixed borders and full-disk amplitude "
            "factor; this is the sole local pole-subtraction extension "
            "inequality, after which the separated complement returns to "
            "the full-operator Neumann cover."
        ),
        minimal_remaining_gate=(
            "enlarge the certified pole-subtracted disk enough to remove the "
            "near-neutral conditioning cost, then complete the separated "
            "principal right-half-strip cover; only that global exclusion "
            "can promote the outer Floquet count or attraction index"
        ),
    )


def build_leaky_outer_grushin_stage1_result(
    repository: Path,
) -> dict[str, Any]:
    repository = repository.resolve()
    certificate = asdict(
        build_leaky_outer_grushin_stage1_certificate(repository)
    )
    sources = {
        relative: _sha256_path(repository / relative)
        for relative in SOURCE_MANIFEST
    }
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
            "riesz_parent_result_sha256": _sha256_path(
                repository / RIESZ_RESULT_RELATIVE_PATH
            ),
            "floquet_transfer_result": FLOQUET_TRANSFER_RESULT_RELATIVE_PATH,
            "floquet_transfer_result_sha256": _sha256_path(
                repository / FLOQUET_TRANSFER_RESULT_RELATIVE_PATH
            ),
            "outer_orbit_result": certificate["outer_orbit_result"],
            "outer_orbit_result_sha256": certificate[
                "outer_orbit_result_sha256"
            ],
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


def validate_leaky_outer_grushin_stage1_result(
    payload: Mapping[str, Any], repository: Path
) -> None:
    if not isinstance(payload, Mapping) or set(payload) != {
        "certificate",
        "manifest",
    }:
        raise ValueError("the outer Grushin result has the wrong outer schema")
    certificate = _mapping(payload.get("certificate"), "outer certificate")
    manifest = _mapping(payload.get("manifest"), "outer manifest")
    if set(certificate) != {
        field.name for field in fields(LeakyOuterGrushinStage1Certificate)
    }:
        raise ValueError("the outer Grushin certificate schema changed")
    if any(certificate.get(name) is not True for name in TRUE_FLAGS):
        raise ValueError("a proved outer local Grushin flag was weakened")
    if any(certificate.get(name) is not False for name in FALSE_FLAGS):
        raise ValueError("an open outer Floquet or onset flag was promoted")
    if certificate.get("branch") != BRANCH:
        raise ValueError("the Grushin theorem was attached to another branch")
    if int(certificate["fourier_cutoff"]) != FOURIER_CUTOFF:
        raise ValueError("the outer Grushin cutoff changed")
    if int(certificate["coefficient_support_half_bandwidth"]) != 256:
        raise ValueError("the outer mode-256 support was lost")
    if int(certificate["explicit_coupling_tail_maximum_mode"]) != 320:
        raise ValueError("the outer explicit coupling tail was shortened")
    if int(certificate["binary_blas_thread_count"]) != int(
        PINNED_OPENBLAS_NUM_THREADS
    ):
        raise ValueError("the outer Grushin BLAS schedule changed")
    if gmpy2.mpq(
        certificate["closed_disk_full_grushin_contraction_upper"]
    ) >= 1:
        raise ValueError("the complete outer Grushin disk is not invertible")
    if gmpy2.mpq(certificate["closed_disk_bloch_amplitude_upper"]) <= 1:
        raise ValueError("the negative-real full-disk amplitude was omitted")
    if gmpy2.mpq(certificate["rouche_margin_lower"]) >= 0:
        raise ValueError("the registered outer Rouche failure disappeared")
    if gmpy2.mpq(certificate["rouche_deficit_upper"]) <= 0:
        raise ValueError("the registered outer Rouche deficit is not positive")
    registered_comparison = gmpy2.mpq(
        certificate["maximum_boundary_comparison_error_upper"]
    )
    components = tuple(
        gmpy2.mpq(certificate[name])
        for name in (
            "worst_reference_affine_difference_upper",
            "worst_center_inverse_first_error_upper",
            "worst_local_taylor_error_upper",
            "worst_neumann_remainder_upper",
        )
    )
    if any(value <= 0 or value > registered_comparison for value in components):
        raise ValueError("the outer Rouche error decomposition is invalid")
    if components[-1] != max(components):
        raise ValueError("the registered dominant Neumann remainder changed")
    if gmpy2.mpq(certificate["reference_effective_slope_modulus_lower"]) <= 0:
        raise ValueError("the outer effective slope guide vanished")
    if not certificate["next_single_inequality"].startswith(
        "On a larger radius R"
    ):
        raise ValueError("the single remaining local inequality changed")

    expected_manifest_fields = {
        "schema_id",
        "result",
        "default_command",
        "arithmetic_scope",
        "certificate_sha256",
        "source_sha256",
        "riesz_parent_result",
        "riesz_parent_result_sha256",
        "floquet_transfer_result",
        "floquet_transfer_result_sha256",
        "outer_orbit_result",
        "outer_orbit_result_sha256",
        "environment",
    }
    if set(manifest) != expected_manifest_fields:
        raise ValueError("the outer Grushin manifest schema changed")
    scalar_expected = {
        "schema_id": SCHEMA_ID,
        "result": RESULT_RELATIVE_PATH,
        "default_command": DEFAULT_COMMAND,
        "arithmetic_scope": ARITHMETIC_SCOPE,
        "riesz_parent_result": RIESZ_RESULT_RELATIVE_PATH,
        "floquet_transfer_result": FLOQUET_TRANSFER_RESULT_RELATIVE_PATH,
        "outer_orbit_result": certificate["outer_orbit_result"],
    }
    for name, expected in scalar_expected.items():
        if manifest.get(name) != expected:
            raise ValueError(f"the outer Grushin manifest {name} changed")
    if manifest.get("certificate_sha256") != canonical_sha256(certificate):
        raise ValueError("the outer Grushin certificate hash changed")
    repository = repository.resolve()
    source_hashes = _mapping(
        manifest.get("source_sha256"), "outer source manifest"
    )
    if set(source_hashes) != set(SOURCE_MANIFEST):
        raise ValueError("the outer Grushin source set changed")
    for relative in SOURCE_MANIFEST:
        if source_hashes.get(relative) != _sha256_path(repository / relative):
            raise ValueError(f"the outer Grushin source changed: {relative}")
    result_bindings = {
        "riesz_parent_result_sha256": RIESZ_RESULT_RELATIVE_PATH,
        "floquet_transfer_result_sha256": FLOQUET_TRANSFER_RESULT_RELATIVE_PATH,
        "outer_orbit_result_sha256": certificate["outer_orbit_result"],
    }
    for field_name, relative in result_bindings.items():
        if manifest.get(field_name) != _sha256_path(repository / relative):
            raise ValueError(f"the outer Grushin parent changed: {relative}")
    expected = (
        build_leaky_outer_grushin_stage1_result(repository)
        if os.environ.get("OPENBLAS_NUM_THREADS")
        == PINNED_OPENBLAS_NUM_THREADS
        else _build_result_in_pinned_binary_blas_subprocess(repository)
    )
    if dict(payload) != expected:
        raise ValueError("the outer Grushin result differs from full replay")


__all__ = [
    "ARITHMETIC_SCOPE",
    "BOUNDARY_ARC_COUNT",
    "BRANCH",
    "COEFFICIENT_SUPPORT_RADIUS",
    "DEFAULT_COMMAND",
    "EXPLICIT_COUPLING_TAIL_MAXIMUM_MODE",
    "FALSE_FLAGS",
    "FOURIER_CUTOFF",
    "GENERATOR_RELATIVE_PATH",
    "LeakyOuterGrushinStage1Certificate",
    "NOTE_RELATIVE_PATH",
    "NESTED_ORBIT_RADIUS",
    "PINNED_OPENBLAS_NUM_THREADS",
    "PRECISION_BITS",
    "RESULT_RELATIVE_PATH",
    "ROOT_DISK_RADIUS",
    "SCHEMA_ID",
    "SOURCE_MANIFEST",
    "SOURCE_RELATIVE_PATH",
    "TEST_RELATIVE_PATH",
    "TRUE_FLAGS",
    "build_leaky_outer_grushin_stage1_certificate",
    "build_leaky_outer_grushin_stage1_result",
    "canonical_sha256",
    "validate_leaky_outer_grushin_stage1_result",
]
