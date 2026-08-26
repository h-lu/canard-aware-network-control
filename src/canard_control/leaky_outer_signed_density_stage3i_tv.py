"""Stage-3I directed continuous signed-density total variation.

This stage closes the last linear gap left by Stage 3H.  On every
``(delta, theta)`` cell it constructs the scalar history density

    d_delta(theta) = sum_j p_delta(theta+tau_j) B_j(theta+tau_j) e_v

with both delayed injection branches and the phase subtraction still inside
one signed Arb interval.  Only then is an absolute value taken and integrated
over the history cell.  Resolvent component ranges are obtained from the
exact-dyadic Stage-3G Chebyshev candidates by 192-bit tensor Bernstein
restriction.  Any lag seam intersecting a cell is covered by the union of
all corresponding one-sided candidate charts.

The resulting continuous *candidate* row norm is compared directly with the
Stage-2 directed discrete shadow.  Candidate-to-guide residual/atom costs
from Stage 3G and guide-to-exact-orbit coefficient/phase costs from Stage 3F
are then each added exactly once.  This is the full arbitrary-C0 linear
return gate on the voltage-history/recovery-scalar reduced space; nonlinear
attraction and pulse capture remain separate claims.
"""

from __future__ import annotations

from copy import deepcopy
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

from canard_control.directed_interval import DirectedInterval
from canard_control.leaky_outer_combined_row_stage3h_size import (
    RESULT_RELATIVE_PATH as STAGE3H_RESULT_RELATIVE_PATH,
    _series_real_box_at_precision,
)
from canard_control.leaky_outer_high_resolution import (
    RESULT_RELATIVE_PATH as OUTER_RESULT_RELATIVE_PATH,
    validate_outer_high_resolution_artifact,
)
from canard_control.leaky_outer_resolvent_stage3g_tensor import (
    DELTA_DEGREE,
    LAG_DEGREE,
    PRECISION_BITS,
    _TensorGuide,
    _arb_interval,
    _chebyshev_to_bernstein_matrix,
    _exact_arb_float,
    _mapping,
    _matrix_from_float,
)
from canard_control.leaky_outer_signed_kernel_stage2 import (
    RESULT_RELATIVE_PATH as STAGE2_RESULT_RELATIVE_PATH,
)
from canard_control.leaky_outer_signed_row_stage3f_adjoint import (
    RESULT_RELATIVE_PATH as STAGE3F_RESULT_RELATIVE_PATH,
)
from canard_control.leaky_periodic_validation import _build_leaky_base_sequences
from canard_control.leaky_pulse_separator_candidate import TAU_0, TAU_1


SCHEMA_ID = "leaky-outer-signed-density-stage3i-tv-v2"
MODEL_ID = "autonomous-leaky-recovery-two-delay-fhn-bistable-proposal"
BRANCH = "outer_pulse"
SOURCE_RELATIVE_PATH = (
    "src/canard_control/leaky_outer_signed_density_stage3i_tv.py"
)
GENERATOR_RELATIVE_PATH = "experiments/leaky_outer_signed_density_stage3i_tv.py"
RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_outer_signed_density_stage3i_tv.json"
)
NOTE_RELATIVE_PATH = "docs/leaky-outer-signed-density-stage3i-tv.md"
TEST_RELATIVE_PATH = "tests/test_leaky_outer_signed_density_stage3i_tv.py"
SOURCE_MANIFEST = (
    SOURCE_RELATIVE_PATH,
    GENERATOR_RELATIVE_PATH,
    NOTE_RELATIVE_PATH,
    TEST_RELATIVE_PATH,
    "src/canard_control/directed_interval.py",
    "src/canard_control/leaky_outer_combined_row_stage3h_size.py",
    "src/canard_control/leaky_outer_high_resolution.py",
    "src/canard_control/leaky_outer_resolvent_stage3g_tensor.py",
    "src/canard_control/leaky_outer_signed_kernel_stage2.py",
    "src/canard_control/leaky_outer_signed_row_stage3f_adjoint.py",
    "src/canard_control/leaky_periodic_validation.py",
    "src/canard_control/leaky_pulse_separator_candidate.py",
)
DEFAULT_COMMAND = (
    "OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONPATH=build/testdeps:src "
    "/usr/bin/python3 experiments/leaky_outer_signed_density_stage3i_tv.py"
)
ARITHMETIC_SCOPE = (
    "160-by-160 event-aware method-of-steps cell cover; exact-dyadic "
    "Stage-3G candidate coefficients; exact rational local "
    "Chebyshev-to-Bernstein restriction; 192-bit Arb one-sided chart unions, "
    "Fourier boxes, signed cross-injection sums, absolute cell integration "
    "and transfer ledger"
)
ROW_SCOPE = (
    "binary center candidate continuous reduced-history rows followed by "
    "once-only candidate-to-guide and guide-to-exact-orbit transfer costs"
)
PREFINAL_ROW_SCOPE = (
    "binary center candidate continuous rows followed by once-only "
    "candidate-to-guide and guide-to-exact-orbit transfer costs"
)
CENTER_EXCESS_SEMANTICS = (
    "Q_candidate_continuous <= Q_stage2_shadow + E_center, where E_center "
    "is max(0,Q_candidate_upper-Q_stage2_shadow_upper), not an "
    "operator-difference norm"
)
TOTAL_ROW_BUDGET_SEMANTICS = (
    "Q_exact_row <= Q_stage2_shadow + E_row; total E_row is a row-budget "
    "slack, not ||L_exact-L_shadow||; only its named Stage-3F/3G transfer "
    "components bound operator perturbations"
)
CONCLUSION_CLOSED = (
    "the event-aware continuous signed-density cell integral strictly closes "
    "the candidate-row excess reserve and, together with the Stage-3G/3H and "
    "exact-orbit budgets, proves arbitrary-C0 linear return contraction; "
    "nonlinear attraction, capture and physical onset remain separate"
)
CONCLUSION_OPEN = (
    "the event-aware continuous signed-density cell integral does not yet "
    "close the candidate-row excess reserve; the computed E_voltage and "
    "E_recovery bounds are validated but the arbitrary-C0 contraction gate "
    "does not close; nonlinear attraction, capture and physical onset remain "
    "separate"
)
CONCLUSION_TRANSFER_OPEN = (
    "the event-aware continuous signed-density cell integral closes the "
    "candidate-row excess reserve and the exact row budgets are validated, "
    "but the resulting arbitrary-C0 linear return bound is not "
    "strictly below one; nonlinear attraction, capture and physical onset "
    "remain separate"
)
CONCLUSION_TARGET_OPEN_CONTRACTION_CLOSED = (
    "the event-aware continuous signed-density cell integral misses the "
    "auxiliary 0.01 candidate-row excess target, but the actual exact "
    "reduced-history row budgets are both strictly below one and prove "
    "arbitrary-C0 reduced-history linear return contraction; nonlinear "
    "phase charts, attraction, capture and physical onset remain separate"
)

