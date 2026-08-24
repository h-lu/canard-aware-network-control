"""Certified controlled-to-autonomous excursions for the balanced FHN model.

The parent balanced-control theorem prepares an exact synchronous complete
history and keeps the nodewise recovery coordinate equal to zero with a
bounded additive cancellation input.  This module certifies two finite
handoffs in the *same* delayed FHN model:

* close every input at the positive ``v=1`` face and reach ``v=3/2``
  autonomously;
* latch the negative ``v=-1`` detector, retain recovery cancellation until
  ``v=-28/25``, close every input, and reach ``v=-6/5`` autonomously.

Both proofs finish before the first delayed layer can see anything except the
prepared value ``r=+/-1/2``.  The RFDE therefore reduces, by the method of
steps and exact synchrony, to a planar polynomial ODE.  Exact rational
piecewise-linear phase barriers certify a strictly signed voltage velocity
all the way to the terminal face.

There is also a structural obstruction: closing the recovery cancellation at
the negative ``v=-1`` face produces a turning point before ``v=-1.17``.
Thus a monotone no-return claim from the old negative detector is false even
on the exact synchronous leaf.  The obstruction does not rule out a later
second excursion after the first reversal.

This is a finite-horizon autonomous-excursion result.  It is not an
autonomous-onset, action-potential, basin, periodic-attraction, or hardware
theorem.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, localcontext
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

import gmpy2
import sympy as sp

from canard_control.directed_interval import decimal_lower, decimal_upper
from canard_control.fhn_balanced_control_chain import (
    validate_balanced_control_chain_result_payload,
)


TRACKED_BALANCED_CONTROL_CHAIN_SHA256 = (
    "090e690808d9106152958c1338980fde686875a4113241c8c842683a43d1ebf9"
)
MODEL_ID = "balanced-fhn-controlled-to-autonomous-synchronous-handoff"
ASSUMPTIONS_ID = (
    "finite-N-balanced-two-half-delay-layer-FHN;"
    "exact-synchronous-Phi_{+/-1/2};"
    "bounded-nodewise-recovery-cancellation-through-handoff;"
    "all-additive-inputs-zero-after-handoff"
)

_SCALE = 10**12
_EPSILON = Fraction(1, 5)
_UNFOLDING = Fraction(3, 5)
_KAPPA_1_LOWER = Fraction(199999999998, _SCALE)
_KAPPA_1_UPPER = Fraction(200000000002, _SCALE)
_KAPPA_3_LOWER = Fraction(249999999998, _SCALE)
_KAPPA_3_UPPER = Fraction(250000000002, _SCALE)

# The slopes have denominator 10^12.  They were rounded in the safe
# direction and are subsequently checked by exact rational inequalities;
# their decimal construction is not part of the proof.
_POSITIVE_BARRIER_SLOPE_NUMERATORS = (
    133765264369,
    143096279980,
    153007851037,
    163613576808,
    175049708952,
    187482152516,
    201116128993,
    216209805744,
    233093987370,
    252201348919,
    274111212843,
    299620690183,
    329862744878,
    366512800287,
    412175011717,
    471168680106,
    551323990425,
    668818224397,
    865161665440,
    1311119796186,
)

_NEGATIVE_BARRIER_SLOPE_NUMERATORS = (
    1117341012456,
    1161024528280,
    1209300717310,
    1263013957967,
    1323243280246,
    1391393792703,
    1469336004930,
    1559625993827,
    1665868781208,
    1793350726927,
    1950215477979,
    2149845887145,
    2416278845765,
    2798745320891,
    3422800528161,
    4810094625935,
)

_NEGATIVE_UNIT_OBSTRUCTION_SLOPE_NUMERATORS = (
    770310931796,
    802625883770,
    838586941824,
    878893160845,
    924443735159,
    976417609782,
    1036395318067,
    1106552205128,
    1189978079519,
    1291233625148,
    1417381507713,
    1580054280693,
    1800052530328,
    2119121252685,
    2637076257738,
    3677178078377,
    7378910502942,
)


@dataclass(frozen=True)
class HandoffAlgebraAudit:
    """Exact symbolic residuals for the frozen-delay planar reductions."""

    positive_voltage_residual: sp.Expr
    positive_recovery_residual: sp.Expr
    negative_voltage_residual: sp.Expr
    negative_recovery_residual: sp.Expr
    positive_vector_derivative_residual: sp.Expr
    negative_vector_derivative_residual: sp.Expr
    positive_vector_derivative_at_one: sp.Expr
    negative_vector_derivative_at_one: sp.Expr


@dataclass(frozen=True)
class BarrierSegmentAudit:
    """One exact rational phase-barrier segment."""

    left: Fraction
    right: Fraction
    slope: Fraction
    barrier_left: Fraction
    barrier_right: Fraction
    vector_lower_at_right: Fraction
    inward_margin: Fraction
    crossing_time_upper: Fraction


@dataclass(frozen=True)
class UpperBarrierAudit:
    """Exact rational hypograph barrier for one autonomous excursion."""

    branch: str
    start: Fraction
    target: Fraction
    step: Fraction
    segments: tuple[BarrierSegmentAudit, ...]
    terminal_barrier_upper: Fraction
    minimum_vector_lower: Fraction
    minimum_inward_margin: Fraction
    crossing_time_upper: Fraction


@dataclass(frozen=True)
class ObstructionSegmentAudit:
    """One exact rational epigraph segment for the negative unit handoff."""

    left: Fraction
    right: Fraction
    slope: Fraction
    barrier_left: Fraction
    barrier_right: Fraction
    upper_vector_at_left: Fraction
    inward_margin: Fraction


@dataclass(frozen=True)
class NegativeUnitHandoffObstructionAudit:
    """Exact phase barrier forcing a turn before magnitude 1.17."""

    segments: tuple[ObstructionSegmentAudit, ...]
    initial_vector_lower: Fraction
    endpoint: Fraction
    terminal_barrier_lower: Fraction
    terminal_vector_upper: Fraction
    terminal_crossing_margin: Fraction
    minimum_inward_margin: Fraction
    turn_time_upper: Fraction


@dataclass(frozen=True)
class AutonomousHandoffCertificate:
    """Public constants and strict scope for the autonomous handoff theorem."""

    balanced_control_chain_result_sha256: str
    precision_bits: int
    model_id: str
    assumptions_id: str
    epsilon: str
    unfolding: str
    enclosing_kappa_1_interval: tuple[str, str]
    enclosing_kappa_3_interval: tuple[str, str]
    prepared_positive_history: str
    prepared_negative_history: str
    positive_controlled_detector_and_handoff_face: str
    negative_controlled_detector_face: str
    negative_controlled_handoff_face: str
    positive_autonomous_excursion_face: str
    negative_autonomous_excursion_face: str
    positive_controlled_handoff_growth_lower: str
    negative_controlled_handoff_growth_lower: str
    positive_controlled_handoff_deadline_upper: str
    negative_controlled_handoff_deadline_upper: str
    positive_autonomous_barrier_segments: int
    negative_autonomous_barrier_segments: int
    positive_autonomous_velocity_lower: str
    negative_autonomous_magnitude_velocity_lower: str
    positive_autonomous_recovery_at_landing_upper: str
    negative_autonomous_recovery_magnitude_at_landing_upper: str
    positive_autonomous_excursion_time_upper: str
    negative_autonomous_excursion_time_upper: str
    positive_decision_release_to_excursion_time_upper: str
    negative_decision_release_to_excursion_time_upper: str
    positive_control_start_to_excursion_time_upper: str
    negative_control_start_to_excursion_time_upper: str
    minimum_delay_lower: str
    positive_frozen_delay_slack_lower: str
    negative_frozen_delay_slack_lower: str
    negative_unit_handoff_turn_magnitude_upper: str
    negative_unit_initial_magnitude_velocity_lower: str
    negative_unit_controlled_detector_deadline_upper: str
    negative_unit_handoff_turn_time_upper: str
    negative_unit_decision_release_to_turn_time_upper: str
    negative_unit_handoff_frozen_delay_slack_lower: str
    exact_symbolic_handoff_reduction_validated: bool
    tracked_gain_box_contained_in_enclosing_box_validated: bool
    exact_positive_phase_barrier_validated: bool
    exact_negative_phase_barrier_validated: bool
    piecewise_barrier_corner_forward_invariance_validated: bool
    method_of_steps_frozen_delay_window_validated: bool
    arbitrary_finite_balanced_topology_on_exact_synchronous_leaf_validated: bool
    all_additive_inputs_zero_after_handoff_validated: bool
    positive_finite_autonomous_excursion_validated: bool
    negative_finite_autonomous_excursion_validated: bool
    positive_finite_horizon_no_reversal_validated: bool
    negative_finite_horizon_no_reversal_validated: bool
    two_synchronous_terminal_faces_validated: bool
    negative_unit_handoff_turn_before_minus_1_17_validated: bool
    negative_unit_handoff_monotone_no_return_validated: bool
    asynchronous_autonomous_excursion_validated: bool
    autonomous_onset_validated: bool
    permanent_no_return_validated: bool
    biological_action_potential_validated: bool
    quiet_or_pulse_basin_validated: bool
    landing_on_periodic_branch_validated: bool
    full_network_periodic_attraction_validated: bool
    general_topology_canard_root_equivalence_validated: bool
    model_uncertainty_validated: bool
    measurement_noise_validated: bool
    hardware_validated: bool


def _mapping(value: object, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{name} must be a mapping")
    return value


def _fhn(value: sp.Expr) -> sp.Expr:
    return value - value**3 / 3


def _gain(value: sp.Expr, kappa_1: sp.Expr, kappa_3: sp.Expr) -> sp.Expr:
    return kappa_1 * value + kappa_3 * (value - 1) ** 3


def handoff_algebra_audit() -> HandoffAlgebraAudit:
    """Return exact residuals for the positive and negative planar systems."""

    v, w, z, p = sp.symbols("v w z p", real=True)
    kappa_1, kappa_3 = sp.symbols(
        "kappa_1 kappa_3", positive=True, real=True
    )
    epsilon = sp.Rational(1, 5)
    unfolding = sp.Rational(3, 5)

    positive_rhs = (
        _fhn(v)
        - w
        + epsilon
        * (_gain(sp.Rational(1, 2), kappa_1, kappa_3) - _gain(v, kappa_1, kappa_3))
    )
    positive_vector = (
        _fhn(v)
        - epsilon
        * (
            kappa_1 * (v - sp.Rational(1, 2))
            + kappa_3 * ((v - 1) ** 3 + sp.Rational(1, 8))
        )
    )

    negative_original = (
        _fhn(-z)
        + p
        + epsilon
        * (_gain(-sp.Rational(1, 2), kappa_1, kappa_3) - _gain(-z, kappa_1, kappa_3))
    )
    negative_vector = (
        _fhn(z)
        - epsilon
        * (
            kappa_1 * (z - sp.Rational(1, 2))
            + kappa_3 * ((z + 1) ** 3 - sp.Rational(27, 8))
        )
    )
    return HandoffAlgebraAudit(
        positive_voltage_residual=sp.simplify(
            positive_rhs - (positive_vector - w)
        ),
        positive_recovery_residual=sp.simplify(
            epsilon * (v - unfolding) - sp.Rational(1, 5) * (v - sp.Rational(3, 5))
        ),
        negative_voltage_residual=sp.simplify(
            -negative_original - (negative_vector - p)
        ),
        negative_recovery_residual=sp.simplify(
            -epsilon * (-z - unfolding) - epsilon * (z + unfolding)
        ),
        positive_vector_derivative_residual=sp.simplify(
            sp.diff(positive_vector, v)
            - (
                1
                - v**2
                - epsilon * (kappa_1 + 3 * kappa_3 * (v - 1) ** 2)
            )
        ),
        negative_vector_derivative_residual=sp.simplify(
            sp.diff(negative_vector, z)
            - (
                1
                - z**2
                - epsilon * (kappa_1 + 3 * kappa_3 * (z + 1) ** 2)
            )
        ),
        positive_vector_derivative_at_one=sp.simplify(
            sp.diff(positive_vector, v).subs(v, 1)
        ),
        negative_vector_derivative_at_one=sp.simplify(
            sp.diff(negative_vector, z).subs(z, 1)
        ),
    )


def _positive_vector_lower(value: Fraction) -> Fraction:
    """Lower bound for the positive frozen-delay voltage vector ``q_+``."""

    return (
        value
        - value**3 / 3
        - _EPSILON
        * (
            _KAPPA_1_UPPER * (value - Fraction(1, 2))
            + _KAPPA_3_UPPER * ((value - 1) ** 3 + Fraction(1, 8))
        )
    )


def _negative_vector_lower(value: Fraction) -> Fraction:
    """Lower bound for ``z'`` on the negative frozen-delay branch."""

    return (
        value
        - value**3 / 3
        - _EPSILON
        * (
            _KAPPA_1_UPPER * (value - Fraction(1, 2))
            + _KAPPA_3_UPPER
            * ((value + 1) ** 3 - Fraction(27, 8))
        )
    )


