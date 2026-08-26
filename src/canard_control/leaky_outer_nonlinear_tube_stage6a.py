"""Stage-6A source-bound nonlinear outer return-tube certificate.

Stage 3I proves the derivative of the phase-fixed outer return on the
reduced arbitrary-C0 history section.  This module adds a deliberately
conservative C2 flow estimate, a directed local-section phase cover, and a
complete-history forward tube.  The resulting radius is tiny; the theorem
is therefore a local nonlinear return result, not a biological pulse-entry
or two-sided-routing theorem.
"""

from __future__ import annotations

from functools import lru_cache
from hashlib import sha256
import json
import math
import os
from pathlib import Path
import platform
from typing import Any, Mapping, Sequence

import gmpy2
import numpy as np
import scipy

from canard_control.directed_interval import (
    DirectedComplexInterval,
    DirectedInterval,
    complex_unit_interval,
    decimal_lower,
    decimal_upper,
    pi_interval,
    upward_sum,
)
from canard_control.fhn_periodic_directed_validation import directed_dft
from canard_control.leaky_floquet_transfer import (
    validate_leaky_floquet_transfer_artifact,
)
from canard_control.leaky_outer_high_resolution import (
    validate_outer_high_resolution_artifact,
)
from canard_control.leaky_outer_signed_density_stage3i_tv import (
    _validate_outer_signed_density_stage3i_tv_result,
)
from canard_control.leaky_outer_two_sided_routing_contract import (
    validate_outer_two_sided_routing_result,
)
from canard_control.leaky_pulse_outer_third_return_enclosure import (
    validate_third_return_result,
)
from canard_control.leaky_pulse_quiet_capture import _poly_bernstein_range


SCHEMA_ID = "leaky-outer-nonlinear-tube-stage6a-v1"
MODEL_ID = "autonomous-leaky-recovery-two-delay-fhn-bistable-proposal"
BRANCH = "outer_pulse"
SOURCE_RELATIVE_PATH = (
    "src/canard_control/leaky_outer_nonlinear_tube_stage6a.py"
)
GENERATOR_RELATIVE_PATH = "experiments/leaky_outer_nonlinear_tube_stage6a.py"
RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_outer_nonlinear_tube_stage6a.json"
)
NOTE_RELATIVE_PATH = "docs/leaky-outer-nonlinear-tube-stage6a.md"
TEST_RELATIVE_PATH = "tests/test_leaky_outer_nonlinear_tube_stage6a.py"
SOURCE_MANIFEST = (
    SOURCE_RELATIVE_PATH,
    GENERATOR_RELATIVE_PATH,
    NOTE_RELATIVE_PATH,
    TEST_RELATIVE_PATH,
    "src/canard_control/directed_interval.py",
    "src/canard_control/fhn_periodic_directed_validation.py",
    "src/canard_control/leaky_floquet_transfer.py",
    "src/canard_control/leaky_outer_high_resolution.py",
    "src/canard_control/leaky_outer_signed_density_stage3i_tv.py",
    "src/canard_control/leaky_outer_two_sided_routing_contract.py",
    "src/canard_control/leaky_pulse_outer_third_return_enclosure.py",
    "src/canard_control/leaky_pulse_quiet_capture.py",
)
DEFAULT_COMMAND = (
    "OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 "
    "PYTHONPATH=build/testdeps:src /usr/bin/python3 "
    "experiments/leaky_outer_nonlinear_tube_stage6a.py"
)
ARITHMETIC_SCOPE = (
    "exact-byte parent binding; 192-bit outward MPFR DFT/Taylor/Bernstein "
    "cover of 256 normalized outer-orbit phase cells; exact-decimal "
    "Gronwall, first/second variation, implicit-event, and complete-history "
    "tube inequalities at a radius of 1e-335"
)

STAGE3I_RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_outer_signed_density_stage3i_tv.json"
)
STAGE3I_RESULT_SHA256 = (
    "5fdb1a843070ceb5887f7384431f2414989afc3cb741abc7f19ed44a333d4970"
)
OUTER_RESULT_RELATIVE_PATH = (
    "experiments/results/autonomous_leaky_recovery_outer_high_resolution.json"
)
OUTER_RESULT_SHA256 = (
    "d888916fed919f1515dd31ab851b2229816ea373365fa0221b1e345580f165a7"
)
FLOQUET_RESULT_RELATIVE_PATH = "experiments/results/leaky_floquet_transfer.json"
FLOQUET_RESULT_SHA256 = (
    "5a3709ec792b29ed41533101245b13b3d35084ae508bdd1d420728200a5a5b16"
)
ROUTING_RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_outer_two_sided_routing_contract.json"
)
ROUTING_RESULT_SHA256 = (
    "1f9920ab25eec017c6cf06d1cd6a0ce9a3c349ef20c400b86ca0e65d56ee8cab"
)
ATTACHMENT_RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_pulse_outer_third_return_enclosure.json"
)
ATTACHMENT_RESULT_SHA256 = (
    "7a01c2a8ec6b5421c090836f4962e595027d78be3381d490c4b6eb56d3beb13d"
)
PARENT_SHA256 = {
    STAGE3I_RESULT_RELATIVE_PATH: STAGE3I_RESULT_SHA256,
    OUTER_RESULT_RELATIVE_PATH: OUTER_RESULT_SHA256,
    FLOQUET_RESULT_RELATIVE_PATH: FLOQUET_RESULT_SHA256,
    ROUTING_RESULT_RELATIVE_PATH: ROUTING_RESULT_SHA256,
    ATTACHMENT_RESULT_RELATIVE_PATH: ATTACHMENT_RESULT_SHA256,
}

