#!/usr/bin/env python3
"""Generate the quadratic physical-onset/capture stop-go certificate."""

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

import canard_control.quadratic_physical_onset_stop_go as proof_source
from canard_control.quadratic_physical_onset_stop_go import (
    ARITHMETIC_DESCRIPTION,
    AUTONOMOUS_HANDOFF_RESULT_SHA256,
    BALANCED_CONTROL_CHAIN_RESULT_SHA256,
    BOUNDED_PREPARATION_RESULT_SHA256,
    DEFAULT_COMMAND,
    FIXED_EPSILON_BVP_RESULT_SHA256,
    GENERATOR_RELATIVE_PATH,
    PERIODIC_ATTRACTION_RESULT_SHA256,
    PERIODIC_BOX_RESULT_SHA256,
    PHYSICAL_OUTER_BRIDGE_DOC_SHA256,
    PROOF_SOURCE_RELATIVE_PATH,
    QUADRATIC_CARRIER_RESULT_SHA256,
    QUADRATIC_DOBRUSHIN_RESULT_SHA256,
    ROBUST_HANDOFF_RESULT_SHA256,
    UNFORCED_CAPTURE_DOC_SHA256,
    reference_composition_mismatch_audit,
    reference_controlled_quadratic_transfer_audit,
    reference_stop_go_certificate,
    validate_stop_go_payload,
)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "experiments/results/quadratic_physical_onset_stop_go.json"
        ),
    )
    return parser.parse_args()


def _sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _json_value(value: Any) -> Any:
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
        "quadratic_carrier_result": repository
        / "experiments/results/quadratic_period_locked_root_carrier.json",
        "quadratic_dobrushin_result": repository
        / "experiments/results/quadratic_period_lock_dobrushin_lift.json",
        "fixed_epsilon_bvp_result": repository
        / "experiments/results/fixed_epsilon_quadratic_root_bvp.json",
        "bounded_preparation_result": repository
        / "experiments/results/fhn_bounded_additive_preparation.json",
        "balanced_control_chain_result": repository
        / "experiments/results/fhn_balanced_control_chain.json",
        "robust_handoff_result": repository
        / "experiments/results/fhn_robust_handoff_tube.json",
        "autonomous_handoff_result": repository
        / "experiments/results/fhn_autonomous_handoff_excursion.json",
        "periodic_box_result": repository
        / "experiments/results/fhn_periodic_parameter_box.json",
        "periodic_attraction_result": repository
        / "experiments/results/fhn_dobrushin_periodic_attraction.json",
        "physical_outer_bridge_doc": repository
        / "docs/paper-iii-physical-outer-pulse-bridge.md",
        "unforced_capture_doc": repository
        / "docs/paper-iii-unforced-capture-no-return.md",
    }
    expected = {
        "quadratic_carrier_result": QUADRATIC_CARRIER_RESULT_SHA256,
        "quadratic_dobrushin_result": QUADRATIC_DOBRUSHIN_RESULT_SHA256,
        "fixed_epsilon_bvp_result": FIXED_EPSILON_BVP_RESULT_SHA256,
        "bounded_preparation_result": BOUNDED_PREPARATION_RESULT_SHA256,
        "balanced_control_chain_result": BALANCED_CONTROL_CHAIN_RESULT_SHA256,
        "robust_handoff_result": ROBUST_HANDOFF_RESULT_SHA256,
        "autonomous_handoff_result": AUTONOMOUS_HANDOFF_RESULT_SHA256,
        "periodic_box_result": PERIODIC_BOX_RESULT_SHA256,
        "periodic_attraction_result": PERIODIC_ATTRACTION_RESULT_SHA256,
        "physical_outer_bridge_doc": PHYSICAL_OUTER_BRIDGE_DOC_SHA256,
        "unforced_capture_doc": UNFORCED_CAPTURE_DOC_SHA256,
    }
    actual = {key: _sha256(path) for key, path in paths.items()}
    if actual != expected:
        changed = [key for key in expected if actual[key] != expected[key]]
        raise ValueError(f"pinned parent hashes changed: {changed}")

    quadratic = _read_json(paths["quadratic_carrier_result"])["audit"]
    dobrushin = _read_json(paths["quadratic_dobrushin_result"])["audit"]
    fixed_bvp = _read_json(paths["fixed_epsilon_bvp_result"])["audit"]
    preparation = _read_json(paths["bounded_preparation_result"])
    balanced_chain = _read_json(paths["balanced_control_chain_result"])
    robust = _read_json(paths["robust_handoff_result"])
    autonomous = _read_json(paths["autonomous_handoff_result"])
    periodic = _read_json(paths["periodic_box_result"])
    basin = _read_json(paths["periodic_attraction_result"])
    outer_text = paths["physical_outer_bridge_doc"].read_text(encoding="utf-8")
    capture_text = paths["unforced_capture_doc"].read_text(encoding="utf-8")

    quadratic_certificate = quadratic.get("certificate", {})
    quadratic_scope = quadratic.get("scope", {})
    dobrushin_certificate = dobrushin.get("certificate", {})
    dobrushin_scope = dobrushin.get("scope", {})
    fixed_certificate = fixed_bvp.get("certificate", {})
    prep_certificate = preparation.get("certificate", {})
    prep_scope = preparation.get("scope", {})
    balanced_certificate = balanced_chain.get("certificate", {})
    balanced_scope = balanced_chain.get("scope", {})
    robust_certificate = robust.get("certificate", {})
    robust_scope = robust.get("scope", {})
    autonomous_certificate = autonomous.get("certificate", {})
    periodic_validation = periodic.get("validation", {})
    basin_certificate = basin.get("certificate", {})
    basin_scope = basin.get("scope", {})
    checks = {
        "small_delta_canonical_root_proved": (
            quadratic_scope.get("fixed_scaled_support_canonical_selected_root")
            is True
            and dobrushin_scope.get(
                "uniform_dobrushin_full_network_canonical_root"
            )
            is True
        ),
        "fixed_epsilon_root_refused": (
            quadratic_certificate.get(
                "fixed_epsilon_one_fifth_rho_nonzero_validated"
            )
            is False
            and dobrushin_certificate.get(
                "fixed_epsilon_one_fifth_root_response_validated"
            )
            is False
            and fixed_certificate.get("fixed_epsilon_selected_root_validated")
            is False
        ),
        "physical_onset_refused_by_root_parents": (
            quadratic_certificate.get("physical_onset_identification_validated")
            is False
            and dobrushin_certificate.get(
                "input_independent_physical_onset_identified"
            )
            is False
            and fixed_certificate.get("physical_onset_identification_validated")
            is False
        ),
        "bounded_preparation_is_controlled_fixed_slice": (
            prep_scope.get("same_fixed_rank_one_d3_e2_fhn_model") is True
            and prep_scope.get("unforced_or_maximal_canard_onset") is False
            and prep_certificate.get("unfolding") == "3/5"
            and prep_certificate.get("epsilon") == "1/5"
        ),
        "balanced_control_chain_has_general_bounded_preparation": (
            balanced_certificate.get(
                "exact_model_additive_preparation_validated"
            )
            is True
            and balanced_certificate.get(
                "finite_time_exact_complete_history_preparation_validated"
            )
            is True
            and balanced_certificate.get(
                "topology_and_node_count_independent_authority_validated"
            )
            is True
            and balanced_scope.get(
                "balanced_general_topology_bounded_additive_preparation_on_declared_bounded_initial_data_cylinder"
            )
            is True
        ),
        "robust_handoff_has_residual_budget": (
            robust_certificate.get("bounded_shutdown_residual_inputs_validated")
            is True
            and robust_certificate.get(
                "post_handoff_voltage_input_residual_bound"
            )
            == "0.00001"
        ),
        "robust_handoff_refuses_basin_and_no_return": (
            robust_scope.get("quiet_or_pulse_basin") is False
            and robust_scope.get("permanent_no_return") is False
            and robust_scope.get("landing_on_periodic_branch") is False
        ),
        "autonomous_handoff_refuses_autonomous_onset": (
            autonomous_certificate.get("autonomous_onset_validated") is False
            and autonomous_certificate.get("permanent_no_return_validated")
            is False
        ),
        "periodic_branch_is_fixed_reference_slice": (
            periodic_validation.get("all_d1_d3_d4_validated") is True
            and periodic.get("scope", {}).get("d1_parameter_box_continuation")
            is True
        ),
        "periodic_attraction_is_local_eta_zero": (
            basin_certificate.get(
                "full_network_nonlinear_local_orbital_attraction_validated"
            )
            is True
            and basin_certificate.get(
                "arbitrary_admitted_balanced_topology_covered"
            )
            is True
            and basin_certificate.get("uniform_nonlinear_basin_over_network_class")
            is False
            and basin_certificate.get("nonzero_eta_full_network_attraction_validated")
            is False
            and basin_scope.get("eta_zero_quadratic_period_locked_model")
            is True
            and basin_certificate.get("model_id")
            == "balanced-dobrushin-dual-scaffold-fhn-quadratic-period-lock-periodic-attraction"
        ),
        "periodic_attraction_refuses_biological_capture": (
            basin_certificate.get("biological_pulse_capture_validated") is False
            and basin_scope.get("biological_pulse_capture") is False
        ),
        "paper_iii_physical_bridge_still_conditional": (
            "physical RFDE comparison remains conditional" in outer_text
            and "U-CAP is still open" in outer_text
        ),
        "paper_iii_capture_gate_still_open": (
            "biological U-CAP remains open" in capture_text
        ),
    }
    if not all(checks.values()):
        failed = [key for key, value in checks.items() if not value]
        raise ValueError(f"pinned parent claim checks failed: {failed}")
    return actual, checks


