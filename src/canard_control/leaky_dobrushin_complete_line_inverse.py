"""Complete-line transverse Green inverse for the leaky network class.

The companion Dobrushin--Halanay certificate proves forward contraction
along three named synchronous invariant objects.  Its differential
inequality in fact uses only a pointwise voltage strip.  This module records
and proves that stripwise statement for an arbitrary complete synchronous
trajectory and then takes the zero-history pullback limit.  The result is a
bounded complete transverse Green operator, uniform in every finite network
in the admitted balanced Dobrushin class.

This is the missing transverse block in a canonical synchronized Lin
realization: whenever a scalar complete-history connection, its Fredholm Lin
operator, and its simple normalized gap have independently been proved inside
the voltage strip, and all auxiliary traces are collective, the full network
Lin operator is the direct sum of the scalar collective block and this
invertible transverse block.  Under precisely those hypotheses the scalar
Fredholm index, cokernel, gap, root, and root slope are preserved exactly.

No scalar canard connection for the leaky model is created here.  In
particular, the conditional root-transfer implication must not be read as a
validated leaky canard root or as physical pulse onset.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from hashlib import sha256
import json
from pathlib import Path
import platform
from typing import Any, Mapping

import gmpy2

from canard_control.leaky_dobrushin_transverse_halanay import (
    RESULT_RELATIVE_PATH as HALANAY_RESULT_RELATIVE_PATH,
    validate_leaky_dobrushin_transverse_result,
)


SCHEMA_ID = "leaky-dobrushin-complete-line-inverse-v1"
SOURCE_RELATIVE_PATH = (
    "src/canard_control/leaky_dobrushin_complete_line_inverse.py"
)
GENERATOR_RELATIVE_PATH = (
    "experiments/leaky_dobrushin_complete_line_inverse.py"
)
NOTE_RELATIVE_PATH = "docs/leaky-dobrushin-complete-line-inverse.md"
RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_dobrushin_complete_line_inverse.json"
)
DEFAULT_COMMAND = (
    "OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONPATH=src "
    "/usr/bin/python3 experiments/leaky_dobrushin_complete_line_inverse.py"
)
ARITHMETIC_SCOPE = (
    "exact complete-line pullback/uniqueness and collective-transverse "
    "direct-sum arguments, using the source-validated 160-bit directed "
    "Dobrushin-Halanay constants; no scalar leaky canard root, nonlinear "
    "network canard persistence, physical onset, or pulse threshold"
)
SOURCE_MANIFEST = (
    SOURCE_RELATIVE_PATH,
    GENERATOR_RELATIVE_PATH,
    NOTE_RELATIVE_PATH,
)


PROVED_FLAGS = (
    "stripwise_halanay_inequality_for_every_complete_synchronous_trajectory",
    "complex_transverse_diameter_spaces_complete_for_each_finite_network",
    "weighted_history_evolution_contraction_uniform_in_network_size",
    "forced_weighted_history_comparison_proved",
    "pullback_uses_only_forward_rfde_evolution_proved",
    "bounded_complete_transverse_homogeneous_kernel_trivial",
    "bounded_complete_transverse_forced_solution_exists_uniquely",
    "bounded_complete_transverse_green_inverse_uniform_in_network_size",
    "canonical_collective_transverse_lin_direct_sum_proved",
    "conditional_scalar_simple_root_data_transfer_exactly",
)

OPEN_FLAGS = (
    "scalar_leaky_complete_history_canard_connection_validated",
    "scalar_leaky_simple_canard_root_validated",
    "unconditional_full_network_canard_connection_validated",
    "noncanonical_endpoint_trace_rules_covered",
    "nonlinear_asynchronous_network_canard_persistence_validated",
    "physical_pulse_onset_identified_with_canard_root",
)


@dataclass(frozen=True)
class LeakyCompleteLineInverseCertificate:
    """Exact implication and its source-validated numerical constants."""

    schema_id: str
    model_id: str
    topology_class: str
    collective_projection: str
    transverse_current_space: str
    transverse_space_completeness: str
    transverse_history_norm: str
    bounded_solution_norm: str
    forcing_space: str
    forcing_norm: str
    dimension_uniformity_scope: str
    voltage_strip: str
    maximum_delay_upper: str
    local_decay_lower: str
    delayed_gain_upper: str
    exponential_rate: str
    rate_residual_lower: str
    homogeneous_history_contraction: str
    forced_history_comparison: str
    pullback_construction: str
    pullback_cauchy_bound: str
    green_operator_mapping: str
    complete_line_green_norm_upper: str
    transverse_lin_operator_spaces: str
    canonical_lin_factorization: str
    canonical_lin_hypotheses: tuple[str, ...]
    transferred_data: tuple[str, ...]
    stripwise_halanay_inequality_for_every_complete_synchronous_trajectory: bool
    complex_transverse_diameter_spaces_complete_for_each_finite_network: bool
    weighted_history_evolution_contraction_uniform_in_network_size: bool
    forced_weighted_history_comparison_proved: bool
    pullback_uses_only_forward_rfde_evolution_proved: bool
    bounded_complete_transverse_homogeneous_kernel_trivial: bool
    bounded_complete_transverse_forced_solution_exists_uniquely: bool
    bounded_complete_transverse_green_inverse_uniform_in_network_size: bool
    canonical_collective_transverse_lin_direct_sum_proved: bool
    conditional_scalar_simple_root_data_transfer_exactly: bool
    scalar_leaky_complete_history_canard_connection_validated: bool
    scalar_leaky_simple_canard_root_validated: bool
    unconditional_full_network_canard_connection_validated: bool
    noncanonical_endpoint_trace_rules_covered: bool
    nonlinear_asynchronous_network_canard_persistence_validated: bool
    physical_pulse_onset_identified_with_canard_root: bool
    minimal_remaining_scalar_gate: str


def _sha256_path(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def canonical_sha256(value: Any) -> str:
    return sha256(
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        ).encode("ascii")
    ).hexdigest()


def _mapping(value: Any, label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{label} must be a mapping")
    return value


def _load_parent(repository: Path) -> tuple[Mapping[str, Any], str]:
    path = repository / HALANAY_RESULT_RELATIVE_PATH
    raw = path.read_bytes()
    payload = _mapping(json.loads(raw), "Dobrushin-Halanay result")
    validate_leaky_dobrushin_transverse_result(payload, repository)
    return payload, sha256(raw).hexdigest()


def build_leaky_complete_line_inverse_certificate(
    repository: Path,
) -> LeakyCompleteLineInverseCertificate:
    """Build the complete-line theorem from the validated strip constants.

    The proof behind the returned truth values is analytic.  For a transverse
    forcing ``f`` put

        F(t)=max{diam f_v(t), 3 diam f_w(t)}.

    Zero-history solutions begun at ``S`` obey the *history-state* forced
    comparison

        ||z_t^S||_lambda
        <= integral_S^t exp(-lambda*(t-u))*F(u) du.

    Their pullback limit as ``S -> -infinity`` is therefore bounded by
    ``||F||_infinity/lambda`` in the declared retained-history norm.
    Differences between two such approximants satisfy the homogeneous
    contraction, which proves convergence and uniqueness.  This argument
    never inverts a retarded semiflow backwards.
    """

    repository = repository.resolve()
    parent, _ = _load_parent(repository)
    source = _mapping(parent.get("certificate"), "Halanay certificate")
    bounds = _mapping(source.get("bounds"), "Halanay bounds")
    required_parent_flags = (
        "synchronous_restriction_is_exact_scalar_model",
        "collective_transverse_splitting_invariant_proved",
        "complexified_transverse_diameter_estimate_proved",
        "dobrushin_oscillation_dini_estimate_proved",
        "balanced_half_mass_delay_bound_proved",
        "exponentially_weighted_history_contraction_proved",
        "arbitrary_finite_network_size_covered",
        "arbitrary_admitted_balanced_topology_covered",
    )
    if any(source.get(name) is not True for name in required_parent_flags):
        raise ValueError("the required Dobrushin-Halanay theorem is absent")

    rate = gmpy2.mpq(str(bounds["exponential_rate"]))
    residual = gmpy2.mpq(str(bounds["rate_residual_lower"]))
    if rate <= 0 or residual <= 0:
        raise ValueError("the complete-line theorem requires a strict rate")
    green_bound = 1 / rate
    if rate != gmpy2.mpq(1, 10) or green_bound != 10:
        raise ValueError("the declared Green constant is no longer ten")

    return LeakyCompleteLineInverseCertificate(
        schema_id=SCHEMA_ID,
        model_id=str(source["model_id"]),
        topology_class=str(source["topology_class"]),
        collective_projection=(
            "pi^T with pi^T*1=1; collective lift c -> c*1"
        ),
        transverse_current_space=(
            "E_{N,perp}=ker(pi^T) x ker(pi^T), "
            "m(x,y)=max{diam x,3 diam y} over C"
        ),
        transverse_space_completeness=(
            "for each finite N, complex diameter is a norm on ker(pi^T); "
            "E_{N,perp}, X_{N,lambda}=C([-r,0],E_{N,perp}), and their "
            "bounded-continuous complete-line spaces are Banach"
        ),
        transverse_history_norm=(
            "sup_{-r<=theta<=0} exp(lambda*theta) "
            "max{diam x(theta),3 diam y(theta)}"
        ),
        bounded_solution_norm=(
            "sup_{t in R} ||z_t||_lambda on C_b(R,X_{N,lambda})"
        ),
        forcing_space="C_b(R,E_{N,perp})",
        forcing_norm=(
            "sup_t max{diam f_v(t),3 diam f_w(t)}"
        ),
        dimension_uniformity_scope=(
            "rate and Green history-norm bound are uniform in N/topology "
            "in diameter norms; no N-uniform equivalence with Euclidean "
            "norms or nonlinear neighborhood is asserted"
        ),
        voltage_strip=(
            "every complete synchronous V with sup_t |V(t)-1|<=5/2"
        ),
        maximum_delay_upper=str(bounds["maximum_delay_upper"]),
        local_decay_lower=str(bounds["local_decay_lower"]),
        delayed_gain_upper=str(bounds["delayed_total_gain_upper"]),
        exponential_rate=str(bounds["exponential_rate"]),
        rate_residual_lower=str(bounds["rate_residual_lower"]),
        homogeneous_history_contraction=(
            "||U_perp(t,s)||_lambda <= exp(-lambda*(t-s)), t>=s"
        ),
        forced_history_comparison=(
            "||z_t^S||_lambda <= integral_S^t exp(-lambda*(t-u)) "
            "max{diam f_v(u),3 diam f_w(u)} du"
        ),
        pullback_construction=(
            "locally uniform limit as S->-infinity of the forced "
            "zero-history solution begun at S"
        ),
        pullback_cauchy_bound=(
            "for S1<S2<=t, ||z_t^{S1}-z_t^{S2}||_lambda <= "
            "exp(-lambda*(t-S2))*||f||_infinity/lambda"
        ),
        green_operator_mapping=(
            "G_perp:C_b(R,E_{N,perp})->C_b(R,X_{N,lambda}); causal "
            "history-state component norm"
        ),
        complete_line_green_norm_upper=str(green_bound),
        transverse_lin_operator_spaces=(
            "L_perp:D_perp->C_b(R,E_{N,perp}), where D_perp is the "
            "bounded classical RFDE domain with graph norm; the number "
            "10 bounds only the C_b(R,X_{N,lambda}) component of G_perp"
        ),
        canonical_lin_factorization=(
            "L_N = L_collective direct_sum L_perp on the synchronized "
            "complete-line Lin realization with bounded-complete "
            "transverse trace"
        ),
        canonical_lin_hypotheses=(
            "a scalar complete synchronous connection exists wholly in "
            "the declared voltage strip",
            "the scalar phase-fixed Lin operator on its declared domain "
            "and range is Fredholm",
            "pi^T*1=1 and the network Lin domain/range use the induced "
            "collective-transverse product splitting",
            "phase, endpoint trace, cokernel normalization, and gap act "
            "only on the collective block; the transverse trace is the "
            "unique bounded-complete one",
            "the varied parameter and any inhomogeneity used to define "
            "the scalar gap are synchronous",
        ),
        transferred_data=(
            "Fredholm index",
            "kernel dimension",
            "cokernel dimension",
            "normalized scalar gap",
            "simple-root location",
            "simple-root slope and orientation",
        ),
        **{name: True for name in PROVED_FLAGS},
        **{name: False for name in OPEN_FLAGS},
        minimal_remaining_scalar_gate=(
            "validate in this same leaky RFDE a scalar complete-history "
            "canard connection lying in |V-1|<=5/2, its phase-fixed "
            "Fredholm Lin realization, and a normalized nonzero scalar "
            "gap slope; the canonical synchronized network realization "
            "then transfers these data without an N-dependent diameter-"
            "norm estimate"
        ),
    )


def build_leaky_complete_line_inverse_result(
    repository: Path,
) -> dict[str, Any]:
    repository = repository.resolve()
    # JSON is the canonical carrier.  Normalize tuples before hashing and
    # replay comparison so an in-memory dataclass and its stored JSON do not
    # disagree merely because JSON represents tuples as arrays.
    certificate = json.loads(
        json.dumps(
            asdict(build_leaky_complete_line_inverse_certificate(repository)),
            sort_keys=True,
            ensure_ascii=True,
            allow_nan=False,
        )
    )
    parent_path = repository / HALANAY_RESULT_RELATIVE_PATH
    return {
        "certificate": certificate,
        "manifest": {
            "schema_id": SCHEMA_ID,
            "result": RESULT_RELATIVE_PATH,
            "default_command": DEFAULT_COMMAND,
            "arithmetic_scope": ARITHMETIC_SCOPE,
            "certificate_sha256": canonical_sha256(certificate),
            "source_sha256": {
                relative: _sha256_path(repository / relative)
                for relative in SOURCE_MANIFEST
            },
            "halanay_parent_result": HALANAY_RESULT_RELATIVE_PATH,
            "halanay_parent_result_sha256": _sha256_path(parent_path),
            "environment": {
                "python": platform.python_version(),
                "gmpy2": gmpy2.__version__,
                "mpfr": gmpy2.mpfr_version(),
            },
        },
    }


def validate_leaky_complete_line_inverse_result(
    payload: Mapping[str, Any], repository: Path
) -> None:
    """Rebuild the theorem and reject provenance or claim promotion."""

    if not isinstance(payload, Mapping) or set(payload) != {
        "certificate",
        "manifest",
    }:
        raise ValueError("the complete-line inverse has the wrong outer schema")
    certificate = _mapping(payload.get("certificate"), "certificate")
    manifest = _mapping(payload.get("manifest"), "manifest")
    expected_fields = {
        field.name for field in fields(LeakyCompleteLineInverseCertificate)
    }
    if set(certificate) != expected_fields:
        raise ValueError("the complete-line certificate schema changed")
    if any(certificate.get(name) is not True for name in PROVED_FLAGS):
        raise ValueError("a proved complete-line statement was weakened")
    if any(certificate.get(name) is not False for name in OPEN_FLAGS):
        raise ValueError("an open canard or onset statement was promoted")
    if gmpy2.mpq(str(certificate["complete_line_green_norm_upper"])) != 10:
        raise ValueError("the complete-line Green bound changed")

    repository = repository.resolve()
    expected = build_leaky_complete_line_inverse_result(repository)
    if dict(payload) != expected:
        raise ValueError("the complete-line result differs from exact replay")


__all__ = [
    "DEFAULT_COMMAND",
    "GENERATOR_RELATIVE_PATH",
    "LeakyCompleteLineInverseCertificate",
    "NOTE_RELATIVE_PATH",
    "OPEN_FLAGS",
    "PROVED_FLAGS",
    "RESULT_RELATIVE_PATH",
    "SOURCE_MANIFEST",
    "build_leaky_complete_line_inverse_certificate",
    "build_leaky_complete_line_inverse_result",
    "validate_leaky_complete_line_inverse_result",
]
