"""Stage-3G tensor-Bernstein certificate for the outer DDE resolvent.

This stage validates the moving-frame family

    S(delta, ell) = R(T-delta, T-delta-ell),

where ``0 <= delta <= tau_1`` and ``0 <= ell <= T-delta``.  On every
method-of-steps rectangle it satisfies

    S_ell = S A(T-delta-ell)
            + sum_j S(delta, ell-tau_j) B_j(T-delta-ell+tau_j).

The two delays are exactly 16 and 20 mesh widths.  Consequently every
retarded term uses the same local tensor coordinates in an earlier chart.
The 730 ordinary rectangles and the 40 terminal clipped cells are all
covered.  The terminal line crosses two lag cells in every delta column
because ``T/h`` lies strictly between 47 and 48.  On a terminal cell the
binary guide is continued by the same retarded row equation.  The continuation is
only a candidate construction; the directed residual proves its validity on
the full rectangle and therefore also on the physical clipped subset.

Candidate Chebyshev coefficients are exact dyadic data.  Exact rational
Chebyshev-to-Bernstein maps and all residual arithmetic are evaluated as
192-bit Arb balls.  Fourier coefficient Taylor models use outward MPFR
arithmetic.  Products are formed in tensor Bernstein form before row norms
are taken.  This stage is deliberately a resolvent/Green certificate.  A
tight strict uniform bound for the two *phase-combined* rows is still needed
before the Stage-3F binary row sizes can be replaced and E_v,E_w promoted.
"""

from __future__ import annotations

import ast
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

from flint import arb, arb_mat, arb_poly, ctx as arb_ctx
import gmpy2
import numpy as np
import scipy
from scipy.integrate import solve_ivp

from canard_control.directed_interval import (
    DirectedComplexInterval,
    DirectedInterval,
    complex_unit_interval,
    decimal_lower,
    decimal_upper,
    pi_interval,
)
from canard_control.leaky_outer_delay_word_stage3d_primitives import (
    RESULT_RELATIVE_PATH as STAGE3D_RESULT_RELATIVE_PATH,
    _PrimitiveGuide,
)
from canard_control.leaky_outer_high_resolution import (
    RESULT_RELATIVE_PATH as OUTER_RESULT_RELATIVE_PATH,
    validate_outer_high_resolution_artifact,
)
from canard_control.leaky_outer_signed_row_stage3f_adjoint import (
    RESULT_RELATIVE_PATH as STAGE3F_RESULT_RELATIVE_PATH,
)
from canard_control.leaky_periodic_validation import _build_leaky_base_sequences
from canard_control.leaky_pulse_separator_candidate import TAU_0, TAU_1


SCHEMA_ID = "leaky-outer-resolvent-stage3g-tensor-v2"
MODEL_ID = "autonomous-leaky-recovery-two-delay-fhn-bistable-proposal"
BRANCH = "outer_pulse"
SOURCE_RELATIVE_PATH = (
    "src/canard_control/leaky_outer_resolvent_stage3g_tensor.py"
)
GENERATOR_RELATIVE_PATH = "experiments/leaky_outer_resolvent_stage3g_tensor.py"
RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_outer_resolvent_stage3g_tensor.json"
)
NOTE_RELATIVE_PATH = "docs/leaky-outer-resolvent-stage3g-tensor.md"
TEST_RELATIVE_PATH = "tests/test_leaky_outer_resolvent_stage3g_tensor.py"
SOURCE_MANIFEST = (
    SOURCE_RELATIVE_PATH,
    GENERATOR_RELATIVE_PATH,
    NOTE_RELATIVE_PATH,
    TEST_RELATIVE_PATH,
    "src/canard_control/directed_interval.py",
    "src/canard_control/leaky_outer_delay_word_stage3d_primitives.py",
    "src/canard_control/leaky_outer_high_resolution.py",
    "src/canard_control/leaky_outer_signed_row_stage3f_adjoint.py",
    "src/canard_control/leaky_periodic_validation.py",
    "src/canard_control/leaky_pulse_separator_candidate.py",
)
DEFAULT_COMMAND = (
    "OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONPATH=build/testdeps:src "
    "/usr/bin/python3 experiments/leaky_outer_resolvent_stage3g_tensor.py"
)
ARITHMETIC_SCOPE = (
    "source-bound binary64 Chebyshev candidates treated as exact dyadics; "
    "192-bit Arb ball tensor-Bernstein transforms, products, degree "
    "elevation and residual norms; 192-bit outward MPFR Fourier-Taylor "
    "coefficients, omitted tails and Taylor remainders"
)
CONCLUSION = (
    "the complete moving-frame resolvent rectangle cover, including "
    "the terminal clipped cells, now has a 192-bit tensor-Bernstein "
    "residual and a closed Green/boundary bootstrap.  The joint S/U "
    "augmented bounds strictly pass both Stage-3F voltage and "
    "recovery residual thresholds.  Tight strict uniform sizes for "
    "the two directly phase-combined rows are still absent, so the "
    "Stage-3F binary row sizes cannot yet be used as proof inputs; "
    "E_voltage,E_recovery and C0 contraction remain open"
)

STAGE3F_RESULT_SHA256 = (
    "d09832c47370dee6588cc0ee7396ca6fe75c1f283785a799682f302427344eee"
)
STAGE3D_RESULT_SHA256 = (
    "11197f7f64289bd239f6167deedae66e54bc7805eaf84d08762ddc843c7372bf"
)
OUTER_RESULT_SHA256 = (
    "d888916fed919f1515dd31ab851b2229816ea373365fa0221b1e345580f165a7"
)
STAGE3F_SCHEMA_ID = "leaky-outer-signed-row-stage3f-adjoint-v1"
STAGE3D_SCHEMA_ID = "leaky-outer-delay-word-stage3d-primitives-v1"
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
STAGE3D_REQUIRED_RUNTIME_SOURCES = frozenset(
    {
        "src/canard_control/directed_interval.py",
        "src/canard_control/leaky_outer_continuous_kernel_stage3_shard.py",
        "src/canard_control/leaky_outer_delay_word_stage3c_compression.py",
        "src/canard_control/leaky_outer_delay_word_stage3d_primitives.py",
        "src/canard_control/leaky_outer_high_resolution.py",
        "src/canard_control/leaky_outer_phase_fixed_return_stage1.py",
        "src/canard_control/leaky_pulse_separator_candidate.py",
    }
)
PRECISION_BITS = 192
PINNED_OPENBLAS_NUM_THREADS = "1"
DELTA_CELL_COUNT = 20
LAG_CELL_COUNT = 48
ORDINARY_RECTANGLE_COUNT = 730
TERMINAL_EXTENDED_RECTANGLE_COUNT = 40
EXPECTED_COEFFICIENT_PATCH_COUNT = 1008
DELTA_DEGREE = 10
LAG_DEGREE = 24
COEFFICIENT_DEGREE = 24
FOURIER_CUTOFF = 128
SUBDIVISION_PARTS = 4
GUIDE_MAXIMUM_STEP = 0.04
EXTENSION_MAXIMUM_STEP = 0.002
EXTENSION_SOLVE_HORIZON = 0.85
FULL_GREEN_TARGET = "60000"
FULL_BOUNDARY_TARGET = "70000"
VOLTAGE_RESIDUAL_TARGET = (
    "1.57603746447248128534003349791174352731178582621493206808834e-06"
)
RECOVERY_RESIDUAL_TARGET = (
    "1.31021008211389802721761680503047374765756596535807913848753e-05"
)

