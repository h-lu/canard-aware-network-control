"""Strengthen the center-inner Poincare stable gap to ``gamma=0.01``.

The base stable-gap artifact owns ``-0.001 <= Re s <= 0`` and the full
neutral disk.  This module covers only the additional closed slab
``-0.01 <= Re s <= -0.001``.  Strict local leaves inherit zero-freeness
from the base full-disk theorem; every other leaf uses the corrected
negative-real-part full-operator Neumann engine.
"""

from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor
from dataclasses import asdict, dataclass, fields
from decimal import Decimal, localcontext
from fractions import Fraction
from hashlib import sha256
import json
import multiprocessing
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
from canard_control.leaky_floquet_inner_stable_gap import (
    CORRECTION_RADIUS,
    PINNED_OPENBLAS_NUM_THREADS,
    RESULT_RELATIVE_PATH as BASE_GAP_RESULT_RELATIVE_PATH,
    _prepare_inner_candidate,
    _rectangle_strictly_inside_full_origin_disk,
    _require_pinned_binary_blas_environment,
    _validate_parents as _validate_base_parents,
    canonical_sha256,
    validate_inner_stable_gap_result,
)
from canard_control.leaky_floquet_left_strip_cover_engine import (
    _left_delay_modulus_upper,
    validate_left_cell,
)
from canard_control.leaky_periodic_validation import (
    _build_leaky_base_sequences,
)


SCHEMA_ID = "leaky-floquet-inner-strong-stable-gap-v1"
MODEL_ID = "autonomous-leaky-recovery-two-delay-fhn-bistable-proposal"
BRANCH = "inner_saddle_candidate"
SOURCE_RELATIVE_PATH = (
    "src/canard_control/leaky_floquet_inner_strong_stable_gap.py"
)
GENERATOR_RELATIVE_PATH = (
    "experiments/leaky_floquet_inner_strong_stable_gap.py"
)
NOTE_RELATIVE_PATH = "docs/leaky-floquet-inner-strong-stable-gap.md"
TEST_RELATIVE_PATH = "tests/test_leaky_floquet_inner_strong_stable_gap.py"
RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_floquet_inner_strong_stable_gap.json"
)
DEFAULT_COMMAND = (
    "OPENBLAS_NUM_THREADS=1 PYTHONPATH=build/testdeps:src /usr/bin/python3 "
    "experiments/leaky_floquet_inner_strong_stable_gap.py --workers 12"
)
ARITHMETIC_SCOPE = (
    "160-bit outward MPFR full-operator cover on the center-inner extension "
    "slab -0.01<=Re(s)<=-0.001; source-bound radius-1e-12 orbit; inherited "
    "full complex neutral disk; corrected negative-real delay factors; exact "
    "dyadic seams; and 256-bit limiting-cell stress replay"
)

PRECISION_BITS = 160
STRESS_PRECISION_BITS = 256
FOURIER_CUTOFF = 64
BASE_GAMMA = Decimal("0.001")
GAMMA = Decimal("0.01")
NEUTRAL_FULL_DISK_RADIUS = Decimal("0.0039")
LOW_SEAM = Decimal(1)
ACCEPTANCE_THRESHOLD = Decimal("0.995")
MAXIMUM_PROCESSED_CELLS = 30000
MAXIMUM_DEPTH = 96
EXPECTED_COMPLETE_LEAF_PARTITION_SHA256 = (
    "b44b5bf14066a8110fd0c2e1305eba723f79be3e2945f0d1d509c36d978256e8"
)
EXPECTED_CERTIFICATE_SHA256 = (
    "44e7207d5396149356aeaed03a15b3859fc0ed8556d1ab2e1d15ffdc49e880ae"
)
EXPECTED_BASE_GAP_RESULT_SHA256 = (
    "9180fd43b6c19d8c6d8ee1e34a88cbdaee714a7f784b5ce862625a9f8015190a"
)

