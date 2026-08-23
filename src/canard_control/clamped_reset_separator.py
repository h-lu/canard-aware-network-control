"""Certificates for the collective-recovery-clamped reset separator.

The original causal reset presets the collective recovery coordinate ``rho``
but lets it drift after voltage release.  The repaired protocol applies the
physical recovery actuator ``u_w=r*u_rho`` with
``u_rho = -epsilon * (xi - mu)`` until a pulse or quiet passage block is
reached.  Its transverse projection is zero, so the recovery coordinate
``kappa`` is not clamped and continues to obey its physical equation.

This module checks the exact controller and equilibrium identities, a
delay-independent small-gain condition preserving the one-dimensional
unstable index, the logarithmic decision-time estimate away from a declared
deadband, and a scalar diffusive-delay example showing why no uniform stable
spectral gap follows merely from weak coupling when the delay diverges.

The stable-manifold and channel-capture theorem itself is analytic and is
stated in ``docs/paper-iii-collective-clamp-separator.md``.  The numerical
utilities here do not replace its RFDE hypotheses.
"""

from __future__ import annotations

from cmath import exp
from dataclasses import dataclass
from math import isfinite, log

import mpmath as mp
import sympy as sp

from .final_two_module import final_two_module_audit


@dataclass(frozen=True)
class CollectiveClampAudit:
    """Exact modal identities for the scalar collective-recovery clamp."""

    epsilon: sp.Expr
    critical_voltage: sp.Symbol
    transverse_voltage: sp.Symbol
    unfolding: sp.Symbol
    recovery_gap: sp.Symbol
    uncontrolled_collective_drift: sp.Expr
    collective_control: sp.Expr
    physical_recovery_actuator: sp.Matrix
    critical_actuator_projection: sp.Expr
    transverse_actuator_projection: sp.Expr
    controlled_collective_drift: sp.Expr
    transverse_recovery_equilibrium: sp.Expr
    transverse_recovery_residual: sp.Expr
    equilibrium_jacobian_determinant_at_zero_epsilon: sp.Expr
    expected_jacobian_determinant: sp.Expr


def collective_clamp_audit() -> CollectiveClampAudit:
    r"""Return exact identities behind the minimally clamped protocol.

    In modal variables the uncontrolled recovery equations are

    ``dot(rho)=epsilon*(xi-mu)`` and
    ``dot(kappa)=epsilon*zeta-D_w*kappa``.

    The corresponding physical recovery actuator is ``u_w=r*u_rho``.
    Since ``ell.T*r=1`` and ``m.T*r=0``, this fixes ``rho`` without directly
    driving ``kappa``.  At a constant voltage,
    ``kappa=epsilon*zeta/D_w`` remains its exact physical equilibrium.

    The final determinant identity is the implicit-function condition for
    continuing any nonsingular frozen-layer voltage equilibrium to an exact
    equilibrium of the clamped ``(v,kappa)`` system.
    """

    base = final_two_module_audit()
    epsilon = sp.Symbol("epsilon", nonnegative=True)
    xi, zeta, mu = sp.symbols("xi zeta mu", real=True)
    recovery_gap = sp.Symbol("D_w", positive=True)

    uncontrolled = epsilon * (xi - mu)
    control = -uncontrolled
    r = sp.Matrix(base.critical_right)
    ell = sp.Matrix(base.critical_left)
    m = sp.Matrix(base.transverse_left)
    physical_actuator = sp.simplify(r * control)
    critical_actuator_projection = sp.simplify(
        (ell.T * physical_actuator)[0]
    )
    transverse_actuator_projection = sp.simplify(
        (m.T * physical_actuator)[0]
    )
    controlled = sp.simplify(uncontrolled + control)
    kappa_equilibrium = sp.simplify(epsilon * zeta / recovery_gap)
    kappa_residual = sp.simplify(
        epsilon * zeta - recovery_gap * kappa_equilibrium
    )

    v_1, v_2, kappa = sp.symbols("v_1 v_2 kappa", real=True)
    rho_0 = sp.Symbol("rho_0", real=True)
    q = sp.Matrix(base.transverse_right)
    w_star = sp.Matrix(base.equilibrium_w)
    w = w_star + r * rho_0 + q * kappa

    fast = sp.Matrix(
        [
            v_1 - v_1**3 / 3 - w[0] + (v_2 - v_1) / 2,
            v_2 - v_2**3 / 3 - w[1] + 2 * (v_1 - v_2),
        ]
    )
    voltage = sp.Matrix([v_1, v_2])
    transverse_voltage = (m.T * (voltage - base.equilibrium_v))[0]
    equilibrium_map = sp.Matrix.vstack(
        fast,
        sp.Matrix([epsilon * transverse_voltage - recovery_gap * kappa]),
    )
    jacobian = equilibrium_map.jacobian((v_1, v_2, kappa))
    determinant_at_zero = sp.factor(
        jacobian.subs({epsilon: 0, kappa: 0}).det()
    )
    fast_jacobian = fast.jacobian((v_1, v_2))
    expected = sp.factor(-recovery_gap * fast_jacobian.det())

    return CollectiveClampAudit(
        epsilon=epsilon,
        critical_voltage=xi,
        transverse_voltage=zeta,
        unfolding=mu,
        recovery_gap=recovery_gap,
        uncontrolled_collective_drift=uncontrolled,
        collective_control=control,
        physical_recovery_actuator=physical_actuator,
        critical_actuator_projection=critical_actuator_projection,
        transverse_actuator_projection=transverse_actuator_projection,
        controlled_collective_drift=controlled,
        transverse_recovery_equilibrium=kappa_equilibrium,
        transverse_recovery_residual=kappa_residual,
        equilibrium_jacobian_determinant_at_zero_epsilon=(
            determinant_at_zero
        ),
        expected_jacobian_determinant=expected,
    )


