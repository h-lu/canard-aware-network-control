"""Small MPFR-directed interval and complex Fourier arithmetic.

The implementation uses :mod:`gmpy2`, whose real operations delegate to
MPFR with an explicitly selected rounding mode.  It is intentionally small:
it supports the algebra and trigonometric operations needed by the FHN
periodic validation experiment, and rejects division by an interval that
contains zero.

Unlike ``numpy.nextafter`` wrappers, the elementary functions here are
evaluated by MPFR itself under downward/upward rounding.  This makes the
endpoints suitable for proof diagnostics, subject to the stated MPFR
backend and precision.
"""

from __future__ import annotations

from dataclasses import dataclass
import math

import gmpy2


def _context(precision: int, rounding: int) -> gmpy2.context:
    if isinstance(precision, bool) or int(precision) != precision or precision < 64:
        raise ValueError("precision must be an integer of at least 64 bits")
    return gmpy2.context(precision=int(precision), round=rounding)


def _down(value: object, precision: int) -> gmpy2.mpfr:
    with _context(precision, gmpy2.RoundDown):
        return gmpy2.mpfr(value)


def _up(value: object, precision: int) -> gmpy2.mpfr:
    with _context(precision, gmpy2.RoundUp):
        return gmpy2.mpfr(value)


@dataclass(frozen=True)
class DirectedInterval:
    """Closed real interval with MPFR endpoints at one fixed precision."""

    lower: gmpy2.mpfr
    upper: gmpy2.mpfr
    precision: int = 160

    def __post_init__(self) -> None:
        if self.precision < 64:
            raise ValueError("precision must be at least 64 bits")
        if (
            self.lower.precision != self.precision
            or self.upper.precision != self.precision
        ):
            raise ValueError("endpoint precision does not match interval precision")
        if not gmpy2.is_finite(self.lower) or not gmpy2.is_finite(self.upper):
            raise ValueError("interval endpoints must be finite")
        if self.lower > self.upper:
            raise ValueError("lower endpoint exceeds upper endpoint")

    @classmethod
    def from_float(cls, value: float, precision: int = 160) -> DirectedInterval:
        """Return the exact binary64 value as a zero-width MPFR interval."""

        number = float(value)
        if not math.isfinite(number):
            raise ValueError("point must be finite")
        # A binary64 number has at most 53 significant bits, hence conversion
        # at precision >=64 is exact under either directed mode.
        return cls(_down(number, precision), _up(number, precision), precision)

    @classmethod
    def from_decimal(
        cls, value: str | int, precision: int = 160
    ) -> DirectedInterval:
        """Enclose an exact decimal string or integer."""

        return cls(_down(value, precision), _up(value, precision), precision)

    @classmethod
    def from_bounds(
        cls,
        lower: str | int | float | gmpy2.mpfr,
        upper: str | int | float | gmpy2.mpfr,
        precision: int = 160,
    ) -> DirectedInterval:
        return cls(_down(lower, precision), _up(upper, precision), precision)

    @classmethod
    def symmetric_radius(
        cls,
        center: float,
        radius: gmpy2.mpfr | str | float,
        precision: int = 160,
    ) -> DirectedInterval:
        point = cls.from_float(center, precision)
        rad = cls.from_bounds(radius, radius, precision)
        if rad.lower < 0:
            raise ValueError("radius must be nonnegative")
        with _context(precision, gmpy2.RoundDown):
            lower = point.lower - rad.upper
        with _context(precision, gmpy2.RoundUp):
            upper = point.upper + rad.upper
        return cls(lower, upper, precision)

    def _coerce(self, other: object) -> DirectedInterval:
        if isinstance(other, DirectedInterval):
            if other.precision != self.precision:
                raise ValueError("interval precisions must agree")
            return other
        if isinstance(other, int):
            return DirectedInterval.from_decimal(other, self.precision)
        if isinstance(other, str):
            return DirectedInterval.from_decimal(other, self.precision)
        if isinstance(other, (float, gmpy2.mpfr)):
            return DirectedInterval.from_bounds(other, other, self.precision)
        raise TypeError(f"cannot coerce {type(other).__name__} to interval")

    def __add__(self, other: object) -> DirectedInterval:
        item = self._coerce(other)
        with _context(self.precision, gmpy2.RoundDown):
            lower = self.lower + item.lower
        with _context(self.precision, gmpy2.RoundUp):
            upper = self.upper + item.upper
        return DirectedInterval(lower, upper, self.precision)

    def __radd__(self, other: object) -> DirectedInterval:
        return self + other

    def __neg__(self) -> DirectedInterval:
        # Unary MPFR operations otherwise inherit the process's current
        # context (often 53 bits), so retain both the declared precision and
        # directed endpoints explicitly.
        with _context(self.precision, gmpy2.RoundDown):
            lower = -self.upper
        with _context(self.precision, gmpy2.RoundUp):
            upper = -self.lower
        return DirectedInterval(lower, upper, self.precision)

    def __sub__(self, other: object) -> DirectedInterval:
        return self + (-self._coerce(other))

    def __rsub__(self, other: object) -> DirectedInterval:
        return self._coerce(other) - self

    def __mul__(self, other: object) -> DirectedInterval:
        item = self._coerce(other)
        with _context(self.precision, gmpy2.RoundDown):
            lower_products = (
                self.lower * item.lower,
                self.lower * item.upper,
                self.upper * item.lower,
                self.upper * item.upper,
            )
            lower = min(lower_products)
        with _context(self.precision, gmpy2.RoundUp):
            upper_products = (
                self.lower * item.lower,
                self.lower * item.upper,
                self.upper * item.lower,
                self.upper * item.upper,
            )
            upper = max(upper_products)
        return DirectedInterval(lower, upper, self.precision)

    def __rmul__(self, other: object) -> DirectedInterval:
        return self * other

    def __truediv__(self, other: object) -> DirectedInterval:
        item = self._coerce(other)
        if item.lower <= 0 <= item.upper:
            raise ZeroDivisionError("division interval contains zero")
        with _context(self.precision, gmpy2.RoundDown):
            lower_values = (
                self.lower / item.lower,
                self.lower / item.upper,
                self.upper / item.lower,
                self.upper / item.upper,
            )
            lower = min(lower_values)
        with _context(self.precision, gmpy2.RoundUp):
            upper_values = (
                self.lower / item.lower,
                self.lower / item.upper,
                self.upper / item.lower,
                self.upper / item.upper,
            )
            upper = max(upper_values)
        return DirectedInterval(lower, upper, self.precision)

    def __rtruediv__(self, other: object) -> DirectedInterval:
        return self._coerce(other) / self

    def __pow__(self, exponent: int) -> DirectedInterval:
        if isinstance(exponent, bool) or int(exponent) != exponent or exponent < 0:
            raise ValueError("only nonnegative integer powers are supported")
        power = int(exponent)
        if power == 0:
            return DirectedInterval.from_decimal(1, self.precision)
        if power % 2 == 1:
            with _context(self.precision, gmpy2.RoundDown):
                lower = self.lower**power
            with _context(self.precision, gmpy2.RoundUp):
                upper = self.upper**power
            return DirectedInterval(lower, upper, self.precision)
        with _context(self.precision, gmpy2.RoundDown):
            if self.lower <= 0 <= self.upper:
                lower = gmpy2.mpfr(0)
            else:
                lower = min(self.lower**power, self.upper**power)
        with _context(self.precision, gmpy2.RoundUp):
            upper = max(self.lower**power, self.upper**power)
        return DirectedInterval(lower, upper, self.precision)

    def sqrt(self) -> DirectedInterval:
        if self.lower < 0:
            raise ValueError("square root interval crosses the negative axis")
        with _context(self.precision, gmpy2.RoundDown):
            lower = gmpy2.sqrt(self.lower)
        with _context(self.precision, gmpy2.RoundUp):
            upper = gmpy2.sqrt(self.upper)
        return DirectedInterval(lower, upper, self.precision)

    def intersects(self, other: DirectedInterval) -> bool:
        item = self._coerce(other)
        return not (self.upper < item.lower or item.upper < self.lower)

    def contains_zero(self) -> bool:
        return self.lower <= 0 <= self.upper

    def upper_abs(self) -> gmpy2.mpfr:
        with _context(self.precision, gmpy2.RoundUp):
            return max(abs(self.lower), abs(self.upper))

    def lower_abs(self) -> gmpy2.mpfr:
        """Return a downward bound for the distance of this interval from zero."""

        if self.contains_zero():
            return _down(0, self.precision)
        with _context(self.precision, gmpy2.RoundDown):
            return min(abs(self.lower), abs(self.upper))

    def width_upper(self) -> gmpy2.mpfr:
        with _context(self.precision, gmpy2.RoundUp):
            return self.upper - self.lower

    def midpoint_nearest(self) -> gmpy2.mpfr:
        with _context(self.precision, gmpy2.RoundToNearest):
            return (self.lower + self.upper) / 2

    def decimal_bounds(self, digits: int = 40) -> tuple[str, str]:
        return (
            decimal_lower(self.lower, digits),
            decimal_upper(self.upper, digits),
        )


