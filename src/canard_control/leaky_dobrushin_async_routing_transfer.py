"""Conditional asynchronous routing and threshold transfer.

This module composes the proved retained-history collective-defect estimate with a
*separately validated* scalar robust-routing tube.  The composition is an
exact theorem, but no scalar routing budget, strip margin, target-lift margin,
gap slope, or gap response constant is currently available for the leaky
model.  Consequently every concrete asynchronous-onset flag remains false.

The point of the contract is to make the missing implication executable.  It
also prevents the stripwise synchronization theorem from being mistaken for
a topology-uniform basin or threshold theorem.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
import platform
from typing import Any, Mapping

from canard_control.leaky_dobrushin_collective_defect import (
    RESULT_RELATIVE_PATH as COLLECTIVE_DEFECT_RESULT_RELATIVE_PATH,
    validate_collective_defect_result,
)


SCHEMA_ID = "leaky-dobrushin-async-routing-transfer-v2"
SOURCE_RELATIVE_PATH = (
    "src/canard_control/leaky_dobrushin_async_routing_transfer.py"
)
GENERATOR_RELATIVE_PATH = (
    "experiments/leaky_dobrushin_async_routing_transfer.py"
)
NOTE_RELATIVE_PATH = "docs/leaky-dobrushin-async-routing-transfer.md"
TEST_RELATIVE_PATH = "tests/test_leaky_dobrushin_async_routing_transfer.py"
RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_dobrushin_async_routing_transfer.json"
)
DEFAULT_COMMAND = (
    "PYTHONPATH=src /usr/bin/python3 "
    "experiments/leaky_dobrushin_async_routing_transfer.py"
)
ARITHMETIC_SCOPE = (
    "exact rational composition of the source-validated delayed-history "
    "collective defect using the strict rational upper 56483/3200 for "
    "703/40+27*sqrt(5)/800, with explicitly declared scalar route, lift, "
    "and gap-response budgets; no scalar budget is numerically supplied"
)

DEFECT_L1_CONSTANT = Fraction(56483, 3200)
DEFECT_L1_RECIPROCAL = Fraction(3200, 56483)

PROVED_FLAGS = (
    "first_strip_exit_bootstrap_implication_proved",
    "conditional_exact_mean_routing_radius_formula_proved",
    "conditional_full_history_ball_budget_formula_proved",
    "monotone_gap_root_perturbation_lemma_proved",
    "conditional_threshold_shift_formula_proved",
    "conditional_safety_guard_formula_proved",
    "conditional_constants_uniform_in_finite_network_size_proved",
    "conditional_constants_uniform_in_admitted_topology_proved",
)

OPEN_FLAGS = (
    "scalar_forced_routing_tube_validated",
    "scalar_route_strip_margin_validated",
    "network_target_lift_margin_validated",
    "scalar_gap_slope_validated",
    "scalar_gap_forcing_response_validated",
    "scalar_gap_derivative_response_validated",
    "concrete_positive_asynchronous_radius_certified",
    "asynchronous_unique_pulse_threshold_certified",
    "asynchronous_two_sided_basin_routing_certified",
    "heterogeneous_node_parameters_covered",
)


@dataclass(frozen=True)
class LeakyAsyncRoutingTransferCertificate:
    schema_id: str
    model_id: str
    topology_class: str
    parent_pointwise_defect_constant_exact: str
    parent_accumulated_defect_constant_exact: str
    parent_accumulated_defect_constant_rational_upper: str
    initial_size_definition: str
    scalar_route_hypothesis: str
    first_exit_bootstrap: str
    exact_mean_radius_squared_formula: str
    full_history_ball_budget: str
    product_basin_lift_hypothesis: str
    scalar_gap_hypothesis: str
    gap_value_error_formula: str
    gap_derivative_error_formula: str
    threshold_existence_conditions: str
    threshold_shift_formula: str
    safety_guard_formula: str
    uniformity_scope: str
    validated_scalar_route_l1_budget: str | None
    validated_scalar_strip_margin: str | None
    validated_network_target_lift_margin: str | None
    validated_scalar_gap_slope: str | None
    validated_gap_value_response_constants: str | None
    validated_gap_derivative_response_constants: str | None
    concrete_asynchronous_radius: str | None
    concrete_threshold_shift_bound: str | None
    strict_boundary: str
    first_strip_exit_bootstrap_implication_proved: bool
    conditional_exact_mean_routing_radius_formula_proved: bool
    conditional_full_history_ball_budget_formula_proved: bool
    monotone_gap_root_perturbation_lemma_proved: bool
    conditional_threshold_shift_formula_proved: bool
    conditional_safety_guard_formula_proved: bool
    conditional_constants_uniform_in_finite_network_size_proved: bool
    conditional_constants_uniform_in_admitted_topology_proved: bool
    scalar_forced_routing_tube_validated: bool
    scalar_route_strip_margin_validated: bool
    network_target_lift_margin_validated: bool
    scalar_gap_slope_validated: bool
    scalar_gap_forcing_response_validated: bool
    scalar_gap_derivative_response_validated: bool
    concrete_positive_asynchronous_radius_certified: bool
    asynchronous_unique_pulse_threshold_certified: bool
    asynchronous_two_sided_basin_routing_certified: bool
    heterogeneous_node_parameters_covered: bool


def _mapping(value: Any, label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{label} must be a mapping")
    return value


def _positive(value: Fraction | int | str, label: str) -> Fraction:
    result = Fraction(value)
    if result <= 0:
        raise ValueError(f"{label} must be strictly positive")
    return result


def _nonnegative(value: Fraction | int | str, label: str) -> Fraction:
    result = Fraction(value)
    if result < 0:
        raise ValueError(f"{label} must be nonnegative")
    return result


def exact_mean_routing_radius_squared(
    d_strip: Fraction | int | str,
    d_lift: Fraction | int | str,
    eta_route: Fraction | int | str,
) -> Fraction:
    """Return the exact strict squared-radius budget for zero mean error.

    The theorem uses ``M0**2 < returned_value``.  Strictness is essential for
    the first-exit contradiction and is deliberately not hidden here.
    """

    strip = _positive(d_strip, "d_strip")
    lift = _positive(d_lift, "d_lift")
    eta = _positive(eta_route, "eta_route")
    return min(
        strip * strip,
        lift * lift,
        DEFECT_L1_RECIPROCAL * eta,
    )


def full_history_route_budget_holds(
    radius: Fraction | int | str,
    d_strip: Fraction | int | str,
    d_lift: Fraction | int | str,
    initial_response: Fraction | int | str,
    eta_route: Fraction | int | str,
) -> bool:
    """Check the exact sufficient budget for a full nodewise history ball."""

    size = _nonnegative(radius, "radius")
    strip = _positive(d_strip, "d_strip")
    lift = _positive(d_lift, "d_lift")
    initial = _nonnegative(initial_response, "initial_response")
    eta = _positive(eta_route, "eta_route")
    return (
        size < strip
        and size < lift
        and initial * size + DEFECT_L1_CONSTANT * size * size < eta
    )


def gap_value_error_bound(
    radius: Fraction | int | str,
    initial_gap_response: Fraction | int | str,
    forcing_gap_response: Fraction | int | str,
) -> Fraction:
    """Exact upper bound for the perturbed gap value error."""

    size = _nonnegative(radius, "radius")
    initial = _nonnegative(initial_gap_response, "initial_gap_response")
    forcing = _nonnegative(forcing_gap_response, "forcing_gap_response")
    return initial * size + forcing * DEFECT_L1_CONSTANT * size * size


def gap_derivative_error_bound(
    radius: Fraction | int | str,
    initial_derivative_response: Fraction | int | str,
    forcing_derivative_response: Fraction | int | str,
) -> Fraction:
    """Exact upper bound for the perturbation of the gap's J derivative."""

    size = _nonnegative(radius, "radius")
    initial = _nonnegative(
        initial_derivative_response, "initial_derivative_response"
    )
    forcing = _nonnegative(
        forcing_derivative_response, "forcing_derivative_response"
    )
    return initial * size + forcing * DEFECT_L1_CONSTANT * size * size


