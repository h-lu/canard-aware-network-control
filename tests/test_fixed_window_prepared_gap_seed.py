"""Hostile tests for the directed finite-window longitudinal-jet seed."""

from __future__ import annotations

from copy import deepcopy
from decimal import Decimal, localcontext
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys

import mpmath as mp
import pytest
import sympy as sp

from canard_control.directed_interval import DirectedInterval
from canard_control.fixed_window_prepared_gap_seed import (
    BLOCH_RESULT_SHA256,
    BUFFER,
    CORE_END,
    CUTOFF_END,
    GREEN_PHASE_DOC_SHA256,
    OUTER_RADIUS,
    PRECISION_BITS,
    QUADRATIC_PERIOD_LOCKED_ROOT_DOC_SHA256,
    RETAINED_SEGMENT_END,
    RISE_COEFFICIENTS,
    SLIDING_WINDOW_BRIDGE_RESULT_SHA256,
    build_reference_certificate,
    endpoint_jet,
    gaussian_moment_intervals,
    json_ready_fixed_window_gap_seed_payload,
    prepared_first_jet_on_canard,
    septic_cutoff,
    transition_coefficients_in_s,
    validate_fixed_window_gap_seed_payload,
)
from canard_control.green_phase import green_phase_audit


REPOSITORY = Path(__file__).resolve().parents[1]
SOURCE = REPOSITORY / "src/canard_control/fixed_window_prepared_gap_seed.py"
GENERATOR = REPOSITORY / "experiments/fixed_window_prepared_gap_seed.py"
RESULT = REPOSITORY / "experiments/results/fixed_window_prepared_gap_seed.json"
NOTE = REPOSITORY / "docs/fixed-window-prepared-gap-seed.md"
README = REPOSITORY / "README.md"
GREEN_PARENT = REPOSITORY / "docs/green-phase-selected-traces.md"
BLOCH_PARENT = REPOSITORY / "experiments/results/fhn_bloch_outer_validation.json"
BRIDGE_PARENT = (
    REPOSITORY
    / "experiments/results/fixed_epsilon_sliding_window_w1p_bridge.json"
)
QUADRATIC_ROOT_PARENT = REPOSITORY / "docs/quadratic-period-locked-selected-root.md"

EXPECTED_SOURCE_SHA256 = (
    "f05d7805132ce692f376393cc7c0c390c088ada50a61792584017e36e2217d91"
)
EXPECTED_GENERATOR_SHA256 = (
    "16f1ec01b74ef354a789941eb01028adc042218ef49cd0fc553105dc8b83c682"
)
EXPECTED_RESULT_SHA256 = (
    "41d325ca4c06b2e1b8a6ffa4e3908737c7be3d34a937a8a852ef7d1195321f39"
)
EXPECTED_NOTE_SHA256 = (
    "e4a9941fa22a70b56814fbccb5d2791df7752f0f098e098759afcc9b498ce0c4"
)


