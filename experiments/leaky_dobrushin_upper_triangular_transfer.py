#!/usr/bin/env python3
"""Generate the non-left-balanced upper-triangular transfer certificate."""

from __future__ import annotations

import json
import os
from pathlib import Path
from tempfile import NamedTemporaryFile

from canard_control.leaky_dobrushin_upper_triangular_transfer import (
    RESULT_RELATIVE_PATH,
    build_upper_triangular_transfer_result,
    validate_upper_triangular_transfer_result,
)


def _atomic_write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary: Path | None = None
    try:
        with NamedTemporaryFile(
            "w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            temporary = Path(handle.name)
            handle.write(json.dumps(payload, indent=2, sort_keys=True) + "\n")
            handle.flush()
            os.fsync(handle.fileno())
        temporary.replace(path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def main() -> None:
    repository = Path(__file__).resolve().parents[1]
    payload = build_upper_triangular_transfer_result(repository)
    validate_upper_triangular_transfer_result(payload, repository)
    destination = repository / RESULT_RELATIVE_PATH
    _atomic_write_json(destination, payload)
    print(destination)
    print(payload["manifest"]["certificate_sha256"])


if __name__ == "__main__":
    main()
