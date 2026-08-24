"""Exact and directed raw-slot/product-tube comparison certificate.

The raw singular-slot sigma clock reverses at the fixed target amplitude.
This module constructs a C3 comparison phase that equals sigma on the
incoming tail, uses the normal drift on the core, and has a positive
derivative on an explicit independent-slot product tube for a declared nu
box.  It does not construct a phase on an actual target causal graph, prove
that a graph exists, or prove that the product tube is invariant.

At the frozen numerical operating anchor, an exact raw-slot equilibrium
family puts a zero vector inside the same radius-1/1000 product geometry.
Consequently the declared parameter box cannot be enlarged to that anchor
while retaining any strictly positive C1 phase clock on the product tube.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
import json
import math
from pathlib import Path
from typing import Any, Sequence

import gmpy2
import sympy as sp

from canard_control.directed_interval import DirectedInterval
from canard_control.fixed_epsilon_clocked_tail_graph_extension import (
    LEFT_PLATEAU_START,
    RIGHT_PLATEAU_END,
    validate_clocked_tail_graph_result,
)


TARGET_RHO_SQUARED = Fraction(1, 5)
TARGET_ETA = 0
TARGET_NU_LOWER = Fraction(0)
TARGET_NU_UPPER = Fraction(1, 5)
TARGET_ANCHOR_NU_DECIMAL = "0.21256022233963731"
TARGET_ANCHOR_NU = Fraction(TARGET_ANCHOR_NU_DECIMAL)
NO_GO_NU_LOWER = Fraction(1, 10)
NO_GO_NU_UPPER = Fraction(1, 4)
CORE_PHASE_LEFT = -20
CORE_PHASE_RIGHT = 20
TAPER_LEFT = -6
TAPER_RIGHT = -5
TILT_SCALE = 8
SLOT_TUBE_RADIUS = Fraction(1, 1000)
PARTITION_DENOMINATOR = 500
PARTITION_CELLS = 20000
RAW_CLOCK_LOWER = Fraction(1, 200)
TUBE_CLOCK_LOWER = Fraction(1, 1000)
GRADIENT_SQUARED_LOWER = Fraction(1, 100)
PRECISION_BITS = 256

STALL_PHASE_BRACKETS = (
    ("-4.143276804", "-4.143276802"),
    ("-0.193924651", "-0.193924650"),
    ("2.312201453", "2.312201455"),
)

CLOCKED_TAIL_RESULT_SHA256 = (
    "826c8ddbd2e9794cec344456f09ccefc8d4d8d737950350859f1679691f1760e"
)

PROOF_SOURCE_RELATIVE_PATH = (
    "src/canard_control/fixed_epsilon_target_tilted_phase.py"
)
GENERATOR_RELATIVE_PATH = (
    "experiments/fixed_epsilon_target_tilted_phase.py"
)
RESULT_RELATIVE_PATH = (
    "experiments/results/fixed_epsilon_target_tilted_phase.json"
)
NOTE_RELATIVE_PATH = "docs/fixed-epsilon-target-tilted-phase.md"
PARENT_RESULT_RELATIVE_PATH = (
    "experiments/results/fixed_epsilon_clocked_tail_graph_extension.json"
)
DEFAULT_COMMAND = (
    "PYTHONPATH=src /usr/bin/python3 "
    "experiments/fixed_epsilon_target_tilted_phase.py"
)
MANIFEST_ARITHMETIC = (
    "exact Sturm arithmetic over Q(sqrt(5)) and 256-bit MPFR-directed "
    "interval arithmetic on 20000 rational raw-slot product-tube cells and "
    "the frozen-decimal target-anchor equilibrium; no actual target causal "
    "phase, target graph, tube invariance, trace, Fredholm inverse, root, "
    "network lift, or biological-control validation"
)

PROVED_FLAGS = (
    "target_raw_coordinate_algebra_proved",
    "raw_sigma_speed_has_three_simple_real_zeros_proved",
    "raw_stall_locus_and_phase_no_go_proved",
    "central_stall_lies_in_comparison_box_proved",
    "constant_affine_phase_no_go_on_nu_box_proved",
    "target_anchor_raw_slot_equilibrium_algebra_proved",
    "target_anchor_raw_slot_equilibrium_enclosed_256_bit",
    "target_anchor_raw_slot_zero_lies_in_product_tube_proved",
    "target_anchor_product_tube_positive_clock_no_go_proved",
    "tapered_phase_matches_incoming_sigma_clock_proved",
    "tapered_raw_clock_uniform_on_nu_box_proved",
    "incoming_to_core_sigma_clock_on_slot_tube_proved",
    "declared_slot_tube_lies_in_unit_plateau_proved",
    "raw_slot_product_tapered_clock_validated",
    "raw_slot_product_tapered_phase_submersion_validated",
    "parent_clock_failure_and_small_rho_graph_replayed",
)
OPEN_FLAGS = (
    "target_graph_candidate_computed",
    "target_slot_tube_invariant_under_backward_flows_validated",
    "target_graph_transform_self_map_validated",
    "target_graph_fixed_point_validated",
    "target_one_sided_traces_validated",
    "target_w1p_fredholm_inverse_validated",
    "target_complete_history_root_validated",
    "target_general_network_lift_validated",
    "target_biological_control_chain_validated",
)


@dataclass(frozen=True)
class IntervalRecord:
    lower: str
    upper: str


@dataclass(frozen=True)
class SturmRecord:
    parameter: str
    sequence_length: int
    negative_infinity_signs: tuple[int, ...]
    positive_infinity_signs: tuple[int, ...]
    negative_infinity_variations: int
    positive_infinity_variations: int
    real_root_count: int
    sample_at_zero: str


@dataclass(frozen=True)
class TargetRawSlotTiltedPhaseCertificate:
    target_rho_squared: str
    target_eta: int
    target_nu_box: tuple[str, str]
    target_anchor_nu_decimal: str
    target_anchor_nu_exact_rational: str
    target_anchor_scope: str
    no_go_comparison_nu_box: tuple[str, str]
    core_phase_interval: tuple[int, int]
    taper_interval: tuple[int, int]
    tilt_scale: int
    slot_tube_radius: str
    partition_cells: int
    precision_bits: int
    raw_sigma_speed_formula: str
    raw_normal_speed_formula: str
    reference_normal_speed_formula: str
    tapered_phase_formula: str
    raw_tapered_phase_speed_formula: str
    sigma_speed_sturm_sequence_length: int
    sigma_speed_real_root_count: int
    sigma_speed_square_free: bool
    stall_phase_enclosures: tuple[IntervalRecord, ...]
    stall_nu_enclosures: tuple[IntervalRecord, ...]
    target_anchor_slot_g_formula: str
    target_anchor_equilibrium_phase_formula: str
    target_anchor_equilibrium_normal_formula: str
    target_anchor_slot_fast_formula: str
    target_anchor_slot_slow_formula: str
    target_anchor_equilibrium_phase_enclosure: IntervalRecord
    target_anchor_equilibrium_normal_enclosure: IntervalRecord
    target_anchor_equilibrium_g_enclosure: IntervalRecord
    raw_clock_lower: str
    endpoint_sturm_records: tuple[SturmRecord, ...]
    left_corridor_nominal_interval: tuple[int, int]
    left_corridor_x_lower: int
    left_corridor_bracket_upper_at_x_lower: str
    left_corridor_derivative_upper_at_x_lower: str
    left_corridor_phase_speed_lower: str
    tube_clock_lower: str
    worst_tube_phase_speed_cell: int
    worst_tube_phase_speed: IntervalRecord
    gradient_squared_lower: str
    worst_gradient_squared_cell: int
    worst_gradient_squared: IntervalRecord
    minimum_plateau_margin: str
    target_raw_coordinate_algebra_proved: bool
    raw_sigma_speed_has_three_simple_real_zeros_proved: bool
    raw_stall_locus_and_phase_no_go_proved: bool
    central_stall_lies_in_comparison_box_proved: bool
    constant_affine_phase_no_go_on_nu_box_proved: bool
    target_anchor_raw_slot_equilibrium_algebra_proved: bool
    target_anchor_raw_slot_equilibrium_enclosed_256_bit: bool
    target_anchor_raw_slot_zero_lies_in_product_tube_proved: bool
    target_anchor_product_tube_positive_clock_no_go_proved: bool
    tapered_phase_matches_incoming_sigma_clock_proved: bool
    tapered_raw_clock_uniform_on_nu_box_proved: bool
    incoming_to_core_sigma_clock_on_slot_tube_proved: bool
    declared_slot_tube_lies_in_unit_plateau_proved: bool
    raw_slot_product_tapered_clock_validated: bool
    raw_slot_product_tapered_phase_submersion_validated: bool
    parent_clock_failure_and_small_rho_graph_replayed: bool
    target_graph_candidate_computed: bool
    target_slot_tube_invariant_under_backward_flows_validated: bool
    target_graph_transform_self_map_validated: bool
    target_graph_fixed_point_validated: bool
    target_one_sided_traces_validated: bool
    target_w1p_fredholm_inverse_validated: bool
    target_complete_history_root_validated: bool
    target_general_network_lift_validated: bool
    target_biological_control_chain_validated: bool


def _finite(value: object, name: str) -> float:
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result


def _fraction_text(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def _sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def target_raw_sigma_speed(phase: float) -> float:
    """Return S_*(s), the target raw singular-slot sigma speed."""

    s = _finite(phase, "phase")
    numerator = -40.0 * s**3 - 81.0 * s**2 + 369.0 * s - 999.0
    return 1.0 + math.sqrt(5.0) * numerator / 2400.0


def target_raw_normal_speed(phase: float, nu: float) -> float:
    """Return D_nu(s)=s(1-S_*(s))/2+nu/sqrt(5)."""

    s = _finite(phase, "phase")
    nu_value = _finite(nu, "nu")
    return s * (1.0 - target_raw_sigma_speed(s)) / 2.0 + nu_value / math.sqrt(5.0)


def reference_normal_speed(phase: float) -> float:
    """Return D_0(s), the normal speed used in the fixed tilt."""

    return target_raw_normal_speed(phase, 0.0)


def target_raw_slot_g(phase: float) -> float:
    """Return the raw-slot forcing ``g_*(s)=(1-S_*(s))/2``."""

    return (1.0 - target_raw_sigma_speed(phase)) / 2.0


def reference_normal_speed_derivative(phase: float) -> float:
    """Return D_0'(s)."""

    s = _finite(phase, "phase")
    sigma_speed = target_raw_sigma_speed(s)
    sigma_speed_derivative = math.sqrt(5.0) * (
        -120.0 * s**2 - 162.0 * s + 369.0
    ) / 2400.0
    return (1.0 - sigma_speed) / 2.0 - s * sigma_speed_derivative / 2.0