STAGE3H_RESULT_SHA256 = (
    "c0c5b854236f8403dacbb0037c5c409ad5f980364571bdf60fa9981a2e287408"
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
STAGE3H_SCHEMA_ID = "leaky-outer-combined-row-stage3h-size-v2"
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
PINNED_OMP_NUM_THREADS = "1"
SUBCELLS_PER_MESH_CELL = 8
MESH_CELL_COUNT = 20
CENTER_TRANSFER_TARGET = "0.01"
PREFINAL_RESULT_SHA256 = (
    "f189c75887465823898d100e545e75797d78b6b798b2c6371def767a47619383"
)
LAG_SEAM_ENDPOINT_CONVENTION = (
    "TV cells use a lower-open/upper-closed endpoint convention: an integer "
    "lower lag endpoint uses its right chart, while an integer upper lag "
    "endpoint unions the adjacent left and right charts; a physical domain "
    "endpoint uses its sole incident chart"
)

BASE_TRUE_FLAGS = (
    "stage3h_strict_row_size_parent_digest_validated",
    "stage3h_parent_source_manifest_validated",
    "stage3g_residual_green_parent_digest_validated",
    "stage3g_parent_source_manifest_validated",
    "stage3f_exact_defect_parent_digest_validated",
    "stage2_discrete_shadow_parent_digest_validated",
    "all_25600_delta_history_rectangles_covered",
    "all_lag_chart_seams_covered_by_one_sided_unions",
    "candidate_resolvent_ranges_tensor_bernstein_192_bit",
    "phase_subtraction_precedes_density_absolute_value",
    "both_history_injections_summed_before_absolute_value",
    "recovery_scalar_atom_kept_separate_from_density",
    "candidate_to_guide_and_guide_to_exact_costs_counted_once",
    "candidate_row_excess_is_one_sided_norm_slack",
    "strict_exact_arb_center_transfer_target_comparison",
    "continuous_signed_density_total_variation_validated",
    "voltage_exact_row_budget_validated",
    "recovery_exact_row_budget_validated",
    "linear_return_gate_evaluated",
)
CLOSURE_FLAGS = (
    "continuous_center_signed_density_TV_reserve_validated",
    "arbitrary_c0_linear_return_contraction_validated",
)
FALSE_FLAGS = (
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
        "mpfr",
        "mpfr_directed_precision_bits",
        "python_flint",
        "arb_precision_bits",
        "openblas_num_threads",
        "omp_num_threads",
    }
)
GEOMETRY_FIELDS = frozenset(
    {
        "mesh_cell_count_per_axis",
        "subcells_per_mesh_cell",
        "delta_subinterval_count",
        "history_subinterval_count",
        "delta_history_rectangle_count",
        "seam_union_rectangle_count",
        "maximum_lag_chart_multiplicity",
        "recovery_history_subinterval_count",
        "recovery_seam_subinterval_count",
        "point_samples_used_as_proof",
        "period_binary64_hex",
        "mesh_width_binary64_hex",
        "delay_mesh_widths",
        "delay_binary64_hex",
        "requested_lag_interval_count",
        "all_requested_lag_intervals_in_domain",
        "lag_domain_lower_mesh",
        "lag_domain_upper_rule",
        "lag_seam_endpoint_convention",
    }
)
CANDIDATE_FIELDS = frozenset(
    {
        "voltage_history_density_TV_upper",
        "voltage_recovery_atom_upper",
        "voltage_total_row_upper",
        "voltage_total_maximizer",
        "recovery_history_density_TV_upper",
        "recovery_recovery_atom_upper",
        "recovery_total_row_upper",
        "both_injection_branches_summed_before_absolute_value",
        "phase_subtraction_inside_each_density_interval",
    }
)
VOLTAGE_MAXIMIZER_FIELDS = frozenset(
    {"delta_cell", "delta_subcell", "atom_lag_chart_count"}
)
LEDGER_FIELDS = frozenset(
    {
        "candidate_row_excess_target",
        "strict_exact_arb_target_comparison",
        "candidate_row_excess_semantics",
        "total_row_budget_semantics",
        "voltage_candidate_row_excess_over_shadow_upper",
        "recovery_candidate_row_excess_over_shadow_upper",
        "candidate_row_excess_target_closes",
        "rows",
        "arbitrary_c0_linear_contraction_closes",
    }
)
LEDGER_ROW_FIELDS = frozenset(
    {
        "candidate_row_excess_over_stage2_shadow_upper",
        "direct_delayed_coefficient_transfer_upper",
        "orbit_coefficient_transfer_upper",
        "phase_ratio_boundary_transfer_upper",
        "candidate_residual_and_atom_transfer_upper",
        "E_row_upper",
        "stage2_shadow_plus_E_upper",
        "strictly_below_one",
    }
)
TRANSFER_ERROR_FIELDS = frozenset({"E_voltage", "E_recovery", "E_phase"})
TRANSFER_GATE_FIELDS = frozenset(
    {
        "strict_combined_row_uniform_sizes_validated",
        "continuous_center_signed_density_TV_reserve_validated",
        "continuous_signed_density_total_variation_validated",
        "linear_return_gate_evaluated",
        "arbitrary_c0_linear_contraction_closes",
        "nonlinear_outer_attraction_closes",
    }
)


def _conclusion_for_outcome(
    center_target_closes: bool, contraction_closes: bool
) -> str:
    if center_target_closes and contraction_closes:
        return CONCLUSION_CLOSED
    if center_target_closes:
        return CONCLUSION_TRANSFER_OPEN
    if contraction_closes:
        return CONCLUSION_TARGET_OPEN_CONTRACTION_CLOSED
    return CONCLUSION_OPEN


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
        "mpfr": gmpy2.mpfr_version(),
        "mpfr_directed_precision_bits": PRECISION_BITS,
        "python_flint": __import__("flint").__version__,
        "arb_precision_bits": PRECISION_BITS,
        "openblas_num_threads": os.environ.get("OPENBLAS_NUM_THREADS"),
        "omp_num_threads": os.environ.get("OMP_NUM_THREADS"),
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
    *registries: tuple[str, Sequence[str]]
) -> None:
    seen: set[str] = set()
    for label, flags in registries:
        if len(flags) != len(set(flags)):
            raise ValueError(f"the Stage-3I {label} registry contains duplicates")
        overlap = seen & set(flags)
        if overlap:
            raise ValueError(
                f"the Stage-3I flag registries overlap: {sorted(overlap)}"
            )
        seen.update(flags)


def _load_parent(repository: Path, relative: str, expected: str) -> Mapping[str, Any]:
    path = repository / relative
    if _sha256_path(path) != expected:
        raise ValueError(f"a Stage-3I parent changed: {relative}")
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
    if not value.is_finite():
        raise ArithmeticError("a Stage-3I Arb enclosure is not finite")
    answer = math.nextafter(float(value.abs_upper()), math.inf)
    if not math.isfinite(answer):
        raise ArithmeticError("a Stage-3I serialized upper bound is not finite")
    return answer


def _upper_record(value: arb) -> str:
    return format(_arb_upper_float(value), ".17g")


def _floor_fraction(value: Fraction) -> int:
    return value.numerator // value.denominator


def _arb_fraction(value: Fraction) -> arb:
    return arb(value.numerator) / value.denominator


def _require_finite_arb(value: arb, name: str) -> arb:
    if not value.is_finite():
        raise ArithmeticError(f"the Stage-3I {name} enclosure is not finite")
    return value


def _local_coordinate(
    subcell: int,
) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    if not 0 <= subcell < SUBCELLS_PER_MESH_CELL:
        raise ValueError("a Stage-3I local subcell index left the mesh")
    lower = Fraction(-1) + Fraction(
        2 * subcell, SUBCELLS_PER_MESH_CELL
    )
    upper = Fraction(-1) + Fraction(
        2 * (subcell + 1), SUBCELLS_PER_MESH_CELL
    )
    return lower, upper, (lower + upper) / 2, (upper - lower) / 2


def _total_mesh_interval(cell: int, subcell: int) -> tuple[Fraction, Fraction]:
    if not 0 <= cell < MESH_CELL_COUNT:
        raise ValueError("a Stage-3I mesh-cell index left the mesh")
    lower, upper, _, _ = _local_coordinate(subcell)
    return (
        Fraction(cell) + Fraction(1, 2) + lower / 2,
        Fraction(cell) + Fraction(1, 2) + upper / 2,
    )


def _active_delays(history_cell: int) -> tuple[tuple[int, int], ...]:
    if not 0 <= history_cell < MESH_CELL_COUNT:
        raise ValueError("a Stage-3I history cell left the delay support")
    return ((0, 16), (1, 20)) if history_cell < 16 else ((1, 20),)


def _lag_chart_indices(
    delta_cell: int,
    lag_mesh_lower: Fraction,
    lag_mesh_upper: Fraction,
) -> tuple[int, ...]:
    """Return every physical chart under the documented seam convention."""

    if not 0 <= delta_cell < MESH_CELL_COUNT:
        raise ValueError("a Stage-3I delta cell left the resolvent cover")
    if lag_mesh_lower > lag_mesh_upper:
        raise ValueError("a Stage-3I requested lag interval was reversed")
    maximum_lag_cell = 47 - delta_cell
    domain_upper = Fraction(maximum_lag_cell + 1)
    if lag_mesh_lower < 0 or lag_mesh_upper > domain_upper:
        raise ValueError(
            "a Stage-3I requested lag interval left the Stage-3G domain"
        )
    first = _floor_fraction(lag_mesh_lower)
    final = _floor_fraction(lag_mesh_upper)
    # At the physical upper endpoint there is only the incident left chart.
    if first > maximum_lag_cell:
        first = maximum_lag_cell
    if final > maximum_lag_cell:
        final = maximum_lag_cell
    indices = tuple(range(first, final + 1))
    if not indices:
        raise ArithmeticError("a Stage-3I lag interval lost every chart")
    return indices


