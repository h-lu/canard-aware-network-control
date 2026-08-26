#!/usr/bin/env python3
"""Generate and atomically install the Stage-4S-B Hessian bridge audit."""

from __future__ import annotations

import json
import os
from pathlib import Path
import tempfile

from canard_control.leaky_inner_stage4s_hessian_bridge import (
    RESULT_RELATIVE_PATH,
    build_stage4s_hessian_bridge_result,
    validate_stage4s_hessian_bridge_result,
)


def main() -> None:
    repository = Path(__file__).resolve().parents[1]
    payload = build_stage4s_hessian_bridge_result(repository)
    validate_stage4s_hessian_bridge_result(payload, repository, recompute=True)

    destination = repository / RESULT_RELATIVE_PATH
    destination.parent.mkdir(parents=True, exist_ok=True)
    serialized = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{destination.name}.", suffix=".tmp", dir=destination.parent
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(serialized)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, destination)
        directory_descriptor = os.open(destination.parent, os.O_RDONLY)
        try:
            os.fsync(directory_descriptor)
        finally:
            os.close(directory_descriptor)
    finally:
        temporary.unlink(missing_ok=True)

    print(destination)
    print(payload["manifest"]["arithmetic_core_sha256"])
    print(payload["manifest"]["bridge_sha256"])


if __name__ == "__main__":
    main()
