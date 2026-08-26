"""Stage-3H strict sizes for the two phase-combined outer rows.

For ``t=T-delta`` and ``u=t-ell`` the voltage row is written directly as

    p_v(delta,ell) = e_v S(delta,ell)
        - alpha(delta) e_v S(0,delta+ell),

where ``S`` is the Stage-3G moving-frame resolvent and
``alpha(delta)=q_v(-delta)/q_v(0)``.  The recovery row is

    p_w(ell) = e_w S(0,ell) - beta e_v S(0,ell).

This module keeps each subtraction inside one Bernstein row.  On a local
patch the phase ratio is centered first; only its rigorously enclosed local
radius is paid after the signed center subtraction.  When ``delta+ell``
crosses a lag-chart seam, the two one-sided terminal-row polynomials are
kept separate.  Each physical triangle is bounded by its full-patch
polynomial superset, so no interpolation is performed across the seam.

The Stage-3G Green bootstrap supplies a strict uniform row error between the
piecewise candidate resolvent and the exact guide resolvent.  It is added
only after the output-specific signed candidate bound has been formed.  The
result is a strict size certificate, not yet the final continuous signed-
density total-variation certificate; consequently E_voltage, E_recovery and
the arbitrary-C0 return gate remain open in this stage.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from decimal import Decimal, InvalidOperation
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
import json
import math
import os
from pathlib import Path
import platform
from typing import Any, Mapping, Sequence

from flint import arb, arb_mat, ctx as arb_ctx
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
)
from canard_control.leaky_outer_high_resolution import (
    RESULT_RELATIVE_PATH as OUTER_RESULT_RELATIVE_PATH,
    validate_outer_high_resolution_artifact,
)
from canard_control.leaky_outer_resolvent_stage3g_tensor import (
    COEFFICIENT_DEGREE,
    DELTA_CELL_COUNT,
    DELTA_DEGREE,
    FOURIER_CUTOFF,
    LAG_DEGREE,
    PRECISION_BITS,
    SUBDIVISION_PARTS,
    _TensorGuide,
    _arb_fraction,
    _arb_interval,
    _candidate_patch,
    _chebyshev_power_polynomials,
    _chebyshev_to_bernstein_matrix,
    _elevate,
    _exact_arb_float,
    _mapping,
    _matrix_max_abs,
    _patch_centers,
    _power_to_bernstein_matrix,
    _two_component_row_max,
)
from canard_control.leaky_outer_signed_kernel_stage2 import (
    RESULT_RELATIVE_PATH as STAGE2_RESULT_RELATIVE_PATH,
)
from canard_control.leaky_outer_signed_row_stage3f_adjoint import (
    RESULT_RELATIVE_PATH as STAGE3F_RESULT_RELATIVE_PATH,
)
from canard_control.leaky_periodic_validation import _build_leaky_base_sequences


SCHEMA_ID = "leaky-outer-combined-row-stage3h-size-v2"
MODEL_ID = "autonomous-leaky-recovery-two-delay-fhn-bistable-proposal"
BRANCH = "outer_pulse"
SOURCE_RELATIVE_PATH = (
    "src/canard_control/leaky_outer_combined_row_stage3h_size.py"
)
GENERATOR_RELATIVE_PATH = (
    "experiments/leaky_outer_combined_row_stage3h_size.py"
)
RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_outer_combined_row_stage3h_size.json"
)
NOTE_RELATIVE_PATH = "docs/leaky-outer-combined-row-stage3h-size.md"
TEST_RELATIVE_PATH = "tests/test_leaky_outer_combined_row_stage3h_size.py"
SOURCE_MANIFEST = (
    SOURCE_RELATIVE_PATH,
    GENERATOR_RELATIVE_PATH,
    NOTE_RELATIVE_PATH,
    TEST_RELATIVE_PATH,
    "src/canard_control/directed_interval.py",
    "src/canard_control/leaky_outer_high_resolution.py",
    "src/canard_control/leaky_outer_resolvent_stage3g_tensor.py",
    "src/canard_control/leaky_outer_signed_kernel_stage2.py",
    "src/canard_control/leaky_outer_signed_row_stage3f_adjoint.py",
    "src/canard_control/leaky_periodic_validation.py",
)
DEFAULT_COMMAND = (
    "OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONPATH=build/testdeps:src "
    "/usr/bin/python3 experiments/leaky_outer_combined_row_stage3h_size.py"
)
ARITHMETIC_SCOPE = (
    "output-specific signed row algebra; exact-dyadic Stage-3G candidate "
    "coefficients; 192-bit Arb Chebyshev/power/Bernstein transforms; "
    "192-bit outward Fourier-Taylor phase-ratio patches; one-sided event "
    "charts bounded on full-patch supersets; strict Stage-3G resolvent error"
)
ROW_SCOPE = (
    "center binary-orbit phase ratios applied to the exact guide resolvent; "
    "exact-orbit phase and coefficient transfer is recorded only in the "
    "linear frontier"
)
STAGE3G_CANDIDATE_ERROR_SEMANTICS = "||S_guide-S_hat||_row"
CONCLUSION = (
    "the voltage and recovery center-guide phase-combined advanced rows "
    "now have strict output-specific 192-bit Bernstein sizes, with phase "
    "ratios centered inside each signed row and event seams kept one-sided.  "
    "Exact-orbit phase and coefficient effects remain in the transfer "
    "frontier.  The remaining minimal linear gap is the directed center signed-"
    "density cell integral that must validate the reserved 0.01 "
    "transfer from the Stage-2 discrete shadow; E_voltage,E_recovery "
    "and arbitrary-C0 contraction therefore remain open here"
)

STAGE3G_RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_outer_resolvent_stage3g_tensor.json"
)
STAGE3G_RESULT_SHA256 = (
    "52d2c4df0cea7b6d98d898669e45ef54bfed1799965b2cff92161e84bd78ce13"
)
STAGE3F_RESULT_SHA256 = (
    "d09832c47370dee6588cc0ee7396ca6fe75c1f283785a799682f302427344eee"
)
STAGE2_RESULT_SHA256 = (
    "f4742db560c5de29072adfb0b963d5a21e993fed5a949a2180dcc6d0b355011f"
)
OUTER_RESULT_SHA256 = (
    "d888916fed919f1515dd31ab851b2229816ea373365fa0221b1e345580f165a7"
)
STAGE3G_SCHEMA_ID = "leaky-outer-resolvent-stage3g-tensor-v2"
STAGE3F_SCHEMA_ID = "leaky-outer-signed-row-stage3f-adjoint-v1"
STAGE2_SCHEMA_ID = "leaky-outer-signed-kernel-stage2-v1"
PARENT_MANIFEST_FIELDS = frozenset(
    {
        "certificate_sha256",
        "default_command",
        "environment",
        "result",
        "schema_id",
        "source_sha256",
    }
)
PINNED_OPENBLAS_NUM_THREADS = "1"
ORDINARY_RECTANGLE_COUNT = 730
TERMINAL_CLIPPED_RECTANGLE_COUNT = 40
LOCAL_PATCH_COUNT = 12320
EVENT_SEAM_PATCH_COUNT = 3080
TWO_SIDED_EVENT_SEAM_PATCH_COUNT = 3000
TERMINAL_LINE_ONE_SIDED_EVENT_PATCH_COUNT = 80
ONE_SIDED_VOLTAGE_ROW_EVALUATION_COUNT = 15200
RECOVERY_ONE_DIMENSIONAL_PATCH_COUNT = 192
EVENT_TRIANGLE_ENCLOSURE = (
    "each one-sided polynomial is bounded on its full local square, "
    "a superset of the corresponding physical seam triangle"
)

TRUE_FLAGS = (
    "stage3g_residual_green_parent_digest_validated",
    "stage3g_parent_source_manifest_validated",
    "stage3f_transfer_budget_parent_digest_validated",
    "stage2_discrete_shadow_parent_digest_validated",
    "output_specific_voltage_signed_row_formed_before_norm",
    "output_specific_recovery_signed_row_formed_before_norm",
    "phase_ratio_centered_inside_each_signed_row_patch",
    "all_730_ordinary_resolvent_rectangles_consumed",
    "all_40_terminal_clipped_rectangles_consumed",
    "delta_plus_lag_event_seams_split_into_one_sided_charts",
    "event_triangles_bounded_by_valid_full_patch_supersets",
    "candidate_coefficients_treated_as_exact_dyadics",
    "row_size_bernstein_arithmetic_outward_192_bit",
    "fourier_phase_ratio_tail_and_taylor_remainders_included",
    "strict_stage3g_resolvent_candidate_error_consumed",
    "direct_center_guide_phase_combined_voltage_row_uniform_bound_validated",
    "direct_center_guide_phase_combined_recovery_row_uniform_bound_validated",
    "direct_center_guide_phase_combined_voltage_component_bounds_validated",
)
FALSE_FLAGS = (
    "continuous_center_signed_density_TV_reserve_validated",
    "continuous_signed_density_total_variation_validated",
    "voltage_shadow_transfer_error_validated",
    "recovery_shadow_transfer_error_validated",
    "arbitrary_c0_linear_return_contraction_validated",
    "nonlinear_phase_chart_validated_on_ambient_tube",
    "outer_nonlinear_return_contraction_validated",
    "outer_quantitative_attracting_tube_validated",
    "outer_pulse_capture_validated",
    "physical_pulse_onset_validated",
)

RESULT_MANIFEST_FIELDS = PARENT_MANIFEST_FIELDS
ENVIRONMENT_FIELDS = frozenset(
    {
        "python",
        "platform",
        "numpy",
        "scipy",
        "gmpy2",
        "python_flint",
        "arb_precision_bits",
        "openblas_num_threads",
    }
)
GEOMETRY_FIELDS = frozenset(
    {
        "ordinary_rectangle_count",
        "terminal_clipped_rectangle_count",
        "local_patch_count",
        "event_seam_patch_count",
        "two_sided_event_seam_patch_count",
        "terminal_line_one_sided_event_patch_count",
        "one_sided_voltage_row_evaluation_count",
        "recovery_one_dimensional_patch_count",
        "event_triangle_enclosure",
    }
)
PHASE_FIELDS = frozenset(
    {
        "voltage_local_ratio_radius_maximum_upper",
        "voltage_ratio_absolute_maximum_upper",
        "recovery_ratio_center_binary64_hex",
        "recovery_ratio_radius_upper",
        "recovery_ratio_absolute_upper",
        "fourier_cutoff",
        "taylor_degree",
    }
)
SIZE_FIELDS = frozenset(
    {
        "stage3g_resolvent_candidate_row_error_upper",
        "stage3g_resolvent_candidate_row_error_semantics",
        "voltage_combined_p_uniform_upper",
        "voltage_combined_p_voltage_component_upper",
        "voltage_uniform_maximizer",
        "recovery_combined_p_uniform_upper",
        "recovery_combined_p_voltage_component_upper",
        "recovery_uniform_maximizer",
        "signed_center_subtraction_precedes_row_norm",
        "ratio_radius_paid_after_signed_center_subtraction",
    }
)
VOLTAGE_MAXIMIZER_FIELDS = frozenset(
    {
        "delta_cell",
        "lag_cell",
        "delta_patch_center",
        "lag_patch_center",
        "terminal_side",
        "q_cell",
        "event_seam_patch",
        "terminal_clipped_cell",
    }
)
RECOVERY_MAXIMIZER_FIELDS = frozenset(
    {"lag_cell", "lag_patch_center"}
)
FRONTIER_FIELDS = frozenset(
    {
        "rows",
        "strict_sizes_validated",
        "continuous_center_TV_reserve_validated",
        "conditional_only_until_center_TV_cell_integral_is_validated",
    }
)
FRONTIER_ROW_FIELDS = frozenset(
    {
        "stage2_shadow_upper",
        "center_TV_transfer_reserve_not_yet_validated",
        "orbit_coefficient_row_residual_upper",
        "direct_delayed_density_cost_upper",
        "orbit_cost_at_strict_stage3g_green_upper",
        "phase_ratio_boundary_cost_at_strict_stage3g_boundary_upper",
        "combined_residual_and_atom_cost_upper",
        "conditional_total_if_center_TV_reserve_is_validated",
        "conditional_contraction_below_one",
    }
)
TRANSFER_ERROR_FIELDS = frozenset({"E_voltage", "E_recovery", "E_phase"})
TRANSFER_GATE_FIELDS = frozenset(
    {
        "strict_combined_row_uniform_sizes_validated",
        "continuous_center_signed_density_TV_reserve_validated",
        "linear_return_gate_evaluated",
        "arbitrary_c0_linear_contraction_closes",
        "nonlinear_outer_attraction_closes",
    }
)


def _sha256_path(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def canonical_sha256(value: Any) -> str:
    encoded = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("ascii")
    return sha256(encoded).hexdigest()


def _require_exact_keys(
    value: Mapping[str, Any], expected: frozenset[str] | set[str], name: str
) -> None:
    if set(value) != set(expected):
        raise ValueError(f"the {name} schema changed")


def _expected_environment() -> dict[str, Any]:
    return {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "gmpy2": gmpy2.__version__,
        "python_flint": __import__("flint").__version__,
        "arb_precision_bits": PRECISION_BITS,
        "openblas_num_threads": os.environ.get("OPENBLAS_NUM_THREADS"),
    }


def _decimal(value: Any, name: str) -> Decimal:
    try:
        answer = Decimal(str(value))
    except (InvalidOperation, ValueError) as error:
        raise ValueError(f"{name} must be a finite decimal") from error
    if not answer.is_finite():
        raise ValueError(f"{name} must be a finite decimal")
    return answer


def _require_unique_disjoint_flags(
    true_flags: Sequence[str], false_flags: Sequence[str]
) -> None:
    if len(true_flags) != len(set(true_flags)):
        raise ValueError("the Stage-3H true-flag registry contains duplicates")
    if len(false_flags) != len(set(false_flags)):
        raise ValueError("the Stage-3H false-flag registry contains duplicates")
    overlap = set(true_flags) & set(false_flags)
    if overlap:
        raise ValueError(f"the Stage-3H flag registries overlap: {sorted(overlap)}")


def _load_parent(repository: Path, relative: str, expected: str) -> Mapping[str, Any]:
    path = repository / relative
    if _sha256_path(path) != expected:
        raise ValueError(f"a Stage-3H parent changed: {relative}")
    return _mapping(json.loads(path.read_text()), relative)


def _validate_parent_artifact_lock(
    payload: Mapping[str, Any],
    repository: Path,
    *,
    label: str,
    schema_id: str,
    result_relative_path: str,
) -> Mapping[str, Any]:
    if set(payload) != {"certificate", "manifest"}:
        raise ValueError(f"the {label} parent top-level schema changed")
    certificate = _mapping(payload.get("certificate"), f"{label} certificate")
    manifest = _mapping(payload.get("manifest"), f"{label} manifest")
    _require_exact_keys(manifest, PARENT_MANIFEST_FIELDS, f"{label} manifest")
    if (
        manifest.get("schema_id") != schema_id
        or manifest.get("result") != result_relative_path
        or certificate.get("schema_id") != schema_id
    ):
        raise ValueError(f"the {label} parent identity changed")
    if canonical_sha256(certificate) != manifest.get("certificate_sha256"):
        raise ValueError(f"the {label} parent certificate digest changed")
    sources = _mapping(manifest.get("source_sha256"), f"{label} source manifest")
    if not sources:
        raise ValueError(f"the {label} parent source manifest is empty")
    root = repository.resolve()
    for relative, expected in sources.items():
        if not isinstance(relative, str) or not isinstance(expected, str):
            raise ValueError(f"the {label} source manifest is malformed")
        path = (root / relative).resolve()
        if path != root and root not in path.parents:
            raise ValueError(f"the {label} source escaped the repository")
        if not path.is_file() or _sha256_path(path) != expected:
            raise ValueError(f"a {label} runtime source changed: {relative}")
    return certificate


def _arb_upper_float(value: arb) -> float:
    return math.nextafter(float(value.abs_upper()), math.inf)


def _upper_record(value: arb) -> str:
    return format(_arb_upper_float(value), ".17g")


def _mpfr_upper_arb(value: gmpy2.mpfr) -> arb:
    return arb(decimal_upper(value, 70))


def _mpfr_lower_arb(value: gmpy2.mpfr) -> arb:
    return arb(decimal_lower(value, 70))


def _column_from_values(values: Sequence[arb]) -> arb_mat:
    return arb_mat([[value] for value in values])


def _series_real_box_at_precision(
    coefficients: Mapping[int, DirectedComplexInterval],
    phase: DirectedInterval,
) -> DirectedInterval:
    """Evaluate a real Fourier series at the caller's interval precision."""

    zero = DirectedInterval.from_decimal(0, phase.precision)
    total = DirectedComplexInterval(zero, zero)
    pi = pi_interval(phase.precision)
    for mode, coefficient in coefficients.items():
        angle = pi * (2 * int(mode)) * phase
        total = total + coefficient * complex_unit_interval(angle)
    return total.real


