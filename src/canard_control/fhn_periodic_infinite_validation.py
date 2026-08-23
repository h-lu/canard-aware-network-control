"""Directed finite/tail validation for the synchronous FHN periodic orbit.

The coefficient space is the real-conjugate Fourier subspace with real
period.  Independent positive-mode real/imaginary coordinates receive weight
two, so their ordinary weighted l1 norm is exactly the full unweighted
component Wiener norm

    sum_k (|Re v_k| + |Im v_k| + |Re w_k| + |Im w_k|) + |T|.

The finite block is ``W R J E W^-1`` on those independent real coordinates,
not a complex-period realification and not the nodal collocation Jacobian.
Its complement is preconditioned by the exact Fourier derivative inverse.
All four finite/tail blocks are bounded.

Moving delays are not operator-norm differentiable on a plain Wiener space.
The nonlinear estimate therefore never asserts such a bound. It estimates
finite output modes directly and uses the tail derivative inverse to cancel
the Fourier-mode factor in the moving-shift derivative.
"""

from __future__ import annotations

import ctypes
from dataclasses import dataclass
from typing import Mapping

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
from canard_control.fhn_periodic_candidate import (
    FHNPeriodicParameters,
    PeriodicOrbitCandidate,
)
from canard_control.fhn_periodic_directed_validation import (
    ComplexSequence,
    _binary_product_defect_upper,
    _complex_zero,
    _constant_sequence,
    _interval_parameters,
    _one,
    _sequence_add,
    _sequence_convolution,
    _sequence_derivative,
    _sequence_scale,
    _sequence_shift,
    _sequence_sub,
    directed_dft,
)


@dataclass(frozen=True)
class DealiasedFiniteCoefficientCertificate:
    """Directed proof data for the finite Fourier coefficient block."""

    cutoff: int
    ambient_complex_dimension: int
    real_conjugate_dimension: int
    ambient_complexification_used: bool
    precision_bits: int
    norm: str
    independent_coordinate_weights: str
    residual_support_half_bandwidth: int
    approximate_inverse_l1_upper: str
    finite_jacobian_distance_l1_upper: str
    floating_product_roundoff_upper: str
    finite_inverse_defect_upper: str
    finite_inverse_norm_upper: str | None
    preconditioned_residual_l1_upper: str
    finite_inverse_validated: bool
    ieee_binary64_product_model_checked: bool


@dataclass(frozen=True)
class DirectedFiniteTailBlocks:
    """Four directed block-column bounds for I-A DF(x_bar)."""

    finite_to_finite_upper: str
    tail_from_finite_upper: str
    finite_from_tail_upper: str
    tail_to_tail_upper: str
    finite_input_column_upper: str
    tail_input_column_upper: str
    full_point_defect_upper: str
    full_point_inverse_gate: bool


@dataclass(frozen=True)
class DirectedCorrectionRadiiBound:
    """Polynomial majorant for the correction-ball derivative variation."""

    maximum_radius: str
    coefficient_z1_upper: str
    coefficient_z2_upper: str
    coefficient_z3_upper: str
    chosen_radius: str
    derivative_variation_upper: str
    contraction_upper: str
    radii_left_upper: str
    radii_margin_lower: str
    bordered_inverse_norm_upper: str | None
    radii_polynomial_evaluated: bool
    radii_polynomial_negative: bool


@dataclass(frozen=True)
class DirectedInfinitePeriodicValidation:
    """Combined infinite coefficient-space validation result."""

    parameters: FHNPeriodicParameters
    finite: DealiasedFiniteCoefficientCertificate
    blocks: DirectedFiniteTailBlocks
    correction: DirectedCorrectionRadiiBound
    periodic_rfde_orbit_validated: bool
    bordered_rfde_inverse_validated: bool
    unit_multiplier_simple_validated: bool
    full_floquet_hyperbolicity_validated: bool
    extrema_validated: bool
    response_box_validated: bool
    issue_15_closed: bool
    remaining_gate: str


@dataclass(frozen=True)
class _BaseSequences:
    parameters: dict[str, DirectedInterval]
    period: DirectedInterval
    voltage: ComplexSequence
    recovery: ComplexSequence
    current_coefficient: ComplexSequence
    delayed_coefficients: tuple[ComplexSequence, ComplexSequence]
    residual_voltage: ComplexSequence
    residual_recovery: ComplexSequence
    period_voltage: ComplexSequence
    period_recovery: ComplexSequence
    phase_voltage: ComplexSequence
    phase_recovery: ComplexSequence
    centered_voltage: ComplexSequence
    delayed_field: ComplexSequence
    delayed_field_derivative: ComplexSequence
    delayed_state_derivative: ComplexSequence


