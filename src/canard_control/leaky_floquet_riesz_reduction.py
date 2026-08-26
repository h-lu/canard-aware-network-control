"""Finite analytic Riesz reduction for the two leaky Floquet branches.

For the logarithmic Floquet pencil ``L_s`` this module proves, branch by
branch, that the Fourier tail is uniformly invertible on the closed principal
right half strip.  Analytic Schur equivalence then reduces every remaining
characteristic value to a finite matrix determinant.  It also excludes a
far right half-plane and extends the already validated local neutral estimate
to a punctured complex half-disk.

The finite determinant winding and the two unstable indices are deliberately
left open.  This module removes the infinite tail; it does not manufacture
the missing integer.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from functools import lru_cache
from hashlib import sha256
import json
from pathlib import Path
import platform
from typing import Any, Mapping

import gmpy2
import numpy as np
import scipy

from canard_control.directed_interval import (
    DirectedInterval,
    decimal_lower,
    decimal_upper,
    pi_interval,
    upward_sum,
)
from canard_control.fhn_periodic_infinite_validation import (
    _sequence_box_norm_upper,
)
from canard_control.leaky_floquet_transfer import (
    RESULT_RELATIVE_PATH as FLOQUET_RESULT_RELATIVE_PATH,
    load_validated_leaky_orbit_evidence,
    validate_leaky_floquet_transfer_artifact,
)
from canard_control.leaky_periodic_validation import (
    _build_leaky_base_sequences,
)


SCHEMA_ID = "leaky-floquet-riesz-reduction-v1"
SOURCE_RELATIVE_PATH = "src/canard_control/leaky_floquet_riesz_reduction.py"
GENERATOR_RELATIVE_PATH = "experiments/leaky_floquet_riesz_reduction.py"
NOTE_RELATIVE_PATH = "docs/leaky-floquet-riesz-reduction.md"
RESULT_RELATIVE_PATH = "experiments/results/leaky_floquet_riesz_reduction.json"
DEFAULT_COMMAND = (
    "OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONPATH=src "
    "/usr/bin/python3 experiments/leaky_floquet_riesz_reduction.py"
)
ARITHMETIC_SCOPE = (
    "exact analytic Schur/Fredholm equivalence and 160-bit MPFR outward "
    "Wiener majorants around the two source-validated orbit balls; no finite "
    "determinant winding or unstable-index claim"
)
SOURCE_MANIFEST = (
    SOURCE_RELATIVE_PATH,
    GENERATOR_RELATIVE_PATH,
    NOTE_RELATIVE_PATH,
    "src/canard_control/leaky_floquet_transfer.py",
    "src/canard_control/leaky_periodic_validation.py",
    "src/canard_control/fhn_periodic_infinite_validation.py",
    "src/canard_control/directed_interval.py",
)

PRECISION_BITS = 160
FOURIER_CUTOFF = 64
TAIL_DIAGONAL_GAP_MULTIPLIER = 2 * (FOURIER_CUTOFF + 1) - 1
OUTER_REAL_PART = 256

TRUE_FLAGS = (
    "principal_logarithmic_strip_covers_all_nonzero_unstable_multipliers",
    "uniform_tail_block_invertible_on_closed_right_half_strip",
    "analytic_finite_schur_reduction_proved",
    "analytic_characteristic_multiplicity_preserved_by_schur_reduction",
    "outer_half_plane_excluded",
    "local_complex_punctured_half_disk_excluded",
)

FALSE_FLAGS = (
    "remaining_compact_keyhole_boundary_invertibility_validated",
    "directed_finite_schur_winding_validated",
    "full_nontranslation_unit_circle_exclusion_validated",
    "unstable_multiplier_count_validated",
    "inner_saddle_floquet_index_validated",
    "outer_attracting_floquet_index_validated",
    "inner_stable_manifold_validated",
    "outer_nonlinear_attracting_block_validated",
    "physical_pulse_onset_validated",
)


@dataclass(frozen=True)
class LeakyFloquetRieszBranch:
    branch: str
    node_count: int
    candidate_fingerprint: str
    source_result: str
    source_result_sha256: str
    correction_radius: str
    precision_bits: int
    fourier_cutoff: int
    complex_finite_dimension: int
    minimum_period_lower: str
    maximum_period_upper: str
    current_coefficient_center_wiener_upper: str
    current_coefficient_variation_upper: str
    current_coefficient_uniform_wiener_upper: str
    delayed_coefficient_center_sum_wiener_upper: str
    delayed_coefficient_variation_sum_upper: str
    delayed_coefficient_uniform_sum_wiener_upper: str
    recovery_voltage_column_upper: str
    recovery_input_column_upper: str
    complex_modulus_lower_order_norm_upper: str
    tail_diagonal_gap_lower: str
    tail_contraction_upper: str
    outer_real_part: str
    outer_half_plane_contraction_upper: str
    bordered_inverse_norm_upper: str
    local_complex_first_order_coefficient_upper: str
    local_complex_second_order_coefficient_upper: str
    local_complex_exclusion_radius_lower: str
    local_keyhole_radius: str
    principal_logarithmic_strip_covers_all_nonzero_unstable_multipliers: bool
    uniform_tail_block_invertible_on_closed_right_half_strip: bool
    analytic_finite_schur_reduction_proved: bool
    analytic_characteristic_multiplicity_preserved_by_schur_reduction: bool
    outer_half_plane_excluded: bool
    local_complex_punctured_half_disk_excluded: bool
    remaining_compact_keyhole_boundary_invertibility_validated: bool
    directed_finite_schur_winding_validated: bool
    directed_keyhole_zero_count: int | None
    full_nontranslation_unit_circle_exclusion_validated: bool
    unstable_multiplier_count_validated: bool
    inner_saddle_floquet_index_validated: bool
    outer_attracting_floquet_index_validated: bool
    inner_stable_manifold_validated: bool
    outer_nonlinear_attracting_block_validated: bool
    physical_pulse_onset_validated: bool
    minimal_remaining_gate: str


def _sha256_path(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def canonical_sha256(value: Any) -> str:
    return sha256(
        json.dumps(
            value, sort_keys=True, separators=(",", ":"), ensure_ascii=True
        ).encode("ascii")
    ).hexdigest()


def _validate_parent(repository: Path) -> Mapping[str, Any]:
    path = repository / FLOQUET_RESULT_RELATIVE_PATH
    payload = json.loads(path.read_text(encoding="utf-8"))
    validate_leaky_floquet_transfer_artifact(payload, repository)
    return payload


@lru_cache(maxsize=2)
def _build_branch_cached(
    repository_text: str, branch: str
) -> LeakyFloquetRieszBranch:
    repository = Path(repository_text).resolve()
    parent = _validate_parent(repository)
    parent_branches = parent["artifact"]["branches"]
    parent_branch = parent_branches[branch]
    orbit, evidence = load_validated_leaky_orbit_evidence(repository, branch)
    if evidence.candidate_fingerprint != parent_branch["candidate_fingerprint"]:
        raise ValueError("the Riesz orbit differs from the Floquet parent")
    if evidence.source_result_sha256 != parent_branch["source_result_sha256"]:
        raise ValueError("the Riesz orbit evidence differs from the Floquet parent")

    precision = PRECISION_BITS
    base = _build_leaky_base_sequences(orbit, precision)
    radius = DirectedInterval.from_decimal(
        evidence.correction_radius, precision
    ).upper
    current_center = _sequence_box_norm_upper(
        base.current_coefficient, precision
    )
    delayed_centers = tuple(
        _sequence_box_norm_upper(coefficient, precision)
        for coefficient in base.delayed_coefficients
    )
    voltage_center = _sequence_box_norm_upper(base.voltage, precision)
    centered_voltage_center = _sequence_box_norm_upper(
        base.centered_voltage, precision
    )
    epsilon = base.parameters["epsilon"].upper
    kappa_3 = base.parameters["kappa_3"].upper
    one = gmpy2.mpfr(1, precision)
    two = gmpy2.mpfr(2, precision)
    three = gmpy2.mpfr(3, precision)
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        current_variation = (
            two * voltage_center * radius
            + radius * radius
            + three
            * epsilon
            * kappa_3
            * (two * centered_voltage_center * radius + radius * radius)
        )
        each_delayed_variation = (
            three
            * epsilon
            * kappa_3
            * (two * centered_voltage_center * radius + radius * radius)
            / two
        )
        delayed_center_sum = upward_sum(delayed_centers, precision)
        delayed_variation_sum = two * each_delayed_variation
        current_uniform = current_center + current_variation
        delayed_uniform_sum = delayed_center_sum + delayed_variation_sum
        recovery_voltage_column = epsilon
        recovery_input_column = one + epsilon
        lower_order = max(
            current_uniform
            + delayed_uniform_sum
            + recovery_voltage_column,
            recovery_input_column,
        )
        maximum_period = base.period.upper + radius
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        minimum_period = base.period.lower - radius
    if minimum_period <= 0:
        raise ArithmeticError("the Riesz orbit ball crosses zero period")

    pi_box = pi_interval(precision)
    if TAIL_DIAGONAL_GAP_MULTIPLIER != 129:
        raise AssertionError("the pinned Fourier tail gap is no longer 129*pi")
    tail_gap = (pi_box * TAIL_DIAGONAL_GAP_MULTIPLIER).lower
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        tail_contraction = maximum_period * lower_order / tail_gap
        outer_contraction = (
            maximum_period * lower_order / gmpy2.mpfr(OUTER_REAL_PART)
        )
    if not 0 < tail_contraction < 1:
        raise ArithmeticError("the leaky right-strip tail did not contract")
    if not 0 < outer_contraction < 1:
        raise ArithmeticError("the leaky far right half-plane did not contract")

    inverse = DirectedInterval.from_decimal(
        parent_branch["bordered_inverse_norm_upper"], precision
    )
    first = DirectedInterval.from_decimal(
        parent_branch["bloch_first_order_coefficient_upper"], precision
    )
    second = DirectedInterval.from_decimal(
        parent_branch["bloch_second_order_coefficient_upper"], precision
    )
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        first_denominator = inverse.upper * first.upper
        second_denominator = inverse.upper * second.upper
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        first_radius = one / first_denominator
        second_radius = minimum_period / second_denominator
        complex_radius = min(first_radius, second_radius, pi_box.lower) / two
        keyhole_radius = complex_radius / two
    if complex_radius <= 0 or keyhole_radius <= 0:
        raise ArithmeticError("the complex local Floquet radius vanished")
    registered_radius = DirectedInterval.from_decimal(
        parent_branch["local_phase_radius_lower"], precision
    ).lower
    if complex_radius < registered_radius:
        with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
            relative_loss = (
                registered_radius - complex_radius
            ) / registered_radius
        if relative_loss > gmpy2.mpfr("1e-40"):
            raise ArithmeticError("the complex radius disagrees with its parent")

    return LeakyFloquetRieszBranch(
        branch=branch,
        node_count=evidence.node_count,
        candidate_fingerprint=evidence.candidate_fingerprint,
        source_result=evidence.source_result,
        source_result_sha256=evidence.source_result_sha256,
        correction_radius=evidence.correction_radius,
        precision_bits=precision,
        fourier_cutoff=FOURIER_CUTOFF,
        complex_finite_dimension=2 * (2 * FOURIER_CUTOFF + 1),
        minimum_period_lower=decimal_lower(minimum_period),
        maximum_period_upper=decimal_upper(maximum_period),
        current_coefficient_center_wiener_upper=decimal_upper(current_center),
        current_coefficient_variation_upper=decimal_upper(current_variation),
        current_coefficient_uniform_wiener_upper=decimal_upper(current_uniform),
        delayed_coefficient_center_sum_wiener_upper=decimal_upper(
            delayed_center_sum
        ),
        delayed_coefficient_variation_sum_upper=decimal_upper(
            delayed_variation_sum
        ),
        delayed_coefficient_uniform_sum_wiener_upper=decimal_upper(
            delayed_uniform_sum
        ),
        recovery_voltage_column_upper=decimal_upper(recovery_voltage_column),
        recovery_input_column_upper=decimal_upper(recovery_input_column),
        complex_modulus_lower_order_norm_upper=decimal_upper(lower_order),
        tail_diagonal_gap_lower=decimal_lower(tail_gap),
        tail_contraction_upper=decimal_upper(tail_contraction),
        outer_real_part=str(OUTER_REAL_PART),
        outer_half_plane_contraction_upper=decimal_upper(outer_contraction),
        bordered_inverse_norm_upper=parent_branch[
            "bordered_inverse_norm_upper"
        ],
        local_complex_first_order_coefficient_upper=parent_branch[
            "bloch_first_order_coefficient_upper"
        ],
        local_complex_second_order_coefficient_upper=parent_branch[
            "bloch_second_order_coefficient_upper"
        ],
        local_complex_exclusion_radius_lower=decimal_lower(complex_radius),
        local_keyhole_radius=decimal_lower(keyhole_radius),
        **{name: True for name in TRUE_FLAGS},
        **{name: False for name in FALSE_FLAGS},
        directed_keyhole_zero_count=None,
        minimal_remaining_gate=(
            "validate invertibility on the compact logarithmic keyhole "
            "boundary, impose a half-open principal-log seam convention, "
            "and compute the directed 258-dimensional Schur determinant "
            "winding (outer 0, inner 1)"
        ),
    )


def build_leaky_floquet_riesz_branch(
    repository: Path, branch: str
) -> LeakyFloquetRieszBranch:
    if branch not in {"inner_saddle_candidate", "outer_pulse"}:
        raise ValueError("unknown leaky Floquet branch")
    return _build_branch_cached(str(repository.resolve()), branch)


def build_leaky_floquet_riesz_result(repository: Path) -> dict[str, Any]:
    repository = repository.resolve()
    branches = {
        branch: asdict(build_leaky_floquet_riesz_branch(repository, branch))
        for branch in ("inner_saddle_candidate", "outer_pulse")
    }
    artifact = {
        "schema_id": SCHEMA_ID,
        "theorem": {
            "logarithmic_pencil": (
                "L_s on Re(s)>=0, -pi<=Im(s)<=pi; lambda=exp(s); "
                "the two boundary copies of a negative-real multiplier "
                "must be identified before any winding count"
            ),
            "leaky_recovery_row": (
                "(d_theta+s)y_w-T*epsilon*y_v+T*epsilon*y_w"
            ),
            "tail_diagonal_gap": (
                "inf_{|k|>=65, |Im(s)|<=pi}|2*pi*i*k+s|>=129*pi"
            ),
            "complex_modulus_column_bound": (
                "max(||g||+||H_0||+||H_1||+epsilon,1+epsilon)"
            ),
            "tail_schur_formula": (
                "S(s)=P L_s P-P L_s Q (Q L_s Q)^(-1) Q L_s P"
            ),
            "analytic_equivalence": (
                "L_s is analytically equivalent to diag(S(s),Q L_s Q)"
            ),
            "finite_dimension": 2 * (2 * FOURIER_CUTOFF + 1),
            "complex_local_extension": (
                "|exp(-alpha*s)|<=1 and integral Taylor remainders for "
                "Re(s)>=0"
            ),
        },
        "branches": branches,
        "claim_status": {
            "infinite_dimensional_tail_removed_for_both_branches": True,
            "finite_258_dimensional_analytic_reduction_proved": True,
            "outer_attracting_floquet_index_validated": False,
            "inner_saddle_floquet_index_validated": False,
            "physical_pulse_onset_validated": False,
        },
    }
    sources = {
        relative: _sha256_path(repository / relative)
        for relative in SOURCE_MANIFEST
    }
    parent_path = repository / FLOQUET_RESULT_RELATIVE_PATH
    return {
        "artifact": artifact,
        "manifest": {
            "schema_id": SCHEMA_ID,
            "result": RESULT_RELATIVE_PATH,
            "default_command": DEFAULT_COMMAND,
            "arithmetic_scope": ARITHMETIC_SCOPE,
            "artifact_sha256": canonical_sha256(artifact),
            "source_sha256": sources,
            "floquet_parent_result": FLOQUET_RESULT_RELATIVE_PATH,
            "floquet_parent_result_sha256": _sha256_path(parent_path),
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


def validate_leaky_floquet_riesz_result(
    payload: Mapping[str, Any], repository: Path
) -> None:
    if not isinstance(payload, Mapping) or set(payload) != {
        "artifact",
        "manifest",
    }:
        raise ValueError("leaky Riesz result has the wrong outer schema")
    artifact = payload.get("artifact")
    manifest = payload.get("manifest")
    if not isinstance(artifact, Mapping) or not isinstance(manifest, Mapping):
        raise ValueError("leaky Riesz records must be mappings")
    if set(artifact) != {"schema_id", "theorem", "branches", "claim_status"}:
        raise ValueError("leaky Riesz artifact schema changed")
    if artifact.get("schema_id") != SCHEMA_ID:
        raise ValueError("leaky Riesz schema id changed")
    expected_claims = {
        "infinite_dimensional_tail_removed_for_both_branches": True,
        "finite_258_dimensional_analytic_reduction_proved": True,
        "outer_attracting_floquet_index_validated": False,
        "inner_saddle_floquet_index_validated": False,
        "physical_pulse_onset_validated": False,
    }
    if artifact.get("claim_status") != expected_claims:
        raise ValueError("leaky Riesz claim ledger changed")
    branches = artifact.get("branches")
    if not isinstance(branches, Mapping) or set(branches) != {
        "inner_saddle_candidate",
        "outer_pulse",
    }:
        raise ValueError("leaky Riesz branch set changed")
    expected_fields = {field.name for field in fields(LeakyFloquetRieszBranch)}
    for branch, record in branches.items():
        if not isinstance(record, Mapping) or set(record) != expected_fields:
            raise ValueError("leaky Riesz branch schema changed")
        if record.get("branch") != branch:
            raise ValueError("leaky Riesz branch label changed")
        if any(record.get(name) is not True for name in TRUE_FLAGS):
            raise ValueError("a proved leaky Riesz flag was weakened")
        if any(record.get(name) is not False for name in FALSE_FLAGS):
            raise ValueError("an open leaky Floquet flag was promoted")
        if record.get("directed_keyhole_zero_count") is not None:
            raise ValueError("an unproved leaky Riesz count was inserted")
        if not 0 < gmpy2.mpq(record["tail_contraction_upper"]) < 1:
            raise ValueError("the leaky tail contraction is not strict")
        if not 0 < gmpy2.mpq(
            record["outer_half_plane_contraction_upper"]
        ) < 1:
            raise ValueError("the leaky outer contraction is not strict")
        if record.get("complex_finite_dimension") != 258:
            raise ValueError("the leaky finite Schur dimension changed")

    # A self-hash alone does not bind theorem numbers: an altered artifact
    # could otherwise be accompanied by its newly computed digest.  Replay
    # both source-validated orbit balls and compare the canonical body.
    repository = repository.resolve()
    expected_artifact = build_leaky_floquet_riesz_result(repository)[
        "artifact"
    ]
    if canonical_sha256(artifact) != canonical_sha256(expected_artifact):
        raise ValueError("leaky Riesz artifact differs from directed replay")

    expected_manifest_keys = {
        "schema_id",
        "result",
        "default_command",
        "arithmetic_scope",
        "artifact_sha256",
        "source_sha256",
        "floquet_parent_result",
        "floquet_parent_result_sha256",
        "environment",
    }
    if set(manifest) != expected_manifest_keys:
        raise ValueError("leaky Riesz manifest schema changed")
    scalar_expected = {
        "schema_id": SCHEMA_ID,
        "result": RESULT_RELATIVE_PATH,
        "default_command": DEFAULT_COMMAND,
        "arithmetic_scope": ARITHMETIC_SCOPE,
        "floquet_parent_result": FLOQUET_RESULT_RELATIVE_PATH,
    }
    for name, expected in scalar_expected.items():
        if manifest.get(name) != expected:
            raise ValueError(f"leaky Riesz manifest {name} changed")
    if manifest.get("artifact_sha256") != canonical_sha256(artifact):
        raise ValueError("leaky Riesz artifact digest changed")
    hashes = manifest.get("source_sha256")
    if not isinstance(hashes, Mapping) or set(hashes) != set(SOURCE_MANIFEST):
        raise ValueError("leaky Riesz source manifest changed")
    for relative in SOURCE_MANIFEST:
        if hashes.get(relative) != _sha256_path(repository / relative):
            raise ValueError(f"leaky Riesz source hash changed for {relative}")
    parent_path = repository / FLOQUET_RESULT_RELATIVE_PATH
    if manifest.get("floquet_parent_result_sha256") != _sha256_path(parent_path):
        raise ValueError("leaky Riesz parent hash changed")
    _validate_parent(repository)
    expected_environment = {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "gmpy2": gmpy2.__version__,
        "mpfr": gmpy2.mpfr_version(),
    }
    if manifest.get("environment") != expected_environment:
        raise ValueError("leaky Riesz environment changed")