def threshold_budget_holds(
    radius: Fraction | int | str,
    gap_slope: Fraction | int | str,
    parameter_half_width: Fraction | int | str,
    initial_gap_response: Fraction | int | str,
    forcing_gap_response: Fraction | int | str,
    initial_derivative_response: Fraction | int | str,
    forcing_derivative_response: Fraction | int | str,
) -> bool:
    """Check endpoint signs and monotonicity on the declared local interval."""

    slope = _positive(gap_slope, "gap_slope")
    width = _positive(parameter_half_width, "parameter_half_width")
    value_error = gap_value_error_bound(
        radius, initial_gap_response, forcing_gap_response
    )
    derivative_error = gap_derivative_error_bound(
        radius, initial_derivative_response, forcing_derivative_response
    )
    return value_error < slope * width and derivative_error < slope


def threshold_shift_bound(
    radius: Fraction | int | str,
    gap_slope: Fraction | int | str,
    initial_gap_response: Fraction | int | str,
    forcing_gap_response: Fraction | int | str,
) -> Fraction:
    """Return the local-interval root displacement bound epsilon_H/m_J."""

    slope = _positive(gap_slope, "gap_slope")
    return gap_value_error_bound(
        radius, initial_gap_response, forcing_gap_response
    ) / slope


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


