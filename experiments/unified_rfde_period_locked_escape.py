#!/usr/bin/env python3
"""Generate the exact period-locked unified-RFDE escape audit."""

from __future__ import annotations

import argparse
from dataclasses import asdict
from hashlib import sha256
import json
from pathlib import Path
import platform
import sys
from typing import Any

import sympy as sp

import canard_control.unified_rfde_period_locked_escape as proof_source
from canard_control.unified_rfde_period_locked_escape import (
    ARITHMETIC_DESCRIPTION,
    AUTONOMOUS_HANDOFF_RESULT_SHA256,
    BALANCED_CONTROL_CHAIN_RESULT_SHA256,
    COMPATIBILITY_RESULT_SHA256,
    DEFAULT_COMMAND,
    DISTINGUISHED_PERIOD_DEFINITION,
    GENERATOR_RELATIVE_PATH,
    HETEROGENEOUS_ROOT_DOC_SHA256,
    PERIODIC_BOX_RESULT_SHA256,
    PROOF_SOURCE_RELATIVE_PATH,
    QUADRATIC_CARRIER_RESULT_SHA256,
    ROOT_ADJOINT_GATE_RESULT_SHA256,
    reference_finite_atom_invisibility_audit,
    reference_heterogeneous_curvature_synchrony_audit,
    reference_linear_canard_parity_audit,
    reference_period_locked_escape_audit,
    reference_unified_escape_certificate,
)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "experiments/results/unified_rfde_period_locked_escape.json"
        ),
    )
    return parser.parse_args()


def _sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _json_value(value: Any) -> Any:
    if isinstance(value, sp.MatrixBase):
        return [[sp.sstr(item) for item in row] for row in value.tolist()]
    if isinstance(value, sp.Basic):
        return sp.sstr(value)
    if isinstance(value, tuple):
        return [_json_value(item) for item in value]
    if isinstance(value, list):
        return [_json_value(item) for item in value]
    if isinstance(value, dict):
        return {key: _json_value(item) for key, item in value.items()}
    return value


