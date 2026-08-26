"""Source-bound neutral-Floquet transfer for the leaky periodic branches.

The inner and outer leaky-recovery periodic-orbit artifacts validate two
phase-fixed RFDE orbits and the inverses of their correctly bordered
periodic derivatives.  This module supplies the missing theorem-level seam
from those bordered Fourier inverses to the history-space monodromy.

There are two conclusions, kept deliberately separate from the still-open
global Floquet index problem.

* On each branch, the autonomous multiplier ``1`` is algebraically simple.
  The proof uses the exact moving-delay period column, not merely the fact
  that the periodic kernel is one-dimensional.
* A directed perturbation estimate excludes every other unit multiplier on
  an explicit punctured arc about ``1``.

Nothing in this module excludes the remaining compact unit-circle arc or
counts multipliers outside the unit disk.  In particular, attraction of the
outer orbit and the one-unstable-multiplier index of the inner orbit remain
false in the returned claim ledger.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from hashlib import sha256
import json
from pathlib import Path
import platform
from typing import Any, Mapping

import gmpy2
import numpy as np
import scipy

from canard_control.directed_interval import (
    DirectedInterval,
    decimal_lower,
    decimal_upper,
    pi_interval,
    upward_sum,
)
from canard_control.fhn_periodic_candidate import PeriodicOrbitCandidate
from canard_control.fhn_periodic_infinite_validation import (
    _sequence_box_norm_upper,
)
from canard_control.leaky_outer_high_resolution import (
    validate_outer_high_resolution_artifact,
)
from canard_control.leaky_periodic_branch_artifact import (
    validate_leaky_periodic_branch_artifact,
)
from canard_control.leaky_periodic_validation import (
    _build_leaky_base_sequences,
)
from canard_control.rfde_floquet_transfer import (
    _nonconstant_mode_lower,
    _residual_sequence_norm_upper,
    _state_sequence_norm_upper,
    periodic_orbit_candidate_fingerprint,
)


SCHEMA_ID = "leaky-floquet-neutral-transfer-v1"
SOURCE_RELATIVE_PATH = "src/canard_control/leaky_floquet_transfer.py"
GENERATOR_RELATIVE_PATH = "experiments/leaky_floquet_transfer.py"
NOTE_RELATIVE_PATH = "docs/leaky-floquet-transfer.md"
RESULT_RELATIVE_PATH = "experiments/results/leaky_floquet_transfer.json"
INNER_RESULT_RELATIVE_PATH = (
    "experiments/results/"
    "autonomous_leaky_recovery_inner_branch_artifact.json"
)
OUTER_RESULT_RELATIVE_PATH = (
    "experiments/results/"
    "autonomous_leaky_recovery_outer_high_resolution.json"
)
DEFAULT_COMMAND = (
    "OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONPATH=src "
    "/usr/bin/python3 experiments/leaky_floquet_transfer.py"
)

# The orbit validators check their own complete source manifests.  The new
# transfer record additionally binds the theorem carrier and every file
# introduced specifically for this result.
SOURCE_MANIFEST = (
    SOURCE_RELATIVE_PATH,
    GENERATOR_RELATIVE_PATH,
    NOTE_RELATIVE_PATH,
    "src/canard_control/rfde_floquet_transfer.py",
)
EVIDENCE_PATHS = (
    INNER_RESULT_RELATIVE_PATH,
    OUTER_RESULT_RELATIVE_PATH,
)

ARITHMETIC_SCOPE = (
    "The Fredholm-to-monodromy implication and moving-delay Jordan identity "
    "are exact functional-analytic statements. Numerical endpoints are "
    "160-bit MPFR-directed bounds around the exact binary64 Fourier "
    "polynomials and their already validated Wiener correction balls. "
    "The source orbit validators check their own body digests and source "
    "manifests. No directed outer Bloch-arc cover, Riesz count, or unstable "
    "Floquet index is inferred."
)

CLAIM_STATUS = {
    "inner_periodic_rfde_orbit_source_validated": True,
    "outer_periodic_rfde_orbit_source_validated": True,
    "fredholm_to_history_monodromy_transfer_proved": True,
    "inner_neutral_multiplier_algebraically_simple_validated": True,
    "outer_neutral_multiplier_algebraically_simple_validated": True,
    "inner_punctured_local_unit_circle_exclusion_validated": True,
    "outer_punctured_local_unit_circle_exclusion_validated": True,
    "inner_full_nontranslation_unit_circle_exclusion_validated": False,
    "outer_full_nontranslation_unit_circle_exclusion_validated": False,
    "inner_unstable_multiplier_count_validated": False,
    "outer_unstable_multiplier_count_validated": False,
    "inner_saddle_floquet_index_validated": False,
    "outer_attracting_floquet_index_validated": False,
}

# Filled after the first deterministic artifact build.  The canonical body
# excludes the manifest, so registering this digest creates no hash cycle.
EXPECTED_ARTIFACT_SHA256: str | None = (
    "baf5eef52bc67a14224a4a228ded74aced7315f9f0b92ee6be7562e91d917089"
)


@dataclass(frozen=True)
class LeakyPeriodColumnTransferAudit:
    """Exact structural statements used in the neutral transfer."""

    autonomous_retarded_rfde: bool
    physical_delays_fixed_when_period_varies: bool
    normalized_period_column: str
    recovery_period_column: str
    moving_delay_terms_present: bool
    jordan_identity: str
    bvp_fredholm_index_zero: bool
    history_regularization_bridge_registered: bool
    algebraic_simplicity_transfer_proved: bool


@dataclass(frozen=True)
class LeakyOrbitFloquetEvidence:
    """Validated source-orbit data admitted to the transfer theorem."""

    branch: str
    source_result: str
    source_result_sha256: str
    source_artifact_sha256: str
    candidate_fingerprint: str
    node_count: int
    correction_radius: str
    bordered_inverse_norm_upper: str
    periodic_rfde_orbit_validated: bool
    phase_bordered_rfde_inverse_validated: bool
    moving_delay_period_column_validated: bool
    recovery_leak_period_column_validated: bool


@dataclass(frozen=True)
class LeakyBranchFloquetTransferCertificate:
    """One branch's neutral multiplier and local-arc certificate."""

    branch: str
    precision_bits: int
    source_result: str
    source_result_sha256: str
    source_artifact_sha256: str
    candidate_fingerprint: str
    node_count: int
    correction_radius: str
    bordered_inverse_norm_upper: str
    nonconstant_fourier_mode_lower: str
    minimum_period_lower: str
    maximum_delay_upper: str
    monodromy_compact: bool
    periodic_bvp_fredholm_index_zero: bool
    regularity_bridge_to_history_monodromy: bool
    exact_moving_delay_jordan_identity: bool
    translation_multiplier_present: bool
    translation_kernel_geometrically_simple_validated: bool
    translation_jordan_vector_excluded: bool
    neutral_multiplier_algebraically_simple_validated: bool
    delayed_variational_coefficient_norm_upper: str
    orbit_tangent_norm_upper: str
    recovery_input_column_upper: str
    state_field_lipschitz_upper: str
    bloch_first_order_coefficient_upper: str
    bloch_second_order_coefficient_upper: str
    first_local_phase_threshold_lower: str
    second_local_phase_threshold_lower: str
    local_phase_radius_lower: str
    punctured_local_unit_circle_exclusion_validated: bool
    remaining_positive_arc_lower: str
    remaining_positive_arc_upper: str
    remaining_positive_arc_directed_exclusion_validated: bool
    full_nontranslation_unit_circle_exclusion_validated: bool
    unstable_multiplier_count_validated: bool
    attracting_or_saddle_floquet_index_validated: bool
    remaining_gate: str


