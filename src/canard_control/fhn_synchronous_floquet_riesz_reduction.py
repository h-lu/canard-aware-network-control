"""Riesz reduction of the last synchronous Floquet-index gate.

The existing Bloch certificate excludes nontranslation multipliers on the
unit circle but does not count the multipliers outside it.  This module makes
the next reduction rigorous without manufacturing that missing integer.

For the logarithmic Floquet family ``L_s`` it proves two uniform estimates.

* At Fourier cutoff 64, the infinite tail block is invertible throughout the
  closed half strip ``Re(s) >= 0, |Im(s)| <= pi``.  Hence characteristic
  values in the strip are exactly the zeros, with multiplicity, of a
  258-dimensional analytic Schur complement.
* The complete operator is invertible for ``Re(s) >= 128``.

The local bordered estimate is also recorded in its natural complex form:
it excludes ``0 < |s| <= delta`` in the right half plane, not just imaginary
``s``.  The proof is the same Lyapunov--Schmidt estimate, using
``|exp(-alpha*s)| <= 1`` for ``Re(s) >= 0`` and the integral Taylor
remainder.

The Schur factorization preserves the analytic characteristic
multiplicity of the operator pencil.  A general identification of that
multiplicity with the algebraic multiplicity of the history monodromy is
not asserted here; only the translation value has the previously proved
generalized-Floquet bridge.  Spectral-set correspondence is enough for the
intended zero-winding conclusion.

The module additionally computes a binary64 finite-block determinant winding
on the resulting keyhole contour.  That calculation is a route diagnostic,
not a directed proof: it has no outward-rounded determinant phase and no
validated homotopy from the exact Schur complement to the candidate finite
block.  The false attraction flags are therefore theorem-bearing fields.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Any, Mapping, Sequence

import gmpy2
import numpy as np

from canard_control.directed_interval import (
    DirectedInterval,
    decimal_lower,
    decimal_upper,
    pi_interval,
)
from canard_control.fhn_periodic_candidate import (
    FHNPeriodicParameters,
    PeriodicOrbitCandidate,
)
from canard_control.rfde_floquet_transfer import (
    periodic_orbit_candidate_fingerprint,
)


_TRACKED_PARAMETER_BOX_SHA256 = (
    "ff13b5352c2b4e9898a4044be63fd490a3e7bb4217445a6a062188c2457c22a0"
)
_TRACKED_BLOCH_SHA256 = (
    "c2f93b6cfe6a8e0df3b341476fbe45a83f6fecc0398dbb7340a5213a55357a31"
)
_TRACKED_INDEX_AUDIT_SHA256 = (
    "328a4207863279cd5136a159dbe1a7deecc50d1b3eb1be30b6fd34e66b2af024"
)
_TRACKED_CANDIDATE_SHA256 = (
    "7437514175586665b1bf10831793427e42d8a9cbd736536444be4a98064a3c28"
)
_TRACKED_CANDIDATE_FINGERPRINT = (
    "2b56b5dff18c5aacd1450252824f5601ba3826f6de5d82eb2380853d3c518169"
)
_MODEL_ID = "dual-scaffold-rank-one-two-module-fhn-two-delay"
_SPLIT_NORM_ID = "complex-component-wiener-l1-split-re-im"
_LOCAL_COMPLEXIFICATION_NORM_ID = (
    "complexification-of-real-conjugate-component-wiener-l1"
)
_TAIL_OUTER_NORM_ID = "complex-component-wiener-l1-modulus"
_CUTOFF = 64
_OUTER_REAL_PART = 128


@dataclass(frozen=True)
class RieszReductionSourceEvidence:
    parameter_box_result_sha256: str
    bloch_result_sha256: str
    index_audit_result_sha256: str
    candidate_result_sha256: str
    candidate_fingerprint: str
    model_id: str


@dataclass(frozen=True)
class FiniteWindingDiagnosticRow:
    edge_subdivision_count: int
    contour_point_count: int
    cutoff: int
    complex_finite_dimension: int
    keyhole_radius: str
    outer_real_part: str
    determinant_phase_winding_binary64: int
    total_unwrapped_phase_change_binary64: str
    winding_residual_binary64: str
    maximum_adjacent_principal_phase_increment_binary64: str
    used_complex_slogdet_phase_not_log_modulus: bool
    outward_rounded_determinant_phase: bool
    exact_schur_to_candidate_boundary_homotopy_validated: bool


@dataclass(frozen=True)
class SynchronousFloquetRieszReduction:
    model_id: str
    parameter_box_result_sha256: str
    bloch_result_sha256: str
    index_audit_result_sha256: str
    candidate_result_sha256: str
    candidate_fingerprint: str
    precision_bits: int
    cutoff: int
    complex_finite_dimension: int
    logarithmic_strip_imaginary_lower: str
    logarithmic_strip_imaginary_upper: str
    current_coefficient_uniform_wiener_upper: str
    delayed_coefficient_uniform_wiener_upper: str
    tail_outer_norm_id: str
    complex_modulus_lower_order_norm_upper: str
    maximum_period_upper: str
    uniform_tail_diagonal_gap_lower: str
    uniform_tail_contraction_upper: str
    uniform_tail_block_invertible_on_closed_right_half_strip: bool
    analytic_finite_schur_reduction_validated: bool
    algebraic_multiplicity_preserved_by_schur_reduction: bool
    general_multiplier_analytic_to_monodromy_multiplicity_bridge_validated: bool
    outer_real_part: str
    outer_half_plane_contraction_upper: str
    no_characteristic_values_at_or_beyond_outer_real_part: bool
    bordered_inverse_norm_upper: str
    minimum_period_lower: str
    local_complex_first_order_coefficient_upper: str
    local_complex_second_order_coefficient_upper: str
    local_complex_exclusion_radius_lower: str
    local_complex_radius_formula: str
    local_complex_border_contraction_validated: bool
    local_complex_keyhole_radius: str
    local_right_half_punctured_disk_excluded: bool
    existing_imaginary_axis_nontranslation_exclusion_bound: bool
    exact_boundary_schur_to_candidate_finite_homotopy_validated: bool
    directed_finite_schur_winding_validated: bool
    directed_nontranslation_right_half_strip_zero_count: int | None
    anchor_unstable_multiplier_count: int | None
    synchronous_stable_index_validated: bool
    synchronous_attraction_validated: bool
    full_network_orbital_attraction_validated: bool
    diagnostic_method: str
    diagnostic_rows: tuple[FiniteWindingDiagnosticRow, ...]
    diagnostic_rows_all_report_zero_winding: bool
    diagnostic_is_directed_proof: bool
    minimal_missing_certificate: str
    failure_reason: str


def _mapping(value: object, label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{label} must be a mapping")
    return value


def _require_true(payload: Mapping[str, Any], key: str) -> None:
    if payload.get(key) is not True:
        raise ValueError(f"required source theorem is absent: {key}")


def _require_false(payload: Mapping[str, Any], key: str) -> None:
    if payload.get(key) is not False:
        raise ValueError(f"source scope was forged or promoted: {key}")


def _validate_evidence(evidence: RieszReductionSourceEvidence) -> None:
    expected = (
        (evidence.parameter_box_result_sha256, _TRACKED_PARAMETER_BOX_SHA256),
        (evidence.bloch_result_sha256, _TRACKED_BLOCH_SHA256),
        (evidence.index_audit_result_sha256, _TRACKED_INDEX_AUDIT_SHA256),
        (evidence.candidate_result_sha256, _TRACKED_CANDIDATE_SHA256),
        (evidence.candidate_fingerprint, _TRACKED_CANDIDATE_FINGERPRINT),
        (evidence.model_id, _MODEL_ID),
    )
    if any(actual != wanted for actual, wanted in expected):
        raise ValueError("the Riesz reduction evidence is outside tracked scope")


def _validate_sources(
    bloch_payload: Mapping[str, Any],
    index_payload: Mapping[str, Any],
    evidence: RieszReductionSourceEvidence,
) -> tuple[Mapping[str, Any], Mapping[str, Any]]:
    source = _mapping(bloch_payload.get("source_evidence"), "Bloch source")
    local = _mapping(bloch_payload.get("local_transfer"), "local transfer")
    outer = _mapping(bloch_payload.get("outer_arc"), "outer arc")
    scope = _mapping(bloch_payload.get("scope"), "Bloch scope")
    if source.get("parameter_box_result_sha256") != (
        evidence.parameter_box_result_sha256
    ):
        raise ValueError("the Bloch theorem belongs to a different parameter box")
    if source.get("candidate_fingerprint") != evidence.candidate_fingerprint:
        raise ValueError("the Bloch theorem belongs to a different candidate")
    _require_true(source, "periodic_branch_validated")
    _require_true(source, "bordered_inverse_validated")
    _require_true(source, "moving_delay_period_column_validated")
    _require_true(local, "monodromy_compact")
    _require_true(local, "unit_multiplier_algebraically_simple_validated")
    _require_true(local, "local_unit_circle_exclusion_validated")
    _require_true(outer, "all_nontrivial_unit_multipliers_excluded")
    _require_true(outer, "synchronous_orbital_hyperbolicity_validated")
    _require_false(outer, "attraction_validated")
    _require_true(scope, "synchronous_orbital_hyperbolicity")
    _require_false(scope, "attraction")
    if local.get("norm_id") != _LOCAL_COMPLEXIFICATION_NORM_ID:
        raise ValueError("the local bordered estimate uses a different norm")
    if int(outer.get("cutoff", -1)) != _CUTOFF:
        raise ValueError("the tracked Bloch cutoff changed")
    cells = outer.get("cells")
    if not isinstance(cells, list) or not cells:
        raise ValueError("the Bloch theorem has no directed cells")
    if cells[0].get("norm_id") != _SPLIT_NORM_ID:
        raise ValueError("the tail coefficient bounds use a different norm")

    audit = _mapping(index_payload.get("certificate"), "index audit")
    if audit.get("parameter_box_result_sha256") != (
        evidence.parameter_box_result_sha256
    ):
        raise ValueError("the index audit belongs to a different parameter box")
    if audit.get("bloch_result_sha256") != evidence.bloch_result_sha256:
        raise ValueError("the index audit belongs to a different Bloch theorem")
    if audit.get("candidate_fingerprint") != evidence.candidate_fingerprint:
        raise ValueError("the index audit belongs to a different candidate")
    _require_true(audit, "source_synchronous_orbital_hyperbolicity")
    _require_true(audit, "box_index_transport_ready_after_anchor_count")
    _require_false(audit, "bound_source_ledger_contains_argument_principle_winding")
    _require_false(audit, "synchronous_stable_index_validated")
    _require_false(audit, "synchronous_attraction_validated")
    _require_false(audit, "full_network_orbital_attraction_validated")
    return local, cells[0]


def _orbit_from_payload(payload: Mapping[str, Any]) -> PeriodicOrbitCandidate:
    status = _mapping(payload.get("claim_status"), "candidate status")
    _require_false(status, "directed_interval_proof")
    _require_false(status, "validated_periodic_orbit")
    orbit_data = _mapping(payload.get("center_orbit"), "center orbit")
    parameter_data = _mapping(orbit_data.get("parameters"), "center parameters")
    parameters = FHNPeriodicParameters(
        **{key: float(value) for key, value in parameter_data.items()}
    )
    phases = np.asarray(orbit_data.get("phase_nodes"), dtype=float)
    state = np.asarray(orbit_data.get("state"), dtype=float)
    if phases.shape != (129,) or state.shape != (129, 2):
        raise ValueError("the tracked finite winding requires the 129-node candidate")
    if not np.array_equal(phases, np.arange(129, dtype=float) / 129):
        raise ValueError("the candidate phase grid changed")
    if not np.all(np.isfinite(state)):
        raise ValueError("the candidate state contains a nonfinite entry")
    orbit = PeriodicOrbitCandidate(
        parameters=parameters,
        phase_nodes=phases,
        state=state,
        period=float(orbit_data["period"]),
        collocation_residual_inf=float(orbit_data["collocation_residual_inf"]),
        oversampled_residual_inf=float(orbit_data["oversampled_residual_inf"]),
        newton_iterations=int(orbit_data["newton_iterations"]),
        final_step_inf=float(orbit_data["final_step_inf"]),
        spectral_tail_l1=float(orbit_data["spectral_tail_l1"]),
    )
    if periodic_orbit_candidate_fingerprint(orbit) != (
        _TRACKED_CANDIDATE_FINGERPRINT
    ):
        raise ValueError("the candidate fingerprint changed")
    return orbit


def _number(value: float) -> str:
    if not math.isfinite(value):
        raise ArithmeticError("the finite winding diagnostic became nonfinite")
    return format(float(value), ".17g")


def _finite_candidate_matrix(
    orbit: PeriodicOrbitCandidate,
    logarithmic_exponent: complex,
    *,
    cutoff: int,
) -> np.ndarray:
    """Binary64 finite Bloch matrix; diagnostic only."""

    parameters = orbit.parameters
    period = float(orbit.period)
    voltage = np.asarray(orbit.state[:, 0], dtype=float)
    count = len(voltage)
    half_bandwidth = count // 2
    interpolation_modes = np.concatenate(
        (np.arange(half_bandwidth + 1), np.arange(-half_bandwidth, 0))
    )
    voltage_coefficients = dict(
        zip(
            interpolation_modes,
            np.fft.fft(voltage) / count,
            strict=True,
        )
    )
    ordered_modes = np.arange(-half_bandwidth, half_bandwidth + 1)
    ordered_voltage = np.asarray(
        [voltage_coefficients[int(mode)] for mode in ordered_modes],
        dtype=complex,
    )
    ordered_centered = ordered_voltage.copy()
    ordered_centered[half_bandwidth] -= 1.0
    voltage_squared = np.convolve(ordered_voltage, ordered_voltage)
    centered_squared = np.convolve(ordered_centered, ordered_centered)
    coefficient_modes = np.arange(-2 * half_bandwidth, 2 * half_bandwidth + 1)
    current_values = (
        -voltage_squared
        - 3.0
        * parameters.epsilon
        * parameters.kappa_3
        * centered_squared
    )
    delayed_values = (
        3.0
        * parameters.epsilon
        * parameters.kappa_3
        * centered_squared
        / 2.0
    )
    current_values[2 * half_bandwidth] += (
        1.0 - parameters.epsilon * parameters.kappa_1
    )
    delayed_values[2 * half_bandwidth] += (
        parameters.epsilon * parameters.kappa_1 / 2.0
    )
    current_coefficients = dict(
        zip(coefficient_modes, current_values, strict=True)
    )
    delayed_coefficients = dict(
        zip(coefficient_modes, delayed_values, strict=True)
    )
    modes = np.arange(-cutoff, cutoff + 1)
    span = len(modes)
    differences = modes[:, None] - modes[None, :]
    current = np.zeros((span, span), dtype=complex)
    delayed = np.zeros((span, span), dtype=complex)
    for mode in coefficient_modes:
        mask = differences == mode
        current[mask] = current_coefficients[int(mode)]
        delayed[mask] = delayed_coefficients[int(mode)]
    diagonal = np.diag(logarithmic_exponent + 2.0j * np.pi * modes)
    delayed_operator = np.zeros_like(delayed)
    for delay in parameters.physical_delays:
        alpha = delay / period
        rotation = np.exp(
            -logarithmic_exponent * alpha
            - 2.0j * np.pi * modes * alpha
        )
        delayed_operator += np.diag(rotation) @ delayed
    identity = np.eye(span)
    return np.block(
        [
            [
                diagonal - period * current - period * delayed_operator,
                period * identity,
            ],
            [
                -period * parameters.epsilon * identity,
                diagonal,
            ],
        ]
    )


def _determinant_phase(matrix: np.ndarray) -> float:
    """Return the determinant phase, deliberately not its log modulus."""

    sign, log_modulus = np.linalg.slogdet(np.asarray(matrix, dtype=complex))
    if not np.isfinite(log_modulus) or sign == 0 or not np.isfinite(sign):
        raise ArithmeticError("the finite contour matrix is numerically singular")
    return float(np.angle(sign))


def _keyhole_contour(
    edge_subdivision_count: int,
    *,
    keyhole_radius: float,
    outer_real_part: float,
) -> tuple[complex, ...]:
    if edge_subdivision_count < 24:
        raise ValueError("each keyhole edge requires at least 24 subdivisions")
    if not 0 < keyhole_radius < math.pi:
        raise ValueError("the keyhole radius must lie between zero and pi")
    if outer_real_part <= 0:
        raise ValueError("the outer real part must be positive")

    def line(start: complex, finish: complex) -> list[complex]:
        return list(
            np.linspace(start, finish, edge_subdivision_count + 1, dtype=complex)
        )

    pieces = (
        line(-1.0j * math.pi, outer_real_part - 1.0j * math.pi),
        line(outer_real_part - 1.0j * math.pi, outer_real_part + 1.0j * math.pi),
        line(outer_real_part + 1.0j * math.pi, 1.0j * math.pi),
        line(1.0j * math.pi, 1.0j * keyhole_radius),
        list(
            keyhole_radius
            * np.exp(
                1.0j
                * np.linspace(
                    math.pi / 2.0,
                    -math.pi / 2.0,
                    edge_subdivision_count + 1,
                )
            )
        ),
        line(-1.0j * keyhole_radius, -1.0j * math.pi),
    )
    points: list[complex] = []
    for piece in pieces:
        points.extend(piece if not points else piece[1:])
    if points[0] != points[-1]:
        raise ArithmeticError("the keyhole contour failed to close")
    return tuple(points)


def compute_finite_winding_diagnostic(
    orbit: PeriodicOrbitCandidate,
    *,
    keyhole_radius: float,
    edge_subdivision_counts: Sequence[int] = (24, 48),
    cutoff: int = _CUTOFF,
    outer_real_part: float = float(_OUTER_REAL_PART),
) -> tuple[FiniteWindingDiagnosticRow, ...]:
    requested = tuple(int(value) for value in edge_subdivision_counts)
    if not requested or tuple(sorted(set(requested))) != requested:
        raise ValueError("edge subdivision counts must be strictly increasing")
    rows: list[FiniteWindingDiagnosticRow] = []
    for subdivisions in requested:
        contour = _keyhole_contour(
            subdivisions,
            keyhole_radius=keyhole_radius,
            outer_real_part=outer_real_part,
        )
        phases = np.asarray(
            [
                _determinant_phase(
                    _finite_candidate_matrix(orbit, point, cutoff=cutoff)
                )
                for point in contour
            ],
            dtype=float,
        )
        unwrapped = np.unwrap(phases)
        total = float(unwrapped[-1] - unwrapped[0])
        winding = int(round(total / (2.0 * math.pi)))
        residual = abs(total - 2.0 * math.pi * winding)
        maximum_increment = float(np.max(np.abs(np.diff(unwrapped))))
        rows.append(
            FiniteWindingDiagnosticRow(
                edge_subdivision_count=subdivisions,
                contour_point_count=len(contour),
                cutoff=cutoff,
                complex_finite_dimension=2 * (2 * cutoff + 1),
                keyhole_radius=_number(keyhole_radius),
                outer_real_part=_number(outer_real_part),
                determinant_phase_winding_binary64=winding,
                total_unwrapped_phase_change_binary64=_number(total),
                winding_residual_binary64=_number(residual),
                maximum_adjacent_principal_phase_increment_binary64=_number(
                    maximum_increment
                ),
                used_complex_slogdet_phase_not_log_modulus=True,
                outward_rounded_determinant_phase=False,
                exact_schur_to_candidate_boundary_homotopy_validated=False,
            )
        )
    return tuple(rows)


def build_synchronous_floquet_riesz_reduction(
    bloch_payload: Mapping[str, Any],
    index_payload: Mapping[str, Any],
    candidate_payload: Mapping[str, Any],
    evidence: RieszReductionSourceEvidence,
    *,
    precision: int = 160,
    edge_subdivision_counts: Sequence[int] = (24, 48),
) -> SynchronousFloquetRieszReduction:
    """Build the proved reduction and the explicitly non-directed winding."""

    _validate_evidence(evidence)
    local, cell = _validate_sources(bloch_payload, index_payload, evidence)
    orbit = _orbit_from_payload(candidate_payload)
    if evidence.candidate_fingerprint != periodic_orbit_candidate_fingerprint(
        orbit
    ):
        raise ValueError("the winding orbit belongs to different evidence")

    current_center = DirectedInterval.from_decimal(
        str(cell["current_coefficient_center_norm_upper"]), precision
    )
    current_variation = DirectedInterval.from_decimal(
        str(cell["current_coefficient_variation_upper"]), precision
    )
    delayed_center = DirectedInterval.from_decimal(
        str(cell["delayed_coefficient_center_norm_upper"]), precision
    )
    delayed_variation = DirectedInterval.from_decimal(
        str(cell["delayed_coefficient_variation_upper"]), precision
    )
    period = DirectedInterval.from_decimal(
        str(local["maximum_period_upper"]), precision
    )
    epsilon = DirectedInterval.from_float(orbit.parameters.epsilon, precision)
    current_uniform = current_center + current_variation
    delayed_uniform = delayed_center + delayed_variation
    # The analytic tail and outer-half-plane Neumann estimates are taken in
    # the complex-modulus Wiener norm sum_k(|v_k|+|w_k|).  In that norm a
    # delay rotation has norm one and multiplication by
    # (sigma+i*omega)^(-1) has norm 1/hypot(sigma,omega).  The split Re/Im
    # norm used by the finite Bloch accelerator is equivalent, but its
    # diagonal inverse has the larger norm
    # (sigma+|omega|)/(sigma**2+omega**2), so it must not be paired with the
    # 129*pi denominator below.
    lower_order = max(
        (
            current_uniform
            + 2 * delayed_uniform
            + epsilon
        ).upper,
        DirectedInterval.from_decimal(1, precision).upper,
    )
    pi_box = pi_interval(precision)
    # For |Im(s)| <= pi and |k| >= M+1 the exact gap is 129*pi.
    # Evaluate 2*pi*(M+1)-pi as an interval so both occurrences of pi
    # retain directed endpoints; raw unary negation of an MPFR endpoint
    # would otherwise inherit the process's usual 53-bit context.
    tail_gap = (pi_box * (2 * (_CUTOFF + 1)) - pi_box).lower
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        tail_contraction = period.upper * lower_order / tail_gap
        outer_contraction = (
            period.upper * lower_order / gmpy2.mpfr(_OUTER_REAL_PART)
        )
    if not 0 < tail_contraction < 1:
        raise ArithmeticError("the closed-strip tail contraction is not strict")
    if not 0 < outer_contraction < 1:
        raise ArithmeticError("the outer half-plane contraction is not strict")

    bordered_inverse = DirectedInterval.from_decimal(
        str(local["bordered_inverse_norm_upper"]), precision
    )
    first_coefficient = DirectedInterval.from_decimal(
        str(local["bloch_first_order_coefficient_upper"]), precision
    )
    second_coefficient = DirectedInterval.from_decimal(
        str(local["bloch_second_order_coefficient_upper"]), precision
    )
    minimum_period = DirectedInterval.from_decimal(
        str(local["minimum_period_lower"]), precision
    )
    with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
        first_denominator = bordered_inverse.upper * first_coefficient.upper
        second_denominator = bordered_inverse.upper * second_coefficient.upper
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        first_radius = gmpy2.mpfr(1) / first_denominator
        second_radius = minimum_period.lower / second_denominator
        complex_radius = min(
            first_radius,
            second_radius,
            pi_box.lower,
        ) / 2
    if complex_radius <= 0:
        raise ArithmeticError("the complex bordered exclusion radius vanished")
    source_local_radius = DirectedInterval.from_decimal(
        str(local["local_phase_radius_lower"]), precision
    )
    if complex_radius < source_local_radius.lower:
        # Re-evaluation from printed outward endpoints may lose a final ulp,
        # but it must not lose a material part of the registered radius.
        with gmpy2.context(precision=precision, round=gmpy2.RoundUp):
            relative_loss = (
                source_local_radius.lower - complex_radius
            ) / source_local_radius.lower
        if relative_loss > gmpy2.mpfr("1e-40"):
            raise ArithmeticError("the complex radius disagrees with its sources")
    complex_radius_interval = DirectedInterval.from_bounds(
        complex_radius, complex_radius, precision
    )
    keyhole_radius_interval = complex_radius_interval / 2
    keyhole_radius = float(keyhole_radius_interval.lower)
    if not 0 < keyhole_radius < float(local["local_phase_radius_lower"]):
        raise ArithmeticError("the complex keyhole does not fit the local disk")
    rows = compute_finite_winding_diagnostic(
        orbit,
        keyhole_radius=keyhole_radius,
        edge_subdivision_counts=edge_subdivision_counts,
    )
    all_zero = bool(rows) and all(
        row.determinant_phase_winding_binary64 == 0 for row in rows
    )
    if any(
        row.used_complex_slogdet_phase_not_log_modulus is not True for row in rows
    ):
        raise ArithmeticError("the winding diagnostic used the wrong slogdet field")

    dimension = 2 * (2 * _CUTOFF + 1)
    return SynchronousFloquetRieszReduction(
        model_id=evidence.model_id,
        parameter_box_result_sha256=evidence.parameter_box_result_sha256,
        bloch_result_sha256=evidence.bloch_result_sha256,
        index_audit_result_sha256=evidence.index_audit_result_sha256,
        candidate_result_sha256=evidence.candidate_result_sha256,
        candidate_fingerprint=evidence.candidate_fingerprint,
        precision_bits=precision,
        cutoff=_CUTOFF,
        complex_finite_dimension=dimension,
        logarithmic_strip_imaginary_lower=decimal_lower(
            (-pi_box).lower
        ),
        logarithmic_strip_imaginary_upper=decimal_upper(
            pi_box.upper
        ),
        current_coefficient_uniform_wiener_upper=decimal_upper(
            current_uniform.upper
        ),
        delayed_coefficient_uniform_wiener_upper=decimal_upper(
            delayed_uniform.upper
        ),
        tail_outer_norm_id=_TAIL_OUTER_NORM_ID,
        complex_modulus_lower_order_norm_upper=decimal_upper(lower_order),
        maximum_period_upper=str(local["maximum_period_upper"]),
        uniform_tail_diagonal_gap_lower=decimal_lower(tail_gap),
        uniform_tail_contraction_upper=decimal_upper(tail_contraction),
        uniform_tail_block_invertible_on_closed_right_half_strip=True,
        analytic_finite_schur_reduction_validated=True,
        algebraic_multiplicity_preserved_by_schur_reduction=True,
        general_multiplier_analytic_to_monodromy_multiplicity_bridge_validated=False,
        outer_real_part=str(_OUTER_REAL_PART),
        outer_half_plane_contraction_upper=decimal_upper(outer_contraction),
        no_characteristic_values_at_or_beyond_outer_real_part=True,
        bordered_inverse_norm_upper=str(local["bordered_inverse_norm_upper"]),
        minimum_period_lower=str(local["minimum_period_lower"]),
        local_complex_first_order_coefficient_upper=str(
            local["bloch_first_order_coefficient_upper"]
        ),
        local_complex_second_order_coefficient_upper=str(
            local["bloch_second_order_coefficient_upper"]
        ),
        local_complex_exclusion_radius_lower=decimal_lower(complex_radius),
        local_complex_radius_formula=(
            "0.5*min(1/(D_U*c1_U), T_minus/(D_U*c2_U), pi)"
        ),
        local_complex_border_contraction_validated=True,
        local_complex_keyhole_radius=decimal_lower(
            keyhole_radius_interval.lower
        ),
        local_right_half_punctured_disk_excluded=True,
        existing_imaginary_axis_nontranslation_exclusion_bound=True,
        exact_boundary_schur_to_candidate_finite_homotopy_validated=False,
        directed_finite_schur_winding_validated=False,
        directed_nontranslation_right_half_strip_zero_count=None,
        anchor_unstable_multiplier_count=None,
        synchronous_stable_index_validated=False,
        synchronous_attraction_validated=False,
        full_network_orbital_attraction_validated=False,
        diagnostic_method=(
            "binary64 determinant phase of the unaliased-convolution cutoff-64 "
            "candidate finite Bloch block on a logarithmic keyhole contour"
        ),
        diagnostic_rows=rows,
        diagnostic_rows_all_report_zero_winding=all_zero,
        diagnostic_is_directed_proof=False,
        minimal_missing_certificate=(
            "for the zero-index conclusion, validate the exact-Schur-to-"
            "candidate-finite homotopy on the whole keyhole boundary and "
            "enclose the cutoff-64 determinant phase winding as the integer "
            "zero; a general analytic-to-monodromy multiplicity bridge is "
            "separate and is not needed to prove absence"
        ),
        failure_reason=(
            "the finite determinant winding is binary64 and the boundary "
            "homotopy from the exact Schur complement is not yet directed"
        ),
    )


def validate_synchronous_floquet_riesz_result_payload(
    payload: Mapping[str, Any],
) -> None:
    """Reject a stale or scope-promoted tracked reduction payload."""

    root = _mapping(payload, "Riesz result")
    certificate = _mapping(root.get("certificate"), "Riesz certificate")
    scope = _mapping(root.get("scope"), "Riesz scope")
    source = _mapping(root.get("source_evidence"), "Riesz source")
    expected_source = {
        "parameter_box_result_sha256": _TRACKED_PARAMETER_BOX_SHA256,
        "bloch_result_sha256": _TRACKED_BLOCH_SHA256,
        "index_audit_result_sha256": _TRACKED_INDEX_AUDIT_SHA256,
        "candidate_result_sha256": _TRACKED_CANDIDATE_SHA256,
        "candidate_fingerprint": _TRACKED_CANDIDATE_FINGERPRINT,
        "model_id": _MODEL_ID,
    }
    if any(source.get(key) != value for key, value in expected_source.items()):
        raise ValueError("the tracked Riesz result has different source evidence")
    if certificate.get("cutoff") != _CUTOFF:
        raise ValueError("the tracked Riesz cutoff changed")
    if certificate.get("complex_finite_dimension") != 2 * (2 * _CUTOFF + 1):
        raise ValueError("the finite Schur dimension changed")
    if certificate.get("tail_outer_norm_id") != _TAIL_OUTER_NORM_ID:
        raise ValueError("the tail/outer Neumann estimates use the wrong norm")
    for key in (
        "uniform_tail_block_invertible_on_closed_right_half_strip",
        "analytic_finite_schur_reduction_validated",
        "algebraic_multiplicity_preserved_by_schur_reduction",
        "no_characteristic_values_at_or_beyond_outer_real_part",
        "local_complex_border_contraction_validated",
        "local_right_half_punctured_disk_excluded",
        "existing_imaginary_axis_nontranslation_exclusion_bound",
    ):
        _require_true(certificate, key)
    for key in (
        "exact_boundary_schur_to_candidate_finite_homotopy_validated",
        "directed_finite_schur_winding_validated",
        "synchronous_stable_index_validated",
        "synchronous_attraction_validated",
        "full_network_orbital_attraction_validated",
        "diagnostic_is_directed_proof",
        "general_multiplier_analytic_to_monodromy_multiplicity_bridge_validated",
    ):
        _require_false(certificate, key)
    if certificate.get("directed_nontranslation_right_half_strip_zero_count") is not None:
        raise ValueError("an unproved directed zero count was inserted")
    if certificate.get("anchor_unstable_multiplier_count") is not None:
        raise ValueError("an unproved unstable multiplier count was inserted")
    tail = float(certificate.get("uniform_tail_contraction_upper", math.inf))
    outer = float(certificate.get("outer_half_plane_contraction_upper", math.inf))
    if not 0 < tail < 1 or not 0 < outer < 1:
        raise ValueError("a strict Riesz-reduction contraction was lost")
    rows = certificate.get("diagnostic_rows")
    if not isinstance(rows, list) or len(rows) < 2:
        raise ValueError("the finite winding convergence table is absent")
    subdivisions: list[int] = []
    for row_value in rows:
        row = _mapping(row_value, "finite winding row")
        subdivisions.append(int(row.get("edge_subdivision_count", -1)))
        if row.get("determinant_phase_winding_binary64") != 0:
            raise ValueError("the tracked finite winding diagnostic changed")
        _require_true(row, "used_complex_slogdet_phase_not_log_modulus")
        _require_false(row, "outward_rounded_determinant_phase")
        _require_false(
            row, "exact_schur_to_candidate_boundary_homotopy_validated"
        )
    if subdivisions != sorted(set(subdivisions)):
        raise ValueError("the finite winding resolutions are not increasing")
    for key in (
        "uniform_right_half_strip_tail_block_invertibility",
        "analytic_258_dimensional_schur_reduction",
        "outer_half_plane_exclusion_from_real_part_128",
        "local_complex_right_half_keyhole_exclusion",
    ):
        _require_true(scope, key)
    for key in (
        "general_multiplier_analytic_to_monodromy_multiplicity_bridge",
        "directed_finite_schur_winding",
        "synchronous_stable_index",
        "synchronous_attraction",
        "full_network_orbital_attraction",
    ):
        _require_false(scope, key)
