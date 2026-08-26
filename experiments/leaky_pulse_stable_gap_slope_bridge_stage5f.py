#!/usr/bin/env python3
"""Generate and validate the Stage-5F stable-gap slope bridge."""

from __future__ import annotations

import json
import os
from pathlib import Path
import tempfile

from canard_control.leaky_pulse_stable_gap_slope_bridge_stage5f import (
    RESULT_RELATIVE_PATH,
    build_stage5f_result,
    validate_stage5f_result,
)


def main() -> None:
    repository = Path(__file__).resolve().parents[1]
    payload = build_stage5f_result(repository)
    validate_stage5f_result(payload, repository)
    destination = repository / RESULT_RELATIVE_PATH
    destination.parent.mkdir(parents=True, exist_ok=True)
    serialized = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{destination.name}.",
        suffix=".tmp",
        dir=destination.parent,
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(serialized)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, destination)
    finally:
        temporary.unlink(missing_ok=True)
    print(destination)
    print(payload["manifest"]["certificate_sha256"])


if __name__ == "__main__":
    main()
