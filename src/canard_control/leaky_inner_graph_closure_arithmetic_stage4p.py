"""Stage-4P fail-closed graph-closure arithmetic for one and two returns.

This module does not prove a nonlinear return map or a stable graph.  It binds
the frozen Stage-4K/4L/4M/4N/5G-b results, replays the exact-rational matrix
Lyapunov--Perron inequalities, and exposes the monotone six-block feasible
region without pretending that there is a componentwise-largest rectangular
cap vector.

Two designs are kept disjoint.  The one-return design uses the proved Stage-4L
stable power pair.  The two-return design uses only the conditional squared
linear rates and fresh abstract blocks of D2(P^2); none of the one-return
Stage-4A Hessian diagnostics is admitted as evidence for those blocks.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR, localcontext
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
import platform
from typing import Any, Mapping

from canard_control.leaky_inner_enlarged_return_hessian_stage4m_contract import (
    RESULT_RELATIVE_PATH as STAGE4M_RESULT_RELATIVE_PATH,
    validate_stage4m_result,
)
from canard_control.leaky_inner_nonlinear_selected_return_tube_stage4n_feasibility import (
    RESULT_RELATIVE_PATH as STAGE4N_RESULT_RELATIVE_PATH,
    validate_stage4n_feasibility_result,
)
from canard_control.leaky_inner_stable_graph_enlargement_stage4k import (
    EXPECTED_STAGE4A_HEURISTIC_BLOCKS,
    RESULT_RELATIVE_PATH as STAGE4K_RESULT_RELATIVE_PATH,
    validate_stage4k_diagnostic_result,
)
from canard_control.leaky_inner_terminal_stable_row_stage4l import (
    RESULT_RELATIVE_PATH as STAGE4L_RESULT_RELATIVE_PATH,
    validate_stage4l_result,
)
from canard_control.leaky_projected_return_hessian_stage4_contract import (
    HESSIAN_FIELD_NAMES,
    MatrixLyapunovPerronInputBudget,
    ProjectedReturnHessianBlockBudget,
    evaluate_matrix_lyapunov_perron_majorant,
)
from canard_control.leaky_pulse_stable_coordinate_cone_stage5gb import (
    RESULT_RELATIVE_PATH as STAGE5GB_RESULT_RELATIVE_PATH,
    validate_stage5gb_result,
)
from canard_control.leaky_pulse_endpoint_functional_stage5ga import (
    RESULT_RELATIVE_PATH as STAGE5GA_RESULT_RELATIVE_PATH,
    validate_stage5ga_result,
)


SCHEMA_ID = "leaky-inner-graph-closure-arithmetic-stage4p-v1"
MODEL_ID = "autonomous-leaky-recovery-two-delay-fhn-bistable-proposal"
BRANCH = "inner_saddle_candidate_selected_near_period_return"
STATUS = "NONCLOSING_SOURCE_BOUND_GRAPH_ARITHMETIC_DESIGN"

SOURCE_RELATIVE_PATH = (
    "src/canard_control/leaky_inner_graph_closure_arithmetic_stage4p.py"
)
GENERATOR_RELATIVE_PATH = (
    "experiments/leaky_inner_graph_closure_arithmetic_stage4p.py"
)
RESULT_RELATIVE_PATH = (
    "experiments/results/leaky_inner_graph_closure_arithmetic_stage4p.json"
)
NOTE_RELATIVE_PATH = "docs/leaky-inner-graph-closure-arithmetic-stage4p.md"
TEST_RELATIVE_PATH = (
    "tests/test_leaky_inner_graph_closure_arithmetic_stage4p.py"
)

STAGE4K_RESULT_SHA256 = (
    "57119dc28bfa841b4f1a9dcddc3af542783493da94862ed2f7336202b05e2f5c"
)
STAGE4L_RESULT_SHA256 = (
    "672f92c7c456a54f39afab7d2a5f92b783311cc0ee5341a4d2e72a588039017e"
)
STAGE4M_RESULT_SHA256 = (
    "1a7f89c4c61480a76149b88ae6a15fa40b11425f4d678615af3469b59f75100c"
)
STAGE4N_RESULT_SHA256 = (
    "5e7214a2f5ba8ca22649c677a1d054b32342b5cc25966bd8e1da7600c605f1de"
)
STAGE5GB_RESULT_SHA256 = (
    "a16e9159d462c6b8f58851c2181147940f27e1a404ee4c2fbeb8999440cf8b64"
)
STAGE5GA_RESULT_SHA256 = (
    "56e847fc804ced75e6c2fbf09ccbec1bdeabf505638e093c0939c2f2e584dd8c"
)
STAGE4E_TRANSITIVE_RELATIVE_PATH = (
    "experiments/results/leaky_shared_yqq_deflation_stage4e.json"
)
STAGE4E_TRANSITIVE_SHA256 = (
    "ccdd6023f911e97785ec6f8be97b84d725d6af9f5051e1da602380d225e47acc"
)
PARENT_RESULT_SHA256 = {
    STAGE4K_RESULT_RELATIVE_PATH: STAGE4K_RESULT_SHA256,
    STAGE4L_RESULT_RELATIVE_PATH: STAGE4L_RESULT_SHA256,
    STAGE4M_RESULT_RELATIVE_PATH: STAGE4M_RESULT_SHA256,
    STAGE4N_RESULT_RELATIVE_PATH: STAGE4N_RESULT_SHA256,
    STAGE5GA_RESULT_RELATIVE_PATH: STAGE5GA_RESULT_SHA256,
    STAGE5GB_RESULT_RELATIVE_PATH: STAGE5GB_RESULT_SHA256,
}

SOURCE_MANIFEST = (
    SOURCE_RELATIVE_PATH,
    GENERATOR_RELATIVE_PATH,
    NOTE_RELATIVE_PATH,
    TEST_RELATIVE_PATH,
)
DEPENDENCY_SOURCE_MANIFEST = (
    "src/canard_control/leaky_inner_stable_graph_enlargement_stage4k.py",
    "src/canard_control/leaky_inner_terminal_stable_row_stage4l.py",
    "src/canard_control/leaky_inner_enlarged_return_hessian_stage4m_contract.py",
    "src/canard_control/leaky_inner_nonlinear_selected_return_tube_stage4n_feasibility.py",
    "src/canard_control/leaky_pulse_endpoint_functional_stage5ga.py",
    "src/canard_control/leaky_pulse_stable_coordinate_cone_stage5gb.py",
    "src/canard_control/leaky_projected_return_hessian_stage4_contract.py",
)
DEFAULT_COMMAND = (
    "OPENBLAS_NUM_THREADS=8 OMP_NUM_THREADS=1 PYTHONPATH=src /usr/bin/python3 "
    "experiments/leaky_inner_graph_closure_arithmetic_stage4p.py"
)
ARITHMETIC_SCOPE = (
    "byte and semantic binding of Stage 4K, final Stage 4L, Stage 4M, "
    "Stage 4N feasibility, Stage 5G-a, and Stage 5G-b; exact Fraction evaluation of "
    "one-return and conditional two-return matrix Lyapunov--Perron feasible "
    "regions, nonmixable axis frontiers, simultaneous reference rows, and "
    "split-output K_ret coupling; no nonlinear return, D2P or D2(P^2) block, "
    "stable graph, first return, crossing, onset, routing, capture, or safety "
    "promotion"
)

STABLE_SEED_RADIUS = "0.0094"
STABLE_GRAPH_RADIUS = "0.0097"
UNIT_UNSTABLE_GRAPH_RADIUS = "0.00025"
SPLIT_RETURN_RADIUS = "0.00995"
SEQUENCE_WEIGHT_BETA = "0.9999"
STABLE_POWER_CONSTANT = "1"
UNSTABLE_POWER_CONSTANT = "1"
ONE_RETURN_STABLE_RATE = (
    "0.00989642748161000022244199598343033161524171712346077110775160712"
)
REGISTERED_STABLE_RATE = "0.1"
ONE_RETURN_UNSTABLE_BACKWARD_RATE = (
    "0.549712198641301272665939640423769383243380071590152304446016306796024304322569720837972565017934"
)
TWO_RETURN_STABLE_RATE = "0.01"
ONE_RETURN_KRET_TARGET_LOWER = (
    "188.9122238810816331205615313733900338195719669891783770252080661252411"
)
ONE_RETURN_JOINT_MULTIPLIER = "5.532"
TWO_RETURN_JOINT_MULTIPLIER = "5.23"
TWO_RETURN_FINITE_SECTION_PILOT = {
    "stable_output_ss_upper": "0.0000000427",
    "stable_output_su_upper": "0.000000520",
    "stable_output_uu_upper": "30.2781",
    "unstable_output_ss_upper": "0.59394",
    "unstable_output_su_upper": "0.56667",
    "unstable_output_uu_upper": "158.5393",
}
TWO_RETURN_CONSERVATIVE_PILOT_ENVELOPE = {
    "stable_output_ss_upper": "0.000001",
    "stable_output_su_upper": "0.00001",
    "stable_output_uu_upper": "35",
    "unstable_output_ss_upper": "0.7",
    "unstable_output_su_upper": "0.7",
    "unstable_output_uu_upper": "180",
}
TWO_RETURN_RECOMMENDED_WIDE_BOX = {
    "stable_output_ss_upper": "1",
    "stable_output_su_upper": "10",
    "stable_output_uu_upper": "1000",
    "unstable_output_ss_upper": "5",
    "unstable_output_su_upper": "10",
    "unstable_output_uu_upper": "1000",
}
STRICT_DECIMAL_DIGITS = 72
_PARENT_CACHE: dict[str, dict[str, Mapping[str, Any]]] = {}

TOP_KEYS = {"design", "manifest"}
MANIFEST_KEYS = {
    "schema_id",
    "result",
    "default_command",
    "arithmetic_scope",
    "design_sha256",
    "numeric_core_sha256",
    "source_sha256",
    "dependency_source_sha256",
    "parent_result_sha256",
    "runtime",
}

TRUE_FLAGS = (
    "all_six_parent_results_byte_and_semantic_validated",
    "stage4l_sharp_stable_power_pair_imported",
    "stage5gb_full_interval_seed_cone_imported",
    "preferred_b_geometry_registered",
    "exact_six_block_feasible_inequalities_registered",
    "one_return_axis_frontiers_computed_exactly",
    "two_return_axis_frontiers_computed_exactly_conditionally",
    "axis_frontiers_declared_nonmixable",
    "one_return_joint_reference_row_closes_arithmetically",
    "two_return_joint_reference_row_closes_arithmetically_conditionally",
    "projected_caps_to_kret_pair_sum_implication_registered",
    "kret_and_six_projected_caps_declared_noninterchangeable",
    "selected_return_suffices_for_abstract_graph_registered",
    "first_return_identification_separated_from_graph_closure",
    "two_return_exact_orbit_smoothing_margin_positive",
    "one_and_two_return_hessian_ingress_kept_disjoint",
    "two_return_conservative_pilot_envelope_replayed",
    "two_return_recommended_wide_box_replayed",
    "kret_declared_sufficient_not_necessary_for_graph_arithmetic",
    "wide_box_conditional_unique_crossing_arithmetic_closes",
)
FALSE_FLAGS = (
    "one_return_nonlinear_selected_map_on_full_ball_validated",
    "two_return_nonlinear_selected_map_on_full_ball_validated",
    "two_return_full_ball_smoothing_window_validated",
    "common_selected_event_window_validated",
    "uniform_positive_event_speed_validated",
    "complete_returned_history_tube_validated",
    "one_return_kret_bound_validated",
    "two_return_kret_bound_validated",
    "one_return_six_projected_hessian_blocks_validated",
    "two_return_six_projected_hessian_blocks_validated",
    "one_return_majorant_with_certified_blocks_validated",
    "two_return_majorant_with_certified_blocks_validated",
    "split_return_ball_validated",
    "no_earlier_positive_hit_validated",
    "first_positive_return_validated",
    "quantitative_inner_stable_graph_validated",
    "selected_pulse_stable_sheet_crossing_validated",
    "unique_physical_pulse_onset_validated",
    "two_sided_basin_routing_validated",
    "outer_or_quiet_capture_from_both_sides_validated",
    "frequency_amplitude_safety_radius_validated",
    "asynchronous_network_safety_radius_validated",
)


@dataclass(frozen=True)
class Stage4PDesign:
    schema_id: str
    model_id: str
    branch: str
    status: str
    parent_result_sha256: dict[str, str]
    source_bound_parent_ingress: dict[str, Any]
    preferred_b_geometry: dict[str, Any]
    exact_feasible_region: dict[str, Any]
    one_return_design: dict[str, Any]
    two_return_design: dict[str, Any]
    kret_coupling: dict[str, Any]
    selected_versus_first_return: dict[str, Any]
    strict_numeric_ingress: dict[str, Any]
    acceptance_decision: dict[str, Any]
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
    number = Decimal(text)
    if not number.is_finite():
        raise ValueError("an exact decimal ingress is not finite")
    return Fraction(number)


def _decimal(value: Fraction, rounding: str, precision: int = 110) -> str:
    with localcontext() as context:
        context.prec = precision
        context.rounding = rounding
        return format(+(Decimal(value.numerator) / Decimal(value.denominator)), "f")


def _exact_decimal(value: Fraction) -> str:
    return _decimal(value, ROUND_FLOOR, 140)


def _fraction_text(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def _strict_bracket(
    value: Fraction, digits: int = STRICT_DECIMAL_DIGITS
) -> tuple[Fraction, Fraction]:
    """Return decimal-grid values strictly below and strictly above value."""

    scale = 10**digits
    quotient, remainder = divmod(value.numerator * scale, value.denominator)
    lower_integer = quotient if remainder else quotient - 1
    return Fraction(lower_integer, scale), Fraction(quotient + 1, scale)


def _json_roundtrip(value: Any) -> Any:
    return json.loads(
        json.dumps(value, sort_keys=True, ensure_ascii=True, allow_nan=False)
    )


def _load_parent(
    repository: Path,
    relative: str,
    expected_hash: str,
    validator: Any,
) -> Mapping[str, Any]:
    raw = (repository / relative).read_bytes()
    if sha256(raw).hexdigest() != expected_hash:
        raise ValueError(f"the Stage-4P parent changed: {relative}")
    payload = json.loads(raw)
    if not isinstance(payload, Mapping):
        raise ValueError(f"the Stage-4P parent is malformed: {relative}")
    validator(payload, repository, recompute=False)
    return payload


def _load_parents(repository: Path) -> dict[str, Mapping[str, Any]]:
    cache_key = str(repository.resolve())
    cached = _PARENT_CACHE.get(cache_key)
    if cached is not None and all(
        _sha256_path(repository / relative) == digest
        for relative, digest in PARENT_RESULT_SHA256.items()
    ):
        return cached
    loaded = {
        "stage4k": _load_parent(
            repository,
            STAGE4K_RESULT_RELATIVE_PATH,
            STAGE4K_RESULT_SHA256,
            validate_stage4k_diagnostic_result,
        ),
        "stage4l": _load_parent(
            repository,
            STAGE4L_RESULT_RELATIVE_PATH,
            STAGE4L_RESULT_SHA256,
            validate_stage4l_result,
        ),
        "stage4m": _load_parent(
            repository,
            STAGE4M_RESULT_RELATIVE_PATH,
            STAGE4M_RESULT_SHA256,
            validate_stage4m_result,
        ),
        "stage4n": _load_parent(
            repository,
            STAGE4N_RESULT_RELATIVE_PATH,
            STAGE4N_RESULT_SHA256,
            validate_stage4n_feasibility_result,
        ),
        "stage5ga": _load_parent(
            repository,
            STAGE5GA_RESULT_RELATIVE_PATH,
            STAGE5GA_RESULT_SHA256,
            validate_stage5ga_result,
        ),
        "stage5gb": _load_parent(
            repository,
            STAGE5GB_RESULT_RELATIVE_PATH,
            STAGE5GB_RESULT_SHA256,
            validate_stage5gb_result,
        ),
    }
    _PARENT_CACHE[cache_key] = loaded
    return loaded


def _rates(rate_s: Fraction, rate_u: Fraction) -> tuple[Fraction, Fraction, Fraction]:
    beta = _fraction(SEQUENCE_WEIGHT_BETA)
    return (
        Fraction(1, 1) / (beta - rate_s),
        rate_u / (1 - beta * rate_u),
        rate_u / (1 - beta * beta * rate_u),
    )


def _zero_blocks() -> dict[str, Fraction]:
    return {name: Fraction(0, 1) for name in HESSIAN_FIELD_NAMES}


def _q_value(blocks: Mapping[str, Fraction], output: str) -> Fraction:
    radius_s = _fraction(STABLE_GRAPH_RADIUS)
    radius_u = _fraction(UNIT_UNSTABLE_GRAPH_RADIUS)
    return (
        blocks[f"{output}_output_ss_upper"] * radius_s * radius_s / 2
        + blocks[f"{output}_output_su_upper"] * radius_s * radius_u
        + blocks[f"{output}_output_uu_upper"] * radius_u * radius_u / 2
    )


def _matrix(
    blocks: Mapping[str, Fraction], rate_s: Fraction, rate_u: Fraction
) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    radius_s = _fraction(STABLE_GRAPH_RADIUS)
    radius_u = _fraction(UNIT_UNSTABLE_GRAPH_RADIUS)
    a_s, a_u, _ = _rates(rate_s, rate_u)
    l_ss = (
        blocks["stable_output_ss_upper"] * radius_s
        + blocks["stable_output_su_upper"] * radius_u
    )
    l_su = (
        blocks["stable_output_su_upper"] * radius_s
        + blocks["stable_output_uu_upper"] * radius_u
    )
    l_us = (
        blocks["unstable_output_ss_upper"] * radius_s
        + blocks["unstable_output_su_upper"] * radius_u
    )
    l_uu = (
        blocks["unstable_output_su_upper"] * radius_s
        + blocks["unstable_output_uu_upper"] * radius_u
    )
    return a_s * l_ss, a_s * l_su, a_u * l_us, a_u * l_uu


def _determinant_i_minus_m(
    matrix: tuple[Fraction, Fraction, Fraction, Fraction]
) -> Fraction:
    m11, m12, m21, m22 = matrix
    return (1 - m11) * (1 - m22) - m12 * m21


def _contraction_boundary(
    background: Mapping[str, Fraction],
    block_name: str,
    rate_s: Fraction,
    rate_u: Fraction,
) -> tuple[Fraction | None, str | None]:
    def at(value: Fraction) -> tuple[Fraction, Fraction, Fraction, Fraction]:
        blocks = dict(background)
        blocks[block_name] = value
        return _matrix(blocks, rate_s, rate_u)

    matrix0 = at(Fraction(0, 1))
    matrix1 = at(Fraction(1, 1))
    matrix2 = at(Fraction(2, 1))
    candidates: list[tuple[Fraction, str]] = []
    for index, label in ((0, "m_ss<1"), (3, "m_uu<1")):
        slope = matrix1[index] - matrix0[index]
        if slope > 0:
            root = (1 - matrix0[index]) / slope
            if root > 0:
                candidates.append((root, label))
    det0 = _determinant_i_minus_m(matrix0)
    det1 = _determinant_i_minus_m(matrix1)
    det2 = _determinant_i_minus_m(matrix2)
    if det2 - 2 * det1 + det0 != 0:
        raise ArithmeticError("a one-block determinant ceased to be affine")
    det_slope = det1 - det0
    if det_slope < 0:
        root = det0 / (-det_slope)
        if root > 0:
            candidates.append((root, "det(I-M)>0"))
    if not candidates:
        return None, None
    return min(candidates, key=lambda item: item[0])


def _make_budget(
    blocks: Mapping[str, Fraction],
    rate_s: Fraction,
    rate_u: Fraction,
    evidence: str,
) -> MatrixLyapunovPerronInputBudget:
    return MatrixLyapunovPerronInputBudget(
        stable_power_rate_upper=_exact_decimal(rate_s),
        unstable_backward_rate_upper=_exact_decimal(rate_u),
        stable_power_constant_upper=STABLE_POWER_CONSTANT,
        unstable_backward_power_constant_upper=UNSTABLE_POWER_CONSTANT,
        sequence_weight_beta=SEQUENCE_WEIGHT_BETA,
        stable_seed_radius=STABLE_SEED_RADIUS,
        stable_graph_radius=STABLE_GRAPH_RADIUS,
        unstable_graph_radius=UNIT_UNSTABLE_GRAPH_RADIUS,
        validated_return_map_split_ball_radius_lower=SPLIT_RETURN_RADIUS,
        hessian_blocks=ProjectedReturnHessianBlockBudget(
            **{name: _exact_decimal(blocks[name]) for name in HESSIAN_FIELD_NAMES},
            evidence_status=evidence,
        ),
        evidence_status=evidence,
    )


def _metrics(evaluation: Any) -> dict[str, Any]:
    return {
        "perron_root_upper": evaluation.perron_root_upper,
        "self_map_slack_vector_lower": evaluation.self_map_slack_vector_lower,
        "graph_height_upper": evaluation.graph_height_upper,
        "graph_derivative_upper": evaluation.graph_derivative_upper,
        "contraction_closes": evaluation.contraction_closes,
        "self_map_closes": evaluation.self_map_closes,
        "split_ball_contains_graph_box": evaluation.split_ball_contains_graph_box,
        "raw_graph_arithmetic_closes": evaluation.graph_certificate_closes,
    }


def _self_map_boundary(
    background: Mapping[str, Fraction],
    block_name: str,
    rate_s: Fraction,
    rate_u: Fraction,
) -> Fraction:
    radius_s = _fraction(STABLE_GRAPH_RADIUS)
    radius_u = _fraction(UNIT_UNSTABLE_GRAPH_RADIUS)
    seed = _fraction(STABLE_SEED_RADIUS)
    a_s, a_u, _ = _rates(rate_s, rate_u)
    output = "stable" if block_name.startswith("stable_") else "unstable"
    slot = block_name.split("_output_")[1].split("_upper")[0]
    coefficient = {
        "ss": radius_s * radius_s / 2,
        "su": radius_s * radius_u,
        "uu": radius_u * radius_u / 2,
    }[slot]
    maximum_q = (radius_s - seed) / a_s if output == "stable" else radius_u / a_u
    blocks0 = dict(background)
    blocks0[block_name] = Fraction(0, 1)
    remaining = maximum_q - _q_value(blocks0, output)
    if remaining <= 0:
        raise ArithmeticError("the registered background already fails self-map")
    return remaining / coefficient


def _graph_frontier(
    background: Mapping[str, Fraction],
    block_name: str,
    rate_s: Fraction,
    rate_u: Fraction,
) -> dict[str, Any]:
    self_boundary = _self_map_boundary(background, block_name, rate_s, rate_u)
    contraction_boundary, contraction_gate = _contraction_boundary(
        background, block_name, rate_s, rate_u
    )
    if contraction_boundary is None or self_boundary <= contraction_boundary:
        boundary = self_boundary
        gate = "component_self_map"
    else:
        boundary = contraction_boundary
        gate = str(contraction_gate)
    lower, upper = _strict_bracket(boundary)
    lower_blocks = dict(background)
    lower_blocks[block_name] = lower
    upper_blocks = dict(background)
    upper_blocks[block_name] = upper
    lower_eval = evaluate_matrix_lyapunov_perron_majorant(
        _make_budget(lower_blocks, rate_s, rate_u, "Stage-4P strict lower probe")
    )
    upper_eval = evaluate_matrix_lyapunov_perron_majorant(
        _make_budget(upper_blocks, rate_s, rate_u, "Stage-4P rejecting upper probe")
    )
    if not lower_eval.graph_certificate_closes:
        raise ArithmeticError("a Stage-4P strict graph probe does not close")
    if upper_eval.graph_certificate_closes:
        raise ArithmeticError("a Stage-4P upper graph probe did not fail")
    return {
        "block": block_name,
        "background_semantics": (
            "all five other blocks fixed at the row declared by the containing ledger"
        ),
        "self_map_boundary_exact_fraction": _fraction_text(self_boundary),
        "self_map_boundary_decimal_lower": _decimal(self_boundary, ROUND_FLOOR),
        "contraction_boundary_exact_fraction": (
            None if contraction_boundary is None else _fraction_text(contraction_boundary)
        ),
        "contraction_boundary_decimal_lower": (
            None if contraction_boundary is None else _decimal(contraction_boundary, ROUND_FLOOR)
        ),
        "graph_boundary_exact_fraction": _fraction_text(boundary),
        "graph_boundary_decimal_lower": _decimal(boundary, ROUND_FLOOR),
        "limiting_graph_gate": gate,
        "strict_lower_probe": _exact_decimal(lower),
        "rejecting_upper_probe": _exact_decimal(upper),
        "strict_lower_probe_metrics": _metrics(lower_eval),
        "rejecting_upper_probe_metrics": _metrics(upper_eval),
    }


def _axis_frontiers(
    rate_s: Fraction, rate_u: Fraction, kret_target: Fraction
) -> list[dict[str, Any]]:
    background = _zero_blocks()
    records = []
    for name in HESSIAN_FIELD_NAMES:
        record = _graph_frontier(background, name, rate_s, rate_u)
        graph_boundary = Fraction(record["graph_boundary_exact_fraction"])
        combined = min(graph_boundary, kret_target)
        lower, upper = _strict_bracket(combined)
        limiting = (
            record["limiting_graph_gate"]
            if graph_boundary <= kret_target
            else "triangle_reconstructed_K_ret"
        )
        record.update(
            {
                "axis_only_other_five_blocks_zero": True,
                "axis_frontier_is_simultaneously_mixable": False,
                "kret_axis_boundary_exact_fraction": _fraction_text(kret_target),
                "graph_and_kret_axis_boundary_exact_fraction": _fraction_text(combined),
                "graph_and_kret_axis_boundary_decimal_lower": _decimal(
                    combined, ROUND_FLOOR
                ),
                "combined_limiting_gate": limiting,
                "combined_strict_lower_probe": _exact_decimal(lower),
                "combined_rejecting_upper_probe": _exact_decimal(upper),
                "combined_lower_passes": lower < combined,
                "combined_upper_fails": upper > combined,
            }
        )
        records.append(record)
    return records


def _heuristic_shape() -> dict[str, Fraction]:
    return {
        name: _fraction(str(EXPECTED_STAGE4A_HEURISTIC_BLOCKS[name]))
        for name in HESSIAN_FIELD_NAMES
    }


def _pair_sums(blocks: Mapping[str, Fraction]) -> dict[str, Fraction]:
    return {
        slot: (
            blocks[f"stable_output_{slot}_upper"]
            + blocks[f"unstable_output_{slot}_upper"]
        )
        for slot in ("ss", "su", "uu")
    }


def _joint_row(
    label: str,
    multiplier: Fraction,
    rate_s: Fraction,
    rate_u: Fraction,
    kret_target: Fraction,
    *,
    two_return: bool,
) -> dict[str, Any]:
    shape = _heuristic_shape()
    blocks = {name: multiplier * shape[name] for name in HESSIAN_FIELD_NAMES}
    evaluation = evaluate_matrix_lyapunov_perron_majorant(
        _make_budget(blocks, rate_s, rate_u, f"Stage-4P {label} reference row")
    )
    sums = _pair_sums(blocks)
    reconstructed = max(sums.values())
    if not evaluation.graph_certificate_closes or not reconstructed < kret_target:
        raise ArithmeticError("a registered Stage-4P joint reference row fails")
    return {
        "label": label,
        "multiplier_exact": _exact_decimal(multiplier),
        "block_targets": {
            name: _exact_decimal(blocks[name]) for name in HESSIAN_FIELD_NAMES
        },
        "allocation_shape_origin": (
            "Stage-4A one-return finite-section heuristic ratios used only as a proof-engineering allocation shape"
        ),
        "allocation_shape_is_a_directed_hessian_bound": False,
        "entered_into_strict_numeric_ingress": False,
        "two_return_blocks_are_inferred_from_one_return_blocks": False,
        "two_return_design": two_return,
        "exact_majorant_metrics": _metrics(evaluation),
        "pair_sum_reconstructed_kret_upper": _exact_decimal(reconstructed),
        "pair_sums": {slot: _exact_decimal(value) for slot, value in sums.items()},
        "kret_target_lower": _exact_decimal(kret_target),
        "kret_margin_lower": _decimal(kret_target - reconstructed, ROUND_FLOOR),
        "raw_graph_arithmetic_closes": True,
        "triangle_reconstructed_return_tube_arithmetic_closes": True,
        "certified_hessian_blocks_supplied": False,
        "certified_kret_supplied": False,
        "stable_graph_validated": False,
        "status": "CONDITIONAL_REFERENCE_ROW_ONLY",
    }


def _registered_block_row(
    label: str,
    decimal_blocks: Mapping[str, str],
    rate_s: Fraction,
    rate_u: Fraction,
    kret_target: Fraction,
    *,
    role: str,
) -> dict[str, Any]:
    if set(decimal_blocks) != set(HESSIAN_FIELD_NAMES):
        raise ValueError("a Stage-4P registered row does not have six blocks")
    blocks = {name: _fraction(str(decimal_blocks[name])) for name in HESSIAN_FIELD_NAMES}
    evaluation = evaluate_matrix_lyapunov_perron_majorant(
        _make_budget(blocks, rate_s, rate_u, f"Stage-4P {label}")
    )
    sums = _pair_sums(blocks)
    reconstructed = max(sums.values())
    if not evaluation.graph_certificate_closes:
        raise ArithmeticError(f"the registered Stage-4P row does not close: {label}")
    return {
        "label": label,
        "role": role,
        "blocks": {name: _exact_decimal(blocks[name]) for name in HESSIAN_FIELD_NAMES},
        "exact_majorant_metrics": _metrics(evaluation),
        "pair_sums": {slot: _exact_decimal(value) for slot, value in sums.items()},
        "pair_sum_reconstructed_kret_upper": _exact_decimal(reconstructed),
        "conditional_kret_target_lower": _exact_decimal(kret_target),
        "pair_sum_implies_conditional_kret_target": reconstructed < kret_target,
        "raw_graph_arithmetic_closes": True,
        "return_domain_is_validated_by_this_row": False,
        "blocks_are_source_bound_continuous_history_bounds": False,
        "entered_into_strict_numeric_ingress": False,
        "stable_graph_validated": False,
    }


def _centered_graph_frontiers(
    background: Mapping[str, str], rate_s: Fraction, rate_u: Fraction
) -> list[dict[str, Any]]:
    parsed = {name: _fraction(str(background[name])) for name in HESSIAN_FIELD_NAMES}
    records = []
    for name in HESSIAN_FIELD_NAMES:
        record = _graph_frontier(parsed, name, rate_s, rate_u)
        record["background_blocks"] = {
            block: _exact_decimal(value) for block, value in parsed.items()
        }
        record["frontiers_from_different_records_may_be_mixed"] = False
        records.append(record)
    return records


def _common_scaling_frontier(
    rate_s: Fraction, rate_u: Fraction, kret_target: Fraction
) -> dict[str, Any]:
    shape = _heuristic_shape()
    radius_s = _fraction(STABLE_GRAPH_RADIUS)
    radius_u = _fraction(UNIT_UNSTABLE_GRAPH_RADIUS)
    seed = _fraction(STABLE_SEED_RADIUS)
    a_s, a_u, _ = _rates(rate_s, rate_u)
    stable_self = (radius_s - seed) / (a_s * _q_value(shape, "stable"))
    unstable_self = radius_u / (a_u * _q_value(shape, "unstable"))
    graph_boundary = min(stable_self, unstable_self)
    graph_gate = (
        "stable_self_map" if stable_self <= unstable_self else "unstable_self_map"
    )
    kret_boundary = kret_target / max(_pair_sums(shape).values())
    combined = min(graph_boundary, kret_boundary)
    graph_lower, graph_upper = _strict_bracket(graph_boundary)
    lower_eval = evaluate_matrix_lyapunov_perron_majorant(
        _make_budget(
            {name: graph_lower * shape[name] for name in HESSIAN_FIELD_NAMES},
            rate_s,
            rate_u,
            "Stage-4P common graph lower probe",
        )
    )
    upper_eval = evaluate_matrix_lyapunov_perron_majorant(
        _make_budget(
            {name: graph_upper * shape[name] for name in HESSIAN_FIELD_NAMES},
            rate_s,
            rate_u,
            "Stage-4P common graph upper probe",
        )
    )
    if not lower_eval.graph_certificate_closes:
        raise ArithmeticError("the common graph lower probe fails")
    if upper_eval.self_map_closes or not upper_eval.contraction_closes:
        raise ArithmeticError("the common graph frontier gate changed")
    return {
        "shape_is_evidentiary": False,
        "stable_self_map_multiplier_boundary_exact_fraction": _fraction_text(
            stable_self
        ),
        "unstable_self_map_multiplier_boundary_exact_fraction": _fraction_text(
            unstable_self
        ),
        "graph_only_common_multiplier_boundary_decimal_lower": _decimal(
            graph_boundary, ROUND_FLOOR
        ),
        "graph_only_limiting_gate": graph_gate,
        "graph_lower_probe_metrics": _metrics(lower_eval),
        "graph_upper_probe_metrics": _metrics(upper_eval),
        "triangle_kret_common_multiplier_boundary_decimal_lower": _decimal(
            kret_boundary, ROUND_FLOOR
        ),
        "graph_and_triangle_kret_common_multiplier_boundary_decimal_lower": _decimal(
            combined, ROUND_FLOOR
        ),
        "joint_limiting_gate": (
            graph_gate
            if graph_boundary <= kret_boundary
            else "uu_pair_sum_to_K_ret"
        ),
        "componentwise_caps_at_different_frontiers_may_be_mixed": False,
    }


def _two_return_kret_target(stage4n: Mapping[str, Any]) -> tuple[Fraction, dict[str, str]]:
    pilot = _mapping(stage4n.get("pilot"), "Stage-4N pilot")
    target = _mapping(
        pilot.get("conditional_terminal_kernel_target"), "Stage-4N target"
    )
    multiplier = _mapping(target.get("unstable_multiplier_upper"), "unstable multiplier")
    mu_one = _fraction(str(multiplier.get("upper")))
    mu_two = mu_one * mu_one
    radius_s = _fraction(STABLE_GRAPH_RADIUS)
    radius_u = _fraction(UNIT_UNSTABLE_GRAPH_RADIUS)
    return_radius = _fraction(SPLIT_RETURN_RADIUS)
    rate_s_two = _fraction(TWO_RETURN_STABLE_RATE)
    linear = rate_s_two * radius_s + mu_two * radius_u
    slack = return_radius - linear
    if slack <= 0:
        raise ArithmeticError("the conditional two-return linear image exceeds the ball")
    kret_target = 2 * slack / (return_radius * return_radius)
    return kret_target, {
        "one_return_forward_unstable_multiplier_upper": _exact_decimal(mu_one),
        "conditional_two_return_forward_unstable_multiplier_upper": _exact_decimal(
            mu_two
        ),
        "conditional_two_return_linear_image_upper": _decimal(linear, ROUND_CEILING),
        "conditional_two_return_remainder_slack_lower": _decimal(
            slack, ROUND_FLOOR
        ),
        "conditional_two_return_kret_target_lower": _decimal(
            kret_target, ROUND_FLOOR
        ),
    }


def _conditional_wide_box_crossing(
    repository: Path,
    stage5ga: Mapping[str, Any],
    stage5gb: Mapping[str, Any],
    wide_row: Mapping[str, Any],
) -> dict[str, Any]:
    manifest5ga = _mapping(stage5ga.get("manifest"), "Stage-5G-a manifest")
    parent_sha = _mapping(
        manifest5ga.get("parent_sha256"), "Stage-5G-a parent hashes"
    )
    if (
        parent_sha.get(STAGE4E_TRANSITIVE_RELATIVE_PATH)
        != STAGE4E_TRANSITIVE_SHA256
        or _sha256_path(repository / STAGE4E_TRANSITIVE_RELATIVE_PATH)
        != STAGE4E_TRANSITIVE_SHA256
    ):
        raise ValueError("the transitive Stage-4E q-norm parent changed")
    stage4e = json.loads(
        (repository / STAGE4E_TRANSITIVE_RELATIVE_PATH).read_text(
            encoding="utf-8"
        )
    )
    artifact4e = _mapping(stage4e.get("artifact"), "Stage-4E artifact")
    base4e = _mapping(
        artifact4e.get("base_orbit_stable_output_uu"), "Stage-4E q ledger"
    )
    alpha_lower = _fraction(str(base4e.get("q_section_norm_lower")))
    if alpha_lower <= 0:
        raise ValueError("the Stage-4E q-norm lower bound is not positive")

    certificate5ga = _mapping(
        stage5ga.get("certificate"), "Stage-5G-a certificate"
    )
    endpoints = certificate5ga.get("endpoints")
    if not isinstance(endpoints, list) or len(endpoints) != 2:
        raise ValueError("the Stage-5G-a endpoint ledger changed")
    by_name = {str(item.get("name")): _mapping(item, "Stage-5G-a endpoint") for item in endpoints}
    left_interval = _mapping(
        by_name["minus"].get("functional_interval"), "left functional interval"
    )
    right_interval = _mapping(
        by_name["plus"].get("functional_interval"), "right functional interval"
    )
    left_lower = _fraction(str(left_interval.get("lower")))
    right_upper = _fraction(str(right_interval.get("upper")))
    if not left_lower > 0 > right_upper:
        raise ValueError("the Stage-5G-a endpoint functional signs changed")

    metrics = _mapping(
        wide_row.get("exact_majorant_metrics"), "two-return wide metrics"
    )
    unit_height_upper = _fraction(str(metrics.get("graph_height_upper")))
    unit_derivative_upper = _fraction(str(metrics.get("graph_derivative_upper")))
    physical_height_upper = unit_height_upper / alpha_lower
    physical_derivative_upper = unit_derivative_upper / alpha_lower
    left_margin = left_lower - physical_height_upper
    right_margin = -right_upper - physical_height_upper

    certificate5gb = _mapping(
        stage5gb.get("certificate"), "Stage-5G-b certificate"
    )
    slope = _mapping(
        certificate5gb.get("conditional_stable_gap_slope"),
        "Stage-5G-b slope",
    )
    action = _mapping(
        slope.get("parent_functional_action_interval"),
        "Stage-5G-b action interval",
    )
    derivative_ledger = _mapping(
        certificate5gb.get("derivative_ledger"), "Stage-5G-b derivative ledger"
    )
    stable_derivative_upper = _fraction(
        str(derivative_ledger.get("stable_projection_derivative_norm_upper"))
    )
    correction = physical_derivative_upper * stable_derivative_upper
    derivative_lower = _fraction(str(action.get("lower"))) - correction
    derivative_upper = _fraction(str(action.get("upper"))) + correction
    if not left_margin > 0 or not right_margin > 0 or not derivative_upper < 0:
        raise ArithmeticError("the conditional wide-box crossing arithmetic fails")
    common_height_target = _fraction("0.001")
    return {
        "stage5ga_result_sha256": STAGE5GA_RESULT_SHA256,
        "stage4e_q_norm_parent_sha256_via_stage5ga": STAGE4E_TRANSITIVE_SHA256,
        "coordinate_warning": (
            "the Lyapunov--Perron height and derivative are in unit-q_hat "
            "coordinates and may not be compared directly with f_phys values"
        ),
        "direct_unit_to_physical_comparison_forbidden": True,
        "normalization_adapter": (
            "psi_phys=psi_hat/alpha and Dpsi_phys=Dpsi_hat/alpha, "
            "alpha=||q_phys||_Y"
        ),
        "alpha_lower": _decimal(alpha_lower, ROUND_FLOOR),
        "unit_graph_height_upper": _decimal(unit_height_upper, ROUND_CEILING),
        "physical_graph_height_upper": _decimal(
            physical_height_upper, ROUND_CEILING
        ),
        "stage5ga_registered_common_height_target": "0.001",
        "registered_common_height_target_met": physical_height_upper <= common_height_target,
        "registered_target_is_only_a_sufficient_convenience": True,
        "left_functional_lower": _decimal(left_lower, ROUND_FLOOR),
        "right_functional_upper": _decimal(right_upper, ROUND_CEILING),
        "adjusted_left_gap_margin_lower": _decimal(left_margin, ROUND_FLOOR),
        "adjusted_right_gap_margin_lower": _decimal(right_margin, ROUND_FLOOR),
        "unit_graph_derivative_upper": _decimal(
            unit_derivative_upper, ROUND_CEILING
        ),
        "physical_graph_derivative_upper": _decimal(
            physical_derivative_upper, ROUND_CEILING
        ),
        "stable_projection_parameter_derivative_upper": _decimal(
            stable_derivative_upper, ROUND_CEILING
        ),
        "graph_derivative_correction_upper": _decimal(correction, ROUND_CEILING),
        "physical_gap_derivative_interval": {
            "lower": _decimal(derivative_lower, ROUND_FLOOR),
            "upper": _decimal(derivative_upper, ROUND_CEILING),
        },
        "conditional_endpoint_signs_close": True,
        "conditional_strict_negative_derivative_closes": True,
        "conditional_unique_selected_crossing_arithmetic_closes": True,
        "premises": (
            "a future source-bound two-return graph for the identical fixed "
            "splitting, containing the Stage-5G-b cone, satisfying the wide "
            "box majorant, and transferred to the physical q_phys chart"
        ),
        "future_graph_supplied": False,
        "selected_crossing_validated": False,
        "physical_onset_validated": False,
        "routing_or_capture_validated": False,
    }


def _runtime_record() -> dict[str, str]:
    return {
        "python": platform.python_version(),
        "python_implementation": platform.python_implementation(),
        "platform": platform.platform(),
        "arithmetic": (
            "fractions.Fraction exact formulas, strict decimal-grid brackets, "
            "and the frozen Stage-4 integer-square-root Perron evaluator"
        ),
        "installation": "fresh replay before fsync-backed atomic replacement",
    }


def _numeric_core(design: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "preferred_b_geometry": design["preferred_b_geometry"],
        "exact_feasible_region": design["exact_feasible_region"],
        "one_return_design": design["one_return_design"],
        "two_return_design": design["two_return_design"],
        "kret_coupling": design["kret_coupling"],
        "strict_numeric_ingress": design["strict_numeric_ingress"],
        "acceptance_decision": design["acceptance_decision"],
        "claim_status": design["claim_status"],
    }


def build_stage4p_design(repository: Path) -> Stage4PDesign:
    repository = repository.resolve()
    parents = _load_parents(repository)
    stage4k_artifact = _mapping(parents["stage4k"].get("artifact"), "Stage-4K artifact")
    stage4l_artifact = _mapping(parents["stage4l"].get("artifact"), "Stage-4L artifact")
    stage4m_contract = _mapping(parents["stage4m"].get("contract"), "Stage-4M contract")
    stage4n_pilot = _mapping(parents["stage4n"].get("pilot"), "Stage-4N pilot")
    stage5gb_certificate = _mapping(
        parents["stage5gb"].get("certificate"), "Stage-5G-b certificate"
    )

    stable_power = _mapping(
        stage4l_artifact.get("stable_power_certificate"), "Stage-4L stable power"
    )
    if (
        stable_power.get("one_step_norm_upper") != ONE_RETURN_STABLE_RATE
        or stable_power.get("stable_power_constant_upper") != STABLE_POWER_CONSTANT
        or stable_power.get("registered_stable_rate_upper") != REGISTERED_STABLE_RATE
        or stable_power.get("k_s_equals_one_validated") is not True
    ):
        raise ValueError("the final Stage-4L stable power pair changed")

    sensitivity = _mapping(
        stage4k_artifact.get("terminal_rate_sensitivity"),
        "Stage-4K preferred-B design",
    )
    budget = _mapping(sensitivity.get("matrix_input_budget"), "Stage-4K budget")
    if (
        sensitivity.get("stable_graph_radius_R_s") != STABLE_GRAPH_RADIUS
        or sensitivity.get("unit_unstable_graph_radius_R_u_hat")
        != UNIT_UNSTABLE_GRAPH_RADIUS
        or sensitivity.get("stable_seed_radius_r") != STABLE_SEED_RADIUS
        or sensitivity.get("graph_box_split_radius_sum") != SPLIT_RETURN_RADIUS
        or budget.get("unstable_backward_rate_upper")
        != ONE_RETURN_UNSTABLE_BACKWARD_RATE
    ):
        raise ValueError("the Stage-4K preferred-B geometry or unstable rate changed")

    cone = _mapping(
        stage5gb_certificate.get("two_ended_cone"), "Stage-5G-b cone"
    )
    cone_upper = _fraction(str(cone.get("cone_radius_upper")))
    if (
        cone.get("target_radius_exact") != "47/5000"
        or cone.get("cone_radius_strictly_below_target") is not True
        or not cone_upper < _fraction(STABLE_SEED_RADIUS)
    ):
        raise ValueError("the Stage-5G-b stable seed cone changed")

    n_target = _mapping(
        stage4n_pilot.get("conditional_terminal_kernel_target"),
        "Stage-4N target",
    )
    if n_target.get("strict_kernel_target_lower") != ONE_RETURN_KRET_TARGET_LOWER:
        raise ValueError("the Stage-4N conditional K_ret target changed")
    one_target = _fraction(ONE_RETURN_KRET_TARGET_LOWER)
    two_target, two_target_ledger = _two_return_kret_target(parents["stage4n"])

    rate_s_one = _fraction(ONE_RETURN_STABLE_RATE)
    rate_u_one = _fraction(ONE_RETURN_UNSTABLE_BACKWARD_RATE)
    rate_s_two = _fraction(TWO_RETURN_STABLE_RATE)
    rate_u_two = rate_u_one * rate_u_one
    one_axis = _axis_frontiers(rate_s_one, rate_u_one, one_target)
    two_axis = _axis_frontiers(rate_s_two, rate_u_two, two_target)

    one_joint = _joint_row(
        "one_return_joint_graph_and_triangle_tube_row",
        _fraction(ONE_RETURN_JOINT_MULTIPLIER),
        rate_s_one,
        rate_u_one,
        one_target,
        two_return=False,
    )
    two_joint = _joint_row(
        "two_return_separate_conditional_reference_row",
        _fraction(TWO_RETURN_JOINT_MULTIPLIER),
        rate_s_two,
        rate_u_two,
        two_target,
        two_return=True,
    )
    two_pilot_row = _registered_block_row(
        "two_return_conservative_finite_section_pilot_envelope",
        TWO_RETURN_CONSERVATIVE_PILOT_ENVELOPE,
        rate_s_two,
        rate_u_two,
        two_target,
        role=(
            "DIAGNOSTIC envelope around an independently reported N=180 "
            "P-composed-with-P finite-section pilot"
        ),
    )
    two_wide_row = _registered_block_row(
        "two_return_recommended_wide_proof_box",
        TWO_RETURN_RECOMMENDED_WIDE_BOX,
        rate_s_two,
        rate_u_two,
        two_target,
        role=(
            "recommended simultaneous target box for a future source-bound "
            "continuous-history D2(P^2) certificate"
        ),
    )
    two_centered_frontiers = _centered_graph_frontiers(
        TWO_RETURN_CONSERVATIVE_PILOT_ENVELOPE, rate_s_two, rate_u_two
    )
    wide_crossing = _conditional_wide_box_crossing(
        repository, parents["stage5ga"], parents["stage5gb"], two_wide_row
    )

    support = _mapping(
        stage4l_artifact.get("true_period_and_word_support"),
        "Stage-4L period support",
    )
    period_lower = _fraction(str(support.get("true_period_lower")))
    tau_max_upper = _fraction(str(support.get("tau1_upper")))
    one_smoothing_margin = period_lower - 2 * tau_max_upper
    two_smoothing_margin = 2 * period_lower - 2 * tau_max_upper
    if not one_smoothing_margin < 0 < two_smoothing_margin:
        raise ValueError("the one-versus-two return smoothing audit changed")

    null_blocks = {name: None for name in HESSIAN_FIELD_NAMES}
    claims = {name: True for name in TRUE_FLAGS}
    claims.update({name: False for name in FALSE_FLAGS})
    return Stage4PDesign(
        schema_id=SCHEMA_ID,
        model_id=MODEL_ID,
        branch=BRANCH,
        status=STATUS,
        parent_result_sha256=dict(PARENT_RESULT_SHA256),
        source_bound_parent_ingress={
            "stage4k_preferred_b_geometry_and_unstable_rate_chain_bound": True,
            "stage4l_selected_linear_map_only": True,
            "stage4l_sharp_stable_rate_upper": ONE_RETURN_STABLE_RATE,
            "stage4l_registered_power_pair": "K_s=1, rho_s=0.1",
            "stage4m_six_block_interface_and_projection_order_bound": True,
            "stage4m_actual_six_blocks_validated": False,
            "stage4n_one_return_kret_target_is_conditional_only": True,
            "stage4n_actual_kret_validated": False,
            "stage5ga_endpoint_functional_intervals_bound": True,
            "stage5gb_selected_pulse_stable_cone_bound": "47/5000",
            "stage5gb_seed_containment_strict": True,
        },
        preferred_b_geometry={
            "stable_seed_radius_r": STABLE_SEED_RADIUS,
            "stable_graph_radius_R_s": STABLE_GRAPH_RADIUS,
            "unit_unstable_graph_radius_R_u_hat": UNIT_UNSTABLE_GRAPH_RADIUS,
            "split_graph_box_radius_sum": SPLIT_RETURN_RADIUS,
            "sequence_weight_beta": SEQUENCE_WEIGHT_BETA,
            "fixed_splitting": "x=X_*+x_s+q_hat*x_u, ||q_hat||_Y=1",
            "split_norm": "||x_s||_Y+|x_u|",
            "geometry_is_a_registered_design": True,
            "return_domain_validated": False,
        },
        exact_feasible_region={
            "component_derivative_bounds": (
                "L_i,s=C_i,ss*R_s+C_i,su*R_u; "
                "L_i,u=C_i,su*R_s+C_i,uu*R_u"
            ),
            "kernel_coefficients": (
                "a_s=K_s/(beta-rho_s), a_u=K_u*rho_u/(1-beta*rho_u)"
            ),
            "matrix": "M=diag(a_s,a_u)*[[L_s,s,L_s,u],[L_u,s,L_u,u]]",
            "contraction_gates": "m_ss<1, m_uu<1, det(I-M)>0",
            "perron_equivalence": "for nonnegative 2x2 M these gates imply rho(M)<1",
            "quadratic_values": (
                "Q_i=C_i,ss*R_s^2/2+C_i,su*R_s*R_u+C_i,uu*R_u^2/2"
            ),
            "stable_self_map": "K_s*r+a_s*Q_s<=R_s",
            "unstable_self_map": "a_u*Q_u<=R_u",
            "return_domain_gate": "R_s+R_u<=R_return",
            "graph_height": "K_u*rho_u*Q_u/(1-beta^2*rho_u)",
            "graph_derivative": "d_u where (d_s,d_u)=(I-M)^(-1)(K_s,0)",
            "unique_componentwise_widest_cap_vector_exists": False,
            "reason_no_unique_widest_vector": (
                "all six caps trade against one another in Q_s,Q_u and det(I-M); "
                "axis frontiers are therefore deliberately nonmixable"
            ),
        },
        one_return_design={
            "map": "selected near-one-period phase-fixed return P",
            "stable_rate_upper": ONE_RETURN_STABLE_RATE,
            "stable_power_constant_upper": STABLE_POWER_CONSTANT,
            "unstable_backward_rate_upper": ONE_RETURN_UNSTABLE_BACKWARD_RATE,
            "unstable_backward_power_constant_upper": UNSTABLE_POWER_CONSTANT,
            "rates_are_source_bound": True,
            "axis_frontiers_other_five_zero": one_axis,
            "preferred_b_factor_two_baseline": {
                name: _exact_decimal(2 * value)
                for name, value in _heuristic_shape().items()
            },
            "factor_two_baseline_is_evidence": False,
            "common_scaling_frontier": _common_scaling_frontier(
                rate_s_one, rate_u_one, one_target
            ),
            "joint_reference_row": one_joint,
            "current_release_status": "NO_GO_MISSING_SELECTED_C2_MAP_TUBE_AND_SIX_BLOCKS",
        },
        two_return_design={
            "map": "selected near-two-period phase-fixed return P2",
            "conditional_linear_transfer": {
                "stable_rate_upper": TWO_RETURN_STABLE_RATE,
                "formula_stable": "rho_s,2<=0.1^2=0.01",
                "unstable_backward_rate_upper": _exact_decimal(rate_u_two),
                "formula_unstable": "rho_u,2<=rho_u,1^2",
                "power_constants": "K_s=K_u=1",
                "requires_exact_invariant_splitting_and_intertwining_transfer": True,
                "transfer_validated_here": False,
            },
            "smoothing_audit": {
                "required_full_ball_condition": "T2_minus-tau_max>tau_max",
                "equivalent_condition": "T2_minus>2*tau_max",
                "one_return_exact_orbit_margin_lower": _decimal(
                    one_smoothing_margin, ROUND_FLOOR
                ),
                "two_return_exact_orbit_margin_lower": _decimal(
                    two_smoothing_margin, ROUND_FLOOR
                ),
                "two_return_exact_orbit_center_passes": True,
                "two_return_full_ball_event_window_passes": False,
            },
            "composition_hessian_formula": (
                "D2(P^2)(x)[h,k]=D2P(Px)[DP(x)h,DP(x)k]+DP(Px)D2P(x)[h,k]"
            ),
            "direct_or_correlated_composition_certificate_required": True,
            "one_return_block_caps_may_be_squared_or_reused": False,
            "independently_reported_finite_section_pilot": {
                "truncation_N": 180,
                "approximate_blocks": dict(TWO_RETURN_FINITE_SECTION_PILOT),
                "source_bound_continuous_history_certificate": False,
                "entered_into_strict_numeric_ingress": False,
            },
            "conservative_pilot_envelope_replay": two_pilot_row,
            "isolated_graph_frontiers_holding_conservative_pilot_envelope": (
                two_centered_frontiers
            ),
            "recommended_wide_proof_box": two_wide_row,
            "wide_box_stage5gb_conditional_derivative_audit": {
                "future_graph_derivative_threshold": "16",
                "majorant_graph_derivative_upper": two_wide_row[
                    "exact_majorant_metrics"
                ]["graph_derivative_upper"],
                "strictly_below_threshold": (
                    _fraction(
                        str(
                            two_wide_row["exact_majorant_metrics"][
                                "graph_derivative_upper"
                            ]
                        )
                    )
                    < 16
                ),
                "graph_exists": False,
                "endpoint_stable_gap_signs_validated": False,
                "crossing_validated": False,
            },
            "wide_box_conditional_crossing_arithmetic": wide_crossing,
            "axis_frontiers_other_five_zero": two_axis,
            "common_scaling_frontier": _common_scaling_frontier(
                rate_s_two, rate_u_two, two_target
            ),
            "joint_reference_row": two_joint,
            "conditional_return_tube_ledger": two_target_ledger,
            "current_release_status": (
                "NO_GO_MISSING_FULL_BALL_SMOOTH_SELECTED_P2_MAP_AND_D2P2_BLOCKS"
            ),
        },
        kret_coupling={
            "one_return_conditional_target_lower": ONE_RETURN_KRET_TARGET_LOWER,
            "two_return_conditional_target_lower": _decimal(
                two_target, ROUND_FLOOR
            ),
            "projected_to_raw_split_formula": (
                "K_ret_from_caps=max(C_s,ss+C_u,ss, C_s,su+C_u,su, "
                "C_s,uu+C_u,uu)"
            ),
            "derivation": (
                "D2P=P_sD2P+q_hat*f_hat(D2P), ||q_hat||_Y=1, followed by "
                "the split-input bilinear expansion"
            ),
            "projected_caps_imply_raw_bound_only_if_fixed_correlated_split_used": True,
            "raw_to_projected_converse": (
                "a raw K_ret gives only C_s,ab<=||P_s||K_ret and "
                "C_u,ab<=||f_hat||K_ret"
            ),
            "stage4n_target_alone_implies_any_stage4m_cap": False,
            "kret_is_required_by_matrix_lyapunov_perron_arithmetic": False,
            "what_graph_arithmetic_requires_instead": (
                "a validated selected-map domain containing the split graph "
                "box and the six correlated projected Hessian blocks"
            ),
            "kret_role": (
                "one sufficient scalar route to prove nonlinear return-ball "
                "containment; it is not a necessary graph-transform input"
            ),
            "stage4m_common_13p2353_pair_sum_uu": _exact_decimal(
                _fraction("105.178488996792070958566234")
                + _fraction("346.72372256934974231438886")
            ),
            "stage4m_common_13p2353_box_implies_stage4n_target": False,
            "one_return_joint_row_pair_sum_uu": one_joint[
                "pair_sums"
            ]["uu"],
            "one_return_joint_row_implies_conditional_target": True,
            "two_return_joint_row_pair_sum_uu": two_joint[
                "pair_sums"
            ]["uu"],
            "two_return_joint_row_implies_conditional_target": True,
            "two_return_conservative_pilot_pair_sum_implies_target": (
                two_pilot_row["pair_sum_implies_conditional_kret_target"]
            ),
            "two_return_wide_box_pair_sum_implies_target": two_wide_row[
                "pair_sum_implies_conditional_kret_target"
            ],
            "two_return_wide_box_graph_arithmetic_closes_despite_pair_sum_failure": (
                two_wide_row["raw_graph_arithmetic_closes"]
                and not two_wide_row["pair_sum_implies_conditional_kret_target"]
            ),
            "independent_ambient_hessian_pilot_approx": "337",
            "ambient_pilot_exceeds_one_return_stage4n_target_diagnostically": True,
            "ambient_norm_may_replace_correlated_six_blocks": False,
            "tight_family_for_graph_common_scaling": "unstable_output blocks",
            "dominant_graph_self_map_contribution_in_reference_shape": (
                "unstable_output_ss_upper because it is weighted by R_s^2/2"
            ),
            "tight_family_for_triangle_kret": (
                "stable_output_uu_upper+unstable_output_uu_upper"
            ),
        },
        selected_versus_first_return={
            "abstract_graph_requires_first_positive_return": False,
            "abstract_graph_requires_no_earlier_hit": False,
            "abstract_graph_requires": (
                "one common C2 selected section map on the full graph box, a "
                "validated return domain, the invariant linear splitting, and "
                "six projected Hessian bounds in one normalization"
            ),
            "first_return_identification_requires_no_earlier_hit": True,
            "crossing_and_onset_pipeline_requires_first_return_semantics": True,
            "current_selected_map_on_full_ball_validated": False,
            "conclusion": (
                "stable-graph arithmetic can close before first-positive-return, "
                "but it cannot close before the selected C2 map itself exists"
            ),
        },
        strict_numeric_ingress={
            "one_return": {
                "stable_power_pair": {
                    "rho_s": ONE_RETURN_STABLE_RATE,
                    "K_s": STABLE_POWER_CONSTANT,
                },
                "stable_seed_cone_radius_upper": str(cone.get("cone_radius_upper")),
                "selected_return_map_parent": None,
                "validated_split_return_radius": None,
                "directed_uniform_hessian_blocks": dict(null_blocks),
                "actual_kret_upper": None,
                "majorant_with_certified_blocks": None,
                "stable_graph": None,
            },
            "two_return": {
                "conditional_linear_rate_pair_only": True,
                "full_ball_smoothing_event_window": None,
                "selected_two_return_map_parent": None,
                "validated_split_return_radius": None,
                "directed_uniform_D2P2_blocks": dict(null_blocks),
                "actual_kret2_upper": None,
                "majorant_with_certified_D2P2_blocks": None,
                "stable_graph": None,
            },
            "one_return_blocks_may_fill_two_return_slots": False,
            "evidence_status": "OPEN_FAIL_CLOSED",
        },
        acceptance_decision={
            "one_return_arithmetic_design": "GO",
            "one_return_theorem_release": "NO_GO",
            "two_return_arithmetic_design": "GO_CONDITIONAL",
            "two_return_theorem_release": "NO_GO",
            "first_new_one_return_hard_gate": (
                "source-bound signed event-aligned selected-return tube plus all "
                "six fixed-projection D2P blocks"
            ),
            "first_new_two_return_hard_gate": (
                "directed T2_minus>2*tau_max on the full ball, followed by a "
                "correlated complete-history D2(P^2) certificate"
            ),
            "first_positive_return_can_be_deferred": True,
            "scalar_kret_route_can_be_replaced_by_direct_return_domain_proof": True,
            "breakthrough_assessment": (
                "the graph-transform arithmetic has wide margins; a two-return "
                "map materially relaxes unstable graph caps and may unlock C2 "
                "smoothing, while the signed event/history certificate remains "
                "the genuine proof bottleneck"
            ),
        },
        theorem_boundary={
            "proved_here": (
                "source-bound parent identities, exact graph-closure formulas, "
                "nonmixable one-axis frontiers, conditional joint reference rows, "
                "K_ret coupling, and the exact-orbit one-versus-two-return smoothing audit"
            ),
            "not_proved_here": (
                "a nonlinear selected return on the full ball, a full-ball "
                "two-return smoothing window, K_ret, any D2P or D2(P^2) block, "
                "a stable graph, first return, crossing, onset, routing, capture, "
                "or safety theorem"
            ),
            "flagship_files_modified": False,
        },
        claim_status=claims,
    )


def build_stage4p_result(repository: Path) -> dict[str, Any]:
    repository = repository.resolve()
    design = asdict(build_stage4p_design(repository))
    return {
        "design": design,
        "manifest": {
            "schema_id": SCHEMA_ID,
            "result": RESULT_RELATIVE_PATH,
            "default_command": DEFAULT_COMMAND,
            "arithmetic_scope": ARITHMETIC_SCOPE,
            "design_sha256": canonical_sha256(design),
            "numeric_core_sha256": canonical_sha256(_numeric_core(design)),
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


def validate_stage4p_result(
    payload: Mapping[str, Any], repository: Path, *, recompute: bool = False
) -> None:
    if not isinstance(payload, Mapping) or set(payload) != TOP_KEYS:
        raise ValueError("the Stage-4P result has the wrong outer schema")
    design = _mapping(payload.get("design"), "Stage-4P design")
    manifest = _mapping(payload.get("manifest"), "Stage-4P manifest")
    if set(design) != {field.name for field in fields(Stage4PDesign)}:
        raise ValueError("the Stage-4P design schema changed")
    if (
        design.get("schema_id") != SCHEMA_ID
        or design.get("model_id") != MODEL_ID
        or design.get("branch") != BRANCH
        or design.get("status") != STATUS
        or design.get("parent_result_sha256") != PARENT_RESULT_SHA256
    ):
        raise ValueError("the Stage-4P identity changed")
    repository = repository.resolve()
    _load_parents(repository)

    claims = _mapping(design.get("claim_status"), "Stage-4P claims")
    if set(claims) != set(TRUE_FLAGS) | set(FALSE_FLAGS):
        raise ValueError("the Stage-4P claim ledger changed")
    if any(claims.get(name) is not True for name in TRUE_FLAGS):
        raise ValueError("a Stage-4P arithmetic fact was weakened")
    if any(claims.get(name) is not False for name in FALSE_FLAGS):
        raise ValueError("an open Stage-4P theorem gate was promoted")

    region = _mapping(design.get("exact_feasible_region"), "Stage-4P region")
    if (
        region.get("unique_componentwise_widest_cap_vector_exists") is not False
        or "nonmixable" not in str(region.get("reason_no_unique_widest_vector"))
    ):
        raise ValueError("the six-dimensional cap tradeoff was obscured")

    for key in ("one_return_design", "two_return_design"):
        subdesign = _mapping(design.get(key), key)
        records = subdesign.get("axis_frontiers_other_five_zero")
        if not isinstance(records, list) or len(records) != len(HESSIAN_FIELD_NAMES):
            raise ValueError(f"the {key} axis frontier count changed")
        if [item.get("block") for item in records] != list(HESSIAN_FIELD_NAMES):
            raise ValueError(f"the {key} axis frontier order changed")
        if any(
            item.get("axis_only_other_five_blocks_zero") is not True
            or item.get("axis_frontier_is_simultaneously_mixable") is not False
            or item.get("combined_lower_passes") is not True
            or item.get("combined_upper_fails") is not True
            for item in records
        ):
            raise ValueError(f"the {key} nonmixable frontier semantics changed")
        joint = _mapping(subdesign.get("joint_reference_row"), f"{key} joint row")
        metrics = _mapping(joint.get("exact_majorant_metrics"), f"{key} metrics")
        if (
            metrics.get("raw_graph_arithmetic_closes") is not True
            or joint.get("triangle_reconstructed_return_tube_arithmetic_closes")
            is not True
            or joint.get("allocation_shape_is_a_directed_hessian_bound") is not False
            or joint.get("entered_into_strict_numeric_ingress") is not False
            or joint.get("certified_hessian_blocks_supplied") is not False
            or joint.get("stable_graph_validated") is not False
        ):
            raise ValueError(f"the {key} reference row was promoted")

    two = _mapping(design.get("two_return_design"), "two-return design")
    transfer = _mapping(two.get("conditional_linear_transfer"), "two-return transfer")
    smoothing = _mapping(two.get("smoothing_audit"), "two-return smoothing")
    if (
        transfer.get("transfer_validated_here") is not False
        or two.get("one_return_block_caps_may_be_squared_or_reused") is not False
        or smoothing.get("two_return_exact_orbit_center_passes") is not True
        or smoothing.get("two_return_full_ball_event_window_passes") is not False
    ):
        raise ValueError("the conditional two-return route was promoted")
    for row_key in (
        "conservative_pilot_envelope_replay",
        "recommended_wide_proof_box",
    ):
        row = _mapping(two.get(row_key), f"two-return {row_key}")
        metrics = _mapping(row.get("exact_majorant_metrics"), f"{row_key} metrics")
        if (
            metrics.get("raw_graph_arithmetic_closes") is not True
            or row.get("blocks_are_source_bound_continuous_history_bounds") is not False
            or row.get("entered_into_strict_numeric_ingress") is not False
            or row.get("stable_graph_validated") is not False
        ):
            raise ValueError("a two-return design row was promoted")
    wide = _mapping(two.get("recommended_wide_proof_box"), "wide proof box")
    if wide.get("pair_sum_implies_conditional_kret_target") is not False:
        raise ValueError("the wide graph box was falsely made K_ret-compatible")
    crossing = _mapping(
        two.get("wide_box_conditional_crossing_arithmetic"),
        "wide-box conditional crossing",
    )
    derivative_interval = _mapping(
        crossing.get("physical_gap_derivative_interval"),
        "wide-box derivative interval",
    )
    if (
        crossing.get("direct_unit_to_physical_comparison_forbidden") is not True
        or "psi_phys=psi_hat/alpha" not in str(crossing.get("normalization_adapter"))
        or crossing.get("registered_common_height_target_met") is not False
        or crossing.get("conditional_endpoint_signs_close") is not True
        or crossing.get("conditional_strict_negative_derivative_closes") is not True
        or crossing.get("conditional_unique_selected_crossing_arithmetic_closes")
        is not True
        or Decimal(str(crossing.get("adjusted_left_gap_margin_lower"))) <= 0
        or Decimal(str(crossing.get("adjusted_right_gap_margin_lower"))) <= 0
        or Decimal(str(derivative_interval.get("upper"))) >= 0
        or crossing.get("future_graph_supplied") is not False
        or crossing.get("selected_crossing_validated") is not False
        or crossing.get("physical_onset_validated") is not False
    ):
        raise ValueError("the conditional crossing boundary or alpha adapter changed")

    distinction = _mapping(
        design.get("selected_versus_first_return"), "selected-versus-first"
    )
    if (
        distinction.get("abstract_graph_requires_first_positive_return") is not False
        or distinction.get("abstract_graph_requires_no_earlier_hit") is not False
        or distinction.get("first_return_identification_requires_no_earlier_hit")
        is not True
        or distinction.get("current_selected_map_on_full_ball_validated") is not False
    ):
        raise ValueError("selected-map and first-return logic was conflated")

    ingress = _mapping(design.get("strict_numeric_ingress"), "Stage-4P ingress")
    one_ingress = _mapping(ingress.get("one_return"), "one-return ingress")
    two_ingress = _mapping(ingress.get("two_return"), "two-return ingress")
    for blocks_key, sub in (
        ("directed_uniform_hessian_blocks", one_ingress),
        ("directed_uniform_D2P2_blocks", two_ingress),
    ):
        blocks = _mapping(sub.get(blocks_key), blocks_key)
        if set(blocks) != set(HESSIAN_FIELD_NAMES) or any(
            blocks.get(name) is not None for name in HESSIAN_FIELD_NAMES
        ):
            raise ValueError("an unvalidated Stage-4P Hessian block was filled")
    if (
        one_ingress.get("selected_return_map_parent") is not None
        or one_ingress.get("actual_kret_upper") is not None
        or one_ingress.get("stable_graph") is not None
        or two_ingress.get("selected_two_return_map_parent") is not None
        or two_ingress.get("actual_kret2_upper") is not None
        or two_ingress.get("stable_graph") is not None
        or ingress.get("one_return_blocks_may_fill_two_return_slots") is not False
    ):
        raise ValueError("the fail-closed Stage-4P ingress was filled")

    decision = _mapping(design.get("acceptance_decision"), "Stage-4P decision")
    if (
        decision.get("one_return_arithmetic_design") != "GO"
        or decision.get("one_return_theorem_release") != "NO_GO"
        or decision.get("two_return_arithmetic_design") != "GO_CONDITIONAL"
        or decision.get("two_return_theorem_release") != "NO_GO"
        or decision.get("first_positive_return_can_be_deferred") is not True
        or decision.get("scalar_kret_route_can_be_replaced_by_direct_return_domain_proof")
        is not True
    ):
        raise ValueError("the Stage-4P GO/NO-GO boundary changed")

    if set(manifest) != MANIFEST_KEYS:
        raise ValueError("the Stage-4P manifest schema changed")
    fixed_manifest = {
        "schema_id": SCHEMA_ID,
        "result": RESULT_RELATIVE_PATH,
        "default_command": DEFAULT_COMMAND,
        "arithmetic_scope": ARITHMETIC_SCOPE,
        "design_sha256": canonical_sha256(design),
        "numeric_core_sha256": canonical_sha256(_numeric_core(design)),
        "parent_result_sha256": PARENT_RESULT_SHA256,
        "runtime": _runtime_record(),
    }
    if any(manifest.get(name) != value for name, value in fixed_manifest.items()):
        raise ValueError("the Stage-4P fixed manifest changed")
    sources = _mapping(manifest.get("source_sha256"), "Stage-4P source manifest")
    dependencies = _mapping(
        manifest.get("dependency_source_sha256"), "Stage-4P dependency manifest"
    )
    if set(sources) != set(SOURCE_MANIFEST):
        raise ValueError("the Stage-4P source set changed")
    if set(dependencies) != set(DEPENDENCY_SOURCE_MANIFEST):
        raise ValueError("the Stage-4P dependency source set changed")
    for relative in SOURCE_MANIFEST:
        if sources.get(relative) != _sha256_path(repository / relative):
            raise ValueError(f"the Stage-4P source changed: {relative}")
    for relative in DEPENDENCY_SOURCE_MANIFEST:
        if dependencies.get(relative) != _sha256_path(repository / relative):
            raise ValueError(f"the Stage-4P dependency changed: {relative}")
    for relative, digest in PARENT_RESULT_SHA256.items():
        if _sha256_path(repository / relative) != digest:
            raise ValueError(f"the Stage-4P parent changed: {relative}")

    if recompute:
        expected = _json_roundtrip(asdict(build_stage4p_design(repository)))
        if dict(design) != expected:
            raise ValueError("the Stage-4P design differs from a fresh replay")


__all__ = [
    "ARITHMETIC_SCOPE",
    "BRANCH",
    "DEFAULT_COMMAND",
    "DEPENDENCY_SOURCE_MANIFEST",
    "FALSE_FLAGS",
    "GENERATOR_RELATIVE_PATH",
    "MANIFEST_KEYS",
    "MODEL_ID",
    "NOTE_RELATIVE_PATH",
    "ONE_RETURN_JOINT_MULTIPLIER",
    "ONE_RETURN_KRET_TARGET_LOWER",
    "ONE_RETURN_STABLE_RATE",
    "ONE_RETURN_UNSTABLE_BACKWARD_RATE",
    "PARENT_RESULT_SHA256",
    "RESULT_RELATIVE_PATH",
    "SCHEMA_ID",
    "SOURCE_MANIFEST",
    "SOURCE_RELATIVE_PATH",
    "SPLIT_RETURN_RADIUS",
    "STABLE_GRAPH_RADIUS",
    "STABLE_SEED_RADIUS",
    "STATUS",
    "Stage4PDesign",
    "TEST_RELATIVE_PATH",
    "TOP_KEYS",
    "TRUE_FLAGS",
    "TWO_RETURN_JOINT_MULTIPLIER",
    "TWO_RETURN_STABLE_RATE",
    "UNIT_UNSTABLE_GRAPH_RADIUS",
    "_numeric_core",
    "build_stage4p_design",
    "build_stage4p_result",
    "canonical_sha256",
    "validate_stage4p_result",
]
