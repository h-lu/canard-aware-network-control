"""Quantitative center-inner Poincare stable spectral gap.

The audited right-half theorem already counts the simple translation value
and the simple positive value.  This module adds a source-bound full-operator
cover of the thin strip ``-gamma <= Re s <= 0``.  A full complex neutral
disk, rather than the earlier right half-disk, owns the only value on the
``Re s = 0`` seam.  The open negative strip is therefore zero-free and the
stable multipliers satisfy ``rho_s <= exp(-gamma) < 1``.

This is a center-orbit spectral theorem.  It is not a parameter-box,
spectral-projection, invariant-manifold, nonlinear pulse, or onset theorem.
"""

from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor
from dataclasses import asdict, dataclass, fields
from decimal import Decimal, localcontext
from fractions import Fraction
from hashlib import sha256
import json
import multiprocessing
import os
from pathlib import Path
import platform
from typing import Any, Callable, Mapping

import gmpy2
import numpy as np
import scipy

from canard_control.directed_interval import (
    DirectedInterval,
    decimal_lower,
    decimal_upper,
    pi_interval,
)
from canard_control.floquet_cover_arithmetic import _binary_environment_checked
from canard_control.leaky_floquet_compact_cover_engine import (
    BinaryCandidate,
    CoverLeaf,
    Rectangle,
    WorstCoverCell,
    leaf_digest,
    prefix_complete,
    rectangle_from_path,
    split_rectangle,
)
from canard_control.leaky_floquet_inner_right_half_cover import (
    RESULT_RELATIVE_PATH as RIGHT_HALF_RESULT_RELATIVE_PATH,
    _prepare_inner_candidate,
    canonical_sha256,
    validate_inner_right_half_result,
)
from canard_control.leaky_floquet_left_strip_cover_engine import (
    _left_delay_modulus_upper,
    validate_left_cell,
)
from canard_control.leaky_floquet_transfer import (
    RESULT_RELATIVE_PATH as FLOQUET_TRANSFER_RESULT_RELATIVE_PATH,
    load_validated_leaky_orbit_evidence,
    validate_leaky_floquet_transfer_artifact,
)
from canard_control.leaky_periodic_validation import (
    _build_leaky_base_sequences,
)


SCHEMA_ID = "leaky-floquet-inner-stable-gap-v1"
MODEL_ID = "autonomous-leaky-recovery-two-delay-fhn-bistable-proposal"
BRANCH = "inner_saddle_candidate"
SOURCE_RELATIVE_PATH = (
    "src/canard_control/leaky_floquet_inner_stable_gap.py"
)
GENERATOR_RELATIVE_PATH = (
    "experiments/leaky_floquet_inner_stable_gap.py"
)
NOTE_RELATIVE_PATH = "docs/leaky-floquet-inner-stable-gap.md"
TEST_RELATIVE_PATH = "tests/test_leaky_floquet_inner_stable_gap.py"
RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_floquet_inner_stable_gap.json"
)
DEFAULT_COMMAND = (
    "OPENBLAS_NUM_THREADS=1 PYTHONPATH=build/testdeps:src /usr/bin/python3 "
    "experiments/leaky_floquet_inner_stable_gap.py --workers 12"
)
ARITHMETIC_SCOPE = (
    "160-bit outward MPFR full-operator cover on the center-inner left "
    "principal strip; physical output-row phases with exp(alpha*gamma) "
    "left-strip factors; source-bound radius-1e-12 orbit; a full complex "
    "neutral uniqueness disk; exact dyadic seams; and 256-bit stress replay"
)

PRECISION_BITS = 160
STRESS_PRECISION_BITS = 256
FOURIER_CUTOFF = 64
GAMMA = Decimal("0.001")
NEUTRAL_FULL_DISK_RADIUS = Decimal("0.0039")
LOW_SEAM = Decimal(1)
CORRECTION_RADIUS = "1e-12"
ACCEPTANCE_THRESHOLD = Decimal("0.995")
MAXIMUM_PROCESSED_CELLS = 20000
MAXIMUM_DEPTH = 96
PINNED_OPENBLAS_NUM_THREADS = "1"
EXPECTED_COMPLETE_LEAF_PARTITION_SHA256 = (
    "7663d9147c5c1af663a37420b6894da9f973ba33b2c13e8ff998554f5f5118e6"
)
EXPECTED_CERTIFICATE_SHA256 = (
    "9bd03dac1a043a13deeff9c387d9dba2605e35bc7777442ee4f8746710149c15"
)

EXPECTED_RIGHT_HALF_RESULT_SHA256 = (
    "f0458acf59b8fad96e43f204df37fd8d37f356ebbf67701180c8ff31c668739a"
)
EXPECTED_FLOQUET_TRANSFER_RESULT_SHA256 = (
    "5a3709ec792b29ed41533101245b13b3d35084ae508bdd1d420728200a5a5b16"
)

STRUCTURAL_TRUE = (
    "source_validated_inner_orbit_ball_used",
    "source_validated_right_half_count_used",
    "source_validated_neutral_simplicity_used",
    "source_validated_compact_history_monodromy_used",
    "history_spectrum_to_fourier_characteristic_values_bridge_used",
    "physical_unshifted_coefficient_output_phase_used",
    "shifted_coefficient_input_phase_equivalence_inherited",
    "negative_real_delay_modulus_restored",
    "negative_real_tail_frequency_absolute_value_restored",
    "negative_real_delay_taylor_factor_restored",
    "negative_real_full_disk_farthest_corner_used",
    "full_mode_128_coefficient_support_used",
    "complex_split_wiener_norm_used",
)

