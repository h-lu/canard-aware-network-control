"""Directed Bloch cells for the periodic FHN parameter box.

The periodic branch certificate lives in a real-conjugate Fourier space,
because its orbit is real.  A nonzero Bloch phase does not preserve that
subspace.  This module therefore works on the full complex Fourier block

    (y_v, y_w) = (y_{v,k}, y_{w,k})_{|k| <= M}

and realifies it only when a binary64 inverse or product is audited.  The
underlying norm is the componentwise split Wiener norm

    sum_k (|Re y_{v,k}| + |Im y_{v,k}|
           + |Re y_{w,k}| + |Im y_{w,k}|).

The delayed coefficient is *not* shifted separately from the input.  We use

    H_v(S_alpha v) S_alpha y = S_alpha(H_v(v)y),

so the Bloch-delay rotation depends on the output mode.  This identity is
essential for a uniform moving-period bound on an unweighted Wiener space.

Only direct, unbordered Bloch operators are certified here.  Invertibility
of a phase-bordered operator would not imply injectivity of the unbordered
operator.
"""

from __future__ import annotations

import ctypes
from dataclasses import dataclass
from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR, localcontext
from functools import cache
from typing import Iterable, Mapping

import gmpy2
import numpy as np

from canard_control.directed_interval import (
    DirectedComplexInterval,
    DirectedInterval,
    complex_unit_interval,
    decimal_lower,
    decimal_upper,
    pi_interval,
    upward_division,
    upward_sum,
)
from canard_control.fhn_periodic_candidate import PeriodicOrbitCandidate
from canard_control.fhn_periodic_directed_validation import (
    ComplexSequence,
    _complex_zero,
    _constant_sequence,
    _one,
    _sequence_sub,
)
from canard_control.fhn_periodic_infinite_validation import (
    _BaseSequences,
    _box_abs_upper,
    _build_base_sequences,
    _float_matrix_l1_upper,
    _sequence_box_norm_upper,
)
from canard_control.fhn_periodic_parameter_box import (
    _Workspace,
    _build_parameter_box_sequences,
    _validate_continuation,
    _variation_bounds,
)
from canard_control.rfde_floquet_transfer import (
    _nonconstant_mode_lower,
    periodic_orbit_candidate_fingerprint,
)


_TRACKED_PARAMETER_BOX_SHA256 = (
    "ff13b5352c2b4e9898a4044be63fd490a3e7bb4217445a6a062188c2457c22a0"
)
_TRACKED_PARAMETER_BOX_CANDIDATE = (
    "2b56b5dff18c5aacd1450252824f5601ba3826f6de5d82eb2380853d3c518169"
)
_SPLIT_NORM_ID = "complex-component-wiener-l1-split-re-im"
_LOCAL_COMPLEXIFICATION_NORM_ID = (
    "complexification-of-real-conjugate-component-wiener-l1"
)


@dataclass(frozen=True)
class BlochParameterBoxEvidence:
    """Evidence hand-off from the tracked D1 parameter-box theorem."""

    parameter_box_result_sha256: str
    candidate_fingerprint: str
    gain_half_width: str
    correction_radius: str
    continuation_cutoff: int
    periodic_branch_validated: bool
    bordered_inverse_validated: bool
    moving_delay_period_column_validated: bool


@dataclass(frozen=True)
class DirectedParameterBoxLocalFloquet:
    """Uniform unit-root simplicity and punctured local-arc exclusion."""

    precision_bits: int
    norm_id: str
    parameter_box_result_sha256: str
    candidate_fingerprint: str
    correction_radius: str
    bordered_inverse_norm_upper: str
    minimum_period_lower: str
    maximum_period_upper: str
    maximum_delay_upper: str
    nonconstant_fourier_mode_lower: str
    delayed_coefficient_center_norm_upper: str
    delayed_coefficient_variation_upper: str
    delayed_coefficient_uniform_norm_upper: str
    orbit_tangent_norm_upper: str
    bloch_first_order_coefficient_upper: str
    bloch_second_order_coefficient_upper: str
    local_phase_radius_lower: str
    monodromy_compact: bool
    regularity_bridge_to_history_monodromy: bool
    period_column_jordan_identity: str
    unit_multiplier_algebraically_simple_validated: bool
    local_unit_circle_exclusion_validated: bool


@dataclass(frozen=True)
class DirectedBlochCellCertificate:
    """One direct full-complex finite/tail Bloch contraction."""

    precision_bits: int
    norm_id: str
    parameter_box_result_sha256: str
    candidate_fingerprint: str
    cutoff: int
    complex_finite_dimension: int
    realified_finite_dimension: int
    coefficient_support_half_bandwidth: int
    phase_lower: str
    phase_center: str
    phase_upper: str
    phase_half_width: str
    tail_diagonal_gap_lower: str
    finite_inverse_l1_upper: str
    finite_inverse_defect_upper: str
    finite_phase_first_product_upper: str
    finite_phase_second_remainder_coefficient_upper: str
    finite_from_tail_center_upper: str
    finite_from_tail_phase_first_upper: str
    finite_from_tail_phase_second_coefficient_upper: str
    tail_from_finite_center_upper: str
    tail_from_finite_phase_first_upper: str
    tail_from_finite_phase_second_coefficient_upper: str
    current_coefficient_center_norm_upper: str
    current_coefficient_variation_upper: str
    delayed_coefficient_center_norm_upper: str
    delayed_coefficient_variation_upper: str
    finite_convolution_correction_upper: str
    finite_full_correction_upper: str
    tail_from_finite_correction_upper: str
    finite_to_finite_upper: str
    tail_from_finite_upper: str
    finite_from_tail_upper: str
    tail_to_tail_upper: str
    finite_input_column_sum_upper: str
    tail_input_column_sum_upper: str
    contraction_upper: str
    contraction_margin_lower: str
    direct_unbordered_operator: bool
    arbitrary_complex_modes: bool
    moving_delay_output_rotation_validated: bool
    exact_parameter_box_orbit_ball_included: bool
    cell_validated: bool
    failure_reason: str | None


@dataclass(frozen=True)
class DirectedBlochArcCertificate:
    """Connected positive-arc cover and the resulting unit-circle theorem."""

    precision_bits: int
    norm_id: str
    local_norm_id: str
    cutoff: int
    parameter_box_result_sha256: str
    candidate_fingerprint: str
    local_phase_radius_lower: str
    positive_arc_required_lower: str
    positive_arc_required_upper: str
    relative_half_width_seed: str
    cell_count: int
    maximum_contraction_upper: str | None
    minimum_contraction_margin_lower: str | None
    connected_positive_arc_cover: bool
    every_cell_validated: bool
    negative_arc_mode_reversal_conjugacy_validated: bool
    all_nontrivial_unit_multipliers_excluded: bool
    synchronous_orbital_hyperbolicity_validated: bool
    attraction_validated: bool
    full_network_transverse_stability_validated: bool
    cells: tuple[DirectedBlochCellCertificate, ...]
    failure_reason: str | None


