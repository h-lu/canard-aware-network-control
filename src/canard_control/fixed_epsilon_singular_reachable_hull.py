"""Exact singular reachable-hull geometry for the fixed-epsilon graph gate.

The target synchronous graph at ``rho=1/sqrt(5)`` is still unknown.  This
module studies only the uncut singular planar field

    sigma' = 1 - 2 d,        d' = sigma d.

It records a smooth first integral, the real Lambert-W branch geometry, the
exact backward delay hull of the retained canard segment, and the Lie
derivative used by a later positive-amplitude barrier proof.  It deliberately
does not construct a graph fixed point or certify a positive-amplitude hull.

The floating Lambert-W evaluator is diagnostic.  The identities and the
reported hull/conditioning bounds are checked independently with symbolic or
MPFR-directed arithmetic in the hostile tests.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
import math
from pathlib import Path
import platform
from typing import Any, Mapping, Sequence

import gmpy2
import mpmath as mp

from canard_control.directed_interval import (
    DirectedInterval,
    decimal_lower,
    decimal_upper,
    pi_interval,
)
MODEL_ID = "quadratic-period-lock-fixed-epsilon-singular-reachable-hull"
AUDIT_ID = "fixed-epsilon-singular-reachable-hull-v1"
PRECISION_BITS = 512

RETAINED_PHASE_LEFT = -5
RETAINED_PHASE_RIGHT = 5
DELAY_SET = (4, 5, "Theta_*")
REFERENCE_LONGITUDINAL_PLATEAU = 20

# These are the serialized directed endpoints in the two pinned parent JSON
# results, not imports from mutable live Python constants.  The generator and
# hostile tests compare them back to those source-bound parent artifacts.
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
PERIOD_LOWER = (
    "16.540387793180933742742126923985779285430908203086452499999999999999999"
    "999999999999999999999999999999999999999999999999999999999999999999999999"
    "99999999999672458"
)
PERIOD_UPPER = (
    "16.540387803180933742742126923985779285430908203163547500000000000000000"
    "000000000000000000000000000000000000000000000000000000000000000000000000"
    "00000000000327542"
)

FROZEN_GRAPH_RESULT_SHA256 = (
    "2c16c96153c056dd7880adacf3d0f9247a3cecd9f8b5369ffd403b826b3b43be"
)
FIXED_WINDOW_SEED_RESULT_SHA256 = (
    "41d325ca4c06b2e1b8a6ffa4e3908737c7be3d34a937a8a852ef7d1195321f39"
)
LONG_DELAY_TRACE_DOC_SHA256 = (
    "2d04f6c1177960924094acb08e5d3adcb162222522abfd802670f75da4892448"
)

PARENT_SHA256 = {
    "fixed_epsilon_frozen_graph_operator_result": FROZEN_GRAPH_RESULT_SHA256,
    "fixed_window_prepared_gap_seed_result": FIXED_WINDOW_SEED_RESULT_SHA256,
    "long_delay_selected_trace_doc": LONG_DELAY_TRACE_DOC_SHA256,
}

PARENT_CLAIM_CHECK_KEYS = {
    "frozen_graph_parent_requires_positive_amplitude_hull",
    "seed_parent_uses_retained_segment_minus5_plus5",
    "trace_parent_defines_canonical_first_integral",
    "parent_theta_and_period_endpoints_replayed_exactly",
}

PROOF_SOURCE_RELATIVE_PATH = (
    "src/canard_control/fixed_epsilon_singular_reachable_hull.py"
)
GENERATOR_RELATIVE_PATH = (
    "experiments/fixed_epsilon_singular_reachable_hull.py"
)
RESULT_RELATIVE_PATH = (
    "experiments/results/fixed_epsilon_singular_reachable_hull.json"
)
NOTE_RELATIVE_PATH = "docs/fixed-epsilon-singular-reachable-hull.md"
DEFAULT_COMMAND = (
    "PYTHONPATH=src /usr/bin/python3 "
    "experiments/fixed_epsilon_singular_reachable_hull.py"
)
MANIFEST_ARITHMETIC = (
    "exact symbolic identities and 512-bit MPFR-directed horizon, hull, "
    "branch-threshold, and conditioning arithmetic; Lambert-W point "
    "evaluation is diagnostic only; no positive-amplitude flow, graph "
    "fixed point, inverse, trace, or root validation"
)


Point = tuple[float, float]


def _finite(value: float, name: str) -> float:
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result


def _point(value: Sequence[float], name: str = "point") -> Point:
    if len(value) != 2:
        raise ValueError(f"{name} must have two coordinates")
    return _finite(value[0], f"{name}[0]"), _finite(value[1], f"{name}[1]")


def singular_coordinate_rhs(state: Sequence[float]) -> Point:
    """Return ``(sigma',d')`` for the uncut singular field."""

    sigma, normal = _point(state)
    return 1.0 - 2.0 * normal, sigma * normal


def smooth_first_integral(state: Sequence[float]) -> float:
    """Evaluate ``J=d*exp(-2d-sigma^2/2)`` in binary64.

    This evaluator is for diagnostics at moderate finite states.  The exact
    identity is symbolic, and proof bounds in the certificate use MPFR.
    """

    sigma, normal = _point(state)
    exponent = -2.0 * normal - 0.5 * sigma * sigma
    try:
        value = normal * math.exp(exponent)
    except OverflowError as error:
        raise ValueError("first-integral evaluation overflows binary64") from error
    if not math.isfinite(value):
        raise ValueError("first-integral evaluation is not finite")
    return value


def smooth_first_integral_gradient(state: Sequence[float]) -> Point:
    """Return ``(J_sigma,J_d)``."""

    sigma, normal = _point(state)
    exponent = -2.0 * normal - 0.5 * sigma * sigma
    try:
        weight = math.exp(exponent)
    except OverflowError as error:
        raise ValueError("first-integral gradient overflows binary64") from error
    gradient = (-sigma * normal * weight, (1.0 - 2.0 * normal) * weight)
    if not all(math.isfinite(item) for item in gradient):
        raise ValueError("first-integral gradient is not finite")
    return gradient


def log_first_integral(state: Sequence[float]) -> float:
    """Evaluate ``log|d|-2d-sigma^2/2`` away from ``d=0``."""

    sigma, normal = _point(state)
    if normal == 0.0:
        raise ValueError("the logarithmic first integral is undefined at d=0")
    return math.log(abs(normal)) - 2.0 * normal - 0.5 * sigma * sigma


def perturbed_coordinate_rhs(
    state: Sequence[float], perturbation_xy: Sequence[float]
) -> Point:
    """Return the canard-coordinate field for ``Q=q0+Delta``.

    ``perturbation_xy=(Delta_X,Delta_Y)`` contains Cartesian vector-field
    components.  It is not a perturbation already expressed in ``(sigma,d)``.
    """

    sigma, normal = _point(state)
    delta_x, delta_y = _point(perturbation_xy, "perturbation_xy")
    return (
        1.0 - 2.0 * normal - 2.0 * delta_x,
        sigma * normal + sigma * delta_x + delta_y,
    )


def perturbed_first_integral_drift(
    state: Sequence[float], perturbation_xy: Sequence[float]
) -> float:
    """Return the exact forward Lie derivative of ``J`` under ``q0+Delta``."""

    sigma, normal = _point(state)
    delta_x, delta_y = _point(perturbation_xy, "perturbation_xy")
    exponent = -2.0 * normal - 0.5 * sigma * sigma
    try:
        weight = math.exp(exponent)
    except OverflowError as error:
        raise ValueError("first-integral drift overflows binary64") from error
    value = weight * (
        sigma * delta_x + (1.0 - 2.0 * normal) * delta_y
    )
    if not math.isfinite(value):
        raise ValueError("first-integral drift is not finite")
    return value


def curved_barrier_lie_derivative(
    state: Sequence[float],
    perturbation_xy: Sequence[float],
    barrier_slope: float,
) -> float:
    """Return ``L_Q[J-j(sigma)]`` when ``j'(sigma)=barrier_slope``."""

    slope = _finite(barrier_slope, "barrier_slope")
    sigma_dot, _ = perturbed_coordinate_rhs(state, perturbation_xy)
    return perturbed_first_integral_drift(state, perturbation_xy) - slope * sigma_dot


