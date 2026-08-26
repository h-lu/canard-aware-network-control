from __future__ import annotations

from copy import deepcopy
from decimal import Decimal
import hashlib
import json
from pathlib import Path
from types import SimpleNamespace

import gmpy2
import numpy as np
import pytest

from canard_control.directed_interval import (
    DirectedComplexInterval,
    DirectedInterval,
    pi_interval,
)
from canard_control.floquet_cover_arithmetic import _coefficient_matrix
from canard_control.leaky_floquet_compact_cover_engine import (
    CoverLeaf,
    Rectangle,
    _orbit_corrections,
    leaf_digest,
    output_rotated_convolution,
    prefix_complete,
    rectangle_strictly_inside_origin_disk,
    split_rectangle,
)
from canard_control.leaky_floquet_inner_unstable_root import (
    physical_delay_convolution_oracle_error,
)
from canard_control.leaky_floquet_inner_right_half_cover import (
    ALWAYS_FALSE,
    COEFFICIENT_SUPPORT_RADIUS,
    PRECISION_BITS,
    RESULT_RELATIVE_PATH,
    SOURCE_MANIFEST,
    STRUCTURAL_TRUE,
    TRUE_ON_COMPLETE,
    canonical_sha256,
    validate_inner_right_half_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]
RESULT = REPOSITORY / RESULT_RELATIVE_PATH
EXPECTED_RESULT_SHA256 = (
    "f0458acf59b8fad96e43f204df37fd8d37f356ebbf67701180c8ff31c668739a"
)


@pytest.fixture(scope="module")
def payload() -> dict:
    return json.loads(RESULT.read_text(encoding="utf-8"))


def _refresh_certificate(payload: dict) -> None:
    payload["manifest"]["certificate_sha256"] = canonical_sha256(
        payload["certificate"]
    )


def test_tracked_result_sha_is_registered() -> None:
    assert hashlib.sha256(RESULT.read_bytes()).hexdigest() == EXPECTED_RESULT_SHA256


def test_tracked_result_is_source_bound(payload: dict) -> None:
    validate_inner_right_half_result(
        payload, REPOSITORY, validate_parents=False
    )


def test_complete_count_and_claim_boundary(payload: dict) -> None:
    certificate = payload["certificate"]
    assert certificate["pending_cell_count"] == 0
    assert certificate["accepted_normalized_root_fraction"] == "3"
    assert certificate["neutral_disk_characteristic_value_count"] == 1
    assert certificate["positive_disk_characteristic_value_count"] == 1
    assert certificate["compact_keyhole_characteristic_value_count"] == 0
    assert certificate["directed_closed_right_half_characteristic_value_count"] == 2
    assert certificate[
        "closed_right_half_nontranslation_characteristic_value_count"
    ] == 1
    assert certificate["directed_unstable_multiplier_count"] == 1
    assert certificate["inner_no_other_right_half_roots_validated"]
    assert certificate["inner_total_unstable_multiplier_count_validated"]
    assert certificate["inner_saddle_floquet_index_validated"]
    assert Decimal(certificate["maximum_contraction_upper"]) <= Decimal("0.995")
    assert Decimal(certificate["minimum_contraction_margin_lower"]) > 0
    assert certificate["worst_cell_finer_split_stress_strict"]
    for name in STRUCTURAL_TRUE + TRUE_ON_COMPLETE:
        assert certificate[name] is True
    for name in ALWAYS_FALSE:
        assert certificate[name] is False
    assert certificate["accepted_leaf_count"] == 60432
    assert certificate["processed_cell_count"] == 120861
    assert certificate["neutral_disk_leaf_count"] == 61
    assert certificate["positive_disk_leaf_count"] == 202
    assert certificate["neumann_leaf_count"] == 60169
    assert certificate["leaf_partition_sha256"] == (
        "8d105b4d17e2628c216dbd8fa8474b886f6d1d9684dcaaff279f4bb6f563baa5"
    )
    assert COEFFICIENT_SUPPORT_RADIUS == 128


