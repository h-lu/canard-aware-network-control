"""Directed Stage-5E physical-phase adjoint action certificate.

The Stage-3 Grushin eigencolumn is stored in a common complex gauge.  If

    gamma = q_tilde_v(theta_*) / |q_tilde_v(theta_*)|,

then ``q_phys=q_tilde/gamma`` is the real Route-C unstable history oriented
by ``q_phys_v(theta_*)>0``.  Consequently

    f_phys(y) = gamma * ell(y) / ell(q_tilde)

is real for real histories, although the raw quotient on the right without
``gamma`` generally is not.

This module encloses the correlated residual

    Y_*(J) = D_J K(J) - c_* q_phys,       c_*=-252,

on the complete event history.  It retains the Stage-5B parameter
polynomials, Stage-5C event graph, Stage-5D variational error, event
translation, recovery atom, and the Stage-4E finite-row plus Neumann-tail
density.  Every parameter shard and history segment is evaluated as an
interval; no finite sample is promoted to error evidence.

The result is only an oriented fixed-center functional action.  It is not a
stable graph, stable-gap, interval-Newton, onset, or routing certificate.
"""

from __future__ import annotations

from bisect import bisect_left
from functools import lru_cache
from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

import gmpy2

from canard_control.autonomous_leaky_recovery_bistable import (
    EPSILON,
    KAPPA_1,
    KAPPA_3,
    UNFOLDING,
)
from canard_control.directed_interval import (
    DirectedComplexInterval,
    DirectedInterval,
    complex_unit_interval,
    decimal_lower,
    decimal_upper,
    pi_interval,
    upward_sum,
)
from canard_control.leaky_pulse_event_aligned_derivative_stage5d import (
    PRECISION_BITS,
    _event_time_polynomial,
    _fraction_interval,
    _parameter_derivative,
    _scaled_sensitivity_on_time_parameter_box,
    _state_on_time_parameter_box,
    build_sensitivity_error_propagation,
    validate_stage5d_result,
)
from canard_control.leaky_pulse_parameter_jet_directed_enclosure import (
    PARAMETER_HALF_WIDTH,
    CoefficientCell,
    CoefficientPropagation,
    RemainderPropagation,
    build_coefficient_propagation,
    build_remainder_propagation,
    canonical_sha256,
)
from canard_control.leaky_pulse_quiet_capture import (
    _cell_key,
    _node_interval,
    _point,
)
from canard_control.leaky_pulse_route_c_event_stage5c import (
    _hull,
    _parameter_shards,
    _power_range,
    _time_range_intersection_with_cell,
)
from canard_control.leaky_shared_yqq_deflation_stage4e import (
    _adjoint_mode_rows,
    _centre_data,
    _complex_point,
    _exp_real,
    _evaluate,
    _guide_density_dictionary,
    _model_uncertainty,
    _row_tail_neumann,
    validate_stage4e_result,
)
from canard_control.leaky_inner_stable_projection_stage3 import (
    HISTORY_TEST_TIME,
    validate_stage3_stable_projection_result,
)


SCHEMA_ID = "leaky-pulse-oriented-adjoint-action-stage5e-v1"
MODEL_ID = "autonomous-leaky-recovery-physical-pulse"

SOURCE_RELATIVE_PATH = (
    "src/canard_control/leaky_pulse_oriented_adjoint_action_stage5e.py"
)
GENERATOR_RELATIVE_PATH = (
    "experiments/leaky_pulse_oriented_adjoint_action_stage5e.py"
)
RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_pulse_oriented_adjoint_action_stage5e.json"
)
NOTE_RELATIVE_PATH = "docs/leaky-pulse-oriented-adjoint-action-stage5e.md"
CONTRACT_RELATIVE_PATH = (
    "docs/leaky-pulse-oriented-adjoint-action-stage5e-contract.md"
)
TEST_RELATIVE_PATH = (
    "tests/test_leaky_pulse_oriented_adjoint_action_stage5e.py"
)

STAGE5B_RELATIVE_PATH = (
    "experiments/results/leaky_pulse_parameter_jet_directed_enclosure.json"
)
STAGE5B_SHA256 = "71276785fd803b663fc11de9489751ccd53dd8a408323a0bb140d0c9e7b7862b"
STAGE5C_RELATIVE_PATH = (
    "experiments/results/leaky_pulse_route_c_event_stage5c.json"
)
STAGE5C_SHA256 = "f1f198d68cb736bc9b5a48a0bff3eb5a93d39ee3f0b8f7cb6f7e07779483128d"
STAGE5D_RELATIVE_PATH = (
    "experiments/results/leaky_pulse_event_aligned_derivative_stage5d.json"
)
STAGE5D_SHA256 = "e8be485b8b4711a0ae0b1f3ec875f704c509d9ba0abd5b2166a2384567ed654e"
STAGE4D_RELATIVE_PATH = (
    "experiments/results/leaky_route_c_adjoint_stage4d.json"
)
STAGE4D_SHA256 = "af51bcfc20000b804134c1d8b9cacc303013676c440a89f2ecb52faf0042d568"
STAGE4E_RELATIVE_PATH = (
    "experiments/results/leaky_shared_yqq_deflation_stage4e.json"
)
STAGE4E_SHA256 = "ccdd6023f911e97785ec6f8be97b84d725d6af9f5051e1da602380d225e47acc"
STAGE3_RELATIVE_PATH = (
    "experiments/results/leaky_inner_stable_projection_stage3.json"
)
STAGE3_SHA256 = "9ea776a6e627745ded7f7023523999bfbd29a0be4878172c76512d623146e2ea"

SOURCE_MANIFEST = (
    SOURCE_RELATIVE_PATH,
    GENERATOR_RELATIVE_PATH,
    NOTE_RELATIVE_PATH,
    CONTRACT_RELATIVE_PATH,
    TEST_RELATIVE_PATH,
)
DEPENDENCY_SOURCE_MANIFEST = (
    "src/canard_control/directed_interval.py",
    "src/canard_control/leaky_pulse_event_aligned_derivative_stage5d.py",
    "src/canard_control/leaky_pulse_parameter_jet_directed_enclosure.py",
    "src/canard_control/leaky_pulse_route_c_event_stage5c.py",
    "src/canard_control/leaky_shared_yqq_deflation_stage4e.py",
    "src/canard_control/leaky_inner_stable_projection_stage3.py",
)

DEFAULT_COMMAND = (
    "OPENBLAS_NUM_THREADS=8 OMP_NUM_THREADS=1 "
    "PYTHONPATH=.venv/lib/python3.14/site-packages:src /usr/bin/python3 "
    "experiments/leaky_pulse_oriented_adjoint_action_stage5e.py"
)
ARITHMETIC_SCOPE = (
    "192-bit outward MPFR; exact 128-shard cover of xi in [-1,1]; exact "
    "partition of both delay-history pieces into 256 cells each; Stage-5B "
    "time-parameter polynomial boxes with the Stage-5D first-variation "
    "comparison inserted after differentiation; Stage-5C event polynomial "
    "plus its 1e-4 remainder; full event translation; Stage-3 nonzero test "
    "component physical phase; and the common Stage-4E finite-row plus "
    "Neumann-tail atom-density guide with its certified complete-measure "
    "difference; no finite sampling, stable graph, stable gap, Newton, "
    "onset, or routing promotion"
)

PROJECTION_IDENTITY = (
    "q_phys*f_phys(y)=q_tilde*ell(y)/ell(q_tilde)"
)
Q_PHYS_REALITY_REASON = (
    "The RFDE is real and the unstable real root is geometrically simple.  "
    "q_tilde/chi(q_tilde) is fixed by conjugation, hence real; multiplication "
    "by |chi(q_tilde)| gives q_phys."
)
COMPLEX_DISK_STATEMENT = (
    "gamma*ell(D_JK)/ell(q_tilde) lies in the closed complex "
    "disk centered at c_* with the displayed quotient radius"
)
REAL_INTERSECTION_STATEMENT = (
    "Reality and simplicity imply the exact disk member is real, "
    "so its intersection with R is the displayed interval."
)
THEOREM_STATEMENT = (
    "For every physical pulse amplitude in the exact Stage-5B interval, "
    "the physical-phase normalized fixed Route-C functional applied to "
    "the Stage-5D event-aligned derivative lies in the displayed real "
    "interval.  This uses the event translation and the common finite-"
    "plus-tail adjoint row.  No stable graph, stable-gap, Newton, onset, "
    "crossing ordinal, or routing conclusion follows."
)
COMMON_MEASURE_COVERAGE_STATEMENT = (
    "The imported Stage-4E history_measure_difference is the "
    "operator-norm difference between the exact complete atom-"
    "density measure and this same untrimmed finite-plus-Neumann-"
    "tail guide.  It includes finite-row, remaining tail, orbit/"
    "root/period covariance, density-basis, convolution and "
    "rounding terms."
)

