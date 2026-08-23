"""Model-specific obstructions for the declared three-actuator FHN control.

The accompanying theorem note is ``docs/paper-iv-fhn-control-no-go.md``.
This module records only exact finite-network algebra, explicit Halanay
constants, and high-precision sharpness diagnostics.  It does not assert the
existence of a periodic FHN branch or of the physical pulse separator.
"""

from __future__ import annotations

from dataclasses import dataclass

import mpmath as mp
import numpy as np
import sympy as sp


@dataclass(frozen=True)
class TransverseLayerAudit:
    """Exact invariant-mode identities for the two-module delay layers."""

    module_sizes: tuple[int, int]
    within_layer: sp.Matrix
    cross_layer: sp.Matrix
    collective_vector: sp.Matrix
    module_difference_vector: sp.Matrix
    within_module_basis: sp.Matrix
    collective_same_residual: sp.Matrix
    collective_cross_residual: sp.Matrix
    difference_same_residual: sp.Matrix
    difference_cross_residual: sp.Matrix
    within_same_residual: sp.Matrix
    within_cross_residual: sp.Matrix


@dataclass(frozen=True)
class HalanayCertificate:
    """A sufficient full-network transverse stability certificate."""

    epsilon: float
    voltage_radius: float
    coefficient_bound: float
    local_decay: float
    delayed_gain: float
    margin: float
    maximal_physical_delay: float
    decay_rate: float

    @property
    def certified(self) -> bool:
        return self.margin > 0.0 and self.decay_rate > 0.0


@dataclass(frozen=True)
class TwoScaleNoGoBounds:
    """Upper bounds for physical and naturally scaled response moduli."""

    epsilon: float
    width: float
    safety_row_bound: float
    physical_layer_bound: float
    physical_combined_bound: float
    natural_scaled_layer_bound: float


@dataclass(frozen=True)
class SharpnessDiagnostic:
    """High-precision singular values of the canonical sheared response."""

    epsilon: mp.mpf
    width: mp.mpf
    safety_magnitude: mp.mpf
    physical_smallest_singular_value: mp.mpf
    physical_bound: mp.mpf
    physical_ratio: mp.mpf
    scaled_smallest_singular_value: mp.mpf
    scaled_bound: mp.mpf
    scaled_ratio: mp.mpf


def two_module_delay_layer_audit(
    first_module_size: int,
    second_module_size: int,
) -> TransverseLayerAudit:
    r"""Return the exact collective/difference/within-module decomposition.

    The matrices are the same-module and cross-module halves of the frozen
    row-stochastic matrix ``P``.  Their actions are

    ``B0 1=1/2 1``, ``B1 1=1/2 1``,
    ``B0 q=1/2 q``, ``B1 q=-1/2 q``, and ``Bk W=0``.
    """

    n_1 = int(first_module_size)
    n_2 = int(second_module_size)
    if n_1 < 1 or n_2 < 1:
        raise ValueError("module sizes must be positive")
    n_total = n_1 + n_2
    same = sp.zeros(n_total)
    cross = sp.zeros(n_total)
    modules = (range(0, n_1), range(n_1, n_total))
    sizes = (n_1, n_2)
    for receiver_module, receiver_indices in enumerate(modules):
        for receiver in receiver_indices:
            for source_module, source_indices in enumerate(modules):
                target = same if receiver_module == source_module else cross
                weight = sp.Rational(1, 2 * sizes[source_module])
                for source in source_indices:
                    target[receiver, source] = weight

    collective = sp.ones(n_total, 1)
    difference = sp.Matrix([1] * n_1 + [-1] * n_2)
    within_vectors: list[sp.Matrix] = []
    for start, size in ((0, n_1), (n_1, n_2)):
        for offset in range(1, size):
            vector = sp.zeros(n_total, 1)
            vector[start] = 1
            vector[start + offset] = -1
            within_vectors.append(vector)
    within_basis = (
        sp.Matrix.hstack(*within_vectors)
        if within_vectors
        else sp.zeros(n_total, 0)
    )

    return TransverseLayerAudit(
        module_sizes=(n_1, n_2),
        within_layer=same,
        cross_layer=cross,
        collective_vector=collective,
        module_difference_vector=difference,
        within_module_basis=within_basis,
        collective_same_residual=sp.simplify(same * collective - collective / 2),
        collective_cross_residual=sp.simplify(cross * collective - collective / 2),
        difference_same_residual=sp.simplify(same * difference - difference / 2),
        difference_cross_residual=sp.simplify(cross * difference + difference / 2),
        within_same_residual=sp.simplify(same * within_basis),
        within_cross_residual=sp.simplify(cross * within_basis),
    )


