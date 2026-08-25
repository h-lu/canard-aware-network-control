"""Strict replay contract for leaky-recovery periodic branch candidates.

The tracked artifacts governed by this module freeze *binary64
trigonometric polynomials*.  Such a polynomial alone is not an RFDE orbit.
The nested directed calculation and the independent leaky-majorant audit
together validate the registered inner phase-fixed RFDE orbit and its
bordered derivative.  Floquet multiplicity and index flags remain false.

The validator has three independent duties.

* It binds the artifact to its generator and all source files used by the
  replay calculation.
* It reconstructs the exact binary64 phase grid, state samples, phase
  reference, period, and equation parameters and recomputes the finite
  collocation diagnostics.
* It locks the complete branch body to a source-registered SHA-256 digest.
  A caller may additionally request the expensive directed-radii replay.

No directed enclosure is inferred from the recomputed binary64 residuals.
"""

from __future__ import annotations

from dataclasses import asdict, fields
from decimal import Decimal, InvalidOperation, localcontext
from hashlib import sha256
import json
import math
from pathlib import Path
import platform
from typing import Any, Mapping

import gmpy2
import numpy as np
import scipy

from canard_control.fhn_periodic_candidate import (
    FHNPeriodicParameters,
    PeriodicOrbitCandidate,
    odd_fourier_matrices,
)
from canard_control.fhn_periodic_infinite_validation import (
    DealiasedFiniteCoefficientCertificate,
    DirectedCorrectionRadiiBound,
    DirectedFiniteTailBlocks,
)
from canard_control.leaky_periodic_validation import (
    DirectedLeakyPeriodicValidation,
    LeakyFloquetValidationContract,
    evaluate_leaky_periodic_radii_candidate,
)


SCHEMA_ID = "leaky-periodic-branch-binary64-artifact-v2"
SOURCE_RELATIVE_PATH = (
    "src/canard_control/leaky_periodic_branch_artifact.py"
)
GENERATOR_RELATIVE_PATH = (
    "experiments/autonomous_leaky_recovery_periodic_branch_artifact.py"
)
PARENT_PROBE_RELATIVE_PATH = (
    "experiments/autonomous_leaky_recovery_bistable_probe.py"
)
LEAKY_VALIDATOR_RELATIVE_PATH = (
    "src/canard_control/leaky_periodic_validation.py"
)
RESULT_RELATIVE_PATHS = {
    "inner_saddle_candidate": (
        "experiments/results/"
        "autonomous_leaky_recovery_inner_branch_artifact.json"
    ),
    "outer_pulse": (
        "experiments/results/"
        "autonomous_leaky_recovery_outer_branch_artifact.json"
    ),
}
DEFAULT_COMMANDS = {
    branch: (
        "OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONPATH=src "
        "/usr/bin/python3 "
        "experiments/autonomous_leaky_recovery_periodic_branch_artifact.py "
        f"--branch {branch}"
    )
    for branch in RESULT_RELATIVE_PATHS
}

SOURCE_MANIFEST = (
    SOURCE_RELATIVE_PATH,
    GENERATOR_RELATIVE_PATH,
    PARENT_PROBE_RELATIVE_PATH,
    LEAKY_VALIDATOR_RELATIVE_PATH,
    "src/canard_control/leaky_periodic_majorant_audit.py",
    "src/canard_control/fhn_periodic_candidate.py",
    "src/canard_control/fhn_periodic_directed_validation.py",
    "src/canard_control/fhn_periodic_infinite_validation.py",
    "src/canard_control/directed_interval.py",
)

MODEL_EQUATION = (
    "v'=v-v^3/3-w+epsilon*kappa_1*((v_tau0+v_tau1)/2-v)"
    "+epsilon*kappa_3*(((v_tau0-1)^3+(v_tau1-1)^3)/2"
    "-(v-1)^3); w'=epsilon*(v-a-w)"
)
REPRESENTATION = (
    "exact binary64 samples of an odd-grid real trigonometric polynomial; "
    "the samples are candidate data, not an exact RFDE orbit"
)
PHASE_BORDER = (
    "mean Euclidean pairing with D_phase(reference); reference and state "
    "are stored as exact binary64 samples"
)
ARITHMETIC_SCOPE = (
    "The branch polynomial and finite collocation diagnostics are IEEE-754 "
    "binary64. The nested directed-radii prototype uses MPFR-directed "
    "interval endpoints around that exact binary64 polynomial and a NumPy "
    "midpoint inverse with a directed product-error bound. The leaky "
    "majorant adaptation is independently audited. For the registered inner "
    "artifact the negative radii polynomial validates a phase-fixed RFDE "
    "orbit and its bordered derivative; no Floquet multiplicity or index is "
    "inferred."
)

MODEL_VALUES = {
    "epsilon": 1.0 / 5.0,
    "unfolding_a": 1.0 / 4.0,
    "recovery_leak_b": 1.0,
    "kappa_1": 1.0 / 250.0,
    "kappa_3": 1.0 / 200.0,
    "theta_0": 4.0,
    "theta_1": 5.0,
    "tau_0": 4.0 * math.sqrt(5.0),
    "tau_1": 5.0 * math.sqrt(5.0),
    "delay_weight_0": 1.0 / 2.0,
    "delay_weight_1": 1.0 / 2.0,
}