@dataclass(frozen=True)
class _RealConjugateLayout:
    """Independent real coordinates for conjugate Fourier sequences.

    Each state has coordinates ``c_0, Re(c_1), Im(c_1), ...``.  The
    normalized coordinates multiply every positive-mode real/imaginary
    coordinate by two, so their ordinary l1 norm is exactly the full
    component Wiener norm after embedding ``c_-k=conj(c_k)``.
    """

    cutoff: int

    @property
    def state_span(self) -> int:
        return 2 * self.cutoff + 1

    @property
    def dimension(self) -> int:
        return 2 * self.state_span + 1

    @property
    def period_index(self) -> int:
        return self.dimension - 1

    def state_index(self, component: int, mode: int, part: str) -> int:
        if component not in (0, 1):
            raise ValueError("component must be zero or one")
        if not 0 <= mode <= self.cutoff:
            raise ValueError("mode lies outside the finite block")
        base = component * self.state_span
        if mode == 0:
            if part != "real":
                raise ValueError("the zero Fourier mode is real")
            return base
        if part == "real":
            return base + 2 * mode - 1
        if part == "imag":
            return base + 2 * mode
        raise ValueError("part must be real or imag")

    @staticmethod
    def state_weight(mode: int) -> int:
        return 1 if mode == 0 else 2


def _embed_normalized_real_coordinates(
    layout: _RealConjugateLayout,
    values: np.ndarray,
) -> tuple[dict[int, complex], dict[int, complex], float]:
    """Apply ``E W^-1`` to normalized independent coordinates."""

    coordinates = np.asarray(values, dtype=float)
    if coordinates.shape != (layout.dimension,):
        raise ValueError("real-conjugate coordinate vector has wrong shape")
    sequences: list[dict[int, complex]] = []
    for component in (0, 1):
        sequence = {
            0: complex(
                coordinates[
                    layout.state_index(component, 0, "real")
                ],
                0.0,
            )
        }
        for mode in range(1, layout.cutoff + 1):
            coefficient = complex(
                coordinates[
                    layout.state_index(component, mode, "real")
                ]
                / 2,
                coordinates[
                    layout.state_index(component, mode, "imag")
                ]
                / 2,
            )
            sequence[mode] = coefficient
            sequence[-mode] = coefficient.conjugate()
        sequences.append(sequence)
    return sequences[0], sequences[1], float(coordinates[-1])


def _restrict_normalized_real_coordinates(
    layout: _RealConjugateLayout,
    voltage: Mapping[int, complex],
    recovery: Mapping[int, complex],
    scalar: float,
) -> np.ndarray:
    """Apply ``W R`` to a real-conjugate coefficient vector."""

    values = np.zeros(layout.dimension, dtype=float)
    for component, sequence in enumerate((voltage, recovery)):
        values[layout.state_index(component, 0, "real")] = float(
            sequence[0].real
        )
        for mode in range(1, layout.cutoff + 1):
            coefficient = sequence[mode]
            values[
                layout.state_index(component, mode, "real")
            ] = 2 * coefficient.real
            values[
                layout.state_index(component, mode, "imag")
            ] = 2 * coefficient.imag
    values[layout.period_index] = float(scalar)
    return values


def _box_abs_upper(value: DirectedComplexInterval) -> gmpy2.mpfr:
    return upward_sum(
        [value.real.upper_abs(), value.imag.upper_abs()],
        value.precision,
    )


def _sequence_box_norm_upper(
    sequence: Mapping[int, DirectedComplexInterval],
    precision: int,
) -> gmpy2.mpfr:
    return upward_sum(
        [_box_abs_upper(value) for value in sequence.values()],
        precision,
    )


def _imaginary_interval(value: DirectedInterval) -> DirectedComplexInterval:
    zero = DirectedInterval.from_decimal(0, value.precision)
    return DirectedComplexInterval(zero, value)


def _sequence_neg(
    sequence: Mapping[int, DirectedComplexInterval],
) -> ComplexSequence:
    return {mode: -value for mode, value in sequence.items()}


