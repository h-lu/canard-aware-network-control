"""Sharp scale audits for the physical U-OUT terminal match.

The local right-fold construction suppresses prepared endpoint data by a
Gaussian factor on a logarithmic chart.  For a fixed chart exponent ``p``
this factor is algebraic, ``exp(-S_delta**2/2)=delta**p``.  A tracker over a
fixed repelling slow interval instead requires an action-scale residual of
order ``exp(-A/delta**2)``.

This module compares those scales in logarithms and records the independent
parameter-jet budget for a terminal implicit-function argument.  It does not
construct a physical RFDE boundary-value family.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import cos, exp, isfinite, log, sin, sqrt
import sys


@dataclass(frozen=True)
class LogTubeActionAudit:
    """Comparison of fixed-``p`` Gaussian suppression with an action scale."""

    delta: float
    logarithmic_power: float
    chart_radius: float
    physical_fold_radius: float
    log_local_residual_bound: float
    log_action_residual_target: float
    log_scale_ratio: float
    action_scale_certified: bool


@dataclass(frozen=True)
class TerminalRootJetBudget:
    """Value and parameter-derivative bounds for one scalar terminal root."""

    log_derivative_floor: float
    log_value_residual_bound: float
    log_parameter_residual_bound: float
    log_root_bound: float
    log_parameter_root_derivative_bound: float
    terminal_radius: float
    root_closes: bool


@dataclass(frozen=True)
class OscillatoryCompleteHistoryAudit:
    """Exact complete-history identities for the ODE-subclass counterexample."""

    current_mismatch: float
    history_sup_mismatch: float
    oldest_history_mismatch: float
    canonical_history_parameter_jet: float
    terminal_coordinate_parameter_jet: float


def logarithmic_tube_action_audit(
    *,
    delta: float,
    logarithmic_power: float,
    action: float,
    action_margin: float = 0.0,
    gaussian_loss_constant: float = 0.0,
    local_polynomial_loss: float = 0.0,
    action_polynomial_loss: float = 0.0,
    action_delay_loss: float = 0.0,
    local_prefactor: float = 1.0,
    action_prefactor: float = 1.0,
) -> LogTubeActionAudit:
    r"""Compare a fixed logarithmic fold chart with the outer action target.

    Put ``ell=log(1/delta)`` and

    ``S_delta=sqrt(2*p*ell)``.

    The local estimate audited here is

    ``C_loc delta**(p-M_loc) exp(c*S_delta)``,

    while the required action-supercritical ceiling is

    ``C_act delta**(-M_act)``
    ``      * exp(-(A+chi)/delta**2+L/delta)``.

    ``action_scale_certified`` is true only when the *displayed local upper
    bound* is already no larger than the displayed action target.  Failure
    does not prove that an exact physical residual is nonzero; it proves that
    the fixed-``p`` estimate alone cannot certify the needed scale.
    """

    values = (
        delta,
        logarithmic_power,
        action,
        action_margin,
        gaussian_loss_constant,
        local_polynomial_loss,
        action_polynomial_loss,
        action_delay_loss,
        local_prefactor,
        action_prefactor,
    )
    if not all(isfinite(float(value)) for value in values):
        raise ValueError("all logarithmic/action data must be finite")
    if not 0.0 < delta < 1.0:
        raise ValueError("delta must lie in (0,1)")
    if delta < 1.0 / sys.float_info.max:
        raise ValueError(
            "delta is too small for binary64 reciprocal arithmetic; "
            "use an arbitrary-precision logarithmic audit"
        )
    if logarithmic_power <= 0.0:
        raise ValueError("logarithmic_power must be positive")
    if action <= 0.0:
        raise ValueError("action must be positive")
    if action_margin < 0.0:
        raise ValueError("action_margin must be nonnegative")
    if gaussian_loss_constant < 0.0:
        raise ValueError("gaussian_loss_constant must be nonnegative")
    if local_polynomial_loss < 0.0 or action_polynomial_loss < 0.0:
        raise ValueError("polynomial losses must be nonnegative")
    if action_delay_loss < 0.0:
        raise ValueError("action_delay_loss must be nonnegative")
    if local_prefactor <= 0.0 or action_prefactor <= 0.0:
        raise ValueError("prefactors must be positive")

    ell = -log(delta)
    chart_radius = sqrt(2.0 * logarithmic_power * ell)
    local_log = (
        log(local_prefactor)
        - (logarithmic_power - local_polynomial_loss) * ell
        + gaussian_loss_constant * chart_radius
    )
    inverse_delta = 1.0 / delta
    scaled_action = (action + action_margin) * inverse_delta
    if not isfinite(scaled_action):
        action_exponent = float("-inf")
    else:
        action_exponent = -inverse_delta * (
            scaled_action - action_delay_loss
        )
    action_log = (
        log(action_prefactor)
        + action_polynomial_loss * ell
        + action_exponent
    )
    ratio_log = local_log - action_log
    return LogTubeActionAudit(
        delta=float(delta),
        logarithmic_power=float(logarithmic_power),
        chart_radius=float(chart_radius),
        physical_fold_radius=float(delta * chart_radius),
        log_local_residual_bound=float(local_log),
        log_action_residual_target=float(action_log),
        log_scale_ratio=float(ratio_log),
        action_scale_certified=bool(ratio_log <= 0.0),
    )


def minimum_logarithmic_power_for_action_scale(
    *,
    delta: float,
    action: float,
    action_margin: float = 0.0,
    gaussian_loss_constant: float = 0.0,
    local_polynomial_loss: float = 0.0,
    action_polynomial_loss: float = 0.0,
    action_delay_loss: float = 0.0,
    local_prefactor: float = 1.0,
    action_prefactor: float = 1.0,
) -> float:
    r"""Return the nonnegative infimum of powers making the bound sufficient.

    The comparison is solved exactly as a quadratic in
    ``x=sqrt(p*log(1/delta))``.  In particular, for fixed losses,

    ``p_min ~ (action+action_margin)/(delta**2*log(1/delta))``.

    Thus no fixed chart power pays a positive outer action as
    ``delta -> 0``. A returned zero is an infimum: the audit itself still
    requires a strictly positive power. Small positive powers are admissible
    only when the Gaussian loss does not create a second positive threshold.
    """

    # Validate all shared inputs and obtain the target logarithm from any
    # positive trial power.  Only the target side is used below.
    trial = logarithmic_tube_action_audit(
        delta=delta,
        logarithmic_power=1.0,
        action=action,
        action_margin=action_margin,
        gaussian_loss_constant=gaussian_loss_constant,
        local_polynomial_loss=local_polynomial_loss,
        action_polynomial_loss=action_polynomial_loss,
        action_delay_loss=action_delay_loss,
        local_prefactor=local_prefactor,
        action_prefactor=action_prefactor,
    )
    ell = -log(delta)
    # local_log = log(C_loc)+M_loc*ell-x^2+c*sqrt(2)*x.
    required_drop = (
        log(local_prefactor)
        + local_polynomial_loss * ell
        - trial.log_action_residual_target
    )
    c_sqrt_two = gaussian_loss_constant * sqrt(2.0)
    if required_drop < 0.0:
        return 0.0
    if required_drop == 0.0:
        if c_sqrt_two == 0.0:
            return 0.0
        return float((c_sqrt_two * c_sqrt_two) / ell)
    x_min = 0.5 * (
        c_sqrt_two
        + sqrt(c_sqrt_two**2 + 4.0 * required_drop)
    )
    if not isfinite(x_min) or x_min > sqrt(sys.float_info.max):
        return float("inf")
    return float((x_min * x_min) / ell)


def terminal_root_jet_budget(
    *,
    log_derivative_floor: float,
    log_value_residual_bound: float,
    log_parameter_residual_bound: float,
    terminal_radius: float,
) -> TerminalRootJetBudget:
    r"""Audit the scalar root and its parameter derivative in logarithms.

    If ``|partial_beta m|>=d`` has one sign, ``|m(0,u)|<=r``, and at the
    selected root ``|D_u m(beta_*(u),u)|<=s``, then

    ``|beta_*|<=r/d`` and ``|D_u beta_*|<=s/d``.

    The value residual and parameter residual are independent hypotheses.
    In particular, an action-supercritical value residual does not control
    the parameter jet of the selected root.
    """

    derivative_log = float(log_derivative_floor)
    value_log = float(log_value_residual_bound)
    parameter_log = float(log_parameter_residual_bound)
    allowed_infinite = float("-inf")
    if not isfinite(derivative_log):
        raise ValueError("log_derivative_floor must be finite")
    if value_log != allowed_infinite and not isfinite(value_log):
        raise ValueError("value residual log must be finite or -inf")
    if parameter_log != allowed_infinite and not isfinite(parameter_log):
        raise ValueError("parameter residual log must be finite or -inf")
    if not isfinite(float(terminal_radius)) or terminal_radius <= 0.0:
        raise ValueError("terminal_radius must be positive and finite")

    root_log = (
        allowed_infinite
        if value_log == allowed_infinite
        else value_log - derivative_log
    )
    jet_log = (
        allowed_infinite
        if parameter_log == allowed_infinite
        else parameter_log - derivative_log
    )
    return TerminalRootJetBudget(
        log_derivative_floor=derivative_log,
        log_value_residual_bound=value_log,
        log_parameter_residual_bound=parameter_log,
        log_root_bound=float(root_log),
        log_parameter_root_derivative_bound=float(jet_log),
        terminal_radius=float(terminal_radius),
        root_closes=bool(root_log < log(float(terminal_radius))),
    )


def oscillatory_root_jet_log_bound(
    *,
    log_derivative: float,
    log_residual_amplitude: float,
    log_parameter_frequency: float,
) -> float:
    r"""Return ``log|D_u beta_*(0)|`` for an exact oscillatory mismatch.

    For

    ``m(beta,u)=d*beta+r*sin(omega*u)``,

    the unique root is ``beta_*=-(r/d)sin(omega*u)`` and

    ``|D_u beta_*(0)|=r*omega/d``.

    This gives a minimal exact counterexample to deriving a uniform root
    jet from a value-residual estimate alone.
    """

    values = (
        log_derivative,
        log_residual_amplitude,
        log_parameter_frequency,
    )
    if not all(isfinite(float(value)) for value in values):
        raise ValueError("all oscillatory mismatch logs must be finite")
    return float(
        log_residual_amplitude
        + log_parameter_frequency
        - log_derivative
    )


def oscillatory_complete_history_audit(
    *,
    delta: float,
    action: float,
    action_margin: float,
    delay_length: float,
    parameter: float,
    terminal_coordinate: float,
) -> OscillatoryCompleteHistoryAudit:
    r"""Evaluate the exact complete-history ODE-subclass counterexample.

    Take ``a(s)=action`` on an outer interval of length one and extend it
    across an incoming history buffer. The normal history shape is

    ``H(theta)=exp(-action/delta**2 + action*theta)``.

    Its sup norm on ``[-delay_length,0]`` is attained at the present time.
    The returned current mismatch therefore equals the full-history sup
    mismatch along the declared affine leaf. This direct-value helper rejects
    binary64 under/overflow; use the logarithmic helpers for asymptotically
    smaller ``delta``.
    """

    values = (
        delta,
        action,
        action_margin,
        delay_length,
        parameter,
        terminal_coordinate,
    )
    if not all(isfinite(float(value)) for value in values):
        raise ValueError("complete-history audit data must be finite")
    if not 0.0 < delta < 1.0:
        raise ValueError("delta must lie in (0,1)")
    if not action > action_margin > 0.0:
        raise ValueError("require action > action_margin > 0")
    if delay_length <= 0.0:
        raise ValueError("delay_length must be positive")

    epsilon = delta * delta
    if epsilon == 0.0:
        raise ValueError(
            "delta**2 underflows in binary64; use logarithmic helpers"
        )
    try:
        derivative = exp(-action / epsilon)
        residual = exp(-(action + action_margin) / epsilon)
        frequency = exp(2.0 * action_margin / epsilon)
    except OverflowError as error:
        raise ValueError(
            "complete-history values are not representable; use log helpers"
        ) from error
    if derivative == 0.0 or residual == 0.0 or not isfinite(frequency):
        raise ValueError(
            "complete-history values are not representable; use log helpers"
        )
    beta_can = -(residual / derivative) * sin(frequency * parameter)
    coefficient_difference = terminal_coordinate - beta_can
    current_mismatch = derivative * coefficient_difference
    oldest_shape = derivative * exp(-action * delay_length)
    cosine = abs(cos(frequency * parameter))
    return OscillatoryCompleteHistoryAudit(
        current_mismatch=float(current_mismatch),
        history_sup_mismatch=float(abs(coefficient_difference) * derivative),
        oldest_history_mismatch=float(
            abs(coefficient_difference) * oldest_shape
        ),
        canonical_history_parameter_jet=float(residual * frequency * cosine),
        terminal_coordinate_parameter_jet=float(
            (residual / derivative) * frequency * cosine
        ),
    )


def exp_if_representable(log_value: float) -> float:
    """Exponentiate a diagnostic log, allowing honest under/overflow."""

    value = float(log_value)
    if value == float("-inf"):
        return 0.0
    if not isfinite(value):
        raise ValueError("log_value must be finite or -inf")
    try:
        return float(exp(value))
    except OverflowError:
        return float("inf")
