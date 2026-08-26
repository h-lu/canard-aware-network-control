"""Complete the inner-orbit right-half Floquet count.

The local inner-root theorem isolates one simple positive characteristic
value.  The leaky Floquet--Riesz theorem isolates the algebraically simple
translation value at zero and removes the infinite tail and ``Re s >= 256``.
This module reuses the corrected full-operator cover engine on the compact
principal strip left after those two disks are removed.  Its physical main
representation uses unshifted delayed coefficients and output-row phases;
an equivalent shifted-coefficient/input-column formula is checked separately.

A completed exact dyadic partition therefore proves that the two registered
local roots are the only closed-right-half-plane characteristic values.  It
follows that the center inner orbit has exactly one unstable multiplier.  No
parameter-box, invariant-manifold, nonlinear pulse, or onset claim is made.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from concurrent.futures import ProcessPoolExecutor
from decimal import Decimal, localcontext
from fractions import Fraction
from hashlib import sha256
import json
import math
import multiprocessing
from pathlib import Path
import platform
from typing import Any, Callable, Mapping, Sequence

import gmpy2
import numpy as np
import scipy

from canard_control.directed_interval import (
    DirectedInterval,
    decimal_upper,
    pi_interval,
    upward_sum,
)
from canard_control.floquet_cover_arithmetic import (
    _binary_coefficients,
    _binary_complex_split_upper,
    _binary_environment_checked,
    _box_distance_split_upper,
    _coefficient_matrix,
)
from canard_control.leaky_floquet_inner_unstable_root import (
    RESULT_RELATIVE_PATH as INNER_ROOT_RESULT_RELATIVE_PATH,
    validate_leaky_inner_unstable_root_result,
)
from canard_control.leaky_floquet_compact_cover_engine import (
    BinaryCandidate,
    CoverLeaf,
    Rectangle,
    WorstCoverCell,
    leaf_digest,
    mode_rotation_basis,
    prefix_complete,
    rectangle_from_path,
    rectangle_strictly_inside_origin_disk,
    split_rectangle,
    validate_cell,
)
from canard_control.leaky_floquet_riesz_reduction import (
    RESULT_RELATIVE_PATH as RIESZ_RESULT_RELATIVE_PATH,
    validate_leaky_floquet_riesz_result,
)
from canard_control.leaky_floquet_transfer import (
    RESULT_RELATIVE_PATH as FLOQUET_TRANSFER_RESULT_RELATIVE_PATH,
    load_validated_leaky_orbit_evidence,
    validate_leaky_floquet_transfer_artifact,
)
from canard_control.leaky_periodic_validation import (
    _build_leaky_base_sequences,
)


SCHEMA_ID = "leaky-floquet-inner-right-half-cover-v3"
MODEL_ID = "autonomous-leaky-recovery-two-delay-fhn-bistable-proposal"
BRANCH = "inner_saddle_candidate"
SOURCE_RELATIVE_PATH = (
    "src/canard_control/leaky_floquet_inner_right_half_cover.py"
)
GENERATOR_RELATIVE_PATH = (
    "experiments/leaky_floquet_inner_right_half_cover.py"
)
NOTE_RELATIVE_PATH = "docs/leaky-floquet-inner-right-half-cover.md"
TEST_RELATIVE_PATH = "tests/test_leaky_floquet_inner_right_half_cover.py"
RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_floquet_inner_right_half_cover.json"
)
DEFAULT_COMMAND = (
    "OPENBLAS_NUM_THREADS=1 PYTHONPATH=build/testdeps:src /usr/bin/python3 "
    "experiments/leaky_floquet_inner_right_half_cover.py --workers 12"
)
ARITHMETIC_SCOPE = (
    "160-bit outward MPFR split-Wiener full-operator cells on the upper "
    "compact principal strip; source-bound radius-1e-12 center inner orbit; "
    "physical output-row delay phases, a dual-representation oracle, exact "
    "dyadic partition, two rigorously "
    "counted local disks, and 256-bit limiting-cell stress replay"
)

PRECISION_BITS = 160
STRESS_PRECISION_BITS = 256
FOURIER_CUTOFF = 64
COEFFICIENT_SUPPORT_RADIUS = 128
OUTER_REAL_PART = Decimal(256)
LOW_SEAM = Decimal(1)
CORRECTION_RADIUS = "1e-12"
ACCEPTANCE_THRESHOLD = Decimal("0.995")
MAXIMUM_PROCESSED_CELLS = 300000
MAXIMUM_DEPTH = 96
EXPECTED_COMPLETE_LEAF_PARTITION_SHA256 = (
    "8d105b4d17e2628c216dbd8fa8474b886f6d1d9684dcaaff279f4bb6f563baa5"
)

EXPECTED_RIESZ_RESULT_SHA256 = (
    "5185f8f39cd8f87052a50b072af2bfee591d8cd626301bd9a9470134c14df55c"
)
EXPECTED_FLOQUET_TRANSFER_RESULT_SHA256 = (
    "5a3709ec792b29ed41533101245b13b3d35084ae508bdd1d420728200a5a5b16"
)
EXPECTED_INNER_ROOT_RESULT_SHA256 = (
    "ab2876efc8a26df544f56257ab00b9fde0fea4ba043f4500f1450e0d0885fa2c"
)
EXPECTED_INNER_ORBIT_RESULT_SHA256 = (
    "bee1da065d213c3c33d724ced1dba37c5914934515c1128588919bed34abe69b"
)

STRUCTURAL_TRUE = (
    "source_validated_inner_orbit_ball_used",
    "leaky_recovery_bottom_right_pencil_validated",
    "physical_unshifted_coefficient_output_phase_used",
    "shifted_coefficient_input_phase_equivalence_oracle_used",
    "tail_output_frequency_cancellation_validated",
    "corrected_full_operator_cover_engine_reused",
    "full_mode_128_coefficient_support_used",
    "complex_split_wiener_norm_used",
    "correct_fast_and_slow_tail_inverses_used",
    "inner_nested_orbit_ball_parent_used",
    "neutral_root_algebraically_simple_parent_used",
    "positive_root_algebraically_simple_parent_used",
)

TRUE_ON_COMPLETE = (
    "neutral_and_positive_disks_disjoint_validated",
    "neutral_and_positive_disk_boundary_seams_validated",
    "disk_boundaries_owned_by_zero_free_keyhole_validated",
    "three_region_spectral_partition_no_gap_or_double_count_validated",
    "upper_compact_strip_exact_partition_validated",
    "all_nonlocal_cells_full_operator_neumann_validated",
    "compact_remainder_zero_free_validated",
    "far_right_half_plane_excluded_by_riesz_parent",
    "lower_half_strip_excluded_by_real_conjugacy",
    "principal_strip_global_root_count_validated",
    "inner_no_other_right_half_roots_validated",
    "inner_total_unstable_multiplier_count_validated",
    "inner_saddle_floquet_index_validated",
    "global_count_from_local_roots_plus_zero_free_remainder_validated",
    "analytic_fredholm_argument_principle_additivity_used",
)

ALWAYS_FALSE = (
    "finite_binary_winding_promoted_to_proof",
    "common_parameter_box_inner_index_validated",
    "inner_stable_manifold_validated",
    "inner_nonlinear_saddle_block_validated",
    "asynchronous_network_root_validated",
    "history_space_separator_validated",
    "physical_pulse_onset_validated",
    "canard_root_equals_physical_onset_proved",
)

SOURCE_MANIFEST = (
    SOURCE_RELATIVE_PATH,
    GENERATOR_RELATIVE_PATH,
    NOTE_RELATIVE_PATH,
    "src/canard_control/directed_interval.py",
    "src/canard_control/fhn_periodic_infinite_validation.py",
    "src/canard_control/floquet_cover_arithmetic.py",
    "src/canard_control/leaky_floquet_compact_cover_engine.py",
    "src/canard_control/leaky_floquet_inner_unstable_root.py",
    "src/canard_control/leaky_floquet_riesz_reduction.py",
    "src/canard_control/leaky_floquet_transfer.py",
    "src/canard_control/leaky_periodic_validation.py",
)


@dataclass(frozen=True)
class _ParentData:
    orbit: Any
    evidence: Any
    riesz: Mapping[str, Any]
    root: Mapping[str, Any]


@dataclass(frozen=True)
class _StressReplay:
    precision_bits: int
    same_cell_upper: str | None
    finer_split_upper: str | None
    strict: bool


@dataclass(frozen=True)
class InnerRightHalfCoverCertificate:
    schema_id: str
    model_id: str
    branch: str
    riesz_result_sha256: str
    floquet_transfer_result_sha256: str
    inner_root_result_sha256: str
    inner_orbit_result: str
    inner_orbit_result_sha256: str
    cover_engine_source_sha256: str
    candidate_fingerprint: str
    source_orbit_correction_radius: str
    correction_radius: str
    precision_bits: int
    norm_id: str
    fourier_cutoff: int
    coefficient_support_half_bandwidth: int
    complex_finite_dimension: int
    outer_real_part: str
    upper_phase_lower: str
    upper_phase_upper: str
    neutral_disk_radius: str
    positive_disk_center: str
    positive_disk_radius: str
    root_rectangle_count: int
    accepted_leaf_count: int
    neutral_disk_leaf_count: int
    positive_disk_leaf_count: int
    neumann_leaf_count: int
    processed_cell_count: int
    pending_cell_count: int
    pending_low_unit_count: int
    pending_right_low_count: int
    pending_upper_band_count: int
    neutral_disk_first_processed_cell: int | None
    positive_disk_first_processed_cell: int | None
    accepted_normalized_root_fraction: str
    maximum_depth: int
    acceptance_threshold: str
    maximum_contraction_upper: str | None
    minimum_contraction_margin_lower: str | None
    stress_replay_precision_bits: int
    worst_cell_stress_contraction_upper: str | None
    worst_cell_finer_split_stress_maximum_contraction_upper: str | None
    worst_cell_finer_split_stress_strict: bool
    leaf_partition_sha256: str
    neutral_disk_characteristic_value_count: int | None
    positive_disk_characteristic_value_count: int | None
    compact_keyhole_characteristic_value_count: int | None
    directed_closed_right_half_characteristic_value_count: int | None
    closed_right_half_nontranslation_characteristic_value_count: int | None
    directed_unstable_multiplier_count: int | None
    source_validated_inner_orbit_ball_used: bool
    leaky_recovery_bottom_right_pencil_validated: bool
    physical_unshifted_coefficient_output_phase_used: bool
    shifted_coefficient_input_phase_equivalence_oracle_used: bool
    tail_output_frequency_cancellation_validated: bool
    corrected_full_operator_cover_engine_reused: bool
    full_mode_128_coefficient_support_used: bool
    complex_split_wiener_norm_used: bool
    correct_fast_and_slow_tail_inverses_used: bool
    inner_nested_orbit_ball_parent_used: bool
    neutral_root_algebraically_simple_parent_used: bool
    positive_root_algebraically_simple_parent_used: bool
    neutral_and_positive_disks_disjoint_validated: bool
    neutral_and_positive_disk_boundary_seams_validated: bool
    disk_boundaries_owned_by_zero_free_keyhole_validated: bool
    three_region_spectral_partition_no_gap_or_double_count_validated: bool
    upper_compact_strip_exact_partition_validated: bool
    all_nonlocal_cells_full_operator_neumann_validated: bool
    compact_remainder_zero_free_validated: bool
    far_right_half_plane_excluded_by_riesz_parent: bool
    lower_half_strip_excluded_by_real_conjugacy: bool
    principal_strip_global_root_count_validated: bool
    inner_no_other_right_half_roots_validated: bool
    inner_total_unstable_multiplier_count_validated: bool
    inner_saddle_floquet_index_validated: bool
    global_count_from_local_roots_plus_zero_free_remainder_validated: bool
    analytic_fredholm_argument_principle_additivity_used: bool
    finite_binary_winding_promoted_to_proof: bool
    common_parameter_box_inner_index_validated: bool
    inner_stable_manifold_validated: bool
    inner_nonlinear_saddle_block_validated: bool
    asynchronous_network_root_validated: bool
    history_space_separator_validated: bool
    physical_pulse_onset_validated: bool
    canard_root_equals_physical_onset_proved: bool
    leaves: tuple[CoverLeaf, ...]
    worst_cell: WorstCoverCell | None
    failure_reason: str | None


_CELL_WORKER_STATE: tuple[
    BinaryCandidate,
    Any,
    DirectedInterval,
    int,
    Decimal,
] | None = None


def _parallel_validate_cell(rectangle: Rectangle) -> Any:
    if _CELL_WORKER_STATE is None:
        raise RuntimeError("the inner cell worker was not initialized")
    candidate, base, correction, precision, threshold = _CELL_WORKER_STATE
    return validate_cell(
        rectangle,
        candidate,
        base,
        correction,
        precision,
        threshold,
    )


def _mapping(value: object, label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{label} must be a mapping")
    return value


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


def _margin(value: str) -> str:
    with localcontext() as context:
        context.prec = max(160, len(value) + 10)
        return format(Decimal(1) - Decimal(value), "f")


def _validate_parents(
    repository: Path,
    *,
    replay_parents: bool,
) -> _ParentData:
    repository = repository.resolve()
    riesz_path = repository / RIESZ_RESULT_RELATIVE_PATH
    root_path = repository / INNER_ROOT_RESULT_RELATIVE_PATH
    transfer_path = repository / FLOQUET_TRANSFER_RESULT_RELATIVE_PATH
    if _sha256_path(riesz_path) != EXPECTED_RIESZ_RESULT_SHA256:
        raise ValueError("the inner cover Riesz parent changed")
    if _sha256_path(root_path) != EXPECTED_INNER_ROOT_RESULT_SHA256:
        raise ValueError("the inner local-root parent changed")
    if _sha256_path(transfer_path) != EXPECTED_FLOQUET_TRANSFER_RESULT_SHA256:
        raise ValueError("the inner neutral-root transfer parent changed")
    riesz_payload = _mapping(json.loads(riesz_path.read_text()), "Riesz parent")
    root_payload = _mapping(json.loads(root_path.read_text()), "root parent")
    transfer_payload = _mapping(
        json.loads(transfer_path.read_text()), "transfer parent"
    )
    if replay_parents:
        validate_leaky_floquet_riesz_result(riesz_payload, repository)
        validate_leaky_inner_unstable_root_result(root_payload, repository)
        validate_leaky_floquet_transfer_artifact(
            transfer_payload, repository, recompute=False
        )
    riesz_artifact = _mapping(riesz_payload.get("artifact"), "Riesz artifact")
    riesz_branches = _mapping(riesz_artifact.get("branches"), "Riesz branches")
    riesz = _mapping(riesz_branches.get(BRANCH), "inner Riesz branch")
    for name in (
        "principal_logarithmic_strip_covers_all_nonzero_unstable_multipliers",
        "uniform_tail_block_invertible_on_closed_right_half_strip",
        "analytic_finite_schur_reduction_proved",
        "analytic_characteristic_multiplicity_preserved_by_schur_reduction",
        "outer_half_plane_excluded",
        "local_complex_punctured_half_disk_excluded",
    ):
        if riesz.get(name) is not True:
            raise ValueError(f"the inner Riesz gate is absent: {name}")
    root = _mapping(root_payload.get("certificate"), "inner root certificate")
    for name in (
        "exactly_one_characteristic_value_in_root_disk",
        "root_analytic_algebraic_multiplicity_one",
        "unique_disk_root_real_by_conjugacy",
        "root_strictly_positive",
        "associated_multiplier_strictly_greater_than_one",
        "physical_delay_dual_representation_oracle_validated",
        "unshifted_coefficient_output_phase_pencil_used",
        "orbit_period_phase_variation_uses_output_modes",
        "tail_output_frequency_cancellation_validated",
    ):
        if root.get(name) is not True:
            raise ValueError(f"the positive-root parent gate is absent: {name}")
    if root.get("inner_no_other_right_half_roots_validated") is not False:
        raise ValueError("the local-root parent overstates its global scope")
    transfer_artifact = _mapping(
        transfer_payload.get("artifact"), "transfer artifact"
    )
    transfer_branches = _mapping(
        transfer_artifact.get("branches"), "transfer branches"
    )
    transfer = _mapping(transfer_branches.get(BRANCH), "inner transfer branch")
    if (
        transfer.get("neutral_multiplier_algebraically_simple_validated")
        is not True
        or transfer.get("translation_jordan_vector_excluded") is not True
    ):
        raise ValueError("the neutral translation root is not algebraically simple")
    orbit, evidence = load_validated_leaky_orbit_evidence(repository, BRANCH)
    if evidence.source_result_sha256 != EXPECTED_INNER_ORBIT_RESULT_SHA256:
        raise ValueError("the inner source orbit changed")
    fingerprints = {
        evidence.candidate_fingerprint,
        str(riesz.get("candidate_fingerprint")),
        str(root.get("candidate_fingerprint")),
        str(transfer.get("candidate_fingerprint")),
    }
    if len(fingerprints) != 1:
        raise ValueError("the inner cover parents use different center orbits")
    if root.get("nested_correction_radius") != CORRECTION_RADIUS:
        raise ValueError("the inner local-root nested ball changed")
    return _ParentData(orbit, evidence, riesz, root)


def _prepare_inner_candidate(
    orbit: Any,
    base: Any,
    precision: int,
) -> BinaryCandidate:
    current, delayed = _binary_coefficients(orbit)
    expected = set(
        range(-COEFFICIENT_SUPPORT_RADIUS, COEFFICIENT_SUPPORT_RADIUS + 1)
    )
    if set(current) != expected or set(delayed) != expected:
        raise ValueError("the inner coefficient support is incomplete")
    modes = np.arange(-FOURIER_CUTOFF, FOURIER_CUTOFF + 1, dtype=int)
    tail_modes = np.concatenate(
        (
            np.arange(
                -FOURIER_CUTOFF - COEFFICIENT_SUPPORT_RADIUS,
                -FOURIER_CUTOFF,
                dtype=int,
            ),
            np.arange(
                FOURIER_CUTOFF + 1,
                FOURIER_CUTOFF + COEFFICIENT_SUPPORT_RADIUS + 1,
                dtype=int,
            ),
        )
    )
    current_errors: list[gmpy2.mpfr] = []
    delayed_errors: list[gmpy2.mpfr] = []
    current_terms: list[gmpy2.mpfr] = []
    delayed_terms: list[gmpy2.mpfr] = []
    for mode in range(
        -COEFFICIENT_SUPPORT_RADIUS,
        COEFFICIENT_SUPPORT_RADIUS + 1,
    ):
        current_errors.append(
            _box_distance_split_upper(
                base.current_coefficient[mode], current[mode]
            )
        )
        delayed_errors.append(
            _box_distance_split_upper(
                base.delayed_state_derivative[mode], delayed[mode]
            )
        )
        current_terms.append(_binary_complex_split_upper(current[mode], precision))
        delayed_terms.append(_binary_complex_split_upper(delayed[mode], precision))
    finite_basis = mode_rotation_basis(modes, base, precision)
    tail_basis = mode_rotation_basis(tail_modes, base, precision)
    return BinaryCandidate(
        modes=modes,
        tail_modes=tail_modes,
        current_finite=_coefficient_matrix(modes, modes, current),
        delayed_finite=_coefficient_matrix(modes, modes, delayed),
        current_finite_tail=_coefficient_matrix(modes, tail_modes, current),
        delayed_finite_tail=_coefficient_matrix(modes, tail_modes, delayed),
        current_tail_finite=_coefficient_matrix(tail_modes, modes, current),
        delayed_tail_finite=_coefficient_matrix(tail_modes, modes, delayed),
        current_coefficients=current,
        delayed_coefficients=delayed,
        current_error_norm=upward_sum(current_errors, precision),
        delayed_error_norm=upward_sum(delayed_errors, precision),
        current_binary_norm=upward_sum(current_terms, precision),
        delayed_binary_norm=upward_sum(delayed_terms, precision),
        finite_mode_rotations=finite_basis[0],
        tail_mode_rotations=tail_basis[0],
        finite_mode_rotation_split=finite_basis[1],
        tail_mode_rotation_split=tail_basis[1],
        finite_mode_rotation_error=finite_basis[2],
        tail_mode_rotation_error=tail_basis[2],
        finite_mode_binary_split=finite_basis[3],
        tail_mode_binary_split=tail_basis[3],
    )


def _root_rectangles(phase_upper: Decimal) -> tuple[Rectangle, ...]:
    if not Decimal(0) < LOW_SEAM < phase_upper:
        raise ValueError("the inner cover seam left the principal upper strip")
    return (
        Rectangle(
            "low_unit",
            "",
            Decimal(0),
            LOW_SEAM,
            Decimal(0),
            LOW_SEAM,
        ),
        Rectangle(
            "right_low",
            "",
            LOW_SEAM,
            OUTER_REAL_PART,
            Decimal(0),
            LOW_SEAM,
        ),
        Rectangle(
            "upper_band",
            "",
            Decimal(0),
            OUTER_REAL_PART,
            LOW_SEAM,
            phase_upper,
        ),
    )


def _rectangle_strictly_inside_positive_disk(
    rectangle: Rectangle,
    center: Decimal,
    radius: Decimal,
) -> bool:
    """Exact upper-corner geometry for a disk centered on the real axis."""

    horizontal = max(
        abs(Fraction(rectangle.sigma_lower) - Fraction(center)),
        abs(Fraction(rectangle.sigma_upper) - Fraction(center)),
    )
    vertical = max(
        abs(Fraction(rectangle.phase_lower)),
        abs(Fraction(rectangle.phase_upper)),
    )
    exact_radius = Fraction(radius)
    return horizontal * horizontal + vertical * vertical < (
        exact_radius * exact_radius
    )


def _stress_replay(
    orbit: Any,
    worst: WorstCoverCell | None,
    phase_upper: Decimal,
) -> _StressReplay:
    if worst is None:
        return _StressReplay(STRESS_PRECISION_BITS, None, None, False)
    roots = {root.root_id: root for root in _root_rectangles(phase_upper)}
    if worst.root_id not in roots:
        raise ValueError("the inner stress cell has an unknown root")
    rectangle = rectangle_from_path(roots[worst.root_id], worst.path)
    base = _build_leaky_base_sequences(orbit, STRESS_PRECISION_BITS)
    candidate = _prepare_inner_candidate(
        orbit, base, STRESS_PRECISION_BITS
    )
    correction = DirectedInterval.from_decimal(
        CORRECTION_RADIUS, STRESS_PRECISION_BITS
    )
    threshold = Decimal("0.999999999999")
    same = validate_cell(
        rectangle,
        candidate,
        base,
        correction,
        STRESS_PRECISION_BITS,
        threshold,
    )
    grandchildren: list[Rectangle] = []
    for child in split_rectangle(rectangle):
        grandchildren.extend(split_rectangle(child))
    finer = [
        validate_cell(
            child,
            candidate,
            base,
            correction,
            STRESS_PRECISION_BITS,
            threshold,
        )
        for child in grandchildren
    ]
    finer_upper = max(
        Decimal(item.worst.contraction_upper) for item in finer
    )
    strict = (
        Decimal(same.worst.contraction_upper) < 1 and finer_upper < 1
    )
    return _StressReplay(
        STRESS_PRECISION_BITS,
        same.worst.contraction_upper,
        format(finer_upper, "f"),
        strict,
    )


def build_inner_right_half_cover(
    repository: Path,
    *,
    precision: int = PRECISION_BITS,
    acceptance_threshold: str = str(ACCEPTANCE_THRESHOLD),
    maximum_processed_cells: int = MAXIMUM_PROCESSED_CELLS,
    maximum_depth: int = MAXIMUM_DEPTH,
    parallel_workers: int = 1,
    replay_parents: bool = True,
    progress: Callable[[int, int, int], None] | None = None,
) -> InnerRightHalfCoverCertificate:
    repository = repository.resolve()
    parent = _validate_parents(repository, replay_parents=replay_parents)
    if precision != PRECISION_BITS:
        raise ValueError("the inner cover precision is pinned at 160 bits")
    threshold = Decimal(acceptance_threshold)
    if not Decimal(0) < threshold < Decimal(1):
        raise ValueError("the inner cover threshold must lie in (0,1)")
    if maximum_processed_cells < 1 or maximum_depth < 1 or parallel_workers < 1:
        raise ValueError("the inner cover budgets must be positive")
    _binary_environment_checked()
    base = _build_leaky_base_sequences(parent.orbit, precision)
    candidate = _prepare_inner_candidate(parent.orbit, base, precision)
    correction = DirectedInterval.from_decimal(CORRECTION_RADIUS, precision)
    neutral_radius = Decimal(
        str(parent.riesz["local_complex_exclusion_radius_lower"])
    )
    positive_center = Decimal(str(parent.root["root_disk_center_binary64"]))
    positive_radius = Decimal(str(parent.root["root_disk_radius"]))
    phase_upper = Decimal(decimal_upper(pi_interval(precision).upper))
    disks_disjoint = positive_center - positive_radius > neutral_radius
    disks_inside = (
        positive_center - positive_radius > 0
        and positive_center + positive_radius < OUTER_REAL_PART
        and positive_radius < phase_upper
    )
    if not disks_disjoint or not disks_inside:
        raise ArithmeticError("the two local inner disks are not disjoint and interior")
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        maximum_slow_real = (
            gmpy2.mpfr(str(OUTER_REAL_PART))
            + (base.period.upper + correction.upper)
            * base.parameters["epsilon"].upper
        )
        nearest_tail_frequency = 129 * pi_interval(precision).lower
        monotonicity = (
            (DirectedInterval.from_decimal(2, precision).sqrt().upper - 1)
            * maximum_slow_real
            < nearest_tail_frequency
        )
    if not monotonicity:
        raise ArithmeticError("the inner shifted tail inverse is not monotone")

    roots = _root_rectangles(phase_upper)
    pending = list(reversed(roots))
    leaves: list[CoverLeaf] = []
    neutral_count = 0
    positive_count = 0
    neumann_count = 0
    neutral_first: int | None = None
    positive_first: int | None = None
    worst: WorstCoverCell | None = None
    blocking: WorstCoverCell | None = None
    processed = 0
    deepest = 0

    def prioritise_unhit_local_disks() -> None:
        """Follow the two disk-containing chains before broad calibration.

        This changes only traversal order.  Cell tests, splits, and hence a
        completed minimal dyadic tree are independent of this priority.
        """

        if neutral_first is not None and positive_first is not None:
            return

        def contains_real_point(rectangle: Rectangle, point: Decimal) -> bool:
            return (
                rectangle.sigma_lower <= point <= rectangle.sigma_upper
                and rectangle.phase_lower <= 0 <= rectangle.phase_upper
            )

        pending.sort(
            key=lambda rectangle: (
                neutral_first is None
                and contains_real_point(rectangle, Decimal(0)),
                positive_first is None
                and contains_real_point(rectangle, positive_center),
                len(rectangle.path),
            )
        )

    def classify_local(rectangle: Rectangle) -> bool:
        nonlocal neutral_count, positive_count, processed, neutral_first, positive_first
        if rectangle_strictly_inside_origin_disk(rectangle, neutral_radius):
            leaves.append(
                CoverLeaf(
                    rectangle.root_id,
                    rectangle.path,
                    "riesz_neutral_disk",
                    "0",
                    "0",
                    "0",
                )
            )
            neutral_count += 1
            if neutral_first is None:
                neutral_first = processed + 1
            processed += 1
            return True
        if _rectangle_strictly_inside_positive_disk(
            rectangle, positive_center, positive_radius
        ):
            leaves.append(
                CoverLeaf(
                    rectangle.root_id,
                    rectangle.path,
                    "grushin_positive_root_disk",
                    "0",
                    "0",
                    "0",
                )
            )
            positive_count += 1
            if positive_first is None:
                positive_first = processed + 1
            processed += 1
            return True
        return False

    def record_cell(rectangle: Rectangle, depth: int, bounds: Any) -> None:
        nonlocal neumann_count, worst, blocking, processed
        processed += 1
        if bounds.validated:
            leaves.append(bounds.leaf)
            neumann_count += 1
            if worst is None or Decimal(bounds.worst.contraction_upper) > Decimal(
                worst.contraction_upper
            ):
                worst = bounds.worst
        else:
            if depth >= maximum_depth:
                blocking = bounds.worst
                pending.append(rectangle)
            else:
                first, second = split_rectangle(rectangle)
                pending.extend((second, first))

    if parallel_workers == 1:
        while pending and processed < maximum_processed_cells:
            prioritise_unhit_local_disks()
            rectangle = pending.pop()
            depth = len(rectangle.path) // 2
            deepest = max(deepest, depth)
            if classify_local(rectangle):
                continue
            bounds = validate_cell(
                rectangle,
                candidate,
                base,
                correction,
                precision,
                threshold,
            )
            record_cell(rectangle, depth, bounds)
            if blocking is not None:
                break
            if progress is not None and processed % 100 == 0:
                progress(processed, len(leaves), len(pending))
    else:
        global _CELL_WORKER_STATE
        if "fork" not in multiprocessing.get_all_start_methods():
            raise RuntimeError("the parallel rigorous cover requires fork workers")
        _CELL_WORKER_STATE = (
            candidate,
            base,
            correction,
            precision,
            threshold,
        )
        context = multiprocessing.get_context("fork")
        try:
            with ProcessPoolExecutor(
                max_workers=parallel_workers,
                mp_context=context,
            ) as executor:
                while pending and processed < maximum_processed_cells:
                    prioritise_unhit_local_disks()
                    batch: list[tuple[Rectangle, int]] = []
                    batch_limit = 2 * parallel_workers
                    while (
                        pending
                        and processed + len(batch) < maximum_processed_cells
                        and len(batch) < batch_limit
                    ):
                        rectangle = pending.pop()
                        depth = len(rectangle.path) // 2
                        deepest = max(deepest, depth)
                        if classify_local(rectangle):
                            continue
                        batch.append((rectangle, depth))
                    if batch:
                        results = executor.map(
                            _parallel_validate_cell,
                            (rectangle for rectangle, _ in batch),
                            chunksize=1,
                        )
                        for (rectangle, depth), bounds in zip(
                            batch, results, strict=True
                        ):
                            record_cell(rectangle, depth, bounds)
                    if blocking is not None:
                        break
                    if progress is not None:
                        progress(processed, len(leaves), len(pending))
        finally:
            _CELL_WORKER_STATE = None

    complete = not pending
    root_ids = tuple(root.root_id for root in roots)
    prefix = complete and prefix_complete(leaves, root_ids)
    strict = bool(leaves) and all(
        Decimal(leaf.contraction_upper) < 1 for leaf in leaves
    )
    maximum = max(
        (Decimal(leaf.contraction_upper) for leaf in leaves),
        default=None,
    )
    normalized = sum(
        (
            Fraction(1, 2 ** (len(leaf.path) // 2))
            for leaf in leaves
        ),
        Fraction(0),
    )
    normalized_text = (
        str(normalized.numerator)
        if normalized.denominator == 1
        else f"{normalized.numerator}/{normalized.denominator}"
    )
    covered = (
        complete
        and prefix
        and strict
        and monotonicity
        and normalized == len(roots)
        and neutral_count > 0
        and positive_count > 0
        and neumann_count > 0
    )
    stress = (
        _stress_replay(parent.orbit, worst, phase_upper)
        if covered
        else _StressReplay(STRESS_PRECISION_BITS, None, None, False)
    )
    covered = covered and stress.strict
    digest = leaf_digest(leaves)
    pending_by_root = {
        root.root_id: sum(
            rectangle.root_id == root.root_id for rectangle in pending
        )
        for root in roots
    }
    if (
        covered
        and isinstance(EXPECTED_COMPLETE_LEAF_PARTITION_SHA256, str)
        and digest != EXPECTED_COMPLETE_LEAF_PARTITION_SHA256
    ):
        raise ValueError("the registered inner leaf partition changed")
    failure = None
    if not covered:
        failure = (
            f"inner compact cover incomplete: processed={processed}, "
            f"accepted={len(leaves)}, pending={len(pending)}; "
            + (
                f"blocking contraction={blocking.contraction_upper}; "
                if blocking is not None
                else ""
            )
            + "the total inner index remains open"
        )
    theorem_flags = {name: covered for name in TRUE_ON_COMPLETE}
    return InnerRightHalfCoverCertificate(
        schema_id=SCHEMA_ID,
        model_id=MODEL_ID,
        branch=BRANCH,
        riesz_result_sha256=EXPECTED_RIESZ_RESULT_SHA256,
        floquet_transfer_result_sha256=(
            EXPECTED_FLOQUET_TRANSFER_RESULT_SHA256
        ),
        inner_root_result_sha256=EXPECTED_INNER_ROOT_RESULT_SHA256,
        inner_orbit_result=parent.evidence.source_result,
        inner_orbit_result_sha256=EXPECTED_INNER_ORBIT_RESULT_SHA256,
        cover_engine_source_sha256=_sha256_path(
            repository
            / "src/canard_control/leaky_floquet_compact_cover_engine.py"
        ),
        candidate_fingerprint=parent.evidence.candidate_fingerprint,
        source_orbit_correction_radius=parent.evidence.correction_radius,
        correction_radius=CORRECTION_RADIUS,
        precision_bits=precision,
        norm_id="complex-component-wiener-l1-split-re-im",
        fourier_cutoff=FOURIER_CUTOFF,
        coefficient_support_half_bandwidth=COEFFICIENT_SUPPORT_RADIUS,
        complex_finite_dimension=2 * (2 * FOURIER_CUTOFF + 1),
        outer_real_part=str(OUTER_REAL_PART),
        upper_phase_lower="0",
        upper_phase_upper=format(phase_upper, "f"),
        neutral_disk_radius=format(neutral_radius, "f"),
        positive_disk_center=format(positive_center, "f"),
        positive_disk_radius=format(positive_radius, "f"),
        root_rectangle_count=len(roots),
        accepted_leaf_count=len(leaves),
        neutral_disk_leaf_count=neutral_count,
        positive_disk_leaf_count=positive_count,
        neumann_leaf_count=neumann_count,
        processed_cell_count=processed,
        pending_cell_count=len(pending),
        pending_low_unit_count=pending_by_root["low_unit"],
        pending_right_low_count=pending_by_root["right_low"],
        pending_upper_band_count=pending_by_root["upper_band"],
        neutral_disk_first_processed_cell=neutral_first,
        positive_disk_first_processed_cell=positive_first,
        accepted_normalized_root_fraction=normalized_text,
        maximum_depth=deepest,
        acceptance_threshold=str(threshold),
        maximum_contraction_upper=(
            None if maximum is None else format(maximum, "f")
        ),
        minimum_contraction_margin_lower=(
            None if maximum is None else _margin(format(maximum, "f"))
        ),
        stress_replay_precision_bits=stress.precision_bits,
        worst_cell_stress_contraction_upper=stress.same_cell_upper,
        worst_cell_finer_split_stress_maximum_contraction_upper=(
            stress.finer_split_upper
        ),
        worst_cell_finer_split_stress_strict=stress.strict,
        leaf_partition_sha256=digest,
        neutral_disk_characteristic_value_count=(1 if covered else None),
        positive_disk_characteristic_value_count=(1 if covered else None),
        compact_keyhole_characteristic_value_count=(0 if covered else None),
        directed_closed_right_half_characteristic_value_count=(
            2 if covered else None
        ),
        closed_right_half_nontranslation_characteristic_value_count=(
            1 if covered else None
        ),
        directed_unstable_multiplier_count=1 if covered else None,
        **{name: True for name in STRUCTURAL_TRUE},
        **theorem_flags,
        **{name: False for name in ALWAYS_FALSE},
        leaves=tuple(sorted(leaves, key=lambda leaf: (leaf.root_id, leaf.path))),
        worst_cell=worst if worst is not None else blocking,
        failure_reason=failure,
    )


def build_inner_right_half_result(
    repository: Path,
    *,
    maximum_processed_cells: int = MAXIMUM_PROCESSED_CELLS,
    parallel_workers: int = 1,
    replay_parents: bool = True,
    progress: Callable[[int, int, int], None] | None = None,
) -> dict[str, Any]:
    repository = repository.resolve()
    certificate = asdict(
        build_inner_right_half_cover(
            repository,
            maximum_processed_cells=maximum_processed_cells,
            parallel_workers=parallel_workers,
            replay_parents=replay_parents,
            progress=progress,
        )
    )
    # Canonical JSON containers make the in-memory validator identical to the
    # tracked JSON replay (notably for the tuple of dataclass leaves).
    certificate = json.loads(json.dumps(certificate, allow_nan=False))
    sources = {
        relative: _sha256_path(repository / relative)
        for relative in SOURCE_MANIFEST
    }
    result: dict[str, Any] = {
        "certificate": certificate,
        "scope": {
            "center_parameter_inner_unstable_multiplier_count": certificate[
                "directed_unstable_multiplier_count"
            ],
            "inner_no_other_right_half_roots_validated": certificate[
                "inner_no_other_right_half_roots_validated"
            ],
            "inner_saddle_floquet_index_validated": certificate[
                "inner_saddle_floquet_index_validated"
            ],
            "common_parameter_box_inner_index_validated": False,
            "inner_stable_manifold_validated": False,
            "physical_pulse_onset_validated": False,
        },
    }
    result["manifest"] = {
        "schema_id": SCHEMA_ID,
        "result": RESULT_RELATIVE_PATH,
        "default_command": DEFAULT_COMMAND,
        "arithmetic_scope": ARITHMETIC_SCOPE,
        "certificate_sha256": canonical_sha256(certificate),
        "source_sha256": sources,
        "riesz_result": RIESZ_RESULT_RELATIVE_PATH,
        "riesz_result_sha256": _sha256_path(
            repository / RIESZ_RESULT_RELATIVE_PATH
        ),
        "inner_root_result": INNER_ROOT_RESULT_RELATIVE_PATH,
        "inner_root_result_sha256": _sha256_path(
            repository / INNER_ROOT_RESULT_RELATIVE_PATH
        ),
        "floquet_transfer_result": FLOQUET_TRANSFER_RESULT_RELATIVE_PATH,
        "floquet_transfer_result_sha256": _sha256_path(
            repository / FLOQUET_TRANSFER_RESULT_RELATIVE_PATH
        ),
        "inner_orbit_result": certificate["inner_orbit_result"],
        "inner_orbit_result_sha256": _sha256_path(
            repository / certificate["inner_orbit_result"]
        ),
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "gmpy2": gmpy2.__version__,
            "mpfr": gmpy2.mpfr_version(),
        },
    }
    return result


def validate_inner_right_half_result(
    payload: Mapping[str, Any],
    repository: Path,
    *,
    validate_parents: bool = True,
) -> None:
    if not isinstance(payload, Mapping) or set(payload) != {
        "certificate",
        "scope",
        "manifest",
    }:
        raise ValueError("the inner right-half result has the wrong schema")
    certificate = _mapping(payload.get("certificate"), "inner cover certificate")
    scope = _mapping(payload.get("scope"), "inner cover scope")
    manifest = _mapping(payload.get("manifest"), "inner cover manifest")
    if set(certificate) != {
        field.name for field in fields(InnerRightHalfCoverCertificate)
    }:
        raise ValueError("the inner right-half certificate schema changed")
    for name in STRUCTURAL_TRUE:
        if certificate.get(name) is not True:
            raise ValueError(f"an inner structural gate is absent: {name}")
    for name in ALWAYS_FALSE:
        if certificate.get(name) is not False:
            raise ValueError(f"an open inner nonlinear claim was promoted: {name}")
    fixed = {
        "schema_id": SCHEMA_ID,
        "model_id": MODEL_ID,
        "branch": BRANCH,
        "riesz_result_sha256": EXPECTED_RIESZ_RESULT_SHA256,
        "floquet_transfer_result_sha256": (
            EXPECTED_FLOQUET_TRANSFER_RESULT_SHA256
        ),
        "inner_root_result_sha256": EXPECTED_INNER_ROOT_RESULT_SHA256,
        "inner_orbit_result_sha256": EXPECTED_INNER_ORBIT_RESULT_SHA256,
        "source_orbit_correction_radius": "1e-5",
        "correction_radius": CORRECTION_RADIUS,
        "precision_bits": PRECISION_BITS,
        "norm_id": "complex-component-wiener-l1-split-re-im",
        "fourier_cutoff": FOURIER_CUTOFF,
        "coefficient_support_half_bandwidth": COEFFICIENT_SUPPORT_RADIUS,
        "complex_finite_dimension": 258,
        "outer_real_part": str(OUTER_REAL_PART),
        "upper_phase_lower": "0",
        "root_rectangle_count": 3,
        "acceptance_threshold": str(ACCEPTANCE_THRESHOLD),
        "stress_replay_precision_bits": STRESS_PRECISION_BITS,
    }
    if any(certificate.get(name) != value for name, value in fixed.items()):
        raise ValueError("the inner right-half fixed theorem data changed")
    repository = repository.resolve()
    parents = _validate_parents(
        repository, replay_parents=validate_parents
    )
    if certificate.get("candidate_fingerprint") != (
        parents.evidence.candidate_fingerprint
    ):
        raise ValueError("the inner cover candidate fingerprint changed")
    if certificate.get("inner_orbit_result") != parents.evidence.source_result:
        raise ValueError("the inner cover source-orbit path changed")
    expected_geometry = {
        "upper_phase_upper": format(
            Decimal(decimal_upper(pi_interval(PRECISION_BITS).upper)), "f"
        ),
        "neutral_disk_radius": str(
            parents.riesz["local_complex_exclusion_radius_lower"]
        ),
        "positive_disk_center": str(
            parents.root["root_disk_center_binary64"]
        ),
        "positive_disk_radius": str(parents.root["root_disk_radius"]),
    }
    if any(
        certificate.get(name) != value
        for name, value in expected_geometry.items()
    ):
        raise ValueError("the inner cover domain or local-disk geometry changed")
    engine_path = (
        repository
        / "src/canard_control/leaky_floquet_compact_cover_engine.py"
    )
    if certificate.get("cover_engine_source_sha256") != _sha256_path(engine_path):
        raise ValueError("the reused full-operator cover engine changed")
    leaves_value = certificate.get("leaves")
    if not isinstance(leaves_value, list):
        raise ValueError("the inner cover leaves must be a JSON list")
    leaf_fields = {field.name for field in fields(CoverLeaf)}
    leaves: list[CoverLeaf] = []
    for value in leaves_value:
        record = _mapping(value, "inner cover leaf")
        if set(record) != leaf_fields:
            raise ValueError("an inner cover leaf schema changed")
        leaves.append(CoverLeaf(**dict(record)))
    if len(leaves) != certificate.get("accepted_leaf_count"):
        raise ValueError("the inner accepted leaf count changed")
    if leaves != sorted(leaves, key=lambda leaf: (leaf.root_id, leaf.path)):
        raise ValueError("the inner leaves are not in canonical order")
    if len({(leaf.root_id, leaf.path) for leaf in leaves}) != len(leaves):
        raise ValueError("the inner cover leaves are not unique")
    if leaf_digest(leaves) != certificate.get("leaf_partition_sha256"):
        raise ValueError("the inner leaf digest changed")
    phase_upper = Decimal(str(certificate["upper_phase_upper"]))
    roots = {root.root_id: root for root in _root_rectangles(phase_upper)}
    neutral_radius = Decimal(str(certificate["neutral_disk_radius"]))
    positive_center = Decimal(str(certificate["positive_disk_center"]))
    positive_radius = Decimal(str(certificate["positive_disk_radius"]))
    if not (
        positive_center - positive_radius > neutral_radius
        and positive_center - positive_radius > 0
        and positive_center + positive_radius < OUTER_REAL_PART
        and positive_radius < phase_upper
    ):
        raise ValueError("the registered local disks overlap or leave the strip")
    neutral_count = 0
    positive_count = 0
    neumann_count = 0
    for leaf in leaves:
        if leaf.root_id not in roots:
            raise ValueError("an inner leaf has an unknown root rectangle")
        rectangle = rectangle_from_path(roots[leaf.root_id], leaf.path)
        contraction = Decimal(leaf.contraction_upper)
        finite = Decimal(leaf.finite_input_column_sum_upper)
        tail = Decimal(leaf.tail_input_column_sum_upper)
        if min(contraction, finite, tail) < 0:
            raise ValueError("an inner leaf bound became negative")
        in_neutral = rectangle_strictly_inside_origin_disk(
            rectangle, neutral_radius
        )
        in_positive = _rectangle_strictly_inside_positive_disk(
            rectangle, positive_center, positive_radius
        )
        if leaf.proof_kind == "riesz_neutral_disk":
            neutral_count += 1
            if not in_neutral or (contraction, finite, tail) != (Decimal(0),) * 3:
                raise ValueError("a neutral-disk leaf is invalid")
        elif leaf.proof_kind == "grushin_positive_root_disk":
            positive_count += 1
            if not in_positive or (contraction, finite, tail) != (Decimal(0),) * 3:
                raise ValueError("a positive-disk leaf is invalid")
        elif leaf.proof_kind == "full_operator_neumann":
            neumann_count += 1
            if in_neutral or in_positive:
                raise ValueError("a local-disk rectangle was misclassified")
            if contraction != max(finite, tail) or not Decimal(0) < contraction < 1:
                raise ValueError("an inner Neumann leaf is not strict")
            if contraction > ACCEPTANCE_THRESHOLD:
                raise ValueError("an inner Neumann leaf exceeds its threshold")
        else:
            raise ValueError("an inner leaf has an unknown proof kind")
    if (
        neutral_count != certificate.get("neutral_disk_leaf_count")
        or positive_count != certificate.get("positive_disk_leaf_count")
        or neumann_count != certificate.get("neumann_leaf_count")
    ):
        raise ValueError("the inner proof-kind counts changed")
    pending_counts = (
        int(certificate["pending_low_unit_count"]),
        int(certificate["pending_right_low_count"]),
        int(certificate["pending_upper_band_count"]),
    )
    if min(pending_counts) < 0 or sum(pending_counts) != int(
        certificate["pending_cell_count"]
    ):
        raise ValueError("the inner pending-region counts changed")
    for leaf_count, first_name in (
        (neutral_count, "neutral_disk_first_processed_cell"),
        (positive_count, "positive_disk_first_processed_cell"),
    ):
        first = certificate[first_name]
        if (leaf_count == 0) != (first is None):
            raise ValueError("an inner local-disk first-hit marker changed")
        if first is not None and not (
            1 <= int(first) <= int(certificate["processed_cell_count"])
        ):
            raise ValueError("an inner local-disk first-hit marker is invalid")
    complete = certificate.get("pending_cell_count") == 0
    prefix = complete and prefix_complete(leaves, tuple(roots))
    promoted = bool(certificate.get("inner_no_other_right_half_roots_validated"))
    if promoted:
        if not isinstance(EXPECTED_COMPLETE_LEAF_PARTITION_SHA256, str):
            raise ValueError("the complete inner leaf digest is not registered")
        if certificate.get("leaf_partition_sha256") != (
            EXPECTED_COMPLETE_LEAF_PARTITION_SHA256
        ):
            raise ValueError("the registered inner leaf digest changed")
        if not prefix:
            raise ValueError("the promoted inner partition is incomplete")
        if certificate.get("accepted_normalized_root_fraction") != "3":
            raise ValueError("the promoted inner forest has an area gap")
        if certificate.get("processed_cell_count") != 2 * len(leaves) - len(roots):
            raise ValueError("the promoted inner binary-forest count changed")
        if certificate.get("maximum_depth") != max(
            len(leaf.path) // 2 for leaf in leaves
        ):
            raise ValueError("the promoted inner maximum depth changed")
        if neutral_count <= 0 or positive_count <= 0 or neumann_count <= 0:
            raise ValueError("the promoted inner proof partition is empty")
        maximum = max(Decimal(leaf.contraction_upper) for leaf in leaves)
        if format(maximum, "f") != certificate.get("maximum_contraction_upper"):
            raise ValueError("the inner maximum contraction changed")
        if _margin(format(maximum, "f")) != certificate.get(
            "minimum_contraction_margin_lower"
        ):
            raise ValueError("the inner minimum contraction margin changed")
        if certificate.get("worst_cell_finer_split_stress_strict") is not True:
            raise ValueError("the inner stress replay is not strict")
        if any(certificate.get(name) is not True for name in TRUE_ON_COMPLETE):
            raise ValueError("a completed inner theorem flag is absent")
        expected_counts = {
            "neutral_disk_characteristic_value_count": 1,
            "positive_disk_characteristic_value_count": 1,
            "compact_keyhole_characteristic_value_count": 0,
            "directed_closed_right_half_characteristic_value_count": 2,
            "closed_right_half_nontranslation_characteristic_value_count": 1,
            "directed_unstable_multiplier_count": 1,
        }
        if any(
            certificate.get(name) != value
            for name, value in expected_counts.items()
        ):
            raise ValueError("an inner analytic characteristic count changed")
        if (
            certificate["neutral_disk_characteristic_value_count"]
            + certificate["positive_disk_characteristic_value_count"]
            + certificate["compact_keyhole_characteristic_value_count"]
            != certificate[
                "directed_closed_right_half_characteristic_value_count"
            ]
            or certificate[
                "directed_closed_right_half_characteristic_value_count"
            ]
            - certificate["neutral_disk_characteristic_value_count"]
            != certificate[
                "closed_right_half_nontranslation_characteristic_value_count"
            ]
        ):
            raise ValueError("the inner analytic count is not additive")
    else:
        if any(certificate.get(name) is not False for name in TRUE_ON_COMPLETE):
            raise ValueError("an incomplete inner cover promoted a theorem")
        count_fields = (
            "neutral_disk_characteristic_value_count",
            "positive_disk_characteristic_value_count",
            "compact_keyhole_characteristic_value_count",
            "directed_closed_right_half_characteristic_value_count",
            "closed_right_half_nontranslation_characteristic_value_count",
            "directed_unstable_multiplier_count",
        )
        if any(certificate.get(name) is not None for name in count_fields):
            raise ValueError("an incomplete inner cover inserted a root count")
    expected_scope = {
        "center_parameter_inner_unstable_multiplier_count": certificate[
            "directed_unstable_multiplier_count"
        ],
        "inner_no_other_right_half_roots_validated": promoted,
        "inner_saddle_floquet_index_validated": certificate[
            "inner_saddle_floquet_index_validated"
        ],
        "common_parameter_box_inner_index_validated": False,
        "inner_stable_manifold_validated": False,
        "physical_pulse_onset_validated": False,
    }
    if dict(scope) != expected_scope:
        raise ValueError("the inner cover scope ledger changed")
    expected_manifest_fields = {
        "schema_id",
        "result",
        "default_command",
        "arithmetic_scope",
        "certificate_sha256",
        "source_sha256",
        "riesz_result",
        "riesz_result_sha256",
        "inner_root_result",
        "inner_root_result_sha256",
        "floquet_transfer_result",
        "floquet_transfer_result_sha256",
        "inner_orbit_result",
        "inner_orbit_result_sha256",
        "environment",
    }
    if set(manifest) != expected_manifest_fields:
        raise ValueError("the inner cover manifest schema changed")
    if manifest.get("certificate_sha256") != canonical_sha256(certificate):
        raise ValueError("the inner cover certificate digest changed")
    source_hashes = _mapping(manifest.get("source_sha256"), "source manifest")
    if set(source_hashes) != set(SOURCE_MANIFEST):
        raise ValueError("the inner cover source set changed")
    for relative in SOURCE_MANIFEST:
        if source_hashes.get(relative) != _sha256_path(repository / relative):
            raise ValueError(f"the inner cover source changed: {relative}")
    parent_paths = {
        "riesz_result": RIESZ_RESULT_RELATIVE_PATH,
        "inner_root_result": INNER_ROOT_RESULT_RELATIVE_PATH,
        "floquet_transfer_result": FLOQUET_TRANSFER_RESULT_RELATIVE_PATH,
        "inner_orbit_result": str(certificate["inner_orbit_result"]),
    }
    for name, relative in parent_paths.items():
        if manifest.get(name) != relative:
            raise ValueError(f"the inner cover parent path changed: {name}")
        if manifest.get(name + "_sha256") != _sha256_path(repository / relative):
            raise ValueError(f"the inner cover parent hash changed: {name}")


__all__ = [
    "ACCEPTANCE_THRESHOLD",
    "ALWAYS_FALSE",
    "COEFFICIENT_SUPPORT_RADIUS",
    "DEFAULT_COMMAND",
    "EXPECTED_COMPLETE_LEAF_PARTITION_SHA256",
    "FOURIER_CUTOFF",
    "InnerRightHalfCoverCertificate",
    "MAXIMUM_PROCESSED_CELLS",
    "RESULT_RELATIVE_PATH",
    "SCHEMA_ID",
    "SOURCE_MANIFEST",
    "STRUCTURAL_TRUE",
    "TRUE_ON_COMPLETE",
    "build_inner_right_half_cover",
    "build_inner_right_half_result",
    "canonical_sha256",
    "validate_inner_right_half_result",
]