def _digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _result() -> dict:
    value = json.loads(RESULT.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def _interval(record: object, precision: int = PRECISION_BITS) -> DirectedInterval:
    assert isinstance(record, dict)
    return DirectedInterval.from_bounds(record["lower"], record["upper"], precision)


def test_septic_cutoff_has_exact_c3_but_not_c4_joins() -> None:
    assert endpoint_jet(RISE_COEFFICIENTS, Fraction(0), 4) == (
        Fraction(0),
        Fraction(0),
        Fraction(0),
        Fraction(0),
        Fraction(840),
    )
    assert endpoint_jet(RISE_COEFFICIENTS, Fraction(1), 4) == (
        Fraction(1),
        Fraction(0),
        Fraction(0),
        Fraction(0),
        Fraction(-840),
    )

    expected = tuple(
        Fraction(value)
        for value in (
            -30354399999,
            10372320000,
            -1518804000,
            123538800,
            -6028435,
            176484,
            -2870,
            20,
        )
    )
    assert transition_coefficients_in_s() == expected

    def exact_value(point: int) -> Fraction:
        total = Fraction(0)
        for coefficient in reversed(expected):
            total = total * point + coefficient
        return total

    assert exact_value(CORE_END) == 1
    assert exact_value(CUTOFF_END) == 0

    r = sp.symbols("r", real=True)
    rise = sum(
        sp.Rational(value.numerator, value.denominator) * r**index
        for index, value in enumerate(RISE_COEFFICIENTS)
    )
    assert sp.expand(
        sp.diff(rise, r) - 140 * r**3 * (1 - r) ** 3
    ) == 0


def test_cutoff_is_even_bounded_monotone_and_has_a_tail_neighborhood() -> None:
    nodes = [index / 16 for index in range(-400, 401)]
    values = [septic_cutoff(node) for node in nodes]
    assert all(0.0 <= value <= 1.0 for value in values)
    positive_values = [septic_cutoff(index / 16) for index in range(0, 400)]
    assert all(
        left >= right
        for left, right in zip(positive_values, positive_values[1:])
    )
    for point in (0.0, 4.9, 5.0, 9.0, 19.75, 20.75, 21.0, 22.0):
        assert septic_cutoff(point) == pytest.approx(septic_cutoff(-point))
    assert septic_cutoff(21.0) == 0.0
    assert septic_cutoff(21.5) == 0.0
    assert septic_cutoff(OUTER_RADIUS) == 0.0
    assert OUTER_RADIUS - CUTOFF_END == 1
    assert CORE_END == 20
    assert CUTOFF_END == 21


def test_declared_first_jet_is_core_exact_and_tail_zero() -> None:
    assert prepared_first_jet_on_canard(0.0, -0.2) == pytest.approx((0.45, -0.2))
    core_s = 4.0
    assert prepared_first_jet_on_canard(core_s, 0.3) == pytest.approx(
        (core_s**3 / 24 + 9 / 20, 0.3)
    )
    hull_s = 19.75
    assert prepared_first_jet_on_canard(hull_s, 0.3) == pytest.approx(
        (hull_s**3 / 24 + 9 / 20, 0.3)
    )
    assert 0 < septic_cutoff(20.5) < 1
    assert prepared_first_jet_on_canard(21.0, 0.3) == (0.0, 0.0)
    assert prepared_first_jet_on_canard(-22.0, 0.3) == (0.0, 0.0)


@pytest.mark.parametrize("lower,upper", [(0, 20), (20, 21)])
def test_directed_gaussian_moments_contain_independent_quadrature(
    lower: int, upper: int
) -> None:
    maximum_power = 11
    moments = gaussian_moment_intervals(lower, upper, maximum_power)
    mp.mp.dps = 200
    for power, moment in enumerate(moments):
        reference = mp.power(2, mp.mpf(power - 1) / 2) * mp.gammainc(
            mp.mpf(power + 1) / 2,
            mp.mpf(lower) ** 2 / 2,
            mp.mpf(upper) ** 2 / 2,
        )
        assert mp.mpf(str(moment.lower)) <= reference
        assert reference <= mp.mpf(str(moment.upper))
        assert moment.lower > 0


def test_higher_precision_moment_boxes_are_nested() -> None:
    moments_256 = gaussian_moment_intervals(20, 21, 11, precision=256)
    moments_512 = gaussian_moment_intervals(20, 21, 11, precision=512)
    for coarse, fine in zip(moments_256, moments_512):
        assert coarse.lower <= fine.lower <= fine.upper <= coarse.upper


def test_directed_seed_is_nondegenerate_and_not_the_whole_line_root() -> None:
    certificate = build_reference_certificate()
    assert Decimal(certificate.coefficient_a.lower) > 0
    assert Decimal(certificate.coefficient_b.lower) > 0
    assert Decimal(certificate.root_nu_chi.upper) < 0
    assert Decimal(certificate.root_nu_chi.lower) > Decimal("-0.125")
    assert Decimal(certificate.root_offset_above_minus_one_eighth.lower) > 0
    assert Decimal(certificate.coefficient_a_full_line_defect.lower) > 0
    assert Decimal(certificate.coefficient_b_full_line_defect.lower) > 0
    assert certificate.finite_window_root_distinct_from_minus_one_eighth_directed


def test_symbolic_green_parent_has_the_exact_normal_row() -> None:
    audit = green_phase_audit()
    s = audit.phase
    f_1, f_2 = audit.forcing
    expected = sp.exp(-(s**2) / 2) * (s * f_1 + f_2)
    assert sp.simplify(audit.normal_coefficient_derivative - expected) == 0
    assert audit.phase_value == -sp.Symbol("a", real=True)
    assert audit.h_boundary_residual == 0


def test_public_moments_reassemble_a_b_and_the_affine_root() -> None:
    result = _result()
    certificate = result["audit"]["certificate"]
    core = tuple(
        _interval(record)
        for record in certificate["core_gaussian_moments_zero_through_four"]
    )
    transition = tuple(
        _interval(record)
        for record in certificate[
            "transition_gaussian_moments_zero_through_eleven"
        ]
    )
    coefficients = transition_coefficients_in_s()
    zero = DirectedInterval.from_decimal(0, PRECISION_BITS)
    transition_a = zero
    transition_b = zero
    for index, coefficient in enumerate(coefficients):
        coefficient_interval = (
            DirectedInterval.from_decimal(coefficient.numerator, PRECISION_BITS)
            / coefficient.denominator
        )
        transition_a += coefficient_interval * transition[index]
        transition_b += coefficient_interval * transition[index + 4]
    reconstructed_a = 2 * (core[0] + transition_a)
    reconstructed_b = (core[4] + transition_b) / 12
    stored_a = _interval(certificate["coefficient_a"])
    stored_b = _interval(certificate["coefficient_b"])
    assert reconstructed_a.lower <= stored_a.lower
    assert stored_a.upper <= reconstructed_a.upper
    assert reconstructed_b.lower <= stored_b.lower
    assert stored_b.upper <= reconstructed_b.upper

    root = _interval(certificate["root_nu_chi"])
    residual = stored_a * root + stored_b
    assert residual.contains_zero()


def test_every_serialized_interval_width_bounds_its_decimal_endpoints() -> None:
    certificate = _result()["audit"]["certificate"]

    def visit(value: object) -> None:
        if isinstance(value, dict):
            if set(value) == {"lower", "upper", "width_upper"}:
                with localcontext() as context:
                    context.prec = 400
                    endpoint_width = Decimal(value["upper"]) - Decimal(
                        value["lower"]
                    )
                    assert endpoint_width >= 0
                    assert endpoint_width <= Decimal(value["width_upper"])
            else:
                for item in value.values():
                    visit(item)
        elif isinstance(value, list):
            for item in value:
                visit(item)

    visit(certificate)


def test_horizon_selects_period_and_buffer_has_strict_margin() -> None:
    certificate = build_reference_certificate()
    assert Decimal(certificate.fold_history_horizon.lower) > Decimal("5")
    assert certificate.fold_history_horizon_exceeds_largest_plant_delay
    assert Decimal(certificate.singular_depth_two_hull_radius.upper) < Decimal(
        "20"
    )
    assert Decimal(
        certificate.plateau_margin_over_singular_depth_two_hull.lower
    ) > Decimal("0.205")
    assert certificate.singular_depth_two_hull_covered
    assert RETAINED_SEGMENT_END == 5
    assert Decimal(
        certificate.buffer_margin_over_two_horizons_plus_two.lower
    ) > Decimal("1.205")
    assert certificate.buffer_condition_validated
    assert BUFFER == 18


def test_scope_ledger_refuses_full_preparation_root_or_control_promotion() -> None:
    certificate = build_reference_certificate()
    assert certificate.linear_green_gap_row_validated
    assert not certificate.linear_row_identified_with_target_d_rho_d
    assert not certificate.complete_graph_preparation_datum_constructed
    assert not certificate.frozen_target_graph_family_validated
    assert not certificate.first_jet_realised_by_same_graph_preparation
    assert not certificate.nonlinear_prepared_trace_family_validated
    assert not certificate.positive_amplitude_depth_two_hull_validated
    assert not certificate.positive_amplitude_root_continued
    assert not certificate.fixed_epsilon_complete_history_root_validated
    assert not certificate.general_network_fredholm_lift_validated
    assert not certificate.biological_pulse_control_chain_validated

    promoted = deepcopy(json_ready_fixed_window_gap_seed_payload())
    promoted["certificate"]["complete_graph_preparation_datum_constructed"] = True
    with pytest.raises(ValueError, match="differs from reference"):
        validate_fixed_window_gap_seed_payload(promoted)

    weakened = deepcopy(json_ready_fixed_window_gap_seed_payload())
    weakened["certificate"]["coefficient_a_excludes_zero_directed"] = False
    with pytest.raises(ValueError, match="differs from reference"):
        validate_fixed_window_gap_seed_payload(weakened)


def test_checked_artifact_and_parent_hashes_are_pinned() -> None:
    assert _digest(SOURCE) == EXPECTED_SOURCE_SHA256
    assert _digest(GENERATOR) == EXPECTED_GENERATOR_SHA256
    assert _digest(RESULT) == EXPECTED_RESULT_SHA256
    assert _digest(NOTE) == EXPECTED_NOTE_SHA256
    assert _digest(GREEN_PARENT) == GREEN_PHASE_DOC_SHA256
    assert _digest(BLOCH_PARENT) == BLOCH_RESULT_SHA256
    assert _digest(BRIDGE_PARENT) == SLIDING_WINDOW_BRIDGE_RESULT_SHA256
    assert _digest(QUADRATIC_ROOT_PARENT) == QUADRATIC_PERIOD_LOCKED_ROOT_DOC_SHA256

    result = _result()
    manifest = result["manifest"]
    assert manifest["proof_source_sha256"] == EXPECTED_SOURCE_SHA256
    assert manifest["generator_sha256"] == EXPECTED_GENERATOR_SHA256
    assert manifest["note_sha256"] == EXPECTED_NOTE_SHA256
    validate_fixed_window_gap_seed_payload(result["audit"])


def test_generator_reproduces_checked_payload(tmp_path: Path) -> None:
    output = tmp_path / "seed.json"
    subprocess.run(
        [sys.executable, str(GENERATOR), "--output", str(output)],
        cwd=REPOSITORY,
        check=True,
    )
    assert output.read_bytes() == RESULT.read_bytes()


def test_note_keeps_every_promotion_boundary_explicit() -> None:
    text = NOTE.read_text(encoding="utf-8")
    assert "longitudinal first-order forcing datum" in text
    assert "is **not** the complete admissible preparation" in text
    assert "finite reference section" in text
    assert "logarithmic moving radius" in text
    assert "must not be reused as the higher-regularity" in text
    assert "does not claim" in text
    assert "does not" in text
    assert "positive-\\(\\varrho\\) flow hull" in text
    assert "not yet been proved" in text
    assert "same RFDE graph preparation" in text
    assert "General-network Fredholm lift | open" in text
    assert "Biological pulse onset-to-output control chain | open" in text
    readme = README.read_text(encoding="utf-8")
    assert "docs/fixed-window-prepared-gap-seed.md" in readme
    assert "singular-hull-compatible longitudinal first-order forcing datum" in readme