def _build_base_sequences(
    orbit: PeriodicOrbitCandidate,
    precision: int,
) -> _BaseSequences:
    parameters = _interval_parameters(orbit.parameters, precision)
    epsilon = parameters["epsilon"]
    kappa_1 = parameters["kappa_1"]
    kappa_3 = parameters["kappa_3"]
    period = DirectedInterval.from_float(orbit.period, precision)
    voltage = directed_dft(orbit.state[:, 0], precision)
    recovery = directed_dft(orbit.state[:, 1], precision)
    one = _constant_sequence(_one(precision), precision)
    unfolding = _constant_sequence(parameters["unfolding"], precision)
    centered = _sequence_sub(voltage, one)
    voltage_squared = _sequence_convolution(voltage, voltage)
    voltage_cubed = _sequence_convolution(voltage_squared, voltage)
    centered_squared = _sequence_convolution(centered, centered)
    centered_cubed = _sequence_convolution(centered_squared, centered)

    delayed: list[ComplexSequence] = []
    delayed_centered_cubed: list[ComplexSequence] = []
    delayed_coefficients: list[ComplexSequence] = []
    for tau in (parameters["tau_0"], parameters["tau_1"]):
        shifted = _sequence_shift(voltage, tau / period)
        shifted_centered = _sequence_sub(shifted, one)
        shifted_centered_squared = _sequence_convolution(
            shifted_centered, shifted_centered
        )
        delayed.append(shifted)
        delayed_centered_cubed.append(
            _sequence_convolution(
                shifted_centered_squared, shifted_centered
            )
        )
        delayed_coefficients.append(
            _sequence_scale(
                _sequence_add(
                    _constant_sequence(kappa_1, precision),
                    _sequence_scale(
                        shifted_centered_squared, 3 * kappa_3
                    ),
                ),
                epsilon / 2,
            )
        )

    linear_difference = _sequence_sub(
        _sequence_scale(_sequence_add(delayed[0], delayed[1]), "0.5"),
        voltage,
    )
    cubic_difference = _sequence_sub(
        _sequence_scale(
            _sequence_add(
                delayed_centered_cubed[0],
                delayed_centered_cubed[1],
            ),
            "0.5",
        ),
        centered_cubed,
    )
    fast = _sequence_sub(
        _sequence_sub(
            voltage,
            _sequence_scale(voltage_cubed, _one(precision) / 3),
        ),
        recovery,
    )
    fast = _sequence_add(
        fast,
        _sequence_scale(linear_difference, epsilon * kappa_1),
    )
    fast = _sequence_add(
        fast,
        _sequence_scale(cubic_difference, epsilon * kappa_3),
    )
    slow = _sequence_scale(
        _sequence_sub(voltage, unfolding), epsilon
    )
    residual_voltage = _sequence_sub(
        _sequence_derivative(voltage, precision),
        _sequence_scale(fast, period),
    )
    residual_recovery = _sequence_sub(
        _sequence_derivative(recovery, precision),
        _sequence_scale(slow, period),
    )

    current = _sequence_sub(
        _constant_sequence(_one(precision) - epsilon * kappa_1, precision),
        voltage_squared,
    )
    current = _sequence_sub(
        current,
        _sequence_scale(centered_squared, 3 * epsilon * kappa_3),
    )
    period_voltage = _sequence_neg(fast)
    tangent_voltage = _sequence_derivative(voltage, precision)
    for tau, coefficient in zip(
        (parameters["tau_0"], parameters["tau_1"]),
        delayed_coefficients,
        strict=True,
    ):
        shifted_tangent = _sequence_shift(tangent_voltage, tau / period)
        period_voltage = _sequence_sub(
            period_voltage,
            _sequence_scale(
                _sequence_convolution(coefficient, shifted_tangent),
                tau / period,
            ),
        )
    period_recovery = _sequence_neg(slow)

    delayed_field = _sequence_add(
        _sequence_scale(voltage, epsilon * kappa_1 / 2),
        _sequence_scale(centered_cubed, epsilon * kappa_3 / 2),
    )
    delayed_field_derivative = _sequence_derivative(
        delayed_field, precision
    )
    delayed_state_derivative = _sequence_add(
        _constant_sequence(epsilon * kappa_1 / 2, precision),
        _sequence_scale(
            centered_squared, 3 * epsilon * kappa_3 / 2
        ),
    )
    return _BaseSequences(
        parameters=parameters,
        period=period,
        voltage=voltage,
        recovery=recovery,
        current_coefficient=current,
        delayed_coefficients=(
            delayed_coefficients[0],
            delayed_coefficients[1],
        ),
        residual_voltage=residual_voltage,
        residual_recovery=residual_recovery,
        period_voltage=period_voltage,
        period_recovery=period_recovery,
        phase_voltage=tangent_voltage,
        phase_recovery=_sequence_derivative(recovery, precision),
        centered_voltage=centered,
        delayed_field=delayed_field,
        delayed_field_derivative=delayed_field_derivative,
        delayed_state_derivative=delayed_state_derivative,
    )


def _state_voltage_entry(
    base: _BaseSequences,
    output_mode: int,
    input_mode: int,
) -> DirectedComplexInterval:
    precision = base.period.precision
    entry = _complex_zero(precision)
    if output_mode == input_mode:
        entry += _imaginary_interval(
            pi_interval(precision) * (2 * output_mode)
        )
    difference = output_mode - input_mode
    entry -= (
        DirectedComplexInterval.from_real(base.period)
        * base.current_coefficient.get(
            difference, _complex_zero(precision)
        )
    )
    for tau, coefficient in zip(
        (base.parameters["tau_0"], base.parameters["tau_1"]),
        base.delayed_coefficients,
        strict=True,
    ):
        shift = complex_unit_interval(
            pi_interval(precision)
            * (-2 * input_mode)
            * tau
            / base.period
        )
        entry -= (
            DirectedComplexInterval.from_real(base.period)
            * coefficient.get(difference, _complex_zero(precision))
            * shift
        )
    return entry


def _embedded_mode_factors(
    mode: int,
    part: str,
    precision: int,
) -> tuple[tuple[int, DirectedComplexInterval], ...]:
    """Embed one independent real coordinate into conjugate coefficients."""

    one = DirectedComplexInterval.from_real(_one(precision))
    if mode == 0:
        if part != "real":
            raise ValueError("the zero Fourier mode has no imaginary coordinate")
        return ((0, one),)
    imaginary = _imaginary_interval(_one(precision))
    if part == "real":
        return ((mode, one), (-mode, one))
    if part == "imag":
        return ((mode, imaginary), (-mode, -imaginary))
    raise ValueError("part must be real or imag")