@dataclass(frozen=True)
class _BoxEntry:
    row: int
    column: int
    value: DirectedComplexInterval


@dataclass(frozen=True)
class _ComplexBoxMatrix:
    midpoint: np.ndarray
    entries: tuple[_BoxEntry, ...]

    @property
    def shape(self) -> tuple[int, int]:
        return self.midpoint.shape


@dataclass(frozen=True)
class _CoefficientBudget:
    current_center: gmpy2.mpfr
    current_variation: gmpy2.mpfr
    current_uniform: gmpy2.mpfr
    delayed_center: gmpy2.mpfr
    delayed_variation: gmpy2.mpfr
    delayed_uniform: gmpy2.mpfr
    period_lower: gmpy2.mpfr
    period_center: DirectedInterval
    period_upper: gmpy2.mpfr
    finite_convolution_correction: gmpy2.mpfr
    finite_full_correction: gmpy2.mpfr
    tail_from_finite_correction: gmpy2.mpfr


@dataclass(frozen=True)
class _PreparedBlochValidation:
    orbit: PeriodicOrbitCandidate
    evidence: BlochParameterBoxEvidence
    workspace: _Workspace
    center_base: _BaseSequences
    box_base: _BaseSequences


def _zero(precision: int) -> DirectedInterval:
    return DirectedInterval.from_decimal(0, precision)


def _imaginary(value: DirectedInterval) -> DirectedComplexInterval:
    return DirectedComplexInterval(_zero(value.precision), value)


def _complex_point(value: complex, precision: int) -> DirectedComplexInterval:
    return DirectedComplexInterval(
        DirectedInterval.from_float(float(value.real), precision),
        DirectedInterval.from_float(float(value.imag), precision),
    )


def _split_abs_upper(value: DirectedComplexInterval) -> gmpy2.mpfr:
    """Complex scalar cost in the declared split norm."""

    return _box_abs_upper(value)


def _mpfr_up(value: object, precision: int) -> gmpy2.mpfr:
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        return gmpy2.mpfr(value)


def _mpfr_down(value: object, precision: int) -> gmpy2.mpfr:
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        return gmpy2.mpfr(value)


def _exact_decimal_sum(values: Iterable[str]) -> str:
    """Add directed decimal uppers exactly for external JSON replay."""

    items = tuple(values)
    with localcontext() as context:
        context.prec = max(120, sum(len(item) for item in items) + 10)
        total = sum((Decimal(item) for item in items), Decimal(0))
    return format(total, "f")


def _exact_decimal_margin(contraction_upper: str) -> str:
    """Subtract a decimal upper bound from one without another rounding."""

    with localcontext() as context:
        context.prec = max(120, len(contraction_upper) + 10)
        margin = Decimal(1) - Decimal(contraction_upper)
    return format(margin, "f")


def _upper_add(values: Iterable[gmpy2.mpfr], precision: int) -> gmpy2.mpfr:
    return upward_sum(tuple(values), precision)


def _midpoint_complex(value: DirectedComplexInterval) -> complex:
    return complex(
        float(value.real.midpoint_nearest()),
        float(value.imag.midpoint_nearest()),
    )


def _realify(matrix: np.ndarray) -> np.ndarray:
    """Realify a possibly rectangular complex matrix in split coordinates."""

    values = np.asarray(matrix, dtype=complex)
    return np.block(
        [[values.real, -values.imag], [values.imag, values.real]]
    ).astype(float, copy=False)


def _binary_environment_checked() -> None:
    info = np.finfo(float)
    if not (
        info.bits == 64
        and info.nmant == 52
        and info.eps == 2.0**-52
        and np.nextafter(0.0, 1.0)
        == float.fromhex("0x0.0000000000001p-1022")
    ):
        raise RuntimeError("the Bloch accelerator requires IEEE binary64")
    process = ctypes.CDLL(None)
    if not hasattr(process, "fegetround"):
        raise RuntimeError("cannot audit the host floating rounding mode")
    process.fegetround.restype = ctypes.c_int
    if process.fegetround() != 0:
        raise RuntimeError("binary Bloch products require round-to-nearest")


def _binary_matrix_product_l1_upper(
    left: np.ndarray,
    right: np.ndarray,
    precision: int,
) -> gmpy2.mpfr:
    """Bound the l1 norm of the exact product of two binary64 matrices."""

    a = np.asarray(left, dtype=float)
    b = np.asarray(right, dtype=float)
    if a.ndim != 2 or b.ndim != 2 or a.shape[1] != b.shape[0]:
        raise ValueError("binary product matrices have incompatible shapes")
    if not np.all(np.isfinite(a)) or not np.all(np.isfinite(b)):
        raise ValueError("binary product matrices must be finite")
    _binary_environment_checked()
    product = a @ b
    _binary_environment_checked()
    if not np.all(np.isfinite(product)):
        raise RuntimeError("binary Bloch matrix product overflowed")
    stored = _float_matrix_l1_upper(product, precision)
    a_norm = _float_matrix_l1_upper(a, precision)
    b_norm = _float_matrix_l1_upper(b, precision)
    inner = a.shape[1]
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        unit_roundoff = gmpy2.mpfr(2) ** -53
        gamma = inner * unit_roundoff / (1 - inner * unit_roundoff)
        smallest_normal = gmpy2.mpfr(2) ** -1022
        roundoff = (
            gamma * a_norm * b_norm
            + a.shape[0] * inner * smallest_normal
        )
        return stored + roundoff


def _complex_column_weights(
    matrix: np.ndarray, precision: int
) -> tuple[gmpy2.mpfr, ...]:
    """Column costs of a complex matrix in the split norm."""

    values = np.asarray(matrix, dtype=complex)
    weights: list[gmpy2.mpfr] = []
    for column in values.T:
        terms: list[gmpy2.mpfr] = []
        for entry in column:
            real = DirectedInterval.from_float(abs(float(entry.real)), precision)
            imag = DirectedInterval.from_float(abs(float(entry.imag)), precision)
            terms.extend((real.upper, imag.upper))
        weights.append(upward_sum(terms, precision))
    return tuple(weights)


def _complex_matrix_split_l1_upper(
    matrix: np.ndarray, precision: int
) -> gmpy2.mpfr:
    return max(_complex_column_weights(matrix, precision))


def _box_distance_split_upper(
    value: DirectedComplexInterval,
    center: complex,
) -> gmpy2.mpfr:
    precision = value.precision
    real_center = DirectedInterval.from_float(float(center.real), precision)
    imag_center = DirectedInterval.from_float(float(center.imag), precision)
    return upward_sum(
        (
            (value.real - real_center).upper_abs(),
            (value.imag - imag_center).upper_abs(),
        ),
        precision,
    )