def _phase_ratio_patch(
    sequence: Mapping[int, Any],
    *,
    center_time: DirectedInterval,
    period: DirectedInterval,
    h: DirectedInterval,
    denominator: DirectedInterval,
    binary_center: float,
) -> tuple[arb, arb, arb]:
    """Return exact-dyadic center, strict radius, and strict absolute bound."""

    zero = DirectedInterval.from_decimal(0, PRECISION_BITS)
    one = DirectedInterval.from_decimal(1, PRECISION_BITS)
    pi = pi_interval(PRECISION_BITS)
    scale = DirectedInterval.from_decimal(SUBDIVISION_PARTS, PRECISION_BITS)
    coefficients = [
        DirectedComplexInterval.zero(PRECISION_BITS)
        for _ in range(COEFFICIENT_DEGREE + 1)
    ]
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
        tail = gmpy2.mpfr(0)
        remainder = gmpy2.mpfr(0)
        factorial = gmpy2.fac(COEFFICIENT_DEGREE + 1)
    for mode, value in sequence.items():
        magnitude = value.upper_abs()
        if abs(mode) > FOURIER_CUTOFF:
            with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
                tail += magnitude
            continue
        angle = 2 * pi * mode * center_time / period
        factor = value * complex_unit_interval(angle)
        lam = DirectedComplexInterval(
            zero,
            -(pi * mode * h / (period * scale)),
        )
        coefficients[0] = coefficients[0] + factor
        for degree in range(1, COEFFICIENT_DEGREE + 1):
            factor = factor * lam * (one / degree)
            coefficients[degree] = coefficients[degree] + factor
        with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
            maximum_argument = (
                pi.upper
                * abs(mode)
                * h.upper
                / (period.lower * SUBDIVISION_PARTS)
            )
            remainder += (
                magnitude
                * maximum_argument ** (COEFFICIENT_DEGREE + 1)
                / factorial
            )
    power = [_arb_interval(value.real) for value in coefficients]
    bernstein = _power_to_bernstein_matrix(COEFFICIENT_DEGREE) * _column_from_values(
        power
    )
    denominator_arb = _arb_interval(denominator)
    bernstein /= denominator_arb
    center = _exact_arb_float(binary_center)
    radius = arb(0)
    for index in range(bernstein.nrows()):
        radius = max(radius, (bernstein[index, 0] - center).abs_upper())
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
        analytic_remainder = (tail + remainder) / denominator.lower
    radius += _mpfr_upper_arb(analytic_remainder)
    absolute = center.abs_upper() + radius
    return center, radius, absolute


