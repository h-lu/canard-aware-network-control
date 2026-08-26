"""Uniform nonlinear synchronization inside the validated voltage strip.

The parent certificate proves a Dobrushin--Halanay estimate for transverse
variational equations.  For real network solutions the same constants give
an exact nonlinear oscillation inequality: the instantaneous scalar cubic
has one-sided slope at most ``1-epsilon*kappa_1``, the current delayed cubic
is dissipative, and the delayed cubic is Lipschitz on ``|v-1| <= 5/2``.

The resulting theorem is conditional only on the network solution remaining
in that strip.  It proves topology- and dimension-uniform decay of node-to-
node diameter, but it does not prove forward invariance of the strip, a
uniform basin, an asynchronous canard connection, or physical pulse onset.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from functools import lru_cache
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


SCHEMA_ID = "leaky-dobrushin-nonlinear-synchronization-v1"
SOURCE_RELATIVE_PATH = (
    "src/canard_control/leaky_dobrushin_nonlinear_synchronization.py"
)
GENERATOR_RELATIVE_PATH = (
    "experiments/leaky_dobrushin_nonlinear_synchronization.py"
)
NOTE_RELATIVE_PATH = "docs/leaky-dobrushin-nonlinear-synchronization.md"
RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_dobrushin_nonlinear_synchronization.json"
)
DEFAULT_COMMAND = (
    "PYTHONPATH=src /usr/bin/python3 "
    "experiments/leaky_dobrushin_nonlinear_synchronization.py"
)
ARITHMETIC_SCOPE = (
    "exact real one-sided cubic inequalities and Dobrushin oscillation "
    "calculus, using the source-validated 160-bit Halanay constants; the "
    "solution is assumed to remain in the declared voltage strip"
)

PROVED_FLAGS = (
    "instantaneous_cubic_one_sided_slope_bound_proved",
    "current_delayed_cubic_dissipativity_proved",
    "delayed_cubic_strip_lipschitz_bound_proved",
    "nonlinear_voltage_oscillation_dini_inequality_proved",
    "nonlinear_recovery_oscillation_dini_inequality_proved",
    "nonlinear_weighted_halanay_inequality_proved",
    "conditional_exponential_node_synchronization_proved",
    "decay_rate_uniform_in_finite_network_size_proved",
    "decay_rate_uniform_in_admitted_topology_proved",
)

OPEN_FLAGS = (
    "declared_voltage_strip_forward_invariant_proved",
    "topology_uniform_nonlinear_basin_radius_proved",
    "nonlinear_asynchronous_canard_connection_proved",
    "heterogeneous_node_parameters_covered",
    "asynchronous_physical_pulse_onset_proved",
)


@dataclass(frozen=True)
class LeakyNonlinearSynchronizationCertificate:
    schema_id: str
    model_id: str
    topology_class: str
    solution_scope: str
    real_oscillation: str
    weighted_diameter: str
    voltage_strip: str
    instantaneous_scalar_map: str
    instantaneous_one_sided_slope_upper: str
    delayed_scalar_map: str
    delayed_strip_lipschitz_upper: str
    current_delayed_cubic_sign: str
    nonlinear_voltage_dini_bound: str
    nonlinear_recovery_dini_bound: str
    nonlinear_weighted_halanay_bound: str
    maximum_delay_upper: str
    local_decay_lower: str
    delayed_gain_upper: str
    exponential_rate: str
    rate_residual_lower: str
    synchronization_estimate: str
    uniformity_scope: str
    strict_boundary: str
    instantaneous_cubic_one_sided_slope_bound_proved: bool
    current_delayed_cubic_dissipativity_proved: bool
    delayed_cubic_strip_lipschitz_bound_proved: bool
    nonlinear_voltage_oscillation_dini_inequality_proved: bool
    nonlinear_recovery_oscillation_dini_inequality_proved: bool
    nonlinear_weighted_halanay_inequality_proved: bool
    conditional_exponential_node_synchronization_proved: bool
    decay_rate_uniform_in_finite_network_size_proved: bool
    decay_rate_uniform_in_admitted_topology_proved: bool
    declared_voltage_strip_forward_invariant_proved: bool
    topology_uniform_nonlinear_basin_radius_proved: bool
    nonlinear_asynchronous_canard_connection_proved: bool
    heterogeneous_node_parameters_covered: bool
    asynchronous_physical_pulse_onset_proved: bool


def _mapping(value: Any, label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{label} must be a mapping")
    return value


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


@lru_cache(maxsize=1)
def _validated_parent(repository: Path) -> Mapping[str, Any]:
    parent_path = repository / HALANAY_RESULT_RELATIVE_PATH
    parent = _mapping(json.loads(parent_path.read_bytes()), "Halanay result")
    validate_leaky_dobrushin_transverse_result(parent, repository)
    return parent


def build_nonlinear_synchronization_certificate(
    repository: Path,
) -> LeakyNonlinearSynchronizationCertificate:
    repository = repository.resolve()
    parent = _validated_parent(repository)
    source = _mapping(parent.get("certificate"), "Halanay certificate")
    bounds = _mapping(source.get("bounds"), "Halanay bounds")
    required = (
        "synchronous_restriction_is_exact_scalar_model",
        "dobrushin_oscillation_dini_estimate_proved",
        "balanced_half_mass_delay_bound_proved",
        "exponentially_weighted_history_contraction_proved",
        "arbitrary_finite_network_size_covered",
        "arbitrary_admitted_balanced_topology_covered",
    )
    if any(source.get(name) is not True for name in required):
        raise ValueError("the nonlinear theorem lacks its Halanay parent")

    epsilon = gmpy2.mpq(1, 5)
    kappa_1 = gmpy2.mpq(1, 250)
    kappa_3 = gmpy2.mpq(1, 200)
    radius = gmpy2.mpq(5, 2)
    one_sided = 1 - epsilon * kappa_1
    delayed_lipschitz = 3 * radius * radius
    delayed_gain = epsilon * (kappa_1 + kappa_3 * delayed_lipschitz)
    parent_one_sided = gmpy2.mpq(
        str(bounds["current_voltage_coefficient_upper"])
    )
    parent_delayed_gain = gmpy2.mpq(str(bounds["delayed_total_gain_upper"]))
    tolerance = gmpy2.mpq(1, 10**45)
    if not one_sided <= parent_one_sided < one_sided + tolerance:
        raise ValueError("the nonlinear one-sided slope changed parent constants")
    if not delayed_gain <= parent_delayed_gain < delayed_gain + tolerance:
        raise ValueError("the nonlinear delayed Lipschitz gain changed parent constants")
    if gmpy2.mpq(str(bounds["rate_residual_lower"])) <= 0:
        raise ValueError("the nonlinear Halanay rate has no strict residual")

    values: dict[str, Any] = {name: True for name in PROVED_FLAGS}
    values.update({name: False for name in OPEN_FLAGS})
    return LeakyNonlinearSynchronizationCertificate(
        schema_id=SCHEMA_ID,
        model_id=str(source["model_id"]),
        topology_class=str(source["topology_class"]),
        solution_scope=(
            "every real classical network solution on an interval for which "
            "all node voltages satisfy |v_i(t)-1|<=5/2 on the retained past"
        ),
        real_oscillation="osc(z)=max_i z_i-min_i z_i",
        weighted_diameter="M=max{osc(v),3 osc(w)}",
        voltage_strip="|v_i(t)-1|<=5/2 for every node and retained time",
        instantaneous_scalar_map=(
            "F(s)=s-s^3/3-epsilon*kappa_1*s-"
            "epsilon*kappa_3*(s-1)^3"
        ),
        instantaneous_one_sided_slope_upper=str(
            bounds["current_voltage_coefficient_upper"]
        ),
        delayed_scalar_map="H(s)=(s-1)^3",
        delayed_strip_lipschitz_upper="18.75",
        current_delayed_cubic_sign=(
            "-(H(p)-H(q))*(p-q)<=0 for all real p,q"
        ),
        nonlinear_voltage_dini_bound=(
            "D+ osc(v)<=-alpha_v*M+beta*sup_past(M) whenever "
            "osc(v)=M, with alpha_v=3*(1-tau)-(1-epsilon*kappa_1)-1/3"
        ),
        nonlinear_recovery_dini_bound=(
            "D+[3 osc(w)] <= -alpha_w M whenever 3 osc(w)=M"
        ),
        nonlinear_weighted_halanay_bound=(
            "D+M(t)<=-alpha M(t)+beta sup_{t-r<=s<=t}M(s)"
        ),
        maximum_delay_upper=str(bounds["maximum_delay_upper"]),
        local_decay_lower=str(bounds["local_decay_lower"]),
        delayed_gain_upper=str(bounds["delayed_total_gain_upper"]),
        exponential_rate=str(bounds["exponential_rate"]),
        rate_residual_lower=str(bounds["rate_residual_lower"]),
        synchronization_estimate=(
            "M(t)<=exp(-(t-t0)/10)*sup_{t0-r<=s<=t0}M(s)"
        ),
        uniformity_scope=(
            "constant one and rate 1/10 are independent of every finite N "
            "and every admitted balanced Dobrushin topology in oscillation norm"
        ),
        strict_boundary=(
            "strip residence is a hypothesis; no forward-invariant strip, "
            "uniform basin, heterogeneous-node canard, or asynchronous pulse "
            "threshold follows"
        ),
        **values,
    )


def json_ready_nonlinear_synchronization(repository: Path) -> dict[str, Any]:
    return asdict(build_nonlinear_synchronization_certificate(repository))


def validate_nonlinear_synchronization_result(
    payload: Mapping[str, Any], repository: Path
) -> None:
    if not isinstance(payload, Mapping) or set(payload) != {
        "certificate",
        "manifest",
    }:
        raise ValueError("nonlinear synchronization result requires two records")
    certificate = _mapping(payload.get("certificate"), "certificate")
    manifest = _mapping(payload.get("manifest"), "manifest")
    expected_certificate = json_ready_nonlinear_synchronization(repository)
    if set(certificate) != {field.name for field in fields(LeakyNonlinearSynchronizationCertificate)}:
        raise ValueError("nonlinear synchronization certificate schema changed")
    if certificate != expected_certificate:
        raise ValueError("nonlinear synchronization certificate differs from replay")
    if any(certificate.get(name) is not True for name in PROVED_FLAGS):
        raise ValueError("a nonlinear synchronization theorem flag was weakened")
    if any(certificate.get(name) is not False for name in OPEN_FLAGS):
        raise ValueError("an open nonlinear network claim was promoted")
    sources = {
        "source": SOURCE_RELATIVE_PATH,
        "generator": GENERATOR_RELATIVE_PATH,
        "note": NOTE_RELATIVE_PATH,
        "parent_result": HALANAY_RESULT_RELATIVE_PATH,
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
        raise ValueError("nonlinear synchronization manifest schema changed")
    if manifest.get("schema_id") != SCHEMA_ID:
        raise ValueError("nonlinear synchronization manifest identity changed")
    if manifest.get("certificate_sha256") != canonical_sha256(certificate):
        raise ValueError("nonlinear synchronization certificate digest changed")
    if manifest.get("default_command") != DEFAULT_COMMAND or manifest.get(
        "arithmetic_scope"
    ) != ARITHMETIC_SCOPE:
        raise ValueError("nonlinear synchronization method disclosure changed")
    if manifest.get("python") != platform.python_version() or manifest.get(
        "platform"
    ) != platform.platform():
        raise ValueError("nonlinear synchronization runtime changed")
    for name, relative in sources.items():
        if manifest.get(name) != relative:
            raise ValueError(f"nonlinear synchronization {name} path changed")
        if manifest.get(f"{name}_sha256") != _sha256_path(repository / relative):
            raise ValueError(f"nonlinear synchronization {name} hash changed")


__all__ = [
    "ARITHMETIC_SCOPE",
    "DEFAULT_COMMAND",
    "GENERATOR_RELATIVE_PATH",
    "NOTE_RELATIVE_PATH",
    "RESULT_RELATIVE_PATH",
    "SCHEMA_ID",
    "SOURCE_RELATIVE_PATH",
    "build_nonlinear_synchronization_certificate",
    "canonical_sha256",
    "json_ready_nonlinear_synchronization",
    "validate_nonlinear_synchronization_result",
]
