"""Stage-4K v2 diagnostic design for an enlarged inner stable-graph box.

This module replays the exact-rational Stage-4 Lyapunov--Perron matrix
evaluator on one proposed anisotropic radius design.  It imports the six
Stage-4A finite-section heuristic blocks and evaluates simultaneous factors
one, three-halves, and two.  These rows answer only an arithmetic design
question: if the displayed inputs were future directed bounds, would the
registered positive majorant close?

They are not such bounds.  In particular, the stable power rate and
constant, the return ball, and all six Hessian blocks are hypothetical
ingress.  An expected future Stage-5G-b endpoint-cone number motivates the
v2 radii but is neither a bound parent nor a proved containment statement.
The strict proof ingress remains null, and every graph, intersection,
crossing, and onset flag remains false.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from decimal import Decimal, localcontext
from hashlib import sha256
import json
from pathlib import Path
import platform
from typing import Any, Mapping

from canard_control.leaky_projected_return_hessian_stage4_contract import (
    HESSIAN_FIELD_NAMES,
    MatrixLyapunovPerronInputBudget,
    ProjectedReturnHessianBlockBudget,
    RESULT_RELATIVE_PATH as STAGE4_RESULT_RELATIVE_PATH,
    evaluate_matrix_lyapunov_perron_majorant,
    validate_stage4_projected_return_result,
)
from canard_control.leaky_projected_return_hessian_stage4a_pilot import (
    RESULT_RELATIVE_PATH as STAGE4A_RESULT_RELATIVE_PATH,
    validate_stage4a_pilot_result,
)


SCHEMA_ID = "leaky-inner-stable-graph-enlargement-stage4k-diagnostic-v2"
MODEL_ID = "autonomous-leaky-recovery-two-delay-fhn-bistable-proposal"
BRANCH = "inner_saddle_candidate"
STATUS = "DIAGNOSTIC"
SOURCE_RELATIVE_PATH = (
    "src/canard_control/leaky_inner_stable_graph_enlargement_stage4k.py"
)
GENERATOR_RELATIVE_PATH = (
    "experiments/leaky_inner_stable_graph_enlargement_stage4k.py"
)
RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_inner_stable_graph_enlargement_stage4k.json"
)
NOTE_RELATIVE_PATH = "docs/leaky-inner-stable-graph-enlargement-stage4k.md"
TEST_RELATIVE_PATH = (
    "tests/test_leaky_inner_stable_graph_enlargement_stage4k.py"
)
DEFAULT_COMMAND = (
    "PYTHONPATH=src /usr/bin/python3 "
    "experiments/leaky_inner_stable_graph_enlargement_stage4k.py"
)
ARITHMETIC_SCOPE = (
    "source-bound replay of the Stage-4A finite-section heuristic block row; "
    "exact decimal-to-Fraction ingress; the existing exact-rational Stage-4 "
    "two-by-two Lyapunov--Perron evaluator, including its integer-square-root "
    "Perron upper bound; and three simultaneous heuristic inflation rows; "
    "one isolated terminal-rate sensitivity row; no directed Hessian block, "
    "stable power rate or constant, Stage-5G-b cone, full-pulse containment, "
    "return tube, stable graph, pulse intersection, crossing, or onset is "
    "proved"
)
SOURCE_MANIFEST = (
    SOURCE_RELATIVE_PATH,
    GENERATOR_RELATIVE_PATH,
    NOTE_RELATIVE_PATH,
)

STAGE4_RESULT_SHA256 = (
    "670fb21874fa26d953ee7bc2dc70f415c47ccc259690567fb20e5e00ea64fe13"
)
STAGE4A_RESULT_SHA256 = (
    "b9308d01137559f5b88e42f7120b6eb01490aaa6bda3ac7b6eed2fd2ce5421c7"
)

STABLE_POWER_RATE = (
    "0.995024916874584026786952988590018278886039540627453615"
)
TERMINAL_RATE_SENSITIVITY = "0.1"
TERMINAL_RATE_SENSITIVITY_STABLE_GRAPH_RADIUS = "0.0097"
TERMINAL_RATE_SENSITIVITY_UNSTABLE_GRAPH_RADIUS = "0.00025"
TERMINAL_RATE_SENSITIVITY_CEILING_ESTIMATE = "13.23539"
TERMINAL_RATE_SENSITIVITY_CEILING_LOWER_PROBE = "13.2353"
TERMINAL_RATE_SENSITIVITY_CEILING_UPPER_PROBE = "13.2354"
UNSTABLE_BACKWARD_RATE = (
    "0.549712198641301272665939640423769383243380071590152304446016306796024304322569720837972565017934"
)
STABLE_POWER_CONSTANT_HYPOTHESIS = "1"
UNSTABLE_BACKWARD_POWER_CONSTANT = "1"
SEQUENCE_WEIGHT_BETA = "0.9999"
STABLE_SEED_RADIUS = "0.0094"
STABLE_GRAPH_RADIUS = "0.0099"
UNIT_UNSTABLE_GRAPH_RADIUS = "0.00005"
HYPOTHETICAL_RETURN_BALL_RADIUS = "0.00995"
UNBOUND_STAGE5GB_EXPECTED_CONE_UPPER = "0.0093802671"
UNBOUND_STAGE5GB_EXPECTED_CONE_MARGIN = "0.0000197329"
UNBOUND_STAGE4E_ALPHA_LOWER = "0.0775543158981"
CONDITIONAL_PHYSICAL_GRAPH_HEIGHT_UPPER = "0.0004871"
UNBOUND_STAGE5GA_PHYSICAL_TARGET_RADIUS = "0.001"
INFLATION_MULTIPLIERS = ("1", "1.5", "2")

EXPECTED_STAGE4A_HEURISTIC_BLOCKS = {
    "stable_output_ss_upper": "0.0224686695028964572574",
    "stable_output_su_upper": "0.0887641356072132875488",
    "stable_output_uu_upper": "7.94681563672845125978",
    "unstable_output_ss_upper": "0.296931483708838817037",
    "unstable_output_su_upper": "0.283096126328013231177",
    "unstable_output_uu_upper": "26.1968918399544961062",
}

TRUE_FLAGS = (
    "status_is_diagnostic",
    "stage4a_heuristic_row_byte_bound",
    "recommended_anisotropic_radius_design_registered",
    "three_exact_rational_majorant_rows_computed",
    "numerical_closure_is_conditional_design_arithmetic_only",
    "strict_proof_ingress_kept_open",
    "cone_compatible_v2_design_registered",
    "terminal_rate_sensitivity_is_separate_diagnostic",
    "conditional_unit_to_physical_scaling_interface_registered",
)
FALSE_FLAGS = (
    "stage4a_heuristic_blocks_are_directed_uniform_bounds",
    "normalization_transfer_to_continuous_unit_y_coordinates_validated",
    "hypothetical_stable_power_rate_validated",
    "stable_power_constant_k_s_equals_one_validated",
    "stage5gb_endpoint_cone_bound_validated",
    "conditional_physical_scaling_premises_validated",
    "physical_graph_height_below_stage5ga_target_validated",
    "stage5ga_endpoint_stable_gap_signs_validated",
    "split_return_tube_validated",
    "first_positive_return_and_no_earlier_hit_validated",
    "six_projected_return_hessian_blocks_validated",
    "matrix_lyapunov_perron_contraction_validated",
    "matrix_lyapunov_perron_self_map_validated",
    "stable_seed_contains_full_pulse_interval_validated",
    "graph_radius_0p0099_validated",
    "inner_local_stable_graph_quantitatively_validated",
    "selected_pulse_stable_graph_intersection_validated",
    "physical_pulse_separator_crossing_validated",
    "unique_physical_pulse_onset_validated",
)

ROW_KEYS = {
    "multiplier",
    "input_hessian_blocks",
    "matrix_input_budget",
    "exact_majorant_evaluation",
    "proof_interpretation",
}
ROW_INTERPRETATION_KEYS = {
    "arithmetic_status",
    "raw_evaluator_closes_numerically",
    "hessian_blocks_are_directed_uniform_bounds",
    "stable_power_rate_is_validated",
    "stable_power_constant_is_validated",
    "return_ball_is_validated",
    "strict_graph_certificate_closes",
}
TERMINAL_RATE_SENSITIVITY_KEYS = {
    "status",
    "design_label",
    "source_hypothesis",
    "stable_power_rate_hypothesis",
    "stable_seed_radius_r",
    "stable_graph_radius_R_s",
    "unit_unstable_graph_radius_R_u_hat",
    "graph_box_split_radius_sum",
    "hypothetical_return_map_split_ball_radius",
    "multiplier",
    "input_hessian_blocks",
    "matrix_input_budget",
    "exact_majorant_evaluation",
    "proof_interpretation",
    "entered_into_main_majorant_rows",
    "entered_into_strict_proof_ingress",
    "simultaneous_multiplier_ceiling_estimate",
    "ceiling_lower_probe",
    "ceiling_upper_probe",
    "limiting_gate",
    "limiting_block_family",
}
SENSITIVITY_PROBE_KEYS = {
    "multiplier",
    "exact_majorant_evaluation",
}
STRICT_PROOF_INGRESS_KEYS = {
    "directed_uniform_hessian_blocks",
    "stable_power_rate_upper",
    "stable_power_constant_upper",
    "k_s_equals_one_validated",
    "validated_return_map_split_ball_radius_lower",
    "return_tube_history_radius_upper",
    "split_return_tube_validated",
    "first_positive_return_and_no_earlier_hit_validated",
    "validated_full_pulse_stable_coordinate_upper",
    "full_pulse_interval_stable_seed_containment_validated",
    "evidence_status",
}


@dataclass(frozen=True)
class Stage4KDiagnosticArtifact:
    schema_id: str
    model_id: str
    branch: str
    status: str
    parent_result_sha256: dict[str, str]
    coordinate_convention: dict[str, Any]
    recommended_design: dict[str, Any]
    cone_compatibility_design_driver: dict[str, Any]
    stage4a_heuristic_ingress: dict[str, Any]
    exact_majorant_rows: list[dict[str, Any]]
    terminal_rate_sensitivity: dict[str, Any]
    strict_proof_ingress: dict[str, Any]
    directed_upgrade_contract: dict[str, Any]
    scope_boundary: dict[str, Any]
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


def _json_roundtrip(value: Any) -> Any:
    """Return the exact JSON data model used by the installed result."""

    return json.loads(
        json.dumps(
            value,
            sort_keys=True,
            ensure_ascii=True,
            allow_nan=False,
        )
    )


def _mapping(value: Any, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{name} is missing")
    return value


def _runtime_record() -> dict[str, str]:
    return {
        "python": platform.python_version(),
        "python_implementation": platform.python_implementation(),
        "platform": platform.platform(),
        "arithmetic": (
            "decimal strings parsed by fractions.Fraction; directed decimal "
            "serialization and integer-square-root Perron upper bound"
        ),
        "installation": (
            "fresh replay validation before fsync-backed atomic replacement"
        ),
    }


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


def _scaled_decimal(value: str, multiplier: str) -> str:
    with localcontext() as context:
        context.prec = 120
        scaled = Decimal(value) * Decimal(multiplier)
        if not scaled.is_finite():
            raise ValueError("a Stage-4K scaled block is not finite")
        return format(scaled, "f")


def _scaled_blocks(
    blocks: Mapping[str, str], multiplier: str
) -> dict[str, str]:
    if set(blocks) != set(HESSIAN_FIELD_NAMES):
        raise ValueError("the Stage-4K six-block ingress changed")
    return {
        name: _scaled_decimal(str(blocks[name]), multiplier)
        for name in HESSIAN_FIELD_NAMES
    }


def _matrix_budget(
    blocks: Mapping[str, str],
    multiplier: str,
    *,
    stable_power_rate: str = STABLE_POWER_RATE,
    stable_seed_radius: str = STABLE_SEED_RADIUS,
    stable_graph_radius: str = STABLE_GRAPH_RADIUS,
    unstable_graph_radius: str = UNIT_UNSTABLE_GRAPH_RADIUS,
    return_ball_radius: str = HYPOTHETICAL_RETURN_BALL_RADIUS,
) -> MatrixLyapunovPerronInputBudget:
    return MatrixLyapunovPerronInputBudget(
        stable_power_rate_upper=stable_power_rate,
        unstable_backward_rate_upper=UNSTABLE_BACKWARD_RATE,
        stable_power_constant_upper=STABLE_POWER_CONSTANT_HYPOTHESIS,
        unstable_backward_power_constant_upper=(
            UNSTABLE_BACKWARD_POWER_CONSTANT
        ),
        sequence_weight_beta=SEQUENCE_WEIGHT_BETA,
        stable_seed_radius=stable_seed_radius,
        stable_graph_radius=stable_graph_radius,
        unstable_graph_radius=unstable_graph_radius,
        validated_return_map_split_ball_radius_lower=(
            return_ball_radius
        ),
        hessian_blocks=ProjectedReturnHessianBlockBudget(
            **dict(blocks),
            evidence_status=(
                "DIAGNOSTIC Stage-4A finite-section heuristic blocks scaled "
                f"simultaneously by {multiplier}; not directed bounds"
            ),
        ),
        evidence_status=(
            "DIAGNOSTIC hypothetical complete budget; the stable power rate, "
            "K_s=1, the return ball, and all six Hessian blocks are unproved"
        ),
    )


def _majorant_row(
    heuristic_blocks: Mapping[str, str],
    multiplier: str,
    *,
    stable_power_rate: str = STABLE_POWER_RATE,
    stable_graph_radius: str = STABLE_GRAPH_RADIUS,
    unstable_graph_radius: str = UNIT_UNSTABLE_GRAPH_RADIUS,
) -> dict[str, Any]:
    scaled = _scaled_blocks(heuristic_blocks, multiplier)
    budget = _matrix_budget(
        scaled,
        multiplier,
        stable_power_rate=stable_power_rate,
        stable_graph_radius=stable_graph_radius,
        unstable_graph_radius=unstable_graph_radius,
    )
    evaluation = evaluate_matrix_lyapunov_perron_majorant(budget)
    if not evaluation.graph_certificate_closes:
        raise ArithmeticError(
            f"the Stage-4K multiplier {multiplier} design stopped closing"
        )
    return {
        "multiplier": multiplier,
        "input_hessian_blocks": scaled,
        "matrix_input_budget": asdict(budget),
        "exact_majorant_evaluation": asdict(evaluation),
        "proof_interpretation": {
            "arithmetic_status": (
                "CLOSES_DIAGNOSTICALLY_UNDER_UNPROVED_INPUTS"
            ),
            "raw_evaluator_closes_numerically": True,
            "hessian_blocks_are_directed_uniform_bounds": False,
            "stable_power_rate_is_validated": False,
            "stable_power_constant_is_validated": False,
            "return_ball_is_validated": False,
            "strict_graph_certificate_closes": False,
        },
    }


def _terminal_rate_sensitivity_row(
    heuristic_blocks: Mapping[str, str],
) -> dict[str, Any]:
    row = _majorant_row(
        heuristic_blocks,
        "2",
        stable_power_rate=TERMINAL_RATE_SENSITIVITY,
        stable_graph_radius=TERMINAL_RATE_SENSITIVITY_STABLE_GRAPH_RADIUS,
        unstable_graph_radius=(
            TERMINAL_RATE_SENSITIVITY_UNSTABLE_GRAPH_RADIUS
        ),
    )
    return {
        "status": STATUS,
        "design_label": "preferred_if_stage4l_proves_rho_term_at_most_0p1",
        "source_hypothesis": (
            "prospective Stage-4L terminal stable-row target; Stage-4K does "
            "not bind or validate a Stage-4L result"
        ),
        "stable_power_rate_hypothesis": TERMINAL_RATE_SENSITIVITY,
        "stable_seed_radius_r": STABLE_SEED_RADIUS,
        "stable_graph_radius_R_s": (
            TERMINAL_RATE_SENSITIVITY_STABLE_GRAPH_RADIUS
        ),
        "unit_unstable_graph_radius_R_u_hat": (
            TERMINAL_RATE_SENSITIVITY_UNSTABLE_GRAPH_RADIUS
        ),
        "hypothetical_return_map_split_ball_radius": (
            HYPOTHETICAL_RETURN_BALL_RADIUS
        ),
        "graph_box_split_radius_sum": HYPOTHETICAL_RETURN_BALL_RADIUS,
        "multiplier": row["multiplier"],
        "input_hessian_blocks": row["input_hessian_blocks"],
        "matrix_input_budget": row["matrix_input_budget"],
        "exact_majorant_evaluation": row["exact_majorant_evaluation"],
        "proof_interpretation": row["proof_interpretation"],
        "entered_into_main_majorant_rows": False,
        "entered_into_strict_proof_ingress": False,
        "simultaneous_multiplier_ceiling_estimate": (
            TERMINAL_RATE_SENSITIVITY_CEILING_ESTIMATE
        ),
        "ceiling_lower_probe": _terminal_rate_sensitivity_probe(
            heuristic_blocks,
            TERMINAL_RATE_SENSITIVITY_CEILING_LOWER_PROBE,
        ),
        "ceiling_upper_probe": _terminal_rate_sensitivity_probe(
            heuristic_blocks,
            TERMINAL_RATE_SENSITIVITY_CEILING_UPPER_PROBE,
        ),
        "limiting_gate": "unstable_self_map",
        "limiting_block_family": "unstable-output C_u blocks",
    }


def _terminal_rate_sensitivity_probe(
    heuristic_blocks: Mapping[str, str], multiplier: str
) -> dict[str, Any]:
    scaled = _scaled_blocks(heuristic_blocks, multiplier)
    budget = _matrix_budget(
        scaled,
        multiplier,
        stable_power_rate=TERMINAL_RATE_SENSITIVITY,
        stable_graph_radius=TERMINAL_RATE_SENSITIVITY_STABLE_GRAPH_RADIUS,
        unstable_graph_radius=(
            TERMINAL_RATE_SENSITIVITY_UNSTABLE_GRAPH_RADIUS
        ),
    )
    return {
        "multiplier": multiplier,
        "exact_majorant_evaluation": asdict(
            evaluate_matrix_lyapunov_perron_majorant(budget)
        ),
    }


def build_stage4k_diagnostic_artifact(
    repository: Path,
) -> Stage4KDiagnosticArtifact:
    repository = repository.resolve()
    stage4 = _load_parent(
        repository,
        STAGE4_RESULT_RELATIVE_PATH,
        STAGE4_RESULT_SHA256,
        "Stage-4",
    )
    stage4a = _load_parent(
        repository,
        STAGE4A_RESULT_RELATIVE_PATH,
        STAGE4A_RESULT_SHA256,
        "Stage-4A",
    )
    validate_stage4_projected_return_result(stage4, repository)
    validate_stage4a_pilot_result(stage4a, repository)

    stage4_contract = _mapping(stage4.get("contract"), "Stage-4 contract")
    stage4_budget = _mapping(
        stage4_contract.get("matrix_input_budget"), "Stage-4 matrix budget"
    )
    if (
        stage4_budget.get("stable_power_rate_upper") != STABLE_POWER_RATE
        or stage4_budget.get("unstable_backward_rate_upper")
        != UNSTABLE_BACKWARD_RATE
        or stage4_budget.get("unstable_backward_power_constant_upper")
        != UNSTABLE_BACKWARD_POWER_CONSTANT
    ):
        raise ValueError("the Stage-4 rate ingress changed")

    stage4a_artifact = _mapping(stage4a.get("artifact"), "Stage-4A artifact")
    envelope = _mapping(
        stage4a_artifact.get("refinement_pilot_envelope"),
        "Stage-4A refinement envelope",
    )
    heuristic_blocks = dict(
        _mapping(
            envelope.get("projected_hessian_block_candidate_upper"),
            "Stage-4A heuristic blocks",
        )
    )
    if heuristic_blocks != EXPECTED_STAGE4A_HEURISTIC_BLOCKS:
        raise ValueError("the Stage-4A heuristic six-block row changed")
    stage4a_claims = _mapping(
        stage4a_artifact.get("claim_status"), "Stage-4A claims"
    )
    if (
        stage4a_claims.get("six_projected_return_hessian_blocks_validated")
        is not False
        or stage4a_claims.get("stable_power_constant_numeric_upper_validated")
        is not False
        or stage4a_claims.get("split_return_map_ball_validated") is not False
    ):
        raise ValueError("the Stage-4A diagnostic boundary changed")

    rows = [
        _majorant_row(heuristic_blocks, multiplier)
        for multiplier in INFLATION_MULTIPLIERS
    ]
    sensitivity = _terminal_rate_sensitivity_row(heuristic_blocks)
    sensitivity_graph_height = sensitivity["exact_majorant_evaluation"][
        "graph_height_upper"
    ]
    claims = {name: True for name in TRUE_FLAGS}
    claims.update({name: False for name in FALSE_FLAGS})
    twice_blocks = rows[-1]["input_hessian_blocks"]

    return Stage4KDiagnosticArtifact(
        schema_id=SCHEMA_ID,
        model_id=MODEL_ID,
        branch=BRANCH,
        status=STATUS,
        parent_result_sha256={
            STAGE4_RESULT_RELATIVE_PATH: STAGE4_RESULT_SHA256,
            STAGE4A_RESULT_RELATIVE_PATH: STAGE4A_RESULT_SHA256,
        },
        coordinate_convention={
            "proposed_fixed_splitting": "P_s=I-q_hat*f_hat",
            "proposed_unstable_vector": "q_hat=q/||q||_Y",
            "proposed_unstable_covector": "f_hat=||q||_Y*f",
            "proposed_normalization": "f_hat(q_hat)=1",
            "unstable_radius_symbol": "R_u_hat",
            "stage4a_finite_section_normalization": (
                "dominant right vector normalized in nodal l-infinity; used "
                "only as a heuristic proxy for the proposed unit-Y coordinate"
            ),
            "normalization_transfer_validated": False,
            "physical_grushin_scaling_adapter_validated": False,
            "pulse_ambient_unstable_coordinate_is_graph_radius": False,
            "conditional_unit_to_physical_scaling_interface": {
                "formula": "|psi|<=H_graph_hat/alpha",
                "sensitivity_design_graph_height_upper": (
                    sensitivity_graph_height
                ),
                "sensitivity_design_box_radius_R_u_hat": (
                    TERMINAL_RATE_SENSITIVITY_UNSTABLE_GRAPH_RADIUS
                ),
                "box_radius_is_not_substituted_for_graph_height": True,
                "unbound_stage4e_alpha_lower": UNBOUND_STAGE4E_ALPHA_LOWER,
                "conditional_physical_height_coarse_upper": (
                    CONDITIONAL_PHYSICAL_GRAPH_HEIGHT_UPPER
                ),
                "unbound_stage5ga_target_radius": (
                    UNBOUND_STAGE5GA_PHYSICAL_TARGET_RADIUS
                ),
                "same_q_f_normalization_required": True,
                "stage4e_alpha_parent_bound": False,
                "stage5ga_target_parent_bound": False,
                "sensitivity_graph_self_map_validated": False,
                "conditional_premises_validated": False,
                "physical_height_target_claim": False,
                "endpoint_stable_gap_signs_validated": False,
                "interpretation": (
                    "future conditional coordinate conversion only; it does "
                    "not prove a graph or either endpoint stable-gap sign"
                ),
            },
        },
        recommended_design={
            "stable_seed_radius_r": STABLE_SEED_RADIUS,
            "stable_graph_radius_R_s": STABLE_GRAPH_RADIUS,
            "unit_unstable_graph_radius_R_u_hat": (
                UNIT_UNSTABLE_GRAPH_RADIUS
            ),
            "sequence_weight_beta": SEQUENCE_WEIGHT_BETA,
            "stable_power_rate_upper": STABLE_POWER_RATE,
            "stable_power_rate_is_hypothetical": True,
            "unstable_backward_rate_upper": UNSTABLE_BACKWARD_RATE,
            "stable_power_constant_hypothesis": (
                STABLE_POWER_CONSTANT_HYPOTHESIS
            ),
            "unstable_backward_power_constant_upper": (
                UNSTABLE_BACKWARD_POWER_CONSTANT
            ),
            "graph_box_split_radius_sum": HYPOTHETICAL_RETURN_BALL_RADIUS,
            "hypothetical_return_map_split_ball_radius": (
                HYPOTHETICAL_RETURN_BALL_RADIUS
            ),
            "design_values_are_validated": False,
            "full_pulse_interval_seed_containment_validated": False,
        },
        cone_compatibility_design_driver={
            "status": STATUS,
            "anticipated_source": (
                "future Stage-5G-b two-endpoint cone certificate"
            ),
            "expected_stable_coordinate_upper": (
                UNBOUND_STAGE5GB_EXPECTED_CONE_UPPER
            ),
            "stable_seed_radius_r": STABLE_SEED_RADIUS,
            "expected_numeric_margin": (
                UNBOUND_STAGE5GB_EXPECTED_CONE_MARGIN
            ),
            "strict_expected_inequality_holds_numerically": True,
            "stage5gb_result_parent_bound": False,
            "cone_bound_is_directed_and_validated": False,
            "full_pulse_interval_seed_containment_validated": False,
            "entered_into_strict_proof_ingress": False,
            "interpretation": (
                "unbound design motivation only; Stage-4K neither proves "
                "the endpoint cone nor imports it as theorem evidence"
            ),
        },
        stage4a_heuristic_ingress={
            "source": STAGE4A_RESULT_RELATIVE_PATH,
            "construction": envelope["construction"],
            "six_block_candidate_upper": heuristic_blocks,
            "continuous_history_upper_bound": False,
            "directed_uniform_bound": False,
            "entered_into_strict_proof_ingress": False,
        },
        exact_majorant_rows=rows,
        terminal_rate_sensitivity=sensitivity,
        strict_proof_ingress={
            "directed_uniform_hessian_blocks": {
                name: None for name in HESSIAN_FIELD_NAMES
            },
            "stable_power_rate_upper": None,
            "stable_power_constant_upper": None,
            "k_s_equals_one_validated": False,
            "validated_return_map_split_ball_radius_lower": None,
            "return_tube_history_radius_upper": None,
            "split_return_tube_validated": False,
            "first_positive_return_and_no_earlier_hit_validated": False,
            "validated_full_pulse_stable_coordinate_upper": None,
            "full_pulse_interval_stable_seed_containment_validated": False,
            "evidence_status": (
                "OPEN: the Stage-4K rows do not supply any strict theorem ingress"
            ),
        },
        directed_upgrade_contract={
            "candidate_two_times_heuristic_caps": twice_blocks,
            "candidate_caps_are_directed_bounds": False,
            "priority_block": "stable_output_ss_upper",
            "secondary_priority_block": "unstable_output_ss_upper",
            "required_fixed_split_outputs": (
                "all six fixed-projection complete-history blocks of D2P on "
                "the entire anisotropic graph box"
            ),
            "required_stable_power": (
                "a directed continuous-history signed stable row proving the "
                "all-power pair (rho_s,K_s), including K_s=1"
            ),
            "required_return_geometry": (
                "a nonlinear moving-flow tube, a terminal event tube, one "
                "positive return, and exclusion of every earlier hit"
            ),
            "required_pulse_adapter": (
                "a separate source-bound Stage-5G-b parameter-sharded cone "
                "proof that the full pulse stable coordinate interval is "
                "contained in the seed radius"
            ),
            "projection_order": (
                "form stable deflation and unstable scalar action before "
                "taking continuous-history operator norms"
            ),
        },
        scope_boundary={
            "raw_evaluator_field_meaning": (
                "graph_certificate_closes means only that the exact algebraic "
                "majorant closes for the supplied complete numeric budget"
            ),
            "strict_implication_available": False,
            "reason": (
                "the stable power pair, return ball/tube, six uniform Hessian "
                "blocks, and anticipated Stage-5G-b cone are hypothetical or "
                "unbound"
            ),
            "stable_graph_claim": False,
            "pulse_intersection_claim": False,
            "pulse_crossing_claim": False,
            "pulse_onset_claim": False,
            "stage5g_files_modified": False,
            "stage5gb_result_parent_bound": False,
            "full_pulse_containment_claim": False,
            "flagship_files_modified": False,
        },
        claim_status=claims,
    )


def build_stage4k_diagnostic_result(repository: Path) -> dict[str, Any]:
    repository = repository.resolve()
    artifact = _json_roundtrip(
        asdict(build_stage4k_diagnostic_artifact(repository))
    )
    return {
        "artifact": artifact,
        "manifest": {
            "schema_id": SCHEMA_ID,
            "result": RESULT_RELATIVE_PATH,
            "default_command": DEFAULT_COMMAND,
            "arithmetic_scope": ARITHMETIC_SCOPE,
            "diagnostic_status": STATUS,
            "artifact_sha256": canonical_sha256(artifact),
            "source_sha256": {
                relative: _sha256_path(repository / relative)
                for relative in SOURCE_MANIFEST
            },
            "parent_result_sha256": {
                STAGE4_RESULT_RELATIVE_PATH: STAGE4_RESULT_SHA256,
                STAGE4A_RESULT_RELATIVE_PATH: STAGE4A_RESULT_SHA256,
            },
            "runtime": _runtime_record(),
        },
    }


def _validate_proof_boundary(artifact: Mapping[str, Any]) -> None:
    claims = _mapping(artifact.get("claim_status"), "Stage-4K claims")
    if set(claims) != set(TRUE_FLAGS) | set(FALSE_FLAGS):
        raise ValueError("the Stage-4K claim ledger changed")
    if any(claims.get(name) is not True for name in TRUE_FLAGS):
        raise ValueError("a Stage-4K diagnostic statement was weakened")
    if any(claims.get(name) is not False for name in FALSE_FLAGS):
        raise ValueError("an open Stage-4K proof gate was promoted")

    ingress = _mapping(
        artifact.get("strict_proof_ingress"), "Stage-4K strict proof ingress"
    )
    if set(ingress) != STRICT_PROOF_INGRESS_KEYS:
        raise ValueError("the Stage-4K strict ingress schema changed")
    blocks = _mapping(
        ingress.get("directed_uniform_hessian_blocks"),
        "Stage-4K directed Hessian ingress",
    )
    if set(blocks) != set(HESSIAN_FIELD_NAMES):
        raise ValueError("the Stage-4K strict six-block schema changed")
    if any(blocks.get(name) is not None for name in HESSIAN_FIELD_NAMES):
        raise ValueError("a heuristic Hessian block entered strict ingress")
    for name in (
        "stable_power_rate_upper",
        "stable_power_constant_upper",
        "validated_return_map_split_ball_radius_lower",
        "return_tube_history_radius_upper",
        "validated_full_pulse_stable_coordinate_upper",
    ):
        if ingress.get(name) is not None:
            raise ValueError(f"an unproved Stage-4K numeric input was filled: {name}")
    for name in (
        "k_s_equals_one_validated",
        "split_return_tube_validated",
        "first_positive_return_and_no_earlier_hit_validated",
        "full_pulse_interval_stable_seed_containment_validated",
    ):
        if ingress.get(name) is not False:
            raise ValueError(f"an open Stage-4K proof flag was promoted: {name}")

    scope = _mapping(artifact.get("scope_boundary"), "Stage-4K scope")
    for name in (
        "strict_implication_available",
        "stable_graph_claim",
        "pulse_intersection_claim",
        "pulse_crossing_claim",
        "pulse_onset_claim",
        "stage5g_files_modified",
        "stage5gb_result_parent_bound",
        "full_pulse_containment_claim",
        "flagship_files_modified",
    ):
        if scope.get(name) is not False:
            raise ValueError(f"the Stage-4K scope boundary changed: {name}")


def _validate_design_rows(artifact: Mapping[str, Any]) -> None:
    coordinates = _mapping(
        artifact.get("coordinate_convention"),
        "Stage-4K coordinate convention",
    )
    scaling = _mapping(
        coordinates.get("conditional_unit_to_physical_scaling_interface"),
        "Stage-4K conditional physical scaling",
    )
    sensitivity_for_scaling = _mapping(
        artifact.get("terminal_rate_sensitivity"),
        "Stage-4K scaling sensitivity",
    )
    sensitivity_evaluation_for_scaling = _mapping(
        sensitivity_for_scaling.get("exact_majorant_evaluation"),
        "Stage-4K scaling sensitivity evaluation",
    )
    sensitivity_graph_height = str(
        sensitivity_evaluation_for_scaling.get("graph_height_upper")
    )
    if (
        scaling.get("formula") != "|psi|<=H_graph_hat/alpha"
        or scaling.get("sensitivity_design_graph_height_upper")
        != sensitivity_graph_height
        or scaling.get("sensitivity_design_box_radius_R_u_hat")
        != TERMINAL_RATE_SENSITIVITY_UNSTABLE_GRAPH_RADIUS
        or scaling.get("box_radius_is_not_substituted_for_graph_height")
        is not True
        or scaling.get("unbound_stage4e_alpha_lower")
        != UNBOUND_STAGE4E_ALPHA_LOWER
        or scaling.get("conditional_physical_height_coarse_upper")
        != CONDITIONAL_PHYSICAL_GRAPH_HEIGHT_UPPER
        or scaling.get("unbound_stage5ga_target_radius")
        != UNBOUND_STAGE5GA_PHYSICAL_TARGET_RADIUS
        or scaling.get("same_q_f_normalization_required") is not True
        or Decimal(sensitivity_graph_height)
        / Decimal(UNBOUND_STAGE4E_ALPHA_LOWER)
        >= Decimal(CONDITIONAL_PHYSICAL_GRAPH_HEIGHT_UPPER)
        or Decimal(CONDITIONAL_PHYSICAL_GRAPH_HEIGHT_UPPER)
        >= Decimal(UNBOUND_STAGE5GA_PHYSICAL_TARGET_RADIUS)
    ):
        raise ValueError("the Stage-4K conditional scaling interface changed")
    for name in (
        "stage4e_alpha_parent_bound",
        "stage5ga_target_parent_bound",
        "sensitivity_graph_self_map_validated",
        "conditional_premises_validated",
        "physical_height_target_claim",
        "endpoint_stable_gap_signs_validated",
    ):
        if scaling.get(name) is not False:
            raise ValueError("the Stage-4K conditional scaling was promoted")

    design = _mapping(
        artifact.get("recommended_design"), "Stage-4K recommended design"
    )
    expected_design = {
        "stable_seed_radius_r": STABLE_SEED_RADIUS,
        "stable_graph_radius_R_s": STABLE_GRAPH_RADIUS,
        "unit_unstable_graph_radius_R_u_hat": UNIT_UNSTABLE_GRAPH_RADIUS,
        "sequence_weight_beta": SEQUENCE_WEIGHT_BETA,
        "stable_power_constant_hypothesis": STABLE_POWER_CONSTANT_HYPOTHESIS,
        "stable_power_rate_upper": STABLE_POWER_RATE,
        "hypothetical_return_map_split_ball_radius": (
            HYPOTHETICAL_RETURN_BALL_RADIUS
        ),
        "graph_box_split_radius_sum": HYPOTHETICAL_RETURN_BALL_RADIUS,
    }
    if any(design.get(name) != value for name, value in expected_design.items()):
        raise ValueError("the Stage-4K recommended design changed")
    if (
        Decimal(STABLE_GRAPH_RADIUS) + Decimal(UNIT_UNSTABLE_GRAPH_RADIUS)
        != Decimal(HYPOTHETICAL_RETURN_BALL_RADIUS)
    ):
        raise ValueError("the Stage-4K fallback split-radius sum changed")
    if (
        design.get("design_values_are_validated") is not False
        or design.get("stable_power_rate_is_hypothetical") is not True
        or design.get("full_pulse_interval_seed_containment_validated")
        is not False
    ):
        raise ValueError("the Stage-4K radius design was promoted")

    cone = _mapping(
        artifact.get("cone_compatibility_design_driver"),
        "Stage-4K cone design driver",
    )
    if (
        cone.get("status") != STATUS
        or cone.get("expected_stable_coordinate_upper")
        != UNBOUND_STAGE5GB_EXPECTED_CONE_UPPER
        or cone.get("stable_seed_radius_r") != STABLE_SEED_RADIUS
        or cone.get("expected_numeric_margin")
        != UNBOUND_STAGE5GB_EXPECTED_CONE_MARGIN
        or Decimal(STABLE_SEED_RADIUS)
        - Decimal(UNBOUND_STAGE5GB_EXPECTED_CONE_UPPER)
        != Decimal(UNBOUND_STAGE5GB_EXPECTED_CONE_MARGIN)
        or cone.get("strict_expected_inequality_holds_numerically") is not True
    ):
        raise ValueError("the Stage-4K unbound cone design driver changed")
    for name in (
        "stage5gb_result_parent_bound",
        "cone_bound_is_directed_and_validated",
        "full_pulse_interval_seed_containment_validated",
        "entered_into_strict_proof_ingress",
    ):
        if cone.get(name) is not False:
            raise ValueError("the unbound Stage-5G-b cone was promoted")

    heuristic = _mapping(
        artifact.get("stage4a_heuristic_ingress"),
        "Stage-4K Stage-4A ingress",
    )
    source_blocks = _mapping(
        heuristic.get("six_block_candidate_upper"),
        "Stage-4K heuristic blocks",
    )
    if dict(source_blocks) != EXPECTED_STAGE4A_HEURISTIC_BLOCKS:
        raise ValueError("the Stage-4K heuristic row changed")
    for name in (
        "continuous_history_upper_bound",
        "directed_uniform_bound",
        "entered_into_strict_proof_ingress",
    ):
        if heuristic.get(name) is not False:
            raise ValueError("the Stage-4A heuristic row was promoted")

    rows = artifact.get("exact_majorant_rows")
    if not isinstance(rows, list) or len(rows) != len(INFLATION_MULTIPLIERS):
        raise ValueError("the Stage-4K majorant row count changed")
    previous_perron = Decimal("-1")
    for row, multiplier in zip(rows, INFLATION_MULTIPLIERS, strict=True):
        if not isinstance(row, Mapping) or set(row) != ROW_KEYS:
            raise ValueError("a Stage-4K majorant row schema changed")
        if row.get("multiplier") != multiplier:
            raise ValueError("the Stage-4K multiplier order changed")
        scaled = _mapping(row.get("input_hessian_blocks"), "scaled blocks")
        if dict(scaled) != _scaled_blocks(
            EXPECTED_STAGE4A_HEURISTIC_BLOCKS, multiplier
        ):
            raise ValueError("a Stage-4K scaled Hessian row changed")
        budget = _mapping(row.get("matrix_input_budget"), "matrix budget")
        if (
            budget.get("stable_power_rate_upper") != STABLE_POWER_RATE
            or budget.get("stable_power_constant_upper")
            != STABLE_POWER_CONSTANT_HYPOTHESIS
            or budget.get("stable_seed_radius") != STABLE_SEED_RADIUS
            or budget.get("stable_graph_radius") != STABLE_GRAPH_RADIUS
            or budget.get("unstable_graph_radius")
            != UNIT_UNSTABLE_GRAPH_RADIUS
            or budget.get("validated_return_map_split_ball_radius_lower")
            != HYPOTHETICAL_RETURN_BALL_RADIUS
        ):
            raise ValueError("a Stage-4K hypothetical matrix budget changed")
        evaluation = _mapping(
            row.get("exact_majorant_evaluation"), "exact majorant evaluation"
        )
        if (
            evaluation.get("input_complete") is not True
            or evaluation.get("contraction_closes") is not True
            or evaluation.get("self_map_closes") is not True
            or evaluation.get("split_ball_contains_graph_box") is not True
            or evaluation.get("graph_certificate_closes") is not True
        ):
            raise ValueError("a Stage-4K exact arithmetic row stopped closing")
        perron = Decimal(str(evaluation["perron_root_upper"]))
        if perron <= previous_perron or perron >= Decimal("0.13"):
            raise ValueError("the Stage-4K Perron design margin changed")
        previous_perron = perron
        interpretation = _mapping(
            row.get("proof_interpretation"), "Stage-4K row interpretation"
        )
        if set(interpretation) != ROW_INTERPRETATION_KEYS:
            raise ValueError("the Stage-4K row interpretation schema changed")
        if (
            interpretation.get("arithmetic_status")
            != "CLOSES_DIAGNOSTICALLY_UNDER_UNPROVED_INPUTS"
            or interpretation.get("raw_evaluator_closes_numerically") is not True
        ):
            raise ValueError("the Stage-4K diagnostic arithmetic status changed")
        for name in (
            "hessian_blocks_are_directed_uniform_bounds",
            "stable_power_rate_is_validated",
            "stable_power_constant_is_validated",
            "return_ball_is_validated",
            "strict_graph_certificate_closes",
        ):
            if interpretation.get(name) is not False:
                raise ValueError("numeric closure was promoted to a proof")

    twice = _mapping(rows[-1]["exact_majorant_evaluation"], "twofold row")
    slacks = _mapping(
        twice.get("self_map_slack_vector_lower"), "twofold slacks"
    )
    if (
        Decimal(str(slacks["stable"])) <= Decimal("0.000026")
        or Decimal(str(slacks["unstable"])) <= Decimal("0.000014")
        or Decimal(str(twice["graph_height_upper"])) >= Decimal("0.000036")
        or Decimal(str(twice["graph_derivative_upper"])) >= Decimal("0.0081")
    ):
        raise ValueError("the Stage-4K twofold design margins changed")

    sensitivity = _mapping(
        artifact.get("terminal_rate_sensitivity"),
        "Stage-4K terminal-rate sensitivity",
    )
    if set(sensitivity) != TERMINAL_RATE_SENSITIVITY_KEYS:
        raise ValueError("the Stage-4K terminal-rate sensitivity schema changed")
    if (
        sensitivity.get("status") != STATUS
        or sensitivity.get("design_label")
        != "preferred_if_stage4l_proves_rho_term_at_most_0p1"
        or sensitivity.get("stable_power_rate_hypothesis")
        != TERMINAL_RATE_SENSITIVITY
        or sensitivity.get("stable_seed_radius_r") != STABLE_SEED_RADIUS
        or sensitivity.get("stable_graph_radius_R_s")
        != TERMINAL_RATE_SENSITIVITY_STABLE_GRAPH_RADIUS
        or sensitivity.get("unit_unstable_graph_radius_R_u_hat")
        != TERMINAL_RATE_SENSITIVITY_UNSTABLE_GRAPH_RADIUS
        or sensitivity.get("graph_box_split_radius_sum")
        != HYPOTHETICAL_RETURN_BALL_RADIUS
        or sensitivity.get("hypothetical_return_map_split_ball_radius")
        != HYPOTHETICAL_RETURN_BALL_RADIUS
        or sensitivity.get("multiplier") != "2"
        or sensitivity.get("entered_into_main_majorant_rows") is not False
        or sensitivity.get("entered_into_strict_proof_ingress") is not False
        or sensitivity.get("simultaneous_multiplier_ceiling_estimate")
        != TERMINAL_RATE_SENSITIVITY_CEILING_ESTIMATE
        or sensitivity.get("limiting_gate") != "unstable_self_map"
        or sensitivity.get("limiting_block_family")
        != "unstable-output C_u blocks"
    ):
        raise ValueError("the Stage-4K terminal-rate sensitivity was promoted")
    if not (
        Decimal(TERMINAL_RATE_SENSITIVITY_CEILING_LOWER_PROBE)
        < Decimal(TERMINAL_RATE_SENSITIVITY_CEILING_ESTIMATE)
        < Decimal(TERMINAL_RATE_SENSITIVITY_CEILING_UPPER_PROBE)
    ):
        raise ValueError("the Stage-4K sensitivity ceiling bracket changed")
    if (
        Decimal(TERMINAL_RATE_SENSITIVITY_STABLE_GRAPH_RADIUS)
        + Decimal(TERMINAL_RATE_SENSITIVITY_UNSTABLE_GRAPH_RADIUS)
        != Decimal(HYPOTHETICAL_RETURN_BALL_RADIUS)
    ):
        raise ValueError("the Stage-4K sensitivity split-radius sum changed")
    sensitivity_blocks = _mapping(
        sensitivity.get("input_hessian_blocks"),
        "Stage-4K sensitivity blocks",
    )
    if dict(sensitivity_blocks) != _scaled_blocks(
        EXPECTED_STAGE4A_HEURISTIC_BLOCKS, "2"
    ):
        raise ValueError("the Stage-4K sensitivity Hessian row changed")
    sensitivity_budget = _mapping(
        sensitivity.get("matrix_input_budget"),
        "Stage-4K sensitivity budget",
    )
    if (
        sensitivity_budget.get("stable_power_rate_upper")
        != TERMINAL_RATE_SENSITIVITY
        or sensitivity_budget.get("stable_power_constant_upper")
        != STABLE_POWER_CONSTANT_HYPOTHESIS
        or sensitivity_budget.get("stable_seed_radius") != STABLE_SEED_RADIUS
        or sensitivity_budget.get("stable_graph_radius")
        != TERMINAL_RATE_SENSITIVITY_STABLE_GRAPH_RADIUS
        or sensitivity_budget.get("unstable_graph_radius")
        != TERMINAL_RATE_SENSITIVITY_UNSTABLE_GRAPH_RADIUS
        or sensitivity_budget.get(
            "validated_return_map_split_ball_radius_lower"
        )
        != HYPOTHETICAL_RETURN_BALL_RADIUS
    ):
        raise ValueError("the Stage-4K sensitivity budget changed")
    sensitivity_evaluation = _mapping(
        sensitivity.get("exact_majorant_evaluation"),
        "Stage-4K sensitivity evaluation",
    )
    if any(
        sensitivity_evaluation.get(name) is not True
        for name in (
            "input_complete",
            "contraction_closes",
            "self_map_closes",
            "split_ball_contains_graph_box",
            "graph_certificate_closes",
        )
    ):
        raise ValueError("the Stage-4K sensitivity arithmetic stopped closing")
    sensitivity_slacks = _mapping(
        sensitivity_evaluation.get("self_map_slack_vector_lower"),
        "Stage-4K sensitivity slacks",
    )
    if (
        Decimal(str(sensitivity_evaluation["perron_root_upper"]))
        >= Decimal("0.025")
        or Decimal(str(sensitivity_slacks["stable"]))
        <= Decimal("0.000296")
        or Decimal(str(sensitivity_slacks["unstable"]))
        <= Decimal("0.000212")
        or Decimal(str(sensitivity_evaluation["graph_height_upper"]))
        >= Decimal("0.000038")
        or Decimal(str(sensitivity_evaluation["graph_derivative_upper"]))
        >= Decimal("0.0074")
    ):
        raise ValueError("the Stage-4K terminal-rate sensitivity changed")
    sensitivity_interpretation = _mapping(
        sensitivity.get("proof_interpretation"),
        "Stage-4K sensitivity interpretation",
    )
    if set(sensitivity_interpretation) != ROW_INTERPRETATION_KEYS:
        raise ValueError("the Stage-4K sensitivity interpretation changed")
    if (
        sensitivity_interpretation.get("raw_evaluator_closes_numerically")
        is not True
        or any(
            sensitivity_interpretation.get(name) is not False
            for name in (
                "hessian_blocks_are_directed_uniform_bounds",
                "stable_power_rate_is_validated",
                "stable_power_constant_is_validated",
                "return_ball_is_validated",
                "strict_graph_certificate_closes",
            )
        )
    ):
        raise ValueError("the Stage-4K sensitivity row was promoted")

    lower_probe = _mapping(
        sensitivity.get("ceiling_lower_probe"),
        "Stage-4K sensitivity lower probe",
    )
    upper_probe = _mapping(
        sensitivity.get("ceiling_upper_probe"),
        "Stage-4K sensitivity upper probe",
    )
    for probe, multiplier in (
        (lower_probe, TERMINAL_RATE_SENSITIVITY_CEILING_LOWER_PROBE),
        (upper_probe, TERMINAL_RATE_SENSITIVITY_CEILING_UPPER_PROBE),
    ):
        if set(probe) != SENSITIVITY_PROBE_KEYS:
            raise ValueError("a Stage-4K sensitivity probe schema changed")
        if probe.get("multiplier") != multiplier:
            raise ValueError("a Stage-4K sensitivity probe moved")
    lower_evaluation = _mapping(
        lower_probe.get("exact_majorant_evaluation"),
        "Stage-4K sensitivity lower evaluation",
    )
    upper_evaluation = _mapping(
        upper_probe.get("exact_majorant_evaluation"),
        "Stage-4K sensitivity upper evaluation",
    )
    if (
        lower_evaluation.get("graph_certificate_closes") is not True
        or lower_evaluation.get("self_map_closes") is not True
        or upper_evaluation.get("graph_certificate_closes") is not False
        or upper_evaluation.get("self_map_closes") is not False
    ):
        raise ValueError("the Stage-4K sensitivity ceiling probes changed")
    lower_slacks = _mapping(
        lower_evaluation.get("self_map_slack_vector_lower"),
        "Stage-4K sensitivity lower-probe slacks",
    )
    upper_slacks = _mapping(
        upper_evaluation.get("self_map_slack_vector_lower"),
        "Stage-4K sensitivity upper-probe slacks",
    )
    if (
        Decimal(str(lower_slacks["unstable"])) <= 0
        or Decimal(str(upper_slacks["unstable"])) >= 0
    ):
        raise ValueError("the Stage-4K unstable self-map bottleneck changed")


def validate_stage4k_diagnostic_result(
    payload: Mapping[str, Any], repository: Path, *, recompute: bool = True
) -> None:
    if not isinstance(payload, Mapping) or set(payload) != {"artifact", "manifest"}:
        raise ValueError("the Stage-4K result has the wrong outer schema")
    artifact = _mapping(payload.get("artifact"), "Stage-4K artifact")
    manifest = _mapping(payload.get("manifest"), "Stage-4K manifest")
    if set(artifact) != {
        field.name for field in fields(Stage4KDiagnosticArtifact)
    }:
        raise ValueError("the Stage-4K artifact schema changed")
    if (
        artifact.get("schema_id") != SCHEMA_ID
        or artifact.get("model_id") != MODEL_ID
        or artifact.get("branch") != BRANCH
        or artifact.get("status") != STATUS
    ):
        raise ValueError("the Stage-4K diagnostic identity changed")

    _validate_proof_boundary(artifact)
    _validate_design_rows(artifact)

    expected_manifest_fields = {
        "schema_id",
        "result",
        "default_command",
        "arithmetic_scope",
        "diagnostic_status",
        "artifact_sha256",
        "source_sha256",
        "parent_result_sha256",
        "runtime",
    }
    if set(manifest) != expected_manifest_fields:
        raise ValueError("the Stage-4K manifest schema changed")
    parent_hashes = {
        STAGE4_RESULT_RELATIVE_PATH: STAGE4_RESULT_SHA256,
        STAGE4A_RESULT_RELATIVE_PATH: STAGE4A_RESULT_SHA256,
    }
    fixed = {
        "schema_id": SCHEMA_ID,
        "result": RESULT_RELATIVE_PATH,
        "default_command": DEFAULT_COMMAND,
        "arithmetic_scope": ARITHMETIC_SCOPE,
        "diagnostic_status": STATUS,
        "artifact_sha256": canonical_sha256(artifact),
        "parent_result_sha256": parent_hashes,
        "runtime": _runtime_record(),
    }
    if any(manifest.get(name) != value for name, value in fixed.items()):
        raise ValueError("the Stage-4K manifest fixed data changed")

    repository = repository.resolve()
    sources = _mapping(manifest.get("source_sha256"), "Stage-4K sources")
    if set(sources) != set(SOURCE_MANIFEST):
        raise ValueError("the Stage-4K source manifest changed")
    for relative in SOURCE_MANIFEST:
        if sources.get(relative) != _sha256_path(repository / relative):
            raise ValueError(f"the Stage-4K source changed: {relative}")
    for relative, digest in parent_hashes.items():
        if _sha256_path(repository / relative) != digest:
            raise ValueError(f"the Stage-4K parent changed: {relative}")

    if recompute:
        expected = _json_roundtrip(
            asdict(build_stage4k_diagnostic_artifact(repository))
        )
        if dict(artifact) != expected:
            raise ValueError("the Stage-4K artifact differs from a fresh replay")


__all__ = [
    "ARITHMETIC_SCOPE",
    "BRANCH",
    "CONDITIONAL_PHYSICAL_GRAPH_HEIGHT_UPPER",
    "DEFAULT_COMMAND",
    "EXPECTED_STAGE4A_HEURISTIC_BLOCKS",
    "FALSE_FLAGS",
    "GENERATOR_RELATIVE_PATH",
    "HYPOTHETICAL_RETURN_BALL_RADIUS",
    "INFLATION_MULTIPLIERS",
    "NOTE_RELATIVE_PATH",
    "RESULT_RELATIVE_PATH",
    "SCHEMA_ID",
    "SEQUENCE_WEIGHT_BETA",
    "SOURCE_MANIFEST",
    "SOURCE_RELATIVE_PATH",
    "STABLE_GRAPH_RADIUS",
    "STABLE_SEED_RADIUS",
    "STATUS",
    "TERMINAL_RATE_SENSITIVITY",
    "TERMINAL_RATE_SENSITIVITY_CEILING_ESTIMATE",
    "TERMINAL_RATE_SENSITIVITY_CEILING_LOWER_PROBE",
    "TERMINAL_RATE_SENSITIVITY_CEILING_UPPER_PROBE",
    "TERMINAL_RATE_SENSITIVITY_STABLE_GRAPH_RADIUS",
    "TERMINAL_RATE_SENSITIVITY_UNSTABLE_GRAPH_RADIUS",
    "Stage4KDiagnosticArtifact",
    "TRUE_FLAGS",
    "UNIT_UNSTABLE_GRAPH_RADIUS",
    "UNBOUND_STAGE4E_ALPHA_LOWER",
    "UNBOUND_STAGE5GA_PHYSICAL_TARGET_RADIUS",
    "UNBOUND_STAGE5GB_EXPECTED_CONE_MARGIN",
    "UNBOUND_STAGE5GB_EXPECTED_CONE_UPPER",
    "build_stage4k_diagnostic_artifact",
    "build_stage4k_diagnostic_result",
    "canonical_sha256",
    "validate_stage4k_diagnostic_result",
]
