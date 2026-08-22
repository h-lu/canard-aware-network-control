"""Exact algebra for the proof-oriented two-module FHN benchmark.

The benchmark uses a fixed instantaneous synchronization scaffold and weak
delayed actuators.  The scaffold vanishes on the collective history, so the
scalar delayed-canard calibration is unchanged, while its fast Jacobian
separates the collective voltage direction from every transverse voltage
direction.

This module checks finite-dimensional algebra only.  It does not prove the
RFDE Fredholm hypotheses or periodic-orbit sensitivity bounds.
"""

from __future__ import annotations

from dataclasses import dataclass

import sympy as sp


@dataclass(frozen=True)
class SymmetricReferenceAlgebra:
    """Matrix, modes, and first-delay moment of the symmetric reference."""

    averaging_matrix: sp.Matrix
    collective_mode: sp.Matrix
    difference_mode: sp.Matrix
    collective_residual: sp.Matrix
    difference_residual: sp.Matrix
    first_delay_moment: sp.Expr
    shifted_moment_derivative: sp.Expr
    formal_threshold: sp.Expr


def block_averaging_matrix(n_1: int, n_2: int) -> sp.Matrix:
    r"""Return the rank-one two-module averaging matrix.

    For a source node in module ``b``, every receiving row has weight
    ``1/(2*n_b)``.  Thus each module contributes mass one half and every row
    sums to one.
    """

    if n_1 <= 0 or n_2 <= 0:
        raise ValueError("module sizes must be positive")

    row = [sp.Rational(1, 2 * n_1)] * n_1
    row += [sp.Rational(1, 2 * n_2)] * n_2
    return sp.Matrix([row for _ in range(n_1 + n_2)])


def symmetric_reference_algebra(
    n_1: int = 2,
    n_2: int = 3,
) -> SymmetricReferenceAlgebra:
    r"""Return exact checks for the symmetric two-delay reference.

    The within-module and cross-module scaled delays are ``Theta_0+s`` and
    ``Theta_1+s``.  On the collective history their topology-weighted first
    moment is

    .. math::
       M_1=(\Theta_0+\Theta_1)/2+s.

    With delayed-minus-current linear actuation, the formal calibration law
    is

    .. math::
       a_c=1-\varepsilon/8
       -(\kappa_1/8)M_1\varepsilon^{3/2}+O(\varepsilon^2).
    """

    matrix = block_averaging_matrix(n_1, n_2)
    dimension = n_1 + n_2
    collective = sp.ones(dimension, 1)
    difference = sp.Matrix([1] * n_1 + [-1] * n_2)

    collective_residual = sp.simplify(matrix * collective - collective)
    difference_residual = sp.simplify(matrix * difference)

    theta_0, theta_1, shift = sp.symbols(
        "Theta_0 Theta_1 s", real=True
    )
    epsilon = sp.symbols("epsilon", positive=True)
    kappa_1 = sp.symbols("kappa_1", real=True)
    first_delay_moment = (theta_0 + theta_1) / 2 + shift
    shifted_moment_derivative = sp.diff(first_delay_moment, shift)
    formal_threshold = (
        1
        - epsilon / 8
        - kappa_1 * first_delay_moment * epsilon ** sp.Rational(3, 2) / 8
    )

    return SymmetricReferenceAlgebra(
        averaging_matrix=matrix,
        collective_mode=collective,
        difference_mode=difference,
        collective_residual=collective_residual,
        difference_residual=difference_residual,
        first_delay_moment=first_delay_moment,
        shifted_moment_derivative=shifted_moment_derivative,
        formal_threshold=formal_threshold,
    )