def _sha256_path(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def canonical_sha256(value: object) -> str:
    """Hash one JSON value using the artifact's canonical encoding."""

    encoded = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    return sha256(encoded).hexdigest()


def build_leaky_period_column_transfer_audit(
) -> LeakyPeriodColumnTransferAudit:
    """Return the exact RFDE theorem seam, independently of numerics."""

    return LeakyPeriodColumnTransferAudit(
        autonomous_retarded_rfde=True,
        physical_delays_fixed_when_period_varies=True,
        normalized_period_column=(
            "D_T Phi(X,T)=-b, b=f+sum_j (tau_j/T) "
            "A_j S_{tau_j/T} X'"
        ),
        recovery_period_column=(
            "(D_T Phi)_w=-epsilon*(v-a-w)"
        ),
        moving_delay_terms_present=True,
        jordan_identity="L(theta X')=T*b",
        bvp_fredholm_index_zero=True,
        history_regularization_bridge_registered=True,
        algebraic_simplicity_transfer_proved=True,
    )


def _evidence_from_payload(
    branch: str,
    relative_path: str,
    payload: Mapping[str, Any],
    orbit: PeriodicOrbitCandidate,
) -> LeakyOrbitFloquetEvidence:
    artifact = payload.get("artifact")
    if not isinstance(artifact, Mapping):
        raise ValueError("source artifact is missing")
    if branch == "inner_saddle_candidate":
        wrapper = artifact.get("directed_radii_prototype")
    elif branch == "outer_pulse":
        wrapper = artifact.get("directed_radii_certificate")
    else:
        raise ValueError("unknown leaky branch")
    if not isinstance(wrapper, Mapping):
        raise ValueError("source directed-radii wrapper is missing")
    validation = wrapper.get("validation")
    if not isinstance(validation, Mapping):
        raise ValueError("source directed-radii validation is missing")
    correction = validation.get("correction")
    if not isinstance(correction, Mapping):
        raise ValueError("source correction certificate is missing")
    radius = correction.get("chosen_radius")
    inverse = correction.get("bordered_inverse_norm_upper")
    if not isinstance(radius, str) or not isinstance(inverse, str):
        raise ValueError("source correction radius or inverse bound is missing")
    if validation.get("periodic_rfde_orbit_validated") is not True:
        raise ValueError("source periodic RFDE orbit is not validated")
    if validation.get("phase_bordered_rfde_inverse_validated") is not True:
        raise ValueError("source phase-bordered inverse is not validated")
    floquet = validation.get("floquet")
    if not isinstance(floquet, Mapping):
        raise ValueError("source Floquet boundary is missing")
    # The upstream artifact must not already smuggle in the conclusion that
    # this downstream theorem is proving.
    for name in (
        "fredholm_to_monodromy_multiplicity_transfer_registered",
        "neutral_multiplier_algebraically_simple_validated",
        "nontranslation_unit_circle_exclusion_validated",
        "unstable_multiplier_count_validated",
        "attracting_or_saddle_index_validated",
    ):
        if floquet.get(name) is not False:
            raise ValueError(f"source Floquet boundary {name} changed")
    return LeakyOrbitFloquetEvidence(
        branch=branch,
        source_result=relative_path,
        source_result_sha256="",  # completed by the repository loader
        source_artifact_sha256=canonical_sha256(artifact),
        candidate_fingerprint=periodic_orbit_candidate_fingerprint(orbit),
        node_count=len(orbit.state),
        correction_radius=radius,
        bordered_inverse_norm_upper=inverse,
        periodic_rfde_orbit_validated=True,
        phase_bordered_rfde_inverse_validated=True,
        # Both formulas are exact source-level identities in the validated
        # leaky residual/Jacobian, not floating diagnostic flags.
        moving_delay_period_column_validated=True,
        recovery_leak_period_column_validated=True,
    )


def load_validated_leaky_orbit_evidence(
    repository: Path,
    branch: str,
) -> tuple[PeriodicOrbitCandidate, LeakyOrbitFloquetEvidence]:
    """Validate one source artifact and return its theorem-bearing data."""

    repository = repository.resolve()
    if branch == "inner_saddle_candidate":
        relative = INNER_RESULT_RELATIVE_PATH
        payload = json.loads(
            (repository / relative).read_text(encoding="utf-8")
        )
        orbit = validate_leaky_periodic_branch_artifact(
            payload, repository, replay_directed=False
        )
    elif branch == "outer_pulse":
        relative = OUTER_RESULT_RELATIVE_PATH
        payload = json.loads(
            (repository / relative).read_text(encoding="utf-8")
        )
        orbit = validate_outer_high_resolution_artifact(
            payload, repository, replay_directed=False
        )
    else:
        raise ValueError("branch must be inner_saddle_candidate or outer_pulse")
    evidence = _evidence_from_payload(branch, relative, payload, orbit)
    evidence = LeakyOrbitFloquetEvidence(
        **{
            **asdict(evidence),
            "source_result_sha256": _sha256_path(repository / relative),
        }
    )
    return orbit, evidence


def _positive_lower_quotient(
    numerator: gmpy2.mpfr,
    denominator: gmpy2.mpfr,
    precision: int,
) -> gmpy2.mpfr:
    if numerator <= 0 or denominator <= 0:
        raise ValueError("directed quotient requires positive endpoints")
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        return numerator / denominator


def validate_leaky_branch_floquet_transfer(
    orbit: PeriodicOrbitCandidate,
    evidence: LeakyOrbitFloquetEvidence,
    *,
    precision: int = 160,
) -> LeakyBranchFloquetTransferCertificate:
    """Prove neutral simplicity and a punctured local arc for one branch."""

    if evidence.branch not in {"inner_saddle_candidate", "outer_pulse"}:
        raise ValueError("unknown leaky branch")
    if not evidence.periodic_rfde_orbit_validated:
        raise ValueError("a validated periodic RFDE orbit is required")
    if not evidence.phase_bordered_rfde_inverse_validated:
        raise ValueError("a validated phase-bordered RFDE inverse is required")
    if not evidence.moving_delay_period_column_validated:
        raise ValueError("the exact moving-delay period column is required")
    if not evidence.recovery_leak_period_column_validated:
        raise ValueError("the exact recovery-leak period column is required")
    if evidence.candidate_fingerprint != periodic_orbit_candidate_fingerprint(
        orbit
    ):
        raise ValueError("the Floquet evidence belongs to a different orbit")
    if evidence.node_count != len(orbit.state):
        raise ValueError("the Floquet evidence has the wrong node count")
    if orbit.parameters.kappa_1 < 0 or orbit.parameters.kappa_3 < 0:
        raise ValueError("the coefficient bound requires nonnegative gains")

    radius = DirectedInterval.from_decimal(
        evidence.correction_radius, precision
    ).upper
    inverse_norm = DirectedInterval.from_decimal(
        evidence.bordered_inverse_norm_upper, precision
    ).upper
    if radius <= 0 or inverse_norm <= 0:
        raise ValueError("the correction radius and inverse bound must be positive")

    base = _build_leaky_base_sequences(orbit, precision)
    parameters = base.parameters
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        minimum_period = base.period.lower - radius
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        maximum_period = base.period.upper + radius
    if minimum_period <= 0:
        raise ValueError("the correction ball crosses a nonpositive period")
    maximum_delay = max(
        parameters["tau_0"].upper,
        parameters["tau_1"].upper,
    )
    if minimum_period <= maximum_delay:
        raise ValueError(
            "this certificate requires the one-period monodromy to be compact"
        )
    nonconstant_lower = _nonconstant_mode_lower(base, radius)
    if nonconstant_lower <= 0:
        raise ValueError("the correction ball does not prove a nonconstant orbit")

    voltage_bar = _sequence_box_norm_upper(base.voltage, precision)
    centered_bar = _sequence_box_norm_upper(
        base.centered_voltage, precision
    )
    delayed_field_derivative_bar = _sequence_box_norm_upper(
        base.delayed_field_derivative, precision
    )
    tangent_bar = _state_sequence_norm_upper(base, precision)
    residual_bar = _residual_sequence_norm_upper(base, precision)

    epsilon = parameters["epsilon"].upper
    kappa_1 = parameters["kappa_1"].upper
    kappa_3 = parameters["kappa_3"].upper
    one = gmpy2.mpfr(1, precision)
    two = gmpy2.mpfr(2, precision)
    three = gmpy2.mpfr(3, precision)
    sqrt_two = DirectedInterval.from_decimal(2, precision).sqrt().upper

    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        voltage = voltage_bar + radius
        centered = centered_bar + radius
        delayed_variational = (
            epsilon * kappa_1 / two
            + three * epsilon * kappa_3 * centered * centered / two
        )

        voltage_cubic_slope = (
            voltage * voltage
            + voltage * voltage_bar
            + voltage_bar * voltage_bar
        ) / three
        centered_cubic_slope = (
            centered * centered
            + centered * centered_bar
            + centered_bar * centered_bar
        )
        fast_voltage_lipschitz = (
            one
            + epsilon * kappa_1
            + voltage_cubic_slope
            + epsilon * kappa_3 * centered_cubic_slope
        )
        # This is the only local-arc coefficient change caused by the
        # recovery leak.  The recovery input column is 1+epsilon, not 1.
        recovery_input_column = one + epsilon
        state_field_lipschitz = max(
            fast_voltage_lipschitz + epsilon,
            recovery_input_column,
        )
        delayed_field_lipschitz = (
            epsilon * kappa_1 / two
            + epsilon * kappa_3 * centered_cubic_slope / two
        )

    delay_field_changes: list[gmpy2.mpfr] = []
    for key in ("tau_0", "tau_1"):
        tau = parameters[key].upper
        with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
            delay_fraction_change = (
                tau * radius / (minimum_period * base.period.lower)
            )
            delay_field_changes.append(
                sqrt_two * delayed_field_lipschitz * radius
                + sqrt_two
                * delay_fraction_change
                * delayed_field_derivative_bar
            )

    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        field_change = (
            state_field_lipschitz * radius
            + upward_sum(delay_field_changes, precision)
        )
        candidate_field = (
            tangent_bar + residual_bar
        ) / base.period.lower
        tangent_change = (
            maximum_period * field_change
            + radius * candidate_field
            + residual_bar
        )
        tangent_upper = tangent_bar + tangent_change

        delay_sum = (
            parameters["tau_0"].upper + parameters["tau_1"].upper
        )
        first_order = one + two * delay_sum * delayed_variational
        alpha_square_sum = (
            (parameters["tau_0"].upper / minimum_period) ** 2
            + (parameters["tau_1"].upper / minimum_period) ** 2
        )
        second_order = (
            maximum_period
            * delayed_variational
            * alpha_square_sum
            * tangent_upper
        )
        first_denominator = inverse_norm * first_order
        second_denominator = inverse_norm * second_order

    first_threshold = _positive_lower_quotient(
        one, first_denominator, precision
    )
    second_threshold = _positive_lower_quotient(
        minimum_period, second_denominator, precision
    )
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        local_radius = min(first_threshold, second_threshold) / two
    if local_radius <= 0:
        raise ArithmeticError("the directed local Floquet radius vanished")

    audit = build_leaky_period_column_transfer_audit()
    if not all(
        (
            audit.autonomous_retarded_rfde,
            audit.physical_delays_fixed_when_period_varies,
            audit.moving_delay_terms_present,
            audit.bvp_fredholm_index_zero,
            audit.history_regularization_bridge_registered,
            audit.algebraic_simplicity_transfer_proved,
        )
    ):
        raise ValueError("the exact Floquet transfer audit is incomplete")

    return LeakyBranchFloquetTransferCertificate(
        branch=evidence.branch,
        precision_bits=precision,
        source_result=evidence.source_result,
        source_result_sha256=evidence.source_result_sha256,
        source_artifact_sha256=evidence.source_artifact_sha256,
        candidate_fingerprint=evidence.candidate_fingerprint,
        node_count=evidence.node_count,
        correction_radius=evidence.correction_radius,
        bordered_inverse_norm_upper=evidence.bordered_inverse_norm_upper,
        nonconstant_fourier_mode_lower=decimal_lower(nonconstant_lower),
        minimum_period_lower=decimal_lower(minimum_period),
        maximum_delay_upper=decimal_upper(maximum_delay),
        monodromy_compact=True,
        periodic_bvp_fredholm_index_zero=True,
        regularity_bridge_to_history_monodromy=True,
        exact_moving_delay_jordan_identity=True,
        translation_multiplier_present=True,
        translation_kernel_geometrically_simple_validated=True,
        translation_jordan_vector_excluded=True,
        neutral_multiplier_algebraically_simple_validated=True,
        delayed_variational_coefficient_norm_upper=decimal_upper(
            delayed_variational
        ),
        orbit_tangent_norm_upper=decimal_upper(tangent_upper),
        recovery_input_column_upper=decimal_upper(recovery_input_column),
        state_field_lipschitz_upper=decimal_upper(state_field_lipschitz),
        bloch_first_order_coefficient_upper=decimal_upper(first_order),
        bloch_second_order_coefficient_upper=decimal_upper(second_order),
        first_local_phase_threshold_lower=decimal_lower(first_threshold),
        second_local_phase_threshold_lower=decimal_lower(second_threshold),
        local_phase_radius_lower=decimal_lower(local_radius),
        punctured_local_unit_circle_exclusion_validated=True,
        remaining_positive_arc_lower=decimal_lower(local_radius),
        remaining_positive_arc_upper=decimal_upper(
            pi_interval(precision).upper
        ),
        remaining_positive_arc_directed_exclusion_validated=False,
        full_nontranslation_unit_circle_exclusion_validated=False,
        unstable_multiplier_count_validated=False,
        attracting_or_saddle_floquet_index_validated=False,
        remaining_gate=(
            "Construct source-bound directed full-complex Bloch cells on "
            "[delta,pi], then a deflated Riesz or winding count on the "
            "exterior annulus."
        ),
    )


def build_leaky_floquet_transfer_artifact(
    repository: Path,
    *,
    precision: int = 160,
) -> dict[str, object]:
    """Build the deterministic theorem body and its source manifest."""

    repository = repository.resolve()
    certificates: dict[str, dict[str, object]] = {}
    for branch in ("inner_saddle_candidate", "outer_pulse"):
        orbit, evidence = load_validated_leaky_orbit_evidence(
            repository, branch
        )
        certificate = validate_leaky_branch_floquet_transfer(
            orbit, evidence, precision=precision
        )
        certificates[branch] = asdict(certificate)
    artifact: dict[str, object] = {
        "schema_id": SCHEMA_ID,
        "theorem_scope": asdict(build_leaky_period_column_transfer_audit()),
        "branches": certificates,
        "claim_status": CLAIM_STATUS,
    }
    manifest = {
        "schema_id": SCHEMA_ID,
        "result": RESULT_RELATIVE_PATH,
        "default_command": DEFAULT_COMMAND,
        "arithmetic_scope": ARITHMETIC_SCOPE,
        "artifact_sha256": canonical_sha256(artifact),
        "source_sha256": {
            relative: _sha256_path(repository / relative)
            for relative in SOURCE_MANIFEST
        },
        "evidence_sha256": {
            relative: _sha256_path(repository / relative)
            for relative in EVIDENCE_PATHS
        },
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "gmpy2": gmpy2.__version__,
        },
    }
    return {"artifact": artifact, "manifest": manifest}


