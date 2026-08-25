#!/usr/bin/env python3
"""Generate the source-bound high-resolution outer branch artifact."""

from __future__ import annotations

import argparse
from dataclasses import asdict
import importlib.util
import json
from pathlib import Path
import platform

import gmpy2
import numpy as np
import scipy

from canard_control.leaky_outer_high_resolution import (
    ARITHMETIC_SCOPE,
    CLAIM_STATUS,
    CONTINUATION_STEPS,
    CROSS_GRID_SIZE,
    DEFAULT_COMMAND,
    DIRECTED_CHOSEN_RADIUS,
    DIRECTED_CUTOFF,
    DIRECTED_MAXIMUM_RADIUS,
    DIRECTED_PARAMETER_INTERPRETATION,
    DIRECTED_PRECISION,
    EXPECTED_ARTIFACT_SHA256,
    GENERATOR_RELATIVE_PATH,
    NEWTON_MAX_ITERATIONS,
    NEWTON_STEP_TOLERANCE,
    NODE_COUNTS,
    OVERSAMPLING_FACTORS,
    PRIMARY_NODE_COUNT,
    REFERENCE_NODE_COUNT,
    REPRESENTATION,
    RESULT_RELATIVE_PATH,
    SCHEMA_ID,
    SOURCE_MANIFEST,
    binary64_record,
    canonical_sha256,
    cross_resolution_metrics,
    model_payload,
    resolution_record,
    validate_outer_high_resolution_artifact,
)
from canard_control.leaky_periodic_validation import (
    evaluate_leaky_periodic_radii_candidate,
)


REPOSITORY = Path(__file__).resolve().parents[1]


def _sha256(path: Path) -> str:
    from hashlib import sha256

    return sha256(path.read_bytes()).hexdigest()


def _load_parent_generator():
    path = REPOSITORY / (
        "experiments/autonomous_leaky_recovery_periodic_branch_artifact.py"
    )
    specification = importlib.util.spec_from_file_location(
        "outer_parent_branch_generator", path
    )
    if specification is None or specification.loader is None:
        raise RuntimeError("could not load the parent branch generator")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def _resolution_ladder() -> dict[int, dict[str, object]]:
    parent = _load_parent_generator()
    records: dict[int, dict[str, object]] = {}
    for count in NODE_COUNTS:
        parent.NODE_COUNT = count
        (
            unknown,
            phase_reference,
            _,
            iterations,
            final_step,
            _,
            _,
        ) = parent._continue_with_trace("outer_pulse")
        state = np.column_stack(
            (unknown[:count], unknown[count : 2 * count])
        )
        records[count] = resolution_record(
            state,
            float(unknown[-1]),
            phase_reference,
            iterations=iterations,
            final_step_inf=final_step,
        )
    return records


def _manifest(artifact: dict[str, object]) -> dict[str, object]:
    """Bind an already computed body to the current immutable sources."""

    return {
        "schema_id": SCHEMA_ID,
        "result": RESULT_RELATIVE_PATH,
        "default_command": DEFAULT_COMMAND,
        "arithmetic_scope": ARITHMETIC_SCOPE,
        "artifact_sha256": canonical_sha256(artifact),
        "source_sha256": {
            relative: _sha256(REPOSITORY / relative)
            for relative in SOURCE_MANIFEST
        },
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "gmpy2": gmpy2.__version__,
        },
    }


