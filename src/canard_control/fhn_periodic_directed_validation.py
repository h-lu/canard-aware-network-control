"""Directed finite validation and Fourier residual bounds for the FHN orbit.

The finite collocation root is validated with MPFR-directed interval
arithmetic and a contraction/radii inequality.  Separately, exact interval
convolutions enclose the residual of the associated trigonometric polynomial
outside as well as inside the collocation band.

This module does **not** claim an infinite-dimensional RFDE proof.  The
missing seam is a coupled finite/tail inverse and nonlinear tail radii
estimate.  The returned result contains explicit false validation flags
until that seam is supplied.
"""

from __future__ import annotations

import ctypes
from dataclasses import dataclass
from typing import Mapping, Sequence

import gmpy2
import numpy as np

from canard_control.directed_interval import (
    DirectedComplexInterval,
    DirectedInterval,
    complex_unit_interval,
    cos_interval,
    decimal_lower,
    decimal_upper,
    downward_sum,
    pi_interval,
    upward_product,
    upward_sum,
)
from canard_control.fhn_periodic_candidate import (
    FHNPeriodicParameters,
    PeriodicOrbitCandidate,
    _collocation_system,
    odd_fourier_matrices,
)


IntervalMatrix = list[list[DirectedInterval]]
ComplexSequence = dict[int, DirectedComplexInterval]


@dataclass(frozen=True)
class DirectedFourierResidual:
    """Directed Wiener-norm bounds for one finite Fourier polynomial."""

    node_count: int
    original_half_bandwidth: int
    residual_support_half_bandwidth: int
    precision_bits: int
    unweighted_l1_lower: str
    unweighted_l1_upper: str
    weighted_l1_nu: str
    weighted_l1_upper: str
    outside_collocation_band_l1_lower: str
    outside_collocation_band_l1_upper: str
    maximum_coefficient_lower: str
    maximum_coefficient_upper: str
    orbit_edge_coefficient_l1_upper: str
    linear_tail_wiener_bound_upper: str
    tail_derivative_neumann_ratio_upper: str
    tail_derivative_neumann_gate: bool


@dataclass(frozen=True)
class DirectedFiniteCollocationValidation:
    """Directed contraction certificate for the exact finite nodal map."""

    node_count: int
    bordered_dimension: int
    precision_bits: int
    backend: str
    residual_inf_upper: str
    point_jacobian_enclosure_radius_inf_upper: str
    approximate_inverse_inf_upper: str
    floating_product_roundoff_upper: str
    point_inverse_defect_upper: str
    point_inverse_norm_upper: str | None
    newton_image_bound_upper: str
    contraction_radius: str | None
    uniform_inverse_defect_upper: str | None
    uniform_inverse_norm_upper: str | None
    radii_left_upper: str | None
    radii_margin_lower: str | None
    exact_finite_collocation_root_validated: bool
    exact_finite_bordered_inverse_validated: bool
    ieee_binary64_product_model_checked: bool
    failure_reason: str | None


@dataclass(frozen=True)
class DirectedFHNValidationResult:
    """Combined result with an explicit infinite-dimensional refusal."""

    parameters: FHNPeriodicParameters
    finite: DirectedFiniteCollocationValidation
    fourier: DirectedFourierResidual
    finite_tail_coupling_bound_supplied: bool
    nonlinear_correction_tail_bound_supplied: bool
    infinite_radii_polynomial_evaluated: bool
    periodic_rfde_orbit_validated: bool
    bordered_rfde_inverse_validated: bool
    missing_infinite_bounds: tuple[str, ...]
    falsifier: str


def _zero(precision: int) -> DirectedInterval:
    return DirectedInterval.from_decimal(0, precision)


def _one(precision: int) -> DirectedInterval:
    return DirectedInterval.from_decimal(1, precision)


def _decimal_parameter(value: float, precision: int) -> DirectedInterval:
    # The human-declared input is the shortest decimal spelling, not the
    # nearby binary64 value used to initialize the numerical solve.
    return DirectedInterval.from_decimal(str(float(value)), precision)


def _interval_parameters(
    parameters: FHNPeriodicParameters, precision: int
) -> dict[str, DirectedInterval]:
    epsilon = _decimal_parameter(parameters.epsilon, precision)
    return {
        "epsilon": epsilon,
        "unfolding": _decimal_parameter(parameters.unfolding, precision),
        "theta_0": _decimal_parameter(parameters.theta_0, precision),
        "theta_1": _decimal_parameter(parameters.theta_1, precision),
        "kappa_1": _decimal_parameter(parameters.kappa_1, precision),
        "kappa_3": _decimal_parameter(parameters.kappa_3, precision),
        "tau_0": _decimal_parameter(parameters.theta_0, precision)
        / epsilon.sqrt(),
        "tau_1": _decimal_parameter(parameters.theta_1, precision)
        / epsilon.sqrt(),
    }