def _validated_parent(repository: Path) -> Mapping[str, Any]:
    path = repository / COLLECTIVE_DEFECT_RESULT_RELATIVE_PATH
    payload = _mapping(json.loads(path.read_bytes()), "collective result")
    validate_collective_defect_result(payload, repository)
    return _mapping(payload.get("certificate"), "collective certificate")


def build_async_routing_transfer_certificate(
    repository: Path,
) -> LeakyAsyncRoutingTransferCertificate:
    repository = repository.resolve()
    parent = _validated_parent(repository)
    if parent.get("pointwise_defect_constant_exact") != "703/200":
        raise ValueError("the parent pointwise defect constant changed")
    if parent.get("accumulated_defect_constant_exact") != (
        "703/40+27*sqrt(5)/800"
    ):
        raise ValueError("the parent accumulated defect constant changed")
    if parent.get("accumulated_defect_constant_rational_upper") != (
        "56483/3200"
    ):
        raise ValueError("the parent rational defect upper bound changed")
    if parent.get("conditional_integrable_collective_defect_proved") is not True:
        raise ValueError("the parent integrable-defect theorem is absent")

    values: dict[str, Any] = {name: True for name in PROVED_FLAGS}
    values.update({name: False for name in OPEN_FLAGS})
    return LeakyAsyncRoutingTransferCertificate(
        schema_id=SCHEMA_ID,
        model_id=str(parent["model_id"]),
        topology_class=str(parent["topology_class"]),
        parent_pointwise_defect_constant_exact="703/200",
        parent_accumulated_defect_constant_exact=(
            "703/40+27*sqrt(5)/800"
        ),
        parent_accumulated_defect_constant_rational_upper="56483/3200",
        initial_size_definition=(
            "R0=max{distance of the pi-mean entrance history from the "
            "scalar pulse entrance, retained-past transverse diameter "
            "M0=sup_[t0-r,t0] M(s)}"
        ),
        scalar_route_hypothesis=(
            "every scalar entrance/voltage-forcing pair with combined "
            "budget L0*delta_mean+||e||_L1<eta_route follows the declared "
            "signed route and keeps its mean voltage d_strip inside the strip"
        ),
        first_exit_bootstrap=(
            "before a hypothetical first nodewise strip exit, extend R_coll "
            "by zero; its full L1 norm is <=(56483/3200)M0^2 after retaining "
            "both delayed initial-history residence intervals, so the scalar route "
            "keeps the mean d_strip inside and "
            "|v_i-bar_v|<=osc(v)<=M0<d_strip, contradicting first exit"
        ),
        exact_mean_radius_squared_formula=(
            "M0^2<min{d_strip^2,d_lift^2,(3200/56483)*eta_route}"
        ),
        full_history_ball_budget=(
            "R0<min{d_strip,d_lift} and "
            "L0*R0+(56483/3200)*R0^2<eta_route"
        ),
        product_basin_lift_hypothesis=(
            "a separately certified d_lift margin must turn a routed scalar "
            "target history plus transverse diameter <d_lift into the "
            "corresponding full-network target basin"
        ),
        scalar_gap_hypothesis=(
            "H and the network-perturbed gap H_tilde are C1; H(Jc)=0 "
            "and H'(J)>=m_J>0 on [Jc-r_J,Jc+r_J]"
        ),
        gap_value_error_formula=(
            "epsilon_H(R0)=L_H0*R0+L_H1*(56483/3200)*R0^2"
        ),
        gap_derivative_error_formula=(
            "delta_HJ(R0)=L_HJ0*R0+L_HJ1*(56483/3200)*R0^2"
        ),
        threshold_existence_conditions=(
            "epsilon_H(R0)<m_J*r_J and delta_HJ(R0)<m_J; then the perturbed "
            "gap has opposite endpoint signs, positive derivative, and exactly "
            "one root in [Jc-r_J,Jc+r_J]; no root outside is asserted"
        ),
        threshold_shift_formula=(
            "for the interval root, |Jc_network-Jc|<=epsilon_H(R0)/m_J"
        ),
        safety_guard_formula=(
            "for J in [Jc-r_J,Jc+r_J], |J-Jc|>epsilon_H(R0)/m_J "
            "preserves the signed local threshold side"
        ),
        uniformity_scope=(
            "once the scalar route, lift, and gap constants are common, the "
            "formulas are independent of finite N, pi_min, and admitted topology"
        ),
        validated_scalar_route_l1_budget=None,
        validated_scalar_strip_margin=None,
        validated_network_target_lift_margin=None,
        validated_scalar_gap_slope=None,
        validated_gap_value_response_constants=None,
        validated_gap_derivative_response_constants=None,
        concrete_asynchronous_radius=None,
        concrete_threshold_shift_bound=None,
        strict_boundary=(
            "all radius inequalities are strict; no scalar forced-routing "
            "tube, target-lift margin, concrete asynchronous radius, perturbed "
            "threshold, global root uniqueness, basin route, or biological "
            "safety theorem is promoted"
        ),
        **values,
    )


