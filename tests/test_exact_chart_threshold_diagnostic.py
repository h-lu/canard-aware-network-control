import numpy as np
import pytest

pytest.importorskip("scipy")

from canard_control.exact_chart_threshold_diagnostic import (
    ExactChartParameters,
    alpha_value,
    exact_chart_rhs,
    integrate_exact_chart,
    ks_hamiltonian,
    ks_normalized_energy_gap,
    leading_canard_state,
    threshold_coefficient_row,
)


def test_leading_canard_is_on_the_zero_hamiltonian_level() -> None:
    for inner_time in (-4.0, -1.0, 0.0, 2.5, 4.0):
        chart_x, chart_y, _, _ = leading_canard_state(inner_time, 1.5)
        assert abs(ks_normalized_energy_gap(chart_x, chart_y)) < 2.0e-14
        assert abs(ks_hamiltonian(chart_x, chart_y)) < 2.0e-14


def test_method_of_steps_returns_finite_exact_chart_state() -> None:
    result = integrate_exact_chart(
        ExactChartParameters(delta=0.1),
        eta=0.01,
        nu=-0.35,
        section_half_width=1.0,
        rtol=2.0e-7,
        atol=2.0e-9,
    )

    assert result.segment_count == 4
    assert result.function_evaluations > 0
    assert np.all(np.isfinite(result.final_state))
    assert np.isfinite(result.normalized_energy_gap)


def test_method_of_steps_matches_direct_ode_when_delay_gain_is_zero() -> None:
    from scipy.integrate import solve_ivp

    parameters = ExactChartParameters(delta=0.08, weak_gain=0.0)
    eta = 0.03
    nu = -0.4
    section_half_width = 0.75
    initial = leading_canard_state(
        -section_half_width, parameters.recovery_gap
    )

    stepped = integrate_exact_chart(
        parameters,
        eta=eta,
        nu=nu,
        section_half_width=section_half_width,
        rtol=2.0e-9,
        atol=2.0e-11,
    )
    direct = solve_ivp(
        lambda _time, state: exact_chart_rhs(
            state,
            np.zeros(4),
            np.zeros(4),
            parameters=parameters,
            eta=eta,
            nu=nu,
        ),
        (-section_half_width, section_half_width),
        initial,
        method="Radau",
        rtol=2.0e-9,
        atol=2.0e-11,
    )

    assert direct.success
    assert stepped.final_state == pytest.approx(direct.y[:, -1], abs=2.0e-9)


def test_diagnostic_central_quotient_has_predicted_sign_and_scale() -> None:
    row = threshold_coefficient_row(
        ExactChartParameters(delta=0.02),
        eta_step=0.04,
        section_half_width=3.5,
        rtol=2.0e-8,
        atol=2.0e-10,
    )
    predicted = -1.0 / (8.0 * alpha_value())

    assert row.predicted_coefficient == pytest.approx(predicted)
    assert row.quotient_plus < 0.0
    assert row.quotient_minus < 0.0
    assert row.quotient_central == pytest.approx(predicted, rel=0.025)
    assert abs(row.quotient_plus - row.quotient_minus) < 2.0e-5
    assert row.root_residual_max < 2.0e-7
