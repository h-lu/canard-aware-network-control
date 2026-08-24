"""Hostile tests for the bounded clock-positive graph extension."""

from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import json
import math
from pathlib import Path
import random
import subprocess
import sys

import pytest
import sympy as sp

import canard_control.fixed_epsilon_clocked_tail_graph_extension as extension
from canard_control.fixed_epsilon_clocked_tail_graph_extension import (
    DECLARED_PHASE_LEFT,
    DECLARED_PHASE_RIGHT,
    LEFT_EXTERIOR_END,
    LEFT_PLATEAU_START,
    MANIFEST_ARITHMETIC,
    OPEN_FLAGS,
    PRECISION_BITS,
    PROVED_FLAGS,
    REFUSED_FLAGS,
    RIGHT_EXTERIOR_START,
    RIGHT_PLATEAU_END,
    TAIL_CLOCK_RADIUS,
    TAIL_FAR_FIELD_START_RADIUS,
    THETA_LOWER,
    THETA_UPPER,
    bounded_clock_profile,
    bounded_clock_profile_derivative,
    bounded_clock_tail,
    build_reference_certificate,
    canard_coordinates,
    clocked_delayed_slot_gradients,
    clocked_tail_weak_delay_forcing,
    clocked_tail_slot_transform,
    clocked_tail_weight,
    clocked_tail_zero_amplitude_field,
    json_ready_clocked_tail_graph_audit,
    longitudinal_cutoff,
    longitudinal_cutoff_derivative,
    normal_cutoff,
    normal_cutoff_derivative,
    raw_target_sigma_speed_phase_three,
    singular_canard_slots,
    singular_core_first_rho_jet,
    state_from_canard_coordinates,
    validate_clocked_tail_graph_audit,
    validate_clocked_tail_graph_result,
    verify_clocked_tail_parent_evidence,
    zero_amplitude_coordinate_rhs,
)
from canard_control.fixed_epsilon_frozen_graph_operator import FlowSlots


REPOSITORY = Path(__file__).resolve().parents[1]
SOURCE = (
    REPOSITORY
    / "src/canard_control/fixed_epsilon_clocked_tail_graph_extension.py"
)
GENERATOR = (
    REPOSITORY / "experiments/fixed_epsilon_clocked_tail_graph_extension.py"
)
RESULT = (
    REPOSITORY
    / "experiments/results/fixed_epsilon_clocked_tail_graph_extension.json"
)
NOTE = REPOSITORY / "docs/fixed-epsilon-clocked-tail-graph-extension.md"


