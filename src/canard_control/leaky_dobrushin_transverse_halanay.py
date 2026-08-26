"""Dobrushin-uniform transverse decay for the leaky bistable RFDE.

The synchronous restriction of the finite network in the companion note is
the validated scalar leaky-recovery RFDE.  This module proves a genuinely
finite-network statement at the center parameters: every transverse
variational solution along the quiet equilibrium and along either validated
periodic branch decays at one explicit rate, uniformly in the number of
nodes and in every admitted balanced topology.

The result does not count the collective Floquet multipliers.  Consequently
it does not yet prove that the outer network cycle attracts or that the inner
network cycle has one unstable direction.  It proves that any such unstable
direction must be collective, and it proves local exponential stability of
the full-network quiet equilibrium because the scalar collective equilibrium
is already validated as exponentially stable.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from functools import lru_cache
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Mapping

import gmpy2

from canard_control.autonomous_leaky_recovery_bistable import (
    build_equilibrium_stability_certificate,
)
from canard_control.directed_interval import (
    DirectedInterval,
    complex_unit_interval,
    decimal_lower,
    decimal_upper,
    pi_interval,
)
from canard_control.fhn_periodic_directed_validation import directed_dft
from canard_control.leaky_floquet_transfer import (
    validate_leaky_floquet_transfer_artifact,
)
from canard_control.leaky_outer_high_resolution import (
    validate_outer_high_resolution_artifact,
)
from canard_control.leaky_periodic_branch_artifact import (
    validate_leaky_periodic_branch_artifact,
)
from canard_control.rfde_floquet_transfer import (
    periodic_orbit_candidate_fingerprint,
)


SCHEMA_ID = "leaky-dobrushin-transverse-halanay-v2"
MODEL_ID = "balanced-finite-network-leaky-recovery-two-delay-fhn"
SOURCE_RELATIVE_PATH = (
    "src/canard_control/leaky_dobrushin_transverse_halanay.py"
)
GENERATOR_RELATIVE_PATH = (
    "experiments/leaky_dobrushin_transverse_halanay.py"
)
NOTE_RELATIVE_PATH = "docs/leaky-dobrushin-transverse-halanay.md"
RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_dobrushin_transverse_halanay.json"
)
INNER_RESULT_RELATIVE_PATH = (
    "experiments/results/"
    "autonomous_leaky_recovery_inner_branch_artifact.json"
)
OUTER_RESULT_RELATIVE_PATH = (
    "experiments/results/"
    "autonomous_leaky_recovery_outer_high_resolution.json"
)
FLOQUET_RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_floquet_transfer.json"
)
TRACKED_FLOQUET_RESULT_SHA256 = (
    "5a3709ec792b29ed41533101245b13b3d35084ae508bdd1d420728200a5a5b16"
)
EQUILIBRIUM_SOURCE_RELATIVE_PATH = (
    "src/canard_control/autonomous_leaky_recovery_bistable.py"
)
DEFAULT_COMMAND = (
    "OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONPATH=src "
    "/usr/bin/python3 experiments/leaky_dobrushin_transverse_halanay.py"
)
ARITHMETIC_DESCRIPTION = (
    "160-bit MPFR outward-rounded Fourier phase samples, exact-orbit "
    "tangent interpolation and Halanay constants; exact analytic complex-"
    "diameter Dobrushin inequalities in unweighted and exponentially "
    "weighted retained-history norms"
)
SOURCE_MANIFEST = (
    SOURCE_RELATIVE_PATH,
    GENERATOR_RELATIVE_PATH,
    NOTE_RELATIVE_PATH,
    EQUILIBRIUM_SOURCE_RELATIVE_PATH,
)

PRECISION_BITS = 160
PHASE_SAMPLE_COUNT = 1024
DOBRUSHIN_GAP_LOWER = "0.5"
RECOVERY_WEIGHT = "3"
VOLTAGE_CENTERED_RADIUS = "2.5"
DECAY_RATE = "0.1"


def _sha256_path(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def canonical_sha256(value: Any) -> str:
    encoded = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("ascii")
    return sha256(encoded).hexdigest()


def _mapping(value: Any, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{name} must be a mapping")
    return value


def _correction_radius(
    payload: Mapping[str, Any], branch: str, precision: int
) -> DirectedInterval:
    artifact = _mapping(payload.get("artifact"), "source artifact")
    if branch == "inner_saddle_candidate":
        wrapper_name = "directed_radii_prototype"
    elif branch == "outer_pulse":
        wrapper_name = "directed_radii_certificate"
    else:
        raise ValueError("unknown leaky branch")
    wrapper = _mapping(artifact.get(wrapper_name), wrapper_name)
    validation = _mapping(wrapper.get("validation"), "source validation")
    correction = _mapping(validation.get("correction"), "source correction")
    radius = correction.get("chosen_radius")
    if not isinstance(radius, str):
        raise ValueError("source correction radius is missing")
    if validation.get("periodic_rfde_orbit_validated") is not True:
        raise ValueError("source periodic orbit is not validated")
    if validation.get("phase_bordered_rfde_inverse_validated") is not True:
        raise ValueError("source bordered inverse is not validated")
    result = DirectedInterval.from_decimal(radius, precision)
    if result.lower <= 0:
        raise ValueError("source correction radius must be positive")
    return result


@dataclass(frozen=True)
class LeakyBranchVoltageStrip:
    """Directed pointwise strip for one exact scalar periodic orbit."""

    branch: str
    source_result: str
    source_result_sha256: str
    source_artifact_sha256: str
    candidate_fingerprint: str
    node_count: int
    correction_radius: str
    phase_sample_count: int
    exact_orbit_tangent_norm_upper: str
    between_sample_change_upper: str
    candidate_centered_voltage_abs_upper: str
    exact_centered_voltage_abs_upper: str
    declared_centered_voltage_radius: str
    strict_strip_margin_lower: str
    minimum_period_lower: str
    unweighted_history_monodromy_norm_upper: str
    exponentially_weighted_history_monodromy_norm_upper: str
    transverse_multiplier_modulus_upper: str
    exact_periodic_orbit_strip_validated: bool


@dataclass(frozen=True)
class LeakyDobrushinBounds:
    """Directed constants in the weighted oscillation Halanay estimate."""

    precision_bits: int
    dobrushin_gap_lower: str
    recovery_weight: str
    epsilon: str
    kappa_1: str
    kappa_3: str
    centered_voltage_radius: str
    current_voltage_coefficient_upper: str
    delayed_total_gain_upper: str
    maximum_delay_upper: str
    voltage_local_decay_lower: str
    recovery_local_decay_lower: str
    local_decay_lower: str
    zero_rate_margin_lower: str
    exponential_rate: str
    delay_exponential_upper: str
    rate_residual_lower: str


@dataclass(frozen=True)
class LeakyDobrushinTransverseCertificate:
    """The theorem endpoints and a strict scope ledger."""

    schema_id: str
    model_id: str
    topology_class: str
    phase_space_norm: str
    quiet_centered_voltage_abs_upper: str
    inner: LeakyBranchVoltageStrip
    outer: LeakyBranchVoltageStrip
    bounds: LeakyDobrushinBounds
    scalar_quiet_equilibrium_stability_source_validated: bool
    scalar_inner_periodic_orbit_source_validated: bool
    scalar_outer_periodic_orbit_source_validated: bool
    synchronous_restriction_is_exact_scalar_model: bool
    collective_transverse_splitting_invariant_proved: bool
    complexified_transverse_diameter_estimate_proved: bool
    dobrushin_oscillation_dini_estimate_proved: bool
    balanced_half_mass_delay_bound_proved: bool
    exponentially_weighted_history_contraction_proved: bool
    arbitrary_finite_network_size_covered: bool
    arbitrary_admitted_balanced_topology_covered: bool
    quiet_transverse_exponential_decay_validated: bool
    inner_transverse_exponential_decay_validated: bool
    outer_transverse_exponential_decay_validated: bool
    full_network_quiet_local_exponential_stability_proved: bool
    all_noncollective_periodic_multipliers_inside_rate_disk_proved: bool
    inner_full_network_one_unstable_multiplier_validated: bool
    outer_full_network_orbital_attraction_validated: bool
    uniform_nonlinear_basin_radius_validated: bool
    physical_pulse_onset_lift_validated: bool
    general_closing_gap_networks_covered: bool


def _evaluate_real_sequence(
    sequence: Mapping[int, Any], phase: DirectedInterval
) -> DirectedInterval:
    precision = phase.precision
    result = DirectedInterval.from_decimal(0, precision)
    two_pi = pi_interval(precision) * 2
    for mode, coefficient in sequence.items():
        result += (coefficient * complex_unit_interval(two_pi * mode * phase)).real
    return result


def _pointwise_centered_voltage_upper(
    orbit: Any,
    correction_radius: DirectedInterval,
    tangent_upper: DirectedInterval,
    *,
    precision: int,
    sample_count: int,
) -> tuple[gmpy2.mpfr, gmpy2.mpfr, gmpy2.mpfr, gmpy2.mpfr]:
    """Bound ``|V-1|`` by directed samples and an exact tangent norm."""

    if sample_count < 1024:
        raise ValueError("the phase sample must contain at least 1024 points")
    coefficients = directed_dft(orbit.state[:, 0], precision)
    denominator = DirectedInterval.from_decimal(sample_count, precision)
    one = DirectedInterval.from_decimal(1, precision)
    candidate_upper = gmpy2.mpfr(0, precision)
    for index in range(sample_count):
        phase = DirectedInterval.from_decimal(index, precision) / denominator
        centered = _evaluate_real_sequence(coefficients, phase) - one
        candidate_upper = max(candidate_upper, centered.upper_abs())
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        between_sample = tangent_upper.upper / (2 * sample_count)
        exact_upper = (
            candidate_upper + correction_radius.upper + between_sample
        )
    radius = DirectedInterval.from_decimal(VOLTAGE_CENTERED_RADIUS, precision)
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        margin = radius.lower - exact_upper
    if margin <= 0:
        raise ArithmeticError("the exact periodic orbit left the declared strip")
    return candidate_upper, between_sample, exact_upper, margin


@lru_cache(maxsize=2)
def _validated_floquet_payload(repository: Path) -> Mapping[str, Any]:
    """Load and fully validate the tangent-bound parent artifact once."""

    path = repository / FLOQUET_RESULT_RELATIVE_PATH
    raw = path.read_bytes()
    if sha256(raw).hexdigest() != TRACKED_FLOQUET_RESULT_SHA256:
        raise ValueError("the tracked Floquet transfer result changed")
    payload = _mapping(json.loads(raw), "Floquet result")
    validate_leaky_floquet_transfer_artifact(
        payload, repository, recompute=False
    )
    return payload


def _load_branch_strip(
    repository: Path,
    branch: str,
    *,
    precision: int,
    sample_count: int,
) -> LeakyBranchVoltageStrip:
    if branch == "inner_saddle_candidate":
        relative = INNER_RESULT_RELATIVE_PATH
        validator = validate_leaky_periodic_branch_artifact
    elif branch == "outer_pulse":
        relative = OUTER_RESULT_RELATIVE_PATH
        validator = validate_outer_high_resolution_artifact
    else:
        raise ValueError("unknown leaky branch")
    path = repository / relative
    raw = path.read_bytes()
    payload = _mapping(json.loads(raw), "source result")
    orbit = validator(payload, repository, replay_directed=False)
    correction = _correction_radius(payload, branch, precision)
    floquet_payload = _validated_floquet_payload(repository)
    floquet_artifact = _mapping(
        floquet_payload.get("artifact"), "Floquet artifact"
    )
    floquet_branches = _mapping(
        floquet_artifact.get("branches"), "Floquet branches"
    )
    floquet_branch = _mapping(
        floquet_branches.get(branch), "Floquet branch"
    )
    tangent_text = floquet_branch.get("orbit_tangent_norm_upper")
    if not isinstance(tangent_text, str):
        raise ValueError("the source exact-orbit tangent bound is missing")
    if floquet_branch.get("source_result") != relative:
        raise ValueError("the Floquet branch points to another source result")
    if floquet_branch.get("source_result_sha256") != sha256(raw).hexdigest():
        raise ValueError("the Floquet branch source digest changed")
    if floquet_branch.get(
        "candidate_fingerprint"
    ) != periodic_orbit_candidate_fingerprint(orbit):
        raise ValueError("the Floquet tangent bound belongs to another orbit")
    floquet_radius_text = floquet_branch.get("correction_radius")
    if not isinstance(floquet_radius_text, str):
        raise ValueError("the Floquet correction radius is missing")
    floquet_radius = DirectedInterval.from_decimal(
        floquet_radius_text, precision
    )
    if (
        floquet_radius.lower != correction.lower
        or floquet_radius.upper != correction.upper
    ):
        raise ValueError("the Floquet and orbit correction radii differ")
    tangent = DirectedInterval.from_decimal(tangent_text, precision)
    (
        candidate_upper,
        between_sample,
        exact_upper,
        margin,
    ) = _pointwise_centered_voltage_upper(
        orbit,
        correction,
        tangent,
        precision=precision,
        sample_count=sample_count,
    )
    artifact = _mapping(payload.get("artifact"), "source artifact")
    period = DirectedInterval.from_float(orbit.period, precision) - correction
    maximum_delay = (
        DirectedInterval.from_decimal(5, precision)
        * DirectedInterval.from_decimal(5, precision).sqrt()
    )
    rate = DirectedInterval.from_decimal(DECAY_RATE, precision)
    if period.lower <= maximum_delay.upper:
        raise ValueError("the exact period is not longer than the history")
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        unweighted_history_upper = gmpy2.exp(
            -rate.lower * (period.lower - maximum_delay.upper)
        )
        weighted_history_upper = gmpy2.exp(-rate.lower * period.lower)
    return LeakyBranchVoltageStrip(
        branch=branch,
        source_result=relative,
        source_result_sha256=sha256(raw).hexdigest(),
        source_artifact_sha256=canonical_sha256(artifact),
        candidate_fingerprint=periodic_orbit_candidate_fingerprint(orbit),
        node_count=len(orbit.state),
        correction_radius=decimal_upper(correction.upper),
        phase_sample_count=sample_count,
        exact_orbit_tangent_norm_upper=decimal_upper(tangent.upper),
        between_sample_change_upper=decimal_upper(between_sample),
        candidate_centered_voltage_abs_upper=decimal_upper(candidate_upper),
        exact_centered_voltage_abs_upper=decimal_upper(exact_upper),
        declared_centered_voltage_radius=VOLTAGE_CENTERED_RADIUS,
        strict_strip_margin_lower=decimal_lower(margin),
        minimum_period_lower=decimal_lower(period.lower),
        unweighted_history_monodromy_norm_upper=decimal_upper(
            unweighted_history_upper
        ),
        exponentially_weighted_history_monodromy_norm_upper=decimal_upper(
            weighted_history_upper
        ),
        transverse_multiplier_modulus_upper=decimal_upper(
            weighted_history_upper
        ),
        exact_periodic_orbit_strip_validated=True,
    )


def directed_leaky_dobrushin_bounds(
    *, precision: int = PRECISION_BITS
) -> LeakyDobrushinBounds:
    """Compute the strict center-parameter Halanay constants."""

    one = DirectedInterval.from_decimal(1, precision)
    two = DirectedInterval.from_decimal(2, precision)
    three = DirectedInterval.from_decimal(3, precision)
    five = DirectedInterval.from_decimal(5, precision)
    epsilon = one / five
    kappa_1 = one / DirectedInterval.from_decimal(250, precision)
    kappa_3 = one / DirectedInterval.from_decimal(200, precision)
    gap = DirectedInterval.from_decimal(DOBRUSHIN_GAP_LOWER, precision)
    weight = DirectedInterval.from_decimal(RECOVERY_WEIGHT, precision)
    voltage_radius = DirectedInterval.from_decimal(
        VOLTAGE_CENTERED_RADIUS, precision
    )
    rate = DirectedInterval.from_decimal(DECAY_RATE, precision)
    current = one - epsilon * kappa_1
    delayed = epsilon * (
        kappa_1 + three * kappa_3 * voltage_radius * voltage_radius
    )
    maximum_delay = five * five.sqrt()
    voltage_decay = three * gap - current - one / weight
    recovery_decay = two * gap + epsilon - weight * epsilon
    local_decay = DirectedInterval.from_bounds(
        min(voltage_decay.lower, recovery_decay.lower),
        min(voltage_decay.upper, recovery_decay.upper),
        precision,
    )
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        zero_margin = local_decay.lower - delayed.upper
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        exponential = gmpy2.exp(rate.upper * maximum_delay.upper)
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        rate_residual = (
            local_decay.lower
            - rate.upper
            - delayed.upper * exponential
        )
    if zero_margin <= 0 or rate_residual <= 0:
        raise ArithmeticError("the leaky Dobrushin Halanay inequality failed")
    return LeakyDobrushinBounds(
        precision_bits=precision,
        dobrushin_gap_lower=DOBRUSHIN_GAP_LOWER,
        recovery_weight=RECOVERY_WEIGHT,
        epsilon=decimal_upper(epsilon.upper),
        kappa_1=decimal_upper(kappa_1.upper),
        kappa_3=decimal_upper(kappa_3.upper),
        centered_voltage_radius=VOLTAGE_CENTERED_RADIUS,
        current_voltage_coefficient_upper=decimal_upper(current.upper),
        delayed_total_gain_upper=decimal_upper(delayed.upper),
        maximum_delay_upper=decimal_upper(maximum_delay.upper),
        voltage_local_decay_lower=decimal_lower(voltage_decay.lower),
        recovery_local_decay_lower=decimal_lower(recovery_decay.lower),
        local_decay_lower=decimal_lower(local_decay.lower),
        zero_rate_margin_lower=decimal_lower(zero_margin),
        exponential_rate=DECAY_RATE,
        delay_exponential_upper=decimal_upper(exponential),
        rate_residual_lower=decimal_lower(rate_residual),
    )


def _validate_certificate_semantics(
    certificate: LeakyDobrushinTransverseCertificate,
) -> None:
    """Enforce the proved/open boundary independently of JSON replay."""

    proved = (
        certificate.synchronous_restriction_is_exact_scalar_model,
        certificate.collective_transverse_splitting_invariant_proved,
        certificate.complexified_transverse_diameter_estimate_proved,
        certificate.dobrushin_oscillation_dini_estimate_proved,
        certificate.balanced_half_mass_delay_bound_proved,
        certificate.exponentially_weighted_history_contraction_proved,
        certificate.full_network_quiet_local_exponential_stability_proved,
        certificate.all_noncollective_periodic_multipliers_inside_rate_disk_proved,
    )
    if not all(proved):
        raise ValueError("a proved Dobrushin/Halanay gate was removed")
    open_gates = (
        certificate.inner_full_network_one_unstable_multiplier_validated,
        certificate.outer_full_network_orbital_attraction_validated,
        certificate.uniform_nonlinear_basin_radius_validated,
        certificate.physical_pulse_onset_lift_validated,
        certificate.general_closing_gap_networks_covered,
    )
    if any(open_gates):
        raise ValueError("an open collective, basin, or onset gate was promoted")
    maximum_delay = gmpy2.mpq(certificate.bounds.maximum_delay_upper)
    for branch in (certificate.inner, certificate.outer):
        period = gmpy2.mpq(branch.minimum_period_lower)
        unweighted = gmpy2.mpq(
            branch.unweighted_history_monodromy_norm_upper
        )
        weighted = gmpy2.mpq(
            branch.exponentially_weighted_history_monodromy_norm_upper
        )
        multiplier = gmpy2.mpq(branch.transverse_multiplier_modulus_upper)
        if period <= maximum_delay:
            raise ValueError("the exact period is not longer than the history")
        if not 0 < weighted < unweighted < 1:
            raise ValueError("the two history-norm contractions are unordered")
        if multiplier != weighted:
            raise ValueError("the multiplier disk is not the weighted-history disk")


@lru_cache(maxsize=4)
def build_leaky_dobrushin_transverse_certificate(
    repository: Path,
    *,
    precision: int = PRECISION_BITS,
    sample_count: int = PHASE_SAMPLE_COUNT,
) -> LeakyDobrushinTransverseCertificate:
    """Build the source-validated finite-network theorem certificate."""

    equilibrium = build_equilibrium_stability_certificate()
    if not equilibrium.local_exponential_equilibrium_stability_proved:
        raise ValueError("the scalar quiet equilibrium source is not stable")
    alpha_lower = Fraction(
        equilibrium.alpha_interval["lower_fraction"]
    )
    alpha_upper = Fraction(
        equilibrium.alpha_interval["upper_fraction"]
    )
    quiet_centered = max(abs(alpha_lower - 1), abs(alpha_upper - 1))
    if quiet_centered >= Fraction(5, 2):
        raise ValueError("the quiet equilibrium left the common voltage strip")
    inner = _load_branch_strip(
        repository,
        "inner_saddle_candidate",
        precision=precision,
        sample_count=sample_count,
    )
    outer = _load_branch_strip(
        repository,
        "outer_pulse",
        precision=precision,
        sample_count=sample_count,
    )
    bounds = directed_leaky_dobrushin_bounds(precision=precision)
    certificate = LeakyDobrushinTransverseCertificate(
        schema_id=SCHEMA_ID,
        model_id=MODEL_ID,
        topology_class=(
            "every finite nonnegative row-stochastic Q with positive "
            "stationary pi and tau(Q)<=1/2; nonnegative B0,B1 with "
            "Bj*1=1/2*1 and pi^T*Bj=1/2*pi^T"
        ),
        phase_space_norm=(
            "max{diam(x),3*diam(y)} (real osc on real vectors), with both "
            "the unweighted retained-history supremum and its exp(lambda*"
            "theta)-weighted equivalent"
        ),
        quiet_centered_voltage_abs_upper=str(quiet_centered),
        inner=inner,
        outer=outer,
        bounds=bounds,
        scalar_quiet_equilibrium_stability_source_validated=True,
        scalar_inner_periodic_orbit_source_validated=True,
        scalar_outer_periodic_orbit_source_validated=True,
        synchronous_restriction_is_exact_scalar_model=True,
        collective_transverse_splitting_invariant_proved=True,
        complexified_transverse_diameter_estimate_proved=True,
        dobrushin_oscillation_dini_estimate_proved=True,
        balanced_half_mass_delay_bound_proved=True,
        exponentially_weighted_history_contraction_proved=True,
        arbitrary_finite_network_size_covered=True,
        arbitrary_admitted_balanced_topology_covered=True,
        quiet_transverse_exponential_decay_validated=True,
        inner_transverse_exponential_decay_validated=True,
        outer_transverse_exponential_decay_validated=True,
        full_network_quiet_local_exponential_stability_proved=True,
        all_noncollective_periodic_multipliers_inside_rate_disk_proved=True,
        inner_full_network_one_unstable_multiplier_validated=False,
        outer_full_network_orbital_attraction_validated=False,
        uniform_nonlinear_basin_radius_validated=False,
        physical_pulse_onset_lift_validated=False,
        general_closing_gap_networks_covered=False,
    )
    _validate_certificate_semantics(certificate)
    return certificate


def build_leaky_dobrushin_transverse_result(
    repository: Path,
) -> dict[str, Any]:
    certificate = asdict(
        build_leaky_dobrushin_transverse_certificate(repository)
    )
    return {
        "certificate": certificate,
        "manifest": {
            "schema_id": SCHEMA_ID,
            "result": RESULT_RELATIVE_PATH,
            "default_command": DEFAULT_COMMAND,
            "arithmetic": (
                ARITHMETIC_DESCRIPTION
            ),
            "certificate_sha256": canonical_sha256(certificate),
            "source_sha256": {
                relative: _sha256_path(repository / relative)
                for relative in SOURCE_MANIFEST
            },
            "parent_result_sha256": {
                relative: _sha256_path(repository / relative)
                for relative in (
                    INNER_RESULT_RELATIVE_PATH,
                    OUTER_RESULT_RELATIVE_PATH,
                    FLOQUET_RESULT_RELATIVE_PATH,
                )
            },
        },
    }


def validate_leaky_dobrushin_transverse_result(
    payload: Mapping[str, Any], repository: Path
) -> None:
    """Recompute the theorem and reject claim, source, or parent tampering."""

    if set(payload) != {"certificate", "manifest"}:
        raise ValueError("the leaky Dobrushin result schema changed")
    certificate = payload.get("certificate")
    manifest = payload.get("manifest")
    if not isinstance(certificate, Mapping) or not isinstance(manifest, Mapping):
        raise ValueError("the certificate or manifest is missing")
    expected = asdict(build_leaky_dobrushin_transverse_certificate(repository))
    if dict(certificate) != expected:
        raise ValueError("the certificate differs from directed replay")
    expected_manifest_keys = {
        "schema_id",
        "result",
        "default_command",
        "arithmetic",
        "certificate_sha256",
        "source_sha256",
        "parent_result_sha256",
    }
    if set(manifest) != expected_manifest_keys:
        raise ValueError("the result manifest schema changed")
    if manifest.get("schema_id") != SCHEMA_ID:
        raise ValueError("the result schema id changed")
    if manifest.get("result") != RESULT_RELATIVE_PATH:
        raise ValueError("the result path changed")
    if manifest.get("default_command") != DEFAULT_COMMAND:
        raise ValueError("the default command changed")
    if manifest.get("arithmetic") != ARITHMETIC_DESCRIPTION:
        raise ValueError("the arithmetic description changed")
    if manifest.get("certificate_sha256") != canonical_sha256(certificate):
        raise ValueError("the certificate digest changed")
    source_hashes = _mapping(manifest.get("source_sha256"), "source hashes")
    if set(source_hashes) != set(SOURCE_MANIFEST):
        raise ValueError("the source manifest paths changed")
    for relative in SOURCE_MANIFEST:
        if source_hashes.get(relative) != _sha256_path(repository / relative):
            raise ValueError(f"source hash changed: {relative}")
    parent_hashes = _mapping(
        manifest.get("parent_result_sha256"), "parent hashes"
    )
    parent_paths = (
        INNER_RESULT_RELATIVE_PATH,
        OUTER_RESULT_RELATIVE_PATH,
        FLOQUET_RESULT_RELATIVE_PATH,
    )
    if set(parent_hashes) != set(parent_paths):
        raise ValueError("the parent result paths changed")
    for relative in parent_paths:
        if parent_hashes.get(relative) != _sha256_path(repository / relative):
            raise ValueError(f"parent result hash changed: {relative}")


__all__ = [
    "DECAY_RATE",
    "DEFAULT_COMMAND",
    "GENERATOR_RELATIVE_PATH",
    "LeakyDobrushinBounds",
    "LeakyDobrushinTransverseCertificate",
    "LeakyBranchVoltageStrip",
    "NOTE_RELATIVE_PATH",
    "RESULT_RELATIVE_PATH",
    "SOURCE_MANIFEST",
    "build_leaky_dobrushin_transverse_certificate",
    "build_leaky_dobrushin_transverse_result",
    "directed_leaky_dobrushin_bounds",
    "validate_leaky_dobrushin_transverse_result",
]