def _coefficient_column_outputs(
    base: _BaseSequences,
    output_modes: list[int],
    *,
    input_component: int | None,
    input_mode: int = 0,
    input_part: str = "real",
) -> tuple[ComplexSequence, ComplexSequence, DirectedComplexInterval]:
    """Apply the exact coefficient Jacobian to one real-conjugate column.

    ``input_component=None`` denotes the single real period coordinate.
    Only nonnegative output modes are returned; conjugacy supplies the
    negative modes and is accounted for by the coordinate weights.
    """

    precision = base.period.precision
    zero = _complex_zero(precision)
    fast = {mode: zero for mode in output_modes}
    slow = {mode: zero for mode in output_modes}
    phase = zero
    if input_component is None:
        for output_mode in output_modes:
            fast[output_mode] = base.period_voltage.get(output_mode, zero)
            slow[output_mode] = base.period_recovery.get(output_mode, zero)
        return fast, slow, phase

    factors = _embedded_mode_factors(input_mode, input_part, precision)
    for embedded_mode, factor in factors:
        for output_mode in output_modes:
            if input_component == 0:
                fast[output_mode] += (
                    _state_voltage_entry(
                        base, output_mode, embedded_mode
                    )
                    * factor
                )
                if output_mode == embedded_mode:
                    slow[output_mode] += (
                        DirectedComplexInterval.from_real(
                            -(base.period * base.parameters["epsilon"])
                        )
                        * factor
                    )
            elif input_component == 1:
                if output_mode == embedded_mode:
                    fast[output_mode] += (
                        DirectedComplexInterval.from_real(base.period)
                        * factor
                    )
                    slow[output_mode] += (
                        _imaginary_interval(
                            pi_interval(precision) * (2 * output_mode)
                        )
                        * factor
                    )
            else:
                raise ValueError("input_component must be zero, one, or None")
        phase_sequence = (
            base.phase_voltage
            if input_component == 0
            else base.phase_recovery
        )
        phase += phase_sequence.get(-embedded_mode, zero) * factor
    return fast, slow, phase


def _scaled_real_coordinate_intervals(
    layout: _RealConjugateLayout,
    fast: Mapping[int, DirectedComplexInterval],
    slow: Mapping[int, DirectedComplexInterval],
    phase: DirectedComplexInterval,
    *,
    input_weight: int,
) -> list[DirectedInterval]:
    """Restrict to real-conjugate coordinates and apply Wiener weights."""

    precision = phase.precision
    values = [
        DirectedInterval.from_decimal(0, precision)
        for _ in range(layout.dimension)
    ]
    for component, sequence in enumerate((fast, slow)):
        for mode in range(layout.cutoff + 1):
            output_weight = layout.state_weight(mode)
            scale = DirectedInterval.from_decimal(
                output_weight, precision
            ) / input_weight
            value = sequence[mode]
            values[
                layout.state_index(component, mode, "real")
            ] = value.real * scale
            if mode:
                values[
                    layout.state_index(component, mode, "imag")
                ] = value.imag * scale
    values[layout.period_index] = phase.real / input_weight
    return values


def _finite_coefficient_matrix(
    base: _BaseSequences,
    cutoff: int,
) -> tuple[np.ndarray, gmpy2.mpfr, _RealConjugateLayout]:
    """Enclose ``W R J E W^-1`` on independent real coordinates."""

    precision = base.period.precision
    layout = _RealConjugateLayout(cutoff)
    output_modes = list(range(cutoff + 1))
    matrix = np.zeros((layout.dimension, layout.dimension), dtype=float)
    column_distances: list[list[gmpy2.mpfr]] = [
        [] for _ in range(layout.dimension)
    ]

    specifications: list[tuple[int | None, int, str, int, int]] = []
    for component in (0, 1):
        specifications.append(
            (
                component,
                0,
                "real",
                layout.state_index(component, 0, "real"),
                1,
            )
        )
        for mode in range(1, cutoff + 1):
            for part in ("real", "imag"):
                specifications.append(
                    (
                        component,
                        mode,
                        part,
                        layout.state_index(component, mode, part),
                        2,
                    )
                )
    specifications.append((None, 0, "real", layout.period_index, 1))

    for component, mode, part, column, input_weight in specifications:
        fast, slow, phase = _coefficient_column_outputs(
            base,
            output_modes,
            input_component=component,
            input_mode=mode,
            input_part=part,
        )
        intervals = _scaled_real_coordinate_intervals(
            layout,
            fast,
            slow,
            phase,
            input_weight=input_weight,
        )
        for row, enclosure in enumerate(intervals):
            center = float(enclosure.midpoint_nearest())
            matrix[row, column] = center
            center_interval = DirectedInterval.from_float(center, precision)
            column_distances[column].append(
                (enclosure - center_interval).upper_abs()
            )
    distance = max(
        upward_sum(terms, precision) for terms in column_distances
    )
    return matrix, distance, layout