def taper(phase: float) -> float:
    """Return the C3 septic step from zero at -6 to one at -5."""

    s = _finite(phase, "phase")
    z = s - TAPER_LEFT
    if z <= 0.0:
        return 0.0
    if z >= 1.0:
        return 1.0
    return 35.0 * z**4 - 84.0 * z**5 + 70.0 * z**6 - 20.0 * z**7


def taper_derivative(phase: float) -> float:
    """Return the derivative of the C3 septic taper."""

    s = _finite(phase, "phase")
    z = s - TAPER_LEFT
    if z <= 0.0 or z >= 1.0:
        return 0.0
    return 140.0 * z**3 * (1.0 - z) ** 3


def target_tapered_phase(sigma: float, normal: float) -> float:
    """Return the comparison phase vartheta=sigma+8 beta(sigma)D_0(sigma)d."""

    sigma_value = _finite(sigma, "sigma")
    normal_value = _finite(normal, "normal")
    result = sigma_value + (
        TILT_SCALE
        * taper(sigma_value)
        * reference_normal_speed(sigma_value)
        * normal_value
    )
    if not math.isfinite(result):
        raise ValueError("raw-slot comparison phase overflows binary64")
    return result


def target_tapered_phase_gradient(
    sigma: float, normal: float
) -> tuple[float, float]:
    """Return the gradient of the tapered phase in (sigma,d)."""

    sigma_value = _finite(sigma, "sigma")
    normal_value = _finite(normal, "normal")
    beta = taper(sigma_value)
    beta_derivative = taper_derivative(sigma_value)
    normal_speed = reference_normal_speed(sigma_value)
    normal_speed_derivative = reference_normal_speed_derivative(sigma_value)
    tilt = TILT_SCALE * beta * normal_speed
    tilt_derivative = TILT_SCALE * (
        beta_derivative * normal_speed + beta * normal_speed_derivative
    )
    return 1.0 + tilt_derivative * normal_value, tilt


