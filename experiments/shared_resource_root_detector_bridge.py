#!/usr/bin/env python3
"""Generate the one-RFDE controller-mediated root-to-detector record."""

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

import canard_control.shared_resource_root_detector_bridge as bridge_source
from canard_control.shared_resource_root_detector_bridge import (
    PARENT_PROOF_SOURCE_SHA256,
    PARENT_THEOREM_SHA256,
    reference_bridge_audits,
    reference_bridge_certificate,
)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "experiments/results/shared_resource_root_detector_bridge.json"
        ),
    )
    return parser.parse_args()


def _sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _json_value(value: Any) -> Any:
    if isinstance(value, sp.Basic):
        return sp.sstr(value)
    if isinstance(value, tuple):
        return [_json_value(item) for item in value]
    if isinstance(value, list):
        return [_json_value(item) for item in value]
    if isinstance(value, dict):
        return {key: _json_value(item) for key, item in value.items()}
    return value


def main() -> None:
    arguments = parse_arguments()
    repository = Path(__file__).resolve().parents[1]
    parent_theorem = (
        repository / "docs/paper-ii-heterogeneous-curvature-selected-root.md"
    )
    parent_source = (
        repository / "src/canard_control/heterogeneous_curvature_root.py"
    )
    if _sha256(parent_theorem) != PARENT_THEOREM_SHA256:
        raise ValueError("selected-root parent theorem digest changed")
    if _sha256(parent_source) != PARENT_PROOF_SOURCE_SHA256:
        raise ValueError("selected-root parent proof-source digest changed")

    source_path = Path(bridge_source.__file__).resolve()
    generator_path = Path(__file__).resolve()
    payload = {
        "provenance": {
            "generator": str(generator_path.relative_to(repository)),
            "generator_sha256": _sha256(generator_path),
            "proof_source": str(source_path.relative_to(repository)),
            "proof_source_sha256": _sha256(source_path),
            "parent_theorem": str(parent_theorem.relative_to(repository)),
            "parent_theorem_sha256": _sha256(parent_theorem),
            "parent_proof_source": str(parent_source.relative_to(repository)),
            "parent_proof_source_sha256": _sha256(parent_source),
            "argv": [
                sys.executable,
                "experiments/shared_resource_root_detector_bridge.py",
            ],
            "default_command": (
                "PYTHONPATH=build/testdeps:src /usr/bin/python3 "
                "experiments/shared_resource_root_detector_bridge.py"
            ),
            "python": platform.python_version(),
            "platform": platform.platform(),
            "arithmetic": (
                "exact SymPy cancellation, separable latency, reset "
                "derivative, and selected-root/latency composition; the "
                "invariant history graph and root remainder are inherited "
                "from the pinned analytic parent theorem"
            ),
        },
        "certificate": _json_value(asdict(reference_bridge_certificate())),
        "sample_exact_audits": [
            _json_value(asdict(audit)) for audit in reference_bridge_audits()
        ],
        "scope": {
            "same_underlying_shared_resource_rfde_for_root_and_control_stages": True,
            "one_shared_recovery_coordinate": True,
            "bounded_exact_model_complete_history_preparation": True,
            "controlled_detector_hit": True,
            "exact_detector_latency": True,
            "exact_root_and_model_known_offline_required": True,
            "policy_offset_changes_latency_without_changing_uncontrolled_root": True,
            "controller_mediated_nonzero_root_to_latency_response": True,
            "selected_root_equals_controlled_detector_boundary": False,
            "input_policy_independent_root_to_latency_relation": False,
            "physical_outer_selection": False,
            "unforced_onset": False,
            "maximal_canard_onset": False,
            "autonomous_biological_pulse": False,
            "biological_basin": False,
            "no_return": False,
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
