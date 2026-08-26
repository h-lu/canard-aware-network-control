"""Stage-4S-B bridge from a finite Hessian tensor to Banach history blocks.

This module is deliberately fail closed.  It proves several pieces of the
error architecture around the Stage-4Q finite-section pilot, but it does not
turn any Stage-4Q number into a continuous-history Hessian bound.

The decisive negative fact is elementary and unavoidable.  Point sampling on
an arbitrary unit ball of ``C([-tau,0])`` cannot converge to the identity in
operator norm.  Consequently, mesh refinement of a nodal Hessian tensor is
not by itself an error estimate for the Banach-space return Hessian.  A valid
bridge must instead lift a *directed* coefficient tensor to an atomic
bimeasure and bound the signed atom--density residual in physical history
coordinates, or change to a uniformly equicontinuous history domain.

What is proved here:

* the finite-sampling operator-norm no-go lemma;
* the atomic-bimeasure lift and its row-total-variation norm bound;
* exact Lebesgue and Lipschitz constants for the two cubic stencils used by
  Stage 4Q;
* exact projection-amplification factors for a raw Hessian remainder under
  the frozen continuous-history ``q_hat/f_hat`` splitting;
* exact per-block allocation arithmetic inside the Stage-4P wide box; and
* a complete null ingress ledger for the interval quantities still needed.

No binary Stage-4Q row is treated as outward rounded.  No common event tube,
continuous signed kernel residual, full-ball inflation, Hessian block, stable
graph, crossing, onset, routing, capture, or network-safety claim is made.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR, localcontext
from hashlib import sha256
import json
from pathlib import Path
import platform
from typing import Any, Mapping


SCHEMA_ID = "leaky-inner-stage4s-hessian-bridge-v1"
MODEL_ID = "autonomous-leaky-recovery-two-delay-fhn-bistable-proposal"
BRANCH = "inner_saddle_candidate_selected_near_two_period_event"
STATUS = "PROVED_BRIDGE_DESIGN_AND_SAMPLING_NO_GO; NO_BANACH_HESSIAN_BOUND"

SOURCE_RELATIVE_PATH = (
    "src/canard_control/leaky_inner_stage4s_hessian_bridge.py"
)
GENERATOR_RELATIVE_PATH = (
    "experiments/leaky_inner_stage4s_hessian_bridge.py"
)
RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_inner_stage4s_hessian_bridge.json"
)
NOTE_RELATIVE_PATH = "docs/leaky_inner_stage4s_hessian_bridge.md"
TEST_RELATIVE_PATH = "tests/test_leaky_inner_stage4s_hessian_bridge.py"

SOURCE_MANIFEST = (
    SOURCE_RELATIVE_PATH,
    GENERATOR_RELATIVE_PATH,
    NOTE_RELATIVE_PATH,
    TEST_RELATIVE_PATH,
)

STAGE4D_RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_route_c_adjoint_stage4d.json"
)
STAGE4L_RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_inner_terminal_stable_row_stage4l.json"
)
STAGE4O_RESULT_RELATIVE_PATH = (
    "experiments/results/"
    "leaky_inner_event_aligned_return_hessian_stage4o_contract.json"
)
STAGE4P_RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_inner_graph_closure_arithmetic_stage4p.json"
)
STAGE4Q_RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_inner_signed_second_variation_stage4q_pilot.json"
)

PARENT_RESULT_SHA256 = {
    STAGE4D_RESULT_RELATIVE_PATH: (
        "af51bcfc20000b804134c1d8b9cacc303013676c440a89f2ecb52faf0042d568"
    ),
    STAGE4L_RESULT_RELATIVE_PATH: (
        "672f92c7c456a54f39afab7d2a5f92b783311cc0ee5341a4d2e72a588039017e"
    ),
    STAGE4O_RESULT_RELATIVE_PATH: (
        "dc0e3951cb529dbdca384ff548ab0d7cd7786fe02573741e80e9c945452b2a23"
    ),
    STAGE4P_RESULT_RELATIVE_PATH: (
        "860a51d51648919f74bd7bd4e8230a629f7864b2bdcccf490aab5ff9e8e6b542"
    ),
    STAGE4Q_RESULT_RELATIVE_PATH: (
        "e4481bca2d021517073216dab15ee91c43cf301822b15e337c1b5061e9aaf49a"
    ),
}

DEFAULT_COMMAND = (
    "PYTHONPATH=src /usr/bin/python3 "
    "experiments/leaky_inner_stage4s_hessian_bridge.py"
)
ARITHMETIC_SCOPE = (
    "exact Decimal/Fraction-equivalent wide-box allocation arithmetic; exact "
    "finite-sampling no-go and atomic-bimeasure lift; symbolic cubic-stencil "
    "Lebesgue/Lipschitz constants; exact projection perturbation factors from "
    "the frozen Stage-4L continuous-history norm; byte and source-manifest "
    "binding of Stages 4D, 4L, 4O, 4P and 4Q; no outward enclosure of the "
    "Stage-4Q tensor and no continuous-history or full-ball Hessian claim"
)

BLOCK_NAMES = (
    "stable_output_ss_upper",
    "stable_output_su_upper",
    "stable_output_uu_upper",
    "unstable_output_ss_upper",
    "unstable_output_su_upper",
    "unstable_output_uu_upper",
)

# These are independent acceptance targets, not enclosures of the Stage-4Q
# pilot.  Their only role is to reserve explicit room inside the Stage-4P box.
CORE_TARGETS = {
    "stable_output_ss_upper": Decimal("0.0001"),
    "stable_output_su_upper": Decimal("0.02"),
    "stable_output_uu_upper": Decimal("40"),
    "unstable_output_ss_upper": Decimal("0.75"),
    "unstable_output_su_upper": Decimal("0.75"),
    "unstable_output_uu_upper": Decimal("180"),
}

ERROR_FRACTIONS = {
    "base_orbit_and_coefficient_error": Decimal("0.10"),
    "first_variation_kernel_residual": Decimal("0.15"),
    "second_variation_kernel_residual": Decimal("0.20"),
    "event_quotient_and_history_translation": Decimal("0.15"),
    "continuous_qf_and_output_phase_completion": Decimal("0.10"),
    "full_ball_inflation_and_return_domain": Decimal("0.20"),
}
RESERVE_FRACTION = Decimal("0.10")

TRUE_FLAGS = (
    "all_five_parent_results_byte_and_source_manifest_bound",
    "stage4q_all_theorem_flags_false_audited",
    "finite_sampling_operator_norm_no_go_proved",
    "finite_atomic_bimeasure_lift_lemma_proved",
    "piecewise_linear_output_lift_norm_one_proved",
    "interior_cubic_stencil_stability_constant_proved",
    "one_sided_endpoint_stencil_stability_constant_proved",
    "common_modulus_and_lipschitz_error_formulas_proved",
    "continuous_history_projection_amplification_factors_proved",
    "six_block_wide_box_budget_arithmetic_proved",
    "required_interval_quantity_ledger_registered",
    "direct_projected_residual_route_identified_as_preferred",
)

FALSE_FLAGS = (
    "stage4q_binary_tensor_outward_rounded",
    "stage4q_mesh_sequence_converges_in_operator_norm_on_arbitrary_C_ball",
    "stage4q_finite_qf_adapter_equals_continuous_grushin_pair",
    "directed_finite_atomic_tensor_coefficients_enclosed",
    "directed_base_orbit_and_coefficient_tube_validated",
    "directed_first_variation_signed_kernel_residual_validated",
    "directed_second_variation_signed_bimeasure_residual_validated",
    "common_full_ball_two_return_event_window_validated",
    "uniform_positive_event_speed_validated",
    "complete_output_phase_and_history_seams_validated",
    "continuous_qf_action_on_all_six_kernels_validated",
    "full_ball_hessian_inflation_validated",
    "all_six_complete_history_hessian_blocks_validated",
    "stage4p_wide_box_entered_into_strict_numeric_ingress",
    "quantitative_inner_stable_graph_validated",
    "selected_pulse_stable_sheet_crossing_validated",
    "unique_physical_pulse_onset_validated",
    "two_sided_basin_routing_validated",
    "biological_capture_validated",
    "asynchronous_network_safety_validated",
)


@dataclass(frozen=True)
class Stage4SHessianBridge:
    schema_id: str
    model_id: str
    branch: str
    status: str
    parent_result_sha256: dict[str, str]
    finite_section_audit: dict[str, Any]
    finite_sampling_no_go: dict[str, Any]
    atomic_bimeasure_lift: dict[str, Any]
    cubic_stencil_certificates: dict[str, Any]
    continuous_projection_stability: dict[str, Any]
    wide_box_error_budget: dict[str, Any]
    required_interval_quantities: dict[str, Any]
    strict_numeric_ingress: dict[str, Any]
    failure_gates: dict[str, Any]
    theorem_boundary: dict[str, Any]
    claim_status: dict[str, bool]


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


def _mapping(value: Any, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{name} is missing")
    return value


def _decimal_text(value: Decimal) -> str:
    if value == value.to_integral():
        return str(value.quantize(Decimal(1)))
    return format(value.normalize(), "f")


def _directed_decimal_bracket(value: Decimal, places: int = 70) -> dict[str, str]:
    quantum = Decimal(1).scaleb(-places)
    lower = value.quantize(quantum, rounding=ROUND_FLOOR)
    upper = value.quantize(quantum, rounding=ROUND_CEILING)
    if lower == upper:
        lower -= quantum
        upper += quantum
    return {
        "lower": format(lower, "f"),
        "upper": format(upper, "f"),
    }


def _load_parent(
    repository: Path, relative: str, expected_digest: str
) -> Mapping[str, Any]:
    path = repository / relative
    raw = path.read_bytes()
    if sha256(raw).hexdigest() != expected_digest:
        raise ValueError(f"the Stage-4S-B parent changed: {relative}")
    payload = json.loads(raw)
    if not isinstance(payload, Mapping):
        raise ValueError(f"the Stage-4S-B parent is malformed: {relative}")
    manifest = _mapping(payload.get("manifest"), f"manifest of {relative}")
    source_hashes = _mapping(
        manifest.get("source_sha256"), f"source manifest of {relative}"
    )
    for source_relative, source_digest in source_hashes.items():
        if _sha256_path(repository / str(source_relative)) != source_digest:
            raise ValueError(
                f"a source bound by the Stage-4S-B parent changed: {source_relative}"
            )
    return payload


def _load_parents(repository: Path) -> dict[str, Mapping[str, Any]]:
    parents = {
        relative: _load_parent(repository, relative, digest)
        for relative, digest in PARENT_RESULT_SHA256.items()
    }

    stage4d = _mapping(
        parents[STAGE4D_RESULT_RELATIVE_PATH].get("artifact"), "Stage-4D artifact"
    )
    measure = _mapping(
        stage4d.get("continuous_history_measure_enclosure"),
        "Stage-4D continuous measure",
    )
    tail = _mapping(
        stage4d.get("summable_adjoint_tail_certificate"), "Stage-4D tail"
    )
    if (
        measure.get("continuous_atom_density_measure_numeric_enclosed") is not True
        or tail.get("tail_summability_validated") is not True
    ):
        raise ValueError("the continuous Stage-4D q/f ingress changed")

    stage4l = _mapping(
        parents[STAGE4L_RESULT_RELATIVE_PATH].get("artifact"), "Stage-4L artifact"
    )
    if stage4l.get("claim_status", {}).get(
        "phase_fixed_selected_stable_map_norm_at_most_0p1_validated"
    ) is not True:
        raise ValueError("the Stage-4L continuous splitting ingress changed")

    stage4o = _mapping(
        parents[STAGE4O_RESULT_RELATIVE_PATH].get("contract"), "Stage-4O contract"
    )
    claims_o = _mapping(stage4o.get("claim_status"), "Stage-4O claims")
    if (
        claims_o.get("exact_implicit_event_Tx_Txx_registered") is not True
        or claims_o.get("moving_event_phase_projection_applied_exactly_once_registered")
        is not True
        or claims_o.get("all_six_projected_return_hessian_blocks_validated")
        is not False
    ):
        raise ValueError("the Stage-4O Hessian boundary changed")

    stage4p = _mapping(
        parents[STAGE4P_RESULT_RELATIVE_PATH].get("design"), "Stage-4P design"
    )
    claims_p = _mapping(stage4p.get("claim_status"), "Stage-4P claims")
    if (
        claims_p.get("wide_box_conditional_unique_crossing_arithmetic_closes")
        is not True
        or claims_p.get("two_return_six_projected_hessian_blocks_validated")
        is not False
    ):
        raise ValueError("the Stage-4P wide-box boundary changed")

    stage4q = _mapping(
        parents[STAGE4Q_RESULT_RELATIVE_PATH].get("pilot"), "Stage-4Q pilot"
    )
    claims_q = _mapping(stage4q.get("claim_status"), "Stage-4Q claims")
    if len(claims_q) != 19 or any(value is not False for value in claims_q.values()):
        raise ValueError("a Stage-4Q diagnostic flag was promoted")
    if stage4q.get("status") != "DIAGNOSTIC_NONRIGOROUS_SOURCE_BOUND":
        raise ValueError("the Stage-4Q status changed")
    return parents


def _stage4p_caps(parent: Mapping[str, Any]) -> dict[str, Decimal]:
    design = _mapping(parent.get("design"), "Stage-4P design")
    two = _mapping(design.get("two_return_design"), "Stage-4P two-return design")
    wide = _mapping(
        two.get("recommended_wide_proof_box"), "Stage-4P recommended wide box"
    )
    blocks = _mapping(wide.get("blocks"), "Stage-4P wide blocks")
    result = {str(name): Decimal(str(value)) for name, value in blocks.items()}
    if set(result) != set(BLOCK_NAMES):
        raise ValueError("the Stage-4P block set changed")
    if (
        wide.get("blocks_are_source_bound_continuous_history_bounds") is not False
        or wide.get("entered_into_strict_numeric_ingress") is not False
    ):
        raise ValueError("the Stage-4P target box was promoted")
    return result


def _stage4q_envelope(parent: Mapping[str, Any]) -> dict[str, Decimal]:
    pilot = _mapping(parent.get("pilot"), "Stage-4Q pilot")
    refinement = _mapping(
        pilot.get("refinement_and_acceptance"), "Stage-4Q refinement"
    )
    if refinement.get("any_diagnostic_test_is_a_theorem") is not False:
        raise ValueError("the Stage-4Q envelope was promoted")
    envelope = _mapping(
        refinement.get("two_period_projected_block_heuristic_envelope"),
        "Stage-4Q heuristic envelope",
    )
    result = {str(name): Decimal(str(value)) for name, value in envelope.items()}
    if set(result) != set(BLOCK_NAMES):
        raise ValueError("the Stage-4Q block set changed")
    return result


def _stage4l_f_norm_upper(parent: Mapping[str, Any]) -> Decimal:
    artifact = _mapping(parent.get("artifact"), "Stage-4L artifact")
    ledger = _mapping(
        artifact.get("directed_error_ledger"), "Stage-4L error ledger"
    )
    value = Decimal(str(ledger["exact_normalized_restricted_f_norm_upper"]))
    if value <= 0:
        raise ValueError("the Stage-4L f norm is not positive")
    return value


def _projection_factors(f_norm: Decimal) -> dict[str, Decimal]:
    p_norm = Decimal(1) + f_norm
    return {
        "stable_output_ss_upper": p_norm**3,
        "stable_output_su_upper": p_norm**2,
        "stable_output_uu_upper": p_norm,
        "unstable_output_ss_upper": f_norm * p_norm**2,
        "unstable_output_su_upper": f_norm * p_norm,
        "unstable_output_uu_upper": f_norm,
    }


def _budget_rows(
    caps: Mapping[str, Decimal],
    diagnostic: Mapping[str, Decimal],
    factors: Mapping[str, Decimal],
) -> dict[str, Any]:
    rows: dict[str, Any] = {}
    raw_ceilings: list[Decimal] = []
    used_fraction = sum(ERROR_FRACTIONS.values(), Decimal(0))
    if used_fraction + RESERVE_FRACTION != 1:
        raise ArithmeticError("the Stage-4S-B allocation fractions do not sum to one")
    for name in BLOCK_NAMES:
        cap = caps[name]
        core = CORE_TARGETS[name]
        pilot = diagnostic[name]
        if not Decimal(0) <= pilot < core < cap:
            raise ArithmeticError(f"the Stage-4S-B target ordering failed for {name}")
        residual = cap - core
        allocations = {
            category: residual * fraction
            for category, fraction in ERROR_FRACTIONS.items()
        }
        reserve = residual * RESERVE_FRACTION
        used_error = sum(allocations.values(), Decimal(0))
        if core + used_error + reserve != cap:
            raise ArithmeticError(f"the Stage-4S-B budget does not add up for {name}")
        raw_ceiling = used_error / factors[name]
        raw_ceilings.append(raw_ceiling)
        rows[name] = {
            "stage4p_wide_cap": _decimal_text(cap),
            "stage4q_heuristic_envelope_diagnostic_only": _decimal_text(pilot),
            "independent_directed_banach_core_target": _decimal_text(core),
            "pilot_to_core_target_ratio_diagnostic_only": _decimal_text(
                pilot / core
            ),
            "residual_after_core_target": _decimal_text(residual),
            "projected_error_allowances": {
                category: _decimal_text(value)
                for category, value in allocations.items()
            },
            "strict_unused_reserve": _decimal_text(reserve),
            "sum_identity": (
                "core_target + six projected error allowances + reserve = wide_cap"
            ),
            "raw_hessian_remainder_amplification_factor": _decimal_text(
                factors[name]
            ),
            "raw_hessian_only_error_ceiling_if_it_consumes_all_six_allowances": (
                _decimal_text(raw_ceiling)
            ),
            "actual_directed_core_bound": None,
            "actual_projected_error_contributions": {
                category: None for category in ERROR_FRACTIONS
            },
            "strict_block_acceptance_validated": False,
        }
    return {
        "budget_role": (
            "future acceptance design only; the Stage-4Q heuristic column is not "
            "an ingress value and cannot satisfy the directed core target"
        ),
        "error_allowance_fraction_sum": _decimal_text(used_fraction),
        "reserve_fraction": _decimal_text(RESERVE_FRACTION),
        "blocks": rows,
        "simultaneous_raw_hessian_only_error_ceiling": _decimal_text(
            min(raw_ceilings)
        ),
        "direct_projected_route_preferred": True,
        "reason_direct_projected_route_preferred": (
            "a raw ambient remainder is multiplied by up to ||P_s||^3; retaining "
            "the q/f correlations and enclosing each projected bimeasure directly "
            "uses the much larger blockwise allowances without this loss"
        ),
        "all_six_strict_acceptance_tests_validated": False,
    }


def _required_interval_quantities() -> dict[str, Any]:
    groups = {
        "A_full_ball_domain_and_selected_event": (
            "common_solution_tube_through_T2_plus",
            "T2_minus_strictly_greater_than_2_tau_max",
            "strict_event_endpoint_signs",
            "uniform_event_speed_lower_a_star",
            "returned_split_ball_and_graph_domain_containment",
        ),
        "B_base_orbit_and_field_jets": (
            "base_history_tube_all_source_and_output_times",
            "dot_X_and_ddot_X_complete_history_rows",
            "D1F_current_and_every_delay_slot",
            "D2F_current_and_every_delay_slot",
            "D3F_full_ball_perturbation_bound",
            "delay_activation_faces_and_short_cells",
        ),
        "C_first_variation_signed_measures": (
            "initial_translation_atoms_at_physical_history_points",
            "stable_input_rows_every_source_time_and_delay_slot",
            "qhat_input_rows_every_source_time_and_delay_slot",
            "measure_residual_integrals_and_initial_trace_error",
            "time_cell_and_delay_seam_jumps",
        ),
        "D_second_variation_signed_bimeasures": (
            "ss_su_uu_quadratic_source_bimeasures",
            "retarded_terminal_response_all_output_phases",
            "bimeasure_residual_integrals",
            "bilinear_symmetry_and_all_history_seams",
            "outward_rounding_and_quadrature_remainders",
        ),
        "E_event_quotient_and_translation": (
            "common_positive_denominator_and_inverse_powers_through_a_minus_3",
            "n_s_n_u_dot_U_and_ddot_X_correlated_rows",
            "T_h_T_k_T_hk_same_denominator_enclosures",
            "complete_theta_translation_before_one_phase_projection",
            "event_identity_and_section_tangency_residuals",
        ),
        "F_continuous_qf_and_output_completion": (
            "exact_qhat_complete_history_enclosure_and_normalization",
            "exact_fhat_atom_density_measure_and_tail",
            "fhat_qhat_pairing_error",
            "qf_action_on_each_correlated_output_bimeasure",
            "output_phase_lipschitz_or_Bernstein_supremum_bound",
            "left_endpoint_and_theta_zero_section_rows",
        ),
        "G_full_ball_inflation": (
            "center_to_ball_coefficient_change",
            "center_to_ball_first_kernel_change",
            "center_to_ball_second_kernel_change",
            "event_time_and_denominator_change",
            "uniform_projected_block_remainder_on_split_ball",
        ),
    }
    return {
        name: {
            "purpose": "required outward interval ingress",
            "values": {field: None for field in fields_},
            "validated": False,
        }
        for name, fields_ in groups.items()
    }


def _strict_numeric_ingress() -> dict[str, Any]:
    return {
        "evidence_status": "OPEN_FAIL_CLOSED_AFTER_EXACT_BRIDGE_AUDIT",
        "directed_finite_atomic_tensor_coefficients": None,
        "continuous_signed_kernel_residual_norms": {
            name: None for name in BLOCK_NAMES
        },
        "directed_banach_core_blocks": {name: None for name in BLOCK_NAMES},
        "projected_error_contributions": {
            category: {name: None for name in BLOCK_NAMES}
            for category in ERROR_FRACTIONS
        },
        "uniform_full_ball_hessian_blocks": {name: None for name in BLOCK_NAMES},
        "all_source_time_cells_and_delay_seams_covered": False,
        "all_output_phase_cells_and_endpoints_covered": False,
        "all_six_blocks_from_one_correlated_run": False,
        "all_six_strict_budget_tests_pass": False,
    }


def _arithmetic_core(bridge: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "finite_sampling_no_go": bridge["finite_sampling_no_go"],
        "atomic_bimeasure_lift": bridge["atomic_bimeasure_lift"],
        "cubic_stencil_certificates": bridge["cubic_stencil_certificates"],
        "continuous_projection_stability": bridge[
            "continuous_projection_stability"
        ],
        "wide_box_error_budget": bridge["wide_box_error_budget"],
        "required_interval_quantities": bridge["required_interval_quantities"],
    }


def _build_stage4s_hessian_bridge_in_context(
    repository: Path,
) -> Stage4SHessianBridge:
    repository = repository.resolve()
    parents = _load_parents(repository)
    caps = _stage4p_caps(parents[STAGE4P_RESULT_RELATIVE_PATH])
    diagnostic = _stage4q_envelope(parents[STAGE4Q_RESULT_RELATIVE_PATH])
    f_norm = _stage4l_f_norm_upper(parents[STAGE4L_RESULT_RELATIVE_PATH])
    factors = _projection_factors(f_norm)

    sqrt_7 = Decimal(7).sqrt()
    endpoint_lebesgue = (Decimal(7) + Decimal(14) * sqrt_7) / Decimal(27)
    claims = {name: True for name in TRUE_FLAGS}
    claims.update({name: False for name in FALSE_FLAGS})

    stage4d_artifact = _mapping(
        parents[STAGE4D_RESULT_RELATIVE_PATH].get("artifact"), "Stage-4D artifact"
    )
    stage4d_tail = _mapping(
        stage4d_artifact.get("summable_adjoint_tail_certificate"),
        "Stage-4D tail",
    )
    stage4d_measure = _mapping(
        stage4d_artifact.get("continuous_history_measure_enclosure"),
        "Stage-4D measure",
    )

    return Stage4SHessianBridge(
        schema_id=SCHEMA_ID,
        model_id=MODEL_ID,
        branch=BRANCH,
        status=STATUS,
        parent_result_sha256=dict(PARENT_RESULT_SHA256),
        finite_section_audit={
            "stage4q_mesh_counts": [120, 180, 240],
            "stage4q_evidence_status": "DIAGNOSTIC_NONRIGOROUS_SOURCE_BOUND",
            "stage4q_binary_rows_are_outward_rounded": False,
            "stage4q_finite_section_adapter_is_validated": False,
            "stage4q_all_nineteen_theorem_flags_false": True,
            "stage4q_signed_formation_order_is_structurally_correct": True,
            "stage4q_direct_vs_composition_oracle_is_an_error_bound": False,
            "stage4q_mesh_envelope_is_an_error_bound": False,
            "use_permitted_here": (
                "allocation-scale diagnostic only; no value enters strict numeric "
                "ingress or a Banach Hessian inequality"
            ),
        },
        finite_sampling_no_go={
            "phase_space": "X=C(K) with the supremum norm, K a nontrivial compact interval",
            "sampler": "S_N h=(h(t_1),...,h(t_N)) at any finite node set",
            "reconstruction": "any bounded linear R_N:R^N->X",
            "witness": (
                "choose t_* outside the nodes and h in C(K) with ||h||_infinity=1, "
                "h(t_j)=0 and h(t_*)=1"
            ),
            "identity": "S_N h=0, hence (I-R_N S_N)h=h",
            "operator_norm_lower": "1",
            "conclusion": "||I-R_N S_N||>=1 for every finite N",
            "bilinear_invisibility_witness": (
                "B_*(h,k)=h(t_*)k(t_*)y_* has norm one but its action is "
                "undetermined by the nodal data"
            ),
            "mesh_refinement_alone_controls_arbitrary_C_ball": False,
            "repair": (
                "use a physical-coordinate signed atom-density bimeasure residual, "
                "or declare an equicontinuous/smoother domain with a common modulus"
            ),
            "proved": True,
        },
        atomic_bimeasure_lift={
            "coefficient_tensor": "A=(a_oij) at exact physical input nodes",
            "lift": (
                "B_N(h,k)=R_out((sum_ij a_oij h(t_i)k(t_j))_o), with "
                "piecewise-linear R_out"
            ),
            "input_sampler_norm": "1",
            "piecewise_linear_output_reconstruction_norm": "1",
            "operator_bound": "||B_N|| <= max_o sum_ij |a_oij|",
            "continuous_output_completion": (
                "if the exact bimeasure row is L_theta-Lipschitz on an endpoint-"
                "complete mesh of width Delta, sup_theta ||B(theta)|| <= "
                "max_nodes ||B(theta_j)|| + Delta*L_theta/2"
            ),
            "directed_coefficients_required": True,
            "stage4q_coefficients_directed_here": False,
            "difference_to_true_RFDE_Hessian_bounded_here": False,
            "proved_lemma": True,
        },
        cubic_stencil_certificates={
            "interior_four_node": {
                "normalized_nodes": ["-1", "0", "1", "2"],
                "evaluation_cell": "x in [0,1]",
                "weight_signs_on_open_cell": ["-", "+", "+", "-"],
                "lebesgue_polynomial_on_cell": "1+x-x^2",
                "exact_lebesgue_constant": "5/4",
                "lebesgue_maximizer": "x=1/2",
                "common_Lipschitz_error_polynomial_times_Delta_L": (
                    "(4/3)*x*(x-2)*(x-1)*(x+1)"
                ),
                "exact_common_Lipschitz_error_constant_times_Delta": "3/4",
                "common_Lipschitz_error_maximizer": "x=1/2",
                "modulus_bound": "|h-I_3h| <= (5/4)*omega_h(2*Delta)",
                "stability_proved": True,
                "uniform_C_ball_convergence_proved": False,
            },
            "one_sided_right_endpoint": {
                "normalized_nodes": ["-3", "-2", "-1", "0"],
                "evaluation_cell": "x in [-1,0]",
                "weight_polynomials": [
                    "-x(x+1)(x+2)/6",
                    "x(x+1)(x+3)/2",
                    "-x(x+2)(x+3)/2",
                    "(x+1)(x+2)(x+3)/6",
                ],
                "weight_signs_on_open_cell": ["+", "-", "+", "+"],
                "lebesgue_polynomial_on_cell": "1-3*x-4*x^2-x^3",
                "exact_lebesgue_constant": "(7+14*sqrt(7))/27",
                "lebesgue_constant_directed_decimal": _directed_decimal_bracket(
                    endpoint_lebesgue
                ),
                "lebesgue_maximizer": "x=(-4+sqrt(7))/3",
                "common_Lipschitz_error_polynomial_times_Delta_L": (
                    "-(4/3)*x*(x+1)*(x+2)*(x+3)"
                ),
                "exact_common_Lipschitz_error_constant_times_Delta": "4/3",
                "common_Lipschitz_error_maximizer": "x=(-3+sqrt(5))/2",
                "modulus_bound": (
                    "|h-I_3h| <= ((7+14*sqrt(7))/27)*omega_h(3*Delta)"
                ),
                "positive_time_nodes_used": False,
                "stability_proved": True,
                "uniform_C_ball_convergence_proved": False,
            },
            "application_boundary": (
                "the constants prove stability and conditional error for a common "
                "modulus/Lipschitz class; the Stage-4M stable ball contains arbitrary "
                "continuous histories and supplies no such common modulus"
            ),
        },
        continuous_projection_stability={
            "continuous_pair": "||q_hat||_Y=1, f_hat(q_hat)=1, P_s=I-q_hat*f_hat",
            "stage4l_exact_restricted_fhat_norm_upper": _decimal_text(f_norm),
            "P_s_norm_upper": _decimal_text(Decimal(1) + f_norm),
            "raw_Hessian_remainder_rule": (
                "if ||H-H_tilde||_bilinear<=eta before input/output projection, "
                "the six block errors are at most factor_i*eta"
            ),
            "block_amplification_factors": {
                name: _decimal_text(value) for name, value in factors.items()
            },
            "factor_formulas": {
                "stable_output_ss_upper": "||P_s||^3",
                "stable_output_su_upper": "||P_s||^2",
                "stable_output_uu_upper": "||P_s||",
                "unstable_output_ss_upper": "||f_hat||*||P_s||^2",
                "unstable_output_su_upper": "||f_hat||*||P_s||",
                "unstable_output_uu_upper": "||f_hat||",
            },
            "stage4d_continuous_atom_density_measure_enclosed": True,
            "stage4d_normalized_history_measure_norm_upper": str(
                stage4d_measure["normalized_history_measure_norm_upper"]
            ),
            "stage4d_raw_fourier_tail_split_l1_upper": str(
                stage4d_tail["full_tail_split_l1_upper"]
            ),
            "tail_use_boundary": (
                "these parent bounds validate existence/summability of the continuous "
                "output covector; an all-six kernel action and its correlated tail "
                "error still require the missing bimeasure rows"
            ),
            "direct_projected_residual_avoids_raw_factor_loss": True,
        },
        wide_box_error_budget=_budget_rows(caps, diagnostic, factors),
        required_interval_quantities=_required_interval_quantities(),
        strict_numeric_ingress=_strict_numeric_ingress(),
        failure_gates={
            "release_rule": (
                "fail if any one of the following gates is triggered; all six blocks "
                "must be certified in one correlated source-bound run"
            ),
            "gates": [
                {
                    "id": "S1_sampling_blindness",
                    "failure_condition": (
                        "mesh convergence or nodal interpolation is used as an "
                        "operator-norm estimate on the arbitrary C-history ball"
                    ),
                    "triggered_by_current_stage4q": True,
                },
                {
                    "id": "S2_binary_not_outward",
                    "failure_condition": (
                        "a Stage-4Q binary row or heuristic envelope is entered as an "
                        "outward core bound"
                    ),
                    "triggered_by_current_stage4q": True,
                },
                {
                    "id": "S3_missing_signed_kernel_residual",
                    "failure_condition": (
                        "any source time, delay slot, activation face, short cell, "
                        "history seam, or output phase is absent"
                    ),
                    "triggered_by_current_stage4q": True,
                },
                {
                    "id": "S4_event_denominator",
                    "failure_condition": (
                        "the full-ball common event window or positive denominator is "
                        "missing, or event terms are divided/normed separately"
                    ),
                    "triggered_by_current_stage4q": True,
                },
                {
                    "id": "S5_coordinate_mismatch",
                    "failure_condition": (
                        "finite q/f quadrature replaces the exact continuous pair "
                        "without a directed pair-and-tail error"
                    ),
                    "triggered_by_current_stage4q": True,
                },
                {
                    "id": "S6_output_phase_completion",
                    "failure_condition": (
                        "nodal output maxima are used without a continuous theta "
                        "supremum or derivative/Bernstein completion"
                    ),
                    "triggered_by_current_stage4q": True,
                },
                {
                    "id": "S7_full_ball_inflation",
                    "failure_condition": (
                        "a center-orbit kernel is promoted without a D3F-based or "
                        "direct nonlinear-ball perturbation enclosure"
                    ),
                    "triggered_by_current_stage4q": True,
                },
                {
                    "id": "S8_projection_order",
                    "failure_condition": (
                        "rank-one/event/output terms are normed before their signed "
                        "combination or the moving phase projection is applied twice"
                    ),
                    "triggered_by_current_stage4q": False,
                },
            ],
            "all_release_gates_pass": False,
        },
        theorem_boundary={
            "proved_here": (
                "the sampling no-go, atomic lift, stencil stability constants, exact "
                "projection factors, exact wide-box allocation, and complete future "
                "interval certificate interface"
            ),
            "not_proved_here": (
                "a directed lift of the Stage-4Q tensor, its distance to the RFDE "
                "Hessian, a common two-return event/return tube, any uniform Hessian "
                "block, stable graph, crossing, onset, routing, capture, or safety"
            ),
            "stage4q_status_preserved": "DIAGNOSTIC_NONRIGOROUS_SOURCE_BOUND",
            "wide_box_status_preserved": "CONDITIONAL_ACCEPTANCE_DESIGN_ONLY",
            "preferred_next_certificate": (
                "a physical-coordinate atom-density-bimeasure residual for U and V "
                "through two periods, with the event quotient and exact q/f outputs "
                "formed before total variation"
            ),
        },
        claim_status=claims,
    )


def build_stage4s_hessian_bridge(repository: Path) -> Stage4SHessianBridge:
    """Build at fixed precision without mutating the process Decimal context."""

    with localcontext() as context:
        context.prec = 110
        return _build_stage4s_hessian_bridge_in_context(repository)


def build_stage4s_hessian_bridge_result(repository: Path) -> dict[str, Any]:
    repository = repository.resolve()
    bridge = asdict(build_stage4s_hessian_bridge(repository))
    return {
        "bridge": bridge,
        "manifest": {
            "schema_id": SCHEMA_ID,
            "result": RESULT_RELATIVE_PATH,
            "default_command": DEFAULT_COMMAND,
            "arithmetic_scope": ARITHMETIC_SCOPE,
            "bridge_sha256": canonical_sha256(bridge),
            "arithmetic_core_sha256": canonical_sha256(_arithmetic_core(bridge)),
            "source_sha256": {
                relative: _sha256_path(repository / relative)
                for relative in SOURCE_MANIFEST
            },
            "parent_result_sha256": dict(PARENT_RESULT_SHA256),
            "runtime": {
                "python": platform.python_version(),
                "platform": platform.platform(),
                "arithmetic": (
                    "decimal.Decimal at 110 digits plus exact symbolic identities"
                ),
            },
        },
    }


def validate_stage4s_hessian_bridge_result(
    payload: Mapping[str, Any], repository: Path, *, recompute: bool = False
) -> None:
    if not isinstance(payload, Mapping) or set(payload) != {"bridge", "manifest"}:
        raise ValueError("the Stage-4S-B result has the wrong outer schema")
    bridge = _mapping(payload.get("bridge"), "Stage-4S-B bridge")
    manifest = _mapping(payload.get("manifest"), "Stage-4S-B manifest")
    if set(bridge) != {field.name for field in fields(Stage4SHessianBridge)}:
        raise ValueError("the Stage-4S-B bridge schema changed")
    if (
        bridge.get("schema_id") != SCHEMA_ID
        or bridge.get("model_id") != MODEL_ID
        or bridge.get("branch") != BRANCH
        or bridge.get("status") != STATUS
        or bridge.get("parent_result_sha256") != PARENT_RESULT_SHA256
    ):
        raise ValueError("the Stage-4S-B identity changed")

    expected_bridge = asdict(build_stage4s_hessian_bridge(repository.resolve()))
    if dict(bridge) != expected_bridge:
        raise ValueError("the Stage-4S-B theorem/design record changed")

    claims = _mapping(bridge.get("claim_status"), "Stage-4S-B claims")
    if set(claims) != set(TRUE_FLAGS) | set(FALSE_FLAGS):
        raise ValueError("the Stage-4S-B claim ledger changed")
    if any(claims.get(name) is not True for name in TRUE_FLAGS):
        raise ValueError("a proved Stage-4S-B bridge fact was weakened")
    if any(claims.get(name) is not False for name in FALSE_FLAGS):
        raise ValueError("an open Stage-4S-B Hessian gate was promoted")

    no_go = _mapping(bridge.get("finite_sampling_no_go"), "sampling no-go")
    if (
        no_go.get("operator_norm_lower") != "1"
        or no_go.get("mesh_refinement_alone_controls_arbitrary_C_ball") is not False
        or no_go.get("proved") is not True
    ):
        raise ValueError("the finite-sampling no-go was weakened")

    ingress = _mapping(
        bridge.get("strict_numeric_ingress"), "Stage-4S-B strict ingress"
    )
    for key, value in ingress.items():
        if key == "evidence_status":
            if value != "OPEN_FAIL_CLOSED_AFTER_EXACT_BRIDGE_AUDIT":
                raise ValueError("the Stage-4S-B evidence status changed")
        elif key in {
            "all_source_time_cells_and_delay_seams_covered",
            "all_output_phase_cells_and_endpoints_covered",
            "all_six_blocks_from_one_correlated_run",
            "all_six_strict_budget_tests_pass",
        }:
            if value is not False:
                raise ValueError("a Stage-4S-B coverage gate was promoted")
        elif isinstance(value, Mapping):
            stack = [value]
            while stack:
                current = stack.pop()
                for item in current.values():
                    if isinstance(item, Mapping):
                        stack.append(item)
                    elif item is not None:
                        raise ValueError("a Stage-4S-B numeric ingress was filled")
        elif value is not None:
            raise ValueError("a Stage-4S-B numeric ingress was filled")

    budget = _mapping(bridge.get("wide_box_error_budget"), "Stage-4S-B budget")
    if (
        budget.get("direct_projected_route_preferred") is not True
        or budget.get("all_six_strict_acceptance_tests_validated") is not False
    ):
        raise ValueError("the Stage-4S-B budget boundary changed")
    for name in BLOCK_NAMES:
        row = _mapping(
            _mapping(budget.get("blocks"), "Stage-4S-B block rows").get(name),
            name,
        )
        if (
            row.get("actual_directed_core_bound") is not None
            or row.get("strict_block_acceptance_validated") is not False
            or any(
                item is not None
                for item in _mapping(
                    row.get("actual_projected_error_contributions"),
                    f"{name} actual errors",
                ).values()
            )
        ):
            raise ValueError("a Stage-4S-B design budget was promoted")

    expected_manifest = {
        "schema_id": SCHEMA_ID,
        "result": RESULT_RELATIVE_PATH,
        "default_command": DEFAULT_COMMAND,
        "arithmetic_scope": ARITHMETIC_SCOPE,
        "bridge_sha256": canonical_sha256(bridge),
        "arithmetic_core_sha256": canonical_sha256(_arithmetic_core(bridge)),
        "source_sha256": {
            relative: _sha256_path(repository / relative)
            for relative in SOURCE_MANIFEST
        },
        "parent_result_sha256": dict(PARENT_RESULT_SHA256),
        "runtime": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "arithmetic": "decimal.Decimal at 110 digits plus exact symbolic identities",
        },
    }
    if dict(manifest) != expected_manifest:
        raise ValueError("the Stage-4S-B manifest or source binding changed")


__all__ = [
    "ARITHMETIC_SCOPE",
    "BLOCK_NAMES",
    "CORE_TARGETS",
    "DEFAULT_COMMAND",
    "ERROR_FRACTIONS",
    "FALSE_FLAGS",
    "GENERATOR_RELATIVE_PATH",
    "NOTE_RELATIVE_PATH",
    "PARENT_RESULT_SHA256",
    "RESULT_RELATIVE_PATH",
    "SCHEMA_ID",
    "SOURCE_MANIFEST",
    "SOURCE_RELATIVE_PATH",
    "STATUS",
    "TEST_RELATIVE_PATH",
    "TRUE_FLAGS",
    "Stage4SHessianBridge",
    "_arithmetic_core",
    "build_stage4s_hessian_bridge",
    "build_stage4s_hessian_bridge_result",
    "canonical_sha256",
    "validate_stage4s_hessian_bridge_result",
]