def _negative_vector_upper(value: Fraction) -> Fraction:
    """Upper bound for ``z'`` on the negative frozen-delay branch."""

    return (
        value
        - value**3 / 3
        - _EPSILON
        * (
            _KAPPA_1_LOWER * (value - Fraction(1, 2))
            + _KAPPA_3_LOWER
            * ((value + 1) ** 3 - Fraction(27, 8))
        )
    )


def _upper_barrier_audit(
    *,
    branch: str,
    start: Fraction,
    step: Fraction,
    slope_numerators: Sequence[int],
) -> UpperBarrierAudit:
    if branch == "positive":
        vector_lower = _positive_vector_lower
        recovery_rate = lambda value: _EPSILON * (value - _UNFOLDING)
    elif branch == "negative":
        vector_lower = _negative_vector_lower
        recovery_rate = lambda value: _EPSILON * (value + _UNFOLDING)
    else:
        raise ValueError("branch must be 'positive' or 'negative'")

    barrier = Fraction(0)
    segments: list[BarrierSegmentAudit] = []
    for index, numerator in enumerate(slope_numerators):
        left = start + index * step
        right = left + step
        slope = Fraction(int(numerator), _SCALE)
        barrier_right = barrier + slope * step
        vector_at_right = vector_lower(right) - barrier_right
        inward_margin = slope * vector_at_right - recovery_rate(right)
        if slope <= 0 or vector_at_right <= 0 or inward_margin <= 0:
            raise RuntimeError(
                f"{branch} phase barrier fails on segment {index + 1}"
            )
        segments.append(
            BarrierSegmentAudit(
                left=left,
                right=right,
                slope=slope,
                barrier_left=barrier,
                barrier_right=barrier_right,
                vector_lower_at_right=vector_at_right,
                inward_margin=inward_margin,
                crossing_time_upper=step / vector_at_right,
            )
        )
        barrier = barrier_right

    return UpperBarrierAudit(
        branch=branch,
        start=start,
        target=start + len(segments) * step,
        step=step,
        segments=tuple(segments),
        terminal_barrier_upper=barrier,
        minimum_vector_lower=min(
            segment.vector_lower_at_right for segment in segments
        ),
        minimum_inward_margin=min(
            segment.inward_margin for segment in segments
        ),
        crossing_time_upper=sum(
            (segment.crossing_time_upper for segment in segments),
            Fraction(0),
        ),
    )


