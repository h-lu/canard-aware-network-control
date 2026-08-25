"""Replay contract for the high-resolution outer leaky-RFDE candidate.

This module deliberately separates three numerical objects.

* A four-level binary64 Fourier-collocation resolution ladder diagnoses the
  severe under-resolution of the original 129-node outer branch.
* The 257-node polynomial is the least ladder member whose off-grid defect is
  at the ``1e-11`` scale.  It is also the largest practical member for the
  current directed finite/tail implementation because the cubic support
  forces cutoff 384.
* The 385-node polynomial is a higher-resolution comparison object.  Its
  off-grid defect is at the binary64 noise floor, but its required cutoff 576
  makes the present directed calculation substantially more expensive.

All stored states are exact IEEE-754 binary64 trigonometric polynomials.  The
independent equation-level majorant audit in
:mod:`canard_control.leaky_periodic_majorant_audit` allows a source-locked
closed radii inequality to validate a nearby phase-fixed RFDE orbit and its
bordered derivative.  It does not identify the orbit as attracting: no
Floquet multiplicity, unit-circle exclusion, or multiplier count is inferred
from the periodic BVP calculation.
"""

from __future__ import annotations

from dataclasses import asdict
from decimal import Decimal, InvalidOperation
from hashlib import sha256
import json
import math
from pathlib import Path
import platform
from typing import Any, Mapping

import gmpy2
import numpy as np
import scipy

from canard_control.fhn_periodic_candidate import (
    FHNPeriodicParameters,
    PeriodicOrbitCandidate,
)
from canard_control.leaky_periodic_branch_artifact import (
    MODEL_VALUES,
    _binary64_array,
    _collocation_system,
    _compare_directed_replay,
    binary64_record,
    canonical_sha256,
    model_payload,
    parameters_from_model_payload,
    recompute_binary64_metrics,
)


SCHEMA_ID = "leaky-outer-high-resolution-binary64-artifact-v1"
SOURCE_RELATIVE_PATH = "src/canard_control/leaky_outer_high_resolution.py"
GENERATOR_RELATIVE_PATH = (
    "experiments/autonomous_leaky_recovery_outer_high_resolution.py"
)
PARENT_GENERATOR_RELATIVE_PATH = (
    "experiments/autonomous_leaky_recovery_periodic_branch_artifact.py"
)
PARENT_PROBE_RELATIVE_PATH = (
    "experiments/autonomous_leaky_recovery_bistable_probe.py"
)
NOTE_RELATIVE_PATH = "docs/leaky-outer-high-resolution-artifact.md"
RESULT_RELATIVE_PATH = (
    "experiments/results/"
    "autonomous_leaky_recovery_outer_high_resolution.json"
)
DEFAULT_COMMAND = (
    "OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONPATH=src "
    "/usr/bin/python3 "
    "experiments/autonomous_leaky_recovery_outer_high_resolution.py"
)

SOURCE_MANIFEST = (
    SOURCE_RELATIVE_PATH,
    GENERATOR_RELATIVE_PATH,
    PARENT_GENERATOR_RELATIVE_PATH,
    PARENT_PROBE_RELATIVE_PATH,
    NOTE_RELATIVE_PATH,
    "src/canard_control/leaky_periodic_branch_artifact.py",
    "src/canard_control/leaky_periodic_validation.py",
    "src/canard_control/leaky_periodic_majorant_audit.py",
    "docs/leaky-periodic-majorant-audit.md",
    "src/canard_control/fhn_periodic_candidate.py",
    "src/canard_control/fhn_periodic_directed_validation.py",
    "src/canard_control/fhn_periodic_infinite_validation.py",
    "src/canard_control/directed_interval.py",
)

