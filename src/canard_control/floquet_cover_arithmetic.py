"""Shared directed arithmetic for Fourier Floquet covers.

This module contains only phase-placement-neutral arithmetic.  In
particular, :func:`_rotation_data` evaluates diagonal Fourier shift factors;
it does not attach them to an operator row or column.  A delayed convolution
``H S_alpha`` must apply those factors to the input Fourier mode (the matrix
column), and each theorem module is required to test that identity directly.

The binary FFT, BLAS, and transcendental outputs produced here are never
treated as rigorous by themselves.  Consumers compare FFT/transcendental
values with MPFR boxes and use the explicit four-real-GEMM error model below.
"""

from __future__ import annotations

import ctypes
import math
from typing import Any, Mapping

import gmpy2
import numpy as np

from canard_control.directed_interval import (
    DirectedComplexInterval,
    DirectedInterval,
    complex_unit_interval,
    upward_sum,
)


def _binary_environment_checked() -> None:
    """Require IEEE binary64, gradual underflow, and round-to-nearest."""

    info = np.finfo(float)
    if not (
        info.bits == 64
        and info.nmant == 52
        and info.eps == 2.0**-52
        and np.nextafter(0.0, 1.0)
        == float.fromhex("0x0.0000000000001p-1022")
    ):
        raise RuntimeError("the Floquet accelerator requires IEEE binary64")
    process = ctypes.CDLL(None)
    if not hasattr(process, "fegetround"):
        raise RuntimeError("cannot audit the host floating rounding mode")
    process.fegetround.restype = ctypes.c_int
    if process.fegetround() != 0:
        raise RuntimeError("binary Floquet products require round-to-nearest")


def _box_distance_split_upper(
    value: DirectedComplexInterval,
    center: complex,
) -> gmpy2.mpfr:
    """Directed split distance from a complex interval to a binary point."""

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


def _up(value: object, precision: int) -> gmpy2.mpfr:
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        return gmpy2.mpfr(value)


def _exp_interval(value: DirectedInterval) -> DirectedInterval:
    with gmpy2.context(precision=value.precision, round=gmpy2.RoundDown):
        lower = gmpy2.exp(value.lower)
    with gmpy2.context(precision=value.precision, round=gmpy2.RoundUp):
        upper = gmpy2.exp(value.upper)
    return DirectedInterval(lower, upper, value.precision)


def _binary_complex_split_upper(
    value: complex,
    precision: int,
) -> gmpy2.mpfr:
    """Directed split norm of one stored binary64 complex number."""

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
    """Directed maximum of stored componentwise split norms."""

    stored_values = np.asarray(values, dtype=complex)
    if not np.all(np.isfinite(stored_values)):
        raise ValueError("a binary complex split bound requires finite values")
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


def _binary_coefficients(
    orbit: Any,
) -> tuple[dict[int, complex], dict[int, complex]]:
    """Return the stored-center fast-row coefficient convolutions.

    The result consists of the instantaneous coefficient and one of the two
    identical delayed-slot coefficients.  FFT and convolution rounding is
    intentionally left visible for a consumer to compare with its directed
    coefficient boxes.
    """

    voltage = np.asarray(orbit.state[:, 0], dtype=float)
    count = len(voltage)
    half = count // 2
    interpolation_modes = np.concatenate(
        (np.arange(half + 1), np.arange(-half, 0))
    )
    voltage_map = dict(
        zip(
            interpolation_modes,
            np.fft.fft(voltage) / count,
            strict=True,
        )
    )
    ordered = np.asarray(
        [voltage_map[k] for k in range(-half, half + 1)],
        dtype=complex,
    )
    centered = ordered.copy()
    centered[half] -= 1.0
    voltage_squared = np.convolve(ordered, ordered)
    centered_squared = np.convolve(centered, centered)
    modes = range(-2 * half, 2 * half + 1)
    parameters = orbit.parameters
    current = (
        -voltage_squared
        - 3.0
        * parameters.epsilon
        * parameters.kappa_3
        * centered_squared
    )
    delayed = (
        3.0
        * parameters.epsilon
        * parameters.kappa_3
        * centered_squared
        / 2.0
    )
    current[2 * half] += 1.0 - parameters.epsilon * parameters.kappa_1
    delayed[2 * half] += parameters.epsilon * parameters.kappa_1 / 2.0
    return (
        dict(zip(modes, current, strict=True)),
        dict(zip(modes, delayed, strict=True)),
    )