def directed_odd_fourier_matrices(
    node_count: int,
    delay_fraction: DirectedInterval,
) -> tuple[IntervalMatrix, IntervalMatrix]:
    """Enclose the exact odd Fourier derivative and shift matrices."""

    if node_count < 5 or node_count % 2 == 0:
        raise ValueError("node_count must be odd and at least five")
    precision = delay_fraction.precision
    pi = pi_interval(precision)
    count_interval = DirectedInterval.from_decimal(node_count, precision)
    derivative_offsets: list[DirectedInterval] = [_zero(precision)]
    shift_offsets: list[DirectedInterval] = []
    half_bandwidth = (node_count - 1) // 2
    for offset in range(1, node_count):
        angle = pi * DirectedInterval.from_decimal(offset, precision) / count_interval
        sine = _sin_for_spectral_denominator(angle)
        sign = -1 if offset % 2 else 1
        derivative_offsets.append(pi * sign / sine)
    for offset in range(node_count):
        phase = (
            DirectedInterval.from_decimal(offset, precision) / count_interval
            - delay_fraction
        )
        value = _one(precision)
        for mode in range(1, half_bandwidth + 1):
            angle = pi * 2 * mode * phase
            value += 2 * cos_interval(angle)
        shift_offsets.append(value / count_interval)
    derivative: IntervalMatrix = []
    shift: IntervalMatrix = []
    for row in range(node_count):
        derivative.append(
            [
                derivative_offsets[(row - column) % node_count]
                for column in range(node_count)
            ]
        )
        shift.append(
            [shift_offsets[(row - column) % node_count] for column in range(node_count)]
        )
    return derivative, shift


def _sin_for_spectral_denominator(angle: DirectedInterval) -> DirectedInterval:
    from canard_control.directed_interval import sin_interval

    result = sin_interval(angle)
    if result.contains_zero():
        raise RuntimeError("spectral denominator enclosure unexpectedly contains zero")
    return result


def _interval_matvec(
    matrix: IntervalMatrix, vector: Sequence[DirectedInterval]
) -> list[DirectedInterval]:
    if not matrix or len(matrix[0]) != len(vector):
        raise ValueError("incompatible interval matrix/vector shapes")
    result: list[DirectedInterval] = []
    for row in matrix:
        total = _zero(vector[0].precision)
        for coefficient, value in zip(row, vector, strict=True):
            total += coefficient * value
        result.append(total)
    return result


