import numpy as np
import sympy as sp

from canard_control.physical_pulse_bridge import (
    equilibria_at_recovery,
    fast_channel_falsifier,
    fold_points,
    physical_pulse_bridge_audit,
    repelling_action,
)


def test_singular_fast_field_is_weighted_gradient() -> None:
    result = physical_pulse_bridge_audit()

    assert result.weighted_gradient_residual == sp.zeros(2, 1)
    v_1, v_2 = result.voltage_1, result.voltage_2
    f_1, f_2 = result.fast_field
    potential_derivative = sp.expand(
        sp.diff(result.potential, v_1) * f_1
        + sp.diff(result.potential, v_2) * f_2
    )
    assert sp.simplify(potential_derivative + 4 * f_1**2 + f_2**2) == 0


def test_critical_curve_is_one_graph_with_exactly_two_folds() -> None:
    result = physical_pulse_bridge_audit()
    a = result.scaled_voltage_1
    b = result.scaled_voltage_2

    assert result.critical_constraint_b_derivative == -3 * b**2 - 4
    assert result.fold_resultant_real_root_count == 2
    assert result.left_fold_resultant_interval_root_count == 1
    assert result.left_fold_real_lift_certified
    assert result.determinant_fold_residual == 0
    assert sp.simplify(
        result.critical_constraint.subs({a: 1, b: 0})
    ) == 0
    assert sp.simplify(result.fold_equation.subs({a: 1, b: 0})) == 0

    left, local = fold_points()
    assert -0.743 < left.a < -0.742
    assert -1.427 < left.critical_voltage < -1.425
    assert -0.923 < left.collective_recovery < -0.921
    assert abs(local.a - 1.0) < 1e-14
    assert abs(local.critical_voltage) < 1e-14
    assert abs(local.collective_recovery) < 1e-14
    left_substitutions = {
        a: sp.Float(left.a, 30),
        b: sp.Float(left.b, 30),
    }
    assert abs(float(result.critical_constraint.subs(left_substitutions))) < 1e-12
    assert abs(float(result.fold_equation.subs(left_substitutions))) < 1e-12
    assert float(result.left_fold_b_squared.subs(a, left.a)) > 0


def test_reference_bistable_layer_has_two_stable_nodes_and_one_saddle() -> None:
    lower, saddle, upper = equilibria_at_recovery(-0.5)

    assert lower.critical_voltage < saddle.critical_voltage < 0
    assert 0 < upper.critical_voltage
    assert lower.fast_determinant > 0
    assert saddle.fast_determinant < 0
    assert upper.fast_determinant > 0
    assert lower.fast_trace < 0
    assert saddle.fast_trace < 0
    assert upper.fast_trace < 0


def test_equilibrium_solver_retains_near_fold_pairs_and_far_roots() -> None:
    left, _ = fold_points()
    near_fold = equilibria_at_recovery(left.collective_recovery + 1e-8)
    at_fold = equilibria_at_recovery(left.collective_recovery)
    far_field = equilibria_at_recovery(100.0)

    assert len(near_fold) == 3
    assert len(at_fold) == 2
    assert len(far_field) == 1
    assert abs(
        far_field[0].collective_recovery - 100.0
    ) < 1e-9


def test_weighted_pulse_and_quiet_sections_are_crossed_transversely() -> None:
    pulse, quiet = fast_channel_falsifier()

    assert abs(pulse.hit_critical_voltage + 1.4) < 1e-8
    assert pulse.hit_speed < -0.1
    assert pulse.endpoint_error < 1e-7
    assert pulse.maximum_potential_increase < 1e-10

    assert abs(quiet.hit_critical_voltage) < 1e-8
    assert quiet.hit_speed > 0.1
    assert quiet.endpoint_error < 1e-7
    assert quiet.maximum_potential_increase < 1e-10


def test_repelling_action_is_positive_and_has_expected_value() -> None:
    a_h, action = repelling_action(1.0)

    assert -0.181 < a_h < -0.179
    assert np.isclose(action, 0.7047846185619534, rtol=1e-10)


def test_repelling_action_accepts_levels_close_to_both_folds() -> None:
    left, _ = fold_points()
    maximum_level = -left.critical_voltage
    near_zero = repelling_action(1e-12)
    near_left = repelling_action(maximum_level - 1e-12)

    for a_h, action in (near_zero, near_left):
        assert left.a <= a_h <= 1.0
        assert np.isfinite(action)
        assert action >= 0.0