def target_raw_tapered_phase_speed(phase: float, nu: float) -> float:
    """Return L_V vartheta on the target raw singular slots."""

    s = _finite(phase, "phase")
    nu_value = _finite(nu, "nu")
    return target_raw_sigma_speed(s) + (
        TILT_SCALE
        * taper(s)
        * reference_normal_speed(s)
        * target_raw_normal_speed(s, nu_value)
    )


def _exact_expressions() -> dict[str, Any]:
    phase, nu = sp.symbols("s nu", real=True)
    sqrt_five = sp.sqrt(5)
    raw_sigma = sp.expand(
        1
        + sqrt_five
        * (-40 * phase**3 - 81 * phase**2 + 369 * phase - 999)
        / 2400
    )
    reference_normal = sp.expand(phase * (1 - raw_sigma) / 2)
    raw_normal = sp.expand(reference_normal + nu / sqrt_five)
    untapered_phase_speed = sp.expand(
        raw_sigma + TILT_SCALE * reference_normal * raw_normal
    )
    return {
        "phase": phase,
        "nu": nu,
        "raw_sigma": raw_sigma,
        "raw_normal": raw_normal,
        "reference_normal": reference_normal,
        "untapered_phase_speed": untapered_phase_speed,
    }


def _algebraic_sign(value: object) -> int:
    expression = value.as_expr() if hasattr(value, "as_expr") else value
    sign = sp.sign(sp.simplify(expression))
    if sign not in (-1, 1):
        raise ValueError("expected a nonzero exact algebraic number")
    return int(sign)


def _infinity_sign(polynomial: sp.Poly, direction: int) -> int:
    sign = _algebraic_sign(polynomial.LC())
    if direction < 0 and polynomial.degree() % 2:
        sign = -sign
    return sign


def _variations(signs: Sequence[int]) -> int:
    if any(sign not in (-1, 1) for sign in signs):
        raise ValueError("Sturm infinity signs must be nonzero")
    return sum(left != right for left, right in zip(signs, signs[1:]))


def _sturm_record(polynomial: sp.Poly, parameter: Fraction) -> SturmRecord:
    sequence = polynomial.sturm()
    negative_signs = tuple(_infinity_sign(item, -1) for item in sequence)
    positive_signs = tuple(_infinity_sign(item, 1) for item in sequence)
    negative_variations = _variations(negative_signs)
    positive_variations = _variations(positive_signs)
    root_count = negative_variations - positive_variations
    sample = polynomial.eval(0)
    if root_count != 0 or _algebraic_sign(sample) != 1:
        raise ValueError("tapered raw-clock endpoint Sturm check failed")
    return SturmRecord(
        parameter=_fraction_text(parameter),
        sequence_length=len(sequence),
        negative_infinity_signs=negative_signs,
        positive_infinity_signs=positive_signs,
        negative_infinity_variations=negative_variations,
        positive_infinity_variations=positive_variations,
        real_root_count=root_count,
        sample_at_zero=sp.sstr(sample.as_expr()),
    )


