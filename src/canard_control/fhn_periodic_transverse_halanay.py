"""Directed transverse Halanay certificate along the periodic FHN branch.

The synchronous periodic-orbit certificate controls the coefficient

``H(t) = epsilon/2 * (kappa_1 + 3*kappa_3*(V(t)-1)**2)``

in the Wiener norm on the entire microscopic gain box.  This module combines
that bound with the exact modal decomposition of the frozen rank-one
two-module topology and fixed instantaneous scaffolds ``D=3`` and ``E=2``.

For every transverse mode, in the unweighted max norm of voltage and
recovery perturbations, the local decay is bounded below by

``alpha = min(D-g_max-1, E-epsilon)``,

where the global concave-quadratic bound is

``g_max = 1-epsilon*kappa_1-q/(1+q)``, ``q=3*epsilon*kappa_3``.

The two delayed layers have total gain at most ``beta=2*||H||``.  A strict
``alpha>beta`` therefore gives size-uniform exponential decay by Halanay's
inequality.  Together with the already validated synchronous Floquet
exclusion, this proves full-network orbital hyperbolicity for arbitrary
positive module sizes in this *fixed rank-one two-module topology*.  It does
not prove synchronous attraction, nonlinear synchronization, or a theorem
for general topology.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Mapping

import gmpy2
import sympy as sp

from canard_control.directed_interval import (
    DirectedInterval,
    decimal_lower,
    decimal_upper,
)
from canard_control.full_network_blocks import (
    two_module_block_algebra,
    uniform_history_layer,
)
from canard_control.reference_fhn import symmetric_reference_algebra


TRACKED_PARAMETER_BOX_SHA256 = (
    "ff13b5352c2b4e9898a4044be63fd490a3e7bb4217445a6a062188c2457c22a0"
)
TRACKED_BLOCH_RESULT_SHA256 = (
    "c2f93b6cfe6a8e0df3b341476fbe45a83f6fecc0398dbb7340a5213a55357a31"
)
MODEL_ID = "dual-scaffold-rank-one-two-module-fhn-two-delay"


@dataclass(frozen=True)
class PeriodicTransverseAlgebra:
    """Exact identities behind the coefficient and modal estimates."""

    completed_square_residual: sp.Expr
    same_delay_collective_residual: sp.Matrix
    same_delay_difference_residual: sp.Matrix
    cross_delay_collective_residual: sp.Matrix
    cross_delay_difference_residual: sp.Matrix


@dataclass(frozen=True)
class PeriodicTransverseNetworkAlgebra:
    """Exact node-level lift, within-mode, and scaffold identities."""

    n1: int
    n2: int
    delay_sum_projection_residual: sp.Matrix
    modal_rank: int
    collective_same_delay_residual: sp.Matrix
    collective_cross_delay_residual: sp.Matrix
    difference_same_delay_residual: sp.Matrix
    difference_cross_delay_residual: sp.Matrix
    within_same_delay_residual: sp.Matrix
    within_cross_delay_residual: sp.Matrix
    collective_scaffold_residual: sp.Matrix
    transverse_voltage_scaffold_residual: sp.Matrix
    transverse_recovery_scaffold_residual: sp.Matrix
    reference_projection_residual: sp.Matrix
    reference_collective_residual: sp.Matrix
    reference_difference_residual: sp.Matrix


@dataclass(frozen=True)
class PeriodicTransverseHalanayCertificate:
    """Public theorem endpoints recomposed from serialized parent bounds."""

    parameter_box_result_sha256: str
    bloch_result_sha256: str
    precision_bits: int
    model_id: str
    topology: str
    epsilon: str
    voltage_scaffold: str
    recovery_scaffold: str
    max_norm_weight: str
    gain_half_width: str
    kappa_1_interval: tuple[str, str]
    kappa_3_interval: tuple[str, str]
    maximum_delay_upper: str
    current_coefficient_global_maximum_upper: str
    delayed_each_wiener_norm_upper: str
    delayed_total_gain_upper: str
    voltage_local_decay_lower: str
    recovery_local_decay_lower: str
    halanay_local_decay_lower: str
    halanay_margin_lower: str
    halanay_rate_candidate: str
    halanay_rate_exponential_upper: str
    halanay_rate_residual_lower: str
    exact_rank_one_modal_decomposition_validated: bool
    representative_full_node_delay_layer_audits_validated: bool
    within_module_delay_annihilation_validated: bool
    instantaneous_scaffold_modal_action_validated: bool
    full_node_audit_module_sizes: tuple[tuple[int, int], ...]
    arbitrary_size_quantifier_from_enumeration: bool
    arbitrary_positive_module_sizes_formulaic_theorem: bool
    source_periodic_branch_validated: bool
    source_synchronous_orbital_hyperbolicity_validated: bool
    periodic_transverse_variational_decay_validated: bool
    full_network_orbital_hyperbolicity_validated: bool
    synchronous_attraction_validated: bool
    full_network_attraction_validated: bool
    nonlinear_synchronization_validated: bool
    general_network_topology_validated: bool
    physical_pulse_onset_validated: bool
    issue_15_closed: bool


def periodic_transverse_algebra() -> PeriodicTransverseAlgebra:
    """Return exact completed-square and two-module delay-mode identities."""

    v, q = sp.symbols("v q", real=True)
    completed = sp.simplify(
        v**2 + q * (v - 1) ** 2
        - ((1 + q) * (v - q / (1 + q)) ** 2 + q / (1 + q))
    )
    collective = sp.Matrix([1, 1])
    difference = sp.Matrix([1, -1])
    same = sp.eye(2) / 2
    cross = sp.Matrix([[0, 1], [1, 0]]) / 2
    return PeriodicTransverseAlgebra(
        completed_square_residual=completed,
        same_delay_collective_residual=sp.simplify(
            same * collective - collective / 2
        ),
        same_delay_difference_residual=sp.simplify(
            same * difference - difference / 2
        ),
        cross_delay_collective_residual=sp.simplify(
            cross * collective - collective / 2
        ),
        cross_delay_difference_residual=sp.simplify(
            cross * difference + difference / 2
        ),
    )


def periodic_transverse_network_algebra(
    n1: int,
    n2: int,
) -> PeriodicTransverseNetworkAlgebra:
    """Audit the exact node lift for any declared positive module sizes.

    The construction in :func:`two_module_block_algebra` is formulaic in
    ``n1,n2``.  This routine checks the lifted same/cross delay layers,
    their annihilation of every within-module zero-mean column, and the
    action of both instantaneous scaffolds on the complete transverse basis.
    """

    algebra = two_module_block_algebra(n1, n2)
    same_module = sp.eye(2) / 2
    cross_module = sp.Matrix([[0, 1], [1, 0]]) / 2
    same = uniform_history_layer(algebra, same_module)
    cross = uniform_history_layer(algebra, cross_module)
    projection = algebra.collective_projector
    identity = sp.eye(algebra.node_count)
    collective = algebra.collective_vector
    difference = algebra.module_difference_vector
    within = algebra.within_basis
    transverse = sp.Matrix.hstack(difference, within)
    voltage_scaffold = sp.Integer(3) * (projection - identity)
    recovery_scaffold = sp.Integer(2) * (projection - identity)
    reference = symmetric_reference_algebra(n1, n2)
    return PeriodicTransverseNetworkAlgebra(
        n1=n1,
        n2=n2,
        delay_sum_projection_residual=sp.ImmutableMatrix(
            same + cross - projection
        ),
        modal_rank=int(algebra.modal_basis.rank()),
        collective_same_delay_residual=sp.ImmutableMatrix(
            same * collective - collective / 2
        ),
        collective_cross_delay_residual=sp.ImmutableMatrix(
            cross * collective - collective / 2
        ),
        difference_same_delay_residual=sp.ImmutableMatrix(
            same * difference - difference / 2
        ),
        difference_cross_delay_residual=sp.ImmutableMatrix(
            cross * difference + difference / 2
        ),
        within_same_delay_residual=sp.ImmutableMatrix(same * within),
        within_cross_delay_residual=sp.ImmutableMatrix(cross * within),
        collective_scaffold_residual=sp.ImmutableMatrix(
            (projection - identity) * collective
        ),
        transverse_voltage_scaffold_residual=sp.ImmutableMatrix(
            voltage_scaffold * transverse + 3 * transverse
        ),
        transverse_recovery_scaffold_residual=sp.ImmutableMatrix(
            recovery_scaffold * transverse + 2 * transverse
        ),
        reference_projection_residual=sp.ImmutableMatrix(
            reference.averaging_matrix - projection
        ),
        reference_collective_residual=sp.ImmutableMatrix(
            reference.collective_residual
        ),
        reference_difference_residual=sp.ImmutableMatrix(
            reference.difference_residual
        ),
    )


def _network_algebra_is_exact(
    audit: PeriodicTransverseNetworkAlgebra,
) -> bool:
    node_count = audit.n1 + audit.n2
    within_count = node_count - 2
    return (
        audit.delay_sum_projection_residual == sp.zeros(node_count)
        and audit.modal_rank == node_count
        and audit.collective_same_delay_residual == sp.zeros(node_count, 1)
        and audit.collective_cross_delay_residual == sp.zeros(node_count, 1)
        and audit.difference_same_delay_residual == sp.zeros(node_count, 1)
        and audit.difference_cross_delay_residual == sp.zeros(node_count, 1)
        and audit.within_same_delay_residual
        == sp.zeros(node_count, within_count)
        and audit.within_cross_delay_residual
        == sp.zeros(node_count, within_count)
        and audit.collective_scaffold_residual == sp.zeros(node_count, 1)
        and audit.transverse_voltage_scaffold_residual
        == sp.zeros(node_count, node_count - 1)
        and audit.transverse_recovery_scaffold_residual
        == sp.zeros(node_count, node_count - 1)
        and audit.reference_projection_residual == sp.zeros(node_count)
        and audit.reference_collective_residual == sp.zeros(node_count, 1)
        and audit.reference_difference_residual == sp.zeros(node_count, 1)
    )
def _mapping(value: object, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{name} must be a mapping")
    return value


def _require_true(mapping: Mapping[str, Any], name: str) -> None:
    if mapping.get(name) is not True:
        raise ValueError(f"source proof flag {name!r} must be true")


def _require_false(mapping: Mapping[str, Any], name: str) -> None:
    if mapping.get(name) is not False:
        raise ValueError(f"source scope flag {name!r} must be false")


def _pair(interval: DirectedInterval) -> tuple[str, str]:
    return decimal_lower(interval.lower, 55), decimal_upper(interval.upper, 55)


def _public_lower(value: gmpy2.mpfr, precision: int) -> tuple[str, gmpy2.mpfr]:
    text = decimal_lower(value, 55)
    return text, DirectedInterval.from_decimal(text, precision).lower


def _public_upper(value: gmpy2.mpfr, precision: int) -> tuple[str, gmpy2.mpfr]:
    text = decimal_upper(value, 55)
    return text, DirectedInterval.from_decimal(text, precision).upper


def _exp_upper(value: gmpy2.mpfr, precision: int) -> gmpy2.mpfr:
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        return gmpy2.exp(value)


def periodic_transverse_halanay_from_payloads(
    parameter_payload: Mapping[str, Any],
    bloch_payload: Mapping[str, Any],
    *,
    parameter_box_result_sha256: str,
    bloch_result_sha256: str,
    precision: int = 160,
) -> PeriodicTransverseHalanayCertificate:
    """Validate source semantics and derive the periodic transverse bound.

    The two digest arguments are provenance at this low level.  They are not
    recomputed from already-decoded mappings; use
    :func:`load_periodic_transverse_halanay` for the byte-hash-checked path.
    This function remains public so refusal tests can mutate individual
    semantic fields without manufacturing colliding files.
    """

    for digest, name in (
        (parameter_box_result_sha256, "parameter_box_result_sha256"),
        (bloch_result_sha256, "bloch_result_sha256"),
    ):
        if not isinstance(digest, str) or len(digest) != 64:
            raise ValueError(f"{name} must be a 64-character digest")
        try:
            int(digest, 16)
        except ValueError as error:
            raise ValueError(f"{name} must be hexadecimal") from error
    if parameter_box_result_sha256 != TRACKED_PARAMETER_BOX_SHA256:
        raise ValueError("parameter record is not the tracked microscopic box")
    if bloch_result_sha256 != TRACKED_BLOCH_RESULT_SHA256:
        raise ValueError("Bloch record is not the tracked Floquet theorem")
    if (
        isinstance(precision, bool)
        or int(precision) != precision
        or int(precision) < 64
    ):
        raise ValueError("precision must be an integer of at least 64 bits")
    precision = int(precision)

    parameter_root = _mapping(parameter_payload, "parameter payload")
    validation = _mapping(parameter_root.get("validation"), "validation")
    gain_box = _mapping(validation.get("gain_box"), "validation.gain_box")
    _require_true(validation, "d1_validated")
    continuation = _mapping(
        validation.get("continuation"), "validation.continuation"
    )
    _require_true(continuation, "parameter_box_orbit_validated")
    if gain_box.get("half_width") != "1e-12":
        raise ValueError("unexpected gain half-width")
    gain_fields = (
        "kappa_1_lower",
        "kappa_1_upper",
        "kappa_3_lower",
        "kappa_3_upper",
    )
    if any(not isinstance(gain_box.get(name), str) for name in gain_fields):
        raise ValueError("gain endpoints must be directed decimal strings")
    kappa_1 = DirectedInterval.from_bounds(
        gain_box["kappa_1_lower"], gain_box["kappa_1_upper"], precision
    )
    kappa_3 = DirectedInterval.from_bounds(
        gain_box["kappa_3_lower"], gain_box["kappa_3_upper"], precision
    )
    if kappa_1.lower <= 0 or kappa_3.lower <= 0:
        raise ValueError("the transverse theorem requires positive gains")

    bloch_root = _mapping(bloch_payload, "Bloch payload")
    local = _mapping(bloch_root.get("local_transfer"), "local_transfer")
    source = _mapping(bloch_root.get("source_evidence"), "source_evidence")
    scope = _mapping(bloch_root.get("scope"), "scope")
    if source.get("parameter_box_result_sha256") != parameter_box_result_sha256:
        raise ValueError("Bloch and parameter records use different branches")
    _require_true(source, "periodic_branch_validated")
    _require_true(scope, "synchronous_orbital_hyperbolicity")
    _require_false(scope, "attraction")
    _require_false(scope, "full_network_transverse_stability")
    _require_true(local, "regularity_bridge_to_history_monodromy")
    _require_true(local, "monodromy_compact")
    if local.get("norm_id") != (
        "complexification-of-real-conjugate-component-wiener-l1"
    ):
        raise ValueError("unexpected source coefficient norm")
    delayed_text = local.get("delayed_coefficient_uniform_norm_upper")
    delay_text = local.get("maximum_delay_upper")
    if not isinstance(delayed_text, str) or not isinstance(delay_text, str):
        raise ValueError("source coefficient and delay bounds must be strings")
    delayed_each = DirectedInterval.from_decimal(delayed_text, precision)
    maximum_delay = DirectedInterval.from_decimal(delay_text, precision)
    if delayed_each.lower <= 0 or maximum_delay.lower <= 0:
        raise ValueError("source coefficient and delay bounds must be positive")

    one = DirectedInterval.from_decimal(1, precision)
    two = DirectedInterval.from_decimal(2, precision)
    three = DirectedInterval.from_decimal(3, precision)
    five = DirectedInterval.from_decimal(5, precision)
    epsilon = one / five
    voltage_scaffold = three
    recovery_scaffold = two

    # Complete the square globally in V.  The maximum decreases with both
    # positive gains, so directed interval arithmetic automatically selects
    # their lower endpoints for the upper theorem bound.
    q = three * epsilon * kappa_3
    current_maximum = one - epsilon * kappa_1 - q / (one + q)
    current_text, public_current = _public_upper(
        current_maximum.upper, precision
    )
    delayed_each_text, public_delayed_each = _public_upper(
        delayed_each.upper, precision
    )
    delay_public_text, public_delay = _public_upper(
        maximum_delay.upper, precision
    )

    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        voltage_decay_raw = voltage_scaffold.lower - public_current - 1
        recovery_decay_raw = recovery_scaffold.lower - epsilon.upper
    voltage_decay_text, public_voltage_decay = _public_lower(
        voltage_decay_raw, precision
    )
    recovery_decay_text, public_recovery_decay = _public_lower(
        recovery_decay_raw, precision
    )
    local_decay_raw = min(public_voltage_decay, public_recovery_decay)
    local_decay_text, public_local_decay = _public_lower(
        local_decay_raw, precision
    )
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        delayed_total_raw = 2 * public_delayed_each
    delayed_total_text, public_delayed_total = _public_upper(
        delayed_total_raw, precision
    )
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        margin_raw = public_local_decay - public_delayed_total
    margin_text, public_margin = _public_lower(margin_raw, precision)
    if public_margin <= 0:
        raise ValueError("periodic transverse Halanay margin is nonpositive")

    rate = DirectedInterval.from_decimal("0.02", precision)
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        rate_delay = rate.upper * public_delay
    exponential_raw = _exp_upper(rate_delay, precision)
    exponential_text, public_exponential = _public_upper(
        exponential_raw, precision
    )
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        delayed_exponential = public_delayed_total * public_exponential
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        residual_raw = public_local_decay - rate.upper - delayed_exponential
    residual_text, public_residual = _public_lower(residual_raw, precision)
    if public_residual <= 0:
        raise ValueError("declared periodic transverse rate is not certified")

    algebra = periodic_transverse_algebra()
    exact_modal = (
        algebra.completed_square_residual == 0
        and algebra.same_delay_collective_residual == sp.zeros(2, 1)
        and algebra.same_delay_difference_residual == sp.zeros(2, 1)
        and algebra.cross_delay_collective_residual == sp.zeros(2, 1)
        and algebra.cross_delay_difference_residual == sp.zeros(2, 1)
    )
    if not exact_modal:
        raise RuntimeError("exact transverse modal algebra failed")
    audit_sizes = ((1, 1), (2, 3), (4, 2))
    network_audits = tuple(
        periodic_transverse_network_algebra(n1, n2)
        for n1, n2 in audit_sizes
    )
    exact_full_node = all(
        _network_algebra_is_exact(audit) for audit in network_audits
    )
    if not exact_full_node:
        raise RuntimeError("exact full-node transverse lift audit failed")

    return PeriodicTransverseHalanayCertificate(
        parameter_box_result_sha256=parameter_box_result_sha256,
        bloch_result_sha256=bloch_result_sha256,
        precision_bits=precision,
        model_id=MODEL_ID,
        topology="fixed rank-one two-module averaging with within/cross delays",
        epsilon="0.2",
        voltage_scaffold="3",
        recovery_scaffold="2",
        max_norm_weight="1",
        gain_half_width="1e-12",
        kappa_1_interval=_pair(kappa_1),
        kappa_3_interval=_pair(kappa_3),
        maximum_delay_upper=delay_public_text,
        current_coefficient_global_maximum_upper=current_text,
        delayed_each_wiener_norm_upper=delayed_each_text,
        delayed_total_gain_upper=delayed_total_text,
        voltage_local_decay_lower=voltage_decay_text,
        recovery_local_decay_lower=recovery_decay_text,
        halanay_local_decay_lower=local_decay_text,
        halanay_margin_lower=margin_text,
        halanay_rate_candidate="0.02",
        halanay_rate_exponential_upper=exponential_text,
        halanay_rate_residual_lower=residual_text,
        exact_rank_one_modal_decomposition_validated=True,
        representative_full_node_delay_layer_audits_validated=True,
        within_module_delay_annihilation_validated=True,
        instantaneous_scaffold_modal_action_validated=True,
        full_node_audit_module_sizes=audit_sizes,
        arbitrary_size_quantifier_from_enumeration=False,
        arbitrary_positive_module_sizes_formulaic_theorem=True,
        source_periodic_branch_validated=True,
        source_synchronous_orbital_hyperbolicity_validated=True,
        periodic_transverse_variational_decay_validated=True,
        full_network_orbital_hyperbolicity_validated=True,
        synchronous_attraction_validated=False,
        full_network_attraction_validated=False,
        nonlinear_synchronization_validated=False,
        general_network_topology_validated=False,
        physical_pulse_onset_validated=False,
        issue_15_closed=False,
    )


def load_periodic_transverse_halanay(
    parameter_box_path: str | Path,
    bloch_result_path: str | Path,
    *,
    expected_parameter_sha256: str = TRACKED_PARAMETER_BOX_SHA256,
    expected_bloch_sha256: str = TRACKED_BLOCH_RESULT_SHA256,
    precision: int = 160,
) -> PeriodicTransverseHalanayCertificate:
    """Hash-check both tracked records before deriving the certificate."""

    parameter_raw = Path(parameter_box_path).read_bytes()
    bloch_raw = Path(bloch_result_path).read_bytes()
    parameter_digest = sha256(parameter_raw).hexdigest()
    bloch_digest = sha256(bloch_raw).hexdigest()
    if parameter_digest != expected_parameter_sha256:
        raise ValueError(
            "parameter-box result SHA-256 mismatch: "
            f"expected {expected_parameter_sha256}, got {parameter_digest}"
        )
    if bloch_digest != expected_bloch_sha256:
        raise ValueError(
            "Bloch result SHA-256 mismatch: "
            f"expected {expected_bloch_sha256}, got {bloch_digest}"
        )
    try:
        parameter_payload = json.loads(parameter_raw)
        bloch_payload = json.loads(bloch_raw)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError("one source record is not valid UTF-8 JSON") from error
    return periodic_transverse_halanay_from_payloads(
        _mapping(parameter_payload, "parameter payload"),
        _mapping(bloch_payload, "Bloch payload"),
        parameter_box_result_sha256=parameter_digest,
        bloch_result_sha256=bloch_digest,
        precision=precision,
    )


def validate_periodic_transverse_result_payload(
    payload: Mapping[str, Any],
) -> None:
    """Refuse missing proof flags and every unsupported scope promotion."""

    root = _mapping(payload, "result payload")
    certificate = _mapping(root.get("certificate"), "certificate")
    scope = _mapping(root.get("scope"), "scope")
    source = _mapping(root.get("source_evidence"), "source_evidence")
    if source.get("parameter_box_result_sha256") != TRACKED_PARAMETER_BOX_SHA256:
        raise ValueError("result is not bound to the tracked parameter box")
    if source.get("bloch_result_sha256") != TRACKED_BLOCH_RESULT_SHA256:
        raise ValueError("result is not bound to the tracked Bloch theorem")
    for name in (
        "exact_rank_one_modal_decomposition_validated",
        "representative_full_node_delay_layer_audits_validated",
        "within_module_delay_annihilation_validated",
        "instantaneous_scaffold_modal_action_validated",
        "arbitrary_positive_module_sizes_formulaic_theorem",
        "source_periodic_branch_validated",
        "source_synchronous_orbital_hyperbolicity_validated",
        "periodic_transverse_variational_decay_validated",
        "full_network_orbital_hyperbolicity_validated",
    ):
        _require_true(certificate, name)
    for name in (
        "synchronous_attraction_validated",
        "full_network_attraction_validated",
        "nonlinear_synchronization_validated",
        "general_network_topology_validated",
        "physical_pulse_onset_validated",
        "issue_15_closed",
    ):
        _require_false(certificate, name)
    _require_false(certificate, "arbitrary_size_quantifier_from_enumeration")
    for name in (
        "periodic_transverse_variational_decay",
        "full_network_orbital_hyperbolicity",
        "arbitrary_positive_module_sizes_for_fixed_rank_one_topology",
    ):
        _require_true(scope, name)
    for name in (
        "synchronous_attraction",
        "full_network_attraction",
        "nonlinear_synchronization",
        "general_network_topology",
        "physical_pulse_onset",
        "issue_15_closed",
    ):
        _require_false(scope, name)


def load_periodic_transverse_result(
    path: str | Path,
    *,
    expected_sha256: str,
) -> Mapping[str, Any]:
    """Hash-check and semantically validate a generated result artifact."""

    raw = Path(path).read_bytes()
    digest = sha256(raw).hexdigest()
    if digest != expected_sha256:
        raise ValueError(
            "periodic transverse result SHA-256 mismatch: "
            f"expected {expected_sha256}, got {digest}"
        )
    try:
        payload = json.loads(raw)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError("periodic transverse result is not valid JSON") from error
    validate_periodic_transverse_result_payload(payload)
    return payload