def positive_autonomous_barrier_audit() -> UpperBarrierAudit:
    """Certify the autonomous ``1 -> 3/2`` phase corridor exactly."""

    return _upper_barrier_audit(
        branch="positive",
        start=Fraction(1),
        step=Fraction(1, 40),
        slope_numerators=_POSITIVE_BARRIER_SLOPE_NUMERATORS,
    )


def negative_autonomous_barrier_audit() -> UpperBarrierAudit:
    """Certify the autonomous ``28/25 -> 6/5`` phase corridor exactly."""

    return _upper_barrier_audit(
        branch="negative",
        start=Fraction(28, 25),
        step=Fraction(1, 200),
        slope_numerators=_NEGATIVE_BARRIER_SLOPE_NUMERATORS,
    )


def negative_unit_handoff_obstruction_audit(
) -> NegativeUnitHandoffObstructionAudit:
    """Certify a first reversal before magnitude 1.17 after handoff at -1."""

    step = Fraction(1, 100)
    barrier = Fraction(0)
    segments: list[ObstructionSegmentAudit] = []
    for index, numerator in enumerate(
        _NEGATIVE_UNIT_OBSTRUCTION_SLOPE_NUMERATORS
    ):
        left = Fraction(1) + index * step
        right = left + step
        slope = Fraction(int(numerator), _SCALE)
        vector_at_left = _negative_vector_upper(left) - barrier
        inward_margin = (
            _EPSILON * (left + _UNFOLDING) - slope * vector_at_left
        )
        if slope <= 0 or vector_at_left <= 0 or inward_margin <= 0:
            raise RuntimeError(
                f"negative unit obstruction fails on segment {index + 1}"
            )
        barrier_right = barrier + slope * step
        segments.append(
            ObstructionSegmentAudit(
                left=left,
                right=right,
                slope=slope,
                barrier_left=barrier,
                barrier_right=barrier_right,
                upper_vector_at_left=vector_at_left,
                inward_margin=inward_margin,
            )
        )
        barrier = barrier_right

    endpoint = Fraction(117, 100)
    initial_vector_lower = _negative_vector_lower(Fraction(1))
    vector_endpoint = _negative_vector_upper(endpoint)
    crossing_margin = barrier - vector_endpoint
    if (
        segments[-1].right != endpoint
        or initial_vector_lower <= 0
        or crossing_margin <= 0
    ):
        raise RuntimeError("negative unit obstruction does not force a turn")
    turn_time = _negative_vector_upper(Fraction(1)) / (
        _EPSILON * (Fraction(1) + _UNFOLDING)
    )
    return NegativeUnitHandoffObstructionAudit(
        segments=tuple(segments),
        initial_vector_lower=initial_vector_lower,
        endpoint=endpoint,
        terminal_barrier_lower=barrier,
        terminal_vector_upper=vector_endpoint,
        terminal_crossing_margin=crossing_margin,
        minimum_inward_margin=min(
            segment.inward_margin for segment in segments
        ),
        turn_time_upper=turn_time,
    )