def transverse_mode_multiplicities(
    first_module_size: int,
    second_module_size: int,
) -> tuple[int, int, int]:
    """Return collective, module-difference, and within-mode multiplicities."""

    n_1 = int(first_module_size)
    n_2 = int(second_module_size)
    if n_1 < 1 or n_2 < 1:
        raise ValueError("module sizes must be positive")
    return 1, 1, n_1 + n_2 - 2


def transverse_halanay_certificate(
    *,
    epsilon: float,
    voltage_radius: float,
    voltage_scaffold: float,
    recovery_scaffold: float,
    linear_gain: float,
    cubic_gain: float,
    weight: float,
    maximal_scaled_delay: float,
) -> HalanayCertificate:
    r"""Certify all noncollective variational modes by a small-gain bound.

    ``voltage_radius`` bounds ``|V(t)-1|`` on the synchronous orbit.  With
    ``Z=|p|+weight*|q|``, every transverse mode satisfies

    ``D+ Z <= -a Z + b sup_[t-tau*,t] Z``

    with the returned ``local_decay=a`` and ``delayed_gain=b``.  If
    ``a>b``, the returned positive rate solves ``lambda=a-b exp(lambda*tau*)``.
    The estimate is independent of both module sizes.
    """

    values = np.asarray(
        (
            epsilon,
            voltage_radius,
            voltage_scaffold,
            recovery_scaffold,
            linear_gain,
            cubic_gain,
            weight,
            maximal_scaled_delay,
        ),
        dtype=float,
    )
    if not np.all(np.isfinite(values)):
        raise ValueError("all parameters must be finite")
    eps, radius, d_value, e_value, kappa_1, kappa_3, rho, theta = values
    if eps <= 0 or radius < 0 or d_value <= 0 or e_value <= 0:
        raise ValueError("epsilon and scaffolds must be positive; radius nonnegative")
    if rho <= 0 or theta <= 0:
        raise ValueError("weight and maximal scaled delay must be positive")

    coefficient = abs(kappa_1) + 3.0 * abs(kappa_3) * radius**2
    voltage_decay = d_value - 1.0 - eps * (coefficient + rho)
    recovery_decay = e_value - 1.0 / rho
    local_decay = min(voltage_decay, recovery_decay)
    delayed_gain = eps * coefficient
    margin = local_decay - delayed_gain
    physical_delay = theta / np.sqrt(eps)

    if margin <= 0.0:
        decay_rate = 0.0
    elif delayed_gain == 0.0:
        decay_rate = local_decay
    else:
        # The Lambert-W formula avoids root-finding ambiguity:
        # lambda=a-W(b*h*exp(a*h))/h.
        with mp.workdps(80):
            a_mp = mp.mpf(str(local_decay))
            b_mp = mp.mpf(str(delayed_gain))
            h_mp = mp.mpf(str(physical_delay))
            rate_mp = a_mp - mp.lambertw(b_mp * h_mp * mp.exp(a_mp * h_mp)) / h_mp
            decay_rate = float(rate_mp)
    return HalanayCertificate(
        epsilon=float(eps),
        voltage_radius=float(radius),
        coefficient_bound=float(coefficient),
        local_decay=float(local_decay),
        delayed_gain=float(delayed_gain),
        margin=float(margin),
        maximal_physical_delay=float(physical_delay),
        decay_rate=float(decay_rate),
    )


def leading_safety_direction(linear_gain: float, first_delay_moment: float) -> np.ndarray:
    r"""Return the declared leading ``(kappa1,kappa3,s)`` safety row.

    The physical row is ``epsilon**(3/2)`` times this vector, up to the
    separately assumed ``O(epsilon**2)`` root remainder.
    """

    values = np.asarray((linear_gain, first_delay_moment), dtype=float)
    if not np.all(np.isfinite(values)):
        raise ValueError("gain and delay moment must be finite")
    return np.array([values[1] / 8.0, 0.0, values[0] / 8.0], dtype=float)


