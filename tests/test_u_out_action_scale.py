import math

from canard_control.u_out_action_scale import (
    exp_if_representable,
    logarithmic_tube_action_audit,
    minimum_logarithmic_power_for_action_scale,
    oscillatory_complete_history_audit,
    oscillatory_root_jet_log_bound,
    terminal_root_jet_budget,
)


def test_fixed_logarithmic_tube_is_action_subcritical() -> None:
    audits = [
        logarithmic_tube_action_audit(
            delta=delta,
            logarithmic_power=12.0,
            action=0.08,
            action_margin=0.02,
            gaussian_loss_constant=0.7,
            local_polynomial_loss=3.0,
            action_polynomial_loss=4.0,
            action_delay_loss=0.2,
        )
        for delta in (0.08, 0.05, 0.03, 0.02)
    ]

    assert all(not audit.action_scale_certified for audit in audits[-2:])
    assert audits[-1].log_scale_ratio > audits[-2].log_scale_ratio
    assert audits[-1].physical_fold_radius < audits[-2].physical_fold_radius


def test_required_logarithmic_power_diverges_at_outer_action_rate() -> None:
    powers = [
        minimum_logarithmic_power_for_action_scale(
            delta=delta,
            action=0.08,
            action_margin=0.02,
            gaussian_loss_constant=0.4,
            local_polynomial_loss=2.0,
            action_polynomial_loss=3.0,
            action_delay_loss=0.1,
        )
        for delta in (0.08, 0.05, 0.03, 0.02)
    ]

    assert powers[0] < powers[1] < powers[2] < powers[3]
    delta = 0.02
    asymptotic_scale = 0.10 / (delta**2 * math.log(1.0 / delta))
    assert powers[-1] / asymptotic_scale > 0.75


def test_computed_minimum_power_really_closes_the_displayed_budget() -> None:
    data = {
        "delta": 0.04,
        "action": 0.06,
        "action_margin": 0.01,
        "gaussian_loss_constant": 0.3,
        "local_polynomial_loss": 1.0,
        "action_polynomial_loss": 2.0,
        "action_delay_loss": 0.05,
        "local_prefactor": 1.7,
        "action_prefactor": 0.8,
    }
    power = minimum_logarithmic_power_for_action_scale(**data)
    audit = logarithmic_tube_action_audit(
        logarithmic_power=power * (1.0 + 1.0e-10),
        **data,
    )

    assert audit.action_scale_certified
    assert audit.log_scale_ratio < 0.0


def test_value_closure_and_parameter_jet_are_independent() -> None:
    delta = 0.05
    action = 0.08
    margin = 0.02
    log_d = -action / delta**2
    log_r = -(action + margin) / delta**2
    # The value residual gives an exponentially tiny root.
    # An arbitrarily oscillatory parameter selection makes its derivative
    # exponentially large without changing either value hypothesis.
    log_omega = 2.0 * margin / delta**2
    log_jet = oscillatory_root_jet_log_bound(
        log_derivative=log_d,
        log_residual_amplitude=log_r,
        log_parameter_frequency=log_omega,
    )
    budget = terminal_root_jet_budget(
        log_derivative_floor=log_d,
        log_value_residual_bound=log_r,
        log_parameter_residual_bound=log_r + log_omega,
        terminal_radius=1.0,
    )

    assert budget.root_closes
    assert math.isclose(budget.log_root_bound, -margin / delta**2)
    assert math.isclose(budget.log_parameter_root_derivative_bound, log_jet)
    assert log_jet > 0.0
    assert exp_if_representable(log_jet) > 1.0


def test_oscillatory_counterexample_is_a_complete_history_identity() -> None:
    audit = oscillatory_complete_history_audit(
        delta=0.2,
        action=0.2,
        action_margin=0.05,
        delay_length=3.0,
        parameter=0.07,
        terminal_coordinate=0.1,
    )

    assert math.isclose(
        abs(audit.current_mismatch), audit.history_sup_mismatch
    )
    assert audit.oldest_history_mismatch < audit.history_sup_mismatch
    assert (
        audit.canonical_history_parameter_jet
        < audit.terminal_coordinate_parameter_jet
    )


