"""Executable contract for the frozen synchronous history-graph operator.

This module fixes the *operator that remains to be solved* at the target
``delta=1/sqrt(5)``.  It does not return a graph candidate and it does not
validate a contraction or an inverse.  The distinction is important: on the
synchronous quotient the stable network graph vanishes, but the delayed
planar flow still depends on an unknown scalar field ``q=Q_X``.

Two extensions are kept separate.

``chi_graph``
    A C-infinity anisotropic cutoff used to make the nonlocal graph transform
    a global complete-field problem.  The explicit extension below is one
    admissible frozen datum.  Its adequacy at the target amplitude is not
    certified by merely writing it down.

``chi_plan``
    The C3 longitudinal cutoff from the finite-window Green seed.  Together
    with a finite Seeley reflection it conditionally turns a computed C3
    graph field into a full-plane prepared trace field which equals ``q0``
    near the canonical tails.  It is never used in the graph transform.

The exact physical slot algebra, the cutoff extension, the delayed-flow
variation equation, and the Seeley matching identities are executable.  The
claim ledger deliberately leaves the fixed point, positive-amplitude hull,
prepared traces, complete-history root, network lift, and biological control
chain open.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from fractions import Fraction
from hashlib import sha256
import json
import math
from pathlib import Path
import platform
from typing import Any, Callable, Mapping, Protocol, Sequence

from canard_control.directed_interval import (
    DirectedInterval,
    decimal_lower,
    decimal_upper,
)
from canard_control.fixed_window_prepared_gap_seed import septic_cutoff


MODEL_ID = "quadratic-period-lock-fixed-epsilon-frozen-synchronous-graph"
AUDIT_ID = "fixed-epsilon-frozen-graph-operator-v1"
PRECISION_BITS = 512

EPSILON = "1/5"
TARGET_AMPLITUDE = "1/sqrt(5)"
DELAY_FOUR = 4.0
DELAY_FIVE = 5.0
THETA_LOWER = (
    "7.3970862959520600605496654174898409301164678211784933042579909565"
)
THETA_UPPER = (
    "7.3970863004241960155492448103081882675790202920942079556261116625"
)

# The fixed-window reference uses S=4 and B=18.  Its wider graph target is
# therefore 22.  This is a computational target, not a claim that S=4 equals
# the non-explicit logarithmic radius in the small-amplitude theorem.
RETAINED_HALF_WINDOW = 4
PREPARATION_BUFFER = 18
WIDE_GRAPH_TARGET = RETAINED_HALF_WINDOW + PREPARATION_BUFFER

# The theorem-native rectangular jet family is blocked by
# (total grade, parameter grade).  There are 4*7=28 such blocks.
STATE_JET_MAX = 3
AMPLITUDE_JET_MAX = 3
NU_JET_MAX = 1
ETA_JET_MAX = 2

# Freeze an explicit conservative graph cutoff.  Section 2 of the growing
# tube proof only asks for a fixed d_*>0; d_*=1 is a legitimate datum.  The
# positive-amplitude reachable hull has *not* yet been proved to lie inside
# it.  The longitudinal value 537 is the first integer above the entire
# directed theorem-native nesting requirement computed below.
GRAPH_NORMAL_PLATEAU_RADIUS = 1.0
GRAPH_NORMAL_SUPPORT_RADIUS = 2.0
GRAPH_LONGITUDINAL_PLATEAU_RADIUS = 537.0
GRAPH_LONGITUDINAL_SUPPORT_RADIUS = 1074.0

# The prepared trace extension uses only the graph field on |d|<=1.  Width
# 1/2 is the largest value for which every reflected sample with b_k<=4
# remains in that strip.
PLANAR_NORMAL_CORE_RADIUS = 1.0
PLANAR_NORMAL_EXTENSION_WIDTH = 0.5
PLANAR_LONGITUDINAL_PLATEAU_RADIUS = 20
PLANAR_LONGITUDINAL_SUPPORT_RADIUS = 21

SEELEY_NODES = (1, 2, 3, 4)
SEELEY_WEIGHTS = (
    Fraction(10),
    Fraction(-20),
    Fraction(15),
    Fraction(-4),
)

GROWING_TUBE_GRAPH_DOC_SHA256 = (
    "d9f16108a9e3680a38db9a9cdf7ea0092e879673195c69c95d4677b4cffb021a"
)
SPECIAL_FLOW_GRAPH_DOC_SHA256 = (
    "9c7d7073ef9b3d01bd69e9c559445be470c74622c993cf8051c7c0b21904657d"
)
GREEN_PHASE_DOC_SHA256 = (
    "543ae331d0ffc656bba3a667dab1301fed29f9796afe8a84c4390fcff4088dc8"
)
QUADRATIC_PERIOD_LOCKED_ROOT_DOC_SHA256 = (
    "f08632721279f6bfc00d0aa4d118a9a7c5bda2b489f5457003e9914c540b87e3"
)
SLIDING_WINDOW_BRIDGE_RESULT_SHA256 = (
    "4afc81cc6472f1c24fe938147623d0042f27d3ab4f30d3f5f052e924b60c3b05"
)
FIXED_WINDOW_GAP_SEED_RESULT_SHA256 = (
    "41d325ca4c06b2e1b8a6ffa4e3908737c7be3d34a937a8a852ef7d1195321f39"
)

PROOF_SOURCE_RELATIVE_PATH = (
    "src/canard_control/fixed_epsilon_frozen_graph_operator.py"
)
GENERATOR_RELATIVE_PATH = (
    "experiments/fixed_epsilon_frozen_graph_operator.py"
)
RESULT_RELATIVE_PATH = (
    "experiments/results/fixed_epsilon_frozen_graph_operator.json"
)
NOTE_RELATIVE_PATH = "docs/fixed-epsilon-frozen-graph-operator.md"
DEFAULT_COMMAND = (
    "PYTHONPATH=src /usr/bin/python3 "
    "experiments/fixed_epsilon_frozen_graph_operator.py"
)
MANIFEST_ARITHMETIC = (
    "exact rational operator/Seeley/block algebra and 512-bit MPFR-directed "
    "nesting arithmetic; no graph solve, interval flow integration, trace "
    "solve, or root continuation"
)

PARENT_SHA256 = {
    "growing_tube_graph_doc": GROWING_TUBE_GRAPH_DOC_SHA256,
    "special_flow_graph_doc": SPECIAL_FLOW_GRAPH_DOC_SHA256,
    "green_phase_selected_traces_doc": GREEN_PHASE_DOC_SHA256,
    "quadratic_period_locked_root_doc": (
        QUADRATIC_PERIOD_LOCKED_ROOT_DOC_SHA256
    ),
    "fixed_epsilon_sliding_window_w1p_bridge_result": (
        SLIDING_WINDOW_BRIDGE_RESULT_SHA256
    ),
    "fixed_window_prepared_gap_seed_result": (
        FIXED_WINDOW_GAP_SEED_RESULT_SHA256
    ),
}

PARENT_CLAIM_CHECK_KEYS = {
    "growing_parent_freezes_target_cutoff_and_requires_flow_hull",
    "special_flow_parent_uses_backward_complete_flow_embedding",
    "green_parent_separates_graph_and_planar_cutoffs",
    "quadratic_parent_has_exact_0_4_5_theta_slot_model",
    "bridge_parent_leaves_target_graph_trace_and_root_open",
    "seed_parent_proves_only_singular_not_positive_hull",
}


Point = tuple[float, float]
Matrix2 = tuple[tuple[float, float], tuple[float, float]]
VectorField = Callable[[Point], Point]
ScalarField = Callable[[Point], float]


class BackwardFlow(Protocol):
    """Protocol for a backward-flow evaluator.

    The implementation must return ``Phi_Q^{-tau}(u)``.  No numerical
    implementation is certified in this module.
    """

    def __call__(
        self, field: VectorField, state: Point, delay: float
    ) -> Point: ...


def _point(value: Sequence[float], name: str = "point") -> Point:
    if len(value) != 2:
        raise ValueError(f"{name} must have two coordinates")
    x, y = float(value[0]), float(value[1])
    if not math.isfinite(x) or not math.isfinite(y):
        raise ValueError(f"{name} coordinates must be finite")
    return x, y


def _finite(value: float, name: str) -> float:
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result


def canard_coordinates(state: Sequence[float]) -> Point:
    """Return ``(sigma,d)=(-2X,Y-X^2+1/2)`` for alpha=1."""

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


def singular_field(state: Sequence[float]) -> Point:
    """The uncut fold field ``q0=(Y-X^2,-X)``."""

    x, y = _point(state)
    qx = y - x * x
    if not math.isfinite(qx):
        raise ValueError("singular field overflows binary64")
    return qx, -x


def flat_cutoff_ratio(ratio: float) -> float:
    """A C-infinity cutoff equal to one on ``r<=1`` and zero on ``r>=2``."""

    value = _finite(ratio, "cutoff ratio")
    if value < 0:
        raise ValueError("cutoff ratio must be nonnegative")
    if value <= 1.0:
        return 1.0
    if value >= 2.0:
        return 0.0
    left = math.exp(-1.0 / (value - 1.0))
    right = math.exp(-1.0 / (2.0 - value))
    return right / (left + right)


def flat_cutoff_ratio_derivative(ratio: float) -> float:
    """Derivative of :func:`flat_cutoff_ratio` with respect to its ratio."""

    value = _finite(ratio, "cutoff ratio")
    if value < 0:
        raise ValueError("cutoff ratio must be nonnegative")
    if value <= 1.0 or value >= 2.0:
        return 0.0
    cutoff = flat_cutoff_ratio(value)
    logarithmic_difference = -1.0 / (2.0 - value) ** 2 - 1.0 / (
        value - 1.0
    ) ** 2
    return cutoff * (1.0 - cutoff) * logarithmic_difference


def anisotropic_graph_cutoff(state: Sequence[float]) -> float:
    """Evaluate the explicit frozen ``chi_graph`` in canard coordinates."""

    x, y = _point(state)
    # If |X|>=support_sigma/2, the longitudinal factor is already zero.
    # Exit before forming X^2 so every finite binary64 point in this exterior
    # is handled without overflow.
    if abs(x) >= GRAPH_LONGITUDINAL_SUPPORT_RADIUS / 2.0:
        return 0.0
    sigma = -2.0 * x
    normal = y - x * x + 0.5
    return flat_cutoff_ratio(
        abs(sigma) / GRAPH_LONGITUDINAL_PLATEAU_RADIUS
    ) * flat_cutoff_ratio(abs(normal) / GRAPH_NORMAL_PLATEAU_RADIUS)


def anisotropic_graph_cutoff_gradient(state: Sequence[float]) -> Point:
    """Return the Cartesian gradient of the frozen graph cutoff."""

    x, y = _point(state)
    if abs(x) >= GRAPH_LONGITUDINAL_SUPPORT_RADIUS / 2.0:
        return 0.0, 0.0
    sigma = -2.0 * x
    normal = y - x * x + 0.5
    sigma_ratio = abs(sigma) / GRAPH_LONGITUDINAL_PLATEAU_RADIUS
    normal_ratio = abs(normal) / GRAPH_NORMAL_PLATEAU_RADIUS
    chi_sigma = flat_cutoff_ratio(sigma_ratio)
    chi_normal = flat_cutoff_ratio(normal_ratio)
    dchi_sigma = flat_cutoff_ratio_derivative(sigma_ratio)
    dchi_normal = flat_cutoff_ratio_derivative(normal_ratio)

    sigma_sign = 0.0 if sigma == 0.0 else math.copysign(1.0, sigma)
    normal_sign = 0.0 if normal == 0.0 else math.copysign(1.0, normal)
    sigma_factor = (
        dchi_sigma
        * sigma_sign
        / GRAPH_LONGITUDINAL_PLATEAU_RADIUS
    )
    normal_factor = (
        dchi_normal * normal_sign / GRAPH_NORMAL_PLATEAU_RADIUS
    )
    # grad sigma=(-2,0), grad d=(-2X,1).
    return (
        chi_normal * sigma_factor * -2.0
        + chi_sigma * normal_factor * (-2.0 * x),
        chi_sigma * normal_factor,
    )


@dataclass(frozen=True)
class FlowSlots:
    """Current state and the three exact backward-flow slots."""

    current: Point
    delay_4: Point
    delay_5: Point
    delay_theta: Point


def uncut_physical_transform(
    slots: FlowSlots, *, rho: float, nu: float, eta: float
) -> Point:
    """Evaluate the exact physical synchronous graph-map slot algebra."""

    rho_value = _finite(rho, "rho")
    nu_value = _finite(nu, "nu")
    eta_value = _finite(eta, "eta")
    x, y = _point(slots.current, "current slot")
    x4, _ = _point(slots.delay_4, "delay-4 slot")
    x5, _ = _point(slots.delay_5, "delay-5 slot")
    xtheta, _ = _point(slots.delay_theta, "delay-Theta slot")
    qx = (
        y
        - x * x
        + rho_value
        * (
            -(x**3) / 3.0
            + ((x4 + x5) / 2.0 - x) / 5.0
        )
        + rho_value**2 * eta_value * (x * x - xtheta * xtheta)
        + rho_value**3
        / 4.0
        * ((x4**3 + x5**3) / 2.0 - x**3)
    )
    return qx, -x + rho_value * nu_value


def _cutoff_term_data(slots: FlowSlots) -> tuple[
    tuple[float, Point],
    tuple[float, Point],
    tuple[float, Point],
    tuple[float, Point],
]:
    current = _point(slots.current, "current slot")
    delay_4 = _point(slots.delay_4, "delay-4 slot")
    delay_5 = _point(slots.delay_5, "delay-5 slot")
    delay_theta = _point(slots.delay_theta, "delay-Theta slot")
    return tuple(
        (anisotropic_graph_cutoff(point), anisotropic_graph_cutoff_gradient(point))
        for point in (current, delay_4, delay_5, delay_theta)
    )  # type: ignore[return-value]


def cutoff_graph_transform(
    slots: FlowSlots, *, rho: float, nu: float, eta: float
) -> Point:
    """Evaluate one explicit global bounded graph-transform extension.

    Each physical channel is multiplied by the graph cutoffs of exactly the
    state slots on which that channel depends: ``{0}`` for the local cubic,
    ``{0,4,5}`` for the linear and cubic delay channels, and ``{0,Theta}``
    for the eta channel.  Thus eta=0 is globally Theta-inactive.  The
    extension is physical when all active slots lie in the plateau.  It is a
    frozen admissible datum, not a solved graph.
    """

    rho_value = _finite(rho, "rho")
    nu_value = _finite(nu, "nu")
    eta_value = _finite(eta, "eta")
    x, y = _point(slots.current, "current slot")
    x4, _ = _point(slots.delay_4, "delay-4 slot")
    x5, _ = _point(slots.delay_5, "delay-5 slot")
    xtheta, _ = _point(slots.delay_theta, "delay-Theta slot")
    (w0, _), (w4, _), (w5, _), (wtheta, _) = _cutoff_term_data(slots)

    if w0 == 0.0:
        return 0.0, rho_value * nu_value

    local = -(x**3) / 3.0
    shared_delay = 0.0
    if w4 != 0.0 and w5 != 0.0:
        linear_delay = (x4 + x5) / 2.0 - x
        cubic_delay = (x4**3 + x5**3) / 2.0 - x**3
        shared_delay = (
            (w4 * w5 / 5.0) * linear_delay
            + (rho_value**2 * w4 * w5 / 4.0) * cubic_delay
        )
    eta_channel = 0.0
    if wtheta != 0.0 and eta_value != 0.0 and rho_value != 0.0:
        eta_delay = x * x - xtheta * xtheta
        eta_channel = rho_value * eta_value * wtheta * eta_delay

    forcing_x = (
        w0 * local
        + w0 * shared_delay
        + w0 * eta_channel
    )
    qx = w0 * (y - x * x) + rho_value * forcing_x
    # F_Y=nu is already bounded and uses no state slot.  Keeping it uncut
    # gives the exact global scalar reduction Q_Y=chi*q0_Y+rho*nu.
    qy = w0 * (-x) + rho_value * nu_value
    return qx, qy


def cutoff_graph_y(state: Sequence[float], *, rho: float, nu: float) -> float:
    """The known global Y component in the scalar fixed-point reduction."""

    x, _ = _point(state)
    rho_value = _finite(rho, "rho")
    nu_value = _finite(nu, "nu")
    return anisotropic_graph_cutoff(state) * (-x) + rho_value * nu_value


def cutoff_delayed_slot_gradients(
    slots: FlowSlots, *, rho: float, eta: float
) -> tuple[Point, Point, Point]:
    """Gradients of ``T_X`` with respect to the 4, 5, and Theta slots."""

    rho_value = _finite(rho, "rho")
    eta_value = _finite(eta, "eta")
    x, _ = _point(slots.current, "current slot")
    x4, _ = _point(slots.delay_4, "delay-4 slot")
    x5, _ = _point(slots.delay_5, "delay-5 slot")
    xtheta, _ = _point(slots.delay_theta, "delay-Theta slot")
    (w0, _), (w4, dw4), (w5, dw5), (wtheta, dwtheta) = (
        _cutoff_term_data(slots)
    )
    if w0 == 0.0:
        return (0.0, 0.0), (0.0, 0.0), (0.0, 0.0)

    def add(left: Point, right: Point) -> Point:
        return left[0] + right[0], left[1] + right[1]

    def scaled_product_gradient(
        *,
        other_weight: float,
        weight: float,
        dweight: Point,
        value: float,
        dx: float,
        scale: float,
    ) -> Point:
        return (
            scale
            * w0
            * other_weight
            * (dweight[0] * value + weight * dx),
            scale * w0 * other_weight * dweight[1] * value,
        )

    shared_4 = (0.0, 0.0)
    shared_5 = (0.0, 0.0)
    if w4 != 0.0 and w5 != 0.0:
        linear_delay = (x4 + x5) / 2.0 - x
        cubic_delay = (x4**3 + x5**3) / 2.0 - x**3
        linear_4 = scaled_product_gradient(
            other_weight=w5,
            weight=w4,
            dweight=dw4,
            value=linear_delay,
            dx=0.5,
            scale=rho_value / 5.0,
        )
        cubic_4 = scaled_product_gradient(
            other_weight=w5,
            weight=w4,
            dweight=dw4,
            value=cubic_delay,
            dx=1.5 * x4 * x4,
            scale=rho_value**3 / 4.0,
        )
        linear_5 = scaled_product_gradient(
            other_weight=w4,
            weight=w5,
            dweight=dw5,
            value=linear_delay,
            dx=0.5,
            scale=rho_value / 5.0,
        )
        cubic_5 = scaled_product_gradient(
            other_weight=w4,
            weight=w5,
            dweight=dw5,
            value=cubic_delay,
            dx=1.5 * x5 * x5,
            scale=rho_value**3 / 4.0,
        )
        shared_4 = add(linear_4, cubic_4)
        shared_5 = add(linear_5, cubic_5)
    theta = (0.0, 0.0)
    if wtheta != 0.0 and rho_value != 0.0 and eta_value != 0.0:
        eta_delay = x**2 - xtheta * xtheta
        theta = (
            rho_value**2
            * eta_value
            * w0
            * (dwtheta[0] * eta_delay - 2.0 * wtheta * xtheta),
            rho_value**2 * eta_value * w0 * dwtheta[1] * eta_delay,
        )
    return shared_4, shared_5, theta


def uncut_flow_slot_coefficients(
    slots: FlowSlots, *, rho: float, eta: float
) -> tuple[float, float, float]:
    """Return the exact uncut coefficients multiplying flow variations."""

    rho_value = _finite(rho, "rho")
    eta_value = _finite(eta, "eta")
    x4, _ = _point(slots.delay_4, "delay-4 slot")
    x5, _ = _point(slots.delay_5, "delay-5 slot")
    xtheta, _ = _point(slots.delay_theta, "delay-Theta slot")
    return (
        rho_value / 10.0 + 3.0 * rho_value**3 * x4 * x4 / 8.0,
        rho_value / 10.0 + 3.0 * rho_value**3 * x5 * x5 / 8.0,
        -2.0 * rho_value**2 * eta_value * xtheta,
    )


def flow_variation_rhs(
    derivative: Matrix2,
    variation: Sequence[float],
    field_direction: Sequence[float],
) -> Point:
    """Evaluate ``zeta'=-DQ(y)zeta-V(y)`` for a backward flow."""

    if len(derivative) != 2 or any(len(row) != 2 for row in derivative):
        raise ValueError("derivative must be a 2 by 2 matrix")
    z0, z1 = _point(variation, "flow variation")
    v0, v1 = _point(field_direction, "field direction")
    entries = tuple(float(value) for row in derivative for value in row)
    if any(not math.isfinite(value) for value in entries):
        raise ValueError("derivative entries must be finite")
    return (
        -(entries[0] * z0 + entries[1] * z1) - v0,
        -(entries[2] * z0 + entries[3] * z1) - v1,
    )