def _digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _result() -> dict:
    value = json.loads(RESULT.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_clocked_tail_and_base_coordinate_algebra_are_symbolically_exact() -> None:
    sigma, normal, speed, weight = sp.symbols(
        "sigma normal speed weight", real=True
    )
    x = -sigma / 2

    tail_x = -speed / 2
    tail_y = sigma * speed / 2
    assert sp.simplify(-2 * tail_x - speed) == 0
    assert sp.simplify(tail_y - 2 * x * tail_x) == 0

    base_x = tail_x + weight * normal
    base_y = tail_y
    assert sp.simplify(-2 * base_x - (speed - 2 * weight * normal)) == 0
    assert sp.simplify(
        base_y - 2 * x * base_x - sigma * weight * normal
    ) == 0

    for sigma_value, normal_value in (
        (-150.0, -0.4),
        (-30.0, 0.75),
        (0.0, 0.0),
        (21.0, -0.2),
        (160.0, 1.3),
    ):
        state = state_from_canard_coordinates(sigma_value, normal_value)
        tail = bounded_clock_tail(state)
        assert -2.0 * tail[0] == pytest.approx(
            bounded_clock_profile(sigma_value)
        )
        assert tail[1] - 2.0 * state[0] * tail[0] == pytest.approx(0.0)


def test_raw_constant_clock_germ_is_unbounded_and_not_a_cb_extension() -> None:
    x = sp.symbols("x", real=True)
    raw_clock_germ = (sp.Rational(-1, 2), -x)
    assert sp.limit(abs(raw_clock_germ[1]), x, sp.oo) == sp.oo
    for magnitude in (1.0, 1e6, 1e100, 1e300):
        assert abs(-magnitude) == magnitude
    note = NOTE.read_text(encoding="utf-8")
    assert "unbounded affine germ" in note
    assert "(-1/2,-X)" in note
    assert "not a \\(C_b\\) field" in note


def test_profile_interfaces_survive_nextafter_attacks() -> None:
    for boundary, expected in (
        (float(TAIL_CLOCK_RADIUS), 1.0),
        (float(TAIL_FAR_FIELD_START_RADIUS), 0.5),
    ):
        below = math.nextafter(boundary, -math.inf)
        above = math.nextafter(boundary, math.inf)
        values = tuple(bounded_clock_profile(value) for value in (below, boundary, above))
        assert values[1] == expected
        assert values[0] == pytest.approx(expected, rel=0.0, abs=4e-15)
        assert values[2] == pytest.approx(expected, rel=0.0, abs=4e-15)
        expected_derivative = (
            0.0
            if boundary == TAIL_CLOCK_RADIUS
            else -1.0 / (4.0 * TAIL_CLOCK_RADIUS)
        )
        assert bounded_clock_profile_derivative(boundary) == expected_derivative

        negative_values = tuple(
            bounded_clock_profile(-value) for value in (below, boundary, above)
        )
        assert negative_values == pytest.approx(values)
        assert bounded_clock_profile_derivative(-boundary) == -expected_derivative


def test_graph_cutoff_interfaces_and_nonfinite_inputs_are_hostile_safe() -> None:
    longitudinal_interfaces = (
        (float(LEFT_EXTERIOR_END), 0.0),
        (float(LEFT_PLATEAU_START), 1.0),
        (float(RIGHT_PLATEAU_END), 1.0),
        (float(RIGHT_EXTERIOR_START), 0.0),
    )
    for boundary, expected in longitudinal_interfaces:
        assert longitudinal_cutoff(boundary) == expected
        assert longitudinal_cutoff_derivative(boundary) == 0.0
        for neighbor in (
            math.nextafter(boundary, -math.inf),
            math.nextafter(boundary, math.inf),
        ):
            assert longitudinal_cutoff(neighbor) == pytest.approx(
                expected, rel=0.0, abs=4e-14
            )

    normal_interfaces = (
        (-2.0, 0.0),
        (-1.0, 1.0),
        (1.0, 1.0),
        (2.0, 0.0),
    )
    for boundary, expected in normal_interfaces:
        assert normal_cutoff(boundary) == expected
        assert normal_cutoff_derivative(boundary) == 0.0
        for neighbor in (
            math.nextafter(boundary, -math.inf),
            math.nextafter(boundary, math.inf),
        ):
            assert normal_cutoff(neighbor) == pytest.approx(
                expected, rel=0.0, abs=4e-14
            )

    for hostile in (math.nan, math.inf, -math.inf):
        for evaluator in (
            longitudinal_cutoff,
            longitudinal_cutoff_derivative,
            normal_cutoff,
            normal_cutoff_derivative,
        ):
            with pytest.raises(ValueError, match="must be finite"):
                evaluator(hostile)


def test_profile_tail_bounds_and_completeness_criterion_are_explicit() -> None:
    samples = (
        -1e300,
        -1000.0,
        -128.0,
        -100.0,
        -64.0,
        0.0,
        64.0,
        100.0,
        128.0,
        1000.0,
        1e300,
    )
    for sigma in samples:
        speed = bounded_clock_profile(sigma)
        assert 0.0 < speed <= 1.0
        state = (-sigma / 2.0, 0.0)
        qx, qy = bounded_clock_tail(state)
        assert abs(qx) <= 0.5
        assert abs(qy) <= TAIL_CLOCK_RADIUS
        if abs(sigma) >= TAIL_FAR_FIELD_START_RADIUS:
            assert speed == pytest.approx(TAIL_CLOCK_RADIUS / abs(sigma))

    start = float(TAIL_FAR_FIELD_START_RADIUS)
    travel_times = [
        (end * end - start * start) / (2.0 * TAIL_CLOCK_RADIUS)
        for end in (256.0, 1024.0, 1e6)
    ]
    assert travel_times[0] < travel_times[1] < travel_times[2]
    assert travel_times[2] > 1e9


def test_cutoff_plateau_recovers_the_exact_physical_slot_operator() -> None:
    current = state_from_canard_coordinates(3.0, 0.25)
    delay_4 = state_from_canard_coordinates(-1.0, -0.75)
    delay_5 = state_from_canard_coordinates(-2.0, 1.0)
    delay_theta = state_from_canard_coordinates(-4.0, 0.4)
    slots = FlowSlots(current, delay_4, delay_5, delay_theta)
    assert all(
        clocked_tail_weight(state) == 1.0
        for state in (current, delay_4, delay_5, delay_theta)
    )

    rho, nu, eta = 0.37, -0.8, 0.11
    x, y = current
    x4, _ = delay_4
    x5, _ = delay_5
    xtheta, _ = delay_theta
    expected_x = y - x * x
    expected_x += rho * (-(x**3) / 3.0 + ((x4 + x5) / 2.0 - x) / 5.0)
    expected_x += rho**2 * eta * (x * x - xtheta * xtheta)
    expected_x += rho**3 * ((x4**3 + x5**3) / 2.0 - x**3) / 4.0
    expected_y = -x + rho * nu
    assert clocked_tail_slot_transform(
        slots, rho=rho, nu=nu, eta=eta
    ) == pytest.approx((expected_x, expected_y))


def test_slot_transform_has_exact_weak_delay_factorization() -> None:
    generator = random.Random(20260824)
    slot_families = [
        FlowSlots(
            state_from_canard_coordinates(
                generator.uniform(-28.0, 20.0),
                generator.uniform(-0.9, 0.9),
            ),
            state_from_canard_coordinates(
                generator.uniform(-28.0, 20.0),
                generator.uniform(-0.9, 0.9),
            ),
            state_from_canard_coordinates(
                generator.uniform(-28.0, 20.0),
                generator.uniform(-0.9, 0.9),
            ),
            state_from_canard_coordinates(
                generator.uniform(-28.0, 20.0),
                generator.uniform(-0.9, 0.9),
            ),
        )
        for _ in range(20)
    ]
    slot_families.extend(
        (
            FlowSlots((1e308, -1e308), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0)),
            FlowSlots((0.0, -0.5), (1e308, 0.0), (-1e308, 0.0), (1e308, 0.0)),
        )
    )
    for slots in slot_families:
        base = clocked_tail_zero_amplitude_field(slots.current)
        for rho, nu, eta in (
            (0.0, 0.7, -0.2),
            (0.125, -0.8, 0.3),
            (-0.4, 1.1, -0.6),
            (1.0, 0.0, 0.0),
        ):
            forcing = clocked_tail_weak_delay_forcing(
                slots, rho=rho, nu=nu, eta=eta
            )
            actual = clocked_tail_slot_transform(
                slots, rho=rho, nu=nu, eta=eta
            )
            assert actual == (
                base[0] + rho * forcing[0],
                base[1] + rho * forcing[1],
            )
            assert all(math.isfinite(value) for value in forcing)