def _stage3i_geometry_preflight(
    period: float,
    h: float,
    taus: tuple[float, float] = (float(TAU_0), float(TAU_1)),
) -> dict[str, Any]:
    """Check every requested lag interval before the Bernstein sweep."""

    if not math.isfinite(period) or not math.isfinite(h) or h <= 0:
        raise ValueError("the Stage-3I binary guide geometry is invalid")
    if (
        len(taus) != 2
        or Fraction.from_float(float(taus[0])) != 16 * Fraction.from_float(h)
        or Fraction.from_float(float(taus[1])) != 20 * Fraction.from_float(h)
        or float(taus[0]).hex() != float(TAU_0).hex()
        or float(taus[1]).hex() != float(TAU_1).hex()
    ):
        raise ValueError("the Stage-3I 16h/20h delay geometry changed")
    period_mesh = Fraction.from_float(period) / Fraction.from_float(h)
    total_rectangles = 0
    seam_rectangles = 0
    maximum_multiplicity = 1
    requested_intervals = 4  # Four S(0,T) scalar-component point requests.
    maximum_atom_chart_count = 1
    for delta_cell in range(MESH_CELL_COUNT):
        for delta_subcell in range(SUBCELLS_PER_MESH_CELL):
            delta_lower, delta_upper = _total_mesh_interval(
                delta_cell, delta_subcell
            )
            for history_cell in range(MESH_CELL_COUNT):
                for history_subcell in range(SUBCELLS_PER_MESH_CELL):
                    history_lower, history_upper = _total_mesh_interval(
                        history_cell, history_subcell
                    )
                    multiplicity = 1
                    for _, delay_mesh in _active_delays(history_cell):
                        current = _lag_chart_indices(
                            delta_cell,
                            period_mesh
                            - delta_upper
                            - delay_mesh
                            + history_lower,
                            period_mesh
                            - delta_lower
                            - delay_mesh
                            + history_upper,
                        )
                        terminal = _lag_chart_indices(
                            0,
                            period_mesh - delay_mesh + history_lower,
                            period_mesh - delay_mesh + history_upper,
                        )
                        requested_intervals += 2
                        multiplicity *= len(current) * len(terminal)
                    total_rectangles += 1
                    maximum_multiplicity = max(
                        maximum_multiplicity, multiplicity
                    )
                    if multiplicity > 1:
                        seam_rectangles += 1
            atom = _lag_chart_indices(
                delta_cell,
                period_mesh - delta_upper,
                period_mesh - delta_lower,
            )
            requested_intervals += 1
            maximum_atom_chart_count = max(maximum_atom_chart_count, len(atom))
            maximum_multiplicity = max(maximum_multiplicity, len(atom))

    recovery_seams = 0
    for history_cell in range(MESH_CELL_COUNT):
        for history_subcell in range(SUBCELLS_PER_MESH_CELL):
            history_lower, history_upper = _total_mesh_interval(
                history_cell, history_subcell
            )
            multiplicity = 1
            for _, delay_mesh in _active_delays(history_cell):
                terminal = _lag_chart_indices(
                    0,
                    period_mesh - delay_mesh + history_lower,
                    period_mesh - delay_mesh + history_upper,
                )
                # The recovery row requests both the recovery and voltage
                # component on the same physical terminal interval.
                requested_intervals += 2
                multiplicity *= len(terminal) ** 2
            maximum_multiplicity = max(maximum_multiplicity, multiplicity)
            if multiplicity > 1:
                recovery_seams += 1

    expected_rectangles = (
        MESH_CELL_COUNT * SUBCELLS_PER_MESH_CELL
    ) ** 2
    if total_rectangles != expected_rectangles:
        raise AssertionError("the Stage-3I zero-cost rectangle count changed")
    return {
        "mesh_cell_count_per_axis": MESH_CELL_COUNT,
        "subcells_per_mesh_cell": SUBCELLS_PER_MESH_CELL,
        "delta_subinterval_count": MESH_CELL_COUNT * SUBCELLS_PER_MESH_CELL,
        "history_subinterval_count": MESH_CELL_COUNT * SUBCELLS_PER_MESH_CELL,
        "delta_history_rectangle_count": total_rectangles,
        "seam_union_rectangle_count": seam_rectangles,
        "maximum_lag_chart_multiplicity": maximum_multiplicity,
        "recovery_history_subinterval_count": (
            MESH_CELL_COUNT * SUBCELLS_PER_MESH_CELL
        ),
        "recovery_seam_subinterval_count": recovery_seams,
        "point_samples_used_as_proof": False,
        "period_binary64_hex": period.hex(),
        "mesh_width_binary64_hex": h.hex(),
        "delay_mesh_widths": [16, 20],
        "delay_binary64_hex": [float(value).hex() for value in taus],
        "requested_lag_interval_count": requested_intervals,
        "all_requested_lag_intervals_in_domain": True,
        "lag_domain_lower_mesh": "0",
        "lag_domain_upper_rule": "48-delta_cell",
        "lag_seam_endpoint_convention": LAG_SEAM_ENDPOINT_CONVENTION,
    }


def _fraction_interval(lower: Fraction, upper: Fraction) -> DirectedInterval:
    if lower > upper:
        raise ValueError("an interval endpoint was reversed")
    return DirectedInterval.from_bounds(
        gmpy2.mpq(lower.numerator, lower.denominator),
        gmpy2.mpq(upper.numerator, upper.denominator),
        PRECISION_BITS,
    )


def _arb_hull_matrix(value: arb_mat) -> arb:
    answer = value[0, 0]
    for row in range(value.nrows()):
        for column in range(value.ncols()):
            answer = answer.union(value[row, column])
    return answer


def _one_sided_candidate_excess_upper(left: arb, right: arb) -> arb:
    """Return slack E with candidate upper <= shadow upper + E."""

    difference = left - right
    if difference.upper() <= 0:
        return arb(0)
    return difference.upper()


def _candidate_excess_records(
    candidate: Mapping[str, Any], stage2_certificate: Mapping[str, Any]
) -> dict[str, str]:
    arb_ctx.prec = PRECISION_BITS
    arb_ctx.threads = 1
    records: dict[str, str] = {}
    for row_id in ("voltage", "recovery"):
        candidate_upper = arb(str(candidate[f"{row_id}_total_row_upper"]))
        shadow_upper = arb(
            str(stage2_certificate[f"directed_{row_id}_shadow_norm_upper"])
        )
        records[row_id] = _upper_record(
            _one_sided_candidate_excess_upper(candidate_upper, shadow_upper)
        )
    return records


@dataclass(frozen=True)
class OuterSignedDensityStage3ITV:
    schema_id: str
    model_id: str
    branch: str
    arithmetic_scope: str
    precision_bits: int
    row_scope: str
    parent_result_sha256: dict[str, str]
    cell_geometry: dict[str, Any]
    candidate_continuous_rows: dict[str, Any]
    transfer_ledger: dict[str, Any]
    transfer_errors: dict[str, str | None]
    transfer_gate: dict[str, bool]
    claim_status: dict[str, bool]
    conclusion: str


def _transfer_rows_from_excess_records(
    excess_records: Mapping[str, str],
    stage3h_certificate: Mapping[str, Any],
    stage3g_certificate: Mapping[str, Any],
    stage3f_certificate: Mapping[str, Any],
    stage2_certificate: Mapping[str, Any],
) -> tuple[dict[str, Any], dict[str, arb], dict[str, arb]]:
    """Recompute the exact-orbit transfer ledger from serialized inputs."""

    arb_ctx.prec = PRECISION_BITS
    arb_ctx.threads = 1

    sizes = _mapping(
        stage3h_certificate.get("combined_row_size"), "Stage-3H row sizes"
    )
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
    ledger: dict[str, Any] = {}
    final_errors: dict[str, arb] = {}
    final_totals: dict[str, arb] = {}
    for row_id in ("voltage", "recovery"):
        center_excess = arb(str(excess_records[row_id]))
        uniform = arb(str(sizes[f"{row_id}_combined_p_uniform_upper"]))
        component = arb(
            str(sizes[f"{row_id}_combined_p_voltage_component_upper"])
        )
        shadow = arb(
            str(stage2_certificate[f"directed_{row_id}_shadow_norm_upper"])
        )
        orbit_residual = component * rank_one + uniform * full_period
        direct_cost = delay_sum * component * delayed_variation
        orbit_cost = lift * exact_green * orbit_residual
        ratio_cost = lift * exact_boundary * arb(
            str(defects[f"{row_id}_phase_ratio_transfer_error_upper"])
        )
        residual_cost = lift * (
            exact_green
            * arb(str(combined[f"{row_id}_joint_augmented_residual_upper"]))
            + exact_boundary * arb(str(combined[f"{row_id}_joint_atom_upper"]))
        )
        transfer = (
            center_excess
            + direct_cost
            + orbit_cost
            + ratio_cost
            + residual_cost
        )
        total = shadow + transfer
        final_errors[row_id] = transfer
        final_totals[row_id] = total
        transfer_record = _upper_record(transfer)
        total_record = _upper_record(total)
        ledger[row_id] = {
            "candidate_row_excess_over_stage2_shadow_upper": str(
                excess_records[row_id]
            ),
            "direct_delayed_coefficient_transfer_upper": _upper_record(direct_cost),
            "orbit_coefficient_transfer_upper": _upper_record(orbit_cost),
            "phase_ratio_boundary_transfer_upper": _upper_record(ratio_cost),
            "candidate_residual_and_atom_transfer_upper": _upper_record(
                residual_cost
            ),
            "E_row_upper": transfer_record,
            "stage2_shadow_plus_E_upper": total_record,
            "strictly_below_one": _decimal(
                total_record, f"{row_id} serialized exact-orbit total"
            )
            < 1,
        }
    return ledger, final_errors, final_totals