def backward_static_barrier_margin(lie_derivative: float, side: str) -> float:
    """Return a nonnegative inward margin for a static backward J barrier.

    On an upper boundary backward invariance requires the *forward* Lie
    derivative to be nonnegative.  On a lower boundary it must be
    nonpositive.  Returning a common signed margin makes this convention
    executable without hiding the time reversal.
    """

    value = _finite(lie_derivative, "lie_derivative")
    if side == "upper":
        return value
    if side == "lower":
        return -value
    raise ValueError("side must be 'upper' or 'lower'")


def backward_moving_tube_face_margin(
    state: Sequence[float],
    perturbation_xy: Sequence[float],
    face: str,
    boundary_speed: float,
) -> float:
    """Return the inward first-exit margin for one moving backward face."""

    speed = _finite(boundary_speed, "boundary_speed")
    sigma_dot = perturbed_coordinate_rhs(state, perturbation_xy)[0]
    j_dot = perturbed_first_integral_drift(state, perturbation_xy)
    if face == "sigma_lower":
        return -sigma_dot - speed
    if face == "sigma_upper":
        return speed + sigma_dot
    if face == "j_lower":
        return -j_dot - speed
    if face == "j_upper":
        return speed + j_dot
    raise ValueError(
        "face must be sigma_lower, sigma_upper, j_lower, or j_upper"
    )


