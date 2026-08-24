"""First outward-rounded physical cell for the target C4 causal chart.

This module validates one rectangle

    -3 <= t <= -2.99,       -1/20 <= lambda <= 1/20

for the frozen target-amplitude state equation together with its true
``lambda``-variational equation.  Every real operation used in the proof is
performed by :class:`~canard_control.directed_interval.DirectedInterval` at a
fixed MPFR precision and with directed endpoint rounding.

The cell lies in the first method-of-steps interval.  All delayed arguments
therefore lie in the explicit, unpatched part of the C4 incoming history.  In
particular the delayed X coordinates are affine functions of time and their
lambda derivatives vanish.  The four-dimensional state--variation problem is
then a nonautonomous polynomial ODE on this cell.

The proof has two independent enclosure layers.

* A prescribed rectangular box ``B`` satisfies the strict interval Picard
  inclusion ``z0 + [0,h] f(T,B) subset int(B)``.  This is the wrapping box
  and proves that every solution in the label cell stays in ``B``.
* On ``B`` we enclose ``d f(t,z(t))/dt`` and use the integral Taylor formula
  through order one.  The resulting local-truncation enclosure is narrower
  than ``B`` and is used for the three P-matrix quantities.

Thus local truncation, MPFR rounding, and rectangular wrapping are all part of
the stored proof.  The result is deliberately only one physical cell.  It is
not a cover of the physical strip, a C4-history cover, a cross-separation or
collar proof, a global embedding, or a target graph theorem.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from decimal import Decimal, InvalidOperation
from functools import lru_cache
from hashlib import sha256
import json
from pathlib import Path
import platform
from typing import Any, Mapping, Sequence

import gmpy2

from canard_control.directed_interval import DirectedInterval
from canard_control.fixed_epsilon_target_chart_univalence_gate import (
    PHYSICAL_FRAME_DETERMINANT,
    PHYSICAL_TIME_FRAME,
)


MODEL_ID = "fixed-epsilon-target-first-step-outward-cell"
AUDIT_ID = "fixed-epsilon-target-first-step-outward-cell-v1"

PRECISION_BITS = 192
REFINEMENT_PRECISION_BITS = 256
TIME_LEFT = "-3"
TIME_RIGHT = "-2.99"
LABEL_LEFT = "-0.05"
LABEL_RIGHT = "0.05"

# Exact decimal anchors.  Rho is constructed as sqrt(5)/5, not from the
# binary64 constant in the exploratory causal-tube module.
NU = "0.21256022233963731"
PHASE_SHIFT = "-0.061579261574946566"
SECTION_HALF_WIDTH = "3"
PATCH_WIDTH = "0.5"

# A human-chosen wrapping box.  Its strict Picard inclusion is checked rather
# than assumed, so these decimal endpoints are proof inputs rather than
# rounded numerical output.
WRAPPING_BOX_BOUNDS = (
    ("1.524", "1.532"),
    ("0.967", "1.084"),
    ("-0.001", "0.011"),
    ("0.999", "1.001"),
)

PROOF_SOURCE_RELATIVE_PATH = (
    "src/canard_control/fixed_epsilon_target_first_step_interval.py"
)
GENERATOR_RELATIVE_PATH = (
    "experiments/fixed_epsilon_target_first_step_interval.py"
)
RESULT_RELATIVE_PATH = (
    "experiments/results/fixed_epsilon_target_first_step_interval.json"
)
NOTE_RELATIVE_PATH = "docs/fixed-epsilon-target-first-step-interval.md"
INTERVAL_BACKEND_SOURCE_RELATIVE_PATH = (
    "src/canard_control/directed_interval.py"
)
PHYSICAL_MODEL_SOURCE_RELATIVE_PATH = (
    "src/canard_control/fixed_epsilon_frozen_graph_operator.py"
)
C4_SEAM_SOURCE_RELATIVE_PATH = (
    "src/canard_control/fixed_epsilon_target_c4_preparation_seam.py"
)
UNIVALENCE_GATE_SOURCE_RELATIVE_PATH = (
    "src/canard_control/fixed_epsilon_target_chart_univalence_gate.py"
)
DEFAULT_COMMAND = (
    "PYTHONPATH=src /usr/bin/python3 "
    "experiments/fixed_epsilon_target_first_step_interval.py"
)
MANIFEST_ARITHMETIC = (
    "192-bit MPFR interval algebra with explicit downward/upward rounding; "
    "strict rectangular Picard inclusion for wrapping; first-order integral "
    "Taylor enclosure with outward-rounded total-derivative remainder; a "
    "256-bit nested recomputation audit; no binary64 flow values"
)


IntervalVector = tuple[DirectedInterval, ...]


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


def _point(value: str | int, precision: int) -> DirectedInterval:
    return DirectedInterval.from_decimal(value, precision)


def _closed(
    lower: str | int, upper: str | int, precision: int
) -> DirectedInterval:
    return DirectedInterval.from_bounds(lower, upper, precision)


def _mpfr_point(value: gmpy2.mpfr, precision: int) -> DirectedInterval:
    return DirectedInterval.from_bounds(value, value, precision)


def _symmetric(interval_radius: DirectedInterval) -> DirectedInterval:
    if interval_radius.lower < 0:
        raise ValueError("a Taylor radius must be nonnegative")
    return DirectedInterval.from_bounds(
        -interval_radius.upper,
        interval_radius.upper,
        interval_radius.precision,
    )


@dataclass(frozen=True)
class IntervalRecord:
    """Serializable outward decimal enclosure."""

    lower: str
    upper: str


def _record(value: DirectedInterval, digits: int = 70) -> IntervalRecord:
    if value.lower == 0 and value.upper == 0:
        lower, upper = "0", "0"
    else:
        lower, upper = value.decimal_bounds(digits)
    # Reparse the printed decimals and require them to contain the in-memory
    # MPFR interval.  This makes the JSON layer part of the enclosure audit.
    serialized = DirectedInterval.from_bounds(
        lower, upper, value.precision
    )
    if serialized.lower > value.lower or serialized.upper < value.upper:
        raise AssertionError("serialized interval lost an MPFR endpoint")
    return IntervalRecord(lower=lower, upper=upper)


def _constants(precision: int) -> tuple[DirectedInterval, ...]:
    five = _point(5, precision)
    rho = five.sqrt() / five
    return (
        rho,
        _point(NU, precision),
        _point(PHASE_SHIFT, precision),
        _point(SECTION_HALF_WIDTH, precision),
    )


def _entry_initial_box(
    label: DirectedInterval,
) -> IntervalVector:
    """Enclose ``(X,Y,X_lambda,Y_lambda)`` at the C4 seam.

    The right-Hermite correction starts at jet order one, so its state value
    vanishes at the right endpoint.  Hence the entry state is the unpatched
    value, while its label derivative is exactly ``(0,1)``.
    """

    precision = label.precision
    rho, nu, q, section = _constants(precision)
    two = _point(2, precision)
    three = _point(3, precision)
    four = _point(4, precision)
    five = _point(5, precision)
    time = _point(TIME_LEFT, precision)

    x0 = (section - q) / two
    x4 = (section + four - q) / two
    x5 = (section + five - q) / two
    correction = (
        rho
        * (
            -(x0**3) / three
            + ((x4 + x5) / two - x0) / five
        )
        + rho**3
        / four
        * ((x4**3 + x5**3) / two - x0**3)
    )
    entry_shift = -correction
    shifted = time + q
    y0 = (
        (shifted**2 - two) / four
        + rho * nu * (time + section)
        + entry_shift
        + label
    )
    return x0, y0, _point(0, precision), _point(1, precision)


def _delayed_x(
    time: DirectedInterval, delay: int
) -> DirectedInterval:
    """Return the exact unpatched delayed X coordinate on the first cell."""

    _, _, q, _ = _constants(time.precision)
    return -(time - _point(delay, time.precision) + q) / 2


def _state_variation_rhs(
    time: DirectedInterval, state: Sequence[DirectedInterval]
) -> IntervalVector:
    """Evaluate the first-step state plus label-variation vector field."""

    if len(state) != 4:
        raise ValueError("state-variation vectors must have four coordinates")
    if any(value.precision != time.precision for value in state):
        raise ValueError("all state intervals must use the time precision")
    precision = time.precision
    rho, nu, _, _ = _constants(precision)
    x, y, vx, vy = state
    x4 = _delayed_x(time, 4)
    x5 = _delayed_x(time, 5)
    two = _point(2, precision)
    three = _point(3, precision)
    four = _point(4, precision)
    five = _point(5, precision)

    fast = (
        y
        - x**2
        - rho * x**3 / three
        + rho / five * ((x4 + x5) / two - x)
        + rho**3 / four * ((x4**3 + x5**3) / two - x**3)
    )
    slow = -x + rho * nu
    current_x_derivative = (
        -two * x
        - rho * x**2
        - rho / five
        - three * rho**3 * x**2 / four
    )
    # On this cell all delayed X label derivatives are exactly zero.  Delayed
    # Y never enters the frozen physical field, and eta is exactly zero.
    variation_fast = current_x_derivative * vx + vy
    variation_slow = -vx
    return fast, slow, variation_fast, variation_slow


@lru_cache(maxsize=1)
def exact_first_step_reduction_defects() -> tuple[Any, ...]:
    """Return exact symbolic defects against the authoritative RFDE algebra.

    The interval evaluator is intentionally elementary.  This independent
    symbolic audit ties its four reduced equations to the exact slot formula
    already used by the C4 seam construction.
    """

    import sympy as sp

    from canard_control.fixed_epsilon_target_c4_preparation_seam import (
        physical_field_time_derivative_from_jets,
    )

    x, y, x4, x5, xtheta = sp.symbols("x y x4 x5 xtheta", real=True)
    vx, vy = sp.symbols("vx vy", real=True)
    rho, nu = sp.symbols("rho nu", real=True)
    parent_fast, parent_slow = physical_field_time_derivative_from_jets(
        ((x, y),),
        ((x4, sp.Symbol("y4")),),
        ((x5, sp.Symbol("y5")),),
        ((xtheta, sp.Symbol("ytheta")),),
        rho=rho,
        nu=nu,
        eta=sp.Integer(0),
        derivative_order=0,
    )
    reduced_fast = (
        y
        - x**2
        - rho * x**3 / 3
        + rho / 5 * ((x4 + x5) / 2 - x)
        + rho**3 / 4 * ((x4**3 + x5**3) / 2 - x**3)
    )
    reduced_slow = -x + rho * nu
    parent_variation_fast = (
        sp.diff(parent_fast, x) * vx + sp.diff(parent_fast, y) * vy
    )
    parent_variation_slow = (
        sp.diff(parent_slow, x) * vx + sp.diff(parent_slow, y) * vy
    )
    current_x_derivative = (
        -2 * x - rho * x**2 - rho / 5 - 3 * rho**3 * x**2 / 4
    )
    reduced_variation_fast = current_x_derivative * vx + vy
    reduced_variation_slow = -vx
    return tuple(
        sp.simplify(value)
        for value in (
            reduced_fast - parent_fast,
            reduced_slow - parent_slow,
            reduced_variation_fast - parent_variation_fast,
            reduced_variation_slow - parent_variation_slow,
        )
    )


@lru_cache(maxsize=1)
def exact_first_step_delay_remainder_and_frame_defects() -> tuple[Any, ...]:
    """Audit the delayed affine regime, Taylor remainder, and output frame.

    This calculation is independent of the interval evaluation.  It ties the
    duplicated decimal anchors to the exact C4 seam, differentiates the two
    active delayed histories symbolically, reconstructs every total
    derivative used in the Taylor remainder by the chain rule, and checks the
    determinant of the physical output frame imported from the univalence
    contract.
    """

    import sympy as sp

    from canard_control.fixed_epsilon_target_c4_preparation_seam import (
        EXACT_NU,
        EXACT_PATCH_WIDTH,
        EXACT_PHASE_SHIFT,
        EXACT_RHO,
        EXACT_SECTION_HALF_WIDTH,
    )

    time = sp.Symbol("t", real=True)
    label = sp.Symbol("lambda", real=True)
    x, y, vx, vy = sp.symbols("x y vx vy", real=True)
    rho = sp.sqrt(5) / 5
    nu = sp.Rational(NU)
    phase_shift = sp.Rational(PHASE_SHIFT)

    delayed = tuple(
        -(time - sp.Integer(delay) + phase_shift) / 2
        for delay in (4, 5)
    )
    parent_delayed = tuple(
        -(time - sp.Integer(delay) + EXACT_PHASE_SHIFT) / 2
        for delay in (4, 5)
    )
    x4, x5 = delayed

    fast = (
        y
        - x**2
        - rho * x**3 / 3
        + rho / 5 * ((x4 + x5) / 2 - x)
        + rho**3 / 4 * ((x4**3 + x5**3) / 2 - x**3)
    )
    slow = -x + rho * nu
    current_x_derivative = (
        -2 * x - rho * x**2 - rho / 5 - 3 * rho**3 * x**2 / 4
    )
    variation_fast = current_x_derivative * vx + vy
    variation_slow = -vx
    rhs = (fast, slow, variation_fast, variation_slow)
    variables = (x, y, vx, vy)
    chain_rule = tuple(
        sp.diff(component, time)
        + sum(
            sp.diff(component, variable) * derivative
            for variable, derivative in zip(variables, rhs, strict=True)
        )
        for component in rhs
    )

    explicit_time_derivative = (
        -rho / 10 - 3 * rho**3 * (x4**2 + x5**2) / 16
    )
    current_x_second_derivative = (
        -2 - 2 * rho * x - 3 * rho**3 * x / 2
    )
    implemented_total_derivative = (
        explicit_time_derivative + current_x_derivative * fast + slow,
        -fast,
        current_x_second_derivative * fast * vx
        + current_x_derivative * variation_fast
        + variation_slow,
        -variation_fast,
    )

    frame = sp.Matrix(PHYSICAL_TIME_FRAME)
    defects = (
        sp.Rational(NU) - EXACT_NU,
        sp.Rational(PHASE_SHIFT) - EXACT_PHASE_SHIFT,
        sp.Rational(SECTION_HALF_WIDTH) - EXACT_SECTION_HALF_WIDTH,
        sp.Rational(PATCH_WIDTH) - EXACT_PATCH_WIDTH,
        rho - EXACT_RHO,
        *(value - reference for value, reference in zip(delayed, parent_delayed)),
        *(sp.diff(value, time) + sp.Rational(1, 2) for value in delayed),
        *(sp.diff(value, label) for value in delayed),
        *(
            implemented - reconstructed
            for implemented, reconstructed in zip(
                implemented_total_derivative, chain_rule, strict=True
            )
        ),
        frame.det() - PHYSICAL_FRAME_DETERMINANT,
    )
    return tuple(sp.simplify(value) for value in defects)


def _rhs_total_time_derivative(
    time: DirectedInterval,
    state: Sequence[DirectedInterval],
    rhs: Sequence[DirectedInterval],
) -> IntervalVector:
    """Enclose ``d f(t,z(t))/dt`` on a wrapping box.

    This is a total derivative along solutions, including the derivatives of
    both known delayed X forcings.  It supplies the Lagrange/integral
    remainder in the first-order Taylor enclosure.
    """

    if len(state) != 4 or len(rhs) != 4:
        raise ValueError("state and right-hand side must have four coordinates")
    precision = time.precision
    if any(value.precision != precision for value in (*state, *rhs)):
        raise ValueError("all intervals must have the same precision")
    rho, _, _, _ = _constants(precision)
    x, _, vx, _ = state
    fast, slow, variation_fast, variation_slow = rhs
    x4 = _delayed_x(time, 4)
    x5 = _delayed_x(time, 5)
    two = _point(2, precision)
    three = _point(3, precision)
    four = _point(4, precision)
    five = _point(5, precision)
    sixteen = _point(16, precision)

    current_x_derivative = (
        -two * x
        - rho * x**2
        - rho / five
        - three * rho**3 * x**2 / four
    )
    current_x_second_derivative = (
        -two - two * rho * x - three * rho**3 * x / two
    )
    explicit_time_derivative = (
        -rho / _point(10, precision)
        - three * rho**3 * (x4**2 + x5**2) / sixteen
    )
    return (
        explicit_time_derivative + current_x_derivative * fast + slow,
        -fast,
        current_x_second_derivative * fast * vx
        + current_x_derivative * variation_fast
        + variation_slow,
        -variation_fast,
    )


def _wrapping_box(precision: int) -> IntervalVector:
    return tuple(
        _closed(lower, upper, precision)
        for lower, upper in WRAPPING_BOX_BOUNDS
    )


def _picard_image(
    initial: Sequence[DirectedInterval],
    time_cell: DirectedInterval,
    wrapping_box: Sequence[DirectedInterval],
) -> IntervalVector:
    if len(initial) != 4 or len(wrapping_box) != 4:
        raise ValueError("Picard vectors must have four coordinates")
    elapsed = time_cell - _point(TIME_LEFT, time_cell.precision)
    rhs = _state_variation_rhs(time_cell, wrapping_box)
    return tuple(
        value + elapsed * derivative
        for value, derivative in zip(initial, rhs, strict=True)
    )


def _strict_interior_gaps(
    inner: Sequence[DirectedInterval],
    outer: Sequence[DirectedInterval],
) -> tuple[tuple[DirectedInterval, DirectedInterval], ...]:
    if len(inner) != len(outer):
        raise ValueError("inner and outer vectors must have equal length")
    gaps = []
    for enclosed, container in zip(inner, outer, strict=True):
        precision = enclosed.precision
        left = _mpfr_point(enclosed.lower, precision) - _mpfr_point(
            container.lower, precision
        )
        right = _mpfr_point(container.upper, precision) - _mpfr_point(
            enclosed.upper, precision
        )
        gaps.append((left, right))
    return tuple(gaps)


def _local_truncation_radii(
    total_derivative: Sequence[DirectedInterval],
    step: DirectedInterval,
) -> IntervalVector:
    if len(total_derivative) != 4:
        raise ValueError("the total derivative must have four coordinates")
    half = _point(2, step.precision)
    factor = step**2 / half
    radii = tuple(
        factor * _mpfr_point(value.upper_abs(), step.precision)
        for value in total_derivative
    )
    # A radius is an upper-bound object, not a point evaluation.  Store it as
    # [0,r] so that its semantics and the precision-nesting audit agree.
    return tuple(
        DirectedInterval.from_bounds(0, radius.upper, step.precision)
        for radius in radii
    )


def _taylor_enclosure(
    initial: Sequence[DirectedInterval],
    initial_rhs: Sequence[DirectedInterval],
    elapsed: DirectedInterval,
    radii: Sequence[DirectedInterval],
) -> IntervalVector:
    if not len(initial) == len(initial_rhs) == len(radii) == 4:
        raise ValueError("Taylor vectors must have four coordinates")
    return tuple(
        value + elapsed * derivative + _symmetric(radius)
        for value, derivative, radius in zip(
            initial, initial_rhs, radii, strict=True
        )
    )


def _contains(
    outer: Sequence[DirectedInterval], inner: Sequence[DirectedInterval]
) -> bool:
    return len(outer) == len(inner) and all(
        container.lower <= enclosed.lower
        and enclosed.upper <= container.upper
        for container, enclosed in zip(outer, inner, strict=True)
    )


@dataclass(frozen=True)
class FirstStepIntervalCell:
    """One complete outward-rounded state--variation cell record."""

    precision_bits: int
    time_cell: IntervalRecord
    label_cell: IntervalRecord
    rho: IntervalRecord
    initial_state_variation_box: tuple[IntervalRecord, ...]
    rectangular_wrapping_box: tuple[IntervalRecord, ...]
    rhs_on_wrapping_box: tuple[IntervalRecord, ...]
    picard_image: tuple[IntervalRecord, ...]
    picard_left_gap_lower: tuple[str, ...]
    picard_right_gap_lower: tuple[str, ...]
    total_rhs_time_derivative_on_wrapping_box: tuple[IntervalRecord, ...]
    local_truncation_radius_upper: tuple[str, ...]
    first_order_taylor_enclosure: tuple[IntervalRecord, ...]
    time_principal_minor: IntervalRecord
    lambda_principal_minor: IntervalRecord
    oriented_determinant: IntervalRecord
    raw_chart_determinant: IntervalRecord


@dataclass(frozen=True)
class TargetFirstStepIntervalCertificate:
    model_id: str
    audit_id: str
    arithmetic: str
    gmpy2_version: str
    mpfr_version: str
    coordinate_order: tuple[str, ...]
    physical_output_frame: tuple[tuple[int, int], tuple[int, int]]
    physical_frame_determinant: int
    delayed_history_regime: str
    wrapping_method: str
    local_truncation_method: str
    primary_cell: FirstStepIntervalCell
    refinement_precision_bits: int
    refinement_nested_in_primary: bool
    exact_reduction_to_first_step_ode_verified: bool
    exact_delayed_affine_remainder_and_frame_audit_verified: bool
    strict_picard_inclusion_validated: bool
    first_order_local_truncation_enclosure_validated: bool
    directed_rounding_used_for_every_real_operation: bool
    serialized_decimal_bounds_reparsed_outward: bool
    first_physical_p_matrix_cell_validated: bool
    state_and_true_lambda_variation_enclosed_together: bool
    delayed_x_variations_identically_zero_on_cell_proved: bool
    binary64_flow_or_sampling_used: bool
    full_first_method_step_cover_validated: bool
    full_physical_strip_interval_cover_validated: bool
    c4_history_interval_cover_validated: bool
    cross_separation_interval_validated: bool
    expanded_open_collar_interval_validated: bool
    target_chart_global_embedding_validated: bool
    target_global_graph_fixed_point_validated: bool
    exact_scope: str
    remaining_gate: str


RIGOROUS_TRUE_FLAGS = (
    "exact_reduction_to_first_step_ode_verified",
    "exact_delayed_affine_remainder_and_frame_audit_verified",
    "strict_picard_inclusion_validated",
    "first_order_local_truncation_enclosure_validated",
    "directed_rounding_used_for_every_real_operation",
    "serialized_decimal_bounds_reparsed_outward",
    "first_physical_p_matrix_cell_validated",
    "state_and_true_lambda_variation_enclosed_together",
    "delayed_x_variations_identically_zero_on_cell_proved",
)
FALSE_METHOD_FLAGS = ("binary64_flow_or_sampling_used",)
OPEN_FLAGS = (
    "full_first_method_step_cover_validated",
    "full_physical_strip_interval_cover_validated",
    "c4_history_interval_cover_validated",
    "cross_separation_interval_validated",
    "expanded_open_collar_interval_validated",
    "target_chart_global_embedding_validated",
    "target_global_graph_fixed_point_validated",
)


def _build_cell(precision: int) -> tuple[FirstStepIntervalCell, tuple[DirectedInterval, ...]]:
    if type(precision) is not int or precision < 64:
        raise ValueError("precision must be an integer of at least 64 bits")
    time_cell = _closed(TIME_LEFT, TIME_RIGHT, precision)
    label_cell = _closed(LABEL_LEFT, LABEL_RIGHT, precision)
    elapsed = time_cell - _point(TIME_LEFT, precision)
    step = _point("0.01", precision)
    initial = _entry_initial_box(label_cell)
    wrapping = _wrapping_box(precision)
    rhs_wrapping = _state_variation_rhs(time_cell, wrapping)
    picard = _picard_image(initial, time_cell, wrapping)
    gaps = _strict_interior_gaps(picard, wrapping)
    if any(left.lower <= 0 or right.lower <= 0 for left, right in gaps):
        raise AssertionError("the first-step Picard inclusion is not strict")

    total_derivative = _rhs_total_time_derivative(
        time_cell, wrapping, rhs_wrapping
    )
    radii = _local_truncation_radii(total_derivative, step)
    initial_rhs = _state_variation_rhs(
        _point(TIME_LEFT, precision), initial
    )
    taylor = _taylor_enclosure(initial, initial_rhs, elapsed, radii)
    if not _contains(wrapping, taylor):
        raise AssertionError("the Taylor enclosure left the wrapping box")

    rhs_taylor = _state_variation_rhs(time_cell, taylor)
    fast, slow = rhs_taylor[:2]
    vx, vy = taylor[2:]
    time_row, label_row = PHYSICAL_TIME_FRAME
    time_minor = time_row[0] * fast + time_row[1] * slow
    lambda_minor = label_row[0] * vx + label_row[1] * vy
    raw_determinant = fast * vy - slow * vx
    oriented_determinant = PHYSICAL_FRAME_DETERMINANT * raw_determinant
    if (
        time_minor.lower <= 0
        or lambda_minor.lower <= 0
        or oriented_determinant.lower <= 0
        or raw_determinant.upper >= 0
    ):
        raise AssertionError("the first physical P-matrix cell did not close")

    rho = _constants(precision)[0]
    cell = FirstStepIntervalCell(
        precision_bits=precision,
        time_cell=_record(time_cell),
        label_cell=_record(label_cell),
        rho=_record(rho),
        initial_state_variation_box=tuple(map(_record, initial)),
        rectangular_wrapping_box=tuple(map(_record, wrapping)),
        rhs_on_wrapping_box=tuple(map(_record, rhs_wrapping)),
        picard_image=tuple(map(_record, picard)),
        picard_left_gap_lower=tuple(
            _record(left).lower for left, _ in gaps
        ),
        picard_right_gap_lower=tuple(
            _record(right).lower for _, right in gaps
        ),
        total_rhs_time_derivative_on_wrapping_box=tuple(
            map(_record, total_derivative)
        ),
        local_truncation_radius_upper=tuple(
            _record(radius).upper for radius in radii
        ),
        first_order_taylor_enclosure=tuple(map(_record, taylor)),
        time_principal_minor=_record(time_minor),
        lambda_principal_minor=_record(lambda_minor),
        oriented_determinant=_record(oriented_determinant),
        raw_chart_determinant=_record(raw_determinant),
    )
    proof_intervals = (
        *initial,
        *wrapping,
        *rhs_wrapping,
        *picard,
        *total_derivative,
        *radii,
        *taylor,
        time_minor,
        lambda_minor,
        oriented_determinant,
        raw_determinant,
    )
    return cell, proof_intervals


def _nested(
    coarse: Sequence[DirectedInterval], fine: Sequence[DirectedInterval]
) -> bool:
    return len(coarse) == len(fine) and all(
        outer.lower <= inner.lower and inner.upper <= outer.upper
        for outer, inner in zip(coarse, fine, strict=True)
    )


def build_target_first_step_interval_certificate(
) -> TargetFirstStepIntervalCertificate:
    """Build the rigorous one-cell certificate and precision audit."""

    if (
        _decimal(TIME_RIGHT, "time right") - Decimal(4)
        >= _decimal(TIME_LEFT, "time left") - _decimal(PATCH_WIDTH, "patch width")
    ):
        raise AssertionError("an active delay entered the C4 Hermite patch")
    primary, primary_intervals = _build_cell(PRECISION_BITS)
    _, refined_intervals = _build_cell(REFINEMENT_PRECISION_BITS)
    nested = _nested(primary_intervals, refined_intervals)
    if not nested:
        raise AssertionError("the higher-precision recomputation is not nested")
    if any(defect != 0 for defect in exact_first_step_reduction_defects()):
        raise AssertionError("the first-step equations differ from the RFDE algebra")
    if any(
        defect != 0
        for defect in exact_first_step_delay_remainder_and_frame_defects()
    ):
        raise AssertionError(
            "the delayed regime, Taylor derivative, or physical frame changed"
        )
    return TargetFirstStepIntervalCertificate(
        model_id=MODEL_ID,
        audit_id=AUDIT_ID,
        arithmetic=MANIFEST_ARITHMETIC,
        gmpy2_version=gmpy2.version(),
        mpfr_version=gmpy2.mpfr_version(),
        coordinate_order=("X", "Y", "partial_lambda X", "partial_lambda Y"),
        physical_output_frame=PHYSICAL_TIME_FRAME,
        physical_frame_determinant=PHYSICAL_FRAME_DETERMINANT,
        delayed_history_regime=(
            "for t in [-3,-2.99], t-4<=-6.99<-3.5; all active delayed "
            "slots lie in the exact unpatched history, delayed X is affine "
            "in t, and partial_lambda delayed X is identically zero"
        ),
        wrapping_method=(
            "strict interval Picard self-map in one rectangular four-"
            "coordinate box B; dependency loss is retained as wrapping"
        ),
        local_truncation_method=(
            "z(t)=z0+s f(t0,z0)+R2 with |R2_i| <= "
            "s^2 sup|d f_i/dt|/2, the total derivative being enclosed on B"
        ),
        primary_cell=primary,
        refinement_precision_bits=REFINEMENT_PRECISION_BITS,
        refinement_nested_in_primary=True,
        exact_reduction_to_first_step_ode_verified=True,
        exact_delayed_affine_remainder_and_frame_audit_verified=True,
        strict_picard_inclusion_validated=True,
        first_order_local_truncation_enclosure_validated=True,
        directed_rounding_used_for_every_real_operation=True,
        serialized_decimal_bounds_reparsed_outward=True,
        first_physical_p_matrix_cell_validated=True,
        state_and_true_lambda_variation_enclosed_together=True,
        delayed_x_variations_identically_zero_on_cell_proved=True,
        binary64_flow_or_sampling_used=False,
        full_first_method_step_cover_validated=False,
        full_physical_strip_interval_cover_validated=False,
        c4_history_interval_cover_validated=False,
        cross_separation_interval_validated=False,
        expanded_open_collar_interval_validated=False,
        target_chart_global_embedding_validated=False,
        target_global_graph_fixed_point_validated=False,
        exact_scope=(
            "rigorous computer-assisted enclosure of exactly one physical "
            "time-label rectangle at the frozen decimal target anchor"
        ),
        remaining_gate=(
            "continue a wrapping-controlled method of steps across the full "
            "physical strip, combine it with the independent C4-history and "
            "cross-separation covers on an enlarged label collar, and only "
            "then invoke the conditional Gale--Nikaido embedding theorem"
        ),
    )


def json_ready_target_first_step_interval() -> dict[str, Any]:
    return json.loads(
        json.dumps(
            {"certificate": asdict(build_target_first_step_interval_certificate())}
        )
    )


def validate_target_first_step_interval_audit(
    payload: Mapping[str, Any],
) -> None:
    """Reject altered enclosures, provenance loss, and claim promotion."""

    if not isinstance(payload, Mapping):
        raise ValueError("the target first-step audit must be a mapping")
    certificate = payload.get("certificate")
    if not isinstance(certificate, Mapping):
        raise ValueError("the target first-step certificate must be a mapping")
    if any(certificate.get(name) is not True for name in RIGOROUS_TRUE_FLAGS):
        raise ValueError("a rigorous first-cell flag was weakened")
    if any(certificate.get(name) is not False for name in FALSE_METHOD_FLAGS):
        raise ValueError("a forbidden numerical method flag was promoted")
    if any(certificate.get(name) is not False for name in OPEN_FLAGS):
        raise ValueError("an open target-chart claim was promoted")
    if certificate.get("refinement_nested_in_primary") is not True:
        raise ValueError("the precision nesting audit was weakened")
    if certificate.get("physical_output_frame") != [
        list(row) for row in PHYSICAL_TIME_FRAME
    ]:
        raise ValueError("the physical output frame changed")
    if certificate.get("physical_frame_determinant") != PHYSICAL_FRAME_DETERMINANT:
        raise ValueError("the physical frame determinant changed")
    boolean_fields = {
        field.name
        for field in fields(TargetFirstStepIntervalCertificate)
        if field.type in (bool, "bool")
    }
    expected = (
        set(RIGOROUS_TRUE_FLAGS)
        | set(FALSE_METHOD_FLAGS)
        | set(OPEN_FLAGS)
        | {"refinement_nested_in_primary"}
    )
    if boolean_fields != expected:
        raise AssertionError("the first-cell claim ledger is incomplete")

    cell = certificate.get("primary_cell")
    if not isinstance(cell, Mapping):
        raise ValueError("the primary cell is missing")
    for name in (
        "time_principal_minor",
        "lambda_principal_minor",
        "oriented_determinant",
    ):
        interval = cell.get(name)
        if not isinstance(interval, Mapping):
            raise ValueError(f"{name} interval is missing")
        if _decimal(interval.get("lower"), f"{name} lower") <= 0:
            raise ValueError(f"{name} does not have a strict positive margin")
    raw = cell.get("raw_chart_determinant")
    if not isinstance(raw, Mapping) or _decimal(
        raw.get("upper"), "raw determinant upper"
    ) >= 0:
        raise ValueError("the raw chart determinant is not strictly negative")
    for name in ("picard_left_gap_lower", "picard_right_gap_lower"):
        gaps = cell.get(name)
        if not isinstance(gaps, list) or len(gaps) != 4:
            raise ValueError(f"{name} has the wrong shape")
        if any(_decimal(value, name) <= 0 for value in gaps):
            raise ValueError(f"{name} lost strict inclusion")
    radii = cell.get("local_truncation_radius_upper")
    if not isinstance(radii, list) or len(radii) != 4:
        raise ValueError("local truncation radii have the wrong shape")
    if any(_decimal(value, "local truncation radius") <= 0 for value in radii):
        raise ValueError("every local truncation radius must be positive")
    if dict(payload) != json_ready_target_first_step_interval():
        raise ValueError("the target first-step audit differs from reference")


def _sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def validate_target_first_step_interval_result(
    payload: Mapping[str, Any], repository: Path
) -> None:
    """Validate a generated one-cell result and its local provenance."""

    if not isinstance(payload, Mapping):
        raise ValueError("the target first-step result must be a mapping")
    audit = payload.get("audit")
    manifest = payload.get("manifest")
    if not isinstance(audit, Mapping) or not isinstance(manifest, Mapping):
        raise ValueError("the result requires audit and manifest mappings")
    validate_target_first_step_interval_audit(audit)
    expected_paths = {
        "proof_source": PROOF_SOURCE_RELATIVE_PATH,
        "generator": GENERATOR_RELATIVE_PATH,
        "note": NOTE_RELATIVE_PATH,
        "interval_backend_source": INTERVAL_BACKEND_SOURCE_RELATIVE_PATH,
        "physical_model_source": PHYSICAL_MODEL_SOURCE_RELATIVE_PATH,
        "c4_seam_source": C4_SEAM_SOURCE_RELATIVE_PATH,
        "univalence_gate_source": UNIVALENCE_GATE_SOURCE_RELATIVE_PATH,
    }
    for name, relative in expected_paths.items():
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
    "C4_SEAM_SOURCE_RELATIVE_PATH",
    "DEFAULT_COMMAND",
    "FALSE_METHOD_FLAGS",
    "FirstStepIntervalCell",
    "IntervalRecord",
    "INTERVAL_BACKEND_SOURCE_RELATIVE_PATH",
    "LABEL_LEFT",
    "LABEL_RIGHT",
    "MANIFEST_ARITHMETIC",
    "MODEL_ID",
    "OPEN_FLAGS",
    "PHYSICAL_MODEL_SOURCE_RELATIVE_PATH",
    "PRECISION_BITS",
    "REFINEMENT_PRECISION_BITS",
    "RESULT_RELATIVE_PATH",
    "RIGOROUS_TRUE_FLAGS",
    "TIME_LEFT",
    "TIME_RIGHT",
    "TargetFirstStepIntervalCertificate",
    "UNIVALENCE_GATE_SOURCE_RELATIVE_PATH",
    "build_target_first_step_interval_certificate",
    "exact_first_step_delay_remainder_and_frame_defects",
    "exact_first_step_reduction_defects",
    "json_ready_target_first_step_interval",
    "validate_target_first_step_interval_audit",
    "validate_target_first_step_interval_result",
]
