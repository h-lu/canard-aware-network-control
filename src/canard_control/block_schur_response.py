"""Exact finite-dimensional regression for the graph Schur response.

The paper-level result is an operator identity on Banach spaces.  This module
only checks the same block algebra with exact SymPy matrices.  In particular,
it does not prove existence of an invariant history graph, a Fredholm inverse,
or any uniform-in-network estimate.
"""

from __future__ import annotations

from dataclasses import dataclass

import sympy as sp


Matrix = sp.ImmutableMatrix


def _matrix(value: sp.MatrixBase) -> sp.Matrix:
    return sp.Matrix(value)


@dataclass(frozen=True)
class BlockSchurResponse:
    """Exact response of a two-block implicit residual and scalar gap."""

    schur_complement: Matrix
    critical_response: Matrix
    transverse_response: Matrix
    effective_critical_gap: Matrix
    direct_gap_response: sp.Expr
    transverse_gap_response: sp.Expr
    total_gap_response: sp.Expr


def block_schur_gap_response(
    a: sp.MatrixBase,
    b: sp.MatrixBase,
    c: sp.MatrixBase,
    d: sp.MatrixBase,
    g_critical: sp.MatrixBase,
    g_transverse: sp.MatrixBase,
    gap_critical: sp.MatrixBase,
    gap_transverse: sp.MatrixBase,
    *,
    explicit_gap_response: sp.Expr = sp.Integer(0),
) -> BlockSchurResponse:
    """Return the exact implicit response and its direct/transverse gap split.

    The residual derivative is ``[[a,b],[c,d]]`` and the parameter forcing is
    ``(g_critical,g_transverse)``.  Thus the state derivative solves

    ``[[a,b],[c,d]] * (q_dot,h_dot) = -(g_critical,g_transverse)``.

    ``gap_critical`` and ``gap_transverse`` are row matrices.  The returned
    split is the Banach-space Schur formula specialized to finite dimensions.
    """

    a_m = _matrix(a)
    b_m = _matrix(b)
    c_m = _matrix(c)
    d_m = _matrix(d)
    gc_m = _matrix(g_critical)
    gp_m = _matrix(g_transverse)
    mc_m = _matrix(gap_critical)
    mp_m = _matrix(gap_transverse)

    if a_m.rows != a_m.cols or d_m.rows != d_m.cols:
        raise ValueError("a and d must be square")
    if b_m.shape != (a_m.rows, d_m.rows):
        raise ValueError("b has incompatible shape")
    if c_m.shape != (d_m.rows, a_m.rows):
        raise ValueError("c has incompatible shape")
    if gc_m.shape != (a_m.rows, 1):
        raise ValueError("g_critical must be a compatible column")
    if gp_m.shape != (d_m.rows, 1):
        raise ValueError("g_transverse must be a compatible column")
    if mc_m.shape != (1, a_m.rows):
        raise ValueError("gap_critical must be a compatible row")
    if mp_m.shape != (1, d_m.rows):
        raise ValueError("gap_transverse must be a compatible row")

    d_inverse = d_m.inv()
    schur = sp.simplify(a_m - b_m * d_inverse * c_m)
    schur_inverse = schur.inv()

    q_dot = sp.simplify(
        -schur_inverse * gc_m
        + schur_inverse * b_m * d_inverse * gp_m
    )
    h_dot = sp.simplify(-d_inverse * gp_m - d_inverse * c_m * q_dot)

    effective_gap = sp.simplify(mc_m - mp_m * d_inverse * c_m)
    direct = sp.simplify(
        sp.sympify(explicit_gap_response)
        - (effective_gap * schur_inverse * gc_m)[0]
    )
    transverse = sp.simplify(
        (
            (effective_gap * schur_inverse * b_m - mp_m)
            * d_inverse
            * gp_m
        )[0]
    )
    total = sp.simplify(direct + transverse)

    return BlockSchurResponse(
        schur_complement=sp.ImmutableMatrix(schur),
        critical_response=sp.ImmutableMatrix(q_dot),
        transverse_response=sp.ImmutableMatrix(h_dot),
        effective_critical_gap=sp.ImmutableMatrix(effective_gap),
        direct_gap_response=direct,
        transverse_gap_response=transverse,
        total_gap_response=total,
    )
