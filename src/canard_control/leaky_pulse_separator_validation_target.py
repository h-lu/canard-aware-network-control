"""Source-bound numerical target for a validated pulse-separator proof.

This module narrows the existing finite-section separator diagnostic to one
third-return bracket.  It records the endpoint gap, a derivative sample
ladder, and the distance to the inner-cycle section in the solution-
determining reduced coordinates.  These numbers select tolerances for a
future directed flow/stable-graph calculation; they are not interval
enclosures and do not prove a separator, threshold, or routing theorem.
"""

from __future__ import annotations

from hashlib import sha256
import json
import math
from pathlib import Path
import platform
from typing import Any, Mapping, Sequence

import numpy as np
import scipy

from canard_control.leaky_periodic_branch_artifact import orbit_from_artifact
from canard_control.leaky_pulse_separator_candidate import (
    _history_vector,
    binary64_record,
    binary64_value,
    finite_section,
    shooting_data,
    simulate_physical_pulse,
    validate_separator_candidate_result,
)


SCHEMA_ID = "leaky-pulse-separator-validation-target-v1"
MODEL_ID = "autonomous-leaky-recovery-physical-pulse"
BRANCH = "inner_saddle_candidate"

SOURCE_RELATIVE_PATH = (
    "src/canard_control/leaky_pulse_separator_validation_target.py"
)
GENERATOR_RELATIVE_PATH = (
    "experiments/leaky_pulse_separator_validation_target.py"
)
RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_pulse_separator_validation_target.json"
)
NOTE_RELATIVE_PATH = "docs/leaky-pulse-separator-validation-contract.md"
PARENT_CANDIDATE_SOURCE_RELATIVE_PATH = (
    "src/canard_control/leaky_pulse_separator_candidate.py"
)
PARENT_CANDIDATE_RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_pulse_separator_candidate.json"
)
PARENT_ORBIT_RESULT_RELATIVE_PATH = (
    "experiments/results/autonomous_leaky_recovery_inner_branch_artifact.json"
)

DEFAULT_COMMAND = (
    "OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONPATH=src "
    "/usr/bin/python3 experiments/leaky_pulse_separator_validation_target.py"
)
ARITHMETIC_SCOPE = (
    "binary64 finite-section/RK4 monodromy data and SciPy DOP853 method-of-"
    "steps trajectories sampled on the 180-step reduced-history mesh; no "
    "directed flow enclosure, continuous-history norm enclosure, RFDE Riesz "
    "covector, stable graph, separator, onset, or routing proof"
)

SECTION_STEP_COUNT = 180
CROSSING_DEPTH = 3
BRACKET = (0.30113, 0.30114)
SAMPLE_AMPLITUDES = tuple(float(value) for value in np.linspace(*BRACKET, 9))
DERIVATIVE_STEP = 2.0e-7

# These are requested upper bounds for the future directed certificate, not
# bounds established by this binary64 target calculation.
ENDPOINT_TOTAL_ERROR_TARGET = 3.0e-5
DERIVATIVE_TOTAL_ERROR_TARGET = 5.0
LOCAL_REDUCED_HISTORY_RADIUS_TARGET = 2.0e-4

# Filled after an independently inspected ``--digest-only`` replay.
EXPECTED_TARGET_SHA256: str | None = (
    "74c5d9dc03060ef0e8ddd02ebe803dc3a0a89d2e5c5b37addd378f9f17449d84"
)

NUMERICAL_TRUE_FLAGS = (
    "narrow_third_return_sign_change_observed",
    "sampled_coordinate_strictly_decreasing_observed",
    "sampled_derivative_separated_from_zero_observed",
    "sampled_endpoint_reduced_state_inside_target_radius_observed",
    "registered_root_strictly_inside_narrow_bracket_observed",
)

PROOF_FALSE_FLAGS = (
    "continuous_reduced_history_tube_validated",
    "directed_endpoint_gap_enclosures_validated",
    "directed_uniform_gap_derivative_validated",
    "rfde_unstable_riesz_covector_validated",
    "inner_local_stable_graph_validated",
    "physical_pulse_separator_crossing_validated",
    "unique_physical_pulse_onset_validated",
    "two_sided_basin_routing_validated",
)


def canonical_sha256(value: object) -> str:
    encoded = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    return sha256(encoded).hexdigest()


