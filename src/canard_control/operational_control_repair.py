"""Quantitative certificates for a reset-only safety actuator.

The mathematical statements are proved in
``docs/paper-iv-reset-only-block-control.md``.  This module evaluates the
finite-dimensional constants occurring in those statements.  It does not
certify a periodic FitzHugh--Nagumo branch, an RFDE separator, or an interval
enclosure for either object.

The repaired response has the exact form

``[[B, 0], [c.T, -1]]``

when the first two outputs are measured on a baseline periodic experiment
and the third actuator is used only in a separate reset experiment.  Here
``B`` is the two-by-two frequency--amplitude response and ``c`` is the
gradient of the operational channel threshold.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite, pi, sqrt

import numpy as np


@dataclass(frozen=True)
class BlockTriangularControlCertificate:
    """Pointwise singular-value certificate for the repaired response."""

    base_response: np.ndarray
    threshold_gradient: np.ndarray
    response_matrix: np.ndarray
    base_smallest_singular_value: float
    threshold_gradient_norm: float
    inverse_norm_squared_bound: float
    full_smallest_singular_value_lower_bound: float
    full_smallest_singular_value: float


@dataclass(frozen=True)
class QuantitativeInverseRadius:
    """A contraction-based local inverse and target-ball certificate."""

    smallest_singular_value_lower_bound: float
    derivative_lipschitz_bound: float
    available_domain_radius: float
    certified_input_radius: float
    contraction_factor_bound: float
    certified_output_radius: float


@dataclass(frozen=True)
class HopfNormalFormCertificate:
    """Exact frequency--amplitude response of the cubic Hopf normal form."""

    growth_gradient: np.ndarray
    angular_frequency_gradient: np.ndarray
    nonlinear_shear: float
    parameter_jacobian: np.ndarray
    response_matrix: np.ndarray
    determinant: float
    frobenius_norm: float
    smallest_singular_value: float
    determinant_over_frobenius_lower_bound: float


@dataclass(frozen=True)
class FloatingIntervalCandidateDiagnostic:
    """Non-rigorous floating-point screen for a proposed interval box.

    The values in this record are ordinary binary floating-point estimates.
    They are candidates for a later directed-rounding calculation, not an
    interval certificate.
    """

    midpoint: np.ndarray
    entrywise_radius: np.ndarray
    floating_midpoint_smallest_singular_value: float
    floating_radius_frobenius_norm: float
    candidate_margin: float

    @property
    def candidate_margin_positive(self) -> bool:
        """Whether the floating-point screen is worth rigorous follow-up."""

        return self.candidate_margin > 0.0


def _finite_matrix(value: np.ndarray, shape: tuple[int, ...], name: str) -> np.ndarray:
    matrix = np.asarray(value, dtype=float)
    if matrix.shape != shape:
        raise ValueError(f"{name} must have shape {shape}")
    if not np.all(np.isfinite(matrix)):
        raise ValueError(f"{name} must be finite")
    return matrix


def block_triangular_lower_bound(
    base_smallest_singular_value_lower_bound: float,
    threshold_gradient_norm_upper_bound: float,
) -> tuple[float, float]:
    r"""Bound ``sigma_min([[B,0],[c.T,-1]])`` from ``B`` and ``c``.

    If ``sigma_min(B) >= beta > 0`` and ``||c|| <= gamma``, the inverse is

    ``[[B^-1,0],[c.T B^-1,-1]]``.

    Its squared norm is bounded by the largest eigenvalue of

    ``[[beta^-2*(1+gamma^2), gamma/beta], [gamma/beta, 1]]``.

    Direct evaluation of that matrix can overflow even when ``beta`` and
    ``gamma`` are finite.  Instead write it as ``K.T @ K`` with

    ``K=beta^-1*[[1,0],[gamma,beta]]``

    and scale the second matrix before taking its largest singular value.
    The function returns the inverse-norm-squared bound when representable
    (otherwise positive infinity) and its reciprocal square root.  The latter
    can be zero only when the positive mathematical bound is smaller than the
    least representable nonzero binary64 number.
    """

    beta = float(base_smallest_singular_value_lower_bound)
    gamma = float(threshold_gradient_norm_upper_bound)
    if not isfinite(beta) or beta <= 0.0:
        raise ValueError("base singular-value lower bound must be positive")
    if not isfinite(gamma) or gamma < 0.0:
        raise ValueError("threshold-gradient norm bound must be nonnegative")

    scale = max(1.0, beta, gamma)
    beta_scaled = beta / scale
    scaled_factor = np.array(
        [[1.0 / scale, 0.0], [gamma / scale, beta_scaled]],
        dtype=float,
    )
    scaled_norm = float(np.linalg.svd(scaled_factor, compute_uv=False)[0])
    if scaled_norm <= 0.0:
        raise ArithmeticError("scaled inverse factor unexpectedly vanished")

    lower_bound = beta_scaled / scaled_norm
    maximum_float_root = sqrt(np.finfo(float).max)
    if beta_scaled == 0.0 or beta_scaled < scaled_norm / maximum_float_root:
        inverse_norm_squared = float("inf")
    else:
        inverse_norm = scaled_norm / beta_scaled
        inverse_norm_squared = inverse_norm * inverse_norm
    return float(inverse_norm_squared), float(lower_bound)


def operational_response_certificate(
    base_response: np.ndarray,
    threshold_gradient: np.ndarray,
) -> BlockTriangularControlCertificate:
    r"""Evaluate the exact block response and the analytic lower bound.

    The output convention is ``S=a_c(b)-a_op``.  Consequently the reset-only
    column is exactly ``(0,0,-1).T``.
    """

    base = _finite_matrix(base_response, (2, 2), "base_response")
    gradient = _finite_matrix(
        np.asarray(threshold_gradient, dtype=float),
        (2,),
        "threshold_gradient",
    )
    base_singular = float(np.linalg.svd(base, compute_uv=False)[-1])
    if base_singular <= 0.0:
        raise ValueError("base response must be nonsingular")
    gradient_norm = float(np.linalg.norm(gradient, ord=2))
    inverse_bound, full_lower = block_triangular_lower_bound(
        base_singular,
        gradient_norm,
    )
    response = np.block(
        [
            [base, np.zeros((2, 1), dtype=float)],
            [gradient.reshape(1, 2), -np.ones((1, 1), dtype=float)],
        ]
    )
    full_singular = float(np.linalg.svd(response, compute_uv=False)[-1])
    return BlockTriangularControlCertificate(
        base_response=base,
        threshold_gradient=gradient,
        response_matrix=response,
        base_smallest_singular_value=base_singular,
        threshold_gradient_norm=gradient_norm,
        inverse_norm_squared_bound=inverse_bound,
        full_smallest_singular_value_lower_bound=full_lower,
        full_smallest_singular_value=full_singular,
    )


def threshold_gradient_bound(
    base_gap_gradient_norm_upper_bound: float,
    stimulus_gap_derivative_lower_bound: float,
) -> float:
    r"""Return the IFT bound ``||D_b a_c|| <= G/g``.

    This uses ``Gamma(a_c(b),b)=0``, ``||D_b Gamma|| <= G``, and
    ``|partial_a Gamma| >= g > 0``.  Supplying these two scalars is not a
    substitute for proving the complete-history separator hypotheses.
    """

    numerator = float(base_gap_gradient_norm_upper_bound)
    denominator = float(stimulus_gap_derivative_lower_bound)
    if not isfinite(numerator) or numerator < 0.0:
        raise ValueError("base gap-gradient bound must be nonnegative")
    if not isfinite(denominator) or denominator <= 0.0:
        raise ValueError("stimulus transversality bound must be positive")
    return numerator / denominator


def quantitative_inverse_radius(
    *,
    smallest_singular_value_lower_bound: float,
    derivative_lipschitz_bound: float,
    available_domain_radius: float,
) -> QuantitativeInverseRadius:
    r"""Give an explicit local input radius and covered output radius.

    Let ``Q`` be continuously differentiable on the closed input ball of
    radius ``R``, let ``sigma_min(DQ(x0)) >= m``, and suppose

    ``||DQ(x)-DQ(y)|| <= L ||x-y||``.

    For ``L>0`` this routine selects ``r=min(R/2,m/(2L))``.  The Newton map
    based at ``x0`` is then a contraction with factor at most ``1/2``, and
    ``Q(B_r(x0))`` contains the output ball of radius
    ``rho=m*r-L*r^2/2``.  For ``L=0`` the map is affine on the ball and the
    returned conservative radius is ``m*R/2``.
    """

    m_value = float(smallest_singular_value_lower_bound)
    lipschitz = float(derivative_lipschitz_bound)
    domain = float(available_domain_radius)
    if not isfinite(m_value) or m_value <= 0.0:
        raise ValueError("singular-value lower bound must be positive")
    if not isfinite(lipschitz) or lipschitz < 0.0:
        raise ValueError("derivative Lipschitz bound must be nonnegative")
    if not isfinite(domain) or domain <= 0.0:
        raise ValueError("available domain radius must be positive")

    if lipschitz == 0.0:
        radius = domain / 2.0
        contraction = 0.0
        output = m_value * radius
    else:
        radius = min(domain / 2.0, m_value / (2.0 * lipschitz))
        contraction = lipschitz * radius / m_value
        output = m_value * radius - 0.5 * lipschitz * radius**2
    return QuantitativeInverseRadius(
        smallest_singular_value_lower_bound=m_value,
        derivative_lipschitz_bound=lipschitz,
        available_domain_radius=domain,
        certified_input_radius=float(radius),
        contraction_factor_bound=float(contraction),
        certified_output_radius=float(output),
    )


def hopf_normal_form_certificate(
    growth_gradient: np.ndarray,
    angular_frequency_gradient: np.ndarray,
    nonlinear_shear: float,
) -> HopfNormalFormCertificate:
    r"""Return the exact ``(F,A)`` response for a cubic Hopf family.

    The family is

    ``z'=(lambda(b)+i*omega(b))*z-(1+i*c)*|z|^2*z``,

    with affine ``lambda`` and ``omega`` having the supplied gradients.
    On ``lambda>0`` and ``omega-c*lambda>0``, for ``h=Re(z)``,

    ``F=(omega-c*lambda)/(2*pi)`` and ``A=(max h-min h)^2=4*lambda``.

    Thus the response rows are ``(w-c*l)/(2*pi)`` and ``4*l``.  It is
    nonsingular exactly when the parameter Jacobian with rows ``l,w`` is.
    """

    growth = _finite_matrix(
        np.asarray(growth_gradient, dtype=float),
        (2,),
        "growth_gradient",
    )
    frequency = _finite_matrix(
        np.asarray(angular_frequency_gradient, dtype=float),
        (2,),
        "angular_frequency_gradient",
    )
    shear = float(nonlinear_shear)
    if not isfinite(shear):
        raise ValueError("nonlinear shear must be finite")

    parameter_jacobian = np.vstack((growth, frequency))
    response = np.vstack(
        ((frequency - shear * growth) / (2.0 * pi), 4.0 * growth)
    )
    determinant = float(np.linalg.det(response))
    frobenius = float(np.linalg.norm(response, ord="fro"))
    singular = float(np.linalg.svd(response, compute_uv=False)[-1])
    det_frobenius = (
        abs(determinant) / frobenius if frobenius > 0.0 else 0.0
    )
    return HopfNormalFormCertificate(
        growth_gradient=growth,
        angular_frequency_gradient=frequency,
        nonlinear_shear=shear,
        parameter_jacobian=parameter_jacobian,
        response_matrix=response,
        determinant=determinant,
        frobenius_norm=frobenius,
        smallest_singular_value=singular,
        determinant_over_frobenius_lower_bound=float(det_frobenius),
    )


def floating_interval_candidate_diagnostic(
    midpoint: np.ndarray,
    entrywise_radius: np.ndarray,
) -> FloatingIntervalCandidateDiagnostic:
    r"""Screen a proposed two-by-two entrywise interval box.

    Every matrix in the box has the form ``midpoint+E`` with
    ``abs(E_ij)<=entrywise_radius_ij``.  Hence ``||E||_2<=||radius||_F``
    and Weyl's inequality motivates the returned candidate margin.

    All operations here use ordinary NumPy floating point.  In particular,
    neither the input endpoints, the singular value, nor the Frobenius norm
    is outward rounded.  A positive result is only a screening diagnostic;
    it cannot certify a mathematical interval enclosure.
    """

    center = _finite_matrix(midpoint, (2, 2), "midpoint")
    radius = _finite_matrix(entrywise_radius, (2, 2), "entrywise_radius")
    if np.any(radius < 0.0):
        raise ValueError("entrywise radii must be nonnegative")
    center_singular = float(np.linalg.svd(center, compute_uv=False)[-1])
    perturbation = float(np.linalg.norm(radius, ord="fro"))
    candidate = center_singular - perturbation
    return FloatingIntervalCandidateDiagnostic(
        midpoint=center,
        entrywise_radius=radius,
        floating_midpoint_smallest_singular_value=center_singular,
        floating_radius_frobenius_norm=perturbation,
        candidate_margin=float(candidate),
    )