# A ``None`` entry denotes a generator route for which no tracked body has
# yet been registered.  The digest excludes the manifest, so adding a source
# lock does not create a hash cycle.
EXPECTED_ARTIFACT_SHA256 = {
    "inner_saddle_candidate": (
        "35c3737f8970c54cf28fa9911325e3785ea01c3e76c3d3efe531f344726e759a"
    ),
    "outer_pulse": None,
}

CLAIM_STATUS = {
    "exact_binary64_polynomial_replay_artifact": True,
    "finite_collocation_residual_recomputed": True,
    "directed_radii_prototype_evaluated": True,
    "directed_radii_formula_adaptation_independently_audited": True,
    "periodic_rfde_orbit_validated": True,
    "phase_bordered_rfde_inverse_validated": True,
    "neutral_multiplier_algebraically_simple_validated": False,
    "nontranslation_unit_circle_exclusion_validated": False,
    "unstable_multiplier_count_validated": False,
    "attracting_or_saddle_floquet_index_validated": False,
}

# The directed prototype contains a NumPy midpoint inverse.  Different
# deterministic BLAS reduction trees can change the last few bits of that
# midpoint while the subsequent MPFR bounds and every proof gate remain the
# same.  Replay therefore compares decimal bounds with this fixed, very
# small tolerance and the sum of the two independently directed finite
# inverse-defect bounds, instead of requiring brittle decimal-string
# identity.  The gate booleans and their defining inequality signs are
# still checked exactly below, with every strict slack larger than that
# defect buffer.
DIRECTED_REPLAY_RELATIVE_TOLERANCE = Decimal("1e-10")
DIRECTED_REPLAY_ABSOLUTE_TOLERANCE = Decimal("1e-18")