def _validate_branch_payload(
    branch: str,
    payload: object,
) -> None:
    if not isinstance(payload, Mapping):
        raise ValueError("branch certificate must be a mapping")
    if set(payload) != {field.name for field in fields(
        LeakyBranchFloquetTransferCertificate
    )}:
        raise ValueError("branch certificate schema changed")
    if payload.get("branch") != branch:
        raise ValueError("branch certificate label changed")
    true_fields = (
        "monodromy_compact",
        "periodic_bvp_fredholm_index_zero",
        "regularity_bridge_to_history_monodromy",
        "exact_moving_delay_jordan_identity",
        "translation_multiplier_present",
        "translation_kernel_geometrically_simple_validated",
        "translation_jordan_vector_excluded",
        "neutral_multiplier_algebraically_simple_validated",
        "punctured_local_unit_circle_exclusion_validated",
    )
    false_fields = (
        "remaining_positive_arc_directed_exclusion_validated",
        "full_nontranslation_unit_circle_exclusion_validated",
        "unstable_multiplier_count_validated",
        "attracting_or_saddle_floquet_index_validated",
    )
    if any(payload.get(name) is not True for name in true_fields):
        raise ValueError("a proved branch transfer flag was removed")
    if any(payload.get(name) is not False for name in false_fields):
        raise ValueError("an open branch Floquet flag was promoted")
    for name in (
        "correction_radius",
        "bordered_inverse_norm_upper",
        "nonconstant_fourier_mode_lower",
        "minimum_period_lower",
        "maximum_delay_upper",
        "delayed_variational_coefficient_norm_upper",
        "orbit_tangent_norm_upper",
        "recovery_input_column_upper",
        "state_field_lipschitz_upper",
        "bloch_first_order_coefficient_upper",
        "bloch_second_order_coefficient_upper",
        "first_local_phase_threshold_lower",
        "second_local_phase_threshold_lower",
        "local_phase_radius_lower",
        "remaining_positive_arc_lower",
        "remaining_positive_arc_upper",
    ):
        value = payload.get(name)
        if not isinstance(value, str):
            raise ValueError(f"branch decimal {name} is missing")
        try:
            number = gmpy2.mpq(value)
        except ValueError as error:
            raise ValueError(f"branch decimal {name} is invalid") from error
        if number <= 0:
            raise ValueError(f"branch decimal {name} is not positive")
    if gmpy2.mpq(payload["minimum_period_lower"]) <= gmpy2.mpq(
        payload["maximum_delay_upper"]
    ):
        raise ValueError("the monodromy compactness inequality failed")
    if gmpy2.mpq(payload["local_phase_radius_lower"]) > min(
        gmpy2.mpq(payload["first_local_phase_threshold_lower"]),
        gmpy2.mpq(payload["second_local_phase_threshold_lower"]),
    ) / 2:
        raise ValueError("the local phase radius exceeds its strict budget")
    if payload["remaining_positive_arc_lower"] != payload[
        "local_phase_radius_lower"
    ]:
        raise ValueError("the remaining arc does not start at the local radius")
    if gmpy2.mpq(payload["recovery_input_column_upper"]) <= 1:
        raise ValueError("the recovery leak was omitted from the column bound")


