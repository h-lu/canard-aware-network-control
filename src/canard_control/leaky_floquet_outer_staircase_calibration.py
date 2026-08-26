"""Predetermined rectilinear ownership calibration for the outer cover.

The validated Riesz parent excludes nontranslation characteristic values in
the punctured right half-disk ``|s|<delta_outer``.  This calibration replaces
the single ``0.002`` neutral square by a finite staircase of rational
rectangles whose upper-right corners lie strictly inside that half-disk.
Each staircase rectangle is a predetermined root and is accepted exactly
once by the parent theorem.  Every complementary root and every descendant
uses the complete infinite-operator Neumann test, even if it later lies in
the circular disk.

This is a calibration artifact.  An incomplete run does not promote the
outer Floquet count or attraction index.
"""

from __future__ import annotations

from collections import deque
from dataclasses import asdict, dataclass, fields
from decimal import Decimal, localcontext
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
from typing import Any, Mapping, Sequence

import gmpy2
import numpy as np
import scipy

from canard_control.directed_interval import decimal_upper, pi_interval
from canard_control.floquet_cover_arithmetic import _binary_environment_checked
from canard_control.leaky_floquet_outer_right_half_cover import (
    BRANCH,
    COEFFICIENT_SUPPORT_RADIUS,
    FOURIER_CUTOFF,
    OUTER_REAL_PART,
    PRECISION_BITS,
    RIESZ_RESULT_RELATIVE_PATH,
    CoverLeaf,
    _Rectangle,
    _derive_nested_outer_ball,
    _fraction_text,
    _leaf_digest,
    _normalized_area_fraction,
    _prefix_complete,
    _prepare_outer_candidate,
    _rectangle_area_fraction,
    _split_rectangle,
    _validate_cell,
    _validate_sources,
)
from canard_control.leaky_periodic_validation import _build_leaky_base_sequences


SCHEMA_ID = "leaky-floquet-outer-staircase-calibration-v1"
SOURCE_RELATIVE_PATH = (
    "src/canard_control/leaky_floquet_outer_staircase_calibration.py"
)
GENERATOR_RELATIVE_PATH = (
    "experiments/leaky_floquet_outer_staircase_calibration.py"
)
NOTE_RELATIVE_PATH = "docs/leaky-floquet-outer-staircase-calibration.md"
TEST_RELATIVE_PATH = "tests/test_leaky_floquet_outer_staircase_calibration.py"
RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_floquet_outer_staircase_calibration.json"
)
DEFAULT_COMMAND = (
    "OPENBLAS_NUM_THREADS=8 PYTHONPATH=build/testdeps:src /usr/bin/python3 "
    "experiments/leaky_floquet_outer_staircase_calibration.py"
)
PINNED_OPENBLAS_NUM_THREADS = "8"
ACCEPTANCE_THRESHOLD = "0.999"
MAXIMUM_DEPTH = 88

# (lower imaginary edge, upper imaginary edge, local real ceiling).  Decimal
# literals are exact rationals in the ownership proof.
STAIRCASE_BANDS = (
    ("0", "0.0008", "0.00274"),
    ("0.0008", "0.0014", "0.00249"),
    ("0.0014", "0.0019", "0.00214"),
    ("0.0019", "0.0023", "0.00170"),
    ("0.0023", "0.0026", "0.00119"),
    ("0.0026", "0.00275", "0.00079"),
    ("0.00275", "0.00284", "0.00036"),
    ("0.00284", "0.00286", "0.00014"),
)

SOURCE_MANIFEST = (
    SOURCE_RELATIVE_PATH,
    GENERATOR_RELATIVE_PATH,
    NOTE_RELATIVE_PATH,
    "src/canard_control/directed_interval.py",
    "src/canard_control/floquet_cover_arithmetic.py",
    "src/canard_control/leaky_floquet_outer_right_half_cover.py",
    "src/canard_control/leaky_floquet_riesz_reduction.py",
    "src/canard_control/leaky_floquet_transfer.py",
    "src/canard_control/leaky_periodic_validation.py",
)