STRUCTURAL_TRUE = (
    "source_validated_base_gap_used",
    "source_validated_same_inner_orbit_used",
    "base_full_complex_neutral_disk_used",
    "base_compact_history_monodromy_bridge_used",
    "physical_unshifted_coefficient_output_phase_used",
    "shifted_coefficient_input_phase_equivalence_inherited",
    "negative_real_delay_modulus_restored",
    "negative_real_tail_frequency_absolute_value_restored",
    "negative_real_delay_taylor_factor_restored",
    "negative_real_full_disk_farthest_corner_used",
    "tail_diagonal_edge_monotonicity_validated",
    "full_mode_128_coefficient_support_used",
    "complex_split_wiener_norm_used",
)

TRUE_ON_COMPLETE = (
    "extension_upper_half_exact_partition_validated",
    "extension_local_parent_disk_leaves_zero_free_validated",
    "extension_disk_boundary_owned_by_neumann_cover_validated",
    "all_extension_nonlocal_cells_full_operator_neumann_validated",
    "extension_closed_slab_zero_free_validated",
    "base_extension_vertical_seam_zero_free_validated",
    "combined_left_open_strip_zero_free_validated",
    "lower_extension_excluded_by_real_conjugacy",
    "poincare_strong_stable_spectral_radius_bound_validated",
    "quantitative_inner_strong_stable_spectral_gap_validated",
)

ALWAYS_FALSE = (
    "common_parameter_box_strong_stable_gap_validated",
    "stable_spectral_projection_constructed",
    "stable_boundary_power_bound_validated",
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
    "src/canard_control/leaky_floquet_inner_stable_gap.py",
    "src/canard_control/leaky_floquet_left_strip_cover_engine.py",
    "src/canard_control/leaky_periodic_validation.py",
)


@dataclass(frozen=True)
class _StressReplay:
    precision_bits: int
    same_cell_upper: str | None
    finer_split_upper: str | None
    strict: bool


@dataclass(frozen=True)
class InnerStrongStableGapCertificate:
    schema_id: str
    model_id: str
    branch: str
    base_gap_result_sha256: str
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
    base_gamma_lower: str
    gamma_lower: str
    stable_multiplier_modulus_upper: str
    one_minus_stable_multiplier_modulus_lower: str
    neutral_parent_full_disk_radius: str
    maximum_extension_delay_modulus_upper: str
    upper_phase_lower: str
    upper_phase_upper: str
    root_rectangle_count: int
    accepted_leaf_count: int
    neutral_parent_leaf_count: int
    neumann_leaf_count: int
    processed_cell_count: int
    pending_cell_count: int
    pending_strong_low_count: int
    pending_strong_upper_count: int
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
    extension_closed_slab_characteristic_value_count: int | None
    combined_left_closed_strip_characteristic_value_count: int | None
    combined_left_open_strip_characteristic_value_count: int | None
    combined_shifted_closed_strip_characteristic_value_count: int | None
    combined_shifted_nontranslation_characteristic_value_count: int | None
    stable_multiplier_spectral_radius_upper: str | None
    source_validated_base_gap_used: bool
    source_validated_same_inner_orbit_used: bool
    base_full_complex_neutral_disk_used: bool
    base_compact_history_monodromy_bridge_used: bool
    physical_unshifted_coefficient_output_phase_used: bool
    shifted_coefficient_input_phase_equivalence_inherited: bool
    negative_real_delay_modulus_restored: bool
    negative_real_tail_frequency_absolute_value_restored: bool
    negative_real_delay_taylor_factor_restored: bool
    negative_real_full_disk_farthest_corner_used: bool
    tail_diagonal_edge_monotonicity_validated: bool
    full_mode_128_coefficient_support_used: bool
    complex_split_wiener_norm_used: bool
    extension_upper_half_exact_partition_validated: bool
    extension_local_parent_disk_leaves_zero_free_validated: bool
    extension_disk_boundary_owned_by_neumann_cover_validated: bool
    all_extension_nonlocal_cells_full_operator_neumann_validated: bool
    extension_closed_slab_zero_free_validated: bool
    base_extension_vertical_seam_zero_free_validated: bool
    combined_left_open_strip_zero_free_validated: bool
    lower_extension_excluded_by_real_conjugacy: bool
    poincare_strong_stable_spectral_radius_bound_validated: bool
    quantitative_inner_strong_stable_spectral_gap_validated: bool
    common_parameter_box_strong_stable_gap_validated: bool
    stable_spectral_projection_constructed: bool
    stable_boundary_power_bound_validated: bool
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
        raise RuntimeError("the strong-gap worker was not initialized")
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


