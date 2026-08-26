#!/usr/bin/env python3
"""Generate, validate, and atomically install the Stage-5G-b certificate."""

from __future__ import annotations

import json
import os
from pathlib import Path
import tempfile

from canard_control.leaky_pulse_stable_coordinate_cone_stage5gb import (
    RESULT_RELATIVE_PATH,
    build_stage5gb_result,
    validate_stage5gb_result,
)


def main() -> None:
    repository = Path(__file__).resolve().parents[1]
    payload = build_stage5gb_result(repository)
    # Validate every parent and all exact/directed arithmetic before creating
    # a temporary output.  Release verification separately invokes the fresh
    # ``recompute=True`` path in a new interpreter.
    validate_stage5gb_result(payload, repository)
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
    print(payload["manifest"]["numeric_core_sha256"])
    print(payload["manifest"]["certificate_sha256"])


if __name__ == "__main__":
    main()
