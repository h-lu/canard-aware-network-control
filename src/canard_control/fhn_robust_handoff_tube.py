"""Robust finite-horizon shutdown tubes for balanced delayed FHN networks.

This module extends the exact synchronous autonomous-handoff certificate to
an open cylinder in the full RFDE history space.  The post-handoff trajectory
may be asynchronous, the handoff state and the remote delayed history may be
imperfect, the FHN parameters ``epsilon`` and ``a`` may vary in a declared
box, and both nominally closed additive inputs may leave a bounded residual.

The conclusion is deliberately finite-horizon: every voltage component keeps
the certified sign and the network enters an explicit terminal block near the
old synchronous landing face.  It is not a theorem about robust preparation,
permanent no-return, a biological action potential, a pulse basin, actuator
bandwidth, or delay uncertainty.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, localcontext
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Mapping

import gmpy2

from canard_control.directed_interval import decimal_lower, decimal_upper
from canard_control.fhn_autonomous_handoff_excursion import (
    TRACKED_BALANCED_CONTROL_CHAIN_SHA256,
    validate_autonomous_handoff_result_payload,
)


TRACKED_AUTONOMOUS_HANDOFF_SHA256 = (
    "38f612771fd5f7e50ffd4f77103ea680b447fd11a7af25cc5ccea95b9bf606f2"
)
MODEL_ID = "balanced-fhn-robust-finite-horizon-shutdown-tube"
ASSUMPTIONS_ID = (
    "finite-N-balanced-two-half-delay-layer-FHN;"
    "open-full-RFDE-handoff-cylinder;"
    "declared-kappa-epsilon-a-box;"
    "bounded-L-infinity-post-handoff-input-residual;"
    "fixed-delays-and-balanced-topology"
)

_STATE_RADIUS = Fraction(1, 10_000)
_REMOTE_HISTORY_RADIUS = Fraction(1, 10_000)
_VOLTAGE_RESIDUAL_BOUND = Fraction(1, 100_000)
_RECOVERY_RESIDUAL_BOUND = Fraction(1, 100_000)
_EPSILON_RADIUS = Fraction(1, 1_000_000)
_UNFOLDING_RADIUS = Fraction(1, 1_000_000)
_TUBE_RADIUS = Fraction(3, 5_000)

_EPSILON = Fraction(1, 5)
_UNFOLDING = Fraction(3, 5)
_EPSILON_UPPER = _EPSILON + _EPSILON_RADIUS
_KAPPA_1_UPPER = Fraction(200000000002, 10**12)
_KAPPA_3_UPPER = Fraction(250000000002, 10**12)

_ONE_SIDED_F_LIPSCHITZ_UPPER = Fraction(1, 50)
_DINI_RATE_UPPER = Fraction(21, 20)
_HISTORY_FORCING_COEFFICIENT_UPPER = Fraction(2, 5)
_REFERENCE_PARAMETER_COEFFICIENT_UPPER = Fraction(2)
_ABSOLUTE_VOLTAGE_ERROR_COEFFICIENT_UPPER = Fraction(10)

_POSITIVE_ROBUST_VELOCITY_LOWER = Fraction(131, 1_000)
_NEGATIVE_ROBUST_VELOCITY_MAGNITUDE_LOWER = Fraction(17, 250)

_POSITIVE_HORIZON = (
    "1.278339402787582773861681613826836042069901030142172264"
)
_NEGATIVE_HORIZON = (
    "0.4444584011141191698086150978017082389825931513417759996"
)
_POSITIVE_NOMINAL_VELOCITY = (
    "0.1372872269707499999999999999999999999999999999997965513"
)
_NEGATIVE_NOMINAL_VELOCITY = (
    "0.07484260258816079999999999999999999999999999999988048404"
)
_POSITIVE_NOMINAL_LANDING = (
    "0.1852127730287500000000000000000000000000000000002499532"
)
_NEGATIVE_NOMINAL_LANDING = (
    "0.1575073974086500000000000000000000000000000000002482193"
)
_MINIMUM_DELAY = (
    "8.944271909999158785636694674925104941762473438424472008"
)


@dataclass(frozen=True)
class RobustTubeAlgebraAudit:
    """Exact rational domination checks behind the max-norm tube."""

    one_sided_f_margin: Fraction
    remote_history_cubic_lipschitz_margin: Fraction
    current_f_absolute_lipschitz_margin: Fraction
    current_cubic_lipschitz_margin: Fraction
    delayed_history_coefficient_margin: Fraction
    instantaneous_linear_coefficient_margin: Fraction
    instantaneous_cubic_coefficient_margin: Fraction
    absolute_voltage_coefficient_margin: Fraction
    reference_parameter_coefficient_margin: Fraction
    recovery_parameter_state_margin: Fraction
    recovery_epsilon_coefficient_margin: Fraction
    dini_rate_margin: Fraction
    voltage_forcing_upper: Fraction
    recovery_forcing_upper: Fraction
    common_forcing_upper: Fraction
    voltage_field_perturbation_upper: Fraction


@dataclass(frozen=True)
class RobustHandoffTubeCertificate:
    """Public constants and strict scope for the robust shutdown tube."""

    autonomous_handoff_result_sha256: str
    balanced_control_chain_result_sha256: str
    precision_bits: int
    model_id: str
    assumptions_id: str
    kappa_1_open_interval: tuple[str, str]
    kappa_3_open_interval: tuple[str, str]
    epsilon_open_interval: tuple[str, str]
    unfolding_open_interval: tuple[str, str]
    current_handoff_state_radius: str
    remote_history_voltage_radius: str
    post_handoff_voltage_input_residual_bound: str
    post_handoff_recovery_input_residual_bound: str
    common_tracking_tube_radius: str
    gronwall_rate_upper: str
    common_forcing_upper: str
    minimum_delay_lower: str
    positive_nominal_horizon_upper: str
    negative_nominal_horizon_upper: str
    positive_tracking_error_upper: str
    negative_tracking_error_upper: str
    positive_tracking_slack_lower: str
    negative_tracking_slack_lower: str
    voltage_field_perturbation_upper: str
    positive_component_velocity_lower: str
    negative_component_velocity_magnitude_lower: str
    positive_capture_voltage_interval: tuple[str, str]
    negative_capture_voltage_interval: tuple[str, str]
    positive_capture_recovery_interval: tuple[str, str]
    negative_capture_recovery_interval: tuple[str, str]
    remote_history_window_definition: str
    exact_rational_coefficient_audit_validated: bool
    row_stochastic_scaffold_max_norm_dissipativity_validated: bool
    nonnegative_delay_layer_max_norm_bound_validated: bool
    full_rfde_open_handoff_cylinder_validated: bool
    asynchronous_finite_horizon_tracking_tube_validated: bool
    arbitrary_finite_balanced_topology_validated: bool
    declared_gain_perturbation_box_validated: bool
    epsilon_and_unfolding_perturbations_validated: bool
    bounded_shutdown_residual_inputs_validated: bool
    positive_robust_terminal_capture_validated: bool
    negative_robust_terminal_capture_validated: bool
    positive_componentwise_no_reversal_validated: bool
    negative_componentwise_no_reversal_validated: bool
    exact_synchrony_required: bool
    exact_zero_input_after_handoff_required: bool
    robust_history_preparation_validated: bool
    delay_perturbations_validated: bool
    permanent_no_return_validated: bool
    biological_action_potential_validated: bool
    quiet_or_pulse_basin_validated: bool
    landing_on_periodic_branch_validated: bool
    actuator_bandwidth_or_slew_rate_validated: bool
    hardware_validated: bool


def _mapping(value: object, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{name} must be a mapping")
    return value


def _f(value: Fraction) -> Fraction:
    return value - value**3 / 3


def _h(value: Fraction) -> Fraction:
    return (value - 1) ** 3


def robust_tube_algebra_audit() -> RobustTubeAlgebraAudit:
    """Recompute every rational coefficient used by the tube estimate."""

    # The bootstrap enclosure is the radius-R neighborhood of the two
    # nominal corridors [1,3/2] and [-6/5,-28/25].
    positive_left = Fraction(1) - _TUBE_RADIUS
    positive_right = Fraction(3, 2) + _TUBE_RADIUS
    negative_left = -Fraction(6, 5) - _TUBE_RADIUS

    one_sided_f_exact = 1 - positive_left**2
    one_sided_f_margin = _ONE_SIDED_F_LIPSCHITZ_UPPER - one_sided_f_exact

    history_distance = Fraction(3, 2) + _REMOTE_HISTORY_RADIUS
    history_cubic_lipschitz = 3 * history_distance**2
    history_cubic_margin = Fraction(7) - history_cubic_lipschitz

    current_f_lipschitz = max(
        abs(1 - positive_right**2),
        abs(1 - negative_left**2),
    )
    current_f_margin = Fraction(13, 10) - current_f_lipschitz

    current_h_distance = abs(negative_left - 1)
    current_h_lipschitz = 3 * current_h_distance**2
    current_h_margin = Fraction(15) - current_h_lipschitz

    delayed_history_coefficient = _EPSILON_UPPER * (
        _KAPPA_1_UPPER + 7 * _KAPPA_3_UPPER
    )
    delayed_history_margin = (
        _HISTORY_FORCING_COEFFICIENT_UPPER
        - delayed_history_coefficient
    )
    instantaneous_linear_coefficient = (
        _EPSILON_UPPER * _KAPPA_1_UPPER
    )
    instantaneous_linear_margin = (
        Fraction(41, 1_000) - instantaneous_linear_coefficient
    )
    instantaneous_cubic_coefficient = (
        _EPSILON_UPPER * _KAPPA_3_UPPER * 15
    )
    instantaneous_cubic_margin = (
        Fraction(4, 5) - instantaneous_cubic_coefficient
    )
    absolute_voltage_sum = (
        Fraction(13, 10)
        + 1
        + 6
        + Fraction(41, 1_000)
        + Fraction(4, 5)
    )
    absolute_voltage_margin = (
        _ABSOLUTE_VOLTAGE_ERROR_COEFFICIENT_UPPER
        - absolute_voltage_sum
    )

    positive_reference_parameter = (
        _KAPPA_1_UPPER + _KAPPA_3_UPPER / 4
    )
    negative_reference_parameter = (
        _KAPPA_1_UPPER * Fraction(7, 10)
        + _KAPPA_3_UPPER
        * abs(_h(-Fraction(1, 2)) - _h(-Fraction(6, 5)))
    )
    reference_parameter_margin = (
        _REFERENCE_PARAMETER_COEFFICIENT_UPPER
        - max(positive_reference_parameter, negative_reference_parameter)
    )
    recovery_parameter_state_margin = Fraction(2) - Fraction(9, 5)
    recovery_epsilon_margin = Fraction(201, 1_000) - _EPSILON_UPPER
    dini_rate_margin = _DINI_RATE_UPPER - (
        1 + _ONE_SIDED_F_LIPSCHITZ_UPPER
    )

    voltage_forcing = (
        _HISTORY_FORCING_COEFFICIENT_UPPER * _REMOTE_HISTORY_RADIUS
        + _REFERENCE_PARAMETER_COEFFICIENT_UPPER * _EPSILON_RADIUS
        + _VOLTAGE_RESIDUAL_BOUND
    )
    recovery_forcing = (
        _RECOVERY_RESIDUAL_BOUND
        + 2 * _EPSILON_RADIUS
        + Fraction(201, 1_000) * _UNFOLDING_RADIUS
    )
    common_forcing = Fraction(13, 250_000)
    voltage_field_perturbation = (
        _ABSOLUTE_VOLTAGE_ERROR_COEFFICIENT_UPPER * _TUBE_RADIUS
        + _HISTORY_FORCING_COEFFICIENT_UPPER * _REMOTE_HISTORY_RADIUS
        + _REFERENCE_PARAMETER_COEFFICIENT_UPPER * _EPSILON_RADIUS
        + _VOLTAGE_RESIDUAL_BOUND
    )

    strict_margins = (
        one_sided_f_margin,
        history_cubic_margin,
        current_f_margin,
        current_h_margin,
        delayed_history_margin,
        instantaneous_linear_margin,
        instantaneous_cubic_margin,
        absolute_voltage_margin,
        reference_parameter_margin,
        recovery_parameter_state_margin,
        recovery_epsilon_margin,
        dini_rate_margin,
    )
    if min(strict_margins) <= 0 or not (
        voltage_forcing <= common_forcing
        and recovery_forcing <= common_forcing
    ):
        raise RuntimeError("a robust-tube rational domination margin failed")
    if voltage_field_perturbation != Fraction(1513, 250_000):
        raise RuntimeError("the voltage field perturbation constant changed")

    return RobustTubeAlgebraAudit(
        one_sided_f_margin=one_sided_f_margin,
        remote_history_cubic_lipschitz_margin=history_cubic_margin,
        current_f_absolute_lipschitz_margin=current_f_margin,
        current_cubic_lipschitz_margin=current_h_margin,
        delayed_history_coefficient_margin=delayed_history_margin,
        instantaneous_linear_coefficient_margin=instantaneous_linear_margin,
        instantaneous_cubic_coefficient_margin=instantaneous_cubic_margin,
        absolute_voltage_coefficient_margin=absolute_voltage_margin,
        reference_parameter_coefficient_margin=reference_parameter_margin,
        recovery_parameter_state_margin=recovery_parameter_state_margin,
        recovery_epsilon_coefficient_margin=recovery_epsilon_margin,
        dini_rate_margin=dini_rate_margin,
        voltage_forcing_upper=voltage_forcing,
        recovery_forcing_upper=recovery_forcing,
        common_forcing_upper=common_forcing,
        voltage_field_perturbation_upper=voltage_field_perturbation,
    )


def _fraction_mpfr(
    value: Fraction, precision: int, rounding: int
) -> gmpy2.mpfr:
    with gmpy2.context(precision=precision, round=rounding):
        return gmpy2.mpfr(value.numerator) / gmpy2.mpfr(value.denominator)


def _tracking_bound_upper(horizon: str, precision: int) -> gmpy2.mpfr:
    """Directed upper bound for ``exp(LH)d+(exp(LH)-1)b/L``."""

    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        time = gmpy2.mpfr(horizon)
        rate = _fraction_mpfr(
            _DINI_RATE_UPPER, precision, gmpy2.RoundUp
        )
        reciprocal_rate = _fraction_mpfr(
            1 / _DINI_RATE_UPPER, precision, gmpy2.RoundUp
        )
        state = _fraction_mpfr(_STATE_RADIUS, precision, gmpy2.RoundUp)
        forcing = _fraction_mpfr(
            Fraction(13, 250_000), precision, gmpy2.RoundUp
        )
        growth = gmpy2.exp(rate * time)
        return growth * state + (growth - 1) * forcing * reciprocal_rate


def _public_tracking_data(
    horizon: str, precision: int
) -> tuple[str, str]:
    upper = decimal_upper(_tracking_bound_upper(horizon, precision), 55)
    with localcontext() as context:
        context.prec = 100
        slack = Decimal(_TUBE_RADIUS.numerator) / Decimal(
            _TUBE_RADIUS.denominator
        ) - Decimal(upper)
    if slack <= 0:
        raise RuntimeError("the robust tracking tube does not close")
    return upper, format(slack, "f")


def robust_handoff_tube_from_payload(
    payload: Mapping[str, Any],
    *,
    autonomous_handoff_result_sha256: str,
    precision: int = 160,
) -> RobustHandoffTubeCertificate:
    """Validate the frozen handoff theorem and derive its robust tube."""

    if autonomous_handoff_result_sha256 != TRACKED_AUTONOMOUS_HANDOFF_SHA256:
        raise ValueError("autonomous handoff result is not the tracked source")
    if (
        isinstance(precision, bool)
        or int(precision) != precision
        or int(precision) < 64
    ):
        raise ValueError("precision must be an integer of at least 64 bits")
    precision = int(precision)

    root = _mapping(payload, "autonomous handoff payload")
    validate_autonomous_handoff_result_payload(root)
    parent = _mapping(root.get("certificate"), "autonomous handoff certificate")
    if parent.get("balanced_control_chain_result_sha256") != (
        TRACKED_BALANCED_CONTROL_CHAIN_SHA256
    ):
        raise ValueError("the autonomous theorem has the wrong parent")

    expected_parent = {
        "positive_autonomous_excursion_time_upper": _POSITIVE_HORIZON,
        "negative_autonomous_excursion_time_upper": _NEGATIVE_HORIZON,
        "positive_autonomous_velocity_lower": _POSITIVE_NOMINAL_VELOCITY,
        "negative_autonomous_magnitude_velocity_lower": (
            _NEGATIVE_NOMINAL_VELOCITY
        ),
        "positive_autonomous_recovery_at_landing_upper": (
            _POSITIVE_NOMINAL_LANDING
        ),
        "negative_autonomous_recovery_magnitude_at_landing_upper": (
            _NEGATIVE_NOMINAL_LANDING
        ),
        "minimum_delay_lower": _MINIMUM_DELAY,
    }
    for name, expected in expected_parent.items():
        if parent.get(name) != expected:
            raise ValueError(f"tracked autonomous endpoint {name!r} changed")
    if not (
        Decimal(_POSITIVE_HORIZON) < Decimal(_MINIMUM_DELAY)
        and Decimal(_NEGATIVE_HORIZON) < Decimal(_MINIMUM_DELAY)
    ):
        raise RuntimeError("a remote-history window reaches the handoff time")

    audit = robust_tube_algebra_audit()
    positive_tracking, positive_slack = _public_tracking_data(
        _POSITIVE_HORIZON, precision
    )
    negative_tracking, negative_slack = _public_tracking_data(
        _NEGATIVE_HORIZON, precision
    )

    field_error = audit.voltage_field_perturbation_upper
    if not (
        Fraction(_POSITIVE_NOMINAL_VELOCITY) - field_error
        > _POSITIVE_ROBUST_VELOCITY_LOWER
        and Fraction(_NEGATIVE_NOMINAL_VELOCITY) - field_error
        > _NEGATIVE_ROBUST_VELOCITY_MAGNITUDE_LOWER
    ):
        raise RuntimeError("a robust componentwise velocity margin failed")

    with localcontext() as context:
        context.prec = 100
        radius = Decimal(_TUBE_RADIUS.numerator) / Decimal(
            _TUBE_RADIUS.denominator
        )
        positive_recovery_upper = Decimal(_POSITIVE_NOMINAL_LANDING) + radius
        negative_recovery_lower = -(
            Decimal(_NEGATIVE_NOMINAL_LANDING) + radius
        )

    return RobustHandoffTubeCertificate(
        autonomous_handoff_result_sha256=autonomous_handoff_result_sha256,
        balanced_control_chain_result_sha256=(
            TRACKED_BALANCED_CONTROL_CHAIN_SHA256
        ),
        precision_bits=precision,
        model_id=MODEL_ID,
        assumptions_id=ASSUMPTIONS_ID,
        kappa_1_open_interval=("0.199999999998", "0.200000000002"),
        kappa_3_open_interval=("0.249999999998", "0.250000000002"),
        epsilon_open_interval=("0.199999", "0.200001"),
        unfolding_open_interval=("0.599999", "0.600001"),
        current_handoff_state_radius="0.0001",
        remote_history_voltage_radius="0.0001",
        post_handoff_voltage_input_residual_bound="0.00001",
        post_handoff_recovery_input_residual_bound="0.00001",
        common_tracking_tube_radius="0.0006",
        gronwall_rate_upper="1.05",
        common_forcing_upper="0.000052",
        minimum_delay_lower=_MINIMUM_DELAY,
        positive_nominal_horizon_upper=_POSITIVE_HORIZON,
        negative_nominal_horizon_upper=_NEGATIVE_HORIZON,
        positive_tracking_error_upper=positive_tracking,
        negative_tracking_error_upper=negative_tracking,
        positive_tracking_slack_lower=positive_slack,
        negative_tracking_slack_lower=negative_slack,
        voltage_field_perturbation_upper="0.006052",
        positive_component_velocity_lower="0.131",
        negative_component_velocity_magnitude_lower="0.068",
        positive_capture_voltage_interval=("1.4994", "1.5006"),
        negative_capture_voltage_interval=("-1.2006", "-1.1994"),
        positive_capture_recovery_interval=(
            "-0.0006",
            format(positive_recovery_upper, "f"),
        ),
        negative_capture_recovery_interval=(
            format(negative_recovery_lower, "f"),
            "0.0006",
        ),
        remote_history_window_definition=(
            "I_{j,sigma}=[-tau_j,H_sigma-tau_j], j=0,1"
        ),
        exact_rational_coefficient_audit_validated=True,
        row_stochastic_scaffold_max_norm_dissipativity_validated=True,
        nonnegative_delay_layer_max_norm_bound_validated=True,
        full_rfde_open_handoff_cylinder_validated=True,
        asynchronous_finite_horizon_tracking_tube_validated=True,
        arbitrary_finite_balanced_topology_validated=True,
        declared_gain_perturbation_box_validated=True,
        epsilon_and_unfolding_perturbations_validated=True,
        bounded_shutdown_residual_inputs_validated=True,
        positive_robust_terminal_capture_validated=True,
        negative_robust_terminal_capture_validated=True,
        positive_componentwise_no_reversal_validated=True,
        negative_componentwise_no_reversal_validated=True,
        exact_synchrony_required=False,
        exact_zero_input_after_handoff_required=False,
        robust_history_preparation_validated=False,
        delay_perturbations_validated=False,
        permanent_no_return_validated=False,
        biological_action_potential_validated=False,
        quiet_or_pulse_basin_validated=False,
        landing_on_periodic_branch_validated=False,
        actuator_bandwidth_or_slew_rate_validated=False,
        hardware_validated=False,
    )


_TRUE_FIELDS = (
    "exact_rational_coefficient_audit_validated",
    "row_stochastic_scaffold_max_norm_dissipativity_validated",
    "nonnegative_delay_layer_max_norm_bound_validated",
    "full_rfde_open_handoff_cylinder_validated",
    "asynchronous_finite_horizon_tracking_tube_validated",
    "arbitrary_finite_balanced_topology_validated",
    "declared_gain_perturbation_box_validated",
    "epsilon_and_unfolding_perturbations_validated",
    "bounded_shutdown_residual_inputs_validated",
    "positive_robust_terminal_capture_validated",
    "negative_robust_terminal_capture_validated",
    "positive_componentwise_no_reversal_validated",
    "negative_componentwise_no_reversal_validated",
)

_FALSE_FIELDS = (
    "exact_synchrony_required",
    "exact_zero_input_after_handoff_required",
    "robust_history_preparation_validated",
    "delay_perturbations_validated",
    "permanent_no_return_validated",
    "biological_action_potential_validated",
    "quiet_or_pulse_basin_validated",
    "landing_on_periodic_branch_validated",
    "actuator_bandwidth_or_slew_rate_validated",
    "hardware_validated",
)


def validate_robust_handoff_tube_result_payload(
    payload: Mapping[str, Any],
) -> None:
    """Reject altered constants and unsupported biological promotions."""

    root = _mapping(payload, "robust tube result payload")
    source = _mapping(root.get("source_evidence"), "source_evidence")
    certificate = _mapping(root.get("certificate"), "certificate")
    scope = _mapping(root.get("scope"), "scope")
    if source.get("autonomous_handoff_result_sha256") != (
        TRACKED_AUTONOMOUS_HANDOFF_SHA256
    ):
        raise ValueError("source evidence is not bound to the tracked handoff")
    if source.get("balanced_control_chain_result_sha256") != (
        TRACKED_BALANCED_CONTROL_CHAIN_SHA256
    ):
        raise ValueError("source evidence is not bound to the preparation theorem")
    if certificate.get("autonomous_handoff_result_sha256") != (
        TRACKED_AUTONOMOUS_HANDOFF_SHA256
    ):
        raise ValueError("certificate is not bound to the tracked handoff")
    if certificate.get("balanced_control_chain_result_sha256") != (
        TRACKED_BALANCED_CONTROL_CHAIN_SHA256
    ):
        raise ValueError("certificate is not bound to the preparation theorem")
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

    exact_values: dict[str, object] = {
        "kappa_1_open_interval": ["0.199999999998", "0.200000000002"],
        "kappa_3_open_interval": ["0.249999999998", "0.250000000002"],
        "epsilon_open_interval": ["0.199999", "0.200001"],
        "unfolding_open_interval": ["0.599999", "0.600001"],
        "current_handoff_state_radius": "0.0001",
        "remote_history_voltage_radius": "0.0001",
        "post_handoff_voltage_input_residual_bound": "0.00001",
        "post_handoff_recovery_input_residual_bound": "0.00001",
        "common_tracking_tube_radius": "0.0006",
        "gronwall_rate_upper": "1.05",
        "common_forcing_upper": "0.000052",
        "minimum_delay_lower": _MINIMUM_DELAY,
        "positive_nominal_horizon_upper": _POSITIVE_HORIZON,
        "negative_nominal_horizon_upper": _NEGATIVE_HORIZON,
        "voltage_field_perturbation_upper": "0.006052",
        "positive_component_velocity_lower": "0.131",
        "negative_component_velocity_magnitude_lower": "0.068",
        "positive_capture_voltage_interval": ["1.4994", "1.5006"],
        "negative_capture_voltage_interval": ["-1.2006", "-1.1994"],
        "remote_history_window_definition": (
            "I_{j,sigma}=[-tau_j,H_sigma-tau_j], j=0,1"
        ),
    }
    for name, expected in exact_values.items():
        if certificate.get(name) != expected:
            raise ValueError(f"certificate field {name!r} is invalid")

    precision = certificate.get("precision_bits")
    if (
        isinstance(precision, bool)
        or not isinstance(precision, int)
        or precision < 64
    ):
        raise ValueError("certificate precision is invalid")
    audit = robust_tube_algebra_audit()
    expected_positive = Decimal(
        decimal_upper(_tracking_bound_upper(_POSITIVE_HORIZON, precision), 55)
    )
    expected_negative = Decimal(
        decimal_upper(_tracking_bound_upper(_NEGATIVE_HORIZON, precision), 55)
    )
    try:
        radius = Decimal(str(certificate["common_tracking_tube_radius"]))
        positive_tracking = Decimal(
            str(certificate["positive_tracking_error_upper"])
        )
        negative_tracking = Decimal(
            str(certificate["negative_tracking_error_upper"])
        )
        positive_slack = Decimal(
            str(certificate["positive_tracking_slack_lower"])
        )
        negative_slack = Decimal(
            str(certificate["negative_tracking_slack_lower"])
        )
        field_error = Decimal(
            str(certificate["voltage_field_perturbation_upper"])
        )
        positive_velocity = Decimal(
            str(certificate["positive_component_velocity_lower"])
        )
        negative_velocity = Decimal(
            str(
                certificate[
                    "negative_component_velocity_magnitude_lower"
                ]
            )
        )
        positive_recovery = tuple(
            Decimal(str(value))
            for value in certificate["positive_capture_recovery_interval"]
        )
        negative_recovery = tuple(
            Decimal(str(value))
            for value in certificate["negative_capture_recovery_interval"]
        )
    except Exception as error:
        raise ValueError("robust tube endpoints must be decimal") from error

    with localcontext() as context:
        context.prec = 100
        if not (
            positive_tracking >= expected_positive
            and negative_tracking >= expected_negative
            and positive_tracking < radius
            and negative_tracking < radius
            and 0 < positive_slack <= radius - positive_tracking
            and 0 < negative_slack <= radius - negative_tracking
        ):
            raise ValueError("public Gronwall tracking composition failed")
        if Fraction(field_error) < audit.voltage_field_perturbation_upper:
            raise ValueError("voltage field perturbation endpoint is too small")
        if not (
            Fraction(positive_velocity)
            <= Fraction(_POSITIVE_NOMINAL_VELOCITY) - Fraction(field_error)
            and Fraction(negative_velocity)
            <= Fraction(_NEGATIVE_NOMINAL_VELOCITY) - Fraction(field_error)
        ):
            raise ValueError("a robust velocity endpoint is too large")
        expected_positive_recovery = Decimal(_POSITIVE_NOMINAL_LANDING) + radius
        expected_negative_recovery = -(
            Decimal(_NEGATIVE_NOMINAL_LANDING) + radius
        )
        if not (
            positive_recovery[0] <= -radius
            and positive_recovery[1] >= expected_positive_recovery
            and negative_recovery[0] <= expected_negative_recovery
            and negative_recovery[1] >= radius
        ):
            raise ValueError("a terminal recovery interval is not outward safe")

    true_scope = (
        "declared_nearby_fhn_parameter_family",
        "full_rfde_open_handoff_cylinder",
        "asynchronous_finite_horizon_tracking_tube",
        "arbitrary_finite_balanced_topology",
        "bounded_post_handoff_shutdown_residual",
        "positive_and_negative_robust_terminal_capture",
        "componentwise_no_reversal_until_capture",
    )
    false_scope = (
        "robust_history_preparation",
        "all_additive_inputs_exactly_zero_after_handoff",
        "delay_perturbations",
        "permanent_no_return",
        "biological_action_potential",
        "quiet_or_pulse_basin",
        "landing_on_periodic_branch",
        "actuator_bandwidth_or_slew_rate",
        "hardware",
    )
    for name in true_scope:
        if scope.get(name) is not True:
            raise ValueError(f"scope flag {name!r} must be true")
    for name in false_scope:
        if scope.get(name) is not False:
            raise ValueError(f"scope flag {name!r} must be false")


def load_robust_handoff_tube_result(
    path: str | Path,
    *,
    expected_sha256: str | None = None,
) -> Mapping[str, Any]:
    """Hash-check and validate a stored robust-tube result."""

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
        raise ValueError("robust tube result is not valid UTF-8 JSON") from error
    root = _mapping(payload, "robust tube result payload")
    validate_robust_handoff_tube_result_payload(root)
    return root
