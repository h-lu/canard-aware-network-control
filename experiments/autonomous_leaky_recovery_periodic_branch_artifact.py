#!/usr/bin/env python3
"""Generate one source-bound leaky-recovery periodic branch artifact.

The generator repeats the branch-specific ODE initialization and the same
129-node gain continuation used by
``autonomous_leaky_recovery_bistable_probe.py``.  It then freezes the
resulting binary64 trigonometric polynomial, its final phase reference, and
the unpromoted directed-radii prototype.  It never changes an RFDE-orbit or
Floquet proof flag to true.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict
import importlib.util
import json
from pathlib import Path
import platform
import sys

import gmpy2
import numpy as np
import scipy

from canard_control.fhn_periodic_candidate import (
    FHNPeriodicParameters,
    PeriodicOrbitCandidate,
    odd_fourier_matrices,
)
from canard_control.leaky_periodic_branch_artifact import (
    ARITHMETIC_SCOPE,
    CLAIM_STATUS,
    DEFAULT_COMMANDS,
    EXPECTED_ARTIFACT_SHA256,
    MODEL_VALUES,
    PHASE_BORDER,
    REPRESENTATION,
    RESULT_RELATIVE_PATHS,
    SCHEMA_ID,
    SOURCE_MANIFEST,
    binary64_record,
    canonical_sha256,
    model_payload,
    recompute_binary64_metrics,
    validate_leaky_periodic_branch_artifact,
)
from canard_control.leaky_periodic_validation import (
    evaluate_leaky_periodic_radii_candidate,
)


REPOSITORY = Path(__file__).resolve().parents[1]
NODE_COUNT = 129
CONTINUATION_STEPS = 10
NEWTON_MAX_ITERATIONS = 14
NEWTON_STEP_TOLERANCE = 2.0e-13
OVERSAMPLING_FACTOR = 8
DIRECTED_CUTOFF = 192
DIRECTED_PRECISION = 160
DIRECTED_MAXIMUM_RADIUS = "1e-5"
DIRECTED_CHOSEN_RADIUS = "1e-5"


def _sha256(path: Path) -> str:
    from hashlib import sha256

    return sha256(path.read_bytes()).hexdigest()


def _load_parent_probe():
    path = REPOSITORY / (
        "experiments/autonomous_leaky_recovery_bistable_probe.py"
    )
    specification = importlib.util.spec_from_file_location(
        "autonomous_leaky_recovery_bistable_probe", path
    )
    if specification is None or specification.loader is None:
        raise RuntimeError("could not load the parent branch probe")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def _continue_with_trace(branch: str):
    """Repeat the parent continuation while retaining its final phase border."""

    probe = _load_parent_probe()
    derivative, _ = odd_fourier_matrices(NODE_COUNT)
    if branch == "inner_saddle_candidate":
        state, period, _, _ = probe._unstable_ode_cycle(
            node_count=NODE_COUNT,
            unfolding=float(MODEL_VALUES["unfolding_a"]),
            epsilon=float(MODEL_VALUES["epsilon"]),
        )
    elif branch == "outer_pulse":
        state, period = probe._stable_ode_cycle(
            node_count=NODE_COUNT,
            unfolding=float(MODEL_VALUES["unfolding_a"]),
            epsilon=float(MODEL_VALUES["epsilon"]),
        )
    else:
        raise ValueError("branch is not registered")

    unknown = np.concatenate((state[:, 0], state[:, 1], [period]))
    total_iterations = 0
    final_step_inf = float("inf")
    final_reference = None
    residual_inf = float("inf")
    smallest_singular = 0.0
    gain_fractions = np.linspace(0.0, 1.0, CONTINUATION_STEPS + 1)
    for gain_fraction in gain_fractions:
        reference = np.column_stack(
            (
                unknown[:NODE_COUNT],
                unknown[NODE_COUNT : 2 * NODE_COUNT],
            )
        )
        tangent = np.column_stack(
            (
                derivative @ reference[:, 0],
                derivative @ reference[:, 1],
            )
        )
        for _ in range(NEWTON_MAX_ITERATIONS):
            residual, jacobian = probe._collocation_system(
                unknown,
                unfolding=float(MODEL_VALUES["unfolding_a"]),
                epsilon=float(MODEL_VALUES["epsilon"]),
                gain_fraction=float(gain_fraction),
                kappa_1_center=float(MODEL_VALUES["kappa_1"]),
                kappa_3_center=float(MODEL_VALUES["kappa_3"]),
                derivative=derivative,
                phase_reference=reference,
                phase_tangent=tangent,
            )
            step = np.linalg.solve(jacobian, -residual)
            unknown += step
            total_iterations += 1
            final_step_inf = float(np.max(np.abs(step)))
            if final_step_inf < NEWTON_STEP_TOLERANCE:
                break
        residual, jacobian = probe._collocation_system(
            unknown,
            unfolding=float(MODEL_VALUES["unfolding_a"]),
            epsilon=float(MODEL_VALUES["epsilon"]),
            gain_fraction=float(gain_fraction),
            kappa_1_center=float(MODEL_VALUES["kappa_1"]),
            kappa_3_center=float(MODEL_VALUES["kappa_3"]),
            derivative=derivative,
            phase_reference=reference,
            phase_tangent=tangent,
        )
        residual_inf = float(np.max(np.abs(residual)))
        smallest_singular = float(
            np.linalg.svd(jacobian, compute_uv=False)[-1]
        )
        final_reference = reference
    if final_reference is None:
        raise AssertionError("continuation did not execute")
    return (
        unknown,
        final_reference,
        gain_fractions,
        total_iterations,
        final_step_inf,
        residual_inf,
        smallest_singular,
    )


def build_artifact(branch: str) -> dict[str, object]:
    (
        unknown,
        phase_reference,
        gain_fractions,
        iterations,
        final_step,
        parent_residual,
        parent_singular,
    ) = _continue_with_trace(branch)
    state = np.column_stack(
        (unknown[:NODE_COUNT], unknown[NODE_COUNT : 2 * NODE_COUNT])
    )
    period = float(unknown[-1])
    parameters = FHNPeriodicParameters(
        epsilon=float(MODEL_VALUES["epsilon"]),
        unfolding=float(MODEL_VALUES["unfolding_a"]),
        theta_0=float(MODEL_VALUES["theta_0"]),
        theta_1=float(MODEL_VALUES["theta_1"]),
        kappa_1=float(MODEL_VALUES["kappa_1"]),
        kappa_3=float(MODEL_VALUES["kappa_3"]),
    )
    metrics = recompute_binary64_metrics(
        state,
        period,
        parameters,
        phase_reference,
        oversampling_factor=OVERSAMPLING_FACTOR,
    )
    if not np.isclose(
        metrics["collocation_residual_inf"],
        parent_residual,
        rtol=0.0,
        atol=4096.0 * np.finfo(float).eps,
    ):
        raise ArithmeticError("independent collocation residual replay failed")
    if not np.isclose(
        metrics["bordered_smallest_singular_value"],
        parent_singular,
        rtol=0.0,
        atol=4096.0 * np.finfo(float).eps,
    ):
        raise ArithmeticError("independent bordered singular replay failed")

    phase_nodes = np.arange(NODE_COUNT, dtype=float) / NODE_COUNT
    orbit = PeriodicOrbitCandidate(
        parameters=parameters,
        phase_nodes=phase_nodes,
        state=state,
        period=period,
        collocation_residual_inf=metrics["collocation_residual_inf"],
        oversampled_residual_inf=metrics["oversampled_residual_inf"],
        newton_iterations=iterations,
        final_step_inf=final_step,
        spectral_tail_l1=metrics["spectral_tail_l1"],
    )
    directed = evaluate_leaky_periodic_radii_candidate(
        orbit,
        branch=branch,
        cutoff=DIRECTED_CUTOFF,
        precision=DIRECTED_PRECISION,
        maximum_radius=DIRECTED_MAXIMUM_RADIUS,
        chosen_radius=DIRECTED_CHOSEN_RADIUS,
    )
    directed_payload = json.loads(json.dumps(asdict(directed)))
    if directed_payload["formula_adaptation_independently_audited"] is not False:
        raise AssertionError("directed formula audit flag was promoted")
    for name in (
        "periodic_rfde_orbit_validated",
        "phase_bordered_rfde_inverse_validated",
    ):
        if directed_payload[name] is not False:
            raise AssertionError(f"directed proof flag {name} was promoted")
    if any(
        value is not False
        for name, value in directed_payload["floquet"].items()
        if name != "required_next_certificates"
    ):
        raise AssertionError("a directed Floquet proof flag was promoted")

    artifact = {
        "schema_id": SCHEMA_ID,
        "branch": branch,
        "model": model_payload(),
        "representation": REPRESENTATION,
        "collocation": {
            "node_count": NODE_COUNT,
            "continuation_steps": CONTINUATION_STEPS,
            "continuation_gain_fractions_binary64": [
                float(value).hex() for value in gain_fractions
            ],
            "newton_max_iterations_per_step": NEWTON_MAX_ITERATIONS,
            "newton_step_tolerance": binary64_record(
                NEWTON_STEP_TOLERANCE
            ),
            "newton_iterations": iterations,
            "oversampling_factor": OVERSAMPLING_FACTOR,
            "phase_border": PHASE_BORDER,
            "phase_nodes_binary64": [
                float(value).hex() for value in phase_nodes
            ],
            "phase_reference_binary64": [
                [float(value).hex() for value in row]
                for row in phase_reference
            ],
            "state_binary64": [
                [float(value).hex() for value in row] for row in state
            ],
            "period": binary64_record(period),
            "diagnostics": {
                name: binary64_record(value)
                for name, value in metrics.items()
            }
            | {"final_newton_step_inf": binary64_record(final_step)},
        },
        "directed_radii_prototype": {
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
    return {
        "artifact": artifact,
        "manifest": {
            "schema_id": SCHEMA_ID,
            "result": RESULT_RELATIVE_PATHS[branch],
            "default_command": DEFAULT_COMMANDS[branch],
            "arithmetic_scope": ARITHMETIC_SCOPE,
            "artifact_sha256": canonical_sha256(artifact),
            "source_sha256": {
                relative: _sha256(REPOSITORY / relative)
                for relative in SOURCE_MANIFEST
            },
            "python": platform.python_version(),
            "platform": platform.platform(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "gmpy2": gmpy2.__version__,
        },
    }


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--branch",
        choices=tuple(RESULT_RELATIVE_PATHS),
        default="inner_saddle_candidate",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="override the branch-specific tracked output path",
    )
    parser.add_argument("--stdout", action="store_true")
    return parser.parse_args()


def main() -> None:
    arguments = parse_arguments()
    payload = build_artifact(arguments.branch)
    expected = EXPECTED_ARTIFACT_SHA256[arguments.branch]
    if isinstance(expected, str) and len(expected) == 64:
        validate_leaky_periodic_branch_artifact(payload, REPOSITORY)
    output = arguments.output or (
        REPOSITORY / RESULT_RELATIVE_PATHS[arguments.branch]
    )
    if not output.is_absolute():
        output = REPOSITORY / output
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
