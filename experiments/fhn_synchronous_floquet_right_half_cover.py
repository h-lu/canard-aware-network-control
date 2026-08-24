#!/usr/bin/env python3
"""Build the directed synchronous Floquet right-half zero-free cover."""

from __future__ import annotations

import argparse
from dataclasses import asdict
import hashlib
import json
import os
from pathlib import Path
import platform
import sys

import gmpy2
import numpy as np
import scipy

import canard_control.fhn_synchronous_floquet_right_half_cover as source_module
from canard_control.fhn_synchronous_floquet_right_half_cover import (
    RightHalfCoverEvidence,
    build_right_half_zero_free_cover,
)


def _arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--bloch-result",
        type=Path,
        default=Path("experiments/results/fhn_bloch_outer_validation.json"),
    )
    parser.add_argument(
        "--riesz-result",
        type=Path,
        default=Path(
            "experiments/results/fhn_synchronous_floquet_riesz_reduction.json"
        ),
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
        "--output",
        type=Path,
        default=Path(
            "experiments/results/fhn_synchronous_floquet_right_half_cover.json"
        ),
    )
    parser.add_argument("--precision", type=int, default=160)
    parser.add_argument("--acceptance-threshold", default="0.995")
    parser.add_argument("--maximum-processed-cells", type=int, default=100000)
    parser.add_argument("--maximum-depth", type=int, default=80)
    return parser.parse_args()


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _manifest(repository: Path) -> dict[str, str]:
    paths = (
        "src/canard_control/directed_interval.py",
        "src/canard_control/fhn_bloch_outer_validation.py",
        "src/canard_control/fhn_periodic_candidate.py",
        "src/canard_control/fhn_periodic_directed_validation.py",
        "src/canard_control/fhn_periodic_infinite_validation.py",
        "src/canard_control/fhn_periodic_parameter_box.py",
        "src/canard_control/fhn_synchronous_floquet_right_half_cover.py",
        "src/canard_control/fhn_synchronous_floquet_riesz_reduction.py",
        "src/canard_control/rfde_floquet_transfer.py",
    )
    return {path: _sha256(repository / path) for path in paths}


def main() -> None:
    arguments = _arguments()
    repository = Path(__file__).resolve().parents[1]

    def load(path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))

    bloch_payload = load(arguments.bloch_result)
    riesz_payload = load(arguments.riesz_result)
    transverse_payload = load(arguments.transverse_result)
    candidate_payload = load(arguments.candidate_result)
    evidence = RightHalfCoverEvidence(
        parameter_box_result_sha256=_sha256(arguments.parameter_box_result),
        bloch_result_sha256=_sha256(arguments.bloch_result),
        riesz_result_sha256=_sha256(arguments.riesz_result),
        transverse_result_sha256=_sha256(arguments.transverse_result),
        candidate_result_sha256=_sha256(arguments.candidate_result),
        candidate_fingerprint=str(
            bloch_payload["source_evidence"]["candidate_fingerprint"]
        ),
        model_id=str(transverse_payload["certificate"]["model_id"]),
    )

    def progress(processed: int, accepted: int, pending: int) -> None:
        if processed % 1000 == 0:
            print(
                f"cover progress: processed={processed} "
                f"accepted={accepted} pending={pending}",
                file=sys.stderr,
                flush=True,
            )

    certificate = build_right_half_zero_free_cover(
        bloch_payload,
        riesz_payload,
        transverse_payload,
        candidate_payload,
        evidence,
        precision=arguments.precision,
        acceptance_threshold=arguments.acceptance_threshold,
        maximum_processed_cells=arguments.maximum_processed_cells,
        maximum_depth=arguments.maximum_depth,
        progress=progress,
    )
    payload = {
        "certificate": asdict(certificate),
        "scope": {
            "uniform_exact_parameter_box_right_half_zero_free_cover": (
                certificate.entire_keyhole_region_zero_free_validated
            ),
            "schur_boundary_winding_zero_deduced_from_zero_free_cover": (
                certificate.schur_boundary_winding_deduced_exactly_lower == 0
                and certificate.schur_boundary_winding_deduced_exactly_upper == 0
            ),
            "synchronous_nontranslation_unstable_index_zero": (
                certificate.synchronous_nontranslation_unstable_index_zero_validated
            ),
            "synchronous_linear_orbital_attraction": (
                certificate.synchronous_linear_orbital_attraction_validated
            ),
            "synchronous_nonlinear_orbital_attraction": (
                certificate.synchronous_nonlinear_orbital_attraction_validated
            ),
            "fixed_rank_one_full_network_linear_orbital_attraction": (
                certificate.fixed_rank_one_full_network_linear_orbital_attraction_validated
            ),
            "fixed_rank_one_full_network_nonlinear_orbital_attraction": (
                certificate.fixed_rank_one_full_network_nonlinear_orbital_attraction_validated
            ),
            "general_network_topology": False,
            "biological_pulse_capture": False,
        },
        "source_evidence": asdict(evidence),
        "provenance": {
            "arithmetic": (
                "MPFR directed exact-box bounds plus audited IEEE binary64 "
                "four-real-GEMM accelerators"
            ),
            "default_command": (
                "OPENBLAS_NUM_THREADS=8 PYTHONPATH=build/testdeps:src "
                "/usr/bin/python3 "
                "experiments/fhn_synchronous_floquet_right_half_cover.py"
            ),
            "generator": "experiments/fhn_synchronous_floquet_right_half_cover.py",
            "generator_sha256": _sha256(Path(__file__)),
            "proof_source_manifest": _manifest(repository),
            "source_module_sha256": _sha256(Path(source_module.__file__)),
            "python": platform.python_version(),
            "numpy": np.__version__,
            "numpy_blas": np.__config__.CONFIG.get("Build Dependencies", {}).get(
                "blas", {}
            ),
            "openblas_num_threads": os.environ.get("OPENBLAS_NUM_THREADS"),
            "scipy": scipy.__version__,
            "gmpy2": gmpy2.version(),
            "mpfr": gmpy2.mpfr_version(),
        },
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "accepted_leaf_count": certificate.accepted_leaf_count,
                "processed_cell_count": certificate.processed_cell_count,
                "pending_cell_count": certificate.pending_cell_count,
                "maximum_contraction_upper": certificate.maximum_contraction_upper,
                "zero_free": certificate.entire_keyhole_region_zero_free_validated,
                "failure_reason": certificate.failure_reason,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
