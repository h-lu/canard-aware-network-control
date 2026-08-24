"""Executable audit of the missing synchronous Floquet stability index.

The tracked Bloch certificate proves that the autonomous multiplier one is
algebraically simple and that no other multiplier lies on the unit circle.
That is an orbital-hyperbolicity theorem, not a stable-index computation.
This module deliberately keeps those two statements separate.

It also supplies a reproducible *floating-point diagnostic* of the center
monodromy.  The diagnostic is a Fourier-interpolated, cubic-history,
Runge--Kutta method-of-steps discretization.  It is useful for choosing the
next validated computation, but it has no directed truncation or resolvent
error and therefore cannot set an attraction flag.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Any, Mapping, Sequence

import numpy as np


_TRACKED_PARAMETER_BOX_SHA256 = (
    "ff13b5352c2b4e9898a4044be63fd490a3e7bb4217445a6a062188c2457c22a0"
)
_TRACKED_BLOCH_SHA256 = (
    "c2f93b6cfe6a8e0df3b341476fbe45a83f6fecc0398dbb7340a5213a55357a31"
)
_TRACKED_TRANSVERSE_SHA256 = (
    "ec4b3204695bf40d4309681b0f57d93e3e1e524ca3680cdce316aaee8ad015fb"
)
_TRACKED_CANDIDATE_SHA256 = (
    "7437514175586665b1bf10831793427e42d8a9cbd736536444be4a98064a3c28"
)
_TRACKED_CANDIDATE_FINGERPRINT = (
    "2b56b5dff18c5aacd1450252824f5601ba3826f6de5d82eb2380853d3c518169"
)
_MODEL_ID = "dual-scaffold-rank-one-two-module-fhn-two-delay"


@dataclass(frozen=True)
class FloquetIndexSourceEvidence:
    """Hashes and identifiers of the source ledger audited here."""

    parameter_box_result_sha256: str
    bloch_result_sha256: str
    transverse_result_sha256: str
    candidate_result_sha256: str
    candidate_fingerprint: str
    model_id: str


@dataclass(frozen=True)
class FloquetDiagnosticRow:
    """One non-directed finite-dimensional monodromy diagnostic."""

    step_count: int
    retained_history_steps: int
    matrix_dimension: int
    neutral_multiplier_real: str
    neutral_multiplier_imag: str
    neutral_multiplier_modulus: str
    neutral_multiplier_error_from_one: str
    leading_nontrivial_multiplier_real: str
    leading_nontrivial_multiplier_imag: str
    leading_nontrivial_multiplier_modulus: str
    second_nontrivial_multiplier_real: str
    second_nontrivial_multiplier_imag: str
    second_nontrivial_multiplier_modulus: str
    observed_nontrivial_outside_unit_disk_count: int
    outward_rounded: bool
    operator_norm_error_bound: str | None
    contour_resolvent_bound: str | None


@dataclass(frozen=True)
class SynchronousFloquetIndexAudit:
    """Proof ledger; false flags are part of the mathematical result."""

    model_id: str
    parameter_box_result_sha256: str
    bloch_result_sha256: str
    transverse_result_sha256: str
    candidate_result_sha256: str
    candidate_fingerprint: str
    source_periodic_branch_validated: bool
    source_monodromy_compact: bool
    source_unit_multiplier_algebraically_simple: bool
    source_all_nontrivial_unit_multipliers_excluded: bool
    source_synchronous_orbital_hyperbolicity: bool
    source_fixed_topology_transverse_variational_decay: bool
    box_index_transport_ready_after_anchor_count: bool
    bound_source_ledger_contains_anchor_multiplier_count: bool
    bound_source_ledger_contains_argument_principle_winding: bool
    bound_source_ledger_contains_validated_gain_homotopy: bool
    anchor_unstable_multiplier_count: int | None
    synchronous_stable_index_validated: bool
    synchronous_attraction_validated: bool
    full_network_orbital_attraction_validated: bool
    quantitative_synchronous_decay_rate_validated: bool
    diagnostic_method: str
    diagnostic_rows: tuple[FloquetDiagnosticRow, ...]
    diagnostic_consistent_with_zero_unstable_count: bool
    diagnostic_is_directed_proof: bool
    ode_anchor_nontrivial_multiplier_binary64: str
    ode_anchor_direct_theorem_applies: bool
    ode_to_target_homotopy_interval_validated: bool
    ode_to_target_c0_distance_binary64: str
    minimal_missing_certificate: str
    preferred_executable_route: tuple[str, ...]
    alternative_executable_route: tuple[str, ...]
    failure_reason: str


def _require_mapping(value: Any, label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{label} must be a mapping")
    return value


def _require_true(mapping: Mapping[str, Any], key: str) -> None:
    if mapping.get(key) is not True:
        raise ValueError(f"required validated source flag is absent: {key}")


def _require_false(mapping: Mapping[str, Any], key: str) -> None:
    if mapping.get(key) is not False:
        raise ValueError(f"source scope was forged or promoted: {key}")


def _number(value: float) -> str:
    if not math.isfinite(value):
        raise ArithmeticError("the floating diagnostic produced a nonfinite value")
    return format(float(value), ".17g")


def _validate_evidence(evidence: FloquetIndexSourceEvidence) -> None:
    expected = {
        "parameter-box": (
            evidence.parameter_box_result_sha256,
            _TRACKED_PARAMETER_BOX_SHA256,
        ),
        "Bloch": (evidence.bloch_result_sha256, _TRACKED_BLOCH_SHA256),
        "transverse": (
            evidence.transverse_result_sha256,
            _TRACKED_TRANSVERSE_SHA256,
        ),
        "candidate": (
            evidence.candidate_result_sha256,
            _TRACKED_CANDIDATE_SHA256,
        ),
        "candidate fingerprint": (
            evidence.candidate_fingerprint,
            _TRACKED_CANDIDATE_FINGERPRINT,
        ),
        "model": (evidence.model_id, _MODEL_ID),
    }
    for label, (actual, wanted) in expected.items():
        if actual != wanted:
            raise ValueError(f"the {label} evidence is outside the tracked scope")


def _validate_bloch_payload(
    payload: Mapping[str, Any], evidence: FloquetIndexSourceEvidence
) -> None:
    source = _require_mapping(payload.get("source_evidence"), "Bloch source")
    local = _require_mapping(payload.get("local_transfer"), "local transfer")
    outer = _require_mapping(payload.get("outer_arc"), "outer arc")
    scope = _require_mapping(payload.get("scope"), "Bloch scope")
    if source.get("parameter_box_result_sha256") != (
        evidence.parameter_box_result_sha256
    ):
        raise ValueError("the Bloch theorem belongs to a different parameter box")
    if source.get("candidate_fingerprint") != evidence.candidate_fingerprint:
        raise ValueError("the Bloch theorem belongs to a different orbit candidate")
    _require_true(source, "periodic_branch_validated")
    _require_true(local, "monodromy_compact")
    _require_true(local, "regularity_bridge_to_history_monodromy")
    _require_true(local, "unit_multiplier_algebraically_simple_validated")
    _require_true(outer, "all_nontrivial_unit_multipliers_excluded")
    _require_true(outer, "synchronous_orbital_hyperbolicity_validated")
    _require_true(scope, "synchronous_orbital_hyperbolicity")
    _require_false(outer, "attraction_validated")
    _require_false(scope, "attraction")
    _require_false(scope, "full_network_transverse_stability")


def _validate_transverse_payload(
    payload: Mapping[str, Any], evidence: FloquetIndexSourceEvidence
) -> None:
    source = _require_mapping(payload.get("source_evidence"), "transverse source")
    certificate = _require_mapping(payload.get("certificate"), "transverse cert")
    scope = _require_mapping(payload.get("scope"), "transverse scope")
    if source.get("bloch_result_sha256") != evidence.bloch_result_sha256:
        raise ValueError("the transverse theorem is bound to a different Bloch result")
    if source.get("parameter_box_result_sha256") != (
        evidence.parameter_box_result_sha256
    ):
        raise ValueError("the transverse theorem is bound to a different box")
    if certificate.get("model_id") != evidence.model_id:
        raise ValueError("the transverse theorem belongs to a different model")
    _require_true(certificate, "source_periodic_branch_validated")
    _require_true(certificate, "source_synchronous_orbital_hyperbolicity_validated")
    _require_true(certificate, "periodic_transverse_variational_decay_validated")
    _require_true(certificate, "full_network_orbital_hyperbolicity_validated")
    _require_true(scope, "periodic_transverse_variational_decay")
    _require_true(scope, "full_network_orbital_hyperbolicity")
    _require_false(certificate, "synchronous_attraction_validated")
    _require_false(certificate, "full_network_attraction_validated")
    _require_false(scope, "synchronous_attraction")
    _require_false(scope, "full_network_attraction")
    _require_false(scope, "general_network_topology")


def _validate_candidate_payload(payload: Mapping[str, Any]) -> None:
    status = _require_mapping(payload.get("claim_status"), "candidate status")
    orbit = _require_mapping(payload.get("center_orbit"), "center orbit")
    parameters = _require_mapping(orbit.get("parameters"), "center parameters")
    route = _require_mapping(
        payload.get("ode_persistence_route"), "ODE persistence route"
    )
    _require_false(status, "directed_interval_proof")
    _require_false(status, "validated_periodic_orbit")
    _require_false(status, "validated_response_box")
    expected = {
        "epsilon": 0.2,
        "kappa_1": 0.2,
        "kappa_3": 0.25,
        "theta_0": 4.0,
        "theta_1": 5.0,
        "unfolding": 0.6,
    }
    if any(float(parameters.get(key, math.nan)) != value for key, value in expected.items()):
        raise ValueError("the floating candidate belongs to a different FHN model")
    if len(orbit.get("state", ())) != 129:
        raise ValueError("the tracked diagnostic requires the 129-node candidate")
    _require_false(route, "direct_single_delay_theorem_applies")


def _periodic_voltage_interpolator(
    voltage: np.ndarray, period: float
):
    count = len(voltage)
    coefficients = np.fft.fft(voltage) / count
    modes = np.fft.fftfreq(count, 1.0 / count)

    def evaluate(time: float) -> float:
        phase = (time / period) % 1.0
        value = np.sum(coefficients * np.exp(2j * np.pi * modes * phase))
        return float(value.real)

    return evaluate


def compute_center_monodromy_diagnostic(
    candidate_payload: Mapping[str, Any],
    *,
    step_counts: Sequence[int] = (150, 250, 400, 600),
) -> tuple[FloquetDiagnosticRow, ...]:
    """Compute a non-directed center monodromy convergence table.

    The history is represented on an equidistant grid with three extra
    interpolation nodes.  Delayed values use four-point cubic Lagrange
    interpolation, while the current two-component variational equation is
    advanced by classical RK4.  No claim is made for the continuum operator.
    """

    _validate_candidate_payload(candidate_payload)
    orbit = _require_mapping(candidate_payload["center_orbit"], "center orbit")
    parameters = _require_mapping(orbit["parameters"], "center parameters")
    period = float(orbit["period"])
    state = np.asarray(orbit["state"], dtype=float)
    if state.shape != (129, 2) or not np.all(np.isfinite(state)):
        raise ValueError("the center state must be a finite 129 by 2 array")
    if period <= 0 or not math.isfinite(period):
        raise ValueError("the center period must be positive and finite")
    requested = tuple(int(item) for item in step_counts)
    if not requested or any(item < 24 for item in requested):
        raise ValueError("each diagnostic resolution must have at least 24 steps")
    if tuple(sorted(set(requested))) != requested:
        raise ValueError("diagnostic step counts must be strictly increasing")

    epsilon = float(parameters["epsilon"])
    kappa_1 = float(parameters["kappa_1"])
    kappa_3 = float(parameters["kappa_3"])
    delays = (
        float(parameters["theta_0"]) / math.sqrt(epsilon),
        float(parameters["theta_1"]) / math.sqrt(epsilon),
    )
    voltage = _periodic_voltage_interpolator(state[:, 0], period)

    def feedback_derivative(value: float) -> float:
        return kappa_1 + 3.0 * kappa_3 * (value - 1.0) ** 2

    rows: list[FloquetDiagnosticRow] = []
    for step_count in requested:
        step = period / step_count
        history_steps = math.ceil(max(delays) / step) + 3
        dimension = history_steps + 2
        voltage_maps: list[np.ndarray | None] = [None] * (
            history_steps + step_count + 1
        )
        for index in range(-history_steps, 1):
            basis = np.zeros(dimension)
            basis[index + history_steps] = 1.0
            voltage_maps[index + history_steps] = basis
        recovery_map = np.zeros(dimension)
        recovery_map[history_steps + 1] = 1.0

        def stored(index: int) -> np.ndarray:
            value = voltage_maps[index + history_steps]
            if value is None:
                raise ArithmeticError("the delayed interpolant requested future data")
            return value

        def delayed_map(index: float) -> np.ndarray:
            left = math.floor(index)
            fraction = index - left
            weights = (
                -fraction * (fraction - 1) * (fraction - 2) / 6,
                (fraction + 1) * (fraction - 1) * (fraction - 2) / 2,
                -(fraction + 1) * fraction * (fraction - 2) / 2,
                (fraction + 1) * fraction * (fraction - 1) / 6,
            )
            return sum(
                weight * stored(node)
                for weight, node in zip(
                    weights, (left - 1, left, left + 1, left + 2)
                )
            )

        def right_hand_side(
            time: float,
            current_voltage: np.ndarray,
            current_recovery: np.ndarray,
            grid_index: int,
            stage: float,
        ) -> tuple[np.ndarray, np.ndarray]:
            orbit_voltage = voltage(time)
            current_coefficient = (
                1.0
                - orbit_voltage**2
                - epsilon * feedback_derivative(orbit_voltage)
            )
            delayed_terms = np.zeros(dimension)
            for delay in delays:
                delayed_terms += feedback_derivative(voltage(time - delay)) * (
                    delayed_map(grid_index + stage - delay / step)
                )
            fast = (
                current_coefficient * current_voltage
                - current_recovery
                + 0.5 * epsilon * delayed_terms
            )
            return fast, epsilon * current_voltage

        for grid_index in range(step_count):
            current_voltage = stored(grid_index)
            k1_v, k1_w = right_hand_side(
                grid_index * step,
                current_voltage,
                recovery_map,
                grid_index,
                0.0,
            )
            k2_v, k2_w = right_hand_side(
                (grid_index + 0.5) * step,
                current_voltage + 0.5 * step * k1_v,
                recovery_map + 0.5 * step * k1_w,
                grid_index,
                0.5,
            )
            k3_v, k3_w = right_hand_side(
                (grid_index + 0.5) * step,
                current_voltage + 0.5 * step * k2_v,
                recovery_map + 0.5 * step * k2_w,
                grid_index,
                0.5,
            )
            k4_v, k4_w = right_hand_side(
                (grid_index + 1.0) * step,
                current_voltage + step * k3_v,
                recovery_map + step * k3_w,
                grid_index,
                1.0,
            )
            voltage_maps[grid_index + 1 + history_steps] = (
                current_voltage
                + step * (k1_v + 2 * k2_v + 2 * k3_v + k4_v) / 6
            )
            recovery_map = recovery_map + step * (
                k1_w + 2 * k2_w + 2 * k3_w + k4_w
            ) / 6

        monodromy = np.vstack(
            [
                stored(index)
                for index in range(step_count - history_steps, step_count + 1)
            ]
            + [recovery_map]
        )
        eigenvalues = np.linalg.eigvals(monodromy)
        neutral_index = int(np.argmin(np.abs(eigenvalues - 1.0)))
        neutral = complex(eigenvalues[neutral_index])
        nontrivial = np.delete(eigenvalues, neutral_index)
        order = np.argsort(-np.abs(nontrivial))
        leading = complex(nontrivial[order[0]])
        second = complex(nontrivial[order[1]])
        rows.append(
            FloquetDiagnosticRow(
                step_count=step_count,
                retained_history_steps=history_steps,
                matrix_dimension=dimension,
                neutral_multiplier_real=_number(neutral.real),
                neutral_multiplier_imag=_number(neutral.imag),
                neutral_multiplier_modulus=_number(abs(neutral)),
                neutral_multiplier_error_from_one=_number(abs(neutral - 1.0)),
                leading_nontrivial_multiplier_real=_number(leading.real),
                leading_nontrivial_multiplier_imag=_number(leading.imag),
                leading_nontrivial_multiplier_modulus=_number(abs(leading)),
                second_nontrivial_multiplier_real=_number(second.real),
                second_nontrivial_multiplier_imag=_number(second.imag),
                second_nontrivial_multiplier_modulus=_number(abs(second)),
                observed_nontrivial_outside_unit_disk_count=int(
                    np.count_nonzero(np.abs(nontrivial) > 1.0)
                ),
                outward_rounded=False,
                operator_norm_error_bound=None,
                contour_resolvent_bound=None,
            )
        )
    return tuple(rows)


def audit_synchronous_floquet_index(
    bloch_payload: Mapping[str, Any],
    transverse_payload: Mapping[str, Any],
    candidate_payload: Mapping[str, Any],
    evidence: FloquetIndexSourceEvidence,
    *,
    diagnostic_rows: Sequence[FloquetDiagnosticRow],
    anchor_index_evidence: Mapping[str, Any] | None = None,
) -> SynchronousFloquetIndexAudit:
    """Audit the bound ledger and refuse an unsupported stability promotion."""

    _validate_evidence(evidence)
    _validate_bloch_payload(bloch_payload, evidence)
    _validate_transverse_payload(transverse_payload, evidence)
    _validate_candidate_payload(candidate_payload)
    if anchor_index_evidence is not None:
        raise ValueError(
            "no tracked directed anchor-index artifact is registered; "
            "self-declared flags cannot promote attraction"
        )
    rows = tuple(diagnostic_rows)
    if not rows:
        raise ValueError("the audit requires at least one diagnostic resolution")
    if any(row.outward_rounded for row in rows):
        raise ValueError("the floating diagnostic must not be relabeled as directed")
    if any(
        row.operator_norm_error_bound is not None
        or row.contour_resolvent_bound is not None
        for row in rows
    ):
        raise ValueError("unvalidated diagnostic error fields must remain null")
    if tuple(sorted(row.step_count for row in rows)) != tuple(
        row.step_count for row in rows
    ):
        raise ValueError("diagnostic rows must be ordered by increasing resolution")

    leading_moduli = [
        float(row.leading_nontrivial_multiplier_modulus) for row in rows
    ]
    neutral_errors = [float(row.neutral_multiplier_error_from_one) for row in rows]
    diagnostic_consistent = (
        all(value < 1.0 for value in leading_moduli)
        and all(row.observed_nontrivial_outside_unit_disk_count == 0 for row in rows)
        and neutral_errors[-1] < 1.0e-5
        and (
            len(rows) == 1
            or abs(leading_moduli[-1] - leading_moduli[-2]) < 1.0e-4
        )
    )
    ode_route = _require_mapping(
        candidate_payload["ode_persistence_route"], "ODE persistence route"
    )
    ode_multipliers = tuple(float(item) for item in ode_route["ode_floquet_multipliers"])
    if len(ode_multipliers) != 2:
        raise ValueError("the planar ODE diagnostic must contain two multipliers")
    ode_nontrivial = min(ode_multipliers, key=lambda item: abs(item - 1.0))
    ode_nontrivial = next(
        item for item in ode_multipliers if item != ode_nontrivial
    )

    return SynchronousFloquetIndexAudit(
        model_id=evidence.model_id,
        parameter_box_result_sha256=evidence.parameter_box_result_sha256,
        bloch_result_sha256=evidence.bloch_result_sha256,
        transverse_result_sha256=evidence.transverse_result_sha256,
        candidate_result_sha256=evidence.candidate_result_sha256,
        candidate_fingerprint=evidence.candidate_fingerprint,
        source_periodic_branch_validated=True,
        source_monodromy_compact=True,
        source_unit_multiplier_algebraically_simple=True,
        source_all_nontrivial_unit_multipliers_excluded=True,
        source_synchronous_orbital_hyperbolicity=True,
        source_fixed_topology_transverse_variational_decay=True,
        box_index_transport_ready_after_anchor_count=True,
        bound_source_ledger_contains_anchor_multiplier_count=False,
        bound_source_ledger_contains_argument_principle_winding=False,
        bound_source_ledger_contains_validated_gain_homotopy=False,
        anchor_unstable_multiplier_count=None,
        synchronous_stable_index_validated=False,
        synchronous_attraction_validated=False,
        full_network_orbital_attraction_validated=False,
        quantitative_synchronous_decay_rate_validated=False,
        diagnostic_method=(
            "binary64 cubic-history Fourier-coefficient RK4 method-of-steps "
            "monodromy discretization"
        ),
        diagnostic_rows=rows,
        diagnostic_consistent_with_zero_unstable_count=diagnostic_consistent,
        diagnostic_is_directed_proof=False,
        ode_anchor_nontrivial_multiplier_binary64=_number(ode_nontrivial),
        ode_anchor_direct_theorem_applies=False,
        ode_to_target_homotopy_interval_validated=False,
        ode_to_target_c0_distance_binary64=_number(
            float(ode_route["target_orbit_c0_distance_after_discrete_phase_alignment"])
        ),
        minimal_missing_certificate=(
            "one directed center-anchor certificate proving that the algebraic "
            "count of nontranslation monodromy multipliers with modulus greater "
            "than one is exactly zero"
        ),
        preferred_executable_route=(
            "deflate the algebraically simple translation multiplier using a "
            "validated tangent/adjoint rank-one projector",
            "construct an analytic Fredholm or Riesz-index object on an annular "
            "multiplier contour and prove an outer resolvent bound",
            "enclose its finite-section winding and the finite-to-tail homotopy "
            "with directed complex intervals",
            "certify the resulting integer unstable count as zero at the center",
            "transport that integer over the connected gain box using the existing "
            "uniform nontrivial unit-circle exclusion",
        ),
        alternative_executable_route=(
            "validate the planar zero-gain FHN cycle and its divergence multiplier",
            "continue the periodic branch over the entire gain homotopy from zero "
            "to the target gains",
            "prove simple translation and exclude every other unit multiplier "
            "uniformly along that full homotopy",
        ),
        failure_reason=(
            "unit-circle exclusion preserves an already known unstable index but "
            "does not determine the index; the bound ledger contains no anchor "
            "count, directed winding, or validated full gain homotopy"
        ),
    )


__all__ = [
    "FloquetDiagnosticRow",
    "FloquetIndexSourceEvidence",
    "SynchronousFloquetIndexAudit",
    "audit_synchronous_floquet_index",
    "compute_center_monodromy_diagnostic",
]
