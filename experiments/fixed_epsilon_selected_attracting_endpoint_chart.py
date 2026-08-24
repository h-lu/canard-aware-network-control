#!/usr/bin/env python3
"""Generate the fixed-epsilon selected-attracting-endpoint audit."""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path

from canard_control.fixed_epsilon_selected_attracting_endpoint_chart import (
    ARITHMETIC_DESCRIPTION,
    DEFAULT_COMMAND,
    GENERATOR_RELATIVE_PATH,
    PROOF_SOURCE_RELATIVE_PATH,
    current_parent_sha256,
    expected_parent_sha256,
    reference_selected_endpoint_audit_payload,
)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "experiments/results/"
            "fixed_epsilon_selected_attracting_endpoint_chart.json"
        ),
    )
    return parser.parse_args()


def _sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _read_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def _verify_parent_claims(repository: Path) -> dict[str, bool]:
    candidate = _read_json(
        repository
        / "experiments/results/fixed_epsilon_two_sided_candidate.json"
    )["audit"]
    blueprint = _read_json(
        repository
        / "experiments/results/fixed_epsilon_quadratic_root_bvp.json"
    )["audit"]
    dimensions = candidate["faithful_next_discretization"]
    candidate_scope = candidate["scope"]
    contract = blueprint["bvp_contract"]
    blueprint_scope = blueprint["scope"]
    checks = {
        "candidate_uses_repaired_schema": candidate.get("schema_version") == 2,
        "candidate_declares_raw_history_194": (
            dimensions.get("raw_history_coefficient_dimension") == 194
        ),
        "candidate_declares_discrete_compatibility_192": (
            dimensions.get("discrete_endpoint_compatibility_rank") == 2
            and dimensions.get("discrete_endpoint_compatible_level_dimension")
            == 192
        ),
        "candidate_declares_global_c1_dimensions": (
            dimensions.get("global_c1_internal_derivative_continuity_rows")
            == 30
            and dimensions.get("global_c1_history_dimension") == 164
            and dimensions.get(
                "global_c1_endpoint_compatible_level_dimension"
            )
            == 162
        ),
        "candidate_declares_ambient_193_effective_191": (
            dimensions.get("ambient_attracting_coordinate_dimension") == 193
            and dimensions.get("attracting_compatibility_residual_rows") == 2
            and dimensions.get(
                "effective_compatible_attracting_zero_fiber_dimension"
            )
            == 191
        ),
        "candidate_declares_phase_fixed_775_by_774": (
            dimensions.get("phase_fixed_residual_dimension") == 775
            and dimensions.get("phase_fixed_unknown_dimension") == 774
        ),
        "candidate_entry_template_is_compatible_but_unselected": (
            candidate_scope.get(
                "entry_solution_manifold_compatibility_at_template_current"
            )
            is True
            and candidate_scope.get("selected_attracting_bundle") is False
        ),
        "candidate_refuses_selected_root": (
            candidate_scope.get("selected_root") is False
        ),
        "candidate_repaired_ledger_is_arithmetic_only": (
            dimensions.get("ambient_repaired_ledger_arithmetic_only") is True
            and dimensions.get("selected_endpoint_operator_constructed")
            is False
            and dimensions.get(
                "global_c1_or_w2_multicell_realization_validated"
            )
            is False
        ),
        "blueprint_requires_solution_manifold": (
            contract.get("state_space")
            == "C([-h,0],R^2) on the RFDE solution manifold"
        ),
        "blueprint_requires_parameter_coherent_endpoint_bundles": any(
            "parameter-coherent entry and exit trace bundles" in item
            for item in contract.get("required_validation_gates", [])
        ),
        "blueprint_refuses_fixed_epsilon_selected_root": (
            blueprint_scope.get("fixed_epsilon_selected_root") is False
        ),
    }
    failed = [key for key, value in checks.items() if not value]
    if failed:
        raise ValueError(f"pinned parent claim checks failed: {failed}")
    return checks


def main() -> None:
    arguments = parse_arguments()
    repository = Path(__file__).resolve().parents[1]
    actual_parents = current_parent_sha256()
    if actual_parents != expected_parent_sha256():
        changed = [
            key
            for key, expected in expected_parent_sha256().items()
            if actual_parents.get(key) != expected
        ]
        raise ValueError(f"pinned endpoint-audit parents changed: {changed}")
    parent_claim_checks = _verify_parent_claims(repository)
    proof_source = repository / PROOF_SOURCE_RELATIVE_PATH
    generator = repository / GENERATOR_RELATIVE_PATH
    record = {
        "audit": reference_selected_endpoint_audit_payload(),
        "manifest": {
            "arithmetic": ARITHMETIC_DESCRIPTION,
            "command": DEFAULT_COMMAND,
            "proof_source": PROOF_SOURCE_RELATIVE_PATH,
            "proof_source_sha256": _sha256(proof_source),
            "generator": GENERATOR_RELATIVE_PATH,
            "generator_sha256": _sha256(generator),
            "parent_sha256": actual_parents,
            "parent_claim_checks": parent_claim_checks,
        },
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(
        json.dumps(record, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
