"""Validated continuation across the first target method-of-steps interval.

This module extends the single cell in
``fixed_epsilon_target_first_step_interval``.  It treats the interval
``-3 <= t <= 1``; throughout this interval every delayed argument is still
in the prescribed incoming history.  The delay-four argument enters the
degree-nine C4 Hermite patch when ``t >= 1/2`` and is evaluated here by
outward-rounded polynomial interval arithmetic, together with its exact
first two label derivatives.

The proof uses a fixed binary64 RK4 guide only to choose cubic Hermite
predictors.  The guide is never used as an enclosure.  On every time--label
cell three strict interval Picard arguments are performed in error
coordinates: one for the state at the central label, one for its first label
variation, and one for the second label variation on the whole label cell.
The state and first-variation families are then enclosed by the mean-value
identities

    z_lambda(t, lambda) = z_lambda(t, lambda_c)
                        + (lambda-lambda_c) z_lambdalambda(t, xi_1),
    z(t, lambda) = z(t, lambda_c)
                 + (lambda-lambda_c) z_lambda(t, xi_2).

All claim-bearing operations after the guide has been chosen use the MPFR
directed interval backend.  The public certificate accepts the grid only
after every strict closure test succeeds at both declared precisions.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from decimal import Decimal, InvalidOperation
from functools import lru_cache
from hashlib import sha256
import json
import math
from pathlib import Path
import platform
from typing import Any, Callable, Mapping, Sequence

import gmpy2
import sympy as sp

from canard_control.directed_interval import (
    DirectedInterval,
    decimal_lower,
    decimal_upper,
)
from canard_control.fixed_epsilon_target_c4_preparation_seam import (
    EXACT_ETA,
    EXACT_INCOMING_TIME,
    EXACT_NU,
    EXACT_PHASE_SHIFT,
    EXACT_RHO,
    EXACT_SECTION_HALF_WIDTH,
    EXACT_THETA,
    EXACT_TRANSVERSE,
    _unpatched_history_jet_algebra,
    c4_prepared_history_state,
    c4_prepared_history_transverse_derivative,
    exact_target_endpoint_jets,
    physical_field_time_derivative_from_jets,
    right_jet_shape,
)
from canard_control.fixed_epsilon_target_first_step_interval import (
    _entry_initial_box,
)


PRIMARY_PRECISION_BITS = 192
REFINEMENT_PRECISION_BITS = 256
TIME_LEFT = "-3"
TIME_RIGHT = "1"
TIME_STEP = "0.01"
LABEL_LEFT = "-0.05"
LABEL_RIGHT = "0.05"
LABEL_STEP = "0.005"
PATCH_ENTRY_TIME = "0.5"

MODEL_ID = "fixed-epsilon-target-first-method-step-interval-cover"
AUDIT_ID = "fixed-epsilon-target-first-method-step-interval-cover-v1"
PROOF_SOURCE_RELATIVE_PATH = (
    "src/canard_control/fixed_epsilon_target_first_step_cover.py"
)
GENERATOR_RELATIVE_PATH = (
    "experiments/fixed_epsilon_target_first_step_cover.py"
)
RESULT_RELATIVE_PATH = (
    "experiments/results/fixed_epsilon_target_first_step_cover.json"
)
NOTE_RELATIVE_PATH = "docs/fixed-epsilon-target-first-step-cover.md"
INTERVAL_BACKEND_SOURCE_RELATIVE_PATH = "src/canard_control/directed_interval.py"
C4_SEAM_SOURCE_RELATIVE_PATH = (
    "src/canard_control/fixed_epsilon_target_c4_preparation_seam.py"
)
SINGLE_CELL_SOURCE_RELATIVE_PATH = (
    "src/canard_control/fixed_epsilon_target_first_step_interval.py"
)
UNIVALENCE_GATE_SOURCE_RELATIVE_PATH = (
    "src/canard_control/fixed_epsilon_target_chart_univalence_gate.py"
)
PHYSICAL_MODEL_SOURCE_RELATIVE_PATH = (
    "src/canard_control/fixed_epsilon_frozen_graph_operator.py"
)
DEFAULT_COMMAND = (
    "PYTHONPATH=src /usr/bin/python3 "
    "experiments/fixed_epsilon_target_first_step_cover.py"
)
MANIFEST_ARITHMETIC = (
    "192-bit MPFR outward-rounded interval polynomials; exact power-to-"
    "Bernstein convex-hull bounds in normalized time; strict error-coordinate "
    "Picard inclusions for the central state, central true lambda variation, "
    "and full-label second variation; exact mean-value reconstruction in "
    "lambda; separate same-kernel 256-bit precision replay; binary64 RK4 "
    "values used "
    "only as Hermite guide centers and never as enclosures or sign evidence"
)

IntervalVector = tuple[DirectedInterval, ...]
FloatVector = tuple[float, ...]
IntervalPolynomial = tuple[DirectedInterval, ...]
PolynomialVector = tuple[IntervalPolynomial, ...]


def _point(value: str | int, precision: int) -> DirectedInterval:
    return DirectedInterval.from_decimal(value, precision)


def _float_point(value: float, precision: int) -> DirectedInterval:
    return DirectedInterval.from_float(value, precision)


def _closed(
    lower: str | int, upper: str | int, precision: int
) -> DirectedInterval:
    return DirectedInterval.from_bounds(lower, upper, precision)


def _mpfr_point(value: gmpy2.mpfr, precision: int) -> DirectedInterval:
    return DirectedInterval.from_bounds(value, value, precision)


def _algebraic_pair(value: sp.Expr) -> tuple[sp.Rational, sp.Rational]:
    """Write an element of ``Q(sqrt(5))`` as ``a+b*sqrt(5)``."""

    expression = sp.expand(value)
    root = sp.sqrt(5)
    rational = sp.simplify(expression.subs(root, 0))
    radical = sp.simplify((expression - rational) / root)
    if (
        sp.simplify(expression - rational - radical * root) != 0
        or rational.is_Rational is not True
        or radical.is_Rational is not True
    ):
        raise AssertionError("a patch coefficient left Q(sqrt(5))")
    return sp.Rational(rational), sp.Rational(radical)


@lru_cache(maxsize=1)
def _exact_patch_x_coefficient_pairs(
) -> tuple[tuple[tuple[sp.Rational, sp.Rational], ...], ...]:
    """Return constant-first label coefficients of the four X corrections."""

    rows = []
    for order, endpoint in enumerate(exact_target_endpoint_jets()):
        base = _unpatched_history_jet_algebra(
            EXACT_INCOMING_TIME,
            EXACT_TRANSVERSE,
            order,
            rho=EXACT_RHO,
            nu=EXACT_NU,
            eta=EXACT_ETA,
            theta=EXACT_THETA,
            phase_shift=EXACT_PHASE_SHIFT,
            section_half_width=EXACT_SECTION_HALF_WIDTH,
        )
        polynomial = sp.Poly(
            sp.expand(endpoint[0] - base[0]), EXACT_TRANSVERSE
        )
        if polynomial.is_zero:
            rows.append(((sp.Rational(0), sp.Rational(0)),))
        else:
            rows.append(
                tuple(
                    _algebraic_pair(coefficient)
                    for coefficient in reversed(polynomial.all_coeffs())
                )
            )
    return tuple(rows)


def _rational_interval(
    value: sp.Rational, precision: int
) -> DirectedInterval:
    return _point(int(value.p), precision) / _point(int(value.q), precision)


@lru_cache(maxsize=8)
def _patch_x_coefficients(
    precision: int,
) -> tuple[IntervalVector, ...]:
    root = _point(5, precision).sqrt()
    return tuple(
        tuple(
            _rational_interval(rational, precision)
            + _rational_interval(radical, precision) * root
            for rational, radical in row
        )
        for row in _exact_patch_x_coefficient_pairs()
    )


@lru_cache(maxsize=1)
def exact_first_step_cover_defects() -> tuple[sp.Expr, ...]:
    """Audit the patch, first/second variations, Hermite basis, and frame."""

    label = EXACT_TRANSVERSE
    reconstructed = []
    for row in _exact_patch_x_coefficient_pairs():
        reconstructed.append(
            sp.expand(
                sum(
                    (rational + radical * sp.sqrt(5)) * label**index
                    for index, (rational, radical) in enumerate(row)
                )
            )
        )
    coefficient_defects = []
    for order, endpoint in enumerate(exact_target_endpoint_jets()):
        base = _unpatched_history_jet_algebra(
            EXACT_INCOMING_TIME,
            label,
            order,
            rho=EXACT_RHO,
            nu=EXACT_NU,
            eta=EXACT_ETA,
            theta=EXACT_THETA,
            phase_shift=EXACT_PHASE_SHIFT,
            section_half_width=EXACT_SECTION_HALF_WIDTH,
        )
        coefficient_defects.append(
            sp.expand(reconstructed[order] - (endpoint[0] - base[0]))
        )

    x, y, x4, x5 = sp.symbols("x y x4 x5", real=True)
    vx, vy, vx4, vx5 = sp.symbols("vx vy vx4 vx5", real=True)
    wx, wy, wx4, wx5 = sp.symbols("wx wy wx4 wx5", real=True)
    rho = sp.sqrt(5) / 5
    fast = (
        y
        - x**2
        - rho * x**3 / 3
        + rho / 5 * ((x4 + x5) / 2 - x)
        + rho**3 / 4 * ((x4**3 + x5**3) / 2 - x**3)
    )
    slow = -x + rho * EXACT_NU
    parent_fast, parent_slow = physical_field_time_derivative_from_jets(
        ((x, y),),
        ((x4, sp.Symbol("y4", real=True)),),
        ((x5, sp.Symbol("y5", real=True)),),
        ((sp.Symbol("xtheta", real=True), sp.Symbol("ytheta", real=True)),),
        rho=rho,
        nu=EXACT_NU,
        eta=sp.Integer(0),
        derivative_order=0,
    )
    variables = (x, y, x4, x5)
    first_jets = (vx, vy, vx4, vx5)
    second_jets = (wx, wy, wx4, wx5)
    differentiated_once = sum(
        sp.diff(fast, variable) * jet
        for variable, jet in zip(variables, first_jets, strict=True)
    )
    implemented_once = (
        (-2 * x - rho * x**2 - rho / 5 - 3 * rho**3 * x**2 / 4)
        * vx
        + vy
        + (rho / 10 + 3 * rho**3 * x4**2 / 8) * vx4
        + (rho / 10 + 3 * rho**3 * x5**2 / 8) * vx5
    )
    differentiated_twice = sum(
        sp.diff(fast, variable) * jet
        for variable, jet in zip(variables, second_jets, strict=True)
    ) + sum(
        sp.diff(fast, left, right) * left_jet * right_jet
        for left, left_jet in zip(variables, first_jets, strict=True)
        for right, right_jet in zip(variables, first_jets, strict=True)
    )
    implemented_twice = (
        (-2 * x - rho * x**2 - rho / 5 - 3 * rho**3 * x**2 / 4)
        * wx
        + wy
        + (-2 - 2 * rho * x - 3 * rho**3 * x / 2) * vx**2
        + (rho / 10 + 3 * rho**3 * x4**2 / 8) * wx4
        + 3 * rho**3 * x4 * vx4**2 / 4
        + (rho / 10 + 3 * rho**3 * x5**2 / 8) * wx5
        + 3 * rho**3 * x5 * vx5**2 / 4
    )

    u = sp.Symbol("u", real=True)
    z0, z1, d0, d1, h = sp.symbols("z0 z1 d0 d1 h", real=True)
    a0 = z0
    a1 = h * d0
    a2 = -3 * z0 - 2 * a1 + 3 * z1 - h * d1
    a3 = 2 * z0 + a1 - 2 * z1 + h * d1
    hermite = a0 + u * (a1 + u * (a2 + u * a3))
    frame = sp.Matrix(((-7, 2), (3, 1)))
    return tuple(
        sp.simplify(value)
        for value in (
            *coefficient_defects,
            fast - parent_fast,
            slow - parent_slow,
            implemented_once - differentiated_once,
            implemented_twice - differentiated_twice,
            hermite.subs(u, 0) - z0,
            hermite.subs(u, 1) - z1,
            sp.diff(hermite, u).subs(u, 0) / h - d0,
            sp.diff(hermite, u).subs(u, 1) / h - d1,
            frame.det() + 13,
        )
    )


def _polynomial(
    coefficients: Sequence[DirectedInterval],
    argument: DirectedInterval,
) -> DirectedInterval:
    if not coefficients:
        raise ValueError("a polynomial needs at least one coefficient")
    result = coefficients[-1]
    for coefficient in reversed(coefficients[:-1]):
        result = result * argument + coefficient
    return result


def _polynomial_derivative(
    coefficients: Sequence[DirectedInterval],
    argument: DirectedInterval,
) -> DirectedInterval:
    precision = argument.precision
    if len(coefficients) <= 1:
        return _point(0, precision)
    derivative = tuple(
        _point(index, precision) * coefficients[index]
        for index in range(1, len(coefficients))
    )
    return _polynomial(derivative, argument)


def _right_jet_shape_interval(
    relative_time: DirectedInterval, order: int
) -> DirectedInterval:
    """Evaluate the exact degree-nine shape on ``[-1/2,0]``."""

    if type(order) is not int or not 1 <= order <= 4:
        raise ValueError("the patch jet order must lie between one and four")
    precision = relative_time.precision
    if relative_time.lower < _point("-0.5", precision).lower:
        raise ValueError("a patch interval crossed the left support boundary")
    if relative_time.upper > 0:
        raise ValueError("a patch interval crossed the C4 seam")
    one = _point(1, precision)
    u = one + _point(2, precision) * relative_time
    cutoff = u**5 * (
        _point(126, precision)
        + u
        * (
            _point(-420, precision)
            + u
            * (
                _point(540, precision)
                + u
                * (
                    _point(-315, precision)
                    + u * _point(70, precision)
                )
            )
        )
    )
    return (
        relative_time**order
        / _point(math.factorial(order), precision)
        * cutoff
    )


def _poly_constant(value: DirectedInterval) -> IntervalPolynomial:
    return (value,)


def _poly_add(
    left: Sequence[DirectedInterval], right: Sequence[DirectedInterval]
) -> IntervalPolynomial:
    if not left or not right:
        raise ValueError("polynomials must be nonempty")
    precision = left[0].precision
    if any(value.precision != precision for value in (*left, *right)):
        raise ValueError("polynomial precisions must agree")
    zero = _point(0, precision)
    size = max(len(left), len(right))
    return tuple(
        (left[index] if index < len(left) else zero)
        + (right[index] if index < len(right) else zero)
        for index in range(size)
    )


def _poly_neg(value: Sequence[DirectedInterval]) -> IntervalPolynomial:
    return tuple(-coefficient for coefficient in value)


def _poly_sub(
    left: Sequence[DirectedInterval], right: Sequence[DirectedInterval]
) -> IntervalPolynomial:
    return _poly_add(left, _poly_neg(right))


def _poly_scale(
    value: Sequence[DirectedInterval], scalar: DirectedInterval
) -> IntervalPolynomial:
    return tuple(coefficient * scalar for coefficient in value)


def _poly_multiply(
    left: Sequence[DirectedInterval], right: Sequence[DirectedInterval]
) -> IntervalPolynomial:
    if not left or not right:
        raise ValueError("polynomials must be nonempty")
    precision = left[0].precision
    if any(value.precision != precision for value in (*left, *right)):
        raise ValueError("polynomial precisions must agree")
    zero = _point(0, precision)
    result = [zero for _ in range(len(left) + len(right) - 1)]
    for left_index, left_value in enumerate(left):
        for right_index, right_value in enumerate(right):
            index = left_index + right_index
            result[index] = result[index] + left_value * right_value
    return tuple(result)


def _poly_power(
    value: Sequence[DirectedInterval], exponent: int
) -> IntervalPolynomial:
    if type(exponent) is not int or exponent < 0:
        raise ValueError("the polynomial exponent must be nonnegative")
    precision = value[0].precision
    result: IntervalPolynomial = (_point(1, precision),)
    factor = tuple(value)
    power = exponent
    while power:
        if power & 1:
            result = _poly_multiply(result, factor)
        power >>= 1
        if power:
            factor = _poly_multiply(factor, factor)
    return result


def _poly_add_constant(
    value: Sequence[DirectedInterval], constant: DirectedInterval
) -> IntervalPolynomial:
    result = list(value)
    result[0] = result[0] + constant
    return tuple(result)


def _poly_time_derivative(
    value: Sequence[DirectedInterval], step: DirectedInterval
) -> IntervalPolynomial:
    precision = step.precision
    if len(value) == 1:
        return (_point(0, precision),)
    return tuple(
        _point(index, precision) * value[index] / step
        for index in range(1, len(value))
    )


@lru_cache(maxsize=256)
def _bernstein_weights(
    degree: int, precision: int
) -> tuple[tuple[DirectedInterval, ...], ...]:
    if type(degree) is not int or degree < 0:
        raise ValueError("the Bernstein degree must be nonnegative")
    rows = []
    for bernstein_index in range(degree + 1):
        row = []
        for power in range(bernstein_index + 1):
            weight = sp.Rational(
                math.comb(bernstein_index, power), math.comb(degree, power)
            )
            row.append(_rational_interval(weight, precision))
        rows.append(tuple(row))
    return tuple(rows)


def _poly_bernstein_range(
    value: Sequence[DirectedInterval],
) -> DirectedInterval:
    """Return the convex-hull Bernstein enclosure on ``0 <= u <= 1``."""

    if not value:
        raise ValueError("a polynomial must be nonempty")
    precision = value[0].precision
    if any(coefficient.precision != precision for coefficient in value):
        raise ValueError("polynomial coefficients use different precisions")
    degree = len(value) - 1
    weights = _bernstein_weights(degree, precision)
    coefficients = []
    for index, row in enumerate(weights):
        coefficient = _point(0, precision)
        for power, weight in enumerate(row):
            coefficient = coefficient + weight * value[power]
        coefficients.append(coefficient)
    return DirectedInterval.from_bounds(
        min(coefficient.lower for coefficient in coefficients),
        max(coefficient.upper for coefficient in coefficients),
        precision,
    )


def _poly_vector_range(value: PolynomialVector) -> IntervalVector:
    return tuple(_poly_bernstein_range(component) for component in value)


def _patch_shape_polynomial(
    relative_time: IntervalPolynomial, order: int
) -> IntervalPolynomial:
    precision = relative_time[0].precision
    one = _poly_constant(_point(1, precision))
    u = _poly_add(one, _poly_scale(relative_time, _point(2, precision)))
    cutoff_tail = _poly_add(
        _poly_constant(_point(-315, precision)),
        _poly_scale(u, _point(70, precision)),
    )
    cutoff_tail = _poly_add(
        _poly_constant(_point(540, precision)),
        _poly_multiply(u, cutoff_tail),
    )
    cutoff_tail = _poly_add(
        _poly_constant(_point(-420, precision)),
        _poly_multiply(u, cutoff_tail),
    )
    cutoff_tail = _poly_add(
        _poly_constant(_point(126, precision)),
        _poly_multiply(u, cutoff_tail),
    )
    cutoff = _poly_multiply(_poly_power(u, 5), cutoff_tail)
    return _poly_scale(
        _poly_multiply(_poly_power(relative_time, order), cutoff),
        _point(1, precision) / _point(math.factorial(order), precision),
    )


def _history_x_and_label_variation_polynomial(
    time_left: DirectedInterval,
    step: DirectedInterval,
    label: DirectedInterval,
    delay: int,
) -> tuple[IntervalPolynomial, IntervalPolynomial, IntervalPolynomial]:
    """Exact delayed X and X_lambda polynomials in normalized cell time."""

    precision = step.precision
    time = (time_left, step)
    phase = _point("-0.061579261574946566", precision)
    base = _poly_scale(
        _poly_add_constant(time, -_point(delay, precision) + phase),
        -_point(1, precision) / _point(2, precision),
    )
    variation: IntervalPolynomial = (_point(0, precision),)
    second_variation: IntervalPolynomial = (_point(0, precision),)
    patch_entry = _point(PATCH_ENTRY_TIME, precision)
    if delay == 5 or time_left.upper < patch_entry.lower:
        return base, variation, second_variation
    if time_left.lower < patch_entry.lower:
        raise ValueError("the time grid must split at the patch entry")
    relative = _poly_add_constant(time, -_point(1, precision))
    coefficients = _patch_x_coefficients(precision)
    for order in range(1, 5):
        shape = _patch_shape_polynomial(relative, order)
        base = _poly_add(
            base,
            _poly_scale(shape, _polynomial(coefficients[order], label)),
        )
        variation = _poly_add(
            variation,
            _poly_scale(
                shape,
                _polynomial_derivative(coefficients[order], label),
            ),
        )
        first_derivative_coefficients = tuple(
            _point(index, precision) * coefficients[order][index]
            for index in range(1, len(coefficients[order]))
        )
        second_variation = _poly_add(
            second_variation,
            _poly_scale(
                shape,
                _polynomial_derivative(first_derivative_coefficients, label),
            ),
        )
    return base, variation, second_variation


def _state_rhs_polynomial(
    time_left: DirectedInterval,
    step: DirectedInterval,
    state: PolynomialVector,
    label: DirectedInterval,
) -> PolynomialVector:
    precision = step.precision
    rho = _point(5, precision).sqrt() / _point(5, precision)
    nu = _point("0.21256022233963731", precision)
    x, y = state
    x4, _, _ = _history_x_and_label_variation_polynomial(
        time_left, step, label, 4
    )
    x5, _, _ = _history_x_and_label_variation_polynomial(
        time_left, step, label, 5
    )
    x2 = _poly_power(x, 2)
    x3 = _poly_multiply(x2, x)
    delayed_linear = _poly_sub(
        _poly_scale(_poly_add(x4, x5), _point(1, precision) / _point(2, precision)),
        x,
    )
    delayed_cubic = _poly_sub(
        _poly_scale(
            _poly_add(_poly_power(x4, 3), _poly_power(x5, 3)),
            _point(1, precision) / _point(2, precision),
        ),
        x3,
    )
    fast = _poly_add(y, _poly_scale(x2, -_point(1, precision)))
    fast = _poly_add(
        fast, _poly_scale(x3, -rho / _point(3, precision))
    )
    fast = _poly_add(
        fast, _poly_scale(delayed_linear, rho / _point(5, precision))
    )
    fast = _poly_add(
        fast, _poly_scale(delayed_cubic, rho**3 / _point(4, precision))
    )
    slow = _poly_add_constant(
        _poly_scale(x, -_point(1, precision)), rho * nu
    )
    return fast, slow


def _variation_rhs_polynomial(
    time_left: DirectedInterval,
    step: DirectedInterval,
    family_state: PolynomialVector,
    variation: PolynomialVector,
    label: DirectedInterval,
) -> PolynomialVector:
    precision = step.precision
    rho = _point(5, precision).sqrt() / _point(5, precision)
    x = family_state[0]
    vx, vy = variation
    x4, vx4, _ = _history_x_and_label_variation_polynomial(
        time_left, step, label, 4
    )
    x5, vx5, _ = _history_x_and_label_variation_polynomial(
        time_left, step, label, 5
    )
    x2 = _poly_power(x, 2)
    current = _poly_scale(x, -_point(2, precision))
    current = _poly_add(
        current, _poly_scale(x2, -rho)
    )
    current = _poly_add_constant(current, -rho / _point(5, precision))
    current = _poly_add(
        current,
        _poly_scale(x2, -_point(3, precision) * rho**3 / _point(4, precision)),
    )
    delayed_4 = _poly_add_constant(
        _poly_scale(
            _poly_power(x4, 2),
            _point(3, precision) * rho**3 / _point(8, precision),
        ),
        rho / _point(10, precision),
    )
    delayed_5 = _poly_add_constant(
        _poly_scale(
            _poly_power(x5, 2),
            _point(3, precision) * rho**3 / _point(8, precision),
        ),
        rho / _point(10, precision),
    )
    fast = _poly_add(_poly_multiply(current, vx), vy)
    fast = _poly_add(fast, _poly_multiply(delayed_4, vx4))
    fast = _poly_add(fast, _poly_multiply(delayed_5, vx5))
    return fast, _poly_scale(vx, -_point(1, precision))


def _second_variation_rhs_polynomial(
    time_left: DirectedInterval,
    step: DirectedInterval,
    family_state: PolynomialVector,
    family_variation: PolynomialVector,
    second_variation: PolynomialVector,
    label: DirectedInterval,
) -> PolynomialVector:
    """Enclose the exact second label-variational equation."""

    precision = step.precision
    rho = _point(5, precision).sqrt() / _point(5, precision)
    x = family_state[0]
    vx = family_variation[0]
    wx, wy = second_variation
    x4, vx4, wx4 = _history_x_and_label_variation_polynomial(
        time_left, step, label, 4
    )
    x5, vx5, wx5 = _history_x_and_label_variation_polynomial(
        time_left, step, label, 5
    )
    x2 = _poly_power(x, 2)
    current = _poly_scale(x, -_point(2, precision))
    current = _poly_add(current, _poly_scale(x2, -rho))
    current = _poly_add_constant(current, -rho / _point(5, precision))
    current = _poly_add(
        current,
        _poly_scale(
            x2, -_point(3, precision) * rho**3 / _point(4, precision)
        ),
    )
    current_second = _poly_add_constant(
        _poly_scale(
            x, -_point(2, precision) * rho - _point(3, precision) * rho**3 / _point(2, precision)
        ),
        -_point(2, precision),
    )

    def delayed_terms(
        delayed_x: IntervalPolynomial,
        delayed_v: IntervalPolynomial,
        delayed_w: IntervalPolynomial,
    ) -> IntervalPolynomial:
        first = _poly_add_constant(
            _poly_scale(
                _poly_power(delayed_x, 2),
                _point(3, precision) * rho**3 / _point(8, precision),
            ),
            rho / _point(10, precision),
        )
        second = _poly_scale(
            delayed_x, _point(3, precision) * rho**3 / _point(4, precision)
        )
        return _poly_add(
            _poly_multiply(first, delayed_w),
            _poly_multiply(second, _poly_power(delayed_v, 2)),
        )

    fast = _poly_add(_poly_multiply(current, wx), wy)
    fast = _poly_add(
        fast, _poly_multiply(current_second, _poly_power(vx, 2))
    )
    fast = _poly_add(fast, delayed_terms(x4, vx4, wx4))
    fast = _poly_add(fast, delayed_terms(x5, vx5, wx5))
    return fast, _poly_scale(wx, -_point(1, precision))


def _history_x_and_label_variation(
    physical_time: DirectedInterval,
    label: DirectedInterval,
    delay: int,
) -> tuple[DirectedInterval, DirectedInterval]:
    """Enclose the exact incoming delayed X slot and its label derivative."""

    if delay not in (4, 5):
        raise ValueError("only the active delays four and five are supported")
    precision = physical_time.precision
    if label.precision != precision:
        raise ValueError("time and label precisions must agree")
    phase = _point("-0.061579261574946566", precision)
    base = -(physical_time - _point(delay, precision) + phase) / _point(
        2, precision
    )
    variation = _point(0, precision)
    patch_entry = _point(PATCH_ENTRY_TIME, precision)
    if delay == 5 or physical_time.upper <= patch_entry.upper:
        return base, variation
    if physical_time.lower < patch_entry.lower:
        raise ValueError("the time grid must split at the patch entry")
    relative = physical_time - _point(1, precision)
    coefficients = _patch_x_coefficients(precision)
    for order in range(1, 5):
        shape = _right_jet_shape_interval(relative, order)
        variation = variation + _polynomial_derivative(
            coefficients[order], label
        ) * shape
        base = base + _polynomial(coefficients[order], label) * shape
    return base, variation


def _state_rhs(
    physical_time: DirectedInterval,
    state: Sequence[DirectedInterval],
    label: DirectedInterval,
) -> IntervalVector:
    if len(state) != 2:
        raise ValueError("the state must have two coordinates")
    precision = physical_time.precision
    if any(value.precision != precision for value in (*state, label)):
        raise ValueError("all state RHS intervals must use one precision")
    rho = _point(5, precision).sqrt() / _point(5, precision)
    nu = _point("0.21256022233963731", precision)
    x, y = state
    x4, _ = _history_x_and_label_variation(physical_time, label, 4)
    x5, _ = _history_x_and_label_variation(physical_time, label, 5)
    two = _point(2, precision)
    three = _point(3, precision)
    four = _point(4, precision)
    five = _point(5, precision)
    return (
        y
        - x**2
        - rho * x**3 / three
        + rho / five * ((x4 + x5) / two - x)
        + rho**3 / four * ((x4**3 + x5**3) / two - x**3),
        -x + rho * nu,
    )


def _variation_rhs(
    physical_time: DirectedInterval,
    family_state: Sequence[DirectedInterval],
    variation: Sequence[DirectedInterval],
    label: DirectedInterval,
) -> IntervalVector:
    if len(family_state) != 2 or len(variation) != 2:
        raise ValueError("state and variation must have two coordinates")
    precision = physical_time.precision
    if any(
        value.precision != precision
        for value in (*family_state, *variation, label)
    ):
        raise ValueError("all variation RHS intervals must use one precision")
    rho = _point(5, precision).sqrt() / _point(5, precision)
    x = family_state[0]
    vx, vy = variation
    x4, vx4 = _history_x_and_label_variation(physical_time, label, 4)
    x5, vx5 = _history_x_and_label_variation(physical_time, label, 5)
    two = _point(2, precision)
    three = _point(3, precision)
    four = _point(4, precision)
    five = _point(5, precision)
    eight = _point(8, precision)
    current = (
        -two * x
        - rho * x**2
        - rho / five
        - three * rho**3 * x**2 / four
    )
    delayed_4 = rho / _point(10, precision) + (
        three * rho**3 * x4**2 / eight
    )
    delayed_5 = rho / _point(10, precision) + (
        three * rho**3 * x5**2 / eight
    )
    return current * vx + vy + delayed_4 * vx4 + delayed_5 * vx5, -vx


@lru_cache(maxsize=1)
def _float_patch_x_coefficients() -> tuple[tuple[float, ...], ...]:
    root = math.sqrt(5.0)
    return tuple(
        tuple(float(rational) + float(radical) * root for rational, radical in row)
        for row in _exact_patch_x_coefficient_pairs()
    )


def _float_history_x_label_jets(
    physical_time: float, label: float, delay: int
) -> tuple[float, float, float]:
    delayed_time = physical_time - float(delay)
    value = c4_prepared_history_state(delayed_time, label)[0]
    first = c4_prepared_history_transverse_derivative(
        delayed_time, label
    )[0]
    second = 0.0
    relative = delayed_time + 3.0
    if delay == 4 and relative > -0.5:
        for order in range(1, 5):
            coefficients = _float_patch_x_coefficients()[order]
            polynomial_second = 0.0
            for index in range(2, len(coefficients)):
                polynomial_second += (
                    index
                    * (index - 1)
                    * coefficients[index]
                    * label ** (index - 2)
                )
            second += polynomial_second * right_jet_shape(relative, order)
    return float(value), float(first), float(second)


def _float_coupled_rhs(time: float, state: FloatVector, label: float) -> FloatVector:
    """Binary64 guide field; no value returned here is proof-bearing."""

    if len(state) != 6:
        raise ValueError("the guide state must contain state, first, and second jets")
    x, y, vx, vy, wx, wy = state
    rho = math.sqrt(5.0) / 5.0
    nu = 0.21256022233963731
    x4, vx4, wx4 = _float_history_x_label_jets(time, label, 4)
    x5, vx5, wx5 = _float_history_x_label_jets(time, label, 5)
    fast = (
        y
        - x * x
        - rho * x**3 / 3.0
        + rho / 5.0 * ((x4 + x5) / 2.0 - x)
        + rho**3 / 4.0 * ((x4**3 + x5**3) / 2.0 - x**3)
    )
    slow = -x + rho * nu
    current = -2.0 * x - rho * x * x - rho / 5.0 - 0.75 * rho**3 * x * x
    delayed_4 = rho / 10.0 + 3.0 * rho**3 * x4 * x4 / 8.0
    delayed_5 = rho / 10.0 + 3.0 * rho**3 * x5 * x5 / 8.0
    current_second = -2.0 - 2.0 * rho * x - 1.5 * rho**3 * x
    delayed_4_second = 0.75 * rho**3 * x4
    delayed_5_second = 0.75 * rho**3 * x5
    return (
        fast,
        slow,
        current * vx + vy + delayed_4 * vx4 + delayed_5 * vx5,
        -vx,
        current * wx
        + wy
        + current_second * vx * vx
        + delayed_4 * wx4
        + delayed_4_second * vx4 * vx4
        + delayed_5 * wx5
        + delayed_5_second * vx5 * vx5,
        -wx,
    )


def _add_scaled(left: FloatVector, right: FloatVector, scale: float) -> FloatVector:
    return tuple(a + scale * b for a, b in zip(left, right, strict=True))


def _rk4_step(time: float, state: FloatVector, label: float, step: float) -> FloatVector:
    k1 = _float_coupled_rhs(time, state, label)
    k2 = _float_coupled_rhs(
        time + step / 2.0, _add_scaled(state, k1, step / 2.0), label
    )
    k3 = _float_coupled_rhs(
        time + step / 2.0, _add_scaled(state, k2, step / 2.0), label
    )
    k4 = _float_coupled_rhs(time + step, _add_scaled(state, k3, step), label)
    return tuple(
        value
        + step
        * (a + 2.0 * b + 2.0 * c + d)
        / 6.0
        for value, a, b, c, d in zip(state, k1, k2, k3, k4, strict=True)
    )


def _time_node(index: int) -> str:
    return format(Decimal(-3) + Decimal(index) / Decimal(100), "f")


def _label_node(index: int) -> str:
    return format(Decimal("-0.05") + Decimal(index) / Decimal(200), "f")


@lru_cache(maxsize=32)
def _guide(label_index: int) -> tuple[FloatVector, ...]:
    left = float(_label_node(label_index))
    right = float(_label_node(label_index + 1))
    label = (left + right) / 2.0
    state_value = c4_prepared_history_state(-3.0, label)
    variation_value = c4_prepared_history_transverse_derivative(-3.0, label)
    state: FloatVector = (*state_value, *variation_value, 0.0, 0.0)
    rows = [state]
    for index in range(400):
        state = _rk4_step(-3.0 + index * 0.01, state, label, 0.01)
        if not all(math.isfinite(value) for value in state):
            raise RuntimeError("the nonrigorous RK4 guide became nonfinite")
        rows.append(state)
    return tuple(rows)


def _hermite_polynomials(
    start: Sequence[DirectedInterval],
    end: Sequence[DirectedInterval],
    start_derivative: Sequence[DirectedInterval],
    end_derivative: Sequence[DirectedInterval],
    step: DirectedInterval,
) -> tuple[PolynomialVector, PolynomialVector]:
    """Return power coefficients of the guide and its time derivative."""

    if not (
        len(start)
        == len(end)
        == len(start_derivative)
        == len(end_derivative)
    ):
        raise ValueError("Hermite vectors must have equal length")
    precision = step.precision
    two = _point(2, precision)
    three = _point(3, precision)
    polynomials = []
    derivatives = []
    for left, right, left_rhs, right_rhs in zip(
        start, end, start_derivative, end_derivative, strict=True
    ):
        a0 = left
        a1 = step * left_rhs
        a2 = -three * left - two * a1 + three * right - step * right_rhs
        a3 = two * left + a1 - two * right + step * right_rhs
        polynomial = (a0, a1, a2, a3)
        polynomials.append(polynomial)
        derivatives.append(_poly_time_derivative(polynomial, step))
    return tuple(polynomials), tuple(derivatives)


def _symmetric_error(radius: gmpy2.mpfr, precision: int) -> DirectedInterval:
    raw = _mpfr_point(radius, precision) * _point("1.03125", precision) + _point(
        "1e-50", precision
    )
    # Negating an MPFR value outside an explicit context can first round it at
    # the process default (usually 53 bits), occasionally moving the negative
    # endpoint inward.  Construct the symmetric box directly at the proof
    # precision with directed endpoint rounding.
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        lower = -raw.upper
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        upper = gmpy2.mpfr(raw.upper)
    return DirectedInterval(lower, upper, precision)


def _strict_gaps(
    image: Sequence[DirectedInterval], box: Sequence[DirectedInterval]
) -> tuple[gmpy2.mpfr, ...]:
    if len(image) != len(box):
        raise ValueError("the Picard image and box have different dimensions")
    gaps = []
    for enclosed, container in zip(image, box, strict=True):
        with gmpy2.context(precision=enclosed.precision, round=gmpy2.RoundDown):
            gaps.extend(
                (enclosed.lower - container.lower, container.upper - enclosed.upper)
            )
    return tuple(gaps)


@dataclass(frozen=True)
class _PolynomialPicardStep:
    tube: PolynomialVector
    endpoint: IntervalVector
    minimum_gap: gmpy2.mpfr
    maximum_error_radius: gmpy2.mpfr


def _polynomial_picard_error_step(
    *,
    initial: Sequence[DirectedInterval],
    guide_start: Sequence[DirectedInterval],
    guide_end: Sequence[DirectedInterval],
    predictor: PolynomialVector,
    predictor_derivative: PolynomialVector,
    elapsed: DirectedInterval,
    step: DirectedInterval,
    residual_polynomial_field: Callable[[PolynomialVector], PolynomialVector],
) -> _PolynomialPicardStep:
    """Validate one cell while retaining exact normalized-time dependence."""

    if not (
        len(initial)
        == len(guide_start)
        == len(guide_end)
        == len(predictor)
        == len(predictor_derivative)
    ):
        raise ValueError("all polynomial Picard vectors must have equal dimension")
    precision = step.precision
    initial_error = tuple(
        value - center for value, center in zip(initial, guide_start, strict=True)
    )
    error = tuple(
        _symmetric_error(max(value.upper_abs(), gmpy2.mpfr("1e-55")), precision)
        for value in initial_error
    )
    for _ in range(40):
        tube = tuple(
            _poly_add_constant(polynomial, remainder)
            for polynomial, remainder in zip(predictor, error, strict=True)
        )
        field = residual_polynomial_field(tube)
        residual_polynomial = tuple(
            _poly_sub(value, guide)
            for value, guide in zip(field, predictor_derivative, strict=True)
        )
        residual = _poly_vector_range(residual_polynomial)
        image = tuple(
            value + elapsed * defect
            for value, defect in zip(initial_error, residual, strict=True)
        )
        gaps = _strict_gaps(image, error)
        if min(gaps) > 0:
            endpoint_error = tuple(
                value + step * defect
                for value, defect in zip(initial_error, residual, strict=True)
            )
            endpoint = tuple(
                center + remainder
                for center, remainder in zip(
                    guide_end, endpoint_error, strict=True
                )
            )
            return _PolynomialPicardStep(
                tube=tube,
                endpoint=endpoint,
                minimum_gap=min(gaps),
                maximum_error_radius=max(value.upper_abs() for value in error),
            )
        error = tuple(
            _symmetric_error(
                max(container.upper_abs(), enclosed.upper_abs()), precision
            )
            for container, enclosed in zip(error, image, strict=True)
        )
    raise RuntimeError("the polynomial error-coordinate Picard iteration did not close")


@dataclass(frozen=True)
class CoverProbe:
    precision_bits: int
    completed_label_cells: int
    completed_time_cells: int
    first_failure: tuple[int, int, str] | None
    minimum_central_picard_gap: str
    minimum_first_variation_picard_gap: str
    minimum_second_variation_picard_gap: str
    maximum_central_error_radius: str
    maximum_first_variation_error_radius: str
    maximum_second_variation_error_radius: str
    minimum_time_minor: str
    minimum_label_minor: str
    minimum_oriented_determinant: str
    maximum_raw_determinant: str
    maximum_early_x_time_derivative: str
    c4_patch_cell_count: int
    proof_cell_digest_sha256: str


def _lower_text(value: gmpy2.mpfr) -> str:
    return decimal_lower(value, 70)


def _upper_text(value: gmpy2.mpfr) -> str:
    return decimal_upper(value, 70)


def _digest_interval(value: DirectedInterval) -> str:
    lower = decimal_lower(value.lower, 70)
    upper = decimal_upper(value.upper, 70)
    serialized = DirectedInterval.from_bounds(lower, upper, value.precision)
    if serialized.lower > value.lower or serialized.upper < value.upper:
        raise AssertionError("a digest decimal failed outward reparsing")
    return f"{lower},{upper}"


def _digest_polynomial_vector(value: PolynomialVector) -> str:
    return ";".join(
        ",".join(_digest_interval(coefficient) for coefficient in component)
        for component in value
    )


def probe_cover(
    precision: int = PRIMARY_PRECISION_BITS,
    *,
    maximum_label_cells: int = 20,
    maximum_time_cells: int = 400,
) -> CoverProbe:
    """Run the strict cover kernel, returning the first failure if any."""

    if type(precision) is not int or precision < 64:
        raise ValueError("precision must be an integer of at least 64 bits")
    if not 1 <= maximum_label_cells <= 20:
        raise ValueError("maximum_label_cells must lie between one and twenty")
    if not 1 <= maximum_time_cells <= 400:
        raise ValueError("maximum_time_cells must lie between one and four hundred")
    minimum_central_gap = gmpy2.mpfr("inf")
    minimum_first_variation_gap = gmpy2.mpfr("inf")
    minimum_second_variation_gap = gmpy2.mpfr("inf")
    maximum_central_radius = gmpy2.mpfr(0)
    maximum_first_variation_radius = gmpy2.mpfr(0)
    maximum_second_variation_radius = gmpy2.mpfr(0)
    minimum_time_minor = gmpy2.mpfr("inf")
    minimum_label_minor = gmpy2.mpfr("inf")
    minimum_oriented = gmpy2.mpfr("inf")
    maximum_raw = gmpy2.mpfr("-inf")
    maximum_early_x_time = gmpy2.mpfr("-inf")
    patch_cells = 0
    digest = sha256()
    completed = 0
    failure = None
    step = _point(TIME_STEP, precision)
    elapsed = _closed(0, TIME_STEP, precision)
    for label_index in range(maximum_label_cells):
        label = _closed(
            _label_node(label_index), _label_node(label_index + 1), precision
        )
        label_center_float = (
            float(_label_node(label_index))
            + float(_label_node(label_index + 1))
        ) / 2.0
        label_center = _float_point(label_center_float, precision)
        if (
            label_center.lower < label.lower
            or label_center.upper > label.upper
        ):
            raise AssertionError("the exact binary64 guide label left its cell")
        delta_label = label - label_center
        guide = _guide(label_index)
        # This is an algebraic interval evaluation of the exact seam value;
        # the binary64 guide start below is only the center of its error tube.
        initial_state = _entry_initial_box(label_center)[:2]
        initial_variation = (
            _point(0, precision),
            _point(1, precision),
        )
        initial_second_variation = (
            _point(0, precision),
            _point(0, precision),
        )
        for time_index in range(maximum_time_cells):
            time_left = _time_node(time_index)
            time_right = _time_node(time_index + 1)
            time_left_point = _point(time_left, precision)
            time_right_point = _point(time_right, precision)
            guide_start_all = tuple(
                _float_point(value, precision) for value in guide[time_index]
            )
            guide_end_all = tuple(
                _float_point(value, precision) for value in guide[time_index + 1]
            )
            guide_state_start = guide_start_all[:2]
            guide_state_end = guide_end_all[:2]
            guide_variation_start = guide_start_all[2:4]
            guide_variation_end = guide_end_all[2:4]
            guide_second_start = guide_start_all[4:6]
            guide_second_end = guide_end_all[4:6]
            state_derivative_start = _state_rhs(
                time_left_point, guide_state_start, label_center
            )
            state_derivative_end = _state_rhs(
                time_right_point, guide_state_end, label_center
            )
            state_predictor, state_predictor_derivative = _hermite_polynomials(
                guide_state_start,
                guide_state_end,
                state_derivative_start,
                state_derivative_end,
                step,
            )
            try:
                central = _polynomial_picard_error_step(
                    initial=initial_state,
                    guide_start=guide_state_start,
                    guide_end=guide_state_end,
                    predictor=state_predictor,
                    predictor_derivative=state_predictor_derivative,
                    elapsed=elapsed,
                    step=step,
                    residual_polynomial_field=lambda tube: _state_rhs_polynomial(
                        time_left_point, step, tube, label_center
                    ),
                )
                variation_derivative_start = _variation_rhs(
                    time_left_point,
                    guide_state_start,
                    guide_variation_start,
                    label_center,
                )
                variation_derivative_end = _variation_rhs(
                    time_right_point,
                    guide_state_end,
                    guide_variation_end,
                    label_center,
                )
                variation_predictor, variation_predictor_derivative = (
                    _hermite_polynomials(
                        guide_variation_start,
                        guide_variation_end,
                        variation_derivative_start,
                        variation_derivative_end,
                        step,
                    )
                )

                def variation_field(
                    variation_tube: PolynomialVector,
                ) -> PolynomialVector:
                    return _variation_rhs_polynomial(
                        time_left_point,
                        step,
                        central.tube,
                        variation_tube,
                        label_center,
                    )

                variation = _polynomial_picard_error_step(
                    initial=initial_variation,
                    guide_start=guide_variation_start,
                    guide_end=guide_variation_end,
                    predictor=variation_predictor,
                    predictor_derivative=variation_predictor_derivative,
                    elapsed=elapsed,
                    step=step,
                    residual_polynomial_field=variation_field,
                )
                second_derivative_start = _second_variation_rhs_polynomial(
                    time_left_point,
                    _point(0, precision),
                    tuple(_poly_constant(value) for value in guide_state_start),
                    tuple(
                        _poly_constant(value) for value in guide_variation_start
                    ),
                    tuple(_poly_constant(value) for value in guide_second_start),
                    label_center,
                )
                second_derivative_end = _second_variation_rhs_polynomial(
                    time_right_point,
                    _point(0, precision),
                    tuple(_poly_constant(value) for value in guide_state_end),
                    tuple(
                        _poly_constant(value) for value in guide_variation_end
                    ),
                    tuple(_poly_constant(value) for value in guide_second_end),
                    label_center,
                )
                second_predictor, second_predictor_derivative = (
                    _hermite_polynomials(
                        guide_second_start,
                        guide_second_end,
                        _poly_vector_range(second_derivative_start),
                        _poly_vector_range(second_derivative_end),
                        step,
                    )
                )

                def second_field(
                    second_tube: PolynomialVector,
                ) -> PolynomialVector:
                    family_variation = tuple(
                        _poly_add(
                            center, _poly_scale(second, delta_label)
                        )
                        for center, second in zip(
                            variation.tube, second_tube, strict=True
                        )
                    )
                    family_state = tuple(
                        _poly_add(
                            center, _poly_scale(derivative, delta_label)
                        )
                        for center, derivative in zip(
                            central.tube, family_variation, strict=True
                        )
                    )
                    return _second_variation_rhs_polynomial(
                        time_left_point,
                        step,
                        family_state,
                        family_variation,
                        second_tube,
                        label,
                    )

                second_variation = _polynomial_picard_error_step(
                    initial=initial_second_variation,
                    guide_start=guide_second_start,
                    guide_end=guide_second_end,
                    predictor=second_predictor,
                    predictor_derivative=second_predictor_derivative,
                    elapsed=elapsed,
                    step=step,
                    residual_polynomial_field=second_field,
                )
            except (RuntimeError, ValueError) as error:
                failure = (label_index, time_index, str(error))
                break
            family_variation = tuple(
                _poly_add(center, _poly_scale(second, delta_label))
                for center, second in zip(
                    variation.tube, second_variation.tube, strict=True
                )
            )
            family_state = tuple(
                _poly_add(center, _poly_scale(derivative, delta_label))
                for center, derivative in zip(
                    central.tube, family_variation, strict=True
                )
            )
            fast, slow = _state_rhs_polynomial(
                time_left_point, step, family_state, label
            )
            vx, vy = family_variation
            time_minor = _poly_add(
                _poly_scale(fast, -_point(7, precision)),
                _poly_scale(slow, _point(2, precision)),
            )
            label_minor = _poly_add(
                _poly_scale(vx, _point(3, precision)), vy
            )
            raw_determinant = _poly_sub(
                _poly_multiply(fast, vy), _poly_multiply(slow, vx)
            )
            oriented = _poly_scale(raw_determinant, -_point(13, precision))
            time_minor_range = _poly_bernstein_range(time_minor)
            label_minor_range = _poly_bernstein_range(label_minor)
            raw_determinant_range = _poly_bernstein_range(raw_determinant)
            oriented_range = _poly_bernstein_range(oriented)
            if (
                time_minor_range.lower <= 0
                or label_minor_range.lower <= 0
                or oriented_range.lower <= 0
                or raw_determinant_range.upper >= 0
            ):
                failure = (label_index, time_index, "a P-matrix margin crossed zero")
                break
            minimum_central_gap = min(
                minimum_central_gap, central.minimum_gap
            )
            minimum_first_variation_gap = min(
                minimum_first_variation_gap, variation.minimum_gap
            )
            minimum_second_variation_gap = min(
                minimum_second_variation_gap, second_variation.minimum_gap
            )
            maximum_central_radius = max(
                maximum_central_radius, central.maximum_error_radius
            )
            maximum_first_variation_radius = max(
                maximum_first_variation_radius,
                variation.maximum_error_radius,
            )
            maximum_second_variation_radius = max(
                maximum_second_variation_radius,
                second_variation.maximum_error_radius,
            )
            minimum_time_minor = min(
                minimum_time_minor, time_minor_range.lower
            )
            minimum_label_minor = min(
                minimum_label_minor, label_minor_range.lower
            )
            minimum_oriented = min(
                minimum_oriented, oriented_range.lower
            )
            maximum_raw = max(maximum_raw, raw_determinant_range.upper)
            if time_index < 100:
                maximum_early_x_time = max(
                    maximum_early_x_time, _poly_bernstein_range(fast).upper
                )
            if time_index >= 350:
                patch_cells += 1
            digest.update(
                (
                    f"{label_index}:{time_index}|"
                    + _digest_polynomial_vector(central.tube)
                    + "|"
                    + _digest_polynomial_vector(variation.tube)
                    + "|"
                    + _digest_polynomial_vector(second_variation.tube)
                    + "|"
                    + ";".join(_digest_interval(value) for value in central.endpoint)
                    + "|"
                    + ";".join(_digest_interval(value) for value in variation.endpoint)
                    + "|"
                    + ";".join(
                        _digest_interval(value)
                        for value in second_variation.endpoint
                    )
                    + "|"
                    + ";".join(
                        _digest_interval(value)
                        for value in (
                            time_minor_range,
                            label_minor_range,
                            oriented_range,
                            raw_determinant_range,
                        )
                    )
                    + "\n"
                ).encode("ascii")
            )
            initial_state = central.endpoint
            initial_variation = variation.endpoint
            initial_second_variation = second_variation.endpoint
            completed += 1
        if failure is not None:
            break
    return CoverProbe(
        precision_bits=precision,
        completed_label_cells=(completed // maximum_time_cells),
        completed_time_cells=completed,
        first_failure=failure,
        minimum_central_picard_gap=_lower_text(minimum_central_gap),
        minimum_first_variation_picard_gap=_lower_text(
            minimum_first_variation_gap
        ),
        minimum_second_variation_picard_gap=_lower_text(
            minimum_second_variation_gap
        ),
        maximum_central_error_radius=_upper_text(maximum_central_radius),
        maximum_first_variation_error_radius=_upper_text(
            maximum_first_variation_radius
        ),
        maximum_second_variation_error_radius=_upper_text(
            maximum_second_variation_radius
        ),
        minimum_time_minor=_lower_text(minimum_time_minor),
        minimum_label_minor=_lower_text(minimum_label_minor),
        minimum_oriented_determinant=_lower_text(minimum_oriented),
        maximum_raw_determinant=_upper_text(maximum_raw),
        maximum_early_x_time_derivative=_upper_text(maximum_early_x_time),
        c4_patch_cell_count=patch_cells,
        proof_cell_digest_sha256=digest.hexdigest(),
    )


@dataclass(frozen=True)
class TargetFirstMethodStepCoverCertificate:
    model_id: str
    audit_id: str
    arithmetic: str
    coordinate_order: tuple[str, ...]
    physical_output_frame: tuple[tuple[int, int], tuple[int, int]]
    physical_frame_determinant: int
    physical_time_interval: tuple[str, str]
    label_interval: tuple[str, str]
    time_step: str
    label_step: str
    time_cell_count_per_label: int
    label_cell_count: int
    total_time_label_cell_count: int
    patch_entry_time: str
    patch_time_cell_count_per_label: int
    primary: CoverProbe
    refinement: CoverProbe
    exact_symbolic_zero_defect_count: int
    exact_delay_regime: str
    parameter_reconstruction: str
    wrapping_method: str
    local_defect_method: str
    exact_scope: str
    open_scope: str
    exact_first_method_step_delay_regime_verified: bool
    exact_c4_patch_x_and_first_two_label_derivatives_verified: bool
    exact_state_first_second_variational_reduction_verified: bool
    exact_cubic_hermite_endpoint_identities_verified: bool
    exact_bernstein_convex_hull_range_theorem_used: bool
    strict_central_state_picard_inclusion_on_every_cell_validated: bool
    strict_central_first_variation_picard_inclusion_on_every_cell_validated: bool
    strict_full_label_second_variation_picard_inclusion_on_every_cell_validated: bool
    exact_label_mean_value_reconstruction_used: bool
    local_defect_and_rectangular_wrapping_enclosed_outward: bool
    binary64_rk4_guide_used_only_as_nonclaim_center: bool
    binary64_sampling_or_flow_values_used_to_accept_a_margin: bool
    same_kernel_256_bit_precision_replay_validated: bool
    full_first_method_step_interval_cover_validated: bool
    first_method_step_physical_p_matrix_cover_validated: bool
    first_method_step_early_x_monotonicity_interval_validated: bool
    full_physical_strip_interval_cover_validated: bool
    physical_cross_separation_interval_validated: bool
    expanded_open_collar_interval_validated: bool
    target_chart_global_embedding_validated: bool
    target_global_graph_fixed_point_validated: bool


RIGOROUS_TRUE_FLAGS = (
    "exact_first_method_step_delay_regime_verified",
    "exact_c4_patch_x_and_first_two_label_derivatives_verified",
    "exact_state_first_second_variational_reduction_verified",
    "exact_cubic_hermite_endpoint_identities_verified",
    "exact_bernstein_convex_hull_range_theorem_used",
    "strict_central_state_picard_inclusion_on_every_cell_validated",
    "strict_central_first_variation_picard_inclusion_on_every_cell_validated",
    "strict_full_label_second_variation_picard_inclusion_on_every_cell_validated",
    "exact_label_mean_value_reconstruction_used",
    "local_defect_and_rectangular_wrapping_enclosed_outward",
    "binary64_rk4_guide_used_only_as_nonclaim_center",
    "same_kernel_256_bit_precision_replay_validated",
    "full_first_method_step_interval_cover_validated",
    "first_method_step_physical_p_matrix_cover_validated",
    "first_method_step_early_x_monotonicity_interval_validated",
)
FALSE_METHOD_FLAGS = (
    "binary64_sampling_or_flow_values_used_to_accept_a_margin",
)
OPEN_FLAGS = (
    "full_physical_strip_interval_cover_validated",
    "physical_cross_separation_interval_validated",
    "expanded_open_collar_interval_validated",
    "target_chart_global_embedding_validated",
    "target_global_graph_fixed_point_validated",
)


def _decimal(value: object, name: str) -> Decimal:
    if not isinstance(value, (str, int)) or isinstance(value, bool):
        raise ValueError(f"{name} must be an exact decimal string or integer")
    try:
        result = Decimal(value)
    except InvalidOperation as error:
        raise ValueError(f"{name} is not a decimal") from error
    if not result.is_finite():
        raise ValueError(f"{name} must be finite")
    return result


def _validate_closed_probe(probe: CoverProbe, precision: int) -> None:
    if probe.precision_bits != precision:
        raise AssertionError("the cover precision changed")
    if probe.first_failure is not None:
        raise AssertionError(f"the interval cover failed at {probe.first_failure}")
    if probe.completed_label_cells != 20 or probe.completed_time_cells != 8000:
        raise AssertionError("the interval cover did not traverse the exact grid")
    if probe.c4_patch_cell_count != 1000:
        raise AssertionError("the interval cover has the wrong C4 patch count")
    for name in (
        "minimum_central_picard_gap",
        "minimum_first_variation_picard_gap",
        "minimum_second_variation_picard_gap",
        "minimum_time_minor",
        "minimum_label_minor",
        "minimum_oriented_determinant",
    ):
        if _decimal(getattr(probe, name), name) <= 0:
            raise AssertionError(f"{name} is not strictly positive")
    if _decimal(probe.maximum_raw_determinant, "maximum raw determinant") >= 0:
        raise AssertionError("the raw determinant is not strictly negative")
    if _decimal(
        probe.maximum_early_x_time_derivative,
        "maximum early X time derivative",
    ) >= 0:
        raise AssertionError("early physical X is not strictly decreasing")
    if len(probe.proof_cell_digest_sha256) != 64:
        raise AssertionError("the proof-cell digest has the wrong length")


@lru_cache(maxsize=1)
def build_target_first_method_step_cover_certificate(
) -> TargetFirstMethodStepCoverCertificate:
    """Build and replay the complete 8,000-cell first-step certificate."""

    defects = exact_first_step_cover_defects()
    if any(defect != 0 for defect in defects):
        raise AssertionError("an exact first-step cover identity failed")
    primary = probe_cover(PRIMARY_PRECISION_BITS)
    refinement = probe_cover(REFINEMENT_PRECISION_BITS)
    _validate_closed_probe(primary, PRIMARY_PRECISION_BITS)
    _validate_closed_probe(refinement, REFINEMENT_PRECISION_BITS)
    return TargetFirstMethodStepCoverCertificate(
        model_id=MODEL_ID,
        audit_id=AUDIT_ID,
        arithmetic=MANIFEST_ARITHMETIC,
        coordinate_order=(
            "X",
            "Y",
            "partial_lambda X",
            "partial_lambda Y",
            "partial_lambda_lambda X",
            "partial_lambda_lambda Y",
        ),
        physical_output_frame=((-7, 2), (3, 1)),
        physical_frame_determinant=-13,
        physical_time_interval=(TIME_LEFT, TIME_RIGHT),
        label_interval=(LABEL_LEFT, LABEL_RIGHT),
        time_step=TIME_STEP,
        label_step=LABEL_STEP,
        time_cell_count_per_label=400,
        label_cell_count=20,
        total_time_label_cell_count=8000,
        patch_entry_time=PATCH_ENTRY_TIME,
        patch_time_cell_count_per_label=50,
        primary=primary,
        refinement=refinement,
        exact_symbolic_zero_defect_count=len(defects),
        exact_delay_regime=(
            "on -3<=t<=1, t-5<=-4 stays in the affine far history; "
            "t-4 stays affine for t<=1/2 and traverses exactly the C4 "
            "Hermite patch -3.5<=t-4<=-3 for 1/2<=t<=1"
        ),
        parameter_reconstruction=(
            "z_lambda(t,Lambda) subset z_lambda(t,lambda_c) + "
            "(Lambda-lambda_c) z_lambda_lambda(t,Lambda), followed by "
            "z(t,Lambda) subset z(t,lambda_c) + "
            "(Lambda-lambda_c) z_lambda(t,Lambda)"
        ),
        wrapping_method=(
            "strict rectangular Picard inclusion in moving cubic-Hermite "
            "error coordinates, separately for the central state, central "
            "first variation, and full-label second variation"
        ),
        local_defect_method=(
            "the exact polynomial residual f(t,p+E)-p_t is converted from "
            "power to Bernstein form on each normalized-time cell; its "
            "convex hull bounds the full integral defect and endpoint error"
        ),
        exact_scope=(
            "a rigorous state-plus-true-label-variation P-matrix cover of "
            "[-3,1]x[-1/20,1/20], the complete first method-of-steps strip"
        ),
        open_scope=(
            "the remaining physical interval (1,3], the late cross-"
            "separation inequality through t=3, an enlarged label collar, "
            "the glued global embedding, target graph, and history root"
        ),
        exact_first_method_step_delay_regime_verified=True,
        exact_c4_patch_x_and_first_two_label_derivatives_verified=True,
        exact_state_first_second_variational_reduction_verified=True,
        exact_cubic_hermite_endpoint_identities_verified=True,
        exact_bernstein_convex_hull_range_theorem_used=True,
        strict_central_state_picard_inclusion_on_every_cell_validated=True,
        strict_central_first_variation_picard_inclusion_on_every_cell_validated=True,
        strict_full_label_second_variation_picard_inclusion_on_every_cell_validated=True,
        exact_label_mean_value_reconstruction_used=True,
        local_defect_and_rectangular_wrapping_enclosed_outward=True,
        binary64_rk4_guide_used_only_as_nonclaim_center=True,
        binary64_sampling_or_flow_values_used_to_accept_a_margin=False,
        same_kernel_256_bit_precision_replay_validated=True,
        full_first_method_step_interval_cover_validated=True,
        first_method_step_physical_p_matrix_cover_validated=True,
        first_method_step_early_x_monotonicity_interval_validated=True,
        full_physical_strip_interval_cover_validated=False,
        physical_cross_separation_interval_validated=False,
        expanded_open_collar_interval_validated=False,
        target_chart_global_embedding_validated=False,
        target_global_graph_fixed_point_validated=False,
    )


def json_ready_target_first_method_step_cover() -> dict[str, Any]:
    return json.loads(
        json.dumps(
            {
                "certificate": asdict(
                    build_target_first_method_step_cover_certificate()
                )
            }
        )
    )


def validate_target_first_method_step_cover_audit(
    payload: Mapping[str, Any],
) -> None:
    """Reject altered bounds, missing provenance claims, and promotion."""

    if not isinstance(payload, Mapping):
        raise ValueError("the first-method-step audit must be a mapping")
    certificate = payload.get("certificate")
    if not isinstance(certificate, Mapping):
        raise ValueError("the first-method-step certificate must be a mapping")
    expected_fields = {
        field.name for field in fields(TargetFirstMethodStepCoverCertificate)
    }
    if set(certificate) != expected_fields:
        raise ValueError("the first-method-step certificate fields changed")
    if any(certificate.get(name) is not True for name in RIGOROUS_TRUE_FLAGS):
        raise ValueError("a rigorous first-method-step flag was weakened")
    if any(certificate.get(name) is not False for name in FALSE_METHOD_FLAGS):
        raise ValueError("a forbidden acceptance method flag was promoted")
    if any(certificate.get(name) is not False for name in OPEN_FLAGS):
        raise ValueError("an open target-chart claim was promoted")
    boolean_fields = {
        field.name
        for field in fields(TargetFirstMethodStepCoverCertificate)
        if field.type in (bool, "bool")
    }
    if boolean_fields != (
        set(RIGOROUS_TRUE_FLAGS) | set(FALSE_METHOD_FLAGS) | set(OPEN_FLAGS)
    ):
        raise AssertionError("the first-method-step claim ledger is incomplete")
    for probe_name in ("primary", "refinement"):
        probe = certificate.get(probe_name)
        if not isinstance(probe, Mapping):
            raise ValueError(f"the {probe_name} cover probe is missing")
        if probe.get("first_failure") is not None:
            raise ValueError(f"the {probe_name} cover records a failure")
        if probe.get("completed_time_cells") != 8000:
            raise ValueError(f"the {probe_name} cover is incomplete")
        for name in (
            "minimum_central_picard_gap",
            "minimum_first_variation_picard_gap",
            "minimum_second_variation_picard_gap",
            "minimum_time_minor",
            "minimum_label_minor",
            "minimum_oriented_determinant",
        ):
            if _decimal(probe.get(name), f"{probe_name} {name}") <= 0:
                raise ValueError(f"the {probe_name} {name} is not positive")
        if _decimal(
            probe.get("maximum_raw_determinant"),
            f"{probe_name} maximum raw determinant",
        ) >= 0:
            raise ValueError(f"the {probe_name} raw determinant is not negative")
        if _decimal(
            probe.get("maximum_early_x_time_derivative"),
            f"{probe_name} early X derivative",
        ) >= 0:
            raise ValueError(f"the {probe_name} early X derivative is not negative")
    if dict(payload) != json_ready_target_first_method_step_cover():
        raise ValueError("the first-method-step audit differs from reference")


def _sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def validate_target_first_method_step_cover_result(
    payload: Mapping[str, Any], repository: Path
) -> None:
    """Validate the generated cover and every local source digest."""

    if not isinstance(payload, Mapping):
        raise ValueError("the first-method-step result must be a mapping")
    audit = payload.get("audit")
    manifest = payload.get("manifest")
    if not isinstance(audit, Mapping) or not isinstance(manifest, Mapping):
        raise ValueError("the result requires audit and manifest mappings")
    validate_target_first_method_step_cover_audit(audit)
    paths = {
        "proof_source": PROOF_SOURCE_RELATIVE_PATH,
        "generator": GENERATOR_RELATIVE_PATH,
        "note": NOTE_RELATIVE_PATH,
        "interval_backend_source": INTERVAL_BACKEND_SOURCE_RELATIVE_PATH,
        "physical_model_source": PHYSICAL_MODEL_SOURCE_RELATIVE_PATH,
        "c4_seam_source": C4_SEAM_SOURCE_RELATIVE_PATH,
        "single_cell_source": SINGLE_CELL_SOURCE_RELATIVE_PATH,
        "univalence_gate_source": UNIVALENCE_GATE_SOURCE_RELATIVE_PATH,
    }
    for name, relative in paths.items():
        if manifest.get(name) != relative:
            raise ValueError(f"manifest {name} path changed")
        if manifest.get(f"{name}_sha256") != _sha256(repository / relative):
            raise ValueError(f"manifest {name} hash changed")
    if manifest.get("default_command") != DEFAULT_COMMAND:
        raise ValueError("manifest command changed")
    if manifest.get("arithmetic") != MANIFEST_ARITHMETIC:
        raise ValueError("manifest arithmetic changed")
    if manifest.get("python") != platform.python_version():
        raise ValueError("manifest Python version changed")
    if manifest.get("platform") != platform.platform():
        raise ValueError("manifest platform changed")
    if manifest.get("gmpy2") != gmpy2.version():
        raise ValueError("manifest gmpy2 version changed")
    if manifest.get("mpfr") != gmpy2.mpfr_version():
        raise ValueError("manifest MPFR version changed")


__all__ = [
    "AUDIT_ID",
    "CoverProbe",
    "DEFAULT_COMMAND",
    "FALSE_METHOD_FLAGS",
    "GENERATOR_RELATIVE_PATH",
    "LABEL_LEFT",
    "LABEL_RIGHT",
    "LABEL_STEP",
    "MANIFEST_ARITHMETIC",
    "MODEL_ID",
    "NOTE_RELATIVE_PATH",
    "OPEN_FLAGS",
    "PATCH_ENTRY_TIME",
    "PRIMARY_PRECISION_BITS",
    "REFINEMENT_PRECISION_BITS",
    "RESULT_RELATIVE_PATH",
    "RIGOROUS_TRUE_FLAGS",
    "TIME_LEFT",
    "TIME_RIGHT",
    "TIME_STEP",
    "TargetFirstMethodStepCoverCertificate",
    "build_target_first_method_step_cover_certificate",
    "exact_first_step_cover_defects",
    "json_ready_target_first_method_step_cover",
    "probe_cover",
    "validate_target_first_method_step_cover_audit",
    "validate_target_first_method_step_cover_result",
]