def _validate_base_gap(
    repository: Path,
    *,
    replay_parents: bool,
) -> tuple[Mapping[str, Any], Any]:
    repository = repository.resolve()
    path = repository / BASE_GAP_RESULT_RELATIVE_PATH
    if _sha256_path(path) != EXPECTED_BASE_GAP_RESULT_SHA256:
        raise ValueError("the strong-gap base result changed")
    payload = _mapping(json.loads(path.read_text()), "base gap result")
    validate_inner_stable_gap_result(
        payload,
        repository,
        validate_parents=replay_parents,
    )
    certificate = _mapping(payload.get("certificate"), "base gap certificate")
    required = {
        "gamma_lower": format(BASE_GAMMA, "f"),
        "quantitative_inner_stable_spectral_gap_validated": True,
        "neutral_full_complex_disk_uniqueness_validated": True,
        "neutral_full_disk_boundary_zero_free_validated": True,
        "source_validated_compact_history_monodromy_used": True,
        "history_spectrum_to_fourier_characteristic_values_bridge_used": True,
        "left_open_strip_characteristic_value_count": 0,
        "shifted_closed_strip_characteristic_value_count": 2,
        "shifted_closed_strip_nontranslation_characteristic_value_count": 1,
    }
    if any(certificate.get(name) != value for name, value in required.items()):
        raise ValueError("the strong-gap base theorem is incomplete")
    parent = _validate_base_parents(repository, replay_parents=False)
    if certificate.get("candidate_fingerprint") != (
        parent.evidence.candidate_fingerprint
    ):
        raise ValueError("the strong-gap base theorem uses another orbit")
    return certificate, parent


def _root_rectangles(phase_upper: Decimal) -> tuple[Rectangle, ...]:
    if not Decimal(0) < LOW_SEAM < phase_upper:
        raise ValueError("the strong-gap phase seam left the principal strip")
    return (
        Rectangle(
            "strong_low",
            "",
            -GAMMA,
            -BASE_GAMMA,
            Decimal(0),
            LOW_SEAM,
        ),
        Rectangle(
            "strong_upper",
            "",
            -GAMMA,
            -BASE_GAMMA,
            LOW_SEAM,
            phase_upper,
        ),
    )


def _tail_diagonal_monotone(
    base: Any,
    correction: DirectedInterval,
    precision: int,
) -> bool:
    gamma = DirectedInterval.from_decimal(format(GAMMA, "f"), precision)
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        maximum_real = max(
            gamma.upper,
            (base.period.upper + correction.upper)
            * base.parameters["epsilon"].upper,
        )
    sqrt_two = DirectedInterval.from_decimal(2, precision).sqrt().upper
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        tail_gap = 129 * pi_interval(precision).lower
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        left = (sqrt_two - 1) * maximum_real
    return left < tail_gap


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
    candidate = _prepare_inner_candidate(orbit, base, STRESS_PRECISION_BITS)
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
    strict = Decimal(same.worst.contraction_upper) < 1 and finer_upper < 1
    return _StressReplay(
        STRESS_PRECISION_BITS,
        same.worst.contraction_upper,
        format(finer_upper, "f"),
        strict,
    )