def pi_interval(precision: int = 160) -> DirectedInterval:
    with _context(precision, gmpy2.RoundDown):
        lower = gmpy2.const_pi()
    with _context(precision, gmpy2.RoundUp):
        upper = gmpy2.const_pi()
    return DirectedInterval(lower, upper, precision)


def _critical_interval(
    coefficient_numerator: int,
    coefficient_denominator: int,
    precision: int,
) -> DirectedInterval:
    return (
        pi_interval(precision)
        * DirectedInterval.from_decimal(coefficient_numerator, precision)
        / DirectedInterval.from_decimal(coefficient_denominator, precision)
    )


def _trig_interval(value: DirectedInterval, *, cosine: bool) -> DirectedInterval:
    """Enclose sine or cosine, including any interior extrema."""

    precision = value.precision
    two_pi = pi_interval(precision) * 2
    if value.width_upper() >= two_pi.lower:
        return DirectedInterval.from_bounds(-1, 1, precision)

    function = gmpy2.cos if cosine else gmpy2.sin
    with _context(precision, gmpy2.RoundDown):
        endpoint_lower = min(function(value.lower), function(value.upper))
    with _context(precision, gmpy2.RoundUp):
        endpoint_upper = max(function(value.lower), function(value.upper))

    # Work out the relevant turns with directed MPFR division.  Using a
    # binary64 quotient here would be unsafe for very large arguments.
    turns = value / two_pi
    if turns.width_upper() >= 1:
        # Argument reduction is then too uncertain to exclude a full pair
        # of extrema.  The full range is safe and avoids an unbounded scan.
        return DirectedInterval.from_bounds(-1, 1, precision)
    first_n = int(gmpy2.floor(turns.lower)) - 2
    last_n = int(gmpy2.ceil(turns.upper)) + 2
    include_maximum = False
    include_minimum = False
    for index in range(first_n, last_n + 1):
        if cosine:
            maximum = _critical_interval(2 * index, 1, precision)
            minimum = _critical_interval(2 * index + 1, 1, precision)
        else:
            maximum = _critical_interval(4 * index + 1, 2, precision)
            minimum = _critical_interval(4 * index - 1, 2, precision)
        include_maximum = include_maximum or value.intersects(maximum)
        include_minimum = include_minimum or value.intersects(minimum)
    if include_maximum:
        endpoint_upper = _up(1, precision)
    if include_minimum:
        endpoint_lower = _down(-1, precision)
    return DirectedInterval(endpoint_lower, endpoint_upper, precision)