def _target_row(section: Any, amplitude: float) -> dict[str, object]:
    coordinate, crossing_time, l2_distance = shooting_data(
        section,
        amplitude,
        CROSSING_DEPTH,
    )
    trajectory = simulate_physical_pulse(amplitude, section.section_voltage)
    if len(trajectory.crossings) < CROSSING_DEPTH:
        raise ArithmeticError("target trajectory has too few section returns")
    crossing = trajectory.crossings[CROSSING_DEPTH - 1]
    vector = _history_vector(trajectory, section, crossing)
    difference = vector - section.reference
    left = shooting_data(
        section,
        amplitude - DERIVATIVE_STEP,
        CROSSING_DEPTH,
    )[0]
    right = shooting_data(
        section,
        amplitude + DERIVATIVE_STEP,
        CROSSING_DEPTH,
    )[0]
    derivative = (right - left) / (2.0 * DERIVATIVE_STEP)
    return {
        "pulse_amplitude": binary64_record(amplitude),
        "third_return_coordinate": binary64_record(coordinate),
        "centered_difference_derivative": binary64_record(derivative),
        "third_return_time": binary64_record(crossing_time),
        "sampled_reduced_l2_distance": binary64_record(l2_distance),
        "sampled_reduced_sup_distance": binary64_record(
            float(np.max(np.abs(difference)))
        ),
        "sampled_voltage_history_sup_distance": binary64_record(
            float(np.max(np.abs(difference[:-1])))
        ),
        "current_recovery_difference": binary64_record(float(difference[-1])),
    }


def build_target(
    parent_candidate_payload: Mapping[str, Any],
    parent_orbit_payload: Mapping[str, Any],
    repository: Path,
) -> dict[str, object]:
    """Build the non-directed validation target body."""

    validate_separator_candidate_result(parent_candidate_payload, repository)
    artifact = parent_orbit_payload.get("artifact")
    if not isinstance(artifact, Mapping) or artifact.get("branch") != BRANCH:
        raise ValueError("the target requires the registered inner orbit")
    orbit = orbit_from_artifact(artifact)
    section = finite_section(orbit, SECTION_STEP_COUNT)
    rows = [_target_row(section, amplitude) for amplitude in SAMPLE_AMPLITUDES]
    coordinates = [
        binary64_value(row["third_return_coordinate"], "target coordinate")
        for row in rows
    ]
    derivatives = [
        binary64_value(
            row["centered_difference_derivative"], "target derivative"
        )
        for row in rows
    ]
    endpoint_sup = [
        binary64_value(
            rows[index]["sampled_reduced_sup_distance"],
            "endpoint sampled sup distance",
        )
        for index in (0, -1)
    ]
    parent_candidate = parent_candidate_payload.get("candidate")
    if not isinstance(parent_candidate, Mapping):
        raise ValueError("parent separator candidate body is missing")
    resolutions = parent_candidate.get("resolutions")
    if not isinstance(resolutions, Sequence):
        raise ValueError("parent separator resolutions are missing")
    parent_resolution = next(
        (
            row
            for row in resolutions
            if isinstance(row, Mapping)
            and row.get("step_count") == SECTION_STEP_COUNT
        ),
        None,
    )
    if not isinstance(parent_resolution, Mapping):
        raise ValueError("the selected parent separator resolution is absent")
    roots = parent_resolution.get("shooting_roots")
    if not isinstance(roots, Sequence) or len(roots) < CROSSING_DEPTH:
        raise ValueError("the selected parent third-return root is absent")
    registered_root = binary64_value(
        roots[CROSSING_DEPTH - 1]["pulse_amplitude"],
        "registered third-return root",
    )
    minimum_endpoint_margin = min(coordinates[0], -coordinates[-1])
    minimum_derivative_magnitude = min(abs(value) for value in derivatives)
    maximum_endpoint_sup_distance = max(endpoint_sup)
    if not (
        coordinates[0] > 0.0
        and coordinates[-1] < 0.0
        and all(
            right < left
            for left, right in zip(coordinates, coordinates[1:])
        )
        and all(value < -10.0 for value in derivatives)
        and BRACKET[0] < registered_root < BRACKET[1]
        and maximum_endpoint_sup_distance
        < LOCAL_REDUCED_HISTORY_RADIUS_TARGET
        and ENDPOINT_TOTAL_ERROR_TARGET < minimum_endpoint_margin
        and DERIVATIVE_TOTAL_ERROR_TARGET < minimum_derivative_magnitude
    ):
        raise ArithmeticError("the narrow separator validation target did not close")
    claims = {name: True for name in NUMERICAL_TRUE_FLAGS}
    claims.update({name: False for name in PROOF_FALSE_FLAGS})
    return {
        "schema_id": SCHEMA_ID,
        "model_id": MODEL_ID,
        "parent_branch": BRANCH,
        "selected_section_step_count": SECTION_STEP_COUNT,
        "selected_crossing_depth": CROSSING_DEPTH,
        "narrow_pulse_bracket": [binary64_record(value) for value in BRACKET],
        "derivative_step": binary64_record(DERIVATIVE_STEP),
        "sample_rows": rows,
        "registered_third_return_root": binary64_record(registered_root),
        "observed_margins": {
            "minimum_absolute_endpoint_coordinate": binary64_record(
                minimum_endpoint_margin
            ),
            "minimum_sampled_derivative_magnitude": binary64_record(
                minimum_derivative_magnitude
            ),
            "maximum_endpoint_sampled_reduced_sup_distance": binary64_record(
                maximum_endpoint_sup_distance
            ),
        },
        "requested_directed_certificate_bounds": {
            "total_endpoint_gap_error_upper": binary64_record(
                ENDPOINT_TOTAL_ERROR_TARGET
            ),
            "total_gap_derivative_error_upper": binary64_record(
                DERIVATIVE_TOTAL_ERROR_TARGET
            ),
            "local_reduced_history_radius_lower": binary64_record(
                LOCAL_REDUCED_HISTORY_RADIUS_TARGET
            ),
            "these_are_validation_targets_not_proved_bounds": True,
        },
        "claim_status": claims,
    }


