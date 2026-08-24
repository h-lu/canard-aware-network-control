#!/usr/bin/env python3
"""Generate the fixed-epsilon selected-repelling-endpoint audit."""

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

import canard_control.fixed_epsilon_selected_repelling_endpoint as proof_source  # noqa: E402
from canard_control.fixed_epsilon_selected_repelling_endpoint import (  # noqa: E402
    DEFAULT_COMMAND,
    FIXED_EPSILON_BVP_RESULT_SHA256,
    GENERATOR_RELATIVE_PATH,
    PROOF_SOURCE_RELATIVE_PATH,
    RESULT_RELATIVE_PATH,
    TWO_SIDED_CANDIDATE_RESULT_SHA256,
    compatible_history_fiber_algebra_is_exact,
    invariant_chart_backward_extension_identity_is_exact,
    reference_selected_repelling_endpoint_payload,
    validate_selected_repelling_endpoint_payload,
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
        "fixed_epsilon_bvp_result": (
            REPOSITORY
            / "experiments/results/fixed_epsilon_quadratic_root_bvp.json"
        ),
        "two_sided_candidate_result": (
            REPOSITORY
            / "experiments/results/fixed_epsilon_two_sided_candidate.json"
        ),
    }
    expected = {
        "fixed_epsilon_bvp_result": FIXED_EPSILON_BVP_RESULT_SHA256,
        "two_sided_candidate_result": TWO_SIDED_CANDIDATE_RESULT_SHA256,
    }
    actual = {key: _sha256(path) for key, path in paths.items()}
    if actual != expected:
        changed = [key for key in expected if actual[key] != expected[key]]
        raise ValueError(f"pinned parent hashes changed: {changed}")

    bvp = _read_json(paths["fixed_epsilon_bvp_result"])
    candidate = _read_json(paths["two_sided_candidate_result"])
    bvp_scope = bvp.get("audit", {}).get("scope", {})
    candidate_scope = candidate.get("audit", {}).get("scope", {})
    candidate_next = candidate.get("audit", {}).get(
        "faithful_next_discretization", {}
    )
    checks = {
        "parent_bvp_is_contract_not_solution": (
            bvp_scope.get("exact_validation_contract") is True
            and bvp_scope.get("complete_history_bvp_solution") is False
            and bvp_scope.get("fixed_epsilon_selected_root") is False
        ),
        "candidate_has_scalar_exit_not_selected_bundle": (
            candidate_scope.get("actual_two_branch_numerical_candidate")
            is True
            and candidate_scope.get("backward_extendible_repelling_bundle")
            is False
            and candidate_scope.get("selected_complete_history_bvp") is False
            and candidate_scope.get("selected_root") is False
        ),
        "candidate_repaired_history_ledger_is_194_192_193_1": (
            candidate_next.get("raw_history_coefficient_dimension") == 194
            and candidate_next.get(
                "discrete_endpoint_compatible_level_dimension"
            )
            == 192
            and candidate_next.get("ambient_attracting_coordinate_dimension")
            == 193
            and candidate_next.get("repelling_endpoint_chart_dimension")
            == 1
        ),
        "candidate_strong_history_seam_remains_open": (
            candidate_next.get("global_c1_history_dimension") == 164
            and candidate_next.get(
                "global_c1_endpoint_compatible_level_dimension"
            )
            == 162
            and candidate_next.get(
                "global_c1_or_w2_multicell_realization_validated"
            )
            is False
            and candidate_next.get("ambient_repaired_ledger_arithmetic_only")
            is True
        ),
        "candidate_refuses_backward_ivp_substitute": (
            candidate_next.get("backward_ivp_is_not_an_admissible_substitute")
            is True
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
    if not compatible_history_fiber_algebra_is_exact():
        raise ArithmeticError("compatible-history witness algebra failed")
    if not invariant_chart_backward_extension_identity_is_exact():
        raise ArithmeticError("invariant-chart chain-rule contract failed")

    audit = reference_selected_repelling_endpoint_payload()
    validate_selected_repelling_endpoint_payload(audit)
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
                "exact SymPy Hermite history identities, exact RFDE "
                "solution-manifold compatibility, and a declarative "
                "invariant-chart continuation contract; no interval chart solve"
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