def backward_normal_boundary_velocity(sigma: float, normal: float) -> float:
    """Return ``d_r=-sigma*d`` for backward time ``r=-t`` under ``q0``."""

    sigma_value = _finite(sigma, "sigma")
    normal_value = _finite(normal, "normal")
    return -sigma_value * normal_value


def backward_normal_variation(sigma: float, delay: float) -> float:
    """Return the exact normal multiplier along the singular canard."""

    sigma_value = _finite(sigma, "sigma")
    delay_value = _finite(delay, "delay")
    if delay_value < 0.0:
        raise ValueError("delay must be nonnegative")
    exponent = -sigma_value * delay_value + 0.5 * delay_value * delay_value
    try:
        value = math.exp(exponent)
    except OverflowError as error:
        raise ValueError("normal variation overflows binary64") from error
    if not math.isfinite(value):
        raise ValueError("normal variation is not finite")
    return value


def lambert_argument(sigma: object, level: object) -> mp.mpf:
    """Return ``-2*h*exp(sigma^2/2)`` using the active mpmath context."""

    sigma_value = mp.mpf(sigma)
    level_value = mp.mpf(level)
    return -2 * level_value * mp.exp(sigma_value * sigma_value / 2)


def level_normals_diagnostic(
    sigma: object, level: object, *, decimal_digits: int = 80
) -> tuple[mp.mpf, ...]:
    """Return the finite real Lambert-W branches of ``J=h``.

    This is a point diagnostic, not an interval proof routine.  Negative
    levels have one ``W_0`` branch.  Positive levels can have lower ``W_0``
    and upper ``W_{-1}`` branches.  The branch point is returned once.
    """

    if type(decimal_digits) is not int:
        raise ValueError("decimal_digits must be an integer")
    if decimal_digits < 30:
        raise ValueError("decimal_digits must be at least 30")
    with mp.workdps(int(decimal_digits)):
        sigma_value = mp.mpf(sigma)
        level_value = mp.mpf(level)
        if not mp.isfinite(sigma_value) or not mp.isfinite(level_value):
            raise ValueError("sigma and level must be finite")
        if level_value == 0:
            return (mp.mpf("0"),)
        if level_value < 0:
            argument = lambert_argument(sigma_value, level_value)
            return (-mp.lambertw(argument, 0).real / 2,)
        maximum = mp.exp(-1 - sigma_value * sigma_value / 2) / 2
        if level_value > maximum:
            return ()
        if level_value == maximum:
            return (mp.mpf("0.5"),)
        argument = lambert_argument(sigma_value, level_value)
        lower = -mp.lambertw(argument, 0).real / 2
        upper = -mp.lambertw(argument, -1).real / 2
        return lower, upper


