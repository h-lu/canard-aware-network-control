#!/usr/bin/env python3
"""Generate the quadratic reference-slice dual-basin no-go certificate."""

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

import canard_control.quadratic_reference_dual_basin_no_go as proof_source
from canard_control.quadratic_reference_dual_basin_no_go import (
    AMPLITUDE_RESULT_SHA256,
    ARITHMETIC_DESCRIPTION,
    AUTONOMOUS_HANDOFF_RESULT_SHA256,
    DEFAULT_COMMAND,
    GENERATOR_RELATIVE_PATH,
    PERIODIC_ATTRACTION_RESULT_SHA256,
    PROOF_SOURCE_RELATIVE_PATH,
    STOP_GO_RESULT_SHA256,
    SYNCHRONOUS_FLOQUET_RESULT_SHA256,
    reference_equilibrium_rouche_audit,
    reference_no_go_certificate,
    reference_periodic_face_audit,
    reference_repair_contract_audit,
    validate_no_go_payload,
)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "experiments/results/quadratic_reference_dual_basin_no_go.json"
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
        "amplitude_result": repository
        / "experiments/results/fhn_unsquared_amplitude_transfer.json",
        "periodic_attraction_result": repository
        / "experiments/results/fhn_dobrushin_periodic_attraction.json",
        "synchronous_floquet_result": repository
        / "experiments/results/fhn_synchronous_floquet_right_half_cover.json",
        "autonomous_handoff_result": repository
        / "experiments/results/fhn_autonomous_handoff_excursion.json",
        "stop_go_result": repository
        / "experiments/results/quadratic_physical_onset_stop_go.json",
    }
    expected = {
        "amplitude_result": AMPLITUDE_RESULT_SHA256,
        "periodic_attraction_result": PERIODIC_ATTRACTION_RESULT_SHA256,
        "synchronous_floquet_result": SYNCHRONOUS_FLOQUET_RESULT_SHA256,
        "autonomous_handoff_result": AUTONOMOUS_HANDOFF_RESULT_SHA256,
        "stop_go_result": STOP_GO_RESULT_SHA256,
    }
    actual = {key: _sha256(path) for key, path in paths.items()}
    if actual != expected:
        changed = [key for key in expected if actual[key] != expected[key]]
        raise ValueError(f"pinned parent hashes changed: {changed}")

    amplitude = _read_json(paths["amplitude_result"])
    attraction = _read_json(paths["periodic_attraction_result"])
    floquet = _read_json(paths["synchronous_floquet_result"])
    handoff = _read_json(paths["autonomous_handoff_result"])
    stop_go = _read_json(paths["stop_go_result"])
    amp_certificate = amplitude.get("certificate", {})
    attraction_certificate = attraction.get("certificate", {})
    attraction_scope = attraction.get("scope", {})
    floquet_certificate = floquet.get("certificate", {})
    handoff_certificate = handoff.get("certificate", {})
    stop_scope = stop_go.get("scope", {})

    maximum_lower = sp.Rational(amp_certificate["voltage_maximum_lower"])
    minimum_lower = sp.Rational(amp_certificate["voltage_minimum_lower"])
    minimum_upper = sp.Rational(amp_certificate["voltage_minimum_upper"])
    checks = {
        "periodic_extrema_validated": (
            amp_certificate.get("uniform_positive_amplitude_enclosure_validated")
            is True
            and amp_certificate.get("unique_voltage_extrema_on_gain_box") is True
        ),
        "periodic_orbit_crosses_declared_faces": bool(
            maximum_lower > sp.Rational(3, 2)
            and minimum_upper < -1
            and minimum_lower > -sp.Rational(6, 5)
        ),
        "eta_zero_periodic_local_attraction_validated": (
            attraction_scope.get("eta_zero_quadratic_period_locked_model") is True
            and attraction_scope.get("full_network_local_nonlinear_orbital_attraction")
            is True
        ),
        "nonzero_eta_attraction_refused": (
            attraction_certificate.get(
                "nonzero_eta_full_network_attraction_validated"
            )
            is False
        ),
        "uniform_basin_refused": (
            attraction_certificate.get("uniform_nonlinear_basin_over_network_class")
            is False
        ),
        "asymptotic_phase_source_validated": (
            floquet_certificate.get(
                "hale_verduyn_lunel_hyperbolic_periodic_orbit_theorem_applied"
            )
            is True
            and floquet_certificate.get(
                "synchronous_nonlinear_orbital_attraction_validated"
            )
            is True
        ),
        "handoff_faces_and_finite_excursions_validated": (
            handoff_certificate.get("positive_controlled_detector_and_handoff_face")
            == "1"
            and handoff_certificate.get("positive_autonomous_excursion_face")
            == "1.5"
            and handoff_certificate.get("negative_controlled_detector_face")
            == "-1"
            and handoff_certificate.get("negative_autonomous_excursion_face")
            == "-1.2"
            and handoff_certificate.get("positive_finite_autonomous_excursion_validated")
            is True
            and handoff_certificate.get("negative_finite_autonomous_excursion_validated")
            is True
        ),
        "handoff_permanent_no_return_refused": (
            handoff_certificate.get("permanent_no_return_validated") is False
        ),
        "prior_stop_go_refuses_capture_and_basin": (
            stop_scope.get("pulse_quiet_capture") is False
            and stop_scope.get("quiet_basin") is False
            and stop_scope.get("terminal_block_periodic_basin_containment")
            is False
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
    certificate = reference_no_go_certificate()
    scope = {
        field.removesuffix("_validated"): getattr(certificate, field)
        for field in certificate.__dataclass_fields__
        if field.endswith("_validated")
    }
    payload = {
        "certificate": _json_value(asdict(certificate)),
        "exact_audits": {
            "equilibrium_rouche": _json_value(
                asdict(reference_equilibrium_rouche_audit())
            ),
            "periodic_faces": _json_value(
                asdict(reference_periodic_face_audit())
            ),
            "repair_contracts": _json_value(
                asdict(reference_repair_contract_audit())
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
    validate_no_go_payload(payload)
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
