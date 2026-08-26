#!/usr/bin/env python3
"""Generate the source-bound outer leaky Floquet right-half cover."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from canard_control.leaky_floquet_outer_right_half_cover import (
    MAXIMUM_PROCESSED_CELLS,
    RESULT_RELATIVE_PATH,
    RIESZ_RESULT_RELATIVE_PATH,
    build_outer_right_half_cover,
    build_outer_right_half_result,
    validate_outer_right_half_result,
)


def _arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output", type=Path, default=Path(RESULT_RELATIVE_PATH)
    )
    parser.add_argument(
        "--maximum-processed-cells",
        type=int,
        default=MAXIMUM_PROCESSED_CELLS,
    )
    parser.add_argument(
        "--checkpoint",
        type=Path,
        help="atomically write a source-bound resumable execution frontier",
    )
    parser.add_argument(
        "--resume-checkpoint",
        type=Path,
        help="resume from a previously validated source-bound frontier",
    )
    parser.add_argument("--checkpoint-interval", type=int, default=1000)
    parser.add_argument(
        "--calibration-only",
        action="store_true",
        help="print a nonclaim summary without writing or validating a result",
    )
    return parser.parse_args()


def main() -> None:
    arguments = _arguments()
    repository = Path(__file__).resolve().parents[1]
    checkpoint_path = None
    if arguments.checkpoint is not None:
        checkpoint_path = (
            arguments.checkpoint
            if arguments.checkpoint.is_absolute()
            else repository / arguments.checkpoint
        )
    resume = None
    if arguments.resume_checkpoint is not None:
        resume_path = (
            arguments.resume_checkpoint
            if arguments.resume_checkpoint.is_absolute()
            else repository / arguments.resume_checkpoint
        )
        resume = json.loads(resume_path.read_text(encoding="utf-8"))

    def progress(processed: int, accepted: int, pending: int) -> None:
        if processed % 1000 == 0:
            print(
                f"cover progress: processed={processed} "
                f"accepted={accepted} pending={pending}",
                file=sys.stderr,
                flush=True,
            )

    def checkpoint(payload: dict) -> None:
        if checkpoint_path is None:
            return
        checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
        temporary = checkpoint_path.with_suffix(checkpoint_path.suffix + ".tmp")
        temporary.write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        temporary.replace(checkpoint_path)

    common = {
        "maximum_processed_cells": arguments.maximum_processed_cells,
        "progress": progress,
        "resume_checkpoint": resume,
        "checkpoint_interval": arguments.checkpoint_interval,
        "checkpoint_callback": checkpoint if checkpoint_path is not None else None,
    }
    if arguments.calibration_only:
        riesz_payload = json.loads(
            (repository / RIESZ_RESULT_RELATIVE_PATH).read_text(encoding="utf-8")
        )
        certificate = build_outer_right_half_cover(
            repository, riesz_payload, replay_parent=False, **common
        )
        print(
            json.dumps(
                {
                    "accepted_leaf_count": certificate.accepted_leaf_count,
                    "failure_reason": certificate.failure_reason,
                    "leaf_partition_sha256": certificate.leaf_partition_sha256,
                    "local_disk_leaf_count": certificate.local_disk_leaf_count,
                    "maximum_contraction_upper": certificate.maximum_contraction_upper,
                    "maximum_depth": certificate.maximum_depth,
                    "minimum_contraction_margin_lower": (
                        certificate.minimum_contraction_margin_lower
                    ),
                    "neumann_leaf_count": certificate.neumann_leaf_count,
                    "pending_cell_count": certificate.pending_cell_count,
                    "processed_cell_count": certificate.processed_cell_count,
                    "stress_replay_precision_bits": (
                        certificate.stress_replay_precision_bits
                    ),
                    "worst_cell": (
                        None
                        if certificate.worst_cell is None
                        else certificate.worst_cell.__dict__
                    ),
                    "worst_cell_finer_split_stress_maximum_contraction_upper": (
                        certificate.worst_cell_finer_split_stress_maximum_contraction_upper
                    ),
                    "worst_cell_stress_contraction_upper": (
                        certificate.worst_cell_stress_contraction_upper
                    ),
                    "zero_free": (
                        certificate.complete_nontranslation_right_half_strip_zero_free_validated
                    ),
                },
                indent=2,
                sort_keys=True,
            )
        )
        return

    payload = build_outer_right_half_result(repository, **common)
    validate_outer_right_half_result(payload, repository)
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
    certificate = payload["certificate"]
    print(
        json.dumps(
            {
                "accepted_leaf_count": certificate["accepted_leaf_count"],
                "local_disk_leaf_count": certificate["local_disk_leaf_count"],
                "maximum_contraction_upper": certificate[
                    "maximum_contraction_upper"
                ],
                "maximum_depth": certificate["maximum_depth"],
                "neumann_leaf_count": certificate["neumann_leaf_count"],
                "pending_cell_count": certificate["pending_cell_count"],
                "processed_cell_count": certificate["processed_cell_count"],
                "zero_free": certificate[
                    "complete_nontranslation_right_half_strip_zero_free_validated"
                ],
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
