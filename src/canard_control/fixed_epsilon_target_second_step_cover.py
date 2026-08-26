"""Validated continuation across the second target method-of-steps interval.

The active delays are four and five.  On ``1 <= t <= 3`` the delay-four
slot lies in the already enclosed first-step solution on ``[-3,-1]``.  The
delay-five slot lies successively in the affine incoming history, the exact
C4 patch, and the already enclosed first-step solution on ``[-3,-2]``.  The
only interior source changes are therefore ``t=3/2`` and ``t=2``.

For every time--label cell this module first replays the strict first-step
Picard enclosures and retains their normalized-time polynomials.  Integer
delays preserve the normalized cell coordinate, so these polynomials are
inserted directly into the second-step residual.  No sampled or interpolated
history is used in a claim-bearing operation.  A binary64 RK4 trace is used
only to center cubic Hermite error coordinates.

As in the first-step proof, three nested Picard arguments enclose the state
at the label center, its first label variation there, and the second label
variation on the whole label cell.  Two exact mean-value reconstructions
then enclose the full state and first-variation families.  The public
certificate requires strict closure and signs at 192 bits and a separate
same-kernel 256-bit replay.  The latter is a precision consistency check,
not an independent proof.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from decimal import Decimal, InvalidOperation
from functools import lru_cache
from hashlib import sha256
import json
import math
from pathlib import Path
import platform
from typing import Any, Mapping, Sequence

import gmpy2
import sympy as sp

import canard_control.fixed_epsilon_target_first_step_cover as first
from canard_control.directed_interval import DirectedInterval, decimal_lower, decimal_upper
from canard_control.fixed_epsilon_target_c4_preparation_seam import (
    c4_prepared_history_state,
    c4_prepared_history_transverse_derivative,
    right_jet_shape,
)
from canard_control.fixed_epsilon_target_first_step_interval import _entry_initial_box


PRIMARY_PRECISION_BITS = 192
REFINEMENT_PRECISION_BITS = 256
TIME_LEFT = "1"
TIME_RIGHT = "3"
TIME_STEP = "0.005"
FIRST_STEP_TIME_STEP = "0.01"
LABEL_LEFT = "-0.05"
LABEL_RIGHT = "0.05"
LABEL_STEP = "0.005"
DELAY_FIVE_PATCH_ENTRY_TIME = "1.5"
DELAY_FIVE_PHYSICAL_ENTRY_TIME = "2"

MODEL_ID = "fixed-epsilon-target-second-method-step-interval-cover"
AUDIT_ID = "fixed-epsilon-target-second-method-step-interval-cover-v1"
PROOF_SOURCE_RELATIVE_PATH = (
    "src/canard_control/fixed_epsilon_target_second_step_cover.py"
)
GENERATOR_RELATIVE_PATH = "experiments/fixed_epsilon_target_second_step_cover.py"
RESULT_RELATIVE_PATH = (
    "experiments/results/fixed_epsilon_target_second_step_cover.json"
)
SHARD_DIRECTORY_RELATIVE_PATH = (
    "experiments/results/fixed_epsilon_target_second_step_cover_shards"
)
NOTE_RELATIVE_PATH = "docs/fixed-epsilon-target-second-step-cover.md"
FIRST_STEP_SOURCE_RELATIVE_PATH = (
    "src/canard_control/fixed_epsilon_target_first_step_cover.py"
)
FIRST_STEP_RESULT_RELATIVE_PATH = (
    "experiments/results/fixed_epsilon_target_first_step_cover.json"
)
FIRST_STEP_RESULT_SHA256 = (
    "5228eafcb7b497d976c48e0ff78a277bbd13ec1ef7b72e685dbaa885e61c031a"
)
INTERVAL_BACKEND_SOURCE_RELATIVE_PATH = "src/canard_control/directed_interval.py"
C4_SEAM_SOURCE_RELATIVE_PATH = (
    "src/canard_control/fixed_epsilon_target_c4_preparation_seam.py"
)
PHYSICAL_MODEL_SOURCE_RELATIVE_PATH = (
    "src/canard_control/fixed_epsilon_frozen_graph_operator.py"
)
DEFAULT_COMMAND = (
    "PYTHONPATH=src /usr/bin/python3 "
    "experiments/fixed_epsilon_target_second_step_cover.py"
)
MANIFEST_ARITHMETIC = (
    "192-bit MPFR outward-rounded interval polynomials; retained strict "
    "first-step Picard tubes inserted as delay-four and delay-five sources; "
    "exact C4 delay-five history polynomials before t=2; exact power-to-"
    "Bernstein convex-hull bounds; degree-eight coupled Taylor centers and "
    "nested Euclidean error balls propagated with the exact two-dimensional "
    "logarithmic norm for the state, central first variation and full-label "
    "second variation; exact "
    "mean-value reconstruction in the label; separate same-kernel 256-bit "
    "precision replay; binary64 RK4 values used only as nonclaim centers"
)

# Filled only after every deterministic per-label computation has completed.
# These are proof-cell body digests, not claims of an independent replay.
EXPECTED_PROOF_CELL_DIGESTS: dict[int, tuple[str, ...]] = {
    PRIMARY_PRECISION_BITS: (
        "d78e93c30b7d6f0dea2ae3e5024343a97648283db06750f9a82b016d75cb62e0",
        "262161485b68cd658db8f3de3d099088b0c928dba5150a9eb92917d4fd1bf414",
        "fcb4727b990f1f2c486fee2bb466b05b14c4675fe364d39cfe7446fc9c6e79c6",
        "d4a7d214a21aae56f95da7d64f94ecb52b9117dc06a8e2cb14aca6d607e10f7c",
        "e8444dc0c49f3c60de1f902ef4ce517189184f621127b70dd093b6bd9885065c",
        "aad42e4b50792350a886438ed9444a275928bd9d6b9bd6c386d1741aaa0b8d7d",
        "44c8e29bf2707831ad7b15eb7ae73b55dabddf33477196f6c70e626eb0c0797b",
        "10b5aa19a73ddad9d798d2127cd3c00bd24ecd3b21a66af5d3eb71ef59d7b9c8",
        "ff8c01160df1c81e0c65a3d62458ea471b7b271075e53a56383c4a98113cc8c7",
        "f88c3ca69729b1a6b700a077bf86ba117ee1ca6d76e666b4ed620e894dd4e916",
        "e3e617690767131627eb95cb5927b64b5d68f076b71b399396a7f27d3400aa8c",
        "7905decf401351a126ff6fcb65554103968da180871099a221106d8550eab175",
        "1b5f62a45268cb5bbdef6dcb2b7b9070a009f51d812c7a8be22c0de1e6fe0fea",
        "a40494ca503c073fec356318d2ad048817dc8ea21e95225dd6ae53eb4b2ace85",
        "9c489d712af7ec7d24ab3debf5be5bfeafdd8ac81a23368cbe77517939144f80",
        "b67e118b0b475f96e74c283759320e2998e99f0f1c44b201d874000ba7258244",
        "a5eba015bd8bbefa06ddb724c157a8f0caa2f522dffb3e7ef45e5b2db2c8f052",
        "c5d3f750fadb6655c1dee42944eb6848985c154a64ef9e0aba6ebbc3760d9d4c",
        "9a179d6282c47faea92a0d2192ef5b641243049b620079cf0cd3c042379890b3",
        "d549349ae34ae3fbbbe568287619176ecbd444fa077e54c42aa7d41ff17a0b94",
    ),
    REFINEMENT_PRECISION_BITS: (
        "af302fdcaeb6138ebaf5faa800fa97c1fef6867ded4258e405c6f3a71ea083c6",
        "690309e41ea1d21f345a1b91d349b3a6ed2d0842e41174f5d34ac5a2f84e4a61",
        "8f660dc421eecc4a823cbd94977ed2b30efe49d3eb8445d71c959e2720b12269",
        "30a4cbb6d90a19cc7a037c42fb18e62070d588ccbc7d7c4f5df072fad89bd2ce",
        "16478c43017491d0e26384d9cbf0312cfaec72e11d4545ea35a963523c499ab2",
        "b18007c1c3fd12e099c9dec80285f5fbb66680876c866a18a86b37991b6f324f",
        "b38924da86460a97b33d2e1010a72cf561637798017e6629ad0553f228fbd6bb",
        "4da10f6e57b698cb412ac7bbff2a940add965bfd0e9bfc41381999a6de1fcc38",
        "da47037c3e877866bc36314231a61c4742ae1d6872af3cb527a281a217bad8e2",
        "bc28dc4c60a57142a1bffcbfbef9871816d135564e96ad387acbf84b62911cd1",
        "c47da479b075c787ec0c7d678d47d977aab446166ff181d47d107ed8b3664134",
        "847e2ac5df23f0b101f2c932cae63d9a5cf57ec32c33dd6ef4410f563c7af878",
        "a725197fa166e4e5c43df1b214da58faf7d5e831528d4d70a51c49b9c82e0362",
        "48588335daab3220930a4ed7cfd7eabcc3bd92fb79def1f9f88ccdad1810f31f",
        "2eb2c98b52e5a77fcb3ee26c2810f287cebb7b60b01800f2607acec919e97a12",
        "717791ea411f84161421a79ee3467c8890b61b9492090ef843823d3fad080439",
        "d9d392947cf427cb0c9b05975837cdb9fe25fb3c11eb11634af3f7d6aa27a4c8",
        "a775e5ffd0bceb1a2cb5643b17e6e5bc324190d5072cc095c47d6b261313a5c2",
        "d1874c38531b09af57d32675f90af331f5e03098d59a05d9b4743221d53baf64",
        "4dc2a26908e3a760e41cfc812a6d8ae8709111f60758f7c5aee071ded2d4e1db",
    ),
}

IntervalVector = tuple[DirectedInterval, ...]
IntervalPolynomial = tuple[DirectedInterval, ...]
PolynomialVector = tuple[IntervalPolynomial, ...]
FloatVector = tuple[float, ...]


def _point(value: str | int, precision: int) -> DirectedInterval:
    return DirectedInterval.from_decimal(value, precision)


def _float_point(value: float, precision: int) -> DirectedInterval:
    return DirectedInterval.from_float(value, precision)


def _closed(lower: str | int, upper: str | int, precision: int) -> DirectedInterval:
    return DirectedInterval.from_bounds(lower, upper, precision)


def _poly_constant(value: DirectedInterval) -> IntervalPolynomial:
    return (value,)


def _restrict_polynomial_to_half(
    value: IntervalPolynomial, half: int
) -> IntervalPolynomial:
    """Compose ``value(u)`` with ``u=(half+v)/2``, ``0<=v<=1``."""

    if half not in (0, 1):
        raise ValueError("the source-cell half must be zero or one")
    precision = value[0].precision
    affine = (
        _point(half, precision) / _point(2, precision),
        _point(1, precision) / _point(2, precision),
    )
    result: IntervalPolynomial = (_point(0, precision),)
    for exponent, coefficient in enumerate(value):
        result = first._poly_add(
            result,
            first._poly_scale(
                first._poly_power(affine, exponent), coefficient
            ),
        )
    return result


def _time_node(index: int) -> str:
    return format(Decimal(1) + Decimal(index) / Decimal(200), "f")


def _label_node(index: int) -> str:
    return format(Decimal("-0.05") + Decimal(index) / Decimal(200), "f")


def _state_rhs_from_slots(
    state: PolynomialVector,
    delayed_x4: IntervalPolynomial,
    delayed_x5: IntervalPolynomial,
) -> PolynomialVector:
    """Evaluate the exact frozen physical field from polynomial slots."""

    precision = state[0][0].precision
    rho = _point(5, precision).sqrt() / _point(5, precision)
    nu = _point("0.21256022233963731", precision)
    x, y = state
    x2 = first._poly_power(x, 2)
    x3 = first._poly_multiply(x2, x)
    delayed_linear = first._poly_sub(
        first._poly_scale(
            first._poly_add(delayed_x4, delayed_x5),
            _point(1, precision) / _point(2, precision),
        ),
        x,
    )
    delayed_cubic = first._poly_sub(
        first._poly_scale(
            first._poly_add(
                first._poly_power(delayed_x4, 3),
                first._poly_power(delayed_x5, 3),
            ),
            _point(1, precision) / _point(2, precision),
        ),
        x3,
    )
    fast = first._poly_add(y, first._poly_scale(x2, -_point(1, precision)))
    fast = first._poly_add(
        fast, first._poly_scale(x3, -rho / _point(3, precision))
    )
    fast = first._poly_add(
        fast, first._poly_scale(delayed_linear, rho / _point(5, precision))
    )
    fast = first._poly_add(
        fast, first._poly_scale(delayed_cubic, rho**3 / _point(4, precision))
    )
    slow = first._poly_add_constant(
        first._poly_scale(x, -_point(1, precision)), rho * nu
    )
    return fast, slow


def _variation_rhs_from_slots(
    family_state: PolynomialVector,
    variation: PolynomialVector,
    delayed_x4: IntervalPolynomial,
    delayed_v4: IntervalPolynomial,
    delayed_x5: IntervalPolynomial,
    delayed_v5: IntervalPolynomial,
) -> PolynomialVector:
    precision = family_state[0][0].precision
    rho = _point(5, precision).sqrt() / _point(5, precision)
    x = family_state[0]
    vx, vy = variation
    x2 = first._poly_power(x, 2)
    current = first._poly_scale(x, -_point(2, precision))
    current = first._poly_add(current, first._poly_scale(x2, -rho))
    current = first._poly_add_constant(current, -rho / _point(5, precision))
    current = first._poly_add(
        current,
        first._poly_scale(
            x2, -_point(3, precision) * rho**3 / _point(4, precision)
        ),
    )

    def delayed_coefficient(delayed_x: IntervalPolynomial) -> IntervalPolynomial:
        return first._poly_add_constant(
            first._poly_scale(
                first._poly_power(delayed_x, 2),
                _point(3, precision) * rho**3 / _point(8, precision),
            ),
            rho / _point(10, precision),
        )

    fast = first._poly_add(first._poly_multiply(current, vx), vy)
    fast = first._poly_add(
        fast,
        first._poly_multiply(delayed_coefficient(delayed_x4), delayed_v4),
    )
    fast = first._poly_add(
        fast,
        first._poly_multiply(delayed_coefficient(delayed_x5), delayed_v5),
    )
    return fast, first._poly_scale(vx, -_point(1, precision))


def _second_variation_rhs_from_slots(
    family_state: PolynomialVector,
    family_variation: PolynomialVector,
    second_variation: PolynomialVector,
    delayed_x4: IntervalPolynomial,
    delayed_v4: IntervalPolynomial,
    delayed_w4: IntervalPolynomial,
    delayed_x5: IntervalPolynomial,
    delayed_v5: IntervalPolynomial,
    delayed_w5: IntervalPolynomial,
) -> PolynomialVector:
    precision = family_state[0][0].precision
    rho = _point(5, precision).sqrt() / _point(5, precision)
    x = family_state[0]
    vx = family_variation[0]
    wx, wy = second_variation
    x2 = first._poly_power(x, 2)
    current = first._poly_scale(x, -_point(2, precision))
    current = first._poly_add(current, first._poly_scale(x2, -rho))
    current = first._poly_add_constant(current, -rho / _point(5, precision))
    current = first._poly_add(
        current,
        first._poly_scale(
            x2, -_point(3, precision) * rho**3 / _point(4, precision)
        ),
    )
    current_second = first._poly_add_constant(
        first._poly_scale(
            x,
            -_point(2, precision) * rho
            - _point(3, precision) * rho**3 / _point(2, precision),
        ),
        -_point(2, precision),
    )

    def delayed_terms(
        delayed_x: IntervalPolynomial,
        delayed_v: IntervalPolynomial,
        delayed_w: IntervalPolynomial,
    ) -> IntervalPolynomial:
        first_derivative = first._poly_add_constant(
            first._poly_scale(
                first._poly_power(delayed_x, 2),
                _point(3, precision) * rho**3 / _point(8, precision),
            ),
            rho / _point(10, precision),
        )
        second_derivative = first._poly_scale(
            delayed_x, _point(3, precision) * rho**3 / _point(4, precision)
        )
        return first._poly_add(
            first._poly_multiply(first_derivative, delayed_w),
            first._poly_multiply(
                second_derivative, first._poly_power(delayed_v, 2)
            ),
        )

    fast = first._poly_add(first._poly_multiply(current, wx), wy)
    fast = first._poly_add(
        fast,
        first._poly_multiply(current_second, first._poly_power(vx, 2)),
    )
    fast = first._poly_add(fast, delayed_terms(delayed_x4, delayed_v4, delayed_w4))
    fast = first._poly_add(fast, delayed_terms(delayed_x5, delayed_v5, delayed_w5))
    return fast, first._poly_scale(wx, -_point(1, precision))


def _incoming_history_x_label_jets_polynomial(
    time_left: DirectedInterval,
    step: DirectedInterval,
    label: DirectedInterval,
    delay: int,
) -> tuple[IntervalPolynomial, IntervalPolynomial, IntervalPolynomial]:
    """Return exact incoming-history X, X_lambda and X_lambdalambda."""

    if delay != 5:
        raise ValueError("only the second-step incoming delay-five slot is supported")
    precision = step.precision
    time: IntervalPolynomial = (time_left, step)
    phase = _point("-0.061579261574946566", precision)
    base = first._poly_scale(
        first._poly_add_constant(time, -_point(delay, precision) + phase),
        -_point(1, precision) / _point(2, precision),
    )
    variation: IntervalPolynomial = (_point(0, precision),)
    second: IntervalPolynomial = (_point(0, precision),)
    patch_entry = _point(DELAY_FIVE_PATCH_ENTRY_TIME, precision)
    if time_left.upper < patch_entry.lower:
        return base, variation, second
    if time_left.lower < patch_entry.lower:
        raise ValueError("the grid crossed the delay-five C4 patch entry")
    if time_left.lower >= _point(DELAY_FIVE_PHYSICAL_ENTRY_TIME, precision).lower:
        raise ValueError("incoming history was queried after the physical seam")
    relative = first._poly_add_constant(time, -_point(2, precision))
    coefficients = first._patch_x_coefficients(precision)
    for order in range(1, 5):
        shape = first._patch_shape_polynomial(relative, order)
        base = first._poly_add(
            base,
            first._poly_scale(shape, first._polynomial(coefficients[order], label)),
        )
        variation = first._poly_add(
            variation,
            first._poly_scale(
                shape, first._polynomial_derivative(coefficients[order], label)
            ),
        )
        derivative_coefficients = tuple(
            _point(index, precision) * coefficients[order][index]
            for index in range(1, len(coefficients[order]))
        )
        second = first._poly_add(
            second,
            first._poly_scale(
                shape,
                first._polynomial_derivative(derivative_coefficients, label),
            ),
        )
    return base, variation, second


@dataclass(frozen=True)
class _RetainedCell:
    central_state: PolynomialVector
    central_variation: PolynomialVector
    full_second_variation: PolynomialVector


def _restrict_cell_to_half(cell: _RetainedCell, half: int) -> _RetainedCell:
    return _RetainedCell(
        tuple(
            _restrict_polynomial_to_half(value, half)
            for value in cell.central_state
        ),
        tuple(
            _restrict_polynomial_to_half(value, half)
            for value in cell.central_variation
        ),
        tuple(
            _restrict_polynomial_to_half(value, half)
            for value in cell.full_second_variation
        ),
    )


@dataclass(frozen=True)
class _RetainedFirstStep:
    cells: tuple[_RetainedCell, ...]
    endpoint_state: IntervalVector
    endpoint_variation: IntervalVector
    endpoint_second_variation: IntervalVector
    minimum_picard_gap: gmpy2.mpfr
    maximum_late_x_upper: gmpy2.mpfr


def _reconstruct_family(
    cell: _RetainedCell,
    delta_label: DirectedInterval,
) -> tuple[PolynomialVector, PolynomialVector]:
    variation = tuple(
        first._poly_add(center, first._poly_scale(second, delta_label))
        for center, second in zip(
            cell.central_variation, cell.full_second_variation, strict=True
        )
    )
    state = tuple(
        first._poly_add(center, first._poly_scale(derivative, delta_label))
        for center, derivative in zip(cell.central_state, variation, strict=True)
    )
    return state, variation


def _retain_first_step(
    label_index: int,
    precision: int,
    label: DirectedInterval,
    label_center: DirectedInterval,
    delta_label: DirectedInterval,
) -> _RetainedFirstStep:
    """Replay and retain the source-bound first-step Picard polynomials."""

    guide = first._guide(label_index)
    step = _point(FIRST_STEP_TIME_STEP, precision)
    elapsed = _closed(0, FIRST_STEP_TIME_STEP, precision)
    initial_state = _entry_initial_box(label_center)[:2]
    initial_variation = (_point(0, precision), _point(1, precision))
    initial_second = (_point(0, precision), _point(0, precision))
    cells: list[_RetainedCell] = []
    minimum_gap = gmpy2.mpfr("inf")
    maximum_late_x = gmpy2.mpfr("-inf")

    for time_index in range(400):
        left = _point(first._time_node(time_index), precision)
        right = _point(first._time_node(time_index + 1), precision)
        guide_start = tuple(_float_point(value, precision) for value in guide[time_index])
        guide_end = tuple(
            _float_point(value, precision) for value in guide[time_index + 1]
        )
        state_start, state_end = guide_start[:2], guide_end[:2]
        variation_start, variation_end = guide_start[2:4], guide_end[2:4]
        second_start, second_end = guide_start[4:6], guide_end[4:6]
        state_predictor, state_predictor_t = first._hermite_polynomials(
            state_start,
            state_end,
            first._state_rhs(left, state_start, label_center),
            first._state_rhs(right, state_end, label_center),
            step,
        )
        central = first._polynomial_picard_error_step(
            initial=initial_state,
            guide_start=state_start,
            guide_end=state_end,
            predictor=state_predictor,
            predictor_derivative=state_predictor_t,
            elapsed=elapsed,
            step=step,
            residual_polynomial_field=lambda tube, left=left: first._state_rhs_polynomial(
                left, step, tube, label_center
            ),
        )
        variation_predictor, variation_predictor_t = first._hermite_polynomials(
            variation_start,
            variation_end,
            first._variation_rhs(left, state_start, variation_start, label_center),
            first._variation_rhs(right, state_end, variation_end, label_center),
            step,
        )
        variation = first._polynomial_picard_error_step(
            initial=initial_variation,
            guide_start=variation_start,
            guide_end=variation_end,
            predictor=variation_predictor,
            predictor_derivative=variation_predictor_t,
            elapsed=elapsed,
            step=step,
            residual_polynomial_field=lambda tube, left=left, central=central: first._variation_rhs_polynomial(
                left, step, central.tube, tube, label_center
            ),
        )
        second_rhs_start = first._second_variation_rhs_polynomial(
            left,
            _point(0, precision),
            tuple(_poly_constant(value) for value in state_start),
            tuple(_poly_constant(value) for value in variation_start),
            tuple(_poly_constant(value) for value in second_start),
            label_center,
        )
        second_rhs_end = first._second_variation_rhs_polynomial(
            right,
            _point(0, precision),
            tuple(_poly_constant(value) for value in state_end),
            tuple(_poly_constant(value) for value in variation_end),
            tuple(_poly_constant(value) for value in second_end),
            label_center,
        )
        second_predictor, second_predictor_t = first._hermite_polynomials(
            second_start,
            second_end,
            first._poly_vector_range(second_rhs_start),
            first._poly_vector_range(second_rhs_end),
            step,
        )

        def second_field(second_tube: PolynomialVector) -> PolynomialVector:
            family_variation = tuple(
                first._poly_add(center, first._poly_scale(second, delta_label))
                for center, second in zip(
                    variation.tube, second_tube, strict=True
                )
            )
            family_state = tuple(
                first._poly_add(center, first._poly_scale(derivative, delta_label))
                for center, derivative in zip(
                    central.tube, family_variation, strict=True
                )
            )
            return first._second_variation_rhs_polynomial(
                left,
                step,
                family_state,
                family_variation,
                second_tube,
                label,
            )

        second = first._polynomial_picard_error_step(
            initial=initial_second,
            guide_start=second_start,
            guide_end=second_end,
            predictor=second_predictor,
            predictor_derivative=second_predictor_t,
            elapsed=elapsed,
            step=step,
            residual_polynomial_field=second_field,
        )
        retained = _RetainedCell(central.tube, variation.tube, second.tube)
        cells.append(retained)
        minimum_gap = min(
            minimum_gap,
            central.minimum_gap,
            variation.minimum_gap,
            second.minimum_gap,
        )
        if time_index >= 100:
            family_state, _ = _reconstruct_family(retained, delta_label)
            maximum_late_x = max(
                maximum_late_x,
                first._poly_bernstein_range(family_state[0]).upper,
            )
        initial_state = central.endpoint
        initial_variation = variation.endpoint
        initial_second = second.endpoint

    return _RetainedFirstStep(
        cells=tuple(cells),
        endpoint_state=initial_state,
        endpoint_variation=initial_variation,
        endpoint_second_variation=initial_second,
        minimum_picard_gap=minimum_gap,
        maximum_late_x_upper=maximum_late_x,
    )


@lru_cache(maxsize=32)
def _float_first_guide_derivatives(label_index: int) -> tuple[FloatVector, ...]:
    label = (float(_label_node(label_index)) + float(_label_node(label_index + 1))) / 2.0
    return tuple(
        first._float_coupled_rhs(-3.0 + index * 0.01, state, label)
        for index, state in enumerate(first._guide(label_index))
    )


def _float_first_guide_value(time: float, label_index: int) -> FloatVector:
    """Cubic interpolation used only for the nonclaim second-step guide."""

    if time < -3.0 - 1e-12 or time > -1.0 + 1e-12:
        raise ValueError("the second-step guide queried the wrong first-step range")
    scaled = min(max((time + 3.0) / 0.01, 0.0), 200.0)
    nearest = round(scaled)
    guide = first._guide(label_index)
    if abs(scaled - nearest) <= 2e-12:
        return guide[int(nearest)]
    index = min(int(math.floor(scaled)), 199)
    u = scaled - index
    left = guide[index]
    right = guide[index + 1]
    derivatives = _float_first_guide_derivatives(label_index)
    left_d = derivatives[index]
    right_d = derivatives[index + 1]
    h00 = 2.0 * u**3 - 3.0 * u**2 + 1.0
    h10 = u**3 - 2.0 * u**2 + u
    h01 = -2.0 * u**3 + 3.0 * u**2
    h11 = u**3 - u**2
    return tuple(
        h00 * z0 + 0.01 * h10 * d0 + h01 * z1 + 0.01 * h11 * d1
        for z0, z1, d0, d1 in zip(left, right, left_d, right_d, strict=True)
    )


def _float_incoming_history_x_jets(time: float, label: float) -> tuple[float, float, float]:
    value = c4_prepared_history_state(time, label)[0]
    variation = c4_prepared_history_transverse_derivative(time, label)[0]
    second = 0.0
    relative = time + 3.0
    if relative > -0.5:
        for order in range(1, 5):
            coefficients = first._float_patch_x_coefficients()[order]
            polynomial_second = sum(
                index * (index - 1) * coefficients[index] * label ** (index - 2)
                for index in range(2, len(coefficients))
            )
            second += polynomial_second * right_jet_shape(relative, order)
    return float(value), float(variation), float(second)


def _float_delayed_x_jets(
    time: float, delay: int, label: float, label_index: int
) -> tuple[float, float, float]:
    source_time = time - float(delay)
    if source_time <= -3.0 + 2e-13:
        return _float_incoming_history_x_jets(min(source_time, -3.0), label)
    value = _float_first_guide_value(source_time, label_index)
    return value[0], value[2], value[4]


def _float_second_rhs(
    time: float, state: FloatVector, label: float, label_index: int
) -> FloatVector:
    x, y, vx, vy, wx, wy = state
    rho = math.sqrt(5.0) / 5.0
    nu = 0.21256022233963731
    x4, vx4, wx4 = _float_delayed_x_jets(time, 4, label, label_index)
    x5, vx5, wx5 = _float_delayed_x_jets(time, 5, label, label_index)
    fast = (
        y
        - x * x
        - rho * x**3 / 3.0
        + rho / 5.0 * ((x4 + x5) / 2.0 - x)
        + rho**3 / 4.0 * ((x4**3 + x5**3) / 2.0 - x**3)
    )
    slow = -x + rho * nu
    current = -2.0 * x - rho * x * x - rho / 5.0 - 0.75 * rho**3 * x * x
    delayed4 = rho / 10.0 + 3.0 * rho**3 * x4 * x4 / 8.0
    delayed5 = rho / 10.0 + 3.0 * rho**3 * x5 * x5 / 8.0
    current_second = -2.0 - 2.0 * rho * x - 1.5 * rho**3 * x
    delayed4_second = 0.75 * rho**3 * x4
    delayed5_second = 0.75 * rho**3 * x5
    return (
        fast,
        slow,
        current * vx + vy + delayed4 * vx4 + delayed5 * vx5,
        -vx,
        current * wx
        + wy
        + current_second * vx * vx
        + delayed4 * wx4
        + delayed4_second * vx4 * vx4
        + delayed5 * wx5
        + delayed5_second * vx5 * vx5,
        -wx,
    )


def _float_rk4_second(
    time: float, state: FloatVector, label: float, label_index: int, step: float
) -> FloatVector:
    k1 = _float_second_rhs(time, state, label, label_index)
    k2_state = tuple(a + step * b / 2.0 for a, b in zip(state, k1, strict=True))
    k2 = _float_second_rhs(time + step / 2.0, k2_state, label, label_index)
    k3_state = tuple(a + step * b / 2.0 for a, b in zip(state, k2, strict=True))
    k3 = _float_second_rhs(time + step / 2.0, k3_state, label, label_index)
    k4_state = tuple(a + step * b for a, b in zip(state, k3, strict=True))
    k4 = _float_second_rhs(time + step, k4_state, label, label_index)
    return tuple(
        value + step * (a + 2.0 * b + 2.0 * c + d) / 6.0
        for value, a, b, c, d in zip(state, k1, k2, k3, k4, strict=True)
    )


@lru_cache(maxsize=32)
def _second_guide(label_index: int) -> tuple[FloatVector, ...]:
    label = (float(_label_node(label_index)) + float(_label_node(label_index + 1))) / 2.0
    state = first._guide(label_index)[-1]
    rows = [state]
    for index in range(400):
        state = _float_rk4_second(
            1.0 + index * 0.005, state, label, label_index, 0.005
        )
        if not all(math.isfinite(value) for value in state):
            raise RuntimeError("the nonrigorous second-step guide became nonfinite")
        rows.append(state)
    return tuple(rows)


def _delayed_cell(
    retained: _RetainedFirstStep,
    time_index: int,
    delay: int,
    time_left: DirectedInterval,
    step: DirectedInterval,
    label: DirectedInterval,
    label_center: DirectedInterval,
) -> _RetainedCell:
    if delay == 4:
        return _restrict_cell_to_half(
            retained.cells[time_index // 2], time_index % 2
        )
    if delay != 5:
        raise ValueError("only delays four and five are active")
    if time_index < 200:
        x, v, _ = _incoming_history_x_label_jets_polynomial(
            time_left, step, label_center, 5
        )
        _, _, w = _incoming_history_x_label_jets_polynomial(
            time_left, step, label, 5
        )
        zero = (_point(0, step.precision),)
        return _RetainedCell((x, zero), (v, zero), (w, zero))
    source_index = time_index - 200
    return _restrict_cell_to_half(
        retained.cells[source_index // 2], source_index % 2
    )


def _slot_families(
    delayed: _RetainedCell,
    delta_label: DirectedInterval,
) -> tuple[IntervalPolynomial, IntervalPolynomial, IntervalPolynomial]:
    state, variation = _reconstruct_family(delayed, delta_label)
    return state[0], variation[0], delayed.full_second_variation[0]


def _midpoint_polynomial(value: IntervalPolynomial) -> IntervalPolynomial:
    """Choose binary64 coefficient centers for a nonclaim predictor."""

    precision = value[0].precision
    return tuple(
        _float_point(float((coefficient.lower + coefficient.upper) / 2), precision)
        for coefficient in value
    )


def _coupled_taylor_predictor(
    guide_start: IntervalVector,
    step: DirectedInterval,
    delayed4: _RetainedCell,
    delayed5: _RetainedCell,
    degree: int = 8,
) -> tuple[PolynomialVector, PolynomialVector, IntervalVector]:
    """Build a high-order local center; all proof error stays in Picard."""

    if len(guide_start) != 6 or degree < 2:
        raise ValueError("the coupled Taylor predictor data changed")
    x4 = _midpoint_polynomial(delayed4.central_state[0])
    v4 = _midpoint_polynomial(delayed4.central_variation[0])
    w4 = _midpoint_polynomial(delayed4.full_second_variation[0])
    x5 = _midpoint_polynomial(delayed5.central_state[0])
    v5 = _midpoint_polynomial(delayed5.central_variation[0])
    w5 = _midpoint_polynomial(delayed5.full_second_variation[0])
    coefficients: list[list[DirectedInterval]] = [[value] for value in guide_start]
    for order in range(1, degree + 1):
        current: PolynomialVector = tuple(tuple(row) for row in coefficients)
        state = current[:2]
        variation = current[2:4]
        second = current[4:6]
        rhs = (
            *_state_rhs_from_slots(state, x4, x5),
            *_variation_rhs_from_slots(state, variation, x4, v4, x5, v5),
            *_second_variation_rhs_from_slots(
                state, variation, second, x4, v4, w4, x5, v5, w5
            ),
        )
        for row, component in zip(coefficients, rhs, strict=True):
            coefficient = (
                component[order - 1]
                if order - 1 < len(component)
                else _point(0, step.precision)
            )
            coefficient = step * coefficient / _point(order, step.precision)
            row.append(
                _float_point(
                    float((coefficient.lower + coefficient.upper) / 2),
                    step.precision,
                )
            )
    predictor: PolynomialVector = tuple(tuple(row) for row in coefficients)
    derivative = tuple(first._poly_time_derivative(row, step) for row in predictor)
    one = _point(1, step.precision)
    endpoint = tuple(first._polynomial(row, one) for row in predictor)
    return predictor, derivative, endpoint


def _euclidean_radius(
    box: Sequence[DirectedInterval], center: Sequence[DirectedInterval]
) -> gmpy2.mpfr:
    if len(box) != len(center):
        raise ValueError("the ball box and center dimensions differ")
    precision = box[0].precision
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        squared = gmpy2.mpfr(0)
        for value, midpoint in zip(box, center, strict=True):
            difference = value - midpoint
            radius = difference.upper_abs()
            squared += radius * radius
        return gmpy2.sqrt(squared)


def _center_distance(
    left: Sequence[DirectedInterval], right: Sequence[DirectedInterval]
) -> gmpy2.mpfr:
    return _euclidean_radius(left, right)


def _vector_range_norm(value: Sequence[DirectedInterval]) -> gmpy2.mpfr:
    precision = value[0].precision
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        squared = gmpy2.mpfr(0)
        for component in value:
            radius = component.upper_abs()
            squared += radius * radius
        return gmpy2.sqrt(squared)


def _symmetric_ball_box(radius: gmpy2.mpfr, precision: int) -> DirectedInterval:
    # Raw unary MPFR negation inherits the process-wide context (typically
    # 53 bits), so ``from_bounds(-radius, radius, precision)`` can round the
    # negative endpoint inward before the declared-precision constructor sees
    # it.  Form both endpoints under the proof precision and the appropriate
    # directed modes instead.
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        lower = -radius
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        upper = gmpy2.mpfr(radius)
    return DirectedInterval(lower, upper, precision)


@dataclass(frozen=True)
class _PolynomialBallPicardStep:
    tube: PolynomialVector
    endpoint: IntervalVector
    endpoint_center: IntervalVector
    endpoint_radius: gmpy2.mpfr
    minimum_gap: gmpy2.mpfr
    maximum_error_radius: gmpy2.mpfr


def _polynomial_ball_picard_error_step(
    *,
    initial_center: IntervalVector,
    initial_radius: gmpy2.mpfr,
    predictor: PolynomialVector,
    predictor_derivative: PolynomialVector,
    step: DirectedInterval,
    residual_polynomial_field: Any,
) -> _PolynomialBallPicardStep:
    """Validate a cell in a Euclidean error ball without reboxing it."""

    precision = step.precision
    predictor_start = tuple(component[0] for component in predictor)
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        starting_radius = initial_radius + _center_distance(
            initial_center, predictor_start
        )
        radius = (
            max(starting_radius, gmpy2.mpfr("1e-55"))
            * gmpy2.mpfr("1.03125")
            + gmpy2.mpfr("1e-55")
        )
    for _ in range(60):
        error = _symmetric_ball_box(radius, precision)
        tube = tuple(
            first._poly_add_constant(component, error)
            for component in predictor
        )
        field = residual_polynomial_field(tube)
        residual_polynomial = tuple(
            first._poly_sub(component, derivative)
            for component, derivative in zip(
                field, predictor_derivative, strict=True
            )
        )
        residual = first._poly_vector_range(residual_polynomial)
        residual_norm = _vector_range_norm(residual)
        with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
            image_radius = starting_radius + step.upper * residual_norm
        with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
            gap = radius - image_radius
        if gap > 0:
            endpoint_center = tuple(
                first._polynomial(component, _point(1, precision))
                for component in predictor
            )
            endpoint_error = _symmetric_ball_box(image_radius, precision)
            endpoint = tuple(
                center + endpoint_error for center in endpoint_center
            )
            return _PolynomialBallPicardStep(
                tube=tube,
                endpoint=endpoint,
                endpoint_center=endpoint_center,
                endpoint_radius=image_radius,
                minimum_gap=gap,
                maximum_error_radius=radius,
            )
        with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
            radius = (
                max(radius, image_radius) * gmpy2.mpfr("1.03125")
                + gmpy2.mpfr("1e-55")
            )
    raise RuntimeError("the Euclidean-ball polynomial Picard iteration did not close")


def _current_log_norm_upper(state_tube: PolynomialVector) -> gmpy2.mpfr:
    """Upper bound for mu_2([[F_X,1],[-1,0]]) on a state tube."""

    precision = state_tube[0][0].precision
    rho = _point(5, precision).sqrt() / _point(5, precision)
    x = state_tube[0]
    x2 = first._poly_power(x, 2)
    coefficient = first._poly_scale(x, -_point(2, precision))
    coefficient = first._poly_add(coefficient, first._poly_scale(x2, -rho))
    coefficient = first._poly_add_constant(
        coefficient, -rho / _point(5, precision)
    )
    coefficient = first._poly_add(
        coefficient,
        first._poly_scale(
            x2, -_point(3, precision) * rho**3 / _point(4, precision)
        ),
    )
    upper = first._poly_bernstein_range(coefficient).upper
    return max(gmpy2.mpfr(0), upper)


def _gronwall_radius(
    initial_radius: gmpy2.mpfr,
    defect_norm: gmpy2.mpfr,
    log_norm: gmpy2.mpfr,
    elapsed: gmpy2.mpfr,
    precision: int,
) -> gmpy2.mpfr:
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        if log_norm == 0:
            return initial_radius + elapsed * defect_norm
        exponential = gmpy2.exp(log_norm * elapsed)
        return exponential * initial_radius + (
            (exponential - 1) / log_norm
        ) * defect_norm


def _polynomial_log_norm_error_step(
    *,
    initial_center: IntervalVector,
    initial_radius: gmpy2.mpfr,
    predictor: PolynomialVector,
    predictor_derivative: PolynomialVector,
    step: DirectedInterval,
    defect_polynomial_field: Any | None,
    coefficient_state_tube: PolynomialVector | None = None,
    tube_dependent_data: Any | None = None,
) -> _PolynomialBallPicardStep:
    """Validate an error ball by the exact two-dimensional log norm."""

    precision = step.precision
    predictor_start = tuple(component[0] for component in predictor)
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        starting_radius = initial_radius + _center_distance(
            initial_center, predictor_start
        )
        radius = (
            max(starting_radius, gmpy2.mpfr("1e-55"))
            * gmpy2.mpfr("1.03125")
            + gmpy2.mpfr("1e-55")
        )
    if (defect_polynomial_field is None) == (tube_dependent_data is None):
        raise ValueError("exactly one log-norm defect provider is required")
    for _ in range(60):
        error = _symmetric_ball_box(radius, precision)
        tube = tuple(
            first._poly_add_constant(component, error)
            for component in predictor
        )
        if tube_dependent_data is None:
            field_at_predictor = defect_polynomial_field(predictor)
            coefficient_tube = (
                tube if coefficient_state_tube is None else coefficient_state_tube
            )
        else:
            field_at_predictor, coefficient_tube = tube_dependent_data(
                tube, predictor
            )
        defect_polynomial = tuple(
            first._poly_sub(component, derivative)
            for component, derivative in zip(
                field_at_predictor, predictor_derivative, strict=True
            )
        )
        defect = first._poly_vector_range(defect_polynomial)
        defect_norm = _vector_range_norm(defect)
        log_norm = _current_log_norm_upper(coefficient_tube)
        image_radius = _gronwall_radius(
            starting_radius,
            defect_norm,
            log_norm,
            step.upper,
            precision,
        )
        with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
            gap = radius - image_radius
        if gap > 0:
            endpoint_center = tuple(
                first._polynomial(component, _point(1, precision))
                for component in predictor
            )
            endpoint_error = _symmetric_ball_box(image_radius, precision)
            endpoint = tuple(
                center + endpoint_error for center in endpoint_center
            )
            return _PolynomialBallPicardStep(
                tube=tube,
                endpoint=endpoint,
                endpoint_center=endpoint_center,
                endpoint_radius=image_radius,
                minimum_gap=gap,
                maximum_error_radius=radius,
            )
        with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
            radius = (
                max(radius, image_radius) * gmpy2.mpfr("1.03125")
                + gmpy2.mpfr("1e-55")
            )
    raise RuntimeError("the logarithmic-norm polynomial enclosure did not close")


def _constant_rhs_from_float_guide(
    time: float,
    guide_state: Sequence[DirectedInterval],
    label_float: float,
    label_index: int,
    which: str,
) -> IntervalVector:
    precision = guide_state[0].precision
    delayed4 = _float_delayed_x_jets(time, 4, label_float, label_index)
    delayed5 = _float_delayed_x_jets(time, 5, label_float, label_index)
    x4, v4, w4 = tuple(_poly_constant(_float_point(value, precision)) for value in delayed4)
    x5, v5, w5 = tuple(_poly_constant(_float_point(value, precision)) for value in delayed5)
    state = tuple(_poly_constant(value) for value in guide_state[:2])
    variation = tuple(_poly_constant(value) for value in guide_state[2:4])
    second = tuple(_poly_constant(value) for value in guide_state[4:6])
    if which == "state":
        result = _state_rhs_from_slots(state, x4, x5)
    elif which == "variation":
        result = _variation_rhs_from_slots(state, variation, x4, v4, x5, v5)
    elif which == "second":
        result = _second_variation_rhs_from_slots(
            state, variation, second, x4, v4, w4, x5, v5, w5
        )
    else:
        raise ValueError("unknown guide derivative kind")
    return first._poly_vector_range(result)


@lru_cache(maxsize=1)
def exact_second_step_cover_defects() -> tuple[sp.Expr, ...]:
    """Audit slot derivatives, source partitions, frame, and MVT algebra."""

    x, y, x4, x5 = sp.symbols("x y x4 x5", real=True)
    vx, vy, vx4, vx5 = sp.symbols("vx vy vx4 vx5", real=True)
    wx, wy, wx4, wx5 = sp.symbols("wx wy wx4 wx5", real=True)
    rho = sp.sqrt(5) / 5
    nu = sp.Rational("0.21256022233963731")
    fast = (
        y
        - x**2
        - rho * x**3 / 3
        + rho / 5 * ((x4 + x5) / 2 - x)
        + rho**3 / 4 * ((x4**3 + x5**3) / 2 - x**3)
    )
    slow = -x + rho * nu
    variables = (x, y, x4, x5)
    v = (vx, vy, vx4, vx5)
    w = (wx, wy, wx4, wx5)
    first_exact = sum(sp.diff(fast, variable) * jet for variable, jet in zip(variables, v, strict=True))
    second_exact = sum(sp.diff(fast, variable) * jet for variable, jet in zip(variables, w, strict=True)) + sum(
        sp.diff(fast, left, right) * left_jet * right_jet
        for left, left_jet in zip(variables, v, strict=True)
        for right, right_jet in zip(variables, v, strict=True)
    )
    current = -2 * x - rho * x**2 - rho / 5 - 3 * rho**3 * x**2 / 4
    implemented_first = (
        current * vx
        + vy
        + (rho / 10 + 3 * rho**3 * x4**2 / 8) * vx4
        + (rho / 10 + 3 * rho**3 * x5**2 / 8) * vx5
    )
    implemented_second = (
        current * wx
        + wy
        + (-2 - 2 * rho * x - 3 * rho**3 * x / 2) * vx**2
        + (rho / 10 + 3 * rho**3 * x4**2 / 8) * wx4
        + 3 * rho**3 * x4 * vx4**2 / 4
        + (rho / 10 + 3 * rho**3 * x5**2 / 8) * wx5
        + 3 * rho**3 * x5 * vx5**2 / 4
    )
    t = sp.symbols("t", real=True)
    frame = sp.Matrix(((-7, 2), (3, 1)))
    linearization = sp.Matrix(((current, 1), (-1, 0)))
    symmetric_defect = (
        (linearization + linearization.T) / 2
        - sp.diag(current, 0)
    )
    mu, radius0, defect_size, elapsed = sp.symbols(
        "mu radius0 defect_size elapsed", positive=True
    )
    gronwall = (
        sp.exp(mu * elapsed) * radius0
        + (sp.exp(mu * elapsed) - 1) * defect_size / mu
    )
    return tuple(
        sp.simplify(value)
        for value in (
            implemented_first - first_exact,
            implemented_second - second_exact,
            sp.diff(slow, x) + 1,
            (t - 4).subs(t, 1) + 3,
            (t - 4).subs(t, 3) + 1,
            (t - 5).subs(t, 1) + 4,
            (t - 5).subs(t, sp.Rational(3, 2)) + sp.Rational(7, 2),
            (t - 5).subs(t, 2) + 3,
            (t - 5).subs(t, 3) + 2,
            frame.det() + 13,
            *tuple(symmetric_defect),
            gronwall.subs(elapsed, 0) - radius0,
            sp.diff(gronwall, elapsed) - mu * gronwall - defect_size,
        )
    )


@dataclass(frozen=True)
class SecondStepProbe:
    precision_bits: int
    completed_label_cells: int
    completed_second_time_cells: int
    first_failure: tuple[int, int, str, str] | None
    minimum_replayed_first_step_picard_gap: str
    minimum_central_picard_gap: str
    minimum_first_variation_picard_gap: str
    minimum_second_variation_picard_gap: str
    maximum_central_error_radius: str
    maximum_first_variation_error_radius: str
    maximum_second_variation_error_radius: str
    minimum_time_minor: str
    minimum_label_minor: str
    minimum_oriented_determinant: str
    maximum_raw_determinant: str
    maximum_late_physical_x: str
    minimum_late_entry_x_gap: str
    delay_four_previous_solution_cell_count: int
    delay_five_affine_history_cell_count: int
    delay_five_c4_patch_cell_count: int
    delay_five_previous_solution_cell_count: int
    proof_cell_digest_sha256: str


def _lower_text(value: gmpy2.mpfr) -> str:
    return decimal_lower(value, 70)


def _upper_text(value: gmpy2.mpfr) -> str:
    return decimal_upper(value, 70)


def _digest(value: DirectedInterval) -> str:
    lower = decimal_lower(value.lower, 70)
    upper = decimal_upper(value.upper, 70)
    reparsed = DirectedInterval.from_bounds(lower, upper, value.precision)
    if reparsed.lower > value.lower or reparsed.upper < value.upper:
        raise AssertionError("a digest endpoint was not outward serialized")
    return f"{lower},{upper}"


def _digest_polynomial_vector(value: PolynomialVector) -> str:
    return ";".join(
        ",".join(_digest(coefficient) for coefficient in component)
        for component in value
    )


def probe_second_step_cover(
    precision: int = PRIMARY_PRECISION_BITS,
    *,
    label_start_index: int = 0,
    maximum_label_cells: int = 20,
    maximum_second_time_cells: int = 400,
) -> SecondStepProbe:
    """Run the source-bound second-step kernel and return its first failure."""

    if type(precision) is not int or precision < 64:
        raise ValueError("precision must be an integer of at least 64 bits")
    if type(label_start_index) is not int or not 0 <= label_start_index < 20:
        raise ValueError("label_start_index must lie between zero and nineteen")
    if not 1 <= maximum_label_cells <= 20 - label_start_index:
        raise ValueError("the requested label-cell range left the twenty-cell grid")
    if not 1 <= maximum_second_time_cells <= 400:
        raise ValueError("maximum_second_time_cells must lie between one and 400")
    step = _point(TIME_STEP, precision)
    elapsed = _closed(0, TIME_STEP, precision)
    minimum_replayed = gmpy2.mpfr("inf")
    minimum_central = gmpy2.mpfr("inf")
    minimum_variation = gmpy2.mpfr("inf")
    minimum_second = gmpy2.mpfr("inf")
    maximum_central = gmpy2.mpfr(0)
    maximum_variation = gmpy2.mpfr(0)
    maximum_second = gmpy2.mpfr(0)
    minimum_time_minor = gmpy2.mpfr("inf")
    minimum_label_minor = gmpy2.mpfr("inf")
    minimum_oriented = gmpy2.mpfr("inf")
    maximum_raw = gmpy2.mpfr("-inf")
    maximum_late_x = gmpy2.mpfr("-inf")
    minimum_late_gap = gmpy2.mpfr("inf")
    delay4_count = delay5_affine_count = delay5_patch_count = delay5_solution_count = 0
    completed = 0
    failure: tuple[int, int, str, str] | None = None
    digest = sha256()

    for label_index in range(
        label_start_index, label_start_index + maximum_label_cells
    ):
        label = _closed(_label_node(label_index), _label_node(label_index + 1), precision)
        label_float = (float(_label_node(label_index)) + float(_label_node(label_index + 1))) / 2.0
        label_center = _float_point(label_float, precision)
        if label_center.lower < label.lower or label_center.upper > label.upper:
            raise AssertionError("the guide label left its exact decimal cell")
        delta_label = label - label_center
        try:
            retained = _retain_first_step(
                label_index, precision, label, label_center, delta_label
            )
        except (RuntimeError, ValueError) as error:
            failure = (label_index, -1, "first-step dependency", str(error))
            break
        minimum_replayed = min(minimum_replayed, retained.minimum_picard_gap)
        maximum_late_x = max(maximum_late_x, retained.maximum_late_x_upper)
        entry_x = _entry_initial_box(label_center)[0]
        with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
            minimum_late_gap = min(
                minimum_late_gap, entry_x.lower - retained.maximum_late_x_upper
            )
        initial_state = retained.endpoint_state
        initial_variation = retained.endpoint_variation
        initial_second_variation = retained.endpoint_second_variation
        guide = _second_guide(label_index)
        initial_guide = tuple(
            _float_point(value, precision) for value in guide[0]
        )
        initial_state_center = initial_guide[:2]
        initial_variation_center = initial_guide[2:4]
        initial_second_center = initial_guide[4:6]
        initial_state_radius = _euclidean_radius(
            initial_state, initial_state_center
        )
        initial_variation_radius = _euclidean_radius(
            initial_variation, initial_variation_center
        )
        initial_second_radius = _euclidean_radius(
            initial_second_variation, initial_second_center
        )

        for time_index in range(maximum_second_time_cells):
            left_text = _time_node(time_index)
            right_text = _time_node(time_index + 1)
            left = _point(left_text, precision)
            guide_start = tuple(_float_point(value, precision) for value in guide[time_index])
            delayed4 = _delayed_cell(
                retained, time_index, 4, left, step, label, label_center
            )
            delayed5 = _delayed_cell(
                retained, time_index, 5, left, step, label, label_center
            )
            predictor, predictor_t, guide_end = _coupled_taylor_predictor(
                guide_start, step, delayed4, delayed5
            )
            state_start, state_end = guide_start[:2], guide_end[:2]
            variation_start, variation_end = guide_start[2:4], guide_end[2:4]
            second_start, second_end = guide_start[4:6], guide_end[4:6]
            x4_c = delayed4.central_state[0]
            v4_c = delayed4.central_variation[0]
            w4 = delayed4.full_second_variation[0]
            x5_c = delayed5.central_state[0]
            v5_c = delayed5.central_variation[0]
            w5 = delayed5.full_second_variation[0]
            try:
                central = _polynomial_log_norm_error_step(
                    initial_center=initial_state_center,
                    initial_radius=initial_state_radius,
                    predictor=predictor[:2],
                    predictor_derivative=predictor_t[:2],
                    step=step,
                    defect_polynomial_field=lambda tube: _state_rhs_from_slots(
                        tube, x4_c, x5_c
                    ),
                )
                variation = _polynomial_log_norm_error_step(
                    initial_center=initial_variation_center,
                    initial_radius=initial_variation_radius,
                    predictor=predictor[2:4],
                    predictor_derivative=predictor_t[2:4],
                    step=step,
                    defect_polynomial_field=lambda tube: _variation_rhs_from_slots(
                        central.tube, tube, x4_c, v4_c, x5_c, v5_c
                    ),
                    coefficient_state_tube=central.tube,
                )
                def second_data(
                    second_tube: PolynomialVector,
                    predictor_second: PolynomialVector,
                ) -> tuple[PolynomialVector, PolynomialVector]:
                    family_variation = tuple(
                        first._poly_add(center, first._poly_scale(second, delta_label))
                        for center, second in zip(
                            variation.tube, second_tube, strict=True
                        )
                    )
                    family_state = tuple(
                        first._poly_add(center, first._poly_scale(derivative, delta_label))
                        for center, derivative in zip(
                            central.tube, family_variation, strict=True
                        )
                    )
                    x4, v4, full_w4 = _slot_families(delayed4, delta_label)
                    x5, v5, full_w5 = _slot_families(delayed5, delta_label)
                    field = _second_variation_rhs_from_slots(
                        family_state,
                        family_variation,
                        predictor_second,
                        x4,
                        v4,
                        full_w4,
                        x5,
                        v5,
                        full_w5,
                    )
                    return field, family_state

                second = _polynomial_log_norm_error_step(
                    initial_center=initial_second_center,
                    initial_radius=initial_second_radius,
                    predictor=predictor[4:6],
                    predictor_derivative=predictor_t[4:6],
                    step=step,
                    defect_polynomial_field=None,
                    tube_dependent_data=second_data,
                )
            except (RuntimeError, ValueError) as error:
                failure = (label_index, time_index, "second-step Picard", str(error))
                break

            cell = _RetainedCell(central.tube, variation.tube, second.tube)
            family_state, family_variation = _reconstruct_family(cell, delta_label)
            x4, _, _ = _slot_families(delayed4, delta_label)
            x5, _, _ = _slot_families(delayed5, delta_label)
            fast, slow = _state_rhs_from_slots(family_state, x4, x5)
            vx, vy = family_variation
            time_minor = first._poly_add(
                first._poly_scale(fast, -_point(7, precision)),
                first._poly_scale(slow, _point(2, precision)),
            )
            label_minor = first._poly_add(
                first._poly_scale(vx, _point(3, precision)), vy
            )
            raw = first._poly_sub(
                first._poly_multiply(fast, vy),
                first._poly_multiply(slow, vx),
            )
            oriented = first._poly_scale(raw, -_point(13, precision))
            time_range = first._poly_bernstein_range(time_minor)
            label_range = first._poly_bernstein_range(label_minor)
            raw_range = first._poly_bernstein_range(raw)
            oriented_range = first._poly_bernstein_range(oriented)
            state_x_range = first._poly_bernstein_range(family_state[0])
            with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
                late_gap = entry_x.lower - state_x_range.upper
            if (
                time_range.lower <= 0
                or label_range.lower <= 0
                or oriented_range.lower <= 0
                or raw_range.upper >= 0
            ):
                failure = (
                    label_index,
                    time_index,
                    "P-matrix",
                    "time=["
                    + _lower_text(time_range.lower)
                    + ","
                    + _upper_text(time_range.upper)
                    + "], label=["
                    + _lower_text(label_range.lower)
                    + ","
                    + _upper_text(label_range.upper)
                    + "], oriented=["
                    + _lower_text(oriented_range.lower)
                    + ","
                    + _upper_text(oriented_range.upper)
                    + "], raw=["
                    + _lower_text(raw_range.lower)
                    + ","
                    + _upper_text(raw_range.upper)
                    + "]",
                )
                break
            if late_gap <= 0:
                failure = (label_index, time_index, "late cross-separation", "X_entry-X crossed zero")
                break
            minimum_central = min(minimum_central, central.minimum_gap)
            minimum_variation = min(minimum_variation, variation.minimum_gap)
            minimum_second = min(minimum_second, second.minimum_gap)
            maximum_central = max(maximum_central, central.maximum_error_radius)
            maximum_variation = max(maximum_variation, variation.maximum_error_radius)
            maximum_second = max(maximum_second, second.maximum_error_radius)
            minimum_time_minor = min(minimum_time_minor, time_range.lower)
            minimum_label_minor = min(minimum_label_minor, label_range.lower)
            minimum_oriented = min(minimum_oriented, oriented_range.lower)
            maximum_raw = max(maximum_raw, raw_range.upper)
            maximum_late_x = max(maximum_late_x, state_x_range.upper)
            minimum_late_gap = min(minimum_late_gap, late_gap)
            delay4_count += 1
            if time_index < 100:
                delay5_affine_count += 1
            elif time_index < 200:
                delay5_patch_count += 1
            else:
                delay5_solution_count += 1
            digest.update(
                (
                    f"{label_index}:{time_index}|"
                    + _digest_polynomial_vector(central.tube)
                    + "|"
                    + _digest_polynomial_vector(variation.tube)
                    + "|"
                    + _digest_polynomial_vector(second.tube)
                    + "|"
                    + _digest_polynomial_vector((x4_c, v4_c, w4, x5_c, v5_c, w5))
                    + "|"
                    + ";".join(
                        _digest(value)
                        for value in (
                            time_range,
                            label_range,
                            oriented_range,
                            raw_range,
                            state_x_range,
                        )
                    )
                    + "\n"
                ).encode("ascii")
            )
            initial_state = central.endpoint
            initial_variation = variation.endpoint
            initial_second_variation = second.endpoint
            initial_state_center = central.endpoint_center
            initial_variation_center = variation.endpoint_center
            initial_second_center = second.endpoint_center
            initial_state_radius = central.endpoint_radius
            initial_variation_radius = variation.endpoint_radius
            initial_second_radius = second.endpoint_radius
            completed += 1
        if failure is not None:
            break

    return SecondStepProbe(
        precision_bits=precision,
        completed_label_cells=completed // maximum_second_time_cells,
        completed_second_time_cells=completed,
        first_failure=failure,
        minimum_replayed_first_step_picard_gap=_lower_text(minimum_replayed),
        minimum_central_picard_gap=_lower_text(minimum_central),
        minimum_first_variation_picard_gap=_lower_text(minimum_variation),
        minimum_second_variation_picard_gap=_lower_text(minimum_second),
        maximum_central_error_radius=_upper_text(maximum_central),
        maximum_first_variation_error_radius=_upper_text(maximum_variation),
        maximum_second_variation_error_radius=_upper_text(maximum_second),
        minimum_time_minor=_lower_text(minimum_time_minor),
        minimum_label_minor=_lower_text(minimum_label_minor),
        minimum_oriented_determinant=_lower_text(minimum_oriented),
        maximum_raw_determinant=_upper_text(maximum_raw),
        maximum_late_physical_x=_upper_text(maximum_late_x),
        minimum_late_entry_x_gap=_lower_text(minimum_late_gap),
        delay_four_previous_solution_cell_count=delay4_count,
        delay_five_affine_history_cell_count=delay5_affine_count,
        delay_five_c4_patch_cell_count=delay5_patch_count,
        delay_five_previous_solution_cell_count=delay5_solution_count,
        proof_cell_digest_sha256=digest.hexdigest(),
    )


def shard_relative_path(precision: int, label_index: int) -> str:
    if precision not in (PRIMARY_PRECISION_BITS, REFINEMENT_PRECISION_BITS):
        raise ValueError("a shard precision must be 192 or 256 bits")
    if type(label_index) is not int or not 0 <= label_index < 20:
        raise ValueError("a shard label index must lie between zero and nineteen")
    return (
        f"{SHARD_DIRECTORY_RELATIVE_PATH}/"
        f"precision_{precision}_label_{label_index:02d}.json"
    )


def _canonical_sha256(value: object) -> str:
    return sha256(
        json.dumps(
            value, sort_keys=True, separators=(",", ":"), ensure_ascii=True
        ).encode("ascii")
    ).hexdigest()


def build_second_step_shard_payload(
    precision: int, label_index: int
) -> dict[str, Any]:
    """Run one deterministic label shard at one declared precision."""

    probe = probe_second_step_cover(
        precision,
        label_start_index=label_index,
        maximum_label_cells=1,
        maximum_second_time_cells=400,
    )
    body = {
        "audit_id": AUDIT_ID,
        "precision_bits": precision,
        "label_index": label_index,
        "label_interval": (
            _label_node(label_index),
            _label_node(label_index + 1),
        ),
        "probe": asdict(probe),
    }
    return {"body": body, "body_sha256": _canonical_sha256(body)}


def _probe_from_mapping(value: Mapping[str, Any]) -> SecondStepProbe:
    expected = {field.name for field in fields(SecondStepProbe)}
    if set(value) != expected:
        raise ValueError("the shard probe fields changed")
    return SecondStepProbe(**dict(value))


def validate_second_step_shard_payload(
    payload: Mapping[str, Any],
    *,
    precision: int,
    label_index: int,
    require_pinned_digest: bool = True,
) -> SecondStepProbe:
    """Reject wrong-label, incomplete, tampered, or unpinned shard data."""

    if set(payload) != {"body", "body_sha256"}:
        raise ValueError("the shard envelope fields changed")
    body = payload.get("body")
    if not isinstance(body, Mapping):
        raise ValueError("the shard body is missing")
    if payload.get("body_sha256") != _canonical_sha256(body):
        raise ValueError("the shard body digest changed")
    if set(body) != {
        "audit_id",
        "precision_bits",
        "label_index",
        "label_interval",
        "probe",
    }:
        raise ValueError("the shard body schema changed")
    if body.get("audit_id") != AUDIT_ID:
        raise ValueError("the shard audit id changed")
    if body.get("precision_bits") != precision:
        raise ValueError("the shard precision changed")
    if body.get("label_index") != label_index:
        raise ValueError("the shard label index changed")
    if tuple(body.get("label_interval", ())) != (
        _label_node(label_index),
        _label_node(label_index + 1),
    ):
        raise ValueError("the shard label interval changed")
    probe_mapping = body.get("probe")
    if not isinstance(probe_mapping, Mapping):
        raise ValueError("the shard probe is missing")
    probe = _probe_from_mapping(probe_mapping)
    if probe.precision_bits != precision or probe.first_failure is not None:
        raise ValueError("the shard did not close at the declared precision")
    if probe.completed_label_cells != 1 or probe.completed_second_time_cells != 400:
        raise ValueError("the shard did not traverse its exact 400-cell grid")
    if (
        probe.delay_four_previous_solution_cell_count,
        probe.delay_five_affine_history_cell_count,
        probe.delay_five_c4_patch_cell_count,
        probe.delay_five_previous_solution_cell_count,
    ) != (400, 100, 100, 200):
        raise ValueError("the shard delayed-source counts changed")
    for name in (
        "minimum_replayed_first_step_picard_gap",
        "minimum_central_picard_gap",
        "minimum_first_variation_picard_gap",
        "minimum_second_variation_picard_gap",
        "minimum_time_minor",
        "minimum_label_minor",
        "minimum_oriented_determinant",
        "minimum_late_entry_x_gap",
    ):
        if Decimal(getattr(probe, name)) <= 0:
            raise ValueError(f"the shard {name} is not strictly positive")
    if Decimal(probe.maximum_raw_determinant) >= 0:
        raise ValueError("the shard raw determinant is not strictly negative")
    if len(probe.proof_cell_digest_sha256) != 64:
        raise ValueError("the shard proof-cell digest has the wrong length")
    if require_pinned_digest:
        pinned = EXPECTED_PROOF_CELL_DIGESTS.get(precision, ())
        if len(pinned) != 20:
            raise ValueError("the proof-cell digest table is not complete")
        if probe.proof_cell_digest_sha256 != pinned[label_index]:
            raise ValueError("the shard proof-cell digest differs from the pinned run")
    return probe


def _selected_text(
    probes: Sequence[SecondStepProbe], name: str, *, minimum: bool
) -> str:
    key = lambda probe: Decimal(getattr(probe, name))
    selected = min(probes, key=key) if minimum else max(probes, key=key)
    return getattr(selected, name)


def aggregate_second_step_shards(
    payloads: Sequence[Mapping[str, Any]],
    *,
    precision: int,
    require_pinned_digest: bool = True,
) -> SecondStepProbe:
    """Hostile exact aggregation of the twenty unique label shards."""

    if len(payloads) != 20:
        raise ValueError("the aggregate requires exactly twenty shard payloads")
    probes = tuple(
        validate_second_step_shard_payload(
            payload,
            precision=precision,
            label_index=index,
            require_pinned_digest=require_pinned_digest,
        )
        for index, payload in enumerate(payloads)
    )
    digest = sha256()
    for index, probe in enumerate(probes):
        digest.update(
            f"{index}:{probe.proof_cell_digest_sha256}\n".encode("ascii")
        )
    return SecondStepProbe(
        precision_bits=precision,
        completed_label_cells=sum(probe.completed_label_cells for probe in probes),
        completed_second_time_cells=sum(
            probe.completed_second_time_cells for probe in probes
        ),
        first_failure=None,
        minimum_replayed_first_step_picard_gap=_selected_text(
            probes, "minimum_replayed_first_step_picard_gap", minimum=True
        ),
        minimum_central_picard_gap=_selected_text(
            probes, "minimum_central_picard_gap", minimum=True
        ),
        minimum_first_variation_picard_gap=_selected_text(
            probes, "minimum_first_variation_picard_gap", minimum=True
        ),
        minimum_second_variation_picard_gap=_selected_text(
            probes, "minimum_second_variation_picard_gap", minimum=True
        ),
        maximum_central_error_radius=_selected_text(
            probes, "maximum_central_error_radius", minimum=False
        ),
        maximum_first_variation_error_radius=_selected_text(
            probes, "maximum_first_variation_error_radius", minimum=False
        ),
        maximum_second_variation_error_radius=_selected_text(
            probes, "maximum_second_variation_error_radius", minimum=False
        ),
        minimum_time_minor=_selected_text(probes, "minimum_time_minor", minimum=True),
        minimum_label_minor=_selected_text(probes, "minimum_label_minor", minimum=True),
        minimum_oriented_determinant=_selected_text(
            probes, "minimum_oriented_determinant", minimum=True
        ),
        maximum_raw_determinant=_selected_text(
            probes, "maximum_raw_determinant", minimum=False
        ),
        maximum_late_physical_x=_selected_text(
            probes, "maximum_late_physical_x", minimum=False
        ),
        minimum_late_entry_x_gap=_selected_text(
            probes, "minimum_late_entry_x_gap", minimum=True
        ),
        delay_four_previous_solution_cell_count=sum(
            probe.delay_four_previous_solution_cell_count for probe in probes
        ),
        delay_five_affine_history_cell_count=sum(
            probe.delay_five_affine_history_cell_count for probe in probes
        ),
        delay_five_c4_patch_cell_count=sum(
            probe.delay_five_c4_patch_cell_count for probe in probes
        ),
        delay_five_previous_solution_cell_count=sum(
            probe.delay_five_previous_solution_cell_count for probe in probes
        ),
        proof_cell_digest_sha256=digest.hexdigest(),
    )


def load_and_aggregate_second_step_shards(
    repository: Path,
    *,
    precision: int,
    require_pinned_digest: bool = True,
) -> SecondStepProbe:
    payloads = tuple(
        json.loads(
            (repository / shard_relative_path(precision, index)).read_text(
                encoding="utf-8"
            )
        )
        for index in range(20)
    )
    return aggregate_second_step_shards(
        payloads,
        precision=precision,
        require_pinned_digest=require_pinned_digest,
    )


@dataclass(frozen=True)
class TargetSecondMethodStepCoverCertificate:
    model_id: str
    audit_id: str
    arithmetic: str
    physical_output_frame: tuple[tuple[int, int], tuple[int, int]]
    physical_frame_determinant: int
    physical_time_interval: tuple[str, str]
    full_physical_time_interval: tuple[str, str]
    label_interval: tuple[str, str]
    time_step: str
    label_step: str
    time_cell_count_per_label: int
    label_cell_count: int
    total_second_step_cell_count: int
    regularity_breakpoints: tuple[str, str]
    delay_source_partition: tuple[str, str, str]
    primary: SecondStepProbe
    refinement: SecondStepProbe
    exact_symbolic_zero_defect_count: int
    exact_scope: str
    open_scope: str
    exact_delay_landing_partition_verified: bool
    exact_c4_regular_source_breakpoints_respected: bool
    exact_two_dimensional_log_norm_identity_verified: bool
    strict_first_step_tubes_replayed_as_delayed_sources: bool
    sampled_or_interpolated_history_used_as_claim_source: bool
    strict_second_step_state_picard_inclusion_validated: bool
    strict_second_step_first_variation_picard_inclusion_validated: bool
    strict_second_step_second_variation_picard_inclusion_validated: bool
    exact_label_mean_value_reconstruction_used: bool
    exact_bernstein_convex_hull_range_theorem_used: bool
    same_kernel_256_bit_precision_replay_validated: bool
    independent_second_interval_kernel_replay_validated: bool
    second_method_step_p_matrix_cover_validated: bool
    late_cross_separation_interval_validated: bool
    full_physical_strip_interval_cover_validated: bool
    physical_cross_separation_interval_validated: bool
    expanded_open_collar_interval_validated: bool
    target_chart_global_embedding_validated: bool
    target_global_graph_fixed_point_validated: bool


RIGOROUS_TRUE_FLAGS = (
    "exact_delay_landing_partition_verified",
    "exact_c4_regular_source_breakpoints_respected",
    "exact_two_dimensional_log_norm_identity_verified",
    "strict_first_step_tubes_replayed_as_delayed_sources",
    "strict_second_step_state_picard_inclusion_validated",
    "strict_second_step_first_variation_picard_inclusion_validated",
    "strict_second_step_second_variation_picard_inclusion_validated",
    "exact_label_mean_value_reconstruction_used",
    "exact_bernstein_convex_hull_range_theorem_used",
    "same_kernel_256_bit_precision_replay_validated",
    "second_method_step_p_matrix_cover_validated",
    "late_cross_separation_interval_validated",
    "full_physical_strip_interval_cover_validated",
    "physical_cross_separation_interval_validated",
)
FALSE_METHOD_FLAGS = (
    "sampled_or_interpolated_history_used_as_claim_source",
    "independent_second_interval_kernel_replay_validated",
)
OPEN_FLAGS = (
    "expanded_open_collar_interval_validated",
    "target_chart_global_embedding_validated",
    "target_global_graph_fixed_point_validated",
)


def _decimal(value: object, name: str) -> Decimal:
    if not isinstance(value, (str, int)) or isinstance(value, bool):
        raise ValueError(f"{name} must be an exact decimal string or integer")
    try:
        result = Decimal(value)
    except InvalidOperation as error:
        raise ValueError(f"{name} is not a decimal") from error
    if not result.is_finite():
        raise ValueError(f"{name} must be finite")
    return result


def _validate_closed_probe(probe: SecondStepProbe, precision: int) -> None:
    if probe.precision_bits != precision:
        raise AssertionError("the second-step precision changed")
    if probe.first_failure is not None:
        raise AssertionError(f"the second-step cover failed at {probe.first_failure}")
    if probe.completed_label_cells != 20 or probe.completed_second_time_cells != 8000:
        raise AssertionError("the second-step cover did not traverse the exact grid")
    expected_counts = (8000, 2000, 2000, 4000)
    actual_counts = (
        probe.delay_four_previous_solution_cell_count,
        probe.delay_five_affine_history_cell_count,
        probe.delay_five_c4_patch_cell_count,
        probe.delay_five_previous_solution_cell_count,
    )
    if actual_counts != expected_counts:
        raise AssertionError("the delayed-source partition cell counts changed")
    for name in (
        "minimum_replayed_first_step_picard_gap",
        "minimum_central_picard_gap",
        "minimum_first_variation_picard_gap",
        "minimum_second_variation_picard_gap",
        "minimum_time_minor",
        "minimum_label_minor",
        "minimum_oriented_determinant",
        "minimum_late_entry_x_gap",
    ):
        if _decimal(getattr(probe, name), name) <= 0:
            raise AssertionError(f"{name} is not strictly positive")
    if _decimal(probe.maximum_raw_determinant, "maximum raw determinant") >= 0:
        raise AssertionError("the raw determinant is not strictly negative")
    if len(probe.proof_cell_digest_sha256) != 64:
        raise AssertionError("the second-step digest has the wrong length")


def _certificate_from_probes(
    primary: SecondStepProbe, refinement: SecondStepProbe
) -> TargetSecondMethodStepCoverCertificate:
    defects = exact_second_step_cover_defects()
    if any(defect != 0 for defect in defects):
        raise AssertionError("an exact second-step identity failed")
    _validate_closed_probe(primary, PRIMARY_PRECISION_BITS)
    _validate_closed_probe(refinement, REFINEMENT_PRECISION_BITS)
    return TargetSecondMethodStepCoverCertificate(
        model_id=MODEL_ID,
        audit_id=AUDIT_ID,
        arithmetic=MANIFEST_ARITHMETIC,
        physical_output_frame=((-7, 2), (3, 1)),
        physical_frame_determinant=-13,
        physical_time_interval=(TIME_LEFT, TIME_RIGHT),
        full_physical_time_interval=("-3", "3"),
        label_interval=(LABEL_LEFT, LABEL_RIGHT),
        time_step=TIME_STEP,
        label_step=LABEL_STEP,
        time_cell_count_per_label=400,
        label_cell_count=20,
        total_second_step_cell_count=8000,
        regularity_breakpoints=(DELAY_FIVE_PATCH_ENTRY_TIME, DELAY_FIVE_PHYSICAL_ENTRY_TIME),
        delay_source_partition=(
            "1<=t<=3: t-4 in the validated first-step solution [-3,-1]",
            "1<=t<=2: t-5 in incoming history [-4,-3], split at the C4 patch onset t=3/2",
            "2<=t<=3: t-5 in the validated first-step solution [-3,-2]",
        ),
        primary=primary,
        refinement=refinement,
        exact_symbolic_zero_defect_count=len(defects),
        exact_scope=(
            "the complete second method-of-steps P-matrix cover on "
            "[1,3]x[-1/20,1/20], composed with the pinned first-step result "
            "to cover [-3,3], and the late X_entry-X separation on [-2,3]"
        ),
        open_scope=(
            "an enlarged label collar, the C4-history/physical gluing theorem "
            "on that collar, the target global graph, and the complete-history root"
        ),
        exact_delay_landing_partition_verified=True,
        exact_c4_regular_source_breakpoints_respected=True,
        exact_two_dimensional_log_norm_identity_verified=True,
        strict_first_step_tubes_replayed_as_delayed_sources=True,
        sampled_or_interpolated_history_used_as_claim_source=False,
        strict_second_step_state_picard_inclusion_validated=True,
        strict_second_step_first_variation_picard_inclusion_validated=True,
        strict_second_step_second_variation_picard_inclusion_validated=True,
        exact_label_mean_value_reconstruction_used=True,
        exact_bernstein_convex_hull_range_theorem_used=True,
        same_kernel_256_bit_precision_replay_validated=True,
        independent_second_interval_kernel_replay_validated=False,
        second_method_step_p_matrix_cover_validated=True,
        late_cross_separation_interval_validated=True,
        full_physical_strip_interval_cover_validated=True,
        physical_cross_separation_interval_validated=True,
        expanded_open_collar_interval_validated=False,
        target_chart_global_embedding_validated=False,
        target_global_graph_fixed_point_validated=False,
    )


@lru_cache(maxsize=1)
def build_target_second_method_step_cover_certificate() -> TargetSecondMethodStepCoverCertificate:
    """Run both full grids directly without consuming stored shards."""

    return _certificate_from_probes(
        probe_second_step_cover(PRIMARY_PRECISION_BITS),
        probe_second_step_cover(REFINEMENT_PRECISION_BITS),
    )


def build_target_second_method_step_cover_certificate_from_shards(
    repository: Path,
    *,
    require_pinned_digest: bool = True,
) -> TargetSecondMethodStepCoverCertificate:
    """Assemble the exact full-grid certificate from twenty shards per run."""

    return _certificate_from_probes(
        load_and_aggregate_second_step_shards(
            repository,
            precision=PRIMARY_PRECISION_BITS,
            require_pinned_digest=require_pinned_digest,
        ),
        load_and_aggregate_second_step_shards(
            repository,
            precision=REFINEMENT_PRECISION_BITS,
            require_pinned_digest=require_pinned_digest,
        ),
    )


def json_ready_target_second_method_step_cover() -> dict[str, Any]:
    return json.loads(
        json.dumps({"certificate": asdict(build_target_second_method_step_cover_certificate())})
    )


def validate_target_second_method_step_cover_audit(payload: Mapping[str, Any]) -> None:
    if not isinstance(payload, Mapping):
        raise ValueError("the second-step audit must be a mapping")
    certificate = payload.get("certificate")
    if not isinstance(certificate, Mapping):
        raise ValueError("the second-step certificate must be a mapping")
    expected_fields = {field.name for field in fields(TargetSecondMethodStepCoverCertificate)}
    if set(certificate) != expected_fields:
        raise ValueError("the second-step certificate fields changed")
    if any(certificate.get(name) is not True for name in RIGOROUS_TRUE_FLAGS):
        raise ValueError("a rigorous second-step claim was weakened")
    if any(certificate.get(name) is not False for name in FALSE_METHOD_FLAGS):
        raise ValueError("a forbidden second-step method was promoted")
    if any(certificate.get(name) is not False for name in OPEN_FLAGS):
        raise ValueError("an open target-chart claim was promoted")
    boolean_fields = {
        field.name
        for field in fields(TargetSecondMethodStepCoverCertificate)
        if field.type in (bool, "bool")
    }
    if boolean_fields != set(RIGOROUS_TRUE_FLAGS) | set(FALSE_METHOD_FLAGS) | set(OPEN_FLAGS):
        raise AssertionError("the second-step claim ledger is incomplete")
    exact_values = {
        "model_id": MODEL_ID,
        "audit_id": AUDIT_ID,
        "arithmetic": MANIFEST_ARITHMETIC,
        "physical_frame_determinant": -13,
        "time_step": TIME_STEP,
        "label_step": LABEL_STEP,
        "time_cell_count_per_label": 400,
        "label_cell_count": 20,
        "total_second_step_cell_count": 8000,
        "exact_symbolic_zero_defect_count": len(exact_second_step_cover_defects()),
    }
    for name, expected in exact_values.items():
        if certificate.get(name) != expected:
            raise ValueError(f"the exact certificate field {name} changed")
    sequence_values = {
        "physical_time_interval": (TIME_LEFT, TIME_RIGHT),
        "full_physical_time_interval": ("-3", "3"),
        "label_interval": (LABEL_LEFT, LABEL_RIGHT),
        "regularity_breakpoints": (
            DELAY_FIVE_PATCH_ENTRY_TIME,
            DELAY_FIVE_PHYSICAL_ENTRY_TIME,
        ),
    }
    for name, expected in sequence_values.items():
        if tuple(certificate.get(name, ())) != expected:
            raise ValueError(f"the exact certificate field {name} changed")
    if tuple(
        tuple(row) for row in certificate.get("physical_output_frame", ())
    ) != ((-7, 2), (3, 1)):
        raise ValueError("the physical output frame changed")
    for name, precision in (("primary", 192), ("refinement", 256)):
        probe = certificate.get(name)
        if not isinstance(probe, Mapping):
            raise ValueError(f"the {name} probe is missing")
        if probe.get("precision_bits") != precision or probe.get("first_failure") is not None:
            raise ValueError(f"the {name} probe did not close")
        if probe.get("completed_second_time_cells") != 8000:
            raise ValueError(f"the {name} second-step grid is incomplete")
        for margin in (
            "minimum_central_picard_gap",
            "minimum_first_variation_picard_gap",
            "minimum_second_variation_picard_gap",
            "minimum_time_minor",
            "minimum_label_minor",
            "minimum_oriented_determinant",
            "minimum_late_entry_x_gap",
        ):
            if _decimal(probe.get(margin), f"{name} {margin}") <= 0:
                raise ValueError(f"the {name} {margin} is not positive")
        if _decimal(probe.get("maximum_raw_determinant"), f"{name} raw determinant") >= 0:
            raise ValueError(f"the {name} raw determinant is not negative")


def _sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def validate_target_second_method_step_cover_result(
    payload: Mapping[str, Any], repository: Path
) -> None:
    if not isinstance(payload, Mapping):
        raise ValueError("the second-step result must be a mapping")
    audit = payload.get("audit")
    manifest = payload.get("manifest")
    if not isinstance(audit, Mapping) or not isinstance(manifest, Mapping):
        raise ValueError("the second-step result requires audit and manifest mappings")
    validate_target_second_method_step_cover_audit(audit)
    paths = {
        "proof_source": PROOF_SOURCE_RELATIVE_PATH,
        "generator": GENERATOR_RELATIVE_PATH,
        "note": NOTE_RELATIVE_PATH,
        "first_step_source": FIRST_STEP_SOURCE_RELATIVE_PATH,
        "first_step_result": FIRST_STEP_RESULT_RELATIVE_PATH,
        "interval_backend_source": INTERVAL_BACKEND_SOURCE_RELATIVE_PATH,
        "c4_seam_source": C4_SEAM_SOURCE_RELATIVE_PATH,
        "physical_model_source": PHYSICAL_MODEL_SOURCE_RELATIVE_PATH,
    }
    expected_manifest_fields = {
        "default_command",
        "arithmetic",
        "python",
        "platform",
        "gmpy2",
        "mpfr",
        "first_step_result_sha256",
        "shards",
        *paths.keys(),
        *(f"{name}_sha256" for name in paths),
    }
    if set(manifest) != expected_manifest_fields:
        raise ValueError("the exact result manifest schema changed")
    if manifest.get("default_command") != DEFAULT_COMMAND:
        raise ValueError("manifest command changed")
    if manifest.get("arithmetic") != MANIFEST_ARITHMETIC:
        raise ValueError("manifest arithmetic changed")
    if manifest.get("python") != platform.python_version():
        raise ValueError("manifest Python version changed")
    if manifest.get("platform") != platform.platform():
        raise ValueError("manifest platform changed")
    if manifest.get("gmpy2") != gmpy2.version() or manifest.get("mpfr") != gmpy2.mpfr_version():
        raise ValueError("the directed interval runtime changed")
    for name, relative in paths.items():
        if manifest.get(name) != relative:
            raise ValueError(f"manifest {name} path changed")
        if manifest.get(f"{name}_sha256") != _sha256(repository / relative):
            raise ValueError(f"manifest {name} hash changed")
    expected_shards = []
    for precision in (PRIMARY_PRECISION_BITS, REFINEMENT_PRECISION_BITS):
        for label_index in range(20):
            relative = shard_relative_path(precision, label_index)
            expected_shards.append(
                {"path": relative, "sha256": _sha256(repository / relative)}
            )
    if manifest.get("shards") != expected_shards:
        raise ValueError("the exact shard source manifest changed")
    reference = {
        "certificate": asdict(
            build_target_second_method_step_cover_certificate_from_shards(
                repository
            )
        )
    }
    if json.loads(json.dumps(dict(audit), sort_keys=True)) != json.loads(
        json.dumps(reference, sort_keys=True)
    ):
        raise ValueError("the second-step audit differs from its pinned shards")
    if manifest.get("first_step_result_sha256") != FIRST_STEP_RESULT_SHA256:
        raise ValueError("the pinned first-step result digest changed")
    if _sha256(repository / FIRST_STEP_RESULT_RELATIVE_PATH) != FIRST_STEP_RESULT_SHA256:
        raise ValueError("the local first-step result is not the pinned parent")
    parent_payload = json.loads(
        (repository / FIRST_STEP_RESULT_RELATIVE_PATH).read_text(encoding="utf-8")
    )
    first.validate_target_first_method_step_cover_result(parent_payload, repository)


__all__ = [
    "AUDIT_ID",
    "DEFAULT_COMMAND",
    "FALSE_METHOD_FLAGS",
    "GENERATOR_RELATIVE_PATH",
    "MANIFEST_ARITHMETIC",
    "MODEL_ID",
    "NOTE_RELATIVE_PATH",
    "OPEN_FLAGS",
    "PRIMARY_PRECISION_BITS",
    "REFINEMENT_PRECISION_BITS",
    "RESULT_RELATIVE_PATH",
    "RIGOROUS_TRUE_FLAGS",
    "SecondStepProbe",
    "TargetSecondMethodStepCoverCertificate",
    "build_target_second_method_step_cover_certificate",
    "exact_second_step_cover_defects",
    "json_ready_target_second_method_step_cover",
    "probe_second_step_cover",
    "validate_target_second_method_step_cover_audit",
    "validate_target_second_method_step_cover_result",
]