def positive_level_turning_phase(level: object, *, decimal_digits: int = 80) -> mp.mpf:
    """Return ``sqrt(-2*(1+log(2h)))`` for ``0<h<=1/(2e)``."""

    if type(decimal_digits) is not int:
        raise ValueError("decimal_digits must be an integer")
    if decimal_digits < 30:
        raise ValueError("decimal_digits must be at least 30")
    with mp.workdps(int(decimal_digits)):
        level_value = mp.mpf(level)
        maximum = mp.exp(-1) / 2
        if not mp.isfinite(level_value) or level_value <= 0 or level_value > maximum:
            raise ValueError("level must lie in (0,1/(2e)]")
        if level_value == maximum:
            return mp.mpf("0")
        radicand = -2 * (1 + mp.log(2 * level_value))
        return mp.sqrt(radicand)


def flow_time_integrand_diagnostic(
    sigma: object,
    level: object,
    *,
    branch: int = 0,
    decimal_digits: int = 80,
) -> mp.mpf:
    """Return ``dt/dsigma`` on a regular Lambert-W branch."""

    if type(branch) is not int or branch not in (0, -1):
        raise ValueError("branch must be 0 or -1")
    if type(decimal_digits) is not int:
        raise ValueError("decimal_digits must be an integer")
    if decimal_digits < 30:
        raise ValueError("decimal_digits must be at least 30")
    with mp.workdps(int(decimal_digits)):
        sigma_value = mp.mpf(sigma)
        level_value = mp.mpf(level)
        if not mp.isfinite(sigma_value) or not mp.isfinite(level_value):
            raise ValueError("sigma and level must be finite")
        if branch == -1 and level_value <= 0:
            raise ValueError("W_-1 is not a finite branch for nonpositive level")
        maximum = mp.exp(-1 - sigma_value * sigma_value / 2) / 2
        if level_value > maximum:
            raise ValueError("flow-time coordinate is nonreal")
        if level_value == maximum:
            raise ValueError("flow-time coordinate is singular at a turning point")
        argument = lambert_argument(sigma_value, level_value)
        denominator = 1 + mp.lambertw(argument, branch)
        if denominator == 0:
            raise ValueError("flow-time coordinate is singular at a turning point")
        value = 1 / denominator
        if not mp.isfinite(value) or abs(value.imag) > mp.eps * 32:
            raise ValueError("requested branch is not regular and real")
        return value.real


def normal_level_sensitivity(sigma: float, normal: float) -> float:
    """Return ``partial d / partial h`` on a regular level branch."""

    sigma_value = _finite(sigma, "sigma")
    normal_value = _finite(normal, "normal")
    denominator = 1.0 - 2.0 * normal_value
    if denominator == 0.0:
        raise ValueError("level coordinate is singular at d=1/2")
    exponent = 2.0 * normal_value + 0.5 * sigma_value * sigma_value
    try:
        value = math.exp(exponent) / denominator
    except OverflowError as error:
        raise ValueError("normal level sensitivity overflows binary64") from error
    if not math.isfinite(value):
        raise ValueError("normal level sensitivity is not finite")
    return value


def causal_backward_crossing_time_bound(width: float, clock_lower: float) -> float:
    """Bound backward time to cross a slab when ``sigma_dot>=clock_lower``."""

    width_value = _finite(width, "width")
    clock_value = _finite(clock_lower, "clock_lower")
    if width_value < 0.0:
        raise ValueError("width must be nonnegative")
    if clock_value <= 0.0:
        raise ValueError("clock_lower must be positive")
    return width_value / clock_value


def causal_slab_inverse_gain(
    diagonal_contraction: float, incoming_gain: float
) -> float:
    """Return ``P/(1-lambda)`` for one lower-triangular causal slab."""

    contraction = _finite(diagonal_contraction, "diagonal_contraction")
    incoming = _finite(incoming_gain, "incoming_gain")
    if contraction < 0.0 or contraction >= 1.0:
        raise ValueError("diagonal_contraction must lie in [0,1)")
    if incoming < 0.0:
        raise ValueError("incoming_gain must be nonnegative")
    return incoming / (1.0 - contraction)


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


