"""Dobrushin-class transverse decay and local periodic attraction.

This module lifts the validated scalar periodic orbit from the fixed
rank-one witness to every finite balanced topology with a sufficiently
large common Dobrushin gap.  It uses only coefficient bounds already proved
for the synchronous orbit.  The topology argument is analytic: the
executable record checks the directed scalar inequality and one exact
non-rank-one witness, not a finite enumeration of graphs.

The full-network attraction conclusion is restricted to the ``eta=0``
slice of the quadratic period-locked RFDE.  The quadratic carrier has zero
pure-transverse derivative for every eta, but synchronous Floquet stability
has not been validated on a nonzero eta interval.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Mapping

import gmpy2

from canard_control.directed_interval import (
    DirectedInterval,
    decimal_lower,
    decimal_upper,
)
from canard_control.fhn_periodic_transverse_halanay import (
    validate_periodic_transverse_result_payload,
)
from canard_control.fhn_synchronous_floquet_right_half_cover import (
    validate_right_half_cover_payload,
)
from canard_control.quadratic_period_lock_dobrushin_lift import (
    dobrushin_lift_algebra,
    dobrushin_lift_algebra_is_exact,
)


MODEL_ID = (
    "balanced-dobrushin-dual-scaffold-fhn-"
    "quadratic-period-lock-periodic-attraction"
)
TRACKED_TRANSVERSE_RESULT_SHA256 = (
    "ec4b3204695bf40d4309681b0f57d93e3e1e524ca3680cdce316aaee8ad015fb"
)
TRACKED_RIGHT_HALF_RESULT_SHA256 = (
    "6795e6f19f31ffb6bfcf9abd24efb1c5dde4dccf54d896d01298b3e8f9a0d1c3"
)
DEFAULT_TRANSVERSE_RESULT = (
    Path(__file__).resolve().parents[2]
    / "experiments/results/fhn_periodic_transverse_halanay.json"
)
DEFAULT_RIGHT_HALF_RESULT = (
    Path(__file__).resolve().parents[2]
    / "experiments/results/fhn_synchronous_floquet_right_half_cover.json"
)


@dataclass(frozen=True)
class DobrushinHalanayBounds:
    """Directed public endpoints in the weighted oscillation estimate."""

    precision_bits: int
    dobrushin_gap_lower: str
    recovery_weight: str
    current_coefficient_upper: str
    delayed_total_gain_upper: str
    maximum_active_delay_upper: str
    voltage_local_decay_lower: str
    recovery_local_decay_lower: str
    local_decay_lower: str
    zero_rate_margin_lower: str
    exponential_rate_candidate: str
    rate_exponential_upper: str
    rate_residual_lower: str


@dataclass(frozen=True)
class DobrushinPeriodicAttractionCertificate:
    """Strict theorem and scope ledger for the topology lift."""

    model_id: str
    transverse_result_sha256: str
    right_half_result_sha256: str
    topology_class: str
    phase_space_norm: str
    variational_voltage_equation: str
    variational_recovery_equation: str
    halanay_condition: str
    bounds: DobrushinHalanayBounds
    exact_non_rank_one_witness_validated: bool
    transverse_space_invariant: bool
    dobrushin_max_min_dini_bound_proved: bool
    balanced_delay_operator_bound_proved: bool
    quadratic_carrier_pure_transverse_derivative_zero: bool
    enlarged_inert_horizon_adds_only_zero_multipliers_at_eta_zero: bool
    synchronous_nontranslation_unstable_index_zero_source_validated: bool
    synchronous_nonlinear_orbital_attraction_source_validated: bool
    arbitrary_finite_network_size_covered: bool
    arbitrary_admitted_balanced_topology_covered: bool
    uniform_transverse_exponential_rate_validated: bool
    full_network_linear_orbital_attraction_validated: bool
    full_network_nonlinear_local_orbital_attraction_validated: bool
    arbitrary_positive_dobrushin_gap_covered: bool
    nonzero_eta_full_network_attraction_validated: bool
    uniform_nonlinear_basin_over_network_class: bool
    global_synchronization_validated: bool
    biological_pulse_capture_validated: bool


def _mapping(value: Any, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{name} must be a mapping")
    return value


def _require_true(mapping: Mapping[str, Any], name: str) -> None:
    if mapping.get(name) is not True:
        raise ValueError(f"source proof flag {name!r} must be true")


def _require_false(mapping: Mapping[str, Any], name: str) -> None:
    if mapping.get(name) is not False:
        raise ValueError(f"source scope flag {name!r} must be false")


def _load_json_bound(path: str | Path, expected: str, name: str) -> Mapping[str, Any]:
    raw = Path(path).read_bytes()
    actual = sha256(raw).hexdigest()
    if actual != expected:
        raise ValueError(
            f"{name} SHA-256 mismatch: expected {expected}, got {actual}"
        )
    try:
        payload = json.loads(raw)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError(f"{name} is not valid UTF-8 JSON") from error
    return _mapping(payload, name)


def _public_lower(value: gmpy2.mpfr, precision: int) -> tuple[str, gmpy2.mpfr]:
    text = decimal_lower(value, 55)
    return text, DirectedInterval.from_decimal(text, precision).lower


def _public_upper(value: gmpy2.mpfr, precision: int) -> tuple[str, gmpy2.mpfr]:
    text = decimal_upper(value, 55)
    return text, DirectedInterval.from_decimal(text, precision).upper


def directed_dobrushin_halanay_bounds(
    *,
    current_coefficient_upper: str,
    delayed_total_gain_upper: str,
    maximum_active_delay_upper: str,
    gamma: str = "0.75",
    recovery_weight: str = "2.5",
    rate: str = "0.007",
    precision: int = 160,
) -> DobrushinHalanayBounds:
    """Recompose the weighted Halanay inequality with directed rounding.

    For ``X=osc(x)``, ``Y=osc(y)`` and
    ``M=max(X, recovery_weight*Y)``, the local coefficient is

    ``min(3*gamma-g_upper-1/recovery_weight,
          2*gamma-recovery_weight*epsilon)``.

    A strict positive zero-rate margin and rate residual are required.
    """

    if isinstance(precision, bool) or int(precision) != precision or precision < 64:
        raise ValueError("precision must be an integer of at least 64 bits")
    precision = int(precision)
    one = DirectedInterval.from_decimal(1, precision)
    two = DirectedInterval.from_decimal(2, precision)
    three = DirectedInterval.from_decimal(3, precision)
    five = DirectedInterval.from_decimal(5, precision)
    epsilon = one / five
    gap = DirectedInterval.from_decimal(gamma, precision)
    weight = DirectedInterval.from_decimal(recovery_weight, precision)
    rate_interval = DirectedInterval.from_decimal(rate, precision)
    current = DirectedInterval.from_decimal(current_coefficient_upper, precision)
    delayed = DirectedInterval.from_decimal(delayed_total_gain_upper, precision)
    delay = DirectedInterval.from_decimal(maximum_active_delay_upper, precision)
    if gap.lower <= 0 or gap.upper > 1:
        raise ValueError("the Dobrushin gap must lie in (0,1]")
    if weight.lower <= 0 or rate_interval.lower <= 0:
        raise ValueError("the weight and candidate rate must be positive")
    if delayed.lower < 0 or delay.lower <= 0:
        raise ValueError("the delayed gain and active delay must be nonnegative")

    voltage_interval = three * gap - current - one / weight
    recovery_interval = two * gap - weight * epsilon
    voltage_text, public_voltage = _public_lower(voltage_interval.lower, precision)
    recovery_text, public_recovery = _public_lower(
        recovery_interval.lower, precision
    )
    local_raw = min(public_voltage, public_recovery)
    local_text, public_local = _public_lower(local_raw, precision)
    delayed_text, public_delayed = _public_upper(delayed.upper, precision)
    current_text, _ = _public_upper(current.upper, precision)
    delay_text, public_delay = _public_upper(delay.upper, precision)
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        margin_raw = public_local - public_delayed
    margin_text, public_margin = _public_lower(margin_raw, precision)
    if public_margin <= 0:
        raise ValueError("the Dobrushin Halanay zero-rate margin is nonpositive")

    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        exponent_argument = rate_interval.upper * public_delay
        exponential_raw = gmpy2.exp(exponent_argument)
    exponential_text, public_exponential = _public_upper(
        exponential_raw, precision
    )
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        residual_raw = (
            public_local
            - rate_interval.upper
            - public_delayed * public_exponential
        )
    residual_text, public_residual = _public_lower(residual_raw, precision)
    if public_residual <= 0:
        raise ValueError("the proposed Dobrushin Halanay rate is not certified")

    return DobrushinHalanayBounds(
        precision_bits=precision,
        dobrushin_gap_lower=gamma,
        recovery_weight=recovery_weight,
        current_coefficient_upper=current_text,
        delayed_total_gain_upper=delayed_text,
        maximum_active_delay_upper=delay_text,
        voltage_local_decay_lower=voltage_text,
        recovery_local_decay_lower=recovery_text,
        local_decay_lower=local_text,
        zero_rate_margin_lower=margin_text,
        exponential_rate_candidate=rate,
        rate_exponential_upper=exponential_text,
        rate_residual_lower=residual_text,
    )


def dobrushin_periodic_attraction_from_payloads(
    transverse_payload: Mapping[str, Any],
    right_half_payload: Mapping[str, Any],
    *,
    transverse_result_sha256: str,
    right_half_result_sha256: str,
    precision: int = 160,
) -> DobrushinPeriodicAttractionCertificate:
    """Validate both parents and construct the general-topology certificate."""

    if transverse_result_sha256 != TRACKED_TRANSVERSE_RESULT_SHA256:
        raise ValueError("unexpected periodic transverse parent digest")
    if right_half_result_sha256 != TRACKED_RIGHT_HALF_RESULT_SHA256:
        raise ValueError("unexpected synchronous right-half parent digest")
    validate_periodic_transverse_result_payload(transverse_payload)
    validate_right_half_cover_payload(right_half_payload)

    transverse = _mapping(transverse_payload.get("certificate"), "transverse certificate")
    right_half = _mapping(right_half_payload.get("certificate"), "right-half certificate")
    right_source = _mapping(
        right_half_payload.get("source_evidence"), "right-half source evidence"
    )
    for name in (
        "source_periodic_branch_validated",
        "periodic_transverse_variational_decay_validated",
    ):
        _require_true(transverse, name)
    for name in (
        "synchronous_nontranslation_unstable_index_zero_validated",
        "synchronous_linear_orbital_attraction_validated",
        "synchronous_nonlinear_orbital_attraction_validated",
        "hale_verduyn_lunel_hyperbolic_periodic_orbit_theorem_applied",
    ):
        _require_true(right_half, name)
    _require_false(right_half, "general_network_topology_validated")
    if right_source.get("transverse_result_sha256") != transverse_result_sha256:
        raise ValueError("the synchronous and coefficient parents are inconsistent")
    if (
        transverse.get("epsilon") != "0.2"
        or transverse.get("voltage_scaffold") != "3"
        or transverse.get("recovery_scaffold") != "2"
    ):
        raise ValueError("unexpected periodic FHN normalization")

    for field in (
        "current_coefficient_global_maximum_upper",
        "delayed_total_gain_upper",
        "maximum_delay_upper",
    ):
        if not isinstance(transverse.get(field), str):
            raise ValueError(f"transverse coefficient {field!r} is missing")
    bounds = directed_dobrushin_halanay_bounds(
        current_coefficient_upper=transverse[
            "current_coefficient_global_maximum_upper"
        ],
        delayed_total_gain_upper=transverse["delayed_total_gain_upper"],
        maximum_active_delay_upper=transverse["maximum_delay_upper"],
        precision=precision,
    )
    witness = dobrushin_lift_algebra()
    if not dobrushin_lift_algebra_is_exact(witness):
        raise RuntimeError("the non-rank-one Dobrushin witness is not exact")

    return DobrushinPeriodicAttractionCertificate(
        model_id=MODEL_ID,
        transverse_result_sha256=transverse_result_sha256,
        right_half_result_sha256=right_half_result_sha256,
        topology_class=(
            "every finite nonnegative row-stochastic Q with positive stationary "
            "pi, tau(Q)<=1/4, and nonnegative balanced half-mass B0,B1"
        ),
        phase_space_norm=(
            "max{osc(x), (5/2)*osc(y)} on ker(pi^T) x ker(pi^T), "
            "with the corresponding history supremum"
        ),
        variational_voltage_equation=(
            "x'=(g(t)I+3(Q-I))x-y+r0(t)B0*x_tau0+"
            "r1(t)B1*x_tau1"
        ),
        variational_recovery_equation="y'=epsilon*x+2(Q-I)y",
        halanay_condition=(
            "min{3*gamma-g_upper-1/c, 2*gamma-c*epsilon}>beta"
        ),
        bounds=bounds,
        exact_non_rank_one_witness_validated=True,
        transverse_space_invariant=True,
        dobrushin_max_min_dini_bound_proved=True,
        balanced_delay_operator_bound_proved=True,
        quadratic_carrier_pure_transverse_derivative_zero=True,
        enlarged_inert_horizon_adds_only_zero_multipliers_at_eta_zero=True,
        synchronous_nontranslation_unstable_index_zero_source_validated=True,
        synchronous_nonlinear_orbital_attraction_source_validated=True,
        arbitrary_finite_network_size_covered=True,
        arbitrary_admitted_balanced_topology_covered=True,
        uniform_transverse_exponential_rate_validated=True,
        full_network_linear_orbital_attraction_validated=True,
        full_network_nonlinear_local_orbital_attraction_validated=True,
        arbitrary_positive_dobrushin_gap_covered=False,
        nonzero_eta_full_network_attraction_validated=False,
        uniform_nonlinear_basin_over_network_class=False,
        global_synchronization_validated=False,
        biological_pulse_capture_validated=False,
    )


def load_dobrushin_periodic_attraction(
    transverse_path: str | Path = DEFAULT_TRANSVERSE_RESULT,
    right_half_path: str | Path = DEFAULT_RIGHT_HALF_RESULT,
    *,
    precision: int = 160,
) -> DobrushinPeriodicAttractionCertificate:
    """Load both byte-bound parent proofs and derive the certificate."""

    transverse = _load_json_bound(
        transverse_path,
        TRACKED_TRANSVERSE_RESULT_SHA256,
        "periodic transverse result",
    )
    right_half = _load_json_bound(
        right_half_path,
        TRACKED_RIGHT_HALF_RESULT_SHA256,
        "synchronous right-half result",
    )
    return dobrushin_periodic_attraction_from_payloads(
        transverse,
        right_half,
        transverse_result_sha256=TRACKED_TRANSVERSE_RESULT_SHA256,
        right_half_result_sha256=TRACKED_RIGHT_HALF_RESULT_SHA256,
        precision=precision,
    )


def reference_dobrushin_periodic_payload() -> dict[str, Any]:
    """Serialize the proved theorem and every refusal boundary."""

    certificate = load_dobrushin_periodic_attraction()
    return {
        "certificate": asdict(certificate),
        "scope": {
            "eta_zero_quadratic_period_locked_model": True,
            "uniform_dobrushin_gap_at_least_three_quarters": True,
            "arbitrary_finite_admitted_balanced_topology": True,
            "uniform_transverse_rate": True,
            "full_network_local_nonlinear_orbital_attraction": True,
            "arbitrary_positive_dobrushin_gap": False,
            "nonzero_eta_full_network_attraction": False,
            "uniform_nonlinear_basin": False,
            "global_synchronization": False,
            "biological_pulse_capture": False,
        },
        "source_evidence": {
            "periodic_transverse_result_sha256": (
                TRACKED_TRANSVERSE_RESULT_SHA256
            ),
            "synchronous_right_half_result_sha256": (
                TRACKED_RIGHT_HALF_RESULT_SHA256
            ),
        },
    }


def validate_dobrushin_periodic_payload(payload: Mapping[str, Any]) -> None:
    """Reject numerical drift and every unsupported promotion."""

    expected = reference_dobrushin_periodic_payload()
    for section in ("certificate", "scope", "source_evidence"):
        actual = dict(_mapping(payload.get(section), section))
        if actual != expected[section]:
            raise ValueError(f"the Dobrushin periodic {section} changed")