TRUE_FLAGS = (
    "stage3f_parent_digest_validated",
    "stage3d_parent_digest_validated",
    "stage3d_parent_source_manifest_validated",
    "outer_orbit_parent_digest_validated",
    "stage3f_voltage_recovery_residual_targets_exactly_ingressed",
    "strict_exact_arb_target_comparisons_used",
    "method_of_steps_delay_alignment_exact_binary64",
    "binary64_guide_period_inside_directed_period_interval",
    "directed_period_satisfies_47h_lt_T_lt_48h",
    "directed_terminal_extension_satisfies_0_lt_49h_minus_T_lt_0p85",
    "terminal_extension_within_candidate_solve_horizon",
    "degree10_by24_resolvent_tensor_constructed",
    "all_730_ordinary_rectangles_covered",
    "all_40_terminal_clipped_cells_covered_by_equation_extension",
    "terminal_extension_revalidated_by_same_tensor_residual",
    "candidate_coefficients_treated_as_exact_dyadics",
    "tensor_bernstein_arithmetic_outward_192_bit",
    "fourier_taylor_coefficients_outward_192_bit",
    "fourier_tail_and_taylor_remainders_included",
    "signed_matrix_residual_formed_before_row_norm",
    "chart_boundary_and_lag_interface_defects_directed",
    "full_advanced_green_target_validated",
    "full_advanced_boundary_target_validated",
    "joint_augmented_voltage_residual_target_validated",
    "joint_augmented_recovery_residual_target_validated",
)
FALSE_FLAGS = (
    "direct_phase_combined_voltage_row_uniform_bound_validated",
    "direct_phase_combined_recovery_row_uniform_bound_validated",
    "stage3f_binary_combined_row_sizes_replaced",
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
        "period_mesh_ratio_interval",
        "period_minus_47h_lower",
        "48h_minus_period_lower",
        "period_strictly_between_47h_and_48h",
        "guide_period_binary64_hex",
        "guide_period_inside_directed_period_interval",
        "terminal_extension_length_interval",
        "terminal_extension_decimal_limit",
        "terminal_extension_solver_horizon_binary64_hex",
        "terminal_extension_solver_horizon_lower",
        "terminal_extension_solver_margin_lower",
        "terminal_extension_strictly_between_zero_and_0p85",
        "terminal_extension_within_solver_horizon",
        "ordinary_rectangle_count",
        "terminal_extended_rectangle_count",
        "tensor_patch_count",
        "mesh_width_binary64_hex",
        "tau0_mesh_widths",
        "tau1_mesh_widths",
        "delta_cell_count",
        "lag_cell_count",
        "terminal_extension_satisfies_same_retarded_equation",
        "physical_terminal_clipped_domain_subset_of_validated_rectangle",
        "delta_degree",
        "lag_degree",
        "coefficient_degree",
        "subdivision_parts_per_axis",
        "fourier_cutoff",
    }
)
COEFFICIENT_FIELDS = frozenset(
    {
        "cached_coefficient_patch_count",
        "current_tail_plus_taylor_effect_included",
        "delayed_tail_plus_taylor_effect_included",
    }
)
RESIDUAL_FIELDS = frozenset(
    {
        "voltage_terminal_row_polynomial_upper",
        "recovery_terminal_row_polynomial_upper",
        "voltage_terminal_row_tail_upper",
        "recovery_terminal_row_tail_upper",
        "voltage_terminal_row_total_upper",
        "recovery_terminal_row_total_upper",
        "voltage_terminal_row_maximizer",
        "recovery_terminal_row_maximizer",
        "full_matrix_row_residual_upper",
        "normalization",
        "signed_matrix_residual_before_row_norm",
        "arb_precision_bits",
    }
)
MAXIMIZER_FIELDS = frozenset(
    {
        "delta_cell",
        "lag_cell",
        "delta_patch_center",
        "lag_patch_center",
        "terminal_extended_cell",
    }
)
DEFECT_FIELDS = frozenset(
    {
        "initial_boundary_matrix_row_defect_upper",
        "maximum_one_lag_interface_matrix_row_jump_upper",
        "summed_lag_interface_matrix_row_jump_upper",
        "boundary_plus_interface_atom_upper",
        "delta_interfaces_not_evolution_atoms",
    }
)
GREEN_FIELDS = frozenset(
    {
        "candidate_uniform_matrix_row_norm_upper",
        "candidate_normalized_green_integral_upper",
        "lag_cover_factor_upper",
        "target_bootstrap_error_upper",
        "bootstrapped_exact_boundary_upper",
        "bootstrapped_exact_green_upper",
        "full_green_target",
        "full_boundary_target",
        "strict_exact_arb_target_comparison",
        "full_green_target_closes",
        "full_boundary_target_closes",
        "target_bootstrap_closes",
    }
)
COMBINED_FIELDS = frozenset(
    {
        "guide_voltage_phase_ratio_uniform_upper",
        "guide_recovery_phase_ratio_uniform_upper",
        "voltage_joint_augmented_residual_upper",
        "recovery_joint_augmented_residual_upper",
        "voltage_joint_atom_upper",
        "recovery_joint_atom_upper",
        "voltage_effective_residual_upper",
        "recovery_effective_residual_upper",
        "voltage_target",
        "recovery_target",
        "voltage_target_stage3f_field",
        "recovery_target_stage3f_field",
        "targets_exactly_ingressed_from_stage3f",
        "strict_exact_arb_target_comparison",
        "voltage_target_closes",
        "recovery_target_closes",
        "direct_combined_row_uniform_size_still_open",
        "triangle_bound_uses_joint_S_and_terminal_phase_row",
    }
)
TRANSFER_ERROR_FIELDS = frozenset({"E_voltage", "E_recovery", "E_phase"})
TRANSFER_GATE_FIELDS = frozenset(
    {
        "complete_directed_tensor_geometry_validated",
        "full_advanced_green_target_validated",
        "full_advanced_boundary_target_validated",
        "joint_augmented_phase_residual_targets_validated",
        "strict_combined_row_uniform_sizes_validated",
        "linear_return_gate_evaluated",
        "arbitrary_c0_linear_contraction_closes",
        "nonlinear_outer_attraction_closes",
    }
)


def _require_unique_integer_assignment(
    source: str, name: str, expected: int
) -> None:
    """Reject duplicate or silently regressed geometry constants."""

    tree = ast.parse(source)
    values: list[int] = []
    for statement in tree.body:
        if not isinstance(statement, (ast.Assign, ast.AnnAssign)):
            continue
        targets = (
            statement.targets
            if isinstance(statement, ast.Assign)
            else [statement.target]
        )
        if not any(
            isinstance(target, ast.Name) and target.id == name
            for target in targets
        ):
            continue
        value = statement.value
        if not isinstance(value, ast.Constant) or not isinstance(value.value, int):
            raise ValueError(f"{name} must be a literal integer assignment")
        values.append(value.value)
    if values != [expected]:
        raise ValueError(
            f"{name} must occur exactly once with value {expected}; found {values}"
        )


def _validate_static_geometry_constants(repository: Path) -> None:
    source = (repository / SOURCE_RELATIVE_PATH).read_text()
    for name, expected in (
        ("DELTA_CELL_COUNT", 20),
        ("LAG_CELL_COUNT", 48),
        ("ORDINARY_RECTANGLE_COUNT", 730),
        ("TERMINAL_EXTENDED_RECTANGLE_COUNT", 40),
    ):
        _require_unique_integer_assignment(source, name, expected)


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


