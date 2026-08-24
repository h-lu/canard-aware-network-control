"""Directed zero-free cover of the synchronous Floquet right half strip.

This module attacks the last unstable-index gate without trying to enclose a
258-dimensional determinant phase.  For every rectangle in a finite cover
of the logarithmic keyhole it constructs a block-diagonal approximate
inverse of the *full* infinite Bloch operator.  The finite block uses an
audited binary64 inverse, while the Fourier tail uses the exact diagonal at
the rectangle centre.  A strict two-column four-block Neumann estimate then
proves invertibility throughout the rectangle, uniformly on the validated
periodic-orbit parameter box.

The computation uses the split real/imaginary Wiener norm.  Consequently the
tail multiplier ``(sigma+i*omega)^(-1)`` is bounded by

    (sigma + abs(omega)) / (sigma**2 + omega**2),

not by ``1/hypot(sigma, omega)``.  The separate analytic Riesz reduction and
outer exclusion use the complex-modulus Wiener norm; invertibility is of
course independent of this equivalent-norm choice.

No unstable-index or attraction flag is promoted unless the adaptive cover is
complete and every stored leaf has a directed contraction strictly below
one.  The local half-square around the translation value is discharged by
the already proved complex punctured-disk theorem.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, localcontext
from fractions import Fraction
from hashlib import sha256
import math
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping, Sequence

import gmpy2
import numpy as np

from canard_control.directed_interval import (
    DirectedComplexInterval,
    DirectedInterval,
    complex_unit_interval,
    decimal_lower,
    decimal_upper,
    pi_interval,
    upward_sum,
)
from canard_control.fhn_bloch_outer_validation import (
    BlochParameterBoxEvidence,
    _binary_environment_checked,
    _box_distance_split_upper,
    _sequence_box_norm_upper,
)
from canard_control.fhn_periodic_infinite_validation import (
    _BaseSequences,
    _build_base_sequences,
)
from canard_control.fhn_periodic_parameter_box import (
    _build_parameter_box_sequences,
)
from canard_control.fhn_synchronous_floquet_riesz_reduction import (
    _orbit_from_payload,
    validate_synchronous_floquet_riesz_result_payload,
)


_PARAMETER_BOX_SHA256 = (
    "ff13b5352c2b4e9898a4044be63fd490a3e7bb4217445a6a062188c2457c22a0"
)
_BLOCH_SHA256 = (
    "c2f93b6cfe6a8e0df3b341476fbe45a83f6fecc0398dbb7340a5213a55357a31"
)
_RIESZ_SHA256 = (
    "b68483ae12421195a485e6c9af950d8d101cf04497565cf079fcf57ba57793f6"
)
_TRANSVERSE_SHA256 = (
    "ec4b3204695bf40d4309681b0f57d93e3e1e524ca3680cdce316aaee8ad015fb"
)
_CANDIDATE_SHA256 = (
    "7437514175586665b1bf10831793427e42d8a9cbd736536444be4a98064a3c28"
)
_CANDIDATE_FINGERPRINT = (
    "2b56b5dff18c5aacd1450252824f5601ba3826f6de5d82eb2380853d3c518169"
)
_MODEL_ID = "dual-scaffold-rank-one-two-module-fhn-two-delay"
_NORM_ID = "complex-component-wiener-l1-split-re-im"
_CUTOFF = 64
_SUPPORT_RADIUS = 128
_OUTER_REAL_PART = Decimal(128)
_FUNDAMENTAL_PHASE_LOWER = (
    "-3.14159265358979323846264338327950288419716939937909994"
)
_FUNDAMENTAL_PHASE_UPPER = (
    "3.14159265358979323846264338327950288419716939937909994"
)
_LOCAL_COMPLEX_EXCLUSION_RADIUS = (
    "0.00110371801789578632406620967700529547972127567299941844"
)
_HALF_SQUARE_RADIUS = (
    "0.000551859008947893162033104838502647739860637836499709222"
)


@dataclass(frozen=True)
class RightHalfCoverEvidence:
    parameter_box_result_sha256: str
    bloch_result_sha256: str
    riesz_result_sha256: str
    transverse_result_sha256: str
    candidate_result_sha256: str
    candidate_fingerprint: str
    model_id: str


@dataclass(frozen=True)
class CoverLeaf:
    root_id: str
    path: str
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
    tail_diagonal_inverse_split_upper: str
    finite_full_parameter_correction_upper: str
    finite_convolution_parameter_correction_upper: str
    tail_from_finite_parameter_correction_upper: str
    finite_to_finite_upper: str
    finite_from_tail_upper: str
    tail_from_finite_upper: str
    tail_to_tail_upper: str
    finite_input_column_sum_upper: str
    tail_input_column_sum_upper: str
    contraction_upper: str
    contraction_margin_lower: str


@dataclass(frozen=True)
class RightHalfZeroFreeCover:
    model_id: str
    parameter_box_result_sha256: str
    bloch_result_sha256: str
    riesz_result_sha256: str
    transverse_result_sha256: str
    candidate_result_sha256: str
    candidate_fingerprint: str
    precision_bits: int
    norm_id: str
    cutoff: int
    complex_finite_dimension: int
    coefficient_support_half_bandwidth: int
    outer_real_part: str
    fundamental_phase_lower: str
    fundamental_phase_upper: str
    local_complex_exclusion_radius_lower: str
    half_square_radius: str
    half_square_corner_radius_upper: str
    half_square_strictly_inside_local_disk: bool
    root_rectangle_count: int
    accepted_leaf_count: int
    processed_cell_count: int
    pending_cell_count: int
    maximum_depth: int
    acceptance_threshold: str
    maximum_contraction_upper: str | None
    minimum_contraction_margin_lower: str | None
    leaf_partition_sha256: str
    binary_environment_validated: bool
    exact_parameter_box_orbit_ball_included_everywhere: bool
    complex_s_taylor_segment_stays_in_closed_right_half_plane: bool
    correct_split_tail_diagonal_inverse_used: bool
    negative_half_strip_mode_reversal_conjugacy_validated: bool
    prefix_complete_dyadic_cover_validated: bool
    entire_keyhole_region_zero_free_validated: bool
    cellwise_left_preconditioned_full_operator_neumann_homotopy_validated: bool
    exact_schur_to_candidate_finite_homotopy_validated: bool
    schur_boundary_winding_deduced_exactly_lower: int | None
    schur_boundary_winding_deduced_exactly_upper: int | None
    directed_nontranslation_right_half_strip_zero_count: int | None
    spectral_set_correspondence_used_without_general_multiplicity_bridge: bool
    synchronous_nontranslation_unstable_index_zero_validated: bool
    synchronous_linear_orbital_attraction_validated: bool
    hale_verduyn_lunel_hyperbolic_periodic_orbit_theorem_applied: bool
    synchronous_nonlinear_orbital_attraction_validated: bool
    fixed_rank_one_full_network_linear_orbital_attraction_validated: bool
    fixed_rank_one_full_network_nonlinear_orbital_attraction_validated: bool
    general_network_topology_validated: bool
    biological_pulse_capture_validated: bool
    leaves: tuple[CoverLeaf, ...]
    worst_cell: WorstCoverCell | None
    failure_reason: str | None


@dataclass(frozen=True)
class _Rectangle:
    root_id: str
    path: str
    sigma_lower: Decimal
    sigma_upper: Decimal
    phase_lower: Decimal
    phase_upper: Decimal


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
class _CellBounds:
    leaf: CoverLeaf
    worst: WorstCoverCell
    validated: bool


def _mapping(value: object, label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{label} must be a mapping")
    return value


def _require_true(payload: Mapping[str, Any], key: str) -> None:
    if payload.get(key) is not True:
        raise ValueError(f"required source theorem is absent: {key}")


def _require_false(payload: Mapping[str, Any], key: str) -> None:
    if payload.get(key) is not False:
        raise ValueError(f"source scope was promoted: {key}")


def _validate_evidence(evidence: RightHalfCoverEvidence) -> None:
    expected = {
        "parameter_box_result_sha256": _PARAMETER_BOX_SHA256,
        "bloch_result_sha256": _BLOCH_SHA256,
        "riesz_result_sha256": _RIESZ_SHA256,
        "transverse_result_sha256": _TRANSVERSE_SHA256,
        "candidate_result_sha256": _CANDIDATE_SHA256,
        "candidate_fingerprint": _CANDIDATE_FINGERPRINT,
        "model_id": _MODEL_ID,
    }
    if any(getattr(evidence, key) != value for key, value in expected.items()):
        raise ValueError("the right-half cover evidence is outside tracked scope")


def _validate_sources(
    bloch_payload: Mapping[str, Any],
    riesz_payload: Mapping[str, Any],
    transverse_payload: Mapping[str, Any],
    evidence: RightHalfCoverEvidence,
) -> tuple[Mapping[str, Any], Mapping[str, Any], BlochParameterBoxEvidence]:
    validate_synchronous_floquet_riesz_result_payload(riesz_payload)
    riesz = _mapping(riesz_payload.get("certificate"), "Riesz certificate")
    if riesz.get("tail_outer_norm_id") != "complex-component-wiener-l1-modulus":
        raise ValueError("the repaired modulus-norm Riesz theorem is required")
    for key in (
        "uniform_tail_block_invertible_on_closed_right_half_strip",
        "analytic_finite_schur_reduction_validated",
        "no_characteristic_values_at_or_beyond_outer_real_part",
        "local_right_half_punctured_disk_excluded",
    ):
        _require_true(riesz, key)
    for key in (
        "directed_finite_schur_winding_validated",
        "synchronous_stable_index_validated",
        "synchronous_attraction_validated",
        "full_network_orbital_attraction_validated",
    ):
        _require_false(riesz, key)

    bloch_source = _mapping(bloch_payload.get("source_evidence"), "Bloch source")
    bloch_scope = _mapping(bloch_payload.get("scope"), "Bloch scope")
    bloch_outer = _mapping(bloch_payload.get("outer_arc"), "Bloch outer arc")
    local = _mapping(bloch_payload.get("local_transfer"), "local transfer")
    if bloch_source.get("parameter_box_result_sha256") != evidence.parameter_box_result_sha256:
        raise ValueError("the Bloch theorem belongs to a different parameter box")
    if bloch_source.get("candidate_fingerprint") != evidence.candidate_fingerprint:
        raise ValueError("the Bloch theorem belongs to a different orbit")
    for key in (
        "periodic_branch_validated",
        "bordered_inverse_validated",
        "moving_delay_period_column_validated",
    ):
        _require_true(bloch_source, key)
    _require_true(bloch_scope, "all_nontrivial_unit_multipliers_excluded")
    _require_true(bloch_scope, "synchronous_orbital_hyperbolicity")
    _require_false(bloch_scope, "attraction")
    _require_true(
        bloch_outer, "negative_arc_mode_reversal_conjugacy_validated"
    )
    _require_true(local, "monodromy_compact")
    _require_true(local, "unit_multiplier_algebraically_simple_validated")

    transverse = _mapping(transverse_payload.get("certificate"), "transverse certificate")
    if transverse.get("parameter_box_result_sha256") != evidence.parameter_box_result_sha256:
        raise ValueError("the transverse theorem belongs to a different parameter box")
    if transverse.get("bloch_result_sha256") != evidence.bloch_result_sha256:
        raise ValueError("the transverse theorem belongs to a different Bloch theorem")
    if transverse.get("model_id") != evidence.model_id:
        raise ValueError("the transverse theorem belongs to a different model")
    for key in (
        "exact_rank_one_modal_decomposition_validated",
        "arbitrary_positive_module_sizes_formulaic_theorem",
        "periodic_transverse_variational_decay_validated",
        "full_network_orbital_hyperbolicity_validated",
    ):
        _require_true(transverse, key)
    for key in (
        "synchronous_attraction_validated",
        "full_network_attraction_validated",
        "general_network_topology_validated",
    ):
        _require_false(transverse, key)

    bloch_evidence = BlochParameterBoxEvidence(
        parameter_box_result_sha256=str(bloch_source["parameter_box_result_sha256"]),
        candidate_fingerprint=str(bloch_source["candidate_fingerprint"]),
        gain_half_width=str(bloch_source["gain_half_width"]),
        correction_radius=str(bloch_source["correction_radius"]),
        continuation_cutoff=int(bloch_source["continuation_cutoff"]),
        periodic_branch_validated=True,
        bordered_inverse_validated=True,
        moving_delay_period_column_validated=True,
    )
    return riesz, transverse, bloch_evidence


def _up(value: object, precision: int) -> gmpy2.mpfr:
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        return gmpy2.mpfr(value)


def _down(value: object, precision: int) -> gmpy2.mpfr:
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        return gmpy2.mpfr(value)


def _exp_interval(value: DirectedInterval) -> DirectedInterval:
    with gmpy2.context(precision=value.precision, round=gmpy2.RoundDown):
        lower = gmpy2.exp(value.lower)
    with gmpy2.context(precision=value.precision, round=gmpy2.RoundUp):
        upper = gmpy2.exp(value.upper)
    return DirectedInterval(lower, upper, value.precision)


def _rotation_interval(
    mode: int,
    sigma: DirectedInterval,
    phase: DirectedInterval,
    tau: DirectedInterval,
    period: DirectedInterval,
) -> DirectedComplexInterval:
    alpha = tau / period
    amplitude = _exp_interval(-(sigma * alpha))
    angle = -((pi_interval(sigma.precision) * (2 * mode) + phase) * alpha)
    return complex_unit_interval(angle) * amplitude


def _inverse_diagonal_interval(
    mode: int,
    sigma: DirectedInterval,
    phase: DirectedInterval,
) -> DirectedComplexInterval:
    omega = pi_interval(sigma.precision) * (2 * mode) + phase
    denominator = sigma * sigma + omega * omega
    return DirectedComplexInterval(sigma / denominator, -omega / denominator)


def _binary_complex_split_upper(
    value: complex,
    precision: int,
) -> gmpy2.mpfr:
    """Directed split norm of one stored binary64 complex number.

    Taking the two absolute values is exact in binary64, but adding them in
    binary64 before conversion to MPFR need not round upward.  Convert the
    components first and perform the addition under directed MPFR rounding.
    """

    stored = complex(value)
    if not math.isfinite(stored.real) or not math.isfinite(stored.imag):
        raise ValueError("a binary complex split bound requires a finite value")
    real = DirectedInterval.from_float(abs(stored.real), precision).upper
    imag = DirectedInterval.from_float(abs(stored.imag), precision).upper
    return upward_sum((real, imag), precision)


def _binary_complex_max_split_upper(
    values: np.ndarray,
    precision: int,
) -> gmpy2.mpfr:
    """Fast directed maximum of stored componentwise split norms."""

    stored_values = np.asarray(values, dtype=complex)
    if not np.all(np.isfinite(stored_values)):
        raise ValueError("a binary complex split bound requires finite values")
    # Each stored component absolute value is exact.  One rounded addition is
    # enclosed by gamma_1; max selection adds no arithmetic error.
    stored = float(
        np.max(
            np.abs(stored_values.real) + np.abs(stored_values.imag),
            initial=0.0,
        )
    )
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        unit = gmpy2.mpfr(2) ** -53
        gamma = unit / (1 - unit)
        return stored * (1 + gamma) + 2 * (gmpy2.mpfr(2) ** -1022)


def _binary_coefficients(orbit: Any) -> tuple[dict[int, complex], dict[int, complex]]:
    voltage = np.asarray(orbit.state[:, 0], dtype=float)
    count = len(voltage)
    half = count // 2
    interpolation_modes = np.concatenate((np.arange(half + 1), np.arange(-half, 0)))
    voltage_map = dict(zip(interpolation_modes, np.fft.fft(voltage) / count, strict=True))
    ordered = np.asarray([voltage_map[k] for k in range(-half, half + 1)], dtype=complex)
    centered = ordered.copy()
    centered[half] -= 1.0
    voltage_squared = np.convolve(ordered, ordered)
    centered_squared = np.convolve(centered, centered)
    modes = range(-2 * half, 2 * half + 1)
    p = orbit.parameters
    current = -voltage_squared - 3.0 * p.epsilon * p.kappa_3 * centered_squared
    delayed = 3.0 * p.epsilon * p.kappa_3 * centered_squared / 2.0
    current[2 * half] += 1.0 - p.epsilon * p.kappa_1
    delayed[2 * half] += p.epsilon * p.kappa_1 / 2.0
    return (
        dict(zip(modes, current, strict=True)),
        dict(zip(modes, delayed, strict=True)),
    )


def _coefficient_matrix(
    output_modes: np.ndarray,
    input_modes: np.ndarray,
    coefficients: Mapping[int, complex],
) -> np.ndarray:
    differences = output_modes[:, None] - input_modes[None, :]
    result = np.zeros(differences.shape, dtype=complex)
    for mode, value in coefficients.items():
        result[differences == mode] = value
    return result


def _prepare_binary_candidate(
    orbit: Any,
    base: _BaseSequences,
    precision: int,
) -> _BinaryCandidate:
    current, delayed = _binary_coefficients(orbit)
    modes = np.arange(-_CUTOFF, _CUTOFF + 1, dtype=int)
    tail_modes = np.concatenate(
        (
            np.arange(-_CUTOFF - _SUPPORT_RADIUS, -_CUTOFF, dtype=int),
            np.arange(_CUTOFF + 1, _CUTOFF + _SUPPORT_RADIUS + 1, dtype=int),
        )
    )
    current_errors: list[gmpy2.mpfr] = []
    delayed_errors: list[gmpy2.mpfr] = []
    current_binary_terms: list[gmpy2.mpfr] = []
    delayed_binary_terms: list[gmpy2.mpfr] = []
    for mode in range(-_SUPPORT_RADIUS, _SUPPORT_RADIUS + 1):
        current_errors.append(
            _box_distance_split_upper(base.current_coefficient[mode], current[mode])
        )
        delayed_errors.append(
            _box_distance_split_upper(base.delayed_state_derivative[mode], delayed[mode])
        )
        current_binary_terms.append(
            _binary_complex_split_upper(current[mode], precision)
        )
        delayed_binary_terms.append(
            _binary_complex_split_upper(delayed[mode], precision)
        )
    def mode_rotation_basis(
        requested_modes: np.ndarray,
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
            for mode, stored in zip(requested_modes, stored_values, strict=True):
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
                error = max(error, _box_distance_split_upper(exact, complex(stored)))
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

    finite_basis = mode_rotation_basis(modes)
    tail_basis = mode_rotation_basis(tail_modes)
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
        current_binary_norm=upward_sum(current_binary_terms, precision),
        delayed_binary_norm=upward_sum(delayed_binary_terms, precision),
        finite_mode_rotations=finite_basis[0],
        tail_mode_rotations=tail_basis[0],
        finite_mode_rotation_split=finite_basis[1],
        tail_mode_rotation_split=tail_basis[1],
        finite_mode_rotation_error=finite_basis[2],
        tail_mode_rotation_error=tail_basis[2],
        finite_mode_binary_split=finite_basis[3],
        tail_mode_binary_split=tail_basis[3],
    )


def _formation_error(scale: gmpy2.mpfr, rows: int, precision: int) -> gmpy2.mpfr:
    """Very conservative basic-binary-arithmetic forward error.

    Transcendental-library outputs and FFT/convolution coefficients are not
    trusted here: they are compared directly with MPFR interval enclosures.
    After those comparisons, an entry uses far fewer than 1024 rounded basic
    operations.  ``gamma_1024`` therefore dominates its assembly and complex
    multiplication/division error.  The smallest-normal term covers gradual
    underflow independently of FTZ state.
    """

    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        unit = gmpy2.mpfr(2) ** -53
        gamma = 1024 * unit / (1 - 1024 * unit)
        return gamma * scale + rows * 1024 * (gmpy2.mpfr(2) ** -1022)


def _binary_complex_matrix_split_l1_upper(
    matrix: np.ndarray,
    precision: int,
) -> gmpy2.mpfr:
    """Fast directed bound for the split l1 norm of a binary complex matrix."""

    values = np.asarray(matrix, dtype=complex)
    if values.ndim != 2 or not np.all(np.isfinite(values)):
        raise ValueError("a binary complex norm requires a finite matrix")
    rows = values.shape[0]
    # Absolute value of each real component is exact.  Each row contribution
    # uses one rounded addition and the reduction uses at most rows-1 more.
    stored_columns = np.sum(
        np.abs(values.real) + np.abs(values.imag), axis=0, dtype=float
    )
    stored = float(np.max(stored_columns, initial=0.0))
    if not math.isfinite(stored):
        raise ArithmeticError("a binary complex column sum overflowed")
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        unit = gmpy2.mpfr(2) ** -53
        gamma = (rows + 1) * unit / (1 - (rows + 1) * unit)
        return (
            gmpy2.mpfr(stored) * (1 + gamma)
            + (rows + 1) * (gmpy2.mpfr(2) ** -1022)
        )


def _binary_complex_product_split_l1_upper(
    left: np.ndarray,
    right: np.ndarray,
    precision: int,
    *,
    defect_from_identity: bool = False,
    left_norm: gmpy2.mpfr | None = None,
    right_norm: gmpy2.mpfr | None = None,
) -> gmpy2.mpfr:
    """Audit a complex binary product using four real GEMMs.

    The stored real and imaginary parts are formed explicitly as
    ``Ar Br - Ai Bi`` and ``Ar Bi + Ai Br``.  The normwise error uses
    ``gamma_(2*n+4)``: each output component contains two length-``n`` dot
    products followed by one addition/subtraction.  This deliberately
    overcounts the operations.  No complex-BLAS error model is assumed.
    """

    a = np.asarray(left, dtype=complex)
    b = np.asarray(right, dtype=complex)
    if a.ndim != 2 or b.ndim != 2 or a.shape[1] != b.shape[0]:
        raise ValueError("binary complex product shapes are incompatible")
    if not np.all(np.isfinite(a)) or not np.all(np.isfinite(b)):
        raise ValueError("binary complex product inputs must be finite")
    _binary_environment_checked()
    real = a.real @ b.real - a.imag @ b.imag
    imag = a.real @ b.imag + a.imag @ b.real
    _binary_environment_checked()
    product = real + 1.0j * imag
    if defect_from_identity:
        if product.shape[0] != product.shape[1]:
            raise ValueError("an inverse defect must be square")
        product = np.eye(product.shape[0], dtype=complex) - product
    stored = _binary_complex_matrix_split_l1_upper(product, precision)
    a_norm = left_norm or _binary_complex_matrix_split_l1_upper(a, precision)
    b_norm = right_norm or _binary_complex_matrix_split_l1_upper(b, precision)
    inner = a.shape[1]
    rows = a.shape[0]
    operations = 2 * inner + 5
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        unit = gmpy2.mpfr(2) ** -53
        gamma = operations * unit / (1 - operations * unit)
        underflow = (
            2 * rows * operations * (gmpy2.mpfr(2) ** -1022)
        )
        return stored + gamma * a_norm * b_norm + underflow


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


def _center_and_radius(rectangle: _Rectangle, precision: int) -> tuple[
    DirectedInterval, DirectedInterval, gmpy2.mpfr, str, str
]:
    with localcontext() as context:
        context.prec = 120
        sigma_decimal = (rectangle.sigma_lower + rectangle.sigma_upper) / 2
        phase_decimal = (rectangle.phase_lower + rectangle.phase_upper) / 2
    sigma_float = float(sigma_decimal)
    phase_float = float(phase_decimal)
    sigma = DirectedInterval.from_float(sigma_float, precision)
    phase = DirectedInterval.from_float(phase_float, precision)
    sigma_lower = DirectedInterval.from_decimal(format(rectangle.sigma_lower, "f"), precision)
    sigma_upper = DirectedInterval.from_decimal(format(rectangle.sigma_upper, "f"), precision)
    phase_lower = DirectedInterval.from_decimal(format(rectangle.phase_lower, "f"), precision)
    phase_upper = DirectedInterval.from_decimal(format(rectangle.phase_upper, "f"), precision)
    if sigma.lower < sigma_lower.lower or sigma.upper > sigma_upper.upper:
        raise ArithmeticError("binary sigma centre escaped its rectangle")
    if phase.lower < phase_lower.lower or phase.upper > phase_upper.upper:
        raise ArithmeticError("binary phase centre escaped its rectangle")
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        dx = max(sigma.upper - sigma_lower.lower, sigma_upper.upper - sigma.lower)
        dy = max(phase.upper - phase_lower.lower, phase_upper.upper - phase.lower)
        radius = dx + dy
    return sigma, phase, radius, format(sigma_float, ".17g"), format(phase_float, ".17g")


def _rotation_data(
    mode_rotations: tuple[np.ndarray, np.ndarray],
    mode_rotation_split: tuple[gmpy2.mpfr, gmpy2.mpfr],
    mode_rotation_error: tuple[gmpy2.mpfr, gmpy2.mpfr],
    mode_binary_split: tuple[gmpy2.mpfr, gmpy2.mpfr],
    sigma: DirectedInterval,
    phase: DirectedInterval,
    base: _BaseSequences,
    precision: int,
) -> tuple[tuple[np.ndarray, np.ndarray], gmpy2.mpfr, gmpy2.mpfr]:
    binary_by_delay: list[np.ndarray] = []
    maximum_split = _up(0, precision)
    maximum_error = _up(0, precision)
    sigma_float = float(sigma.lower)
    phase_float = float(phase.lower)
    period_float = float(base.period.lower)
    for delay_index, tau in enumerate(
        (base.parameters["tau_0"], base.parameters["tau_1"])
    ):
        tau_float = float(tau.lower)
        alpha_float = tau_float / period_float
        factor_binary = np.exp(
            -complex(sigma_float, phase_float) * alpha_float
        )
        binary = factor_binary * mode_rotations[delay_index]
        binary_by_delay.append(binary)
        alpha = tau / base.period
        factor_exact = DirectedComplexInterval.from_real(
            _exp_interval(-(sigma * alpha))
        ) * complex_unit_interval(-(phase * alpha))
        factor_split = upward_sum(
            (factor_exact.real.upper_abs(), factor_exact.imag.upper_abs()),
            precision,
        )
        factor_error = _box_distance_split_upper(
            factor_exact, complex(factor_binary)
        )
        with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
            split_bound = factor_split * mode_rotation_split[delay_index]
            error_bound = (
                factor_split * mode_rotation_error[delay_index]
                + factor_error * mode_binary_split[delay_index]
                + _formation_error(
                    factor_split * mode_rotation_split[delay_index],
                    1,
                    precision,
                )
            )
        maximum_split = max(maximum_split, split_bound)
        maximum_error = max(maximum_error, error_bound)
    return (binary_by_delay[0], binary_by_delay[1]), maximum_split, maximum_error


def _candidate_matrices(
    candidate: _BinaryCandidate,
    base: _BaseSequences,
    sigma: DirectedInterval,
    phase: DirectedInterval,
    precision: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, dict[str, gmpy2.mpfr]]:
    modes = candidate.modes
    tail_modes = candidate.tail_modes
    period = float(base.period.lower)
    epsilon = float(base.parameters["epsilon"].lower)
    tau_values = (
        float(base.parameters["tau_0"].lower),
        float(base.parameters["tau_1"].lower),
    )
    finite_rotations, finite_rotation_split, finite_rotation_error = _rotation_data(
        candidate.finite_mode_rotations,
        candidate.finite_mode_rotation_split,
        candidate.finite_mode_rotation_error,
        candidate.finite_mode_binary_split,
        sigma,
        phase,
        base,
        precision,
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
    for tau, rotation in zip(tau_values, finite_rotations, strict=True):
        top -= period * rotation[:, None] * candidate.delayed_finite
        derivative_top += tau * rotation[:, None] * candidate.delayed_finite
    identity = np.eye(len(modes), dtype=complex)
    zero = np.zeros_like(identity)
    finite = np.block(
        [
            [top, period * identity],
            [-period * epsilon * identity, np.diag(finite_frequency)],
        ]
    )
    derivative = np.block(
        [[derivative_top, zero], [zero, identity]]
    )

    finite_tail_top = -period * candidate.current_finite_tail
    finite_tail_derivative_top = np.zeros_like(finite_tail_top)
    for tau, rotation in zip(tau_values, finite_rotations, strict=True):
        finite_tail_top -= period * rotation[:, None] * candidate.delayed_finite_tail
        finite_tail_derivative_top += tau * rotation[:, None] * candidate.delayed_finite_tail
    finite_tail = np.vstack((finite_tail_top, np.zeros_like(finite_tail_top)))
    finite_tail_derivative = np.vstack(
        (finite_tail_derivative_top, np.zeros_like(finite_tail_derivative_top))
    )

    tail_finite = -period * candidate.current_tail_finite
    tail_finite_derivative = np.zeros_like(tail_finite)
    for tau, rotation in zip(tau_values, tail_rotations, strict=True):
        tail_finite -= period * rotation[:, None] * candidate.delayed_tail_finite
        tail_finite_derivative += tau * rotation[:, None] * candidate.delayed_tail_finite

    current_exact = _sequence_box_norm_upper(base.current_coefficient, precision)
    delayed_exact = _sequence_box_norm_upper(base.delayed_state_derivative, precision)
    maximum_frequency = _up(0, precision)
    maximum_diagonal_error = _up(0, precision)
    for mode, stored in zip(modes, finite_frequency, strict=True):
        exact = DirectedComplexInterval(
            sigma,
            pi_interval(precision) * (2 * int(mode)) + phase,
        )
        maximum_frequency = max(
            maximum_frequency,
            upward_sum((exact.real.upper_abs(), exact.imag.upper_abs()), precision),
        )
        maximum_diagonal_error = max(
            maximum_diagonal_error,
            _box_distance_split_upper(exact, complex(stored)),
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
            base.parameters["tau_0"].upper + base.parameters["tau_1"].upper
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
            base.parameters["tau_0"].upper + base.parameters["tau_1"].upper
        ) * (
            tail_rotation_split * candidate.delayed_error_norm
            + tail_rotation_error * candidate.delayed_binary_norm
        )
        finite_scale = max(
            maximum_frequency
            + base.period.upper
            * (
                current_exact + 2 * finite_rotation_split * delayed_exact
            )
            + base.period.upper * base.parameters["epsilon"].upper,
            base.period.upper,
        )
        derivative_scale = max(
            1
            + (base.parameters["tau_0"].upper + base.parameters["tau_1"].upper)
            * finite_rotation_split
            * delayed_exact,
            gmpy2.mpfr(1),
        )
        finite_conv_scale = base.period.upper * (
            current_exact + 2 * finite_rotation_split * delayed_exact
        )
        finite_derivative_conv_scale = (
            base.parameters["tau_0"].upper + base.parameters["tau_1"].upper
        ) * finite_rotation_split * delayed_exact
        tail_conv_scale = base.period.upper * (
            current_exact + 2 * tail_rotation_split * delayed_exact
        )
        tail_derivative_conv_scale = (
            base.parameters["tau_0"].upper + base.parameters["tau_1"].upper
        ) * tail_rotation_split * delayed_exact
        coupling_exact = base.period * base.parameters["epsilon"]
        coupling_stored = complex(-period * epsilon, 0.0)
        coupling_error = _box_distance_split_upper(
            DirectedComplexInterval.from_real(-coupling_exact), coupling_stored
        )
        finite_error = (
            maximum_diagonal_error
            + finite_conv_error
            + coupling_error
            + _formation_error(finite_scale, len(modes), precision)
        )
        derivative_error = finite_derivative_error + _formation_error(
            derivative_scale, len(modes), precision
        )
        finite_tail_error = finite_conv_error + _formation_error(
            finite_conv_scale, len(modes), precision
        )
        finite_tail_derivative_error = finite_derivative_error + _formation_error(
            finite_derivative_conv_scale, len(modes), precision
        )
        tail_finite_error = tail_conv_error + _formation_error(
            tail_conv_scale, len(tail_modes), precision
        )
        tail_finite_derivative_error = tail_derivative_error + _formation_error(
            tail_derivative_conv_scale, len(tail_modes), precision
        )
    errors = {
        "finite": finite_error,
        "derivative": derivative_error,
        "finite_tail": finite_tail_error,
        "finite_tail_derivative": finite_tail_derivative_error,
        "tail_finite": tail_finite_error,
        "tail_finite_derivative": tail_finite_derivative_error,
    }
    return (
        finite,
        derivative,
        finite_tail,
        finite_tail_derivative,
        tail_finite,
        tail_finite_derivative,
        errors,
    )


def _parameter_corrections(
    base: _BaseSequences,
    box: _BaseSequences,
    correction_radius: DirectedInterval,
    sigma_upper: Decimal,
    phase_lower: Decimal,
    phase_upper: Decimal,
    split_radius: gmpy2.mpfr,
    tail_inverse_split: gmpy2.mpfr,
    precision: int,
) -> tuple[gmpy2.mpfr, gmpy2.mpfr, gmpy2.mpfr, dict[str, gmpy2.mpfr]]:
    r = correction_radius.upper
    current_center = _sequence_box_norm_upper(base.current_coefficient, precision)
    delayed_center = _sequence_box_norm_upper(base.delayed_state_derivative, precision)
    voltage = _sequence_box_norm_upper(base.voltage, precision)
    centered = _sequence_box_norm_upper(base.centered_voltage, precision)
    epsilon = base.parameters["epsilon"].upper
    kappa_3_max = box.parameters["kappa_3"].upper
    h1 = (box.parameters["kappa_1"] - base.parameters["kappa_1"]).upper_abs()
    h3 = (box.parameters["kappa_3"] - base.parameters["kappa_3"]).upper_abs()
    sqrt_two = DirectedInterval.from_decimal(2, precision).sqrt().upper
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        common = kappa_3_max * (2 * centered + r) * r + h3 * centered * centered
        current_variation = (2 * voltage + r) * r + epsilon * h1 + 3 * epsilon * common
        delayed_variation = epsilon * (h1 + 3 * common) / 2
        current_uniform = current_center + current_variation
        delayed_uniform = delayed_center + delayed_variation
    period_lower = (base.period - correction_radius).lower
    period_upper = (base.period + correction_radius).upper
    if period_lower <= 0:
        raise ArithmeticError("the exact orbit ball crosses nonpositive periods")
    sigma_box = DirectedInterval.from_decimal(format(sigma_upper, "f"), precision)
    phase_abs = max(abs(phase_lower), abs(phase_upper))
    phase_box = DirectedInterval.from_decimal(format(phase_abs, "f"), precision)
    frequency = (
        sigma_box * sigma_box
        + (pi_interval(precision) * (2 * _CUTOFF) + phase_box) ** 2
    ).sqrt().upper
    delayed_terms: list[gmpy2.mpfr] = []
    tail_delayed_terms: list[gmpy2.mpfr] = []
    for tau in (base.parameters["tau_0"], base.parameters["tau_1"]):
        with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
            common_finite = (
                r * delayed_uniform
                + base.period.upper * delayed_variation
                + delayed_center * tau.upper * frequency * r / period_lower
            )
            delayed_terms.append(sqrt_two * common_finite)
            tail_delayed_terms.append(
                sqrt_two
                * (
                    tail_inverse_split
                    * (r * delayed_uniform + base.period.upper * delayed_variation)
                    + delayed_center
                    * tau.upper
                    * r
                    / period_lower
                    * (1 + tail_inverse_split * split_radius)
                )
            )
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        current_term = r * current_uniform + base.period.upper * current_variation
        finite_convolution = current_term + sum(delayed_terms, gmpy2.mpfr(0))
        finite_full = max(finite_convolution + epsilon * r, r)
        tail_correction = (
            tail_inverse_split * current_term
            + sum(tail_delayed_terms, gmpy2.mpfr(0))
        )
        lower_order_split = max(
            current_uniform + 2 * sqrt_two * delayed_uniform + epsilon,
            gmpy2.mpfr(1),
        )
    values = {
        "current_center": current_center,
        "current_uniform": current_uniform,
        "delayed_center": delayed_center,
        "delayed_uniform": delayed_uniform,
        "period_upper": period_upper,
        "period_lower": period_lower,
        "lower_order_split": lower_order_split,
    }
    return finite_convolution, finite_full, tail_correction, values


def _validate_cell(
    rectangle: _Rectangle,
    candidate: _BinaryCandidate,
    base: _BaseSequences,
    box: _BaseSequences,
    correction_radius: DirectedInterval,
    precision: int,
    acceptance_threshold: Decimal,
) -> _CellBounds:
    sigma, phase, h, sigma_text, phase_text = _center_and_radius(rectangle, precision)
    if rectangle.sigma_lower < 0:
        raise ValueError("a Taylor rectangle left the closed right half-plane")
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
        mu = (
            _binary_complex_product_split_l1_upper(
                inverse,
                derivative,
                precision,
                left_norm=inverse_norm,
            )
            + inverse_norm * errors["derivative"]
        )
        p0 = (
            _binary_complex_product_split_l1_upper(
                inverse,
                finite_tail,
                precision,
                left_norm=inverse_norm,
            )
            + inverse_norm * errors["finite_tail"]
        )
        p1 = (
            _binary_complex_product_split_l1_upper(
                inverse,
                finite_tail_derivative,
                precision,
                left_norm=inverse_norm,
            )
            + inverse_norm * errors["finite_tail_derivative"]
        )

    tail_frequency_binary = complex(float(sigma.lower), float(phase.lower)) + (
        2.0j * math.pi * candidate.tail_modes
    )
    tail_inverse_binary = 1.0 / tail_frequency_binary
    # For 0 <= sigma <= 128 and every tail frequency |omega| >= 129*pi,
    # (sigma+|omega|)/(sigma^2+omega^2) decreases with |omega|.  Hence the
    # two nearest tail modes +/-65 give the exact split-norm supremum over
    # the infinite tail.
    if sigma.upper > DirectedInterval.from_decimal(128, precision).upper:
        raise ArithmeticError("the tail inverse monotonicity range was exceeded")
    nearest_inverse = (
        _inverse_diagonal_interval(-(_CUTOFF + 1), sigma, phase),
        _inverse_diagonal_interval(_CUTOFF + 1, sigma, phase),
    )
    tail_inverse_split = max(
        upward_sum((value.real.upper_abs(), value.imag.upper_abs()), precision)
        for value in nearest_inverse
    )
    binary_inverse_split = _binary_complex_max_split_upper(
        tail_inverse_binary,
        precision,
    )
    pi_point = DirectedInterval.from_float(math.pi, precision)
    pi_error = (pi_interval(precision) - pi_point).upper_abs()
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        largest_tail_mode = int(np.max(np.abs(candidate.tail_modes)))
        maximum_tail_frequency_split = (
            sigma.upper
            + phase.upper_abs()
            + 2 * largest_tail_mode * pi_interval(precision).upper
        )
        # Besides the stored-pi error, enclose all basic binary operations in
        # forming sigma+i(phi+2*pi*k).  This deliberately oversized gamma_1024
        # term avoids relying on a vector-ufunc evaluation order.
        diagonal_error = (
            2 * largest_tail_mode * pi_error
            + _formation_error(maximum_tail_frequency_split, 1, precision)
        )
        inverse_formation_error = _formation_error(
            binary_inverse_split,
            1,
            precision,
        )
        resolvent_correction = tail_inverse_split * diagonal_error
        tail_inverse_error = (
            resolvent_correction * binary_inverse_split
            + (1 + resolvent_correction) * inverse_formation_error
        )
    normalized_tail_finite = tail_inverse_binary[:, None] * tail_finite
    normalized_tail_finite_derivative = (
        tail_inverse_binary[:, None] * tail_finite_derivative
    )
    q0_binary = _binary_complex_matrix_split_l1_upper(normalized_tail_finite, precision)
    q1_binary = _binary_complex_matrix_split_l1_upper(
        normalized_tail_finite_derivative, precision
    )
    tail_finite_norm = _binary_complex_matrix_split_l1_upper(tail_finite, precision)
    tail_finite_derivative_norm = _binary_complex_matrix_split_l1_upper(
        tail_finite_derivative, precision
    )
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        q0 = (
            q0_binary
            + tail_inverse_split * errors["tail_finite"]
            + tail_inverse_error * tail_finite_norm
            + _formation_error(q0_binary, len(candidate.tail_modes), precision)
        )
        q1 = (
            q1_binary
            + tail_inverse_split * errors["tail_finite_derivative"]
            + tail_inverse_error * tail_finite_derivative_norm
            + _formation_error(q1_binary, len(candidate.tail_modes), precision)
        )

    finite_convolution_correction, finite_full_correction, tail_correction, values = (
        _parameter_corrections(
            base,
            box,
            correction_radius,
            rectangle.sigma_upper,
            rectangle.phase_lower,
            rectangle.phase_upper,
            h,
            tail_inverse_split,
            precision,
        )
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
        tail_second = tail_inverse_split * second_raw
        z_pp = (
            eta
            + h * mu
            + h * h * finite_second
            + inverse_norm * finite_full_correction
        )
        z_pq = (
            p0
            + h * p1
            + h * h * finite_second
            + inverse_norm * finite_convolution_correction
        )
        z_qp = (
            q0
            + h * q1
            + h * h * tail_second
            + tail_correction
        )
        z_qq = tail_inverse_split * (
            h + values["period_upper"] * values["lower_order_split"]
        )
        finite_input = z_pp + z_qp
        tail_input = z_pq + z_qq
        contraction = max(finite_input, tail_input)
    finite_input_text = _exact_decimal_sum(
        (decimal_upper(z_pp), decimal_upper(z_qp))
    )
    tail_input_text = _exact_decimal_sum(
        (decimal_upper(z_pq), decimal_upper(z_qq))
    )
    contraction_text = str(max(Decimal(finite_input_text), Decimal(tail_input_text)))
    margin_text = _margin(contraction_text)
    validated = (
        Decimal(contraction_text) < 1
        and Decimal(contraction_text) <= acceptance_threshold
        and Decimal(margin_text) > 0
    )
    leaf = CoverLeaf(
        root_id=rectangle.root_id,
        path=rectangle.path,
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
        finite_first_product_upper=decimal_upper(mu),
        finite_from_tail_center_upper=decimal_upper(p0),
        finite_from_tail_first_upper=decimal_upper(p1),
        tail_from_finite_center_upper=decimal_upper(q0),
        tail_from_finite_first_upper=decimal_upper(q1),
        tail_diagonal_inverse_split_upper=decimal_upper(tail_inverse_split),
        finite_full_parameter_correction_upper=decimal_upper(finite_full_correction),
        finite_convolution_parameter_correction_upper=decimal_upper(
            finite_convolution_correction
        ),
        tail_from_finite_parameter_correction_upper=decimal_upper(tail_correction),
        finite_to_finite_upper=decimal_upper(z_pp),
        finite_from_tail_upper=decimal_upper(z_pq),
        tail_from_finite_upper=decimal_upper(z_qp),
        tail_to_tail_upper=decimal_upper(z_qq),
        finite_input_column_sum_upper=finite_input_text,
        tail_input_column_sum_upper=tail_input_text,
        contraction_upper=contraction_text,
        contraction_margin_lower=margin_text,
    )
    return _CellBounds(leaf=leaf, worst=worst, validated=validated)


def _split_rectangle(rectangle: _Rectangle) -> tuple[_Rectangle, _Rectangle]:
    sigma_width = rectangle.sigma_upper - rectangle.sigma_lower
    phase_width = rectangle.phase_upper - rectangle.phase_lower
    if sigma_width >= phase_width:
        midpoint = (rectangle.sigma_lower + rectangle.sigma_upper) / 2
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


def _root_rectangles(rho: Decimal, phase_outer: Decimal) -> tuple[_Rectangle, ...]:
    return (
        _Rectangle(
            "main_upper",
            "",
            rho,
            _OUTER_REAL_PART,
            Decimal(0),
            phase_outer,
        ),
        _Rectangle(
            "upper_cap",
            "",
            Decimal(0),
            rho,
            rho,
            phase_outer,
        ),
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


def _prefix_complete(leaves: Sequence[CoverLeaf], root_ids: Sequence[str]) -> bool:
    by_root = {root: [] for root in root_ids}
    for leaf in leaves:
        if leaf.root_id not in by_root or len(leaf.path) % 2:
            return False
        tokens = tuple(leaf.path[index : index + 2] for index in range(0, len(leaf.path), 2))
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
        kraft = sum(Fraction(1, 2 ** len(path)) for path in paths)
        if kraft != 1:
            return False
    return True


def _leaf_digest(leaves: Sequence[CoverLeaf]) -> str:
    lines = [
        "|".join(
            (
                leaf.root_id,
                leaf.path,
                leaf.contraction_upper,
                leaf.finite_input_column_sum_upper,
                leaf.tail_input_column_sum_upper,
            )
        )
        for leaf in sorted(leaves, key=lambda item: (item.root_id, item.path))
    ]
    return sha256(("\n".join(lines) + "\n").encode("ascii")).hexdigest()


def build_right_half_zero_free_cover(
    bloch_payload: Mapping[str, Any],
    riesz_payload: Mapping[str, Any],
    transverse_payload: Mapping[str, Any],
    candidate_payload: Mapping[str, Any],
    evidence: RightHalfCoverEvidence,
    *,
    precision: int = 160,
    acceptance_threshold: str = "0.98",
    maximum_processed_cells: int = 100000,
    maximum_depth: int = 80,
    progress: Callable[[int, int, int], None] | None = None,
) -> RightHalfZeroFreeCover:
    """Build the adaptive directed cover or an explicit incomplete budget."""

    _validate_evidence(evidence)
    riesz, transverse, bloch_evidence = _validate_sources(
        bloch_payload, riesz_payload, transverse_payload, evidence
    )
    orbit = _orbit_from_payload(candidate_payload)
    _binary_environment_checked()
    # The expensive D1 continuation is already a hash-bound source theorem.
    # Rebuild only the exact directed coefficient sequences used by this new
    # proof; do not replay the unrelated bordered Newton finite/tail argument
    # once for every cover run.
    base = _build_base_sequences(orbit, precision)
    box = _build_parameter_box_sequences(
        orbit, precision, bloch_evidence.gain_half_width
    )
    radius = DirectedInterval.from_decimal(
        bloch_evidence.correction_radius, precision
    )
    candidate = _prepare_binary_candidate(orbit, base, precision)
    threshold = Decimal(acceptance_threshold)
    if not Decimal(0) < threshold < Decimal(1):
        raise ValueError("the acceptance threshold must lie strictly between zero and one")
    if maximum_processed_cells < 1:
        raise ValueError("the cell budget must be positive")
    local_radius = Decimal(str(riesz["local_complex_exclusion_radius_lower"]))
    rho = Decimal(str(riesz["local_complex_keyhole_radius"]))
    phase_outer = Decimal(str(riesz["logarithmic_strip_imaginary_upper"]))
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        corner = (
            DirectedInterval.from_decimal(str(rho), precision)
            * DirectedInterval.from_decimal(2, precision).sqrt()
        ).upper
    local_lower = DirectedInterval.from_decimal(str(local_radius), precision).lower
    local_geometry = corner < local_lower
    if not local_geometry:
        raise ArithmeticError("the half-square does not fit strictly in the local disk")
    # It is enough to cover Im(s)>=0.  For the real exact periodic branch,
    # (Cy)_k=conj(y_{-k}) gives C L_s C^{-1}=L_conj(s); hence every negative
    # half-strip point is conjugate to its positive counterpart.  The source
    # Bloch theorem already audits the same mode-reversal conjugacy on the
    # imaginary axis, and adding the real scalar sigma does not alter it.
    roots = _root_rectangles(rho, phase_outer)
    pending = list(reversed(roots))
    leaves: list[CoverLeaf] = []
    worst: WorstCoverCell | None = None
    processed = 0
    deepest = 0
    while pending and processed < maximum_processed_cells:
        rectangle = pending.pop()
        depth = len(rectangle.path) // 2
        deepest = max(deepest, depth)
        bounds = _validate_cell(
            rectangle,
            candidate,
            base,
            box,
            radius,
            precision,
            threshold,
        )
        processed += 1
        if bounds.validated:
            leaves.append(bounds.leaf)
            if worst is None or Decimal(bounds.worst.contraction_upper) > Decimal(
                worst.contraction_upper
            ):
                worst = bounds.worst
        else:
            if depth >= maximum_depth:
                pending.append(rectangle)
                break
            first, second = _split_rectangle(rectangle)
            pending.extend((second, first))
        if progress is not None and processed % 100 == 0:
            progress(processed, len(leaves), len(pending))
    complete = not pending
    prefix_complete = complete and _prefix_complete(
        leaves, tuple(root.root_id for root in roots)
    )
    maximum_contraction = (
        max((Decimal(leaf.contraction_upper) for leaf in leaves), default=None)
    )
    minimum_margin = (
        None
        if maximum_contraction is None
        else _margin(format(maximum_contraction, "f"))
    )
    every_leaf_strict = bool(leaves) and all(
        Decimal(leaf.contraction_upper) < 1 for leaf in leaves
    )
    conjugacy = True
    zero_free = (
        complete
        and prefix_complete
        and every_leaf_strict
        and local_geometry
        and conjugacy
    )
    winding_lower = 0 if zero_free else None
    winding_upper = 0 if zero_free else None
    zero_count = 0 if zero_free else None
    # A zero-free homotopy of the left-preconditioned full operator is
    # supplied by t -> I-t(I-A L_s) on every rectangle.  The union plus the
    # local punctured disk gives a globally zero-free keyhole, so its
    # argument-principle winding is exactly zero.
    preconditioned_operator_homotopy = zero_free
    unstable_index_zero = zero_free
    synchronous_linear = zero_free
    fixed_network_linear = zero_free and bool(
        transverse["periodic_transverse_variational_decay_validated"]
    )
    # The RFDE vector field is polynomial (hence C-infinity), one-period smoothing
    # gives compact monodromy, the translation multiplier is simple, and the
    # cover excludes every other multiplier on or outside the unit circle.
    # The standard RFDE principle of linearized orbital stability therefore
    # promotes the spectral conclusion to local nonlinear orbital attraction.
    linearized_stability_theorem = zero_free
    reason = None
    if not zero_free:
        reason = (
            f"directed cover incomplete: processed={processed}, "
            f"accepted={len(leaves)}, pending={len(pending)}; "
            "subdivide every pending rectangle until both input-column "
            "bounds are below one"
        )
    return RightHalfZeroFreeCover(
        model_id=evidence.model_id,
        parameter_box_result_sha256=evidence.parameter_box_result_sha256,
        bloch_result_sha256=evidence.bloch_result_sha256,
        riesz_result_sha256=evidence.riesz_result_sha256,
        transverse_result_sha256=evidence.transverse_result_sha256,
        candidate_result_sha256=evidence.candidate_result_sha256,
        candidate_fingerprint=evidence.candidate_fingerprint,
        precision_bits=precision,
        norm_id=_NORM_ID,
        cutoff=_CUTOFF,
        complex_finite_dimension=2 * (2 * _CUTOFF + 1),
        coefficient_support_half_bandwidth=_SUPPORT_RADIUS,
        outer_real_part=str(_OUTER_REAL_PART),
        fundamental_phase_lower=str(riesz["logarithmic_strip_imaginary_lower"]),
        fundamental_phase_upper=str(riesz["logarithmic_strip_imaginary_upper"]),
        local_complex_exclusion_radius_lower=str(local_radius),
        half_square_radius=str(rho),
        half_square_corner_radius_upper=decimal_upper(corner),
        half_square_strictly_inside_local_disk=local_geometry,
        root_rectangle_count=len(roots),
        accepted_leaf_count=len(leaves),
        processed_cell_count=processed,
        pending_cell_count=len(pending),
        maximum_depth=deepest,
        acceptance_threshold=str(threshold),
        maximum_contraction_upper=(
            None if maximum_contraction is None else format(maximum_contraction, "f")
        ),
        minimum_contraction_margin_lower=(
            minimum_margin
        ),
        leaf_partition_sha256=_leaf_digest(leaves),
        binary_environment_validated=True,
        exact_parameter_box_orbit_ball_included_everywhere=True,
        complex_s_taylor_segment_stays_in_closed_right_half_plane=True,
        correct_split_tail_diagonal_inverse_used=True,
        negative_half_strip_mode_reversal_conjugacy_validated=conjugacy,
        prefix_complete_dyadic_cover_validated=prefix_complete,
        entire_keyhole_region_zero_free_validated=zero_free,
        cellwise_left_preconditioned_full_operator_neumann_homotopy_validated=(
            preconditioned_operator_homotopy
        ),
        # The stronger left-preconditioned full-operator homotopy supersedes,
        # but is not renamed as, the previously proposed exact-Schur-to-
        # candidate homotopy.
        exact_schur_to_candidate_finite_homotopy_validated=False,
        schur_boundary_winding_deduced_exactly_lower=winding_lower,
        schur_boundary_winding_deduced_exactly_upper=winding_upper,
        directed_nontranslation_right_half_strip_zero_count=zero_count,
        spectral_set_correspondence_used_without_general_multiplicity_bridge=zero_free,
        synchronous_nontranslation_unstable_index_zero_validated=(
            unstable_index_zero
        ),
        synchronous_linear_orbital_attraction_validated=synchronous_linear,
        hale_verduyn_lunel_hyperbolic_periodic_orbit_theorem_applied=(
            linearized_stability_theorem
        ),
        synchronous_nonlinear_orbital_attraction_validated=(
            linearized_stability_theorem
        ),
        fixed_rank_one_full_network_linear_orbital_attraction_validated=(
            fixed_network_linear
        ),
        fixed_rank_one_full_network_nonlinear_orbital_attraction_validated=(
            fixed_network_linear and linearized_stability_theorem
        ),
        general_network_topology_validated=False,
        biological_pulse_capture_validated=False,
        leaves=tuple(sorted(leaves, key=lambda item: (item.root_id, item.path))),
        worst_cell=worst,
        failure_reason=reason,
    )


def validate_right_half_cover_payload(payload: Mapping[str, Any]) -> None:
    """Structural/provenance validation of the tracked serialized result.

    This deliberately does not recompute 32,000 directed cell bounds.  The
    numerical proof is completed by a byte-identical full replay; this
    validator checks fixed scope, geometry, provenance and cover structure.
    """

    root = _mapping(payload, "right-half cover result")
    certificate = _mapping(root.get("certificate"), "right-half cover certificate")
    source = _mapping(root.get("source_evidence"), "right-half cover source")
    expected = {
        "parameter_box_result_sha256": _PARAMETER_BOX_SHA256,
        "bloch_result_sha256": _BLOCH_SHA256,
        "riesz_result_sha256": _RIESZ_SHA256,
        "transverse_result_sha256": _TRANSVERSE_SHA256,
        "candidate_result_sha256": _CANDIDATE_SHA256,
        "candidate_fingerprint": _CANDIDATE_FINGERPRINT,
        "model_id": _MODEL_ID,
    }
    if any(source.get(key) != value for key, value in expected.items()):
        raise ValueError("the serialized cover has stale source evidence")
    if any(certificate.get(key) != value for key, value in expected.items()):
        raise ValueError("the certificate/source evidence fields disagree")
    if certificate.get("norm_id") != _NORM_ID:
        raise ValueError("the serialized cover uses the wrong computational norm")
    fixed_geometry: dict[str, object] = {
        "precision_bits": 160,
        "cutoff": _CUTOFF,
        "complex_finite_dimension": 2 * (2 * _CUTOFF + 1),
        "coefficient_support_half_bandwidth": _SUPPORT_RADIUS,
        "outer_real_part": str(_OUTER_REAL_PART),
        "fundamental_phase_lower": _FUNDAMENTAL_PHASE_LOWER,
        "fundamental_phase_upper": _FUNDAMENTAL_PHASE_UPPER,
        "local_complex_exclusion_radius_lower": _LOCAL_COMPLEX_EXCLUSION_RADIUS,
        "half_square_radius": _HALF_SQUARE_RADIUS,
        "root_rectangle_count": 2,
        "acceptance_threshold": "0.995",
    }
    if any(certificate.get(key) != value for key, value in fixed_geometry.items()):
        raise ValueError("the serialized fixed keyhole geometry changed")
    with gmpy2.context(precision=160, round=gmpy2.RoundUp):
        expected_corner = (
            DirectedInterval.from_decimal(_HALF_SQUARE_RADIUS, 160)
            * DirectedInterval.from_decimal(2, 160).sqrt()
        ).upper
    if certificate.get("half_square_corner_radius_upper") != decimal_upper(
        expected_corner
    ):
        raise ValueError("the serialized half-square corner bound changed")
    leaves_value = certificate.get("leaves")
    if not isinstance(leaves_value, list):
        raise ValueError("the serialized cover leaf list is absent")
    leaves = tuple(
        CoverLeaf(
            root_id=str(_mapping(value, "cover leaf")["root_id"]),
            path=str(_mapping(value, "cover leaf")["path"]),
            contraction_upper=str(_mapping(value, "cover leaf")["contraction_upper"]),
            finite_input_column_sum_upper=str(
                _mapping(value, "cover leaf")["finite_input_column_sum_upper"]
            ),
            tail_input_column_sum_upper=str(
                _mapping(value, "cover leaf")["tail_input_column_sum_upper"]
            ),
        )
        for value in leaves_value
    )
    if _leaf_digest(leaves) != certificate.get("leaf_partition_sha256"):
        raise ValueError("the serialized cover leaf digest changed")
    if certificate.get("accepted_leaf_count") != len(leaves):
        raise ValueError("the serialized accepted-leaf count changed")
    if certificate.get("root_rectangle_count") != 2:
        raise ValueError("the positive-half-strip root geometry changed")
    complete = certificate.get("pending_cell_count") == 0
    prefix = _prefix_complete(leaves, ("main_upper", "upper_cap")) if complete else False
    if bool(certificate.get("prefix_complete_dyadic_cover_validated")) != prefix:
        raise ValueError("the serialized dyadic coverage flag is inconsistent")
    zero_free = bool(certificate.get("entire_keyhole_region_zero_free_validated"))
    if zero_free:
        if certificate.get("processed_cell_count") != 2 * len(leaves) - 2:
            raise ValueError("the complete two-root binary-forest count is inconsistent")
        maximum = max(Decimal(leaf.contraction_upper) for leaf in leaves)
        if maximum != Decimal(str(certificate.get("maximum_contraction_upper"))):
            raise ValueError("the serialized maximum leaf contraction changed")
        if _margin(format(maximum, "f")) != str(
            certificate.get("minimum_contraction_margin_lower")
        ):
            raise ValueError("the serialized contraction margin changed")
        if maximum > Decimal(str(certificate.get("acceptance_threshold"))):
            raise ValueError("a leaf exceeds the declared acceptance threshold")
        worst_value = _mapping(certificate.get("worst_cell"), "tightest leaf")
        if Decimal(str(worst_value.get("contraction_upper"))) != maximum:
            raise ValueError("the detailed tightest leaf is not the maximum leaf")
        roots = {
            item.root_id: item
            for item in _root_rectangles(
                Decimal(_HALF_SQUARE_RADIUS),
                Decimal(_FUNDAMENTAL_PHASE_UPPER),
            )
        }
        worst_root = str(worst_value.get("root_id"))
        if worst_root not in roots:
            raise ValueError("the tightest leaf has an unknown root")
        worst_path = str(worst_value.get("path"))
        reconstructed = _rectangle_from_path(roots[worst_root], worst_path)
        rectangle_fields = {
            "sigma_lower": format(reconstructed.sigma_lower, "f"),
            "sigma_upper": format(reconstructed.sigma_upper, "f"),
            "phase_lower": format(reconstructed.phase_lower, "f"),
            "phase_upper": format(reconstructed.phase_upper, "f"),
        }
        if any(worst_value.get(key) != value for key, value in rectangle_fields.items()):
            raise ValueError("the tightest leaf geometry does not match its path")
        _, _, reconstructed_radius, sigma_text, phase_text = _center_and_radius(
            reconstructed,
            160,
        )
        if (
            worst_value.get("sigma_center_binary64") != sigma_text
            or worst_value.get("phase_center_binary64") != phase_text
            or worst_value.get("split_parameter_radius_upper")
            != decimal_upper(reconstructed_radius)
        ):
            raise ValueError("the tightest leaf centre/radius changed")
        matching_leaves = [
            leaf
            for leaf in leaves
            if leaf.root_id == worst_root and leaf.path == worst_path
        ]
        if len(matching_leaves) != 1:
            raise ValueError("the tightest leaf is absent or duplicated")
        matching = matching_leaves[0]
        if (
            matching.contraction_upper != str(worst_value.get("contraction_upper"))
            or matching.finite_input_column_sum_upper
            != str(worst_value.get("finite_input_column_sum_upper"))
            or matching.tail_input_column_sum_upper
            != str(worst_value.get("tail_input_column_sum_upper"))
        ):
            raise ValueError("the tightest leaf details disagree with its leaf record")
        if Decimal(str(certificate.get("half_square_corner_radius_upper"))) >= Decimal(
            str(certificate.get("local_complex_exclusion_radius_lower"))
        ):
            raise ValueError("the serialized half-square left the local disk")
        for key in (
            "half_square_strictly_inside_local_disk",
            "exact_parameter_box_orbit_ball_included_everywhere",
            "complex_s_taylor_segment_stays_in_closed_right_half_plane",
            "correct_split_tail_diagonal_inverse_used",
            "negative_half_strip_mode_reversal_conjugacy_validated",
            "prefix_complete_dyadic_cover_validated",
            "cellwise_left_preconditioned_full_operator_neumann_homotopy_validated",
            "spectral_set_correspondence_used_without_general_multiplicity_bridge",
            "synchronous_nontranslation_unstable_index_zero_validated",
            "synchronous_linear_orbital_attraction_validated",
            "hale_verduyn_lunel_hyperbolic_periodic_orbit_theorem_applied",
            "synchronous_nonlinear_orbital_attraction_validated",
            "fixed_rank_one_full_network_linear_orbital_attraction_validated",
            "fixed_rank_one_full_network_nonlinear_orbital_attraction_validated",
        ):
            _require_true(certificate, key)
        if any(Decimal(leaf.contraction_upper) >= 1 for leaf in leaves):
            raise ValueError("a non-strict leaf was promoted into the zero-free cover")
        for leaf in leaves:
            finite = Decimal(leaf.finite_input_column_sum_upper)
            tail = Decimal(leaf.tail_input_column_sum_upper)
            if Decimal(leaf.contraction_upper) != max(finite, tail):
                raise ValueError("a leaf contraction is not its two-column maximum")
        if (
            certificate.get("schur_boundary_winding_deduced_exactly_lower") != 0
            or certificate.get("schur_boundary_winding_deduced_exactly_upper") != 0
            or certificate.get("directed_nontranslation_right_half_strip_zero_count") != 0
        ):
            raise ValueError("the zero-free cover has a nonzero winding/count")
    scope = _mapping(root.get("scope"), "right-half cover scope")
    expected_scope = {
        "uniform_exact_parameter_box_right_half_zero_free_cover": zero_free,
        "schur_boundary_winding_zero_deduced_from_zero_free_cover": (
            certificate.get("schur_boundary_winding_deduced_exactly_lower") == 0
            and certificate.get("schur_boundary_winding_deduced_exactly_upper") == 0
        ),
        "synchronous_nontranslation_unstable_index_zero": bool(
            certificate.get(
                "synchronous_nontranslation_unstable_index_zero_validated"
            )
        ),
        "synchronous_linear_orbital_attraction": bool(
            certificate.get("synchronous_linear_orbital_attraction_validated")
        ),
        "synchronous_nonlinear_orbital_attraction": bool(
            certificate.get("synchronous_nonlinear_orbital_attraction_validated")
        ),
        "fixed_rank_one_full_network_linear_orbital_attraction": bool(
            certificate.get(
                "fixed_rank_one_full_network_linear_orbital_attraction_validated"
            )
        ),
        "fixed_rank_one_full_network_nonlinear_orbital_attraction": bool(
            certificate.get(
                "fixed_rank_one_full_network_nonlinear_orbital_attraction_validated"
            )
        ),
        "general_network_topology": False,
        "biological_pulse_capture": False,
    }
    if dict(scope) != expected_scope:
        raise ValueError("the serialized scope does not mirror the certificate")
    provenance = _mapping(root.get("provenance"), "right-half cover provenance")
    manifest = _mapping(
        provenance.get("proof_source_manifest"),
        "right-half cover source manifest",
    )
    repository = Path(__file__).resolve().parents[2]
    required_manifest_paths = (
        "src/canard_control/directed_interval.py",
        "src/canard_control/fhn_bloch_outer_validation.py",
        "src/canard_control/fhn_periodic_candidate.py",
        "src/canard_control/fhn_periodic_directed_validation.py",
        "src/canard_control/fhn_periodic_infinite_validation.py",
        "src/canard_control/fhn_periodic_parameter_box.py",
        "src/canard_control/fhn_synchronous_floquet_right_half_cover.py",
        "src/canard_control/fhn_synchronous_floquet_riesz_reduction.py",
        "src/canard_control/rfde_floquet_transfer.py",
    )
    if set(manifest) != set(required_manifest_paths):
        raise ValueError("the serialized proof-source manifest is incomplete")
    for relative in required_manifest_paths:
        actual = sha256((repository / relative).read_bytes()).hexdigest()
        if manifest.get(relative) != actual:
            raise ValueError(f"the serialized source hash is stale: {relative}")
    source_hash = sha256(Path(__file__).read_bytes()).hexdigest()
    if (
        provenance.get("source_module_sha256") != source_hash
        or manifest.get(
            "src/canard_control/fhn_synchronous_floquet_right_half_cover.py"
        )
        != source_hash
    ):
        raise ValueError("the serialized cover source hash changed")
    generator = repository / "experiments/fhn_synchronous_floquet_right_half_cover.py"
    if provenance.get("generator_sha256") != sha256(generator.read_bytes()).hexdigest():
        raise ValueError("the serialized cover generator hash changed")
    blas = _mapping(provenance.get("numpy_blas"), "recorded NumPy BLAS")
    if (
        blas.get("name") != "scipy-openblas"
        or not str(blas.get("version", "")).startswith("0.3.")
        or provenance.get("openblas_num_threads") != "8"
    ):
        raise ValueError("the tracked BLAS implementation/thread count changed")
    for key in (
        "exact_schur_to_candidate_finite_homotopy_validated",
        "general_network_topology_validated",
        "biological_pulse_capture_validated",
    ):
        _require_false(certificate, key)
