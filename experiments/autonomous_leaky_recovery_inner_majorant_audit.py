#!/usr/bin/env python3
"""Build the source-bound inner leaky-periodic majorant certificate."""

from __future__ import annotations

from dataclasses import asdict
from hashlib import sha256
import json
from pathlib import Path

import gmpy2

from canard_control.fhn_periodic_directed_validation import (
    _interval_parameters,
)
from canard_control.leaky_periodic_branch_artifact import (
    canonical_sha256 as branch_canonical_sha256,
    orbit_from_artifact,
    validate_leaky_periodic_branch_artifact,
)
from canard_control.leaky_periodic_majorant_audit import (
    AUDIT_RESULT_RELATIVE_PATH,
    AUDIT_RESULT_SCHEMA_ID,
    AUDIT_SOURCE_MANIFEST,
    INNER_ARTIFACT_RELATIVE_PATH,
    audit_payload,
    canonical_sha256,
    validate_leaky_periodic_majorant_audit_result,
)
from canard_control.leaky_periodic_validation import (
    evaluate_leaky_periodic_radii_candidate,
)


REPOSITORY = Path(__file__).resolve().parents[1]


def _sha256_path(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def build_certificate(*, replay_directed: bool = True) -> dict[str, object]:
    """Build the certificate; tracked output requires a fresh full replay."""

    if not replay_directed:
        raise ValueError("the tracked audit certificate requires directed replay")
    artifact_path = REPOSITORY / INNER_ARTIFACT_RELATIVE_PATH
    branch_payload = json.loads(artifact_path.read_text(encoding="utf-8"))
    orbit = validate_leaky_periodic_branch_artifact(
        branch_payload,
        REPOSITORY,
        replay_directed=False,
    )
    settings = branch_payload["artifact"]["directed_radii_prototype"][
        "settings"
    ]
    validation = evaluate_leaky_periodic_radii_candidate(
        orbit,
        branch="inner_saddle_candidate",
        cutoff=settings["cutoff"],
        precision=settings["precision_bits"],
        maximum_radius=settings["maximum_radius"],
        chosen_radius=settings["chosen_radius"],
    )
    validation_payload = json.loads(json.dumps(asdict(validation)))
    if not (
        validation.formula_adaptation_independently_audited
        and validation.periodic_rfde_orbit_validated
        and validation.phase_bordered_rfde_inverse_validated
    ):
        raise ArithmeticError("inner leaky periodic proof gates did not close")
    precision = settings["precision_bits"]
    finite_inverse = gmpy2.mpfr(
        validation.finite.approximate_inverse_l1_upper,
        precision,
    )
    epsilon = _interval_parameters(orbit.parameters, precision)["epsilon"].upper
    formula = audit_payload(
        finite_preconditioner_l1_upper=finite_inverse,
        epsilon_upper=epsilon,
        cutoff=settings["cutoff"],
        precision=precision,
    )
    directed = {
        "preconditioned_residual_l1_upper": validation.finite.preconditioned_residual_l1_upper,
        "full_point_defect_upper": validation.blocks.full_point_defect_upper,
        **{
            name: getattr(validation.correction, name)
            for name in (
                "coefficient_z1_upper",
                "coefficient_z2_upper",
                "coefficient_z3_upper",
                "chosen_radius",
                "contraction_upper",
                "radii_margin_lower",
                "bordered_inverse_norm_upper",
            )
        },
    }
    # Refuse accidental spectral promotion even if a future dataclass default
    # changes.  These gates require a separate monodromy certificate.
    spectral_names = (
        "neutral_multiplier_algebraically_simple_validated",
        "nontranslation_unit_circle_exclusion_validated",
        "unstable_multiplier_count_validated",
        "attracting_or_saddle_index_validated",
    )
    if any(getattr(validation.floquet, name) for name in spectral_names):
        raise ArithmeticError("a Floquet spectral gate was promoted")
    certificate = {
        "schema_id": AUDIT_RESULT_SCHEMA_ID,
        "branch": "inner_saddle_candidate",
        "artifact": {
            "result_relative_path": INNER_ARTIFACT_RELATIVE_PATH,
            "file_sha256": _sha256_path(artifact_path),
            "body_sha256": branch_canonical_sha256(
                branch_payload["artifact"]
            ),
        },
        "formula_audit": formula,
        "directed_radii": directed,
        "claims": {
            "formula_adaptation_independently_audited": True,
            "inner_periodic_rfde_orbit_validated": True,
            "phase_bordered_rfde_inverse_validated": True,
            "neutral_multiplier_algebraically_simple_validated": False,
            "nontranslation_unit_circle_exclusion_validated": False,
            "unstable_multiplier_count_validated": False,
            "inner_saddle_floquet_index_validated": False,
            "outer_periodic_rfde_orbit_validated": False,
        },
    }
    payload = {
        "certificate": certificate,
        "manifest": {
            "schema_id": AUDIT_RESULT_SCHEMA_ID,
            "certificate_sha256": canonical_sha256(certificate),
            "source_sha256": {
                relative: _sha256_path(REPOSITORY / relative)
                for relative in AUDIT_SOURCE_MANIFEST
            },
            "directed_replay_completed": True,
        },
    }
    # This compares the independent evaluation above to the artifact fields
    # before the final strict validator rereads the tracked result.
    stored_validation = branch_payload["artifact"][
        "directed_radii_prototype"
    ]["validation"]
    for group in ("finite", "blocks", "correction"):
        if set(validation_payload[group]) != set(stored_validation[group]):
            raise ArithmeticError(f"directed replay changed {group} schema")
    return payload


def main() -> None:
    payload = build_certificate(replay_directed=True)
    output = REPOSITORY / AUDIT_RESULT_RELATIVE_PATH
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    validate_leaky_periodic_majorant_audit_result(payload, REPOSITORY)
    print(output)
    print(f"certificate_sha256={payload['manifest']['certificate_sha256']}")


if __name__ == "__main__":
    main()
