"""Bounded clock-positive extension for the fixed-epsilon graph operator.

The earlier frozen graph operator uses a zero exterior.  It is bounded and
complete, but Q_X=0 there, so sigma_dot=0 and the causal restriction cannot
start.  This module freezes a different artificial extension.

On the physical plateau the extension is exactly the same quadratic
period-locked graph operator.  In the remote exterior it is a bounded
clocked canard field Q_v.  Its canard coordinates satisfy

    sigma_dot=v(sigma)>0,    d_dot=0,

and v(sigma)=1 on a large finite clock core.  At zero amplitude the slot
transform is independent of its candidate and has an explicit unique fixed
point.  Applying the pinned special-flow and finite mixed-jet theorems to the
exact weak-delay factorization proves a non-explicit small-rho graph family
and promotes the declared transform derivative to its first graph jet.

No graph at rho=1/sqrt(5), target clock, barrier, retained target hull, trace
family, or fixed-epsilon root is validated here.  The Volterra result recorded
below is an abstract theorem under explicit self-map, causal-flow,
incoming-trace, and uniform Lipschitz hypotheses.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from hashlib import sha256
import json
import math
from pathlib import Path
import platform
from typing import Any, Mapping, Sequence

from canard_control.directed_interval import DirectedInterval
from canard_control.fixed_epsilon_frozen_graph_operator import (
    FlowSlots,
    validate_frozen_graph_operator_result,
)
from canard_control.fixed_epsilon_singular_reachable_hull import (
    validate_singular_reachable_hull_result,
)
from canard_control.fixed_window_prepared_gap_seed import (
    BLOCH_RESULT_SHA256 as SEED_BLOCH_RESULT_SHA256,
    GREEN_PHASE_DOC_SHA256 as SEED_GREEN_PHASE_DOC_SHA256,
    PERIOD_LOWER as SEED_PERIOD_LOWER,
    PERIOD_UPPER as SEED_PERIOD_UPPER,
    QUADRATIC_PERIOD_LOCKED_ROOT_DOC_SHA256 as SEED_QUADRATIC_DOC_SHA256,
    SLIDING_WINDOW_BRIDGE_RESULT_SHA256 as SEED_BRIDGE_RESULT_SHA256,
    validate_fixed_window_gap_seed_payload,
)


MODEL_ID = "quadratic-period-lock-fixed-epsilon-clocked-tail-graph"
AUDIT_ID = "fixed-epsilon-clocked-tail-graph-extension-v1"
PRECISION_BITS = 512

LEFT_EXTERIOR_END = -30
LEFT_PLATEAU_START = -29
RIGHT_PLATEAU_END = 21
RIGHT_EXTERIOR_START = 22
NORMAL_PLATEAU_RADIUS = 1
NORMAL_SUPPORT_RADIUS = 2
DECLARED_PHASE_LEFT = -21
DECLARED_PHASE_RIGHT = 21
TAIL_CLOCK_RADIUS = 64
TAIL_FAR_FIELD_START_RADIUS = 128

# Exact serialized endpoints copied from the pinned singular-hull result.
THETA_LOWER = (
    "7.3970862959520600605496654174898409301164678211784933042579909564999999"
    "999999999999999999999999999999999999999999999999999999999999999999999999"
    "99999999998890756"
)
THETA_UPPER = (
    "7.3970863004241960155492448103081882675790202920942079556261116625000000"
    "000000000000000000000000000000000000000000000000000000000000000000000000"
    "00000000000736861"
)

FROZEN_GRAPH_RESULT_SHA256 = (
    "2c16c96153c056dd7880adacf3d0f9247a3cecd9f8b5369ffd403b826b3b43be"
)
SINGULAR_HULL_RESULT_SHA256 = (
    "0bf501b77fa43761e34a8ad084b7630912bf56850f43e5c094e17dbc08a78431"
)
FIXED_WINDOW_SEED_RESULT_SHA256 = (
    "41d325ca4c06b2e1b8a6ffa4e3908737c7be3d34a937a8a852ef7d1195321f39"
)
SPECIAL_FLOW_GRAPH_DOC_SHA256 = (
    "9c7d7073ef9b3d01bd69e9c559445be470c74622c993cf8051c7c0b21904657d"
)
MIXED_JET_GRAPH_DOC_SHA256 = (
    "45e4f6d4a5e7b47b96c56b07dafb94ffc540c76e499b2204a1913b123eb61bb5"
)

PARENT_SHA256 = {
    "fixed_epsilon_frozen_graph_operator_result": FROZEN_GRAPH_RESULT_SHA256,
    "fixed_epsilon_singular_reachable_hull_result": (
        SINGULAR_HULL_RESULT_SHA256
    ),
    "fixed_window_prepared_gap_seed_result": FIXED_WINDOW_SEED_RESULT_SHA256,
    "special_flow_graph_theorem_doc": SPECIAL_FLOW_GRAPH_DOC_SHA256,
    "mixed_jet_graph_theorem_doc": MIXED_JET_GRAPH_DOC_SHA256,
}

PARENT_CLAIM_CHECK_KEYS = {
    "frozen_parent_has_zero_exterior_and_open_graph_solve",
    "singular_parent_proves_zero_exterior_clock_failure_and_causal_lemma",
    "seed_parent_declares_same_first_jet_but_leaves_realization_open",
    "theta_endpoints_replayed_exactly",
    "special_flow_parent_requires_bounded_smooth_fields",
    "mixed_jet_parent_proves_fixed_cutoff_c3_graph_family",
    "frozen_parent_provides_conditional_seeley_preparation_rule",
    "seed_parent_self_hashes_and_condition_21_pinned",
    "seed_parent_recursive_upstream_evidence_replayed",
}

PROOF_SOURCE_RELATIVE_PATH = (
    "src/canard_control/fixed_epsilon_clocked_tail_graph_extension.py"
)
GENERATOR_RELATIVE_PATH = (
    "experiments/fixed_epsilon_clocked_tail_graph_extension.py"
)
RESULT_RELATIVE_PATH = (
    "experiments/results/fixed_epsilon_clocked_tail_graph_extension.json"
)
NOTE_RELATIVE_PATH = "docs/fixed-epsilon-clocked-tail-graph-extension.md"
DEFAULT_COMMAND = (
    "PYTHONPATH=src /usr/bin/python3 "
    "experiments/fixed_epsilon_clocked_tail_graph_extension.py"
)
MANIFEST_ARITHMETIC = (
    "exact operator and canard-coordinate algebra, binary64 diagnostic "
    "cutoff/slot evaluators, and 512-bit MPFR-directed phase-slot "
    "containment; no computed target-amplitude candidate or interval flow, "
    "no target "
    "clock/barrier, target graph solve, trace solve, or root validation"
)


Point = tuple[float, float]


def _finite(value: object, name: str) -> float:
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result


def _point(value: Sequence[float], name: str = "point") -> Point:
    if len(value) != 2:
        raise ValueError(f"{name} must have two coordinates")
    return _finite(value[0], f"{name}[0]"), _finite(value[1], f"{name}[1]")


def canard_coordinates(state: Sequence[float]) -> Point:
    """Return (sigma,d)=(-2X,Y-X^2+1/2)."""

    x, y = _point(state)
    sigma = -2.0 * x
    normal = y - x * x + 0.5
    if not math.isfinite(sigma) or not math.isfinite(normal):
        raise ValueError("canard coordinates overflow binary64")
    return sigma, normal


def state_from_canard_coordinates(sigma: float, normal: float) -> Point:
    """Invert the global polynomial canard coordinates."""

    sigma_value = _finite(sigma, "sigma")
    normal_value = _finite(normal, "normal")
    x = -sigma_value / 2.0
    y = x * x - 0.5 + normal_value
    if not math.isfinite(x) or not math.isfinite(y):
        raise ValueError("state coordinates overflow binary64")
    return x, y


def smooth_step(value: float) -> float:
    """A smooth step equal to zero on z<=0 and one on z>=1."""

    z = _finite(value, "step argument")
    if z <= 0.0:
        return 0.0
    if z >= 1.0:
        return 1.0
    left = math.exp(-1.0 / z)
    right = math.exp(-1.0 / (1.0 - z))
    return left / (left + right)


def smooth_step_derivative(value: float) -> float:
    """Return the binary64 derivative of smooth_step."""

    z = _finite(value, "step argument")
    if z <= 0.0 or z >= 1.0:
        return 0.0
    step = smooth_step(z)
    if step == 0.0 or step == 1.0:
        return 0.0
    logarithmic_derivative = 1.0 / z**2 + 1.0 / (1.0 - z) ** 2
    result = step * (1.0 - step) * logarithmic_derivative
    if not math.isfinite(result):
        raise ValueError("step derivative overflows binary64")
    return result


def flat_radial_cutoff(radius: float) -> float:
    """A smooth cutoff equal to one on r<=1 and zero on r>=2."""

    value = _finite(radius, "radius")
    if value < 0.0:
        raise ValueError("radius must be nonnegative")
    if value <= 1.0:
        return 1.0
    if value >= 2.0:
        return 0.0
    left = math.exp(-1.0 / (value - 1.0))
    right = math.exp(-1.0 / (2.0 - value))
    return right / (left + right)


def flat_radial_cutoff_derivative(radius: float) -> float:
    """Return the derivative of flat_radial_cutoff."""

    value = _finite(radius, "radius")
    if value < 0.0:
        raise ValueError("radius must be nonnegative")
    if value <= 1.0 or value >= 2.0:
        return 0.0
    cutoff = flat_radial_cutoff(value)
    return cutoff * (1.0 - cutoff) * (
        -1.0 / (2.0 - value) ** 2 - 1.0 / (value - 1.0) ** 2
    )


def longitudinal_cutoff(sigma: float) -> float:
    """Return the asymmetric flat cutoff in the canard phase."""

    sigma_value = _finite(sigma, "sigma")
    return smooth_step(sigma_value - LEFT_EXTERIOR_END) * smooth_step(
        RIGHT_EXTERIOR_START - sigma_value
    )


def longitudinal_cutoff_derivative(sigma: float) -> float:
    """Return da/dsigma for longitudinal_cutoff."""

    sigma_value = _finite(sigma, "sigma")
    left = smooth_step(sigma_value - LEFT_EXTERIOR_END)
    right = smooth_step(RIGHT_EXTERIOR_START - sigma_value)
    return (
        smooth_step_derivative(sigma_value - LEFT_EXTERIOR_END) * right
        - left
        * smooth_step_derivative(RIGHT_EXTERIOR_START - sigma_value)
    )


def normal_cutoff(normal: float) -> float:
    """Return the flat normal cutoff with radii one and two."""

    normal_value = _finite(normal, "normal")
    return flat_radial_cutoff(abs(normal_value))


def normal_cutoff_derivative(normal: float) -> float:
    """Return dc/dd for normal_cutoff."""

    normal_value = _finite(normal, "normal")
    if normal_value == 0.0:
        return 0.0
    sign = math.copysign(1.0, normal_value)
    return flat_radial_cutoff_derivative(abs(normal_value)) * sign


def raw_constant_clock_germ(state: Sequence[float]) -> Point:
    """Return Q_c=(-1/2,-X), an exact but unbounded clock germ."""

    x, _ = _point(state)
    return -0.5, -x


def bounded_clock_profile(sigma: float) -> float:
    """Return the positive bounded-tail phase speed v(sigma)."""

    sigma_value = _finite(sigma, "sigma")
    ratio = abs(sigma_value) / TAIL_CLOCK_RADIUS
    if ratio <= 1.0:
        return 1.0
    if ratio >= 2.0:
        return 1.0 / ratio
    cutoff = flat_radial_cutoff(ratio)
    return cutoff + (1.0 - cutoff) / ratio


def bounded_clock_profile_derivative(sigma: float) -> float:
    """Return dv/dsigma for bounded_clock_profile."""

    sigma_value = _finite(sigma, "sigma")
    absolute = abs(sigma_value)
    ratio = absolute / TAIL_CLOCK_RADIUS
    if ratio <= 1.0:
        return 0.0
    if ratio >= 2.0:
        inverse_ratio = 1.0 / ratio
        radial = -(inverse_ratio * inverse_ratio)
    else:
        cutoff = flat_radial_cutoff(ratio)
        cutoff_derivative = flat_radial_cutoff_derivative(ratio)
        radial = (
            cutoff_derivative * (1.0 - 1.0 / ratio)
            + (cutoff - 1.0) / ratio**2
        )
    sign = math.copysign(1.0, sigma_value)
    return radial * sign / TAIL_CLOCK_RADIUS


def bounded_clock_tail(state: Sequence[float]) -> Point:
    """Return Q_v=(-v/2,sigma*v/2), a bounded complete canard tail."""

    x, _ = _point(state)
    if abs(x) >= TAIL_FAR_FIELD_START_RADIUS / 2.0:
        speed = (TAIL_CLOCK_RADIUS / 2.0) / abs(x)
        return -speed / 2.0, -math.copysign(
            TAIL_CLOCK_RADIUS / 2.0, x
        )
    sigma = -2.0 * x
    speed = bounded_clock_profile(sigma)
    return -speed / 2.0, sigma * speed / 2.0


def clocked_tail_weight(state: Sequence[float]) -> float:
    """Return w(sigma,d)=a(sigma)c(d) without exterior overflow."""

    x, y = _point(state)
    # sigma=-2X lies outside [-30,22] when X>=15 or X<=-11.
    if x >= 15.0 or x <= -11.0:
        return 0.0
    sigma = -2.0 * x
    normal = y - x * x + 0.5
    return longitudinal_cutoff(sigma) * normal_cutoff(normal)


def clocked_tail_weight_gradient(state: Sequence[float]) -> Point:
    """Return the Cartesian gradient of clocked_tail_weight."""

    x, y = _point(state)
    if x >= 15.0 or x <= -11.0:
        return 0.0, 0.0
    sigma = -2.0 * x
    normal = y - x * x + 0.5
    a_value = longitudinal_cutoff(sigma)
    a_derivative = longitudinal_cutoff_derivative(sigma)
    c_value = normal_cutoff(normal)
    c_derivative = normal_cutoff_derivative(normal)
    return (
        -2.0 * a_derivative * c_value
        - 2.0 * x * a_value * c_derivative,
        a_value * c_derivative,
    )


def _slot_data(
    slots: FlowSlots,
) -> tuple[
    tuple[float, Point],
    tuple[float, Point],
    tuple[float, Point],
    tuple[float, Point],
]:
    points = (
        _point(slots.current, "current slot"),
        _point(slots.delay_4, "delay-4 slot"),
        _point(slots.delay_5, "delay-5 slot"),
        _point(slots.delay_theta, "delay-Theta slot"),
    )
    return tuple(
        (clocked_tail_weight(point), clocked_tail_weight_gradient(point))
        for point in points
    )  # type: ignore[return-value]


def clocked_tail_zero_amplitude_field(state: Sequence[float]) -> Point:
    """Return the explicit rho=0 graph fixed-point field."""

    x, y = _point(state)
    weight = clocked_tail_weight((x, y))
    tail = bounded_clock_tail((x, y))
    if weight == 0.0:
        return tail
    physical = (y - x * x, -x)
    return (
        tail[0] + weight * (physical[0] - tail[0]),
        tail[1] + weight * (physical[1] - tail[1]),
    )


def zero_amplitude_coordinate_rhs(state: Sequence[float]) -> Point:
    """Return (sigma_dot,d_dot) for the explicit zero-amplitude field."""

    sigma, normal = canard_coordinates(state)
    weight = clocked_tail_weight(state)
    speed = bounded_clock_profile(sigma)
    return (
        speed - 2.0 * weight * normal,
        sigma * weight * normal,
    )


def clocked_tail_slot_transform(
    slots: FlowSlots, *, rho: float, nu: float, eta: float
) -> Point:
    """Evaluate the bounded clock-positive slot-transform algebra."""

    rho_value = _finite(rho, "rho")
    x, y = _point(slots.current, "current slot")
    base = clocked_tail_zero_amplitude_field((x, y))
    forcing = clocked_tail_weak_delay_forcing(
        slots,
        rho=rho_value,
        nu=nu,
        eta=eta,
    )
    qx = base[0] + rho_value * forcing[0]
    qy = base[1] + rho_value * forcing[1]
    if not math.isfinite(qx) or not math.isfinite(qy):
        raise ValueError("clocked-tail transform overflows binary64")
    return qx, qy


def clocked_tail_weak_delay_forcing(
    slots: FlowSlots, *, rho: float, nu: float, eta: float
) -> Point:
    """Return F-hat in the exact factorization T_rho=B+rho*F-hat."""

    rho_value = _finite(rho, "rho")
    nu_value = _finite(nu, "nu")
    eta_value = _finite(eta, "eta")
    x, _ = _point(slots.current, "current slot")
    x4, _ = _point(slots.delay_4, "delay-4 slot")
    x5, _ = _point(slots.delay_5, "delay-5 slot")
    xtheta, _ = _point(slots.delay_theta, "delay-Theta slot")
    (w0, _), (w4, _), (w5, _), (wtheta, _) = _slot_data(slots)
    if w0 == 0.0:
        return 0.0, 0.0

    forcing_x = -w0 * x**3 / 3.0
    if w4 != 0.0 and w5 != 0.0:
        forcing_x += (
            w0 * w4 * w5 * ((x4 + x5) / 2.0 - x) / 5.0
        )
        forcing_x += (
            rho_value**2
            * w0
            * w4
            * w5
            * ((x4**3 + x5**3) / 2.0 - x**3)
            / 4.0
        )
    if wtheta != 0.0 and rho_value != 0.0 and eta_value != 0.0:
        forcing_x += (
            rho_value
            * eta_value
            * w0
            * wtheta
            * (x * x - xtheta * xtheta)
        )
    forcing_y = nu_value * w0
    if not math.isfinite(forcing_x) or not math.isfinite(forcing_y):
        raise ValueError("clocked-tail weak-delay forcing overflows binary64")
    return forcing_x, forcing_y


def clocked_tail_y(
    state: Sequence[float], *, rho: float, nu: float
) -> float:
    """Return the known Y component in the scalar fixed-point reduction."""

    x, y = _point(state)
    rho_value = _finite(rho, "rho")
    nu_value = _finite(nu, "nu")
    weight = clocked_tail_weight((x, y))
    tail_y = bounded_clock_tail((x, y))[1]
    result = tail_y + weight * (-x - tail_y) + rho_value * nu_value * weight
    if not math.isfinite(result):
        raise ValueError("clocked-tail Y component overflows binary64")
    return result


def clocked_delayed_slot_gradients(
    slots: FlowSlots, *, rho: float, eta: float
) -> tuple[Point, Point, Point]:
    """Return gradients of T_X with respect to the delayed slots."""

    rho_value = _finite(rho, "rho")
    eta_value = _finite(eta, "eta")
    x, _ = _point(slots.current, "current slot")
    x4, _ = _point(slots.delay_4, "delay-4 slot")
    x5, _ = _point(slots.delay_5, "delay-5 slot")
    xtheta, _ = _point(slots.delay_theta, "delay-Theta slot")
    (w0, _), (w4, dw4), (w5, dw5), (wtheta, dwtheta) = _slot_data(
        slots
    )
    if w0 == 0.0:
        return (0.0, 0.0), (0.0, 0.0), (0.0, 0.0)

    gradient_4 = (0.0, 0.0)
    gradient_5 = (0.0, 0.0)
    if rho_value != 0.0 and w4 != 0.0 and w5 != 0.0:
        linear_delay = (x4 + x5) / 2.0 - x
        cubic_delay = (x4**3 + x5**3) / 2.0 - x**3

        def shared_gradient(
            weight: float,
            weight_gradient: Point,
            other_weight: float,
            delayed_x: float,
        ) -> Point:
            linear_scale = rho_value * w0 * other_weight / 5.0
            cubic_scale = rho_value**3 * w0 * other_weight / 4.0
            return (
                linear_scale
                * (weight_gradient[0] * linear_delay + weight / 2.0)
                + cubic_scale
                * (
                    weight_gradient[0] * cubic_delay
                    + weight * 1.5 * delayed_x * delayed_x
                ),
                linear_scale * weight_gradient[1] * linear_delay
                + cubic_scale * weight_gradient[1] * cubic_delay,
            )

        gradient_4 = shared_gradient(w4, dw4, w5, x4)
        gradient_5 = shared_gradient(w5, dw5, w4, x5)
    gradient_theta = (0.0, 0.0)
    if wtheta != 0.0 and rho_value != 0.0 and eta_value != 0.0:
        eta_delay = x * x - xtheta * xtheta
        scale = rho_value**2 * eta_value * w0
        gradient_theta = (
            scale
            * (dwtheta[0] * eta_delay - 2.0 * wtheta * xtheta),
            scale * dwtheta[1] * eta_delay,
        )
    return gradient_4, gradient_5, gradient_theta


def singular_canard_state(phase: float) -> Point:
    """Return gamma_0(s)=(-s/2,s^2/4-1/2)."""

    phase_value = _finite(phase, "phase")
    return (
        -phase_value / 2.0,
        phase_value * phase_value / 4.0 - 0.5,
    )


def _declared_phase(phase: float) -> float:
    phase_value = _finite(phase, "phase")
    if not DECLARED_PHASE_LEFT <= phase_value <= DECLARED_PHASE_RIGHT:
        raise ValueError("phase must lie in the declared interval [-21,21]")
    return phase_value


def singular_canard_slots(phase: float, theta: float) -> FlowSlots:
    """Return exact zero-amplitude slots on the declared phase window."""

    phase_value = _declared_phase(phase)
    theta_value = _finite(theta, "Theta")
    if not float(THETA_LOWER) <= theta_value <= float(THETA_UPPER):
        raise ValueError("Theta must lie in the pinned directed interval")
    return FlowSlots(
        current=singular_canard_state(phase_value),
        delay_4=singular_canard_state(phase_value - 4.0),
        delay_5=singular_canard_state(phase_value - 5.0),
        delay_theta=singular_canard_state(phase_value - theta_value),
    )


def singular_core_first_rho_jet(phase: float, nu: float) -> Point:
    """Return the declared-window transform jet (s^3/24+9/20,nu)."""

    phase_value = _declared_phase(phase)
    nu_value = _finite(nu, "nu")
    return phase_value**3 / 24.0 + 9.0 / 20.0, nu_value


def volterra_iterate_factor(
    constant: float, interval_length: float, iteration: int
) -> float:
    """Return (C ell)^n/n! from the causal Volterra induction."""

    c_value = _finite(constant, "constant")
    length = _finite(interval_length, "interval_length")
    if c_value < 0.0 or length < 0.0:
        raise ValueError("constant and interval_length must be nonnegative")
    if type(iteration) is not int or iteration < 0:
        raise ValueError("iteration must be a nonnegative integer")
    try:
        result = (c_value * length) ** iteration / math.factorial(iteration)
    except OverflowError as error:
        raise ValueError("Volterra iterate factor overflows binary64") from error
    if not math.isfinite(result):
        raise ValueError("Volterra iterate factor is not finite")
    return result


def volterra_resolvent_factor(
    constant: float, interval_length: float
) -> float:
    """Return the Gronwall factor exp(C ell)."""

    c_value = _finite(constant, "constant")
    length = _finite(interval_length, "interval_length")
    if c_value < 0.0 or length < 0.0:
        raise ValueError("constant and interval_length must be nonnegative")
    try:
        result = math.exp(c_value * length)
    except OverflowError as error:
        raise ValueError("Volterra resolvent factor overflows binary64") from error
    if not math.isfinite(result):
        raise ValueError("Volterra resolvent factor is not finite")
    return result


def causal_volterra_constant(
    field_dependence_bound: float,
    clock_lower_bound: float,
    flow_lipschitz_bound: float,
    delays: Sequence[float],
    slot_lipschitz_bounds: Sequence[float],
) -> float:
    """Return B_F/kappa times sum A_i exp(L_F tau_i)."""

    field_bound = _finite(
        field_dependence_bound, "field_dependence_bound"
    )
    clock = _finite(clock_lower_bound, "clock_lower_bound")
    flow_bound = _finite(flow_lipschitz_bound, "flow_lipschitz_bound")
    if field_bound < 0.0 or flow_bound < 0.0:
        raise ValueError("field and flow bounds must be nonnegative")
    if clock <= 0.0:
        raise ValueError("clock_lower_bound must be positive")
    if len(delays) == 0 or len(delays) != len(slot_lipschitz_bounds):
        raise ValueError("delays and slot bounds must have equal nonzero length")
    total = 0.0
    for index, (delay, slot_bound) in enumerate(
        zip(delays, slot_lipschitz_bounds, strict=True)
    ):
        delay_value = _finite(delay, f"delays[{index}]")
        slot_value = _finite(slot_bound, f"slot_lipschitz_bounds[{index}]")
        if delay_value <= 0.0:
            raise ValueError("all Volterra delays must be strictly positive")
        if slot_value < 0.0:
            raise ValueError("slot Lipschitz bounds must be nonnegative")
        try:
            total += slot_value * math.exp(flow_bound * delay_value)
        except OverflowError as error:
            raise ValueError("Volterra constant overflows binary64") from error
    result = field_bound * total / clock
    if not math.isfinite(result):
        raise ValueError("Volterra constant is not finite")
    return result


def raw_target_sigma_speed_phase_three() -> float:
    """Return the exact-formula raw-slot sigma speed at rho=1/sqrt(5)."""

    return 1.0 - 567.0 / (160.0 * math.sqrt(5.0))


@dataclass(frozen=True)
class IntervalRecord:
    lower: str
    upper: str


def _record(value: DirectedInterval, digits: int = 100) -> IntervalRecord:
    lower, upper = value.decimal_bounds(digits)
    serialized = DirectedInterval.from_bounds(lower, upper, value.precision)
    if serialized.lower > value.lower or serialized.upper < value.upper:
        raise AssertionError("serialized interval does not contain MPFR interval")
    return IntervalRecord(lower=lower, upper=upper)


@dataclass(frozen=True)
class ClockedTailGraphCertificate:
    model_id: str
    audit_id: str
    precision_bits: int
    longitudinal_step_formula: str
    longitudinal_cutoff_formula: str
    normal_cutoff_contract: str
    bounded_clock_profile_formula: str
    raw_constant_clock_germ: str
    raw_constant_clock_germ_coordinate_rhs: tuple[str, str]
    left_exterior_end: int
    left_plateau_start: int
    right_plateau_end: int
    right_exterior_start: int
    normal_plateau_radius: int
    normal_support_radius: int
    tail_clock_radius: int
    tail_far_field_start_radius: int
    declared_phase_interval: tuple[int, int]
    delay_set: tuple[int | str, ...]
    theta_parent_endpoint_strings: tuple[str, str]
    theta_interval: IntervalRecord
    declared_single_slot_phase_hull: IntervalRecord
    left_plateau_margin_over_declared_slots: IntervalRecord
    tail_unit_clock_margin_after_left_delay: IntervalRecord
    right_plateau_closed_margin: int
    bounded_tail_component_bounds: tuple[str, str]
    physical_uncut_x_transform: str
    physical_uncut_y_transform: str
    clocked_tail_x_transform: str
    clocked_tail_y_transform: str
    active_slot_sets: tuple[str, str, str, str]
    bounded_clock_tail: str
    bounded_clock_tail_coordinate_rhs: tuple[str, str]
    bounded_clock_tail_far_speed: str
    bounded_clock_profile_global_infimum: str
    candidate_space: str
    fixed_exterior_germ_condition: str
    incoming_trace: tuple[str, str]
    incoming_self_map_identity: str
    zero_amplitude_fixed_point: tuple[str, str]
    zero_amplitude_coordinate_rhs: tuple[str, str]
    singular_core_first_rho_transform_jet: tuple[str, str]
    weak_delay_factorization: str
    fixed_cutoff_small_rho_graph_contract: str
    fixed_cutoff_small_rho_uniqueness_scope: str
    fixed_cutoff_small_rho_first_graph_jet: str
    seed_planar_preparation_rule: str
    seed_prepared_first_rho_jet: str
    seed_planar_preparation_scope: str
    volterra_prefix_inequality: str
    volterra_constant_formula: str
    volterra_iterate_bound: str
    volterra_resolvent_bound: str
    causal_component_restriction: str
    raw_target_phase_three_sigma_speed: IntervalRecord
    raw_target_phase_three_clock_warning: str
    longitudinal_cutoff_c_infinity: bool
    normal_cutoff_c_infinity: bool
    cutoff_between_zero_and_one: bool
    raw_constant_clock_germ_identity_proved: bool
    raw_constant_clock_germ_unboundedness_recorded: bool
    bounded_clock_profile_c_infinity: bool
    bounded_clock_profile_strictly_positive: bool
    bounded_clock_profile_has_no_global_positive_infimum: bool
    bounded_clock_tail_c_b_infinity: bool
    bounded_clock_tail_complete: bool
    bounded_clock_tail_preserves_normal_coordinate: bool
    bounded_clock_tail_unit_speed_on_cutoff_support: bool
    physical_operator_recovered_when_all_active_slots_are_in_plateau: bool
    termwise_active_slot_sets_exact: bool
    slow_unfolding_current_weighted: bool
    eta_zero_theta_slot_inactive: bool
    incoming_trace_parameter_independent: bool
    incoming_trace_self_map_identity_proved: bool
    incoming_positive_parameter_jets_zero: bool
    fixed_exterior_affine_subspace_self_map_proved: bool
    flat_left_interface_all_order_matching: bool
    bounded_complete_field_neighborhood_available: bool
    clocked_base_clock_positive_for_d_below_one_half: bool
    old_zero_exterior_clock_obstruction_removed_for_new_tail: bool
    rho_zero_fixed_point_explicit_and_unique: bool
    rho_zero_graph_frechet_derivative_zero: bool
    rho_zero_d_zero_orbit_complete: bool
    declared_window_canonical_phase_exact: bool
    declared_phase_slot_hull_inside_unit_plateau: bool
    singular_first_rho_transform_jet_realized_by_extension: bool
    weak_delay_factorization_c_b_infinity_proved: bool
    fixed_cutoff_small_rho_graph_exists: bool
    fixed_cutoff_small_rho_graph_unique_in_contraction_neighborhood: bool
    fixed_cutoff_small_rho_c3_rho_jets_proved: bool
    fixed_cutoff_small_rho_first_graph_jet_proved: bool
    seed_equation_21_graph_field_and_jet_realized: bool
    volterra_weissinger_uniqueness_theorem_proved_under_hypotheses: bool
    ordinary_global_contraction_not_required: bool
    order_zero_residual_inverse_on_range_bounded_conditionally: bool
    raw_singular_slot_target_clock_failure_proved: bool
    preparation_index_retained: bool
    old_537_global_nesting_argument_reused: bool
    target_positive_amplitude_graph_candidate_computed: bool
    target_candidate_self_map_validated: bool
    target_uniform_clock_bound_validated: bool
    target_j_barriers_validated: bool
    target_positive_amplitude_hull_validated: bool
    target_flow_lipschitz_bounds_validated: bool
    target_volterra_constant_validated: bool
    target_localized_causal_graph_theorem_validated: bool
    target_order_zero_fixed_point_validated: bool
    target_loss_scale_c3_parameter_jets_validated: bool
    target_planar_preparation_validated: bool
    target_trace_pair_fredholm_validated: bool
    fixed_epsilon_complete_history_root_validated: bool
    left_preparation_independence_proved: bool
    general_network_fixed_epsilon_lift_validated: bool
    biological_pulse_control_chain_validated: bool
    small_rho_global_uniqueness_outside_contraction_neighborhood_claimed: bool
    seed_prepared_trace_field_global_completeness_claimed: bool


PROVED_FLAGS = (
    "longitudinal_cutoff_c_infinity",
    "normal_cutoff_c_infinity",
    "cutoff_between_zero_and_one",
    "raw_constant_clock_germ_identity_proved",
    "raw_constant_clock_germ_unboundedness_recorded",
    "bounded_clock_profile_c_infinity",
    "bounded_clock_profile_strictly_positive",
    "bounded_clock_profile_has_no_global_positive_infimum",
    "bounded_clock_tail_c_b_infinity",
    "bounded_clock_tail_complete",
    "bounded_clock_tail_preserves_normal_coordinate",
    "bounded_clock_tail_unit_speed_on_cutoff_support",
    "physical_operator_recovered_when_all_active_slots_are_in_plateau",
    "termwise_active_slot_sets_exact",
    "slow_unfolding_current_weighted",
    "eta_zero_theta_slot_inactive",
    "incoming_trace_parameter_independent",
    "incoming_trace_self_map_identity_proved",
    "incoming_positive_parameter_jets_zero",
    "fixed_exterior_affine_subspace_self_map_proved",
    "flat_left_interface_all_order_matching",
    "bounded_complete_field_neighborhood_available",
    "clocked_base_clock_positive_for_d_below_one_half",
    "old_zero_exterior_clock_obstruction_removed_for_new_tail",
    "rho_zero_fixed_point_explicit_and_unique",
    "rho_zero_graph_frechet_derivative_zero",
    "rho_zero_d_zero_orbit_complete",
    "declared_window_canonical_phase_exact",
    "declared_phase_slot_hull_inside_unit_plateau",
    "singular_first_rho_transform_jet_realized_by_extension",
    "weak_delay_factorization_c_b_infinity_proved",
    "fixed_cutoff_small_rho_graph_exists",
    "fixed_cutoff_small_rho_graph_unique_in_contraction_neighborhood",
    "fixed_cutoff_small_rho_c3_rho_jets_proved",
    "fixed_cutoff_small_rho_first_graph_jet_proved",
    "seed_equation_21_graph_field_and_jet_realized",
    "volterra_weissinger_uniqueness_theorem_proved_under_hypotheses",
    "ordinary_global_contraction_not_required",
    "order_zero_residual_inverse_on_range_bounded_conditionally",
    "raw_singular_slot_target_clock_failure_proved",
    "preparation_index_retained",
)

OPEN_FLAGS = (
    "target_positive_amplitude_graph_candidate_computed",
    "target_candidate_self_map_validated",
    "target_uniform_clock_bound_validated",
    "target_j_barriers_validated",
    "target_positive_amplitude_hull_validated",
    "target_flow_lipschitz_bounds_validated",
    "target_volterra_constant_validated",
    "target_localized_causal_graph_theorem_validated",
    "target_order_zero_fixed_point_validated",
    "target_loss_scale_c3_parameter_jets_validated",
    "target_planar_preparation_validated",
    "target_trace_pair_fredholm_validated",
    "fixed_epsilon_complete_history_root_validated",
    "left_preparation_independence_proved",
    "general_network_fixed_epsilon_lift_validated",
    "biological_pulse_control_chain_validated",
)

REFUSED_FLAGS = (
    "old_537_global_nesting_argument_reused",
    "small_rho_global_uniqueness_outside_contraction_neighborhood_claimed",
    "seed_prepared_trace_field_global_completeness_claimed",
)


def build_reference_certificate(
    precision: int = PRECISION_BITS,
) -> ClockedTailGraphCertificate:
    """Build the directed structural certificate."""

    if type(precision) is not int or precision < 64:
        raise ValueError("precision must be an integer of at least 64 bits")
    theta = DirectedInterval.from_bounds(THETA_LOWER, THETA_UPPER, precision)
    phase_left = DirectedInterval.from_decimal(DECLARED_PHASE_LEFT, precision)
    phase_right = DirectedInterval.from_decimal(DECLARED_PHASE_RIGHT, precision)
    slot_left = phase_left - theta
    slot_hull = DirectedInterval(
        slot_left.lower,
        phase_right.upper,
        precision,
    )
    left_margin = slot_left - DirectedInterval.from_decimal(
        LEFT_PLATEAU_START, precision
    )
    tail_margin = (
        DirectedInterval.from_decimal(TAIL_CLOCK_RADIUS, precision)
        + DirectedInterval.from_decimal(LEFT_EXTERIOR_END, precision)
        - theta
    )
    one = DirectedInterval.from_decimal(1, precision)
    five = DirectedInterval.from_decimal(5, precision)
    raw_speed = one - (
        DirectedInterval.from_decimal(567, precision)
        / (
            DirectedInterval.from_decimal(160, precision)
            * five.sqrt()
        )
    )

    return ClockedTailGraphCertificate(
        model_id=MODEL_ID,
        audit_id=AUDIT_ID,
        precision_bits=precision,
        longitudinal_step_formula=(
            "S(z)=0[z<=0], exp(-1/z)/(exp(-1/z)+exp(-1/(1-z)))"
            "[0<z<1], 1[z>=1]"
        ),
        longitudinal_cutoff_formula="a(sigma)=S(sigma+30)S(22-sigma)",
        normal_cutoff_contract="c(d)=1 for |d|<=1, c(d)=0 for |d|>=2",
        bounded_clock_profile_formula=(
            "v_R=1[r<=1], c(r)+(1-c(r))/r[1<r<2], "
            "1/r[r>=2], r=|sigma|/64"
        ),
        raw_constant_clock_germ="Q_c=(-1/2,-X)",
        raw_constant_clock_germ_coordinate_rhs=(
            "sigma_dot=1",
            "d_dot=0",
        ),
        left_exterior_end=LEFT_EXTERIOR_END,
        left_plateau_start=LEFT_PLATEAU_START,
        right_plateau_end=RIGHT_PLATEAU_END,
        right_exterior_start=RIGHT_EXTERIOR_START,
        normal_plateau_radius=NORMAL_PLATEAU_RADIUS,
        normal_support_radius=NORMAL_SUPPORT_RADIUS,
        tail_clock_radius=TAIL_CLOCK_RADIUS,
        tail_far_field_start_radius=TAIL_FAR_FIELD_START_RADIUS,
        declared_phase_interval=(DECLARED_PHASE_LEFT, DECLARED_PHASE_RIGHT),
        delay_set=(4, 5, "Theta_*"),
        theta_parent_endpoint_strings=(THETA_LOWER, THETA_UPPER),
        theta_interval=_record(theta),
        declared_single_slot_phase_hull=_record(slot_hull),
        left_plateau_margin_over_declared_slots=_record(left_margin),
        tail_unit_clock_margin_after_left_delay=_record(tail_margin),
        right_plateau_closed_margin=0,
        bounded_tail_component_bounds=("1/2", "64"),
        physical_uncut_x_transform=(
            "Y-X^2+rho[-X^3/3+((X_4+X_5)/2-X)/5]"
            "+rho^2*eta[X^2-X_Theta^2]"
            "+rho^3[((X_4^3+X_5^3)/2-X^3)/4]"
        ),
        physical_uncut_y_transform="-X+rho*nu",
        clocked_tail_x_transform=(
            "-v0/2+w0*d-rho*w0*X^3/3"
            "+rho*w0*w4*w5*((X_4+X_5)/2-X)/5"
            "+rho^2*eta*w0*wTheta*(X^2-X_Theta^2)"
            "+rho^3*w0*w4*w5*((X_4^3+X_5^3)/2-X^3)/4"
        ),
        clocked_tail_y_transform="sigma*v0/2+rho*nu*w0",
        active_slot_sets=(
            "base/local/nu:{0}",
            "linear-delay:{0,4,5}",
            "cubic-delay:{0,4,5}",
            "eta:{0,Theta_*}",
        ),
        bounded_clock_tail="Q_v=(-v_R/2,sigma*v_R/2)",
        bounded_clock_tail_coordinate_rhs=("sigma_dot=v_R", "d_dot=0"),
        bounded_clock_tail_far_speed="v_R=64/|sigma| for |sigma|>=128",
        bounded_clock_profile_global_infimum="inf_R v_R=0",
        candidate_space=(
            "bounded uniformly-Lipschitz full vector fields Q with Q=Q_v "
            "on w=0; fixed points have the explicit known Y component"
        ),
        fixed_exterior_germ_condition=(
            "Q=Q_v on w=0; every delayed physical channel and rho*nu "
            "contains the current factor w0"
        ),
        incoming_trace=("-1/2", "-15"),
        incoming_self_map_identity=(
            "T(Q;rho,nu,eta)(Gamma(-30,d))=Q_v(Gamma(-30,d))"
        ),
        zero_amplitude_fixed_point=("-v_R/2+w(sigma,d)*d", "sigma*v_R/2"),
        zero_amplitude_coordinate_rhs=("v_R-2w*d", "sigma*w*d"),
        singular_core_first_rho_transform_jet=("s^3/24+9/20", "nu"),
        weak_delay_factorization=(
            "T_rho=B+rho*Fhat_rho with Fhat_rho in C_b^infinity; "
            "all candidate-flow dependence is at delays 4,5,Theta_*>0"
        ),
        fixed_cutoff_small_rho_graph_contract=(
            "for fixed Theta_* and bounded (nu,eta), there exists "
            "non-explicit rho_0>0 and a unique C_b^3 special-flow fixed "
            "graph in the declared O(|rho|) contraction neighborhood"
        ),
        fixed_cutoff_small_rho_uniqueness_scope=(
            "unique only in the theorem's contraction neighborhood, not "
            "among every bounded-Lipschitz fixed point"
        ),
        fixed_cutoff_small_rho_first_graph_jet=(
            "partial_rho Q_rho|_0=Fhat_0(E_B); on gamma_0(s), "
            "s in [-21,21], this is (s^3/24+9/20,nu)"
        ),
        seed_planar_preparation_rule=(
            "Q_rho^pr=q0+chi_plan*(Q_rho-B); the pinned C3 Seeley "
            "extension is an optional equivalent strip-only construction"
        ),
        seed_prepared_first_rho_jet=(
            "partial_rho Q_rho^pr(gamma_0(s))|_0="
            "chi_plan(s)*(s^3/24+9/20,nu)"
        ),
        seed_planar_preparation_scope=(
            "full-plane C3 compact perturbation of q0 for finite-window "
            "traces; not a special-flow fixed point and not claimed complete"
        ),
        volterra_prefix_inequality=(
            "E_s(Tq,Tp)<=C_V*integral_a^s E_xi(q,p)dxi"
        ),
        volterra_constant_formula=(
            "C_V=(B_F/kappa)*sum_i A_i*exp(L_F*tau_i)"
        ),
        volterra_iterate_bound=(
            "E_b(T^nq,T^np)<=(C_V*ell)^n/n!*E_b(q,p)"
        ),
        volterra_resolvent_bound="gain_on_range<=exp(C_V*ell)",
        causal_component_restriction=(
            "a one-branch target tube may use d_-<d<d_+<1/2; the global "
            "|d|<=1 cutoff plateau is not itself one causal Lambert component"
        ),
        raw_target_phase_three_sigma_speed=_record(raw_speed),
        raw_target_phase_three_clock_warning=(
            "raw singular slots at rho=1/sqrt(5), eta=0, s=3 give "
            "sigma_dot=1-567/(160*sqrt(5))<0; this is not a target "
            "fixed-point evaluation"
        ),
        longitudinal_cutoff_c_infinity=True,
        normal_cutoff_c_infinity=True,
        cutoff_between_zero_and_one=True,
        raw_constant_clock_germ_identity_proved=True,
        raw_constant_clock_germ_unboundedness_recorded=True,
        bounded_clock_profile_c_infinity=True,
        bounded_clock_profile_strictly_positive=True,
        bounded_clock_profile_has_no_global_positive_infimum=True,
        bounded_clock_tail_c_b_infinity=True,
        bounded_clock_tail_complete=True,
        bounded_clock_tail_preserves_normal_coordinate=True,
        bounded_clock_tail_unit_speed_on_cutoff_support=True,
        physical_operator_recovered_when_all_active_slots_are_in_plateau=True,
        termwise_active_slot_sets_exact=True,
        slow_unfolding_current_weighted=True,
        eta_zero_theta_slot_inactive=True,
        incoming_trace_parameter_independent=True,
        incoming_trace_self_map_identity_proved=True,
        incoming_positive_parameter_jets_zero=True,
        fixed_exterior_affine_subspace_self_map_proved=True,
        flat_left_interface_all_order_matching=True,
        bounded_complete_field_neighborhood_available=True,
        clocked_base_clock_positive_for_d_below_one_half=True,
        old_zero_exterior_clock_obstruction_removed_for_new_tail=True,
        rho_zero_fixed_point_explicit_and_unique=True,
        rho_zero_graph_frechet_derivative_zero=True,
        rho_zero_d_zero_orbit_complete=True,
        declared_window_canonical_phase_exact=True,
        declared_phase_slot_hull_inside_unit_plateau=(
            left_margin.lower > 0
        ),
        singular_first_rho_transform_jet_realized_by_extension=True,
        weak_delay_factorization_c_b_infinity_proved=True,
        fixed_cutoff_small_rho_graph_exists=True,
        fixed_cutoff_small_rho_graph_unique_in_contraction_neighborhood=True,
        fixed_cutoff_small_rho_c3_rho_jets_proved=True,
        fixed_cutoff_small_rho_first_graph_jet_proved=True,
        seed_equation_21_graph_field_and_jet_realized=True,
        volterra_weissinger_uniqueness_theorem_proved_under_hypotheses=True,
        ordinary_global_contraction_not_required=True,
        order_zero_residual_inverse_on_range_bounded_conditionally=True,
        raw_singular_slot_target_clock_failure_proved=(raw_speed.upper < 0),
        preparation_index_retained=True,
        old_537_global_nesting_argument_reused=False,
        target_positive_amplitude_graph_candidate_computed=False,
        target_candidate_self_map_validated=False,
        target_uniform_clock_bound_validated=False,
        target_j_barriers_validated=False,
        target_positive_amplitude_hull_validated=False,
        target_flow_lipschitz_bounds_validated=False,
        target_volterra_constant_validated=False,
        target_localized_causal_graph_theorem_validated=False,
        target_order_zero_fixed_point_validated=False,
        target_loss_scale_c3_parameter_jets_validated=False,
        target_planar_preparation_validated=False,
        target_trace_pair_fredholm_validated=False,
        fixed_epsilon_complete_history_root_validated=False,
        left_preparation_independence_proved=False,
        general_network_fixed_epsilon_lift_validated=False,
        biological_pulse_control_chain_validated=False,
        small_rho_global_uniqueness_outside_contraction_neighborhood_claimed=(
            False
        ),
        seed_prepared_trace_field_global_completeness_claimed=False,
    )


def json_ready_clocked_tail_graph_audit() -> dict[str, Any]:
    """Return the canonical JSON-ready audit object."""

    return json.loads(json.dumps({"certificate": asdict(build_reference_certificate())}))


def validate_clocked_tail_graph_audit(payload: Mapping[str, Any]) -> None:
    """Reject formula, scalar-type, or claim-status tampering."""

    if not isinstance(payload, Mapping):
        raise ValueError("audit payload must be a mapping")
    certificate = payload.get("certificate")
    if not isinstance(certificate, Mapping):
        raise ValueError("certificate must be a mapping")
    if type(certificate.get("precision_bits")) is not int:
        raise ValueError("precision_bits must be an integer")
    integer_keys = (
        "left_exterior_end",
        "left_plateau_start",
        "right_plateau_end",
        "right_exterior_start",
        "normal_plateau_radius",
        "normal_support_radius",
        "tail_clock_radius",
        "tail_far_field_start_radius",
        "right_plateau_closed_margin",
    )
    if any(type(certificate.get(key)) is not int for key in integer_keys):
        raise ValueError("a geometric endpoint is not an integer")
    phase = certificate.get("declared_phase_interval")
    if (
        not isinstance(phase, list)
        or len(phase) != 2
        or any(type(value) is not int for value in phase)
    ):
        raise ValueError("declared phase endpoints must be integers")
    delays = certificate.get("delay_set")
    if (
        not isinstance(delays, list)
        or len(delays) != 3
        or delays[:2] != [4, 5]
        or type(delays[0]) is not int
        or type(delays[1]) is not int
        or not isinstance(delays[2], str)
    ):
        raise ValueError("delay_set has invalid values or scalar types")
    if any(certificate.get(name) is not True for name in PROVED_FLAGS):
        raise ValueError("a proved clocked-tail flag was weakened")
    if any(certificate.get(name) is not False for name in OPEN_FLAGS):
        raise ValueError("an open target graph/root gate was promoted")
    if any(certificate.get(name) is not False for name in REFUSED_FLAGS):
        raise ValueError("a refused inherited argument was promoted")
    boolean_fields = {
        field.name
        for field in fields(ClockedTailGraphCertificate)
        if field.type in (bool, "bool")
    }
    if boolean_fields != set(PROVED_FLAGS) | set(OPEN_FLAGS) | set(REFUSED_FLAGS):
        raise AssertionError("boolean claim ledger does not cover the schema")
    if dict(payload) != json_ready_clocked_tail_graph_audit():
        raise ValueError("clocked-tail graph audit differs from reference")


def _sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _read_json_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def _verify_seed_upstream_evidence(
    repository: Path,
    seed_manifest: Mapping[str, Any],
) -> tuple[dict[str, str], dict[str, bool]]:
    """Replay the seed generator's own parent hashes and semantic checks."""

    paths = {
        "green_phase_selected_traces_doc": repository
        / "docs/green-phase-selected-traces.md",
        "fhn_bloch_outer_validation_result": repository
        / "experiments/results/fhn_bloch_outer_validation.json",
        "fixed_epsilon_sliding_window_w1p_bridge_result": repository
        / "experiments/results/fixed_epsilon_sliding_window_w1p_bridge.json",
        "quadratic_period_locked_root_doc": repository
        / "docs/quadratic-period-locked-selected-root.md",
    }
    expected = {
        "green_phase_selected_traces_doc": SEED_GREEN_PHASE_DOC_SHA256,
        "fhn_bloch_outer_validation_result": SEED_BLOCH_RESULT_SHA256,
        "fixed_epsilon_sliding_window_w1p_bridge_result": (
            SEED_BRIDGE_RESULT_SHA256
        ),
        "quadratic_period_locked_root_doc": SEED_QUADRATIC_DOC_SHA256,
    }
    actual = {name: _sha256(path) for name, path in paths.items()}
    declared_hashes = seed_manifest.get("parent_sha256")
    if (
        not isinstance(declared_hashes, Mapping)
        or dict(declared_hashes) != expected
        or actual != expected
    ):
        raise ValueError("seed parent recursive hashes changed")

    green = paths["green_phase_selected_traces_doc"].read_text(
        encoding="utf-8"
    )
    bloch = _read_json_object(paths["fhn_bloch_outer_validation_result"])
    bridge = _read_json_object(
        paths["fixed_epsilon_sliding_window_w1p_bridge_result"]
    )
    quadratic = paths["quadratic_period_locked_root_doc"].read_text(
        encoding="utf-8"
    )
    local_transfer = bloch.get("local_transfer")
    bridge_audit = bridge.get("audit")
    if not isinstance(local_transfer, Mapping) or not isinstance(
        bridge_audit, Mapping
    ):
        raise ValueError("seed upstream result schema changed")
    bridge_certificate = bridge_audit.get("certificate")
    if not isinstance(bridge_certificate, Mapping):
        raise ValueError("seed bridge certificate is missing")
    checks = {
        "green_parent_freezes_preparation_before_differentiation": (
            "After \\(p\\) is chosen, fix one preparation datum" in green
            and "no derivative of `S` is taken" in green
        ),
        "green_parent_uses_two_distinct_cutoffs": (
            "two different frozen cutoffs" in green
            and "must not be conflated" in green
        ),
        "period_interval_matches_pinned_parent": (
            local_transfer.get("minimum_period_lower") == SEED_PERIOD_LOWER
            and local_transfer.get("maximum_period_upper")
            == SEED_PERIOD_UPPER
        ),
        "parent_full_fixed_window_row_remains_open": (
            bridge_certificate.get("fixed_window_gap_row_validated") is False
            and bridge_certificate.get("frozen_target_graph_family_validated")
            is False
            and bridge_certificate.get(
                "prepared_planar_trace_family_validated"
            )
            is False
        ),
        "quadratic_carrier_first_jet_is_directly_pinned": (
            "\\frac{s^3}{24}+\\frac94\\kappa_1" in quadratic
            and "(\\kappa_1,\\kappa_3,\\eta)=(1/5,1/4,0)" in quadratic
        ),
    }
    declared_checks = seed_manifest.get("parent_claim_checks")
    if (
        not isinstance(declared_checks, Mapping)
        or dict(declared_checks) != checks
        or any(value is not True for value in checks.values())
    ):
        raise ValueError("seed parent recursive claim checks changed")
    return actual, checks