def _collapsed_terminal_chebyshev(
    coefficients: np.ndarray, row: int, column: int
) -> tuple[arb, ...]:
    values: list[arb] = []
    for lag_degree in range(LAG_DEGREE + 1):
        total = arb(0)
        for delta_degree in range(DELTA_DEGREE + 1):
            value = _exact_arb_float(
                coefficients[delta_degree, lag_degree, row, column]
            )
            total += value if delta_degree % 2 == 0 else -value
        values.append(total)
    return tuple(values)


def _composed_terminal_component(
    lag_chebyshev: Sequence[arb], z_center: Fraction
) -> arb_mat:
    """Enclose f(z_center+(X+Y)/parts) on the full local square."""

    chebyshev_power = _chebyshev_power_polynomials(LAG_DEGREE)
    univariate = [arb(0) for _ in range(LAG_DEGREE + 1)]
    for degree, coefficient in enumerate(lag_chebyshev):
        for power, rational in enumerate(chebyshev_power[degree]):
            univariate[power] += coefficient * _arb_fraction(rational)
    scale = Fraction(1, SUBDIVISION_PARTS)
    tensor = [[arb(0) for _ in range(LAG_DEGREE + 1)] for _ in range(LAG_DEGREE + 1)]
    for degree, coefficient in enumerate(univariate):
        for x_power in range(degree + 1):
            for y_power in range(degree - x_power + 1):
                constant_power = degree - x_power - y_power
                multinomial = Fraction(
                    math.factorial(degree),
                    math.factorial(x_power)
                    * math.factorial(y_power)
                    * math.factorial(constant_power),
                )
                weight = (
                    multinomial
                    * z_center**constant_power
                    * scale ** (x_power + y_power)
                )
                tensor[x_power][y_power] += coefficient * _arb_fraction(weight)
    transform = _power_to_bernstein_matrix(LAG_DEGREE)
    return transform * arb_mat(tensor) * transform.transpose()


def _one_dimensional_terminal_component(
    lag_chebyshev: Sequence[arb], center: Fraction
) -> arb_mat:
    transform = _chebyshev_to_bernstein_matrix(
        LAG_DEGREE, center, Fraction(1, SUBDIVISION_PARTS)
    )
    return transform * _column_from_values(lag_chebyshev)


def _signed_tensor_bounds(
    current: tuple[arb_mat, arb_mat],
    terminal: tuple[arb_mat, arb_mat],
    center: arb,
    radius: arb,
) -> tuple[arb, arb]:
    shape = (LAG_DEGREE + 1, LAG_DEGREE + 1)
    current_first = _elevate(current[0], *shape)
    current_second = _elevate(current[1], *shape)
    signed_first = current_first - terminal[0] * center
    signed_second = current_second - terminal[1] * center
    center_uniform = _two_component_row_max(signed_first, signed_second)
    terminal_uniform = _two_component_row_max(terminal[0], terminal[1])
    uniform = center_uniform + radius * terminal_uniform
    voltage_component = _matrix_max_abs(signed_first) + radius * _matrix_max_abs(
        terminal[0]
    )
    return uniform, voltage_component