class _CandidateRangeGuide:
    def __init__(self, guide: _TensorGuide):
        self.guide = guide
        self.period_mesh = Fraction.from_float(guide.period) / Fraction.from_float(
            guide.h
        )
        self.component_cache: dict[
            tuple[int, int, int, int, Fraction, Fraction, Fraction, Fraction], arb
        ] = {}

    def component_range(
        self,
        delta_cell: int,
        lag_cell: int,
        row: int,
        column: int,
        x_center: Fraction,
        x_scale: Fraction,
        z_center: Fraction,
        z_scale: Fraction,
    ) -> arb:
        key = (
            delta_cell,
            lag_cell,
            row,
            column,
            x_center,
            x_scale,
            z_center,
            z_scale,
        )
        if key in self.component_cache:
            return self.component_cache[key]
        coefficients = self.guide.coefficients(delta_cell, lag_cell)
        delta_transform = _chebyshev_to_bernstein_matrix(
            DELTA_DEGREE, x_center, x_scale
        )
        lag_transform = _chebyshev_to_bernstein_matrix(
            LAG_DEGREE, z_center, z_scale
        )
        patch = (
            delta_transform
            * _matrix_from_float(coefficients[:, :, row, column])
            * lag_transform.transpose()
        )
        answer = _require_finite_arb(
            _arb_hull_matrix(patch), "candidate component range"
        )
        self.component_cache[key] = answer
        return answer

    def piecewise_range(
        self,
        *,
        delta_cell: int,
        row: int,
        column: int,
        x_center: Fraction,
        x_scale: Fraction,
        lag_mesh_lower: Fraction,
        lag_mesh_upper: Fraction,
    ) -> tuple[arb, int]:
        answer: arb | None = None
        chart_count = 0
        for lag_cell in _lag_chart_indices(
            delta_cell, lag_mesh_lower, lag_mesh_upper
        ):
            lower = max(lag_mesh_lower, Fraction(lag_cell))
            upper = min(lag_mesh_upper, Fraction(lag_cell + 1))
            if lower > upper:
                continue
            z_lower = 2 * (lower - Fraction(2 * lag_cell + 1, 2))
            z_upper = 2 * (upper - Fraction(2 * lag_cell + 1, 2))
            local = self.component_range(
                delta_cell,
                lag_cell,
                row,
                column,
                x_center,
                x_scale,
                (z_lower + z_upper) / 2,
                (z_upper - z_lower) / 2,
            )
            answer = local if answer is None else answer.union(local)
            chart_count += 1
        if answer is None:
            raise ArithmeticError("a Stage-3I physical lag range lost its chart")
        return _require_finite_arb(answer, "piecewise candidate range"), chart_count

    def terminal_range(
        self,
        *,
        row: int,
        column: int,
        lag_mesh_lower: Fraction,
        lag_mesh_upper: Fraction,
    ) -> tuple[arb, int]:
        return self.piecewise_range(
            delta_cell=0,
            row=row,
            column=column,
            x_center=Fraction(-1),
            x_scale=Fraction(0),
            lag_mesh_lower=lag_mesh_lower,
            lag_mesh_upper=lag_mesh_upper,
        )