NODE_COUNTS = (129, 193, 257, 385)
PRIMARY_NODE_COUNT = 257
REFERENCE_NODE_COUNT = 385
CONTINUATION_STEPS = 10
NEWTON_MAX_ITERATIONS = 14
NEWTON_STEP_TOLERANCE = 2.0e-13
OVERSAMPLING_FACTORS = (8, 16)
CROSS_GRID_SIZE = 6160
DIRECTED_CUTOFF = 384
DIRECTED_PRECISION = 160
DIRECTED_MAXIMUM_RADIUS = "1e-5"
DIRECTED_CHOSEN_RADIUS = "1e-5"
DIRECTED_PARAMETER_INTERPRETATION = (
    "epsilon, a, theta_0, theta_1, kappa_1, and kappa_3 are the exact "
    "shortest decimal spellings of the stored binary64 inputs; directed "
    "delays are tau_j=theta_j/sqrt(epsilon)"
)

REPRESENTATION = (
    "source-bound exact binary64 samples of four odd-grid real "
    "trigonometric polynomials; each polynomial is a numerical candidate, "
    "not an exact RFDE orbit"
)
ARITHMETIC_SCOPE = (
    "Fourier collocation, singular values, spectral tails, and cross-grid "
    "comparisons are binary64 diagnostics. The 257-node directed calculation "
    "uses MPFR-directed interval endpoints around its exact binary64 "
    "polynomial and a binary64 midpoint inverse with a directed product "
    "error bound. The leaky formula adaptation is supplied by the separate "
    "equation-level majorant audit. This validates a phase-fixed orbit and "
    "bordered inverse when the radii gate closes, but no Floquet index."
)

CLAIM_STATUS = {
    "exact_binary64_resolution_ladder_replay_artifact": True,
    "source_hash_manifest_verified": True,
    "finite_collocation_diagnostics_recomputed": True,
    "cross_resolution_diagnostics_recomputed": True,
    "directed_radii_certificate_evaluated_on_257_nodes": True,
    "directed_radii_formula_adaptation_independently_audited": True,
    "periodic_rfde_orbit_validated": True,
    "phase_bordered_rfde_inverse_validated": True,
    "neutral_multiplier_algebraically_simple_validated": False,
    "nontranslation_unit_circle_exclusion_validated": False,
    "unstable_multiplier_count_validated": False,
    "outer_attracting_floquet_index_validated": False,
}

# The artifact-body digest excludes the manifest.  It is filled only after a
# generator run and then source-registered; ``None`` keeps an ungenerated body
# from being accepted as a tracked research artifact.
EXPECTED_ARTIFACT_SHA256: str | None = (
    "91189b24c491f4d0ad3ec6a68df3f25108124566a2f89f40b9ad8aa532058a2f"
)


