#!/usr/bin/env python3
"""Generate the lifted-root/dual-scaffold incompatibility record."""

from __future__ import annotations

import argparse
from dataclasses import asdict
from hashlib import sha256
import json
from pathlib import Path
import platform
import sys
from typing import Any

import sympy as sp

import canard_control.fhn_root_periodic_compatibility as proof_source
from canard_control.fhn_root_periodic_compatibility import (
    AUTONOMOUS_HANDOFF_RESULT_SHA256,
    BALANCED_CHAIN_RESULT_SHA256,
    PERIODIC_BOX_RESULT_SHA256,
    PERIODIC_MODEL_DOC_SHA256,
    ROOT_CLASS_DOC_SHA256,
    ROOT_MODEL_SOURCE_SHA256,
    ROOT_RESPONSE_SOURCE_SHA256,
    ROOT_THEOREM_DOC_SHA256,
    reference_compatibility_audit,
    reference_compatibility_certificate,
)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "experiments/results/fhn_root_periodic_compatibility.json"
        ),
    )
    return parser.parse_args()


def _sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _json_value(value: Any) -> Any:
    if isinstance(value, sp.MatrixBase):
        return [[sp.sstr(item) for item in row] for row in value.tolist()]
    if isinstance(value, sp.Basic):
        return sp.sstr(value)
    if isinstance(value, tuple):
        return [_json_value(item) for item in value]
    if isinstance(value, list):
        return [_json_value(item) for item in value]
    if isinstance(value, dict):
        return {key: _json_value(item) for key, item in value.items()}
    return value


def _verify_parent_hashes(repository: Path) -> dict[str, str]:
    parent_paths = {
        "root_class_doc": repository / "docs/paper-ii-lifted-two-module-class.md",
        "root_theorem_doc": repository
        / "docs/paper-ii-selected-root-lift-and-symmetry-breaking.md",
        "root_model_source": repository
        / "src/canard_control/lifted_two_module_network.py",
        "root_response_source": repository
        / "src/canard_control/lifted_selected_root_response.py",
        "periodic_model_doc": repository / "docs/two-module-reference.md",
        "periodic_box_result": repository
        / "experiments/results/fhn_periodic_parameter_box.json",
        "balanced_chain_result": repository
        / "experiments/results/fhn_balanced_control_chain.json",
        "autonomous_handoff_result": repository
        / "experiments/results/fhn_autonomous_handoff_excursion.json",
    }
    expected = {
        "root_class_doc": ROOT_CLASS_DOC_SHA256,
        "root_theorem_doc": ROOT_THEOREM_DOC_SHA256,
        "root_model_source": ROOT_MODEL_SOURCE_SHA256,
        "root_response_source": ROOT_RESPONSE_SOURCE_SHA256,
        "periodic_model_doc": PERIODIC_MODEL_DOC_SHA256,
        "periodic_box_result": PERIODIC_BOX_RESULT_SHA256,
        "balanced_chain_result": BALANCED_CHAIN_RESULT_SHA256,
        "autonomous_handoff_result": AUTONOMOUS_HANDOFF_RESULT_SHA256,
    }
    actual = {key: _sha256(path) for key, path in parent_paths.items()}
    if actual != expected:
        raise ValueError("one or more pinned parent hashes changed")
    return actual