def _left_product_interval_remainder(
    left: np.ndarray,
    boxed_right: _ComplexBoxMatrix,
    precision: int,
    weights: tuple[gmpy2.mpfr, ...] | None = None,
) -> gmpy2.mpfr:
    """Bound ``left * (boxed_right-midpoint)`` without ``||left||||E||``."""

    if left.shape[1] != boxed_right.shape[0]:
        raise ValueError("boxed product has incompatible shapes")
    column_weights = weights or _complex_column_weights(left, precision)
    if len(column_weights) != left.shape[1]:
        raise ValueError("the supplied complex column weights have wrong length")
    columns: list[list[gmpy2.mpfr]] = [
        [] for _ in range(boxed_right.shape[1])
    ]
    for entry in boxed_right.entries:
        radius = _box_distance_split_upper(
            entry.value,
            complex(boxed_right.midpoint[entry.row, entry.column]),
        )
        with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
            columns[entry.column].append(column_weights[entry.row] * radius)
    zero = _mpfr_up(0, precision)
    return max(
        (upward_sum(items, precision) if items else zero)
        for items in columns
    )


def _boxed_left_product_l1_upper(
    left: np.ndarray,
    boxed_right: _ComplexBoxMatrix,
    precision: int,
    weights: tuple[gmpy2.mpfr, ...] | None = None,
) -> gmpy2.mpfr:
    midpoint = _binary_matrix_product_l1_upper(
        _realify(left), _realify(boxed_right.midpoint), precision
    )
    remainder = _left_product_interval_remainder(
        left, boxed_right, precision, weights
    )
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        return midpoint + remainder


def _binary_inverse_defect_l1_upper(
    inverse: np.ndarray,
    boxed_operator: _ComplexBoxMatrix,
    precision: int,
    weights: tuple[gmpy2.mpfr, ...] | None = None,
) -> gmpy2.mpfr:
    """Bound ``I-inverse*operator`` including interval coefficient boxes."""

    a = _realify(inverse)
    j = _realify(boxed_operator.midpoint)
    # Local import avoids exposing a real-conjugate layout in this module.
    from canard_control.fhn_periodic_directed_validation import (
        _binary_product_defect_upper,
    )

    binary, _, _, checked = _binary_product_defect_upper(
        j.T, a.T, precision
    )
    if not checked:
        raise RuntimeError("binary inverse defect was not audited")
    remainder = _left_product_interval_remainder(
        inverse, boxed_operator, precision, weights
    )
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        return binary + remainder


def _matrix_from_entries(
    row_count: int,
    column_count: int,
    entries: Iterable[tuple[int, int, DirectedComplexInterval]],
) -> _ComplexBoxMatrix:
    midpoint = np.zeros((row_count, column_count), dtype=complex)
    stored: list[_BoxEntry] = []
    seen: set[tuple[int, int]] = set()
    for row, column, value in entries:
        key = (row, column)
        if key in seen:
            raise RuntimeError("a boxed Bloch entry was supplied twice")
        seen.add(key)
        midpoint[row, column] = _midpoint_complex(value)
        stored.append(_BoxEntry(row, column, value))
    return _ComplexBoxMatrix(midpoint, tuple(stored))


def _mode_index(component: int, mode: int, cutoff: int) -> int:
    if component not in (0, 1) or not -cutoff <= mode <= cutoff:
        raise ValueError("Bloch coordinate lies outside the finite block")
    span = 2 * cutoff + 1
    return component * span + mode + cutoff


def _coefficient_support(
    current: Mapping[int, DirectedComplexInterval],
    delayed: Mapping[int, DirectedComplexInterval],
) -> tuple[int, set[int]]:
    support = set(current) | set(delayed)
    if not support:
        raise ValueError("the Bloch coefficient support is empty")
    return max(abs(mode) for mode in support), support


@cache
def _bloch_rotation(
    output_mode: int,
    phase: DirectedInterval,
    tau: DirectedInterval,
    period: DirectedInterval,
) -> DirectedComplexInterval:
    precision = phase.precision
    omega = pi_interval(precision) * (2 * output_mode) + phase
    return complex_unit_interval(-(omega * tau / period))


def _center_voltage_entry(
    base: _BaseSequences,
    *,
    output_mode: int,
    input_mode: int,
    phase: DirectedInterval,
) -> DirectedComplexInterval:
    """Exact directed center Bloch entry from voltage to fast output."""

    precision = phase.precision
    zero = _complex_zero(precision)
    difference = output_mode - input_mode
    current = base.current_coefficient.get(difference, zero)
    delayed = base.delayed_state_derivative.get(difference, zero)
    entry = -(current * base.period)
    for tau in (base.parameters["tau_0"], base.parameters["tau_1"]):
        rotation = _bloch_rotation(
            output_mode, phase, tau, base.period
        )
        entry = entry - rotation * delayed * base.period
    if output_mode == input_mode:
        omega = pi_interval(precision) * (2 * output_mode) + phase
        entry = entry + _imaginary(omega)
    return entry


def _center_voltage_phase_derivative_entry(
    base: _BaseSequences,
    *,
    output_mode: int,
    input_mode: int,
    phase: DirectedInterval,
) -> DirectedComplexInterval:
    """Directed entry of ``d L_phi / d phi`` at the center orbit."""

    precision = phase.precision
    zero = _complex_zero(precision)
    difference = output_mode - input_mode
    delayed = base.delayed_state_derivative.get(difference, zero)
    entry = zero
    for tau in (base.parameters["tau_0"], base.parameters["tau_1"]):
        rotation = _bloch_rotation(
            output_mode, phase, tau, base.period
        )
        entry = entry + _imaginary(tau) * rotation * delayed
    if output_mode == input_mode:
        entry = entry + _imaginary(DirectedInterval.from_decimal(1, precision))
    return entry


def _finite_center_matrix(
    base: _BaseSequences,
    cutoff: int,
    phase: DirectedInterval,
) -> _ComplexBoxMatrix:
    precision = phase.precision
    span = 2 * cutoff + 1
    dimension = 2 * span
    support_radius, support = _coefficient_support(
        base.current_coefficient, base.delayed_state_derivative
    )
    del support_radius
    entries: list[tuple[int, int, DirectedComplexInterval]] = []
    for output_mode in range(-cutoff, cutoff + 1):
        row = _mode_index(0, output_mode, cutoff)
        first = max(-cutoff, output_mode - max(abs(k) for k in support))
        last = min(cutoff, output_mode + max(abs(k) for k in support))
        for input_mode in range(first, last + 1):
            if output_mode - input_mode not in support and output_mode != input_mode:
                continue
            value = _center_voltage_entry(
                base,
                output_mode=output_mode,
                input_mode=input_mode,
                phase=phase,
            )
            entries.append(
                (row, _mode_index(0, input_mode, cutoff), value)
            )

        recovery_column = _mode_index(1, output_mode, cutoff)
        entries.append(
            (
                row,
                recovery_column,
                DirectedComplexInterval.from_real(base.period),
            )
        )
        slow_row = _mode_index(1, output_mode, cutoff)
        entries.append(
            (
                slow_row,
                _mode_index(0, output_mode, cutoff),
                DirectedComplexInterval.from_real(
                    -(base.period * base.parameters["epsilon"])
                ),
            )
        )
        omega = pi_interval(precision) * (2 * output_mode) + phase
        entries.append((slow_row, recovery_column, _imaginary(omega)))
    return _matrix_from_entries(dimension, dimension, entries)