def test_action_audit_is_stable_for_small_representable_reciprocal() -> None:
    audit = logarithmic_tube_action_audit(
        delta=1.0e-200,
        logarithmic_power=12.0,
        action=0.08,
        action_margin=0.02,
        action_delay_loss=0.2,
    )

    assert audit.log_action_residual_target == float("-inf")
    assert audit.log_scale_ratio == float("inf")
    assert not audit.action_scale_certified


def test_zero_minimum_power_is_an_infimum_not_an_admissible_power() -> None:
    data = {
        "delta": 0.5,
        "action": 0.01,
        "action_delay_loss": 100.0,
    }
    infimum = minimum_logarithmic_power_for_action_scale(**data)
    audit = logarithmic_tube_action_audit(
        logarithmic_power=1.0e-12,
        **data,
    )

    assert infimum == 0.0
    assert audit.action_scale_certified


def test_gaussian_loss_creates_positive_threshold_at_zero_drop() -> None:
    data = {
        "delta": 0.5,
        "action": 0.01,
        "action_delay_loss": 0.02,
        "gaussian_loss_constant": 1.0,
    }
    power = minimum_logarithmic_power_for_action_scale(**data)
    expected = 2.0 / math.log(2.0)
    below = logarithmic_tube_action_audit(
        logarithmic_power=0.99 * power,
        **data,
    )
    above = logarithmic_tube_action_audit(
        logarithmic_power=1.01 * power,
        **data,
    )

    assert math.isclose(power, expected)
    assert not below.action_scale_certified
    assert above.action_scale_certified


def test_exact_zero_residual_and_parameter_residual_have_zero_budgets() -> None:
    budget = terminal_root_jet_budget(
        log_derivative_floor=-100.0,
        log_value_residual_bound=float("-inf"),
        log_parameter_residual_bound=float("-inf"),
        terminal_radius=0.5,
    )

    assert budget.root_closes
    assert budget.log_root_bound == float("-inf")
    assert budget.log_parameter_root_derivative_bound == float("-inf")
    assert exp_if_representable(budget.log_root_bound) == 0.0


def test_action_scale_helpers_reject_invalid_data() -> None:
    invalid_calls = (
        lambda: logarithmic_tube_action_audit(
            delta=1.0,
            logarithmic_power=4.0,
            action=0.1,
        ),
        lambda: logarithmic_tube_action_audit(
            delta=0.1,
            logarithmic_power=0.0,
            action=0.1,
        ),
        lambda: minimum_logarithmic_power_for_action_scale(
            delta=0.1,
            action=-0.1,
        ),
        lambda: logarithmic_tube_action_audit(
            delta=5.0e-324,
            logarithmic_power=4.0,
            action=5.0e-324,
            action_delay_loss=2.0,
        ),
        lambda: oscillatory_complete_history_audit(
            delta=1.0e-200,
            action=0.2,
            action_margin=0.05,
            delay_length=1.0,
            parameter=0.0,
            terminal_coordinate=0.0,
        ),
        lambda: terminal_root_jet_budget(
            log_derivative_floor=float("-inf"),
            log_value_residual_bound=-1.0,
            log_parameter_residual_bound=-1.0,
            terminal_radius=1.0,
        ),
        lambda: oscillatory_root_jet_log_bound(
            log_derivative=0.0,
            log_residual_amplitude=0.0,
            log_parameter_frequency=float("inf"),
        ),
    )

    for invalid_call in invalid_calls:
        try:
            invalid_call()
        except ValueError:
            pass
        else:
            raise AssertionError("invalid U-OUT action-scale data accepted")