@lru_cache(maxsize=1)
def exact_sturm_certificate() -> dict[str, Any]:
    """Return exact clock, reversal, and raw-stall algebra."""

    expressions = _exact_expressions()
    phase = expressions["phase"]
    nu = expressions["nu"]
    raw_sigma_poly = sp.Poly(
        expressions["raw_sigma"], phase, extension=sp.sqrt(5)
    )
    raw_sigma_sequence = raw_sigma_poly.sturm()
    negative_signs = tuple(
        _infinity_sign(item, -1) for item in raw_sigma_sequence
    )
    positive_signs = tuple(
        _infinity_sign(item, 1) for item in raw_sigma_sequence
    )
    raw_sigma_roots = _variations(negative_signs) - _variations(positive_signs)
    square_free = sp.gcd(raw_sigma_poly, raw_sigma_poly.diff()).degree() == 0
    if raw_sigma_roots != 3 or not square_free:
        raise ValueError("raw sigma-speed reversal count failed")

    root_enclosures: list[IntervalRecord] = []
    stall_enclosures: list[IntervalRecord] = []
    precision = PRECISION_BITS
    sqrt_five_interval = DirectedInterval.from_decimal(5, precision).sqrt()
    for lower_text, upper_text in STALL_PHASE_BRACKETS:
        lower = sp.Rational(lower_text)
        upper = sp.Rational(upper_text)
        if raw_sigma_poly.count_roots(lower, upper) != 1:
            raise ValueError("a raw-stall phase bracket is not isolating")
        phase_interval = DirectedInterval.from_bounds(
            lower_text, upper_text, precision
        )
        stall_interval = -sqrt_five_interval * phase_interval / 2
        root_enclosures.append(_interval_record(phase_interval))
        stall_enclosures.append(_interval_record(stall_interval))

    central_stall = stall_enclosures[1]
    no_go_lower = _point_interval(
        NO_GO_NU_LOWER.numerator, NO_GO_NU_LOWER.denominator, precision
    )
    no_go_upper = _point_interval(
        NO_GO_NU_UPPER.numerator, NO_GO_NU_UPPER.denominator, precision
    )
    if not (
        gmpy2.mpfr(central_stall.lower) > no_go_lower.upper
        and gmpy2.mpfr(central_stall.upper) < no_go_upper.lower
    ):
        raise ValueError("central raw-stall parameter left the comparison box")

    raw_lower = sp.Rational(RAW_CLOCK_LOWER.numerator, RAW_CLOCK_LOWER.denominator)
    records: list[SturmRecord] = []
    for endpoint in (TARGET_NU_LOWER, TARGET_NU_UPPER):
        endpoint_value = sp.Rational(endpoint.numerator, endpoint.denominator)
        expression = sp.expand(
            expressions["untapered_phase_speed"].subs(nu, endpoint_value)
            - raw_lower
        )
        records.append(
            _sturm_record(
                sp.Poly(expression, phase, extension=sp.sqrt(5)), endpoint
            )
        )
    if raw_sigma_poly.count_roots(-sp.oo, TAPER_LEFT) != 0:
        raise ValueError("incoming raw sigma clock has an unexpected zero")
    if _algebraic_sign(raw_sigma_poly.eval(TAPER_LEFT) - raw_lower) != 1:
        raise ValueError("incoming raw sigma clock lower bound failed")
    transition_numerator = -40 * phase**3 - 81 * phase**2 + 369 * phase - 999
    transition_derivative = sp.diff(transition_numerator, phase)
    if transition_numerator.subs(phase, TAPER_RIGHT) != 131:
        raise ValueError("left taper transition endpoint value differs")
    if transition_derivative.subs(phase, TAPER_RIGHT) >= 0:
        raise ValueError("left taper transition monotonicity failed")
    if sp.diff(transition_derivative, phase).subs(phase, TAPER_RIGHT) <= 0:
        raise ValueError("left taper transition derivative ordering failed")

    nu_lower = sp.Rational(TARGET_NU_LOWER.numerator, TARGET_NU_LOWER.denominator)
    nu_upper = sp.Rational(TARGET_NU_UPPER.numerator, TARGET_NU_UPPER.denominator)
    raw_normal = expressions["raw_normal"]
    affine_signs = (
        _algebraic_sign(expressions["raw_sigma"].subs(phase, -3)),
        _algebraic_sign(expressions["raw_sigma"].subs(phase, 3)),
        _algebraic_sign(raw_normal.subs({phase: -3, nu: nu_upper})),
        _algebraic_sign(raw_normal.subs({phase: 3, nu: nu_lower})),
    )
    if affine_signs != (-1, -1, -1, 1):
        raise ValueError("constant affine-phase sign obstruction failed")
    return {
        "sigma_sequence_length": len(raw_sigma_sequence),
        "sigma_root_count": raw_sigma_roots,
        "sigma_square_free": square_free,
        "root_enclosures": tuple(root_enclosures),
        "stall_enclosures": tuple(stall_enclosures),
        "endpoint_records": tuple(records),
    }


def _point_interval(
    numerator: int, denominator: int, precision: int
) -> DirectedInterval:
    return (
        DirectedInterval.from_decimal(numerator, precision)
        / DirectedInterval.from_decimal(denominator, precision)
    )


def _closed_interval(
    lower_numerator: int,
    upper_numerator: int,
    denominator: int,
    precision: int,
) -> DirectedInterval:
    lower = _point_interval(lower_numerator, denominator, precision)
    upper = _point_interval(upper_numerator, denominator, precision)
    return DirectedInterval(lower.lower, upper.upper, precision)


def _interval_record(value: DirectedInterval, digits: int = 80) -> IntervalRecord:
    lower, upper = value.decimal_bounds(digits)
    return IntervalRecord(lower=lower, upper=upper)


def _interval_raw_sigma_speed(phase: DirectedInterval) -> DirectedInterval:
    sqrt_five = DirectedInterval.from_decimal(5, phase.precision).sqrt()
    return (
        1
        + sqrt_five
        * (-40 * phase**3 - 81 * phase**2 + 369 * phase - 999)
        / 2400
    )


def _interval_reference_normal_speed(
    phase: DirectedInterval,
) -> DirectedInterval:
    return phase * (1 - _interval_raw_sigma_speed(phase)) / 2


def _interval_reference_normal_speed_derivative(
    phase: DirectedInterval,
) -> DirectedInterval:
    sqrt_five = DirectedInterval.from_decimal(5, phase.precision).sqrt()
    sigma_speed = _interval_raw_sigma_speed(phase)
    sigma_speed_derivative = (
        sqrt_five * (-120 * phase**2 - 162 * phase + 369) / 2400
    )
    return (1 - sigma_speed) / 2 - phase * sigma_speed_derivative / 2


