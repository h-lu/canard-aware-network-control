"""Exact regression for the Banach-scale response identities.

Finite matrices cannot prove the Banach-scale theorem.  This test audits the
signs and factor-of-two conventions in its first/second graph response,
trace elimination, endpoint chain rule, and levelwise Schur solve.
"""

from __future__ import annotations

import sympy as sp

from canard_control.block_schur_response import block_schur_gap_response


def _quadratic_vector(
    hessians: tuple[sp.Matrix, ...], left: sp.Matrix, right: sp.Matrix
) -> sp.Matrix:
    return sp.Matrix([(left.T * hessian * right)[0] for hessian in hessians])


def test_first_second_scale_response_trace_and_endpoint_chain() -> None:
    # Graph residual:
    # L z - r t - r^2 u/2 - r M z - B[z,z]/2 = 0.
    linear = sp.Matrix([[3, 1], [2, 4]])
    first_source = sp.Matrix([2, -1])
    second_explicit = sp.Matrix([3, 5])
    mixed = sp.Matrix([[1, 2], [-1, 1]])
    graph_hessians = (
        sp.Matrix([[2, 1], [1, -1]]),
        sp.Matrix([[0, 3], [3, 2]]),
    )

    z_1 = linear.inv() * first_source
    z_2_source = (
        second_explicit
        + 2 * mixed * z_1
        + _quadratic_vector(graph_hessians, z_1, z_1)
    )
    z_2 = linear.inv() * z_2_source

    # The same first response must be returned by the critical/transverse
    # Schur formula, using the residual-forcing convention g = -t.
    schur = block_schur_gap_response(
        sp.Matrix([[linear[0, 0]]]),
        sp.Matrix([[linear[0, 1]]]),
        sp.Matrix([[linear[1, 0]]]),
        sp.Matrix([[linear[1, 1]]]),
        sp.Matrix([[-first_source[0]]]),
        sp.Matrix([[-first_source[1]]]),
        sp.Matrix([[0]]),
        sp.Matrix([[0]]),
    )
    assert schur.critical_response == sp.Matrix([[z_1[0]]])
    assert schur.transverse_response == sp.Matrix([[z_1[1]]])

    # Nonlinear history extension A(z) = E z + H[z,z]/2.
    history_linear = sp.Matrix([[1, 2], [-2, 1], [3, -1]])
    history_hessians = (
        sp.Matrix([[1, 0], [0, 2]]),
        sp.Matrix([[0, 1], [1, -1]]),
        sp.Matrix([[2, -1], [-1, 0]]),
    )
    a_1 = history_linear * z_1
    a_2 = (
        history_linear * z_2
        + _quadratic_vector(history_hessians, z_1, z_1)
    )

    # Selected trace residual:
    # D w + P A + p r + r^2 q/2 + r M_A A
    #     + B_A[A,A]/2 = 0.
    trace_linear = sp.Matrix([[5]])
    trace_history = sp.Matrix([[1, -2, 1]])
    trace_parameter = sp.Matrix([[3]])
    trace_second_explicit = sp.Matrix([[7]])
    trace_mixed = sp.Matrix([[2, 0, -1]])
    trace_history_hessian = sp.Matrix(
        [[1, 0, 2], [0, -1, 1], [2, 1, 0]]
    )

    w_1 = -trace_linear.inv() * (
        trace_history * a_1 + trace_parameter
    )
    w_2 = -trace_linear.inv() * (
        trace_history * a_2
        + trace_second_explicit
        + 2 * trace_mixed * a_1
        + sp.Matrix([(a_1.T * trace_history_hessian * a_1)[0]])
    )

    # Two complete-history endpoint observations.  The vectors y_1 and y_2
    # are the first and second responses of (A,w,r).
    y_1 = a_1.col_join(w_1).col_join(sp.Matrix([1]))
    y_2 = a_2.col_join(w_2).col_join(sp.Matrix([0]))
    endpoint_a_linear = sp.Matrix([[1, -1, 2, 3, 4]])
    endpoint_r_linear = sp.Matrix([[2, 1, -2, -1, 5]])
    endpoint_a_hessian = sp.Matrix(
        [
            [1, 0, 0, 1, -1],
            [0, 2, 1, 0, 0],
            [0, 1, -1, 2, 1],
            [1, 0, 2, 3, -2],
            [-1, 0, 1, -2, 2],
        ]
    )
    endpoint_r_hessian = sp.Matrix(
        [
            [0, 1, -1, 0, 2],
            [1, 1, 0, -1, 0],
            [-1, 0, 2, 1, -2],
            [0, -1, 1, 1, 1],
            [2, 0, -2, 1, -1],
        ]
    )

    endpoint_a_1 = (endpoint_a_linear * y_1)[0]
    endpoint_r_1 = (endpoint_r_linear * y_1)[0]
    endpoint_a_2 = (
        endpoint_a_linear * y_2
    )[0] + (y_1.T * endpoint_a_hessian * y_1)[0]
    endpoint_r_2 = (
        endpoint_r_linear * y_2
    )[0] + (y_1.T * endpoint_r_hessian * y_1)[0]

    # Scalar phase-normal matcher j(e_a,e_r,r).
    matcher_linear = sp.Matrix([[2, -3, 5]])
    matcher_hessian = sp.Matrix([[1, 2, -1], [2, -2, 3], [-1, 3, 4]])
    endpoint_first = sp.Matrix([endpoint_a_1, endpoint_r_1, 1])
    endpoint_second = sp.Matrix([endpoint_a_2, endpoint_r_2, 0])
    gap_1 = (matcher_linear * endpoint_first)[0]
    gap_2 = (
        matcher_linear * endpoint_second
    )[0] + (endpoint_first.T * matcher_hessian * endpoint_first)[0]

    # Independent formal-series substitution audits every factor of two.
    r = sp.symbols("r")
    z_series = r * z_1 + r**2 * z_2 / 2
    graph_residual = (
        linear * z_series
        - r * first_source
        - r**2 * second_explicit / 2
        - r * mixed * z_series
        - _quadratic_vector(graph_hessians, z_series, z_series) / 2
    )
    assert all(
        sp.expand(component).coeff(r, degree) == 0
        for component in graph_residual
        for degree in (1, 2)
    )

    a_series = (
        history_linear * z_series
        + _quadratic_vector(history_hessians, z_series, z_series) / 2
    )
    w_series = r * w_1 + r**2 * w_2 / 2
    trace_residual = (
        trace_linear * w_series
        + trace_history * a_series
        + r * trace_parameter
        + r**2 * trace_second_explicit / 2
        + r * trace_mixed * a_series
        + sp.Matrix(
            [(a_series.T * trace_history_hessian * a_series)[0] / 2]
        )
    )
    assert sp.expand(trace_residual[0]).coeff(r, 1) == 0
    assert sp.expand(trace_residual[0]).coeff(r, 2) == 0

    y_series = a_series.col_join(w_series).col_join(sp.Matrix([r]))
    endpoint_a_series = (
        endpoint_a_linear * y_series
    )[0] + (y_series.T * endpoint_a_hessian * y_series)[0] / 2
    endpoint_r_series = (
        endpoint_r_linear * y_series
    )[0] + (y_series.T * endpoint_r_hessian * y_series)[0] / 2
    endpoint_series = sp.Matrix([endpoint_a_series, endpoint_r_series, r])
    gap_series = (
        matcher_linear * endpoint_series
    )[0] + (endpoint_series.T * matcher_hessian * endpoint_series)[0] / 2

    assert sp.diff(gap_series, r).subs(r, 0) == gap_1
    assert sp.diff(gap_series, r, 2).subs(r, 0) == gap_2
