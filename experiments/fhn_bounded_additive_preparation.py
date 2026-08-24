#!/usr/bin/env python3
"""Generate the directed bounded-additive FHN preparation record."""

from __future__ import annotations

import argparse
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import platform
import sys

import gmpy2

import canard_control.fhn_bounded_additive_preparation as preparation_source
from canard_control.fhn_bounded_additive_preparation import (
    BoundedPreparationSourceEvidence,
    bounded_additive_preparation_from_payload,
)
from canard_control.fhn_same_model_separator import (
    FULL_NETWORK_INSTANCE_ID,
    SYNCHRONOUS_MODEL_ID,
)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--separator-result",
        type=Path,
        default=Path("experiments/results/fhn_same_model_separator.json"),
    )
    parser.add_argument(
        "--causal-hold-note",
        type=Path,
        default=Path("docs/paper-iv-causal-hold-sign-cone.md"),
    )
    parser.add_argument("--voltage-history-bound", default="2")
    parser.add_argument("--recovery-current-bound", default="2")
    parser.add_argument("--reset-abs-bound", default="0.75")
    parser.add_argument("--voltage-gain", default="1")
    parser.add_argument("--recovery-gain", default="1")
    parser.add_argument("--decision-voltage-bound", default="1.5")
    parser.add_argument("--precision", type=int, default=160)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "experiments/results/fhn_bounded_additive_preparation.json"
        ),
    )
    return parser.parse_args()


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    arguments = parse_arguments()
    repository = Path(__file__).resolve().parents[1]
    separator = json.loads(
        arguments.separator_result.read_text(encoding="utf-8")
    )
    evidence = BoundedPreparationSourceEvidence(
        separator_result_sha256=_sha256(arguments.separator_result),
        causal_hold_note_sha256=_sha256(arguments.causal_hold_note),
        source_synchronous_model_id=SYNCHRONOUS_MODEL_ID,
        full_network_instance_id=FULL_NETWORK_INSTANCE_ID,
    )
    certificate = bounded_additive_preparation_from_payload(
        separator,
        evidence,
        voltage_history_sup_bound=arguments.voltage_history_bound,
        recovery_current_sup_bound=arguments.recovery_current_bound,
        reset_abs_bound=arguments.reset_abs_bound,
        voltage_reaching_gain=arguments.voltage_gain,
        recovery_reaching_gain=arguments.recovery_gain,
        decision_voltage_tube_bound=arguments.decision_voltage_bound,
        precision=arguments.precision,
    )
    source_path = Path(preparation_source.__file__).resolve()
    dependency_paths = (
        source_path,
        repository / "src/canard_control/directed_interval.py",
        repository / "src/canard_control/fhn_same_model_separator.py",
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
            "argv": [sys.executable, *sys.argv],
            "default_command": (
                "PYTHONPATH=build/testdeps:src /usr/bin/python3 "
                "experiments/fhn_bounded_additive_preparation.py"
            ),
            "python": platform.python_version(),
            "platform": platform.platform(),
            "gmpy2": gmpy2.version(),
            "mpfr": gmpy2.mpfr_version(),
            "arithmetic": (
                "exact symbolic network cancellation and MPFR-directed "
                "authority/time endpoints"
            ),
        },
        "source_evidence": asdict(evidence),
        "certificate": asdict(certificate),
        "scope": {
            "same_fixed_rank_one_d3_e2_fhn_model": True,
            "bounded_additive_finite_time_preparation_on_declared_bounded_cylinder": (
                certificate.finite_time_exact_state_preparation
            ),
            "exact_complete_history_phi_r_after_scheduled_hold": (
                certificate.maximum_delay_hold_produces_exact_complete_history
            ),
            "causal_current_and_discrete_delay_measurement": (
                certificate.causal_current_and_discrete_delay_measurement
            ),
            "caratheodory_forward_uniqueness": certificate.forward_uniqueness,
            "node_count_independent_input_authority": (
                certificate.input_bound_independent_of_node_count
            ),
            "bounded_initial_data_cylinder_required": (
                certificate.bounded_initial_data_cylinder_required
            ),
            "exact_model_cancellation_required": (
                certificate.exact_model_cancellation_required
            ),
            "full_node_state_and_both_delayed_voltage_layers_required": (
                certificate.full_node_state_measurement_required
                and certificate.both_delayed_voltage_layers_required
            ),
            "optional_nodewise_zero_recovery_continuation_on_declared_voltage_tube": (
                certificate.optional_nodewise_zero_recovery_leaf_invariant
                and certificate.optional_nodewise_voltage_dynamics_preserved
            ),
            "collective_clamp_route_available_separately": (
                certificate.collective_clamp_route_still_available_separately
            ),
            "state_overwrite": False,
            "impulse": False,
            "bandwidth": False,
            "slew_rate": False,
            "energy": False,
            "model_uncertainty": False,
            "measurement_noise": False,
            "hardware_implementation": False,
            "uniform_control_from_unbounded_initial_sets": False,
            "rfde_phase_space_compactness": False,
            "general_network_topology": False,
            "unforced_or_maximal_canard_onset": False,
            "periodic_attraction": False,
            "issue_15_closed": False,
        },
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    arguments.output.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
