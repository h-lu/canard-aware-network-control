import math

import sympy as sp

from canard_control.clamped_reset_separator import (
    collective_clamp_audit,
    decision_time_bound,
    diffusive_scalar_characteristic_root,
    diffusive_scalar_leading_real_part,
    diffusive_scalar_residual,
    spectral_index_certificate,
)


def test_collective_clamp_removes_only_the_neutral_recovery_drift() -> None:
    result = collective_clamp_audit()

    assert result.controlled_collective_drift == 0
    assert sp.simplify(
        result.physical_recovery_actuator
        - sp.Matrix(
            [result.collective_control, 2 * result.collective_control]
        )
    ) == sp.zeros(2, 1)
    assert sp.simplify(
        result.critical_actuator_projection - result.collective_control
    ) == 0
    assert result.transverse_actuator_projection == 0
    assert result.transverse_recovery_residual == 0
    assert sp.simplify(
        result.uncontrolled_collective_drift
        + result.collective_control
    ) == 0
    assert sp.simplify(
        result.equilibrium_jacobian_determinant_at_zero_epsilon
        - result.expected_jacobian_determinant
    ) == 0


def test_resolvent_small_gain_certificate_is_delay_independent() -> None:
    result = spectral_index_certificate(
        epsilon=0.01,
        weak_gain=2.0,
        current_gain_norm=1.5,
        delayed_gain_norm_sum=1.5,
        imaginary_axis_resolvent_bound=4.0,
    )

    assert math.isclose(result.perturbation_bound, 0.06)
    assert math.isclose(result.loop_bound, 0.24)
    assert math.isclose(result.margin, 0.76)
    assert result.certifies_index_preservation


def test_fixed_clamp_time_resolves_only_a_declared_deadband() -> None:
    first = decision_time_bound(
        unstable_rate_lower=0.5,
        exit_coordinate=0.1,
        reset_slope_lower=0.25,
        parameter_deadband=1.0e-3,
    )
    second = decision_time_bound(
        unstable_rate_lower=0.5,
        exit_coordinate=0.1,
        reset_slope_lower=0.25,
        parameter_deadband=1.0e-6,
    )

    assert second > first
    assert math.isclose(
        second - first,
        math.log(1.0e3) / 0.5,
    )


def test_weak_long_diffusive_delay_has_stable_roots_approaching_axis() -> None:
    parameters = {
        "decay": 2.0,
        "weak_gain": 1.0,
        "layer_gain": 0.5,
        "scaled_delay": 1.0,
    }
    roots = [
        diffusive_scalar_characteristic_root(
            delta=delta,
            **parameters,
        )
        for delta in (0.2, 0.1, 0.05)
    ]

    for delta, root in zip((0.2, 0.1, 0.05), roots, strict=True):
        residual = diffusive_scalar_residual(
            root,
            delta=delta,
            **parameters,
        )
        assert abs(residual) < 1.0e-9
        assert root.real < 0.0
    assert roots[0].real < roots[1].real < roots[2].real < 0.0


def test_lambert_cut_branches_are_conjugate_and_have_claimed_asymptotic() -> None:
    parameters = {
        "decay": 2.0,
        "weak_gain": 1.0,
        "layer_gain": 0.5,
        "scaled_delay": 1.0,
    }
    ratios = []
    for delta in (0.05, 0.02, 0.01, 0.005):
        upper = diffusive_scalar_characteristic_root(
            delta=delta,
            branch=0,
            **parameters,
        )
        lower = diffusive_scalar_characteristic_root(
            delta=delta,
            branch=-1,
            **parameters,
        )
        leading = diffusive_scalar_leading_real_part(
            delta=delta,
            **parameters,
        )

        assert abs(upper - lower.conjugate()) < 1.0e-12
        assert abs(
            diffusive_scalar_residual(
                lower,
                delta=delta,
                **parameters,
            )
        ) < 1.0e-9
        assert leading < 0.0
        ratios.append(upper.real / leading)

    assert all(0.0 < ratio < 1.0 for ratio in ratios)
    assert ratios == sorted(ratios)
    assert abs(ratios[-1] - 1.0) < 3.0e-3


def test_clamp_helpers_reject_invalid_data() -> None:
    invalid_calls = (
        lambda: spectral_index_certificate(
            epsilon=-1.0,
            weak_gain=1.0,
            current_gain_norm=1.0,
            delayed_gain_norm_sum=1.0,
            imaginary_axis_resolvent_bound=1.0,
        ),
        lambda: decision_time_bound(
            unstable_rate_lower=0.0,
            exit_coordinate=1.0,
            reset_slope_lower=1.0,
            parameter_deadband=1.0,
        ),
        lambda: diffusive_scalar_characteristic_root(
            delta=0.0,
            decay=1.0,
            weak_gain=1.0,
            layer_gain=1.0,
            scaled_delay=1.0,
        ),
        lambda: diffusive_scalar_leading_real_part(
            delta=2.0,
            decay=1.0,
            weak_gain=1.0,
            layer_gain=1.0,
            scaled_delay=1.0,
        ),
    )
    for invalid_call in invalid_calls:
        try:
            invalid_call()
        except ValueError:
            pass
        else:
            raise AssertionError("invalid clamp data were accepted")