def _finite_phase_derivative_matrix(
    base: _BaseSequences,
    cutoff: int,
    phase: DirectedInterval,
) -> _ComplexBoxMatrix:
    precision = phase.precision
    span = 2 * cutoff + 1
    dimension = 2 * span
    _, support = _coefficient_support(
        base.current_coefficient, base.delayed_state_derivative
    )
    radius = max(abs(k) for k in support)
    entries: list[tuple[int, int, DirectedComplexInterval]] = []
    for output_mode in range(-cutoff, cutoff + 1):
        row = _mode_index(0, output_mode, cutoff)
        first = max(-cutoff, output_mode - radius)
        last = min(cutoff, output_mode + radius)
        for input_mode in range(first, last + 1):
            difference = output_mode - input_mode
            if (
                difference not in base.delayed_state_derivative
                and output_mode != input_mode
            ):
                continue
            value = _center_voltage_phase_derivative_entry(
                base,
                output_mode=output_mode,
                input_mode=input_mode,
                phase=phase,
            )
            entries.append(
                (row, _mode_index(0, input_mode, cutoff), value)
            )
        slow = _mode_index(1, output_mode, cutoff)
        entries.append(
            (
                slow,
                slow,
                _imaginary(DirectedInterval.from_decimal(1, precision)),
            )
        )
    return _matrix_from_entries(dimension, dimension, entries)


def _finite_from_tail_matrix(
    base: _BaseSequences,
    cutoff: int,
    phase: DirectedInterval,
    *,
    derivative: bool,
) -> tuple[_ComplexBoxMatrix, tuple[int, ...]]:
    support_radius, support = _coefficient_support(
        base.current_coefficient, base.delayed_state_derivative
    )
    tail_modes = tuple(
        list(range(-cutoff - support_radius, -cutoff))
        + list(range(cutoff + 1, cutoff + support_radius + 1))
    )
    span = 2 * cutoff + 1
    dimension = 2 * span
    entries: list[tuple[int, int, DirectedComplexInterval]] = []
    for column, input_mode in enumerate(tail_modes):
        for output_mode in range(-cutoff, cutoff + 1):
            if output_mode - input_mode not in support:
                continue
            if derivative:
                value = _center_voltage_phase_derivative_entry(
                    base,
                    output_mode=output_mode,
                    input_mode=input_mode,
                    phase=phase,
                )
            else:
                value = _center_voltage_entry(
                    base,
                    output_mode=output_mode,
                    input_mode=input_mode,
                    phase=phase,
                )
            entries.append(
                (_mode_index(0, output_mode, cutoff), column, value)
            )
    return _matrix_from_entries(dimension, len(tail_modes), entries), tail_modes


def _tail_from_finite_upper(
    base: _BaseSequences,
    cutoff: int,
    phase: DirectedInterval,
    *,
    derivative: bool,
) -> gmpy2.mpfr:
    precision = phase.precision
    support_radius, support = _coefficient_support(
        base.current_coefficient, base.delayed_state_derivative
    )
    bounds: list[gmpy2.mpfr] = [_mpfr_up(0, precision)]
    for input_mode in range(-cutoff, cutoff + 1):
        terms: list[gmpy2.mpfr] = []
        first = input_mode - support_radius
        last = input_mode + support_radius
        for output_mode in range(first, last + 1):
            if abs(output_mode) <= cutoff:
                continue
            if output_mode - input_mode not in support:
                continue
            if derivative:
                value = _center_voltage_phase_derivative_entry(
                    base,
                    output_mode=output_mode,
                    input_mode=input_mode,
                    phase=phase,
                )
            else:
                value = _center_voltage_entry(
                    base,
                    output_mode=output_mode,
                    input_mode=input_mode,
                    phase=phase,
                )
            omega = pi_interval(precision) * (2 * output_mode) + phase
            terms.append(
                upward_division(
                    _split_abs_upper(value), omega.lower_abs(), precision
                )
            )
        bounds.append(upward_sum(terms, precision))
    return max(bounds)


def _coefficient_budget(
    center: _BaseSequences,
    box: _BaseSequences,
    correction_radius: DirectedInterval,
    cutoff: int,
    phase_upper: DirectedInterval,
) -> _CoefficientBudget:
    precision = center.period.precision
    r = correction_radius.upper
    current_center = _sequence_box_norm_upper(
        center.current_coefficient, precision
    )
    delayed_center = _sequence_box_norm_upper(
        center.delayed_state_derivative, precision
    )
    voltage = _sequence_box_norm_upper(center.voltage, precision)
    centered = _sequence_box_norm_upper(center.centered_voltage, precision)
    epsilon = center.parameters["epsilon"].upper
    kappa_3_max = box.parameters["kappa_3"].upper
    h1 = (
        box.parameters["kappa_1"] - center.parameters["kappa_1"]
    ).upper_abs()
    h3 = (
        box.parameters["kappa_3"] - center.parameters["kappa_3"]
    ).upper_abs()
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        common = (
            kappa_3_max * (2 * centered + r) * r
            + h3 * centered * centered
        )
        current_variation = (
            (2 * voltage + r) * r
            + epsilon * h1
            + 3 * epsilon * common
        )
        delayed_variation = epsilon * (h1 + 3 * common) / 2
        current_uniform = current_center + current_variation
        delayed_uniform = delayed_center + delayed_variation
    period_lower = (center.period - correction_radius).lower
    period_upper = (center.period + correction_radius).upper
    if period_lower <= 0:
        raise ValueError("the orbit ball crosses nonpositive periods")
    sqrt_two = DirectedInterval.from_decimal(2, precision).sqrt().upper
    finite_frequency = (
        pi_interval(precision) * (2 * cutoff) + phase_upper
    ).upper
    delayed_finite_terms: list[gmpy2.mpfr] = []
    for tau in (center.parameters["tau_0"], center.parameters["tau_1"]):
        with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
            term = sqrt_two * (
                r * delayed_uniform
                + center.period.upper * delayed_variation
                + delayed_center * tau.upper * finite_frequency * r / period_lower
            )
        delayed_finite_terms.append(term)
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        current_term = r * current_uniform + center.period.upper * current_variation
        finite_convolution = current_term + sum(
            delayed_finite_terms, gmpy2.mpfr(0, precision)
        )
        finite_full = max(
            finite_convolution + epsilon * r,
            r,
        )
    return _CoefficientBudget(
        current_center=current_center,
        current_variation=current_variation,
        current_uniform=current_uniform,
        delayed_center=delayed_center,
        delayed_variation=delayed_variation,
        delayed_uniform=delayed_uniform,
        period_lower=period_lower,
        period_center=center.period,
        period_upper=period_upper,
        finite_convolution_correction=finite_convolution,
        finite_full_correction=finite_full,
        tail_from_finite_correction=_mpfr_up(0, precision),
    )