def _mapping(value: Any, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{name} must be a mapping")
    return value


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


def _load_parent(repository: Path, relative: str, expected: str) -> Mapping[str, Any]:
    path = repository / relative
    if _sha256_path(path) != expected:
        raise ValueError(f"a Stage-3G parent changed: {relative}")
    return _mapping(json.loads(path.read_text()), relative)


def _pinned_outer_guide_period(outer: Mapping[str, Any]) -> float:
    artifact = _mapping(outer.get("artifact"), "outer parent artifact")
    strategy = _mapping(
        artifact.get("resolution_strategy"), "outer resolution strategy"
    )
    primary = strategy.get("primary_node_count")
    if primary != 257:
        raise ValueError("the pinned outer primary resolution changed")
    resolutions = _mapping(artifact.get("resolutions"), "outer resolutions")
    resolution = _mapping(
        resolutions.get(str(primary)), "outer primary resolution"
    )
    period_record = _mapping(
        resolution.get("period"), "outer primary period record"
    )
    hexadecimal = period_record.get("binary64_hex")
    decimal = period_record.get("decimal")
    if not isinstance(hexadecimal, str) or not isinstance(decimal, str):
        raise ValueError("the outer primary period record changed")
    try:
        period = float.fromhex(hexadecimal)
    except ValueError as error:
        raise ValueError("the outer primary period hex is invalid") from error
    if (
        not math.isfinite(period)
        or period <= 0
        or period.hex() != hexadecimal
        or Decimal(decimal) != Decimal(str(period))
    ):
        raise ValueError("the outer primary period record is inconsistent")
    return period


def _require_unique_disjoint_flags(
    true_flags: Sequence[str], false_flags: Sequence[str]
) -> None:
    if len(true_flags) != len(set(true_flags)):
        raise ValueError("the Stage-3G true-flag registry contains duplicates")
    if len(false_flags) != len(set(false_flags)):
        raise ValueError("the Stage-3G false-flag registry contains duplicates")
    overlap = set(true_flags) & set(false_flags)
    if overlap:
        raise ValueError(f"the Stage-3G flag registries overlap: {sorted(overlap)}")


def _validate_parent_artifact_lock(
    payload: Mapping[str, Any],
    repository: Path,
    *,
    label: str,
    schema_id: str,
    result_relative_path: str,
    validate_sources: bool,
    required_sources: frozenset[str] = frozenset(),
) -> Mapping[str, Any]:
    if set(payload) != {"certificate", "manifest"}:
        raise ValueError(f"the {label} parent top-level schema changed")
    certificate = _mapping(payload.get("certificate"), f"{label} certificate")
    manifest = _mapping(payload.get("manifest"), f"{label} manifest")
    if set(manifest) != PARENT_MANIFEST_FIELDS:
        raise ValueError(f"the {label} parent manifest schema changed")
    if (
        manifest.get("schema_id") != schema_id
        or manifest.get("result") != result_relative_path
        or certificate.get("schema_id") != schema_id
    ):
        raise ValueError(f"the {label} parent identity changed")
    if canonical_sha256(certificate) != manifest.get("certificate_sha256"):
        raise ValueError(f"the {label} parent certificate digest changed")
    sources = _mapping(manifest.get("source_sha256"), f"{label} source manifest")
    if not required_sources.issubset(sources):
        missing = sorted(required_sources - set(sources))
        raise ValueError(f"the {label} runtime source lock is incomplete: {missing}")
    if validate_sources:
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


def _validate_stage3f_target_ingress(stage3f: Mapping[str, Any]) -> Mapping[str, Any]:
    certificate = _mapping(stage3f.get("certificate"), "Stage-3F certificate")
    targets = _mapping(
        certificate.get("residual_closure_targets"),
        "Stage-3F closure targets",
    )
    if targets.get("full_advanced_green_target") != FULL_GREEN_TARGET:
        raise ValueError("the Stage-3F Green target changed")
    if targets.get("full_advanced_boundary_target") != FULL_BOUNDARY_TARGET:
        raise ValueError("the Stage-3F boundary target changed")
    rows = _mapping(targets.get("rows"), "Stage-3F target rows")
    if set(rows) != {"voltage", "recovery"}:
        raise ValueError("the Stage-3F target row schema changed")
    expected = {
        "voltage": VOLTAGE_RESIDUAL_TARGET,
        "recovery": RECOVERY_RESIDUAL_TARGET,
    }
    for name, target in expected.items():
        row = _mapping(rows.get(name), f"Stage-3F {name} target row")
        if row.get("required_combined_p_bernstein_residual_upper") != target:
            raise ValueError(f"the Stage-3F {name} residual target changed")
        if row.get("budget_closes_if_targets_are_proved") is not True:
            raise ValueError(f"the Stage-3F {name} target contract weakened")
    return targets


def _arb_strict_upper_below(value: arb, exact_target: str) -> bool:
    target = arb(exact_target)
    if not target.lower() > 0:
        raise ValueError("a Stage-3G exact target is not positive")
    return bool(value.abs_upper() < target.lower())


def _exact_arb_float(value: float) -> arb:
    number = float(value)
    if not math.isfinite(number):
        raise ValueError("a Stage-3G dyadic candidate is not finite")
    numerator, denominator = number.as_integer_ratio()
    return arb(numerator) / denominator


def _arb_fraction(value: Fraction) -> arb:
    return arb(value.numerator) / value.denominator


def _arb_interval(value: DirectedInterval) -> arb:
    lower = arb(decimal_lower(value.lower, 70))
    upper = arb(decimal_upper(value.upper, 70))
    return lower.union(upper)


def _arb_mpfr_upper(value: gmpy2.mpfr) -> arb:
    return arb(decimal_upper(value, 70))


def _arb_mpfr_lower(value: gmpy2.mpfr) -> arb:
    return arb(decimal_lower(value, 70))


def _arb_upper_float(value: arb) -> float:
    return math.nextafter(float(value.abs_upper()), math.inf)


def _upper_record(value: arb) -> str:
    return format(_arb_upper_float(value), ".17g")


def _matrix_from_float(value: np.ndarray) -> arb_mat:
    array = np.asarray(value, dtype=float)
    return arb_mat(
        [[_exact_arb_float(array[i, j]) for j in range(array.shape[1])]
         for i in range(array.shape[0])]
    )


def _zero_matrix(rows: int, columns: int) -> arb_mat:
    return arb_mat(rows, columns)


def _chebyshev_power_polynomials(degree: int) -> tuple[tuple[Fraction, ...], ...]:
    answer: list[list[Fraction]] = [[Fraction(1)]]
    if degree >= 1:
        answer.append([Fraction(0), Fraction(1)])
    for current in range(2, degree + 1):
        polynomial = [Fraction(0)] * (current + 1)
        for index, value in enumerate(answer[-1]):
            polynomial[index + 1] += 2 * value
        for index, value in enumerate(answer[-2]):
            polynomial[index] -= value
        answer.append(polynomial)
    return tuple(tuple(value) for value in answer)


def _power_polynomial_to_bernstein(
    polynomial: Sequence[Fraction],
    degree: int,
    center: Fraction = Fraction(0),
    scale: Fraction = Fraction(1),
) -> tuple[Fraction, ...]:
    """Map p(center+scale*X), -1<=X<=1, to degree-N Bernstein."""

    x_power = [Fraction(0)] * (degree + 1)
    for source_degree, coefficient in enumerate(polynomial):
        for power in range(source_degree + 1):
            x_power[power] += (
                coefficient
                * math.comb(source_degree, power)
                * center ** (source_degree - power)
                * scale**power
            )
    unit_power = [Fraction(0)] * (degree + 1)
    for source_degree, coefficient in enumerate(x_power):
        for power in range(source_degree + 1):
            unit_power[power] += (
                coefficient
                * math.comb(source_degree, power)
                * 2**power
                * (-1) ** (source_degree - power)
            )
    return tuple(
        sum(
            unit_power[power]
            * Fraction(math.comb(index, power), math.comb(degree, power))
            for power in range(index + 1)
        )
        for index in range(degree + 1)
    )


@lru_cache(maxsize=None)
def _chebyshev_to_bernstein_matrix(
    degree: int, center: Fraction, scale: Fraction
) -> arb_mat:
    polynomials = _chebyshev_power_polynomials(degree)
    columns = tuple(
        _power_polynomial_to_bernstein(value, degree, center, scale)
        for value in polynomials
    )
    return arb_mat(
        [[_arb_fraction(columns[column][row]) for column in range(degree + 1)]
         for row in range(degree + 1)]
    )


@lru_cache(maxsize=None)
def _power_to_bernstein_matrix(degree: int) -> arb_mat:
    columns = []
    for power in range(degree + 1):
        polynomial = [Fraction(0)] * power + [Fraction(1)]
        columns.append(_power_polynomial_to_bernstein(polynomial, degree))
    return arb_mat(
        [[_arb_fraction(columns[column][row]) for column in range(degree + 1)]
         for row in range(degree + 1)]
    )


@lru_cache(maxsize=None)
def _degree_elevation_matrix(source: int, target: int) -> arb_mat:
    if source > target:
        raise ValueError("Bernstein degree elevation cannot lower degree")
    rows = []
    for target_index in range(target + 1):
        row = []
        for source_index in range(source + 1):
            if not (
                max(0, target_index - (target - source))
                <= source_index
                <= min(source, target_index)
            ):
                row.append(arb(0))
                continue
            weight = Fraction(
                math.comb(source, source_index)
                * math.comb(target - source, target_index - source_index),
                math.comb(target, target_index),
            )
            row.append(_arb_fraction(weight))
        rows.append(row)
    return arb_mat(rows)


def _elevate(value: arb_mat, rows: int, columns: int) -> arb_mat:
    return (
        _degree_elevation_matrix(value.nrows() - 1, rows - 1)
        * value
        * _degree_elevation_matrix(value.ncols() - 1, columns - 1).transpose()
    )


def _bernstein_product(left: arb_mat, right: arb_mat) -> arb_mat:
    """Multiply two tensor Bernstein polynomials with outward Arb balls."""

    m, n = left.nrows() - 1, left.ncols() - 1
    p, q = right.nrows() - 1, right.ncols() - 1
    left_rows = [
        arb_poly(
            [
                left[i, j] * math.comb(m, i) * math.comb(n, j)
                for j in range(n + 1)
            ]
        )
        for i in range(m + 1)
    ]
    right_rows = [
        arb_poly(
            [
                right[i, j] * math.comb(p, i) * math.comb(q, j)
                for j in range(q + 1)
            ]
        )
        for i in range(p + 1)
    ]
    result_rows = [arb_poly() for _ in range(m + p + 1)]
    for left_index, left_row in enumerate(left_rows):
        for right_index, right_row in enumerate(right_rows):
            result_rows[left_index + right_index] += left_row * right_row
    return arb_mat(
        [
            [
                result_rows[i][j]
                / (math.comb(m + p, i) * math.comb(n + q, j))
                for j in range(n + q + 1)
            ]
            for i in range(m + p + 1)
        ]
    )


def _matrix_max_abs(value: arb_mat) -> arb:
    answer = arb(0)
    for row in value.tolist():
        for coefficient in row:
            answer = max(answer, coefficient.abs_upper())
    return answer


def _two_component_row_max(first: arb_mat, second: arb_mat) -> arb:
    if first.nrows() != second.nrows() or first.ncols() != second.ncols():
        raise ValueError("row component Bernstein degrees differ")
    answer = arb(0)
    for i in range(first.nrows()):
        for j in range(first.ncols()):
            answer = max(
                answer,
                first[i, j].abs_upper() + second[i, j].abs_upper(),
            )
    return answer


class _TensorGuide:
    """Binary source guide, including an equation-consistent terminal extension."""

    def __init__(self, orbit: Any):
        self.guide = _PrimitiveGuide(orbit, GUIDE_MAXIMUM_STEP)
        self.period = self.guide.period
        self.h = float(TAU_1) / DELTA_CELL_COUNT
        self.taus = (float(TAU_0), float(TAU_1))
        self.delta_nodes = np.cos(
            np.pi * np.arange(DELTA_DEGREE + 1) / DELTA_DEGREE
        )
        self.lag_nodes = np.cos(
            np.pi * np.arange(LAG_DEGREE + 1) / LAG_DEGREE
        )
        self._extension: dict[float, Any] = {}
        self._coefficients: dict[tuple[int, int], np.ndarray] = {}

    def _extension_solution(self, terminal: float) -> Any:
        key = float(terminal)
        if key in self._extension:
            return self._extension[key]
        initial = self.guide.resolvent(terminal, np.asarray([0.0]))[0]

        def rhs(lag: float, flattened: np.ndarray) -> np.ndarray:
            start = terminal - lag
            value = flattened.reshape(2, 2)
            derivative = value @ self.guide.current_matrix(start)
            for delay_index, delay in enumerate(self.taus):
                earlier = self.guide.resolvent(
                    terminal, np.asarray([start + delay])
                )[0]
                derivative[:, 0] += (
                    earlier[:, 0]
                    * self.guide.delayed_scalar(delay_index, start + delay)
                )
            return derivative.ravel()

        solution = solve_ivp(
            rhs,
            (terminal, terminal + EXTENSION_SOLVE_HORIZON),
            initial.ravel(),
            method="DOP853",
            rtol=2.0e-12,
            atol=2.0e-14,
            max_step=EXTENSION_MAXIMUM_STEP,
            dense_output=True,
        )
        if not solution.success:
            raise ArithmeticError("the Stage-3G terminal extension failed")
        self._extension[key] = solution
        return solution

    def resolvent(self, terminal: float, start: np.ndarray) -> np.ndarray:
        values = np.asarray(start, dtype=float)
        answer = np.empty((len(values), 2, 2), dtype=float)
        physical = values >= 0
        if np.any(physical):
            answer[physical] = self.guide.resolvent(terminal, values[physical])
        if np.any(~physical):
            extension = self._extension_solution(terminal)
            answer[~physical] = extension.sol(terminal - values[~physical]).T.reshape(
                -1, 2, 2
            )
        return answer

    def coefficients(self, delta_cell: int, lag_cell: int) -> np.ndarray:
        key = (delta_cell, lag_cell)
        if key in self._coefficients:
            return self._coefficients[key]
        deltas = (
            (delta_cell + 0.5) * self.h
            + 0.5 * self.h * self.delta_nodes
        )
        lags = (
            (lag_cell + 0.5) * self.h
            + 0.5 * self.h * self.lag_nodes
        )
        values = np.empty(
            (DELTA_DEGREE + 1, LAG_DEGREE + 1, 2, 2), dtype=float
        )
        for index, delta in enumerate(deltas):
            terminal = self.period - delta
            values[index] = self.resolvent(terminal, terminal - lags)
        coefficients = np.empty_like(values)
        for row in range(2):
            for column in range(2):
                lag_coefficients = np.asarray(
                    [
                        np.polynomial.chebyshev.chebfit(
                            self.lag_nodes,
                            values[index, :, row, column],
                            LAG_DEGREE,
                        )
                        for index in range(DELTA_DEGREE + 1)
                    ]
                )
                for lag_degree in range(LAG_DEGREE + 1):
                    coefficients[:, lag_degree, row, column] = (
                        np.polynomial.chebyshev.chebfit(
                            self.delta_nodes,
                            lag_coefficients[:, lag_degree],
                            DELTA_DEGREE,
                        )
                    )
        if not np.all(np.isfinite(coefficients)):
            raise ArithmeticError("a Stage-3G guide chart is not finite")
        self._coefficients[key] = coefficients
        return coefficients


def _patch_centers() -> tuple[Fraction, ...]:
    return tuple(
        Fraction(2 * index + 1 - SUBDIVISION_PARTS, SUBDIVISION_PARTS)
        for index in range(SUBDIVISION_PARTS)
    )


def _candidate_patch(
    coefficients: np.ndarray, delta_center: Fraction, lag_center: Fraction
) -> tuple[tuple[arb_mat, arb_mat], tuple[arb_mat, arb_mat]]:
    scale = Fraction(1, SUBDIVISION_PARTS)
    delta_transform = _chebyshev_to_bernstein_matrix(
        DELTA_DEGREE, delta_center, scale
    )
    lag_transform = _chebyshev_to_bernstein_matrix(
        LAG_DEGREE, lag_center, scale
    )
    rows: list[tuple[arb_mat, arb_mat]] = []
    for row in range(2):
        components = []
        for column in range(2):
            components.append(
                delta_transform
                * _matrix_from_float(coefficients[:, :, row, column])
                * lag_transform.transpose()
            )
        rows.append((components[0], components[1]))
    return (rows[0], rows[1])


def _fourier_taylor_patch(
    sequence: Mapping[int, DirectedComplexInterval],
    *,
    center_time: DirectedInterval,
    period: DirectedInterval,
    h: DirectedInterval,
) -> tuple[arb_mat, gmpy2.mpfr, gmpy2.mpfr]:
    """Return a tensor Bernstein Taylor polynomial and strict two remainders."""

    zero = DirectedInterval.from_decimal(0, PRECISION_BITS)
    one = DirectedInterval.from_decimal(1, PRECISION_BITS)
    pi = pi_interval(PRECISION_BITS)
    scale = DirectedInterval.from_decimal(
        SUBDIVISION_PARTS, PRECISION_BITS
    )
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
                2 * pi.upper * abs(mode) * h.upper
                / (period.lower * SUBDIVISION_PARTS)
            )
            remainder += (
                magnitude
                * maximum_argument ** (COEFFICIENT_DEGREE + 1)
                / factorial
            )
    power = [[arb(0) for _ in range(COEFFICIENT_DEGREE + 1)]
             for _ in range(COEFFICIENT_DEGREE + 1)]
    for degree, coefficient in enumerate(coefficients):
        real = _arb_interval(coefficient.real)
        for first in range(degree + 1):
            power[first][degree - first] += real * math.comb(degree, first)
    transform = _power_to_bernstein_matrix(COEFFICIENT_DEGREE)
    polynomial = transform * arb_mat(power) * transform.transpose()
    return polynomial, tail, remainder