def _signed_vector_bounds(
    recovery: tuple[arb_mat, arb_mat],
    voltage: tuple[arb_mat, arb_mat],
    center: arb,
    radius: arb,
) -> tuple[arb, arb]:
    first = recovery[0] - voltage[0] * center
    second = recovery[1] - voltage[1] * center
    center_uniform = arb(0)
    for index in range(first.nrows()):
        center_uniform = max(
            center_uniform,
            first[index, 0].abs_upper() + second[index, 0].abs_upper(),
        )
    voltage_uniform = arb(0)
    for index in range(voltage[0].nrows()):
        voltage_uniform = max(
            voltage_uniform,
            voltage[0][index, 0].abs_upper()
            + voltage[1][index, 0].abs_upper(),
        )
    uniform = center_uniform + radius * voltage_uniform
    component = _matrix_max_abs(first) + radius * _matrix_max_abs(voltage[0])
    return uniform, component


@dataclass(frozen=True)
class OuterCombinedRowStage3HSize:
    schema_id: str
    model_id: str
    branch: str
    arithmetic_scope: str
    precision_bits: int
    row_scope: str
    parent_result_sha256: dict[str, str]
    chart_geometry: dict[str, Any]
    phase_ratio_enclosures: dict[str, Any]
    combined_row_size: dict[str, Any]
    linear_transfer_frontier: dict[str, Any]
    transfer_errors: dict[str, str | None]
    transfer_gate: dict[str, bool]
    claim_status: dict[str, bool]
    conclusion: str


def _frontier_rows_from_size_records(
    sizes: Mapping[str, Any],
    stage3g_certificate: Mapping[str, Any],
    stage3f_certificate: Mapping[str, Any],
    stage2_certificate: Mapping[str, Any],
) -> dict[str, Any]:
    """Recompute the conditional ledger from its serialized proof inputs."""

    green = _mapping(
        stage3g_certificate.get("green_bootstrap"), "Stage-3G Green bootstrap"
    )
    combined = _mapping(
        stage3g_certificate.get("phase_combination_target"),
        "Stage-3G combined residual",
    )
    defects = _mapping(
        stage3f_certificate.get("exact_defect_budget"), "Stage-3F defects"
    )
    exact_green = arb(str(green["bootstrapped_exact_green_upper"]))
    exact_boundary = arb(str(green["bootstrapped_exact_boundary_upper"]))
    lift = arb(str(defects["exact_history_density_lift_factor_upper"]))
    rank_one = arb(str(defects["rank_one_advanced_operator_variation_upper"]))
    full_period = arb(str(defects["full_period_matrix_variation_upper"]))
    delay_sum = arb(str(defects["delay_sum_upper"]))
    delayed_variation = arb(
        str(defects["delayed_physical_coefficient_variation_upper"])
    )
    reserve = arb("0.01")
    projected: dict[str, Any] = {}
    for row_id in ("voltage", "recovery"):
        uniform = arb(str(sizes[f"{row_id}_combined_p_uniform_upper"]))
        component = arb(
            str(sizes[f"{row_id}_combined_p_voltage_component_upper"])
        )
        shadow = arb(
            str(stage2_certificate[f"directed_{row_id}_shadow_norm_upper"])
        )
        ratio = arb(str(defects[f"{row_id}_phase_ratio_transfer_error_upper"]))
        orbit_residual = component * rank_one + uniform * full_period
        direct_density = delay_sum * component * delayed_variation
        orbit_cost = lift * exact_green * orbit_residual
        ratio_cost = lift * exact_boundary * ratio
        residual_cost = lift * (
            exact_green
            * arb(str(combined[f"{row_id}_joint_augmented_residual_upper"]))
            + exact_boundary * arb(str(combined[f"{row_id}_joint_atom_upper"]))
        )
        conditional_total = (
            shadow
            + reserve
            + direct_density
            + orbit_cost
            + ratio_cost
            + residual_cost
        )
        projected[row_id] = {
            "stage2_shadow_upper": _upper_record(shadow),
            "center_TV_transfer_reserve_not_yet_validated": "0.01",
            "orbit_coefficient_row_residual_upper": _upper_record(orbit_residual),
            "direct_delayed_density_cost_upper": _upper_record(direct_density),
            "orbit_cost_at_strict_stage3g_green_upper": _upper_record(orbit_cost),
            "phase_ratio_boundary_cost_at_strict_stage3g_boundary_upper": (
                _upper_record(ratio_cost)
            ),
            "combined_residual_and_atom_cost_upper": _upper_record(residual_cost),
            "conditional_total_if_center_TV_reserve_is_validated": _upper_record(
                conditional_total
            ),
            "conditional_contraction_below_one": bool(
                conditional_total.abs_upper() < 1
            ),
        }
    return projected


