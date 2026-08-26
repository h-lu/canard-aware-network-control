"""Quadratic collective defect for the finite leaky Dobrushin network.

The nonlinear synchronization theorem controls node diameter but does not,
by itself, control the collective coordinate.  Balance gives an exact mean
equation: the pi-weighted network mean solves the scalar leaky RFDE plus a
single voltage forcing.  Taylor cancellation of the weighted first-order
term makes that forcing quadratic in node diameter.

Combining the exact quadratic bound with the proved stripwise exponential
synchronization makes the forcing integrable with constants independent of
finite network size and admitted topology.  The delayed Taylor remainders
are evaluated at ``t-tau_j``; their initial-history residence is retained
explicitly.  No invariant strip, scalar shadowing tube, asynchronous
threshold, or routed basin conclusion is made.
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

from canard_control.directed_interval import DirectedInterval
from canard_control.leaky_dobrushin_nonlinear_synchronization import (
    RESULT_RELATIVE_PATH as SYNCHRONIZATION_RESULT_RELATIVE_PATH,
    validate_nonlinear_synchronization_result,
)


SCHEMA_ID = "leaky-dobrushin-collective-defect-v2"
SOURCE_RELATIVE_PATH = (
    "src/canard_control/leaky_dobrushin_collective_defect.py"
)
GENERATOR_RELATIVE_PATH = (
    "experiments/leaky_dobrushin_collective_defect.py"
)
NOTE_RELATIVE_PATH = "docs/leaky-dobrushin-collective-defect.md"
TEST_RELATIVE_PATH = "tests/test_leaky_dobrushin_collective_defect.py"
RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_dobrushin_collective_defect.json"
)
DEFAULT_COMMAND = (
    "PYTHONPATH=src /usr/bin/python3 "
    "experiments/leaky_dobrushin_collective_defect.py"
)
ARITHMETIC_SCOPE = (
    "exact rational balance and weighted Taylor bounds on "
    "|v_i-1|<=5/2, with both delayed evaluation times and their exact "
    "4*sqrt(5),5*sqrt(5) initial-history residence retained; 160-bit "
    "outward evaluation of the resulting algebraic accumulated constant, "
    "composed with the source-validated nonlinear synchronization estimate"
)

PROVED_FLAGS = (
    "balanced_collective_mean_equation_proved",
    "linear_collective_terms_cancel_exactly",
    "weighted_first_order_taylor_terms_cancel_exactly",
    "quadratic_collective_defect_bound_proved",
    "delayed_history_residence_accounted_exactly",
    "conditional_integrable_collective_defect_proved",
    "defect_constants_uniform_in_finite_network_size_proved",
    "defect_constants_uniform_in_admitted_topology_proved",
)

OPEN_FLAGS = (
    "declared_voltage_strip_forward_invariant_proved",
    "collective_scalar_shadowing_tube_proved",
    "topology_uniform_asynchronous_threshold_radius_proved",
    "asynchronous_two_sided_basin_routing_proved",
    "heterogeneous_node_parameters_covered",
)


@dataclass(frozen=True)
class LeakyCollectiveDefectCertificate:
    schema_id: str
    model_id: str
    topology_class: str
    collective_coordinates: str
    scalar_maps: str
    exact_collective_voltage_equation: str
    exact_collective_recovery_equation: str
    exact_defect_formula: str
    voltage_strip: str
    instantaneous_second_derivative_upper: str
    delayed_second_derivative_upper: str
    weighted_taylor_remainder_rule: str
    pointwise_defect_constant_exact: str
    pointwise_defect_constant_decimal: str
    pointwise_defect_estimate: str
    synchronization_rate_exact: str
    conditional_diameter_estimate: str
    retained_history_diameter_envelope: str
    componentwise_pointwise_defect_estimate: str
    conditional_defect_decay_estimate: str
    accumulated_defect_constant_exact: str
    accumulated_defect_constant_decimal: str
    accumulated_defect_constant_rational_upper: str
    delayed_history_residence_correction_exact: str
    conditional_accumulated_defect_estimate: str
    uniformity_scope: str
    strict_boundary: str
    balanced_collective_mean_equation_proved: bool
    linear_collective_terms_cancel_exactly: bool
    weighted_first_order_taylor_terms_cancel_exactly: bool
    quadratic_collective_defect_bound_proved: bool
    delayed_history_residence_accounted_exactly: bool
    conditional_integrable_collective_defect_proved: bool
    defect_constants_uniform_in_finite_network_size_proved: bool
    defect_constants_uniform_in_admitted_topology_proved: bool
    declared_voltage_strip_forward_invariant_proved: bool
    collective_scalar_shadowing_tube_proved: bool
    topology_uniform_asynchronous_threshold_radius_proved: bool
    asynchronous_two_sided_basin_routing_proved: bool
    heterogeneous_node_parameters_covered: bool


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


def _clear_parent_validation_caches() -> None:
    """Force the formal validator to replay the live parent dependency tree.

    The parent modules cache expensive directed reconstructions for ordinary
    builds.  A validator must not let a warm cache hide a later mutation of a
    parent result or any source bound by that parent, so the security boundary
    clears the relevant transitive caches before rebuilding this certificate.
    """

    from canard_control import leaky_dobrushin_nonlinear_synchronization as sync
    from canard_control import leaky_dobrushin_transverse_halanay as halanay

    _validated_parent.cache_clear()
    sync._validated_parent.cache_clear()
    halanay._validated_floquet_payload.cache_clear()
    halanay.build_leaky_dobrushin_transverse_certificate.cache_clear()


@lru_cache(maxsize=1)
def _validated_parent(repository: Path) -> Mapping[str, Any]:
    path = repository / SYNCHRONIZATION_RESULT_RELATIVE_PATH
    payload = _mapping(json.loads(path.read_bytes()), "synchronization result")
    validate_nonlinear_synchronization_result(payload, repository)
    return payload


def build_collective_defect_certificate(
    repository: Path,
) -> LeakyCollectiveDefectCertificate:
    repository = repository.resolve()
    parent = _validated_parent(repository)
    synchronization = _mapping(
        parent.get("certificate"), "synchronization certificate"
    )
    required = (
        "conditional_exponential_node_synchronization_proved",
        "decay_rate_uniform_in_finite_network_size_proved",
        "decay_rate_uniform_in_admitted_topology_proved",
    )
    if any(synchronization.get(name) is not True for name in required):
        raise ValueError("collective defect lacks its synchronization parent")
    if synchronization.get("voltage_strip") != (
        "|v_i(t)-1|<=5/2 for every node and retained time"
    ):
        raise ValueError("the parent voltage strip changed")

    epsilon = gmpy2.mpq(1, 5)
    kappa_3 = gmpy2.mpq(1, 200)
    strip_abs_voltage = gmpy2.mpq(7, 2)
    strip_abs_shift = gmpy2.mpq(5, 2)
    f_second = 2 * strip_abs_voltage
    h_second = 6 * strip_abs_shift
    taylor_factor = gmpy2.mpq(1, 2)
    delayed_absolute_mass = gmpy2.mpq(1, 2) + gmpy2.mpq(1, 2) + 1
    defect_constant = (
        taylor_factor * f_second
        + epsilon
        * kappa_3
        * delayed_absolute_mass
        * taylor_factor
        * h_second
    )
    expected_defect = gmpy2.mpq(703, 200)
    if defect_constant != expected_defect:
        raise ArithmeticError("the collective defect constant changed")

    rate = gmpy2.mpq(1, 10)
    current_quadratic = gmpy2.mpq(1403, 400)
    each_delayed_quadratic = gmpy2.mpq(3, 800)
    if current_quadratic + 2 * each_delayed_quadratic != defect_constant:
        raise ArithmeticError("the pointwise delayed decomposition changed")
    # The common ``5=1/(2*rate)`` contribution comes from integrating the
    # squared post-t0 decay.  Each delayed Taylor remainder additionally
    # reads an arbitrary retained history for exactly tau_j units of time.
    base_accumulated = defect_constant / (2 * rate)
    if base_accumulated != gmpy2.mpq(703, 40):
        raise ArithmeticError("the no-residence accumulated constant changed")
    tau_0_coefficient = gmpy2.mpq(3, 800) * 4
    tau_1_coefficient = gmpy2.mpq(3, 800) * 5
    if tau_0_coefficient + tau_1_coefficient != gmpy2.mpq(27, 800):
        raise ArithmeticError("the delayed residence coefficient changed")
    residence_correction = "27*sqrt(5)/800"
    precision = 160
    sqrt_five = DirectedInterval.from_decimal(5, precision).sqrt()
    accumulated_interval = (
        DirectedInterval.from_decimal(703, precision) / 40
        + (DirectedInterval.from_decimal(27, precision) * sqrt_five) / 800
    )
    rational_upper = gmpy2.mpq(56483, 3200)
    if accumulated_interval.upper >= rational_upper:
        raise ArithmeticError("the rational residence upper bound no longer closes")

    values: dict[str, Any] = {name: True for name in PROVED_FLAGS}
    values.update({name: False for name in OPEN_FLAGS})
    return LeakyCollectiveDefectCertificate(
        schema_id=SCHEMA_ID,
        model_id=str(synchronization["model_id"]),
        topology_class=str(synchronization["topology_class"]),
        collective_coordinates=(
            "bar_v=pi^T v, bar_w=pi^T w, with pi^T 1=1"
        ),
        scalar_maps="f(s)=s-s^3/3 and H(s)=(s-1)^3",
        exact_collective_voltage_equation=(
            "bar_v'=f(bar_v)-bar_w+epsilon*kappa_1*"
            "(bar_v_tau0/2+bar_v_tau1/2-bar_v)+epsilon*kappa_3*"
            "(H(bar_v_tau0)/2+H(bar_v_tau1)/2-H(bar_v))+R_coll"
        ),
        exact_collective_recovery_equation=(
            "bar_w'=epsilon*(bar_v-a-bar_w)"
        ),
        exact_defect_formula=(
            "R_coll=pi^T f(v)-f(bar_v)+epsilon*kappa_3*"
            "{[pi^T H(v_tau0)-H(bar_v_tau0)]/2+"
            "[pi^T H(v_tau1)-H(bar_v_tau1)]/2-"
            "[pi^T H(v)-H(bar_v)]}"
        ),
        voltage_strip="|v_i-1|<=5/2, hence |v_i|<=7/2",
        instantaneous_second_derivative_upper=str(f_second),
        delayed_second_derivative_upper=str(h_second),
        weighted_taylor_remainder_rule=(
            "|sum_i pi_i g(x_i)-g(sum_i pi_i x_i)| <= "
            "sup|g''|*osc(x)^2/2"
        ),
        pointwise_defect_constant_exact=str(defect_constant),
        pointwise_defect_constant_decimal="3.515",
        pointwise_defect_estimate=(
            "|R_coll(t)|<=(703/200)*H_M(t)^2, where "
            "H_M(t)=sup_[t-r,t] M(s)"
        ),
        synchronization_rate_exact=str(rate),
        conditional_diameter_estimate=(
            "M(t)<=M0*exp(-(t-t0)/10) while the retained solution "
            "remains in the strip"
        ),
        retained_history_diameter_envelope=(
            "H_M(t)=sup_{t-r<=s<=t}M(s), with "
            "M0=sup_{t0-r<=s<=t0}M(s)"
        ),
        componentwise_pointwise_defect_estimate=(
            "|R_coll(t)|<=(1403/400)*M(t)^2+"
            "(3/800)*(M(t-tau0)^2+M(t-tau1)^2)"
        ),
        conditional_defect_decay_estimate=(
            "the current term decays from t0; each delayed term retains "
            "M0 on [t0,t0+tau_j] and then decays at squared rate 1/5"
        ),
        accumulated_defect_constant_exact=(
            "703/40+27*sqrt(5)/800"
        ),
        accumulated_defect_constant_decimal=str(accumulated_interval.upper),
        accumulated_defect_constant_rational_upper=str(rational_upper),
        delayed_history_residence_correction_exact=residence_correction,
        conditional_accumulated_defect_estimate=(
            "integral_{t0}^infinity |R_coll(t)|dt <= "
            "(703/40+27*sqrt(5)/800)*M0^2 <= (56483/3200)*M0^2"
        ),
        uniformity_scope=(
            "the pointwise and accumulated constants are independent of "
            "every finite N, pi_min, and every admitted balanced "
            "Dobrushin topology"
        ),
        strict_boundary=(
            "strip residence remains a hypothesis; integrable forcing is "
            "not itself a scalar shadowing tube, threshold, or basin route"
        ),
        **values,
    )


def json_ready_collective_defect(repository: Path) -> dict[str, Any]:
    return asdict(build_collective_defect_certificate(repository))


def validate_collective_defect_result(
    payload: Mapping[str, Any], repository: Path
) -> None:
    _clear_parent_validation_caches()
    if not isinstance(payload, Mapping) or set(payload) != {
        "certificate",
        "manifest",
    }:
        raise ValueError("collective defect result requires two records")
    certificate = _mapping(payload.get("certificate"), "certificate")
    manifest = _mapping(payload.get("manifest"), "manifest")
    if set(certificate) != {
        field.name for field in fields(LeakyCollectiveDefectCertificate)
    }:
        raise ValueError("collective defect certificate schema changed")
    if any(certificate.get(name) is not True for name in PROVED_FLAGS):
        raise ValueError("a collective defect theorem flag was weakened")
    if any(certificate.get(name) is not False for name in OPEN_FLAGS):
        raise ValueError("an open collective defect claim was promoted")
    if certificate.get("accumulated_defect_constant_exact") != (
        "703/40+27*sqrt(5)/800"
    ) or certificate.get("accumulated_defect_constant_rational_upper") != (
        "56483/3200"
    ):
        raise ValueError("the delayed-history accumulated constant changed")
    if "H_M(t)^2" not in str(certificate.get("pointwise_defect_estimate")):
        raise ValueError("the retained-history pointwise envelope changed")

    sources = {
        "source": SOURCE_RELATIVE_PATH,
        "generator": GENERATOR_RELATIVE_PATH,
        "note": NOTE_RELATIVE_PATH,
        "test": TEST_RELATIVE_PATH,
        "parent_result": SYNCHRONIZATION_RESULT_RELATIVE_PATH,
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
        raise ValueError("collective defect manifest schema changed")
    if manifest.get("schema_id") != SCHEMA_ID:
        raise ValueError("collective defect manifest identity changed")
    if manifest.get("certificate_sha256") != canonical_sha256(certificate):
        raise ValueError("collective defect certificate digest changed")
    if manifest.get("default_command") != DEFAULT_COMMAND or manifest.get(
        "arithmetic_scope"
    ) != ARITHMETIC_SCOPE:
        raise ValueError("collective defect method disclosure changed")
    if manifest.get("python") != platform.python_version() or manifest.get(
        "platform"
    ) != platform.platform():
        raise ValueError("collective defect runtime changed")
    for name, relative in sources.items():
        if manifest.get(name) != relative:
            raise ValueError(f"collective defect {name} path changed")
        if manifest.get(f"{name}_sha256") != _sha256_path(repository / relative):
            raise ValueError(f"collective defect {name} hash changed")
    expected = json_ready_collective_defect(repository)
    if certificate != expected:
        raise ValueError("collective defect certificate differs from replay")


__all__ = [
    "ARITHMETIC_SCOPE",
    "DEFAULT_COMMAND",
    "GENERATOR_RELATIVE_PATH",
    "LeakyCollectiveDefectCertificate",
    "NOTE_RELATIVE_PATH",
    "OPEN_FLAGS",
    "PROVED_FLAGS",
    "RESULT_RELATIVE_PATH",
    "SCHEMA_ID",
    "SOURCE_RELATIVE_PATH",
    "TEST_RELATIVE_PATH",
    "build_collective_defect_certificate",
    "canonical_sha256",
    "json_ready_collective_defect",
    "validate_collective_defect_result",
]
