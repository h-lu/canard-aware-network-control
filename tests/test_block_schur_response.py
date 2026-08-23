from __future__ import annotations

import sympy as sp

from canard_control.block_schur_response import block_schur_gap_response


def test_block_formula_equals_full_exact_solve_and_raw_gap_pairing() -> None:
    a = sp.Matrix([[2, 1], [0, 3]])
    b = sp.Matrix([[1], [2]])
    c = sp.Matrix([[3, -1]])
    d = sp.Matrix([[5]])
    g_critical = sp.Matrix([7, -2])
    g_transverse = sp.Matrix([4])
    gap_critical = sp.Matrix([[2, -3]])
    gap_transverse = sp.Matrix([[5]])
    explicit = sp.Rational(11, 7)

    response = block_schur_gap_response(
        a,
        b,
        c,
        d,
        g_critical,
        g_transverse,
        gap_critical,
        gap_transverse,
        explicit_gap_response=explicit,
    )

    full_operator = a.row_join(b).col_join(c.row_join(d))
    full_forcing = g_critical.col_join(g_transverse)
    full_response = -full_operator.inv() * full_forcing
    q_dot = full_response[:2, :]
    h_dot = full_response[2:, :]
    raw_gap_response = (
        explicit + (gap_critical * q_dot)[0] + (gap_transverse * h_dot)[0]
    )

    assert response.critical_response == q_dot
    assert response.transverse_response == h_dot
    assert sp.simplify(response.total_gap_response - raw_gap_response) == 0
    assert sp.simplify(
        response.total_gap_response
        - response.direct_gap_response
        - response.transverse_gap_response
    ) == 0


def test_critical_only_gap_reduces_to_the_short_schur_formula() -> None:
    a = sp.Matrix([[3]])
    b = sp.Matrix([[2]])
    c = sp.Matrix([[1]])
    d = sp.Matrix([[5]])
    g_critical = sp.Matrix([[7]])
    g_transverse = sp.Matrix([[11]])
    gap_critical = sp.Matrix([[13]])
    gap_transverse = sp.zeros(1, 1)

    response = block_schur_gap_response(
        a,
        b,
        c,
        d,
        g_critical,
        g_transverse,
        gap_critical,
        gap_transverse,
    )
    schur = a - b * d.inv() * c
    expected = (
        -gap_critical * schur.inv() * g_critical
        + gap_critical * schur.inv() * b * d.inv() * g_transverse
    )[0]

    assert sp.simplify(response.total_gap_response - expected) == 0


def test_strict_direct_sum_kills_projection_neutral_transverse_return() -> None:
    a = sp.Matrix([[2]])
    b = sp.zeros(1, 1)
    c = sp.zeros(1, 1)
    d = sp.Matrix([[3]])
    g_critical = sp.zeros(1, 1)
    g_transverse = sp.Matrix([[5]])
    gap_critical = sp.Matrix([[7]])
    gap_transverse = sp.zeros(1, 1)

    response = block_schur_gap_response(
        a,
        b,
        c,
        d,
        g_critical,
        g_transverse,
        gap_critical,
        gap_transverse,
    )

    assert response.critical_response == sp.zeros(1, 1)
    assert response.total_gap_response == 0

    # A direct transverse observation is a different mechanism and survives.
    observed = block_schur_gap_response(
        a,
        b,
        c,
        d,
        g_critical,
        g_transverse,
        gap_critical,
        sp.Matrix([[11]]),
    )
    assert observed.total_gap_response == -sp.Rational(55, 3)


def test_projection_neutral_direction_exposes_the_delta_cubed_return() -> None:
    delta, projected, direction = sp.symbols("delta projected direction")
    direct_three, return_block, transverse_source = sp.symbols(
        "direct_three return_block transverse_source"
    )

    response = block_schur_gap_response(
        sp.Matrix([[1]]),
        sp.Matrix([[delta * return_block]]),
        sp.zeros(1, 1),
        sp.Matrix([[1]]),
        sp.Matrix(
            [[
                delta**2 * projected * direction
                + delta**3 * direct_three * direction
            ]]
        ),
        sp.Matrix([[delta**2 * transverse_source * direction]]),
        sp.Matrix([[1]]),
        sp.zeros(1, 1),
    )

    expected = (
        -delta**2 * projected * direction
        + delta**3
        * (return_block * transverse_source - direct_three)
        * direction
    )
    assert sp.expand(response.total_gap_response - expected) == 0
    assert sp.expand(
        response.total_gap_response.subs(projected, 0)
        - delta**3
        * (return_block * transverse_source - direct_three)
        * direction
    ) == 0