def _exp_interval(value: DirectedInterval) -> DirectedInterval:
    with gmpy2.context(precision=value.precision, round=gmpy2.RoundDown):
        lower = gmpy2.exp(value.lower)
    with gmpy2.context(precision=value.precision, round=gmpy2.RoundUp):
        upper = gmpy2.exp(value.upper)
    return DirectedInterval(lower, upper, value.precision)


@dataclass(frozen=True)
class SingularReachableHullCertificate:
    model_id: str
    audit_id: str
    precision_bits: int
    singular_coordinate_rhs: tuple[str, str]
    smooth_first_integral: str
    canonical_trace_integral_relation: str
    lambert_inverse_formula: str
    positive_turning_phase_formula: str
    flow_time_integrand_formula: str
    negative_level_uncut_flow_is_incomplete: bool
    zero_level_is_complete_singular_canard: bool
    positive_regular_levels_are_closed: bool
    maximum_positive_level_is_equilibrium: bool
    delay_set: tuple[int | str, ...]
    theta_parent_endpoint_strings: tuple[str, str]
    theta_horizon: IntervalRecord
    theta_recomputed_from_period: IntervalRecord
    inherited_theta_contains_recomputed_theta: bool
    theta_exceeds_linear_center_period: bool
    retained_phase_interval: tuple[int, int]
    depth_one_left_endpoint: IntervalRecord
    depth_two_left_endpoint: IntervalRecord
    depth_two_exact_length: IntervalRecord
    prior_symmetric_depth_two_radius: IntervalRecord
    reference_plateau_margin_over_exact_hull: IntervalRecord
    lower_positive_level_cap_at_sigma_20: IntervalRecord
    level_coordinate_condition_at_sigma_20_d0: IntervalRecord
    backward_normal_factor_at_sigma_minus5_theta: IntervalRecord
    perturbed_coordinate_rhs: tuple[str, str]
    perturbed_first_integral_drift: str
    curved_barrier_lie_derivative: str
    backward_static_lower_condition: str
    backward_static_upper_condition: str
    backward_moving_face_conditions: tuple[str, str, str, str]
    causal_clock_condition: str
    causal_left_germ_condition: str
    causal_lower_component_condition: str
    causal_backward_crossing_bound: str
    causal_slab_forward_substitution: str
    singular_first_integral_identity_proved: bool
    canonical_tail_equivalence_proved: bool
    real_lambert_branch_classification_proved: bool
    branch_and_maximal_interval_qualifications_recorded: bool
    flowbox_delay_translation_proved_conditionally: bool
    singular_depth_m_continuous_hull_formula_proved: bool
    singular_depth_two_asymmetric_hull_validated: bool
    prior_symmetric_interval_is_only_an_overbound: bool
    constant_width_backward_tube_refused: bool
    singular_normal_variation_formula_proved: bool
    perturbed_first_integral_drift_identity_proved: bool
    backward_barrier_sign_contract_proved: bool
    causal_slab_restriction_lemma_proved: bool
    causal_slab_interface_conditions_recorded: bool
    causal_lower_component_ambiguity_excluded: bool
    right_completion_independence_proved_under_lemma_hypotheses: bool
    frozen_zero_exterior_clock_condition_fails: bool
    positive_amplitude_graph_candidate_computed: bool
    positive_amplitude_delta_bounds_validated: bool
    positive_amplitude_barriers_instantiated: bool
    positive_amplitude_depth_two_hull_validated: bool
    fixed_target_localized_graph_theorem_proved: bool
    remote_cutoff_independence_or_decay_proved: bool
    left_preparation_independence_proved: bool
    target_uniform_clock_bound_validated: bool
    target_causal_slab_contractions_validated: bool
    weighted_left_tail_decay_validated: bool
    graph_fixed_point_inverse_validated: bool
    fixed_epsilon_complete_history_root_validated: bool


