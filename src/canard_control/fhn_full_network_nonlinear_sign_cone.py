"""Exact and directed certificate for nonlinear full-network sign cones.

The theorem concerns the fixed rank-one two-module FHN decision model with
voltage scaffold D=3, recovery scaffold E=2, and the collective recovery
clamp.  It proves a nodewise first hit for fully nonlinear, nonsynchronous
histories that stay a positive distance from the voltage sign boundary.

For the nodewise detector faces ``H=1``, the sufficient cone condition is

    D*m > max(W0, epsilon/E),

where every voltage history component has the declared sign and magnitude
at least m, all current voltages lie strictly between the sign boundary and
the corresponding detector face, the collective recovery history is zero,
and W0 bounds the recovery history.  The result is not synchronization,
attraction, cross-sign noise robustness, a hardware theorem, or a
beyond-detector biological basin theorem.  A second certificate uses
``D*m_exc > max(W0, epsilon*H/E)`` to force the finite controlled faces
``H=1.5`` and ``H=1.2``; it does not assert detector-face no-return or that
the first detector node is the excursion-face node.
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
from canard_control.fhn_same_model_separator import (
    FULL_NETWORK_INSTANCE_ID,
    validate_same_model_separator_result_payload,
)
from canard_control.full_network_blocks import (
    two_module_block_algebra,
    uniform_history_layer,
)


TRACKED_SEPARATOR_RESULT_SHA256 = (
    "9e859f31c177638a70b3ca451fe743227308343792d77eeca286fca26afc8a86"
)
MODEL_ID = "rank-one-two-module-fhn-D3-E2-recovery-clamped"
THEOREM_CONDITION = "D*m>max(W0,epsilon/E)"
EXCURSION_THEOREM_CONDITION = "D*m_exc>max(W0,epsilon*H/E)"


@dataclass(frozen=True)
class FullNetworkSignConeAlgebra:
    """Exact rank-one averaging and recovery-clamp identities."""

    n1: int
    n2: int
    pi_sum_residual: sp.Expr
    delay_sum_projection_residual: sp.Matrix
    pi_same_delay_residual: sp.Matrix
    pi_cross_delay_residual: sp.Matrix
    same_delay_collective_residual: sp.Matrix
    cross_delay_collective_residual: sp.Matrix
    recovery_mean_residual: sp.Expr
    recovery_deviation_residual: sp.Matrix
    positive_intrinsic_factor_residual: sp.Expr
    negative_intrinsic_factor_residual: sp.Expr
    boundary_cubic_factor_residual: sp.Expr
    delay_layers_entrywise_nonnegative: bool


@dataclass(frozen=True)
class FullNetworkNonlinearSignConeCertificate:
    """Public constants and strict scope of the nonlinear cone theorem."""

    separator_result_sha256: str
    precision_bits: int
    model_id: str
    theorem_condition: str
    epsilon: str
    voltage_scaffold: str
    recovery_scaffold: str
    declared_voltage_sign_margin: str
    declared_recovery_history_bound: str
    recovery_forcing_bound: str
    effective_recovery_bound: str
    inward_boundary_margin_lower: str
    positive_mean_growth_lower: str
    negative_mean_growth_lower: str
    positive_release_deadline_upper: str
    negative_release_deadline_upper: str
    physical_hold_duration_upper: str
    positive_total_protocol_deadline_upper: str
    negative_total_protocol_deadline_upper: str
    detector_faces: tuple[str, str]
    excursion_theorem_condition: str
    declared_excursion_voltage_sign_margin: str
    positive_excursion_face: str
    negative_excursion_face: str
    positive_excursion_growth_lower: str
    negative_excursion_growth_lower: str
    positive_excursion_recovery_forcing_bound: str
    negative_excursion_recovery_forcing_bound: str
    positive_excursion_effective_recovery_bound: str
    negative_excursion_effective_recovery_bound: str
    positive_excursion_inward_boundary_margin_lower: str
    negative_excursion_inward_boundary_margin_lower: str
    positive_excursion_release_deadline_upper: str
    negative_excursion_release_deadline_upper: str
    positive_excursion_total_protocol_deadline_upper: str
    negative_excursion_total_protocol_deadline_upper: str
    exact_pi_delay_layer_identities_validated: bool
    exact_collective_recovery_deviation_equation_validated: bool
    arbitrary_positive_module_sizes_formula_validated: bool
    positive_full_network_nonlinear_sign_cone_first_hit_validated: bool
    negative_full_network_nonlinear_sign_cone_first_hit_validated: bool
    nodewise_detector_first_hit_validated: bool
    positive_finite_controlled_suprathreshold_excursion_validated: bool
    negative_finite_controlled_excursion_validated: bool
    latched_nodewise_detector_then_excursion_validated: bool
    ideal_recovery_clamp_validated: bool
    same_detector_node_reaches_excursion_face_validated: bool
    detector_face_no_return_validated: bool
    nonlinear_synchronization_validated: bool
    attraction_validated: bool
    noise_across_voltage_sign_boundary_validated: bool
    bounded_additive_hold_or_hardware_validated: bool
    beyond_face_biological_basin_validated: bool
    unforced_or_maximal_canard_onset_validated: bool
    general_network_topology_validated: bool
    issue_15_closed: bool


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


def full_network_sign_cone_algebra(
    n1: int,
    n2: int,
) -> FullNetworkSignConeAlgebra:
    """Return exact identities for any declared positive module sizes."""

    algebra = two_module_block_algebra(n1, n2)
    node_count = algebra.node_count
    one = sp.ones(node_count, 1)
    identity = sp.eye(node_count)
    projection = sp.Matrix(algebra.collective_projector)
    pi = sp.Matrix([list(projection[0, :])])
    same = sp.Matrix(
        uniform_history_layer(algebra, sp.eye(2) / 2)
    )
    cross = sp.Matrix(
        uniform_history_layer(
            algebra,
            sp.Matrix([[0, 1], [1, 0]]) / 2,
        )
    )

    voltage = sp.Matrix(sp.symbols(f"v_0:{node_count}", real=True))
    recovery = sp.Matrix(sp.symbols(f"w_0:{node_count}", real=True))
    epsilon, unfolding, recovery_scaffold = sp.symbols(
        "epsilon unfolding E", real=True
    )
    mean_voltage = (pi * voltage)[0]
    mean_recovery = (pi * recovery)[0]
    actuator = -epsilon * (mean_voltage - unfolding) * one
    recovery_field = (
        epsilon * (voltage - unfolding * one)
        + recovery_scaffold * (projection - identity) * recovery
        + actuator
    )
    recovery_expected = (
        epsilon * (voltage - mean_voltage * one)
        - recovery_scaffold * (recovery - mean_recovery * one)
    )

    scalar = sp.Symbol("s", real=True)
    intrinsic = scalar - scalar**3 / 3
    boundary_cubic = (scalar - 1) ** 3 + 1
    return FullNetworkSignConeAlgebra(
        n1=n1,
        n2=n2,
        pi_sum_residual=sp.simplify((pi * one)[0] - 1),
        delay_sum_projection_residual=sp.ImmutableMatrix(
            same + cross - projection
        ),
        pi_same_delay_residual=sp.ImmutableMatrix(pi * same - pi / 2),
        pi_cross_delay_residual=sp.ImmutableMatrix(pi * cross - pi / 2),
        same_delay_collective_residual=sp.ImmutableMatrix(
            same * one - one / 2
        ),
        cross_delay_collective_residual=sp.ImmutableMatrix(
            cross * one - one / 2
        ),
        recovery_mean_residual=sp.simplify((pi * recovery_field)[0]),
        recovery_deviation_residual=sp.ImmutableMatrix(
            sp.simplify(recovery_field - recovery_expected)
        ),
        positive_intrinsic_factor_residual=sp.simplify(
            intrinsic - sp.Rational(2, 3) * scalar
            - scalar * (1 - scalar**2) / 3
        ),
        negative_intrinsic_factor_residual=sp.simplify(
            sp.Rational(2, 3) * scalar - intrinsic
            - scalar * (scalar**2 - 1) / 3
        ),
        boundary_cubic_factor_residual=sp.simplify(
            boundary_cubic - scalar * (scalar**2 - 3 * scalar + 3)
        ),
        delay_layers_entrywise_nonnegative=all(
            entry >= 0 for entry in tuple(same) + tuple(cross)
        ),
    )


def _algebra_is_exact(audit: FullNetworkSignConeAlgebra) -> bool:
    node_count = audit.n1 + audit.n2
    return (
        audit.pi_sum_residual == 0
        and audit.delay_sum_projection_residual == sp.zeros(node_count)
        and audit.pi_same_delay_residual == sp.zeros(1, node_count)
        and audit.pi_cross_delay_residual == sp.zeros(1, node_count)
        and audit.same_delay_collective_residual == sp.zeros(node_count, 1)
        and audit.cross_delay_collective_residual == sp.zeros(node_count, 1)
        and audit.recovery_mean_residual == 0
        and audit.recovery_deviation_residual == sp.zeros(node_count, 1)
        and audit.positive_intrinsic_factor_residual == 0
        and audit.negative_intrinsic_factor_residual == 0
        and audit.boundary_cubic_factor_residual == 0
        and audit.delay_layers_entrywise_nonnegative
    )


def _public_lower(value: gmpy2.mpfr, precision: int) -> tuple[str, gmpy2.mpfr]:
    text = decimal_lower(value, 55)
    return text, DirectedInterval.from_decimal(text, precision).lower


def _public_upper(value: gmpy2.mpfr, precision: int) -> tuple[str, gmpy2.mpfr]:
    text = decimal_upper(value, 55)
    return text, DirectedInterval.from_decimal(text, precision).upper


def _log_upper(value: gmpy2.mpfr, precision: int) -> gmpy2.mpfr:
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        return gmpy2.log(value)


def full_network_nonlinear_sign_cone_from_payload(
    payload: Mapping[str, Any],
    *,
    separator_result_sha256: str,
    precision: int = 160,
    voltage_sign_margin: str = "0.04",
    excursion_voltage_sign_margin: str = "0.06",
    recovery_history_bound: str = "0.1",
) -> FullNetworkNonlinearSignConeCertificate:
    """Validate the separator source and derive one concrete cone certificate."""

    if separator_result_sha256 != TRACKED_SEPARATOR_RESULT_SHA256:
        raise ValueError("separator result is not the tracked same-model theorem")
    if (
        isinstance(precision, bool)
        or int(precision) != precision
        or int(precision) < 64
    ):
        raise ValueError("precision must be an integer of at least 64 bits")
    precision = int(precision)

    root = _mapping(payload, "separator payload")
    validate_same_model_separator_result_payload(root)
    source_certificate = _mapping(root.get("certificate"), "certificate")
    source_scope = _mapping(root.get("scope"), "scope")
    if source_certificate.get("certified_full_network_instance_id") != (
        FULL_NETWORK_INSTANCE_ID
    ):
        raise ValueError("source full-network instance is not D3-E2")
    if source_certificate.get("epsilon") != "1/5":
        raise ValueError("source epsilon is not 1/5")
    if source_certificate.get("voltage_scaffold") != "3":
        raise ValueError("source voltage scaffold is not 3")
    if source_certificate.get("recovery_scaffold") != "2":
        raise ValueError("source recovery scaffold is not 2")
    for flag in (
        "full_network_collective_projection_exact",
        "physical_collective_recovery_actuator_exact",
        "controlled_collective_recovery_leaf_invariant_exact",
    ):
        _require_true(source_certificate, flag)
    _require_false(source_scope, "quantified_noisy_history_capture")
    _require_false(
        source_scope, "biological_pulse_or_quiet_basin_capture_beyond_channel_faces"
    )

    positive_growth_text = source_certificate.get(
        "positive_channel_growth_lower"
    )
    negative_growth_text = source_certificate.get(
        "negative_channel_growth_lower"
    )
    physical_delay_text = source_certificate.get("physical_delay_upper")
    if not all(
        isinstance(text, str)
        for text in (
            positive_growth_text,
            negative_growth_text,
            physical_delay_text,
        )
    ):
        raise ValueError("source directed endpoints must be decimal strings")

    epsilon = DirectedInterval.from_decimal("0.2", precision)
    voltage_scaffold = DirectedInterval.from_decimal(3, precision)
    recovery_scaffold = DirectedInterval.from_decimal(2, precision)
    sign_margin = DirectedInterval.from_decimal(voltage_sign_margin, precision)
    excursion_sign_margin = DirectedInterval.from_decimal(
        excursion_voltage_sign_margin, precision
    )
    recovery_history = DirectedInterval.from_decimal(
        recovery_history_bound, precision
    )
    if sign_margin.lower <= 0 or sign_margin.upper >= 1:
        raise ValueError("voltage sign margin must lie strictly between 0 and 1")
    if excursion_sign_margin.lower <= 0 or excursion_sign_margin.upper >= 1:
        raise ValueError(
            "excursion voltage sign margin must lie strictly between 0 and 1"
        )
    if recovery_history.lower < 0:
        raise ValueError("recovery history bound must be nonnegative")

    recovery_forcing = epsilon / recovery_scaffold
    effective_recovery_upper = max(
        recovery_history.upper, recovery_forcing.upper
    )
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        inward_margin_raw = (
            voltage_scaffold.lower * sign_margin.lower
            - effective_recovery_upper
        )
    inward_margin_text, public_inward_margin = _public_lower(
        inward_margin_raw, precision
    )
    if public_inward_margin <= 0:
        raise ValueError("D*m must exceed max(W0,epsilon/E)")

    positive_growth = DirectedInterval.from_decimal(
        positive_growth_text, precision
    )
    negative_growth = DirectedInterval.from_decimal(
        negative_growth_text, precision
    )
    if positive_growth.lower <= 0 or negative_growth.lower <= 0:
        raise ValueError("source mean-growth lower bounds must be positive")
    one = DirectedInterval.from_decimal(1, precision)
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        inverse_margin = one.upper / sign_margin.lower
    logarithm = _log_upper(inverse_margin, precision)
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        positive_deadline_raw = logarithm / positive_growth.lower
        negative_deadline_raw = logarithm / negative_growth.lower
    positive_deadline_text, public_positive_deadline = _public_upper(
        positive_deadline_raw, precision
    )
    negative_deadline_text, public_negative_deadline = _public_upper(
        negative_deadline_raw, precision
    )
    physical_delay = DirectedInterval.from_decimal(
        physical_delay_text, precision
    )
    physical_delay_public_text, public_physical_delay = _public_upper(
        physical_delay.upper, precision
    )
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        positive_total_raw = public_physical_delay + public_positive_deadline
        negative_total_raw = public_physical_delay + public_negative_deadline
    positive_total_text, _ = _public_upper(positive_total_raw, precision)
    negative_total_text, _ = _public_upper(negative_total_raw, precision)

    kappa_1_bounds = source_certificate.get("kappa_1_interval")
    kappa_3_bounds = source_certificate.get("kappa_3_interval")
    if not (
        isinstance(kappa_1_bounds, (list, tuple))
        and len(kappa_1_bounds) == 2
        and all(isinstance(item, str) for item in kappa_1_bounds)
        and isinstance(kappa_3_bounds, (list, tuple))
        and len(kappa_3_bounds) == 2
        and all(isinstance(item, str) for item in kappa_3_bounds)
    ):
        raise ValueError("source gain intervals must be decimal endpoint pairs")
    kappa_1 = DirectedInterval.from_bounds(*kappa_1_bounds, precision)
    kappa_3 = DirectedInterval.from_bounds(*kappa_3_bounds, precision)
    if kappa_1.lower <= 0 or kappa_3.lower <= 0:
        raise ValueError("source gain intervals must be positive")

    three = DirectedInterval.from_decimal(3, precision)
    positive_excursion_face = DirectedInterval.from_decimal("1.5", precision)
    negative_excursion_magnitude = DirectedInterval.from_decimal(
        "1.2", precision
    )
    positive_excursion_intrinsic = (
        one - positive_excursion_face**2 / three
    )
    positive_excursion_growth = positive_excursion_intrinsic - epsilon * (
        kappa_1 + three * kappa_3
    )
    negative_excursion_secant = (
        negative_excursion_magnitude**2
        + three * negative_excursion_magnitude
        + three
    )
    negative_excursion_intrinsic = (
        one - negative_excursion_magnitude**2 / three
    )
    negative_excursion_growth = negative_excursion_intrinsic - epsilon * (
        kappa_1 + negative_excursion_secant * kappa_3
    )
    if (
        positive_excursion_growth.lower <= 0
        or negative_excursion_growth.lower <= 0
    ):
        raise ValueError("finite-excursion mean-growth lower bounds must be positive")

    positive_excursion_forcing = (
        epsilon * positive_excursion_face / recovery_scaffold
    )
    negative_excursion_forcing = (
        epsilon * negative_excursion_magnitude / recovery_scaffold
    )
    positive_excursion_effective = max(
        recovery_history.upper, positive_excursion_forcing.upper
    )
    negative_excursion_effective = max(
        recovery_history.upper, negative_excursion_forcing.upper
    )
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        positive_excursion_inward_raw = (
            voltage_scaffold.lower * excursion_sign_margin.lower
            - positive_excursion_effective
        )
        negative_excursion_inward_raw = (
            voltage_scaffold.lower * excursion_sign_margin.lower
            - negative_excursion_effective
        )
    positive_excursion_inward_text, public_positive_excursion_inward = (
        _public_lower(positive_excursion_inward_raw, precision)
    )
    negative_excursion_inward_text, public_negative_excursion_inward = (
        _public_lower(negative_excursion_inward_raw, precision)
    )
    if public_positive_excursion_inward <= 0:
        raise ValueError(
            "D*m_exc must exceed max(W0,epsilon*H_plus/E)"
        )
    if public_negative_excursion_inward <= 0:
        raise ValueError(
            "D*m_exc must exceed max(W0,epsilon*H_minus/E)"
        )

    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        positive_excursion_ratio = (
            positive_excursion_face.upper / excursion_sign_margin.lower
        )
        negative_excursion_ratio = (
            negative_excursion_magnitude.upper / excursion_sign_margin.lower
        )
    positive_excursion_logarithm = _log_upper(
        positive_excursion_ratio, precision
    )
    negative_excursion_logarithm = _log_upper(
        negative_excursion_ratio, precision
    )
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        positive_excursion_deadline_raw = (
            positive_excursion_logarithm
            / positive_excursion_growth.lower
        )
        negative_excursion_deadline_raw = (
            negative_excursion_logarithm
            / negative_excursion_growth.lower
        )
    positive_excursion_deadline_text, public_positive_excursion_deadline = (
        _public_upper(positive_excursion_deadline_raw, precision)
    )
    negative_excursion_deadline_text, public_negative_excursion_deadline = (
        _public_upper(negative_excursion_deadline_raw, precision)
    )
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        positive_excursion_total_raw = (
            public_physical_delay + public_positive_excursion_deadline
        )
        negative_excursion_total_raw = (
            public_physical_delay + public_negative_excursion_deadline
        )
    positive_excursion_total_text, _ = _public_upper(
        positive_excursion_total_raw, precision
    )
    negative_excursion_total_text, _ = _public_upper(
        negative_excursion_total_raw, precision
    )

    network_audits = tuple(
        full_network_sign_cone_algebra(n1, n2)
        for n1, n2 in ((1, 1), (2, 3), (4, 2))
    )
    if not all(_algebra_is_exact(audit) for audit in network_audits):
        raise RuntimeError("exact full-network sign-cone algebra failed")

    recovery_forcing_text, _ = _public_upper(
        recovery_forcing.upper, precision
    )
    effective_recovery_text, _ = _public_upper(
        effective_recovery_upper, precision
    )
    positive_excursion_growth_text, _ = _public_lower(
        positive_excursion_growth.lower, precision
    )
    negative_excursion_growth_text, _ = _public_lower(
        negative_excursion_growth.lower, precision
    )
    positive_excursion_forcing_text, _ = _public_upper(
        positive_excursion_forcing.upper, precision
    )
    negative_excursion_forcing_text, _ = _public_upper(
        negative_excursion_forcing.upper, precision
    )
    positive_excursion_effective_text, _ = _public_upper(
        positive_excursion_effective, precision
    )
    negative_excursion_effective_text, _ = _public_upper(
        negative_excursion_effective, precision
    )
    return FullNetworkNonlinearSignConeCertificate(
        separator_result_sha256=separator_result_sha256,
        precision_bits=precision,
        model_id=MODEL_ID,
        theorem_condition=THEOREM_CONDITION,
        epsilon="0.2",
        voltage_scaffold="3",
        recovery_scaffold="2",
        declared_voltage_sign_margin=voltage_sign_margin,
        declared_recovery_history_bound=recovery_history_bound,
        recovery_forcing_bound=recovery_forcing_text,
        effective_recovery_bound=effective_recovery_text,
        inward_boundary_margin_lower=inward_margin_text,
        positive_mean_growth_lower=positive_growth_text,
        negative_mean_growth_lower=negative_growth_text,
        positive_release_deadline_upper=positive_deadline_text,
        negative_release_deadline_upper=negative_deadline_text,
        physical_hold_duration_upper=physical_delay_public_text,
        positive_total_protocol_deadline_upper=positive_total_text,
        negative_total_protocol_deadline_upper=negative_total_text,
        detector_faces=("-1", "1"),
        excursion_theorem_condition=EXCURSION_THEOREM_CONDITION,
        declared_excursion_voltage_sign_margin=(
            excursion_voltage_sign_margin
        ),
        positive_excursion_face="1.5",
        negative_excursion_face="-1.2",
        positive_excursion_growth_lower=positive_excursion_growth_text,
        negative_excursion_growth_lower=negative_excursion_growth_text,
        positive_excursion_recovery_forcing_bound=(
            positive_excursion_forcing_text
        ),
        negative_excursion_recovery_forcing_bound=(
            negative_excursion_forcing_text
        ),
        positive_excursion_effective_recovery_bound=(
            positive_excursion_effective_text
        ),
        negative_excursion_effective_recovery_bound=(
            negative_excursion_effective_text
        ),
        positive_excursion_inward_boundary_margin_lower=(
            positive_excursion_inward_text
        ),
        negative_excursion_inward_boundary_margin_lower=(
            negative_excursion_inward_text
        ),
        positive_excursion_release_deadline_upper=(
            positive_excursion_deadline_text
        ),
        negative_excursion_release_deadline_upper=(
            negative_excursion_deadline_text
        ),
        positive_excursion_total_protocol_deadline_upper=(
            positive_excursion_total_text
        ),
        negative_excursion_total_protocol_deadline_upper=(
            negative_excursion_total_text
        ),
        exact_pi_delay_layer_identities_validated=True,
        exact_collective_recovery_deviation_equation_validated=True,
        arbitrary_positive_module_sizes_formula_validated=True,
        positive_full_network_nonlinear_sign_cone_first_hit_validated=True,
        negative_full_network_nonlinear_sign_cone_first_hit_validated=True,
        nodewise_detector_first_hit_validated=True,
        positive_finite_controlled_suprathreshold_excursion_validated=True,
        negative_finite_controlled_excursion_validated=True,
        latched_nodewise_detector_then_excursion_validated=True,
        ideal_recovery_clamp_validated=True,
        same_detector_node_reaches_excursion_face_validated=False,
        detector_face_no_return_validated=False,
        nonlinear_synchronization_validated=False,
        attraction_validated=False,
        noise_across_voltage_sign_boundary_validated=False,
        bounded_additive_hold_or_hardware_validated=False,
        beyond_face_biological_basin_validated=False,
        unforced_or_maximal_canard_onset_validated=False,
        general_network_topology_validated=False,
        issue_15_closed=False,
    )


def load_full_network_nonlinear_sign_cone(
    separator_result_path: str | Path,
    *,
    expected_separator_sha256: str = TRACKED_SEPARATOR_RESULT_SHA256,
    precision: int = 160,
    voltage_sign_margin: str = "0.04",
    excursion_voltage_sign_margin: str = "0.06",
    recovery_history_bound: str = "0.1",
) -> FullNetworkNonlinearSignConeCertificate:
    """Hash-check the separator artifact before deriving the cone certificate."""

    raw = Path(separator_result_path).read_bytes()
    digest = sha256(raw).hexdigest()
    if digest != expected_separator_sha256:
        raise ValueError(
            "separator result SHA-256 mismatch: "
            f"expected {expected_separator_sha256}, got {digest}"
        )
    try:
        payload = json.loads(raw)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError("separator result is not valid UTF-8 JSON") from error
    return full_network_nonlinear_sign_cone_from_payload(
        _mapping(payload, "separator payload"),
        separator_result_sha256=digest,
        precision=precision,
        voltage_sign_margin=voltage_sign_margin,
        excursion_voltage_sign_margin=excursion_voltage_sign_margin,
        recovery_history_bound=recovery_history_bound,
    )


def validate_full_network_nonlinear_sign_cone_result_payload(
    payload: Mapping[str, Any],
) -> None:
    """Refuse missing proof flags and every unsupported scope promotion."""

    root = _mapping(payload, "result payload")
    source = _mapping(root.get("source_evidence"), "source_evidence")
    certificate = _mapping(root.get("certificate"), "certificate")
    scope = _mapping(root.get("scope"), "scope")
    if source.get("separator_result_sha256") != TRACKED_SEPARATOR_RESULT_SHA256:
        raise ValueError("result is not bound to the tracked separator theorem")
    if certificate.get("separator_result_sha256") != (
        TRACKED_SEPARATOR_RESULT_SHA256
    ):
        raise ValueError("certificate separator digest is invalid")
    if certificate.get("model_id") != MODEL_ID:
        raise ValueError("certificate model identifier is invalid")
    if certificate.get("theorem_condition") != THEOREM_CONDITION:
        raise ValueError("certificate theorem condition is invalid")
    if certificate.get("excursion_theorem_condition") != (
        EXCURSION_THEOREM_CONDITION
    ):
        raise ValueError("certificate excursion theorem condition is invalid")
    for name in (
        "exact_pi_delay_layer_identities_validated",
        "exact_collective_recovery_deviation_equation_validated",
        "arbitrary_positive_module_sizes_formula_validated",
        "positive_full_network_nonlinear_sign_cone_first_hit_validated",
        "negative_full_network_nonlinear_sign_cone_first_hit_validated",
        "nodewise_detector_first_hit_validated",
        "positive_finite_controlled_suprathreshold_excursion_validated",
        "negative_finite_controlled_excursion_validated",
        "latched_nodewise_detector_then_excursion_validated",
        "ideal_recovery_clamp_validated",
    ):
        _require_true(certificate, name)
    for name in (
        "nonlinear_synchronization_validated",
        "attraction_validated",
        "noise_across_voltage_sign_boundary_validated",
        "bounded_additive_hold_or_hardware_validated",
        "beyond_face_biological_basin_validated",
        "unforced_or_maximal_canard_onset_validated",
        "general_network_topology_validated",
        "issue_15_closed",
        "same_detector_node_reaches_excursion_face_validated",
        "detector_face_no_return_validated",
    ):
        _require_false(certificate, name)
    for name in (
        "positive_full_network_nonlinear_sign_cone_first_hit",
        "negative_full_network_nonlinear_sign_cone_first_hit",
        "nodewise_detector_first_hit",
        "arbitrary_positive_module_sizes_for_fixed_rank_one_family",
        "positive_finite_controlled_suprathreshold_excursion",
        "negative_finite_controlled_excursion",
        "latched_nodewise_detector_then_excursion",
    ):
        _require_true(scope, name)
    for name in (
        "nonlinear_synchronization",
        "attraction",
        "noise_across_voltage_sign_boundary",
        "bounded_additive_hold_or_hardware",
        "beyond_face_biological_basin",
        "unforced_or_maximal_canard_onset",
        "general_network_topology",
        "issue_15_closed",
        "same_detector_node_reaches_excursion_face",
        "detector_face_no_return",
    ):
        _require_false(scope, name)


def load_full_network_nonlinear_sign_cone_result(
    path: str | Path,
    *,
    expected_sha256: str,
) -> Mapping[str, Any]:
    """Hash-check and semantically validate a generated result artifact."""

    raw = Path(path).read_bytes()
    digest = sha256(raw).hexdigest()
    if digest != expected_sha256:
        raise ValueError(
            "full-network sign-cone result SHA-256 mismatch: "
            f"expected {expected_sha256}, got {digest}"
        )
    try:
        payload = json.loads(raw)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError("full-network sign-cone result is not valid JSON") from error
    validate_full_network_nonlinear_sign_cone_result_payload(payload)
    return payload