def _build_density_certificate(
    guide: _TensorGuide,
    base: Any,
    stage3h: Mapping[str, Any],
    stage3g: Mapping[str, Any],
    stage3f: Mapping[str, Any],
    stage2: Mapping[str, Any],
) -> dict[str, Any]:
    ranges = _CandidateRangeGuide(guide)
    subdivisions = SUBCELLS_PER_MESH_CELL
    geometry_preflight = _stage3i_geometry_preflight(
        guide.period, guide.h, tuple(float(value) for value in guide.taus)
    )
    h_arb = _exact_arb_float(guide.h)
    h_interval = DirectedInterval.from_float(guide.h, PRECISION_BITS)
    period = base.period
    zero = DirectedInterval.from_decimal(0, PRECISION_BITS)
    qv0 = _series_real_box_at_precision(base.phase_voltage, zero)
    qw0 = _series_real_box_at_precision(base.phase_recovery, zero)
    alpha_denominator = _require_finite_arb(
        _arb_interval(qv0), "phase-voltage denominator"
    )
    if not alpha_denominator.lower() > 0:
        raise ArithmeticError(
            "the Stage-3I phase-voltage denominator is not strictly positive"
        )
    beta = _require_finite_arb(
        _arb_interval(qw0) / alpha_denominator, "recovery phase ratio"
    )

    series_cache: dict[tuple[int, Fraction, Fraction], arb] = {}

    def series_range(sequence: Mapping[int, Any], time_lower: Fraction, time_upper: Fraction) -> arb:
        key = (id(sequence), time_lower, time_upper)
        if key in series_cache:
            return series_cache[key]
        physical = h_interval * _fraction_interval(time_lower, time_upper)
        phase = physical / period
        answer = _require_finite_arb(
            _arb_interval(_series_real_box_at_precision(sequence, phase)),
            "Fourier series range",
        )
        series_cache[key] = answer
        return answer

    # S(0,T) is common to every scalar atom.
    terminal_point: dict[tuple[int, int], arb] = {}
    for row in range(2):
        for column in range(2):
            terminal_point[(row, column)] = ranges.terminal_range(
                row=row,
                column=column,
                lag_mesh_lower=ranges.period_mesh,
                lag_mesh_upper=ranges.period_mesh,
            )[0]

    maximum_voltage = arb(0)
    maximum_voltage_density = arb(0)
    maximum_voltage_atom = arb(0)
    maximum_voltage_location: dict[str, int] | None = None
    total_rectangles = 0
    maximum_lag_chart_multiplicity = 0
    seam_union_rectangle_count = 0
    requested_lag_intervals = 4

    for delta_cell in range(MESH_CELL_COUNT):
        for delta_subcell in range(subdivisions):
            delta_lower, delta_upper = _total_mesh_interval(
                delta_cell, delta_subcell
            )
            _, _, x_center, x_scale = _local_coordinate(delta_subcell)
            delta_physical = h_interval * _fraction_interval(
                delta_lower, delta_upper
            )
            alpha = _require_finite_arb(
                _arb_interval(
                    _series_real_box_at_precision(
                        base.phase_voltage, (period - delta_physical) / period
                    )
                )
                / alpha_denominator,
                "voltage phase ratio",
            )
            density_mass = arb(0)
            for history_cell in range(MESH_CELL_COUNT):
                active = _active_delays(history_cell)
                for history_subcell in range(subdivisions):
                    history_lower, history_upper = _total_mesh_interval(
                        history_cell, history_subcell
                    )
                    current_sum = arb(0)
                    terminal_sum = arb(0)
                    local_multiplicity = 1
                    for delay_index, delay_mesh in active:
                        lag_lower = (
                            ranges.period_mesh
                            - delta_upper
                            - delay_mesh
                            + history_lower
                        )
                        lag_upper = (
                            ranges.period_mesh
                            - delta_lower
                            - delay_mesh
                            + history_upper
                        )
                        current, current_charts = ranges.piecewise_range(
                            delta_cell=delta_cell,
                            row=0,
                            column=0,
                            x_center=x_center,
                            x_scale=x_scale,
                            lag_mesh_lower=lag_lower,
                            lag_mesh_upper=lag_upper,
                        )
                        terminal_lower = (
                            ranges.period_mesh - delay_mesh + history_lower
                        )
                        terminal_upper = (
                            ranges.period_mesh - delay_mesh + history_upper
                        )
                        terminal, terminal_charts = ranges.terminal_range(
                            row=0,
                            column=0,
                            lag_mesh_lower=terminal_lower,
                            lag_mesh_upper=terminal_upper,
                        )
                        requested_lag_intervals += 2
                        coefficient = series_range(
                            base.delayed_coefficients[delay_index],
                            Fraction(delay_mesh) - history_upper,
                            Fraction(delay_mesh) - history_lower,
                        )
                        current_sum += current * coefficient
                        terminal_sum += terminal * coefficient
                        local_multiplicity *= current_charts * terminal_charts
                    density = _require_finite_arb(
                        current_sum - alpha * terminal_sum,
                        "voltage signed history density",
                    )
                    history_width = h_arb * _arb_fraction(
                        history_upper - history_lower
                    )
                    density_mass += density.abs_upper() * history_width
                    total_rectangles += 1
                    maximum_lag_chart_multiplicity = max(
                        maximum_lag_chart_multiplicity, local_multiplicity
                    )
                    if local_multiplicity > 1:
                        seam_union_rectangle_count += 1

            lag_lower = ranges.period_mesh - delta_upper
            lag_upper = ranges.period_mesh - delta_lower
            current_atom, atom_charts = ranges.piecewise_range(
                delta_cell=delta_cell,
                row=0,
                column=1,
                x_center=x_center,
                x_scale=x_scale,
                lag_mesh_lower=lag_lower,
                lag_mesh_upper=lag_upper,
            )
            requested_lag_intervals += 1
            maximum_lag_chart_multiplicity = max(
                maximum_lag_chart_multiplicity, atom_charts
            )
            atom = _require_finite_arb(
                current_atom - alpha * terminal_point[(0, 1)],
                "voltage recovery atom",
            )
            atom_upper = atom.abs_upper()
            total = _require_finite_arb(
                density_mass + atom_upper, "voltage candidate row total"
            )
            if (
                density_mass.abs_upper()
                > maximum_voltage_density.abs_upper()
            ):
                maximum_voltage_density = density_mass
            if atom_upper.abs_upper() > maximum_voltage_atom.abs_upper():
                maximum_voltage_atom = atom_upper
            if total.abs_upper() > maximum_voltage.abs_upper():
                maximum_voltage = total
                maximum_voltage_location = {
                    "delta_cell": delta_cell,
                    "delta_subcell": delta_subcell,
                    "atom_lag_chart_count": atom_charts,
                }

    if total_rectangles != (MESH_CELL_COUNT * subdivisions) ** 2:
        raise AssertionError("the Stage-3I voltage rectangle count changed")

    recovery_density = arb(0)
    recovery_seam_cells = 0
    for history_cell in range(MESH_CELL_COUNT):
        active = _active_delays(history_cell)
        for history_subcell in range(subdivisions):
            history_lower, history_upper = _total_mesh_interval(
                history_cell, history_subcell
            )
            recovery_sum = arb(0)
            voltage_sum = arb(0)
            local_multiplicity = 1
            for delay_index, delay_mesh in active:
                terminal_lower = ranges.period_mesh - delay_mesh + history_lower
                terminal_upper = ranges.period_mesh - delay_mesh + history_upper
                recovery, recovery_charts = ranges.terminal_range(
                    row=1,
                    column=0,
                    lag_mesh_lower=terminal_lower,
                    lag_mesh_upper=terminal_upper,
                )
                voltage, voltage_charts = ranges.terminal_range(
                    row=0,
                    column=0,
                    lag_mesh_lower=terminal_lower,
                    lag_mesh_upper=terminal_upper,
                )
                requested_lag_intervals += 2
                coefficient = series_range(
                    base.delayed_coefficients[delay_index],
                    Fraction(delay_mesh) - history_upper,
                    Fraction(delay_mesh) - history_lower,
                )
                recovery_sum += recovery * coefficient
                voltage_sum += voltage * coefficient
                local_multiplicity *= recovery_charts * voltage_charts
            density = _require_finite_arb(
                recovery_sum - beta * voltage_sum,
                "recovery signed history density",
            )
            history_width = h_arb * _arb_fraction(
                history_upper - history_lower
            )
            recovery_density += density.abs_upper() * history_width
            if local_multiplicity > 1:
                recovery_seam_cells += 1
            maximum_lag_chart_multiplicity = max(
                maximum_lag_chart_multiplicity, local_multiplicity
            )
    recovery_atom = _require_finite_arb(
        terminal_point[(1, 1)] - beta * terminal_point[(0, 1)],
        "recovery scalar atom",
    ).abs_upper()
    recovery_total = _require_finite_arb(
        recovery_density + recovery_atom, "recovery candidate row total"
    )
    if maximum_voltage_location is None:
        raise AssertionError("the Stage-3I voltage maximizer was not recorded")
    if (
        seam_union_rectangle_count
        != geometry_preflight["seam_union_rectangle_count"]
        or recovery_seam_cells
        != geometry_preflight["recovery_seam_subinterval_count"]
        or maximum_lag_chart_multiplicity
        != geometry_preflight["maximum_lag_chart_multiplicity"]
        or requested_lag_intervals
        != geometry_preflight["requested_lag_interval_count"]
    ):
        raise AssertionError("the Stage-3I runtime lag geometry changed")

    candidate_records = {
        "voltage_history_density_TV_upper": _upper_record(
            maximum_voltage_density
        ),
        "voltage_recovery_atom_upper": _upper_record(maximum_voltage_atom),
        "voltage_total_row_upper": _upper_record(maximum_voltage),
        "voltage_total_maximizer": maximum_voltage_location,
        "recovery_history_density_TV_upper": _upper_record(recovery_density),
        "recovery_recovery_atom_upper": _upper_record(recovery_atom),
        "recovery_total_row_upper": _upper_record(recovery_total),
        "both_injection_branches_summed_before_absolute_value": True,
        "phase_subtraction_inside_each_density_interval": True,
    }
    stage2_certificate = _mapping(stage2.get("certificate"), "Stage-2 certificate")
    excess_records = _candidate_excess_records(candidate_records, stage2_certificate)
    center_target = arb(CENTER_TRANSFER_TARGET)
    if not center_target.lower() > 0:
        raise ValueError("the Stage-3I exact center target is not positive")
    center_closes = bool(
        arb(excess_records["voltage"]).abs_upper() < center_target.lower()
        and arb(excess_records["recovery"]).abs_upper() < center_target.lower()
    )

    stage3h_certificate = _mapping(stage3h.get("certificate"), "Stage-3H certificate")
    stage3g_certificate = _mapping(stage3g.get("certificate"), "Stage-3G certificate")
    stage3f_certificate = _mapping(stage3f.get("certificate"), "Stage-3F certificate")
    ledger, final_errors, final_totals = _transfer_rows_from_excess_records(
        excess_records,
        stage3h_certificate,
        stage3g_certificate,
        stage3f_certificate,
        stage2_certificate,
    )
    contraction_closes = bool(
        ledger["voltage"]["strictly_below_one"]
        and ledger["recovery"]["strictly_below_one"]
    )

    return {
        "geometry": {
            **geometry_preflight,
            "delta_history_rectangle_count": total_rectangles,
            "seam_union_rectangle_count": seam_union_rectangle_count,
            "maximum_lag_chart_multiplicity": max(
                maximum_lag_chart_multiplicity,
                geometry_preflight["maximum_lag_chart_multiplicity"],
            ),
            "recovery_seam_subinterval_count": recovery_seam_cells,
        },
        "candidate": candidate_records,
        "ledger": {
            "candidate_row_excess_target": CENTER_TRANSFER_TARGET,
            "strict_exact_arb_target_comparison": True,
            "candidate_row_excess_semantics": CENTER_EXCESS_SEMANTICS,
            "total_row_budget_semantics": TOTAL_ROW_BUDGET_SEMANTICS,
            "voltage_candidate_row_excess_over_shadow_upper": excess_records[
                "voltage"
            ],
            "recovery_candidate_row_excess_over_shadow_upper": excess_records[
                "recovery"
            ],
            "candidate_row_excess_target_closes": center_closes,
            "rows": ledger,
            "arbitrary_c0_linear_contraction_closes": contraction_closes,
        },
        "errors": final_errors,
        "totals": final_totals,
        "closes": contraction_closes,
    }


