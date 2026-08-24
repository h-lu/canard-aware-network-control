#!/usr/bin/env python3
"""Generate the fixed-epsilon frozen synchronous graph-operator contract."""

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

import canard_control.fixed_epsilon_frozen_graph_operator as contract  # noqa: E402
from canard_control.fixed_epsilon_frozen_graph_operator import (  # noqa: E402
    DEFAULT_COMMAND,
    GENERATOR_RELATIVE_PATH,
    MANIFEST_ARITHMETIC,
    NOTE_RELATIVE_PATH,
    PARENT_SHA256,
    PROOF_SOURCE_RELATIVE_PATH,
    RESULT_RELATIVE_PATH,
    json_ready_frozen_graph_operator_audit,
    validate_frozen_graph_operator_result,
)


def _sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def _verify_parents() -> tuple[dict[str, str], dict[str, bool]]:
    paths = {
        "growing_tube_graph_doc": REPOSITORY
        / "docs/growing-tube-graph-proof.md",
        "special_flow_graph_doc": REPOSITORY
        / "docs/special-flow-graph-theorem.md",
        "green_phase_selected_traces_doc": REPOSITORY
        / "docs/green-phase-selected-traces.md",
        "quadratic_period_locked_root_doc": REPOSITORY
        / "docs/quadratic-period-locked-selected-root.md",
        "fixed_epsilon_sliding_window_w1p_bridge_result": REPOSITORY
        / "experiments/results/fixed_epsilon_sliding_window_w1p_bridge.json",
        "fixed_window_prepared_gap_seed_result": REPOSITORY
        / "experiments/results/fixed_window_prepared_gap_seed.json",
    }
    actual = {name: _sha256(path) for name, path in paths.items()}
    if actual != PARENT_SHA256:
        changed = [name for name in PARENT_SHA256 if actual[name] != PARENT_SHA256[name]]
        raise ValueError(f"pinned parent hashes changed: {changed}")

    growing = paths["growing_tube_graph_doc"].read_text(encoding="utf-8")
    special = paths["special_flow_graph_doc"].read_text(encoding="utf-8")
    green = paths["green_phase_selected_traces_doc"].read_text(encoding="utf-8")
    quadratic = paths["quadratic_period_locked_root_doc"].read_text(
        encoding="utf-8"
    )
    bridge = _read_json(
        paths["fixed_epsilon_sliding_window_w1p_bridge_result"]
    )["audit"]["certificate"]
    seed = _read_json(paths["fixed_window_prepared_gap_seed_result"])[
        "audit"
    ]["certificate"]

    checks = {
        "growing_parent_freezes_target_cutoff_and_requires_flow_hull": (
            "cutoff is frozen at the target value" in growing
            and "continuous flow hull" in growing
            and "N_{\\rm bl}" in growing
            and "D=2N_{\\rm bl}+4" in growing
        ),
        "special_flow_parent_uses_backward_complete_flow_embedding": (
            "\\Phi_Q^{-\\theta_j}u" in special
            and "complete two-sided flow" in special
            and "injective embedding" in special
        ),
        "green_parent_separates_graph_and_planar_cutoffs": (
            "two different frozen cutoffs" in green
            and "must not be conflated" in green
        ),
        "quadratic_parent_has_exact_0_4_5_theta_slot_model": (
            "X_4" in quadratic
            and "X_5" in quadratic
            and "X_\\Theta" in quadratic
            and "no Taylor remainder" in quadratic
        ),
        "bridge_parent_leaves_target_graph_trace_and_root_open": (
            bridge.get("frozen_target_graph_family_validated") is False
            and bridge.get("prepared_planar_trace_family_validated") is False
            and bridge.get("fixed_window_gap_row_validated") is False
            and bridge.get("fixed_epsilon_selected_root_validated") is False
        ),
        "seed_parent_proves_only_singular_not_positive_hull": (
            seed.get("singular_depth_two_hull_covered") is True
            and seed.get("positive_amplitude_depth_two_hull_validated")
            is False
            and seed.get("complete_graph_preparation_datum_constructed")
            is False
            and seed.get("frozen_target_graph_family_validated") is False
        ),
    }
    if any(value is not True for value in checks.values()):
        failed = [name for name, value in checks.items() if value is not True]
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
    source_path = Path(contract.__file__).resolve()
    generator_path = Path(__file__).resolve()
    note_path = REPOSITORY / NOTE_RELATIVE_PATH
    payload = {
        "audit": json_ready_frozen_graph_operator_audit(),
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
            "arithmetic": MANIFEST_ARITHMETIC,
        },
    }
    validate_frozen_graph_operator_result(payload, REPOSITORY)
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