def sin_interval(value: DirectedInterval) -> DirectedInterval:
    return _trig_interval(value, cosine=False)


def cos_interval(value: DirectedInterval) -> DirectedInterval:
    return _trig_interval(value, cosine=True)


@dataclass(frozen=True)
class DirectedComplexInterval:
    """Rectangular complex interval built from directed real intervals."""

    real: DirectedInterval
    imag: DirectedInterval

    def __post_init__(self) -> None:
        if self.real.precision != self.imag.precision:
            raise ValueError("real and imaginary precisions must agree")

    @property
    def precision(self) -> int:
        return self.real.precision

    @classmethod
    def zero(cls, precision: int = 160) -> DirectedComplexInterval:
        zero = DirectedInterval.from_decimal(0, precision)
        return cls(zero, zero)

    @classmethod
    def from_real(cls, value: DirectedInterval) -> DirectedComplexInterval:
        return cls(value, DirectedInterval.from_decimal(0, value.precision))

    def __add__(self, other: DirectedComplexInterval) -> DirectedComplexInterval:
        return DirectedComplexInterval(self.real + other.real, self.imag + other.imag)

    def __neg__(self) -> DirectedComplexInterval:
        return DirectedComplexInterval(-self.real, -self.imag)

    def __sub__(self, other: DirectedComplexInterval) -> DirectedComplexInterval:
        return self + (-other)

    def __mul__(
        self, other: DirectedComplexInterval | DirectedInterval | int | str | float
    ) -> DirectedComplexInterval:
        if isinstance(other, DirectedComplexInterval):
            return DirectedComplexInterval(
                self.real * other.real - self.imag * other.imag,
                self.real * other.imag + self.imag * other.real,
            )
        scalar = self.real._coerce(other)
        return DirectedComplexInterval(self.real * scalar, self.imag * scalar)

    def __rmul__(
        self, other: DirectedComplexInterval | DirectedInterval | int | str | float
    ) -> DirectedComplexInterval:
        return self * other

    def upper_abs(self) -> gmpy2.mpfr:
        real_abs = self.real.upper_abs()
        imag_abs = self.imag.upper_abs()
        with _context(self.precision, gmpy2.RoundUp):
            return gmpy2.sqrt(real_abs * real_abs + imag_abs * imag_abs)

    def lower_abs(self) -> gmpy2.mpfr:
        """Return a downward bound for distance of the rectangle from zero."""

        real_abs = self.real.lower_abs()
        imag_abs = self.imag.lower_abs()
        with _context(self.precision, gmpy2.RoundDown):
            return gmpy2.sqrt(real_abs * real_abs + imag_abs * imag_abs)