def _interval_system(
    orbit: PeriodicOrbitCandidate,
    radius: gmpy2.mpfr,
    precision: int,
) -> tuple[list[DirectedInterval], IntervalMatrix]:
    """Enclose the residual and Jacobian on an infinity-norm ball."""

    count = len(orbit.state)
    parameters = _interval_parameters(orbit.parameters, precision)
    epsilon = parameters["epsilon"]
    unfolding = parameters["unfolding"]
    kappa_1 = parameters["kappa_1"]
    kappa_3 = parameters["kappa_3"]
    voltage = [
        DirectedInterval.symmetric_radius(value, radius, precision)
        for value in orbit.state[:, 0]
    ]
    recovery = [
        DirectedInterval.symmetric_radius(value, radius, precision)
        for value in orbit.state[:, 1]
    ]
    period = DirectedInterval.symmetric_radius(orbit.period, radius, precision)
    if period.lower <= 0:
        raise ValueError("validation ball crosses nonpositive periods")
    alpha_0 = parameters["tau_0"] / period
    alpha_1 = parameters["tau_1"] / period
    derivative, shift_0 = directed_odd_fourier_matrices(count, alpha_0)
    _, shift_1 = directed_odd_fourier_matrices(count, alpha_1)
    delayed_0 = _interval_matvec(shift_0, voltage)
    delayed_1 = _interval_matvec(shift_1, voltage)
    tangent_voltage = _interval_matvec(derivative, voltage)
    tangent_recovery = _interval_matvec(derivative, recovery)
    delayed_tangent_0 = _interval_matvec(shift_0, tangent_voltage)
    delayed_tangent_1 = _interval_matvec(shift_1, tangent_voltage)

    fast: list[DirectedInterval] = []
    slow: list[DirectedInterval] = []
    current_voltage: list[DirectedInterval] = []
    delayed_voltage_0: list[DirectedInterval] = []
    delayed_voltage_1: list[DirectedInterval] = []
    for voltage_now, recovery_now, delay_0, delay_1 in zip(
        voltage, recovery, delayed_0, delayed_1, strict=True
    ):
        linear_difference = (delay_0 + delay_1) / 2 - voltage_now
        cubic_difference = (
            ((delay_0 - 1) ** 3 + (delay_1 - 1) ** 3) / 2
            - (voltage_now - 1) ** 3
        )
        fast.append(
            voltage_now
            - voltage_now**3 / 3
            - recovery_now
            + epsilon * kappa_1 * linear_difference
            + epsilon * kappa_3 * cubic_difference
        )
        slow.append(epsilon * (voltage_now - unfolding))
        current_voltage.append(
            1
            - voltage_now**2
            - epsilon * kappa_1
            - 3 * epsilon * kappa_3 * (voltage_now - 1) ** 2
        )
        delayed_voltage_0.append(
            epsilon / 2 * (kappa_1 + 3 * kappa_3 * (delay_0 - 1) ** 2)
        )
        delayed_voltage_1.append(
            epsilon / 2 * (kappa_1 + 3 * kappa_3 * (delay_1 - 1) ** 2)
        )

    residual_fast = [
        tangent - period * field
        for tangent, field in zip(tangent_voltage, fast, strict=True)
    ]
    residual_slow = [
        tangent - period * field
        for tangent, field in zip(tangent_recovery, slow, strict=True)
    ]

    reference_voltage = [
        DirectedInterval.from_float(value, precision) for value in orbit.state[:, 0]
    ]
    reference_recovery = [
        DirectedInterval.from_float(value, precision) for value in orbit.state[:, 1]
    ]
    reference_tangent_voltage = _interval_matvec(derivative, reference_voltage)
    reference_tangent_recovery = _interval_matvec(derivative, reference_recovery)
    phase = _zero(precision)
    for ref_v, ref_w, value_v, value_w, center_v, center_w in zip(
        reference_tangent_voltage,
        reference_tangent_recovery,
        voltage,
        recovery,
        reference_voltage,
        reference_recovery,
        strict=True,
    ):
        phase += ref_v * (value_v - center_v) + ref_w * (value_w - center_w)
    phase /= count
    residual = [*residual_fast, *residual_slow, phase]

    dimension = 2 * count + 1
    jacobian: IntervalMatrix = [
        [_zero(precision) for _ in range(dimension)] for _ in range(dimension)
    ]
    for row in range(count):
        for column in range(count):
            entry = derivative[row][column]
            if row == column:
                entry -= period * current_voltage[row]
            entry -= period * (
                delayed_voltage_0[row] * shift_0[row][column]
                + delayed_voltage_1[row] * shift_1[row][column]
            )
            jacobian[row][column] = entry
            if row == column:
                jacobian[row][count + column] = period
                jacobian[count + row][column] = -period * epsilon
            jacobian[count + row][count + column] = derivative[row][column]
        jacobian[row][-1] = -fast[row] - (
            parameters["tau_0"]
            / period
            * delayed_voltage_0[row]
            * delayed_tangent_0[row]
            + parameters["tau_1"]
            / period
            * delayed_voltage_1[row]
            * delayed_tangent_1[row]
        )
        jacobian[count + row][-1] = -slow[row]
        jacobian[-1][row] = reference_tangent_voltage[row] / count
        jacobian[-1][count + row] = reference_tangent_recovery[row] / count
    return residual, jacobian


def _interval_vector_inf_upper(values: Sequence[DirectedInterval]) -> gmpy2.mpfr:
    return max(value.upper_abs() for value in values)


def _float_matrix_inf_upper(matrix: np.ndarray, precision: int) -> gmpy2.mpfr:
    row_bounds: list[gmpy2.mpfr] = []
    for row in np.asarray(matrix, dtype=float):
        terms = [
            DirectedInterval.from_float(abs(value), precision).upper
            for value in row
        ]
        row_bounds.append(upward_sum(terms, precision))
    return max(row_bounds)


def _interval_matrix_distance_inf_upper(
    enclosure: IntervalMatrix,
    midpoint: np.ndarray,
    precision: int,
) -> gmpy2.mpfr:
    if np.shape(midpoint) != (len(enclosure), len(enclosure)):
        raise ValueError("midpoint matrix has incompatible shape")
    row_bounds: list[gmpy2.mpfr] = []
    for interval_row, midpoint_row in zip(enclosure, midpoint, strict=True):
        terms: list[gmpy2.mpfr] = []
        for interval, center in zip(interval_row, midpoint_row, strict=True):
            center_interval = DirectedInterval.from_float(float(center), precision)
            terms.append((interval - center_interval).upper_abs())
        row_bounds.append(upward_sum(terms, precision))
    return max(row_bounds)