@dataclass(frozen=True)
class OuterResolventStage3GTensor:
    schema_id: str
    model_id: str
    branch: str
    arithmetic_scope: str
    precision_bits: int
    parent_result_sha256: dict[str, str]
    tensor_geometry: dict[str, Any]
    coefficient_remainder: dict[str, str]
    resolvent_residual: dict[str, Any]
    chart_defects: dict[str, Any]
    green_bootstrap: dict[str, Any]
    phase_combination_target: dict[str, Any]
    transfer_errors: dict[str, str | None]
    transfer_gate: dict[str, bool]
    claim_status: dict[str, bool]
    conclusion: str


def _directed_geometry_preflight(
    period: DirectedInterval,
    h_binary64: float,
    guide_period_binary64: float,
) -> dict[str, Any]:
    """Prove the complete rectangle count before the expensive sweep."""

    h = DirectedInterval.from_float(h_binary64, PRECISION_BITS)
    period_minus_47h = period - h * (LAG_CELL_COUNT - 1)
    forty_eight_h_minus_period = h * LAG_CELL_COUNT - period
    terminal_extension = h * (LAG_CELL_COUNT + 1) - period
    decimal_limit = DirectedInterval.from_decimal("0.85", PRECISION_BITS)
    solve_horizon = DirectedInterval.from_float(
        EXTENSION_SOLVE_HORIZON, PRECISION_BITS
    )
    solve_margin = solve_horizon - terminal_extension
    guide_period = DirectedInterval.from_float(
        guide_period_binary64, PRECISION_BITS
    )
    if guide_period.lower < period.lower or guide_period.upper > period.upper:
        raise ArithmeticError(
            "the binary64 guide period is outside the directed period interval"
        )
    if period_minus_47h.lower <= 0 or forty_eight_h_minus_period.lower <= 0:
        raise ArithmeticError("the directed period does not satisfy 47h<T<48h")
    if terminal_extension.lower <= 0 or terminal_extension.upper >= decimal_limit.lower:
        raise ArithmeticError(
            "the directed terminal extension does not satisfy 0<49h-T<0.85"
        )
    if terminal_extension.upper >= solve_horizon.lower:
        raise ArithmeticError(
            "the terminal extension is not covered by the numerical solve horizon"
        )

    ordinary = 0
    terminal = 0
    for delta_cell in range(DELTA_CELL_COUNT):
        for lag_cell in range(LAG_CELL_COUNT - delta_cell):
            if lag_cell >= LAG_CELL_COUNT - 2 - delta_cell:
                terminal += 1
            else:
                ordinary += 1
    patches = (ordinary + terminal) * SUBDIVISION_PARTS**2
    if (
        ordinary != ORDINARY_RECTANGLE_COUNT
        or terminal != TERMINAL_EXTENDED_RECTANGLE_COUNT
        or patches != 12320
    ):
        raise AssertionError(
            "the Stage-3G zero-cost geometry preflight changed: "
            f"ordinary={ordinary}, terminal={terminal}, patches={patches}"
        )
    ratio = period / h
    return {
        "period_mesh_ratio_interval": {
            "lower": decimal_lower(ratio.lower, 70),
            "upper": decimal_upper(ratio.upper, 70),
        },
        "period_minus_47h_lower": decimal_lower(period_minus_47h.lower, 70),
        "48h_minus_period_lower": decimal_lower(
            forty_eight_h_minus_period.lower, 70
        ),
        "period_strictly_between_47h_and_48h": True,
        "guide_period_binary64_hex": guide_period_binary64.hex(),
        "guide_period_inside_directed_period_interval": True,
        "terminal_extension_length_interval": {
            "lower": decimal_lower(terminal_extension.lower, 70),
            "upper": decimal_upper(terminal_extension.upper, 70),
        },
        "terminal_extension_decimal_limit": "0.85",
        "terminal_extension_solver_horizon_binary64_hex": (
            EXTENSION_SOLVE_HORIZON.hex()
        ),
        "terminal_extension_solver_horizon_lower": decimal_lower(
            solve_horizon.lower, 70
        ),
        "terminal_extension_solver_margin_lower": decimal_lower(
            solve_margin.lower, 70
        ),
        "terminal_extension_strictly_between_zero_and_0p85": True,
        "terminal_extension_within_solver_horizon": True,
        "ordinary_rectangle_count": ordinary,
        "terminal_extended_rectangle_count": terminal,
        "tensor_patch_count": patches,
    }