@lru_cache(maxsize=1)
def target_anchor_raw_slot_equilibrium_certificate() -> dict[str, Any]:
    """Certify the frozen-anchor zero of the shifted raw-slot family.

    The decimal anchor is interpreted as the exact rational number written in
    :data:`TARGET_ANCHOR_NU_DECIMAL`.  This is an exact statement about the
    independent raw slots, not a claim that the decimal is a selected root or
    that the slots arise from one RFDE history.
    """

    expressions = _exact_expressions()
    phase = expressions["phase"]
    nu = expressions["nu"]
    normal = sp.symbols("d", real=True)
    sqrt_five = sp.sqrt(5)
    rho = 1 / sqrt_five
    x = -phase / 2
    x_four = -(phase - 4) / 2
    x_five = -(phase - 5) / 2
    fast = sp.expand(
        -sp.Rational(1, 2)
        + normal
        + rho * (-x**3 / 3 + ((x_four + x_five) / 2 - x) / 5)
        + rho**3 * ((x_four**3 + x_five**3) / 2 - x**3) / 4
    )
    slow = sp.expand(phase / 2 + nu / sqrt_five)
    slot_g = sp.expand((1 - expressions["raw_sigma"]) / 2)
    if sp.simplify(fast - (normal - sp.Rational(1, 2) + slot_g)) != 0:
        raise ValueError("target-anchor raw-slot fast identity failed")

    anchor_nu = sp.Rational(
        TARGET_ANCHOR_NU.numerator, TARGET_ANCHOR_NU.denominator
    )
    equilibrium_phase = sp.simplify(-2 * anchor_nu / sqrt_five)
    equilibrium_normal = sp.simplify(
        sp.Rational(1, 2) - slot_g.subs(phase, equilibrium_phase)
    )
    if sp.simplify(
        equilibrium_normal
        - expressions["raw_sigma"].subs(phase, equilibrium_phase) / 2
    ) != 0:
        raise ValueError("target-anchor equilibrium normal identity failed")
    if sp.simplify(
        fast.subs({phase: equilibrium_phase, normal: equilibrium_normal})
    ) != 0:
        raise ValueError("target-anchor raw-slot fast component is nonzero")
    if sp.simplify(
        slow.subs({phase: equilibrium_phase, nu: anchor_nu})
    ) != 0:
        raise ValueError("target-anchor raw-slot slow component is nonzero")

    precision = PRECISION_BITS
    five = DirectedInterval.from_decimal(5, precision)
    half = _point_interval(1, 2, precision)
    anchor_interval = DirectedInterval.from_decimal(
        TARGET_ANCHOR_NU_DECIMAL, precision
    )
    phase_interval = -2 * anchor_interval / five.sqrt()
    sigma_speed_interval = _interval_raw_sigma_speed(phase_interval)
    g_interval = (1 - sigma_speed_interval) / 2
    normal_interval = half - g_interval
    zero = DirectedInterval.from_decimal(0, precision)
    radius = _point_interval(
        SLOT_TUBE_RADIUS.numerator, SLOT_TUBE_RADIUS.denominator, precision
    )
    core_left = DirectedInterval.from_decimal(CORE_PHASE_LEFT, precision)
    core_right = DirectedInterval.from_decimal(CORE_PHASE_RIGHT, precision)
    if not (
        normal_interval.lower > zero.upper
        and normal_interval.upper < radius.lower
    ):
        raise ValueError("target-anchor zero left the radius-1/1000 tube")
    if not (
        phase_interval.lower > core_left.upper
        and phase_interval.upper < core_right.lower
    ):
        raise ValueError("target-anchor zero left the declared core")

    return {
        "slot_g_formula": sp.sstr(slot_g),
        "equilibrium_phase_formula": "s_e=-2*nu_anchor/sqrt(5)",
        "equilibrium_normal_formula": "d_e=1/2-g_*(s_e)=S_*(s_e)/2",
        "slot_fast_formula": "Q_X=d-1/2+g_*(s)",
        "slot_slow_formula": "Q_Y=s/2+nu/sqrt(5)",
        "phase_enclosure": _interval_record(phase_interval),
        "normal_enclosure": _interval_record(normal_interval),
        "g_enclosure": _interval_record(g_interval),
    }


def _taper_point(value: DirectedInterval) -> DirectedInterval:
    return 35 * value**4 - 84 * value**5 + 70 * value**6 - 20 * value**7


def _taper_derivative_point(value: DirectedInterval) -> DirectedInterval:
    return 140 * value**3 * (1 - value) ** 3


def _interval_taper(
    phase: DirectedInterval,
) -> tuple[DirectedInterval, DirectedInterval]:
    precision = phase.precision
    zero = DirectedInterval.from_decimal(0, precision)
    one = DirectedInterval.from_decimal(1, precision)
    shifted = phase - TAPER_LEFT
    if shifted.upper <= 0:
        return zero, zero
    if shifted.lower >= 1:
        return one, zero

    lower_value = max(shifted.lower, gmpy2.mpfr(0))
    upper_value = min(shifted.upper, gmpy2.mpfr(1))
    lower_point = DirectedInterval.from_bounds(
        lower_value, lower_value, precision
    )
    upper_point = DirectedInterval.from_bounds(
        upper_value, upper_value, precision
    )
    lower_taper = _taper_point(lower_point)
    upper_taper = _taper_point(upper_point)
    taper_lower = zero.lower if shifted.lower <= 0 else lower_taper.lower
    taper_upper = one.upper if shifted.upper >= 1 else upper_taper.upper

    lower_derivative = _taper_derivative_point(lower_point)
    upper_derivative = _taper_derivative_point(upper_point)
    if shifted.lower <= 0 or shifted.upper >= 1:
        derivative_lower = zero.lower
    else:
        derivative_lower = min(
            lower_derivative.lower, upper_derivative.lower
        )
    half = DirectedInterval.from_decimal("0.5", precision)
    if lower_value <= half.lower <= upper_value:
        derivative_upper = (DirectedInterval.from_decimal(35, precision) / 16).upper
    else:
        derivative_upper = max(
            lower_derivative.upper, upper_derivative.upper
        )
    return (
        DirectedInterval.from_bounds(taper_lower, taper_upper, precision),
        DirectedInterval.from_bounds(
            derivative_lower, derivative_upper, precision
        ),
    )