FALSE_CLAIMS = (
    "complete_nontranslation_right_half_strip_zero_free_validated",
    "outer_nontranslation_floquet_zero_count_validated",
    "center_parameter_outer_floquet_count_validated",
    "outer_nontrivial_unit_circle_exclusion_validated",
    "outer_attracting_floquet_index_validated",
    "outer_nonlinear_attracting_block_validated",
    "physical_pulse_onset_validated",
    "parameter_box_uniform_outer_floquet_count_validated",
)


@dataclass(frozen=True)
class RootDiagnostic:
    root_id: str
    proof_owner: str
    processed_cell_count: int
    accepted_leaf_count: int
    pending_cell_count: int
    pending_maximum_depth: int | None
    pending_real_lower_minimum: str | None
    pending_real_upper_maximum: str | None
    pending_phase_lower_minimum: str | None
    pending_phase_upper_maximum: str | None


@dataclass(frozen=True)
class CalibrationRun:
    maximum_processed_cells: int
    processed_cell_count: int
    accepted_leaf_count: int
    local_parent_leaf_count: int
    neumann_leaf_count: int
    pending_cell_count: int
    maximum_depth: int
    maximum_contraction_upper: str | None
    accepted_normalized_area_fraction: str
    accepted_normalized_area_decimal: str
    leaf_partition_sha256: str
    pending_partition_sha256: str
    pending_real_lower_minimum: str | None
    pending_real_upper_maximum: str | None
    pending_phase_upper_maximum: str | None
    root_diagnostics: tuple[RootDiagnostic, ...]
    prefix_complete: bool
    exact_area_complete: bool
    calibration_cover_complete: bool


@dataclass(frozen=True)
class StaircaseCalibration:
    schema_id: str
    branch: str
    precision_bits: int
    binary_blas_thread_count: int
    fourier_cutoff: int
    coefficient_support_half_bandwidth: int
    correction_radius: str
    acceptance_threshold: str
    parent_local_complex_exclusion_radius_lower: str
    staircase_band_count: int
    local_root_count: int
    complement_root_count: int
    total_root_count: int
    exact_root_partition_validated: bool
    every_local_upper_corner_strictly_inside_parent_disk: bool
    local_roots_accepted_only_at_empty_path: bool
    complement_descendants_always_use_full_neumann: bool
    low_band_phase_upper: str
    low_band_real_ceiling: str
    low_band_covers_previous_pending_real_upper: str
    low_band_covers_previous_pending_phase_upper: str
    runs: tuple[CalibrationRun, ...]
    breadth_first_all_complement_roots_receive_budget: bool
    old_depth_first_pending_count_direct_comparison_valid: bool
    final_accepted_area_exceeds_95_percent: bool
    old_square_5000_pending_count: int
    calibration_is_not_a_theorem_artifact: bool
    complete_nontranslation_right_half_strip_zero_free_validated: bool
    outer_nontranslation_floquet_zero_count_validated: bool
    center_parameter_outer_floquet_count_validated: bool
    outer_nontrivial_unit_circle_exclusion_validated: bool
    outer_attracting_floquet_index_validated: bool
    outer_nonlinear_attracting_block_validated: bool
    physical_pulse_onset_validated: bool
    parameter_box_uniform_outer_floquet_count_validated: bool
    conclusion: str


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


def _staircase_roots(phase_upper: Decimal) -> tuple[_Rectangle, ...]:
    roots: list[_Rectangle] = []
    for index, (lower, upper, ceiling) in enumerate(STAIRCASE_BANDS):
        y0 = Decimal(lower)
        y1 = Decimal(upper)
        x = Decimal(ceiling)
        roots.append(_Rectangle(f"local_{index:02d}", "", Decimal(0), x, y0, y1))
        roots.append(
            _Rectangle(
                f"complement_{index:02d}",
                "",
                x,
                OUTER_REAL_PART,
                y0,
                y1,
            )
        )
    top = Decimal(STAIRCASE_BANDS[-1][1])
    roots.append(
        _Rectangle(
            "complement_upper",
            "",
            Decimal(0),
            OUTER_REAL_PART,
            top,
            phase_upper,
        )
    )
    return tuple(roots)


