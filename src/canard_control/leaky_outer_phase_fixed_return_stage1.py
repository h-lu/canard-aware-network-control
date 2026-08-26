"""Stage-1 contract for a direct phase-fixed outer return contraction.

The finite matrices in this module are diagnostics only.  The theorem route
uses the exact matrix-measure kernel of the linear two-delay RFDE on the
continuous reduced-history space.  In particular, it never assigns an
interpolation error to an arbitrary continuous input history.

For each returned output row, the fixed-time solution operator is represented
by a current-value atom, an absolutely continuous signed density on the input
history, and one scalar coefficient multiplying the initial recovery value.
The return-time correction is applied to those signed measures before total
variation is bounded.  Once the two corrected row norms and a nonlinear
derivative Lipschitz constant are directed, the only numerical gate is

    max(Q_v, Q_w) + C_DP * 1e-4 < 1.

No directed kernel enclosure is supplied yet, so all contraction, attraction,
outer-capture, and pulse-onset claims remain false.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from decimal import Decimal, InvalidOperation, ROUND_CEILING, localcontext
from hashlib import sha256
import json
import math
import os
from pathlib import Path
import platform
from typing import Any, Mapping

import numpy as np
import scipy

from canard_control.leaky_floquet_outer_grushin_stage1 import (
    RESULT_RELATIVE_PATH as GRUSHIN_RESULT_RELATIVE_PATH,
)
from canard_control.leaky_outer_high_resolution import (
    RESULT_RELATIVE_PATH as OUTER_RESULT_RELATIVE_PATH,
    validate_outer_high_resolution_artifact,
)
from canard_control.leaky_pulse_separator_candidate import (
    _periodic_interpolator,
    finite_section,
)


SCHEMA_ID = "leaky-outer-phase-fixed-return-stage1-v1"
MODEL_ID = "autonomous-leaky-recovery-two-delay-fhn-bistable-proposal"
BRANCH = "outer_pulse"
SOURCE_RELATIVE_PATH = (
    "src/canard_control/leaky_outer_phase_fixed_return_stage1.py"
)
GENERATOR_RELATIVE_PATH = (
    "experiments/leaky_outer_phase_fixed_return_stage1.py"
)
RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_outer_phase_fixed_return_stage1.json"
)
NOTE_RELATIVE_PATH = "docs/leaky-outer-phase-fixed-return-stage1.md"
TEST_RELATIVE_PATH = "tests/test_leaky_outer_phase_fixed_return_stage1.py"
SOURCE_MANIFEST = (
    SOURCE_RELATIVE_PATH,
    GENERATOR_RELATIVE_PATH,
    NOTE_RELATIVE_PATH,
    "src/canard_control/leaky_outer_high_resolution.py",
    "src/canard_control/leaky_pulse_separator_candidate.py",
)
DEFAULT_COMMAND = (
    "OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONPATH=build/testdeps:src "
    "/usr/bin/python3 experiments/leaky_outer_phase_fixed_return_stage1.py"
)
ARITHMETIC_SCOPE = (
    "source-bound binary64 RK4/cubic-interpolation finite-section pilot; "
    "exact algebraic phase projection using the stored Fourier-orbit tangent; "
    "and an executable Decimal evaluator for future directed matrix-measure "
    "kernel and nonlinear return bounds.  No finite-to-C0 promotion occurs"
)

OUTER_RESULT_SHA256 = (
    "d888916fed919f1515dd31ab851b2229816ea373365fa0221b1e345580f165a7"
)
GRUSHIN_RESULT_SHA256 = (
    "5ca82a8c3e25ef0749e29142e9e19f49f21d219794b881ad3c9fb9011de0e524"
)
FINITE_SECTION_STEPS = (120, 180, 240, 360)
CHOSEN_SECTION_RADIUS = "0.0001"
NESTED_EXACT_ORBIT_RADIUS = "1e-8"

TRUE_FLAGS = (
    "outer_exact_periodic_orbit_parent_validated",
    "outer_exact_translation_identity_parent_validated",
    "physical_current_voltage_phase_row_normalized",
    "matrix_measure_kernel_recurrence_registered",
    "rank_one_return_time_measure_correction_registered",
    "continuous_history_induced_norm_total_variation_identity_registered",
    "four_level_binary64_phase_fixed_pilot_computed",
)
FALSE_FLAGS = (
    "binary64_finite_section_promoted_to_continuous_history_proof",
    "directed_matrix_measure_kernel_enclosed",
    "arbitrary_continuous_history_operator_norm_validated",
    "unique_first_return_on_radius_1e_minus_4_tube_validated",
    "phase_fixed_outer_return_derivative_contraction_validated",
    "second_variational_kernel_bound_validated",
    "nonlinear_phase_fixed_return_contraction_validated",
    "outer_quantitative_attracting_tube_validated",
    "ambient_pulse_distance_promoted_directly_to_section_distance",
    "pulse_to_outer_section_entry_validated",
    "outer_pulse_capture_validated",
    "physical_pulse_onset_validated",
)


def _sha256_path(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def canonical_sha256(value: Any) -> str:
    encoded = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("ascii")
    return sha256(encoded).hexdigest()


def _binary64_record(value: float) -> dict[str, str]:
    number = float(value)
    if not math.isfinite(number):
        raise ValueError("diagnostic values must be finite")
    return {"binary64_hex": number.hex(), "decimal": format(number, ".17g")}


def _binary64_value(value: Any, name: str) -> float:
    if not isinstance(value, Mapping) or set(value) != {
        "binary64_hex",
        "decimal",
    }:
        raise ValueError(f"{name} is not a canonical binary64 record")
    hexadecimal = value.get("binary64_hex")
    decimal = value.get("decimal")
    if not isinstance(hexadecimal, str) or not isinstance(decimal, str):
        raise ValueError(f"{name} binary64 fields must be strings")
    try:
        number = float.fromhex(hexadecimal)
    except ValueError as error:
        raise ValueError(f"{name} has invalid hexadecimal data") from error
    if (
        not math.isfinite(number)
        or number.hex() != hexadecimal
        or format(number, ".17g") != decimal
    ):
        raise ValueError(f"{name} binary64 record changed")
    return number


def _decimal(value: str | None, name: str) -> Decimal | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError(f"{name} must be a decimal string or null")
    try:
        number = Decimal(value)
    except InvalidOperation as error:
        raise ValueError(f"{name} is not a decimal") from error
    if not number.is_finite() or number < 0:
        raise ValueError(f"{name} must be finite and nonnegative")
    return number


def _upper(value: Decimal) -> str:
    with localcontext() as context:
        context.prec = 96
        context.rounding = ROUND_CEILING
        return format(+value, "f")


@dataclass(frozen=True)
class FinitePhaseFixedPilot:
    step_count: int
    matrix_dimension: int
    history_step_count: int
    physical_step_binary64: dict[str, str]
    stored_orbit_current_voltage_speed_binary64: dict[str, str]
    stored_translation_monodromy_residual_inf_binary64: dict[str, str]
    algebraic_phase_projection_tangent_residual_inf_binary64: dict[str, str]
    fixed_time_section_input_inf_norm_binary64: dict[str, str]
    rank_one_phase_correction_inf_norm_binary64: dict[str, str]
    phase_fixed_spectral_radius_binary64: dict[str, str]
    phase_fixed_one_return_inf_norm_binary64: dict[str, str]
    phase_fixed_two_return_inf_norm_binary64: dict[str, str]


@dataclass(frozen=True)
class DirectedReturnInputBudget:
    phase_fixed_voltage_history_row_norm_upper: str | None
    phase_fixed_recovery_row_norm_upper: str | None
    return_derivative_lipschitz_upper: str | None
    chosen_section_radius: str
    validated_section_tube_radius_lower: str | None
    directed_kernel_recurrence_validated: bool
    arbitrary_c0_input_covered_by_measure_representation: bool
    corrected_signed_measure_total_variation_validated: bool
    unique_first_positive_return_and_event_speed_validated: bool
    second_variational_return_kernel_validated: bool
    evidence_status: str


@dataclass(frozen=True)
class DirectedReturnEvaluation:
    input_complete: bool
    missing_numeric_inputs: tuple[str, ...]
    missing_proof_inputs: tuple[str, ...]
    linear_phase_fixed_return_norm_upper: str | None
    nonlinear_derivative_increment_upper: str | None
    phase_fixed_return_lipschitz_upper: str | None
    section_tube_contains_chosen_ball: bool
    single_strict_inequality_holds: bool
    direct_outer_return_contraction_closes: bool
    single_strict_inequality: str


@dataclass(frozen=True)
class AmbientToSectionInputBudget:
    ambient_complete_history_distance_upper: str | None
    phase_chart_lipschitz_upper: str | None
    validated_section_radius: str
    ambient_distance_to_exact_phase_zero_orbit_validated: bool
    nonlinear_phase_chart_validated_on_ambient_tube: bool
    evidence_status: str


@dataclass(frozen=True)
class AmbientToSectionEvaluation:
    input_complete: bool
    missing_numeric_inputs: tuple[str, ...]
    missing_proof_inputs: tuple[str, ...]
    projected_section_distance_upper: str | None
    strict_section_entry_inequality_holds: bool
    pulse_to_section_entry_closes: bool
    strict_section_entry_inequality: str


@dataclass(frozen=True)
class OuterPhaseFixedReturnStage1:
    schema_id: str
    model_id: str
    branch: str
    arithmetic_scope: str
    parent_result_sha256: dict[str, str]
    nested_exact_orbit_radius: str
    reduced_history_space: str
    phase_section: str
    finite_section_pilot: tuple[FinitePhaseFixedPilot, ...]
    finite_section_pilot_scope: str
    matrix_measure_kernel_contract: dict[str, Any]
    input_budget: DirectedReturnInputBudget
    evaluation: DirectedReturnEvaluation
    ambient_to_section_budget: AmbientToSectionInputBudget
    ambient_to_section_evaluation: AmbientToSectionEvaluation
    claim_status: dict[str, bool]
    conclusion: str


def evaluate_directed_return_budget(
    budget: DirectedReturnInputBudget,
) -> DirectedReturnEvaluation:
    numeric_names = (
        "phase_fixed_voltage_history_row_norm_upper",
        "phase_fixed_recovery_row_norm_upper",
        "return_derivative_lipschitz_upper",
        "validated_section_tube_radius_lower",
    )
    missing_numeric = tuple(
        name for name in numeric_names if getattr(budget, name) is None
    )
    proof_flags = (
        "directed_kernel_recurrence_validated",
        "arbitrary_c0_input_covered_by_measure_representation",
        "corrected_signed_measure_total_variation_validated",
        "unique_first_positive_return_and_event_speed_validated",
        "second_variational_return_kernel_validated",
    )
    missing_proof = tuple(name for name in proof_flags if not getattr(budget, name))
    voltage = _decimal(
        budget.phase_fixed_voltage_history_row_norm_upper,
        "phase_fixed_voltage_history_row_norm_upper",
    )
    recovery = _decimal(
        budget.phase_fixed_recovery_row_norm_upper,
        "phase_fixed_recovery_row_norm_upper",
    )
    derivative = _decimal(
        budget.return_derivative_lipschitz_upper,
        "return_derivative_lipschitz_upper",
    )
    radius = _decimal(budget.chosen_section_radius, "chosen_section_radius")
    domain = _decimal(
        budget.validated_section_tube_radius_lower,
        "validated_section_tube_radius_lower",
    )
    if radius is None or radius <= 0:
        raise ValueError("chosen_section_radius must be positive")

    linear_text: str | None = None
    increment_text: str | None = None
    lipschitz_text: str | None = None
    contains = False
    strict = False
    if not missing_numeric:
        assert voltage is not None
        assert recovery is not None
        assert derivative is not None
        assert domain is not None
        with localcontext() as context:
            context.prec = 96
            context.rounding = ROUND_CEILING
            linear = max(voltage, recovery)
            increment = derivative * radius
            lipschitz = linear + increment
        linear_text = _upper(linear)
        increment_text = _upper(increment)
        lipschitz_text = _upper(lipschitz)
        contains = domain >= radius
        strict = lipschitz < 1
    closes = not missing_numeric and not missing_proof and contains and strict
    return DirectedReturnEvaluation(
        input_complete=not missing_numeric and not missing_proof,
        missing_numeric_inputs=missing_numeric,
        missing_proof_inputs=missing_proof,
        linear_phase_fixed_return_norm_upper=linear_text,
        nonlinear_derivative_increment_upper=increment_text,
        phase_fixed_return_lipschitz_upper=lipschitz_text,
        section_tube_contains_chosen_ball=contains,
        single_strict_inequality_holds=strict,
        direct_outer_return_contraction_closes=closes,
        single_strict_inequality=(
            "max(Q_voltage_history,Q_recovery)+C_DP*0.0001 < 1"
        ),
    )


def evaluate_ambient_to_section_budget(
    budget: AmbientToSectionInputBudget,
) -> AmbientToSectionEvaluation:
    numeric_names = (
        "ambient_complete_history_distance_upper",
        "phase_chart_lipschitz_upper",
    )
    missing_numeric = tuple(
        name for name in numeric_names if getattr(budget, name) is None
    )
    proof_flags = (
        "ambient_distance_to_exact_phase_zero_orbit_validated",
        "nonlinear_phase_chart_validated_on_ambient_tube",
    )
    missing_proof = tuple(name for name in proof_flags if not getattr(budget, name))
    distance = _decimal(
        budget.ambient_complete_history_distance_upper,
        "ambient_complete_history_distance_upper",
    )
    chart = _decimal(
        budget.phase_chart_lipschitz_upper,
        "phase_chart_lipschitz_upper",
    )
    radius = _decimal(budget.validated_section_radius, "validated_section_radius")
    if radius is None or radius <= 0:
        raise ValueError("validated_section_radius must be positive")
    projected_text: str | None = None
    strict = False
    if not missing_numeric:
        assert distance is not None
        assert chart is not None
        with localcontext() as context:
            context.prec = 96
            context.rounding = ROUND_CEILING
            projected = chart * distance
        projected_text = _upper(projected)
        strict = projected < radius
    closes = not missing_numeric and not missing_proof and strict
    return AmbientToSectionEvaluation(
        input_complete=not missing_numeric and not missing_proof,
        missing_numeric_inputs=missing_numeric,
        missing_proof_inputs=missing_proof,
        projected_section_distance_upper=projected_text,
        strict_section_entry_inequality_holds=strict,
        pulse_to_section_entry_closes=closes,
        strict_section_entry_inequality="Q_phase*d_ambient < r_section",
    )


def _finite_pilot(orbit: Any, step_count: int) -> FinitePhaseFixedPilot:
    section = finite_section(orbit, step_count)
    voltage, voltage_derivative = _periodic_interpolator(
        orbit.state[:, 0], orbit.period
    )
    del voltage
    recovery, recovery_derivative = _periodic_interpolator(
        orbit.state[:, 1], orbit.period
    )
    del recovery
    history_steps = section.history_steps
    tangent = np.asarray(
        [
            voltage_derivative((index - history_steps) * section.step)
            for index in range(history_steps + 1)
        ]
        + [recovery_derivative(0.0)],
        dtype=float,
    )
    current_voltage_index = history_steps
    phase_speed = float(tangent[current_voltage_index])
    if not phase_speed > 0.0:
        raise ArithmeticError("the physical current-voltage section lost transversality")
    phase_row = np.zeros(len(tangent), dtype=float)
    phase_row[current_voltage_index] = 1.0 / phase_speed
    projection = np.eye(len(tangent)) - np.outer(tangent, phase_row)
    keep = np.arange(len(tangent)) != current_voltage_index
    fixed_time = section.matrix[:, keep]
    rank_one_correction = np.outer(tangent, phase_row @ section.matrix)[:, keep]
    phase_fixed = (projection @ section.matrix)[np.ix_(keep, keep)]
    phase_residual = float(np.linalg.norm(projection @ tangent, ord=np.inf))
    translation_residual = float(
        np.linalg.norm(section.matrix @ tangent - tangent, ord=np.inf)
    )
    return FinitePhaseFixedPilot(
        step_count=step_count,
        matrix_dimension=len(tangent),
        history_step_count=history_steps,
        physical_step_binary64=_binary64_record(section.step),
        stored_orbit_current_voltage_speed_binary64=_binary64_record(phase_speed),
        stored_translation_monodromy_residual_inf_binary64=_binary64_record(
            translation_residual
        ),
        algebraic_phase_projection_tangent_residual_inf_binary64=_binary64_record(
            phase_residual
        ),
        fixed_time_section_input_inf_norm_binary64=_binary64_record(
            float(np.linalg.norm(fixed_time, ord=np.inf))
        ),
        rank_one_phase_correction_inf_norm_binary64=_binary64_record(
            float(np.linalg.norm(rank_one_correction, ord=np.inf))
        ),
        phase_fixed_spectral_radius_binary64=_binary64_record(
            float(np.max(np.abs(np.linalg.eigvals(phase_fixed))))
        ),
        phase_fixed_one_return_inf_norm_binary64=_binary64_record(
            float(np.linalg.norm(phase_fixed, ord=np.inf))
        ),
        phase_fixed_two_return_inf_norm_binary64=_binary64_record(
            float(np.linalg.norm(phase_fixed @ phase_fixed, ord=np.inf))
        ),
    )


def _load_bound_parent(repository: Path, relative: str, expected: str) -> Mapping[str, Any]:
    path = repository / relative
    if _sha256_path(path) != expected:
        raise ValueError(f"a phase-fixed return parent changed: {relative}")
    payload = json.loads(path.read_text())
    if not isinstance(payload, Mapping):
        raise ValueError(f"{relative} must contain a mapping")
    return payload


def build_outer_phase_fixed_return_stage1(
    repository: Path,
) -> OuterPhaseFixedReturnStage1:
    repository = repository.resolve()
    if os.environ.get("OPENBLAS_NUM_THREADS") != "1":
        raise RuntimeError("the binary64 pilot requires OPENBLAS_NUM_THREADS=1")
    outer_payload = _load_bound_parent(
        repository, OUTER_RESULT_RELATIVE_PATH, OUTER_RESULT_SHA256
    )
    grushin_payload = _load_bound_parent(
        repository, GRUSHIN_RESULT_RELATIVE_PATH, GRUSHIN_RESULT_SHA256
    )
    orbit = validate_outer_high_resolution_artifact(
        outer_payload, repository, replay_directed=False
    )
    grushin = grushin_payload.get("certificate")
    if not isinstance(grushin, Mapping):
        raise ValueError("the outer Grushin parent has no certificate")
    if grushin.get("nested_correction_radius") != NESTED_EXACT_ORBIT_RADIUS:
        raise ValueError("the nested exact outer-orbit radius changed")
    if grushin.get(
        "exact_translation_zero_of_effective_hamiltonian_retained"
    ) is not True:
        raise ValueError("the exact outer translation identity is absent")

    pilots = tuple(_finite_pilot(orbit, step) for step in FINITE_SECTION_STEPS)
    budget = DirectedReturnInputBudget(
        phase_fixed_voltage_history_row_norm_upper=None,
        phase_fixed_recovery_row_norm_upper=None,
        return_derivative_lipschitz_upper=None,
        chosen_section_radius=CHOSEN_SECTION_RADIUS,
        validated_section_tube_radius_lower=None,
        directed_kernel_recurrence_validated=False,
        arbitrary_c0_input_covered_by_measure_representation=False,
        corrected_signed_measure_total_variation_validated=False,
        unique_first_positive_return_and_event_speed_validated=False,
        second_variational_return_kernel_validated=False,
        evidence_status=(
            "open: finite matrices strongly suggest contraction, but no "
            "directed signed-kernel total-variation or second-return-variation "
            "enclosure has been supplied"
        ),
    )
    evaluation = evaluate_directed_return_budget(budget)
    attachment_budget = AmbientToSectionInputBudget(
        ambient_complete_history_distance_upper=None,
        phase_chart_lipschitz_upper=None,
        validated_section_radius=CHOSEN_SECTION_RADIUS,
        ambient_distance_to_exact_phase_zero_orbit_validated=False,
        nonlinear_phase_chart_validated_on_ambient_tube=False,
        evidence_status=(
            "open: a pulse artifact must bound ambient complete-history "
            "distance to the exact phase-zero orbit, and the nonlinear phase "
            "chart must transport that distance to the section"
        ),
    )
    attachment_evaluation = evaluate_ambient_to_section_budget(attachment_budget)
    claims = {name: True for name in TRUE_FLAGS}
    claims.update({name: False for name in FALSE_FLAGS})
    return OuterPhaseFixedReturnStage1(
        schema_id=SCHEMA_ID,
        model_id=MODEL_ID,
        branch=BRANCH,
        arithmetic_scope=ARITHMETIC_SCOPE,
        parent_result_sha256={
            OUTER_RESULT_RELATIVE_PATH: OUTER_RESULT_SHA256,
            GRUSHIN_RESULT_RELATIVE_PATH: GRUSHIN_RESULT_SHA256,
        },
        nested_exact_orbit_radius=NESTED_EXACT_ORBIT_RADIUS,
        reduced_history_space=(
            "Y=C([-5*sqrt(5),0],R) x R with max{sup|h_v|,|h_w(0)|}"
        ),
        phase_section=(
            "h_v(0)=0; ell(h)=h_v(0)/dot(V_o)(0), ell(q)=1; "
            "phase projection I-q tensor ell"
        ),
        finite_section_pilot=pilots,
        finite_section_pilot_scope=(
            "binary64 sampled-input RK4 matrices only; spectral radii and row "
            "norms are diagnostics and do not bound the C0-history operator"
        ),
        matrix_measure_kernel_contract={
            "input_representation": (
                "u(t)=alpha_v(t)*h_w(0)+integral h_v(theta) dmu_t(theta); "
                "w(t)=alpha_w(t)*h_w(0)+integral h_v(theta) dnu_t(theta)"
            ),
            "initial_measures": (
                "mu_theta=Dirac_theta for -r<=theta<=0; nu_0=0; "
                "alpha_v(theta)=0 for theta<=0, alpha_w(0)=1"
            ),
            "measure_recurrence": (
                "mu_dot=a(t)mu-nu+b0(t)mu_(t-tau0)+b1(t)mu_(t-tau1); "
                "nu_dot=epsilon*(mu-nu), with the identical scalar recurrence "
                "for alpha"
            ),
            "physical_coefficients": (
                "a=1-V_o^2-epsilon*(kappa1+3*kappa3*(V_o-1)^2); "
                "bj=epsilon/2*(kappa1+3*kappa3*(V_o(t-tauj)-1)^2)"
            ),
            "phase_corrected_voltage_row": (
                "mu_(T+theta)-q_v(theta)*mu_T/q_v(0), and the same signed "
                "subtraction for the h_w(0) scalar coefficient"
            ),
            "phase_corrected_recovery_row": (
                "nu_T-q_w(0)*mu_T/q_v(0), and the same signed subtraction "
                "for the h_w(0) scalar coefficient"
            ),
            "phase_chart_norm": (
                "the same normalized event row and rank-one correction must "
                "also enclose Q_phase, the Lipschitz norm of the ambient-to-"
                "section phase chart; it is not inferred from a pulse voltage event"
            ),
            "section_quotient": (
                "drop the Dirac mass at theta=0 exactly because every input "
                "direction satisfies h_v(0)=0"
            ),
            "row_norm_identity": (
                "operator row norm = total variation of the corrected signed "
                "history measure modulo Dirac_0 plus absolute scalar coefficient"
            ),
            "voltage_output_norm": (
                "Q_voltage_history=sup over returned theta in [-r,0] of the row norm"
            ),
            "recovery_output_norm": "Q_recovery=the corrected current-recovery row norm",
            "directed_engine": (
                "interval-Taylor or Bernstein method of steps for the signed "
                "densities and atoms; prove total variation cellwise after "
                "phase subtraction, with coefficient and quadrature remainders"
            ),
            "arbitrary_continuous_input_guard": (
                "no nodal interpolation of h_v is allowed; dual signed-measure "
                "total variation must cover every h_v in C0"
            ),
            "nonlinear_increment": (
                "a second-variational matrix-measure enclosure supplies "
                "||DP(z)-DP(0)|| <= C_DP*||z|| on the radius-1e-4 tube"
            ),
        },
        input_budget=budget,
        evaluation=evaluation,
        ambient_to_section_budget=attachment_budget,
        ambient_to_section_evaluation=attachment_evaluation,
        claim_status=claims,
        conclusion=(
            "the four finite sections expose a large contraction margin, but "
            "the continuous-history signed-kernel and nonlinear bounds remain "
            "open; no outer attraction claim is promoted"
        ),
    )


def build_outer_phase_fixed_return_result(repository: Path) -> dict[str, Any]:
    repository = repository.resolve()
    certificate = json.loads(
        json.dumps(
            asdict(build_outer_phase_fixed_return_stage1(repository)),
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        )
    )
    return {
        "certificate": certificate,
        "manifest": {
            "schema_id": SCHEMA_ID,
            "result": RESULT_RELATIVE_PATH,
            "default_command": DEFAULT_COMMAND,
            "certificate_sha256": canonical_sha256(certificate),
            "source_sha256": {
                relative: _sha256_path(repository / relative)
                for relative in SOURCE_MANIFEST
            },
            "environment": {
                "python": platform.python_version(),
                "numpy": np.__version__,
                "scipy": scipy.__version__,
                "platform": platform.platform(),
                "openblas_num_threads": os.environ.get("OPENBLAS_NUM_THREADS"),
            },
        },
    }


def validate_outer_phase_fixed_return_result(
    payload: Mapping[str, Any], repository: Path
) -> None:
    if not isinstance(payload, Mapping) or set(payload) != {"certificate", "manifest"}:
        raise ValueError("phase-fixed return result fields changed")
    certificate = payload.get("certificate")
    manifest = payload.get("manifest")
    if not isinstance(certificate, Mapping) or not isinstance(manifest, Mapping):
        raise ValueError("phase-fixed return result is incomplete")
    if set(certificate) != {field.name for field in fields(OuterPhaseFixedReturnStage1)}:
        raise ValueError("phase-fixed return certificate fields changed")
    if canonical_sha256(certificate) != manifest.get("certificate_sha256"):
        raise ValueError("phase-fixed return certificate digest changed")
    if manifest.get("schema_id") != SCHEMA_ID or certificate.get("schema_id") != SCHEMA_ID:
        raise ValueError("phase-fixed return schema changed")
    sources = manifest.get("source_sha256")
    if not isinstance(sources, Mapping) or set(sources) != set(SOURCE_MANIFEST):
        raise ValueError("phase-fixed return source manifest changed")
    repository = repository.resolve()
    for relative in SOURCE_MANIFEST:
        if sources.get(relative) != _sha256_path(repository / relative):
            raise ValueError(f"phase-fixed return source changed: {relative}")
    claims = certificate.get("claim_status")
    if not isinstance(claims, Mapping) or set(claims) != set(TRUE_FLAGS + FALSE_FLAGS):
        raise ValueError("phase-fixed return claim ledger changed")
    if any(claims.get(name) is not True for name in TRUE_FLAGS):
        raise ValueError("a proved phase-fixed return contract fact was weakened")
    if any(claims.get(name) is not False for name in FALSE_FLAGS):
        raise ValueError("an open phase-fixed return claim was promoted")
    pilots = certificate.get("finite_section_pilot")
    if not isinstance(pilots, (list, tuple)) or [
        row.get("step_count") for row in pilots
    ] != list(FINITE_SECTION_STEPS):
        raise ValueError("the four-level finite-section pilot changed")
    for row in pilots:
        if not isinstance(row, Mapping):
            raise ValueError("a finite-section pilot row is missing")
        for name in (
            "stored_orbit_current_voltage_speed_binary64",
            "stored_translation_monodromy_residual_inf_binary64",
            "algebraic_phase_projection_tangent_residual_inf_binary64",
            "fixed_time_section_input_inf_norm_binary64",
            "rank_one_phase_correction_inf_norm_binary64",
            "phase_fixed_spectral_radius_binary64",
            "phase_fixed_one_return_inf_norm_binary64",
            "phase_fixed_two_return_inf_norm_binary64",
        ):
            _binary64_value(row.get(name), name)
    expected = json.loads(
        json.dumps(
            asdict(build_outer_phase_fixed_return_stage1(repository)),
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        )
    )
    if certificate != expected:
        raise ValueError("phase-fixed return certificate differs from source replay")


__all__ = [
    "CHOSEN_SECTION_RADIUS",
    "DEFAULT_COMMAND",
    "DirectedReturnEvaluation",
    "DirectedReturnInputBudget",
    "AmbientToSectionEvaluation",
    "AmbientToSectionInputBudget",
    "FALSE_FLAGS",
    "FINITE_SECTION_STEPS",
    "NOTE_RELATIVE_PATH",
    "RESULT_RELATIVE_PATH",
    "SOURCE_MANIFEST",
    "TRUE_FLAGS",
    "build_outer_phase_fixed_return_result",
    "build_outer_phase_fixed_return_stage1",
    "canonical_sha256",
    "evaluate_directed_return_budget",
    "evaluate_ambient_to_section_budget",
    "validate_outer_phase_fixed_return_result",
]
