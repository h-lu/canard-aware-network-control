"""Directed transfer from squared voltage range to voltage amplitude.

The binary64 collocation record is used only as an *exact finite Fourier
polynomial*.  A fresh parameter-box radii argument then puts the exact RFDE
orbit in a Wiener ball about that polynomial.  In particular, no sampled
maximum or minimum is promoted to an exact-orbit statement.

The second part of the module transfers the already validated target ball in
``(F, R_h)``, where ``R_h=A**2``, to an inner target ball in ``(F, A)``.
This is an inner-ball calculation through the inverse coordinate change, not
an outer Lipschitz estimate for the square-root map.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from typing import Any, Mapping

import gmpy2
import numpy as np

from canard_control.directed_interval import (
    DirectedInterval,
    decimal_lower,
    decimal_upper,
)
from canard_control.fhn_periodic_candidate import (
    FHNPeriodicParameters,
    PeriodicOrbitCandidate,
)
from canard_control.fhn_periodic_parameter_box import (
    DirectedGainBox,
    DirectedPeriodicParameterBoxValidation,
    _state_interval,
    _validate_continuation,
    _validate_extrema,
    _validate_response,
)
from canard_control.fhn_response_target_ball import (
    DirectedDerivativeBoxTargetBall,
    directed_target_ball_from_payload,
)


@dataclass(frozen=True)
class DirectedUnsquaredAmplitudeCertificate:
    """Uniform amplitude enclosure and inner target-ball certificate."""

    candidate_source_sha256: str
    reconstructed_validation_sha256: str
    precision_bits: int
    parameter_center: tuple[str, str]
    gain_half_width: str
    correction_norm_id: str
    exact_orbit_correction_radius: str
    maximum_phase_lower: str
    maximum_phase_upper: str
    minimum_phase_lower: str
    minimum_phase_upper: str
    voltage_maximum_lower: str
    voltage_maximum_upper: str
    voltage_minimum_lower: str
    voltage_minimum_upper: str
    amplitude_lower: str
    amplitude_upper: str
    squared_range_target_radius_lower: str
    unsquared_amplitude_target_radius_lower: str
    target_ball_center: str
    target_ball_inverse_change: str
    candidate_binary64_is_exact_polynomial_data: bool
    candidate_binary64_is_exact_orbit: bool
    exact_orbit_in_wiener_correction_ball: bool
    unique_voltage_extrema_on_gain_box: bool
    uniform_positive_amplitude_enclosure_validated: bool
    frequency_amplitude_target_ball_validated: bool
    calibrated_safety_coordinate_transfer_conditional: bool
    calibrated_three_output_target_ball_validated: bool
    physical_pulse_onset_validated: bool


@dataclass(frozen=True)
class DirectedUnsquaredAmplitudeAudit:
    """Internal audit bundle retained by the source-bound driver."""

    certificate: DirectedUnsquaredAmplitudeCertificate
    parameter_validation: DirectedPeriodicParameterBoxValidation
    squared_range_target_ball: DirectedDerivativeBoxTargetBall


def _mapping(value: object, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{name} must be a mapping")
    return value


def orbit_from_binary64_candidate_payload(
    payload: Mapping[str, Any],
) -> PeriodicOrbitCandidate:
    """Reconstruct the exact binary64 polynomial stored in a candidate JSON.

    JSON numbers are converted to Python floats and hence to the same
    binary64 values that the directed Fourier routines enclose exactly.  The
    function deliberately requires the source record to deny that this
    polynomial is already a validated orbit.
    """

    root = _mapping(payload, "candidate payload")
    claims = _mapping(root.get("claim_status"), "claim_status")
    if claims.get("validated_periodic_orbit") is not False:
        raise ValueError("candidate source must not claim a validated orbit")
    orbit_data = _mapping(root.get("center_orbit"), "center_orbit")
    parameters_data = _mapping(
        orbit_data.get("parameters"), "center_orbit.parameters"
    )
    parameters = FHNPeriodicParameters(
        **{name: float(value) for name, value in parameters_data.items()}
    )
    phase_nodes = np.asarray(orbit_data.get("phase_nodes"), dtype=float)
    state = np.asarray(orbit_data.get("state"), dtype=float)
    if phase_nodes.ndim != 1 or len(phase_nodes) < 5 or len(phase_nodes) % 2 != 1:
        raise ValueError("candidate phase grid must have odd length at least five")
    if state.shape != (len(phase_nodes), 2):
        raise ValueError("candidate state has the wrong shape")
    if not np.all(np.isfinite(phase_nodes)) or not np.all(np.isfinite(state)):
        raise ValueError("candidate arrays must be finite")
    expected_phases = np.arange(len(phase_nodes), dtype=float) / len(phase_nodes)
    if not np.array_equal(phase_nodes, expected_phases):
        raise ValueError("candidate phase nodes are not the declared odd grid")
    return PeriodicOrbitCandidate(
        parameters=parameters,
        phase_nodes=phase_nodes,
        state=state,
        period=float(orbit_data["period"]),
        collocation_residual_inf=float(
            orbit_data["collocation_residual_inf"]
        ),
        oversampled_residual_inf=float(
            orbit_data["oversampled_residual_inf"]
        ),
        newton_iterations=int(orbit_data["newton_iterations"]),
        final_step_inf=float(orbit_data["final_step_inf"]),
        spectral_tail_l1=float(orbit_data["spectral_tail_l1"]),
    )


def _parameter_validation_payload(
    validation: DirectedPeriodicParameterBoxValidation,
) -> dict[str, object]:
    """Build the semantic payload consumed by the target-ball validator."""

    return {
        "validation": asdict(validation),
        "scope": {
            "d1_parameter_box_continuation": validation.d1_validated,
            "d3_unique_voltage_extrema": validation.d3_validated,
            "d4_directed_response_lower_bound": (
                validation.d4_response_lower_bound_validated
            ),
        },
    }


def _public_inner_radius(
    amplitude_lower: str,
    amplitude_upper: str,
    squared_target_radius_lower: str,
    precision: int,
) -> str:
    """Return a public lower radius for the inverse square-coordinate map.

    If ``||(x,y)|| <= r`` in ``(F,A)`` coordinates, then

    ``Delta R_h = 2 A_c y + y**2``.

    It is therefore sufficient that ``r <= rho``, ``r < A_-`` and
    ``(2 A_+ + r) r <= rho``.  The positive root of the last inequality is
    evaluated in its cancellation-free form.  A tiny 2**-100 relative shave
    leaves ample room for re-serialization of the public decimal endpoint.
    """

    a_lower = DirectedInterval.from_decimal(amplitude_lower, precision)
    a_upper = DirectedInterval.from_decimal(amplitude_upper, precision)
    rho = DirectedInterval.from_decimal(
        squared_target_radius_lower, precision
    )
    if a_lower.lower <= 0 or rho.lower <= 0:
        raise ValueError("amplitude and squared target radii must be positive")
    root = rho / ((a_upper * a_upper + rho).sqrt() + a_upper)
    with gmpy2.context(precision=precision, round=gmpy2.RoundDown):
        bound = min(root.lower, rho.lower, a_lower.lower / 2)
        shave = gmpy2.mul_2exp(bound, -100)
        safe = bound - shave
    public = decimal_lower(safe)
    radius = DirectedInterval.from_decimal(public, precision)
    if radius.upper >= a_lower.lower:
        raise RuntimeError("serialized amplitude target radius crosses zero")
    if radius.upper > rho.lower:
        raise RuntimeError("serialized radius exceeds the frequency allowance")
    if ((2 * a_upper + radius) * radius).upper > rho.lower:
        raise RuntimeError("serialized inverse coordinate change exceeds target ball")
    return public


def validate_unsquared_amplitude_transfer(
    orbit: PeriodicOrbitCandidate,
    *,
    candidate_source_sha256: str,
    half_width: str = "1e-12",
    cutoff: int = 144,
    precision: int = 160,
    maximum_radius: str = "5e-9",
    chosen_radius: str = "5e-9",
    phase_partition_count: int = 4096,
) -> DirectedUnsquaredAmplitudeAudit:
    """Validate a uniform amplitude enclosure and its two-output inner ball."""

    if (
        not isinstance(candidate_source_sha256, str)
        or len(candidate_source_sha256) != 64
    ):
        raise ValueError("candidate_source_sha256 must be a 64-character digest")
    try:
        int(candidate_source_sha256, 16)
    except ValueError as error:
        raise ValueError("candidate_source_sha256 must be hexadecimal") from error

    workspace = _validate_continuation(
        orbit,
        half_width=half_width,
        cutoff=cutoff,
        precision=precision,
        maximum_radius=maximum_radius,
        chosen_radius=chosen_radius,
    )
    extrema = _validate_extrema(
        workspace, partition_count=phase_partition_count
    )
    response = _validate_response(workspace, extrema)
    if not workspace.continuation.parameter_box_orbit_validated:
        raise ValueError("the uniform periodic-orbit correction ball failed")
    if not extrema.extrema_validated:
        raise ValueError("the uniform unique-extrema certificate failed")
    if not response.response_box_validated:
        raise ValueError("the squared-range response box failed")

    kappa_1 = workspace.base.parameters["kappa_1"]
    kappa_3 = workspace.base.parameters["kappa_3"]
    gain_box = DirectedGainBox(
        kappa_1_lower=decimal_lower(kappa_1.lower),
        kappa_1_upper=decimal_upper(kappa_1.upper),
        kappa_3_lower=decimal_lower(kappa_3.lower),
        kappa_3_upper=decimal_upper(kappa_3.upper),
        half_width=half_width,
    )
    validation = DirectedPeriodicParameterBoxValidation(
        gain_box=gain_box,
        continuation=workspace.continuation,
        extrema=extrema,
        response=response,
        d1_validated=True,
        d3_validated=True,
        d4_response_lower_bound_validated=True,
        all_d1_d3_d4_validated=True,
        issue_15_closed=False,
        remaining_gates=(
            "directed exclusion of the remaining compact Bloch arc and "
            "full Floquet hyperbolicity",
            "a directed Lipschitz bound for the response derivative "
            "(second sensitivities)",
            "controlled-separator/reset constants and the final target-ball radius",
        ),
    )
    validation_payload = _parameter_validation_payload(validation)
    validation_bytes = (
        json.dumps(validation_payload, sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode("utf-8")
    validation_digest = sha256(validation_bytes).hexdigest()
    target = directed_target_ball_from_payload(
        validation_payload,
        source_result_sha256=validation_digest,
        precision=precision,
        parameter_center=(
            str(float(orbit.parameters.kappa_1)),
            str(float(orbit.parameters.kappa_3)),
        ),
    )

    maximum_phase = DirectedInterval.from_bounds(
        extrema.maximum_phase_lower,
        extrema.maximum_phase_upper,
        precision,
    )
    minimum_phase = DirectedInterval.from_bounds(
        extrema.minimum_phase_lower,
        extrema.minimum_phase_upper,
        precision,
    )
    correction = workspace.chosen_radius.upper
    voltage_maximum = _state_interval(
        workspace.base.voltage, maximum_phase, correction
    )
    voltage_minimum = _state_interval(
        workspace.base.voltage, minimum_phase, correction
    )
    amplitude = voltage_maximum - voltage_minimum
    if amplitude.lower <= 0:
        raise ValueError("the uniform unsquared voltage range is not positive")
    amplitude_lower = decimal_lower(amplitude.lower)
    amplitude_upper = decimal_upper(amplitude.upper)
    amplitude_target_radius = _public_inner_radius(
        amplitude_lower,
        amplitude_upper,
        target.certified_output_ball_radius_lower,
        precision,
    )
    certificate = DirectedUnsquaredAmplitudeCertificate(
        candidate_source_sha256=candidate_source_sha256,
        reconstructed_validation_sha256=validation_digest,
        precision_bits=precision,
        parameter_center=target.parameter_center,
        gain_half_width=half_width,
        correction_norm_id=(
            "real-conjugate component-Wiener coefficient norm plus |T|"
        ),
        exact_orbit_correction_radius=chosen_radius,
        maximum_phase_lower=extrema.maximum_phase_lower,
        maximum_phase_upper=extrema.maximum_phase_upper,
        minimum_phase_lower=extrema.minimum_phase_lower,
        minimum_phase_upper=extrema.minimum_phase_upper,
        voltage_maximum_lower=decimal_lower(voltage_maximum.lower),
        voltage_maximum_upper=decimal_upper(voltage_maximum.upper),
        voltage_minimum_lower=decimal_lower(voltage_minimum.lower),
        voltage_minimum_upper=decimal_upper(voltage_minimum.upper),
        amplitude_lower=amplitude_lower,
        amplitude_upper=amplitude_upper,
        squared_range_target_radius_lower=(
            target.certified_output_ball_radius_lower
        ),
        unsquared_amplitude_target_radius_lower=amplitude_target_radius,
        target_ball_center=(
            "exact (F,A)("
            f"{target.parameter_center[0]},{target.parameter_center[1]}), "
            "with A>0; not a binary64 surrogate"
        ),
        target_ball_inverse_change="Delta R_h = 2 A_c Delta A + (Delta A)^2",
        candidate_binary64_is_exact_polynomial_data=True,
        candidate_binary64_is_exact_orbit=False,
        exact_orbit_in_wiener_correction_ball=True,
        unique_voltage_extrema_on_gain_box=True,
        uniform_positive_amplitude_enclosure_validated=True,
        frequency_amplitude_target_ball_validated=True,
        calibrated_safety_coordinate_transfer_conditional=True,
        calibrated_three_output_target_ball_validated=False,
        physical_pulse_onset_validated=False,
    )
    return DirectedUnsquaredAmplitudeAudit(
        certificate=certificate,
        parameter_validation=validation,
        squared_range_target_ball=target,
    )
