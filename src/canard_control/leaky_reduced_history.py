"""Exact reduced-history factorization for the leaky-recovery RFDE.

The voltage equation reads delayed voltage histories but no delayed recovery
history.  The recovery equation is a scalar current-state ODE.  Hence the
future factors through one voltage history and one current recovery value.
This module records the exact factorization, the pullback of stable sets and
the corresponding monodromy and pulse-transversality consequences.

No stable manifold is constructed here.  The result reduces the space in
which that later construction must be validated and proves how to pull it
back to the complete two-component RFDE history space.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Mapping

import sympy as sp

from canard_control.leaky_floquet_transfer import (
    validate_leaky_floquet_transfer_artifact,
)
from canard_control.leaky_pulse_terminal_history import (
    validate_pulse_terminal_history_result,
)


SCHEMA_ID = "leaky-reduced-history-factorization-v1"
MODEL_ID = "autonomous-leaky-recovery-two-delay-rfde"
SOURCE_RELATIVE_PATH = "src/canard_control/leaky_reduced_history.py"
GENERATOR_RELATIVE_PATH = "experiments/leaky_reduced_history.py"
NOTE_RELATIVE_PATH = "docs/leaky-reduced-history-factorization.md"
RESULT_RELATIVE_PATH = "experiments/results/leaky_reduced_history.json"
MODEL_SOURCE_RELATIVE_PATH = (
    "src/canard_control/autonomous_leaky_recovery_bistable.py"
)
PULSE_SOURCE_RELATIVE_PATH = (
    "src/canard_control/leaky_pulse_terminal_history.py"
)
PULSE_RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_pulse_terminal_history.json"
)
FLOQUET_RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_floquet_transfer.json"
)
TRACKED_PULSE_RESULT_SHA256 = (
    "db593b3675819f7b62180643ab983499e8e67790a0cacaf944ce099363a524c1"
)
TRACKED_FLOQUET_RESULT_SHA256 = (
    "5a3709ec792b29ed41533101245b13b3d35084ae508bdd1d420728200a5a5b16"
)
DEFAULT_COMMAND = (
    "PYTHONPATH=src /usr/bin/python3 experiments/leaky_reduced_history.py"
)
ARITHMETIC_DESCRIPTION = (
    "exact symbolic recovery-ODE identity and exact Banach-space "
    "semiflow factorization; parent theorem digests, source manifests, "
    "and evidence manifests are checked"
)
SOURCE_MANIFEST = (
    SOURCE_RELATIVE_PATH,
    GENERATOR_RELATIVE_PATH,
    NOTE_RELATIVE_PATH,
    MODEL_SOURCE_RELATIVE_PATH,
    PULSE_SOURCE_RELATIVE_PATH,
)


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


def exact_recovery_lift_defects() -> tuple[sp.Expr, ...]:
    """Differentiate the compatible recovery lift symbolically."""

    theta, epsilon, unfolding, omega = sp.symbols(
        "theta epsilon a omega", real=True
    )
    s = sp.symbols("s", real=True)
    q = sp.Function("q")
    recovery = sp.exp(-epsilon * theta) * (
        omega
        - epsilon
        * sp.Integral(
            sp.exp(epsilon * s) * (q(s) - unfolding),
            (s, theta, 0),
        )
    )
    ode_defect = sp.simplify(
        sp.diff(recovery, theta)
        - epsilon * (q(theta) - unfolding - recovery)
    )
    endpoint_defect = sp.simplify(recovery.subs(theta, 0) - omega)

    h = sp.Function("h")
    eta = sp.symbols("eta", real=True)
    derivative_lift = sp.exp(-epsilon * theta) * (
        eta
        - epsilon
        * sp.Integral(
            sp.exp(epsilon * s) * h(s),
            (s, theta, 0),
        )
    )
    derivative_ode_defect = sp.simplify(
        sp.diff(derivative_lift, theta)
        - epsilon * (h(theta) - derivative_lift)
    )
    derivative_endpoint_defect = sp.simplify(
        derivative_lift.subs(theta, 0) - eta
    )
    return (
        ode_defect,
        endpoint_defect,
        derivative_ode_defect,
        derivative_endpoint_defect,
    )


@dataclass(frozen=True)
class LeakyReducedHistoryCertificate:
    """Exact factorization theorem and its strict scope boundary."""

    schema_id: str
    model_id: str
    maximum_delay: str
    full_history_space: str
    reduced_history_space: str
    projection_formula: str
    compatible_lift_formula: str
    derivative_lift_formula: str
    reduced_semiflow_formula: str
    future_factorization_formula: str
    stable_set_pullback_formula: str
    monodromy_factorization_formula: str
    terminal_defining_function_formula: str
    terminal_crossing_derivative_formula: str
    exact_symbolic_zero_defect_count: int
    pulse_result_sha256: str
    floquet_result_sha256: str
    inner_period_lower: str
    outer_period_lower: str
    projection_has_continuous_split_right_inverse_proved: bool
    future_depends_only_on_voltage_history_and_current_recovery_proved: bool
    old_recovery_history_flushed_after_one_maximum_delay_proved: bool
    full_semiflow_factors_through_reduced_semiflow_proved: bool
    compatible_history_range_invariant_after_one_delay_proved: bool
    global_orbital_stable_set_pullback_equality_proved: bool
    local_stable_manifold_codimension_preserved_by_pullback_proved: bool
    inner_monodromy_nonzero_spectrum_reduction_proved: bool
    outer_monodromy_nonzero_spectrum_reduction_proved: bool
    old_recovery_history_fiber_contributes_only_zero_spectrum_proved: bool
    physical_pulse_terminal_history_compatible_proved: bool
    pulse_crossing_derivative_uses_only_reduced_terminal_derivative_proved: bool
    inner_reduced_dichotomy_validated: bool
    inner_stable_manifold_validated: bool
    physical_pulse_stable_manifold_crossing_validated: bool
    two_sided_physical_onset_validated: bool


def _load_parent_evidence(repository: Path) -> tuple[str, str]:
    pulse_path = repository / PULSE_RESULT_RELATIVE_PATH
    pulse_raw = pulse_path.read_bytes()
    if sha256(pulse_raw).hexdigest() != TRACKED_PULSE_RESULT_SHA256:
        raise ValueError("the tracked pulse terminal-history result changed")
    pulse_payload = json.loads(pulse_raw)
    validate_pulse_terminal_history_result(pulse_payload, repository)

    floquet_raw = (repository / FLOQUET_RESULT_RELATIVE_PATH).read_bytes()
    if sha256(floquet_raw).hexdigest() != TRACKED_FLOQUET_RESULT_SHA256:
        raise ValueError("the tracked Floquet transfer result changed")
    floquet = json.loads(floquet_raw)
    # The byte digest binds the precise theorem record used here.  The
    # parent's own validator is still required: it checks that the theorem
    # carrier, note, numerical parents, and their complete source manifests
    # have not drifted while the JSON result itself remained unchanged.
    validate_leaky_floquet_transfer_artifact(
        floquet, repository, recompute=False
    )
    artifact = floquet.get("artifact")
    if not isinstance(artifact, Mapping):
        raise ValueError("the Floquet artifact is missing")
    branches = artifact.get("branches")
    if not isinstance(branches, Mapping):
        raise ValueError("the Floquet branches are missing")
    periods: list[str] = []
    for branch in ("inner_saddle_candidate", "outer_pulse"):
        evidence = branches.get(branch)
        if not isinstance(evidence, Mapping):
            raise ValueError(f"the {branch} Floquet evidence is missing")
        if evidence.get("monodromy_compact") is not True:
            raise ValueError(f"the {branch} period is not longer than memory")
        period = evidence.get("minimum_period_lower")
        maximum_delay = evidence.get("maximum_delay_upper")
        if not isinstance(period, str) or not isinstance(maximum_delay, str):
            raise ValueError("the Floquet period comparison is missing")
        if sp.Rational(period) <= sp.Rational(maximum_delay):
            raise ValueError("a source period is not longer than memory")
        periods.append(period)
    return periods[0], periods[1]


def build_leaky_reduced_history_certificate(
    repository: Path,
) -> LeakyReducedHistoryCertificate:
    """Build the exact reduced-history theorem from source-bound parents."""

    defects = exact_recovery_lift_defects()
    if any(defect != 0 for defect in defects):
        raise AssertionError("the recovery lift identity failed")
    inner_period, outer_period = _load_parent_evidence(repository)
    return LeakyReducedHistoryCertificate(
        schema_id=SCHEMA_ID,
        model_id=MODEL_ID,
        maximum_delay="5*sqrt(5)",
        full_history_space="X=C([-r,0],R^2)",
        reduced_history_space="Y=C([-r,0],R)xR",
        projection_formula="pi(phi_v,phi_w)=(phi_v,phi_w(0))",
        compatible_lift_formula=(
            "R(q,omega)(theta)=exp(-epsilon*theta)*[omega-"
            "epsilon*integral_theta^0 exp(epsilon*s)*(q(s)-a) ds]"
        ),
        derivative_lift_formula=(
            "DR(q,omega)[h,eta](theta)=exp(-epsilon*theta)*[eta-"
            "epsilon*integral_theta^0 exp(epsilon*s)*h(s) ds]"
        ),
        reduced_semiflow_formula="pi*Phi_t=Psi_t*pi for every t>=0",
        future_factorization_formula="Phi_t=iota*Psi_t*pi for every t>=r",
        stable_set_pullback_formula=(
            "W_X^s(Gamma_X)=pi^{-1}(W_Y^s(Gamma_Y))"
        ),
        monodromy_factorization_formula="M_X=D_iota*M_Y*pi when T>r",
        terminal_defining_function_formula="h_X=h_Y*pi",
        terminal_crossing_derivative_formula=(
            "d_J h_X(K(J))=Dh_Y(pi*K(J))[pi*D_J K(J)]"
        ),
        exact_symbolic_zero_defect_count=len(defects),
        pulse_result_sha256=TRACKED_PULSE_RESULT_SHA256,
        floquet_result_sha256=TRACKED_FLOQUET_RESULT_SHA256,
        inner_period_lower=inner_period,
        outer_period_lower=outer_period,
        projection_has_continuous_split_right_inverse_proved=True,
        future_depends_only_on_voltage_history_and_current_recovery_proved=True,
        old_recovery_history_flushed_after_one_maximum_delay_proved=True,
        full_semiflow_factors_through_reduced_semiflow_proved=True,
        compatible_history_range_invariant_after_one_delay_proved=True,
        global_orbital_stable_set_pullback_equality_proved=True,
        local_stable_manifold_codimension_preserved_by_pullback_proved=True,
        inner_monodromy_nonzero_spectrum_reduction_proved=True,
        outer_monodromy_nonzero_spectrum_reduction_proved=True,
        old_recovery_history_fiber_contributes_only_zero_spectrum_proved=True,
        physical_pulse_terminal_history_compatible_proved=True,
        pulse_crossing_derivative_uses_only_reduced_terminal_derivative_proved=True,
        inner_reduced_dichotomy_validated=False,
        inner_stable_manifold_validated=False,
        physical_pulse_stable_manifold_crossing_validated=False,
        two_sided_physical_onset_validated=False,
    )


def build_leaky_reduced_history_result(repository: Path) -> dict[str, Any]:
    certificate = asdict(build_leaky_reduced_history_certificate(repository))
    return {
        "certificate": certificate,
        "manifest": {
            "schema_id": SCHEMA_ID,
            "result": RESULT_RELATIVE_PATH,
            "default_command": DEFAULT_COMMAND,
            "arithmetic": ARITHMETIC_DESCRIPTION,
            "certificate_sha256": canonical_sha256(certificate),
            "source_sha256": {
                relative: _sha256_path(repository / relative)
                for relative in SOURCE_MANIFEST
            },
            "parent_result_sha256": {
                PULSE_RESULT_RELATIVE_PATH: TRACKED_PULSE_RESULT_SHA256,
                FLOQUET_RESULT_RELATIVE_PATH: TRACKED_FLOQUET_RESULT_SHA256,
            },
        },
    }


def validate_leaky_reduced_history_result(
    payload: Mapping[str, Any], repository: Path
) -> None:
    """Recompute exact identities and reject source or claim tampering."""

    if set(payload) != {"certificate", "manifest"}:
        raise ValueError("the reduced-history result schema changed")
    certificate = payload.get("certificate")
    manifest = payload.get("manifest")
    if not isinstance(certificate, Mapping) or not isinstance(manifest, Mapping):
        raise ValueError("the reduced-history certificate or manifest is missing")
    expected = asdict(build_leaky_reduced_history_certificate(repository))
    if dict(certificate) != expected:
        raise ValueError("the reduced-history certificate differs from replay")
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
        raise ValueError("the reduced-history manifest schema changed")
    exact_scalars = {
        "schema_id": SCHEMA_ID,
        "result": RESULT_RELATIVE_PATH,
        "default_command": DEFAULT_COMMAND,
        "arithmetic": ARITHMETIC_DESCRIPTION,
        "certificate_sha256": canonical_sha256(certificate),
    }
    for name, expected_value in exact_scalars.items():
        if manifest.get(name) != expected_value:
            raise ValueError(f"the reduced-history manifest {name} changed")
    source_hashes = manifest.get("source_sha256")
    if not isinstance(source_hashes, Mapping):
        raise ValueError("the reduced-history source hashes are missing")
    if set(source_hashes) != set(SOURCE_MANIFEST):
        raise ValueError("the reduced-history source paths changed")
    for relative in SOURCE_MANIFEST:
        if source_hashes.get(relative) != _sha256_path(repository / relative):
            raise ValueError(f"source hash changed: {relative}")
    parent_hashes = manifest.get("parent_result_sha256")
    expected_parents = {
        PULSE_RESULT_RELATIVE_PATH: TRACKED_PULSE_RESULT_SHA256,
        FLOQUET_RESULT_RELATIVE_PATH: TRACKED_FLOQUET_RESULT_SHA256,
    }
    if parent_hashes != expected_parents:
        raise ValueError("the reduced-history parent hashes changed")
    for relative, digest in expected_parents.items():
        if _sha256_path(repository / relative) != digest:
            raise ValueError(f"parent result changed: {relative}")


__all__ = [
    "DEFAULT_COMMAND",
    "FLOQUET_RESULT_RELATIVE_PATH",
    "GENERATOR_RELATIVE_PATH",
    "LeakyReducedHistoryCertificate",
    "NOTE_RELATIVE_PATH",
    "RESULT_RELATIVE_PATH",
    "SOURCE_MANIFEST",
    "PULSE_RESULT_RELATIVE_PATH",
    "TRACKED_FLOQUET_RESULT_SHA256",
    "TRACKED_PULSE_RESULT_SHA256",
    "build_leaky_reduced_history_certificate",
    "build_leaky_reduced_history_result",
    "exact_recovery_lift_defects",
    "validate_leaky_reduced_history_result",
]