def main() -> None:
    arguments = parse_arguments()
    repository = Path(__file__).resolve().parents[1]
    parent_hashes, parent_checks = _verify_parents(repository)
    source_path = Path(proof_source.__file__).resolve()
    generator_path = Path(__file__).resolve()
    certificate = reference_stop_go_certificate()
    scope = {
        field.removesuffix("_validated"): getattr(certificate, field)
        for field in certificate.__dataclass_fields__
        if field.endswith("_validated")
    }
    payload = {
        "certificate": _json_value(asdict(certificate)),
        "exact_audits": {
            "composition_mismatch": _json_value(
                asdict(reference_composition_mismatch_audit())
            ),
            "controlled_quadratic_transfer": _json_value(
                asdict(reference_controlled_quadratic_transfer_audit())
            ),
        },
        "provenance": {
            "generator": GENERATOR_RELATIVE_PATH,
            "generator_sha256": _sha256(generator_path),
            "proof_source": PROOF_SOURCE_RELATIVE_PATH,
            "proof_source_sha256": _sha256(source_path),
            "parent_sha256": parent_hashes,
            "parent_claim_checks": parent_checks,
            "argv": [sys.executable, GENERATOR_RELATIVE_PATH],
            "default_command": DEFAULT_COMMAND,
            "python": platform.python_version(),
            "platform": platform.platform(),
            "arithmetic": ARITHMETIC_DESCRIPTION,
        },
        "scope": scope,
    }
    validate_stop_go_payload(payload)
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