def _complete_tail_correction(
    budget: _CoefficientBudget,
    center: _BaseSequences,
    correction_radius: DirectedInterval,
    tail_gap: gmpy2.mpfr,
    phase_half_width: gmpy2.mpfr,
) -> _CoefficientBudget:
    precision = center.period.precision
    r = correction_radius.upper
    sqrt_two = DirectedInterval.from_decimal(2, precision).sqrt().upper
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        ratio = 1 + phase_half_width / tail_gap
        current_term = (
            r * budget.current_uniform
            + center.period.upper * budget.current_variation
        ) / tail_gap
        delayed_terms = []
        for tau in (
            center.parameters["tau_0"],
            center.parameters["tau_1"],
        ):
            delayed_terms.append(
                sqrt_two
                * (
                    (
                        r * budget.delayed_uniform
                        + center.period.upper * budget.delayed_variation
                    )
                    / tail_gap
                    + budget.delayed_center
                    * tau.upper
                    * r
                    / budget.period_lower
                    * ratio
                )
            )
        correction = current_term + sum(
            delayed_terms, gmpy2.mpfr(0, precision)
        )
    return _CoefficientBudget(
        current_center=budget.current_center,
        current_variation=budget.current_variation,
        current_uniform=budget.current_uniform,
        delayed_center=budget.delayed_center,
        delayed_variation=budget.delayed_variation,
        delayed_uniform=budget.delayed_uniform,
        period_lower=budget.period_lower,
        period_center=budget.period_center,
        period_upper=budget.period_upper,
        finite_convolution_correction=budget.finite_convolution_correction,
        finite_full_correction=budget.finite_full_correction,
        tail_from_finite_correction=correction,
    )


def _validate_scope_evidence(
    orbit: PeriodicOrbitCandidate,
    evidence: BlochParameterBoxEvidence,
) -> None:
    if evidence.parameter_box_result_sha256 != _TRACKED_PARAMETER_BOX_SHA256:
        raise ValueError("the Bloch scope is not bound to the tracked box result")
    if evidence.candidate_fingerprint != periodic_orbit_candidate_fingerprint(
        orbit
    ):
        raise ValueError("the Bloch scope belongs to a different candidate")
    if evidence.candidate_fingerprint != _TRACKED_PARAMETER_BOX_CANDIDATE:
        raise ValueError("the Bloch scope is not the tracked 129-node candidate")
    if evidence.gain_half_width != "1e-12":
        raise ValueError("the tracked Bloch gain half-width is 1e-12")
    if evidence.correction_radius != "5e-9":
        raise ValueError("the tracked Bloch correction radius is 5e-9")
    if evidence.continuation_cutoff != 144:
        raise ValueError("the tracked branch continuation cutoff is 144")
    if not evidence.periodic_branch_validated:
        raise ValueError("a validated periodic parameter-box branch is required")
    if not evidence.bordered_inverse_validated:
        raise ValueError("a uniform phase-bordered inverse is required")
    if not evidence.moving_delay_period_column_validated:
        raise ValueError("the exact moving-delay period column is required")


def _tracked_workspace(
    orbit: PeriodicOrbitCandidate,
    evidence: BlochParameterBoxEvidence,
    precision: int,
) -> _Workspace:
    _validate_scope_evidence(orbit, evidence)
    workspace = _validate_continuation(
        orbit,
        half_width=evidence.gain_half_width,
        cutoff=evidence.continuation_cutoff,
        precision=precision,
        maximum_radius=evidence.correction_radius,
        chosen_radius=evidence.correction_radius,
    )
    if not workspace.continuation.parameter_box_orbit_validated:
        raise ArithmeticError("the recomputed parameter-box branch did not validate")
    if not workspace.continuation.parameter_box_bordered_inverse_validated:
        raise ArithmeticError("the recomputed bordered inverse did not validate")
    if workspace.inverse_norm is None:
        raise ArithmeticError("the branch certificate supplied no inverse norm")
    return workspace


def _prepare_bloch_validation(
    orbit: PeriodicOrbitCandidate,
    evidence: BlochParameterBoxEvidence,
    precision: int,
) -> _PreparedBlochValidation:
    workspace = _tracked_workspace(orbit, evidence, precision)
    return _PreparedBlochValidation(
        orbit=orbit,
        evidence=evidence,
        workspace=workspace,
        center_base=_build_base_sequences(orbit, precision),
        box_base=_build_parameter_box_sequences(
            orbit, precision, evidence.gain_half_width
        ),
    )


