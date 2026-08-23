import math

from scipy.integrate import solve_ivp

from canard_control.unforced_capture_audit import (
    deadband_capture_time_bound,
    fixed_layer_capture_critical_offset,
    middle_tracker_detector_audit,
    saturating_channel_capture_audit,
    saturating_channel_hit_time,
)


def test_physical_pulse_level_is_far_outside_the_reset_layer() -> None:
    result = middle_tracker_detector_audit()

    assert math.isclose(result.reset_middle_level, 0.8551590808270868)
    assert math.isclose(result.fold_level, 1.4259744889895694)
    assert math.isclose(result.crossing_a, -0.7101925627831396)
    assert math.isclose(
        result.crossing_collective_recovery,
        -0.9209995692926648,
        rel_tol=2.0e-14,
    )
    assert math.isclose(
        result.recovery_displacement,
        0.4209995692926648,
        rel_tol=2.0e-14,
    )
    assert result.outside_fixed_recovery_tube(
        epsilon=0.01,
        tube_factor=40.0,
    )
    assert not result.outside_fixed_recovery_tube(
        epsilon=0.01,
        tube_factor=50.0,
    )


def test_exact_saturating_channel_hit_time_matches_integration() -> None:
    initial = 0.07
    radius = 0.6
    exact_time = saturating_channel_hit_time(
        initial_offset=initial,
        target_radius=radius,
    )

    def rhs(_time: float, state: list[float]) -> list[float]:
        return [state[0] * (1.0 - state[0] ** 2)]

    def hit(_time: float, state: list[float]) -> float:
        return state[0] - radius

    hit.terminal = True  # type: ignore[attr-defined]
    hit.direction = 1.0  # type: ignore[attr-defined]
    solution = solve_ivp(
        rhs,
        (0.0, 20.0),
        [initial],
        events=hit,
        rtol=1.0e-12,
        atol=1.0e-14,
        max_step=0.01,
    )

    assert solution.t_events[0].size == 1
    assert math.isclose(
        exact_time,
        float(solution.t_events[0][0]),
        rel_tol=2.0e-11,
    )


def test_fixed_layer_capture_has_an_exact_punctured_no_hit_band() -> None:
    radius = 0.5
    tube_factor = 1.25
    drift = 0.8
    cutoff = fixed_layer_capture_critical_offset(
        target_radius=radius,
        recovery_tube_factor=tube_factor,
        slow_drift_speed=drift,
    )

    for epsilon in (0.1, 0.01, 1.0e-6):
        for sign in (-1.0, 1.0):
            miss = saturating_channel_capture_audit(
                epsilon=epsilon,
                initial_offset=sign * 0.9 * cutoff,
                target_radius=radius,
                recovery_tube_factor=tube_factor,
                slow_drift_speed=drift,
            )
            capture = saturating_channel_capture_audit(
                epsilon=epsilon,
                initial_offset=sign * 1.1 * cutoff,
                target_radius=radius,
                recovery_tube_factor=tube_factor,
                slow_drift_speed=drift,
            )

            assert not miss.fixed_layer_target_hit
            assert capture.fixed_layer_target_hit
            assert miss.assigned_channel != ""


def test_critical_offset_lands_exactly_on_recovery_tube_boundary() -> None:
    radius = 0.7
    tube_factor = 2.0
    drift = 1.5
    cutoff = fixed_layer_capture_critical_offset(
        target_radius=radius,
        recovery_tube_factor=tube_factor,
        slow_drift_speed=drift,
    )
    hit_time = saturating_channel_hit_time(
        initial_offset=cutoff,
        target_radius=radius,
    )

    assert math.isclose(hit_time, tube_factor / drift, rel_tol=2.0e-15)


def test_capture_cutoff_has_the_declared_large_tube_asymptotics() -> None:
    radius = 0.4
    prefactor = radius / math.sqrt(1.0 - radius**2)
    ratios = []
    for tube_factor in (2.0, 4.0, 8.0, 12.0):
        cutoff = fixed_layer_capture_critical_offset(
            target_radius=radius,
            recovery_tube_factor=tube_factor,
        )
        ratios.append(cutoff / (prefactor * math.exp(-tube_factor)))

    errors = [abs(ratio - 1.0) for ratio in ratios]
    assert errors[0] > errors[1] > errors[2] > errors[3]
    assert errors[-1] < 1.0e-9


def test_deadband_restores_a_finite_uniform_capture_time() -> None:
    radius = 0.6
    bound_small = deadband_capture_time_bound(
        deadband=0.05,
        target_radius=radius,
    )
    bound_large = deadband_capture_time_bound(
        deadband=0.1,
        target_radius=radius,
    )

    assert bound_small > bound_large > 0.0
    for initial in (0.1, 0.2, 0.4):
        assert saturating_channel_hit_time(
            initial_offset=initial,
            target_radius=radius,
        ) <= bound_large


def test_capture_helpers_reject_data_outside_their_contract() -> None:
    invalid_calls = (
        lambda: middle_tracker_detector_audit(pulse_level=0.5),
        lambda: middle_tracker_detector_audit(
            reset_collective_recovery=-2.0,
        ),
        lambda: saturating_channel_hit_time(
            initial_offset=0.0,
            target_radius=0.5,
        ),
        lambda: saturating_channel_hit_time(
            initial_offset=0.6,
            target_radius=0.5,
        ),
        lambda: fixed_layer_capture_critical_offset(
            target_radius=1.0,
            recovery_tube_factor=1.0,
        ),
        lambda: saturating_channel_capture_audit(
            epsilon=0.0,
            initial_offset=0.1,
        ),
        lambda: deadband_capture_time_bound(
            deadband=0.7,
            target_radius=0.6,
        ),
    )

    for invalid_call in invalid_calls:
        try:
            invalid_call()
        except ValueError:
            pass
        else:
            raise AssertionError("invalid U-CAP audit data were accepted")
