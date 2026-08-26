#!/usr/bin/env python3
"""Generate the complete center-inner Floquet right-half count."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from canard_control.leaky_floquet_inner_right_half_cover import (
    EXPECTED_COMPLETE_LEAF_PARTITION_SHA256,
    MAXIMUM_PROCESSED_CELLS,
    RESULT_RELATIVE_PATH,
    build_inner_right_half_result,
    validate_inner_right_half_result,
)


def _arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path(RESULT_RELATIVE_PATH))
    parser.add_argument(
        "--maximum-processed-cells",
        type=int,
        default=MAXIMUM_PROCESSED_CELLS,
    )
    parser.add_argument(
        "--skip-parent-replay",
        action="store_true",
        help="Use only already hash-bound parent ledgers during calibration.",
    )
    parser.add_argument("--workers", type=int, default=12)
    parser.add_argument(
        "--calibrate-unregistered-complete",
        action="store_true",
        help=(
            "Print a completed tree digest before it is registered; no "
            "artifact is written in this mode."
        ),
    )
    return parser.parse_args()


def main() -> None:
    arguments = _arguments()
    repository = Path(__file__).resolve().parents[1]

    def progress(processed: int, accepted: int, pending: int) -> None:
        if processed % 1000 == 0:
            print(
                f"inner cover progress: processed={processed} "
                f"accepted={accepted} pending={pending}",
                file=sys.stderr,
                flush=True,
            )

    payload = build_inner_right_half_result(
        repository,
        maximum_processed_cells=arguments.maximum_processed_cells,
        parallel_workers=arguments.workers,
        replay_parents=not arguments.skip_parent_replay,
        progress=progress,
    )
    certificate = payload["certificate"]
    if arguments.calibrate_unregistered_complete:
        if certificate["pending_cell_count"] != 0:
            raise RuntimeError("the calibration tree did not complete")
        if EXPECTED_COMPLETE_LEAF_PARTITION_SHA256 is not None:
            raise RuntimeError("the complete leaf digest is already registered")
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
                    "positive_disk_leaf_count": certificate[
                        "positive_disk_leaf_count"
                    ],
                    "processed_cell_count": certificate[
                        "processed_cell_count"
                    ],
                },
                indent=2,
                sort_keys=True,
            )
        )
        return
    validate_inner_right_half_result(
        payload,
        repository,
        validate_parents=False,
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
                "accepted_leaf_count": certificate["accepted_leaf_count"],
                "neutral_disk_characteristic_value_count": certificate[
                    "neutral_disk_characteristic_value_count"
                ],
                "positive_disk_characteristic_value_count": certificate[
                    "positive_disk_characteristic_value_count"
                ],
                "compact_keyhole_characteristic_value_count": certificate[
                    "compact_keyhole_characteristic_value_count"
                ],
                "directed_unstable_multiplier_count": certificate[
                    "directed_unstable_multiplier_count"
                ],
                "maximum_contraction_upper": certificate[
                    "maximum_contraction_upper"
                ],
                "pending_cell_count": certificate["pending_cell_count"],
                "processed_cell_count": certificate["processed_cell_count"],
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
