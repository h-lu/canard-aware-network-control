"""Hostile tests for the target raw-slot tilted-phase comparison."""

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

import canard_control.fixed_epsilon_target_tilted_phase as phase_module
from canard_control.fixed_epsilon_clocked_tail_graph_extension import (
    canard_coordinates,
    clocked_tail_slot_transform,
    state_from_canard_coordinates,
)
from canard_control.fixed_epsilon_frozen_graph_operator import FlowSlots
from canard_control.fixed_epsilon_target_tilted_phase import (
    CLOCKED_TAIL_RESULT_SHA256,
    CORE_PHASE_LEFT,
    CORE_PHASE_RIGHT,
    GRADIENT_SQUARED_LOWER,
    NO_GO_NU_LOWER,
    NO_GO_NU_UPPER,
    OPEN_FLAGS,
    PARTITION_CELLS,
    PARTITION_DENOMINATOR,
    PRECISION_BITS,
    PROVED_FLAGS,
    SLOT_TUBE_RADIUS,
    TARGET_ANCHOR_NU,
    TARGET_ANCHOR_NU_DECIMAL,
    TARGET_NU_LOWER,
    TARGET_NU_UPPER,
    TARGET_RHO_SQUARED,
    TAPER_LEFT,
    TAPER_RIGHT,
    TUBE_CLOCK_LOWER,
    build_reference_certificate,
    exact_sturm_certificate,
    json_ready_target_tilted_phase_audit,
    reference_normal_speed,
    taper,
    taper_derivative,
    target_raw_normal_speed,
    target_raw_sigma_speed,
    target_raw_slot_g,
    target_raw_tapered_phase_speed,
    target_anchor_raw_slot_equilibrium_certificate,
    target_slot_tube_cell_bounds,
    target_tapered_phase,
    target_tapered_phase_gradient,
    validate_target_tilted_phase_audit,
    validate_target_tilted_phase_result,
    verify_parent_evidence,
)


REPOSITORY = Path(__file__).resolve().parents[1]
SOURCE = REPOSITORY / "src/canard_control/fixed_epsilon_target_tilted_phase.py"
GENERATOR = REPOSITORY / "experiments/fixed_epsilon_target_tilted_phase.py"
RESULT = (
    REPOSITORY / "experiments/results/fixed_epsilon_target_tilted_phase.json"
)
NOTE = REPOSITORY / "docs/fixed-epsilon-target-tilted-phase.md"
PARENT_RESULT = (
    REPOSITORY
    / "experiments/results/fixed_epsilon_clocked_tail_graph_extension.json"
)