def _direct_rows(
    outputs: np.ndarray,
    inputs: np.ndarray,
    coefficients: dict[int, complex],
    rotations: np.ndarray,
) -> np.ndarray:
    return np.asarray(
        [
            [
                coefficients.get(int(k - m), 0j) * rotations[row]
                for m in inputs
            ]
            for row, k in enumerate(outputs)
        ],
        dtype=complex,
    )


def test_rectangular_physical_delay_convolution_uses_output_rows() -> None:
    rng = np.random.default_rng(20260825)
    coefficients = {
        mode: complex(*rng.integers(-3, 4, size=2))
        for mode in range(-8, 9)
    }
    finite = np.arange(-2, 3)
    tail = np.asarray([-6, -5, 5, 6])
    for outputs, inputs in (
        (finite, finite),
        (finite, tail),
        (tail, finite),
    ):
        rotations = np.asarray([(1j) ** (-int(mode)) for mode in outputs])
        matrix = _coefficient_matrix(outputs, inputs, coefficients)
        assert np.array_equal(
            output_rotated_convolution(matrix, rotations),
            _direct_rows(outputs, inputs, coefficients, rotations),
        )


def test_physical_delay_dual_representation_rejects_both_mixes() -> None:
    assert physical_delay_convolution_oracle_error(
        representation="unshifted_row"
    ) < 5e-15
    assert physical_delay_convolution_oracle_error(
        representation="shifted_column"
    ) < 5e-15
    assert physical_delay_convolution_oracle_error(
        representation="unshifted_column"
    ) > 1e-3
    assert physical_delay_convolution_oracle_error(
        representation="shifted_row"
    ) > 1e-3


def _point_complex(value: str, precision: int) -> DirectedComplexInterval:
    return DirectedComplexInterval.from_real(
        DirectedInterval.from_decimal(value, precision)
    )


def _synthetic_orbit_correction_base(precision: int) -> SimpleNamespace:
    point = lambda value: DirectedInterval.from_decimal(value, precision)
    return SimpleNamespace(
        period=point("2"),
        parameters={
            "epsilon": point("0.1"),
            "kappa_3": point("0.2"),
            "tau_0": point("0.3"),
            "tau_1": point("0.4"),
        },
        voltage={0: _point_complex("0.75", precision)},
        centered_voltage={0: _point_complex("0.5", precision)},
        current_coefficient={0: _point_complex("1.25", precision)},
        delayed_state_derivative={0: _point_complex("0.375", precision)},
    )


def _independent_orbit_correction_formula(
    base,
    correction_radius: DirectedInterval,
    rectangle: Rectangle,
    *,
    finite_output_mode: int,
    spectral_radius: gmpy2.mpfr,
    fast_tail_inverse: gmpy2.mpfr,
    precision: int,
) -> tuple[gmpy2.mpfr, gmpy2.mpfr, gmpy2.mpfr, gmpy2.mpfr]:
    """Recompute the four corrections without the engine implementation."""

    radius = correction_radius.upper
    period_upper = base.period.upper
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        period_lower = base.period.lower - radius
    sigma = DirectedInterval.from_decimal(
        format(rectangle.sigma_upper, "f"), precision
    ).upper
    phase = DirectedInterval.from_decimal(
        format(
            max(abs(rectangle.phase_lower), abs(rectangle.phase_upper)),
            "f",
        ),
        precision,
    ).upper
    pi_upper = pi_interval(precision).upper
    sqrt_two = DirectedInterval.from_decimal(2, precision).sqrt().upper

    def output_frequency(mode: int) -> gmpy2.mpfr:
        with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
            angular = 2 * pi_upper * mode + phase
            return gmpy2.sqrt(sigma * sigma + angular * angular)

    voltage = base.voltage[0].real.upper
    centered = base.centered_voltage[0].real.upper
    current_center = base.current_coefficient[0].real.upper
    delayed_center = base.delayed_state_derivative[0].real.upper
    epsilon = base.parameters["epsilon"].upper
    kappa_3 = base.parameters["kappa_3"].upper
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        tau_sum = (
            base.parameters["tau_0"].upper
            + base.parameters["tau_1"].upper
        )
        current_variation = (
            (2 * voltage + radius) * radius
            + 3
            * epsilon
            * kappa_3
            * (2 * centered + radius)
            * radius
        )
        delayed_variation = (
            3
            * epsilon
            * kappa_3
            * (2 * centered + radius)
            * radius
            / 2
        )
        current_uniform = current_center + current_variation
        delayed_uniform = delayed_center + delayed_variation
        current_term = (
            radius * current_uniform
            + period_upper * current_variation
        )
        delay_common = (
            2
            * (radius * delayed_uniform + period_upper * delayed_variation)
        )
        finite_convolution = current_term + sqrt_two * (
            delay_common
            + delayed_center
            * tau_sum
            * output_frequency(finite_output_mode)
            * radius
            / period_lower
        )
        finite_tail_convolution = finite_convolution
        finite_full = max(
            finite_convolution + epsilon * radius,
            (1 + epsilon) * radius,
        )
        tail_from_finite = fast_tail_inverse * current_term + sqrt_two * (
            fast_tail_inverse * delay_common
            + delayed_center
            * tau_sum
            * radius
            / period_lower
            * (1 + fast_tail_inverse * spectral_radius)
        )
    return (
        finite_convolution,
        finite_full,
        finite_tail_convolution,
        tail_from_finite,
    )