def test_weak_delay_forcing_short_circuits_inactive_huge_slots() -> None:
    huge = (1e308, -1e308)
    exterior_current = FlowSlots(huge, huge, huge, huge)
    assert clocked_tail_weak_delay_forcing(
        exterior_current, rho=-1e200, nu=1e200, eta=-1e200
    ) == (0.0, 0.0)

    plateau_current = state_from_canard_coordinates(0.0, 0.0)
    inactive_delays = FlowSlots(plateau_current, huge, huge, huge)
    forcing = clocked_tail_weak_delay_forcing(
        inactive_delays, rho=-1e100, nu=0.25, eta=1e100
    )
    assert forcing == (0.0, 0.25)


def test_delayed_slot_gradients_match_transition_region_finite_differences() -> None:
    slots = FlowSlots(
        state_from_canard_coordinates(2.0, 0.2),
        state_from_canard_coordinates(-29.5, 1.5),
        state_from_canard_coordinates(21.5, -1.3),
        state_from_canard_coordinates(0.5, 1.4),
    )
    rho, nu, eta = 0.31, -0.27, 0.17
    analytic = clocked_delayed_slot_gradients(slots, rho=rho, eta=eta)
    slot_names = ("delay_4", "delay_5", "delay_theta")
    step = 2e-6

    for slot_index, slot_name in enumerate(slot_names):
        for coordinate in (0, 1):
            perturbed_values = []
            for direction in (-1.0, 1.0):
                slot_value = list(getattr(slots, slot_name))
                slot_value[coordinate] += direction * step
                replacements = {
                    "current": slots.current,
                    "delay_4": slots.delay_4,
                    "delay_5": slots.delay_5,
                    "delay_theta": slots.delay_theta,
                }
                replacements[slot_name] = tuple(slot_value)
                perturbed = FlowSlots(**replacements)
                perturbed_values.append(
                    clocked_tail_slot_transform(
                        perturbed, rho=rho, nu=nu, eta=eta
                    )[0]
                )
            finite_difference = (
                perturbed_values[1] - perturbed_values[0]
            ) / (2.0 * step)
            assert analytic[slot_index][coordinate] == pytest.approx(
                finite_difference, rel=3e-5, abs=3e-7
            )