def _sha256_path(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _record_value(value: object, name: str) -> float:
    if not isinstance(value, Mapping) or set(value) != {
        "binary64_hex",
        "decimal",
    }:
        raise ValueError(f"{name} is not a complete binary64 record")
    hexadecimal = value.get("binary64_hex")
    decimal = value.get("decimal")
    if not isinstance(hexadecimal, str) or not isinstance(decimal, str):
        raise ValueError(f"{name} binary64 fields must be strings")
    try:
        number = float.fromhex(hexadecimal)
    except ValueError as error:
        raise ValueError(f"{name} has an invalid hexadecimal value") from error
    if (
        not math.isfinite(number)
        or number.hex() != hexadecimal
        or format(number, ".17g") != decimal
    ):
        raise ValueError(f"{name} has inconsistent binary64 encodings")
    return number


def _decimal_value(value: object, name: str) -> Decimal:
    if not isinstance(value, str):
        raise ValueError(f"{name} is not a decimal string")
    try:
        number = Decimal(value)
    except InvalidOperation as error:
        raise ValueError(f"{name} is not decimal") from error
    if not number.is_finite():
        raise ValueError(f"{name} is not finite")
    return number


def fixed_parameters() -> FHNPeriodicParameters:
    """Return the exact binary64 model parameters used by every rung."""

    return FHNPeriodicParameters(
        epsilon=float(MODEL_VALUES["epsilon"]),
        unfolding=float(MODEL_VALUES["unfolding_a"]),
        theta_0=float(MODEL_VALUES["theta_0"]),
        theta_1=float(MODEL_VALUES["theta_1"]),
        kappa_1=float(MODEL_VALUES["kappa_1"]),
        kappa_3=float(MODEL_VALUES["kappa_3"]),
    )


def trigonometric_values(
    samples: np.ndarray,
    phases: np.ndarray,
    *,
    derivative_order: int = 0,
) -> np.ndarray:
    """Evaluate the exact supplied binary64 trigonometric polynomial."""

    count = len(samples)
    coefficients = np.fft.fft(samples, axis=0) / count
    modes = np.fft.fftfreq(count, d=1.0 / count)
    multiplier = (2.0j * np.pi * modes) ** derivative_order
    if samples.ndim == 1:
        weighted = multiplier * coefficients
    elif samples.ndim == 2:
        weighted = multiplier[:, None] * coefficients
    else:
        raise ValueError("trigonometric samples must have one or two axes")
    basis = np.exp(2.0j * np.pi * phases[:, None] * modes[None, :])
    return np.asarray((basis @ weighted).real)


def resolution_metrics(
    state: np.ndarray,
    period: float,
    phase_reference: np.ndarray,
    *,
    oversampling_factor: int,
) -> dict[str, float]:
    """Return binary64 orbit-defect and bordered-conditioning diagnostics."""

    parameters = fixed_parameters()
    metrics = recompute_binary64_metrics(
        state,
        period,
        parameters,
        phase_reference,
        oversampling_factor=oversampling_factor,
    )
    _, jacobian = _collocation_system(
        state, period, parameters, phase_reference
    )
    singular_values = np.linalg.svd(jacobian, compute_uv=False)
    phases = np.arange(
        oversampling_factor * len(state), dtype=float
    ) / (oversampling_factor * len(state))
    dense = trigonometric_values(state, phases)
    metrics.update(
        {
            "bordered_largest_singular_value": float(singular_values[0]),
            "bordered_condition_number_2": float(
                singular_values[0] / singular_values[-1]
            ),
            "voltage_minimum": float(np.min(dense[:, 0])),
            "voltage_maximum": float(np.max(dense[:, 0])),
            "voltage_amplitude": float(np.ptp(dense[:, 0])),
            "frequency": float(1.0 / period),
        }
    )
    return metrics


def cross_resolution_metrics(
    primary_state: np.ndarray,
    primary_period: float,
    reference_state: np.ndarray,
    reference_period: float,
    *,
    grid_size: int = CROSS_GRID_SIZE,
) -> dict[str, float]:
    """Compare the 257- and 385-node polynomials on one common phase grid."""

    phases = np.arange(grid_size, dtype=float) / grid_size
    primary = trigonometric_values(primary_state, phases)
    reference = trigonometric_values(reference_state, phases)
    difference = np.abs(primary - reference)
    primary_derivative = trigonometric_values(
        primary_state, phases, derivative_order=1
    )
    reference_derivative = trigonometric_values(
        reference_state, phases, derivative_order=1
    )
    return {
        "period_absolute_difference": abs(primary_period - reference_period),
        "frequency_absolute_difference": abs(
            1.0 / primary_period - 1.0 / reference_period
        ),
        "state_inf_difference": float(np.max(difference)),
        "voltage_inf_difference": float(np.max(difference[:, 0])),
        "recovery_inf_difference": float(np.max(difference[:, 1])),
        "phase_derivative_inf_difference": float(
            np.max(np.abs(primary_derivative - reference_derivative))
        ),
    }


def _array_hex(array: np.ndarray) -> list[Any]:
    if array.ndim == 1:
        return [float(value).hex() for value in array]
    if array.ndim == 2:
        return [
            [float(value).hex() for value in row]
            for row in array
        ]
    raise ValueError("only vectors and matrices are serialized")


def resolution_record(
    state: np.ndarray,
    period: float,
    phase_reference: np.ndarray,
    *,
    iterations: int,
    final_step_inf: float,
) -> dict[str, object]:
    """Serialize one source-replayable binary64 resolution rung."""

    count = len(state)
    phases = np.arange(count, dtype=float) / count
    return {
        "node_count": count,
        "phase_nodes_binary64": _array_hex(phases),
        "state_binary64": _array_hex(state),
        "phase_reference_binary64": _array_hex(phase_reference),
        "period": binary64_record(period),
        "newton_iterations": iterations,
        "final_newton_step_inf": binary64_record(final_step_inf),
        "metrics": {
            str(factor): {
                name: binary64_record(value)
                for name, value in resolution_metrics(
                    state,
                    period,
                    phase_reference,
                    oversampling_factor=factor,
                ).items()
            }
            for factor in OVERSAMPLING_FACTORS
        },
    }


def orbit_from_resolution(record: Mapping[str, Any]) -> PeriodicOrbitCandidate:
    """Reconstruct the exact binary64 polynomial stored in one rung."""

    count = record.get("node_count")
    if type(count) is not int or count not in NODE_COUNTS:
        raise ValueError("resolution node count is not registered")
    phases = _binary64_array(
        record.get("phase_nodes_binary64"), "resolution phases", 1
    )
    state = _binary64_array(
        record.get("state_binary64"), "resolution state", 2
    )
    reference = _binary64_array(
        record.get("phase_reference_binary64"), "phase reference", 2
    )
    if phases.shape != (count,) or state.shape != (count, 2):
        raise ValueError("resolution grid or state has the wrong shape")
    if reference.shape != state.shape:
        raise ValueError("phase reference has the wrong shape")
    expected_phases = np.arange(count, dtype=float) / count
    if not np.array_equal(phases, expected_phases):
        raise ValueError("resolution phase grid changed")
    period = _record_value(record.get("period"), "resolution period")
    if period <= 0.0:
        raise ValueError("resolution period is not positive")
    metrics = record.get("metrics")
    if not isinstance(metrics, Mapping) or set(metrics) != {"8", "16"}:
        raise ValueError("resolution metric factors changed")
    selected = metrics["16"]
    if not isinstance(selected, Mapping):
        raise ValueError("resolution metrics must be a mapping")
    iterations = record.get("newton_iterations")
    if type(iterations) is not int or iterations <= 0:
        raise ValueError("resolution Newton count changed")
    final_step = _record_value(
        record.get("final_newton_step_inf"), "final Newton step"
    )
    return PeriodicOrbitCandidate(
        parameters=fixed_parameters(),
        phase_nodes=phases,
        state=state,
        period=period,
        collocation_residual_inf=_record_value(
            selected.get("collocation_residual_inf"),
            "collocation residual",
        ),
        oversampled_residual_inf=_record_value(
            selected.get("oversampled_residual_inf"),
            "oversampled residual",
        ),
        newton_iterations=iterations,
        final_step_inf=final_step,
        spectral_tail_l1=_record_value(
            selected.get("spectral_tail_l1"), "spectral tail"
        ),
    )


def _metric_close(observed: float, stored: float, name: str) -> None:
    tolerance = 5.0e-12 + 2.0e-9 * max(abs(observed), abs(stored))
    if abs(observed - stored) > tolerance:
        raise ValueError(f"{name} failed binary64 replay")


def _validate_proof_boundary(directed: Mapping[str, Any]) -> None:
    if directed.get("branch") != "outer_pulse":
        raise ValueError("outer directed branch label changed")
    if directed.get("directed_radii_inequality_candidate_closed") is not True:
        raise ValueError("outer directed radii inequality is not closed")
    if directed.get("formula_adaptation_independently_audited") is not True:
        raise ValueError("outer directed formula audit is not registered")
    for name in (
        "periodic_rfde_orbit_validated",
        "phase_bordered_rfde_inverse_validated",
    ):
        if directed.get(name) is not True:
            raise ValueError(f"outer proof flag {name} is not registered")
    floquet = directed.get("floquet")
    if not isinstance(floquet, Mapping):
        raise ValueError("outer Floquet contract is missing")
    allowed_true = {
        "translation_identity_exact_for_validated_orbit",
        "phase_bordered_rfde_inverse_validated",
        "geometric_translation_kernel_conditional_on_standard_bvp_identification",
    }
    for name, value in floquet.items():
        if name == "required_next_certificates":
            if not isinstance(value, list) or len(value) != 3:
                raise ValueError("outer Floquet next-certificate list changed")
        elif name in allowed_true:
            if value is not True:
                raise ValueError(f"outer conditional Floquet flag {name} changed")
        elif value is not False:
            raise ValueError(f"outer Floquet spectral flag {name} was promoted")
    finite = directed.get("finite")
    blocks = directed.get("blocks")
    correction = directed.get("correction")
    if not all(isinstance(value, Mapping) for value in (finite, blocks, correction)):
        raise ValueError("outer directed finite/tail records are missing")
    if finite.get("cutoff") != DIRECTED_CUTOFF:
        raise ValueError("outer directed cutoff changed")
    if finite.get("finite_inverse_validated") is not True:
        raise ValueError("outer finite inverse gate is not closed")
    if blocks.get("full_point_inverse_gate") is not True:
        raise ValueError("outer full point inverse gate is not closed")
    if correction.get("radii_polynomial_negative") is not True:
        raise ValueError("outer radii-polynomial sign changed")
    contraction = _decimal_value(
        correction.get("contraction_upper"), "outer contraction"
    )
    margin = _decimal_value(
        correction.get("radii_margin_lower"), "outer radii margin"
    )
    if contraction >= 1 or margin <= 0:
        raise ValueError("outer directed strict inequalities failed")
    if correction.get("bordered_inverse_norm_upper") is None:
        raise ValueError("outer bordered inverse bound is missing")


def validate_outer_high_resolution_artifact(
    payload: Mapping[str, Any],
    repository: Path,
    *,
    replay_directed: bool = False,
) -> PeriodicOrbitCandidate:
    """Validate the source lock, ladder replay, and exact claim boundary."""

    if not isinstance(payload, Mapping) or set(payload) != {
        "artifact",
        "manifest",
    }:
        raise ValueError("outer result must contain artifact and manifest")
    artifact = payload.get("artifact")
    manifest = payload.get("manifest")
    if not isinstance(artifact, Mapping) or not isinstance(manifest, Mapping):
        raise ValueError("outer artifact and manifest must be mappings")
    if set(artifact) != {
        "schema_id",
        "branch",
        "model",
        "representation",
        "resolution_strategy",
        "resolutions",
        "cross_resolution",
        "directed_radii_certificate",
        "claim_status",
    }:
        raise ValueError("outer artifact schema changed")
    if artifact.get("schema_id") != SCHEMA_ID:
        raise ValueError("outer schema id changed")
    if artifact.get("branch") != "outer_pulse":
        raise ValueError("outer branch label changed")
    if artifact.get("representation") != REPRESENTATION:
        raise ValueError("outer representation changed")
    if artifact.get("claim_status") != CLAIM_STATUS:
        raise ValueError("outer claim ledger changed")
    if not isinstance(EXPECTED_ARTIFACT_SHA256, str):
        raise ValueError("outer artifact body is not source registered")
    if canonical_sha256(artifact) != EXPECTED_ARTIFACT_SHA256:
        raise ValueError("outer artifact differs from its source-locked body")

    parsed_parameters = parameters_from_model_payload(artifact.get("model"))
    if parsed_parameters != fixed_parameters():
        raise ValueError("outer model parameters changed")
    strategy = artifact.get("resolution_strategy")
    if strategy != {
        "node_counts": list(NODE_COUNTS),
        "primary_node_count": PRIMARY_NODE_COUNT,
        "reference_node_count": REFERENCE_NODE_COUNT,
        "continuation_steps": CONTINUATION_STEPS,
        "newton_max_iterations_per_step": NEWTON_MAX_ITERATIONS,
        "newton_step_tolerance": binary64_record(NEWTON_STEP_TOLERANCE),
        "oversampling_factors": list(OVERSAMPLING_FACTORS),
        "cross_grid_size": CROSS_GRID_SIZE,
        "directed_cutoff": DIRECTED_CUTOFF,
        "directed_parameter_interpretation": DIRECTED_PARAMETER_INTERPRETATION,
    }:
        raise ValueError("outer resolution strategy changed")

    resolutions = artifact.get("resolutions")
    if not isinstance(resolutions, Mapping) or set(resolutions) != {
        str(count) for count in NODE_COUNTS
    }:
        raise ValueError("outer resolution ladder changed")
    orbits: dict[int, PeriodicOrbitCandidate] = {}
    references: dict[int, np.ndarray] = {}
    expected_metric_names = {
        "collocation_residual_inf",
        "oversampled_residual_inf",
        "bordered_smallest_singular_value",
        "spectral_tail_l1",
        "bordered_largest_singular_value",
        "bordered_condition_number_2",
        "voltage_minimum",
        "voltage_maximum",
        "voltage_amplitude",
        "frequency",
    }
    for count in NODE_COUNTS:
        record = resolutions[str(count)]
        if not isinstance(record, Mapping) or set(record) != {
            "node_count",
            "phase_nodes_binary64",
            "state_binary64",
            "phase_reference_binary64",
            "period",
            "newton_iterations",
            "final_newton_step_inf",
            "metrics",
        }:
            raise ValueError("outer resolution record schema changed")
        orbit = orbit_from_resolution(record)
        reference = _binary64_array(
            record["phase_reference_binary64"], "phase reference", 2
        )
        metrics = record["metrics"]
        for factor in OVERSAMPLING_FACTORS:
            stored = metrics[str(factor)]
            if not isinstance(stored, Mapping) or set(stored) != expected_metric_names:
                raise ValueError("outer resolution metric schema changed")
            replay = resolution_metrics(
                orbit.state,
                orbit.period,
                reference,
                oversampling_factor=factor,
            )
            for name, observed in replay.items():
                _metric_close(
                    observed,
                    _record_value(stored[name], f"{count}.{factor}.{name}"),
                    f"{count}.{factor}.{name}",
                )
        orbits[count] = orbit
        references[count] = reference

    cross = artifact.get("cross_resolution")
    if not isinstance(cross, Mapping) or set(cross) != {
        "primary_node_count",
        "reference_node_count",
        "grid_size",
        "metrics",
    }:
        raise ValueError("outer cross-resolution schema changed")
    if (
        cross.get("primary_node_count") != PRIMARY_NODE_COUNT
        or cross.get("reference_node_count") != REFERENCE_NODE_COUNT
        or cross.get("grid_size") != CROSS_GRID_SIZE
    ):
        raise ValueError("outer cross-resolution settings changed")
    cross_metrics = cross.get("metrics")
    replay_cross = cross_resolution_metrics(
        orbits[PRIMARY_NODE_COUNT].state,
        orbits[PRIMARY_NODE_COUNT].period,
        orbits[REFERENCE_NODE_COUNT].state,
        orbits[REFERENCE_NODE_COUNT].period,
    )
    if not isinstance(cross_metrics, Mapping) or set(cross_metrics) != set(
        replay_cross
    ):
        raise ValueError("outer cross-resolution metric list changed")
    for name, observed in replay_cross.items():
        _metric_close(
            observed,
            _record_value(cross_metrics[name], f"cross.{name}"),
            f"cross.{name}",
        )

    wrapper = artifact.get("directed_radii_certificate")
    if not isinstance(wrapper, Mapping) or set(wrapper) != {
        "node_count",
        "settings",
        "validation",
    }:
        raise ValueError("outer directed wrapper changed")
    if wrapper.get("node_count") != PRIMARY_NODE_COUNT:
        raise ValueError("outer directed node count changed")
    settings = wrapper.get("settings")
    if settings != {
        "cutoff": DIRECTED_CUTOFF,
        "precision_bits": DIRECTED_PRECISION,
        "maximum_radius": DIRECTED_MAXIMUM_RADIUS,
        "chosen_radius": DIRECTED_CHOSEN_RADIUS,
    }:
        raise ValueError("outer directed settings changed")
    directed = wrapper.get("validation")
    if not isinstance(directed, Mapping):
        raise ValueError("outer directed validation is missing")
    _validate_proof_boundary(directed)
    if replay_directed:
        from canard_control.leaky_periodic_validation import (
            evaluate_leaky_periodic_radii_candidate,
        )

        replay = asdict(
            evaluate_leaky_periodic_radii_candidate(
                orbits[PRIMARY_NODE_COUNT],
                branch="outer_pulse",
                cutoff=DIRECTED_CUTOFF,
                precision=DIRECTED_PRECISION,
                maximum_radius=DIRECTED_MAXIMUM_RADIUS,
                chosen_radius=DIRECTED_CHOSEN_RADIUS,
            )
        )
        _compare_directed_replay(directed, replay)

    if set(manifest) != {
        "schema_id",
        "result",
        "default_command",
        "arithmetic_scope",
        "artifact_sha256",
        "source_sha256",
        "environment",
    }:
        raise ValueError("outer manifest schema changed")
    if (
        manifest.get("schema_id") != SCHEMA_ID
        or manifest.get("result") != RESULT_RELATIVE_PATH
        or manifest.get("default_command") != DEFAULT_COMMAND
        or manifest.get("arithmetic_scope") != ARITHMETIC_SCOPE
        or manifest.get("artifact_sha256") != canonical_sha256(artifact)
    ):
        raise ValueError("outer manifest scalar changed")
    source_hashes = manifest.get("source_sha256")
    if not isinstance(source_hashes, Mapping) or set(source_hashes) != set(
        SOURCE_MANIFEST
    ):
        raise ValueError("outer source manifest changed")
    for relative in SOURCE_MANIFEST:
        if source_hashes.get(relative) != _sha256_path(repository / relative):
            raise ValueError(f"outer source hash changed for {relative}")
    environment = manifest.get("environment")
    expected_environment = {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "gmpy2": gmpy2.__version__,
    }
    if environment != expected_environment:
        raise ValueError("outer environment record changed")

    primary = orbits[PRIMARY_NODE_COUNT]
    reference = orbits[REFERENCE_NODE_COUNT]
    if primary.oversampled_residual_inf >= 1.0e-10:
        raise ValueError("257-node outer defect left the high-resolution scale")
    if reference.oversampled_residual_inf >= 2.0e-12:
        raise ValueError("385-node outer defect left the reference scale")
    if primary.spectral_tail_l1 >= 1.0e-10:
        raise ValueError("257-node outer spectral tail regressed")
    return primary


__all__ = [
    "ARITHMETIC_SCOPE",
    "CLAIM_STATUS",
    "CROSS_GRID_SIZE",
    "DEFAULT_COMMAND",
    "DIRECTED_CHOSEN_RADIUS",
    "DIRECTED_CUTOFF",
    "DIRECTED_MAXIMUM_RADIUS",
    "DIRECTED_PARAMETER_INTERPRETATION",
    "DIRECTED_PRECISION",
    "EXPECTED_ARTIFACT_SHA256",
    "GENERATOR_RELATIVE_PATH",
    "NODE_COUNTS",
    "NOTE_RELATIVE_PATH",
    "PRIMARY_NODE_COUNT",
    "REFERENCE_NODE_COUNT",
    "REPRESENTATION",
    "RESULT_RELATIVE_PATH",
    "SCHEMA_ID",
    "SOURCE_MANIFEST",
    "SOURCE_RELATIVE_PATH",
    "cross_resolution_metrics",
    "fixed_parameters",
    "orbit_from_resolution",
    "resolution_metrics",
    "resolution_record",
    "trigonometric_values",
    "validate_outer_high_resolution_artifact",
]
