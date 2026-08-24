#!/usr/bin/env python3
"""Generate the periodic full-network transverse Halanay certificate."""

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
import canard_control.fhn_periodic_transverse_halanay as halanay_source
import canard_control.full_network_blocks as full_network_source
import canard_control.reference_fhn as reference_source
from canard_control.fhn_periodic_transverse_halanay import (
    load_periodic_transverse_halanay,
)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--parameter-box-result",
        type=Path,
        default=Path("experiments/results/fhn_periodic_parameter_box.json"),
    )
    parser.add_argument(
        "--bloch-result",
        type=Path,
        default=Path("experiments/results/fhn_bloch_outer_validation.json"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "experiments/results/fhn_periodic_transverse_halanay.json"
        ),
    )
    parser.add_argument("--precision", type=int, default=160)
    return parser.parse_args()


def _sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def main() -> None:
    arguments = parse_arguments()
    repository = Path(__file__).resolve().parents[1]
    certificate = load_periodic_transverse_halanay(
        arguments.parameter_box_result,
        arguments.bloch_result,
        precision=arguments.precision,
    )
    source_paths = {
        "src/canard_control/directed_interval.py": Path(
            directed_interval_source.__file__
        ).resolve(),
        "src/canard_control/fhn_periodic_transverse_halanay.py": Path(
            halanay_source.__file__
        ).resolve(),
        "src/canard_control/full_network_blocks.py": Path(
            full_network_source.__file__
        ).resolve(),
        "src/canard_control/reference_fhn.py": Path(
            reference_source.__file__
        ).resolve(),
    }
    payload = {
        "provenance": {
            "generator": "experiments/fhn_periodic_transverse_halanay.py",
            "generator_sha256": _sha256(Path(__file__).resolve()),
            "argv": [sys.executable, *sys.argv],
            "default_command": (
                "PYTHONPATH=build/testdeps:src /usr/bin/python3 "
                "experiments/fhn_periodic_transverse_halanay.py"
            ),
            "python": platform.python_version(),
            "platform": platform.platform(),
            "gmpy2": gmpy2.version(),
            "mpfr": gmpy2.mpfr_version(),
            "arithmetic": "exact symbolic identities and MPFR directed endpoints",
            "proof_source_manifest": {
                str(path.relative_to(repository)): _sha256(path)
                for path in source_paths.values()
            },
        },
        "source_evidence": {
            "parameter_box_result_sha256": (
                certificate.parameter_box_result_sha256
            ),
            "bloch_result_sha256": certificate.bloch_result_sha256,
            "historical_bloch_scope_full_network_transverse_stability": False,
            "downstream_certificate_adds_fixed_topology_transverse_theorem": True,
            "voltage_and_recovery_scaffolds_newly_fixed_here": ["3", "2"],
        },
        "certificate": asdict(certificate),
        "scope": {
            "periodic_transverse_variational_decay": True,
            "full_network_orbital_hyperbolicity": True,
            "arbitrary_positive_module_sizes_for_fixed_rank_one_topology": True,
            "synchronous_attraction": False,
            "full_network_attraction": False,
            "nonlinear_synchronization": False,
            "general_network_topology": False,
            "physical_pulse_onset": False,
            "issue_15_closed": False,
        },
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    arguments.output.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