def declared_two_scale_no_go_bounds(
    *,
    epsilon: float,
    width: float,
    linear_gain: float,
    first_delay_moment: float,
    safety_remainder_constant: float,
    profile_slope_lower_bound: float,
    shape_derivative_bound: float,
) -> TwoScaleNoGoBounds:
    r"""Return the two model-specific upper bounds for response surjectivity.

    Assumptions represented by the arguments are

    ``D S = eps**(3/2) s0 + e_s``, ``|e_s|<=C_s eps**2``, and
    ``D R_h = (A'/width) D S + r``, ``|A'|>=a_*``, ``|r|<=C_R``.

    The naturally scaled output is ``S/eps**(3/2)``.  These are theorem
    constants, not estimates extracted from an orbit computation.
    """

    values = np.asarray(
        (
            epsilon,
            width,
            linear_gain,
            first_delay_moment,
            safety_remainder_constant,
            profile_slope_lower_bound,
            shape_derivative_bound,
        ),
        dtype=float,
    )
    if not np.all(np.isfinite(values)):
        raise ValueError("all bounds must be finite")
    eps, layer_width, kappa_1, moment, c_s, slope, c_r = values
    if eps <= 0 or layer_width <= 0 or slope <= 0:
        raise ValueError("epsilon, width, and slope bound must be positive")
    if c_s < 0 or c_r < 0:
        raise ValueError("remainder constants must be nonnegative")
    safety_bound = eps ** 1.5 * np.linalg.norm(
        leading_safety_direction(kappa_1, moment)
    ) + c_s * eps**2
    physical_layer = c_r * layer_width / np.hypot(layer_width, slope)
    natural_scale = eps ** 1.5
    scaled_layer = c_r * layer_width / np.hypot(
        layer_width, slope * natural_scale
    )
    return TwoScaleNoGoBounds(
        epsilon=float(eps),
        width=float(layer_width),
        safety_row_bound=float(safety_bound),
        physical_layer_bound=float(physical_layer),
        physical_combined_bound=float(min(safety_bound, physical_layer)),
        natural_scaled_layer_bound=float(scaled_layer),
    )


def _canonical_smallest_singular_value(
    safety_magnitude: mp.mpf,
    shear: mp.mpf,
    *,
    displayed_safety_magnitude: mp.mpf | None = None,
) -> mp.mpf:
    """Smallest singular value of the exact three-row sharpness example."""

    kappa = (
        safety_magnitude
        if displayed_safety_magnitude is None
        else displayed_safety_magnitude
    )
    amplitude_shear = shear * safety_magnitude
    trace = mp.mpf(1) + amplitude_shear**2 + kappa**2
    determinant = kappa**2
    discriminant = mp.sqrt(trace**2 - 4 * determinant)
    # Rationalized eigenvalue formula prevents catastrophic cancellation.
    smallest_squared = 2 * determinant / (trace + discriminant)
    return min(mp.mpf(1), mp.sqrt(smallest_squared))


def canonical_sharpness_diagnostic(
    *,
    epsilon: float | str,
    width: float | str,
    safety_direction_norm: float | str,
    profile_slope: float | str = 1,
    decimal_digits: int = 100,
) -> SharpnessDiagnostic:
    r"""Evaluate a response family attaining both layer bounds asymptotically.

    After an orthogonal actuator change, the rows are

    ``f=e2``, ``s=kappa*e3``, ``a=e1+(profile_slope/width)*s``.

    Here ``kappa=epsilon**(3/2)*safety_direction_norm``.  The second
    singular value reported by the function divides the safety row by
    ``epsilon**(3/2)`` (not by its full norm).  This is a sharpness
    diagnostic tied to the declared leading safety direction; it is not a
    numerical FHN orbit or a periodic-orbit certificate.
    """

    digits = int(decimal_digits)
    if digits < 30:
        raise ValueError("at least 30 decimal digits are required")
    with mp.workdps(digits):
        eps = mp.mpf(epsilon)
        layer_width = mp.mpf(width)
        direction_norm = mp.mpf(safety_direction_norm)
        slope = abs(mp.mpf(profile_slope))
        if eps <= 0 or layer_width <= 0 or direction_norm <= 0 or slope <= 0:
            raise ValueError("epsilon, width, direction norm, and slope must be positive")
        safety_magnitude = eps ** mp.mpf("1.5") * direction_norm
        shear = slope / layer_width
        physical_sigma = _canonical_smallest_singular_value(
            safety_magnitude,
            shear,
        )
        scaled_sigma = _canonical_smallest_singular_value(
            safety_magnitude,
            shear,
            displayed_safety_magnitude=direction_norm,
        )
        physical_bound = 1 / mp.sqrt(1 + shear**2)
        scaled_shear = shear * eps ** mp.mpf("1.5")
        scaled_bound = 1 / mp.sqrt(1 + scaled_shear**2)
        return SharpnessDiagnostic(
            epsilon=+eps,
            width=+layer_width,
            safety_magnitude=+safety_magnitude,
            physical_smallest_singular_value=+physical_sigma,
            physical_bound=+physical_bound,
            physical_ratio=+(physical_sigma / physical_bound),
            scaled_smallest_singular_value=+scaled_sigma,
            scaled_bound=+scaled_bound,
            scaled_ratio=+(scaled_sigma / scaled_bound),
        )