def _build_size_certificate(
    guide: _TensorGuide,
    base: Any,
    stage3g: Mapping[str, Any],
    stage3f: Mapping[str, Any],
    stage2: Mapping[str, Any],
) -> dict[str, Any]:
    centers = _patch_centers()
    period = base.period
    h_interval = DirectedInterval.from_float(guide.h, PRECISION_BITS)
    zero = DirectedInterval.from_decimal(0, PRECISION_BITS)
    qv0 = _series_real_box_at_precision(base.phase_voltage, zero)
    qw0 = _series_real_box_at_precision(base.phase_recovery, zero)
    if qv0.lower <= 0:
        raise ArithmeticError("the Stage-3H guide phase denominator vanished")
    binary_phase_speed = guide.guide.voltage_derivative(0.0)
    if binary_phase_speed <= 0:
        raise ArithmeticError("the Stage-3H binary phase denominator vanished")

    alpha_cache: dict[tuple[int, Fraction], tuple[arb, arb, arb]] = {}
    maximum_alpha_radius = arb(0)
    maximum_alpha_absolute = arb(0)
    for delta_cell in range(DELTA_CELL_COUNT):
        for delta_center in centers:
            center_time = period - h_interval * (
                DirectedInterval.from_decimal(2 * delta_cell + 1, PRECISION_BITS)
                / 2
                + DirectedInterval.from_decimal(
                    delta_center.numerator, PRECISION_BITS
                )
                / DirectedInterval.from_decimal(
                    2 * delta_center.denominator, PRECISION_BITS
                )
            )
            relative = -guide.h * (
                delta_cell + 0.5 + 0.5 * float(delta_center)
            )
            binary_center = (
                guide.guide.voltage_derivative(relative) / binary_phase_speed
            )
            enclosure = _phase_ratio_patch(
                base.phase_voltage,
                center_time=center_time,
                period=period,
                h=h_interval,
                denominator=qv0,
                binary_center=binary_center,
            )
            alpha_cache[(delta_cell, delta_center)] = enclosure
            maximum_alpha_radius = max(maximum_alpha_radius, enclosure[1])
            maximum_alpha_absolute = max(maximum_alpha_absolute, enclosure[2])

    beta_ball = _arb_interval(qw0) / _arb_interval(qv0)
    binary_beta_center = (
        guide.guide.recovery_derivative(0.0) / binary_phase_speed
    )
    beta_center = _exact_arb_float(binary_beta_center)
    beta_radius = (beta_ball - beta_center).abs_upper()
    beta_absolute = beta_center.abs_upper() + beta_radius

    terminal_chebyshev: dict[tuple[int, int, int], tuple[arb, ...]] = {}

    def collapsed(q_cell: int, row: int, column: int) -> tuple[arb, ...]:
        key = (q_cell, row, column)
        if key not in terminal_chebyshev:
            terminal_chebyshev[key] = _collapsed_terminal_chebyshev(
                guide.coefficients(0, q_cell), row, column
            )
        return terminal_chebyshev[key]

    terminal_patch_cache: dict[
        tuple[int, Fraction], tuple[arb_mat, arb_mat]
    ] = {}

    def terminal_patch(q_cell: int, z_center: Fraction) -> tuple[arb_mat, arb_mat]:
        key = (q_cell, z_center)
        if key not in terminal_patch_cache:
            terminal_patch_cache[key] = (
                _composed_terminal_component(collapsed(q_cell, 0, 0), z_center),
                _composed_terminal_component(collapsed(q_cell, 0, 1), z_center),
            )
        return terminal_patch_cache[key]

    stage3g_certificate = _mapping(stage3g.get("certificate"), "Stage-3G certificate")
    green = _mapping(
        stage3g_certificate.get("green_bootstrap"), "Stage-3G Green bootstrap"
    )
    candidate_error = arb(str(green["target_bootstrap_error_upper"]))
    voltage_uniform = arb(0)
    voltage_component = arb(0)
    voltage_location: dict[str, Any] | None = None
    ordinary = 0
    terminal = 0
    event_patches = 0
    two_sided_event_patches = 0
    evaluated_one_sided_rows = 0

    for delta_cell in range(DELTA_CELL_COUNT):
        final_lag_cell = 47 - delta_cell
        for lag_cell in range(final_lag_cell + 1):
            if lag_cell >= 46 - delta_cell:
                terminal += 1
            else:
                ordinary += 1
            coefficients = guide.coefficients(delta_cell, lag_cell)
            for delta_center in centers:
                alpha_center, alpha_radius, alpha_absolute = alpha_cache[
                    (delta_cell, delta_center)
                ]
                for lag_center in centers:
                    current = _candidate_patch(
                        coefficients, delta_center, lag_center
                    )[0]
                    center_sum = delta_center + lag_center
                    q_base = delta_cell + lag_cell
                    sides: list[tuple[str, int, Fraction]] = []
                    if center_sum <= 0:
                        sides.append(("lower", q_base, 1 + center_sum))
                    if center_sum >= 0 and q_base + 1 <= 47:
                        sides.append(("upper", q_base + 1, -1 + center_sum))
                    if center_sum == 0:
                        event_patches += 1
                        if len(sides) == 2:
                            two_sided_event_patches += 1
                    for side, q_cell, z_center in sides:
                        evaluated_one_sided_rows += 1
                        local_uniform, local_component = _signed_tensor_bounds(
                            current,
                            terminal_patch(q_cell, z_center),
                            alpha_center,
                            alpha_radius,
                        )
                        exact_error = (1 + alpha_absolute) * candidate_error
                        local_uniform += exact_error
                        local_component += exact_error
                        if local_uniform.abs_upper() > voltage_uniform.abs_upper():
                            voltage_uniform = local_uniform
                            voltage_location = {
                                "delta_cell": delta_cell,
                                "lag_cell": lag_cell,
                                "delta_patch_center": str(delta_center),
                                "lag_patch_center": str(lag_center),
                                "terminal_side": side,
                                "q_cell": q_cell,
                                "event_seam_patch": bool(center_sum == 0),
                                "terminal_clipped_cell": bool(
                                    lag_cell >= 46 - delta_cell
                                ),
                            }
                        voltage_component = max(voltage_component, local_component)

    if (
        ordinary != ORDINARY_RECTANGLE_COUNT
        or terminal != TERMINAL_CLIPPED_RECTANGLE_COUNT
    ):
        raise AssertionError("the Stage-3H resolvent cover changed")
    if (
        event_patches != EVENT_SEAM_PATCH_COUNT
        or two_sided_event_patches != TWO_SIDED_EVENT_SEAM_PATCH_COUNT
        or evaluated_one_sided_rows
        != ONE_SIDED_VOLTAGE_ROW_EVALUATION_COUNT
    ):
        raise AssertionError("the Stage-3H event-seam count changed")

    recovery_uniform = arb(0)
    recovery_component = arb(0)
    recovery_location: dict[str, Any] | None = None
    one_dimensional_patch_count = 0
    for lag_cell in range(48):
        for lag_center in centers:
            voltage = (
                _one_dimensional_terminal_component(
                    collapsed(lag_cell, 0, 0), lag_center
                ),
                _one_dimensional_terminal_component(
                    collapsed(lag_cell, 0, 1), lag_center
                ),
            )
            recovery = (
                _one_dimensional_terminal_component(
                    collapsed(lag_cell, 1, 0), lag_center
                ),
                _one_dimensional_terminal_component(
                    collapsed(lag_cell, 1, 1), lag_center
                ),
            )
            local_uniform, local_component = _signed_vector_bounds(
                recovery, voltage, beta_center, beta_radius
            )
            exact_error = (1 + beta_absolute) * candidate_error
            local_uniform += exact_error
            local_component += exact_error
            one_dimensional_patch_count += 1
            if local_uniform.abs_upper() > recovery_uniform.abs_upper():
                recovery_uniform = local_uniform
                recovery_location = {
                    "lag_cell": lag_cell,
                    "lag_patch_center": str(lag_center),
                }
            recovery_component = max(recovery_component, local_component)

    if one_dimensional_patch_count != RECOVERY_ONE_DIMENSIONAL_PATCH_COUNT:
        raise AssertionError("the Stage-3H recovery patch cover changed")

    size_records = {
        "stage3g_resolvent_candidate_row_error_upper": _upper_record(
            candidate_error
        ),
        "stage3g_resolvent_candidate_row_error_semantics": (
            STAGE3G_CANDIDATE_ERROR_SEMANTICS
        ),
        "voltage_combined_p_uniform_upper": _upper_record(voltage_uniform),
        "voltage_combined_p_voltage_component_upper": _upper_record(
            voltage_component
        ),
        "voltage_uniform_maximizer": voltage_location,
        "recovery_combined_p_uniform_upper": _upper_record(recovery_uniform),
        "recovery_combined_p_voltage_component_upper": _upper_record(
            recovery_component
        ),
        "recovery_uniform_maximizer": recovery_location,
        "signed_center_subtraction_precedes_row_norm": True,
        "ratio_radius_paid_after_signed_center_subtraction": True,
    }
    stage3f_certificate = _mapping(stage3f.get("certificate"), "Stage-3F certificate")
    stage2_certificate = _mapping(stage2.get("certificate"), "Stage-2 certificate")
    projected = _frontier_rows_from_size_records(
        size_records,
        stage3g_certificate,
        stage3f_certificate,
        stage2_certificate,
    )

    return {
        "geometry": {
            "ordinary_rectangle_count": ordinary,
            "terminal_clipped_rectangle_count": terminal,
            "local_patch_count": (ordinary + terminal) * SUBDIVISION_PARTS**2,
            "event_seam_patch_count": event_patches,
            "two_sided_event_seam_patch_count": two_sided_event_patches,
            "terminal_line_one_sided_event_patch_count": (
                event_patches - two_sided_event_patches
            ),
            "one_sided_voltage_row_evaluation_count": evaluated_one_sided_rows,
            "recovery_one_dimensional_patch_count": one_dimensional_patch_count,
            "event_triangle_enclosure": EVENT_TRIANGLE_ENCLOSURE,
        },
        "phase": {
            "voltage_local_ratio_radius_maximum_upper": _upper_record(
                maximum_alpha_radius
            ),
            "voltage_ratio_absolute_maximum_upper": _upper_record(
                maximum_alpha_absolute
            ),
            "recovery_ratio_center_binary64_hex": binary_beta_center.hex(),
            "recovery_ratio_radius_upper": _upper_record(beta_radius),
            "recovery_ratio_absolute_upper": _upper_record(beta_absolute),
            "fourier_cutoff": FOURIER_CUTOFF,
            "taylor_degree": COEFFICIENT_DEGREE,
        },
        "sizes": size_records,
        "frontier": {
            "rows": projected,
            "strict_sizes_validated": True,
            "continuous_center_TV_reserve_validated": False,
            "conditional_only_until_center_TV_cell_integral_is_validated": True,
        },
    }


