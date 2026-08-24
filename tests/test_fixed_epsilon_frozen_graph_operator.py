"""Hostile tests for the fixed-epsilon frozen graph-operator contract."""

from __future__ import annotations

from copy import deepcopy
from fractions import Fraction
from hashlib import sha256
import json
import math
from pathlib import Path
import subprocess
import sys

import pytest
import sympy as sp

from canard_control.fixed_epsilon_frozen_graph_operator import (
    GRAPH_LONGITUDINAL_PLATEAU_RADIUS,
    GRAPH_LONGITUDINAL_SUPPORT_RADIUS,
    MODEL_ID,
    OPEN_FLAGS,
    PLANAR_NORMAL_CORE_RADIUS,
    PLANAR_NORMAL_EXTENSION_WIDTH,
    PROVED_FLAGS,
    SEELEY_NODES,
    SEELEY_WEIGHTS,
    THETA_LOWER,
    THETA_UPPER,
    FlowSlots,
    anisotropic_graph_cutoff,
    anisotropic_graph_cutoff_gradient,
    build_reference_certificate,
    canard_coordinates,
    cutoff_delayed_slot_gradients,
    cutoff_graph_transform,
    flat_cutoff_ratio,
    flat_cutoff_ratio_derivative,
    flow_variation_rhs,
    graph_fixed_point_residual,
    graph_residual_directional_derivative,
    graph_transform_from_candidate,
    jet_block_keys,
    json_ready_frozen_graph_operator_audit,
    prepared_planar_field,
    seeley_moment,
    seeley_normal_extension,
    singular_field,
    state_from_canard_coordinates,
    uncut_flow_slot_coefficients,
    uncut_physical_transform,
    validate_frozen_graph_operator_audit,
    validate_frozen_graph_operator_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]
SOURCE = (
    REPOSITORY
    / "src/canard_control/fixed_epsilon_frozen_graph_operator.py"
)
GENERATOR = (
    REPOSITORY / "experiments/fixed_epsilon_frozen_graph_operator.py"
)
RESULT = (
    REPOSITORY
    / "experiments/results/fixed_epsilon_frozen_graph_operator.json"
)
NOTE = REPOSITORY / "docs/fixed-epsilon-frozen-graph-operator.md"
README = REPOSITORY / "README.md"

# Filled after the deterministic artifact is generated.  These locks make a
# source/note change an explicit review event rather than a silent replay.
EXPECTED_SOURCE_SHA256 = (
    "ef9e4177b536e97d425a96fb4cbba3a0669cddc44ab0b8f544ccb440a2836651"
)
EXPECTED_GENERATOR_SHA256 = (
    "b84d5eb028dfc478bff021c0a8a8a8cf20af880d7f5ba4c8f19a37c5f4cd5b15"
)
EXPECTED_RESULT_SHA256 = (
    "2c16c96153c056dd7880adacf3d0f9247a3cecd9f8b5369ffd403b826b3b43be"
)
EXPECTED_NOTE_SHA256 = (
    "cce273873e560c607b0ef4d1191c4f20997b84fe475031b5acdfef4ce506ed83"
)