def _binary_product_defect_upper(
    approximate_inverse: np.ndarray,
    midpoint: np.ndarray,
    precision: int,
) -> tuple[gmpy2.mpfr, gmpy2.mpfr, gmpy2.mpfr, bool]:
    """Bound ``||I-A*J||_inf`` for exact binary matrices A and J.

    NumPy supplies the binary64 product.  The difference between that stored
    product and the exact real product of its binary inputs is bounded by
    Higham's ``gamma_n`` dot-product model plus gradual-underflow correction.
    """

    a = np.asarray(approximate_inverse, dtype=float)
    j = np.asarray(midpoint, dtype=float)
    if a.shape != j.shape or a.shape[0] != a.shape[1]:
        raise ValueError("inverse and midpoint must be equal square matrices")
    if not np.all(np.isfinite(a)) or not np.all(np.isfinite(j)):
        raise ValueError("binary matrices must be finite")
    float_info = np.finfo(float)
    binary64 = (
        float_info.bits == 64
        and float_info.nmant == 52
        and float_info.eps == 2.0**-52
        and np.nextafter(0.0, 1.0) == float.fromhex("0x0.0000000000001p-1022")
    )
    process = ctypes.CDLL(None)
    if not hasattr(process, "fegetround"):
        raise RuntimeError("cannot audit the host floating rounding mode")
    process.fegetround.restype = ctypes.c_int
    round_to_nearest_before = process.fegetround() == 0
    if not binary64 or not round_to_nearest_before:
        raise RuntimeError(
            "binary product accelerator is not IEEE binary64 round-to-nearest"
        )
    dimension = a.shape[0]
    product = a @ j
    round_to_nearest_after = process.fegetround() == 0
    if not np.all(np.isfinite(product)):
        raise RuntimeError("binary matrix product overflowed")
    if not round_to_nearest_after:
        raise RuntimeError("binary matrix product changed the host rounding mode")

    exact_stored_residual_rows: list[gmpy2.mpfr] = []
    for row in range(dimension):
        terms: list[gmpy2.mpfr] = []
        for column in range(dimension):
            target = 1.0 if row == column else 0.0
            exact_difference = DirectedInterval.from_float(target, precision) - (
                DirectedInterval.from_float(float(product[row, column]), precision)
            )
            terms.append(exact_difference.upper_abs())
        exact_stored_residual_rows.append(upward_sum(terms, precision))
    stored_residual = max(exact_stored_residual_rows)

    a_norm = _float_matrix_inf_upper(a, precision)
    j_norm = _float_matrix_inf_upper(j, precision)
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        unit_roundoff = gmpy2.mpfr(2) ** -53
        gamma = dimension * unit_roundoff / (1 - dimension * unit_roundoff)
        relative_roundoff = gamma * a_norm * j_norm
        # Use the smallest *normal* number, not the smallest subnormal.  This
        # remains valid even if a BLAS kernel flushes subnormals to zero.
        smallest_normal = gmpy2.mpfr(2) ** -1022
        underflow_correction = dimension * dimension * smallest_normal
        roundoff = relative_roundoff + underflow_correction
        defect = stored_residual + roundoff
    return defect, roundoff, a_norm, True


def _mpfr_lower_difference(
    left: gmpy2.mpfr, right: gmpy2.mpfr, precision: int
) -> gmpy2.mpfr:
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        return left - right