def _mpfr_relative_error(left: gmpy2.mpfr, right: gmpy2.mpfr) -> gmpy2.mpfr:
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
        return abs(left - right) / max(abs(left), abs(right), gmpy2.mpfr(1))


def test_orbit_correction_formula_oracle_uses_output_modes_and_tail_cancellation() -> None:
    precision = PRECISION_BITS
    base = _synthetic_orbit_correction_base(precision)
    radius = DirectedInterval.from_decimal("1e-6", precision)
    rectangle = Rectangle(
        "formula_oracle",
        "",
        Decimal("0.5"),
        Decimal("0.75"),
        Decimal("0.125"),
        Decimal("0.375"),
    )
    fast_tail_inverse = DirectedInterval.from_decimal(
        "0.01", precision
    ).upper
    actual = _orbit_corrections(
        base,
        radius,
        rectangle,
        fast_tail_inverse,
        64,
        precision,
    )[:4]
    expected = _independent_orbit_correction_formula(
        base,
        radius,
        rectangle,
        finite_output_mode=64,
        spectral_radius=DirectedInterval.from_decimal("0.25", precision).upper,
        fast_tail_inverse=fast_tail_inverse,
        precision=precision,
    )
    for measured, predicted in zip(actual, expected, strict=True):
        assert _mpfr_relative_error(measured, predicted) < gmpy2.mpfr("1e-40")

    assert actual[2] == actual[0]

    # A mixed unshifted-coefficient/column-phase derivation would use the
    # finite input frequency and then multiply the whole correction by the
    # tail inverse.  It is not the physical aligned-output formula and must
    # be numerically distinct from the independently recomputed result.
    mixed_column_mutant = fast_tail_inverse * actual[0]
    assert actual[3] != mixed_column_mutant


def _toy_complete_partition(*, seam_priority: bool) -> list[CoverLeaf]:
    root = Rectangle(
        "toy",
        "",
        Decimal(0),
        Decimal(1),
        Decimal(0),
        Decimal(1),
    )
    pending = [root]
    leaves: list[CoverLeaf] = []
    while pending:
        if seam_priority:
            pending.sort(
                key=lambda rectangle: (
                    rectangle.sigma_lower <= 0 <= rectangle.sigma_upper
                    and rectangle.phase_lower <= 0 <= rectangle.phase_upper,
                    rectangle.sigma_lower
                    <= Decimal("0.7")
                    <= rectangle.sigma_upper
                    and rectangle.phase_lower <= 0 <= rectangle.phase_upper,
                    len(rectangle.path),
                )
            )
        rectangle = pending.pop()
        in_neutral = rectangle_strictly_inside_origin_disk(
            rectangle, Decimal("0.2")
        )
        in_positive = (
            max(
                abs(rectangle.sigma_lower - Decimal("0.7")),
                abs(rectangle.sigma_upper - Decimal("0.7")),
            )
            ** 2
            + max(abs(rectangle.phase_lower), abs(rectangle.phase_upper)) ** 2
            < Decimal("0.1") ** 2
        )
        if in_neutral or in_positive or len(rectangle.path) // 2 >= 6:
            leaves.append(
                CoverLeaf(
                    rectangle.root_id,
                    rectangle.path,
                    "toy",
                    "0",
                    "0",
                    "0",
                )
            )
        else:
            first, second = split_rectangle(rectangle)
            pending.extend((second, first))
    return leaves