def _float_matrix_l1_upper(
    matrix: np.ndarray,
    precision: int,
) -> gmpy2.mpfr:
    return max(
        upward_sum(
            [
                DirectedInterval.from_float(abs(value), precision).upper
                for value in column
            ],
            precision,
        )
        for column in np.asarray(matrix, dtype=float).T
    )


def _binary_matvec_l1_upper(
    matrix: np.ndarray,
    vector: np.ndarray,
    precision: int,
    matrix_l1_upper: gmpy2.mpfr,
) -> gmpy2.mpfr:
    values = np.asarray(vector, dtype=float)
    operator = np.asarray(matrix, dtype=float)
    if operator.ndim != 2 or operator.shape[1] != len(values):
        raise ValueError("matrix and vector have incompatible dimensions")
    if not np.all(np.isfinite(operator)) or not np.all(np.isfinite(values)):
        raise ValueError("binary matvec inputs must be finite")
    process = ctypes.CDLL(None)
    if not hasattr(process, "fegetround"):
        raise RuntimeError("cannot audit the host floating rounding mode")
    process.fegetround.restype = ctypes.c_int
    if process.fegetround() != 0:
        raise RuntimeError("binary matvec is not running round-to-nearest")
    product = operator @ values
    if not np.all(np.isfinite(product)):
        raise RuntimeError("binary matrix-vector product overflowed")
    if process.fegetround() != 0:
        raise RuntimeError("binary matvec changed the host rounding mode")
    stored = upward_sum(
        [
            DirectedInterval.from_float(abs(value), precision).upper
            for value in product
        ],
        precision,
    )
    vector_norm = upward_sum(
        [
            DirectedInterval.from_float(abs(value), precision).upper
            for value in values
        ],
        precision,
    )
    dimension = operator.shape[1]
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        unit_roundoff = gmpy2.mpfr(2) ** -53
        gamma = dimension * unit_roundoff / (1 - dimension * unit_roundoff)
        smallest_normal = gmpy2.mpfr(2) ** -1022
        roundoff = (
            gamma * matrix_l1_upper * vector_norm
            + operator.shape[0] * dimension * smallest_normal
        )
        return stored + roundoff


def _residual_vector(
    base: _BaseSequences,
    layout: _RealConjugateLayout,
) -> tuple[np.ndarray, gmpy2.mpfr]:
    precision = base.period.precision
    zero = _complex_zero(precision)
    fast = {
        mode: base.residual_voltage.get(mode, zero)
        for mode in range(layout.cutoff + 1)
    }
    slow = {
        mode: base.residual_recovery.get(mode, zero)
        for mode in range(layout.cutoff + 1)
    }
    intervals = _scaled_real_coordinate_intervals(
        layout,
        fast,
        slow,
        zero,
        input_weight=1,
    )
    centers = np.asarray(
        [float(value.midpoint_nearest()) for value in intervals],
        dtype=float,
    )
    distance = upward_sum(
        [
            (
                value
                - DirectedInterval.from_float(float(center), precision)
            ).upper_abs()
            for value, center in zip(intervals, centers, strict=True)
        ],
        precision,
    )
    if len(centers) != layout.dimension:
        raise RuntimeError("residual vector has the wrong dimension")
    return centers, distance


def _tail_residual_upper(
    base: _BaseSequences,
    cutoff: int,
) -> gmpy2.mpfr:
    precision = base.period.precision
    pi = pi_interval(precision)
    terms: list[gmpy2.mpfr] = []
    for sequence in (base.residual_voltage, base.residual_recovery):
        for mode, value in sequence.items():
            if abs(mode) <= cutoff:
                continue
            denominator = (pi * (2 * abs(mode))).lower
            terms.append(
                upward_division(
                    _box_abs_upper(value), denominator, precision
                )
            )
    return upward_sum(terms, precision)


def _tail_from_finite_upper(
    base: _BaseSequences,
    layout: _RealConjugateLayout,
) -> gmpy2.mpfr:
    precision = base.period.precision
    support = set(base.current_coefficient)
    for coefficient in base.delayed_coefficients:
        support.update(coefficient)
    pi = pi_interval(precision)
    column_bounds: list[gmpy2.mpfr] = []
    zero = _complex_zero(precision)
    for input_mode in range(layout.cutoff + 1):
        for input_part in (("real",) if input_mode == 0 else ("real", "imag")):
            tail_output: ComplexSequence = {}
            for embedded_mode, factor in _embedded_mode_factors(
                input_mode, input_part, precision
            ):
                for difference in support:
                    output_mode = embedded_mode + difference
                    if abs(output_mode) <= layout.cutoff:
                        continue
                    tail_output[output_mode] = tail_output.get(
                        output_mode, zero
                    ) + (
                        _state_voltage_entry(
                            base, output_mode, embedded_mode
                        )
                        * factor
                    )
            terms: list[gmpy2.mpfr] = []
            for output_mode, entry in tail_output.items():
                denominator = (pi * (2 * abs(output_mode))).lower
                terms.append(
                    upward_division(
                        _box_abs_upper(entry), denominator, precision
                    )
                )
            input_weight = layout.state_weight(input_mode)
            column_bounds.append(
                upward_division(
                    upward_sum(terms, precision), input_weight, precision
                )
            )

    period_terms: list[gmpy2.mpfr] = []
    for sequence in (base.period_voltage, base.period_recovery):
        for mode, value in sequence.items():
            if abs(mode) <= layout.cutoff:
                continue
            denominator = (pi * (2 * abs(mode))).lower
            period_terms.append(
                upward_division(
                    _box_abs_upper(value), denominator, precision
                )
            )
    column_bounds.append(upward_sum(period_terms, precision))
    return max(column_bounds)


