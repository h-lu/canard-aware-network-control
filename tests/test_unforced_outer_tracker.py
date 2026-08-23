import math

import sympy as sp

from canard_control.unforced_geometric_separator import reset_layer_geometry
from canard_control.unforced_outer_tracker import (
    action_supercritical_terminal_budget,
    causal_outer_bounds,
    log_terminal_coordinate,
    scalar_terminal_matching_identity,
    terminal_matching_budget,
    terminal_root_radius_from_log_budget,
)


def test_scalar_terminal_trace_identity_is_exact() -> None:
    identity = scalar_terminal_matching_identity()

    assert identity.round_trip_residual == 0
    assert identity.incoming_from_terminal == (
        identity.terminal_coordinate
        * sp.exp(-identity.action / identity.epsilon)
    )
    assert identity.terminal_required_by_incoming == (
        identity.incoming_coordinate
        * sp.exp(identity.action / identity.epsilon)
    )


def test_monotone_outer_bounds_record_delay_direction_and_hit_time() -> None:
    bounds = causal_outer_bounds(
        delta=0.1,
        maximum_scaled_delay=2.0,
        recovery_speed_floor=0.25,
        recovery_speed_ceiling=1.0,
        overlap_recovery=-0.02,
        reset_recovery=-0.5,
    )

    assert math.isclose(bounds.slow_time_delay, 0.2)
    assert math.isclose(bounds.maximum_recovery_backtrack, 0.2)
    assert math.isclose(bounds.maximum_fast_hit_time, 192.0)


def test_exact_zero_incoming_coordinate_needs_no_terminal_correction() -> None:
    log_beta = log_terminal_coordinate(
        log_absolute_incoming_coordinate=float("-inf"),
        action=0.25,
        epsilon=0.01,
    )
    budget = terminal_matching_budget(
        log_derivative_floor=-100.0,
        log_reference_mismatch_bound=float("-inf"),
        terminal_radius=1.0,
    )

    assert log_beta == float("-inf")
    assert budget.closes
    assert terminal_root_radius_from_log_budget(budget) == 0.0


def test_algebraic_and_delay_exponential_errors_are_action_subcritical() -> None:
    action = reset_layer_geometry(-0.5).repelling_action_from_right_fold
    delta = 0.04
    epsilon = delta**2
    fixed_terminal_radius = 1.0

    algebraic_log_beta = log_terminal_coordinate(
        log_absolute_incoming_coordinate=4.0 * math.log(delta),
        action=action,
        epsilon=epsilon,
    )
    delay_exponential_log_beta = log_terminal_coordinate(
        log_absolute_incoming_coordinate=-1.0 / delta,
        action=action,
        epsilon=epsilon,
    )

    assert algebraic_log_beta > math.log(fixed_terminal_radius)
    assert delay_exponential_log_beta > math.log(fixed_terminal_radius)


def test_action_supercritical_margin_beats_polynomial_and_delay_losses() -> None:
    action = reset_layer_geometry(-0.5).repelling_action_from_right_fold
    budgets = [
        action_supercritical_terminal_budget(
            delta=delta,
            action=action,
            action_margin=0.08,
            derivative_delay_loss_constant=0.25,
            residual_delay_loss_constant=0.15,
            derivative_polynomial_power=3.0,
            residual_polynomial_power=4.0,
            derivative_prefactor=0.5,
            residual_prefactor=2.0,
            terminal_radius=0.75,
        )
        for delta in (0.08, 0.06, 0.04, 0.03)
    ]

    root_logs = [budget.log_root_radius_bound for budget in budgets]
    expected_first_log = (
        math.log(2.0 / 0.5)
        - 7.0 * math.log(0.08)
        - 0.08 / 0.08**2
        + (0.25 + 0.15) / 0.08
    )
    assert math.isclose(root_logs[0], expected_first_log)
    assert root_logs[0] > root_logs[1] > root_logs[2] > root_logs[3]
    assert budgets[-1].closes
    assert terminal_root_radius_from_log_budget(budgets[-1]) < 0.75


def test_generic_terminal_budget_uses_the_exact_ratio() -> None:
    budget = terminal_matching_budget(
        log_derivative_floor=-12.0,
        log_reference_mismatch_bound=-15.0,
        terminal_radius=0.1,
    )

    assert math.isclose(budget.log_root_radius_bound, -3.0)
    assert budget.closes
    assert math.isclose(
        terminal_root_radius_from_log_budget(budget),
        math.exp(-3.0),
    )


def test_outer_tracker_helpers_reject_data_outside_their_contract() -> None:
    invalid_calls = (
        lambda: causal_outer_bounds(
            delta=0.0,
            maximum_scaled_delay=2.0,
            recovery_speed_floor=0.25,
            recovery_speed_ceiling=1.0,
            overlap_recovery=-0.02,
            reset_recovery=-0.5,
        ),
        lambda: causal_outer_bounds(
            delta=0.1,
            maximum_scaled_delay=2.0,
            recovery_speed_floor=1.1,
            recovery_speed_ceiling=1.0,
            overlap_recovery=-0.02,
            reset_recovery=-0.5,
        ),
        lambda: causal_outer_bounds(
            delta=0.1,
            maximum_scaled_delay=2.0,
            recovery_speed_floor=0.25,
            recovery_speed_ceiling=1.0,
            overlap_recovery=-0.5,
            reset_recovery=-0.02,
        ),
        lambda: log_terminal_coordinate(
            log_absolute_incoming_coordinate=0.0,
            action=0.0,
            epsilon=0.01,
        ),
        lambda: terminal_matching_budget(
            log_derivative_floor=float("-inf"),
            log_reference_mismatch_bound=-1.0,
            terminal_radius=1.0,
        ),
        lambda: action_supercritical_terminal_budget(
            delta=0.1,
            action=1.0,
            action_margin=0.0,
            derivative_delay_loss_constant=0.0,
            residual_delay_loss_constant=0.0,
            derivative_polynomial_power=0.0,
            residual_polynomial_power=0.0,
        ),
        lambda: action_supercritical_terminal_budget(
            delta=0.1,
            action=1.0,
            action_margin=0.1,
            derivative_delay_loss_constant=0.0,
            residual_delay_loss_constant=-0.1,
            derivative_polynomial_power=0.0,
            residual_polynomial_power=0.0,
        ),
    )

    for invalid_call in invalid_calls:
        try:
            invalid_call()
        except ValueError:
            pass
        else:
            raise AssertionError("invalid U-OUT data were accepted")
