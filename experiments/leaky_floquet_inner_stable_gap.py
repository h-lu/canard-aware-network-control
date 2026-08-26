#!/usr/bin/env python3
"""Generate the center-inner quantitative Poincare stable spectral gap."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from canard_control.leaky_floquet_inner_stable_gap import (
    EXPECTED_COMPLETE_LEAF_PARTITION_SHA256,
    MAXIMUM_PROCESSED_CELLS,
    RESULT_RELATIVE_PATH,
    build_inner_stable_gap_result,
    validate_inner_stable_gap_result,
)


def _arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path(RESULT_RELATIVE_PATH))
    parser.add_argument(
        "--maximum-processed-cells",
        type=int,
        default=MAXIMUM_PROCESSED_CELLS,
    )
    parser.add_argument("--workers", type=int, default=12)
    parser.add_argument("--skip-parent-replay", action="store_true")
    parser.add_argument("--calibrate-unregistered-complete", action="store_true")
    return parser.parse_args()


def main() -> None:
    arguments = _arguments()
    repository = Path(__file__).resolve().parents[1]

    def progress(processed: int, accepted: int, pending: int) -> None:
        if processed % 500 == 0:
            print(
                f"stable-gap progress: processed={processed} "
                f"accepted={accepted} pending={pending}",
                file=sys.stderr,
                flush=True,
            )

    payload = build_inner_stable_gap_result(
        repository,
        maximum_processed_cells=arguments.maximum_processed_cells,
        parallel_workers=arguments.workers,
        replay_parents=not arguments.skip_parent_replay,
        progress=progress,
    )
    certificate = payload["certificate"]
    if arguments.calibrate_unregistered_complete:
        if certificate["pending_cell_count"] != 0:
            raise RuntimeError("the stable-gap calibration did not complete")
        if EXPECTED_COMPLETE_LEAF_PARTITION_SHA256 is not None:
            raise RuntimeError("the stable-gap leaf digest is already registered")
        print(
            json.dumps(
                {
                    "accepted_leaf_count": certificate["accepted_leaf_count"],
                    "leaf_partition_sha256": certificate[
                        "leaf_partition_sha256"
                    ],
                    "maximum_contraction_upper": certificate[
                        "maximum_contraction_upper"
                    ],
                    "neutral_disk_leaf_count": certificate[
                        "neutral_disk_leaf_count"
                    ],
                    "neumann_leaf_count": certificate["neumann_leaf_count"],
                    "processed_cell_count": certificate[
                        "processed_cell_count"
                    ],
                    "stable_multiplier_modulus_upper": certificate[
                        "stable_multiplier_modulus_upper"
                    ],
                },
                indent=2,
                sort_keys=True,
            )
        )
        return
    validate_inner_stable_gap_result(
        payload, repository, validate_parents=False
    )
    output = (
        arguments.output
        if arguments.output.is_absolute()
        else repository / arguments.output
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "gamma_lower": certificate["gamma_lower"],
                "stable_multiplier_spectral_radius_upper": certificate[
                    "stable_multiplier_spectral_radius_upper"
                ],
                "accepted_leaf_count": certificate["accepted_leaf_count"],
                "processed_cell_count": certificate["processed_cell_count"],
                "maximum_contraction_upper": certificate[
                    "maximum_contraction_upper"
                ],
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