def _finite_from_tail_upper(
    base: _BaseSequences,
    layout: _RealConjugateLayout,
    approximate_inverse: np.ndarray,
    inverse_l1_upper: gmpy2.mpfr,
) -> gmpy2.mpfr:
    precision = base.period.precision
    support = set(base.current_coefficient)
    for coefficient in base.delayed_coefficients:
        support.update(coefficient)
    support_radius = max(abs(mode) for mode in support)
    bounds: list[gmpy2.mpfr] = [gmpy2.mpfr(0, precision)]
    output_modes = list(range(layout.cutoff + 1))
    tail_modes = range(
        layout.cutoff + 1,
        layout.cutoff + support_radius + 1,
    )
    for input_mode in tail_modes:
        for input_part in ("real", "imag"):
            fast, slow, phase = _coefficient_column_outputs(
                base,
                output_modes,
                input_component=0,
                input_mode=input_mode,
                input_part=input_part,
            )
            intervals = _scaled_real_coordinate_intervals(
                layout,
                fast,
                slow,
                phase,
                input_weight=2,
            )
            centers = np.asarray(
                [float(value.midpoint_nearest()) for value in intervals],
                dtype=float,
            )
            distance = upward_sum(
                [
                    (
                        value
                        - DirectedInterval.from_float(
                            float(center), precision
                        )
                    ).upper_abs()
                    for value, center in zip(
                        intervals, centers, strict=True
                    )
                ],
                precision,
            )
            midpoint_bound = _binary_matvec_l1_upper(
                approximate_inverse,
                centers,
                precision,
                inverse_l1_upper,
            )
            with gmpy2.context(
                precision=precision, round=gmpy2.RoundUp
            ):
                bounds.append(
                    midpoint_bound + inverse_l1_upper * distance
                )
    return max(bounds)


def _tail_to_tail_upper(
    base: _BaseSequences,
    cutoff: int,
) -> gmpy2.mpfr:
    precision = base.period.precision
    current_norm = _sequence_box_norm_upper(
        base.current_coefficient, precision
    )
    delayed_norms = [
        _sequence_box_norm_upper(coefficient, precision)
        for coefficient in base.delayed_coefficients
    ]
    sqrt_two = DirectedInterval.from_decimal(2, precision).sqrt().upper
    denominator = (
        pi_interval(precision) * (2 * (cutoff + 1))
    ).lower
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        voltage_column = (
            current_norm
            + sqrt_two * sum(
                delayed_norms, gmpy2.mpfr(0, precision)
            )
            + base.parameters["epsilon"].upper
        )
        lower_order_norm = max(voltage_column, gmpy2.mpfr(1))
        return base.period.upper * lower_order_norm / denominator


