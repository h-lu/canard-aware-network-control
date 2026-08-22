import sympy as sp

from canard_control.symbolic_blowup import delayed_vdp_blowup


def test_delayed_vdp_right_fold_scaling_is_exact() -> None:
    delta, X, X_tau, Y, K, nu = sp.symbols(
        "delta X X_tau Y K nu", nonzero=True
    )
    result = delayed_vdp_blowup()

    expected_local = delta**2 * (Y - X**2) - delta**3 * X**3 / 3
    expected_delay = delta**3 * K * (X - X_tau)
    expected_slow = -delta**3 * X + delta**4 * nu
    expected_fast_scaled = Y - X**2 + delta * (
        -X**3 / 3 + K * (X - X_tau)
    )
    expected_slow_scaled = -X + delta * nu

    assert sp.simplify(result.local_fast_rhs - expected_local) == 0
    assert sp.simplify(result.delayed_fast_rhs - expected_delay) == 0
    assert sp.simplify(result.slow_rhs - expected_slow) == 0
    assert sp.simplify(result.scaled_fast_rhs - expected_fast_scaled) == 0
    assert sp.simplify(result.scaled_slow_rhs - expected_slow_scaled) == 0