def _target_slot_tube_cell(
    index: int, precision: int
) -> tuple[DirectedInterval, DirectedInterval, DirectedInterval]:
    if isinstance(index, bool) or not 0 <= index < PARTITION_CELLS:
        raise ValueError("cell index is outside the target partition")
    phase_cell = _closed_interval(
        CORE_PHASE_LEFT * PARTITION_DENOMINATOR + index,
        CORE_PHASE_LEFT * PARTITION_DENOMINATOR + index + 1,
        PARTITION_DENOMINATOR,
        precision,
    )
    radius = _closed_interval(-1, 1, SLOT_TUBE_RADIUS.denominator, precision)
    nu = _closed_interval(
        TARGET_NU_LOWER.numerator,
        TARGET_NU_UPPER.numerator,
        TARGET_NU_UPPER.denominator,
        precision,
    )
    return phase_cell, radius, nu


def target_slot_tube_cell_bounds(
    index: int, precision: int = PRECISION_BITS
) -> tuple[DirectedInterval, DirectedInterval]:
    """Return phase-speed and gradient-square bounds for one rational cell."""

    phase_cell, radius, nu = _target_slot_tube_cell(index, precision)
    one = DirectedInterval.from_decimal(1, precision)
    rho = one / DirectedInterval.from_decimal(5, precision).sqrt()
    sigma = phase_cell + radius
    sigma_four = phase_cell - 4 + radius
    sigma_five = phase_cell - 5 + radius
    normal = radius
    x = -sigma / 2
    x_four = -sigma_four / 2
    x_five = -sigma_five / 2
    field_x = (
        -one / 2
        + normal
        - rho * x**3 / 3
        + rho * ((x_four + x_five) / 2 - x) / 5
        + rho**3 * ((x_four**3 + x_five**3) / 2 - x**3) / 4
    )
    sigma_speed = -2 * field_x
    normal_speed = sigma * (one - sigma_speed) / 2 + rho * nu
    beta, beta_derivative = _interval_taper(sigma)
    reference = _interval_reference_normal_speed(sigma)
    reference_derivative = _interval_reference_normal_speed_derivative(sigma)
    tilt = TILT_SCALE * beta * reference
    tilt_derivative = TILT_SCALE * (
        beta_derivative * reference + beta * reference_derivative
    )
    phase_sigma = one + tilt_derivative * normal
    phase_speed = phase_sigma * sigma_speed + tilt * normal_speed
    gradient_squared = phase_sigma**2 + tilt**2
    return phase_speed, gradient_squared


@lru_cache(maxsize=4)
def directed_slot_tube_certificate(
    precision: int = PRECISION_BITS,
) -> dict[str, Any]:
    """Validate the comparison clock on the rational raw-slot product tube."""

    if isinstance(precision, bool) or precision < 128:
        raise ValueError("precision must be an integer of at least 128 bits")
    worst_phase: DirectedInterval | None = None
    worst_gradient: DirectedInterval | None = None
    phase_index = -1
    gradient_index = -1
    for index in range(PARTITION_CELLS):
        phase_speed, gradient_squared = target_slot_tube_cell_bounds(
            index, precision
        )
        if worst_phase is None or phase_speed.lower < worst_phase.lower:
            worst_phase = phase_speed
            phase_index = index
        if (
            worst_gradient is None
            or gradient_squared.lower < worst_gradient.lower
        ):
            worst_gradient = gradient_squared
            gradient_index = index
    if worst_phase is None or worst_gradient is None:
        raise ValueError("empty raw-slot product-tube partition")
    clock_lower = _point_interval(
        TUBE_CLOCK_LOWER.numerator,
        TUBE_CLOCK_LOWER.denominator,
        precision,
    )
    gradient_lower = _point_interval(
        GRADIENT_SQUARED_LOWER.numerator,
        GRADIENT_SQUARED_LOWER.denominator,
        precision,
    )
    if worst_phase.lower <= clock_lower.upper:
        raise ValueError("raw-slot product clock margin did not close")
    if worst_gradient.lower <= gradient_lower.upper:
        raise ValueError("raw-slot comparison phase is not a submersion")
    return {
        "phase_index": phase_index,
        "phase_speed": _interval_record(worst_phase),
        "gradient_index": gradient_index,
        "gradient_squared": _interval_record(worst_gradient),
    }


def _plateau_margin() -> Fraction:
    radius = SLOT_TUBE_RADIUS
    margins = (
        Fraction(RIGHT_PLATEAU_END - CORE_PHASE_RIGHT) - radius,
        Fraction(CORE_PHASE_LEFT - LEFT_PLATEAU_START) - radius,
        Fraction(CORE_PHASE_LEFT - 5 - LEFT_PLATEAU_START) - radius,
        Fraction(CORE_PHASE_LEFT - 4 - LEFT_PLATEAU_START) - radius,
        Fraction(RIGHT_PLATEAU_END - (CORE_PHASE_RIGHT - 4)) - radius,
        Fraction(RIGHT_PLATEAU_END - (CORE_PHASE_RIGHT - 5)) - radius,
        Fraction(1) - radius,
    )
    margin = min(margins)
    if margin <= 0:
        raise ValueError("declared target slot tube leaves the unit plateau")
    return margin


