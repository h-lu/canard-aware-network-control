"""Directed ``(a,kappa_3) -> (F,A)`` response for both leaky branches.

The parent parameter-box certificate already proves a phase-fixed periodic
orbit, a bordered inverse, and one simple voltage maximum and minimum for
each branch on the common parameter box.  This module does not construct a
new orbit inverse.  It reuses the parent's outward ``Y,Z_0,z_1,z_2,z_3``
majorants to close smaller nested balls and replays the parent's fixed
preconditioner only to validate the two first-sensitivity columns.

Here ``F=1/T`` is physical frequency in cycles per unit time and
``A=v(phi_max)-v(phi_min)`` is the unsquared physical voltage amplitude.
Only the response theorem is proved.  Pulse onset, a history separator,
network safety thresholds, and outer capture by a physical pulse remain
open.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from functools import lru_cache
from hashlib import sha256
import json
from pathlib import Path
import platform
from types import SimpleNamespace
from typing import Any, Mapping, Sequence

import gmpy2
import numpy as np
import scipy
import sympy as sp

from canard_control.directed_interval import (
    DirectedComplexInterval,
    DirectedInterval,
    decimal_lower,
    decimal_upper,
    pi_interval,
    upward_division,
    upward_sum,
)
from canard_control.fhn_periodic_parameter_box import (
    _preconditioned_sequence_upper,
)
from canard_control.fhn_periodic_directed_validation import (
    ComplexSequence,
    _complex_zero,
    _constant_sequence,
    _sequence_add,
    _sequence_convolution,
    _sequence_derivative,
    _sequence_scale,
    _sequence_shift,
    _sequence_sub,
    directed_dft,
)
from canard_control.fhn_periodic_infinite_validation import (
    _BaseSequences,
    _RealConjugateLayout,
    _box_abs_upper,
    _float_matrix_l1_upper,
    _sequence_box_norm_upper,
)
from canard_control.leaky_periodic_branch_artifact import (
    _collocation_system,
)
from canard_control.leaky_periodic_parameter_box import (
    _build_leaky_parameter_box_sequences,
    _candidate_fields,
    _evaluate_real_sequence,
    _validate_continuation,
    _variation_bounds,
)
from canard_control.leaky_periodic_parameter_response import (
    INNER_PARENT_RELATIVE_PATH,
    OUTER_PARENT_RELATIVE_PATH,
    RESULT_RELATIVE_PATH as PARAMETER_BOX_PARENT_RELATIVE_PATH,
    _load_parents,
    _matrix_from_records,
    _parameter_rhs,
    validate_parameter_response_artifact,
)


SCHEMA_ID = "leaky-periodic-directed-response-v1"
MODEL_ID = "autonomous-leaky-recovery-two-delay-fhn-bistable-proposal"
SOURCE_RELATIVE_PATH = (
    "src/canard_control/leaky_periodic_directed_response.py"
)
GENERATOR_RELATIVE_PATH = (
    "experiments/leaky_periodic_directed_response.py"
)
NOTE_RELATIVE_PATH = "docs/leaky-periodic-directed-response.md"
RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_periodic_directed_response.json"
)
DEFAULT_COMMAND = (
    "OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONPATH=src "
    "/usr/bin/python3 experiments/leaky_periodic_directed_response.py"
)
ARITHMETIC = (
    "160-bit outward-rounded MPFR Fourier/Wiener residual and response "
    "bounds; parent Y,Z0,z1,z2,z3 nested radii; parent bordered-inverse "
    "preconditioner replay with separate fast/slow input-block norms; "
    "direct interval 2x2 determinant, directed binary64 left-inverse "
    "formation audit, and uniform fixed-preconditioner target-ball test"
)

CONTROL_ORDER = ("unfolding_a", "kappa_3")
OUTPUT_ORDER = ("F=1/T", "A=v_max-v_min")
HALF_WIDTH_UNFOLDING_A = "1e-10"
HALF_WIDTH_KAPPA_3 = "1e-10"
PARENT_RADIUS = "1e-5"
PRECISION_BITS = 160
REFINEMENT_DENOMINATOR = 1 << 24

BRANCH_SETTINGS = {
    "inner_saddle_candidate": {
        "nested_radius": "1e-7",
        "cutoff": 192,
        "expected_determinant_sign": -1,
    },
    "outer_pulse": {
        "nested_radius": "1e-6",
        "cutoff": 384,
        "expected_determinant_sign": 1,
    },
}

TRUE_FLAGS = (
    "parent_parameter_box_validated",
    "parent_preconditioner_directed_replayed",
    "nested_radii_inequalities_validated",
    "exact_parameter_columns_validated",
    "directed_first_sensitivities_validated",
    "uniform_simple_extrema_reused",
    "unsquared_amplitude_derivative_validated",
    "directed_response_matrices_validated",
    "response_determinants_bounded_away_from_zero",
    "uniform_pointwise_local_diffeomorphisms_validated",
)

FALSE_FLAGS = (
    "new_periodic_orbit_or_inverse_validation_claimed",
    "physical_pulse_unique_onset_validated",
    "history_space_separator_validated",
    "network_safety_threshold_validated",
    "pulse_J_032_outer_capture_validated",
    "canard_root_equals_physical_onset_proved",
)

SOURCE_PATHS = {
    "source": SOURCE_RELATIVE_PATH,
    "generator": GENERATOR_RELATIVE_PATH,
    "note": NOTE_RELATIVE_PATH,
    "parameter_box_parent_source": (
        "src/canard_control/leaky_periodic_parameter_response.py"
    ),
    "leaky_parameter_box_source": (
        "src/canard_control/leaky_periodic_parameter_box.py"
    ),
    "fhn_d4_framework_source": (
        "src/canard_control/fhn_periodic_parameter_box.py"
    ),
    "periodic_candidate_source": (
        "src/canard_control/fhn_periodic_candidate.py"
    ),
    "inner_parent_source": (
        "src/canard_control/leaky_periodic_branch_artifact.py"
    ),
    "outer_parent_source": (
        "src/canard_control/leaky_outer_high_resolution.py"
    ),
    "leaky_validation_source": (
        "src/canard_control/leaky_periodic_validation.py"
    ),
    "infinite_validation_source": (
        "src/canard_control/fhn_periodic_infinite_validation.py"
    ),
    "directed_fourier_source": (
        "src/canard_control/fhn_periodic_directed_validation.py"
    ),
    "directed_interval_source": "src/canard_control/directed_interval.py",
}


@dataclass(frozen=True)
class NestedRadiiCertificate:
    """Strict child ball derived only from stored parent majorants."""

    parent_radius: str
    nested_radius: str
    residual_y_upper: str
    point_defect_z0_upper: str
    coefficient_z1_upper: str
    coefficient_z2_upper: str
    coefficient_z3_upper: str
    contraction_upper: str
    radii_left_upper: str
    radii_margin_lower: str
    global_preconditioner_l1_upper: str
    nested_bordered_inverse_norm_upper: str
    nested_radius_below_parent_radius: bool
    nested_radii_inequality_validated: bool
    same_parent_branch_by_uniqueness: bool


@dataclass(frozen=True)
class DirectedExtremumWindow:
    """Uniform refined location of one exact voltage extremum."""

    kind: str
    parent_phase_lower: str
    parent_phase_upper: str
    refined_phase_lower: str
    refined_phase_upper: str
    refinement_denominator: int
    left_derivative_lower: str
    left_derivative_upper: str
    right_derivative_lower: str
    right_derivative_upper: str
    parent_curvature_bound: str
    endpoint_signs_validated: bool
    parent_curvature_sign_reused: bool


@dataclass(frozen=True)
class DirectedSensitivityBudget:
    """Raw residual decomposition for one exact sensitivity column."""

    control: str
    center_period_derivative_binary64_hex: str
    bordered_solve_residual_upper: str
    base_preconditioned_residual_upper: str
    state_operator_variation_upper: str
    period_operator_variation_upper: str
    leaky_slow_row_variation_upper: str
    parameter_forcing_variation_upper: str
    total_raw_residual_upper: str
    fast_block_preconditioner_l1_upper: str
    slow_block_preconditioner_l1_upper: str
    preconditioned_variation_upper: str
    nested_contraction_upper: str
    exact_sensitivity_error_upper: str


@dataclass(frozen=True)
class DirectedResponseBranch:
    """Directed response and determinant theorem for one periodic branch."""

    branch: str
    cutoff: int
    precision_bits: int
    nested_radii: NestedRadiiCertificate
    maximum_window: DirectedExtremumWindow
    minimum_window: DirectedExtremumWindow
    maximum_center_derivative_error_upper: str
    output_frequency_lower: str
    output_frequency_upper: str
    output_amplitude_lower: str
    output_amplitude_upper: str
    sensitivities: tuple[DirectedSensitivityBudget, DirectedSensitivityBudget]
    response_lower: tuple[tuple[str, str], tuple[str, str]]
    response_upper: tuple[tuple[str, str], tuple[str, str]]
    response_midpoint_binary64_hex: (
        tuple[tuple[str, str], tuple[str, str]]
    )
    left_preconditioner_binary64_hex: (
        tuple[tuple[str, str], tuple[str, str]]
    )
    determinant_lower: str
    determinant_upper: str
    determinant_sign: int
    determinant_absolute_margin_lower: str
    response_frobenius_norm_upper: str
    smallest_singular_value_lower: str
    pointwise_inverse_2norm_upper: str
    left_preconditioner_formation_defect_upper: str
    left_preconditioner_2_to_infinity_norm_upper: str
    left_preconditioned_derivative_defect_upper: str
    quantitative_target_ball_radius_lower: str | None
    parameter_inverse_lipschitz_upper: str | None
    left_preconditioner_formation_audited: bool
    derivative_defect_uniform_on_common_parameter_box: bool
    exact_extremum_phase_terms_vanish: bool
    response_matrix_validated: bool
    determinant_nonzero_validated: bool
    pointwise_local_diffeomorphism_validated: bool
    quantitative_target_ball_validated: bool


@dataclass(frozen=True)
class LeakyPeriodicDirectedResponseCertificate:
    """Joint inner/outer directed response theorem."""

    schema_id: str
    model_id: str
    control_order: tuple[str, str]
    output_order: tuple[str, str]
    frequency_definition: str
    amplitude_definition: str
    target_ball_definition: str
    common_parameter_box: tuple[str, str]
    precision_bits: int
    exact_symbolic_zero_defect_count: int
    inner: DirectedResponseBranch
    outer: DirectedResponseBranch
    flagship_outer_target_ball_radius_lower: str | None
    flagship_outer_parameter_inverse_lipschitz_upper: str | None
    quantitative_common_target_ball_radius_lower: str | None
    common_parameter_inverse_lipschitz_upper: str | None
    theorem_statement: str
    parent_parameter_box_validated: bool
    parent_preconditioner_directed_replayed: bool
    nested_radii_inequalities_validated: bool
    exact_parameter_columns_validated: bool
    directed_first_sensitivities_validated: bool
    uniform_simple_extrema_reused: bool
    unsquared_amplitude_derivative_validated: bool
    directed_response_matrices_validated: bool
    response_determinants_bounded_away_from_zero: bool
    uniform_pointwise_local_diffeomorphisms_validated: bool
    quantitative_common_target_ball_validated: bool
    new_periodic_orbit_or_inverse_validation_claimed: bool
    physical_pulse_unique_onset_validated: bool
    history_space_separator_validated: bool
    network_safety_threshold_validated: bool
    pulse_J_032_outer_capture_validated: bool
    canard_root_equals_physical_onset_proved: bool


@dataclass(frozen=True)
class _RawVariationBudget:
    state: gmpy2.mpfr
    period: gmpy2.mpfr
    slow: gmpy2.mpfr
    forcing: gmpy2.mpfr
    fast_total: gmpy2.mpfr
    slow_total: gmpy2.mpfr
    total: gmpy2.mpfr


@dataclass(frozen=True)
class _BranchData:
    orbit: Any
    base: _BaseSequences
    layout: _RealConjugateLayout
    approximate_inverse: np.ndarray
    approximate_inverse_l1: gmpy2.mpfr
    global_preconditioner_l1: gmpy2.mpfr
    fast_block_preconditioner_l1: gmpy2.mpfr
    slow_block_preconditioner_l1: gmpy2.mpfr
    radius: DirectedInterval
    contraction: gmpy2.mpfr
    inverse_norm: gmpy2.mpfr
    variation: Any
    nested: NestedRadiiCertificate
    parent_extrema: Mapping[str, Any]
    parent_midpoint: np.ndarray


def _sha256_path(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


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


def _canonical_json(value: Any) -> str:
    """Normalize tuples to JSON arrays while preserving every JSON type."""

    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    )


def _point(value: str | int, precision: int) -> DirectedInterval:
    return DirectedInterval.from_decimal(value, precision)


def _symmetric(radius: gmpy2.mpfr, precision: int) -> DirectedInterval:
    positive = DirectedInterval.from_bounds(radius, radius, precision)
    if positive.lower < 0:
        raise ValueError("a symmetric radius must be nonnegative")
    negative = -positive
    return DirectedInterval.from_bounds(
        negative.lower, positive.upper, precision
    )


def _upper_decimal(value: object, precision: int, name: str) -> gmpy2.mpfr:
    if not isinstance(value, str):
        raise ValueError(f"{name} must be a decimal string")
    return DirectedInterval.from_decimal(value, precision).upper


@lru_cache(maxsize=1)
def exact_directed_response_defects() -> tuple[sp.Expr, ...]:
    """Exact signs of both residual columns and both output derivatives."""

    phase_v, phase_w, v, w, a, kappa_3 = sp.symbols(
        "Dphi_v Dphi_w v w a kappa_3", real=True
    )
    period, epsilon, cubic = sp.symbols(
        "T epsilon C", positive=True, real=True
    )
    period_q, sv_max, sv_min = sp.symbols(
        "T_q s_v_max s_v_min", real=True
    )
    maximum_phase_q, minimum_phase_q = sp.symbols(
        "phi_max_q phi_min_q", real=True
    )
    v_phase_max, v_phase_min = sp.symbols(
        "v_phase_max v_phase_min", real=True
    )
    slow_residual = phase_w - period * epsilon * (v - a - w)
    fast_parameter_part = -period * epsilon * kappa_3 * cubic
    frequency_derivative = -period_q / period**2
    amplitude_chain_rule = (
        sv_max
        + v_phase_max * maximum_phase_q
        - sv_min
        - v_phase_min * minimum_phase_q
    )
    return tuple(
        sp.simplify(item)
        for item in (
            sp.diff(slow_residual, a) - period * epsilon,
            sp.diff(fast_parameter_part, kappa_3)
            + period * epsilon * cubic,
            -sp.diff(slow_residual, a) + period * epsilon,
            -sp.diff(fast_parameter_part, kappa_3)
            - period * epsilon * cubic,
            sp.diff(1 / period, period) * period_q
            - frequency_derivative,
            amplitude_chain_rule.subs(
                {v_phase_max: 0, v_phase_min: 0}
            )
            - (sv_max - sv_min),
        )
    )


def _nested_radii(
    continuation: Mapping[str, Any], nested_radius: str, precision: int
) -> tuple[NestedRadiiCertificate, DirectedInterval, gmpy2.mpfr, gmpy2.mpfr]:
    if continuation.get("chosen_radius") != PARENT_RADIUS:
        raise ValueError("the parent continuation radius changed")
    parent = _point(PARENT_RADIUS, precision)
    radius = _point(nested_radius, precision)
    if radius.upper >= parent.lower:
        raise ArithmeticError("the response radius is not nested")
    names = {
        "y": "preconditioned_box_residual_upper",
        "z0": "full_point_defect_upper",
        "z1": "coefficient_z1_upper",
        "z2": "coefficient_z2_upper",
        "z3": "coefficient_z3_upper",
        "preconditioner": "global_preconditioner_l1_upper",
    }
    values = {
        key: _upper_decimal(continuation.get(field), precision, field)
        for key, field in names.items()
    }
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        contraction = (
            values["z0"]
            + values["z1"] * radius.upper
            + values["z2"] * radius.upper * radius.upper
            + values["z3"]
            * radius.upper
            * radius.upper
            * radius.upper
        )
        radii_left = values["y"] + contraction * radius.upper
        inverse_norm = values["preconditioner"] / (1 - contraction)
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        margin = radius.lower - radii_left
    validated = contraction < 1 and margin > 0
    if not validated:
        raise ArithmeticError("a nested response radius did not close")
    certificate = NestedRadiiCertificate(
        parent_radius=PARENT_RADIUS,
        nested_radius=nested_radius,
        residual_y_upper=decimal_upper(values["y"]),
        point_defect_z0_upper=decimal_upper(values["z0"]),
        coefficient_z1_upper=decimal_upper(values["z1"]),
        coefficient_z2_upper=decimal_upper(values["z2"]),
        coefficient_z3_upper=decimal_upper(values["z3"]),
        contraction_upper=decimal_upper(contraction),
        radii_left_upper=decimal_upper(radii_left),
        radii_margin_lower=decimal_lower(margin),
        global_preconditioner_l1_upper=decimal_upper(
            values["preconditioner"]
        ),
        nested_bordered_inverse_norm_upper=decimal_upper(inverse_norm),
        nested_radius_below_parent_radius=True,
        nested_radii_inequality_validated=True,
        same_parent_branch_by_uniqueness=True,
    )
    return certificate, radius, contraction, inverse_norm


def _phase_pairing(
    base: _BaseSequences,
    voltage: Mapping[int, DirectedComplexInterval],
    recovery: Mapping[int, DirectedComplexInterval],
) -> DirectedComplexInterval:
    precision = base.period.precision
    zero = _complex_zero(precision)
    result = zero
    for mode, value in voltage.items():
        result += base.phase_voltage.get(-mode, zero) * value
    for mode, value in recovery.items():
        result += base.phase_recovery.get(-mode, zero) * value
    return result


def _floating_sensitivities(
    orbit: Any, precision: int
) -> tuple[
    tuple[ComplexSequence, ComplexSequence, DirectedInterval],
    tuple[ComplexSequence, ComplexSequence, DirectedInterval],
]:
    # Passing the center state itself as the phase reference reproduces the
    # phase row used by the parent Fourier/Wiener bordered operator.
    _, jacobian = _collocation_system(
        orbit.state, orbit.period, orbit.parameters, orbit.state
    )
    rhs, _ = _parameter_rhs(orbit)
    sensitivities = np.linalg.solve(jacobian, rhs)
    count = len(orbit.state)
    result = []
    for column in range(2):
        result.append(
            (
                directed_dft(sensitivities[:count, column], precision),
                directed_dft(
                    sensitivities[count : 2 * count, column], precision
                ),
                DirectedInterval.from_float(
                    float(sensitivities[-1, column]), precision
                ),
            )
        )
    return result[0], result[1]


def _sensitivity_residual(
    base: _BaseSequences,
    sensitivity: tuple[ComplexSequence, ComplexSequence, DirectedInterval],
    control_index: int,
) -> tuple[ComplexSequence, ComplexSequence, DirectedComplexInterval]:
    """Enclose ``J_box(x_bar)s_bar + F_q(x_bar)``."""

    precision = base.period.precision
    sv, sw, st = sensitivity
    local = _sequence_sub(
        _sequence_convolution(base.current_coefficient, sv), sw
    )
    for tau, coefficient in zip(
        (base.parameters["tau_0"], base.parameters["tau_1"]),
        base.delayed_coefficients,
        strict=True,
    ):
        local = _sequence_add(
            local,
            _sequence_convolution(
                coefficient, _sequence_shift(sv, tau / base.period)
            ),
        )
    fast = _sequence_sub(
        _sequence_derivative(sv, precision),
        _sequence_scale(local, base.period),
    )
    fast = _sequence_add(fast, _sequence_scale(base.period_voltage, st))
    slow = _sequence_sub(
        _sequence_derivative(sw, precision),
        _sequence_scale(
            _sequence_sub(sv, sw),
            base.period * base.parameters["epsilon"],
        ),
    )
    slow = _sequence_add(slow, _sequence_scale(base.period_recovery, st))
    cubic, _ = _candidate_fields(base)
    if control_index == 0:
        # F_a=(0,+T epsilon 1,0).
        slow = _sequence_add(
            slow,
            _constant_sequence(
                base.period * base.parameters["epsilon"], precision
            ),
        )
    elif control_index == 1:
        # F_kappa3=(-T epsilon C,0,0).
        fast = _sequence_sub(
            fast,
            _sequence_scale(
                cubic, base.period * base.parameters["epsilon"]
            ),
        )
    else:
        raise ValueError("the response has exactly two control columns")
    return fast, slow, _phase_pairing(base, sv, sw)


def _raw_residual_norm(
    residual: tuple[ComplexSequence, ComplexSequence, DirectedComplexInterval],
    precision: int,
) -> gmpy2.mpfr:
    fast, slow, phase = residual
    return upward_sum(
        [
            _sequence_box_norm_upper(fast, precision),
            _sequence_box_norm_upper(slow, precision),
            _box_abs_upper(phase),
        ],
        precision,
    )


def _sequence_derivative_norm(
    sequence: Mapping[int, DirectedComplexInterval], precision: int
) -> gmpy2.mpfr:
    return _sequence_box_norm_upper(
        _sequence_derivative(sequence, precision), precision
    )


def _raw_sensitivity_variation(
    data: _BranchData,
    sensitivity: tuple[ComplexSequence, ComplexSequence, DirectedInterval],
    control_index: int,
) -> _RawVariationBudget:
    """Bound the exact-operator and parameter-forcing variations."""

    base = data.base
    variation = data.variation
    precision = base.period.precision
    rho = data.radius.upper
    epsilon = base.parameters["epsilon"].upper
    sigma = _point(2, precision).sqrt().upper
    minimum_period = (base.period - data.radius).lower
    maximum_period = (base.period + data.radius).upper
    sv, sw, st_interval = sensitivity
    st = st_interval.upper_abs()
    sv_norm = _sequence_box_norm_upper(sv, precision)
    sw_norm = _sequence_box_norm_upper(sw, precision)
    dsv_norm = _sequence_derivative_norm(sv, precision)
    cubic, _ = _candidate_fields(base)
    cubic_norm = _sequence_box_norm_upper(cubic, precision)
    delayed_coefficient_norms = tuple(
        _sequence_box_norm_upper(item, precision)
        for item in base.delayed_coefficients
    )

    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        alpha_changes = []
        shifted_state_changes = []
        shifted_derivative_changes = []
        second_derivative_norm = _sequence_derivative_norm(
            base.phase_voltage, precision
        )
        for tau in (base.parameters["tau_0"], base.parameters["tau_1"]):
            alpha_change = (
                tau.upper
                * rho
                / (minimum_period * base.period.lower)
            )
            alpha_changes.append(alpha_change)
            shifted_state_changes.append(
                sigma * dsv_norm * alpha_change
            )
            shifted_derivative_changes.append(
                sigma * variation.derivative_error
                + sigma * second_derivative_norm * alpha_change
            )

        local_center_norm = (
            _sequence_box_norm_upper(
                base.current_coefficient, precision
            )
            * sv_norm
            + sw_norm
            + sum(
                coefficient_norm * sigma * sv_norm
                for coefficient_norm in delayed_coefficient_norms
            )
        )
        local_difference = (
            variation.current_coefficient_difference * sv_norm
        )
        for coefficient_norm, coefficient_change, shift_change in zip(
            delayed_coefficient_norms,
            variation.delayed_coefficient_differences,
            shifted_state_changes,
            strict=True,
        ):
            local_difference += (
                coefficient_change * sigma * sv_norm
                + (coefficient_norm + coefficient_change) * shift_change
            )
        state_part = rho * local_center_norm + maximum_period * local_difference

        period_column_difference = variation.field_difference
        derivative_voltage_norm = _sequence_box_norm_upper(
            base.phase_voltage, precision
        )
        for (
            tau,
            coefficient_norm,
            coefficient_change,
            shifted_change,
            alpha_change,
        ) in zip(
            (base.parameters["tau_0"], base.parameters["tau_1"]),
            delayed_coefficient_norms,
            variation.delayed_coefficient_differences,
            shifted_derivative_changes,
            alpha_changes,
            strict=True,
        ):
            alpha_maximum = tau.upper / minimum_period
            period_column_difference += (
                alpha_change
                * coefficient_norm
                * sigma
                * derivative_voltage_norm
                + alpha_maximum
                * (
                    coefficient_change
                    * sigma
                    * derivative_voltage_norm
                    + (coefficient_norm + coefficient_change)
                    * shifted_change
                )
            )
        period_part = st * period_column_difference

        # For w'=epsilon(v-a-w), changing T contributes
        # epsilon*rho*(||s_v||+||s_w||), and changing the period column
        # contributes 2*epsilon*rho*|s_T|.  The extra s_w term is the leaky
        # recovery correction absent from the nonleaky D4 formula.
        slow_part = epsilon * rho * (sv_norm + sw_norm) + (
            2 * st * epsilon * rho
        )
        if control_index == 0:
            # F_a=(0,T epsilon,0) varies only through T.
            forcing_part = epsilon * rho
        elif control_index == 1:
            # F_kappa3=(-T epsilon C,0,0).
            forcing_part = epsilon * (
                rho * cubic_norm
                + maximum_period * variation.cubic_field_difference
            )
        else:
            raise ValueError("the response has exactly two control columns")
        fast_total = state_part + period_part
        slow_total = slow_part
        if control_index == 0:
            slow_total += forcing_part
        else:
            fast_total += forcing_part
        total = state_part + period_part + slow_part + forcing_part
    return _RawVariationBudget(
        state=state_part,
        period=period_part,
        slow=slow_part,
        forcing=forcing_part,
        fast_total=fast_total,
        slow_total=slow_total,
        total=total,
    )


def _derivative_interval(
    data: _BranchData, phase: DirectedInterval
) -> DirectedInterval:
    center = _evaluate_real_sequence(data.base.phase_voltage, phase)
    return center + _symmetric(
        data.variation.derivative_error, phase.precision
    )


def _refined_extremum_window(
    data: _BranchData,
    *,
    kind: str,
    center_phase: float,
) -> tuple[DirectedExtremumWindow, DirectedInterval]:
    """Find a dyadic uniform sign bracket inside the proved parent window."""

    precision = data.base.period.precision
    extrema = data.parent_extrema
    if kind == "maximum":
        parent_lower_text = extrema["maximum_phase_lower"]
        parent_upper_text = extrema["maximum_phase_upper"]
        curvature = extrema["maximum_curvature_upper"]
        left_positive = True
    elif kind == "minimum":
        parent_lower_text = extrema["minimum_phase_lower"]
        parent_upper_text = extrema["minimum_phase_upper"]
        curvature = extrema["minimum_curvature_lower"]
        left_positive = False
    else:
        raise ValueError("an extremum is a maximum or minimum")
    parent_lower = _point(parent_lower_text, precision).lower
    parent_upper = _point(parent_upper_text, precision).upper
    curvature_interval = _point(curvature, precision)
    if parent_lower >= parent_upper:
        raise ArithmeticError("a parent extremum window is empty")
    if (
        kind == "maximum" and curvature_interval.upper >= 0
    ) or (
        kind == "minimum" and curvature_interval.lower <= 0
    ):
        raise ArithmeticError("the inherited curvature sign is not strict")
    denominator = REFINEMENT_DENOMINATOR
    center_index = int(np.floor(center_phase * denominator))

    def evaluate(half_steps: int) -> tuple[
        DirectedInterval,
        DirectedInterval,
        DirectedInterval,
        DirectedInterval,
    ] | None:
        left_index = center_index - half_steps
        right_index = center_index + half_steps + 1
        left = _point(left_index, precision) / _point(denominator, precision)
        right = _point(right_index, precision) / _point(denominator, precision)
        if left.lower < parent_lower or right.upper > parent_upper:
            return None
        left_value = _derivative_interval(data, left)
        right_value = _derivative_interval(data, right)
        return left, right, left_value, right_value

    half_steps = 1
    last_failure = 0
    successful = None
    while True:
        trial = evaluate(half_steps)
        if trial is None:
            raise ArithmeticError("no refined extremum sign bracket closed")
        _, _, left_value, right_value = trial
        signs = (
            left_value.lower > 0 and right_value.upper < 0
            if left_positive
            else left_value.upper < 0 and right_value.lower > 0
        )
        if signs:
            successful = trial
            break
        last_failure = half_steps
        half_steps *= 2

    lower_steps = last_failure + 1
    upper_steps = half_steps
    while lower_steps < upper_steps:
        middle = (lower_steps + upper_steps) // 2
        trial = evaluate(middle)
        if trial is None:
            upper_steps = middle
            continue
        _, _, left_value, right_value = trial
        signs = (
            left_value.lower > 0 and right_value.upper < 0
            if left_positive
            else left_value.upper < 0 and right_value.lower > 0
        )
        if signs:
            upper_steps = middle
            successful = trial
        else:
            lower_steps = middle + 1
    successful = evaluate(upper_steps)
    if successful is None:
        raise ArithmeticError("the extremum bracket vanished")
    left, right, left_value, right_value = successful
    phase = DirectedInterval.from_bounds(left.lower, right.upper, precision)
    certificate = DirectedExtremumWindow(
        kind=kind,
        parent_phase_lower=parent_lower_text,
        parent_phase_upper=parent_upper_text,
        refined_phase_lower=decimal_lower(phase.lower),
        refined_phase_upper=decimal_upper(phase.upper),
        refinement_denominator=denominator,
        left_derivative_lower=decimal_lower(left_value.lower),
        left_derivative_upper=decimal_upper(left_value.upper),
        right_derivative_lower=decimal_lower(right_value.lower),
        right_derivative_upper=decimal_upper(right_value.upper),
        parent_curvature_bound=curvature,
        endpoint_signs_validated=True,
        parent_curvature_sign_reused=True,
    )
    return certificate, phase


def _interval_matrix_bounds(
    matrix: Sequence[Sequence[DirectedInterval]],
) -> tuple[
    tuple[tuple[str, str], tuple[str, str]],
    tuple[tuple[str, str], tuple[str, str]],
]:
    lower = tuple(
        tuple(decimal_lower(item.lower) for item in row) for row in matrix
    )
    upper = tuple(
        tuple(decimal_upper(item.upper) for item in row) for row in matrix
    )
    return lower, upper  # type: ignore[return-value]


def _matrix_product_defect_upper(
    left: np.ndarray,
    right: Sequence[Sequence[DirectedInterval]],
    precision: int,
) -> gmpy2.mpfr:
    row_bounds = []
    for row in range(2):
        terms = []
        for column in range(2):
            value = _point(0, precision)
            for index in range(2):
                value += DirectedInterval.from_float(
                    float(left[row, index]), precision
                ) * right[index][column]
            if row == column:
                value -= 1
            terms.append(value.upper_abs())
        row_bounds.append(upward_sum(terms, precision))
    return max(row_bounds)


def _float_matrix_hex(
    matrix: np.ndarray,
) -> tuple[tuple[str, str], tuple[str, str]]:
    values = np.asarray(matrix, dtype=float)
    return (
        (float(values[0, 0]).hex(), float(values[0, 1]).hex()),
        (float(values[1, 0]).hex(), float(values[1, 1]).hex()),
    )


def _branch_data(
    orbit: Any,
    branch: str,
    parent_branch: Mapping[str, Any],
    parent_midpoint: np.ndarray,
) -> _BranchData:
    settings = BRANCH_SETTINGS[branch]
    continuation = parent_branch.get("continuation")
    extrema = parent_branch.get("extrema")
    if not isinstance(continuation, Mapping) or not isinstance(extrema, Mapping):
        raise ValueError("the parent branch certificate is incomplete")
    if not (
        parent_branch.get("uniform_orbit_and_bordered_inverse_validated")
        is True
        and parent_branch.get("uniform_simple_extrema_validated") is True
        and continuation.get("parameter_box_bordered_inverse_validated")
        is True
        and extrema.get("extrema_validated") is True
    ):
        raise ValueError("a required parent branch gate is false")
    if (
        continuation.get("cutoff") != settings["cutoff"]
        or continuation.get("precision_bits") != PRECISION_BITS
        or continuation.get("half_width_unfolding_a")
        != HALF_WIDTH_UNFOLDING_A
        or continuation.get("half_width_kappa_3") != HALF_WIDTH_KAPPA_3
    ):
        raise ValueError("the parent branch settings changed")
    # Reconstruct the same source-defined midpoint preconditioner solely to
    # apply it to the D4 residual.  The periodic orbit and inverse theorem
    # remain the source-bound parent theorem; no new orbit candidate or
    # independent inverse claim is introduced here.
    replay = _validate_continuation(
        orbit,
        branch=branch,
        half_width_unfolding_a=HALF_WIDTH_UNFOLDING_A,
        half_width_kappa_3=HALF_WIDTH_KAPPA_3,
        cutoff=int(settings["cutoff"]),
        precision=PRECISION_BITS,
        maximum_radius=PARENT_RADIUS,
        chosen_radius=PARENT_RADIUS,
    )
    if replay.inverse_norm is None:
        raise ArithmeticError("the parent preconditioner replay did not close")
    replay_continuation = asdict(replay.continuation)
    merged_continuation = dict(continuation)
    upper_fields = (
        "preconditioned_box_residual_upper",
        "full_point_defect_upper",
        "coefficient_z1_upper",
        "coefficient_z2_upper",
        "coefficient_z3_upper",
        "global_preconditioner_l1_upper",
    )
    for field in upper_fields:
        parent_value = _upper_decimal(
            continuation.get(field), PRECISION_BITS, f"parent {field}"
        )
        replay_value = _upper_decimal(
            replay_continuation.get(field), PRECISION_BITS, f"replay {field}"
        )
        merged_continuation[field] = decimal_upper(
            max(parent_value, replay_value)
        )
    nested, radius, contraction, inverse_norm = _nested_radii(
        merged_continuation,
        str(settings["nested_radius"]),
        PRECISION_BITS,
    )
    base = replay.base
    layout = _RealConjugateLayout(int(settings["cutoff"]))
    fast_indices = [
        layout.state_index(0, 0, "real"),
        *[
            layout.state_index(0, mode, part)
            for mode in range(1, layout.cutoff + 1)
            for part in ("real", "imag")
        ],
    ]
    slow_indices = [
        layout.state_index(1, 0, "real"),
        *[
            layout.state_index(1, mode, part)
            for mode in range(1, layout.cutoff + 1)
            for part in ("real", "imag")
        ],
    ]
    finite_fast = _float_matrix_l1_upper(
        replay.approximate_inverse[:, fast_indices], PRECISION_BITS
    )
    finite_slow = _float_matrix_l1_upper(
        replay.approximate_inverse[:, slow_indices], PRECISION_BITS
    )
    tail_denominator = (
        pi_interval(PRECISION_BITS) * (2 * (layout.cutoff + 1))
    ).lower
    analytic_tail = upward_division(
        gmpy2.mpfr(1, PRECISION_BITS),
        tail_denominator,
        PRECISION_BITS,
    )
    fast_block = max(finite_fast, analytic_tail)
    slow_block = max(finite_slow, analytic_tail)
    variation_workspace = SimpleNamespace(
        orbit=orbit, base=base, chosen_radius=radius
    )
    variation = _variation_bounds(variation_workspace)
    return _BranchData(
        orbit=orbit,
        base=base,
        layout=layout,
        approximate_inverse=replay.approximate_inverse,
        approximate_inverse_l1=replay.approximate_inverse_l1,
        global_preconditioner_l1=max(
            replay.global_preconditioner_l1,
            _upper_decimal(
                merged_continuation["global_preconditioner_l1_upper"],
                PRECISION_BITS,
                "merged global preconditioner",
            ),
        ),
        fast_block_preconditioner_l1=fast_block,
        slow_block_preconditioner_l1=slow_block,
        radius=radius,
        contraction=contraction,
        inverse_norm=inverse_norm,
        variation=variation,
        nested=nested,
        parent_extrema=extrema,
        parent_midpoint=parent_midpoint,
    )


def _build_branch(data: _BranchData, branch: str) -> DirectedResponseBranch:
    precision = data.base.period.precision
    settings = BRANCH_SETTINGS[branch]
    from canard_control.leaky_periodic_parameter_box import (
        _floating_extrema_phases,
    )

    maximum_center, minimum_center = _floating_extrema_phases(data.orbit)
    maximum_window, maximum_phase = _refined_extremum_window(
        data, kind="maximum", center_phase=maximum_center
    )
    minimum_window, minimum_phase = _refined_extremum_window(
        data, kind="minimum", center_phase=minimum_center
    )
    if maximum_phase.upper >= minimum_phase.lower:
        raise ArithmeticError("the refined extrema windows overlap")

    sensitivities = _floating_sensitivities(data.orbit, precision)
    errors = []
    budgets = []
    for control_index, sensitivity in enumerate(sensitivities):
        residual = _sensitivity_residual(
            data.base, sensitivity, control_index
        )
        solve_residual = _raw_residual_norm(residual, precision)
        preconditioned_residual = _preconditioned_sequence_upper(
            data, *residual
        )
        variation = _raw_sensitivity_variation(
            data, sensitivity, control_index
        )
        with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
            total_raw = solve_residual + variation.total
            preconditioned_variation = (
                data.fast_block_preconditioner_l1 * variation.fast_total
                + data.slow_block_preconditioner_l1 * variation.slow_total
            )
            error = (
                preconditioned_residual.total + preconditioned_variation
            ) / (1 - data.contraction)
        errors.append(error)
        budgets.append(
            DirectedSensitivityBudget(
                control=CONTROL_ORDER[control_index],
                center_period_derivative_binary64_hex=float(
                    sensitivity[2].lower
                ).hex(),
                bordered_solve_residual_upper=decimal_upper(solve_residual),
                base_preconditioned_residual_upper=decimal_upper(
                    preconditioned_residual.total
                ),
                state_operator_variation_upper=decimal_upper(
                    variation.state
                ),
                period_operator_variation_upper=decimal_upper(
                    variation.period
                ),
                leaky_slow_row_variation_upper=decimal_upper(
                    variation.slow
                ),
                parameter_forcing_variation_upper=decimal_upper(
                    variation.forcing
                ),
                total_raw_residual_upper=decimal_upper(total_raw),
                fast_block_preconditioner_l1_upper=decimal_upper(
                    data.fast_block_preconditioner_l1
                ),
                slow_block_preconditioner_l1_upper=decimal_upper(
                    data.slow_block_preconditioner_l1
                ),
                preconditioned_variation_upper=decimal_upper(
                    preconditioned_variation
                ),
                nested_contraction_upper=data.nested.contraction_upper,
                exact_sensitivity_error_upper=decimal_upper(error),
            )
        )

    period = data.base.period + _symmetric(data.radius.upper, precision)
    if period.lower <= 0:
        raise ArithmeticError("the period interval reached zero")
    frequency = 1 / period
    maximum_voltage = _evaluate_real_sequence(
        data.base.voltage, maximum_phase
    ) + _symmetric(data.radius.upper, precision)
    minimum_voltage = _evaluate_real_sequence(
        data.base.voltage, minimum_phase
    ) + _symmetric(data.radius.upper, precision)
    amplitude = maximum_voltage - minimum_voltage
    if amplitude.lower <= 0:
        raise ArithmeticError("the unsquared amplitude is not positive")

    response: list[list[DirectedInterval]] = [[], []]
    for sensitivity, error in zip(sensitivities, errors, strict=True):
        sv, _, st = sensitivity
        st_box = st + _symmetric(error, precision)
        response[0].append(-st_box / (period * period))
        amplitude_derivative = (
            _evaluate_real_sequence(sv, maximum_phase)
            - _evaluate_real_sequence(sv, minimum_phase)
            + _symmetric(
                (_point(2, precision) * error).upper, precision
            )
        )
        response[1].append(amplitude_derivative)

    determinant = (
        response[0][0] * response[1][1]
        - response[0][1] * response[1][0]
    )
    determinant_margin = determinant.lower_abs()
    expected_sign = int(settings["expected_determinant_sign"])
    sign_valid = (
        determinant.upper < 0 if expected_sign < 0 else determinant.lower > 0
    )
    if not sign_valid or determinant_margin <= 0:
        raise ArithmeticError(f"{branch} response determinant contains zero")
    entries = [item for row in response for item in row]
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        frobenius = gmpy2.sqrt(
            sum(item.upper_abs() * item.upper_abs() for item in entries)
        )
        inverse_2norm = frobenius / determinant_margin
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        smallest_singular = determinant_margin / frobenius

    midpoint = np.asarray(data.parent_midpoint, dtype=float)
    left_preconditioner = np.linalg.inv(midpoint)
    midpoint_intervals = [
        [
            DirectedInterval.from_float(float(item), precision)
            for item in row
        ]
        for row in midpoint
    ]
    formation_defect = _matrix_product_defect_upper(
        left_preconditioner, midpoint_intervals, precision
    )
    if formation_defect >= _point("1e-12", precision).lower:
        raise ArithmeticError("the fixed 2 by 2 preconditioner formation failed")
    preconditioned_defect = _matrix_product_defect_upper(
        left_preconditioner, response, precision
    )
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        row_norms = [
            gmpy2.sqrt(
                sum(gmpy2.mpfr(float(item)) ** 2 for item in row)
            )
            for row in left_preconditioner
        ]
        preconditioner_2_to_infinity = max(row_norms)
    # Reparse the outward decimal records before deriving the target
    # corollary.  This makes the serialized radius and inverse-Lipschitz
    # fields algebraically checkable from the separately serialized q and
    # ||B|| records, rather than relying on hidden MPFR guard bits.
    preconditioned_defect_record = decimal_upper(preconditioned_defect)
    preconditioner_2_to_infinity_record = decimal_upper(
        preconditioner_2_to_infinity
    )
    recorded_defect_upper = _point(
        preconditioned_defect_record, precision
    ).upper
    recorded_preconditioner_upper = _point(
        preconditioner_2_to_infinity_record, precision
    ).upper
    target_radius = None
    inverse_lipschitz = None
    target_validated = recorded_defect_upper < 1
    if target_validated:
        with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
            inverse_lipschitz_value = (
                recorded_preconditioner_upper
                / (1 - recorded_defect_upper)
            )
        with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
            parameter_half_width = min(
                _point(HALF_WIDTH_UNFOLDING_A, precision).lower,
                _point(HALF_WIDTH_KAPPA_3, precision).lower,
            )
            target_radius_value = (
                parameter_half_width
                * (1 - recorded_defect_upper)
                / recorded_preconditioner_upper
            )
        if target_radius_value > 0:
            target_radius = decimal_lower(target_radius_value)
            inverse_lipschitz = decimal_upper(inverse_lipschitz_value)
        else:
            target_validated = False

    response_lower, response_upper = _interval_matrix_bounds(response)
    return DirectedResponseBranch(
        branch=branch,
        cutoff=int(settings["cutoff"]),
        precision_bits=precision,
        nested_radii=data.nested,
        maximum_window=maximum_window,
        minimum_window=minimum_window,
        maximum_center_derivative_error_upper=decimal_upper(
            data.variation.derivative_error
        ),
        output_frequency_lower=decimal_lower(frequency.lower),
        output_frequency_upper=decimal_upper(frequency.upper),
        output_amplitude_lower=decimal_lower(amplitude.lower),
        output_amplitude_upper=decimal_upper(amplitude.upper),
        sensitivities=(budgets[0], budgets[1]),
        response_lower=response_lower,
        response_upper=response_upper,
        response_midpoint_binary64_hex=_float_matrix_hex(midpoint),
        left_preconditioner_binary64_hex=_float_matrix_hex(
            left_preconditioner
        ),
        determinant_lower=decimal_lower(determinant.lower),
        determinant_upper=decimal_upper(determinant.upper),
        determinant_sign=expected_sign,
        determinant_absolute_margin_lower=decimal_lower(
            determinant_margin
        ),
        response_frobenius_norm_upper=decimal_upper(frobenius),
        smallest_singular_value_lower=decimal_lower(smallest_singular),
        pointwise_inverse_2norm_upper=decimal_upper(inverse_2norm),
        left_preconditioner_formation_defect_upper=decimal_upper(
            formation_defect
        ),
        left_preconditioner_2_to_infinity_norm_upper=(
            preconditioner_2_to_infinity_record
        ),
        left_preconditioned_derivative_defect_upper=(
            preconditioned_defect_record
        ),
        quantitative_target_ball_radius_lower=target_radius,
        parameter_inverse_lipschitz_upper=inverse_lipschitz,
        left_preconditioner_formation_audited=True,
        derivative_defect_uniform_on_common_parameter_box=True,
        exact_extremum_phase_terms_vanish=True,
        response_matrix_validated=True,
        determinant_nonzero_validated=True,
        pointwise_local_diffeomorphism_validated=True,
        quantitative_target_ball_validated=target_validated,
    )


def _load_parent_body(repository: Path) -> Mapping[str, Any]:
    path = repository / PARAMETER_BOX_PARENT_RELATIVE_PATH
    payload = json.loads(path.read_text(encoding="utf-8"))
    validate_parameter_response_artifact(
        payload, repository, replay_centers=False
    )
    artifact = payload.get("artifact")
    if not isinstance(artifact, Mapping):
        raise ValueError("the parameter-box parent has no artifact")
    directed = artifact.get("directed_common_box")
    branches = artifact.get("branches")
    if not isinstance(directed, Mapping) or not isinstance(branches, Mapping):
        raise ValueError("the parameter-box parent has no branch records")
    if not (
        directed.get("uniform_orbit_and_bordered_inverse_validated") is True
        and directed.get("uniform_simple_extrema_validated") is True
    ):
        raise ValueError("the parameter-box parent gates are false")
    return artifact


@lru_cache(maxsize=1)
def build_leaky_periodic_directed_response_certificate(
    repository_text: str,
) -> LeakyPeriodicDirectedResponseCertificate:
    """Build both branch response theorems from the source-bound parent."""

    if exact_directed_response_defects() != (0,) * 6:
        raise AssertionError("the exact response formulas changed")
    repository = Path(repository_text)
    artifact = _load_parent_body(repository)
    directed = artifact["directed_common_box"]
    directed_branches = directed["branches"]
    diagnostic_branches = artifact["branches"]
    (inner_orbit, _), outer_orbits = _load_parents(repository)
    orbits = {
        "inner_saddle_candidate": inner_orbit,
        "outer_pulse": outer_orbits[257][0],
    }
    built = {}
    for branch in BRANCH_SETTINGS:
        midpoint = _matrix_from_records(
            diagnostic_branches[branch]["center_response"]["response_matrix"],
            f"{branch} midpoint response",
        )
        if midpoint.shape != (2, 2):
            raise ValueError("a parent midpoint response is not 2 by 2")
        data = _branch_data(
            orbits[branch],
            branch,
            directed_branches[branch],
            midpoint,
        )
        built[branch] = _build_branch(data, branch)
    inner = built["inner_saddle_candidate"]
    outer = built["outer_pulse"]
    # A common target ball is asserted only when both separately computed
    # fixed-left-preconditioner tests close.
    common_target = (
        inner.quantitative_target_ball_validated
        and outer.quantitative_target_ball_validated
    )
    common_target_radius = None
    common_inverse_lipschitz = None
    if common_target:
        if (
            inner.quantitative_target_ball_radius_lower is None
            or outer.quantitative_target_ball_radius_lower is None
            or inner.parameter_inverse_lipschitz_upper is None
            or outer.parameter_inverse_lipschitz_upper is None
        ):
            raise AssertionError("a quantitative branch target is incomplete")
        common_target_radius = decimal_lower(
            min(
                _point(
                    inner.quantitative_target_ball_radius_lower,
                    PRECISION_BITS,
                ).lower,
                _point(
                    outer.quantitative_target_ball_radius_lower,
                    PRECISION_BITS,
                ).lower,
            )
        )
        common_inverse_lipschitz = decimal_upper(
            max(
                _point(
                    inner.parameter_inverse_lipschitz_upper,
                    PRECISION_BITS,
                ).upper,
                _point(
                    outer.parameter_inverse_lipschitz_upper,
                    PRECISION_BITS,
                ).upper,
            )
        )
    flags = {name: True for name in TRUE_FLAGS}
    false_flags = {name: False for name in FALSE_FLAGS}
    false_flags["quantitative_common_target_ball_validated"] = common_target
    return LeakyPeriodicDirectedResponseCertificate(
        schema_id=SCHEMA_ID,
        model_id=MODEL_ID,
        control_order=CONTROL_ORDER,
        output_order=OUTPUT_ORDER,
        frequency_definition="F=1/T cycles per unit physical time",
        amplitude_definition=(
            "A=max_phi v(phi)-min_phi v(phi), without squaring"
        ),
        target_ball_definition=(
            "for each branch separately: Euclidean output ball centered "
            "at the exact G_branch(1/4,1/200), with parameter distance "
            "measured in the infinity norm; the flagship outer interface "
            "uses the outer radius, while the common radius is the minimum "
            "for simultaneous two-branch tuning and does not make the "
            "branch-centered balls concentric"
        ),
        common_parameter_box=(
            "|a-1/4|<=1e-10",
            "|kappa_3-1/200|<=1e-10",
        ),
        precision_bits=PRECISION_BITS,
        exact_symbolic_zero_defect_count=6,
        inner=inner,
        outer=outer,
        flagship_outer_target_ball_radius_lower=(
            outer.quantitative_target_ball_radius_lower
        ),
        flagship_outer_parameter_inverse_lipschitz_upper=(
            outer.parameter_inverse_lipschitz_upper
        ),
        quantitative_common_target_ball_radius_lower=common_target_radius,
        common_parameter_inverse_lipschitz_upper=common_inverse_lipschitz,
        theorem_statement=(
            "on the common closed (a,kappa_3) box, each validated leaky "
            "periodic branch has a C1 response G=(1/T,v_max-v_min) whose "
            "directed 2 by 2 derivative enclosure has the recorded fixed "
            "nonzero determinant sign; hence G is a pointwise local "
            "diffeomorphism throughout the box; the separate whole-box "
            "fixed-preconditioner contractions also validate the recorded "
            "branch-centered target balls, with the outer radius retained "
            "for the flagship interface and their minimum recorded only "
            "for simultaneous two-branch tuning"
        ),
        **flags,
        **false_flags,
    )


def build_leaky_periodic_directed_response_result(
    repository: Path,
) -> dict[str, Any]:
    certificate = json.loads(
        json.dumps(
            asdict(
                build_leaky_periodic_directed_response_certificate(
                    str(repository.resolve())
                )
            )
        )
    )
    parent_results = {
        "parameter_box_parent": PARAMETER_BOX_PARENT_RELATIVE_PATH,
        "inner_orbit_parent": INNER_PARENT_RELATIVE_PATH,
        "outer_orbit_parent": OUTER_PARENT_RELATIVE_PATH,
    }
    return {
        "certificate": certificate,
        "manifest": {
            "schema_id": SCHEMA_ID,
            "result": RESULT_RELATIVE_PATH,
            "default_command": DEFAULT_COMMAND,
            "arithmetic": ARITHMETIC,
            "certificate_sha256": canonical_sha256(certificate),
            "parent_results": parent_results,
            "parent_result_sha256": {
                name: _sha256_path(repository / relative)
                for name, relative in parent_results.items()
            },
            "sources": SOURCE_PATHS,
            "source_sha256": {
                name: _sha256_path(repository / relative)
                for name, relative in SOURCE_PATHS.items()
            },
            "runtime": {
                "python": platform.python_version(),
                "platform": platform.platform(),
                "numpy": np.__version__,
                "scipy": scipy.__version__,
                "gmpy2": gmpy2.__version__,
                "mpfr": gmpy2.mpfr_version(),
                "sympy": sp.__version__,
            },
        },
    }


def validate_leaky_periodic_directed_response_result(
    payload: Mapping[str, Any], repository: Path
) -> None:
    if not isinstance(payload, Mapping) or set(payload) != {
        "certificate",
        "manifest",
    }:
        raise ValueError("directed response result has the wrong outer schema")
    certificate = payload.get("certificate")
    manifest = payload.get("manifest")
    if not isinstance(certificate, Mapping) or not isinstance(manifest, Mapping):
        raise ValueError("directed response records must be mappings")
    if set(certificate) != {
        field.name for field in fields(LeakyPeriodicDirectedResponseCertificate)
    }:
        raise ValueError("directed response certificate schema changed")
    expected = json.loads(
        json.dumps(
            asdict(
                build_leaky_periodic_directed_response_certificate(
                    str(repository.resolve())
                )
            )
        )
    )
    normalized = json.loads(json.dumps(certificate, allow_nan=False))
    if _canonical_json(normalized) != _canonical_json(expected):
        raise ValueError("directed response certificate differs from replay")
    if any(certificate.get(name) is not True for name in TRUE_FLAGS):
        raise ValueError("a proved directed response flag was weakened")
    for name in FALSE_FLAGS:
        if certificate.get(name) is not False:
            raise ValueError("an open pulse/safety claim was promoted")
    expected_manifest_keys = {
        "schema_id",
        "result",
        "default_command",
        "arithmetic",
        "certificate_sha256",
        "parent_results",
        "parent_result_sha256",
        "sources",
        "source_sha256",
        "runtime",
    }
    if set(manifest) != expected_manifest_keys:
        raise ValueError("directed response manifest schema changed")
    scalar = {
        "schema_id": SCHEMA_ID,
        "result": RESULT_RELATIVE_PATH,
        "default_command": DEFAULT_COMMAND,
        "arithmetic": ARITHMETIC,
    }
    for name, value in scalar.items():
        if manifest.get(name) != value:
            raise ValueError(f"directed response manifest {name} changed")
    if manifest.get("certificate_sha256") != canonical_sha256(normalized):
        raise ValueError("directed response certificate digest changed")
    parent_results = {
        "parameter_box_parent": PARAMETER_BOX_PARENT_RELATIVE_PATH,
        "inner_orbit_parent": INNER_PARENT_RELATIVE_PATH,
        "outer_orbit_parent": OUTER_PARENT_RELATIVE_PATH,
    }
    if manifest.get("parent_results") != parent_results:
        raise ValueError("directed response parent paths changed")
    hashes = manifest.get("parent_result_sha256")
    if not isinstance(hashes, Mapping) or set(hashes) != set(parent_results):
        raise ValueError("directed response parent hash schema changed")
    for name, relative in parent_results.items():
        if hashes.get(name) != _sha256_path(repository / relative):
            raise ValueError(f"directed response parent {name} hash changed")
    if manifest.get("sources") != SOURCE_PATHS:
        raise ValueError("directed response source paths changed")
    source_hashes = manifest.get("source_sha256")
    if not isinstance(source_hashes, Mapping) or set(source_hashes) != set(
        SOURCE_PATHS
    ):
        raise ValueError("directed response source hash schema changed")
    for name, relative in SOURCE_PATHS.items():
        if source_hashes.get(name) != _sha256_path(repository / relative):
            raise ValueError(f"directed response source {name} hash changed")
    runtime = {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "gmpy2": gmpy2.__version__,
        "mpfr": gmpy2.mpfr_version(),
        "sympy": sp.__version__,
    }
    if manifest.get("runtime") != runtime:
        raise ValueError("directed response runtime changed")
    _load_parent_body(repository)


__all__ = [
    "FALSE_FLAGS",
    "RESULT_RELATIVE_PATH",
    "TRUE_FLAGS",
    "build_leaky_periodic_directed_response_certificate",
    "build_leaky_periodic_directed_response_result",
    "canonical_sha256",
    "exact_directed_response_defects",
    "validate_leaky_periodic_directed_response_result",
]
