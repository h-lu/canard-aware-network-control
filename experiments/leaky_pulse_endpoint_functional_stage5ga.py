#!/usr/bin/env python3
"""Generate, validate, and atomically install the Stage-5G-a certificate."""

from __future__ import annotations

import json
import os
from pathlib import Path
import tempfile

from canard_control.leaky_pulse_endpoint_functional_stage5ga import (
    RESULT_RELATIVE_PATH,
    build_stage5ga_result,
    validate_stage5ga_result,
)


def main() -> None:
    repository = Path(__file__).resolve().parents[1]
    payload = build_stage5ga_result(repository)
    # Validation, including every parent validator, precedes creation of the
    # temporary output.  The release procedure separately performs a cold
    # ``recompute=True`` replay in a fresh interpreter.
    validate_stage5ga_result(payload, repository)
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