def _local_floquet_from_prepared(
    prepared: _PreparedBlochValidation,
) -> DirectedParameterBoxLocalFloquet:
    orbit = prepared.orbit
    evidence = prepared.evidence
    workspace = prepared.workspace
    center = prepared.center_base
    box = workspace.base
    precision = center.period.precision
    variation = _variation_bounds(workspace)
    radius = workspace.chosen_radius
    inverse = workspace.inverse_norm
    assert inverse is not None
    minimum_period = (center.period - radius).lower
    maximum_period = (center.period + radius).upper
    maximum_delay = max(
        center.parameters["tau_0"].upper,
        center.parameters["tau_1"].upper,
    )
    monodromy_compact = minimum_period > maximum_delay
    nonconstant = _nonconstant_mode_lower(center, radius.upper)
    if not monodromy_compact:
        raise ValueError("the parameter box does not have one-period smoothing")
    if nonconstant <= 0:
        raise ValueError("the parameter box does not prove a nonconstant orbit")

    coefficient = _coefficient_budget(
        center,
        box,
        radius,
        cutoff=0,
        phase_upper=DirectedInterval.from_decimal(0, precision),
    )
    voltage_tangent = _sequence_box_norm_upper(
        center.phase_voltage, precision
    )
    voltage_minus_unfolding = _sequence_box_norm_upper(
        _sequence_sub(
            center.voltage,
            _constant_sequence(center.parameters["unfolding"], precision),
        ),
        precision,
    )
    epsilon = center.parameters["epsilon"].upper
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        tangent_voltage = voltage_tangent + variation.derivative_error
        tangent_recovery = (
            maximum_period
            * epsilon
            * (voltage_minus_unfolding + radius.upper)
        )
        tangent = tangent_voltage + tangent_recovery
        delay_sum = (
            center.parameters["tau_0"].upper
            + center.parameters["tau_1"].upper
        )
        first = 1 + 2 * delay_sum * coefficient.delayed_uniform
        alpha_square_sum = (
            (center.parameters["tau_0"].upper / minimum_period) ** 2
            + (center.parameters["tau_1"].upper / minimum_period) ** 2
        )
        second = (
            maximum_period
            * coefficient.delayed_uniform
            * alpha_square_sum
            * tangent
        )
        first_denominator = inverse * first
        second_denominator = inverse * second
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        first_radius_lower = gmpy2.mpfr(1) / first_denominator
        second_radius_lower = minimum_period / second_denominator
        local_radius = min(
            first_radius_lower,
            second_radius_lower,
            pi_interval(precision).lower,
        ) / 2
    if local_radius <= 0:
        raise ArithmeticError("the uniform local Floquet radius vanished")
    return DirectedParameterBoxLocalFloquet(
        precision_bits=precision,
        # The bordered inverse comes from the real RFDE space and is used on
        # its abstract complexification.  This is deliberately not labeled
        # as the arbitrary-coefficient split norm used by the outer cells.
        norm_id=_LOCAL_COMPLEXIFICATION_NORM_ID,
        parameter_box_result_sha256=evidence.parameter_box_result_sha256,
        candidate_fingerprint=evidence.candidate_fingerprint,
        correction_radius=evidence.correction_radius,
        bordered_inverse_norm_upper=decimal_upper(inverse),
        minimum_period_lower=decimal_lower(minimum_period),
        maximum_period_upper=decimal_upper(maximum_period),
        maximum_delay_upper=decimal_upper(maximum_delay),
        nonconstant_fourier_mode_lower=decimal_lower(nonconstant),
        delayed_coefficient_center_norm_upper=decimal_upper(
            coefficient.delayed_center
        ),
        delayed_coefficient_variation_upper=decimal_upper(
            coefficient.delayed_variation
        ),
        delayed_coefficient_uniform_norm_upper=decimal_upper(
            coefficient.delayed_uniform
        ),
        orbit_tangent_norm_upper=decimal_upper(tangent),
        bloch_first_order_coefficient_upper=decimal_upper(first),
        bloch_second_order_coefficient_upper=decimal_upper(second),
        local_phase_radius_lower=decimal_lower(local_radius),
        monodromy_compact=monodromy_compact,
        regularity_bridge_to_history_monodromy=True,
        period_column_jordan_identity=(
            "L(theta*X') = T*b, with b = f + "
            "sum_j (tau_j/T) A_j S_j X'"
        ),
        unit_multiplier_algebraically_simple_validated=True,
        local_unit_circle_exclusion_validated=True,
    )


def validate_parameter_box_local_floquet(
    orbit: PeriodicOrbitCandidate,
    evidence: BlochParameterBoxEvidence,
    *,
    precision: int = 160,
) -> DirectedParameterBoxLocalFloquet:
    """Prove unit-root simplicity and a uniform punctured local Bloch arc."""

    return _local_floquet_from_prepared(
        _prepare_bloch_validation(orbit, evidence, precision)
    )