def _fraction_lower(value: Fraction, precision: int) -> gmpy2.mpfr:
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        return gmpy2.mpfr(value.numerator) / gmpy2.mpfr(value.denominator)


def _fraction_upper(value: Fraction, precision: int) -> gmpy2.mpfr:
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        return gmpy2.mpfr(value.numerator) / gmpy2.mpfr(value.denominator)


def _deadline_upper(
    face_ratio: Fraction, growth_lower: Fraction, precision: int
) -> gmpy2.mpfr:
    ratio = _fraction_upper(face_ratio, precision)
    growth = _fraction_lower(growth_lower, precision)
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        return gmpy2.log(ratio) / growth


def _sum_upper(values: Sequence[gmpy2.mpfr], precision: int) -> gmpy2.mpfr:
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        total = gmpy2.mpfr(0)
        for value in values:
            total += value
        return total


def _minimum_delay_lower(precision: int) -> gmpy2.mpfr:
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        return 4 * gmpy2.sqrt(gmpy2.mpfr(5))


def _difference_lower(
    minuend: gmpy2.mpfr, subtrahend: gmpy2.mpfr, precision: int
) -> gmpy2.mpfr:
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        return minuend - subtrahend


def _public_recomposable_slack_lower(
    value: gmpy2.mpfr, precision: int
) -> str:
    """Return a lower slack endpoint with a decimal recomposition guard."""

    # The individually printed delay and time endpoints are outward rounded.
    # Shaving 1e-40 (many orders below every claimed margin) ensures that
    # subtracting those *printed* endpoints still dominates this public
    # slack.  The MPFR-directed value remains the authoritative precursor.
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        guarded = value - gmpy2.mpfr("1e-40")
    return decimal_lower(guarded, 55)


def _tracked_box_is_contained(parent: Mapping[str, Any]) -> bool:
    bounds_1 = parent.get("kappa_1_interval")
    bounds_3 = parent.get("kappa_3_interval")
    if not (
        isinstance(bounds_1, list)
        and len(bounds_1) == 2
        and isinstance(bounds_3, list)
        and len(bounds_3) == 2
    ):
        return False
    try:
        low_1, high_1 = map(Decimal, bounds_1)
        low_3, high_3 = map(Decimal, bounds_3)
    except Exception:
        return False
    return (
        Decimal("0.199999999998") <= low_1
        <= high_1 <= Decimal("0.200000000002")
        and Decimal("0.249999999998") <= low_3
        <= high_3 <= Decimal("0.250000000002")
    )