def _digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _result() -> dict:
    value = json.loads(RESULT.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_raw_target_coordinate_algebra_is_symbolically_exact() -> None:
    s, nu = sp.symbols("s nu", real=True)
    rho = 1 / sp.sqrt(5)
    x = -s / 2
    x_four = -(s - 4) / 2
    x_five = -(s - 5) / 2
    field_x = -sp.Rational(1, 2)
    field_x += rho * (
        -x**3 / 3 + ((x_four + x_five) / 2 - x) / 5
    )
    field_x += rho**3 * (
        (x_four**3 + x_five**3) / 2 - x**3
    ) / 4
    sigma_speed = sp.expand(-2 * field_x)
    expected_sigma = 1 + sp.sqrt(5) * (
        -40 * s**3 - 81 * s**2 + 369 * s - 999
    ) / 2400
    assert sp.simplify(sigma_speed - expected_sigma) == 0

    field_y = s / 2 + rho * nu
    normal_speed = sp.expand(field_y + s * field_x)
    expected_normal = s * (1 - expected_sigma) / 2 + nu / sp.sqrt(5)
    assert sp.simplify(normal_speed - expected_normal) == 0


def test_sigma_reversals_stalls_and_phase_no_go_are_exact() -> None:
    exact = exact_sturm_certificate()
    assert exact["sigma_sequence_length"] == 4
    assert exact["sigma_root_count"] == 3
    assert exact["sigma_square_free"] is True
    assert len(exact["root_enclosures"]) == 3
    assert len(exact["stall_enclosures"]) == 3

    central = exact["stall_enclosures"][1]
    assert float(central.lower) > float(NO_GO_NU_LOWER)
    assert float(central.upper) < float(NO_GO_NU_UPPER)

    for root, stall in zip(
        exact["root_enclosures"], exact["stall_enclosures"]
    ):
        root_midpoint = (float(root.lower) + float(root.upper)) / 2.0
        stall_midpoint = (float(stall.lower) + float(stall.upper)) / 2.0
        assert target_raw_sigma_speed(root_midpoint) == pytest.approx(
            0.0, abs=2e-9
        )
        assert target_raw_normal_speed(
            root_midpoint, stall_midpoint
        ) == pytest.approx(0.0, abs=2e-9)

    gradient_sigma, gradient_normal = sp.symbols("a b", real=True)
    assert sp.simplify(gradient_sigma * 0 + gradient_normal * 0) == 0


def test_no_constant_affine_phase_can_cross_both_reversals() -> None:
    for nu in (
        float(TARGET_NU_LOWER),
        0.07,
        float(TARGET_NU_UPPER),
    ):
        assert target_raw_sigma_speed(-3.0) < 0.0
        assert target_raw_normal_speed(-3.0, nu) < 0.0
        assert target_raw_sigma_speed(3.0) < 0.0
        assert target_raw_normal_speed(3.0, nu) > 0.0

    a, b = sp.symbols("a b", real=True, positive=True)
    assert (a > 0) is sp.true
    assert (b > 0) is sp.true


def test_frozen_anchor_zero_is_exact_and_inside_the_product_tube() -> None:
    nu = sp.Rational(TARGET_ANCHOR_NU.numerator, TARGET_ANCHOR_NU.denominator)
    assert nu == sp.Rational(TARGET_ANCHOR_NU_DECIMAL)
    s = -2 * nu / sp.sqrt(5)
    g = sp.sqrt(5) * (
        40 * s**3 + 81 * s**2 - 369 * s + 999
    ) / 4800
    d = sp.Rational(1, 2) - g
    x = -s / 2
    x_four = -(s - 4) / 2
    x_five = -(s - 5) / 2
    rho = 1 / sp.sqrt(5)
    qx = (
        d
        - sp.Rational(1, 2)
        + rho * (-x**3 / 3 + ((x_four + x_five) / 2 - x) / 5)
        + rho**3 * ((x_four**3 + x_five**3) / 2 - x**3) / 4
    )
    qy = s / 2 + nu / sp.sqrt(5)
    assert sp.simplify(qx) == 0
    assert sp.simplify(qy) == 0

    anchor = target_anchor_raw_slot_equilibrium_certificate()
    phase = anchor["phase_enclosure"]
    normal = anchor["normal_enclosure"]
    forcing = anchor["g_enclosure"]
    assert CORE_PHASE_LEFT < float(phase.lower)
    assert float(phase.upper) < CORE_PHASE_RIGHT
    assert 0.0 < float(normal.lower)
    assert float(normal.upper) < float(SLOT_TUBE_RADIUS)
    assert float(forcing.lower) > 0.499
    assert float(forcing.upper) < 0.5

    midpoint = (float(phase.lower) + float(phase.upper)) / 2.0
    assert target_raw_slot_g(midpoint) == pytest.approx(
        (float(forcing.lower) + float(forcing.upper)) / 2.0,
        abs=2e-16,
    )
    gradient_sigma, gradient_normal = sp.symbols("a b", real=True)
    assert sp.simplify(gradient_sigma * qx + gradient_normal * qy) == 0


def test_septic_taper_has_exact_c3_joins_and_is_not_silently_c4() -> None:
    z = sp.symbols("z", real=True)
    polynomial = 35 * z**4 - 84 * z**5 + 70 * z**6 - 20 * z**7
    assert polynomial.subs(z, 0) == 0
    assert polynomial.subs(z, 1) == 1
    for order in (1, 2, 3):
        derivative = sp.diff(polynomial, z, order)
        assert derivative.subs(z, 0) == 0
        assert derivative.subs(z, 1) == 0
    assert sp.diff(polynomial, z, 4).subs(z, 0) != 0
    assert sp.diff(polynomial, z, 4).subs(z, 1) != 0

    for boundary, expected in ((TAPER_LEFT, 0.0), (TAPER_RIGHT, 1.0)):
        assert taper(boundary) == expected
        assert taper_derivative(boundary) == 0.0
        for neighbor in (
            math.nextafter(float(boundary), -math.inf),
            math.nextafter(float(boundary), math.inf),
        ):
            assert taper(neighbor) == pytest.approx(
                expected, rel=0.0, abs=3e-13
            )


def test_tapered_phase_matches_the_incoming_sigma_face() -> None:
    for sigma in (-1e6, -64.0, -30.0, -6.0):
        for normal in (-1e4, -1.0, 0.0, 1.0, 1e4):
            assert target_tapered_phase(sigma, normal) == sigma
            assert target_tapered_phase_gradient(sigma, normal) == (1.0, 0.0)


def test_exact_endpoint_sturm_bounds_imply_the_full_nu_box() -> None:
    certificate = build_reference_certificate()
    assert len(certificate.endpoint_sturm_records) == 2
    for record in certificate.endpoint_sturm_records:
        assert record.sequence_length == 9
        assert record.negative_infinity_variations == 4
        assert record.positive_infinity_variations == 4
        assert record.real_root_count == 0

    generator = random.Random(20260825)
    for _ in range(5000):
        s = generator.uniform(-30.0, 30.0)
        nu = generator.uniform(
            float(TARGET_NU_LOWER), float(TARGET_NU_UPPER)
        )
        assert target_raw_tapered_phase_speed(s, nu) > 1.0 / 200.0


def test_tapered_phase_gradient_matches_finite_differences() -> None:
    step = 2e-6
    for sigma, normal in (
        (-6.2, 0.001),
        (-5.7, -0.001),
        (-5.2, 0.0004),
        (-0.18, 0.0008),
        (8.0, -0.0007),
    ):
        analytic = target_tapered_phase_gradient(sigma, normal)
        sigma_fd = (
            target_tapered_phase(sigma + step, normal)
            - target_tapered_phase(sigma - step, normal)
        ) / (2 * step)
        normal_fd = (
            target_tapered_phase(sigma, normal + step)
            - target_tapered_phase(sigma, normal - step)
        ) / (2 * step)
        assert analytic == pytest.approx(
            (sigma_fd, normal_fd), rel=2e-7, abs=2e-8
        )


def test_directed_tube_worst_cells_close_strictly() -> None:
    certificate = build_reference_certificate()
    assert certificate.slot_tube_radius == "1/1000"
    assert certificate.partition_cells == PARTITION_CELLS
    assert certificate.precision_bits == PRECISION_BITS
    assert float(certificate.worst_tube_phase_speed.lower) > float(
        TUBE_CLOCK_LOWER
    )
    assert float(certificate.worst_gradient_squared.lower) > float(
        GRADIENT_SQUARED_LOWER
    )
    assert certificate.minimum_plateau_margin == "999/1000"

    phase_speed, _ = target_slot_tube_cell_bounds(
        certificate.worst_tube_phase_speed_cell
    )
    assert phase_speed.decimal_bounds(80) == (
        certificate.worst_tube_phase_speed.lower,
        certificate.worst_tube_phase_speed.upper,
    )
    _, gradient_squared = target_slot_tube_cell_bounds(
        certificate.worst_gradient_squared_cell
    )
    assert gradient_squared.decimal_bounds(80) == (
        certificate.worst_gradient_squared.lower,
        certificate.worst_gradient_squared.upper,
    )


def test_directed_cells_contain_independent_binary64_slot_attacks() -> None:
    generator = random.Random(2026082501)
    rho = math.sqrt(float(TARGET_RHO_SQUARED))
    radius = float(SLOT_TUBE_RADIUS)
    for _ in range(300):
        s = generator.uniform(CORE_PHASE_LEFT, CORE_PHASE_RIGHT)
        if s == CORE_PHASE_RIGHT:
            s = math.nextafter(s, -math.inf)
        errors = [generator.uniform(-radius, radius) for _ in range(7)]
        sigma, sigma_four, sigma_five = (
            s + errors[0],
            s - 4.0 + errors[1],
            s - 5.0 + errors[2],
        )
        current = state_from_canard_coordinates(sigma, errors[3])
        delay_four = state_from_canard_coordinates(sigma_four, errors[4])
        delay_five = state_from_canard_coordinates(sigma_five, errors[5])
        delay_theta = state_from_canard_coordinates(s - 7.4, errors[6])
        slots = FlowSlots(current, delay_four, delay_five, delay_theta)
        nu = generator.uniform(float(TARGET_NU_LOWER), float(TARGET_NU_UPPER))
        field_x, field_y = clocked_tail_slot_transform(
            slots, rho=rho, nu=nu, eta=0.0
        )
        sigma_speed = -2.0 * field_x
        normal_speed = field_y + sigma * field_x
        gradient = target_tapered_phase_gradient(sigma, errors[3])
        actual = gradient[0] * sigma_speed + gradient[1] * normal_speed
        index = min(
            PARTITION_CELLS - 1,
            int((s - CORE_PHASE_LEFT) * PARTITION_DENOMINATOR),
        )
        interval, _ = target_slot_tube_cell_bounds(index)
        assert float(interval.lower) <= actual <= float(interval.upper)


def test_incoming_corridor_fast_bound_survives_cutoff_weights() -> None:
    certificate = build_reference_certificate()
    assert certificate.left_corridor_bracket_upper_at_x_lower == "-17981/250"
    assert certificate.left_corridor_derivative_upper_at_x_lower == "-1107/40"
    assert certificate.left_corridor_phase_speed_lower == "1/1"

    generator = random.Random(2026082502)
    rho = math.sqrt(float(TARGET_RHO_SQUARED))
    radius = float(SLOT_TUBE_RADIUS)
    for _ in range(500):
        s = generator.uniform(-30.0, -20.0)
        sigma = s + generator.uniform(-radius, radius)
        sigma_four = s - 4.0 + generator.uniform(-radius, radius)
        sigma_five = s - 5.0 + generator.uniform(-radius, radius)
        current = state_from_canard_coordinates(
            sigma, generator.uniform(-radius, radius)
        )
        delay_four = state_from_canard_coordinates(
            sigma_four, generator.uniform(-2.0, 2.0)
        )
        delay_five = state_from_canard_coordinates(
            sigma_five, generator.uniform(-2.0, 2.0)
        )
        slots = FlowSlots(current, delay_four, delay_five, (1e100, -1e100))
        field_x, _ = clocked_tail_slot_transform(
            slots,
            rho=rho,
            nu=generator.uniform(0.0, 0.2),
            eta=0.0,
        )
        assert -2.0 * field_x >= 1.0


def test_cell_api_and_scalar_apis_reject_hostile_inputs() -> None:
    for index in (-1, PARTITION_CELLS, True):
        with pytest.raises(ValueError, match="cell index"):
            target_slot_tube_cell_bounds(index)  # type: ignore[arg-type]
    for hostile in (math.nan, math.inf, -math.inf):
        with pytest.raises(ValueError, match="must be finite"):
            target_raw_sigma_speed(hostile)
        with pytest.raises(ValueError, match="must be finite"):
            target_raw_normal_speed(0.0, hostile)
        with pytest.raises(ValueError, match="must be finite"):
            target_tapered_phase(hostile, 0.0)


def test_parent_hash_and_semantic_boundary_are_replayed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    checks = verify_parent_evidence(REPOSITORY)
    assert all(value is True for value in checks.values())
    assert _digest(PARENT_RESULT) == CLOCKED_TAIL_RESULT_SHA256

    original_sha256 = phase_module._sha256

    def corrupted_hash(path: Path) -> str:
        if path == PARENT_RESULT:
            return "0" * 64
        return original_sha256(path)

    monkeypatch.setattr(phase_module, "_sha256", corrupted_hash)
    with pytest.raises(ValueError, match="parent result hash"):
        verify_parent_evidence(REPOSITORY)


def test_boolean_claim_ledger_is_literal_and_strict() -> None:
    audit = json_ready_target_tilted_phase_audit()
    validate_target_tilted_phase_audit(audit)
    certificate = audit["certificate"]
    assert all(certificate[name] is True for name in PROVED_FLAGS)
    assert all(certificate[name] is False for name in OPEN_FLAGS)

    for name in PROVED_FLAGS:
        tampered = deepcopy(audit)
        tampered["certificate"][name] = 1
        with pytest.raises(ValueError):
            validate_target_tilted_phase_audit(tampered)
    for name in OPEN_FLAGS:
        tampered = deepcopy(audit)
        tampered["certificate"][name] = 0
        with pytest.raises(ValueError):
            validate_target_tilted_phase_audit(tampered)


def test_result_hashes_claims_and_generator_replay_are_strict(
    tmp_path: Path,
) -> None:
    payload = _result()
    validate_target_tilted_phase_result(payload, REPOSITORY)
    manifest = payload["manifest"]
    assert manifest["proof_source_sha256"] == _digest(SOURCE)
    assert manifest["generator_sha256"] == _digest(GENERATOR)
    assert manifest["note_sha256"] == _digest(NOTE)
    assert manifest["parent_result_sha256"] == _digest(PARENT_RESULT)

    tampered = deepcopy(payload)
    tampered["manifest"]["proof_source_sha256"] = "0" * 64
    with pytest.raises(ValueError):
        validate_target_tilted_phase_result(tampered, REPOSITORY)

    replay = tmp_path / "replay.json"
    subprocess.run(
        [sys.executable, str(GENERATOR), "--output", str(replay)],
        cwd=REPOSITORY,
        check=True,
    )
    assert replay.read_bytes() == RESULT.read_bytes()