def _local_root_ids() -> tuple[str, ...]:
    return tuple(f"local_{index:02d}" for index in range(len(STAIRCASE_BANDS)))


def _validate_exact_partition(
    roots: Sequence[_Rectangle],
    phase_upper: Decimal,
    local_radius: Decimal,
) -> None:
    expected = _staircase_roots(phase_upper)
    if tuple(roots) != expected:
        raise ArithmeticError("the staircase root forest changed")
    local_ids = set(_local_root_ids())
    if len({root.root_id for root in roots}) != len(roots):
        raise ArithmeticError("the staircase root ids are not unique")
    total = Fraction(OUTER_REAL_PART) * Fraction(phase_upper)
    area = sum((_rectangle_area_fraction(root) for root in roots), Fraction())
    if area != total:
        raise ArithmeticError("the staircase roots do not partition the rectangle")
    radius_squared = Fraction(local_radius) ** 2
    for root in roots:
        if root.root_id in local_ids:
            corner = Fraction(root.sigma_upper) ** 2 + Fraction(root.phase_upper) ** 2
            if not corner < radius_squared:
                raise ArithmeticError("a staircase local root escaped the parent disk")
            if root.path or root.sigma_lower != 0:
                raise ArithmeticError("a staircase local root has invalid ownership")
        elif root.root_id.startswith("local_"):
            raise ArithmeticError("an unknown staircase local root appeared")


def _pending_digest(pending: Sequence[_Rectangle]) -> str:
    records = [
        (
            item.root_id,
            item.path,
            format(item.sigma_lower, "f"),
            format(item.sigma_upper, "f"),
            format(item.phase_lower, "f"),
            format(item.phase_upper, "f"),
        )
        for item in sorted(pending, key=lambda item: (item.root_id, item.path))
    ]
    return canonical_sha256(records)


def _fraction_decimal(value: str) -> str:
    fraction = Fraction(value)
    with localcontext() as context:
        context.prec = 100
        return format(Decimal(fraction.numerator) / Decimal(fraction.denominator), "f")