def autonomous_handoff_from_payload(
    payload: Mapping[str, Any],
    *,
    balanced_control_chain_result_sha256: str,
    precision: int = 160,
) -> AutonomousHandoffCertificate:
    """Validate the parent theorem and derive the autonomous handoff record."""

    if balanced_control_chain_result_sha256 != (
        TRACKED_BALANCED_CONTROL_CHAIN_SHA256
    ):
        raise ValueError("balanced control-chain result is not the tracked source")
    if (
        isinstance(precision, bool)
        or int(precision) != precision
        or int(precision) < 64
    ):
        raise ValueError("precision must be an integer of at least 64 bits")
    precision = int(precision)

    root = _mapping(payload, "balanced control-chain payload")
    validate_balanced_control_chain_result_payload(root)
    parent = _mapping(root.get("certificate"), "parent certificate")
    if not _tracked_box_is_contained(parent):
        raise ValueError("tracked gain box is not inside the handoff audit box")
    if parent.get("complete_history_preparation_time_upper") is None:
        raise ValueError("parent preparation deadline is missing")

    algebra = handoff_algebra_audit()
    if not (
        algebra.positive_voltage_residual == 0
        and algebra.positive_recovery_residual == 0
        and algebra.negative_voltage_residual == 0
        and algebra.negative_recovery_residual == 0
        and algebra.positive_vector_derivative_residual == 0
        and algebra.negative_vector_derivative_residual == 0
        and algebra.positive_vector_derivative_at_one.is_negative is True
        and algebra.negative_vector_derivative_at_one.is_negative is True
    ):
        raise RuntimeError("symbolic autonomous handoff reduction failed")

    positive = positive_autonomous_barrier_audit()
    negative = negative_autonomous_barrier_audit()
    obstruction = negative_unit_handoff_obstruction_audit()
    if positive.target != Fraction(3, 2):
        raise RuntimeError("positive barrier has the wrong terminal face")
    if negative.target != Fraction(6, 5):
        raise RuntimeError("negative barrier has the wrong terminal face")

    positive_growth = (
        Fraction(2, 3)
        - _EPSILON * (_KAPPA_1_UPPER + 3 * _KAPPA_3_UPPER)
    )
    negative_handoff = Fraction(28, 25)
    negative_secant = (
        negative_handoff**2 + 3 * negative_handoff + 3
    )
    negative_growth = (
        1
        - negative_handoff**2 / 3
        - _EPSILON
        * (_KAPPA_1_UPPER + _KAPPA_3_UPPER * negative_secant)
    )
    negative_unit_growth = (
        Fraction(2, 3)
        - _EPSILON * (_KAPPA_1_UPPER + 7 * _KAPPA_3_UPPER)
    )
    if min(positive_growth, negative_growth, negative_unit_growth) <= 0:
        raise RuntimeError("controlled handoff growth is not positive")

    positive_controlled = _deadline_upper(
        Fraction(2), positive_growth, precision
    )
    negative_controlled = _deadline_upper(
        Fraction(56, 25), negative_growth, precision
    )
    negative_unit_controlled = _deadline_upper(
        Fraction(2), negative_unit_growth, precision
    )
    positive_autonomous = _fraction_upper(
        positive.crossing_time_upper, precision
    )
    negative_autonomous = _fraction_upper(
        negative.crossing_time_upper, precision
    )
    positive_total = _sum_upper(
        (positive_controlled, positive_autonomous), precision
    )
    negative_total = _sum_upper(
        (negative_controlled, negative_autonomous), precision
    )
    obstruction_turn = _fraction_upper(obstruction.turn_time_upper, precision)
    obstruction_total = _sum_upper(
        (negative_unit_controlled, obstruction_turn), precision
    )
    minimum_delay = _minimum_delay_lower(precision)
    positive_slack = _difference_lower(minimum_delay, positive_total, precision)
    negative_slack = _difference_lower(minimum_delay, negative_total, precision)
    obstruction_slack = _difference_lower(
        minimum_delay, obstruction_total, precision
    )
    if min(positive_slack, negative_slack, obstruction_slack) <= 0:
        raise RuntimeError("a handoff leaves the frozen-delay method-of-steps window")

    positive_controlled_public = decimal_upper(positive_controlled, 55)
    negative_controlled_public = decimal_upper(negative_controlled, 55)
    positive_autonomous_public = decimal_upper(positive_autonomous, 55)
    negative_autonomous_public = decimal_upper(negative_autonomous, 55)
    negative_unit_controlled_public = decimal_upper(
        negative_unit_controlled, 55
    )
    obstruction_turn_public = decimal_upper(obstruction_turn, 55)

    try:
        preparation_text = str(parent["complete_history_preparation_time_upper"])
        with localcontext() as context:
            context.prec = 100
            preparation = Decimal(preparation_text)
            # Sum the individually published upper endpoints so the public
            # composition is itself outward-safe without hidden guard digits.
            positive_total_public = format(
                Decimal(positive_controlled_public)
                + Decimal(positive_autonomous_public),
                "f",
            )
            negative_total_public = format(
                Decimal(negative_controlled_public)
                + Decimal(negative_autonomous_public),
                "f",
            )
            obstruction_total_public = format(
                Decimal(negative_unit_controlled_public)
                + Decimal(obstruction_turn_public),
                "f",
            )
            # Recompose from the *published* coarser upper endpoints.  This
            # preserves the safe direction for downstream Decimal audits.
            positive_from_start = preparation + Decimal(positive_total_public)
            negative_from_start = preparation + Decimal(negative_total_public)
    except Exception as error:
        raise ValueError("parent preparation deadline is not decimal") from error

    return AutonomousHandoffCertificate(
        balanced_control_chain_result_sha256=(
            balanced_control_chain_result_sha256
        ),
        precision_bits=precision,
        model_id=MODEL_ID,
        assumptions_id=ASSUMPTIONS_ID,
        epsilon="1/5",
        unfolding="3/5",
        enclosing_kappa_1_interval=("0.199999999998", "0.200000000002"),
        enclosing_kappa_3_interval=("0.249999999998", "0.250000000002"),
        prepared_positive_history="Phi_{1/2}",
        prepared_negative_history="Phi_{-1/2}",
        positive_controlled_detector_and_handoff_face="1",
        negative_controlled_detector_face="-1",
        negative_controlled_handoff_face="-1.12",
        positive_autonomous_excursion_face="1.5",
        negative_autonomous_excursion_face="-1.2",
        positive_controlled_handoff_growth_lower=decimal_lower(
            _fraction_lower(positive_growth, precision), 55
        ),
        negative_controlled_handoff_growth_lower=decimal_lower(
            _fraction_lower(negative_growth, precision), 55
        ),
        positive_controlled_handoff_deadline_upper=positive_controlled_public,
        negative_controlled_handoff_deadline_upper=negative_controlled_public,
        positive_autonomous_barrier_segments=len(positive.segments),
        negative_autonomous_barrier_segments=len(negative.segments),
        positive_autonomous_velocity_lower=decimal_lower(
            _fraction_lower(positive.minimum_vector_lower, precision), 55
        ),
        negative_autonomous_magnitude_velocity_lower=decimal_lower(
            _fraction_lower(negative.minimum_vector_lower, precision), 55
        ),
        positive_autonomous_recovery_at_landing_upper=decimal_upper(
            _fraction_upper(positive.terminal_barrier_upper, precision), 55
        ),
        negative_autonomous_recovery_magnitude_at_landing_upper=decimal_upper(
            _fraction_upper(negative.terminal_barrier_upper, precision), 55
        ),
        positive_autonomous_excursion_time_upper=positive_autonomous_public,
        negative_autonomous_excursion_time_upper=negative_autonomous_public,
        positive_decision_release_to_excursion_time_upper=positive_total_public,
        negative_decision_release_to_excursion_time_upper=negative_total_public,
        positive_control_start_to_excursion_time_upper=format(
            positive_from_start, "f"
        ),
        negative_control_start_to_excursion_time_upper=format(
            negative_from_start, "f"
        ),
        minimum_delay_lower=decimal_lower(minimum_delay, 55),
        positive_frozen_delay_slack_lower=_public_recomposable_slack_lower(
            positive_slack, precision
        ),
        negative_frozen_delay_slack_lower=_public_recomposable_slack_lower(
            negative_slack, precision
        ),
        negative_unit_handoff_turn_magnitude_upper="1.17",
        negative_unit_initial_magnitude_velocity_lower=decimal_lower(
            _fraction_lower(obstruction.initial_vector_lower, precision), 55
        ),
        negative_unit_controlled_detector_deadline_upper=(
            negative_unit_controlled_public
        ),
        negative_unit_handoff_turn_time_upper=obstruction_turn_public,
        negative_unit_decision_release_to_turn_time_upper=(
            obstruction_total_public
        ),
        negative_unit_handoff_frozen_delay_slack_lower=(
            _public_recomposable_slack_lower(obstruction_slack, precision)
        ),
        exact_symbolic_handoff_reduction_validated=True,
        tracked_gain_box_contained_in_enclosing_box_validated=True,
        exact_positive_phase_barrier_validated=True,
        exact_negative_phase_barrier_validated=True,
        piecewise_barrier_corner_forward_invariance_validated=True,
        method_of_steps_frozen_delay_window_validated=True,
        arbitrary_finite_balanced_topology_on_exact_synchronous_leaf_validated=True,
        all_additive_inputs_zero_after_handoff_validated=True,
        positive_finite_autonomous_excursion_validated=True,
        negative_finite_autonomous_excursion_validated=True,
        positive_finite_horizon_no_reversal_validated=True,
        negative_finite_horizon_no_reversal_validated=True,
        two_synchronous_terminal_faces_validated=True,
        negative_unit_handoff_turn_before_minus_1_17_validated=True,
        negative_unit_handoff_monotone_no_return_validated=False,
        asynchronous_autonomous_excursion_validated=False,
        autonomous_onset_validated=False,
        permanent_no_return_validated=False,
        biological_action_potential_validated=False,
        quiet_or_pulse_basin_validated=False,
        landing_on_periodic_branch_validated=False,
        full_network_periodic_attraction_validated=False,
        general_topology_canard_root_equivalence_validated=False,
        model_uncertainty_validated=False,
        measurement_noise_validated=False,
        hardware_validated=False,
    )


