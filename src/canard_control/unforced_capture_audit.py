"""Capture diagnostics and exact counterexamples for Paper III Gate U-CAP.

This module deliberately separates three statements.

* ``middle_tracker_detector_audit`` locates the declared pulse level on the
  physical singular middle branch.  It shows that a trajectory which shadows
  the middle branch to the lower fold meets that voltage level a fixed slow
  distance away from the old reset-layer passage cylinder.
* ``saturating_channel_capture_audit`` solves an exact ODE (and hence RFDE
  subclass) with a simple separator and two attracting channels.  Slow drift
  makes a punctured interval of nonzero offsets miss both fixed-layer target
  sections.  Thus two channels plus a fold/event coordinate do not imply the
  old all-offset first-hit claim.
* ``deadband_capture_time_bound`` records the finite-time bound recovered
  after imposing a nonzero outgoing deadband.  It is the scale needed by a
  finite chain of complete-history isolating cylinders.

The routines are proof diagnostics.  They do not integrate the full delayed
FitzHugh--Nagumo RFDE and do not certify its still-open fold map or biological
capture gate.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, isfinite, log, sqrt

from scipy.optimize import brentq

from .physical_pulse_bridge import (
    critical_point,
    equilibria_at_recovery,
    fold_points,
)


@dataclass(frozen=True)
class PhysicalDetectorDriftAudit:
    """Location of one voltage level on the physical middle branch."""

    reset_collective_recovery: float
    pulse_level: float
    reset_middle_level: float
    fold_level: float
    crossing_a: float
    crossing_collective_recovery: float
    recovery_displacement: float

    def outside_fixed_recovery_tube(
        self, *, epsilon: float, tube_factor: float
    ) -> bool:
        """Whether the crossing is outside ``tube_factor*epsilon``."""

        _require_positive_finite("epsilon", epsilon)
        _require_positive_finite("tube_factor", tube_factor)
        return self.recovery_displacement > tube_factor * epsilon


@dataclass(frozen=True)
class SaturatingChannelCaptureAudit:
    """Exact first-section data for the saturating two-channel ODE."""

    epsilon: float
    initial_offset: float
    target_radius: float
    recovery_tube_factor: float
    slow_drift_speed: float
    hit_time: float
    recovery_displacement: float
    critical_absolute_offset: float
    assigned_channel: str
    fixed_layer_target_hit: bool


def _require_positive_finite(name: str, value: float) -> None:
    if not isfinite(float(value)) or float(value) <= 0.0:
        raise ValueError(f"{name} must be positive and finite")


def middle_tracker_detector_audit(
    *,
    reset_collective_recovery: float = -0.5,
    pulse_level: float = 1.4,
) -> PhysicalDetectorDriftAudit:
    r"""Locate ``H=-xi=pulse_level`` on the singular middle branch.

    The branch is followed from the reset layer toward the physical lower
    fold.  The level must lie strictly between its reset and fold values.
    Its recovery displacement is independent of ``epsilon``; consequently it
    eventually lies outside every old fixed-layer tube of width
    ``c_out*epsilon``.
    """

    if not all(
        isfinite(float(value))
        for value in (reset_collective_recovery, pulse_level)
    ):
        raise ValueError("detector data must be finite")
    if pulse_level <= 0.0:
        raise ValueError("pulse_level must be positive")

    lower_fold, upper_fold = fold_points()
    rho_reset = float(reset_collective_recovery)
    if not lower_fold.collective_recovery < rho_reset < (
        upper_fold.collective_recovery
    ):
        raise ValueError("reset recovery must lie between the folds")

    equilibria = equilibria_at_recovery(rho_reset)
    if len(equilibria) != 3:
        raise RuntimeError("reset layer is not bistable")
    middle = equilibria[1]
    reset_level = -middle.critical_voltage
    fold_level = -lower_fold.critical_voltage
    target = float(pulse_level)
    if not reset_level < target < fold_level:
        raise ValueError(
            "pulse_level must lie strictly between the reset-middle and "
            "lower-fold levels"
        )

    crossing_a = brentq(
        lambda a: critical_point(a).critical_voltage + target,
        lower_fold.a,
        middle.a,
        xtol=1.0e-14,
        rtol=1.0e-14,
    )
    crossing = critical_point(crossing_a)
    displacement = abs(crossing.collective_recovery - rho_reset)
    return PhysicalDetectorDriftAudit(
        reset_collective_recovery=rho_reset,
        pulse_level=target,
        reset_middle_level=reset_level,
        fold_level=fold_level,
        crossing_a=float(crossing_a),
        crossing_collective_recovery=(
            crossing.collective_recovery
        ),
        recovery_displacement=float(displacement),
    )


def saturating_channel_hit_time(
    *, initial_offset: float, target_radius: float
) -> float:
    r"""Return the exact hit time for ``z'=z*(1-z**2)``.

    For ``0<abs(z_0)<R<1``, the first hit of ``z=sign(z_0)*R`` is

    ``0.5*log(R**2*(1-z_0**2)/(z_0**2*(1-R**2)))``.

    The equilibrium ``z=0`` is the separator and ``z=+/-1`` are the two
    attracting channels.
    """

    if not isfinite(float(initial_offset)) or initial_offset == 0.0:
        raise ValueError("initial_offset must be finite and nonzero")
    _require_positive_finite("target_radius", target_radius)
    absolute_offset = abs(float(initial_offset))
    radius = float(target_radius)
    if not absolute_offset < radius < 1.0:
        raise ValueError("require 0 < abs(initial_offset) < target_radius < 1")
    ratio = (
        radius**2
        * (1.0 - absolute_offset**2)
        / (absolute_offset**2 * (1.0 - radius**2))
    )
    return 0.5 * log(ratio)


def fixed_layer_capture_critical_offset(
    *,
    target_radius: float,
    recovery_tube_factor: float,
    slow_drift_speed: float = 1.0,
) -> float:
    r"""Return the exact all-offset cutoff for a fixed recovery tube.

    In the counterexample

    ``z'=z*(1-z**2)``, ``rho'=-epsilon*c``,

    the target is accepted only while
    ``abs(rho-rho_0)<epsilon*h``.  The critical initial magnitude is

    ``R/sqrt(R**2+(1-R**2)*exp(2*h/c))``.

    Every smaller nonzero magnitude misses both target sections forever.
    """

    _require_positive_finite("target_radius", target_radius)
    _require_positive_finite("recovery_tube_factor", recovery_tube_factor)
    _require_positive_finite("slow_drift_speed", slow_drift_speed)
    radius = float(target_radius)
    if radius >= 1.0:
        raise ValueError("target_radius must be smaller than one")
    exponent = 2.0 * float(recovery_tube_factor) / float(slow_drift_speed)
    return radius / sqrt(
        radius**2 + (1.0 - radius**2) * exp(exponent)
    )


def saturating_channel_capture_audit(
    *,
    epsilon: float,
    initial_offset: float,
    target_radius: float = 0.5,
    recovery_tube_factor: float = 1.0,
    slow_drift_speed: float = 1.0,
) -> SaturatingChannelCaptureAudit:
    r"""Audit capture by fixed-layer sections in the exact ODE subclass.

    At the channel-section hit, the slow recovery displacement is
    ``epsilon*c*T_hit``.  The target is counted only if that displacement is
    strictly smaller than ``epsilon*h``.  Because recovery is monotone and
    ``abs(z)`` increases through the target radius, a missed section can never
    be recovered later.
    """

    _require_positive_finite("epsilon", epsilon)
    _require_positive_finite("recovery_tube_factor", recovery_tube_factor)
    _require_positive_finite("slow_drift_speed", slow_drift_speed)
    hit_time = saturating_channel_hit_time(
        initial_offset=initial_offset,
        target_radius=target_radius,
    )
    displacement = (
        float(epsilon) * float(slow_drift_speed) * hit_time
    )
    cutoff = fixed_layer_capture_critical_offset(
        target_radius=target_radius,
        recovery_tube_factor=recovery_tube_factor,
        slow_drift_speed=slow_drift_speed,
    )
    return SaturatingChannelCaptureAudit(
        epsilon=float(epsilon),
        initial_offset=float(initial_offset),
        target_radius=float(target_radius),
        recovery_tube_factor=float(recovery_tube_factor),
        slow_drift_speed=float(slow_drift_speed),
        hit_time=float(hit_time),
        recovery_displacement=float(displacement),
        critical_absolute_offset=float(cutoff),
        assigned_channel=("positive" if initial_offset > 0.0 else "negative"),
        fixed_layer_target_hit=bool(
            displacement
            < float(epsilon) * float(recovery_tube_factor)
        ),
    )


def deadband_capture_time_bound(
    *, deadband: float, target_radius: float
) -> float:
    """Worst exact channel hit time for ``deadband <= abs(z_0) < R``."""

    _require_positive_finite("deadband", deadband)
    _require_positive_finite("target_radius", target_radius)
    if not deadband < target_radius < 1.0:
        raise ValueError("require deadband < target_radius < one")
    return saturating_channel_hit_time(
        initial_offset=deadband,
        target_radius=target_radius,
    )