def json_ready_async_routing_transfer(repository: Path) -> dict[str, Any]:
    return asdict(build_async_routing_transfer_certificate(repository))


def validate_async_routing_transfer_result(
    payload: Mapping[str, Any], repository: Path
) -> None:
    if not isinstance(payload, Mapping) or set(payload) != {
        "certificate",
        "manifest",
    }:
        raise ValueError("async routing result requires two records")
    certificate = _mapping(payload.get("certificate"), "certificate")
    manifest = _mapping(payload.get("manifest"), "manifest")
    if set(certificate) != {
        field.name for field in fields(LeakyAsyncRoutingTransferCertificate)
    }:
        raise ValueError("async routing certificate schema changed")
    if any(certificate.get(name) is not True for name in PROVED_FLAGS):
        raise ValueError("an abstract composition theorem flag was weakened")
    if any(certificate.get(name) is not False for name in OPEN_FLAGS):
        raise ValueError("an open asynchronous claim was promoted")
    null_fields = (
        "validated_scalar_route_l1_budget",
        "validated_scalar_strip_margin",
        "validated_network_target_lift_margin",
        "validated_scalar_gap_slope",
        "validated_gap_value_response_constants",
        "validated_gap_derivative_response_constants",
        "concrete_asynchronous_radius",
        "concrete_threshold_shift_bound",
    )
    if any(certificate.get(name) is not None for name in null_fields):
        raise ValueError("an unvalidated scalar/network constant was inserted")
    if certificate.get("parent_accumulated_defect_constant_exact") != (
        "703/40+27*sqrt(5)/800"
    ) or certificate.get(
        "parent_accumulated_defect_constant_rational_upper"
    ) != "56483/3200":
        raise ValueError("the delayed-history parent budget changed")

    sources = {
        "source": SOURCE_RELATIVE_PATH,
        "generator": GENERATOR_RELATIVE_PATH,
        "note": NOTE_RELATIVE_PATH,
        "test": TEST_RELATIVE_PATH,
        "parent_result": COLLECTIVE_DEFECT_RESULT_RELATIVE_PATH,
    }
    expected_manifest_keys = {
        "schema_id",
        "certificate_sha256",
        "default_command",
        "arithmetic_scope",
        "python",
        "platform",
        *sources.keys(),
        *(f"{name}_sha256" for name in sources),
    }
    if set(manifest) != expected_manifest_keys:
        raise ValueError("async routing manifest schema changed")
    if manifest.get("schema_id") != SCHEMA_ID:
        raise ValueError("async routing manifest identity changed")
    if manifest.get("certificate_sha256") != canonical_sha256(certificate):
        raise ValueError("async routing certificate digest changed")
    if manifest.get("default_command") != DEFAULT_COMMAND or manifest.get(
        "arithmetic_scope"
    ) != ARITHMETIC_SCOPE:
        raise ValueError("async routing method disclosure changed")
    if manifest.get("python") != platform.python_version() or manifest.get(
        "platform"
    ) != platform.platform():
        raise ValueError("async routing runtime changed")
    for name, relative in sources.items():
        if manifest.get(name) != relative:
            raise ValueError(f"async routing {name} path changed")
        if manifest.get(f"{name}_sha256") != _sha256_path(repository / relative):
            raise ValueError(f"async routing {name} hash changed")
    expected = json_ready_async_routing_transfer(repository)
    if certificate != expected:
        raise ValueError("async routing certificate differs from replay")


__all__ = [
    "ARITHMETIC_SCOPE",
    "DEFAULT_COMMAND",
    "DEFECT_L1_CONSTANT",
    "DEFECT_L1_RECIPROCAL",
    "GENERATOR_RELATIVE_PATH",
    "LeakyAsyncRoutingTransferCertificate",
    "NOTE_RELATIVE_PATH",
    "OPEN_FLAGS",
    "PROVED_FLAGS",
    "RESULT_RELATIVE_PATH",
    "SCHEMA_ID",
    "SOURCE_RELATIVE_PATH",
    "TEST_RELATIVE_PATH",
    "build_async_routing_transfer_certificate",
    "canonical_sha256",
    "exact_mean_routing_radius_squared",
    "full_history_route_budget_holds",
    "gap_derivative_error_bound",
    "gap_value_error_bound",
    "json_ready_async_routing_transfer",
    "threshold_budget_holds",
    "threshold_shift_bound",
    "validate_async_routing_transfer_result",
]