@lru_cache(maxsize=1)
def build_outer_combined_row_stage3h_size(
    repository: Path,
) -> OuterCombinedRowStage3HSize:
    repository = repository.resolve()
    if os.environ.get("OPENBLAS_NUM_THREADS") != PINNED_OPENBLAS_NUM_THREADS:
        raise RuntimeError("Stage-3H requires OPENBLAS_NUM_THREADS=1")
    arb_ctx.prec = PRECISION_BITS
    arb_ctx.threads = 1
    _require_unique_disjoint_flags(TRUE_FLAGS, FALSE_FLAGS)
    stage3g = _load_parent(
        repository, STAGE3G_RESULT_RELATIVE_PATH, STAGE3G_RESULT_SHA256
    )
    stage3f = _load_parent(
        repository, STAGE3F_RESULT_RELATIVE_PATH, STAGE3F_RESULT_SHA256
    )
    stage2 = _load_parent(repository, STAGE2_RESULT_RELATIVE_PATH, STAGE2_RESULT_SHA256)
    outer = _load_parent(repository, OUTER_RESULT_RELATIVE_PATH, OUTER_RESULT_SHA256)
    stage3g_certificate = _validate_parent_artifact_lock(
        stage3g,
        repository,
        label="Stage-3G",
        schema_id=STAGE3G_SCHEMA_ID,
        result_relative_path=STAGE3G_RESULT_RELATIVE_PATH,
    )
    _validate_parent_artifact_lock(
        stage3f,
        repository,
        label="Stage-3F",
        schema_id=STAGE3F_SCHEMA_ID,
        result_relative_path=STAGE3F_RESULT_RELATIVE_PATH,
    )
    _validate_parent_artifact_lock(
        stage2,
        repository,
        label="Stage-2",
        schema_id=STAGE2_SCHEMA_ID,
        result_relative_path=STAGE2_RESULT_RELATIVE_PATH,
    )
    stage3g_gate = _mapping(
        stage3g_certificate.get("transfer_gate"),
        "Stage-3G transfer gate",
    )
    if not (
        stage3g_gate.get("full_advanced_green_target_validated") is True
        and stage3g_gate.get("joint_augmented_phase_residual_targets_validated")
        is True
    ):
        raise ValueError("the Stage-3G residual/Green theorem was weakened")
    orbit = validate_outer_high_resolution_artifact(
        outer, repository, replay_directed=False
    )
    base = _build_leaky_base_sequences(orbit, PRECISION_BITS)
    guide = _TensorGuide(orbit)
    data = _build_size_certificate(guide, base, stage3g, stage3f, stage2)
    sizes = data["sizes"]
    if not (
        math.isfinite(float(sizes["voltage_combined_p_uniform_upper"]))
        and math.isfinite(float(sizes["recovery_combined_p_uniform_upper"]))
    ):
        raise ArithmeticError("a strict Stage-3H row size is not finite")
    claims = {name: True for name in TRUE_FLAGS}
    claims.update({name: False for name in FALSE_FLAGS})
    return OuterCombinedRowStage3HSize(
        schema_id=SCHEMA_ID,
        model_id=MODEL_ID,
        branch=BRANCH,
        arithmetic_scope=ARITHMETIC_SCOPE,
        precision_bits=PRECISION_BITS,
        row_scope=ROW_SCOPE,
        parent_result_sha256={
            STAGE3G_RESULT_RELATIVE_PATH: STAGE3G_RESULT_SHA256,
            STAGE3F_RESULT_RELATIVE_PATH: STAGE3F_RESULT_SHA256,
            STAGE2_RESULT_RELATIVE_PATH: STAGE2_RESULT_SHA256,
            OUTER_RESULT_RELATIVE_PATH: OUTER_RESULT_SHA256,
        },
        chart_geometry=data["geometry"],
        phase_ratio_enclosures=data["phase"],
        combined_row_size=sizes,
        linear_transfer_frontier=data["frontier"],
        transfer_errors={
            "E_voltage": None,
            "E_recovery": None,
            "E_phase": _mapping(
                _mapping(stage3g.get("certificate"), "Stage-3G certificate").get(
                    "transfer_errors"
                ),
                "Stage-3G transfer errors",
            )["E_phase"],
        },
        transfer_gate={
            "strict_combined_row_uniform_sizes_validated": True,
            "continuous_center_signed_density_TV_reserve_validated": False,
            "linear_return_gate_evaluated": False,
            "arbitrary_c0_linear_contraction_closes": False,
            "nonlinear_outer_attraction_closes": False,
        },
        claim_status=claims,
        conclusion=CONCLUSION,
    )


def build_outer_combined_row_stage3h_size_result(repository: Path) -> dict[str, Any]:
    repository = repository.resolve()
    certificate = json.loads(
        json.dumps(
            asdict(build_outer_combined_row_stage3h_size(repository)),
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        )
    )
    return {
        "certificate": certificate,
        "manifest": {
            "schema_id": SCHEMA_ID,
            "result": RESULT_RELATIVE_PATH,
            "default_command": DEFAULT_COMMAND,
            "certificate_sha256": canonical_sha256(certificate),
            "source_sha256": {
                relative: _sha256_path(repository / relative)
                for relative in SOURCE_MANIFEST
            },
            "environment": _expected_environment(),
        },
    }