def graph_residual_directional_derivative(
    *,
    field_direction_at_current: float,
    delayed_variations: tuple[Point, Point, Point],
    delayed_slot_gradients: tuple[Point, Point, Point],
) -> float:
    """Evaluate ``(I-D_q T)[V]`` after the three flow variations are known."""

    current = _finite(field_direction_at_current, "field direction")
    total = 0.0
    for variation, gradient in zip(
        delayed_variations, delayed_slot_gradients, strict=True
    ):
        z0, z1 = _point(variation, "delayed variation")
        g0, g1 = _point(gradient, "slot gradient")
        total += g0 * z0 + g1 * z1
    return current - total


def _theta_value(theta: float) -> float:
    value = _finite(theta, "Theta")
    if not float(THETA_LOWER) <= value <= float(THETA_UPPER):
        raise ValueError("Theta must lie in the pinned directed interval")
    return value


def graph_transform_from_candidate(
    qx: ScalarField,
    state: Sequence[float],
    *,
    rho: float,
    nu: float,
    eta: float,
    theta: float,
    backward_flow: BackwardFlow,
) -> tuple[Point, FlowSlots]:
    """Apply the cutoff graph transform to a supplied scalar candidate.

    The callback is required to compute backward, not forward, flow.  This
    routine intentionally supplies no ODE integrator and makes no validation
    claim about the callback.
    """

    current = _point(state)
    theta_value = _theta_value(theta)

    def field(point: Point) -> Point:
        point_value = _point(point)
        qx_value = _finite(qx(point_value), "candidate qx")
        return qx_value, cutoff_graph_y(point_value, rho=rho, nu=nu)

    slots = FlowSlots(
        current=current,
        delay_4=_point(backward_flow(field, current, DELAY_FOUR), "delay-4 flow"),
        delay_5=_point(backward_flow(field, current, DELAY_FIVE), "delay-5 flow"),
        delay_theta=_point(
            backward_flow(field, current, theta_value), "delay-Theta flow"
        ),
    )
    return cutoff_graph_transform(slots, rho=rho, nu=nu, eta=eta), slots