def _build_tensor_certificate(
    guide: _TensorGuide,
    base: Any,
    stage3f: Mapping[str, Any],
    stage3d: Mapping[str, Any],
) -> dict[str, Any]:
    _validate_stage3f_target_ingress(stage3f)
    period_interval = base.period
    h_interval = DirectedInterval.from_float(guide.h, PRECISION_BITS)
    geometry_preflight = _directed_geometry_preflight(
        period_interval, guide.h, guide.period
    )
    if guide.taus[0] != 16 * guide.h or guide.taus[1] != 20 * guide.h:
        raise ArithmeticError("the two binary64 delays are not mesh aligned")
    centers = _patch_centers()
    scale = Fraction(1, SUBDIVISION_PARTS)
    result_degree_delta = DELTA_DEGREE + COEFFICIENT_DEGREE
    result_degree_lag = LAG_DEGREE + COEFFICIENT_DEGREE
    result_shape = (result_degree_delta + 1, result_degree_lag + 1)
    maximum_rows = [arb(0), arb(0)]
    maximum_row_locations: list[dict[str, Any] | None] = [None, None]
    maximum_polynomial_rows = [arb(0), arb(0)]
    maximum_tail_rows = [arb(0), arb(0)]
    maximum_candidate_uniform = arb(0)
    epsilon_arb = _arb_interval(base.parameters["epsilon"])
    period_upper_arb = _arb_mpfr_upper(period_interval.upper)
    green_cell_bounds: dict[tuple[int, int], arb] = {}
    coefficient_cache: dict[
        tuple[str, int, int, Fraction], tuple[arb_mat, gmpy2.mpfr, gmpy2.mpfr]
    ] = {}

    def coefficient(
        kind: str,
        delay_index: int,
        total_cell: int,
        center_sum: Fraction,
    ) -> tuple[arb_mat, gmpy2.mpfr, gmpy2.mpfr]:
        key = (kind, delay_index, total_cell, center_sum)
        if key in coefficient_cache:
            return coefficient_cache[key]
        center = period_interval - h_interval * (total_cell + 1)
        center_shift = DirectedInterval.from_decimal(
            center_sum.numerator, PRECISION_BITS
        ) / DirectedInterval.from_decimal(
            2 * center_sum.denominator, PRECISION_BITS
        )
        center = center - h_interval * center_shift
        sequence = (
            base.current_coefficient
            if kind == "current"
            else base.delayed_coefficients[delay_index]
        )
        if kind == "delay":
            center = center + DirectedInterval.from_float(
                guide.taus[delay_index], PRECISION_BITS
            )
        value = _fourier_taylor_patch(
            sequence,
            center_time=center,
            period=period_interval,
            h=h_interval,
        )
        coefficient_cache[key] = value
        return value

    ordinary = 0
    terminal = 0
    for delta_cell in range(DELTA_CELL_COUNT):
        final_lag_cell = LAG_CELL_COUNT - 1 - delta_cell
        for lag_cell in range(final_lag_cell + 1):
            if lag_cell >= LAG_CELL_COUNT - 2 - delta_cell:
                terminal += 1
            else:
                ordinary += 1
            current_coefficients = guide.coefficients(delta_cell, lag_cell)
            for delta_center in centers:
                for lag_center in centers:
                    current = _candidate_patch(
                        current_coefficients, delta_center, lag_center
                    )
                    current_scalar, current_tail, current_taylor = coefficient(
                        "current",
                        0,
                        delta_cell + lag_cell,
                        delta_center + lag_center,
                    )
                    delayed_data = [
                        coefficient(
                            "delay",
                            delay_index,
                            delta_cell + lag_cell,
                            delta_center + lag_center,
                        )
                        for delay_index in range(2)
                    ]
                    delayed_candidates: list[
                        tuple[tuple[arb_mat, arb_mat], tuple[arb_mat, arb_mat]] | None
                    ] = []
                    for shift in (16, 20):
                        if lag_cell < shift:
                            delayed_candidates.append(None)
                        else:
                            delayed_candidates.append(
                                _candidate_patch(
                                    guide.coefficients(
                                        delta_cell, lag_cell - shift
                                    ),
                                    delta_center,
                                    lag_center,
                                )
                            )
                    for row in range(2):
                        first, second = current[row]
                        derivative_components = []
                        derivative_scale = arb(LAG_DEGREE) / (
                            _exact_arb_float(guide.h)
                            * _arb_fraction(scale)
                        )
                        for component in (first, second):
                            derivative_components.append(
                                arb_mat(
                                    [
                                        [
                                            (component[i, j + 1] - component[i, j])
                                            * derivative_scale
                                            for j in range(LAG_DEGREE)
                                        ]
                                        for i in range(DELTA_DEGREE + 1)
                                    ]
                                )
                            )
                        residual_first = _elevate(
                            derivative_components[0], *result_shape
                        )
                        residual_first -= _bernstein_product(
                            first, current_scalar
                        )
                        residual_first -= _elevate(
                            second * epsilon_arb,
                            *result_shape,
                        )
                        residual_second = _elevate(
                            derivative_components[1], *result_shape
                        )
                        residual_second += _elevate(first, *result_shape)
                        residual_second += _elevate(
                            second * epsilon_arb,
                            *result_shape,
                        )
                        tail_cost = _arb_mpfr_upper(
                            current_tail + current_taylor
                        ) * (
                            _matrix_max_abs(first)
                        )
                        for delay_index, delayed_candidate in enumerate(
                            delayed_candidates
                        ):
                            if delayed_candidate is None:
                                continue
                            delayed_first = delayed_candidate[row][0]
                            delayed_polynomial, delayed_tail, delayed_taylor = (
                                delayed_data[delay_index]
                            )
                            residual_first -= _bernstein_product(
                                delayed_first, delayed_polynomial
                            )
                            tail_cost += _arb_mpfr_upper(
                                delayed_tail + delayed_taylor
                            ) * (
                                _matrix_max_abs(delayed_first)
                            )
                        polynomial_row = _two_component_row_max(
                            residual_first, residual_second
                        )
                        normalized_polynomial = polynomial_row * period_upper_arb
                        normalized_tail = tail_cost * period_upper_arb
                        normalized_total = normalized_polynomial + normalized_tail
                        maximum_polynomial_rows[row] = max(
                            maximum_polynomial_rows[row], normalized_polynomial
                        )
                        maximum_tail_rows[row] = max(
                            maximum_tail_rows[row], normalized_tail
                        )
                        if normalized_total.abs_upper() > maximum_rows[row].abs_upper():
                            maximum_rows[row] = normalized_total
                            maximum_row_locations[row] = {
                                "delta_cell": delta_cell,
                                "lag_cell": lag_cell,
                                "delta_patch_center": str(delta_center),
                                "lag_patch_center": str(lag_center),
                                "terminal_extended_cell": bool(
                                    lag_cell
                                    >= LAG_CELL_COUNT - 2 - delta_cell
                                ),
                            }
                        candidate_row = _two_component_row_max(first, second)
                        maximum_candidate_uniform = max(
                            maximum_candidate_uniform, candidate_row
                        )
                        key = (delta_cell, lag_cell)
                        green_cell_bounds[key] = max(
                            green_cell_bounds.get(key, arb(0)), candidate_row
                        )
    if (
        ordinary != ORDINARY_RECTANGLE_COUNT
        or terminal != TERMINAL_EXTENDED_RECTANGLE_COUNT
    ):
        raise AssertionError(
            "the Stage-3G tensor cover count changed: "
            f"ordinary={ordinary}, terminal={terminal}"
        )

    # Boundary and one-sided lag-chart interface atoms.  Delta interfaces do
    # not enter the ell evolution: each delta is an independent parameter.
    boundary = arb(0)
    interface_sum = arb(0)
    interface_maximum = arb(0)
    whole_delta = _chebyshev_to_bernstein_matrix(
        DELTA_DEGREE, Fraction(0), Fraction(1)
    )
    for delta_cell in range(DELTA_CELL_COUNT):
        first = guide.coefficients(delta_cell, 0)
        lag_minus_signs = (-1.0) ** np.arange(LAG_DEGREE + 1)
        lag_plus_signs = np.ones(LAG_DEGREE + 1)
        for row in range(2):
            components = []
            for column in range(2):
                endpoint = first[:, :, row, column] @ lag_minus_signs
                target = 1.0 if row == column else 0.0
                vector = np.asarray(endpoint, dtype=float).reshape(-1)
                difference = vector.copy()
                difference[0] -= target
                components.append(
                    whole_delta
                    * arb_mat([[_exact_arb_float(value)] for value in difference])
                )
            local = arb(0)
            for index in range(DELTA_DEGREE + 1):
                local = max(
                    local,
                    components[0][index, 0].abs_upper()
                    + components[1][index, 0].abs_upper(),
                )
            boundary = max(boundary, local)
        final_lag_cell = LAG_CELL_COUNT - 1 - delta_cell
        local_interface_sum = arb(0)
        for lag_cell in range(1, final_lag_cell + 1):
            right = guide.coefficients(delta_cell, lag_cell)
            left = guide.coefficients(delta_cell, lag_cell - 1)
            local_matrix = arb(0)
            for row in range(2):
                row_components = []
                for column in range(2):
                    right_edge = right[:, :, row, column] @ lag_minus_signs
                    left_edge = left[:, :, row, column] @ lag_plus_signs
                    difference = np.asarray(right_edge - left_edge).reshape(-1)
                    row_components.append(
                        whole_delta
                        * arb_mat(
                            [[_exact_arb_float(value)] for value in difference]
                        )
                    )
                local = arb(0)
                for index in range(DELTA_DEGREE + 1):
                    local = max(
                        local,
                        row_components[0][index, 0].abs_upper()
                        + row_components[1][index, 0].abs_upper(),
                    )
                local_matrix = max(local_matrix, local)
            interface_maximum = max(interface_maximum, local_matrix)
            local_interface_sum += local_matrix
        interface_sum = max(interface_sum, local_interface_sum)

    candidate_green = arb(0)
    coverage_factor = arb(0)
    for delta_cell in range(DELTA_CELL_COUNT):
        local = arb(0)
        for lag_cell in range(LAG_CELL_COUNT - delta_cell):
            local += green_cell_bounds[(delta_cell, lag_cell)] * (
                _exact_arb_float(guide.h)
                / _arb_mpfr_lower(period_interval.lower)
            )
        candidate_green = max(candidate_green, local)
        coverage_factor = max(
            coverage_factor,
            arb(LAG_CELL_COUNT - delta_cell) * _exact_arb_float(guide.h)
            / _arb_mpfr_lower(period_interval.lower),
        )

    phase = _mapping(
        _mapping(stage3d.get("certificate"), "Stage-3D certificate").get(
            "continuous_phase_projection"
        ),
        "Stage-3D phase projection",
    )
    q0 = arb(str(phase["guide_phase_speed_interval"]["lower"]))
    if not q0.lower() > 0:
        raise ArithmeticError("the Stage-3D phase-speed lower bound is not positive")
    alpha = arb(str(phase["guide_voltage_speed_wiener_upper"])) / q0
    beta = arb(str(phase["guide_recovery_speed_wiener_upper"])) / q0
    matrix_residual = max(maximum_rows)
    atom = boundary + interface_sum
    voltage_combined = (1 + alpha) * matrix_residual
    recovery_combined = (1 + beta) * matrix_residual
    voltage_atom = (1 + alpha) * atom
    recovery_atom = (1 + beta) * atom
    target_green = arb(FULL_GREEN_TARGET)
    target_boundary = arb(FULL_BOUNDARY_TARGET)
    voltage_effective = voltage_combined + (
        target_boundary / target_green
    ) * voltage_atom
    recovery_effective = recovery_combined + (
        target_boundary / target_green
    ) * recovery_atom

    # A target bootstrap: if the exact Green/boundary pair first reached the
    # declared target, the parametrix equation would still put it strictly
    # below that target.  Continuity in terminal time closes the bootstrap.
    bootstrap_error = target_green * matrix_residual + target_boundary * atom
    exact_boundary_candidate = maximum_candidate_uniform + bootstrap_error
    exact_green_candidate = candidate_green + coverage_factor * bootstrap_error
    boundary_closes = _arb_strict_upper_below(
        exact_boundary_candidate, FULL_BOUNDARY_TARGET
    )
    green_integral_closes = _arb_strict_upper_below(
        exact_green_candidate, FULL_GREEN_TARGET
    )
    green_closes = bool(boundary_closes and green_integral_closes)
    voltage_closes = _arb_strict_upper_below(
        voltage_effective, VOLTAGE_RESIDUAL_TARGET
    )
    recovery_closes = _arb_strict_upper_below(
        recovery_effective, RECOVERY_RESIDUAL_TARGET
    )
    if len(coefficient_cache) != EXPECTED_COEFFICIENT_PATCH_COUNT:
        raise AssertionError(
            "the Stage-3G coefficient patch cache changed: "
            f"{len(coefficient_cache)}"
        )

    return {
        "geometry": {
            **geometry_preflight,
            "mesh_width_binary64_hex": guide.h.hex(),
            "tau0_mesh_widths": 16,
            "tau1_mesh_widths": 20,
            "delta_cell_count": DELTA_CELL_COUNT,
            "lag_cell_count": LAG_CELL_COUNT,
            "terminal_extension_satisfies_same_retarded_equation": True,
            "physical_terminal_clipped_domain_subset_of_validated_rectangle": True,
            "delta_degree": DELTA_DEGREE,
            "lag_degree": LAG_DEGREE,
            "coefficient_degree": COEFFICIENT_DEGREE,
            "subdivision_parts_per_axis": SUBDIVISION_PARTS,
            "fourier_cutoff": FOURIER_CUTOFF,
        },
        "coefficient": {
            "cached_coefficient_patch_count": len(coefficient_cache),
            "current_tail_plus_taylor_effect_included": True,
            "delayed_tail_plus_taylor_effect_included": True,
        },
        "residual": {
            "voltage_terminal_row_polynomial_upper": _upper_record(
                maximum_polynomial_rows[0]
            ),
            "recovery_terminal_row_polynomial_upper": _upper_record(
                maximum_polynomial_rows[1]
            ),
            "voltage_terminal_row_tail_upper": _upper_record(
                maximum_tail_rows[0]
            ),
            "recovery_terminal_row_tail_upper": _upper_record(
                maximum_tail_rows[1]
            ),
            "voltage_terminal_row_total_upper": _upper_record(maximum_rows[0]),
            "recovery_terminal_row_total_upper": _upper_record(maximum_rows[1]),
            "voltage_terminal_row_maximizer": maximum_row_locations[0],
            "recovery_terminal_row_maximizer": maximum_row_locations[1],
            "full_matrix_row_residual_upper": _upper_record(matrix_residual),
            "normalization": "period times physical-lag residual",
            "signed_matrix_residual_before_row_norm": True,
            "arb_precision_bits": PRECISION_BITS,
        },
        "defects": {
            "initial_boundary_matrix_row_defect_upper": _upper_record(boundary),
            "maximum_one_lag_interface_matrix_row_jump_upper": _upper_record(
                interface_maximum
            ),
            "summed_lag_interface_matrix_row_jump_upper": _upper_record(
                interface_sum
            ),
            "boundary_plus_interface_atom_upper": _upper_record(atom),
            "delta_interfaces_not_evolution_atoms": True,
        },
        "green": {
            "candidate_uniform_matrix_row_norm_upper": _upper_record(
                maximum_candidate_uniform
            ),
            "candidate_normalized_green_integral_upper": _upper_record(
                candidate_green
            ),
            "lag_cover_factor_upper": _upper_record(coverage_factor),
            "target_bootstrap_error_upper": _upper_record(bootstrap_error),
            "bootstrapped_exact_boundary_upper": _upper_record(
                exact_boundary_candidate
            ),
            "bootstrapped_exact_green_upper": _upper_record(
                exact_green_candidate
            ),
            "full_green_target": FULL_GREEN_TARGET,
            "full_boundary_target": FULL_BOUNDARY_TARGET,
            "strict_exact_arb_target_comparison": True,
            "full_green_target_closes": green_integral_closes,
            "full_boundary_target_closes": boundary_closes,
            "target_bootstrap_closes": green_closes,
        },
        "combined": {
            "guide_voltage_phase_ratio_uniform_upper": _upper_record(alpha),
            "guide_recovery_phase_ratio_uniform_upper": _upper_record(beta),
            "voltage_joint_augmented_residual_upper": _upper_record(
                voltage_combined
            ),
            "recovery_joint_augmented_residual_upper": _upper_record(
                recovery_combined
            ),
            "voltage_joint_atom_upper": _upper_record(voltage_atom),
            "recovery_joint_atom_upper": _upper_record(recovery_atom),
            "voltage_effective_residual_upper": _upper_record(voltage_effective),
            "recovery_effective_residual_upper": _upper_record(recovery_effective),
            "voltage_target": VOLTAGE_RESIDUAL_TARGET,
            "recovery_target": RECOVERY_RESIDUAL_TARGET,
            "voltage_target_stage3f_field": (
                "certificate.residual_closure_targets.rows.voltage."
                "required_combined_p_bernstein_residual_upper"
            ),
            "recovery_target_stage3f_field": (
                "certificate.residual_closure_targets.rows.recovery."
                "required_combined_p_bernstein_residual_upper"
            ),
            "targets_exactly_ingressed_from_stage3f": True,
            "strict_exact_arb_target_comparison": True,
            "voltage_target_closes": voltage_closes,
            "recovery_target_closes": recovery_closes,
            "direct_combined_row_uniform_size_still_open": True,
            "triangle_bound_uses_joint_S_and_terminal_phase_row": True,
        },
    }