def _read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def _verify_parent_claims(repository: Path) -> dict[str, bool]:
    periodic = _read_json(
        repository / "experiments/results/fhn_periodic_parameter_box.json"
    )
    balanced = _read_json(
        repository / "experiments/results/fhn_balanced_control_chain.json"
    )
    handoff = _read_json(
        repository / "experiments/results/fhn_autonomous_handoff_excursion.json"
    )
    periodic_validation = periodic.get("validation", {})
    balanced_certificate = balanced.get("certificate", {})
    handoff_certificate = handoff.get("certificate", {})
    handoff_scope = handoff.get("scope", {})
    checks = {
        "periodic_box_orbit_and_response_validated": (
            periodic_validation.get("all_d1_d3_d4_validated") is True
        ),
        "periodic_box_unique_extrema_validated": (
            periodic_validation.get("d3_validated") is True
        ),
        "balanced_synchronous_subspace_invariance_validated": (
            balanced_certificate.get("synchronous_subspace_invariance_validated")
            is True
        ),
        "balanced_scalar_periodic_restriction_validated": (
            balanced_certificate.get(
                "topology_independent_synchronous_scalar_restriction_validated"
            )
            is True
        ),
        "balanced_frequency_amplitude_outputs_validated": (
            balanced_certificate.get(
                "synchronous_branch_frequency_amplitude_outputs_validated"
            )
            is True
        ),
        "balanced_positive_and_negative_controlled_onset_validated": (
            balanced_certificate.get("positive_controlled_onset_validated")
            is True
            and balanced_certificate.get("negative_controlled_onset_validated")
            is True
        ),
        "handoff_pins_balanced_parent": (
            handoff_certificate.get("balanced_control_chain_result_sha256")
            == BALANCED_CHAIN_RESULT_SHA256
        ),
        "handoff_same_delayed_baseline_validated": (
            handoff_scope.get("same_delayed_fhn_baseline_model") is True
        ),
        "handoff_positive_and_negative_autonomous_excursions_validated": (
            handoff_certificate.get("positive_finite_autonomous_excursion_validated")
            is True
            and handoff_certificate.get("negative_finite_autonomous_excursion_validated")
            is True
        ),
        "handoff_rejects_autonomous_onset_and_periodic_landing": (
            handoff_certificate.get("autonomous_onset_validated") is False
            and handoff_certificate.get("landing_on_periodic_branch_validated")
            is False
        ),
    }
    if not all(checks.values()):
        raise ValueError("one or more pinned parent claims changed")
    return checks


def main() -> None:
    arguments = parse_arguments()
    repository = Path(__file__).resolve().parents[1]
    parent_hashes = _verify_parent_hashes(repository)
    parent_claim_checks = _verify_parent_claims(repository)
    source_path = Path(proof_source.__file__).resolve()
    generator_path = Path(__file__).resolve()
    payload = {
        "provenance": {
            "generator": str(generator_path.relative_to(repository)),
            "generator_sha256": _sha256(generator_path),
            "proof_source": str(source_path.relative_to(repository)),
            "proof_source_sha256": _sha256(source_path),
            "parent_sha256": parent_hashes,
            "argv": [
                sys.executable,
                "experiments/fhn_root_periodic_compatibility.py",
            ],
            "default_command": (
                "PYTHONPATH=build/testdeps:src /usr/bin/python3 "
                "experiments/fhn_root_periodic_compatibility.py"
            ),
            "python": platform.python_version(),
            "platform": platform.platform(),
            "arithmetic": (
                "exact SymPy comparison of folds, scaffolds, slow unfolding "
                "columns, two delay layers, balance residuals, and the "
                "lifted eta action on the root and periodic critical modes"
            ),
        },
        "certificate": _json_value(
            asdict(reference_compatibility_certificate())
        ),
        "exact_audit": _json_value(asdict(reference_compatibility_audit())),
        "parent_claim_checks": parent_claim_checks,
        "scope": {
            "same_nodewise_voltage_recovery_state_type": True,
            "same_local_fhn_cubic_term": True,
            "same_literal_rfde": False,
            "same_fold_state": False,
            "same_instantaneous_voltage_scaffold": False,
            "same_recovery_scaffold": False,
            "same_slow_unfolding_field": False,
            "same_delay_layers": False,
            "same_linear_current_compensator": False,
            "lifted_root_layers_satisfy_balanced_two_half_delay_class": False,
            "lifted_eta_zero_root_critical_pairing": True,
            "lifted_eta_nonzero_root_stable_forcing": True,
            "lifted_eta_preserves_periodic_synchrony": False,
            "lifted_eta_invisible_on_validated_periodic_branch": False,
            "sync_invisible_redistribution_annihilates_sync_critical_forcing": True,
            "balanced_control_and_autonomous_handoff_same_baseline": True,
            "balanced_synchronous_restriction_matches_periodic_scalar_rfde": True,
            "periodic_branch_validated_in_eta_neighborhood": False,
            "lifted_selected_root_theorem_applies_to_dual_scaffold_periodic_model": False,
            "three_input_three_output_parameter_linked_theorem": False,
            "canard_root_to_handoff_trajectory_link": False,
            "controlled_onset_to_autonomous_finite_excursion_in_balanced_model": True,
            "autonomous_onset": False,
            "biological_basin": False,
            "landing_on_periodic_branch": False,
        },
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    arguments.output.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
