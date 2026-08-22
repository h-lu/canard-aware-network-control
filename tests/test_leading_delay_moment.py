import sympy as sp

from canard_control.leading_delay_moment import (
    leading_delay_coefficients,
    leading_distributed_delay_coefficients,
)


def test_first_delayed_canard_coefficients() -> None:
    X, K, Theta = sp.symbols("X K Theta")
    result = leading_delay_coefficients()

    assert sp.simplify(result.critical_graph_0 - (X**2 - sp.Rational(1, 2))) == 0
    assert sp.simplify(result.delayed_state_0 - (X + Theta / 2)) == 0
    assert sp.simplify(
        result.critical_graph_1
        - (X**3 / 3 + X / 4 + K * Theta / 2)
    ) == 0
    assert sp.simplify(result.fast_field_1 - X / 4) == 0
    assert sp.simplify(
        result.delayed_state_1 + Theta * (Theta + 4 * X) / 16
    ) == 0
    assert sp.simplify(
        result.critical_graph_2
        - (
            -X**2 / 8
            - K * Theta * X / 4
            - K * Theta**2 / 16
            - sp.Rational(3, 32)
        )
    ) == 0
    assert result.nu_0 == -sp.Rational(1, 8)
    assert sp.simplify(result.nu_1 - K * Theta / 8) == 0


def test_row_equivalent_distributed_delay_selects_only_first_moment() -> None:
    X, K, m_1, m_2 = sp.symbols("X K m_1 m_2")
    result = leading_distributed_delay_coefficients()

    assert sp.simplify(
        result.critical_graph_1
        - (X**3 / 3 + X / 4 + K * m_1 / 2)
    ) == 0
    assert sp.simplify(result.fast_field_1 - X / 4) == 0
    assert sp.simplify(
        result.mean_delayed_state_1 + (m_2 + 4 * X * m_1) / 16
    ) == 0
    assert sp.simplify(
        result.critical_graph_2
        - (
            -X**2 / 8
            - K * m_1 * X / 4
            - K * m_2 / 16
            - sp.Rational(3, 32)
        )
    ) == 0
    assert result.nu_0 == -sp.Rational(1, 8)
    assert sp.simplify(result.nu_1 - K * m_1 / 8) == 0
    assert not result.nu_1.has(m_2)
