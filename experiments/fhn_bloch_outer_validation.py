#!/usr/bin/env python3
"""Run the directed full-complex FHN Bloch-arc validation."""

from __future__ import annotations

import argparse
import ctypes
from dataclasses import asdict
import hashlib
import json
import multiprocessing as mp
import os
from pathlib import Path
import platform
import sys
from typing import Any

import gmpy2
import numpy as np
import scipy

import canard_control.fhn_bloch_outer_validation as bloch_validation_source
from canard_control.directed_interval import decimal_upper, pi_interval
from canard_control.fhn_bloch_outer_validation import (
    BlochParameterBoxEvidence,
    _PreparedBlochValidation,
    _assemble_bloch_arc_certificate,
    _geometric_phase_cells,
    _local_floquet_from_prepared,
    _prepare_bloch_validation,
    validate_directed_bloch_cell,
)
from canard_control.fhn_periodic_candidate import (
    PeriodicOrbitCandidate,
    solve_fhn_periodic_orbit,
)
from canard_control.rfde_floquet_transfer import (
    periodic_orbit_candidate_fingerprint,
)


_FORK_ORBIT: PeriodicOrbitCandidate | None = None
_FORK_EVIDENCE: BlochParameterBoxEvidence | None = None
_FORK_PREPARED: _PreparedBlochValidation | None = None
_FORK_CUTOFF = 64
_FORK_PRECISION = 160


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--nodes", type=int, default=129)
    parser.add_argument("--cutoff", type=int, default=64)
    parser.add_argument("--precision", type=int, default=160)
    parser.add_argument("--relative-half-width", default="0.0125")
    parser.add_argument("--maximum-cells", type=int, default=500)
    parser.add_argument(
        "--workers", type=int, default=min(8, os.cpu_count() or 1)
    )
    parser.add_argument(
        "--parameter-box-result",
        type=Path,
        default=Path("experiments/results/fhn_periodic_parameter_box.json"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("experiments/results/fhn_bloch_outer_validation.json"),
    )
    return parser.parse_args()


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _proof_source_manifest(repository: Path) -> dict[str, str]:
    """Bind the artifact to the complete local proof-source dependency set."""

    relative_paths = (
        "src/canard_control/directed_interval.py",
        "src/canard_control/fhn_bloch_outer_validation.py",
        "src/canard_control/fhn_periodic_candidate.py",
        "src/canard_control/fhn_periodic_directed_validation.py",
        "src/canard_control/fhn_periodic_infinite_validation.py",
        "src/canard_control/fhn_periodic_parameter_box.py",
        "src/canard_control/rfde_floquet_transfer.py",
    )
    return {path: _sha256(repository / path) for path in relative_paths}


def _set_numpy_blas_threads(count: int) -> dict[str, Any]:
    """Set the already loaded scipy-openblas thread count through its C API."""

    if count < 1:
        raise ValueError("BLAS thread count must be positive")
    maps = Path("/proc/self/maps")
    if not maps.exists():
        return {"controlled": False, "reason": "/proc/self/maps unavailable"}
    libraries: list[str] = []
    for line in maps.read_text(encoding="utf-8").splitlines():
        candidate = line.split()[-1] if "/" in line else ""
        if "openblas" in candidate and candidate not in libraries:
            libraries.append(candidate)
    symbol_pairs = (
        (
            "scipy_openblas_get_num_threads64_",
            "scipy_openblas_set_num_threads64_",
        ),
        (
            "scipy_openblas_get_num_threads_64_",
            "scipy_openblas_set_num_threads_64_",
        ),
    )
    for library_path in libraries:
        library = ctypes.CDLL(library_path)
        for getter_name, setter_name in symbol_pairs:
            if not hasattr(library, getter_name) or not hasattr(
                library, setter_name
            ):
                continue
            getter = getattr(library, getter_name)
            getter.restype = ctypes.c_int
            getter.argtypes = []
            setter = getattr(library, setter_name)
            setter.restype = None
            setter.argtypes = [ctypes.c_int]
            before = int(getter())
            setter(int(count))
            after = int(getter())
            if after != count:
                raise RuntimeError("the OpenBLAS thread control did not stick")
            return {
                "controlled": True,
                "library": library_path,
                "getter": getter_name,
                "setter": setter_name,
                "before": before,
                "after": after,
            }
    return {"controlled": False, "reason": "scipy-openblas C API not found"}


def _worker_initializer() -> None:
    _set_numpy_blas_threads(1)


def _validate_indexed_cell(
    item: tuple[int, tuple[str, str, str, str]],
):
    index, declaration = item
    if _FORK_ORBIT is None or _FORK_EVIDENCE is None or _FORK_PREPARED is None:
        raise RuntimeError("the forked Bloch worker has no prepared evidence")
    lower, center, upper, half = declaration
    certificate = validate_directed_bloch_cell(
        _FORK_ORBIT,
        _FORK_EVIDENCE,
        phase_lower=lower,
        phase_center=center,
        phase_upper=upper,
        phase_half_width=half,
        cutoff=_FORK_CUTOFF,
        precision=_FORK_PRECISION,
        _prepared=_FORK_PREPARED,
    )
    return index, certificate


def main() -> None:
    arguments = parse_arguments()
    repository = Path(__file__).resolve().parents[1]
    if arguments.nodes != 129:
        raise ValueError("the tracked parameter-box theorem uses 129 nodes")
    if arguments.workers < 1:
        raise ValueError("workers must be positive")
    parameter_payload = json.loads(
        arguments.parameter_box_result.read_text(encoding="utf-8")
    )
    parameter_validation = parameter_payload["validation"]

    # The exact tracked candidate is generated before changing the loaded
    # BLAS thread count.  Its binary fingerprint is evidence, not a tolerance
    # comparison with a separately solved nearby orbit.
    orbit = solve_fhn_periodic_orbit(node_count=arguments.nodes)
    fingerprint = periodic_orbit_candidate_fingerprint(orbit)
    evidence = BlochParameterBoxEvidence(
        parameter_box_result_sha256=_sha256(arguments.parameter_box_result),
        candidate_fingerprint=fingerprint,
        gain_half_width=parameter_validation["gain_box"]["half_width"],
        correction_radius=parameter_validation["continuation"][
            "chosen_radius"
        ],
        continuation_cutoff=parameter_validation["continuation"]["cutoff"],
        periodic_branch_validated=parameter_validation[
            "d1_validated"
        ],
        bordered_inverse_validated=parameter_validation["continuation"][
            "parameter_box_bordered_inverse_validated"
        ],
        moving_delay_period_column_validated=True,
    )
    blas = _set_numpy_blas_threads(1)
    if blas.get("controlled", False):
        blas["library_sha256"] = _sha256(Path(blas["library"]))
    if arguments.workers > 1 and not blas.get("controlled", False):
        raise RuntimeError(
            "parallel Bloch validation requires auditable single-thread BLAS"
        )
    prepared = _prepare_bloch_validation(
        orbit, evidence, arguments.precision
    )
    local = _local_floquet_from_prepared(prepared)
    required_upper = decimal_upper(pi_interval(arguments.precision).upper)
    declarations = _geometric_phase_cells(
        local.local_phase_radius_lower,
        required_upper,
        arguments.relative_half_width,
        maximum_cells=arguments.maximum_cells,
    )

    global _FORK_ORBIT, _FORK_EVIDENCE, _FORK_PREPARED
    global _FORK_CUTOFF, _FORK_PRECISION
    _FORK_ORBIT = orbit
    _FORK_EVIDENCE = evidence
    _FORK_PREPARED = prepared
    _FORK_CUTOFF = arguments.cutoff
    _FORK_PRECISION = arguments.precision
    indexed = tuple(enumerate(declarations))
    results: list[Any] = [None] * len(indexed)
    if arguments.workers == 1:
        iterator = map(_validate_indexed_cell, indexed)
        pool = None
    else:
        context = mp.get_context("fork")
        pool = context.Pool(
            processes=arguments.workers,
            initializer=_worker_initializer,
        )
        iterator = pool.imap_unordered(
            _validate_indexed_cell, indexed, chunksize=1
        )
    try:
        for completed, (index, certificate) in enumerate(iterator, start=1):
            results[index] = certificate
            if completed == 1 or completed % 10 == 0 or completed == len(indexed):
                print(
                    f"validated Bloch cells: {completed}/{len(indexed)}; "
                    f"latest q={certificate.contraction_upper}",
                    flush=True,
                )
    finally:
        if pool is not None:
            pool.close()
            pool.join()
    if any(item is None for item in results):
        raise RuntimeError("the parallel Bloch scan returned an incomplete list")
    cells = tuple(results)
    arc = _assemble_bloch_arc_certificate(
        local,
        evidence,
        cells,
        declarations,
        cutoff=arguments.cutoff,
        precision=arguments.precision,
        relative_half_width=arguments.relative_half_width,
    )
    payload = {
        "provenance": {
            "generator": "experiments/fhn_bloch_outer_validation.py",
            "generator_sha256": _sha256(Path(__file__).resolve()),
            "proof_source": str(
                Path(bloch_validation_source.__file__).resolve().relative_to(
                    repository
                )
            ),
            "proof_source_sha256": _sha256(
                Path(bloch_validation_source.__file__).resolve()
            ),
            "proof_source_manifest": _proof_source_manifest(repository),
            "argv": [sys.executable, *sys.argv],
            "default_command": (
                "PYTHONPATH=build/testdeps:src /usr/bin/python3 "
                "experiments/fhn_bloch_outer_validation.py"
            ),
            "python": platform.python_version(),
            "platform": platform.platform(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "gmpy2": gmpy2.version(),
            "mpfr": gmpy2.mpfr_version(),
            "rounding": "MPFR RoundDown/RoundUp at every theorem endpoint",
            "binary_accelerators": (
                "stored binary64 full-complex inverses/products, each "
                "covered by directed Higham and interval-remainder bounds"
            ),
            "multiprocessing_start_method": (
                "sequential" if arguments.workers == 1 else "fork"
            ),
            "worker_count": arguments.workers,
            "blas_thread_control": blas,
        },
        "source_evidence": asdict(evidence),
        "local_transfer": asdict(local),
        "outer_arc": asdict(arc),
        "scope": {
            "uniform_history_fourier_regularity_bridge": (
                local.regularity_bridge_to_history_monodromy
            ),
            "uniform_simple_unit_multiplier": (
                local.unit_multiplier_algebraically_simple_validated
            ),
            "uniform_local_punctured_arc_exclusion": (
                local.local_unit_circle_exclusion_validated
            ),
            "uniform_positive_outer_arc_exclusion": (
                arc.connected_positive_arc_cover
                and arc.every_cell_validated
            ),
            "all_nontrivial_unit_multipliers_excluded": (
                arc.all_nontrivial_unit_multipliers_excluded
            ),
            "synchronous_orbital_hyperbolicity": (
                arc.synchronous_orbital_hyperbolicity_validated
            ),
            "attraction": arc.attraction_validated,
            "full_network_transverse_stability": (
                arc.full_network_transverse_stability_validated
            ),
        },
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    arguments.output.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
