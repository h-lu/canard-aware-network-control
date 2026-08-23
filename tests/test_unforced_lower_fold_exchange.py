import math

from scipy.special import airy

from canard_control.unforced_lower_fold_exchange import (
    airy_fold_boundary_audit,
    airy_fold_coordinate,
    airy_repelling_state,
    airy_reset_offset_log,
    log_fold_visibility_scale,
    lower_fold_orientation_audit,
    lower_fold_rational_certificate,
    middle_branch_action,
)


def test_lower_fold_box_and_convexity_have_exact_rational_signs() -> None:
    result = lower_fold_rational_certificate()

    assert result.constraint_at_lower_corner > 0
    assert result.constraint_at_upper_corner < 0
    assert 10 * result.b_second_first_term_lower_bound > -11
    assert result.rho_second_bracket_lower_bound > 3
    assert result.certified


def test_physical_lower_fold_has_the_dynamic_saddle_node_orientation() -> None:
    result = lower_fold_orientation_audit(unfolding=0.0)

    assert -0.743 < result.fold_a < -0.742
    assert -1.174 < result.fold_b < -1.171
    assert result.recovery_second_derivative > 2.2
    assert result.strong_fast_eigenvalue < -3.3
    assert result.normal_quadratic_coefficient > 0.4
    assert result.collective_recovery_loading < -2.3
    assert result.slow_drift < -1.4
    assert result.ordinary_fold_orientation


def test_middle_branch_action_is_positive_and_has_the_declared_value() -> None:
    result = middle_branch_action(
        reset_collective_recovery=-0.5,
        unfolding=0.0,
    )

    assert math.isclose(result.reset_a, 0.023545664672220922)
    assert math.isclose(result.reset_collective_voltage, -0.8551590808270868)
    assert math.isclose(
        result.fold_collective_recovery,
        -0.9221564930989384,
    )
    assert math.isclose(result.action, 0.279268050491515, rel_tol=2e-12)
    assert result.quadrature_error < 1.0e-11


def test_physical_action_exposes_the_exponentially_small_fold_band() -> None:
    action = middle_branch_action().action
    log_scale = log_fold_visibility_scale(
        epsilon=0.01,
        action=action,
        algebraic_prefactor=1.0,
    )

    assert math.isclose(log_scale, -27.9268050491515, rel_tol=1e-13)
    assert 7.0e-13 < math.exp(log_scale) < 8.0e-13


def test_airy_negative_reset_side_splits_at_the_fold() -> None:
    epsilon = 0.01
    # Every c>0 is below the selected Bi trajectory at the reset section.
    for mixing in (0.5, 1.0, math.sqrt(3.0), 2.0):
        assert airy_reset_offset_log(
            epsilon=epsilon,
            entry_distance=0.5,
            airy_mixing=mixing,
        ) < 0.0

    selected_fold = airy_fold_coordinate(
        epsilon=epsilon,
        airy_mixing=0.0,
    )
    same_fold_side = airy_fold_coordinate(
        epsilon=epsilon,
        airy_mixing=1.0,
    )
    boundary = airy_fold_coordinate(
        epsilon=epsilon,
        airy_mixing=math.sqrt(3.0),
    )
    opposite_fold_side = airy_fold_coordinate(
        epsilon=epsilon,
        airy_mixing=2.0,
    )

    assert selected_fold > 0.0
    assert same_fold_side > 0.0
    assert abs(boundary) < 1.0e-15
    assert opposite_fold_side < 0.0


def test_airy_wronskian_reset_offset_formula_matches_direct_evaluation() -> None:
    epsilon = 0.1
    entry_distance = 0.5
    mixing = 1.25
    z = entry_distance / epsilon ** (2.0 / 3.0)
    ai, ai_prime, bi, bi_prime = airy(z)
    selected = epsilon ** (1.0 / 3.0) * bi_prime / bi
    mixed = epsilon ** (1.0 / 3.0) * (
        bi_prime + mixing * ai_prime
    ) / (bi + mixing * ai)
    direct_offset = mixed - selected
    log_formula = airy_reset_offset_log(
        epsilon=epsilon,
        entry_distance=entry_distance,
        airy_mixing=mixing,
    )

    assert direct_offset < 0.0
    assert math.isclose(
        math.log(abs(direct_offset)),
        log_formula,
        rel_tol=1.0e-13,
        abs_tol=1.0e-13,
    )


def test_airy_boundary_has_the_predicted_action_and_prefactor() -> None:
    audits = [
        airy_fold_boundary_audit(epsilon=epsilon, entry_distance=0.5)
        for epsilon in (0.05, 0.02, 0.01, 0.005)
    ]
    expected_action = 4.0 * 0.5 ** 1.5 / 3.0

    assert all(math.isclose(item.action, expected_action) for item in audits)
    assert all(item.selected_repelling_reset_state > 0.0 for item in audits)
    errors = [abs(item.asymptotic_ratio - 1.0) for item in audits]
    assert errors[0] > errors[1] > errors[2] > errors[3]
    assert audits[-1].asymptotic_ratio > 0.997


def test_airy_logarithmic_formula_survives_offset_underflow() -> None:
    result = airy_fold_boundary_audit(
        epsilon=1.0e-4,
        entry_distance=0.5,
    )

    assert result.log_absolute_reset_shift < -4000.0
    assert math.exp(result.log_absolute_reset_shift) == 0.0
    assert 0.999 < result.asymptotic_ratio < 1.001


def test_selected_airy_state_uses_scaled_functions_without_overflow() -> None:
    state = airy_repelling_state(
        epsilon=1.0e-6,
        distance_to_fold=0.5,
    )

    assert math.isfinite(state)
    assert math.isclose(state, math.sqrt(0.5), rel_tol=1.0e-5)


def test_lower_fold_helpers_reject_data_outside_their_contract() -> None:
    invalid_calls = (
        lambda: lower_fold_orientation_audit(unfolding=float("nan")),
        lambda: middle_branch_action(reset_collective_recovery=-1.0),
        lambda: middle_branch_action(
            reset_collective_recovery=-0.5,
            unfolding=-1.0,
        ),
        lambda: log_fold_visibility_scale(epsilon=0.0, action=1.0),
        lambda: log_fold_visibility_scale(epsilon=1.0, action=-1.0),
        lambda: airy_repelling_state(
            epsilon=1.0,
            distance_to_fold=-1.0,
        ),
        lambda: airy_fold_coordinate(epsilon=1.0, airy_mixing=-1.0),
        lambda: airy_reset_offset_log(
            epsilon=1.0,
            entry_distance=1.0,
            airy_mixing=0.0,
        ),
        lambda: airy_fold_boundary_audit(
            epsilon=1.0,
            entry_distance=0.0,
        ),
    )

    for invalid_call in invalid_calls:
        try:
            invalid_call()
        except ValueError:
            pass
        else:
            raise AssertionError("invalid lower-fold data were accepted")