def build_artifact() -> dict[str, object]:
    records = _resolution_ladder()
    primary_record = records[PRIMARY_NODE_COUNT]
    reference_record = records[REFERENCE_NODE_COUNT]

    # Reuse the strict loader semantics by presenting the primary resolution
    # through its natural PeriodicOrbitCandidate fields locally.
    from canard_control.leaky_outer_high_resolution import orbit_from_resolution

    primary_orbit = orbit_from_resolution(primary_record)
    reference_orbit = orbit_from_resolution(reference_record)
    directed = evaluate_leaky_periodic_radii_candidate(
        primary_orbit,
        branch="outer_pulse",
        cutoff=DIRECTED_CUTOFF,
        precision=DIRECTED_PRECISION,
        maximum_radius=DIRECTED_MAXIMUM_RADIUS,
        chosen_radius=DIRECTED_CHOSEN_RADIUS,
    )
    directed_payload = json.loads(json.dumps(asdict(directed)))
    if (
        directed_payload["formula_adaptation_independently_audited"]
        is not True
    ):
        raise AssertionError("outer directed audit is not registered")
    for name in (
        "periodic_rfde_orbit_validated",
        "phase_bordered_rfde_inverse_validated",
    ):
        if directed_payload[name] is not True:
            raise AssertionError(f"outer proof flag {name} is not registered")
    allowed_true = {
        "translation_identity_exact_for_validated_orbit",
        "phase_bordered_rfde_inverse_validated",
        "geometric_translation_kernel_conditional_on_standard_bvp_identification",
    }
    for name, value in directed_payload["floquet"].items():
        if name == "required_next_certificates":
            continue
        if name in allowed_true:
            if value is not True:
                raise AssertionError(
                    f"outer conditional Floquet flag {name} changed"
                )
        elif value is not False:
            raise AssertionError(f"outer spectral flag {name} was promoted")

    cross = cross_resolution_metrics(
        primary_orbit.state,
        primary_orbit.period,
        reference_orbit.state,
        reference_orbit.period,
    )
    artifact = {
        "schema_id": SCHEMA_ID,
        "branch": "outer_pulse",
        "model": model_payload(),
        "representation": REPRESENTATION,
        "resolution_strategy": {
            "node_counts": list(NODE_COUNTS),
            "primary_node_count": PRIMARY_NODE_COUNT,
            "reference_node_count": REFERENCE_NODE_COUNT,
            "continuation_steps": CONTINUATION_STEPS,
            "newton_max_iterations_per_step": NEWTON_MAX_ITERATIONS,
            "newton_step_tolerance": binary64_record(
                NEWTON_STEP_TOLERANCE
            ),
            "oversampling_factors": list(OVERSAMPLING_FACTORS),
            "cross_grid_size": CROSS_GRID_SIZE,
            "directed_cutoff": DIRECTED_CUTOFF,
            "directed_parameter_interpretation": (
                DIRECTED_PARAMETER_INTERPRETATION
            ),
        },
        "resolutions": {
            str(count): records[count] for count in NODE_COUNTS
        },
        "cross_resolution": {
            "primary_node_count": PRIMARY_NODE_COUNT,
            "reference_node_count": REFERENCE_NODE_COUNT,
            "grid_size": CROSS_GRID_SIZE,
            "metrics": {
                name: binary64_record(value) for name, value in cross.items()
            },
        },
        "directed_radii_certificate": {
            "node_count": PRIMARY_NODE_COUNT,
            "settings": {
                "cutoff": DIRECTED_CUTOFF,
                "precision_bits": DIRECTED_PRECISION,
                "maximum_radius": DIRECTED_MAXIMUM_RADIUS,
                "chosen_radius": DIRECTED_CHOSEN_RADIUS,
            },
            "validation": directed_payload,
        },
        "claim_status": dict(CLAIM_STATUS),
    }
    return {"artifact": artifact, "manifest": _manifest(artifact)}


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--stdout", action="store_true")
    parser.add_argument(
        "--rebind-existing",
        action="store_true",
        help=(
            "retain a source-registered body and rebuild only its manifest; "
            "this is allowed only after EXPECTED_ARTIFACT_SHA256 is fixed"
        ),
    )
    return parser.parse_args()


def main() -> None:
    arguments = parse_arguments()
    output = arguments.output or (REPOSITORY / RESULT_RELATIVE_PATH)
    if not output.is_absolute():
        output = REPOSITORY / output
    if arguments.rebind_existing:
        if not isinstance(EXPECTED_ARTIFACT_SHA256, str):
            raise ValueError("cannot rebind an unregistered artifact body")
        existing = json.loads(output.read_text(encoding="utf-8"))
        artifact = existing.get("artifact")
        if not isinstance(artifact, dict):
            raise ValueError("existing artifact body is missing")
        if canonical_sha256(artifact) != EXPECTED_ARTIFACT_SHA256:
            raise ValueError("existing artifact body is not source registered")
        payload = {"artifact": artifact, "manifest": _manifest(artifact)}
    else:
        payload = build_artifact()
    if isinstance(EXPECTED_ARTIFACT_SHA256, str):
        validate_outer_high_resolution_artifact(payload, REPOSITORY)
    encoded = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(encoded, encoding="utf-8")
    if arguments.stdout:
        print(encoded, end="")
    else:
        print(output)
        print(f"artifact_sha256={payload['manifest']['artifact_sha256']}")


if __name__ == "__main__":
    main()