PROVED_FLAGS = (
    "negative_level_uncut_flow_is_incomplete",
    "zero_level_is_complete_singular_canard",
    "positive_regular_levels_are_closed",
    "maximum_positive_level_is_equilibrium",
    "inherited_theta_contains_recomputed_theta",
    "theta_exceeds_linear_center_period",
    "singular_first_integral_identity_proved",
    "canonical_tail_equivalence_proved",
    "real_lambert_branch_classification_proved",
    "branch_and_maximal_interval_qualifications_recorded",
    "flowbox_delay_translation_proved_conditionally",
    "singular_depth_m_continuous_hull_formula_proved",
    "singular_depth_two_asymmetric_hull_validated",
    "prior_symmetric_interval_is_only_an_overbound",
    "constant_width_backward_tube_refused",
    "singular_normal_variation_formula_proved",
    "perturbed_first_integral_drift_identity_proved",
    "backward_barrier_sign_contract_proved",
    "causal_slab_restriction_lemma_proved",
    "causal_slab_interface_conditions_recorded",
    "causal_lower_component_ambiguity_excluded",
    "right_completion_independence_proved_under_lemma_hypotheses",
    "frozen_zero_exterior_clock_condition_fails",
)

OPEN_FLAGS = (
    "positive_amplitude_graph_candidate_computed",
    "positive_amplitude_delta_bounds_validated",
    "positive_amplitude_barriers_instantiated",
    "positive_amplitude_depth_two_hull_validated",
    "fixed_target_localized_graph_theorem_proved",
    "remote_cutoff_independence_or_decay_proved",
    "left_preparation_independence_proved",
    "target_uniform_clock_bound_validated",
    "target_causal_slab_contractions_validated",
    "weighted_left_tail_decay_validated",
    "graph_fixed_point_inverse_validated",
    "fixed_epsilon_complete_history_root_validated",
)