def _left_corridor_certificate() -> dict[str, str | int | tuple[int, int]]:
    """Return the exact monotone polynomial bound for the left corridor."""

    x_lower = 9
    bracket = (
        SLOT_TUBE_RADIUS
        - Fraction(2 * x_lower**3, 15)
        + Fraction(3, 10)
        + Fraction(9 * x_lower**2 + 27 * x_lower + 27, 40)
    )
    derivative = (
        -Fraction(2 * x_lower**2, 5)
        + Fraction(9 * x_lower, 20)
        + Fraction(27, 40)
    )
    if bracket >= 0 or derivative >= 0:
        raise ValueError("left-corridor fast-field upper bound failed")
    return {
        "interval": (-30, -20),
        "x_lower": x_lower,
        "bracket": _fraction_text(bracket),
        "derivative": _fraction_text(derivative),
        "clock_lower": "1/1",
    }


def verify_parent_evidence(repository: Path) -> dict[str, bool]:
    """Replay the clocked-tail parent and its decisive claim boundary."""

    result_path = repository / PARENT_RESULT_RELATIVE_PATH
    if _sha256(result_path) != CLOCKED_TAIL_RESULT_SHA256:
        raise ValueError("clocked-tail parent result hash mismatch")
    payload = json.loads(result_path.read_text(encoding="utf-8"))
    validate_clocked_tail_graph_result(payload, repository)
    certificate = payload["audit"]["certificate"]
    checks = {
        "parent_proves_raw_target_sigma_clock_failure": (
            certificate["raw_singular_slot_target_clock_failure_proved"] is True
        ),
        "parent_proves_nonexplicit_small_rho_graph": (
            certificate["fixed_cutoff_small_rho_graph_exists"] is True
        ),
        "parent_leaves_target_graph_open": (
            certificate["target_positive_amplitude_graph_candidate_computed"]
            is False
        ),
        "parent_leaves_target_clock_open": (
            certificate["target_uniform_clock_bound_validated"] is False
        ),
    }
    if not all(checks.values()):
        raise ValueError("clocked-tail parent claim checks failed")
    return checks


@lru_cache(maxsize=1)
def build_reference_certificate() -> TargetRawSlotTiltedPhaseCertificate:
    """Build the exact/directed raw-slot comparison certificate."""

    exact = exact_sturm_certificate()
    anchor = target_anchor_raw_slot_equilibrium_certificate()
    directed = directed_slot_tube_certificate()
    left_corridor = _left_corridor_certificate()
    expressions = _exact_expressions()
    return TargetRawSlotTiltedPhaseCertificate(
        target_rho_squared=_fraction_text(TARGET_RHO_SQUARED),
        target_eta=TARGET_ETA,
        target_nu_box=(
            _fraction_text(TARGET_NU_LOWER),
            _fraction_text(TARGET_NU_UPPER),
        ),
        target_anchor_nu_decimal=TARGET_ANCHOR_NU_DECIMAL,
        target_anchor_nu_exact_rational=_fraction_text(TARGET_ANCHOR_NU),
        target_anchor_scope=(
            "frozen numerical operating anchor interpreted as the exact "
            "written decimal; not a validated selected root"
        ),
        no_go_comparison_nu_box=(
            _fraction_text(NO_GO_NU_LOWER),
            _fraction_text(NO_GO_NU_UPPER),
        ),
        core_phase_interval=(CORE_PHASE_LEFT, CORE_PHASE_RIGHT),
        taper_interval=(TAPER_LEFT, TAPER_RIGHT),
        tilt_scale=TILT_SCALE,
        slot_tube_radius=_fraction_text(SLOT_TUBE_RADIUS),
        partition_cells=PARTITION_CELLS,
        precision_bits=PRECISION_BITS,
        raw_sigma_speed_formula=sp.sstr(expressions["raw_sigma"]),
        raw_normal_speed_formula=sp.sstr(expressions["raw_normal"]),
        reference_normal_speed_formula=sp.sstr(
            expressions["reference_normal"]
        ),
        tapered_phase_formula=(
            "vartheta(sigma,d)=sigma+8*beta(sigma)*D_0(sigma)*d"
        ),
        raw_tapered_phase_speed_formula=(
            "S_*(s)+8*beta(s)*D_0(s)*D_nu(s)"
        ),
        sigma_speed_sturm_sequence_length=exact["sigma_sequence_length"],
        sigma_speed_real_root_count=exact["sigma_root_count"],
        sigma_speed_square_free=exact["sigma_square_free"],
        stall_phase_enclosures=exact["root_enclosures"],
        stall_nu_enclosures=exact["stall_enclosures"],
        target_anchor_slot_g_formula=anchor["slot_g_formula"],
        target_anchor_equilibrium_phase_formula=anchor[
            "equilibrium_phase_formula"
        ],
        target_anchor_equilibrium_normal_formula=anchor[
            "equilibrium_normal_formula"
        ],
        target_anchor_slot_fast_formula=anchor["slot_fast_formula"],
        target_anchor_slot_slow_formula=anchor["slot_slow_formula"],
        target_anchor_equilibrium_phase_enclosure=anchor["phase_enclosure"],
        target_anchor_equilibrium_normal_enclosure=anchor[
            "normal_enclosure"
        ],
        target_anchor_equilibrium_g_enclosure=anchor["g_enclosure"],
        raw_clock_lower=_fraction_text(RAW_CLOCK_LOWER),
        endpoint_sturm_records=exact["endpoint_records"],
        left_corridor_nominal_interval=left_corridor["interval"],
        left_corridor_x_lower=left_corridor["x_lower"],
        left_corridor_bracket_upper_at_x_lower=left_corridor["bracket"],
        left_corridor_derivative_upper_at_x_lower=left_corridor["derivative"],
        left_corridor_phase_speed_lower=left_corridor["clock_lower"],
        tube_clock_lower=_fraction_text(TUBE_CLOCK_LOWER),
        worst_tube_phase_speed_cell=directed["phase_index"],
        worst_tube_phase_speed=directed["phase_speed"],
        gradient_squared_lower=_fraction_text(GRADIENT_SQUARED_LOWER),
        worst_gradient_squared_cell=directed["gradient_index"],
        worst_gradient_squared=directed["gradient_squared"],
        minimum_plateau_margin=_fraction_text(_plateau_margin()),
        target_raw_coordinate_algebra_proved=True,
        raw_sigma_speed_has_three_simple_real_zeros_proved=True,
        raw_stall_locus_and_phase_no_go_proved=True,
        central_stall_lies_in_comparison_box_proved=True,
        constant_affine_phase_no_go_on_nu_box_proved=True,
        target_anchor_raw_slot_equilibrium_algebra_proved=True,
        target_anchor_raw_slot_equilibrium_enclosed_256_bit=True,
        target_anchor_raw_slot_zero_lies_in_product_tube_proved=True,
        target_anchor_product_tube_positive_clock_no_go_proved=True,
        tapered_phase_matches_incoming_sigma_clock_proved=True,
        tapered_raw_clock_uniform_on_nu_box_proved=True,
        incoming_to_core_sigma_clock_on_slot_tube_proved=True,
        declared_slot_tube_lies_in_unit_plateau_proved=True,
        raw_slot_product_tapered_clock_validated=True,
        raw_slot_product_tapered_phase_submersion_validated=True,
        parent_clock_failure_and_small_rho_graph_replayed=True,
        target_graph_candidate_computed=False,
        target_slot_tube_invariant_under_backward_flows_validated=False,
        target_graph_transform_self_map_validated=False,
        target_graph_fixed_point_validated=False,
        target_one_sided_traces_validated=False,
        target_w1p_fredholm_inverse_validated=False,
        target_complete_history_root_validated=False,
        target_general_network_lift_validated=False,
        target_biological_control_chain_validated=False,
    )