def _sha256_path(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def validate_target_body(target: Mapping[str, Any]) -> None:
    expected_keys = {
        "schema_id",
        "model_id",
        "parent_branch",
        "selected_section_step_count",
        "selected_crossing_depth",
        "narrow_pulse_bracket",
        "derivative_step",
        "sample_rows",
        "registered_third_return_root",
        "observed_margins",
        "requested_directed_certificate_bounds",
        "claim_status",
    }
    if not isinstance(target, Mapping) or set(target) != expected_keys:
        raise ValueError("separator validation target schema changed")
    if target.get("schema_id") != SCHEMA_ID or target.get("model_id") != MODEL_ID:
        raise ValueError("separator validation target identity changed")
    if target.get("parent_branch") != BRANCH:
        raise ValueError("separator validation target branch changed")
    if target.get("selected_section_step_count") != SECTION_STEP_COUNT or target.get(
        "selected_crossing_depth"
    ) != CROSSING_DEPTH:
        raise ValueError("separator validation target section changed")
    bracket = target.get("narrow_pulse_bracket")
    if not isinstance(bracket, Sequence) or len(bracket) != 2:
        raise ValueError("separator validation target bracket is missing")
    if tuple(binary64_value(value, "target bracket") for value in bracket) != BRACKET:
        raise ValueError("separator validation target bracket changed")
    if binary64_value(target.get("derivative_step"), "target derivative step") != (
        DERIVATIVE_STEP
    ):
        raise ValueError("separator validation derivative step changed")
    rows = target.get("sample_rows")
    if not isinstance(rows, Sequence) or len(rows) != len(SAMPLE_AMPLITUDES):
        raise ValueError("separator validation sample ladder changed")
    coordinates: list[float] = []
    derivatives: list[float] = []
    for expected_amplitude, row in zip(SAMPLE_AMPLITUDES, rows, strict=True):
        if not isinstance(row, Mapping) or set(row) != {
            "pulse_amplitude",
            "third_return_coordinate",
            "centered_difference_derivative",
            "third_return_time",
            "sampled_reduced_l2_distance",
            "sampled_reduced_sup_distance",
            "sampled_voltage_history_sup_distance",
            "current_recovery_difference",
        }:
            raise ValueError("separator validation sample row changed")
        if binary64_value(row["pulse_amplitude"], "target amplitude") != (
            expected_amplitude
        ):
            raise ValueError("separator validation sample amplitude changed")
        coordinates.append(
            binary64_value(row["third_return_coordinate"], "target coordinate")
        )
        derivatives.append(
            binary64_value(
                row["centered_difference_derivative"], "target derivative"
            )
        )
    if not coordinates[0] > 0.0 or not coordinates[-1] < 0.0:
        raise ValueError("separator target endpoint sign change was lost")
    if any(
        right >= left
        for left, right in zip(coordinates, coordinates[1:])
    ):
        raise ValueError("separator target sampled monotonicity was lost")
    if any(value >= -10.0 for value in derivatives):
        raise ValueError("separator target derivative separation was lost")
    claims = target.get("claim_status")
    if not isinstance(claims, Mapping) or set(claims) != {
        *NUMERICAL_TRUE_FLAGS,
        *PROOF_FALSE_FLAGS,
    }:
        raise ValueError("separator validation target claim ledger changed")
    if any(claims.get(name) is not True for name in NUMERICAL_TRUE_FLAGS):
        raise ValueError("a separator target observation was weakened")
    if any(claims.get(name) is not False for name in PROOF_FALSE_FLAGS):
        raise ValueError("an unproved separator target claim was promoted")
    requested = target.get("requested_directed_certificate_bounds")
    if not isinstance(requested, Mapping) or requested.get(
        "these_are_validation_targets_not_proved_bounds"
    ) is not True:
        raise ValueError("separator validation target disclaimer was removed")
    if EXPECTED_TARGET_SHA256 is None:
        raise ValueError("separator validation target digest is unregistered")
    if canonical_sha256(target) != EXPECTED_TARGET_SHA256:
        raise ValueError("separator validation target differs from registered body")


def validate_target_result(payload: Mapping[str, Any], repository: Path) -> None:
    if not isinstance(payload, Mapping) or set(payload) != {"target", "manifest"}:
        raise ValueError("separator validation result requires target and manifest")
    target = payload.get("target")
    manifest = payload.get("manifest")
    if not isinstance(target, Mapping) or not isinstance(manifest, Mapping):
        raise ValueError("separator validation result records must be mappings")
    validate_target_body(target)
    sources = {
        "source": SOURCE_RELATIVE_PATH,
        "generator": GENERATOR_RELATIVE_PATH,
        "note": NOTE_RELATIVE_PATH,
        "parent_candidate_source": PARENT_CANDIDATE_SOURCE_RELATIVE_PATH,
        "parent_candidate_result": PARENT_CANDIDATE_RESULT_RELATIVE_PATH,
        "parent_orbit_result": PARENT_ORBIT_RESULT_RELATIVE_PATH,
    }
    expected_keys = {
        "schema_id",
        "target_sha256",
        "default_command",
        "arithmetic_scope",
        "python",
        "platform",
        "numpy",
        "scipy",
        *sources.keys(),
        *(f"{name}_sha256" for name in sources),
    }
    if set(manifest) != expected_keys:
        raise ValueError("separator validation manifest schema changed")
    if manifest.get("schema_id") != SCHEMA_ID:
        raise ValueError("separator validation manifest identity changed")
    if manifest.get("target_sha256") != canonical_sha256(target):
        raise ValueError("separator validation manifest target digest changed")
    if manifest.get("default_command") != DEFAULT_COMMAND or manifest.get(
        "arithmetic_scope"
    ) != ARITHMETIC_SCOPE:
        raise ValueError("separator validation method disclosure changed")
    versions = {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
    }
    for name, expected in versions.items():
        if manifest.get(name) != expected:
            raise ValueError(f"separator validation manifest {name} changed")
    for name, relative in sources.items():
        if manifest.get(name) != relative:
            raise ValueError(f"separator validation manifest {name} path changed")
        if manifest.get(f"{name}_sha256") != _sha256_path(repository / relative):
            raise ValueError(f"separator validation manifest {name} hash changed")


__all__ = [
    "ARITHMETIC_SCOPE",
    "DEFAULT_COMMAND",
    "EXPECTED_TARGET_SHA256",
    "GENERATOR_RELATIVE_PATH",
    "NOTE_RELATIVE_PATH",
    "PARENT_CANDIDATE_RESULT_RELATIVE_PATH",
    "PARENT_CANDIDATE_SOURCE_RELATIVE_PATH",
    "PARENT_ORBIT_RESULT_RELATIVE_PATH",
    "RESULT_RELATIVE_PATH",
    "SCHEMA_ID",
    "SOURCE_RELATIVE_PATH",
    "build_target",
    "canonical_sha256",
    "validate_target_body",
    "validate_target_result",
]