def graph_fixed_point_residual(
    qx: ScalarField,
    state: Sequence[float],
    *,
    rho: float,
    nu: float,
    eta: float,
    theta: float,
    backward_flow: BackwardFlow,
) -> float:
    """Return the scalar residual ``q(u)-T_X(q)(u)``."""

    current = _point(state)
    transformed, _ = graph_transform_from_candidate(
        qx,
        current,
        rho=rho,
        nu=nu,
        eta=eta,
        theta=theta,
        backward_flow=backward_flow,
    )
    return _finite(qx(current), "candidate qx") - transformed[0]


def seeley_moment(order: int) -> Fraction:
    """Return ``sum a_k(-b_k)^order`` exactly."""

    if isinstance(order, bool) or int(order) != order or order < 0:
        raise ValueError("order must be a nonnegative integer")
    return sum(
        (
            weight * Fraction((-node) ** int(order))
            for node, weight in zip(SEELEY_NODES, SEELEY_WEIGHTS, strict=True)
        ),
        Fraction(0),
    )


def seeley_normal_extension(
    field_difference: Callable[[float, float], Sequence[float]],
    sigma: float,
    normal: float,
    *,
    core_radius: float = PLANAR_NORMAL_CORE_RADIUS,
    extension_width: float = PLANAR_NORMAL_EXTENSION_WIDTH,
) -> Point:
    """Extend a C3 field difference off a fixed normal strip.

    On ``|d|<=r0`` this returns the supplied value.  On each outer strip it
    uses ``sum a_k f(sign*(r0-b_k*t))`` and a flat cutoff.  The moment
    identities through order three match all normal derivatives at the
    inner boundary, while flatness makes the extension zero at the outer
    boundary.  The implication requires the supplied field to be C3 on the
    closed core strip; this routine does not certify that hypothesis.
    """

    sigma_value = _finite(sigma, "sigma")
    normal_value = _finite(normal, "normal")
    radius = _finite(core_radius, "core radius")
    width = _finite(extension_width, "extension width")
    if radius <= 0 or width <= 0:
        raise ValueError("normal radii must be positive")
    if width > radius / 2.0:
        raise ValueError("extension width must not exceed half the core radius")

    def value_at(sample_normal: float) -> Point:
        return _point(
            field_difference(sigma_value, sample_normal),
            "field difference",
        )

    distance = abs(normal_value)
    if distance <= radius:
        return value_at(normal_value)
    outward = distance - radius
    if outward >= width:
        return 0.0, 0.0
    sign = math.copysign(1.0, normal_value)
    reflected = [0.0, 0.0]
    for node, weight in zip(SEELEY_NODES, SEELEY_WEIGHTS, strict=True):
        sample = sign * (radius - node * outward)
        component = value_at(sample)
        reflected[0] += float(weight) * component[0]
        reflected[1] += float(weight) * component[1]
    outer_cutoff = flat_cutoff_ratio(1.0 + outward / width)
    return outer_cutoff * reflected[0], outer_cutoff * reflected[1]