@dataclass(frozen=True)
class SpectralIndexCertificate:
    """Small-gain margin for preservation of the RFDE unstable index."""

    perturbation_bound: float
    loop_bound: float
    margin: float
    certifies_index_preservation: bool


def spectral_index_certificate(
    *,
    epsilon: float,
    weak_gain: float,
    current_gain_norm: float,
    delayed_gain_norm_sum: float,
    imaginary_axis_resolvent_bound: float,
) -> SpectralIndexCertificate:
    r"""Evaluate the delay-independent resolvent small-gain condition.

    Let ``A`` be the non-delay linearization of the clamped ``(v,kappa)``
    system and suppose it has one unstable eigenvalue and no imaginary-axis
    spectrum.  On ``Re(z)=0`` the diffusive RFDE perturbation has norm at
    most

    ``epsilon*abs(K)*(||B|| + sum_k ||C_k||)``.

    If this number times ``sup_w ||(i*w I-A)^(-1)||`` is strictly below
    one, the characteristic determinant has no imaginary-axis zero along
    the homotopy that switches on all delay atoms.  Hence the RFDE retains
    the same unstable root count.  The estimate is independent of the delay
    lengths because ``|exp(-i*w*tau_k)|=1``.
    """

    values = (
        epsilon,
        weak_gain,
        current_gain_norm,
        delayed_gain_norm_sum,
        imaginary_axis_resolvent_bound,
    )
    if not all(isfinite(float(value)) for value in values):
        raise ValueError("all spectral certificate data must be finite")
    if epsilon < 0.0:
        raise ValueError("epsilon must be nonnegative")
    if current_gain_norm < 0.0 or delayed_gain_norm_sum < 0.0:
        raise ValueError("gain norms must be nonnegative")
    if imaginary_axis_resolvent_bound <= 0.0:
        raise ValueError("resolvent bound must be positive")

    perturbation = (
        epsilon
        * abs(weak_gain)
        * (current_gain_norm + delayed_gain_norm_sum)
    )
    loop_bound = perturbation * imaginary_axis_resolvent_bound
    margin = 1.0 - loop_bound
    return SpectralIndexCertificate(
        perturbation_bound=perturbation,
        loop_bound=loop_bound,
        margin=margin,
        certifies_index_preservation=margin > 0.0,
    )


