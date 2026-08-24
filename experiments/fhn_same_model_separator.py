#!/usr/bin/env python3
"""Generate the directed same-model clamped-separator certificate."""

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
import canard_control.fhn_periodic_candidate as periodic_model_source
import canard_control.fhn_same_model_separator as separator_source
from canard_control.fhn_periodic_candidate import FHNPeriodicParameters
from canard_control.fhn_same_model_separator import (
    CONTROLLED_PHASE_SPACE,
    DECISION_PROTOCOL,
    load_same_model_separator,
)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--parameter-box-result",
        type=Path,
        default=Path("experiments/results/fhn_periodic_parameter_box.json"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("experiments/results/fhn_same_model_separator.json"),
    )
    parser.add_argument("--precision", type=int, default=160)
    return parser.parse_args()


def _sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def main() -> None:
    arguments = parse_arguments()
    repository = Path(__file__).resolve().parents[1]
    certificate = load_same_model_separator(
        arguments.parameter_box_result,
        precision=arguments.precision,
    )
    baseline = FHNPeriodicParameters()
    expected_baseline = (0.2, 0.6, 4.0, 5.0, 0.2, 0.25)
    actual_baseline = (
        baseline.epsilon,
        baseline.unfolding,
        baseline.theta_0,
        baseline.theta_1,
        baseline.kappa_1,
        baseline.kappa_3,
    )
    if actual_baseline != expected_baseline:
        raise ValueError("periodic model defaults no longer match the certificate")
    source_paths = {
        "src/canard_control/directed_interval.py": Path(
            directed_interval_source.__file__
        ).resolve(),
        "src/canard_control/fhn_same_model_separator.py": Path(
            separator_source.__file__
        ).resolve(),
        "src/canard_control/fhn_periodic_candidate.py": Path(
            periodic_model_source.__file__
        ).resolve(),
    }
    payload = {
        "provenance": {
            "generator": "experiments/fhn_same_model_separator.py",
            "generator_sha256": _sha256(Path(__file__).resolve()),
            "argv": [sys.executable, *sys.argv],
            "default_command": (
                "PYTHONPATH=build/testdeps:src /usr/bin/python3 "
                "experiments/fhn_same_model_separator.py"
            ),
            "python": platform.python_version(),
            "platform": platform.platform(),
            "gmpy2": gmpy2.version(),
            "mpfr": gmpy2.mpfr_version(),
            "arithmetic": (
                "exact symbolic identities and MPFR directed endpoints"
            ),
            "proof_source_manifest": {
                str(path.relative_to(repository)): _sha256(path)
                for path in source_paths.values()
            },
        },
        "source_evidence": {
            "parameter_box_result_sha256": certificate.source_result_sha256,
            "source_synchronous_model": (
                certificate.source_synchronous_model_id
            ),
            "periodic_synchronous_parameters": {
                "epsilon": "1/5",
                "unfolding": "3/5",
                "theta_0": "4",
                "theta_1": "5",
                "gain_center": ["1/5", "1/4"],
            },
            "source_periodic_artifact_certifies_full_network_scaffolds": False,
            "full_network_instance_fixed_by_separator_certificate": {
                "instance_id": certificate.certified_full_network_instance_id,
                "network_class": "rank-one two-module dual-scaffold",
                "voltage_scaffold": "3",
                "recovery_scaffold": "2",
                "collective_projection": "pi*x=(bar(x)_1+bar(x)_2)/2",
                "recovery_actuator": "u_i^w=-epsilon*(pi*v-unfolding)",
            },
            "decision_protocol": DECISION_PROTOCOL,
            "controlled_complete_history_phase_space": (
                CONTROLLED_PHASE_SPACE
            ),
            "reset_only_controller_absent_from_baseline_periodic_rfde": True,
        },
        "certificate": asdict(certificate),
        "scope": {
            "same_synchronous_baseline_and_gain_box": (
                certificate.same_synchronous_baseline_and_gain_box_validated
            ),
            "full_network_d3_e2_instance_fixed_by_separator_certificate": (
                certificate.full_network_d3_e2_instance_fixed_by_this_certificate
            ),
            "source_periodic_artifact_certifies_full_network_scaffolds": (
                certificate.source_periodic_artifact_certifies_full_network_scaffolds
            ),
            "full_network_collective_clamp_exact": (
                certificate.full_network_collective_projection_exact
                and certificate.physical_collective_recovery_actuator_exact
                and certificate.actuator_has_zero_transverse_projection_exact
                and certificate.controlled_collective_recovery_leaf_invariant_exact
            ),
            "controlled_operational_first_hit_onset": (
                certificate.controlled_operational_onset_validated
            ),
            "reset_family_complete_history_threshold": (
                certificate.reset_family_complete_history_threshold_validated
            ),
            "controlled_clamped_complete_history_stable_manifold": (
                certificate.controlled_clamped_complete_history_stable_manifold_validated
            ),
            "quantified_noisy_history_capture": (
                certificate.quantified_noisy_history_capture_validated
            ),
            "nonlinear_transverse_synchronization_during_clamped_decision": (
                certificate.nonlinear_transverse_synchronization_during_clamped_decision_validated
            ),
            "periodic_full_network_transverse_stability": (
                certificate.periodic_full_network_transverse_stability_validated
            ),
            "unforced_complete_history_stable_manifold": (
                certificate.unforced_complete_history_stable_manifold_validated
            ),
            "arbitrary_two_module_sizes_linear_variational_transverse_decay_during_clamped_decision": (
                certificate.arbitrary_two_module_sizes_linear_variational_transverse_decay_during_clamped_decision_validated
            ),
            "unforced_onset": certificate.unforced_onset_validated,
            "maximal_canard_onset": certificate.maximal_canard_onset_validated,
            "periodic_orbit_attraction": (
                certificate.periodic_orbit_attraction_validated
            ),
            "general_network_topology": (
                certificate.general_network_topology_validated
            ),
            "biological_pulse_or_quiet_basin_capture_beyond_channel_faces": False,
            "issue_15_closed": False,
        },
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    arguments.output.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
