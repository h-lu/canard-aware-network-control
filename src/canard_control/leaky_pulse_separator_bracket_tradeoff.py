"""Source-bound diagnostic for choosing the pulse-separator bracket.

The narrow third-return bracket was selected before a quantitative stable
graph radius was available.  This module records several wider binary64
brackets on the same finite section and exposes the tradeoff between
endpoint gap margin and endpoint distance from the inner periodic orbit.

Nothing here is directed arithmetic.  The result proves only an abstract
bracket-selection implication and records reproducible feasibility data; it
does not prove a Riesz covector, stable graph, separator, onset, or routing.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from hashlib import sha256
import json
from pathlib import Path
import platform
from typing import Any, Mapping

import numpy as np
import scipy

from canard_control.leaky_periodic_branch_artifact import orbit_from_artifact
from canard_control.leaky_pulse_separator_candidate import finite_section
from canard_control.leaky_pulse_separator_validation_target import (
    PARENT_ORBIT_RESULT_RELATIVE_PATH,
    RESULT_RELATIVE_PATH as NARROW_TARGET_RESULT_RELATIVE_PATH,
    SECTION_STEP_COUNT,
    _target_row,
    binary64_value,
    validate_target_result,
)


SCHEMA_ID = "leaky-pulse-separator-bracket-tradeoff-v1"
MODEL_ID = "autonomous-leaky-recovery-physical-pulse"
BRANCH = "inner_saddle_candidate"
SOURCE_RELATIVE_PATH = (
    "src/canard_control/leaky_pulse_separator_bracket_tradeoff.py"
)
GENERATOR_RELATIVE_PATH = (
    "experiments/leaky_pulse_separator_bracket_tradeoff.py"
)
RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_pulse_separator_bracket_tradeoff.json"
)
NOTE_RELATIVE_PATH = "docs/leaky-pulse-separator-bracket-tradeoff.md"
TEST_RELATIVE_PATH = "tests/test_leaky_pulse_separator_bracket_tradeoff.py"
DEFAULT_COMMAND = (
    "OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 "
    "PYTHONPATH=src:.venv/lib/python3.14/site-packages /usr/bin/python3 "
    "experiments/leaky_pulse_separator_bracket_tradeoff.py"
)
ARITHMETIC_SCOPE = (
    "source-bound binary64 SciPy DOP853 method-of-steps trajectories and "
    "the 180-step finite-section left coordinate; no directed flow, "
    "continuous-history enclosure, RFDE adjoint covector, stable graph, "
    "separator, onset, or basin assertion"
)

BRACKETS = (
    ("narrow", 0.30113, 0.30114),
    ("medium", 0.30110, 0.30117),
    ("wide_recommended", 0.30105, 0.30120),
    ("wide_dominated", 0.30100, 0.30120),
)
RECOMMENDED_ID = "wide_recommended"

SOURCE_MANIFEST = (
    SOURCE_RELATIVE_PATH,
    GENERATOR_RELATIVE_PATH,
    NOTE_RELATIVE_PATH,
    "src/canard_control/leaky_pulse_separator_validation_target.py",
    "src/canard_control/leaky_pulse_separator_candidate.py",
    "src/canard_control/leaky_periodic_branch_artifact.py",
    NARROW_TARGET_RESULT_RELATIVE_PATH,
    PARENT_ORBIT_RESULT_RELATIVE_PATH,
)

NUMERICAL_TRUE_FLAGS = (
    "all_selected_brackets_have_observed_endpoint_sign_change",
    "registered_candidate_root_lies_in_every_selected_bracket",
    "recommended_gap_margin_exceeds_narrow_margin_by_factor_thirteen",
    "recommended_endpoint_mesh_sup_distance_below_0_0017",
    "wide_dominated_row_is_pareto_dominated",
)
PROOF_FALSE_FLAGS = (
    "continuous_history_endpoint_tubes_validated",
    "directed_endpoint_gap_enclosures_validated",
    "directed_uniform_gap_derivative_validated",
    "rfde_unstable_riesz_covector_validated",
    "quantitative_inner_stable_graph_validated",
    "physical_pulse_separator_crossing_validated",
    "unique_physical_pulse_onset_validated",
    "two_sided_basin_routing_validated",
)


@dataclass(frozen=True)
class BracketDiagnostic:
    bracket_id: str
    lower_amplitude: str
    upper_amplitude: str
    left_coordinate: str
    right_coordinate: str
    left_centered_derivative: str
    right_centered_derivative: str
    left_reduced_mesh_sup_distance: str
    right_reduced_mesh_sup_distance: str
    minimum_endpoint_gap_margin: str
    maximum_endpoint_reduced_mesh_sup_distance: str
    observed_endpoint_sign_change: bool
    registered_candidate_root_inside: bool
    pareto_dominated: bool


@dataclass(frozen=True)
class PulseSeparatorBracketTradeoff:
    schema_id: str
    model_id: str
    parent_branch: str
    finite_section_step_count: int
    registered_candidate_root: str
    rows: tuple[BracketDiagnostic, ...]
    recommended_bracket_id: str
    recommended_minimum_endpoint_gap_margin: str
    recommended_maximum_endpoint_reduced_mesh_sup_distance: str
    recommended_to_narrow_gap_margin_ratio: str
    conditional_selection_rule: str
    interpretation: str
    claim_status: dict[str, bool]


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


def _mapping(value: Any, label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{label} is missing")
    return value


def _decimal(value: float) -> str:
    return format(float(value), ".17g")


def _row_value(row: Mapping[str, Any], key: str) -> float:
    return binary64_value(row[key], key)


def _dominates(left: BracketDiagnostic, right: BracketDiagnostic) -> bool:
    left_margin = float(left.minimum_endpoint_gap_margin)
    right_margin = float(right.minimum_endpoint_gap_margin)
    left_radius = float(left.maximum_endpoint_reduced_mesh_sup_distance)
    right_radius = float(right.maximum_endpoint_reduced_mesh_sup_distance)
    return (
        left_margin >= right_margin
        and left_radius <= right_radius
        and (left_margin > right_margin or left_radius < right_radius)
    )


def build_bracket_tradeoff(
    narrow_target_payload: Mapping[str, Any],
    orbit_payload: Mapping[str, Any],
    repository: Path,
) -> PulseSeparatorBracketTradeoff:
    """Build the non-directed bracket tradeoff on one frozen finite section."""

    validate_target_result(narrow_target_payload, repository)
    target = _mapping(narrow_target_payload.get("target"), "narrow target")
    root = binary64_value(
        target["registered_third_return_root"], "registered root"
    )
    artifact = _mapping(orbit_payload.get("artifact"), "inner orbit artifact")
    if artifact.get("branch") != BRANCH:
        raise ValueError("the bracket tradeoff requires the inner orbit")
    orbit = orbit_from_artifact(artifact)
    section = finite_section(orbit, SECTION_STEP_COUNT)

    amplitudes = sorted({value for _, lower, upper in BRACKETS for value in (lower, upper)})
    samples = {value: _target_row(section, value) for value in amplitudes}
    provisional: list[BracketDiagnostic] = []
    for bracket_id, lower, upper in BRACKETS:
        left = samples[lower]
        right = samples[upper]
        left_coordinate = _row_value(left, "third_return_coordinate")
        right_coordinate = _row_value(right, "third_return_coordinate")
        left_derivative = _row_value(left, "centered_difference_derivative")
        right_derivative = _row_value(right, "centered_difference_derivative")
        left_distance = _row_value(left, "sampled_reduced_sup_distance")
        right_distance = _row_value(right, "sampled_reduced_sup_distance")
        provisional.append(
            BracketDiagnostic(
                bracket_id=bracket_id,
                lower_amplitude=_decimal(lower),
                upper_amplitude=_decimal(upper),
                left_coordinate=_decimal(left_coordinate),
                right_coordinate=_decimal(right_coordinate),
                left_centered_derivative=_decimal(left_derivative),
                right_centered_derivative=_decimal(right_derivative),
                left_reduced_mesh_sup_distance=_decimal(left_distance),
                right_reduced_mesh_sup_distance=_decimal(right_distance),
                minimum_endpoint_gap_margin=_decimal(
                    min(left_coordinate, -right_coordinate)
                ),
                maximum_endpoint_reduced_mesh_sup_distance=_decimal(
                    max(left_distance, right_distance)
                ),
                observed_endpoint_sign_change=(
                    left_coordinate > 0 > right_coordinate
                ),
                registered_candidate_root_inside=(lower < root < upper),
                pareto_dominated=False,
            )
        )
    rows = tuple(
        BracketDiagnostic(
            **{
                **asdict(row),
                "pareto_dominated": any(
                    other.bracket_id != row.bracket_id
                    and _dominates(other, row)
                    for other in provisional
                ),
            }
        )
        for row in provisional
    )
    by_id = {row.bracket_id: row for row in rows}
    recommended = by_id[RECOMMENDED_ID]
    narrow = by_id["narrow"]
    ratio = (
        float(recommended.minimum_endpoint_gap_margin)
        / float(narrow.minimum_endpoint_gap_margin)
    )
    if not all(row.observed_endpoint_sign_change for row in rows):
        raise ArithmeticError("a selected binary64 bracket lost its sign change")
    if not all(row.registered_candidate_root_inside for row in rows):
        raise ArithmeticError("the registered candidate escaped a selected bracket")
    if ratio <= 13:
        raise ArithmeticError("the wider bracket did not improve the gap budget")
    if float(recommended.maximum_endpoint_reduced_mesh_sup_distance) >= 0.0017:
        raise ArithmeticError("the recommended endpoint left the diagnostic radius")
    if not by_id["wide_dominated"].pareto_dominated:
        raise ArithmeticError("the deliberately dominated bracket became efficient")

    claims = {name: True for name in NUMERICAL_TRUE_FLAGS}
    claims.update({name: False for name in PROOF_FALSE_FLAGS})
    return PulseSeparatorBracketTradeoff(
        schema_id=SCHEMA_ID,
        model_id=MODEL_ID,
        parent_branch=BRANCH,
        finite_section_step_count=SECTION_STEP_COUNT,
        registered_candidate_root=_decimal(root),
        rows=rows,
        recommended_bracket_id=RECOMMENDED_ID,
        recommended_minimum_endpoint_gap_margin=(
            recommended.minimum_endpoint_gap_margin
        ),
        recommended_maximum_endpoint_reduced_mesh_sup_distance=(
            recommended.maximum_endpoint_reduced_mesh_sup_distance
        ),
        recommended_to_narrow_gap_margin_ratio=_decimal(ratio),
        conditional_selection_rule=(
            "a bracket may be used only after directed bounds prove that its "
            "entire return-history tube lies in the validated stable-graph "
            "ball, both exact endpoint gaps retain opposite signs, and the "
            "exact gap derivative has one strict sign on the whole bracket"
        ),
        interpretation=(
            "if a future directed stable graph contains the recommended "
            "endpoint tubes, the wider bracket offers a substantially larger "
            "endpoint-error budget; these binary64 rows establish no premise "
            "of that conditional statement"
        ),
        claim_status=claims,
    )


def build_bracket_tradeoff_result(repository: Path) -> dict[str, Any]:
    repository = repository.resolve()
    narrow = json.loads(
        (repository / NARROW_TARGET_RESULT_RELATIVE_PATH).read_text(encoding="utf-8")
    )
    orbit = json.loads(
        (repository / PARENT_ORBIT_RESULT_RELATIVE_PATH).read_text(encoding="utf-8")
    )
    certificate = asdict(build_bracket_tradeoff(narrow, orbit, repository))
    return {
        "certificate": certificate,
        "manifest": {
            "schema_id": SCHEMA_ID,
            "result": RESULT_RELATIVE_PATH,
            "default_command": DEFAULT_COMMAND,
            "arithmetic_scope": ARITHMETIC_SCOPE,
            "certificate_sha256": canonical_sha256(certificate),
            "source_sha256": {
                relative: _sha256_path(repository / relative)
                for relative in SOURCE_MANIFEST
            },
            "environment": {
                "python": platform.python_version(),
                "platform": platform.platform(),
                "numpy": np.__version__,
                "scipy": scipy.__version__,
            },
        },
    }


def validate_bracket_tradeoff_result(
    payload: Mapping[str, Any], repository: Path
) -> None:
    if not isinstance(payload, Mapping) or set(payload) != {"certificate", "manifest"}:
        raise ValueError("the bracket tradeoff has the wrong outer schema")
    certificate = _mapping(payload.get("certificate"), "tradeoff certificate")
    manifest = _mapping(payload.get("manifest"), "tradeoff manifest")
    if set(certificate) != {
        field.name for field in fields(PulseSeparatorBracketTradeoff)
    }:
        raise ValueError("the bracket tradeoff certificate schema changed")
    if certificate.get("schema_id") != SCHEMA_ID:
        raise ValueError("the bracket tradeoff schema id changed")
    if certificate.get("model_id") != MODEL_ID or certificate.get("parent_branch") != BRANCH:
        raise ValueError("the bracket tradeoff belongs to another model")
    claims = _mapping(certificate.get("claim_status"), "tradeoff claims")
    if set(claims) != set(NUMERICAL_TRUE_FLAGS) | set(PROOF_FALSE_FLAGS):
        raise ValueError("the bracket tradeoff claim ledger changed")
    if any(claims.get(name) is not True for name in NUMERICAL_TRUE_FLAGS):
        raise ValueError("a registered bracket observation was weakened")
    if any(claims.get(name) is not False for name in PROOF_FALSE_FLAGS):
        raise ValueError("an unproved pulse claim was promoted")
    rows = certificate.get("rows")
    if not isinstance(rows, (list, tuple)) or len(rows) != len(BRACKETS):
        raise ValueError("the bracket tradeoff rows changed")
    expected_fields = {field.name for field in fields(BracketDiagnostic)}
    by_id: dict[str, Mapping[str, Any]] = {}
    for row in rows:
        mapping = _mapping(row, "bracket row")
        if set(mapping) != expected_fields:
            raise ValueError("a bracket diagnostic schema changed")
        by_id[str(mapping["bracket_id"])] = mapping
        if mapping.get("observed_endpoint_sign_change") is not True:
            raise ValueError("a registered endpoint sign change vanished")
        if mapping.get("registered_candidate_root_inside") is not True:
            raise ValueError("the candidate root escaped a bracket")
    if set(by_id) != {item[0] for item in BRACKETS}:
        raise ValueError("the selected bracket ids changed")
    recommended = by_id[RECOMMENDED_ID]
    narrow = by_id["narrow"]
    if float(recommended["minimum_endpoint_gap_margin"]) <= 13 * float(
        narrow["minimum_endpoint_gap_margin"]
    ):
        raise ValueError("the recommended gap improvement was lost")
    if float(recommended["maximum_endpoint_reduced_mesh_sup_distance"]) >= 0.0017:
        raise ValueError("the recommended mesh diagnostic left its target radius")
    if by_id["wide_dominated"].get("pareto_dominated") is not True:
        raise ValueError("the dominated bracket was misclassified")

    expected_manifest = {
        "schema_id",
        "result",
        "default_command",
        "arithmetic_scope",
        "certificate_sha256",
        "source_sha256",
        "environment",
    }
    if set(manifest) != expected_manifest:
        raise ValueError("the bracket tradeoff manifest schema changed")
    fixed = {
        "schema_id": SCHEMA_ID,
        "result": RESULT_RELATIVE_PATH,
        "default_command": DEFAULT_COMMAND,
        "arithmetic_scope": ARITHMETIC_SCOPE,
        "certificate_sha256": canonical_sha256(certificate),
    }
    if any(manifest.get(name) != value for name, value in fixed.items()):
        raise ValueError("the bracket tradeoff fixed manifest data changed")
    repository = repository.resolve()
    hashes = _mapping(manifest.get("source_sha256"), "tradeoff source hashes")
    if set(hashes) != set(SOURCE_MANIFEST):
        raise ValueError("the bracket tradeoff source set changed")
    for relative in SOURCE_MANIFEST:
        if hashes.get(relative) != _sha256_path(repository / relative):
            raise ValueError(f"the bracket tradeoff source changed: {relative}")


__all__ = [
    "ARITHMETIC_SCOPE",
    "BRACKETS",
    "DEFAULT_COMMAND",
    "GENERATOR_RELATIVE_PATH",
    "NOTE_RELATIVE_PATH",
    "NUMERICAL_TRUE_FLAGS",
    "PROOF_FALSE_FLAGS",
    "RESULT_RELATIVE_PATH",
    "SCHEMA_ID",
    "SOURCE_MANIFEST",
    "SOURCE_RELATIVE_PATH",
    "BracketDiagnostic",
    "PulseSeparatorBracketTradeoff",
    "build_bracket_tradeoff",
    "build_bracket_tradeoff_result",
    "canonical_sha256",
    "validate_bracket_tradeoff_result",
]