TRUE_ON_COMPLETE = (
    "neutral_full_complex_disk_uniqueness_validated",
    "neutral_full_disk_boundary_zero_free_validated",
    "neutral_root_owned_by_right_half_seam_validated",
    "left_upper_half_exact_partition_validated",
    "all_left_nonlocal_cells_full_operator_neumann_validated",
    "left_open_strip_zero_free_validated",
    "lower_left_strip_excluded_by_real_conjugacy",
    "right_half_parent_and_left_strip_union_validated",
    "inner_no_other_roots_in_shifted_closed_strip_validated",
    "poincare_stable_spectral_radius_bound_validated",
    "quantitative_inner_stable_spectral_gap_validated",
)

ALWAYS_FALSE = (
    "common_parameter_box_stable_gap_validated",
    "stable_spectral_projection_constructed",
    "inner_stable_manifold_validated",
    "inner_nonlinear_saddle_block_validated",
    "asynchronous_network_stable_gap_validated",
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
    "src/canard_control/leaky_floquet_inner_right_half_cover.py",
    "src/canard_control/leaky_floquet_left_strip_cover_engine.py",
    "src/canard_control/leaky_floquet_transfer.py",
    "src/canard_control/leaky_periodic_validation.py",
)


@dataclass(frozen=True)
class _ParentData:
    orbit: Any
    evidence: Any
    right: Mapping[str, Any]
    transfer: Mapping[str, Any]


@dataclass(frozen=True)
class _NeutralDiskBounds:
    delay_exponential_modulus_upper: str
    first_order_coefficient_upper: str
    second_order_coefficient_upper: str
    first_neutral_contraction_upper: str
    second_neutral_contraction_upper: str


@dataclass(frozen=True)
class _StressReplay:
    precision_bits: int
    same_cell_upper: str | None
    finer_split_upper: str | None
    strict: bool


