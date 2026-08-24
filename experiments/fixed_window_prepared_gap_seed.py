#!/usr/bin/env python3
"""Generate the directed explicit finite-window longitudinal-jet seed."""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import platform
import sys
from typing import Any


REPOSITORY = Path(__file__).resolve().parents[1]
SOURCE_ROOT = REPOSITORY / "src"
if str(SOURCE_ROOT) not in sys.path:
    sys.path.insert(0, str(SOURCE_ROOT))

import canard_control.fixed_window_prepared_gap_seed as proof_source  # noqa: E402
from canard_control.fixed_window_prepared_gap_seed import (  # noqa: E402
    BLOCH_RESULT_SHA256,
    DEFAULT_COMMAND,
    GENERATOR_RELATIVE_PATH,
    GREEN_PHASE_DOC_SHA256,
    NOTE_RELATIVE_PATH,
    PERIOD_LOWER,
    PERIOD_UPPER,
    PRECISION_BITS,
    PROOF_SOURCE_RELATIVE_PATH,
    QUADRATIC_PERIOD_LOCKED_ROOT_DOC_SHA256,
    RESULT_RELATIVE_PATH,
    SLIDING_WINDOW_BRIDGE_RESULT_SHA256,
    json_ready_fixed_window_gap_seed_payload,
    validate_fixed_window_gap_seed_payload,
)


def _sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def _verify_parents() -> tuple[dict[str, str], dict[str, bool]]:
    green_path = REPOSITORY / "docs/green-phase-selected-traces.md"
    bloch_path = REPOSITORY / "experiments/results/fhn_bloch_outer_validation.json"
    bridge_path = (
        REPOSITORY
        / "experiments/results/fixed_epsilon_sliding_window_w1p_bridge.json"
    )
    quadratic_root_path = (
        REPOSITORY / "docs/quadratic-period-locked-selected-root.md"
    )
    expected = {
        "green_phase_selected_traces_doc": GREEN_PHASE_DOC_SHA256,
        "fhn_bloch_outer_validation_result": BLOCH_RESULT_SHA256,
        "fixed_epsilon_sliding_window_w1p_bridge_result": (
            SLIDING_WINDOW_BRIDGE_RESULT_SHA256
        ),
        "quadratic_period_locked_root_doc": (
            QUADRATIC_PERIOD_LOCKED_ROOT_DOC_SHA256
        ),
    }
    actual = {
        "green_phase_selected_traces_doc": _sha256(green_path),
        "fhn_bloch_outer_validation_result": _sha256(bloch_path),
        "fixed_epsilon_sliding_window_w1p_bridge_result": _sha256(bridge_path),
        "quadratic_period_locked_root_doc": _sha256(quadratic_root_path),
    }
    if actual != expected:
        changed = [key for key in expected if actual[key] != expected[key]]
        raise ValueError(f"pinned parent hashes changed: {changed}")

    green_text = green_path.read_text(encoding="utf-8")
    bloch = _read_json(bloch_path)
    bridge = _read_json(bridge_path)
    quadratic_root_text = quadratic_root_path.read_text(encoding="utf-8")
    local_transfer = bloch.get("local_transfer", {})
    bridge_certificate = bridge.get("audit", {}).get("certificate", {})
    checks = {
        "green_parent_freezes_preparation_before_differentiation": (
            "After \\(p\\) is chosen, fix one preparation datum" in green_text
            and "no derivative of `S` is taken" in green_text
        ),
        "green_parent_uses_two_distinct_cutoffs": (
            "two different frozen cutoffs" in green_text
            and "must not be conflated" in green_text
        ),
        "period_interval_matches_pinned_parent": (
            local_transfer.get("minimum_period_lower") == PERIOD_LOWER
            and local_transfer.get("maximum_period_upper") == PERIOD_UPPER
        ),
        "parent_full_fixed_window_row_remains_open": (
            bridge_certificate.get("fixed_window_gap_row_validated") is False
            and bridge_certificate.get("frozen_target_graph_family_validated")
            is False
            and bridge_certificate.get("prepared_planar_trace_family_validated")
            is False
        ),
        "quadratic_carrier_first_jet_is_directly_pinned": (
            "\\frac{s^3}{24}+\\frac94\\kappa_1" in quadratic_root_text
            and "(\\kappa_1,\\kappa_3,\\eta)=(1/5,1/4,0)"
            in quadratic_root_text
        ),
    }
    if not all(checks.values()):
        failed = [key for key, value in checks.items() if not value]
        raise ValueError(f"pinned parent claim checks failed: {failed}")
    return actual, checks


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=REPOSITORY / RESULT_RELATIVE_PATH,
    )
    return parser.parse_args()


def main() -> None:
    arguments = parse_arguments()
    parent_hashes, parent_checks = _verify_parents()
    audit = json_ready_fixed_window_gap_seed_payload()
    validate_fixed_window_gap_seed_payload(audit)
    source_path = Path(proof_source.__file__).resolve()
    generator_path = Path(__file__).resolve()
    note_path = REPOSITORY / NOTE_RELATIVE_PATH
    payload = {
        "audit": audit,
        "manifest": {
            "generator": GENERATOR_RELATIVE_PATH,
            "generator_sha256": _sha256(generator_path),
            "proof_source": PROOF_SOURCE_RELATIVE_PATH,
            "proof_source_sha256": _sha256(source_path),
            "note": NOTE_RELATIVE_PATH,
            "note_sha256": _sha256(note_path),
            "parent_sha256": parent_hashes,
            "parent_claim_checks": parent_checks,
            "default_command": DEFAULT_COMMAND,
            "python": platform.python_version(),
            "platform": platform.platform(),
            "arithmetic": (
                "exact rational cutoff algebra and Gaussian moment recurrence; "
                f"{PRECISION_BITS}-bit MPFR-directed exp, erfc, sqrt, pi, "
                "and interval algebra; "
                "no floating quadrature and no nonlinear trace solve"
            ),
        },
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