PRECISION_BITS = 192
PHASE_CELL_COUNT = 256
FOURIER_TAYLOR_DEGREE = 24
SECTION_RADIUS = "1e-335"
COMPLETE_HISTORY_TUBE_RADIUS = "0.001"
EPSILON = "0.2"
KAPPA_1 = "0.004"
KAPPA_3 = "0.005"
EXPECTED_NUMERIC_CORE_SHA256 = (
    "a4afa5902d95fcbfa50477bae7c30b6998097fd823eab2ea3eee9c26cad0f144"
)

TRUE_FLAGS = (
    "stage3i_arbitrary_c0_linear_return_parent_validated",
    "stage3i_exact_voltage_and_recovery_row_bounds_imported",
    "outer_exact_periodic_orbit_parent_validated",
    "outer_local_vector_field_quadratic_remainder_validated",
    "outer_local_vector_field_second_derivative_bound_validated",
    "all_254_middle_phase_cells_directed_bernstein_separated",
    "both_wrap_event_cells_have_strict_positive_exact_speed",
    "uniform_reduced_section_ball_validated",
    "c2_event_phase_map_validated",
    "no_earlier_local_section_hit_validated",
    "returned_history_window_strictly_after_initial_time",
    "complete_history_forward_tube_invariant",
    "outer_nonlinear_return_contraction_validated",
    "outer_quantitative_attracting_return_tube_validated",
)
FALSE_FLAGS = (
    "radius_1e_minus_4_outer_return_tube_validated",
    "ambient_ball_phase_projection_validated_at_J_0p32_distance",
    "J_0p32_outer_tube_entry_validated",
    "outer_pulse_capture_validated",
    "inner_stable_graph_used_by_stage6a",
    "two_sided_biological_routing_validated",
    "physical_pulse_onset_validated",
    "frequency_amplitude_safety_control_theorem_validated",
)


def canonical_sha256(value: Any) -> str:
    return sha256(
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        ).encode("ascii")
    ).hexdigest()


