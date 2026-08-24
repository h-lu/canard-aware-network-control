#!/usr/bin/env python3
"""Build the synchronous Floquet Riesz-reduction certificate."""

from __future__ import annotations

import argparse
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import platform

import gmpy2
import numpy as np
import scipy

import canard_control.fhn_synchronous_floquet_riesz_reduction as source_module
from canard_control.fhn_synchronous_floquet_riesz_reduction import (
    RieszReductionSourceEvidence,
    build_synchronous_floquet_riesz_reduction,
)


def _arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--bloch-result",
        type=Path,
        default=Path("experiments/results/fhn_bloch_outer_validation.json"),
    )
    parser.add_argument(
        "--index-audit-result",
        type=Path,
        default=Path(
            "experiments/results/fhn_synchronous_floquet_index_audit.json"
        ),
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
        "--output",
        type=Path,
        default=Path(
            "experiments/results/fhn_synchronous_floquet_riesz_reduction.json"
        ),
    )
    parser.add_argument("--precision", type=int, default=160)
    parser.add_argument(
        "--edge-subdivisions",
        type=int,
        nargs="+",
        default=(24, 48),
    )
    return parser.parse_args()


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _manifest(repository: Path) -> dict[str, str]:
    paths = (
        "src/canard_control/directed_interval.py",
        "src/canard_control/fhn_periodic_candidate.py",
        "src/canard_control/fhn_synchronous_floquet_riesz_reduction.py",
        "src/canard_control/rfde_floquet_transfer.py",
    )
    return {path: _sha256(repository / path) for path in paths}


def main() -> None:
    arguments = _arguments()
    repository = Path(__file__).resolve().parents[1]
    bloch_payload = json.loads(arguments.bloch_result.read_text(encoding="utf-8"))
    index_payload = json.loads(
        arguments.index_audit_result.read_text(encoding="utf-8")
    )
    candidate_payload = json.loads(
        arguments.candidate_result.read_text(encoding="utf-8")
    )
    evidence = RieszReductionSourceEvidence(
        parameter_box_result_sha256=_sha256(arguments.parameter_box_result),
        bloch_result_sha256=_sha256(arguments.bloch_result),
        index_audit_result_sha256=_sha256(arguments.index_audit_result),
        candidate_result_sha256=_sha256(arguments.candidate_result),
        candidate_fingerprint=bloch_payload["source_evidence"][
            "candidate_fingerprint"
        ],
        model_id=index_payload["certificate"]["model_id"],
    )
    certificate = build_synchronous_floquet_riesz_reduction(
        bloch_payload,
        index_payload,
        candidate_payload,
        evidence,
        precision=arguments.precision,
        edge_subdivision_counts=tuple(arguments.edge_subdivisions),
    )
    payload = {
        "certificate": asdict(certificate),
        "scope": {
            "uniform_right_half_strip_tail_block_invertibility": True,
            "analytic_258_dimensional_schur_reduction": True,
            "outer_half_plane_exclusion_from_real_part_128": True,
            "local_complex_right_half_keyhole_exclusion": True,
            "general_multiplier_analytic_to_monodromy_multiplicity_bridge": False,
            "directed_finite_schur_winding": False,
            "synchronous_stable_index": False,
            "synchronous_attraction": False,
            "full_network_orbital_attraction": False,
        },
        "source_evidence": asdict(evidence),
        "provenance": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "gmpy2": gmpy2.version(),
            "proof_source_manifest": _manifest(repository),
            "source_module_sha256": _sha256(Path(source_module.__file__)),
        },
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