def _digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _result() -> dict:
    value = json.loads(RESULT.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_canard_coordinates_are_global_inverses_and_q0_is_exact() -> None:
    assert canard_coordinates((2.0, 7.0)) == (-4.0, 3.5)
    assert state_from_canard_coordinates(-4.0, 3.5) == (2.0, 7.0)
    for sigma, normal in ((0.0, 0.0), (3.25, -0.2), (-9.0, 1.1)):
        state = state_from_canard_coordinates(sigma, normal)
        assert canard_coordinates(state) == pytest.approx((sigma, normal))
    state = (sp.Rational(2, 3), sp.Rational(7, 5))
    q0 = singular_field((float(state[0]), float(state[1])))
    assert q0 == pytest.approx((float(state[1] - state[0] ** 2), -2 / 3))


def test_uncut_slot_algebra_matches_an_independent_symbolic_formula() -> None:
    x, y, p4, p5, ptheta, rho, nu, eta = sp.symbols(
        "x y p4 p5 ptheta rho nu eta", real=True
    )
    expected_x = (
        y
        - x**2
        + rho * (-x**3 / 3 + ((p4 + p5) / 2 - x) / 5)
        + rho**2 * eta * (x**2 - ptheta**2)
        + rho**3 * ((p4**3 + p5**3) / 2 - x**3) / 4
    )
    expected_y = -x + rho * nu
    assert sp.diff(expected_x, eta) == rho**2 * (x**2 - ptheta**2)
    assert sp.diff(expected_x, p4).subs(rho, 0) == 0
    assert sp.diff(expected_x, ptheta).subs(eta, 0) == 0
    assert sp.simplify(expected_x.subs(rho, 0) - (y - x**2)) == 0
    assert sp.simplify(expected_y.subs(rho, 0) + x) == 0

    values = {
        x: sp.Rational(2, 5),
        y: sp.Rational(-1, 7),
        p4: sp.Rational(3, 4),
        p5: sp.Rational(-2, 3),
        ptheta: sp.Rational(5, 6),
        rho: sp.Rational(1, 5),
        nu: sp.Rational(-1, 8),
        eta: sp.Rational(1, 100),
    }
    slots = FlowSlots(
        current=(float(values[x]), float(values[y])),
        delay_4=(float(values[p4]), 9.0),
        delay_5=(float(values[p5]), -8.0),
        delay_theta=(float(values[ptheta]), 7.0),
    )
    actual = uncut_physical_transform(
        slots,
        rho=float(values[rho]),
        nu=float(values[nu]),
        eta=float(values[eta]),
    )
    assert actual == pytest.approx(
        (float(expected_x.subs(values)), float(expected_y.subs(values)))
    )


def test_delay_four_and_five_are_symmetric_but_theta_has_only_eta_order() -> None:
    slots = FlowSlots((0.2, -0.1), (0.7, 2.0), (-0.4, 3.0), (0.9, 4.0))
    swapped = FlowSlots(
        slots.current, slots.delay_5, slots.delay_4, slots.delay_theta
    )
    for eta in (0.0, 0.03):
        assert uncut_physical_transform(
            slots, rho=0.3, nu=-0.1, eta=eta
        ) == pytest.approx(
            uncut_physical_transform(
                swapped, rho=0.3, nu=-0.1, eta=eta
            )
        )
    changed_theta = FlowSlots(
        slots.current, slots.delay_4, slots.delay_5, (-7.0, 100.0)
    )
    assert uncut_physical_transform(
        slots, rho=0.3, nu=-0.1, eta=0.0
    ) == pytest.approx(
        uncut_physical_transform(
            changed_theta, rho=0.3, nu=-0.1, eta=0.0
        )
    )


def test_singular_core_first_graph_jet_is_the_pinned_seed_carrier() -> None:
    symbol = sp.symbols("s", real=True)
    x = -symbol / 2
    x4 = -(symbol - 4) / 2
    x5 = -(symbol - 5) / 2
    exact_x_jet = -x**3 / 3 + ((x4 + x5) / 2 - x) / 5
    assert sp.expand(exact_x_jet - (symbol**3 / 24 + sp.Rational(9, 20))) == 0

    s = 3.25
    theta = (float(THETA_LOWER) + float(THETA_UPPER)) / 2
    slots = FlowSlots(
        state_from_canard_coordinates(s, 0.0),
        state_from_canard_coordinates(s - 4.0, 0.0),
        state_from_canard_coordinates(s - 5.0, 0.0),
        state_from_canard_coordinates(s - theta, 0.0),
    )
    step = 1e-5
    plus = cutoff_graph_transform(
        slots, rho=step, nu=-0.17, eta=0.03
    )
    minus = cutoff_graph_transform(
        slots, rho=-step, nu=-0.17, eta=0.03
    )
    derivative = tuple((right - left) / (2 * step) for right, left in zip(plus, minus))
    assert derivative == pytest.approx(
        (s**3 / 24.0 + 9.0 / 20.0, -0.17), rel=1e-9, abs=1e-10
    )
    certificate = build_reference_certificate()
    assert certificate.rho_zero_graph_frechet_derivative_is_zero
    assert certificate.singular_core_first_rho_graph_jet_validated
    assert certificate.singular_core_first_rho_graph_jet == "(s^3/24+9/20,nu)"
    assert "reference |s|<=20 core" in (
        certificate.singular_core_first_rho_graph_jet_domain
    )


def test_flat_graph_cutoff_is_monotone_flat_and_uses_canard_coordinates() -> None:
    assert flat_cutoff_ratio(0.0) == 1.0
    assert flat_cutoff_ratio(1.0) == 1.0
    assert flat_cutoff_ratio(2.0) == 0.0
    assert flat_cutoff_ratio(3.0) == 0.0
    values = [flat_cutoff_ratio(1.0 + index / 100) for index in range(101)]
    assert all(left >= right for left, right in zip(values, values[1:]))
    assert flat_cutoff_ratio_derivative(1.0) == 0.0
    assert flat_cutoff_ratio_derivative(2.0) == 0.0
    assert flat_cutoff_ratio_derivative(1.5) < 0.0

    for sigma, normal in ((0.0, 0.0), (536.9, 0.9), (-500.0, -0.5)):
        assert anisotropic_graph_cutoff(
            state_from_canard_coordinates(sigma, normal)
        ) == 1.0
    assert anisotropic_graph_cutoff(
        state_from_canard_coordinates(
            GRAPH_LONGITUDINAL_SUPPORT_RADIUS, 0.0
        )
    ) == 0.0
    assert anisotropic_graph_cutoff(
        state_from_canard_coordinates(0.0, 2.0)
    ) == 0.0
    assert anisotropic_graph_cutoff((1e200, 0.0)) == 0.0
    assert anisotropic_graph_cutoff_gradient((1e200, 0.0)) == (0.0, 0.0)


@pytest.mark.parametrize(
    "state",
    [
        state_from_canard_coordinates(800.0, 0.0),
        state_from_canard_coordinates(2.0, 1.4),
    ],
)
def test_graph_cutoff_gradient_matches_independent_central_differences(
    state: tuple[float, float],
) -> None:
    analytic = anisotropic_graph_cutoff_gradient(state)
    step = 1e-5
    numeric = []
    for coordinate in range(2):
        left = list(state)
        right = list(state)
        left[coordinate] -= step
        right[coordinate] += step
        numeric.append(
            (anisotropic_graph_cutoff(right) - anisotropic_graph_cutoff(left))
            / (2 * step)
        )
    assert analytic == pytest.approx(tuple(numeric), rel=3e-6, abs=3e-9)


def test_cutoff_transform_is_physical_on_plateau_and_zero_outside_current_support() -> None:
    slots = FlowSlots(
        state_from_canard_coordinates(1.0, 0.1),
        state_from_canard_coordinates(-4.0, -0.2),
        state_from_canard_coordinates(5.0, 0.3),
        state_from_canard_coordinates(-7.0, -0.4),
    )
    actual = cutoff_graph_transform(slots, rho=0.2, nu=-0.1, eta=0.03)
    expected = uncut_physical_transform(
        slots, rho=0.2, nu=-0.1, eta=0.03
    )
    assert actual == pytest.approx(expected)

    outside = FlowSlots(
        state_from_canard_coordinates(1100.0, 0.0),
        slots.delay_4,
        slots.delay_5,
        slots.delay_theta,
    )
    assert cutoff_graph_transform(
        outside, rho=0.2, nu=-0.1, eta=0.03
    ) == pytest.approx((0.0, -0.02))


def test_eta_zero_cutoff_operator_is_globally_theta_inactive() -> None:
    common = dict(
        current=state_from_canard_coordinates(700.0, 0.2),
        delay_4=state_from_canard_coordinates(600.0, 0.4),
        delay_5=state_from_canard_coordinates(900.0, 1.4),
    )
    left = FlowSlots(
        **common, delay_theta=state_from_canard_coordinates(0.0, 0.0)
    )
    right = FlowSlots(
        **common, delay_theta=state_from_canard_coordinates(2000.0, 4.0)
    )
    assert cutoff_graph_transform(
        left, rho=0.2, nu=0.1, eta=0.0
    ) == pytest.approx(
        cutoff_graph_transform(right, rho=0.2, nu=0.1, eta=0.0)
    )


def test_cutoff_operator_short_circuits_inactive_huge_binary64_slots() -> None:
    core = state_from_canard_coordinates(1.0, 0.1)
    huge = (1e200, -1e200)
    outside_current = FlowSlots(huge, huge, huge, huge)
    assert cutoff_graph_transform(
        outside_current, rho=0.2, nu=-0.1, eta=0.04
    ) == pytest.approx((0.0, -0.02))
    inactive_delay = FlowSlots(core, huge, core, huge)
    value = cutoff_graph_transform(
        inactive_delay, rho=0.2, nu=-0.1, eta=0.0
    )
    assert all(math.isfinite(component) for component in value)
    gradients = cutoff_delayed_slot_gradients(
        inactive_delay, rho=0.2, eta=0.0
    )
    assert all(math.isfinite(component) for pair in gradients for component in pair)


def test_cutoff_slot_gradients_reduce_to_exact_uncut_coefficients() -> None:
    slots = FlowSlots(
        state_from_canard_coordinates(1.0, 0.0),
        state_from_canard_coordinates(2.0, 0.1),
        state_from_canard_coordinates(3.0, -0.1),
        state_from_canard_coordinates(4.0, 0.2),
    )
    gradients = cutoff_delayed_slot_gradients(slots, rho=0.3, eta=0.02)
    coefficients = uncut_flow_slot_coefficients(slots, rho=0.3, eta=0.02)
    assert tuple(value for pair in gradients for value in pair) == pytest.approx(
        tuple(value for coefficient in coefficients for value in (coefficient, 0.0))
    )


@pytest.mark.parametrize("slot_name", ["delay_4", "delay_5", "delay_theta"])
def test_cutoff_slot_gradients_match_finite_differences(slot_name: str) -> None:
    index = {"delay_4": 0, "delay_5": 1, "delay_theta": 2}[slot_name]
    points = [
        state_from_canard_coordinates(2.0, 0.1),
        state_from_canard_coordinates(3.0, 0.1),
        state_from_canard_coordinates(4.0, 0.1),
    ]
    points[index] = state_from_canard_coordinates(2.0 + index, 1.3)
    slots = FlowSlots(
        state_from_canard_coordinates(1.0, 0.2),
        points[0],
        points[1],
        points[2],
    )
    analytic = cutoff_delayed_slot_gradients(slots, rho=0.21, eta=0.04)[index]
    base = getattr(slots, slot_name)
    numeric = []
    step = 1e-5
    for coordinate in range(2):
        values = []
        for direction in (-1.0, 1.0):
            point = list(base)
            point[coordinate] += direction * step
            arguments = {
                "current": slots.current,
                "delay_4": slots.delay_4,
                "delay_5": slots.delay_5,
                "delay_theta": slots.delay_theta,
            }
            arguments[slot_name] = tuple(point)
            values.append(
                cutoff_graph_transform(
                    FlowSlots(**arguments), rho=0.21, nu=-0.1, eta=0.04
                )[0]
            )
        numeric.append((values[1] - values[0]) / (2 * step))
    assert analytic == pytest.approx(tuple(numeric), rel=5e-6, abs=3e-9)


def test_backward_flow_slots_use_one_candidate_and_keep_theta_at_eta_zero() -> None:
    calls: list[tuple[float, tuple[float, float]]] = []

    def qx(point: tuple[float, float]) -> float:
        return point[1] - point[0] ** 2

    def backward_flow(field, state, delay):
        calls.append((delay, field(state)))
        return state[0] - delay, state[1] + delay

    theta = (float(THETA_LOWER) + float(THETA_UPPER)) / 2
    transformed, slots = graph_transform_from_candidate(
        qx,
        (0.1, -0.2),
        rho=0.0,
        nu=-0.1,
        eta=0.0,
        theta=theta,
        backward_flow=backward_flow,
    )
    assert [call[0] for call in calls] == pytest.approx([4.0, 5.0, theta])
    assert calls[0][1] == calls[1][1] == calls[2][1]
    assert slots.delay_4 == pytest.approx((-3.9, 3.8))
    assert transformed == pytest.approx(
        cutoff_graph_transform(slots, rho=0.0, nu=-0.1, eta=0.0)
    )
    with pytest.raises(ValueError, match="pinned directed interval"):
        graph_transform_from_candidate(
            qx,
            (0.1, -0.2),
            rho=0.0,
            nu=0.0,
            eta=0.0,
            theta=float(THETA_LOWER) - 0.01,
            backward_flow=backward_flow,
        )


def test_rho_zero_global_fixed_point_is_cutoff_q0_not_bare_q0() -> None:
    theta = (float(THETA_LOWER) + float(THETA_UPPER)) / 2

    def q0_cutoff_x(point):
        return anisotropic_graph_cutoff(point) * singular_field(point)[0]

    def irrelevant_flow(field, state, delay):
        return state

    for state in (
        state_from_canard_coordinates(0.0, 0.0),
        state_from_canard_coordinates(1100.0, 0.0),
    ):
        assert graph_fixed_point_residual(
            q0_cutoff_x,
            state,
            rho=0.0,
            nu=-0.1,
            eta=0.0,
            theta=theta,
            backward_flow=irrelevant_flow,
        ) == pytest.approx(0.0)


def test_flow_variation_and_residual_rows_have_the_correct_signs() -> None:
    derivative = ((2.0, -1.0), (0.5, 3.0))
    assert flow_variation_rhs(derivative, (4.0, -2.0), (1.0, 5.0)) == (
        -11.0,
        -1.0,
    )
    delayed_variations = ((1.0, 2.0), (-1.0, 3.0), (0.5, -2.0))
    gradients = ((2.0, 1.0), (4.0, -1.0), (3.0, 2.0))
    expected = 7.0 - sum(
        gx * zx + gy * zy
        for (zx, zy), (gx, gy) in zip(
            delayed_variations, gradients, strict=True
        )
    )
    assert graph_residual_directional_derivative(
        field_direction_at_current=7.0,
        delayed_variations=delayed_variations,
        delayed_slot_gradients=gradients,
    ) == pytest.approx(expected)


def test_seeley_weights_match_exactly_through_c3_and_samples_stay_in_core() -> None:
    assert SEELEY_NODES == (1, 2, 3, 4)
    assert SEELEY_WEIGHTS == (
        Fraction(10),
        Fraction(-20),
        Fraction(15),
        Fraction(-4),
    )
    assert tuple(seeley_moment(order) for order in range(4)) == (
        Fraction(1),
    ) * 4
    assert seeley_moment(4) == Fraction(-119)
    sampled: list[float] = []

    def difference(sigma, normal):
        assert -PLANAR_NORMAL_CORE_RADIUS <= normal <= PLANAR_NORMAL_CORE_RADIUS
        sampled.append(normal)
        return sigma + normal, sigma - normal

    assert seeley_normal_extension(difference, 2.0, 0.25) == pytest.approx(
        (2.25, 1.75)
    )
    value = seeley_normal_extension(difference, 2.0, 1.49)
    assert all(math.isfinite(component) for component in value)
    assert sampled
    assert seeley_normal_extension(difference, 2.0, 1.5) == (0.0, 0.0)
    assert seeley_normal_extension(difference, 2.0, -1.5) == (0.0, 0.0)
    with pytest.raises(ValueError, match="half the core"):
        seeley_normal_extension(
            difference,
            2.0,
            1.1,
            core_radius=1.0,
            extension_width=0.6,
        )


@pytest.mark.parametrize("degree", range(4))
@pytest.mark.parametrize("sign", [-1.0, 1.0])
def test_seeley_outer_strip_reproduces_both_c3_boundary_jets(
    degree: int, sign: float
) -> None:
    def polynomial_difference(sigma, normal):
        return normal**degree, (normal + sigma) ** degree

    outward = 0.1
    normal = sign * (PLANAR_NORMAL_CORE_RADIUS + outward)
    actual = seeley_normal_extension(
        polynomial_difference, 0.25, normal
    )
    weight = flat_cutoff_ratio(
        1.0 + outward / PLANAR_NORMAL_EXTENSION_WIDTH
    )
    expected = (
        weight * normal**degree,
        weight * (normal + 0.25) ** degree,
    )
    assert actual == pytest.approx(expected, rel=2e-12, abs=2e-12)


@pytest.mark.parametrize("sign", [-1.0, 1.0])
def test_seeley_outer_boundary_has_numerically_flat_zero_jet(sign: float) -> None:
    def constant_difference(sigma, normal):
        return 1.0, -2.0

    outer = PLANAR_NORMAL_CORE_RADIUS + PLANAR_NORMAL_EXTENSION_WIDTH
    step = 1e-3
    samples = [
        seeley_normal_extension(
            constant_difference, 0.0, sign * (outer - index * step)
        )
        for index in range(4)
    ]
    assert samples[0] == (0.0, 0.0)
    assert all(
        abs(component) < 1e-30 for sample in samples for component in sample
    )


def test_prepared_planar_field_equals_graph_on_core_and_q0_on_tails() -> None:
    def graph_field(state):
        sigma, normal = canard_coordinates(state)
        q0 = singular_field(state)
        return q0[0] + sigma + 2 * normal, q0[1] - sigma + normal

    core_state = state_from_canard_coordinates(3.0, 0.2)
    assert prepared_planar_field(graph_field, core_state) == pytest.approx(
        graph_field(core_state)
    )
    for state in (
        state_from_canard_coordinates(21.0, 0.2),
        state_from_canard_coordinates(-22.0, -0.2),
        state_from_canard_coordinates(3.0, 1.5),
    ):
        assert prepared_planar_field(graph_field, state) == pytest.approx(
            singular_field(state)
        )


@pytest.mark.parametrize("normal", [-1.2, 1.2])
def test_prepared_planar_field_uses_the_seeley_rule_in_normal_transition(
    normal: float,
) -> None:
    def constant_graph_perturbation(state):
        q0 = singular_field(state)
        return q0[0] + 1.0, q0[1] - 2.0

    state = state_from_canard_coordinates(3.0, normal)
    q0 = singular_field(state)
    transverse_weight = flat_cutoff_ratio(
        1.0
        + (abs(normal) - PLANAR_NORMAL_CORE_RADIUS)
        / PLANAR_NORMAL_EXTENSION_WIDTH
    )
    expected = q0[0] + transverse_weight, q0[1] - 2 * transverse_weight
    assert prepared_planar_field(
        constant_graph_perturbation, state
    ) == pytest.approx(expected)


def test_theorem_native_nesting_arithmetic_is_directed_and_not_seed_radius() -> None:
    certificate = build_reference_certificate()
    assert certificate.model_id == MODEL_ID
    assert certificate.theorem_jet_rectangle_cardinality == 96
    assert len(jet_block_keys()) == certificate.theorem_block_count == 28
    assert certificate.theorem_nesting_depth == 60
    assert float(certificate.theorem_outer_buffer_b_star.lower) > 514.22
    assert float(certificate.theorem_required_longitudinal_plateau.lower) > 536.22
    assert float(certificate.theorem_required_longitudinal_plateau.upper) < 537
    assert float(certificate.chosen_longitudinal_plateau_margin.lower) > 0.777
    assert certificate.chosen_longitudinal_plateau_contains_theorem_native_nesting
    assert GRAPH_LONGITUDINAL_PLATEAU_RADIUS == 537
    assert GRAPH_LONGITUDINAL_SUPPORT_RADIUS == 1074
    assert certificate.graph_cutoff_id != certificate.planar_cutoff_id
    assert certificate.graph_cutoff_regular_order == "C_infinity (in particular C_b^12)"
    assert certificate.graph_cutoff_frozen_in_rho_nu_eta
    assert certificate.graph_base_extension_formula == "q0,S=chi_graph*q0"
    assert certificate.graph_forcing_termwise_slot_sets == (
        "local_cubic:{0}",
        "linear_delay:{0,4,5}",
        "eta_quadratic:{0,Theta_*}",
        "cubic_delay:{0,4,5}",
        "slow_unfolding:{}",
    )
    assert len(certificate.theorem_kappa_schedule) == 61
    assert certificate.theorem_kappa_schedule[0] == "61/62"
    assert certificate.theorem_kappa_schedule[-1] == "1/62"
    assert certificate.planar_longitudinal_plateau_radius == 20
    assert certificate.planar_longitudinal_support_radius == 21


def test_claim_ledger_is_strictly_typed_and_refuses_every_promotion() -> None:
    audit = json_ready_frozen_graph_operator_audit()
    certificate = audit["certificate"]
    assert all(certificate[name] is True for name in PROVED_FLAGS)
    assert all(certificate[name] is False for name in OPEN_FLAGS)
    validate_frozen_graph_operator_audit(audit)

    for name in PROVED_FLAGS:
        weakened = deepcopy(audit)
        weakened["certificate"][name] = False
        with pytest.raises(ValueError, match="weakened"):
            validate_frozen_graph_operator_audit(weakened)
        integer_tamper = deepcopy(audit)
        integer_tamper["certificate"][name] = 1
        with pytest.raises(ValueError, match="weakened"):
            validate_frozen_graph_operator_audit(integer_tamper)
    for name in OPEN_FLAGS:
        promoted = deepcopy(audit)
        promoted["certificate"][name] = True
        with pytest.raises(ValueError, match="promoted"):
            validate_frozen_graph_operator_audit(promoted)
        integer_tamper = deepcopy(audit)
        integer_tamper["certificate"][name] = 0
        with pytest.raises(ValueError, match="promoted"):
            validate_frozen_graph_operator_audit(integer_tamper)


@pytest.mark.parametrize(
    "field,value",
    [
        ("model_id", "another-model"),
        ("backward_flow_convention", "P_tau=pi_X Phi_Q^{+tau}"),
        ("backward_flow_slots", ["4", "4", "Theta_*"]),
        ("eta_partial_source_at_fixed_graph", "rho*(X^2-P_Theta^2)"),
        ("graph_cutoff_id", "chi_plan_c3_septic_20_21"),
        ("graph_longitudinal_plateau_radius", "20"),
        ("seeley_fourth_moment", "1"),
    ],
)
def test_audit_validator_rejects_equation_cutoff_and_schema_tampering(
    field: str, value: object
) -> None:
    audit = json_ready_frozen_graph_operator_audit()
    audit["certificate"][field] = value
    with pytest.raises(ValueError):
        validate_frozen_graph_operator_audit(audit)


def test_generated_result_replays_and_whole_manifest_validator_is_hostile(
    tmp_path: Path,
) -> None:
    subprocess.run(
        [sys.executable, str(GENERATOR), "--output", str(tmp_path / "result.json")],
        cwd=REPOSITORY,
        check=True,
    )
    assert (tmp_path / "result.json").read_bytes() == RESULT.read_bytes()
    payload = _result()
    validate_frozen_graph_operator_result(payload, REPOSITORY)

    changed_hash = deepcopy(payload)
    changed_hash["manifest"]["generator_sha256"] = "0" * 64
    with pytest.raises(ValueError, match="self hash"):
        validate_frozen_graph_operator_result(changed_hash, REPOSITORY)

    changed_check_type = deepcopy(payload)
    first_check = next(iter(changed_check_type["manifest"]["parent_claim_checks"]))
    changed_check_type["manifest"]["parent_claim_checks"][first_check] = 1
    with pytest.raises(ValueError, match="strictly true"):
        validate_frozen_graph_operator_result(changed_check_type, REPOSITORY)

    missing_check = deepcopy(payload)
    missing_check["manifest"]["parent_claim_checks"].pop(first_check)
    with pytest.raises(ValueError, match="missing or unknown"):
        validate_frozen_graph_operator_result(missing_check, REPOSITORY)

    extra = deepcopy(payload)
    extra["manifest"]["unexpected"] = True
    with pytest.raises(ValueError, match="missing or unknown"):
        validate_frozen_graph_operator_result(extra, REPOSITORY)

    for field, value in (
        ("arithmetic", "false certification"),
        ("python", "0"),
        ("platform", "fabricated"),
    ):
        changed_runtime = deepcopy(payload)
        changed_runtime["manifest"][field] = value
        with pytest.raises(ValueError, match="runtime or arithmetic"):
            validate_frozen_graph_operator_result(changed_runtime, REPOSITORY)


def test_artifact_hashes_and_readme_claim_boundary_are_locked() -> None:
    assert _digest(SOURCE) == EXPECTED_SOURCE_SHA256
    assert _digest(GENERATOR) == EXPECTED_GENERATOR_SHA256
    assert _digest(RESULT) == EXPECTED_RESULT_SHA256
    assert _digest(NOTE) == EXPECTED_NOTE_SHA256
    text = README.read_text(encoding="utf-8")
    assert "docs/fixed-epsilon-frozen-graph-operator.md" in text
    assert "no graph fixed point, positive-amplitude hull" in text


def test_note_keeps_graph_preparation_and_root_boundaries_explicit() -> None:
    text = NOTE.read_text(encoding="utf-8")
    for phrase in (
        "does **not** compute the fixed point",
        "never enters the graph transform",
        "does not eliminate the scalar delayed history",
        "cannot be reused as a graph cutoff",
        "not yet an instantiated canonical preparation",
        "Physical onset and biological pulse-control chain",
    ):
        assert phrase in text
    assert "-\\frac{K_4(\\sigma)+K_5(\\sigma)}{10}" in text