PARAMETER_SUBDIVISIONS = 128
HISTORY_SUBDIVISIONS_PER_DELAY_PIECE = 256
CENTER = -252
JOINT_ENVELOPE_NAMES = (
    "r_joint_guide",
    "r_joint_measure",
)
COVERAGE_LEDGER_NAMES = (
    "r_guide",
    "r_pulse",
    "r_event",
    "r_row",
    "r_tail",
    "r_orbit",
    "r_seam",
    "r_round",
)
COVERAGE_LEDGER = {
    "r_guide": {
        "joint_envelope": "r_joint_guide",
        "relation": "principal directed atom-density action box",
    },
    "r_pulse": {
        "joint_envelope": "r_joint_guide",
        "relation": "nested: Stage-5B/5D exact pulse and sensitivity boxes",
    },
    "r_event": {
        "joint_envelope": "r_joint_guide",
        "relation": "nested: Stage-5C graph, speed division and translation",
    },
    "r_row": {
        "joint_envelope": "r_joint_measure",
        "relation": "overlapping: finite Grushin-row enclosure",
    },
    "r_tail": {
        "joint_envelope": "r_joint_measure",
        "relation": "overlapping: complete Neumann-tail remainder",
    },
    "r_orbit": {
        "joint_envelope": "r_joint_measure",
        "relation": "overlapping: orbit/root/period and covariance transfer",
    },
    "r_seam": {
        "joint_envelope": "r_joint_guide",
        "relation": "nested: exact release, delay, event and history cell cover",
    },
    "r_round": {
        "joint_envelope": "r_joint_measure",
        "relation": "overlapping: convolution and directed-rounding guard",
    },
}


TRUE_FLAGS = (
    "stage5b_stage5c_stage5d_stage4d_stage4e_stage3_bytes_source_bound",
    "stored_grushin_eigencolumn_complex_gauge_acknowledged",
    "nonzero_route_c_test_component_source_bound",
    "physical_real_eigencolumn_phase_oriented",
    "raw_complex_quotient_not_promoted_to_real",
    "same_adjoint_row_used_in_numerator_and_denominator",
    "stage5d_event_translation_retained",
    "recovery_atom_retained",
    "finite_fourier_row_and_neumann_tail_retained",
    "all_history_and_delay_seams_retained",
    "correlated_residual_formed_before_absolute_value",
    "full_parameter_interval_covered_without_sampling",
    "oriented_physical_functional_action_interval_validated",
)

CONDITIONAL_TRUE_FLAGS = (
    "oriented_physical_functional_action_excludes_zero_validated",
)

FALSE_FLAGS = (
    "raw_complex_gauge_quotient_is_real_validated",
    "quantitative_inner_stable_graph_validated",
    "stable_gap_derivative_interval_validated",
    "stable_gap_derivative_excludes_zero_validated",
    "stable_gap_endpoint_signs_validated",
    "interval_newton_strict_inclusion_validated",
    "unique_stable_sheet_pulse_parameter_Jc_validated",
    "ordinal_third_crossing_validated",
    "unique_physical_pulse_onset_validated",
    "two_sided_basin_routing_validated",
    "outer_or_quiet_capture_from_both_sides_validated",
    "frequency_amplitude_safety_radius_validated",
    "asynchronous_network_safety_radius_validated",
)

_FLAG_GROUPS = (TRUE_FLAGS, CONDITIONAL_TRUE_FLAGS, FALSE_FLAGS)
if any(len(group) != len(set(group)) for group in _FLAG_GROUPS):
    raise RuntimeError("Stage-5E claim flag groups must each be unique")
if any(
    set(_FLAG_GROUPS[left]) & set(_FLAG_GROUPS[right])
    for left in range(len(_FLAG_GROUPS))
    for right in range(left + 1, len(_FLAG_GROUPS))
):
    raise RuntimeError("Stage-5E claim flag groups must be pairwise disjoint")

CERTIFICATE_KEYS = (
    "schema_id",
    "model_id",
    "physical_phase_orientation",
    "correlated_history_action",
    "oriented_action",
    "stable_gap_interface",
    "theorem_statement",
    "claim_status",
)
MANIFEST_KEYS = (
    "schema_id",
    "result",
    "default_command",
    "arithmetic_scope",
    "parent_sha256",
    "source_sha256",
    "dependency_source_sha256",
    "certificate_sha256",
)
PHASE_KEYS = (
    "test_functional",
    "stored_object",
    "gamma_definition",
    "q_phys_definition",
    "f_phys_definition",
    "projection_identity",
    "test_component_box",
    "test_component_modulus_interval",
    "gamma_box",
    "q_phys_reality_reason",
    "raw_complex_quotient_is_real",
    "diagnostic_raw_center_quotient",
    "diagnostic_phase_corrected_center_quotient",
    "diagnostic_only_not_error_evidence",
)
ACTION_KEYS = (
    "center_c_star_exact",
    "residual",
    "parameter_subdivision_count",
    "history_subdivision_count",
    "history_subdivisions_per_delay_piece",
    "finite_parameter_sampling_used",
    "event_translation_retained",
    "recovery_atom_retained",
    "voltage_current_atom_exactly_zero_after_section_and_q_section",
    "exact_section_identities",
    "finite_row_retained",
    "neumann_tail_retained",
    "neumann_tail_step_count",
    "neumann_tail_residual_history",
    "density_direct_and_omitted_dictionaries_kept_separate",
    "density_delay_piece_count",
    "density_dictionary_count",
    "delay_and_history_seams_retained",
    "guide_action_complex_box",
    "maximum_correlated_residual_Y_norm_upper",
    "maximum_voltage_translation_term_upper",
    "maximum_recovery_translation_term_upper",
    "minimum_event_speed_lower",
    "stage4e_complete_measure_difference_upper",
    "named_error_budget",
)
BUDGET_KEYS = (
    "joint_envelope_upper",
    "joint_sum_order",
    "coverage_ledger",
    "coverage_ledger_is_nested_or_overlapping_and_not_additive",
    "common_measure_difference_components",
    "total_numerator_radius_upper",
    "sum_identity",
)
COMMON_COMPONENT_KEYS = (
    "finite_adjoint_l1_error_upper",
    "adjoint_fourier_tail_l1_error_upper",
    "adjoint_density_basis_shift_upper",
    "density_convolution_rounding_guard_upper",
    "neumann_tail_remainder_covered",
    "finite_row_enclosure_covered",
    "periodic_orbit_and_advanced_covariance_covered",
    "guide_exact_atom_density_difference_covered",
    "coverage_statement",
)
ORIENTED_KEYS = (
    "same_row_denominator_modulus_lower",
    "numerator_residual_modulus_upper",
    "quotient_radius_upper",
    "physical_real_interval",
    "physical_real_interval_excludes_zero",
    "complex_disk_statement",
    "real_intersection_statement",
)
STABLE_INTERFACE_KEYS = (
    "oriented_fixed_functional_action_interval_available",
    "oriented_fixed_functional_action_excludes_zero",
    "quantitative_inner_stable_graph_available",
    "stable_gap_derivative_interval",
    "stable_gap_endpoint_intervals",
    "interval_newton_image",
    "pulse_parameter_Jc",
    "onset_or_routing_conclusion",
)
COMPLEX_INTERVAL_KEYS = ("real", "imag")


