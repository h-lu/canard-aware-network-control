"""Independent formula audit for the leaky periodic Wiener proof.

The non-leaky periodic validator is adapted to

    F_w(v,w,T) = D w - T epsilon (v-a-w).

Relative to the old recovery equation, the added coefficient-space map is

    L(v,w,T) = (0, epsilon T w, 0).

This module records the exact operator identities that are used in the
adaptation and supplies the one norm calculation that is easy to get wrong:
on the product l1 norm, the derivative variation of ``L`` costs one, rather
than two, copies of ``epsilon``.  It also takes the maximum of the finite and
analytic-tail preconditioner norms, so the formula does not rely silently on
the finite inverse being the larger block.

The accompanying proof is in
``docs/leaky-periodic-majorant-audit.md``.  This source contains no Floquet
claim; a phase-bordered periodic-orbit inverse is not a multiplier count.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation, localcontext
from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Mapping

import gmpy2

from canard_control.directed_interval import (
    DirectedInterval,
    decimal_upper,
    pi_interval,
)


AUDIT_VERSION = "leaky-periodic-majorant-audit-v1"
AUDIT_RESULT_SCHEMA_ID = "leaky-periodic-inner-majorant-certificate-v1"
AUDIT_RESULT_RELATIVE_PATH = (
    "experiments/results/autonomous_leaky_recovery_inner_majorant_audit.json"
)
INNER_ARTIFACT_RELATIVE_PATH = (
    "experiments/results/"
    "autonomous_leaky_recovery_inner_branch_artifact.json"
)
AUDIT_SOURCE_MANIFEST = (
    "src/canard_control/leaky_periodic_majorant_audit.py",
    "src/canard_control/leaky_periodic_validation.py",
    "src/canard_control/leaky_periodic_branch_artifact.py",
    "src/canard_control/fhn_periodic_infinite_validation.py",
    "src/canard_control/fhn_periodic_directed_validation.py",
    "src/canard_control/directed_interval.py",
    "experiments/autonomous_leaky_recovery_inner_majorant_audit.py",
    INNER_ARTIFACT_RELATIVE_PATH,
)


@dataclass(frozen=True)
class LeakyPeriodicMajorantFormulaAudit:
    """Truth-valued ledger for the equation-level adaptation theorem."""

    audit_version: str
    added_operator: str
    added_derivative: str
    added_derivative_variation: str
    recovery_residual_identity_proved: bool
    recovery_state_columns_proved: bool
    recovery_period_column_proved: bool
    finite_tail_cross_blocks_unchanged_proved: bool
    recovery_tail_column_bound_proved: bool
    nonlinear_z1_increment_proved: bool
    old_nonlinear_and_delay_majorants_transfer_proved: bool
    formula_adaptation_independently_audited: bool
    excluded_claims: tuple[str, ...]


def build_leaky_periodic_majorant_formula_audit(
) -> LeakyPeriodicMajorantFormulaAudit:
    """Return the fixed theorem ledger proved in the accompanying note."""

    return LeakyPeriodicMajorantFormulaAudit(
        audit_version=AUDIT_VERSION,
        added_operator="L(v,w,T)=(0,epsilon*T*w,0)",
        added_derivative=(
            "DL(v,w,T)[u]=(0,epsilon*(T*u_w+w*u_T),0)"
        ),
        added_derivative_variation=(
            "(DL(x+h)-DL(x))[u]="
            "(0,epsilon*(h_T*u_w+h_w*u_T),0)"
        ),
        recovery_residual_identity_proved=True,
        recovery_state_columns_proved=True,
        recovery_period_column_proved=True,
        finite_tail_cross_blocks_unchanged_proved=True,
        recovery_tail_column_bound_proved=True,
        nonlinear_z1_increment_proved=True,
        old_nonlinear_and_delay_majorants_transfer_proved=True,
        formula_adaptation_independently_audited=True,
        excluded_claims=(
            "neutral Floquet multiplier algebraic simplicity",
            "unit-circle exclusion away from one",
            "unstable multiplier count or attracting/saddle index",
            "outer-branch periodic orbit without its own replay artifact",
        ),
    )


def analytic_tail_preconditioner_norm_upper(
    cutoff: int,
    precision: int,
) -> gmpy2.mpfr:
    """Bound ``||D_Q^{-1}||`` on modes ``|k| >= cutoff+1``.

    Multiplication by ``1/i`` is an isometry for the component complex norm
    ``|Re z|+|Im z|``.  Hence the exact norm is
    ``1/(2*pi*(cutoff+1))``; the returned endpoint is rounded upward.
    """

    if cutoff < 0:
        raise ValueError("cutoff must be nonnegative")
    denominator = (
        pi_interval(precision)
        * DirectedInterval.from_decimal(2 * (cutoff + 1), precision)
    )
    return (DirectedInterval.from_decimal(1, precision) / denominator).upper


def full_preconditioner_norm_upper(
    finite_preconditioner_l1_upper: gmpy2.mpfr,
    cutoff: int,
    precision: int,
) -> gmpy2.mpfr:
    """Return ``max(||A_P||_1, ||D_Q^{-1}||)`` with directed bounds."""

    if finite_preconditioner_l1_upper < 0:
        raise ValueError("finite preconditioner norm must be nonnegative")
    return max(
        finite_preconditioner_l1_upper,
        analytic_tail_preconditioner_norm_upper(cutoff, precision),
    )


def leak_derivative_variation_z1_increment_upper(
    epsilon_upper: gmpy2.mpfr,
    finite_preconditioner_l1_upper: gmpy2.mpfr,
    cutoff: int,
    precision: int,
) -> gmpy2.mpfr:
    """Bound the additional coefficient in the derivative variation.

    If ``||h||_1 <= rho`` and ``||u||_1 <= 1``, the two nonzero input
    columns of ``DL(x+h)-DL(x)`` have norms ``epsilon*|h_T|`` and
    ``epsilon*||h_w||``.  The induced l1 norm is their maximum, so it is at
    most ``epsilon*rho``.  Preconditioning adds
    ``||A||*epsilon`` to the coefficient of ``rho`` and nothing to the
    quadratic or cubic coefficients.
    """

    if epsilon_upper < 0:
        raise ValueError("epsilon upper bound must be nonnegative")
    preconditioner = full_preconditioner_norm_upper(
        finite_preconditioner_l1_upper,
        cutoff,
        precision,
    )
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        return preconditioner * epsilon_upper


def audit_payload(
    *,
    finite_preconditioner_l1_upper: gmpy2.mpfr,
    epsilon_upper: gmpy2.mpfr,
    cutoff: int,
    precision: int,
) -> dict[str, object]:
    """Serialize the theorem ledger and its directed norm specialization."""

    audit = build_leaky_periodic_majorant_formula_audit()
    tail = analytic_tail_preconditioner_norm_upper(cutoff, precision)
    full = full_preconditioner_norm_upper(
        finite_preconditioner_l1_upper, cutoff, precision
    )
    increment = leak_derivative_variation_z1_increment_upper(
        epsilon_upper,
        finite_preconditioner_l1_upper,
        cutoff,
        precision,
    )
    return {
        "audit_version": audit.audit_version,
        "operator_identities": {
            "added_operator": audit.added_operator,
            "added_derivative": audit.added_derivative,
            "added_derivative_variation": audit.added_derivative_variation,
        },
        "proof_ledger": {
            name: getattr(audit, name)
            for name in (
                "recovery_residual_identity_proved",
                "recovery_state_columns_proved",
                "recovery_period_column_proved",
                "finite_tail_cross_blocks_unchanged_proved",
                "recovery_tail_column_bound_proved",
                "nonlinear_z1_increment_proved",
                "old_nonlinear_and_delay_majorants_transfer_proved",
                "formula_adaptation_independently_audited",
            )
        },
        "directed_specialization": {
            "cutoff": cutoff,
            "precision_bits": precision,
            "finite_preconditioner_l1_upper": decimal_upper(
                finite_preconditioner_l1_upper
            ),
            "analytic_tail_preconditioner_l1_upper": decimal_upper(tail),
            "full_preconditioner_l1_upper": decimal_upper(full),
            "epsilon_upper": decimal_upper(epsilon_upper),
            "leak_z1_increment_upper": decimal_upper(increment),
            "finite_block_dominates_tail_block": (
                finite_preconditioner_l1_upper >= tail
            ),
        },
        "excluded_claims": list(audit.excluded_claims),
    }


def canonical_sha256(value: object) -> str:
    """Hash one JSON value with a deterministic UTF-8 encoding."""

    encoded = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    return sha256(encoded).hexdigest()


def _decimal(value: object, name: str) -> Decimal:
    if not isinstance(value, str):
        raise ValueError(f"{name} must be a decimal string")
    try:
        number = Decimal(value)
    except InvalidOperation as error:
        raise ValueError(f"{name} is not decimal") from error
    if not number.is_finite():
        raise ValueError(f"{name} must be finite")
    return number


def _sha256_path(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def validate_leaky_periodic_majorant_audit_result(
    payload: Mapping[str, Any],
    repository: Path,
) -> None:
    """Hostile structural validation of the tracked inner audit result."""

    if set(payload) != {"certificate", "manifest"}:
        raise ValueError("majorant audit result has the wrong outer schema")
    certificate = payload.get("certificate")
    manifest = payload.get("manifest")
    if not isinstance(certificate, Mapping) or not isinstance(manifest, Mapping):
        raise ValueError("majorant audit certificate and manifest must be mappings")
    expected_certificate_keys = {
        "schema_id",
        "branch",
        "artifact",
        "formula_audit",
        "directed_radii",
        "claims",
    }
    if set(certificate) != expected_certificate_keys:
        raise ValueError("majorant audit certificate schema changed")
    if certificate.get("schema_id") != AUDIT_RESULT_SCHEMA_ID:
        raise ValueError("majorant audit schema id changed")
    if certificate.get("branch") != "inner_saddle_candidate":
        raise ValueError("majorant audit branch changed")
    expected_manifest_keys = {
        "schema_id",
        "certificate_sha256",
        "source_sha256",
        "directed_replay_completed",
    }
    if set(manifest) != expected_manifest_keys:
        raise ValueError("majorant audit manifest schema changed")
    if manifest.get("schema_id") != AUDIT_RESULT_SCHEMA_ID:
        raise ValueError("majorant audit manifest id changed")
    if manifest.get("certificate_sha256") != canonical_sha256(certificate):
        raise ValueError("majorant audit certificate digest changed")
    if manifest.get("directed_replay_completed") is not True:
        raise ValueError("majorant audit did not replay the directed proof")
    hashes = manifest.get("source_sha256")
    if not isinstance(hashes, Mapping) or set(hashes) != set(
        AUDIT_SOURCE_MANIFEST
    ):
        raise ValueError("majorant audit source manifest changed")
    for relative in AUDIT_SOURCE_MANIFEST:
        if hashes.get(relative) != _sha256_path(repository / relative):
            raise ValueError(f"majorant audit source hash changed for {relative}")

    artifact_record = certificate.get("artifact")
    if not isinstance(artifact_record, Mapping) or set(artifact_record) != {
        "result_relative_path",
        "file_sha256",
        "body_sha256",
    }:
        raise ValueError("majorant audit artifact record changed")
    if artifact_record.get("result_relative_path") != INNER_ARTIFACT_RELATIVE_PATH:
        raise ValueError("majorant audit artifact path changed")
    artifact_path = repository / INNER_ARTIFACT_RELATIVE_PATH
    if artifact_record.get("file_sha256") != _sha256_path(artifact_path):
        raise ValueError("majorant audit artifact file digest changed")
    artifact_payload = json.loads(artifact_path.read_text(encoding="utf-8"))
    from canard_control.leaky_periodic_branch_artifact import (
        canonical_sha256 as branch_canonical_sha256,
        validate_leaky_periodic_branch_artifact,
    )

    validate_leaky_periodic_branch_artifact(artifact_payload, repository)
    if artifact_record.get("body_sha256") != branch_canonical_sha256(
        artifact_payload["artifact"]
    ):
        raise ValueError("majorant audit artifact body digest changed")

    formula = certificate.get("formula_audit")
    if not isinstance(formula, Mapping) or set(formula) != {
        "audit_version",
        "operator_identities",
        "proof_ledger",
        "directed_specialization",
        "excluded_claims",
    }:
        raise ValueError("majorant formula audit schema changed")
    if formula.get("audit_version") != AUDIT_VERSION:
        raise ValueError("majorant formula audit version changed")
    ledger = formula.get("proof_ledger")
    if not isinstance(ledger, Mapping) or not ledger or any(
        value is not True for value in ledger.values()
    ):
        raise ValueError("majorant formula proof ledger is not closed")
    specialization = formula.get("directed_specialization")
    if not isinstance(specialization, Mapping):
        raise ValueError("majorant directed specialization changed")
    if specialization.get("cutoff") != 192:
        raise ValueError("majorant cutoff changed")
    if specialization.get("precision_bits") != 160:
        raise ValueError("majorant precision changed")
    finite = _decimal(
        specialization.get("finite_preconditioner_l1_upper"),
        "finite preconditioner norm",
    )
    tail = _decimal(
        specialization.get("analytic_tail_preconditioner_l1_upper"),
        "tail preconditioner norm",
    )
    full = _decimal(
        specialization.get("full_preconditioner_l1_upper"),
        "full preconditioner norm",
    )
    epsilon = _decimal(specialization.get("epsilon_upper"), "epsilon")
    increment = _decimal(
        specialization.get("leak_z1_increment_upper"),
        "leak Z1 increment",
    )
    if specialization.get("finite_block_dominates_tail_block") is not (
        finite >= tail
    ):
        raise ValueError("preconditioner dominance flag changed")
    if full != max(finite, tail):
        raise ValueError("full preconditioner norm is not the block maximum")
    with localcontext() as context:
        context.prec = 200
        exact_product = full * epsilon
        tolerance = Decimal("1e-40") * max(Decimal(1), exact_product)
        if increment + tolerance < exact_product:
            raise ValueError("leak Z1 increment is not an upper bound")
        if increment - exact_product > tolerance:
            raise ValueError("leak Z1 increment has unexplained excess")

    directed = certificate.get("directed_radii")
    if not isinstance(directed, Mapping) or set(directed) != {
        "preconditioned_residual_l1_upper",
        "full_point_defect_upper",
        "coefficient_z1_upper",
        "coefficient_z2_upper",
        "coefficient_z3_upper",
        "chosen_radius",
        "contraction_upper",
        "radii_margin_lower",
        "bordered_inverse_norm_upper",
    }:
        raise ValueError("majorant directed-radii record changed")
    branch_validation = artifact_payload["artifact"]["directed_radii_prototype"][
        "validation"
    ]
    expected_directed = {
        "preconditioned_residual_l1_upper": branch_validation["finite"][
            "preconditioned_residual_l1_upper"
        ],
        "full_point_defect_upper": branch_validation["blocks"][
            "full_point_defect_upper"
        ],
        **{
            name: branch_validation["correction"][name]
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
    if dict(directed) != expected_directed:
        raise ValueError("majorant directed bounds differ from the branch proof")
    if _decimal(directed["contraction_upper"], "contraction") >= 1:
        raise ValueError("majorant contraction gate is not strict")
    if _decimal(directed["radii_margin_lower"], "radii margin") <= 0:
        raise ValueError("majorant radii margin is not strict")

    claims = certificate.get("claims")
    if not isinstance(claims, Mapping) or set(claims) != {
        "formula_adaptation_independently_audited",
        "inner_periodic_rfde_orbit_validated",
        "phase_bordered_rfde_inverse_validated",
        "neutral_multiplier_algebraically_simple_validated",
        "nontranslation_unit_circle_exclusion_validated",
        "unstable_multiplier_count_validated",
        "inner_saddle_floquet_index_validated",
        "outer_periodic_rfde_orbit_validated",
    }:
        raise ValueError("majorant claim ledger changed")
    expected_true = (
        "formula_adaptation_independently_audited",
        "inner_periodic_rfde_orbit_validated",
        "phase_bordered_rfde_inverse_validated",
    )
    expected_false = tuple(name for name in claims if name not in expected_true)
    if any(claims[name] is not True for name in expected_true) or any(
        claims[name] is not False for name in expected_false
    ):
        raise ValueError("majorant claim ledger over- or under-promoted")


__all__ = [
    "AUDIT_RESULT_RELATIVE_PATH",
    "AUDIT_RESULT_SCHEMA_ID",
    "AUDIT_SOURCE_MANIFEST",
    "AUDIT_VERSION",
    "INNER_ARTIFACT_RELATIVE_PATH",
    "LeakyPeriodicMajorantFormulaAudit",
    "analytic_tail_preconditioner_norm_upper",
    "audit_payload",
    "build_leaky_periodic_majorant_formula_audit",
    "canonical_sha256",
    "full_preconditioner_norm_upper",
    "leak_derivative_variation_z1_increment_upper",
    "validate_leaky_periodic_majorant_audit_result",
]
