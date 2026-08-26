#!/usr/bin/env python3
"""Generate recoverable shards and aggregate the target second-step proof."""

from __future__ import annotations

import argparse
from dataclasses import asdict
from hashlib import sha256
import json
from pathlib import Path
import platform

import gmpy2

from canard_control.fixed_epsilon_target_second_step_cover import (
    C4_SEAM_SOURCE_RELATIVE_PATH,
    DEFAULT_COMMAND,
    FIRST_STEP_RESULT_RELATIVE_PATH,
    FIRST_STEP_RESULT_SHA256,
    FIRST_STEP_SOURCE_RELATIVE_PATH,
    GENERATOR_RELATIVE_PATH,
    INTERVAL_BACKEND_SOURCE_RELATIVE_PATH,
    MANIFEST_ARITHMETIC,
    NOTE_RELATIVE_PATH,
    PHYSICAL_MODEL_SOURCE_RELATIVE_PATH,
    PRIMARY_PRECISION_BITS,
    PROOF_SOURCE_RELATIVE_PATH,
    REFINEMENT_PRECISION_BITS,
    RESULT_RELATIVE_PATH,
    build_second_step_shard_payload,
    build_target_second_method_step_cover_certificate_from_shards,
    shard_relative_path,
    validate_second_step_shard_payload,
    validate_target_second_method_step_cover_result,
)


REPOSITORY = Path(__file__).resolve().parents[1]


def _sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def run_shard(precision: int, label_index: int) -> Path:
    payload = build_second_step_shard_payload(precision, label_index)
    validate_second_step_shard_payload(
        payload,
        precision=precision,
        label_index=label_index,
        require_pinned_digest=False,
    )
    path = REPOSITORY / shard_relative_path(precision, label_index)
    _write_json(path, payload)
    return path


def run_missing(precision: int) -> None:
    for label_index in range(20):
        path = REPOSITORY / shard_relative_path(precision, label_index)
        if path.exists():
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
                validate_second_step_shard_payload(
                    payload,
                    precision=precision,
                    label_index=label_index,
                    require_pinned_digest=False,
                )
                print(f"reuse {path.relative_to(REPOSITORY)}", flush=True)
                continue
            except (ValueError, KeyError, json.JSONDecodeError):
                pass
        print(f"run precision={precision} label={label_index}", flush=True)
        run_shard(precision, label_index)


def build_aggregate_payload() -> dict[str, object]:
    certificate = build_target_second_method_step_cover_certificate_from_shards(
        REPOSITORY
    )
    paths = {
        "proof_source": PROOF_SOURCE_RELATIVE_PATH,
        "generator": GENERATOR_RELATIVE_PATH,
        "note": NOTE_RELATIVE_PATH,
        "first_step_source": FIRST_STEP_SOURCE_RELATIVE_PATH,
        "first_step_result": FIRST_STEP_RESULT_RELATIVE_PATH,
        "interval_backend_source": INTERVAL_BACKEND_SOURCE_RELATIVE_PATH,
        "c4_seam_source": C4_SEAM_SOURCE_RELATIVE_PATH,
        "physical_model_source": PHYSICAL_MODEL_SOURCE_RELATIVE_PATH,
    }
    manifest: dict[str, object] = {
        "default_command": DEFAULT_COMMAND,
        "arithmetic": MANIFEST_ARITHMETIC,
        "python": platform.python_version(),
        "platform": platform.platform(),
        "gmpy2": gmpy2.version(),
        "mpfr": gmpy2.mpfr_version(),
        "first_step_result_sha256": FIRST_STEP_RESULT_SHA256,
    }
    for name, relative in paths.items():
        manifest[name] = relative
        manifest[f"{name}_sha256"] = _sha256(REPOSITORY / relative)
    manifest["shards"] = [
        {
            "path": relative,
            "sha256": _sha256(REPOSITORY / relative),
        }
        for precision in (PRIMARY_PRECISION_BITS, REFINEMENT_PRECISION_BITS)
        for label_index in range(20)
        for relative in (shard_relative_path(precision, label_index),)
    ]
    return {"audit": {"certificate": asdict(certificate)}, "manifest": manifest}


def aggregate() -> Path:
    payload = build_aggregate_payload()
    validate_target_second_method_step_cover_result(payload, REPOSITORY)
    path = REPOSITORY / RESULT_RELATIVE_PATH
    _write_json(path, payload)
    return path


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--precision", type=int, choices=(192, 256))
    parser.add_argument("--label-index", type=int)
    parser.add_argument("--run-missing", action="store_true")
    parser.add_argument("--aggregate", action="store_true")
    return parser


def main() -> None:
    arguments = _parser().parse_args()
    if arguments.label_index is not None:
        if arguments.precision is None:
            raise SystemExit("--label-index requires --precision")
        if arguments.run_missing or arguments.aggregate:
            raise SystemExit("a one-shard run cannot be combined with other modes")
        print(run_shard(arguments.precision, arguments.label_index))
        return
    if arguments.run_missing:
        if arguments.precision is None:
            raise SystemExit("--run-missing requires --precision")
        run_missing(arguments.precision)
        if arguments.aggregate:
            print(aggregate())
        return
    if arguments.aggregate:
        if arguments.precision is not None:
            raise SystemExit("--aggregate consumes both fixed precisions")
        print(aggregate())
        return
    if arguments.precision is not None:
        raise SystemExit("--precision requires --label-index or --run-missing")
    run_missing(PRIMARY_PRECISION_BITS)
    run_missing(REFINEMENT_PRECISION_BITS)
    print(aggregate())


if __name__ == "__main__":
    main()
