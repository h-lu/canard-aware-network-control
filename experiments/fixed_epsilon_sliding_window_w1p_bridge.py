#!/usr/bin/env python3
"""Generate the sliding-window and W1p Fredholm-bridge audit."""

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

import canard_control.fixed_epsilon_sliding_window_w1p_bridge as proof_source  # noqa: E402
from canard_control.fixed_epsilon_sliding_window_w1p_bridge import (  # noqa: E402
    CANONICAL_LONG_DELAY_DOC_SHA256,
    DEFAULT_COMMAND,
    GENERATOR_RELATIVE_PATH,
    GREEN_PHASE_TRACES_DOC_SHA256,
    GROWING_TUBE_GRAPH_DOC_SHA256,
    PROOF_SOURCE_RELATIVE_PATH,
    RESULT_RELATIVE_PATH,
    QUADRATIC_PERIOD_LOCKED_ROOT_DOC_SHA256,
    SELECTED_REPELLING_ENDPOINT_RESULT_SHA256,
    TWO_SIDED_CANDIDATE_RESULT_SHA256,
    json_ready_sliding_window_w1p_bridge_payload,
)


def _sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def _verify_parents() -> tuple[dict[str, Any], dict[str, str], dict[str, bool]]:
    candidate_path = (
        REPOSITORY / "experiments/results/fixed_epsilon_two_sided_candidate.json"
    )
    endpoint_path = (
        REPOSITORY
        / "experiments/results/fixed_epsilon_selected_repelling_endpoint.json"
    )
    growing_tube_path = REPOSITORY / "docs/growing-tube-graph-proof.md"
    green_phase_path = REPOSITORY / "docs/green-phase-selected-traces.md"
    canonical_path = REPOSITORY / "docs/canonical-long-delay-theorem.md"
    quadratic_root_path = (
        REPOSITORY / "docs/quadratic-period-locked-selected-root.md"
    )
    expected = {
        "two_sided_candidate_result": TWO_SIDED_CANDIDATE_RESULT_SHA256,
        "selected_repelling_endpoint_result": (
            SELECTED_REPELLING_ENDPOINT_RESULT_SHA256
        ),
        "growing_tube_graph_doc": GROWING_TUBE_GRAPH_DOC_SHA256,
        "green_phase_traces_doc": GREEN_PHASE_TRACES_DOC_SHA256,
        "canonical_long_delay_doc": CANONICAL_LONG_DELAY_DOC_SHA256,
        "quadratic_period_locked_root_doc": (
            QUADRATIC_PERIOD_LOCKED_ROOT_DOC_SHA256
        ),
    }
    actual = {
        "two_sided_candidate_result": _sha256(candidate_path),
        "selected_repelling_endpoint_result": _sha256(endpoint_path),
        "growing_tube_graph_doc": _sha256(growing_tube_path),
        "green_phase_traces_doc": _sha256(green_phase_path),
        "canonical_long_delay_doc": _sha256(canonical_path),
        "quadratic_period_locked_root_doc": _sha256(quadratic_root_path),
    }
    if actual != expected:
        changed = [key for key in expected if actual[key] != expected[key]]
        raise ValueError(f"pinned parent hashes changed: {changed}")

    candidate = _read_json(candidate_path)
    endpoint = _read_json(endpoint_path)
    growing_tube_text = growing_tube_path.read_text(encoding="utf-8")
    green_phase_text = green_phase_path.read_text(encoding="utf-8")
    canonical_text = canonical_path.read_text(encoding="utf-8")
    quadratic_root_text = quadratic_root_path.read_text(encoding="utf-8")
    candidate_scope = candidate.get("audit", {}).get("scope", {})
    endpoint_certificate = endpoint.get("audit", {}).get("certificate", {})
    checks = {
        "candidate_is_diagnostic_not_selected_root": (
            candidate_scope.get("actual_two_branch_numerical_candidate") is True
            and candidate_scope.get("backward_extendible_repelling_bundle")
            is False
            and candidate_scope.get("selected_root") is False
        ),
        "parent_chart_is_contract_not_constructed": (
            endpoint_certificate.get(
                "invariant_chart_implies_local_backward_extension_validated"
            )
            is True
            and endpoint_certificate.get(
                "backward_extendible_selected_repelling_chart_constructed"
            )
            is False
            and endpoint_certificate.get("fixed_epsilon_selected_root_validated")
            is False
        ),
        "graph_transform_has_zero_amplitude_fixed_point": (
            "(q_{0,S},0)" in growing_tube_text
            and "F_S" in growing_tube_text
            and "G_S" in growing_tube_text
        ),
        "green_phase_trace_scope_is_canonical_not_arbitrary_outer": (
            "planar trace theorem are proved below" in green_phase_text
            and "arbitrary outer selections are not covered" in green_phase_text
        ),
        "canonical_history_selection_scope_is_preparation_indexed": (
            "canonical local history selection" in canonical_text
            and "does not identify an unspecified" in canonical_text
            and "no preparation-independent exact finite-\\(\\delta\\) root is asserted"
            in canonical_text
        ),
        "small_delta_gap_has_gaussian_asymptotic_not_fixed_window_identity": (
            "\\frac{D}{\\delta}" in quadratic_root_text
            and "\\sqrt{2\\pi}(\\nu+1/8)+O(\\delta)"
            in quadratic_root_text
        ),
    }
    if not all(checks.values()):
        failed = [key for key, value in checks.items() if not value]
        raise ValueError(f"pinned parent claim checks failed: {failed}")
    return candidate, actual, checks


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
    candidate, parent_hashes, parent_checks = _verify_parents()
    audit = json_ready_sliding_window_w1p_bridge_payload(candidate)
    source_path = Path(proof_source.__file__).resolve()
    generator_path = Path(__file__).resolve()
    payload = {
        "audit": audit,
        "manifest": {
            "generator": GENERATOR_RELATIVE_PATH,
            "generator_sha256": _sha256(generator_path),
            "proof_source": PROOF_SOURCE_RELATIVE_PATH,
            "proof_source_sha256": _sha256(source_path),
            "parent_sha256": parent_hashes,
            "parent_claim_checks": parent_checks,
            "default_command": DEFAULT_COMMAND,
            "python": platform.python_version(),
            "platform": platform.platform(),
            "arithmetic": (
                "exact SymPy inverse-phase, time-scale, Sobolev-bump, "
                "dimension, and Fredholm-index identities; one recomputed "
                "binary64 node diagnostic from the pinned candidate; no "
                "selected-orbit or interval solve"
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
