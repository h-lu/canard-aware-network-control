"""Exact diagnostics for the unforced drifting-saddle obstruction.

The causal reset releases the collective recovery coordinate instead of
holding it fixed.  Close to a saddle-type separator, an unstable coordinate
needs logarithmically long fast time to reach a fixed exit face.  During that
time the collective recovery coordinate drifts by ``epsilon`` times the exit
time.  Consequently fixed-layer passage blocks cannot classify every
nonzero reset offset, even when an exact finite-dimensional saddle trajectory
and a unique codimension-one separator are already available.

The model checked here is an ODE, hence an RFDE whose functional ignores its
history, for every declared delay length.  It is a logical counterexample to
deriving the full unforced Gate R-S from a low-dimensional graph, a local
stable foliation, and fixed-fast-time channel persistence alone.  It is not a
counterexample to the full physical FitzHugh--Nagumo RFDE after an additional
global exchange-and-return theorem has been proved.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, isfinite, log


@dataclass(frozen=True)
class DriftingSaddlePassage:
    """Exact passage data for ``u'=lambda*u, rho'=epsilon*drift``."""

    exit_time: float
    recovery_displacement: float
    recovery_tube_half_width: float
    reaches_fixed_layer_block: bool


def drifting_saddle_passage(
    *,
    epsilon: float,
    unstable_rate: float,
    drift_magnitude: float,
    exit_coordinate: float,
    reset_offset: float,
    layer_tube_constant: float,
) -> DriftingSaddlePassage:
    r"""Return the exact first passage data for the drifting saddle normal form.

    The current-state equations are

    ``u' = unstable_rate*u`` and
    ``rho' = epsilon*drift_magnitude``.

    A reset starts at ``u(0)=reset_offset`` and ``rho(0)=rho_0``.  The
    relevant signed exit face is ``|u|=exit_coordinate``.  Its fixed-layer
    recovery window is

    ``|rho-rho_0| < layer_tube_constant*epsilon``.

    The function assumes ``0 < |reset_offset| < exit_coordinate``.  The
    recovery tube is open, as in the physical passage cylinders.
    """

    values = (
        epsilon,
        unstable_rate,
        drift_magnitude,
        exit_coordinate,
        reset_offset,
        layer_tube_constant,
    )
    if not all(isfinite(float(value)) for value in values):
        raise ValueError("all drifting-saddle data must be finite")
    if epsilon <= 0.0:
        raise ValueError("epsilon must be positive")
    if unstable_rate <= 0.0:
        raise ValueError("unstable rate must be positive")
    if drift_magnitude <= 0.0:
        raise ValueError("drift magnitude must be positive")
    if exit_coordinate <= 0.0:
        raise ValueError("exit coordinate must be positive")
    if layer_tube_constant <= 0.0:
        raise ValueError("layer tube constant must be positive")
    offset = abs(reset_offset)
    if not 0.0 < offset < exit_coordinate:
        raise ValueError(
            "require 0 < abs(reset_offset) < exit_coordinate"
        )

    exit_time = log(exit_coordinate / offset) / unstable_rate
    displacement = epsilon * drift_magnitude * exit_time
    half_width = layer_tube_constant * epsilon
    return DriftingSaddlePassage(
        exit_time=exit_time,
        recovery_displacement=displacement,
        recovery_tube_half_width=half_width,
        reaches_fixed_layer_block=displacement < half_width,
    )


def fixed_layer_miss_cutoff(
    *,
    unstable_rate: float,
    drift_magnitude: float,
    exit_coordinate: float,
    layer_tube_constant: float,
) -> float:
    r"""Return the exact punctured interval missed by fixed-layer blocks.

    For the normal form in :func:`drifting_saddle_passage`, every nonzero
    reset offset satisfying

    ``|a| <= exit_coordinate*exp(-unstable_rate*layer_tube_constant/drift)``

    leaves the recovery tube before reaching its signed exit face.  Notice
    that ``epsilon`` cancels because the tube itself has width ``O(epsilon)``.
    """

    log_cutoff = log_fixed_layer_miss_cutoff(
        unstable_rate=unstable_rate,
        drift_magnitude=drift_magnitude,
        exit_coordinate=exit_coordinate,
        layer_tube_constant=layer_tube_constant,
    )
    cutoff = exp(log_cutoff)
    if cutoff == 0.0:
        raise OverflowError(
            "fixed-layer cutoff underflows in binary64; use "
            "log_fixed_layer_miss_cutoff"
        )
    return cutoff


def log_fixed_layer_miss_cutoff(
    *,
    unstable_rate: float,
    drift_magnitude: float,
    exit_coordinate: float,
    layer_tube_constant: float,
) -> float:
    r"""Return the natural logarithm of the fixed-layer miss cutoff.

    This logarithmic form remains finite when the positive cutoff itself is
    smaller than the binary64 range.
    """

    values = (
        unstable_rate,
        drift_magnitude,
        exit_coordinate,
        layer_tube_constant,
    )
    if not all(isfinite(float(value)) for value in values):
        raise ValueError("all fixed-layer cutoff data must be finite")
    if unstable_rate <= 0.0:
        raise ValueError("unstable rate must be positive")
    if drift_magnitude <= 0.0:
        raise ValueError("drift magnitude must be positive")
    if exit_coordinate <= 0.0:
        raise ValueError("exit coordinate must be positive")
    if layer_tube_constant <= 0.0:
        raise ValueError("layer tube constant must be positive")
    return log(exit_coordinate) - (
        unstable_rate * layer_tube_constant / drift_magnitude
    )


def exponential_offset_recovery_displacement(
    *,
    epsilon: float,
    action: float,
    unstable_rate: float,
    drift_magnitude: float,
    exit_coordinate: float,
) -> float:
    r"""Return the drift at exit for the offset ``exp(-action/epsilon)``.

    The exact identity is

    ``Delta rho = drift/unstable_rate * action``
    ``            + epsilon*drift/unstable_rate*log(exit_coordinate)``.

    Hence the recovery displacement tends to the nonzero order-one limit
    ``drift_magnitude*action/unstable_rate`` as ``epsilon`` tends to zero.
    The calculation is performed in logarithmic form and does not construct
    the exponentially small offset numerically.
    """

    values = (
        epsilon,
        action,
        unstable_rate,
        drift_magnitude,
        exit_coordinate,
    )
    if not all(isfinite(float(value)) for value in values):
        raise ValueError("all exponential-offset data must be finite")
    if epsilon <= 0.0:
        raise ValueError("epsilon must be positive")
    if action <= 0.0:
        raise ValueError("action must be positive")
    if unstable_rate <= 0.0:
        raise ValueError("unstable rate must be positive")
    if drift_magnitude <= 0.0:
        raise ValueError("drift magnitude must be positive")
    if exit_coordinate <= 0.0:
        raise ValueError("exit coordinate must be positive")
    if action + epsilon * log(exit_coordinate) <= 0.0:
        raise ValueError(
            "the exponential reset offset must lie strictly inside the "
            "exit face"
        )
    return (
        drift_magnitude * action / unstable_rate
        + epsilon
        * drift_magnitude
        * log(exit_coordinate)
        / unstable_rate
    )