def build_reference_certificate(
    precision: int = PRECISION_BITS,
) -> SingularReachableHullCertificate:
    """Build the directed singular-geometry certificate."""

    if type(precision) is not int or precision < 64:
        raise ValueError("precision must be an integer of at least 64 bits")
    theta = DirectedInterval.from_bounds(THETA_LOWER, THETA_UPPER, precision)
    period = DirectedInterval.from_bounds(PERIOD_LOWER, PERIOD_UPPER, precision)
    two = DirectedInterval.from_decimal(2, precision)
    five = DirectedInterval.from_decimal(5, precision)
    ten = DirectedInterval.from_decimal(10, precision)
    twenty = DirectedInterval.from_decimal(20, precision)
    recomputed_theta = period / DirectedInterval.from_decimal(5, precision).sqrt()

    depth_one_left = -five - theta
    depth_two_left = -five - two * theta
    depth_two_length = ten + two * theta
    symmetric_radius = five + two * theta
    plateau_margin = twenty - symmetric_radius

    positive_cap = _exp_interval(DirectedInterval.from_decimal(-201, precision)) / two
    level_condition = _exp_interval(DirectedInterval.from_decimal(200, precision))
    normal_exponent = five * theta + (theta**2) / two
    normal_factor = _exp_interval(normal_exponent)
    two_pi = pi_interval(precision) * two

    return SingularReachableHullCertificate(
        model_id=MODEL_ID,
        audit_id=AUDIT_ID,
        precision_bits=precision,
        singular_coordinate_rhs=("1-2d", "sigma*d"),
        smooth_first_integral="d*exp(-2d-sigma^2/2)",
        canonical_trace_integral_relation="mathscrH=(e/2)J",
        lambert_inverse_formula="d_k=-(1/2)W_k(-2h*exp(sigma^2/2))",
        positive_turning_phase_formula="sqrt(-2*(1+log(2h)))",
        flow_time_integrand_formula="1/(1+W_k(-2h*exp(sigma^2/2)))",
        negative_level_uncut_flow_is_incomplete=True,
        zero_level_is_complete_singular_canard=True,
        positive_regular_levels_are_closed=True,
        maximum_positive_level_is_equilibrium=True,
        delay_set=DELAY_SET,
        theta_parent_endpoint_strings=(THETA_LOWER, THETA_UPPER),
        theta_horizon=_record(theta),
        theta_recomputed_from_period=_record(recomputed_theta),
        inherited_theta_contains_recomputed_theta=(
            theta.lower <= recomputed_theta.lower
            and theta.upper >= recomputed_theta.upper
        ),
        theta_exceeds_linear_center_period=(theta.lower > two_pi.upper),
        retained_phase_interval=(RETAINED_PHASE_LEFT, RETAINED_PHASE_RIGHT),
        depth_one_left_endpoint=_record(depth_one_left),
        depth_two_left_endpoint=_record(depth_two_left),
        depth_two_exact_length=_record(depth_two_length),
        prior_symmetric_depth_two_radius=_record(symmetric_radius),
        reference_plateau_margin_over_exact_hull=_record(plateau_margin),
        lower_positive_level_cap_at_sigma_20=_record(positive_cap),
        level_coordinate_condition_at_sigma_20_d0=_record(level_condition),
        backward_normal_factor_at_sigma_minus5_theta=_record(normal_factor),
        perturbed_coordinate_rhs=(
            "1-2d-2Delta_X",
            "sigma*d+sigma*Delta_X+Delta_Y",
        ),
        perturbed_first_integral_drift=(
            "exp(-2d-sigma^2/2)*(sigma*Delta_X+(1-2d)*Delta_Y)"
        ),
        curved_barrier_lie_derivative="Jdot-j'(sigma)*sigma_dot",
        backward_static_lower_condition="Jdot<=0",
        backward_static_upper_condition="Jdot>=0",
        backward_moving_face_conditions=(
            "-sigma_dot>=a'(r)",
            "-sigma_dot<=b'(r)",
            "-Jdot>=ell'(r)",
            "-Jdot<=u'(r)",
        ),
        causal_clock_condition="sigma_dot>=kappa>0",
        causal_left_germ_condition=(
            "matched locally-Lipschitz extension and sigma_dot_Qminus>=0"
        ),
        causal_lower_component_condition=(
            "J(sigma,-d*)<j_-(sigma)<j_+(sigma)<J(sigma,d*), d*<1/2"
        ),
        causal_backward_crossing_bound="slab_width/kappa",
        causal_slab_forward_substitution=(
            "e_j<=(sum_{ell<j}P_jell*e_ell)/(1-lambda_j)"
        ),
        singular_first_integral_identity_proved=True,
        canonical_tail_equivalence_proved=True,
        real_lambert_branch_classification_proved=True,
        branch_and_maximal_interval_qualifications_recorded=True,
        flowbox_delay_translation_proved_conditionally=True,
        singular_depth_m_continuous_hull_formula_proved=True,
        singular_depth_two_asymmetric_hull_validated=True,
        prior_symmetric_interval_is_only_an_overbound=True,
        constant_width_backward_tube_refused=True,
        singular_normal_variation_formula_proved=True,
        perturbed_first_integral_drift_identity_proved=True,
        backward_barrier_sign_contract_proved=True,
        causal_slab_restriction_lemma_proved=True,
        causal_slab_interface_conditions_recorded=True,
        causal_lower_component_ambiguity_excluded=True,
        right_completion_independence_proved_under_lemma_hypotheses=True,
        frozen_zero_exterior_clock_condition_fails=True,
        positive_amplitude_graph_candidate_computed=False,
        positive_amplitude_delta_bounds_validated=False,
        positive_amplitude_barriers_instantiated=False,
        positive_amplitude_depth_two_hull_validated=False,
        fixed_target_localized_graph_theorem_proved=False,
        remote_cutoff_independence_or_decay_proved=False,
        left_preparation_independence_proved=False,
        target_uniform_clock_bound_validated=False,
        target_causal_slab_contractions_validated=False,
        weighted_left_tail_decay_validated=False,
        graph_fixed_point_inverse_validated=False,
        fixed_epsilon_complete_history_root_validated=False,
    )


def json_ready_singular_reachable_hull_audit() -> dict[str, Any]:
    """Return the canonical JSON-ready audit object."""

    return json.loads(json.dumps({"certificate": asdict(build_reference_certificate())}))