def prepared_planar_field(
    graph_field: VectorField,
    state: Sequence[float],
    *,
    core_radius: float = PLANAR_NORMAL_CORE_RADIUS,
    extension_width: float = PLANAR_NORMAL_EXTENSION_WIDTH,
) -> Point:
    """Conditionally form the separate full-plane C3 prepared trace field."""

    current = _point(state)
    sigma, normal = canard_coordinates(current)
    q0_current = singular_field(current)
    longitudinal_weight = septic_cutoff(
        sigma,
        plateau_end=PLANAR_LONGITUDINAL_PLATEAU_RADIUS,
        transition_width=(
            PLANAR_LONGITUDINAL_SUPPORT_RADIUS
            - PLANAR_LONGITUDINAL_PLATEAU_RADIUS
        ),
    )
    if longitudinal_weight == 0.0:
        return q0_current

    def difference(sample_sigma: float, sample_normal: float) -> Point:
        sample_state = state_from_canard_coordinates(
            sample_sigma, sample_normal
        )
        graph_value = _point(graph_field(sample_state), "graph field")
        q0_value = singular_field(sample_state)
        return graph_value[0] - q0_value[0], graph_value[1] - q0_value[1]

    extension = seeley_normal_extension(
        difference,
        sigma,
        normal,
        core_radius=core_radius,
        extension_width=extension_width,
    )
    return (
        q0_current[0] + longitudinal_weight * extension[0],
        q0_current[1] + longitudinal_weight * extension[1],
    )


