import math

import sympy as sp

from canard_control.causal_reset_separator import (
    causal_reset_audit,
    maximal_physical_delay,
    recovery_endpoint_error,
    reset_memory_margin,
    simple_root_transfer_certificate,
)


def test_voltage_hold_generates_the_declared_complete_history() -> None:
    result = causal_reset_audit()

    assert result.constant_voltage_delay_residual == sp.zeros(2, 1)
    assert result.recovery_history_residual == sp.zeros(2, 1)
    assert result.history_endpoint_residual == sp.zeros(2, 1)
    assert result.reset_modal_endpoint == sp.Matrix(
        [
            result.critical_setpoint,
            result.transverse_setpoint,
            result.terminal_collective_recovery,
            result.delta**2
            * result.transverse_setpoint
            / result.recovery_gap,
        ]
    )


def test_reset_controls_are_nondegenerate_at_release() -> None:
    result = causal_reset_audit()

    assert result.reset_parameter_rank == 3
    assert result.critical_recovery_injection == -1
    assert result.transverse_recovery_injection == 0
    assert sp.simplify(
        result.release_critical_fast_field.subs(
            {
                result.critical_setpoint: 0,
                result.transverse_setpoint: 0,
                result.terminal_collective_recovery: 0,
            }
        )
    ) == 0


def test_one_maximal_delay_is_the_sharp_memory_overwrite_duration() -> None:
    delta = 0.1
    delays = (0.4, 1.3, 0.7)
    required = maximal_physical_delay(delta, delays)

    assert math.isclose(required, 13.0)
    assert reset_memory_margin(
        required,
        delta=delta,
        scaled_delays=delays,
    ) == 0.0
    assert reset_memory_margin(
        required + 2.0,
        delta=delta,
        scaled_delays=delays,
    ) == 2.0
    assert reset_memory_margin(
        required - 0.25,
        delta=delta,
        scaled_delays=delays,
    ) < 0.0


def test_voltage_hold_does_not_erase_collective_recovery_error() -> None:
    collective, transverse = recovery_endpoint_error(
        7.0,
        recovery_gap=2.0,
        initial_collective_error=0.125,
        initial_transverse_error=-0.5,
    )

    assert collective == 0.125
    assert math.isclose(transverse, -0.5 * math.exp(-14.0))


def test_simple_root_transfer_certificate_has_the_sharp_margin_bound() -> None:
    result = simple_root_transfer_certificate(
        gap_slope_lower=3.0,
        perturbation_derivative_upper=1.0,
        perturbation_at_gap_root=-0.2,
        interval_radius=0.5,
    )

    assert result.derivative_margin == 2.0
    assert math.isclose(result.shift_bound, 0.1)
    assert result.is_contained


def test_reset_helpers_reject_ill_posed_data() -> None:
    invalid_calls = (
        lambda: maximal_physical_delay(0.0, (1.0,)),
        lambda: maximal_physical_delay(1.0, ()),
        lambda: maximal_physical_delay(1.0, (-1.0,)),
        lambda: reset_memory_margin(
            -1.0, delta=1.0, scaled_delays=(1.0,)
        ),
        lambda: recovery_endpoint_error(
            1.0,
            recovery_gap=0.0,
            initial_collective_error=0.0,
            initial_transverse_error=0.0,
        ),
        lambda: simple_root_transfer_certificate(
            gap_slope_lower=1.0,
            perturbation_derivative_upper=1.0,
            perturbation_at_gap_root=0.0,
            interval_radius=1.0,
        ),
    )
    for invalid_call in invalid_calls:
        try:
            invalid_call()
        except ValueError:
            pass
        else:
            raise AssertionError("ill-posed reset data were accepted")