_TRUE_FIELDS = (
    "exact_symbolic_handoff_reduction_validated",
    "tracked_gain_box_contained_in_enclosing_box_validated",
    "exact_positive_phase_barrier_validated",
    "exact_negative_phase_barrier_validated",
    "piecewise_barrier_corner_forward_invariance_validated",
    "method_of_steps_frozen_delay_window_validated",
    "arbitrary_finite_balanced_topology_on_exact_synchronous_leaf_validated",
    "all_additive_inputs_zero_after_handoff_validated",
    "positive_finite_autonomous_excursion_validated",
    "negative_finite_autonomous_excursion_validated",
    "positive_finite_horizon_no_reversal_validated",
    "negative_finite_horizon_no_reversal_validated",
    "two_synchronous_terminal_faces_validated",
    "negative_unit_handoff_turn_before_minus_1_17_validated",
)

_FALSE_FIELDS = (
    "negative_unit_handoff_monotone_no_return_validated",
    "asynchronous_autonomous_excursion_validated",
    "autonomous_onset_validated",
    "permanent_no_return_validated",
    "biological_action_potential_validated",
    "quiet_or_pulse_basin_validated",
    "landing_on_periodic_branch_validated",
    "full_network_periodic_attraction_validated",
    "general_topology_canard_root_equivalence_validated",
    "model_uncertainty_validated",
    "measurement_noise_validated",
    "hardware_validated",
)


