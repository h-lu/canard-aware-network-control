"""Stage-4E physical-time shared ``Y_qq`` deflation certificate.

This module is intentionally organized around the expression that has to be
small,

    Y_qq - q * f(Y_qq) / f(q),

rather than around separate absolute bounds for its two large summands.  The
first implementation below builds the source-bound centre calculation used
by the directed proof: a finite exponential--Fourier algebra for the orbit,
the Route-C unstable history and the forcing; a degree-24 method-of-steps
Taylor guide for the physical second variation; and a Neumann reconstruction
of the summable adjoint tail.  The public artifact builder is added only after
the residual and outward-error ingress is complete; no theorem flag is
exported by this computational core alone.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import asdict, dataclass, fields
import cmath
from hashlib import sha256
import json
import math
import os
from pathlib import Path
import platform
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
)
from canard_control.floquet_cover_arithmetic import (
    _binary_coefficients,
    _box_distance_split_upper,
)
from canard_control.leaky_floquet_inner_unstable_root import (
    _dependency_fingerprint,
    _prepare_cached,
)
from canard_control.leaky_inner_stable_projection_stage3 import (
    EIGENCOLUMN_CENTER,
    RESULT_RELATIVE_PATH as STAGE3_RESULT_RELATIVE_PATH,
    _eigencolumn_enclosure,
    validate_stage3_stable_projection_result,
)
from canard_control.leaky_route_c_adjoint_stage4c import (
    _directed_grushin_left_row,
)
from canard_control.leaky_route_c_adjoint_stage4d import (
    RESULT_RELATIVE_PATH as STAGE4D_RESULT_RELATIVE_PATH,
    validate_stage4d_result,
)
from canard_control.leaky_stable_output_uu_stage4b_contract import (
    RESULT_RELATIVE_PATH as STAGE4B_RESULT_RELATIVE_PATH,
    validate_stage4b_contract_result,
)
from canard_control.leaky_pulse_quiet_capture import (
    _current_log_norm_upper,
    _delayed_forcing_upper,
    _gronwall_endpoint,
    _p_box_norm_upper,
    _p_constants,
)
from canard_control.leaky_quiet_history_basin import P11, P12, P22


ExpKey = tuple[int, int]
ExpDict = dict[ExpKey, complex]

TAYLOR_DEGREE = 24
DELAY_GRID_DIVISOR = 512
ADJOINT_NEUMANN_STEPS = 10
TRIM_THRESHOLD = 1.0e-18
VALIDATION_TRIM_THRESHOLD = 1.0e-8
DIRECT_ACTION_DENSITY_TRIM_THRESHOLD = 1.0e-16
PRECISION_BITS = 192
SCALAR_TRANSCRIPTION_GUARD = 1.0e-12

SCHEMA_ID = "leaky-shared-yqq-deflation-stage4e-v1"
MODEL_ID = "autonomous-leaky-recovery-two-delay-fhn-bistable-proposal"
BRANCH = "inner_saddle_candidate"
SOURCE_RELATIVE_PATH = "src/canard_control/leaky_shared_yqq_deflation_stage4e.py"
GENERATOR_RELATIVE_PATH = "experiments/leaky_shared_yqq_deflation_stage4e.py"
RESULT_RELATIVE_PATH = "experiments/results/leaky_shared_yqq_deflation_stage4e.json"
NOTE_RELATIVE_PATH = "docs/leaky-shared-yqq-deflation-stage4e.md"
TEST_RELATIVE_PATH = "tests/test_leaky_shared_yqq_deflation_stage4e.py"
DEFAULT_COMMAND = (
    "OPENBLAS_NUM_THREADS=8 OMP_NUM_THREADS=1 PYTHONPATH=src "
    "/usr/bin/python3 experiments/leaky_shared_yqq_deflation_stage4e.py"
)
ARITHMETIC_SCOPE = (
    "exact source and parent-byte binding; 192-bit outward MPFR interval "
    "Taylor--Bernstein residuals on a physical method-of-steps grid with "
    "both delays aligned; P-logarithmic-norm propagation of one base-orbit "
    "V_qq tube; continuous Route-C atom-plus-density covector pairing; "
    "same-row correlated quotient residual f(Y_qq-cq)/f(q), formed before "
    "the history norm; no mesh-spread error, uniform split-ball Hessian, "
    "other five blocks, stable-power, split-return-tube, graph, or onset proof"
)
SOURCE_MANIFEST = (
    SOURCE_RELATIVE_PATH,
    GENERATOR_RELATIVE_PATH,
    NOTE_RELATIVE_PATH,
)
STAGE3_RESULT_SHA256 = (
    "9ea776a6e627745ded7f7023523999bfbd29a0be4878172c76512d623146e2ea"
)
STAGE4B_RESULT_SHA256 = (
    "a310e4c1dba96961cc6fe7f70e4ee978f3b25a46956f9bcdde9f31286b40f7f7"
)
STAGE4D_RESULT_SHA256 = (
    "af51bcfc20000b804134c1d8b9cacc303013676c440a89f2ecb52faf0042d568"
)

TRUE_FLAGS = (
    "exact_physical_delay_grid_alignment_validated",
    "directed_physical_time_vqq_residual_validated",
    "base_orbit_physical_time_vqq_tube_validated",
    "continuous_history_route_c_covector_pairing_used",
    "shared_yqq_minus_q_action_formed_before_norm",
    "same_adjoint_row_correlated_quotient_residual_validated",
    "base_orbit_stable_output_uu_below_twelve_validated",
)
FALSE_FLAGS = (
    "mesh_spread_is_interval_error",
    "uniform_split_ball_stable_output_uu_below_twelve_validated",
    "other_five_projected_return_hessian_blocks_validated",
    "six_projected_return_hessian_blocks_validated",
    "stable_power_constant_numeric_upper_validated",
    "split_return_tube_validated",
    "stage4b_strict_certificate_closes",
    "inner_local_stable_graph_quantitatively_validated",
    "graph_radius_1p7e_minus_3_validated",
    "physical_pulse_separator_crossing_validated",
    "unique_physical_pulse_onset_validated",
)


def _trim(value: Mapping[ExpKey, complex], threshold: float = TRIM_THRESHOLD) -> ExpDict:
    return {
        key: complex(coefficient)
        for key, coefficient in value.items()
        if abs(coefficient) > threshold
    }


def _add(*values: Mapping[ExpKey, complex]) -> ExpDict:
    result: defaultdict[ExpKey, complex] = defaultdict(complex)
    for value in values:
        for key, coefficient in value.items():
            result[key] += coefficient
    return _trim(result)


def _scale(value: Mapping[ExpKey, complex], scalar: complex) -> ExpDict:
    return _trim({key: scalar * coefficient for key, coefficient in value.items()})


def _multiply(left: Mapping[ExpKey, complex], right: Mapping[ExpKey, complex]) -> ExpDict:
    result: defaultdict[ExpKey, complex] = defaultdict(complex)
    for (left_growth, left_mode), left_value in left.items():
        for (right_growth, right_mode), right_value in right.items():
            result[(left_growth + right_growth, left_mode + right_mode)] += (
                left_value * right_value
            )
    return _trim(result)


def _constant(value: complex) -> ExpDict:
    return {} if value == 0 else {(0, 0): complex(value)}


def _delay(value: Mapping[ExpKey, complex], delay: float, period: float, root: float) -> ExpDict:
    return _trim(
        {
            (growth, mode): coefficient
            * cmath.exp(-(growth * root + 2.0j * math.pi * mode) * delay / period)
            for (growth, mode), coefficient in value.items()
        }
    )


def _derivative(value: Mapping[ExpKey, complex], period: float, root: float) -> ExpDict:
    return _trim(
        {
            (growth, mode): coefficient
            * (growth * root + 2.0j * math.pi * mode)
            / period
            for (growth, mode), coefficient in value.items()
        }
    )


def _period_shift(value: Mapping[ExpKey, complex], root: float) -> ExpDict:
    return _trim(
        {
            (growth, mode): coefficient * math.exp(growth * root)
            for (growth, mode), coefficient in value.items()
        }
    )


def _evaluate(value: Mapping[ExpKey, complex], time: float, period: float, root: float) -> complex:
    return sum(
        (
            coefficient
            * cmath.exp((growth * root + 2.0j * math.pi * mode) * time / period)
            for (growth, mode), coefficient in value.items()
        ),
        0.0j,
    )


def _taylor(
    value: Mapping[ExpKey, complex],
    left: float,
    step: float,
    period: float,
    root: float,
    degree: int = TAYLOR_DEGREE,
) -> np.ndarray:
    result = np.zeros(degree + 1, dtype=complex)
    for (growth, mode), coefficient in value.items():
        frequency = (growth * root + 2.0j * math.pi * mode) / period
        term = coefficient * cmath.exp(frequency * left)
        result[0] += term
        scaled = frequency * step
        for order in range(1, degree + 1):
            term *= scaled / order
            result[order] += term
    return result


def _taylor_tail_upper(
    value: Mapping[ExpKey, complex],
    step: float,
    period: float,
    root: float,
    degree: int = TAYLOR_DEGREE,
) -> float:
    total = 0.0
    factorial = math.factorial(degree + 1)
    for (growth, mode), coefficient in value.items():
        scaled = abs((growth * root + 2.0j * math.pi * mode) * step / period)
        total += abs(coefficient) * math.exp(max(growth * root * step / period, 0.0)) * (
            math.exp(scaled) * scaled ** (degree + 1) / factorial
        )
    return total


def _real_point(value: float | gmpy2.mpfr | int, precision: int = PRECISION_BITS) -> DirectedInterval:
    if isinstance(value, float):
        return DirectedInterval.from_float(value, precision)
    return DirectedInterval.from_bounds(value, value, precision)


def _complex_point(value: complex, precision: int = PRECISION_BITS) -> DirectedComplexInterval:
    return DirectedComplexInterval(
        DirectedInterval.from_float(float(value.real), precision),
        DirectedInterval.from_float(float(value.imag), precision),
    )


def _exp_real(value: DirectedInterval) -> DirectedInterval:
    with gmpy2.context(precision=value.precision, round=gmpy2.RoundDown):
        lower = gmpy2.exp(value.lower)
    with gmpy2.context(precision=value.precision, round=gmpy2.RoundUp):
        upper = gmpy2.exp(value.upper)
    return DirectedInterval(lower, upper, value.precision)


def _directed_taylor(
    value: Mapping[ExpKey, complex],
    left: DirectedInterval,
    step: DirectedInterval,
    period: DirectedInterval,
    root: DirectedInterval,
    degree: int = TAYLOR_DEGREE,
) -> tuple[DirectedComplexInterval, ...]:
    precision = left.precision
    result = [DirectedComplexInterval.zero(precision) for _ in range(degree + 1)]
    for (growth, mode), coefficient in value.items():
        real_frequency = root * growth / period
        imaginary_frequency = pi_interval(precision) * (2 * mode) / period
        amplitude = _exp_real(real_frequency * left)
        phase = imaginary_frequency * left
        term = _complex_point(coefficient, precision) * (
            DirectedComplexInterval.from_real(amplitude) * complex_unit_interval(phase)
        )
        result[0] = result[0] + term
        scaled = DirectedComplexInterval(real_frequency * step, imaginary_frequency * step)
        for order in range(1, degree + 1):
            term = term * scaled * (_real_point(1, precision) / order)
            result[order] = result[order] + term
    return tuple(result)


def _directed_taylor_tail_upper(
    value: Mapping[ExpKey, complex],
    step: DirectedInterval,
    period: DirectedInterval,
    root: DirectedInterval,
    degree: int = TAYLOR_DEGREE,
) -> gmpy2.mpfr:
    precision = step.precision
    total = gmpy2.mpfr(0, precision)
    factorial = math.factorial(degree + 1)
    for (growth, mode), coefficient in value.items():
        real = root * growth / period
        imaginary = pi_interval(precision) * (2 * mode) / period
        frequency = DirectedComplexInterval(real, imaginary)
        with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
            scaled = frequency.upper_abs() * step.upper
            amplitude = gmpy2.exp(max(gmpy2.mpfr(0), real.upper * step.upper))
            remainder = (
                _complex_point(coefficient, precision).upper_abs()
                * amplitude
                * gmpy2.exp(scaled)
                * scaled ** (degree + 1)
                / factorial
            )
            total += remainder
    return total


def _complex_poly_add(
    left: Iterable[DirectedComplexInterval],
    right: Iterable[DirectedComplexInterval],
) -> tuple[DirectedComplexInterval, ...]:
    left_values = tuple(left)
    right_values = tuple(right)
    precision = (left_values or right_values)[0].precision
    zero = DirectedComplexInterval.zero(precision)
    return tuple(
        (left_values[index] if index < len(left_values) else zero)
        + (right_values[index] if index < len(right_values) else zero)
        for index in range(max(len(left_values), len(right_values)))
    )


def _complex_poly_neg(
    value: Iterable[DirectedComplexInterval],
) -> tuple[DirectedComplexInterval, ...]:
    return tuple(-item for item in value)


def _complex_poly_sub(
    left: Iterable[DirectedComplexInterval],
    right: Iterable[DirectedComplexInterval],
) -> tuple[DirectedComplexInterval, ...]:
    return _complex_poly_add(left, _complex_poly_neg(right))


def _complex_poly_multiply(
    left: Iterable[DirectedComplexInterval],
    right: Iterable[DirectedComplexInterval],
) -> tuple[DirectedComplexInterval, ...]:
    left_values = tuple(left)
    right_values = tuple(right)
    precision = left_values[0].precision
    result = [
        DirectedComplexInterval.zero(precision)
        for _ in range(len(left_values) + len(right_values) - 1)
    ]
    for left_index, left_value in enumerate(left_values):
        for right_index, right_value in enumerate(right_values):
            result[left_index + right_index] = (
                result[left_index + right_index] + left_value * right_value
            )
    return tuple(result)


def _complex_poly_derivative(
    value: Iterable[DirectedComplexInterval], step: DirectedInterval
) -> tuple[DirectedComplexInterval, ...]:
    values = tuple(value)
    return tuple(values[index] * index * (1 / step) for index in range(1, len(values)))


def _complex_poly_bernstein_upper(
    value: Iterable[DirectedComplexInterval],
) -> gmpy2.mpfr:
    values = tuple(value)
    precision = values[0].precision
    degree = len(values) - 1
    maximum = gmpy2.mpfr(0, precision)
    for index in range(degree + 1):
        coefficient = DirectedComplexInterval.zero(precision)
        for power in range(index + 1):
            weight = _real_point(math.comb(index, power), precision) / math.comb(
                degree, power
            )
            coefficient = coefficient + values[power] * weight
        maximum = max(maximum, coefficient.upper_abs())
    return maximum


def _real_part_bernstein_range(
    value: Iterable[DirectedComplexInterval],
) -> DirectedInterval:
    values = tuple(value)
    precision = values[0].precision
    degree = len(values) - 1
    coefficients: list[DirectedInterval] = []
    for index in range(degree + 1):
        coefficient = _real_point(0, precision)
        for power in range(index + 1):
            weight = _real_point(math.comb(index, power), precision) / math.comb(
                degree, power
            )
            coefficient = coefficient + values[power].real * weight
        coefficients.append(coefficient)
    return DirectedInterval.from_bounds(
        min(item.lower for item in coefficients),
        max(item.upper for item in coefficients),
        precision,
    )


def _enlarge_real(value: DirectedInterval, radius: gmpy2.mpfr) -> DirectedInterval:
    with gmpy2.context(precision=value.precision, round=gmpy2.RoundDown):
        lower = value.lower - radius
    with gmpy2.context(precision=value.precision, round=gmpy2.RoundUp):
        upper = value.upper + radius
    return DirectedInterval(lower, upper, value.precision)


def _convolve(left: np.ndarray, right: np.ndarray) -> np.ndarray:
    return np.convolve(left, right)


def _poly_translate_scale(value: np.ndarray, ratio: float) -> np.ndarray:
    powers = ratio ** np.arange(len(value), dtype=float)
    return value * powers


@dataclass(frozen=True)
class _CentreData:
    repository: Path
    prepared: object
    period: float
    root: float
    epsilon: float
    tau0: float
    tau1: float
    orbit_v: ExpDict
    orbit_w: ExpDict
    xdot_v: ExpDict
    xdot_w: ExpDict
    xddot_v: ExpDict
    xddot_w: ExpDict
    qraw_v: ExpDict
    qraw_w: ExpDict
    qsection_v: ExpDict
    qsection_w: ExpDict
    u_v: ExpDict
    u_w: ExpDict
    udot_v: ExpDict
    udot_w: ExpDict
    current: ExpDict
    delayed0: ExpDict
    delayed1: ExpDict
    forcing: ExpDict
    section_scalar: complex
    right_coefficients: np.ndarray
    right_error: float
    left_finite: np.ndarray
    left_row_dual_error: float


def _dictionary_l1_upper(
    value: Mapping[ExpKey, complex],
    root: float,
    positive_phase: float = 1.0,
) -> float:
    return sum(
        abs(coefficient) * math.exp(max(growth * root * positive_phase, 0.0))
        for (growth, _), coefficient in value.items()
    )


def _dictionary_l1_directed_upper(
    value: Mapping[ExpKey, complex],
    root: float,
    positive_phase: float = 1.0,
    precision: int = PRECISION_BITS,
) -> gmpy2.mpfr:
    """Outward Wiener bound for one stored exponential--Fourier dictionary."""

    root_interval = DirectedInterval.from_float(root, precision)
    phase_interval = DirectedInterval.from_float(positive_phase, precision)
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        total = gmpy2.mpfr(0, precision)
        for (growth, _), coefficient in value.items():
            amplitude = gmpy2.mpfr(1, precision)
            if growth > 0 and positive_phase > 0:
                amplitude = _exp_real(
                    root_interval * growth * phase_interval
                ).upper
            total += _complex_point(coefficient, precision).upper_abs() * amplitude
    return total


def _adjoint_component_l2_upper(
    finite: Iterable[complex],
    tail: Mapping[int, complex],
    precision: int = PRECISION_BITS,
) -> gmpy2.mpfr:
    """Parseval upper bound for a binary centre adjoint component.

    The finite and Neumann-tail coefficients are stored binary64 numbers.
    Their conversion to MPFR is exact; only the modulus, squares, sum and
    square root need outward rounding.
    """

    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        square_sum = gmpy2.mpfr(0, precision)
        for coefficient in tuple(finite) + tuple(tail.values()):
            modulus = _complex_point(complex(coefficient), precision).upper_abs()
            square_sum += modulus * modulus
        return gmpy2.sqrt(square_sum)


def _validation_trim(
    value: Mapping[ExpKey, complex],
    root: float,
    precision: int = PRECISION_BITS,
) -> tuple[ExpDict, gmpy2.mpfr]:
    retained: ExpDict = {}
    omitted = gmpy2.mpfr(0, precision)
    for key, coefficient in value.items():
        if abs(coefficient) >= VALIDATION_TRIM_THRESHOLD:
            retained[key] = coefficient
            continue
        growth, _ = key
        with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
            amplitude = gmpy2.exp(max(gmpy2.mpfr(0), growth * gmpy2.mpfr(root)))
            omitted += _complex_point(coefficient, precision).upper_abs() * amplitude
    return retained, omitted


def _model_uncertainty(data: _CentreData) -> dict[str, float]:
    """Conservative sup-error transfer from the validated orbit and q column.

    The ``binary_algebra_guard`` is not a mesh error.  It is an IEEE operation
    count guard for every rounded convolution used to form the finite centre
    dictionaries; the retained-dictionary operation count is below 4e6 and
    every intermediate l1 norm is below 10, so ``1e-8`` dominates the usual
    gamma bound by more than two orders of magnitude.
    """

    binary_algebra_guard = 1.0e-8
    orbit_v_error = 0.0
    orbit_w_error = 0.0
    for component, center, destination in (
        (data.prepared.base.voltage, data.orbit_v, "voltage"),
        (data.prepared.base.recovery, data.orbit_w, "recovery"),
    ):
        total = 0.0
        for mode, interval in component.items():
            total += float(
                _box_distance_split_upper(
                    interval, center.get((0, int(mode)), 0.0j)
                )
            )
        if destination == "voltage":
            orbit_v_error = total
        else:
            orbit_w_error = total
    orbit_error = max(orbit_v_error, orbit_w_error) + float(
        data.prepared.period_radius
    )
    period_error = float(data.prepared.period_radius)
    root_error = 1.1e-8
    right_l1 = float(np.sum(np.abs(data.right_coefficients)))
    maximum_time = max(data.tau1, data.period)
    period_lower = data.period - period_error
    phase = maximum_time / period_lower
    exponent_error = (
        phase * root_error
        + abs(data.root) * maximum_time * period_error / period_lower**2
    )
    qraw_error = math.exp(data.root + exponent_error) * (
        data.right_error + right_l1 * math.expm1(exponent_error)
    )
    voltage_bound = _dictionary_l1_upper(data.orbit_v, data.root) + orbit_error
    current_linear_bound = (
        1
        + voltage_bound**2
        + data.epsilon
        * (
            float(data.prepared.orbit.parameters.kappa_1)
            + 3
            * float(data.prepared.orbit.parameters.kappa_3)
            * (voltage_bound + 1) ** 2
        )
    )
    delayed_sum_bound = data.epsilon * (
        float(data.prepared.orbit.parameters.kappa_1)
        + 3
        * float(data.prepared.orbit.parameters.kappa_3)
        * (voltage_bound + 1) ** 2
    )
    xdot_error = max(
        (current_linear_bound + 1 + delayed_sum_bound) * orbit_error,
        2 * data.epsilon * orbit_error,
    ) + binary_algebra_guard
    xdot_bound = max(
        _dictionary_l1_upper(data.xdot_v, data.root),
        _dictionary_l1_upper(data.xdot_w, data.root),
    )
    qv0_bound = abs(_evaluate(data.qraw_v, 0, data.period, data.root))
    event_speed_lower = 0.24695922696978402
    section_scalar_error = (
        qraw_error / event_speed_lower
        + qv0_bound * xdot_error / event_speed_lower**2
    )
    qsection_error = (
        qraw_error
        + abs(data.section_scalar) * xdot_error
        + xdot_bound * section_scalar_error
        + binary_algebra_guard
    )
    u_error = qsection_error
    u_bound = max(
        _dictionary_l1_upper(data.u_v, data.root),
        _dictionary_l1_upper(data.u_w, data.root),
    )
    kappa3 = float(data.prepared.orbit.parameters.kappa_3)
    current_error = (
        2 * voltage_bound + 6 * data.epsilon * kappa3 * (voltage_bound + 1)
    ) * orbit_error + binary_algebra_guard
    delayed_each_error = (
        3 * data.epsilon * kappa3 * (voltage_bound + 1) * orbit_error
        + binary_algebra_guard
    )
    udot_error = (
        (current_linear_bound + 1 + delayed_sum_bound) * u_error
        + (current_error + 2 * delayed_each_error) * u_bound
        + binary_algebra_guard
    )
    xddot_error = (
        (current_linear_bound + 1 + delayed_sum_bound) * xdot_error
        + (current_error + 2 * delayed_each_error) * xdot_bound
        + binary_algebra_guard
    )
    h_current_bound = (2 + 6 * data.epsilon * kappa3) * voltage_bound + 6 * data.epsilon * kappa3
    h_delayed_bound = 3 * data.epsilon * kappa3 * (voltage_bound + 1)
    h_current_error = (2 + 6 * data.epsilon * kappa3) * orbit_error + binary_algebra_guard
    h_delayed_error = 3 * data.epsilon * kappa3 * orbit_error + binary_algebra_guard
    square_error = 2 * u_bound * u_error + u_error**2
    forcing_error = (
        h_current_error * (u_bound + u_error) ** 2
        + h_current_bound * square_error
        + 2
        * (
            h_delayed_error * (u_bound + u_error) ** 2
            + h_delayed_bound * square_error
        )
        + binary_algebra_guard
    )
    return {
        "binary_algebra_guard": binary_algebra_guard,
        # Each following binary64 scalar is an analytic upper (or the final
        # lower) transcribed from a short expression.  The explicit guard is
        # much larger than the accumulated rounding of those scalar formulas
        # and is present before any value enters MPFR propagation.
        "orbit_error": orbit_error + SCALAR_TRANSCRIPTION_GUARD,
        "period_error": period_error + SCALAR_TRANSCRIPTION_GUARD,
        "root_error": root_error + SCALAR_TRANSCRIPTION_GUARD,
        "qraw_error": qraw_error + SCALAR_TRANSCRIPTION_GUARD,
        "xdot_error": xdot_error + SCALAR_TRANSCRIPTION_GUARD,
        "section_scalar_error": section_scalar_error + SCALAR_TRANSCRIPTION_GUARD,
        "qsection_error": qsection_error + SCALAR_TRANSCRIPTION_GUARD,
        "u_error": u_error + SCALAR_TRANSCRIPTION_GUARD,
        "udot_error": udot_error + SCALAR_TRANSCRIPTION_GUARD,
        "xddot_error": xddot_error + SCALAR_TRANSCRIPTION_GUARD,
        "current_coefficient_error": current_error + SCALAR_TRANSCRIPTION_GUARD,
        "delayed_coefficient_each_error": delayed_each_error + SCALAR_TRANSCRIPTION_GUARD,
        "forcing_error": forcing_error + SCALAR_TRANSCRIPTION_GUARD,
        "voltage_bound": voltage_bound + SCALAR_TRANSCRIPTION_GUARD,
        "xdot_bound": xdot_bound + SCALAR_TRANSCRIPTION_GUARD,
        "u_bound": u_bound + SCALAR_TRANSCRIPTION_GUARD,
        "event_speed_lower": event_speed_lower - SCALAR_TRANSCRIPTION_GUARD,
    }


def _orbit_dictionary(samples: np.ndarray, component: int) -> ExpDict:
    count = len(samples)
    coefficients = np.fft.fft(np.asarray(samples[:, component], dtype=float)) / count
    modes = np.rint(np.fft.fftfreq(count, d=1.0 / count)).astype(int)
    return _trim({(0, int(mode)): complex(coefficient) for mode, coefficient in zip(modes, coefficients, strict=True)}, 0.0)


def _centre_data(repository: Path) -> _CentreData:
    repository = repository.resolve()
    prepared, _ = _prepare_cached(
        str(repository), _dependency_fingerprint(repository)
    )
    _, right, right_error, _ = _eigencolumn_enclosure(prepared)
    grushin = _directed_grushin_left_row(repository)
    left = np.asarray(
        [
            complex(float(item["real_binary64"]), float(item["imag_binary64"]))
            for item in grushin["finite_row_coefficients"]
        ],
        dtype=complex,
    )
    period = float(prepared.orbit.period)
    root = float(EIGENCOLUMN_CENTER)
    epsilon = float(prepared.orbit.parameters.epsilon)
    tau0, tau1 = (float(value) for value in prepared.orbit.parameters.physical_delays)
    orbit_v = _orbit_dictionary(prepared.orbit.state, 0)
    orbit_w = _orbit_dictionary(prepared.orbit.state, 1)
    one = _constant(1)
    half = 0.5
    kappa1 = float(prepared.orbit.parameters.kappa_1)
    kappa3 = float(prepared.orbit.parameters.kappa_3)
    unfolding = float(prepared.orbit.parameters.unfolding)
    delayed_v0 = _delay(orbit_v, tau0, period, root)
    delayed_v1 = _delay(orbit_v, tau1, period, root)
    v_minus_one = _add(orbit_v, _constant(-1))
    delayed_minus_one0 = _add(delayed_v0, _constant(-1))
    delayed_minus_one1 = _add(delayed_v1, _constant(-1))
    fast = _add(
        orbit_v,
        _scale(_multiply(_multiply(orbit_v, orbit_v), orbit_v), -1.0 / 3.0),
        _scale(orbit_w, -1),
        _scale(_add(_scale(_add(delayed_v0, delayed_v1), half), _scale(orbit_v, -1)), epsilon * kappa1),
        _scale(
            _add(
                _scale(
                    _add(
                        _multiply(_multiply(delayed_minus_one0, delayed_minus_one0), delayed_minus_one0),
                        _multiply(_multiply(delayed_minus_one1, delayed_minus_one1), delayed_minus_one1),
                    ),
                    half,
                ),
                _scale(_multiply(_multiply(v_minus_one, v_minus_one), v_minus_one), -1),
            ),
            epsilon * kappa3,
        ),
    )
    slow = _scale(_add(orbit_v, _scale(orbit_w, -1), _constant(-unfolding)), epsilon)
    xdot_v, xdot_w = fast, slow

    current = _add(
        one,
        _scale(_multiply(orbit_v, orbit_v), -1),
        _scale(one, -epsilon * kappa1),
        _scale(_multiply(v_minus_one, v_minus_one), -3 * epsilon * kappa3),
    )
    delayed0 = _scale(
        _add(_constant(kappa1), _scale(_multiply(delayed_minus_one0, delayed_minus_one0), 3 * kappa3)),
        epsilon / 2,
    )
    delayed1 = _scale(
        _add(_constant(kappa1), _scale(_multiply(delayed_minus_one1, delayed_minus_one1), 3 * kappa3)),
        epsilon / 2,
    )

    def linear_apply(voltage: ExpDict, recovery: ExpDict) -> tuple[ExpDict, ExpDict]:
        return (
            _add(
                _multiply(current, voltage),
                _scale(recovery, -1),
                _multiply(delayed0, _delay(voltage, tau0, period, root)),
                _multiply(delayed1, _delay(voltage, tau1, period, root)),
            ),
            _scale(_add(voltage, _scale(recovery, -1)), epsilon),
        )

    xddot_v, xddot_w = linear_apply(xdot_v, xdot_w)
    mode_count = len(prepared.modes)
    qraw_v = _trim({(1, int(mode)): complex(coefficient) for mode, coefficient in zip(prepared.modes, right[:mode_count], strict=True)}, 0.0)
    qraw_w = _trim({(1, int(mode)): complex(coefficient) for mode, coefficient in zip(prepared.modes, right[mode_count:], strict=True)}, 0.0)
    qv0 = _evaluate(qraw_v, 0.0, period, root)
    xdotv0 = _evaluate(xdot_v, 0.0, period, root)
    section_scalar = qv0 / xdotv0
    qsection_v = _add(qraw_v, _scale(xdot_v, -section_scalar))
    qsection_w = _add(qraw_w, _scale(xdot_w, -section_scalar))
    u_v, u_w = qsection_v, qsection_w
    udot_v, udot_w = linear_apply(u_v, u_w)
    h_current = _add(_scale(orbit_v, -(2 + 6 * epsilon * kappa3)), _constant(6 * epsilon * kappa3))
    h_delayed0 = _scale(delayed_minus_one0, 3 * epsilon * kappa3)
    h_delayed1 = _scale(delayed_minus_one1, 3 * epsilon * kappa3)
    forcing = _add(
        _multiply(h_current, _multiply(u_v, u_v)),
        _multiply(h_delayed0, _multiply(_delay(u_v, tau0, period, root), _delay(u_v, tau0, period, root))),
        _multiply(h_delayed1, _multiply(_delay(u_v, tau1, period, root), _delay(u_v, tau1, period, root))),
    )
    return _CentreData(
        repository=repository,
        prepared=prepared,
        period=period,
        root=root,
        epsilon=epsilon,
        tau0=tau0,
        tau1=tau1,
        orbit_v=orbit_v,
        orbit_w=orbit_w,
        xdot_v=xdot_v,
        xdot_w=xdot_w,
        xddot_v=xddot_v,
        xddot_w=xddot_w,
        qraw_v=qraw_v,
        qraw_w=qraw_w,
        qsection_v=qsection_v,
        qsection_w=qsection_w,
        u_v=u_v,
        u_w=u_w,
        udot_v=udot_v,
        udot_w=udot_w,
        current=current,
        delayed0=delayed0,
        delayed1=delayed1,
        forcing=forcing,
        section_scalar=section_scalar,
        right_coefficients=right,
        right_error=float(right_error),
        left_finite=left,
        left_row_dual_error=float(
            grushin["exact_bottom_row_distance_dual_upper"]
        ),
    )


@dataclass(frozen=True)
class _GuideCell:
    left: float
    right: float
    voltage: np.ndarray
    recovery: np.ndarray
    residual_l1: float
    analytic_tail_upper: float


def _point_polynomial(
    value: np.ndarray, precision: int = PRECISION_BITS
) -> tuple[DirectedComplexInterval, ...]:
    return tuple(_complex_point(complex(coefficient), precision) for coefficient in value)


def _pad_complex_poly(
    value: Iterable[DirectedComplexInterval], length: int
) -> tuple[DirectedComplexInterval, ...]:
    values = tuple(value)
    zero = DirectedComplexInterval.zero(values[0].precision)
    return values + tuple(zero for _ in range(length - len(values)))


def _source_polynomial_directed(
    cells: tuple[_GuideCell, ...],
    index: int,
    delay_cells: int,
    local_step: DirectedInterval,
    regular_step: DirectedInterval,
) -> tuple[DirectedComplexInterval, ...]:
    if index < delay_cells:
        return tuple(
            DirectedComplexInterval.zero(local_step.precision)
            for _ in range(TAYLOR_DEGREE + 1)
        )
    source = _point_polynomial(cells[index - delay_cells].voltage)
    if local_step.lower == regular_step.lower and local_step.upper == regular_step.upper:
        return source
    ratio = local_step / regular_step
    result: list[DirectedComplexInterval] = []
    power = _real_point(1, local_step.precision)
    for coefficient in source:
        result.append(coefficient * power)
        power = power * ratio
    return tuple(result)


def _directed_residual_rows(
    data: _CentreData,
    cells: tuple[_GuideCell, ...],
    maximum_cells: int | None = None,
) -> tuple[dict[str, gmpy2.mpfr | int], ...]:
    """Recompute the guide residual with 192-bit outward arithmetic."""

    precision = PRECISION_BITS
    period = DirectedInterval.from_float(data.period, precision)
    root = DirectedInterval.from_float(data.root, precision)
    regular_step = DirectedInterval.from_float(data.tau0, precision) / DELAY_GRID_DIVISOR
    current_dictionary, current_omitted = _validation_trim(
        data.current, data.root, precision
    )
    delayed0_dictionary, delayed0_omitted = _validation_trim(
        data.delayed0, data.root, precision
    )
    delayed1_dictionary, delayed1_omitted = _validation_trim(
        data.delayed1, data.root, precision
    )
    forcing_dictionary, forcing_omitted = _validation_trim(
        data.forcing, data.root, precision
    )
    rows: list[dict[str, gmpy2.mpfr | int]] = []
    count = len(cells) if maximum_cells is None else min(len(cells), maximum_cells)
    for index, cell in enumerate(cells[:count]):
        if index < len(cells) - 1:
            left = regular_step * index
            step = regular_step
        else:
            left = regular_step * index
            step = period - left
        current = _directed_taylor(current_dictionary, left, step, period, root)
        delayed0 = _directed_taylor(delayed0_dictionary, left, step, period, root)
        delayed1 = _directed_taylor(delayed1_dictionary, left, step, period, root)
        forcing = _directed_taylor(forcing_dictionary, left, step, period, root)
        voltage = _point_polynomial(cell.voltage)
        recovery = _point_polynomial(cell.recovery)
        source0 = _source_polynomial_directed(
            cells, index, 512, step, regular_step
        )
        source1 = _source_polynomial_directed(
            cells, index, 640, step, regular_step
        )
        length = 2 * TAYLOR_DEGREE + 1
        derivative_v = _pad_complex_poly(
            _complex_poly_derivative(voltage, step), length
        )
        derivative_w = _pad_complex_poly(
            _complex_poly_derivative(recovery, step), length
        )
        residual_v = _complex_poly_sub(
            derivative_v,
            _pad_complex_poly(_complex_poly_multiply(current, voltage), length),
        )
        residual_v = _complex_poly_add(
            residual_v, _pad_complex_poly(recovery, length)
        )
        residual_v = _complex_poly_sub(
            residual_v,
            _pad_complex_poly(_complex_poly_multiply(delayed0, source0), length),
        )
        residual_v = _complex_poly_sub(
            residual_v,
            _pad_complex_poly(_complex_poly_multiply(delayed1, source1), length),
        )
        residual_v = _complex_poly_sub(
            residual_v, _pad_complex_poly(forcing, length)
        )
        residual_w = _complex_poly_sub(
            derivative_w,
            _pad_complex_poly(
                tuple((voltage[order] - recovery[order]) * data.epsilon for order in range(len(voltage))),
                length,
            ),
        )
        polynomial_v = _complex_poly_bernstein_upper(residual_v)
        polynomial_w = _complex_poly_bernstein_upper(residual_w)
        voltage_upper = _complex_poly_bernstein_upper(voltage)
        source0_upper = _complex_poly_bernstein_upper(source0)
        source1_upper = _complex_poly_bernstein_upper(source1)
        with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
            analytic_tail = (
                (_directed_taylor_tail_upper(current_dictionary, step, period, root) + current_omitted)
                * voltage_upper
                + (_directed_taylor_tail_upper(delayed0_dictionary, step, period, root) + delayed0_omitted)
                * source0_upper
                + (_directed_taylor_tail_upper(delayed1_dictionary, step, period, root) + delayed1_omitted)
                * source1_upper
                + _directed_taylor_tail_upper(forcing_dictionary, step, period, root)
                + forcing_omitted
            )
            voltage_residual = polynomial_v + analytic_tail
        rows.append(
            {
                "cell_index": index,
                "voltage_residual_upper": voltage_residual,
                "recovery_residual_upper": polynomial_w,
                "polynomial_voltage_residual_upper": polynomial_v,
                "analytic_tail_upper": analytic_tail,
                "voltage_guide_upper": voltage_upper,
                "delayed0_guide_upper": source0_upper,
                "delayed1_guide_upper": source1_upper,
            }
        )
    return tuple(rows)


def _directed_vqq_tube(
    data: _CentreData,
    cells: tuple[_GuideCell, ...],
    residual_rows: tuple[dict[str, gmpy2.mpfr | int], ...],
    uncertainty: Mapping[str, float],
) -> tuple[dict[str, gmpy2.mpfr | int], ...]:
    """Propagate the continuous-time P-norm error of the V_qq guide."""

    if len(residual_rows) != len(cells):
        raise ValueError("the V_qq tube requires every residual cell")
    precision = PRECISION_BITS
    period = DirectedInterval.from_float(data.period, precision)
    root = DirectedInterval.from_float(data.root, precision)
    regular_step = DirectedInterval.from_float(data.tau0, precision) / DELAY_GRID_DIVISOR
    orbit_error = gmpy2.mpfr(uncertainty["orbit_error"], precision)
    current_error = gmpy2.mpfr(
        uncertainty["current_coefficient_error"], precision
    )
    delayed_error = gmpy2.mpfr(
        uncertainty["delayed_coefficient_each_error"], precision
    )
    forcing_error = gmpy2.mpfr(uncertainty["forcing_error"], precision)
    orbit_dictionary, orbit_omitted = _validation_trim(
        data.orbit_v, data.root, precision
    )
    delayed_orbit0_full = _delay(data.orbit_v, data.tau0, data.period, data.root)
    delayed_orbit1_full = _delay(data.orbit_v, data.tau1, data.period, data.root)
    delayed_orbit0, delayed0_omitted = _validation_trim(
        delayed_orbit0_full, data.root, precision
    )
    delayed_orbit1, delayed1_omitted = _validation_trim(
        delayed_orbit1_full, data.root, precision
    )
    rows: list[dict[str, gmpy2.mpfr | int]] = []
    previous_endpoint = gmpy2.mpfr(0, precision)
    previous_voltage: tuple[DirectedComplexInterval, ...] | None = None
    previous_recovery: tuple[DirectedComplexInterval, ...] | None = None
    for index, (cell, residual) in enumerate(zip(cells, residual_rows, strict=True)):
        if index < len(cells) - 1:
            left = regular_step * index
            step = regular_step
        else:
            left = regular_step * index
            step = period - left
        voltage = _point_polynomial(cell.voltage)
        recovery = _point_polynomial(cell.recovery)
        if index == 0:
            jump = gmpy2.mpfr(0, precision)
            start_radius = gmpy2.mpfr(0, precision)
        else:
            assert previous_voltage is not None and previous_recovery is not None
            endpoint_v = DirectedComplexInterval.zero(precision)
            endpoint_w = DirectedComplexInterval.zero(precision)
            for coefficient in previous_voltage:
                endpoint_v = endpoint_v + coefficient
            for coefficient in previous_recovery:
                endpoint_w = endpoint_w + coefficient
            jump_v = (endpoint_v - voltage[0]).upper_abs()
            jump_w = (endpoint_w - recovery[0]).upper_abs()
            jump = _p_box_norm_upper(jump_v, jump_w, precision)
            with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
                start_radius = previous_endpoint + jump
        source0_radius = (
            gmpy2.mpfr(0, precision)
            if index < 512
            else rows[index - 512]["maximum_radius"]
        )
        source1_radius = (
            gmpy2.mpfr(0, precision)
            if index < 640
            else rows[index - 640]["maximum_radius"]
        )
        assert isinstance(source0_radius, gmpy2.mpfr)
        assert isinstance(source1_radius, gmpy2.mpfr)
        orbit_polynomial = _directed_taylor(
            orbit_dictionary, left, step, period, root
        )
        orbit_range = _real_part_bernstein_range(orbit_polynomial)
        orbit_tail = _directed_taylor_tail_upper(
            orbit_dictionary, step, period, root
        )
        with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
            exact_orbit_radius = orbit_error + orbit_tail + orbit_omitted
        exact_orbit_range = _enlarge_real(orbit_range, exact_orbit_radius)
        log_norm = _current_log_norm_upper(exact_orbit_range, precision)

        delayed_ranges: list[DirectedInterval] = []
        for delayed_dictionary, omitted in (
            (delayed_orbit0, delayed0_omitted),
            (delayed_orbit1, delayed1_omitted),
        ):
            delayed_polynomial = _directed_taylor(
                delayed_dictionary, left, step, period, root
            )
            delayed_range = _real_part_bernstein_range(delayed_polynomial)
            delayed_tail = _directed_taylor_tail_upper(
                delayed_dictionary, step, period, root
            )
            with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
                delayed_radius = orbit_error + delayed_tail + omitted
            delayed_ranges.append(_enlarge_real(delayed_range, delayed_radius))
        delay_gain0 = _delayed_forcing_upper(delayed_ranges[0], precision)
        delay_gain1 = _delayed_forcing_upper(delayed_ranges[1], precision)
        voltage_residual = residual["voltage_residual_upper"]
        recovery_residual = residual["recovery_residual_upper"]
        voltage_guide = residual["voltage_guide_upper"]
        delayed0_guide = residual["delayed0_guide_upper"]
        delayed1_guide = residual["delayed1_guide_upper"]
        assert isinstance(voltage_residual, gmpy2.mpfr)
        assert isinstance(recovery_residual, gmpy2.mpfr)
        assert isinstance(voltage_guide, gmpy2.mpfr)
        assert isinstance(delayed0_guide, gmpy2.mpfr)
        assert isinstance(delayed1_guide, gmpy2.mpfr)
        with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
            model_voltage_residual = (
                current_error * voltage_guide
                + delayed_error * (delayed0_guide + delayed1_guide)
                + forcing_error
            )
            total_voltage_residual = voltage_residual + model_voltage_residual
        local_residual = _p_box_norm_upper(
            total_voltage_residual, recovery_residual, precision
        )
        with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
            total_forcing = (
                local_residual
                + delay_gain0 * source0_radius
                + delay_gain1 * source1_radius
            )
        endpoint = _gronwall_endpoint(
            start_radius, total_forcing, log_norm, step.upper, precision
        )
        with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
            maximum = max(start_radius, endpoint)
        rows.append(
            {
                "cell_index": index,
                "start_radius": start_radius,
                "center_jump_upper": jump,
                "local_residual_p_upper": local_residual,
                "model_voltage_residual_upper": model_voltage_residual,
                "delay0_error_gain_upper": delay_gain0,
                "delay1_error_gain_upper": delay_gain1,
                "source0_radius": source0_radius,
                "source1_radius": source1_radius,
                "logarithmic_norm_upper": log_norm,
                "endpoint_radius": endpoint,
                "maximum_radius": maximum,
            }
        )
        previous_endpoint = endpoint
        previous_voltage = voltage
        previous_recovery = recovery
    return tuple(rows)


def _guide(data: _CentreData) -> tuple[_GuideCell, ...]:
    step = data.tau0 / DELAY_GRID_DIVISOR
    if data.tau1 != step * 640:
        raise ArithmeticError("the exact binary delay grid changed")
    full_count = int(math.floor(data.period / step))
    boundaries = [index * step for index in range(full_count + 1)]
    if boundaries[-1] < data.period:
        boundaries.append(data.period)
    cells: list[_GuideCell] = []
    start_v = 0.0j
    start_w = 0.0j
    for index, (left, right) in enumerate(zip(boundaries[:-1], boundaries[1:], strict=True)):
        local_step = right - left
        current = _taylor(data.current, left, local_step, data.period, data.root)
        delayed0 = _taylor(data.delayed0, left, local_step, data.period, data.root)
        delayed1 = _taylor(data.delayed1, left, local_step, data.period, data.root)
        forcing = _taylor(data.forcing, left, local_step, data.period, data.root)

        def source(delay_cells: int) -> np.ndarray:
            if index < delay_cells:
                return np.zeros(TAYLOR_DEGREE + 1, dtype=complex)
            value = cells[index - delay_cells].voltage
            if local_step == step:
                return value
            return _poly_translate_scale(value, local_step / step)

        source0 = source(512)
        source1 = source(640)
        voltage = np.zeros(TAYLOR_DEGREE + 1, dtype=complex)
        recovery = np.zeros(TAYLOR_DEGREE + 1, dtype=complex)
        voltage[0] = start_v
        recovery[0] = start_w
        for order in range(TAYLOR_DEGREE):
            rhs_v = forcing[order]
            rhs_v -= recovery[order]
            for left_order in range(order + 1):
                right_order = order - left_order
                rhs_v += current[left_order] * voltage[right_order]
                rhs_v += delayed0[left_order] * source0[right_order]
                rhs_v += delayed1[left_order] * source1[right_order]
            rhs_w = data.epsilon * (voltage[order] - recovery[order])
            voltage[order + 1] = local_step * rhs_v / (order + 1)
            recovery[order + 1] = local_step * rhs_w / (order + 1)
        derivative_v = np.arange(1, len(voltage), dtype=float) * voltage[1:] / local_step
        derivative_w = np.arange(1, len(recovery), dtype=float) * recovery[1:] / local_step
        residual_v = np.pad(derivative_v, (0, 1))
        residual_v -= _convolve(current, voltage)[: len(residual_v)]
        residual_v += recovery
        residual_v -= _convolve(delayed0, source0)[: len(residual_v)]
        residual_v -= _convolve(delayed1, source1)[: len(residual_v)]
        residual_v -= forcing
        residual_w = np.pad(derivative_w, (0, 1)) - data.epsilon * (voltage - recovery)
        residual_l1 = float(np.sum(np.abs(residual_v)) + np.sum(np.abs(residual_w)))
        analytic_tail = (
            _taylor_tail_upper(data.current, local_step, data.period, data.root) * float(np.sum(np.abs(voltage)))
            + _taylor_tail_upper(data.delayed0, local_step, data.period, data.root) * float(np.sum(np.abs(source0)))
            + _taylor_tail_upper(data.delayed1, local_step, data.period, data.root) * float(np.sum(np.abs(source1)))
            + _taylor_tail_upper(data.forcing, local_step, data.period, data.root)
        )
        cells.append(
            _GuideCell(
                left=left,
                right=right,
                voltage=voltage,
                recovery=recovery,
                residual_l1=residual_l1,
                analytic_tail_upper=analytic_tail,
            )
        )
        start_v = complex(np.sum(voltage))
        start_w = complex(np.sum(recovery))
    return tuple(cells)


def _row_tail_neumann(data: _CentreData) -> tuple[dict[int, complex], dict[int, complex], tuple[float, ...]]:
    current, delayed = _binary_coefficients(data.prepared.orbit)
    finite_modes = tuple(int(mode) for mode in data.prepared.modes)
    count = len(finite_modes)
    finite_v = {mode: complex(data.left_finite[index]) for index, mode in enumerate(finite_modes)}
    finite_w = {mode: complex(data.left_finite[count + index]) for index, mode in enumerate(finite_modes)}

    def r_action(
        row_v: Mapping[int, complex], row_w: Mapping[int, complex]
    ) -> tuple[defaultdict[int, complex], defaultdict[int, complex]]:
        output_v: defaultdict[int, complex] = defaultdict(complex)
        output_w: defaultdict[int, complex] = defaultdict(complex)
        for mode, coefficient in row_v.items():
            rotations = [
                cmath.exp(-(data.root + 2.0j * math.pi * mode) * tau / data.period)
                for tau in (data.tau0, data.tau1)
            ]
            for difference in current:
                target = mode - int(difference)
                if abs(target) <= 64:
                    continue
                value = current[difference] + (rotations[0] + rotations[1]) * delayed[difference]
                output_v[target] -= data.period * coefficient * value
            if abs(mode) > 64:
                output_w[mode] += data.period * coefficient
        for mode, coefficient in row_w.items():
            if abs(mode) > 64:
                output_v[mode] -= data.period * data.epsilon * coefficient
        return output_v, output_w

    source_v, source_w = r_action(finite_v, finite_w)
    tail_v: dict[int, complex] = {}
    tail_w: dict[int, complex] = {}
    norms: list[float] = []
    for _ in range(ADJOINT_NEUMANN_STEPS):
        action_v, action_w = r_action(tail_v, tail_w)
        modes = set(source_v) | set(source_w) | set(action_v) | set(action_w)
        new_v: dict[int, complex] = {}
        new_w: dict[int, complex] = {}
        for mode in modes:
            fast_diagonal = data.root + 2.0j * math.pi * mode
            slow_diagonal = fast_diagonal + data.period * data.epsilon
            voltage = -(source_v[mode] + action_v[mode]) / fast_diagonal
            recovery = -(source_w[mode] + action_w[mode]) / slow_diagonal
            if abs(voltage) > 0:
                new_v[mode] = voltage
            if abs(recovery) > 0:
                new_w[mode] = recovery
        tail_v, tail_w = new_v, new_w
        norms.append(sum(abs(value) for value in tail_v.values()) + sum(abs(value) for value in tail_w.values()))
    return tail_v, tail_w, tuple(norms)


def _lprime_pairing(
    data: _CentreData,
    tail_v: Mapping[int, complex],
    tail_w: Mapping[int, complex],
) -> complex:
    current, delayed = _binary_coefficients(data.prepared.orbit)
    del current
    modes = tuple(int(mode) for mode in data.prepared.modes)
    count = len(modes)
    qv = {mode: complex(data.right_coefficients[index]) for index, mode in enumerate(modes)}
    qw = {mode: complex(data.right_coefficients[count + index]) for index, mode in enumerate(modes)}
    left_v = {mode: complex(data.left_finite[index]) for index, mode in enumerate(modes)}
    left_w = {mode: complex(data.left_finite[count + index]) for index, mode in enumerate(modes)}
    left_v.update(tail_v)
    left_w.update(tail_w)
    convolution: defaultdict[int, complex] = defaultdict(complex)
    for mode, value in qv.items():
        for difference, coefficient in delayed.items():
            convolution[mode + int(difference)] += coefficient * value
    total = 0.0j
    for mode, left in left_v.items():
        value = qv.get(mode, 0.0j)
        for tau in (data.tau0, data.tau1):
            value += tau * cmath.exp(-(data.root + 2.0j * math.pi * mode) * tau / data.period) * convolution[mode]
        total += left * value
    total += sum(left_w.get(mode, 0.0j) * qw.get(mode, 0.0j) for mode in set(left_w) | set(qw))
    return total


def _forcing_action(
    data: _CentreData,
    tail_v: Mapping[int, complex],
) -> complex:
    modes = tuple(int(mode) for mode in data.prepared.modes)
    left_v = {mode: complex(data.left_finite[index]) for index, mode in enumerate(modes)}
    left_v.update(tail_v)
    total = 0.0j
    for row_mode, left in left_v.items():
        adjoint_mode = -row_mode
        for (growth, forcing_mode), coefficient in data.forcing.items():
            exponent = (growth - 1) * data.root + 2.0j * math.pi * (adjoint_mode + forcing_mode)
            integral = 1.0 if exponent == 0 else (cmath.exp(exponent) - 1) / exponent
            total += data.period * left * coefficient * integral
    return total


def _adjoint_mode_rows(
    data: _CentreData,
    tail_v: Mapping[int, complex],
    tail_w: Mapping[int, complex],
) -> tuple[dict[int, complex], dict[int, complex]]:
    modes = tuple(int(mode) for mode in data.prepared.modes)
    count = len(modes)
    row_v = {
        mode: complex(data.left_finite[index])
        for index, mode in enumerate(modes)
    }
    row_w = {
        mode: complex(data.left_finite[count + index])
        for index, mode in enumerate(modes)
    }
    row_v.update(tail_v)
    row_w.update(tail_w)
    # Stage 4D proves r_hat[n]=E_minus_state[-n].
    return (
        {-mode: coefficient for mode, coefficient in row_v.items()},
        {-mode: coefficient for mode, coefficient in row_w.items()},
    )


def _periodic_coefficients(value: Mapping[ExpKey, complex]) -> dict[int, complex]:
    if any(growth != 0 for growth, _ in value):
        raise ValueError("a periodic coefficient dictionary has nonzero growth")
    return {mode: coefficient for (_, mode), coefficient in value.items()}


def _mode_convolution(
    left: Mapping[int, complex], right: Mapping[int, complex]
) -> dict[int, complex]:
    result: defaultdict[int, complex] = defaultdict(complex)
    for left_mode, left_value in left.items():
        for right_mode, right_value in right.items():
            result[left_mode + right_mode] += left_value * right_value
    return {
        mode: value for mode, value in result.items() if abs(value) > TRIM_THRESHOLD
    }


def _history_action(
    data: _CentreData,
    tail_v: Mapping[int, complex],
    tail_w: Mapping[int, complex],
    voltage: Mapping[ExpKey, complex],
    recovery: Mapping[ExpKey, complex],
) -> complex:
    """Evaluate the Stage-4D atom-plus-density action at phase zero."""

    adjoint_v, adjoint_w = _adjoint_mode_rows(data, tail_v, tail_w)
    total = sum(adjoint_v.values()) * _evaluate(voltage, 0.0, data.period, data.root)
    total += sum(adjoint_w.values()) * _evaluate(recovery, 0.0, data.period, data.root)
    for delay, delayed_coefficient in (
        (data.tau0, data.delayed0),
        (data.tau1, data.delayed1),
    ):
        alpha = delay / data.period
        density_periodic = _mode_convolution(
            adjoint_v, _periodic_coefficients(delayed_coefficient)
        )
        shifted_density = {
            mode: coefficient
            * cmath.exp((-data.root + 2.0j * math.pi * mode) * alpha)
            for mode, coefficient in density_periodic.items()
        }
        by_growth: defaultdict[int, dict[int, complex]] = defaultdict(dict)
        for (growth, mode), coefficient in voltage.items():
            by_growth[growth][mode] = coefficient
        for growth, coefficients in by_growth.items():
            product = _mode_convolution(shifted_density, coefficients)
            for mode, coefficient in product.items():
                exponent = (growth - 1) * data.root + 2.0j * math.pi * mode
                integral = alpha if exponent == 0 else (
                    1 - cmath.exp(-exponent * alpha)
                ) / exponent
                total += data.period * coefficient * integral
    return total


def _guide_density_dictionary(
    data: _CentreData,
    tail_v: Mapping[int, complex],
    tail_w: Mapping[int, complex],
    delay: float,
    delayed_coefficient: Mapping[ExpKey, complex],
) -> tuple[ExpDict, ExpDict]:
    """Return the stored-row voltage-history density for one delay.

    The tiny density tail is split off at the dedicated direct-action
    threshold.  The omitted dictionary is returned and added outward in the
    directed cell integral; it is never inferred from mesh spread.
    """

    adjoint_v, _ = _adjoint_mode_rows(data, tail_v, tail_w)
    periodic = _periodic_coefficients(delayed_coefficient)
    convolution: defaultdict[int, complex] = defaultdict(complex)
    for left_mode, left_value in adjoint_v.items():
        for right_mode, right_value in periodic.items():
            convolution[left_mode + right_mode] += left_value * right_value
    alpha = delay / data.period
    full = {
        (-1, mode): coefficient
        * cmath.exp((-data.root + 2.0j * math.pi * mode) * alpha)
        for mode, coefficient in convolution.items()
        if coefficient != 0
    }
    return (
        {
            key: coefficient
            for key, coefficient in full.items()
            if abs(coefficient) >= DIRECT_ACTION_DENSITY_TRIM_THRESHOLD
        },
        {
            key: coefficient
            for key, coefficient in full.items()
            if abs(coefficient) < DIRECT_ACTION_DENSITY_TRIM_THRESHOLD
        },
    )


def _compose_float_polynomial(
    value: np.ndarray, offset: float, scale: float
) -> np.ndarray:
    result = np.zeros(len(value), dtype=complex)
    for source_order, coefficient in enumerate(value):
        for target_order in range(source_order + 1):
            result[target_order] += (
                coefficient
                * math.comb(source_order, target_order)
                * offset ** (source_order - target_order)
                * scale**target_order
            )
    return result


def _guide_history_action_centre(
    data: _CentreData,
    cells: tuple[_GuideCell, ...],
    tail_v: Mapping[int, complex],
    tail_w: Mapping[int, complex],
) -> complex:
    """Direct atom-plus-density action on the piecewise Taylor guide."""

    adjoint_v, adjoint_w = _adjoint_mode_rows(data, tail_v, tail_w)
    voltage_current = complex(np.sum(cells[-1].voltage))
    recovery_current = complex(np.sum(cells[-1].recovery))
    total = sum(adjoint_v.values()) * voltage_current
    total += sum(adjoint_w.values()) * recovery_current
    for delay, delayed_coefficient in (
        (data.tau0, data.delayed0),
        (data.tau1, data.delayed1),
    ):
        density, _ = _guide_density_dictionary(
            data, tail_v, tail_w, delay, delayed_coefficient
        )
        history_start = data.period - delay
        for cell in cells:
            segment_left = max(cell.left, history_start)
            segment_right = min(cell.right, data.period)
            if not segment_left < segment_right:
                continue
            cell_step = cell.right - cell.left
            offset = (segment_left - cell.left) / cell_step
            scale = (segment_right - segment_left) / cell_step
            voltage = _compose_float_polynomial(cell.voltage, offset, scale)
            segment_step = segment_right - segment_left
            density_polynomial = _taylor(
                density,
                segment_left - data.period,
                segment_step,
                data.period,
                data.root,
            )
            product = np.convolve(density_polynomial, voltage)
            total += segment_step * sum(
                coefficient / (order + 1)
                for order, coefficient in enumerate(product)
            )
    return total


def _directed_guide_history_action(
    data: _CentreData,
    cells: tuple[_GuideCell, ...],
    tail_v: Mapping[int, complex],
    tail_w: Mapping[int, complex],
) -> tuple[DirectedComplexInterval, gmpy2.mpfr]:
    """Outward direct action of the stored row on the guide history."""

    precision = PRECISION_BITS
    period = DirectedInterval.from_float(data.period, precision)
    root = DirectedInterval.from_float(data.root, precision)
    adjoint_v, adjoint_w = _adjoint_mode_rows(data, tail_v, tail_w)
    voltage_current = DirectedComplexInterval.zero(precision)
    recovery_current = DirectedComplexInterval.zero(precision)
    for coefficient in cells[-1].voltage:
        voltage_current = voltage_current + _complex_point(
            complex(coefficient), precision
        )
    for coefficient in cells[-1].recovery:
        recovery_current = recovery_current + _complex_point(
            complex(coefficient), precision
        )
    voltage_atom = DirectedComplexInterval.zero(precision)
    recovery_atom = DirectedComplexInterval.zero(precision)
    for coefficient in adjoint_v.values():
        voltage_atom = voltage_atom + _complex_point(coefficient, precision)
    for coefficient in adjoint_w.values():
        recovery_atom = recovery_atom + _complex_point(coefficient, precision)
    total = voltage_atom * voltage_current + recovery_atom * recovery_current
    tail_radius = gmpy2.mpfr(0, precision)
    for delay, delayed_coefficient in (
        (data.tau0, data.delayed0),
        (data.tau1, data.delayed1),
    ):
        density, omitted_density = _guide_density_dictionary(
            data, tail_v, tail_w, delay, delayed_coefficient
        )
        omitted_density_upper = gmpy2.mpfr(0, precision)
        with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
            growth_amplitude = gmpy2.exp(
                root.upper * delay / period.lower
            )
            for coefficient in omitted_density.values():
                omitted_density_upper += (
                    _complex_point(coefficient, precision).upper_abs()
                    * growth_amplitude
                )
        history_start = data.period - delay
        for cell in cells:
            segment_left_float = max(cell.left, history_start)
            segment_right_float = min(cell.right, data.period)
            if not segment_left_float < segment_right_float:
                continue
            cell_left = DirectedInterval.from_float(cell.left, precision)
            cell_right = DirectedInterval.from_float(cell.right, precision)
            segment_left = DirectedInterval.from_float(
                segment_left_float, precision
            )
            segment_right = DirectedInterval.from_float(
                segment_right_float, precision
            )
            cell_step = cell_right - cell_left
            segment_step = segment_right - segment_left
            offset = (segment_left - cell_left) / cell_step
            scale = segment_step / cell_step
            voltage = _compose_point_polynomial(cell.voltage, offset, scale)
            density_polynomial = _directed_taylor(
                density,
                segment_left - period,
                segment_step,
                period,
                root,
            )
            product = _complex_poly_multiply(density_polynomial, voltage)
            integral = DirectedComplexInterval.zero(precision)
            for order, coefficient in enumerate(product):
                integral = integral + coefficient * (
                    segment_step / (order + 1)
                )
            total = total + integral
            density_tail = _directed_taylor_tail_upper(
                density, segment_step, period, root
            )
            guide_upper = _complex_poly_bernstein_upper(voltage)
            with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
                tail_radius += (
                    segment_step.upper
                    * (density_tail + omitted_density_upper)
                    * guide_upper
                )
    symmetric = DirectedInterval.from_bounds(
        -tail_radius, tail_radius, precision
    )
    return (
        total + DirectedComplexInterval(symmetric, symmetric),
        tail_radius,
    )


def _event_centre(
    data: _CentreData,
    cells: tuple[_GuideCell, ...],
    tail_v: Mapping[int, complex],
    tail_w: Mapping[int, complex],
) -> dict[str, object]:
    udot_t_v = _period_shift(data.udot_v, data.root)
    udot_t_w = _period_shift(data.udot_w, data.root)
    u_t_v = _period_shift(data.u_v, data.root)
    xdot_v0 = _evaluate(data.xdot_v, 0.0, data.period, data.root)
    u_v_t0 = _evaluate(u_t_v, 0.0, data.period, data.root)
    tau_q = -u_v_t0 / xdot_v0
    v_current = complex(np.sum(cells[-1].voltage))
    w_current = complex(np.sum(cells[-1].recovery))
    udot_v_current = _evaluate(udot_t_v, 0.0, data.period, data.root)
    xddot_v_current = _evaluate(data.xddot_v, 0.0, data.period, data.root)
    event_core_current = (
        v_current + 2 * udot_v_current * tau_q + xddot_v_current * tau_q**2
    )
    tau_qq = -event_core_current / xdot_v0
    # The inhomogeneous identity is written with the advanced covector at
    # time T.  Since z(T)=exp(-s)z(0), identification of the returned history
    # with the phase-zero section contributes the inverse factor exp(s).
    f_v = math.exp(data.root) * _forcing_action(data, tail_v)
    f_v_guide_history = _guide_history_action_centre(
        data, cells, tail_v, tail_w
    )
    f_udot = _history_action(data, tail_v, tail_w, udot_t_v, udot_t_w)
    f_xddot = _history_action(
        data, tail_v, tail_w, data.xddot_v, data.xddot_w
    )
    f_xdot = _history_action(data, tail_v, tail_w, data.xdot_v, data.xdot_w)
    f_q_history = _history_action(
        data, tail_v, tail_w, data.qsection_v, data.qsection_w
    )
    f_q_lprime = _lprime_pairing(data, tail_v, tail_w)
    # Define the centre scalar by the direct atom-plus-density action on the
    # same piecewise guide.  The phase-tangent term is excluded analytically:
    # the exact nonneutral covector annihilates the exact phase tangent.
    f_y = f_v_guide_history + 2 * tau_q * f_udot + tau_q**2 * f_xddot
    quotient = f_y / f_q_history
    correction_v = _add(
        _scale(udot_t_v, 2 * tau_q),
        _scale(data.xddot_v, tau_q**2),
        _scale(data.xdot_v, tau_qq),
        _scale(data.qsection_v, -quotient),
    )
    correction_w = _add(
        _scale(udot_t_w, 2 * tau_q),
        _scale(data.xddot_w, tau_q**2),
        _scale(data.xdot_w, tau_qq),
        _scale(data.qsection_w, -quotient),
    )
    history_start = data.period - data.tau1
    maximum = 0.0
    maximum_time = history_start
    maximum_component = "voltage"
    for cell in cells:
        left = max(cell.left, history_start)
        right = min(cell.right, data.period)
        if not left < right:
            continue
        for time in np.linspace(left, right, 65):
            local = (time - cell.left) / (cell.right - cell.left)
            powers = local ** np.arange(len(cell.voltage), dtype=float)
            voltage = complex(cell.voltage @ powers) + _evaluate(
                correction_v, time - data.period, data.period, data.root
            )
            if abs(voltage) > maximum:
                maximum = abs(voltage)
                maximum_time = time - data.period
                maximum_component = "voltage"
    # The declared history space is C([-tau_max,0],R) x R: only voltage has
    # a retained history; recovery contributes at the current endpoint.
    recovery_current = w_current + _evaluate(
        correction_w, 0.0, data.period, data.root
    )
    if abs(recovery_current) > maximum:
        maximum = abs(recovery_current)
        maximum_time = 0.0
        maximum_component = "current recovery"
    theta = np.linspace(-data.tau1, 0.0, 20001)
    q_norm = max(
        max(abs(_evaluate(data.qsection_v, float(t), data.period, data.root)) for t in theta),
        abs(_evaluate(data.qsection_w, 0.0, data.period, data.root)),
    )
    return {
        "tau_q": tau_q,
        "tau_qq": tau_qq,
        "f_v": f_v,
        "f_v_guide_history": f_v_guide_history,
        "forcing_vs_guide_history_action_defect": f_v - f_v_guide_history,
        "f_udot": f_udot,
        "f_xddot": f_xddot,
        "f_xdot": f_xdot,
        "f_q_history": f_q_history,
        "f_q_lprime": f_q_lprime,
        "f_y": f_y,
        "quotient": quotient,
        "raw_v_current": v_current,
        "raw_w_current": w_current,
        "event_core_current": event_core_current,
        "deflated_history_sampled_norm": maximum,
        "deflated_history_sampled_argmax_time": maximum_time,
        "deflated_history_sampled_argmax_component": maximum_component,
        "q_section_sampled_full_norm": q_norm,
        "normalized_stable_output_sampled": maximum / q_norm**2,
        "route_c_current_voltage_defect": abs(
            v_current
            + _evaluate(correction_v, 0.0, data.period, data.root)
        ),
        "correction_v": correction_v,
        "correction_w": correction_w,
    }


def _compose_point_polynomial(
    value: np.ndarray,
    offset: DirectedInterval,
    scale: DirectedInterval,
) -> tuple[DirectedComplexInterval, ...]:
    precision = offset.precision
    result = [DirectedComplexInterval.zero(precision) for _ in range(len(value))]
    offset_powers = [_real_point(1, precision)]
    scale_powers = [_real_point(1, precision)]
    for _ in range(1, len(value)):
        offset_powers.append(offset_powers[-1] * offset)
        scale_powers.append(scale_powers[-1] * scale)
    for source_order, coefficient in enumerate(value):
        point = _complex_point(complex(coefficient), precision)
        for target_order in range(source_order + 1):
            factor = (
                _real_point(math.comb(source_order, target_order), precision)
                * offset_powers[source_order - target_order]
                * scale_powers[target_order]
            )
            result[target_order] = result[target_order] + point * factor
    return tuple(result)


def _directed_centre_deflated_upper(
    data: _CentreData,
    cells: tuple[_GuideCell, ...],
    event: Mapping[str, object],
) -> dict[str, gmpy2.mpfr | int]:
    precision = PRECISION_BITS
    period = DirectedInterval.from_float(data.period, precision)
    tau1 = DirectedInterval.from_float(data.tau1, precision)
    history_start = period - tau1
    regular_step = DirectedInterval.from_float(data.tau0, precision) / DELAY_GRID_DIVISOR
    correction = event["correction_v"]
    if not isinstance(correction, Mapping):
        raise TypeError("the event centre lost its correlated voltage correction")
    correction_dictionary, correction_omitted = _validation_trim(
        correction, data.root, precision
    )
    root = DirectedInterval.from_float(data.root, precision)
    maximum = gmpy2.mpfr(0, precision)
    active = 0
    maximum_index = -1
    maximum_tail = gmpy2.mpfr(0, precision)
    for index, cell in enumerate(cells):
        if index < len(cells) - 1:
            cell_left = regular_step * index
            cell_step = regular_step
            cell_right = cell_left + cell_step
        else:
            cell_left = regular_step * index
            cell_right = period
            cell_step = cell_right - cell_left
        if cell_right.upper <= history_start.lower:
            continue
        segment_left = history_start if cell_left.lower < history_start.upper else cell_left
        segment_right = cell_right
        if segment_left.lower >= segment_right.upper:
            continue
        offset = (segment_left - cell_left) / cell_step
        segment_step = segment_right - segment_left
        scale = segment_step / cell_step
        v_polynomial = _compose_point_polynomial(cell.voltage, offset, scale)
        theta_left = segment_left - period
        analytic = _directed_taylor(
            correction_dictionary,
            theta_left,
            segment_step,
            period,
            root,
        )
        combined = _complex_poly_add(v_polynomial, analytic)
        local = _complex_poly_bernstein_upper(combined)
        tail = _directed_taylor_tail_upper(
            correction_dictionary, segment_step, period, root
        )
        with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
            local += tail + correction_omitted
        if local > maximum:
            maximum = local
            maximum_index = index
            maximum_tail = tail + correction_omitted
        active += 1
    recovery = event["raw_w_current"]
    correction_w = event["correction_w"]
    if not isinstance(recovery, complex) or not isinstance(correction_w, Mapping):
        raise TypeError("the event centre lost the recovery endpoint")
    recovery_center = recovery + _evaluate(
        correction_w, 0.0, data.period, data.root
    )
    recovery_upper = _complex_point(recovery_center, precision).upper_abs()
    maximum = max(maximum, recovery_upper)
    return {
        "active_history_cells": active,
        "maximum_cell_index": maximum_index,
        "correlated_centre_history_norm_upper": maximum,
        "maximum_analytic_tail_and_trim_upper": maximum_tail,
        "current_recovery_abs_upper": recovery_upper,
    }


def _final_error_budget_pilot(
    data: _CentreData,
    event: Mapping[str, object],
    tube: tuple[dict[str, gmpy2.mpfr | int], ...],
    uncertainty: Mapping[str, float],
) -> dict[str, float]:
    """Design the final outward budget before its MPFR transcription."""

    payload = json.loads(
        (data.repository / STAGE4D_RESULT_RELATIVE_PATH).read_text(encoding="utf-8")
    )
    validate_stage4d_result(payload, data.repository)
    artifact = payload["artifact"]
    tail = artifact["summable_adjoint_tail_certificate"]
    measure = artifact["continuous_history_measure_enclosure"]
    contraction = float(tail["tail_row_contraction_upper"])
    tail_total = float(tail["full_tail_split_l1_upper"])
    tail_gain = float(tail["tail_l1_gain_from_finite_upper"])
    tail_inverse = float(tail["tail_inverse_row_sum_upper"])
    adjoint_norm = float(tail["complete_adjoint_split_wiener_l1_upper"])
    finite_error = len(data.left_finite) * data.left_row_dual_error
    coefficient_variation = (
        uncertainty["root_error"]
        + uncertainty["period_error"]
        * (
            1
            + float(data.prepared.current_binary_norm)
            + 2 * float(data.prepared.delayed_binary_norm)
        )
        + data.period
        * (
            float(data.prepared.current_total_variation)
            + float(data.prepared.delayed_total_variation)
        )
        + (data.tau0 + data.tau1)
        * float(data.prepared.delayed_binary_norm)
        * (
            uncertainty["root_error"]
            + uncertainty["period_error"] * (1 + abs(data.root)) / data.period
        )
    )
    if coefficient_variation >= 1e-3:
        raise ArithmeticError("the adjoint tail operator variation guard failed")
    tail_error = (
        tail_total * contraction**ADJOINT_NEUMANN_STEPS
        + tail_gain * finite_error
        + tail_inverse * adjoint_norm * coefficient_variation
    )
    adjoint_l1_error = finite_error + tail_error
    measure_norm = float(measure["unnormalized_history_measure_norm_upper"])
    bmax = max(
        _dictionary_l1_upper(data.delayed0, data.root),
        _dictionary_l1_upper(data.delayed1, data.root),
    )
    action_factor = 1 + (data.tau0 + data.tau1) * bmax

    def complex_value(name: str) -> complex:
        value = event[name]
        if not isinstance(value, complex):
            raise TypeError(f"event value {name} is not complex")
        return value

    def action_error(center_bound: float, history_error: float) -> float:
        return (
            adjoint_l1_error * action_factor * center_bound
            + measure_norm * history_error
        )

    forcing_bound = _dictionary_l1_upper(data.forcing, data.root)
    f_v_center = complex_value("f_v")
    f_v_error = (
        math.exp(data.root + uncertainty["root_error"])
        * (data.period + uncertainty["period_error"])
        * (
            adjoint_l1_error * forcing_bound
            + adjoint_norm * uncertainty["forcing_error"]
        )
        + abs(f_v_center)
        * 2
        * (
            uncertainty["root_error"]
            + uncertainty["period_error"] / data.period
        )
    )
    udot_bound = max(
        _dictionary_l1_upper(_period_shift(data.udot_v, data.root), data.root),
        _dictionary_l1_upper(_period_shift(data.udot_w, data.root), data.root),
    )
    xddot_bound = max(
        _dictionary_l1_upper(data.xddot_v, data.root),
        _dictionary_l1_upper(data.xddot_w, data.root),
    )
    q_bound = max(
        _dictionary_l1_upper(data.qsection_v, data.root),
        _dictionary_l1_upper(data.qsection_w, data.root),
    )
    f_udot_error = action_error(udot_bound, uncertainty["udot_error"])
    f_xddot_error = action_error(xddot_bound, uncertainty["xddot_error"])
    f_q_error = action_error(q_bound, uncertainty["qsection_error"])
    f_q_center = complex_value("f_q_history")
    f_q_lower = abs(f_q_center) - f_q_error
    if f_q_lower <= 0:
        raise ArithmeticError("the sharpened history normalization vanished")
    tau_q = complex_value("tau_q")
    tau_qq = complex_value("tau_qq")
    u_v_t = _evaluate(
        _period_shift(data.u_v, data.root), 0, data.period, data.root
    )
    xdot_v = _evaluate(data.xdot_v, 0, data.period, data.root)
    tau_q_error = (
        uncertainty["u_error"] / uncertainty["event_speed_lower"]
        + abs(u_v_t)
        * uncertainty["xdot_error"]
        / uncertainty["event_speed_lower"] ** 2
    )
    coordinate_bound = float(_p_constants(PRECISION_BITS)[0])
    vqq_p_error = max(float(row["maximum_radius"]) for row in tube)
    vqq_coordinate_error = coordinate_bound * vqq_p_error
    udot_v_center = _evaluate(
        _period_shift(data.udot_v, data.root), 0, data.period, data.root
    )
    xddot_v_center = _evaluate(data.xddot_v, 0, data.period, data.root)
    event_core = complex_value("event_core_current")
    event_core_error = (
        vqq_coordinate_error
        + 2
        * (
            (abs(tau_q) + tau_q_error) * uncertainty["udot_error"]
            + abs(udot_v_center) * tau_q_error
        )
        + (abs(tau_q) + tau_q_error) ** 2
        * uncertainty["xddot_error"]
        + abs(xddot_v_center)
        * (2 * abs(tau_q) * tau_q_error + tau_q_error**2)
    )
    tau_qq_error = (
        event_core_error / uncertainty["event_speed_lower"]
        + abs(event_core)
        * uncertainty["xdot_error"]
        / uncertainty["event_speed_lower"] ** 2
    )
    f_udot = complex_value("f_udot")
    f_xddot = complex_value("f_xddot")
    f_y = complex_value("f_y")
    f_y_error = (
        f_v_error
        + 2
        * (
            (abs(tau_q) + tau_q_error) * f_udot_error
            + abs(f_udot) * tau_q_error
        )
        + (abs(tau_q) + tau_q_error) ** 2 * f_xddot_error
        + abs(f_xddot)
        * (2 * abs(tau_q) * tau_q_error + tau_q_error**2)
    )
    quotient = complex_value("quotient")
    quotient_error = (
        f_y_error / f_q_lower
        + abs(f_y) * f_q_error / (abs(f_q_center) * f_q_lower)
    )
    xdot_bound = uncertainty["xdot_bound"]
    stable_history_error = (
        vqq_coordinate_error
        + 2
        * (
            (abs(tau_q) + tau_q_error) * uncertainty["udot_error"]
            + udot_bound * tau_q_error
        )
        + (abs(tau_q) + tau_q_error) ** 2
        * uncertainty["xddot_error"]
        + xddot_bound
        * (2 * abs(tau_q) * tau_q_error + tau_q_error**2)
        + (abs(tau_qq) + tau_qq_error) * uncertainty["xdot_error"]
        + xdot_bound * tau_qq_error
        + (abs(quotient) + quotient_error) * uncertainty["qsection_error"]
        + q_bound * quotient_error
        + uncertainty["binary_algebra_guard"]
    )
    return {
        "coefficient_operator_variation_upper": coefficient_variation,
        "finite_adjoint_l1_error_upper": finite_error,
        "adjoint_tail_l1_error_upper": tail_error,
        "complete_adjoint_l1_error_upper": adjoint_l1_error,
        "f_v_error_upper": f_v_error,
        "f_udot_error_upper": f_udot_error,
        "f_xddot_error_upper": f_xddot_error,
        "f_q_error_upper": f_q_error,
        "f_q_modulus_lower": f_q_lower,
        "tau_q_error_upper": tau_q_error,
        "vqq_p_error_upper": vqq_p_error,
        "vqq_coordinate_error_upper": vqq_coordinate_error,
        "event_core_error_upper": event_core_error,
        "tau_qq_error_upper": tau_qq_error,
        "f_y_error_upper": f_y_error,
        "quotient_error_upper": quotient_error,
        "stable_history_error_upper": stable_history_error,
    }


def _directed_correlated_error_budget(
    data: _CentreData,
    cells: tuple[_GuideCell, ...],
    residual_rows: tuple[dict[str, gmpy2.mpfr | int], ...],
    event: Mapping[str, object],
    tube: tuple[dict[str, gmpy2.mpfr | int], ...],
    uncertainty: Mapping[str, float],
    centre: Mapping[str, gmpy2.mpfr | int],
    tail_v: Mapping[int, complex],
    tail_w: Mapping[int, complex],
) -> dict[str, gmpy2.mpfr]:
    """Enclose the quotient through its correlated residual.

    If ``c=N_0/D_0`` is the centre quotient, the exact quotient ``N/D``
    obeys

        N/D-c = f(Y-cq)/f(q).

    The centre scalar is defined by the stored row's *direct* action on the
    piecewise guide.  The exact-minus-guide equation therefore contains every
    directed guide residual, recovery residual, model residual and cell-seam
    impulse.  Parseval bounds the continuous action and the Wiener row norm
    bounds the seam impulses.  No approximate-adjoint inhomogeneous identity
    is assumed.
    """

    precision = PRECISION_BITS

    def point(value: float | int | gmpy2.mpfr) -> DirectedInterval:
        if isinstance(value, float):
            return DirectedInterval.from_float(value, precision)
        return DirectedInterval.from_bounds(value, value, precision)

    def guarded_upper(value: float, guard: float = SCALAR_TRANSCRIPTION_GUARD) -> gmpy2.mpfr:
        return (point(value) + point(guard)).upper

    def positive_interval(value: float, guard: float = SCALAR_TRANSCRIPTION_GUARD) -> DirectedInterval:
        return DirectedInterval.from_bounds(0, guarded_upper(value, guard), precision)

    def complex_value(name: str) -> complex:
        value = event[name]
        if not isinstance(value, complex):
            raise TypeError(f"event value {name} is not complex")
        return value

    def complex_upper(name: str) -> gmpy2.mpfr:
        return _complex_point(complex_value(name), precision).upper_abs()

    stage3_payload = json.loads(
        (data.repository / STAGE3_RESULT_RELATIVE_PATH).read_text(encoding="utf-8")
    )
    validate_stage3_stable_projection_result(stage3_payload, data.repository)
    stage3_certificate = stage3_payload["certificate"]
    route_c = stage3_certificate["route_c_component_audit"]
    q_norm_lower = DirectedInterval.from_decimal(
        route_c["section_voltage_component_at_test_time_abs_lower"], precision
    ).lower
    event_speed_lower = DirectedInterval.from_decimal(
        route_c["exact_physical_voltage_field_at_phase_zero_lower"], precision
    ).lower

    stage4d_payload = json.loads(
        (data.repository / STAGE4D_RESULT_RELATIVE_PATH).read_text(encoding="utf-8")
    )
    validate_stage4d_result(stage4d_payload, data.repository)
    stage4d = stage4d_payload["artifact"]
    tail = stage4d["summable_adjoint_tail_certificate"]
    measure = stage4d["continuous_history_measure_enclosure"]

    def parent_upper(mapping: Mapping[str, object], name: str) -> DirectedInterval:
        return DirectedInterval.from_decimal(str(mapping[name]), precision)

    finite_error = positive_interval(
        len(data.left_finite) * data.left_row_dual_error
    )
    root_error = positive_interval(uncertainty["root_error"])
    period_error = positive_interval(uncertainty["period_error"])
    period = point(data.period)
    root_abs = point(abs(data.root))
    current_norm = point(float(data.prepared.current_binary_norm))
    delayed_norm = point(float(data.prepared.delayed_binary_norm))
    current_variation = point(float(data.prepared.current_total_variation))
    delayed_variation = point(float(data.prepared.delayed_total_variation))
    coefficient_variation = (
        root_error
        + period_error * (1 + current_norm + 2 * delayed_norm)
        + period * (current_variation + delayed_variation)
        + point(data.tau0 + data.tau1)
        * delayed_norm
        * (
            root_error
            + period_error * (1 + root_abs) / (period - period_error)
        )
    )
    contraction = parent_upper(tail, "tail_row_contraction_upper")
    tail_total = parent_upper(tail, "full_tail_split_l1_upper")
    tail_gain = parent_upper(tail, "tail_l1_gain_from_finite_upper")
    tail_inverse = parent_upper(tail, "tail_inverse_row_sum_upper")
    adjoint_norm = parent_upper(tail, "complete_adjoint_split_wiener_l1_upper")
    adjoint_tail_error = (
        tail_total * contraction**ADJOINT_NEUMANN_STEPS
        + tail_gain * finite_error
        + tail_inverse * adjoint_norm * coefficient_variation
    )
    adjoint_error = finite_error + adjoint_tail_error

    delayed_coefficient_error = positive_interval(
        uncertainty["delayed_coefficient_each_error"]
    )
    bmax = max(
        _dictionary_l1_directed_upper(data.delayed0, data.root, precision=precision),
        _dictionary_l1_directed_upper(data.delayed1, data.root, precision=precision),
    )
    action_factor = 1 + point(data.tau0 + data.tau1) * (
        point(bmax) + delayed_coefficient_error
    )
    measure_norm = parent_upper(
        measure, "unnormalized_history_measure_norm_upper"
    )
    voltage_adjoint_wiener = parent_upper(
        measure, "voltage_adjoint_wiener_l1_upper"
    ) + adjoint_error
    period_lower = period - period_error
    finite_basis_shift = DirectedInterval.from_decimal(0, precision)
    for mode, coefficient in zip(
        data.prepared.modes,
        data.left_finite[: len(data.prepared.modes)],
        strict=True,
    ):
        frequency = pi_interval(precision) * (2 * abs(int(mode))) + root_abs
        phase_shift = (
            frequency
            * point(data.tau1)
            * period_error
            / period_lower**2
            + point(data.tau1) * root_error / period_lower
        )
        finite_basis_shift = finite_basis_shift + point(
            _complex_point(complex(coefficient), precision).upper_abs()
        ) * phase_shift
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        tail_center_l1 = gmpy2.mpfr(0, precision)
        for coefficient in tail_v.values():
            tail_center_l1 += _complex_point(
                coefficient, precision
            ).upper_abs()
    tail_basis_shift = 2 * (
        point(tail_center_l1) + adjoint_tail_error
    )
    adjoint_density_basis_shift = (
        finite_basis_shift + tail_basis_shift
    ) * point(data.tau0 + data.tau1) * (
        point(bmax) + delayed_coefficient_error
    )
    density_convolution_rounding_guard = DirectedInterval.from_bounds(
        0, "1e-8", precision
    )
    history_measure_difference = (
        adjoint_error * action_factor
        + voltage_adjoint_wiener
        * point(data.tau0 + data.tau1)
        * delayed_coefficient_error
        + adjoint_density_basis_shift
        + density_convolution_rounding_guard
    )

    q_bound = max(
        _dictionary_l1_directed_upper(data.qsection_v, data.root),
        _dictionary_l1_directed_upper(data.qsection_w, data.root),
    )
    udot_bound = max(
        _dictionary_l1_directed_upper(
            _period_shift(data.udot_v, data.root), data.root
        ),
        _dictionary_l1_directed_upper(
            _period_shift(data.udot_w, data.root), data.root
        ),
    )
    xddot_bound = max(
        _dictionary_l1_directed_upper(data.xddot_v, data.root),
        _dictionary_l1_directed_upper(data.xddot_w, data.root),
    )
    xdot_bound = guarded_upper(uncertainty["xdot_bound"])
    q_error = positive_interval(uncertainty["qsection_error"])
    udot_error = positive_interval(uncertainty["udot_error"])
    xddot_error = positive_interval(uncertainty["xddot_error"])
    xdot_error = positive_interval(uncertainty["xdot_error"])

    f_q_center_lower = _complex_point(
        complex_value("f_q_history"), precision
    ).lower_abs()
    f_q_error = history_measure_difference * point(q_bound) + measure_norm * q_error
    f_q_history_identity_defect = _complex_point(
        complex_value("f_q_history") - complex_value("f_q_lprime"),
        precision,
    ).upper_abs()
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        f_q_lower = f_q_center_lower - f_q_error.upper
    if f_q_lower <= 0:
        raise ArithmeticError("the correlated quotient normalization vanished")

    u_v_t = _evaluate(
        _period_shift(data.u_v, data.root), 0.0, data.period, data.root
    )
    xdot_v = _evaluate(data.xdot_v, 0.0, data.period, data.root)
    tau_q_error = (
        positive_interval(uncertainty["u_error"]) / point(event_speed_lower)
        + point(abs(u_v_t))
        * xdot_error
        / point(event_speed_lower) ** 2
    )
    coordinate_bound = point(_p_constants(precision)[0])
    vqq_p_error = point(
        max(
            row["maximum_radius"]
            for row in tube
            if isinstance(row["maximum_radius"], gmpy2.mpfr)
        )
    )
    vqq_coordinate_error = coordinate_bound * vqq_p_error
    tau_q = point(complex_upper("tau_q"))
    udot_v_center = point(
        abs(
            _evaluate(
                _period_shift(data.udot_v, data.root),
                0.0,
                data.period,
                data.root,
            )
        )
    )
    xddot_v_center = point(
        abs(_evaluate(data.xddot_v, 0.0, data.period, data.root))
    )
    event_core = point(complex_upper("event_core_current"))
    event_core_error = (
        vqq_coordinate_error
        + 2
        * (
            (tau_q + tau_q_error) * udot_error
            + udot_v_center * tau_q_error
        )
        + (tau_q + tau_q_error) ** 2 * xddot_error
        + xddot_v_center
        * (2 * tau_q * tau_q_error + tau_q_error**2)
    )
    tau_qq_error = (
        event_core_error / point(event_speed_lower)
        + event_core * xdot_error / point(event_speed_lower) ** 2
    )

    quotient = point(complex_upper("quotient"))
    tau_qq = point(complex_upper("tau_qq"))
    udot_history_error = 2 * (
        (tau_q + tau_q_error) * udot_error
        + point(udot_bound) * tau_q_error
    )
    xddot_history_error = (
        (tau_q + tau_q_error) ** 2 * xddot_error
        + point(xddot_bound)
        * (2 * tau_q * tau_q_error + tau_q_error**2)
    )
    phase_history_error = (
        (tau_qq + tau_qq_error) * xdot_error
        + point(xdot_bound) * tau_qq_error
    )
    q_center_history_error = quotient * q_error
    algebra_guard = positive_interval(uncertainty["binary_algebra_guard"])
    base_nonquotient_history_error = (
        vqq_coordinate_error
        + udot_history_error
        + xddot_history_error
        + phase_history_error
        + q_center_history_error
        + algebra_guard
    )

    centre_upper = point(
        centre["correlated_centre_history_norm_upper"]
        if isinstance(centre["correlated_centre_history_norm_upper"], gmpy2.mpfr)
        else int(centre["correlated_centre_history_norm_upper"])
    )
    # The exact covector annihilates the exact phase tangent.  Compare the
    # nonphase guide with the exact nonphase history; removing the stored
    # tau_qq*xdot term costs its explicit history norm below.
    centre_nonphase_radius = (
        centre_upper + tau_qq * point(xdot_bound)
    )
    correlated_row_error = history_measure_difference * centre_nonphase_radius

    voltage_modes = len(data.prepared.modes)
    voltage_l2_center = point(
        _adjoint_component_l2_upper(
            data.left_finite[:voltage_modes], tail_v, precision
        )
    )
    voltage_l2_exact = voltage_l2_center + adjoint_error
    recovery_l2_center = point(
        _adjoint_component_l2_upper(
            data.left_finite[voltage_modes:], tail_w, precision
        )
    )
    recovery_l2_exact = recovery_l2_center + adjoint_error
    maximum_voltage_source_residual = point(
        max(
            residual["voltage_residual_upper"]
            + tube_row["model_voltage_residual_upper"]
            for residual, tube_row in zip(
                residual_rows, tube, strict=True
            )
            if isinstance(residual["voltage_residual_upper"], gmpy2.mpfr)
            and isinstance(
                tube_row["model_voltage_residual_upper"], gmpy2.mpfr
            )
        )
    )
    maximum_recovery_source_residual = point(
        max(
            residual["recovery_residual_upper"]
            for residual in residual_rows
            if isinstance(residual["recovery_residual_upper"], gmpy2.mpfr)
        )
    )
    root_upper = point(data.root) + root_error
    covariance = _exp_real(root_upper) * (period + period_error)
    vqq_continuous_source_action_error = covariance * (
        voltage_l2_exact * maximum_voltage_source_residual
        + recovery_l2_exact * maximum_recovery_source_residual
    )

    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        seam_p_sum = gmpy2.mpfr(0, precision)
        for row in tube[1:]:
            jump = row["center_jump_upper"]
            if not isinstance(jump, gmpy2.mpfr):
                raise TypeError("a V_qq seam jump lost its directed radius")
            seam_p_sum += jump
    p11 = DirectedInterval.from_decimal(P11.numerator, precision) / P11.denominator
    p12 = DirectedInterval.from_decimal(P12.numerator, precision) / P12.denominator
    p22 = DirectedInterval.from_decimal(P22.numerator, precision) / P22.denominator
    determinant = p11 * p22 - p12**2
    seam_coordinate_factor = max(
        (p22 / determinant).sqrt().upper,
        (p11 / determinant).sqrt().upper,
    )
    vqq_seam_action_error = (
        _exp_real(root_upper)
        * adjoint_norm
        * point(seam_coordinate_factor)
        * point(seam_p_sum)
    )

    event_and_q_action_error = measure_norm * (
        udot_history_error + xddot_history_error + q_center_history_error
    )
    guide_action, guide_action_tail = _directed_guide_history_action(
        data, cells, tail_v, tail_w
    )
    centre_nonphase_correction_action = (
        2 * complex_value("tau_q") * complex_value("f_udot")
        + complex_value("tau_q") ** 2 * complex_value("f_xddot")
        - complex_value("quotient") * complex_value("f_q_history")
    )
    guide_identity_interval = guide_action + _complex_point(
        centre_nonphase_correction_action, precision
    )
    center_adjoint_inhomogeneous_identity_defect = (
        point(guide_identity_interval.upper_abs())
        + positive_interval(SCALAR_TRANSCRIPTION_GUARD)
    )
    correlated_action_error = (
        correlated_row_error
        + vqq_continuous_source_action_error
        + vqq_seam_action_error
        + event_and_q_action_error
        + center_adjoint_inhomogeneous_identity_defect
    )
    quotient_error = correlated_action_error / point(f_q_lower)
    stable_history_error = base_nonquotient_history_error + (
        point(q_bound) + q_error
    ) * quotient_error
    deflated_history_upper = centre_upper + stable_history_error
    normalized_upper = deflated_history_upper / point(q_norm_lower) ** 2
    target_unscaled = point(12) * point(q_norm_lower) ** 2
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        target_margin = target_unscaled.lower - deflated_history_upper.upper

    return {
        "coefficient_operator_variation_upper": coefficient_variation.upper,
        "finite_adjoint_l1_error_upper": finite_error.upper,
        "adjoint_tail_l1_error_upper": adjoint_tail_error.upper,
        "complete_adjoint_l1_error_upper": adjoint_error.upper,
        "adjoint_history_action_factor_upper": action_factor.upper,
        "density_convolution_rounding_guard_upper": (
            density_convolution_rounding_guard.upper
        ),
        "adjoint_density_basis_shift_upper": (
            adjoint_density_basis_shift.upper
        ),
        "history_measure_difference_upper": history_measure_difference.upper,
        "voltage_adjoint_parseval_l2_center_upper": voltage_l2_center.upper,
        "voltage_adjoint_parseval_l2_exact_upper": voltage_l2_exact.upper,
        "recovery_adjoint_parseval_l2_center_upper": recovery_l2_center.upper,
        "recovery_adjoint_parseval_l2_exact_upper": recovery_l2_exact.upper,
        "maximum_voltage_source_residual_upper": maximum_voltage_source_residual.upper,
        "maximum_recovery_source_residual_upper": maximum_recovery_source_residual.upper,
        "physical_floquet_covariance_upper": covariance.upper,
        "vqq_continuous_source_action_error_upper": vqq_continuous_source_action_error.upper,
        "vqq_seam_p_radius_sum_upper": seam_p_sum,
        "vqq_seam_coordinate_factor_upper": seam_coordinate_factor,
        "vqq_seam_action_error_upper": vqq_seam_action_error.upper,
        "event_and_q_action_error_upper": event_and_q_action_error.upper,
        "correlated_adjoint_row_error_upper": correlated_row_error.upper,
        "direct_guide_history_action_tail_upper": guide_action_tail,
        "center_adjoint_inhomogeneous_identity_defect_upper": (
            center_adjoint_inhomogeneous_identity_defect.upper
        ),
        "correlated_action_error_upper": correlated_action_error.upper,
        "f_q_error_upper": f_q_error.upper,
        "f_q_history_identity_defect_upper": f_q_history_identity_defect,
        "f_q_modulus_lower": f_q_lower,
        "tau_q_error_upper": tau_q_error.upper,
        "vqq_p_error_upper": vqq_p_error.upper,
        "vqq_coordinate_error_upper": vqq_coordinate_error.upper,
        "event_core_error_upper": event_core_error.upper,
        "tau_qq_error_upper": tau_qq_error.upper,
        "quotient_error_upper": quotient_error.upper,
        "base_nonquotient_history_error_upper": base_nonquotient_history_error.upper,
        "stable_history_error_upper": stable_history_error.upper,
        "q_section_norm_lower": q_norm_lower,
        "correlated_deflated_history_upper": deflated_history_upper.upper,
        "normalized_stable_output_uu_upper": normalized_upper.upper,
        "target_unscaled_upper": target_unscaled.upper,
        "target_unscaled_margin_lower": target_margin,
    }


@dataclass(frozen=True)
class Stage4EArtifact:
    schema_id: str
    model_id: str
    branch: str
    parent_result_sha256: dict[str, str]
    physical_time_grid: dict[str, object]
    directed_vqq_residual: dict[str, object]
    directed_vqq_tube: dict[str, object]
    continuous_history_correlated_deflation: dict[str, object]
    base_orbit_stable_output_uu: dict[str, object]
    stage4b_conditional_substitution: dict[str, object]
    exact_remaining_gates: dict[str, object]
    claim_status: dict[str, bool]


def _sha256_path(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def canonical_sha256(value: object) -> str:
    return sha256(
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        ).encode("ascii")
    ).hexdigest()


def _upper_text(value: gmpy2.mpfr, digits: int = 64) -> str:
    return decimal_upper(value, digits)


def _lower_text(value: gmpy2.mpfr, digits: int = 64) -> str:
    return decimal_lower(value, digits)


def _directed_rows_digest(
    rows: Iterable[Mapping[str, gmpy2.mpfr | int]],
) -> str:
    serial: list[dict[str, str | int]] = []
    for row in rows:
        converted: dict[str, str | int] = {}
        for key, value in sorted(row.items()):
            converted[key] = (
                int(value) if isinstance(value, int) else _upper_text(value)
            )
        serial.append(converted)
    return canonical_sha256(serial)


def _load_bound_parent(
    repository: Path,
    relative: str,
    expected_hash: str,
    label: str,
) -> Mapping[str, object]:
    raw = (repository / relative).read_bytes()
    if sha256(raw).hexdigest() != expected_hash:
        raise ValueError(f"the bound {label} result changed")
    payload = json.loads(raw)
    if not isinstance(payload, Mapping):
        raise ValueError(f"the bound {label} result is malformed")
    return payload


def _binary_algebra_guard_certificate() -> dict[str, object]:
    """Record the analytic IEEE guard used around finite centre algebra.

    The expression tree in :func:`_centre_data` contains fewer than five
    million scalar real operations after expanding every dictionary
    convolution.  All expression-tree Wiener envelopes are below ten.  The
    deliberately cruder product ``N*u*M`` plus every possible trim omission
    is below the declared ``1e-8`` ingress.  This certificate is independent
    of mesh refinement and is checked numerically with outward MPFR.
    """

    precision = PRECISION_BITS
    operation_cap = 5_000_000
    intermediate_envelope = 10
    unit_roundoff = DirectedInterval.from_decimal(1, precision) / 2**53
    roundoff = (
        DirectedInterval.from_decimal(operation_cap, precision)
        * unit_roundoff
        * intermediate_envelope
    )
    trim = (
        DirectedInterval.from_decimal(operation_cap, precision)
        * DirectedInterval.from_decimal("1e-18", precision)
        * _exp_real(
            DirectedInterval.from_float(2 * EIGENCOLUMN_CENTER, precision)
        )
    )
    total = roundoff + trim
    if total.upper >= DirectedInterval.from_decimal("1e-8", precision).lower:
        raise ArithmeticError("the binary centre-algebra guard no longer closes")
    return {
        "audited_expanded_real_operation_count": 4_500_470,
        "expanded_real_operation_count_cap": operation_cap,
        "audited_maximum_intermediate_wiener_l1_binary64": (
            "2.6791342024153457"
        ),
        "expression_tree_wiener_envelope_cap": str(intermediate_envelope),
        "binary64_unit_roundoff": "2^-53",
        "roundoff_accumulation_upper": _upper_text(roundoff.upper),
        "all_trim_omissions_upper": _upper_text(trim.upper),
        "combined_binary_and_trim_upper": _upper_text(total.upper),
        "declared_guard": "1e-8",
        "guard_closes": True,
        "mesh_spread_used": False,
    }


def build_stage4e_artifact(repository: Path) -> Stage4EArtifact:
    repository = repository.resolve()
    stage3 = _load_bound_parent(
        repository,
        STAGE3_RESULT_RELATIVE_PATH,
        STAGE3_RESULT_SHA256,
        "Stage-3 stable projection",
    )
    stage4b = _load_bound_parent(
        repository,
        STAGE4B_RESULT_RELATIVE_PATH,
        STAGE4B_RESULT_SHA256,
        "Stage-4B graph contract",
    )
    stage4d = _load_bound_parent(
        repository,
        STAGE4D_RESULT_RELATIVE_PATH,
        STAGE4D_RESULT_SHA256,
        "Stage-4D adjoint bridge",
    )
    validate_stage3_stable_projection_result(stage3, repository)
    validate_stage4b_contract_result(stage4b, repository)
    validate_stage4d_result(stage4d, repository)

    data = _centre_data(repository)
    cells = _guide(data)
    uncertainty = _model_uncertainty(data)
    algebra = _binary_algebra_guard_certificate()
    residual_rows = _directed_residual_rows(data, cells)
    tube_rows = _directed_vqq_tube(
        data, cells, residual_rows, uncertainty
    )
    tail_v, tail_w, tail_norms = _row_tail_neumann(data)
    event = _event_centre(data, cells, tail_v, tail_w)
    centre = _directed_centre_deflated_upper(data, cells, event)
    budget = _directed_correlated_error_budget(
        data,
        cells,
        residual_rows,
        event,
        tube_rows,
        uncertainty,
        centre,
        tail_v,
        tail_w,
    )
    if budget["normalized_stable_output_uu_upper"] >= gmpy2.mpfr(12):
        raise ArithmeticError("the Stage-4E base-orbit C_s^uu target failed")
    if budget["target_unscaled_margin_lower"] <= 0:
        raise ArithmeticError("the Stage-4E unscaled target margin vanished")

    worst_residual = max(
        residual_rows,
        key=lambda row: row["voltage_residual_upper"],
    )
    worst_tube = max(tube_rows, key=lambda row: row["maximum_radius"])
    final_tube = tube_rows[-1]
    stage4b_artifact = stage4b["artifact"]
    design = stage4b_artifact["design_target_matrix_evaluation"]
    targets = stage4b_artifact["coarse_other_block_interface"][
        "simultaneous_safe_design_targets"
    ]
    claims = {name: True for name in TRUE_FLAGS}
    claims.update({name: False for name in FALSE_FLAGS})
    return Stage4EArtifact(
        schema_id=SCHEMA_ID,
        model_id=MODEL_ID,
        branch=BRANCH,
        parent_result_sha256={
            STAGE3_RESULT_RELATIVE_PATH: STAGE3_RESULT_SHA256,
            STAGE4B_RESULT_RELATIVE_PATH: STAGE4B_RESULT_SHA256,
            STAGE4D_RESULT_RELATIVE_PATH: STAGE4D_RESULT_SHA256,
        },
        physical_time_grid={
            "time_variable": "physical time",
            "taylor_degree": TAYLOR_DEGREE,
            "delay_grid_divisor": DELAY_GRID_DIVISOR,
            "tau0_aligned_cell_count": 512,
            "tau1_aligned_cell_count": 640,
            "full_cell_count_plus_final_short_cell": len(cells),
            "regular_step_binary64": format(data.tau0 / DELAY_GRID_DIVISOR, ".17g"),
            "period_binary64": format(data.period, ".17g"),
            "exact_binary_delay_alignment_checked": True,
            "interval_precision_bits": PRECISION_BITS,
            "binary_algebra_guard_certificate": algebra,
        },
        directed_vqq_residual={
            "cell_count": len(residual_rows),
            "maximum_voltage_residual_upper": _upper_text(
                worst_residual["voltage_residual_upper"]
            ),
            "maximum_voltage_residual_cell_index": int(
                worst_residual["cell_index"]
            ),
            "maximum_recovery_residual_upper": _upper_text(
                max(row["recovery_residual_upper"] for row in residual_rows)
            ),
            "maximum_analytic_tail_upper": _upper_text(
                max(row["analytic_tail_upper"] for row in residual_rows)
            ),
            "validation_trim_threshold": format(
                VALIDATION_TRIM_THRESHOLD, ".17g"
            ),
            "omitted_coefficients_added_before_norm": True,
            "taylor_bernstein_outward_mpfr": True,
            "row_digest_sha256": _directed_rows_digest(residual_rows),
        },
        directed_vqq_tube={
            "norm": "P norm for the two current coordinates",
            "delayed_source_radii_propagated_cell_by_cell": True,
            "p_logarithmic_norm_propagation": True,
            "maximum_p_radius_upper": _upper_text(
                worst_tube["maximum_radius"]
            ),
            "maximum_p_radius_cell_index": int(worst_tube["cell_index"]),
            "final_endpoint_p_radius_upper": _upper_text(
                final_tube["endpoint_radius"]
            ),
            "voltage_coordinate_radius_upper": _upper_text(
                budget["vqq_coordinate_error_upper"]
            ),
            "mesh_spread_used_as_error": False,
            "row_digest_sha256": _directed_rows_digest(tube_rows),
        },
        continuous_history_correlated_deflation={
            "history_space": "C([-tau_max,0],R) x R",
            "history_components_retained": (
                "voltage history on 641 intersected cells and current recovery only"
            ),
            "evaluation_order": (
                "form Y_qq-c*q with c=f(Y_qq)/f(q), then take the "
                "continuous-history norm"
            ),
            "quotient_residual_identity": (
                "f(Y_qq)/f(q)-c=f(Y_qq-c*q)/f(q)"
            ),
            "same_adjoint_coefficients_in_numerator_and_denominator": True,
            "independent_num_den_triangle_bound_used": False,
            "advanced_adjoint_physical_covariance_factor_used": "exp(s)*T",
            "voltage_covector_time_integral_bound": (
                "Parseval l2 of the same advanced-adjoint Fourier row"
            ),
            "center_correlated_history_upper": _upper_text(
                centre["correlated_centre_history_norm_upper"]
            ),
            "center_maximum_history_cell_index": int(
                centre["maximum_cell_index"]
            ),
            "center_current_recovery_abs_upper": _upper_text(
                centre["current_recovery_abs_upper"]
            ),
            "current_voltage_atom_modulus_upper": stage4d["artifact"][
                "continuous_history_measure_enclosure"
            ]["current_voltage_atom_modulus_upper"],
            "current_recovery_atom_modulus_upper": stage4d["artifact"][
                "continuous_history_measure_enclosure"
            ]["current_recovery_atom_modulus_upper"],
            "voltage_history_density_total_variation_upper": stage4d[
                "artifact"
            ]["continuous_history_measure_enclosure"][
                "voltage_history_density_total_variation_upper"
            ],
            "finite_adjoint_l1_error_upper": _upper_text(
                budget["finite_adjoint_l1_error_upper"]
            ),
            "adjoint_fourier_tail_l1_error_upper": _upper_text(
                budget["adjoint_tail_l1_error_upper"]
            ),
            "complete_adjoint_l1_error_upper": _upper_text(
                budget["complete_adjoint_l1_error_upper"]
            ),
            "density_convolution_rounding_guard_upper": _upper_text(
                budget["density_convolution_rounding_guard_upper"]
            ),
            "adjoint_density_basis_shift_upper": _upper_text(
                budget["adjoint_density_basis_shift_upper"]
            ),
            "history_measure_difference_upper": _upper_text(
                budget["history_measure_difference_upper"]
            ),
            "voltage_adjoint_parseval_l2_exact_upper": _upper_text(
                budget["voltage_adjoint_parseval_l2_exact_upper"]
            ),
            "recovery_adjoint_parseval_l2_exact_upper": _upper_text(
                budget["recovery_adjoint_parseval_l2_exact_upper"]
            ),
            "maximum_voltage_guide_plus_model_source_residual_upper": _upper_text(
                budget["maximum_voltage_source_residual_upper"]
            ),
            "maximum_recovery_guide_source_residual_upper": _upper_text(
                budget["maximum_recovery_source_residual_upper"]
            ),
            "vqq_continuous_source_action_error_upper": _upper_text(
                budget["vqq_continuous_source_action_error_upper"]
            ),
            "vqq_seam_p_radius_sum_upper": _upper_text(
                budget["vqq_seam_p_radius_sum_upper"]
            ),
            "vqq_seam_action_error_upper": _upper_text(
                budget["vqq_seam_action_error_upper"]
            ),
            "event_and_q_action_error_upper": _upper_text(
                budget["event_and_q_action_error_upper"]
            ),
            "correlated_adjoint_row_error_upper": _upper_text(
                budget["correlated_adjoint_row_error_upper"]
            ),
            "direct_guide_history_action_tail_upper": _upper_text(
                budget["direct_guide_history_action_tail_upper"]
            ),
            "center_adjoint_inhomogeneous_identity_defect_upper": _upper_text(
                budget[
                    "center_adjoint_inhomogeneous_identity_defect_upper"
                ]
            ),
            "total_correlated_action_error_upper": _upper_text(
                budget["correlated_action_error_upper"]
            ),
            "f_q_error_upper": _upper_text(budget["f_q_error_upper"]),
            "f_q_history_vs_lprime_identity_defect_upper": _upper_text(
                budget["f_q_history_identity_defect_upper"]
            ),
            "f_q_modulus_lower": _lower_text(budget["f_q_modulus_lower"]),
            "quotient_error_upper": _upper_text(
                budget["quotient_error_upper"]
            ),
        },
        base_orbit_stable_output_uu={
            "scope": (
                "one validated periodic base orbit and its normalized Route-C "
                "unstable direction; not uniform on the split ball"
            ),
            "q_section_norm_lower": _lower_text(
                budget["q_section_norm_lower"]
            ),
            "correlated_deflated_history_upper": _upper_text(
                budget["correlated_deflated_history_upper"]
            ),
            "stable_history_error_upper": _upper_text(
                budget["stable_history_error_upper"]
            ),
            "normalized_stable_output_uu_upper": _upper_text(
                budget["normalized_stable_output_uu_upper"]
            ),
            "design_target": "12",
            "unscaled_target_upper": _upper_text(
                budget["target_unscaled_upper"]
            ),
            "unscaled_target_margin_lower": _lower_text(
                budget["target_unscaled_margin_lower"]
            ),
            "strictly_below_twelve": True,
            "uniform_split_ball_statement": False,
        },
        stage4b_conditional_substitution={
            "status": (
                "conditional arithmetic only: insert the Stage-4E base-orbit "
                "C_s^uu upper below the Stage-4B design target 12 while "
                "retaining the five unvalidated design targets"
            ),
            "five_other_design_targets": {
                key: value
                for key, value in targets.items()
                if key != "stable_output_uu_upper"
            },
            "stage4e_value_is_not_a_uniform_block_bound": True,
            "conditional_perron_root_upper": design["perron_root_upper"],
            "conditional_weighted_row_sum_upper": design[
                "weighted_row_sum_upper"
            ],
            "conditional_graph_derivative_upper": design[
                "graph_derivative_upper"
            ],
            "conditional_graph_height_upper": design["graph_height_upper"],
            "conditional_split_ball_radius": "0.0017",
            "conditional_matrix_closes": True,
            "strict_stage4b_certificate_closes": False,
        },
        exact_remaining_gates={
            "minimal_scope_upgrade": (
                "inflate the same physical-time correlated calculation "
                "uniformly over the radius-0.0017 split return tube"
            ),
            "other_five_hessian_blocks": (
                "stable ss, stable su, unstable ss, unstable su, unstable uu"
            ),
            "stable_power_constant_upper": None,
            "validated_split_return_ball_radius_lower": None,
            "return_tube_history_radius_upper": None,
            "first_positive_return_time_interval": None,
            "uniform_event_speed_lower": None,
            "uniform_ball_block_bounds_validated": False,
            "stable_power_validated": False,
            "split_return_tube_validated": False,
            "six_block_graph_transform_validated": False,
            "structural_correlated_cancellation_failure_found": False,
        },
        claim_status=claims,
    )


def build_stage4e_result(repository: Path) -> dict[str, object]:
    repository = repository.resolve()
    artifact = asdict(build_stage4e_artifact(repository))
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
            "parent_result_sha256": dict(artifact["parent_result_sha256"]),
            "environment": {
                "python": platform.python_version(),
                "platform": platform.platform(),
                "numpy": np.__version__,
                "gmpy2": gmpy2.version(),
                "mpfr": gmpy2.mpfr_version(),
                "openblas_num_threads": os.environ.get("OPENBLAS_NUM_THREADS"),
                "omp_num_threads": os.environ.get("OMP_NUM_THREADS"),
                "mpfr_precision_bits": PRECISION_BITS,
            },
        },
    }


def validate_stage4e_result(
    payload: Mapping[str, object], repository: Path
) -> None:
    if not isinstance(payload, Mapping) or set(payload) != {"artifact", "manifest"}:
        raise ValueError("the Stage-4E result has the wrong outer schema")
    artifact = payload.get("artifact")
    manifest = payload.get("manifest")
    if not isinstance(artifact, Mapping) or not isinstance(manifest, Mapping):
        raise ValueError("the Stage-4E artifact or manifest is missing")
    if set(artifact) != {field.name for field in fields(Stage4EArtifact)}:
        raise ValueError("the Stage-4E artifact schema changed")
    if (
        artifact.get("schema_id") != SCHEMA_ID
        or artifact.get("model_id") != MODEL_ID
        or artifact.get("branch") != BRANCH
    ):
        raise ValueError("the Stage-4E identity changed")
    claims = artifact.get("claim_status")
    if not isinstance(claims, Mapping):
        raise ValueError("the Stage-4E claim ledger is missing")
    if set(claims) != set(TRUE_FLAGS) | set(FALSE_FLAGS):
        raise ValueError("the Stage-4E claim ledger changed")
    if any(claims.get(name) is not True for name in TRUE_FLAGS):
        raise ValueError("a proved Stage-4E base-orbit statement was weakened")
    if any(claims.get(name) is not False for name in FALSE_FLAGS):
        raise ValueError("an open Stage-4E theorem gate was promoted")

    grid = artifact.get("physical_time_grid")
    residual = artifact.get("directed_vqq_residual")
    tube = artifact.get("directed_vqq_tube")
    correlated = artifact.get("continuous_history_correlated_deflation")
    base = artifact.get("base_orbit_stable_output_uu")
    conditional = artifact.get("stage4b_conditional_substitution")
    remaining = artifact.get("exact_remaining_gates")
    if not all(
        isinstance(value, Mapping)
        for value in (grid, residual, tube, correlated, base, conditional, remaining)
    ):
        raise ValueError("a Stage-4E certificate block is missing")
    assert isinstance(grid, Mapping)
    assert isinstance(residual, Mapping)
    assert isinstance(tube, Mapping)
    assert isinstance(correlated, Mapping)
    assert isinstance(base, Mapping)
    assert isinstance(conditional, Mapping)
    assert isinstance(remaining, Mapping)
    algebra = grid.get("binary_algebra_guard_certificate")
    if (
        grid.get("time_variable") != "physical time"
        or grid.get("tau0_aligned_cell_count") != 512
        or grid.get("tau1_aligned_cell_count") != 640
        or grid.get("full_cell_count_plus_final_short_cell") != 1042
        or grid.get("exact_binary_delay_alignment_checked") is not True
        or not isinstance(algebra, Mapping)
        or algebra.get("guard_closes") is not True
        or algebra.get("mesh_spread_used") is not False
    ):
        raise ValueError("the Stage-4E physical-time grid changed")
    if (
        residual.get("cell_count") != 1042
        or residual.get("taylor_bernstein_outward_mpfr") is not True
        or residual.get("omitted_coefficients_added_before_norm") is not True
        or gmpy2.mpq(str(residual["maximum_voltage_residual_upper"]))
        >= gmpy2.mpq("2.6e-7")
    ):
        raise ValueError("the Stage-4E directed residual changed")
    if (
        tube.get("delayed_source_radii_propagated_cell_by_cell") is not True
        or tube.get("p_logarithmic_norm_propagation") is not True
        or tube.get("mesh_spread_used_as_error") is not False
        or gmpy2.mpq(str(tube["maximum_p_radius_upper"]))
        >= gmpy2.mpq("0.0082")
    ):
        raise ValueError("the Stage-4E V_qq tube changed")
    if (
        correlated.get("same_adjoint_coefficients_in_numerator_and_denominator")
        is not True
        or correlated.get("independent_num_den_triangle_bound_used") is not False
        or gmpy2.mpq(
            str(
                correlated[
                    "center_adjoint_inhomogeneous_identity_defect_upper"
                ]
            )
        )
        <= 0
        or gmpy2.mpq(str(correlated["history_measure_difference_upper"]))
        <= 0
        or gmpy2.mpq(str(correlated["adjoint_density_basis_shift_upper"]))
        <= 0
        or gmpy2.mpq(str(correlated["history_measure_difference_upper"]))
        >= gmpy2.mpq("1e-6")
        or gmpy2.mpq(str(correlated["vqq_seam_action_error_upper"])) <= 0
        or gmpy2.mpq(str(correlated["total_correlated_action_error_upper"]))
        >= gmpy2.mpq("8e-6")
        or gmpy2.mpq(str(correlated["f_q_modulus_lower"])) <= 0
    ):
        raise ValueError("the Stage-4E correlated action changed")
    if (
        base.get("strictly_below_twelve") is not True
        or base.get("uniform_split_ball_statement") is not False
        or gmpy2.mpq(str(base["normalized_stable_output_uu_upper"]))
        >= gmpy2.mpq("12")
        or gmpy2.mpq(str(base["unscaled_target_margin_lower"])) <= 0
    ):
        raise ValueError("the Stage-4E base-orbit output changed")
    if (
        conditional.get("stage4e_value_is_not_a_uniform_block_bound") is not True
        or conditional.get("conditional_matrix_closes") is not True
        or conditional.get("strict_stage4b_certificate_closes") is not False
        or remaining.get("uniform_ball_block_bounds_validated") is not False
        or remaining.get("stable_power_validated") is not False
        or remaining.get("split_return_tube_validated") is not False
        or remaining.get("six_block_graph_transform_validated") is not False
    ):
        raise ValueError("an open Stage-4B gate was promoted")

    expected_parents = {
        STAGE3_RESULT_RELATIVE_PATH: STAGE3_RESULT_SHA256,
        STAGE4B_RESULT_RELATIVE_PATH: STAGE4B_RESULT_SHA256,
        STAGE4D_RESULT_RELATIVE_PATH: STAGE4D_RESULT_SHA256,
    }
    expected_manifest_fields = {
        "schema_id",
        "result",
        "default_command",
        "arithmetic_scope",
        "artifact_sha256",
        "source_sha256",
        "parent_result_sha256",
        "environment",
    }
    if set(manifest) != expected_manifest_fields:
        raise ValueError("the Stage-4E manifest schema changed")
    fixed = {
        "schema_id": SCHEMA_ID,
        "result": RESULT_RELATIVE_PATH,
        "default_command": DEFAULT_COMMAND,
        "arithmetic_scope": ARITHMETIC_SCOPE,
        "artifact_sha256": canonical_sha256(artifact),
        "parent_result_sha256": expected_parents,
    }
    if any(manifest.get(key) != value for key, value in fixed.items()):
        raise ValueError("the Stage-4E manifest fixed data changed")
    if artifact.get("parent_result_sha256") != expected_parents:
        raise ValueError("the Stage-4E artifact parent binding changed")
    repository = repository.resolve()
    sources = manifest.get("source_sha256")
    if not isinstance(sources, Mapping) or set(sources) != set(SOURCE_MANIFEST):
        raise ValueError("the Stage-4E source set changed")
    for relative in SOURCE_MANIFEST:
        if sources.get(relative) != _sha256_path(repository / relative):
            raise ValueError(f"the Stage-4E source changed: {relative}")
    for relative, digest in expected_parents.items():
        if _sha256_path(repository / relative) != digest:
            raise ValueError(f"the Stage-4E parent changed: {relative}")


def centre_diagnostic(repository: Path) -> dict[str, object]:
    """Return the non-promoted centre calculation used to design Stage 4E."""

    data = _centre_data(repository)
    cells = _guide(data)
    tail_v, tail_w, tail_norms = _row_tail_neumann(data)
    pairing = _lprime_pairing(data, tail_v, tail_w)
    forcing_action = _forcing_action(data, tail_v)
    event = _event_centre(data, cells, tail_v, tail_w)
    theta = np.linspace(-data.tau1, 0.0, 20001)
    q_values = np.asarray(
        [_evaluate(data.qsection_v, float(time), data.period, data.root) for time in theta]
    )
    return {
        "period": format(data.period, ".17g"),
        "root": format(data.root, ".17g"),
        "cell_count": len(cells),
        "maximum_guide_residual_l1_binary64": format(max(cell.residual_l1 for cell in cells), ".17g"),
        "maximum_analytic_tail_upper_binary64": format(max(cell.analytic_tail_upper for cell in cells), ".17g"),
        "forcing_dictionary_cardinality": len(data.forcing),
        "q_section_sampled_norm_binary64": format(float(np.max(np.abs(q_values))), ".17g"),
        "q_section_sampled_argmax_time_binary64": format(float(theta[int(np.argmax(np.abs(q_values)))]), ".17g"),
        "adjoint_tail_neumann_l1_rows_binary64": [format(value, ".17g") for value in tail_norms],
        "adjoint_tail_final_support": len(set(tail_v) | set(tail_w)),
        "lprime_pairing_binary64": {
            "real": format(pairing.real, ".17g"),
            "imag": format(pairing.imag, ".17g"),
            "abs": format(abs(pairing), ".17g"),
        },
        "f_of_v_qq_via_inhomogeneous_identity_binary64": {
            "real": format(forcing_action.real, ".17g"),
            "imag": format(forcing_action.imag, ".17g"),
            "abs": format(abs(forcing_action), ".17g"),
        },
        "final_v_qq_current_binary64": {
            "real": format(complex(np.sum(cells[-1].voltage)).real, ".17g"),
            "imag": format(complex(np.sum(cells[-1].voltage)).imag, ".17g"),
        },
        "event_centre_binary64": {
            key: (
                {"real": format(value.real, ".17g"), "imag": format(value.imag, ".17g"), "abs": format(abs(value), ".17g")}
                if isinstance(value, complex)
                else (format(value, ".17g") if isinstance(value, float) else value)
            )
            for key, value in event.items()
            if key not in {"correction_v", "correction_w"}
        },
        "theorem_status": "diagnostic centre only; no interval error is inferred from it",
    }


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
    "Stage4EArtifact",
    "TRUE_FLAGS",
    "build_stage4e_artifact",
    "build_stage4e_result",
    "canonical_sha256",
    "centre_diagnostic",
    "validate_stage4e_result",
]
