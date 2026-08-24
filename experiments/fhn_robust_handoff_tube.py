#!/usr/bin/env python3
"""Generate the robust finite-horizon FHN shutdown-tube certificate."""

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
import canard_control.fhn_autonomous_handoff_excursion as handoff_source
import canard_control.fhn_robust_handoff_tube as theorem_source
from canard_control.fhn_robust_handoff_tube import (
    TRACKED_AUTONOMOUS_HANDOFF_SHA256,
    TRACKED_BALANCED_CONTROL_CHAIN_SHA256,
    robust_handoff_tube_from_payload,
    robust_tube_algebra_audit,
)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--autonomous-handoff",
        type=Path,
        default=Path(
            "experiments/results/fhn_autonomous_handoff_excursion.json"
        ),
    )
    parser.add_argument(
        "--balanced-control-chain",
        type=Path,
        default=Path("experiments/results/fhn_balanced_control_chain.json"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("experiments/results/fhn_robust_handoff_tube.json"),
    )
    parser.add_argument("--precision", type=int, default=160)
    return parser.parse_args()


def _sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def main() -> None:
    arguments = parse_arguments()
    repository = Path(__file__).resolve().parents[1]
    handoff_raw = arguments.autonomous_handoff.read_bytes()
    handoff_digest = sha256(handoff_raw).hexdigest()
    if handoff_digest != TRACKED_AUTONOMOUS_HANDOFF_SHA256:
        raise ValueError("autonomous handoff result digest changed")
    handoff = json.loads(handoff_raw)
    if not isinstance(handoff, dict):
        raise ValueError("autonomous handoff result must contain an object")

    balanced_digest = _sha256(arguments.balanced_control_chain)
    if balanced_digest != TRACKED_BALANCED_CONTROL_CHAIN_SHA256:
        raise ValueError("balanced control-chain result digest changed")
    certificate = robust_handoff_tube_from_payload(
        handoff,
        autonomous_handoff_result_sha256=handoff_digest,
        precision=arguments.precision,
    )
    audit = robust_tube_algebra_audit()
    source_paths = (
        Path(theorem_source.__file__).resolve(),
        Path(handoff_source.__file__).resolve(),
        Path(directed_interval_source.__file__).resolve(),
    )
    payload = {
        "provenance": {
            "generator": "experiments/fhn_robust_handoff_tube.py",
            "generator_sha256": _sha256(Path(__file__).resolve()),
            "argv": [sys.executable, *sys.argv],
            "default_command": (
                "PYTHONPATH=build/testdeps:src /usr/bin/python3 "
                "experiments/fhn_robust_handoff_tube.py"
            ),
            "python": platform.python_version(),
            "platform": platform.platform(),
            "gmpy2": gmpy2.version(),
            "mpfr": gmpy2.mpfr_version(),
            "arithmetic": (
                "exact rational coefficient domination plus MPFR-directed "
                "Gronwall exponentials"
            ),
            "proof_source_manifest": {
                str(path.relative_to(repository)): _sha256(path)
                for path in source_paths
            },
            "parent_result_manifest": {
                str(
                    arguments.autonomous_handoff.resolve().relative_to(repository)
                ): handoff_digest,
                str(
                    arguments.balanced_control_chain.resolve().relative_to(
                        repository
                    )
                ): balanced_digest,
            },
        },
        "source_evidence": {
            "autonomous_handoff_result_sha256": handoff_digest,
            "balanced_control_chain_result_sha256": balanced_digest,
            "autonomous_handoff_generator": handoff["provenance"]["generator"],
            "autonomous_handoff_generator_sha256": handoff["provenance"][
                "generator_sha256"
            ],
            "phase_space_norm": (
                "max of the nodewise l-infinity voltage and recovery errors; "
                "remote voltage histories use the l-infinity sup norm"
            ),
            "remote_history_windows": (
                "I_{j,sigma}=[-tau_j,H_sigma-tau_j] for both j=0,1"
            ),
            "scaffold_dissipativity": (
                "at an active signed l-infinity component, "
                "sign(e_i)*(P e-e_i)<=0 for every nonnegative row-stochastic P"
            ),
            "input_residual_norm": (
                "arbitrary-sign measurable residuals with componentwise "
                "essential-supremum bounds"
            ),
            "rational_audit": {
                key: str(value) for key, value in asdict(audit).items()
            },
        },
        "certificate": asdict(certificate),
        "scope": {
            "declared_nearby_fhn_parameter_family": True,
            "full_rfde_open_handoff_cylinder": True,
            "asynchronous_finite_horizon_tracking_tube": True,
            "arbitrary_finite_balanced_topology": True,
            "bounded_post_handoff_shutdown_residual": True,
            "positive_and_negative_robust_terminal_capture": True,
            "componentwise_no_reversal_until_capture": True,
            "robust_history_preparation": False,
            "all_additive_inputs_exactly_zero_after_handoff": False,
            "delay_perturbations": False,
            "permanent_no_return": False,
            "biological_action_potential": False,
            "quiet_or_pulse_basin": False,
            "landing_on_periodic_branch": False,
            "actuator_bandwidth_or_slew_rate": False,
            "hardware": False,
        },
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    arguments.output.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