def complex_unit_interval(angle: DirectedInterval) -> DirectedComplexInterval:
    """Enclose ``exp(i*angle)``."""

    return DirectedComplexInterval(cos_interval(angle), sin_interval(angle))


def upward_sum(
    values: list[gmpy2.mpfr] | tuple[gmpy2.mpfr, ...], precision: int
) -> gmpy2.mpfr:
    with _context(precision, gmpy2.RoundUp):
        total = gmpy2.mpfr(0)
        for value in values:
            total += value
    return total


def downward_sum(
    values: list[gmpy2.mpfr] | tuple[gmpy2.mpfr, ...], precision: int
) -> gmpy2.mpfr:
    with _context(precision, gmpy2.RoundDown):
        total = gmpy2.mpfr(0)
        for value in values:
            total += value
        return total


def upward_product(
    left: gmpy2.mpfr, right: gmpy2.mpfr, precision: int
) -> gmpy2.mpfr:
    with _context(precision, gmpy2.RoundUp):
        return left * right


def upward_division(
    numerator: gmpy2.mpfr, denominator: gmpy2.mpfr, precision: int
) -> gmpy2.mpfr:
    if denominator <= 0:
        raise ValueError("upper division requires a positive denominator")
    with _context(precision, gmpy2.RoundUp):
        return numerator / denominator


def _safe_decimal_digits(value: gmpy2.mpfr, requested: int) -> int:
    # Five guard digits beyond the round-trip requirement ensure that the
    # decimal conversion error is much smaller than one MPFR ulp.
    return max(requested, math.ceil(value.precision * math.log10(2.0)) + 5)


def decimal_upper(value: gmpy2.mpfr, digits: int = 40) -> str:
    """Return a decimal real number guaranteed to be at least ``value``."""

    pushed = gmpy2.next_above(value)
    count = _safe_decimal_digits(value, digits)
    return format(pushed, f".{count}g")


def decimal_lower(value: gmpy2.mpfr, digits: int = 40) -> str:
    """Return a decimal real number guaranteed to be at most ``value``."""

    pushed = gmpy2.next_below(value)
    count = _safe_decimal_digits(value, digits)
    return format(pushed, f".{count}g")
