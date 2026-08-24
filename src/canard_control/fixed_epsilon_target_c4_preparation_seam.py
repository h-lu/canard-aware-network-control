"""Exact order-four preparation seam at the frozen target anchor.

The first target causal-tube candidate prepared only the value and first
time derivative at ``t=-3``.  This module closes the *finite seam problem*
through order four.  It does not validate the subsequent numerical solution
tube, its embedding, an interval flow enclosure, or a target fixed graph.

For a fixed-delay RFDE ``z'=F(z,z_4,z_5,z_Theta)``, let ``a_0`` be the
chosen current endpoint.  The compatible endpoint jets are defined
recursively by

    a_{m+1} = m! [s^m] F(A_m(s), B_{4,m}(s),
                         B_{5,m}(s), B_{Theta,m}(s)),

where ``A_m=sum_{j=0}^m a_j s^j/j!`` and each ``B`` is the corresponding
Taylor polynomial of the unpatched incoming history at a delayed slot.
The recursion is triangular because every delay is positive.

The jets are installed with a compact right-Hermite patch.  On ``-w<=r<=0``
put

    chi_9(1+r/w)=126 u^5-420 u^6+540 u^7-315 u^8+70 u^9,
    phi_j(r)=r^j chi_9(1+r/w)/j!.

Every derivative through order four vanishes at ``r=-w``, while
``phi_j^(k)(0)=delta_{jk}``.  Hence the piecewise polynomial incoming history
is jointly C4 and has exactly the recursive endpoint jets.  Differentiating
the identities in the transverse label gives all mixed seam identities of
total order at most four.

The exact algebra below freezes the decimal target anchor as rational input
and uses ``rho=sqrt(5)/5``.  Binary64 strip samples are diagnostics only.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from functools import lru_cache
from hashlib import sha256
import json
import math
from pathlib import Path
import platform
from typing import Mapping, Sequence

import sympy as sp

from canard_control.fixed_epsilon_target_causal_tube_candidate import (
    TARGET_ETA,
    TARGET_NU,
    TARGET_PHASE_SHIFT,
    TARGET_RHO,
    TARGET_THETA,
    TargetTubeConfiguration,
    entry_compatibility_shift,
)


MODEL_ID = "fixed-epsilon-target-c4-preparation-seam"
AUDIT_ID = "fixed-epsilon-target-c4-preparation-seam-v1"

PATCH_WIDTH = 0.5
MAXIMUM_JET_ORDER = 4
SMOOTHERSTEP9_COEFFICIENTS = (126, -420, 540, -315, 70)

TARGET_PARENT_RESULT_SHA256 = (
    "fb61c0576afb9a401f16947d47917fa03b4461a8889fbb04f3d450411c448ffd"
)
PARENT_RESULT_RELATIVE_PATH = (
    "experiments/results/fixed_epsilon_target_causal_tube_candidate.json"
)
PROOF_SOURCE_RELATIVE_PATH = (
    "src/canard_control/fixed_epsilon_target_c4_preparation_seam.py"
)
GENERATOR_RELATIVE_PATH = (
    "experiments/fixed_epsilon_target_c4_preparation_seam.py"
)
RESULT_RELATIVE_PATH = (
    "experiments/results/fixed_epsilon_target_c4_preparation_seam.json"
)
NOTE_RELATIVE_PATH = "docs/fixed-epsilon-target-c4-preparation-seam.md"
DEFAULT_COMMAND = (
    "PYTHONPATH=src /usr/bin/python3 "
    "experiments/fixed_epsilon_target_c4_preparation_seam.py"
)
MANIFEST_ARITHMETIC = (
    "exact SymPy algebra over Q(sqrt(5),lambda) for the frozen decimal "
    "anchor and degree-nine Hermite jets; binary64 preparation-strip "
    "sampling only; no interval RFDE flow, chart embedding, target graph, "
    "candidate-class self-map, trace solve, or complete-history root"
)

EXACT_RHO = sp.sqrt(5) / 5
EXACT_NU = sp.Rational("0.21256022233963731")
EXACT_ETA = sp.Integer(0)
EXACT_THETA = sp.Rational("7.3970862981881309")
EXACT_PHASE_SHIFT = sp.Rational("-0.061579261574946566")
EXACT_SECTION_HALF_WIDTH = sp.Integer(3)
EXACT_INCOMING_TIME = -EXACT_SECTION_HALF_WIDTH
EXACT_TRANSVERSE_RADIUS = sp.Rational(1, 20)
EXACT_PATCH_WIDTH = sp.Rational(1, 2)
EXACT_TRANSVERSE = sp.Symbol("lambda", real=True)


Point = tuple[float, float]
AlgebraicPoint = tuple[sp.Expr, sp.Expr]


def _finite(value: object, name: str) -> float:
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result


def _nonnegative_integer(value: object, name: str) -> int:
    if type(value) is not int or value < 0:
        raise ValueError(f"{name} must be a nonnegative integer")
    return value


def _format(value: float) -> str:
    return format(float(value), ".17g")


def smootherstep9(value: float) -> float:
    """Evaluate the degree-nine step with four flat endpoint derivatives."""

    u = _finite(value, "smootherstep argument")
    if u <= 0.0:
        return 0.0
    if u >= 1.0:
        return 1.0
    powers = (u**5, u**6, u**7, u**8, u**9)
    return float(
        sum(
            coefficient * power
            for coefficient, power in zip(
                SMOOTHERSTEP9_COEFFICIENTS, powers, strict=True
            )
        )
    )


def smootherstep9_derivative(value: float, order: int) -> float:
    """Evaluate a derivative of the degree-nine step through order four."""

    u = _finite(value, "smootherstep argument")
    derivative_order = _nonnegative_integer(order, "order")
    if derivative_order > MAXIMUM_JET_ORDER:
        raise ValueError("order must not exceed four")
    if u <= 0.0:
        return 0.0
    if u >= 1.0:
        return 1.0 if derivative_order == 0 else 0.0
    result = 0.0
    for power, coefficient in zip(
        range(5, 10), SMOOTHERSTEP9_COEFFICIENTS, strict=True
    ):
        if power >= derivative_order:
            result += (
                coefficient
                * math.factorial(power)
                / math.factorial(power - derivative_order)
                * u ** (power - derivative_order)
            )
    return _finite(result, "smootherstep derivative")


def right_jet_shape_derivative(
    relative_time: float,
    jet_order: int,
    derivative_order: int,
    width: float = PATCH_WIDTH,
) -> float:
    """Evaluate ``d^k/dr^k (r^j chi_9(1+r/w)/j!)``.

    The shape is extended by zero on ``r<=-w`` and is required only on the
    incoming side ``r<=0``.  The zero extension is C4, exactly the regularity
    needed for the present seam.
    """

    relative = _finite(relative_time, "relative_time")
    j = _nonnegative_integer(jet_order, "jet_order")
    k = _nonnegative_integer(derivative_order, "derivative_order")
    width_value = _finite(width, "width")
    if j > MAXIMUM_JET_ORDER or k > MAXIMUM_JET_ORDER:
        raise ValueError("jet and derivative orders must not exceed four")
    if width_value <= 0.0:
        raise ValueError("width must be positive")
    if relative > 0.0:
        raise ValueError("right-jet shapes are defined only for r<=0")
    if relative <= -width_value:
        return 0.0
    argument = 1.0 + relative / width_value
    result = 0.0
    for polynomial_derivatives in range(min(j, k) + 1):
        cutoff_derivatives = k - polynomial_derivatives
        result += (
            math.comb(k, polynomial_derivatives)
            * relative ** (j - polynomial_derivatives)
            / math.factorial(j - polynomial_derivatives)
            * width_value ** (-cutoff_derivatives)
            * smootherstep9_derivative(argument, cutoff_derivatives)
        )
    return _finite(result, "right-jet shape derivative")


def right_jet_shape(
    relative_time: float, jet_order: int, width: float = PATCH_WIDTH
) -> float:
    """Evaluate one compact right-Hermite jet shape."""

    return right_jet_shape_derivative(
        relative_time, jet_order, 0, width
    )


def _series_add(*values: Sequence[object]) -> list[object]:
    if not values:
        raise ValueError("at least one series is required")
    length = len(values[0])
    if any(len(value) != length for value in values):
        raise ValueError("series lengths must agree")
    return [sum(value[index] for value in values) for index in range(length)]


def _series_scale(value: Sequence[object], scalar: object) -> list[object]:
    return [scalar * item for item in value]


def _series_multiply(
    left: Sequence[object], right: Sequence[object]
) -> list[object]:
    if len(left) != len(right):
        raise ValueError("series lengths must agree")
    return [
        sum(left[index] * right[power - index] for index in range(power + 1))
        for power in range(len(left))
    ]


def physical_field_time_derivative_from_jets(
    current_jets: Sequence[Sequence[object]],
    delay_4_jets: Sequence[Sequence[object]],
    delay_5_jets: Sequence[Sequence[object]],
    delay_theta_jets: Sequence[Sequence[object]],
    *,
    rho: object,
    nu: object,
    eta: object,
    derivative_order: int,
) -> tuple[object, object]:
    """Return the requested time derivative of the physical RFDE field.

    Input entries are ordinary derivatives, not Taylor coefficients.  The
    routine uses truncated Taylor arithmetic and works both for floats and
    exact SymPy expressions.
    """

    order = _nonnegative_integer(derivative_order, "derivative_order")
    if order >= MAXIMUM_JET_ORDER:
        raise ValueError("field derivative order must lie between zero and three")
    slot_families = (
        current_jets,
        delay_4_jets,
        delay_5_jets,
        delay_theta_jets,
    )
    if any(len(slot) < order + 1 for slot in slot_families):
        raise ValueError("every slot must supply all requested derivatives")
    if any(len(point) != 2 for slot in slot_families for point in slot[: order + 1]):
        raise ValueError("every state jet must have two coordinates")

    def coordinate(
        jets: Sequence[Sequence[object]], component: int
    ) -> list[object]:
        return [
            jets[index][component] / math.factorial(index)
            for index in range(order + 1)
        ]

    x = coordinate(current_jets, 0)
    y = coordinate(current_jets, 1)
    x4 = coordinate(delay_4_jets, 0)
    x5 = coordinate(delay_5_jets, 0)
    xtheta = coordinate(delay_theta_jets, 0)

    x2 = _series_multiply(x, x)
    x3 = _series_multiply(x2, x)
    x4_cube = _series_multiply(_series_multiply(x4, x4), x4)
    x5_cube = _series_multiply(_series_multiply(x5, x5), x5)
    xtheta2 = _series_multiply(xtheta, xtheta)
    zero_tail = [rho * nu] + [0] * order
    fast = _series_add(
        y,
        _series_scale(x2, -1),
        _series_scale(x3, -rho / 3),
        _series_scale(
            _series_add(
                _series_scale(_series_add(x4, x5), sp.Rational(1, 2)),
                _series_scale(x, -1),
            ),
            rho / 5,
        ),
        _series_scale(
            _series_add(x2, _series_scale(xtheta2, -1)), rho**2 * eta
        ),
        _series_scale(
            _series_add(
                _series_scale(
                    _series_add(x4_cube, x5_cube), sp.Rational(1, 2)
                ),
                _series_scale(x3, -1),
            ),
            rho**3 / 4,
        ),
    )
    slow = _series_add(_series_scale(x, -1), zero_tail)
    multiplier = math.factorial(order)
    return multiplier * fast[order], multiplier * slow[order]


def recursive_endpoint_jets(
    current_value: Sequence[object],
    delay_4_jets: Sequence[Sequence[object]],
    delay_5_jets: Sequence[Sequence[object]],
    delay_theta_jets: Sequence[Sequence[object]],
    *,
    rho: object,
    nu: object,
    eta: object,
    maximum_order: int = MAXIMUM_JET_ORDER,
) -> tuple[tuple[object, object], ...]:
    """Construct the triangular compatible endpoint jets."""

    order = _nonnegative_integer(maximum_order, "maximum_order")
    if order > MAXIMUM_JET_ORDER:
        raise ValueError("maximum_order must not exceed four")
    if len(current_value) != 2:
        raise ValueError("current_value must have two coordinates")
    endpoint: list[tuple[object, object]] = [
        (current_value[0], current_value[1])
    ]
    for derivative_order in range(order):
        endpoint.append(
            physical_field_time_derivative_from_jets(
                endpoint,
                delay_4_jets,
                delay_5_jets,
                delay_theta_jets,
                rho=rho,
                nu=nu,
                eta=eta,
                derivative_order=derivative_order,
            )
        )
    return tuple(endpoint)


def _entry_shift_algebra(
    *,
    rho: object,
    eta: object,
    theta: object,
    phase_shift: object,
    section_half_width: object,
) -> object:
    x0 = (section_half_width - phase_shift) / 2
    x4 = (section_half_width + 4 - phase_shift) / 2
    x5 = (section_half_width + 5 - phase_shift) / 2
    xtheta = (section_half_width + theta - phase_shift) / 2
    correction = (
        rho * (-x0**3 / 3 + ((x4 + x5) / 2 - x0) / 5)
        + rho**2 * eta * (x0**2 - xtheta**2)
        + rho**3 / 4 * ((x4**3 + x5**3) / 2 - x0**3)
    )
    return -correction


def _unpatched_history_jet_algebra(
    time: object,
    transverse: object,
    derivative_order: int,
    *,
    rho: object,
    nu: object,
    eta: object,
    theta: object,
    phase_shift: object,
    section_half_width: object,
) -> tuple[object, object]:
    order = _nonnegative_integer(derivative_order, "derivative_order")
    if order > MAXIMUM_JET_ORDER:
        raise ValueError("derivative_order must not exceed four")
    if order == 0:
        shifted = time + phase_shift
        return (
            -shifted / 2,
            (shifted**2 - 2) / 4
            + rho * nu * (time + section_half_width)
            + _entry_shift_algebra(
                rho=rho,
                eta=eta,
                theta=theta,
                phase_shift=phase_shift,
                section_half_width=section_half_width,
            )
            + transverse,
        )
    if order == 1:
        return -sp.Rational(1, 2), (time + phase_shift) / 2 + rho * nu
    if order == 2:
        return 0, sp.Rational(1, 2)
    return 0, 0


def unpatched_history_jet(
    time: float,
    transverse: float,
    derivative_order: int,
    configuration: TargetTubeConfiguration | None = None,
) -> Point:
    """Evaluate the polynomial far history before the C4 correction."""

    config = configuration or TargetTubeConfiguration()
    config.validate()
    time_value = _finite(time, "time")
    transverse_value = _finite(transverse, "transverse")
    order = _nonnegative_integer(derivative_order, "derivative_order")
    if time_value > config.incoming_time:
        raise ValueError("incoming history is defined only up to entry time")
    if abs(transverse_value) > config.transverse_radius * (1.0 + 1e-14):
        raise ValueError("transverse parameter lies outside the frozen strip")
    if order > MAXIMUM_JET_ORDER:
        raise ValueError("derivative_order must not exceed four")
    if order == 0:
        shifted = time_value + config.phase_shift
        return (
            _finite(-shifted / 2.0, "unpatched X"),
            _finite(
                (shifted * shifted - 2.0) / 4.0
                + config.rho
                * config.nu
                * (time_value + config.section_half_width)
                + entry_compatibility_shift(config)
                + transverse_value,
                "unpatched Y",
            ),
        )
    if order == 1:
        return (
            -0.5,
            _finite(
                (time_value + config.phase_shift) / 2.0
                + config.rho * config.nu,
                "unpatched Y derivative",
            ),
        )
    if order == 2:
        return 0.0, 0.5
    return 0.0, 0.0


@lru_cache(maxsize=1024)
def endpoint_jets_numeric(
    transverse: float,
    configuration: TargetTubeConfiguration | None = None,
) -> tuple[Point, ...]:
    """Return binary64 evaluations of the exact recursive endpoint jets."""

    config = configuration or TargetTubeConfiguration()
    config.validate()
    transverse_value = _finite(transverse, "transverse")
    if abs(transverse_value) > config.transverse_radius * (1.0 + 1e-14):
        raise ValueError("transverse parameter lies outside the frozen strip")
    delayed = tuple(
        tuple(
            unpatched_history_jet(
                config.incoming_time - delay,
                transverse_value,
                order,
                config,
            )
            for order in range(MAXIMUM_JET_ORDER)
        )
        for delay in (4.0, 5.0, config.theta)
    )
    result = recursive_endpoint_jets(
        unpatched_history_jet(
            config.incoming_time, transverse_value, 0, config
        ),
        delayed[0],
        delayed[1],
        delayed[2],
        rho=config.rho,
        nu=config.nu,
        eta=config.eta,
    )
    return tuple(
        (_finite(point[0], "endpoint X jet"), _finite(point[1], "endpoint Y jet"))
        for point in result
    )


@lru_cache(maxsize=1)
def _exact_target_endpoint_jets() -> tuple[AlgebraicPoint, ...]:
    delayed = tuple(
        tuple(
            _unpatched_history_jet_algebra(
                EXACT_INCOMING_TIME - delay,
                EXACT_TRANSVERSE,
                order,
                rho=EXACT_RHO,
                nu=EXACT_NU,
                eta=EXACT_ETA,
                theta=EXACT_THETA,
                phase_shift=EXACT_PHASE_SHIFT,
                section_half_width=EXACT_SECTION_HALF_WIDTH,
            )
            for order in range(MAXIMUM_JET_ORDER)
        )
        for delay in (sp.Integer(4), sp.Integer(5), EXACT_THETA)
    )
    current = _unpatched_history_jet_algebra(
        EXACT_INCOMING_TIME,
        EXACT_TRANSVERSE,
        0,
        rho=EXACT_RHO,
        nu=EXACT_NU,
        eta=EXACT_ETA,
        theta=EXACT_THETA,
        phase_shift=EXACT_PHASE_SHIFT,
        section_half_width=EXACT_SECTION_HALF_WIDTH,
    )
    recursive = recursive_endpoint_jets(
        current,
        delayed[0],
        delayed[1],
        delayed[2],
        rho=EXACT_RHO,
        nu=EXACT_NU,
        eta=EXACT_ETA,
    )
    return tuple(
        (sp.expand(point[0]), sp.expand(point[1])) for point in recursive
    )


def exact_target_endpoint_jets(
    transverse_symbol: sp.Expr | None = None,
) -> tuple[AlgebraicPoint, ...]:
    """Return exact endpoint jets over ``Q(sqrt(5),lambda)``."""

    endpoint = _exact_target_endpoint_jets()
    if transverse_symbol is None or transverse_symbol == EXACT_TRANSVERSE:
        return endpoint
    return tuple(
        tuple(
            sp.expand(value.subs(EXACT_TRANSVERSE, transverse_symbol))
            for value in point
        )
        for point in endpoint
    )  # type: ignore[return-value]


@lru_cache(maxsize=1)
def _exact_endpoint_transverse_derivative_coefficients(
) -> tuple[tuple[tuple[float, ...], tuple[float, ...]], ...]:
    """Return exact-then-rounded polynomial data for endpoint derivatives.

    Each endpoint jet is an exact polynomial in ``EXACT_TRANSVERSE`` over
    ``Q(sqrt(5))``.  We differentiate those polynomials in SymPy first and
    only then round their coefficients to binary64.  The resulting Horner
    evaluation is therefore an analytic label derivative, not a neighboring
    label difference.
    """

    rows: list[tuple[tuple[float, ...], tuple[float, ...]]] = []
    for point in exact_target_endpoint_jets():
        components: list[tuple[float, ...]] = []
        for value in point:
            derivative = sp.Poly(
                sp.diff(value, EXACT_TRANSVERSE), EXACT_TRANSVERSE
            )
            components.append(
                tuple(
                    _finite(sp.N(coefficient, 30), "endpoint derivative coefficient")
                    for coefficient in derivative.all_coeffs()
                )
            )
        rows.append((components[0], components[1]))
    return tuple(rows)


def _require_frozen_target_dynamics(
    configuration: TargetTubeConfiguration,
) -> None:
    """Reject use of frozen exact polynomials at a different anchor."""

    target = TargetTubeConfiguration()
    dynamic_fields = (
        "rho",
        "nu",
        "eta",
        "theta",
        "phase_shift",
        "section_half_width",
    )
    if any(
        getattr(configuration, name) != getattr(target, name)
        for name in dynamic_fields
    ):
        raise ValueError(
            "analytic endpoint label derivatives are frozen at the target anchor"
        )


@lru_cache(maxsize=1024)
def endpoint_jets_transverse_derivative_numeric(
    transverse: float,
    configuration: TargetTubeConfiguration | None = None,
) -> tuple[Point, ...]:
    """Evaluate the exact analytic label derivatives of all endpoint jets.

    The symbolic differentiation is exact at the frozen target anchor.  This
    function merely evaluates the resulting polynomials in binary64.  The
    sampling radius and label count may change, but the RFDE parameters and
    entry section must remain frozen.
    """

    config = configuration or TargetTubeConfiguration()
    config.validate()
    _require_frozen_target_dynamics(config)
    transverse_value = _finite(transverse, "transverse")
    if abs(transverse_value) > config.transverse_radius * (1.0 + 1e-14):
        raise ValueError("transverse parameter lies outside the frozen strip")

    def evaluate(coefficients: Sequence[float]) -> float:
        value = 0.0
        for coefficient in coefficients:
            value = value * transverse_value + coefficient
        return _finite(value, "endpoint label derivative")

    return tuple(
        (evaluate(point[0]), evaluate(point[1]))
        for point in _exact_endpoint_transverse_derivative_coefficients()
    )


def exact_mixed_compatibility_defects(
) -> tuple[tuple[int, int, AlgebraicPoint], ...]:
    """Return all mixed seam defects with time-plus-label order at most four."""

    endpoint = exact_target_endpoint_jets()
    delayed = tuple(
        tuple(
            _unpatched_history_jet_algebra(
                EXACT_INCOMING_TIME - delay,
                EXACT_TRANSVERSE,
                order,
                rho=EXACT_RHO,
                nu=EXACT_NU,
                eta=EXACT_ETA,
                theta=EXACT_THETA,
                phase_shift=EXACT_PHASE_SHIFT,
                section_half_width=EXACT_SECTION_HALF_WIDTH,
            )
            for order in range(MAXIMUM_JET_ORDER)
        )
        for delay in (sp.Integer(4), sp.Integer(5), EXACT_THETA)
    )
    defects: list[tuple[int, int, AlgebraicPoint]] = []
    for field_order in range(MAXIMUM_JET_ORDER):
        right = physical_field_time_derivative_from_jets(
            endpoint,
            delayed[0],
            delayed[1],
            delayed[2],
            rho=EXACT_RHO,
            nu=EXACT_NU,
            eta=EXACT_ETA,
            derivative_order=field_order,
        )
        for transverse_order in range(MAXIMUM_JET_ORDER - field_order):
            defect = tuple(
                sp.simplify(
                    sp.diff(
                        endpoint[field_order + 1][component]
                        - right[component],
                        EXACT_TRANSVERSE,
                        transverse_order,
                    )
                )
                for component in range(2)
            )
            defects.append(
                (field_order + 1, transverse_order, defect)  # type: ignore[arg-type]
            )
    return tuple(defects)


def exact_shape_endpoint_matrices() -> tuple[sp.Matrix, sp.Matrix]:
    """Return the exact left and right 0--4 derivative matrices."""

    r = sp.Symbol("r", real=True)
    u = 1 + r / EXACT_PATCH_WIDTH
    chi = sum(
        coefficient * u**power
        for power, coefficient in zip(
            range(5, 10), SMOOTHERSTEP9_COEFFICIENTS, strict=True
        )
    )
    shapes = [r**order * chi / sp.factorial(order) for order in range(5)]
    left = sp.Matrix(
        5,
        5,
        lambda derivative_order, jet_order: sp.simplify(
            sp.diff(shapes[jet_order], r, derivative_order).subs(
                r, -EXACT_PATCH_WIDTH
            )
        ),
    )
    right = sp.Matrix(
        5,
        5,
        lambda derivative_order, jet_order: sp.simplify(
            sp.diff(shapes[jet_order], r, derivative_order).subs(r, 0)
        ),
    )
    return left, right


def c4_prepared_history_jet(
    time: float,
    transverse: float,
    derivative_order: int,
    configuration: TargetTubeConfiguration | None = None,
    *,
    width: float = PATCH_WIDTH,
) -> Point:
    """Evaluate the C4 incoming history or one of its first four time jets."""

    config = configuration or TargetTubeConfiguration()
    config.validate()
    time_value = _finite(time, "time")
    transverse_value = _finite(transverse, "transverse")
    order = _nonnegative_integer(derivative_order, "derivative_order")
    width_value = _finite(width, "width")
    if order > MAXIMUM_JET_ORDER:
        raise ValueError("derivative_order must not exceed four")
    if width_value <= 0.0 or width_value >= min(4.0, 5.0, config.theta):
        raise ValueError("width must be positive and smaller than every delay")
    if time_value > config.incoming_time:
        raise ValueError("incoming history is defined only up to entry time")
    base = unpatched_history_jet(
        time_value, transverse_value, order, config
    )
    relative = time_value - config.incoming_time
    if relative <= -width_value:
        return base
    endpoint = endpoint_jets_numeric(transverse_value, config)
    base_endpoint = tuple(
        unpatched_history_jet(
            config.incoming_time, transverse_value, jet_order, config
        )
        for jet_order in range(MAXIMUM_JET_ORDER + 1)
    )
    corrected = []
    for component in range(2):
        value = base[component]
        for jet_order in range(1, MAXIMUM_JET_ORDER + 1):
            value += (
                endpoint[jet_order][component]
                - base_endpoint[jet_order][component]
            ) * right_jet_shape_derivative(
                relative, jet_order, order, width_value
            )
        corrected.append(_finite(value, "prepared history jet"))
    return corrected[0], corrected[1]


def c4_prepared_history_state(
    time: float,
    transverse: float,
    configuration: TargetTubeConfiguration | None = None,
    *,
    width: float = PATCH_WIDTH,
) -> Point:
    """Evaluate the order-four-compatible incoming history."""

    return c4_prepared_history_jet(
        time, transverse, 0, configuration, width=width
    )


def c4_prepared_history_transverse_derivative(
    time: float,
    transverse: float,
    configuration: TargetTubeConfiguration | None = None,
    *,
    width: float = PATCH_WIDTH,
) -> Point:
    """Evaluate the analytic label derivative of the C4 history state.

    The unpatched history has derivative ``(0,1)``.  Every correction
    coefficient is an exact endpoint-jet polynomial in the transverse label;
    differentiating those polynomials before binary64 evaluation gives

    ``(0,1) + sum_{j=1}^4 partial_lambda(a_j) phi_j``.

    No neighboring-label state evaluations enter this routine.
    """

    config = configuration or TargetTubeConfiguration()
    config.validate()
    time_value = _finite(time, "time")
    transverse_value = _finite(transverse, "transverse")
    width_value = _finite(width, "width")
    if width_value <= 0.0 or width_value >= min(4.0, 5.0, config.theta):
        raise ValueError("width must be positive and smaller than every delay")
    if time_value > config.incoming_time:
        raise ValueError("incoming history is defined only up to entry time")
    if abs(transverse_value) > config.transverse_radius * (1.0 + 1e-14):
        raise ValueError("transverse parameter lies outside the frozen strip")
    relative = time_value - config.incoming_time
    if relative <= -width_value:
        return 0.0, 1.0
    endpoint_derivatives = endpoint_jets_transverse_derivative_numeric(
        transverse_value, config
    )
    derivative = [0.0, 1.0]
    for component in range(2):
        for jet_order in range(1, MAXIMUM_JET_ORDER + 1):
            derivative[component] += endpoint_derivatives[jet_order][
                component
            ] * right_jet_shape(relative, jet_order, width_value)
    return (
        _finite(derivative[0], "prepared history X label derivative"),
        _finite(derivative[1], "prepared history Y label derivative"),
    )


def _exact_endpoint_expression_digest() -> str:
    serialization = "|".join(
        sp.srepr(value)
        for point in exact_target_endpoint_jets()
        for value in point
    )
    return sha256(serialization.encode("utf-8")).hexdigest()


def _sampled_strip_diagnostics() -> tuple[float, float, float]:
    config = TargetTubeConfiguration()
    time_count = 201
    transverse_count = 21
    minimum_determinant = math.inf
    maximum_determinant = -math.inf
    maximum_correction = 0.0
    transverse_step = 1.0e-6
    for time_index in range(time_count):
        time = config.incoming_time - PATCH_WIDTH + (
            PATCH_WIDTH * time_index / (time_count - 1)
        )
        for label_index in range(transverse_count):
            transverse = -config.transverse_radius + (
                2.0
                * config.transverse_radius
                * label_index
                / (transverse_count - 1)
            )
            time_derivative = c4_prepared_history_jet(
                time, transverse, 1, config
            )
            state = c4_prepared_history_state(time, transverse, config)
            if label_index == 0:
                plus = c4_prepared_history_state(
                    time, transverse + transverse_step, config
                )
                transverse_derivative = (
                    (plus[0] - state[0]) / transverse_step,
                    (plus[1] - state[1]) / transverse_step,
                )
            elif label_index == transverse_count - 1:
                minus = c4_prepared_history_state(
                    time, transverse - transverse_step, config
                )
                transverse_derivative = (
                    (state[0] - minus[0]) / transverse_step,
                    (state[1] - minus[1]) / transverse_step,
                )
            else:
                plus = c4_prepared_history_state(
                    time, transverse + transverse_step, config
                )
                minus = c4_prepared_history_state(
                    time, transverse - transverse_step, config
                )
                transverse_derivative = (
                    (plus[0] - minus[0]) / (2.0 * transverse_step),
                    (plus[1] - minus[1]) / (2.0 * transverse_step),
                )
            determinant = (
                time_derivative[0] * transverse_derivative[1]
                - time_derivative[1] * transverse_derivative[0]
            )
            minimum_determinant = min(minimum_determinant, determinant)
            maximum_determinant = max(maximum_determinant, determinant)
            base = unpatched_history_jet(time, transverse, 0, config)
            maximum_correction = max(
                maximum_correction,
                abs(state[0] - base[0]),
                abs(state[1] - base[1]),
            )
    return minimum_determinant, maximum_determinant, maximum_correction


@dataclass(frozen=True)
class TargetC4PreparationSeamCertificate:
    model_id: str
    audit_id: str
    arithmetic: str
    parent_result_sha256: str
    frozen_target_rho: str
    frozen_target_nu: str
    frozen_target_eta: str
    frozen_target_theta: str
    frozen_phase_shift: str
    incoming_time: str
    transverse_interval: tuple[str, str]
    patch_width: str
    minimum_delay: str
    smootherstep_polynomial: str
    recursive_endpoint_formula: str
    exact_left_shape_jet_matrix: tuple[tuple[str, ...], ...]
    exact_right_shape_jet_matrix: tuple[tuple[str, ...], ...]
    exact_endpoint_jet_parameter_degrees: tuple[int, ...]
    exact_endpoint_expression_sha256: str
    exact_mixed_vector_identity_count: int
    exact_mixed_scalar_zero_count: int
    sampled_strip_time_count: int
    sampled_strip_transverse_count: int
    sampled_strip_minimum_determinant: str
    sampled_strip_maximum_determinant: str
    sampled_strip_maximum_state_correction: str
    exact_scope: str
    conditional_scope: str
    open_scope: str
    degree_nine_right_hermite_basis_proved_exactly: bool
    target_frozen_anchor_time_jet_recursion_through_order_four_proved_exactly: bool
    target_frozen_anchor_mixed_seam_identities_total_order_four_proved_exactly: bool
    target_frozen_anchor_incoming_history_is_joint_c4_proved_exactly: bool
    target_frozen_anchor_c4_preparation_seam_constructed_exactly: bool
    seam_patch_preserves_endpoint_curve_exactly: bool
    seam_patch_is_supported_inside_last_half_unit: bool
    conditional_c4_method_of_steps_continuation_from_prepared_history_proved: bool
    sampled_preparation_strip_jacobian_is_negative: bool
    target_interval_flow_enclosure_validated: bool
    target_chart_global_injectivity_proved: bool
    target_c4_solution_chart_validated: bool
    target_c4_chart_and_seam_compatibility_validated: bool
    target_candidate_class_self_map_validated: bool
    target_global_graph_fixed_point_validated: bool
    selected_trace_or_complete_history_root_validated: bool


EXACT_TRUE_FLAGS = (
    "degree_nine_right_hermite_basis_proved_exactly",
    "target_frozen_anchor_time_jet_recursion_through_order_four_proved_exactly",
    "target_frozen_anchor_mixed_seam_identities_total_order_four_proved_exactly",
    "target_frozen_anchor_incoming_history_is_joint_c4_proved_exactly",
    "target_frozen_anchor_c4_preparation_seam_constructed_exactly",
    "seam_patch_preserves_endpoint_curve_exactly",
    "seam_patch_is_supported_inside_last_half_unit",
    "conditional_c4_method_of_steps_continuation_from_prepared_history_proved",
)

NUMERICAL_TRUE_FLAGS = (
    "sampled_preparation_strip_jacobian_is_negative",
)

OPEN_FALSE_FLAGS = (
    "target_interval_flow_enclosure_validated",
    "target_chart_global_injectivity_proved",
    "target_c4_solution_chart_validated",
    "target_c4_chart_and_seam_compatibility_validated",
    "target_candidate_class_self_map_validated",
    "target_global_graph_fixed_point_validated",
    "selected_trace_or_complete_history_root_validated",
)


def build_target_c4_preparation_seam_certificate(
) -> TargetC4PreparationSeamCertificate:
    """Build the exact seam audit and the separate strip diagnostic."""

    left, right = exact_shape_endpoint_matrices()
    defects = exact_mixed_compatibility_defects()
    if left != sp.zeros(5) or right != sp.eye(5):
        raise RuntimeError("the exact Hermite endpoint matrices failed")
    if any(defect != (sp.Integer(0), sp.Integer(0)) for _, _, defect in defects):
        raise RuntimeError("an exact mixed compatibility identity failed")
    endpoint = exact_target_endpoint_jets()
    degrees = tuple(
        max(
            int(sp.Poly(value, EXACT_TRANSVERSE).degree())
            for value in point
        )
        for point in endpoint
    )
    determinant_minimum, determinant_maximum, maximum_correction = (
        _sampled_strip_diagnostics()
    )
    return TargetC4PreparationSeamCertificate(
        model_id=MODEL_ID,
        audit_id=AUDIT_ID,
        arithmetic=MANIFEST_ARITHMETIC,
        parent_result_sha256=TARGET_PARENT_RESULT_SHA256,
        frozen_target_rho="sqrt(5)/5",
        frozen_target_nu=sp.sstr(EXACT_NU),
        frozen_target_eta=sp.sstr(EXACT_ETA),
        frozen_target_theta=sp.sstr(EXACT_THETA),
        frozen_phase_shift=sp.sstr(EXACT_PHASE_SHIFT),
        incoming_time=sp.sstr(EXACT_INCOMING_TIME),
        transverse_interval=(
            sp.sstr(-EXACT_TRANSVERSE_RADIUS),
            sp.sstr(EXACT_TRANSVERSE_RADIUS),
        ),
        patch_width=sp.sstr(EXACT_PATCH_WIDTH),
        minimum_delay="4",
        smootherstep_polynomial=(
            "chi_9(u)=126*u^5-420*u^6+540*u^7-315*u^8+70*u^9"
        ),
        recursive_endpoint_formula=(
            "a_{m+1}=m![s^m]F(sum_{j=0}^m a_j s^j/j!,"
            "sum_{j=0}^m b_{tau,j} s^j/j!), m=0,1,2,3"
        ),
        exact_left_shape_jet_matrix=tuple(
            tuple(sp.sstr(left[row, column]) for column in range(5))
            for row in range(5)
        ),
        exact_right_shape_jet_matrix=tuple(
            tuple(sp.sstr(right[row, column]) for column in range(5))
            for row in range(5)
        ),
        exact_endpoint_jet_parameter_degrees=degrees,
        exact_endpoint_expression_sha256=_exact_endpoint_expression_digest(),
        exact_mixed_vector_identity_count=len(defects),
        exact_mixed_scalar_zero_count=2 * len(defects),
        sampled_strip_time_count=201,
        sampled_strip_transverse_count=21,
        sampled_strip_minimum_determinant=_format(determinant_minimum),
        sampled_strip_maximum_determinant=_format(determinant_maximum),
        sampled_strip_maximum_state_correction=_format(maximum_correction),
        exact_scope=(
            "the frozen-anchor incoming history and all time/mixed seam jets "
            "of total order at most four"
        ),
        conditional_scope=(
            "the method-of-steps solution is jointly C4 on any interval on "
            "which the polynomial RFDE solution exists"
        ),
        open_scope=(
            "interval continuation, full-chart C4 bounds and embedding, "
            "degree one, target graph, selected traces, and history root"
        ),
        degree_nine_right_hermite_basis_proved_exactly=True,
        target_frozen_anchor_time_jet_recursion_through_order_four_proved_exactly=True,
        target_frozen_anchor_mixed_seam_identities_total_order_four_proved_exactly=True,
        target_frozen_anchor_incoming_history_is_joint_c4_proved_exactly=True,
        target_frozen_anchor_c4_preparation_seam_constructed_exactly=True,
        seam_patch_preserves_endpoint_curve_exactly=True,
        seam_patch_is_supported_inside_last_half_unit=True,
        conditional_c4_method_of_steps_continuation_from_prepared_history_proved=True,
        sampled_preparation_strip_jacobian_is_negative=(
            determinant_maximum < 0.0
        ),
        target_interval_flow_enclosure_validated=False,
        target_chart_global_injectivity_proved=False,
        target_c4_solution_chart_validated=False,
        target_c4_chart_and_seam_compatibility_validated=False,
        target_candidate_class_self_map_validated=False,
        target_global_graph_fixed_point_validated=False,
        selected_trace_or_complete_history_root_validated=False,
    )


def json_ready_target_c4_preparation_seam() -> dict[str, object]:
    """Return the strict seam audit as JSON-compatible data."""

    return json.loads(
        json.dumps(
            {
                "certificate": asdict(
                    build_target_c4_preparation_seam_certificate()
                )
            }
        )
    )


def _sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def verify_parent_result(repository: Path) -> dict[str, bool]:
    """Verify the pinned target-candidate parent and its open seam gate."""

    path = repository / PARENT_RESULT_RELATIVE_PATH
    if _sha256(path) != TARGET_PARENT_RESULT_SHA256:
        raise ValueError("target causal-tube parent hash changed")
    payload = json.loads(path.read_text(encoding="utf-8"))
    certificate = payload.get("audit", {}).get("certificate", {})
    checks = {
        "parent_constructed_only_first_order_preparation": certificate.get(
            "first_order_compatible_transverse_preparation_constructed_exactly"
        )
        is True,
        "parent_left_target_c4_chart_and_seam_open": certificate.get(
            "target_c4_chart_and_seam_compatibility_validated"
        )
        is False,
        "parent_left_interval_flow_open": certificate.get(
            "target_interval_flow_enclosure_validated"
        )
        is False,
        "parent_left_target_graph_open": certificate.get(
            "target_global_graph_fixed_point_validated"
        )
        is False,
    }
    if not all(checks.values()):
        raise ValueError("target causal-tube parent claim boundary changed")
    return checks


def validate_target_c4_preparation_seam_audit(audit: Mapping[str, object]) -> None:
    """Reject weakened exact claims and every promotion of an open gate."""

    if not isinstance(audit, Mapping):
        raise ValueError("seam audit must be a mapping")
    certificate = audit.get("certificate")
    if not isinstance(certificate, Mapping):
        raise ValueError("seam audit requires a certificate mapping")
    expected_fields = {field.name for field in fields(TargetC4PreparationSeamCertificate)}
    if set(certificate) != expected_fields:
        raise ValueError("seam certificate fields changed")
    for key in EXACT_TRUE_FLAGS:
        if certificate.get(key) is not True:
            raise ValueError(f"exact or conditional seam flag was weakened: {key}")
    for key in NUMERICAL_TRUE_FLAGS:
        if certificate.get(key) is not True:
            raise ValueError(f"numerical seam diagnostic was weakened: {key}")
    for key in OPEN_FALSE_FLAGS:
        if certificate.get(key) is not False:
            raise ValueError(f"open target-chart gate was promoted: {key}")
    if certificate.get("model_id") != MODEL_ID or certificate.get("audit_id") != AUDIT_ID:
        raise ValueError("seam identifiers changed")
    if certificate.get("arithmetic") != MANIFEST_ARITHMETIC:
        raise ValueError("seam arithmetic description changed")
    if certificate.get("parent_result_sha256") != TARGET_PARENT_RESULT_SHA256:
        raise ValueError("seam parent hash changed")
    left_matrix = tuple(
        tuple(row) for row in certificate.get("exact_left_shape_jet_matrix", ())
    )
    if left_matrix != tuple(tuple("0" for _ in range(5)) for _ in range(5)):
        raise ValueError("left Hermite jet matrix changed")
    right_matrix = tuple(
        tuple(row) for row in certificate.get("exact_right_shape_jet_matrix", ())
    )
    if right_matrix != tuple(
        tuple("1" if row == column else "0" for column in range(5))
        for row in range(5)
    ):
        raise ValueError("right Hermite jet matrix changed")
    if tuple(certificate.get("exact_endpoint_jet_parameter_degrees", ())) != (
        1,
        1,
        1,
        2,
        3,
    ):
        raise ValueError("endpoint parameter degrees changed")
    if certificate.get("exact_mixed_vector_identity_count") != 10:
        raise ValueError("mixed vector identity count changed")
    if certificate.get("exact_mixed_scalar_zero_count") != 20:
        raise ValueError("mixed scalar identity count changed")
    for key in (
        "sampled_strip_minimum_determinant",
        "sampled_strip_maximum_determinant",
        "sampled_strip_maximum_state_correction",
    ):
        value = _finite(certificate.get(key), key)
        if key.endswith("determinant") and value >= 0.0:
            raise ValueError("sampled preparation determinant lost its sign")
    if float(certificate["sampled_strip_maximum_state_correction"]) <= 0.0:
        raise ValueError("the nontrivial seam correction disappeared")
    if dict(audit) != json_ready_target_c4_preparation_seam():
        raise ValueError("seam audit differs from the authoritative reference")


def validate_target_c4_preparation_seam_result(
    payload: Mapping[str, object], repository: Path
) -> None:
    """Validate a generated result, its manifest, and its pinned parent."""

    if not isinstance(payload, Mapping):
        raise ValueError("seam result must be a mapping")
    audit = payload.get("audit")
    manifest = payload.get("manifest")
    if not isinstance(audit, Mapping) or not isinstance(manifest, Mapping):
        raise ValueError("seam result requires audit and manifest mappings")
    validate_target_c4_preparation_seam_audit(audit)
    parent_checks = verify_parent_result(repository)
    expected_paths = {
        "proof_source": PROOF_SOURCE_RELATIVE_PATH,
        "generator": GENERATOR_RELATIVE_PATH,
        "note": NOTE_RELATIVE_PATH,
    }
    for key, relative in expected_paths.items():
        if manifest.get(key) != relative:
            raise ValueError(f"manifest {key} path changed")
        if manifest.get(f"{key}_sha256") != _sha256(repository / relative):
            raise ValueError(f"manifest {key} hash changed")
    if manifest.get("parent_result") != PARENT_RESULT_RELATIVE_PATH:
        raise ValueError("manifest parent path changed")
    if manifest.get("parent_result_sha256") != TARGET_PARENT_RESULT_SHA256:
        raise ValueError("manifest parent hash changed")
    if manifest.get("parent_claim_checks") != parent_checks:
        raise ValueError("manifest parent claim checks changed")
    if manifest.get("default_command") != DEFAULT_COMMAND:
        raise ValueError("manifest command changed")
    if manifest.get("arithmetic") != MANIFEST_ARITHMETIC:
        raise ValueError("manifest arithmetic changed")
    if manifest.get("python") != platform.python_version():
        raise ValueError("manifest Python version changed")
    if manifest.get("platform") != platform.platform():
        raise ValueError("manifest platform changed")


__all__ = [
    "AUDIT_ID",
    "DEFAULT_COMMAND",
    "EXACT_ETA",
    "EXACT_INCOMING_TIME",
    "EXACT_NU",
    "EXACT_PATCH_WIDTH",
    "EXACT_PHASE_SHIFT",
    "EXACT_RHO",
    "EXACT_SECTION_HALF_WIDTH",
    "EXACT_THETA",
    "EXACT_TRANSVERSE",
    "EXACT_TRANSVERSE_RADIUS",
    "EXACT_TRUE_FLAGS",
    "GENERATOR_RELATIVE_PATH",
    "MANIFEST_ARITHMETIC",
    "MAXIMUM_JET_ORDER",
    "MODEL_ID",
    "NOTE_RELATIVE_PATH",
    "NUMERICAL_TRUE_FLAGS",
    "OPEN_FALSE_FLAGS",
    "PARENT_RESULT_RELATIVE_PATH",
    "PATCH_WIDTH",
    "PROOF_SOURCE_RELATIVE_PATH",
    "RESULT_RELATIVE_PATH",
    "SMOOTHERSTEP9_COEFFICIENTS",
    "TARGET_PARENT_RESULT_SHA256",
    "TargetC4PreparationSeamCertificate",
    "build_target_c4_preparation_seam_certificate",
    "c4_prepared_history_jet",
    "c4_prepared_history_state",
    "c4_prepared_history_transverse_derivative",
    "endpoint_jets_numeric",
    "endpoint_jets_transverse_derivative_numeric",
    "exact_mixed_compatibility_defects",
    "exact_shape_endpoint_matrices",
    "exact_target_endpoint_jets",
    "json_ready_target_c4_preparation_seam",
    "physical_field_time_derivative_from_jets",
    "recursive_endpoint_jets",
    "right_jet_shape",
    "right_jet_shape_derivative",
    "smootherstep9",
    "smootherstep9_derivative",
    "unpatched_history_jet",
    "validate_target_c4_preparation_seam_audit",
    "validate_target_c4_preparation_seam_result",
    "verify_parent_result",
]