def test_incoming_trace_is_independent_of_parameters_normal_and_slots() -> None:
    hostile_slots = (
        (0.0, 0.0),
        (1e300, -1e300),
        (-1e300, 1e300),
    )
    for normal in (-1e6, -2.0, 0.0, 2.0, 1e6):
        current = state_from_canard_coordinates(LEFT_EXTERIOR_END, normal)
        assert clocked_tail_weight(current) == 0.0
        for delayed in hostile_slots:
            slots = FlowSlots(current, delayed, delayed, delayed)
            for rho, nu, eta in (
                (0.0, 0.0, 0.0),
                (0.3, 1e200, -1e200),
                (-2.0, -1e250, 1e250),
            ):
                assert clocked_tail_slot_transform(
                    slots, rho=rho, nu=nu, eta=eta
                ) == (-0.5, -15.0)


def test_every_declared_zero_amplitude_slot_is_in_the_unit_plateau() -> None:
    for phase in (DECLARED_PHASE_LEFT, 0.0, DECLARED_PHASE_RIGHT):
        for theta in (float(THETA_LOWER), float(THETA_UPPER)):
            slots = singular_canard_slots(phase, theta)
            for state in (
                slots.current,
                slots.delay_4,
                slots.delay_5,
                slots.delay_theta,
            ):
                sigma, normal = canard_coordinates(state)
                assert LEFT_PLATEAU_START <= sigma <= RIGHT_PLATEAU_END
                assert normal == pytest.approx(0.0, abs=2e-14)
                assert clocked_tail_weight(state) == 1.0


def test_declared_phase_apis_reject_even_one_ulp_outside_window() -> None:
    invalid = (
        math.nextafter(float(DECLARED_PHASE_LEFT), -math.inf),
        math.nextafter(float(DECLARED_PHASE_RIGHT), math.inf),
    )
    for phase in invalid:
        with pytest.raises(ValueError, match="declared interval"):
            singular_canard_slots(phase, float(THETA_LOWER))
        with pytest.raises(ValueError, match="declared interval"):
            singular_core_first_rho_jet(phase, 0.0)


def test_normal_plateau_does_not_imply_a_positive_phase_clock() -> None:
    state = state_from_canard_coordinates(0.0, 0.75)
    assert clocked_tail_weight(state) == 1.0
    assert zero_amplitude_coordinate_rhs(state) == pytest.approx((-0.5, 0.0))
    certificate = build_reference_certificate()
    assert "d_-<d<d_+<1/2" in certificate.causal_component_restriction


