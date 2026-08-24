#!/usr/bin/env python3
"""Generate the balanced general-network FHN sign-cone certificate."""

from __future__ import annotations

import argparse
from dataclasses import asdict
from hashlib import sha256
import json
from pathlib import Path
import platform
import sys

import gmpy2

import canard_control.directed_interval as directed_interval_source
import canard_control.fhn_general_network_sign_cone as theorem_source
import canard_control.fhn_same_model_separator as separator_source
from canard_control.fhn_general_network_sign_cone import (
    load_general_network_sign_cone,
    reference_general_topology_audits,
)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--separator-result",
        type=Path,
        default=Path("experiments/results/fhn_same_model_separator.json"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("experiments/results/fhn_general_network_sign_cone.json"),
    )
    parser.add_argument("--precision", type=int, default=160)
    parser.add_argument("--initial-mean-magnitude-lower", default="0.06")
    return parser.parse_args()


def _sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def main() -> None:
    arguments = parse_arguments()
    repository = Path(__file__).resolve().parents[1]
    certificate = load_general_network_sign_cone(
        arguments.separator_result,
        precision=arguments.precision,
        initial_mean_magnitude_lower=arguments.initial_mean_magnitude_lower,
    )
    source_paths = (
        Path(directed_interval_source.__file__).resolve(),
        Path(theorem_source.__file__).resolve(),
        Path(separator_source.__file__).resolve(),
    )
    separator_payload = json.loads(
        arguments.separator_result.read_text(encoding="utf-8")
    )
    audits = reference_general_topology_audits()
    payload = {
        "provenance": {
            "generator": "experiments/fhn_general_network_sign_cone.py",
            "generator_sha256": _sha256(Path(__file__).resolve()),
            "argv": [sys.executable, *sys.argv],
            "default_command": (
                "PYTHONPATH=build/testdeps:src /usr/bin/python3 "
                "experiments/fhn_general_network_sign_cone.py"
            ),
            "python": platform.python_version(),
            "platform": platform.platform(),
            "gmpy2": gmpy2.version(),
            "mpfr": gmpy2.mpfr_version(),
            "arithmetic": "exact SymPy identities and MPFR directed endpoints",
            "proof_source_manifest": {
                str(path.relative_to(repository)): _sha256(path)
                for path in source_paths
            },
        },
        "source_evidence": {
            "separator_result_sha256": certificate.separator_result_sha256,
            "separator_generator": separator_payload["provenance"]["generator"],
            "separator_generator_sha256": separator_payload["provenance"][
                "generator_sha256"
            ],
            "separator_proof_source_manifest": separator_payload["provenance"][
                "proof_source_manifest"
            ],
            "balance_assumptions": certificate.assumptions_id,
            "decision_stage_recovery_control": (
                "ideal nodewise state clamp w_i=0, stronger than a collective "
                "mean clamp"
            ),
            "orthant_boundary_interpretation": (
                "RFDE quasipositivity gives closed-orthant invariance; strict "
                "inward pointing at every zero component is not claimed"
            ),
            "first_hit_deadline_formula": "log(H/abs(pi^T*v(0)))/c_sign(H)",
            "reference_scalar_inheritance": (
                "for alpha=(1/2,1/2) and scaled delays (4,5), the synchronous "
                "periodic RFDE has the tracked scalar form"
            ),
            "staged_map_form": "Q_A(kappa_1,kappa_3,r)=(F,A,-r)",
            "exact_reference_topologies": [
                {
                    "node_count": audit.node_count,
                    "scaffold_rank": audit.scaffold_rank,
                    "delay_layer_count": audit.delay_layer_count,
                }
                for audit in audits
            ],
        },
        "certificate": asdict(certificate),
        "scope": {
            "balanced_general_topology_history_orthant_invariance": True,
            "topology_independent_nodewise_detector_first_hit": True,
            "topology_independent_finite_controlled_excursion": True,
            "synchronized_scalar_restriction_form": True,
            "staged_frequency_amplitude_reset_map_form": True,
            "bounded_actuator": False,
            "transverse_attraction": False,
            "full_network_periodic_hyperbolicity": False,
            "general_topology_canard_root_equivalence": False,
            "general_topology_three_output_target_ball": False,
            "asynchronous_frequency_amplitude_map": False,
            "strict_inward_orthant_boundary": False,
            "biological_basin": False,
            "hardware": False,
        },
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    arguments.output.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