def _read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def _verify_parents(repository: Path) -> tuple[dict[str, str], dict[str, bool]]:
    paths = {
        "compatibility_result": repository
        / "experiments/results/fhn_root_periodic_compatibility.json",
        "periodic_box_result": repository
        / "experiments/results/fhn_periodic_parameter_box.json",
        "balanced_control_chain_result": repository
        / "experiments/results/fhn_balanced_control_chain.json",
        "autonomous_handoff_result": repository
        / "experiments/results/fhn_autonomous_handoff_excursion.json",
        "root_adjoint_gate_result": repository
        / "experiments/results/dual_scaffold_root_adjoint_gate.json",
        "quadratic_carrier_result": repository
        / "experiments/results/quadratic_period_locked_root_carrier.json",
        "heterogeneous_root_doc": repository
        / "docs/paper-ii-heterogeneous-curvature-selected-root.md",
    }
    expected = {
        "compatibility_result": COMPATIBILITY_RESULT_SHA256,
        "periodic_box_result": PERIODIC_BOX_RESULT_SHA256,
        "balanced_control_chain_result": BALANCED_CONTROL_CHAIN_RESULT_SHA256,
        "autonomous_handoff_result": AUTONOMOUS_HANDOFF_RESULT_SHA256,
        "root_adjoint_gate_result": ROOT_ADJOINT_GATE_RESULT_SHA256,
        "quadratic_carrier_result": QUADRATIC_CARRIER_RESULT_SHA256,
        "heterogeneous_root_doc": HETEROGENEOUS_ROOT_DOC_SHA256,
    }
    actual = {key: _sha256(path) for key, path in paths.items()}
    if actual != expected:
        raise ValueError("one or more pinned parent hashes changed")

    compatibility = _read_json(paths["compatibility_result"])
    periodic = _read_json(paths["periodic_box_result"])
    balanced = _read_json(paths["balanced_control_chain_result"])
    handoff = _read_json(paths["autonomous_handoff_result"])
    adjoint_gate = _read_json(paths["root_adjoint_gate_result"])
    quadratic = _read_json(paths["quadratic_carrier_result"])
    compatibility_scope = compatibility.get("scope", {})
    periodic_validation = periodic.get("validation", {})
    balanced_certificate = balanced.get("certificate", {})
    handoff_certificate = handoff.get("certificate", {})
    handoff_scope = handoff.get("scope", {})
    adjoint_audit = adjoint_gate.get("audit", {})
    adjoint_certificate = adjoint_audit.get("certificate", {})
    adjoint_scope = adjoint_audit.get("scope", {})
    quadratic_audit = quadratic.get("audit", {})
    quadratic_certificate = quadratic_audit.get("certificate", {})
    quadratic_scope = quadratic_audit.get("scope", {})
    checks = {
        "parent_refuses_literal_model_identity": (
            compatibility_scope.get("same_literal_rfde") is False
        ),
        "parent_refuses_existing_three_input_theorem": (
            compatibility_scope.get(
                "three_input_three_output_parameter_linked_theorem"
            )
            is False
        ),
        "center_periodic_orbit_and_response_validated": (
            periodic_validation.get("all_d1_d3_d4_validated") is True
        ),
        "center_periodic_unique_extrema_validated": (
            periodic_validation.get("d3_validated") is True
        ),
        "center_periodic_bordered_inverse_validated": (
            periodic_validation.get("continuation", {}).get(
                "parameter_box_bordered_inverse_validated"
            )
            is True
        ),
        "balanced_parent_allows_arbitrary_finite_node_count": (
            balanced_certificate.get(
                "arbitrary_finite_node_count_formula_validated"
            )
            is True
        ),
        "balanced_parent_has_topology_independent_synchronous_restriction": (
            balanced_certificate.get(
                "topology_independent_synchronous_scalar_restriction_validated"
            )
            is True
        ),
        "balanced_parent_refuses_full_network_periodic_attraction": (
            balanced_certificate.get(
                "full_network_periodic_attraction_validated"
            )
            is False
        ),
        "balanced_parent_has_two_controlled_voltage_excursions": (
            balanced_certificate.get(
                "positive_finite_controlled_excursion_validated"
            )
            is True
            and balanced_certificate.get(
                "negative_finite_controlled_excursion_validated"
            )
            is True
        ),
        "balanced_parent_refuses_unforced_biological_action_potential": (
            balanced_certificate.get("unforced_onset_validated") is False
            and balanced_certificate.get("biological_basin_validated") is False
            and balanced_certificate.get("action_potential_validated") is False
        ),
        "handoff_uses_same_baseline_at_eta_zero": (
            handoff_scope.get("same_delayed_fhn_baseline_model") is True
        ),
        "handoff_has_finite_autonomous_crossings_after_controlled_handoff": (
            handoff_certificate.get("positive_finite_autonomous_excursion_validated")
            is True
            and handoff_certificate.get(
                "negative_finite_autonomous_excursion_validated"
            )
            is True
        ),
        "handoff_refuses_autonomous_onset": (
            handoff_certificate.get("autonomous_onset_validated") is False
        ),
        "linear_parent_has_exact_singular_parity_cancellation": (
            adjoint_scope.get("exact_singular_parity_cancellation") is True
            and adjoint_certificate.get(
                "leading_singular_interior_pairing_nonzero"
            )
            is False
        ),
        "linear_parent_refuses_moment_only_root_inference": (
            adjoint_certificate.get("nonzero_first_moment_validated") is True
            and adjoint_certificate.get(
                "nonzero_moment_implies_nonzero_selected_root_response"
            )
            is False
        ),
        "linear_parent_refuses_fixed_epsilon_nonzero_rho": (
            adjoint_certificate.get("fixed_epsilon_one_fifth_overlap_validated")
            is False
            and adjoint_scope.get("nonzero_rho_star") is False
        ),
        "quadratic_parent_has_nonzero_leading_pairing": (
            quadratic_certificate.get(
                "quadratic_carrier_leading_pairing_nonzero"
            )
            is True
            and quadratic_certificate.get(
                "linear_carrier_leading_pairing_nonzero"
            )
            is False
        ),
        "quadratic_parent_has_canonical_small_delta_root_response": (
            quadratic_certificate.get(
                "fixed_scaled_support_canonical_root_response_proved"
            )
            is True
            and quadratic_scope.get("fixed_scaled_support_canonical_selected_root")
            is True
        ),
        "quadratic_parent_has_qualitative_periodic_branch": (
            quadratic_certificate.get(
                "qualitative_three_parameter_periodic_branch_proved"
            )
            is True
        ),
        "quadratic_parent_has_zero_center_periodic_eta_column": (
            quadratic_certificate.get(
                "center_periodic_frequency_amplitude_eta_column_zero"
            )
            is True
        ),
        "quadratic_parent_refuses_quantitative_eta_periodic_box": (
            quadratic_certificate.get("quantitative_eta_periodic_box_validated")
            is False
        ),
        "quadratic_parent_refuses_fixed_epsilon_nonzero_rho": (
            quadratic_certificate.get(
                "fixed_epsilon_one_fifth_rho_nonzero_validated"
            )
            is False
            and quadratic_scope.get("fixed_epsilon_one_fifth_nonzero_rho")
            is False
        ),
    }
    if not all(checks.values()):
        raise ValueError("one or more pinned parent claim checks failed")
    return actual, checks


def main() -> None:
    arguments = parse_arguments()
    repository = Path(__file__).resolve().parents[1]
    parent_hashes, parent_checks = _verify_parents(repository)
    source_path = Path(proof_source.__file__).resolve()
    generator_path = Path(__file__).resolve()
    certificate = reference_unified_escape_certificate()
    scope = {
        field.removesuffix("_validated"): getattr(certificate, field)
        for field in certificate.__dataclass_fields__
        if field.endswith("_validated")
    }
    payload = {
        "provenance": {
            "generator": GENERATOR_RELATIVE_PATH,
            "generator_sha256": _sha256(generator_path),
            "proof_source": PROOF_SOURCE_RELATIVE_PATH,
            "proof_source_sha256": _sha256(source_path),
            "parent_sha256": parent_hashes,
            "parent_claim_checks": parent_checks,
            "argv": [
                sys.executable,
                "experiments/unified_rfde_period_locked_escape.py",
            ],
            "default_command": DEFAULT_COMMAND,
            "python": platform.python_version(),
            "platform": platform.platform(),
            "arithmetic": ARITHMETIC_DESCRIPTION,
            "distinguished_period_definition": DISTINGUISHED_PERIOD_DEFINITION,
        },
        "certificate": _json_value(asdict(certificate)),
        "exact_audits": {
            "finite_atom": _json_value(
                asdict(reference_finite_atom_invisibility_audit())
            ),
            "heterogeneous_curvature": _json_value(
                asdict(reference_heterogeneous_curvature_synchrony_audit())
            ),
            "period_locked": _json_value(
                asdict(reference_period_locked_escape_audit())
            ),
            "linear_canard_parity": _json_value(
                asdict(reference_linear_canard_parity_audit())
            ),
        },
        "scope": scope,
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    arguments.output.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