def test_inactive_huge_slots_and_exterior_current_do_not_overflow() -> None:
    huge = (1e308, -1e308)
    current = state_from_canard_coordinates(0.0, 0.0)
    slots = FlowSlots(current, huge, huge, huge)
    transformed = clocked_tail_slot_transform(
        slots, rho=1e100, nu=1e100, eta=1e100
    )
    assert all(math.isfinite(value) for value in transformed)
    gradients = clocked_delayed_slot_gradients(
        slots, rho=1e100, eta=1e100
    )
    assert gradients == ((0.0, 0.0),) * 3

    exterior = clocked_tail_zero_amplitude_field(huge)
    assert all(math.isfinite(value) for value in exterior)
    assert exterior == bounded_clock_tail(huge)


def test_singular_first_jet_and_raw_target_clock_warning_are_exact() -> None:
    phase, nu = sp.symbols("phase nu", real=True)
    x = -phase / 2
    x4 = -(phase - 4) / 2
    x5 = -(phase - 5) / 2
    first_x = sp.simplify(-x**3 / 3 + ((x4 + x5) / 2 - x) / 5)
    assert first_x == phase**3 / 24 + sp.Rational(9, 20)
    assert singular_core_first_rho_jet(3.0, -0.7) == pytest.approx(
        (3.0**3 / 24.0 + 9.0 / 20.0, -0.7)
    )

    raw_speed = raw_target_sigma_speed_phase_three()
    assert raw_speed == pytest.approx(1.0 - 567.0 / (160.0 * math.sqrt(5.0)))
    assert raw_speed < 0.0
    certificate = build_reference_certificate()
    assert float(certificate.raw_target_phase_three_sigma_speed.upper) < 0.0
    assert certificate.raw_singular_slot_target_clock_failure_proved is True
    assert certificate.target_uniform_clock_bound_validated is False


def test_small_rho_certificate_is_nonexplicit_local_and_not_a_target_solve() -> None:
    certificate = build_reference_certificate()
    required_proved = (
        "weak_delay_factorization_c_b_infinity_proved",
        "fixed_cutoff_small_rho_graph_exists",
        "fixed_cutoff_small_rho_graph_unique_in_contraction_neighborhood",
        "fixed_cutoff_small_rho_c3_rho_jets_proved",
        "fixed_cutoff_small_rho_first_graph_jet_proved",
        "seed_equation_21_graph_field_and_jet_realized",
    )
    assert all(getattr(certificate, name) is True for name in required_proved)
    assert "T_rho=B+rho*Fhat_rho" in certificate.weak_delay_factorization
    assert "non-explicit rho_0>0" in certificate.fixed_cutoff_small_rho_graph_contract
    assert "contraction neighborhood" in certificate.fixed_cutoff_small_rho_uniqueness_scope
    assert "not among every" in certificate.fixed_cutoff_small_rho_uniqueness_scope
    assert "partial_rho Q_rho|_0" in certificate.fixed_cutoff_small_rho_first_graph_jet
    assert "C3 Seeley extension" in certificate.seed_planar_preparation_rule
    assert all(getattr(certificate, name) is False for name in OPEN_FLAGS)
    assert (
        certificate.small_rho_global_uniqueness_outside_contraction_neighborhood_claimed
        is False
    )


def test_planar_preparation_first_seed_jet_is_only_an_algebraic_mock() -> None:
    rho, cutoff = sp.symbols("rho cutoff", real=True)
    q0_x, q0_y = sp.symbols("q0_x q0_y", real=True)
    base_x, base_y = sp.symbols("base_x base_y", real=True)
    seed_x, seed_y = sp.symbols("seed_x seed_y", real=True)
    remainder_x, remainder_y = sp.symbols("remainder_x remainder_y", real=True)
    graph = sp.Matrix(
        (
            base_x + rho * seed_x + rho**2 * remainder_x,
            base_y + rho * seed_y + rho**2 * remainder_y,
        )
    )
    base = sp.Matrix((base_x, base_y))
    q0 = sp.Matrix((q0_x, q0_y))
    prepared = q0 + cutoff * (graph - base)
    assert prepared.subs(rho, 0) == q0
    assert prepared.diff(rho).subs(rho, 0) == cutoff * sp.Matrix(
        (seed_x, seed_y)
    )


