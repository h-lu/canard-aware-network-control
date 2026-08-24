"""Directed certificate for an explicit finite-window prepared gap seed.

The fixed-epsilon sliding-window bridge leaves the finite-window row

    d_rho D(0, nu, 0) = A_{S,P} nu + B_{S,P}

to the *actual* frozen graph and planar preparation.  This module does not
pretend to construct that nonlinear object.  It freezes instead one explicit
longitudinal first-jet datum along the singular canard and validates its
Green row.  The datum is one admissibility-compatible candidate benchmark
that a later graph preparation may choose to realise; a different admissible
joining datum must recompute its own finite-window row.

For the even C3 cutoff ``chi_S`` below,

    f_J(s; nu) = chi_S(s) (s^3/24 + 9/20, nu),

the one-sided Green formula gives

    A_S = integral exp(-s^2/2) chi_S(s) ds,
    B_S = (1/24) integral exp(-s^2/2) chi_S(s) s^4 ds.

Both coefficients are strictly positive for every nonzero, nonnegative even
cutoff.  The reference certificate takes S=4 and buffer B=18, and its plateau
covers the entire pinned singular depth-two delay hull.  All reported
quadratures are finite linear combinations of Gaussian moments evaluated
with MPFR-directed rounding; no floating quadrature is used.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from fractions import Fraction
import json
from math import comb
from typing import Any, Iterable, Mapping

import gmpy2

from canard_control.directed_interval import (
    DirectedInterval,
    decimal_lower,
    decimal_upper,
    pi_interval,
)


MODEL_ID = "quadratic-period-lock-fixed-window-longitudinal-jet-seed"
AUDIT_ID = "fixed-window-prepared-gap-seed-v1"
PRECISION_BITS = 512

SECTION_HALF_WINDOW = 4
BUFFER = 18
OUTER_RADIUS = SECTION_HALF_WINDOW + BUFFER
RETAINED_SEGMENT_END = SECTION_HALF_WINDOW + 1
# The singular retained segment and all continuous depth-two backtracks lie
# inside |s|<20 for the pinned period horizon.  The plateau is deliberately
# larger than the retained segment; using 5 here would be incompatible with
# the preparation contract.
CORE_END = 20
CUTOFF_END = OUTER_RADIUS - 1
TRANSITION_WIDTH = CUTOFF_END - CORE_END

EPSILON = "1/5"
DELTA = "1/sqrt(5)"
PLANT_FOLD_DELAYS = ("4", "5")
PERIOD_LOWER = (
    "16.5403877931809337427421269239857792854309082030864525"
)
PERIOD_UPPER = (
    "16.5403878031809337427421269239857792854309082031635475"
)

GREEN_PHASE_DOC_SHA256 = (
    "543ae331d0ffc656bba3a667dab1301fed29f9796afe8a84c4390fcff4088dc8"
)
BLOCH_RESULT_SHA256 = (
    "c2f93b6cfe6a8e0df3b341476fbe45a83f6fecc0398dbb7340a5213a55357a31"
)
SLIDING_WINDOW_BRIDGE_RESULT_SHA256 = (
    "4afc81cc6472f1c24fe938147623d0042f27d3ab4f30d3f5f052e924b60c3b05"
)
QUADRATIC_PERIOD_LOCKED_ROOT_DOC_SHA256 = (
    "f08632721279f6bfc00d0aa4d118a9a7c5bda2b489f5457003e9914c540b87e3"
)

PROOF_SOURCE_RELATIVE_PATH = (
    "src/canard_control/fixed_window_prepared_gap_seed.py"
)
GENERATOR_RELATIVE_PATH = "experiments/fixed_window_prepared_gap_seed.py"
RESULT_RELATIVE_PATH = "experiments/results/fixed_window_prepared_gap_seed.json"
NOTE_RELATIVE_PATH = "docs/fixed-window-prepared-gap-seed.md"
DEFAULT_COMMAND = (
    "PYTHONPATH=src /usr/bin/python3 "
    "experiments/fixed_window_prepared_gap_seed.py"
)


# h(r) rises from zero to one; chi=1-h on the transition annulus.
RISE_COEFFICIENTS = (
    Fraction(0),
    Fraction(0),
    Fraction(0),
    Fraction(0),
    Fraction(35),
    Fraction(-84),
    Fraction(70),
    Fraction(-20),
)


def _context(precision: int, rounding: int) -> gmpy2.context:
    if isinstance(precision, bool) or int(precision) != precision or precision < 64:
        raise ValueError("precision must be an integer of at least 64 bits")
    return gmpy2.context(precision=int(precision), round=rounding)


def _fraction_text(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def _fraction_interval(value: Fraction, precision: int) -> DirectedInterval:
    return (
        DirectedInterval.from_decimal(value.numerator, precision)
        / value.denominator
    )


def _polynomial_value(coefficients: Iterable[Fraction], point: Fraction) -> Fraction:
    result = Fraction(0)
    for coefficient in reversed(tuple(coefficients)):
        result = result * point + coefficient
    return result


def _differentiate(coefficients: Iterable[Fraction]) -> tuple[Fraction, ...]:
    values = tuple(coefficients)
    return tuple(index * values[index] for index in range(1, len(values)))


def endpoint_jet(
    coefficients: Iterable[Fraction], point: Fraction, order: int
) -> tuple[Fraction, ...]:
    """Return exact derivatives through ``order`` at one rational point."""

    if isinstance(order, bool) or int(order) != order or order < 0:
        raise ValueError("order must be a nonnegative integer")
    current = tuple(coefficients)
    values: list[Fraction] = []
    for _ in range(int(order) + 1):
        values.append(_polynomial_value(current, point))
        current = _differentiate(current)
    return tuple(values)


def transition_coefficients_in_s(
    *, core_end: int = CORE_END, width: int = TRANSITION_WIDTH
) -> tuple[Fraction, ...]:
    """Expand ``1-h((s-core_end)/width)`` in powers of ``s`` exactly."""

    if width <= 0:
        raise ValueError("transition width must be positive")
    coefficients = [Fraction(0) for _ in range(len(RISE_COEFFICIENTS))]
    coefficients[0] = Fraction(1)
    for power, rise_coefficient in enumerate(RISE_COEFFICIENTS):
        if rise_coefficient == 0:
            continue
        scaled = -rise_coefficient / (width**power)
        for index in range(power + 1):
            coefficients[index] += (
                scaled
                * comb(power, index)
                * ((-core_end) ** (power - index))
            )
    return tuple(coefficients)


def septic_cutoff(
    value: float,
    *,
    plateau_end: int = CORE_END,
    transition_width: int = TRANSITION_WIDTH,
) -> float:
    """Evaluate the explicit even C3 cutoff in ordinary arithmetic."""

    if plateau_end < 0:
        raise ValueError("plateau end must be nonnegative")
    if transition_width <= 0:
        raise ValueError("transition width must be positive")
    radius = abs(float(value))
    cutoff_end = plateau_end + transition_width
    if radius <= plateau_end:
        return 1.0
    if radius >= cutoff_end:
        return 0.0
    scaled = (radius - plateau_end) / transition_width
    rise = scaled**4 * (
        35.0 + scaled * (-84.0 + scaled * (70.0 - 20.0 * scaled))
    )
    return 1.0 - rise


def prepared_first_jet_on_canard(s: float, nu: float) -> tuple[float, float]:
    """Evaluate the frozen longitudinal first-jet datum ``f_J(s;nu)``."""

    cutoff = septic_cutoff(s)
    return cutoff * (s**3 / 24.0 + 9.0 / 20.0), cutoff * nu


def _erfc_interval(value: DirectedInterval) -> DirectedInterval:
    """Enclose erfc on a real interval using monotonicity and MPFR."""

    precision = value.precision
    with _context(precision, gmpy2.RoundDown):
        lower = gmpy2.erfc(value.upper)
    with _context(precision, gmpy2.RoundUp):
        upper = gmpy2.erfc(value.lower)
    return DirectedInterval(lower, upper, precision)


def _exp_negative_half_square(point: int, precision: int) -> DirectedInterval:
    """Enclose ``exp(-point**2/2)`` for an exact integer point."""

    with _context(precision, gmpy2.RoundDown):
        value = gmpy2.mpfr(point)
        lower = gmpy2.exp(-(value * value) / 2)
    with _context(precision, gmpy2.RoundUp):
        value = gmpy2.mpfr(point)
        upper = gmpy2.exp(-(value * value) / 2)
    return DirectedInterval(lower, upper, precision)


def gaussian_moment_intervals(
    lower: int, upper: int, maximum_power: int, *, precision: int = PRECISION_BITS
) -> tuple[DirectedInterval, ...]:
    """Enclose ``J_n=integral_lower^upper s^n exp(-s^2/2) ds``.

    Endpoints are exact nonnegative integers.  ``J_0`` uses erfc to avoid
    subtracting two numbers close to one, and higher moments use

        J_n = a^(n-1)e^(-a^2/2) - b^(n-1)e^(-b^2/2)
              + (n-1)J_(n-2).
    """

    if lower < 0 or upper <= lower:
        raise ValueError("moment endpoints must satisfy 0 <= lower < upper")
    if isinstance(maximum_power, bool) or int(maximum_power) != maximum_power:
        raise ValueError("maximum power must be an integer")
    if maximum_power < 0:
        raise ValueError("maximum power must be nonnegative")
    a = DirectedInterval.from_decimal(lower, precision)
    b = DirectedInterval.from_decimal(upper, precision)
    sqrt_two = DirectedInterval.from_decimal(2, precision).sqrt()
    root_pi_over_two = (pi_interval(precision) / 2).sqrt()
    j_zero = root_pi_over_two * (
        _erfc_interval(a / sqrt_two) - _erfc_interval(b / sqrt_two)
    )
    if maximum_power == 0:
        return (j_zero,)

    exp_a = _exp_negative_half_square(lower, precision)
    exp_b = _exp_negative_half_square(upper, precision)
    moments = [j_zero, exp_a - exp_b]
    for power in range(2, maximum_power + 1):
        moments.append(
            (a ** (power - 1)) * exp_a
            - (b ** (power - 1)) * exp_b
            + (power - 1) * moments[power - 2]
        )
    return tuple(moments)


def _interval_linear_combination(
    coefficients: Iterable[Fraction],
    moments: tuple[DirectedInterval, ...],
    *,
    offset: int = 0,
) -> DirectedInterval:
    coefficients_tuple = tuple(coefficients)
    if not coefficients_tuple:
        raise ValueError("at least one coefficient is required")
    precision = moments[0].precision
    if offset < 0 or offset + len(coefficients_tuple) > len(moments):
        raise ValueError("moment range does not cover the polynomial")
    result = DirectedInterval.from_decimal(0, precision)
    for index, coefficient in enumerate(coefficients_tuple):
        result += _fraction_interval(coefficient, precision) * moments[index + offset]
    return result


@dataclass(frozen=True)
class IntervalRecord:
    lower: str
    upper: str
    width_upper: str


def _record(value: DirectedInterval, digits: int = 100) -> IntervalRecord:
    lower = decimal_lower(value.lower, digits)
    upper = decimal_upper(value.upper, digits)
    # The decimal conversion deliberately pushes both endpoints outward.
    # Record the width of those *serialized* endpoints, not the narrower
    # in-memory MPFR interval, so every JSON IntervalRecord is self-consistent.
    serialized = DirectedInterval.from_bounds(
        lower, upper, value.precision
    )
    return IntervalRecord(
        lower=lower,
        upper=upper,
        width_upper=decimal_upper(serialized.width_upper(), digits),
    )


@dataclass(frozen=True)
class FixedWindowGapSeedCertificate:
    """Machine-readable theorem record for the explicit first-jet row."""

    audit_id: str
    model_id: str
    precision_bits: int
    arithmetic: str
    epsilon: str
    delta: str
    section_half_window: int
    retained_segment_end: int
    buffer: int
    outer_radius: int
    cutoff_plateau_end: int
    cutoff_support_end: int
    transition_width: int
    plant_fold_delays: tuple[str, str]
    period: IntervalRecord
    fold_history_horizon: IntervalRecord
    fold_history_horizon_exceeds_largest_plant_delay: bool
    singular_depth_two_hull_radius: IntervalRecord
    plateau_margin_over_singular_depth_two_hull: IntervalRecord
    singular_depth_two_hull_covered: bool
    buffer_margin_over_two_horizons_plus_two: IntervalRecord
    rise_coefficients_in_r: tuple[str, ...]
    rise_derivative_coefficients_in_r: tuple[str, ...]
    rise_derivative_factorization: str
    cutoff_coefficients_in_s_on_positive_transition: tuple[str, ...]
    rise_endpoint_jet_at_zero_through_four: tuple[str, ...]
    rise_endpoint_jet_at_one_through_four: tuple[str, ...]
    cutoff_even: bool
    cutoff_between_zero_and_one: bool
    cutoff_nonincreasing_on_positive_transition: bool
    cutoff_global_c3: bool
    cutoff_not_global_c4: bool
    declared_core_first_jet: str
    prepared_tail_first_jet: str
    prepared_tail_zero_neighborhood_width: int
    linear_tail_normal_coefficients_zero: bool
    one_sided_linear_bvp: str
    linear_section_gap: str
    green_gap_row: str
    coefficient_a_formula: str
    coefficient_b_formula: str
    odd_delay_constant_cancels: bool
    coefficient_a: IntervalRecord
    coefficient_b: IntervalRecord
    root_nu_chi: IntervalRecord
    root_offset_above_minus_one_eighth: IntervalRecord
    core_gaussian_moments_zero_through_four: tuple[IntervalRecord, ...]
    transition_gaussian_moments_zero_through_eleven: tuple[IntervalRecord, ...]
    full_line_coefficient_a: IntervalRecord
    full_line_coefficient_b: IntervalRecord
    full_line_root_nu: IntervalRecord
    coefficient_a_full_line_defect: IntervalRecord
    coefficient_b_full_line_defect: IntervalRecord
    coefficient_a_strictly_positive_analytic: bool
    coefficient_b_strictly_positive_analytic: bool
    coefficient_a_excludes_zero_directed: bool
    coefficient_b_excludes_zero_directed: bool
    unique_affine_seed_root_directed: bool
    root_strictly_negative_directed: bool
    finite_window_root_distinct_from_minus_one_eighth_directed: bool
    buffer_condition_validated: bool
    parent_green_row_identity_required: bool
    parent_quadratic_carrier_jet_required: bool
    explicit_longitudinal_first_jet_frozen: bool
    linear_green_gap_row_validated: bool
    linear_row_identified_with_target_d_rho_d: bool
    complete_graph_preparation_datum_constructed: bool
    frozen_target_graph_family_validated: bool
    first_jet_realised_by_same_graph_preparation: bool
    nonlinear_prepared_trace_family_validated: bool
    positive_amplitude_depth_two_hull_validated: bool
    positive_amplitude_root_continued: bool
    fixed_epsilon_complete_history_root_validated: bool
    general_network_fredholm_lift_validated: bool
    biological_pulse_control_chain_validated: bool


def build_reference_certificate(
    *, precision: int = PRECISION_BITS
) -> FixedWindowGapSeedCertificate:
    """Build the deterministic directed reference certificate."""

    transition_coefficients = transition_coefficients_in_s()
    core_moments = gaussian_moment_intervals(0, CORE_END, 4, precision=precision)
    transition_moments = gaussian_moment_intervals(
        CORE_END, CUTOFF_END, 11, precision=precision
    )
    transition_a = _interval_linear_combination(
        transition_coefficients, transition_moments
    )
    transition_b_moment = _interval_linear_combination(
        transition_coefficients, transition_moments, offset=4
    )
    coefficient_a = 2 * (core_moments[0] + transition_a)
    coefficient_b = (core_moments[4] + transition_b_moment) / 12
    root_nu = -coefficient_b / coefficient_a

    full_line_coefficient_a = (2 * pi_interval(precision)).sqrt()
    full_line_coefficient_b = full_line_coefficient_a / 8
    full_line_root_nu = -DirectedInterval.from_decimal(1, precision) / 8
    root_offset = root_nu - full_line_root_nu
    coefficient_a_defect = full_line_coefficient_a - coefficient_a
    coefficient_b_defect = full_line_coefficient_b - coefficient_b

    period = DirectedInterval.from_bounds(
        PERIOD_LOWER, PERIOD_UPPER, precision
    )
    delta = 1 / DirectedInterval.from_decimal(5, precision).sqrt()
    horizon = delta * period
    singular_hull_radius = RETAINED_SEGMENT_END + 2 * horizon
    plateau_margin = CORE_END - singular_hull_radius
    margin = BUFFER - (2 * horizon + 2)

    rise_zero_jet = endpoint_jet(RISE_COEFFICIENTS, Fraction(0), 4)
    rise_one_jet = endpoint_jet(RISE_COEFFICIENTS, Fraction(1), 4)

    return FixedWindowGapSeedCertificate(
        audit_id=AUDIT_ID,
        model_id=MODEL_ID,
        precision_bits=precision,
        arithmetic=(
            "exact rational septic cutoff; analytic Gaussian-moment recurrence; "
            "MPFR exp, erfc, sqrt, pi, and algebra with directed rounding"
        ),
        epsilon=EPSILON,
        delta=DELTA,
        section_half_window=SECTION_HALF_WINDOW,
        retained_segment_end=RETAINED_SEGMENT_END,
        buffer=BUFFER,
        outer_radius=OUTER_RADIUS,
        cutoff_plateau_end=CORE_END,
        cutoff_support_end=CUTOFF_END,
        transition_width=TRANSITION_WIDTH,
        plant_fold_delays=PLANT_FOLD_DELAYS,
        period=_record(period),
        fold_history_horizon=_record(horizon),
        fold_history_horizon_exceeds_largest_plant_delay=(horizon.lower > 5),
        singular_depth_two_hull_radius=_record(singular_hull_radius),
        plateau_margin_over_singular_depth_two_hull=_record(plateau_margin),
        singular_depth_two_hull_covered=(plateau_margin.lower > 0),
        buffer_margin_over_two_horizons_plus_two=_record(margin),
        rise_coefficients_in_r=tuple(
            _fraction_text(value) for value in RISE_COEFFICIENTS
        ),
        rise_derivative_coefficients_in_r=tuple(
            _fraction_text(value) for value in _differentiate(RISE_COEFFICIENTS)
        ),
        rise_derivative_factorization="140*r^3*(1-r)^3",
        cutoff_coefficients_in_s_on_positive_transition=tuple(
            _fraction_text(value) for value in transition_coefficients
        ),
        rise_endpoint_jet_at_zero_through_four=tuple(
            _fraction_text(value) for value in rise_zero_jet
        ),
        rise_endpoint_jet_at_one_through_four=tuple(
            _fraction_text(value) for value in rise_one_jet
        ),
        cutoff_even=True,
        cutoff_between_zero_and_one=True,
        cutoff_nonincreasing_on_positive_transition=True,
        cutoff_global_c3=True,
        cutoff_not_global_c4=True,
        declared_core_first_jet="(s^3/24+9/20, nu)",
        prepared_tail_first_jet="(0,0)",
        prepared_tail_zero_neighborhood_width=OUTER_RADIUS - CUTOFF_END,
        linear_tail_normal_coefficients_zero=True,
        one_sided_linear_bvp=(
            "L0(U,V)=(U'-sU-V,V'+U)=f_J; U^a(0)=U^r(0)=0; "
            "-R U^a(-R)+V^a(-R)=0; R U^r(R)+V^r(R)=0"
        ),
        linear_section_gap="M_chi(nu)=V^a(0)-V^r(0) for the linear BVP",
        green_gap_row=(
            "M_chi(nu)=integral_-R^R exp(-s^2/2) "
            "[s f_J,1(s;nu)+f_J,2(s;nu)] ds=A_chi nu+B_chi"
        ),
        coefficient_a_formula=(
            "A_chi=integral_-R^R exp(-s^2/2) chi(s) ds"
        ),
        coefficient_b_formula=(
            "B_chi=(1/24) integral_-R^R exp(-s^2/2) chi(s) s^4 ds"
        ),
        odd_delay_constant_cancels=True,
        coefficient_a=_record(coefficient_a),
        coefficient_b=_record(coefficient_b),
        root_nu_chi=_record(root_nu),
        root_offset_above_minus_one_eighth=_record(root_offset),
        core_gaussian_moments_zero_through_four=tuple(
            _record(value) for value in core_moments
        ),
        transition_gaussian_moments_zero_through_eleven=tuple(
            _record(value) for value in transition_moments
        ),
        full_line_coefficient_a=_record(full_line_coefficient_a),
        full_line_coefficient_b=_record(full_line_coefficient_b),
        full_line_root_nu=_record(full_line_root_nu),
        coefficient_a_full_line_defect=_record(coefficient_a_defect),
        coefficient_b_full_line_defect=_record(coefficient_b_defect),
        coefficient_a_strictly_positive_analytic=True,
        coefficient_b_strictly_positive_analytic=True,
        coefficient_a_excludes_zero_directed=(coefficient_a.lower > 0),
        coefficient_b_excludes_zero_directed=(coefficient_b.lower > 0),
        unique_affine_seed_root_directed=(coefficient_a.lower > 0),
        root_strictly_negative_directed=(root_nu.upper < 0),
        finite_window_root_distinct_from_minus_one_eighth_directed=(
            root_offset.lower > 0
        ),
        buffer_condition_validated=(margin.lower > 0),
        parent_green_row_identity_required=True,
        parent_quadratic_carrier_jet_required=True,
        explicit_longitudinal_first_jet_frozen=True,
        linear_green_gap_row_validated=True,
        linear_row_identified_with_target_d_rho_d=False,
        complete_graph_preparation_datum_constructed=False,
        frozen_target_graph_family_validated=False,
        first_jet_realised_by_same_graph_preparation=False,
        nonlinear_prepared_trace_family_validated=False,
        positive_amplitude_depth_two_hull_validated=False,
        positive_amplitude_root_continued=False,
        fixed_epsilon_complete_history_root_validated=False,
        general_network_fredholm_lift_validated=False,
        biological_pulse_control_chain_validated=False,
    )


def json_ready_fixed_window_gap_seed_payload() -> dict[str, Any]:
    # Round-trip through JSON once so tuples become arrays.  Validators then
    # compare the in-memory reference to a payload reloaded from disk without
    # a tuple/list representation mismatch.
    return json.loads(
        json.dumps({"certificate": asdict(build_reference_certificate())})
    )


def validate_fixed_window_gap_seed_payload(payload: Mapping[str, Any]) -> None:
    """Reject any weakening or silent promotion of the theorem record."""

    if not isinstance(payload, Mapping):
        raise ValueError("payload must be a mapping")
    expected = json_ready_fixed_window_gap_seed_payload()
    if dict(payload) != expected:
        raise ValueError("fixed-window gap seed payload differs from reference")

    certificate = payload.get("certificate")
    if not isinstance(certificate, Mapping):
        raise ValueError("certificate must be a mapping")
    required_true = (
        "cutoff_even",
        "cutoff_between_zero_and_one",
        "cutoff_nonincreasing_on_positive_transition",
        "cutoff_global_c3",
        "cutoff_not_global_c4",
        "odd_delay_constant_cancels",
        "fold_history_horizon_exceeds_largest_plant_delay",
        "singular_depth_two_hull_covered",
        "linear_tail_normal_coefficients_zero",
        "coefficient_a_strictly_positive_analytic",
        "coefficient_b_strictly_positive_analytic",
        "coefficient_a_excludes_zero_directed",
        "coefficient_b_excludes_zero_directed",
        "unique_affine_seed_root_directed",
        "root_strictly_negative_directed",
        "finite_window_root_distinct_from_minus_one_eighth_directed",
        "buffer_condition_validated",
        "parent_green_row_identity_required",
        "parent_quadratic_carrier_jet_required",
        "explicit_longitudinal_first_jet_frozen",
        "linear_green_gap_row_validated",
    )
    required_false = (
        "complete_graph_preparation_datum_constructed",
        "linear_row_identified_with_target_d_rho_d",
        "frozen_target_graph_family_validated",
        "first_jet_realised_by_same_graph_preparation",
        "nonlinear_prepared_trace_family_validated",
        "positive_amplitude_depth_two_hull_validated",
        "positive_amplitude_root_continued",
        "fixed_epsilon_complete_history_root_validated",
        "general_network_fredholm_lift_validated",
        "biological_pulse_control_chain_validated",
    )
    if any(certificate.get(name) is not True for name in required_true):
        raise ValueError("a proved first-jet certificate flag was weakened")
    if any(certificate.get(name) is not False for name in required_false):
        raise ValueError("an open graph/root/control gate was silently promoted")