@lru_cache(maxsize=1)
def build_outer_resolvent_stage3g_tensor(
    repository: Path,
) -> OuterResolventStage3GTensor:
    repository = repository.resolve()
    _validate_static_geometry_constants(repository)
    _require_unique_disjoint_flags(TRUE_FLAGS, FALSE_FLAGS)
    if os.environ.get("OPENBLAS_NUM_THREADS") != PINNED_OPENBLAS_NUM_THREADS:
        raise RuntimeError("Stage-3G requires OPENBLAS_NUM_THREADS=1")
    arb_ctx.prec = PRECISION_BITS
    arb_ctx.threads = 1
    stage3f = _load_parent(
        repository, STAGE3F_RESULT_RELATIVE_PATH, STAGE3F_RESULT_SHA256
    )
    _validate_parent_artifact_lock(
        stage3f,
        repository,
        label="Stage-3F",
        schema_id=STAGE3F_SCHEMA_ID,
        result_relative_path=STAGE3F_RESULT_RELATIVE_PATH,
        validate_sources=False,
    )
    _validate_stage3f_target_ingress(stage3f)
    stage3d = _load_parent(
        repository, STAGE3D_RESULT_RELATIVE_PATH, STAGE3D_RESULT_SHA256
    )
    _validate_parent_artifact_lock(
        stage3d,
        repository,
        label="Stage-3D",
        schema_id=STAGE3D_SCHEMA_ID,
        result_relative_path=STAGE3D_RESULT_RELATIVE_PATH,
        validate_sources=True,
        required_sources=STAGE3D_REQUIRED_RUNTIME_SOURCES,
    )
    outer = _load_parent(repository, OUTER_RESULT_RELATIVE_PATH, OUTER_RESULT_SHA256)
    orbit = validate_outer_high_resolution_artifact(
        outer, repository, replay_directed=False
    )
    base = _build_leaky_base_sequences(orbit, PRECISION_BITS)
    guide = _TensorGuide(orbit)
    data = _build_tensor_certificate(guide, base, stage3f, stage3d)
    geometry = data["geometry"]
    coefficient = data["coefficient"]
    residual = data["residual"]
    defects = data["defects"]
    green = data["green"]
    combined = data["combined"]
    claims = {name: True for name in TRUE_FLAGS}
    claims.update({name: False for name in FALSE_FLAGS})
    green_closes = bool(green["target_bootstrap_closes"])
    green_integral_closes = bool(green["full_green_target_closes"])
    boundary_closes = bool(green["full_boundary_target_closes"])
    combined_closes = bool(
        combined["voltage_target_closes"] and combined["recovery_target_closes"]
    )
    if not (green_closes and green_integral_closes and boundary_closes):
        raise ArithmeticError("the Stage-3G Green target bootstrap failed")
    if not combined_closes:
        raise ArithmeticError("a Stage-3G joint augmented row target failed")
    return OuterResolventStage3GTensor(
        schema_id=SCHEMA_ID,
        model_id=MODEL_ID,
        branch=BRANCH,
        arithmetic_scope=ARITHMETIC_SCOPE,
        precision_bits=PRECISION_BITS,
        parent_result_sha256={
            STAGE3F_RESULT_RELATIVE_PATH: STAGE3F_RESULT_SHA256,
            STAGE3D_RESULT_RELATIVE_PATH: STAGE3D_RESULT_SHA256,
            OUTER_RESULT_RELATIVE_PATH: OUTER_RESULT_SHA256,
        },
        tensor_geometry=geometry,
        coefficient_remainder=coefficient,
        resolvent_residual=residual,
        chart_defects=defects,
        green_bootstrap=green,
        phase_combination_target=combined,
        transfer_errors={
            "E_voltage": None,
            "E_recovery": None,
            "E_phase": _mapping(
                _mapping(stage3f.get("certificate"), "Stage-3F certificate").get(
                    "transfer_errors"
                ),
                "Stage-3F transfer errors",
            )["E_phase"],
        },
        transfer_gate={
            "complete_directed_tensor_geometry_validated": True,
            "full_advanced_green_target_validated": green_integral_closes,
            "full_advanced_boundary_target_validated": boundary_closes,
            "joint_augmented_phase_residual_targets_validated": combined_closes,
            "strict_combined_row_uniform_sizes_validated": False,
            "linear_return_gate_evaluated": False,
            "arbitrary_c0_linear_contraction_closes": False,
            "nonlinear_outer_attraction_closes": False,
        },
        claim_status=claims,
        conclusion=CONCLUSION,
    )