def validate_singular_reachable_hull_audit(payload: Mapping[str, Any]) -> None:
    """Reject formula, interval, or claim-status tampering."""

    if not isinstance(payload, Mapping):
        raise ValueError("audit payload must be a mapping")
    certificate = payload.get("certificate")
    if not isinstance(certificate, Mapping):
        raise ValueError("certificate must be a mapping")
    if type(certificate.get("precision_bits")) is not int:
        raise ValueError("precision_bits must be an integer")
    retained = certificate.get("retained_phase_interval")
    if (
        not isinstance(retained, list)
        or len(retained) != 2
        or any(type(item) is not int for item in retained)
    ):
        raise ValueError("retained phase endpoints must be integers")
    delays = certificate.get("delay_set")
    if (
        not isinstance(delays, list)
        or len(delays) != 3
        or type(delays[0]) is not int
        or type(delays[1]) is not int
        or not isinstance(delays[2], str)
    ):
        raise ValueError("delay_set has invalid scalar types")
    if any(certificate.get(name) is not True for name in PROVED_FLAGS):
        raise ValueError("a proved singular-geometry flag was weakened")
    if any(certificate.get(name) is not False for name in OPEN_FLAGS):
        raise ValueError("an open graph/root gate was promoted")
    if dict(payload) != json_ready_singular_reachable_hull_audit():
        raise ValueError("singular reachable-hull audit differs from reference")


def _sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _read_json_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def verify_singular_reachable_hull_parent_evidence(
    repository: Path,
) -> tuple[dict[str, str], dict[str, bool]]:
    """Replay the pinned parent hashes and semantic seam checks."""

    paths = {
        "fixed_epsilon_frozen_graph_operator_result": repository
        / "experiments/results/fixed_epsilon_frozen_graph_operator.json",
        "fixed_window_prepared_gap_seed_result": repository
        / "experiments/results/fixed_window_prepared_gap_seed.json",
        "long_delay_selected_trace_doc": repository
        / "docs/long-delay-selected-trace-proof.md",
    }
    actual = {name: _sha256(path) for name, path in paths.items()}
    if actual != PARENT_SHA256:
        changed = [name for name in PARENT_SHA256 if actual[name] != PARENT_SHA256[name]]
        raise ValueError(f"pinned parent hashes changed: {changed}")

    frozen = _read_json_object(
        paths["fixed_epsilon_frozen_graph_operator_result"]
    )["audit"]["certificate"]
    seed = _read_json_object(paths["fixed_window_prepared_gap_seed_result"])[
        "audit"
    ]["certificate"]
    trace = paths["long_delay_selected_trace_doc"].read_text(encoding="utf-8")
    checks = {
        "frozen_graph_parent_requires_positive_amplitude_hull": (
            frozen.get("continuous_depth_two_flow_hull_required") is True
            and frozen.get("positive_amplitude_depth_two_hull_validated") is False
            and frozen.get("graph_fixed_point_candidate_computed") is False
        ),
        "seed_parent_uses_retained_segment_minus5_plus5": (
            seed.get("retained_segment_end") == 5
            and type(seed.get("retained_segment_end")) is int
            and seed.get("singular_depth_two_hull_covered") is True
            and seed.get("positive_amplitude_depth_two_hull_validated") is False
        ),
        "trace_parent_defines_canonical_first_integral": (
            "H(x,y)=\\frac12e^{-2y}" in trace
            and "\\mathscr H(X,Y)=H(-\\alpha X,\\alpha Y)" in trace
        ),
        "parent_theta_and_period_endpoints_replayed_exactly": (
            frozen.get("theta_interval", {}).get("lower") == THETA_LOWER
            and frozen.get("theta_interval", {}).get("upper") == THETA_UPPER
            and seed.get("period", {}).get("lower") == PERIOD_LOWER
            and seed.get("period", {}).get("upper") == PERIOD_UPPER
        ),
    }
    if set(checks) != PARENT_CLAIM_CHECK_KEYS:
        raise AssertionError("parent claim-check implementation drifted")
    if any(value is not True for value in checks.values()):
        failed = [name for name, value in checks.items() if value is not True]
        raise ValueError(f"pinned parent claim checks failed: {failed}")
    return actual, checks


def validate_singular_reachable_hull_result(
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
    validate_singular_reachable_hull_audit(audit)

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
    replayed_hashes, replayed_checks = (
        verify_singular_reachable_hull_parent_evidence(repository)
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