@lru_cache(maxsize=1)
def build_outer_signed_density_stage3i_tv(
    repository: Path,
) -> OuterSignedDensityStage3ITV:
    repository = repository.resolve()
    if (
        os.environ.get("OPENBLAS_NUM_THREADS")
        != PINNED_OPENBLAS_NUM_THREADS
        or os.environ.get("OMP_NUM_THREADS") != PINNED_OMP_NUM_THREADS
    ):
        raise RuntimeError(
            "Stage-3I requires OPENBLAS_NUM_THREADS=1 and OMP_NUM_THREADS=1"
        )
    arb_ctx.prec = PRECISION_BITS
    arb_ctx.threads = 1
    _require_unique_disjoint_flags(
        ("base-true flags", BASE_TRUE_FLAGS),
        ("closure flags", CLOSURE_FLAGS),
        ("false flags", FALSE_FLAGS),
    )
    stage3h = _load_parent(
        repository, STAGE3H_RESULT_RELATIVE_PATH, STAGE3H_RESULT_SHA256
    )
    stage3g = _load_parent(
        repository, STAGE3G_RESULT_RELATIVE_PATH, STAGE3G_RESULT_SHA256
    )
    stage3f = _load_parent(
        repository, STAGE3F_RESULT_RELATIVE_PATH, STAGE3F_RESULT_SHA256
    )
    stage2 = _load_parent(repository, STAGE2_RESULT_RELATIVE_PATH, STAGE2_RESULT_SHA256)
    outer = _load_parent(repository, OUTER_RESULT_RELATIVE_PATH, OUTER_RESULT_SHA256)
    stage3h_certificate = _validate_parent_artifact_lock(
        stage3h,
        repository,
        label="Stage-3H",
        schema_id=STAGE3H_SCHEMA_ID,
        result_relative_path=STAGE3H_RESULT_RELATIVE_PATH,
    )
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
    stage3h_gate = _mapping(
        stage3h_certificate.get("transfer_gate"),
        "Stage-3H transfer gate",
    )
    if not (
        stage3h_gate.get("strict_combined_row_uniform_sizes_validated") is True
        and stage3h_gate.get(
            "continuous_center_signed_density_TV_reserve_validated"
        )
        is False
        and stage3h_gate.get("arbitrary_c0_linear_contraction_closes") is False
    ):
        raise ValueError("the strict Stage-3H row sizes were weakened")
    stage3g_gate = _mapping(
        stage3g_certificate.get("transfer_gate"), "Stage-3G transfer gate"
    )
    if not (
        stage3g_gate.get("full_advanced_green_target_validated") is True
        and stage3g_gate.get("full_advanced_boundary_target_validated") is True
        and stage3g_gate.get("joint_augmented_phase_residual_targets_validated")
        is True
    ):
        raise ValueError("the Stage-3G residual/Green theorem was weakened")
    orbit = validate_outer_high_resolution_artifact(
        outer, repository, replay_directed=False
    )
    base = _build_leaky_base_sequences(orbit, PRECISION_BITS)
    guide = _TensorGuide(orbit)
    data = _build_density_certificate(
        guide, base, stage3h, stage3g, stage3f, stage2
    )
    closes = bool(data["closes"])
    claims = {name: True for name in BASE_TRUE_FLAGS}
    claims.update(
        {
            "continuous_center_signed_density_TV_reserve_validated": bool(
                data["ledger"]["candidate_row_excess_target_closes"]
            ),
            "arbitrary_c0_linear_return_contraction_validated": closes,
        }
    )
    claims.update({name: False for name in FALSE_FLAGS})
    return OuterSignedDensityStage3ITV(
        schema_id=SCHEMA_ID,
        model_id=MODEL_ID,
        branch=BRANCH,
        arithmetic_scope=ARITHMETIC_SCOPE,
        precision_bits=PRECISION_BITS,
        row_scope=ROW_SCOPE,
        parent_result_sha256={
            STAGE3H_RESULT_RELATIVE_PATH: STAGE3H_RESULT_SHA256,
            STAGE3G_RESULT_RELATIVE_PATH: STAGE3G_RESULT_SHA256,
            STAGE3F_RESULT_RELATIVE_PATH: STAGE3F_RESULT_SHA256,
            STAGE2_RESULT_RELATIVE_PATH: STAGE2_RESULT_SHA256,
            OUTER_RESULT_RELATIVE_PATH: OUTER_RESULT_SHA256,
        },
        cell_geometry=data["geometry"],
        candidate_continuous_rows=data["candidate"],
        transfer_ledger=data["ledger"],
        transfer_errors={
            "E_voltage": _upper_record(data["errors"]["voltage"]),
            "E_recovery": _upper_record(data["errors"]["recovery"]),
            "E_phase": _mapping(
                _mapping(stage3h.get("certificate"), "Stage-3H certificate").get(
                    "transfer_errors"
                ),
                "Stage-3H transfer errors",
            )["E_phase"],
        },
        transfer_gate={
            "strict_combined_row_uniform_sizes_validated": True,
            "continuous_center_signed_density_TV_reserve_validated": bool(
                data["ledger"]["candidate_row_excess_target_closes"]
            ),
            "continuous_signed_density_total_variation_validated": True,
            "linear_return_gate_evaluated": True,
            "arbitrary_c0_linear_contraction_closes": closes,
            "nonlinear_outer_attraction_closes": False,
        },
        claim_status=claims,
        conclusion=_conclusion_for_outcome(
            bool(data["ledger"]["candidate_row_excess_target_closes"]),
            closes,
        ),
    )