def _sha256_path(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _mapping(value: object, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{name} must be a mapping")
    return value


def _load_bound_json(
    repository: Path, relative: str, expected_sha256: str
) -> Mapping[str, Any]:
    path = repository / relative
    if _sha256_path(path) != expected_sha256:
        raise ValueError(f"a Stage-6A parent changed: {relative}")
    payload = json.loads(path.read_text(encoding="utf-8"))
    return _mapping(payload, relative)


def _environment() -> dict[str, Any]:
    return {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "gmpy2": gmpy2.version(),
        "mpfr": gmpy2.mpfr_version(),
        "precision_bits": PRECISION_BITS,
        "openblas_num_threads": os.environ.get("OPENBLAS_NUM_THREADS"),
        "omp_num_threads": os.environ.get("OMP_NUM_THREADS"),
    }


def _point(value: str | int, precision: int = PRECISION_BITS) -> DirectedInterval:
    return DirectedInterval.from_decimal(value, precision)


def _complex_one(precision: int) -> DirectedComplexInterval:
    return DirectedComplexInterval.from_real(_point(1, precision))


def _fourier_taylor_polynomial(
    sequence: Mapping[int, DirectedComplexInterval],
    relative_left: DirectedInterval,
    normalized_width: DirectedInterval,
    degree: int = FOURIER_TAYLOR_DEGREE,
) -> tuple[tuple[DirectedInterval, ...], gmpy2.mpfr]:
    """Taylor-enclose an exact-dyadic DFT on one normalized phase cell."""

    precision = relative_left.precision
    if normalized_width.precision != precision:
        raise ValueError("phase-cell precisions differ")
    two_pi = 2 * pi_interval(precision)
    coefficients = [
        DirectedComplexInterval.zero(precision) for _ in range(degree + 1)
    ]
    remainders: list[gmpy2.mpfr] = []
    for mode, value in sequence.items():
        phase = complex_unit_interval(two_pi * mode * relative_left)
        imaginary_rate = two_pi * mode * normalized_width
        rate = DirectedComplexInterval(_point(0, precision), imaginary_rate)
        phased = value * phase
        power = _complex_one(precision)
        factorial = 1
        for order in range(degree + 1):
            if order:
                factorial *= order
            coefficients[order] = coefficients[order] + (
                phased * power * (_point(1, precision) / factorial)
            )
            power = power * rate
        with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
            magnitude = (
                two_pi.upper * abs(mode) * normalized_width.upper
            )
            remainders.append(
                value.upper_abs()
                * gmpy2.exp(magnitude)
                * magnitude ** (degree + 1)
                / math.factorial(degree + 1)
            )
    return (
        tuple(coefficient.real for coefficient in coefficients),
        upward_sum(remainders, precision),
    )


def _range_with_remainder(
    coefficients: Sequence[DirectedInterval], remainder: gmpy2.mpfr
) -> DirectedInterval:
    polynomial_range = _poly_bernstein_range(coefficients)
    precision = polynomial_range.precision
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        lower = polynomial_range.lower - remainder
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        upper = polynomial_range.upper + remainder
    return DirectedInterval(lower, upper, precision)


def _component_cell_range(
    sequence: Mapping[int, DirectedComplexInterval],
    left: DirectedInterval,
    width: DirectedInterval,
) -> DirectedInterval:
    polynomial, remainder = _fourier_taylor_polynomial(
        sequence, left, width
    )
    return _range_with_remainder(polynomial, remainder)


def _lower_absolute(interval: DirectedInterval) -> gmpy2.mpfr:
    if interval.lower > 0:
        return interval.lower
    if interval.upper < 0:
        with gmpy2.context(
            precision=interval.precision, round=gmpy2.RoundDown
        ):
            return -interval.upper
    return gmpy2.mpfr(0, precision=interval.precision)


def _phase_zero(
    sequence: Mapping[int, DirectedComplexInterval],
) -> DirectedInterval:
    precision = next(iter(sequence.values())).precision
    total = DirectedComplexInterval.zero(precision)
    for value in sequence.values():
        total = total + value
    return total.real


def _candidate_fast_cell(
    voltage: Mapping[int, DirectedComplexInterval],
    recovery: Mapping[int, DirectedComplexInterval],
    period: DirectedInterval,
    cell_index: int,
) -> DirectedInterval:
    precision = period.precision
    one = _point(1, precision)
    width = one / PHASE_CELL_COUNT
    left = _point(cell_index, precision) / PHASE_CELL_COUNT
    current_voltage = _component_cell_range(voltage, left, width)
    current_recovery = _component_cell_range(recovery, left, width)
    epsilon = _point(EPSILON, precision)
    kappa_1 = _point(KAPPA_1, precision)
    kappa_3 = _point(KAPPA_3, precision)
    sqrt_five = _point(5, precision).sqrt()
    delayed = tuple(
        _component_cell_range(
            voltage, left - multiplier * sqrt_five / period, width
        )
        for multiplier in (4, 5)
    )
    half = one / 2
    return (
        current_voltage
        - current_voltage**3 / 3
        - current_recovery
        + epsilon
        * kappa_1
        * (half * (delayed[0] + delayed[1]) - current_voltage)
        + epsilon
        * kappa_3
        * (
            half * ((delayed[0] - 1) ** 3 + (delayed[1] - 1) ** 3)
            - (current_voltage - 1) ** 3
        )
    )


def _directed_phase_cover(
    orbit: Any,
    orbit_correction_upper: gmpy2.mpfr,
    exact_history_correction_upper: gmpy2.mpfr,
    fast_lipschitz_upper: gmpy2.mpfr,
    history_correction_formula: str,
) -> dict[str, Any]:
    """Prove middle-arc separation and positive speed on both wrap cells."""

    precision = PRECISION_BITS
    voltage = directed_dft(orbit.state[:, 0], precision)
    recovery = directed_dft(orbit.state[:, 1], precision)
    period = DirectedInterval.from_float(float(orbit.period), precision)
    one = _point(1, precision)
    width = one / PHASE_CELL_COUNT
    zero_values = (_phase_zero(voltage), _phase_zero(recovery))
    minimum: gmpy2.mpfr | None = None
    minimum_index: int | None = None
    minimum_components: tuple[gmpy2.mpfr, gmpy2.mpfr] | None = None

    for cell_index in range(1, PHASE_CELL_COUNT - 1):
        left = _point(cell_index, precision) / PHASE_CELL_COUNT
        component_lowers: list[gmpy2.mpfr] = []
        for sequence, phase_zero in zip(
            (voltage, recovery), zero_values, strict=True
        ):
            polynomial, remainder = _fourier_taylor_polynomial(
                sequence, left, width
            )
            shifted = list(polynomial)
            shifted[0] = shifted[0] - phase_zero
            component_lowers.append(
                _lower_absolute(
                    _range_with_remainder(tuple(shifted), remainder)
                )
            )
        local = max(component_lowers)
        if minimum is None or local < minimum:
            minimum = local
            minimum_index = cell_index
            minimum_components = (
                component_lowers[0],
                component_lowers[1],
            )

    if minimum is None or minimum_index is None or minimum_components is None:
        raise AssertionError("the Stage-6A middle phase cover is empty")
    first_fast = _candidate_fast_cell(voltage, recovery, period, 0)
    final_fast = _candidate_fast_cell(
        voltage, recovery, period, PHASE_CELL_COUNT - 1
    )
    candidate_speed_lower = min(first_fast.lower, final_fast.lower)
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        exact_separation_lower = minimum - 2 * orbit_correction_upper
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        speed_transfer = (
            fast_lipschitz_upper * exact_history_correction_upper
        )
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        exact_speed_lower = candidate_speed_lower - speed_transfer
    if exact_separation_lower <= 0 or exact_speed_lower <= 0:
        raise ArithmeticError("the Stage-6A directed phase cover did not close")
    return {
        "precision_bits": precision,
        "normalized_phase_cell_count": PHASE_CELL_COUNT,
        "normalized_wrap_half_width": "1/256",
        "middle_phase_cell_count": PHASE_CELL_COUNT - 2,
        "fourier_taylor_degree": FOURIER_TAYLOR_DEGREE,
        "candidate_coefficients_treated_as_exact_binary64_dyadics": True,
        "candidate_period_binary64_hex": float(orbit.period).hex(),
        "candidate_period_binary64_decimal": format(
            float(orbit.period), ".17g"
        ),
        "exact_period_correction_upper": decimal_upper(
            orbit_correction_upper, 70
        ),
        "point_samples_used_as_proof": False,
        "candidate_middle_current_state_separation_lower": decimal_lower(
            minimum, 70
        ),
        "middle_separation_minimizer_cell": minimum_index,
        "minimizer_voltage_absolute_lower": decimal_lower(
            minimum_components[0], 70
        ),
        "minimizer_recovery_absolute_lower": decimal_lower(
            minimum_components[1], 70
        ),
        "twice_exact_orbit_coefficient_correction_upper": decimal_upper(
            2 * orbit_correction_upper, 70
        ),
        "exact_middle_current_state_separation_lower": decimal_lower(
            exact_separation_lower, 70
        ),
        "first_wrap_candidate_fast_speed_lower": decimal_lower(
            first_fast.lower, 70
        ),
        "final_wrap_candidate_fast_speed_lower": decimal_lower(
            final_fast.lower, 70
        ),
        "candidate_wrap_fast_speed_lower": decimal_lower(
            candidate_speed_lower, 70
        ),
        "candidate_to_exact_history_correction_upper": decimal_upper(
            exact_history_correction_upper, 70
        ),
        "candidate_to_exact_history_correction_formula": (
            history_correction_formula
        ),
        "period_correction_included_in_exact_history_transfer": True,
        "fast_field_speed_transfer_upper": decimal_upper(
            speed_transfer, 70
        ),
        "exact_wrap_fast_speed_lower": decimal_lower(
            exact_speed_lower, 70
        ),
        "all_middle_cells_separated": True,
        "both_wrap_cells_strictly_positive": True,
    }


def _upper_decimal(value: object) -> gmpy2.mpfr:
    return DirectedInterval.from_decimal(str(value), PRECISION_BITS).upper


def _lower_decimal(value: object) -> gmpy2.mpfr:
    return DirectedInterval.from_decimal(str(value), PRECISION_BITS).lower


def _analytic_tube(
    *,
    orbit: Any,
    routing: Mapping[str, Any],
    stage3i: Mapping[str, Any],
    attachment: Mapping[str, Any],
    phase_cover: Mapping[str, Any],
) -> dict[str, Any]:
    precision = PRECISION_BITS
    local_field = _mapping(
        routing.get("outer_local_vector_field_evidence"),
        "routing local-field evidence",
    )
    if not (
        local_field.get("quadratic_vector_field_remainder_validated") is True
        and local_field.get("vector_field_second_derivative_bound_validated")
        is True
        and local_field.get("declared_tube_remains_inside_proved_voltage_strip")
        is True
    ):
        raise ValueError("the outer local-field theorem parent changed")
    ledger = _mapping(stage3i.get("transfer_ledger"), "Stage-3I ledger")
    rows = _mapping(ledger.get("rows"), "Stage-3I rows")
    voltage_row = _mapping(rows.get("voltage"), "Stage-3I voltage row")
    recovery_row = _mapping(rows.get("recovery"), "Stage-3I recovery row")
    q_v = _upper_decimal(voltage_row.get("stage2_shadow_plus_E_upper"))
    q_w = _upper_decimal(recovery_row.get("stage2_shadow_plus_E_upper"))
    q = max(q_v, q_w)
    if q >= 1 or ledger.get("arbitrary_c0_linear_contraction_closes") is not True:
        raise ValueError("the Stage-3I arbitrary-C0 contraction was lost")

    centered_voltage = _upper_decimal(
        local_field.get("exact_outer_centered_voltage_abs_upper")
    )
    exact_orbit_speed = _upper_decimal(
        local_field.get("exact_outer_physical_history_speed_upper")
    )
    radius = _upper_decimal(SECTION_RADIUS)
    full_radius = _upper_decimal(COMPLETE_HISTORY_TUBE_RADIUS)
    declared_parent_radius = _upper_decimal(
        local_field.get("declared_local_history_radius")
    )
    strip_margin = _lower_decimal(
        local_field.get("strict_outer_orbit_strip_margin_lower")
    )
    if full_radius > declared_parent_radius or full_radius > strip_margin:
        raise ValueError("the Stage-6A full tube left the proved field domain")
    epsilon = _upper_decimal(EPSILON)
    kappa_1 = _upper_decimal(KAPPA_1)
    kappa_3 = _upper_decimal(KAPPA_3)
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        voltage_strip = centered_voltage + full_radius
        fast_lipschitz = (
            2
            + (1 + voltage_strip) ** 2
            + 2 * epsilon * kappa_1
            + 6 * epsilon * kappa_3 * voltage_strip**2
        )
        flow_lipschitz = max(fast_lipschitz, 2 * epsilon)
        field_second_derivative = (
            2 * (1 + centered_voltage + full_radius)
            + 12 * epsilon * kappa_3 * (centered_voltage + full_radius)
        )
        field_quadratic_remainder = (
            1
            + centered_voltage
            + full_radius / 3
            + 2
            * epsilon
            * kappa_3
            * (3 * centered_voltage + full_radius)
        )

    outer_artifact = _mapping(
        _mapping(attachment.get("exact_outer_orbit_correction"), "attachment correction"),
        "attachment correction",
    )
    candidate_period = DirectedInterval.from_float(float(orbit.period), precision)
    period_correction = _upper_decimal(
        outer_artifact.get("coefficient_and_period_correction_radius_upper")
    )
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        period_lower = candidate_period.lower - period_correction
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        period_upper = candidate_period.upper + period_correction
        horizon = period_upper * (PHASE_CELL_COUNT + 1) / PHASE_CELL_COUNT
        flow_gain = gmpy2.exp(flow_lipschitz * horizon)
        flow_deviation = flow_gain * radius
    if flow_deviation >= full_radius:
        raise ArithmeticError("the Stage-6A uniform nonlinear flow ball failed")

    base_speed = _lower_decimal(phase_cover.get("exact_wrap_fast_speed_lower"))
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        perturbation_speed_loss = fast_lipschitz * flow_deviation
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        event_speed = base_speed - perturbation_speed_loss
        event_sign_margin = (
            base_speed * period_lower / PHASE_CELL_COUNT - flow_deviation
        )
        no_earlier_margin = (
            _lower_decimal(
                phase_cover.get("exact_middle_current_state_separation_lower")
            )
            - flow_deviation
            - radius
        )
    if event_speed <= 0 or event_sign_margin <= 0 or no_earlier_margin <= 0:
        raise ArithmeticError("the Stage-6A event/no-earlier-hit gate failed")

    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        perturbed_flow_speed = exact_orbit_speed + flow_lipschitz * full_radius
        acceleration = flow_lipschitz * perturbed_flow_speed
        first_variation = flow_gain
        second_fixed_time_variation = (
            field_second_derivative * horizon * flow_gain**2
        )
        event_time_first_derivative = first_variation / event_speed
        time_derivative_variation = flow_lipschitz * first_variation
        event_time_second_derivative = (
            second_fixed_time_variation
            + 2
            * time_derivative_variation
            * event_time_first_derivative
            + acceleration * event_time_first_derivative**2
        ) / event_speed
        return_second_derivative = (
            second_fixed_time_variation
            + 2
            * time_derivative_variation
            * event_time_first_derivative
            + acceleration * event_time_first_derivative**2
            + perturbed_flow_speed * event_time_second_derivative
        )
        derivative_increment = return_second_derivative * radius
        nonlinear_return_lipschitz = q + derivative_increment
        nonlinear_map_remainder = (
            return_second_derivative * radius**2 / 2
        )
        return_image_radius = nonlinear_return_lipschitz * radius
        event_time_shift = event_time_first_derivative * radius
        full_return_deviation = (
            flow_deviation + exact_orbit_speed * event_time_shift
        )
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        contraction_margin = 1 - nonlinear_return_lipschitz
        self_map_margin = radius - return_image_radius
        event_bracket_margin = period_lower / PHASE_CELL_COUNT - event_time_shift
        full_history_margin = full_radius - full_return_deviation
        returned_history_start = (
            period_lower * (PHASE_CELL_COUNT - 1) / PHASE_CELL_COUNT
            - 5 * _point(5, precision).sqrt().upper
        )
    if min(
        contraction_margin,
        self_map_margin,
        event_bracket_margin,
        full_history_margin,
        returned_history_start,
    ) <= 0:
        raise ArithmeticError("the Stage-6A nonlinear return tube did not close")

    attachment_history = _mapping(
        attachment.get("history_ball"), "J=.32 attachment history ball"
    )
    attachment_distance = _upper_decimal(
        attachment_history.get("complete_history_distance_upper")
    )
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        attachment_to_section_radius_ratio = attachment_distance / radius
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        optimistic_entry_gap = attachment_distance - radius
        attachment_hessian_threshold = (1 - q) / attachment_distance
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        hessian_gap_factor = (
            return_second_derivative / attachment_hessian_threshold
        )
        hessian_base10_order_gap = gmpy2.log10(hessian_gap_factor)

    return {
        "reduced_history_space": (
            "Y=C([-5*sqrt(5),0],R)_v x R_w(0), max norm, with section "
            "h_v(0)=0"
        ),
        "complete_history_space": (
            "X=C([-5*sqrt(5),0],R^2), max component norm"
        ),
        "local_section_semantics": (
            "a hit means the affine voltage section together with membership "
            "in the radius-r reduced disk; the opposite-orientation global "
            "voltage-level crossing is outside this local disk"
        ),
        "section_radius": SECTION_RADIUS,
        "complete_history_tube_radius": COMPLETE_HISTORY_TUBE_RADIUS,
        "parent_local_field_domain_radius": decimal_upper(
            declared_parent_radius, 70
        ),
        "parent_voltage_strip_margin_lower": decimal_lower(
            strip_margin, 70
        ),
        "full_tube_inside_parent_field_domain": True,
        "stage3i_voltage_linear_row_upper": decimal_upper(q_v, 70),
        "stage3i_recovery_linear_row_upper": decimal_upper(q_w, 70),
        "linear_return_norm_upper": decimal_upper(q, 70),
        "linear_margin_below_one_lower": decimal_lower(1 - q, 70),
        "fast_field_lipschitz_row_sum_upper": decimal_upper(
            fast_lipschitz, 70
        ),
        "full_reduced_flow_lipschitz_upper": decimal_upper(
            flow_lipschitz, 70
        ),
        "field_quadratic_remainder_coefficient_upper": decimal_upper(
            field_quadratic_remainder, 70
        ),
        "field_second_derivative_norm_upper": decimal_upper(
            field_second_derivative, 70
        ),
        "exact_period_lower": decimal_lower(period_lower, 70),
        "exact_period_upper": decimal_upper(period_upper, 70),
        "event_horizon_upper": decimal_upper(horizon, 70),
        "uniform_flow_gain_upper": decimal_upper(flow_gain, 70),
        "uniform_flow_deviation_upper": decimal_upper(flow_deviation, 70),
        "uniform_flow_ball_margin_lower": decimal_lower(
            full_radius - flow_deviation, 70
        ),
        "exact_base_wrap_speed_lower": decimal_lower(base_speed, 70),
        "perturbed_event_speed_lower": decimal_lower(event_speed, 70),
        "event_endpoint_sign_margin_lower": decimal_lower(
            event_sign_margin, 70
        ),
        "middle_no_earlier_local_hit_margin_lower": decimal_lower(
            no_earlier_margin, 70
        ),
        "first_variation_flow_bound_upper": decimal_upper(
            first_variation, 70
        ),
        "second_fixed_time_variation_bound_upper": decimal_upper(
            second_fixed_time_variation, 70
        ),
        "event_time_first_derivative_upper": decimal_upper(
            event_time_first_derivative, 70
        ),
        "event_time_second_derivative_upper": decimal_upper(
            event_time_second_derivative, 70
        ),
        "return_second_derivative_upper": decimal_upper(
            return_second_derivative, 70
        ),
        "nonlinear_derivative_increment_upper": decimal_upper(
            derivative_increment, 70
        ),
        "nonlinear_map_quadratic_remainder_upper": decimal_upper(
            nonlinear_map_remainder, 70
        ),
        "nonlinear_return_lipschitz_upper": decimal_upper(
            nonlinear_return_lipschitz, 70
        ),
        "strict_contraction_margin_lower": decimal_lower(
            contraction_margin, 70
        ),
        "return_image_radius_upper": decimal_upper(
            return_image_radius, 70
        ),
        "strict_self_map_margin_lower": decimal_lower(self_map_margin, 70),
        "event_time_shift_upper": decimal_upper(event_time_shift, 70),
        "event_bracket_margin_lower": decimal_lower(
            event_bracket_margin, 70
        ),
        "returned_history_window_after_initial_time_lower": decimal_lower(
            returned_history_start, 70
        ),
        "full_return_history_deviation_upper": decimal_upper(
            full_return_deviation, 70
        ),
        "full_history_invariance_margin_lower": decimal_lower(
            full_history_margin, 70
        ),
        "event_phase_map": {
            "domain": "the exact radius-1e-335 reduced local section disk",
            "event_window": "normalized phase [255/256,257/256]",
            "orientation": "positive current-voltage speed",
            "unique_root": True,
            "c2_implicit_map": True,
            "no_earlier_local_section_hit": True,
        },
        "complete_history_invariance": {
            "future_factorization": (
                "future voltage and recovery depend only on the voltage "
                "history and current recovery"
            ),
            "initial_complete_recovery_history_radius": (
                COMPLETE_HISTORY_TUBE_RADIUS
            ),
            "returned_window_entirely_at_positive_time": True,
            "one_return_maps_tube_to_itself": True,
            "iterated_flow_sweeps_remain_in_tube": True,
        },
        "J_0p32_attachment_audit": {
            "directed_complete_history_distance_upper": decimal_upper(
                attachment_distance, 70
            ),
            "distance_to_section_radius_ratio_lower": decimal_lower(
                attachment_to_section_radius_ratio, 70
            ),
            "optimistic_distance_minus_section_radius_lower": decimal_lower(
                optimistic_entry_gap, 70
            ),
            "required_C_P_for_r_equal_distance_strict_upper_threshold_lower": (
                decimal_lower(attachment_hessian_threshold, 70)
            ),
            "required_C_P_formula": "C_P < (1-q_stage3i)/d_J032",
            "current_C_P_to_required_threshold_ratio_upper": decimal_upper(
                hessian_gap_factor, 70
            ),
            "current_C_P_base10_order_gap_upper": decimal_upper(
                hessian_base10_order_gap, 70
            ),
            "same_exact_section_parent_gate": False,
            "inside_stage6a_phase_chart_domain": False,
            "first_failed_gate": (
                "ambient-to-section domain containment: the directed J=.32 "
                "history distance is vastly larger than the Stage-6A "
                "section radius, before any capture inference"
            ),
            "outer_capture_closes": False,
        },
        "uniform_flow_ball_closes": True,
        "event_phase_map_closes": True,
        "no_earlier_local_hit_closes": True,
        "full_history_invariance_closes": True,
        "nonlinear_return_contraction_closes": True,
        "biological_attachment_closes": False,
    }


def _validated_parents(repository: Path) -> dict[str, Any]:
    stage3i_payload = _load_bound_json(
        repository, STAGE3I_RESULT_RELATIVE_PATH, STAGE3I_RESULT_SHA256
    )
    outer_payload = _load_bound_json(
        repository, OUTER_RESULT_RELATIVE_PATH, OUTER_RESULT_SHA256
    )
    floquet_payload = _load_bound_json(
        repository, FLOQUET_RESULT_RELATIVE_PATH, FLOQUET_RESULT_SHA256
    )
    routing_payload = _load_bound_json(
        repository, ROUTING_RESULT_RELATIVE_PATH, ROUTING_RESULT_SHA256
    )
    attachment_payload = _load_bound_json(
        repository, ATTACHMENT_RESULT_RELATIVE_PATH, ATTACHMENT_RESULT_SHA256
    )
    _validate_outer_signed_density_stage3i_tv_result(
        stage3i_payload, repository, replay_numerics=False
    )
    orbit = validate_outer_high_resolution_artifact(
        outer_payload, repository, replay_directed=False
    )
    validate_leaky_floquet_transfer_artifact(
        floquet_payload, repository, recompute=False
    )
    validate_outer_two_sided_routing_result(routing_payload, repository)
    validate_third_return_result(
        attachment_payload, repository, recompute=False
    )
    return {
        "stage3i_payload": stage3i_payload,
        "outer_payload": outer_payload,
        "floquet_payload": floquet_payload,
        "routing_payload": routing_payload,
        "attachment_payload": attachment_payload,
        "orbit": orbit,
    }


@lru_cache(maxsize=1)
def build_stage6a_certificate(repository: Path) -> dict[str, Any]:
    repository = Path(repository).resolve()
    if os.environ.get("OPENBLAS_NUM_THREADS") != "1":
        raise RuntimeError("Stage 6A requires OPENBLAS_NUM_THREADS=1")
    if os.environ.get("OMP_NUM_THREADS") != "1":
        raise RuntimeError("Stage 6A requires OMP_NUM_THREADS=1")
    parents = _validated_parents(repository)
    stage3i_certificate = _mapping(
        parents["stage3i_payload"].get("certificate"), "Stage-3I certificate"
    )
    routing_contract = _mapping(
        parents["routing_payload"].get("contract"), "routing contract"
    )
    attachment_certificate = _mapping(
        parents["attachment_payload"].get("certificate"),
        "attachment certificate",
    )
    outer_artifact = _mapping(
        parents["outer_payload"].get("artifact"), "outer artifact"
    )
    correction = _mapping(
        _mapping(
            _mapping(
                outer_artifact.get("directed_radii_certificate"),
                "outer directed certificate",
            ).get("validation"),
            "outer validation",
        ).get("correction"),
        "outer correction",
    )
    orbit_correction = _upper_decimal(correction.get("chosen_radius"))
    attachment_correction = _mapping(
        attachment_certificate.get("exact_outer_orbit_correction"),
        "attachment orbit correction",
    )
    exact_history_correction = _upper_decimal(
        attachment_correction.get("exact_outer_orbit_history_correction_upper")
    )
    history_correction_formula = str(attachment_correction.get("formula"))
    if history_correction_formula != (
        "E_orbit=R_A+||dz_*/dx||*tau_max*R_T/"
        "(T_bar*(T_bar-R_T))"
    ):
        raise ValueError("the exact outer period/history transfer changed")
    local_field = _mapping(
        routing_contract.get("outer_local_vector_field_evidence"),
        "routing local field",
    )
    centered_voltage = _upper_decimal(
        local_field.get("exact_outer_centered_voltage_abs_upper")
    )
    full_radius = _upper_decimal(COMPLETE_HISTORY_TUBE_RADIUS)
    epsilon = _upper_decimal(EPSILON)
    kappa_1 = _upper_decimal(KAPPA_1)
    kappa_3 = _upper_decimal(KAPPA_3)
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
        strip = centered_voltage + full_radius
        fast_lipschitz = (
            2
            + (1 + strip) ** 2
            + 2 * epsilon * kappa_1
            + 6 * epsilon * kappa_3 * strip**2
        )
    phase_cover = _directed_phase_cover(
        parents["orbit"],
        orbit_correction,
        exact_history_correction,
        fast_lipschitz,
        history_correction_formula,
    )
    tube = _analytic_tube(
        orbit=parents["orbit"],
        routing=routing_contract,
        stage3i=stage3i_certificate,
        attachment=attachment_certificate,
        phase_cover=phase_cover,
    )
    claims = {name: True for name in TRUE_FLAGS}
    claims.update({name: False for name in FALSE_FLAGS})
    return {
        "schema_id": SCHEMA_ID,
        "model_id": MODEL_ID,
        "branch": BRANCH,
        "arithmetic_scope": ARITHMETIC_SCOPE,
        "parent_result_sha256": dict(PARENT_SHA256),
        "phase_cover": phase_cover,
        "nonlinear_return_tube": tube,
        "claim_status": claims,
        "theorem_statement": (
            "On the exact outer phase-zero reduced section, the radius-1e-335 "
            "ball has a unique next positive local-section return, no earlier "
            "local-section hit, a C2 event phase map, and a strictly "
            "contractive nonlinear return.  Its compatible complete-history "
            "flow sweep is forward invariant inside radius 0.001.  The "
            "directed J=.32 attachment lies far outside the phase-chart "
            "domain, so no pulse capture, two-sided routing, or onset follows."
        ),
        "conclusion": (
            "Stage 6A closes a nonzero source-bound nonlinear outer return "
            "tube, but the generic Gronwall/Hessian estimate makes its "
            "section radius 1e-335; the first biological failure is "
            "ambient-to-section entry, not linear contraction"
        ),
    }


def build_stage6a_result(repository: Path) -> dict[str, Any]:
    repository = Path(repository).resolve()
    certificate = build_stage6a_certificate(repository)
    digest = canonical_sha256(certificate)
    return {
        "certificate": certificate,
        "manifest": {
            "schema_id": SCHEMA_ID,
            "result": RESULT_RELATIVE_PATH,
            "default_command": DEFAULT_COMMAND,
            "environment": _environment(),
            "parent_result_sha256": dict(PARENT_SHA256),
            "source_sha256": {
                relative: _sha256_path(repository / relative)
                for relative in SOURCE_MANIFEST
            },
            "numeric_core_sha256": digest,
            "certificate_sha256": digest,
        },
    }


def _validate_numeric_claims(certificate: Mapping[str, Any]) -> None:
    if set(certificate) != {
        "schema_id",
        "model_id",
        "branch",
        "arithmetic_scope",
        "parent_result_sha256",
        "phase_cover",
        "nonlinear_return_tube",
        "claim_status",
        "theorem_statement",
        "conclusion",
    }:
        raise ValueError("the Stage-6A certificate schema changed")
    if (
        certificate.get("schema_id") != SCHEMA_ID
        or certificate.get("model_id") != MODEL_ID
        or certificate.get("branch") != BRANCH
        or certificate.get("arithmetic_scope") != ARITHMETIC_SCOPE
    ):
        raise ValueError("the Stage-6A identity changed")
    if certificate.get("parent_result_sha256") != PARENT_SHA256:
        raise ValueError("the Stage-6A parent map changed")
    claims = _mapping(certificate.get("claim_status"), "Stage-6A claims")
    if set(claims) != set(TRUE_FLAGS) | set(FALSE_FLAGS):
        raise ValueError("the Stage-6A claim ledger changed")
    if any(claims.get(name) is not True for name in TRUE_FLAGS):
        raise ValueError("a proved Stage-6A claim was removed")
    if any(claims.get(name) is not False for name in FALSE_FLAGS):
        raise ValueError("an open biological claim was promoted")
    phase = _mapping(certificate.get("phase_cover"), "Stage-6A phase cover")
    if not (
        phase.get("normalized_phase_cell_count") == PHASE_CELL_COUNT
        and phase.get("middle_phase_cell_count") == PHASE_CELL_COUNT - 2
        and phase.get("all_middle_cells_separated") is True
        and phase.get("both_wrap_cells_strictly_positive") is True
        and phase.get("period_correction_included_in_exact_history_transfer")
        is True
        and _lower_decimal(
            phase.get("exact_middle_current_state_separation_lower")
        )
        > 0
        and _lower_decimal(phase.get("exact_wrap_fast_speed_lower")) > 0
    ):
        raise ValueError("the Stage-6A phase cover no longer closes")
    tube = _mapping(
        certificate.get("nonlinear_return_tube"), "Stage-6A return tube"
    )
    for gate in (
        "uniform_flow_ball_closes",
        "event_phase_map_closes",
        "no_earlier_local_hit_closes",
        "full_history_invariance_closes",
        "nonlinear_return_contraction_closes",
    ):
        if tube.get(gate) is not True:
            raise ValueError(f"the Stage-6A gate {gate} opened")
    if tube.get("biological_attachment_closes") is not False:
        raise ValueError("Stage 6A invented a biological attachment")
    if tube.get("full_tube_inside_parent_field_domain") is not True:
        raise ValueError("the Stage-6A tube left the parent field domain")
    if _upper_decimal(tube.get("nonlinear_return_lipschitz_upper")) >= 1:
        raise ValueError("the Stage-6A nonlinear contraction was lost")
    if _lower_decimal(tube.get("strict_self_map_margin_lower")) <= 0:
        raise ValueError("the Stage-6A self-map margin was lost")
    if _lower_decimal(tube.get("full_history_invariance_margin_lower")) <= 0:
        raise ValueError("the Stage-6A complete-history margin was lost")
    attachment = _mapping(
        tube.get("J_0p32_attachment_audit"), "Stage-6A attachment audit"
    )
    if not (
        attachment.get("inside_stage6a_phase_chart_domain") is False
        and attachment.get("outer_capture_closes") is False
        and _lower_decimal(
            attachment.get("optimistic_distance_minus_section_radius_lower")
        )
        > 0
        and _lower_decimal(
            attachment.get(
                "required_C_P_for_r_equal_distance_strict_upper_threshold_lower"
            )
        )
        > 0
        and _lower_decimal(
            attachment.get("current_C_P_to_required_threshold_ratio_upper")
        )
        > 1
    ):
        raise ValueError("the Stage-6A biological failure boundary changed")


def validate_stage6a_result(
    payload: Mapping[str, Any],
    repository: Path,
    *,
    recompute: bool = False,
) -> None:
    repository = Path(repository).resolve()
    if not isinstance(payload, Mapping) or set(payload) != {
        "certificate",
        "manifest",
    }:
        raise ValueError("the Stage-6A result schema changed")
    certificate = _mapping(payload.get("certificate"), "Stage-6A certificate")
    manifest = _mapping(payload.get("manifest"), "Stage-6A manifest")
    if set(manifest) != {
        "schema_id",
        "result",
        "default_command",
        "environment",
        "parent_result_sha256",
        "source_sha256",
        "numeric_core_sha256",
        "certificate_sha256",
    }:
        raise ValueError("the Stage-6A manifest schema changed")
    if (
        manifest.get("schema_id") != SCHEMA_ID
        or manifest.get("result") != RESULT_RELATIVE_PATH
        or manifest.get("default_command") != DEFAULT_COMMAND
    ):
        raise ValueError("the Stage-6A manifest identity changed")
    _validate_numeric_claims(certificate)
    digest = canonical_sha256(certificate)
    if (
        manifest.get("certificate_sha256") != digest
        or manifest.get("numeric_core_sha256") != digest
    ):
        raise ValueError("the Stage-6A certificate digest changed")
    if (
        EXPECTED_NUMERIC_CORE_SHA256 != "TO_BE_FILLED"
        and digest != EXPECTED_NUMERIC_CORE_SHA256
    ):
        raise ValueError("the Stage-6A frozen numeric core changed")
    if manifest.get("environment") != _environment():
        raise ValueError("the Stage-6A runtime environment changed")
    if manifest.get("parent_result_sha256") != PARENT_SHA256:
        raise ValueError("the Stage-6A manifest parent map changed")
    sources = _mapping(manifest.get("source_sha256"), "Stage-6A sources")
    if set(sources) != set(SOURCE_MANIFEST):
        raise ValueError("the Stage-6A source set changed")
    for relative in SOURCE_MANIFEST:
        if sources.get(relative) != _sha256_path(repository / relative):
            raise ValueError(f"a Stage-6A source changed: {relative}")
    _validated_parents(repository)
    if recompute:
        build_stage6a_certificate.cache_clear()
        expected = build_stage6a_certificate(repository)
        if canonical_sha256(expected) != digest:
            raise ValueError("the Stage-6A fresh directed replay changed")


__all__ = [
    "ARITHMETIC_SCOPE",
    "DEFAULT_COMMAND",
    "EXPECTED_NUMERIC_CORE_SHA256",
    "FALSE_FLAGS",
    "NOTE_RELATIVE_PATH",
    "RESULT_RELATIVE_PATH",
    "SCHEMA_ID",
    "SOURCE_MANIFEST",
    "TRUE_FLAGS",
    "build_stage6a_certificate",
    "build_stage6a_result",
    "canonical_sha256",
    "validate_stage6a_result",
]