@dataclass(frozen=True)
class IntervalRecord:
    lower: str
    upper: str
    width_upper: str


def _record(value: DirectedInterval, digits: int = 100) -> IntervalRecord:
    lower = decimal_lower(value.lower, digits)
    upper = decimal_upper(value.upper, digits)
    serialized = DirectedInterval.from_bounds(lower, upper, value.precision)
    return IntervalRecord(
        lower=lower,
        upper=upper,
        width_upper=decimal_upper(serialized.width_upper(), digits),
    )


def jet_block_keys() -> tuple[tuple[int, int], ...]:
    """Return the exact theorem-native (total, parameter) block keys."""

    keys = {
        (a + b + c + e, b + c + e)
        for a in range(STATE_JET_MAX + 1)
        for b in range(AMPLITUDE_JET_MAX + 1)
        for c in range(NU_JET_MAX + 1)
        for e in range(ETA_JET_MAX + 1)
    }
    return tuple(sorted(keys))


@dataclass(frozen=True)
class FrozenGraphOperatorCertificate:
    """Machine-readable status of the executable operator contract."""

    audit_id: str
    model_id: str
    epsilon: str
    target_amplitude: str
    arithmetic: str
    backward_flow_slots: tuple[str, str, str]
    backward_flow_convention: str
    synchronous_unknown: str
    synchronous_known_y_component_on_uncut_hull: str
    synchronous_known_y_component_global_extension: str
    physical_uncut_x_transform: str
    physical_uncut_y_transform: str
    uncut_residual_frechet_row: str
    eta_partial_source_at_fixed_graph: str
    singular_core_first_rho_graph_jet: str
    singular_core_first_rho_graph_jet_domain: str
    graph_cutoff_id: str
    graph_cutoff_role: str
    graph_cutoff_profile: str
    graph_cutoff_coordinates: str
    graph_cutoff_regular_order: str
    graph_cutoff_frozen_in_rho_nu_eta: bool
    graph_base_extension_formula: str
    graph_forcing_termwise_slot_sets: tuple[str, ...]
    graph_longitudinal_plateau_radius: str
    graph_longitudinal_support_radius: str
    graph_normal_plateau_radius: str
    graph_normal_support_radius: str
    planar_cutoff_id: str
    planar_cutoff_role: str
    planar_longitudinal_plateau_radius: int
    planar_longitudinal_support_radius: int
    planar_normal_core_radius: str
    planar_normal_extension_width: str
    seeley_nodes: tuple[int, ...]
    seeley_weights: tuple[str, ...]
    seeley_moments_zero_through_three: tuple[str, ...]
    seeley_fourth_moment: str
    theta_interval: IntervalRecord
    theorem_jet_rectangle_cardinality: int
    theorem_block_keys: tuple[str, ...]
    theorem_block_count: int
    theorem_nesting_depth: int
    theorem_kappa_schedule: tuple[str, ...]
    theorem_time_buffer: IntervalRecord
    theorem_outer_buffer_b_star: IntervalRecord
    theorem_required_longitudinal_plateau: IntervalRecord
    chosen_longitudinal_plateau_margin: IntervalRecord
    explicit_uncut_slot_algebra_validated: bool
    rho_zero_uncut_map_is_q0: bool
    rho_zero_graph_frechet_derivative_is_zero: bool
    singular_core_first_rho_graph_jet_validated: bool
    eta_zero_theta_slot_coefficient_is_zero: bool
    theta_slot_retained_for_eta_jet_and_history_horizon: bool
    backward_flow_variation_equation_encoded: bool
    cutoff_residual_directional_row_encoded: bool
    graph_and_planar_cutoffs_distinct: bool
    seed_c3_cutoff_refused_as_graph_cutoff: bool
    continuous_depth_two_flow_hull_required: bool
    explicit_c_infinity_graph_extension_frozen: bool
    graph_extension_is_bounded_complete_field_datum: bool
    theorem_native_nesting_arithmetic_validated: bool
    chosen_longitudinal_plateau_contains_theorem_native_nesting: bool
    seeley_c3_matching_identities_validated: bool
    conditional_full_plane_c3_preparation_rule_constructed: bool
    nonpolynomial_first_graph_jet_obstruction_proved: bool
    target_graph_theorem_hypotheses_validated: bool
    target_nesting_inequalities_validated: bool
    backward_flow_evaluator_interval_validated: bool
    graph_operator_discretized: bool
    graph_fixed_point_candidate_computed: bool
    graph_fixed_point_residual_interval_validated: bool
    graph_fixed_point_inverse_interval_validated: bool
    positive_amplitude_depth_two_hull_validated: bool
    complete_graph_preparation_datum_constructed: bool
    first_jet_realised_by_same_graph_preparation: bool
    nonlinear_prepared_trace_family_validated: bool
    positive_amplitude_root_continued: bool
    fixed_epsilon_complete_history_root_validated: bool
    general_network_fredholm_lift_validated: bool
    biological_pulse_control_chain_validated: bool


