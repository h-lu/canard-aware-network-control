#!/usr/bin/env python3
"""Generate the rigorous target first-method-step interval cover."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import platform

import gmpy2

from canard_control.fixed_epsilon_target_first_step_cover import (
    C4_SEAM_SOURCE_RELATIVE_PATH,
    DEFAULT_COMMAND,
    GENERATOR_RELATIVE_PATH,
    INTERVAL_BACKEND_SOURCE_RELATIVE_PATH,
    MANIFEST_ARITHMETIC,
    NOTE_RELATIVE_PATH,
    PHYSICAL_MODEL_SOURCE_RELATIVE_PATH,
    PROOF_SOURCE_RELATIVE_PATH,
    RESULT_RELATIVE_PATH,
    SINGLE_CELL_SOURCE_RELATIVE_PATH,
    UNIVALENCE_GATE_SOURCE_RELATIVE_PATH,
    json_ready_target_first_method_step_cover,
    validate_target_first_method_step_cover_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]


def _sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def build_payload() -> dict[str, object]:
    paths = {
        "proof_source": PROOF_SOURCE_RELATIVE_PATH,
        "generator": GENERATOR_RELATIVE_PATH,
        "note": NOTE_RELATIVE_PATH,
        "interval_backend_source": INTERVAL_BACKEND_SOURCE_RELATIVE_PATH,
        "physical_model_source": PHYSICAL_MODEL_SOURCE_RELATIVE_PATH,
        "c4_seam_source": C4_SEAM_SOURCE_RELATIVE_PATH,
        "single_cell_source": SINGLE_CELL_SOURCE_RELATIVE_PATH,
        "univalence_gate_source": UNIVALENCE_GATE_SOURCE_RELATIVE_PATH,
    }
    manifest: dict[str, object] = {
        "default_command": DEFAULT_COMMAND,
        "arithmetic": MANIFEST_ARITHMETIC,
        "python": platform.python_version(),
        "platform": platform.platform(),
        "gmpy2": gmpy2.version(),
        "mpfr": gmpy2.mpfr_version(),
    }
    for name, relative in paths.items():
        manifest[name] = relative
        manifest[f"{name}_sha256"] = _sha256(REPOSITORY / relative)
    return {
        "audit": json_ready_target_first_method_step_cover(),
        "manifest": manifest,
    }


def main() -> None:
    path = REPOSITORY / RESULT_RELATIVE_PATH
    payload = build_payload()
    validate_target_first_method_step_cover_result(payload, REPOSITORY)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