def _coefficient_matrix(
    output_modes: np.ndarray,
    input_modes: np.ndarray,
    coefficients: Mapping[int, complex],
) -> np.ndarray:
    """Form ``H[k-m]`` without applying a delay phase."""

    differences = output_modes[:, None] - input_modes[None, :]
    result = np.zeros(differences.shape, dtype=complex)
    for mode, value in coefficients.items():
        result[differences == mode] = value
    return result


def _formation_error(
    scale: gmpy2.mpfr,
    rows: int,
    precision: int,
) -> gmpy2.mpfr:
    """Conservative basic-binary-arithmetic forward error."""

    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        unit = gmpy2.mpfr(2) ** -53
        gamma = 1024 * unit / (1 - 1024 * unit)
        return gamma * scale + rows * 1024 * (gmpy2.mpfr(2) ** -1022)


def _binary_complex_matrix_split_l1_upper(
    matrix: np.ndarray,
    precision: int,
) -> gmpy2.mpfr:
    """Directed split-real majorant of a complex matrix l1 norm."""

    values = np.asarray(matrix, dtype=complex)
    if values.ndim != 2 or not np.all(np.isfinite(values)):
        raise ValueError("a binary complex norm requires a finite matrix")
    rows = values.shape[0]
    stored_columns = np.sum(
        np.abs(values.real) + np.abs(values.imag),
        axis=0,
        dtype=float,
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
    """Audit a complex binary product using four real GEMMs."""

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
    a_norm = (
        left_norm
        if left_norm is not None
        else _binary_complex_matrix_split_l1_upper(a, precision)
    )
    b_norm = (
        right_norm
        if right_norm is not None
        else _binary_complex_matrix_split_l1_upper(b, precision)
    )
    inner = a.shape[1]
    rows = a.shape[0]
    operations = 2 * inner + 5
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        unit = gmpy2.mpfr(2) ** -53
        gamma = operations * unit / (1 - operations * unit)
        underflow = 2 * rows * operations * (gmpy2.mpfr(2) ** -1022)
        return stored + gamma * a_norm * b_norm + underflow


def _rotation_data(
    mode_rotations: tuple[np.ndarray, np.ndarray],
    mode_rotation_split: tuple[gmpy2.mpfr, gmpy2.mpfr],
    mode_rotation_error: tuple[gmpy2.mpfr, gmpy2.mpfr],
    mode_binary_split: tuple[gmpy2.mpfr, gmpy2.mpfr],
    sigma: DirectedInterval,
    phase: DirectedInterval,
    base: Any,
    precision: int,
) -> tuple[tuple[np.ndarray, np.ndarray], gmpy2.mpfr, gmpy2.mpfr]:
    """Evaluate shift factors, without choosing their matrix axis."""

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
    return (
        (binary_by_delay[0], binary_by_delay[1]),
        maximum_split,
        maximum_error,
    )


__all__ = [
    "_binary_environment_checked",
    "_binary_coefficients",
    "_binary_complex_matrix_split_l1_upper",
    "_binary_complex_max_split_upper",
    "_binary_complex_product_split_l1_upper",
    "_binary_complex_split_upper",
    "_box_distance_split_upper",
    "_coefficient_matrix",
    "_exp_interval",
    "_formation_error",
    "_rotation_data",
    "_up",
]
