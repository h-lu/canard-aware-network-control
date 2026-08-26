from __future__ import annotations

from copy import deepcopy
from decimal import Decimal
from fractions import Fraction
import hashlib
import json
from pathlib import Path

import gmpy2
import pytest
import numpy as np

from canard_control.directed_interval import (
    DirectedInterval,
    complex_unit_interval,
    decimal_upper,
    pi_interval,
)
from canard_control.fhn_periodic_infinite_validation import (
    _sequence_box_norm_upper,
)
from canard_control.leaky_floquet_outer_right_half_cover import (
    ALWAYS_FALSE,
    CHECKPOINT_SCHEMA_ID,
    COEFFICIENT_SUPPORT_RADIUS,
    ACCEPTANCE_THRESHOLD,
    CoverLeaf,
    EXPECTED_SHARED_ARITHMETIC_SHA256,
    FOURIER_CUTOFF,
    MAXIMUM_DEPTH,
    NEUTRAL_CORE_SIZE,
    PRECISION_BITS,
    RESULT_RELATIVE_PATH,
    TRUE_ON_COMPLETE,
    _Rectangle,
    _candidate_matrices,
    _cover_checkpoint,
    _leaf_digest,
    _normalized_area_fraction,
    _coefficient_matrix,
    _input_rotated_convolution,
    _output_rotated_convolution,
    _orbit_corrections,
    _prepare_outer_candidate,
    _rectangle_is_neutral_core_root,
    _rectilinear_root_partition_validated,
    _restore_cover_checkpoint,
    _root_rectangles,
    _split_rectangle,
    canonical_sha256,
    validate_outer_right_half_result,
)
from canard_control.leaky_floquet_transfer import (
    load_validated_leaky_orbit_evidence,
)
from canard_control.leaky_periodic_validation import (
    _build_leaky_base_sequences,
)


REPOSITORY = Path(__file__).resolve().parents[1]
RESULT = REPOSITORY / RESULT_RELATIVE_PATH
EXPECTED_RESULT_SHA256 = "TO_REGISTER"