def _nonlinear_coefficients(
    base: _BaseSequences,
    cutoff: int,
    approximate_inverse_l1: gmpy2.mpfr,
    maximum_radius: str,
) -> tuple[gmpy2.mpfr, gmpy2.mpfr, gmpy2.mpfr]:
    """Return z1,z2,z3 with ||A Delta DF|| bounded by their polynomial."""

    precision = base.period.precision
    radius = DirectedInterval.from_decimal(maximum_radius, precision)
    minimum_period = (base.period - radius).lower
    maximum_period = (base.period + radius).upper
    if minimum_period <= 0:
        raise ValueError("correction ball crosses nonpositive periods")

    voltage_norm = _sequence_box_norm_upper(base.voltage, precision)
    centered_norm = _sequence_box_norm_upper(
        base.centered_voltage, precision
    )
    delayed_field_norm = _sequence_box_norm_upper(
        base.delayed_field, precision
    )
    delayed_field_derivative_norm = _sequence_box_norm_upper(
        base.delayed_field_derivative, precision
    )
    delayed_state_derivative_norm = _sequence_box_norm_upper(
        base.delayed_state_derivative, precision
    )
    local_derivative_norm = _sequence_box_norm_upper(
        base.current_coefficient, precision
    )
    epsilon = base.parameters["epsilon"].upper
    kappa_1 = base.parameters["kappa_1"].upper
    kappa_3 = base.parameters["kappa_3"].upper
    sqrt_two = DirectedInterval.from_decimal(2, precision).sqrt().upper
    pi_upper = pi_interval(precision).upper

    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        derivative_preconditioner = sqrt_two * (
            approximate_inverse_l1 * 2 * pi_upper * cutoff + 1
        )
        shift_preconditioners = [
            derivative_preconditioner
            * tau.upper
            / (minimum_period * minimum_period)
            for tau in (
                base.parameters["tau_0"],
                base.parameters["tau_1"],
            )
        ]
        shift_sum = sum(
            shift_preconditioners, gmpy2.mpfr(0, precision)
        )

        base_state_column = max(
            local_derivative_norm
            + 2 * sqrt_two * delayed_state_derivative_norm
            + epsilon,
            gmpy2.mpfr(1),
        )
        local_change_1 = 2 * (
            voltage_norm + 3 * epsilon * kappa_3 * centered_norm
        )
        local_change_2 = 1 + 3 * epsilon * kappa_3
        delayed_derivative_change_1 = (
            3 * epsilon * kappa_3 * centered_norm
        )
        delayed_derivative_change_2 = (
            3 * epsilon * kappa_3 / 2
        )
        state_change_1 = (
            local_change_1
            + 2 * sqrt_two * delayed_derivative_change_1
        )
        state_change_2 = (
            local_change_2
            + 2 * sqrt_two * delayed_derivative_change_2
        )
        state_z1 = approximate_inverse_l1 * (
            base_state_column + maximum_period * state_change_1
        ) + (
            maximum_period
            * delayed_state_derivative_norm
            * shift_sum
        )
        state_z2 = (
            approximate_inverse_l1
            * maximum_period
            * state_change_2
        )

        local_field_1 = (
            1
            + epsilon * kappa_1
            + 1
            + voltage_norm * voltage_norm
            + 3 * epsilon * kappa_3 * centered_norm * centered_norm
        )
        local_field_2 = (
            voltage_norm + 3 * epsilon * kappa_3 * centered_norm
        )
        local_field_3 = gmpy2.mpfr(1) / 3 + epsilon * kappa_3
        delayed_field_1 = (
            epsilon * kappa_1 / 2
            + 3
            * epsilon
            * kappa_3
            * centered_norm
            * centered_norm
            / 2
        )
        delayed_field_2 = (
            3 * epsilon * kappa_3 * centered_norm / 2
        )
        delayed_field_3 = epsilon * kappa_3 / 2
        period_z1 = approximate_inverse_l1 * (
            local_field_1 + 2 * sqrt_two * delayed_field_1
        ) + delayed_field_norm * shift_sum
        period_z2 = approximate_inverse_l1 * (
            local_field_2 + 2 * sqrt_two * delayed_field_2
        )
        period_z3 = approximate_inverse_l1 * (
            local_field_3 + 2 * sqrt_two * delayed_field_3
        )
        for tau, shift_bound in zip(
            (
                base.parameters["tau_0"].upper,
                base.parameters["tau_1"].upper,
            ),
            shift_preconditioners,
            strict=True,
        ):
            period_z1 += (
                approximate_inverse_l1
                * sqrt_two
                * delayed_field_derivative_norm
                * tau
                / (minimum_period * base.period.lower)
                + derivative_preconditioner
                * delayed_field_1
                * tau
                / minimum_period
                + shift_bound
                * delayed_field_derivative_norm
                * tau
                / minimum_period
            )
            period_z2 += (
                derivative_preconditioner
                * delayed_field_2
                * tau
                / minimum_period
            )
            period_z3 += (
                derivative_preconditioner
                * delayed_field_3
                * tau
                / minimum_period
            )
        period_z1 += approximate_inverse_l1 * epsilon
        return (
            max(state_z1, period_z1),
            max(state_z2, period_z2),
            max(gmpy2.mpfr(0, precision), period_z3),
        )


