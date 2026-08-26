"""History-space contract for outer attraction and two-sided pulse routing.

The module keeps three logically different statements separate.

* A local attracting tube around the validated outer periodic orbit is a
  consequence of a phase-fixed stable power bound and a nonlinear return-map
  derivative bound.  A Floquet zero count by itself is not such a tube.
* Exit from the inner stable sheet is controlled by the exact signed factor
  of the graph-straightened return map.  A positive unstable multiplier by
  itself does not route either side.
* The complete bounded exit slabs must be propagated by a directed method of steps
  into either the proved quiet Razumikhin sublevel or the outer section ball.

The current parents prove the outer orbit, its simple neutral multiplier, a
quadratic vector-field remainder near it, a qualitative inner stable sheet,
the physical pulse curve, the quiet history basin, and the complete-history
capture for J=3/10.  They do not prove the outer zero index, quantitative
stable projections, a signed inner exit, or either exit-face attachment.

The source-bound J=0.32 calculation below selects a concrete third-return
outer attachment target.  It remains a binary64 target: sampled or dense-grid
agreement is never interpreted as a continuous-history enclosure.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from decimal import Decimal, InvalidOperation, ROUND_CEILING, ROUND_FLOOR, localcontext
from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np

from canard_control.leaky_outer_high_resolution import (
    validate_outer_high_resolution_artifact,
)
from canard_control.leaky_pulse_separator_candidate import (
    TAU_1,
    _history_vector,
    _periodic_interpolator,
    binary64_record,
    finite_section,
    simulate_physical_pulse,
)


SCHEMA_ID = "leaky-outer-two-sided-routing-contract-v1"
MODEL_ID = "autonomous-leaky-recovery-two-delay-fhn-bistable-proposal"

SOURCE_RELATIVE_PATH = (
    "src/canard_control/leaky_outer_two_sided_routing_contract.py"
)
GENERATOR_RELATIVE_PATH = (
    "experiments/leaky_outer_two_sided_routing_contract.py"
)
RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_outer_two_sided_routing_contract.json"
)
NOTE_RELATIVE_PATH = "docs/leaky-outer-two-sided-routing-contract.md"
TEST_RELATIVE_PATH = "tests/test_leaky_outer_two_sided_routing_contract.py"

OUTER_ORBIT_RESULT = (
    "experiments/results/autonomous_leaky_recovery_outer_high_resolution.json"
)
FLOQUET_TRANSFER_RESULT = "experiments/results/leaky_floquet_transfer.json"
FLOQUET_RIESZ_RESULT = (
    "experiments/results/leaky_floquet_riesz_reduction.json"
)
OUTER_COVER_CALIBRATION_RESULT = (
    "experiments/results/leaky_floquet_outer_right_half_cover_calibration.json"
)
INNER_STAGE1_RESULT = (
    "experiments/results/leaky_inner_stable_manifold_stage1_contract.json"
)
INNER_STAGE2_RESULT = (
    "experiments/results/leaky_inner_stable_manifold_stage2_contract.json"
)
PULSE_TERMINAL_RESULT = "experiments/results/leaky_pulse_terminal_history.json"
PULSE_TARGET_RESULT = (
    "experiments/results/leaky_pulse_separator_validation_target.json"
)
QUIET_BASIN_RESULT = (
    "experiments/results/leaky_quiet_large_razumikhin_basin.json"
)
QUIET_CAPTURE_RESULT = "experiments/results/leaky_pulse_quiet_capture.json"
REDUCED_HISTORY_RESULT = "experiments/results/leaky_reduced_history.json"
DOBRUSHIN_STRIP_RESULT = (
    "experiments/results/leaky_dobrushin_transverse_halanay.json"
)

PARENT_RESULT_SHA256 = {
    OUTER_ORBIT_RESULT: (
        "d888916fed919f1515dd31ab851b2229816ea373365fa0221b1e345580f165a7"
    ),
    FLOQUET_TRANSFER_RESULT: (
        "5a3709ec792b29ed41533101245b13b3d35084ae508bdd1d420728200a5a5b16"
    ),
    FLOQUET_RIESZ_RESULT: (
        "5185f8f39cd8f87052a50b072af2bfee591d8cd626301bd9a9470134c14df55c"
    ),
    OUTER_COVER_CALIBRATION_RESULT: (
        "dd84499297d7808cd8b787f1d84f9eae235aadf992f60a3117c7050bbd1e6bd8"
    ),
    INNER_STAGE1_RESULT: (
        "3c400ec92f00d4c94313b6e0a5b514f60f21335f54cba41ad5ba8a4217e8f21b"
    ),
    INNER_STAGE2_RESULT: (
        "eafa4d07b0558d9d4ce7423969379fa51875fcabce55af89a2378261fdb1e18d"
    ),
    PULSE_TERMINAL_RESULT: (
        "db593b3675819f7b62180643ab983499e8e67790a0cacaf944ce099363a524c1"
    ),
    PULSE_TARGET_RESULT: (
        "175a03bad09c81c9289ee5747d870113c6afcc22b1ec23942379c4c81bcda917"
    ),
    QUIET_BASIN_RESULT: (
        "eab26b970511676f9048c17a49f013c0b7f2833a3a132204168e05f9735d0cba"
    ),
    QUIET_CAPTURE_RESULT: (
        "e930be63d80d4aac2cddb896d7ac1b2582a91690dc9649981848ea88e1e05723"
    ),
    REDUCED_HISTORY_RESULT: (
        "4555fb765a5060a3767a7ea669deb2f4921b8d7410d7d4e15ad077e552da8870"
    ),
    DOBRUSHIN_STRIP_RESULT: (
        "21e2e3d282e287f2246d2bc5c3d4dd92b6314e9b46c20d27737db7a94f7c0e25"
    ),
}

SOURCE_MANIFEST = (
    SOURCE_RELATIVE_PATH,
    GENERATOR_RELATIVE_PATH,
    NOTE_RELATIVE_PATH,
)

DEFAULT_COMMAND = (
    "OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONPATH=src "
    "/usr/bin/python3 experiments/leaky_outer_two_sided_routing_contract.py"
)
ARITHMETIC_SCOPE = (
    "exact parent-byte and source-manifest binding; 96-digit outward Decimal "
    "evaluation of sufficient history-space inequalities; exact polynomial "
    "Taylor remainder algebra around the directed outer-orbit strip; and a "
    "source-bound but non-directed binary64 J=0.32 third-return target"
)

OUTER_TARGET_PULSE = 0.32
OUTER_TARGET_SECTION_STEPS = 180
OUTER_TARGET_CROSSING_DEPTH = 3
OUTER_TARGET_FINAL_TIME = 100.0
OUTER_TARGET_DENSE_HISTORY_SAMPLES = 4097
OUTER_TARGET_REFINEMENTS = (
    (2.0e-10, 2.0e-12, 0.04),
    (2.0e-11, 2.0e-13, 0.02),
    (2.0e-12, 2.0e-14, 0.01),
)

TRUE_CLAIMS = (
    "outer_periodic_rfde_orbit_validated",
    "outer_neutral_multiplier_algebraically_simple_validated",
    "outer_local_vector_field_quadratic_remainder_validated",
    "outer_local_vector_field_second_derivative_bound_validated",
    "reduced_history_future_factorization_validated",
    "qualitative_inner_codimension_one_stable_manifold_validated",
    "physical_pulse_terminal_history_curve_oriented_c1_validated",
    "large_quiet_razumikhin_history_basin_validated",
    "pulse_J_030_complete_history_quiet_capture_validated",
    "nonexplicit_open_quiet_history_neighborhood_of_J_030_proved",
    "nonexplicit_open_quiet_pulse_interval_around_J_030_proved",
    "pulse_J_032_outer_attachment_target_source_bound_observed",
    "narrow_candidate_pulse_bracket_source_bound_observed",
)

FALSE_CLAIMS = (
    "center_outer_zero_index_validated",
    "outer_stable_riesz_projection_norm_validated",
    "outer_stable_power_bound_validated",
    "outer_quantitative_attracting_tube_validated",
    "inner_quantitative_stable_graph_validated",
    "inner_signed_exit_factor_validated",
    "quiet_inner_exit_face_attachment_validated",
    "outer_inner_exit_face_attachment_validated",
    "two_sided_basin_routing_validated",
    "physical_pulse_stable_sheet_crossing_validated",
    "unique_physical_pulse_onset_validated",
    "physical_pulse_Jc_validated",
    "frequency_amplitude_safety_control_theorem_validated",
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


def _json_normalize(value: Any) -> Any:
    """Apply the exact tuple-to-array normalization used by JSON storage."""

    return json.loads(
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        )
    )


def _mapping(value: Any, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{name} must be a mapping")
    return value


def _load_parent(repository: Path, relative: str) -> Mapping[str, Any]:
    path = repository / relative
    raw = path.read_bytes()
    expected = PARENT_RESULT_SHA256[relative]
    if sha256(raw).hexdigest() != expected:
        raise ValueError(f"a bound routing parent changed: {relative}")
    payload = json.loads(raw)
    return _mapping(payload, relative)


def _decimal(value: str | None, name: str) -> Decimal | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError(f"{name} must be a decimal string or null")
    try:
        number = Decimal(value)
    except InvalidOperation as error:
        raise ValueError(f"{name} is not a decimal") from error
    if not number.is_finite():
        raise ValueError(f"{name} must be finite")
    return number


def _upper(value: Decimal) -> str:
    with localcontext() as context:
        context.prec = 96
        context.rounding = ROUND_CEILING
        return format(+value, "f")


def _lower(value: Decimal) -> str:
    with localcontext() as context:
        context.prec = 96
        context.rounding = ROUND_FLOOR
        return format(+value, "f")


def _positive_optional(value: str | None, name: str) -> Decimal | None:
    number = _decimal(value, name)
    if number is not None and number <= 0:
        raise ValueError(f"{name} must be positive when supplied")
    return number


def _nonnegative_optional(value: str | None, name: str) -> Decimal | None:
    number = _decimal(value, name)
    if number is not None and number < 0:
        raise ValueError(f"{name} must be nonnegative when supplied")
    return number


@dataclass(frozen=True)
class OuterAttractingTubeInputBudget:
    """Inputs for a quantitative phase-fixed outer attracting tube."""

    outer_zero_index_validated: bool
    neutral_multiplier_algebraically_simple_validated: bool
    reduced_phase_section_and_return_map_validated: bool
    stable_spectral_radius_upper: str | None
    stable_power_constant_upper: str | None
    stable_riesz_projection_norm_upper: str | None
    phase_chart_projection_norm_upper: str | None
    return_iterate_count: int | None
    m_return_nonlinear_derivative_coefficient_upper: str | None
    chosen_section_radius: str | None
    validated_return_map_domain_radius_lower: str | None
    interreturn_flow_lipschitz_upper: str | None
    interreturn_flow_tube_validated: bool
    evidence_status: str


@dataclass(frozen=True)
class OuterAttractingTubeEvaluation:
    input_complete: bool
    missing_inputs: tuple[str, ...]
    missing_artifacts: tuple[str, ...]
    linear_m_return_norm_upper: str | None
    m_return_lipschitz_upper: str | None
    domain_contains_chosen_ball: bool
    strict_contraction_inequality_holds: bool
    outer_attracting_tube_closes: bool
    linear_power_formula: str
    nonlinear_contraction_formula: str
    sufficient_inequality: str
    conclusion: str


OUTER_TUBE_NUMERIC_FIELDS = (
    "stable_spectral_radius_upper",
    "stable_power_constant_upper",
    "stable_riesz_projection_norm_upper",
    "phase_chart_projection_norm_upper",
    "return_iterate_count",
    "m_return_nonlinear_derivative_coefficient_upper",
    "chosen_section_radius",
    "validated_return_map_domain_radius_lower",
    "interreturn_flow_lipschitz_upper",
)


def evaluate_outer_attracting_tube(
    budget: OuterAttractingTubeInputBudget,
) -> OuterAttractingTubeEvaluation:
    """Evaluate the weakest direct m-return contraction inequality.

    The stable spectral radius is never used as a one-step norm.  Instead a
    separately validated power constant gives ``q_m <= K_s rho_s**m``.  If
    ``||D N_m(z)|| <= C_m ||z||`` on the chosen section ball, then
    ``K_s rho_s**m + C_m r < 1`` makes the m-return map a contraction.
    """

    missing = tuple(
        name for name in OUTER_TUBE_NUMERIC_FIELDS if getattr(budget, name) is None
    )
    artifacts: list[str] = []
    if not budget.outer_zero_index_validated:
        artifacts.append("outer_zero_index")
    if not budget.neutral_multiplier_algebraically_simple_validated:
        artifacts.append("simple_neutral_multiplier")
    if not budget.reduced_phase_section_and_return_map_validated:
        artifacts.append("reduced_phase_section_and_return_map")
    if not budget.interreturn_flow_tube_validated:
        artifacts.append("interreturn_flow_tube")

    rho = _positive_optional(
        budget.stable_spectral_radius_upper, "stable_spectral_radius_upper"
    )
    constant = _positive_optional(
        budget.stable_power_constant_upper, "stable_power_constant_upper"
    )
    projection = _positive_optional(
        budget.stable_riesz_projection_norm_upper,
        "stable_riesz_projection_norm_upper",
    )
    chart = _positive_optional(
        budget.phase_chart_projection_norm_upper,
        "phase_chart_projection_norm_upper",
    )
    coefficient = _nonnegative_optional(
        budget.m_return_nonlinear_derivative_coefficient_upper,
        "m_return_nonlinear_derivative_coefficient_upper",
    )
    radius = _positive_optional(budget.chosen_section_radius, "chosen_section_radius")
    domain = _positive_optional(
        budget.validated_return_map_domain_radius_lower,
        "validated_return_map_domain_radius_lower",
    )
    flow_lipschitz = _positive_optional(
        budget.interreturn_flow_lipschitz_upper,
        "interreturn_flow_lipschitz_upper",
    )
    count = budget.return_iterate_count
    if count is not None and (type(count) is not int or count < 1):
        raise ValueError("return_iterate_count must be a positive integer")
    if rho is not None and rho >= 1:
        raise ValueError("stable_spectral_radius_upper must be below one")
    for number, name in (
        (constant, "stable_power_constant_upper"),
        (projection, "stable_riesz_projection_norm_upper"),
        (chart, "phase_chart_projection_norm_upper"),
    ):
        if number is not None and number < 1:
            raise ValueError(f"{name} must be at least one")

    q_text: str | None = None
    lip_text: str | None = None
    domain_ok = False
    contraction = False
    complete = not missing
    if complete:
        assert rho is not None
        assert constant is not None
        assert projection is not None
        assert chart is not None
        assert count is not None
        assert coefficient is not None
        assert radius is not None
        assert domain is not None
        assert flow_lipschitz is not None
        with localcontext() as context:
            context.prec = 96
            context.rounding = ROUND_CEILING
            q = constant * context.power(rho, count)
            lip = q + coefficient * radius
        q_text = _upper(q)
        lip_text = _upper(lip)
        domain_ok = domain >= radius
        contraction = lip < 1

    closes = complete and not artifacts and domain_ok and contraction
    return OuterAttractingTubeEvaluation(
        input_complete=complete,
        missing_inputs=missing,
        missing_artifacts=tuple(artifacts),
        linear_m_return_norm_upper=q_text,
        m_return_lipschitz_upper=lip_text,
        domain_contains_chosen_ball=domain_ok,
        strict_contraction_inequality_holds=contraction,
        outer_attracting_tube_closes=closes,
        linear_power_formula="q_m=K_s*rho_s^m",
        nonlinear_contraction_formula="Lambda_o=q_m+C_m*r_o",
        sufficient_inequality=(
            "validated phase/return tube, r_o<=R_domain, and "
            "K_s*rho_s^m+C_m*r_o<1"
        ),
        conclusion=(
            "the flow sweep of the section ball is a local orbital attracting "
            "tube, with contraction sampled every m returns"
        ),
    )


@dataclass(frozen=True)
class SignedInnerExitInputBudget:
    """Inputs for first exit from a graph-straightened inner cylinder."""

    quantitative_inner_stable_graph_validated: bool
    graph_straightened_return_map_cylinder_validated: bool
    unstable_multiplier_modulus_lower: str
    unstable_multiplier_modulus_upper: str
    signed_gap_factor_deviation_upper: str | None
    stable_row_contraction_upper: str | None
    stable_row_gap_coupling_upper: str | None
    stable_coordinate_radius: str | None
    signed_exit_gap: str | None
    validated_coordinate_gap_radius_lower: str | None
    evidence_status: str


@dataclass(frozen=True)
class SignedInnerExitEvaluation:
    input_complete: bool
    missing_inputs: tuple[str, ...]
    missing_artifacts: tuple[str, ...]
    signed_factor_lower: str | None
    signed_factor_upper: str | None
    signed_expansion_margin_lower: str | None
    stable_row_image_radius_upper: str | None
    stable_coordinate_confinement_holds: bool
    exit_slab_gap_upper: str | None
    coordinate_chart_contains_exit_slab: bool
    signed_exit_closes: bool
    exact_factor_identity: str
    first_exit_bound: str
    exit_slab: str


SIGNED_EXIT_OPTIONAL_FIELDS = (
    "signed_gap_factor_deviation_upper",
    "stable_row_contraction_upper",
    "stable_row_gap_coupling_upper",
    "stable_coordinate_radius",
    "signed_exit_gap",
    "validated_coordinate_gap_radius_lower",
)


def evaluate_signed_inner_exit(
    budget: SignedInnerExitInputBudget,
) -> SignedInnerExitEvaluation:
    """Evaluate sign preservation, expansion, and stable-row confinement.

    In coordinates ``delta=u-h(z)``, invariance of the stable graph gives the
    exact factorization ``delta(P(u,z))=a(delta,z) delta``.  Bounding the
    factor itself is weaker than validating a full invariant cone.
    """

    mu_lower = _positive_optional(
        budget.unstable_multiplier_modulus_lower,
        "unstable_multiplier_modulus_lower",
    )
    mu_upper = _positive_optional(
        budget.unstable_multiplier_modulus_upper,
        "unstable_multiplier_modulus_upper",
    )
    assert mu_lower is not None and mu_upper is not None
    if mu_lower > mu_upper:
        raise ValueError("unstable multiplier interval is reversed")
    missing = tuple(
        name for name in SIGNED_EXIT_OPTIONAL_FIELDS if getattr(budget, name) is None
    )
    artifacts: list[str] = []
    if not budget.quantitative_inner_stable_graph_validated:
        artifacts.append("quantitative_inner_stable_graph")
    if not budget.graph_straightened_return_map_cylinder_validated:
        artifacts.append("graph_straightened_return_map_cylinder")

    deviation = _nonnegative_optional(
        budget.signed_gap_factor_deviation_upper,
        "signed_gap_factor_deviation_upper",
    )
    q_z = _nonnegative_optional(
        budget.stable_row_contraction_upper,
        "stable_row_contraction_upper",
    )
    b_z = _nonnegative_optional(
        budget.stable_row_gap_coupling_upper,
        "stable_row_gap_coupling_upper",
    )
    r_z = _positive_optional(
        budget.stable_coordinate_radius, "stable_coordinate_radius"
    )
    d_exit = _positive_optional(budget.signed_exit_gap, "signed_exit_gap")
    gap_domain = _positive_optional(
        budget.validated_coordinate_gap_radius_lower,
        "validated_coordinate_gap_radius_lower",
    )

    factor_lower_text: str | None = None
    factor_upper_text: str | None = None
    expansion_text: str | None = None
    stable_image_text: str | None = None
    slab_text: str | None = None
    confinement = False
    chart_contains = False
    expansion = False
    complete = not missing
    if complete:
        assert deviation is not None
        assert q_z is not None
        assert b_z is not None
        assert r_z is not None
        assert d_exit is not None
        assert gap_domain is not None
        with localcontext() as context:
            context.prec = 96
            context.rounding = ROUND_FLOOR
            factor_lower = mu_lower - deviation
            expansion_margin = factor_lower - 1
        with localcontext() as context:
            context.prec = 96
            context.rounding = ROUND_CEILING
            factor_upper = mu_upper + deviation
            stable_image = q_z * r_z + b_z * d_exit
            slab_upper = factor_upper * d_exit
        factor_lower_text = _lower(factor_lower)
        factor_upper_text = _upper(factor_upper)
        expansion_text = _lower(expansion_margin)
        stable_image_text = _upper(stable_image)
        slab_text = _upper(slab_upper)
        expansion = factor_lower > 1
        confinement = stable_image < r_z
        chart_contains = gap_domain >= slab_upper

    closes = complete and not artifacts and expansion and confinement and chart_contains
    return SignedInnerExitEvaluation(
        input_complete=complete,
        missing_inputs=missing,
        missing_artifacts=tuple(artifacts),
        signed_factor_lower=factor_lower_text,
        signed_factor_upper=factor_upper_text,
        signed_expansion_margin_lower=expansion_text,
        stable_row_image_radius_upper=stable_image_text,
        stable_coordinate_confinement_holds=confinement,
        exit_slab_gap_upper=slab_text,
        coordinate_chart_contains_exit_slab=chart_contains,
        signed_exit_closes=closes,
        exact_factor_identity=(
            "delta(P(u,z))=a(delta,z)*delta, delta=u-h(z), from invariance "
            "of u=h(z) and the scalar mean-value formula"
        ),
        first_exit_bound=(
            "n_exit<=ceil(log(d_exit/|delta_0|)/log(m_delta)) for "
            "0<|delta_0|<d_exit"
        ),
        exit_slab=(
            "d_exit<=+/-delta<=M_delta*d_exit, ||z||<=r_z, with the sign "
            "fixed by delta_0"
        ),
    )


@dataclass(frozen=True)
class QuietAttachmentInputBudget:
    """Terminal retained-history inequality for the quiet target."""

    initial_set_is_complete_signed_inner_exit_face: bool
    directed_method_of_steps_family_tube_validated: bool
    complete_retained_history_bernstein_bound_validated: bool
    retained_guide_lyapunov_upper: str | None
    retained_p_norm_error_upper: str | None
    quiet_p_norm_threshold_lower: str
    evidence_status: str


@dataclass(frozen=True)
class QuietAttachmentEvaluation:
    input_complete: bool
    missing_inputs: tuple[str, ...]
    retained_total_p_norm_upper: str | None
    quiet_target_margin_lower: str | None
    quiet_target_inequality_closes: bool
    quiet_exit_face_attachment_closes: bool
    sufficient_inequality: str


def evaluate_quiet_attachment(
    budget: QuietAttachmentInputBudget,
) -> QuietAttachmentEvaluation:
    guide = _nonnegative_optional(
        budget.retained_guide_lyapunov_upper,
        "retained_guide_lyapunov_upper",
    )
    error = _nonnegative_optional(
        budget.retained_p_norm_error_upper,
        "retained_p_norm_error_upper",
    )
    threshold = _positive_optional(
        budget.quiet_p_norm_threshold_lower,
        "quiet_p_norm_threshold_lower",
    )
    assert threshold is not None
    missing = tuple(
        name
        for name in (
            "retained_guide_lyapunov_upper",
            "retained_p_norm_error_upper",
        )
        if getattr(budget, name) is None
    )
    total_text: str | None = None
    margin_text: str | None = None
    target = False
    if not missing:
        assert guide is not None and error is not None
        with localcontext() as context:
            context.prec = 96
            context.rounding = ROUND_CEILING
            total = context.sqrt(guide) + error
        with localcontext() as context:
            context.prec = 96
            context.rounding = ROUND_FLOOR
            margin = threshold - total
        total_text = _upper(total)
        margin_text = _lower(margin)
        target = margin > 0
    attachment = (
        target
        and budget.initial_set_is_complete_signed_inner_exit_face
        and budget.directed_method_of_steps_family_tube_validated
        and budget.complete_retained_history_bernstein_bound_validated
    )
    return QuietAttachmentEvaluation(
        input_complete=not missing,
        missing_inputs=missing,
        retained_total_p_norm_upper=total_text,
        quiet_target_margin_lower=margin_text,
        quiet_target_inequality_closes=target,
        quiet_exit_face_attachment_closes=attachment,
        sufficient_inequality=(
            "sqrt(sup_Bernstein (z_hat-E_q)^T P (z_hat-E_q))"
            "+E_P < 1/sqrt(125) on the entire retained history"
        ),
    )


@dataclass(frozen=True)
class OuterAttachmentInputBudget:
    """Event-corrected entry inequality for the outer section ball."""

    initial_set_is_complete_signed_inner_exit_face: bool
    directed_method_of_steps_family_tube_validated: bool
    continuous_history_bernstein_distance_validated: bool
    outer_section_event_bracket_validated: bool
    outer_section_event_speed_lower: str | None
    continuous_guide_to_candidate_orbit_upper: str | None
    method_of_steps_history_error_upper: str | None
    exact_outer_orbit_correction_upper: str
    event_time_error_upper: str | None
    history_speed_upper_on_event_tube: str | None
    section_reference_and_phase_error_upper: str | None
    section_chart_projection_norm_upper: str | None
    outer_section_ball_radius_lower: str | None
    outer_attracting_tube_validated: bool
    evidence_status: str


@dataclass(frozen=True)
class OuterAttachmentEvaluation:
    input_complete: bool
    missing_inputs: tuple[str, ...]
    raw_event_history_error_upper: str | None
    projected_section_error_upper: str | None
    outer_section_entry_margin_lower: str | None
    outer_section_entry_inequality_closes: bool
    outer_exit_face_attachment_closes: bool
    event_history_error_formula: str
    sufficient_inequality: str


OUTER_ATTACHMENT_OPTIONAL_FIELDS = (
    "outer_section_event_speed_lower",
    "continuous_guide_to_candidate_orbit_upper",
    "method_of_steps_history_error_upper",
    "event_time_error_upper",
    "history_speed_upper_on_event_tube",
    "section_reference_and_phase_error_upper",
    "section_chart_projection_norm_upper",
    "outer_section_ball_radius_lower",
)


def evaluate_outer_attachment(
    budget: OuterAttachmentInputBudget,
) -> OuterAttachmentEvaluation:
    correction = _nonnegative_optional(
        budget.exact_outer_orbit_correction_upper,
        "exact_outer_orbit_correction_upper",
    )
    assert correction is not None
    for name in OUTER_ATTACHMENT_OPTIONAL_FIELDS:
        value = getattr(budget, name)
        if name == "outer_section_event_speed_lower":
            _positive_optional(value, name)
        elif name in {
            "history_speed_upper_on_event_tube",
            "section_chart_projection_norm_upper",
            "outer_section_ball_radius_lower",
        }:
            _positive_optional(value, name)
        else:
            _nonnegative_optional(value, name)
    missing = tuple(
        name for name in OUTER_ATTACHMENT_OPTIONAL_FIELDS if getattr(budget, name) is None
    )
    raw_text: str | None = None
    projected_text: str | None = None
    margin_text: str | None = None
    entry = False
    if not missing:
        guide = _decimal(
            budget.continuous_guide_to_candidate_orbit_upper,
            "continuous_guide_to_candidate_orbit_upper",
        )
        flow = _decimal(
            budget.method_of_steps_history_error_upper,
            "method_of_steps_history_error_upper",
        )
        event_time = _decimal(
            budget.event_time_error_upper, "event_time_error_upper"
        )
        speed = _decimal(
            budget.history_speed_upper_on_event_tube,
            "history_speed_upper_on_event_tube",
        )
        section = _decimal(
            budget.section_reference_and_phase_error_upper,
            "section_reference_and_phase_error_upper",
        )
        chart = _decimal(
            budget.section_chart_projection_norm_upper,
            "section_chart_projection_norm_upper",
        )
        radius = _decimal(
            budget.outer_section_ball_radius_lower,
            "outer_section_ball_radius_lower",
        )
        assert all(
            value is not None
            for value in (guide, flow, event_time, speed, section, chart, radius)
        )
        with localcontext() as context:
            context.prec = 96
            context.rounding = ROUND_CEILING
            raw = guide + flow + correction + event_time * speed + section  # type: ignore[operator]
            projected = chart * raw  # type: ignore[operator]
        with localcontext() as context:
            context.prec = 96
            context.rounding = ROUND_FLOOR
            margin = radius - projected  # type: ignore[operator]
        raw_text = _upper(raw)
        projected_text = _upper(projected)
        margin_text = _lower(margin)
        entry = margin > 0
    attachment = (
        entry
        and budget.initial_set_is_complete_signed_inner_exit_face
        and budget.directed_method_of_steps_family_tube_validated
        and budget.continuous_history_bernstein_distance_validated
        and budget.outer_section_event_bracket_validated
        and budget.outer_attracting_tube_validated
    )
    return OuterAttachmentEvaluation(
        input_complete=not missing,
        missing_inputs=missing,
        raw_event_history_error_upper=raw_text,
        projected_section_error_upper=projected_text,
        outer_section_entry_margin_lower=margin_text,
        outer_section_entry_inequality_closes=entry,
        outer_exit_face_attachment_closes=attachment,
        event_history_error_formula=(
            "E_raw=E_guide+E_flow+E_orbit+E_time*F_tube+E_section"
        ),
        sufficient_inequality="Q_section*E_raw < r_outer",
    )


def _outer_attachment_target(
    outer_payload: Mapping[str, Any], repository: Path
) -> dict[str, Any]:
    """Build the non-directed J=.32 third-return attachment target."""

    orbit = validate_outer_high_resolution_artifact(
        outer_payload, repository, replay_directed=False
    )
    section = finite_section(orbit, OUTER_TARGET_SECTION_STEPS)
    voltage, _ = _periodic_interpolator(orbit.state[:, 0], orbit.period)
    recovery, _ = _periodic_interpolator(orbit.state[:, 1], orbit.period)
    rows: list[dict[str, Any]] = []
    for rtol, atol, max_step in OUTER_TARGET_REFINEMENTS:
        trajectory = simulate_physical_pulse(
            OUTER_TARGET_PULSE,
            section.section_voltage,
            final_time=OUTER_TARGET_FINAL_TIME,
            integration_rtol=rtol,
            integration_atol=atol,
            integration_max_step=max_step,
        )
        if len(trajectory.crossings) < OUTER_TARGET_CROSSING_DEPTH:
            raise ArithmeticError("J=.32 target has too few outer section crossings")
        crossing = trajectory.crossings[OUTER_TARGET_CROSSING_DEPTH - 1]
        mesh_difference = _history_vector(trajectory, section, crossing) - section.reference
        theta = np.linspace(
            -TAU_1,
            0.0,
            OUTER_TARGET_DENSE_HISTORY_SAMPLES,
            dtype=float,
        )
        dense_voltage_difference = np.asarray(
            [
                trajectory.state(crossing + offset)[0] - voltage(offset)
                for offset in theta
            ],
            dtype=float,
        )
        recovery_difference = float(
            trajectory.state(crossing)[1] - recovery(0.0)
        )
        dense_reduced = max(
            float(np.max(np.abs(dense_voltage_difference))),
            abs(recovery_difference),
        )
        rows.append(
            {
                "integration_rtol": binary64_record(rtol),
                "integration_atol": binary64_record(atol),
                "integration_max_step": binary64_record(max_step),
                "third_positive_crossing_time": binary64_record(crossing),
                "finite_mesh_reduced_sup_distance": binary64_record(
                    float(np.max(np.abs(mesh_difference)))
                ),
                "finite_mesh_reduced_l2_distance": binary64_record(
                    float(np.linalg.norm(mesh_difference))
                ),
                "dense_sample_voltage_history_sup_distance": binary64_record(
                    float(np.max(np.abs(dense_voltage_difference)))
                ),
                "current_recovery_distance": binary64_record(
                    abs(recovery_difference)
                ),
                "dense_sample_reduced_sup_distance": binary64_record(
                    dense_reduced
                ),
            }
        )
    crossing_values = [
        float(row["third_positive_crossing_time"]["decimal"]) for row in rows
    ]
    distance_values = [
        float(row["dense_sample_reduced_sup_distance"]["decimal"]) for row in rows
    ]
    if max(distance_values) >= 1.0e-5:
        raise ArithmeticError("the source-bound outer target left its design radius")
    return {
        "status": "source_bound_binary64_target_not_history_enclosure",
        "pulse_amplitude": binary64_record(OUTER_TARGET_PULSE),
        "section_step_count": OUTER_TARGET_SECTION_STEPS,
        "crossing_depth": OUTER_TARGET_CROSSING_DEPTH,
        "final_time": binary64_record(OUTER_TARGET_FINAL_TIME),
        "dense_history_sample_count": OUTER_TARGET_DENSE_HISTORY_SAMPLES,
        "candidate_outer_section_voltage": binary64_record(
            section.section_voltage
        ),
        "candidate_outer_section_voltage_derivative": binary64_record(
            section.section_voltage_derivative
        ),
        "rows": rows,
        "cross_refinement_crossing_time_spread": binary64_record(
            max(crossing_values) - min(crossing_values)
        ),
        "cross_refinement_dense_distance_spread": binary64_record(
            max(distance_values) - min(distance_values)
        ),
        "maximum_observed_dense_reduced_sup_distance": binary64_record(
            max(distance_values)
        ),
        "continuous_history_distance_validated": False,
        "directed_method_of_steps_error_validated": False,
        "outer_attracting_tube_entry_validated": False,
        "outer_basin_capture_validated": False,
    }


def _outer_local_field_evidence(
    dobrushin_payload: Mapping[str, Any],
) -> dict[str, Any]:
    certificate = _mapping(dobrushin_payload.get("certificate"), "Dobrushin certificate")
    outer = _mapping(certificate.get("outer"), "outer strip")
    if outer.get("exact_periodic_orbit_strip_validated") is not True:
        raise ValueError("the outer exact-orbit strip is not validated")
    centered = _decimal(
        outer.get("exact_centered_voltage_abs_upper"),
        "outer centered voltage bound",
    )
    margin = _decimal(outer.get("strict_strip_margin_lower"), "outer strip margin")
    tangent = _decimal(
        outer.get("exact_orbit_tangent_norm_upper"), "outer tangent bound"
    )
    period_lower = _decimal(outer.get("minimum_period_lower"), "outer period lower")
    assert centered is not None and margin is not None
    assert tangent is not None and period_lower is not None
    radius = Decimal("0.01")
    if radius >= margin or centered + radius >= Decimal("2.5"):
        raise ArithmeticError("the chosen local tube does not fit the proved strip")
    delayed_gain = Decimal("0.001")  # epsilon*kappa_3=(1/5)(1/200)
    with localcontext() as context:
        context.prec = 96
        context.rounding = ROUND_CEILING
        quadratic = (
            Decimal(1)
            + centered
            + radius / Decimal(3)
            + Decimal(2)
            * delayed_gain
            * (Decimal(3) * centered + radius)
        )
        second = (
            Decimal(2) * (Decimal(1) + centered + radius)
            + Decimal(12) * delayed_gain * (centered + radius)
        )
        physical_history_speed = tangent / period_lower
    return {
        "history_norm": "max{sup|delta v|,sup|delta w|} on X",
        "exact_outer_centered_voltage_abs_upper": str(centered),
        "proved_strip_radius": "2.5",
        "strict_outer_orbit_strip_margin_lower": str(margin),
        "declared_local_history_radius": "0.01",
        "declared_tube_remains_inside_proved_voltage_strip": True,
        "epsilon_times_kappa3": "0.001",
        "quadratic_vector_field_remainder_coefficient_upper": _upper(quadratic),
        "quadratic_remainder_formula": (
            "C_R(r)=1+B+r/3+2*epsilon*kappa3*(3*B+r), "
            "||F(Gamma+eta)-F(Gamma)-DF(Gamma)eta||<=C_R(r)||eta||_X^2"
        ),
        "vector_field_second_derivative_norm_upper": _upper(second),
        "second_derivative_formula": (
            "B_2(r)=2*(1+B+r)+12*epsilon*kappa3*(B+r)"
        ),
        "exact_outer_physical_history_speed_upper": _upper(
            physical_history_speed
        ),
        "outer_return_map_c2_bound_inferred_from_field_bound_alone": False,
        "quadratic_vector_field_remainder_validated": True,
        "vector_field_second_derivative_bound_validated": True,
    }


def _parent_evidence(parents: Mapping[str, Mapping[str, Any]]) -> dict[str, Any]:
    outer_artifact = _mapping(parents[OUTER_ORBIT_RESULT].get("artifact"), "outer artifact")
    outer_claims = _mapping(outer_artifact.get("claim_status"), "outer claims")
    transfer_artifact = _mapping(
        parents[FLOQUET_TRANSFER_RESULT].get("artifact"), "Floquet transfer"
    )
    transfer_outer = _mapping(
        _mapping(transfer_artifact.get("branches"), "Floquet branches").get(
            "outer_pulse"
        ),
        "outer Floquet transfer",
    )
    riesz_artifact = _mapping(
        parents[FLOQUET_RIESZ_RESULT].get("artifact"), "Riesz artifact"
    )
    riesz_outer = _mapping(
        _mapping(riesz_artifact.get("branches"), "Riesz branches").get(
            "outer_pulse"
        ),
        "outer Riesz branch",
    )
    stage1 = _mapping(parents[INNER_STAGE1_RESULT].get("contract"), "Stage 1")
    stage2 = _mapping(parents[INNER_STAGE2_RESULT].get("contract"), "Stage 2")
    pulse = _mapping(
        _mapping(parents[PULSE_TERMINAL_RESULT].get("audit"), "pulse audit").get(
            "certificate"
        ),
        "pulse certificate",
    )
    quiet_basin = _mapping(
        parents[QUIET_BASIN_RESULT].get("certificate"), "quiet basin"
    )
    quiet_capture = _mapping(
        parents[QUIET_CAPTURE_RESULT].get("certificate"), "quiet capture"
    )
    reduced = _mapping(
        parents[REDUCED_HISTORY_RESULT].get("certificate"), "reduced history"
    )
    target = _mapping(parents[PULSE_TARGET_RESULT].get("target"), "pulse target")
    calibration = _mapping(
        parents[OUTER_COVER_CALIBRATION_RESULT].get("claim_ledger"),
        "outer calibration claims",
    )
    stage1_claims = _mapping(stage1.get("claim_status"), "Stage 1 claims")
    stage2_claims = _mapping(stage2.get("claim_status"), "Stage 2 claims")
    target_claims = _mapping(target.get("claim_status"), "target claims")

    required_true = {
        "outer orbit": outer_claims.get("periodic_rfde_orbit_validated"),
        "outer neutral simplicity": transfer_outer.get(
            "neutral_multiplier_algebraically_simple_validated"
        ),
        "outer Schur reduction": riesz_outer.get(
            "analytic_finite_schur_reduction_proved"
        ),
        "inner qualitative stable manifold": stage1_claims.get(
            "qualitative_reduced_history_inner_stable_manifold_c1_proved"
        ),
        "pulse curve": pulse.get("terminal_history_curve_oriented_c1_embedding_proved"),
        "quiet basin": quiet_basin.get("large_quiet_history_basin_validated"),
        "quiet capture": quiet_capture.get("pulse_J_030_quiet_capture_proved"),
        "reduced factorization": reduced.get(
            "full_semiflow_factors_through_reduced_semiflow_proved"
        ),
        "candidate bracket": target_claims.get(
            "registered_root_strictly_inside_narrow_bracket_observed"
        ),
    }
    if any(value is not True for value in required_true.values()):
        raise ValueError("a required routing parent theorem was weakened")
    required_false = {
        "outer zero index": calibration.get(
            "center_parameter_outer_floquet_count_validated"
        ),
        "inner quantitative graph": stage2_claims.get(
            "inner_local_stable_graph_quantitatively_validated"
        ),
        "pulse crossing": target_claims.get(
            "physical_pulse_separator_crossing_validated"
        ),
        "two-sided routing": target_claims.get(
            "two_sided_basin_routing_validated"
        ),
        "onset": target_claims.get("unique_physical_pulse_onset_validated"),
    }
    if any(value is not False for value in required_false.values()):
        raise ValueError("an open routing parent claim was promoted")

    stage1_evidence = _mapping(
        stage1.get("proved_parent_evidence"), "Stage 1 parent evidence"
    )
    return {
        "outer_periodic_rfde_orbit_validated": True,
        "outer_neutral_multiplier_algebraically_simple_validated": True,
        "outer_finite_schur_reduction_validated": True,
        "center_outer_zero_index_validated": False,
        "outer_stable_projection_or_power_constants_validated": False,
        "qualitative_inner_stable_manifold_validated": True,
        "quantitative_inner_stable_graph_validated": False,
        "inner_unstable_multiplier_modulus_lower": stage1_evidence[
            "unstable_multiplier_modulus_lower"
        ],
        "inner_unstable_multiplier_modulus_upper": stage1_evidence[
            "unstable_multiplier_modulus_upper"
        ],
        "physical_pulse_curve_oriented_c1_validated": True,
        "quiet_history_basin_validated": True,
        "pulse_J_030_quiet_capture_validated": True,
        "reduced_history_factorization_validated": True,
        "candidate_pulse_bracket": ["0.30113", "0.30114"],
        "candidate_bracket_is_directed_separator_enclosure": False,
        "physical_pulse_crossing_validated": False,
        "two_sided_routing_validated": False,
        "unique_onset_validated": False,
    }


def build_outer_two_sided_routing_contract(repository: Path) -> dict[str, Any]:
    parents = {
        relative: _load_parent(repository, relative)
        for relative in PARENT_RESULT_SHA256
    }
    evidence = _parent_evidence(parents)
    local_field = _outer_local_field_evidence(parents[DOBRUSHIN_STRIP_RESULT])
    target = _outer_attachment_target(parents[OUTER_ORBIT_RESULT], repository)

    outer_orbit = _mapping(
        parents[OUTER_ORBIT_RESULT].get("artifact"), "outer orbit"
    )
    directed = _mapping(
        outer_orbit.get("directed_radii_certificate"), "outer radii certificate"
    )
    validation = _mapping(directed.get("validation"), "outer validation")
    correction = _mapping(validation.get("correction"), "outer correction")
    orbit_correction = correction.get("chosen_radius")
    if not isinstance(orbit_correction, str):
        raise ValueError("the exact outer correction radius is missing")

    stage1 = _mapping(
        parents[INNER_STAGE1_RESULT].get("contract"), "inner Stage 1"
    )
    stage1_evidence = _mapping(
        stage1.get("proved_parent_evidence"), "inner Stage 1 evidence"
    )

    outer_actual = OuterAttractingTubeInputBudget(
        outer_zero_index_validated=False,
        neutral_multiplier_algebraically_simple_validated=True,
        reduced_phase_section_and_return_map_validated=False,
        stable_spectral_radius_upper=None,
        stable_power_constant_upper=None,
        stable_riesz_projection_norm_upper=None,
        phase_chart_projection_norm_upper=None,
        return_iterate_count=None,
        m_return_nonlinear_derivative_coefficient_upper=None,
        chosen_section_radius=None,
        validated_return_map_domain_radius_lower=None,
        interreturn_flow_lipschitz_upper=None,
        interreturn_flow_tube_validated=False,
        evidence_status="actual_parents_incomplete",
    )

    signed_actual = SignedInnerExitInputBudget(
        quantitative_inner_stable_graph_validated=False,
        graph_straightened_return_map_cylinder_validated=False,
        unstable_multiplier_modulus_lower=stage1_evidence[
            "unstable_multiplier_modulus_lower"
        ],
        unstable_multiplier_modulus_upper=stage1_evidence[
            "unstable_multiplier_modulus_upper"
        ],
        signed_gap_factor_deviation_upper=None,
        stable_row_contraction_upper=None,
        stable_row_gap_coupling_upper=None,
        stable_coordinate_radius=None,
        signed_exit_gap=None,
        validated_coordinate_gap_radius_lower=None,
        evidence_status="actual_parents_incomplete",
    )

    quiet_certificate = _mapping(
        parents[QUIET_CAPTURE_RESULT].get("certificate"), "quiet capture"
    )
    quiet_anchor = QuietAttachmentInputBudget(
        initial_set_is_complete_signed_inner_exit_face=False,
        directed_method_of_steps_family_tube_validated=True,
        complete_retained_history_bernstein_bound_validated=True,
        retained_guide_lyapunov_upper=quiet_certificate[
            "maximum_retained_guide_lyapunov_upper"
        ],
        retained_p_norm_error_upper=quiet_certificate[
            "maximum_retained_p_error_radius_upper"
        ],
        quiet_p_norm_threshold_lower=quiet_certificate[
            "quiet_basin_p_norm_threshold_lower"
        ],
        evidence_status="proved_single_history_J_3_over_10_anchor",
    )
    quiet_exit_face = QuietAttachmentInputBudget(
        initial_set_is_complete_signed_inner_exit_face=False,
        directed_method_of_steps_family_tube_validated=False,
        complete_retained_history_bernstein_bound_validated=False,
        retained_guide_lyapunov_upper=None,
        retained_p_norm_error_upper=None,
        quiet_p_norm_threshold_lower=quiet_certificate[
            "quiet_basin_p_norm_threshold_lower"
        ],
        evidence_status="actual_quiet_exit_face_family_missing",
    )

    outer_attachment_actual = OuterAttachmentInputBudget(
        initial_set_is_complete_signed_inner_exit_face=False,
        directed_method_of_steps_family_tube_validated=False,
        continuous_history_bernstein_distance_validated=False,
        outer_section_event_bracket_validated=False,
        outer_section_event_speed_lower=None,
        continuous_guide_to_candidate_orbit_upper=None,
        method_of_steps_history_error_upper=None,
        exact_outer_orbit_correction_upper=orbit_correction,
        event_time_error_upper=None,
        history_speed_upper_on_event_tube=None,
        section_reference_and_phase_error_upper=None,
        section_chart_projection_norm_upper=None,
        outer_section_ball_radius_lower=None,
        outer_attracting_tube_validated=False,
        evidence_status="actual_outer_exit_face_and_tube_missing",
    )
    outer_attachment_requested = OuterAttachmentInputBudget(
        initial_set_is_complete_signed_inner_exit_face=False,
        directed_method_of_steps_family_tube_validated=False,
        continuous_history_bernstein_distance_validated=False,
        outer_section_event_bracket_validated=False,
        outer_section_event_speed_lower="0.5",
        continuous_guide_to_candidate_orbit_upper="0.00001",
        method_of_steps_history_error_upper="0.000005",
        exact_outer_orbit_correction_upper=orbit_correction,
        event_time_error_upper="0.000001",
        history_speed_upper_on_event_tube="3",
        section_reference_and_phase_error_upper="0.000005",
        section_chart_projection_norm_upper="2",
        outer_section_ball_radius_lower="0.0001",
        outer_attracting_tube_validated=False,
        evidence_status="requested_directed_budget_not_evidence",
    )

    claims = {name: True for name in TRUE_CLAIMS}
    claims.update({name: False for name in FALSE_CLAIMS})

    return {
        "schema_id": SCHEMA_ID,
        "model_id": MODEL_ID,
        "phase_spaces": {
            "full": "X=C([-5*sqrt(5),0],R^2)",
            "reduced": "Y=C([-5*sqrt(5),0],R)xR",
            "full_norm": "max{sup|phi_v|,sup|phi_w|}",
            "reduced_norm": "max{sup|phi_v|,|omega|}",
            "projection": "pi(phi_v,phi_w)=(phi_v,phi_w(0)), ||pi||=1",
            "factorization": "Phi_t=iota*Psi_t*pi for t>=5*sqrt(5)",
        },
        "parent_evidence": evidence,
        "outer_local_vector_field_evidence": local_field,
        "outer_attracting_tube_actual_budget": asdict(outer_actual),
        "outer_attracting_tube_actual_evaluation": asdict(
            evaluate_outer_attracting_tube(outer_actual)
        ),
        "signed_inner_exit_actual_budget": asdict(signed_actual),
        "signed_inner_exit_actual_evaluation": asdict(
            evaluate_signed_inner_exit(signed_actual)
        ),
        "quiet_J_030_anchor_budget": asdict(quiet_anchor),
        "quiet_J_030_anchor_evaluation": asdict(
            evaluate_quiet_attachment(quiet_anchor)
        ),
        "quiet_exit_face_actual_budget": asdict(quiet_exit_face),
        "quiet_exit_face_actual_evaluation": asdict(
            evaluate_quiet_attachment(quiet_exit_face)
        ),
        "pulse_J_032_outer_attachment_target": target,
        "outer_attachment_actual_budget": asdict(outer_attachment_actual),
        "outer_attachment_actual_evaluation": asdict(
            evaluate_outer_attachment(outer_attachment_actual)
        ),
        "outer_attachment_requested_budget_not_evidence": asdict(
            outer_attachment_requested
        ),
        "outer_attachment_requested_evaluation_not_evidence": asdict(
            evaluate_outer_attachment(outer_attachment_requested)
        ),
        "method_of_steps_family_contract": {
            "initial_object": (
                "each complete bounded signed exit slab, not a sampled orbit and not a "
                "terminal point"
            ),
            "causal_cell_error_inequality": (
                "D+R_i<=mu_i R_i+b_i0 R_delay0+b_i1 R_delay1+E_residual_i"
            ),
            "uniform_family_requirement": (
                "time and every exit-face parameter are enclosed on each cell; "
                "power-polynomial residuals and terminal targets use outward "
                "tensor Bernstein convex-hull bounds; any finite head carries "
                "a rigorous function-space tail radius obtained directly or "
                "after a proved smoothing step"
            ),
            "quiet_terminal_test": (
                "sqrt(B_P)+E_P<1/sqrt(125) over every cell in the complete "
                "retained history"
            ),
            "outer_terminal_test": (
                "opposite event signs plus positive section speed, followed by "
                "Q_section*(E_guide+E_flow+E_orbit+E_time F+E_section)<r_outer"
            ),
            "point_samples_are_basin_evidence": False,
        },
        "proof_spine": (
            "quantitative inner graph and exact pulse crossing -> signed factor "
            "expands each nonzero gap to one complete bounded exit slab -> directed "
            "method of steps attaches the negative slab to the quiet sublevel "
            "and the positive slab to a proved outer section contraction ball -> "
            "the crossing is the unique local biological onset"
        ),
        "smallest_missing_artifacts": [
            "outer compact-keyhole zero count and a stable history resolvent/power bound",
            "outer phase-section return tube and m-return nonlinear derivative bound",
            "inner Riesz covector, quantitative stable graph, and graph-straightened cylinder",
            "directed pulse-gap endpoint signs and uniform derivative on [0.30113,0.30114]",
            "two tensor-Bernstein method-of-steps families starting from the complete exit slabs",
        ],
        "claim_status": claims,
    }


def build_outer_two_sided_routing_result(repository: Path) -> dict[str, Any]:
    contract = build_outer_two_sided_routing_contract(repository)
    return {
        "contract": contract,
        "manifest": {
            "schema_id": SCHEMA_ID,
            "result": RESULT_RELATIVE_PATH,
            "default_command": DEFAULT_COMMAND,
            "arithmetic_scope": ARITHMETIC_SCOPE,
            "contract_sha256": canonical_sha256(contract),
            "parent_result_sha256": dict(PARENT_RESULT_SHA256),
            "source_sha256": {
                relative: _sha256_path(repository / relative)
                for relative in SOURCE_MANIFEST
            },
        },
    }


def validate_outer_two_sided_routing_contract_body(
    contract: Mapping[str, Any],
) -> None:
    expected_keys = {
        "schema_id",
        "model_id",
        "phase_spaces",
        "parent_evidence",
        "outer_local_vector_field_evidence",
        "outer_attracting_tube_actual_budget",
        "outer_attracting_tube_actual_evaluation",
        "signed_inner_exit_actual_budget",
        "signed_inner_exit_actual_evaluation",
        "quiet_J_030_anchor_budget",
        "quiet_J_030_anchor_evaluation",
        "quiet_exit_face_actual_budget",
        "quiet_exit_face_actual_evaluation",
        "pulse_J_032_outer_attachment_target",
        "outer_attachment_actual_budget",
        "outer_attachment_actual_evaluation",
        "outer_attachment_requested_budget_not_evidence",
        "outer_attachment_requested_evaluation_not_evidence",
        "method_of_steps_family_contract",
        "proof_spine",
        "smallest_missing_artifacts",
        "claim_status",
    }
    if not isinstance(contract, Mapping) or set(contract) != expected_keys:
        raise ValueError("outer routing contract schema changed")
    if contract.get("schema_id") != SCHEMA_ID or contract.get("model_id") != MODEL_ID:
        raise ValueError("outer routing contract identity changed")
    claims = _mapping(contract.get("claim_status"), "routing claims")
    if set(claims) != {*TRUE_CLAIMS, *FALSE_CLAIMS}:
        raise ValueError("outer routing claim ledger changed")
    if any(claims.get(name) is not True for name in TRUE_CLAIMS):
        raise ValueError("a proved routing input was weakened")
    if any(claims.get(name) is not False for name in FALSE_CLAIMS):
        raise ValueError("an open routing or onset claim was promoted")
    target = _mapping(
        contract.get("pulse_J_032_outer_attachment_target"), "outer target"
    )
    if target.get("continuous_history_distance_validated") is not False:
        raise ValueError("the sampled outer target was promoted to a history bound")
    if target.get("outer_basin_capture_validated") is not False:
        raise ValueError("the sampled outer target was promoted to capture")
    outer_actual = _mapping(
        contract.get("outer_attracting_tube_actual_evaluation"),
        "outer tube evaluation",
    )
    signed_actual = _mapping(
        contract.get("signed_inner_exit_actual_evaluation"),
        "signed exit evaluation",
    )
    quiet_exit = _mapping(
        contract.get("quiet_exit_face_actual_evaluation"),
        "quiet attachment evaluation",
    )
    outer_exit = _mapping(
        contract.get("outer_attachment_actual_evaluation"),
        "outer attachment evaluation",
    )
    if outer_actual.get("outer_attracting_tube_closes") is not False:
        raise ValueError("the actual outer tube was promoted")
    if signed_actual.get("signed_exit_closes") is not False:
        raise ValueError("the actual signed exit was promoted")
    if quiet_exit.get("quiet_exit_face_attachment_closes") is not False:
        raise ValueError("the actual quiet exit face was promoted")
    if outer_exit.get("outer_exit_face_attachment_closes") is not False:
        raise ValueError("the actual outer exit face was promoted")


def validate_outer_two_sided_routing_result(
    payload: Mapping[str, Any], repository: Path
) -> None:
    if not isinstance(payload, Mapping) or set(payload) != {"contract", "manifest"}:
        raise ValueError("outer routing result has the wrong outer schema")
    contract = _mapping(payload.get("contract"), "outer routing contract")
    manifest = _mapping(payload.get("manifest"), "outer routing manifest")
    validate_outer_two_sided_routing_contract_body(contract)
    expected = _json_normalize(build_outer_two_sided_routing_contract(repository))
    if _json_normalize(contract) != expected:
        raise ValueError("outer routing contract differs from source replay")
    expected_manifest_keys = {
        "schema_id",
        "result",
        "default_command",
        "arithmetic_scope",
        "contract_sha256",
        "parent_result_sha256",
        "source_sha256",
    }
    if set(manifest) != expected_manifest_keys:
        raise ValueError("outer routing manifest schema changed")
    if manifest.get("schema_id") != SCHEMA_ID:
        raise ValueError("outer routing manifest identity changed")
    if manifest.get("result") != RESULT_RELATIVE_PATH:
        raise ValueError("outer routing result path changed")
    if manifest.get("default_command") != DEFAULT_COMMAND:
        raise ValueError("outer routing default command changed")
    if manifest.get("arithmetic_scope") != ARITHMETIC_SCOPE:
        raise ValueError("outer routing arithmetic scope changed")
    if manifest.get("contract_sha256") != canonical_sha256(contract):
        raise ValueError("outer routing contract digest changed")
    if manifest.get("parent_result_sha256") != PARENT_RESULT_SHA256:
        raise ValueError("outer routing parent digest map changed")
    for relative, digest in PARENT_RESULT_SHA256.items():
        if _sha256_path(repository / relative) != digest:
            raise ValueError(f"a bound routing parent changed: {relative}")
    sources = _mapping(manifest.get("source_sha256"), "routing source hashes")
    if set(sources) != set(SOURCE_MANIFEST):
        raise ValueError("outer routing source manifest changed")
    for relative in SOURCE_MANIFEST:
        if sources.get(relative) != _sha256_path(repository / relative):
            raise ValueError(f"outer routing source changed: {relative}")


__all__ = [
    "DEFAULT_COMMAND",
    "NOTE_RELATIVE_PATH",
    "OuterAttachmentInputBudget",
    "OuterAttractingTubeInputBudget",
    "PARENT_RESULT_SHA256",
    "QuietAttachmentInputBudget",
    "RESULT_RELATIVE_PATH",
    "SCHEMA_ID",
    "SignedInnerExitInputBudget",
    "build_outer_two_sided_routing_contract",
    "build_outer_two_sided_routing_result",
    "evaluate_outer_attachment",
    "evaluate_outer_attracting_tube",
    "evaluate_quiet_attachment",
    "evaluate_signed_inner_exit",
    "validate_outer_two_sided_routing_contract_body",
    "validate_outer_two_sided_routing_result",
]
