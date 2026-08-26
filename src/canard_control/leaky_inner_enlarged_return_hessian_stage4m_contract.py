"""Stage-4M nonclosing contract for the enlarged return-Hessian blocks.

Stage 4K identifies an enlarged anisotropic graph box and proves an exact
design fact: if all six projected return-Hessian blocks are simultaneously
bounded by the Stage-4A heuristic row times ``13.2353``, then the preferred-B
two-component majorant still closes under its explicitly hypothetical linear
and return-ball inputs.  Stage 4K does not prove any of those six bounds.

This module turns that design fact into a source-bound upgrade contract.  It
fixes the continuous-history unit-Y splitting, computes the six strict caps
exactly, replays one common majorant, records the complete moving-event
second-return formula, and requires stable deflation and unstable action to be
formed before norms.  It also freezes the first missing parent: there is no
validated nonlinear selected-return tube/event graph on the full anisotropic
ball.  Without that common domain, a uniform supremum of ``D2P(x)`` is not a
defined theorem input, so every actual Hessian block and every graph, crossing,
onset, routing, capture, and safety flag remains false.

No Stage-4L numerical result is imported.  Its prospective linear stable-row
certificate cannot substitute for the nonlinear return family needed here.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from decimal import Decimal, localcontext
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
import platform
from typing import Any, Mapping

from canard_control.leaky_inner_stable_graph_enlargement_stage4k import (
    EXPECTED_STAGE4A_HEURISTIC_BLOCKS,
    RESULT_RELATIVE_PATH as STAGE4K_RESULT_RELATIVE_PATH,
    TERMINAL_RATE_SENSITIVITY_CEILING_LOWER_PROBE,
    TERMINAL_RATE_SENSITIVITY_CEILING_UPPER_PROBE,
    validate_stage4k_diagnostic_result,
)
from canard_control.leaky_projected_return_hessian_stage4_contract import (
    HESSIAN_FIELD_NAMES,
    MatrixLyapunovPerronInputBudget,
    ProjectedReturnHessianBlockBudget,
    evaluate_matrix_lyapunov_perron_majorant,
)


SCHEMA_ID = "leaky-inner-enlarged-return-hessian-stage4m-contract-v1"
MODEL_ID = "autonomous-leaky-recovery-two-delay-fhn-bistable-proposal"
BRANCH = "inner_saddle_candidate_selected_near_period_return"
STATUS = "NONCLOSING_CONTRACT"

SOURCE_RELATIVE_PATH = (
    "src/canard_control/leaky_inner_enlarged_return_hessian_stage4m_contract.py"
)
GENERATOR_RELATIVE_PATH = (
    "experiments/leaky_inner_enlarged_return_hessian_stage4m_contract.py"
)
RESULT_RELATIVE_PATH = (
    "experiments/results/"
    "leaky_inner_enlarged_return_hessian_stage4m_contract.json"
)
NOTE_RELATIVE_PATH = (
    "docs/leaky-inner-enlarged-return-hessian-stage4m-contract.md"
)
TEST_RELATIVE_PATH = (
    "tests/test_leaky_inner_enlarged_return_hessian_stage4m_contract.py"
)

STAGE4K_RESULT_SHA256 = (
    "57119dc28bfa841b4f1a9dcddc3af542783493da94862ed2f7336202b05e2f5c"
)
PARENT_RESULT_SHA256 = {
    STAGE4K_RESULT_RELATIVE_PATH: STAGE4K_RESULT_SHA256,
}

SOURCE_MANIFEST = (
    SOURCE_RELATIVE_PATH,
    GENERATOR_RELATIVE_PATH,
    NOTE_RELATIVE_PATH,
    TEST_RELATIVE_PATH,
)
DEPENDENCY_SOURCE_MANIFEST = (
    "src/canard_control/leaky_inner_stable_graph_enlargement_stage4k.py",
    "src/canard_control/leaky_projected_return_hessian_stage4_contract.py",
)

DEFAULT_COMMAND = (
    "PYTHONPATH=src /usr/bin/python3 "
    "experiments/leaky_inner_enlarged_return_hessian_stage4m_contract.py"
)
ARITHMETIC_SCOPE = (
    "normal validation and byte binding of Stage 4K; exact Fraction products "
    "of its six source-bound heuristic decimals with the common lower closing "
    "probe 13.2353; replay of all six caps in one exact-rational Stage-4 "
    "Lyapunov--Perron majorant; and a nonclosing complete-history moving-event "
    "return-Hessian interface; no Stage-4L numeric ingress, nonlinear return "
    "tube, projected Hessian block, graph, crossing, onset, routing, capture, "
    "or safety promotion"
)

COMMON_CAP_MULTIPLIER = TERMINAL_RATE_SENSITIVITY_CEILING_LOWER_PROBE
REJECTED_UPPER_PROBE = TERMINAL_RATE_SENSITIVITY_CEILING_UPPER_PROBE
STABLE_SEED_RADIUS = "0.0094"
STABLE_GRAPH_RADIUS = "0.0097"
UNIT_UNSTABLE_GRAPH_RADIUS = "0.00025"
SPLIT_RETURN_RADIUS = "0.00995"
DESIGN_STABLE_RATE = "0.1"
DESIGN_STABLE_POWER_CONSTANT = "1"
DESIGN_UNSTABLE_RATE = (
    "0.549712198641301272665939640423769383243380071590152304446016306796024304322569720837972565017934"
)
DESIGN_UNSTABLE_POWER_CONSTANT = "1"
DESIGN_SEQUENCE_WEIGHT = "0.9999"

TOP_KEYS = {"contract", "manifest"}
MANIFEST_KEYS = {
    "schema_id",
    "result",
    "default_command",
    "arithmetic_scope",
    "contract_sha256",
    "numeric_core_sha256",
    "source_sha256",
    "dependency_source_sha256",
    "parent_result_sha256",
    "runtime",
}

TRUE_FLAGS = (
    "stage4k_parent_bytes_and_claim_boundary_validated",
    "preferred_b_anisotropic_geometry_registered",
    "fixed_unit_y_splitting_interface_registered",
    "six_common_caps_computed_by_exact_rational_arithmetic",
    "all_six_caps_enter_one_common_majorant_replay",
    "common_cap_majorant_closes_only_as_conditional_design_arithmetic",
    "complete_history_moving_event_hessian_formula_registered",
    "correlated_fixed_projection_before_norm_requirement_registered",
    "first_missing_nonlinear_return_tube_parent_frozen",
    "stage4l_numeric_result_excluded_from_parent_set",
)
FALSE_FLAGS = (
    "nonlinear_selected_return_tube_on_full_anisotropic_ball_validated",
    "common_selected_event_window_validated",
    "uniform_event_speed_lower_bound_validated",
    "complete_returned_history_tube_validated",
    "no_earlier_section_hit_validated",
    "continuous_history_unit_y_normalization_adapter_validated",
    "stable_output_ss_block_validated",
    "stable_output_su_block_validated",
    "stable_output_uu_block_validated",
    "unstable_output_ss_block_validated",
    "unstable_output_su_block_validated",
    "unstable_output_uu_block_validated",
    "all_six_projected_return_hessian_blocks_validated",
    "all_six_certified_blocks_strictly_below_common_caps_validated",
    "majorant_with_certified_hessian_blocks_validated",
    "stable_power_rate_or_constant_validated_here",
    "split_return_ball_validated_here",
    "quantitative_inner_stable_graph_validated",
    "selected_pulse_stable_sheet_crossing_validated",
    "unique_physical_pulse_onset_validated",
    "two_sided_basin_routing_validated",
    "outer_or_quiet_capture_from_both_sides_validated",
    "frequency_amplitude_safety_radius_validated",
    "asynchronous_network_safety_radius_validated",
)


@dataclass(frozen=True)
class Stage4MContract:
    schema_id: str
    model_id: str
    branch: str
    status: str
    parent_result_sha256: dict[str, str]
    coordinate_registration: dict[str, Any]
    anisotropic_domain: dict[str, Any]
    heuristic_source_boundary: dict[str, Any]
    common_cap_ledger: dict[str, Any]
    cap_majorant_evaluation: dict[str, Any]
    six_block_certificate_interface: dict[str, Any]
    physical_variational_system: dict[str, Any]
    moving_event_return_hessian: dict[str, Any]
    correlated_projection_order: dict[str, Any]
    required_uniform_error_ledger: dict[str, Any]
    first_missing_parent: dict[str, Any]
    strict_numeric_ingress: dict[str, Any]
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


def _fraction(text: str) -> Fraction:
    if not isinstance(text, str):
        raise ValueError("an exact decimal ingress is not a string")
    return Fraction(Decimal(text))


def _exact_decimal(value: Fraction) -> str:
    """Serialize a terminating exact fraction without binary conversion."""

    denominator = value.denominator
    twos = 0
    fives = 0
    while denominator % 2 == 0:
        denominator //= 2
        twos += 1
    while denominator % 5 == 0:
        denominator //= 5
        fives += 1
    if denominator != 1:
        raise ValueError("the exact cap does not have a terminating decimal")
    digits = max(twos, fives)
    with localcontext() as context:
        context.prec = max(96, len(str(abs(value.numerator))) + digits + 8)
        result = Decimal(value.numerator) / Decimal(value.denominator)
    text = format(result, "f")
    if _fraction(text) != value:
        raise ArithmeticError("exact decimal serialization lost the cap")
    return text


def _load_stage4k(repository: Path) -> Mapping[str, Any]:
    path = repository / STAGE4K_RESULT_RELATIVE_PATH
    raw = path.read_bytes()
    if sha256(raw).hexdigest() != STAGE4K_RESULT_SHA256:
        raise ValueError("the bound Stage-4K result changed")
    payload = json.loads(raw)
    validate_stage4k_diagnostic_result(payload, repository, recompute=False)
    return _mapping(payload, "Stage-4K result")


def _cap_records(stage4k_artifact: Mapping[str, Any]) -> list[dict[str, str]]:
    ingress = _mapping(
        stage4k_artifact.get("stage4a_heuristic_ingress"),
        "Stage-4K heuristic ingress",
    )
    candidates = _mapping(
        ingress.get("six_block_candidate_upper"),
        "Stage-4K heuristic block row",
    )
    if dict(candidates) != EXPECTED_STAGE4A_HEURISTIC_BLOCKS:
        raise ValueError("the Stage-4K heuristic six-block row changed")
    multiplier = _fraction(COMMON_CAP_MULTIPLIER)
    records: list[dict[str, str]] = []
    for name in HESSIAN_FIELD_NAMES:
        source = _fraction(str(candidates[name]))
        cap = source * multiplier
        records.append(
            {
                "block": name,
                "heuristic_source_decimal_exact": str(candidates[name]),
                "common_multiplier_exact": COMMON_CAP_MULTIPLIER,
                "strict_cap_decimal_exact": _exact_decimal(cap),
                "strict_acceptance_inequality": (
                    f"certified_{name} < strict_cap_decimal_exact"
                ),
            }
        )
    return records


def _cap_majorant(
    cap_records: list[dict[str, str]],
) -> dict[str, Any]:
    caps = {
        str(record["block"]): str(record["strict_cap_decimal_exact"])
        for record in cap_records
    }
    blocks = ProjectedReturnHessianBlockBudget(
        **caps,
        evidence_status=(
            "exact Stage-4M design caps only; no value in this row is an "
            "RFDE Hessian bound"
        ),
    )
    budget = MatrixLyapunovPerronInputBudget(
        stable_power_rate_upper=DESIGN_STABLE_RATE,
        unstable_backward_rate_upper=DESIGN_UNSTABLE_RATE,
        stable_power_constant_upper=DESIGN_STABLE_POWER_CONSTANT,
        unstable_backward_power_constant_upper=(
            DESIGN_UNSTABLE_POWER_CONSTANT
        ),
        sequence_weight_beta=DESIGN_SEQUENCE_WEIGHT,
        stable_seed_radius=STABLE_SEED_RADIUS,
        stable_graph_radius=STABLE_GRAPH_RADIUS,
        unstable_graph_radius=UNIT_UNSTABLE_GRAPH_RADIUS,
        validated_return_map_split_ball_radius_lower=SPLIT_RETURN_RADIUS,
        hessian_blocks=blocks,
        evidence_status=(
            "conditional preferred-B design budget; the stable rate, K_s, "
            "return ball, and six RFDE blocks are not theorem ingress here"
        ),
    )
    evaluation = json.loads(
        json.dumps(
            asdict(evaluate_matrix_lyapunov_perron_majorant(budget)),
            sort_keys=True,
        )
    )
    return {
        "input_budget": asdict(budget),
        "exact_evaluation": evaluation,
        "proof_interpretation": {
            "all_six_caps_inserted_simultaneously": True,
            "individual_caps_mixed_from_different_rows": False,
            "raw_exact_majorant_closes": True,
            "stable_rate_is_validated_here": False,
            "stable_power_constant_is_validated_here": False,
            "return_ball_is_validated_here": False,
            "hessian_caps_are_certified_blocks": False,
            "graph_certificate_closes": False,
            "status": "CONDITIONAL_EXACT_DESIGN_ARITHMETIC_ONLY",
        },
    }


def _numeric_core(contract: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "anisotropic_domain": contract["anisotropic_domain"],
        "common_cap_ledger": contract["common_cap_ledger"],
        "cap_majorant_evaluation": contract["cap_majorant_evaluation"],
        "first_missing_parent": contract["first_missing_parent"],
        "strict_numeric_ingress": contract["strict_numeric_ingress"],
        "claim_status": contract["claim_status"],
    }


def _runtime_record() -> dict[str, str]:
    return {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "arithmetic": (
            "fractions.Fraction exact caps plus the Stage-4 exact-rational "
            "majorant evaluator"
        ),
    }


def build_stage4m_contract(repository: Path) -> Stage4MContract:
    repository = repository.resolve()
    stage4k = _load_stage4k(repository)
    artifact = _mapping(stage4k.get("artifact"), "Stage-4K artifact")
    sensitivity = _mapping(
        artifact.get("terminal_rate_sensitivity"),
        "Stage-4K preferred-B sensitivity",
    )
    if (
        sensitivity.get("stable_graph_radius_R_s") != STABLE_GRAPH_RADIUS
        or sensitivity.get("unit_unstable_graph_radius_R_u_hat")
        != UNIT_UNSTABLE_GRAPH_RADIUS
        or sensitivity.get("graph_box_split_radius_sum")
        != SPLIT_RETURN_RADIUS
        or sensitivity.get("ceiling_lower_probe", {}).get("multiplier")
        != COMMON_CAP_MULTIPLIER
        or sensitivity.get("ceiling_upper_probe", {}).get("multiplier")
        != REJECTED_UPPER_PROBE
    ):
        raise ValueError("the Stage-4K preferred-B geometry or probes changed")

    records = _cap_records(artifact)
    cap_majorant = _cap_majorant(records)
    imported_lower = _mapping(
        _mapping(
            sensitivity.get("ceiling_lower_probe"),
            "Stage-4K lower probe",
        ).get("exact_majorant_evaluation"),
        "Stage-4K lower-probe evaluation",
    )
    if cap_majorant["exact_evaluation"] != dict(imported_lower):
        raise ValueError("the independent 13.2353 majorant replay changed")
    imported_upper = _mapping(
        _mapping(
            sensitivity.get("ceiling_upper_probe"),
            "Stage-4K upper probe",
        ).get("exact_majorant_evaluation"),
        "Stage-4K upper-probe evaluation",
    )
    if (
        imported_lower.get("graph_certificate_closes") is not True
        or imported_upper.get("graph_certificate_closes") is not False
    ):
        raise ValueError("the Stage-4K common-ceiling bracket changed")

    strict_blocks = {name: None for name in HESSIAN_FIELD_NAMES}
    claims = {name: True for name in TRUE_FLAGS}
    claims.update({name: False for name in FALSE_FLAGS})
    return Stage4MContract(
        schema_id=SCHEMA_ID,
        model_id=MODEL_ID,
        branch=BRANCH,
        status=STATUS,
        parent_result_sha256=dict(PARENT_RESULT_SHA256),
        coordinate_registration={
            "history_space": (
                "Y=C([-tau_max,0],R)_v x R_w with the inherited max norm"
            ),
            "section_tangent_space": "Sigma_0={h in Y:h_v(0)=0}",
            "physical_pair": "q,f with f(q)=1 on Sigma_0",
            "unit_y_vector": "q_hat=q/||q||_Y",
            "unit_y_functional": "f_hat=||q||_Y*f",
            "normalization": (
                "||q_hat||_Y=1 and f_hat(q_hat)=1 exactly"
            ),
            "fixed_projection": "P_s=I-q_hat*f_hat=I-q*f",
            "stable_space": "E_s=ker(f_hat) in Sigma_0",
            "unstable_coordinate": (
                "x_u is the scalar coefficient of the fixed q_hat; no moving "
                "eigensplitting is permitted over the ball"
            ),
            "normalization_transfer_validated_here": False,
        },
        anisotropic_domain={
            "base_history": "X_* on the fixed Route-C affine section",
            "history_formula": "x=X_*+x_s+q_hat*x_u",
            "stable_radius_R_s": STABLE_GRAPH_RADIUS,
            "unit_unstable_radius_R_u_hat": UNIT_UNSTABLE_GRAPH_RADIUS,
            "split_radius_sum_exact": SPLIT_RETURN_RADIUS,
            "stable_seed_radius_r": STABLE_SEED_RADIUS,
            "norm": "||(x_s,x_u)||_split=||x_s||_Y+|x_u|",
            "quantifiers": (
                "all ||x_s||_Y<=R_s, |x_u|<=R_u_hat, all unit stable "
                "directions, and both signs of the unit unstable direction"
            ),
            "validated_return_domain": False,
        },
        heuristic_source_boundary={
            "source": STAGE4K_RESULT_RELATIVE_PATH,
            "stage4a_row_is_finite_section_heuristic": True,
            "stage4a_row_is_directed_continuous_history_bound": False,
            "heuristic_row_enters_strict_numeric_ingress": False,
            "use_here": (
                "only to define six proof-design caps and replay exact "
                "preferred-B arithmetic"
            ),
        },
        common_cap_ledger={
            "common_multiplier_exact": COMMON_CAP_MULTIPLIER,
            "rejected_upper_probe_exact": REJECTED_UPPER_PROBE,
            "acceptance_rule": (
                "one future certificate must prove all six upper bounds from "
                "the same nonlinear return tube, each strictly below its cap"
            ),
            "records": records,
            "caps_are_rfde_bounds": False,
            "lower_probe_closes_conditionally": True,
            "upper_probe_fails_conditionally": True,
        },
        cap_majorant_evaluation=cap_majorant,
        six_block_certificate_interface={
            "stable_output_ss": (
                "sup ||P_s D2P(x)[h_s,k_s]||_Y for unit h_s,k_s in E_s"
            ),
            "stable_output_su": (
                "sup ||P_s D2P(x)[h_s,q_hat]||_Y for unit h_s in E_s"
            ),
            "stable_output_uu": "sup ||P_s D2P(x)[q_hat,q_hat]||_Y",
            "unstable_output_ss": (
                "sup |f_hat(D2P(x)[h_s,k_s])| for unit h_s,k_s in E_s"
            ),
            "unstable_output_su": (
                "sup |f_hat(D2P(x)[h_s,q_hat])| for unit h_s in E_s"
            ),
            "unstable_output_uu": (
                "sup |f_hat(D2P(x)[q_hat,q_hat])|"
            ),
            "uniform_base_domain": "the entire anisotropic domain above",
            "mixed_slot_symmetry": "D2P[h_s,q_hat]=D2P[q_hat,h_s]",
            "common_run_requirement": (
                "all six blocks use one source-bound nonlinear flow/event "
                "tube and one fixed q_hat,f_hat,P_s normalization"
            ),
            "forbidden_shortcuts": (
                "four-block reduction, finite-node history norm, sampled "
                "base points, different cap rows, or separately normed "
                "projection terms"
            ),
        },
        physical_variational_system={
            "base_flow": "dX/dt=F(X_t), X_0=x in the anisotropic domain",
            "first_variation": (
                "dU_h/dt=DF(X_t)U_h,t, U_h,0=h"
            ),
            "second_variation": (
                "dV_hk/dt=DF(X_t)V_hk,t+D2F(X_t)[U_h,t,U_k,t], "
                "V_hk,0=0"
            ),
            "required_sectors": "U_s,U_u,V_ss,V_su,V_uu",
            "current_voltage_hessian": (
                "-2*v(t)-6*epsilon*kappa_3*(v(t)-1)"
            ),
            "delayed_voltage_hessian_each_delay": (
                "3*epsilon*kappa_3*(v(t-tau_j)-1), j=0,1"
            ),
            "mixed_and_recovery_hessian_entries": "zero",
            "third_derivatives_for_uniformity": (
                "current -2-6*epsilon*kappa_3; each delayed slot "
                "3*epsilon*kappa_3"
            ),
            "time_scale": "physical time, not normalized Fourier phase",
        },
        moving_event_return_hessian={
            "selected_event": (
                "T(x) is the unique event in one common near-period window; "
                "first-positive status additionally requires no-earlier-hit"
            ),
            "affine_event_row": "ell_0(y)=y_v(0)",
            "event_speed": "a(x)=ell_0(dot X(T(x);x))>0",
            "first_event_derivative": (
                "T_h=-ell_0(U_h(T;x))/a(x)"
            ),
            "history_core": (
                "W_hk(theta)=V_hk(T+theta)+dot U_h(T+theta)T_k+"
                "dot U_k(T+theta)T_h+ddot X(T+theta)T_h*T_k"
            ),
            "second_event_derivative": "T_hk=-ell_0(W_hk(0))/a(x)",
            "complete_history_return_hessian": (
                "D2P(x)[h,k](theta)=W_hk(theta)+dot X(T+theta)T_hk, "
                "for every theta in [-tau_max,0], with the recovery "
                "coordinate evaluated at theta=0"
            ),
            "moving_event_terms_retained": True,
            "endpoint_only_correction_forbidden": True,
        },
        correlated_projection_order={
            "stable_output": (
                "form G_s(theta)=D2P(theta)-q_hat(theta)*"
                "f_hat(D2P) as one atom-density/history object, then take "
                "the inherited Y norm"
            ),
            "unstable_output": (
                "form the complete correlated atom-plus-density action "
                "f_hat(D2P), then take its absolute value"
            ),
            "event_correction_order": (
                "insert T_h,T_k,T_hk and all translated-history terms before "
                "either stable deflation or unstable action"
            ),
            "fixed_projection_over_ball": True,
            "moving_projection_forbidden": True,
            "triangle_of_separately_normed_terms_forbidden": True,
        },
        required_uniform_error_ledger={
            "nonlinear_base_history_tube": None,
            "common_event_time_window": None,
            "event_speed_lower": None,
            "event_speed_and_tangent_correlation": None,
            "complete_returned_history_translation": None,
            "first_variation_stable_operator": None,
            "first_variation_unit_unstable_column": None,
            "second_variation_ss_operator": None,
            "second_variation_su_operator": None,
            "second_variation_uu_history": None,
            "time_derivative_and_acceleration_terms": None,
            "q_hat_f_hat_normalization_and_tails": None,
            "stable_deflation_common_row": None,
            "unstable_functional_common_row": None,
            "delay_activation_and_history_cell_seams": None,
            "continuous_base_and_direction_suprema": None,
            "no_earlier_hit_separation": None,
            "evidence_status": (
                "OPEN: no item may be filled from Stage-4A sampling or an "
                "unpublished Stage-4L numerical value"
            ),
        },
        first_missing_parent={
            "required_parent_stage": "Stage-4N nonlinear selected-return tube",
            "required_parent_result_path": None,
            "required_parent_result_sha256": None,
            "full_anisotropic_ball": (
                "||x_s||_Y<=0.0097 and |x_u_hat|<=0.00025"
            ),
            "nonlinear_flow_family_Y_tube_remainder_upper": None,
            "common_selected_event_window": None,
            "uniform_event_speed_lower": None,
            "complete_returned_history_tube_radius_upper": None,
            "no_earlier_hit_margin_lower": None,
            "blocking_reason": (
                "without one source-bound nonlinear selected-event return "
                "family on the full ball, D2P(x) has no validated common "
                "domain over which any of the six operator suprema can be "
                "taken"
            ),
            "stage4l_can_substitute": False,
        },
        strict_numeric_ingress={
            "directed_uniform_hessian_blocks": strict_blocks,
            "all_six_blocks_from_one_tube": False,
            "all_six_strict_cap_tests_pass": False,
            "majorant_with_certified_blocks": None,
            "return_tube_parent": None,
            "stage4l_numeric_parent": None,
            "evidence_status": "OPEN_NONCLOSING",
        },
        theorem_boundary={
            "proved_here": (
                "only the source-bound contract, six exact design caps, and "
                "their common conditional majorant replay"
            ),
            "not_proved_here": (
                "a nonlinear return map on the enlarged ball, any projected "
                "return-Hessian block, a stable graph, pulse/stable-sheet "
                "crossing, onset, routing, capture, or safety theorem"
            ),
            "stage4l_dependency": (
                "none; a discrete linear stable row cannot define or bound "
                "the nonlinear moving-event return family"
            ),
        },
        claim_status=claims,
    )


def build_stage4m_result(repository: Path) -> dict[str, Any]:
    repository = repository.resolve()
    contract = asdict(build_stage4m_contract(repository))
    return {
        "contract": contract,
        "manifest": {
            "schema_id": SCHEMA_ID,
            "result": RESULT_RELATIVE_PATH,
            "default_command": DEFAULT_COMMAND,
            "arithmetic_scope": ARITHMETIC_SCOPE,
            "contract_sha256": canonical_sha256(contract),
            "numeric_core_sha256": canonical_sha256(_numeric_core(contract)),
            "source_sha256": {
                relative: _sha256_path(repository / relative)
                for relative in SOURCE_MANIFEST
            },
            "dependency_source_sha256": {
                relative: _sha256_path(repository / relative)
                for relative in DEPENDENCY_SOURCE_MANIFEST
            },
            "parent_result_sha256": dict(PARENT_RESULT_SHA256),
            "runtime": _runtime_record(),
        },
    }


def validate_stage4m_result(
    payload: Mapping[str, Any],
    repository: Path,
    *,
    recompute: bool = False,
) -> None:
    if not isinstance(payload, Mapping) or set(payload) != TOP_KEYS:
        raise ValueError("the Stage-4M result has the wrong outer schema")
    contract = _mapping(payload.get("contract"), "Stage-4M contract")
    manifest = _mapping(payload.get("manifest"), "Stage-4M manifest")
    if set(contract) != {field.name for field in fields(Stage4MContract)}:
        raise ValueError("the Stage-4M contract schema changed")
    if (
        contract.get("schema_id") != SCHEMA_ID
        or contract.get("model_id") != MODEL_ID
        or contract.get("branch") != BRANCH
        or contract.get("status") != STATUS
    ):
        raise ValueError("the Stage-4M identity changed")

    repository = repository.resolve()
    _load_stage4k(repository)
    if contract.get("parent_result_sha256") != PARENT_RESULT_SHA256:
        raise ValueError("the Stage-4M parent ledger changed")
    if any("stage4l" in key.lower() for key in PARENT_RESULT_SHA256):
        raise ValueError("Stage 4M may not bind an unpublished Stage-4L result")

    claims = _mapping(contract.get("claim_status"), "Stage-4M claims")
    if set(claims) != set(TRUE_FLAGS) | set(FALSE_FLAGS):
        raise ValueError("the Stage-4M claim ledger changed")
    if any(claims.get(name) is not True for name in TRUE_FLAGS):
        raise ValueError("a Stage-4M contract fact was weakened")
    if any(claims.get(name) is not False for name in FALSE_FLAGS):
        raise ValueError("an open Stage-4M theorem gate was promoted")

    cap_ledger = _mapping(
        contract.get("common_cap_ledger"), "Stage-4M cap ledger"
    )
    records = cap_ledger.get("records")
    if not isinstance(records, list) or len(records) != len(HESSIAN_FIELD_NAMES):
        raise ValueError("the Stage-4M six-cap row changed")
    if cap_ledger.get("common_multiplier_exact") != COMMON_CAP_MULTIPLIER:
        raise ValueError("the Stage-4M common multiplier changed")
    expected_caps = {
        name: _exact_decimal(
            _fraction(EXPECTED_STAGE4A_HEURISTIC_BLOCKS[name])
            * _fraction(COMMON_CAP_MULTIPLIER)
        )
        for name in HESSIAN_FIELD_NAMES
    }
    actual_caps: dict[str, str] = {}
    for index, record in enumerate(records):
        item = _mapping(record, f"Stage-4M cap {index}")
        name = str(item.get("block"))
        if name != HESSIAN_FIELD_NAMES[index]:
            raise ValueError("the Stage-4M cap order changed")
        cap = str(item.get("strict_cap_decimal_exact"))
        if cap != expected_caps[name]:
            raise ValueError(f"the Stage-4M cap changed: {name}")
        if " < strict_cap_decimal_exact" not in str(
            item.get("strict_acceptance_inequality")
        ):
            raise ValueError("a Stage-4M strict cap became non-strict")
        actual_caps[name] = cap

    cap_majorant = _mapping(
        contract.get("cap_majorant_evaluation"), "Stage-4M cap majorant"
    )
    evaluation = _mapping(
        cap_majorant.get("exact_evaluation"), "Stage-4M exact evaluation"
    )
    interpretation = _mapping(
        cap_majorant.get("proof_interpretation"),
        "Stage-4M majorant interpretation",
    )
    if (
        evaluation.get("graph_certificate_closes") is not True
        or interpretation.get("all_six_caps_inserted_simultaneously") is not True
        or interpretation.get("hessian_caps_are_certified_blocks") is not False
        or interpretation.get("graph_certificate_closes") is not False
    ):
        raise ValueError("the conditional Stage-4M majorant was promoted")
    budget = _mapping(
        cap_majorant.get("input_budget"), "Stage-4M cap input budget"
    )
    budget_blocks = _mapping(
        budget.get("hessian_blocks"), "Stage-4M cap input blocks"
    )
    if any(budget_blocks.get(name) != actual_caps[name] for name in HESSIAN_FIELD_NAMES):
        raise ValueError("the Stage-4M common majorant does not use all six caps")

    ingress = _mapping(
        contract.get("strict_numeric_ingress"), "Stage-4M strict ingress"
    )
    blocks = _mapping(
        ingress.get("directed_uniform_hessian_blocks"),
        "Stage-4M strict Hessian blocks",
    )
    if set(blocks) != set(HESSIAN_FIELD_NAMES) or any(
        blocks.get(name) is not None for name in HESSIAN_FIELD_NAMES
    ):
        raise ValueError("an unvalidated Stage-4M Hessian block was filled")
    if (
        ingress.get("all_six_blocks_from_one_tube") is not False
        or ingress.get("all_six_strict_cap_tests_pass") is not False
        or ingress.get("majorant_with_certified_blocks") is not None
        or ingress.get("return_tube_parent") is not None
        or ingress.get("stage4l_numeric_parent") is not None
    ):
        raise ValueError("the nonclosing Stage-4M ingress was promoted")

    missing = _mapping(
        contract.get("first_missing_parent"), "Stage-4M first missing parent"
    )
    if (
        missing.get("required_parent_stage")
        != "Stage-4N nonlinear selected-return tube"
        or missing.get("required_parent_result_path") is not None
        or missing.get("nonlinear_flow_family_Y_tube_remainder_upper") is not None
        or missing.get("common_selected_event_window") is not None
        or missing.get("uniform_event_speed_lower") is not None
        or missing.get("complete_returned_history_tube_radius_upper") is not None
        or missing.get("stage4l_can_substitute") is not False
    ):
        raise ValueError("the Stage-4M first missing parent was altered")

    event = _mapping(
        contract.get("moving_event_return_hessian"),
        "Stage-4M moving-event formula",
    )
    if (
        event.get("moving_event_terms_retained") is not True
        or "dot U_h" not in str(event.get("history_core"))
        or "ddot X" not in str(event.get("history_core"))
        or "every theta in [-tau_max,0]" not in str(
            event.get("complete_history_return_hessian")
        )
    ):
        raise ValueError("the complete moving-event Hessian formula changed")
    projection = _mapping(
        contract.get("correlated_projection_order"),
        "Stage-4M projection order",
    )
    if (
        projection.get("fixed_projection_over_ball") is not True
        or projection.get("moving_projection_forbidden") is not True
        or projection.get("triangle_of_separately_normed_terms_forbidden")
        is not True
    ):
        raise ValueError("the Stage-4M correlated projection order changed")

    if set(manifest) != MANIFEST_KEYS:
        raise ValueError("the Stage-4M manifest schema changed")
    fixed_manifest = {
        "schema_id": SCHEMA_ID,
        "result": RESULT_RELATIVE_PATH,
        "default_command": DEFAULT_COMMAND,
        "arithmetic_scope": ARITHMETIC_SCOPE,
        "contract_sha256": canonical_sha256(contract),
        "numeric_core_sha256": canonical_sha256(_numeric_core(contract)),
        "parent_result_sha256": PARENT_RESULT_SHA256,
        "runtime": _runtime_record(),
    }
    if any(manifest.get(name) != value for name, value in fixed_manifest.items()):
        raise ValueError("the Stage-4M manifest fixed data changed")
    source_hashes = _mapping(
        manifest.get("source_sha256"), "Stage-4M source manifest"
    )
    dependency_hashes = _mapping(
        manifest.get("dependency_source_sha256"),
        "Stage-4M dependency manifest",
    )
    if set(source_hashes) != set(SOURCE_MANIFEST):
        raise ValueError("the Stage-4M source set changed")
    if set(dependency_hashes) != set(DEPENDENCY_SOURCE_MANIFEST):
        raise ValueError("the Stage-4M dependency set changed")
    for relative in SOURCE_MANIFEST:
        if source_hashes.get(relative) != _sha256_path(repository / relative):
            raise ValueError(f"the Stage-4M source changed: {relative}")
    for relative in DEPENDENCY_SOURCE_MANIFEST:
        if dependency_hashes.get(relative) != _sha256_path(repository / relative):
            raise ValueError(f"the Stage-4M dependency changed: {relative}")
    for relative, digest in PARENT_RESULT_SHA256.items():
        if _sha256_path(repository / relative) != digest:
            raise ValueError(f"the Stage-4M parent changed: {relative}")

    if recompute:
        expected = json.loads(
            json.dumps(asdict(build_stage4m_contract(repository)), sort_keys=True)
        )
        if dict(contract) != expected:
            raise ValueError("the Stage-4M contract differs from a fresh replay")


__all__ = [
    "ARITHMETIC_SCOPE",
    "BRANCH",
    "COMMON_CAP_MULTIPLIER",
    "DEFAULT_COMMAND",
    "DEPENDENCY_SOURCE_MANIFEST",
    "FALSE_FLAGS",
    "GENERATOR_RELATIVE_PATH",
    "MANIFEST_KEYS",
    "MODEL_ID",
    "NOTE_RELATIVE_PATH",
    "PARENT_RESULT_SHA256",
    "RESULT_RELATIVE_PATH",
    "SCHEMA_ID",
    "SOURCE_MANIFEST",
    "SOURCE_RELATIVE_PATH",
    "SPLIT_RETURN_RADIUS",
    "STABLE_GRAPH_RADIUS",
    "STABLE_SEED_RADIUS",
    "STATUS",
    "Stage4MContract",
    "TEST_RELATIVE_PATH",
    "TOP_KEYS",
    "TRUE_FLAGS",
    "UNIT_UNSTABLE_GRAPH_RADIUS",
    "_numeric_core",
    "build_stage4m_contract",
    "build_stage4m_result",
    "canonical_sha256",
    "validate_stage4m_result",
]