def validate_infinite_periodic_candidate(
    orbit: PeriodicOrbitCandidate,
    *,
    cutoff: int = 144,
    precision: int = 160,
    maximum_radius: str = "1e-7",
    chosen_radius: str = "1e-7",
) -> DirectedInfinitePeriodicValidation:
    """Validate the center periodic RFDE orbit in a Wiener correction ball."""

    if cutoff < 3 * ((len(orbit.state) - 1) // 2):
        raise ValueError(
            "cutoff must contain the full cubic residual support"
        )
    if orbit.parameters.kappa_1 < 0 or orbit.parameters.kappa_3 < 0:
        raise ValueError(
            "the current nonlinear majorant requires nonnegative gains"
        )
    base = _build_base_sequences(orbit, precision)
    real_matrix, matrix_distance, layout = _finite_coefficient_matrix(
        base, cutoff
    )
    approximate_inverse = np.linalg.inv(real_matrix)
    inverse_norm = _float_matrix_l1_upper(
        approximate_inverse, precision
    )

    base_defect, product_roundoff, _, ieee_checked = (
        _binary_product_defect_upper(
            real_matrix.T,
            approximate_inverse.T,
            precision,
        )
    )
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        finite_defect = base_defect + inverse_norm * matrix_distance
    finite_inverse_norm: gmpy2.mpfr | None = None
    if finite_defect < 1:
        with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
            finite_inverse_norm = inverse_norm / (1 - finite_defect)

    residual_midpoint, residual_distance = _residual_vector(base, layout)
    finite_y = _binary_matvec_l1_upper(
        approximate_inverse,
        residual_midpoint,
        precision,
        inverse_norm,
    )
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        finite_y += inverse_norm * residual_distance
        total_y = finite_y + _tail_residual_upper(base, cutoff)

    tail_from_finite = _tail_from_finite_upper(base, layout)
    finite_from_tail = _finite_from_tail_upper(
        base,
        layout,
        approximate_inverse,
        inverse_norm,
    )
    tail_to_tail = _tail_to_tail_upper(base, cutoff)
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        finite_input = finite_defect + tail_from_finite
        tail_input = finite_from_tail + tail_to_tail
        full_defect = max(finite_input, tail_input)

    z1, z2, z3 = _nonlinear_coefficients(
        base,
        cutoff,
        inverse_norm,
        maximum_radius,
    )
    radius = DirectedInterval.from_decimal(chosen_radius, precision)
    maximum = DirectedInterval.from_decimal(maximum_radius, precision)
    if radius.upper > maximum.upper:
        raise ValueError("chosen radius exceeds the coefficient-bound radius")
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
    radii_negative = contraction < 1 and margin > 0
    bordered_inverse_norm: gmpy2.mpfr | None = None
    if radii_negative:
        with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
            bordered_inverse_norm = inverse_norm / (1 - contraction)

    residual_support = max(
        max(abs(mode) for mode in base.residual_voltage),
        max(abs(mode) for mode in base.residual_recovery),
    )
    finite = DealiasedFiniteCoefficientCertificate(
        cutoff=cutoff,
        ambient_complex_dimension=2 * (2 * cutoff + 1) + 1,
        real_conjugate_dimension=layout.dimension,
        ambient_complexification_used=False,
        precision_bits=precision,
        norm="unweighted component Wiener l1 plus the period scalar",
        independent_coordinate_weights=(
            "mode zero and period weight 1; each positive-mode real and "
            "imaginary coordinate weight 2"
        ),
        residual_support_half_bandwidth=residual_support,
        approximate_inverse_l1_upper=decimal_upper(inverse_norm),
        finite_jacobian_distance_l1_upper=decimal_upper(matrix_distance),
        floating_product_roundoff_upper=decimal_upper(product_roundoff),
        finite_inverse_defect_upper=decimal_upper(finite_defect),
        finite_inverse_norm_upper=(
            decimal_upper(finite_inverse_norm)
            if finite_inverse_norm is not None
            else None
        ),
        preconditioned_residual_l1_upper=decimal_upper(total_y),
        finite_inverse_validated=finite_inverse_norm is not None,
        ieee_binary64_product_model_checked=ieee_checked,
    )
    blocks = DirectedFiniteTailBlocks(
        finite_to_finite_upper=decimal_upper(finite_defect),
        tail_from_finite_upper=decimal_upper(tail_from_finite),
        finite_from_tail_upper=decimal_upper(finite_from_tail),
        tail_to_tail_upper=decimal_upper(tail_to_tail),
        finite_input_column_upper=decimal_upper(finite_input),
        tail_input_column_upper=decimal_upper(tail_input),
        full_point_defect_upper=decimal_upper(full_defect),
        full_point_inverse_gate=full_defect < 1,
    )
    correction = DirectedCorrectionRadiiBound(
        maximum_radius=maximum_radius,
        coefficient_z1_upper=decimal_upper(z1),
        coefficient_z2_upper=decimal_upper(z2),
        coefficient_z3_upper=decimal_upper(z3),
        chosen_radius=chosen_radius,
        derivative_variation_upper=decimal_upper(variation),
        contraction_upper=decimal_upper(contraction),
        radii_left_upper=decimal_upper(radii_left),
        radii_margin_lower=decimal_lower(margin),
        bordered_inverse_norm_upper=(
            decimal_upper(bordered_inverse_norm)
            if bordered_inverse_norm is not None
            else None
        ),
        radii_polynomial_evaluated=True,
        radii_polynomial_negative=radii_negative,
    )
    orbit_validated = radii_negative
    return DirectedInfinitePeriodicValidation(
        parameters=orbit.parameters,
        finite=finite,
        blocks=blocks,
        correction=correction,
        periodic_rfde_orbit_validated=orbit_validated,
        bordered_rfde_inverse_validated=orbit_validated,
        unit_multiplier_simple_validated=False,
        full_floquet_hyperbolicity_validated=False,
        extrema_validated=False,
        response_box_validated=False,
        issue_15_closed=False,
        remaining_gate=(
            "The center RFDE orbit and its phase-bordered inverse are "
            "validated. A separate Fredholm-to-monodromy transfer is still "
            "required before calling the unit Floquet multiplier simple; "
            "full Floquet hyperbolicity, extrema over a parameter box, and "
            "the 2x2 frequency-amplitude response certificate remain open."
        ),
    )