def validate_outer_combined_row_stage3h_size_result(
    payload: Mapping[str, Any], repository: Path
) -> None:
    repository = repository.resolve()
    _require_unique_disjoint_flags(TRUE_FLAGS, FALSE_FLAGS)
    if not isinstance(payload, Mapping) or set(payload) != {"certificate", "manifest"}:
        raise ValueError("the Stage-3H top-level schema changed")
    certificate = _mapping(payload.get("certificate"), "Stage-3H certificate")
    manifest = _mapping(payload.get("manifest"), "Stage-3H manifest")
    _require_exact_keys(
        certificate,
        {field.name for field in fields(OuterCombinedRowStage3HSize)},
        "Stage-3H certificate",
    )
    _require_exact_keys(manifest, RESULT_MANIFEST_FIELDS, "Stage-3H manifest")
    if (
        manifest.get("schema_id") != SCHEMA_ID
        or manifest.get("result") != RESULT_RELATIVE_PATH
        or manifest.get("default_command") != DEFAULT_COMMAND
    ):
        raise ValueError("the Stage-3H manifest identity changed")
    environment = _mapping(manifest.get("environment"), "Stage-3H environment")
    _require_exact_keys(environment, ENVIRONMENT_FIELDS, "Stage-3H environment")
    if dict(environment) != _expected_environment():
        raise ValueError("the Stage-3H environment changed")
    if canonical_sha256(certificate) != manifest.get("certificate_sha256"):
        raise ValueError("the Stage-3H certificate digest changed")
    sources = _mapping(manifest.get("source_sha256"), "Stage-3H source manifest")
    if set(sources) != set(SOURCE_MANIFEST):
        raise ValueError("the Stage-3H source set changed")
    for relative in SOURCE_MANIFEST:
        if sources.get(relative) != _sha256_path(repository / relative):
            raise ValueError(f"a Stage-3H source changed: {relative}")

    if (
        certificate.get("schema_id") != SCHEMA_ID
        or certificate.get("model_id") != MODEL_ID
        or certificate.get("branch") != BRANCH
        or certificate.get("arithmetic_scope") != ARITHMETIC_SCOPE
        or certificate.get("precision_bits") != PRECISION_BITS
        or certificate.get("row_scope") != ROW_SCOPE
    ):
        raise ValueError("the Stage-3H certificate identity changed")
    expected_parents = {
        STAGE3G_RESULT_RELATIVE_PATH: STAGE3G_RESULT_SHA256,
        STAGE3F_RESULT_RELATIVE_PATH: STAGE3F_RESULT_SHA256,
        STAGE2_RESULT_RELATIVE_PATH: STAGE2_RESULT_SHA256,
        OUTER_RESULT_RELATIVE_PATH: OUTER_RESULT_SHA256,
    }
    parents = _mapping(
        certificate.get("parent_result_sha256"), "Stage-3H parents"
    )
    if dict(parents) != expected_parents:
        raise ValueError("the Stage-3H parent digest map changed")
    stage3g = _load_parent(
        repository, STAGE3G_RESULT_RELATIVE_PATH, STAGE3G_RESULT_SHA256
    )
    stage3g_certificate = _validate_parent_artifact_lock(
        stage3g,
        repository,
        label="Stage-3G",
        schema_id=STAGE3G_SCHEMA_ID,
        result_relative_path=STAGE3G_RESULT_RELATIVE_PATH,
    )
    stage3f = _load_parent(
        repository, STAGE3F_RESULT_RELATIVE_PATH, STAGE3F_RESULT_SHA256
    )
    stage3f_certificate = _validate_parent_artifact_lock(
        stage3f,
        repository,
        label="Stage-3F",
        schema_id=STAGE3F_SCHEMA_ID,
        result_relative_path=STAGE3F_RESULT_RELATIVE_PATH,
    )
    stage2 = _load_parent(
        repository, STAGE2_RESULT_RELATIVE_PATH, STAGE2_RESULT_SHA256
    )
    stage2_certificate = _validate_parent_artifact_lock(
        stage2,
        repository,
        label="Stage-2",
        schema_id=STAGE2_SCHEMA_ID,
        result_relative_path=STAGE2_RESULT_RELATIVE_PATH,
    )
    outer = _load_parent(
        repository, OUTER_RESULT_RELATIVE_PATH, OUTER_RESULT_SHA256
    )
    validate_outer_high_resolution_artifact(
        outer, repository, replay_directed=False
    )

    claims = _mapping(certificate.get("claim_status"), "Stage-3H claims")
    if set(claims) != set(TRUE_FLAGS + FALSE_FLAGS):
        raise ValueError("the Stage-3H claim ledger changed")
    if any(claims.get(name) is not True for name in TRUE_FLAGS):
        raise ValueError("a proved Stage-3H fact was weakened")
    if any(claims.get(name) is not False for name in FALSE_FLAGS):
        raise ValueError("an open Stage-3H claim was promoted")

    geometry = _mapping(certificate.get("chart_geometry"), "Stage-3H geometry")
    phase = _mapping(
        certificate.get("phase_ratio_enclosures"), "Stage-3H phase ledger"
    )
    sizes = _mapping(
        certificate.get("combined_row_size"), "Stage-3H row sizes"
    )
    frontier = _mapping(
        certificate.get("linear_transfer_frontier"), "Stage-3H frontier"
    )
    transfer = _mapping(certificate.get("transfer_errors"), "Stage-3H transfer")
    gate = _mapping(certificate.get("transfer_gate"), "Stage-3H gate")
    _require_exact_keys(geometry, GEOMETRY_FIELDS, "Stage-3H geometry")
    _require_exact_keys(phase, PHASE_FIELDS, "Stage-3H phase ledger")
    _require_exact_keys(sizes, SIZE_FIELDS, "Stage-3H row sizes")
    _require_exact_keys(frontier, FRONTIER_FIELDS, "Stage-3H frontier")
    _require_exact_keys(transfer, TRANSFER_ERROR_FIELDS, "Stage-3H transfer")
    _require_exact_keys(gate, TRANSFER_GATE_FIELDS, "Stage-3H gate")

    expected_geometry = {
        "ordinary_rectangle_count": ORDINARY_RECTANGLE_COUNT,
        "terminal_clipped_rectangle_count": TERMINAL_CLIPPED_RECTANGLE_COUNT,
        "local_patch_count": LOCAL_PATCH_COUNT,
        "event_seam_patch_count": EVENT_SEAM_PATCH_COUNT,
        "two_sided_event_seam_patch_count": TWO_SIDED_EVENT_SEAM_PATCH_COUNT,
        "terminal_line_one_sided_event_patch_count": (
            TERMINAL_LINE_ONE_SIDED_EVENT_PATCH_COUNT
        ),
        "one_sided_voltage_row_evaluation_count": (
            ONE_SIDED_VOLTAGE_ROW_EVALUATION_COUNT
        ),
        "recovery_one_dimensional_patch_count": (
            RECOVERY_ONE_DIMENSIONAL_PATCH_COUNT
        ),
        "event_triangle_enclosure": EVENT_TRIANGLE_ENCLOSURE,
    }
    if dict(geometry) != expected_geometry:
        raise ValueError("the Stage-3H complete row chart geometry changed")

    if (
        phase.get("fourier_cutoff") != FOURIER_CUTOFF
        or phase.get("taylor_degree") != COEFFICIENT_DEGREE
    ):
        raise ValueError("the Stage-3H phase approximation ledger changed")
    for name in PHASE_FIELDS - {
        "fourier_cutoff",
        "taylor_degree",
        "recovery_ratio_center_binary64_hex",
    }:
        if _decimal(phase.get(name), name) < 0:
            raise ValueError("a Stage-3H phase bound became negative")
    recovery_center_hex = phase.get("recovery_ratio_center_binary64_hex")
    if not isinstance(recovery_center_hex, str):
        raise ValueError("the recovery phase-ratio center hex is missing")
    try:
        recovery_center = float.fromhex(recovery_center_hex)
    except ValueError as error:
        raise ValueError("the recovery phase-ratio center hex is invalid") from error
    if (
        not math.isfinite(recovery_center)
        or recovery_center.hex() != recovery_center_hex
    ):
        raise ValueError("the recovery phase-ratio center hex is not canonical")
    if (
        _decimal(
            phase.get("voltage_ratio_absolute_maximum_upper"),
            "voltage phase-ratio absolute upper",
        )
        < _decimal(
            phase.get("voltage_local_ratio_radius_maximum_upper"),
            "voltage phase-ratio radius",
        )
        or _decimal(
            phase.get("recovery_ratio_absolute_upper"),
            "recovery phase-ratio absolute upper",
        )
        < _decimal(
            phase.get("recovery_ratio_radius_upper"),
            "recovery phase-ratio radius",
        )
        or _decimal(
            phase.get("recovery_ratio_absolute_upper"),
            "recovery phase-ratio absolute upper",
        )
        < Decimal.from_float(abs(recovery_center))
    ):
        raise ValueError("a Stage-3H phase absolute bound is too small")

    stage3g_green = _mapping(
        stage3g_certificate.get("green_bootstrap"), "Stage-3G Green ledger"
    )
    stage3g_gate = _mapping(
        stage3g_certificate.get("transfer_gate"), "Stage-3G transfer gate"
    )
    if not (
        stage3g_gate.get("complete_directed_tensor_geometry_validated") is True
        and stage3g_gate.get("full_advanced_green_target_validated") is True
        and stage3g_gate.get("full_advanced_boundary_target_validated") is True
        and stage3g_gate.get("joint_augmented_phase_residual_targets_validated")
        is True
        and stage3g_gate.get("strict_combined_row_uniform_sizes_validated")
        is False
    ):
        raise ValueError("the Stage-3G theorem boundary changed")
    arb_ctx.prec = PRECISION_BITS
    expected_candidate_error = _upper_record(
        arb(str(stage3g_green["target_bootstrap_error_upper"]))
    )
    if (
        sizes.get("stage3g_resolvent_candidate_row_error_upper")
        != expected_candidate_error
        or sizes.get("stage3g_resolvent_candidate_row_error_semantics")
        != STAGE3G_CANDIDATE_ERROR_SEMANTICS
    ):
        raise ValueError("the Stage-3G resolvent error ingress changed")
    if (
        sizes.get("signed_center_subtraction_precedes_row_norm") is not True
        or sizes.get("ratio_radius_paid_after_signed_center_subtraction") is not True
    ):
        raise ValueError("the Stage-3H signed-row operation order changed")
    for row_id in ("voltage", "recovery"):
        uniform = _decimal(
            sizes.get(f"{row_id}_combined_p_uniform_upper"),
            f"{row_id} combined uniform size",
        )
        component = _decimal(
            sizes.get(f"{row_id}_combined_p_voltage_component_upper"),
            f"{row_id} voltage-component size",
        )
        if not (0 < component <= uniform):
            raise ValueError(f"the Stage-3H {row_id} row sizes are inconsistent")

    patch_centers = {str(value): value for value in _patch_centers()}
    voltage_location = _mapping(
        sizes.get("voltage_uniform_maximizer"),
        "Stage-3H voltage maximizer",
    )
    _require_exact_keys(
        voltage_location,
        VOLTAGE_MAXIMIZER_FIELDS,
        "Stage-3H voltage maximizer",
    )
    delta_cell = voltage_location.get("delta_cell")
    lag_cell = voltage_location.get("lag_cell")
    delta_center_text = voltage_location.get("delta_patch_center")
    lag_center_text = voltage_location.get("lag_patch_center")
    if (
        not isinstance(delta_cell, int)
        or not 0 <= delta_cell < DELTA_CELL_COUNT
        or not isinstance(lag_cell, int)
        or not 0 <= lag_cell <= 47 - delta_cell
        or delta_center_text not in patch_centers
        or lag_center_text not in patch_centers
    ):
        raise ValueError("the Stage-3H voltage maximizer left the row cover")
    center_sum = (
        patch_centers[str(delta_center_text)]
        + patch_centers[str(lag_center_text)]
    )
    side = voltage_location.get("terminal_side")
    q_base = delta_cell + lag_cell
    expected_q_cell: int | None = None
    if side == "lower" and center_sum <= 0:
        expected_q_cell = q_base
    elif side == "upper" and center_sum >= 0 and q_base + 1 <= 47:
        expected_q_cell = q_base + 1
    if expected_q_cell is None or voltage_location.get("q_cell") != expected_q_cell:
        raise ValueError("the Stage-3H voltage maximizer chart side is invalid")
    if (
        voltage_location.get("event_seam_patch") is not (center_sum == 0)
        or voltage_location.get("terminal_clipped_cell")
        is not (lag_cell >= 46 - delta_cell)
    ):
        raise ValueError("the Stage-3H voltage maximizer flags are inconsistent")

    recovery_location = _mapping(
        sizes.get("recovery_uniform_maximizer"),
        "Stage-3H recovery maximizer",
    )
    _require_exact_keys(
        recovery_location,
        RECOVERY_MAXIMIZER_FIELDS,
        "Stage-3H recovery maximizer",
    )
    recovery_lag = recovery_location.get("lag_cell")
    if (
        not isinstance(recovery_lag, int)
        or not 0 <= recovery_lag < 48
        or recovery_location.get("lag_patch_center") not in patch_centers
    ):
        raise ValueError("the Stage-3H recovery maximizer left the row cover")

    if (
        frontier.get("strict_sizes_validated") is not True
        or frontier.get("continuous_center_TV_reserve_validated") is not False
        or frontier.get(
            "conditional_only_until_center_TV_cell_integral_is_validated"
        )
        is not True
    ):
        raise ValueError("the Stage-3H conditional frontier changed")
    rows = _mapping(frontier.get("rows"), "Stage-3H frontier rows")
    _require_exact_keys(rows, {"voltage", "recovery"}, "Stage-3H frontier rows")
    for row_id in ("voltage", "recovery"):
        row = _mapping(rows.get(row_id), f"Stage-3H {row_id} frontier")
        _require_exact_keys(
            row, FRONTIER_ROW_FIELDS, f"Stage-3H {row_id} frontier"
        )
        if row.get("center_TV_transfer_reserve_not_yet_validated") != "0.01":
            raise ValueError("the Stage-3H unproved center reserve changed")
        numeric_names = FRONTIER_ROW_FIELDS - {
            "conditional_contraction_below_one",
        }
        values = {
            name: _decimal(row.get(name), f"{row_id} {name}")
            for name in numeric_names
        }
        if any(value < 0 for value in values.values()):
            raise ValueError("a Stage-3H frontier contribution became negative")
        if row.get("conditional_contraction_below_one") is not True:
            raise ValueError("the Stage-3H conditional contraction ledger failed")
    expected_frontier_rows = _frontier_rows_from_size_records(
        sizes,
        stage3g_certificate,
        stage3f_certificate,
        stage2_certificate,
    )
    if dict(rows) != expected_frontier_rows:
        raise ValueError("the Stage-3H frontier formula ledger changed")

    stage3g_transfer = _mapping(
        stage3g_certificate.get("transfer_errors"), "Stage-3G transfer errors"
    )
    if (
        transfer.get("E_voltage") is not None
        or transfer.get("E_recovery") is not None
        or transfer.get("E_phase") != stage3g_transfer.get("E_phase")
    ):
        raise ValueError("a Stage-3H transfer error was invented")
    expected_gate = {
        "strict_combined_row_uniform_sizes_validated": True,
        "continuous_center_signed_density_TV_reserve_validated": False,
        "linear_return_gate_evaluated": False,
        "arbitrary_c0_linear_contraction_closes": False,
        "nonlinear_outer_attraction_closes": False,
    }
    if dict(gate) != expected_gate:
        raise ValueError("the Stage-3H transfer gate ledger changed")
    if certificate.get("conclusion") != CONCLUSION:
        raise ValueError("the Stage-3H conclusion changed")

    expected = json.loads(
        json.dumps(
            asdict(build_outer_combined_row_stage3h_size(repository)),
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        )
    )
    if certificate != expected:
        raise ValueError("the Stage-3H certificate differs from replay")


__all__ = [
    "CONCLUSION",
    "DEFAULT_COMMAND",
    "FALSE_FLAGS",
    "NOTE_RELATIVE_PATH",
    "RESULT_RELATIVE_PATH",
    "ROW_SCOPE",
    "SOURCE_MANIFEST",
    "STAGE3G_CANDIDATE_ERROR_SEMANTICS",
    "TRUE_FLAGS",
    "build_outer_combined_row_stage3h_size",
    "build_outer_combined_row_stage3h_size_result",
    "canonical_sha256",
    "validate_outer_combined_row_stage3h_size_result",
]
