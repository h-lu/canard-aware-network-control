from fractions import Fraction
from math import isinf

import pytest

from canard_control.strong_unstable_history import (
    exact_safe_layer_history_norm,
    phase_lift_bound,
    physical_tracker_perturbation_bound,
    singular_middle_current_index,
    strong_unstable_roughness_budget,
)


def test_exact_delay_functional_norm() -> None:
    assert exact_safe_layer_history_norm() == Fraction(8, 3)


def test_phase_lift_constant_is_delay_length_independent() -> None:
    short = phase_lift_bound(
        delay_length=1.0,
        current_evolution_bound=2.5,
        projector_bound=1.75,
    )
    long = phase_lift_bound(
        delay_length=1.0e8,
        current_evolution_bound=2.5,
        projector_bound=1.75,
    )
    assert short.history_evolution_bound == 2.5
    assert long.history_evolution_bound == short.history_evolution_bound


def test_weighted_green_budget_has_sharp_midpoint_formula() -> None:
    budget = strong_unstable_roughness_budget(
        evolution_bound=2.0,
        center_stable_rate=0.0,
        unstable_rate=1.0,
        perturbation_norm=0.05,
    )
    assert budget.weight == 0.5
    assert budget.contraction_constant == pytest.approx(0.4)
    assert budget.resolvent_bound == pytest.approx(5.0 / 3.0)
    assert budget.closes

    failed = strong_unstable_roughness_budget(
        evolution_bound=2.0,
        center_stable_rate=0.0,
        unstable_rate=1.0,
        perturbation_norm=0.2,
    )
    assert failed.contraction_constant == pytest.approx(1.6)
    assert isinf(failed.resolvent_bound)
    assert not failed.closes


def test_physical_perturbation_tends_to_zero_without_delay_penalty() -> None:
    coarse = physical_tracker_perturbation_bound(
        delta=0.1,
        weak_gain=1.0,
        frame_and_tracker_constant=2.0,
        coordinate_condition=3.0,
    )
    fine = physical_tracker_perturbation_bound(
        delta=0.01,
        weak_gain=1.0,
        frame_and_tracker_constant=2.0,
        coordinate_condition=3.0,
    )
    assert fine < coarse / 8.0


def test_singular_middle_current_index() -> None:
    audit = singular_middle_current_index(
        collective_recovery=-0.5,
        recovery_damping=1.5,
    )
    assert audit.unstable_count == 1
    assert audit.center_count == 1
    assert audit.stable_count == 2
    assert audit.unstable_floor > 0.0


@pytest.mark.parametrize(
    ("function", "kwargs"),
    [
        (
            phase_lift_bound,
            {
                "delay_length": 0.0,
                "current_evolution_bound": 1.0,
                "projector_bound": 1.0,
            },
        ),
        (
            strong_unstable_roughness_budget,
            {
                "evolution_bound": 1.0,
                "center_stable_rate": 1.0,
                "unstable_rate": 1.0,
                "perturbation_norm": 0.0,
            },
        ),
        (
            physical_tracker_perturbation_bound,
            {
                "delta": 0.0,
                "weak_gain": 1.0,
                "frame_and_tracker_constant": 1.0,
            },
        ),
        (
            singular_middle_current_index,
            {
                "collective_recovery": 2.0,
                "recovery_damping": 1.0,
            },
        ),
    ],
)
def test_invalid_inputs(function, kwargs) -> None:
    with pytest.raises(ValueError):
        function(**kwargs)
