#!/usr/bin/env python3
"""Generate the exact leaky physical-pulse terminal-history certificate."""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import platform

import sympy as sp

from canard_control.leaky_pulse_terminal_history import (
    AUDIT_ID,
    DEFAULT_COMMAND,
    GENERATOR_RELATIVE_PATH,
    MANIFEST_ARITHMETIC,
    MODEL_ID,
    NOTE_RELATIVE_PATH,
    PARENT_PROBE_RELATIVE_PATH,
    PARENT_SOURCE_RELATIVE_PATH,
    PROOF_SOURCE_RELATIVE_PATH,
    RESULT_RELATIVE_PATH,
    json_ready_pulse_terminal_history_audit,
    validate_pulse_terminal_history_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]
DEFAULT_RESULT = REPOSITORY / RESULT_RELATIVE_PATH


def _sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def build_result() -> dict[str, object]:
    sources = {
        "proof_source": PROOF_SOURCE_RELATIVE_PATH,
        "parent_source": PARENT_SOURCE_RELATIVE_PATH,
        "parent_probe": PARENT_PROBE_RELATIVE_PATH,
        "generator": GENERATOR_RELATIVE_PATH,
        "note": NOTE_RELATIVE_PATH,
    }
    manifest: dict[str, object] = {
        "model_id": MODEL_ID,
        "audit_id": AUDIT_ID,
        "default_command": DEFAULT_COMMAND,
        "arithmetic": MANIFEST_ARITHMETIC,
        "python": platform.python_version(),
        "platform": platform.platform(),
        "sympy": sp.__version__,
    }
    for name, relative in sources.items():
        manifest[name] = relative
        manifest[f"{name}_sha256"] = _sha256(REPOSITORY / relative)
    return {
        "audit": json_ready_pulse_terminal_history_audit(),
        "manifest": manifest,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_RESULT)
    arguments = parser.parse_args()
    payload = build_result()
    validate_pulse_terminal_history_result(payload, REPOSITORY)
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    validate_pulse_terminal_history_result(
        json.loads(arguments.output.read_text(encoding="utf-8")), REPOSITORY
    )
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