def verify_clocked_tail_parent_evidence(
    repository: Path,
) -> tuple[dict[str, str], dict[str, bool]]:
    """Replay parent hashes, validators, and semantic seams."""

    paths = {
        "fixed_epsilon_frozen_graph_operator_result": repository
        / "experiments/results/fixed_epsilon_frozen_graph_operator.json",
        "fixed_epsilon_singular_reachable_hull_result": repository
        / "experiments/results/fixed_epsilon_singular_reachable_hull.json",
        "fixed_window_prepared_gap_seed_result": repository
        / "experiments/results/fixed_window_prepared_gap_seed.json",
        "special_flow_graph_theorem_doc": repository
        / "docs/special-flow-graph-theorem.md",
        "mixed_jet_graph_theorem_doc": repository
        / "docs/mixed-jet-graph-proof.md",
    }
    actual = {name: _sha256(path) for name, path in paths.items()}
    if actual != PARENT_SHA256:
        changed = [
            name for name in PARENT_SHA256 if actual[name] != PARENT_SHA256[name]
        ]
        raise ValueError(f"pinned parent hashes changed: {changed}")

    frozen_payload = _read_json_object(
        paths["fixed_epsilon_frozen_graph_operator_result"]
    )
    singular_payload = _read_json_object(
        paths["fixed_epsilon_singular_reachable_hull_result"]
    )
    seed_payload = _read_json_object(
        paths["fixed_window_prepared_gap_seed_result"]
    )
    validate_frozen_graph_operator_result(frozen_payload, repository)
    validate_singular_reachable_hull_result(singular_payload, repository)
    validate_fixed_window_gap_seed_payload(seed_payload["audit"])

    frozen = frozen_payload["audit"]["certificate"]
    singular = singular_payload["audit"]["certificate"]
    seed = seed_payload["audit"]["certificate"]
    seed_manifest = seed_payload.get("manifest")
    if not isinstance(seed_manifest, Mapping):
        raise ValueError("seed parent manifest is missing")
    seed_artifacts = {
        "generator": repository
        / "experiments/fixed_window_prepared_gap_seed.py",
        "proof_source": repository
        / "src/canard_control/fixed_window_prepared_gap_seed.py",
        "note": repository / "docs/fixed-window-prepared-gap-seed.md",
    }
    expected_seed_relative_paths = {
        "generator": "experiments/fixed_window_prepared_gap_seed.py",
        "proof_source": "src/canard_control/fixed_window_prepared_gap_seed.py",
        "note": "docs/fixed-window-prepared-gap-seed.md",
    }
    if any(
        seed_manifest.get(name) != relative
        for name, relative in expected_seed_relative_paths.items()
    ):
        raise ValueError("seed parent artifact paths changed")
    seed_self_hashes_match = all(
        seed_manifest.get(f"{name}_sha256") == _sha256(path)
        for name, path in seed_artifacts.items()
    )
    if not seed_self_hashes_match:
        raise ValueError("seed parent self hashes changed")
    seed_upstream_hashes, seed_upstream_checks = (
        _verify_seed_upstream_evidence(repository, seed_manifest)
    )
    seed_note = seed_artifacts["note"].read_text(encoding="utf-8")
    special_flow = paths["special_flow_graph_theorem_doc"].read_text(
        encoding="utf-8"
    )
    mixed_jet = paths["mixed_jet_graph_theorem_doc"].read_text(
        encoding="utf-8"
    )
    checks = {
        "frozen_parent_has_zero_exterior_and_open_graph_solve": (
            frozen.get("graph_base_extension_formula") == "q0,S=chi_graph*q0"
            and frozen.get("synchronous_known_y_component_global_extension")
            == "Q_Y=chi_graph(u)*(-X)+rho*nu"
            and frozen.get("graph_fixed_point_candidate_computed") is False
            and frozen.get("graph_fixed_point_inverse_interval_validated")
            is False
        ),
        "singular_parent_proves_zero_exterior_clock_failure_and_causal_lemma": (
            singular.get("frozen_zero_exterior_clock_condition_fails") is True
            and singular.get("causal_slab_restriction_lemma_proved") is True
            and singular.get("target_uniform_clock_bound_validated") is False
        ),
        "seed_parent_declares_same_first_jet_but_leaves_realization_open": (
            seed.get("declared_core_first_jet") == "(s^3/24+9/20, nu)"
            and seed.get("explicit_longitudinal_first_jet_frozen") is True
            and seed.get("cutoff_plateau_end") == 20
            and seed.get("cutoff_support_end") == 21
            and type(seed.get("cutoff_plateau_end")) is int
            and type(seed.get("cutoff_support_end")) is int
            and seed.get("prepared_tail_first_jet") == "(0,0)"
            and seed.get("first_jet_realised_by_same_graph_preparation") is False
        ),
        "theta_endpoints_replayed_exactly": (
            frozen.get("theta_interval", {}).get("lower") == THETA_LOWER
            and frozen.get("theta_interval", {}).get("upper") == THETA_UPPER
            and singular.get("theta_parent_endpoint_strings")
            == [THETA_LOWER, THETA_UPPER]
        ),
        "special_flow_parent_requires_bounded_smooth_fields": (
            "q_0,F,G\\in C_b^R" in special_flow
            and "Q_{\\delta,p}\\in C_b^s" in special_flow
            and "generates a complete two-sided flow" in special_flow
        ),
        "mixed_jet_parent_proves_fixed_cutoff_c3_graph_family": (
            "Theorem 1 (finite-scale mixed-jet graph)" in mixed_jet
            and "unique fixed point in the contraction neighborhood"
            in mixed_jet
            and "C_u^3C_{\\delta,\\eta}^{3,2}" in mixed_jet
            and "C_b^R" in mixed_jet
        ),
        "frozen_parent_provides_conditional_seeley_preparation_rule": (
            frozen.get("conditional_full_plane_c3_preparation_rule_constructed")
            is True
            and frozen.get("seeley_c3_matching_identities_validated") is True
            and frozen.get("graph_and_planar_cutoffs_distinct") is True
            and frozen.get("planar_cutoff_id")
            == "chi_plan_c3_septic_20_21"
        ),
        "seed_parent_self_hashes_and_condition_21_pinned": (
            seed_self_hashes_match
            and "## 5. Exact promotion condition" in seed_note
            and "Q^{\\rm pr}_{0,S,\\mathcal P}=q_0" in seed_note
            and "f_\\chi(s;\\nu)" in seed_note
            and "Equation (21) has\nnot yet been proved" in seed_note
        ),
        "seed_parent_recursive_upstream_evidence_replayed": (
            dict(seed_manifest["parent_sha256"]) == seed_upstream_hashes
            and dict(seed_manifest["parent_claim_checks"])
            == seed_upstream_checks
            and all(value is True for value in seed_upstream_checks.values())
        ),
    }
    if set(checks) != PARENT_CLAIM_CHECK_KEYS:
        raise AssertionError("parent claim-check implementation drifted")
    if any(value is not True for value in checks.values()):
        failed = [name for name, value in checks.items() if value is not True]
        raise ValueError(f"pinned parent claim checks failed: {failed}")
    return actual, checks