def decision_time_bound(
    *,
    unstable_rate_lower: float,
    exit_coordinate: float,
    reset_slope_lower: float,
    parameter_deadband: float,
) -> float:
    r"""Bound clamp time needed to classify outside a parameter deadband.

    In a local unstable coordinate assume

    ``|u(0)| >= reset_slope_lower*|a|`` and
    ``d|u|/dt >= unstable_rate_lower*|u|``

    until ``|u|=exit_coordinate``.  Then every
    ``|a| >= parameter_deadband`` exits no later than the returned time.
    This is a conditional normal-form estimate, not an RFDE enclosure.
    """

    values = (
        unstable_rate_lower,
        exit_coordinate,
        reset_slope_lower,
        parameter_deadband,
    )
    if not all(isfinite(float(value)) for value in values):
        raise ValueError("decision-time data must be finite")
    if unstable_rate_lower <= 0.0:
        raise ValueError("unstable rate must be positive")
    if exit_coordinate <= 0.0:
        raise ValueError("exit coordinate must be positive")
    if reset_slope_lower <= 0.0:
        raise ValueError("reset slope must be positive")
    if parameter_deadband <= 0.0:
        raise ValueError("parameter deadband must be positive")

    initial = reset_slope_lower * parameter_deadband
    if initial >= exit_coordinate:
        return 0.0
    return log(exit_coordinate / initial) / unstable_rate_lower


def diffusive_scalar_characteristic_root(
    *,
    delta: float,
    decay: float,
    weak_gain: float,
    layer_gain: float,
    scaled_delay: float,
    branch: int = 0,
) -> complex:
    r"""Return an exact Lambert-W root of a scalar weak diffusive DDE.

    The equation is

    ``y'=-decay*y + delta**2*weak_gain*layer_gain``
    ``*(y(t)-y(t-scaled_delay/delta))``.

    Its characteristic roots satisfy

    ``lambda = -a0 + W_k(-c*tau*exp(a0*tau))/tau``,

    where ``c=delta**2*weak_gain*layer_gain`` and ``a0=decay-c``.
    For fixed positive data and small ``delta``, suitable complex branches
    have negative real parts tending to zero.  This explicitly demonstrates
    the loss of a delay-uniform stable spectral gap.
    """

    values = (delta, decay, weak_gain, layer_gain, scaled_delay)
    if not all(isfinite(float(value)) for value in values):
        raise ValueError("characteristic data must be finite")
    if delta <= 0.0:
        raise ValueError("delta must be positive")
    if decay <= 0.0:
        raise ValueError("decay must be positive")
    if weak_gain <= 0.0 or layer_gain <= 0.0:
        raise ValueError("gains must be positive")
    if scaled_delay <= 0.0:
        raise ValueError("scaled delay must be positive")

    c = mp.mpf(delta) ** 2 * weak_gain * layer_gain
    a_0 = mp.mpf(decay) - c
    if a_0 <= 0:
        raise ValueError("require decay > delta**2*weak_gain*layer_gain")
    tau = mp.mpf(scaled_delay) / delta
    argument = -c * tau * mp.exp(a_0 * tau)
    root = -a_0 + mp.lambertw(argument, branch) / tau
    return complex(root)


def diffusive_scalar_residual(
    root: complex,
    *,
    delta: float,
    decay: float,
    weak_gain: float,
    layer_gain: float,
    scaled_delay: float,
) -> complex:
    """Evaluate the characteristic residual for the scalar diagnostic."""

    c = delta**2 * weak_gain * layer_gain
    tau = scaled_delay / delta
    return root + decay - c + c * exp(-root * tau)


def diffusive_scalar_leading_real_part(
    *,
    delta: float,
    decay: float,
    weak_gain: float,
    layer_gain: float,
    scaled_delay: float,
) -> float:
    r"""Return the leading real part in the weak-long-delay asymptotic.

    For either conjugate Lambert branch adjacent to the negative real cut,

    ``Re(lambda_delta)`` is asymptotic to

    ``(delta/theta)*log(delta**2*K*b/a)``.

    The returned value is negative in the declared weak-gain regime.  This
    helper evaluates the asymptotic comparator only; it does not compute a
    characteristic root.
    """

    values = (delta, decay, weak_gain, layer_gain, scaled_delay)
    if not all(isfinite(float(value)) for value in values):
        raise ValueError("asymptotic data must be finite")
    if delta <= 0.0 or decay <= 0.0 or scaled_delay <= 0.0:
        raise ValueError("delta, decay, and scaled delay must be positive")
    if weak_gain <= 0.0 or layer_gain <= 0.0:
        raise ValueError("gains must be positive")
    ratio = delta**2 * weak_gain * layer_gain / decay
    if not 0.0 < ratio < 1.0:
        raise ValueError("require delta**2*weak_gain*layer_gain < decay")
    return delta * log(ratio) / scaled_delay