def validate_autonomous_handoff_result_payload(
    payload: Mapping[str, Any],
) -> None:
    """Refuse missing proof flags and unsupported biological promotions."""

    root = _mapping(payload, "result payload")
    source = _mapping(root.get("source_evidence"), "source_evidence")
    certificate = _mapping(root.get("certificate"), "certificate")
    scope = _mapping(root.get("scope"), "scope")
    if source.get("balanced_control_chain_result_sha256") != (
        TRACKED_BALANCED_CONTROL_CHAIN_SHA256
    ):
        raise ValueError("source evidence is not bound to the tracked parent")
    if certificate.get("balanced_control_chain_result_sha256") != (
        TRACKED_BALANCED_CONTROL_CHAIN_SHA256
    ):
        raise ValueError("certificate is not bound to the tracked parent")
    if certificate.get("model_id") != MODEL_ID:
        raise ValueError("certificate model identifier is invalid")
    if certificate.get("assumptions_id") != ASSUMPTIONS_ID:
        raise ValueError("certificate assumptions identifier is invalid")
    for name in _TRUE_FIELDS:
        if certificate.get(name) is not True:
            raise ValueError(f"proof flag {name!r} must be true")
    for name in _FALSE_FIELDS:
        if certificate.get(name) is not False:
            raise ValueError(f"scope flag {name!r} must be false")

    true_scope = (
        "same_delayed_fhn_baseline_model",
        "bounded_control_through_handoff",
        "all_additive_inputs_zero_after_handoff",
        "positive_finite_autonomous_excursion",
        "negative_finite_autonomous_excursion_after_deeper_handoff",
        "finite_horizon_no_reversal_corridors",
        "piecewise_barrier_corner_forward_invariance",
        "two_synchronous_terminal_faces",
        "negative_unit_handoff_turn_obstruction",
    )
    false_scope = (
        "asynchronous_autonomous_excursion",
        "autonomous_onset",
        "permanent_no_return",
        "biological_action_potential",
        "quiet_or_pulse_basin",
        "landing_on_periodic_branch",
        "full_network_periodic_attraction",
        "general_topology_canard_root_equivalence",
        "model_uncertainty",
        "measurement_noise",
        "hardware",
    )
    for name in true_scope:
        if scope.get(name) is not True:
            raise ValueError(f"scope flag {name!r} must be true")
    for name in false_scope:
        if scope.get(name) is not False:
            raise ValueError(f"scope flag {name!r} must be false")

    exact_strings = {
        "epsilon": "1/5",
        "unfolding": "3/5",
        "prepared_positive_history": "Phi_{1/2}",
        "prepared_negative_history": "Phi_{-1/2}",
        "positive_controlled_detector_and_handoff_face": "1",
        "negative_controlled_detector_face": "-1",
        "negative_controlled_handoff_face": "-1.12",
        "positive_autonomous_excursion_face": "1.5",
        "negative_autonomous_excursion_face": "-1.2",
        "negative_unit_handoff_turn_magnitude_upper": "1.17",
    }
    for name, expected in exact_strings.items():
        if certificate.get(name) != expected:
            raise ValueError(f"certificate field {name!r} is invalid")
    if tuple(certificate.get("enclosing_kappa_1_interval", ())) != (
        "0.199999999998",
        "0.200000000002",
    ):
        raise ValueError("enclosing kappa_1 interval is invalid")
    if tuple(certificate.get("enclosing_kappa_3_interval", ())) != (
        "0.249999999998",
        "0.250000000002",
    ):
        raise ValueError("enclosing kappa_3 interval is invalid")
    if certificate.get("positive_autonomous_barrier_segments") != 20:
        raise ValueError("positive barrier segment count is invalid")
    if certificate.get("negative_autonomous_barrier_segments") != 16:
        raise ValueError("negative barrier segment count is invalid")

    try:
        positive_slack = Decimal(str(certificate["positive_frozen_delay_slack_lower"]))
        negative_slack = Decimal(str(certificate["negative_frozen_delay_slack_lower"]))
        positive_velocity = Decimal(str(certificate["positive_autonomous_velocity_lower"]))
        negative_velocity = Decimal(
            str(certificate["negative_autonomous_magnitude_velocity_lower"])
        )
        positive_controlled = Decimal(
            str(certificate["positive_controlled_handoff_deadline_upper"])
        )
        negative_controlled = Decimal(
            str(certificate["negative_controlled_handoff_deadline_upper"])
        )
        positive_autonomous = Decimal(
            str(certificate["positive_autonomous_excursion_time_upper"])
        )
        negative_autonomous = Decimal(
            str(certificate["negative_autonomous_excursion_time_upper"])
        )
        positive_total = Decimal(
            str(certificate["positive_decision_release_to_excursion_time_upper"])
        )
        negative_total = Decimal(
            str(certificate["negative_decision_release_to_excursion_time_upper"])
        )
        minimum_delay = Decimal(str(certificate["minimum_delay_lower"]))
        positive_from_start = Decimal(
            str(certificate["positive_control_start_to_excursion_time_upper"])
        )
        negative_from_start = Decimal(
            str(certificate["negative_control_start_to_excursion_time_upper"])
        )
        positive_landing = Decimal(
            str(certificate["positive_autonomous_recovery_at_landing_upper"])
        )
        negative_landing = Decimal(
            str(
                certificate[
                    "negative_autonomous_recovery_magnitude_at_landing_upper"
                ]
            )
        )
        turn_time = Decimal(
            str(certificate["negative_unit_handoff_turn_time_upper"])
        )
        unit_initial_velocity = Decimal(
            str(
                certificate[
                    "negative_unit_initial_magnitude_velocity_lower"
                ]
            )
        )
        positive_growth_public = Decimal(
            str(certificate["positive_controlled_handoff_growth_lower"])
        )
        negative_growth_public = Decimal(
            str(certificate["negative_controlled_handoff_growth_lower"])
        )
        unit_detector = Decimal(
            str(certificate["negative_unit_controlled_detector_deadline_upper"])
        )
        unit_total = Decimal(
            str(
                certificate[
                    "negative_unit_decision_release_to_turn_time_upper"
                ]
            )
        )
        unit_slack = Decimal(
            str(certificate["negative_unit_handoff_frozen_delay_slack_lower"])
        )
    except Exception as error:
        raise ValueError("directed certificate endpoints must be decimal") from error
    if min(
        positive_slack,
        negative_slack,
        positive_velocity,
        negative_velocity,
        unit_initial_velocity,
    ) <= 0:
        raise ValueError("a directed method-of-steps or velocity margin is not positive")

    precision = certificate.get("precision_bits")
    if (
        isinstance(precision, bool)
        or not isinstance(precision, int)
        or precision < 64
    ):
        raise ValueError("certificate precision is invalid")
    exact_positive_growth = (
        Fraction(2, 3)
        - _EPSILON * (_KAPPA_1_UPPER + 3 * _KAPPA_3_UPPER)
    )
    exact_negative_handoff = Fraction(28, 25)
    exact_negative_growth = (
        1
        - exact_negative_handoff**2 / 3
        - _EPSILON
        * (
            _KAPPA_1_UPPER
            + _KAPPA_3_UPPER
            * (
                exact_negative_handoff**2
                + 3 * exact_negative_handoff
                + 3
            )
        )
    )
    exact_negative_unit_growth = (
        Fraction(2, 3)
        - _EPSILON * (_KAPPA_1_UPPER + 7 * _KAPPA_3_UPPER)
    )
    expected_positive_controlled = Decimal(
        decimal_upper(
            _deadline_upper(Fraction(2), exact_positive_growth, precision),
            55,
        )
    )
    expected_negative_controlled = Decimal(
        decimal_upper(
            _deadline_upper(
                Fraction(56, 25), exact_negative_growth, precision
            ),
            55,
        )
    )
    expected_unit_controlled = Decimal(
        decimal_upper(
            _deadline_upper(
                Fraction(2), exact_negative_unit_growth, precision
            ),
            55,
        )
    )
    expected_minimum_delay = Decimal(
        decimal_lower(_minimum_delay_lower(precision), 55)
    )
    if not (
        Fraction(positive_growth_public) <= exact_positive_growth
        and Fraction(negative_growth_public) <= exact_negative_growth
        and positive_controlled >= expected_positive_controlled
        and negative_controlled >= expected_negative_controlled
        and unit_detector >= expected_unit_controlled
        and minimum_delay <= expected_minimum_delay
    ):
        raise ValueError("a directed growth, deadline, or delay endpoint is invalid")

    positive_barrier = positive_autonomous_barrier_audit()
    negative_barrier = negative_autonomous_barrier_audit()
    obstruction = negative_unit_handoff_obstruction_audit()
    oriented_checks = (
        Fraction(positive_autonomous) >= positive_barrier.crossing_time_upper,
        Fraction(negative_autonomous) >= negative_barrier.crossing_time_upper,
        Fraction(positive_velocity) <= positive_barrier.minimum_vector_lower,
        Fraction(negative_velocity) <= negative_barrier.minimum_vector_lower,
        Fraction(positive_landing) >= positive_barrier.terminal_barrier_upper,
        Fraction(negative_landing) >= negative_barrier.terminal_barrier_upper,
        Fraction(unit_initial_velocity) <= obstruction.initial_vector_lower,
        Fraction(turn_time) >= obstruction.turn_time_upper,
    )
    if not all(oriented_checks):
        raise ValueError("an exact phase-barrier endpoint has the wrong orientation")
    with localcontext() as context:
        context.prec = 100
        parent_preparation = Decimal(
            "14.4969646778543483311608010803270678611301803436710386"
        )
        if positive_total < positive_controlled + positive_autonomous:
            raise ValueError("positive total deadline is below its public sum")
        if negative_total < negative_controlled + negative_autonomous:
            raise ValueError("negative total deadline is below its public sum")
        if unit_total < unit_detector + turn_time:
            raise ValueError("negative-unit turn deadline is below its public sum")
        if not (
            positive_total < minimum_delay
            and negative_total < minimum_delay
            and unit_total < minimum_delay
            and positive_slack <= minimum_delay - positive_total
            and negative_slack <= minimum_delay - negative_total
            and unit_slack <= minimum_delay - unit_total
            and positive_from_start >= parent_preparation + positive_total
            and negative_from_start >= parent_preparation + negative_total
        ):
            raise ValueError("public method-of-steps deadline composition failed")


def load_autonomous_handoff_result(
    path: str | Path,
    *,
    expected_sha256: str | None = None,
) -> Mapping[str, Any]:
    """Hash-check and validate a stored autonomous-handoff result."""

    result_path = Path(path)
    raw = result_path.read_bytes()
    digest = sha256(raw).hexdigest()
    if expected_sha256 is not None and digest != expected_sha256:
        raise ValueError(
            f"result SHA-256 mismatch: expected {expected_sha256}, got {digest}"
        )
    try:
        payload = json.loads(raw)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError("autonomous handoff result is not valid UTF-8 JSON") from error
    root = _mapping(payload, "result payload")
    validate_autonomous_handoff_result_payload(root)
    return root
