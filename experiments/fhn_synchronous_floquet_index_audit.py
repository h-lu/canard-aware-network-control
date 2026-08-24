#!/usr/bin/env python3
"""Audit the missing synchronous Floquet index without promoting stability."""

from __future__ import annotations

import argparse
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import platform
import sys

import numpy as np

import canard_control.fhn_synchronous_floquet_index_audit as audit_source
from canard_control.fhn_synchronous_floquet_index_audit import (
    FloquetIndexSourceEvidence,
    audit_synchronous_floquet_index,
    compute_center_monodromy_diagnostic,
)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--bloch-result",
        type=Path,
        default=Path("experiments/results/fhn_bloch_outer_validation.json"),
    )
    parser.add_argument(
        "--transverse-result",
        type=Path,
        default=Path("experiments/results/fhn_periodic_transverse_halanay.json"),
    )
    parser.add_argument(
        "--candidate-result",
        type=Path,
        default=Path("experiments/results/fhn_periodic_box_candidate.json"),
    )
    parser.add_argument(
        "--parameter-box-result",
        type=Path,
        default=Path("experiments/results/fhn_periodic_parameter_box.json"),
    )
    parser.add_argument(
        "--step-counts",
        default="150,250,400,600",
        help="strictly increasing binary64 diagnostic step counts",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "experiments/results/fhn_synchronous_floquet_index_audit.json"
        ),
    )
    return parser.parse_args()


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def main() -> None:
    arguments = parse_arguments()
    repository = Path(__file__).resolve().parents[1]
    counts = tuple(int(item) for item in arguments.step_counts.split(","))
    bloch = _load(arguments.bloch_result)
    transverse = _load(arguments.transverse_result)
    candidate = _load(arguments.candidate_result)
    evidence = FloquetIndexSourceEvidence(
        parameter_box_result_sha256=_sha256(arguments.parameter_box_result),
        bloch_result_sha256=_sha256(arguments.bloch_result),
        transverse_result_sha256=_sha256(arguments.transverse_result),
        candidate_result_sha256=_sha256(arguments.candidate_result),
        candidate_fingerprint=bloch["source_evidence"]["candidate_fingerprint"],
        model_id=transverse["certificate"]["model_id"],
    )
    diagnostic = compute_center_monodromy_diagnostic(
        candidate, step_counts=counts
    )
    certificate = audit_synchronous_floquet_index(
        bloch,
        transverse,
        candidate,
        evidence,
        diagnostic_rows=diagnostic,
        anchor_index_evidence=None,
    )
    proof_source = Path(audit_source.__file__).resolve()
    payload = {
        "provenance": {
            "generator": str(Path(__file__).resolve().relative_to(repository)),
            "generator_sha256": _sha256(Path(__file__).resolve()),
            "proof_source": str(proof_source.relative_to(repository)),
            "proof_source_sha256": _sha256(proof_source),
            "proof_source_manifest": {
                str(proof_source.relative_to(repository)): _sha256(proof_source),
            },
            "argv": [sys.executable, *sys.argv],
            "default_command": (
                "PYTHONPATH=build/testdeps:src /usr/bin/python3 "
                "experiments/fhn_synchronous_floquet_index_audit.py"
            ),
            "python": platform.python_version(),
            "platform": platform.platform(),
            "numpy": np.__version__,
            "arithmetic": (
                "source-ledger logic is exact; monodromy rows are explicitly "
                "non-directed IEEE binary64 diagnostics"
            ),
        },
        "source_evidence": asdict(evidence),
        "certificate": asdict(certificate),
        "scope": {
            "synchronous_orbital_hyperbolicity": (
                certificate.source_synchronous_orbital_hyperbolicity
            ),
            "fixed_topology_transverse_variational_decay": (
                certificate.source_fixed_topology_transverse_variational_decay
            ),
            "box_index_transport_ready_after_anchor_count": (
                certificate.box_index_transport_ready_after_anchor_count
            ),
            "floating_center_multiplier_diagnostic": True,
            "anchor_unstable_multiplier_count": False,
            "synchronous_stable_index": False,
            "synchronous_attraction": False,
            "quantitative_synchronous_decay_rate": False,
            "full_network_orbital_attraction": False,
            "nonlinear_synchronization": False,
            "general_network_topology": False,
            "issue_15_closed": False,
        },
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    arguments.output.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
