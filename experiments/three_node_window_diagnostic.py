#!/usr/bin/env python3
"""Separate fold-parameter and window effects in Paper A's diagnostic.

From the repository root:
    PYTHONPATH=src uv run --extra numeric python \
        experiments/three_node_window_diagnostic.py --workers 3

This computes prescribed-history section zeros, not the invariant-history
matching function. Refinement differences are not rigorous error bounds.
"""

from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor
from dataclasses import asdict
import hashlib
import json
import os
from pathlib import Path
import platform

for variable in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[variable] = "1"

import numpy as np
import scipy

from canard_control.three_node_finite_section import (
    ThreeNodeParameters,
    tune_section_root,
)


REPOSITORY = Path(__file__).resolve().parents[1]
STANDARD = dict(rtol=2e-9, atol=2e-11, max_step=0.08,
                root_xtol=2e-10, root_rtol=2e-10)
REFINED = dict(rtol=5e-10, atol=5e-12, max_step=0.04,
               root_xtol=1e-11, root_rtol=1e-11)


def compute(job: tuple[float, float, bool]) -> dict:
    delta, section, refined = job
    parameters = ThreeNodeParameters(delta=delta)
    roots = [tune_section_root(
        parameters, zeta=zeta, section_half_width=section,
        **(REFINED if refined else STANDARD),
    ) for zeta in (-0.04, 0.04)]
    quotient = (roots[1].nu - roots[0].nu) / (0.08 * delta)
    return dict(delta=delta, section_half_width=section, refined=refined,
                quotient=quotient, roots=[asdict(root) for root in roots],
                predicted_coefficient=parameters.predicted_coefficient,
                absolute_error=abs(quotient-parameters.predicted_coefficient))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workers", type=int, choices=(1, 2, 3), default=1)
    parser.add_argument("--output", type=Path, default=REPOSITORY /
                        "experiments/results/three_node_window_diagnostic.json")
    arguments = parser.parse_args()
    grid = [(delta, section, False) for delta in (0.05, 0.02, 0.01)
            for section in (3.0, 3.5, 4.0)]
    refined_grid = [(0.05, 4.0, True), (0.01, 3.0, True), (0.01, 3.5, True)]
    with ProcessPoolExecutor(max_workers=arguments.workers) as executor:
        rows = list(executor.map(compute, grid + refined_grid))
    standard_rows, refined_rows = rows[:9], rows[9:]
    for row in refined_rows:
        reference = next(item for item in standard_rows if
                         (item["delta"], item["section_half_width"]) ==
                         (row["delta"], row["section_half_width"]))
        row["quotient_change"] = abs(row["quotient"]-reference["quotient"])
    sources = [Path(__file__), REPOSITORY /
               "src/canard_control/three_node_finite_section.py"]
    payload = dict(
        status="prescribed-history floating-point diagnostic; not used in any proof",
        definition=dict(history="gamma_0 with h=0 on [-S-2,-S]",
                        outgoing_condition="Y(S)-X(S)^2+1/2=0",
                        quotient="[nu(delta,+.04;S)-nu(delta,-.04;S)]/(.08*delta)",
                        not_computed=["D_3^fin", "heteroclinic connection"]),
        fixed_parameters=asdict(ThreeNodeParameters(delta=0.05)) |
                         dict(delta="varied on grid", zeta_step=0.04),
        solver=dict(method="method of steps with Radau; Brent roots",
                    standard=STANDARD, refined=REFINED,
                    bracket_half_width=0.4, workers=arguments.workers),
        environment=dict(python=platform.python_version(), numpy=np.__version__,
                         scipy=scipy.__version__),
        source_sha256={str(path.relative_to(REPOSITORY)):
                       hashlib.sha256(path.read_bytes()).hexdigest()
                       for path in sources},
        rows=standard_rows, refinements=refined_rows,
        maximum_refinement_change=max(row["quotient_change"] for row in refined_rows),
    )
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(payload, indent=2, sort_keys=True)+"\n")
    print(f"Saved {arguments.output}; maximum refinement change "
          f"{payload['maximum_refinement_change']:.3g}")


if __name__ == "__main__":
    main()
