#!/usr/bin/env python3
"""Build and write the source-bound Stage-5E certificate."""

from __future__ import annotations

import json
from pathlib import Path

from canard_control.leaky_pulse_oriented_adjoint_action_stage5e import (
    RESULT_RELATIVE_PATH,
    build_stage5e_result,
    validate_stage5e_result,
)


def main() -> None:
    repository = Path(__file__).resolve().parents[1]
    payload = build_stage5e_result(repository)
    validate_stage5e_result(payload, repository)
    destination = repository / RESULT_RELATIVE_PATH
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(destination)
    print(payload["manifest"]["certificate_sha256"])


if __name__ == "__main__":
    main()

