import math

from canard_control.unforced_separator_obstruction import (
    drifting_saddle_passage,
    exponential_offset_recovery_displacement,
    fixed_layer_miss_cutoff,
    log_fixed_layer_miss_cutoff,
)


def test_fixed_layer_blocks_miss_a_punctured_separator_neighborhood() -> None:
    parameters = {
        "unstable_rate": 2.0,
        "drift_magnitude": 0.5,
        "exit_coordinate": 0.25,
        "layer_tube_constant": 3.0,
    }
    cutoff = fixed_layer_miss_cutoff(**parameters)

    below = drifting_saddle_passage(
        epsilon=1.0e-4,
        reset_offset=0.5 * cutoff,
        **parameters,
    )
    above = drifting_saddle_passage(
        epsilon=1.0e-4,
        reset_offset=2.0 * cutoff,
        **parameters,
    )
    boundary = drifting_saddle_passage(
        epsilon=1.0e-4,
        reset_offset=cutoff,
        **parameters,
    )

    assert 0.0 < cutoff < parameters["exit_coordinate"]
    assert not below.reaches_fixed_layer_block
    assert below.recovery_displacement > below.recovery_tube_half_width
    assert not boundary.reaches_fixed_layer_block
    assert math.isclose(
        boundary.recovery_displacement,
        boundary.recovery_tube_half_width,
        rel_tol=1.0e-12,
    )
    assert above.reaches_fixed_layer_block
    assert above.recovery_displacement < above.recovery_tube_half_width


def test_layer_miss_cutoff_is_independent_of_epsilon() -> None:
    parameters = {
        "unstable_rate": 1.5,
        "drift_magnitude": 0.75,
        "exit_coordinate": 0.2,
        "layer_tube_constant": 2.0,
    }
    cutoff = fixed_layer_miss_cutoff(**parameters)
    offset = 0.25 * cutoff

    normalized_displacements = []
    for epsilon in (1.0e-2, 1.0e-4, 1.0e-8):
        passage = drifting_saddle_passage(
            epsilon=epsilon,
            reset_offset=offset,
            **parameters,
        )
        assert not passage.reaches_fixed_layer_block
        normalized_displacements.append(
            passage.recovery_displacement / epsilon
        )

    assert all(
        math.isclose(value, normalized_displacements[0])
        for value in normalized_displacements[1:]
    )


def test_log_cutoff_survives_binary64_underflow() -> None:
    log_cutoff = log_fixed_layer_miss_cutoff(
        unstable_rate=1000.0,
        drift_magnitude=1.0,
        exit_coordinate=1.0,
        layer_tube_constant=1.0,
    )
    assert log_cutoff == -1000.0
    try:
        fixed_layer_miss_cutoff(
            unstable_rate=1000.0,
            drift_magnitude=1.0,
            exit_coordinate=1.0,
            layer_tube_constant=1.0,
        )
    except OverflowError:
        pass
    else:
        raise AssertionError("binary64 cutoff underflow was not reported")


def test_exponentially_small_offsets_accumulate_order_one_drift() -> None:
    parameters = {
        "action": 0.8,
        "unstable_rate": 2.0,
        "drift_magnitude": 0.5,
        "exit_coordinate": 0.25,
    }
    expected_limit = (
        parameters["drift_magnitude"]
        * parameters["action"]
        / parameters["unstable_rate"]
    )
    errors = []
    for epsilon in (0.1, 0.05, 0.01):
        displacement = exponential_offset_recovery_displacement(
            epsilon=epsilon,
            **parameters,
        )
        errors.append(abs(displacement - expected_limit))

    assert errors[0] > errors[1] > errors[2]
    assert math.isclose(
        errors[0] / errors[1],
        2.0,
        rel_tol=1.0e-12,
    )
    assert math.isclose(
        errors[1] / errors[2],
        5.0,
        rel_tol=1.0e-12,
    )


def test_both_signs_have_the_same_layer_miss() -> None:
    parameters = {
        "epsilon": 1.0e-3,
        "unstable_rate": 1.0,
        "drift_magnitude": 0.8,
        "exit_coordinate": 0.1,
        "layer_tube_constant": 1.5,
    }
    cutoff = fixed_layer_miss_cutoff(
        unstable_rate=parameters["unstable_rate"],
        drift_magnitude=parameters["drift_magnitude"],
        exit_coordinate=parameters["exit_coordinate"],
        layer_tube_constant=parameters["layer_tube_constant"],
    )
    positive = drifting_saddle_passage(
        reset_offset=0.5 * cutoff,
        **parameters,
    )
    negative = drifting_saddle_passage(
        reset_offset=-0.5 * cutoff,
        **parameters,
    )

    assert positive == negative
    assert not positive.reaches_fixed_layer_block


def test_unforced_obstruction_helpers_reject_invalid_data() -> None:
    invalid_calls = (
        lambda: drifting_saddle_passage(
            epsilon=0.0,
            unstable_rate=1.0,
            drift_magnitude=1.0,
            exit_coordinate=1.0,
            reset_offset=0.5,
            layer_tube_constant=1.0,
        ),
        lambda: drifting_saddle_passage(
            epsilon=1.0,
            unstable_rate=1.0,
            drift_magnitude=1.0,
            exit_coordinate=1.0,
            reset_offset=1.0,
            layer_tube_constant=1.0,
        ),
        lambda: fixed_layer_miss_cutoff(
            unstable_rate=-1.0,
            drift_magnitude=1.0,
            exit_coordinate=1.0,
            layer_tube_constant=1.0,
        ),
        lambda: exponential_offset_recovery_displacement(
            epsilon=0.1,
            action=0.0,
            unstable_rate=1.0,
            drift_magnitude=1.0,
            exit_coordinate=1.0,
        ),
        lambda: exponential_offset_recovery_displacement(
            epsilon=1.0,
            action=0.1,
            unstable_rate=1.0,
            drift_magnitude=1.0,
            exit_coordinate=1.0e-100,
        ),
    )

    for invalid_call in invalid_calls:
        try:
            invalid_call()
        except ValueError:
            pass
        else:
            raise AssertionError("invalid obstruction data were accepted")