def build_reference_certificate(
    *, precision: int = PRECISION_BITS
) -> FrozenGraphOperatorCertificate:
    """Build the deterministic exact/directed contract certificate."""

    theta = DirectedInterval.from_bounds(THETA_LOWER, THETA_UPPER, precision)
    block_keys = jet_block_keys()
    rectangle_cardinality = (
        (STATE_JET_MAX + 1)
        * (AMPLITUDE_JET_MAX + 1)
        * (NU_JET_MAX + 1)
        * (ETA_JET_MAX + 1)
    )
    block_count = len(block_keys)
    nesting_depth = 2 * block_count + 4
    time_buffer = theta + 1
    outer_buffer = (nesting_depth + 1) * time_buffer + 2
    required_plateau = WIDE_GRAPH_TARGET + outer_buffer
    chosen_margin = GRAPH_LONGITUDINAL_PLATEAU_RADIUS - required_plateau
    moments = tuple(seeley_moment(order) for order in range(5))

    return FrozenGraphOperatorCertificate(
        audit_id=AUDIT_ID,
        model_id=MODEL_ID,
        epsilon=EPSILON,
        target_amplitude=TARGET_AMPLITUDE,
        arithmetic=(
            "exact rational jet/block/Seeley algebra; 512-bit MPFR-directed "
            "Theta and nesting arithmetic; binary64 evaluators only for the "
            "declared operator maps, not for a graph validation"
        ),
        backward_flow_slots=("4", "5", "Theta_*"),
        backward_flow_convention="P_tau^q(u)=pi_X Phi_Q^{-tau}(u)",
        synchronous_unknown="q=Q_X in a scalar C_b^r(R^2) fixed point",
        synchronous_known_y_component_on_uncut_hull="Q_Y=-X+rho*nu",
        synchronous_known_y_component_global_extension=(
            "Q_Y=chi_graph(u)*(-X)+rho*nu"
        ),
        physical_uncut_x_transform=(
            "Y-X^2+rho[-X^3/3+((P_4+P_5)/2-X)/5]"
            "+rho^2*eta[X^2-P_Theta^2]"
            "+rho^3[((P_4^3+P_5^3)/2-X^3)/4]"
        ),
        physical_uncut_y_transform="-X+rho*nu",
        uncut_residual_frechet_row=(
            "V(u)-(rho/10+3rho^3 P_4^2/8)xi_4"
            "-(rho/10+3rho^3 P_5^2/8)xi_5"
            "+2rho^2 eta P_Theta xi_Theta"
        ),
        eta_partial_source_at_fixed_graph="rho^2*(X^2-P_Theta^2)",
        singular_core_first_rho_graph_jet="(s^3/24+9/20,nu)",
        singular_core_first_rho_graph_jet_domain=(
            "all s whose continuous 0/4/5 backward q0-flow hull remains "
            "inside chi_graph=1; in particular the reference |s|<=20 core"
        ),
        graph_cutoff_id="chi_graph_cinfinity_anisotropic_537x1",
        graph_cutoff_role=(
            "global bounded complete-field extension for q0 and every "
            "current/delayed polynomial slot in the graph transform"
        ),
        graph_cutoff_profile=(
            "chi(r)=1 for r<=1, exp(-1/(2-r))/(exp(-1/(r-1))"
            "+exp(-1/(2-r))) for 1<r<2, 0 for r>=2"
        ),
        graph_cutoff_coordinates="product in |sigma|/537 and |d|/1",
        graph_cutoff_regular_order="C_infinity (in particular C_b^12)",
        graph_cutoff_frozen_in_rho_nu_eta=True,
        graph_base_extension_formula="q0,S=chi_graph*q0",
        graph_forcing_termwise_slot_sets=(
            "local_cubic:{0}",
            "linear_delay:{0,4,5}",
            "eta_quadratic:{0,Theta_*}",
            "cubic_delay:{0,4,5}",
            "slow_unfolding:{}",
        ),
        graph_longitudinal_plateau_radius=str(
            int(GRAPH_LONGITUDINAL_PLATEAU_RADIUS)
        ),
        graph_longitudinal_support_radius=str(
            int(GRAPH_LONGITUDINAL_SUPPORT_RADIUS)
        ),
        graph_normal_plateau_radius=str(int(GRAPH_NORMAL_PLATEAU_RADIUS)),
        graph_normal_support_radius=str(int(GRAPH_NORMAL_SUPPORT_RADIUS)),
        planar_cutoff_id="chi_plan_c3_septic_20_21",
        planar_cutoff_role=(
            "join the normally extended computed graph perturbation to q0 "
            "near the canonical planar tails; excluded from graph transform"
        ),
        planar_longitudinal_plateau_radius=(
            PLANAR_LONGITUDINAL_PLATEAU_RADIUS
        ),
        planar_longitudinal_support_radius=(
            PLANAR_LONGITUDINAL_SUPPORT_RADIUS
        ),
        planar_normal_core_radius=str(int(PLANAR_NORMAL_CORE_RADIUS)),
        planar_normal_extension_width="1/2",
        seeley_nodes=SEELEY_NODES,
        seeley_weights=tuple(str(value) for value in SEELEY_WEIGHTS),
        seeley_moments_zero_through_three=tuple(
            str(value) for value in moments[:4]
        ),
        seeley_fourth_moment=str(moments[4]),
        theta_interval=_record(theta),
        theorem_jet_rectangle_cardinality=rectangle_cardinality,
        theorem_block_keys=tuple(f"({g},{h})" for g, h in block_keys),
        theorem_block_count=block_count,
        theorem_nesting_depth=nesting_depth,
        theorem_kappa_schedule=tuple(
            f"{61 - index}/62" for index in range(nesting_depth + 1)
        ),
        theorem_time_buffer=_record(time_buffer),
        theorem_outer_buffer_b_star=_record(outer_buffer),
        theorem_required_longitudinal_plateau=_record(required_plateau),
        chosen_longitudinal_plateau_margin=_record(chosen_margin),
        explicit_uncut_slot_algebra_validated=True,
        rho_zero_uncut_map_is_q0=True,
        rho_zero_graph_frechet_derivative_is_zero=True,
        singular_core_first_rho_graph_jet_validated=True,
        eta_zero_theta_slot_coefficient_is_zero=True,
        theta_slot_retained_for_eta_jet_and_history_horizon=True,
        backward_flow_variation_equation_encoded=True,
        cutoff_residual_directional_row_encoded=True,
        graph_and_planar_cutoffs_distinct=True,
        seed_c3_cutoff_refused_as_graph_cutoff=True,
        continuous_depth_two_flow_hull_required=True,
        explicit_c_infinity_graph_extension_frozen=True,
        graph_extension_is_bounded_complete_field_datum=True,
        theorem_native_nesting_arithmetic_validated=(
            rectangle_cardinality == 96
            and block_count == 28
            and nesting_depth == 60
        ),
        chosen_longitudinal_plateau_contains_theorem_native_nesting=(
            chosen_margin.lower > 0
        ),
        seeley_c3_matching_identities_validated=(
            moments[:4] == (Fraction(1),) * 4
        ),
        conditional_full_plane_c3_preparation_rule_constructed=True,
        nonpolynomial_first_graph_jet_obstruction_proved=True,
        target_graph_theorem_hypotheses_validated=False,
        target_nesting_inequalities_validated=False,
        backward_flow_evaluator_interval_validated=False,
        graph_operator_discretized=False,
        graph_fixed_point_candidate_computed=False,
        graph_fixed_point_residual_interval_validated=False,
        graph_fixed_point_inverse_interval_validated=False,
        positive_amplitude_depth_two_hull_validated=False,
        complete_graph_preparation_datum_constructed=False,
        first_jet_realised_by_same_graph_preparation=False,
        nonlinear_prepared_trace_family_validated=False,
        positive_amplitude_root_continued=False,
        fixed_epsilon_complete_history_root_validated=False,
        general_network_fredholm_lift_validated=False,
        biological_pulse_control_chain_validated=False,
    )