def build_outer_resolvent_stage3g_tensor_result(repository: Path) -> dict[str, Any]:
    repository = repository.resolve()
    certificate = json.loads(
        json.dumps(
            asdict(build_outer_resolvent_stage3g_tensor(repository)),
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


def validate_outer_resolvent_stage3g_tensor_result(
    payload: Mapping[str, Any], repository: Path
) -> None:
    repository = repository.resolve()
    _validate_static_geometry_constants(repository)
    _require_unique_disjoint_flags(TRUE_FLAGS, FALSE_FLAGS)
    if not isinstance(payload, Mapping) or set(payload) != {"certificate", "manifest"}:
        raise ValueError("the Stage-3G top-level schema changed")
    certificate = _mapping(payload.get("certificate"), "Stage-3G certificate")
    manifest = _mapping(payload.get("manifest"), "Stage-3G manifest")
    _require_exact_keys(manifest, RESULT_MANIFEST_FIELDS, "Stage-3G manifest")
    _require_exact_keys(
        certificate,
        {field.name for field in fields(OuterResolventStage3GTensor)},
        "Stage-3G certificate",
    )
    if (
        manifest.get("schema_id") != SCHEMA_ID
        or manifest.get("result") != RESULT_RELATIVE_PATH
        or manifest.get("default_command") != DEFAULT_COMMAND
    ):
        raise ValueError("the Stage-3G manifest identity changed")
    environment = _mapping(
        manifest.get("environment"), "Stage-3G environment"
    )
    _require_exact_keys(environment, ENVIRONMENT_FIELDS, "Stage-3G environment")
    if dict(environment) != _expected_environment():
        raise ValueError("the Stage-3G environment changed")
    if canonical_sha256(certificate) != manifest.get("certificate_sha256"):
        raise ValueError("the Stage-3G certificate digest changed")
    sources = _mapping(manifest.get("source_sha256"), "Stage-3G source manifest")
    if set(sources) != set(SOURCE_MANIFEST):
        raise ValueError("the Stage-3G source set changed")
    for relative in SOURCE_MANIFEST:
        if sources.get(relative) != _sha256_path(repository / relative):
            raise ValueError(f"a Stage-3G source changed: {relative}")

    if (
        certificate.get("schema_id") != SCHEMA_ID
        or certificate.get("model_id") != MODEL_ID
        or certificate.get("branch") != BRANCH
        or certificate.get("arithmetic_scope") != ARITHMETIC_SCOPE
        or certificate.get("precision_bits") != PRECISION_BITS
    ):
        raise ValueError("the Stage-3G certificate identity changed")
    expected_parents = {
        STAGE3F_RESULT_RELATIVE_PATH: STAGE3F_RESULT_SHA256,
        STAGE3D_RESULT_RELATIVE_PATH: STAGE3D_RESULT_SHA256,
        OUTER_RESULT_RELATIVE_PATH: OUTER_RESULT_SHA256,
    }
    parents = _mapping(
        certificate.get("parent_result_sha256"), "Stage-3G parents"
    )
    if dict(parents) != expected_parents:
        raise ValueError("the Stage-3G parent digest map changed")
    stage3f = _load_parent(
        repository, STAGE3F_RESULT_RELATIVE_PATH, STAGE3F_RESULT_SHA256
    )
    stage3f_certificate = _validate_parent_artifact_lock(
        stage3f,
        repository,
        label="Stage-3F",
        schema_id=STAGE3F_SCHEMA_ID,
        result_relative_path=STAGE3F_RESULT_RELATIVE_PATH,
        validate_sources=False,
    )
    _validate_stage3f_target_ingress(stage3f)
    stage3d = _load_parent(
        repository, STAGE3D_RESULT_RELATIVE_PATH, STAGE3D_RESULT_SHA256
    )
    _validate_parent_artifact_lock(
        stage3d,
        repository,
        label="Stage-3D",
        schema_id=STAGE3D_SCHEMA_ID,
        result_relative_path=STAGE3D_RESULT_RELATIVE_PATH,
        validate_sources=True,
        required_sources=STAGE3D_REQUIRED_RUNTIME_SOURCES,
    )
    outer = _load_parent(
        repository, OUTER_RESULT_RELATIVE_PATH, OUTER_RESULT_SHA256
    )

    claims = _mapping(certificate.get("claim_status"), "Stage-3G claims")
    if set(claims) != set(TRUE_FLAGS + FALSE_FLAGS):
        raise ValueError("the Stage-3G claim ledger changed")
    if any(claims.get(name) is not True for name in TRUE_FLAGS):
        raise ValueError("a proved Stage-3G fact was weakened")
    if any(claims.get(name) is not False for name in FALSE_FLAGS):
        raise ValueError("an open Stage-3G claim was promoted")

    geometry = _mapping(certificate.get("tensor_geometry"), "Stage-3G geometry")
    coefficient = _mapping(
        certificate.get("coefficient_remainder"), "Stage-3G coefficient ledger"
    )
    residual = _mapping(certificate.get("resolvent_residual"), "Stage-3G residual")
    defects = _mapping(certificate.get("chart_defects"), "Stage-3G defects")
    green = _mapping(certificate.get("green_bootstrap"), "Stage-3G Green ledger")
    combined = _mapping(
        certificate.get("phase_combination_target"), "Stage-3G combined ledger"
    )
    transfer = _mapping(certificate.get("transfer_errors"), "Stage-3G transfer")
    gate = _mapping(certificate.get("transfer_gate"), "Stage-3G gate")
    _require_exact_keys(geometry, GEOMETRY_FIELDS, "Stage-3G geometry")
    _require_exact_keys(
        coefficient, COEFFICIENT_FIELDS, "Stage-3G coefficient ledger"
    )
    _require_exact_keys(residual, RESIDUAL_FIELDS, "Stage-3G residual")
    _require_exact_keys(defects, DEFECT_FIELDS, "Stage-3G defects")
    _require_exact_keys(green, GREEN_FIELDS, "Stage-3G Green ledger")
    _require_exact_keys(combined, COMBINED_FIELDS, "Stage-3G combined ledger")
    _require_exact_keys(transfer, TRANSFER_ERROR_FIELDS, "Stage-3G transfer")
    _require_exact_keys(gate, TRANSFER_GATE_FIELDS, "Stage-3G gate")

    pinned_period = _pinned_outer_guide_period(outer)
    expected_preflight = _directed_geometry_preflight(
        DirectedInterval.from_float(pinned_period, PRECISION_BITS),
        float(TAU_1) / DELTA_CELL_COUNT,
        pinned_period,
    )
    for name, expected_value in expected_preflight.items():
        if geometry.get(name) != expected_value:
            raise ValueError(
                f"the Stage-3G directed geometry preflight changed: {name}"
            )
    if (
        geometry.get("ordinary_rectangle_count") != ORDINARY_RECTANGLE_COUNT
        or geometry.get("terminal_extended_rectangle_count")
        != TERMINAL_EXTENDED_RECTANGLE_COUNT
        or geometry.get("tensor_patch_count") != 12320
    ):
        raise ValueError("the Stage-3G complete rectangle cover changed")
    if (
        geometry.get("delta_cell_count") != DELTA_CELL_COUNT
        or geometry.get("lag_cell_count") != LAG_CELL_COUNT
        or geometry.get("tau0_mesh_widths") != 16
        or geometry.get("tau1_mesh_widths") != 20
        or geometry.get("mesh_width_binary64_hex")
        != (float(TAU_1) / DELTA_CELL_COUNT).hex()
        or geometry.get("delta_degree") != DELTA_DEGREE
        or geometry.get("lag_degree") != LAG_DEGREE
        or geometry.get("coefficient_degree") != COEFFICIENT_DEGREE
        or geometry.get("subdivision_parts_per_axis") != SUBDIVISION_PARTS
        or geometry.get("fourier_cutoff") != FOURIER_CUTOFF
    ):
        raise ValueError("the Stage-3G mesh or polynomial ledger changed")
    if (
        geometry.get("period_strictly_between_47h_and_48h") is not True
        or geometry.get("guide_period_inside_directed_period_interval") is not True
    ):
        raise ValueError("a directed Stage-3G period gate was weakened")
    period_ratio = _mapping(
        geometry.get("period_mesh_ratio_interval"), "Stage-3G period/mesh ratio"
    )
    _require_exact_keys(
        period_ratio, frozenset({"lower", "upper"}), "Stage-3G period/mesh ratio"
    )
    if not (
        _decimal(period_ratio.get("lower"), "period/mesh lower") > Decimal(47)
        and _decimal(period_ratio.get("upper"), "period/mesh upper") < Decimal(48)
        and _decimal(
            geometry.get("period_minus_47h_lower"), "period minus 47h"
        )
        > 0
        and _decimal(
            geometry.get("48h_minus_period_lower"), "48h minus period"
        )
        > 0
    ):
        raise ValueError("the directed period/mesh inequalities failed")
    if (
        geometry.get("terminal_extension_strictly_between_zero_and_0p85")
        is not True
        or geometry.get("terminal_extension_within_solver_horizon") is not True
    ):
        raise ValueError("a directed terminal-extension gate was weakened")
    extension = _mapping(
        geometry.get("terminal_extension_length_interval"),
        "Stage-3G terminal extension",
    )
    _require_exact_keys(
        extension, frozenset({"lower", "upper"}), "Stage-3G terminal extension"
    )
    extension_lower = _decimal(extension.get("lower"), "extension lower")
    extension_upper = _decimal(extension.get("upper"), "extension upper")
    extension_limit = _decimal(
        geometry.get("terminal_extension_decimal_limit"), "extension limit"
    )
    solve_horizon = _decimal(
        geometry.get("terminal_extension_solver_horizon_lower"),
        "extension solve horizon",
    )
    solve_margin = _decimal(
        geometry.get("terminal_extension_solver_margin_lower"),
        "extension solve margin",
    )
    if not (
        extension_lower > 0
        and extension_lower <= extension_upper
        and extension_upper < extension_limit == Decimal("0.85")
        and extension_upper < solve_horizon
        and 0 < solve_margin <= solve_horizon - extension_upper
    ):
        raise ValueError("the directed 0<49h-T<0.85 solve cover failed")
    if (
        geometry.get("terminal_extension_solver_horizon_binary64_hex")
        != EXTENSION_SOLVE_HORIZON.hex()
        or geometry.get("terminal_extension_satisfies_same_retarded_equation")
        is not True
        or geometry.get(
            "physical_terminal_clipped_domain_subset_of_validated_rectangle"
        )
        is not True
    ):
        raise ValueError("the Stage-3G terminal extension ledger was weakened")

    if (
        coefficient.get("cached_coefficient_patch_count")
        != EXPECTED_COEFFICIENT_PATCH_COUNT
        or coefficient.get("current_tail_plus_taylor_effect_included") is not True
        or coefficient.get("delayed_tail_plus_taylor_effect_included") is not True
    ):
        raise ValueError("the Stage-3G coefficient remainder ledger weakened")
    if (
        residual.get("normalization") != "period times physical-lag residual"
        or residual.get("signed_matrix_residual_before_row_norm") is not True
        or residual.get("arb_precision_bits") != PRECISION_BITS
        or _decimal(
            residual.get("full_matrix_row_residual_upper"),
            "full matrix residual",
        )
        <= 0
    ):
        raise ValueError("the Stage-3G directed residual ledger changed")
    for name in (
        "voltage_terminal_row_polynomial_upper",
        "recovery_terminal_row_polynomial_upper",
        "voltage_terminal_row_tail_upper",
        "recovery_terminal_row_tail_upper",
        "voltage_terminal_row_total_upper",
        "recovery_terminal_row_total_upper",
    ):
        if _decimal(residual.get(name), name) < 0:
            raise ValueError("a Stage-3G residual component became negative")
    patch_centers = {str(value) for value in _patch_centers()}
    for name in (
        "voltage_terminal_row_maximizer",
        "recovery_terminal_row_maximizer",
    ):
        location = _mapping(residual.get(name), f"Stage-3G {name}")
        _require_exact_keys(location, MAXIMIZER_FIELDS, f"Stage-3G {name}")
        delta_cell = location.get("delta_cell")
        lag_cell = location.get("lag_cell")
        if (
            not isinstance(delta_cell, int)
            or not 0 <= delta_cell < DELTA_CELL_COUNT
            or not isinstance(lag_cell, int)
            or not 0 <= lag_cell < LAG_CELL_COUNT - delta_cell
            or location.get("delta_patch_center") not in patch_centers
            or location.get("lag_patch_center") not in patch_centers
            or location.get("terminal_extended_cell")
            is not (lag_cell >= LAG_CELL_COUNT - 2 - delta_cell)
        ):
            raise ValueError("a Stage-3G residual maximizer left the tensor cover")
    if defects.get("delta_interfaces_not_evolution_atoms") is not True:
        raise ValueError("the Stage-3G interface ledger changed")
    for name in DEFECT_FIELDS - {"delta_interfaces_not_evolution_atoms"}:
        if _decimal(defects.get(name), name) < 0:
            raise ValueError("a Stage-3G defect bound became negative")

    if (
        green.get("full_green_target") != FULL_GREEN_TARGET
        or green.get("full_boundary_target") != FULL_BOUNDARY_TARGET
        or green.get("strict_exact_arb_target_comparison") is not True
    ):
        raise ValueError("the Stage-3G exact Green target ledger changed")
    boundary_upper = _decimal(
        green.get("bootstrapped_exact_boundary_upper"), "exact boundary upper"
    )
    green_upper = _decimal(
        green.get("bootstrapped_exact_green_upper"), "exact Green upper"
    )
    boundary_closes = boundary_upper < Decimal(FULL_BOUNDARY_TARGET)
    green_closes = green_upper < Decimal(FULL_GREEN_TARGET)
    if (
        green.get("full_boundary_target_closes") is not boundary_closes
        or green.get("full_green_target_closes") is not green_closes
        or green.get("target_bootstrap_closes")
        is not (boundary_closes and green_closes)
        or not boundary_closes
        or not green_closes
    ):
        raise ValueError("a Stage-3G exact Green/boundary gate failed")
    for name in GREEN_FIELDS - {
        "full_green_target",
        "full_boundary_target",
        "strict_exact_arb_target_comparison",
        "full_green_target_closes",
        "full_boundary_target_closes",
        "target_bootstrap_closes",
    }:
        if _decimal(green.get(name), name) < 0:
            raise ValueError("a Stage-3G Green bound became negative")

    voltage_source = (
        "certificate.residual_closure_targets.rows.voltage."
        "required_combined_p_bernstein_residual_upper"
    )
    recovery_source = (
        "certificate.residual_closure_targets.rows.recovery."
        "required_combined_p_bernstein_residual_upper"
    )
    if (
        combined.get("voltage_target") != VOLTAGE_RESIDUAL_TARGET
        or combined.get("recovery_target") != RECOVERY_RESIDUAL_TARGET
        or combined.get("voltage_target_stage3f_field") != voltage_source
        or combined.get("recovery_target_stage3f_field") != recovery_source
        or combined.get("targets_exactly_ingressed_from_stage3f") is not True
        or combined.get("strict_exact_arb_target_comparison") is not True
    ):
        raise ValueError("the Stage-3G Stage-3F target ingress changed")
    voltage_upper = _decimal(
        combined.get("voltage_effective_residual_upper"),
        "voltage effective residual",
    )
    recovery_upper = _decimal(
        combined.get("recovery_effective_residual_upper"),
        "recovery effective residual",
    )
    voltage_closes = voltage_upper < Decimal(VOLTAGE_RESIDUAL_TARGET)
    recovery_closes = recovery_upper < Decimal(RECOVERY_RESIDUAL_TARGET)
    if (
        combined.get("voltage_target_closes") is not voltage_closes
        or combined.get("recovery_target_closes") is not recovery_closes
        or not voltage_closes
        or not recovery_closes
        or combined.get("direct_combined_row_uniform_size_still_open") is not True
        or combined.get("triangle_bound_uses_joint_S_and_terminal_phase_row")
        is not True
    ):
        raise ValueError("a Stage-3G exact joint residual gate failed")
    for name in COMBINED_FIELDS - {
        "voltage_target",
        "recovery_target",
        "voltage_target_stage3f_field",
        "recovery_target_stage3f_field",
        "targets_exactly_ingressed_from_stage3f",
        "strict_exact_arb_target_comparison",
        "voltage_target_closes",
        "recovery_target_closes",
        "direct_combined_row_uniform_size_still_open",
        "triangle_bound_uses_joint_S_and_terminal_phase_row",
    }:
        if _decimal(combined.get(name), name) < 0:
            raise ValueError("a Stage-3G combined-row bound became negative")

    if (
        gate.get("complete_directed_tensor_geometry_validated") is not True
        or gate.get("full_advanced_green_target_validated") is not green_closes
        or gate.get("full_advanced_boundary_target_validated")
        is not boundary_closes
        or gate.get("joint_augmented_phase_residual_targets_validated")
        is not (voltage_closes and recovery_closes)
        or gate.get("strict_combined_row_uniform_sizes_validated") is not False
        or gate.get("linear_return_gate_evaluated") is not False
        or gate.get("arbitrary_c0_linear_contraction_closes") is not False
        or gate.get("nonlinear_outer_attraction_closes") is not False
    ):
        raise ValueError("the Stage-3G transfer gate ledger is inconsistent")
    stage3f_transfer = _mapping(
        stage3f_certificate.get("transfer_errors"), "Stage-3F transfer errors"
    )
    if (
        transfer.get("E_voltage") is not None
        or transfer.get("E_recovery") is not None
        or transfer.get("E_phase") != stage3f_transfer.get("E_phase")
    ):
        raise ValueError("a Stage-3G transfer error was invented or changed")
    if certificate.get("conclusion") != CONCLUSION:
        raise ValueError("the Stage-3G conclusion changed")
    expected = json.loads(
        json.dumps(
            asdict(build_outer_resolvent_stage3g_tensor(repository)),
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        )
    )
    if certificate != expected:
        raise ValueError("the Stage-3G certificate differs from replay")


__all__ = [
    "DEFAULT_COMMAND",
    "FALSE_FLAGS",
    "NOTE_RELATIVE_PATH",
    "RESULT_RELATIVE_PATH",
    "SOURCE_MANIFEST",
    "TRUE_FLAGS",
    "build_outer_resolvent_stage3g_tensor",
    "build_outer_resolvent_stage3g_tensor_result",
    "canonical_sha256",
    "validate_outer_resolvent_stage3g_tensor_result",
]
