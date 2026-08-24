"""Directed certificate for a same-model controlled FHN separator.

The periodic response certificate in this repository concerns the completely
synchronous restriction of the dual-scaffold network declared in
``docs/two-module-reference.md``.  This module keeps that model and its
validated gain box, but changes the *decision protocol*: after a constant
history reset, the collective recovery coordinate is held at zero while the
voltage is released.  The reset-only controller is absent from the baseline
periodic RFDE.

At full-network level put
``pi*x=(bar(x)_1+bar(x)_2)/2`` and apply the physical recovery input
``u_i^w=-epsilon*(pi*v-unfolding)`` at every node.  Then
``pi*u^w=-epsilon*(pi*v-unfolding)``, ``(I-P)u^w=0``, and
``d(pi*w)/dt=0``.  The separator's stable manifold is therefore a manifold
in the *controlled clamped complete-history phase space*, not in the
unforced phase space.

For a synchronous voltage ``x`` the decision equation is

``x' = x - x**3/3 + epsilon*((g(x_tau0)+g(x_tau1))/2-g(x))``,

where ``g(x)=kappa_1*x+kappa_3*(x-1)**3``.  Constant histories annihilate
both delayed-minus-current actuators exactly, and ``x=0`` is therefore the
same exact clamped saddle for every gain pair in the tracked parameter box.

This file checks, with MPFR-directed endpoints,

* ``d < a`` for ``d=epsilon*(kappa_1+3*kappa_3)`` and ``a=1-d``;
  this preserves exactly one right-half-plane characteristic root;
* positive and negative method-of-steps channel inequalities up to the
  first hit of ``x=+1`` or ``x=-1``;
* a lower bound for the constant-history reset's unstable spectral
  projection; and
* for the full-network instance newly fixed here by ``D=3, E=2``, the
  size-uniform linear variational transverse Halanay margin during the
  clamped decision interval, including a directed check that ``0.03`` is a
  valid exponential-rate lower bound.

The number seven in the negative-channel bound is an exact *secant* bound,
not a Lipschitz bound.  If ``u=-x`` and ``-1 <= x <= y <= 0``, then

``((y-1)**3-(x-1)**3)/(-x) <= 3+3*u+u**2 <= 7``.

The transverse variational estimate instead needs the derivative bound
``3*(x-1)**2 <= 12`` on ``[-1,1]``.  Keeping these constants separate is
essential.

The certificate proves an operational, recovery-clamped first-hit onset and
the associated reset-family complete-history threshold.  It does not prove
an unforced or maximal-canard onset, attraction of the periodic orbit, noisy
history capture, nonlinear transverse synchronization, or a theorem for
general graph topology.  The source periodic artifact sees only the
synchronous restriction and therefore does not certify the newly fixed
values ``D=3,E=2``.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import (
    Context,
    Decimal,
    InvalidOperation,
    ROUND_CEILING,
    ROUND_FLOOR,
    localcontext,
)
from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Mapping

import gmpy2
import sympy as sp

from canard_control.directed_interval import (
    DirectedInterval,
    decimal_lower,
    decimal_upper,
)


TRACKED_PARAMETER_BOX_SHA256 = (
    "ff13b5352c2b4e9898a4044be63fd490a3e7bb4217445a6a062188c2457c22a0"
)
SYNCHRONOUS_MODEL_ID = "dual-scaffold-synchronous-fhn-two-delay"
FULL_NETWORK_INSTANCE_ID = "rank-one-two-module-fhn-D3-E2"
CONTROL_ORDER = ("kappa_1", "kappa_3")
OUTPUT_ORDER = ("F", "R_h")
DECISION_PROTOCOL = (
    "prepare v(theta)=r*1,w(theta)=0; release voltage; apply "
    "u_i^w=-epsilon*(pi*v-unfolding) so pi*w=0 until first hit"
)
CONTROLLED_PHASE_SPACE = (
    "X_cl={phi: pi*phi_w(theta)=0 for every history theta}"
)


@dataclass(frozen=True)
class SameModelSeparatorCertificate:
    """Auditable constants and claim boundaries for the decision protocol."""

    source_result_sha256: str
    precision_bits: int
    source_synchronous_model_id: str
    certified_full_network_instance_id: str
    epsilon: str
    unfolding: str
    scaled_delays: tuple[str, str]
    physical_delay_upper: str
    voltage_scaffold: str
    recovery_scaffold: str
    halanay_weight: str
    control_order: tuple[str, str]
    output_order: tuple[str, str]
    gain_half_width: str
    kappa_1_interval: tuple[str, str]
    kappa_3_interval: tuple[str, str]
    linearized_delayed_gain_interval: tuple[str, str]
    linearized_current_growth_interval: tuple[str, str]
    spectral_small_gain_margin_lower: str
    decimal_precision_digits: int
    decimal_recomposed_spectral_margin_lower: str
    positive_cubic_secant_upper: str
    negative_cubic_secant_upper: str
    positive_channel_growth_lower: str
    negative_channel_growth_lower: str
    reset_projection_lower: str
    transverse_coefficient_upper: str
    halanay_local_decay_lower: str
    halanay_delayed_gain_upper: str
    halanay_margin_lower: str
    halanay_rate_candidate: str
    halanay_rate_residual_lower: str
    decimal_recomposed_halanay_margin_lower: str
    decimal_recomposed_halanay_rate_residual_lower: str
    reset_voltage_interval: tuple[str, str]
    channel_faces: tuple[str, str]
    positive_hit_time_formula: str
    negative_hit_time_formula: str
    source_periodic_branch_validated: bool
    source_unique_extrema_validated: bool
    source_response_derivative_box_validated: bool
    same_synchronous_baseline_and_gain_box_validated: bool
    full_network_d3_e2_instance_fixed_by_this_certificate: bool
    source_periodic_artifact_certifies_full_network_scaffolds: bool
    full_network_collective_projection_exact: bool
    physical_collective_recovery_actuator_exact: bool
    actuator_has_zero_transverse_projection_exact: bool
    controlled_collective_recovery_leaf_invariant_exact: bool
    constant_history_delayed_actuation_vanishes_exactly: bool
    constant_history_scaffolds_vanish_exactly: bool
    collective_recovery_clamp_identity_exact: bool
    zero_reset_is_exact_clamped_equilibrium: bool
    one_simple_rhp_characteristic_root_validated: bool
    no_imaginary_characteristic_roots_validated: bool
    positive_channel_capture_validated: bool
    negative_channel_capture_validated: bool
    reset_projection_transversality_validated: bool
    arbitrary_two_module_sizes_linear_variational_transverse_decay_during_clamped_decision_validated: bool
    controlled_operational_onset_validated: bool
    reset_family_complete_history_threshold_validated: bool
    controlled_clamped_complete_history_stable_manifold_validated: bool
    quantified_noisy_history_capture_validated: bool
    nonlinear_transverse_synchronization_during_clamped_decision_validated: bool
    periodic_full_network_transverse_stability_validated: bool
    unforced_complete_history_stable_manifold_validated: bool
    unforced_onset_validated: bool
    maximal_canard_onset_validated: bool
    periodic_orbit_attraction_validated: bool
    general_network_topology_validated: bool
    issue_15_closed: bool


@dataclass(frozen=True)
class SameModelSeparatorAlgebra:
    """Exact polynomial identities used by the directed certificate."""

    delayed_constant_history_residual: sp.Expr
    voltage_scaffold_constant_history_residual: sp.Expr
    controlled_collective_recovery_residual: sp.Expr
    zero_saddle_fast_residual: sp.Expr
    positive_cubic_secant_polynomial: sp.Expr
    negative_cubic_secant_polynomial: sp.Expr
    positive_cubic_secant_endpoint: sp.Expr
    negative_cubic_secant_endpoint: sp.Expr


@dataclass(frozen=True)
class CollectiveClampNetworkAlgebra:
    """Exact node-level projection identities for the physical clamp."""

    module_sizes: tuple[int, int]
    averaging_matrix: sp.Matrix
    collective_projection: sp.Matrix
    projection_row_sum: sp.Expr
    projection_idempotence_residual: sp.Matrix
    collective_actuator_projection: sp.Expr
    expected_collective_actuator_projection: sp.Expr
    transverse_actuator_residual: sp.Matrix
    controlled_collective_recovery_derivative: sp.Expr
    transverse_recovery_derivative_residual: sp.Matrix


@dataclass(frozen=True)
class DecimalEndpointRecomposition:
    """Independent Decimal reconstruction from serialized parent endpoints."""

    precision_digits: int
    spectral_margin_lower: str
    halanay_margin_lower: str
    physical_delay_upper: str
    rate_exponential_upper: str
    rate_residual_lower: str


def same_model_separator_algebra() -> SameModelSeparatorAlgebra:
    """Return exact cancellation and secant-polynomial identities."""

    x, kappa_1, kappa_3, epsilon, unfolding = sp.symbols(
        "x kappa_1 kappa_3 epsilon unfolding", real=True
    )
    u = sp.Symbol("u", nonnegative=True)
    g = kappa_1 * x + kappa_3 * (x - 1) ** 3
    delayed_residual = sp.simplify(epsilon * ((g + g) / 2 - g))
    voltage_scaffold_residual = sp.simplify((x + x) / 2 - x)
    recovery_residual = sp.simplify(
        epsilon * (x - unfolding) - epsilon * (x - unfolding)
    )
    saddle_residual = sp.simplify(x - x**3 / 3).subs(x, 0)

    # For 0 <= y <= x <= 1, the largest positive secant is obtained at
    # y=0.  Division is carried out symbolically before x is set to zero.
    positive = sp.cancel(((x - 1) ** 3 + 1) / x)
    # For -1 <= x <= y <= 0, put u=-x.  The largest negative-side secant
    # is obtained at y=0.
    negative = sp.expand(((1 + u) ** 3 - 1) / u)
    return SameModelSeparatorAlgebra(
        delayed_constant_history_residual=delayed_residual,
        voltage_scaffold_constant_history_residual=voltage_scaffold_residual,
        controlled_collective_recovery_residual=recovery_residual,
        zero_saddle_fast_residual=saddle_residual,
        positive_cubic_secant_polynomial=positive,
        negative_cubic_secant_polynomial=negative,
        positive_cubic_secant_endpoint=sp.simplify(positive.subs(x, 0)),
        negative_cubic_secant_endpoint=sp.simplify(negative.subs(u, 1)),
    )


def collective_clamp_network_algebra(
    first_module_size: int = 2,
    second_module_size: int = 3,
) -> CollectiveClampNetworkAlgebra:
    r"""Return exact full-network identities for the collective clamp.

    For module sizes ``n_1,n_2``, every row of ``P`` is

    ``pi=(1/(2*n_1),...,1/(2*n_1),1/(2*n_2),...,1/(2*n_2))``.

    Thus ``P=1*pi`` and ``pi*x=(bar(x)_1+bar(x)_2)/2``.  The physical
    recovery actuator is the same at every node,

    ``u_i^w=-epsilon*(pi*v-unfolding)``.

    The returned identities verify ``pi*u^w`` equals that scalar,
    ``(I-P)u^w=0``, and the controlled recovery field has
    ``d(pi*w)/dt=0``.  Consequently the complete-history leaf whose every
    recovery trace satisfies ``pi*w(theta)=0`` is invariant under the
    controlled clamped semiflow.
    """

    if (
        isinstance(first_module_size, bool)
        or isinstance(second_module_size, bool)
        or int(first_module_size) != first_module_size
        or int(second_module_size) != second_module_size
    ):
        raise ValueError("module sizes must be integers")
    n_1 = int(first_module_size)
    n_2 = int(second_module_size)
    if n_1 <= 0 or n_2 <= 0:
        raise ValueError("module sizes must be positive")
    dimension = n_1 + n_2
    pi = sp.Matrix(
        [[sp.Rational(1, 2 * n_1)] * n_1 + [sp.Rational(1, 2 * n_2)] * n_2]
    )
    one = sp.ones(dimension, 1)
    averaging = one * pi
    identity = sp.eye(dimension)
    voltage = sp.Matrix(sp.symbols(f"v_0:{dimension}", real=True))
    recovery = sp.Matrix(sp.symbols(f"w_0:{dimension}", real=True))
    epsilon, unfolding, recovery_scaffold = sp.symbols(
        "epsilon unfolding E", real=True
    )
    collective_voltage = (pi * voltage)[0]
    actuator_scalar = -epsilon * (collective_voltage - unfolding)
    actuator = one * actuator_scalar
    recovery_field = (
        epsilon * (voltage - unfolding * one)
        + recovery_scaffold * (averaging * recovery - recovery)
        + actuator
    )
    transverse_expected = (
        epsilon * (identity - averaging) * voltage
        - recovery_scaffold * (identity - averaging) * recovery
    )
    return CollectiveClampNetworkAlgebra(
        module_sizes=(n_1, n_2),
        averaging_matrix=averaging,
        collective_projection=pi,
        projection_row_sum=sp.simplify((pi * one)[0]),
        projection_idempotence_residual=sp.simplify(
            averaging * averaging - averaging
        ),
        collective_actuator_projection=sp.simplify((pi * actuator)[0]),
        expected_collective_actuator_projection=actuator_scalar,
        transverse_actuator_residual=sp.simplify(
            (identity - averaging) * actuator
        ),
        controlled_collective_recovery_derivative=sp.simplify(
            (pi * recovery_field)[0]
        ),
        transverse_recovery_derivative_residual=sp.simplify(
            (identity - averaging) * recovery_field - transverse_expected
        ),
    )


def _decimal_fixed(value: Decimal) -> str:
    return format(value, "f")


def decimal_parent_endpoint_recomposition(
    payload: Mapping[str, Any],
    *,
    precision_digits: int = 110,
) -> DecimalEndpointRecomposition:
    r"""Rebuild lower margins from the serialized parent upper endpoints.

    The gain upper endpoints are parsed directly as :class:`Decimal`; no
    binary float or MPFR serialization round trip is used.  Algebraic upper
    quantities are evaluated with ``ROUND_CEILING`` and lower margins with
    ``ROUND_FLOOR``.  ``Decimal.sqrt`` and ``Decimal.exp`` are correctly
    rounded by the library; one ``next_plus`` is nevertheless applied before
    they enter a lower residual, making their direction explicit even when
    the exact value happens to be representable.
    """

    if (
        isinstance(precision_digits, bool)
        or int(precision_digits) != precision_digits
        or int(precision_digits) < 80
    ):
        raise ValueError("Decimal precision must be an integer of at least 80")
    digits = int(precision_digits)
    root = _mapping(payload, "payload")
    validation = _mapping(root.get("validation"), "validation")
    gain_box = _mapping(validation.get("gain_box"), "gain_box")
    upper_1 = gain_box.get("kappa_1_upper")
    upper_3 = gain_box.get("kappa_3_upper")
    if not isinstance(upper_1, str) or not isinstance(upper_3, str):
        raise ValueError("serialized gain upper endpoints must be strings")
    try:
        kappa_1_upper = Decimal(upper_1)
        kappa_3_upper = Decimal(upper_3)
    except InvalidOperation as error:
        raise ValueError("serialized gain upper endpoints are not decimals") from error
    if not kappa_1_upper.is_finite() or not kappa_3_upper.is_finite():
        raise ValueError("serialized gain upper endpoints must be finite")

    upward = Context(prec=digits, rounding=ROUND_CEILING)
    downward = Context(prec=digits, rounding=ROUND_FLOOR)
    one = Decimal(1)
    two = Decimal(2)
    three = Decimal(3)
    five = Decimal(5)
    twelve = Decimal(12)
    rate = Decimal("0.03")
    epsilon = Decimal("0.2")
    with localcontext(upward) as context:
        delayed_gain_upper = context.multiply(
            epsilon,
            context.add(kappa_1_upper, context.multiply(three, kappa_3_upper)),
        )
        transverse_coefficient_upper = context.add(
            kappa_1_upper, context.multiply(twelve, kappa_3_upper)
        )
        halanay_delayed_upper = context.multiply(
            epsilon, transverse_coefficient_upper
        )
        voltage_loss_upper = context.multiply(
            epsilon, context.add(transverse_coefficient_upper, one)
        )
        sqrt_five_nearest = context.sqrt(five)
        sqrt_five_upper = context.next_plus(sqrt_five_nearest)
        physical_delay_upper = context.multiply(five, sqrt_five_upper)
        rate_delay_upper = context.multiply(rate, physical_delay_upper)
        exponential_nearest = context.exp(rate_delay_upper)
        exponential_upper = context.next_plus(exponential_nearest)
        delayed_exponential_upper = context.multiply(
            halanay_delayed_upper, exponential_upper
        )
    with localcontext(downward) as context:
        spectral_margin_lower = context.subtract(
            one, context.multiply(two, delayed_gain_upper)
        )
        voltage_decay_lower = context.subtract(
            two,
            voltage_loss_upper,
        )
        local_decay_lower = min(one, voltage_decay_lower)
        halanay_margin_lower = context.subtract(
            local_decay_lower, halanay_delayed_upper
        )
        rate_residual_lower = context.subtract(
            context.subtract(local_decay_lower, rate),
            delayed_exponential_upper,
        )
    if min(
        spectral_margin_lower,
        halanay_margin_lower,
        rate_residual_lower,
    ) <= 0:
        raise ValueError("Decimal endpoint reconstruction has no positive margin")
    return DecimalEndpointRecomposition(
        precision_digits=digits,
        spectral_margin_lower=_decimal_fixed(spectral_margin_lower),
        halanay_margin_lower=_decimal_fixed(halanay_margin_lower),
        physical_delay_upper=_decimal_fixed(physical_delay_upper),
        rate_exponential_upper=_decimal_fixed(exponential_upper),
        rate_residual_lower=_decimal_fixed(rate_residual_lower),
    )


def _mapping(value: object, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{name} must be a mapping")
    return value


def _require_true(mapping: Mapping[str, Any], name: str) -> None:
    if mapping.get(name) is not True:
        raise ValueError(f"source proof flag {name!r} must be true")


def _require_false(mapping: Mapping[str, Any], name: str) -> None:
    if mapping.get(name) is not False:
        raise ValueError(f"source scope flag {name!r} must be false")


def _decimal_pair(interval: DirectedInterval) -> tuple[str, str]:
    return decimal_lower(interval.lower, 55), decimal_upper(interval.upper, 55)


def _down(value: gmpy2.mpfr, digits: int = 55) -> str:
    return decimal_lower(value, digits)


def _up(value: gmpy2.mpfr, digits: int = 55) -> str:
    return decimal_upper(value, digits)


def _directed_exp_upper(value: gmpy2.mpfr, precision: int) -> gmpy2.mpfr:
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        return gmpy2.exp(value)


def _contained_declared_gain_box(
    kappa_1: DirectedInterval,
    kappa_3: DirectedInterval,
    precision: int,
) -> bool:
    center_1 = DirectedInterval.from_decimal("0.2", precision)
    center_3 = DirectedInterval.from_decimal("0.25", precision)
    width = DirectedInterval.from_decimal("1e-12", precision)
    declared_1 = center_1 + DirectedInterval.from_bounds(
        -width.upper, width.upper, precision
    )
    declared_3 = center_3 + DirectedInterval.from_bounds(
        -width.upper, width.upper, precision
    )
    return (
        kappa_1.lower <= declared_1.lower
        and kappa_1.upper >= declared_1.upper
        and kappa_3.lower <= declared_3.lower
        and kappa_3.upper >= declared_3.upper
    )


def same_model_separator_from_payload(
    payload: Mapping[str, Any],
    *,
    source_result_sha256: str,
    precision: int = 160,
) -> SameModelSeparatorCertificate:
    """Validate source semantics and derive the separator constants.

    The digest argument records provenance only.  Use
    :func:`load_same_model_separator` when reading a file so its bytes are
    checked against the tracked artifact before any theorem flag is trusted.
    """

    if not isinstance(source_result_sha256, str) or len(source_result_sha256) != 64:
        raise ValueError("source_result_sha256 must be a 64-character digest")
    try:
        int(source_result_sha256, 16)
    except ValueError as error:
        raise ValueError("source_result_sha256 must be hexadecimal") from error
    if (
        isinstance(precision, bool)
        or int(precision) != precision
        or int(precision) < 64
    ):
        raise ValueError("precision must be an integer of at least 64 bits")
    precision = int(precision)

    root = _mapping(payload, "payload")
    validation = _mapping(root.get("validation"), "validation")
    continuation = _mapping(validation.get("continuation"), "continuation")
    extrema = _mapping(validation.get("extrema"), "extrema")
    response = _mapping(validation.get("response"), "response")
    gain_box = _mapping(validation.get("gain_box"), "gain_box")
    scope = _mapping(root.get("scope"), "scope")
    for mapping, flags in (
        (
            validation,
            (
                "d1_validated",
                "d3_validated",
                "d4_response_lower_bound_validated",
                "all_d1_d3_d4_validated",
            ),
        ),
        (continuation, ("parameter_box_orbit_validated",)),
        (extrema, ("extrema_validated",)),
        (response, ("response_box_validated",)),
        (
            scope,
            (
                "d1_parameter_box_continuation",
                "d3_unique_voltage_extrema",
                "d4_directed_response_lower_bound",
            ),
        ),
    ):
        for flag in flags:
            _require_true(mapping, flag)
    _require_false(scope, "response_derivative_lipschitz")
    _require_false(scope, "issue_15_closed")
    _require_false(response, "derivative_lipschitz_bound_supplied")

    if tuple(response.get("control_order", ())) != CONTROL_ORDER:
        raise ValueError("source control order is not (kappa_1, kappa_3)")
    if tuple(response.get("output_order", ())) != OUTPUT_ORDER:
        raise ValueError("source output order is not (F, R_h)")
    if gain_box.get("half_width") != "1e-12":
        raise ValueError("source gain half-width is not the tracked 1e-12")

    bound_names = (
        "kappa_1_lower",
        "kappa_1_upper",
        "kappa_3_lower",
        "kappa_3_upper",
    )
    if any(not isinstance(gain_box.get(name), str) for name in bound_names):
        raise ValueError("gain-box endpoints must be directed decimal strings")
    kappa_1 = DirectedInterval.from_bounds(
        gain_box["kappa_1_lower"], gain_box["kappa_1_upper"], precision
    )
    kappa_3 = DirectedInterval.from_bounds(
        gain_box["kappa_3_lower"], gain_box["kappa_3_upper"], precision
    )
    if kappa_1.lower <= 0 or kappa_3.lower <= 0:
        raise ValueError("the same-model proof requires positive gain intervals")
    if not _contained_declared_gain_box(kappa_1, kappa_3, precision):
        raise ValueError("source gain interval does not contain the declared box")
    decimal_recomposition = decimal_parent_endpoint_recomposition(root)

    one = DirectedInterval.from_decimal(1, precision)
    two = DirectedInterval.from_decimal(2, precision)
    three = DirectedInterval.from_decimal(3, precision)
    five = DirectedInterval.from_decimal(5, precision)
    seven = DirectedInterval.from_decimal(7, precision)
    twelve = DirectedInterval.from_decimal(12, precision)
    epsilon = one / five

    delayed_gain = epsilon * (kappa_1 + three * kappa_3)
    current_growth = one - delayed_gain
    spectral_margin = one - two * delayed_gain
    if spectral_margin.lower <= 0:
        raise ValueError("d<a small-gain inequality is not directed-positive")

    two_thirds = two / three
    positive_growth = two_thirds - epsilon * (kappa_1 + three * kappa_3)
    negative_growth = two_thirds - epsilon * (kappa_1 + seven * kappa_3)
    if positive_growth.lower <= 0 or negative_growth.lower <= 0:
        raise ValueError("one of the signed channel growth constants is nonpositive")

    # For the Laplace-residue normalization of the unstable mode, a
    # constant reset history has coefficient
    #   1 / (lambda_u * Delta'(lambda_u)).
    # The positive root obeys 0<lambda_u<1, and
    # (lambda*tau)e^{-lambda*tau} <= 1, so the denominator is <=1+d.
    reset_projection = one / (one + delayed_gain)
    if reset_projection.lower <= 0:
        raise ValueError("reset projection lower bound is not positive")

    # The transverse bound uses a derivative, hence 12 rather than the
    # negative channel's sharper secant constant 7.
    transverse_coefficient = kappa_1 + twelve * kappa_3
    voltage_decay = three - one - epsilon * (transverse_coefficient + one)
    recovery_decay = two - one
    local_decay_lower = min(voltage_decay.lower, recovery_decay.lower)
    local_decay_upper = min(voltage_decay.upper, recovery_decay.upper)
    local_decay = DirectedInterval.from_bounds(
        local_decay_lower, local_decay_upper, precision
    )
    transverse_delayed = epsilon * transverse_coefficient
    halanay_margin = local_decay - transverse_delayed
    if halanay_margin.lower <= 0:
        raise ValueError("D=3, E=2 transverse Halanay margin is nonpositive")

    # Certify a concrete rate without trusting a floating Lambert-W solve.
    # Halanay's equation is lambda=a-b*exp(lambda*tau_*), with
    # tau_*=5/sqrt(epsilon)=5*sqrt(5).
    rate = DirectedInterval.from_decimal("0.03", precision)
    physical_delay = five * five.sqrt()
    rate_delay = rate * physical_delay
    exponential_upper = _directed_exp_upper(rate_delay.upper, precision)
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        delayed_exponential_upper = (
            transverse_delayed.upper * exponential_upper
        )
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        rate_residual_lower = (
            local_decay.lower - rate.upper - delayed_exponential_upper
        )
    if rate_residual_lower <= 0:
        raise ValueError("declared Halanay rate does not have positive residual")

    algebra = same_model_separator_algebra()
    exact_cancellation = (
        algebra.delayed_constant_history_residual == 0
        and algebra.voltage_scaffold_constant_history_residual == 0
    )
    exact_recovery = algebra.controlled_collective_recovery_residual == 0
    exact_saddle = algebra.zero_saddle_fast_residual == 0
    secants_are_exact = (
        sp.expand(algebra.positive_cubic_secant_polynomial)
        == x_polynomial_positive()
        and algebra.positive_cubic_secant_endpoint == 3
        and algebra.negative_cubic_secant_polynomial
        == u_polynomial_negative()
        and algebra.negative_cubic_secant_endpoint == 7
    )
    if not (exact_cancellation and exact_recovery and exact_saddle):
        raise RuntimeError("exact same-model cancellation audit failed")
    if not secants_are_exact:
        raise RuntimeError("exact signed secant audit failed")

    network_audits = (
        collective_clamp_network_algebra(1, 1),
        collective_clamp_network_algebra(2, 3),
    )
    collective_projection_exact = all(
        audit.projection_row_sum == 1
        and audit.projection_idempotence_residual == sp.zeros(
            sum(audit.module_sizes)
        )
        for audit in network_audits
    )
    actuator_exact = all(
        sp.simplify(
            audit.collective_actuator_projection
            - audit.expected_collective_actuator_projection
        )
        == 0
        for audit in network_audits
    )
    transverse_actuator_exact = all(
        audit.transverse_actuator_residual
        == sp.zeros(sum(audit.module_sizes), 1)
        for audit in network_audits
    )
    controlled_leaf_exact = all(
        audit.controlled_collective_recovery_derivative == 0
        and audit.transverse_recovery_derivative_residual
        == sp.zeros(sum(audit.module_sizes), 1)
        for audit in network_audits
    )
    if not (
        collective_projection_exact
        and actuator_exact
        and transverse_actuator_exact
        and controlled_leaf_exact
    ):
        raise RuntimeError("exact full-network collective clamp audit failed")

    def conservative_lower(mpfr_value: gmpy2.mpfr, decimal_text: str) -> str:
        mpfr_text = _down(mpfr_value)
        return _decimal_fixed(min(Decimal(mpfr_text), Decimal(decimal_text)))

    def conservative_upper(mpfr_value: gmpy2.mpfr, decimal_text: str) -> str:
        mpfr_text = _up(mpfr_value)
        return _decimal_fixed(max(Decimal(mpfr_text), Decimal(decimal_text)))

    spectral_margin_text = conservative_lower(
        spectral_margin.lower,
        decimal_recomposition.spectral_margin_lower,
    )
    halanay_margin_text = conservative_lower(
        halanay_margin.lower,
        decimal_recomposition.halanay_margin_lower,
    )
    rate_residual_text = conservative_lower(
        rate_residual_lower,
        decimal_recomposition.rate_residual_lower,
    )
    physical_delay_text = conservative_upper(
        physical_delay.upper,
        decimal_recomposition.physical_delay_upper,
    )

    return SameModelSeparatorCertificate(
        source_result_sha256=source_result_sha256,
        precision_bits=precision,
        source_synchronous_model_id=SYNCHRONOUS_MODEL_ID,
        certified_full_network_instance_id=FULL_NETWORK_INSTANCE_ID,
        epsilon="1/5",
        unfolding="3/5",
        scaled_delays=("4", "5"),
        physical_delay_upper=physical_delay_text,
        voltage_scaffold="3",
        recovery_scaffold="2",
        halanay_weight="1",
        control_order=CONTROL_ORDER,
        output_order=OUTPUT_ORDER,
        gain_half_width="1e-12",
        kappa_1_interval=_decimal_pair(kappa_1),
        kappa_3_interval=_decimal_pair(kappa_3),
        linearized_delayed_gain_interval=_decimal_pair(delayed_gain),
        linearized_current_growth_interval=_decimal_pair(current_growth),
        spectral_small_gain_margin_lower=spectral_margin_text,
        decimal_precision_digits=decimal_recomposition.precision_digits,
        decimal_recomposed_spectral_margin_lower=(
            decimal_recomposition.spectral_margin_lower
        ),
        positive_cubic_secant_upper="3",
        negative_cubic_secant_upper="7",
        positive_channel_growth_lower=_down(positive_growth.lower),
        negative_channel_growth_lower=_down(negative_growth.lower),
        reset_projection_lower=_down(reset_projection.lower),
        transverse_coefficient_upper=_up(transverse_coefficient.upper),
        halanay_local_decay_lower=_down(local_decay.lower),
        halanay_delayed_gain_upper=_up(transverse_delayed.upper),
        halanay_margin_lower=halanay_margin_text,
        halanay_rate_candidate="0.03",
        halanay_rate_residual_lower=rate_residual_text,
        decimal_recomposed_halanay_margin_lower=(
            decimal_recomposition.halanay_margin_lower
        ),
        decimal_recomposed_halanay_rate_residual_lower=(
            decimal_recomposition.rate_residual_lower
        ),
        reset_voltage_interval=("-1", "1"),
        channel_faces=("-1", "1"),
        positive_hit_time_formula="T_+(r) <= log(1/r)/c_+, 0<r<1",
        negative_hit_time_formula="T_-(r) <= log(1/abs(r))/c_-, -1<r<0",
        source_periodic_branch_validated=True,
        source_unique_extrema_validated=True,
        source_response_derivative_box_validated=True,
        same_synchronous_baseline_and_gain_box_validated=True,
        full_network_d3_e2_instance_fixed_by_this_certificate=True,
        source_periodic_artifact_certifies_full_network_scaffolds=False,
        full_network_collective_projection_exact=True,
        physical_collective_recovery_actuator_exact=True,
        actuator_has_zero_transverse_projection_exact=True,
        controlled_collective_recovery_leaf_invariant_exact=True,
        constant_history_delayed_actuation_vanishes_exactly=True,
        constant_history_scaffolds_vanish_exactly=True,
        collective_recovery_clamp_identity_exact=True,
        zero_reset_is_exact_clamped_equilibrium=True,
        one_simple_rhp_characteristic_root_validated=True,
        no_imaginary_characteristic_roots_validated=True,
        positive_channel_capture_validated=True,
        negative_channel_capture_validated=True,
        reset_projection_transversality_validated=True,
        arbitrary_two_module_sizes_linear_variational_transverse_decay_during_clamped_decision_validated=True,
        controlled_operational_onset_validated=True,
        reset_family_complete_history_threshold_validated=True,
        controlled_clamped_complete_history_stable_manifold_validated=True,
        quantified_noisy_history_capture_validated=False,
        nonlinear_transverse_synchronization_during_clamped_decision_validated=False,
        periodic_full_network_transverse_stability_validated=False,
        unforced_complete_history_stable_manifold_validated=False,
        unforced_onset_validated=False,
        maximal_canard_onset_validated=False,
        periodic_orbit_attraction_validated=False,
        general_network_topology_validated=False,
        issue_15_closed=False,
    )


def x_polynomial_positive() -> sp.Expr:
    """Return the exact positive-side cubic secant polynomial."""

    x = sp.Symbol("x", real=True)
    return x**2 - 3 * x + 3


def u_polynomial_negative() -> sp.Expr:
    """Return the exact negative-side cubic secant polynomial."""

    u = sp.Symbol("u", nonnegative=True)
    return u**2 + 3 * u + 3


def load_same_model_separator(
    path: str | Path,
    *,
    expected_sha256: str = TRACKED_PARAMETER_BOX_SHA256,
    precision: int = 160,
) -> SameModelSeparatorCertificate:
    """Hash-check a parameter-box artifact and derive the certificate."""

    source = Path(path)
    raw = source.read_bytes()
    digest = sha256(raw).hexdigest()
    if digest != expected_sha256:
        raise ValueError(
            "parameter-box result SHA-256 mismatch: "
            f"expected {expected_sha256}, got {digest}"
        )
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as error:
        raise ValueError("parameter-box result is not valid JSON") from error
    return same_model_separator_from_payload(
        payload,
        source_result_sha256=digest,
        precision=precision,
    )


def validate_same_model_separator_result_payload(
    payload: Mapping[str, Any],
) -> None:
    """Refuse missing or promoted claims in a generated result record.

    This semantic check complements, rather than replaces, a byte hash.  It
    is intentionally strict: every negative scope flag must be present and
    exactly false, so deleting a limitation cannot silently widen the claim.
    """

    root = _mapping(payload, "result payload")
    provenance = _mapping(root.get("provenance"), "provenance")
    source = _mapping(root.get("source_evidence"), "source_evidence")
    certificate = _mapping(root.get("certificate"), "certificate")
    scope = _mapping(root.get("scope"), "scope")
    if provenance.get("arithmetic") != (
        "exact symbolic identities and MPFR directed endpoints"
    ):
        raise ValueError("result arithmetic provenance is missing or invalid")
    source_digest = source.get("parameter_box_result_sha256")
    if source_digest != certificate.get("source_result_sha256"):
        raise ValueError("result and certificate source digests disagree")
    if source_digest != TRACKED_PARAMETER_BOX_SHA256:
        raise ValueError("result is not bound to the tracked parameter box")
    if source.get("source_synchronous_model") != SYNCHRONOUS_MODEL_ID:
        raise ValueError("result synchronous model identifier is invalid")
    if certificate.get("source_synchronous_model_id") != SYNCHRONOUS_MODEL_ID:
        raise ValueError("certificate synchronous model identifier is invalid")
    if certificate.get("certified_full_network_instance_id") != (
        FULL_NETWORK_INSTANCE_ID
    ):
        raise ValueError("certificate full-network instance identifier is invalid")
    parameters = _mapping(
        source.get("periodic_synchronous_parameters"),
        "source_evidence.periodic_synchronous_parameters",
    )
    expected_parameters: Mapping[str, object] = {
        "epsilon": "1/5",
        "unfolding": "3/5",
        "theta_0": "4",
        "theta_1": "5",
        "gain_center": ["1/5", "1/4"],
    }
    if dict(parameters) != dict(expected_parameters):
        raise ValueError(
            "result synchronous baseline parameters are missing or invalid"
        )
    _require_false(
        source, "source_periodic_artifact_certifies_full_network_scaffolds"
    )
    full_instance = _mapping(
        source.get("full_network_instance_fixed_by_separator_certificate"),
        "source_evidence.full_network_instance",
    )
    expected_instance: Mapping[str, object] = {
        "instance_id": FULL_NETWORK_INSTANCE_ID,
        "network_class": "rank-one two-module dual-scaffold",
        "voltage_scaffold": "3",
        "recovery_scaffold": "2",
        "collective_projection": "pi*x=(bar(x)_1+bar(x)_2)/2",
        "recovery_actuator": "u_i^w=-epsilon*(pi*v-unfolding)",
    }
    if dict(full_instance) != dict(expected_instance):
        raise ValueError("result full-network instance is missing or invalid")
    if source.get("decision_protocol") != DECISION_PROTOCOL:
        raise ValueError("result decision protocol is missing or invalid")
    if source.get("controlled_complete_history_phase_space") != (
        CONTROLLED_PHASE_SPACE
    ):
        raise ValueError(
            "result controlled complete-history phase space is missing or invalid"
        )
    _require_true(
        source, "reset_only_controller_absent_from_baseline_periodic_rfde"
    )

    for flag in (
        "source_periodic_branch_validated",
        "source_unique_extrema_validated",
        "source_response_derivative_box_validated",
        "same_synchronous_baseline_and_gain_box_validated",
        "full_network_d3_e2_instance_fixed_by_this_certificate",
        "full_network_collective_projection_exact",
        "physical_collective_recovery_actuator_exact",
        "actuator_has_zero_transverse_projection_exact",
        "controlled_collective_recovery_leaf_invariant_exact",
        "constant_history_delayed_actuation_vanishes_exactly",
        "constant_history_scaffolds_vanish_exactly",
        "collective_recovery_clamp_identity_exact",
        "zero_reset_is_exact_clamped_equilibrium",
        "one_simple_rhp_characteristic_root_validated",
        "no_imaginary_characteristic_roots_validated",
        "positive_channel_capture_validated",
        "negative_channel_capture_validated",
        "reset_projection_transversality_validated",
        "arbitrary_two_module_sizes_linear_variational_transverse_decay_during_clamped_decision_validated",
        "controlled_operational_onset_validated",
        "reset_family_complete_history_threshold_validated",
        "controlled_clamped_complete_history_stable_manifold_validated",
    ):
        _require_true(certificate, flag)
    for flag in (
        "source_periodic_artifact_certifies_full_network_scaffolds",
        "quantified_noisy_history_capture_validated",
        "nonlinear_transverse_synchronization_during_clamped_decision_validated",
        "periodic_full_network_transverse_stability_validated",
        "unforced_complete_history_stable_manifold_validated",
        "unforced_onset_validated",
        "maximal_canard_onset_validated",
        "periodic_orbit_attraction_validated",
        "general_network_topology_validated",
        "issue_15_closed",
    ):
        _require_false(certificate, flag)

    for flag in (
        "same_synchronous_baseline_and_gain_box",
        "full_network_d3_e2_instance_fixed_by_separator_certificate",
        "full_network_collective_clamp_exact",
        "controlled_operational_first_hit_onset",
        "reset_family_complete_history_threshold",
        "controlled_clamped_complete_history_stable_manifold",
        "arbitrary_two_module_sizes_linear_variational_transverse_decay_during_clamped_decision",
    ):
        _require_true(scope, flag)
    for flag in (
        "source_periodic_artifact_certifies_full_network_scaffolds",
        "quantified_noisy_history_capture",
        "nonlinear_transverse_synchronization_during_clamped_decision",
        "periodic_full_network_transverse_stability",
        "unforced_complete_history_stable_manifold",
        "unforced_onset",
        "maximal_canard_onset",
        "periodic_orbit_attraction",
        "general_network_topology",
        "biological_pulse_or_quiet_basin_capture_beyond_channel_faces",
        "issue_15_closed",
    ):
        _require_false(scope, flag)


def load_same_model_separator_result(
    path: str | Path,
    *,
    expected_sha256: str,
) -> Mapping[str, Any]:
    """Hash-check and semantically validate a generated result record."""

    if not isinstance(expected_sha256, str) or len(expected_sha256) != 64:
        raise ValueError("expected_sha256 must be a 64-character digest")
    result_path = Path(path)
    raw = result_path.read_bytes()
    digest = sha256(raw).hexdigest()
    if digest != expected_sha256:
        raise ValueError(
            "same-model separator result SHA-256 mismatch: "
            f"expected {expected_sha256}, got {digest}"
        )
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as error:
        raise ValueError("same-model separator result is not valid JSON") from error
    validate_same_model_separator_result_payload(payload)
    return payload