def validate_clocked_tail_graph_result(
    payload: Mapping[str, Any], repository: Path
) -> None:
    """Validate the audit, runtime metadata, and complete hash chain."""

    if not isinstance(payload, Mapping):
        raise ValueError("result payload must be a mapping")
    if set(payload) != {"audit", "manifest"}:
        raise ValueError("result must contain exactly audit and manifest")
    audit = payload.get("audit")
    manifest = payload.get("manifest")
    if not isinstance(audit, Mapping) or not isinstance(manifest, Mapping):
        raise ValueError("audit and manifest must be mappings")
    validate_clocked_tail_graph_audit(audit)

    required_manifest_keys = {
        "generator",
        "generator_sha256",
        "proof_source",
        "proof_source_sha256",
        "note",
        "note_sha256",
        "parent_sha256",
        "parent_claim_checks",
        "default_command",
        "python",
        "platform",
        "arithmetic",
    }
    if set(manifest) != required_manifest_keys:
        raise ValueError("result manifest has missing or unknown keys")
    expected_paths = {
        "generator": GENERATOR_RELATIVE_PATH,
        "proof_source": PROOF_SOURCE_RELATIVE_PATH,
        "note": NOTE_RELATIVE_PATH,
        "default_command": DEFAULT_COMMAND,
    }
    if any(manifest.get(key) != value for key, value in expected_paths.items()):
        raise ValueError("result manifest path or command changed")
    own_hashes = {
        "generator_sha256": _sha256(repository / GENERATOR_RELATIVE_PATH),
        "proof_source_sha256": _sha256(repository / PROOF_SOURCE_RELATIVE_PATH),
        "note_sha256": _sha256(repository / NOTE_RELATIVE_PATH),
    }
    if any(manifest.get(key) != value for key, value in own_hashes.items()):
        raise ValueError("result manifest self hash changed")
    replayed_hashes, replayed_checks = verify_clocked_tail_parent_evidence(
        repository
    )
    parent_hashes = manifest.get("parent_sha256")
    if (
        not isinstance(parent_hashes, Mapping)
        or dict(parent_hashes) != PARENT_SHA256
        or dict(parent_hashes) != replayed_hashes
    ):
        raise ValueError("result parent hash ledger changed")
    checks = manifest.get("parent_claim_checks")
    if not isinstance(checks, Mapping) or set(checks) != PARENT_CLAIM_CHECK_KEYS:
        raise ValueError("parent claim checks are missing or unknown")
    if (
        any(value is not True for value in checks.values())
        or dict(checks) != replayed_checks
    ):
        raise ValueError("a parent claim check is not strictly true")
    expected_runtime = {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "arithmetic": MANIFEST_ARITHMETIC,
    }
    if any(manifest.get(key) != value for key, value in expected_runtime.items()):
        raise ValueError("result manifest runtime or arithmetic changed")