def test_q0_noncompleteness_warning_has_the_exact_first_integral() -> None:
    sigma, z = sp.symbols("sigma z", positive=True)
    sigma_dot = 1 + 2 * z
    z_dot = sigma * z
    log_invariant = sp.log(z) + 2 * z - sigma**2 / 2
    derivative = (
        sp.diff(log_invariant, sigma) * sigma_dot
        + sp.diff(log_invariant, z) * z_dot
    )
    assert sp.simplify(derivative) == 0
    certificate = build_reference_certificate()
    assert certificate.seed_prepared_trace_field_global_completeness_claimed is False
    note = NOTE.read_text(encoding="utf-8")
    assert "reaches infinity in finite positive time" in note


def test_boolean_claim_ledger_rejects_truthy_and_falsy_non_booleans() -> None:
    audit = json_ready_clocked_tail_graph_audit()
    validate_clocked_tail_graph_audit(audit)
    certificate = audit["certificate"]
    assert all(certificate[name] is True for name in PROVED_FLAGS)
    assert all(certificate[name] is False for name in OPEN_FLAGS)
    assert all(certificate[name] is False for name in REFUSED_FLAGS)

    for name in PROVED_FLAGS:
        tampered = deepcopy(audit)
        tampered["certificate"][name] = 1
        with pytest.raises(ValueError):
            validate_clocked_tail_graph_audit(tampered)
    for name in OPEN_FLAGS + REFUSED_FLAGS:
        tampered = deepcopy(audit)
        tampered["certificate"][name] = 0
        with pytest.raises(ValueError):
            validate_clocked_tail_graph_audit(tampered)

    for key, value in (
        ("precision_bits", True),
        ("declared_phase_interval", [-21.0, 21.0]),
        ("delay_set", [4.0, 5, "Theta_*"]),
        ("bounded_clock_profile_formula", "constant speed"),
    ):
        tampered = deepcopy(audit)
        tampered["certificate"][key] = value
        with pytest.raises(ValueError):
            validate_clocked_tail_graph_audit(tampered)