PROVED_FLAGS = (
    "explicit_uncut_slot_algebra_validated",
    "rho_zero_uncut_map_is_q0",
    "rho_zero_graph_frechet_derivative_is_zero",
    "singular_core_first_rho_graph_jet_validated",
    "eta_zero_theta_slot_coefficient_is_zero",
    "theta_slot_retained_for_eta_jet_and_history_horizon",
    "backward_flow_variation_equation_encoded",
    "cutoff_residual_directional_row_encoded",
    "graph_and_planar_cutoffs_distinct",
    "seed_c3_cutoff_refused_as_graph_cutoff",
    "continuous_depth_two_flow_hull_required",
    "explicit_c_infinity_graph_extension_frozen",
    "graph_extension_is_bounded_complete_field_datum",
    "theorem_native_nesting_arithmetic_validated",
    "chosen_longitudinal_plateau_contains_theorem_native_nesting",
    "seeley_c3_matching_identities_validated",
    "conditional_full_plane_c3_preparation_rule_constructed",
    "nonpolynomial_first_graph_jet_obstruction_proved",
    "graph_cutoff_frozen_in_rho_nu_eta",
)

OPEN_FLAGS = (
    "target_graph_theorem_hypotheses_validated",
    "target_nesting_inequalities_validated",
    "backward_flow_evaluator_interval_validated",
    "graph_operator_discretized",
    "graph_fixed_point_candidate_computed",
    "graph_fixed_point_residual_interval_validated",
    "graph_fixed_point_inverse_interval_validated",
    "positive_amplitude_depth_two_hull_validated",
    "complete_graph_preparation_datum_constructed",
    "first_jet_realised_by_same_graph_preparation",
    "nonlinear_prepared_trace_family_validated",
    "positive_amplitude_root_continued",
    "fixed_epsilon_complete_history_root_validated",
    "general_network_fredholm_lift_validated",
    "biological_pulse_control_chain_validated",
)


