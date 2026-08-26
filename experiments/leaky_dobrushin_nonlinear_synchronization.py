#!/usr/bin/env python3
"""Generate the nonlinear Dobrushin synchronization certificate."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import platform

from canard_control.leaky_dobrushin_nonlinear_synchronization import (
    ARITHMETIC_SCOPE,
    DEFAULT_COMMAND,
    GENERATOR_RELATIVE_PATH,
    NOTE_RELATIVE_PATH,
    RESULT_RELATIVE_PATH,
    SCHEMA_ID,
    SOURCE_RELATIVE_PATH,
    build_nonlinear_synchronization_certificate,
    canonical_sha256,
    validate_nonlinear_synchronization_result,
)
from canard_control.leaky_dobrushin_transverse_halanay import (
    RESULT_RELATIVE_PATH as HALANAY_RESULT_RELATIVE_PATH,
)


REPOSITORY = Path(__file__).resolve().parents[1]


def _sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def main() -> None:
    certificate = build_nonlinear_synchronization_certificate(REPOSITORY)
    body = certificate.__dict__
    sources = {
        "source": SOURCE_RELATIVE_PATH,
        "generator": GENERATOR_RELATIVE_PATH,
        "note": NOTE_RELATIVE_PATH,
        "parent_result": HALANAY_RESULT_RELATIVE_PATH,
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
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    validate_nonlinear_synchronization_result(payload, REPOSITORY)
    print(output)


if __name__ == "__main__":
    main()
