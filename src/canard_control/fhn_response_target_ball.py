"""Directed target ball from the validated FHN response derivative box.

The tracked parameter-box theorem encloses the derivative of

``P(kappa_1, kappa_3) = (1 / T, (V_max - V_min)**2)``

on a convex gain box.  A uniform derivative enclosure is already enough
for a quantitative inverse theorem: second sensitivities are not needed.
This module checks that implication without changing or regenerating the
parameter-box certificate on which it depends.

For the exact binary64 midpoint matrix ``B0``, let ``s0`` be a directed
lower bound for ``sigma_min(B0)`` and let ``rB`` enclose
``sup ||DQ(b) - B0||_F``.  The fixed-inverse Newton map based on ``B0`` has
Euclidean contraction factor at most ``q = rB / s0``.  Hence a centered
input ball of radius ``h`` covers the output ball of radius
``(s0 - rB) * h`` about the *exact* output ``P(b0)``.

Only the two-output baseline statement is validated here.  Transfer to a
calibrated reset coordinate remains conditional on a separately validated
calibration chart and hardware interval.  No physical pulse-onset theorem
is inferred.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

import gmpy2

from canard_control.directed_interval import (
    DirectedInterval,
    decimal_lower,
    decimal_upper,
    upward_division,
    upward_product,
    upward_sum,
)


TRACKED_PARAMETER_BOX_SHA256 = (
    "ff13b5352c2b4e9898a4044be63fd490a3e7bb4217445a6a062188c2457c22a0"
)
TRACKED_PARAMETER_CENTER = ("0.2", "0.25")


@dataclass(frozen=True)
class DirectedDerivativeBoxTargetBall:
    """Auditable fixed-inverse target-ball certificate in Euclidean norm."""

    source_result_sha256: str
    precision_bits: int
    norm_id: str
    control_order: tuple[str, str]
    output_order: tuple[str, str]
    parameter_center: tuple[str, str]
    gain_half_width: str
    midpoint_matrix_binary64: tuple[tuple[float, float], tuple[float, float]]
    recomputed_midpoint_singular_value_lower: str
    recorded_midpoint_singular_value_lower: str
    recomputed_derivative_frobenius_radius_upper: str
    recorded_derivative_frobenius_radius_upper: str
    recomputed_response_margin_lower: str
    recorded_response_margin_lower: str
    fixed_inverse_contraction_upper: str
    fixed_inverse_contraction_margin_lower: str
    certified_input_ball_radius: str
    certified_output_ball_radius_lower: str
    target_ball_center: str
    source_d1_branch_validated: bool
    source_d3_extrema_validated: bool
    source_d4_derivative_box_validated: bool
    source_record_consistent: bool
    centered_input_ball_contained_in_gain_box: bool
    fixed_inverse_contraction_validated: bool
    base_frequency_squared_range_target_ball_validated: bool
    calibrated_reset_transfer_conditional: bool
    calibrated_reset_target_ball_validated: bool
    second_sensitivity_validated: bool
    second_sensitivity_required_for_base_target_ball: bool
    physical_pulse_onset_validated: bool
    issue_15_closed: bool


def _require_mapping(value: object, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{name} must be a mapping")
    return value


def _require_flag(mapping: Mapping[str, Any], name: str) -> None:
    if mapping.get(name) is not True:
        raise ValueError(f"source theorem flag {name!r} must be true")


def _point_decimal(value: str, precision: int) -> DirectedInterval:
    if not isinstance(value, str):
        raise ValueError("directed decimal bounds must be strings")
    return DirectedInterval.from_decimal(value, precision)


def _exact_binary_matrix(
    value: object, precision: int
) -> tuple[tuple[DirectedInterval, DirectedInterval], ...]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        raise ValueError("midpoint_binary64 must be a 2 by 2 array")
    rows = tuple(value)
    if len(rows) != 2:
        raise ValueError("midpoint_binary64 must be a 2 by 2 array")
    result: list[tuple[DirectedInterval, DirectedInterval]] = []
    for row in rows:
        if not isinstance(row, Sequence) or isinstance(row, (str, bytes)):
            raise ValueError("midpoint_binary64 must be a 2 by 2 array")
        entries = tuple(row)
        if len(entries) != 2:
            raise ValueError("midpoint_binary64 must be a 2 by 2 array")
        try:
            result.append(
                (
                    DirectedInterval.from_float(float(entries[0]), precision),
                    DirectedInterval.from_float(float(entries[1]), precision),
                )
            )
        except (TypeError, ValueError, OverflowError) as error:
            raise ValueError(
                "midpoint_binary64 entries must be finite floats"
            ) from error
    return tuple(result)


def _recomputed_singular_lower(
    matrix: tuple[tuple[DirectedInterval, DirectedInterval], ...],
    precision: int,
) -> gmpy2.mpfr:
    determinant = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    determinant_lower = determinant.lower_abs()
    squares = tuple(
        upward_product(entry.upper_abs(), entry.upper_abs(), precision)
        for row in matrix
        for entry in row
    )
    frobenius_squared = upward_sum(squares, precision)
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        frobenius_upper = gmpy2.sqrt(frobenius_squared)
    if determinant_lower <= 0 or frobenius_upper <= 0:
        raise ValueError("midpoint response matrix is not directed-nonsingular")
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        return determinant_lower / frobenius_upper


def _response_intervals(
    response: Mapping[str, Any], precision: int
) -> tuple[tuple[DirectedInterval, DirectedInterval], ...]:
    lower = response.get("response_lower")
    upper = response.get("response_upper")
    if not isinstance(lower, Sequence) or not isinstance(upper, Sequence):
        raise ValueError("response interval endpoints must be 2 by 2 arrays")
    lower_rows = tuple(lower)
    upper_rows = tuple(upper)
    if len(lower_rows) != 2 or len(upper_rows) != 2:
        raise ValueError("response interval endpoints must be 2 by 2 arrays")
    result: list[tuple[DirectedInterval, DirectedInterval]] = []
    for lower_row, upper_row in zip(lower_rows, upper_rows, strict=True):
        if (
            not isinstance(lower_row, Sequence)
            or isinstance(lower_row, (str, bytes))
            or not isinstance(upper_row, Sequence)
            or isinstance(upper_row, (str, bytes))
        ):
            raise ValueError("response interval endpoints must be 2 by 2 arrays")
        lower_entries = tuple(lower_row)
        upper_entries = tuple(upper_row)
        if len(lower_entries) != 2 or len(upper_entries) != 2:
            raise ValueError("response interval endpoints must be 2 by 2 arrays")
        row: list[DirectedInterval] = []
        for left, right in zip(lower_entries, upper_entries, strict=True):
            if not isinstance(left, str) or not isinstance(right, str):
                raise ValueError("response interval endpoints must be decimal strings")
            row.append(DirectedInterval.from_bounds(left, right, precision))
        result.append((row[0], row[1]))
    return tuple(result)


def _recomputed_response_radius_upper(
    intervals: tuple[tuple[DirectedInterval, DirectedInterval], ...],
    midpoint: tuple[tuple[DirectedInterval, DirectedInterval], ...],
    precision: int,
) -> gmpy2.mpfr:
    entry_radii = tuple(
        (intervals[row][column] - midpoint[row][column]).upper_abs()
        for row in range(2)
        for column in range(2)
    )
    squared = upward_sum(
        tuple(upward_product(item, item, precision) for item in entry_radii),
        precision,
    )
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        return gmpy2.sqrt(squared)


def _box_contains_declared_ball(
    gain_box: Mapping[str, Any],
    center: tuple[str, str],
    half_width: DirectedInterval,
    precision: int,
) -> bool:
    fields = (
        ("kappa_1_lower", "kappa_1_upper"),
        ("kappa_3_lower", "kappa_3_upper"),
    )
    for center_value, (lower_name, upper_name) in zip(
        center, fields, strict=True
    ):
        lower_text = gain_box.get(lower_name)
        upper_text = gain_box.get(upper_name)
        if not isinstance(lower_text, str) or not isinstance(upper_text, str):
            raise ValueError("gain-box endpoints must be decimal strings")
        recorded = DirectedInterval.from_bounds(
            lower_text, upper_text, precision
        )
        center_interval = DirectedInterval.from_decimal(center_value, precision)
        declared_lower = center_interval - half_width
        declared_upper = center_interval + half_width
        if (
            recorded.lower > declared_lower.lower
            or recorded.upper < declared_upper.upper
        ):
            return False
    return True


def _as_binary_tuple(
    matrix: tuple[tuple[DirectedInterval, DirectedInterval], ...]
) -> tuple[tuple[float, float], tuple[float, float]]:
    return (
        (float(matrix[0][0].lower), float(matrix[0][1].lower)),
        (float(matrix[1][0].lower), float(matrix[1][1].lower)),
    )


def directed_target_ball_from_payload(
    payload: Mapping[str, Any],
    *,
    source_result_sha256: str,
    precision: int = 160,
    parameter_center: tuple[str, str] = TRACKED_PARAMETER_CENTER,
) -> DirectedDerivativeBoxTargetBall:
    """Validate the response record and derive its fixed-inverse target ball.

    ``source_result_sha256`` is provenance, not a substitute for checking
    bytes.  Use :func:`load_directed_target_ball` for the hash-checked path.
    This lower-level function is public so manufactured records can exercise
    each semantic refusal independently in tests.
    """

    if not isinstance(source_result_sha256, str) or len(source_result_sha256) != 64:
        raise ValueError("source_result_sha256 must be a 64-character digest")
    try:
        int(source_result_sha256, 16)
    except ValueError as error:
        raise ValueError("source_result_sha256 must be hexadecimal") from error
    if (
        isinstance(precision, bool)
        or int(precision) != precision
        or int(precision) < 64
    ):
        raise ValueError("precision must be an integer of at least 64 bits")
    precision = int(precision)
    if (
        not isinstance(parameter_center, tuple)
        or len(parameter_center) != 2
        or any(not isinstance(item, str) for item in parameter_center)
    ):
        raise ValueError("parameter_center must contain two decimal strings")

    root = _require_mapping(payload, "payload")
    validation = _require_mapping(root.get("validation"), "validation")
    continuation = _require_mapping(
        validation.get("continuation"), "validation.continuation"
    )
    extrema = _require_mapping(validation.get("extrema"), "validation.extrema")
    response = _require_mapping(validation.get("response"), "validation.response")
    gain_box = _require_mapping(validation.get("gain_box"), "validation.gain_box")
    scope = _require_mapping(root.get("scope"), "scope")

    for mapping, names in (
        (
            validation,
            (
                "d1_validated",
                "d3_validated",
                "d4_response_lower_bound_validated",
                "all_d1_d3_d4_validated",
            ),
        ),
        (
            continuation,
            (
                "parameter_box_orbit_validated",
                "parameter_box_bordered_inverse_validated",
            ),
        ),
        (extrema, ("extrema_validated",)),
        (response, ("response_box_validated",)),
        (
            scope,
            (
                "d1_parameter_box_continuation",
                "d3_unique_voltage_extrema",
                "d4_directed_response_lower_bound",
            ),
        ),
    ):
        for name in names:
            _require_flag(mapping, name)

    control_order = tuple(response.get("control_order", ()))
    output_order = tuple(response.get("output_order", ()))
    if control_order != ("kappa_1", "kappa_3"):
        raise ValueError("unexpected control order in response certificate")
    if output_order != ("F", "R_h"):
        raise ValueError("unexpected output order in response certificate")

    half_width_text = gain_box.get("half_width")
    if not isinstance(half_width_text, str):
        raise ValueError("gain half-width must be an exact decimal string")
    half_width = _point_decimal(half_width_text, precision)
    if half_width.lower <= 0:
        raise ValueError("gain half-width must be positive")
    ball_contained = _box_contains_declared_ball(
        gain_box, parameter_center, half_width, precision
    )
    if not ball_contained:
        raise ValueError("gain box does not contain the declared centered ball")

    midpoint = _exact_binary_matrix(response.get("midpoint_binary64"), precision)
    intervals = _response_intervals(response, precision)
    for row in range(2):
        for column in range(2):
            if not intervals[row][column].intersects(midpoint[row][column]):
                raise ValueError(
                    "response interval does not contain its midpoint entry"
                )

    recomputed_s0 = _recomputed_singular_lower(midpoint, precision)
    recomputed_radius = _recomputed_response_radius_upper(
        intervals, midpoint, precision
    )

    recorded_s0_text = response.get("midpoint_smallest_singular_value_lower")
    recorded_radius_text = response.get("response_frobenius_radius_upper")
    recorded_beta_text = response.get("smallest_singular_value_lower")
    if not all(
        isinstance(item, str)
        for item in (recorded_s0_text, recorded_radius_text, recorded_beta_text)
    ):
        raise ValueError("recorded response bounds must be decimal strings")
    recorded_s0 = _point_decimal(recorded_s0_text, precision)
    recorded_radius = _point_decimal(recorded_radius_text, precision)
    recorded_beta = _point_decimal(recorded_beta_text, precision)
    if recorded_s0.lower <= 0 or recorded_radius.lower < 0:
        raise ValueError("recorded response bounds have invalid signs")

    # A reported lower bound may be smaller and a reported upper bound may
    # be larger than the independently recomputed quantities, never the
    # reverse.  Parsing is outward, so compare the safe endpoints.
    if recorded_s0.lower > recomputed_s0:
        raise ValueError("recorded midpoint singular lower bound is overstated")
    # The four exported entry intervals have each been rounded outward to a
    # decimal string independently of the exported aggregate radius.  Their
    # reassembled radius can therefore exceed the separately exported MPFR
    # radius by a few serialization ulps.  The target theorem below uses the
    # larger reassembled radius.  This small consistency allowance is only a
    # refusal threshold; it never enlarges a proved target radius.
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        serialization_slack = gmpy2.mul_2exp(
            max(gmpy2.mpfr(1), recomputed_radius), -precision + 8
        )
        recorded_radius_with_slack = recorded_radius.upper + serialization_slack
    if recorded_radius_with_slack < recomputed_radius:
        raise ValueError("recorded response Frobenius radius is understated")

    # Recompose all public theorem constants from the outward decimal strings
    # that are actually serialized.  The underlying MPFR quantities are
    # already safe, but this extra step makes every displayed beta, contraction,
    # and target radius derivable from the displayed parent endpoints.
    recomputed_s0_text = decimal_lower(recomputed_s0)
    recomputed_radius_text = decimal_upper(recomputed_radius)
    public_s0 = DirectedInterval.from_decimal(
        recomputed_s0_text, precision
    ).lower
    public_radius = DirectedInterval.from_decimal(
        recomputed_radius_text, precision
    ).upper
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        recomputed_beta = public_s0 - public_radius
        recorded_implied_beta = recorded_s0.lower - recorded_radius.upper
    if recomputed_beta <= 0:
        raise ValueError("response derivative box does not give a contraction")
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        recorded_implied_beta_with_slack = (
            recorded_implied_beta + serialization_slack
        )
    if recorded_beta.lower > recorded_implied_beta_with_slack:
        raise ValueError("recorded response singular-value margin is overstated")

    contraction = upward_division(public_radius, public_s0, precision)
    contraction_text = decimal_upper(contraction)
    public_contraction = DirectedInterval.from_decimal(
        contraction_text, precision
    ).upper
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        contraction_margin = gmpy2.mpfr(1) - public_contraction
    if public_contraction >= 1 or contraction_margin <= 0:
        raise ValueError("fixed-inverse Newton map is not a strict contraction")
    input_radius_text = decimal_lower(half_width.lower)
    input_radius = DirectedInterval.from_decimal(
        input_radius_text, precision
    ).lower
    beta_text = decimal_lower(recomputed_beta)
    public_beta = DirectedInterval.from_decimal(beta_text, precision).lower
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        output_radius = public_beta * input_radius
    if output_radius <= 0:
        raise ValueError("directed target-ball radius is not positive")

    return DirectedDerivativeBoxTargetBall(
        source_result_sha256=source_result_sha256,
        precision_bits=precision,
        norm_id="euclidean-input-output-fixed-midpoint-inverse",
        control_order=("kappa_1", "kappa_3"),
        output_order=("F", "R_h"),
        parameter_center=parameter_center,
        gain_half_width=half_width_text,
        midpoint_matrix_binary64=_as_binary_tuple(midpoint),
        recomputed_midpoint_singular_value_lower=recomputed_s0_text,
        recorded_midpoint_singular_value_lower=recorded_s0_text,
        recomputed_derivative_frobenius_radius_upper=recomputed_radius_text,
        recorded_derivative_frobenius_radius_upper=recorded_radius_text,
        recomputed_response_margin_lower=beta_text,
        recorded_response_margin_lower=recorded_beta_text,
        fixed_inverse_contraction_upper=contraction_text,
        fixed_inverse_contraction_margin_lower=decimal_lower(
            contraction_margin
        ),
        certified_input_ball_radius=input_radius_text,
        certified_output_ball_radius_lower=decimal_lower(output_radius),
        target_ball_center=(
            f"exact P({parameter_center[0]},{parameter_center[1]}), "
            "not a binary64 surrogate"
        ),
        source_d1_branch_validated=True,
        source_d3_extrema_validated=True,
        source_d4_derivative_box_validated=True,
        source_record_consistent=True,
        centered_input_ball_contained_in_gain_box=True,
        fixed_inverse_contraction_validated=True,
        base_frequency_squared_range_target_ball_validated=True,
        calibrated_reset_transfer_conditional=True,
        calibrated_reset_target_ball_validated=False,
        second_sensitivity_validated=False,
        second_sensitivity_required_for_base_target_ball=False,
        physical_pulse_onset_validated=False,
        issue_15_closed=False,
    )


def load_directed_target_ball(
    path: str | Path,
    *,
    expected_sha256: str = TRACKED_PARAMETER_BOX_SHA256,
    precision: int = 160,
    parameter_center: tuple[str, str] = TRACKED_PARAMETER_CENTER,
) -> DirectedDerivativeBoxTargetBall:
    """Hash-check a parameter-box JSON file and derive the target ball."""

    source = Path(path)
    data = source.read_bytes()
    actual = sha256(data).hexdigest()
    if actual != expected_sha256:
        raise ValueError(
            "parameter-box result SHA-256 mismatch: "
            f"expected {expected_sha256}, got {actual}"
        )
    try:
        payload = json.loads(data)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError("parameter-box result is not valid UTF-8 JSON") from error
    return directed_target_ball_from_payload(
        _require_mapping(payload, "payload"),
        source_result_sha256=actual,
        precision=precision,
        parameter_center=parameter_center,
    )