def json_ready_frozen_graph_operator_audit() -> dict[str, Any]:
    """Return the canonical JSON-ready audit object."""

    return json.loads(
        json.dumps({"certificate": asdict(build_reference_certificate())})
    )


def validate_frozen_graph_operator_audit(payload: Mapping[str, Any]) -> None:
    """Reject algebra changes or silent claim promotion/weakening."""

    if not isinstance(payload, Mapping):
        raise ValueError("audit payload must be a mapping")
    certificate = payload.get("certificate")
    if not isinstance(certificate, Mapping):
        raise ValueError("certificate must be a mapping")
    # Strict bool checks must precede equality: Python considers 1==True and
    # 0==False, which would otherwise admit a type-changing tamper.
    if any(certificate.get(name) is not True for name in PROVED_FLAGS):
        raise ValueError("a proved operator-contract flag was weakened")
    if any(certificate.get(name) is not False for name in OPEN_FLAGS):
        raise ValueError("an open graph/root/control gate was promoted")
    if dict(payload) != json_ready_frozen_graph_operator_audit():
        raise ValueError("frozen graph operator audit differs from reference")


def _sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def validate_frozen_graph_operator_result(
    payload: Mapping[str, Any], repository: Path
) -> None:
    """Validate the audit together with its complete manifest and hash chain."""

    if not isinstance(payload, Mapping):
        raise ValueError("result payload must be a mapping")
    if set(payload) != {"audit", "manifest"}:
        raise ValueError("result must contain exactly audit and manifest")
    audit = payload.get("audit")
    manifest = payload.get("manifest")
    if not isinstance(audit, Mapping) or not isinstance(manifest, Mapping):
        raise ValueError("audit and manifest must be mappings")
    validate_frozen_graph_operator_audit(audit)

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
        "proof_source_sha256": _sha256(
            repository / PROOF_SOURCE_RELATIVE_PATH
        ),
        "note_sha256": _sha256(repository / NOTE_RELATIVE_PATH),
    }
    if any(manifest.get(key) != value for key, value in own_hashes.items()):
        raise ValueError("result manifest self hash changed")
    parent_hashes = manifest.get("parent_sha256")
    if not isinstance(parent_hashes, Mapping) or dict(parent_hashes) != PARENT_SHA256:
        raise ValueError("result parent hash ledger changed")
    for name, expected in PARENT_SHA256.items():
        relative = {
            "growing_tube_graph_doc": "docs/growing-tube-graph-proof.md",
            "special_flow_graph_doc": "docs/special-flow-graph-theorem.md",
            "green_phase_selected_traces_doc": "docs/green-phase-selected-traces.md",
            "quadratic_period_locked_root_doc": "docs/quadratic-period-locked-selected-root.md",
            "fixed_epsilon_sliding_window_w1p_bridge_result": (
                "experiments/results/fixed_epsilon_sliding_window_w1p_bridge.json"
            ),
            "fixed_window_prepared_gap_seed_result": (
                "experiments/results/fixed_window_prepared_gap_seed.json"
            ),
        }[name]
        if _sha256(repository / relative) != expected:
            raise ValueError(f"pinned parent changed: {name}")
    checks = manifest.get("parent_claim_checks")
    if not isinstance(checks, Mapping) or set(checks) != PARENT_CLAIM_CHECK_KEYS:
        raise ValueError("parent claim checks are missing or unknown")
    if any(value is not True for value in checks.values()):
        raise ValueError("a parent claim check is not strictly true")
    expected_runtime = {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "arithmetic": MANIFEST_ARITHMETIC,
    }
    if any(manifest.get(key) != value for key, value in expected_runtime.items()):
        raise ValueError("result manifest runtime or arithmetic changed")