def validate_finite_collocation_candidate(
    orbit: PeriodicOrbitCandidate,
    *,
    precision: int = 160,
    maximum_radius_trials: int = 4,
) -> DirectedFiniteCollocationValidation:
    """Validate a root of the exact finite odd-Fourier nodal equations."""

    if maximum_radius_trials < 1:
        raise ValueError("maximum_radius_trials must be positive")
    count = len(orbit.state)
    derivative, _ = odd_fourier_matrices(count)
    reference_derivative = derivative @ orbit.state
    unknown = np.concatenate(
        (orbit.state[:, 0], orbit.state[:, 1], [orbit.period])
    )
    _, midpoint_jacobian, _ = _collocation_system(
        unknown,
        orbit.parameters,
        derivative,
        orbit.state,
        reference_derivative,
    )
    approximate_inverse = np.linalg.inv(midpoint_jacobian)
    zero_radius = gmpy2.mpfr(0, precision)
    residual_enclosure, point_jacobian = _interval_system(
        orbit, zero_radius, precision
    )
    residual_upper = _interval_vector_inf_upper(residual_enclosure)
    point_distance = _interval_matrix_distance_inf_upper(
        point_jacobian, midpoint_jacobian, precision
    )
    base_defect, roundoff, inverse_norm, ieee_checked = (
        _binary_product_defect_upper(
            approximate_inverse, midpoint_jacobian, precision
        )
    )
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        point_defect = base_defect + inverse_norm * point_distance
        newton_image = inverse_norm * residual_upper

    inverse_bound: gmpy2.mpfr | None = None
    if point_defect < 1:
        with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
            inverse_bound = inverse_norm / (1 - point_defect)

    chosen_radius: gmpy2.mpfr | None = None
    uniform_defect: gmpy2.mpfr | None = None
    radii_left: gmpy2.mpfr | None = None
    radii_margin: gmpy2.mpfr | None = None
    uniform_inverse_bound: gmpy2.mpfr | None = None
    failure_reason: str | None = None
    if point_defect >= 1:
        failure_reason = "point inverse-defect bound is not below one"
    else:
        with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
            base_radius = 2 * newton_image / (1 - point_defect)
        if base_radius == 0:
            base_radius = gmpy2.mpfr(2) ** (-(precision // 2))
        for trial in range(maximum_radius_trials):
            with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
                radius = base_radius * (2**trial)
            _, box_jacobian = _interval_system(orbit, radius, precision)
            box_distance = _interval_matrix_distance_inf_upper(
                box_jacobian, midpoint_jacobian, precision
            )
            with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
                contraction = base_defect + inverse_norm * box_distance
                left = newton_image + contraction * radius
            margin = _mpfr_lower_difference(radius, left, precision)
            if contraction < 1 and margin > 0:
                chosen_radius = radius
                uniform_defect = contraction
                radii_left = left
                radii_margin = margin
                with gmpy2.context(
                    precision=precision, round=gmpy2.RoundUp
                ):
                    uniform_inverse_bound = inverse_norm / (1 - contraction)
                break
        if chosen_radius is None:
            failure_reason = (
                "no tested radius makes Y+Z(r)r<r with Z(r)<1"
            )
    finite_root = chosen_radius is not None
    finite_uniform_inverse = (
        finite_root and uniform_defect is not None and uniform_defect < 1
    )
    return DirectedFiniteCollocationValidation(
        node_count=count,
        bordered_dimension=2 * count + 1,
        precision_bits=precision,
        backend=f"gmpy2 {gmpy2.version()} / MPFR {gmpy2.mpfr_version()}",
        residual_inf_upper=decimal_upper(residual_upper),
        point_jacobian_enclosure_radius_inf_upper=decimal_upper(point_distance),
        approximate_inverse_inf_upper=decimal_upper(inverse_norm),
        floating_product_roundoff_upper=decimal_upper(roundoff),
        point_inverse_defect_upper=decimal_upper(point_defect),
        point_inverse_norm_upper=(
            decimal_upper(inverse_bound) if inverse_bound is not None else None
        ),
        newton_image_bound_upper=decimal_upper(newton_image),
        contraction_radius=(
            decimal_upper(chosen_radius) if chosen_radius is not None else None
        ),
        uniform_inverse_defect_upper=(
            decimal_upper(uniform_defect) if uniform_defect is not None else None
        ),
        uniform_inverse_norm_upper=(
            decimal_upper(uniform_inverse_bound)
            if uniform_inverse_bound is not None
            else None
        ),
        radii_left_upper=(
            decimal_upper(radii_left) if radii_left is not None else None
        ),
        radii_margin_lower=(
            decimal_lower(radii_margin) if radii_margin is not None else None
        ),
        exact_finite_collocation_root_validated=finite_root,
        exact_finite_bordered_inverse_validated=finite_uniform_inverse,
        ieee_binary64_product_model_checked=ieee_checked,
        failure_reason=failure_reason,
    )


def _complex_zero(precision: int) -> DirectedComplexInterval:
    return DirectedComplexInterval.zero(precision)


def directed_dft(samples: Sequence[float], precision: int = 160) -> ComplexSequence:
    """Enclose every coefficient of the odd trigonometric interpolant."""

    count = len(samples)
    if count < 5 or count % 2 == 0:
        raise ValueError("sample count must be odd and at least five")
    half_bandwidth = (count - 1) // 2
    pi = pi_interval(precision)
    denominator = DirectedInterval.from_decimal(count, precision)
    values = [DirectedInterval.from_float(float(item), precision) for item in samples]
    coefficients: ComplexSequence = {}
    for mode in range(-half_bandwidth, half_bandwidth + 1):
        total = _complex_zero(precision)
        for node, value in enumerate(values):
            angle = (
                pi
                * DirectedInterval.from_decimal(-2 * mode * node, precision)
                / denominator
            )
            total += (
                DirectedComplexInterval.from_real(value)
                * complex_unit_interval(angle)
            )
        coefficients[mode] = total * (1 / denominator)
    return coefficients


def _sequence_add(
    left: Mapping[int, DirectedComplexInterval],
    right: Mapping[int, DirectedComplexInterval],
) -> ComplexSequence:
    if not left and not right:
        raise ValueError("at least one Fourier sequence must be nonempty")
    source = left if left else right
    precision = next(iter(source.values())).precision
    result: ComplexSequence = {}
    for mode in set(left) | set(right):
        result[mode] = left.get(mode, _complex_zero(precision)) + right.get(
            mode, _complex_zero(precision)
        )
    return result


def _sequence_neg(sequence: Mapping[int, DirectedComplexInterval]) -> ComplexSequence:
    return {mode: -value for mode, value in sequence.items()}


def _sequence_sub(
    left: Mapping[int, DirectedComplexInterval],
    right: Mapping[int, DirectedComplexInterval],
) -> ComplexSequence:
    return _sequence_add(left, _sequence_neg(right))


def _sequence_scale(
    sequence: Mapping[int, DirectedComplexInterval],
    scalar: DirectedInterval | int | str | float,
) -> ComplexSequence:
    return {mode: value * scalar for mode, value in sequence.items()}


def _sequence_convolution(
    left: Mapping[int, DirectedComplexInterval],
    right: Mapping[int, DirectedComplexInterval],
) -> ComplexSequence:
    precision = next(iter(left.values())).precision
    result: ComplexSequence = {}
    for left_mode, left_value in left.items():
        for right_mode, right_value in right.items():
            mode = left_mode + right_mode
            result[mode] = result.get(mode, _complex_zero(precision)) + (
                left_value * right_value
            )
    return result


def _sequence_derivative(
    sequence: Mapping[int, DirectedComplexInterval], precision: int
) -> ComplexSequence:
    pi = pi_interval(precision)
    result: ComplexSequence = {}
    for mode, value in sequence.items():
        imaginary_factor = pi * 2 * mode
        factor = DirectedComplexInterval(_zero(precision), imaginary_factor)
        result[mode] = value * factor
    return result


def _sequence_shift(
    sequence: Mapping[int, DirectedComplexInterval],
    delay_fraction: DirectedInterval,
) -> ComplexSequence:
    pi = pi_interval(delay_fraction.precision)
    return {
        mode: value
        * complex_unit_interval(pi * (-2 * mode) * delay_fraction)
        for mode, value in sequence.items()
    }


def _constant_sequence(
    value: DirectedInterval, precision: int
) -> ComplexSequence:
    return {0: DirectedComplexInterval.from_real(value)}


def _sequence_wiener_upper(
    sequence: Mapping[int, DirectedComplexInterval],
    precision: int,
) -> gmpy2.mpfr:
    return upward_sum([value.upper_abs() for value in sequence.values()], precision)


def _vector_sequence_l1_upper(
    voltage: Mapping[int, DirectedComplexInterval],
    recovery: Mapping[int, DirectedComplexInterval],
    precision: int,
    *,
    minimum_mode: int = 0,
    weight_nu: DirectedInterval | None = None,
) -> gmpy2.mpfr:
    terms: list[gmpy2.mpfr] = []
    for mode in set(voltage) | set(recovery):
        if abs(mode) < minimum_mode:
            continue
        voltage_abs = voltage.get(mode, _complex_zero(precision)).upper_abs()
        recovery_abs = recovery.get(mode, _complex_zero(precision)).upper_abs()
        with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
            coefficient_norm = gmpy2.sqrt(
                voltage_abs * voltage_abs + recovery_abs * recovery_abs
            )
        if weight_nu is not None:
            weight = weight_nu ** abs(mode)
            coefficient_norm = upward_product(
                coefficient_norm, weight.upper, precision
            )
        terms.append(coefficient_norm)
    return upward_sum(terms, precision)


def _vector_sequence_l1_lower(
    voltage: Mapping[int, DirectedComplexInterval],
    recovery: Mapping[int, DirectedComplexInterval],
    precision: int,
    *,
    minimum_mode: int = 0,
) -> gmpy2.mpfr:
    """Lower-bound the vector Wiener norm of one enclosed exact sequence."""

    terms: list[gmpy2.mpfr] = []
    for mode in set(voltage) | set(recovery):
        if abs(mode) < minimum_mode:
            continue
        voltage_abs = voltage.get(mode, _complex_zero(precision)).lower_abs()
        recovery_abs = recovery.get(mode, _complex_zero(precision)).lower_abs()
        with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
            terms.append(
                gmpy2.sqrt(
                    voltage_abs * voltage_abs + recovery_abs * recovery_abs
                )
            )
    return downward_sum(terms, precision)


def directed_fourier_residual(
    orbit: PeriodicOrbitCandidate,
    *,
    precision: int = 160,
    weight_nu: str = "1.001",
) -> DirectedFourierResidual:
    """Enclose the full Fourier residual of the interpolating polynomial."""

    count = len(orbit.state)
    half_bandwidth = (count - 1) // 2
    parameters = _interval_parameters(orbit.parameters, precision)
    epsilon = parameters["epsilon"]
    kappa_1 = parameters["kappa_1"]
    kappa_3 = parameters["kappa_3"]
    period = DirectedInterval.from_float(orbit.period, precision)
    voltage = directed_dft(orbit.state[:, 0], precision)
    recovery = directed_dft(orbit.state[:, 1], precision)
    delayed_0 = _sequence_shift(voltage, parameters["tau_0"] / period)
    delayed_1 = _sequence_shift(voltage, parameters["tau_1"] / period)
    one = _constant_sequence(_one(precision), precision)
    unfolding = _constant_sequence(parameters["unfolding"], precision)

    voltage_squared = _sequence_convolution(voltage, voltage)
    voltage_cubed = _sequence_convolution(voltage_squared, voltage)
    current_centered = _sequence_sub(voltage, one)
    delayed_centered_0 = _sequence_sub(delayed_0, one)
    delayed_centered_1 = _sequence_sub(delayed_1, one)
    current_centered_cubed = _sequence_convolution(
        _sequence_convolution(current_centered, current_centered),
        current_centered,
    )
    delayed_centered_cubed_0 = _sequence_convolution(
        _sequence_convolution(delayed_centered_0, delayed_centered_0),
        delayed_centered_0,
    )
    delayed_centered_cubed_1 = _sequence_convolution(
        _sequence_convolution(delayed_centered_1, delayed_centered_1),
        delayed_centered_1,
    )
    linear_difference = _sequence_sub(
        _sequence_scale(_sequence_add(delayed_0, delayed_1), "0.5"),
        voltage,
    )
    cubic_difference = _sequence_sub(
        _sequence_scale(
            _sequence_add(delayed_centered_cubed_0, delayed_centered_cubed_1),
            "0.5",
        ),
        current_centered_cubed,
    )
    one_third = _one(precision) / 3
    fast = _sequence_sub(
        _sequence_sub(voltage, _sequence_scale(voltage_cubed, one_third)),
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
    slow = _sequence_scale(_sequence_sub(voltage, unfolding), epsilon)
    residual_voltage = _sequence_sub(
        _sequence_derivative(voltage, precision),
        _sequence_scale(fast, period),
    )
    residual_recovery = _sequence_sub(
        _sequence_derivative(recovery, precision),
        _sequence_scale(slow, period),
    )

    unweighted = _vector_sequence_l1_upper(
        residual_voltage, residual_recovery, precision
    )
    unweighted_lower = _vector_sequence_l1_lower(
        residual_voltage, residual_recovery, precision
    )
    outside = _vector_sequence_l1_upper(
        residual_voltage,
        residual_recovery,
        precision,
        minimum_mode=half_bandwidth + 1,
    )
    outside_lower = _vector_sequence_l1_lower(
        residual_voltage,
        residual_recovery,
        precision,
        minimum_mode=half_bandwidth + 1,
    )
    nu = DirectedInterval.from_decimal(weight_nu, precision)
    weighted = _vector_sequence_l1_upper(
        residual_voltage,
        residual_recovery,
        precision,
        weight_nu=nu,
    )
    coefficient_norms: list[gmpy2.mpfr] = []
    for mode in set(residual_voltage) | set(residual_recovery):
        voltage_abs = residual_voltage.get(
            mode, _complex_zero(precision)
        ).upper_abs()
        recovery_abs = residual_recovery.get(
            mode, _complex_zero(precision)
        ).upper_abs()
        with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
            coefficient_norms.append(
                gmpy2.sqrt(
                    voltage_abs * voltage_abs + recovery_abs * recovery_abs
                )
            )
    maximum_coefficient = max(coefficient_norms)
    coefficient_lower_norms: list[gmpy2.mpfr] = []
    for mode in set(residual_voltage) | set(residual_recovery):
        voltage_abs = residual_voltage.get(
            mode, _complex_zero(precision)
        ).lower_abs()
        recovery_abs = residual_recovery.get(
            mode, _complex_zero(precision)
        ).lower_abs()
        with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
            coefficient_lower_norms.append(
                gmpy2.sqrt(
                    voltage_abs * voltage_abs + recovery_abs * recovery_abs
                )
            )
    maximum_coefficient_lower = max(coefficient_lower_norms)
    edge_modes = [
        value
        for mode, value in voltage.items()
        if abs(mode) >= max(1, half_bandwidth - 2)
    ] + [
        value
        for mode, value in recovery.items()
        if abs(mode) >= max(1, half_bandwidth - 2)
    ]
    edge_upper = upward_sum(
        [value.upper_abs() for value in edge_modes], precision
    )

    # Wiener norm of the lower-order linearized coefficients at the
    # approximate polynomial. This supplies only a tail-diagonal dominance
    # ingredient, not the coupled finite/tail inverse.
    current_squared = _sequence_convolution(current_centered, current_centered)
    coefficient_current = _sequence_sub(
        _constant_sequence(_one(precision) - epsilon * kappa_1, precision),
        voltage_squared,
    )
    coefficient_current = _sequence_sub(
        coefficient_current,
        _sequence_scale(current_squared, 3 * epsilon * kappa_3),
    )
    coefficient_delayed_0 = _sequence_scale(
        _sequence_add(
            _constant_sequence(kappa_1, precision),
            _sequence_scale(
                _sequence_convolution(delayed_centered_0, delayed_centered_0),
                3 * kappa_3,
            ),
        ),
        epsilon / 2,
    )
    coefficient_delayed_1 = _sequence_scale(
        _sequence_add(
            _constant_sequence(kappa_1, precision),
            _sequence_scale(
                _sequence_convolution(delayed_centered_1, delayed_centered_1),
                3 * kappa_3,
            ),
        ),
        epsilon / 2,
    )
    coefficient_norms = [
        _sequence_wiener_upper(coefficient_current, precision),
        _sequence_wiener_upper(coefficient_delayed_0, precision),
        _sequence_wiener_upper(coefficient_delayed_1, precision),
        _one(precision).upper,
        epsilon.upper,
    ]
    linear_bound = upward_sum(coefficient_norms, precision)
    denominator = (
        pi_interval(precision) * (2 * (half_bandwidth + 1))
    ).lower
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        tail_ratio = period.upper * linear_bound / denominator
    return DirectedFourierResidual(
        node_count=count,
        original_half_bandwidth=half_bandwidth,
        residual_support_half_bandwidth=max(
            max(abs(mode) for mode in residual_voltage),
            max(abs(mode) for mode in residual_recovery),
        ),
        precision_bits=precision,
        unweighted_l1_lower=decimal_lower(unweighted_lower),
        unweighted_l1_upper=decimal_upper(unweighted),
        weighted_l1_nu=weight_nu,
        weighted_l1_upper=decimal_upper(weighted),
        outside_collocation_band_l1_lower=decimal_lower(outside_lower),
        outside_collocation_band_l1_upper=decimal_upper(outside),
        maximum_coefficient_lower=decimal_lower(maximum_coefficient_lower),
        maximum_coefficient_upper=decimal_upper(maximum_coefficient),
        orbit_edge_coefficient_l1_upper=decimal_upper(edge_upper),
        linear_tail_wiener_bound_upper=decimal_upper(linear_bound),
        tail_derivative_neumann_ratio_upper=decimal_upper(tail_ratio),
        tail_derivative_neumann_gate=tail_ratio < 1,
    )


def directed_fhn_validation(
    orbit: PeriodicOrbitCandidate,
    *,
    precision: int = 160,
    weight_nu: str = "1.001",
) -> DirectedFHNValidationResult:
    finite = validate_finite_collocation_candidate(
        orbit, precision=precision
    )
    fourier = directed_fourier_residual(
        orbit, precision=precision, weight_nu=weight_nu
    )
    return DirectedFHNValidationResult(
        parameters=orbit.parameters,
        finite=finite,
        fourier=fourier,
        finite_tail_coupling_bound_supplied=False,
        nonlinear_correction_tail_bound_supplied=False,
        infinite_radii_polynomial_evaluated=False,
        periodic_rfde_orbit_validated=False,
        bordered_rfde_inverse_validated=False,
        missing_infinite_bounds=(
            "dealiased_finite_coefficient_inverse",
            "finite_to_tail_cross_norm",
            "tail_to_finite_cross_norm",
            "phase_period_compatible_tail_inverse",
            "correction_ball_jacobian_variation",
            "quadratic_cubic_correction_tail",
        ),
        falsifier=(
            "The finite nodal radii inequality and directed Fourier residual "
            "do not couple the finite inverse to the correction tail. Supply "
            "finite-tail cross bounds and a nonlinear tail radii estimate "
            "before setting either RFDE validation flag true."
        ),
    )