def json_ready_target_tilted_phase_audit() -> dict[str, Any]:
    """Return the certificate in JSON-ready form."""

    return {"certificate": asdict(build_reference_certificate())}


def validate_target_tilted_phase_audit(payload: dict[str, Any]) -> None:
    """Strictly validate the mathematical claim ledger."""

    if not isinstance(payload, dict) or set(payload) != {"certificate"}:
        raise ValueError("target tilted-phase audit has the wrong shape")
    certificate = payload["certificate"]
    if not isinstance(certificate, dict):
        raise ValueError("target tilted-phase certificate must be an object")
    canonical_certificate = json.loads(
        json.dumps(asdict(build_reference_certificate()), sort_keys=True)
    )
    replayed_certificate = json.loads(
        json.dumps(certificate, sort_keys=True)
    )
    if replayed_certificate != canonical_certificate:
        raise ValueError("target tilted-phase certificate differs from replay")
    for name in PROVED_FLAGS:
        if certificate[name] is not True:
            raise ValueError(f"proved flag {name} must be literal true")
    for name in OPEN_FLAGS:
        if certificate[name] is not False:
            raise ValueError(f"open flag {name} must be literal false")


def validate_target_tilted_phase_result(
    payload: dict[str, Any], repository: Path
) -> None:
    """Validate a generated result, hashes, parent evidence, and audit."""

    if not isinstance(payload, dict) or set(payload) != {"audit", "manifest"}:
        raise ValueError("target tilted-phase result has the wrong shape")
    validate_target_tilted_phase_audit(payload["audit"])
    manifest = payload["manifest"]
    if not isinstance(manifest, dict):
        raise ValueError("target tilted-phase manifest must be an object")
    required = {
        "generator",
        "generator_sha256",
        "proof_source",
        "proof_source_sha256",
        "note",
        "note_sha256",
        "parent_result",
        "parent_result_sha256",
        "parent_claim_checks",
        "default_command",
        "python",
        "platform",
        "arithmetic",
    }
    if set(manifest) != required:
        raise ValueError("target tilted-phase manifest keys differ")
    expected_paths = {
        "generator": GENERATOR_RELATIVE_PATH,
        "proof_source": PROOF_SOURCE_RELATIVE_PATH,
        "note": NOTE_RELATIVE_PATH,
        "parent_result": PARENT_RESULT_RELATIVE_PATH,
    }
    for key, relative in expected_paths.items():
        if manifest[key] != relative:
            raise ValueError(f"target tilted-phase manifest {key} differs")
    for key, relative in (
        ("generator_sha256", GENERATOR_RELATIVE_PATH),
        ("proof_source_sha256", PROOF_SOURCE_RELATIVE_PATH),
        ("note_sha256", NOTE_RELATIVE_PATH),
        ("parent_result_sha256", PARENT_RESULT_RELATIVE_PATH),
    ):
        if manifest[key] != _sha256(repository / relative):
            raise ValueError(f"target tilted-phase manifest {key} differs")
    if manifest["parent_result_sha256"] != CLOCKED_TAIL_RESULT_SHA256:
        raise ValueError("target tilted-phase pinned parent hash differs")
    checks = verify_parent_evidence(repository)
    if manifest["parent_claim_checks"] != checks:
        raise ValueError("target tilted-phase parent checks differ")
    if manifest["default_command"] != DEFAULT_COMMAND:
        raise ValueError("target tilted-phase default command differs")
    if manifest["arithmetic"] != MANIFEST_ARITHMETIC:
        raise ValueError("target tilted-phase arithmetic declaration differs")
    if not isinstance(manifest["python"], str) or not manifest["python"]:
        raise ValueError("target tilted-phase Python version is invalid")
    if not isinstance(manifest["platform"], str) or not manifest["platform"]:
        raise ValueError("target tilted-phase platform is invalid")
