"""Exact and directed certificate for balanced general-network sign cones.

The decision theorem concerns any finite nonnegative row-stochastic voltage
scaffold ``P`` and any finite family of nonnegative delay layers ``B_j`` at
finite nonnegative delays, sharing a positive left weight ``pi``:

    pi.T * P = pi.T,
    B_j * 1 = alpha_j * 1,
    pi.T * B_j = alpha_j * pi.T,
    sum(alpha_j) = 1.

During the decision stage an ideal nodewise recovery clamp enforces
``w_i == 0``.  Under this stronger clamp, the positive and negative history
orthants are invariant and the ``pi``-mean obeys topology-independent FHN
growth bounds.  No irreducibility, unique stationary distribution, strictly
positive matrix entries, Dobrushin contraction, or rank-one structure is
used.

The result does not validate a bounded actuator, transverse attraction,
general-topology canard-root equivalence, a biological basin, or hardware.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

import gmpy2
import sympy as sp

from canard_control.directed_interval import (
    DirectedInterval,
    decimal_lower,
    decimal_upper,
)
from canard_control.fhn_same_model_separator import (
    validate_same_model_separator_result_payload,
)


TRACKED_SEPARATOR_RESULT_SHA256 = (
    "9e859f31c177638a70b3ca451fe743227308343792d77eeca286fca26afc8a86"
)
MODEL_ID = "balanced-general-network-fhn-nodewise-recovery-clamped"
ASSUMPTIONS_ID = (
    "J>=1;0<=tau_j<infinity;D>=0;"
    "P>=0,P1=1;pi>0,pi^T*1=1,pi^T*P=pi^T;"
    "B_j>=0,B_j1=alpha_j1,"
    "pi^T*B_j=alpha_j*pi^T,sum(alpha_j)=1"
)


@dataclass(frozen=True)
class GeneralNetworkBalanceAudit:
    """Exact balance residuals for one rational network instance."""

    node_count: int
    delay_layer_count: int
    pi_sum_residual: sp.Expr
    scaffold_row_mass_residual: sp.Matrix
    scaffold_stationarity_residual: sp.Matrix
    delay_row_mass_residuals: tuple[sp.Matrix, ...]
    delay_stationarity_residuals: tuple[sp.Matrix, ...]
    alpha_sum_residual: sp.Expr
    combined_delay_row_mass_residual: sp.Matrix
    combined_delay_stationarity_residual: sp.Matrix
    synchronous_scaffold_residual: sp.Matrix
    mean_scaffold_residual: sp.Expr
    scaffold_entrywise_nonnegative: bool
    delay_layers_entrywise_nonnegative: bool
    alphas_nonnegative: bool
    stationary_weight_strictly_positive: bool
    scaffold_rank: int


@dataclass(frozen=True)
class GeneralNetworkPolynomialAudit:
    """Exact FHN factorizations and central-gain constants."""

    intrinsic_factor_residual: sp.Expr
    control_secant_factor_residual: sp.Expr
    control_derivative_residual: sp.Expr
    positive_detector_growth: sp.Expr
    negative_detector_growth: sp.Expr
    positive_excursion_growth: sp.Expr
    negative_excursion_growth: sp.Expr


@dataclass(frozen=True)
class GeneralNetworkSignConeCertificate:
    """Public constants and deliberately strict general-topology scope."""

    separator_result_sha256: str
    precision_bits: int
    model_id: str
    assumptions_id: str
    epsilon: str
    voltage_scaffold: str
    kappa_1_interval: tuple[str, str]
    kappa_3_interval: tuple[str, str]
    reference_delay_weights: tuple[str, str]
    reference_scaled_delays: tuple[str, str]
    declared_initial_mean_magnitude_lower: str
    detector_faces: tuple[str, str]
    positive_detector_growth_lower: str
    negative_detector_growth_lower: str
    positive_detector_deadline_upper: str
    negative_detector_deadline_upper: str
    positive_excursion_face: str
    negative_excursion_face: str
    positive_excursion_growth_lower: str
    negative_excursion_growth_lower: str
    positive_excursion_deadline_upper: str
    negative_excursion_deadline_upper: str
    exact_balance_identities_validated_on_diverse_topologies: bool
    exact_fhn_polynomial_identities_validated: bool
    positive_history_orthant_invariance_validated: bool
    negative_history_orthant_invariance_validated: bool
    topology_independent_collective_growth_validated: bool
    arbitrary_finite_node_count_formula_validated: bool
    nodewise_detector_first_hit_validated: bool
    positive_finite_controlled_excursion_validated: bool
    negative_finite_controlled_excursion_validated: bool
    synchronized_scalar_restriction_form_validated: bool
    staged_frequency_amplitude_reset_map_form_validated: bool
    irreducibility_or_unique_stationary_distribution_required: bool
    dobrushin_contraction_required: bool
    rank_one_topology_required: bool
    nodewise_ideal_recovery_clamp_validated: bool
    bounded_actuator_validated: bool
    transverse_attraction_validated: bool
    full_network_periodic_hyperbolicity_validated: bool
    general_topology_canard_root_equivalence_validated: bool
    general_topology_three_output_target_ball_validated: bool
    asynchronous_frequency_amplitude_map_validated: bool
    strict_inward_orthant_boundary_validated: bool
    biological_basin_validated: bool
    hardware_validated: bool


def _mapping(value: object, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{name} must be a mapping")
    return value


def _matrix(value: object, name: str) -> sp.Matrix:
    try:
        result = sp.Matrix(value)
    except (TypeError, ValueError) as error:
        raise ValueError(f"{name} must be a finite rectangular matrix") from error
    if result.rows < 1 or result.cols < 1:
        raise ValueError(f"{name} must be nonempty")
    return result


def _row(value: object, node_count: int) -> sp.Matrix:
    candidate = _matrix(value, "stationary weight")
    if candidate.shape == (node_count, 1):
        candidate = candidate.T
    if candidate.shape != (1, node_count):
        raise ValueError("stationary weight must have one entry per node")
    return candidate


def _entrywise_nonnegative(matrix: sp.Matrix) -> bool:
    return all(entry.is_nonnegative is True for entry in matrix)


def general_network_balance_audit(
    scaffold: object,
    stationary_weight: object,
    delay_layers: Sequence[object],
    delay_weights: Sequence[object],
) -> GeneralNetworkBalanceAudit:
    """Audit exact rational balance assumptions for one finite topology."""

    p_matrix = _matrix(scaffold, "scaffold")
    if p_matrix.rows != p_matrix.cols:
        raise ValueError("scaffold must be square")
    node_count = p_matrix.rows
    pi = _row(stationary_weight, node_count)
    layers = tuple(_matrix(layer, "delay layer") for layer in delay_layers)
    alphas = tuple(sp.sympify(weight) for weight in delay_weights)
    if not layers or len(layers) != len(alphas):
        raise ValueError("delay layers and weights must have equal positive length")
    if any(layer.shape != (node_count, node_count) for layer in layers):
        raise ValueError("every delay layer must match the scaffold shape")

    one = sp.ones(node_count, 1)
    identity = sp.eye(node_count)
    combined = sp.zeros(node_count)
    for layer in layers:
        combined += layer
    alpha_sum = sp.Add(*alphas)
    voltage = sp.Matrix(sp.symbols(f"v_0:{node_count}", real=True))
    return GeneralNetworkBalanceAudit(
        node_count=node_count,
        delay_layer_count=len(layers),
        pi_sum_residual=sp.simplify((pi * one)[0] - 1),
        scaffold_row_mass_residual=sp.ImmutableMatrix(p_matrix * one - one),
        scaffold_stationarity_residual=sp.ImmutableMatrix(pi * p_matrix - pi),
        delay_row_mass_residuals=tuple(
            sp.ImmutableMatrix(layer * one - alpha * one)
            for layer, alpha in zip(layers, alphas, strict=True)
        ),
        delay_stationarity_residuals=tuple(
            sp.ImmutableMatrix(pi * layer - alpha * pi)
            for layer, alpha in zip(layers, alphas, strict=True)
        ),
        alpha_sum_residual=sp.simplify(alpha_sum - 1),
        combined_delay_row_mass_residual=sp.ImmutableMatrix(
            combined * one - one
        ),
        combined_delay_stationarity_residual=sp.ImmutableMatrix(
            pi * combined - pi
        ),
        synchronous_scaffold_residual=sp.ImmutableMatrix(
            (p_matrix - identity) * one
        ),
        mean_scaffold_residual=sp.simplify(
            (pi * (p_matrix - identity) * voltage)[0]
        ),
        scaffold_entrywise_nonnegative=_entrywise_nonnegative(p_matrix),
        delay_layers_entrywise_nonnegative=all(
            _entrywise_nonnegative(layer) for layer in layers
        ),
        alphas_nonnegative=all(alpha.is_nonnegative is True for alpha in alphas),
        stationary_weight_strictly_positive=all(
            entry.is_positive is True for entry in pi
        ),
        scaffold_rank=int(p_matrix.rank()),
    )


def _balance_audit_is_exact(audit: GeneralNetworkBalanceAudit) -> bool:
    zero_column = sp.zeros(audit.node_count, 1)
    zero_row = sp.zeros(1, audit.node_count)
    return (
        audit.pi_sum_residual == 0
        and audit.scaffold_row_mass_residual == zero_column
        and audit.scaffold_stationarity_residual == zero_row
        and all(item == zero_column for item in audit.delay_row_mass_residuals)
        and all(item == zero_row for item in audit.delay_stationarity_residuals)
        and audit.alpha_sum_residual == 0
        and audit.combined_delay_row_mass_residual == zero_column
        and audit.combined_delay_stationarity_residual == zero_row
        and audit.synchronous_scaffold_residual == zero_column
        and audit.mean_scaffold_residual == 0
        and audit.scaffold_entrywise_nonnegative
        and audit.delay_layers_entrywise_nonnegative
        and audit.alphas_nonnegative
        and audit.stationary_weight_strictly_positive
    )


def reference_general_topology_audits() -> tuple[GeneralNetworkBalanceAudit, ...]:
    """Return exact audits for scalar, non-rank-one, reducible, and cyclic cases."""

    one = sp.Rational(1, 1)
    half = sp.Rational(1, 2)
    scalar = general_network_balance_audit(
        [[one]],
        [one],
        [[[half]], [[half]]],
        [half, half],
    )

    nonuniform_pi = [sp.Rational(1, 6), sp.Rational(1, 3), half]
    nonrank_scaffold = sp.Matrix(
        [
            [half, sp.Rational(1, 4), sp.Rational(1, 4)],
            [sp.Rational(1, 8), sp.Rational(5, 8), sp.Rational(1, 4)],
            [sp.Rational(1, 12), sp.Rational(1, 6), sp.Rational(3, 4)],
        ]
    )
    nonrank = general_network_balance_audit(
        nonrank_scaffold,
        nonuniform_pi,
        [nonrank_scaffold / 2, sp.eye(3) / 2],
        [half, half],
    )

    reducible_scaffold = sp.Matrix(
        [
            [0, 1, 0, 0],
            [1, 0, 0, 0],
            [0, 0, 0, 1],
            [0, 0, 1, 0],
        ]
    )
    reducible = general_network_balance_audit(
        reducible_scaffold,
        [sp.Rational(1, 4)] * 4,
        [reducible_scaffold / 2, sp.eye(4) / 2],
        [half, half],
    )

    cycle = sp.zeros(5)
    for row in range(5):
        cycle[row, (row + 1) % 5] = 1
    cycle_weights = (
        sp.Rational(1, 5),
        sp.Rational(3, 10),
        sp.Rational(1, 2),
    )
    directed_cycle = general_network_balance_audit(
        cycle,
        [sp.Rational(1, 5)] * 5,
        [
            cycle_weights[0] * sp.eye(5),
            cycle_weights[1] * cycle,
            cycle_weights[2] * cycle**2,
        ],
        cycle_weights,
    )
    return scalar, nonrank, reducible, directed_cycle


def general_network_polynomial_audit() -> GeneralNetworkPolynomialAudit:
    """Return exact polynomial identities and central parameter constants."""

    s = sp.Symbol("s", real=True)
    kappa_1, kappa_3 = sp.symbols("kappa_1 kappa_3", positive=True)
    intrinsic = s - s**3 / 3
    control = kappa_1 * s + kappa_3 * (s - 1) ** 3
    control_zero = control.subs(s, 0)
    central_1 = sp.Rational(1, 5)
    central_3 = sp.Rational(1, 4)
    epsilon = sp.Rational(1, 5)
    return GeneralNetworkPolynomialAudit(
        intrinsic_factor_residual=sp.simplify(
            intrinsic - s * (1 - s**2 / 3)
        ),
        control_secant_factor_residual=sp.simplify(
            control
            - control_zero
            - s * (kappa_1 + kappa_3 * (s**2 - 3 * s + 3))
        ),
        control_derivative_residual=sp.simplify(
            sp.diff(control, s) - (kappa_1 + 3 * kappa_3 * (s - 1) ** 2)
        ),
        positive_detector_growth=sp.simplify(
            sp.Rational(2, 3)
            - epsilon * (central_1 + 3 * central_3)
        ),
        negative_detector_growth=sp.simplify(
            sp.Rational(2, 3)
            - epsilon * (central_1 + 7 * central_3)
        ),
        positive_excursion_growth=sp.simplify(
            sp.Rational(1, 4)
            - epsilon * (central_1 + 3 * central_3)
        ),
        negative_excursion_growth=sp.simplify(
            sp.Rational(13, 25)
            - epsilon * (central_1 + sp.Rational(201, 25) * central_3)
        ),
    )


def _public_lower(value: gmpy2.mpfr, precision: int) -> str:
    return decimal_lower(value, 55)


def _public_upper(value: gmpy2.mpfr, precision: int) -> str:
    return decimal_upper(value, 55)


def _log_upper(value: gmpy2.mpfr, precision: int) -> gmpy2.mpfr:
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        return gmpy2.log(value)


def _deadline_upper(
    face: DirectedInterval,
    mean_lower: DirectedInterval,
    growth: DirectedInterval,
    precision: int,
) -> str:
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        ratio = face.upper / mean_lower.lower
    logarithm = _log_upper(ratio, precision)
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        deadline = logarithm / growth.lower
    return _public_upper(deadline, precision)


def general_network_sign_cone_from_payload(
    payload: Mapping[str, Any],
    *,
    separator_result_sha256: str,
    precision: int = 160,
    initial_mean_magnitude_lower: str = "0.06",
) -> GeneralNetworkSignConeCertificate:
    """Validate the scalar source and derive general-network constants."""

    if separator_result_sha256 != TRACKED_SEPARATOR_RESULT_SHA256:
        raise ValueError("separator result is not the tracked scalar source")
    if (
        isinstance(precision, bool)
        or int(precision) != precision
        or int(precision) < 64
    ):
        raise ValueError("precision must be an integer of at least 64 bits")
    precision = int(precision)

    root = _mapping(payload, "separator payload")
    validate_same_model_separator_result_payload(root)
    source = _mapping(root.get("certificate"), "source certificate")
    if source.get("epsilon") != "1/5":
        raise ValueError("source epsilon is not 1/5")
    if source.get("voltage_scaffold") != "3":
        raise ValueError("source voltage scaffold is not 3")
    if source.get("scaled_delays") != ["4", "5"]:
        raise ValueError("source delays are not the reference two-delay pair")
    bounds_1 = source.get("kappa_1_interval")
    bounds_3 = source.get("kappa_3_interval")
    if not (
        isinstance(bounds_1, list)
        and len(bounds_1) == 2
        and all(isinstance(item, str) for item in bounds_1)
        and isinstance(bounds_3, list)
        and len(bounds_3) == 2
        and all(isinstance(item, str) for item in bounds_3)
    ):
        raise ValueError("source gain intervals must be decimal pairs")

    epsilon = DirectedInterval.from_decimal("0.2", precision)
    one = DirectedInterval.from_decimal(1, precision)
    three = DirectedInterval.from_decimal(3, precision)
    kappa_1 = DirectedInterval.from_bounds(*bounds_1, precision)
    kappa_3 = DirectedInterval.from_bounds(*bounds_3, precision)
    mean_lower = DirectedInterval.from_decimal(
        initial_mean_magnitude_lower, precision
    )
    if mean_lower.lower <= 0 or mean_lower.upper >= 1:
        raise ValueError("initial mean magnitude must lie strictly between 0 and 1")

    two_thirds = DirectedInterval.from_decimal(2, precision) / three
    positive_detector_growth = two_thirds - epsilon * (
        kappa_1 + three * kappa_3
    )
    negative_detector_growth = two_thirds - epsilon * (
        kappa_1 + 7 * kappa_3
    )
    positive_face = DirectedInterval.from_decimal("1.5", precision)
    negative_magnitude = DirectedInterval.from_decimal("1.2", precision)
    positive_excursion_growth = (
        one - positive_face**2 / three
        - epsilon * (kappa_1 + three * kappa_3)
    )
    negative_secant = (
        negative_magnitude**2 + three * negative_magnitude + three
    )
    negative_excursion_growth = (
        one - negative_magnitude**2 / three
        - epsilon * (kappa_1 + negative_secant * kappa_3)
    )
    growth_intervals = (
        positive_detector_growth,
        negative_detector_growth,
        positive_excursion_growth,
        negative_excursion_growth,
    )
    if any(interval.lower <= 0 for interval in growth_intervals):
        raise ValueError("all detector and excursion growth bounds must be positive")

    topology_audits = reference_general_topology_audits()
    if not all(_balance_audit_is_exact(audit) for audit in topology_audits):
        raise RuntimeError("exact general-network balance audit failed")
    if not (
        topology_audits[1].scaffold_rank > 1
        and topology_audits[2].scaffold_rank > 1
    ):
        raise RuntimeError("reference audits do not include non-rank-one cases")
    polynomial = general_network_polynomial_audit()
    if not (
        polynomial.intrinsic_factor_residual == 0
        and polynomial.control_secant_factor_residual == 0
        and polynomial.control_derivative_residual == 0
        and polynomial.positive_detector_growth == sp.Rational(143, 300)
        and polynomial.negative_detector_growth == sp.Rational(83, 300)
        and polynomial.positive_excursion_growth == sp.Rational(3, 50)
        and polynomial.negative_excursion_growth == sp.Rational(39, 500)
    ):
        raise RuntimeError("exact FHN polynomial audit failed")

    detector_face = DirectedInterval.from_decimal(1, precision)
    return GeneralNetworkSignConeCertificate(
        separator_result_sha256=separator_result_sha256,
        precision_bits=precision,
        model_id=MODEL_ID,
        assumptions_id=ASSUMPTIONS_ID,
        epsilon="0.2",
        voltage_scaffold="3",
        kappa_1_interval=(bounds_1[0], bounds_1[1]),
        kappa_3_interval=(bounds_3[0], bounds_3[1]),
        reference_delay_weights=("0.5", "0.5"),
        reference_scaled_delays=("4", "5"),
        declared_initial_mean_magnitude_lower=initial_mean_magnitude_lower,
        detector_faces=("-1", "1"),
        positive_detector_growth_lower=_public_lower(
            positive_detector_growth.lower, precision
        ),
        negative_detector_growth_lower=_public_lower(
            negative_detector_growth.lower, precision
        ),
        positive_detector_deadline_upper=_deadline_upper(
            detector_face, mean_lower, positive_detector_growth, precision
        ),
        negative_detector_deadline_upper=_deadline_upper(
            detector_face, mean_lower, negative_detector_growth, precision
        ),
        positive_excursion_face="1.5",
        negative_excursion_face="-1.2",
        positive_excursion_growth_lower=_public_lower(
            positive_excursion_growth.lower, precision
        ),
        negative_excursion_growth_lower=_public_lower(
            negative_excursion_growth.lower, precision
        ),
        positive_excursion_deadline_upper=_deadline_upper(
            positive_face, mean_lower, positive_excursion_growth, precision
        ),
        negative_excursion_deadline_upper=_deadline_upper(
            negative_magnitude, mean_lower, negative_excursion_growth, precision
        ),
        exact_balance_identities_validated_on_diverse_topologies=True,
        exact_fhn_polynomial_identities_validated=True,
        positive_history_orthant_invariance_validated=True,
        negative_history_orthant_invariance_validated=True,
        topology_independent_collective_growth_validated=True,
        arbitrary_finite_node_count_formula_validated=True,
        nodewise_detector_first_hit_validated=True,
        positive_finite_controlled_excursion_validated=True,
        negative_finite_controlled_excursion_validated=True,
        synchronized_scalar_restriction_form_validated=True,
        staged_frequency_amplitude_reset_map_form_validated=True,
        irreducibility_or_unique_stationary_distribution_required=False,
        dobrushin_contraction_required=False,
        rank_one_topology_required=False,
        nodewise_ideal_recovery_clamp_validated=True,
        bounded_actuator_validated=False,
        transverse_attraction_validated=False,
        full_network_periodic_hyperbolicity_validated=False,
        general_topology_canard_root_equivalence_validated=False,
        general_topology_three_output_target_ball_validated=False,
        asynchronous_frequency_amplitude_map_validated=False,
        strict_inward_orthant_boundary_validated=False,
        biological_basin_validated=False,
        hardware_validated=False,
    )


def load_general_network_sign_cone(
    separator_result_path: str | Path,
    *,
    expected_separator_sha256: str = TRACKED_SEPARATOR_RESULT_SHA256,
    precision: int = 160,
    initial_mean_magnitude_lower: str = "0.06",
) -> GeneralNetworkSignConeCertificate:
    """Hash-check the scalar source before deriving the certificate."""

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
    return general_network_sign_cone_from_payload(
        _mapping(payload, "separator payload"),
        separator_result_sha256=digest,
        precision=precision,
        initial_mean_magnitude_lower=initial_mean_magnitude_lower,
    )


def _require_true(mapping: Mapping[str, Any], name: str) -> None:
    if mapping.get(name) is not True:
        raise ValueError(f"proof flag {name!r} must be true")


def _require_false(mapping: Mapping[str, Any], name: str) -> None:
    if mapping.get(name) is not False:
        raise ValueError(f"scope flag {name!r} must be false")


def validate_general_network_sign_cone_result_payload(
    payload: Mapping[str, Any],
) -> None:
    """Refuse missing proof flags and unsupported scope promotions."""

    root = _mapping(payload, "result payload")
    source = _mapping(root.get("source_evidence"), "source_evidence")
    certificate = _mapping(root.get("certificate"), "certificate")
    scope = _mapping(root.get("scope"), "scope")
    if source.get("separator_result_sha256") != TRACKED_SEPARATOR_RESULT_SHA256:
        raise ValueError("result is not bound to the tracked scalar source")
    if certificate.get("separator_result_sha256") != (
        TRACKED_SEPARATOR_RESULT_SHA256
    ):
        raise ValueError("certificate scalar-source digest is invalid")
    if certificate.get("model_id") != MODEL_ID:
        raise ValueError("certificate model identifier is invalid")
    if certificate.get("assumptions_id") != ASSUMPTIONS_ID:
        raise ValueError("certificate balance assumptions are invalid")
    for name in (
        "exact_balance_identities_validated_on_diverse_topologies",
        "exact_fhn_polynomial_identities_validated",
        "positive_history_orthant_invariance_validated",
        "negative_history_orthant_invariance_validated",
        "topology_independent_collective_growth_validated",
        "arbitrary_finite_node_count_formula_validated",
        "nodewise_detector_first_hit_validated",
        "positive_finite_controlled_excursion_validated",
        "negative_finite_controlled_excursion_validated",
        "synchronized_scalar_restriction_form_validated",
        "staged_frequency_amplitude_reset_map_form_validated",
        "nodewise_ideal_recovery_clamp_validated",
    ):
        _require_true(certificate, name)
    for name in (
        "irreducibility_or_unique_stationary_distribution_required",
        "dobrushin_contraction_required",
        "rank_one_topology_required",
        "bounded_actuator_validated",
        "transverse_attraction_validated",
        "full_network_periodic_hyperbolicity_validated",
        "general_topology_canard_root_equivalence_validated",
        "general_topology_three_output_target_ball_validated",
        "asynchronous_frequency_amplitude_map_validated",
        "strict_inward_orthant_boundary_validated",
        "biological_basin_validated",
        "hardware_validated",
    ):
        _require_false(certificate, name)
    for name in (
        "balanced_general_topology_history_orthant_invariance",
        "topology_independent_nodewise_detector_first_hit",
        "topology_independent_finite_controlled_excursion",
        "synchronized_scalar_restriction_form",
        "staged_frequency_amplitude_reset_map_form",
    ):
        _require_true(scope, name)
    for name in (
        "bounded_actuator",
        "transverse_attraction",
        "full_network_periodic_hyperbolicity",
        "general_topology_canard_root_equivalence",
        "general_topology_three_output_target_ball",
        "asynchronous_frequency_amplitude_map",
        "strict_inward_orthant_boundary",
        "biological_basin",
        "hardware",
    ):
        _require_false(scope, name)


def load_general_network_sign_cone_result(
    path: str | Path,
    *,
    expected_sha256: str,
) -> Mapping[str, Any]:
    """Hash-check and semantically validate a result artifact."""

    raw = Path(path).read_bytes()
    digest = sha256(raw).hexdigest()
    if digest != expected_sha256:
        raise ValueError(
            "general-network sign-cone result SHA-256 mismatch: "
            f"expected {expected_sha256}, got {digest}"
        )
    try:
        payload = json.loads(raw)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError("general-network result is not valid UTF-8 JSON") from error
    validate_general_network_sign_cone_result_payload(payload)
    return payload