def _sha256_path(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _mapping(value: Any, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{name} must be a mapping")
    return value


def _exact_mapping(
    value: Any, name: str, expected_keys: Sequence[str]
) -> Mapping[str, Any]:
    result = _mapping(value, name)
    if set(result) != set(expected_keys):
        raise ValueError(f"{name} key set changed")
    return result


def _finite_decimal_interval(
    value: Any, name: str, *, positive: bool
) -> DirectedInterval:
    result = DirectedInterval.from_decimal(str(value), PRECISION_BITS)
    if not gmpy2.is_finite(result.lower) or not gmpy2.is_finite(result.upper):
        raise ValueError(f"{name} must be finite")
    invalid_sign = result.lower <= 0 if positive else result.lower < 0
    if invalid_sign:
        qualifier = "positive" if positive else "nonnegative"
        raise ValueError(f"{name} must be {qualifier}")
    return result


def _load_bound_json(repository: Path, relative: str, expected: str) -> Any:
    path = repository / relative
    if _sha256_path(path) != expected:
        raise ValueError(f"Stage-5E bound parent changed: {relative}")
    return json.loads(path.read_text(encoding="utf-8"))


def _interval_record(value: DirectedInterval) -> dict[str, str]:
    return {
        "lower": decimal_lower(value.lower),
        "upper": decimal_upper(value.upper),
    }


def _complex_record(value: DirectedComplexInterval) -> dict[str, dict[str, str]]:
    return {"real": _interval_record(value.real), "imag": _interval_record(value.imag)}


def _parse_interval_record(
    value: Mapping[str, Any], name: str
) -> DirectedInterval:
    if set(value) != {"lower", "upper"}:
        raise ValueError(f"{name} is not an interval record")
    result = DirectedInterval.from_bounds(
        str(value["lower"]), str(value["upper"]), PRECISION_BITS
    )
    if not gmpy2.is_finite(result.lower) or not gmpy2.is_finite(result.upper):
        raise ValueError(f"{name} must be finite")
    return result


def _oriented_arithmetic(
    component_upper: Mapping[str, str], denominator_lower_text: str
) -> dict[str, str]:
    """Recompute the Stage-5E scalar acceptance arithmetic from stored data."""

    if set(component_upper) != set(JOINT_ENVELOPE_NAMES):
        raise ValueError("the Stage-5E joint-envelope names changed")
    values = tuple(
        DirectedInterval.from_decimal(str(component_upper[name]), PRECISION_BITS).upper
        for name in JOINT_ENVELOPE_NAMES
    )
    numerator = upward_sum(values, PRECISION_BITS)
    numerator_text = decimal_upper(numerator)
    numerator_effective = DirectedInterval.from_decimal(
        numerator_text, PRECISION_BITS
    ).upper
    denominator = DirectedInterval.from_decimal(
        denominator_lower_text, PRECISION_BITS
    ).lower
    if denominator <= 0:
        raise ValueError("the Stage-5E denominator is not positive")
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
        radius = numerator_effective / denominator
    radius_text = decimal_upper(radius)
    radius_effective = DirectedInterval.from_decimal(
        radius_text, PRECISION_BITS
    ).upper
    center = gmpy2.mpfr(CENTER, PRECISION_BITS)
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundDown):
        lower = center - radius_effective
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
        upper = center + radius_effective
    return {
        "numerator": numerator_text,
        "radius": radius_text,
        "lower": decimal_lower(lower),
        "upper": decimal_upper(upper),
    }


def _symmetric(radius: gmpy2.mpfr) -> DirectedInterval:
    return DirectedInterval.from_bounds(-radius, radius, PRECISION_BITS)


def _complex_expand(
    value: DirectedComplexInterval, radius: gmpy2.mpfr
) -> DirectedComplexInterval:
    error = _symmetric(radius)
    return DirectedComplexInterval(value.real + error, value.imag + error)


def _complex_conjugate(value: DirectedComplexInterval) -> DirectedComplexInterval:
    return DirectedComplexInterval(value.real, -value.imag)


def _directed_sum(values: Sequence[complex]) -> DirectedComplexInterval:
    total = DirectedComplexInterval.zero(PRECISION_BITS)
    for value in values:
        total = total + _complex_point(complex(value), PRECISION_BITS)
    return total


def _density_box(
    dictionaries: Sequence[Mapping[tuple[int, int], complex]],
    theta: DirectedInterval,
    period: float,
    root: float,
) -> DirectedComplexInterval:
    period_box = DirectedInterval.from_float(period, PRECISION_BITS)
    root_box = DirectedInterval.from_float(root, PRECISION_BITS)
    total = DirectedComplexInterval.zero(PRECISION_BITS)
    for density in dictionaries:
        for (growth, mode), coefficient in density.items():
            real_frequency = root_box * growth / period_box
            angle = pi_interval(PRECISION_BITS) * (2 * mode) * theta / period_box
            exponential = _exp_real(real_frequency * theta)
            total = total + _complex_point(
                complex(coefficient), PRECISION_BITS
            ) * DirectedComplexInterval.from_real(exponential) * complex_unit_interval(
                angle
            )
    return total


class _CellLocator:
    def __init__(self, propagation: CoefficientPropagation):
        self.cells = tuple(propagation.cells.values())
        self.ends = tuple(
            float(_node_interval(cell.right, PRECISION_BITS).upper)
            for cell in self.cells
        )

    def candidates(self, time: DirectedInterval) -> tuple[CoefficientCell, ...]:
        index = max(0, bisect_left(self.ends, float(time.lower)) - 2)
        # The binary search is only a speed hint.  This directed backwards
        # check makes the selected cover independent of binary64 placement.
        while index > 0 and (
            _node_interval(self.cells[index - 1].right, PRECISION_BITS).upper
            >= time.lower
        ):
            index -= 1
        result: list[CoefficientCell] = []
        for cell in self.cells[index:]:
            left = _node_interval(cell.left, PRECISION_BITS)
            if left.lower > time.upper:
                break
            if _time_range_intersection_with_cell(time, cell) is not None:
                result.append(cell)
        if not result:
            raise ArithmeticError("a Stage-5E time box missed the Stage-5B grid")
        return tuple(result)


def _state_component(
    locator: _CellLocator,
    remainder: RemainderPropagation,
    time: DirectedInterval,
    parameter_lower: DirectedInterval,
    parameter_upper: DirectedInterval,
    *,
    voltage: bool,
) -> DirectedInterval:
    values = []
    for cell in locator.candidates(time):
        key = _cell_key(cell.left, cell.right)
        values.append(
            _state_on_time_parameter_box(
                cell,
                remainder.cells[key],
                time,
                parameter_lower,
                parameter_upper,
                voltage=voltage,
            )
        )
    return _hull(tuple(values))


def _scaled_variation_component(
    locator: _CellLocator,
    sensitivity: Any,
    time: DirectedInterval,
    parameter_lower: DirectedInterval,
    parameter_upper: DirectedInterval,
    *,
    voltage: bool,
) -> DirectedInterval:
    values = []
    for cell in locator.candidates(time):
        key = _cell_key(cell.left, cell.right)
        values.append(
            _scaled_sensitivity_on_time_parameter_box(
                cell,
                sensitivity.cells[key],
                time,
                parameter_lower,
                parameter_upper,
                voltage=voltage,
            )
        )
    return _hull(tuple(values))


def _physical_field(
    locator: _CellLocator,
    remainder: RemainderPropagation,
    time: DirectedInterval,
    parameter_lower: DirectedInterval,
    parameter_upper: DirectedInterval,
) -> tuple[DirectedInterval, DirectedInterval]:
    voltage = _state_component(
        locator,
        remainder,
        time,
        parameter_lower,
        parameter_upper,
        voltage=True,
    )
    recovery = _state_component(
        locator,
        remainder,
        time,
        parameter_lower,
        parameter_upper,
        voltage=False,
    )
    sqrt_five = _point(5, PRECISION_BITS).sqrt()
    delayed_four = _state_component(
        locator,
        remainder,
        time - 4 * sqrt_five,
        parameter_lower,
        parameter_upper,
        voltage=True,
    )
    delayed_five = _state_component(
        locator,
        remainder,
        time - 5 * sqrt_five,
        parameter_lower,
        parameter_upper,
        voltage=True,
    )
    epsilon = _fraction_interval(EPSILON, PRECISION_BITS)
    kappa_1 = _fraction_interval(KAPPA_1, PRECISION_BITS)
    kappa_3 = _fraction_interval(KAPPA_3, PRECISION_BITS)
    unfolding = _fraction_interval(UNFOLDING, PRECISION_BITS)
    fast = (
        voltage
        - voltage**3 / 3
        - recovery
        + epsilon
        * kappa_1
        * ((delayed_four + delayed_five) / 2 - voltage)
        + epsilon
        * kappa_3
        * (
            ((delayed_four - 1) ** 3 + (delayed_five - 1) ** 3) / 2
            - (voltage - 1) ** 3
        )
    )
    slow = epsilon * (voltage - unfolding - recovery)
    return fast, slow


def _phase_data(data: Any, uncertainty: Mapping[str, float], stage3: Mapping[str, Any]) -> dict[str, Any]:
    q_error = DirectedInterval.from_bounds(
        0, uncertainty["qsection_error"], PRECISION_BITS
    ).upper
    test_time = float(HISTORY_TEST_TIME)
    test_center = _evaluate(
        data.qsection_v, test_time, data.period, data.root
    )
    test_box = _complex_expand(
        _complex_point(test_center, PRECISION_BITS), q_error
    )
    certified_lower = DirectedInterval.from_decimal(
        str(
            stage3["certificate"]["route_c_component_audit"][
                "section_voltage_component_at_test_time_abs_lower"
            ]
        ),
        PRECISION_BITS,
    ).lower
    if test_box.lower_abs() < certified_lower:
        # The independent Stage-3 component audit is sharper, but the phase
        # rectangle below still comes from the common qsection enclosure.
        nonzero_lower = test_box.lower_abs()
    else:
        nonzero_lower = certified_lower
    if nonzero_lower <= 0:
        raise ArithmeticError("the physical q phase component crossed zero")
    modulus = DirectedInterval(
        nonzero_lower, test_box.upper_abs(), PRECISION_BITS
    )
    gamma = DirectedComplexInterval(
        test_box.real / modulus, test_box.imag / modulus
    )
    center_gamma = test_center / abs(test_center)
    return {
        "q_error": q_error,
        "test_center": test_center,
        "test_box": test_box,
        "test_modulus": modulus,
        "gamma": gamma,
        "center_gamma": center_gamma,
    }


def _serialized_phase_data(
    data: Any, uncertainty: Mapping[str, float], stage3: Mapping[str, Any]
) -> tuple[
    dict[str, Any],
    dict[str, dict[str, str]],
    dict[str, str],
    dict[str, dict[str, str]],
]:
    phase = _phase_data(data, uncertainty, stage3)
    test_record = _complex_record(phase["test_box"])
    serialized_test = DirectedComplexInterval(
        _parse_interval_record(test_record["real"], "phase test real"),
        _parse_interval_record(test_record["imag"], "phase test imag"),
    )
    modulus_record = _interval_record(
        DirectedInterval(
            serialized_test.lower_abs(),
            serialized_test.upper_abs(),
            PRECISION_BITS,
        )
    )
    serialized_modulus = _parse_interval_record(
        modulus_record, "phase test modulus"
    )
    gamma_record = _complex_record(
        DirectedComplexInterval(
            serialized_test.real / serialized_modulus,
            serialized_test.imag / serialized_modulus,
        )
    )
    return phase, test_record, modulus_record, gamma_record


@lru_cache(maxsize=1)
def _source_bound_phase_records(
    repository_text: str,
) -> tuple[
    dict[str, dict[str, str]],
    dict[str, str],
    dict[str, dict[str, str]],
]:
    repository = Path(repository_text).resolve()
    stage3 = _load_bound_json(repository, STAGE3_RELATIVE_PATH, STAGE3_SHA256)
    data = _centre_data(repository)
    uncertainty = _model_uncertainty(data)
    _, test_record, modulus_record, gamma_record = _serialized_phase_data(
        data, uncertainty, stage3
    )
    return test_record, modulus_record, gamma_record


def _q_phys_box(
    data: Any,
    phase: Mapping[str, Any],
    theta: DirectedInterval,
    *,
    voltage: bool,
) -> DirectedInterval:
    # The exponential dictionary is evaluated at the entire theta interval
    # by a direct termwise enclosure.  The Stage-4E qsection_error includes
    # the eigencolumn, root, period, orbit, section and binary-algebra errors.
    dictionary = data.qsection_v if voltage else data.qsection_w
    period_box = DirectedInterval.from_float(data.period, PRECISION_BITS)
    root_box = DirectedInterval.from_float(data.root, PRECISION_BITS)
    q_tilde = DirectedComplexInterval.zero(PRECISION_BITS)
    for (growth, mode), coefficient in dictionary.items():
        real_frequency = root_box * growth / period_box
        angle = pi_interval(PRECISION_BITS) * (2 * mode) * theta / period_box
        exponential = _exp_real(real_frequency * theta)
        q_tilde = q_tilde + _complex_point(
            complex(coefficient), PRECISION_BITS
        ) * DirectedComplexInterval.from_real(exponential) * complex_unit_interval(
            angle
        )
    q_tilde = _complex_expand(q_tilde, phase["q_error"])
    physical = q_tilde * _complex_conjugate(phase["gamma"])
    if not physical.imag.contains_zero():
        raise ArithmeticError("the physical q reality intersection was lost")
    return physical.real


def _history_segments(
) -> tuple[tuple[DirectedInterval, int, DirectedInterval], ...]:
    sqrt_five = _point(5, PRECISION_BITS).sqrt()
    tau0 = 4 * sqrt_five
    tau1 = 5 * sqrt_five
    count = HISTORY_SUBDIVISIONS_PER_DELAY_PIECE
    result: list[tuple[DirectedInterval, int, DirectedInterval]] = []
    for left, right, active in ((-tau1, -tau0, 1), (-tau0, _point(0, PRECISION_BITS), 2)):
        step = (right - left) / count
        for index in range(count):
            segment = left + step * DirectedInterval.from_bounds(
                index, index + 1, PRECISION_BITS
            )
            result.append((segment, active, step))
    return tuple(result)


@lru_cache(maxsize=1)
def build_stage5e_certificate(repository: Path) -> dict[str, Any]:
    repository = Path(repository).resolve()
    stage5b = _load_bound_json(repository, STAGE5B_RELATIVE_PATH, STAGE5B_SHA256)
    stage5c = _load_bound_json(repository, STAGE5C_RELATIVE_PATH, STAGE5C_SHA256)
    stage5d = _load_bound_json(repository, STAGE5D_RELATIVE_PATH, STAGE5D_SHA256)
    stage4d = _load_bound_json(repository, STAGE4D_RELATIVE_PATH, STAGE4D_SHA256)
    stage4e = _load_bound_json(repository, STAGE4E_RELATIVE_PATH, STAGE4E_SHA256)
    stage3 = _load_bound_json(repository, STAGE3_RELATIVE_PATH, STAGE3_SHA256)
    validate_stage5d_result(stage5d, repository)
    validate_stage4e_result(stage4e, repository)
    validate_stage3_stable_projection_result(stage3, repository)

    stage5c_certificate = _mapping(stage5c.get("certificate"), "Stage-5C certificate")
    coefficients = build_coefficient_propagation()
    remainder = build_remainder_propagation()
    sensitivity = build_sensitivity_error_propagation()
    if not coefficients.completed or not remainder.completed or not sensitivity.completed:
        raise ArithmeticError("a Stage-5B/5D propagation parent is incomplete")
    locator = _CellLocator(coefficients)

    data = _centre_data(repository)
    uncertainty = _model_uncertainty(data)
    (
        phase,
        phase_test_record,
        phase_modulus_record,
        phase_gamma_record,
    ) = _serialized_phase_data(
        data, uncertainty, stage3
    )
    tail_v, tail_w, tail_iterations = _row_tail_neumann(data)
    row_v, row_w = _adjoint_mode_rows(data, tail_v, tail_w)
    atom_v = _directed_sum(tuple(row_v.values()))
    atom_w = _directed_sum(tuple(row_w.values()))
    # Keep direct and omitted dictionaries separate.  Stage4E's generic
    # dictionary addition trims below 1e-18; applying it here would silently
    # discard part of the already reconstructed guide density.
    densities: list[tuple[Mapping[tuple[int, int], complex], ...]] = []
    for delay, delayed_coefficient in (
        (data.tau0, data.delayed0),
        (data.tau1, data.delayed1),
    ):
        direct, omitted = _guide_density_dictionary(
            data, tail_v, tail_w, delay, delayed_coefficient
        )
        densities.append((direct, omitted))

    segments = _history_segments()
    density_boxes: list[DirectedComplexInterval] = []
    q_voltage_boxes: list[DirectedInterval] = []
    for theta, active, _ in segments:
        active_densities = (
            densities[1]
            if active == 1
            else densities[0] + densities[1]
        )
        density_boxes.append(
            _density_box(active_densities, theta, data.period, data.root)
        )
        q_voltage_boxes.append(
            _q_phys_box(data, phase, theta, voltage=True)
        )
    zero = _point(0, PRECISION_BITS)
    q_recovery_current = _q_phys_box(
        data, phase, DirectedInterval(zero.lower, zero.upper, PRECISION_BITS), voltage=False
    )

    event_polynomial = _event_time_polynomial(stage5c_certificate)
    half_width = _fraction_interval(PARAMETER_HALF_WIDTH, PRECISION_BITS)
    shard_actions: list[DirectedComplexInterval] = []
    maximum_residual_norm = gmpy2.mpfr(0, PRECISION_BITS)
    maximum_translation_voltage = gmpy2.mpfr(0, PRECISION_BITS)
    maximum_translation_recovery = gmpy2.mpfr(0, PRECISION_BITS)
    minimum_event_speed = gmpy2.inf()
    for parameter_lower, parameter_upper in _parameter_shards(
        PARAMETER_SUBDIVISIONS
    ):
        event_time = _power_range(
            event_polynomial, parameter_lower, parameter_upper
        )
        event_wv = _scaled_variation_component(
            locator,
            sensitivity,
            event_time,
            parameter_lower,
            parameter_upper,
            voltage=True,
        )
        event_ww = _scaled_variation_component(
            locator,
            sensitivity,
            event_time,
            parameter_lower,
            parameter_upper,
            voltage=False,
        )
        event_fast, event_slow = _physical_field(
            locator,
            remainder,
            event_time,
            parameter_lower,
            parameter_upper,
        )
        if event_fast.lower <= 0:
            raise ArithmeticError("a Stage-5E event-speed shard crossed zero")
        minimum_event_speed = min(minimum_event_speed, event_fast.lower)
        event_time_xi = -event_wv / event_fast

        recovery_derivative = (
            event_ww + event_slow * event_time_xi
        ) / half_width
        recovery_residual = recovery_derivative - CENTER * q_recovery_current
        action = atom_w * recovery_residual
        maximum_residual_norm = max(
            maximum_residual_norm, recovery_residual.upper_abs()
        )
        maximum_translation_recovery = max(
            maximum_translation_recovery,
            (event_slow * event_time_xi / half_width).upper_abs(),
        )

        for (theta, _, segment_width), density, q_voltage in zip(
            segments, density_boxes, q_voltage_boxes, strict=True
        ):
            physical_time = event_time + theta
            scaled_voltage = _scaled_variation_component(
                locator,
                sensitivity,
                physical_time,
                parameter_lower,
                parameter_upper,
                voltage=True,
            )
            fast, _ = _physical_field(
                locator,
                remainder,
                physical_time,
                parameter_lower,
                parameter_upper,
            )
            translation = fast * event_time_xi / half_width
            voltage_derivative = scaled_voltage / half_width + translation
            residual = voltage_derivative - CENTER * q_voltage
            action = action + density * residual * segment_width
            maximum_residual_norm = max(
                maximum_residual_norm, residual.upper_abs()
            )
            maximum_translation_voltage = max(
                maximum_translation_voltage, translation.upper_abs()
            )
        shard_actions.append(action)

    action_real = _hull(tuple(value.real for value in shard_actions))
    action_imag = _hull(tuple(value.imag for value in shard_actions))
    guide_action = DirectedComplexInterval(action_real, action_imag)
    guide_action_record = _complex_record(guide_action)
    serialized_guide_action = DirectedComplexInterval(
        _parse_interval_record(guide_action_record["real"], "guide action real"),
        _parse_interval_record(guide_action_record["imag"], "guide action imag"),
    )
    maximum_residual_norm_text = decimal_upper(maximum_residual_norm)
    maximum_residual_norm_effective = DirectedInterval.from_decimal(
        maximum_residual_norm_text, PRECISION_BITS
    ).upper

    correlated = _mapping(
        stage4e["artifact"]["continuous_history_correlated_deflation"],
        "Stage-4E correlated action",
    )
    denominator_lower = DirectedInterval.from_decimal(
        str(correlated["f_q_modulus_lower"]), PRECISION_BITS
    ).lower
    denominator_lower_text = decimal_lower(denominator_lower)
    measure_difference_text = str(correlated["history_measure_difference_upper"])
    measure_difference_effective = DirectedInterval.from_decimal(
        measure_difference_text, PRECISION_BITS
    ).upper
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
        guide_upper = serialized_guide_action.upper_abs()
        common_measure_error = (
            measure_difference_effective * maximum_residual_norm_effective
        )
    # These are two *joint*, disjoint acceptance envelopes.  The eight
    # mechanisms required by the contract form a coverage ledger below;
    # several are nested in or overlap one joint envelope and therefore must
    # not be added as if they were independent radii.
    joint_envelope_upper = {
        "r_joint_guide": decimal_upper(guide_upper),
        "r_joint_measure": decimal_upper(common_measure_error),
    }
    acceptance = _oriented_arithmetic(
        joint_envelope_upper, denominator_lower_text
    )
    oriented_interval = DirectedInterval.from_bounds(
        acceptance["lower"], acceptance["upper"], PRECISION_BITS
    )
    excludes_zero = not oriented_interval.contains_zero()

    raw_center_quotient = (
        26.631524287185137 + 250.8776952139106j
    )
    physical_center_quotient = phase["center_gamma"] * raw_center_quotient

    named_budget = {
        "joint_envelope_upper": joint_envelope_upper,
        "joint_sum_order": list(JOINT_ENVELOPE_NAMES),
        "coverage_ledger": {
            "r_guide": {
                "joint_envelope": "r_joint_guide",
                "relation": "principal directed atom-density action box",
            },
            "r_pulse": {
                "joint_envelope": "r_joint_guide",
                "relation": "nested: Stage-5B/5D exact pulse and sensitivity boxes",
            },
            "r_event": {
                "joint_envelope": "r_joint_guide",
                "relation": "nested: Stage-5C graph, speed division and translation",
            },
            "r_row": {
                "joint_envelope": "r_joint_measure",
                "relation": "overlapping: finite Grushin-row enclosure",
            },
            "r_tail": {
                "joint_envelope": "r_joint_measure",
                "relation": "overlapping: complete Neumann-tail remainder",
            },
            "r_orbit": {
                "joint_envelope": "r_joint_measure",
                "relation": "overlapping: orbit/root/period and covariance transfer",
            },
            "r_seam": {
                "joint_envelope": "r_joint_guide",
                "relation": "nested: exact release, delay, event and history cell cover",
            },
            "r_round": {
                "joint_envelope": "r_joint_measure",
                "relation": "overlapping: convolution and directed-rounding guard",
            },
        },
        "coverage_ledger_is_nested_or_overlapping_and_not_additive": True,
        "common_measure_difference_components": {
            "finite_adjoint_l1_error_upper": str(
                correlated["finite_adjoint_l1_error_upper"]
            ),
            "adjoint_fourier_tail_l1_error_upper": str(
                correlated["adjoint_fourier_tail_l1_error_upper"]
            ),
            "adjoint_density_basis_shift_upper": str(
                correlated["adjoint_density_basis_shift_upper"]
            ),
            "density_convolution_rounding_guard_upper": str(
                correlated["density_convolution_rounding_guard_upper"]
            ),
            "neumann_tail_remainder_covered": True,
            "finite_row_enclosure_covered": True,
            "periodic_orbit_and_advanced_covariance_covered": True,
            "guide_exact_atom_density_difference_covered": True,
            "coverage_statement": COMMON_MEASURE_COVERAGE_STATEMENT,
        },
        "total_numerator_radius_upper": acceptance["numerator"],
        "sum_identity": "r_A=r_joint_guide+r_joint_measure",
    }

    claims = {
        **{name: True for name in TRUE_FLAGS},
        **{name: excludes_zero for name in CONDITIONAL_TRUE_FLAGS},
        **{name: False for name in FALSE_FLAGS},
    }
    return {
        "schema_id": SCHEMA_ID,
        "model_id": MODEL_ID,
        "physical_phase_orientation": {
            "test_functional": f"chi(y)=y_v({HISTORY_TEST_TIME})",
            "stored_object": "q_tilde is the exact complex-gauge Stage-3 Grushin eigencolumn",
            "gamma_definition": "gamma=chi(q_tilde)/|chi(q_tilde)|",
            "q_phys_definition": "q_phys=q_tilde/gamma",
            "f_phys_definition": "f_phys(y)=gamma*ell(y)/ell(q_tilde)",
            "projection_identity": PROJECTION_IDENTITY,
            "test_component_box": phase_test_record,
            "test_component_modulus_interval": phase_modulus_record,
            "gamma_box": phase_gamma_record,
            "q_phys_reality_reason": Q_PHYS_REALITY_REASON,
            "raw_complex_quotient_is_real": False,
            "diagnostic_raw_center_quotient": {
                "real": format(raw_center_quotient.real, ".17g"),
                "imag": format(raw_center_quotient.imag, ".17g"),
            },
            "diagnostic_phase_corrected_center_quotient": {
                "real": format(physical_center_quotient.real, ".17g"),
                "imag": format(physical_center_quotient.imag, ".17g"),
            },
            "diagnostic_only_not_error_evidence": True,
        },
        "correlated_history_action": {
            "center_c_star_exact": str(CENTER),
            "residual": "Y_*(J)=D_JK(J)-c_*q_phys",
            "parameter_subdivision_count": PARAMETER_SUBDIVISIONS,
            "history_subdivision_count": len(segments),
            "history_subdivisions_per_delay_piece": (
                HISTORY_SUBDIVISIONS_PER_DELAY_PIECE
            ),
            "finite_parameter_sampling_used": False,
            "event_translation_retained": True,
            "recovery_atom_retained": True,
            "voltage_current_atom_exactly_zero_after_section_and_q_section": True,
            "exact_section_identities": {
                "D_JK_v_at_zero": "0",
                "q_phys_v_at_zero": "0",
                "Y_star_v_at_zero": "0",
                "voltage_current_atom_action": "0",
                "identity": "Y_star_v(0)=D_JK_v(0)-c_*q_phys_v(0)=0",
            },
            "finite_row_retained": True,
            "neumann_tail_retained": True,
            "neumann_tail_step_count": len(tail_iterations),
            "neumann_tail_residual_history": list(tail_iterations),
            "density_direct_and_omitted_dictionaries_kept_separate": True,
            "density_delay_piece_count": 2,
            "density_dictionary_count": 4,
            "delay_and_history_seams_retained": True,
            "guide_action_complex_box": guide_action_record,
            "maximum_correlated_residual_Y_norm_upper": (
                maximum_residual_norm_text
            ),
            "maximum_voltage_translation_term_upper": decimal_upper(
                maximum_translation_voltage
            ),
            "maximum_recovery_translation_term_upper": decimal_upper(
                maximum_translation_recovery
            ),
            "minimum_event_speed_lower": decimal_lower(minimum_event_speed),
            "stage4e_complete_measure_difference_upper": (
                measure_difference_text
            ),
            "named_error_budget": named_budget,
        },
        "oriented_action": {
            "same_row_denominator_modulus_lower": denominator_lower_text,
            "numerator_residual_modulus_upper": acceptance["numerator"],
            "quotient_radius_upper": acceptance["radius"],
            "physical_real_interval": {
                "lower": acceptance["lower"],
                "upper": acceptance["upper"],
            },
            "physical_real_interval_excludes_zero": excludes_zero,
            "complex_disk_statement": COMPLEX_DISK_STATEMENT,
            "real_intersection_statement": REAL_INTERSECTION_STATEMENT,
        },
        "stable_gap_interface": {
            "oriented_fixed_functional_action_interval_available": True,
            "oriented_fixed_functional_action_excludes_zero": excludes_zero,
            "quantitative_inner_stable_graph_available": False,
            "stable_gap_derivative_interval": None,
            "stable_gap_endpoint_intervals": None,
            "interval_newton_image": None,
            "pulse_parameter_Jc": None,
            "onset_or_routing_conclusion": None,
        },
        "theorem_statement": THEOREM_STATEMENT,
        "claim_status": claims,
    }


def build_stage5e_result(repository: Path) -> dict[str, Any]:
    repository = Path(repository).resolve()
    certificate = build_stage5e_certificate(repository)
    return {
        "certificate": certificate,
        "manifest": {
            "schema_id": SCHEMA_ID,
            "result": RESULT_RELATIVE_PATH,
            "default_command": DEFAULT_COMMAND,
            "arithmetic_scope": ARITHMETIC_SCOPE,
            "parent_sha256": {
                STAGE5B_RELATIVE_PATH: STAGE5B_SHA256,
                STAGE5C_RELATIVE_PATH: STAGE5C_SHA256,
                STAGE5D_RELATIVE_PATH: STAGE5D_SHA256,
                STAGE4D_RELATIVE_PATH: STAGE4D_SHA256,
                STAGE4E_RELATIVE_PATH: STAGE4E_SHA256,
                STAGE3_RELATIVE_PATH: STAGE3_SHA256,
            },
            "source_sha256": {
                relative: _sha256_path(repository / relative)
                for relative in SOURCE_MANIFEST
            },
            "dependency_source_sha256": {
                relative: _sha256_path(repository / relative)
                for relative in DEPENDENCY_SOURCE_MANIFEST
            },
            "certificate_sha256": canonical_sha256(certificate),
        },
    }


def _clear_stage5e_replay_caches() -> None:
    build_stage5e_certificate.cache_clear()
    build_sensitivity_error_propagation.cache_clear()
    build_remainder_propagation.cache_clear()
    build_coefficient_propagation.cache_clear()


@lru_cache(maxsize=1)
def _validated_parent_ingress(
    repository_text: str,
) -> tuple[Mapping[str, Any], Mapping[str, Any], Mapping[str, Any]]:
    repository = Path(repository_text).resolve()
    stage5d = _load_bound_json(repository, STAGE5D_RELATIVE_PATH, STAGE5D_SHA256)
    stage4e = _load_bound_json(repository, STAGE4E_RELATIVE_PATH, STAGE4E_SHA256)
    stage3 = _load_bound_json(repository, STAGE3_RELATIVE_PATH, STAGE3_SHA256)
    validate_stage5d_result(stage5d, repository)
    validate_stage4e_result(stage4e, repository)
    validate_stage3_stable_projection_result(stage3, repository)

    stage5d_certificate = _mapping(
        stage5d.get("certificate"), "source-bound Stage-5D certificate"
    )
    stage5d_claims = _mapping(
        stage5d_certificate.get("claim_status"), "source-bound Stage-5D claims"
    )
    for required in (
        "continuous_event_aligned_complete_history_J_derivative_enclosed_in_Y",
        "event_translation_term_retained_in_history_derivative",
        "section_current_voltage_J_derivative_is_exactly_zero",
    ):
        if stage5d_claims.get(required) is not True:
            raise ValueError(f"source-bound Stage-5D ingress omitted {required}")
    stage5d_history = _mapping(
        stage5d_certificate.get("continuous_Y_derivative"),
        "source-bound Stage-5D continuous derivative",
    )
    if stage5d_history.get("event_current_voltage_D_J_exact") != "0":
        raise ValueError("source-bound Stage-5D section identity changed")
    if (
        stage5d_history.get("exact_chain_rule")
        != "D_J K=(partial_J z+z_t*T_J) on the voltage history and current recovery coordinate"
    ):
        raise ValueError("source-bound Stage-5D event translation formula changed")
    stage5d_event = _mapping(
        stage5d_certificate.get("event_time_first_derivative"),
        "source-bound Stage-5D event derivative",
    )
    stage5d_speed = _mapping(
        stage5d_event.get("uniform_positive_voltage_speed"),
        "source-bound Stage-5D event speed",
    )
    _finite_decimal_interval(
        stage5d_speed.get("lower"), "source-bound Stage-5D event speed lower", positive=True
    )

    stage4e_artifact = _mapping(
        stage4e.get("artifact"), "source-bound Stage-4E artifact"
    )
    stage4e_correlated = _mapping(
        stage4e_artifact.get("continuous_history_correlated_deflation"),
        "source-bound Stage-4E correlated action",
    )
    if stage4e_correlated.get("same_adjoint_coefficients_in_numerator_and_denominator") is not True:
        raise ValueError("source-bound Stage-4E same-row identity changed")

    stage3_certificate = _mapping(
        stage3.get("certificate"), "source-bound Stage-3 certificate"
    )
    stage3_root = _mapping(
        stage3_certificate.get("root_bracket"), "source-bound Stage-3 root bracket"
    )
    if stage3_root.get("parent_disk_contains_exactly_one_real_simple_root") is not True:
        raise ValueError("source-bound Stage-3 real-simple root changed")
    stage3_column = _mapping(
        stage3_certificate.get("eigencolumn_enclosure"),
        "source-bound Stage-3 eigencolumn",
    )
    if stage3_column.get("full_infinite_grushin_eigencolumn_enclosed") is not True:
        raise ValueError("source-bound Stage-3 eigencolumn enclosure changed")
    stage3_route = _mapping(
        stage3_certificate.get("route_c_component_audit"),
        "source-bound Stage-3 Route-C component audit",
    )
    if (
        stage3_route.get("history_test_time") != HISTORY_TEST_TIME
        or stage3_route.get("history_test_time_strictly_inside_delay_interval") is not True
    ):
        raise ValueError("source-bound Stage-3 phase test time changed")
    _finite_decimal_interval(
        stage3_route.get("section_voltage_component_at_test_time_abs_lower"),
        "source-bound Stage-3 phase component lower",
        positive=True,
    )
    return stage5d, stage4e, stage3


def validate_stage5e_result(
    payload: Mapping[str, Any], repository: Path, *, recompute: bool = False
) -> None:
    if not isinstance(payload, Mapping) or set(payload) != {"certificate", "manifest"}:
        raise ValueError("Stage-5E result must contain certificate and manifest")
    certificate = _exact_mapping(
        payload.get("certificate"), "Stage-5E certificate", CERTIFICATE_KEYS
    )
    manifest = _exact_mapping(
        payload.get("manifest"), "Stage-5E manifest", MANIFEST_KEYS
    )
    if certificate.get("schema_id") != SCHEMA_ID or manifest.get("schema_id") != SCHEMA_ID:
        raise ValueError("Stage-5E schema changed")
    if certificate.get("model_id") != MODEL_ID:
        raise ValueError("Stage-5E model changed")
    if manifest.get("result") != RESULT_RELATIVE_PATH:
        raise ValueError("Stage-5E result path changed")
    if manifest.get("default_command") != DEFAULT_COMMAND:
        raise ValueError("Stage-5E command changed")
    if manifest.get("arithmetic_scope") != ARITHMETIC_SCOPE:
        raise ValueError("Stage-5E arithmetic scope changed")
    if manifest.get("certificate_sha256") != canonical_sha256(certificate):
        raise ValueError("Stage-5E certificate digest changed")
    if certificate.get("theorem_statement") != THEOREM_STATEMENT:
        raise ValueError("the Stage-5E theorem statement changed")

    repository = Path(repository).resolve()
    _, stage4e_parent, _ = _validated_parent_ingress(str(repository))
    stage4e_correlated = _mapping(
        stage4e_parent["artifact"]["continuous_history_correlated_deflation"],
        "source-bound Stage-4E correlated action",
    )

    claims = _mapping(certificate.get("claim_status"), "Stage-5E claims")
    if set(claims) != set(TRUE_FLAGS) | set(CONDITIONAL_TRUE_FLAGS) | set(FALSE_FLAGS):
        raise ValueError("Stage-5E claim ledger changed")
    for name in TRUE_FLAGS:
        if claims.get(name) is not True:
            raise ValueError(f"proved Stage-5E claim was removed: {name}")
    for name in FALSE_FLAGS:
        if claims.get(name) is not False:
            raise ValueError(f"open Stage-5E claim was promoted: {name}")
    phase = _exact_mapping(
        certificate.get("physical_phase_orientation"),
        "physical phase",
        PHASE_KEYS,
    )
    if phase.get("raw_complex_quotient_is_real") is not False:
        raise ValueError("the raw complex quotient was illicitly promoted")
    if (
        phase.get("test_functional") != f"chi(y)=y_v({HISTORY_TEST_TIME})"
        or phase.get("stored_object")
        != "q_tilde is the exact complex-gauge Stage-3 Grushin eigencolumn"
        or phase.get("gamma_definition") != "gamma=chi(q_tilde)/|chi(q_tilde)|"
        or phase.get("q_phys_definition") != "q_phys=q_tilde/gamma"
        or phase.get("f_phys_definition")
        != "f_phys(y)=gamma*ell(y)/ell(q_tilde)"
    ):
        raise ValueError("the Stage-5E physical phase definition changed")
    if phase.get("projection_identity") != PROJECTION_IDENTITY:
        raise ValueError("the Stage-5E projection identity changed")
    if phase.get("q_phys_reality_reason") != Q_PHYS_REALITY_REASON:
        raise ValueError("the Stage-5E physical-reality theorem changed")
    if phase.get("diagnostic_only_not_error_evidence") is not True:
        raise ValueError("a Stage-5E center diagnostic was promoted to proof")
    for key in (
        "diagnostic_raw_center_quotient",
        "diagnostic_phase_corrected_center_quotient",
    ):
        diagnostic = _exact_mapping(phase.get(key), key, COMPLEX_INTERVAL_KEYS)
        for component_name in COMPLEX_INTERVAL_KEYS:
            component = gmpy2.mpfr(str(diagnostic[component_name]), PRECISION_BITS)
            if not gmpy2.is_finite(component):
                raise ValueError(f"{key} must be finite")
    test_record = _exact_mapping(
        phase.get("test_component_box"),
        "test component box",
        COMPLEX_INTERVAL_KEYS,
    )
    test_box = DirectedComplexInterval(
        _parse_interval_record(_mapping(test_record.get("real"), "test real"), "test real"),
        _parse_interval_record(_mapping(test_record.get("imag"), "test imag"), "test imag"),
    )
    modulus_record = _mapping(
        phase.get("test_component_modulus_interval"), "test modulus"
    )
    modulus = _parse_interval_record(modulus_record, "test modulus")
    if modulus.lower <= 0 or modulus.lower > test_box.lower_abs() or modulus.upper < test_box.upper_abs():
        raise ValueError("the Stage-5E nonzero phase-component modulus changed")
    expected_gamma = DirectedComplexInterval(
        test_box.real / modulus, test_box.imag / modulus
    )
    gamma_record = _exact_mapping(
        phase.get("gamma_box"), "gamma box", COMPLEX_INTERVAL_KEYS
    )
    gamma = DirectedComplexInterval(
        _parse_interval_record(_mapping(gamma_record.get("real"), "gamma real"), "gamma real"),
        _parse_interval_record(_mapping(gamma_record.get("imag"), "gamma imag"), "gamma imag"),
    )
    if (
        gamma.real.lower > expected_gamma.real.lower
        or gamma.real.upper < expected_gamma.real.upper
        or gamma.imag.lower > expected_gamma.imag.lower
        or gamma.imag.upper < expected_gamma.imag.upper
    ):
        raise ValueError("the Stage-5E gamma box does not contain the phase quotient")
    (
        source_test_record,
        source_modulus_record,
        source_gamma_record,
    ) = _source_bound_phase_records(str(repository))
    if (
        test_record != source_test_record
        or modulus_record != source_modulus_record
        or gamma_record != source_gamma_record
    ):
        raise ValueError("the Stage-5E physical phase triple is not source-bound")
    action = _exact_mapping(
        certificate.get("correlated_history_action"),
        "correlated action",
        ACTION_KEYS,
    )
    if action.get("center_c_star_exact") != str(CENTER):
        raise ValueError("the Stage-5E residual center changed")
    if action.get("residual") != "Y_*(J)=D_JK(J)-c_*q_phys":
        raise ValueError("the Stage-5E c*q_phys residual changed")
    for required in (
        "event_translation_retained",
        "recovery_atom_retained",
        "voltage_current_atom_exactly_zero_after_section_and_q_section",
        "finite_row_retained",
        "neumann_tail_retained",
        "density_direct_and_omitted_dictionaries_kept_separate",
        "delay_and_history_seams_retained",
    ):
        if action.get(required) is not True:
            raise ValueError(f"the Stage-5E action omitted {required}")
    if (
        action.get("parameter_subdivision_count") != PARAMETER_SUBDIVISIONS
        or action.get("history_subdivision_count")
        != 2 * HISTORY_SUBDIVISIONS_PER_DELAY_PIECE
        or action.get("history_subdivisions_per_delay_piece")
        != HISTORY_SUBDIVISIONS_PER_DELAY_PIECE
    ):
        raise ValueError("the Stage-5E exact subdivision counts changed")
    tail_history = action.get("neumann_tail_residual_history")
    if (
        not isinstance(tail_history, Sequence)
        or isinstance(tail_history, (str, bytes))
        or len(tail_history) == 0
        or action.get("neumann_tail_step_count") != len(tail_history)
    ):
        raise ValueError("the Stage-5E Neumann-tail history changed")
    for index, value in enumerate(tail_history):
        _finite_decimal_interval(
            value, f"Stage-5E Neumann-tail history {index}", positive=False
        )
    identities = _mapping(
        action.get("exact_section_identities"), "exact section identities"
    )
    if identities != {
        "D_JK_v_at_zero": "0",
        "q_phys_v_at_zero": "0",
        "Y_star_v_at_zero": "0",
        "voltage_current_atom_action": "0",
        "identity": "Y_star_v(0)=D_JK_v(0)-c_*q_phys_v(0)=0",
    }:
        raise ValueError("the exact Stage-5E section atom identity changed")
    if action.get("density_delay_piece_count") != 2 or action.get("density_dictionary_count") != 4:
        raise ValueError("the complete Stage-5E density pieces changed")
    residual_norm_interval = _finite_decimal_interval(
        action.get("maximum_correlated_residual_Y_norm_upper"),
        "Stage-5E correlated residual norm",
        positive=True,
    )
    _finite_decimal_interval(
        action.get("maximum_voltage_translation_term_upper"),
        "Stage-5E voltage translation upper",
        positive=False,
    )
    _finite_decimal_interval(
        action.get("maximum_recovery_translation_term_upper"),
        "Stage-5E recovery translation upper",
        positive=False,
    )
    _finite_decimal_interval(
        action.get("minimum_event_speed_lower"),
        "Stage-5E event speed lower",
        positive=True,
    )
    source_measure_text = str(stage4e_correlated["history_measure_difference_upper"])
    if action.get("stage4e_complete_measure_difference_upper") != source_measure_text:
        raise ValueError("the Stage-5E complete measure difference is not source-bound")
    measure_difference_interval = _finite_decimal_interval(
        source_measure_text, "Stage-5E complete measure difference", positive=True
    )

    budget = _exact_mapping(
        action.get("named_error_budget"), "named error budget", BUDGET_KEYS
    )
    if budget.get("coverage_ledger_is_nested_or_overlapping_and_not_additive") is not True:
        raise ValueError("the Stage-5E coverage ledger was treated as additive")
    ledger = _mapping(budget.get("coverage_ledger"), "coverage ledger")
    if ledger != COVERAGE_LEDGER or set(ledger) != set(COVERAGE_LEDGER_NAMES):
        raise ValueError("the eight-mechanism Stage-5E coverage ledger changed")
    components = _exact_mapping(
        budget.get("common_measure_difference_components"),
        "common measure difference components",
        COMMON_COMPONENT_KEYS,
    )
    for required in (
        "neumann_tail_remainder_covered",
        "finite_row_enclosure_covered",
        "periodic_orbit_and_advanced_covariance_covered",
        "guide_exact_atom_density_difference_covered",
    ):
        if components.get(required) is not True:
            raise ValueError(f"the Stage-5E common measure omitted {required}")
    if components.get("coverage_statement") != COMMON_MEASURE_COVERAGE_STATEMENT:
        raise ValueError("the Stage-5E common-measure coverage statement changed")
    for field in (
        "finite_adjoint_l1_error_upper",
        "adjoint_fourier_tail_l1_error_upper",
        "adjoint_density_basis_shift_upper",
        "density_convolution_rounding_guard_upper",
    ):
        source_value = str(stage4e_correlated[field])
        if components.get(field) != source_value:
            raise ValueError(f"the Stage-5E common measure field is not source-bound: {field}")
        _finite_decimal_interval(
            source_value, f"Stage-5E common measure field {field}", positive=False
        )
    joint_upper = _mapping(
        budget.get("joint_envelope_upper"), "joint numeric envelopes"
    )
    if set(joint_upper) != set(JOINT_ENVELOPE_NAMES):
        raise ValueError("the two Stage-5E joint envelopes changed")
    if budget.get("joint_sum_order") != list(JOINT_ENVELOPE_NAMES):
        raise ValueError("the Stage-5E joint-envelope sum order changed")
    if budget.get("sum_identity") != "r_A=r_joint_guide+r_joint_measure":
        raise ValueError("the Stage-5E joint-envelope identity changed")
    for name in JOINT_ENVELOPE_NAMES:
        _finite_decimal_interval(
            joint_upper[name], f"Stage-5E joint envelope {name}", positive=False
        )
    guide_record = _exact_mapping(
        action.get("guide_action_complex_box"),
        "guide action complex box",
        COMPLEX_INTERVAL_KEYS,
    )
    guide_box = DirectedComplexInterval(
        _parse_interval_record(_mapping(guide_record.get("real"), "guide real"), "guide real"),
        _parse_interval_record(_mapping(guide_record.get("imag"), "guide imag"), "guide imag"),
    )
    joint_guide = DirectedInterval.from_decimal(
        str(joint_upper["r_joint_guide"]), PRECISION_BITS
    )
    if joint_guide.lower < guide_box.upper_abs():
        raise ValueError("r_joint_guide does not cover the guide action box")
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
        required_measure = (
            measure_difference_interval.upper * residual_norm_interval.upper
        )
    joint_measure = DirectedInterval.from_decimal(
        str(joint_upper["r_joint_measure"]), PRECISION_BITS
    )
    if joint_measure.lower < required_measure:
        raise ValueError("r_joint_measure does not cover measure difference times residual norm")
    if action.get("finite_parameter_sampling_used") is not False:
        raise ValueError("finite sampling was promoted in Stage-5E")
    oriented = _exact_mapping(
        certificate.get("oriented_action"), "oriented action", ORIENTED_KEYS
    )
    if oriented.get("complex_disk_statement") != COMPLEX_DISK_STATEMENT:
        raise ValueError("the Stage-5E complex-disk statement changed")
    if oriented.get("real_intersection_statement") != REAL_INTERSECTION_STATEMENT:
        raise ValueError("the Stage-5E real-intersection theorem changed")
    source_denominator_text = decimal_lower(
        DirectedInterval.from_decimal(
            str(stage4e_correlated["f_q_modulus_lower"]), PRECISION_BITS
        ).lower
    )
    if oriented.get("same_row_denominator_modulus_lower") != source_denominator_text:
        raise ValueError("the Stage-5E denominator is not the source-bound Stage-4E lower")
    _finite_decimal_interval(
        source_denominator_text, "Stage-5E same-row denominator lower", positive=True
    )
    recomputed = _oriented_arithmetic(
        {name: str(joint_upper[name]) for name in JOINT_ENVELOPE_NAMES},
        str(oriented.get("same_row_denominator_modulus_lower")),
    )
    if budget.get("total_numerator_radius_upper") != recomputed["numerator"]:
        raise ValueError("the Stage-5E component sum does not equal the numerator")
    if oriented.get("numerator_residual_modulus_upper") != recomputed["numerator"]:
        raise ValueError("the Stage-5E numerator was not recomputed from components")
    if oriented.get("quotient_radius_upper") != recomputed["radius"]:
        raise ValueError("the Stage-5E quotient radius arithmetic changed")
    interval_record = _mapping(oriented.get("physical_real_interval"), "real interval")
    if (
        interval_record.get("lower") != recomputed["lower"]
        or interval_record.get("upper") != recomputed["upper"]
    ):
        raise ValueError("the Stage-5E c_* plus/minus radius interval changed")
    interval = _parse_interval_record(interval_record, "real interval")
    excludes = not interval.contains_zero()
    if oriented.get("physical_real_interval_excludes_zero") is not excludes:
        raise ValueError("the Stage-5E exclusion flag is inconsistent")
    for name in CONDITIONAL_TRUE_FLAGS:
        if claims.get(name) is not excludes:
            raise ValueError("the Stage-5E conditional claim is inconsistent")
    stable = _exact_mapping(
        certificate.get("stable_gap_interface"),
        "stable-gap interface",
        STABLE_INTERFACE_KEYS,
    )
    if stable != {
        "oriented_fixed_functional_action_interval_available": True,
        "oriented_fixed_functional_action_excludes_zero": excludes,
        "quantitative_inner_stable_graph_available": False,
        "stable_gap_derivative_interval": None,
        "stable_gap_endpoint_intervals": None,
        "interval_newton_image": None,
        "pulse_parameter_Jc": None,
        "onset_or_routing_conclusion": None,
    }:
        raise ValueError("the Stage-5E stable-gap interface was promoted or desynchronized")
    parent_sha = _mapping(manifest.get("parent_sha256"), "parent hashes")
    expected_parent_sha = {
        STAGE5B_RELATIVE_PATH: STAGE5B_SHA256,
        STAGE5C_RELATIVE_PATH: STAGE5C_SHA256,
        STAGE5D_RELATIVE_PATH: STAGE5D_SHA256,
        STAGE4D_RELATIVE_PATH: STAGE4D_SHA256,
        STAGE4E_RELATIVE_PATH: STAGE4E_SHA256,
        STAGE3_RELATIVE_PATH: STAGE3_SHA256,
    }
    if set(parent_sha) != set(expected_parent_sha):
        raise ValueError("the Stage-5E parent hash key set changed")
    for relative, expected in expected_parent_sha.items():
        if parent_sha.get(relative) != expected or _sha256_path(repository / relative) != expected:
            raise ValueError(f"Stage-5E parent changed: {relative}")
    for group, expected_relatives in (
        ("source_sha256", SOURCE_MANIFEST),
        ("dependency_source_sha256", DEPENDENCY_SOURCE_MANIFEST),
    ):
        hashes = _mapping(manifest.get(group), group)
        if set(hashes) != set(expected_relatives):
            raise ValueError(f"the Stage-5E {group} key set changed")
        for relative in expected_relatives:
            expected = hashes[relative]
            if _sha256_path(repository / str(relative)) != expected:
                raise ValueError(f"Stage-5E source changed: {relative}")
    if recompute:
        _clear_stage5e_replay_caches()
        rebuilt = build_stage5e_result(repository)
        if canonical_sha256(rebuilt) != canonical_sha256(payload):
            raise ValueError("the Stage-5E canonical JSON replay changed")