def test_seam_priority_changes_only_traversal_not_complete_partition() -> None:
    original = _toy_complete_partition(seam_priority=False)
    prioritised = _toy_complete_partition(seam_priority=True)
    assert prefix_complete(original, ("toy",))
    assert prefix_complete(prioritised, ("toy",))
    assert {(leaf.root_id, leaf.path) for leaf in original} == {
        (leaf.root_id, leaf.path) for leaf in prioritised
    }
    assert leaf_digest(original) == leaf_digest(prioritised)


@pytest.mark.parametrize(
    "mutation",
    [
        lambda value: value["certificate"].update(
            {"inner_no_other_right_half_roots_validated": False}
        ),
        lambda value: value["certificate"].update(
            {"directed_unstable_multiplier_count": 2}
        ),
        lambda value: value["certificate"].update(
            {"neutral_disk_characteristic_value_count": 2}
        ),
        lambda value: value["certificate"].update(
            {"positive_disk_characteristic_value_count": 2}
        ),
        lambda value: value["certificate"].update(
            {"compact_keyhole_characteristic_value_count": 1}
        ),
        lambda value: value["certificate"].update(
            {"closed_right_half_nontranslation_characteristic_value_count": 2}
        ),
        lambda value: value["certificate"].update(
            {"analytic_fredholm_argument_principle_additivity_used": False}
        ),
        lambda value: value["certificate"].update(
            {"leaf_partition_sha256": "0" * 64}
        ),
        lambda value: value["certificate"].update(
            {"positive_disk_radius": "0.2"}
        ),
        lambda value: value["certificate"].update(
            {"tail_output_frequency_cancellation_validated": False}
        ),
        lambda value: value["certificate"]["leaves"][0].update(
            {"proof_kind": "forged"}
        ),
        lambda value: value["manifest"].update(
            {"inner_root_result_sha256": "0" * 64}
        ),
        lambda value: value["manifest"]["source_sha256"].update(
            {SOURCE_MANIFEST[0]: "0" * 64}
        ),
        lambda value: value["scope"].update(
            {"physical_pulse_onset_validated": True}
        ),
    ],
)
def test_hostile_tampering_is_rejected(payload: dict, mutation) -> None:
    changed = deepcopy(payload)
    mutation(changed)
    _refresh_certificate(changed)
    with pytest.raises(ValueError):
        validate_inner_right_half_result(
            changed, REPOSITORY, validate_parents=False
        )


def test_manifest_avoids_old_or_active_phase_theorem_files(payload: dict) -> None:
    sources = payload["manifest"]["source_sha256"]
    assert "src/canard_control/leaky_floquet_compact_cover_engine.py" in sources
    assert "src/canard_control/floquet_cover_arithmetic.py" in sources
    active_outer = (
        "src/canard_control/leaky_floquet_outer_" + "right_half_cover.py"
    )
    assert active_outer not in sources
    assert "src/canard_control/fhn_synchronous_floquet_right_half_cover.py" not in sources
    assert "src/canard_control/fhn_bloch_outer_validation.py" not in sources


def test_note_states_count_and_scope() -> None:
    text = " ".join(
        (REPOSITORY / "docs/leaky-floquet-inner-right-half-cover.md")
        .read_text()
        .split()
    )
    assert "exactly two characteristic values" in text
    assert "exactly one unstable multiplier" in text
    assert "unshifted coefficients and output row phases" in text
    assert "aligned tail output frequency" in text
    assert "cover leaf counts" in text
    assert "argument-principle additivity" in text
    assert "N(D_0)=1" in text
    assert "N(D_u)=1" in text
    assert "N(K)=0" in text
    assert "not a common" in text
    assert "physical onset" in text
