#!/usr/bin/env python3
"""Generate the controlled-to-autonomous FHN handoff certificate."""

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
import canard_control.fhn_autonomous_handoff_excursion as theorem_source
import canard_control.fhn_balanced_control_chain as parent_source
from canard_control.fhn_autonomous_handoff_excursion import (
    TRACKED_BALANCED_CONTROL_CHAIN_SHA256,
    autonomous_handoff_from_payload,
    negative_autonomous_barrier_audit,
    negative_unit_handoff_obstruction_audit,
    positive_autonomous_barrier_audit,
)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--balanced-control-chain",
        type=Path,
        default=Path("experiments/results/fhn_balanced_control_chain.json"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "experiments/results/fhn_autonomous_handoff_excursion.json"
        ),
    )
    parser.add_argument("--precision", type=int, default=160)
    return parser.parse_args()


def _sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def main() -> None:
    arguments = parse_arguments()
    repository = Path(__file__).resolve().parents[1]
    parent_raw = arguments.balanced_control_chain.read_bytes()
    parent_digest = sha256(parent_raw).hexdigest()
    if parent_digest != TRACKED_BALANCED_CONTROL_CHAIN_SHA256:
        raise ValueError("balanced control-chain result digest changed")
    parent = json.loads(parent_raw)
    if not isinstance(parent, dict):
        raise ValueError("balanced control-chain result must contain an object")

    certificate = autonomous_handoff_from_payload(
        parent,
        balanced_control_chain_result_sha256=parent_digest,
        precision=arguments.precision,
    )
    positive = positive_autonomous_barrier_audit()
    negative = negative_autonomous_barrier_audit()
    obstruction = negative_unit_handoff_obstruction_audit()
    source_paths = (
        Path(theorem_source.__file__).resolve(),
        Path(directed_interval_source.__file__).resolve(),
        Path(parent_source.__file__).resolve(),
    )
    payload = {
        "provenance": {
            "generator": "experiments/fhn_autonomous_handoff_excursion.py",
            "generator_sha256": _sha256(Path(__file__).resolve()),
            "argv": [sys.executable, *sys.argv],
            "default_command": (
                "PYTHONPATH=build/testdeps:src /usr/bin/python3 "
                "experiments/fhn_autonomous_handoff_excursion.py"
            ),
            "python": platform.python_version(),
            "platform": platform.platform(),
            "gmpy2": gmpy2.version(),
            "mpfr": gmpy2.mpfr_version(),
            "arithmetic": (
                "exact SymPy frozen-delay identities, exact rational "
                "piecewise phase barriers, and MPFR-directed logarithmic "
                "deadlines"
            ),
            "proof_source_manifest": {
                str(path.relative_to(repository)): _sha256(path)
                for path in source_paths
            },
            "parent_result_manifest": {
                str(
                    arguments.balanced_control_chain.resolve().relative_to(
                        repository
                    )
                ): parent_digest
            },
        },
        "source_evidence": {
            "balanced_control_chain_result_sha256": parent_digest,
            "balanced_control_chain_generator": parent["provenance"]["generator"],
            "balanced_control_chain_generator_sha256": parent["provenance"][
                "generator_sha256"
            ],
            "same_model_equations": (
                "the balanced two-half-delay-layer FHN baseline of the parent "
                "result; no dynamics are replaced at handoff"
            ),
            "handoff_protocol": (
                "bounded recovery cancellation through the declared handoff "
                "face; u^v=u^w=0 afterwards"
            ),
            "method_of_steps_bridge": (
                "controlled deadline plus autonomous barrier deadline is "
                "strictly below tau_0=4*sqrt(5), so both delayed layers retain "
                "the prepared +/-1/2 value"
            ),
            "positive_barrier": {
                "segments": len(positive.segments),
                "step": str(positive.step),
                "terminal_recovery_upper_exact": str(
                    positive.terminal_barrier_upper
                ),
                "minimum_velocity_lower_exact": str(
                    positive.minimum_vector_lower
                ),
                "minimum_inward_margin_exact": str(
                    positive.minimum_inward_margin
                ),
            },
            "negative_barrier": {
                "segments": len(negative.segments),
                "step": str(negative.step),
                "terminal_recovery_magnitude_upper_exact": str(
                    negative.terminal_barrier_upper
                ),
                "minimum_magnitude_velocity_lower_exact": str(
                    negative.minimum_vector_lower
                ),
                "minimum_inward_margin_exact": str(
                    negative.minimum_inward_margin
                ),
            },
            "negative_unit_handoff_obstruction": {
                "segments": len(obstruction.segments),
                "endpoint": str(obstruction.endpoint),
                "initial_magnitude_velocity_lower_exact": str(
                    obstruction.initial_vector_lower
                ),
                "terminal_crossing_margin_exact": str(
                    obstruction.terminal_crossing_margin
                ),
                "minimum_inward_margin_exact": str(
                    obstruction.minimum_inward_margin
                ),
            },
        },
        "certificate": asdict(certificate),
        "scope": {
            "same_delayed_fhn_baseline_model": True,
            "bounded_control_through_handoff": True,
            "all_additive_inputs_zero_after_handoff": True,
            "positive_finite_autonomous_excursion": True,
            "negative_finite_autonomous_excursion_after_deeper_handoff": True,
            "finite_horizon_no_reversal_corridors": True,
            "piecewise_barrier_corner_forward_invariance": True,
            "two_synchronous_terminal_faces": True,
            "negative_unit_handoff_turn_obstruction": True,
            "asynchronous_autonomous_excursion": False,
            "autonomous_onset": False,
            "permanent_no_return": False,
            "biological_action_potential": False,
            "quiet_or_pulse_basin": False,
            "landing_on_periodic_branch": False,
            "full_network_periodic_attraction": False,
            "general_topology_canard_root_equivalence": False,
            "model_uncertainty": False,
            "measurement_noise": False,
            "hardware": False,
        },
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    arguments.output.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