def validate_directed_bloch_cell(
    orbit: PeriodicOrbitCandidate,
    evidence: BlochParameterBoxEvidence,
    *,
    phase_lower: str,
    phase_center: str,
    phase_upper: str,
    phase_half_width: str,
    cutoff: int = 96,
    precision: int = 160,
    _prepared: _PreparedBlochValidation | None = None,
) -> DirectedBlochCellCertificate:
    """Validate one positive-phase cell for the exact parameter-box branch."""

    if cutoff < (len(orbit.state) - 1) // 2:
        raise ValueError("the Bloch cutoff must contain the orbit support")
    lower_q = gmpy2.mpq(phase_lower)
    center_q = gmpy2.mpq(phase_center)
    upper_q = gmpy2.mpq(phase_upper)
    half_q = gmpy2.mpq(phase_half_width)
    if lower_q <= 0 or half_q <= 0:
        raise ValueError("a directed Bloch cell must lie at positive phase")
    if center_q - half_q != lower_q or center_q + half_q != upper_q:
        raise ValueError("phase center and half-width do not match the endpoints")
    if (
        DirectedInterval.from_decimal(phase_upper, precision).upper
        >= (pi_interval(precision) * 2).lower
    ):
        raise ValueError("a positive Bloch cell must stay below 2*pi")

    prepared = _prepared or _prepare_bloch_validation(
        orbit, evidence, precision
    )
    if prepared.orbit is not orbit or prepared.evidence != evidence:
        raise ValueError("the prepared Bloch workspace has different evidence")
    workspace = prepared.workspace
    center_base = prepared.center_base
    box_base = prepared.box_base
    phase = DirectedInterval.from_decimal(phase_center, precision)
    phase_plus = DirectedInterval.from_decimal(phase_upper, precision)
    half = DirectedInterval.from_decimal(phase_half_width, precision).upper
    _bloch_rotation.cache_clear()
    radius = workspace.chosen_radius
    support_radius, _ = _coefficient_support(
        center_base.current_coefficient,
        center_base.delayed_state_derivative,
    )
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        tail_gap = (
            pi_interval(precision).lower * (2 * (cutoff + 1))
            - phase.upper
        )
    if tail_gap <= 0:
        raise ArithmeticError("the fixed-center tail diagonal gap vanished")

    finite = _finite_center_matrix(center_base, cutoff, phase)
    inverse = np.linalg.inv(finite.midpoint)
    inverse_weights = _complex_column_weights(inverse, precision)
    inverse_norm = max(inverse_weights)
    eta = _binary_inverse_defect_l1_upper(
        inverse, finite, precision, inverse_weights
    )
    derivative = _finite_phase_derivative_matrix(
        center_base, cutoff, phase
    )
    mu = _boxed_left_product_l1_upper(
        inverse, derivative, precision, inverse_weights
    )

    coefficient = _coefficient_budget(
        center_base,
        box_base,
        radius,
        cutoff,
        phase_plus,
    )
    coefficient = _complete_tail_correction(
        coefficient,
        center_base,
        radius,
        tail_gap,
        half,
    )
    sqrt_two = DirectedInterval.from_decimal(2, precision).sqrt().upper
    alpha_square_sum = _upper_add(
        (
            (
                center_base.parameters["tau_0"].upper
                / center_base.period.lower
            )
            ** 2,
            (
                center_base.parameters["tau_1"].upper
                / center_base.period.lower
            )
            ** 2,
        ),
        precision,
    )
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        second_raw = (
            center_base.period.upper
            * sqrt_two
            * coefficient.delayed_center
            * alpha_square_sum
            / 2
        )
        nu = inverse_norm * second_raw

    finite_tail, tail_modes = _finite_from_tail_matrix(
        center_base, cutoff, phase, derivative=False
    )
    finite_tail_derivative, derivative_tail_modes = _finite_from_tail_matrix(
        center_base, cutoff, phase, derivative=True
    )
    if tail_modes != derivative_tail_modes:
        raise RuntimeError("the finite-from-tail mode lists disagree")
    p0 = _boxed_left_product_l1_upper(
        inverse, finite_tail, precision, inverse_weights
    )
    p1 = _boxed_left_product_l1_upper(
        inverse, finite_tail_derivative, precision, inverse_weights
    )
    p2 = nu
    q0 = _tail_from_finite_upper(
        center_base, cutoff, phase, derivative=False
    )
    q1 = _tail_from_finite_upper(
        center_base, cutoff, phase, derivative=True
    )
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        q2 = second_raw / tail_gap
        z_pp = (
            eta
            + half * mu
            + half * half * nu
            + inverse_norm * coefficient.finite_full_correction
        )
        z_pq = (
            p0
            + half * p1
            + half * half * p2
            + inverse_norm * coefficient.finite_convolution_correction
        )
        z_qp = (
            q0
            + half * q1
            + half * half * q2
            + coefficient.tail_from_finite_correction
        )
        lower_order = max(
            coefficient.current_uniform
            + sqrt_two * 2 * coefficient.delayed_uniform
            + center_base.parameters["epsilon"].upper,
            gmpy2.mpfr(1),
        )
        z_qq = (
            half / tail_gap
            + coefficient.period_upper * lower_order / tail_gap
        )
        finite_input = z_pp + z_qp
        tail_input = z_pq + z_qq
        contraction = max(finite_input, tail_input)
    z_pp_text = decimal_upper(z_pp)
    z_pq_text = decimal_upper(z_pq)
    z_qp_text = decimal_upper(z_qp)
    z_qq_text = decimal_upper(z_qq)
    finite_input_text = _exact_decimal_sum((z_pp_text, z_qp_text))
    tail_input_text = _exact_decimal_sum((z_pq_text, z_qq_text))
    contraction_text = str(
        max(Decimal(finite_input_text), Decimal(tail_input_text))
    )
    margin_text = _exact_decimal_margin(contraction_text)
    validated = Decimal(contraction_text) < 1 and Decimal(margin_text) > 0
    reason = None if validated else "the direct four-block contraction is not strict"
    dimension = 2 * (2 * cutoff + 1)
    certificate = DirectedBlochCellCertificate(
        precision_bits=precision,
        norm_id=_SPLIT_NORM_ID,
        parameter_box_result_sha256=evidence.parameter_box_result_sha256,
        candidate_fingerprint=evidence.candidate_fingerprint,
        cutoff=cutoff,
        complex_finite_dimension=dimension,
        realified_finite_dimension=2 * dimension,
        coefficient_support_half_bandwidth=support_radius,
        phase_lower=phase_lower,
        phase_center=phase_center,
        phase_upper=phase_upper,
        phase_half_width=phase_half_width,
        tail_diagonal_gap_lower=decimal_lower(tail_gap),
        finite_inverse_l1_upper=decimal_upper(inverse_norm),
        finite_inverse_defect_upper=decimal_upper(eta),
        finite_phase_first_product_upper=decimal_upper(mu),
        finite_phase_second_remainder_coefficient_upper=decimal_upper(nu),
        finite_from_tail_center_upper=decimal_upper(p0),
        finite_from_tail_phase_first_upper=decimal_upper(p1),
        finite_from_tail_phase_second_coefficient_upper=decimal_upper(p2),
        tail_from_finite_center_upper=decimal_upper(q0),
        tail_from_finite_phase_first_upper=decimal_upper(q1),
        tail_from_finite_phase_second_coefficient_upper=decimal_upper(q2),
        current_coefficient_center_norm_upper=decimal_upper(
            coefficient.current_center
        ),
        current_coefficient_variation_upper=decimal_upper(
            coefficient.current_variation
        ),
        delayed_coefficient_center_norm_upper=decimal_upper(
            coefficient.delayed_center
        ),
        delayed_coefficient_variation_upper=decimal_upper(
            coefficient.delayed_variation
        ),
        finite_convolution_correction_upper=decimal_upper(
            coefficient.finite_convolution_correction
        ),
        finite_full_correction_upper=decimal_upper(
            coefficient.finite_full_correction
        ),
        tail_from_finite_correction_upper=decimal_upper(
            coefficient.tail_from_finite_correction
        ),
        finite_to_finite_upper=z_pp_text,
        tail_from_finite_upper=z_qp_text,
        finite_from_tail_upper=z_pq_text,
        tail_to_tail_upper=z_qq_text,
        finite_input_column_sum_upper=finite_input_text,
        tail_input_column_sum_upper=tail_input_text,
        contraction_upper=contraction_text,
        contraction_margin_lower=margin_text,
        direct_unbordered_operator=True,
        arbitrary_complex_modes=True,
        moving_delay_output_rotation_validated=True,
        exact_parameter_box_orbit_ball_included=True,
        cell_validated=validated,
        failure_reason=reason,
    )
    _bloch_rotation.cache_clear()
    return certificate


def _geometric_phase_cells(
    lower: str,
    upper: str,
    relative_half_width: str,
    *,
    maximum_cells: int,
) -> tuple[tuple[str, str, str, str], ...]:
    """Return exact-decimal connected cells with approximately fixed ``h/c``."""

    if maximum_cells < 1:
        raise ValueError("maximum_cells must be positive")
    with localcontext() as context:
        context.prec = 120
        quantum = Decimal("1e-70")
        left = Decimal(lower).quantize(quantum, rounding=ROUND_FLOOR)
        target = Decimal(upper).quantize(quantum, rounding=ROUND_CEILING)
        relative = Decimal(relative_half_width)
        if not Decimal(0) < relative < Decimal("0.02"):
            raise ValueError("relative phase half-width must lie in (0,0.02)")
        if left <= 0 or target <= left:
            raise ValueError("the requested phase arc is empty or reversed")
        cells: list[tuple[str, str, str, str]] = []
        while left < target:
            half = (
                left * relative / (Decimal(1) - relative)
            ).quantize(quantum, rounding=ROUND_FLOOR)
            if half <= 0:
                raise ArithmeticError("the geometric Bloch half-width vanished")
            center = left + half
            right = center + half
            if right > target:
                half = (target - left) / 2
                center = left + half
                right = center + half
            cells.append(
                (str(left), str(center), str(right), str(half))
            )
            if len(cells) > maximum_cells:
                raise RuntimeError("the Bloch phase grid exceeds maximum_cells")
            if right <= left:
                raise ArithmeticError("the Bloch phase grid did not advance")
            left = right
    return tuple(cells)