def build_inner_strong_stable_gap_certificate(
    repository: Path,
    *,
    precision: int = PRECISION_BITS,
    acceptance_threshold: str = str(ACCEPTANCE_THRESHOLD),
    maximum_processed_cells: int = MAXIMUM_PROCESSED_CELLS,
    maximum_depth: int = MAXIMUM_DEPTH,
    parallel_workers: int = 1,
    replay_parents: bool = True,
    progress: Callable[[int, int, int], None] | None = None,
) -> InnerStrongStableGapCertificate:
    repository = repository.resolve()
    base_gap, parent = _validate_base_gap(
        repository, replay_parents=replay_parents
    )
    if precision != PRECISION_BITS:
        raise ValueError("the strong-gap precision is pinned at 160 bits")
    threshold = Decimal(acceptance_threshold)
    if not Decimal(0) < threshold < Decimal(1):
        raise ValueError("the strong-gap threshold must lie in (0,1)")
    if maximum_processed_cells < 1 or maximum_depth < 1 or parallel_workers < 1:
        raise ValueError("the strong-gap budgets must be positive")
    _require_pinned_binary_blas_environment()
    _binary_environment_checked()
    base = _build_leaky_base_sequences(parent.orbit, precision)
    candidate = _prepare_inner_candidate(parent.orbit, base, precision)
    correction = DirectedInterval.from_decimal(CORRECTION_RADIUS, precision)
    phase_upper = Decimal(decimal_upper(pi_interval(precision).upper))
    roots = _root_rectangles(phase_upper)
    maximum_delay_modulus = _left_delay_modulus_upper(
        roots[0], base, correction, precision
    )
    if not _tail_diagonal_monotone(base, correction, precision):
        raise ArithmeticError("the strong-gap tail inverse is not monotone")

    gamma_box = DirectedInterval.from_decimal(format(GAMMA, "f"), precision)
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        stable_modulus = gmpy2.exp(-gamma_box.lower)
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        stable_margin = 1 - stable_modulus
    if not 0 < stable_modulus < 1 or stable_margin <= 0:
        raise ArithmeticError("the strong stable multiplier gap vanished")

    pending = list(reversed(roots))
    leaves: list[CoverLeaf] = []
    local_count = 0
    neumann_count = 0
    worst: WorstCoverCell | None = None
    blocking: WorstCoverCell | None = None
    processed = 0
    deepest = 0

    def classify_local(rectangle: Rectangle) -> bool:
        nonlocal local_count, processed
        if _rectangle_strictly_inside_full_origin_disk(
            rectangle, NEUTRAL_FULL_DISK_RADIUS
        ):
            if rectangle.sigma_upper > -BASE_GAMMA:
                raise ArithmeticError("a strong local leaf crossed its base seam")
            leaves.append(
                CoverLeaf(
                    rectangle.root_id,
                    rectangle.path,
                    "neutral_parent_zero_free",
                    "0",
                    "0",
                    "0",
                )
            )
            local_count += 1
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
            raise RuntimeError("the parallel strong-gap cover requires fork")
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
        and normalized == len(roots)
        and local_count > 0
        and neumann_count > 0
    )
    stress = (
        _stress_replay(parent.orbit, worst, phase_upper)
        if covered
        else _StressReplay(STRESS_PRECISION_BITS, None, None, False)
    )
    covered = covered and stress.strict
    digest = leaf_digest(leaves)
    if covered and digest != EXPECTED_COMPLETE_LEAF_PARTITION_SHA256:
        raise ValueError("the registered strong-gap leaf partition changed")
    pending_by_root = {
        root.root_id: sum(
            rectangle.root_id == root.root_id for rectangle in pending
        )
        for root in roots
    }
    failure = None
    if not covered:
        failure = (
            f"strong extension cover incomplete: processed={processed}, "
            f"accepted={len(leaves)}, pending={len(pending)}"
        )
    theorem_flags = {name: covered for name in TRUE_ON_COMPLETE}
    return InnerStrongStableGapCertificate(
        schema_id=SCHEMA_ID,
        model_id=MODEL_ID,
        branch=BRANCH,
        base_gap_result_sha256=EXPECTED_BASE_GAP_RESULT_SHA256,
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
        base_gamma_lower=format(BASE_GAMMA, "f"),
        gamma_lower=format(GAMMA, "f"),
        stable_multiplier_modulus_upper=decimal_upper(stable_modulus),
        one_minus_stable_multiplier_modulus_lower=decimal_lower(stable_margin),
        neutral_parent_full_disk_radius=str(
            base_gap["neutral_full_disk_radius"]
        ),
        maximum_extension_delay_modulus_upper=decimal_upper(
            maximum_delay_modulus
        ),
        upper_phase_lower="0",
        upper_phase_upper=format(phase_upper, "f"),
        root_rectangle_count=len(roots),
        accepted_leaf_count=len(leaves),
        neutral_parent_leaf_count=local_count,
        neumann_leaf_count=neumann_count,
        processed_cell_count=processed,
        pending_cell_count=len(pending),
        pending_strong_low_count=pending_by_root["strong_low"],
        pending_strong_upper_count=pending_by_root["strong_upper"],
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
        extension_closed_slab_characteristic_value_count=(
            0 if covered else None
        ),
        combined_left_closed_strip_characteristic_value_count=(
            1 if covered else None
        ),
        combined_left_open_strip_characteristic_value_count=(
            0 if covered else None
        ),
        combined_shifted_closed_strip_characteristic_value_count=(
            2 if covered else None
        ),
        combined_shifted_nontranslation_characteristic_value_count=(
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


def build_inner_strong_stable_gap_result(
    repository: Path,
    *,
    maximum_processed_cells: int = MAXIMUM_PROCESSED_CELLS,
    parallel_workers: int = 1,
    replay_parents: bool = True,
    progress: Callable[[int, int, int], None] | None = None,
) -> dict[str, Any]:
    repository = repository.resolve()
    certificate = asdict(
        build_inner_strong_stable_gap_certificate(
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
            "quantitative_inner_strong_stable_spectral_gap_validated": (
                certificate[
                    "quantitative_inner_strong_stable_spectral_gap_validated"
                ]
            ),
            "common_parameter_box_strong_stable_gap_validated": False,
            "stable_spectral_projection_constructed": False,
            "stable_boundary_power_bound_validated": False,
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
        "base_gap_result": BASE_GAP_RESULT_RELATIVE_PATH,
        "base_gap_result_sha256": _sha256_path(
            repository / BASE_GAP_RESULT_RELATIVE_PATH
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


def validate_inner_strong_stable_gap_result(
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
        raise ValueError("the inner strong-gap result has the wrong schema")
    certificate = _mapping(payload.get("certificate"), "strong certificate")
    scope = _mapping(payload.get("scope"), "strong scope")
    manifest = _mapping(payload.get("manifest"), "strong manifest")
    if set(certificate) != {
        field.name for field in fields(InnerStrongStableGapCertificate)
    }:
        raise ValueError("the strong-gap certificate schema changed")
    if canonical_sha256(certificate) != EXPECTED_CERTIFICATE_SHA256:
        raise ValueError("the registered strong-gap certificate changed")
    for name in STRUCTURAL_TRUE:
        if certificate.get(name) is not True:
            raise ValueError(f"a strong-gap structural gate is absent: {name}")
    for name in ALWAYS_FALSE:
        if certificate.get(name) is not False:
            raise ValueError(f"an open strong-gap claim was promoted: {name}")
    fixed = {
        "schema_id": SCHEMA_ID,
        "model_id": MODEL_ID,
        "branch": BRANCH,
        "base_gap_result_sha256": EXPECTED_BASE_GAP_RESULT_SHA256,
        "correction_radius": CORRECTION_RADIUS,
        "binary_blas_thread_count": int(PINNED_OPENBLAS_NUM_THREADS),
        "precision_bits": PRECISION_BITS,
        "norm_id": "complex-component-wiener-l1-split-re-im",
        "fourier_cutoff": FOURIER_CUTOFF,
        "coefficient_support_half_bandwidth": 128,
        "base_gamma_lower": format(BASE_GAMMA, "f"),
        "gamma_lower": format(GAMMA, "f"),
        "neutral_parent_full_disk_radius": format(
            NEUTRAL_FULL_DISK_RADIUS, "f"
        ),
        "upper_phase_lower": "0",
        "root_rectangle_count": 2,
        "acceptance_threshold": str(ACCEPTANCE_THRESHOLD),
        "stress_replay_precision_bits": STRESS_PRECISION_BITS,
    }
    if any(certificate.get(name) != value for name, value in fixed.items()):
        raise ValueError("the strong-gap fixed theorem data changed")
    repository = repository.resolve()
    base_gap, parent = _validate_base_gap(
        repository, replay_parents=validate_parents
    )
    if certificate.get("candidate_fingerprint") != (
        parent.evidence.candidate_fingerprint
    ):
        raise ValueError("the strong-gap orbit fingerprint changed")
    if certificate.get("inner_orbit_result") != parent.evidence.source_result:
        raise ValueError("the strong-gap source orbit changed")
    if certificate.get("inner_orbit_result_sha256") != (
        parent.evidence.source_result_sha256
    ):
        raise ValueError("the strong-gap source orbit hash changed")
    engine_path = (
        repository
        / "src/canard_control/leaky_floquet_left_strip_cover_engine.py"
    )
    if certificate.get("left_engine_source_sha256") != _sha256_path(engine_path):
        raise ValueError("the strong-gap left engine changed")

    gamma_box = DirectedInterval.from_decimal(format(GAMMA, "f"), PRECISION_BITS)
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundUp):
        stable_modulus = gmpy2.exp(-gamma_box.lower)
    with gmpy2.context(precision=PRECISION_BITS, round=gmpy2.RoundDown):
        stable_margin = 1 - stable_modulus
    expected_gap = {
        "stable_multiplier_modulus_upper": decimal_upper(stable_modulus),
        "one_minus_stable_multiplier_modulus_lower": decimal_lower(
            stable_margin
        ),
    }
    if any(
        certificate.get(name) != value for name, value in expected_gap.items()
    ):
        raise ValueError("the strong multiplier bound changed")

    phase_upper = Decimal(str(certificate["upper_phase_upper"]))
    expected_phase = Decimal(decimal_upper(pi_interval(PRECISION_BITS).upper))
    if phase_upper != expected_phase:
        raise ValueError("the strong-gap principal phase boundary changed")
    roots = {root.root_id: root for root in _root_rectangles(phase_upper)}
    base = _build_leaky_base_sequences(parent.orbit, PRECISION_BITS)
    correction = DirectedInterval.from_decimal(
        CORRECTION_RADIUS, PRECISION_BITS
    )
    if not _tail_diagonal_monotone(base, correction, PRECISION_BITS):
        raise ValueError("the strong-gap tail diagonal gate changed")
    expected_delay = decimal_upper(
        _left_delay_modulus_upper(
            roots["strong_low"], base, correction, PRECISION_BITS
        )
    )
    if certificate.get("maximum_extension_delay_modulus_upper") != expected_delay:
        raise ValueError("the strong-gap delay modulus changed")

    leaves_value = certificate.get("leaves")
    if not isinstance(leaves_value, list):
        raise ValueError("the strong-gap leaves must be a JSON list")
    leaf_fields = {field.name for field in fields(CoverLeaf)}
    leaves: list[CoverLeaf] = []
    for value in leaves_value:
        record = _mapping(value, "strong-gap leaf")
        if set(record) != leaf_fields:
            raise ValueError("a strong-gap leaf schema changed")
        leaves.append(CoverLeaf(**dict(record)))
    if leaves != sorted(leaves, key=lambda leaf: (leaf.root_id, leaf.path)):
        raise ValueError("the strong-gap leaves are not canonical")
    if len(leaves) != certificate.get("accepted_leaf_count"):
        raise ValueError("the strong-gap accepted count changed")
    if len({(leaf.root_id, leaf.path) for leaf in leaves}) != len(leaves):
        raise ValueError("the strong-gap leaves are not unique")
    if leaf_digest(leaves) != certificate.get("leaf_partition_sha256"):
        raise ValueError("the strong-gap leaf digest changed")

    local_count = 0
    neumann_count = 0
    for leaf in leaves:
        if leaf.root_id not in roots:
            raise ValueError("a strong-gap leaf has an unknown root")
        rectangle = rectangle_from_path(roots[leaf.root_id], leaf.path)
        contraction = Decimal(leaf.contraction_upper)
        finite = Decimal(leaf.finite_input_column_sum_upper)
        tail = Decimal(leaf.tail_input_column_sum_upper)
        in_neutral = _rectangle_strictly_inside_full_origin_disk(
            rectangle, NEUTRAL_FULL_DISK_RADIUS
        )
        if leaf.proof_kind == "neutral_parent_zero_free":
            local_count += 1
            if (
                not in_neutral
                or rectangle.sigma_upper > -BASE_GAMMA
                or (contraction, finite, tail) != (Decimal(0),) * 3
            ):
                raise ValueError("a strong-gap local leaf is invalid")
        elif leaf.proof_kind == "full_operator_neumann":
            neumann_count += 1
            if in_neutral:
                raise ValueError("a strong-gap local rectangle was misclassified")
            if contraction != max(finite, tail) or not Decimal(0) < contraction < 1:
                raise ValueError("a strong-gap Neumann leaf is not strict")
            if contraction > ACCEPTANCE_THRESHOLD:
                raise ValueError("a strong-gap Neumann leaf exceeds threshold")
        else:
            raise ValueError("a strong-gap leaf has an unknown proof kind")
    if (
        local_count != certificate.get("neutral_parent_leaf_count")
        or neumann_count != certificate.get("neumann_leaf_count")
    ):
        raise ValueError("the strong-gap proof-kind counts changed")
    pending_counts = (
        int(certificate["pending_strong_low_count"]),
        int(certificate["pending_strong_upper_count"]),
    )
    if min(pending_counts) < 0 or sum(pending_counts) != int(
        certificate["pending_cell_count"]
    ):
        raise ValueError("the strong-gap pending counts changed")

    complete = certificate.get("pending_cell_count") == 0
    prefix = complete and prefix_complete(leaves, tuple(roots))
    promoted = bool(
        certificate.get(
            "quantitative_inner_strong_stable_spectral_gap_validated"
        )
    )
    count_fields = (
        "extension_closed_slab_characteristic_value_count",
        "combined_left_closed_strip_characteristic_value_count",
        "combined_left_open_strip_characteristic_value_count",
        "combined_shifted_closed_strip_characteristic_value_count",
        "combined_shifted_nontranslation_characteristic_value_count",
    )
    if promoted:
        if certificate.get("leaf_partition_sha256") != (
            EXPECTED_COMPLETE_LEAF_PARTITION_SHA256
        ):
            raise ValueError("the registered strong-gap digest changed")
        if not prefix:
            raise ValueError("the promoted strong-gap partition is incomplete")
        if certificate.get("accepted_normalized_root_fraction") != "2":
            raise ValueError("the strong-gap forest has an area gap")
        if certificate.get("processed_cell_count") != 2 * len(leaves) - len(roots):
            raise ValueError("the strong-gap binary-forest count changed")
        if certificate.get("maximum_depth") != max(
            len(leaf.path) // 2 for leaf in leaves
        ):
            raise ValueError("the strong-gap maximum depth changed")
        maximum = max(Decimal(leaf.contraction_upper) for leaf in leaves)
        if format(maximum, "f") != certificate.get("maximum_contraction_upper"):
            raise ValueError("the strong-gap maximum contraction changed")
        if _margin(format(maximum, "f")) != certificate.get(
            "minimum_contraction_margin_lower"
        ):
            raise ValueError("the strong-gap contraction margin changed")
        if certificate.get("worst_cell_finer_split_stress_strict") is not True:
            raise ValueError("the strong-gap stress replay is not strict")
        if any(certificate.get(name) is not True for name in TRUE_ON_COMPLETE):
            raise ValueError("a completed strong-gap theorem flag is absent")
        if tuple(certificate.get(name) for name in count_fields) != (
            0,
            1,
            0,
            2,
            1,
        ):
            raise ValueError("a strong-gap analytic count changed")
        if certificate.get("stable_multiplier_spectral_radius_upper") != (
            certificate.get("stable_multiplier_modulus_upper")
        ):
            raise ValueError("the strong stable spectral-radius bound changed")
    else:
        if any(certificate.get(name) is not False for name in TRUE_ON_COMPLETE):
            raise ValueError("an incomplete strong-gap cover promoted a theorem")
        if any(certificate.get(name) is not None for name in count_fields):
            raise ValueError("an incomplete strong-gap cover inserted a count")
        if certificate.get("stable_multiplier_spectral_radius_upper") is not None:
            raise ValueError("an incomplete strong-gap cover inserted a radius")

    expected_scope = {
        "center_parameter_gamma_lower": certificate["gamma_lower"],
        "center_parameter_stable_spectral_radius_upper": certificate[
            "stable_multiplier_spectral_radius_upper"
        ],
        "quantitative_inner_strong_stable_spectral_gap_validated": promoted,
        "common_parameter_box_strong_stable_gap_validated": False,
        "stable_spectral_projection_constructed": False,
        "stable_boundary_power_bound_validated": False,
        "inner_stable_manifold_validated": False,
        "physical_pulse_onset_validated": False,
    }
    if dict(scope) != expected_scope:
        raise ValueError("the strong-gap scope ledger changed")

    expected_manifest_fields = {
        "schema_id",
        "result",
        "default_command",
        "arithmetic_scope",
        "certificate_sha256",
        "source_sha256",
        "base_gap_result",
        "base_gap_result_sha256",
        "inner_orbit_result",
        "inner_orbit_result_sha256",
        "environment",
    }
    if set(manifest) != expected_manifest_fields:
        raise ValueError("the strong-gap manifest schema changed")
    if manifest.get("schema_id") != SCHEMA_ID:
        raise ValueError("the strong-gap manifest id changed")
    if manifest.get("result") != RESULT_RELATIVE_PATH:
        raise ValueError("the strong-gap result path changed")
    if manifest.get("default_command") != DEFAULT_COMMAND:
        raise ValueError("the strong-gap replay command changed")
    if manifest.get("arithmetic_scope") != ARITHMETIC_SCOPE:
        raise ValueError("the strong-gap arithmetic scope changed")
    if manifest.get("certificate_sha256") != canonical_sha256(certificate):
        raise ValueError("the strong-gap certificate digest changed")
    source_hashes = _mapping(manifest.get("source_sha256"), "source manifest")
    if set(source_hashes) != set(SOURCE_MANIFEST):
        raise ValueError("the strong-gap source set changed")
    for relative in SOURCE_MANIFEST:
        if source_hashes.get(relative) != _sha256_path(repository / relative):
            raise ValueError(f"the strong-gap source changed: {relative}")
    parent_paths = {
        "base_gap_result": BASE_GAP_RESULT_RELATIVE_PATH,
        "inner_orbit_result": str(certificate["inner_orbit_result"]),
    }
    for name, relative in parent_paths.items():
        if manifest.get(name) != relative:
            raise ValueError(f"the strong-gap parent path changed: {name}")
        if manifest.get(name + "_sha256") != _sha256_path(
            repository / relative
        ):
            raise ValueError(f"the strong-gap parent hash changed: {name}")
    if base_gap.get("gamma_lower") != certificate.get("base_gamma_lower"):
        raise ValueError("the strong-gap base seam changed")


__all__ = [
    "ACCEPTANCE_THRESHOLD",
    "ALWAYS_FALSE",
    "BASE_GAMMA",
    "EXPECTED_COMPLETE_LEAF_PARTITION_SHA256",
    "EXPECTED_CERTIFICATE_SHA256",
    "GAMMA",
    "InnerStrongStableGapCertificate",
    "MAXIMUM_PROCESSED_CELLS",
    "RESULT_RELATIVE_PATH",
    "SCHEMA_ID",
    "SOURCE_MANIFEST",
    "STRUCTURAL_TRUE",
    "TRUE_ON_COMPLETE",
    "build_inner_strong_stable_gap_certificate",
    "build_inner_strong_stable_gap_result",
    "canonical_sha256",
    "validate_inner_strong_stable_gap_result",
]
