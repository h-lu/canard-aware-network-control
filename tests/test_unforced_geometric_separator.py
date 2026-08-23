import math

import numpy as np

from canard_control.unforced_geometric_separator import (
    dominated_trichotomy_budget,
    green_roughness_budget,
    log_outer_error_at_reset,
    log_required_incoming_error,
    reset_layer_geometry,
    separator_root_radius_bound,
)


def test_reset_layer_geometry_and_unstable_pairing() -> None:
    geometry = reset_layer_geometry(-0.5)
    point = geometry.middle_point
    right = np.array(geometry.right_unstable_vector)
    left = np.array(geometry.left_unstable_covector)

    assert math.isclose(
        point.collective_recovery,
        -0.5,
        rel_tol=0.0,
        abs_tol=2.0e-13,
    )
    assert point.critical_voltage < 0.0
    assert point.unstable_eigenvalue > 0.0
    assert np.all(right > 0.0)
    assert np.all(left > 0.0)
    assert math.isclose(float(np.linalg.norm(right)), 1.0, rel_tol=1.0e-13)
    assert math.isclose(float(left @ right), 1.0, rel_tol=1.0e-13)
    jacobian = np.array(
        [
            [0.5 - point.voltage_1**2, 0.5],
            [2.0, -1.0 - point.voltage_2**2],
        ]
    )
    assert np.linalg.norm(
        jacobian @ right - point.unstable_eigenvalue * right
    ) < 2.0e-13
    assert np.linalg.norm(
        left @ jacobian - point.unstable_eigenvalue * left
    ) < 2.0e-13
    assert math.isclose(
        geometry.repelling_action_from_right_fold,
        0.5607898753226717,
        rel_tol=2.0e-11,
    )


def test_outer_action_rejects_algebraic_and_weaker_flat_matching() -> None:
    action = reset_layer_geometry(-0.5).repelling_action_from_right_fold
    polynomial_logs = []
    weaker_flat_logs = []
    for delta in (0.2, 0.1, 0.05):
        epsilon = delta**2
        polynomial_logs.append(
            log_outer_error_at_reset(
                log_incoming_error=12.0 * math.log(delta),
                repelling_action_value=action,
                epsilon=epsilon,
            )
        )
        weaker_flat_logs.append(
            log_outer_error_at_reset(
                log_incoming_error=-2.0 / delta,
                repelling_action_value=action,
                epsilon=epsilon,
            )
        )

    assert polynomial_logs[0] < polynomial_logs[1] < polynomial_logs[2]
    assert weaker_flat_logs[0] < weaker_flat_logs[1] < weaker_flat_logs[2]
    assert polynomial_logs[-1] > 0.0
    assert weaker_flat_logs[-1] > 0.0


def test_action_supercritical_matching_survives_to_reset() -> None:
    action = reset_layer_geometry(-0.5).repelling_action_from_right_fold
    margin = 0.08
    for delta in (0.2, 0.1, 0.05):
        epsilon = delta**2
        log_outgoing = log_outer_error_at_reset(
            log_incoming_error=-(action + margin) / epsilon,
            repelling_action_value=action,
            epsilon=epsilon,
        )
        assert math.isclose(log_outgoing, -margin / epsilon)


def test_required_incoming_error_is_sharp_in_scalar_normal_model() -> None:
    action = 0.4
    epsilon = 0.02
    radius = 0.03
    threshold = log_required_incoming_error(
        reset_tube_radius=radius,
        repelling_action_value=action,
        epsilon=epsilon,
    )
    outgoing = log_outer_error_at_reset(
        log_incoming_error=threshold,
        repelling_action_value=action,
        epsilon=epsilon,
    )
    assert math.isclose(outgoing, math.log(radius), rel_tol=1.0e-13)


def test_dominated_trichotomy_budget_keeps_weak_stable_modes() -> None:
    closes = dominated_trichotomy_budget(
        base_unstable_rate=0.8,
        base_center_stable_growth_rate=0.02,
        roughness_rate_loss=0.05,
    )
    fails = dominated_trichotomy_budget(
        base_unstable_rate=0.2,
        base_center_stable_growth_rate=0.12,
        roughness_rate_loss=0.05,
    )

    assert closes.closes
    assert math.isclose(closes.unstable_rate, 0.75)
    assert math.isclose(closes.center_stable_growth_rate, 0.07)
    assert math.isclose(closes.domination_gap, 0.68)
    assert not fails.closes
    assert fails.domination_gap < 0.0


def test_weighted_green_roughness_criterion() -> None:
    closes = green_roughness_budget(
        evolution_bound=2.0,
        base_center_stable_growth_rate=0.05,
        base_unstable_rate=0.85,
        admissible_perturbation_norm=0.04,
    )
    fails = green_roughness_budget(
        evolution_bound=2.0,
        base_center_stable_growth_rate=0.05,
        base_unstable_rate=0.85,
        admissible_perturbation_norm=0.12,
    )

    assert math.isclose(closes.weight, 0.45)
    assert math.isclose(closes.contraction_constant, 0.4)
    assert closes.closes
    assert math.isclose(fails.contraction_constant, 1.2)
    assert not fails.closes


def test_separator_root_bound_is_linear_in_history_residual() -> None:
    assert math.isclose(
        separator_root_radius_bound(
            defining_function_residual=3.0e-4,
            reset_derivative_floor=0.6,
        ),
        5.0e-4,
    )


def test_unforced_geometric_helpers_reject_invalid_data() -> None:
    invalid_calls = (
        lambda: reset_layer_geometry(2.0),
        lambda: log_outer_error_at_reset(
            log_incoming_error=-1.0,
            repelling_action_value=0.0,
            epsilon=0.01,
        ),
        lambda: log_required_incoming_error(
            reset_tube_radius=0.0,
            repelling_action_value=1.0,
            epsilon=0.01,
        ),
        lambda: dominated_trichotomy_budget(
            base_unstable_rate=1.0,
            base_center_stable_growth_rate=-0.1,
            roughness_rate_loss=0.1,
        ),
        lambda: green_roughness_budget(
            evolution_bound=1.0,
            base_center_stable_growth_rate=0.2,
            base_unstable_rate=0.1,
            admissible_perturbation_norm=0.01,
        ),
        lambda: separator_root_radius_bound(
            defining_function_residual=1.0,
            reset_derivative_floor=0.0,
        ),
    )

    for invalid_call in invalid_calls:
        try:
            invalid_call()
        except ValueError:
            pass
        else:
            raise AssertionError("invalid Gate U-SF audit data were accepted")