def _run_cover(
    *,
    roots: tuple[_Rectangle, ...],
    candidate: Any,
    base: Any,
    correction_radius: Any,
    maximum_processed_cells: int,
) -> CalibrationRun:
    threshold = Decimal(ACCEPTANCE_THRESHOLD)
    local_ids = set(_local_root_ids())
    local_roots = tuple(root for root in roots if root.root_id in local_ids)
    pending = deque(root for root in roots if root.root_id not in local_ids)
    leaves: list[CoverLeaf] = [
        CoverLeaf(
            root_id=root.root_id,
            path="",
            proof_kind="riesz_local_disk_staircase",
            contraction_upper="0",
            finite_input_column_sum_upper="0",
            tail_input_column_sum_upper="0",
        )
        for root in local_roots
    ]
    processed = len(local_roots)
    local_count = len(local_roots)
    neumann_count = 0
    deepest = 0
    maximum_contraction: Decimal | None = None
    processed_by_root = {root.root_id: 0 for root in roots}
    accepted_by_root = {root.root_id: 0 for root in roots}
    for root in local_roots:
        processed_by_root[root.root_id] = 1
        accepted_by_root[root.root_id] = 1
    while pending and processed < maximum_processed_cells:
        rectangle = pending.popleft()
        depth = len(rectangle.path) // 2
        deepest = max(deepest, depth)
        if rectangle.root_id in local_ids:
            raise ArithmeticError("a predetermined local root entered Neumann work")
        bounds = _validate_cell(
            rectangle,
            candidate,
            base,
            correction_radius,
            PRECISION_BITS,
            threshold,
        )
        processed += 1
        processed_by_root[rectangle.root_id] += 1
        if bounds.validated:
            leaves.append(bounds.leaf)
            neumann_count += 1
            accepted_by_root[rectangle.root_id] += 1
            value = Decimal(bounds.worst.contraction_upper)
            maximum_contraction = (
                value if maximum_contraction is None else max(maximum_contraction, value)
            )
        else:
            if depth >= MAXIMUM_DEPTH:
                pending.appendleft(rectangle)
                break
            first, second = _split_rectangle(rectangle)
            pending.extend((first, second))
    complete = not pending
    prefix = complete and _prefix_complete(
        leaves, tuple(root.root_id for root in roots)
    )
    area = _normalized_area_fraction(leaves, roots)
    exact_area = complete and area == "1"
    pending_records = tuple(pending)
    pending_real_lower = min((item.sigma_lower for item in pending_records), default=None)
    pending_real_upper = max((item.sigma_upper for item in pending_records), default=None)
    pending_phase_upper = max((item.phase_upper for item in pending_records), default=None)
    diagnostics: list[RootDiagnostic] = []
    for root in roots:
        root_pending = tuple(
            item for item in pending_records if item.root_id == root.root_id
        )
        diagnostics.append(
            RootDiagnostic(
                root_id=root.root_id,
                proof_owner=(
                    "riesz_local_parent"
                    if root.root_id in local_ids
                    else "full_operator_neumann"
                ),
                processed_cell_count=processed_by_root[root.root_id],
                accepted_leaf_count=accepted_by_root[root.root_id],
                pending_cell_count=len(root_pending),
                pending_maximum_depth=(
                    None
                    if not root_pending
                    else max(len(item.path) // 2 for item in root_pending)
                ),
                pending_real_lower_minimum=(
                    None
                    if not root_pending
                    else format(min(item.sigma_lower for item in root_pending), "f")
                ),
                pending_real_upper_maximum=(
                    None
                    if not root_pending
                    else format(max(item.sigma_upper for item in root_pending), "f")
                ),
                pending_phase_lower_minimum=(
                    None
                    if not root_pending
                    else format(min(item.phase_lower for item in root_pending), "f")
                ),
                pending_phase_upper_maximum=(
                    None
                    if not root_pending
                    else format(max(item.phase_upper for item in root_pending), "f")
                ),
            )
        )
    return CalibrationRun(
        maximum_processed_cells=maximum_processed_cells,
        processed_cell_count=processed,
        accepted_leaf_count=len(leaves),
        local_parent_leaf_count=local_count,
        neumann_leaf_count=neumann_count,
        pending_cell_count=len(pending),
        maximum_depth=deepest,
        maximum_contraction_upper=(
            None if maximum_contraction is None else format(maximum_contraction, "f")
        ),
        accepted_normalized_area_fraction=area,
        accepted_normalized_area_decimal=_fraction_decimal(area),
        leaf_partition_sha256=_leaf_digest(leaves),
        pending_partition_sha256=_pending_digest(pending_records),
        pending_real_lower_minimum=(
            None if pending_real_lower is None else format(pending_real_lower, "f")
        ),
        pending_real_upper_maximum=(
            None if pending_real_upper is None else format(pending_real_upper, "f")
        ),
        pending_phase_upper_maximum=(
            None if pending_phase_upper is None else format(pending_phase_upper, "f")
        ),
        root_diagnostics=tuple(diagnostics),
        prefix_complete=prefix,
        exact_area_complete=exact_area,
        calibration_cover_complete=bool(complete and prefix and exact_area),
    )


def _require_pinned_environment() -> None:
    if os.environ.get("OPENBLAS_NUM_THREADS") != PINNED_OPENBLAS_NUM_THREADS:
        raise RuntimeError(
            "the outer staircase calibration requires OPENBLAS_NUM_THREADS=8"
        )


@lru_cache(maxsize=2)
def build_outer_staircase_calibration(repository: Path) -> StaircaseCalibration:
    _require_pinned_environment()
    repository = repository.resolve()
    riesz_payload = json.loads((repository / RIESZ_RESULT_RELATIVE_PATH).read_text())
    orbit, _, riesz = _validate_sources(repository, riesz_payload, replay_parent=True)
    nested = _derive_nested_outer_ball(repository, PRECISION_BITS)
    _binary_environment_checked()
    base = _build_leaky_base_sequences(orbit, PRECISION_BITS)
    candidate = _prepare_outer_candidate(orbit, base, PRECISION_BITS)
    phase_upper = Decimal(decimal_upper(pi_interval(PRECISION_BITS).upper))
    local_radius = Decimal(riesz["local_complex_exclusion_radius_lower"])
    roots = _staircase_roots(phase_upper)
    _validate_exact_partition(roots, phase_upper, local_radius)
    runs = tuple(
        _run_cover(
            roots=roots,
            candidate=candidate,
            base=base,
            correction_radius=nested.radius,
            maximum_processed_cells=budget,
        )
        for budget in (200, 5000)
    )
    final = runs[-1]
    return StaircaseCalibration(
        schema_id=SCHEMA_ID,
        branch=BRANCH,
        precision_bits=PRECISION_BITS,
        binary_blas_thread_count=int(PINNED_OPENBLAS_NUM_THREADS),
        fourier_cutoff=FOURIER_CUTOFF,
        coefficient_support_half_bandwidth=COEFFICIENT_SUPPORT_RADIUS,
        correction_radius="1e-8",
        acceptance_threshold=ACCEPTANCE_THRESHOLD,
        parent_local_complex_exclusion_radius_lower=str(local_radius),
        staircase_band_count=len(STAIRCASE_BANDS),
        local_root_count=len(STAIRCASE_BANDS),
        complement_root_count=len(STAIRCASE_BANDS) + 1,
        total_root_count=len(roots),
        exact_root_partition_validated=True,
        every_local_upper_corner_strictly_inside_parent_disk=True,
        local_roots_accepted_only_at_empty_path=True,
        complement_descendants_always_use_full_neumann=True,
        low_band_phase_upper=STAIRCASE_BANDS[0][1],
        low_band_real_ceiling=STAIRCASE_BANDS[0][2],
        low_band_covers_previous_pending_real_upper="0.0023",
        low_band_covers_previous_pending_phase_upper="0.00077",
        runs=runs,
        breadth_first_all_complement_roots_receive_budget=all(
            diagnostic.processed_cell_count > 0
            for diagnostic in final.root_diagnostics
            if diagnostic.proof_owner == "full_operator_neumann"
        ),
        old_depth_first_pending_count_direct_comparison_valid=False,
        final_accepted_area_exceeds_95_percent=(
            Decimal(final.accepted_normalized_area_decimal) > Decimal("0.95")
        ),
        old_square_5000_pending_count=39,
        calibration_is_not_a_theorem_artifact=True,
        **{name: False for name in FALSE_CLAIMS},
        conclusion=(
            "the predetermined staircase calibration completed the complement"
            if final.calibration_cover_complete
            else "breadth-first calibration covers more than 95 percent of the exact area and localizes every remaining root frontier, but the finite-budget complement remains incomplete"
        ),
    )


def build_outer_staircase_result(repository: Path) -> dict[str, Any]:
    repository = repository.resolve()
    calibration = json.loads(
        json.dumps(
            asdict(build_outer_staircase_calibration(repository)),
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        )
    )
    return {
        "calibration": calibration,
        "manifest": {
            "schema_id": SCHEMA_ID,
            "result": RESULT_RELATIVE_PATH,
            "default_command": DEFAULT_COMMAND,
            "calibration_sha256": canonical_sha256(calibration),
            "source_sha256": {
                relative: _sha256_path(repository / relative)
                for relative in SOURCE_MANIFEST
            },
            "riesz_result": RIESZ_RESULT_RELATIVE_PATH,
            "riesz_result_sha256": _sha256_path(
                repository / RIESZ_RESULT_RELATIVE_PATH
            ),
            "environment": {
                "python": platform.python_version(),
                "platform": platform.platform(),
                "numpy": np.__version__,
                "scipy": scipy.__version__,
                "gmpy2": gmpy2.__version__,
                "mpfr": gmpy2.mpfr_version(),
            },
        },
    }


def _subprocess_result(repository: Path) -> dict[str, Any]:
    environment = dict(os.environ)
    environment["OPENBLAS_NUM_THREADS"] = PINNED_OPENBLAS_NUM_THREADS
    source = str(repository / "src")
    inherited = environment.get("PYTHONPATH", "")
    environment["PYTHONPATH"] = source if not inherited else source + os.pathsep + inherited
    program = (
        "import json,sys; from pathlib import Path; "
        "from canard_control.leaky_floquet_outer_staircase_calibration import "
        "build_outer_staircase_result; print(json.dumps("
        "build_outer_staircase_result(Path(sys.argv[1])),sort_keys=True,"
        "separators=(',',':'),allow_nan=False))"
    )
    completed = subprocess.run(
        [sys.executable, "-c", program, str(repository)],
        cwd=repository,
        env=environment,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode:
        raise RuntimeError(completed.stderr.strip())
    return json.loads(completed.stdout)


def validate_outer_staircase_result(
    payload: Mapping[str, Any], repository: Path
) -> None:
    if not isinstance(payload, Mapping) or set(payload) != {"calibration", "manifest"}:
        raise ValueError("the staircase result schema changed")
    calibration = payload.get("calibration")
    manifest = payload.get("manifest")
    if not isinstance(calibration, Mapping) or not isinstance(manifest, Mapping):
        raise ValueError("the staircase records must be mappings")
    if set(calibration) != {field.name for field in fields(StaircaseCalibration)}:
        raise ValueError("the staircase calibration fields changed")
    if any(calibration.get(name) is not False for name in FALSE_CLAIMS):
        raise ValueError("an open outer claim was promoted by calibration")
    if calibration.get("calibration_is_not_a_theorem_artifact") is not True:
        raise ValueError("the staircase calibration was promoted to a theorem")
    if not all(
        calibration.get(name) is True
        for name in (
            "exact_root_partition_validated",
            "every_local_upper_corner_strictly_inside_parent_disk",
            "local_roots_accepted_only_at_empty_path",
            "complement_descendants_always_use_full_neumann",
        )
    ):
        raise ValueError("the exact staircase ownership contract failed")
    if manifest.get("calibration_sha256") != canonical_sha256(calibration):
        raise ValueError("the staircase calibration hash changed")
    repository = repository.resolve()
    hashes = manifest.get("source_sha256")
    if not isinstance(hashes, Mapping) or set(hashes) != set(SOURCE_MANIFEST):
        raise ValueError("the staircase source manifest changed")
    for relative in SOURCE_MANIFEST:
        if hashes.get(relative) != _sha256_path(repository / relative):
            raise ValueError(f"the staircase source changed: {relative}")
    expected = (
        build_outer_staircase_result(repository)
        if os.environ.get("OPENBLAS_NUM_THREADS") == PINNED_OPENBLAS_NUM_THREADS
        else _subprocess_result(repository)
    )
    if dict(payload) != expected:
        raise ValueError("the staircase result differs from full replay")


__all__ = [
    "ACCEPTANCE_THRESHOLD",
    "DEFAULT_COMMAND",
    "FALSE_CLAIMS",
    "RESULT_RELATIVE_PATH",
    "SOURCE_MANIFEST",
    "STAIRCASE_BANDS",
    "build_outer_staircase_calibration",
    "build_outer_staircase_result",
    "canonical_sha256",
    "validate_outer_staircase_result",
]