@pytest.fixture(scope="module")
def payload() -> dict:
    return json.loads(RESULT.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def outer_source():
    orbit, _ = load_validated_leaky_orbit_evidence(
        REPOSITORY, "outer_pulse"
    )
    return orbit, _build_leaky_base_sequences(orbit, PRECISION_BITS)


@pytest.fixture(scope="module")
def outer_base(outer_source):
    return outer_source[1]


def _refresh_certificate(payload: dict) -> None:
    payload["manifest"]["certificate_sha256"] = canonical_sha256(
        payload["certificate"]
    )


def _refresh_leaf_records(certificate: dict) -> None:
    from canard_control.leaky_floquet_outer_right_half_cover import CoverLeaf

    leaves = [CoverLeaf(**leaf) for leaf in certificate["leaves"]]
    certificate["leaf_partition_sha256"] = _leaf_digest(leaves)
    certificate["accepted_normalized_area_fraction"] = (
        _normalized_area_fraction(leaves)
    )


def _checkpoint_oracle() -> tuple[dict, dict]:
    phase_upper = Decimal(decimal_upper(pi_interval(PRECISION_BITS).upper))
    roots = _root_rectangles(phase_upper)
    first, second = _split_rectangle(roots[1])
    riesz = json.loads(
        (REPOSITORY / "experiments/results/leaky_floquet_riesz_reduction.json")
        .read_text(encoding="utf-8")
    )["artifact"]["branches"]["outer_pulse"]
    arguments = {
        "roots": roots,
        "candidate_fingerprint": "checkpoint-structure-oracle",
        "precision": PRECISION_BITS,
        "threshold": ACCEPTANCE_THRESHOLD,
        "maximum_depth": MAXIMUM_DEPTH,
        "phase_upper": phase_upper,
        "local_radius": Decimal(riesz["local_complex_exclusion_radius_lower"]),
        "keyhole_radius": Decimal(riesz["local_keyhole_radius"]),
    }
    payload = _cover_checkpoint(
        REPOSITORY,
        **arguments,
        pending=(roots[2], second, first),
        leaves=(
            CoverLeaf(
                "neutral_core", "", "riesz_local_disk", "0", "0", "0"
            ),
        ),
        local_leaf_count=1,
        neumann_leaf_count=0,
        processed=2,
        deepest=0,
        worst=None,
    )
    return payload, arguments


def test_source_bound_checkpoint_round_trip_is_lossless() -> None:
    checkpoint, arguments = _checkpoint_oracle()
    assert checkpoint["checkpoint"]["schema_id"] == CHECKPOINT_SCHEMA_ID
    restored = _restore_cover_checkpoint(
        checkpoint, REPOSITORY, **arguments
    )
    assert restored.processed == 2
    assert restored.deepest == 0
    assert [rectangle.root_id for rectangle in restored.pending] == [
        "upper_left_strip",
        "right_strip",
        "right_strip",
    ]
    assert [rectangle.path for rectangle in restored.pending[-2:]] == [
        "x1",
        "x0",
    ]
    rebuilt = _cover_checkpoint(
        REPOSITORY,
        **arguments,
        pending=restored.pending,
        leaves=restored.leaves,
        local_leaf_count=restored.local_leaf_count,
        neumann_leaf_count=restored.neumann_leaf_count,
        processed=restored.processed,
        deepest=restored.deepest,
        worst=restored.worst,
    )
    assert rebuilt == checkpoint


@pytest.mark.parametrize(
    "mutation",
    (
        "digest",
        "wrong_source",
        "geometry",
        "stack_order",
        "precision",
        "threshold",
        "noncore_local",
    ),
)
def test_hostile_checkpoint_mutations_are_rejected(mutation: str) -> None:
    checkpoint, arguments = _checkpoint_oracle()
    changed = deepcopy(checkpoint)
    body = changed["checkpoint"]
    if mutation == "digest":
        changed["checkpoint_sha256"] = "0" * 64
    elif mutation == "wrong_source":
        body["source_sha256"][
            "src/canard_control/leaky_floquet_outer_right_half_cover.py"
        ] = "0" * 64
    elif mutation == "geometry":
        body["pending"][0]["sigma_upper"] = "255"
    elif mutation == "stack_order":
        body["pending"].reverse()
    elif mutation == "precision":
        body["precision_bits"] = PRECISION_BITS - 1
    elif mutation == "threshold":
        body["acceptance_threshold"] = "0.999"
    elif mutation == "noncore_local":
        body["pending"].pop()
        body["leaves"].append(
            {
                "root_id": "right_strip",
                "path": "x0",
                "proof_kind": "riesz_local_disk",
                "contraction_upper": "0",
                "finite_input_column_sum_upper": "0",
                "tail_input_column_sum_upper": "0",
            }
        )
        body["processed_cell_count"] += 1
        body["local_disk_leaf_count"] += 1
        body["accepted_leaf_partition_sha256"] = _leaf_digest(
            [CoverLeaf(**leaf) for leaf in body["leaves"]]
        )
    if mutation != "digest":
        changed["checkpoint_sha256"] = canonical_sha256(body)
    with pytest.raises((ValueError, TypeError)):
        _restore_cover_checkpoint(changed, REPOSITORY, **arguments)


def test_rectilinear_neutral_core_is_an_exact_owned_forest() -> None:
    phase_upper = Decimal(decimal_upper(pi_interval(PRECISION_BITS).upper))
    roots = _root_rectangles(phase_upper)
    riesz = json.loads(
        (REPOSITORY / "experiments/results/leaky_floquet_riesz_reduction.json")
        .read_text(encoding="utf-8")
    )["artifact"]["branches"]["outer_pulse"]
    radius = Decimal(riesz["local_complex_exclusion_radius_lower"])
    assert len(roots) == 3
    assert _rectilinear_root_partition_validated(roots, phase_upper, radius)
    assert 2 * Fraction(NEUTRAL_CORE_SIZE) ** 2 < Fraction(radius) ** 2
    root_leaves = tuple(
        CoverLeaf(root.root_id, "", "geometry", "0", "0", "0")
        for root in roots
    )
    assert _normalized_area_fraction(root_leaves, roots) == "1"

    core, right, upper = roots
    assert _rectangle_is_neutral_core_root(core)
    assert not _rectangle_is_neutral_core_root(right)
    assert not _rectangle_is_neutral_core_root(upper)
    assert not _rectangle_is_neutral_core_root(_split_rectangle(core)[0])
    gap = (
        core,
        _Rectangle(
            right.root_id,
            right.path,
            Decimal("0.0021"),
            right.sigma_upper,
            right.phase_lower,
            right.phase_upper,
        ),
        upper,
    )
    overlap = (
        core,
        right,
        _Rectangle(
            upper.root_id,
            upper.path,
            upper.sigma_lower,
            upper.sigma_upper,
            Decimal("0.0019"),
            upper.phase_upper,
        ),
    )
    wrong_owner = (
        _Rectangle(
            "right_strip",
            core.path,
            core.sigma_lower,
            core.sigma_upper,
            core.phase_lower,
            core.phase_upper,
        ),
        right,
        upper,
    )
    for mutation in (gap, overlap, wrong_owner):
        assert not _rectilinear_root_partition_validated(
            mutation, phase_upper, radius
        )


def test_tracked_result_sha_is_registered() -> None:
    assert hashlib.sha256(RESULT.read_bytes()).hexdigest() == EXPECTED_RESULT_SHA256


def test_tracked_result_is_source_bound_and_replays(payload: dict) -> None:
    validate_outer_right_half_result(payload, REPOSITORY, validate_parent=False)


def test_complete_exact_partition_and_strict_cover(payload: dict) -> None:
    certificate = payload["certificate"]
    assert certificate["pending_cell_count"] == 0
    assert certificate["accepted_leaf_count"] == len(certificate["leaves"])
    assert certificate["processed_cell_count"] == (
        2 * len(certificate["leaves"])
        - certificate["root_rectangle_count"]
    )
    assert certificate["accepted_normalized_area_fraction"] == "1"
    assert certificate["local_disk_leaf_count"] == 1
    assert certificate["neumann_leaf_count"] > 0
    assert certificate["maximum_depth"] > 0
    assert Decimal(certificate["maximum_contraction_upper"]) <= Decimal("0.995")
    assert Decimal(certificate["minimum_contraction_margin_lower"]) > 0
    assert certificate["worst_cell_finer_split_stress_strict"]
    assert Decimal(certificate["worst_cell_stress_contraction_upper"]) < 1
    assert Decimal(
        certificate["worst_cell_finer_split_stress_maximum_contraction_upper"]
    ) < 1
    worst = certificate["worst_cell"]
    assert Decimal(worst["finite_output_frequency_upper"]) > 0
    assert Decimal(
        worst["finite_from_tail_convolution_orbit_correction_upper"]
    ) == Decimal(worst["finite_convolution_orbit_correction_upper"])


def test_leaky_operator_support_and_claim_boundary(payload: dict) -> None:
    certificate = payload["certificate"]
    scope = payload["scope"]
    assert COEFFICIENT_SUPPORT_RADIUS == 256
    assert certificate["leaky_recovery_bottom_right_pencil_validated"]
    assert certificate["correct_fast_and_slow_tail_inverses_used"]
    assert certificate["full_mode_256_coefficient_support_used"]
    assert certificate["delay_operator_representation"].startswith(
        "unshifted-coefficient-output-phase"
    )
    assert certificate["period_correction_frequency_representation"] == (
        "total-output-mode phase for S_alpha M_b"
    )
    assert certificate["complex_split_wiener_norm_used"]
    assert certificate["directed_outer_nontranslation_right_half_zero_count"] == 0
    assert certificate["center_parameter_outer_floquet_count_validated"]
    assert not certificate["parameter_box_uniform_outer_floquet_count_validated"]
    assert scope["center_parameter_outer_floquet_count_validated"]
    assert not scope["parameter_box_uniform_outer_floquet_count_validated"]
    for name in TRUE_ON_COMPLETE:
        assert certificate[name] is True
    for name in ALWAYS_FALSE:
        assert certificate[name] is False
    source_hashes = payload["manifest"]["source_sha256"]
    assert "src/canard_control/floquet_cover_arithmetic.py" in source_hashes
    assert source_hashes[
        "src/canard_control/floquet_cover_arithmetic.py"
    ] == EXPECTED_SHARED_ARITHMETIC_SHA256
    assert (
        "src/canard_control/fhn_synchronous_floquet_right_half_cover.py"
        not in source_hashes
    )
    assert (
        "src/canard_control/fhn_bloch_outer_validation.py"
        not in source_hashes
    )


def test_nested_ball_is_derived_from_fixed_outer_source(payload: dict) -> None:
    certificate = payload["certificate"]
    assert certificate["source_orbit_correction_radius"] == "1e-5"
    assert certificate["correction_radius"] == "1e-8"
    assert certificate["nested_ball_majorant_validity_radius"] == "1e-5"
    assert Decimal(certificate["nested_ball_contraction_upper"]) < 1
    assert Decimal(certificate["nested_ball_radii_margin_lower"]) > 0
    assert certificate["nested_outer_orbit_ball_radii_polynomial_validated"]


def _direct_convolution_columns(
    output_modes: np.ndarray,
    input_modes: np.ndarray,
    coefficients: dict[int, complex],
    rotations: np.ndarray,
) -> np.ndarray:
    """Small exact Gaussian-integer basis-vector convolution oracle."""

    result = np.zeros((len(output_modes), len(input_modes)), dtype=complex)
    for column, input_mode in enumerate(input_modes):
        basis_value = rotations[column]
        for row, output_mode in enumerate(output_modes):
            result[row, column] = (
                coefficients.get(int(output_mode - input_mode), 0j)
                * basis_value
            )
    return result


def _direct_convolution_rows(
    output_modes: np.ndarray,
    input_modes: np.ndarray,
    coefficients: dict[int, complex],
    rotations: np.ndarray,
) -> np.ndarray:
    result = np.zeros((len(output_modes), len(input_modes)), dtype=complex)
    for row, output_mode in enumerate(output_modes):
        for column, input_mode in enumerate(input_modes):
            result[row, column] = (
                rotations[row]
                * coefficients.get(int(output_mode - input_mode), 0j)
            )
    return result


def _shifted_coefficients(
    coefficients: dict[int, complex], power: int
) -> dict[int, complex]:
    return {
        mode: value * (1j) ** (-power * mode)
        for mode, value in coefficients.items()
    }


def test_unshifted_row_and_shifted_column_delay_forms_are_equivalent() -> None:
    rng = np.random.default_rng(20260825)
    support = range(-4, 5)
    current = {
        mode: complex(*rng.integers(-3, 4, size=2)) for mode in support
    }
    delayed_0 = {
        mode: complex(*rng.integers(-3, 4, size=2)) for mode in support
    }
    delayed_1 = {
        mode: complex(*rng.integers(-3, 4, size=2)) for mode in support
    }
    finite_modes = np.arange(-2, 3)
    tail_modes = np.asarray([-6, -5, -4, 4, 5, 6])

    def rotations(modes: np.ndarray, power: int) -> np.ndarray:
        # Gaussian units keep the oracle bit-exact: alpha=1/4 or 1/2.
        return np.asarray([(1j) ** (-power * int(mode)) for mode in modes])

    finite_r0 = rotations(finite_modes, 1)
    finite_r1 = rotations(finite_modes, 2)
    tail_r0 = rotations(tail_modes, 1)
    tail_r1 = rotations(tail_modes, 2)
    shifted_0 = _shifted_coefficients(delayed_0, 1)
    shifted_1 = _shifted_coefficients(delayed_1, 2)

    current_matrix = _coefficient_matrix(
        finite_modes, finite_modes, current
    )
    assert np.array_equal(
        current_matrix,
        _direct_convolution_columns(
            finite_modes,
            finite_modes,
            current,
            np.ones(len(finite_modes), dtype=complex),
        ),
    )
    finite_delay = (
        _output_rotated_convolution(
            _coefficient_matrix(finite_modes, finite_modes, delayed_0),
            finite_r0,
        )
        + _output_rotated_convolution(
            _coefficient_matrix(finite_modes, finite_modes, delayed_1),
            finite_r1,
        )
    )
    finite_oracle = _direct_convolution_rows(
        finite_modes, finite_modes, delayed_0, finite_r0
    ) + _direct_convolution_rows(
        finite_modes, finite_modes, delayed_1, finite_r1
    )
    for coefficients, shifted, mode_rotations in (
        (delayed_0, shifted_0, finite_r0),
        (delayed_1, shifted_1, finite_r1),
    ):
        row_form = _output_rotated_convolution(
            _coefficient_matrix(finite_modes, finite_modes, coefficients),
            mode_rotations,
        )
        column_form = _input_rotated_convolution(
            _coefficient_matrix(finite_modes, finite_modes, shifted),
            mode_rotations,
        )
        assert np.array_equal(
            row_form,
            _direct_convolution_rows(
                finite_modes,
                finite_modes,
                coefficients,
                mode_rotations,
            ),
        )
        assert np.array_equal(row_form, column_form)
    assert np.array_equal(finite_delay, finite_oracle)

    period = 3.0
    epsilon = 0.25
    frequency = 1.0 + 2.0j * finite_modes
    top = np.diag(frequency) - period * (current_matrix + finite_delay)
    identity = np.eye(len(finite_modes), dtype=complex)
    full_finite = np.block(
        [
            [top, period * identity],
            [
                -period * epsilon * identity,
                np.diag(frequency + period * epsilon),
            ],
        ]
    )
    top_oracle = np.diag(frequency) - period * (
        _direct_convolution_columns(
            finite_modes,
            finite_modes,
            current,
            np.ones(len(finite_modes), dtype=complex),
        )
        + finite_oracle
    )
    full_oracle = np.block(
        [
            [top_oracle, period * identity],
            [
                -period * epsilon * identity,
                np.diag(frequency + period * epsilon),
            ],
        ]
    )
    assert np.array_equal(full_finite, full_oracle)

    tail_to_finite = (
        _output_rotated_convolution(
            _coefficient_matrix(finite_modes, tail_modes, delayed_0),
            finite_r0,
        )
        + _output_rotated_convolution(
            _coefficient_matrix(finite_modes, tail_modes, delayed_1),
            finite_r1,
        )
    )
    assert np.array_equal(
        tail_to_finite,
        _direct_convolution_rows(
            finite_modes, tail_modes, delayed_0, finite_r0
        )
        + _direct_convolution_rows(
            finite_modes, tail_modes, delayed_1, finite_r1
        ),
    )
    assert np.array_equal(
        _coefficient_matrix(finite_modes, tail_modes, current),
        _direct_convolution_columns(
            finite_modes,
            tail_modes,
            current,
            np.ones(len(tail_modes), dtype=complex),
        ),
    )
    for coefficients, shifted, row_rotations, column_rotations in (
        (delayed_0, shifted_0, finite_r0, tail_r0),
        (delayed_1, shifted_1, finite_r1, tail_r1),
    ):
        row_form = _output_rotated_convolution(
            _coefficient_matrix(finite_modes, tail_modes, coefficients),
            row_rotations,
        )
        column_form = _input_rotated_convolution(
            _coefficient_matrix(finite_modes, tail_modes, shifted),
            column_rotations,
        )
        assert np.array_equal(row_form, column_form)

    finite_to_tail = (
        _output_rotated_convolution(
            _coefficient_matrix(tail_modes, finite_modes, delayed_0),
            tail_r0,
        )
        + _output_rotated_convolution(
            _coefficient_matrix(tail_modes, finite_modes, delayed_1),
            tail_r1,
        )
    )
    assert np.array_equal(
        finite_to_tail,
        _direct_convolution_rows(
            tail_modes, finite_modes, delayed_0, tail_r0
        )
        + _direct_convolution_rows(
            tail_modes, finite_modes, delayed_1, tail_r1
        ),
    )
    assert np.array_equal(
        _coefficient_matrix(tail_modes, finite_modes, current),
        _direct_convolution_columns(
            tail_modes,
            finite_modes,
            current,
            np.ones(len(finite_modes), dtype=complex),
        ),
    )
    for coefficients, shifted, row_rotations, column_rotations in (
        (delayed_0, shifted_0, tail_r0, finite_r0),
        (delayed_1, shifted_1, tail_r1, finite_r1),
    ):
        row_form = _output_rotated_convolution(
            _coefficient_matrix(tail_modes, finite_modes, coefficients),
            row_rotations,
        )
        column_form = _input_rotated_convolution(
            _coefficient_matrix(tail_modes, finite_modes, shifted),
            column_rotations,
        )
        assert np.array_equal(row_form, column_form)

    wrong_unshifted_column = (
        _input_rotated_convolution(
            _coefficient_matrix(finite_modes, finite_modes, delayed_0),
            finite_r0,
        )
        + _input_rotated_convolution(
            _coefficient_matrix(finite_modes, finite_modes, delayed_1),
            finite_r1,
        )
    )
    wrong_shifted_row = (
        _output_rotated_convolution(
            _coefficient_matrix(finite_modes, finite_modes, shifted_0),
            finite_r0,
        )
        + _output_rotated_convolution(
            _coefficient_matrix(finite_modes, finite_modes, shifted_1),
            finite_r1,
        )
    )
    assert not np.array_equal(wrong_unshifted_column, finite_oracle)
    assert not np.array_equal(wrong_shifted_row, finite_oracle)


def test_directed_delay_representations_agree_and_mixed_forms_separate(
    outer_base,
) -> None:
    base = outer_base
    precision = PRECISION_BITS

    def contains_zero(value) -> bool:
        return (
            value.real.lower <= 0 <= value.real.upper
            and value.imag.lower <= 0 <= value.imag.upper
        )

    def excludes_zero(value) -> bool:
        return not contains_zero(value)

    correct_differences = []
    wrong_unshifted_column = []
    wrong_shifted_row = []
    pairs = ((2, -1), (5, 1), (-3, 2), (64, -64), (0, 1))
    for delay_index, tau in enumerate(
        (base.parameters["tau_0"], base.parameters["tau_1"])
    ):
        alpha = tau / base.period
        for output_mode, input_mode in pairs:
            difference = output_mode - input_mode
            unshifted = base.delayed_state_derivative[difference]
            shifted = base.delayed_coefficients[delay_index][difference]
            output_rotation = complex_unit_interval(
                -(pi_interval(precision) * (2 * output_mode) * alpha)
            )
            input_rotation = complex_unit_interval(
                -(pi_interval(precision) * (2 * input_mode) * alpha)
            )
            physical = unshifted * output_rotation
            equivalent = shifted * input_rotation
            correct_differences.append(physical - equivalent)
            wrong_unshifted_column.append(
                physical - unshifted * input_rotation
            )
            wrong_shifted_row.append(
                physical - shifted * output_rotation
            )
    assert all(contains_zero(value) for value in correct_differences)
    assert any(excludes_zero(value) for value in wrong_unshifted_column)
    assert any(excludes_zero(value) for value in wrong_shifted_row)


def test_actual_candidate_blocks_match_output_mode_direct_oracle(
    outer_source,
) -> None:
    orbit, base = outer_source
    precision = PRECISION_BITS
    candidate = _prepare_outer_candidate(orbit, base, precision)
    sigma = DirectedInterval.from_decimal("0.75", precision)
    phase = DirectedInterval.from_decimal("0.5", precision)
    (
        finite,
        derivative,
        finite_tail,
        finite_tail_derivative,
        tail_finite,
        tail_finite_derivative,
        _,
    ) = _candidate_matrices(
        candidate, base, sigma, phase, precision
    )
    period = float(base.period.lower)
    epsilon = float(base.parameters["epsilon"].lower)
    taus = tuple(
        float(value.lower)
        for value in (base.parameters["tau_0"], base.parameters["tau_1"])
    )
    alpha = tuple(value / period for value in taus)
    center_factor = tuple(
        np.exp(-complex(float(sigma.lower), float(phase.lower)) * value)
        for value in alpha
    )
    finite_rotations = tuple(
        center_factor[index] * candidate.finite_mode_rotations[index]
        for index in range(2)
    )
    tail_rotations = tuple(
        center_factor[index] * candidate.tail_mode_rotations[index]
        for index in range(2)
    )
    modes = candidate.modes
    tail_modes = candidate.tail_modes

    def assert_binary_assembly_close(left: np.ndarray, right: np.ndarray) -> None:
        # The implementation updates blocks in-place while the oracle sums
        # basis-column terms first, so their binary addition order differs.
        # This tolerance is diagnostic only; claim-bearing formation error is
        # recomputed outward in _candidate_matrices.
        assert np.allclose(left, right, rtol=0, atol=2e-12)

    for output_modes, input_modes, stored in (
        (modes, modes, candidate.current_finite),
        (modes, tail_modes, candidate.current_finite_tail),
        (tail_modes, modes, candidate.current_tail_finite),
    ):
        assert np.array_equal(
            stored,
            _direct_convolution_columns(
                output_modes,
                input_modes,
                dict(candidate.current_coefficients),
                np.ones(len(input_modes), dtype=complex),
            ),
        )

    delayed_finite = sum(
        (
            _direct_convolution_rows(
                modes,
                modes,
                dict(candidate.delayed_coefficients),
                rotation,
            )
            for rotation in finite_rotations
        ),
        np.zeros_like(candidate.delayed_finite),
    )
    frequency = float(sigma.lower) + 1j * (
        float(phase.lower) + 2 * np.pi * modes
    )
    top = (
        np.diag(frequency)
        - period * candidate.current_finite
        - period * delayed_finite
    )
    identity = np.eye(len(modes), dtype=complex)
    zero = np.zeros_like(identity)
    expected_finite = np.block(
        [
            [top, period * identity],
            [
                -period * epsilon * identity,
                np.diag(frequency + period * epsilon),
            ],
        ]
    )
    derivative_top = identity + sum(
        (
            tau
            * _direct_convolution_rows(
                modes,
                modes,
                dict(candidate.delayed_coefficients),
                rotation,
            )
            for tau, rotation in zip(taus, finite_rotations, strict=True)
        ),
        np.zeros_like(identity),
    )
    expected_derivative = np.block(
        [[derivative_top, zero], [zero, identity]]
    )
    assert_binary_assembly_close(finite, expected_finite)
    assert_binary_assembly_close(derivative, expected_derivative)

    delayed_finite_tail = sum(
        (
            _direct_convolution_rows(
                modes,
                tail_modes,
                dict(candidate.delayed_coefficients),
                rotation,
            )
            for rotation in finite_rotations
        ),
        np.zeros_like(candidate.delayed_finite_tail),
    )
    finite_tail_top = (
        -period * candidate.current_finite_tail
        - period * delayed_finite_tail
    )
    expected_finite_tail = np.vstack(
        (finite_tail_top, np.zeros_like(finite_tail_top))
    )
    finite_tail_derivative_top = sum(
        (
            tau
            * _direct_convolution_rows(
                modes,
                tail_modes,
                dict(candidate.delayed_coefficients),
                rotation,
            )
            for tau, rotation in zip(taus, finite_rotations, strict=True)
        ),
        np.zeros_like(candidate.delayed_finite_tail),
    )
    expected_finite_tail_derivative = np.vstack(
        (
            finite_tail_derivative_top,
            np.zeros_like(finite_tail_derivative_top),
        )
    )
    assert_binary_assembly_close(finite_tail, expected_finite_tail)
    assert_binary_assembly_close(
        finite_tail_derivative, expected_finite_tail_derivative
    )

    delayed_tail_finite = sum(
        (
            _direct_convolution_rows(
                tail_modes,
                modes,
                dict(candidate.delayed_coefficients),
                rotation,
            )
            for rotation in tail_rotations
        ),
        np.zeros_like(candidate.delayed_tail_finite),
    )
    expected_tail_finite = (
        -period * candidate.current_tail_finite
        - period * delayed_tail_finite
    )
    expected_tail_finite_derivative = sum(
        (
            tau
            * _direct_convolution_rows(
                tail_modes,
                modes,
                dict(candidate.delayed_coefficients),
                rotation,
            )
            for tau, rotation in zip(taus, tail_rotations, strict=True)
        ),
        np.zeros_like(candidate.delayed_tail_finite),
    )
    assert_binary_assembly_close(tail_finite, expected_tail_finite)
    assert_binary_assembly_close(
        tail_finite_derivative, expected_tail_finite_derivative
    )

    wrong_unshifted_column = sum(
        (
            _input_rotated_convolution(
                candidate.delayed_finite, rotation
            )
            for rotation in finite_rotations
        ),
        np.zeros_like(candidate.delayed_finite),
    )
    assert np.max(np.abs(delayed_finite - wrong_unshifted_column)) > 1e-6


def test_orbit_period_corrections_use_total_output_frequencies(
    outer_base,
) -> None:
    """Independent directed oracle rejects input-only period mutants."""

    precision = PRECISION_BITS
    base = outer_base
    correction = DirectedInterval.from_decimal("1e-8", precision)
    rectangle = _Rectangle(
        "oracle",
        "",
        Decimal("0.5"),
        Decimal("1.25"),
        Decimal("0.25"),
        Decimal("0.75"),
    )
    fast_tail_inverse = DirectedInterval.from_decimal(
        "0.003", precision
    ).upper
    actual = _orbit_corrections(
        base,
        correction,
        rectangle,
        DirectedInterval.from_decimal("0.125", precision).upper,
        fast_tail_inverse,
        precision,
    )

    r = correction.upper
    current_center = _sequence_box_norm_upper(
        base.current_coefficient, precision
    )
    delayed_center = _sequence_box_norm_upper(
        base.delayed_state_derivative, precision
    )
    voltage = _sequence_box_norm_upper(base.voltage, precision)
    centered = _sequence_box_norm_upper(base.centered_voltage, precision)
    epsilon = base.parameters["epsilon"].upper
    kappa_3 = base.parameters["kappa_3"].upper
    sqrt_two = DirectedInterval.from_decimal(2, precision).sqrt().upper
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        current_variation = (
            (2 * voltage + r) * r
            + 3 * epsilon * kappa_3 * (2 * centered + r) * r
        )
        delayed_variation = (
            3 * epsilon * kappa_3 * (2 * centered + r) * r / 2
        )
        current_uniform = current_center + current_variation
        delayed_uniform = delayed_center + delayed_variation
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        period_lower = base.period.lower - r

    sigma = DirectedInterval.from_decimal("1.25", precision)
    phase = DirectedInterval.from_decimal("0.75", precision)
    finite_frequency = (
        sigma * sigma
        + (pi_interval(precision) * (2 * FOURIER_CUTOFF) + phase) ** 2
    ).sqrt().upper
    finite_from_tail_frequency = (
        sigma * sigma
        + (
            pi_interval(precision)
            * (2 * (FOURIER_CUTOFF + COEFFICIENT_SUPPORT_RADIUS))
            + phase
        )
        ** 2
    ).sqrt().upper
    finite_delay_terms = []
    row_phase_tail_terms = []
    input_only_finite_tail_terms = []
    split_radius = DirectedInterval.from_decimal(
        "0.125", precision
    ).upper
    for tau in (base.parameters["tau_0"], base.parameters["tau_1"]):
        with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
            common = (
                r * delayed_uniform
                + base.period.upper * delayed_variation
            )
            finite_delay_terms.append(
                sqrt_two
                * (
                    common
                    + delayed_center
                    * tau.upper
                    * finite_frequency
                    * r
                    / period_lower
                )
            )
            input_only_finite_tail_terms.append(
                sqrt_two
                * (
                    common
                    + delayed_center
                    * tau.upper
                    * finite_from_tail_frequency
                    * r
                    / period_lower
                )
            )
            row_phase_tail_terms.append(
                sqrt_two
                * (
                    fast_tail_inverse * common
                    + delayed_center
                    * tau.upper
                    * r
                    / period_lower
                    * (1 + fast_tail_inverse * split_radius)
                )
            )
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        current_term = (
            r * current_uniform + base.period.upper * current_variation
        )
        finite_convolution = current_term + sum(
            finite_delay_terms, gmpy2.mpfr(0)
        )
        finite_full = max(
            finite_convolution + epsilon * r,
            (1 + epsilon) * r,
        )
        row_phase_tail_from_finite = (
            fast_tail_inverse * current_term
            + sum(row_phase_tail_terms, gmpy2.mpfr(0))
        )
        input_only_finite_tail = current_term + sum(
            input_only_finite_tail_terms, gmpy2.mpfr(0)
        )
        input_only_tail_from_finite = fast_tail_inverse * finite_convolution

    expected = (
        finite_convolution,
        finite_full,
        finite_convolution,
        row_phase_tail_from_finite,
    )
    assert actual[:4] == expected
    assert actual[4]["finite_output_frequency"] == finite_frequency
    # Mutant 1: shifted coefficient treated as T-independent, hence |m|=320.
    assert actual[2] != input_only_finite_tail
    # Mutant 2: input-only finite frequency followed by the fast tail inverse.
    assert actual[3] != input_only_tail_from_finite


def _duplicate_leaf(payload: dict) -> None:
    certificate = payload["certificate"]
    certificate["leaves"][-1] = deepcopy(certificate["leaves"][0])
    _refresh_leaf_records(certificate)
    _refresh_certificate(payload)


def _omit_leaf_and_rebalance_scalars(payload: dict) -> None:
    certificate = payload["certificate"]
    removed = certificate["leaves"].pop(len(certificate["leaves"]) // 2)
    certificate["accepted_leaf_count"] -= 1
    certificate[
        "local_disk_leaf_count"
        if removed["proof_kind"] == "riesz_local_disk"
        else "neumann_leaf_count"
    ] -= 1
    certificate["processed_cell_count"] = 2 * len(certificate["leaves"]) - 1
    _refresh_leaf_records(certificate)
    _refresh_certificate(payload)


def _overlap_with_ancestor_leaf(payload: dict) -> None:
    certificate = payload["certificate"]
    leaf = next(
        item
        for item in certificate["leaves"]
        if item["proof_kind"] == "full_operator_neumann"
        and len(item["path"]) >= 4
    )
    leaf["path"] = leaf["path"][:-2]
    _refresh_leaf_records(certificate)
    _refresh_certificate(payload)


def _misclassify_local_leaf(payload: dict) -> None:
    certificate = payload["certificate"]
    leaf = next(
        item for item in certificate["leaves"]
        if item["proof_kind"] == "riesz_local_disk"
    )
    leaf["proof_kind"] = "full_operator_neumann"
    certificate["local_disk_leaf_count"] -= 1
    certificate["neumann_leaf_count"] += 1
    _refresh_leaf_records(certificate)
    _refresh_certificate(payload)


def _misclassify_neumann_leaf(payload: dict) -> None:
    certificate = payload["certificate"]
    leaf = next(
        item for item in certificate["leaves"]
        if item["proof_kind"] == "full_operator_neumann"
    )
    leaf["proof_kind"] = "riesz_local_disk"
    leaf["contraction_upper"] = "0"
    leaf["finite_input_column_sum_upper"] = "0"
    leaf["tail_input_column_sum_upper"] = "0"
    certificate["neumann_leaf_count"] -= 1
    certificate["local_disk_leaf_count"] += 1
    _refresh_leaf_records(certificate)
    _refresh_certificate(payload)


def _promote_uniform_parameter_count(payload: dict) -> None:
    payload["certificate"][
        "parameter_box_uniform_outer_floquet_count_validated"
    ] = True
    _refresh_certificate(payload)


def _break_conjugacy_seam(payload: dict) -> None:
    payload["certificate"]["real_axis_conjugacy_seam_validated"] = False
    _refresh_certificate(payload)


def _shrink_upper_phase(payload: dict) -> None:
    payload["certificate"]["upper_phase_upper"] = "3"
    _refresh_certificate(payload)


def _forge_maximum_depth(payload: dict) -> None:
    payload["certificate"]["maximum_depth"] -= 1
    _refresh_certificate(payload)


def _shrink_nested_radius_without_replay(payload: dict) -> None:
    payload["certificate"]["correction_radius"] = "1e-10"
    _refresh_certificate(payload)


@pytest.mark.parametrize(
    "mutation",
    [
        _duplicate_leaf,
        _omit_leaf_and_rebalance_scalars,
        _overlap_with_ancestor_leaf,
        _misclassify_local_leaf,
        _misclassify_neumann_leaf,
        _promote_uniform_parameter_count,
        _break_conjugacy_seam,
        _shrink_upper_phase,
        _forge_maximum_depth,
        _shrink_nested_radius_without_replay,
    ],
)
def test_hostile_partition_seam_and_scope_mutations_are_rejected(
    payload: dict, mutation
) -> None:
    changed = deepcopy(payload)
    mutation(changed)
    with pytest.raises((ValueError, TypeError)):
        validate_outer_right_half_result(
            changed, REPOSITORY, validate_parent=False
        )


def test_hostile_source_and_parent_rebinding_is_rejected(payload: dict) -> None:
    changed = deepcopy(payload)
    changed["manifest"]["source_sha256"][
        "src/canard_control/leaky_periodic_validation.py"
    ] = "0" * 64
    with pytest.raises(ValueError):
        validate_outer_right_half_result(
            changed, REPOSITORY, validate_parent=False
        )
    changed = deepcopy(payload)
    changed["certificate"]["riesz_result_sha256"] = "0" * 64
    _refresh_certificate(changed)
    with pytest.raises(ValueError):
        validate_outer_right_half_result(
            changed, REPOSITORY, validate_parent=False
        )