def _sha256_path(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def canonical_sha256(value: object) -> str:
    """Hash one JSON value with a deterministic UTF-8 encoding."""

    encoded = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    return sha256(encoded).hexdigest()


def binary64_record(value: float) -> dict[str, str]:
    """Return a readable and bit-exact record of one finite binary64."""

    number = float(value)
    if not math.isfinite(number):
        raise ValueError("binary64 artifact values must be finite")
    return {
        "binary64_hex": number.hex(),
        "decimal": format(number, ".17g"),
    }


def _binary64_from_record(value: object, name: str) -> float:
    if not isinstance(value, Mapping) or set(value) != {
        "binary64_hex",
        "decimal",
    }:
        raise ValueError(f"{name} must be a complete binary64 record")
    hexadecimal = value.get("binary64_hex")
    decimal = value.get("decimal")
    if not isinstance(hexadecimal, str) or not isinstance(decimal, str):
        raise ValueError(f"{name} binary64 fields must be strings")
    try:
        number = float.fromhex(hexadecimal)
        decimal_number = float(decimal)
    except ValueError as error:
        raise ValueError(f"{name} is not a binary64 number") from error
    if not math.isfinite(number) or not math.isfinite(decimal_number):
        raise ValueError(f"{name} must be finite")
    if number.hex() != hexadecimal:
        raise ValueError(f"{name} hexadecimal encoding is not canonical")
    if format(number, ".17g") != decimal or decimal_number != number:
        raise ValueError(f"{name} decimal and hexadecimal values disagree")
    return number


def _binary64_array(value: object, name: str, ndim: int) -> np.ndarray:
    try:
        array = np.asarray(
            [
                [float.fromhex(item) for item in row]
                if ndim == 2
                else float.fromhex(row)
                for row in value  # type: ignore[union-attr]
            ],
            dtype=float,
        )
    except (TypeError, ValueError) as error:
        raise ValueError(f"{name} must contain binary64 hexadecimal strings") from error
    if array.ndim != ndim or not np.all(np.isfinite(array)):
        raise ValueError(f"{name} has wrong shape or nonfinite entries")
    flattened = array.reshape(-1)
    raw = [item for row in value for item in row] if ndim == 2 else list(value)
    if any(number.hex() != item for number, item in zip(flattened, raw, strict=True)):
        raise ValueError(f"{name} contains a noncanonical hexadecimal value")
    return array


def _number_records(values: Mapping[str, float]) -> dict[str, dict[str, str]]:
    return {name: binary64_record(value) for name, value in values.items()}


def model_payload() -> dict[str, object]:
    """Return the canonical complete equation-parameter payload."""

    return {
        "equation": MODEL_EQUATION,
        "parameters": _number_records(MODEL_VALUES),
        "delay_convention": (
            "theta_j are scaled delays and tau_j=theta_j/sqrt(epsilon); "
            "the collocation equation uses the stored physical tau_j/T"
        ),
    }


def parameters_from_model_payload(model: Mapping[str, Any]) -> FHNPeriodicParameters:
    """Reconstruct the validator's parameter object from a strict model payload."""

    if set(model) != {"equation", "parameters", "delay_convention"}:
        raise ValueError("model payload has missing or unknown fields")
    if model.get("equation") != MODEL_EQUATION:
        raise ValueError("model equation changed")
    if model.get("delay_convention") != model_payload()["delay_convention"]:
        raise ValueError("model delay convention changed")
    records = model.get("parameters")
    if not isinstance(records, Mapping) or set(records) != set(MODEL_VALUES):
        raise ValueError("model parameter list changed")
    parsed = {
        name: _binary64_from_record(records[name], f"model.parameters.{name}")
        for name in MODEL_VALUES
    }
    for name, expected in MODEL_VALUES.items():
        if parsed[name].hex() != float(expected).hex():
            raise ValueError(f"model parameter {name} changed")
    return FHNPeriodicParameters(
        epsilon=parsed["epsilon"],
        unfolding=parsed["unfolding_a"],
        theta_0=parsed["theta_0"],
        theta_1=parsed["theta_1"],
        kappa_1=parsed["kappa_1"],
        kappa_3=parsed["kappa_3"],
    )


def _collocation_system(
    state: np.ndarray,
    period: float,
    parameters: FHNPeriodicParameters,
    phase_reference: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """Recompute the final leaky RFDE bordered collocation system."""

    count = len(state)
    derivative, _ = odd_fourier_matrices(count)
    voltage = state[:, 0]
    recovery = state[:, 1]
    reference_tangent = np.column_stack(
        (
            derivative @ phase_reference[:, 0],
            derivative @ phase_reference[:, 1],
        )
    )
    tau_0, tau_1 = parameters.physical_delays
    _, shift_0 = odd_fourier_matrices(count, tau_0 / period)
    _, shift_1 = odd_fourier_matrices(count, tau_1 / period)
    delayed_0 = shift_0 @ voltage
    delayed_1 = shift_1 @ voltage
    linear_difference = (delayed_0 + delayed_1) / 2.0 - voltage
    cubic_difference = (
        ((delayed_0 - 1.0) ** 3 + (delayed_1 - 1.0) ** 3) / 2.0
        - (voltage - 1.0) ** 3
    )
    fast = (
        voltage
        - voltage**3 / 3.0
        - recovery
        + parameters.epsilon * parameters.kappa_1 * linear_difference
        + parameters.epsilon * parameters.kappa_3 * cubic_difference
    )
    slow = parameters.epsilon * (
        voltage - parameters.unfolding - recovery
    )
    phase = float(
        np.vdot(reference_tangent, state - phase_reference).real / count
    )
    residual = np.concatenate(
        (
            derivative @ voltage - period * fast,
            derivative @ recovery - period * slow,
            [phase],
        )
    )

    current = (
        1.0
        - voltage**2
        - parameters.epsilon * parameters.kappa_1
        - 3.0
        * parameters.epsilon
        * parameters.kappa_3
        * (voltage - 1.0) ** 2
    )
    coefficient_0 = parameters.epsilon / 2.0 * (
        parameters.kappa_1
        + 3.0 * parameters.kappa_3 * (delayed_0 - 1.0) ** 2
    )
    coefficient_1 = parameters.epsilon / 2.0 * (
        parameters.kappa_1
        + 3.0 * parameters.kappa_3 * (delayed_1 - 1.0) ** 2
    )
    identity = np.eye(count)
    jacobian = np.zeros((2 * count + 1, 2 * count + 1))
    jacobian[:count, :count] = derivative - period * (
        np.diag(current)
        + np.diag(coefficient_0) @ shift_0
        + np.diag(coefficient_1) @ shift_1
    )
    jacobian[:count, count : 2 * count] = period * identity
    jacobian[count : 2 * count, :count] = (
        -period * parameters.epsilon * identity
    )
    jacobian[count : 2 * count, count : 2 * count] = (
        derivative + period * parameters.epsilon * identity
    )
    delayed_tangent_0 = shift_0 @ (derivative @ voltage)
    delayed_tangent_1 = shift_1 @ (derivative @ voltage)
    jacobian[:count, -1] = (
        -fast
        - tau_0 / period * coefficient_0 * delayed_tangent_0
        - tau_1 / period * coefficient_1 * delayed_tangent_1
    )
    jacobian[count : 2 * count, -1] = -slow
    jacobian[-1, :count] = reference_tangent[:, 0] / count
    jacobian[-1, count : 2 * count] = reference_tangent[:, 1] / count
    return residual, jacobian


def _trigonometric_values(
    samples: np.ndarray,
    phases: np.ndarray,
    *,
    derivative_order: int = 0,
) -> np.ndarray:
    count = len(samples)
    coefficients = np.fft.fft(samples) / count
    modes = np.fft.fftfreq(count, d=1.0 / count)
    multiplier = (2.0j * np.pi * modes) ** derivative_order
    basis = np.exp(2.0j * np.pi * phases[:, None] * modes[None, :])
    return (basis @ (multiplier * coefficients)).real


def recompute_binary64_metrics(
    state: np.ndarray,
    period: float,
    parameters: FHNPeriodicParameters,
    phase_reference: np.ndarray,
    *,
    oversampling_factor: int = 8,
) -> dict[str, float]:
    """Recompute finite diagnostics without promoting them to enclosures."""

    residual, jacobian = _collocation_system(
        state, period, parameters, phase_reference
    )
    count = len(state)
    phases = np.arange(oversampling_factor * count, dtype=float) / (
        oversampling_factor * count
    )
    voltage = _trigonometric_values(state[:, 0], phases)
    recovery = _trigonometric_values(state[:, 1], phases)
    voltage_derivative = _trigonometric_values(
        state[:, 0], phases, derivative_order=1
    )
    recovery_derivative = _trigonometric_values(
        state[:, 1], phases, derivative_order=1
    )
    tau_0, tau_1 = parameters.physical_delays
    delayed_0 = _trigonometric_values(
        state[:, 0], (phases - tau_0 / period) % 1.0
    )
    delayed_1 = _trigonometric_values(
        state[:, 0], (phases - tau_1 / period) % 1.0
    )
    fast = (
        voltage
        - voltage**3 / 3.0
        - recovery
        + parameters.epsilon
        * parameters.kappa_1
        * ((delayed_0 + delayed_1) / 2.0 - voltage)
        + parameters.epsilon
        * parameters.kappa_3
        * (
            ((delayed_0 - 1.0) ** 3 + (delayed_1 - 1.0) ** 3) / 2.0
            - (voltage - 1.0) ** 3
        )
    )
    slow = parameters.epsilon * (
        voltage - parameters.unfolding - recovery
    )
    coefficients = np.fft.fft(state, axis=0) / count
    modes = np.fft.fftfreq(count, d=1.0 / count)
    tail_cutoff = max(1, int(np.floor(0.8 * np.max(np.abs(modes)))))
    return {
        "collocation_residual_inf": float(np.max(np.abs(residual))),
        "oversampled_residual_inf": max(
            float(np.max(np.abs(voltage_derivative - period * fast))),
            float(np.max(np.abs(recovery_derivative - period * slow))),
        ),
        "bordered_smallest_singular_value": float(
            np.linalg.svd(jacobian, compute_uv=False)[-1]
        ),
        "spectral_tail_l1": float(
            np.sum(np.abs(coefficients[np.abs(modes) >= tail_cutoff]))
        ),
    }


def orbit_from_artifact(artifact: Mapping[str, Any]) -> PeriodicOrbitCandidate:
    """Reconstruct the exact supplied binary64 polynomial."""

    branch = artifact.get("branch")
    if branch not in RESULT_RELATIVE_PATHS:
        raise ValueError("artifact branch is not registered")
    model = artifact.get("model")
    collocation = artifact.get("collocation")
    if not isinstance(model, Mapping) or not isinstance(collocation, Mapping):
        raise ValueError("artifact model and collocation must be mappings")
    parameters = parameters_from_model_payload(model)
    count = collocation.get("node_count")
    if type(count) is not int or count < 5 or count % 2 != 1:
        raise ValueError("artifact node count must be an odd integer")
    phases = _binary64_array(
        collocation.get("phase_nodes_binary64"),
        "collocation.phase_nodes_binary64",
        1,
    )
    state = _binary64_array(
        collocation.get("state_binary64"),
        "collocation.state_binary64",
        2,
    )
    if phases.shape != (count,) or state.shape != (count, 2):
        raise ValueError("artifact grid or state has the wrong shape")
    expected_phases = np.arange(count, dtype=float) / count
    if not np.array_equal(phases, expected_phases):
        raise ValueError("artifact phase grid changed")
    period = _binary64_from_record(
        collocation.get("period"), "collocation.period"
    )
    if period <= 0.0:
        raise ValueError("artifact period must be positive")
    diagnostics = collocation.get("diagnostics")
    if not isinstance(diagnostics, Mapping):
        raise ValueError("artifact diagnostics must be a mapping")
    values = {
        name: _binary64_from_record(
            diagnostics.get(name), f"collocation.diagnostics.{name}"
        )
        for name in (
            "collocation_residual_inf",
            "oversampled_residual_inf",
            "bordered_smallest_singular_value",
            "spectral_tail_l1",
            "final_newton_step_inf",
        )
    }
    iterations = collocation.get("newton_iterations")
    if type(iterations) is not int or iterations <= 0:
        raise ValueError("artifact Newton iteration count changed")
    return PeriodicOrbitCandidate(
        parameters=parameters,
        phase_nodes=phases,
        state=state,
        period=period,
        collocation_residual_inf=values["collocation_residual_inf"],
        oversampled_residual_inf=values["oversampled_residual_inf"],
        newton_iterations=iterations,
        final_step_inf=values["final_newton_step_inf"],
        spectral_tail_l1=values["spectral_tail_l1"],
    )


def _finite_decimal_string(value: object, name: str) -> None:
    if not isinstance(value, str):
        raise ValueError(f"{name} must be a decimal string")
    try:
        number = Decimal(value)
    except InvalidOperation as error:
        raise ValueError(f"{name} is not decimal") from error
    if not number.is_finite():
        raise ValueError(f"{name} must be finite")


def _validate_directed_payload(
    payload: object,
    branch: str,
    settings: Mapping[str, Any],
) -> None:
    if not isinstance(payload, Mapping):
        raise ValueError("directed prototype must be a mapping")
    expected_outer = {field.name for field in fields(DirectedLeakyPeriodicValidation)}
    if set(payload) != expected_outer:
        raise ValueError("directed prototype has missing or unknown fields")
    if payload.get("branch") != branch or payload.get("recovery_leak") != "1":
        raise ValueError("directed prototype branch or recovery leak changed")
    if payload.get("formula_adaptation_independently_audited") is not True:
        raise ValueError("directed formula audit is not registered")
    for name in (
        "periodic_rfde_orbit_validated",
        "phase_bordered_rfde_inverse_validated",
    ):
        if type(payload.get(name)) is not bool:
            raise ValueError(f"directed proof flag {name} has wrong type")
    if type(payload.get("directed_radii_inequality_candidate_closed")) is not bool:
        raise ValueError("directed candidate closure flag has wrong type")

    finite = payload.get("finite")
    blocks = payload.get("blocks")
    correction = payload.get("correction")
    floquet = payload.get("floquet")
    expected_nested = (
        (finite, DealiasedFiniteCoefficientCertificate, "finite"),
        (blocks, DirectedFiniteTailBlocks, "blocks"),
        (correction, DirectedCorrectionRadiiBound, "correction"),
        (floquet, LeakyFloquetValidationContract, "floquet"),
    )
    for value, data_class, name in expected_nested:
        if not isinstance(value, Mapping) or set(value) != {
            field.name for field in fields(data_class)
        }:
            raise ValueError(f"directed {name} record has changed schema")

    if finite.get("cutoff") != settings.get("cutoff"):
        raise ValueError("directed cutoff changed")
    if finite.get("precision_bits") != settings.get("precision_bits"):
        raise ValueError("directed precision changed")
    if correction.get("maximum_radius") != settings.get("maximum_radius"):
        raise ValueError("directed maximum radius changed")
    if correction.get("chosen_radius") != settings.get("chosen_radius"):
        raise ValueError("directed chosen radius changed")
    for mapping_name, mapping in (
        ("finite", finite),
        ("blocks", blocks),
        ("correction", correction),
    ):
        for key, value in mapping.items():
            if value is None or type(value) in (bool, int):
                continue
            if isinstance(value, str) and key in {
                "norm",
                "independent_coordinate_weights",
                "maximum_radius",
                "chosen_radius",
            }:
                continue
            _finite_decimal_string(value, f"directed.{mapping_name}.{key}")

    expected_floquet = {
        "translation_identity_exact_for_validated_orbit": payload.get(
            "periodic_rfde_orbit_validated"
        ),
        "phase_bordered_rfde_inverse_validated": payload.get(
            "phase_bordered_rfde_inverse_validated"
        ),
        "geometric_translation_kernel_conditional_on_standard_bvp_identification": (
            payload.get("periodic_rfde_orbit_validated")
            and payload.get("phase_bordered_rfde_inverse_validated")
        ),
    }
    for name, value in floquet.items():
        if name == "required_next_certificates":
            if not isinstance(value, list) or len(value) != 3:
                raise ValueError("Floquet next-certificate list changed")
        elif name in expected_floquet:
            if value is not expected_floquet[name]:
                raise ValueError(f"Floquet contract flag {name} changed")
        elif value is not False:
            raise ValueError(f"Floquet spectral proof flag {name} was promoted")


def _metric_close(recomputed: float, stored: float, name: str) -> None:
    scale = max(1.0, abs(recomputed), abs(stored))
    tolerance = 4096.0 * np.finfo(float).eps * scale
    if abs(recomputed - stored) > tolerance:
        raise ValueError(f"stored {name} does not replay in binary64")


def _decimal_value(value: object, name: str) -> Decimal:
    _finite_decimal_string(value, name)
    return Decimal(value)  # type: ignore[arg-type]


def _directed_decimal_close(
    stored: object,
    replayed: object,
    name: str,
    defect_buffer: Decimal,
) -> None:
    stored_decimal = _decimal_value(stored, f"stored {name}")
    replayed_decimal = _decimal_value(replayed, f"replayed {name}")
    with localcontext() as context:
        context.prec = 200
        scale = max(abs(stored_decimal), abs(replayed_decimal))
        tolerance = max(
            DIRECTED_REPLAY_ABSOLUTE_TOLERANCE,
            DIRECTED_REPLAY_RELATIVE_TOLERANCE * scale,
            defect_buffer,
        )
        if abs(stored_decimal - replayed_decimal) > tolerance:
            raise ValueError(
                f"directed-radii numeric field {name} left the replay tolerance"
            )


def _validate_directed_gate_semantics(
    payload: Mapping[str, Any],
    name: str,
) -> None:
    """Require the serialized booleans to agree with their strict signs."""

    finite = payload["finite"]
    blocks = payload["blocks"]
    correction = payload["correction"]
    if not all(isinstance(value, Mapping) for value in (finite, blocks, correction)):
        raise ValueError(f"{name} directed gate records must be mappings")
    finite_defect = _decimal_value(
        finite["finite_inverse_defect_upper"],
        f"{name}.finite.finite_inverse_defect_upper",
    )
    full_defect = _decimal_value(
        blocks["full_point_defect_upper"],
        f"{name}.blocks.full_point_defect_upper",
    )
    contraction = _decimal_value(
        correction["contraction_upper"],
        f"{name}.correction.contraction_upper",
    )
    margin = _decimal_value(
        correction["radii_margin_lower"],
        f"{name}.correction.radii_margin_lower",
    )
    finite_gate = finite_defect < 1
    point_gate = full_defect < 1
    radii_gate = contraction < 1 and margin > 0
    if finite.get("finite_inverse_validated") is not finite_gate:
        raise ValueError(f"{name} finite-inverse gate disagrees with its bound")
    if blocks.get("full_point_inverse_gate") is not point_gate:
        raise ValueError(f"{name} full-point gate disagrees with its bound")
    if correction.get("radii_polynomial_negative") is not radii_gate:
        raise ValueError(f"{name} radii gate disagrees with its strict signs")
    if payload.get("directed_radii_inequality_candidate_closed") is not radii_gate:
        raise ValueError(f"{name} candidate-closure gate disagrees with its signs")
    formula_gate = payload.get("formula_adaptation_independently_audited") is True
    proof_gate = radii_gate and formula_gate
    if payload.get("periodic_rfde_orbit_validated") is not proof_gate:
        raise ValueError(f"{name} orbit proof gate disagrees with its premises")
    if payload.get("phase_bordered_rfde_inverse_validated") is not proof_gate:
        raise ValueError(f"{name} bordered-inverse gate disagrees with its premises")
    inverse_bound = correction.get("bordered_inverse_norm_upper")
    if (inverse_bound is not None) is not radii_gate:
        raise ValueError(f"{name} bordered-inverse bound has inconsistent presence")


def _compare_directed_replay(
    stored: Mapping[str, Any],
    replayed: Mapping[str, Any],
) -> None:
    """Compare one replay without assuming a bitwise-stable BLAS inverse."""

    if set(stored) != set(replayed):
        raise ValueError("directed-radii replay changed its outer schema")
    stored_finite = stored.get("finite")
    replayed_finite = replayed.get("finite")
    if not isinstance(stored_finite, Mapping) or not isinstance(
        replayed_finite, Mapping
    ):
        raise ValueError("directed-radii replay finite records must be mappings")
    stored_defect = _decimal_value(
        stored_finite.get("finite_inverse_defect_upper"),
        "stored finite inverse defect",
    )
    replayed_defect = _decimal_value(
        replayed_finite.get("finite_inverse_defect_upper"),
        "replayed finite inverse defect",
    )
    if stored_defect < 0 or replayed_defect < 0:
        raise ValueError("directed-radii inverse defects must be nonnegative")
    # Each run supplies an independent directed upper bound for its own
    # binary64 midpoint inverse.  Their sum is a conservative triangle
    # buffer for replay comparisons near the cancelling quantity I-AJ.  It
    # is computed from proof data, not calibrated to an observed mismatch.
    with localcontext() as context:
        context.prec = 200
        defect_buffer = stored_defect + replayed_defect
    numeric_records = {"finite", "blocks", "correction"}
    for key in stored:
        if key in numeric_records:
            continue
        if stored[key] != replayed[key]:
            raise ValueError(f"directed-radii replay changed {key}")
    exact_nested_strings = {
        "norm",
        "independent_coordinate_weights",
        "maximum_radius",
        "chosen_radius",
    }
    for record_name in numeric_records:
        stored_record = stored[record_name]
        replayed_record = replayed[record_name]
        if not isinstance(stored_record, Mapping) or not isinstance(
            replayed_record, Mapping
        ):
            raise ValueError("directed-radii replay records must be mappings")
        if set(stored_record) != set(replayed_record):
            raise ValueError(
                f"directed-radii replay changed the {record_name} schema"
            )
        for key in stored_record:
            stored_value = stored_record[key]
            replayed_value = replayed_record[key]
            if (
                isinstance(stored_value, str)
                and isinstance(replayed_value, str)
                and key not in exact_nested_strings
            ):
                _directed_decimal_close(
                    stored_value,
                    replayed_value,
                    f"{record_name}.{key}",
                    defect_buffer,
                )
            elif stored_value != replayed_value:
                raise ValueError(
                    f"directed-radii replay changed {record_name}.{key}"
                )
    _validate_directed_gate_semantics(stored, "stored")
    _validate_directed_gate_semantics(replayed, "replayed")
    if stored["directed_radii_inequality_candidate_closed"]:
        stored_blocks = stored["blocks"]
        replayed_blocks = replayed["blocks"]
        stored_correction = stored["correction"]
        replayed_correction = replayed["correction"]
        assert isinstance(stored_blocks, Mapping)
        assert isinstance(replayed_blocks, Mapping)
        assert isinstance(stored_correction, Mapping)
        assert isinstance(replayed_correction, Mapping)
        with localcontext() as context:
            context.prec = 200
            gate_slacks = (
                1 - stored_defect,
                1 - replayed_defect,
                1
                - _decimal_value(
                    stored_blocks["full_point_defect_upper"],
                    "stored full-point defect",
                ),
                1
                - _decimal_value(
                    replayed_blocks["full_point_defect_upper"],
                    "replayed full-point defect",
                ),
                1
                - _decimal_value(
                    stored_correction["contraction_upper"],
                    "stored contraction",
                ),
                1
                - _decimal_value(
                    replayed_correction["contraction_upper"],
                    "replayed contraction",
                ),
                _decimal_value(
                    stored_correction["radii_margin_lower"],
                    "stored radii margin",
                ),
                _decimal_value(
                    replayed_correction["radii_margin_lower"],
                    "replayed radii margin",
                ),
            )
            if min(gate_slacks) <= defect_buffer:
                raise ValueError(
                    "directed-radii replay buffer exhausts a strict gate margin"
                )


def _validate_manifest(
    manifest: object,
    artifact: Mapping[str, Any],
    repository: Path,
) -> None:
    if not isinstance(manifest, Mapping):
        raise ValueError("artifact manifest must be a mapping")
    expected_keys = {
        "schema_id",
        "result",
        "default_command",
        "arithmetic_scope",
        "artifact_sha256",
        "source_sha256",
        "python",
        "platform",
        "numpy",
        "scipy",
        "gmpy2",
    }
    if set(manifest) != expected_keys:
        raise ValueError("artifact manifest has missing or unknown fields")
    branch = artifact["branch"]
    expected_scalars = {
        "schema_id": SCHEMA_ID,
        "result": RESULT_RELATIVE_PATHS[branch],
        "default_command": DEFAULT_COMMANDS[branch],
        "arithmetic_scope": ARITHMETIC_SCOPE,
        "artifact_sha256": canonical_sha256(artifact),
        "python": platform.python_version(),
        "platform": platform.platform(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "gmpy2": gmpy2.__version__,
    }
    for name, expected in expected_scalars.items():
        if manifest.get(name) != expected:
            raise ValueError(f"artifact manifest {name} changed")
    source_hashes = manifest.get("source_sha256")
    if not isinstance(source_hashes, Mapping) or set(source_hashes) != set(
        SOURCE_MANIFEST
    ):
        raise ValueError("artifact source manifest changed")
    for relative in SOURCE_MANIFEST:
        if source_hashes.get(relative) != _sha256_path(repository / relative):
            raise ValueError(f"artifact source hash changed for {relative}")

def validate_leaky_periodic_branch_artifact(
    payload: Mapping[str, Any],
    repository: Path,
    *,
    replay_directed: bool = False,
) -> PeriodicOrbitCandidate:
    """Strictly validate one tracked branch artifact.

    ``replay_directed=True`` repeats the expensive finite/tail calculation.
    The default path still verifies the source hashes, the source-registered
    body digest, the complete proof ledger, the exact binary64 data, and the
    independently recomputed finite collocation diagnostics.
    """

    if not isinstance(payload, Mapping) or set(payload) != {"artifact", "manifest"}:
        raise ValueError("branch result must contain exactly artifact and manifest")
    artifact = payload.get("artifact")
    if not isinstance(artifact, Mapping):
        raise ValueError("branch artifact must be a mapping")
    expected_artifact_keys = {
        "schema_id",
        "branch",
        "model",
        "representation",
        "collocation",
        "directed_radii_prototype",
        "claim_status",
    }
    if set(artifact) != expected_artifact_keys:
        raise ValueError("branch artifact has missing or unknown fields")
    if artifact.get("schema_id") != SCHEMA_ID:
        raise ValueError("branch artifact schema changed")
    branch = artifact.get("branch")
    if branch not in RESULT_RELATIVE_PATHS:
        raise ValueError("branch artifact branch is not registered")
    if artifact.get("representation") != REPRESENTATION:
        raise ValueError("branch artifact representation changed")
    if artifact.get("claim_status") != CLAIM_STATUS:
        raise ValueError("branch artifact proof ledger changed")

    expected_digest = EXPECTED_ARTIFACT_SHA256[branch]
    if not isinstance(expected_digest, str) or len(expected_digest) != 64:
        raise ValueError("branch has no source-registered artifact body")
    if canonical_sha256(artifact) != expected_digest:
        raise ValueError("branch artifact differs from the source-locked body")
    _validate_manifest(payload.get("manifest"), artifact, repository)

    collocation = artifact.get("collocation")
    if not isinstance(collocation, Mapping):
        raise ValueError("collocation payload must be a mapping")
    expected_collocation_keys = {
        "node_count",
        "continuation_steps",
        "continuation_gain_fractions_binary64",
        "newton_max_iterations_per_step",
        "newton_step_tolerance",
        "newton_iterations",
        "oversampling_factor",
        "phase_border",
        "phase_nodes_binary64",
        "phase_reference_binary64",
        "state_binary64",
        "period",
        "diagnostics",
    }
    if set(collocation) != expected_collocation_keys:
        raise ValueError("collocation payload has missing or unknown fields")
    if collocation.get("continuation_steps") != 10:
        raise ValueError("continuation step count changed")
    if collocation.get("newton_max_iterations_per_step") != 14:
        raise ValueError("Newton iteration cap changed")
    if collocation.get("oversampling_factor") != 8:
        raise ValueError("oversampling factor changed")
    if collocation.get("phase_border") != PHASE_BORDER:
        raise ValueError("phase border changed")
    if collocation.get("newton_step_tolerance") != binary64_record(2.0e-13):
        raise ValueError("Newton step tolerance changed")
    fractions = _binary64_array(
        collocation.get("continuation_gain_fractions_binary64"),
        "collocation.continuation_gain_fractions_binary64",
        1,
    )
    expected_fractions = np.linspace(0.0, 1.0, 11)
    if not np.array_equal(fractions, expected_fractions):
        raise ValueError("continuation gain fractions changed")

    orbit = orbit_from_artifact(artifact)
    phase_reference = _binary64_array(
        collocation.get("phase_reference_binary64"),
        "collocation.phase_reference_binary64",
        2,
    )
    if phase_reference.shape != orbit.state.shape:
        raise ValueError("phase reference has the wrong shape")
    diagnostics = collocation["diagnostics"]
    if not isinstance(diagnostics, Mapping) or set(diagnostics) != {
        "collocation_residual_inf",
        "oversampled_residual_inf",
        "bordered_smallest_singular_value",
        "spectral_tail_l1",
        "final_newton_step_inf",
    }:
        raise ValueError("collocation diagnostics schema changed")
    recomputed = recompute_binary64_metrics(
        orbit.state,
        orbit.period,
        orbit.parameters,
        phase_reference,
        oversampling_factor=8,
    )
    for name, value in recomputed.items():
        stored = _binary64_from_record(
            diagnostics[name], f"collocation.diagnostics.{name}"
        )
        _metric_close(value, stored, name)
    if orbit.collocation_residual_inf >= 1.0e-9:
        raise ValueError("branch collocation residual is too large for replay")
    if branch == "inner_saddle_candidate" and orbit.oversampled_residual_inf >= 1.0e-9:
        raise ValueError("inner branch oversampled residual changed scale")

    prototype = artifact.get("directed_radii_prototype")
    if not isinstance(prototype, Mapping) or set(prototype) != {
        "settings",
        "validation",
    }:
        raise ValueError("directed prototype wrapper changed")
    settings = prototype.get("settings")
    if not isinstance(settings, Mapping) or set(settings) != {
        "cutoff",
        "precision_bits",
        "maximum_radius",
        "chosen_radius",
    }:
        raise ValueError("directed prototype settings changed")
    expected_cutoff = 3 * ((len(orbit.state) - 1) // 2)
    if settings.get("cutoff") != expected_cutoff:
        raise ValueError("directed cutoff does not contain exact cubic support")
    if settings.get("precision_bits") != 160:
        raise ValueError("directed precision changed")
    if settings.get("maximum_radius") != "1e-5" or settings.get(
        "chosen_radius"
    ) != "1e-5":
        raise ValueError("directed radius settings changed")
    _validate_directed_payload(prototype.get("validation"), branch, settings)
    _validate_directed_gate_semantics(
        prototype["validation"], "stored"
    )

    if replay_directed:
        replay = evaluate_leaky_periodic_radii_candidate(
            orbit,
            branch=branch,
            cutoff=settings["cutoff"],
            precision=settings["precision_bits"],
            maximum_radius=settings["maximum_radius"],
            chosen_radius=settings["chosen_radius"],
        )
        replay_payload = json.loads(json.dumps(asdict(replay)))
        _compare_directed_replay(
            prototype["validation"], replay_payload
        )
    return orbit


__all__ = [
    "ARITHMETIC_SCOPE",
    "CLAIM_STATUS",
    "DIRECTED_REPLAY_ABSOLUTE_TOLERANCE",
    "DIRECTED_REPLAY_RELATIVE_TOLERANCE",
    "DEFAULT_COMMANDS",
    "EXPECTED_ARTIFACT_SHA256",
    "GENERATOR_RELATIVE_PATH",
    "MODEL_EQUATION",
    "MODEL_VALUES",
    "PHASE_BORDER",
    "REPRESENTATION",
    "RESULT_RELATIVE_PATHS",
    "SCHEMA_ID",
    "SOURCE_MANIFEST",
    "SOURCE_RELATIVE_PATH",
    "binary64_record",
    "canonical_sha256",
    "model_payload",
    "orbit_from_artifact",
    "recompute_binary64_metrics",
    "validate_leaky_periodic_branch_artifact",
]
