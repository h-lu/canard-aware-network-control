#!/usr/bin/env python3
"""Generate the nonlinear full-network sign-cone certificate."""

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
import canard_control.fhn_full_network_nonlinear_sign_cone as cone_source
import canard_control.fhn_same_model_separator as separator_source
import canard_control.full_network_blocks as network_source
from canard_control.fhn_full_network_nonlinear_sign_cone import (
    load_full_network_nonlinear_sign_cone,
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
        default=Path(
            "experiments/results/fhn_full_network_nonlinear_sign_cone.json"
        ),
    )
    parser.add_argument("--precision", type=int, default=160)
    parser.add_argument("--voltage-sign-margin", default="0.04")
    parser.add_argument("--excursion-voltage-sign-margin", default="0.06")
    parser.add_argument("--recovery-history-bound", default="0.1")
    return parser.parse_args()


def _sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def main() -> None:
    arguments = parse_arguments()
    repository = Path(__file__).resolve().parents[1]
    certificate = load_full_network_nonlinear_sign_cone(
        arguments.separator_result,
        precision=arguments.precision,
        voltage_sign_margin=arguments.voltage_sign_margin,
        excursion_voltage_sign_margin=(
            arguments.excursion_voltage_sign_margin
        ),
        recovery_history_bound=arguments.recovery_history_bound,
    )
    source_paths = {
        "src/canard_control/directed_interval.py": Path(
            directed_interval_source.__file__
        ).resolve(),
        "src/canard_control/fhn_full_network_nonlinear_sign_cone.py": Path(
            cone_source.__file__
        ).resolve(),
        "src/canard_control/fhn_same_model_separator.py": Path(
            separator_source.__file__
        ).resolve(),
        "src/canard_control/full_network_blocks.py": Path(
            network_source.__file__
        ).resolve(),
    }
    separator_payload = json.loads(
        arguments.separator_result.read_text(encoding="utf-8")
    )
    payload = {
        "provenance": {
            "generator": "experiments/fhn_full_network_nonlinear_sign_cone.py",
            "generator_sha256": _sha256(Path(__file__).resolve()),
            "argv": [sys.executable, *sys.argv],
            "default_command": (
                "PYTHONPATH=build/testdeps:src /usr/bin/python3 "
                "experiments/fhn_full_network_nonlinear_sign_cone.py"
            ),
            "python": platform.python_version(),
            "platform": platform.platform(),
            "gmpy2": gmpy2.version(),
            "mpfr": gmpy2.mpfr_version(),
            "arithmetic": (
                "exact SymPy rank-one identities and MPFR directed endpoints"
            ),
            "proof_source_manifest": {
                str(path.relative_to(repository)): _sha256(path)
                for path in source_paths.values()
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
            "fixed_full_network_instance": certificate.model_id,
            "collective_recovery_clamp": (
                "u_i^w=-epsilon*(pi^T*v-unfolding)"
            ),
            "history_cone_condition": certificate.theorem_condition,
            "excursion_history_cone_condition": (
                certificate.excursion_theorem_condition
            ),
            "detector_interpretation": (
                "first nodewise hit of +1 or -1; this event is externally "
                "latched, and the excursion theorem is a separate finite "
                "continuation statement"
            ),
            "excursion_interpretation": (
                "some node reaches +1.5 or -1.2 while the ideal recovery "
                "clamp remains active; it need not be the first detector node"
            ),
        },
        "certificate": asdict(certificate),
        "scope": {
            "positive_full_network_nonlinear_sign_cone_first_hit": True,
            "negative_full_network_nonlinear_sign_cone_first_hit": True,
            "nodewise_detector_first_hit": True,
            "arbitrary_positive_module_sizes_for_fixed_rank_one_family": True,
            "positive_finite_controlled_suprathreshold_excursion": True,
            "negative_finite_controlled_excursion": True,
            "latched_nodewise_detector_then_excursion": True,
            "nonlinear_synchronization": False,
            "attraction": False,
            "noise_across_voltage_sign_boundary": False,
            "bounded_additive_hold_or_hardware": False,
            "beyond_face_biological_basin": False,
            "unforced_or_maximal_canard_onset": False,
            "general_network_topology": False,
            "same_detector_node_reaches_excursion_face": False,
            "detector_face_no_return": False,
            "issue_15_closed": False,
        },
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    arguments.output.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
