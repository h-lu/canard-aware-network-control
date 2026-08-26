"""Stage-4B contract for a directed stable-output uu return block.

The Stage-4A finite-section pilot shows that the tight nonlinear input is
Pi_s D2P(q,q), not the largest absolute unstable-output block.  This module
turns that diagnosis into a continuous-history certificate interface.  The
proposed proof propagates only the unstable first variation U_q and its
second variation V_qq, validates a complete split return tube, performs the
physical-time event correction, and applies stable deflation before taking
the history norm.

The actual directed inputs remain null.  A nonrigorous target row is
evaluated only to quantify available matrix-majorant margin; it is never
inserted into the strict certificate ingress.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from decimal import Decimal, InvalidOperation
from hashlib import sha256
import json
from pathlib import Path
import platform
from typing import Any, Mapping

from canard_control.leaky_inner_stable_manifold_stage2_contract import (
    RESULT_RELATIVE_PATH as STAGE2_RESULT_RELATIVE_PATH,
    validate_stage2_stable_manifold_result,
)
from canard_control.leaky_inner_stable_projection_stage3 import (
    RESULT_RELATIVE_PATH as STAGE3_RESULT_RELATIVE_PATH,
    validate_stage3_stable_projection_result,
)
from canard_control.leaky_projected_return_hessian_stage4_contract import (
    MatrixLyapunovPerronInputBudget,
    ProjectedReturnHessianBlockBudget,
    evaluate_matrix_lyapunov_perron_majorant,
)
from canard_control.leaky_projected_return_hessian_stage4a_pilot import (
    RESULT_RELATIVE_PATH as STAGE4A_RESULT_RELATIVE_PATH,
    validate_stage4a_pilot_result,
)


SCHEMA_ID = "leaky-stable-output-uu-stage4b-contract-v1"
MODEL_ID = "autonomous-leaky-recovery-two-delay-fhn-bistable-proposal"
BRANCH = "inner_saddle_candidate"
SOURCE_RELATIVE_PATH = (
    "src/canard_control/leaky_stable_output_uu_stage4b_contract.py"
)
GENERATOR_RELATIVE_PATH = (
    "experiments/leaky_stable_output_uu_stage4b_contract.py"
)
RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_stable_output_uu_stage4b_contract.json"
)
NOTE_RELATIVE_PATH = "docs/leaky-stable-output-uu-stage4b-contract.md"
TEST_RELATIVE_PATH = "tests/test_leaky_stable_output_uu_stage4b_contract.py"
DEFAULT_COMMAND = (
    "PYTHONPATH=src /usr/bin/python3 "
    "experiments/leaky_stable_output_uu_stage4b_contract.py"
)
ARITHMETIC_SCOPE = (
    "exact parent-byte and source binding; exact Decimal ingress checks; "
    "the exact-rational Stage-4 positive-matrix evaluator; a conditional "
    "continuous-history atom-plus-density kernel certificate with directed "
    "method-of-steps residuals; physical-time event differentiation; and "
    "direct stable deflation before the history norm; no directed kernel, "
    "return tube, adjoint deflation, block bound, graph, or onset is supplied"
)
SOURCE_MANIFEST = (
    SOURCE_RELATIVE_PATH,
    GENERATOR_RELATIVE_PATH,
    NOTE_RELATIVE_PATH,
)

STAGE2_RESULT_SHA256 = (
    "eafa4d07b0558d9d4ce7423969379fa51875fcabce55af89a2378261fdb1e18d"
)
STAGE3_RESULT_SHA256 = (
    "9ea776a6e627745ded7f7023523999bfbd29a0be4878172c76512d623146e2ea"
)
STAGE4A_RESULT_SHA256 = (
    "b9308d01137559f5b88e42f7120b6eb01490aaa6bda3ac7b6eed2fd2ce5421c7"
)

STABLE_POWER_RATE = (
    "0.995024916874584026786952988590018278886039540627453615"
)
UNSTABLE_BACKWARD_RATE = (
    "0.549712198641301272665939640423769383243380071590152304446016306796024304322569720837972565017934"
)
SEQUENCE_WEIGHT_BETA = (
    "0.999378114609323003348369123573752284860754942578431701875"
)
STABLE_SEED_RADIUS = "0.0002"
STABLE_GRAPH_RADIUS = "0.0010"
UNSTABLE_GRAPH_RADIUS = "0.0007"
SPLIT_RETURN_BALL_TARGET = "0.0017"
VALIDATED_SECTION_BALL_RADIUS = "0.01"
STABLE_OUTPUT_UU_TARGET = "12"

BLOCK_NAMES = (
    "stable_output_ss_upper",
    "stable_output_su_upper",
    "stable_output_uu_upper",
    "unstable_output_ss_upper",
    "unstable_output_su_upper",
    "unstable_output_uu_upper",
)
DESIGN_BLOCK_TARGETS = {
    "stable_output_ss_upper": "0.03370300425434468588610",
    "stable_output_su_upper": "0.13314620341081993132320",
    "stable_output_uu_upper": STABLE_OUTPUT_UU_TARGET,
    "unstable_output_ss_upper": "0.4453972255632582255555",
    "unstable_output_su_upper": "0.4246441894920198467655",
    "unstable_output_uu_upper": "39.29533775993174415930",
}

REQUIRED_NUMERIC_FIELDS = (
    "stable_power_constant_upper",
    "validated_split_return_ball_radius_lower",
    "return_tube_history_radius_upper",
    "first_positive_return_time_lower",
    "first_positive_return_time_upper",
    "uniform_event_speed_lower",
    *BLOCK_NAMES,
)
REQUIRED_PROOF_FLAGS = (
    "continuous_history_atom_density_kernel_validated",
    "validated_orbit_ball_propagated",
    "split_return_tube_validated",
    "first_positive_return_and_no_earlier_hit_validated",
    "physical_time_event_hessian_validated",
    "stable_adjoint_deflation_validated",
    "uniform_ball_block_bounds_validated",
)

TRUE_FLAGS = (
    "bottleneck_stable_output_uu_identified",
    "safe_six_block_design_target_closes_matrix_pilot",
    "continuous_history_kernel_certificate_interface_registered",
    "physical_time_event_correction_precedes_projection",
    "stable_deflation_precedes_history_norm",
)
FALSE_FLAGS = (
    "design_targets_are_directed_bounds",
    "continuous_history_atom_density_kernel_validated",
    "validated_orbit_ball_propagated",
    "split_return_tube_validated",
    "stable_power_constant_numeric_upper_validated",
    "stable_adjoint_deflation_validated",
    "stable_output_uu_bound_below_twelve_validated",
    "six_projected_return_hessian_blocks_validated",
    "stage4b_strict_certificate_closes",
    "inner_local_stable_graph_quantitatively_validated",
    "graph_radius_1p7e_minus_3_validated",
    "physical_pulse_separator_crossing_validated",
    "unique_physical_pulse_onset_validated",
)


@dataclass(frozen=True)
class Stage4BDirectedInputBudget:
    stable_power_constant_upper: str | None
    validated_split_return_ball_radius_lower: str | None
    return_tube_history_radius_upper: str | None
    first_positive_return_time_lower: str | None
    first_positive_return_time_upper: str | None
    uniform_event_speed_lower: str | None
    stable_output_ss_upper: str | None
    stable_output_su_upper: str | None
    stable_output_uu_upper: str | None
    unstable_output_ss_upper: str | None
    unstable_output_su_upper: str | None
    unstable_output_uu_upper: str | None
    continuous_history_atom_density_kernel_validated: bool
    validated_orbit_ball_propagated: bool
    split_return_tube_validated: bool
    first_positive_return_and_no_earlier_hit_validated: bool
    physical_time_event_hessian_validated: bool
    stable_adjoint_deflation_validated: bool
    uniform_ball_block_bounds_validated: bool
    evidence_status: str


@dataclass(frozen=True)
class Stage4BDirectedEvaluation:
    input_complete: bool
    missing_inputs: tuple[str, ...]
    numeric_order_conditions_hold: bool
    proof_flags_hold: bool
    return_tube_inside_validated_section_ball: bool
    stable_output_uu_target_met: bool
    matrix_majorant_evaluation: dict[str, Any] | None
    strict_certificate_closes: bool


@dataclass(frozen=True)
class Stage4BContractArtifact:
    schema_id: str
    model_id: str
    branch: str
    parent_result_sha256: dict[str, str]
    bottleneck_and_safe_target: dict[str, Any]
    design_target_matrix_evaluation: dict[str, Any]
    continuous_history_kernel_contract: dict[str, Any]
    unstable_uu_variational_contract: dict[str, Any]
    return_tube_and_event_contract: dict[str, Any]
    stable_deflation_contract: dict[str, Any]
    pilot_error_allocation: dict[str, Any]
    actual_directed_input_budget: dict[str, Any]
    actual_directed_evaluation: dict[str, Any]
    coarse_other_block_interface: dict[str, Any]
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


def evaluate_stage4b_directed_budget(
    budget: Stage4BDirectedInputBudget,
) -> Stage4BDirectedEvaluation:
    values = asdict(budget)
    missing = [name for name in REQUIRED_NUMERIC_FIELDS if values[name] is None]
    missing.extend(name for name in REQUIRED_PROOF_FLAGS if values[name] is not True)
    parsed = {
        name: _decimal(values[name], name) for name in REQUIRED_NUMERIC_FIELDS
    }
    if missing:
        return Stage4BDirectedEvaluation(
            input_complete=False,
            missing_inputs=tuple(missing),
            numeric_order_conditions_hold=False,
            proof_flags_hold=False,
            return_tube_inside_validated_section_ball=False,
            stable_output_uu_target_met=False,
            matrix_majorant_evaluation=None,
            strict_certificate_closes=False,
        )
    if any(value is None for value in parsed.values()):
        raise AssertionError("a complete Stage-4B budget contains null")
    numbers = {name: value for name, value in parsed.items() if value is not None}
    k_s = numbers["stable_power_constant_upper"]
    ball = numbers["validated_split_return_ball_radius_lower"]
    tube = numbers["return_tube_history_radius_upper"]
    time_lower = numbers["first_positive_return_time_lower"]
    time_upper = numbers["first_positive_return_time_upper"]
    speed = numbers["uniform_event_speed_lower"]
    blocks_nonnegative = all(numbers[name] >= 0 for name in BLOCK_NAMES)
    numeric_order = (
        k_s >= 1
        and ball >= Decimal(SPLIT_RETURN_BALL_TARGET)
        and 0 < tube <= Decimal(VALIDATED_SECTION_BALL_RADIUS)
        and 0 < time_lower < time_upper
        and speed > 0
        and blocks_nonnegative
    )
    if not numeric_order:
        raise ValueError("the Stage-4B numeric budget violates its orders")
    proof_flags = all(values[name] is True for name in REQUIRED_PROOF_FLAGS)
    blocks = ProjectedReturnHessianBlockBudget(
        **{name: values[name] for name in BLOCK_NAMES},
        evidence_status="directed Stage-4B certificate input",
    )
    matrix_budget = MatrixLyapunovPerronInputBudget(
        stable_power_rate_upper=STABLE_POWER_RATE,
        unstable_backward_rate_upper=UNSTABLE_BACKWARD_RATE,
        stable_power_constant_upper=values["stable_power_constant_upper"],
        unstable_backward_power_constant_upper="1",
        sequence_weight_beta=SEQUENCE_WEIGHT_BETA,
        stable_seed_radius=STABLE_SEED_RADIUS,
        stable_graph_radius=STABLE_GRAPH_RADIUS,
        unstable_graph_radius=UNSTABLE_GRAPH_RADIUS,
        validated_return_map_split_ball_radius_lower=(
            values["validated_split_return_ball_radius_lower"]
        ),
        hessian_blocks=blocks,
        evidence_status="directed Stage-4B certificate input",
    )
    matrix = evaluate_matrix_lyapunov_perron_majorant(matrix_budget)
    target_met = numbers["stable_output_uu_upper"] <= Decimal(
        STABLE_OUTPUT_UU_TARGET
    )
    closes = (
        numeric_order
        and proof_flags
        and target_met
        and matrix.graph_certificate_closes
    )
    return Stage4BDirectedEvaluation(
        input_complete=True,
        missing_inputs=(),
        numeric_order_conditions_hold=True,
        proof_flags_hold=proof_flags,
        return_tube_inside_validated_section_ball=True,
        stable_output_uu_target_met=target_met,
        matrix_majorant_evaluation=asdict(matrix),
        strict_certificate_closes=closes,
    )


def _load_parent(
    repository: Path, relative: str, expected_hash: str, label: str
) -> Mapping[str, Any]:
    raw = (repository / relative).read_bytes()
    if sha256(raw).hexdigest() != expected_hash:
        raise ValueError(f"the bound {label} result changed")
    payload = json.loads(raw)
    if not isinstance(payload, Mapping):
        raise ValueError(f"the bound {label} result is malformed")
    return payload


def _design_target_evaluation() -> dict[str, Any]:
    blocks = ProjectedReturnHessianBlockBudget(
        **DESIGN_BLOCK_TARGETS,
        evidence_status="nonrigorous safe design target",
    )
    budget = MatrixLyapunovPerronInputBudget(
        stable_power_rate_upper=STABLE_POWER_RATE,
        unstable_backward_rate_upper=UNSTABLE_BACKWARD_RATE,
        stable_power_constant_upper="1",
        unstable_backward_power_constant_upper="1",
        sequence_weight_beta=SEQUENCE_WEIGHT_BETA,
        stable_seed_radius=STABLE_SEED_RADIUS,
        stable_graph_radius=STABLE_GRAPH_RADIUS,
        unstable_graph_radius=UNSTABLE_GRAPH_RADIUS,
        validated_return_map_split_ball_radius_lower=SPLIT_RETURN_BALL_TARGET,
        hessian_blocks=blocks,
        evidence_status="nonrigorous safe design target",
    )
    result = evaluate_matrix_lyapunov_perron_majorant(budget)
    if not result.graph_certificate_closes:
        raise ArithmeticError("the Stage-4B safe design target stopped closing")
    return asdict(result)


def build_stage4b_contract_artifact(repository: Path) -> Stage4BContractArtifact:
    repository = repository.resolve()
    stage2 = _load_parent(
        repository, STAGE2_RESULT_RELATIVE_PATH, STAGE2_RESULT_SHA256, "Stage-2"
    )
    stage3 = _load_parent(
        repository, STAGE3_RESULT_RELATIVE_PATH, STAGE3_RESULT_SHA256, "Stage-3"
    )
    stage4a = _load_parent(
        repository, STAGE4A_RESULT_RELATIVE_PATH, STAGE4A_RESULT_SHA256, "Stage-4A"
    )
    validate_stage2_stable_manifold_result(stage2, repository)
    validate_stage3_stable_projection_result(stage3, repository)
    validate_stage4a_pilot_result(stage4a, repository)
    stage2_contract = _mapping(stage2.get("contract"), "Stage-2 contract")
    section = _mapping(
        stage2_contract.get("explicit_voltage_section_audit"),
        "Stage-2 voltage section",
    )
    if section.get("declared_section_ball_radius") != (
        "0.00999999999999999999999999999999999999999999999998246666"
    ):
        raise ValueError("the validated Stage-2 section ball changed")
    stage3_certificate = _mapping(stage3.get("certificate"), "Stage-3 certificate")
    eigen = _mapping(
        stage3_certificate.get("eigencolumn_enclosure"), "Stage-3 eigencolumn"
    )
    stage4a_artifact = _mapping(stage4a.get("artifact"), "Stage-4A artifact")
    final_row = stage4a_artifact["mesh_rows"][-1]
    final_center = final_row["projected_hessian_block_pilot"][
        "stable_output_uu_upper"
    ]
    envelope = stage4a_artifact["refinement_pilot_envelope"][
        "projected_hessian_block_candidate_upper"
    ]["stable_output_uu_upper"]
    if final_center != "7.26111932801827375528" or envelope != (
        "7.94681563672845125978"
    ):
        raise ValueError("the Stage-4A bottleneck pilot changed")

    actual_budget = Stage4BDirectedInputBudget(
        stable_power_constant_upper=None,
        validated_split_return_ball_radius_lower=None,
        return_tube_history_radius_upper=None,
        first_positive_return_time_lower=None,
        first_positive_return_time_upper=None,
        uniform_event_speed_lower=None,
        stable_output_ss_upper=None,
        stable_output_su_upper=None,
        stable_output_uu_upper=None,
        unstable_output_ss_upper=None,
        unstable_output_su_upper=None,
        unstable_output_uu_upper=None,
        continuous_history_atom_density_kernel_validated=False,
        validated_orbit_ball_propagated=False,
        split_return_tube_validated=False,
        first_positive_return_and_no_earlier_hit_validated=False,
        physical_time_event_hessian_validated=False,
        stable_adjoint_deflation_validated=False,
        uniform_ball_block_bounds_validated=False,
        evidence_status="open directed Stage-4B ingress",
    )
    actual_evaluation = evaluate_stage4b_directed_budget(actual_budget)
    design_evaluation = _design_target_evaluation()
    claims = {name: True for name in TRUE_FLAGS}
    claims.update({name: False for name in FALSE_FLAGS})
    return Stage4BContractArtifact(
        schema_id=SCHEMA_ID,
        model_id=MODEL_ID,
        branch=BRANCH,
        parent_result_sha256={
            STAGE2_RESULT_RELATIVE_PATH: STAGE2_RESULT_SHA256,
            STAGE3_RESULT_RELATIVE_PATH: STAGE3_RESULT_SHA256,
            STAGE4A_RESULT_RELATIVE_PATH: STAGE4A_RESULT_SHA256,
        },
        bottleneck_and_safe_target={
            "bottleneck_block": "stable_output_uu_upper",
            "stage4a_final_mesh_center": final_center,
            "stage4a_heuristic_envelope": envelope,
            "isolated_first_failure_ceiling_pilot": (
                "13.91505697189666824171448158"
            ),
            "directed_design_target": STABLE_OUTPUT_UU_TARGET,
            "target_minus_final_mesh_center": (
                "4.73888067198172624472"
            ),
            "target_minus_heuristic_envelope": (
                "4.05318436327154874022"
            ),
            "target_is_strictly_below_pilot_failure_ceiling": True,
            "target_is_validated_bound": False,
        },
        design_target_matrix_evaluation=design_evaluation,
        continuous_history_kernel_contract={
            "history_operator_representation": (
                "current-state atoms plus absolutely continuous voltage-history "
                "density kernels on every method-of-steps cell"
            ),
            "history_sup_operator_norm": (
                "sum of current atom magnitudes and total variations of all "
                "history density kernels, plus the current-recovery atom"
            ),
            "required_polynomial_enclosure": (
                "outward MPFR interval Taylor or Bernstein enclosures of atoms, "
                "densities, delay seams, cell residuals, and total-variation "
                "integrals"
            ),
            "nodal_matrix_substitution_allowed": False,
            "kernel_first_variation_equation": (
                "dot(U)=A_0(X_t)U+A_1(X_t)U(t-tau_0)+"
                "A_2(X_t)U(t-tau_1)"
            ),
            "two_dimensional_logarithmic_norm": (
                "mu_2(A_0)=(a-epsilon+sqrt((a+epsilon)^2+"
                "(1-epsilon)^2))/2 for A_0=[[a,-1],[epsilon,-epsilon]]"
            ),
            "moving_center_error_inequality": (
                "r'<=mu_2(A_0)r+||A_1||r_tau0+||A_2||r_tau1+R_cell; "
                "use a pilot-centered moving frame when the raw mu_2 bound is "
                "too expansive"
            ),
        },
        unstable_uu_variational_contract={
            "fixed_input": (
                "the Stage-3 enclosed Route-C unstable section eigenhistory q, "
                "normalized to unit split unstable coordinate"
            ),
            "stage3_grushin_eigencolumn_error_upper": eigen[
                "exact_normalized_eigencolumn_split_wiener_error_upper"
            ],
            "first_variation": (
                "dot(U_q)=DF(X_t)U_q,t with U_q,0=q"
            ),
            "second_variation": (
                "dot(V_qq)=DF(X_t)V_qq,t+D2F(X_t)[U_q,t,U_q,t], "
                "V_qq,0=0"
            ),
            "uniform_ball_requirement": (
                "X ranges over the complete split ball; coefficient, U_q, and "
                "V_qq enclosures must include this dependence, not only the orbit"
            ),
            "fast_current_forcing": (
                "(-2v-6*epsilon*kappa_3*(v-1))*U_q,v(t)^2"
            ),
            "fast_delayed_forcing_each": (
                "3*epsilon*kappa_3*(v(t-tau_j)-1)*U_q,v(t-tau_j)^2"
            ),
            "recovery_forcing": "zero",
        },
        return_tube_and_event_contract={
            "target_split_return_ball_radius": SPLIT_RETURN_BALL_TARGET,
            "validated_section_ball_radius": VALIDATED_SECTION_BALL_RADIUS,
            "stage2_uniform_event_speed_on_section_ball_lower": section[
                "uniform_event_speed_lower_on_declared_section_ball"
            ],
            "required_tube_gate": (
                "the full returned history tube from the split ball stays inside "
                "the validated 0.01 section ball throughout the event window"
            ),
            "required_first_return_gate": (
                "one positive-oriented event near one period and no earlier hit "
                "for every history in the split ball"
            ),
            "tau_q": "-Dh_C[U_q(T)]/Dh_C[dot(X_T)]",
            "event_core_qq": (
                "W_qq=V_qq(T)+2*dot(U_q)(T)*tau_q+ddot(X_T)*tau_q^2"
            ),
            "tau_qq": "-Dh_C[W_qq]/Dh_C[dot(X_T)]",
            "return_hessian_qq": "Y_qq=W_qq+dot(X_T)*tau_qq",
            "time_coordinate": "physical time only",
        },
        stable_deflation_contract={
            "required_operation": (
                "compute Pi_s Y_qq=Y_qq-q*f(Y_qq)/f(q) as a correlated "
                "history enclosure before taking the sup norm"
            ),
            "right_eigenhistory_available": True,
            "left_adjoint_action_directed_upper_available": False,
            "acceptable_left_certificate": (
                "an adjoint Grushin eigencolumn with directed normalization and "
                "atom-plus-density action, or a direct bordered stable-deflation "
                "solve on Y_qq"
            ),
            "global_projection_norm_transfer_allowed": False,
            "reason": (
                "separate absolute bounds on Y_qq and the unstable scalar destroy "
                "the cancellation visible in the stable-output block"
            ),
        },
        pilot_error_allocation={
            "status": "design allocation only; no entry is a bound",
            "target": STABLE_OUTPUT_UU_TARGET,
            "final_mesh_center": final_center,
            "total_error_allowance_from_center": (
                "4.73888067198172624472"
            ),
            "heuristic_mesh_envelope_consumption": (
                "0.68569630871017750450"
            ),
            "remaining_after_heuristic_envelope": (
                "4.05318436327154874022"
            ),
            "suggested_directed_error_caps": {
                "center_rounding_and_polynomial_residual": "0.05",
                "validated_orbit_and_q_enclosures": "0.25",
                "continuous_history_kernel_discretization": "1.25",
                "physical_return_event_evaluation": "0.50",
                "stable_adjoint_deflation": "1.00",
                "uniform_split_ball_inflation": "1.00",
            },
            "suggested_caps_sum": "4.05",
        },
        actual_directed_input_budget=asdict(actual_budget),
        actual_directed_evaluation=asdict(actual_evaluation),
        coarse_other_block_interface={
            "simultaneous_safe_design_targets": DESIGN_BLOCK_TARGETS,
            "construction": (
                "1.5 times each Stage-4A heuristic envelope, except round the "
                "bottleneck stable-output uu target upward to 12"
            ),
            "design_perron_root_upper": design_evaluation[
                "perron_root_upper"
            ],
            "design_weighted_row_sum_upper": design_evaluation[
                "weighted_row_sum_upper"
            ],
            "design_self_map_slack_lower": design_evaluation[
                "self_map_slack_vector_lower"
            ],
            "targets_are_directed_bounds": False,
        },
        claim_status=claims,
    )


def build_stage4b_contract_result(repository: Path) -> dict[str, Any]:
    repository = repository.resolve()
    artifact = asdict(build_stage4b_contract_artifact(repository))
    return {
        "artifact": artifact,
        "manifest": {
            "schema_id": SCHEMA_ID,
            "result": RESULT_RELATIVE_PATH,
            "default_command": DEFAULT_COMMAND,
            "arithmetic_scope": ARITHMETIC_SCOPE,
            "artifact_sha256": canonical_sha256(artifact),
            "source_sha256": {
                relative: _sha256_path(repository / relative)
                for relative in SOURCE_MANIFEST
            },
            "parent_result_sha256": {
                STAGE2_RESULT_RELATIVE_PATH: STAGE2_RESULT_SHA256,
                STAGE3_RESULT_RELATIVE_PATH: STAGE3_RESULT_SHA256,
                STAGE4A_RESULT_RELATIVE_PATH: STAGE4A_RESULT_SHA256,
            },
            "environment": {
                "python": platform.python_version(),
                "platform": platform.platform(),
                "arithmetic": "exact contract logic plus Stage-4 rational evaluator",
            },
        },
    }


def validate_stage4b_contract_result(
    payload: Mapping[str, Any], repository: Path
) -> None:
    if not isinstance(payload, Mapping) or set(payload) != {"artifact", "manifest"}:
        raise ValueError("the Stage-4B result has the wrong outer schema")
    artifact = _mapping(payload.get("artifact"), "Stage-4B artifact")
    manifest = _mapping(payload.get("manifest"), "Stage-4B manifest")
    if set(artifact) != {field.name for field in fields(Stage4BContractArtifact)}:
        raise ValueError("the Stage-4B artifact schema changed")
    if (
        artifact.get("schema_id") != SCHEMA_ID
        or artifact.get("model_id") != MODEL_ID
        or artifact.get("branch") != BRANCH
    ):
        raise ValueError("the Stage-4B identity changed")
    claims = _mapping(artifact.get("claim_status"), "Stage-4B claims")
    if set(claims) != set(TRUE_FLAGS) | set(FALSE_FLAGS):
        raise ValueError("the Stage-4B claim ledger changed")
    if any(claims.get(name) is not True for name in TRUE_FLAGS):
        raise ValueError("a Stage-4B contract statement was weakened")
    if any(claims.get(name) is not False for name in FALSE_FLAGS):
        raise ValueError("an open Stage-4B theorem gate was promoted")
    bottleneck = _mapping(
        artifact.get("bottleneck_and_safe_target"), "Stage-4B target"
    )
    if (
        bottleneck.get("bottleneck_block") != "stable_output_uu_upper"
        or bottleneck.get("directed_design_target") != STABLE_OUTPUT_UU_TARGET
        or bottleneck.get("target_is_validated_bound") is not False
    ):
        raise ValueError("the Stage-4B bottleneck target changed")
    design = _mapping(
        artifact.get("design_target_matrix_evaluation"), "design evaluation"
    )
    if (
        design.get("graph_certificate_closes") is not True
        or Decimal(design["perron_root_upper"]) >= Decimal("0.075")
    ):
        raise ValueError("the safe design row stopped closing")
    actual = _mapping(
        artifact.get("actual_directed_input_budget"), "actual directed budget"
    )
    if any(actual.get(name) is not None for name in REQUIRED_NUMERIC_FIELDS):
        raise ValueError("an unvalidated Stage-4B numeric input was filled")
    if any(actual.get(name) is not False for name in REQUIRED_PROOF_FLAGS):
        raise ValueError("an unvalidated Stage-4B proof flag was promoted")
    evaluation = _mapping(
        artifact.get("actual_directed_evaluation"), "actual evaluation"
    )
    if (
        evaluation.get("input_complete") is not False
        or evaluation.get("strict_certificate_closes") is not False
        or set(evaluation.get("missing_inputs", ()))
        != set(REQUIRED_NUMERIC_FIELDS) | set(REQUIRED_PROOF_FLAGS)
    ):
        raise ValueError("the incomplete Stage-4B ingress was promoted")
    deflation = _mapping(
        artifact.get("stable_deflation_contract"), "stable deflation contract"
    )
    if (
        deflation.get("left_adjoint_action_directed_upper_available") is not False
        or deflation.get("global_projection_norm_transfer_allowed") is not False
    ):
        raise ValueError("stable deflation was bypassed")

    expected_manifest_fields = {
        "schema_id",
        "result",
        "default_command",
        "arithmetic_scope",
        "artifact_sha256",
        "source_sha256",
        "parent_result_sha256",
        "environment",
    }
    if set(manifest) != expected_manifest_fields:
        raise ValueError("the Stage-4B manifest schema changed")
    fixed = {
        "schema_id": SCHEMA_ID,
        "result": RESULT_RELATIVE_PATH,
        "default_command": DEFAULT_COMMAND,
        "arithmetic_scope": ARITHMETIC_SCOPE,
        "artifact_sha256": canonical_sha256(artifact),
        "parent_result_sha256": {
            STAGE2_RESULT_RELATIVE_PATH: STAGE2_RESULT_SHA256,
            STAGE3_RESULT_RELATIVE_PATH: STAGE3_RESULT_SHA256,
            STAGE4A_RESULT_RELATIVE_PATH: STAGE4A_RESULT_SHA256,
        },
    }
    if any(manifest.get(name) != value for name, value in fixed.items()):
        raise ValueError("the Stage-4B manifest fixed data changed")
    repository = repository.resolve()
    sources = _mapping(manifest.get("source_sha256"), "Stage-4B sources")
    if set(sources) != set(SOURCE_MANIFEST):
        raise ValueError("the Stage-4B source set changed")
    for relative in SOURCE_MANIFEST:
        if sources.get(relative) != _sha256_path(repository / relative):
            raise ValueError(f"the Stage-4B source changed: {relative}")
    for relative, digest in fixed["parent_result_sha256"].items():
        if _sha256_path(repository / relative) != digest:
            raise ValueError(f"the Stage-4B parent changed: {relative}")


__all__ = [
    "ARITHMETIC_SCOPE",
    "BLOCK_NAMES",
    "DEFAULT_COMMAND",
    "DESIGN_BLOCK_TARGETS",
    "FALSE_FLAGS",
    "GENERATOR_RELATIVE_PATH",
    "NOTE_RELATIVE_PATH",
    "RESULT_RELATIVE_PATH",
    "SCHEMA_ID",
    "SOURCE_MANIFEST",
    "SOURCE_RELATIVE_PATH",
    "STABLE_OUTPUT_UU_TARGET",
    "Stage4BContractArtifact",
    "Stage4BDirectedEvaluation",
    "Stage4BDirectedInputBudget",
    "TRUE_FLAGS",
    "build_stage4b_contract_artifact",
    "build_stage4b_contract_result",
    "canonical_sha256",
    "evaluate_stage4b_directed_budget",
    "validate_stage4b_contract_result",
]