def test_parent_hashes_and_semantic_checks_are_replayed_strictly(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    hashes, checks = verify_clocked_tail_parent_evidence(REPOSITORY)
    assert hashes == extension.PARENT_SHA256
    assert set(checks) == extension.PARENT_CLAIM_CHECK_KEYS
    assert all(value is True for value in checks.values())

    original_sha256 = extension._sha256

    def corrupted_hash(path: Path) -> str:
        if path.name == "special-flow-graph-theorem.md":
            return "0" * 64
        return original_sha256(path)

    monkeypatch.setattr(extension, "_sha256", corrupted_hash)
    with pytest.raises(ValueError, match="pinned parent hashes"):
        verify_clocked_tail_parent_evidence(REPOSITORY)


def test_mixed_jet_parent_hash_and_theorem_semantics_are_pinned(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    original_sha256 = extension._sha256

    def corrupted_hash(path: Path) -> str:
        if path.name == "mixed-jet-graph-proof.md":
            return "f" * 64
        return original_sha256(path)

    monkeypatch.setattr(extension, "_sha256", corrupted_hash)
    with pytest.raises(ValueError, match="pinned parent hashes"):
        verify_clocked_tail_parent_evidence(REPOSITORY)

    monkeypatch.setattr(extension, "_sha256", original_sha256)
    original_read_text = Path.read_text

    def weakened_read_text(path: Path, *args: object, **kwargs: object) -> str:
        text = original_read_text(path, *args, **kwargs)
        if path.name == "mixed-jet-graph-proof.md":
            return text.replace(
                "Theorem 1 (finite-scale mixed-jet graph)",
                "Unproved finite-scale mixed-jet conjecture",
            )
        return text

    monkeypatch.setattr(Path, "read_text", weakened_read_text)
    with pytest.raises(ValueError, match="parent claim checks"):
        verify_clocked_tail_parent_evidence(REPOSITORY)


def test_seeley_parent_semantic_rule_is_independently_replayed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    original_reader = extension._read_json_object

    def weakened_reader(path: Path) -> dict:
        payload = original_reader(path)
        if path.name == "fixed_epsilon_frozen_graph_operator.json":
            payload = deepcopy(payload)
            payload["audit"]["certificate"][
                "seeley_c3_matching_identities_validated"
            ] = False
        return payload

    monkeypatch.setattr(extension, "_read_json_object", weakened_reader)
    monkeypatch.setattr(
        extension,
        "validate_frozen_graph_operator_result",
        lambda payload, repository: None,
    )
    with pytest.raises(ValueError, match="parent claim checks"):
        verify_clocked_tail_parent_evidence(REPOSITORY)


def test_parent_theta_semantics_are_not_replaced_by_close_decimals(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(extension, "THETA_LOWER", "7.39708")
    with pytest.raises(ValueError, match="parent claim checks"):
        verify_clocked_tail_parent_evidence(REPOSITORY)


def test_seed_parent_recursive_self_hashes_are_replayed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    original_sha256 = extension._sha256

    def corrupted_seed_note_hash(path: Path) -> str:
        if path.name == "fixed-window-prepared-gap-seed.md":
            return "a" * 64
        return original_sha256(path)

    monkeypatch.setattr(extension, "_sha256", corrupted_seed_note_hash)
    with pytest.raises(ValueError, match="seed parent self hashes"):
        verify_clocked_tail_parent_evidence(REPOSITORY)


def test_seed_upstream_hashes_and_claim_checks_are_replayed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    original_sha256 = extension._sha256

    def corrupted_upstream_hash(path: Path) -> str:
        if path.name == "green-phase-selected-traces.md":
            return "b" * 64
        return original_sha256(path)

    monkeypatch.setattr(extension, "_sha256", corrupted_upstream_hash)
    with pytest.raises(ValueError, match="seed parent recursive hashes"):
        verify_clocked_tail_parent_evidence(REPOSITORY)


def test_seed_upstream_semantics_are_replayed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    original_read_text = Path.read_text

    def weakened_read_text(path: Path, *args: object, **kwargs: object) -> str:
        text = original_read_text(path, *args, **kwargs)
        if path.name == "green-phase-selected-traces.md":
            return text.replace(
                "two different frozen cutoffs",
                "one interchangeable cutoff",
            )
        return text

    monkeypatch.setattr(Path, "read_text", weakened_read_text)
    with pytest.raises(ValueError, match="recursive claim checks"):
        verify_clocked_tail_parent_evidence(REPOSITORY)


def test_result_self_hashes_manifest_and_claims_are_strict() -> None:
    payload = _result()
    validate_clocked_tail_graph_result(payload, REPOSITORY)
    manifest = payload["manifest"]
    assert manifest["proof_source_sha256"] == _digest(SOURCE)
    assert manifest["generator_sha256"] == _digest(GENERATOR)
    assert manifest["note_sha256"] == _digest(NOTE)
    assert manifest["arithmetic"] == MANIFEST_ARITHMETIC
    assert "no computed target-amplitude candidate" in manifest["arithmetic"]
    assert "root validation" in manifest["arithmetic"]
    assert all(value is True for value in manifest["parent_claim_checks"].values())

    for key, value in (
        ("proof_source_sha256", "0" * 64),
        ("generator", "experiments/wrong.py"),
        ("arithmetic", "binary64 evidence"),
        ("python", "0.0"),
    ):
        tampered = deepcopy(payload)
        tampered["manifest"][key] = value
        with pytest.raises(ValueError):
            validate_clocked_tail_graph_result(tampered, REPOSITORY)

    tampered = deepcopy(payload)
    first_check = next(iter(tampered["manifest"]["parent_claim_checks"]))
    tampered["manifest"]["parent_claim_checks"][first_check] = 1
    with pytest.raises(ValueError):
        validate_clocked_tail_graph_result(tampered, REPOSITORY)


def test_generator_replays_result_byte_identically(tmp_path: Path) -> None:
    replay = tmp_path / "replay.json"
    subprocess.run(
        [sys.executable, str(GENERATOR), "--output", str(replay)],
        cwd=REPOSITORY,
        check=True,
    )
    assert replay.read_bytes() == RESULT.read_bytes()