def build_outer_signed_density_stage3i_tv_result(repository: Path) -> dict[str, Any]:
    repository = repository.resolve()
    certificate = json.loads(
        json.dumps(
            asdict(build_outer_signed_density_stage3i_tv(repository)),
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


def reissue_outer_signed_density_stage3i_tv_result(
    repository: Path, prefinal_bytes: bytes
) -> dict[str, Any]:
    """Re-sign the frozen cell sweep under the audited independent gate.

    The prefinal artifact already passed generation plus a cache-cleared
    numerical replay.  Its raw digest fixes every cell, row, parent, source,
    and environment byte.  This migration changes only the contraction
    Boolean, its matching claim, the conclusion, and a scope-string
    clarification from ``continuous`` to ``continuous reduced-history``.
    The current static validator then recomputes every numerical ledger from
    the frozen rows.  The public validator always performs a fresh numerical
    replay.
    """

    repository = repository.resolve()
    if sha256(prefinal_bytes).hexdigest() != PREFINAL_RESULT_SHA256:
        raise ValueError("the Stage-3I prefinal cell artifact changed")
    prefinal = _mapping(
        json.loads(prefinal_bytes.decode("utf-8")),
        "Stage-3I prefinal result",
    )
    if set(prefinal) != {"certificate", "manifest"}:
        raise ValueError("the Stage-3I prefinal top-level schema changed")
    old_certificate = _mapping(
        prefinal.get("certificate"), "Stage-3I prefinal certificate"
    )
    old_manifest = _mapping(
        prefinal.get("manifest"), "Stage-3I prefinal manifest"
    )
    _require_exact_keys(
        old_certificate,
        {field.name for field in fields(OuterSignedDensityStage3ITV)},
        "Stage-3I prefinal certificate",
    )
    _require_exact_keys(
        old_manifest, RESULT_MANIFEST_FIELDS, "Stage-3I prefinal manifest"
    )
    if (
        old_manifest.get("schema_id") != SCHEMA_ID
        or old_manifest.get("result") != RESULT_RELATIVE_PATH
        or old_manifest.get("certificate_sha256")
        != canonical_sha256(old_certificate)
        or old_certificate.get("schema_id") != SCHEMA_ID
        or old_certificate.get("row_scope") != PREFINAL_ROW_SCOPE
    ):
        raise ValueError("the Stage-3I prefinal identity changed")
    old_ledger = _mapping(
        old_certificate.get("transfer_ledger"),
        "Stage-3I prefinal transfer ledger",
    )
    old_rows = _mapping(
        old_ledger.get("rows"), "Stage-3I prefinal transfer rows"
    )
    old_gate = _mapping(
        old_certificate.get("transfer_gate"), "Stage-3I prefinal gate"
    )
    old_claims = _mapping(
        old_certificate.get("claim_status"), "Stage-3I prefinal claims"
    )
    if not (
        old_ledger.get("candidate_row_excess_target_closes") is False
        and old_ledger.get("arbitrary_c0_linear_contraction_closes") is False
        and _mapping(old_rows.get("voltage"), "prefinal voltage row").get(
            "strictly_below_one"
        )
        is True
        and _mapping(old_rows.get("recovery"), "prefinal recovery row").get(
            "strictly_below_one"
        )
        is True
        and old_gate.get(
            "continuous_center_signed_density_TV_reserve_validated"
        )
        is False
        and old_gate.get("arbitrary_c0_linear_contraction_closes") is False
        and old_gate.get("nonlinear_outer_attraction_closes") is False
        and old_claims.get(
            "continuous_center_signed_density_TV_reserve_validated"
        )
        is False
        and old_claims.get(
            "arbitrary_c0_linear_return_contraction_validated"
        )
        is False
        and old_certificate.get("conclusion") == CONCLUSION_OPEN
    ):
        raise ValueError("the Stage-3I prefinal gate boundary changed")

    certificate = deepcopy(dict(old_certificate))
    certificate["row_scope"] = ROW_SCOPE
    certificate["transfer_ledger"][
        "arbitrary_c0_linear_contraction_closes"
    ] = True
    certificate["transfer_gate"][
        "arbitrary_c0_linear_contraction_closes"
    ] = True
    certificate["claim_status"][
        "arbitrary_c0_linear_return_contraction_validated"
    ] = True
    certificate["conclusion"] = CONCLUSION_TARGET_OPEN_CONTRACTION_CLOSED
    result = {
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
    _validate_outer_signed_density_stage3i_tv_result(
        result, repository, replay_numerics=False
    )
    return result


def _validate_outer_signed_density_stage3i_tv_result(
    payload: Mapping[str, Any],
    repository: Path,
    *,
    replay_numerics: bool = True,
) -> None:
    repository = repository.resolve()
    arb_ctx.prec = PRECISION_BITS
    arb_ctx.threads = 1
    _require_unique_disjoint_flags(
        ("base-true flags", BASE_TRUE_FLAGS),
        ("closure flags", CLOSURE_FLAGS),
        ("false flags", FALSE_FLAGS),
    )
    if not isinstance(payload, Mapping) or set(payload) != {"certificate", "manifest"}:
        raise ValueError("the Stage-3I top-level schema changed")
    certificate = _mapping(payload.get("certificate"), "Stage-3I certificate")
    manifest = _mapping(payload.get("manifest"), "Stage-3I manifest")
    _require_exact_keys(
        certificate,
        {field.name for field in fields(OuterSignedDensityStage3ITV)},
        "Stage-3I certificate",
    )
    _require_exact_keys(manifest, RESULT_MANIFEST_FIELDS, "Stage-3I manifest")
    if (
        manifest.get("schema_id") != SCHEMA_ID
        or manifest.get("result") != RESULT_RELATIVE_PATH
        or manifest.get("default_command") != DEFAULT_COMMAND
    ):
        raise ValueError("the Stage-3I manifest identity changed")
    environment = _mapping(manifest.get("environment"), "Stage-3I environment")
    _require_exact_keys(environment, ENVIRONMENT_FIELDS, "Stage-3I environment")
    if dict(environment) != _expected_environment():
        raise ValueError("the Stage-3I environment changed")
    if canonical_sha256(certificate) != manifest.get("certificate_sha256"):
        raise ValueError("the Stage-3I certificate digest changed")
    sources = _mapping(manifest.get("source_sha256"), "Stage-3I source manifest")
    if set(sources) != set(SOURCE_MANIFEST):
        raise ValueError("the Stage-3I source set changed")
    for relative in SOURCE_MANIFEST:
        if sources.get(relative) != _sha256_path(repository / relative):
            raise ValueError(f"a Stage-3I source changed: {relative}")

    if (
        certificate.get("schema_id") != SCHEMA_ID
        or certificate.get("model_id") != MODEL_ID
        or certificate.get("branch") != BRANCH
        or certificate.get("arithmetic_scope") != ARITHMETIC_SCOPE
        or certificate.get("precision_bits") != PRECISION_BITS
        or certificate.get("row_scope") != ROW_SCOPE
    ):
        raise ValueError("the Stage-3I certificate identity changed")
    expected_parents = {
        STAGE3H_RESULT_RELATIVE_PATH: STAGE3H_RESULT_SHA256,
        STAGE3G_RESULT_RELATIVE_PATH: STAGE3G_RESULT_SHA256,
        STAGE3F_RESULT_RELATIVE_PATH: STAGE3F_RESULT_SHA256,
        STAGE2_RESULT_RELATIVE_PATH: STAGE2_RESULT_SHA256,
        OUTER_RESULT_RELATIVE_PATH: OUTER_RESULT_SHA256,
    }
    parents = _mapping(
        certificate.get("parent_result_sha256"), "Stage-3I parents"
    )
    if dict(parents) != expected_parents:
        raise ValueError("the Stage-3I parent digest map changed")

    stage3h = _load_parent(
        repository, STAGE3H_RESULT_RELATIVE_PATH, STAGE3H_RESULT_SHA256
    )
    stage3h_certificate = _validate_parent_artifact_lock(
        stage3h,
        repository,
        label="Stage-3H",
        schema_id=STAGE3H_SCHEMA_ID,
        result_relative_path=STAGE3H_RESULT_RELATIVE_PATH,
    )
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
    orbit = validate_outer_high_resolution_artifact(
        outer, repository, replay_directed=False
    )

    stage3h_gate = _mapping(
        stage3h_certificate.get("transfer_gate"), "Stage-3H transfer gate"
    )
    if not (
        stage3h_gate.get("strict_combined_row_uniform_sizes_validated") is True
        and stage3h_gate.get(
            "continuous_center_signed_density_TV_reserve_validated"
        )
        is False
        and stage3h_gate.get("arbitrary_c0_linear_contraction_closes") is False
    ):
        raise ValueError("the Stage-3H theorem boundary changed")
    stage3g_gate = _mapping(
        stage3g_certificate.get("transfer_gate"), "Stage-3G transfer gate"
    )
    if not (
        stage3g_gate.get("full_advanced_green_target_validated") is True
        and stage3g_gate.get("full_advanced_boundary_target_validated") is True
        and stage3g_gate.get(
            "joint_augmented_phase_residual_targets_validated"
        )
        is True
    ):
        raise ValueError("the Stage-3G theorem boundary changed")

    geometry = _mapping(certificate.get("cell_geometry"), "Stage-3I geometry")
    candidate = _mapping(
        certificate.get("candidate_continuous_rows"),
        "Stage-3I candidate rows",
    )
    ledger = _mapping(
        certificate.get("transfer_ledger"), "Stage-3I transfer ledger"
    )
    errors = _mapping(
        certificate.get("transfer_errors"), "Stage-3I row-budget bounds"
    )
    gate = _mapping(certificate.get("transfer_gate"), "Stage-3I gate")
    claims = _mapping(certificate.get("claim_status"), "Stage-3I claims")
    _require_exact_keys(geometry, GEOMETRY_FIELDS, "Stage-3I geometry")
    _require_exact_keys(candidate, CANDIDATE_FIELDS, "Stage-3I candidate rows")
    _require_exact_keys(ledger, LEDGER_FIELDS, "Stage-3I transfer ledger")
    _require_exact_keys(errors, TRANSFER_ERROR_FIELDS, "Stage-3I errors")
    _require_exact_keys(gate, TRANSFER_GATE_FIELDS, "Stage-3I gate")

    expected_geometry = _stage3i_geometry_preflight(
        float(orbit.period), float(TAU_1) / MESH_CELL_COUNT
    )
    if dict(geometry) != expected_geometry:
        raise ValueError("the Stage-3I directed lag geometry changed")

    if (
        candidate.get("both_injection_branches_summed_before_absolute_value")
        is not True
        or candidate.get("phase_subtraction_inside_each_density_interval")
        is not True
    ):
        raise ValueError("the Stage-3I signed-density operation order changed")
    candidate_numeric_fields = CANDIDATE_FIELDS - {
        "voltage_total_maximizer",
        "both_injection_branches_summed_before_absolute_value",
        "phase_subtraction_inside_each_density_interval",
    }
    candidate_values: dict[str, Decimal] = {}
    for name in candidate_numeric_fields:
        if not isinstance(candidate.get(name), str):
            raise ValueError(f"the Stage-3I {name} is not a serialized bound")
        value = _decimal(candidate.get(name), f"Stage-3I {name}")
        if value < 0:
            raise ValueError("a Stage-3I candidate row bound became negative")
        candidate_values[name] = value
    voltage_density = candidate_values["voltage_history_density_TV_upper"]
    voltage_atom = candidate_values["voltage_recovery_atom_upper"]
    voltage_total = candidate_values["voltage_total_row_upper"]
    recovery_density = candidate_values["recovery_history_density_TV_upper"]
    recovery_atom = candidate_values["recovery_recovery_atom_upper"]
    recovery_total = candidate_values["recovery_total_row_upper"]
    if not (
        max(voltage_density, voltage_atom)
        <= voltage_total
        <= voltage_density + voltage_atom
        and max(recovery_density, recovery_atom)
        <= recovery_total
        <= recovery_density + recovery_atom
    ):
        raise ValueError("the Stage-3I candidate row decomposition is inconsistent")

    voltage_location = _mapping(
        candidate.get("voltage_total_maximizer"),
        "Stage-3I voltage maximizer",
    )
    _require_exact_keys(
        voltage_location,
        VOLTAGE_MAXIMIZER_FIELDS,
        "Stage-3I voltage maximizer",
    )
    delta_cell = voltage_location.get("delta_cell")
    delta_subcell = voltage_location.get("delta_subcell")
    atom_chart_count = voltage_location.get("atom_lag_chart_count")
    if (
        type(delta_cell) is not int
        or not 0 <= delta_cell < MESH_CELL_COUNT
        or type(delta_subcell) is not int
        or not 0 <= delta_subcell < SUBCELLS_PER_MESH_CELL
        or type(atom_chart_count) is not int
        or atom_chart_count <= 0
    ):
        raise ValueError("the Stage-3I voltage maximizer left the cell cover")
    delta_lower, delta_upper = _total_mesh_interval(
        delta_cell, delta_subcell
    )
    period_mesh = Fraction.from_float(float(orbit.period)) / Fraction.from_float(
        float(TAU_1) / MESH_CELL_COUNT
    )
    expected_atom_chart_count = len(
        _lag_chart_indices(
            delta_cell,
            period_mesh - delta_upper,
            period_mesh - delta_lower,
        )
    )
    if atom_chart_count != expected_atom_chart_count:
        raise ValueError("the Stage-3I voltage maximizer chart count changed")

    if (
        ledger.get("candidate_row_excess_target") != CENTER_TRANSFER_TARGET
        or ledger.get("strict_exact_arb_target_comparison") is not True
        or ledger.get("candidate_row_excess_semantics")
        != CENTER_EXCESS_SEMANTICS
        or ledger.get("total_row_budget_semantics")
        != TOTAL_ROW_BUDGET_SEMANTICS
    ):
        raise ValueError("the Stage-3I exact center-reserve semantics changed")
    excess_records = _candidate_excess_records(candidate, stage2_certificate)
    if (
        ledger.get("voltage_candidate_row_excess_over_shadow_upper")
        != excess_records["voltage"]
        or ledger.get("recovery_candidate_row_excess_over_shadow_upper")
        != excess_records["recovery"]
    ):
        raise ValueError("the Stage-3I one-sided candidate slack changed")
    target = arb(CENTER_TRANSFER_TARGET)
    if not target.lower() > 0:
        raise ValueError("the Stage-3I exact center target is not positive")
    center_closes = bool(
        arb(excess_records["voltage"]).abs_upper() < target.lower()
        and arb(excess_records["recovery"]).abs_upper() < target.lower()
    )
    if ledger.get("candidate_row_excess_target_closes") is not center_closes:
        raise ValueError("the Stage-3I center-reserve gate is inconsistent")

    rows = _mapping(ledger.get("rows"), "Stage-3I transfer rows")
    _require_exact_keys(rows, {"voltage", "recovery"}, "Stage-3I transfer rows")
    for row_id in ("voltage", "recovery"):
        row = _mapping(rows.get(row_id), f"Stage-3I {row_id} transfer row")
        _require_exact_keys(
            row, LEDGER_ROW_FIELDS, f"Stage-3I {row_id} transfer row"
        )
        for name in LEDGER_ROW_FIELDS - {"strictly_below_one"}:
            if not isinstance(row.get(name), str):
                raise ValueError(
                    f"the Stage-3I {row_id} {name} is not serialized"
                )
            if _decimal(row.get(name), f"Stage-3I {row_id} {name}") < 0:
                raise ValueError("a Stage-3I transfer contribution became negative")
        expected_below_one = (
            _decimal(
                row.get("stage2_shadow_plus_E_upper"),
                f"Stage-3I {row_id} total",
            )
            < 1
        )
        if row.get("strictly_below_one") is not expected_below_one:
            raise ValueError("a Stage-3I row contraction flag is inconsistent")
    expected_rows, _, _ = _transfer_rows_from_excess_records(
        excess_records,
        stage3h_certificate,
        stage3g_certificate,
        stage3f_certificate,
        stage2_certificate,
    )
    if dict(rows) != expected_rows:
        raise ValueError("the Stage-3I once-only transfer formula ledger changed")
    contraction_closes = bool(
        expected_rows["voltage"]["strictly_below_one"]
        and expected_rows["recovery"]["strictly_below_one"]
    )
    if (
        ledger.get("arbitrary_c0_linear_contraction_closes")
        is not contraction_closes
    ):
        raise ValueError("the Stage-3I linear contraction ledger is inconsistent")

    stage3h_errors = _mapping(
        stage3h_certificate.get("transfer_errors"), "Stage-3H transfer errors"
    )
    expected_errors = {
        "E_voltage": expected_rows["voltage"]["E_row_upper"],
        "E_recovery": expected_rows["recovery"]["E_row_upper"],
        "E_phase": stage3h_errors.get("E_phase"),
    }
    if dict(errors) != expected_errors:
        raise ValueError("the Stage-3I row-budget bound ledger changed")
    expected_gate = {
        "strict_combined_row_uniform_sizes_validated": True,
        "continuous_center_signed_density_TV_reserve_validated": center_closes,
        "continuous_signed_density_total_variation_validated": True,
        "linear_return_gate_evaluated": True,
        "arbitrary_c0_linear_contraction_closes": contraction_closes,
        "nonlinear_outer_attraction_closes": False,
    }
    if dict(gate) != expected_gate:
        raise ValueError("the Stage-3I transfer gate ledger changed")

    expected_claims = {name: True for name in BASE_TRUE_FLAGS}
    expected_claims.update(
        {
            "continuous_center_signed_density_TV_reserve_validated": (
                center_closes
            ),
            "arbitrary_c0_linear_return_contraction_validated": (
                contraction_closes
            ),
        }
    )
    expected_claims.update({name: False for name in FALSE_FLAGS})
    if dict(claims) != expected_claims:
        raise ValueError("the Stage-3I claim ledger changed")
    expected_conclusion = _conclusion_for_outcome(
        center_closes, contraction_closes
    )
    if certificate.get("conclusion") != expected_conclusion:
        raise ValueError("the Stage-3I conclusion changed")

    if not replay_numerics:
        return

    # A source-bound validation is a fresh numerical replay, never a warm
    # answer inherited from generation or an earlier repository state.
    build_outer_signed_density_stage3i_tv.cache_clear()
    _chebyshev_to_bernstein_matrix.cache_clear()
    expected = json.loads(
        json.dumps(
            asdict(build_outer_signed_density_stage3i_tv(repository)),
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        )
    )
    if certificate != expected:
        raise ValueError("the Stage-3I certificate differs from replay")


def validate_outer_signed_density_stage3i_tv_result(
    payload: Mapping[str, Any], repository: Path
) -> None:
    """Validate all static ledgers and perform a cache-cleared numeric replay."""

    _validate_outer_signed_density_stage3i_tv_result(
        payload, repository, replay_numerics=True
    )


__all__ = [
    "BASE_TRUE_FLAGS",
    "CENTER_EXCESS_SEMANTICS",
    "CENTER_TRANSFER_TARGET",
    "CLOSURE_FLAGS",
    "CONCLUSION_TARGET_OPEN_CONTRACTION_CLOSED",
    "DEFAULT_COMMAND",
    "FALSE_FLAGS",
    "NOTE_RELATIVE_PATH",
    "PREFINAL_RESULT_SHA256",
    "RESULT_RELATIVE_PATH",
    "ROW_SCOPE",
    "SOURCE_MANIFEST",
    "TOTAL_ROW_BUDGET_SEMANTICS",
    "build_outer_signed_density_stage3i_tv",
    "build_outer_signed_density_stage3i_tv_result",
    "canonical_sha256",
    "reissue_outer_signed_density_stage3i_tv_result",
    "validate_outer_signed_density_stage3i_tv_result",
]