def validate_directed_bloch_arc(
    orbit: PeriodicOrbitCandidate,
    evidence: BlochParameterBoxEvidence,
    *,
    cutoff: int = 64,
    precision: int = 160,
    relative_half_width: str = "0.0125",
    maximum_cells: int = 1000,
) -> tuple[DirectedParameterBoxLocalFloquet, DirectedBlochArcCertificate]:
    """Validate the positive compact arc and transfer by real conjugacy.

    The final cell is allowed to extend by an outward decimal rounding beyond
    ``pi``.  This proves coverage of the exact MPFR enclosure of ``pi`` rather
    than stopping at a binary or truncated decimal approximation.
    """

    prepared = _prepare_bloch_validation(orbit, evidence, precision)
    local = _local_floquet_from_prepared(prepared)
    required_lower = local.local_phase_radius_lower
    required_upper = decimal_upper(pi_interval(precision).upper)
    declarations = _geometric_phase_cells(
        required_lower,
        required_upper,
        relative_half_width,
        maximum_cells=maximum_cells,
    )
    cells: list[DirectedBlochCellCertificate] = []
    failure: str | None = None
    for lower, center, upper, half in declarations:
        cell = validate_directed_bloch_cell(
            orbit,
            evidence,
            phase_lower=lower,
            phase_center=center,
            phase_upper=upper,
            phase_half_width=half,
            cutoff=cutoff,
            precision=precision,
            _prepared=prepared,
        )
        cells.append(cell)
        if not cell.cell_validated:
            failure = (
                "a directed Bloch cell failed at ["
                f"{cell.phase_lower}, {cell.phase_upper}]"
            )
            break

    certificate = _assemble_bloch_arc_certificate(
        local,
        evidence,
        tuple(cells),
        declarations,
        cutoff=cutoff,
        precision=precision,
        relative_half_width=relative_half_width,
        explicit_failure=failure,
    )
    return local, certificate


def _assemble_bloch_arc_certificate(
    local: DirectedParameterBoxLocalFloquet,
    evidence: BlochParameterBoxEvidence,
    cells: tuple[DirectedBlochCellCertificate, ...],
    declarations: tuple[tuple[str, str, str, str], ...],
    *,
    cutoff: int,
    precision: int,
    relative_half_width: str,
    explicit_failure: str | None = None,
) -> DirectedBlochArcCertificate:
    """Assemble already manufactured cells without weakening their evidence."""

    required_lower = local.local_phase_radius_lower
    required_upper = decimal_upper(pi_interval(precision).upper)
    failure = explicit_failure
    connected = bool(cells)
    if cells:
        connected = gmpy2.mpq(cells[0].phase_lower) <= gmpy2.mpq(
            required_lower
        )
        right = gmpy2.mpq(cells[0].phase_upper)
        for cell in cells[1:]:
            left = gmpy2.mpq(cell.phase_lower)
            if left > right:
                connected = False
            right = max(right, gmpy2.mpq(cell.phase_upper))
        connected = connected and right >= gmpy2.mpq(required_upper)
    def structurally_matches(
        cell: DirectedBlochCellCertificate,
        declaration: tuple[str, str, str, str],
    ) -> bool:
        lower, center, upper, half = declaration
        finite_column = Decimal(cell.finite_input_column_sum_upper)
        tail_column = Decimal(cell.tail_input_column_sum_upper)
        contraction = Decimal(cell.contraction_upper)
        margin = Decimal(cell.contraction_margin_lower)
        return (
            (
                cell.phase_lower,
                cell.phase_center,
                cell.phase_upper,
                cell.phase_half_width,
            )
            == (lower, center, upper, half)
            and cell.precision_bits == precision
            and cell.norm_id == _SPLIT_NORM_ID
            and cell.parameter_box_result_sha256
            == evidence.parameter_box_result_sha256
            and cell.candidate_fingerprint == evidence.candidate_fingerprint
            and cell.cutoff == cutoff
            and cell.complex_finite_dimension == 2 * (2 * cutoff + 1)
            and cell.realified_finite_dimension
            == 2 * cell.complex_finite_dimension
            and cell.direct_unbordered_operator
            and cell.arbitrary_complex_modes
            and cell.moving_delay_output_rotation_validated
            and cell.exact_parameter_box_orbit_ball_included
            and cell.cell_validated
            and cell.failure_reason is None
            and cell.finite_input_column_sum_upper
            == _exact_decimal_sum(
                (
                    cell.finite_to_finite_upper,
                    cell.tail_from_finite_upper,
                )
            )
            and cell.tail_input_column_sum_upper
            == _exact_decimal_sum(
                (
                    cell.finite_from_tail_upper,
                    cell.tail_to_tail_upper,
                )
            )
            and contraction == max(finite_column, tail_column)
            and cell.contraction_margin_lower
            == _exact_decimal_margin(cell.contraction_upper)
            and contraction < 1
            and margin > 0
        )

    every = len(cells) == len(declarations) and all(
        structurally_matches(cell, declaration)
        for cell, declaration in zip(cells, declarations)
    )
    maximum_text: str | None = None
    minimum_margin_text: str | None = None
    if cells:
        maximum_text = max(
            (cell.contraction_upper for cell in cells), key=Decimal
        )
        minimum_margin_text = min(
            (cell.contraction_margin_lower for cell in cells), key=Decimal
        )

    # For a real RFDE branch, C y_k = conjugate(y_-k) intertwines
    # L_phi and L_-phi.  This statement includes mode reversal; coefficient
    # conjugation alone would be insufficient.
    conjugacy = True
    full = (
        local.unit_multiplier_algebraically_simple_validated
        and local.local_unit_circle_exclusion_validated
        and connected
        and every
        and conjugacy
    )
    if failure is None and not connected:
        failure = "the directed positive Bloch cells do not cover through pi"
    if failure is None and not every:
        failure = "not every declared positive Bloch cell was validated"
    return DirectedBlochArcCertificate(
        precision_bits=precision,
        norm_id=_SPLIT_NORM_ID,
        local_norm_id=local.norm_id,
        cutoff=cutoff,
        parameter_box_result_sha256=evidence.parameter_box_result_sha256,
        candidate_fingerprint=evidence.candidate_fingerprint,
        local_phase_radius_lower=local.local_phase_radius_lower,
        positive_arc_required_lower=required_lower,
        positive_arc_required_upper=required_upper,
        relative_half_width_seed=relative_half_width,
        cell_count=len(cells),
        maximum_contraction_upper=maximum_text,
        minimum_contraction_margin_lower=minimum_margin_text,
        connected_positive_arc_cover=connected,
        every_cell_validated=every,
        negative_arc_mode_reversal_conjugacy_validated=conjugacy,
        all_nontrivial_unit_multipliers_excluded=full,
        synchronous_orbital_hyperbolicity_validated=full,
        attraction_validated=False,
        full_network_transverse_stability_validated=False,
        cells=tuple(cells),
        failure_reason=failure,
    )
