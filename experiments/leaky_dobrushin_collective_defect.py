#!/usr/bin/env python3
"""Generate the quadratic collective-defect certificate."""

from __future__ import annotations

from hashlib import sha256
import json
import os
from pathlib import Path
import platform
from tempfile import NamedTemporaryFile

from canard_control.leaky_dobrushin_collective_defect import (
    ARITHMETIC_SCOPE,
    DEFAULT_COMMAND,
    GENERATOR_RELATIVE_PATH,
    NOTE_RELATIVE_PATH,
    RESULT_RELATIVE_PATH,
    SCHEMA_ID,
    SOURCE_RELATIVE_PATH,
    TEST_RELATIVE_PATH,
    build_collective_defect_certificate,
    canonical_sha256,
    validate_collective_defect_result,
)
from canard_control.leaky_dobrushin_nonlinear_synchronization import (
    RESULT_RELATIVE_PATH as SYNCHRONIZATION_RESULT_RELATIVE_PATH,
)


REPOSITORY = Path(__file__).resolve().parents[1]


def _sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


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
    certificate = build_collective_defect_certificate(REPOSITORY)
    body = certificate.__dict__
    sources = {
        "source": SOURCE_RELATIVE_PATH,
        "generator": GENERATOR_RELATIVE_PATH,
        "note": NOTE_RELATIVE_PATH,
        "test": TEST_RELATIVE_PATH,
        "parent_result": SYNCHRONIZATION_RESULT_RELATIVE_PATH,
    }
    manifest: dict[str, object] = {
        "schema_id": SCHEMA_ID,
        "certificate_sha256": canonical_sha256(body),
        "default_command": DEFAULT_COMMAND,
        "arithmetic_scope": ARITHMETIC_SCOPE,
        "python": platform.python_version(),
        "platform": platform.platform(),
    }
    for name, relative in sources.items():
        manifest[name] = relative
        manifest[f"{name}_sha256"] = _sha256(REPOSITORY / relative)
    payload = {"certificate": body, "manifest": manifest}
    output = REPOSITORY / RESULT_RELATIVE_PATH
    validate_collective_defect_result(payload, REPOSITORY)
    _atomic_write_json(output, payload)
    print(output)


if __name__ == "__main__":
    main()