def validate_leaky_floquet_transfer_artifact(
    payload: Mapping[str, Any],
    repository: Path,
    *,
    recompute: bool = False,
) -> None:
    """Validate the tracked transfer artifact and optionally recompute it."""

    if not isinstance(payload, Mapping) or set(payload) != {
        "artifact",
        "manifest",
    }:
        raise ValueError("Floquet result must contain artifact and manifest")
    artifact = payload.get("artifact")
    manifest = payload.get("manifest")
    if not isinstance(artifact, Mapping) or not isinstance(manifest, Mapping):
        raise ValueError("Floquet artifact and manifest must be mappings")
    if set(artifact) != {
        "schema_id",
        "theorem_scope",
        "branches",
        "claim_status",
    }:
        raise ValueError("Floquet artifact schema changed")
    if artifact.get("schema_id") != SCHEMA_ID:
        raise ValueError("Floquet schema id changed")
    if artifact.get("claim_status") != CLAIM_STATUS:
        raise ValueError("Floquet claim ledger changed")
    if not isinstance(EXPECTED_ARTIFACT_SHA256, str):
        raise ValueError("Floquet artifact body is not source registered")
    body_digest = canonical_sha256(artifact)
    if body_digest != EXPECTED_ARTIFACT_SHA256:
        raise ValueError("Floquet artifact differs from its registered body")
    expected_audit = asdict(build_leaky_period_column_transfer_audit())
    if artifact.get("theorem_scope") != expected_audit:
        raise ValueError("Floquet theorem scope changed")
    branches = artifact.get("branches")
    if not isinstance(branches, Mapping) or set(branches) != {
        "inner_saddle_candidate",
        "outer_pulse",
    }:
        raise ValueError("Floquet branch set changed")
    for branch in ("inner_saddle_candidate", "outer_pulse"):
        _validate_branch_payload(branch, branches[branch])

    if set(manifest) != {
        "schema_id",
        "result",
        "default_command",
        "arithmetic_scope",
        "artifact_sha256",
        "source_sha256",
        "evidence_sha256",
        "environment",
    }:
        raise ValueError("Floquet manifest schema changed")
    if (
        manifest.get("schema_id") != SCHEMA_ID
        or manifest.get("result") != RESULT_RELATIVE_PATH
        or manifest.get("default_command") != DEFAULT_COMMAND
        or manifest.get("arithmetic_scope") != ARITHMETIC_SCOPE
        or manifest.get("artifact_sha256") != body_digest
    ):
        raise ValueError("Floquet manifest scalar changed")
    repository = repository.resolve()
    source_hashes = manifest.get("source_sha256")
    if not isinstance(source_hashes, Mapping) or set(source_hashes) != set(
        SOURCE_MANIFEST
    ):
        raise ValueError("Floquet source manifest changed")
    for relative in SOURCE_MANIFEST:
        if source_hashes.get(relative) != _sha256_path(repository / relative):
            raise ValueError(f"Floquet source hash changed for {relative}")
    evidence_hashes = manifest.get("evidence_sha256")
    if not isinstance(evidence_hashes, Mapping) or set(evidence_hashes) != set(
        EVIDENCE_PATHS
    ):
        raise ValueError("Floquet evidence manifest changed")
    for relative in EVIDENCE_PATHS:
        actual = _sha256_path(repository / relative)
        if evidence_hashes.get(relative) != actual:
            raise ValueError(f"Floquet evidence hash changed for {relative}")
    branch_evidence = {
        branches["inner_saddle_candidate"]["source_result"]:
            branches["inner_saddle_candidate"]["source_result_sha256"],
        branches["outer_pulse"]["source_result"]:
            branches["outer_pulse"]["source_result_sha256"],
    }
    if branch_evidence != dict(evidence_hashes):
        raise ValueError("branch certificates and evidence manifest disagree")
    expected_environment = {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "gmpy2": gmpy2.__version__,
    }
    if manifest.get("environment") != expected_environment:
        raise ValueError("Floquet environment record changed")

    if recompute:
        replay = build_leaky_floquet_transfer_artifact(repository)
        if replay["artifact"] != artifact:
            raise ValueError("Floquet directed replay changed")


__all__ = [
    "ARITHMETIC_SCOPE",
    "CLAIM_STATUS",
    "DEFAULT_COMMAND",
    "EVIDENCE_PATHS",
    "EXPECTED_ARTIFACT_SHA256",
    "GENERATOR_RELATIVE_PATH",
    "INNER_RESULT_RELATIVE_PATH",
    "LeakyBranchFloquetTransferCertificate",
    "LeakyOrbitFloquetEvidence",
    "LeakyPeriodColumnTransferAudit",
    "NOTE_RELATIVE_PATH",
    "OUTER_RESULT_RELATIVE_PATH",
    "RESULT_RELATIVE_PATH",
    "SCHEMA_ID",
    "SOURCE_MANIFEST",
    "SOURCE_RELATIVE_PATH",
    "build_leaky_floquet_transfer_artifact",
    "build_leaky_period_column_transfer_audit",
    "canonical_sha256",
    "load_validated_leaky_orbit_evidence",
    "validate_leaky_branch_floquet_transfer",
    "validate_leaky_floquet_transfer_artifact",
]