@dataclass(frozen=True)
class InnerStableGapCertificate:
    schema_id: str
    model_id: str
    branch: str
    right_half_result_sha256: str
    floquet_transfer_result_sha256: str
    inner_orbit_result: str
    inner_orbit_result_sha256: str
    candidate_fingerprint: str
    left_engine_source_sha256: str
    correction_radius: str
    binary_blas_thread_count: int
    precision_bits: int
    norm_id: str
    fourier_cutoff: int
    coefficient_support_half_bandwidth: int
    gamma_lower: str
    stable_multiplier_modulus_upper: str
    one_minus_stable_multiplier_modulus_lower: str
    neutral_full_disk_radius: str
    neutral_delay_exponential_modulus_upper: str
    neutral_first_order_coefficient_upper: str
    neutral_second_order_coefficient_upper: str
    neutral_first_contraction_upper: str
    neutral_second_contraction_upper: str
    maximum_left_delay_modulus_upper: str
    upper_phase_lower: str
    upper_phase_upper: str
    root_rectangle_count: int
    accepted_leaf_count: int
    neutral_disk_leaf_count: int
    neutral_root_owner_leaf_count: int
    neumann_leaf_count: int
    processed_cell_count: int
    pending_cell_count: int
    pending_left_low_count: int
    pending_left_upper_count: int
    neutral_disk_first_processed_cell: int | None
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
    left_closed_strip_characteristic_value_count: int | None
    left_open_strip_characteristic_value_count: int | None
    shifted_closed_strip_characteristic_value_count: int | None
    shifted_closed_strip_nontranslation_characteristic_value_count: int | None
    stable_multiplier_spectral_radius_upper: str | None
    source_validated_inner_orbit_ball_used: bool
    source_validated_right_half_count_used: bool
    source_validated_neutral_simplicity_used: bool
    source_validated_compact_history_monodromy_used: bool
    history_spectrum_to_fourier_characteristic_values_bridge_used: bool
    physical_unshifted_coefficient_output_phase_used: bool
    shifted_coefficient_input_phase_equivalence_inherited: bool
    negative_real_delay_modulus_restored: bool
    negative_real_tail_frequency_absolute_value_restored: bool
    negative_real_delay_taylor_factor_restored: bool
    negative_real_full_disk_farthest_corner_used: bool
    full_mode_128_coefficient_support_used: bool
    complex_split_wiener_norm_used: bool
    neutral_full_complex_disk_uniqueness_validated: bool
    neutral_full_disk_boundary_zero_free_validated: bool
    neutral_root_owned_by_right_half_seam_validated: bool
    left_upper_half_exact_partition_validated: bool
    all_left_nonlocal_cells_full_operator_neumann_validated: bool
    left_open_strip_zero_free_validated: bool
    lower_left_strip_excluded_by_real_conjugacy: bool
    right_half_parent_and_left_strip_union_validated: bool
    inner_no_other_roots_in_shifted_closed_strip_validated: bool
    poincare_stable_spectral_radius_bound_validated: bool
    quantitative_inner_stable_spectral_gap_validated: bool
    common_parameter_box_stable_gap_validated: bool
    stable_spectral_projection_constructed: bool
    inner_stable_manifold_validated: bool
    inner_nonlinear_saddle_block_validated: bool
    asynchronous_network_stable_gap_validated: bool
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
        raise RuntimeError("the stable-gap worker was not initialized")
    candidate, base, correction, precision, threshold = _CELL_WORKER_STATE
    return validate_left_cell(
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


def _margin(value: str) -> str:
    with localcontext() as context:
        context.prec = max(160, len(value) + 10)
        return format(Decimal(1) - Decimal(value), "f")


def _require_pinned_binary_blas_environment() -> None:
    """Require the binary inverse/product schedule used by the artifact."""

    if os.environ.get("OPENBLAS_NUM_THREADS") != PINNED_OPENBLAS_NUM_THREADS:
        raise RuntimeError(
            "the inner stable-gap binary replay requires "
            f"OPENBLAS_NUM_THREADS={PINNED_OPENBLAS_NUM_THREADS}; launch a "
            "fresh subprocess so NumPy loads OpenBLAS with that schedule"
        )


def _validate_parents(
    repository: Path,
    *,
    replay_parents: bool,
) -> _ParentData:
    repository = repository.resolve()
    right_path = repository / RIGHT_HALF_RESULT_RELATIVE_PATH
    transfer_path = repository / FLOQUET_TRANSFER_RESULT_RELATIVE_PATH
    if _sha256_path(right_path) != EXPECTED_RIGHT_HALF_RESULT_SHA256:
        raise ValueError("the stable-gap right-half parent changed")
    if _sha256_path(transfer_path) != EXPECTED_FLOQUET_TRANSFER_RESULT_SHA256:
        raise ValueError("the stable-gap neutral transfer parent changed")
    right_payload = _mapping(json.loads(right_path.read_text()), "right parent")
    transfer_payload = _mapping(
        json.loads(transfer_path.read_text()), "transfer parent"
    )
    if replay_parents:
        validate_inner_right_half_result(
            right_payload, repository, validate_parents=True
        )
        validate_leaky_floquet_transfer_artifact(
            transfer_payload, repository, recompute=False
        )
    right = _mapping(right_payload.get("certificate"), "right certificate")
    required_right = {
        "inner_no_other_right_half_roots_validated": True,
        "inner_total_unstable_multiplier_count_validated": True,
        "directed_closed_right_half_characteristic_value_count": 2,
        "closed_right_half_nontranslation_characteristic_value_count": 1,
        "directed_unstable_multiplier_count": 1,
    }
    if any(right.get(name) != value for name, value in required_right.items()):
        raise ValueError("the stable-gap right-half count is incomplete")
    artifact = _mapping(transfer_payload.get("artifact"), "transfer artifact")
    branches = _mapping(artifact.get("branches"), "transfer branches")
    transfer = _mapping(branches.get(BRANCH), "inner transfer branch")
    for name in (
        "monodromy_compact",
        "regularity_bridge_to_history_monodromy",
    ):
        if transfer.get(name) is not True:
            raise ValueError(f"a history-space spectral gate is absent: {name}")
    for name in (
        "translation_multiplier_present",
        "translation_kernel_geometrically_simple_validated",
        "translation_jordan_vector_excluded",
        "neutral_multiplier_algebraically_simple_validated",
    ):
        if transfer.get(name) is not True:
            raise ValueError(f"a neutral full-disk gate is absent: {name}")
    orbit, evidence = load_validated_leaky_orbit_evidence(repository, BRANCH)
    fingerprints = {
        evidence.candidate_fingerprint,
        str(right.get("candidate_fingerprint")),
        str(transfer.get("candidate_fingerprint")),
    }
    if len(fingerprints) != 1:
        raise ValueError("the stable-gap parents use different center orbits")
    if evidence.source_result != right.get("inner_orbit_result"):
        raise ValueError("the stable-gap right parent uses another orbit")
    return _ParentData(orbit, evidence, right, transfer)


def _neutral_full_disk_bounds(
    transfer: Mapping[str, Any],
    precision: int,
) -> _NeutralDiskBounds:
    radius = DirectedInterval.from_decimal(
        format(NEUTRAL_FULL_DISK_RADIUS, "f"), precision
    )
    inverse = DirectedInterval.from_decimal(
        str(transfer["bordered_inverse_norm_upper"]), precision
    )
    first = DirectedInterval.from_decimal(
        str(transfer["bloch_first_order_coefficient_upper"]), precision
    )
    second = DirectedInterval.from_decimal(
        str(transfer["bloch_second_order_coefficient_upper"]), precision
    )
    minimum_period = DirectedInterval.from_decimal(
        str(transfer["minimum_period_lower"]), precision
    )
    maximum_delay = DirectedInterval.from_decimal(
        str(transfer["maximum_delay_upper"]), precision
    )
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        alpha = maximum_delay.upper / minimum_period.lower
        exponential = gmpy2.exp(alpha * radius.upper)
        first_full = 1 + (first.upper - 1) * exponential
        second_full = second.upper * exponential
        first_q = inverse.upper * first_full * radius.upper
        second_q = (
            inverse.upper
            * second_full
            * radius.upper
            / minimum_period.lower
        )
    if not 0 < first_q < 1 or not 0 < second_q < 1:
        raise ArithmeticError("the full complex neutral disk did not close")
    return _NeutralDiskBounds(
        delay_exponential_modulus_upper=decimal_upper(exponential),
        first_order_coefficient_upper=decimal_upper(first_full),
        second_order_coefficient_upper=decimal_upper(second_full),
        first_neutral_contraction_upper=decimal_upper(first_q),
        second_neutral_contraction_upper=decimal_upper(second_q),
    )


def _root_rectangles(phase_upper: Decimal) -> tuple[Rectangle, ...]:
    if not Decimal(0) < LOW_SEAM < phase_upper:
        raise ValueError("the stable-gap phase seam left the principal strip")
    return (
        Rectangle(
            "left_low",
            "",
            -GAMMA,
            Decimal(0),
            Decimal(0),
            LOW_SEAM,
        ),
        Rectangle(
            "left_upper",
            "",
            -GAMMA,
            Decimal(0),
            LOW_SEAM,
            phase_upper,
        ),
    )


def _rectangle_strictly_inside_full_origin_disk(
    rectangle: Rectangle,
    radius: Decimal,
) -> bool:
    """Use the farthest exact corner, including negative real parts."""

    sigma = max(
        abs(Fraction(rectangle.sigma_lower)),
        abs(Fraction(rectangle.sigma_upper)),
    )
    phase = max(
        abs(Fraction(rectangle.phase_lower)),
        abs(Fraction(rectangle.phase_upper)),
    )
    exact_radius = Fraction(radius)
    return sigma * sigma + phase * phase < exact_radius * exact_radius


def _rectangle_contains_origin(rectangle: Rectangle) -> bool:
    return (
        rectangle.sigma_lower <= 0 <= rectangle.sigma_upper
        and rectangle.phase_lower <= 0 <= rectangle.phase_upper
    )


def _stress_replay(
    orbit: Any,
    worst: WorstCoverCell | None,
    phase_upper: Decimal,
) -> _StressReplay:
    if worst is None:
        return _StressReplay(STRESS_PRECISION_BITS, None, None, False)
    roots = {root.root_id: root for root in _root_rectangles(phase_upper)}
    rectangle = rectangle_from_path(roots[worst.root_id], worst.path)
    base = _build_leaky_base_sequences(orbit, STRESS_PRECISION_BITS)
    candidate = _prepare_inner_candidate(
        orbit, base, STRESS_PRECISION_BITS
    )
    correction = DirectedInterval.from_decimal(
        CORRECTION_RADIUS, STRESS_PRECISION_BITS
    )
    threshold = Decimal("0.999999999999")
    same = validate_left_cell(
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
        validate_left_cell(
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


def build_inner_stable_gap_certificate(
    repository: Path,
    *,
    precision: int = PRECISION_BITS,
    acceptance_threshold: str = str(ACCEPTANCE_THRESHOLD),
    maximum_processed_cells: int = MAXIMUM_PROCESSED_CELLS,
    maximum_depth: int = MAXIMUM_DEPTH,
    parallel_workers: int = 1,
    replay_parents: bool = True,
    progress: Callable[[int, int, int], None] | None = None,
) -> InnerStableGapCertificate:
    repository = repository.resolve()
    parent = _validate_parents(repository, replay_parents=replay_parents)
    if precision != PRECISION_BITS:
        raise ValueError("the stable-gap precision is pinned at 160 bits")
    threshold = Decimal(acceptance_threshold)
    if not Decimal(0) < threshold < Decimal(1):
        raise ValueError("the stable-gap threshold must lie in (0,1)")
    if maximum_processed_cells < 1 or maximum_depth < 1 or parallel_workers < 1:
        raise ValueError("the stable-gap budgets must be positive")
    _require_pinned_binary_blas_environment()
    _binary_environment_checked()
    base = _build_leaky_base_sequences(parent.orbit, precision)
    candidate = _prepare_inner_candidate(parent.orbit, base, precision)
    correction = DirectedInterval.from_decimal(CORRECTION_RADIUS, precision)
    neutral = _neutral_full_disk_bounds(parent.transfer, precision)
    phase_upper = Decimal(decimal_upper(pi_interval(precision).upper))
    roots = _root_rectangles(phase_upper)

    maximum_delay_modulus = _left_delay_modulus_upper(
        roots[0], base, correction, precision
    )
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        maximum_real = max(
            DirectedInterval.from_decimal(format(GAMMA, "f"), precision).upper,
            (base.period.upper + correction.upper)
            * base.parameters["epsilon"].upper,
        )
    tail_gap = 129 * pi_interval(precision).lower
    sqrt_two = DirectedInterval.from_decimal(2, precision).sqrt().upper
    tail_monotone = (sqrt_two - 1) * maximum_real < tail_gap
    if not tail_monotone:
        raise ArithmeticError("the left-strip tail inverse is not monotone")

    gamma_box = DirectedInterval.from_decimal(format(GAMMA, "f"), precision)
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        stable_modulus = gmpy2.exp(-gamma_box.lower)
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        stable_margin = 1 - stable_modulus
    if not 0 < stable_modulus < 1 or stable_margin <= 0:
        raise ArithmeticError("the quantitative stable multiplier gap vanished")

    pending = list(reversed(roots))
    leaves: list[CoverLeaf] = []
    neutral_count = 0
    neumann_count = 0
    neutral_first: int | None = None
    worst: WorstCoverCell | None = None
    blocking: WorstCoverCell | None = None
    processed = 0
    deepest = 0

    def prioritise_neutral_chain() -> None:
        if neutral_first is not None:
            return
        pending.sort(
            key=lambda rectangle: (
                rectangle.sigma_lower <= 0 <= rectangle.sigma_upper
                and rectangle.phase_lower <= 0 <= rectangle.phase_upper,
                len(rectangle.path),
            )
        )

    def classify_local(rectangle: Rectangle) -> bool:
        nonlocal neutral_count, neutral_first, processed
        if _rectangle_strictly_inside_full_origin_disk(
            rectangle, NEUTRAL_FULL_DISK_RADIUS
        ):
            leaves.append(
                CoverLeaf(
                    rectangle.root_id,
                    rectangle.path,
                    "neutral_full_complex_disk",
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
        elif depth >= maximum_depth:
            blocking = bounds.worst
            pending.append(rectangle)
        else:
            first, second = split_rectangle(rectangle)
            pending.extend((second, first))

    if parallel_workers == 1:
        while pending and processed < maximum_processed_cells:
            prioritise_neutral_chain()
            rectangle = pending.pop()
            depth = len(rectangle.path) // 2
            deepest = max(deepest, depth)
            if classify_local(rectangle):
                continue
            bounds = validate_left_cell(
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
            raise RuntimeError("the parallel stable-gap cover requires fork")
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
                    prioritise_neutral_chain()
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
    roots_by_id = {root.root_id: root for root in roots}
    origin_owners = [
        leaf
        for leaf in leaves
        if _rectangle_contains_origin(
            rectangle_from_path(roots_by_id[leaf.root_id], leaf.path)
        )
    ]
    covered = (
        complete
        and prefix
        and strict
        and tail_monotone
        and normalized == len(roots)
        and neutral_count > 0
        and neumann_count > 0
        and len(origin_owners) == 1
        and origin_owners[0].proof_kind == "neutral_full_complex_disk"
    )
    stress = (
        _stress_replay(parent.orbit, worst, phase_upper)
        if covered
        else _StressReplay(STRESS_PRECISION_BITS, None, None, False)
    )
    covered = covered and stress.strict
    digest = leaf_digest(leaves)
    if (
        covered
        and isinstance(EXPECTED_COMPLETE_LEAF_PARTITION_SHA256, str)
        and digest != EXPECTED_COMPLETE_LEAF_PARTITION_SHA256
    ):
        raise ValueError("the registered stable-gap leaf partition changed")
    pending_by_root = {
        root.root_id: sum(
            rectangle.root_id == root.root_id for rectangle in pending
        )
        for root in roots
    }
    failure = None
    if not covered:
        failure = (
            f"left-strip cover incomplete: processed={processed}, "
            f"accepted={len(leaves)}, pending={len(pending)}; the "
            "quantitative stable gap remains open"
        )
    theorem_flags = {name: covered for name in TRUE_ON_COMPLETE}
    return InnerStableGapCertificate(
        schema_id=SCHEMA_ID,
        model_id=MODEL_ID,
        branch=BRANCH,
        right_half_result_sha256=EXPECTED_RIGHT_HALF_RESULT_SHA256,
        floquet_transfer_result_sha256=(
            EXPECTED_FLOQUET_TRANSFER_RESULT_SHA256
        ),
        inner_orbit_result=parent.evidence.source_result,
        inner_orbit_result_sha256=parent.evidence.source_result_sha256,
        candidate_fingerprint=parent.evidence.candidate_fingerprint,
        left_engine_source_sha256=_sha256_path(
            repository
            / "src/canard_control/leaky_floquet_left_strip_cover_engine.py"
        ),
        correction_radius=CORRECTION_RADIUS,
        binary_blas_thread_count=int(PINNED_OPENBLAS_NUM_THREADS),
        precision_bits=precision,
        norm_id="complex-component-wiener-l1-split-re-im",
        fourier_cutoff=FOURIER_CUTOFF,
        coefficient_support_half_bandwidth=128,
        gamma_lower=format(GAMMA, "f"),
        stable_multiplier_modulus_upper=decimal_upper(stable_modulus),
        one_minus_stable_multiplier_modulus_lower=decimal_lower(stable_margin),
        neutral_full_disk_radius=format(NEUTRAL_FULL_DISK_RADIUS, "f"),
        neutral_delay_exponential_modulus_upper=(
            neutral.delay_exponential_modulus_upper
        ),
        neutral_first_order_coefficient_upper=(
            neutral.first_order_coefficient_upper
        ),
        neutral_second_order_coefficient_upper=(
            neutral.second_order_coefficient_upper
        ),
        neutral_first_contraction_upper=(
            neutral.first_neutral_contraction_upper
        ),
        neutral_second_contraction_upper=(
            neutral.second_neutral_contraction_upper
        ),
        maximum_left_delay_modulus_upper=decimal_upper(maximum_delay_modulus),
        upper_phase_lower="0",
        upper_phase_upper=format(phase_upper, "f"),
        root_rectangle_count=len(roots),
        accepted_leaf_count=len(leaves),
        neutral_disk_leaf_count=neutral_count,
        neutral_root_owner_leaf_count=len(origin_owners),
        neumann_leaf_count=neumann_count,
        processed_cell_count=processed,
        pending_cell_count=len(pending),
        pending_left_low_count=pending_by_root["left_low"],
        pending_left_upper_count=pending_by_root["left_upper"],
        neutral_disk_first_processed_cell=neutral_first,
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
        left_closed_strip_characteristic_value_count=(1 if covered else None),
        left_open_strip_characteristic_value_count=(0 if covered else None),
        shifted_closed_strip_characteristic_value_count=(
            2 if covered else None
        ),
        shifted_closed_strip_nontranslation_characteristic_value_count=(
            1 if covered else None
        ),
        stable_multiplier_spectral_radius_upper=(
            decimal_upper(stable_modulus) if covered else None
        ),
        **{name: True for name in STRUCTURAL_TRUE},
        **theorem_flags,
        **{name: False for name in ALWAYS_FALSE},
        leaves=tuple(sorted(leaves, key=lambda leaf: (leaf.root_id, leaf.path))),
        worst_cell=worst if worst is not None else blocking,
        failure_reason=failure,
    )


def build_inner_stable_gap_result(
    repository: Path,
    *,
    maximum_processed_cells: int = MAXIMUM_PROCESSED_CELLS,
    parallel_workers: int = 1,
    replay_parents: bool = True,
    progress: Callable[[int, int, int], None] | None = None,
) -> dict[str, Any]:
    repository = repository.resolve()
    certificate = asdict(
        build_inner_stable_gap_certificate(
            repository,
            maximum_processed_cells=maximum_processed_cells,
            parallel_workers=parallel_workers,
            replay_parents=replay_parents,
            progress=progress,
        )
    )
    certificate = json.loads(json.dumps(certificate, allow_nan=False))
    sources = {
        relative: _sha256_path(repository / relative)
        for relative in SOURCE_MANIFEST
    }
    result: dict[str, Any] = {
        "certificate": certificate,
        "scope": {
            "center_parameter_gamma_lower": certificate["gamma_lower"],
            "center_parameter_stable_spectral_radius_upper": certificate[
                "stable_multiplier_spectral_radius_upper"
            ],
            "quantitative_inner_stable_spectral_gap_validated": certificate[
                "quantitative_inner_stable_spectral_gap_validated"
            ],
            "common_parameter_box_stable_gap_validated": False,
            "stable_spectral_projection_constructed": False,
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
        "right_half_result": RIGHT_HALF_RESULT_RELATIVE_PATH,
        "right_half_result_sha256": _sha256_path(
            repository / RIGHT_HALF_RESULT_RELATIVE_PATH
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


def validate_inner_stable_gap_result(
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
        raise ValueError("the inner stable-gap result has the wrong schema")
    certificate = _mapping(payload.get("certificate"), "stable-gap certificate")
    scope = _mapping(payload.get("scope"), "stable-gap scope")
    manifest = _mapping(payload.get("manifest"), "stable-gap manifest")
    if set(certificate) != {
        field.name for field in fields(InnerStableGapCertificate)
    }:
        raise ValueError("the stable-gap certificate schema changed")
    if canonical_sha256(certificate) != EXPECTED_CERTIFICATE_SHA256:
        raise ValueError("the registered stable-gap certificate changed")
    for name in STRUCTURAL_TRUE:
        if certificate.get(name) is not True:
            raise ValueError(f"a stable-gap structural gate is absent: {name}")
    for name in ALWAYS_FALSE:
        if certificate.get(name) is not False:
            raise ValueError(f"an open stable-gap claim was promoted: {name}")
    fixed = {
        "schema_id": SCHEMA_ID,
        "model_id": MODEL_ID,
        "branch": BRANCH,
        "right_half_result_sha256": EXPECTED_RIGHT_HALF_RESULT_SHA256,
        "floquet_transfer_result_sha256": (
            EXPECTED_FLOQUET_TRANSFER_RESULT_SHA256
        ),
        "correction_radius": CORRECTION_RADIUS,
        "binary_blas_thread_count": int(PINNED_OPENBLAS_NUM_THREADS),
        "precision_bits": PRECISION_BITS,
        "norm_id": "complex-component-wiener-l1-split-re-im",
        "fourier_cutoff": FOURIER_CUTOFF,
        "coefficient_support_half_bandwidth": 128,
        "gamma_lower": format(GAMMA, "f"),
        "neutral_full_disk_radius": format(NEUTRAL_FULL_DISK_RADIUS, "f"),
        "upper_phase_lower": "0",
        "root_rectangle_count": 2,
        "acceptance_threshold": str(ACCEPTANCE_THRESHOLD),
        "stress_replay_precision_bits": STRESS_PRECISION_BITS,
    }
    if any(certificate.get(name) != value for name, value in fixed.items()):
        raise ValueError("the stable-gap fixed theorem data changed")
    repository = repository.resolve()
    parents = _validate_parents(
        repository, replay_parents=validate_parents
    )
    if certificate.get("candidate_fingerprint") != (
        parents.evidence.candidate_fingerprint
    ):
        raise ValueError("the stable-gap candidate fingerprint changed")
    if certificate.get("inner_orbit_result") != parents.evidence.source_result:
        raise ValueError("the stable-gap source orbit changed")
    if certificate.get("inner_orbit_result_sha256") != (
        parents.evidence.source_result_sha256
    ):
        raise ValueError("the stable-gap source orbit hash changed")
    engine_path = (
        repository
        / "src/canard_control/leaky_floquet_left_strip_cover_engine.py"
    )
    if certificate.get("left_engine_source_sha256") != _sha256_path(engine_path):
        raise ValueError("the stable-gap left engine changed")

    neutral = _neutral_full_disk_bounds(parents.transfer, PRECISION_BITS)
    expected_neutral = {
        "neutral_delay_exponential_modulus_upper": (
            neutral.delay_exponential_modulus_upper
        ),
        "neutral_first_order_coefficient_upper": (
            neutral.first_order_coefficient_upper
        ),
        "neutral_second_order_coefficient_upper": (
            neutral.second_order_coefficient_upper
        ),
        "neutral_first_contraction_upper": (
            neutral.first_neutral_contraction_upper
        ),
        "neutral_second_contraction_upper": (
            neutral.second_neutral_contraction_upper
        ),
    }
    if any(
        certificate.get(name) != value
        for name, value in expected_neutral.items()
    ):
        raise ValueError("the full complex neutral-disk bounds changed")
    if not (
        Decimal(certificate["neutral_first_contraction_upper"]) < 1
        and Decimal(certificate["neutral_second_contraction_upper"]) < 1
    ):
        raise ValueError("the full complex neutral disk is not strict")

    phase_upper = Decimal(str(certificate["upper_phase_upper"]))
    expected_phase = Decimal(decimal_upper(pi_interval(PRECISION_BITS).upper))
    if phase_upper != expected_phase:
        raise ValueError("the stable-gap principal phase boundary changed")
    roots = {root.root_id: root for root in _root_rectangles(phase_upper)}
    leaves_value = certificate.get("leaves")
    if not isinstance(leaves_value, list):
        raise ValueError("the stable-gap leaves must be a JSON list")
    leaf_fields = {field.name for field in fields(CoverLeaf)}
    leaves: list[CoverLeaf] = []
    for value in leaves_value:
        record = _mapping(value, "stable-gap leaf")
        if set(record) != leaf_fields:
            raise ValueError("a stable-gap leaf schema changed")
        leaves.append(CoverLeaf(**dict(record)))
    if leaves != sorted(leaves, key=lambda leaf: (leaf.root_id, leaf.path)):
        raise ValueError("the stable-gap leaves are not canonical")
    if len(leaves) != certificate.get("accepted_leaf_count"):
        raise ValueError("the stable-gap accepted count changed")
    if len({(leaf.root_id, leaf.path) for leaf in leaves}) != len(leaves):
        raise ValueError("the stable-gap leaves are not unique")
    if leaf_digest(leaves) != certificate.get("leaf_partition_sha256"):
        raise ValueError("the stable-gap leaf digest changed")
    neutral_count = 0
    neumann_count = 0
    origin_owner_count = 0
    origin_owner_is_local = False
    for leaf in leaves:
        if leaf.root_id not in roots:
            raise ValueError("a stable-gap leaf has an unknown root")
        rectangle = rectangle_from_path(roots[leaf.root_id], leaf.path)
        contraction = Decimal(leaf.contraction_upper)
        finite = Decimal(leaf.finite_input_column_sum_upper)
        tail = Decimal(leaf.tail_input_column_sum_upper)
        in_neutral = _rectangle_strictly_inside_full_origin_disk(
            rectangle, NEUTRAL_FULL_DISK_RADIUS
        )
        if _rectangle_contains_origin(rectangle):
            origin_owner_count += 1
            origin_owner_is_local = (
                leaf.proof_kind == "neutral_full_complex_disk"
            )
        if leaf.proof_kind == "neutral_full_complex_disk":
            neutral_count += 1
            if not in_neutral or (contraction, finite, tail) != (Decimal(0),) * 3:
                raise ValueError("a stable-gap neutral leaf is invalid")
        elif leaf.proof_kind == "full_operator_neumann":
            neumann_count += 1
            if in_neutral:
                raise ValueError("a stable-gap local rectangle was misclassified")
            if contraction != max(finite, tail) or not Decimal(0) < contraction < 1:
                raise ValueError("a stable-gap Neumann leaf is not strict")
            if contraction > ACCEPTANCE_THRESHOLD:
                raise ValueError("a stable-gap Neumann leaf exceeds threshold")
        else:
            raise ValueError("a stable-gap leaf has an unknown proof kind")
    if (
        neutral_count != certificate.get("neutral_disk_leaf_count")
        or neumann_count != certificate.get("neumann_leaf_count")
    ):
        raise ValueError("the stable-gap proof-kind counts changed")
    if (
        origin_owner_count != certificate.get("neutral_root_owner_leaf_count")
        or origin_owner_count != 1
        or not origin_owner_is_local
    ):
        raise ValueError("the stable-gap neutral root has no unique local owner")
    pending_counts = (
        int(certificate["pending_left_low_count"]),
        int(certificate["pending_left_upper_count"]),
    )
    if min(pending_counts) < 0 or sum(pending_counts) != int(
        certificate["pending_cell_count"]
    ):
        raise ValueError("the stable-gap pending counts changed")
    first = certificate["neutral_disk_first_processed_cell"]
    if (neutral_count == 0) != (first is None):
        raise ValueError("the stable-gap neutral first-hit marker changed")
    if first is not None and not (
        1 <= int(first) <= int(certificate["processed_cell_count"])
    ):
        raise ValueError("the stable-gap neutral first-hit marker is invalid")

    complete = certificate.get("pending_cell_count") == 0
    prefix = complete and prefix_complete(leaves, tuple(roots))
    promoted = bool(
        certificate.get("quantitative_inner_stable_spectral_gap_validated")
    )
    count_fields = (
        "left_closed_strip_characteristic_value_count",
        "left_open_strip_characteristic_value_count",
        "shifted_closed_strip_characteristic_value_count",
        "shifted_closed_strip_nontranslation_characteristic_value_count",
    )
    if promoted:
        if not isinstance(EXPECTED_COMPLETE_LEAF_PARTITION_SHA256, str):
            raise ValueError("the complete stable-gap digest is unregistered")
        if certificate.get("leaf_partition_sha256") != (
            EXPECTED_COMPLETE_LEAF_PARTITION_SHA256
        ):
            raise ValueError("the registered stable-gap digest changed")
        if not prefix:
            raise ValueError("the promoted stable-gap partition is incomplete")
        if certificate.get("accepted_normalized_root_fraction") != "2":
            raise ValueError("the stable-gap forest has an area gap")
        if certificate.get("processed_cell_count") != 2 * len(leaves) - len(roots):
            raise ValueError("the stable-gap binary-forest count changed")
        if certificate.get("maximum_depth") != max(
            len(leaf.path) // 2 for leaf in leaves
        ):
            raise ValueError("the stable-gap maximum depth changed")
        maximum = max(Decimal(leaf.contraction_upper) for leaf in leaves)
        if format(maximum, "f") != certificate.get("maximum_contraction_upper"):
            raise ValueError("the stable-gap maximum contraction changed")
        if _margin(format(maximum, "f")) != certificate.get(
            "minimum_contraction_margin_lower"
        ):
            raise ValueError("the stable-gap contraction margin changed")
        if certificate.get("worst_cell_finer_split_stress_strict") is not True:
            raise ValueError("the stable-gap stress replay is not strict")
        if any(certificate.get(name) is not True for name in TRUE_ON_COMPLETE):
            raise ValueError("a completed stable-gap theorem flag is absent")
        expected_counts = (1, 0, 2, 1)
        if tuple(certificate.get(name) for name in count_fields) != expected_counts:
            raise ValueError("a stable-gap analytic count changed")
        if certificate.get("stable_multiplier_spectral_radius_upper") != (
            certificate.get("stable_multiplier_modulus_upper")
        ):
            raise ValueError("the stable spectral-radius bound changed")
        if not (
            Decimal(certificate["stable_multiplier_spectral_radius_upper"])
            < 1
            and Decimal(certificate["one_minus_stable_multiplier_modulus_lower"])
            > 0
        ):
            raise ValueError("the stable multiplier gap is not strict")
    else:
        if any(certificate.get(name) is not False for name in TRUE_ON_COMPLETE):
            raise ValueError("an incomplete stable-gap cover promoted a theorem")
        if any(certificate.get(name) is not None for name in count_fields):
            raise ValueError("an incomplete stable-gap cover inserted a count")
        if certificate.get("stable_multiplier_spectral_radius_upper") is not None:
            raise ValueError("an incomplete stable-gap cover inserted a radius")

    expected_scope = {
        "center_parameter_gamma_lower": certificate["gamma_lower"],
        "center_parameter_stable_spectral_radius_upper": certificate[
            "stable_multiplier_spectral_radius_upper"
        ],
        "quantitative_inner_stable_spectral_gap_validated": promoted,
        "common_parameter_box_stable_gap_validated": False,
        "stable_spectral_projection_constructed": False,
        "inner_stable_manifold_validated": False,
        "physical_pulse_onset_validated": False,
    }
    if dict(scope) != expected_scope:
        raise ValueError("the stable-gap scope ledger changed")

    expected_manifest_fields = {
        "schema_id",
        "result",
        "default_command",
        "arithmetic_scope",
        "certificate_sha256",
        "source_sha256",
        "right_half_result",
        "right_half_result_sha256",
        "floquet_transfer_result",
        "floquet_transfer_result_sha256",
        "inner_orbit_result",
        "inner_orbit_result_sha256",
        "environment",
    }
    if set(manifest) != expected_manifest_fields:
        raise ValueError("the stable-gap manifest schema changed")
    if manifest.get("schema_id") != SCHEMA_ID:
        raise ValueError("the stable-gap manifest id changed")
    if manifest.get("result") != RESULT_RELATIVE_PATH:
        raise ValueError("the stable-gap result path changed")
    if manifest.get("default_command") != DEFAULT_COMMAND:
        raise ValueError("the stable-gap replay command changed")
    if manifest.get("arithmetic_scope") != ARITHMETIC_SCOPE:
        raise ValueError("the stable-gap arithmetic scope changed")
    if manifest.get("certificate_sha256") != canonical_sha256(certificate):
        raise ValueError("the stable-gap certificate digest changed")
    source_hashes = _mapping(manifest.get("source_sha256"), "source manifest")
    if set(source_hashes) != set(SOURCE_MANIFEST):
        raise ValueError("the stable-gap source set changed")
    for relative in SOURCE_MANIFEST:
        if source_hashes.get(relative) != _sha256_path(repository / relative):
            raise ValueError(f"the stable-gap source changed: {relative}")
    parent_paths = {
        "right_half_result": RIGHT_HALF_RESULT_RELATIVE_PATH,
        "floquet_transfer_result": FLOQUET_TRANSFER_RESULT_RELATIVE_PATH,
        "inner_orbit_result": str(certificate["inner_orbit_result"]),
    }
    for name, relative in parent_paths.items():
        if manifest.get(name) != relative:
            raise ValueError(f"the stable-gap parent path changed: {name}")
        if manifest.get(name + "_sha256") != _sha256_path(
            repository / relative
        ):
            raise ValueError(f"the stable-gap parent hash changed: {name}")


__all__ = [
    "ACCEPTANCE_THRESHOLD",
    "ALWAYS_FALSE",
    "EXPECTED_COMPLETE_LEAF_PARTITION_SHA256",
    "EXPECTED_CERTIFICATE_SHA256",
    "GAMMA",
    "InnerStableGapCertificate",
    "MAXIMUM_PROCESSED_CELLS",
    "NEUTRAL_FULL_DISK_RADIUS",
    "PINNED_OPENBLAS_NUM_THREADS",
    "RESULT_RELATIVE_PATH",
    "SCHEMA_ID",
    "SOURCE_MANIFEST",
    "STRUCTURAL_TRUE",
    "TRUE_ON_COMPLETE",
    "build_inner_stable_gap_certificate",
    "build_inner_stable_gap_result",
    "canonical_sha256",
    "validate_inner_stable_gap_result",
]
