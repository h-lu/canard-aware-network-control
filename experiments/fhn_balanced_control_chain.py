#!/usr/bin/env python3
"""Generate the balanced-general-topology bounded FHN control-chain record."""

from __future__ import annotations

import argparse
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import platform
import sys

import canard_control.fhn_balanced_control_chain as chain_source
from canard_control.fhn_balanced_control_chain import (
    BalancedControlChainSourceEvidence,
    TRACKED_AMPLITUDE_SAFETY_SHA256,
    TRACKED_BOUNDED_PREPARATION_SHA256,
    TRACKED_GENERAL_SIGN_CONE_SHA256,
    balanced_control_chain_from_payloads,
)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--bounded-preparation",
        type=Path,
        default=Path(
            "experiments/results/fhn_bounded_additive_preparation.json"
        ),
    )
    parser.add_argument(
        "--general-sign-cone",
        type=Path,
        default=Path("experiments/results/fhn_general_network_sign_cone.json"),
    )
    parser.add_argument(
        "--amplitude-safety",
        type=Path,
        default=Path(
            "experiments/results/fhn_same_model_amplitude_safety.json"
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("experiments/results/fhn_balanced_control_chain.json"),
    )
    return parser.parse_args()


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def main() -> None:
    arguments = parse_arguments()
    repository = Path(__file__).resolve().parents[1]
    parent_paths = {
        "bounded_preparation": arguments.bounded_preparation,
        "general_sign_cone": arguments.general_sign_cone,
        "amplitude_safety": arguments.amplitude_safety,
    }
    parents = {name: _load(path) for name, path in parent_paths.items()}
    evidence = BalancedControlChainSourceEvidence(
        bounded_preparation_result_sha256=_sha256(
            arguments.bounded_preparation
        ),
        general_sign_cone_result_sha256=_sha256(arguments.general_sign_cone),
        amplitude_safety_result_sha256=_sha256(arguments.amplitude_safety),
    )
    expected = (
        TRACKED_BOUNDED_PREPARATION_SHA256,
        TRACKED_GENERAL_SIGN_CONE_SHA256,
        TRACKED_AMPLITUDE_SAFETY_SHA256,
    )
    if tuple(asdict(evidence).values()) != expected:
        raise ValueError("one or more parent result digests changed")
    certificate = balanced_control_chain_from_payloads(
        parents["bounded_preparation"],
        parents["general_sign_cone"],
        parents["amplitude_safety"],
        evidence,
    )
    source_path = Path(chain_source.__file__).resolve()
    dependency_paths = (
        source_path,
        repository / "src/canard_control/fhn_bounded_additive_preparation.py",
        repository / "src/canard_control/fhn_general_network_sign_cone.py",
        repository / "src/canard_control/fhn_same_model_amplitude_safety.py",
    )
    payload = {
        "provenance": {
            "generator": str(Path(__file__).resolve().relative_to(repository)),
            "generator_sha256": _sha256(Path(__file__).resolve()),
            "proof_source": str(source_path.relative_to(repository)),
            "proof_source_sha256": _sha256(source_path),
            "proof_source_manifest": {
                str(path.relative_to(repository)): _sha256(path)
                for path in dependency_paths
            },
            "parent_result_manifest": {
                str(path.resolve().relative_to(repository)): _sha256(path)
                for path in parent_paths.values()
            },
            "parent_generator_manifest": {
                name: parents[name]["provenance"]["generator_sha256"]
                for name in parents
            },
            "argv": [sys.executable, *sys.argv],
            "default_command": (
                "PYTHONPATH=build/testdeps:src /usr/bin/python3 "
                "experiments/fhn_balanced_control_chain.py"
            ),
            "python": platform.python_version(),
            "platform": platform.platform(),
            "arithmetic": (
                "exact SymPy balance/cancellation/restriction identities, "
                "directed parent endpoints, and ceiling-rounded Decimal "
                "authority/deadline composition"
            ),
        },
        "source_evidence": asdict(evidence),
        "certificate": asdict(certificate),
        "scope": {
            "balanced_general_topology_bounded_additive_preparation_on_declared_bounded_initial_data_cylinder": True,
            "exact_complete_history_phi_r_after_finite_preparation": True,
            "bounded_mathematical_additive_actuator_on_declared_preparation_cylinder": True,
            "bounded_nodewise_recovery_cancellation_on_declared_decision_tube": True,
            "balanced_general_topology_controlled_positive_and_negative_onset": True,
            "balanced_general_topology_controlled_finite_excursion": True,
            "topology_independent_synchronous_branch_frequency_amplitude_outputs": True,
            "general_topology_synchronous_branch_frequency_amplitude_operational_safety_target_balls": True,
            "unique_preimage_in_each_translated_input_ball": True,
            "end_to_end_staged_control_chain": True,
            "rfde_phase_space_compactness": False,
            "uniform_authority_on_unbounded_initial_data": False,
            "asynchronous_frequency_amplitude_outputs": False,
            "transverse_attraction": False,
            "full_network_periodic_attraction": False,
            "unforced_onset": False,
            "maximal_canard_onset": False,
            "biological_basin": False,
            "action_potential": False,
            "general_topology_canard_root_equivalence": False,
            "model_uncertainty": False,
            "measurement_noise": False,
            "bandwidth": False,
            "slew_rate": False,
            "energy": False,
            "hardware": False,
        },
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    arguments.output.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
