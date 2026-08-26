#!/usr/bin/env python3
"""Generate or independently check the Stage-3I signed-density certificate."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from tempfile import NamedTemporaryFile

from canard_control.leaky_outer_signed_density_stage3i_tv import (
    RESULT_RELATIVE_PATH,
    build_outer_signed_density_stage3i_tv_result,
    reissue_outer_signed_density_stage3i_tv_result,
    validate_outer_signed_density_stage3i_tv_result,
)


def _atomic_write(result_path: Path, payload: dict) -> None:
    result_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path: Path | None = None
    try:
        with NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=result_path.parent,
            prefix=f".{result_path.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            temporary_path = Path(handle.name)
            handle.write(
                json.dumps(
                    payload,
                    indent=2,
                    sort_keys=True,
                    ensure_ascii=True,
                )
                + "\n"
            )
            handle.flush()
            os.fsync(handle.fileno())
        temporary_path.replace(result_path)
        directory_fd = os.open(result_path.parent, os.O_RDONLY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    finally:
        if temporary_path is not None and temporary_path.exists():
            temporary_path.unlink()


def main() -> None:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--reissue-frozen-cells", action="store_true")
    arguments = parser.parse_args()
    repository = Path(__file__).resolve().parents[1]
    result_path = repository / RESULT_RELATIVE_PATH
    if arguments.check:
        payload = json.loads(result_path.read_text())
        validate_outer_signed_density_stage3i_tv_result(payload, repository)
    elif arguments.reissue_frozen_cells:
        payload = reissue_outer_signed_density_stage3i_tv_result(
            repository, result_path.read_bytes()
        )
        _atomic_write(result_path, payload)
    else:
        payload = build_outer_signed_density_stage3i_tv_result(repository)
        # The validator clears every Stage-3I numerical cache and performs a
        # fresh replay before any candidate artifact can replace the result.
        validate_outer_signed_density_stage3i_tv_result(payload, repository)
        _atomic_write(result_path, payload)
    print(result_path)


if __name__ == "__main__":
    main()
